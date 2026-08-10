#!/usr/bin/env python3
"""watch-prs — avisa de un merge de Brian ANTES de que yo toque git, sin preguntarle.

⭐ Brian, 2026-08-08: *"crea algo que permita que tú sepas cuándo yo ya lo mergeé… sin la
necesidad de estar preguntando o esperando mi respuesta. A lo mejor se me olvida decirte, pero
sí lo hice."*

EL HUECO QUE CIERRA, medido: `bin/check-prs` ya corre en el SessionStart, pero el caso real de
Brian es OTRO — mergea **a mitad de sesión**, cuando el arranque ya pasó. Entonces yo sigo
trabajando sobre una rama que ya está mergeada, y lo descubro preguntando… o no lo descubro.

CUÁNDO MIRA
    Antes de un comando `git` que empuja, ramifica o commitea. Ese es el momento en que un merge
    ajeno cambia lo que debería hacer: si mi rama ya se mergeó, no toca empujar — toca verificar
    que viajó y borrarla (`rules/rule-post-merge-cleanup.md`).

⛔ POR QUÉ NO ES UN CRON, otra vez: un cron dispara cuando no hay nadie escuchando. Este hook
dispara **cuando estoy a punto de hacer algo que el merge invalida**, que es el único instante
en que el aviso sirve para algo.

⛔ NUNCA BLOQUEA. Informa y deja pasar: un aviso que corta el trabajo se desactiva a la semana.

Salida: JSON de hookSpecificOutput con `permissionDecision: allow` y el aviso en su razón,
o silencio si no hay novedad.
"""
import os
import re
import sys
import json
import subprocess

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Comandos que cambian lo que un merge ajeno vuelve obsoleto. Un `git status` o un `git log`
# no necesitan aviso: no deciden nada.
ACCIONA = re.compile(r"\bgit\s+(push|checkout\s+-b|switch\s+-c|commit|merge|rebase)\b")


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0                                   # entrada ilegible: callar, nunca estorbar

    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if not ACCIONA.search(cmd):
        return 0

    try:
        r = subprocess.run([os.path.join(MENTE, "bin", "check-prs"), "--quiet"],
                           capture_output=True, text=True, timeout=20)
    except Exception:                                          # noqa: BLE001
        return 0                                   # sin red o sin `gh`: no es motivo de ruido

    if r.returncode != 1:                          # 0 = sin novedad · 2 = no se pudo consultar
        return 0

    # Hay algo accionable. Se pide el detalle para que el aviso diga QUÉ, no solo que "algo pasó".
    try:
        d = subprocess.run([os.path.join(MENTE, "bin", "check-prs")],
                           capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:                                          # noqa: BLE001
        d = ""

    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason":
            "🔀 Cambió el estado de un PR desde la última mirada:\n" + d +
            "\n→ rules/rule-post-merge-cleanup.md: verifica que el trabajo viajó antes de borrar."
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())