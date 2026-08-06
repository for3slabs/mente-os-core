# 🎫 Plan Maestro de Tickets — For3s OS

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Tickets/000_PLAN_MAESTRO_TICKETS.md → bridges/000_PLAN_MAESTRO_TICKETS.md (2026-07-30, ADR-029)

> **El índice general de TODA la construcción de For3s OS en tickets.** De aquí salen los archivos de ticket detallados por hito. Esto es el "backlog épico"; cada hito se abre como su propio archivo cuando Brian aprueba arrancarlo.

**Owner:** Brian López
**Creado:** 2026-06-10
**Estatus:** 🟢 ACTIVO — construcción en curso

---

## 🧭 Las 3 brújulas (autoridad, en orden)

```
   1. Cerebro/For3s_OS_Grafo_Maestro.md   → QUÉ y POR QUÉ (fuente de verdad, §0)
   2. memory/archive/Plan_Maestro_Programacion.md    → marco de FASES / gates / MVP
   3. memory/archive/Mapa_Construccion_Incremental.md → ORDEN de obra (C0,C1,H1..H16)
```

## ⚙️ Cómo funciona el sistema de tickets

```
   • ESTE archivo = el índice maestro (todas las épicas/hitos).
   • Cada hito aprobado → se crea su archivo: NNN_Hn_NOMBRE.md
   • Cada ticket documenta: qué se construyó · qué funcionó · qué NO ·
     por qué · cuándo · qué hicimos. Bitácora forense del proceso.
   • Antes de cada hito: EXPLICAR + CUESTIONAR (alinear qué/cómo/cuándo/por qué).
   • Estados: 🔵 backlog · 🟡 en curso · 🟢 cerrado-OK · 🔴 bloqueado
```

---

## 📋 ÉPICAS Y TICKETS (el backlog completo)

### ✅ CIMIENTOS (completados)

```
   🟢 C0 — Preparar servidor for3s          [cerrado 2026-06-10]
      uv+Python3.12 · Docker · PG16+AGE+pgvector+pgcrypto · Valkey
   🟢 C1 — Esqueleto monorepo + CI verde    [cerrado 2026-06-10]
      repo privado · ruff/ty/pytest · SAST · Pilar3 gate skeleton
```

### 🔵 ÉPICA A — MVP PILOTABLE (H1-H4)

```
   🟢 H1 — HABLA        agente CLI responde con Claude  [CERRADO 2026-06-11]
      ✅ provider dual OAuth/API-key · agent OAuth-aware · CLI rich · cost
      tracker · config .env · gestor concurrencia 3 capas (adelanto R3) ·
      14 tests · CI verde · DEMO: detectó bug en suma(a,b). Ticket 001.
      ⚠️ Suscripción OAuth solo permite rol For3s en el mensaje (no system);
      para rol en system → API key (clientes la necesitan igual).
   🟢 H2 — RECUERDA     persiste + audit chain  [CERRADO 2026-06-11]
      ✅ BD+rol for3s dedicado · asyncpg · schema.sql (sessions/episodes_events
      append-only/audit_events) · audit hash chain SHA-256 + trigger anti
      UPDATE/DELETE (Grafo §6.4) · conversation orquesta memoria+agente+audit ·
      18 tests · CI verde · DEMO: proceso 2 (reinicio) recordó al proceso 1.
      Ticket 002. (Decisión: SQL directo en vez de Alembic ORM.)
   🟢 H3 — TELEGRAM     vive en Telegram (▲ hito LOCKED)  [CERRADO 2026-06-11]
      ✅ @For3s_OS_bot · PTB 22.7 polling (patrón Hermes: delete_webhook +
      fail-closed) · dueño por 1er /start · memoria COMPARTIDA CLI↔TG
      verificada · systemd permanente · 29 tests · CI verde · demo ~4s e2e.
      Ticket 003. ⚠️ pendiente menor: markdown crudo (**) sin parse_mode.
   🔵 H4 — TIENE MANOS  analiza un PR real ★ MVP
      Tickets: GitHub MCP · Filesystem/HTTP MCP · KEK hierarchy ·
      Docker workspace 1er tenant
```

### 🔵 ÉPICA B — CEREBRO DE VERDAD (H5-H9)

```
   🔵 H5 — MEMORIA REAL  Stella embeddings + pgvector/HNSW + KG (AGE Cypher)
   🔵 H6 — SE CUIDA      Valkey/Arq jobs · CLS (consolidación) · Microglía · backup
        ⭐ NOTA (2026-06-10): aquí va la COLA LLM ASÍNCRONA (Arq+Valkey,
        worker concurrency=1) que controla el ritmo de For3s consigo mismo.
        Idea de Brian para el 429; resuelve el 429 tipo A (For3s vs For3s).
        El 429 tipo B (For3s vs Claude Code) se resolvió antes con Carril B
        (API key separada en H1). La cola se reusa también en H8 (multi-agent).
   🔵 H7 — DECIDE        Tálamo · Neuromod · Dual-Process · caching 4 capas
        ⭐ NOTA (2026-06-11): aquí entra OpenCode como 2º PROVEEDOR LLM
        (Camino A, vía su modo servidor HTTP). SPIKE ya hecho y EXITOSO
        (SPIKE_OpenCode_segundo_proveedor.md): For3s Python → opencode serve
        :4096 → LLM responde OK. OpenCode ya instalado en for3s. Da GPT/Gemini/
        locales/Zen + carril alterno anti-429. Integración formal = aquí.
   🔵 H8 — EQUIPO        multi-agent 5 specialists · 18 capas defense · cost control
   🔵 H9 — SUEÑA         idle detection · DMN 8 tasks · budget+9 controles
```

### 🔵 ÉPICA C — APRENDIZAJE GOBERNADO (H10-H12)

```
   🔵 H10 — PLANEA       skill schema · PFC core · confidence 8 señales · check loop
   🔵 H11 — EL FRENO     Meta-Orchestrator governor · NO-GO HARD · activar gate
   🔵 H12 — APRENDE      skills GO · dopaminergic · lifecycle · promotion · failure
```

### 🔵 ÉPICA D — VENDIBLE ENTERPRISE (H13-H16)

```
   🔵 H13 — CARA FORMAL  channels formales · Output Gate firmado · auth/RBAC · dashboard
   🔵 H14 — OJOS         Prometheus 11 nodos · Grafana · Loki/Tempo · audit query · SLO
   🔵 H15 — DEFENSAS     Amígdala 5 capas · anomaly · attack suite · threat model · compliance
   🔵 H16 — PRODUCCIÓN   runtime híbrido · dual-plane · KEK offline · DR · pre-flight
```

---

## 📂 Índice de archivos de ticket (se llena conforme avanzamos)

| Archivo | Hito | Estado | Fecha cierre |
|---|---|---|---|
| 000_PLAN_MAESTRO_TICKETS.md | (este índice) | 🟢 vivo | — |
| _(C0/C1 documentados en Bitácora; tickets formales arrancan en H1)_ | | | |
| 001_H1_HABLA.md | H1 | 🟢 cerrado-OK | 2026-06-11 |
| 002_H2_RECUERDA.md | H2 | 🟢 cerrado-OK | 2026-06-11 |
| 003_H3_TELEGRAM.md | H3 | 🟢 cerrado-OK | 2026-06-11 |
| 004_H4_TIENE_MANOS.md | H4 | 🔵 por crear al aprobar | — |

---

## Estado global

```
   PROGRESO: 5/18 peldaños (C0 ✅ · C1 ✅ · H1 ✅ · H2 ✅ · H3 ✅▲)
   SIGUIENTE: H4 TIENE MANOS (analiza un PR real de GitHub — ★ cierra el MVP) — explicar+aprobar
   MVP PILOTABLE: al cerrar H4 (~4-5 semanas)
```

---

**Fin del Plan Maestro de Tickets.**