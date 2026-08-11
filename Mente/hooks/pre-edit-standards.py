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


def campana_de(bloque):
    """La campaña a la que pertenece un bloque, y los estándares que hereda de ella.

    Devuelve (nombre_campaña, [estándares]) o (None, []).

    ⭐ La pertenencia la declara la CAMPAÑA en su §E, no el bloque. Así un bloque no puede
    auto-adscribirse para heredar estándares más laxos —no los hay: solo se AÑADE— ni quedar
    huérfano por olvidarse de declararlo: si la campaña no lo lista, no pertenece.

    ⛔ Nunca lanza. Un hook que revienta deja al editor sin ningún estándar, que es peor que
    inyectar de menos: el fallo sería silencioso y parecería que no había nada que decir.
    """
    try:
        for cpath in glob.glob(os.path.join(MENTE, "campaigns", "*", "CAMPAIGN.md")):
            txt = open(cpath, encoding="utf-8", errors="replace").read()
            bloques = re.search(r"##\s*Blocks\s*\n((?:.*\n)+?)(?=\n##|\Z)", txt)
            if not bloques or bloque not in bloques.group(1):
                continue
            std = re.search(r"##\s*Standards\s*\n((?:\s*-.*\n)+)", txt)
            return (os.path.basename(os.path.dirname(cpath)),
                    re.findall(r"-\s*(\S+)", std.group(1)) if std else [])
    except Exception:                                          # noqa: BLE001
        pass
    return (None, [])


def main():
    beat(MENTE, "pre-edit-standards")   # proof this gate still fires (hooks/_beat.py)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0                                               # malformed input never blocks

    # 🔴 `json.load` acepta CUALQUIER JSON válido, no solo un objeto: con `[]` o `null` el
    # try/except de arriba no salta —el parseo tuvo éxito— y `.get()` reventaba con
    # AttributeError. Cazado por la auditoría del 2026-08-06; los otros tres hooks
    # (gate-critical, gate-handoff, gate-secrets) ya comprobaban el tipo. Este era el único.
    # ⚠️ Un hook que lanza una excepción no protege: imprime un traceback y deja pasar.
    if not isinstance(payload, dict):
        return 0
    ti = payload.get("tool_input")
    target = ti.get("file_path", "") if isinstance(ti, dict) else ""
    if not target:
        return 0

    for bpath in glob.glob(f"{MENTE}/blocks/active/*/BLOCK.md"):
        try:
            text = open(bpath, encoding="utf-8", errors="replace").read()
        except OSError:
            continue

        # §B IN declares the block's territory.
        #
        # 🔴 MENCIONAR UNA RUTA NO ES RECLAMARLA (2026-08-07). Dos defectos en el mismo sitio:
        #
        #   1. `re.findall` barría la línea ENTERA, así que una ruta citada en la explicación
        #      contaba igual que la declarada. El bloque `separacion-motor-instancia` nombró
        #      `marca-personal/` **sólo para decir de quién NO era** —"las rutas de los hooks las
        #      cerró tal bloque"— y el hook le atribuyó los archivos de `demo`.
        #      ⚠️ Con dos bloques activos, el que más EXPLICA se roba los archivos del otro,
        #      y el editor recibe los estándares equivocados: el daño no es un aviso de más,
        #      es el aviso CORRECTO que ya no llega.
        #      → Ahora solo cuenta el primer token del ítem: `- ruta/…`. Lo que va después de
        #        la ruta es prosa, y la prosa explica, no reclama.
        #
        #   2. `d in target` era SUBCADENA, no ruta: `lib/demo` casaba dentro de
        #      `otro-lib/demo-viejo/x.ts`. Ahora se compara por SEGMENTOS, así que un prefijo
        #      a medias de un nombre de carpeta ya no engancha.
        m = re.search(r"##\s*✅?\s*IN\s*\n((?:\s*-.*\n)+)", text)
        if not m:
            continue
        # ⚠️ Un ítem puede declarar VARIAS rutas separadas por `·` — `bin/a · bin/b · bin/c`.
        # La primera versión de este arreglo solo leía la primera y perdía las otras dos
        # (medido: `bin/init` dejó de reconocerse). Se toma el tramo del ítem ANTERIOR al
        # primer guion largo, que es donde empieza la explicación en prosa, y dentro de ese
        # tramo cuentan todas las rutas.
        seg = [s for s in target.split("/") if s]
        owned = False
        for linea in m.group(1).splitlines():
            cuerpo = re.match(r"\s*-\s*(.*)", linea)
            if not cuerpo:
                continue                       # continuación de línea: no declara nada nuevo
            decl = cuerpo.group(1).split("—")[0]          # la prosa empieza tras el guion largo
            for tok in re.findall(r"[\w./-]+/[\w./*-]*", decl):
                d = tok.split("*")[0].rstrip("/")
                if len(d) <= 4:
                    continue
                partes = [s for s in d.split("/") if s]
                if any(seg[i:i + len(partes)] == partes for i in range(len(seg))):
                    owned = True
                    break
            if owned:
                break
        if not owned:
            continue

        std = re.search(r"##\s*Required standards\s*\n((?:\s*-.*\n)+)", text)
        name = os.path.basename(os.path.dirname(bpath))
        propios = re.findall(r"-\s*(\S+)", std.group(1)) if std else []

        # ⭐ HERENCIA DE CAMPAÑA (2026-08-10, fase C2 de docs/plans/PLAN-campana.md).
        # Brian: "todos los códigos van a ser revisados con los mismos estándares."
        # 🔴 El defecto que cierra: este hook inyectaba SOLO el §D del bloque dueño, así que dos
        # bloques hermanos con §D distintos juzgaban el mismo código con dos varas.
        # ⛔ Se HEREDA, no se copia: los estándares se LEEN de la campaña en cada edición. Si se
        # copiaran al hijo, las dos listas divergirían — el defecto de las tablas de decisiones
        # duplicadas (75 filas contra 37). La prueba que lo distingue: quitar un estándar de la
        # CAMPAÑA debe quitarlo de todos los hijos.
        # ⚠️ Un hijo puede AÑADIR, nunca quitar (rules/rule-inheligence → rule-inheritance.md).
        campana, heredados = campana_de(name)
        lines = [f"📦 {target} belongs to block `{name}` — §D standards apply:"]
        if campana:
            lines[0] = (f"📦 {target} → block `{name}` · campaign `{campana}` — "
                        "standards apply (campaign first, block adds):")
            for s in heredados:
                lines.append(f"   · {s}   ⬅ heredado de la campaña")
        for s in propios:
            if s not in heredados:
                lines.append(f"   · {s}")
        if not propios and not heredados:
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
