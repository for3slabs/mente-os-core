# BLOCK · seguridad

<!-- ══ A · IDENTITY ══ required to OPEN · ≤6 lines ══ -->
id: blk-seguridad-2026-08
type: code
intent: que el dato de For3s OS sea de su dueño — auditar la capa de seguridad contra el gate de la Fase 1
campaign_phase: 1
status: active · lane: full-block · owner: brian
created: 2026-08-14 · updated: 2026-08-14

<!-- ══ B · SCOPE ══ required to OPEN · ≤20 lines ══ -->
## ✅ IN
- `packages/for3s-core/src/for3s_core/crypto.py` (69) — las 4 funciones; `encrypt`/`decrypt` bien hechas (B-14)
- `packages/for3s-core/src/for3s_core/secret_store.py` (96) — ⭐ el ÚNICO `encrypt(` de producción, en su línea 40 (B-01)
- `packages/for3s-core/src/for3s_core/audit.py` (104) — la cadena `hash_self`/`hash_prev` de 12,953 eventos
- `packages/for3s-core/src/for3s_core/sandbox.py` (105) · `packages/for3s-core/src/for3s_core/execute.py` (96) — el aislamiento de `execute_code`
- tablas `secrets` · `audit_log` · **columna `content` de `episodes_events`** — el 🔴 H-01

## ⛔ OUT
- ⛔ **NO se cifra nada aquí.** La Fase 1 MIDE; cifrar es migrar en producción → OK de Brian
- ⛔ el cifrado de la memoria semántica (embeddings, 133 MB): del bloque `memoria`
- ⛔ Auth/RBAC y Output Gate — Fase 4-5, se anotan **FUTURO** (`rules/rule-product-authority.md` §2.4)
- ⛔ las instancias `for3s` y `general` — solo se toca `brian`

## 🌐 System-wide rules that also apply (inherited, not owned here)
- `CLAUDE.md`: migración de BD y reinicio de instancia exigen OK explícito de Brian
- `base-rules.md` #7: server-first · ADR-003: el criterio es de Brian, nunca se inventa
- ⛔ un secreto que aparezca en salida de herramienta se **ROTA**, nunca se escribe en un documento

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- CAMPAIGN: `campaigns/producto-for3s-os/CAMPAIGN.md` — bloque **1 de 12**, abre por gravedad
- DEPENDS ON: nada. Abre primero por GRAVEDAD (⚠️ no por ritmo: SB-3 midió que no crece, §G)
- DEPENDED ON BY: `memoria` (comparte la tabla `episodes_events`, distinta columna) ·
  `datos` (dueño del esquema) · `entrenamiento` (metió 33,737 turnos por esa misma columna)
- ISOLATED FROM: los 8 bloques sin 🔴 — `rules/rule-isolation.md` §1
- 🔴 CRITICAL PIECES: `crypto.py` — si se toca mal, los secretos ya cifrados dejan de descifrarse

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤12 lines ══ -->
## Required standards
- rules/rule-shipping-flow.md
- rules/rule-product-authority.md
- rules/qa-dimensions.md
- rules/rule-fix-not-patch.md
- rules/rule-isolation.md
- principles/owner-3-validation.md
- principles/expertise/val-functional.md
- principles/expertise/val-integration.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: **Fase 1 · NODOS** — ¿existe cada pieza que el Grafo declara, y hace lo que dice?
blockers: ninguno. ✅ El acceso al servidor quedó resuelto el 14-ago — la guía de `secrets/`
          da el método que funciona (password + `StrictHostKeyChecking=accept-new`), no era
          un problema del servidor sino del método que yo intentaba
progress: **6/6 la MEDICIÓN** (5 de 6 dimensiones 🟢) · **0/4 el ARREGLO** (SB-7..10, §F)
next: **SB-7** — la capa única `contenido.py`. ⭐ Brian decidió A el 14-ago: dispersar el
      descifrado en 9 sitios repetiría el defecto que este bloque diagnosticó (⚠️ y que reapareció
      por 3ª vez el 18-ago en el BYOK — §H)
updated: 2026-08-18

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | pieza | imports | status |
|---|---|---|---|---|
| 1 | confirmar las 5 rutas del §B contra el servidor (`find`) | todas | 0 | ✅ done |
| 2 | ¿existe cada pieza del Pilar 1 y hace lo que declara? | crypto · secret_store | 0 | ✅ done |
| 3 | medir H-01: cuántos MB en claro HOY y a qué ritmo crecen | episodes_events | 0 | ✅ done |
| 4 | verificar la cadena de auditoría íntegra (hash_self/hash_prev) | audit | 0 | ✅ done |
| 5 | ¿el sandbox de `execute_code` aísla de verdad? | sandbox · execute | 0 | ✅ done |
| 6 | escribir el hallazgo de fase 1 (ver §J) con veredicto por nodo | — | 0 | ✅ done |
| 7 | 🔴 **H-01a** capa única `contenido.py` — cifra al escribir, descifra al leer | crypto · memory | 0 | todo |
| 8 | 🔴 **H-01b** los **2 escritores** pasan por la capa | memory · entrenamiento | 0 | todo |
| 9 | 🔴 **H-01c** los **9 lectores** pasan por la capa | 9 archivos (§J) | 0 | todo |
| 10 | 🔴 **H-01d** migrar los 15 MB — ⚠️ rollback probado, 33,908 filas | episodes_events | 0 | todo |
| 11 | 🟠 **H-19** los embeddings (133 MB) quedan en claro — decisión de arquitectura | consolidator | 0 | todo |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- ⚠️ 2026-08-14 · **Abrió por "severidad × velocidad" y SB-3 tumbó la mitad "velocidad".** El
  criterio sirve para los otros 11; aquí abre **por gravedad sola**.
- ⭐ 2026-08-14 · **La Fase 1 NO cifra nada** (`docs/plans/PLAN-3-fases.md`: la 1 mide).
  ⛔ **Arreglar durante la medición contamina la medición.**
- ⭐ 2026-08-14 · **El §B IN se declaró con rutas DERIVADAS y se dijo** (§H + SB-1), no como medición.
- 🔴 2026-08-14 · **SB-1 cazó un §B MAL ESCRITO** (las 5 rutas con el prefijo equivocado): el
  hook no habría reconocido ni un archivo y el editor habría trabajado sin estándares, **en
  silencio**. ⭐ **Un §B derivado no falla ruidosamente: falla callando.** Detalle: hallazgo §5.
- ✅ 2026-08-14 · **H-01 RE-CONFIRMADO en vivo:** `encrypt(` en **un solo sitio** de producción
  (`secret_store.py:40`). ⭐ Ya no es "cero cifrado": es **dónde hay que conectarlo** (§J).
- ⭐⭐ 2026-08-14 · **H-01 se arregla con UNA CAPA ÚNICA — decisión de Brian.** El alcance real
  medido: **2 escritores** (`memory.py:93` · `entrenamiento.py:73`) y **9 lectores**, cada uno con
  su propio SQL, **sin capa central**. ⚠️ Cifrar solo los 2 INSERT rompe a los 9 — y no
  ruidosamente: fallaría la próxima vez que el agente intente recordar.
  ⛔ **Descartada la opción rápida** (cada lector descifre): este bloque diagnosticó que el
  defecto es *"se construye la pieza y no se conecta"* — ⭐ **dispersarlo en 9 sitios sería
  cometer ese error mientras se arregla su síntoma.**
  ✅ **Rollback PROBADO:** dump de 131 MB restaurado → **33,908 filas** (BD desechable, eliminada).
- ⚠️ 2026-08-14 · **CORRIJO UN NÚMERO MÍO: decía "10+ escritores" y son 2.** Conté los que
  MENCIONAN la tabla. ⭐ El trabajo real está en los **9 lectores**. Corregido en el hallazgo.
- ✅ 2026-08-14 · **SB-6: FASE 1 CERRADA** → `campaigns/producto-for3s-os/hallazgos/seguridad-fase-1.md`.
  **5 de 6 dimensiones 🟢**; la 6ª es 🔴 H-01. ⭐ **Bien CONSTRUIDA y mal CABLEADA.**
- ✅ 2026-08-14 · **SB-5: el sandbox AÍSLA — probado ATACÁNDOLO.** 5 ataques, 5 contenidos
  (hallazgo §3.5); el timeout corta a los **5.0 s exactos**.
- ⚠️ 2026-08-14 · **El sandbox alcanza internet — A PROPÓSITO** (el compose lo declara: pip/npm).
  ⛔ Diseño declarado que se cumple ⇒ no es deuda. ⚠️ Egreso abierto: el código del LLM podría
  exfiltrar lo que tenga a mano; hoy no tiene nada.
- ✅ 2026-08-14 · **SB-4: la cadena es ÍNTEGRA — EJECUTADA, no contada.** `verify_chain()`:
  **`True`, 12,963 eslabones** · ⭐ **y por SABOTAJE** (sin tocar la BD): alterar `detail` rompe el
  hash → detectado. **Un `True` que nunca se vio fallar no es evidencia.**
- 🟠 2026-08-14 · **La auditoría cubre lo AUTOMÁTICO:** 89% microglía, **110 del usuario**.
  ⭐ Cruzado con SB-3: no ignora al humano — **el humano lleva 16 días sin escribir.** Y es lo
  único VIVO del bloque (último evento **hoy**): registra un sistema que solo se habla a sí mismo.
- 🔴🔴 2026-08-14 · **SB-3 DERRIBA LA PREMISA CON LA QUE ABRÍ ESTE BLOQUE. H-01 NO EMPEORA
  SOLO.** Yo afirmé tres veces —y lo escribí en §C, en §G y en la campaña— que `seguridad` abría
  primero porque *"cada mensaje nuevo se suma a los 15 MB en claro"*. **Medido hoy: es falso.**
  · de los 15 MB, **33,737 filas (99.5%) son IMPORTADAS** del entrenamiento, con fechas
    ene-may 2026 — un lote histórico que **ya no crece**.
  · lo **VIVO** son **171 filas = 81 kB**, el **0.5%**.
  · **crecimiento en los últimos 60 días: 81 kB.** Último mensaje real: **2026-07-30, hace 16
    días.** Junio y agosto: **cero filas**.
  ⭐ **El criterio "severidad × velocidad" era correcto; el dato que le metí no.** Velocidad real
  ~0 → H-01 **no gana por urgencia, gana por GRAVEDAD**: 15 MB legibles siguen expuestos hoy.
  ⚠️ **De dónde salió:** lo deduje de que la BD tenía 15 MB y el bot corría en producción —
  **nunca medí la fecha de las filas.** `base-rules.md`: afirmar sin medir, y decidir encima.
- 🔴 2026-08-14 · **El código PROMETE por escrito lo que no cumple:** el docstring de `crypto.py`
  declara *"los secretos NUNCA viven en texto plano en BD"* y *"decrypt minimum"*. Se cumple para
  los 38 secretos, **no para los 15 MB**. ⭐ Descarta el *"nunca se pretendió cifrar"*.
- 🔬 2026-08-14 · **La criptografía NO es el problema, el CABLEADO sí.** `crypto.py` está bien
  hecho; el contenido **nunca pasa por ahí** (solo `secret_store` y `automod`). ⭐ **Hueco de
  integración, no de implementación** — no se reescribe la cripto, se conecta.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- ⚠️ 2026-08-18 (S15) · **El bloque NO avanzó: la jornada fue del MOTOR.** Sigue en 6/11 y SB-7
  sin empezar. Lo que sí cambia para su ejecución: **la base de un PR es `master`, siempre**
  (`rules/rule-pr-base.md` + `bin/check-pr-base`) — los PRs de SB-7..SB-10 **no se encadenan**
  entre sí aunque dependan en orden; se espera el merge y se rebasa. ⭐ Nació de perder 329 líneas
  ese día por encadenar dos PRs en un repo que squashea.
- 🔴 2026-08-18 · **EL PATRÓN POR 3ª VEZ, y ahora bloquea una VENTA.** Brian preguntó si un cliente
  puede conectar su propio LLM (BYOK). Medido: `llm.py` **ya define `LLMProvider(ABC)`** y el
  `secrets/README.md` **ya preveía** *"las API keys de clientes van en el Key Vault cifrado"* —
  pero **12 archivos instancian `ClaudeProvider(` directo**, puenteando la abstracción.
  ⭐ Mismo defecto que H-01 y que el workspace único: **la pieza existe y nadie pasa por ella.**
  Tres apariciones no son un cable suelto: es **cómo se ha venido trabajando** — la campaña
  debería atacarlo de raíz, no caso por caso.
  📌 Dueño: el bloque `agente` (nº 5). ⛔ No se abre aquí — otro scope (`rule-isolation`).
- ✅ 2026-08-14 · **RESUELTO — el acceso al servidor no estaba roto, mi método sí.** Declaré un
  bloqueador de los 12 **sin leer `secrets/Conectar_Servidor_For3s.md`**, que documenta el método
  que funciona y lista ese error exacto con su solución. El §F de CAMPAIGN.md ya lo señalaba en
  *"Cómo entrar"*. ⭐ Coste: una decisión pedida a Brian que no hacía falta pedirle.

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-14 · ✅ **SB-2 — las 5 piezas EXISTEN y CUMPLEN**, medidas una a una en el servidor:
  `crypto.py` (AES-256-GCM, nonce 12 B, HKDF por workspace) · master key `~/.for3s/master.key`
  **32 B / `600` / fuera del repo** · `audit.py` con `verify_chain()` · `sandbox.py`
  `--network none` + timeout · `execute.py` a URL fija. 38 secretos cifrados · 1 workspace.
  ⭐ **La capa está bien construida: lo que falla no es ninguna de las 5.**
- 2026-08-14 · ✅ **SB-1 cerrado con medición propia en el servidor.** Las 5 piezas existen y
  suman **470 líneas** — coincide exacto con la auditoría del 12-ago. `crypto.py` exporta las 4
  funciones declaradas (`load_or_create_master_key` · `derive_workspace_key` · `encrypt` ·
  `decrypt`). Sus únicos consumidores siguen siendo `secret_store.py` y `automod.py`.
- 2026-08-14 · Bloque abierto. Terreno heredado de la auditoría del 12-ago (35 pasadas sobre el
  servidor): 1 hallazgo 🔴 (H-01), 3 fortalezas medidas (B-01 secretos cifrados · B-14 cripto bien
  implementada · cadena de auditoría íntegra en 12,953 eventos).

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context

**El hueco, en una frase: la criptografía de For3s OS funciona y el contenido nunca pasa por ella.**

### La autoridad, y por qué esto es un hallazgo y no una preferencia

`Cerebro/For3s_OS_Grafo_Maestro.md:112` — **Pilar 1, LOCKED**: *"End-to-end encryption es
requirement v1"* · ⭐ *"No es una capa encima del grafo. **Es propiedad de cada conexión.**"*
⭐ **Por eso pasa el filtro de la vara temporal** (`rules/rule-product-authority.md` §2): no es
una exigencia de Fase 4-5 traída antes de tiempo — **el propio Grafo la declara requirement v1.**

### El estado (todo lo medido vive en §G · aquí solo lo que un arranque en frío necesita)

**Lo roto es UNO:** 🔴 15 MB de conversaciones en claro, con `encrypt(` presente en **un solo
sitio** de producción y 10+ archivos escribiendo sin cifrar. Uno de esos mensajes legibles dice
literalmente *"Sigue diciendo que es privado"*.

⭐ **Lo demás está BIEN, y decirlo importa:** secretos cifrados, `crypto.py` correcto, cadena de
auditoría íntegra (12,963 verificados + sabotaje) y sandbox que aísla de verdad. Un bloque que
solo reporta lo roto enseña a desconfiar del veredicto entero (`rules/qa-dimensions.md`).

### El mismo patrón, en dos sitios

Un solo `workspace_id` **aunque el código soporta varios** (`derive_workspace_key` funciona).
Capacidad construida y no cableada — **igual que H-01**. ⚠️ Repetido dos veces deja de ser *"un
cable suelto"* y pasa a ser **una forma de trabajar**: se construye la pieza y no se conecta.

### Lo que este bloque NO va a encontrar, y no es deuda

Auth/RBAC, el Output Gate y Prometheus son **Fase 4-5** del `Plan_Maestro_Programacion.md`. Se
registran como **FUTURO**. ⭐ **La razón está medida:** auditar contra el Grafo completo dio 24
hallazgos y 15/15 tablas ausentes sobre un sistema que corre a diario; contra el gate de la fase
en curso dio 6/6 y 4 hallazgos accionables. **Los otros 20 no eran falsos: eran prematuros — y un
hallazgo prematuro se ve idéntico a uno urgente, así que entierra a los que sí importan.**

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — el bloque acaba de abrirse; cierra al pasar las 3 fases)