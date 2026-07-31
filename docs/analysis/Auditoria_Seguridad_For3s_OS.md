# 🔒 Auditoría de Seguridad — For3s OS (¿exposición a demanda si lo vendo?)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Auditoria_Seguridad_For3s_OS.md → docs/analysis/Auditoria_Seguridad_For3s_OS.md (2026-07-30, ADR-029)

## Purpose

🔒 Auditoría de Seguridad — For3s OS (¿exposición a demanda si lo vendo?)


> **Origen:** Brian, 2026-07-15 (dentro del Frente E F3): *"dime For3s OS qué tan seguro es,
> dime si existe un error crítico que si alguien compra mis servicios puede haber demanda,
> necesito que me ayudes a decir qué tan segura es toda la infraestructura de For3s."*
> **Método:** auditoría del CÓDIGO REAL del server + pruebas de penetración EN VIVO (no opinión).
> Todo lo que dice ✅ está DEMOSTRADO con una prueba corrida en el server `for3s`, no asumido.

---

## 0 · VEREDICTO (la respuesta directa)

**¿Hay un error crítico que exponga a demanda hoy? → NO encontré ninguno.** El riesgo legal #1
(que un cliente vea los datos de otro cliente) está **cerrado por construcción y demostrado en
vivo**: 4 ataques de fuga entre clientes, ninguno filtró.

**Nivel de seguridad de la infraestructura: ALTO para vender a clientes PYME/negocio.** For3s tiene
más blindaje del que tienen la mayoría de productos SaaS en etapa temprana (cifrado autenticado,
audit inmutable a nivel BD, aislamiento multi-tenant por construcción, sandbox sin credenciales).

**Lo que SÍ cacé y ARREGLÉ en esta auditoría (riesgo medio, no crítico-legal):** el sandbox de
ejecución de código alcanzaba la red interna (puerto de la BD) y salía a internet → **cerrado**
(red segmentada, verificado en vivo). Ver §3.

**Matices honestos que un abogado/cliente enterprise preguntaría (no bloquean vender hoy, sí
conviene tenerlos en el contrato/roadmap):** ver §4. Ninguno es un agujero explotable; son
promesas que hay que redactar con cuidado (residencia de datos, la master key en disco v1).

---

## 1 · El riesgo #1 de demanda: fuga de datos ENTRE clientes → ✅ CERRADO (demostrado)

Si vendes For3s a Hotel A y Hotel B, lo que te lleva a juicio es que A vea la información de B.
Cómo está protegido y la prueba real:

- **Doble candado de aislamiento** (`For3s-OS/.../api_channel.py` + `memory.py`): cada cliente API recibe un
  `user_id` **único garantizado por la BD** (`api_clients.user_id bigint NOT NULL UNIQUE DEFAULT
  nextval(...)` — imposible que dos colisionen) y su memoria se scope-a por **sesión
  (`api:<cliente>:<tema>`) Y por `owner_user_id`**. Dos capas independientes: aunque una fallara,
  la otra aísla.
- La identidad **ES la API key** (`f3k_…`): el cliente no puede falsear su `client_id` en un header
  para hacerse pasar por otro — se deriva del hash de su key.

**PRUEBA EN VIVO (pentest_aislamiento, corrida en el server):** planté un secreto en Hotel A ("caja
fuerte 7391, cliente VIP Ramírez") y otro en Hotel B, y ataqué:
| Ataque | Resultado |
|---|---|
| B busca por significado el secreto de A en su hilo | ✅ **0 fugas** |
| B con el `scope` (user_id) de A robado | ✅ **0 fugas** (la sesión también aísla) |
| A ve LO SUYO (control: el aislamiento no rompe la función) | ✅ sí, funciona |
| `/olvidar` con `client_id = "%"` (comodín para borrar memoria ajena) | ✅ **borraría 0** (escape LIKE) |

**Veredicto: SÓLIDO.** El escape LIKE del `/olvidar` (`_escapar_like` + `ESCAPE '\'`) cierra la
inyección que ya se había cazado y explotado en la auditoría del Molde (M4) — sigue fija.

## 2 · Los otros pilares (auditados en código + probados)

| Pilar | Estado | Evidencia |
|---|---|---|
| **Cifrado de secretos / BYOK** | ✅ fuerte | AES-256-GCM (autenticado, no solo cifrado) + nonce aleatorio por operación + HKDF deriva **una clave por workspace** desde la master → un cliente no descifra los secrets de otro ni con acceso a la BD (`crypto.py`). |
| **Audit inmutable** | ✅ real a nivel BD | Intenté `DELETE FROM audit_events` con psql directo → **rechazado por trigger** (`RAISE EXCEPTION 'audit_events es inmutable'`). Hash-chain SHA-256 encadenado. No hay UPDATE/DELETE ni siendo admin de la BD. |
| **PII en el rastro (GDPR)** | ✅ limpio | El audit del canal API guarda **solo metadatos** (`{session}`, tokens) — **nunca el contenido** de la conversación. El rastro no es una fuga de datos personales. |
| **Auth del canal API** | ✅ correcto | SHA-256 de la key + `hmac.compare_digest` (timing-safe) + fail-closed ante cualquier error + gates de estado/expiración/scope. La demo y los clientes van por caminos separados. |
| **Sandbox sin credenciales** | ✅ | El contenedor que ejecuta código del LLM **no tiene** `DATABASE_URL`, password, ni tokens en su entorno (verificado en vivo: env sensible = NINGUNA). |
| **Errores mudos hacia afuera** | ✅ | El canal API responde `error interno` genérico; el detalle va solo al log interno → no filtra estructura/stack al atacante. |

## 3 · 🔴→✅ HALLAZGO cazado y ARREGLADO en esta auditoría: red del sandbox

**Qué encontré (prueba en vivo):** el sandbox de ejecución (donde corre el código que el LLM
escribe en `/mision` y `execute_code`) **alcanzaba `postgres:5432` y `valkey:6379`** y **salía a
internet**.

**Qué tan grave era (calibrado, sin exagerar):** la BD **rechaza toda conexión sin el password
real** (aleatorio, en `.env`, no adivinable — lo probé con 4 credenciales comunes, todas
`InvalidPasswordError`). Así que **NO había robo directo de datos de clientes** → no era
crítico-legal. PERO era **defensa-en-profundidad ausente**: código no confiable no debe siquiera
VER el puerto de la BD, y la salida a internet permite exfiltrar lo que ese código produzca. Para
un producto que promete "aislamiento total", esa promesa quedaba debilitada.

**La cerradura (aplicada + verificada en vivo):** segmenté la red en el compose de instancia.
- `default`: postgres/valkey/agent/worker/mcp/render/admin (como antes).
- `sandbox_net`: **solo agent ↔ sandbox**. El sandbox salió de `default`.
- **Resultado verificado:** el sandbox ahora da `gaierror` (ni resuelve el DNS) para
  postgres/valkey/mcp → **no los ve**. Conserva internet a propósito (pip/npm de execute_code lo
  necesitan). Y el agent le sigue hablando: `execute_code` real devolvió `5050` tras el cambio.
- Batería §5-BIS completa tras la cerradura: pytest 244, /salud 0 FAIL, memoria+reconexión,
  pentest de aislamiento de nuevo SÓLIDO.

## 4 · Matices honestos para el contrato / conversación con clientes (NO agujeros)

Ninguno es explotable hoy; son cosas que un cliente enterprise o su abogado preguntará, y conviene
tenerlas claras (redactar bien > prometer de más):

1. **Master key en disco (cifrado v1).** La KEK maestra vive en `~/.for3s/master.key` (permisos
   0600) en el server, no en un HSM/KMS. Si alguien roba el disco del server Y la BD, descifra los
   secrets. Mitigación de diseño ya prevista (Grafo R4): master key offline / KMS en v2. **Para
   vender hoy:** el server es tuyo y self-hosted → el modelo de amenaza es "acceso físico/root al
   server", no "cliente remoto". Decláralo así.
2. **Residencia de datos.** Todo vive en TU server (self-hosted) — bueno para "tus datos no salen",
   pero si un cliente exige residencia en su propia región/nube, hoy no hay multi-región. Es una
   feature de venta, no un fallo.
3. **Sin cifrado en reposo a nivel disco de la BD.** Los secrets están cifrados (AES-GCM), pero el
   resto de la BD (memoria de conversaciones) está en Postgres sin TDE. Mitigación: cifrar el
   volumen del server (LUKS) es una decisión de infra, no de código.
4. **Borrado = soft-delete.** `/olvidar` marca `deleted_at`; el purgado físico lo hace el ciclo
   nocturno. Para un "derecho al olvido" contractual (GDPR art. 17), conviene documentar la ventana
   de purga definitiva.

## 5 · Cómo responderle a un cliente que pregunta "¿es seguro?"

> "For3s es self-hosted: tus datos viven en TU servidor, no en el nuestro. Cada cliente está aislado
> por construcción con doble candado (probado con pruebas de penetración: un cliente no puede ver los
> datos de otro). Los secretos se cifran con AES-256-GCM. Toda acción queda en una bitácora inmutable
> que ni el administrador puede alterar. El código que el agente ejecuta corre en un sandbox aislado
> sin acceso a la base de datos. La bitácora nunca guarda el contenido de tus conversaciones."

Todo lo de esa frase está **demostrado**, no es marketing.

---

**Fecha:** 2026-07-15 · **Alcance:** instancia `general` en el server `for3s` (v0.17.0). Aplica a
todas las instancias (mismo código/compose). **Pruebas:** pentest_aislamiento · probe_sandbox ·
probe_db · DELETE audit · batería §5-BIS. Ronda: `work/Ronda_FrenteE_Confianza_Para_Delegar.md` §F3.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `docs/analysis/Auditoria_Seguridad_For3s_OS.md`).
