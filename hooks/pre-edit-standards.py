#!/usr/bin/env python3
"""F5-2 · PreToolUse(Write|Edit) — inject the block's standards before its code is touched.

The measured law of this system: rules enforced by code comply 100%; rules that live only in a
document comply 40-60%. §D of a block lists the standards that apply to it — and until now nothing
read them at the moment they mattered.

This hook closes that gap: touch a file inside a block's Scope IN, and that block's §D standards
are named back to you, in the same turn, before the edit lands.

⛔ It NEVER blocks. It informs. Blocking on a heuristic path match would make editing unbearable,
and an unbearable guard gets deleted — which protects nothing.

Contract: reads a PreToolUse payload on stdin, exits 0 always.
"""
import os
import re
import sys
import glob
import json

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                        # noqa: E402


def main():
    beat(MENTE, "pre-edit-standards")   # proof this gate still fires (hooks/_beat.py)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0                                               # malformed input never blocks

    target = (payload.get("tool_input", {}) or {}).get("file_path", "")
    if not target:
        return 0

    for bpath in glob.glob(f"{MENTE}/blocks/active/*/BLOCK.md"):
        try:
            text = open(bpath, encoding="utf-8", errors="replace").read()
        except OSError:
            continue

        # §B IN declares the block's territory. A path matches if any declared
        # directory appears in it — the same measurement bin/grade-block uses.
        m = re.search(r"##\s*✅?\s*IN\s*\n((?:\s*-.*\n)+)", text)
        if not m:
            continue
        owned = False
        for tok in re.findall(r"[\w./-]+/[\w./*-]*", m.group(1)):
            d = tok.split("*")[0].rstrip("/")
            if len(d) > 4 and d in target:
                owned = True
                break
        if not owned:
            continue

        std = re.search(r"##\s*Required standards\s*\n((?:\s*-.*\n)+)", text)
        name = os.path.basename(os.path.dirname(bpath))
        lines = [f"📦 {target} belongs to block `{name}` — its §D standards apply:"]
        if std:
            for s in re.findall(r"-\s*(\S+)", std.group(1)):
                lines.append(f"   · {s}")
        else:
            lines.append("   🔴 §D is empty — the block declares no standards (contract-block.md)")

        # An UNCLOSED sub-block covering this file is the fix-on-fix pattern the block exists to
        # stop. `active` counts: it is work in progress, and editing under it is how userStore.ts
        # reached 21 edits. (Bug caught by test ⑤, 2026-07-30: the first version omitted `active`.)
        for row in re.findall(r"^\|[^|]*\|([^|]*)\|([^|]*)\|[^|]*\|\s*(\w+)\s*\|", text, re.M):
            piece = row[1].strip().strip("`")
            state = row[2].strip()
            if piece and len(piece) > 4 and piece in target and state != "closed":
                lines.append(f"   ⚠️  sub-block for this file is `{state}`: {row[0].strip()}")

        print("\n".join(lines), file=sys.stderr)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
