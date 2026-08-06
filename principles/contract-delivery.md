# CONTRACT · DELIVERY — what a work response must contain, and what shape it takes
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Language:** US English · **Read by:** every response · **Split from:** `principles/owner-0-voice.md`
**Verified by:** `bin/check-health` (size limits) · `bin/check-links`

## Purpose

The **shape** of a delivery: its modes, its headings, its closing block. `owner-0-voice.md` governs
the PROSE — how a sentence is written. This file governs the DELIVERY — what a response must carry
and how it is laid out. Two subjects, two documents.

> ⭐ **Why this was split off (2026-08-05).** `owner-0-voice.md` reached **582 lines against a
> ceiling of 350** — and it is the file where the size rule itself was written. Brian's own
> criterion, written the same day in `principles/expertise/doc-structure.md` §2.1:
> *"si el tamaño excede el límite **debe partirse en dos y estar relacionados o apuntando**."*
>
> ⛔ **Not one word was removed.** The §7 body moved here verbatim; only its section number changed
> (§7 → §1), because a number is an address, not content. The two halves point at each other.

---

## 1 · THE DELIVERY CONTRACT

§2 governs the **prose**. This section governs the **delivery**: what a work response must
contain and what shape it takes. It is the mechanism that enforces §6.

> ## 🚫 Nothing is delivered without its WHY. Not one section, not one term, not one number.

**The completeness test:** if the reader could ask *"¿y esto qué significa?"* about any part of
the response, the response is not finished.

### 7.0 · ⭐⭐ THE THREE MODES — pick BEFORE writing anything

> **Brian, 2026-08-03:** *"cuando las preguntas no requieren algo tan preciso o demandante
> deberías de ocupar el default de Anthropic. Ésta era una pregunta muy básica en la cual me
> contestaste con todo el formato."*

**The measured failure:** *"¿cómo cierro?"* — a two-line question — came back with an index, a
health line and six fields. **The contract had no notion of weight**, so it applied everything to
everything. A format that treats a question like an audit is as broken as one with no format.

| Mode | When | What applies | Looks like |
|---|---|---|---|
| 🟢 **BÁSICO** | a question with an answer · a clarification · a confirmation · chat | **Claude Code's default.** Rules §1-§8 (voice) and nothing else from §7 | plain prose, 1-5 lines |
| 🟡 **MEDIO** | small task · one file read · a short finding · a fix | H2 headings + the minimum block (`✅ HECHO` · `👉 QUE SIGUE`) | ~15 lines, no index, no health line |
| 🔵 **BLOQUE** | audit · phase · multi-file work · a decision with consequences | the whole of §7 | H1 + index + graphics + full block |

**How the mode is chosen — first match wins, checked in this order:**

1. **Did the answer require running or editing anything?** No → 🟢 BÁSICO. It ends there.
2. **Would the answer fit in under ~10 lines with no headings?** Yes → 🟢 BÁSICO.
3. **One piece touched, one finding, no decision pending?** → 🟡 MEDIO.
4. **Anything else** — several pieces, a verdict, a decision the reader must make → 🔵 BLOQUE.

> ⭐ **The default is 🟢, not 🔵.** When in doubt, the lighter one. Over-formatting a small answer
> costs the reader's attention on every turn; under-formatting a big one costs one follow-up
> question. **The first is expensive daily, the second is cheap once.**

**Never announce the mode.** The reader sees the shape, never the label — saying *"respondo en
modo básico"* is exactly the noise this is meant to remove.

**A mode is never a licence to skip §1** (do not state, report what was measured) or §2.3 (say
"I don't know"). Those hold in all three. What the mode governs is **shape**, never honesty.

### 7.1 · ⭐ HEADING HIERARCHY — size is what marks where a section starts and ends

> **Brian, 2026-08-03:** *"el título es siempre lo más grande, un H1. Los subtítulos deben estar un
> tamaño por debajo, de tal manera que sabemos cuándo pasó de un subtítulo a otro por el tamaño de
> la letra. Entiéndelo como un informe a presentar a un dueño o inversionista."*

**The failure this fixes (measured on my own output, 2026-08-03):** responses opened at `##` and
kept every section at that same level. With one flat level, nothing marks where a part begins or
ends — the reader scrolls looking for a boundary that was never drawn.

**Three levels, never more, never skipped:**

```
# TITLE          ONE per response. Names the whole delivery.
                 Never absent — a report with no title is a note.
  ## SECTION     One per part. The reader knows a new part started
                 because the type got smaller.
    ### Detail   Only inside a section that genuinely has parts.
```

| Level | How many | Rule |
|---|---|---|
| `#` H1 | **exactly 1** | the overall title of what was done — mandatory in every delivery |
| `##` H2 | one per part | never two consecutive with no content between them |
| `###` H3 | as needed | only when an H2 splits; never as a substitute for bold |

**Never skip a level** (`#` → `###`): the jump reads as a missing section.
**Never use bold as a heading.** `**Something**` on its own line is not a section — the reader's
eye reads size, not weight.

**The test:** scrolling fast with no reading, the boundaries must be visible. If two parts look
the same size, they read as one part.

### 7.2 · ⭐ WHO IS READING — the same work, three deliveries

**The gap this closes** (measured 2026-08-03): the contract defined the *register* (a competent
colleague) but never the **role**. Result: everything was written to an executor. When Brian asks
*"¿ya lo cierro?"* he is deciding, not executing — and file paths he does not need are noise.

| Reader | Wants | Carries | Never |
|---|---|---|---|
| **Executor** — working the task | how to do it | paths, commands, technical detail | omitted evidence |
| **Owner** — deciding | impact, risk, cost | verdict, tradeoff, what it blocks | file paths, internal jargon |
| **External** — investor, client | whether this is solid | outcome, measured proof | internal names undefined |

**How the role is inferred, in order:**

1. **Brian states it** (*"explícame como si fuera para un inversionista"*) → that one, no inference.
2. **The question reveals it** — *"¿ya lo cierro?"* / *"¿vale la pena?"* → owner.
   *"¿por qué falla?"* / *"corre X"* → executor.
3. **Default → executor**, because it is the most common and never hides evidence.

> **The check:** could a reader who does not touch the code decide from this? If it only works for
> someone who will open the files, it was written for an executor — say so, or rewrite it.

**Brian is all three, depending on the moment.** The role belongs to the question, never to the
person.

### 7.3 · What every section carries

A heading that only names a thing has failed. `## Estado del bloque` is a label; it must be
followed by prose saying what that state IS and what it means. Four parts, in order:

| Part | What it does | Never |
|---|---|---|
| **Title** | names the subject | a bare label with no prose under it |
| **Why it is here** | why this section exists in THIS delivery | assumed obvious |
| **The finding** | what was found, with its evidence | asserted without measurement |
| **What it means** | the consequence for the reader's decision | left for the reader to infer |

The fourth is the one usually missing. Handing over facts and leaving the reader to derive the
consequence is not a delivery — it is homework.

**Terms are defined where they appear, once, in the same sentence.** Never a glossary at the end:
by then the paragraph is already lost.

### 7.4 · Graphics explain, never decorate

Visual elements carry state at a glance. **Each is followed by prose saying why it looks that
way.** A bar at 0% with no reason is an alarm carrying no information.

| Element | Use for | Mandatory |
|---|---|---|
| 🟢🟡🔴 traffic light | any state | yes — never adjectives |
| `████░░░░` bar | any progress | yes |
| Table | comparing 3+ things | yes |
| ASCII tree | showing structure | when structure matters |
| `───` separator | before the delivery block | yes |
| Box `╭──╮` | title of a major delivery | optional |

> **The rule that stops decoration:** a visual element REPLACES text, never accompanies it. If a
> table and a paragraph say the same thing, delete the paragraph. But the paragraph explaining
> WHY the table looks that way is not duplication — it is the delivery.

**Terminal limit — this is the only surface.** Responses render as Markdown in a terminal:
**there is no font size.** Hierarchy comes from headings, colour, tables and separators, and no
rule of structure changes that. Design for the terminal, never around it.

> ⛔ **Never propose leaving the terminal** — no web page, no browser, no external rendering.
> Brian, 2026-08-03: *"es todo sobre Claude Code, al menos que te diga lo contrario."*
> If he asks for another surface, that is his call and it is made explicitly, once, for that
> delivery. It is never the default and never a suggestion.

### 7.5 · ⭐ SIZE CEILING — the rule that keeps §7.3 from becoming a wall

**Why this exists:** §2.5 removed the instruction that cut the closing short, and §7.1 requires
explanation. Neither puts a ceiling on the other. Without one, "explain everything" becomes three
screens where half a screen was owed — the same failure, arriving from the opposite side.

**The evidence is this project's own, measured on its own tree:**

| File | Size | State |
|---|---|---|
| `memory/PENDIENTES.md` | 240 KB | 🔴 unreadable — read 39× in one session |
| `memory/Estado_Sesion_Continuidad.md` | 196 KB | 🔴 a living fossil |
| `memory/Bitacora_Progreso.md` | 162 KB | 🔴 grows with no trim |
| `memory/RETOMAR.md` | 14 KB | 🟢 **has a limit (~200 lines)** |

> **The measured law:** *the only file with a declared limit is the only one that never
> overflowed.* A ceiling holds when a **script** enforces it — never when it is a good intention.

**Ceilings by response type:**

| Type | Ceiling | Why that one |
|---|---|---|
| A question with an answer | no block, brief | conversation, not delivery |
| Normal delivery | **~60 lines + block** | fits a screen and a half |
| Major delivery (phase, audit) | no ceiling, **but an index up top** | if it is long, it must be navigable |

**The principle:** *a curated summary, never a raw log — the detailed chronology belongs in a
file, not in the summary.* Applied here: when a delivery needs more than its ceiling, **the detail
goes to a file and the response points at it.** Never dumped on screen.

**⭐ THE INDEX a major delivery owes** — the ceiling table says *"index up top"*; this is what that
means. Over the ceiling, before the body:

```
📑 EN ESTA ENTREGA
   1 · What was audited          → the why
   2 · State in one image        → the bars
   3 · What the machine measured → table
   4 · The verdict               → your decision
```

**Why:** tiered reading (§7.6) applied to the body. The reader decides what to read **before**
reading it. Without it, a long delivery forces a linear pass to find the one part that mattered.
Each line names the section **and what it delivers** — a bare list of titles is a table of
contents, not an index.

### 7.6 · TIERED READING — the block goes first when the response is long

**The problem it solves:** the delivery block closes the response. Above two screens, the reader
must cross the entire body to find where things stand — precisely the frustration §7 exists to fix.

**The rule:** above ~40 lines, the block appears **twice**:

```
Tier 1 · top     — 3 lines: ✅ what is done · ⛔ what is blocked · 👉 what is next
                   the reader can stop here and still decide
Tier 2 · body    — the explanation, sections, evidence
Tier 3 · bottom  — the full block with every field
```

**Tier 1 must be enough to decide. The rest is for when the decision needs backing.** Same cost
pyramid the cold-start brief already applies (`memory/RETOMAR.md`: read the state first, the
pointers only if the state does not suffice) — here applied inside a single response.

### 7.7 · The closing block

Any response that ran commands, edited files, investigated, or produced a decision ends with:

```
─────────────────────────────────────────────
## 📦 ENTREGA

🩺 SALUD DEL SISTEMA: 🟢 better than we started — evidence in the same line

### ✅ HECHO
- **Short name** — what it was + its evidence. Why it matters: the consequence.
- **Short name** — …

### ⬜ NO HECHO
- **Short name** — what was in scope, is not done, and why not.

### ⛔ BLOQUEADO
- **Short name** — what blocks it, and what would unblock it.

### 📌 A PENDIENTES
- **Short name** — WITH the file it was filed into.

### 🙋 NECESITA TU DECISIÓN
- what waits on Brian — or the single word "nada".

### 👉 QUE SIGUE
- the ONE next action.

### 🤔 DECIDES TÚ
The question in one line · a table (Option | What it means | Cost) ·
"My recommendation: X. Reason: Y. The tradeoff: Z."
```

Each field is an `###` so its own size marks where it starts — the same law as §7.1, applied
inside the block. A field with a single item may stay on one line; two or more always become a
list under one label.

**⭐ 🩺 THE HEALTH LINE — a diagnosis, not an activity report.** The six fields say what was *done*;
none says **what state the system is in now**. A reader can finish all six and still not know
whether things are better or worse than when the session started.

| Value | Means | Requires |
|---|---|---|
| 🟢 **better** | something measurable improved | the number, in the same line |
| 🟡 **the same** | work advanced, nothing measurable moved | say what did not move |
| 🔴 **worse** | something broke or a debt grew | 🔴 goes FIRST in the response, never buried |

```
🩺 SALUD DEL SISTEMA: 🟢 better — battery 160/160, +2 rules, 0 broken citations
🩺 SALUD DEL SISTEMA: 🔴 worse — battery 158/160: two checks broke on the last edit
```

**Why it matters:** an owner does not ask what you did, they ask how things stand. Without this
line the block is a log of activity; with it, it is a diagnosis. **A 🔴 is never hidden at the
bottom** — it moves to the top of the response.

**⭐ BEFORE → AFTER → BRIDGE for anything measurable.** A change without its *before* cannot be
sized. Never *"fixed the citations"*; instead:

| Before | After | The bridge |
|---|---|---|
| broken citations: 144 | 0 | 66 v1 fossils deleted; **69 were false positives of the validator** |

**Why:** the assertion hides what the table reveals — nearly half the problem was the validator,
not the citations. **The bridge is the column that carries the finding**, and the one an assertion
always loses.

**⭐ THE LABEL APPEARS ONCE. Items hang under it.** (Brian, 2026-08-03: *"los hechos no deberías
de repetir la palabra — debería ser HECHO: ✅ todos los que sí cumplieron, así con los demás."*)

```
⛔ WRONG — the label repeated per item
   ✅ HECHO — wrote the contract
   ✅ HECHO — mirrored the vehicle
   ✅ HECHO — ran the battery

✅ RIGHT — the label once, the items under it
   ### ✅ HECHO
   - **Contract written** — 4 parts per section. Why it matters: …
   - **Vehicle mirrored** — both files aligned. Why it matters: …
   - **Battery run** — 160/160. Why it matters: …
```

**Why repeating it is a real defect, not a style quibble:** the eye uses the label as a boundary
marker. Repeated four times, it stops marking anything and becomes noise — the same reason a
heading level repeated on every line stops being a heading.

**Each item carries its consequence, not just its fact.** `read 3 files` is a log entry.
`read 3 files — which corrected a number RETOMAR had wrong` is a delivery.

**Empty fields are deleted, never filled with "nada".** Exception: `🙋` says "nada" explicitly —
silence there cannot be told apart from having forgotten.

### 7.8 · When the block does not apply

A single question with a single answer gets no delivery block. It still gets its WHY (§7.1), but
not six headers. **The block is for WORK, not for conversation** — six headers on a one-line
answer is the same noise this contract removes. If there was work but the response is short, the
minimum is `✅ HECHO` and `👉 QUE SIGUE`.

### 7.9 · Progress is shown, not promised

Any task over one step uses the todo tool, so state is visible **as it happens** and not only at
the end. Brian must never have to ask *"¿y sí se hizo?"* — the answer is already on screen.

---

Related: `principles/owner-0-voice.md` (**the other half** — the eight rules that govern the prose;
§6 carries Brian's own additions, which this contract enforces) ·
`principles/expertise/doc-structure.md` §2.1 (the rule that forced this split) ·
`rules/contract-document.md` (the shape every document holds).
