# SUMMARY · blk-distribucion-2026-08
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian

## Purpose

Qué se hizo en este bloque y qué se aprendió, para quien lo consulte sin abrir el `BLOCK.md`.
El veredicto medido vive en su §K; la evidencia larga, en el `closing-report` de su carpeta docs.

---

## Qué se hizo

**Mente OS v2 pasó a ser instalable por alguien que no es Brian.** Seis sub-bloques:

- **Los 4 hooks, portables.** Antes apuntaban al home de un usuario, así que **un clon arrancaba
  sin ninguna puerta viva — en silencio**. Es el peor modo de fallo posible para un sistema cuya
  tesis es *"lo que está en código se cumple 100%"*.
- **`bin/init`** — genera `CLAUDE.md`, `PROJECT-RULES.md` y las rutas de los hooks desde
  `mente.config.yml`. **Genera, nunca se rellena a mano**: un valor copiado es correcto una vez.
- **`CAPABILITIES.md`** — el mapa de capacidades, porque **quien instala es un AGENTE, no una
  persona** (Brian, 2026-08-02). Un formulario asume que alguien lee etiquetas; un agente necesita
  saber qué puede ejecutar y dónde está la línea.
- **La frontera motor/instancia como CANDADO portable** — 24 reglas sobre `$CLAUDE_PROJECT_DIR`
  donde antes había 3 rutas absolutas que no viajaban.

**Veredicto al cerrar: 🟢 PRODUCTO** — capa 1 7/7 + capa 2 6/6 con evidencia mostrada.
Fue **el primer bloque de la historia juzgado por la capa 2**, que se llenó ese mismo día.

## What was learned

> ⭐ **Un límite que no has verificado no es un límite: es una suposición disfrazada.**

El sub-bloque 1 se declaró BLOQUEADO por *"necesita un clon limpio"*, tras una sonda ingenua que
resolvió a vacío. **Nunca se consultó la fuente.** La documentación oficial lo respondía, y los
tres sub-bloques se hicieron **en una hora**. Es el mismo defecto que un check que reporta verde
sin medir (`rules/rule-checks-must-measure.md`), un nivel más arriba: **un PLAN reportando
bloqueado sin medir.**

🔴 **Segundo hallazgo, encontrado trabajando:** las reglas `deny` de `Edit`/`Write` **no cubren
`Bash`** — un `python3 -c` reescribió un archivo bajo `bin/` que la regla de Edit protegía. La
misma puerta trasera que `rule-config-hygiene` §1.5.

## Qué NO cerró

**La prueba de campo real.** El clon se probó en esta máquina, por la IA: eso demuestra el
mecanismo, **no la experiencia de otro dueño**. Sigue pendiente que alguien externo lo instale.

---

Related: `blocks/archive/distribucion_2026-08/BLOCK.md` (el bloque como cerró) ·
`blocks/archive/distribucion_2026-08/connections.md` · el closing-report de su carpeta docs (la evidencia por dimensión) ·
`memory/PENDIENTES.md` (la deuda que dejó).
