# RULE · INHERITANCE

**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** found in F3 · **Supersedes the flat model** where every rule lived in `CLAUDE.md`

---

## Purpose

Rules live at **three levels** and inherit downward, like classes in OOP. This exists because the
flat model contaminated every piece of work with rules that belonged to one project.

---

## 0 · WHY THIS EXISTS

> **Brian, 2026-07-29:** *"el sistema NO SOLO LO VOY A OCUPAR PARA DEMO, y entonces el resto de lo
> que haga va a estar contagiado con esas reglas… existirían 3 jerarquías: reglas universales para
> todo el sistema, reglas por proyecto y reglas por bloque, como POO con sistemas de herencia."*

**Measured 2026-07-29 — of the 8 non-negotiables in `base-rules.md`, only 5 were universal:**

| Rule | Real level |
|---|---|
| Explain → approve → build · AI invents no criterion · report the measurement · secrets are referenced · scope is declared | 🌐 **UNIVERSAL** |
| **Never read another Mente OS without the gate** | 🏢 **project** — only matters near NavigoX |
| **Server-first** | 🏢 **project** — only matters in repos with auto-deploy |
| No `/clear` without registering | 🌐 universal |

And `CLAUDE.md` was worse: `NO tocar marca-personal/Mente` · `NO mezclar con For3s QA` ·
`NO leer ~/5M-incubathon` — **three project-specific rules injected into every session.**

> **The consequence:** if Jazz clones Mente OS for design work, she inherits *"never read
> ~/5M-incubathon"* — a rule about a project that is not hers. **Contamination, exactly as Brian
> named it.**

---

## 1 · THE THREE LEVELS

```
🌐 UNIVERSAL          Mente/base-rules.md
   conduct that holds for any work, any project, any block
   applies BEFORE any block exists — from the first response of a session
        │
        │ inherits
        ▼
🏢 PROJECT            <project>/PROJECT-RULES.md
   "this is For3s OS: QA is a separate branch, NavigoX has a gate"
   applies while working in this project
        │
        │ inherits
        ▼
📦 BLOCK              blocks/active/<name>/BLOCK.md §B
   "do not touch the agent's repo"
   applies only while this block is open
```

### The test that assigns a level

> **Would this rule still hold if the level below did not exist?**

| Answer | Level |
|---|---|
| Holds with no block open | 🏢 project or 🌐 universal |
| Holds in **any** project, even one that does not exist yet | 🌐 **universal** |
| Only makes sense while this specific work is open | 📦 **block** |

---

## 2 · ⭐ THE INHERITANCE RULE — restrict only, never relax

> ## A lower level may only ADD or TIGHTEN a rule. It can never LOOSEN one.

This is the one place the OOP analogy breaks on purpose: **there is no override that widens
permissions.** A subclass cannot grant itself what the parent forbade.

| Operation | Allowed | Example |
|---|---|---|
| **ADD** a rule the parent does not have | ✅ | the block forbids touching the agent's repo |
| **TIGHTEN** an inherited rule | ✅ | universal says *"push only on explicit order"* → the demo block adds *"and any push to main is a production deploy"* |
| **LOOSEN** an inherited rule | ⛔ **never** | a block cannot grant itself access to `marca-personal/Mente` |
| **Grant an exception** | ⛔ only Brian, and it becomes a **new rule at the parent's level** with its own ADR |

### Why loosening is banned — three real cases

| Case | What it shows |
|---|---|
| The demo block adding *"any push to main deploys"* | ✅ **tightening** — the rule got stricter, not weaker |
| The NavigoX gate refusing **even Brian** before checking permissions | ⛔ some rules protect cost, and cost applies to whoever holds authority |
| `marca-personal/Mente` locked by a technical `deny` | ⛔ **the harness enforces it** — a block declaring otherwise would just be lying on paper |

> ⭐ **The reason:** on 2026-07-21 the scope rule existed in `CLAUDE.md` and was violated 6 times.
> If a block could have declared itself exempt, the rule would protect nothing.

---

## 3 · WHEN BLOCKS COMMUNICATE — the rules ADD UP

> **Brian:** *"cuando se comunican dos o más bloques comparten reglas y se suman, solo para el caso
> que se quiera modificar o estar trabajando con muchos bloques y necesites las reglas para que
> sepas qué hacer y qué no hacer."*

**The effective rule set while working =**

```
universal  +  project  +  (block A)  +  (block B, if declared in §C)
```

| Situation | Effective set |
|---|---|
| One block open | universal + project + that block |
| Block A **declares** B in §C `DEPENDS ON` | + B's rules |
| Two blocks with **no declared connection** | ⛔ their rules do NOT mix — isolation (`rule-isolation.md`) |
| A conflict between two blocks' rules | 🔴 **the stricter one wins** — never the more permissive |

> ⚠️ **Rules add up only through a DECLARED connection.** Two unrelated blocks stay isolated, or the
> gate that protects consumption stops meaning anything.

---

## 4 · WHERE EACH LEVEL LIVES

| Level | File | Status |
|---|---|---|
| 🌐 Universal | `base-rules.md` | ✅ exists — **needs the 3 project rules removed** |
| 🏢 Project | `PROJECT-RULES.md` per project | 🔴 **does not exist yet** |
| 📦 Block | `BLOCK.md` §B | ✅ exists |

**`CLAUDE.md` becomes a router, not a rule store:** it points at the universal file and at the
project file for the current directory. **A rule written directly in `CLAUDE.md` has no declared
level — that is the bug this rule fixes.**

---

## 5 · WHAT `bin/check-blocks` VERIFIES

```
🔴 INHERITANCE
   · a block repeating a rule that exists at project or universal level
     (repetition diverges silently — the decisions table did exactly that: 75 rows vs 37)
   · a block that LOOSENS an inherited rule
   · a rule with no declared level

🟡 INHERITANCE
   · a project rule that is actually universal (holds in any project)
   · a universal rule that names a specific project → it is not universal
```

---

## 6 · MIGRATION

**Not done yet.** Registered in `memory/PENDIENTES.md`:

1. Split `base-rules.md`: keep the 5 universal, move 3 to `PROJECT-RULES.md`
2. Create `PROJECT-RULES.md` for For3s OS with what leaves `CLAUDE.md`
3. Turn `CLAUDE.md` into a router
4. Re-audit the demo block: it already separates `OUT` from inherited rules (F3)

> ⚠️ **Order matters:** create the project file **before** removing anything from `CLAUDE.md`, or a
> session in between loses the rule entirely.

---

Related: `base-rules.md` · `contract-block.md` §B (the two levels in a block) ·
`rule-isolation.md` (why rules do not mix without a declared connection) · ADR-002 (portability).
