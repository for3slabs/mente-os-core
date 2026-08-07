# RULE · A CHECK MUST MEASURE WHAT IT CLAIMS
**Status:** current · **Type:** rule · **Updated:** 2026-08-02 · **Owner:** brian
**Ticket:** 8 findings of the 2026-08-02 session · **Enforced by:** `bin/test-f0-f6`
**Implements:** ADR-024 (the system audits itself) · **Governs:** every validator in `bin/` and `hooks/`
---

## Purpose

The failure mode this system keeps producing: **a check that runs, reports green, and is not
measuring what it claims.** Not a missing check — a present one, active, trusted, and blind.

> ⭐ **The rule in one line:** a check that has only ever been seen GREEN has not been tested.

---

## 0 · WHY THIS FILE EXISTS

Measured on 2026-08-02, in one session, **eight findings of the same shape**. Every one of them
was a check that existed and was believed:

| What was believed | What was true |
|---|---|
| the battery was green | it read `$?` **after** another command overwrote it |
| broken citations were ~73 | they were **144** — `check-links` was the only validator nothing ran |
| `CLAUDE.md` was audited | the glob started inside `Mente/`; the file lives one level up |
| the `/clear` guard was armed | it matched 8 hex as a **substring** — a commit hash disarmed it |
| ADR supersede symmetry held | it compared `"016"`, which `2016` satisfies |
| `deny` protected `secrets/` | `python3 -c "open(...)"` read straight past it |

**None of these was found by the system.** All were found by attacking it — and two by the
battery catching a fix that had just been written for something else.

---

## 1 · THE FOUR FAMILIES

### A · Loose comparison — the string is too short to mean anything

```python
⛔  if sid not in text:                 # 8 hex chars: 'abcdc733bc1def' satisfies 'dc733bc1'
⛔  if basename(f).split("-")[1] in s:  # "016" — so does "2016" and "F3-016b"
✅  re.search(rf"(?<![0-9a-f]){re.escape(sid)}(?![0-9a-f])", text)
```

**Found in 4 files** written at different times: `check-blocks` · `check-clear-ready` ·
`check-health` · `generate-metrics`. The last one **publishes** the number, so the lie travelled.

> **The test:** if this string turned up by accident, would the system become more permissive?
> Short + alphanumeric (ids, numbers) → delimit it. A literal with markup (`**Type:**`, `⬜`,
> a full path) cannot appear by chance and needs nothing.

### B · Short reach — the scope starts one level too low

```python
⛔  glob.glob("**/*.md")          # run from Mente/ — CLAUDE.md lives above it
⛔  for d in (RETOMAR, how-it-runs, SKILL):   # the router was not on the list
```

`CLAUDE.md` is loaded at **every** session start and was the only document nothing audited: zero
of the four required header fields, two dead pointers, three frozen numbers.

> **The test:** name the thing this check is meant to protect. Now list what it actually reaches.
> **The gap is the finding.** ⭐ *The file read FIRST was the least watched.*

### C · Clobbered value — measured correctly, then overwritten

```bash
⛔  cmd; eq "label $( [ $x = 0 ] && echo yes )" "$want" "$?"   # the $() ate $?
✅  cmd; _e=$?; eq "label …" "$want" "$_e"
```

`$?` survives exactly one command. This one only showed when the expected value was `1`: with `0`
the clobbered value coincided **by accident**, so it passed for weeks.

---

### D · Exigir algo que POR DISEÑO no viaja — el check mide la máquina, no el sistema

```bash
⛔  eq "secrets/ is 700" "700" "$(stat -c %a secrets)"     # secrets/ está en .gitignore
⛔  for f in settings.json settings.local.json; do …       # la .local NUNCA viaja
⛔  [ -f ".beats/$_g" ] || bad …                            # .beats/ es por máquina
✅  [ -d secrets ] && eq … || ok "no existe aquí — nada que proteger aún"
✅  [ -f "$REPO/.claude/$f" ] || continue
✅  printf '…' | python3 "hooks/$_g.py" >/dev/null 2>&1     # se INVOCA, luego se exige la marca
```

🔴 **Medido el 2026-08-07 y es la familia más cara de todas:** la batería daba **195/0 en la
máquina de Brian y 22 fallos en un clon limpio**. Nadie lo vio durante meses porque nadie corría
la batería fuera de este árbol — lo encontró una auditoría externa, no el sistema.

**Encontrada en 4 sitios** por la misma causa: `piezas.tsv` (atrapada en `Maestro/`, otro repo) ·
`secrets/` y `settings.local.json` (en el `.gitignore`) · `blocks/blocked/` (git no versiona
directorios vacíos) · `.beats/` (por máquina, a propósito).

> **El test:** *¿este archivo llega a un clon?* Si está en `.gitignore`, es de otro repo, o se
> crea al usar el sistema — entonces exigirlo presente mide **quién trabajó antes en ese árbol**,
> no si el sistema funciona.
>
> ⭐ **Y la salida nunca es dejar de verificar:** si el archivo existe, se le exige lo mismo de
> siempre; si no, se comprueba el COMPORTAMIENTO en su lugar. Los latidos pasaron de *"¿existe la
> marca?"* a *"invoco la puerta y exijo la marca después"* — eso se verifica igual en cualquier
> máquina.

⚠️ **Corolario, aprendido cuatro veces el mismo día:** corregir esta familia en un validador **no
la corrige en sus hermanos**. `check-health` arrastraba el mismo fallo que ya se había arreglado
en `test-f0-f6`. Al encontrar uno, se busca el patrón en los demás.

---

## 2 · ⭐ THE RULE

> ## Before trusting a check, make it FAIL on purpose.
> A green you have never seen turn red is a green that proves nothing.

Two runs, always:

| Direction | Question |
|---|---|
| 🟢 **positive** | with the condition satisfied, does it pass? |
| 🔴 **negative** | breaking the condition **on purpose**, does it report it, and does the message name the real cause? |

**The negative run is the one that gets skipped**, and it is the only one that proves the check
is connected to what it claims to measure.

### The corollary, learned the hard way the same day

**A failed negative run may mean the TEST is wrong, not the check.** Twice on 2026-08-02:

- The first probe of the ADR symmetry check removed **one** of two mentions — "it did not detect"
  was a false negative of the *probe*. Both had to go.
- Investigating that probe is what exposed the real defect: the check compared `"016"`.

> When a negative run does not fire, suspect the probe **and** the check. Fixing only the probe
> leaves the hole, and you will have proven nothing while feeling that you did.

---

## 3 · WHAT THIS DOES NOT MEAN

- Not *"delimit every comparison"*. Six were audited and **left alone on purpose** — literals with
  markup cannot collide. A validator that warns about non-defects is one people learn to ignore.
- Not *"test all 66 assertions both ways"*. Unaffordable, and it would bury the ones that matter.
  Scope it to what guards something **irreversible**: the `/clear`, the three gates, the
  credentials, ADR symmetry.
- Not a replacement for `rule-config-hygiene` §1.5. That one governs **lists**; this one governs
  **comparisons, reach and captured values**. Sibling rules, different failure.

---

## 4 · WHERE THIS IS ENFORCED

| Moment | What runs |
|---|---|
| every battery run | `bin/test-f0-f6` — the checks themselves |
| at session start | `bin/check-health` — the guards exist, are armed, and are wired |
| ✅ every battery run | `bin/test-f0-f6` §SELF-TEST — breaks the critical guards **on purpose** and requires them to fail. The manual step that found these eight is no longer manual. |

**Scope, measured rather than estimated:** the plan assumed 12-15 checks needed this. Measuring
showed the battery already carried the negative twin for `GATE db`, `GATE close`, `pre-commit`
and `gate-handoff` (`BLOCKS …` / `allows …`). Genuinely orphaned: **3**. Estimating would have
produced a dozen redundant probes — and redundant probes are how a battery becomes noise.

---

Related: `rules/rule-config-hygiene.md` §1.5 (the sibling rule, for lists) ·
`rules/rule-fix-not-patch.md` (*why does this failure exist and WHERE ELSE does it live* — the
question that turned 1 finding into 4) · `rules/decisions/ADR-024-system-audits-itself.md` ·
`bin/test-f0-f6` · `memory/PENDIENTES.md`.
