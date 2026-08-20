#!/usr/bin/env python3
"""gate-accounts — la PUERTA de los repos: nada sale hacia un destino que nadie declaró.

⭐ POR QUÉ EXISTE, medido. El 2026-07-23 se empujó a `origin` y no a `backup`, y los dos
remotos quedaron divergentes **24 días sin que nada avisara**. Dos commits firmados vivieron
fuera de GitHub todo ese tiempo. La alarma llegó cuando un humano lo miró a mano.

⛔ Y el caso peor no es ese: es empujar a un repo que **no está en `cuentas.tsv`**. El trabajo
sale del sistema y nadie sabe adónde fue — un repo no registrado no tiene dueño declarado, ni
razón de existir, ni guía de acceso.

── LAS CUATRO RESPUESTAS ───────────────────────────────────────────────────────
| situación                                   | respuesta | por qué                        |
|---------------------------------------------|-----------|--------------------------------|
| push a un repo REGISTRADO                   | allow     | destino conocido y declarado   |
| push a un clon con 2 remotos, empujando a 1 | ask       | el bug del 23-jul, antes de él |
| push a un repo NO registrado                | deny      | fail-closed: destino sin dueño |
| crear / borrar / cambiar visibilidad        | ask       | ⛔ es decisión de Brian, no mía |

⚠️ ESTA PUERTA NO BLOQUEA LEER. `git fetch`, `clone` y `status` pasan intactos: leer no manda
trabajo a ningún sitio. Una puerta que estorba en lo cotidiano se termina desactivando, y una
puerta desactivada protege menos que no tenerla (`rules/rule-friction.md`).

Cuando bloquea, su mensaje ES el recibo (ADR-030): qué repo, por qué, y la salida exacta.

Exit: 0 con veredicto en stdout (contrato PreToolUse de Claude Code).
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, "cuentas.tsv")
COLS = ("repo", "cuenta", "rol", "remoto", "ruta_local", "por_que_existe", "guia")

# Lo que MANDA trabajo fuera. `fetch`, `pull`, `clone` y `status` no están aquí a propósito.
# ⚠️ Anclado al INICIO del comando o tras un separador (`&&`, `;`, `|`, `(`), nunca en medio:
# medido 2026-08-20, `echo "recuerda: git push origin main"` disparaba la puerta. Un aviso sobre
# un comando que nadie va a ejecutar es ruido, y el ruido enseña a ignorar los avisos de verdad.
PUSH = re.compile(r"""(?:^|[;&|(]\s*|\bbash\s+-c\s+["'])\s*\S*git\s+(?:-C\s+\S+\s+)?push\b""")
# Lo que crea, borra o expone un repo — irreversible o de cara al público.
REPO_ADMIN = re.compile(r"\bgh\s+repo\s+(create|delete|edit|archive|rename|transfer)\b")
# ⭐ La OTRA vía de escritura, encontrada en la auditoría adversarial 2026-08-20: `gh api` con un
# método de escritura empuja refs, crea releases y borra ramas SIN pasar por `git push`. La puerta
# la ignoraba por completo — un candado en la puerta principal con la ventana abierta.
GH_API_WRITE = re.compile(r"\bgh\s+api\b[^|;&]*(?:-X\s*(?:POST|PUT|PATCH|DELETE)|--method\s*(?:POST|PUT|PATCH|DELETE))")
# ⚠️ Borrar una rama remota NO es empujar trabajo: es destruirlo. Pasaba como un push normal.
PUSH_DELETE = re.compile(r"\bpush\b[^|;&]*(?:--delete\b|\s:\S)")


def verdict(decision, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    return 0


def rows():
    if not os.path.exists(REGISTER):
        return []
    out = []
    for raw in open(REGISTER, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in line.split("\t")]
        if len(cells) != len(COLS) or cells[0] == "repo":
            continue
        out.append(dict(zip(COLS, cells)))
    return out


def normalize(url):
    """https://github.com/owner/name.git y git@github.com:owner/name → owner/name.

    Ambas formas DEBEN colapsar a la misma clave o la puerta bloquea trabajo legítimo,
    que es la forma más rápida de que alguien la desactive.
    """
    m = re.search(r"(?:github\.com[:/])([^/\s]+/[^/\s]+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def remote_target(cmd, cwd):
    """¿A qué repo apunta este push? Devuelve (repo, nombre_del_remoto) o (None, None).

    Un `git push` sin nombre de remoto usa el upstream o `origin` — resolverlo mal aquí
    haría que la puerta juzgue un destino que no es el real.
    """
    m = re.search(r"\bpush\b((?:\s+--?\S+)*)\s+(\S+)", cmd)
    name = m.group(2) if m and not m.group(2).startswith("-") else "origin"
    if name.startswith("http") or name.startswith("git@"):
        return normalize(name), name          # push a una URL literal
    try:
        r = subprocess.run(["git", "-C", cwd, "remote", "get-url", name],
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return normalize(r.stdout.strip()), name
    except Exception:
        pass
    return None, name


def siblings(repo, data):
    """Otros remotos del MISMO clon. Es el bug del 23-jul: se empuja a uno y el otro se queda."""
    me = [r for r in data if r["repo"].lower() == repo.lower()]
    if not me or me[0]["ruta_local"] in ("-", ""):
        return []
    path = me[0]["ruta_local"]
    return [r for r in data if r["ruta_local"] == path and r["repo"].lower() != repo.lower()]


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    if payload.get("tool_name") != "Bash":
        return 0

    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(cmd, str) or not cmd:
        return 0

    if REPO_ADMIN.search(cmd):
        return verdict("ask",
                       "🏗️  Esta orden CREA, BORRA o CAMBIA LA VISIBILIDAD de un repositorio.\n"
                       "⛔ Eso es decisión de Brian, nunca automática — y varias no se deshacen.\n"
                       "Si es lo que quieres, apruébalo aquí.")

    if GH_API_WRITE.search(cmd):
        m = re.search(r"repos/([\w.-]+/[\w.-]+)", cmd)
        target = m.group(1) if m else "un repositorio"
        return verdict("ask",
                       f"🌐 `gh api` con método de ESCRITURA sobre `{target}`.\n"
                       f"Esta vía crea refs, releases y borra ramas sin pasar por `git push`, "
                       f"así que no puedo medirla como un push normal.\n"
                       f"Si es lo que quieres, apruébalo.")

    if not PUSH.search(cmd):
        return 0                      # leer no manda nada fuera: esta puerta no se mete

    if PUSH_DELETE.search(cmd):
        m = re.search(r"--delete\s+(\S+)", cmd)
        rama = m.group(1) if m else "una rama"
        return verdict("ask",
                       f"🗑️  Esto BORRA la rama remota `{rama}`.\n"
                       f"⛔ No es empujar trabajo: es destruirlo, y en el remoto no hay reflog.\n"
                       f"`rules/rule-post-merge-cleanup.md`: se borra tras VERIFICAR que su "
                       f"trabajo viajó — por contenido, nunca por la etiqueta MERGED.")

    data = rows()
    if not data:
        return verdict("ask",
                       f"⬜ `cuentas.tsv` está vacío o no existe, así que no puedo decir si el "
                       f"destino de este push está declarado.\n"
                       f"La salida: regístralo y corre `bin/check-accounts`.")

    cwd = (payload.get("cwd") or ROOT)
    m = re.search(r"\bgit\s+-C\s+(\S+)", cmd)
    if m:
        cwd = m.group(1)

    repo, name = remote_target(cmd, cwd)
    if not repo:
        return verdict("ask",
                       f"❓ No pude resolver a qué repositorio apunta el remoto `{name}`.\n"
                       f"⛔ No dejo pasar un push a un destino que no puedo medir.\n"
                       f"Compruébalo: `git -C {cwd} remote -v`")

    known = {r["repo"].lower(): r for r in data}
    if repo.lower() not in known:
        # 🔴 FAIL-CLOSED. La salida es registrarlo, nunca rodear la puerta.
        return verdict("deny",
                       f"🔴 `{repo}` NO está en `cuentas.tsv` — no dejo salir trabajo hacia ahí.\n\n"
                       f"Por qué: un repo no registrado no tiene dueño declarado, ni razón de "
                       f"existir, ni guía de acceso. Si el trabajo sale, nadie sabe adónde fue.\n\n"
                       f"La salida:\n"
                       f"  1. añade su fila a `cuentas.tsv` — con su `por_que_existe`\n"
                       f"  2. `bin/check-accounts`\n"
                       f"  3. repite el push")

    rest = siblings(repo, data)
    if rest:
        pushed = re.findall(r"\bpush\b(?:\s+--?\S+)*\s+(\S+)", cmd)
        missing = [s for s in rest if s["remoto"] not in pushed]
        if missing:
            lst = "\n".join(f"     git push {s['remoto']} <rama>   → {s['repo']}"
                            for s in missing)
            return verdict("ask",
                           f"⚠️  Este clon tiene MÁS DE UN REMOTO y solo estás empujando a "
                           f"`{name}`.\n\n"
                           f"Quedaría(n) atrás:\n{lst}\n\n"
                           f"Medido: el 2026-07-23 pasó exactamente esto y nadie lo notó en "
                           f"**24 días** — 2 commits firmados fuera de GitHub.\n"
                           f"Si es a propósito, apruébalo.")

    r = known[repo.lower()]
    return verdict("allow",
                   f"✅ `{repo}` registrado · cuenta `{r['cuenta']}` · rol `{r['rol']}`")


if __name__ == "__main__":
    sys.exit(main())
