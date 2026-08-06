# PROJECT RULES · For3s OS

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-02 · **Owner:** brian
**Level:** 🏢 PROJECT — inherits from `Mente/base-rules.md` (🌐 universal)
**Verified by:** `Mente/bin/check-blocks` · **Model:** `Mente/rules/rule-inheritance.md`
---

## Purpose

The rules that apply **while working on For3s OS** — and nowhere else. They exist as a separate file
because of a measured problem: they used to live in `CLAUDE.md`, which meant every block and every
future project inherited them.

> **Brian, 2026-07-29:** *"el sistema NO SOLO LO VOY A OCUPAR PARA DEMO, y entonces el resto de lo
> que haga va a estar contagiado con esas reglas."*

**If Jazz clones Mente OS for design work, she must NOT inherit "never read ~/5M-incubathon" —**
a rule about a project that is not hers. That is the contamination this file prevents.

---

## 0 · THE THREE LEVELS — where this file sits

```
🌐 UNIVERSAL   Mente/base-rules.md        any project, any block, from the first response
      │ inherits (may ADD or TIGHTEN — never LOOSEN)
      ▼
🏢 PROJECT     PROJECT-RULES.md  ← YOU ARE HERE
      │ inherits
      ▼
📦 BLOCK       Mente/blocks/active/<name>/BLOCK.md §B
```

⛔ **A lower level can never grant itself what a higher level forbids.** Exceptions are Brian's
only, and become a **new rule at the parent's level** with its own ADR.

---

## 1 · 🔒 WHICH RULES ARE LOCKS, AND WHICH ARE DISCIPLINE

> **Measured 2026-08-02.** §3 claims *"the gate is a technical lock, not a promise"* — true of §2
> and §3. It is **not** true of every rule here, and presenting them all the same way makes
> doctrine read as enforcement.
>
> ## A declared limit is engineering. A hidden one is debt.

| Rule | Enforced by | Level |
|---|---|---|
| §2 `marca-personal/Mente` out of scope | 4 `deny` rules, both settings files | 🔒 **lock** |
| §3 the NavigoX gate | 6 `deny` rules, both settings files | 🔒 **lock** |
| §5 `secrets/` 700 · files 600 | `bin/test-f0-f6` §F0 measures the real modes | 🔒 **lock** |
| §4 server-first (`git push`) | `ask` on all three push forms — Brian confirms each one | 🟡 **prompt** |
| §5 Master KEK offline | ⛔ **nothing can verify it** — it lives off this machine | 📖 **discipline** |
| §5 server password rotation | deliberately deferred by Brian, with its three trigger conditions | 📖 **discipline** |
| §6 reading · §7 F-method | conduct — not mechanically verifiable by design | 📖 **discipline** |

⭐ **Why the distinction matters:** this project's own measured law is that a rule in code is
obeyed 100% and a rule in a document 40-60%. **The 📖 rows are the 40-60%.** They are not weaker
rules — they are rules whose compliance nobody can prove, and that is worth knowing before
trusting them.

---

## 2 · SCOPE — what this project is, and is not

| | |
|---|---|
| **This project IS** | For3s OS. Its documentary brain is `Mente/` = **"Mente OS"** |
| **Architectural source of truth** | `Mente/Cerebro/For3s_OS_Grafo_Maestro.md` |
| ⛔ **NOT this project** | `marca-personal/Mente/` — public site, separate project. **Technically locked** by a `deny` rule |
| ⛔ **NOT this project** | For3s QA — separate working branch, never mixed in |
| ⚠️ **Ask first** | any modification outside `for3s-inter/` |

> `marca-personal/` (the site) **is** in scope — the demo lives there. `marca-personal/Mente/` is
> not. The distinction is the `/Mente/` suffix, and it is enforced by the harness, not by trust.

---

## 3 · 🌉 THE GATE — other Mente OS instances

Other projects have their own Mente OS (**NavigoX** in `~/5M-incubathon/`). This one **points at
them but does not integrate them** — integrating burns tokens with no request behind it.

| | |
|---|---|
| ⛔ **Never read** `~/5M-incubathon/` unless Brian asks with the access phrase | not "for context", not "just in case" |
| **Open** | Brian writes `acceder mente <project>` → confirm the WHY → **read-only + report** |
| **Close** | `cerrar mente <project>` **or** auto-close when the task ends, whichever comes first |
| **Enforcement** | 🔒 `deny` on Read/Edit/Write in **both** `.claude/settings.json` and `settings.local.json` |

⭐ **The gate is a technical lock, not a promise.** It was doctrine on 2026-07-21 and got violated
6 times in one session. Now the harness refuses. **Never propose lifting a deny for convenience.**

Registry and full rules: `Mente/bridges/Puentes_Mente_OS.md`.

---

## 4 · 📏 SERVER-FIRST — the deploy rule

> **Develop and test on the SERVER. Push to GitHub only on an explicit order.**
> Flow: `server → local → GitHub`.

⚠️ **Why this is project-level and not universal:** it only matters in repos with auto-deploy.
**Vercel deploys from `main`, so any push to `main` is a production deploy.**

| Repo | Role |
|---|---|
| `github.com/fruterito101/for3s` | the repo of truth (AGPL, GPG-signed by Brian) |
| server `~/for3s-os` | the workshop |
| `marca-personal` | the site — **pushing to `main` publishes** |

---

## 5 · 🔒 IDENTITY AND SECURITY

| | |
|---|---|
| Founder | **Brian López** — never "Aguilar". `ema@frutero.club` |
| Master KEK | **always offline.** Never on the server |
| Plaintext secrets | **Brian never sees them** |
| Audit trail | immutable — no `UPDATE`, no `DELETE` |
| `Mente/secrets/` | 700, files 600, gitignored, **no `!README.md` exception** |
| Server password | ⚠️ **rotation deliberately deferred by Brian.** Mitigant: the server is Tailscale-only. **Must rotate before**: opening the Tailscale Funnel · granting tailnet access to anyone · publishing any repo carrying a `.jsonl` or `settings.local.json` |

---

## 6 · 📖 READING — what to load and what not to

| | |
|---|---|
| **First, always** | `Mente/memory/RETOMAR.md` (~5 KB) — the cold-start brief. **~90% of the time it is enough** |
| ⛔ **Do NOT read** | `Mente/memory/Estado_Sesion_Continuidad.md` (200 KB) unless a pointer in RETOMAR sends you there explicitly |
| **Why** | reading it "just in case" burns tokens for nothing — measured by Brian, 2026-06-09 |
| **Open block** | load Tier 1 (§A-E) of `Mente/blocks/active/*/BLOCK.md`. If §A-E do not suffice → **say so, do not infer** |

---

## 7 · 🏗️ HOW WORK IS BUILT

Every **large milestone** uses the F-phase method: `Mente/rules/ESTANDAR_Metodo_Fases_F.md`.

```
explain → approve → build          (never skip the middle step)
investigate the ground → build defensively → §5-BIS battery → signed commit → server first
```

⭐ **Curiosity that hunts bugs:** actively look for your own latent bug. Never call something good
without testing it, nor bad without investigating it.

---

## 8 · WHAT THIS FILE IS NOT

⛔ **Universal conduct does not live here.** "Do not state — report the measurement", "the AI does
not invent criterion", "no `/clear` without registering" hold in **any** project → `Mente/base-rules.md`.

⛔ **Block limits do not live here.** "Do not touch the agent's repo" belongs to one block → its
`BLOCK.md` §B.

**The test:** *would this rule still hold in a different project?*
**Yes → universal.** **No, but it holds with no block open → here.** **Only while this work is open → the block.**

---

Related: `Mente/base-rules.md` (🌐 universal) · `Mente/rules/rule-inheritance.md` (the model) ·
`CLAUDE.md` (the router that loads this) · `Mente/bridges/Puentes_Mente_OS.md` (the gate).
