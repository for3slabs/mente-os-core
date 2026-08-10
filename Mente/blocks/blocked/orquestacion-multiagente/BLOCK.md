# BLOCK · orquestacion-multiagente

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-orquestacion-multiagente-2026-08
type: infra
intent: gobernar VARIOS agentes trabajando a la vez, sin que se pisen — en Mente OS v2 y en For3s OS
status: blocked · lane: full-block · owner: brian
created: 2026-08-10 · updated: 2026-08-10

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- `Mente/rules/` — el vocabulario que hoy no existe: propiedad de archivos · olas · ledger
- `Mente/bin/` `Mente/hooks/` — los mecanismos que lo hagan cumplir
- `Mente/principles/` — el criterio de Brian sobre qué puerta es HUMANA y cuál AUTOMÁTICA
- ⭐ **For3s OS** (repo `for3slabs/for3s-os`) — su motor multi-agente ya existe (H8: 5
  specialists + Synthesizer) y **hoy no comparte vocabulario con Mente OS**

## ⛔ OUT
- ⛔ **NO se diseña todavía.** Brian, 2026-08-10: *"no lo vamos a diseñar ahorita, va a estar
  bloqueado, pero sí es indispensable que lo señales."*
- ⛔ el paralelismo REAL (worktrees, dispatch) antes de que exista el vocabulario que lo gobierne
- ⛔ copiar GSD o ultracode-epic tal cual — se adopta el MECANISMO, nunca el prompt

## 🌐 System-wide rules that also apply (inherited, not owned here)
- `CLAUDE.md`: nunca tocar `marca-personal/Mente/` · nunca leer `~/5M-incubathon/` sin el gate
- `base-rules.md` #7: server-first · ADR-003: el criterio es de Brian, nunca se inventa

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: nada técnico. **Depende de una decisión de Brian** (§E)
- DEPENDED ON BY: ⭐ **la unión Mente OS v2 ↔ For3s OS.** Brian, 2026-08-10: *"más adelante
  Mente OS v2 va a estar dentro de For3s OS, van a estar comunicados"*
- ISOLATED FROM: el bloque `demo` — otro repo, otra relación
- 🔴 CRITICAL PIECES: ninguna medida aún — el bloque no ha abierto trabajo

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤12 lines ══ -->
## Required standards
- rules/rule-shipping-flow.md
- rules/rule-pr-batching.md
- rules/rule-isolation.md
- rules/rule-checks-must-measure.md
- principles/owner-3-validation.md
- principles/expertise/doc-planning.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: 🔒 **BLOQUEADO A PROPÓSITO** — el hallazgo está registrado, el diseño no empieza
blockers: ⭐ **el diseño lo decide BRIAN** — cuándo se abre y con qué alcance. Ninguna IA puede
          decidirlo: es criterio (ADR-003), y además define cómo se unen los DOS sistemas
progress: 0/9 — nada construido. Lo que existe es el ANÁLISIS de §J
next: nada hasta que Brian lo desbloquee. ⚠️ `bin/flag-stale` lo marcará a los 14 días: es
      esperado, no una alarma — el bloqueador es una decisión, no un impedimento técnico
updated: 2026-08-10

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | pieza | imports | status |
|---|---|---|---|---|
| 1 | tabla de PROPIEDAD de archivos — quién edita qué antes de lanzar | rules/ | 0 | blocked |
| 2 | contrato de puertas CONGELADO antes de empezar | rules/ | 0 | blocked |
| 3 | puertas declaradas HUMANA vs AUTOMÁTICA + comando de evidencia | rules/ · hooks/ | 0 | blocked |
| 4 | LEDGER de decisiones de puerta (fecha · razón · evidencia) | bin/ | 0 | blocked |
| 5 | olas de trabajo: qué entra en una y qué la cierra | rules/ | 0 | blocked |
| 6 | aislamiento por worktree, un agente por árbol | bin/ | 0 | blocked |
| 7 | cortacircuitos: datos borrados · lockfile · regresión de tests | hooks/ | 0 | blocked |
| 8 | presupuesto de contexto por agente (de GSD) | rules/ | 0 | blocked |
| 9 | ⭐ el PUENTE Mente OS v2 ↔ For3s OS: vocabulario compartido | ambos repos | 0 | blocked |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- ⭐ 2026-08-10 · **Nace BLOQUEADO, no cerrado ni abierto.** Brian: *"no lo vamos a diseñar
  ahorita… pero sí es indispensable que lo señales."* ⛔ Un hallazgo que no se registra se
  redescubre: es exactamente el defecto que destapó que los conflictos no estaban cubiertos —
  **un hueco del que nadie habla es indistinguible de uno que no existe.**
- ⭐ 2026-08-10 · **Es para LOS DOS sistemas, no solo para Mente OS.** For3s OS ya tiene motor
  multi-agente en producción (H8: 5 specialists + Synthesizer); Mente OS tiene el gobierno.
  **Ninguno de los dos tiene el vocabulario del otro**, y van a unirse.
- 🔬 2026-08-10 · **El hallazgo salió de analizar DOS sistemas ajenos, y coincidieron.** GSD
  (33 agentes con perfil de modelo · presupuesto de contexto) y ultracode-epic (propiedad de
  archivos · contrato congelado · ledger) señalan **el mismo hueco desde ángulos distintos**:
  Mente OS gobierna **un agente en serie**. Dos fuentes independientes apuntando al mismo sitio
  es evidencia, no opinión.
- ⛔ 2026-08-10 · **No se adopta ninguno de los dos tal cual.** Ambos son *prompt-enforced* —
  ultracode lo dice de sí mismo: *"This is prompt-enforced, not sandboxed"*. Mente OS ya vive en
  el 100% (código) y bajar al 40-60% (documento) sería una regresión. **Se adopta el MECANISMO
  y se le pone un check.**

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- ⚠️ **La evidencia externa es débil y hay que decirlo:** ultracode-epic tiene **UNA corrida
  validada** de su skill de ola, y su orquestador completo está **sin validar de extremo a
  extremo**, en un solo stack (Node/pnpm). GSD está **archivado** desde el 26-jun y migró a otro
  repo. ⭐ **Buenas ideas con poca prueba: se toma el mecanismo, nunca la confianza.**

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-10 · Registrado el hallazgo tras analizar `gsd-build/get-shit-done` (3.1 MB instalados
  en esta máquina: 33 agentes, 100 workflows, 53 referencias) y `troopdegen/ultracode-epic`.
  Medido contra el árbol: **9 de sus mecanismos no existen en Mente OS**, ninguno a medias.

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context

**El hueco, en una frase: Mente OS v2 gobierna UN agente trabajando EN SERIE.**

No es un defecto de lo construido — es un límite de su alcance, y hasta hoy nadie lo había
nombrado. Hoy no duele porque Brian trabaja con un agente a la vez. **Empezará a doler el día que
quiera paralelizar**, y ese día el defecto será concreto: dos agentes tocando `session.ts` y el
merge decidiendo por nadie.

### Lo que falta, medido contra el árbol el 2026-08-10

| Mecanismo | Origen | Qué resuelve |
|---|---|---|
| **Propiedad de archivos** | ultracode | declarar quién edita qué **antes** de lanzar. Su corrida: *cero colisiones* |
| **Contrato de puertas congelado** | ultracode | se fija antes y **no se puede relajar durante la ejecución** |
| **Puertas HUMANA vs AUTO** | ultracode | cada puerta declara si pasa sola —con **comando de evidencia**— o necesita a Brian |
| **Ledger de decisiones** | ultracode | *"el ledger hace visible la violación, no silenciosa"* |
| **Olas de trabajo** | ultracode | qué entra en una tanda y qué la cierra |
| **Worktree por agente** | ultracode | aislamiento real, no confianza |
| **Cortacircuitos** | ultracode | corta ante borrado de datos, cambio de lockfile o regresión |
| **Perfil de modelo por agente** | GSD | cada tarea en el modelo que le toca, no todo en el mismo |
| **Presupuesto de contexto** | GSD | la profundidad de lectura escala con la ventana |

⭐ **El octavo y el noveno importan aparte:** atacan de frente **el peor incidente registrado** —
la degradación por contexto del 21-jul (5 días de sesión, 821K de contexto, *"no eres el mismo de
siempre, no me sirves así"*). Hoy Mente OS no tiene **ninguna** defensa declarada contra eso.

### Lo que Mente OS tiene y ellos no — para no copiar a ciegas

Batería de **220 checks ejecutables** · veredicto medido producto/MVP en 2 capas · hooks que
**BLOQUEAN** (exit 2, no un prompt) · checks que **se ven fallar por sabotaje** · *nunca inventar
criterio* (ADR-003) · techos de tamaño por tipo de documento. **Ninguno de los dos tiene nada de
esto.**

⭐ **La ley de este sistema aplicada a la decisión:** *código 100%, documento 40-60%*. Los dos
sistemas analizados viven en el 40-60%. **Se les toma el vocabulario, no el método.**

### Por qué es para los DOS sistemas

For3s OS **ya corre multi-agente en producción** (H8: motor de 5 specialists + Synthesizer).
Mente OS **ya tiene el gobierno** (puertas, contratos, veredicto). Cada uno tiene la mitad que al
otro le falta, y Brian declaró el 2026-08-10 que **van a unirse**: *"más adelante Mente OS v2 va a
estar dentro de For3s OS, van a estar comunicados."*

⚠️ **El riesgo de no hacerlo:** los dos sistemas se unen con vocabularios distintos para la misma
cosa, y entonces el puente se construye traduciendo — que es la forma más cara de conectar dos
sistemas y la que garantiza que diverjan.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — el bloque nace bloqueado y no ha abierto trabajo)
