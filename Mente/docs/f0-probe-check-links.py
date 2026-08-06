#!/usr/bin/env python3
"""F0 · ¿el índice responde EXACTAMENTE lo mismo que el glob recursivo?

⛔ NO toca bin/check-links. Carga sus funciones reales y compara las dos estrategias
   sobre TODAS las citas que hoy llegan a la rama cara.

Regla que debe preservarse literal: un nombre desnudo se perdona SOLO si el repo hermano
contiene EXACTAMENTE UN archivo con ese nombre. Dos coincidencias = cita ambigua = defecto.
"""
import os
import re
import sys
import glob
import time
import importlib.util as iu

MENTE = "/home/brianweb3/for3s/Mente"
os.chdir(MENTE)
sys.path.insert(0, "bin")

# ── cargar el validador REAL sin ejecutarlo ────────────────────────────────────
src = open("bin/check-links", encoding="utf-8").read()
# cortar antes de main() para que no corra al importar
head = src.split("\ndef main(")[0]
mod = {"__name__": "cl_probe", "__file__": os.path.join(MENTE, "bin", "check-links")}
exec(compile(head, "bin/check-links", "exec"), mod)

cited = mod["cited"]
in_sibling_repo_GLOB = mod["in_sibling_repo"]   # el método ACTUAL, tal cual
OUTSIDE = mod["OUTSIDE"]

print(f"repos 'outside': {OUTSIDE}\n")

# ── la alternativa: un índice {nombre: [rutas]} por repo ──────────────────────
_IDX = {}


def _index(repo):
    if repo in _IDX:
        return _IDX[repo]
    root = os.path.join("..", repo.rstrip("/"))
    d = {}
    if os.path.isdir(root):
        for dp, dn, fn in os.walk(root):
            # 🔴 glob NO desciende a directorios ocultos; os.walk SÍ. Medido 2026-08-05:
            # 6,036 archivos de diferencia. Sin podarlos, el índice vería `layout.md` dos
            # veces (una en .claude/) y lo declararía ambiguo cuando el glob lo perdona.
            # Un cambio de rendimiento que altera el veredicto es el fallo del v1.
            dn[:] = [x for x in dn if not x.startswith(".")]
            for n in fn:
                if n.startswith("."):
                    continue
                d.setdefault(n, []).append(os.path.join(dp, n))
    _IDX[repo] = d
    return d


def in_sibling_repo_INDEX(c):
    """Misma semántica, otra estructura de datos. Rama con '/' idéntica a la actual."""
    for repo in OUTSIDE:
        root = os.path.join("..", repo.rstrip("/"))
        if "/" in c:
            if os.path.exists(os.path.join(root, c)):
                return True
            continue
        if len(_index(repo).get(c, [])) == 1:
            return True
    return False


# ── recoger TODAS las citas tal como las ve el validador ─────────────────────
files = [f for f in glob.glob("**/*.md", recursive=True)]
files += [p for p in ("../CLAUDE.md", "../PROJECT-RULES.md") if os.path.exists(p)]

todas = set()
for f in files:
    try:
        todas |= cited(open(f, encoding="utf-8", errors="replace").read())
    except OSError:
        continue

# la rama cara es la que consulta repos hermanos: toda cita que no resuelve en el árbol local
candidatas = sorted(c for c in todas if not os.path.exists(c))
bare = [c for c in candidatas if "/" not in c]
slash = [c for c in candidatas if "/" in c]

print(f"citas totales extraídas: {len(todas)}")
print(f"  · no resuelven localmente: {len(candidatas)}")
print(f"      - de nombre desnudo (rama CARA): {len(bare)}")
print(f"      - con '/' (rama barata):        {len(slash)}\n")

# ── comparar, una por una ────────────────────────────────────────────────────
t0 = time.time()
resp_glob = {c: in_sibling_repo_GLOB(c) for c in candidatas}
t_glob = time.time() - t0

_IDX.clear()
t0 = time.time()
resp_idx = {c: in_sibling_repo_INDEX(c) for c in candidatas}
t_idx = time.time() - t0

same = [c for c in candidatas if resp_glob[c] == resp_idx[c]]
diff = [c for c in candidatas if resp_glob[c] != resp_idx[c]]

print("═══ RESULTADO F0 ═══")
print(f"  same={len(same)}  diff={len(diff)}")
print(f"\n  tiempo glob (actual): {t_glob:6.2f}s")
print(f"  tiempo índice:        {t_idx:6.2f}s")
if t_idx > 0:
    print(f"  factor:               {t_glob / t_idx:6.1f}x más rápido")

perdonadas = [c for c in candidatas if resp_glob[c]]
print(f"\n  citas que el glob PERDONA hoy: {len(perdonadas)}")

if diff:
    print(f"\n🔴 {len(diff)} DIFERENCIA(S) — el plan se detiene aquí:")
    for c in diff:
        print(f"     {c}: glob={resp_glob[c]}  índice={resp_idx[c]}")
    sys.exit(1)

# ── F0-bis · ⭐ LA PRUEBA QUE DISCRIMINA ─────────────────────────────────────
# 🔴 Encontrado al sabotear la sonda: relajar el criterio de `== 1` a `>= 1` NO cambiaba
#    ni una respuesta sobre las 626 citas reales, porque solo UNA (`SKILL.md`) es ambigua
#    y un repo anterior ya la resolvía. Una comparación que no distingue los dos criterios
#    es un verde vacío — exactamente lo que val-functional.md §2.2 condición 3 prohíbe.
#    Estos nombres SÍ discriminan: son ambiguos y solo existen en marca-personal.
print("\n── F0-bis · nombres que DISCRIMINAN ==1 de >=1 ──")
disc = ["layout.md", "readme.md", "HISTORY.md"]
fallos = 0
for c in disc:
    g = in_sibling_repo_GLOB(c)
    i = in_sibling_repo_INDEX(c)
    n = len(_index("marca-personal").get(c, []))
    marca = "✅" if g == i else "🔴"
    print(f"  {marca} {c:<14} coincidencias={n:<4} glob={g}  índice={i}")
    if g != i:
        fallos += 1
    # el criterio: >1 coincidencia debe RECHAZARSE. ==1 se perdona (y es correcto).
    if n > 1 and i is not False:
        print(f"     🔴 {n} coincidencias y el índice PERDONA — criterio `==1` roto")
        fallos += 1
if fallos:
    print(f"\n🔴 F0-bis FALLA — el índice no preserva el criterio de ambigüedad")
    sys.exit(1)
print("  → ambos RECHAZAN los ambiguos: el criterio `== 1` se preserva")

print("\n✅ 0 diferencias + criterio de ambigüedad preservado.")
sys.exit(0)
