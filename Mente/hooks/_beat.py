"""_beat — every gate leaves proof it still fires.

F2 of the heartbeat plan. F1 covered `SessionStart`: the guard that reports every other guard
now stamps a date, so its silence became measurable. F2 covers the three gates themselves.

THE GAP IT CLOSES, and the evidence that made it worth building:
    On 2026-07-31 `gate-handoff` blocked three launches — proof it fires. But after editing
    dozens of files that same day there was NO way to tell whether `gate-critical` ran even
    once. A gate that stopped firing looks exactly like a gate with nothing to block.

WHY THIS DESIGN AND NOT THE OBVIOUS ONE:
    Measured on this session's own transcript: Write+Edit fired 97 times. Stamping on every
    call would mean ~194 disk writes per session on the hot path — and the project's own rule
    is that a gate costing more than it protects gets switched off.

    So the beat is written ONLY when the date changes: one write per gate per day, and a
    no-op read the other 96 times. The signal is identical (did this gate fire today?) at a
    fraction of the cost.

⛔ NEVER raises. A hook that crashes because its telemetry failed is worse than no telemetry:
   `pre-edit-standards` must never block, and `gate-critical` must block for its OWN reasons,
   never because a stamp could not be written.
"""
import os
from datetime import date, timezone, datetime


def beat(mente, name):
    """Stamp `mente/.beats/<name>` with today, only if it does not already say today."""
    try:
        today = datetime.now(timezone.utc).date().isoformat()
        d = os.path.join(mente, ".beats")
        p = os.path.join(d, name)
        # The read is the point: 96 of 97 calls stop here without touching the disk to write.
        try:
            if open(p, encoding="utf-8").read().strip() == today:
                return
        except OSError:
            pass
        os.makedirs(d, exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(today)
    except Exception:                                          # noqa: BLE001
        return          # telemetry never breaks the gate it is measuring


def last(mente, name):
    """The date a gate last fired, or None. Used by check-health, never by the hooks."""
    try:
        raw = open(os.path.join(mente, ".beats", name), encoding="utf-8").read().strip()
        return date.fromisoformat(raw)
    except (OSError, ValueError):
        return None
