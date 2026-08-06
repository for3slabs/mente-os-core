# SHIPPING FLOW · how a ticket becomes a merged PR
**Status:** current · **Type:** rule · **Updated:** 2026-08-05 · **Owner:** brian
**Language:** US English · **Applies to:** EVERY discipline — backend · frontend · database · docs
**Declared by:** a block's §D `Required standards` · injected by `hooks/pre-edit-standards.py`
**Source:** `cracked-dev` (MIT), imported 2026-08-05 → `blocks/archive/expertise-programacion_2026-08`
---

## Purpose

The workflow that turns a ticket into a reviewable PR: **branch → verify → PR → do not merge.**

> ⭐ **Why this is a RULE and not part of an expertise file** (Brian, 2026-08-05):
> *"no solo los PR deben ir en backend, porque va a haber PR de frontend, de base de datos."*
>
> **Measured, and it is what makes this a real defect:** `hooks/pre-edit-standards.py` injects
> **only what the block declares in its §D**. A frontend block declares `principles/expertise/dev-frontend.md`, so if
> the PR flow lived in `principles/expertise/dev-backend.md` it would **never reach that block** — the agent shipping a
> frontend ticket would not know how to open the PR. Same for a database block.
>
> The flow is **transversal**: it does not change with the discipline. What changes per discipline
> is *what gets verified*, and that stays in each `expertise/*.md`.

> 🔴 **This is imported methodology, NOT Brian's criterion** (ADR-003). It is usable today, but it
> is not his judgement. His criterion lives in `principles/expertise/*` §2-§4.

---

## 1 · THE EXECUTION LOOP — every ticket, no exceptions

```
PRE-FLIGHT → BRANCH → IMPLEMENT → VERIFY → COMMIT → UPDATE CONTEXT → PUSH + PR → ⛔ STOP
```

**Pre-flight, before writing ANY code:** read the project's `CLAUDE.md` (phase status, architecture
rules, known issues, last commit log) · read the spec the ticket references · check what just
shipped and what broke · check known issues so a past mistake is not repeated · read the stack
rules for the frameworks involved.

> 🏢 **Mente OS equivalent, and it is stricter:** the pre-flight is not a habit here, it is a
> **hook** — `hooks/pre-edit-standards.py` injects the owning block's §D before an edit, and
> `hooks/gate-critical.py` blocks outright. A human can forget to read; the gate cannot.

**Branch:** `git checkout <base> && git pull && git checkout -b <type>/<scope>-<ticket>`
Types: `feat` · `fix` · `refactor` · `docs` · `test` · `chore`.

**Implement:** touch only files in scope · follow the patterns of nearby files · reference the spec
section in comments where non-obvious · **if the spec is unclear, flag it — never guess.**

**Verify — run every check, no "it probably works".** Which checks apply **depends on the
discipline** and is declared by the block's §D expertise file. Typically: type-check · lint ·
production build · tests.
**If ANY check fails, fix it before proceeding. Never commit broken code.**

> 🏢 **Mente OS equivalent, stricter:** `bin/test-f0-f6` — the only thing that matters is
> `failed: 0`, plus the §5-BIS battery (`principles/owner-3-validation.md` §4) which additionally
> demands a real startup, `/salud` at 0 FAIL, and **affirmative verification**: *"recovered X"*,
> never *"seems fine"*.

**Commit:** atomic, one ticket = one commit (or a small focused series), with the spec reference in
the body.

**Update the context file before pushing — mandatory:** last commit log (hash, branch, what, status)
· patterns that worked · known issues hit, so the next agent does not repeat them.

**Push + PR:** open the PR against the base branch using the checklist in §3.

> ## ⛔ DO NOT MERGE. Creating the PR is the end of the agent's job. **Merging is a human decision.**

**Post-merge, only when told to merge:** verify the deployment succeeded · verify backend changes
are live · smoke-test the critical paths · delete the branch.

---

## 2 · 🔴 THE 8 ANTI-PATTERNS — never, in any ticket, in any discipline

| # | Anti-pattern | Status in Mente OS |
|---|---|---|
| 1 | Pushing straight to `main` or the base branch | 🏢 already law: server-first, push only on explicit order. ⚠️ Vercel deploys from `main` — a push to main IS a production deploy |
| 2 | Skipping the build (*"tsc passed, it's fine"*) | 🏢 harder: `failed: 0` on the full battery |
| 3 | Touching files outside the ticket's scope | 🏢 already law: block §B Scope + `rules/rule-isolation.md` |
| 4 | Guessing when the spec is unclear | 🏢 already law: *never invent criterion* (ADR-003) — ask or flag |
| 5 | Leaving the context file un-updated | 🏢 already law: `rules/rule-session-close.md` + `bin/check-clear-ready` refuses |
| 6 | Force-pushing shared branches | 🆕 **new here** |
| 7 | Committing secrets, API keys or `.env` files | 🏢 harder: 212 `deny` rules + gitleaks in CI |
| 8 | A PR that depends on another un-merged PR (unless explicitly stacked) | 🆕 **new here** |

---

## 3 · THE PR CHECKLIST — what a PR body must carry

**What** it does · **why** (ticket or spec section) · **spec reference** · **changes** ·
**notes for the reviewer** (trade-offs, open questions, follow-ups), and the verification list:

- [ ] Type-check passes · [ ] Lint passes · [ ] Production build passes · [ ] Tests pass
- [ ] **Discipline-specific checks pass** — see the block's §D expertise file
- [ ] Context file updated (commit log, known issues)
- [ ] **No secrets committed**
- [ ] **Only in-scope files modified**

---

## 4 · BRANCH AND COMMIT REFERENCE

```
main (production)
  └── dev (staging / preview)
        └── feat/phase-1-auth      one branch per ticket
        └── fix/phase-1-redirect
```

All work on feature branches from the base · every branch targets the base via PR · base → main is
manual, when ready for production · **never push directly to `dev` or `main`.**

Commit shape: `type(scope): short description`, then the detail lines and the spec reference.
Types: `feat` `fix` `docs` `refactor` `test` `chore`. Scope: phase, feature area, or module.

---

## 5 · ORCHESTRATION — spawning sub-agents

**⛔ Maximum 2 concurrent sub-agents on one repo.** Beyond that you get merge conflicts, race
conditions on the shared context file, and chaos.

- **Never** assign two agents to tickets that touch the same files.
- **Stagger launches** — let the first commit before spawning the second on a dependent ticket.
- If one needs the other's output, **serialize them.**
- Track active streams in a table: stream · ticket · branch · agent · status.

**The spawn prompt is the highest-leverage artifact. A vague spawn gives vague results.** Every one
must carry: exact file paths to read and modify · exact branch name and its base · exact
verification commands · **scope boundaries** (*"do NOT modify files outside X"*) · read order ·
and what NOT to do, taken from known past failures.

> ## ⛔ WHAT WAS REFUSED, AND WHY — not omitted
>
> `cracked-dev` recommends `--dangerously-skip-permissions` (and `bypassPermissions`) so spawned
> agents run without confirmation prompts. **It does not come in.** It is the exact inverse of this
> project's 212 `deny` rules and 3 gates, and `PROJECT-RULES.md` §3 forbids proposing that a deny be
> lifted for convenience. Recorded rather than silently dropped, so a future reader knows it was
> **evaluated and refused**, not overlooked.

**Progress reporting:** report on completion and on blockers; stay quiet while working. State the
ticket, the PR, the branch, the verification results, the file count, and what is next.

**Rollback when something breaks after merging:** revert the PR (creates a revert commit) · additive
DB changes may stay, destructive ones need their migration reverted · redeploy if backend functions
were touched · **never force-push the base branch** · document the failure so it becomes a one-line
warning for the next agent.

---

## 6 · WHAT MAKES A SPEC EXECUTABLE

> **The quality of the spec determines the quality of the output. Directly.**
> ⛔ *"add a scoring system"* → ✅ *"create `src/scoring/record.ts` exporting
> `recordInteraction(platform, handle, action)` that computes a spam signal over the last 24h,
> updates the composite via `calculateComposite()`, and returns `{ score, signals }"*

A spec must carry exact schema and types · function signatures · data flow · edge cases · and what
to do when things go wrong. **If a sub-agent has to ask a question, the spec failed.**

Ticket shape: branch · spec section · scope · files touched · verify commands · depends on.
A ticket must be completable by one agent in one session, verifiable, and scoped to specific files.

> 🏢 **Mente OS equivalent:** Epic→Phase→Ticket maps onto Método F (phases) + block §F sub-blocks.
> The dependency graph is not drawn by hand here — **it is measured** (`rules/rule-lanes.md`),
> which is the stricter version. What Mente OS did NOT have is the ticket→branch→PR mapping above.

---

## 7 · PROJECT SETUP — the context that makes an agent effective

> **Most agents fail not because they are dumb, but because the project context is missing.**

Six layers, to exist before the first sub-agent is ever spawned:

| # | Layer | What it carries |
|---|---|---|
| 1 | **Context file** (`CLAUDE.md`) | phase status · architecture rules (hard *"do NOT do X"*) · known issues with ⚠️ · exact commands · doc index · last commit log |
| 2 | **Workspace cheat sheet** | ✅ **`docs/WORKSPACE.md`** (created 2026-08-05) — repo paths · what is gated · **where** credentials live (never their values) · which command answers which question |
| 3 | **Stack rules files** | framework patterns that stop code that *looks* right but does not work with this stack. Practical patterns, not philosophy |
| 4 | **Spec documents** | §6 — detailed enough that no question is needed |
| 5 | **The spawn prompt** | §5 — the single most impactful artifact |
| 6 | **Institutional memory** | every failure written down: what went wrong, why, what to do instead |

> **The compounding pattern:** agent fails → the failure is documented → the next agent reads it →
> it does not fail the same way. *"A catastrophic multi-commit revert spiral becomes a one-line
> warning that saves hours."* This is what makes the 10th sub-agent far better than the 1st.

> 🏢 **Mente OS equivalent — and here it is markedly stricter.** Layer 1 is `CLAUDE.md` **as a
> router with three inheriting rule levels**, not a status file. Layer 3 is the `principles/expertise/*`
> tree. Layer 6 is three mechanisms, not one: block §H friction · `memory/` · `rules/case-*.md`.
> ✅ **Layer 2 was the gap this rule exposed, and it is now closed** (2026-08-05):
> `docs/WORKSPACE.md`. It **points**, never duplicates — `mente.config.yml` stays the
> machine-readable source for gates and siblings, and the cheat sheet says WHERE a credential
> lives, never its value.

---

Related: `principles/expertise/dev-backend.md` §4-BIS (backend-specific failure patterns) ·
`principles/expertise/dev-database.md` §4-BIS · `principles/expertise/dev-frontend.md` §4-BIS ·
`rules/contract-block.md` (§D declares this file) · `rules/rule-isolation.md` ·
`principles/owner-3-validation.md` §4 (the §5-BIS battery) · `blocks/archive/expertise-programacion_2026-08`.
