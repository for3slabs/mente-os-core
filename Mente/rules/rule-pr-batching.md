# RULE · PR BATCHING — un PR por bloque, no por error
**Status:** current · **Type:** rule · **Updated:** 2026-08-08 · **Owner:** brian
**Language:** US English · **Applies to:** EVERY discipline — backend · frontend · database · docs
**Split from:** `rules/rule-shipping-flow.md` §0-bis (2026-08-08: 297 líneas sobre el techo de 250,
y `-bis` es la señal literal de *"pártanme"* — `principles/expertise/doc-structure.md` §2.1)
**Verified by:** `bin/test-f0-f6`
---

## Purpose

**Cuántos pendientes entran en un PR, y cuándo un bloque cierra el suyo.** `rules/rule-shipping-flow.md`
dice cómo un ticket se convierte en PR; esta regla dice **cuántos tickets van en ese PR**.

## 1 · CUÁNTOS PENDIENTES POR PR

> **Brian, 2026-08-08:** *"cuando estás solucionando un bloque no se hace un PR por cada error, es
> un PR por todo el bloque, de tal manera no tenemos tantos PR. Cada 4 errores de un bloque es un PR."*

| Cuántos pendientes de un mismo bloque | Cuántos PRs |
|---|---|
| 1 a 4 | **1 PR** |
| 5 a 8 | 2 PRs |
| 9+ | uno por cada 4 |

⛔ **Un PR por error es el anti-patrón.** El 2026-08-08 se abrieron **5 PRs en una sola sesión**
(#20-#24), cada uno con su rama, su verificación y su merge. **El coste no es el PR: es la cadena
que arrastra** — cada merge por squash reescribe shas, y este repo ya perdió trabajo **4 veces** por
esa vía (§2 anti-patrón #8). Menos PRs = menos superficie donde el squash puede morder.

⭐ **Por qué el tope es 4 y no "todo el bloque":** un PR que toca 7 pendientes es **irrevisable** —
el diff deja de leerse y se aprueba por confianza, que es exactamente lo que un PR existe para
evitar. Cuatro es el punto donde el diff todavía se lee entero.

**Se agrupa por BLOQUE, no por tema:** los pendientes de un bloque comparten análisis y plan global,
así que su diff se revisa con el mismo contexto cargado. Mezclar bloques obliga a cambiar de
contexto dentro del mismo diff.

## 2 · ⭐ El ÚLTIMO PR de un bloque es su CIERRE — y no espera a llenar 4

> **Brian, 2026-08-08:** *"cuando se terminan los pendientes de un bloque, sin importar la cantidad,
> se genera un PR. Es como si fuera un cierre del bloque, que también debe apuntar a los PR que se
> crearon de ese bloque."*

**Quedan 3 pendientes y son los últimos → PR ya.** Esperar a juntar 4 dejaría el bloque terminado y
sin cerrar, que es cómo un bloque acabado se queda meses en `active/` (pasó con
`separacion-motor-instancia`: 5/5 hecho y semanas en `active/`).

**El PR de cierre lleva, además del diff:**

| Qué | Por qué |
|---|---|
| 🔗 **Los PRs anteriores del bloque**, enlazados | el bloque se revisó en trozos; su cierre es el único sitio donde se ve entero |
| 📊 El **estado final** de todos sus pendientes | cerrados con fecha, y los que quedan abiertos **con su razón** |
| 🩺 Las medidas del bloque **antes → después** | si no cambió nada medible, el bloque no hizo nada |

⛔ **Un bloque no se cierra en silencio.** Sin el PR de cierre, la única huella de que terminó son
N PRs sueltos que nadie vuelve a leer juntos.

---

---

## 3 · ⭐ UN PR CON CONFLICTOS — casi siempre son el SQUASH, no trabajo rival

> **Brian, 2026-08-08:** *"¿no habías hecho el sistema de conflictos? Aparece conflictos,
> soluciónalos."* — **y no existía**: ninguna regla los trataba. Se escribió al encontrarlo.

**El caso normal en este repo, medido:** el PR #27 mostró **3 archivos en conflicto**. La causa no
era trabajo rival — era que **el merge por squash del #26 reescribió el sha** de un commit que la
rama ya tenía. Git ve dos commits distintos con el mismo contenido y marca conflicto.

### El procedimiento — 3 pasos, y el primero es diagnosticar

```
1 · ¿DE QUÉ TIPO ES?   git log --oneline HEAD..origin/<base>     ¿qué trae la base?
                       git log --oneline origin/<base>..HEAD     ¿qué traigo yo?
                       git show <mío> --stat  vs  git show <suyo> --stat
2 · SI ES EL SQUASH    git rebase origin/<base>    → git SALTA los ya aplicados, 0 conflictos
3 · EMPUJAR            git push --force-with-lease  ⛔ nunca --force a secas
```

⛔ **`--force-with-lease`, jamás `--force`.** El primero **se niega** si alguien empujó a esa rama
desde tu último fetch; el segundo pisa su trabajo sin avisar. En una rama con PR abierto, `--force`
a secas es la forma más rápida de borrar trabajo ajeno.

### ⛔ Lo que NUNCA se hace

| Nunca | Por qué |
|---|---|
| **Resolver conflictos en la web de GitHub** | el editor no corre la batería: se mergea sin saber si el sistema sigue verde |
| **`Accept both changes` sin leer** | en un archivo generado (`INDEX.md`, `METRICS.md`) duplica filas y produce un índice que nadie midió |
| **Resolver sin backup** | un rebase reescribe historia; antes se copia lo que no se puede reconstruir |
| **Dar por bueno el rebase sin verificar** | tras resolver, **la batería vuelve a correr**: `failed: 0` o no se empuja |

⭐ **Los archivos generados no se resuelven a mano: se REGENERAN.** `INDEX.md` y `METRICS.md`
entraron en conflicto porque ambos lados los habían regenerado. Elegir "el mío" o "el suyo" es
elegir entre dos fotos viejas — la respuesta correcta es correr `bin/generate-index` después.

---

Related: `rules/rule-shipping-flow.md` (el ciclo hasta el PR; §0-bis apunta aquí) ·
`rules/rule-post-merge-cleanup.md` (qué pasa después del merge) ·
`rules/contract-pending.md` (qué es un bloque de pendientes).
