"""mente_config — the ONE place that knows what is instance-specific.

⭐ The line this draws (Brian, 2026-07-31): the ENGINE is universal and cloned as-is; the
INSTANCE is declared once in `mente.config.yml`. A new user edits that file and nothing else.

WHY THIS EXISTS, measured 2026-07-31: four validators carried the literal string
`~/.claude/projects/-home-brianweb3-for3s`, and each failed SILENTLY when it did not resolve
(`if not js: return`). On any other machine the session watch — the guard that exists BECAUSE
of the 21-jul incident — would simply go quiet. A guard aimed at a path that does not exist is
not a guard; it is a green light. Hence `session_dir()` returns a reason when it finds nothing,
so the caller can SAY SO instead of returning early.

⛔ No PyYAML. A dependency that must be installed is a system that does not run on clone — and
this file exists precisely so cloning works. The config subset is fixed and small, so it is
parsed directly.

Usage:
    from mente_config import CONFIG, session_dir, gates, siblings
"""
import os
import re
import glob

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(MENTE)
CONFIG_PATH = os.path.join(MENTE, "mente.config.yml")


def _parse(path):
    """Parse the config subset: top-level keys, one level of nesting, and lists.

    Deliberately NOT a general YAML parser. It handles exactly the three shapes the config
    file uses — `key: value`, a nested block of `key: value`, and a list of either scalars or
    one-level mappings — because a hand-rolled general parser is a bug generator.

    🔴 The first version tried to decide "mapping or list?" while walking, using a stack and a
    sentinel key. It was unreadable and had an UnboundLocalError on its first run. Rewritten to
    the obvious two-level walk: this config is two levels deep, so the parser is too.
    """
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        return {}

    out, key, block, items = {}, None, None, None

    def flush():
        if key is None:
            return
        if items:
            out[key] = items
        elif block is not None:
            out[key] = block

    for raw in lines:
        line = raw.split(" #")[0].rstrip() if " #" in raw else raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()

        if indent == 0:                                   # a new top-level key closes the last
            flush()
            key, block, items = None, None, None
            k, _, v = s.partition(":")
            k, v = k.strip(), v.strip()
            if v == "":
                key, block, items = k, {}, []
            elif v.startswith("["):
                inner = v.strip("[]").strip()
                out[k] = [_scalar(x.strip()) for x in inner.split(",")] if inner else []
            else:
                out[k] = _scalar(v)
            continue

        if key is None:
            continue

        if s.startswith("- "):                            # a list entry under the current key
            item = s[2:].strip()
            if ":" in item and not item.startswith(('"', "'")):
                k, _, v = item.partition(":")
                items.append({k.strip(): _scalar(v.strip())})
            else:
                items.append(_scalar(item))
            continue

        k, _, v = s.partition(":")
        k, v = k.strip(), v.strip()
        if items and isinstance(items[-1], dict) and indent >= 4:
            items[-1][k] = _scalar(v)                     # continuation of the last list entry
        elif v.startswith("["):
            inner = v.strip("[]").strip()
            block[k] = [_scalar(x.strip()) for x in inner.split(",")] if inner else []
        else:
            block[k] = _scalar(v)

    flush()
    return out


def _scalar(v):
    v = v.strip().strip('"').strip("'")
    if v in ("null", "~", ""):
        return None
    if v in ("true", "True"):
        return True
    if v in ("false", "False"):
        return False
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


CONFIG = _parse(CONFIG_PATH)


def _get(path, default=None):
    node = CONFIG
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return default if node is None else node


def session_slug():
    """Claude Code's transcript folder name: the working directory with `/` → `-`.

    COMPUTED, not stored. Hardcoding it is what made four guards machine-specific.
    """
    override = _get("session.project_dir")
    if override:
        return override
    return REPO.replace("/", "-")


def session_dir():
    """(path, reason). `reason` is None when transcripts were found.

    🔴 Returns a REASON instead of nothing, so a caller can report the gap out loud. The old
    code did `if not js: return` — the guard vanished without a word.
    """
    d = os.path.expanduser(f"~/.claude/projects/{session_slug()}")
    if not os.path.isdir(d):
        return d, f"no transcript directory at {d} — session watch is blind"
    if not glob.glob(f"{d}/*.jsonl"):
        return d, f"{d} has no .jsonl transcripts yet"
    return d, None


def session_files():
    """Transcripts, newest first. Empty list when there are none — check session_dir() first."""
    d, why = session_dir()
    if why:
        return []
    return sorted(glob.glob(f"{d}/*.jsonl"), key=os.path.getmtime, reverse=True)


def gates():
    """[(expanded_path, why)] — trees the AI must not read without explicit permission."""
    out = []
    for g in _get("gates", []) or []:
        if isinstance(g, dict) and g.get("path"):
            out.append((os.path.expanduser(g["path"]), g.get("why", "")))
    return out


def siblings():
    """Absolute paths of repos beside Mente/ whose uncommitted state is worth reporting."""
    return [os.path.join(REPO, s) for s in (_get("siblings", []) or [])]


def outside():
    return list(_get("outside", []) or [])


def owner_name():
    return _get("owner.name", "the owner")


def thresholds():
    return (_get("session.size_warn_mb", 15),
            _get("session.size_red_mb", 50),
            _get("session.heavy_mb", 2))
