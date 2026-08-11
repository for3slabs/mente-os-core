# CONTRACT · CAMPAIGN.md
**Status:** current · **Type:** contract · **Updated:** 2026-08-10 · **Owner:** brian
**Applies to:** every file at `campaigns/<name>/CAMPAIGN.md`
**Verified by:** `bin/check-campaigns` · **Plan:** `docs/plans/PLAN-campana.md` (fase C1)
---

## 0 · LA FORMA

**Una campaña = UN archivo.** Secciones A-H en este orden. Máximo **150 líneas**.

⭐ **Más bajo que un bloque (200) a propósito:** la campaña **no ejecuta**, ordena. Si necesita 200
líneas para explicar su misión, la misión no está clara — o son dos campañas.

| Momento | Obligatorio |
|---|---|
| **ABRIR** | A · B · C — **tres campos** |
| **Mientras vive** | D-G, según se sepan |
| **CERRAR** | todo + `bin/check-campaigns` en verde |

> **Barata de abrir, cara de cerrar** — mismo principio que `rules/contract-block.md` §0: si abrir
> cuesta diez campos, el trabajo ocurre *sin* campaña y el contexto se pierde, que es justo lo que
> esta figura existe para evitar.

---

## 1 · LAS SECCIONES

| § | Sección | Requerida | Límite |
|---|---|---|---|
| **A** | `Identity` | 🔴 ABRIR | 5 líneas |
| **B** | `Mission` — qué se persigue y cuándo termina | 🔴 ABRIR | 10 líneas |
| **C** | `Authority` — quién manda cuando dos documentos se contradicen | 🔴 ABRIR | 5 líneas |
| **D** | `Standards` — el `§D` que **heredan todos** sus bloques | 🟡 vivo | 12 líneas |
| **E** | `Blocks` — los bloques que la componen | 🟡 vivo | sin techo (ver §2) |
| **F** | `Shared context` — el contexto GRANDE, igual para todos | 🟡 vivo | 40 líneas |
| **G** | `Channel` — los hechos que un bloque necesita de otro | 🟡 vivo | sin techo |
| **H** | `Closing` | 🔴 CERRAR | — |

---

## 2 · ⭐ §E · CUÁNTOS BLOQUES — DINÁMICO, sin techo ni suelo

> **Brian, 2026-08-10:** *"No lo sabemos hasta que empecemos a desarrollarlo, eso es algo dinámico.
> Va a haber campañas con muchos bloques y algunas con pocos."*

⛔ **El contrato NO fija un número.** Fijarlo produciría uno de dos daños: **inventar bloques para
llenar el hueco**, o **partir la misión** para que quepa. Ambos falsean el trabajo para complacer al
formulario.

**Lo único obligatorio: al abrir, al menos UN bloque declarado.** Una campaña sin bloques no ordena
nada — es un título.

```markdown
## Blocks
| bloque | qué persigue | estado |
|---|---|---|
| blk-<id> | una frase | active · blocked · closed |
```

---

## 3 · §D · LOS ESTÁNDARES SE HEREDAN, NO SE COPIAN

El `§D` de la campaña **llega a todos sus bloques** vía `hooks/pre-edit-standards.py`. Un bloque
hijo puede **AÑADIR** en su propio `§D`; **nunca quitar** (`rules/rule-inheritance.md`: las reglas
se suman, en conflicto gana la más estricta).

⛔ **Heredar, no copiar.** Si el estándar se copia al hijo, las dos listas divergen — el mismo
defecto que las tablas de decisiones duplicadas (**75 filas contra 37**, medido). 🔬 La prueba que
lo distingue: **quitar un estándar de la CAMPAÑA debe quitarlo de todos los hijos.** Si sigue
llegando, se copió.

---

## 4 · §G · EL CANAL — un hecho se declara UNA VEZ

> **Brian, 2026-08-10:** *"Si un bloque quiere conocer el contexto de otro lo puede hacer… para que
> no se interprete de distintas maneras. Siempre la campaña lo va a regir."*

Cuando un bloque necesita saber algo de otro, **el hecho se escribe en el §G de la campaña**, no se
lee del hermano.

```markdown
## Channel
| hecho | lo aporta | lo necesitan | fecha |
|---|---|---|---|
| `session.ts` es el guardián único de la sesión | blk-a | blk-b · blk-c | 2026-08-10 |
```

⛔ **El canal NO relaja `rules/rule-isolation.md` §1:** leer los archivos de otro bloque sigue
prohibido. Lo que el canal permite es **leer el HECHO ya redactado**, no el bloque.

⭐ **Por qué pasa por la campaña:** si dos bloques se leen directamente, cada uno interpreta lo que
ve. Declarado una vez, **los dos leen la misma frase** — una sola redacción, una sola
interpretación.

---

## 5 · CERRAR UN BLOQUE DENTRO DE UNA CAMPAÑA

> **Brian, 2026-08-10:** *"Todo debe estar en comunicación y entender que lo que se realizó puede
> afectar o mejorar a algo. No se realiza a ciegas: se evalúa toda la campaña."*

Además de su `§K` normal, un bloque de campaña declara **el impacto sobre sus hermanos**:

```markdown
### Impacto en la campaña
- blk-b · queda AFECTADO: <qué cambia para él>
- blk-c · sin impacto, porque <razón>
```

⛔ **El silencio no vale.** Decir *"ninguno"* es una respuesta válida **con su razón**; no decir nada
no lo es. Un cierre que no mira a los hermanos es trabajo a ciegas.

⚠️ Hoy `connections.md` ya pide algo así al archivar, pero **solo mira hacia fuera del bloque** —
nunca hacia sus hermanos de campaña.

---

## 6 · UNA CAMPAÑA NO CIERRA SI…

| Condición | Por qué |
|---|---|
| queda un bloque `active` o `blocked` | igual que un bloque no cierra con sub-bloques abiertos |
| algún bloque cerró **sin declarar impacto** | el §5 quedó incumplido |
| `§C Authority` está vacío | nadie sabría con qué vara se juzgó |
| `§H Closing` falta | sin veredicto no hay cierre |

---

## 7 · ⚠️ LO QUE UNA CAMPAÑA NO ES

- **No sustituye al bloque.** El bloque sigue siendo la unidad de trabajo, con su `§A-K` intacto.
- **No relaja techos.** Los hijos siguen en 200 líneas y 20 sub-bloques.
- **No es un cajón.** Declara sus bloques **por nombre** en `§E`: lo que no está, no pertenece.
- **No decide criterio.** La autoridad es la que declare su `§C` — para el producto,
  `rules/rule-product-authority.md`.
- **No reemplaza al bloque de pendientes del mismo nombre.** Uno registra QUÉ falta; la campaña
  organiza CÓMO se ataca. ⚠️ Si comparten nombre, **cada uno apunta al otro** — dos cosas con el
  mismo nombre y distinta naturaleza es como nace una confusión.

---

Related: `docs/plans/PLAN-campana.md` (el plan que lo diseñó) · `rules/contract-block.md` (la forma
que imita) · `rules/rule-inheritance.md` (por qué se hereda y no se copia) ·
`rules/rule-isolation.md` (el aislamiento que el canal canaliza, no relaja) ·
`rules/rule-product-authority.md`.
