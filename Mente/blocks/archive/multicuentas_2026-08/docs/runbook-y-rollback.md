# RUNBOOK y ROLLBACK · bloque multicuentas

**Status:** current · **Type:** plan · **Updated:** 2026-08-20 · **Owner:** brian
**Block:** `blocks/archive/multicuentas_2026-08/BLOCK.md`

## Purpose

Cómo se opera este sistema y **cómo se deshace entero**. Lo exige `bin/grade-block` para un
bloque `infra`, y con razón: este bloque tocó el `.gitignore`, `settings.json` y **reescribió
el historial de un repo público**. Sin esto escrito, revertir es adivinar.

---

## 1 · RUNBOOK — paso a paso, el uso diario

### ¿Con qué cuenta toco este repo?

```bash
bin/conectar-cuenta for3slabs/for3s-os     # qué cuenta, qué guía, si el acceso está vivo
bin/conectar-cuenta --list                 # todos los repos registrados
```

⛔ **Nunca imprime el valor de una credencial** — da la ruta y el estado.

### ¿El registro sigue diciendo la verdad?

```bash
bin/check-accounts        # 0 limpio · 1 avisos · 2 un remoto real no está declarado
```

### Añadir un repo nuevo

1. Una fila en `cuentas.tsv` (TAB entre columnas, **nunca espacios**).
2. Su `por_que_existe` es **obligatorio** — un repo que no puede justificarse es basura.
3. `bin/check-accounts` para confirmar.

⚠️ **Sin ese paso la puerta DENIEGA el push** — a propósito: trabajo que sale hacia un destino
que nadie declaró es trabajo que nadie sabe dónde quedó.

---

## 2 · ROLLBACK — cómo se deshace TODO

| Qué | Cómo se deshace | Riesgo |
|---|---|---|
| **el historial reescrito** | `git clone /home/brianweb3/backups-mente-os/mente-os-for3s_20260820-152200.git` — espejo del 2026-08-20 15:22 · 135/135 commits · **conserva los 2 con la contraseña** | ninguno: copia aparte |
| **el árbol completo** | `/home/brianweb3/backups-mente-os/mente-os-for3s_20260820-152200-worktree.tar.gz` (79M) — incluye `secrets/`, que no viaja en git | ninguno |
| la puerta | quitar el bloque `gate-accounts` de `.claude/settings.json` | vuelve el agujero |
| `cuentas.tsv` gitignored | quitar su línea del `.gitignore` | 🔴 un clon vuelve a heredar cuentas ajenas |
| los 3 comandos | borrar `bin/check-accounts` · `bin/conectar-cuenta` · `hooks/gate-accounts.py` | la batería §F7 se pone 🔴 y **dice cuál falta** |
| §F7 de la batería | `git revert c33c24e` | se pierden 16 comprobaciones |

⛔ **Lo que NO tiene vuelta atrás:** el force-push del historial ya ocurrió. El espejo permite
**recuperar el contenido**, no restaurar el repo público a su estado anterior sin otro force-push.

⚠️ **Y la contraseña no se rotó** — decisión consciente de Brian (2026-08-20). Estuvo pública, así
que el rollback del historial **no revierte la exposición**: solo la quita de GitHub hacia delante.

---

Related: `../BLOCK.md` · `../../../../docs/plans/PLAN-multicuentas.md` ·
`../../../../secrets/README.md` (las 3 guías de acceso).
