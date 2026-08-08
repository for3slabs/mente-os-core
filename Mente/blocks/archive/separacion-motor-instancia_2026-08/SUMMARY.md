# SUMMARY · blk-separacion-motor-instancia-2026-08
**Status:** current · **Type:** analysis · **Updated:** 2026-08-07 · **Owner:** brian

## Purpose

Qué se hizo en este bloque y qué se aprendió, para quien lo consulte sin abrir el `BLOCK.md`.
El veredicto medido vive en su §K; el detalle de verificación, en `blocks/archive/separacion-motor-instancia_2026-08/docs/runbook-y-rollback.md`.

---

## Qué se hizo

**Un clon de este repo ya verifica el MOTOR sin exigir la INSTANCIA de Brian.** El recorrido
medido en un clon limpio de master mergeado: **6 fallos en frío → 1 tras `bin/init`** — y ese 1
(`check-clear-ready registered=no`) **es la respuesta correcta**, porque la sesión de un árbol
recién nacido no está registrada y ponerse verde ahí sería mentir.

Cinco sub-bloques, todos cerrados:

- **`bin/init` poda los `additionalDirectories` muertos y lo DICE** — un directorio de otra
  máquina dejaba de existir y el arranque lo arrastraba en silencio.
- **`docs/WORKSPACE.md` se GENERA de plantilla, no se hereda.** Su propia línea 3 lo declaraba
  desde el 05-ago y **nadie lo hacía cumplir**: el mapa de la máquina de Brian viajaba con el motor.
- **Los checks de instancia se SALTAN lo ausente en 🟡, no fallan.** Un check ausente no es un
  check fallido — pero nunca se da por bueno en silencio.
- **Un repo hermano ausente deja de ser una cita rota** — `check-links` 12 → 0 en el clon.
- **Clon limpio verificado end-to-end desde master mergeado**, no desde la rama de trabajo.

Además, `owner == "Maestro"` estaba hardcodeado en `check-structure`.

**Veredicto: 🟢 PRODUCTO** — capa 1 🟢 + capa 2 (criterio) 6/6 🟢, ambas con evidencia.

⭐ **Cerró en 🟡 y subió a 🟢 arreglando el MEDIDOR, no el documento.** `grade-block` marcaba
`runbook NO` y `rollback NO` **con el documento escrito y en su sitio**; en vez de ensanchar el §B
para complacerlo, el 🔴 se dejó escrito y medible, y Brian ordenó corregir el medidor el mismo día.

## What was learned

> ⭐ **Una explicación cómoda para un rojo es cómo un bug sobrevive a una auditoría.**

La etiqueta *"son 8 fallos y son de la instancia de Brian"* llevaba meses tapando **4 defectos
reales del motor** (familia D casos 5-8 de `rules/rule-checks-must-measure.md`). 🔴 El peor:
`grade-block archived` — bajo `pipefail` el pipe tomaba el exit `2` del veredicto 🔴 MVP **aunque
el `grep` acertara**. Exigía **la nota que saca en la máquina de su autor**: un check atado a la
instancia **sin nombrarla una sola vez**. Un check así no se encuentra buscando el nombre de Brian
en el código, porque no está.

> ⭐ **Mover archivos habría escondido el defecto en vez de corregirlo.**

La hipótesis de partida era mover 221 archivos de instancia a una carpeta `instance/`. **Medido:
ninguno estorbaba.** Lo que fallaba eran los CHECKS que los interrogaban mal. `instance/` NO se
creó y el §B del bloque se corrigió — la medición cambió el alcance, no al revés.

Tercer hallazgo, de paso: **`hooks/pre-edit-standards.py` confundía MENCIONAR una ruta con
RECLAMARLA** (`d in target`, subcadena). Este bloque nombró `marca-personal/` solo para decir de
quién NO era, y el hook le atribuyó los archivos de `demo`. Con dos bloques activos, el que más
"habla" en su §B se roba los del otro **y el aviso correcto deja de llegar**. Arreglado el mismo
día sin cambiar el formato del §B — el coste que se temía no hizo falta pagarlo.

## Qué NO cerró

**La prueba de campo real.** El clon lo verificó la IA en esta máquina: eso demuestra el
mecanismo, **no la experiencia de otro dueño.** Cero instalaciones externas verificadas.

**La separación real** (opción A: partir la historia, motor publicable en limpio) — decisión de
Brian el 2026-08-07: **opción C, un solo repo, reversible.** Es otro bloque, después de éste.

---

Related: `blocks/archive/separacion-motor-instancia_2026-08/BLOCK.md` (el bloque como cerró) ·
`blocks/archive/separacion-motor-instancia_2026-08/connections.md` ·
`blocks/archive/separacion-motor-instancia_2026-08/docs/runbook-y-rollback.md` ·
`memory/PENDIENTES.md` (la deuda que dejó) · `rules/rule-checks-must-measure.md`.
