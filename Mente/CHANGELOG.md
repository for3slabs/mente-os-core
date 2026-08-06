# CHANGELOG — Mente OS
**Status:** current · **Type:** append-only · **Updated:** 2026-08-05 · **Owner:** brian
**Verified by:** `bin/test-f0-f6` (§VERSION · el archivo `VERSION` y esta entrada deben coincidir)

## Purpose

Qué cambió en el motor, versión por versión. **La versión vive en UN solo sitio: `VERSION`.**
Todo lo demás la lee de ahí — un número copiado a mano es correcto exactamente una vez
(`principles/expertise/doc-structure.md` §3 regla 1).

> ⭐ **Por qué el versionado arranca en 0.1.0 y no en 2.0.0** (Brian, 2026-08-05):
> el nombre *"Mente OS v2"* describe la **arquitectura** — bloques, 3 dueños, veredicto en 2 capas —
> no la madurez del producto. **El versionado empieza limpio hoy**, con el primer número que un
> tercero puede citar al reportar un fallo. `0.x` dice la verdad medida: **construido y verificado,
> sin prueba de campo externa** — cero instalaciones por alguien que no sea Brian.
>
> La historia anterior no se pierde: vive en los **30 ADRs** (`rules/decisions/`) y en
> `Cerebro/Registro_Conversaciones.md`. Este archivo empieza donde empieza el versionado, no donde
> empezó el sistema.

---

## 0.1.0 — 2026-08-05

**Primera versión numerada.** El motor existía y funcionaba desde julio; lo que no existía era una
forma de decir *cuál* está corriendo. Eso es lo que abre esta entrada.

### El sistema ya sabe juzgar — los 3 dueños tienen criterio

- ⭐ **`rules/qa-dimensions.md` — la capa 2 del veredicto, viva.** Sus 6 dimensiones dejaron de ser
  un formulario vacío: cada una lleva el criterio de Brian **con evidencia obligatoria**.
- ⭐ **Las 7 disciplinas llenas** (`principles/expertise/*`): `dev-database` · `dev-backend` ·
  `dev-frontend` · `val-functional` · `val-integration` · `doc-planning` · `doc-structure`.
  **Huecos de criterio: 66 → 0.**
- **owner-1, owner-2 y owner-3 juzgan con cuerpo propio.** Antes, el único dueño que puede
  *negarse* a cerrar un bloque (owner-3) lo hacía sin criterio propio.

### Distribución

- `bin/init` genera una instancia nueva desde `mente.config.yml`, probado en un clon real.
- `CAPABILITIES.md` — el mapa que un agente lee para saber qué puede ejecutar y qué no tocar.
- `docs/WORKSPACE.md` — dónde vive cada cosa de esta máquina. ⛔ **Nunca un valor de credencial:
  dice DÓNDE, jamás CUÁL.**
- La frontera motor/instancia es un **candado portable** (24 reglas sobre `$CLAUDE_PROJECT_DIR`),
  no un párrafo.

### Reglas nuevas

- `rules/rule-shipping-flow.md` — rama → verificar → PR → ⛔ **no mergear**. **Transversal**: la
  declara cualquier disciplina en su §D, porque también hay PR de frontend y de base de datos.
- `rules/rule-checks-must-measure.md` — un check que solo has visto en verde no está probado.

### Puertas

- 🆕 **`pre-commit` bloquea un índice generado que esté desfasado.** El `--check` ya existía en los
  generadores; nada en la puerta lo llamaba, así que un índice viejo podía commitearse. Medido el
  mismo día: **lo estaba**.
- 🆕 **`check-clear-ready` lee el resultado de la batería antes de permitir un `/clear`** — y avisa
  si es de otro día. Un verde de la semana pasada no dice nada del trabajo de hoy.

### Verificación

- **`bin/test-f0-f6`: 173 checks, `failed: 0`.** Incluye una sección `SELF-TEST` que rompe sus
  propios checks a propósito.
- `bin/grade-block` — 3 defectos corregidos, todos hallados calificando: un comentario en el §B
  mataba el scope **en silencio** (⬜ falso con todas las métricas en verde) · dos validadores
  resolvían rutas desde raíces distintas · la línea de la capa 2 estaba escrita a mano como
  *"pending Brian"* y empezó a mentir el día que se llenó.
- **Las 20 reglas tienen ya un script que las verifica** (eran 17).

### Lo que esta versión NO tiene — declarado, no omitido

| | Estado |
|---|---|
| Instalaciones verificadas por alguien que no sea Brian | 🔴 **cero** |
| Tests en el producto que gobierna (`blk-demo`) | 🔴 **cero** |
| CI en el repositorio publicado | 🔴 no existe |
| Bugs reportados por usuarios externos | 🔴 ninguno |

> ⭐ **Por eso `0.x`.** El sistema está verificado **contra sí mismo**, que es exactamente lo que
> `principles/expertise/val-functional.md` §2.2 llama *reproducible* — y exactamente lo que no es *prueba de campo*.

---

Related: `VERSION` (la única fuente del número) · `rules/decisions/` (los 30 ADRs con la historia
anterior) · `docs/METRICS.md` (todo número vivo) · `memory/PENDIENTES.md` (lo que falta).
