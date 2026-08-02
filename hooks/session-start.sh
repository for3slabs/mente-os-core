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

# Silence unless something is actually red. exit 2 = red (bin/check-health contract).
out="$("$MENTE/bin/check-health" 2>/dev/null)" ; code=$?
if [ "$code" -eq 2 ]; then
  printf '⚠️  Mente OS · check-health reports 🔴 — run: Mente/bin/check-health\n'
  printf '%s\n' "$out" | grep -A2 '^🔴' | head -12
fi

# A block that has drifted is worse than no block: it is a wrong map read as if it were right.
stale="$("$MENTE/bin/flag-stale" 2>/dev/null)" ; scode=$?
[ "$scode" -ne 0 ] && printf '%s\n' "$stale" | head -6

exit 0   # ⛔ always 0 — this hook informs, it never blocks
