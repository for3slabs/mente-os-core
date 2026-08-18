#!/usr/bin/env bash
# F5-1 · SessionStart — the system reports its own state without being asked.
#
# Rule behind this file (Brian, 2026-07-27): if you have to ASK for it, it is not automated.
# Three failures lived for weeks and were found by Brian asking, not by anything watching.
#
# Two hard constraints, both learned the hard way:
#   1. NEVER block the session. A hook that fails must not stop Brian from working.
#   2. Speak ONLY on 🔴. A validator that talks every time is a validator that gets ignored.
set -uo pipefail
MENTE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Implements ADR-024 — the audit runs by itself — asking for it means it is not automated

# ── THE HEARTBEAT ───────────────────────────────────────────────────────────
# 🔴 The structural gap, measured 2026-07-31: this hook is SILENT when everything is fine —
# and equally silent if it is dead. Healthy silence and dead silence were indistinguishable,
# so the guard that reports on every other guard could stop running and nobody would know.
#
# No check can catch that from the inside AS IT HAPPENS: a missing warning is exactly what a
# healthy system looks like. But it is catchable AFTERWARDS. Stamping a date turns "it said
# nothing" into "it has said nothing since Tuesday", and that IS distinguishable.
#
# Same shape as bin/flag-stale: "a block that goes quiet is not neutral." Neither is a guard.
# Written FIRST, before check-health runs, so the beat lands even if the check below crashes.
date -u +%Y-%m-%d > "$MENTE/.heartbeat" 2>/dev/null || true

# ── WHICH SESSION IS THIS? ──────────────────────────────────────────────────
# 🔴 Measured 2026-08-18: the validators below decided "the current session" by taking the
# newest .jsonl by mtime. Right after a /clear the new transcript is a few KB old and has NOT
# yet won on mtime, so they measured the PREVIOUS session — closed, registered, 154h long — and
# reported "session open 262h". The alarm that exists because of the 21-jul incident fired at a
# file nobody was writing to, and the noise got repeated as if it were a finding.
#
# Claude Code hands us the real id in the SessionStart payload. Reading it turns the guess into
# a fact. Exported so EVERY validator this hook launches resolves the same session; a validator
# run by hand still falls back to mtime, and knows that it did.
payload="$(timeout 2 cat 2>/dev/null || true)"
MENTE_SESSION_ID="$(printf '%s' "$payload" \
  | grep -o '"session_id"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | head -1 | sed 's/.*"\([^"]*\)"$/\1/')"
export MENTE_SESSION_ID

# Silence unless something is actually red. exit 2 = red (bin/check-health contract).
out="$("$MENTE/bin/check-health" 2>/dev/null)" ; code=$?
if [ "$code" -eq 2 ]; then
  printf '⚠️  Mente OS · check-health reports 🔴 — run: Mente/bin/check-health\n'
  printf '%s\n' "$out" | grep -A2 '^🔴' | head -12
fi

# A block that has drifted is worse than no block: it is a wrong map read as if it were right.
stale="$("$MENTE/bin/flag-stale" 2>/dev/null)" ; scode=$?
[ "$scode" -ne 0 ] && printf '%s\n' "$stale" | head -6

# ⭐ ¿CAMBIÓ ALGÚN PR MIENTRAS YO NO ESTABA? (2026-08-08)
# Brian: "no tienes que estarme preguntando si ya lo mergeé… a lo mejor se me olvida decirte,
# pero sí lo hice". Medido ese día: se preguntó 5 veces en una sesión y una respuesta fue "sí"
# sobre OTRO PR — preguntar cuesta un turno y puede devolver un dato equivocado.
# ⛔ No es un cron: un cron dispara cuando no hay nadie escuchando. El estado vive en GitHub y
# consultarlo al arrancar es barato — el arranque es justo el momento en que puedo actuar.
prs="$("$MENTE/bin/check-prs" 2>/dev/null)" ; pcode=$?
[ "$pcode" -eq 1 ] && printf '%s\n' "$prs" | head -8

exit 0   # ⛔ always 0 — this hook informs, it never blocks
