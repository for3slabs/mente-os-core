# BLOCK · separacion-motor-instancia

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-separacion-motor-instancia-2026-08
type: infra
intent: que un clon de este repo verifique el MOTOR sin exigir la INSTANCIA de Brian
status: active · lane: task · owner: brian
created: 2026-08-07 · updated: 2026-08-07

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
<!-- ⭐ The only field the AI does not fill: the boundary is a decision, not a
     derivation (block-lifecycle.md §1). An empty OUT is a block with no boundary. -->
## ✅ IN
- `bin/test-f0-f6` · `bin/check-structure` · `bin/init` — los checks que hoy exigen instancia
- la clave `additionalDirectories` de los settings — SOLO esa clave; las rutas de los hooks
  las cerró `blocks/archive/distribucion_2026-08` §F1
- `mente.config.yml` + su plantilla — donde se declara qué es de la instancia
- `docs/WORKSPACE.md` — documento de instancia que viajaba con el motor

## ⛔ OUT
- **BRIAN (2026-08-07): NO se parte la historia de git.** Opción C, no A ni B: un solo repo,
  reversible. Publicar el motor en limpio es otro bloque, después de éste.
- **NO se toca `Cerebro/`** — es el producto For3s OS, no la instancia de Mente OS.
- **NO se borra nada de la instancia.** Se mueve; una decisión de no hacer algo es información.

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: `rules/rule-checks-must-measure.md` §D — la familia que este bloque aplica
- DEPENDED ON BY: `blocks/active/demo` — sus §F import counts son 1 de los 7 rojos del clon
- ISOLATED FROM: `Maestro/` (sub-repo con su propio git) · `marca-personal/`
- PIECE: bin/init → 0 dependents (measured 2026-08-07)

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
<!-- These get injected before editing (architecture §12-QUATER). Every path must exist. -->
## Required standards
- rules/rule-fix-not-patch.md
- rules/rule-checks-must-measure.md
- rules/rule-shipping-flow.md
- principles/expertise/val-functional.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: 4/5 sub-bloques cerrados · clon limpio 10 → 1 fallo
next: el único rojo que queda es la respuesta CORRECTA (sesión sin registrar) — se documenta
blockers: none
progress: 4/5 sub-blocks closed
updated: 2026-08-07

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | `init` poda los `additionalDirectories` muertos y lo dice | bin/init | 0 | ✅ |
| 2 | `WORKSPACE.md` se GENERA de plantilla, no se hereda | bin/init | 0 | ✅ |
| 3 | los checks de instancia se SALTAN lo ausente en 🟡, no fallan | bin/test-f0-f6 | 0 | ✅ |
| 4 | un hermano ausente no es una cita rota (12 → 0 en el clon) | bin/check-links | 0 | ✅ |
| 5 | clon limpio verificado end-to-end | — | — | ⬜ |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- **Opción C, no A ni B** (Brian, 2026-08-07). Razón: el trabajo real no es mover archivos, es
  que los checks dejen de exigir instancia ajena — eso sirve para las tres opciones. Partir la
  historia se paga una vez y no se deshace. El tradeoff aceptado: el repo público seguirá
  conteniendo la instancia hasta que se decida A.
- **Un check ausente NO es un check fallido.** Si la instancia no está, el check se salta y lo
  DICE; nunca se da por bueno en silencio, porque eso convierte un hueco en un falso verde.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- La etiqueta *"son 8 fallos y son de la instancia de Brian"* estaba TAPANDO 3 defectos reales
  del motor (familia D casos 5 y 6, + un `owner == "Maestro"` hardcodeado en check-structure).
  ⭐ Una explicación cómoda para un rojo es cómo un bug sobrevive a una auditoría.
- 🔴 **`pre-edit-standards.py` confunde MENCIONAR una ruta con RECLAMARLA.** Su matcher hace
  `d in target` (subcadena): este bloque nombró `marca-personal/` sólo para decir de quién NO
  era, y el hook le atribuyó los archivos de `demo`. Un §B que explica un límite reclama
  territorio. Medido 2026-08-07; se esquivó reescribiendo el §B, **el matcher sigue igual**.
  ⚠️ Con dos bloques activos el más "hablador" se roba los archivos del otro. Pendiente para
  Brian: arreglarlo pide decidir si §B pasa a ser una lista de rutas parseable.

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-07 · clon limpio: 10 → 7 (familia D 5-6) → 6 (`additionalDirectories`) → 2
  (`WORKSPACE.md` generado) → **1** (hermano ausente ≠ cita rota). Tras `bin/init`.
- 2026-08-07 · ⭐ **no hizo falta crear `instance/`.** La hipótesis de partida era mover 221
  archivos; medido, **ninguno estorbaba**. Lo que fallaba eran los CHECKS que los interrogaban
  mal. Mover archivos habría escondido el defecto en vez de corregirlo.

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context

**El problema medido.** Un clon de este repo termina la batería en rojo. La causa no es un fallo:
es que **1 de cada 3 archivos es motor y 2 de cada 3 son la instancia de Brian** (118 vs 221
medidos el 2026-08-07), y los checks verifican esa instancia contra un árbol que no la tiene.

**La línea ya estaba decidida, no escrita.** `mente.config.yml` la declara desde el 31-jul:
*el motor es `bin/ hooks/ rules/ principles/` y nadie lo edita; la instancia es tuya y se declara
una vez*. Este bloque la lleva del documento al árbol.

**Los 7 rojos que quedan, por clase:**

| Rojo | Clase | Lo cierra |
|---|---|---|
| `additionalDirectories` | instancia dentro de un archivo del MOTOR | sub-bloque 1 |
| `WORKSPACE.md names` (4) · `§F import counts` (7) · `grade-block archived` | instancia pura | sub-bloques 2-3 |
| `broken citations ≤ techo` (12) | citas a `Maestro/` + memorias del harness | sub-bloque 4 |
| `exit code del veredicto` | sabotaje que depende de un bloque de Brian | sub-bloque 3 |
| `check-clear-ready registered=no` | ⭐ **es la respuesta CORRECTA** | ninguno — se documenta |

⚠️ Ese último no se arregla: en un clon nuevo la sesión **no** está registrada, y decirlo es el
comportamiento bueno. Un check que se pusiera verde ahí estaría mintiendo.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — the block is still active)
