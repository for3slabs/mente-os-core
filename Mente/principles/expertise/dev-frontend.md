# EXPERTISE · FRONTEND
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Ticket:** F1-bis-2 · ✅ **FILLED 2026-08-05 by Brian** — with this, **owner-2 is fully covered**.
**Language:** US English · **Read by:** owner-2 (development) before writing code, and owner-3
(validation) at block close.
**Injected by:** the block's §D `Required standards` + the hook (architecture §12-QUATER).
---

## 0 · WHAT THIS FILE IS

The **expert criterion** for this discipline, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (architecture §9.1). It asks, structures, and applies —
> it never fills this in on its own. That is exactly the error that produced the current state:
> *"todo está hecho como la IA quiso."*

**Status:** filled 2026-08-05. F1 closed with `dev-database.md`; this one completes owner-2.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian

| Quote | Date |
|---|---|
| *"esta parte de conversación con For3s está mal responsivamente, tienes un hueco del lado derecho"* | 2026-07-23 |
| *"este menú queda de más porque ya está en el lateral"* | 2026-07-23 |
| *"el problema de fondo es que el estado vive solo en react, no se rehidrata"* | 2026-07-24 |

**Precedents to formalize:** the state that did not survive a refresh · `pagehide` being too
aggressive · the toggle that lied about the agent being on.

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

The frame lives in `rules/qa-dimensions.md`. What each dimension **demands here** is Brian's
criterion — ✅ filled below.

### 2.1 · Architecture
**Question (frame):** does each piece have a single responsibility and sit in the right layer?
**Required evidence:** the dependency tree + which piece would break how many others.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — when a component does too much
>
> | # | It does too much when… | Why |
> |---|---|---|
> | 1 | **it paints AND decides business rules** | the component shows; deciding belongs to another layer. Business rules inside it cannot be tested or reused — the frontend twin of *"the endpoint orchestrates, it does not decide"* (`dev-backend.md` §2.1) |
> | 2 | **it touches data and presentation at once** | if one file fetches, transforms and paints, a change to any of the three touches the whole thing |
> | 3 | **you must read it whole to know what it does** | practical size test: if it does not fit in one read, it is already doing extra |
> | 4 | ⭐ **different people change it for different reasons** | two reasons to change = two responsibilities. If the designer and the data person edit the same file, it must be split |
>
> **Signal 4 is the sharpest**, because it survives refactors: a file can be short and still be
> wrong if two unrelated motives keep landing in it. It is the shape that turned `userStore.ts`
> into **5 responsibilities and 21 edits**.
>
> **How to apply it:** name the ONE reason this component would change. If the sentence needs an
> *and*, it is two components.

### 2.2 · Data design
**Question (frame):** does the schema represent the domain? Are impossible states impossible?
**Required evidence:** the real schema + one case the model cannot represent incorrectly.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — 🔴 where state lives
>
> > **The anchor:** *"el problema de fondo es que el estado vive solo en react, no se rehidrata."*
> > — Brian, 2026-07-24
>
> ## THE SERVER OWNS THE STATE. REACT ONLY REFLECTS IT.
>
> React holds a **copy in order to paint**, never the truth. When the two diverge, **the server
> wins** — the client does not recompute what the backend already decided (§4-BIS pattern 2).
>
> | # | Rule | The failure it kills |
> |---|---|---|
> | 1 | **Everything the user already decided or typed survives a refresh** | session, chosen instance, open thread, half-written text. If `F5` erases it, the user believes they lost their work |
> | 2 | **Nothing unreconstructable lives only in memory** | if the only place a datum exists is component state, closing the tab kills it. It belongs in the DB, the URL, or storage |
> | 3 | **The server is the owner; React reflects** | two sources of truth for one datum diverge — impossible state #2 (`dev-database.md` §2.1), seen from the client |
>
> ### ✅ THE BOUNDARY — what MAY live only in React
>
> **Ephemeral state may, and should.** An open menu, a hover, an animation, a tooltip: rebuilding
> them is free and persisting them is noise.
>
> **The test:** *if this is lost on refresh, does the user lose anything they did?* No → ephemeral,
> leave it in React. Yes → it must survive, and the block says where it lives.
>
> **How to apply it:** refresh the page mid-task and list what disappeared. Anything on that list
> the user had decided or typed is 🔴.

### 2.3 · Abstraction
**Question (frame):** right level — neither copied three times nor generalized for one use?
**Required evidence:** where it repeats, or the real usages.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> | # | Rule | Why |
> |---|---|---|
> | 1 | **A visual pattern copied 3 times becomes a component** | buttons, cards, notices: three copies drift on their own, and then the product looks like three products |
> | 2 | **A repeated style goes to the design system, never copied** | colours, spacing, typography in ONE place. Copied values make the look impossible to change later — you must find every copy first |
>
> ⚠️ **Note the asymmetry, and it is deliberate:** three copies for a *component*, but a repeated
> *style* goes to the system on the second. A duplicated style is cheaper to centralise and far
> more expensive to leave — it is the thing that gets copied fastest and diverges most quietly.
>
> **How this relates to `rules/qa-dimensions.md` §2.3:** the general rule says there is no fixed
> number — what decides is whether the copies must change together. Visual patterns **always** must:
> a button that stops matching the other buttons is a defect the user sees. Hence the fixed number
> here.

### 2.4 · Naming
**Question (frame):** does the name say what it does without reading the body?
**Required evidence:** explain three names without opening the file.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## The name says WHAT IT SHOWS, never how it looks.
>
> ✅ `ThreadList` · `InstancePicker` — ⛔ `BluePanel` · `BoxLeft` · `RightColumn`
>
> **Why:** the appearance changes; what it shows does not. A name describing the look is wrong the
> first time the design moves — and then it lies, which is worse than being vague.
>
> ## ⛔ No generic component — `Wrapper`, `Container`, `Box`
>
> A name that says nothing forces you to open the file. **It is `kind` at the component level:** one
> label covering several meanings, and the reader cannot tell which one they have.
>
> **How to apply it:** name three components in the block and say what each shows **without opening
> them**. If you cannot, or if the answer describes a colour or a position, this dimension is 🔴.

### 2.5 · Contracts
**Question (frame):** are interfaces declared? Are errors part of the contract?
**Required evidence:** the real signature + what happens when it fails.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — when a user action fails
>
> | # | The interface must… | Why |
> |---|---|---|
> | 1 | **Say it in language the user understands** | no codes, no stacks: what happened and what they can do. Mirror of the backend rule — **detail goes to the log, not to the client** (`dev-backend.md` §2.5) |
> | 2 | 🔴 **NEVER leave the screen in a state that lies** | if the save failed, it cannot keep showing "saved". This is the toggle-that-lied, generalised (§4 signal 4) |
> | 3 | **Let them retry without losing what they typed** | the failure must not cost the user what they had already done. Retrying is one click, not redoing everything |
> | 4 | **Record the failure even if the user never sees it** | same criterion as backend: **a failure with no trace does not exist** for whoever must fix it |
>
> ⭐ **Rules 2 and 3 together are what separates an error from a disaster.** An error the user
> understands and can retry costs seconds. A screen that lies about having saved costs the work —
> and the trust.
>
> **How to apply it:** force the failure (cut the network, make the endpoint return an error) and
> watch the screen. If it still shows success, or the typed content is gone, this dimension is 🔴.

### 2.6 · Necessity
**Question (frame):** does every file that exists have to exist?
**Required evidence:** who consumes it, and why it could not live elsewhere.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## Nobody imports it → it is DELETED.
>
> **Measured with importers, never with mentions** (`blk-demo` §G: a dependent is a file that
> IMPORTS the piece, not one that names it).
>
> **The case is open right now:** `components/demo/ConnectClaude.tsx` — **145 lines, 0 importers,
> untouched since 2026-06-16**, still in the tree. It is sub-block 10 of `blk-demo` and one of the
> two reds in that block's layer-1 verdict.
>
> ⚠️ **A dead component is quieter than a dead endpoint** — it answers nothing, so nothing reveals
> it. That is exactly why it needs a measurement rather than a memory: it will never announce
> itself, and *"lo dejo aquí por si lo necesitamos"* keeps it alive forever
> (`rules/qa-dimensions.md` §2.6).

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — never, no exceptions
>
> | # | ⛔ Never | Why |
> |---|---|---|
> | 1 | 🔴 **Put a secret or an API key in the client** | everything that reaches the browser is public. **If it is in the bundle, it is leaked** — and a leaked secret is ROTATED, not deleted (`rules/rule-config-hygiene.md` §1.1) |
> | 2 | 🔴 **Hide a button as the only authorization** | hiding is presentation, not permission. The real check lives on the server (§4-BIS pattern 3 · `dev-backend.md` §3 rule 2) |
> | 3 | **Freeze the interface waiting for the server** | the screen does not lock: it shows it is working and lets the user cancel or continue |
> | 4 | **Leave the screen showing a state that is not real** | §2.5 rule 2 — the toggle that lied |
>
> Rules 1 and 2 are **security findings**: 🔴 on sight. Rule 1 is verifiable by searching the built
> bundle, not the source — a value can reach the client without ever being typed in a component.

---

## 4 · WHAT MAKES BRIAN REJECT WORK IN THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## FOUR SIGNALS OF AN UNFINISHED UI — any ONE is enough
>
> | # | Signal | The anchor |
> |---|---|---|
> | 1 | **It breaks or leaves gaps when resized** | *"esta parte de conversación con For3s está mal responsivamente, tienes un hueco del lado derecho"* (2026-07-23). ⭐ **Responsive is not "it fits"** — it is that at NO width does it leave a gap or cut content |
> | 2 | **Two ways to do the same thing on screen** | *"este menú queda de más porque ya está en el lateral"* (2026-07-23). Duplicated navigation forces the user to choose with no criterion for choosing |
> | 3 | **The user cannot tell whether it is loading or it failed** | a click with no response looks like a broken app. It is the visual form of failing silently (`val-integration.md` §2.5) |
> | 4 | 🔴 **A control LIES about the real state** | the toggle that said the agent was on when it was off. **This is the worst of the four: it is not ugly, it is false** — the user acts on information the system knows is wrong |
>
> ⚠️ **Signal 4 outranks the rest.** 1 to 3 make the product look unfinished; 4 makes it
> untrustworthy. A UI that lies costs what `dev-database.md` §2.5 names: *"perdemos credibilidad,
> perdemos confianza."*

---

## 4-BIS · IMPORTED PATTERNS → `principles/imported-patterns.md` §3 · FRONTEND

The failure patterns imported from an external skill live there now, gathered with the other two
disciplines' — **same source, same status, and none of them Brian's criterion.**

> ⭐ **Moved 2026-08-05** because `dev-database.md` broke its 350-line ceiling and
> `principles/expertise/doc-structure.md` §2.1 says a document over its ceiling **must be split,
> with the halves pointing at each other**. ⛔ **Nothing was deleted** — only the numbering changed.

⚠️ **They still apply.** A block that declares this file in its §D is judged by §2-§4 here
(**Brian's criterion**) **and** by those patterns — and where both speak, the stricter one wins
(`rules/rule-inheritance.md`).

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> Never the reverse — a draft written first comes out as *"use best practices."*

**Suggested questions for the interview:**

1. What do you demand of a component before it is done?
2. What makes a UI look unfinished to you?
3. Where must state live, and what must survive a refresh?
4. When is a component doing too much?
5. What do you demand of responsiveness, concretely?
6. What must the user always be able to see or undo?
7. Which frontend error do you see most often?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context (layer D, §12-QUATER) |
| Block closes | owner-3 evaluates the 6 dimensions using it (`rules/qa-dimensions.md`) |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are FILLED**, so both the wiring and the criterion are live. Layer 1 of QA
> (`bin/grade-block`) does not depend on this file — that is why F4 can run first.

---

Related: `rules/qa-dimensions.md` (the frame) · `principles/owner-2-dev.md` (who reads it) ·
`principles/owner-3-validation.md` (who applies it) · `docs/Arquitectura_Mente_OS_v2_Bloques.md` §9.
