# For3s OS — Grafo Maestro de Conexiones

**El sistema completo como red de nodos: las 11 piezas cerebrales conectadas, con seguridad/encriptación, escalabilidad y autonomía generativa como propiedades estructurales**

**Owner:** Brian López
**Fecha:** 2026-05-28 (⚠️ actualizado 2026-06-10 — ver §0 Estado de Implementación)
**Estatus:** Mapa visual maestro. Iteración 1. **FUENTE DE VERDAD ARQUITECTÓNICA** (con §0 reconciliando tecnología vs rondas).
**Capa:** Cerebro — marco teórico estructural.
**Propósito:** Mostrar For3s OS como un GRAFO DE CONEXIONES completo — no piezas aisladas. Cada nodo, cada edge, cada flujo de información explícito. Con seguridad/escalabilidad/autonomía-generativa integradas estructuralmente desde día 1.
**Documentos ancla:**
- [Mente/Alma/Vision_For3s_Frontier.md](../Alma/Vision_For3s_Frontier.md)
- [Mente/Cerebro/Arquitectura_Grafo_vs_Loop.md](Arquitectura_Grafo_vs_Loop.md)
- [Mente/Cerebro/Cerebro_Humano_acercamiento1.md](Cerebro_Humano_acercamiento1.md)
- [Mente/Cerebro/Cerebro_Humano_acercamiento2.md](Cerebro_Humano_acercamiento2.md)
- [for3s-inter/03-security/security-principles.md](../../for3s-inter/03-security/security-principles.md)

---

## §0 — ESTADO DE IMPLEMENTACIÓN (añadido 2026-06-10 — LEER ANTES QUE NADA)

> **Este documento es el diseño conceptual fundacional (mayo 2026) y SIGUE SIENDO la autoridad arquitectónica:** los 11 nodos, los 24 edges, los 3 pilares, las reglas de autonomía (§8.3 niveles de aprobación, §8.4 límites duros) y las propiedades emergentes (§12) son LEY. Ninguna ronda los contradijo (verificado: `Doc/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md`, veredicto 9.2/10).
>
> **PERO:** las 10 rondas técnicas (`Mente/Cuerpo/Ronda_01..10`, junio 2026, 100% LOCKED) **materializaron** este grafo y, al hacerlo, eligieron tecnologías más afinadas que las nombradas aquí (este doc se escribió ANTES de las rondas). **Regla de precedencia: donde una tecnología nombrada abajo difiera de lo lockeado en una ronda, MANDA LA RONDA.** Este documento conserva la autoridad CONCEPTUAL (qué nodos, qué conexiones, qué reglas); la autoridad TÉCNICA (con qué se construye) vive en las rondas.

### §0.1 — Mapa de cambios tecnológicos (lo que dice este doc → lo lockeado)

| Dónde en este doc | Dice | Lo LOCKED real | Ronda |
|---|---|---|---|
| Nodo 1 (KG) | Neo4j / Memgraph | **Apache AGE** (extensión Postgres) | R2 B1 |
| Nodo 2 (Hipocampo) | Qdrant/pgvector | **pgvector + HNSW + Stella @1024 LOCAL** | R2 B2 |
| Pilar 2 | Kafka/Redis Streams + service mesh | **Valkey + Arq** (sin Kafka, sin mesh) | R2 B3 |
| Nodo 3 (PFC) | LLM + LangGraph | **Claude + orquestación custom Python/asyncio** (sin LangGraph) | R3/R5/R6 |
| Nodo 4 (Skills) | Markdown library + embedding index | **filesystem .md + Postgres + pgvector** | R6 |
| Nodo 7 (Amígdala) | "modelo pequeño + reglas" | **scanner 5 capas + Haiku 4.5 classifier** | R9 |
| §7.2 (escala) | Spot instances / edge deployment | **hardware LOCAL Brian (D-009), systemd+Docker** | R10 |
| Nodo 2 (persistencia) | SQLAlchemy 2 + Alembic (R2 B1) | **asyncpg directo + migraciones SQL numeradas** (H2, sin ORM) | R2→H2 |

→ El stack completo consolidado vive en `Doc/Reporte_Maestro_Consolidado_R1-R10.md` §3.

### §0.2 — Desviaciones estructurales registradas (justificadas, NO contradicciones)

1. **Pilar 2 en v1 = MONOLITO MODULAR, no microservicios.** Este doc dice "cada nodo es un servicio independiente". La decisión LOCKED (D-009 + R2 + R10) es: v1 corre como monolito modular en una sola máquina (hardware local de Brian), con los nodos como módulos con interfaces limpias — el diseño PERMITE extraerlos a servicios cuando la escala lo exija (v2/v3). Razón: ancla 3.D (equipo pequeño) — un solo deploy, un solo backup, operable por 1 persona.
2. **Pilar 3 en v1 = SOLO la capacidad generativa #1 (skills).** Este doc lista 4 capacidades (§8.1: skills, relaciones KG, sub-agentes, modos). En v1 solo se activa la #1, gobernada por el Meta-Orchestrator (detallado post-diseño en `Cuerpo/Ronda_06_Pre_Code_Review_Detailed.md` — governor 6 frenos + kill switch). Las #2/#3/#4 quedan diferidas a v3. Razón: soltar autonomía gradualmente, freno antes que motor.
3. **Capa de datos en construcción (H2) = asyncpg directo + migraciones SQL numeradas, sin ORM.** R2 B1 lockeó "SQLAlchemy 2 + Alembic". Al programar H2 se eligió SQL directo con asyncpg (R2 ya lockeó asyncpg) + un runner de migraciones SQL versionadas (`migrations/NNN_*.sql` + tabla `schema_version`) en vez de Alembic ORM. Razón: para el esquema actual (pocas tablas + triggers + audit chain que es SQL puro) es más simple, transparente y auditable, y conserva evolución versionada del esquema. Si el ORM se vuelve necesario al crecer (H5+), se reevalúa. Registrado 2026-06-11 (ticket 002).

### §0.3 — Reconciliación "cobertura cerebral %" vs "11/11 nodos"

Las dos afirmaciones son ciertas a la vez: **los 11 nodos EXISTEN en v1 (ancho completo del grafo), pero a una profundidad ≈40% de la capacidad cerebral total** que la Visión contempla (predictive coding, capacidades generativas #2-4, Tree/Graph of Thoughts y modos avanzados quedan diferidos a v2/v3+). Es decir: **11/11 = ancho · ~40% = profundidad v1.** Ningún nodo falta; varios operan en su versión foundation.

### §0.4 — Dónde está el resto de la verdad

- **El ORDEN de construcción:** `Doc/Plan_Maestro_Programacion.md` (6 fases foundation-first).
- **El TIEMPO:** `Doc/Estimacion_Tiempo_Por_Subtema.md` (~9-10 meses Brian solo; MVP ~3.5-4).
- **La coherencia interna de las rondas:** `Doc/Reporte_Maestro_Consolidado_R1-R10.md`.
- **La numeración canónica de nodos:** este doc §4 = Visión §6.1 = `Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md` §0.

---

## Por qué este documento existe

Los documentos anteriores describieron las **piezas** del cerebro de For3s (acercamiento 1 y 2) y la **arquitectura de ejecución** (grafo vs loop). Pero **no había un mapa visual maestro** que mostrara TODO el sistema como una red de nodos conectados, donde se vea de un vistazo:

- Las 11 piezas cerebrales como nodos
- Qué información fluye por cada conexión
- Dónde vive la seguridad/encriptación (no como capa aparte sino como propiedad de cada edge)
- Cómo se escala cada nodo independientemente
- Cómo el sistema **genera nuevos nodos y conexiones por sí mismo** (autonomía generativa)

Tú lo nombraste: *"considera muy bien los pilares: Seguridad (encriptación), Escalabilidad tiene que ser escalable, autónomo que sea capaz de generar nuevas neuronas y nuevos sistemas de aprendizaje."*

Estos 3 pilares **no son features añadidas**. Son **propiedades estructurales** que tienen que estar en cada nodo y cada edge del grafo desde el principio. Por eso este documento existe.

---

## Tabla de contenidos

1. [Los 3 pilares estructurales](#1-los-3-pilares-estructurales)
2. [Convenciones del grafo](#2-convenciones-del-grafo)
3. [El grafo maestro completo](#3-el-grafo-maestro-completo)
4. [Los 11 nodos cerebrales en detalle](#4-los-11-nodos-cerebrales-en-detalle)
5. [Los 24 edges principales — qué fluye por cada uno](#5-los-24-edges-principales--qué-fluye-por-cada-uno)
6. [Capa de seguridad — cómo se entrelaza con todo](#6-capa-de-seguridad--cómo-se-entrelaza-con-todo)
7. [Capa de escalabilidad — escalado por nodo](#7-capa-de-escalabilidad--escalado-por-nodo)
8. [Capa de autonomía generativa — el sistema crece solo](#8-capa-de-autonomía-generativa--el-sistema-crece-solo)
9. [Flujos de información completos (3 casos de uso)](#9-flujos-de-información-completos-3-casos-de-uso)
10. [Cómo nace una neurona nueva en For3s OS](#10-cómo-nace-una-neurona-nueva-en-for3s-os)
11. [Cómo nace un sistema de aprendizaje nuevo](#11-cómo-nace-un-sistema-de-aprendizaje-nuevo)
12. [Propiedades emergentes del grafo](#12-propiedades-emergentes-del-grafo)
13. [Lo que este grafo NO es todavía](#13-lo-que-este-grafo-no-es-todavía)
14. [Cierre](#14-cierre)

---

## 1. Los 3 pilares estructurales

Antes del grafo, los pilares. Cada uno cambia cómo se diseña cada nodo y cada edge.

### Pilar 1 — Seguridad (Encriptación end-to-end)

**Anclado en** [for3s-inter/03-security/security-principles.md](../../for3s-inter/03-security/security-principles.md) §5.6 y §6.1.

**Decisión locked:**
- End-to-end encryption es requirement v1
- Workspaces privados por default
- Customer data ≠ training data
- ZK / RISC Zero como dirección de investigación a largo plazo

**Implicación estructural en el grafo:**

```
   Cada EDGE del grafo lleva información ENCRIPTADA.
   Cada NODO tiene una zona de "decrypted operation"
   limitada al mínimo necesario.
   Cada NODO declara explícitamente:
       - Qué keys tiene acceso a usar
       - Cuánto tiempo retiene el plaintext
       - Qué workspace pertenece la operación
```

**Esto no es una capa encima del grafo. Es propiedad de cada conexión.**

### Pilar 2 — Escalabilidad

**Decisión:** cada nodo debe poder escalar **independientemente** del resto. No hay nodo monolítico. Si el HIPOCAMPO se vuelve cuello de botella, escala solo HIPOCAMPO sin tocar nada más.

**Implicación estructural:**

```
   • Cada nodo es un SERVICIO INDEPENDIENTE
     (microservicio o equivalente)
   • Cada edge es una COLA/STREAM, no llamada síncrona
     directa cuando es posible
   • Cada nodo tiene SHARDING por workspace
   • Las queries son IDEMPOTENTES por diseño
   • El sistema soporta HORIZONTAL SCALING en cada nodo
```

**Esto cambia tooling:** no es solo "Python + LangGraph". Es Python + LangGraph + Kafka/Redis Streams + sharded DBs + service mesh.

> ⚠️ **Nota de implementación (2026-06-10, ver §0.2):** en v1 LOCKED este pilar se materializa como **monolito modular** (Valkey+Arq, sin Kafka/mesh/LangGraph, hardware local D-009) con nodos como módulos extraíbles. "Cada nodo escala independiente" se cumple a nivel de DISEÑO de interfaces; la extracción a servicios independientes es v2/v3, cuando la escala lo exija.

### Pilar 3 — Autonomía Generativa

**Esto es lo más radical.** El sistema debe poder:
- Generar **neuronas nuevas** (skills, sub-agentes, nodos de razonamiento) sin intervención humana
- Crear **sistemas de aprendizaje nuevos** cuando detecta una clase de problema no resuelta
- Modificar su **propio grafo** en runtime cuando una conexión nueva tiene valor

**Análogo cerebral:**
- Neurogénesis adulta en hipocampo (~700 neuronas nuevas/día)
- Sinaptogénesis con la experiencia
- Reorganización funcional ante nueva demanda

**Implicación estructural:**

```
   • Cada nodo tiene un "modo aprendizaje" donde
     puede generar sub-nodos
   • Existe un META-ORCHESTRATOR (sobre el PFC normal)
     que detecta cuando el grafo necesita extenderse
   • Las nuevas neuronas nacen, se prueban en sandbox,
     se evalúan, y se promueven al grafo "vivo"
   • La microglía artificial también pode neuronas
     que no demostraron valor
```

**Esto NO existe en NINGÚN agente actual.** Es la pieza más diferenciadora de For3s OS.

---

## 2. Convenciones del grafo

Para que el grafo sea legible:

```
   NODOS — tipos:
   ╔═══════════╗  Nodo CEREBRAL (las 11 piezas)
   ║   NODO    ║
   ╚═══════════╝

   ┌───────────┐  Nodo de PROCESO DE FONDO (continuo)
   │   NODO    │
   └───────────┘

   ┌╌╌╌╌╌╌╌╌╌╌╌┐  Nodo GENERATIVO (puede crear sub-nodos)
   ╎   NODO    ╎
   └╌╌╌╌╌╌╌╌╌╌╌┘

   ▓▓▓▓▓▓▓▓▓▓▓   Nodo de INFRAESTRUCTURA DE SEGURIDAD
   ▓   NODO   ▓   (keys, vault, audit, etc.)
   ▓▓▓▓▓▓▓▓▓▓▓

   EDGES — anotaciones:
   ──────►        Edge plano (información encriptada por default)
   ══════►        Edge con CONTROL (auth, audit, rate limit)
   ╌╌╌╌╌╌►        Edge GENERATIVO (puede crear nuevos edges)
   ◄═════►        Edge BIDIRECCIONAL con feedback loop

   Cada edge en el grafo real lleva metadata:
   { workspace_id, encryption_key_id, audit_trail, latency_budget }
```

---

## 3. El grafo maestro completo

Aquí está el sistema completo en una sola vista. Después vamos pieza por pieza.

```
═════════════════════════════════════════════════════════════════════════════
                  FOR3S OS — GRAFO MAESTRO DE CONEXIONES
═════════════════════════════════════════════════════════════════════════════

                ┌───────────────────────────────────────────┐
                │            INPUT (Usuario / API)          │
                │   PR · Query · Comando · Webhook · CI/CD  │
                └────────────────────┬──────────────────────┘
                                     │ ══►  [E1] auth + encrypt
                                     ▼
                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                ▓        WORKSPACE GATE (Seguridad)         ▓
                ▓   • Valida workspace_id                   ▓
                ▓   • Carga keys del workspace              ▓
                ▓   • Marca audit_trail                     ▓
                ▓   • Aplica RBAC                           ▓
                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                                     │ ══►  [E2]
                                     ▼
                ╔═══════════════════════════════════════════╗
                ║       TÁLAMO (Nodo 8 — Router)            ║
                ║   Decide qué subsistemas activar          ║
                ║   • Subgrafo mínimo                       ║
                ║   • Subgrafo completo                     ║
                ║   • Subgrafo emergencia                   ║
                ╚────────┬───────────────────────┬──────────╝
                         │ ──►[E3]               │ ──►[E4]
                         ▼                       ▼
                ╔════════════════╗      ╔════════════════╗
                ║   AMÍGDALA     ║      ║      PFC       ║
                ║  (Nodo 7)      ║◄════►║   ORCHESTRATOR ║
                ║                ║ [E5] ║   (Nodo 3)     ║
                ║ Triaje rápido  ║ ════►║  Metacognición ║
                ║ Valoración     ║      ║  + Planning    ║
                ║ instantánea    ║      ║                ║
                ╚════════════════╝      ╚════════╤═══════╝
                                                 │
                                                 │ orquesta
                              ┌──────────────────┼──────────────────┐
                              │                  │                  │
                              ▼ [E6]             ▼ [E7]             ▼ [E8]
                    ╔════════════════╗ ╔════════════════╗ ╔════════════════╗
                    ║   HIPOCAMPO    ║ ║  KNOWLEDGE     ║ ║  GANGLIOS      ║
                    ║   (Nodo 2)     ║ ║  GRAPH         ║ ║  BASALES       ║
                    ║                ║ ║  (Nodo 1)      ║ ║  (Nodo 4)      ║
                    ║ Episódica      ║ ║                ║ ║                ║
                    ║ + Pattern Sep  ║ ║ Semántica      ║ ║ Skills QA      ║
                    ║                ║ ║ estructurada   ║ ║ procedurales   ║
                    ║ Cada evento    ║ ║                ║ ║                ║
                    ║ con metadata:  ║ ║ Nodos +        ║ ║ Vía GO         ║
                    ║ - timestamp    ║ ║ relaciones     ║ ║ Vía NO-GO      ║
                    ║ - workspace    ║ ║                ║ ║                ║
                    ║ - trigger      ║ ║ Auditable      ║ ║ Dopamina-style ║
                    ║ - confidence   ║ ║ multi-salto    ║ ║ reinforcement  ║
                    ╚════════╤═══════╝ ╚════════╤═══════╝ ╚════════╤═══════╝
                             │                  │                  │
                             │ [E9]             │ [E10]            │ [E11]
                             └──────────────────┼──────────────────┘
                                                │
                                                ▼
                              ╔═══════════════════════════════════╗
                              ║    MULTI-AGENT NETWORK (Grafo)    ║
                              ║                                   ║
                              ║  ┌─────────┐ ┌─────────┐          ║
                              ║  │Analyzer │ │History  │          ║
                              ║  │         │ │Detective│          ║
                              ║  └────┬────┘ └────┬────┘          ║
                              ║       │           │               ║
                              ║  ┌────┴───────────┴────┐          ║
                              ║  │   Synthesizer       │          ║
                              ║  └────┬────────────────┘          ║
                              ║       │                           ║
                              ║  ┌────┴────┐ ┌─────────┐          ║
                              ║  │Risk     │ │Test     │          ║
                              ║  │Scorer   │ │Generator│          ║
                              ║  └────┬────┘ └────┬────┘          ║
                              ║       │           │               ║
                              ║  ┌────┴───────────┴────┐          ║
                              ║  │    Reviewer         │          ║
                              ║  └────┬────────────────┘          ║
                              ╚═══════╪═══════════════════════════╝
                                      │ [E12]
                                      ▼
                ╔═══════════════════════════════════════════╗
                ║   DUAL-PROCESS CHECK (Nodo 9)             ║
                ║   ¿Es claro? → output directo             ║
                ║   ¿Es complejo? → análisis profundo       ║
                ╚────────────────────┬──────────────────────╝
                                     │ [E13]
                                     ▼
                ╔═══════════════════════════════════════════╗
                ║   CONFIDENCE CHECK (PFC metacognición)    ║
                ║                                           ║
                ║   confidence < threshold ──► ask human    ║
                ║   confidence >= threshold ──► proceed     ║
                ╚────────────────────┬──────────────────────╝
                                     │ ══►  [E14] audit + encrypt
                                     ▼
                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                ▓    OUTPUT GATE (Seguridad + Trazabilidad)▓
                ▓   • Firma criptográfica del output       ▓
                ▓   • Trace completo: qué nodos decidieron ▓
                ▓   • Encripta para entrega                ▓
                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                                     │
                                     ▼
                ┌───────────────────────────────────────────┐
                │            OUTPUT (Usuario / API)         │
                │   QA Pack + Trace + Confidence + Audit   │
                └───────────────────────────────────────────┘

   ═════════════════════════════════════════════════════════════════════════
   PROCESOS DE FONDO (corren continuamente, no por request del usuario)
   ═════════════════════════════════════════════════════════════════════════

   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
   │  MICROGLÍA      │  │ CONSOLIDACIÓN   │  │      DMN        │
   │  (Nodo 5)       │  │ CLS (Nodo 10)   │  │   (Nodo 6)      │
   │                 │  │                 │  │                 │
   │ Poda memoria    │  │ Episódica       │  │ Reflexión       │
   │ obsoleta        │  │ ──► semántica   │  │ offline         │
   │                 │  │                 │  │                 │
   │ Marca para      │  │ "Sueño SWS"     │  │ Re-juega        │
   │ archivo o       │  │ del agente      │  │ escenarios      │
   │ borrado         │  │                 │  │                 │
   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
            │                    │                    │
            │ [E15]              │ [E16]              │ [E17]
            └────────────────────┼────────────────────┘
                                 │
                                 ▼
                    ╔═══════════════════════════╗
                    ║  NEUROMODULADORES         ║
                    ║  (Nodo 11)                ║
                    ║                           ║
                    ║  Modos globales:          ║
                    ║  • exploración            ║
                    ║  • consolidación          ║
                    ║  • alta atención          ║
                    ║  • reposo                 ║
                    ║                           ║
                    ║  Ajustan parámetros       ║
                    ║  de TODOS los nodos       ║
                    ╚═══════════════════════════╝

   ═════════════════════════════════════════════════════════════════════════
   AUTONOMÍA GENERATIVA (el sistema crece solo)
   ═════════════════════════════════════════════════════════════════════════

   ┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐
   ╎                                                                  ╎
   ╎          META-ORCHESTRATOR (sobre todo el sistema)               ╎
   ╎                                                                  ╎
   ╎  • Detecta patrones de fallo recurrentes en el grafo             ╎
   ╎  • Identifica clases de problemas no cubiertas                   ╎
   ╎  • Propone nuevas neuronas o sistemas de aprendizaje             ╎
   ╎  • Sandboxea propuestas, mide impacto                            ╎
   ╎  • Promueve neuronas exitosas al grafo vivo                      ╎
   ╎  • Marca neuronas inútiles para que MICROGLÍA las pode           ╎
   ╎                                                                  ╎
   └╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘
                              ╌╌╌╌╌╌╌╌╌╌╌► hacia cualquier nodo

   ═════════════════════════════════════════════════════════════════════════
   INFRAESTRUCTURA DE SEGURIDAD (transversal a todo)
   ═════════════════════════════════════════════════════════════════════════

   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
   ▓  KEY VAULT      ▓   ▓  AUDIT LOG      ▓   ▓ ZK / RISC ZERO ▓
   ▓                 ▓   ▓                 ▓   ▓ (research)     ▓
   ▓ Per-workspace   ▓   ▓ Append-only     ▓   ▓                ▓
   ▓ Per-node        ▓   ▓ Cryptographic   ▓   ▓ Future:        ▓
   ▓ Rotación        ▓   ▓ chain           ▓   ▓ verifiable     ▓
   ▓                 ▓   ▓                 ▓   ▓ computation    ▓
   ▓ Client-managed  ▓   ▓ Toda decisión   ▓   ▓                ▓
   ▓ keys (roadmap)  ▓   ▓ del grafo       ▓   ▓                ▓
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
```

Este es el grafo maestro. Las siguientes secciones lo desmenuzan pieza por pieza.

---

## 4. Los 11 nodos cerebrales en detalle

Cada nodo con: análogo cerebral, función, inputs, outputs, propiedades de seguridad, estrategia de escalado, capacidad generativa.

### Nodo 1 — Knowledge Graph (Neocorteza semántica)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Neocorteza semántica |
| **Función** | Conocimiento general estructurado del workspace: entidades, relaciones, hechos consolidados |
| **Inputs** | Hechos consolidados (vía Nodo 10), edges nuevos (vía Multi-Agent), queries (vía PFC) |
| **Outputs** | Contextos estructurados navegables, multi-hop reasoning |
| **Tecnología** | Neo4j / Memgraph + capa de aplicación propia |
| **Seguridad** | Cada subgrafo encriptado por workspace_id. Queries autenticadas. Nunca cruza workspace boundary. |
| **Escalabilidad** | Sharded por workspace_id. Read replicas. Cache de subgrafos calientes. |
| **Capacidad generativa** | El Meta-Orchestrator puede **proponer nuevos tipos de entidades** o **relaciones** cuando detecta patrones recurrentes |

### Nodo 2 — Hipocampo + Pattern Separation (Memoria episódica)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Hipocampo (giro dentado + CA3/CA1) |
| **Función** | Memoria episódica de eventos únicos con metadata rica para pattern separation |
| **Inputs** | Eventos del flujo (PR analizados, bugs encontrados, decisiones tomadas) |
| **Outputs** | Episodios específicos con contexto temporal + multi-dimensional |
| **Tecnología** | Vector DB (Qdrant/pgvector) con metadata rica + capa propia de pattern separation |
| **Seguridad** | Cada episodio encriptado, accessible solo dentro de workspace_id. Pattern separation impide fuga cross-workspace incluso si los embeddings se parecen. |
| **Escalabilidad** | Sharded por workspace + tiempo. Tier hot/warm/cold con costo decreciente. |
| **Capacidad generativa** | Puede crear **nuevas dimensiones de pattern separation** cuando el Meta-Orchestrator detecta que la existente no distingue bien una clase de eventos |

### Nodo 3 — PFC / Orchestrator (Corteza prefrontal)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Corteza prefrontal dorsolateral + ventromedial |
| **Función** | Control ejecutivo, planning, metacognición ("¿qué estrategia uso? ¿confío en mi output?") |
| **Inputs** | Query del usuario, contexto del Tálamo, señal de Amígdala |
| **Outputs** | Plan de ejecución, decisiones de routing, confidence scores |
| **Tecnología** | LLM (Claude Sonnet) + lógica de planning explícita + LangGraph |
| **Seguridad** | Acceso a keys del workspace activo solamente. Logs todas las decisiones de planning. |
| **Escalabilidad** | Stateless por sesión, escala horizontal trivialmente. Caching de planes recurrentes. |
| **Capacidad generativa** | Puede **proponer nuevos planes** y, vía Meta-Orchestrator, **promoverlos** a templates reutilizables (skills) |

### Nodo 4 — Ganglios Basales QA (Skills procedurales)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Estriado (putamen + caudado) + sustancia negra (dopamina) |
| **Función** | Memoria procedural especializada: "cómo se prueba este tipo de feature" |
| **Inputs** | Patrones repetidos detectados, feedback de éxito/fallo de tests generados |
| **Outputs** | Skills aplicables a nuevos casos, vía GO (qué hacer) + vía NO-GO (qué evitar) |
| **Tecnología** | Markdown library + embedding index + dopaminergic-style scoring |
| **Seguridad** | Skills NO se comparten entre workspaces (skills aprendidas con cliente X no se aplican a cliente Y sin permiso explícito). Skills del "stack común QA" sí son compartidas. |
| **Escalabilidad** | Skills indexadas. Búsqueda por intent. Lazy loading. |
| **Capacidad generativa** | **Núcleo de la autonomía generativa.** El sistema **escribe sus propias skills** cuando resuelve un problema repetidamente. Vía NO-GO también aprende qué tests NO generar. |

### Nodo 5 — Microglía (Olvido inteligente)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Microglía (sistema inmune del cerebro) |
| **Función** | Poda activa de memoria episódica obsoleta o consolidada |
| **Inputs** | Scan periódico de Hipocampo + signals de "ya consolidado en Knowledge Graph" |
| **Outputs** | Episodios marcados para archivo, comprimir, o borrar |
| **Tecnología** | Job periódico (cron-like) + scoring de relevancia + políticas por workspace |
| **Seguridad** | Borrado verificable. Audit log de qué se podó y por qué. Soporta "right to be forgotten" GDPR. |
| **Escalabilidad** | Job distribuido, paralelizable por workspace. |
| **Capacidad generativa** | Puede **proponer nuevas políticas de poda** cuando detecta clases de memorias que siempre se podan o nunca se consultan |

### Nodo 6 — DMN (Default Mode Network)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Default Mode Network (mPFC + PCC + precúneo + hipocampo) |
| **Función** | Procesamiento offline: cuando nadie pide nada, el agente reflexiona, simula, anticipa |
| **Inputs** | Estado actual del Knowledge Graph + episodios recientes |
| **Outputs** | Hipótesis pre-computadas: "este módulo va a romper", "este tipo de PR vendrá pronto", "este test es redundante" |
| **Tecnología** | Servicio background que activa cuando el workspace está idle. Genera "intuiciones" pre-warmed. |
| **Seguridad** | Solo procesa dentro de workspace_id. No genera output externo sin trigger autenticado. |
| **Escalabilidad** | Bajísima prioridad de cómputo. Usa idle capacity. Spot instances. |
| **Capacidad generativa** | **Gran fuente de neuronas nuevas.** Es donde el sistema "imagina" mejoras y propone al Meta-Orchestrator |

### Nodo 7 — Amígdala (Valoración rápida)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Amígdala (vía rápida tálamo→amígdala) |
| **Función** | Triaje rápido de criticidad: "¿bug de seguridad? alta prioridad. ¿typo? baja." |
| **Inputs** | Cualquier evento entrante |
| **Outputs** | Score de criticidad (low/med/high/critical), activa subgrafos específicos |
| **Tecnología** | Modelo pequeño + reglas heurísticas + clasificador trained on QA criticidad |
| **Seguridad** | No accede a contenido sensible — solo metadata + signals. Latencia <50ms. |
| **Escalabilidad** | Stateless, escala trivialmente. Es el primer filtro, por eso debe ser MUY rápido. |
| **Capacidad generativa** | Aprende **nuevos patrones de criticidad** del histórico de qué resultó importante |

### Nodo 8 — Tálamo (Router)

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Tálamo |
| **Función** | Decide qué subsistemas del grafo activar según input. Algunos requests no necesitan todo el cerebro. |
| **Inputs** | Request del usuario + signal de Amígdala |
| **Outputs** | Routing decision: subgrafo mínimo / completo / emergencia |
| **Tecnología** | Routing layer con políticas + ML para casos ambiguos |
| **Seguridad** | Decisiones de routing logueadas. No descifra contenido — solo decide. |
| **Escalabilidad** | Stateless. Cache de routing patterns. |
| **Capacidad generativa** | Aprende nuevos patterns de routing cuando subgrafos demuestran efectividad |

### Nodo 9 — Dual-Process Check

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Sistema 1 (rápido, Kahneman) vs Sistema 2 (lento) |
| **Función** | Decide si responder rápido (modelo pequeño) o iniciar análisis profundo (modelo grande) |
| **Inputs** | Output preliminar del Multi-Agent Network + confidence score |
| **Outputs** | "Output directo" o "iniciar análisis ToT/profundo" |
| **Tecnología** | Heurística + clasificador entrenado en cuándo el quick output basta |
| **Seguridad** | No afecta encryption — solo política de procesamiento. |
| **Escalabilidad** | Trivial — es un check. |
| **Capacidad generativa** | Aprende qué tipos de query siempre necesitan profundidad |

### Nodo 10 — Consolidación CLS

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Sueño SWS (transferencia hipocampo→neocorteza) |
| **Función** | Promueve episodios repetidos del Hipocampo al Knowledge Graph como hechos consolidados |
| **Inputs** | Patrones detectados en episodios + signal de "repetido N veces" |
| **Outputs** | Nuevos nodos/edges en Knowledge Graph |
| **Tecnología** | Job periódico + detección de patrones + escritura controlada en KG |
| **Seguridad** | Promoción respeta workspace boundaries. Hechos cross-workspace requieren permiso explícito. |
| **Escalabilidad** | Job nocturno por workspace. Paralelizable. |
| **Capacidad generativa** | **Sistema de aprendizaje base.** Cada consolidación es aprendizaje real. |

### Nodo 11 — Neuromoduladores

| Propiedad | Detalle |
|---|---|
| **Análogo cerebral** | Dopamina, serotonina, norepinefrina, acetilcolina |
| **Función** | Modos globales del sistema: ajustan parámetros de todos los nodos a la vez |
| **Inputs** | Estado global del sistema + contexto del workspace + hora del día |
| **Outputs** | "Modo exploración" / "modo consolidación" / "modo alta atención" / "modo reposo" |
| **Tecnología** | Config global per-workspace con parámetros que afectan todos los nodos |
| **Seguridad** | Cambios de modo se loguean. Modos extremos (alta atención) consumen más cómputo, alertas de costo. |
| **Escalabilidad** | Estado pequeño, replicado globalmente. |
| **Capacidad generativa** | Puede **proponer nuevos modos** cuando detecta combinaciones útiles |

---

## 5. Los 24 edges principales — qué fluye por cada uno

Cada edge en el grafo lleva información específica. Aquí están los 24 principales con metadata real.

```
   E1: INPUT → WORKSPACE GATE
       Payload: { request, user_id, workspace_id_claim, signature }
       Encryption: TLS 1.3 in transit
       Audit: SI (toda entrada se loguea)

   E2: WORKSPACE GATE → TÁLAMO
       Payload: { request_decrypted, workspace_keys, user_roles, audit_id }
       Encryption: in-memory only, never persisted unencrypted
       Audit: SI

   E3-E4: TÁLAMO → AMÍGDALA / PFC
       Payload: { routing_decision, subgraph_activated, urgency_hint }
       Encryption: por workspace_key
       Audit: routing decision

   E5: AMÍGDALA ◄═► PFC
       Payload: { criticality_score, priority_class, lateral_pathway }
       Bidireccional: amígdala alerta a PFC, PFC modula amígdala con contexto
       Latencia objetivo: <100ms total roundtrip

   E6: PFC → HIPOCAMPO
       Payload: { query, contextual_filter, time_window, workspace_id }
       Query es DIRIGIDA (no retrieval pasivo)
       Audit: qué se buscó y por qué

   E7: PFC → KNOWLEDGE GRAPH
       Payload: { entity_query, relationship_query, max_hops }
       Cypher-like query, ejecutada en subgrafo del workspace
       Audit: queries logueadas

   E8: PFC → GANGLIOS BASALES
       Payload: { intent, context_summary, skill_hint }
       Activa skills aplicables al intent
       Audit: qué skills se aplicaron

   E9-E11: HIPOCAMPO / KG / GB → MULTI-AGENT
       Payloads:
         E9: { episodes: [...], pattern_separated: true }
         E10: { semantic_context, related_nodes }
         E11: { applicable_skills, go_paths, no_go_paths }
       Encryption: subset relevante decrypted just-in-time
       Audit: qué información alimentó qué agente

   E12: MULTI-AGENT → DUAL-PROCESS
       Payload: { preliminary_output, confidence, complexity_score }
       Decisión: ¿basta el quick path o necesita profundidad?

   E13: DUAL-PROCESS → CONFIDENCE CHECK
       Payload: { output, confidence, evidence_chain }
       Threshold-based routing

   E14: CONFIDENCE CHECK → OUTPUT GATE
       Payload: { final_output, trace, confidence, audit_id }
       Audit: decision final + trace completo
       Output signed criptográficamente

   E15: HIPOCAMPO ──► MICROGLÍA (continuo)
       Payload: scan periódico de episodios viejos
       Microglía decide: keep / archive / delete

   E16: HIPOCAMPO ──► CONSOLIDACIÓN
       Payload: episodios candidates a consolidación
       (criterio: aparecidos N veces o marcados como importantes)

   E17: CONSOLIDACIÓN → KG
       Payload: nuevos nodos/edges semánticos
       Audit: qué se consolidó y por qué

   E18: DMN ◄═► Todos los nodos cerebrales
       Bidireccional: DMN lee estado de todos, propone hipótesis
       Cuando idle, simula escenarios

   E19: NEUROMODULADORES ──► Todos los nodos
       Payload: global_mode + parámetros
       Cambia thresholds, latencias, prioridades

   E20: META-ORCHESTRATOR ╌╌╌► Cualquier nodo
       Edge GENERATIVO: puede inyectar nuevos sub-nodos
       Audit: críticamente loggeado, requiere validación

   E21: GANGLIOS BASALES ╌╌╌► Skills nuevas
       Edge GENERATIVO: skills emergen de patrones repetidos
       Sandboxed primero, promovidas si funcionan

   E22: KEY VAULT ══► Cualquier nodo
       Provee keys just-in-time
       Rotación automática
       Audit: cada acceso

   E23: AUDIT LOG ◄══ Todos los nodos
       Append-only, cryptographic chain
       Cada decisión, cada acceso, cada cambio

   E24: ZK / RISC ZERO ◄══ Output Gate (futuro)
       Proof opcional de que el output siguió un proceso aprobado
       Por ahora research, no producción
```

---

## 6. Capa de seguridad — cómo se entrelaza con todo

Aquí está la clave: **la seguridad NO es un módulo aparte. Es propiedad de cada nodo y edge.**

### 6.1 Las 5 capas de seguridad

```
   ┌─────────────────────────────────────────────────────────┐
   │  CAPA 5: ZK / RISC ZERO (futuro)                        │
   │  Verifiable computation para workflows críticos         │
   ├─────────────────────────────────────────────────────────┤
   │  CAPA 4: AUDIT (continuo)                               │
   │  Cada decisión, cada acceso, cryptographic chain        │
   ├─────────────────────────────────────────────────────────┤
   │  CAPA 3: WORKSPACE BOUNDARIES (en cada nodo)            │
   │  Ningún nodo cruza workspace_id sin permission          │
   ├─────────────────────────────────────────────────────────┤
   │  CAPA 2: END-TO-END ENCRYPTION (en cada edge)           │
   │  Plaintext solo just-in-time, ventana mínima            │
   ├─────────────────────────────────────────────────────────┤
   │  CAPA 1: KEY MANAGEMENT (vault central)                 │
   │  Per-workspace, per-node, rotation, client-managed      │
   └─────────────────────────────────────────────────────────┘
```

### 6.2 El principio de "decrypt minimum"

```
   Datos en reposo:    SIEMPRE encriptados
   Datos en tránsito:  SIEMPRE encriptados (TLS 1.3+ inter-nodo)
   Datos en uso:       Decriptados SOLO en el nodo que los procesa,
                       SOLO durante el procesamiento,
                       y eliminados del plaintext después
```

**Cada nodo declara explícitamente:**
- Qué tipos de datos necesita en plaintext
- Por cuánto tiempo
- Qué keys requiere
- Qué hace cuando termina (clear from memory)

Esto NO se hace en la generación actual de agentes. Es propiedad de For3s.

### 6.3 Workspace boundaries por diseño

```
   Workspace A           Workspace B           Workspace C
   ┌──────────┐          ┌──────────┐          ┌──────────┐
   │ Hipocampo│          │ Hipocampo│          │ Hipocampo│
   │   shard  │          │   shard  │          │   shard  │
   └──────────┘          └──────────┘          └──────────┘
        │                     │                     │
        ▼                     ▼                     ▼
   ┌──────────┐          ┌──────────┐          ┌──────────┐
   │   KG     │          │   KG     │          │   KG     │
   │   shard  │          │   shard  │          │   shard  │
   └──────────┘          └──────────┘          └──────────┘
        │                     │                     │
        ▼                     ▼                     ▼
   ┌──────────┐          ┌──────────┐          ┌──────────┐
   │  Skills  │          │  Skills  │          │  Skills  │
   │  privadas│          │  privadas│          │  privadas│
   └──────────┘          └──────────┘          └──────────┘

                   ┌────────────────────┐
                   │  SKILLS COMUNES    │
                   │  (QA general,      │
                   │   anonimizadas)    │
                   │                    │
                   │ Compartidas SOLO   │
                   │ con permiso        │
                   └────────────────────┘
```

**Las skills aprendidas con cliente X no se aplican a cliente Y** sin opt-in explícito. Esto resuelve el problema de "customer data ≠ training data" a nivel arquitectónico.

### 6.4 Audit como infraestructura, no feature

Cada decisión del grafo deja audit trail:

```
   Audit entry estructura:
   {
     timestamp: 2026-05-28T...
     workspace_id: ws_abc123
     user_id: usr_xyz
     node: "PFC.confidence_check"
     decision: "ask_human"
     reason: "confidence 0.62 < threshold 0.7"
     evidence: [...refs to episodes used...]
     hash_prev: 0xabcd... (cryptographic chain)
     hash_self: 0x1234...
   }
```

**Esto es lo que hace For3s defendible enterprise.** El cliente puede pedir: "muéstrame todas las decisiones que el agente tomó en mi workspace en marzo." Y el sistema lo entrega completo, verificable, inmutable.

---

## 7. Capa de escalabilidad — escalado por nodo

### 7.1 Principio: ningún nodo escala como bloque

Cada nodo tiene su perfil de carga:

```
   Nodo                    Carga típica           Escala con
   ─────────────────────────────────────────────────────────
   Workspace Gate          ⭐⭐⭐⭐⭐               #requests
   Tálamo                  ⭐⭐⭐⭐⭐               #requests
   Amígdala                ⭐⭐⭐⭐⭐               #requests
   PFC / Orchestrator      ⭐⭐⭐                   #requests
   Multi-Agent Network     ⭐⭐⭐⭐                  #análisis profundos
   Hipocampo               ⭐⭐⭐                   tamaño workspace
   KG                      ⭐⭐                    tamaño workspace
   Ganglios Basales        ⭐⭐                    #skills + #aplicaciones
   Microglía               ⭐                     job nocturno
   Consolidación           ⭐                     job nocturno
   DMN                     variable              idle capacity
   Neuromoduladores        ⭐                     config global
   Meta-Orchestrator       ⭐                     job periódico
```

### 7.2 Estrategias por nodo

**Workspace Gate / Tálamo / Amígdala (alta carga, baja latencia):**
- Stateless
- Múltiples replicas
- Auto-scaling agresivo
- Edge deployment (CDN-style)

**PFC / Multi-Agent (alta carga, alta complejidad):**
- Worker pool con queue
- Modelos cacheable
- Concurrent execution
- Scale to zero when idle

**Hipocampo / KG (storage-heavy):**
- Sharded por workspace
- Read replicas
- Hot/warm/cold tiering
- Cache de queries comunes

**Microglía / Consolidación / DMN (background):**
- Spot instances
- Batch processing
- Off-peak hours
- No SLA crítico

**Meta-Orchestrator (raro pero crítico):**
- On-demand
- Manual approval para cambios mayores
- Sandbox antes de promover

### 7.3 Costo unitario escalable

```
   Costo por análisis QA (target):

   v1 (10 usuarios):    $0.80
   v1 (100 usuarios):   $0.60  (economías de escala)
   v1 (1000 usuarios):  $0.45
   v2 (10K usuarios):   $0.30
   v2 (100K usuarios):  $0.20

   Cómo se logra:
   • Caching agresivo a escala
   • Microglía mantiene memoria controlada
   • Modelos pequeños donde basten
   • Spot instances para background
   • Skills reusan trabajo previo
```

**Esto es clave:** la generación actual de agentes **empeora unit economics con la escala** (más usuarios = más memoria = más costo). For3s **mejora** con la escala.

---

## 8. Capa de autonomía generativa — el sistema crece solo

Este es el pilar más radical. Aquí se explica en detalle.

### 8.1 Las 4 capacidades generativas

> ⚠️ **Nota de implementación (2026-06-10, ver §0.2):** en v1 LOCKED solo se activa la capacidad **#1 (skills)**, gobernada por el Meta-Orchestrator (governor 6 frenos + kill switch, `Cuerpo/Ronda_06_Pre_Code_Review_Detailed.md`). Las capacidades #2 (relaciones KG), #3 (sub-agentes) y #4 (modos) están DISEÑADAS aquí pero diferidas a v3.

**1. Generar skills nuevas (Ganglios Basales)**
- Cuando el sistema resuelve un problema con esfuerzo, escribe skill
- Después de N usos exitosos, la skill se promueve a "core"
- Si la skill falla, vía NO-GO la marca como evitar

**2. Generar nuevos tipos de relaciones (Knowledge Graph)**
- El sistema detecta patrones recurrentes entre entidades
- Propone nuevo tipo de relación al Meta-Orchestrator
- Si valida, se vuelve parte del schema

**3. Generar sub-agentes especializados (Multi-Agent Network)**
- Cuando una clase de problema requiere análisis repetido, el sistema propone crear un sub-agente especializado
- Sandbox primero, promoción si demuestra valor

**4. Generar nuevos modos globales (Neuromoduladores)**
- El sistema observa combinaciones efectivas de parámetros
- Propone nuevo "modo de operación" si la combinación es útil recurrentemente

### 8.2 El ciclo de vida de una neurona nueva

```
   ╔════════════════════════════════════════════════════════════╗
   ║       CICLO DE VIDA DE UNA NEURONA NUEVA EN FOR3S OS        ║
   ╚════════════════════════════════════════════════════════════╝

   1. DETECCIÓN (DMN o nodos durante operación normal)
        │
        │ "Hay un patrón que estoy resolviendo manualmente
        │  cada vez. Es candidato a automatización."
        ▼

   2. PROPUESTA (Meta-Orchestrator)
        │
        │ Genera spec de la neurona propuesta:
        │ - Qué hace
        │ - Inputs / outputs
        │ - Qué nodos existentes la alimentarán
        │ - Métricas de éxito
        ▼

   3. SANDBOX (entorno aislado)
        │
        │ La neurona vive en sandbox.
        │ Recibe data sintética + data real (con permiso).
        │ Sus outputs NO afectan el grafo vivo.
        │ Se mide su valor durante N días.
        ▼

   4. EVALUACIÓN (métricas objetivas)
        │
        │ ¿Mejoró calidad? ¿redujo costo? ¿añadió capability?
        │ Tres caminos:
        │
        │   FAIL → archive + lessons learned
        │   MARGINAL → keep en sandbox, iterar
        │   PASS → promoción
        ▼

   5. PROMOCIÓN (entrada al grafo vivo)
        │
        │ Se integra al grafo con audit.
        │ Comienza recibiendo X% del tráfico relevante.
        │ Si performance se mantiene, escala a 100%.
        ▼

   6. VIDA ÚTIL (operación normal)
        │
        │ Neurona activa, contribuye al sistema.
        │ Métricas continuas.
        ▼

   7. DECLIVE (microglía detecta uso decreciente)
        │
        │ Si la neurona deja de aportar:
        │ - Se marca para archive
        │ - Se documentan sus lessons
        │ - Microglía la poda
```

### 8.3 La pregunta crítica: ¿quién aprueba?

**Esto es delicado.** Un sistema que se auto-modifica sin control es peligroso.

For3s OS resuelve esto con **niveles de autonomía** por tipo de cambio:

| Tipo de cambio | Aprobación |
|---|---|
| Skill nueva dentro de workspace | Automática (con audit) |
| Modificar peso/score de skill existente | Automática |
| Promover skill de workspace a core | Founder/admin manual |
| Nuevo tipo de relación en KG | Founder/admin manual |
| Nuevo sub-agente | Founder/admin manual + sandbox |
| Nuevo modo global | Founder/admin manual |
| Modificar schema de seguridad | NUNCA automática |
| Cross-workspace learning | NUNCA sin opt-in cliente |

**Esto preserva la disciplina enterprise** mientras permite autonomía donde es seguro.

### 8.4 Limites duros de la autonomía generativa

For3s OS NUNCA va a:
- Generar código que se ejecute sin sandbox + audit
- Cruzar workspace boundaries
- Aprender de customer data sin opt-in
- Modificar su propia capa de seguridad
- Cambiar su core mission sin aprobación humana

Esto está alineado con `security-principles.md` §5.2 y §5.11.

---

## 9. Flujos de información completos (3 casos de uso)

Aquí se ven los flujos del grafo en acción.

### 9.1 Caso A — Análisis de PR simple

```
   1. PR llega via webhook
   2. → Workspace Gate (auth + decrypt context)
   3. → Tálamo: "PR simple, subgrafo mínimo"
   4. → Amígdala: "criticidad baja" (no es módulo crítico)
   5. → PFC: planifica
   6. PFC consulta:
      ├─ Hipocampo: "¿PRs similares recientes?"
      ├─ KG: "¿qué sé de estos archivos?"
      └─ Ganglios Basales: "skills aplicables"
   7. Multi-Agent (subset): Analyzer + Test Generator
   8. → Dual-Process: "claro, output directo"
   9. → Confidence Check: 0.85, proceed
   10. → Output Gate: firma + encrypt
   11. Output al usuario

   Latencia: ~10s
   Costo: $0.15
   Audit entries: 8
```

### 9.2 Caso B — Análisis de PR crítico (auth/security)

```
   1. PR llega
   2. → Workspace Gate
   3. → Tálamo: "subgrafo completo"
   4. → Amígdala: "CRÍTICO, módulo auth"
        → activa neuromodulador "alta atención"
   5. → PFC con modo alta atención: planning detallado
   6. PFC consulta en paralelo:
      ├─ Hipocampo: "todos los bugs de auth históricos"
      ├─ KG: "grafo completo de dependencias de auth"
      └─ Ganglios Basales: "skills específicas auth + security"
   7. Multi-Agent completo (5 agentes paralelos):
      Analyzer + History + Deps + Risk + Edge Case Miner
   8. → Synthesizer combina
   9. → Reviewer critica
   10. → Dual-Process: "complejo, profundo"
   11. → Tree of Thoughts en piezas críticas
   12. → Confidence Check: 0.72, threshold 0.8 → ASK HUMAN
   13. Sistema pide al usuario clarificar 3 puntos
   14. Usuario responde
   15. Loop al paso 7 con info nueva
   16. → Confidence Check: 0.88, proceed
   17. → Output Gate: firma + encrypt
   18. Output con trace completo

   Latencia: ~90s (con human-in-loop)
   Costo: $1.20
   Audit entries: 47
```

### 9.3 Caso C — Procesamiento nocturno (sin usuario)

```
   3am, workspace idle.

   1. Neuromoduladores cambian a "modo consolidación"

   2. Microglía:
      → scan Hipocampo, marca 234 episodios viejos
      → 180 a archivar (>90 días, no consultados)
      → 54 a borrar (consolidados en KG hace tiempo)

   3. Consolidación CLS:
      → detecta patrón: "5 PRs distintos rompieron el mismo
         tipo de test en módulo X"
      → promueve a KG: nuevo edge "modulo_X tiende_a_romper test_Y"
      → Ganglios Basales: refuerza skill "test_modulo_X_extra"

   4. DMN:
      → simula: "si mañana llega un PR de modulo_X, ¿qué prepararía?"
      → genera pre-warmed analysis
      → guarda en cache para uso futuro

   5. Meta-Orchestrator:
      → detecta: "esta clase de bug pattern aparece 12 veces
         este mes en distintos workspaces"
      → propone nueva neurona: "detector_de_bug_clase_X"
      → coloca en sandbox para evaluación

   6. Audit log:
      → graba todo lo anterior
      → 0 cross-workspace contamination

   Latencia: irrelevante (background)
   Costo: $0.40 (spot instances)
   Audit entries: 500+
   Resultado: el sistema es mejor mañana que ayer
```

---

## 10. Cómo nace una neurona nueva en For3s OS

Caso concreto, paso a paso.

### Ejemplo: nace la skill "detect_race_condition_in_db_writes"

```
Día 1:
  Usuario hace PR que cambia escritura concurrente a DB.
  For3s analiza con skills genéricas.
  Tests generados son adequate pero no específicos.
  Audit: caso analizado, confidence 0.78.

Día 5:
  PR similar de otro autor en mismo workspace.
  For3s aplica mismo análisis.
  Audit: caso similar, confidence 0.76.

Día 12:
  Tercer PR similar.
  DMN nocturno detecta: "3 PRs en 12 días con patrón similar,
  análisis genérico, confidence consistentemente <0.8."

Día 13 (Meta-Orchestrator):
  Genera propuesta:
  {
    "neuron_type": "specialized_skill",
    "name": "detect_race_condition_in_db_writes",
    "trigger_patterns": [...],
    "actions": [
      "check_for_transaction_isolation",
      "check_for_locking_strategy",
      "check_for_idempotency",
      "generate_concurrency_tests"
    ],
    "evaluation_metric": "confidence on similar PRs > 0.85"
  }

Día 13-19 (Sandbox):
  Skill corre en paralelo (no afecta output al usuario).
  Compara: confidence con skill vs sin skill.
  Resultado: 0.91 vs 0.78. Significativo.

Día 20 (Promoción):
  Skill se integra al grafo vivo.
  Comienza recibiendo 25% del tráfico de "DB write PRs".
  Si performance se mantiene, escala a 100% en 1 semana.

Día 27 (Operación normal):
  Skill activa para este workspace.
  Otros workspaces NO la reciben automáticamente
  (protección de privacidad).

Día 90 (Possible cross-workspace promotion):
  Si el founder/admin aprueba, la skill se anonimiza
  (remueve detalles específicos del workspace original)
  y se ofrece a otros workspaces como skill "common QA".
  Workspaces optan in voluntariamente.
```

**Resultado:** una skill nueva nació, fue probada, fue promovida, se aplica con audit completo, respeta workspace boundaries. **El sistema aprendió. Solo.**

---

## 11. Cómo nace un sistema de aprendizaje nuevo

Esto es más profundo que una skill. Es una **nueva forma de aprender**.

### Ejemplo: nace el sistema "predictive_regression_anticipation"

```
   Detección:
     DMN observa que en múltiples workspaces, los PRs que
     causan regresiones tienen un patrón temporal predecible:
     ocurren 2-3 días antes de release dates.

   Insight:
     El sistema actual reacciona a PRs.
     Podría ANTICIPAR riesgos antes del PR.

   Propuesta del Meta-Orchestrator:
     Nuevo subsistema: "predictive_regression_anticipation"
     - Monitorea release calendar del workspace
     - 3 días antes de release, escanea módulos críticos
     - Genera "alertas preventivas" sin esperar PR
     - Tipo de nodo nuevo: PREDICTIVE (no reactive)

   Implicación arquitectónica:
     Esto NO es una skill nueva (Ganglios Basales).
     Es un nuevo TIPO de procesamiento.
     Requiere:
     - Nuevo nodo en el grafo
     - Nueva fuente de input (release calendar)
     - Nuevos edges
     - Nueva categoría de output (predictivo, no reactivo)

   Esto es un SISTEMA DE APRENDIZAJE NUEVO.

   Aprobación:
     Founder/admin debe aprobar (cambio mayor de grafo).
     Si aprueba:
     - Sandbox por 30 días
     - Comparación: workspaces con feature vs sin feature
     - Métrica: reducción de production incidents post-release
     - Si valida, se promueve

   Si se promueve:
     For3s OS ahora tiene una capacidad nueva
     que NO existía cuando se diseñó.
     Es genuinamente más inteligente.
```

**Esto es lo radical de For3s OS:** no solo mejora dentro del paradigma actual. **Inventa nuevos paradigmas dentro de sí mismo.**

---

## 12. Propiedades emergentes del grafo

Cuando estos 11 nodos + edges + 3 pilares + autonomía generativa operan juntos, emergen propiedades que ninguna pieza tiene sola:

### 12.1 Mejora continua sin intervención

El sistema literalmente mejora cada noche.
- Microglía libera espacio
- Consolidación genera nuevos hechos
- DMN genera nuevas hipótesis
- Meta-Orchestrator propone nuevas neuronas

**Resultado:** retention enterprise altísima — el sistema vale más mes a mes.

### 12.2 Confianza calibrada

A diferencia de LLMs vanilla, For3s sabe cuándo no sabe.
- PFC metacognición
- Confidence checks explícitos
- Ask-human cuando duda

**Resultado:** ningún output "confidente pero equivocado" — el modo de fallo más caro de los agentes actuales.

### 12.3 Auditabilidad total

Cada decisión deja audit trail criptográfico.
- 24+ tipos de edges, cada uno logueado
- Workspace boundaries enforced
- Cryptographic chain

**Resultado:** compliance-ready desde día 1. Vendible a regulated industries en Fase 2.

### 12.4 Economía estable a escala

Microglía + consolidación + caching + skills reusables.
- Memoria no crece infinitamente
- Skills aprenden y se aplican rápido
- Background processing en spot instances

**Resultado:** unit economics MEJORAN con escala, no empeoran.

### 12.5 Inteligencia especializada vendible

Ganglios Basales específicos de QA + skills emergentes + KG del codebase.
- For3s aprende del cliente específico
- Skills genéricas + customizadas
- Cada workspace tiene "su" For3s

**Resultado:** alta retención porque cambiar de For3s a competidor = perder meses de aprendizaje específico.

### 12.6 Categoría nueva

Las 5 propiedades anteriores juntas no las tiene ningún agente actual. Eso es **nueva categoría**, no incremental improvement.

---

## 13. Lo que este grafo NO es todavía

Honestidad como siempre.

**Este grafo es DISEÑO ARQUITECTÓNICO, no implementación.**

> ⚠️ **ACTUALIZACIÓN 2026-06-10:** la lista de abajo era el estado de MAYO 2026. Las 10 rondas técnicas (junio 2026) resolvieron casi todo lo listado. Estado real por ítem:

Para que sea realidad falta(ba):
- **Documentos técnicos en `Mente/Cuerpo/`** detallando cada nodo → ✅ HECHO (R1-R10, 46 archivos, 100% LOCKED)
- **Decisiones de stack específico** por componente → ✅ HECHO (ver §0.1 + Consolidado §3)
- **Prototipos de cada nodo** validados individualmente → ⏳ PENDIENTE (es la programación, Fase 0+)
- **Pruebas de integración** entre nodos → ⏳ PENDIENTE (al programar, gates del Plan Maestro)
- **Validación de seguridad** por experto externo → ⏳ PENDIENTE (pentest externo, post-revenue v2)
- **Pilots reales** que validen el approach → ⏳ PENDIENTE (tras MVP ~3.5-4 meses)

**Y falta(ba)n piezas conceptuales también:**
- Cómo se hace key management exactamente → ✅ RESUELTO (R4 B1: KEK hierarchy AES-256-GCM+HKDF, Master KEK offline)
- Cómo funciona el sandbox de autonomía generativa → ✅ RESUELTO (R6: lifecycle 8 estados + sandbox eval independiente + Pre-Code Review)
- Cómo se mide "valor de neurona nueva" → ✅ RESUELTO (R6: dopaminergic scoring TD-learning + métricas de promoción)
- Cómo se versiona el grafo (rollback si degrada) → ✅ RESUELTO (R6 failure handling re-plan+rollback + R10 deploy auto-rollback)
- Cómo se prueba el grafo entero como sistema → ✅ RESUELTO (R6 memory regression 4 layers + 7 canaries · R9 attack suite · R10 pre-flight + DR testing)

**Lo ÚNICO que falta hoy es PROGRAMARLO.** El orden está en `Doc/Plan_Maestro_Programacion.md` (6 fases, empezar por Fase 0) y el tiempo en `Doc/Estimacion_Tiempo_Por_Subtema.md` (~9-10 meses Brian solo, MVP ~3.5-4).

Cada pieza tiene su documento. Este es el **mapa maestro**, no el manual de implementación.

---

## 14. Cierre

Brian, este es For3s OS visto como **un cerebro completo, no piezas aisladas**:

- **11 nodos cerebrales** trabajando como red, no como loop
- **3 pilares estructurales** (seguridad, escalabilidad, autonomía generativa) integrados en cada nodo y edge, no añadidos
- **24+ edges** con metadata, audit, encryption por default
- **Procesos de fondo continuos** que mejoran el sistema sin input del usuario
- **Capacidad de generar neuronas y sistemas nuevos** con disciplina enterprise (sandbox, evaluación, aprobación humana en cambios mayores)

**Lo que la generación actual (OpenClaw, Hermes) tiene:**
- 1 nodo (LLM) + 1-2 memorias + tools
- Loop secuencial
- Seguridad como capa añadida
- Sin autonomía generativa

**Lo que For3s OS tiene:**
- 11 nodos + 24 edges + 3 pilares estructurales
- Grafo paralelo con metacognición
- Seguridad como propiedad de cada conexión
- Sistema que crece solo, dentro de límites enterprise

**Esto es categóricamente distinto. No es marketing — es arquitectura.**

---

**Próximos pasos lógicos** *(redactados en mayo 2026 — estado a 2026-06-10):*

1. ~~Validar este grafo con el founder~~ → ✅ HECHO (validado + auditado: alineación 9.2/10)
2. ~~Traducir a `Mente/Cuerpo/` con documentos técnicos~~ → ✅ HECHO (R1-R10 LOCKED, 46 archivos)
3. ~~Empezar prototipo del MVP cerebral mínimo~~ → ⏳ ES EL SIGUIENTE PASO: programar Fase 0 (`Doc/Plan_Maestro_Programacion.md`) → MVP pilotable ~3.5-4 meses
4. Validar pilares en el prototipo (E2E + sharding + 1 skill auto-generada) → ⏳ son los gates de las Fases 1-3 del Plan Maestro

---

**Fin del documento.**
