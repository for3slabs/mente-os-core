# PR BASE · la base de un PR es `master`, siempre
**Status:** current · **Type:** rule · **Updated:** 2026-08-18 · **Owner:** brian
**Language:** US English · **Applies to:** EVERY discipline — backend · frontend · database · docs
**Split from:** `rules/rule-shipping-flow.md` §2-bis (2026-08-18, doc-structure.md §2.1: 261 líneas
sobre el techo de 250, y `-bis` es la señal literal de *"pártanme"*). Tercera hermana de
`rule-pr-batching.md` y `rule-post-merge-cleanup.md`.
**Verified by:** `bin/check-pr-base` · `bin/test-f0-f6` § "la base de un PR es master, y hay candado"
---

## Purpose

Contra qué rama se abre un PR — y por qué encadenar uno sobre otra rama sin mergear pierde trabajo
sin que git avise. `rule-shipping-flow.md` §2-bis da la orden en dos líneas; aquí vive el mecanismo,
el incidente medido y qué hacer cuando ya ocurrió.

> ⭐ **Es la tercera cara del mismo defecto.** `rule-pr-batching.md` §3 trata el squash cuando
> produce **conflictos visibles**; `rule-post-merge-cleanup.md` trata el squash cuando deja
> **trabajo empujado fuera**. Esta trata el squash cuando **no produce ninguna señal** — y por eso
> es la peor de las tres: no hay nada que resolver, nada que avise, y el PR queda MERGED.

---

## 1 · ⛔ LA REGLA

⛔ **La base de un PR es `master`. Nunca otra rama.** La excepción *"unless explicitly stacked"*
del anti-patrón #8 (`rule-shipping-flow.md` §2) **queda ANULADA en este repo**: encadenar solo es
seguro con merges de verdad (dos parents), y **este repo squashea**.

```bash
bin/check-pr-base master              # ⛔ antes de abrir CUALQUIER PR — rc=1 → no lo abras
bin/check-pr-base --audit             # ¿hay algún PR abierto ya encadenado?
```

**Una dependencia real entre dos PRs se resuelve ESPERANDO**, nunca encadenando:

```bash
git fetch origin && git rebase origin/master
```

---

## 2 · EL INCIDENTE Y EL MECANISMO

> 🔴 **Medido el 2026-08-18, no contado:**
> ```
> #32  feat/airlock-revision → master    mergeado 23:08:27   (SQUASH)
> #33  fix/session-resolver  → airlock   mergeado 23:08:36   (9 segundos después)
> ```
> Los dos quedaron **MERGED** en GitHub. El arreglo **nunca llegó a `master`**: 0 ocurrencias de
> `session_current`, `RESOLVER MISS`, `MENTE_SESSION_ID` y `Inicio (local, CST)`. **9 archivos,
> 329 líneas**, con la etiqueta de mergeado puesta.

**El mecanismo, para que no haya que redescubrirlo.** Un squash aplasta los commits de la rama en
**uno nuevo** sobre `master`. Ese commit **no es descendiente** de la rama original, así que el
parentesco se rompe en el instante del merge. Un PR encadenado sobre esa rama se mergea entonces
contra un ancestro que ya no lo es, y su trabajo se queda colgando — sin conflicto, sin aviso de
git, sin nada que se vea. **La etiqueta MERGED no significa que el código esté en `master`.**

⛔ **La excepción *"unless explicitly stacked"* del anti-patrón #8 NO aplica aquí.** Encadenar PRs
solo es seguro con merges de verdad (dos parents). **Este repo squashea**, así que la base de un
PR es `master` y nada más.

**Una dependencia real entre dos PRs se resuelve esperando:**

```bash
bin/check-pr-base master              # ✅ antes de abrir CUALQUIER PR
# la base aún no se mergeó → NO se encadena, se espera:
git fetch origin && git rebase origin/master
```

⭐ **Por qué esto es un SCRIPT y no solo este párrafo.** El anti-patrón #8 **ya estaba escrito**
desde el 05-ago, y la memoria `feedback_squash_merge_borra_trabajo_empujado` lo registraba desde
el 08-ago tras pasar **dos veces el mismo día**. Ambos se leyeron al arrancar la sesión del 18-ago
y **ninguno se aplicó al elegir la base**. Tener el dato no impidió el error: la regla escrita se
cumplió 0 de 1 veces el día que importaba. *Código 100%, documento 40-60%* — por eso ahora hay
`bin/check-pr-base`, y por eso la batería verifica que el candado siga puesto.

📌 **Detección, no solo prevención:** `bin/check-pr-base --audit` marca los PR abiertos ya
encadenados, y `bin/check-health` sigue avisando 🟡 de las ramas cuyo contenido no llegó a la base
(el detector post-mortem que **sí cazó** este incidente, pero después de mergear).

---

---

---

## 3 · SI YA OCURRIÓ — cómo se repara

⚠️ **La etiqueta MERGED no prueba nada.** Se verifica por CONTENIDO, nunca por el estado del PR:

```bash
git show origin/master:<ruta> | grep -c "<marca del cambio>"    # 0 = no llegó
git diff --name-only origin/master origin/<rama>                # qué difiere
```

**La reparación** es una rama nueva desde `origin/master` con `git cherry-pick` de los commits
originales — siguen existiendo en la rama vieja aunque su PR figure mergeado — y la batería
corrida **sobre esa rama**, no sobre el árbol donde se escribió
(`feedback_verificar_fuera_del_arbol_del_autor`).

⛔ **No borrar la rama huérfana hasta que la reparación esté mergeada:** es el único sitio donde
vive ese trabajo. `rule-post-merge-cleanup.md` ya lo exige — verificar primero, borrar después.

---

Related: `rules/rule-shipping-flow.md` (§2 anti-patrón #8 · §2-bis da la orden) ·
`rules/rule-pr-batching.md` (§3 el mismo squash con conflictos visibles) ·
`rules/rule-post-merge-cleanup.md` (verificar que viajó antes de borrar) ·
`bin/check-pr-base` (el candado) · memoria `feedback_squash_merge_borra_trabajo_empujado`.
