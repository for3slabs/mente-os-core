# 🔒 Estándar de Tratamiento de Datos — For3s OS (v1)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Estandar_De_Datos_For3s_v1.md → memory/archive/Estandar_De_Datos_For3s_v1.md (2026-07-30, ADR-029)

> **Qué es:** la respuesta formal a la pregunta de Brian (Ronda §5, bug #12):
> *"¿Cómo se trata la información una vez consumiendo la API? ¿Hay un estándar?"*.
> Documento de cara al CLIENTE + checklist interno SOC2-wedge (R9). Frente B · F6.
> **Honesto por diseño:** distingue lo que YA se cumple de lo que es futuro. Todo
> lo marcado ✅ está verificado en el server el 2026-07-15.

---

## 1 · Qué datos toca For3s (y cuáles NO)

Cuando un cliente consume la API (`/v1/chat`), For3s maneja tres tipos de dato, cada uno con su tabla:

| Dato | Dónde vive | Qué contiene | Nota |
|---|---|---|---|
| **Metadatos de uso** | `api_consumo` | cliente, tema, tokens, costo, ms, estado, fecha | Para facturar. **CERO contenido de mensajes.** |
| **Memoria conversacional** | `episodes_events` | el `content` del chat (para que For3s recuerde), su embedding | Aislada por cliente. Borrable (§4). |
| **Token BYOK** (si el cliente lo registra) | `secrets` | el token de Claude del cliente, **cifrado** (nonce + ciphertext) | AES-256-GCM. Jamás en claro, jamás se loguea, jamás viaja de vuelta. |

**For3s NO guarda:** tarjetas, contraseñas del cliente, ni el token BYOK en claro. La demo pública comparte una key; los clientes de pago tienen **su propia key** (la identidad ES la key, no falseable).

## 2 · Cifrado (en tránsito y en reposo)

- **En tránsito** ✅ — todo el tráfico entra por HTTPS (túnel Tailscale con TLS real). El puerto interno del canal solo escucha en `127.0.0.1`; internet entra únicamente por el túnel.
- **En reposo** ✅ — los secretos (BYOK) se cifran con **AES-256-GCM** bajo una KEK (Key Encryption Key) que vive **offline, nunca en el servidor**. El founder nunca ve un secreto en claro. (Los mensajes de la memoria se guardan sin cifrar en la BD del contenedor, aislada por instancia — ver §3; cifrado at-rest de toda la BD es futuro registrado.)

## 3 · Aislamiento (un cliente NUNCA ve lo de otro)

- ✅ Cada cliente recibe una **identidad sintética propia** (`user_id` en el rango reservado 9e9+, jamás choca con un usuario real). Su memoria vive en hilos `api:<cliente>:<tema>` que solo él toca (doctrina AI1).
- ✅ **Verificado E2E (F6):** cliente A borró su memoria y la de cliente B quedó **intacta**. Un cliente solo puede leer/borrar LO SUYO.
- ✅ Además, **aislamiento a nivel de contenedor**: cada For3s (instancia) corre en su propia red, BD, volúmenes y KEK — un cliente de pago puede tener su instancia dedicada.

## 4 · Retención y borrado a petición

- ✅ **Borrado a petición self-service** (`POST /v1/olvidar`, construido en F6): el cliente, con su key, borra toda su memoria (o un solo tema con `{"tema":"..."}`). Devuelve cuántos turnos borró. **Auditado.** Aislado: solo borra lo suyo.
- ✅ El borrado es **soft-delete** (recuperable un tiempo, como la microglía) y el **purgado físico definitivo** lo ejecuta el ciclo nocturno — mismo mecanismo probado del olvido real (H6).
- ✅ **Retención de uso:** los metadatos de facturación (`api_consumo`) son append-only y se conservan para el histórico de cobro; no contienen contenido de mensajes.
- **Futuro registrado:** ventana de retención configurable por cliente + borrado físico inmediato bajo demanda (hoy es a través del ciclo nocturno).

## 5 · Trazabilidad (auditoría inmutable)

- ✅ Cada llamada (`api_chat`), cada transición de cliente (alta/suspensión/revocación), cada BYOK y cada olvido queda en un **audit inmutable con cadena hash** (SHA-256 encadenado, tipo blockchain): alterar una entrada vieja rompe la cadena y se detecta en `/salud`.
- ✅ El trigger de BD **bloquea UPDATE y DELETE** sobre el audit (inmutabilidad forzada por Postgres, no solo por código).
- ✅ El audit **nunca guarda el contenido** del mensaje — solo quién, cuándo, qué acción y qué hilo.

## 6 · Límites y abuso

- ✅ **Cuotas por cliente** (rate por minuto + cuota diaria de llamadas y tokens), persistentes en BD.
- ✅ **BYOK obligatorio para clientes de pago**: su gasto va a SU cuenta de Claude, no al cupo compartido — protege la "joya" (el cupo de las instancias).
- ✅ **Estados de acceso**: activo → suspendido → revocado (terminal), cada transición auditada. Revocar mata la key al instante.

## 7 · Checklist SOC2-wedge (los 5 Trust Services Criteria — R9)

> No es una certificación (eso requiere auditor externo); es el **mapa** de qué ya cumplimos, para el pitch enterprise ("certificado de calidad B2B") y para saber qué falta.

| TSC | Qué pregunta | Estado For3s |
|---|---|---|
| **Security** | ¿proteges los datos? | ✅ TLS + BYOK cifrado AES-256 + KEK offline + aislamiento + audit inmutable + cuotas |
| **Availability** | ¿está disponible? | ✅ URL fija (túnel systemd-persistente) + check en /salud con alerta si cae + carga medida (F5: 100% éxito hasta 200 conc HTTP) |
| **Processing Integrity** | ¿procesa correcto? | ✅ metering exacto por llamada + verificación afirmativa + **2 races de concurrencia cerrados en F5** (seq + cadena audit) |
| **Confidentiality** | ¿guardas secretos? | ✅ BYOK cifrado, nunca en claro/logs + founder nunca ve secretos + aislamiento entre clientes |
| **Privacy** | ¿manejas bien datos personales? | ✅ borrado a petición (/v1/olvidar) + minimización (no se guarda de más) + trazabilidad · **futuro:** DPA formal + política pública |

## 8 · Resumen para el cliente (1 párrafo, lenguaje llano)

> *"Tus datos con For3s: el tráfico va cifrado (HTTPS). Si nos das tu propia llave de IA, la guardamos cifrada y nunca la vemos. Lo que conversas queda en TU espacio, aislado de otros clientes — nadie más lo lee. Puedes borrar toda tu memoria cuando quieras con un solo llamado a la API. Guardamos solo lo mínimo para facturarte (cuánto usaste, no qué dijiste), y cada operación queda registrada en un historial que no se puede alterar."*

---

**Estado F6:** Estándar v1 escrito + `/v1/olvidar` construido y verificado E2E (aislamiento probado:
A borra lo suyo, B intacto; sin key → 401; auditado). Commit del endpoint en el server.
Futuro registrado: cifrado at-rest de toda la BD · DPA formal · retención configurable · política
pública de privacidad. **Con F6, el Frente B queda COMPLETO (F1→F6).**
