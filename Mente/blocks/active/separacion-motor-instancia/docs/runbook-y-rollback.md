# Runbook y rollback · separacion-motor-instancia
**Status:** current · **Type:** contract · **Updated:** 2026-08-07 · **Owner:** brian

## Purpose

Cómo se VERIFICA lo que hizo este bloque, y cómo se DESHACE si estorba. Vive aquí y no dentro del
contrato porque `bin/grade-block` mide los documentos del bloque — y porque un runbook enterrado
en un §K no se puede seguir sin leer el contrato entero.

## Runbook — cómo se verifica esto (paso a paso)

Lo que este bloque cambió solo se puede comprobar **fuera del árbol donde se escribió**:

```bash
T=$(mktemp -d) && git clone -q -b master . $T/c && cd $T/c/Mente
bin/test-f0-f6                 # ① en frío: 6 fallos esperados (falta la instancia)
cp templates/mente.config.yml.template mente.config.yml   # ② declarar el dueño
bin/init --force               # debe decir: WORKSPACE.md written · N additionalDirectories podados
bin/test-f0-f6                 # ③ 1 fallo: `check-clear-ready registered=no` — CORRECTO
```

⭐ El paso ③ es el que importa: **un número distinto de 1 significa regresión**. `bin/verify-all`
F8 lo automatiza con `CLON_CAP=7` sobre el paso ①.

## Rollback — cómo volver atrás si algo de esto estorba

Ningún cambio de este bloque destruye datos; los cuatro se revierten por separado:

| Si estorba | Cómo se revierte |
|---|---|
| la poda de `additionalDirectories` | `bin/init` deja `.claude/settings.json.mente-bak` — un `mv` lo restaura |
| `docs/WORKSPACE.md` generado | `git show f2f47d2~1:Mente/docs/WORKSPACE.md > Mente/docs/WORKSPACE.md` (el historial lo conserva aunque ya no se rastree) |
| las guardias `HAS_INST` de la batería | quitar el `if`: los checks vuelven a exigir la instancia |
| el matcher de `hooks/pre-edit-standards.py` | `git revert` del commit; el hook nunca bloquea, solo informa |

⛔ **Lo único que NO se revierte solo:** `docs/WORKSPACE.md` está en `.gitignore`, así que borrarlo
del disco lo pierde de la copia viva. Se recupera del historial con el comando de arriba.

---

Related: `blocks/active/separacion-motor-instancia/BLOCK.md` (el contrato que esto ejecuta) ·
`bin/verify-all` (F8 automatiza el paso ①) · `rules/rule-checks-must-measure.md` (§D, la familia
que este bloque aplicó).
