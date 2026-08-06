#!/usr/bin/env python3
"""gate-secrets — la PUERTA de `Mente/secrets/`: deja LEER con permiso, nunca escribir en silencio.

⭐ Sustituye a un `deny` que era técnicamente perfecto y operativamente inservible: `secrets/`
era inalcanzable, así que Mente OS no podía entrar al servidor ni añadir el secreto de un
servidor nuevo. Este hook cambia *imposible* por *posible, con permiso y con registro*.

── LAS TRES RESPUESTAS ─────────────────────────────────────────────────────────
| situación                       | respuesta | por qué                                    |
|---------------------------------|-----------|--------------------------------------------|
| LEER con permiso vivo           | allow     | el permiso se concedió al cargar el contexto |
| LEER sin permiso                | ask       | el contexto no se ha cargado: que Brian decida |
| ESCRIBIR / BORRAR (siempre)     | ask       | ⛔ crear o cambiar un secreto NUNCA es automático |

El permiso lo emite `bin/secrets-lease`, llamado desde el arranque. **Nace con el contexto y
muere cuando el contexto se recarga** — no hay reloj: la caducidad es de caché, no de minutos.

⚠️ **Esto NO es levantar el deny por comodidad** (`PROJECT-RULES.md` §3). La escritura sigue
preguntando siempre, y **toda** operación queda en `secrets/.access-log.md` — algo que el `deny`
no hacía, porque un acceso que no ocurre tampoco se registra. En ese punto esto es más estricto
que antes: hoy no existe ninguna bitácora.

Exit: 0 con veredicto en stdout (JSON del contrato PreToolUse).
"""
import json
import os
import re
import subprocess
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEASE_BIN = os.path.join(MENTE, "bin", "secrets-lease")

# Rutas que este hook gobierna. Se compara sobre la ruta RESUELTA, nunca sobre el texto:
# un `../` o un enlace simbólico burlan una comparación de cadenas (patrón de `bin/migrate-doc`,
# tomado de graphify #3 el 2026-08-05).
SECRETS_DIR = os.path.realpath(os.path.join(MENTE, "secrets"))

ESCRITURA = ("Write", "Edit", "NotebookEdit")


def veredicto(decision, razon):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": razon,
        }
    }))
    return 0


def apunta_a_secrets(payload):
    """¿Esta llamada toca secrets/? Devuelve la ruta si sí, None si no.

    Cubre las dos vías: una ruta de archivo (Read/Write/Edit) y un comando de shell que
    mencione el directorio (Bash). La segunda es tosca a propósito — `deny` compara el TEXTO
    del comando, así que un `"$(...)"` se le cuela, y está escrito en `docs/WORKSPACE.md`.
    Aquí no se pretende sellar esa vía: se pretende que el camino NORMAL quede registrado."""
    ti = payload.get("tool_input") or {}
    ruta = ti.get("file_path") or ti.get("notebook_path")
    if isinstance(ruta, str) and ruta:
        real = os.path.realpath(ruta)
        if real == SECRETS_DIR or real.startswith(SECRETS_DIR + os.sep):
            return real
    cmd = ti.get("command")
    if isinstance(cmd, str) and re.search(r"(^|[\s/'\"])Mente/secrets/|(^|\s)secrets/", cmd):
        return "(comando shell)"
    return None


def hay_permiso():
    try:
        return subprocess.run([LEASE_BIN, "check"], capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        # 🔴 FAIL-CLOSED. Si el otorgante no responde, NO se concede: un permiso por avería
        # es exactamente el fallo que el `deny` existía para impedir.
        return False


def anotar(op, ruta, motivo):
    try:
        subprocess.run([LEASE_BIN, "log", op, ruta, motivo], capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        pass   # ⛔ la bitácora nunca bloquea el trabajo


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0

    ruta = apunta_a_secrets(payload)
    if not ruta:
        return 0                       # no es asunto de esta puerta

    herramienta = payload.get("tool_name", "?")

    # ── ESCRITURA · siempre pregunta, tenga permiso o no ─────────────────────
    if herramienta in ESCRITURA:
        anotar("write?", ruta, f"{herramienta} — pendiente de aprobación")
        return veredicto("ask",
                         f"✍️  {herramienta} sobre `{os.path.basename(ruta)}` en secrets/.\n"
                         "Crear o cambiar un secreto NUNCA es automático, ni con permiso vivo.\n"
                         "Queda anotado en secrets/.access-log.md pase lo que pase.")

    # ── LECTURA · depende del permiso ────────────────────────────────────────
    if hay_permiso():
        anotar("read", ruta, "permiso vivo (concedido al cargar el contexto)")
        return veredicto("allow",
                         f"🔑 permiso de secrets VIVO — lectura de `{os.path.basename(ruta)}` "
                         "registrada en secrets/.access-log.md")

    anotar("read?", ruta, "sin permiso — pendiente de aprobación")
    return veredicto("ask",
                     f"🔒 sin permiso vivo para leer `{os.path.basename(ruta)}`.\n"
                     "El permiso se emite solo al cargar el contexto (bin/secrets-lease).")


if __name__ == "__main__":
    sys.exit(main())