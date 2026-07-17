# Análisis: el LEARNING LOOP de Hermes (skills auto-generables) → adaptar a For3s

> Fase A (análisis, Brian 2026-06-24): descomponer cómo Hermes (NousResearch) implementa
> su "joya" — skills auto-generables / learning loop — en su CÓDIGO REAL, para adaptarlo
> a For3s como CÓDIGO PROPIO (= H10-H12). NO copia: aprender. Repo clonado /tmp/hermes-agent.
> Archivos analizados: learn_prompt.py, curator.py, background_review.py, skills_guard.py,
> skill_provenance.py, skills_tool.py (~14.700 líneas en el sistema de skills total).

---

## 0. El hallazgo MARCO (tranquilizador)

La arquitectura del learning loop de Hermes es **sorprendentemente CERCANA a lo que For3s
ya tiene** (H5/H6/H8). No es magia inalcanzable; son patrones que ya dominamos, aplicados a
"el agente escribe sus propias skills". Varios componentes tienen **gemelo directo** en For3s.

---

## 1. Cómo funciona el learning loop de Hermes (las 5 piezas)

### Pieza 1 — `/learn` (crear skill bajo demanda) · `learn_prompt.py`
- **NO hay motor de destilación separado.** `/learn` construye UN PROMPT que instruye al
  AGENTE VIVO a: (1) juntar las fuentes (con sus tools normales: read_file, web_extract, la
  conversación actual), (2) escribir UN SKILL.md vía la tool `skill_manage`.
- Lleva embebidos los "authoring standards" (formato del SKILL.md, secciones, "no inventes
  flags/APIs que no viste"). El agente autoría como lo haría un humano mantenedor.
- **Clave:** reusa el toolset existente → funciona igual en cualquier backend. Elegante y simple.

### Pieza 2 — auto-mejora tras cada turno · `background_review.py`
- Tras cada turno, opcionalmente forkea el agente (daemon thread) que **se pregunta a sí mismo**
  "¿debería guardar/actualizar alguna skill o memoria?". Escribe directo a los stores.
- **El fork NO toca la conversación principal ni el prompt cache.** Hereda el runtime (provider/
  modelo/credenciales) → mismo prefix cache. Corre con **whitelist de tools** (solo memoria +
  skills; todo lo demás denegado en runtime).

### Pieza 3 — curación periódica · `curator.py`
- Tarea de modelo AUXILIAR que de noche/por inactividad revisa las skills auto-creadas:
  auto-transición de lifecycle (active→stale→archived por timestamps), pin/archive/consolidate/
  patch. **Invariantes estrictos:** solo toca skills AUTO-creadas; NUNCA borra (solo archiva,
  recuperable); pinned se saltan todo; usa cliente auxiliar (no el cache principal).

### Pieza 4 — seguridad (el FRENO) · `skills_guard.py`
- Scanner de seguridad para skills externas: regex anti-patrones (exfiltración, prompt-injection,
  comandos destructivos, persistencia) + política por **trust level** (builtin/trusted/community).
  community con cualquier hallazgo = bloqueado salvo --force.

### Pieza 5 — trazabilidad · `skill_provenance.py`
- Un **ContextVar** marca si una skill se creó en el fork de auto-mejora ("background_review")
  vs por el usuario ("foreground"). El curator SOLO gestiona las auto-creadas; las del usuario
  son intocables. Distingue "sedimento del agente" de "lo que pidió el usuario".

---

## 2. ⭐ GEMELOS en For3s (lo que YA tenemos del patrón)

| Pieza de Hermes | Gemelo en For3s | Estado |
|---|---|---|
| curator (revisión nocturna por inactividad, cliente aux, nunca borra) | **CLS + Microglía (H6)** — consolida/olvida de noche, soft-delete recuperable | ✅ idéntico patrón |
| background_review (fork aislado, no toca cache, whitelist tools) | **specialists/equipo (H8)** — corre aislado, whitelist, mutation guard | ✅ patrón ya usado |
| skill_provenance (ContextVar foreground vs auto) | **_ctx_specialist (H8 S9)** — ContextVar de aislamiento | ✅ MISMO mecanismo |
| skills_guard (freno/governor antes de instalar) | **Meta-Orchestrator R6 (governor 6 frenos)** | ⬜ diseñado, no construido |
| /learn (prompt que instruye al agente a autoría) | (nada aún) | ⬜ |
| skill_manage (crear/editar SKILL.md en disco) | (nada aún) | ⬜ |

**Conclusión:** For3s tiene ~3 de las 5 piezas como PATRÓN (de H6/H8). Faltan: el motor de
autoría (/learn + skill_manage) y el governor construido (R6).

---

## 3. Qué adaptar a For3s (H10-H12) — diseño preliminar

> ⚠️ REGLA LOCKED de For3s (R6, Grafo §8.4): **el GOVERNOR/freno (H11) debe existir ANTES
> del motor de auto-generación (H12)**. Hermes lo confirma: su skills_guard es el freno.

Ruta sugerida (respeta el orden sagrado H10→H11→H12):
1. **H10 — Skills básicas (almacenamiento + ejecución manual):** estructura de skill (un .md +
   scripts), tool `skill_manage` (crear/listar/ver), que el agente las pueda USAR. Sin auto-gen aún.
2. **H11 — GOVERNOR (el freno):** el Meta-Orchestrator R6 — scanner de seguridad (estilo
   skills_guard: anti-patrones + trust level) + lifecycle + provenance (ContextVar foreground vs
   auto). NADA se auto-genera sin pasar por aquí.
3. **H12 — MOTOR de auto-generación:** `/learn` (prompt que instruye al propio For3s a destilar
   una skill de la conversación/fuentes con sus tools) + auto-mejora en background (reusa el
   patrón de H6 nocturno + H8 fork aislado) + curación (reusa CLS/Microglía).

**Lo que For3s reusaría (no construir de cero):** el ciclo nocturno (H6), el fork aislado +
ContextVar + whitelist (H8), el soft-delete recuperable (H6 Microglía). El learning loop es
"H6+H8 aplicados a skills" + el governor R6 + el motor /learn.

---

## 4. Esfuerzo y riesgo (honesto)

- **Grande** (es un hito completo, H10-12), pero NO partimos de cero: ~60% del patrón ya existe.
- **Delicado**: un agente que escribe y ejecuta su propio código. Por eso el governor PRIMERO.
- **No urgente**: Brian dijo Bloque 3 (producto) "aún no, falta pulir". H10-12 es aún más grande.
  Conviene tenerlo ANALIZADO (este doc) y construirlo cuando el resto esté pulido.

## 5. Veredicto

Sí, se puede adaptar (como intern-os) — y mejor de lo esperado: For3s ya tiene el grueso del
patrón (memoria nocturna H6 + fork aislado H8 + ContextVar). El learning loop de Hermes
"valida" el diseño R6 de For3s. Falta: el governor construido + el motor /learn + skill_manage.
Es el camino H10→H11→H12, con el orden LOCKED (freno antes que motor).

> Repo: github.com/NousResearch/hermes-agent (MIT). Análisis privado en Mente OS; nunca en
> código distribuible de For3s.
