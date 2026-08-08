# BLOCK · separacion-motor-instancia

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-separacion-motor-instancia-2026-08
type: infra
intent: que un clon de este repo verifique el MOTOR sin exigir la INSTANCIA de Brian
status: closed · lane: task · owner: brian
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
phase: **CERRADO 2026-08-07** · 🟡 cierra (capa 2 6/6 🟢 · capa 1 🔴 por límite del medidor, §K)
next: ninguno aquí. La separación real (motor publicable, opción A) es OTRO bloque
blockers: none
progress: 5/5 sub-blocks closed · verificado end-to-end en un clon de master mergeado
updated: 2026-08-07

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | `init` poda los `additionalDirectories` muertos y lo dice | bin/init | 0 | closed |
| 2 | `WORKSPACE.md` se GENERA de plantilla, no se hereda | bin/init | 0 | closed |
| 3 | los checks de instancia se SALTAN lo ausente en 🟡, no fallan | bin/test-f0-f6 | 0 | closed |
| 4 | un hermano ausente no es una cita rota (12 → 0 en el clon) | bin/check-links | 0 | closed |
| 5 | clon limpio verificado end-to-end **desde master mergeado** | — | — | closed |

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
- ✅ **`pre-edit-standards.py` confundía MENCIONAR una ruta con RECLAMARLA** — RESUELTO el
  mismo día (Brian: *"arréglalo"*). Su matcher hacía `d in target` sobre cualquier ruta de la
  línea: este bloque nombró `marca-personal/` sólo para decir de quién NO era y el hook le
  atribuyó los archivos de `demo`. ⚠️ El daño no era ruido de más — con dos bloques activos el
  más "hablador" se roba los del otro, y el aviso CORRECTO deja de llegar.
  **No hizo falta cambiar el formato del §B**, que era el coste que se temía.

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-07 · clon limpio: 10 → 7 (familia D 5-6) → 6 (`additionalDirectories`) → 2
  (`WORKSPACE.md` generado) → **1** (hermano ausente ≠ cita rota). Tras `bin/init`.
- 2026-08-07 · ✅ **CIERRE MEDIDO desde master mergeado**: clon en frío **6 fallos**, tras
  `bin/init` **1** — y ese 1 es `check-clear-ready registered=no`, la respuesta correcta en un
  árbol recién nacido. `check-links` 300 limpio · `check-blocks` 0 errores. `bin/init` reporta
  `WORKSPACE.md: written` y `1 additionalDirectories muertos podados`: las dos piezas de este
  bloque funcionando en una máquina que no es la de su autor.
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

### Runbook y rollback
→ `blocks/archive/separacion-motor-instancia_2026-08/docs/runbook-y-rollback.md` — cómo se verifica esto
en un clon (3 pasos) y cómo se revierte cada uno de los 4 cambios por separado.

⚠️ **`bin/grade-block` los sigue marcando 🔴 NO, y el documento SÍ existe.** Medido 2026-08-07:
`infra_evidence()` busca esos textos recorriendo los DIRECTORIOS que el §B declara como scope —
y el §B de este bloque declara **archivos sueltos** (`bin/init`, `bin/test-f0-f6`), no carpetas,
así que el texto que analiza llega VACÍO y ambas métricas salen NO pase lo que pase.
⭐ **No se toca el §B para complacer al medidor**: el scope describe lo que el bloque toca, y
falsearlo para sacar un 🟢 convertiría el veredicto en un número decorativo. El 🔴 se deja como
lo que es —un límite del validador, no una carencia del bloque— y queda en `memory/PENDIENTES.md`.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing

**Cerrado 2026-08-07.** Los tres criterios de `owner-3-validation.md` §2, medidos:

| Criterio | Resultado |
|---|---|
| **Funcional** | 🟢 `bin/test-f0-f6` **199 passed · 0 failed** · `bin/check-blocks` 0 errores |
| **Suficiencia** | 🟢 `bin/check-sufficiency` — *SUFFICIENT: A-E answer all seven restart questions* |
| **Veredicto de calidad** | 🟢 capa 1 **🟢 PRODUCT** (tras corregir el medidor) · capa 2 🟢 6/6 |

<!-- ⚠️ Esta tabla NO se numera a propósito: `bin/generate-index` captura como sub-bloque
     cualquier fila que empiece por un dígito con 5 columnas, y contaba este §K como uno más. -->



### Capa 1 — `bin/grade-block separacion-motor-instancia`

`secret values written down 0 🟢` · `runbook documented yes 🟢` · `rollback documented yes 🟢` ·
las 3 métricas de código `n/a ⬜` (no hay código en scope). **LAYER 1 VERDICT: 🟢 PRODUCT.**

🔬 **Al cerrar, estas dos salían 🔴 — y el medidor era el que leía mal.** Verificado antes de
tocarlo: el runbook de este bloque existía (43 líneas, §Runbook en la 10, §Rollback en la 25).
`infra_evidence()` tenía **dos puntos ciegos**: solo leía entradas `isdir` (este §B declara
**archivos sueltos** — `bin/init`, `bin/test-f0-f6` — así que el texto llegaba vacío y ambas
métricas salían NO pasara lo que pasara) y **nunca leía `blocks/<bloque>/docs/`**, que es donde
`contract-block.md` dice que vive la documentación del bloque.

⛔ **No se ensanchó el §B para complacer al medidor** — falsear el scope convierte el veredicto en
un número decorativo. **Se corrigió el medidor** (`bin/grade-block`, 2026-08-07) y se verificó por
sabotaje: escondido el documento, `runbook` vuelve a 🔴; restaurado, 🟢.
⭐ Un bloque de infraestructura que nombra las piezas exactas que toca **ya puede salir de 🔴 MVP**.

### Capa 2 — revisión de criterio (`rules/qa-dimensions.md`)

```
BLOCK separacion-motor-instancia — criterion review · 2026-08-07
  1 architecture ... 🟢  la frontera motor/instancia vive en mente.config.yml, no repartida
                         evidencia: los 4 cambios leen esa declaración; ninguno reintroduce ruta absoluta
  2 data .......... 🟢  no hay esquema; el único estado es el config declarativo
                         evidencia: `n/a` medido, no asumido — el §B no declara BD ni tablas
  3 abstraction ... 🟢  un solo lugar decide "esto es instancia": el config
                         evidencia: 4 checks corregidos, 0 copias de la regla en cada uno
  4 naming ........ 🟢  `additionalDirectories`, `WORKSPACE.md` dicen qué contienen
                         evidencia: ningún nombre exigió leer el cuerpo para entenderlo
  5 contracts ..... 🟢  un check ausente lo DICE (🟡 skip), nunca calla en verde
                         evidencia: §G decisión 2 · el clon reporta `1 additionalDirectories podados`
  6 necessity ..... 🟢  ⭐ medido: `instance/` NO se creó porque NINGÚN archivo estorbaba
                         evidencia: §I checkpoint 3 — 221 archivos medidos, 0 movidos
  ─────────────────────────────────────────────────────────────
  CRITERION VERDICT: 🟢 pass — 6/6 con evidencia
```

**VEREDICTO COMBINADO: 🟢 PRODUCTO** — capa 1 🟢 + capa 2 6/6 🟢, ambas con evidencia.

⭐ **Cerró primero en 🟡 y subió a 🟢 arreglando el medidor, no el documento.** El bloque no se
auto-aprobó declarando que el validador se equivocaba: lo dejó escrito, medible, y Brian ordenó
corregirlo el mismo día (`bin/grade-block` + `bin/generate-index`, verificados por sabotaje).

### La deuda que deja

1. ⭐ **La prueba de campo** — cero instalaciones externas. El clon lo verificó la IA en esta
   máquina: eso demuestra el mecanismo, **no la experiencia de otro dueño.**
2. **La separación real** (motor publicable en limpio, opción A) — otro bloque, después de éste,
   tal como el §B lo declaró desde el principio.

✅ **Cerrado el mismo día, ya no es deuda:** los 2 defectos de `bin/grade-block` (scope de archivos
sueltos · `blocks/<bloque>/docs/` nunca leído) y los 3 de `bin/generate-index` (un `✅` no contaba ·
capturaba filas fuera del §F · exigía 5 columnas cuando los §F reales tienen 4 o 5).
