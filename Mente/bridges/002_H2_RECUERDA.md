# 🎫 Ticket 002 — H2 "RECUERDA"

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Tickets/002_H2_RECUERDA.md → bridges/002_H2_RECUERDA.md (2026-07-30, ADR-029)

> **Hito H2 del Mapa de Construcción Incremental.** For3s deja de ser amnésico: guarda cada conversación en PostgreSQL, la recupera al reiniciar, y nace el AUDIT CHAIN inmutable (la columna vertebral de confianza enterprise).

**Épica:** A — MVP Pilotable
**Estado:** 🟢 CERRADO-OK · DEMO PASADO 2026-06-11 (proceso 2 recordó lo del proceso 1)
**Abierto:** 2026-06-11 · **Cerrado:** 2026-06-11
**Owner:** Brian López · construido en servidor for3s
**Brújulas:** Grafo Maestro (Nodo 2 Hipocampo + §6.4 audit) · Plan Maestro (Fase 1, R2) · Mapa Incremental (H2)

---

## 🎯 Objetivo

Que For3s recuerde entre reinicios (persistencia en Postgres) y que cada decisión quede en un registro inmutable verificable (audit hash chain).

## ⚙️ Decisiones alineadas con Brian (2026-06-11)

```
   • DB:      crear base de datos 'for3s' + rol 'for3s' DEDICADO (no usar el
              superusuario postgres). Password en .env del servidor (fuera del repo).
   • Audit:   COMPLETO desde H2 — hash chain SHA-256 (hash_prev + hash_self) +
              trigger Postgres que BLOQUEA UPDATE/DELETE (inmutabilidad real).
              Grafo §6.4 lo pide desde el inicio.
   • Memoria: historial COMPLETO de la sesión se reconstruye desde Postgres y
              se pasa a Claude (truncado inteligente = R3/H5, no ahora).
   • Auth:    seguir con OAuth-suscripción (cuenta separada) de H1. H2 es memoria,
              no toca LLM.
```

## 📋 Sub-tickets (estado vivo)

```
   [x] H2.1  BD 'for3s' + rol 'for3s' dedicado en PG16 (pass aleatoria en .env) ✅
   [x] H2.2  Conexión async (asyncpg) + database_url en config/.env ✅
   [x] H2.3  Esquema SQL versionado (schema.sql): sessions, episodes_events,
             audit_events + índices. (Decisión: SQL directo en vez de Alembic
             ORM — más simple/transparente para 3 tablas + trigger). ✅
   [x] H2.4  Audit hash chain SHA-256 (hash_prev/hash_self) + trigger que
             BLOQUEA UPDATE/DELETE. Probado: DELETE rechazado ✅
   [x] H2.5  Capa de memoria (memory.py): ensure_session, record_turn append-only,
             load_history. Event Sourcing ✅
   [x] H2.6  conversation.py orquesta memoria+agente+audit; agent.ask_with_history();
             cli.py con --session persistente ✅
   [x] H2.7  Tests: hash determinista/encadenado/detección de manipulación +
             agente arma historial. 18 tests verdes ✅
   [x] H2.8  DEMO end-to-end ✅ + commit 0af0968 + CI VERDE (3 jobs) ✅
   [x] H2.9  schema.sql como package-data (source-include) para build robusto ✅
```

## 🧱 Esquema mínimo (Event Sourcing)

```
   sessions          una fila por conversación
     id, started_at, channel, status, meta
   episodes_events   Event Sourcing: cada turno = evento inmutable append-only
     id, session_id, seq, role(user/assistant), content, tokens_in/out, created_at
   audit_events      🔒 hash chain inmutable
     id, ts, workspace_id, actor, action, detail(JSON), hash_prev, hash_self
     + TRIGGER que bloquea UPDATE y DELETE
```

## ✅ DEMO de cierre (definición de "terminado")

```
   1. CLI: "mi función suma() tiene un bug" → For3s responde + guarda en PG.
   2. Cierro el proceso (Ctrl+C).
   3. Reabro el CLI con la MISMA sesión.
   4. "¿qué te dije antes?" → For3s RECUERDA la conversación previa.
   5. Consulto audit_events → la cadena de hashes es íntegra y verificable.
   6. Intento UPDATE/DELETE en audit_events → Postgres lo BLOQUEA.
```

## 🚫 Fuera de alcance (otros hitos)

embeddings/vector/KG (H5) · Microglía/CLS (H6) · multi-tenant workspaces (H4+) ·
truncado inteligente de contexto largo (R3/H5).

---

## 📓 BITÁCORA VIVA (qué funcionó / qué no / por qué / cuándo)

```
   2026-06-11 · Ticket abierto. Decisiones confirmadas con Brian. Arranca H2.1.
   2026-06-11 · BD+rol for3s creados (pass aleatoria 24 bytes, solo en .env del
                servidor). Conexión del rol verificada. pgcrypto en la BD.
   2026-06-11 · DECISIÓN: SQL directo (schema.sql + asyncpg) en vez de Alembic
                ORM. Para 3 tablas + trigger es más simple, transparente y
                auditable (el audit chain es SQL puro). Respeta R2 (asyncpg).
   2026-06-11 · Construidos db.py, audit.py, memory.py, conversation.py +
                config/agent/cli actualizados. 18 tests verdes. ruff/ty OK.
   2026-06-11 · QUÉ NO funcionó (1er intento): audit.append pasaba ts como
                string → asyncpg DataError (espera datetime). POR QUÉ: el cast
                ::timestamptz no convierte el bind param. QUÉ HICIMOS: leer
                now() como datetime real de PG y usarlo tal cual. Memoria SÍ
                funcionó a la primera (2 turnos guardados/recuperados).
   2026-06-11 · Audit chain verificado íntegro + inmutabilidad probada (DELETE
                bloqueado por el trigger). ✅
   2026-06-11 · DEMO end-to-end PASADO: proceso 1 le dijo a For3s "proyecto=
                For3s OS, bug en función suma". Proceso 2 (REINICIO total,
                nuevo proceso) recuperó 2 turnos de memoria y respondió correcto
                "For3s OS, función suma" — solo posible leyendo Postgres.
                Audit chain íntegro (6 entradas). ✅
   2026-06-11 · QUÉ FUNCIONÓ: memoria persistente, audit inmutable, DEMO, CI.
                QUÉ NO (y resuelto): el ts datetime de asyncpg. CUÁNDO: hoy.
                COMMIT: 0af0968, CI verde (SAST+Lint/Types/Tests+Pilar3 gate).
```

---

**Estado al momento:** ticket abierto, arrancando H2.1 (BD + rol dedicado).