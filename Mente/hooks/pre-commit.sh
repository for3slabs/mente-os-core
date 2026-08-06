#!/usr/bin/env bash
# F5-3 · pre-commit — an invalid block never reaches a commit.
#
# ⭐ The ONLY hook in F5 that BLOCKS, deliberately:
#   · session-start / pre-edit inform, because blocking on a heuristic makes work unbearable
#   · a commit is permanent. A block that lies inside a commit lies forever, and the next
#     session reads it as truth. That is the failure this whole system exists to stop.
#
# 🔴 BUG FOUND 2026-07-30 (by testing an actual commit, not by reading the script):
#   the first version resolved MENTE from BASH_SOURCE. Git runs the hook from .git/hooks/,
#   so dirname/.. resolved to `.git` — check-blocks was not there, exit was 127, and the
#   `-eq 2` test never matched. **The hook let every commit through while looking installed.**
#   A guard that fails open is worse than no guard: it is a false sense of safety.
#
#   Fix: resolve from the repo root (git rev-parse), and FAIL CLOSED if the validator is
#   missing — a validator that cannot run is not a pass.
set -uo pipefail
# Implements ADR-012 — one of the ONLY THREE closed gates

REPO="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0

# Mente may be this repo, a directory inside it, or a SIBLING (marca-personal is its own repo
# and Mente lives next to it). Checked in that order.
# EXISTS and EXECUTABLE are different answers: absent → not our repo; present but unusable →
# 🔴 refuse, because a validator that cannot run is not a pass. (Found adversarially 2026-07-30:
# a chmod -x made the hook take the fail-OPEN path and let EVERY commit through.)
for cand in "$REPO/bin/check-blocks" \
            "$REPO/Mente/bin/check-blocks" \
            "$(dirname "$REPO")/Mente/bin/check-blocks"; do
  if [ -x "$cand" ]; then CHECK="$cand"; break
  elif [ -f "$cand" ]; then FOUND_BROKEN="$cand"
  fi
done

if [ -n "${FOUND_BROKEN:-}" ] && [ -z "${CHECK:-}" ]; then
  printf '🔴 COMMIT BLOCKED — %s exists but is not executable.\n' "$FOUND_BROKEN"
  printf '   A validator that cannot run is NOT a pass. Fix: chmod +x %s\n' "$FOUND_BROKEN"
  exit 1
fi

# ⚠️ fail-OPEN when Mente is genuinely absent, fail-CLOSED when it exists but is broken.
# Second bug caught 2026-07-30: blanket fail-closed would have blocked EVERY commit in
# marca-personal — the repo where the demo lives. A guard that stops all work gets deleted,
# and a deleted guard protects nothing (rule-friction.md).
if [ -z "${CHECK:-}" ]; then
  exit 0   # no Mente reachable → this repo is not governed by blocks. Nothing to verify.
fi

# A validator that hangs is a commit that hangs. 120s is ~40x the measured runtime.
out="$(timeout 120 "$CHECK" 2>&1)"; code=$?
if [ "$code" -eq 124 ]; then
  printf '🔴 COMMIT BLOCKED — check-blocks timed out after 120s.\n'
  exit 1
fi
if [ "$code" -eq 2 ]; then
  printf '🔴 COMMIT BLOCKED — a block violates its contract.\n\n'
  printf '%s\n' "$out" | sed -n '/^🔴/,$p' | head -20
  printf '\nFix it, or: git commit --no-verify   (and log why in the block §H)\n'
  exit 1
fi
if [ "$code" -ne 0 ] && [ "$code" -ne 1 ]; then
  printf '🔴 COMMIT BLOCKED — check-blocks exited %d (unexpected).\n' "$code"
  printf '   Failing closed on purpose: an unexplained exit is not a pass.\n'
  exit 1
fi

# ── P2 · GENERATED ARTEFACTS MUST NOT DRIFT (2026-08-05) ─────────────────────
# The pattern comes from graphify's `tools/skillgen --check`: generated files are committed
# artefacts, and CI byte-diffs the render against what is committed so drift is impossible
# rather than merely detectable. `--check` already existed in both generators; nothing at the
# GATE called it, so a stale docs/INDEX.md could be committed. Measured the same day: it WAS
# stale. This is the defect this session caught five times — a piece written and not wired.
#
# ⚠️ Only generate-index runs here. `generate-metrics --check` runs the whole battery and takes
# 2m31s (measured); generate-index takes 0.118s. A gate that costs 2.5 minutes per commit is a
# gate that gets bypassed, and a bypassed gate protects nothing (rule-friction.md). METRICS drift
# is covered by bin/test-f0-f6 instead — see P1.
IDX="$(dirname "$CHECK")/generate-index"
if [ -x "$IDX" ]; then
  if ! timeout 60 "$IDX" --check >/dev/null 2>&1; then
    printf '🔴 COMMIT BLOCKED — a generated index is out of date.\n\n'
    printf '   Committing it would publish a value nobody measured.\n'
    printf '   Fix: %s\n' "$IDX"
    printf '\n   Or: git commit --no-verify   (and log why in the block §H)\n'
    exit 1
  fi
fi

# ── ⭐ TECHO DE WARNINGS (2026-08-06) ────────────────────────────────────────
# 🔴 EL DEFECTO QUE ESTO CIERRA, señalado por Brian: *"el sistema está permitiendo tener
# warnings y no verificarlos"*. Este hook solo miraba `-eq 2` (errores). Los warnings no los
# miraba NADIE, así que crecieron de 31 (2026-07-30) a **76** en cinco días sin resistencia
# alguna — y entre ellos había 5 defectos reales del bloque `demo` mezclados con falsos
# positivos del propio validador.
#
# ⭐ El techo NO es cero, y es deliberado: `grown section` es una SEÑAL de partir, no un
# defecto, y forzarla a cero empujaría a partir documentos por obediencia. Lo que se prohíbe
# es la ACUMULACIÓN silenciosa: por encima del techo hay que bajar la deuda o subirlo a
# conciencia, que es una decisión visible en el diff.
WARN_CAP=15
w=$("$CHECK" 2>/dev/null | grep -oE '[0-9]+ warnings' | grep -oE '^[0-9]+' | head -1)
if [ -n "$w" ] && [ "$w" -gt "$WARN_CAP" ]; then
  printf '🔴 COMMIT BLOCKED — %s warnings, por encima del techo de %s.\n\n' "$w" "$WARN_CAP"
  printf '   Un warning que nadie mira se acumula: pasaron de 31 a 76 en cinco días.\n'
  printf '   Míralos: %s   y baja la deuda, o sube WARN_CAP a conciencia.\n' "$CHECK"
  printf '\n   Or: git commit --no-verify   (and log why in the block §H)\n'
  exit 1
fi
exit 0
