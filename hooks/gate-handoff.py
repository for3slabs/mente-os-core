#!/usr/bin/env python3
"""PreToolUse(Agent) — a specialist that can WRITE does not launch without a declared scope.

Turns rules/contract-handoff.md from intention into a gate. The measured law of this system:
a rule enforced by code complies 100%; a rule that lives only in a document complies 40-60%.

⭐ THE LEVEL WAS MEASURED, NOT ASSUMED (2026-07-31, across every .jsonl in the project):

    Bash ......... 9,786 calls
    Edit ......... 3,289
    Read ......... 1,851
    Agent ..........  32     ← 15 of them read-only (Explore)

That number inverted the diagnosis. The 20-jul failure (421 Bash commands, 999K context, the
21-jul incident) was NOT "delegating badly" — it was **not delegating at all**. There is no
history of specialists writing where they should not; there is a history of everything happening
in one context until it saturated.

So the gate follows plan §F6: **if a gate obstructs more than it protects, it degrades to a
warning.** Blocking a read-only Explore would make cheap delegation more expensive than doing
the work inline — pushing straight back toward the behavior that caused the incident.

| Agent can… | Level | Why |
|---|---|---|
| WRITE (general-purpose, custom agents) | 🔴 **BLOCK** | an unbounded writer inside a bounded system is the real risk |
| only READ (Explore) | ⚠️ **WARN** | it cannot corrupt anything, and this is the delegation that was missing |

Escape hatch (rules/rule-friction.md — a gate with no escape gets deleted):

    MENTE_HANDOFF_BYPASS=1

Deliberate and visible: it prints that the gate was skipped and what that costs.

Contract: PreToolUse payload on stdin. exit 0 = allow · exit 2 = BLOCK.
"""
# Implements ADR-012 — one of the ONLY THREE closed gates
import os
import re
import sys
import glob
import json
import subprocess

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                        # noqa: E402

# Read-only agent types: they return a conclusion and write nothing, so there is no write scope
# to declare. Explore is defined read-only by the harness itself ("All tools except ... Edit,
# Write, NotebookEdit"). Plan is the same shape.
READ_ONLY = {"explore", "plan", "claude-code-guide", "statusline-setup",
             "gsd-plan-checker", "gsd-integration-checker", "gsd-assumptions-analyzer",
             "gsd-user-profiler", "gsd-ui-checker"}


def manifests():
    """Every handoff manifest on disk, newest first."""
    found = glob.glob(f"{MENTE}/blocks/*/*/handoffs/*.yml")
    return sorted(found, key=os.path.getmtime, reverse=True)


def verified(path):
    """A manifest counts only if bin/verify-handoff says it is bounded (exit 0).

    🔴 The whole point: presence is not compliance. A malformed manifest sitting on disk must
    NOT open the gate — that would be the paperwork version of a scope.
    """
    try:
        r = subprocess.run([f"{MENTE}/bin/verify-handoff", path, "--quiet"],
                           capture_output=True, text=True, timeout=15)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False                       # cannot verify → does not count as verified


def main():
    beat(MENTE, "gate-handoff")   # proof this gate still fires (hooks/_beat.py)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0                                               # malformed input never blocks

    # Same defensive shape as the other hooks: the payload comes from outside.
    if not isinstance(payload, dict):
        return 0
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return 0

    subagent = ti.get("subagent_type")
    subagent = subagent.strip().lower() if isinstance(subagent, str) else ""
    desc = ti.get("description") if isinstance(ti.get("description"), str) else ""

    # ── read-only specialists: warn, never block ────────────────────────────
    # Measured decision (see docstring). They cannot corrupt anything, and this is exactly the
    # cheap delegation whose ABSENCE caused the 20-jul saturation.
    if subagent in READ_ONLY:
        print(f"⚠️  `{subagent}` is read-only — no manifest required.\n"
              "   It returns a conclusion and writes nothing. If it ever needs to WRITE,\n"
              "   it needs a manifest first (rules/contract-handoff.md).", file=sys.stderr)
        return 0

    # ── the escape hatch, loud on purpose ──────────────────────────────────
    if os.environ.get("MENTE_HANDOFF_BYPASS") == "1":
        print("🟡 HANDOFF GATE BYPASSED — MENTE_HANDOFF_BYPASS=1\n"
              f"   Launching `{subagent or 'a specialist'}` with NO declared scope.\n"
              "   Nothing records what it may read, where it may write, or when it must stop.\n"
              "   If it writes outside the block, no validator will catch it.", file=sys.stderr)
        return 0

    # ── a writer needs a verified manifest ─────────────────────────────────
    ok = [m for m in manifests() if verified(m)]
    if ok:
        rel = os.path.relpath(ok[0], MENTE)
        print(f"✅ handoff gate: bounded by {rel}\n"
              "   Verify the objective matches THIS task — a stale manifest is a scope for "
              "different work.", file=sys.stderr)
        return 0

    total = len(manifests())
    detail = (f"   {total} manifest(s) on disk, none passing bin/verify-handoff — "
              "presence is not compliance.\n"
              if total else "   No handoff manifest exists for any active block.\n")

    print(f"🔴 BLOCKED · `{subagent or 'specialist'}` can WRITE and has no declared scope.\n"
          f"   Task: {desc[:70]}\n"
          f"{detail}"
          "   An unbounded writer inside a bounded system is what the manifest exists to stop:\n"
          "   what it may read · what it must do · where it may write · when it must stop.\n"
          "\n"
          "   Fix (rules/contract-handoff.md):\n"
          "     1. cp Mente/rules/template-handoff.yml \\\n"
          "          Mente/blocks/active/<block>/handoffs/<YYYY-MM-DD-HHMM-slug>.yml\n"
          "     2. fill it in — every placeholder is rejected\n"
          "     3. Mente/bin/verify-handoff <that file>     # must exit 0\n"
          "\n"
          "   Not worth a manifest? Then it is not worth a subagent — do it inline\n"
          "   (contract-handoff.md §7).\n"
          "   Bypass: MENTE_HANDOFF_BYPASS=1 — deliberate, and it says so out loud.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
