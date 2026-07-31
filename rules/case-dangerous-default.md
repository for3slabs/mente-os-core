# CASE · THE DANGEROUS DEFAULT
**Status:** current · **Type:** case · **Updated:** 2026-07-29 · **Owner:** brian
**Migrated** 2026-07-29 from `memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` (4 files referenced this
path and it did not exist). **Content in Spanish — it is the original record.**
---

## Purpose

A reusable case: when another inherited or hardcoded value needs cleaning up, this is the method
that worked and the mistakes not to repeat. **Injected before choosing any default** — declared in
§D of the relevant block.

---

# 🎓 CASO DE ESTUDIO — "El default peligroso": cómo se limpió el tema `hoteles`

> **Para qué sirve este documento:** es un CASO REUTILIZABLE. Cuando aparezca otro valor
> heredado/hardcodeado que haya que limpiar (un default, una etiqueta, una constante de una fase
> vieja), este es el método que funcionó y los errores que NO hay que repetir.
> **Fecha:** 2026-07-26 · **Origen:** pulido de la demo (`marca-personal`) + agente (`For3s-OS/.../api_channel.py`).

---

## 1 · EL SÍNTOMA
El hilo de las conversaciones de la demo se llamaba `api:<client-id>:hoteles` — en TODAS las
instancias, incluida la personal de Brian. Brian lo vio al rastrear un mensaje suyo en la BD del
agente y preguntó: *"no sé de dónde viene este hoteleria, no entiendo"*.

## 2 · EL ORIGEN (rastrearlo ANTES de tocar)
Una sola línea en `For3s-OS/.../api_channel.py` del agente:
```python
TEMA_DEFAULT = "hoteles"  # el hilo/tema por defecto de esta fase (Incubathon)
```
El propio comentario lo decía: **"esta fase (Incubathon)"**. Cuando se construyó el canal API, el
único cliente era **NavigoX** (hotelería, el 2º lugar del Incubathon). El default se puso para esa
fase y **nunca se limpió** al pasar a fase MERCADO.

**Lección 1 — el código suele decir de dónde viene.** Antes de teorizar, `grep` + leer el comentario
+ contrastar con Mente OS (memoria `project_hito_hoteleria_navigox` y RETOMAR). En 3 comandos se
supo el origen exacto y que era inofensivo-pero-obsoleto, no un bug.

## 3 · 🔴 EL ERROR QUE CASI COMETO (lo importante de este caso)
Primer fix propuesto: cambiar el default de `"hoteles"` a **`"general"`** (parecía neutro y encajaba
con la visión "el dueño usa su hilo general").

**Brian lo cazó:** *"general únicamente es para los dueños, no puede acceder otra persona… si un
cliente no manda un tema lo vas a pasar a general y eso está mal"*.

Tenía razón, y era grave: **`general` es un nombre RESERVADO** (el hilo base del dueño, su memoria
de siempre). Como default habría significado:
```
Cliente API / invitado que NO manda tema  →  cae en el hilo PRIVADO del dueño  🔴
```
Habría cambiado una etiqueta inofensiva por un **problema de aislamiento**.

**⭐ LECCIÓN 2 — LA REGLA QUE SALE DE ESTE CASO:**
> **Un valor por defecto NUNCA debe apuntar a algo que tenga dueño o significado reservado.**
> El default es "lo que pasa cuando nadie decidió": tiene que ser un **cajón neutro que no sea de
> nadie**. Si el default cae en un espacio con dueño, cualquiera que no configure nada aterriza en
> propiedad ajena.
> Antes de elegir un default, preguntar: *¿este nombre significa algo para alguien?* Si sí → otro.

## 4 · LA SOLUCIÓN (en el ORDEN que no rompe)
Se resolvió en 2 capas, y el orden fue lo que evitó romper producción:

**Capa 1 — el que SABE, decide (sitio):**
El sitio manda el `tema` EXPLÍCITO en cada llamada, leído de la BD (`demo_users.hilo_nombre`) con el
nuevo helper `hiloDe(email)`:
- dueño → `general` (su memoria de siempre)
- invitado → `hilo-<nombre>-<sufijo>` (aislado)

**Capa 2 — el que RECIBE, deja de adivinar (agente):**
Default `hoteles` → **`sin-tema`** (cajón neutro) + `FOR3S_API_TEMA_REQUERIDO` para exigirlo.

**⭐ LECCIÓN 3 — orden de despliegue:** primero enseñar a los emisores a mandar el dato, DESPUÉS
endurecer al receptor. Al revés se rompe todo lo que aún no lo manda. Y como efecto secundario
valioso: **el fix quedó funcionando sin necesidad de rebuild del agente**, porque el emisor ya no
deja que el receptor use su default.

## 5 · LA DECISIÓN DE NO SER ESTRICTO (y por qué)
La regla original de Brian era *"si no manda tema, error"*. Se implementó
(`FOR3S_API_TEMA_REQUERIDO=1`) pero quedó **APAGADA**. Razón:
> Un cliente de la API **no debe estar obligado** a saber de "temas" para mandar un mensaje simple.
> Es justo el caso de las keys f3k_ ("usa tu For3s desde tu propio código"): el body lo arma el
> usuario. La rigidez tenía sentido **mientras el default era peligroso**; con un default neutro
> deja de hacer falta.

**⭐ LECCIÓN 4 — arreglar la causa, no poner un candado.** Si el default es seguro, obligar al
cliente es fricción sin ganancia. Endurecer se justifica cuando NO puedes hacer seguro el default.

## 6 · VERIFICAR EL IMPACTO ANTES DE AFIRMARLO
Primero se dijo "activarlo rompería a cualquier cliente API". Brian preguntó *"¿por qué rompería?"*
y al verificarlo la afirmación resultó **excesivamente cauta**. La comprobación real
(`api_clients` en la BD del agente + quién consume `/v1/chat`):

| Cliente | ¿Rompería? | Por qué |
|---|---|---|
| Demo web | ❌ | ya manda tema |
| Telegram | ❌ | **no consume** el canal API (solo lo arranca) |
| NavigoX | ❌ | otra instancia, sin consumo activo |
| **Keys f3k_** | ✅ | el usuario arma su propio body |

**⭐ LECCIÓN 5 — "rompería X" es una afirmación que se COMPRUEBA, no se supone.** Cuando Brian
pregunta "¿por qué?", casi siempre hay un matiz que la medición corrige.

## 7 · CHECKLIST REUTILIZABLE (para el próximo valor heredado)
1. **Rastrear el origen** — grep + comentario del código + Mente OS. ¿De qué fase venía?
2. **¿El valor nuevo pisa algo reservado?** Si el nombre significa algo para alguien → elegir otro.
3. **¿Quién SABE el valor correcto?** Que lo mande explícito quien lo sabe (normalmente la BD).
4. **Orden:** emisores primero, receptor estricto después (nunca al revés).
5. **Medir el impacto real** antes de decir "esto rompería X" (consultar clientes reales).
6. **¿Hace falta endurecer?** Solo si el default no puede ser seguro.
7. **Probar contra lo real** (aquí: el agente brian) y **documentar el porqué en el propio código**,
   para que nadie lo "corrija" después sin el contexto.

## 8 · DÓNDE QUEDÓ
- Sitio: `marca-personal/lib/demo/for3sChat.ts` (`enviarMensaje` manda `tema`) +
  `lib/demo/userStore.ts` (`hiloDe`) + `lib/demo/hilos.ts` (estándar del nombre).
- Agente: `For3s-OS/.../api_channel.py` (`TEMA_DEFAULT="sin-tema"`, `TEMA_REQUERIDO` apagado). Aplicado en
  `~/for3s-os` del server (respaldo `.bak-tema`), **pendiente de rebuild de imagen** — no urgente,
  porque el sitio ya manda el tema.
- Memoria: [[project_pendientes_demo_hilos_keys]].

---

Related: `rules/rule-fix-not-patch.md` · `rules/qa-dimensions.md` §2.2 ·
`principles/owner-0-voice.md` §2.7 (source of *"a claim is VERIFIED, not assumed"*) ·
`principles/expertise/database.md` · ADR-017.
