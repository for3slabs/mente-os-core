# Mapeo Nodo Cerebral ↔ Tabla SQL — For3s OS

**Documento canónico del bridge filosofía ↔ código.**

**Owner:** Brian López
**Fecha de creación:** 2026-06-01 (al cierre del Bloque 2 R2)
**Estatus:** ✅ Documento VIVO — actualizar al añadir/cambiar nodos
**Capa:** Cerebro — bridge entre Grafo Maestro y materialización técnica
**Última actualización:** 2026-06-09 (⚠️ reconciliación de numeración de nodos — ver §0)

**Origen:**
- Sub-tema 2.7 LOCKED en R2 Bloque 2
- Origen conceptual: Brian identificó gap entre vocabulario cerebral (Grafo Maestro) y vocabulario técnico (código real)
- Decisión: añadir 2.7 como sub-tema obligatorio del Bloque 2

**Documentos relacionados (fuentes):**
- [`For3s_OS_Grafo_Maestro.md`](For3s_OS_Grafo_Maestro.md) — fuente de verdad cerebral
- [`Ronda_02_Bloque_1_Storage_Foundation.md`](../Cuerpo/Ronda_02_Bloque_1_Storage_Foundation.md) — storage físico
- [`Ronda_02_Bloque_2_Memory_Architecture.md`](../Cuerpo/Ronda_02_Bloque_2_Memory_Architecture.md) — arquitectura semántica
- [`Ronda_02_Data_Layer.md`](../Cuerpo/Ronda_02_Data_Layer.md) — master R2

**Documentos relacionados (espejos público-formales):**
- [`for3s-inter/09-technical-architecture/storage-foundation.md`](../../for3s-inter/09-technical-architecture/storage-foundation.md)
- [`for3s-inter/09-technical-architecture/memory-architecture.md`](../../for3s-inter/09-technical-architecture/memory-architecture.md)
- [`for3s-inter/07-operations/decision-log.md`](../../for3s-inter/07-operations/decision-log.md) D-007

---

## §0 — NUMERACIÓN CANÓNICA DE NODOS (AUTORIDAD) ⚠️ LEER PRIMERO

> **Reconciliación 2026-06-09.** Una auditoría de coherencia (`Doc/Reporte_Maestro_Consolidado_R1-R10.md` + `Doc/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md`) detectó que la numeración de nodos 5-9 en el CUERPO de este documento (escrito 2026-06-01, antes de R5/R9) **no coincide** con la del `For3s_OS_Grafo_Maestro.md` ni con la `Vision_For3s_Frontier.md §6.1` ni con las rondas R5/R6/R9. **Esta sección §0 es la AUTORIDAD.** Donde el cuerpo (§3-§19) diga otro número para los nodos 5-9, prevalece §0.

### La numeración canónica (= Grafo Maestro = Visión §6.1 = R5/R6/R9)

```
   Nodo 1  — Knowledge Graph (Neocorteza semántica)
   Nodo 2  — Hipocampo + Pattern Separation (memoria episódica)
   Nodo 3  — PFC / Orchestrator (corteza prefrontal)
   Nodo 4  — Ganglios Basales / Skills (incluye Action Selection)
   Nodo 5  — Microglía (olvido inteligente / forgetting)
   Nodo 6  — DMN (Default Mode Network / idle compute)
   Nodo 7  — Amígdala (valoración rápida / threat detection)
   Nodo 8  — Tálamo (router)
   Nodo 9  — Dual-Process Check (Sistema 1 vs Sistema 2, Kahneman)
   Nodo 10 — Consolidación CLS (sleep cycle)
   Nodo 11 — Neuromoduladores (dopamina / serotonina / etc.)
```

### Tabla de corrección — numeración VIEJA (cuerpo §3-§19) → CANÓNICA (§0)

```
   ┌────────────────────────┬──────────────┬──────────────┬─────────────────────────┐
   │ Concepto               │ Nº VIEJO     │ Nº CANÓNICO  │ Nota                    │
   │                        │ (cuerpo)     │ (§0/Grafo)   │                         │
   ├────────────────────────┼──────────────┼──────────────┼─────────────────────────┤
   │ Knowledge Graph        │ 1            │ 1            │ ✅ sin cambio           │
   │ Hipocampo              │ 2            │ 2            │ ✅ sin cambio           │
   │ PFC                    │ 3            │ 3            │ ✅ sin cambio           │
   │ Ganglios Basales/Skills│ 4            │ 4            │ ✅ sin cambio           │
   │ Action Selection       │ 5 (era nodo) │ → parte de 4 │ NO es nodo aparte; es   │
   │                        │              │              │ función de Ganglios B.  │
   │ Microglía              │ 6            │ 5            │ ⚠️ baja de 6 a 5        │
   │ DMN                    │ 7            │ 6            │ ⚠️ baja de 7 a 6        │
   │ Amígdala               │ 8            │ 7            │ ⚠️ baja de 8 a 7        │
   │ Tálamo                 │ (ausente)    │ 8            │ ⚠️ FALTABA como nodo    │
   │ Dual-Process Check     │ (ausente)    │ 9            │ ⚠️ FALTABA como nodo    │
   │ Pattern Separation     │ 9 (era nodo) │ → parte de 2 │ NO es nodo aparte; es   │
   │                        │              │              │ función del Hipocampo   │
   │ Consolidación CLS      │ 10           │ 10           │ ✅ sin cambio           │
   │ Neuromoduladores       │ 11           │ 11           │ ✅ sin cambio           │
   └────────────────────────┴──────────────┴──────────────┴─────────────────────────┘
```

### Causa raíz del desajuste

El cuerpo de este documento (2026-06-01) modeló **"Action Selection" (5)** y **"Pattern Separation" (9)** como nodos numerados independientes. El Grafo Maestro NO los numera por separado: Action Selection es una **función del Nodo 4 (Ganglios Basales)** y Pattern Separation es una **función del Nodo 2 (Hipocampo)**. Esa duplicación corrió la numeración de Microglía/DMN/Amígdala (subieron de número) y dejó **fuera de la lista numerada a Tálamo y Dual-Process Check** (que sí son nodos 8 y 9 en el Grafo). R5 (que materializó Tálamo=8 + Dual-Process=9) y R9 (Amígdala=7) siguieron el Grafo, confirmando que el outlier es este Mapeo.

### Cómo leer el resto del documento

- **§3 (status agregado) y §4 (tabla maestra): YA CORREGIDOS** a numeración canónica abajo.
- **§5-§19 (detalle por nodo, diccionario, flujos): conservan números viejos en el texto.** Al leerlos, traducir con la tabla de arriba. El CONTENIDO técnico de cada nodo (tablas SQL, módulos, operaciones) es correcto — solo el NÚMERO de etiqueta puede estar viejo. La función "Action Selection" (§9 viejo Nodo 5) pertenece al Nodo 4; "Pattern Separation" (§13 viejo Nodo 9) pertenece al Nodo 2.

---

## Tabla de contenidos

1. [Propósito y filosofía del documento](#1-propósito-y-filosofía-del-documento)
2. [Cómo usar este documento](#2-cómo-usar-este-documento)
3. [Resumen ejecutivo del mapeo](#3-resumen-ejecutivo-del-mapeo)
4. [TABLA MAESTRA — 11 nodos × 8 columnas](#4-tabla-maestra--11-nodos--8-columnas)
5. [Detalle por nodo — Nodo 1: Knowledge Graph](#5-nodo-1--knowledge-graph-neocorteza-semántica)
6. [Detalle por nodo — Nodo 2: Hipocampo](#6-nodo-2--hipocampo-memoria-episódica)
7. [Detalle por nodo — Nodo 3: PFC](#7-nodo-3--pfc-prefrontal-cortex--orquestador)
8. [Detalle por nodo — Nodo 4: Ganglios Basales (Skills)](#8-nodo-4--ganglios-basales-skills-aprendidas)
9. [Detalle por nodo — Nodo 5: Action Selection](#9-nodo-5--ganglios-basales-extensión-action-selection)
10. [Detalle por nodo — Nodo 6: Microglía](#10-nodo-6--microglía-forgetting--poda-sináptica)
11. [Detalle por nodo — Nodo 7: DMN](#11-nodo-7--dmn-default-mode-network--idle-compute)
12. [Detalle por nodo — Nodo 8: Amígdala](#12-nodo-8--amígdala-policy-enforcement--emotional-gating)
13. [Detalle por nodo — Nodo 9: Pattern Separation](#13-nodo-9--pattern-separation-función-hipocampal)
14. [Detalle por nodo — Nodo 10: CLS](#14-nodo-10--consolidación-cls-sleep-cycle)
15. [Detalle por nodo — Nodo 11: Neuromoduladores](#15-nodo-11--neuromoduladores-dopamina--serotonina--etc)
16. [Diagrama visual completo](#16-diagrama-visual-completo-de-la-arquitectura-cerebral)
17. [Diccionario bilingüe cerebral ↔ técnico](#17-diccionario-bilingüe-cerebral--técnico)
18. [Operaciones cerebrales ↔ operaciones código](#18-operaciones-cerebrales--operaciones-código)
19. [Flujos cross-nodo (cómo se comunican entre sí)](#19-flujos-cross-nodo-cómo-se-comunican-entre-sí)
20. [Excepciones inmutables (NUNCA tocar)](#20-excepciones-inmutables-nunca-tocar)
21. [Protocolo de actualización del documento](#21-protocolo-de-actualización-del-documento)

---

## 1. Propósito y filosofía del documento

### El problema que resuelve

Brian identificó originalmente este gap:

> "El Grafo Maestro habla en términos cerebrales (Hipocampo, KG, Microglía, CLS, etc.). El código habla en términos técnicos (episodes_events, pgvector, HNSW, etc.). Sin un MAPEO EXPLÍCITO, los devs (y agentes futuros) se perderán traduciendo entre los dos lenguajes."

Este documento es la solución: un **bridge explícito** que traduce ambos vocabularios.

### Filosofía

```
DOS LENGUAJES, UN SOLO SISTEMA:

   LENGUAJE CEREBRAL                  LENGUAJE TÉCNICO
   (Grafo Maestro)                    (código real)

   "Hipocampo"               ↔        episodes_events + pgvector
   "Pattern Separation"      ↔        HNSW recall threshold
   "Microglía poda sinapsis" ↔        soft delete + decay + archive
   "Sleep cycle"             ↔        consolidator.py cron 2 AM
   "Refuerzo dopaminérgico"  ↔        success_rate++

Sin este mapeo:
   • Devs nuevos no saben dónde tocar
   • Code reviews pierden contexto cerebral
   • Cambios "técnicos" pueden romper alineación cerebral
   • Agente futuro pierde trazabilidad
```

### Beneficios documentados

```
1. Onboarding de devs nuevos
   • Una sola lectura → entienden el bridge
   • Saben dónde vive cada nodo cerebral
   • Saben qué tabla materializa qué función

2. Code reviews informados
   • "¿Esta función modifica el comportamiento del Nodo X?"
   • Si SÍ → actualizar mapeo + documentar
   • Si NO → revisar si debería

3. Debugging trazable
   • "¿De qué nodo cerebral viene este comportamiento?"
   • Resp: ver memory/forgetter.py → Nodo 6 Microglía
   • Bug en forgetting → revisar políticas de Microglía

4. Auditoría arquitectónica
   • ¿Cubrimos todos los nodos del Grafo?
   • ¿Algún nodo quedó sin materializar?
   • Status: FULLY / FOUNDATION / PENDIENTE

5. Continuidad cross-sesión (Claude futuro)
   • Un Claude que retoma puede leer este doc
   • Entiende qué hace cada parte del sistema
   • No reinventa decisiones ya tomadas
```

---

## 2. Cómo usar este documento

### Para devs (humanos o IA)

```
ANTES de tocar memory/, security/, orchestrator/:
   1. LEER esta tabla maestra (§4)
   2. Identificar qué nodo cerebral toca tu cambio
   3. Verificar status del nodo (FULLY/FOUNDATION/PENDIENTE)
   4. Leer detalle del nodo afectado (§5-§15)
   5. Verificar excepciones inmutables (§20)

DURANTE el desarrollo:
   • Mantener nombres alineados con vocabulario cerebral
   • Si añades tabla → mapear a un nodo
   • Si modificas comportamiento → actualizar §17/§18

EN code reviews:
   • Pregunta obligatoria: "¿Qué nodo cerebral toca este PR?"
   • Si toca audit_events o events tables → BLOCKER (inmutable)
   • Si toca un nodo "FOUNDATION" → revisar si debería pasar a "FULLY"
```

### Para Brian (founder)

```
Este doc es REFERENCIA MAESTRA. Lo consultas cuando:
   • Necesitas explicar la arquitectura a alguien
   • Vas a contratar y quieres dar contexto técnico
   • Vas a revisar si For3s OS sigue alineado con Grafo Maestro
   • Vas a planear nuevas rondas (R3+)
```

### Para Claude/agentes futuros

```
Si retomas conversación con Brian:
   1. Lee Estado_Sesion_Continuidad.md (continuidad operativa)
   2. Lee For3s_OS_Grafo_Maestro.md (filosofía)
   3. Lee ESTE DOC (bridge)
   4. Ya tienes el modelo mental completo de For3s OS

NO inventes mapeos nuevos sin Brian.
NO renombres conceptos sin documentar.
NO toques excepciones inmutables (§20).
```

---

## 3. Resumen ejecutivo del mapeo

### Status agregado de los 11 nodos

```
> ⚠️ Numeración corregida a CANÓNICA (§0) el 2026-06-09. Estado v1 (foto 2026-06-01);
> R5/R9 luego cerraron Tálamo/Dual-Process/DMN/Amígdala → ver maestros R5 y R9 para estado final.

✅ FULLY MAPPED (6 nodos)
   El nodo tiene tabla(s) + módulo + función productiva en v1.

   • Nodo 1 — Knowledge Graph (Apache AGE + concepts)
   • Nodo 2 — Hipocampo + Pattern Separation (episodes_events + pgvector + HNSW)
   • Nodo 4 — Ganglios Basales / Skills (skills_events + state + Action Selection)
   • Nodo 5 — Microglía (forgetter.py + archive tables)
   • Nodo 10 — Consolidación CLS (consolidator.py + Haiku)
   • (Pattern Separation = función del Nodo 2 · Action Selection = función del Nodo 4)

🟡 FOUNDATION READY (4 nodos)
   Infraestructura base existe pero R5+ completa la función.

   • Nodo 3 — PFC (Working Memory existe, R5 extiende orquestador)
   • Nodo 7 — Amígdala (RBAC + policies foundation, R9 completa)
   • Nodo 8 — Tálamo (router — R5 lo materializa completo)
   • Nodo 11 — Neuromoduladores (success_rate + decay, R5 modula)

⏳ PENDIENTE en v1 / cerrados en R5 (2 nodos)
   No tenían materialización al 2026-06-01. R5 los definió.

   • Nodo 6 — DMN (Default Mode Network — idle compute) → R5 B4
   • Nodo 9 — Dual-Process Check (Sistema 1 vs 2) → R5 B2
```

### Cobertura porcentual

```
Total nodos: 11
   FULLY mapped:       6/11 = 55%
   FOUNDATION ready:   4/11 = 36%
   PENDIENTE:          1/11 = 9%

Cobertura productiva v1: 91% (10/11 nodos servidos en algún nivel)
```

### Por dónde se completarán los gaps

```
PENDIENTES Y CIERRES POR RONDA:

   R3 (Model/LLM Layer):
      → Refuerza Nodo 10 (CLS usa Claude Haiku)
      → Refuerza Nodo 3 PFC (LLM razona en working memory)

   R5 (Orchestration):
      → Cierra Nodo 3 PFC (orquestador completo)
      → Cierra Nodo 5 Action Selection
      → DEFINE Nodo 7 DMN
      → Cierra Nodo 11 Neuromoduladores

   R9 (Security/Compliance):
      → Cierra Nodo 8 Amígdala (policy engine)

   R8 (Observability):
      → No añade nodos pero monitorea TODOS
```

---

## 4. TABLA MAESTRA — 11 nodos × 8 columnas

```
┌─────┬──────────────────┬──────────────┬───────────────────┬─────────────────┬──────────────┬─────────────┬──────────────────┐
│ #   │ Nombre Cerebral  │ Status v1    │ Tabla(s) SQL       │ Módulo Python   │ Extensión PG │ Bloque Ronda│ Próxima dep.      │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 1   │ Knowledge Graph  │ ✅ FULLY    │ {age}.kg_nodes/   │ memory/         │ AGE +        │ B1 1.2      │ R5 razonamiento  │
│     │ (Neocorteza)     │             │ edges + concepts  │ kg_bridge.py    │ pgvector     │ B2 2.4      │                  │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 2   │ Hipocampo        │ ✅ FULLY    │ episodes_events,  │ memory/         │ pgvector +   │ B1 1.6      │ R5 lectura       │
│     │ (mem. episódica  │             │ episodes_state,   │ repository.py + │ triggers     │ B2 2.2/2.3  │ contexto         │
│     │ + Pattern Sep)   │             │ episodes_archived │ tiers.py        │ HNSW tuneado │ B2 2.4      │ (Pattern Sep=§13)│
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 3   │ PFC              │ 🟡 PARTIAL  │ (sin tabla v1)    │ memory/tiers.py │ ninguna      │ B2 2.4      │ R5 extiende      │
│     │ (Working Memory) │             │ in-process Python │ + R5            │              │             │ con planning     │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 4   │ Ganglios Basales │ ✅ FULLY    │ skills_events,    │ memory/         │ pgvector +   │ B1 1.6      │ R3 LLM ejecuta   │
│     │ (Skills +        │             │ skills_state,     │ repository.py   │ triggers     │ B2 2.2/2.5  │ R4 MCP registra  │
│     │ Action Select)   │             │ skills_archived   │                 │              │             │ (Action Sel=§9)  │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 5   │ Microglía        │ ✅ FULLY    │ Modifica state    │ memory/         │ partial idx  │ B2 2.5      │ R3 jobs schedul. │
│     │ (forgetting)     │             │ tables + archive  │ forgetter.py    │              │             │                  │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 6   │ DMN              │ ⏳ PEND→R5  │ (definido en R5)  │ orchestrator/   │ ninguna      │ R5 B4       │ R5 define todo   │
│     │ (idle compute)   │             │                   │ dmn.py (R5)     │              │             │                  │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 7   │ Amígdala         │ 🟡 FOUND→R9 │ shared.security_  │ security/       │ pgcrypto +   │ B1 +        │ R9 policy        │
│     │ (threat/gating)  │             │ policies, rbac    │ policy_engine   │ RLS opcional │ R9          │ engine completo  │
│     │                  │             │                   │ .py (R9)        │              │             │                  │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 8   │ Tálamo           │ 🟡 FOUND→R5 │ routing layer     │ orchestrator/   │ ninguna      │ R5 B1       │ R5 materializa   │
│     │ (router)         │             │ (políticas + ML)  │ thalamus.py(R5) │              │             │ completo         │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 9   │ Dual-Process     │ ⏳ PEND→R5  │ (definido en R5)  │ orchestrator/   │ pgvector     │ R5 B2       │ R5 define S1/S2  │
│     │ Check (S1 vs S2) │             │                   │ dual_process(R5)│ (history)    │             │ + tier routing   │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 10  │ Consolidación    │ ✅ FULLY    │ Lee episodes_     │ memory/         │ pgvector +   │ B2 2.6      │ R3 LLM provee    │
│     │ CLS              │             │ state, escribe    │ consolidator.py │ AGE          │             │ Claude Haiku     │
│     │                  │             │ AGE + concepts    │                 │              │             │                  │
├─────┼──────────────────┼──────────────┼───────────────────┼─────────────────┼──────────────┼─────────────┼──────────────────┤
│ 11  │ Neuromoduladores │ 🟡 FOUNDA-  │ Implícitos en     │ memory/ranker + │ ninguna      │ B2 2.5/2.6  │ R5 modulación    │
│     │ (dopamina, etc.) │   TION       │ success_rate +    │ forgetter +     │              │             │ dinámica         │
│     │                  │             │ relevance_score   │ R5              │              │             │                  │
└─────┴──────────────────┴──────────────┴───────────────────┴─────────────────┴──────────────┴─────────────┴──────────────────┘
```

---

## 5. Nodo 1 — Knowledge Graph (Neocorteza semántica)

### Función neurocientífica

La **neocorteza** del cerebro almacena conocimiento conceptual generalizado. Es el resultado de la **consolidación** de experiencias episódicas (Hipocampo) durante el sueño (CLS). Permite razonamiento **multi-hop semántico**: saltar de un concepto a otro relacionado siguiendo aristas de significado.

> En el cerebro biológico, la neocorteza tiene capas (V1, V2, V4, áreas asociativas) que jerarquizan el conocimiento. En For3s OS lo modelamos como un grafo Cypher con nodos tipados (PR, File, Bug, Skill, Concept) y aristas semánticas (TOUCHES, CAUSED, SIMILAR_TO, DERIVED_FROM).

### Status v1

```
✅ FULLY MAPPED (Bloques 1 + 2)
```

### Tablas SQL principales

```sql
-- KG global compartido (conceptos cross-workspace)
SELECT create_graph('shared_kg');  -- AGE extension

-- KG por workspace (concepts del cliente)
SELECT create_graph('wks_X_kg');  -- per-workspace

-- Concepts table (con embeddings para búsqueda semántica)
CREATE TABLE wks_X.concepts (
    id                   UUID PRIMARY KEY,
    concept_type         TEXT NOT NULL,
    label                TEXT NOT NULL,
    description          TEXT,
    embedding            VECTOR(1024),
    embedding_model      TEXT NOT NULL DEFAULT 'stella:dunzhang_400M_v5@1024',
    source_episode_ids   UUID[] NOT NULL DEFAULT '{}',
    cluster_size         INT,
    reinforced_count     INT NOT NULL DEFAULT 0,
    last_reinforced_at   TIMESTAMPTZ,
    essential            BOOLEAN NOT NULL DEFAULT false,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_concepts_embedding
    ON wks_X.concepts
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);
```

### Extensiones PostgreSQL utilizadas

```
✓ Apache AGE — Cypher queries sobre grafo
✓ pgvector — embeddings de conceptos
```

### Módulos Python responsables

```
for3s_os/memory/kg_bridge.py
   • create_or_strengthen_node(concept_meta)
   • create_or_strengthen_edge(from, to, type, weight)
   • query_cypher(workspace, query)
   • find_related(entity_id, depth=2)

for3s_os/memory/tiers.py::LongTermMemory
   • store_concept(node, edges)
   • query_graph(cypher)
   • find_related(entity, depth)
```

### Bloque(s) que lo materializa

```
B1 1.2 → Decisión Apache AGE como extensión Postgres
B1 1.3 → pgvector para embeddings de conceptos
B2 2.4 → Tier 3 LongTermMemory architecture
B2 2.6 → CLS poblará este nodo (Hipocampo → KG)
B2 2.7 → Mapeo documentado (este doc)
```

### Operaciones principales

```python
# Pseudocódigo de operaciones típicas:

# 1. Crear concepto (vía CLS)
await kg.create_or_strengthen_node({
    'type': 'Pattern',
    'label': 'Auth bugs en módulos legacy',
    'description': 'Cluster recurrente de bugs en auth/*',
    'embedding': centroid_vector,
    'source_episodes': cluster_episode_ids
})

# 2. Crear arista (relación)
await kg.create_or_strengthen_edge(
    from_node='Pattern:auth-bugs',
    to_node='File:auth/login.py',
    relation='AFFECTS',
    weight=0.85
)

# 3. Query multi-hop (Cypher)
results = await age.execute("""
    MATCH (pr:PR)-[:TOUCHES]->(f:File)
          -[:HISTORICALLY_CAUSED]->(b:Bug)
          -[:REPORTED_BY]->(c:Client {tier:'enterprise'})
    RETURN pr.id, count(b) as risk_score
    ORDER BY risk_score DESC LIMIT 10
""")

# 4. Búsqueda semántica de conceptos
similar = await db.execute("""
    SELECT * FROM wks_X.concepts
    ORDER BY embedding <=> $1 LIMIT 5
""", query_embedding)
```

### Dependencias R3+

```
R3 (Model/LLM Layer):
   LLM consulta este nodo para razonamiento contextual

R5 (Orchestration):
   PFC usa KG para context building al construir respuesta
   action_selector consulta skills consolidadas

R6 (Memory Stack extensions):
   Posible: integrar Neo4j en v3 si AGE no escala
```

### Riesgos y observaciones

```
⚠️ AGE es joven (5 años vs Neo4j 18) — migración planeada v3
⚠️ Cypher queries pesadas pueden afectar Postgres compartido
✓ Joins NATIVOS con pgvector + relacional (único entre KGs)
✓ Backup unificado con resto de Postgres
```

---

## 6. Nodo 2 — Hipocampo (memoria episódica)

### Función neurocientífica

El **hipocampo** captura episodios contextualizados con relaciones espacio-temporales. Cada experiencia se codifica con su contexto: qué, cuándo, dónde, en qué situación. Es la fuente primaria para **consolidación CLS** durante el sueño. También realiza **Pattern Separation**: distingue episodios similares pero distintos para que no se confundan.

> En el cerebro biológico, el hipocampo está en el lóbulo temporal medial. Su giro dentado realiza la pattern separation. CA3 hace pattern completion. En For3s OS, episodes_events captura cada evento del agente con su contexto completo, y pgvector + HNSW permiten distinguirlos semánticamente.

### Status v1

```
✅ FULLY MAPPED (Bloques 1 + 2)
```

### Tablas SQL principales

```sql
-- Event Sourcing (inmutable)
CREATE TABLE wks_X.episodes_events (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    episode_id      UUID NOT NULL,
    event_type      TEXT NOT NULL,
    event_version   INT NOT NULL DEFAULT 1,
    payload         JSONB NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    sequence_number BIGINT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    UNIQUE (episode_id, sequence_number)
);

CREATE TRIGGER no_modify_episodes_events
    BEFORE UPDATE OR DELETE ON wks_X.episodes_events
    FOR EACH ROW EXECUTE FUNCTION shared.prevent_audit_mutation();

-- State projection (CRUD)
CREATE TABLE wks_X.episodes_state (
    id                   UUID PRIMARY KEY,
    workspace_id         UUID NOT NULL,
    status               TEXT NOT NULL,
    steps_done           INT NOT NULL DEFAULT 0,
    duration_seconds     INT,
    context_encrypted    BYTEA,   -- P4 app-layer encryption
    output_encrypted     BYTEA,   -- P4 app-layer encryption
    embedding            VECTOR(1024),
    embedding_model      TEXT NOT NULL DEFAULT 'stella:dunzhang_400M_v5@1024',
    deleted_at           TIMESTAMPTZ,             -- B2 2.5 forgetting
    relevance_score      FLOAT NOT NULL DEFAULT 1.0,  -- decay
    last_accessed_at     TIMESTAMPTZ DEFAULT now(),
    consolidated_to_kg   BOOLEAN NOT NULL DEFAULT false,  -- trigger Microglía
    legal_hold           BOOLEAN NOT NULL DEFAULT false,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index HNSW tuneado (B2 2.3)
CREATE INDEX idx_episodes_state_embedding
    ON wks_X.episodes_state
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

-- Partial index para episodios activos
CREATE INDEX idx_episodes_state_active
    ON wks_X.episodes_state (last_accessed_at)
    WHERE deleted_at IS NULL;

-- Cold storage (archive)
CREATE TABLE wks_X.episodes_archived (
    LIKE wks_X.episodes_state INCLUDING ALL,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    archive_reason TEXT
);
-- NO HNSW index en archived (cold storage)
```

### Extensiones PostgreSQL utilizadas

```
✓ pgvector (HNSW index para búsqueda semántica)
✓ Triggers de inmutabilidad en events table
```

### Módulos Python responsables

```
for3s_os/memory/repository.py::EpisodesRepository
   • store_event(workspace, episode_id, event)
   • get_pending_consolidation(workspace, limit)
   • find_similar(workspace, query_vec, top_k, ef_search)
   • get_recent(workspace, days)
   • mark_consolidated(workspace, episode_ids)
   • soft_delete(workspace, episode_id, reason)
   • refresh_on_access(workspace, episode_id)

for3s_os/memory/tiers.py::ShortTermMemory
   • store_episode(workspace, event)
   • recall_similar(query, k=10)
   • get_recent(workspace, days=7)

for3s_os/memory/embedder.py
   • Genera embeddings con Stella (default) o OpenAI (fallback)
```

### Bloque(s) que lo materializa

```
B1 1.1 → PostgreSQL base
B1 1.4 → SQLAlchemy 2 ORM (EpisodesRepository)
B1 1.6 → ES tables (episodes_events) + triggers inmutabilidad
B2 2.2 → Stella embeddings @ 1024
B2 2.3 → HNSW index tuneado
B2 2.4 → Tier 2 ShortTermMemory architecture
B2 2.5 → soft delete + decay + archive
B2 2.7 → Mapeo documentado (este doc)
```

### Operaciones principales

```python
# Pseudocódigo:

# 1. Store episode (genera evento ES + actualiza state)
async def store_episode(workspace, event_data):
    # 1.1 Insert evento (inmutable)
    event_id = await db.execute("""
        INSERT INTO {workspace}.episodes_events
        (episode_id, event_type, payload, sequence_number, created_by)
        VALUES ($1, $2, $3, $4, $5) RETURNING id
    """, ...)

    # 1.2 Generar embedding (Nodo 9 Pattern Separation)
    embedding = await embedder.embed(event_data.context)

    # 1.3 Actualizar projection state
    await db.execute("""
        INSERT INTO {workspace}.episodes_state
        (id, workspace_id, status, embedding, ...)
        VALUES ($1, $2, $3, $4, ...)
        ON CONFLICT (id) DO UPDATE SET
            updated_at = now(),
            embedding = EXCLUDED.embedding
    """, ...)

# 2. Recall similar (HNSW search con Pattern Separation)
async def recall_similar(workspace, query, k=10):
    query_vec = await embedder.embed(query)
    await db.execute("SET hnsw.ef_search = 100")
    results = await db.execute("""
        SELECT * FROM {workspace}.episodes_state
        WHERE deleted_at IS NULL
        ORDER BY embedding <=> $1
        LIMIT $2
    """, query_vec, k)

    # Refresh relevance score on access (Nodo 11 Neuromodulator)
    for ep in results:
        await refresh_on_access(workspace, ep.id)

    return results

# 3. Mark consolidated (trigger Microglía via Nodo 10 CLS)
async def mark_consolidated(workspace, episode_ids):
    await db.execute("""
        UPDATE {workspace}.episodes_state
        SET consolidated_to_kg = true, updated_at = now()
        WHERE id = ANY($1)
    """, episode_ids)
```

### Dependencias R3+

```
R3 (Model/LLM Layer):
   LLM consume episodios como contexto

R5 (Orchestration):
   Working Memory (Tier 1) flush a este nodo al cerrar sesión
   Context building integra Tier 2 + Tier 1 + Tier 3

R8 (Observability):
   Métricas críticas: latencia HNSW, RAM usage, recall accuracy
```

### Riesgos y observaciones

```
⚠️ HNSW RAM-hungry (riesgo 4 Bloque 1) — monitor desde día 1
⚠️ Volumen v3 (5M vectores) requiere Qdrant migración
✓ Inmutabilidad eventos = audit trail garantizado
✓ Pattern Separation crítico para For3s QA
```

---

## 7. Nodo 3 — PFC (Prefrontal Cortex / Orquestador)

### Función neurocientífica

El **PFC (corteza prefrontal)** maneja la **working memory** + metacognición + planning ejecutivo. Es "lo que tengo en mente AHORA mismo en esta tarea". Su capacidad es limitada (7±2 items según Miller 1956). Coordina el resto del cerebro para ejecutar tareas complejas.

> En el cerebro biológico, el PFC dorsolateral maneja working memory. El PFC ventromedial integra emoción + cognición. En For3s OS, modelamos la working memory en v1 (B2 2.4) y el orquestador completo en R5.

### Status v1

```
🟡 PARTIALLY MAPPED
   Tier 1 (Working memory) LOCKED en B2 2.4
   Orquestador completo se cierra en R5 (Orchestration)
```

### Tablas SQL principales

```
v1: NINGUNA (working memory in-process Python)

v2 posible: session_state si necesitamos persistencia
   • CREATE TABLE wks_X.session_state
     (session_id, working_memory JSONB, ...)
```

### Extensiones PostgreSQL utilizadas

```
v1: ninguna
v2: posible JSONB para estado de sesión
```

### Módulos Python responsables

```
for3s_os/memory/tiers.py::WorkingMemory
   • max_items: int = 15  (Miller 7±2 ajustado para agente AI)
   • ttl_minutes: int = 60
   • storage: dict[session_id, deque]
   • async def add(item)
   • async def get_context(budget_tokens)
   • async def flush_to_short_term()

for3s_os/orchestrator/* (futuro R5)
   • planning.py     — metacognición + plan ejecutivo
   • dual_process.py — sistema 1 vs sistema 2 (Kahneman)
   • action_selector.py — qué acción tomar siguiente
```

### Bloque(s) que lo materializa

```
B2 2.4 → Working memory Tier 1 (parcial)
B2 2.7 → Mapeo documentado (este doc)
R5    → PFC completo (orquestador, planning, metacognición)
```

### Operaciones principales (v1)

```python
# Pseudocódigo Working Memory:

class WorkingMemory:
    """Tier 1 — vida de la sesión."""

    def __init__(self):
        self.storage: dict[str, deque] = {}  # session_id → deque
        self.last_access: dict[str, datetime] = {}

    async def add(self, session_id: str, item: dict):
        if session_id not in self.storage:
            self.storage[session_id] = deque(maxlen=15)  # LRU cap
        self.storage[session_id].append(item)
        self.last_access[session_id] = datetime.now()

    async def get_context(self, session_id: str, budget_tokens: int):
        items = list(self.storage.get(session_id, []))
        # Trim hasta budget
        return trim_to_budget(items, budget_tokens)

    async def flush_to_short_term(self, session_id: str):
        # Al cerrar sesión, escribir batch a Tier 2 (Hipocampo)
        items = self.storage.pop(session_id, [])
        if items:
            await ShortTermMemory.store_batch(session_id, items)

    async def cleanup_expired(self):
        # Microglía Tier 1 (TTL 60 min)
        now = datetime.now()
        expired = [sid for sid, ts in self.last_access.items()
                   if (now - ts).total_seconds() > 3600]
        for sid in expired:
            await self.flush_to_short_term(sid)
            del self.storage[sid]
            del self.last_access[sid]
```

### Dependencias R3+

```
R5 (Orchestration):
   • Extiende WorkingMemory con planning state
   • Añade orchestrator/dmn.py (Nodo 7)
   • Añade orchestrator/action_selector.py (Nodo 5)
   • Añade dual-process check (sistema 1 vs 2)
   • Define metacognición (¿cómo va el agente?)

R6 (Memory extensions):
   • Posible Redis para working memory cross-procesos
```

### Riesgos y observaciones

```
⚠️ Working memory in-process → se pierde al reiniciar proceso
   Mitigación: Tier 2 (Hipocampo) tiene los eventos persistentes
✓ Latencia 0ms (in-process)
✓ Sin servicios extra v1
```

---

## 8. Nodo 4 — Ganglios Basales (Skills aprendidas)

### Función neurocientífica

Los **ganglios basales** almacenan y seleccionan **procedimientos aprendidos** (skills). El **refuerzo dopaminérgico** los fortalece: cuando un skill funciona (success), la dopamina refuerza esa vía neuronal. Con suficiente uso, los skills se vuelven **automáticos** (habit formation).

> En el cerebro biológico, los ganglios basales incluyen striatum, globus pallidus, sustancia nigra. Procesan recompensa y selección de acción. En For3s OS, modelamos skills como entidades con success_rate que se refuerza con uso exitoso.

### Status v1

```
✅ FULLY MAPPED (Bloques 1 + 2)
```

### Tablas SQL principales

```sql
-- Event Sourcing (inmutable)
CREATE TABLE wks_X.skills_events (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    skill_id        UUID NOT NULL,
    event_type      TEXT NOT NULL,  -- 'created', 'used', 'success', 'failure'
    event_version   INT NOT NULL DEFAULT 1,
    payload         JSONB NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    sequence_number BIGINT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    UNIQUE (skill_id, sequence_number)
);

CREATE TRIGGER no_modify_skills_events
    BEFORE UPDATE OR DELETE ON wks_X.skills_events
    FOR EACH ROW EXECUTE FUNCTION shared.prevent_audit_mutation();

-- State projection con success tracking
CREATE TABLE wks_X.skills_state (
    id                   UUID PRIMARY KEY,
    workspace_id         UUID NOT NULL,
    name                 TEXT NOT NULL,
    description          TEXT,
    code                 BYTEA,  -- cifrado P4

    -- Neuromodulación (Nodo 11)
    success_count        INT NOT NULL DEFAULT 0,
    failure_count        INT NOT NULL DEFAULT 0,
    success_rate         FLOAT GENERATED ALWAYS AS (
        CASE WHEN (success_count + failure_count) = 0 THEN 0.0
        ELSE success_count::float / (success_count + failure_count) END
    ) STORED,

    -- Embeddings para matching
    embedding            VECTOR(1024),
    embedding_model      TEXT NOT NULL DEFAULT 'stella:dunzhang_400M_v5@1024',

    -- Forgetting (skills protegidos con success_rate > 0.7)
    deleted_at           TIMESTAMPTZ,
    last_used_at         TIMESTAMPTZ,
    consolidated_to_kg   BOOLEAN NOT NULL DEFAULT false,

    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_skills_state_embedding
    ON wks_X.skills_state
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

CREATE INDEX idx_skills_state_success
    ON wks_X.skills_state (success_rate DESC)
    WHERE deleted_at IS NULL;

-- Archive
CREATE TABLE wks_X.skills_archived (
    LIKE wks_X.skills_state INCLUDING ALL,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    archive_reason TEXT
);
```

### Módulos Python responsables

```
for3s_os/memory/repository.py::SkillsRepository
   • create_skill(workspace, name, description, code)
   • use_skill(workspace, skill_id, success: bool)
   • match_skill(workspace, context_embedding, top_k)
   • get_high_performers(workspace, threshold=0.7)

for3s_os/memory/ranker.py
   • rank_skills_by_context(context, skills)
   • compute_skill_score(skill, context)  # similarity × success_rate
```

### Bloque(s) que lo materializa

```
B1 1.6 → skills_events ES tables
B2 2.2 → embeddings de contexto skill
B2 2.5 → forgetting policy (skills success_rate >0.7 NUNCA borrar)
B2 2.6 → CLS consolida skills frecuentes a KG
B2 2.7 → Mapeo documentado (este doc)
```

### Operaciones principales

```python
# 1. Crear skill nuevo (al aprender procedimiento)
async def create_skill(workspace, name, description, code, context):
    skill_id = uuid7()
    embedding = await embedder.embed(context)

    # Evento inmutable
    await db.execute("""
        INSERT INTO {workspace}.skills_events
        (skill_id, event_type, payload, sequence_number)
        VALUES ($1, 'created', $2, 1)
    """, skill_id, {'name': name, 'description': description})

    # State projection
    await db.execute("""
        INSERT INTO {workspace}.skills_state
        (id, workspace_id, name, description, code, embedding)
        VALUES ($1, $2, $3, $4, $5, $6)
    """, skill_id, workspace, name, description, encrypt(code), embedding)

# 2. Usar skill (refuerzo dopaminérgico — Nodo 11)
async def use_skill(workspace, skill_id, success: bool):
    event_type = 'success' if success else 'failure'

    # Evento inmutable
    await db.execute("""
        INSERT INTO {workspace}.skills_events
        (skill_id, event_type, sequence_number)
        VALUES ($1, $2, (
            SELECT COALESCE(MAX(sequence_number), 0) + 1
            FROM {workspace}.skills_events WHERE skill_id = $1
        ))
    """, skill_id, event_type)

    # Refuerzo: actualizar counts (success_rate se computa STORED)
    if success:
        await db.execute("""
            UPDATE {workspace}.skills_state
            SET success_count = success_count + 1,
                last_used_at = now()
            WHERE id = $1
        """, skill_id)
    else:
        await db.execute("""
            UPDATE {workspace}.skills_state
            SET failure_count = failure_count + 1,
                last_used_at = now()
            WHERE id = $1
        """, skill_id)

# 3. Matching skills por contexto (Nodo 5 action selection)
async def match_skill(workspace, context, top_k=5):
    ctx_embedding = await embedder.embed(context)
    return await db.execute("""
        SELECT *, (embedding <=> $1) * (1.0 - success_rate) as score
        FROM {workspace}.skills_state
        WHERE deleted_at IS NULL
        ORDER BY score ASC
        LIMIT $2
    """, ctx_embedding, top_k)
```

### Dependencias R3+

```
R3 (Model/LLM Layer):
   LLM ejecuta skills cuando matchean contexto

R4 (Tools/MCP):
   Tools MCP pueden registrar nuevas skills automáticamente

R5 (Orchestration):
   action_selector decide cuándo aplicar qué skill
```

### Riesgos y observaciones

```
✓ success_rate como columna GENERATED (siempre consistente)
✓ Skills high-performers (>0.7) protegidos de forgetting
✓ Cifrado de código sensible (P4)
⚠️ Embeddings de skills deben estar actualizados cuando código cambia
```

---

## 9. Nodo 5 — Ganglios Basales extensión (Action Selection)

### Función neurocientífica

Selección de acción entre alternativas competitivas. Trabaja junto al Nodo 4 (Skills) pero con rol específico de **"decidir qué hacer ahora"** ante un contexto dado. En el cerebro biológico, esto involucra el striatum + corteza motora.

### Status v1

```
🟡 FOUNDATION READY (R5 lo cierra)
```

### Tablas SQL

```
v1: Comparte con Nodo 4 (skills_state)
v2 (R5): Añadirá:
   • action_log (auditoría de decisiones)
   • decision_audit (qué consideró y por qué)
```

### Módulos Python

```
v1:
   for3s_os/memory/ranker.py (rank skills)

R5:
   for3s_os/orchestrator/action_selector.py
      • match_context(context) → candidate_skills
      • rank_candidates(skills, context) → top_action
      • log_decision(action, alternatives, rationale)
```

### Operaciones (v1 actual)

```python
# v1: lo básico vía ranker
async def select_action(workspace, context):
    # 1. Match skills por contexto (Nodo 4)
    candidates = await SkillsRepository.match_skill(workspace, context, top_k=5)

    # 2. Rankear por similarity × success_rate
    ranked = sorted(candidates, key=lambda s: s.score)

    # 3. Retornar top
    return ranked[0] if ranked else None

# R5 añadirá:
# - Multi-criteria ranking
# - Exploration vs exploitation (epsilon-greedy)
# - Log de decisión para audit
# - Fallback si confianza baja
```

### Dependencias R3+

```
R5 (Orchestration) lo cierra completamente
R8 (Observability) monitorea efectividad de selección
```

---

## 10. Nodo 6 — Microglía (forgetting / poda sináptica)

### Función neurocientífica

Las **microglías** son células gliales que **podan sinapsis débiles**. Mantienen el cerebro libre de ruido acumulado. Sin microglía sana, el cerebro desarrolla enfermedades neurológicas (esquizofrenia, autismo severo en teorías recientes).

> En el cerebro biológico, las microglías son ~10-15% de las células cerebrales. Activas durante el sueño podando sinapsis poco usadas. En For3s OS, modelamos esto como workers que soft-delete + decay + archive en 3 tiers.

### Status v1

```
✅ FULLY MAPPED (Bloque 2 sub-tema 2.5)
```

### Tablas SQL afectadas (modifica, no crea propias)

```
Modifica:
   • episodes_state (deleted_at, relevance_score, last_accessed_at)
   • skills_state (decay scores)
   • AGE edges (weight decay)

Escribe:
   • episodes_archived (cold storage)
   • skills_archived (cold storage)

Audit:
   • shared.audit_events (meta-audit de cada forgetting)
```

### Módulos Python responsables

```
for3s_os/memory/forgetter.py
   ├── WorkingMemoryForgetter
   │     async def cleanup_expired()  # TTL 60 min
   │     async def evict_lru_if_full()  # cap 15 items
   │
   ├── ShortTermForgetter
   │     async def soft_delete_stale()
   │     async def decay_relevance_scores()
   │     async def archive_soft_deleted()
   │     async def final_purge_archived()
   │     async def refresh_on_access(episode_id)
   │
   ├── LongTermForgetter
   │     async def decay_edge_weights()
   │     async def prune_weak_edges()
   │     async def review_orphan_nodes()
   │
   └── MicrogliaOrchestrator
         async def nightly_routine()
         async def weekly_routine()
         async def monthly_routine()
```

### Bloque(s) que lo materializa

```
B2 2.5 → política completa (Soft + Decay + Archive)
B2 2.7 → Mapeo documentado (este doc)
```

### Operaciones principales

```python
# Pipeline diario (orchestrator)
async def nightly_routine(workspace_id):
    audit_id = await audit_start('microglia:nightly', workspace_id)

    try:
        # 1. Working: limpia expired in-process
        await working_forgetter.cleanup_expired()

        # 2. Short: decay scores
        await short_forgetter.decay_relevance_scores(workspace_id)

        # 3. Short: soft delete stale + low relevance + consolidated
        deleted_count = await short_forgetter.soft_delete_stale(workspace_id)

        # 4. Long: decay edge weights
        await long_forgetter.decay_edge_weights(workspace_id)

        # 5. Meta-audit
        await audit_complete(audit_id, {
            'expired_working': ...,
            'decayed': ...,
            'soft_deleted': deleted_count,
            'edge_decayed': ...
        })
    except Exception as e:
        await audit_fail(audit_id, str(e))
        raise

# Soft delete con auditoría
async def soft_delete_stale(workspace_id):
    # Solo episodios que cumplen TODAS las condiciones:
    rows = await db.execute("""
        UPDATE {workspace}.episodes_state
        SET deleted_at = now()
        WHERE last_accessed_at < now() - interval '30 days'
          AND relevance_score < 0.3
          AND consolidated_to_kg = true
          AND legal_hold = false
          AND deleted_at IS NULL
        RETURNING id, relevance_score
    """)

    # Audit cada borrado (Pilar 1 §6.4)
    for row in rows:
        await audit.insert(
            action='forgetting:soft_delete',
            resource_type='episode',
            payload={
                'workspace_id': workspace_id,
                'episode_id': row.id,
                'reason': 'stale_30d + low_relevance + consolidated',
                'relevance_score': row.relevance_score,
                'reversible_until': (now + 30 days).isoformat()
            }
        )

    return len(rows)
```

### Excepciones inmutables (NUNCA tocar)

```
❌ audit_events (Pilar 1 §6.4) — inmutable por trigger Postgres
❌ episodes_events (ES) — inmutable por trigger
❌ skills_events (ES) — inmutable por trigger
❌ Skills con success_rate >0.7 (alta evidencia)
❌ Episodios con legal_hold = true
❌ Episodios NO consolidados (necesarios para CLS)
❌ Episodios referenciados desde Tier 3 KG (sources de concepts)

Solo PUEDE tocar:
✓ episodes_state (projection regenerable)
✓ skills_state (projection regenerable)
✓ AGE edges (con weight decay)
✓ Mover a episodes_archived (no delete)
```

### Coordinación crítica con otros nodos

```
Nodo 10 (CLS):
   ← CLS marca consolidated_to_kg = true
   → Microglía usa flag como condición soft delete

Nodo 11 (Neuromoduladores):
   ← Microglía respeta success_rate alto (>0.7) en skills
   ← Microglía respeta relevance_score alto

Pilar 1 (Audit chain):
   → Cada forgetting → INSERT audit_events
   ❌ NUNCA modifica audit_events ni events tables
```

### Dependencias R3+

```
R3 (Background jobs framework):
   nightly/weekly/monthly routines necesitan scheduler robusto
   Decisión en B3 sub-tema 3.2 (Celery vs Arq vs APScheduler)
```

---

## 11. Nodo 7 — DMN (Default Mode Network / idle compute)

### Función neurocientífica

La **DMN** es la red cerebral activa cuando NO hay tarea externa. Realiza **self-referential thinking, mind-wandering, planning futuro**. Es "lo que el cerebro hace cuando está libre". Históricamente subestimada, ahora se sabe que es crítica para creatividad, integración de experiencias, y planeación a largo plazo.

> Descubierta en 2001 por Marcus Raichle. Incluye corteza medial prefrontal, corteza cingulada posterior, lóbulos parietales inferiores. Su disfunción está implicada en depresión y autismo.

### Status v1

```
⏳ PENDIENTE (R5 lo define)
```

### Tablas SQL

```
v1: NINGUNA
R5: por definir
```

### Módulos Python

```
v1: NO existe
R5: for3s_os/orchestrator/dmn.py (futuro)
```

### Potencial design (sketch para R5)

```python
# Pseudocódigo R5:

class DefaultModeNetwork:
    """
    Worker idle que detecta inactividad del agente y ejecuta
    tareas 'background' creativas/integrativas.
    """

    async def detect_idle(self):
        # Si no hay sesiones activas por >5 min → activar DMN
        if not active_sessions and time_since_last > 300:
            await self.run_idle_routines()

    async def run_idle_routines(self):
        # Resumen del día/semana
        await self.summarize_recent_activity()

        # Identificar aprendizajes pendientes
        await self.identify_unconsolidated_learnings()

        # Pre-consolidación oportunista
        await self.opportunistic_consolidation()

        # Sugerencias proactivas (notificar usuario)
        await self.generate_proactive_suggestions()
```

### Bloque(s) que lo materializa

```
v1: ninguno (pendiente)
R5: lo define completo
```

### Dependencias R3+

```
R5 (Orchestration):
   Define el módulo dmn.py completo
   Coordina con Nodo 10 CLS y Nodo 6 Microglía
   Decide cuándo "el agente está idle"

R3 (LLM):
   Posibles LLM calls para resúmenes/sugerencias
```

### Razón de quedar PENDIENTE en v1

```
DMN es FUNCIONALIDAD AVANZADA — no MVP.
v1 enfoca en operaciones core (recall/store/consolidate/forget).
v2-v3: DMN añade "valor proactivo" del agente.

Brian podrá decidir en R5:
   • DMN activo cada 5 min de idle
   • DMN solo nocturno
   • DMN trigger manual ("agente, descansa y reflexiona")
```

---

## 12. Nodo 8 — Amígdala (policy enforcement / emotional gating)

### Función neurocientífica

La **amígdala** detecta amenazas + realiza **valoración emocional**. **Gates** qué memoria se prioriza (high-arousal events = priority). **Modula learning rate** según contexto emocional.

> En el cerebro biológico, amígdala está en lóbulo temporal medial. Crítica para memoria emocional. En For3s OS, modelamos esto como policy engine + RBAC + gating de retrieval.

### Status v1

```
🟡 FOUNDATION READY (B1 + R9 completa)
```

### Tablas SQL principales

```sql
-- Foundation B1
CREATE TABLE shared.security_policies (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID REFERENCES shared.workspaces(id),
    policy_type     TEXT NOT NULL,
    rules           JSONB NOT NULL,
    active          BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RBAC (B1)
CREATE TABLE shared.roles ( ... );
CREATE TABLE shared.user_roles ( ... );

-- R9 añadirá:
CREATE TABLE wks_X.policy_violations (
    id              UUID PRIMARY KEY,
    actor_id        UUID,
    action_attempted TEXT,
    policy_id       UUID,
    blocked_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Módulos Python

```
v1 (B1 foundation):
   • RBAC checks vía SQLAlchemy + middleware FastAPI
   • Encryption decisions vía pgcrypto (P4)

R9 (completo):
   for3s_os/security/policy_engine.py
      • check_action(actor, action, resource) → allow/deny
      • gate_retrieval(query, priority_filter)
      • log_violation(actor, action, policy)
```

### Extensiones PostgreSQL utilizadas

```
✓ pgcrypto (P4 encryption)
✓ RLS opcional (Row-Level Security) — v2 si necesario
```

### Bloque(s) que lo materializa

```
B1 → CRUD foundation (RBAC tables, policies, encryption)
B2 → priorización implícita vía relevance_score (ranker)
B2 2.7 → Mapeo documentado (este doc)
R9 → policy_engine completo
```

### Operaciones (v1 actual + R9 futuro)

```python
# v1: lo básico
async def check_rbac(user_id, workspace_id, action):
    role = await db.fetchone("""
        SELECT r.name FROM shared.user_roles ur
        JOIN shared.roles r ON r.id = ur.role_id
        WHERE ur.user_id = $1 AND r.workspace_id = $2
    """, user_id, workspace_id)

    return action_allowed_for_role(action, role.name)

# R9: lo completo
async def check_action(actor, action, resource):
    # 1. RBAC
    if not await check_rbac(actor.id, resource.workspace, action):
        await log_violation(actor, action, 'rbac_deny')
        raise PolicyDenied()

    # 2. Policy engine (custom rules)
    policies = await get_active_policies(resource.workspace)
    for policy in policies:
        if not policy.evaluate(actor, action, resource):
            await log_violation(actor, action, policy.id)
            raise PolicyDenied()

    # 3. Allow
    return True

# Gating de retrieval (emocional/prioridad)
async def gate_retrieval(query, results):
    # Priorizar high-relevance + high-severity
    return sorted(results, key=lambda r:
        (r.relevance_score * r.priority_weight))
```

### Dependencias R3+

```
R9 (Security/Compliance) lo extiende:
   • Policy engine completo
   • Audit trail de policy decisions
   • Cumplimiento SOC2/ISO27001
```

---

## 13. Nodo 9 — Pattern Separation (función hipocampal)

### Función neurocientífica

Distinguir episodios similares pero distintos. Crítico para NO confundir memorias parecidas. Función computacional del **giro dentado del hipocampo**. Sin pattern separation, recuerdos similares se sobreescribirían entre sí.

> Demostrado experimentalmente: ratones con giro dentado dañado confunden contextos espaciales similares. En For3s OS, lo modelamos como precision de HNSW recall + threshold de similarity en pre-insert checks.

### Status v1

```
✅ FULLY MAPPED (Bloque 1 + 2)
```

### Tablas SQL

```
Comparte tablas con Nodo 2 (Hipocampo).
La FUNCIÓN está en el HNSW index tuneado:

CREATE INDEX idx_episodes_state_embedding
    ON wks_X.episodes_state
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

-- Pattern Separation precision depende de:
-- m: max connections per node (16 default, mayor = mejor recall)
-- ef_construction: calidad del índice (128 tuneado, default 64)
-- ef_search: calidad query (100 tuneado, default 40)
```

### Extensiones PostgreSQL utilizadas

```
✓ pgvector con HNSW algorithm
   Parámetros tuneados para recall ~97-99%
```

### Módulos Python

```
for3s_os/memory/repository.py
   • find_similar() con ef_search configurable
   • Pre-insert check: si similarity > 0.95 → mergear, no duplicar

for3s_os/memory/ranker.py
   • Algoritmos de distinción fina entre top-K results
   • Re-ranking con metadata adicional
```

### Bloque(s) que lo materializa

```
B1 1.3 → pgvector + HNSW disponible
B2 2.2 → embeddings Stella (calidad MTEB 66.5)
B2 2.3 → params tuneados para recall ~97-99%
B2 2.7 → Mapeo documentado (este doc)
```

### Operaciones principales

```python
# 1. Pre-insert pattern separation check
async def store_episode_with_separation(workspace, event_data):
    # Generar embedding
    new_embedding = await embedder.embed(event_data.context)

    # Buscar episodios MUY similares
    similar = await db.execute("""
        SELECT id, embedding <=> $1 as distance
        FROM {workspace}.episodes_state
        WHERE embedding <=> $1 < 0.05  -- 0.05 distance = ~95% similarity
        AND deleted_at IS NULL
        ORDER BY distance LIMIT 1
    """, new_embedding)

    if similar and similar[0].distance < 0.05:
        # Merge en lugar de duplicar (Pattern Separation evita duplicación)
        await merge_with_existing(workspace, similar[0].id, event_data)
        return similar[0].id
    else:
        # Nuevo episodio (lo suficientemente distinto)
        return await store_new(workspace, event_data, new_embedding)

# 2. Top-K retrieval con distinción fina
async def recall_with_separation(workspace, query, k=10):
    query_vec = await embedder.embed(query)

    # ef_search alto = mejor pattern separation
    await db.execute("SET hnsw.ef_search = 100")

    results = await db.execute("""
        SELECT *, embedding <=> $1 as distance
        FROM {workspace}.episodes_state
        WHERE deleted_at IS NULL
        ORDER BY embedding <=> $1
        LIMIT $2
    """, query_vec, k)

    # Re-ranking para asegurar diversidad (MMR — Maximal Marginal Relevance)
    return apply_mmr(results, lambda_diversity=0.3)

# 3. Pattern completion (función inversa, usada en CLS)
async def find_similar_episodes_for_clustering(workspace):
    # HDBSCAN sobre embeddings extrae patrones
    vectors = await get_all_episode_embeddings(workspace)
    return HDBSCAN(min_cluster_size=3).fit_predict(vectors)
```

### Dependencias R3+

```
R3 (LLM Layer):
   LLM puede mejorar pattern separation con razonamiento

R6 (Memory extensions):
   Quantization puede afectar precisión — monitorear
```

### Riesgos y observaciones

```
✓ Recall ~97-99% con params tuneados (B2 2.3)
✓ Pre-insert check evita duplicación
⚠️ ef_search alto = más latencia (trade-off)
⚠️ Si quantization → puede degradar precision
```

---

## 14. Nodo 10 — Consolidación CLS (sleep cycle)

### Función neurocientífica

**CLS = Complementary Learning Systems** (McClelland, McNaughton & O'Reilly, 1995). Hipocampo → Neocorteza durante sueño. Convierte experiencia episódica en conocimiento semántico generalizado.

> Mecanismo: durante sueño REM y SWS (Slow Wave Sleep), el hipocampo "replayea" episodios al neocórtex. Las experiencias se integran en redes semánticas distribuidas. Lo episódico específico se generaliza en conceptos abstraídos.

> En For3s OS, replicamos esto con job nocturno que clusteriza episodios pendientes y extrae conceptos al KG.

### Status v1

```
✅ FULLY MAPPED (Bloque 2 sub-tema 2.6)
```

### Tablas SQL afectadas

```
Lee:
   • wks_X.episodes_state (Tier 2)
   • wks_X.skills_state (skills con uso reciente)

Escribe:
   • wks_X.concepts (nuevos conceptos)
   • wks_X.{age}.workspace_kg (nodos + aristas Cypher)

Modifica:
   • episodes_state (consolidated_to_kg = true)
   • skills_state (consolidated_to_kg = true)

Audit:
   • shared.audit_events (meta-audit por run)
```

### Extensiones PostgreSQL utilizadas

```
✓ pgvector (clustering + concept embeddings)
✓ Apache AGE (escribir nodos + aristas Cypher)
```

### Módulos Python responsables

```
for3s_os/memory/consolidator.py
   ├── ConsolidationPolicy (config por workspace)
   │     schedule: cron "0 2 * * *"  (2 AM diario)
   │     min_episodes_threshold: 10
   │     max_episodes_per_run: 500
   │     min_cluster_size: 3
   │     llm_model: "claude-haiku-4-5"
   │     llm_budget_per_run_usd: 0.10
   │     fallback_to_heuristic: True
   │
   ├── ClusteringEngine (HDBSCAN)
   │     async def cluster_episodes(episodes)
   │
   ├── ConceptExtractor (LLM Haiku focalizado)
   │     async def extract_concept(cluster_eps, llm_model)
   │     async def fallback_heuristic_concept(cluster_eps)
   │
   ├── KGPopulator (escribe Apache AGE)
   │     async def create_or_strengthen_node(meta)
   │     async def link_to_source_episodes(node, ep_ids)
   │
   └── CLSOrchestrator (coordina sleep cycle)
         async def run_consolidation(workspace_id)
```

### Bloque(s) que lo materializa

```
B2 2.6 → Híbrido Heurística + LLM completo
B2 2.7 → Mapeo documentado (este doc)
```

### Pipeline completo del sleep cycle

```python
async def run_consolidation(workspace_id):
    """Pipeline CLS — sleep cycle nocturno."""
    policy = await get_policy(workspace_id)
    audit_id = await audit_start('cls:run', workspace_id)

    try:
        # 1. Get pending episodes
        eps = await EpisodesRepository.get_pending_consolidation(
            workspace_id,
            limit=policy.max_episodes_per_run
        )

        # 2. Skip si <threshold (no vale la pena)
        if len(eps) < policy.min_episodes_threshold:
            await audit_skip(audit_id, 'below_threshold',
                            episodes=len(eps))
            return

        # 3. Clustering HDBSCAN sobre embeddings Stella
        vectors = [e.embedding for e in eps]
        labels = ClusteringEngine.cluster(vectors,
                                         min_size=policy.min_cluster_size)

        # 4. Por cluster: extract concept con LLM Haiku
        stats = {'created': 0, 'strengthened': 0, 'cost_usd': 0.0}
        for cluster_id in set(labels):
            cluster_eps = [e for e, l in zip(eps, labels) if l == cluster_id]

            try:
                # 4.1 Genera SUMMARY (no episodios crudos)
                summary = build_cluster_summary(cluster_eps)

                # 4.2 LLM call FOCALIZADA
                concept_meta = await ConceptExtractor.extract(
                    summary, policy.llm_model)

                stats['cost_usd'] += concept_meta.cost_usd

            except LLMError:
                if policy.fallback_to_heuristic:
                    # Heurística pura como fallback
                    concept_meta = await ConceptExtractor.fallback(cluster_eps)
                else:
                    raise

            # 5. KG populate
            existing = await KGPopulator.find_similar_concept(
                workspace_id, concept_meta.embedding)

            if existing and similarity > 0.85:
                # Strengthen edge (refuerzo)
                await KGPopulator.strengthen(existing, weight_delta=0.1)
                stats['strengthened'] += 1
            else:
                # Create new node
                node = await KGPopulator.create_node(workspace_id, concept_meta)

                # Crear aristas DERIVED_FROM hacia episodes
                await KGPopulator.link_to_episodes(
                    node, [e.id for e in cluster_eps])
                stats['created'] += 1

        # 6. Mark consolidated (trigger Microglía)
        await EpisodesRepository.mark_consolidated(
            workspace_id, [e.id for e in eps])

        # 7. Meta-audit
        await audit_complete(audit_id, {
            'episodes_processed': len(eps),
            'clusters_found': len(set(labels)),
            'concepts_created': stats['created'],
            'concepts_strengthened': stats['strengthened'],
            'cost_usd': stats['cost_usd'],
            'duration_seconds': elapsed
        })

    except Exception as e:
        await audit_fail(audit_id, str(e))
        raise
```

### Coordinación crítica con otros nodos

```
Nodo 2 (Hipocampo):
   ← CLS lee episodios pending de aquí
   → Marca consolidated_to_kg = true al procesarlos

Nodo 1 (KG):
   → CLS escribe nuevos nodos + aristas
   → Refuerza aristas existentes (weight++)

Nodo 4 (Skills):
   → Skills con high success_rate consolidan al KG

Nodo 9 (Pattern Separation):
   ↔ CLS hace PATTERN COMPLETION (inversa de Pattern Separation)
     Encuentra similitudes entre episodios distintos.

Nodo 6 (Microglía):
   → consolidated_to_kg = true ES la condición clave para
     soft delete en Microglía
   → Sin CLS, Microglía no sabe qué borrar
   → Sin Microglía, CLS satura Tier 2
   → SIMBIÓTICOS

Pilar 1 (Audit chain):
   → Meta-audit de cada run
   → Cumple Pilar 1 §6.4
```

### Costo y performance

```
Volumen v1 estimado:
   • 50 workspaces × 30 días × ~150 episodios/run = 225K eps/mes
   • Clusters generados: ~5-15 por workspace por run
   • LLM calls totales: ~9K-22K por mes
   • Tokens: ~5K input + ~3K output por workspace por run

Costo con Claude Haiku 4.5:
   • Input: $1 / 1M tokens
   • Output: $5 / 1M tokens
   • Total mensual estimado: ~$37/mes
   • % del techo P2 Pilot Light ($875): 1.1%
```

### Dependencias R3+

```
R3 (Model/LLM Layer):
   Provee modelo Claude Haiku 4.5 vía anthropic SDK

R3 3.2 (Jobs framework):
   Corre el cron (decisión en Bloque 3)

R8 (Observability):
   Monitorea costo + calidad de consolidación
```

---

## 15. Nodo 11 — Neuromoduladores (dopamina / serotonina / etc.)

### Función neurocientífica

Sistemas químicos que **modulan**: learning rate, atención, reward signaling, regulación emocional.

```
Neuromodulador     Función principal
─────────────────────────────────────────────
Dopamina           Refuerzo positivo (reward)
Serotonina         Mood, regulación, satisfacción
Noradrenalina      Atención, arousal
Acetilcolina       Atención, aprendizaje
GABA               Inhibición
Glutamato          Excitación
```

> En For3s OS v1, modelamos primariamente **dopamina** (success_rate como refuerzo) y **serotonina** (relevance_score como satisfacción/uso). Modulación dinámica completa llega en R5.

### Status v1

```
🟡 FOUNDATION READY (B1 + B2 parcial, R5 completa)
```

### Tablas SQL

```
v1: Modulación implícita en columnas existentes:
   • skills_state.success_rate (dopamina — Nodo 4)
   • episodes_state.relevance_score (serotonina — Nodo 2)
   • shared.workspace_config (CRUD — config global)

R5 añadirá:
   • agent_state con tunables dinámicos
   • neuromodulator_config por workspace
```

### Módulos Python

```
v1 (foundation):
   for3s_os/memory/forgetter.py (uso de scores)
   for3s_os/memory/ranker.py (priorización por scores)

R5 (completo):
   for3s_os/orchestrator/modulation.py
      • adjust_learning_rate(context)
      • boost_attention(focus_target)
      • compute_arousal(situation)
```

### Operaciones (v1 actuales)

```python
# Dopamina implícita: refuerzo de skills
await use_skill(workspace, skill_id, success=True)
# → success_rate++ automáticamente (Nodo 4)

# Serotonina implícita: refresh de episodios accedidos
await refresh_on_access(workspace, episode_id)
# → relevance_score = min(1.0, score + 0.2)

# Decay automático sin uso (todos los moduladores)
# Diario: -5% en scores sin actividad

# Priorización en ranker (usa scores)
async def rank_results(results):
    return sorted(results, key=lambda r:
        r.similarity * r.relevance_score * (1 + r.success_rate))
```

### Operaciones futuras (R5)

```python
# Modulación dinámica
class NeuromodulatorSystem:
    async def adjust_for_context(self, context):
        if context.is_high_stakes:
            # Aumenta atención (noradrenalina)
            self.attention_boost = 1.5
            # Aumenta learning rate (dopamina activa)
            self.learning_rate = 0.2
        else:
            self.attention_boost = 1.0
            self.learning_rate = 0.05

    async def compute_reward_signal(self, outcome):
        # RLHF-style en v3
        if outcome.user_satisfied:
            return 1.0  # dopamina alta
        elif outcome.user_corrected:
            return -0.5  # punishment signal
        return 0.0
```

### Bloque(s) que lo materializa

```
B2 2.5 → decay rates configurables (proto-modulación)
B2 2.6 → success_rate threshold para consolidación
B2 2.7 → Mapeo documentado (este doc)
R5 → modulación dinámica completa
```

### Dependencias R3+

```
R5 (Orchestration):
   Modulación dinámica based on context

R3 (LLM):
   Posible RLHF feedback como señal dopaminérgica explícita

R8 (Observability):
   Métricas de scores agregados
```

---

## 16. Diagrama visual completo de la arquitectura cerebral

```
                  FOR3S OS — Arquitectura cerebral completa
                  (vista funcional, todos los nodos)

   ┌─────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │   Cliente (humano) → Sesión activa (HTTP/Telegram → FastAPI)     │
   │                            │                                      │
   │                            ▼                                      │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ Nodo 3 — PFC (Working Memory, Tier 1)        🟡 PART. │      │
   │   │   for3s_os/memory/tiers.py::WorkingMemory              │      │
   │   │   • In-process Python (15 items LRU, TTL 60min)        │      │
   │   │   • Contexto activo de sesión                          │      │
   │   │   • R5 añadirá: planning, metacognición                 │      │
   │   └───────────────────────────────────────────────────────┘      │
   │            │                              ▲                       │
   │            │ flush al cerrar              │ load context           │
   │            ▼                              │                       │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ Nodo 2 — HIPOCAMPO (Short-term, Tier 2)       ✅ FULL │      │
   │   │   Postgres: episodes_events (ES inmutable)             │      │
   │   │           + episodes_state (projection)                 │      │
   │   │   pgvector HNSW @ 1024 cosine                          │      │
   │   │   Nodo 9 (Pattern Separation) activo aquí ──┐          │      │
   │   └───────────────────────────────────────────────────────┘      │
   │            │                                  │                   │
   │            │ sleep cycle (diario)              │ retrieval         │
   │            │                                  │ semántico         │
   │            ▼                                  ▼                   │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ Nodo 10 — CLS Consolidación                  ✅ FULL  │      │
   │   │   for3s_os/memory/consolidator.py                      │      │
   │   │   • HDBSCAN clustering                                  │      │
   │   │   • LLM Haiku 4.5 focalizado (summaries)                │      │
   │   │   • Pattern Completion (inversa de Pattern Separation)  │      │
   │   │   • marca consolidated_to_kg = true                     │      │
   │   └───────────────────────────────────────────────────────┘      │
   │            │                                                      │
   │            ▼                                                      │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ Nodo 1 — KG NEOCORTEZA (Long-term, Tier 3)   ✅ FULL  │      │
   │   │   Apache AGE: nodos + aristas Cypher                   │      │
   │   │   pgvector: embeddings de conceptos                     │      │
   │   │   Workspace subgraph (P3 isolation)                     │      │
   │   │   Razonamiento multi-hop semántico                       │      │
   │   └───────────────────────────────────────────────────────┘      │
   │            │                                                      │
   │            │ refuerza skills consolidadas                          │
   │            ▼                                                      │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ Nodo 4 — GANGLIOS BASALES (Skills)           ✅ FULL  │      │
   │   │   Postgres: skills_events + skills_state                │      │
   │   │   memory/repository.py::SkillsRepository                │      │
   │   │   Nodo 11 modula: success_rate++ (dopamina)             │      │
   │   └───────────────────────────────────────────────────────┘      │
   │            │                                                      │
   │            ▼                                                      │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ Nodo 5 — Action Selection                    🟡 FOUND │      │
   │   │   memory/ranker.py (v1 básico)                          │      │
   │   │   R5: orchestrator/action_selector.py                   │      │
   │   └───────────────────────────────────────────────────────┘      │
   │                                                                  │
   │   ╔═══════════════════════════════════════════════════════╗      │
   │   ║ Nodo 6 — MICROGLÍA (forgetting paralelo, nightly)      ║      │
   │   ║   ✅ FULL — for3s_os/memory/forgetter.py                ║      │
   │   ║   • WorkingMemoryForgetter (TTL + LRU)                  ║      │
   │   ║   • ShortTermForgetter (Soft+Decay+Archive)              ║      │
   │   ║   • LongTermForgetter (Edge weight decay + prune)        ║      │
   │   ║   • MicrogliaOrchestrator (coordinator)                  ║      │
   │   ║   PROHIBIDO tocar: audit_events, events tables          ║      │
   │   ╚═══════════════════════════════════════════════════════╝      │
   │                                                                  │
   │   ╔═══════════════════════════════════════════════════════╗      │
   │   ║ Nodo 11 — NEUROMODULADORES (modulación scores)         ║      │
   │   ║   🟡 FOUNDATION                                          ║      │
   │   ║   • Dopamina: success_rate++ en skills (Nodo 4)         ║      │
   │   ║   • Serotonina: relevance_score en episodios (Nodo 2)   ║      │
   │   ║   • R5: modulación dinámica completa                     ║      │
   │   ╚═══════════════════════════════════════════════════════╝      │
   │                                                                  │
   │   ╔═══════════════════════════════════════════════════════╗      │
   │   ║ Nodo 8 — AMÍGDALA (security/policy gating)             ║      │
   │   ║   🟡 FOUNDATION — shared.security_policies + RBAC      ║      │
   │   ║   security/policy_engine.py (futuro R9)                 ║      │
   │   ╚═══════════════════════════════════════════════════════╝      │
   │                                                                  │
   │   ╔═══════════════════════════════════════════════════════╗      │
   │   ║ Nodo 7 — DMN (idle compute)                            ║      │
   │   ║   ⏳ PENDIENTE — R5 lo define                           ║      │
   │   ║   orchestrator/dmn.py (futuro)                          ║      │
   │   ╚═══════════════════════════════════════════════════════╝      │
   │                                                                  │
   │   ╔═══════════════════════════════════════════════════════╗      │
   │   ║ Pilar 1 — AUDIT CHAIN (inmutable, NUNCA Microglía)     ║      │
   │   ║   shared.audit_events                                   ║      │
   │   ║   Hash chain criptográfico (§6.4 Grafo Maestro)         ║      │
   │   ║   Trigger Postgres rechaza UPDATE/DELETE                ║      │
   │   ║   META-AUDIT de Microglía + CLS + todas las ops         ║      │
   │   ╚═══════════════════════════════════════════════════════╝      │
   │                                                                  │
   └─────────────────────────────────────────────────────────────────┘
```

---

## 17. Diccionario bilingüe cerebral ↔ técnico

```
═══════════════════════════════════════════════════════════════════
ENTIDADES / CONCEPTOS
═══════════════════════════════════════════════════════════════════

TÉRMINO CEREBRAL                  TÉRMINO TÉCNICO FOR3S OS
─────────────────────────────────────────────────────────────────────
Knowledge Graph / Neocorteza      Apache AGE + pgvector concepts
Hipocampo                         pgvector + episodes_events ES
Memoria episódica                 Tier 2 (Postgres episodes)
Memoria semántica                 Tier 3 (Apache AGE)
Working Memory                    WorkingMemory in-process deque
PFC / Prefrontal Cortex           orchestrator/* (R5)
Ganglios Basales                  skills_events + skills_state
Striatum                          skills_state.success_rate
Microglía                         forgetter.py (Soft+Decay+Archive)
DMN / Default Mode Network        orchestrator/dmn.py (futuro R5)
Amígdala                          policy_engine.py (futuro R9) + RBAC
Neuromoduladores                  modulation scores (success_rate, etc.)
Dopamina                          success_rate++ en skill use
Serotonina                        relevance_score refresh on access
Noradrenalina                     attention boost (R5)
Sinapsis                          edges en AGE graph
Sinapsis débil                    edge weight < threshold
Pattern Separation                HNSW recall threshold + ef_search
Pattern Completion                HDBSCAN clustering (CLS)
Sleep cycle / SWS                 consolidator.py cron 2 AM
Consolidación de memoria          CLS pipeline (HDBSCAN + LLM Haiku)
Long-term Potentiation (LTP)      success_rate increase
Long-term Depression (LTD)        relevance_score decay
Neuroplasticidad                  Schema evolution + re-embedding
Trauma / Memoria imborrable       audit_events (hash chain inmutable)

═══════════════════════════════════════════════════════════════════
OPERACIONES
═══════════════════════════════════════════════════════════════════

OPERACIÓN CEREBRAL                OPERACIÓN CÓDIGO
─────────────────────────────────────────────────────────────────────
"Recordar"                        memory.recall(query, budget)
"Aprender"                        memory.store(episode/skill)
"Olvidar"                         forgetter.soft_delete()
"Consolidar"                      consolidator.run_consolidation()
"Razonar"                         LLM call con context built
"Reflexionar"                     DMN job (R5+)
"Decidir"                         action_selector (R5+)
"Reconocer"                       Pattern Separation HNSW similar
"Generalizar"                     Pattern Completion HDBSCAN
"Reforzar"                        success_rate++ / weight++
"Inhibir"                         relevance_score decay
"Atender"                         priorización en ranker
"Soñar / Procesar background"     DMN routines (R5+)

═══════════════════════════════════════════════════════════════════
CONDICIONES / ESTADOS
═══════════════════════════════════════════════════════════════════

ESTADO CEREBRAL                   ESTADO TÉCNICO
─────────────────────────────────────────────────────────────────────
Memoria fresca                    last_accessed_at recent
Memoria decayendo                 relevance_score < 0.3
Memoria reprimida                 deleted_at IS NOT NULL
Memoria archivada                 episodes_archived
Memoria consolidada               consolidated_to_kg = true
Skill automatizado                success_rate > 0.7
Skill abandonado                  last_used_at > 60 días ago
Concepto reforzado                reinforced_count > 10
Concepto esencial                 essential = true
Agente despierto                  active session
Agente durmiendo (CLS)            consolidator running
Agente idle (DMN)                 no active sessions (R5)
```

---

## 18. Operaciones cerebrales ↔ operaciones código

### Diccionario detallado de operaciones con ejemplos

```python
# ═══════════════════════════════════════════════════════════════
# "Recordar" → memory.recall()
# ═══════════════════════════════════════════════════════════════

# CEREBRAL: "¿Qué episodios similares tengo en mi memoria?"
# CÓDIGO:
async def recall(query: str, budget_tokens: int = 8000):
    # Tier 1 (working memory) — siempre incluido
    working_items = working_memory.get_context(budget=500)

    # Tier 2 (Hipocampo) — top-10 similares
    short_items = await ShortTermMemory.recall_similar(query, k=10)

    # Tier 3 (KG) — conceptos relacionados
    concepts = await LongTermMemory.find_related(query, k=5)

    # Mezcla con budget
    return build_context_within_budget(working_items, short_items,
                                       concepts, budget_tokens)

# ═══════════════════════════════════════════════════════════════
# "Aprender" → memory.store()
# ═══════════════════════════════════════════════════════════════

# CEREBRAL: "Esto es importante, lo voy a recordar."
# CÓDIGO:
async def store(workspace, event_data):
    # 1. Working memory (siempre)
    working_memory.add(session_id, event_data)

    # 2. Hipocampo (Tier 2)
    await ShortTermMemory.store_episode(workspace, event_data)

    # 3. Si es skill exitosa, registrar en Ganglios Basales
    if event_data.is_skill_application:
        await SkillsRepository.use_skill(workspace,
                                          event_data.skill_id,
                                          event_data.success)

# ═══════════════════════════════════════════════════════════════
# "Olvidar" → forgetter.soft_delete()
# ═══════════════════════════════════════════════════════════════

# CEREBRAL: "Esto ya no es relevante, lo dejo decaer."
# CÓDIGO (worker nightly Microglía):
async def forget_irrelevant(workspace):
    # NO toca: audit_events, events ES tables
    # SÍ toca: state projections

    await ShortTermForgetter.decay_relevance_scores(workspace)
    await ShortTermForgetter.soft_delete_stale(workspace)
    await LongTermForgetter.decay_edge_weights(workspace)

# ═══════════════════════════════════════════════════════════════
# "Consolidar" → consolidator.run_consolidation()
# ═══════════════════════════════════════════════════════════════

# CEREBRAL: "Voy a integrar las experiencias del día en conocimiento."
# CÓDIGO (worker nightly CLS):
async def consolidate(workspace):
    eps = await get_pending_episodes(workspace)

    if len(eps) < 10:
        return  # skip threshold

    clusters = HDBSCAN.cluster([e.embedding for e in eps])

    for cluster in clusters:
        summary = build_summary(cluster)
        concept = await LLM(Haiku).extract_concept(summary)
        await KG.create_or_strengthen(concept)

    await mark_consolidated([e.id for e in eps])

# ═══════════════════════════════════════════════════════════════
# "Reforzar" → success_rate++
# ═══════════════════════════════════════════════════════════════

# CEREBRAL: "Esta acción funcionó, refuerzo la conexión neuronal."
# CÓDIGO:
async def reinforce_skill(workspace, skill_id):
    await SkillsRepository.use_skill(workspace, skill_id, success=True)
    # success_rate aumenta automáticamente (columna GENERATED)
```

---

## 19. Flujos cross-nodo (cómo se comunican entre sí)

### Flujo 1 — Vida de un episodio (cradle to grave)

```
1. Usuario interactúa con For3s QA
   ↓
2. Nodo 3 (PFC/Working Memory)
   memory/tiers.py::WorkingMemory.add()
   → in-process Python deque
   ↓
3. Al cerrar sesión:
   Nodo 3 → Nodo 2 (Hipocampo)
   memory/tiers.py::WorkingMemory.flush_to_short_term()
   → INSERT episodes_events + UPDATE episodes_state
   → Genera embedding (Stella)
   → Index HNSW actualizado
   ↓
4. Nodo 9 (Pattern Separation) verifica
   memory/repository.py::store_episode_with_separation()
   → Si similarity > 0.95 → merge
   → Si distinto → store new
   ↓
5. Dormimos. Llega 2 AM.
   Nodo 10 (CLS) corre nightly
   memory/consolidator.py::run_consolidation()
   → Lee episodes pending
   → HDBSCAN clustering
   → LLM Haiku extrae conceptos
   → Crea/refuerza nodos en KG (Nodo 1)
   → Marca consolidated_to_kg = true
   ↓
6. Día siguiente: 2 AM Microglía corre
   Nodo 6 (Microglía) nightly_routine()
   memory/forgetter.py::ShortTermForgetter
   → Decay relevance_score (-5%)
   → Skip episodios usados hoy
   ↓
7. 30 días después si episodio NO se accede:
   → relevance_score < 0.3 + consolidated_to_kg = true
   → soft_delete: deleted_at = now()
   → audit_events: INSERT meta-audit
   ↓
8. 60 días después (30 más en soft-deleted):
   Nodo 6 archive_worker (weekly)
   → INSERT episodes_archived
   → DELETE FROM episodes_state
   ↓
9. 12 meses después en archived:
   Nodo 6 final_purge_worker (monthly)
   → DELETE FROM episodes_archived (hard)
   → audit_events: INSERT final purge

EPISODES_EVENTS NUNCA SE BORRA. Event sourcing inmutable.
   Solo state projections evolucionan.
```

### Flujo 2 — Recuperación de contexto para LLM

```
1. Usuario pregunta: "¿Es este PR riesgoso?"
   ↓
2. Nodo 3 (PFC) builds context:
   memory/api.py::build_context(query, budget=8000 tokens)
   ↓
3. Pull desde Tier 1 (Working) — últimos 5 items
   ↓
4. Pull desde Tier 2 (Hipocampo) — top-10 similar episodes
   Nodo 9 (Pattern Separation) asegura distinción
   HNSW @ ef_search=100
   ↓
5. Pull desde Tier 3 (KG/Neocorteza) — top-5 conceptos
   Apache AGE Cypher query
   ↓
6. Re-rank final con MMR (diversidad)
   ↓
7. Nodo 11 (Neuromoduladores) ajusta prioridades:
   priorización × success_rate × relevance_score
   ↓
8. Context compacto → LLM (R3 futuro)
   ↓
9. Respuesta al usuario
   ↓
10. Episodios accedidos → refresh_on_access()
    relevance_score += 0.2 (max 1.0)
```

### Flujo 3 — Skill ejecutada exitosamente

```
1. Agente decide ejecutar skill X
   Nodo 5 (Action Selection) selecciona
   ↓
2. Skill se ejecuta
   ↓
3. Si exitosa:
   Nodo 4 (Ganglios Basales) registra
   memory/repository.py::SkillsRepository.use_skill(success=True)
   → INSERT skills_events ('success')
   → UPDATE skills_state: success_count++
   → success_rate se recomputa (columna GENERATED)
   ↓
4. Nodo 11 (Neuromoduladores) dispara dopamina
   (implícito en success_rate++)
   ↓
5. Si skill alcanza success_rate > 0.7 sostenido:
   Nodo 10 (CLS) lo consolida al KG en próximo run
   → consolidated_to_kg = true
   → Crea/refuerza concepto en AGE
   ↓
6. Skill ahora protegida de Microglía
   (Excepción inmutable: success_rate > 0.7)
```

### Flujo 4 — Audit chain (Pilar 1)

```
1. Cualquier operación sensible:
   • Forgetting de episodio
   • Consolidación CLS
   • RBAC violation
   • Encryption key rotation
   • etc.
   ↓
2. INSERT shared.audit_events:
   (action, resource_type, resource_id, payload,
    previous_hash, event_hash, ...)
   ↓
3. Hash chain:
   event_hash = SHA256(previous_hash || payload || timestamp)
   ↓
4. Inmutabilidad enforced por trigger:
   no_modify_audit_events: rechaza UPDATE/DELETE
   ↓
5. Grants restringidos:
   for3s_app_role: GRANT INSERT, SELECT (NO UPDATE/DELETE)
   ↓
6. Verificación independiente posible:
   Cualquier auditor puede re-computar la chain y verificar
   que ningún evento fue tampered

NUNCA NUNCA NUNCA un nodo puede borrar audit_events.
Microglía explícitamente excluye audit_events.
CLS explícitamente excluye audit_events.
```

---

## 20. Excepciones inmutables (NUNCA tocar)

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   REGLAS INMUTABLES — VIOLAR ES BLOCKER EN CODE REVIEW         ║
║                                                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                                ║
║   1. shared.audit_events                                        ║
║      ❌ UPDATE        ❌ DELETE        ❌ TRUNCATE              ║
║      Razón: Pilar 1 Seguridad §6.4 — hash chain inmutable      ║
║      Enforcement: Trigger Postgres prevent_audit_mutation()    ║
║      Grants:  for3s_app_role tiene SOLO INSERT/SELECT          ║
║                                                                ║
║   2. wks_X.episodes_events                                      ║
║      ❌ UPDATE        ❌ DELETE        ❌ TRUNCATE              ║
║      Razón: Event Sourcing inmutable (P5 LOCKED)               ║
║      Enforcement: Trigger Postgres                              ║
║                                                                ║
║   3. wks_X.skills_events                                        ║
║      ❌ UPDATE        ❌ DELETE        ❌ TRUNCATE              ║
║      Razón: Event Sourcing inmutable (P5 LOCKED)               ║
║      Enforcement: Trigger Postgres                              ║
║                                                                ║
║   4. Skills con success_rate > 0.7                              ║
║      ❌ Microglía NO PUEDE soft-delete                          ║
║      Razón: Alta evidencia de utilidad (refuerzo dopaminérgico)║
║      Enforcement: Lógica en ShortTermForgetter                 ║
║                                                                ║
║   5. Episodios con legal_hold = true                            ║
║      ❌ Microglía NO PUEDE soft-delete                          ║
║      ❌ No archive automático                                   ║
║      Razón: Compliance / legal hold cliente                    ║
║      Enforcement: WHERE clause en queries de forgetting        ║
║                                                                ║
║   6. Episodios NO consolidados (consolidated_to_kg = false)    ║
║      ❌ Microglía NO PUEDE soft-delete                          ║
║      Razón: CLS aún no extrajo conocimiento                    ║
║      Enforcement: Condition en soft_delete_stale()              ║
║                                                                ║
║   7. Conceptos con essential = true                             ║
║      ❌ Microglía NO PUEDE eliminar                             ║
║      Razón: Conocimiento crítico marcado por humano/sistema    ║
║      Enforcement: Lógica en LongTermForgetter                  ║
║                                                                ║
║   8. Nombres de tablas / módulos en mapeo                       ║
║      ❌ NO renombrar sin actualizar este documento              ║
║      Razón: Bridge cerebral ↔ técnico se rompe                  ║
║      Enforcement: Code review obligatorio                       ║
║                                                                ║
║   9. Vocabulario cerebral del Grafo Maestro                     ║
║      ❌ NO renombrar nodos (Hipocampo, CLS, etc.)               ║
║      Razón: Identidad arquitectónica del proyecto               ║
║      Enforcement: For3s_OS_Grafo_Maestro.md es fuente verdad   ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 21. Protocolo de actualización del documento

### Cuándo actualizar este documento

```
ACTUALIZA cuando:
   ✓ Se añade un nuevo nodo cerebral al Grafo Maestro
   ✓ Un nodo cambia de status (PENDIENTE → FOUNDATION → FULLY)
   ✓ Se añade tabla nueva relacionada a un nodo
   ✓ Se renombra un módulo/archivo Python
   ✓ Se añade extensión PostgreSQL nueva
   ✓ Se modifica el flujo de comunicación entre nodos
   ✓ Se cierran rondas técnicas (R3, R4, R5, ...) que extienden nodos
   ✓ Se descubre una operación nueva que conecta a un nodo

NO ACTUALIZA por:
   ✗ Cambios cosméticos en código (rename de variable interna)
   ✗ Refactor sin cambio funcional
   ✗ Optimizaciones de performance sin cambio de arquitectura
   ✗ Bug fixes
```

### Cómo actualizar

```
1. Identifica qué nodo(s) afecta el cambio
2. Lee la sección §N del nodo afectado
3. Actualiza:
   - Status si cambió (FULLY/FOUNDATION/PENDIENTE)
   - Tablas SQL si se añadió/modificó
   - Módulos Python si cambiaron
   - Bloque(s) que lo materializa (añadir nueva ronda)
   - Operaciones si hay nuevas
   - Dependencias si cambiaron
4. Actualiza §4 TABLA MAESTRA con los cambios
5. Si hay nueva operación cerebral ↔ código, añadir a §17/§18
6. Si hay nuevo flujo cross-nodo, documentarlo en §19
7. Si hay nueva excepción inmutable, añadir a §20
8. Actualiza "Última actualización" arriba
```

### Ownership

```
Owner principal:      Brian López
Reviewers obligatorios:
   • Brian (cualquier cambio)
   • Cualquier dev tocando memory/, security/, orchestrator/

Cuando llegue equipo:
   • Cualquier hire que toque estos módulos
     DEBE leer este doc primero
   • Code reviews referencian este doc
```

### Versionado

```
Este documento NO usa versionado semántico.
Es DOCUMENTO VIVO con "Última actualización" en header.

Cambios significativos se loguean en:
   • for3s-inter/07-operations/decision-log.md (si afecta arquitectura)
   • Mente/Doc/Estado_Sesion_Continuidad.md (si afecta continuidad)
```

---

## Cierre — Por qué este documento importa

```
Sin este mapeo:
   • Devs perdidos entre "Hipocampo" vs "episodes_state"
   • Code reviews sin contexto cerebral
   • Cambios técnicos rompen alineación filosófica
   • Agente futuro pierde modelo mental

Con este mapeo:
   • Bridge explícito filosofía ↔ código
   • Todos hablan el mismo idioma
   • Code reviews informados
   • Continuidad cross-sesión garantizada
   • For3s OS sigue siendo "agente cerebral" no "wrapper LLM"

Este es el documento más importante para entender QUÉ ES For3s OS.
El Grafo Maestro dice POR QUÉ.
Las Rondas técnicas dicen CÓMO.
Este documento dice DÓNDE VIVE CADA POR QUÉ.
```

---

**Última actualización:** 2026-06-01 (creación inicial al cierre del Bloque 2 R2)
**Próxima actualización esperada:** Al cerrar Bloque 3 R2 (Performance & Async — añadir Redis si se LOCKEA, jobs framework, etc.)
**Documento canónico:** Mente/Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md