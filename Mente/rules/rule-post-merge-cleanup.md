# POST-MERGE CLEANUP · verificar que viajó, luego borrar la rama
**Status:** current · **Type:** rule · **Updated:** 2026-08-08 · **Owner:** brian
**Language:** US English · **Applies to:** EVERY discipline — backend · frontend · database · docs
**Split from:** `rules/rule-shipping-flow.md` §1-bis (2026-08-08, doc-structure.md §2.1: 279 líneas
sobre el techo de 250, y `-bis` es la señal literal de *"pártanme"*)
**Verified by:** `bin/test-f0-f6` § "el post-merge borra la rama, pero VERIFICA antes"
---

## Purpose

Qué se hace con una rama **después** de que su PR se mergeó. `rule-shipping-flow.md` termina en
*"⛔ no mergear"* porque mergear es decisión humana; esta regla empieza justo después de esa
decisión y cierra el ciclo.

> **Brian, 2026-08-07:** *"cuando la rama ya fue mergeada, eliminada de local + remoto."*

---

## 1 · LOS DOS PASOS — y el orden no es preferencia

```
1 · VERIFICAR   gh pr list --head <rama> --state all   → MERGED = su trabajo entró
                git diff origin/<base> <rama> --stat   → vacío  = todo llegó
2 · BORRAR      git branch -d <rama> && git push origin --delete <rama>
```

⛔ **Borrar antes de verificar destruye la única copia del trabajo que el squash pudo dejar fuera.**

⚠️ **`git branch -d`, nunca `-D` de entrada.** La minúscula **se niega** si la rama tiene commits
que la base no contiene; la mayúscula borra en silencio. Esa negativa es el último candado antes de
perder trabajo. **El squash la hace protestar aunque todo haya viajado** (reescribe el sha), así que
su queja obliga a **mirar el contenido** — nunca a forzar sin haberlo mirado.

🔬 **Medido 2026-08-08:** `fix/sonda-nested-repo` hizo protestar a `-d` con 2 commits "ausentes"; el
diff de contenido contra master salió **vacío** — eran los mismos cambios con otro sha. Forzar sin
comprobarlo habría sido correcto por casualidad, y esa casualidad es la que un día no se cumple.

---

## 2 · POR QUÉ VERIFICAR VA PRIMERO

**El squash colapsa la rama en un commit nuevo**, así que git **no puede** detectar que faltó algo:
no hay conflicto, no hay divergencia, el diff simplemente no lo incluye. Es el anti-patrón #8 de
`rule-shipping-flow.md` §2, y **pasó 4 veces el 2026-08-07** — una de ellas borró de `master` el
candado que vigila exactamente este defecto.

> ⭐ **Una rama mergeada es la copia de seguridad de su propio merge, y solo hasta que se comprueba
> que el merge la contiene.** Después no aporta nada y estorba.

📊 **El coste de no borrar, medido:** el 2026-08-08 había **10 ramas** colgando. Cuatro parecían
tener trabajo suelto y hubo que auditarlas una por una; las diez tenían su PR MERGED. El tiempo se
gastó en demostrar que no había nada que rescatar.

---

## 3 · ⛔ LAS ÚNICAS EXCEPCIONES — se conserva la rama

| Caso | Por qué |
|---|---|
| **Migración de versión mayor** (v1 → v2 y equivalentes) | la rama es el único estado íntegro del "antes"; un rollback la necesita entera, no reconstruida commit a commit |
| **Vida o muerte** — irreversible, en producción, o que toca datos reales | el criterio es *"¿y si hay que volver HOY?"*, no el tamaño del diff |

**Fuera de esos dos casos: se borra.** Brian, 2026-08-07: *"al menos que sea algo delicado muuuuy
delicado de vida o muerte, o en este caso cuando pasamos de v1 a v2 — solo esos casos."*

⛔ **La duda no conserva la rama: se pregunta.** Guardar "por si acaso" es cómo se llegó a 10.

---

## 4 · ⛔ NUNCA COMMITEAR SOBRE UNA RAMA CUYO PR YA ESTÁ MERGED

```
gh pr list --head <rama> --state all      → si sale MERGED, esa rama está muerta
```

Rama muerta → **rama nueva desde `origin/<base>` + `git cherry-pick`**, nunca commits encima.

🔬 **Medido 2026-08-07:** `git status` decía `[ahead 1]` y era **cierto y engañoso a la vez** —
adelantada respecto al remoto *de esa rama*, no respecto a master. **La rama local no sabe que su
PR se mergeó.** Un PR abierto desde ahí propone la base equivocada.

---

Related: `rules/rule-shipping-flow.md` (§1-bis apunta aquí; el ciclo hasta el merge) ·
`rules/rule-shipping-flow.md` §2 anti-patrón #8 · `principles/expertise/doc-structure.md` §2.1
(por qué esta mitad existe).
