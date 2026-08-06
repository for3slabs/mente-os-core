# WORKSPACE · the cheat sheet an agent needs before it starts
**Status:** current · **Type:** entry-point · **Updated:** 2026-08-05 · **Owner:** brian
**Scope:** ⚠️ INSTANCE document, not the engine — what is true of *this* machine and *these* repos.
A clone regenerates it; it is not copied.
---

## Purpose

Everything a sub-agent would otherwise waste minutes discovering on its own: which repo is which,
what is a sibling and what is off-limits, where the credentials live (**never their values**), and
which command answers which question.

> **Why this file exists** (`rules/rule-shipping-flow.md` §7, layer 2 of six): the setup layer that
> Mente OS did **not** have. Measured 2026-08-05 — this information existed, scattered across
> `mente.config.yml`, `Mente/secrets/` and a memory. Scattered facts are re-derived every session,
> and re-derivation is where a wrong assumption enters.

> ## ⛔ THIS FILE NEVER CARRIES A VALUE
> No passwords, no tokens, no keys, no connection strings. **It says WHERE, never WHAT.**
> A secret written here would land in every transcript that reads it, and a leaked secret is
> **ROTATED, not deleted** (`rules/rule-config-hygiene.md` §1.1). The `.jsonl` files are not editable.

---

## 1 · THE REPOS — which is which

| Path | What it is | Rule that governs it |
|---|---|---|
| `~/for3s/` | ⭐ **THE repo — el `.git` vive aquí desde 2026-08-05.** Publica `.claude/` + `CLAUDE.md` + `PROJECT-RULES.md` + `Mente/` | `CLAUDE.md` (the router) |
| `~/for3s/Mente/` | 🧠 the engine + this instance. **Se publica ENTERA**, ya no está en `.gitignore` | `PROJECT-RULES.md` |
| `~/for3s/.git-for3s-absorbido/` | 📦 **historia, no basura.** Los 12 commits del repo `for3s` que existía antes de subir el `.git` un nivel. Ignorado; **976 KB** | ver el aviso de abajo |
| `~/for3s/marca-personal/` | 🖥️ **the site + the demo.** Declared `sibling` in `mente.config.yml` | block `demo` §B |
| `~/for3s/for3s-inter/` | separate scope — ask before modifying | `feedback_for3s_inter_scope` |
| `~/for3s/For3s-OS/` | the product, not the engine | `mente.config.yml` `outside:` |

> 📦 **`.git-for3s-absorbido/` — por qué se conserva y no se borra (2026-08-05).**
> Al subir el `.git` de `Mente/` a la raíz, el repositorio `for3s` que vivía aquí quedó absorbido.
> Sus **12 commits NO existen en el repo actual** (verificado con `git cat-file -e`): son historia
> única. El **contenido** sí sobrevivió — `CLAUDE.md` y `PROJECT-RULES.md` son idénticos byte a
> byte a los de hoy — así que lo que se perdería al borrarlo **no son archivos, es el PORQUÉ**:
> los mensajes explican por qué nació la categoría `ask`, qué bypass del `deny` se cerró
> (`python3`/`perl`/`xargs` leían lo prohibido) y qué almacenes de credenciales no estaban
> protegidos. Ese razonamiento no está en ningún otro sitio.
>
> **Cómo leerlo:** `git --git-dir=.git-for3s-absorbido log --oneline`
>
> ⛔ **No se borra** — `principles/expertise/doc-structure.md`: nunca borrar historia para que algo quede limpio.
> Si algún día estorba, primero se vuelcan los 12 mensajes a un documento de `Mente/`.

**Published engine:** `github.com/fruterito101/mente-os` (MIT, engine only — no `memory/`,
`work/`, `vision/`, `Cerebro/`).
**Product repo of record:** `for3slabs/for3s-os`. **Site repo:** `ElBrAyAn1967/For3s`.

## 2 · ⛔ GATED — never read without permission

Declared in `mente.config.yml` `gates:` — that file is the source, this table is the reminder:

| Path | Why |
|---|---|
| `~/5M-incubathon/` | NavigoX has its **own** Mente OS. Needs `acceder mente navigox` + a reason |
| `~/for3s/marca-personal/Mente/` | a different project's Mente. Not this one |

Rules: `bridges/Puentes_Mente_OS.md`. The reason is **consumption**, not secrecy.

## 3 · WHERE THE CREDENTIALS LIVE — pointers only

| What | Where it lives | ⛔ |
|---|---|---|
| Server access (host, user, password) | `Mente/secrets/Conectar_Servidor_For3s.md` | 🔴 **11 `deny` rules** block reading it — Read, `cat`, `head`, `tail`, `less`, `more`, `strings`, `xxd`, `od`, `base64`, `cp` |
| Demo secrets (`DEMO_ENC_KEY`) | `Mente/secrets/Secretos_Demo_Sitio.md` | same |
| Harness OAuth | `~/.claude.json` | `deny` on 13 channels. ⚠️ **`deny` is not a sandbox** — it matches the command TEXT, so `"$(…)"` slips past. Known and written: `memory/PENDIENTES.md` §🔐 |
| Site env vars | Vercel dashboard | §5 below — an env var holding content is a finding |

> 🔑 **2026-08-05 · EL `deny` DE LECTURA SE CONVIRTIÓ EN UNA CREDENCIAL ATADA AL CACHÉ.**
> `bin/secrets-lease` emite el permiso **cuando el contexto se carga** (SessionStart + PostCompact)
> y muere cuando vuelve a cargarse. `hooks/gate-secrets.py` decide: **leer** con permiso vivo pasa
> y queda anotado; **escribir o borrar** pregunta SIEMPRE, tenga permiso o no; y ⛔ **copiar, mover
> o empaquetar sigue en `deny`** — el permiso abre CONSULTAR, nunca EXTRAER.
> Toda operación va a `secrets/.access-log.md` (nombre del archivo y motivo, **jamás el valor**).
> 🔴 Fail-closed probado: si el emisor no responde, **pregunta**, no concede.
>
> ⚠️ Lo anterior sigue aplicando a lo que NO se movió:
> 🔴 **The `deny` on `secrets/` is not an obstacle to route around.** `PROJECT-RULES.md` §3 forbids
> proposing that it be lifted for convenience. If a task needs a value from there, **Brian supplies
> it** — through the environment, never pasted into the conversation.

## 4 · THE SERVER

Reachable over Tailscale; host, user and password are in the secrets file above (§3), never here.
Five For3s instances run on one machine, isolated by `docker compose -p for3s-<name>`, sharing only
the machine, the image and **one** Claude subscription seat. Manager: `for3s
listar|agregar|entrar|encender|apagar|borrar`. Specs and the IPv6→Telegram fix: memory
`reference_servidor_for3s`.

> 📏 **Server-first** (`PROJECT-RULES.md` §4): develop and test on the server. **Push to GitHub only
> on an explicit order** — all three push forms are `ask`.
> ⚠️ **Vercel deploys `marca-personal` from `main`: any push to main is a production deploy.**

## 5 · ENVIRONMENT VARIABLES — the rule, not the list

The values are not listed here on purpose (§ the banner). What governs them is criterion:

> **An env var is for WIRING** (connection strings, deploy identity) — **never for CONTENT.**
> A variable holding anything with an owner, anything that changes without deploying, a fixed
> list, a threshold, or sensitive user data is a **finding**, not a config choice.
> → `principles/expertise/dev-database.md` §2.2, Brian's five categories.

Precedent: 3 bridge env vars were retired from Vercel on 2026-07-26 and the demo stayed alive
(HTTP 200). ⚠️ The harness **rewrites `settings.local.json` on every approval** — pruning the allow
list without changing the approval habit is work that undoes itself.

## 6 · WHICH COMMAND ANSWERS WHICH QUESTION

Full map: **`CAPABILITIES.md`**. The ones used most:

| Question | Command |
|---|---|
| is the whole system still sound? | `bin/test-f0-f6` — only `failed: 0` matters |
| product or MVP? | `bin/grade-block <block>` (add `--root <repo>` for a sibling) |
| any live number (battery, holes, citations) | 🤖 `docs/METRICS.md` — regenerate with `bin/generate-metrics` |
| do the blocks hold their contract? | `bin/check-blocks` |
| does every citation resolve? | `bin/check-links` |
| is the tree the declared one? | `bin/check-structure` (reads `Maestro/piezas.tsv`) |
| safe to `/clear`? | `bin/check-clear-ready` — refuses if something would be lost |
| set up a new instance | `bin/init` |

⚠️ `bin/generate-metrics` runs the whole battery (~2 min) and takes its lock. Launching it while
another run is live publishes the OLD numbers with no warning.

## 7 · WHAT RUNS BY ITSELF

4 hooks, portable via `$CLAUDE_PROJECT_DIR`: session start (health, structure, drifting blocks —
**speaks only in 🔴**) · pre-edit standards injection · `gate-critical` (DB with no rollback,
insufficient close) · pre-commit (**blocks** a block that violates its contract).

> ⛔ `Edit`/`Write` deny rules do **not** cover `Bash` — a python one-liner rewrote a file under
> `bin/` that the Edit rule protected. Same back door as `rule-config-hygiene` §1.5.

---

Related: `mente.config.yml` (the machine-readable source for gates, siblings and paths) ·
`CAPABILITIES.md` (what the agent can do) · `CLAUDE.md` (the router) · `PROJECT-RULES.md` ·
`rules/rule-shipping-flow.md` §7 (why this layer exists) · `memory/PENDIENTES.md` §🔐.
