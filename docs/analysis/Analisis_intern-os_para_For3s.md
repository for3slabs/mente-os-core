# 🔍 Análisis a profundidad: intern-os → qué traer a For3s OS (como código propio)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Analisis_intern-os_para_For3s.md → docs/analysis/Analisis_intern-os_para_For3s.md (2026-07-30, ADR-029)

## Purpose

🔍 Análisis a profundidad: intern-os → qué traer a For3s OS (como código propio)


**Fecha:** 2026-07-01
**Tarea (Brian):** auditar a fondo el repo `intern-os` (clonado en `~/Frutero-Empresa/Frutero/intern-os/`,
v0.4.1, commit be27ac2) para identificar qué tiene RESUELTO que For3s aún no, y derivar qué traer.
**Regla (Brian 2026-06-30):** lo que se traiga a For3s se implementa como **capacidad PROPIA, sin
referencias externas en el código**. Este doc es notación INTERNA de Mente OS (aquí sí se nombra la
fuente para el análisis); el código que salga NO menciona el origen.

---

## 1. Qué es intern-os (en una línea)

Un **framework de coordinación de trabajo por ARCHIVOS markdown + scripts bash** ("Workstreams"):
cada unidad de trabajo (workstream) se liga a exactamente UN hilo de comunicación, guarda su estado
en archivos estructurados, y puede reconstruirse desde esos archivos. Para agentes de cualquier
harness (no es específico de uno).

**Naturaleza vs For3s:** intern-os = disciplina de organización en markdown/bash (0 infra, 0 BD).
For3s = Python + PostgreSQL con motor cerebral (memoria semántica, grafo, CLS, equipo). Arquitecturas
MUY distintas → lo valioso son los **CONCEPTOS**, no el código (que no se puede copiar tal cual).

### Las 3 capas del framework
1. **Storage** — los archivos del workstream son el estado autoritativo (no el transcript, no la
   memoria del agente): PROJECT.md · AGENTS.md · TICK.md (tareas) · archivos de workstream · REGISTRY.md.
2. **Resolution** — binding EXACTO hilo↔workstream vía `thread_id` en BRIEF.md. Determinista, NUNCA
   por fuzzy/keyword/proximidad.
3. **Runtime** — carga por TIERS: default BRIEF+STATUS; escalar a DECISIONS/STAKEHOLDERS a demanda;
   MEMORY/RESOURCES/docs solo si hace falta. Sin lecturas cruzadas por defecto.

### Estructura de estado por workstream (los archivos)
- **BRIEF.md** — identidad + thread_id + objetivo
- **STATUS.md** — Phase / Next / Owner / Blockers / Updated
- **DECISIONS.md** — decisiones con: decisión, rationale, impacto, status (active/superseded/reversed)
- **MEMORY.md** — contexto durable + aprendizajes + hilos abiertos
- **STAKEHOLDERS.md** — quién es quién · **RESOURCES.md** — enlaces/recursos

### Features destacadas (CHANGELOG)
- **shared-thread inbox (v0.4.0)** — opt-in para plataformas tipo DM (Telegram, WhatsApp…) donde UN
  DM es la superficie de varios workstreams.
- **isolated handoff (v0.4.0)** — un coordinador delega a un subagente aislado con un manifest
  verificable, sin perder el binding (4 invariantes: resolución determinista, aislamiento explícito,
  archivos-como-verdad, separación de roles). Scripts de verificación POSIX.

---

## 2. Comparación For3s vs intern-os

| # | Concepto de intern-os | ¿For3s lo tiene? | ¿Traer? |
|---|----------------------|------------------|---------|
| 1 | Workstream = unidad de trabajo ligada a 1 hilo | Parcial (hilos por usuario/tema #6/AI2; NO "unidad de trabajo con estado propio") | 🟡 |
| 2 | Resolución determinista por thread_id (nunca fuzzy) | ❌ For3s resuelve por semántica | 🟢 valioso |
| 3 | Carga por Tiers (default→escalar) | ✅ ya (AI6 disciplina de tamaño) | ✅ hecho |
| 4 | Estado operativo estructurado (STATUS: fase/next/blockers) | ❌ For3s tiene memoria pero no "estado de proyecto" | 🟢 valioso |
| 5 | Isolated handoff con manifest verificable | Parcial (equipo H8, sin manifest) | 🟡 cruza H8 |
| 6 | DECISIONS registro (decisión+rationale+impacto+status) | ❌ no existe | 🟢 valioso |
| 7 | shared-thread inbox (1 DM = varios workstreams) | Relevante (For3s vive en DM Telegram) | 🟡 cruza MEM-2 |
| 8 | checkpoint-reminder (STATUS obsoleto) | Monitoreo /salud, no "workstreams sin actualizar" | 🟢 menor |

**Nota:** For3s YA adoptó (rondas AI1-AI7, 2026-06-23) varios conceptos de este ámbito: aislamiento
de hilos (AI1), shared-thread inbox (AI2), handoff auditable (AI3), auto-inyectar estado (AI4),
version-awareness (AI5), disciplina de tamaño/tiered (AI6), registry de hilos (AI7). Este análisis es
la SIGUIENTE capa: estado operativo de PROYECTO + decisiones + resolución determinista.

---

## 3. Los 3 conceptos VALIOSOS a traer (como capacidad propia de For3s)

### C1 · Estado operativo estructurado por tema/proyecto 🟢
Que un tema de For3s (AI2) pueda tener un **estado consultable**: fase actual, próximo paso, blockers,
última actualización. Hoy For3s tiene el historial y el grafo, pero no un "¿en qué punto está este
proyecto?" de un vistazo. Implementación propia: tabla `tema_estado` (o extender la de temas) +
comando (ej. `/estado_tema`) + que el bot lo actualice al cerrar sesión de trabajo.
Cruza con: AI2 (temas), REDISEÑO MEMORIA, D (memoria híbrida).

### C2 · Registro de DECISIONES 🟢
Un registro estructurado de decisiones tomadas: qué se decidió, por qué (rationale), impacto, estado
(vigente/superada/revertida). Hoy For3s NO distingue "una decisión" del resto de la conversación.
Valor: el bot podría responder "¿por qué decidimos X?" con la decisión + su rationale, y saber si
sigue vigente. Implementación propia: tabla `decisiones` + detección/registro (manual `/decidi ...`
o inferido) + inyección al contexto cuando aplica. Cruza con memoria y auditoría.

### C3 · Resolución determinista de hilo (complemento a la semántica) 🟢
For3s resuelve memoria por SIGNIFICADO (semántica) — potente pero puede traer lo parecido en vez de
lo exacto (fue la raíz de bugs de hilos). Concepto a adoptar: donde haya un binding EXACTO
disponible (hilo/tema/proyecto concreto), usarlo PRIMERO y determinista, y caer a semántica solo si
no hay match exacto. No reemplaza la semántica de For3s — la complementa con una capa exacta.
Cruza con: MEM-3 (cascada de capas — encaja perfecto: exacto → semántico), BUG-17.

---

## 4. Veredicto

intern-os es una **disciplina de organización de trabajo**, complementaria al motor cerebral de For3s
(no competidora). For3s ya absorbió su capa de hilos/handoff (AI1-AI7). Lo que queda por traer son 3
conceptos de **gestión de estado de trabajo**: C1 estado de proyecto · C2 decisiones · C3 resolución
determinista. Los 3 son de valor real y encajan con bloques ya planeados (REDISEÑO MEMORIA, temas).

⚠️ **NO implementado aún** — este doc es el MAPA. Cuando Brian decida construir alguno, se hace como
código propio de For3s (sin referencias). C3 conviene hacerlo DENTRO del REDISEÑO MEMORIA (MEM-3
cascada). C1 y C2 pueden ser mejoras puntuales o parte del rediseño.

**Relacionado:** REDISEÑO MEMORIA (MEM-1/2/3) · AI1-AI7 (ya adoptado) · temas (AI2).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `docs/analysis/Analisis_intern-os_para_For3s.md`).
