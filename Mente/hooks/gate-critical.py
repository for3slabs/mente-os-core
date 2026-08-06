#!/usr/bin/env python3
"""F6-3 · the three critical gates — each at the level it EARNED.

Rule of this phase (plan §F6): **if a gate obstructs more than it protects, it degrades to a
warning.** A system that gets in the way gets switched off, and a switched-off gate protects nothing.

Measured 2026-07-30 before choosing each level:

| Gate | Measurement | Level chosen | Why |
|---|---|---|---|
| edit a piece with declared dependents | 5 files, edited constantly | ⚠️ **WARN** | blocking the daily path is pure friction; the propagation LANE already handles it |
| touch the database | 4 SQL files, rarely touched | 🔴 **BLOCK** | an irreversible migration is the one mistake with no undo |
| close a block without sufficiency | `check-sufficiency` exists, nothing called it | 🔴 **BLOCK** | it is the entire point of a block: restart from disk alone |

⭐ Gate 1 stays a warning ON PURPOSE. It is not weakness — it is the measurement saying that the
propagation graph (`rule-lanes.md`) already forces the lane up, so a second stop adds nothing.

Escape hatch, documented on purpose (`rules/rule-friction.md`): every block prints how to bypass it.
A gate with no escape hatch gets deleted.

Contract: PreToolUse payload on stdin. exit 0 = allow · exit 2 = BLOCK (Claude Code convention).
"""
# Implements ADR-012 — one of the ONLY THREE closed gates
import os
import re
import sys
import glob
import json

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                        # noqa: E402

# A migration is irreversible unless it says how to go back. Measured, not assumed.
DB_HINT = re.compile(r"(migration|migr|\d{3}_)|\.sql$", re.I)
# 🔴 THREE BUGS in this pattern, each found by attacking it (2026-07-30):
#   1. It included `DROP\s+(TABLE|COLUMN)`, so a `DROP TABLE x` counted as its OWN rollback and
#      the gate could never fire.
#   2. A bare `\brollback\b` matched the word ANYWHERE — so the comment
#      `DROP TABLE x; -- no rollback needed` DISABLED the gate. A comment saying the opposite
#      switched off the protection. ⭐ The worst class of bug: the escape hatch was a typo away.
#   3. Only files whose NAME looked like a migration were checked — but the demo runs SQL from
#      inside .ts files (measured: duenos.ts, eventos.ts, userStore.ts). Destroying a table from
#      TypeScript was completely unguarded.
#
# A rollback is a STRUCTURAL declaration — a down marker or a reverse statement — never a word in
# prose. Anchored to line starts so prose cannot satisfy it.
DOWN = re.compile(
    r"^\s*--\s*down\b"                 # -- down
    r"|^\s*--\s*rollback\b"            # -- rollback
    r"|^\s*/\*\s*(down|rollback)\b"    # /* down
    r"|^\s*(CREATE\s+TABLE|ALTER\s+TABLE\s+\w+\s+ADD\s+COLUMN)",   # the reverse statement
    re.I | re.M)
DESTRUCTIVE = re.compile(r"\b(DROP\s+(TABLE|COLUMN|DATABASE)|TRUNCATE|DELETE\s+FROM)\b", re.I)


def blocks():
    for b in glob.glob(f"{MENTE}/blocks/active/*/BLOCK.md"):
        try:
            yield b, open(b, encoding="utf-8", errors="replace").read()
        except OSError:
            continue


def owning_block(target):
    """The block whose §B IN covers this path — the same measurement grade-block uses."""
    for path, text in blocks():
        m = re.search(r"##\s*✅?\s*IN\s*\n((?:\s*<!--[^\n]*-->\s*\n)*)((?:\s*-[^\n]*\n)+)", text)
        if not m:
            continue
        for tok in re.findall(r"[\w./-]+/[\w./*-]*", m.group(2)):
            d = tok.split("*")[0].rstrip("/")
            if len(d) > 4 and d in target:
                return os.path.basename(os.path.dirname(path)), text
    return None, None


def main():
    beat(MENTE, "gate-critical")   # proof this gate still fires (hooks/_beat.py)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0                                               # malformed input never blocks

    # Same defensive shape as pre-edit-standards.py — the payload comes from outside.
    # `body` matters too: a non-str would raise inside every regex below.
    if not isinstance(payload, dict):
        return 0
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return 0
    target = ti.get("file_path")
    if not isinstance(target, str) or not target:
        return 0
    body = ti.get("content") or ti.get("new_string") or ""
    if not isinstance(body, str):
        body = ""

    name, text = owning_block(target)

    # ── GATE 2 · 🔴 the database ────────────────────────────────────────────
    # The only mistake on this list with no undo. Blocks when a migration has no way back.
    #
    # Destructive SQL embedded in application code is the SAME damage without the filename:
    # measured 2026-07-30, the demo runs SQL from duenos.ts, eventos.ts and userStore.ts.
    # A gate that only reads filenames guards the paperwork, not the database.
    #
    # ⭐ EXCEPTION · an INTEGRATION TEST, and only if it proves where it points.
    # Added 2026-08-05, when the demo got its first tests. A test that writes to a real
    # database MUST clean up after itself — forbidding its DELETE would force either a
    # mocked db() (which tests the mock, not the brake — `val-functional.md` §2.3) or a
    # suite that leaves rows behind forever.
    #
    # ⚠️ The exemption is NOT "it is a test file". A test pointing at production is worse
    # than application code, because nobody reviews it before it runs. It is exempt only
    # when it reads a DEDICATED test connection variable — the same shape as the rule
    # `a default never points at something with an owner`. A test that reaches for the
    # production URL still gets blocked, which is the case worth catching.
    is_test = re.search(r"(^|/)(tests?|__tests__)/|\.(test|spec)\.[jt]sx?$", target)
    proves_target = re.search(r"DATABASE_URL_TEST|TEST_DATABASE_URL", body)
    test_exempt = bool(is_test and proves_target)

    embedded = (not DB_HINT.search(target)
                and not test_exempt
                and target.endswith((".ts", ".tsx", ".js", ".py"))
                and DESTRUCTIVE.search(body)
                and re.search(r"sql\s*[`(]|execute\s*\(|query\s*\(", body, re.I))
    if embedded:
        if is_test:
            print("🔴 BLOCKED · a test that runs destructive SQL must name its OWN database.\n"
                  "   Use DEMO_DATABASE_URL_TEST (or TEST_DATABASE_URL) and skip when it is "
                  "absent.\n"
                  "   Falling back to the production URL is how a test suite deletes real rows.\n",
                  file=sys.stderr)
            return 2
        print(f"🔴 BLOCKED · {os.path.basename(target)} runs destructive SQL from application "
              "code.\n"
              "   Same damage as a migration, without the filename that would have flagged it.\n"
              "   Put it in a migration with a rollback, or state in §G why it must live here.\n"
              "   Bypass: git commit --no-verify is NOT a bypass for this — the edit is blocked.",
              file=sys.stderr)
        return 2

    if DB_HINT.search(target):
        if DESTRUCTIVE.search(body) and not DOWN.search(body):
            print(f"🔴 BLOCKED · {os.path.basename(target)} destroys data with no rollback.\n"
                  "   A migration that cannot go back is the one mistake with no undo.\n"
                  "   Add a down/rollback section, or state in the block §G why it is one-way.\n"
                  "   Bypass: edit it outside this session, and log the reason in §H.",
                  file=sys.stderr)
            return 2
        if not DOWN.search(body) and len(body) > 80:
            print(f"⚠️  {os.path.basename(target)} declares no rollback — "
                  "`bin/grade-block` will count it as irreversible (type `data`).", file=sys.stderr)

    # ── GATE 3 · 🔴 closing a block ─────────────────────────────────────────
    # A block that closes without sufficiency is a block that cannot be restarted from disk —
    # which is the only reason blocks exist.
    # re.I: `status: CLOSED` in caps evaded the gate entirely (found adversarially, 2026-07-30).
    # Markdown is written by humans; a case-sensitive guard is a guard with a typo-sized hole.
    if target.endswith("BLOCK.md") and re.search(r"^status:\s*closed", body, re.M | re.I):
        bname = os.path.basename(os.path.dirname(target))
        import subprocess
        r = subprocess.run([f"{MENTE}/bin/check-sufficiency", bname],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"🔴 BLOCKED · block `{bname}` cannot close — it fails the sufficiency test.\n"
                  f"{r.stdout.strip()[-500:]}\n"
                  "   §A-E must answer the seven restart questions, or the next session after a\n"
                  "   /clear rebuilds the scope by inference — and sounds just as confident.\n"
                  "   Bypass: bin/check-sufficiency <block> and fix what it names.", file=sys.stderr)
            return 2
        # 🔴 BUG found by test ② (2026-07-30): this used `text` from owning_block(), which is
        # None for a BLOCK.md — a block does not declare its own file in its §B IN. So the
        # open-sub-block check silently never ran. Read the file being closed, directly.
        try:
            own = open(target, encoding="utf-8", errors="replace").read()
        except OSError:
            own = text or ""
        # ⚠️ La lista es una LISTA BLANCA de estados CERRADOS invertida, y por eso incluye
        # `pendiente`: el 2026-08-06 se escribió ese estado en el §F-11 de `demo` y la puerta
        # dejó pasar un cierre con trabajo abierto. **Un vocabulario nuevo abrió un agujero en
        # una puerta de seguridad**, y el fallo fue silencioso: exit 0 donde debía ser 2.
        # Regla que se deriva: cualquier palabra que no signifique CERRADO cuenta como abierta.
        if re.search(r"\|\s*(active|open|blocked|pendiente|pending|abierto|en curso)\s*\|",
                     own, re.I):
            print(f"🔴 BLOCKED · block `{bname}` still has open sub-blocks in §F.\n"
                  "   A parent does not close over unfinished children (block-lifecycle.md §5).",
                  file=sys.stderr)
            return 2

    # ── GATE 1 · ⚠️ a piece with declared dependents ────────────────────────
    # Deliberately a WARNING. Measured: 5 files edited constantly; the lane already covers it.
    if name and text:
        for row in re.finditer(r"^\|[^|]*\|([^|]*)\|([^|]*)\|\s*(\d+)\s*\|\s*(\w+)\s*\|",
                               text, re.M):
            piece = row.group(2).strip().strip("`")
            deps = int(row.group(3))
            if piece and len(piece) > 4 and piece in target and deps >= 5:
                print(f"⚠️  {piece} propagates to {deps} files — lane `full-block`.\n"
                      f"   Evaluate the construction before writing (rules/rule-fix-not-patch.md):\n"
                      f"   a fix that ignores {deps} consumers is a patch.", file=sys.stderr)
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())
