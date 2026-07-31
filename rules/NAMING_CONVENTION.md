# 📐 NAMING CONVENTION — Mente OS v2
**Status:** current · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
Legacy files are renamed **on demand** (when touched), never in bulk — see §7.
**Language — decided by Brian 2026-07-27:** **US English** for names *and* for every text the AI
reads as an instruction. Spanish stays for Brian's own thinking.
| What | Language | Why |
|---|---|---|
| **Anything the AI reads as an INSTRUCTION** | 🇺🇸 **US English** | the AI resolves it precisely; it is the language of every convention this standard builds on |
| **Brian's thinking** | 🇪🇸 Spanish | it is his criterion — another language strips the nuance |
**In English:** `CLAUDE.md` · `output-styles/` · `Mente/base-rules.md` · `principles/owner-*.md` ·
`principles/expertise/*` · `rules/*` · **`blocks/active/*/BLOCK.md`** · validator output · commits.
**In Spanish:** the vision · the plan · the comparative analyses · `memory/RETOMAR.md` ·
`Bitacora_Progreso` · `Registro_Conversaciones` · the memories · **and conversation with Brian**.
> **The cutting test:** *does the AI read this to KNOW WHAT TO DO, or does a human read it to
> UNDERSTAND WHAT HAPPENED?* First case → English. Second → Spanish.
### Canonical vocabulary — one term per concept, no mixing
| Spanish (v1) | 🇺🇸 **English (v2)** |
|---|---|
| bloque · sub-bloque | **block · sub-block** |
| encargado 0/1/2/3 | **owner-0 (voice) · owner-1 · owner-2 · owner-3** |
| carril | **lane** (`direct` · `task` · `full-block`) |
| límites qué SÍ / qué NO | **scope: IN / OUT** |
| roce | **friction** |
| veredicto de calidad | **quality verdict** |
| prueba de suficiencia | **sufficiency check** |
| punto de guardado | **checkpoint** |
| estándar obligatorio | **required standard** |
| puerta cerrada · recibo | **closed gate · approval receipt** |
> ⚠️ **Never mix** (`lane` in one place, `carril` in another) — that is exactly the anarchy v2 exists
> to remove.
**US spelling, not British:** `behavior` · `organize` · `analyze` · `center` · `license`.
**Dates:** ISO `2026-07-27` always — avoids MM/DD vs DD/MM ambiguity.
---

## 1 · THE THREE SOURCES THIS STANDARD FOLLOWS

| Source | What it dictates | Negotiable? |
|---|---|---|
| **Claude Code** | `CLAUDE.md` · `.claude/{agents,commands,hooks,skills,output-styles}` · `.claude/settings.json` | 🔴 **NO — reserved names** |
| **Repo conventions** (kriasoft · World Bank) | lowercase · short · **hyphens, not underscores** · `docs/` · `bin/` | 🟢 adopted |
| **ADR standard** | `ADR-NNN-decision-name.md` for decisions | 🟢 adopted |

> ⚠️ **Reserved names are not a style choice.** If `output-styles/` is renamed, the feature stops
> working. Same for `CLAUDE.md`, `skills/`, `hooks/`.

---

## 2 · TOP-LEVEL FOLDERS

| Current | **New** | Holds |
|---|---|---|
| `Alma/` | **`principles/`** | the WHY · the 3 owners (encargados) · expertise per discipline |
| `Cerebro/` | **`rules/`** | contracts · unit rules · cases · this standard |
| `Cuerpo/` | **`blocks/`** | ⭐ the work-unit system — the unit names the folder |
| `Doc/` | **`docs/`** | RETOMAR · index · states · pending · logbook |
| `Maestro/` | **`registry/`** | branch registry · pointers · permissions |
| `Tickets/` | **`bridges/`** | connections to other Mente OS instances |
| `secrets/` | **`secrets/`** | ⚠️ never in git |
| *(new)* | **`bin/`** | validators (executables) |

**Rules:** lowercase · single word when possible · English · **plural for containers**
(`blocks/`, `rules/`), **singular for a place** (`archive/`).

---

## 3 · INSIDE `blocks/`

```
blocks/
├── active/                  ← one file per block, several may exist
│   └── demo/
│       ├── BLOCK.md         ← the single file, sections A-K (≤150 lines)
│       ├── docs/            ← long detail lives here
│       └── cache/
├── blocked/
└── archive/                 ← closed blocks = consultable experience
    └── demo-2026-07/
        ├── SUMMARY.md
        └── connections.md
```

> No `_` prefixes. `active/` not `_activos/` — the underscore added nothing and broke the convention.

---

## 4 · FILE NAMES

### 4.1 · General form

**`lowercase-with-hyphens.md`** — never underscores, never CamelCase, never spaces.

### 4.2 · Type prefixes (use when the type matters for retrieval)

| Prefix | For | Example |
|---|---|---|
| `ADR-NNN-` | a decision, with sequence | `ADR-001-single-file-per-block.md` |
| `rule-` | a unit rule | `rule-fix-not-patch.md` |
| `case-` | a learning case | `case-dangerous-default.md` |
| `contract-` | a contract / template | `contract-block.md` |
| `spec-` | a specification | `spec-quality-verdict.md` |
| `analysis-` | external research | `analysis-internos-v1.md` |
| `plan-` | an implementation plan | `plan-v2-rollout.md` |
| *(none)* | anything else | `naming-convention.md` |

### 4.3 · ⭐ THE UPPERCASE EXCEPTION — entry points only

| File | Why uppercase |
|---|---|
| `CLAUDE.md` | 🔴 reserved by Claude Code |
| `README.md` | universal convention |
| `memory/RETOMAR.md` | the cold-start brief — **must be impossible to miss** |
| `BLOCK.md` | the block's single file — same reason |
| `SUMMARY.md` | a closed block's entry point |

> **The rule behind the exception:** UPPERCASE means *"this is a door, read it first"*.
> Everything else is lowercase. If everything shouts, nothing does.

### 4.4 · What NEVER goes in a file name

| ⛔ Never | Why |
|---|---|
| dates (`-2026-07-27`) | git already knows; a dated name is a fossil by design |
| versions (`-v2`, `-final`) | that is what git and the `status:` field are for |
| `_` underscores | breaks the convention; harder to read in URLs |
| accents or `ñ` | breaks tooling, URLs and greps |
| spaces | breaks shell scripts |
| `Mente_OS` in the name | everything here is Mente OS — redundant |

> ⚠️ **Exception for archived blocks:** `archive/demo-2026-07/` **does** carry the date, because the
> date is what distinguishes two archived runs of the same block. It is an identifier, not metadata.

---

## 5 · CLAUDE CODE PATHS — reserved, do not rename

```
CLAUDE.md                      ← project rules (auto-injected)
.claude/
├── settings.json              ← committed config
├── settings.local.json        ← local overrides (gitignored)
├── output-styles/<name>.md     ← ⭐ THE VOICE lives here
├── hooks/                     ← the gates that enforce
├── skills/<name>/SKILL.md
├── agents/<name>.md
└── commands/<name>.md
```

> ⭐ **Why `output-styles/` matters more than expected:** per Anthropic's documentation, output styles
> *"inject instructions into the system prompt"* and carry **the highest instruction-following weight
> of any customization method** — above `CLAUDE.md`. The voice (F0-4) is therefore the **strongest
> lever in the whole system**, not a cosmetic layer.

---

## 6 · WHY THE OLD NAMES FAIL

| Old name | Problem |
|---|---|
| `Alma/` `Cerebro/` `Cuerpo/` | poetic but **opaque** — nobody outside Brian's head knows what is inside. A new collaborator (or a new AI) has to open them to find out |
| `Doc/` | singular, capitalized, non-standard. Every repo on earth uses `docs/` |
| `Tickets/` | **lies** — it holds bridges to other Mente OS, not tickets. Frozen since 14-jun |
| `secrets/` | underscore + accent-adjacent + Spanish. `secrets/` is unambiguous |
| `Ronda_SEC4c_NonRoot_Perfil_Instancia.md` | 4 conventions in one name; unsearchable |

> **The test this standard must pass:** *someone who has never seen Mente OS opens the root folder
> and can guess what is in each directory.* Today it fails that test.

---

## 7 · MIGRATION — on demand, never in bulk

### 7.1 · Measured blast radius (2026-07-27)

| What points at the current folders | Count |
|---|---|
| **Unique paths cited inside documents** | **218** |
| Documents referencing `docs/` (as `Doc/`) | 62 |
| Documents referencing `blocks/` (as `Cuerpo/`) | 54 |
| **Memories citing paths** (outside git) | **~87** |
| Lines in `CLAUDE.md` carrying paths | **13** |
| `pointers.tsv` rows hardcoding `memory/RETOMAR.md` | 2 branches |

### 7.2 · 🔴 Why a bulk rename is dangerous

**A broken markdown link throws no error.** Nothing crashes — the link simply leads nowhere, and
nobody finds out until someone follows it weeks later.

Three systems break beyond the documents:

1. **`pointers.tsv`** hardcodes `memory/RETOMAR.md` → `maestro leer for3s` stops finding the index.
2. **Foresito reads the Maestro repo LIVE** via MCP, and was trained on 1,829 episodes carrying the
   old paths → the master agent would point at ghost routes.
3. **The ~87 memories live outside git** → if something breaks there, there is no history to revert.

### 7.3 · The rule — ✅ DECIDED BY BRIAN 2026-07-27

| Case | What happens |
|---|---|
| **New file** | born with this convention, **always** — starting F0-4 |
| **Legacy file being touched** | renamed **then**, with its pointers updated |
| **Legacy file nobody touches** | **left alone** — renaming what is never read is work without return |

### 7.4 · 🔴 THE BULK RENAME IS A PENDING ITEM — not part of F0-F8

> **Brian, 2026-07-27:** *"no renombramos a los 208, eso será un pendiente de v2."*

**Measured scope of that pending work:**

| | Count |
|---|---|
| Files across the 7 folders | **208** |
| With underscores | 185 |
| With uppercase | 194 |
| With a date baked into the name | 15 |
| **Alive** (touched since 2026-07-01) | **97** |
| **Fossils** (untouched since June) | **~97** |

**Half the tree is fossil.** Any bulk rename must account for that: renaming a fossil is work with no
return, and worse — **it makes something dead look current.** Today the modification date is the only
signal separating alive from fossil; a blanket rename destroys that signal.

**Recommended shape when the block is opened** (3 tranches, each verified before the next):

| Tranche | What | Count |
|---|---|---|
| 1 | the 7 folders + create `bin/` | 7 moves |
| 2 | the **alive** files | ~97 |
| 3 | fossils → `docs/archive/` **keeping their old names** | ~97 |

> ⭐ Tranche 3 is the elegant part: **fossils are not renamed, they are archived.** Still
> consultable, explicitly historical, and they stop polluting the new standard.

**Non-negotiable prerequisites for that block:**
1. **Clean commit first** — without it there is no clean rollback point. `git mv` only tracks renames
   when content stays stable.
2. **Update the pointers**, not just the names: `CLAUDE.md` (13 lines) · `pointers.tsv` · `memory/RETOMAR.md`
3. **Sweep the ~87 memories** (they live outside git — no history to revert).
4. **A validator** proving no pointer was orphaned. Without it this is a blind `sed` waiting to fail.

> **Why it is a BLOCK and not a task:** 218 pointer sites, 3 systems affected (docs, scripts,
> a trained agent), and **a broken markdown link throws no error** — it fails silently and surfaces
> weeks later. Full-block carril per §5 of the architecture.

---

## 8 · QUICK REFERENCE

```
✅  blocks/active/demo/BLOCK.md
✅  rules/rule-fix-not-patch.md
✅  rules/ADR-001-single-file-per-block.md
✅  principles/expertise/dev-database.md
✅  docs/RETOMAR.md
✅  bin/check-blocks

⛔  Cuerpo/_activos/DEMO/Bloque_Demo_v2.md
⛔  Cerebro/Regla_Fix_No_Parche_2026-07-27.md
⛔  Alma/expertise/base_datos.md
⛔  docs/analysis-internos-v1.md
```

---

Related: `Arquitectura_Mente_OS_v2_Bloques.md` §12 (folder structure) ·
`principles/owner-0-voice.md` (content stays Spanish) · [[project_mente_os_v2_bloques]].
