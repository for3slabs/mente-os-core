# FUENTES DE VERDAD — qué repo manda, y por qué

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-20 · **Owner:** brian
**Level:** 🚪 ENTRY-POINT — se lee antes de tocar cualquier repo
**Verified by:** `bin/check-accounts` (compara esto contra `git remote -v`)

## Purpose

**Un solo lugar que responde: ¿a qué repo va este trabajo, y quién lo gobierna?**

Existe porque la respuesta vivía en la cabeza de Brian y en tres documentos que se contradecían:
`PROJECT-RULES.md` estuvo **46 días** nombrando un repo que había dejado de ser oficial, la
memoria **31** llamando *"copia vieja"* al que el servidor usa a diario, y `RETOMAR.md` **24**
declarando una tríada ya rota. Ningún validador los comparaba con la máquina.

> ⛔ **Este archivo NO es el registro.** El registro es `cuentas.tsv`, que una máquina lee.
> Esto explica **el porqué**; `cuentas.tsv` guarda **el dato**, y `bin/check-accounts` verifica
> que el dato no contradiga a `git remote -v`. Un número o una URL copiados a mano son correctos
> exactamente una vez.

---

## 1 · ⭐ EL CAMBIO DEL 2026-08-20 — leerlo antes que nada

> ## `for3slabs/mente-os-core` es la nueva FUENTE DE VERDAD del motor.
> ## `for3slabs/mente-os-for3s` está ARCHIVADO. ⛔ No se empuja ahí.

**Por qué se mudó, medido:** el repo anterior fue público y llevó la contraseña del servidor en
texto plano en 4 archivos. Se limpió el historial, pero **los objetos huérfanos siguen servidos
por GitHub** (`git/blobs/<sha>` los devolvía) y **ningún comando de git los borra** — solo su
recolección de basura o GitHub Support.

⭐ **Un repo nuevo es lo único que ELIMINA el problema en vez de esconderlo:** se empujó el
historial ya limpio —**137 commits, 2159 blobs escaneados, 0 contaminados**— a un repo que nunca
tuvo esos objetos. Verificado: los 3 blobs contaminados devuelven `Not Found` allí.

---

## 2 · EL MAPA — quién manda sobre qué

| Repo | Rol | Cuenta | ¿Se empuja? |
|---|---|---|---|
| ⭐ **`for3slabs/mente-os-core`** | **el motor Mente OS v2 + la instancia** | `for3slabs` | ✅ sí — es el `origin` |
| `for3slabs/for3s-os` | **el taller** del producto | `for3slabs` | ✅ sí — `origin` en el servidor |
| `for3slabs/for3s` | **el respaldo** del producto verificado | `for3slabs` | ✅ sí — `backup` en el servidor |
| `for3slabs/mente-os-maestro` | el **controlador** que apunta a las ramas | `for3slabs` | ✅ repo anidado, propio `.git` |
| `ElBrAyAn1967/For3s` | **el sitio y la demo** (Next.js) | `ElBrAyAn1967` | ⚠️ un push a `main` **PUBLICA** |
| `fruterito101/mente-os` | el motor **publicado** en MIT | `fruterito101` | solo releases |
| ⛔ `for3slabs/mente-os-for3s` | **ARCHIVADO** — el anterior | — | 🔴 **NO** |
| ⛔ `fruterito101/for3s` | **URL VIEJA** (301 desde el 4-jul) | — | 🔴 **no citar** |

---

## 3 · ⚠️ LAS DOS TRAMPAS QUE YA COSTARON DÍAS

### 3.1 · El producto tiene DOS remotos, y los dos importan

```
servidor ~/for3s-os
   origin  → for3slabs/for3s-os     el taller
   backup  → for3slabs/for3s        el respaldo
```

⛔ **Empujar a uno solo los deja divergentes.** Pasó el 2026-07-23: dos commits firmados vivieron
**24 días** fuera de GitHub y nada avisó. Hoy la puerta avisa antes.

### 3.2 · `fruterito101` NO es otra persona

Es la cuenta **personal de Brian** y **admin de la organización `for3slabs`** — medido con
`gh api user/memberships/orgs/for3slabs` → `rol: admin · active`. Una sola sesión de `gh` alcanza
ambas, y ver `fruterito101` en `gh auth status` **es correcto**.

⛔ **`ElBrAyAn1967` sí es otra identidad**: el sitio, por SSH.

---

## 4 · CÓMO SE USA ESTO — no se lee, se ejecuta

```bash
bin/conectar-cuenta <owner/repo>    # qué cuenta, qué guía, si el acceso está vivo
bin/conectar-cuenta --list          # todos los repos registrados
bin/check-accounts                  # ¿lo escrito coincide con git remote -v?
```

**Dos puertas lo hacen cumplir, y la segunda no se rodea:**

| Capa | Qué | Se puede evadir |
|---|---|---|
| 1 · `hooks/gate-accounts.py` | lee el comando, explica **antes** | ⚠️ sí — 5 formas medidas (alias, `eval`, `xargs`…) |
| 2 · `hooks/pre-push.sh` | **lo ejecuta git** en el push real | ⛔ **no** — 6 formas probadas, 6 abortadas |

⭐ **Un repo que no está en `cuentas.tsv` no recibe trabajo.** No es un obstáculo: es la diferencia
entre saber dónde está tu trabajo y suponerlo.

---

## 5 · AÑADIR UN REPO NUEVO

1. Una fila en `cuentas.tsv` (TAB entre columnas, **nunca espacios**).
2. Su **`por_que_existe` es obligatorio** — *"un repo que no puede justificarse es basura"* (Brian).
3. `bin/check-accounts` para confirmar.

⚠️ Sin ese paso **el push se aborta**, y es a propósito.

---

Related: `../cuentas.tsv` (el registro que una máquina lee) · `../secrets/README.md` (las guías de
acceso) · `plans/PLAN-multicuentas.md` (por qué existe el sistema) ·
`../blocks/archive/multicuentas_2026-08/docs/incidente-fuga-credencial.md` (el incidente que forzó
la mudanza) · `../../PROJECT-RULES.md` §4.
