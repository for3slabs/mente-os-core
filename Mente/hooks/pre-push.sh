#!/usr/bin/env bash
# pre-push — la SEGUNDA CAPA de la puerta de cuentas: la que no se puede rodear.
#
# ⭐ POR QUÉ EXISTE, medido 2026-08-20. `hooks/gate-accounts.py` lee el TEXTO del comando, así
# que basta no escribir literalmente "git push" para pasarlo. Se probaron 7 formas y **5 lo
# evadían**: un alias, una función de shell, una variable (`P=push; git $P`), `eval` y `xargs`.
# La deuda declarada decía "un alias"; la realidad era cinco.
#
# ⛔ LA LECCIÓN: un regex sobre texto NUNCA cubre todas las formas de invocar un comando. Da
# igual cuántos patrones se añadan — siempre queda una más. Por eso la defensa no puede vivir
# solo ahí.
#
# ⭐ ESTE hook lo ejecuta GIT, en el push real, con el remoto ya resuelto. No importa cómo se
# escribió el comando: alias, función, eval o xargs terminan invocando git, y git ejecuta esto.
# No hay texto que interpretar — hay un destino que verificar.
#
#   capa 1  gate-accounts.py   rápida, explica ANTES, y se puede rodear
#   capa 2  ESTA               no se rodea, pero solo habla en el momento del push
#
# Instalación: `bin/init` lo enlaza en .git/hooks/pre-push (y `bin/check-accounts` avisa si falta).
# Salida: 0 deja pasar · 1 ABORTA el push.
set -uo pipefail

REMOTE_NAME="${1:-}"
REMOTE_URL="${2:-}"
# ⚠️ Este hook se INVOCA desde .git/hooks/pre-push, normalmente un symlink. `BASH_SOURCE`
# resuelve entonces a .git/hooks/, no a Mente/hooks/ — medido 2026-08-20: el hook corría y
# reportaba "no hay cuentas.tsv" sobre un registro de 8 filas, dejando pasar TODO en silencio.
# ⭐ Un guardia que falla ABIERTO es peor que ninguno: da confianza sin dar protección.
# La raíz se pide a git, que siempre la conoce, con el symlink resuelto como respaldo.
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$ROOT" ]; then
  SELF="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}")"
  ROOT="$(cd "$(dirname "$SELF")/../.." && pwd)"
fi
REG="$ROOT/Mente/cuentas.tsv"

# Sin registro no hay nada que verificar: un clon recién nacido lo tiene vacío a propósito,
# y abortar ahí impediría el primer push de cualquiera. Avisa y deja pasar.
if [ ! -f "$REG" ]; then
  echo "⬜ pre-push: no hay cuentas.tsv — el destino no se verificó (corre Mente/bin/init)" >&2
  exit 0
fi

# owner/name, venga como venga la URL: https://github.com/o/n.git o git@github.com:o/n
REPO=$(printf '%s' "$REMOTE_URL" | sed -E 's|\.git$||; s|/$||' \
       | sed -nE 's|.*github\.com[:/]([^/]+/[^/]+)$|\1|p')

# Un remoto que no es de GitHub (una ruta local, un espejo) no lo gobierna este registro.
if [ -z "$REPO" ]; then
  exit 0
fi

if grep -qiE "^${REPO}[[:space:]]" "$REG"; then
  # ⚠️ El clon puede tener MÁS remotos declarados. Empujar a uno solo los deja divergentes:
  # es el defecto del 2026-07-23, que nadie notó en 24 días.
  MINE=$(grep -iE "^${REPO}[[:space:]]" "$REG" | cut -f5 | head -1)
  if [ -n "$MINE" ] && [ "$MINE" != "-" ]; then
    OTHERS=$(awk -F'\t' -v p="$MINE" -v r="$REPO" \
      '!/^#/ && NF==7 && $5==p && tolower($1)!=tolower(r) {print "     git push "$4" <rama>   → "$1}' "$REG")
    if [ -n "$OTHERS" ]; then
      echo "" >&2
      echo "⚠️  Este clon declara MÁS DE UN REMOTO y estás empujando solo a \`$REMOTE_NAME\`." >&2
      echo "   Quedaría(n) atrás:" >&2
      echo "$OTHERS" >&2
      echo "   Medido: el 2026-07-23 pasó esto y nadie lo notó en 24 días." >&2
      echo "" >&2
    fi
  fi
  exit 0
fi

# 🔴 FAIL-CLOSED. Aquí no se pregunta: git no tiene "ask". O pasa o se aborta, y ante un destino
# que nadie declaró la respuesta segura es abortar — el trabajo sigue en local, no se pierde.
cat >&2 <<MSG

🔴 PUSH ABORTADO — \`$REPO\` no está en cuentas.tsv

   Por qué: un repo no registrado no tiene dueño declarado, ni razón de existir,
   ni guía de acceso. Si el trabajo sale, nadie sabe adónde fue.

   ⭐ Esta es la capa que no se rodea: se dispara en el push real, así que un alias,
      una función, \`eval\` o \`xargs\` llegan igual hasta aquí.

   La salida:
     1. añade su fila a Mente/cuentas.tsv — con su \`por_que_existe\`
     2. Mente/bin/check-accounts
     3. repite el push

   Tu trabajo sigue en local: no se ha perdido nada.

MSG
exit 1
