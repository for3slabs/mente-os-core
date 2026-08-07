# Estado de Sesión y Continuidad — For3s

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Documento de continuidad cross-sesión. Leer SIEMPRE primero al retomar conversación con Brian López.**

**Owner:** Brian López
**Fecha de creación:** 2026-05-30
**Estatus:** Documento vivo. Se actualiza al final de cada sesión importante.
**Capa:** Doc — transversal de protocolo
**Propósito:** Si la conversación se compacta, se interrumpe, o se reanuda en otra sesión, este documento permite a Claude (o cualquier agente) **retomar exactamente donde quedamos sin omitir contexto crítico**.

---

## CÓMO USAR ESTE DOCUMENTO

**Si eres Claude/agente que retoma la conversación:**

1. **LEE PRIMERO ESTE DOCUMENTO COMPLETO** antes de responder cualquier cosa
2. Después lee [README.md](memory/archive/README.md) (índice maestro de Mente/Doc/)
3. Lee la sección "Lo que está abierto AHORA" más abajo
4. Aplica las "Reglas de conversación con Brian" más abajo
5. Si Brian te pregunta dónde quedamos, **resume con honestidad usando este doc**
6. NO inventes contexto que no esté aquí o en los docs referenciados

**Si eres Brian:**

- Este doc te asegura que cualquier futuro Claude pueda retomar exacto donde estamos
- Pídele al agente que LEA ESTO PRIMERO al inicio de cualquier sesión nueva
- Si los chats se compactan, este doc preserva la memoria operativa

---

## 1. ESTADO ACTUAL (snapshot 2026-05-30)

### 1.1 Quién es Brian

**Brian López** (NO Brian Aguilar — corregido 2026-05-18 en 6 archivos del sitio público).

- Founder único de For3s
- Builder técnico (background: full-stack, product lead, Web3, AI agents)
- Construyó previamente: **OpenClaw, Hermes (versión propia), Kukulcan Brain** — agentes operacionales en LATAM
- Email actual: `brian@frutero.club` (transicionando a `brian@for3s.ai` cuando se verifique dominio)
- Equipo operativo: Brian + Jenny (colaboradora) + 3 AI agents (Fruterito Personal, Empleado, Design)
- Idioma de trabajo: **español**, ocasionalmente inglés

### 1.2 Qué es For3s ahora

For3s pivotó el **2026-05-18** de "LATAM-first general AI agent infrastructure" a **"secure AI agent infrastructure for QA workflows, starting from LATAM"**.

**Estado actual:**
- For3s = empresa
- For3s OS = visión de plataforma cerebral completa (agentic AI categoría)
- For3s QA = primer wedge / módulo / producto vendible

**Mission:** Turn messy product context into trusted QA execution
**Vision:** Trusted infrastructure for secure AI agent workflows

### 1.3 Las 3 anclas estratégicas LOCKED

```
   1.D  Dedicated SaaS              (instancia dedicada por cliente)
   2.B  Open Core                   (núcleo open, features enterprise cerradas)
   3.D  Equipo pequeño contratado   (2-3 personas full-time)
```

Estas anclas **filtran todas las decisiones técnicas**. Si una decisión rompe una ancla, se rechaza.

### 1.3.bis Decisiones LOCKED del 2026-05-30 (decisión estratégica + 3 preguntas del README)

**Estrategia próximos 30 días — Opción B confirmada:**

```
   ► Opción B — Rondas completas (10 rondas técnicas exhaustivas)
     siguiendo el AI Infrastructure Master Tree (#57 del banco):

     R1. Compute (Lenguaje + Runtime)
     R2. Data (DB relacional + Vector + KG + Memoria)
     R3. Model (LLM provider abstraction)
     R4. Security (E2E + Vault + Workspaces)
     R5. Deployment (Containers + Orquestación)
     R6. Agent Runtime (Framework + MCP + Skills)
     R7. Tooling (Web/Browser/Code/Git)
     R8. Cloud Infra (Provider + Storage + CDN)
     R9. Observability (Logs + Metrics + Traces)
     R10. CI/CD + Testing

   ► MÁS cierre formal de 4 documentos faltantes en for3s-inter/:
     - 01-market-strategy/client-archetypes.md
     - 01-market-strategy/ideal-customer-profile.md (cierre formal)
     - 02-product/mvp-scope.md (cierre formal)
     - 04-commercial/first-paid-pilot-offer.md

   ► Horizonte: 4-6 semanas
   ► Prioridad: RIGOR MÁXIMO sobre velocidad
   ► Resultado esperado: arquitectura impecablemente documentada,
     cada decisión justificada, defendible ante inversionistas /
     cofundadores técnicos
   ► Riesgo aceptado: 4-6 semanas más sin código corriendo;
     competidores (Anthropic, Cognition, Hermes/GEPA) avanzan
     mientras documentamos
```

**Respuestas a las 3 preguntas del README §7:**

```
   P1: ¿"Alma" en Mente/ es el por qué/valores, o algo distinto?
       ► RESPUESTA: SÍ. Alma = POR QUÉ + VALORES (confirmado).
                    Convicciones no-negociables, dirección de fondo.

   P2: ¿Esto es para Brian, para For3s, o para ambos?
       ► RESPUESTA: AMBOS — pero MÁS para For3s.
                    Mente/ vive entrelazada con el founder
                    pero su propósito es servir a For3s.

   P3: ¿Mente/ reemplaza, complementa, o convive con
       for3s-inter/ y marca-personal/?
       ► RESPUESTA: NO REEMPLAZA NADA. Es COMPLEMENTO TOTAL.
                    Mente/ es complemento de TODO lo que vive en
                    /home/brianweb3/for3s/
                    Regla establecida por Brian:
                    "No voy a meter nada en /for3s/ que no
                     ayude a For3s"
                    Funcionalidades de unión entre Mente/,
                    for3s-inter/ y marca-personal/ se determinarán
                    en futuras sesiones (NO ahora).
```

**Implicaciones de estas decisiones:**

1. **Todo lo que vive en `/home/brianweb3/for3s/` debe servir a For3s.** Si algo no aporta, no debería estar ahí.
2. **`Mente/` es capa adicional, no sustitutiva.** Decisiones LOCKED de empresa siguen viviendo en `for3s-inter/`. Sitio público sigue en `marca-personal/`. `Mente/` añade pensamiento profundo encima.
3. **El usuario humano (Brian) y el sistema empresarial (For3s) se piensan juntos** desde Mente/, pero el output predominante es estratégico para For3s.
4. **Las 10 rondas técnicas + 4 docs en for3s-inter/ son el contrato de trabajo de las próximas 4-6 semanas.** No buscar atajos.

### 1.3.ter Protocolo operativo de las 10 rondas técnicas (LOCKED 2026-05-30)

**Formato de cada ronda:**

Cada ronda genera UN documento en `Mente/Cuerpo/` con nombre estándar:

```
   Mente/Cuerpo/
   ├── Ronda_01_Compute_Lenguaje.md
   ├── Ronda_02_Data_Layer.md
   ├── Ronda_03_Model_LLM_Abstraction.md
   ├── Ronda_04_Security.md
   ├── Ronda_05_Deployment.md
   ├── Ronda_06_Agent_Runtime_MCP.md
   ├── Ronda_07_Tooling.md
   ├── Ronda_08_Cloud_Infra.md
   ├── Ronda_09_Observability.md
   └── Ronda_10_CICD_Testing.md
```

**Estructura interna de cada doc de ronda:**

- Contexto (qué es esta capa, por qué importa, qué dice el Grafo Maestro)
- Candidatos (opciones con pros/contras filtrados desde el banco)
- Filtro (cómo aplican las 3 anclas + las 5 tensiones)
- Recomendación con razones explícitas
- Decisión LOCKED (la que Brian aprueba al cerrar la ronda)
- Implicaciones (qué cambia en otras rondas)
- Pendientes (qué quedó abierto)

**Modo de debate por ronda:**

- **Modo A** (yo propongo recomendación clara, Brian decide): para rondas técnicas claras
  → Aplica a: R1, R5, R10
- **Modo B** (conversamos sin recomendación inicial, exploramos juntos): para rondas con tensiones
  → Aplica a: R2, R6 (5 tensiones detectadas en el filtro)
- Las rondas no etiquetadas (R3, R4, R7, R8, R9) se eligen su modo al arrancarlas

**🚨 REGLA CRÍTICA DE FLUJO (no romper):**

```
   1. DEBATIMOS la ronda PRIMERO (conversación sin generar docs)
   2. NOS ALINEAMOS en la decisión / dirección
   3. RECIÉN ENTONCES generamos el .md en Mente/Cuerpo/
   4. PASAMOS a la siguiente ronda

   Brian establece:
   "PRIMERO debatimos y cuando ya estemos alineados,
    AHORA SÍ lo generas y pasamos al siguiente."

   ✗ NO generar el .md antes de la conversación
   ✗ NO asumir decisiones sin alineación explícita
   ✗ NO saltarse rondas
   ✗ NO mezclar rondas (una a la vez, en orden)
```

### 1.4 Estado del producto (honestidad cruda)

```
   ╔══════════════════════════════════════════════════╗
   ║   AVANCE FOR3S OS COMO PRODUCTO                    ║
   ║                                                    ║
   ║   Visión + posicionamiento:       ███████░░  70%   ║
   ║   Base teórica neurocientífica:   █████████  85%   ║
   ║   Arquitectura técnica:           ██░░░░░░░  25%   ║
   ║   Inteligencia competitiva:       ████████░  80%   ║
   ║   Discovery (banco):              █████████  90%   ║
   ║   Implementación / código:        ░░░░░░░░░   0%   ║
   ║   Validación de mercado:          ░░░░░░░░░   0%   ║
   ║   Empresa operativa:              ██░░░░░░░  20%   ║
   ║                                                    ║
   ║   PROMEDIO GLOBAL:                ███░░░░░░  ~18%  ║
   ║   PROMEDIO "valor al cliente":    █░░░░░░░░  ~5-8% ║
   ║                                                    ║
   ╚══════════════════════════════════════════════════╝
```

**Importante:** Brian sabe esto y lo aceptó. Le pedí honestidad sobre dónde estamos y respondió con conciencia plena de la situación.

---

## 2. EL ÁRBOL DE DOCUMENTOS (qué hay y qué significa cada uno)

```
/home/brianweb3/for3s/
│
├── for3s-inter/                    ← Company OS (decisiones LOCKED de empresa)
│   ├── 00-company-foundation/
│   │   ├── founder-thesis.md       ⭐ 7 lecciones de OpenClaw/Hermes/Kukulcan
│   │   ├── mission-vision.md       ⭐ Misión + Visión + 8 valores
│   │   ├── strategic-framework.md
│   │   ├── strategic-pillars.md
│   │   ├── principles.md
│   │   └── brand-architecture.md
│   ├── 01-market-strategy/
│   ├── 02-product/
│   │   ├── for3s-qa-product-brief.md  ⭐ Brief del wedge QA
│   │   ├── mvp-scope.md
│   │   └── ...
│   ├── 03-security/
│   │   ├── security-principles.md  ⭐ E2E encryption v1, ZK roadmap
│   │   └── ...
│   ├── 07-operations/
│   │   ├── pivot-brief-2026-05-18.md  ⭐ Las 7 decisiones del pivote
│   │   ├── decision-log.md             ⭐ D-001 al D-004
│   │   ├── post-pivot-roadmap.md       ⭐ 4 fases hasta relanzamiento
│   │   └── ...
│   └── ... (otras carpetas)
│
├── marca-personal/                 ← Sitio público actual (refleja pasado pre-pivote)
│   └── ... (Next.js + Vercel)
│
├── Mente/                          ← PENSAMIENTO PROFUNDO sobre For3s OS
│   ├── Alma/                       ← El "POR QUÉ"
│   │   └── Vision_For3s_Frontier.md     ⭐⭐⭐ Manifiesto fundacional
│   │
│   ├── Cerebro/                    ← Los "MARCOS TEÓRICOS"
│   │   ├── Cerebro_Humano_acercamiento1.md   ⭐ 8 niveles cerebro humano
│   │   ├── Cerebro_Humano_acercamiento2.md   ⭐ circuitos+conectoma+patología+BCIs
│   │   ├── Arquitectura_Grafo_vs_Loop.md     ⭐⭐ 16 secciones técnicas
│   │   └── For3s_OS_Grafo_Maestro.md         ⭐⭐⭐⭐⭐ EL DOC DE VERDAD
│   │
│   ├── Cuerpo/                     ← La "IMPLEMENTACIÓN EJECUTABLE"
│   │   └── Hermes_Arquitectura_Completa.md   ⭐ Reporte 19 secciones de Hermes
│   │
│   └── Doc/                        ← Transversales (índices + protocolo)
│       ├── README.md                          ⭐ Índice maestro
│       ├── Primeros_Pasos.md                  ⭐ Base teórica fundacional sesión 1
│       ├── Banco_Infografias_Completo.md      ⭐⭐⭐ 81+ infografías
│       ├── Banco_Diario_Mayo_2026.md          ⭐⭐ 3 docs históricos
│       ├── Banco_Filtro_Alineacion.md         ⭐⭐⭐ KEEP/REFINE/DEFER/DROP
│       └── Estado_Sesion_Continuidad.md       ⭐⭐⭐ ESTE DOCUMENTO
│
└── doc/                            ← Documentos diarios de Brian (mayo 2026)
    ├── FOR3S-STACK-DEFINED.md      (NO fuente verdad — diario histórico)
    ├── FOR3S-SERVER-ARCHITECTURE.md (NO fuente verdad — diario histórico)
    └── FOR3S-RECURSOS-ACTUALES.md   (NO fuente verdad — diario histórico)
```

### Orden de lectura crítica al retomar

Si solo tienes tiempo para leer 5 documentos:

1. **Este documento** (Estado_Sesion_Continuidad.md) — saber dónde estamos
2. **`Cerebro/For3s_OS_Grafo_Maestro.md`** — la verdad arquitectónica
3. **`Mente/Alma/Vision_For3s_Frontier.md`** — el por qué estratégico
4. **`Mente/memory/archive/Banco_Filtro_Alineacion.md`** — qué tecnologías SÍ/NO
5. **`for3s-inter/07-operations/pivot-brief-2026-05-18.md`** — decisiones LOCKED de empresa

Todo lo demás es expansión/contexto.

---

## 3. LO QUE ESTÁ ABIERTO AHORA (estado de avance)

### 3.1 Última decisión de Brian (al cierre de esta sesión)

Brian respondió las preguntas pendientes:

- **Estrategia 30 días: OPCIÓN B** (rondas completas) + 4 docs faltantes en for3s-inter/
- **Pregunta 1: SÍ** — Alma = por qué + valores
- **Pregunta 2: AMBOS** — más para For3s
- **Pregunta 3: NO REEMPLAZA** — `Mente/` es complemento de todo `/home/brianweb3/for3s/`

Ver §1.3.bis arriba para detalle completo de las decisiones LOCKED.

### 3.1.bis — RONDA 1 CERRADA (2026-05-30)

**Ronda 1 — Compute (Lenguaje + Runtime + Package Manager) está LOCKED.**

Decisión:

```
   🐍 LENGUAJE BASE:    Python 3.12+ (fallback 3.11)
   📦 PACKAGE MANAGER:  uv (Astral, Rust-based)
   🌐 FRAMEWORK WEB:    FastAPI
   🔍 VALIDACIÓN:       Pydantic v2
   ✅ TYPE CHECKER:     ty (Astral) con pyright fallback
   🧹 LINTER/FORMAT:    ruff (Astral, Rust-based)
   🧪 TESTING:          pytest + pytest-asyncio + timeout
   ⚡ ASYNC:            asyncio + anyio
   📂 MONOREPO:         uv workspaces
   🖥️  CLI/TUI:          rich + prompt_toolkit

   FRONTEND v1:
   ❌ NO React/Vue/Angular
   ✅ Telegram (python-telegram-bot)
   ✅ Dashboard sencillo (Streamlit o FastAPI+HTMX)
   ⏸️  Frontend web pulido = roadmap v3+
```

**Razones técnicas (sin sesgo de expertise de Brian):**
1. Ecosistema AI Python dominante con primitivas maduras (LangGraph, LlamaIndex, sentence-transformers)
2. Hermes (referencia técnica) está 100% en Python y ya validó este caso de uso
3. OpenClaw + 23 skills + 200+ sesiones = capital técnico Python existente reutilizable
4. MCP SDK Python first-class con Anthropic

**Plan de validación (hito 4-6 semanas):** Replicar lo que Hermes hace (CLI rico + Telegram + sesiones persistentes + multi-profile + installer one-line) para validar el stack en producción real.

Documento completo: [Mente/Cuerpo/Ronda_01_Compute_Lenguaje.md](../Cuerpo/Ronda_01_Compute_Lenguaje.md)

### 3.1.octies — DESPLIEGUE LOCAL LOCKED (2026-06-01) — D-009

**Despliegue v1 LOCKED en hardware LOCAL de Brian (NO Hetzner cloud).**

#### Decisión

```
Hardware host:    Linux LOCAL Brian
   • 30 GB RAM (sobra holgado vs ~12 GB necesarios)
   • 1 TB disco (sobra holgado vs ~150 GB necesarios)
   • 24/7 con UPS recomendado
   • Disponibilidad: garantizada por Brian

Acceso externo:   Cloudflare Tunnel (free tier)
   • HTTPS automático sin abrir puertos del router
   • Subdominio: api.for3s.ai (a configurar cuando R10)
   • DDoS protection incluida

Dominio:          for3s.ai (a registrar próximamente)
   • Cloudflare Registrar
   • ~USD 10/año

Backup:           LOCAL (disco externo USB)
   • Detalle exacto en R2 Bloque 4 sub-tema 4.4
   • Recomendación preliminar: 2 TB USB ~USD 60 una vez
```

#### Costo total v1 ACTUALIZADO

```
ANTES (Hetzner cloud — D-006 original):
   Hetzner CX42:        USD ~25/mes
   Claude Haiku CLS:    USD ~37/mes
   OpenAI fallback:     USD <1/mes
   ─────────────────────────────
   TOTAL:               USD ~63/mes

AHORA (LOCAL D-009 LOCKED):
   Hardware local:      USD 0
   Electricidad 24/7:   USD ~5/mes
   Cloudflare Tunnel:   USD 0 (free)
   Dominio for3s.ai:    USD ~$1/mes ($10/año)
   Claude Haiku CLS:    USD ~37/mes
   OpenAI fallback:     USD <1/mes
   ─────────────────────────────
   TOTAL:               USD ~43/mes

Ahorro mensual: USD ~20/mes
Compliance boost: datos del cliente JAMÁS salen del hardware Brian
```

#### Verificación P2 <25%

```
Pilot Light USD 3,500 (3 semanas) → techo USD 875
Consumo v1 (3 sem): USD 43 × 3/4 = USD ~32
→ 3.7% del techo (vs 5.4% con Hetzner cloud)
→ MARGEN 96.3% disponible para R3+R4+R8+R9
```

#### Compras únicas recomendadas

```
UPS básico:                    USD ~80-150 una vez
Disco externo USB 2 TB:        USD ~60 una vez
Dominio for3s.ai (registro):   USD ~10 una vez
─────────────────────────────────────────
TOTAL una vez:                 USD ~150-220
```

#### Impacto en decisiones técnicas LOCKED

**TODA la arquitectura técnica de Bloques 1+2+3 sigue válida sin cambios:**
- PostgreSQL 16 + AGE + pgvector + pgcrypto → IGUAL
- SQLAlchemy 2 + Pydantic v2 + Alembic → IGUAL
- Custom memory module + Stella local + HDBSCAN → IGUAL
- Valkey + Arq + pgbouncer → IGUAL
- asyncio + anyio + 7 patterns → IGUAL
- Claude Haiku 4.5 (CLS) → IGUAL
- 7/11 nodos cerebrales servidos → IGUAL

Solo cambia:
- HOST físico: Hetzner CX42 → Linux LOCAL Brian
- ACCESO externo: IP cloud → Cloudflare Tunnel
- BACKUP: cloud → disco externo local (detalle en R2 B4 4.4)

#### Riesgos aceptados conscientemente

```
1. Disponibilidad < cloud SLA
   Mitigación: UPS + monitoring activo

2. Internet casa/oficina variable
   Mitigación: ISP con SLA o backup 4G

3. Sin DDoS infra propia
   Mitigación: Cloudflare Tunnel absorbe

4. Migración cloud futura v3 si escala
   Mitigación: stack idéntico, solo cambia host (~1 sem trabajo)
```

#### Ventaja comercial — compliance

```
Cliente B2B regulado pregunta: "¿Dónde están MIS datos?"

ANTES (Hetzner cloud Alemania):
   "En infraestructura Hetzner, jurisdicción alemana"
   → Cliente preocupado GDPR, jurisdicción

AHORA (LOCAL Brian):
   "En MI servidor, jamás salen, encryption híbrida P4,
    backup en MI disco externo, audit chain inmutable"
   → Cliente compliance-friendly enterprise gusta MUCHO
```

#### Docs actualizados (11)

```
✅ for3s-inter/07-operations/decision-log.md (+ D-009)
✅ for3s-inter/09-technical-architecture/README.md
✅ for3s-inter/09-technical-architecture/storage-foundation.md
✅ for3s-inter/09-technical-architecture/memory-architecture.md
✅ for3s-inter/09-technical-architecture/performance-async.md
✅ Mente/Cuerpo/Ronda_02_Bloque_1_Storage_Foundation.md (header nota)
✅ Mente/Cuerpo/Ronda_02_Bloque_2_Memory_Architecture.md (§5)
✅ Mente/Cuerpo/Ronda_02_Bloque_3_Performance_Async.md (§10)
✅ Mente/Cuerpo/Ronda_02_Data_Layer.md (master decisiones)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.octies)
⏳ for3s-inter/02-product/mvp-scope.md (próxima edición)
```

#### Próximos pasos asociados a D-009

```
Antes de primer pilot:
- [ ] Brian registra dominio for3s.ai (~USD 10/año)
- [ ] Brian compra UPS básico (~USD 100)
- [ ] Brian compra disco externo USB 2 TB (~USD 60)
- [ ] LOCKEAR estrategia backup detallada en R2 B4 sub-tema 4.4

Cuando R10 (CI/CD/Deploy):
- [ ] Configurar Cloudflare Tunnel (cloudflared systemd)
- [ ] Configurar dominio for3s.ai + DNS Cloudflare
- [ ] Documentar plan de recuperación operacional
- [ ] Setup monitoring de uptime/disponibilidad
```

---

### 3.1.septies — RONDA 2 BLOQUE 3 LOCKED (2026-06-01) — Performance & Async

**Bloque 3 — Performance & Async CERRADO 4/4 sub-temas.**

#### Las 4 decisiones LOCKED

```
3.1 Redis layer              ✅ LOCKED
      → Valkey self-hosted, scope MÍNIMO (BSD-3 fork de Redis 7.2.4)
      → Razón: Redis OSS 7.4+ cambió a SSPL/RSALv2 (viola 2.B)
        DragonflyDB usa BSL (viola 2.B también)
        Valkey respaldado por Linux Foundation + AWS + Google + Oracle
      → Usos: SOLO job queue backend (Arq) + rate limiting
      → Vive en CX42 (~100 MB RAM, USD 0)
      → Cliente: redis-py async

3.2 Background jobs           ✅ LOCKED
      → Arq (async-native Python, MIT)
      → Razón: mismo autor que Pydantic v2, match perfecto stack async,
        setup ~30 min vs ~1-2 días Celery
      → Cron jobs: CLS 2 AM, Microglía nightly/weekly/monthly
      → Jobs on-demand: consolidate, onboarding, re-embed (v2)
      → max_jobs 10, job_timeout 600s, max_tries 3 backoff exponencial

3.3 Connection pooling        ✅ LOCKED
      → pgbouncer + asyncpg pool transaction mode + redis-py pool nativo
      → Razón: estándar industria 17 años, ISC license, evita refactor v2
      → pgbouncer: pool 30, max_clients 200, puerto 6432
      → asyncpg: pool 10 FastAPI / 5 Arq con statement_cache_size=0
      → SQLAlchemy 2: NullPool (delega a pgbouncer)
      → redis-py pool: 50 FastAPI / 20 Arq

3.4 Async patterns            ✅ LOCKED
      → asyncio + anyio + 7 patterns OBLIGATORIOS LOCKED
      → Razón: stack ya tiene anyio (FastAPI dep), APIs mejores
      → 7 patterns:
         1. Sync wrapper (Stella vía anyio.to_thread.run_sync)
         2. CapacityLimiter (stella_limiter(4), llm_limiter(3))
         3. Timeouts por operación (constantes LOCKED)
         4. async with obligatorio para cleanup
         5. Structured concurrency con task groups
         6. CancelledError re-raise siempre + cleanup
         7. Rate limiting para servicios externos
      → uvloop DEFERIBLE a v2
```

#### Stack final del Performance & Async v1

```
┌──────────────────────────────────────────────────────┐
│   FOR3S OS — Runtime completo (B1+B2+B3)              │
│                                                        │
│   Hetzner CX42 (16 GB RAM, 8 vCPU) ~USD 25/mes         │
│                                                        │
│   PROCESOS systemd:                                    │
│     1. PostgreSQL 16 + AGE + pgvector + pgcrypto      │
│        port 5432, max_conn 100                         │
│     2. pgbouncer (transaction mode)                    │
│        port 6432, pool 30                              │
│     3. Valkey (BSD-3, scope mínimo)                    │
│        port 6379, maxmemory 256mb                      │
│     4. FastAPI worker (uvicorn + asyncio + anyio)      │
│        rate limiter + handlers async                   │
│     5. Arq worker (async-native)                       │
│        cron CLS + Microglía + AsyncStellaWrapper       │
│                                                        │
│   Uso RAM v1: ~4 GB de 16 GB (holgura 75%)             │
│   Servicios extra de infra: 0 (todo en CX42)           │
│                                                        │
└──────────────────────────────────────────────────────┘
```

#### Cobertura del Grafo Maestro post-Bloque 3

```
B3 es CAPA TRANSVERSAL — no añade nodos cerebrales nuevos.
Refuerza foundation runtime para TODOS los nodos.

Pilares:
   ✅ Pilar 1 Seguridad: + rate limiting (Valkey)
                          + statement timeout (pgbouncer)
                          + cancellation safety (anyio)
   ✅ Pilar 2 Escalabilidad: COMPLETO B3
                              foundation connection management
                              foundation background processing
   ✅ Pilar 3 Autonomía: workers async autónomos
                          + sleep cycle (CLS via Arq cron)

Nodos refuerza:
   ✅ Nodo 2 Hipocampo (Stella wrapper + connection pool)
   ✅ Nodo 6 Microglía (Arq cron + cleanup patterns)
   ✅ Nodo 10 CLS (Arq + LLM limiter + timeouts)
   ✅ Nodo 1 KG (Cypher con pool dedicado)
   ✅ Nodo 4 Skills (CRUD con pool dedicado)

Anclas LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → todo en CX42
   2.B Open Core       → todas licencias permisivas (BSD/MIT/ISC/Apache/PSF)
   3.D Equipo pequeño  → cero servicios extra de infra
```

#### Costo total v1 actualizado (sin cambio post-B3)

```
Hetzner CX42:                          USD ~25/mes
PostgreSQL + extensiones:               USD 0
pgbouncer + Valkey + Arq:               USD 0
asyncio + anyio + librerías pool:       USD 0
OpenAI fallback embeddings:             USD <1/mes
Claude Haiku 4.5 (CLS):                 USD ~37/mes
─────────────────────────────────────────────────
TOTAL infra+AI v1 (B1+B2+B3):           USD ~63/mes
% techo Pilot Light ($875):             5.4%
Margen disponible R3+R4+R8+R9:          94.6%
```

#### Filosofía emergente del Bloque 3

```
"Foundation de escalabilidad con scope mínimo y patterns LOCKED."

   • SCOPE MÍNIMO desde día 1 (3.1)
   • ASYNC-NATIVE end-to-end (3.2 + 3.4)
   • PREPARACIÓN ESCALA sin pagar AHORA (3.3)
   • OPEN CORE PURO (todas las decisiones)
   • CERO SERVICIOS EXTRA INFRA
```

#### Protocolo Bidireccional aplicado

Spillovers identificados hacia `for3s-inter/` y decisión de Brian:

```
✅ Mente/Cuerpo/Ronda_02_Bloque_3_Performance_Async.md
   → Documento formal exhaustivo del Bloque 3 con 12 secciones,
     incluye las exploraciones futuras documentadas

✅ for3s-inter/09-technical-architecture/performance-async.md
   → Sub-doc dedicado público-formal del Bloque 3
   → Patrón replicado de B1+B2

✅ for3s-inter/09-technical-architecture/README.md
   → Actualizado con sección Performance & Async LOCKED
   → Costo total v1 actualizado (sin cambio)
   → Tabla de rondas actualizada (B3 LOCKED)

✅ for3s-inter/07-operations/decision-log.md
   → D-008 (Stack Performance & Async LOCKED) añadido

✅ Mente/Cuerpo/Ronda_02_Data_Layer.md (master)
   → Sub-documentos: B3 marcado ✅ LOCKED
   → Decisiones loggeadas: D-008 añadido
   → §5 Status Bloques: B3 con detalle completo LOCKED
   → §9 Próximo paso: ahora Bloque 4

✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.septies)
   → Preserva continuidad cross-sesión

⏳ DIFERIDOS hasta cierre R2 completo (después de B4):
   • for3s-inter/09-technical-architecture/files-external.md
   • for3s-inter/03-security/encryption-strategy.md
   • for3s-inter/03-security/data-handling-policy.md
   • for3s-inter/03-security/access-control-model.md
   • for3s-inter/05-finance/unit-economics.md
```

#### Exploraciones futuras documentadas (no v1)

Registradas en `Ronda_02_Bloque_3_Performance_Async.md §11`:

```
3.1 Redis layer:
   📚 DragonflyDB (v3 si Valkey CPU >70%, re-evaluar 2.B)
   📚 Valkey Cluster mode (v3 si 1 instance no aguanta)
   📚 Valkey Sentinel HA (v2 si SLA enterprise 99.99%)
   📚 Cache embeddings frecuentes (v2 si HNSW degrada)
   📚 Working memory shared cross-procesos (v2 multi-worker)
   📚 Pub/sub coordinación inter-workers (v2 si workers interfieren)

3.2 Background jobs:
   📚 Celery upgrade (v3 si workflows complejos chains/groups)
   📚 arq-dashboard (v2 si logs estructurados no bastan)
   📚 Múltiples workers Arq (v2 si queue_depth >100 sostenido)
   📚 Inngest/Hatchet (v3+ improbable, cabe self-hosted)
   📚 Job priorities con queues separadas
   📚 Dead Letter Queue (v2 si retry-exhausted >1%)
   📚 Job result webhooks

3.3 Connection pooling:
   📚 PgCat (v3 si read replica routing/sharding)
   📚 pgbouncer session mode (si LISTEN/NOTIFY crítico)
   📚 Twemproxy/Envoy para Valkey (v2-v3 si pool >50%)
   📚 Múltiples pgbouncer con load balancer (v3+ SLA 99.99%)
   📚 Postgres read replicas
   📚 Subir max_connections a 200+

3.4 Async patterns:
   📚 uvloop event loop (v2 si event loop blocked >10ms)
   📚 ProcessPoolExecutor embeddings batch (v2 throughput)
   📚 GPU para Stella CUDA (v3 si calidad exigida)
   📚 Métricas event loop Prometheus (R8)
```

#### Próximo paso inmediato

**Arrancar R2 Bloque 4 — Files & External Data** con 4 sub-temas (ÚLTIMO bloque de R2):

```
4.1 File storage (BLOB postgres vs S3-compatible)
4.2 S3 provider (AWS S3 vs Cloudflare R2 vs Backblaze B2 vs MinIO)
4.3 Code repo access (Git providers integration strategy)
4.4 Backup strategy (pg_dump + WAL archiving)
```

Tensión esperada en 4.2 (S3 provider — costo vs reliability). Después de B4, R2 estará 100% cerrado y avanzaremos a R3 — Model/LLM Layer.

---

### 3.1.sexies — RONDA 2 BLOQUE 2 LOCKED (2026-06-01) — Memory Architecture

**Bloque 2 — Memory Architecture CERRADO 7/7 sub-temas.**

#### Las 7 decisiones LOCKED

```
2.1 Memory framework        ✅ LOCKED
      → Custom core + librerías pequeñas composables
      → for3s_os/memory/ módulo propio (control 100%)
      → Librerías: pgvector-python, sentence-transformers,
        hdbscan, cryptography, SDKs Anthropic + OpenAI

2.4 Memory tiers             ✅ LOCKED
      → 3 tiers clásico (Working + Short + Long)
      → Tier 1: in-process Python (Nodo 3 PFC)
      → Tier 2: Postgres + pgvector (Nodo 2 Hipocampo)
      → Tier 3: Apache AGE + concepts (Nodo 1 KG)

2.2 Embeddings               ✅ LOCKED
      → Primary: Stella local dunzhang/stella_en_400M_v5
        @ 1024 dim (MIT, MTEB 66.5 > OpenAI 3-large)
      → Fallback: OpenAI text-embedding-3-small @ 1536
      → Hardware upgrade: CX32 → CX42 (~USD 12 más)

2.3 Vector indexing          ✅ LOCKED
      → HNSW @ 1024 cosine tuneado
      → m=16, ef_construction=128, ef_search=100
      → Recall ~97-99% crítico para Pattern Separation

2.5 Forgetting (Microglía)   ✅ LOCKED
      → Soft Delete + Decay scores + Archive cold storage
      → ~13 meses a purge final (4 etapas reversibles)
      → EXCEPCIONES inmutables: audit_events, events ES
      → Meta-audit de TODAS las acciones

2.6 CLS Consolidation        ✅ LOCKED
      → Híbrido Heurística (HDBSCAN) + LLM Haiku 4.5
      → Diario, threshold 10 episodios
      → Privacy: solo summaries al LLM, no datos crudos
      → Costo: ~USD 37/mes v1 (1.1% techo Pilot)
      → Fallback graceful a heurística pura

2.7 Mapeo Nodo↔Tabla SQL     ✅ LOCKED
      → Documentación oficial (no decisión técnica)
      → 11 nodos cerebrales mapeados a tablas + módulos
      → Diccionario bilingüe cerebral ↔ técnico
      → Documento VIVO actualizable
```

#### Stack final del Memory Architecture v1

```
┌──────────────────────────────────────────────────────┐
│   FOR3S OS — Memory Architecture v1                   │
│                                                        │
│   Tier 1 — WORKING (Nodo 3 PFC)                        │
│     • In-process Python (deque LRU)                    │
│     • 15 items max, TTL 60 min                         │
│                                                        │
│   Tier 2 — SHORT-TERM (Nodo 2 Hipocampo)               │
│     • Postgres: episodes_events + episodes_state        │
│     • pgvector HNSW @ 1024 cosine                      │
│     • Stella embeddings local                          │
│     • Retención 30-90 días + decay                     │
│                                                        │
│   Tier 3 — LONG-TERM (Nodo 1 KG)                       │
│     • Apache AGE: nodes + edges Cypher                 │
│     • pgvector: concept embeddings                     │
│     • Permanente (audit + KG)                          │
│                                                        │
│   Forgetting (Nodo 6 Microglía):                       │
│     • Nightly: decay + soft delete                     │
│     • Weekly: archive                                  │
│     • Monthly: final purge + edge prune                │
│                                                        │
│   CLS (Nodo 10):                                       │
│     • Diario: HDBSCAN clustering + Haiku 4.5            │
│     • Skip si <10 episodios                            │
│     • Costo ~$37/mes                                   │
│                                                        │
│   Hardware: Hetzner CX42 (16 GB RAM) ~USD 25/mes        │
└──────────────────────────────────────────────────────┘
```

#### Cobertura del Grafo Maestro post-Bloque 2

```
Nodos servidos:
   ✅ FULLY (6): Nodo 1, 2, 4, 6, 9, 10
   🟡 FOUNDATION (4): Nodo 3 (R5 ext), 5, 8 (R9 ext), 11
   ⏳ PENDIENTE (1): Nodo 7 (DMN → R5)

Pilares:
   ✅ Pilar 1 Seguridad: REFORZADO (privacy Stella + meta-audit)
   🟡 Pilar 2 Escalabilidad: foundation (pool/cache en Bloque 3)
   ✅ Pilar 3 Autonomía: CUSTOM control + CLS = aprendizaje real

Anclas LOCKED: 3/3 respetadas ✅
```

#### Costo total v1 actualizado

```
Hetzner CX42:                          USD ~25/mes
PostgreSQL + extensiones:               USD 0
Custom memory module:                   USD 0
OpenAI fallback embeddings:             USD <1/mes
Claude Haiku 4.5 (CLS):                 USD ~37/mes
─────────────────────────────────────────────────
TOTAL infra+AI v1 (B1+B2):              USD ~63/mes

% techo Pilot Light ($875):             5.4%
Margen disponible para R3+R4:           94.6%
```

#### Filosofía emergente del Bloque 2

```
"Custom core con librerías composables, mapeo 1:1 con el
cerebro biológico, control total sobre la semántica."

   • CONTROL 100% del código (2.1)
   • ALINEACIÓN cerebral 1:1 (2.4 + 2.7)
   • PRIVACY-FIRST (Stella local + summaries CLS)
   • REVERSIBILIDAD (forgetting 4 etapas)
   • CALIDAD/COSTO balance (HNSW tuneado + Haiku)
   • CONSISTENCIA con Bloque 1 (cero servicios extra)
```

#### Protocolo Bidireccional aplicado

Spillovers identificados hacia `for3s-inter/` y decisión de Brian:

```
✅ Mente/Cuerpo/Ronda_02_Bloque_2_Memory_Architecture.md
   → Documento formal exhaustivo del Bloque 2 con 16 secciones,
     incluye las exploraciones futuras documentadas

✅ for3s-inter/09-technical-architecture/README.md
   → Actualizado con sección Memory Architecture LOCKED
   → Hardware update CX32 → CX42 reflejado
   → Costo total v1 actualizado

✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.sexies)
   → Preserva continuidad cross-sesión

⏳ DIFERIDOS hasta cierre R2 completo:
   • for3s-inter/09-technical-architecture/memory-architecture.md
   • for3s-inter/03-security/encryption-strategy.md
   • for3s-inter/03-security/data-handling-policy.md
   • for3s-inter/03-security/access-control-model.md
   • for3s-inter/05-finance/unit-economics.md
   • for3s-inter/07-operations/decision-log.md D-007
     (decisión: incluir Bloque 2 en D-007 al cerrar R2)
```

#### Exploraciones futuras documentadas (no v1)

Registradas en `Ronda_02_Bloque_2_Memory_Architecture.md §15`:

```
2.4 Memory tiers:
   📚 4 tiers Hermes-style (Redis cache cuando 3.1 lockee Redis)
   📚 Tiers por dominio (v3 si complejidad lo demanda)

2.3 Vector indexing:
   📚 IVFFlat (cuando RAM HNSW >50% sostenido)
   📚 Híbrido HNSW T2 + IVFFlat T3
   📚 Quantization (IVFPQ, binary, scalar)
   📚 Migración Qdrant (cuando >5M vectores/wks)

2.5 Forgetting:
   📚 Hard delete para datos NO críticos
   📚 Solo decay (cliente enterprise zero-deletion)
   📚 Forgetting RLHF (v2 con usuarios activos)
   📚 Forgetting ML-driven (v3)

2.6 CLS:
   📚 LLM puro Opus (clientes premium tier)
   📚 Upgrade Sonnet/Opus si Haiku queda corto
   📚 Re-consolidación periódica (v2-v3)
   📚 Active learning del clustering
   📚 CLS multi-workspace (cross-tenant patterns)
```

#### Próximo paso inmediato

**Arrancar R2 Bloque 3 — Performance & Async** con 4 sub-temas:

```
3.1 Redis layer (cache, sessions, pub/sub)
3.2 Background jobs (Celery vs Arq vs APScheduler vs Dramatiq)
3.3 Connection pooling (pgbouncer vs asyncpg pool)
3.4 Async patterns (asyncio + anyio coordination)
```

Tensión esperada en 3.2 (jobs framework), informada por:
- forgetter workers (2.5) nightly/weekly/monthly
- CLS consolidator (2.6) diario
- Coordinación entre workers async

---

### 3.1.nonies — R2 — DATA LAYER 100% CERRADO (2026-06-01) ⭐

**RONDA 2 — DATA LAYER COMPLETADA AL 100%** (20/20 sub-temas LOCKED).

#### Cierre completo

```
✅ Bloque 1 — Storage Foundation (6/6) — D-006
✅ Bloque 2 — Memory Architecture (7/7) — D-007
✅ Bloque 3 — Performance & Async (4/4) — D-008
✅ Bloque 4 — Files & External (3/3) — D-011 ⭐ CIERRA R2

Decisiones cross-bloque:
   D-005 — Tensión E2E vía P4 híbrido
   D-009 — Despliegue LOCAL Linux + Cloudflare Tunnel
   D-010 — Sub-tema 4.3 movido a R4 (Tools/MCP)
```

#### Las 3 decisiones LOCKED del Bloque 4 (D-011)

```
4.1 File storage         ✅ Filesystem local + Postgres metadata
4.2 S3 provider          ✅ NO S3 v1 (defer a v2-v3)
4.4 Backup strategy      ✅ Local USB + Cloudflare R2 (3-2-1 rule)
⏭️ 4.3 Code repo access  → MOVIDO a R4 Tools/MCP (D-010)
```

#### Stack v1 FINAL CONSOLIDADO (R1 + R2 completo)

```
HARDWARE & NETWORK (D-009):
   Linux LOCAL Brian (30 GB RAM, 1 TB disco, 24/7)
   Cloudflare Tunnel (free) → api.for3s.ai
   Cloudflare R2 (free tier) → backup offsite
   Dominio for3s.ai (a registrar)

COMPUTE (R1):
   Python 3.12+ + uv + FastAPI + Pydantic v2
   SQLAlchemy 2 + asyncio + anyio
   ruff + ty + pytest
   Frontend: Telegram bot + Streamlit

STORAGE (R2 B1):
   PostgreSQL 16 + AGE + pgvector + pgcrypto
   Schema-per-tenant (P3)
   Alembic single multi-schema
   ES tables por aggregate (P5 híbrido)
   Audit chain inmutable con hash

MEMORY (R2 B2):
   Custom memory module (control 100%)
   3 tiers (Working/Short/Long)
   Stella local embeddings @ 1024 dim
   OpenAI 3-small fallback
   HNSW tuneado (m=16, ef=128/100, cosine)
   Microglía forgetting (Soft+Decay+Archive)
   CLS con HDBSCAN + Claude Haiku 4.5

PERFORMANCE (R2 B3):
   Valkey (BSD-3, scope mínimo)
   Arq (MIT, async-native jobs)
   pgbouncer (ISC, transaction mode)
   CapacityLimiters + timeouts LOCKED

FILES & BACKUP (R2 B4):
   Filesystem local + Postgres metadata
   NO S3 v1
   Backup 3-2-1: USB local + R2 cloud
   age encryption + LUKS + systemd timers
```

#### Cobertura del Grafo Maestro post-R2 COMPLETO

```
NODOS CEREBRALES:
   ✅ FULLY MAPPED (6):
      Nodo 1 KG, Nodo 2 Hipocampo, Nodo 4 Skills,
      Nodo 6 Microglía, Nodo 9 Pattern Sep, Nodo 10 CLS
   🟡 FOUNDATION READY (4):
      Nodo 3 PFC, Nodo 5 Action Sel, Nodo 8 Amígdala,
      Nodo 11 Neuromoduladores
   ⏳ PENDIENTE (1):
      Nodo 7 DMN → R5

PILARES: 3/3 cubiertos ✅
   ✅ Pilar 1 Seguridad (iso + audit + encryption + backup)
   ✅ Pilar 2 Escalabilidad (foundation + pool + cache + jobs + backup)
   ✅ Pilar 3 Autonomía (memory + sleep cycle + backup garantiza continuidad)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS
   2.B Open Core (todas licencias permisivas)
   3.D Equipo pequeño (0 servicios extra, automation completa)
```

#### Costo total v1 FINAL

```
Hardware Linux LOCAL:                   USD 0
Electricidad servidor 24/7:             USD ~5/mes
Cloudflare Tunnel:                      USD 0 (free)
Cloudflare R2 backup:                   USD 0 (free tier)
Dominio for3s.ai:                       USD ~$1/mes
PostgreSQL + extensiones:                USD 0
Custom memory + Stella + libs:           USD 0
Valkey + Arq + pgbouncer + asyncio:      USD 0
Backup tools (age + rclone):             USD 0
OpenAI fallback embeddings:              USD <1/mes
Claude Haiku 4.5 (CLS):                  USD ~37/mes
─────────────────────────────────────────────
TOTAL v1 FINAL:                          USD ~43/mes

Verificación P2 <25%:
   Pilot Light: 3.7% del techo (margen 96.3%)
   Pilot Pro:   1.6% del techo (margen 98.4%)

Compras únicas:
   UPS básico:                          USD ~100
   Disco externo USB 2 TB:              USD ~60
   Dominio for3s.ai registro:           USD ~10
   TOTAL una vez:                        USD ~170
```

#### Filosofía consolidada R2

```
1. CENTRALIZAR EN POSTGRESQL (B1)
2. CUSTOM CORE + LIBRERÍAS COMPOSABLES (B2)
3. MAPEO 1:1 CON CEREBRO (B2 2.7 + canónico)
4. PRIVACY-FIRST (B2 + D-009)
5. SCOPE MÍNIMO + PREPARACIÓN ESCALA (B3)
6. LOCAL PRIMARY + CLOUD SECONDARY (B4 + D-009)
7. OPEN CORE PURO (todas decisiones)
8. CERO SERVICIOS EXTRA INFRA
9. COSTO HOLGADO EN P2 <25%
10. ABSTRACCIÓN OS vs WEDGE (D-010)
```

#### Protocolo Bidireccional aplicado al cierre R2

Spillovers TODOS escritos al cierre R2 (2026-06-01):

```
✅ Mente/Cuerpo/Ronda_02_Bloque_4_Files_External.md (sub-doc detallado)
✅ for3s-inter/09-technical-architecture/files-external.md (público-formal)
✅ for3s-inter/09-technical-architecture/README.md (R2 COMPLETO añadido)
✅ for3s-inter/07-operations/decision-log.md (+ D-011)
✅ Mente/Cuerpo/Ronda_02_Data_Layer.md (master R2 100% cerrado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.nonies)
✅ for3s-inter/03-security/encryption-strategy.md (P4 detallado)
✅ for3s-inter/03-security/data-handling-policy.md (retención + forgetting + backup)
✅ for3s-inter/03-security/access-control-model.md (RBAC + workspace isolation)
✅ for3s-inter/05-finance/unit-economics.md (costo total + escalado)
```

#### Próximo paso inmediato — R3

**Arrancar R3 — Model/LLM Layer** con decisión principal:

```
R3 decidirá:
   • LLM principal para razonamiento (Claude Opus / GPT-4o / Gemini)
   • Routing entre múltiples LLMs
   • Local LLM como fallback (Llama, Qwen)
   • Estrategia multi-model
   • Embeddings YA decididos (Stella local, B2 2.2)
   • Claude Haiku YA en uso (CLS, B2 2.6)

Costos AI margen disponible:
   • Pilot Light: USD 843 (96.3% del techo $875)
   • Pilot Pro:   USD 1,968 (98.4% del techo $2,000)
   → Espacio enorme para LLM principal
```

#### Pendientes operacionales antes de primer pilot

```
- [ ] Brian registra dominio for3s.ai (Cloudflare Registrar)
- [ ] Brian compra UPS básico (~USD 100)
- [ ] Brian compra disco externo USB 2 TB (~USD 60)
- [ ] Configurar Cloudflare Tunnel (cuando R10)
- [ ] Configurar Cloudflare R2 bucket (cuando R10)
- [ ] Activar systemd timers de backup (cuando R10)
- [ ] Setup monitoring uptime (cuando R8)
- [ ] Cifrado age keypair: generar + guardar private OFFLINE
```

---

### 3.1.decies — R3 BLOQUE 1 LOCKED (2026-06-01) — LLM PRINCIPAL

**R3 BLOQUE 1 — LLM PRINCIPAL CERRADO** (4/4 sub-temas LOCKED).

#### Pre-preguntas P1-P5 LOCKED (antes del Bloque 1)

```
P1 — Uso LLM:                  MIXTO UNIVERSAL
   • Razonamiento + Q&A
   • CUALQUIER dominio (salud, belleza, código, etc.)
   • NO solo PRs (For3s OS es plataforma universal)

P2 — Prioridad LLM principal:  Sonnet 4.6 default → Opus 4.7 selectivo

P3 — Privacy LLM:               Cloud Anthropic con disclaimer
   • DPA firmado
   • Cliente puede opt-out con allow_llm_fallback

P4 — Multi vs single model:    Single-model v1
   • Tiers per workspace, no routing per request

P5 — Budget AI principal:      USD 50-200/mes cap operacional
```

#### Aclaración arquitectónica crítica

```
For3s = empresa
   ├── For3s OS (plataforma universal "segundo cerebro")
   │      • ESTE CHAT habla SOLO de esto
   │      • Carpeta: Mente/
   │      • R1, R2, R3-R10 = construir For3s OS
   │      • Sirve para CUALQUIER dominio
   │
   └── For3s QA (primer "agente vertical" sobre For3s OS)
          • Carpeta: for3s-inter/
          • Equipo trabajando aparte
          • NO scope este chat

✅ Arquitectura R1+R2 = PERFECTA porque ES universal
✅ Wedge QA = primer agente vertical encima
✅ Fuente de verdad LOCKED: For3s_OS_Grafo_Maestro.md
```

#### Las 4 decisiones LOCKED del Bloque 1 R3 (D-012)

```
3.1.1 Provider LLM principal        ✅ LOCKED
      → Anthropic (Claude family) + abstraction layer LLMProvider
      → Alineación PERFECTA con Grafo Maestro §4 Nodo 3
        (sugiere "Claude Sonnet" explícitamente)
      → Stack consistency (Haiku ya LOCKED B2 2.6 para CLS)
      → MCP protocol nativo (preparación R4)
      → Prompt caching 90% off (vs 50% OpenAI)
      → SDK: anthropic (oficial MIT)

3.1.2 Modelo específico             ✅ LOCKED
      → Sonnet 4.6 default + Opus 4.7 opt-in per workspace
      → Cumple Grafo Maestro (Sonnet) + P2 ("apuntando Opus")
      → Tier per workspace via shared.workspaces.llm_tier
      → Pricing tier natural:
         - Pilot Light $3.5K → Sonnet fijo
         - Pilot Pro $8K → Opus opcional
         - Enterprise (v2+) → Opus + custom
      → ALTER TABLE shared.workspaces ADD llm_tier, llm_tier_changed_at

3.1.3 Multi-model routing strategy  ✅ LOCKED
      → NO routing v1, diferir 100% a v2
      → Cumple P4 LOCKED ("Single-model v1")
      → Alineación Grafo (Nodo 9 vive en R5, no R3)
      → Triggers v2 routing automático:
         • R5 cierra Nodo 9 Dual-Process Check
         • R8 mide cost per request
         • 60%+ requests sobre-spec'd
         • >10 workspaces activos

3.1.4 Local LLM fallback            ✅ LOCKED
      → Cloud fallback OpenAI (sin local LLM v1)
      → Aprovecha OpenAI ya en stack (B2 2.2)
      → Cumple D-009 LOCAL (sin GPU extra)
      → Costo trivial (~$3/año en outages)
      → Triggers fallback:
         • HTTP 503 Anthropic
         • HTTP 429 rate limit
         • Timeout >60s
         • 3 retries fallidas con exponential backoff
      → Opt-out per workspace: allow_llm_fallback BOOLEAN
      → Transparencia: header X-LLM-Provider + audit log
```

#### Stack LLM v1 LOCKED

```
PRIMARY PROVIDER:
   • Anthropic (Claude family)
   • SDK: anthropic (MIT)

MODELOS:
   • Default workspace: Claude Sonnet 4.6
   • Premium upgrade: Claude Opus 4.7 (opt-in)
   • CLS background: Claude Haiku 4.5 [B2 2.6 LOCKED]

FALLBACK PROVIDER:
   • OpenAI (GPT-4o)
   • Activación automática ante outages
   • SDK: openai (oficial)

EMBEDDINGS [B2 2.2 LOCKED]:
   • Primary: Stella local @ 1024 dim
   • Fallback: OpenAI text-embedding-3-small

ROUTING v1:
   • Tier per workspace (sonnet | opus)
   • Sin routing per request (defer v2)

ARQUITECTURA:
   • LLMProvider abstract Protocol
   • FailoverManager orquesta primary + fallback
   • Compatible swap futuro
```

#### Estructura módulo for3s_os/llm/

```
for3s_os/llm/
├── base.py              → LLMProvider abstract
├── anthropic_provider.py → ClaudeProvider (primary)
├── openai_provider.py    → GPTProvider (fallback)
├── failover.py           → FailoverManager
├── router.py             → multi-model v2+
├── prompts/              → templates
├── context_builder.py    → context desde memory tiers
├── cost_tracker.py        → per-workspace tracking
└── llm_observability.py   → tokens, latency, errors
```

#### Patrones obligatorios

```
✓ llm_limiter (CapacityLimiter 3) — B3 3.4 LOCKED
✓ LLM_CALL_TIMEOUT (60s) — B3 3.4 LOCKED
✓ CancelledError re-raise siempre
✓ Meta-audit cada call (audit_events)
✓ Cost tracking per workspace
✓ Header X-LLM-Provider en response
✓ Opt-out per workspace respetado
✓ Cap P5 enforcement (BudgetExceeded)
```

#### Costo total v1 actualizado (R1+R2+R3 B1)

```
SUBTOTAL R2 cerrado:               USD ~43/mes
R3 BLOQUE 1 NUEVO:
   Claude Sonnet 4.6 principal:    USD ~50/mes
   OpenAI fallback LLM:            USD ~$0.30/mes
─────────────────────────────────────────────
TOTAL v1 (R1+R2+R3 B1):            USD ~93/mes

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$70
   → 8.0% del techo (vs 5.4% pre-R3)
   → MARGEN 92% para R3 B2-B4 + R4-R10

Verificación P5 cap LLM ($50-200/mes):
   Total LLM: $87/mes (Haiku $37 + Sonnet $50)
   → 43.5% del cap medio
   → Margen $113 escalado workspaces
```

#### Cobertura Grafo Maestro post-Bloque 1 R3

```
NODOS servidos:
   ✅ Nodo 3 PFC (LLM principal definido)
   ✅ Nodo 10 CLS (Haiku ya integrado B2 2.6)
   🟡 Nodo 9 Dual-Process Check (preparación R5)
   🟡 Nodo 11 Neuromoduladores (foundation tier dynamic)

PILARES:
   ✅ Pilar 1 Seguridad (meta-audit + opt-out + transparencia)
   ✅ Pilar 2 Escalabilidad (FailoverManager resiliencia)
   ✅ Pilar 3 Autonomía (LLM habilita razonamiento autónomo)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → tier per workspace
   2.B Open Core       → SDKs abiertos (anthropic MIT, openai MIT)
   3.D Equipo pequeño  → provider único maduro, simplicidad
```

#### Filosofía emergente del Bloque 1 R3

```
"Provider único maduro con fallback automático, sin sobre-
ingeniería, alineado con Grafo Maestro §4 Nodo 3."

   • ALINEACIÓN GRAFO MAESTRO (3.1.1)
   • TIERS PER WORKSPACE (3.1.2)
   • SIN ROUTING PREMATURO (3.1.3)
   • RESILIENCIA SIN GPU (3.1.4)
   • ABSTRACTION LAYER FUTURE-PROOF
```

#### Riesgos legítimos aceptados (3)

```
1. Dependencia Anthropic (cloud + provider único)
   Mitigación: OpenAI fallback + abstraction layer permite swap

2. Costo Opus si workspace activa tier premium
   Mitigación: Pilot Pro $8K cubre, cap P5 enforcement

3. Outage Anthropic activa fallback con diferencias sutiles
   Mitigación: prompts compatibles, testing periódico, transparencia
```

#### Protocolo Bidireccional aplicado

Spillovers identificados y ejecutados:

```
✅ for3s-inter/07-operations/decision-log.md + D-012
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (master R3)
✅ Mente/Cuerpo/Ronda_03_Bloque_1_LLM_Principal.md (detallado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.decies)

⏳ DIFERIDOS hasta cierre R3 completo:
   • for3s-inter/09-technical-architecture/model-llm-layer.md
   • Actualización 09-technical-architecture/README.md
   • Actualización 02-product/mvp-scope.md
```

#### Exploraciones futuras documentadas

Lista completa en `Ronda_03_Bloque_1_LLM_Principal.md §10`. Resumen:

```
3.1.1: OpenAI, Gemini, Local LLMs, multi-model routing, computer use,
       vision, OpenAI gpt-oss
3.1.2: routing automático, manual flag, tier haiku, pricing automático,
       routing por dominio, cost prediction, dynamic tier
3.1.3: foundation hooks, routing v2, routing por dominio v3+, dynamic
3.1.4: local Llama, graceful degradation, multi-cloud rotation,
       fallback inteligente por error type, notificación cliente
```

#### Próximo paso inmediato (post-B1 R3) — SUPERADO por §3.1.undecies abajo

~~Arrancar R3 Bloque 2~~ → **EJECUTADO** 2026-06-02 → 2026-06-03

Ver §3.1.undecies para snapshot Bloque 2 LOCKED.

---

### 3.1.undecies — R3 BLOQUE 2 LOCKED (2026-06-03) — PROMPT & CONTEXT MANAGEMENT

**R3 BLOQUE 2 — PROMPT & CONTEXT MANAGEMENT CERRADO** (4/4 sub-temas LOCKED).

#### Las 4 decisiones LOCKED del Bloque 2 R3 (D-013)

```
3.2.1 Prompt engineering framework      ✅ LOCKED
      → Custom framework liviano (Jinja2 + Pydantic + dataclasses)
      → Templates versionables, type-safe, auditables
      → No lock-in vendor
      → Multi-dominio escalable (templates per dominio v2-v3)
      → Estructura módulo:
         for3s_os/llm/prompts/
            ├── base.py (PromptTemplate Pydantic)
            ├── templates/{system,reasoning,memory,domain}/
            ├── renderer.py (render + audit)
            └── registry.py (versionado)
      → Anthropic XML tags nativos (best practice oficial)
      → Cada render → audit_events chain

3.2.2 Context window management         ✅ LOCKED
      → Budget tokens (15K input) + relevance ranking + tier-aware
      → 7 slots distribuidos:
         • System prompt:        ~1,500 tok (CACHED Layer 1)
         • Tool definitions:     ~1,500 tok (CACHED Layer 3)
         • Working memory:       ~2,000 tok
         • Short-term retrieval: ~3,000 tok
         • Long-term retrieval:  ~5,000 tok
         • Few-shot examples:    ~1,000 tok (CACHED Layer 4)
         • User query + reserva: ~1,000 tok
      → Re-ranking multi-factor:
         final_score = 0.5*sim + 0.2*recency + 0.2*importance + 0.1*graph
      → Token packing 'prefer_recent_and_relevant'
      → SIEMPRE incluir top-3 ranked por seguridad
      → Foundation Nodo 8 Tálamo (R5)
      → 📚 GUARDADO: RAG agentic loop (Candidato D) para v3 (R5)
        Brian explícitamente quiere mantener disponible

3.2.3 Prompt caching strategy           ✅ LOCKED
      → Cache stratificado por estabilidad (4 cache breakpoints)
      → Layer 1 AGENT_IDENTITY (~1,500 tok, hit ~99%)
      → Layer 2 DOMAIN_RULES (~500 tok, hit ~95%)
      → Layer 3 TOOL_DEFINITIONS (~1,500 tok, hit ~90%)
      → Layer 4 FEW_SHOT_EXAMPLES (~1,000 tok, hit ~85%)
      → Cache_control: ephemeral (TTL 5min Anthropic default)
      → Invalidación event-driven (no temporal)
      → Cache observability obligatoria:
         • cache_creation_input_tokens
         • cache_read_input_tokens
         • cache_hit_rate_per_layer
         • cost_saved_usd
         • cache_ttl_renewals
      → Alarma hit_rate <60% sostenido
      → Ahorro -62% costo Sonnet maduro

3.2.4 Function calling / tool use       ✅ LOCKED
      → Anthropic native tool_use + custom ToolRegistry
      → Tool Protocol abstracto
      → ToolRegistry acepta 3 backends:
         • LocalPythonTool (v1 default)
         • MCPServerTool (R4 llenará)
         • AgentDelegationTool (R5 Multi-Agent)
      → ToolExecutor loop estándar:
         • MAX_ITERATIONS=10 (hard limit)
         • TOOL_TIMEOUT=30s [B3 3.4 LOCKED reused]
         • tool_limiter CapacityLimiter
         • Audit cada tool_call
      → Permission model granular:
         • READ_MEMORY, WRITE_MEMORY
         • EXTERNAL_API, FILE_READ, FILE_WRITE
         • NETWORK_OUTBOUND, DELEGATE_AGENT
      → Permission check ANTES execute (NO LLM-decided)
      → 5 core tools LOCAL v1 predefinidas:
         • recall_memory
         • write_memory
         • list_workspace_skills
         • cancel_current_task
         • request_clarification
      → ALTER TABLE shared.workspaces:
         • allowed_tools TEXT[]
         • tool_permissions JSONB
      → ErrorType taxonomy (permission_denied, validation_error,
        timeout, external_api_error, unknown)
      → Streaming tool_use compatible (R7 frontend)
      → OpenAI fallback adapter (schema conversion)
```

#### Estructura módulo for3s_os/llm/ extendida (post-B2)

```
for3s_os/llm/
├── base.py                      → LLMProvider Protocol (B1)
├── anthropic_provider.py        → ClaudeProvider (B1)
├── openai_provider.py           → GPTProvider fallback (B1)
├── failover.py                  → FailoverManager (B1)
├── prompts/                     → 3.2.1 framework
│   ├── base.py
│   ├── templates/
│   ├── renderer.py
│   └── registry.py
├── context_builder.py           → 3.2.2 ContextBuilder
├── reranker.py                  → 3.2.2 multi-factor
├── token_packer.py              → 3.2.2 packing strategies
├── cache.py                     → 3.2.3 CacheManager
├── cache_invalidator.py         → 3.2.3 event-driven
├── tools/                       → 3.2.4 tool system
│   ├── base.py                  → Tool Protocol
│   ├── registry.py              → ToolRegistry
│   ├── executor.py              → ToolExecutor loop
│   ├── permissions.py           → Permission model
│   ├── local_python.py          → LocalPythonTool
│   ├── mcp_server.py            → MCPServerTool (R4 llena)
│   ├── agent_delegation.py      → AgentDelegationTool (R5)
│   └── core/                    → 5 core tools v1
│       ├── recall_memory.py
│       ├── write_memory.py
│       ├── list_skills.py
│       ├── cancel_task.py
│       └── request_clarification.py
├── cost_tracker.py              → per-workspace tracking (B1)
└── llm_observability.py         → tokens, latency, errors (B1)
```

#### Patrones obligatorios añadidos B2

```
✓ PromptTemplate renderiza con audit (audit_events)
✓ ContextBuilder asyncio.gather paralelo retrieval (3 tiers)
✓ Re-ranking SIEMPRE incluye top-3 por seguridad
✓ Cache breakpoints orden estabilidad descendente
✓ Cache_control marker SOLO final bloque cacheable
✓ Layer 1 (identity) NUNCA contenido dinámico
✓ ToolExecutor MAX_ITERATIONS=10 hard limit
✓ Permission check ANTES execute (no LLM-decided)
✓ tool_limiter CapacityLimiter [B3 3.4 LOCKED reused]
✓ TOOL_TIMEOUT=30s [B3 3.4 LOCKED reused]
✓ CancelledError re-raise siempre
✓ Audit cada render/build/cache/tool_call
✓ Alarma cache_hit_rate <60% sostenido
✓ Alarma tool_iterations >5 (debug)
```

#### Costo total v1 actualizado (R1+R2+R3 B1+B2)

```
SUBTOTAL R2 cerrado:                       USD ~43/mes
R3 BLOQUE 1:
   Claude Sonnet 4.6 principal:            USD ~50/mes
   OpenAI fallback LLM:                    USD ~$0.30/mes
R3 BLOQUE 2 (impacto neto caching):
   Caching maduro saving (-62%):           USD ~-$31/mes
   Tool overhead (~20% calls con tools):   USD ~+$6/mes (compensado)
─────────────────────────────────────────────────────────
TOTAL v1 (R1+R2+R3 B1+B2):                 USD ~62/mes

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$47
   → 5.4% del techo (vs 8.0% pre-B2)
   → MARGEN 94.6% para R3 B3-B4 + R4-R10

Verificación P5 cap LLM ($50-200/mes):
   Total LLM con caching maduro: ~$56/mes
   → 28% del cap (vs 43.5% pre-caching)
   → Margen $144 escalado workspaces
   → Caching habilita 2.5x más volumen DENTRO del cap P5
```

#### Cobertura Grafo Maestro post-B2 R3

```
NODOS servidos:
   ✅ Nodo 1 Hipocampo (ContextBuilder consume short-term)
   ✅ Nodo 3 PFC (templates + tool loop)
   🟡 Nodo 4 Cuerpo Calloso (foundation lista, R4 implementa)
   ✅ Nodo 5 Memoria Largo (ContextBuilder consume long-term)
   🟡 Nodo 8 Tálamo (foundation re-ranking, R5 implementa)
   🟡 Nodo 9 Dual-Process Check (preparación R5)
   ✅ Nodo 10 CLS (Haiku usa PromptTemplate)
   🟡 Nodo 11 Neuromoduladores (foundation tier dynamic)

PILARES:
   ✅ Pilar 1 Seguridad (permission + audit + timeout)
   ✅ Pilar 2 Escalabilidad (caching + budget + parallel)
   ✅ Pilar 3 Autonomía (LLM decide tools con guardrails)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → templates per workspace, cache separado
   2.B Open Core       → SDKs abiertos (Jinja2 BSD, Pydantic MIT)
   3.D Equipo pequeño  → vanilla Python sin frameworks pesados
```

#### Filosofía emergente del Bloque 2 R3

```
"Foundation universal de razonamiento: templates versionables,
contexto inteligente, caching agresivo, tool use limpio.
R4 y R5 solo necesitan llenar el qué — el cómo ya está."

   • TEMPLATES VERSIONABLES (3.2.1)
   • BUDGET TOKENS DETERMINISTA (3.2.2)
   • CACHING STRATIFICADO (3.2.3)
   • TOOL REGISTRY EXTENSIBLE (3.2.4)
   • FOUNDATION R4 + R5 LISTA
```

#### Foundation entregada a rondas futuras

```
R4 Tools/MCP Layer:
   • MCPServerTool clase abstracta lista
   • tool_definitions cacheables (Layer 3)
   • Permission model granular
   • Audit chain por tool_call
   • 5 core tools LOCAL pre-construidas
   • R4 solo decide: framework MCP, servers concretos,
     discovery/registration, hosting

R5 Orchestration / Multi-Agent:
   • AgentDelegationTool clase foundation
   • tool_use schema sub-agent invocation
   • Audit chain padre↔hijo lista
   • ContextBuilder foundation Nodo 8 Tálamo
   • Re-ranking foundation Nodo 9 routing
   • R5 decide: PFC orquestador, Tálamo router, Dual-Process

R7 Frontend / Channel:
   • Streaming tool_use compatible
   • Tool partial results foundation
   • ToolResult types (success/error/timeout)

R8 Observability:
   • Cache metrics obligatorias definidas
   • Tool metrics obligatorias definidas
   • Audit events render/build/cache/tool

R9 Security / Compliance:
   • Permission model granular foundation
   • Audit chain inmutable
   • Tool authorization foundation
   • R9 decide: amígdala safety, prompt injection detection
```

#### Riesgos legítimos aceptados (5)

```
1. Re-ranking puede omitir memoria crítica (3.2.2)
   Mitigación: top-3 siempre + observability + feedback loop v2

2. Penalty writes cache invalidado frecuentemente (3.2.3)
   Mitigación: Layer 1-2 estables diseño + event-driven invalidation

3. Loop infinito tool use (3.2.4)
   Mitigación: MAX_ITERATIONS=10 + audit + alarma >5 iterations

4. Permission bypass via prompt injection (3.2.4)
   Mitigación: check ANTES execute + audit chain + R9 amígdala

5. OpenAI fallback no soporta caching/parallel idéntico
   Mitigación: adapter + secuencial + audit visible (raro <1%)
```

#### Protocolo Bidireccional aplicado (OPCIÓN 4 Híbrido)

Spillovers identificados y ejecutados (2026-06-03):

```
✅ for3s-inter/07-operations/decision-log.md + D-013
✅ Mente/Cuerpo/Ronda_03_Bloque_2_Prompt_Context.md (detallado)
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (master actualizado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.undecies)

⏳ DIFERIDOS hasta cierre R3 completo (después B3+B4):
   • for3s-inter/09-technical-architecture/model-llm-layer.md
   • Actualización 09-technical-architecture/README.md (sección R3)
   • Actualización 02-product/mvp-scope.md (LLM stack final)
   • Actualización 05-finance/unit-economics.md (refresh costos)
```

#### Exploraciones futuras documentadas en Bloque 2

Lista completa en `Ronda_03_Bloque_2_Prompt_Context.md §10`. Resumen:

```
3.2.1: Custom strings, LangChain, DSPy v3, Anthropic Workbench,
       multi-language i18n, A/B testing framework, versionado auto

3.2.2: Stuffing (debug), Top-K fijo (descartado),
       ⭐ RAG agentic loop (Candidato D — GUARDADO POR BRIAN v3 R5),
       caching extremo, budget adaptativo, Cohere rerank,
       learned-to-rank, multi-query expansion, context compression

3.2.3: NO caching, cache mínimo, cache agresivo, 1h TTL beta v2,
       cache warm-up, cross-workspace cache, predictive invalidation,
       multi-tier cache (LLM + Valkey)

3.2.4: MCP-only, LangChain, custom JSON-RPC, DSPy ReAct v3,
       tool composition, tool ranking selection, tool result caching,
       streaming partial results, tool authorization workflows,
       tool versioning + rollback, cross-agent tool sharing
```

#### Próximo paso inmediato

**Arrancar R3 Bloque 3 — Streaming & Performance** → **EJECUTADO** 2026-06-03
Ver §3.1.duodecies para snapshot Bloque 3 LOCKED.

**Arrancar R3 Bloque 4 — Observabilidad & Costo LLM** → **EJECUTADO** 2026-06-03 ⭐ CIERRA R3 100%
Ver §3.1.terdecies para snapshot Bloque 4 + R3 100% cerrado.

---

### 3.1.duodecies — R3 BLOQUE 3 LOCKED (2026-06-03) — STREAMING & PERFORMANCE

**R3 BLOQUE 3 — STREAMING & PERFORMANCE CERRADO** (3/3 sub-temas LOCKED).

#### Las 3 decisiones LOCKED del Bloque 3 R3 (D-014)

```
3.3.1 Streaming responses               ✅ LOCKED
      → SSE (Server-Sent Events) HTTP estándar
      → FastAPI + sse_starlette MIT
      → Eventos LOCKED v1:
         • stream_start, text_delta, tool_use_*,
         • message_complete, fallback_activated,
         • stream_partial, error, stream_end
      → Cancel desde cliente: is_disconnected() check
      → Heartbeat: 15s ping si silencio
      → Reconnect/Resume: foundation v2 (Last-Event-ID param ignorado v1)
      → NO retry mid-stream (regla heredada por 3.3.3)
      → Partial preserve con audit_flag si stream se interrumpe

3.3.2 LLM concurrency control            ✅ LOCKED
      → Capa 1: CapacityLimiter(3) global [R2 B3 LOCKED reused]
      → Capa 2: Token Bucket per workspace en Valkey (NUEVO)
      → Tiers LOCKED v1:
         • pilot_light:  10 RPM / 10K TPM
         • pilot_pro:    50 RPM / 50K TPM
         • enterprise:   100 RPM / 100K TPM (v2)
      → Algoritmo: Token Bucket (NO Leaky Bucket)
      → Estimación pre-call: chars/3.5 × 1.1 margin
      → Refund/charge post-call con números reales
      → Estrategia exceso: wait max 30s → 429 Retry-After
      → Tool calls: heredan workspace bucket (1 RPM/agent.invoke)
      → Streaming: acquire UNA vez por stream
      → Anthropic 429 → trigger fallback + penalize bucket
      → Si Valkey down → fallback solo CapacityLimiter + alarma

3.3.3 Retry & fallback patterns          ✅ LOCKED
      → Taxonomía 14 ErrorTypes LOCKED:
         Transient:    NETWORK_TRANSIENT, PROVIDER_5XX, TIMEOUT
         Rate limit:   RATE_LIMIT_PROVIDER, RATE_LIMIT_CLIENT
         Permanent:    AUTH_FAILURE, BAD_REQUEST, SAFETY_FILTER
         Streaming:    STREAM_INTERRUPTED, STREAM_TIMEOUT
         Tool:         TOOL_PERMISSION, TOOL_VALIDATION,
                       TOOL_EXTERNAL_API, TOOL_TIMEOUT
      → RetryPolicy per ErrorType explícita
         (max_attempts, backoff, fallback_after, alarms)
      → Circuit Breaker per provider:
         CLOSED → OPEN: 5 errors 5xx/timeout en 60s
         OPEN → HALF_OPEN: tras 30s sleep
         HALF_OPEN → CLOSED: prueba exitosa
         HALF_OPEN → OPEN: prueba falla
      → NO retry mid-stream (preserve partial)
      → Tool retry separado del LLM retry
      → Idempotency metadata per tool (idempotent=True/False)
      → Tools NO idempotentes → NO retry
      → Headers cliente: Retry-After, X-LLM-Provider, X-Error-Type
      → Alarmas críticas:
         AUTH_FAILURE → Brian Telegram inmediato
         BOTH_PROVIDERS_DOWN → Brian crítico
         Circuit OPEN >5min → Brian + log
      → Respect opt-out: allow_llm_fallback workspace flag
      → Penalize bucket: en rate_limit_provider (coord 3.3.2)
```

#### Estructura módulo for3s_os/llm/ extendida (post-B3)

```
for3s_os/llm/
├── base.py                         → LLMProvider Protocol (B1)
├── anthropic_provider.py           → ClaudeProvider (B1)
├── openai_provider.py              → GPTProvider fallback (B1)
├── failover.py                     → FailoverManager (B1, extendido B3)
├── prompts/                        → 3.2.1 framework (B2)
├── context_builder.py              → 3.2.2 (B2)
├── reranker.py                     → 3.2.2 (B2)
├── token_packer.py                 → 3.2.2 (B2)
├── cache.py                        → 3.2.3 (B2)
├── cache_invalidator.py            → 3.2.3 (B2)
├── tools/                          → 3.2.4 (B2)
├── streaming/                      → 3.3.1 NUEVO B3
│   ├── sse.py                      → SSE transport
│   ├── orchestrator.py             → StreamOrchestrator
│   ├── events.py                   → SSE event types
│   └── heartbeat.py                → 15s ping
├── concurrency/                    → 3.3.2 NUEVO B3
│   ├── controller.py               → ConcurrencyController
│   ├── token_bucket.py             → Valkey-backed
│   ├── tier_limits.py              → Tiers LOCKED
│   └── estimator.py                → Token estimation
├── resilience/                     → 3.3.3 NUEVO B3
│   ├── manager.py                  → ResilienceManager
│   ├── taxonomy.py                 → 14 ErrorTypes
│   ├── policies.py                 → RetryPolicy per type
│   ├── circuit_breaker.py          → Per-provider CB
│   ├── error_mapping.py            → Provider error → ErrorType
│   └── client_errors.py            → HTTP status + messages
├── cost_tracker.py                 → per-workspace (B1)
└── llm_observability.py            → métricas (B1, extendido B3)
```

#### Patrones obligatorios añadidos B3

```
✓ SSE events estándar (event: + data:)
✓ is_disconnected() check cada yield
✓ llm_limiter wrap completo del stream
✓ Heartbeat 15s si silencio
✓ NO retry mid-stream
✓ Partial preserve con audit_flag
✓ Token Bucket acquire UNA vez por stream
✓ Estimation pre-call con margin 10%
✓ Refund/charge post-call con números reales
✓ Tiers per workspace LOCKED
✓ wait max 30s antes de 429
✓ Anthropic 429 → trigger fallback + penalize bucket
✓ Circuit breaker per provider (5/60s → OPEN, 30s → HALF_OPEN)
✓ NO retry types permanentes (auth, bad_request, safety)
✓ Tool retry separado del LLM retry
✓ Idempotency declarada per tool
✓ Headers cliente obligatorios
✓ Alarmas críticas (auth, both_down, CB OPEN >5min)
✓ Audit cada retry + state change + fallback
✓ Respect allow_llm_fallback opt-out
```

#### Costo total v1 actualizado (R1+R2+R3 B1+B2+B3)

```
SUBTOTAL R2 cerrado:                       USD ~43/mes
R3 BLOQUE 1:                                ~$50/mes + ~$0.30/mes fallback
R3 BLOQUE 2 (impacto caching maduro):       -$31/mes saving + $6/mes overhead
R3 BLOQUE 3 (impacto resilience):           $0 infra + ~-$5-10/mes saving
─────────────────────────────────────────────────────────
TOTAL v1 (R1+R2+R3 B1+B2+B3):              USD ~57-62/mes

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$45
   → 5.1% del techo
   → MARGEN 94.9% para R3 B4 + R4-R10

Verificación P5 cap LLM ($50-200/mes):
   Token bucket per workspace = enforcement AUTOMÁTICO
   Pilot Light hard-capped a 10 RPM / 10K TPM = ~$50/mes max
   Pilot Pro hard-capped a 50 RPM / 50K TPM = ~$200/mes max
```

#### Cobertura Grafo Maestro post-B3 R3

```
NODOS:
   ✅ Nodo 3 PFC (pleno con streaming + concurrency + resilience)
   🟡 Nodo 6 Sistema Sensorial (foundation streaming I/O)
   🟡 Nodo 8 Tálamo (foundation concurrency awareness)
   🟡 Nodo 11 Neuromoduladores (foundation stress level)

PILARES:
   ✅ Pilar 1 Seguridad (audit + idempotency + workspace fairness)
   ✅ Pilar 2 Escalabilidad (streaming + bucket + circuit breaker)
   ✅ Pilar 3 Autonomía (retry decisions + tool resilience)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → tiers per workspace + fairness + opt-out
   2.B Open Core       → sse_starlette MIT + asyncio stdlib + valkey-py MIT
   3.D Equipo pequeño  → todo en código vanilla, alarmas a Brian directo
```

#### Filosofía emergente del Bloque 3 R3

```
"Resiliencia operacional sin sobre-ingeniería. Cada componente
del Bloque 3 maneja un tipo específico de falla con la mínima
complejidad necesaria. La UX percibida del usuario es lo más
importante — streaming hace que se sienta rápido, concurrency
control evita que se caiga, retry/fallback hace que se recupere."

   • UX MODERNA (3.3.1)
   • ENFORCEMENT AUTOMÁTICO (3.3.2)
   • ERRORES TRATADOS CORRECTAMENTE (3.3.3)
   • INTEGRACIÓN PROFUNDA CON B1+B2
   • FOUNDATION RONDAS FUTURAS
```

#### Foundation entregada a rondas futuras

```
R3 B4 Observability:
   • Métricas obligatorias 60+ definidas (B1+B2+B3)
   • Audit chain meta-audit completo
   • Cost tracking foundation per workspace
   • Token bucket = visibility per workspace nativa
   • Circuit breaker state observable per provider

R4 Tools/MCP Layer:
   • Tool retry separado del LLM retry
   • Idempotency metadata foundation
   • Tool error types en taxonomía
   • Streaming tool_use compatible

R5 Orchestration/Multi-Agent:
   • Streaming sub-agent invocation compatible
   • Concurrency control hereda a sub-agents
   • Resilience taxonomy reused para Nodo 9 Dual-Process

R7 Frontend/Channel:
   • Streaming SSE protocol LOCKED
   • Eventos canónicos LOCKED
   • Cancel API + heartbeat protocol
   • Headers cliente estandarizados

R8 Observability:
   • Métricas obligatorias definidas
   • Audit chain inmutable
   • Circuit breaker state observable

R9 Security/Compliance:
   • AUTH_FAILURE alarma crítica
   • Workspace fairness anti-DoS interno
   • Audit inmutable retries/fallbacks/circuit
   • Idempotency tools preserve integrity
```

#### Riesgos legítimos aceptados (6)

```
1. Cloudflare Tunnel buffer puede romper SSE
   Mitigación: sse_starlette + X-Accel-Buffering:no + tests

2. Valkey down → fallback degraded
   Mitigación: solo CapacityLimiter + alarma + log

3. Token estimation mal calibrada
   Mitigación: refund/charge post-call + ajuste v2 con datos

4. Taxonomía error incompleta
   Mitigación: default NETWORK_TRANSIENT + revisión mensual

5. Circuit breaker oscilante
   Mitigación: success consecutive + alarma >10 transitions/hora

6. Auth failure alarma fatiga
   Mitigación: distinguir 401 expired vs invalid + cooldown 1h
```

#### Protocolo Bidireccional aplicado (OPCIÓN 4 → luego OPCIÓN 1)

Spillovers identificados y ejecutados FASE 1 (2026-06-03):

```
✅ for3s-inter/07-operations/decision-log.md + D-014
✅ Mente/Cuerpo/Ronda_03_Bloque_3_Streaming_Performance.md (detallado)
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (master actualizado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.duodecies)

EJECUTANDO FASE 2 (OPCIÓN 1 — spillovers diferidos B1+B2+B3):
   ⏳ for3s-inter/09-technical-architecture/model-llm-layer.md
   ⏳ for3s-inter/09-technical-architecture/README.md (sección R3)
   ⏳ for3s-inter/02-product/mvp-scope.md (LLM stack annotation)
   ⏳ for3s-inter/05-finance/unit-economics.md (refresh costos)
```

#### Próximo paso inmediato

**Decisión Brian:** continuar Bloque 4 (decisión tomada 2026-06-03).
Bloque 4 ejecutado completo. R3 ahora 100% CERRADO.

---

### 3.1.terdecies — R3 BLOQUE 4 LOCKED + R3 100% CERRADO (2026-06-03) — OBSERVABILIDAD & COSTO LLM

**R3 BLOQUE 4 — OBSERVABILIDAD & COSTO LLM CERRADO** (3/3 sub-temas LOCKED).
**⭐ R3 — MODEL/LLM LAYER 100% CERRADO** (14/14 sub-temas, 4/4 bloques).

#### Las 3 decisiones LOCKED del Bloque 4 R3 (D-015)

```
3.4.1 LLM observability                ✅ LOCKED
      → Audit chain Postgres (forensics 13m) + Prometheus LOCAL (15d)
      → prometheus_fastapi_instrumentator MIT + prometheus_client Apache
      → Endpoint /metrics (auth interno)
      → ~25 métricas LLM-specific LOCKED:
         Tokens: input/output/cache_read/cache_write
         Latency: request_duration, ttft, tokens_per_second
         Cost: cost_usd, cost_saved_caching
         Cache: hit_rate per layer, ttl_renewals
         Concurrency: acquire, wait_seconds, rate_limit_exceeded, 429s
         Bucket: rpm_remaining, tpm_remaining
         Limiter: in_flight, queue_depth
         Resilience: retry_attempts, retry_success, fallback_activated
         Circuit: state per provider
         Tools: execution, duration, retry
         Streaming: active_count, partial, cancelled
         Quality: eval_score
      → Storage Prometheus: ~200 MB RAM, ~5 GB disco
      → Cardinality limit ~1200 series max
      → Scrape interval 15s
      → LLMCallRecorder wrapper atomic (audit + metrics juntos)
      → Foundation R8 Grafana dashboards
      → Compliance B2B (datos LOCAL, no salen)

3.4.2 Cost monitoring per workspace    ✅ LOCKED
      → Sistema completo con 5 capacidades coordinadas:
      
      CAPACIDAD 1: Alarmas graduales
         • 50% cap → email cliente + dashboard banner
         • 75% cap → email + dashboard + Telegram Brian
         • 90% cap → email + Telegram Brian inmediato
         • 100% cap → hard stop (B3 3.3.2)
         • Dedupe: 1 por threshold per mes
         • Arq cron cada 15 min
      
      CAPACIDAD 2: Dashboard cliente self-service
         • Endpoint /workspaces/{id}/cost-dashboard
         • Auth workspace_id token
         • Métricas: cap, current cost, %, días restantes,
                     forecast, breakdown por modelo, cache savings
         • HTMX + Jinja2 (reused B2 3.2.1)
      
      CAPACIDAD 3: Anomaly detection statistical
         • Algoritmo 3-sigma sobre baseline 7d
         • 4 tipos LOCKED:
            - spike_hour: bug nuestro probable → notify Brian
            - spike_sustained: cliente growth → suggest upgrade
            - key_leaked: AUTO-SUSPEND + notify crítico
            - bug_loop: notify Brian crítico
         • Arq cron cada 5 min
      
      CAPACIDAD 4: Forecast end-of-month
         • Algoritmo: daily_avg × days_in_month
         • Dashboard color: verde<75%, amarillo 75-90%, rojo>90%
         • Alarma si forecast >100% cap
      
      CAPACIDAD 5: Reporting recurring
         • Daily 9 AM digest Brian (Telegram)
         • Weekly Mon 9 AM digest clientes (email)
         • Monthly day 1 9 AM report clientes (email)
         • Templates Jinja2 (reused B2 3.2.1)
         • Arq cron (reused R2 B3)
      
      SQL nuevas: cost_alarms + cost_anomalies tables
      Email engine: SMTP local v1 (SendGrid/SES v2)
      USD-only v1 (multi-currency R10)

3.4.3 LLM quality evaluation           ✅ LOCKED
      → Framework híbrido 4 capas complementarias:
      
      CAPA 1: Rule-based checks (sync, deterministic, blocking critical)
         • Format compliance (JSON, Pydantic schema)
         • Length checks, forbidden phrases
         • PII leakage detection (regex)
         • Tool call validity, citation presence
         • Costo $0, latencia <10ms, cobertura ~30%
      
      CAPA 2: Golden datasets (CI/CD + weekly cron)
         • general/v1.0 (50 Q&A representativas)
         • code/v1.0 (30 ejemplos análisis PR wedge QA)
         • Format YAML + tabla SQL versioned
         • Triggers:
            - CI/CD pre-deploy: full dataset
            - Weekly cron: full regression check
            - Daily cron: 5 random smoke test
         • Costo ~$0.10/full run, cobertura ~50%
      
      CAPA 3: LLM-as-judge Haiku (async background, 5% sample)
         • Sample rate 5% default (configurable)
         • Modelo: Claude Haiku 4.5
         • Multi-prompt rotation (3 evaluators)
         • Dimensiones per dominio:
            General: correctness, relevance, completeness,
                     coherence, safety, format
            Code: correctness, no_bugs, idiomatic, complete
            Health: safety_first, evidence_based, no_diagnosis, refs
         • Costo ~$5-15/mes, cobertura ~70%
      
      CAPA 4: Human review Brian (weekly + escalation)
         • Triggers escalation:
            - LLM-judge score <3 (any dimension)
            - Cliente marca "respuesta mala"
            - Anomaly detection signals quality drop
            - Random 1/día (calibration)
         • Frecuencia ~5-10 calls/semana max
         • Tiempo Brian ~30 min/semana
         • Cobertura 100% issues complejos
      
      Anti-sesgo strategies LOCKED (5):
         1. Evaluator anonymization (no sabe qué modelo generó)
         2. Multi-prompt rotation (3 evaluators)
         3. Golden references comparative
         4. Periodic human calibration (weekly Brian)
         5. Evaluator diversity v2 (cross-validator GPT-4o-mini futuro)
      
      SQL nuevas: eval_runs + eval_results + golden_datasets
      Cost cap eval: $15/mes hard (dentro cap P5)
      Multi-dominio: yaml configs extensible
```

#### Estructura módulo for3s_os/llm/ FINAL (post-R3 100%)

```
for3s_os/llm/
├── base.py                         → LLMProvider Protocol (B1)
├── anthropic_provider.py           → ClaudeProvider (B1)
├── openai_provider.py              → GPTProvider fallback (B1)
├── failover.py                     → FailoverManager (B1, ext B3)
├── prompts/                        → 3.2.1 (B2)
├── context_builder.py              → 3.2.2 (B2)
├── reranker.py                     → 3.2.2 (B2)
├── token_packer.py                 → 3.2.2 (B2)
├── cache.py                        → 3.2.3 (B2)
├── cache_invalidator.py            → 3.2.3 (B2)
├── tools/                          → 3.2.4 (B2)
├── streaming/                      → 3.3.1 (B3)
├── concurrency/                    → 3.3.2 (B3)
├── resilience/                     → 3.3.3 (B3)
├── observability/                  → 3.4.1 (B4) ⭐ NEW
│   ├── llm_metrics.py              → Prometheus métricas
│   ├── recorder.py                 → LLMCallRecorder atomic
│   └── instrumentator.py           → FastAPI setup
├── cost/                           → 3.4.2 (B4) ⭐ NEW
│   ├── monitor.py                  → CostMonitor 5 capacidades
│   ├── alarms.py                   → 3 thresholds graduales
│   ├── anomaly.py                  → Statistical 3-sigma
│   ├── forecast.py                 → daily_avg × days
│   ├── dashboard.py                → Endpoint cliente
│   └── reporting.py                → Cron digest/report
├── eval/                           → 3.4.3 (B4) ⭐ NEW
│   ├── framework.py                → Orchestrator
│   ├── rule_based.py               → CAPA 1
│   ├── golden_dataset.py           → CAPA 2
│   ├── llm_judge.py                → CAPA 3 Haiku
│   ├── human_review.py             → CAPA 4 queue
│   ├── calibration.py              → Anti-sesgo
│   └── golden_datasets/            → YAML files
│       ├── general/v1.0/
│       └── code/v1.0/
├── cost_tracker.py                 → per-workspace (B1)
└── llm_observability.py            → métricas (B1, ext B3+B4)
```

#### Patrones obligatorios añadidos B4

```
✓ Prometheus LOCAL en mismo servidor (NO externalizado)
✓ Retención 15 días Prometheus + 13 meses audit Postgres
✓ Scrape interval 15s, métricas LOCKED ~25
✓ /metrics endpoint con auth interno
✓ Cardinality limit hard (1200 series)
✓ LLMCallRecorder atomic (audit + metrics juntos)
✓ Alarmas graduales 50/75/90% dedupe per mes
✓ Background jobs Arq:
   - alarmas check 15 min
   - anomaly detection 5 min
   - daily digest 9 AM
   - weekly digest Mon 9 AM
   - monthly report day 1 9 AM
✓ Dashboard cliente con workspace_id auth
✓ Anomaly 3-sigma sobre baseline 7d
✓ 4 tipos anomaly clasificados
✓ Auto-actions: key_leaked SUSPEND
✓ Eval 4 capas obligatorias
✓ Sample rate LLM-judge 5%
✓ Anti-sesgo: 5 strategies LOCKED
✓ Golden datasets versioned YAML + SQL
✓ CI/CD pre-deploy full dataset
✓ Human review triggers automáticos (4)
✓ Audit cada eval run + alarm + anomaly
✓ Critical rule failures REJECT response
✓ Otros eval failures NO bloquean (audit + flag)
✓ Cost cap eval $15/mes hard
```

#### Costo total v1 FINAL (R1+R2+R3 100% LOCKED)

```
SUBTOTAL R1+R2:                            USD ~43/mes
R3 BLOQUE 1:                                +$50.30/mes
R3 BLOQUE 2 (caching neto):                 -$25/mes
R3 BLOQUE 3 (resilience neto):              -$5-10/mes
R3 BLOQUE 4 (observability + eval):         +$5-15/mes
─────────────────────────────────────────────────────────
TOTAL v1 FINAL:                             USD ~62-77/mes

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$55
   → 6.3% del techo
   → MARGEN 93.7% para R4-R10

Verificación P5 cap LLM ($50-200/mes):
   Total LLM v1 FINAL: $61-71/mes
   → 31-36% del cap medio
   → Margen $130-140 escalado workspaces
   → Caching + eval + observability DENTRO cap P5
```

#### Cobertura Grafo Maestro post-R3 100%

```
NODOS servidos:
   ✅ Nodo 1 Hipocampo (B2 context)
   ✅ Nodo 3 PFC (pleno B1+B2+B3+B4)
   ✅ Nodo 5 Memoria Largo (B2 context)
   ✅ Nodo 10 CLS (Haiku + tmpl + eval B4)
   🟡 Nodo 4 Cuerpo Calloso (foundation B2)
   🟡 Nodo 6 Sistema Sensorial (foundation B3 streaming)
   🟡 Nodo 8 Tálamo (foundation B2+B3 ranking+concurrency)
   🟡 Nodo 9 Dual-Process Check (eval informa B4)
   🟡 Nodo 11 Neuromoduladores (B3+B4 signals)

PILARES post-R3 COMPLETO:
   ✅ Pilar 1 Seguridad (audit + permissions + anomaly + eval safety + PII)
   ✅ Pilar 2 Escalabilidad (caching + streaming + budget + observability + forecast)
   ✅ Pilar 3 Autonomía (LLM + tools + retry + eval feedback + anomaly auto-actions)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → tiers + templates + alarmas + eval per workspace
   2.B Open Core       → SDKs MIT/BSD/Apache 8+ libraries
   3.D Equipo pequeño  → todo vanilla Python sin frameworks pesados, operable 1 persona
```

#### Filosofía emergente del Bloque 4 R3

```
"Observability LLM-specific + cost monitoring + quality evaluation
no son features — son lo que separa 'wrapper Claude bonito' de
plataforma producción-ready B2B. Cada capa de B4 mitiga
debilidades de las anteriores con interdependencia coordinada."

   • OBSERVABILITY DUAL (audit + Prometheus)
   • COST MONITORING COORDINADO (5 capacidades)
   • EVAL HÍBRIDO ANTI-SESGO (4 capas)
   • INTEGRACIÓN PROFUNDA con B1+B2+B3 (zero duplicación)
   • FOUNDATION COMERCIAL REAL (defendible enterprise B2B)
```

#### Foundation entregada a rondas futuras (R3 100% completo)

```
R4 Tools/MCP Layer:
   ✅ Tool retry separado + idempotency + tool metrics + tool eval rule-based
   • R4 decide: MCP framework, MCP servers concretos, hosting

R5 Orchestration/Multi-Agent:
   ✅ Streaming sub-agent + concurrency hereda + eval informa Nodo 9 + cost tracking
   • R5 decide: PFC orquestador, Tálamo router, Dual-Process Check, Multi-Agent lifecycle

R6 Memory Stack extensions:
   ✅ Eval informa CLS promotion + cost-aware retrieval + memory metrics
   • R6 decide: tier rebalancing, procedural memory, semantic extensions

R7 Frontend / Channel:
   ✅ SSE protocol + dashboard cliente HTMX foundation + quality scores expuestos
   • R7 decide: framework, Telegram bot, UX streaming

R8 Observability completa:
   ✅ Prometheus métricas ~25 + audit chain inmutable + foundation Grafana
   • R8 decide: Grafana setup, dashboards, distributed tracing, alerting rules

R9 Security/Compliance:
   ✅ AUTH_FAILURE alarma + anomaly key_leaked + eval safety + PII detection
   • R9 decide: Amígdala, prompt injection detection, adversarial eval, SOC2/ISO27001

R10 CI/CD/Deploy:
   ✅ Eval pre-deploy regression + cost forecasting + observability metrics
   • R10 decide: billing integration, multi-currency, CI/CD pipeline, deploy strategy
```

#### Riesgos legítimos aceptados (6)

```
1. Cardinality explosion Prometheus
   Mitigación: límites duros + cardinality audit mensual

2. False positive anomaly detection
   Mitigación: cliente puede reportar OK + ajuste thresholds post-launch

3. Email delivery falla SMTP
   Mitigación: retry queue Arq + fallback Telegram Brian

4. LLM-judge sesgo Anthropic-self
   Mitigación: 5 anti-bias strategies LOCKED + v2 cross-validator

5. Golden datasets sesgo curation Brian
   Mitigación: revisión clientes + community-sourced v2

6. Human review queue se acumula
   Mitigación: Telegram alert + auto-archive + weekly batch
```

#### Protocolo Bidireccional aplicado (FASE 1 OPCIÓN 4 + FASE 2 OPCIÓN 1)

Spillovers FASE 1 ejecutados (2026-06-03):

```
✅ for3s-inter/07-operations/decision-log.md + D-015
✅ Mente/Cuerpo/Ronda_03_Bloque_4_Observability_Cost.md (detallado)
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (master 100% CERRADO)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.terdecies)

EJECUTANDO FASE 2 (OPCIÓN 1 — cierre formal R3 público):
   ⏳ for3s-inter/09-technical-architecture/model-llm-layer.md (agregar B4)
   ⏳ for3s-inter/09-technical-architecture/README.md (R3 → ✅ CERRADO 100%)
   ⏳ for3s-inter/02-product/mvp-scope.md (LLM stack FINAL R3)
   ⏳ for3s-inter/05-finance/unit-economics.md (costo total final)
```

#### R3 — STATUS FINAL

```
╔══════════════════════════════════════════════════════════════╗
║   ✅✅✅ R3 — MODEL/LLM LAYER 100% CERRADO ✅✅✅              ║
║                                                                ║
║   Bloque 1 ✅ LOCKED (4/4) — D-012                              ║
║   Bloque 2 ✅ LOCKED (4/4) — D-013                              ║
║   Bloque 3 ✅ LOCKED (3/3) — D-014                              ║
║   Bloque 4 ✅ LOCKED (3/3) — D-015 ⭐ CIERRA R3                  ║
║                                                                ║
║   TOTAL: 14/14 sub-temas LOCKED (100%)                          ║
║   Tiempo total: 2026-06-01 → 2026-06-03 (3 días)                ║
╚══════════════════════════════════════════════════════════════╝
```

#### Próximo paso inmediato (post-FASE 2)

**Iniciar R4 — Tools / MCP Layer** → **EJECUTANDO 2026-06-06**
Bloque 1 LOCKED — Ver §3.1.quaterdecies
Bloque 2 LOCKED — Ver §3.1.quindecies

---

### 3.1.quaterdecies — R4 BLOQUE 1 LOCKED (2026-06-06) — MCP FRAMEWORK & DISCOVERY

**R4 BLOQUE 1 — MCP FRAMEWORK & DISCOVERY CERRADO** (4/4 sub-temas LOCKED).

#### Pre-preguntas P1-P3 LOCKED (antes del Bloque 1)

```
P1 — MCP servers v1:           GitHub + Filesystem + HTTP + Telegram
   • Compromise: wedge QA + foundation universal + Brian comm
   • Slack y otros: defer R4 v2

P2 — MCP hosting v1:           LOCAL primero, cloud opcional v2
   • Cumple D-009 LOCAL + compliance B2B máximo
   • Código abstraction-aware (swap futuro)

P3 — Tool authorization v1:    Permission + whitelist + human-in-loop opcional
   • Tools no sensibles: ejecutan directo
   • Tools sensibles: require_confirmation → Telegram approve
   • Foundation enterprise B2B
```

#### Aclaración arquitectónica crítica

```
CONSTRAINT BRIAN APORTADO:
   "Clientes quieren seguridad y privacidad"

PIVOTE ARQUITECTÓNICO:
   • NO usar Kubernetes v1 (8 sem setup, +3 GB RAM, no da más security)
   • SÍ usar Docker Multi-tenant con CONTAINER PER CLIENTE
   • Tools shared stateless
   • 3-layer compliance (DB + container + network)
   • BYOC enabled
   • K8s-ready foundation (8 best practices)
```

#### Las 4 decisiones LOCKED del Bloque 1 R4 (D-016)

```
4.1.1 MCP client framework        ✅ LOCKED
      → mcp Python SDK oficial Anthropic (>=1.0,<2.0, MIT)
      → Abstraction layer interno MCPClient Protocol
      → Wrapper MCPServerTool adapta a Tool Protocol (B2 3.2.4)
      → Transport v1: stdio (servers LOCAL P2)
      → Transport ready v2: SSE + websocket
      → Async-first asyncio + anyio
      → AsyncExitStack lifecycle FastAPI startup/shutdown
      → Naming: "{server}_{tool}" (github_get_pr, fs_read_file)
      → TOOL_TIMEOUT 30s reused (R2 B3)
      → ErrorType reused (B3 3.3.3): TOOL_EXTERNAL_API / TOOL_TIMEOUT
      → require_confirmation flag heredado (P3)
      → Permission check ANTES execute (B2 3.2.4)

4.1.2 Tool discovery / registration  ✅ LOCKED
      → HÍBRIDO A+C optimizado
      → Foundation A: static config + startup discovery + per-workspace whitelist
      → + 5 triggers event-driven hot-reload (sin TTL temporal):
         1. Admin endpoint POST /admin/mcp/reload/{server}
         2. File watcher mcp_servers.yaml (watchfiles MIT)
         3. MCP push notification (list_changed spec)
         4. Workspace allowed_tools change hook
         5. Background retry exitoso auto-reload
      → _refresh_lock asyncio.Lock anti race conditions
      → Rollback automático si reload falla
      → Rate limit: max 1 reload/server/10s
      → Layer 3 cache invalidation GRANULAR per workspace
      → Eventually consistent
      → NO TTL temporal (explícito: no "reset cada rato")
      → Background retry [10s, 60s, 5min, 30min] → abandon + notify
      → Static config: config/mcp_servers.yaml + Pydantic validation
      → Admin endpoints: /admin/mcp/reload, /reload-all, /status

4.1.3 MCP server hosting              ✅ LOCKED
      → Docker Multi-tenant 3 capas
      → ARQUITECTURA 3 CAPAS:
         • Capa 1 systemd (host): PostgreSQL + Valkey + Prometheus + Docker daemon
         • Capa 2 containers compartidos:
           - For3s core: for3s-api, for3s-arq, for3s-orchestrator
           - MCP tools shared: mcp-github, mcp-filesystem, mcp-http, mcp-telegram
         • Capa 3 containers exclusivos per cliente:
           - workspace-{cliente} con volumes + secrets + memory privados
      → AISLAMIENTO 3 NIVELES:
         • Lógico: schema per workspace en PostgreSQL (R2 B1)
         • Físico: container Docker per cliente (NEW R4)
         • Red: Docker network per cliente (NEW R4)
      → NETWORKING (4 bridges):
         • for3s-public-net: único entry externo (Cloudflare Tunnel)
         • for3s-core-net: internal core services
         • for3s-mcp-net: internal MCP tools
         • workspace-{cliente}-net: aislamiento per cliente
      → RESOURCE QUOTAS Docker per tier:
         • Pilot Light:  512 MB RAM, 0.5 CPU
         • Pilot Pro:    2 GB RAM, 2 CPU
         • Enterprise:   custom
      → PROVISIONING AUTOMÁTICO scripts:
         • provision_workspace.sh (~30s onboarding)
         • deprovision_workspace.sh (kill switch físico)
         • backup_workspace.sh (per cliente)
         • migrate_workspace_tier.sh (upgrade en segundos)
      → MCP TOOLS SHARED (stateless multi-tenant):
         • Reciben workspace_id en cada call
         • NO almacenan data cliente
         • Pitch: "shared services como load balancer"
      → K8s-READY DOCKER (8 best practices):
         • HEALTHCHECK formal
         • Imágenes pinned SHA (no :latest)
         • Env vars + secrets explícitos
         • Resource limits compose
         • Logs stdout/stderr (12-factor)
         • Stateless containers
         • Multi-stage Dockerfiles
         • Non-root user
      → BYOC ENABLED: workspace containers exportables
      → NO Kubernetes v1 (defer triggers objetivos v3+)
      → Diagrama detallado: DEFER fase implementación

4.1.4 Tool authentication & secrets   ✅ LOCKED
      → PostgreSQL encrypted secrets + KEK hierarchy
      → ENCRYPTION: AES-256-GCM con nonce random per encrypt
      → LIBRARY: cryptography (PyPA, BSD)
      → KEY HIERARCHY:
         • Master KEK: /etc/for3s/master_key (chmod 400, root only)
         • Workspace KEK: HKDF-SHA256(master, workspace_id)
         • Per-secret: cifrado con workspace KEK + nonce
      → SCHEMA SQL NUEVAS:
         • shared.workspace_secrets (encrypted_value + nonce + kek_version)
         • shared.secret_usage_audit (audit trail per-usage)
      → MASTER KEK BACKUP OFFLINE OBLIGATORIO:
         • Backup #1: USB hardware Brian custodia (encrypted passphrase)
         • Backup #2: paper safe (Shamir's Secret Sharing si compliance)
         • Backup #3: succession plan familiar
         • NO backup cloud (defeats LOCAL)
         • NO backup junto al servidor (single point failure)
      → PER-REQUEST FLOW:
         • SecretsManager.get(workspace_id, secret_name, used_by, used_for, request_id)
         • Decrypt en memoria ms → use → discard plaintext
         • Brian NUNCA ve plaintext (defense in depth)
      → AUDIT TRAIL COMPLETO:
         • secret_stored, secret_used, secret_rotated, secret_deleted, secret_expired
      → CLIENTE SELF-SERVICE:
         • Rotation vía dashboard
         • Auto-rotation reminders (Arq cron 7 días antes expiry)
         • Email notification cliente
      → KILL SWITCH:
         • docker rm workspace + DELETE workspace_secrets CASCADE
      → COMPARTIDOS FOR3S:
         • workspace_id='for3s_shared' entry especial
         • Admin-managed: Anthropic API key, OpenAI fallback, etc.
      → ARCHITECTURAL ISOLATION:
         • MCP containers NO acceden Postgres directo (reciben como params)
         • Workspace containers NO acceden Postgres directo (vía for3s-api)
         • Workspace KEK cache in-memory (no Valkey extra)
      → PERFORMANCE: AES-NI hardware accel (<2ms per decrypt)
      → COMPATIBLE: P3 + P4 + R2 B1 + 4.1.3
```

#### Estructura módulo for3s_os/ extendida (post-R4 B1)

```
for3s_os/
├── llm/                            → R3 (intacto)
├── secrets/                        → 4.1.4 NUEVO R4
│   ├── manager.py                  → SecretsManager (KEK + crypto)
│   ├── master_kek.py               → Carga + backup verification
│   ├── workspace_kek.py            → HKDF derivation + cache
│   └── audit.py                    → secret_usage_audit logging
├── mcp/                            → 4.1.1-4.1.3 NUEVO R4
│   ├── client/
│   │   ├── base.py                 → MCPClient Protocol (abstraction)
│   │   ├── official.py             → OfficialMCPClient (mcp SDK)
│   │   └── pool.py                 → MCPClientPool (lifecycle)
│   ├── discovery/
│   │   ├── orchestrator.py         → MCPHotReloadOrchestrator (5 triggers)
│   │   ├── config_loader.py        → mcp_servers.yaml parser
│   │   ├── workspace_resolver.py   → WorkspaceToolResolver
│   │   └── file_watcher.py         → watchfiles integration
│   ├── server_tool.py              → MCPServerTool (wrapper Tool Protocol)
│   └── health.py                   → MCPHealthMonitor
├── admin/                          → NUEVO R4
│   └── mcp_endpoints.py            → /admin/mcp/reload, /status
└── ...

config/
└── mcp_servers.yaml                → Static config (4 servers v1)

containers/                          → NUEVO R4
├── docker-compose.yml              → CAPA 2 core + MCP shared
├── docker-compose.workspaces.yml   → CAPA 3 generated per client
├── for3s-api/Dockerfile
├── for3s-arq/Dockerfile
├── for3s-orchestrator/Dockerfile
├── workspace-template/Dockerfile
└── mcp-servers/
    ├── github/
    ├── filesystem/
    ├── http/
    └── telegram/

scripts/                             → NUEVO R4
├── provision_workspace.sh
├── deprovision_workspace.sh
├── backup_workspace.sh
└── migrate_workspace_tier.sh
```

#### Patrones obligatorios añadidos R4 B1

```
✓ MCPClient Protocol abstraction (swap futuro)
✓ AsyncExitStack lifecycle MCP servers
✓ Discovery paralelo asyncio.gather al startup
✓ Background retry MCP failed servers ([10s,60s,5m,30m])
✓ 5 triggers event-driven hot-reload (sin TTL)
✓ _refresh_lock asyncio.Lock anti race
✓ Rollback automático si reload falla
✓ Layer 3 cache invalidation granular per workspace
✓ Docker Multi-tenant 3 capas obligatorio
✓ Container per cliente (Capa 3)
✓ MCP tools shared stateless (Capa 2)
✓ Networking aislado per cliente (4 Docker bridges)
✓ Resource quotas Docker per tier
✓ K8s-ready 8 best practices Dockerfile
✓ Master KEK chmod 400 + backup OFFLINE OBLIGATORIO
✓ Workspace KEK HKDF derivation + cache in-memory
✓ Per-secret AES-256-GCM con nonce random
✓ Per-request decrypt memoria ms → discard
✓ Audit per-uso secret_usage_audit
✓ Cliente self-service rotation
✓ Auto-rotation reminders (Arq cron)
✓ Kill switch CASCADE delete
✓ Brian NUNCA ve plaintext (defense in depth)
```

#### Costo total v1 actualizado (post-R4 B1)

```
SUBTOTAL R1+R2+R3 100%:                       USD ~62-77/mes
R4 BLOQUE 1 INCREMENTAL:                       $0 infra
   • mcp SDK (MIT): $0
   • cryptography (BSD): $0
   • watchfiles (MIT): $0
   • Docker daemon: $0
   • PostgreSQL secrets table: $0
─────────────────────────────────────────────────────────
TOTAL v1 (post-R4 B1):                         USD ~62-77/mes (sin cambio)

COMPRAS ÚNICAS B1 R4:
   USB hardware Master KEK backup: ~$10 (Brian custodia)

RECURSOS SERVIDOR R4 B1:
   • Docker daemon: ~500 MB RAM
   • 4 MCP containers shared (200 MB cap each): ~800 MB
   • Secrets crypto cache: <50 MB
   ─────────────────────────────────
   Base R4 B1: ~1.5 GB + scaling per workspace
   
   Per workspace:
   • Pilot Light: 512 MB
   • Pilot Pro: 2 GB

CAPACIDAD SERVIDOR BRIAN (30 GB RAM, 1 TB disco):
   ~40 workspaces Pilot Light simultáneos
   ~10 workspaces Pilot Pro simultáneos
   Suficiente v1 (3-5 pilots → 20-30 clientes)

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$55 (sin cambio)
   → 6.3% del techo
   → MARGEN 93.7% para R4 B2+B3 + R5-R10
```

#### Cobertura Grafo Maestro post-R4 B1

```
NODOS servidos:
   ✅ Nodo 4 Cuerpo Calloso (infraestructura completa)
   ✅ Nodo 3 PFC (orquesta tool calls + secrets)
   🟡 Nodo 2 Cerebelo (Skills auto v3 — foundation)
   🟡 Nodo 8 Tálamo (R5 routing — foundation)

PILARES post-R4 B1:
   ✅ Pilar 1 Seguridad:
      - Container per cliente (aislamiento físico)
      - Network per cliente (aislamiento red)
      - Secrets KEK hierarchy (defense in depth)
      - Audit per-secret-usage SOC2-defendible
      - Brian NUNCA ve plaintext secrets
   ✅ Pilar 2 Escalabilidad:
      - Docker containers compartidos
      - Resource quotas per tier
      - Hot-reload sin downtime
      - Capacidad ~40 Pilot Light / ~10 Pilot Pro
   ✅ Pilar 3 Autonomía:
      - MCP estándar extensibilidad
      - Discovery dinámico
      - Abstraction layer MCPClient

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → container per cliente + tier quotas
   2.B Open Core       → SDKs abiertos (mcp MIT + cryptography BSD + watchfiles MIT)
   3.D Equipo pequeño  → Docker compose simplicidad + hot-reload + scripts
```

#### Filosofía emergente del Bloque 1 R4

```
"Foundation aislada y defendible. Los 4 sub-temas convergen
en una arquitectura multi-tenant donde cada cliente tiene
container propio, secrets cifrados con KEK derivada, tools
compartidos stateless con audit per-uso, y hot-reload
event-driven sin downtime."

   • ESTÁNDAR INDUSTRY (4.1.1)
   • DISCOVERY SIN DOWNTIME (4.1.2)
   • AISLAMIENTO FÍSICO PER CLIENTE (4.1.3)
   • SECRETS DEFENSE IN DEPTH (4.1.4)
   • INTEGRACIÓN PROFUNDA CON R3
```

#### Foundation entregada a rondas futuras

```
R4 Bloque 2 (MCP Servers Core - siguiente):
   ✅ mcp SDK ready + Discovery + Hosting + Secrets injection
   → B2 solo decide qué tools concretas y cómo configurarlas

R4 Bloque 3 (Tool Lifecycle):
   ✅ Permission model + require_confirmation + Hot-reload + Resource quotas
   → B3 decide authorization workflows, versionado, testing

R5 Orchestration / Multi-Agent:
   ✅ Container workspace per cliente ready
   ✅ MCP tools shared stateless ready
   ✅ AgentDelegationTool foundation (B2 3.2.4)

R7 Frontend / Channel:
   ✅ for3s-api único entry point
   ✅ Dashboard cliente self-service ready
   ✅ Telegram MCP foundation

R8 Observability:
   ✅ Métricas per container Docker
   ✅ Audit trail completo R4

R9 Security/Compliance:
   ✅✅ 3-layer isolation defendible SOC2/ISO27001
   ✅✅ Secrets KEK hierarchy SOC2-defendible
   ✅ Compliance pitch B2B fuerte

R10 CI/CD/Deploy:
   ✅ Docker compose foundation
   ✅ Provisioning scripts foundation
   ✅ BYOC packaging trivial
   ✅ Path K8s migration via kompose (futuro v3)
```

#### Riesgos legítimos aceptados (11)

```
1. mcp SDK breaking changes v2.x
   Mitigación: pin >=1.0,<2.0 + abstraction layer

2. MCP server crash deja sesión zombie
   Mitigación: AsyncExitStack cleanup + health check + retry

3. Static config drift (config vs realidad)
   Mitigación: Pydantic validation + audit divergence

4. Workspace allowed_tools tool inexistente
   Mitigación: audit + Telegram alert si missing

5. Race conditions durante reload
   Mitigación: _refresh_lock + rollback automático

6. Config file mal formado por edición Brian
   Mitigación: validation antes apply + revert + audit

7. MCP push notifications spam
   Mitigación: rate limit 1 reload/server/10s + alarm

8. Container Docker crashea cliente
   Mitigación: Docker restart policy: always + health check + backup

9. Brian rompe arquitectura con setup error
   Mitigación: scripts idempotentes + test environment + Ansible (R10)

10. Master KEK loss
    Mitigación: backup #1 USB + #2 paper safe + #3 succession plan
    + setup ritual verificar antes producción
    + Telegram weekly "verify backup integrity"

11. Performance overhead decrypt per request
    Mitigación: workspace_kek_cache + AES-NI <2ms + Prometheus métrica
```

#### Protocolo Bidireccional aplicado (OPCIÓN 4 — mismo patrón R3)

Spillovers ejecutados FASE 1 (2026-06-06):

```
✅ for3s-inter/07-operations/decision-log.md + D-016
✅ Mente/Cuerpo/Ronda_04_Tools_MCP_Layer.md (master R4)
✅ Mente/Cuerpo/Ronda_04_Bloque_1_MCP_Framework_Discovery.md (detallado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.quaterdecies)

DIFERIDOS hasta cierre R4 completo (después B2+B3):
   ⏳ for3s-inter/09-technical-architecture/tools-mcp-layer.md
   ⏳ Actualización 09-technical-architecture/README.md (sección R4)
   ⏳ Actualización 02-product/mvp-scope.md (Tools stack annotation)
   ⏳ Actualización 05-finance/unit-economics.md (recursos servidor R4)
```

#### Próximo paso inmediato (post-B1)

**Arrancar R4 Bloque 2** → **EJECUTADO 2026-06-06**
Ver §3.1.quindecies para snapshot Bloque 2 R4 LOCKED.

---

### 3.1.quindecies — R4 BLOQUE 2 LOCKED (2026-06-06) — MCP SERVERS CORE

**R4 BLOQUE 2 — MCP SERVERS CORE CERRADO** (4/4 sub-temas LOCKED).

#### Pre-preguntas Bloque 2 LOCKED

```
B2-Q1: Confirma R4 B2 (no R2 B2) ✅
B2-Q2: Orden 4.2.1 → 4.2.4 (GitHub crítico primero) ✅
B2-Q3: Read+Write desde inicio (destructive con require_confirmation P3) ✅
```

#### Las 4 decisiones LOCKED del Bloque 2 R4 (D-017)

```
4.2.1 GitHub MCP                  ✅ LOCKED
      → A) MCP server oficial Anthropic
      → @modelcontextprotocol/server-github (>=0.6,<0.7 pinned SHA)
      → 26 tools (14 read + 9 write + 4 destructive)
      → PAT per workspace via SecretsManager (4.1.4)
      → Multi-repo via workspace.github_allowed_repos[]
      → Cache Valkey + Rate limit + Webhook async
      → Sensitive (4): merge_pr, update_pr_branch, create/delete_repo
      → Setup: 3-4 días
      → PRINCIPIO ARQUITECTÓNICO LOCKED PARTE 2 ESTABLECIDO AQUÍ:
        "Tools comunes y maduras → oficial (A)
         Tools niche/For3s-specific → custom Python (B)
         Hybrid (E) cuando oficial necesita extensión"

4.2.2 Filesystem MCP              ✅ LOCKED
      → B) Custom Python (FastMCP) con permission model nuestro
      → APLICACIÓN PRINCIPIO ARQUITECTÓNICO #1
      → for3s/mcp-filesystem:1.0.0
      → FastMCP + Pydantic v2 + aiofiles (BSD)
      → Path validation OBLIGATORIA: resolve() + relative_to()
      → 8 patterns blocked (.env, .git/, .ssh/, credentials, etc.)
      → Extensions whitelist per workspace
      → Max file size 10 MB, total quota 10/50 GB per tier
      → 12 tools (7 read + 4 write + 3 destructive)
      → Backup automático antes write/delete (trash 7 días)
      → Binary handling: base64 + mime detection
      → Setup: 4-5 días

4.2.3 HTTP MCP                    ✅ LOCKED
      → B) Custom Python (FastMCP) con SSRF 5-capa
      → APLICACIÓN PRINCIPIO ARQUITECTÓNICO #2
      → for3s/mcp-http:1.0.0
      → FastMCP + httpx (BSD) + trafilatura (Apache 2.0)
      → SSRF protection 5 CAPAS:
        1. URL validation (schema, format, length 2048)
        2. Domain policy (workspace allowlist + global blocklist)
        3. DNS + IP validation (10 networks blocked + DNS rebinding)
        4. Rate limit (Token Bucket per workspace+domain)
        5. Method + body validation
      → 10 networks blocked + cloud metadata blocklist
      → 6 tools (2 read + 3 write + 1 destructive)
      → Cache solo GET 200 con Cache-Control respect
      → HTML processing trafilatura
      → Auth injection per-request vía SecretsManager
      → OWASP LLM Top 10 compliance
      → Setup: 4-5 días

4.2.4 Telegram MCP                ✅ LOCKED (refinado con Hermes)
      → B) Custom Python (FastMCP + PTB) + 7 patrones Hermes
      → APLICACIÓN PRINCIPIO ARQUITECTÓNICO #3
      → for3s/mcp-telegram:1.0.0
      → FastMCP + python-telegram-bot 21.x (LGPLv3)
      → Reference: Mente/Cuerpo/Hermes_Arquitectura_Completa.md §11
      → 7 PATRONES HERMES REUSADOS:
        1. PlatformAdapter ABC (foundation R7 multi-canal)
        2. GatewayRunner FastAPI (webhook handler)
        3. NormalizedMessage abstracta (agente NO acoplado canal)
        4. Authorize pattern (workspace_user check)
        5. Session persistence (adapted Postgres)
        6. Cross-platform user linking (foundation v2)
        7. Config-driven enable
      → ADAPTACIONES FOR3S-SPECIFIC:
        • Multi-tenant: workspace_id en TODA operación
        • KEK encryption (bot_token + webhook_secret)
        • Role-based auth (member/admin/owner)
        • Inline keyboard P3 approval flow
        • Container Docker shared Capa 2
        • Audit chain inmutable
      → Bot strategy: 1 BOT PER WORKSPACE (no global)
      → Transport: WEBHOOK (Cloudflare Tunnel D-009)
      → 8 tools (5 outbound + 3 inbound)
      → Multi-user routing via workspace_telegram_users table
      → Approval token único 5 min expiry
      → Setup: 3-4 días (con Hermes ahorra 2)
```

#### Tools concretas habilitadas post-R4 B2 (~57 total)

```
GitHub MCP (oficial):       26 tools
Filesystem MCP (custom):    12 tools
HTTP MCP (custom):           6 tools
Telegram MCP (custom):       8 tools
+ Core LOCAL (B2 3.2.4):     5 tools (ya LOCKED R3)
─────────────────────────────────────
TOTAL DISPONIBLES:          ~57 tools
```

#### Principio Arquitectónico LOCKED VALIDADO 3 VECES

```
ÁRBOL DE DECISIÓN MCP SERVER:

¿Existe MCP server oficial Anthropic maduro?
├─ SÍ + cobertura suficiente → USAR OFICIAL (A)
│   Ejemplo validado: GitHub (4.2.1)
│
├─ SÍ + cobertura insuficiente → HÍBRIDO (E)
│
├─ NO + 3rd party community maduro → ADOPTAR con pin
│
└─ NO existe → CUSTOM PYTHON (B)
    Ejemplos validados:
    • Filesystem (4.2.2) — aislamiento multi-tenant
    • HTTP (4.2.3) — SSRF 5-capa
    • Telegram (4.2.4) — multi-user + no oficial

PROPORCIÓN: 1 oficial (25%) / 3 custom (75%)

TEMPLATE B (validado 3 veces):
   • FastMCP framework
   • Pydantic v2 schemas obligatorios
   • Audit logger (R2 B1)
   • Healthcheck (K8s-ready)
   • TOOL_TIMEOUT respect (R2 B3)
   • Multi-stage Dockerfile non-root
   • Tests pytest async
```

#### Estructura código extendida post-B2

```
containers/mcp-servers/
├── github/                          → Container oficial Anthropic
├── filesystem/                      → ⭐ Custom Python B2
│   ├── server.py, policy.py
│   └── tools/, tests/
├── http/                            → ⭐ Custom Python B2
│   ├── server.py, ssrf_validator.py, rate_limiter.py
│   └── tools/, tests/
└── telegram/                        → ⭐ Custom Python + Hermes B2
    ├── server.py
    ├── adapter/ (Hermes PlatformAdapter)
    ├── tools/, webhook/, worker/, tests/

config/mcp_servers.yaml              → 4 servers configured
```

#### Schema SQL extensiones B2

```sql
-- GitHub MCP
ALTER TABLE shared.workspaces ADD COLUMN
    github_allowed_repos TEXT[] NOT NULL DEFAULT '{}';
ALTER TABLE shared.workspaces ADD COLUMN github_user TEXT;
ALTER TABLE shared.workspaces ADD COLUMN github_pat_expires_at TIMESTAMPTZ;

-- Filesystem MCP
ALTER TABLE shared.workspaces ADD COLUMN filesystem_allowed_extensions TEXT[];
ALTER TABLE shared.workspaces ADD COLUMN filesystem_max_file_size_mb INTEGER DEFAULT 10;
ALTER TABLE shared.workspaces ADD COLUMN filesystem_total_quota_gb INTEGER DEFAULT 10;

-- HTTP MCP
ALTER TABLE shared.workspaces ADD COLUMN http_domain_allowlist TEXT[] DEFAULT NULL;
ALTER TABLE shared.workspaces ADD COLUMN http_auth_configs JSONB DEFAULT '{}';

-- Telegram MCP
ALTER TABLE shared.workspaces ADD COLUMN telegram_bot_username TEXT;
ALTER TABLE shared.workspaces ADD COLUMN telegram_webhook_configured_at TIMESTAMPTZ;
CREATE TABLE shared.workspace_telegram_users (...);
CREATE TABLE shared.telegram_approval_requests (...);
```

#### Patrones obligatorios añadidos R4 B2

```
✓ Principio Arquitectónico LOCKED (4.2.1 PARTE 2) aplicable a todos sub-temas R4+
✓ GitHub oficial via mcp SDK official
✓ Custom Python servers: template estándar FastMCP
✓ Path validation multi-capa filesystem
✓ SSRF 5-capa HTTP
✓ HMAC signature validation Telegram webhook
✓ PAT/bot_token/secrets KEK encryption (4.1.4 reused)
✓ Multi-user routing via mapping tables
✓ Approval flow Telegram inline keyboard (P3)
✓ Cache responses Valkey (per workspace key)
✓ Rate limit per workspace+resource (Token Bucket R3 B3)
✓ Audit per-tool-call obligatorio
✓ Métricas Prometheus específicas (~32 nuevas)
✓ Sensitive tools require_confirmation=True
✓ Backup automático destructive operations
✓ Hermes patterns reusados Telegram
✓ PlatformAdapter ABC = foundation R7 multi-canal
✓ NormalizedMessage abstracta = agente desacoplado canal
✓ Tests exhaustivos security (path traversal, SSRF, signature)
```

#### Costo total v1 actualizado (post-R4 B1+B2)

```
SUBTOTAL R1+R2+R3 100% + R4 B1:               ~$62-77/mes
R4 BLOQUE 2 INCREMENTAL:                       $0 infra
   • GitHub MCP (oficial MIT)
   • Filesystem MCP (custom FastMCP MIT)
   • HTTP MCP (custom + httpx BSD + trafilatura Apache)
   • Telegram MCP (custom + PTB LGPLv3)
─────────────────────────────────────────────────────────
TOTAL v1 (post-R4 B1+B2):                      ~$62-77/mes (sin cambio)

RECURSOS SERVIDOR R4 B2:
   • mcp-github:       200 MB RAM
   • mcp-filesystem:   200 MB RAM
   • mcp-http:         300 MB RAM
   • mcp-telegram:     250 MB RAM
   ──────────────────────────
   TOTAL B2:           ~950 MB RAM
   
ACUMULADO R4 v1 (B1+B2): ~2.5 GB RAM (de 30 GB disponibles)
Disponible: ~25 GB (83%) → ~40 Pilot Light o ~10 Pilot Pro

VERIFICACIÓN P2:
   Pilot Light $3,500 → 6.3% techo (margen 93.7%) — sin cambio
```

#### Cobertura Grafo Maestro post-R4 B2

```
NODOS:
   ✅ Nodo 4 Cuerpo Calloso (pleno: 4 MCP servers operativos)
   ✅ Nodo 6 Sistema Sensorial (Telegram canal bidireccional)
   ✅ Nodo 3 PFC (orquesta 57 tools concretas)
   🟡 Nodo 2 Cerebelo (Skills auto v3 — foundation tools registradas)
   🟡 Nodo 8 Tálamo (R5 tool selection v2)

PILARES post-R4 B2:
   ✅ Pilar 1 Seguridad:
      - SSRF 5-capa HTTP
      - Path traversal protection Filesystem
      - HMAC signature validation Telegram + GitHub webhook
      - PAT/bot_token KEK encryption
      - Permission model per tool
      - require_confirmation destructive
      - Audit chain inmutable per call
   ✅ Pilar 2 Escalabilidad:
      - Containers shared stateless
      - Cache responses Valkey
      - Rate limit per workspace+resource
      - Hot-reload sin downtime
      - Resource quotas per tier
   ✅ Pilar 3 Autonomía:
      - 57 tools disponibles agente
      - Discovery dinámico hot-reload
      - Permission boundaries claros
      - Approval flow human-in-loop (P3)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → per-workspace whitelist, quotas
   2.B Open Core       → SDKs abiertos (MIT/BSD/Apache/LGPLv3)
   3.D Equipo pequeño  → 4 containers + automation + Brian conoce stack
```

#### Filosofía emergente Bloque 2 R4

```
"Composición sobre reinvención. Tools donde comunidad MCP ya
hizo el trabajo (GitHub): usar oficial. Tools donde aislamiento
multi-tenant, security crítico, o lógica For3s-specific son
requirements (Filesystem, HTTP, Telegram): construir custom
Python con FastMCP y reusar learnings probados en producción
(Hermes patterns)."

PROPORCIÓN VALIDADA: 25% oficial / 75% custom
```

#### Foundation entregada a Bloque 3 y rondas futuras

```
R4 Bloque 3 (siguiente):
   ✅ 57 tools registradas
   ✅ Permission + require_confirmation flags
   ✅ Telegram inline keyboard ready para human-in-loop
   ✅ Pinned SHA images K8s-ready (versioning)
   
R5 Orchestration:
   ✅ MCP tools shared accesibles sub-agents
   ✅ Workspace isolation respetada
   ✅ Telegram canal bidireccional
   ✅ AgentDelegationTool foundation
   
R7 Frontend:
   ✅✅ PlatformAdapter ABC = Discord/Slack/WhatsApp v2 sin reescribir
   ✅ NormalizedMessage abstracta
   ✅ Approval flow P3 funcional
   
R8 Observability:
   ✅ ~32 métricas Prometheus nuevas B2
   ✅ Audit chain extendido per MCP
   
R9 Security/Compliance:
   ✅✅ OWASP LLM Top 10 compliance (HTTP)
   ✅ Path traversal protection (Filesystem)
   ✅ Signature validation (Telegram, GitHub webhook)
   ✅ Defense in depth multi-capa
   ✅ Foundation SOC2 audit path
   
R10 CI/CD:
   ✅ Docker images custom build pattern (3 containers)
   ✅ Pinned SHA images
   ✅ Health checks formales
```

#### Riesgos legítimos aceptados (12)

```
GitHub (3): abandonment Anthropic, PAT expire, scopes excesivos
Filesystem (3): path traversal bug, volume mount, quota exceed
HTTP (3): SSRF bypass, DNS rebinding, IPv6 evasion
Telegram (3): bot token leak, signature bypass, multi-user routing bug

Todos con mitigaciones específicas documentadas.
Top critical: path traversal (Filesystem) + SSRF bypass (HTTP) + Master KEK loss
```

#### Protocolo Bidireccional aplicado (OPCIÓN 4 — patrón validado R3+R4 B1)

Spillovers ejecutados FASE 1 (2026-06-06):

```
✅ for3s-inter/07-operations/decision-log.md + D-017
✅ Mente/Cuerpo/Ronda_04_Bloque_2_MCP_Servers_Core.md (detallado)
✅ Mente/Cuerpo/Ronda_04_Tools_MCP_Layer.md (master actualizado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.quindecies)

DIFERIDOS hasta cierre R4 completo (después B3):
   ⏳ for3s-inter/09-technical-architecture/tools-mcp-layer.md
   ⏳ Actualización 09-tech-arch/README.md (sección R4)
   ⏳ Actualización 02-product/mvp-scope.md
   ⏳ Actualización 05-finance/unit-economics.md
```

#### Próximo paso inmediato (post-B2)

**Arrancar R4 Bloque 3 — Tool Lifecycle** → **EJECUTADO 2026-06-06** ⭐ CIERRA R4 v1
Ver §3.1.sedecies para snapshot Bloque 3 + R4 v1 100% cerrado.

---

### 3.1.sedecies — R4 BLOQUE 3 LOCKED + R4 v1 100% CERRADO (2026-06-06) — TOOL LIFECYCLE

**R4 BLOQUE 3 — TOOL LIFECYCLE CERRADO** (3/3 sub-temas LOCKED).
**⭐ R4 v1 — TOOLS/MCP LAYER 100% CERRADO** (11/11 sub-temas operativos, B4 DIFERIDO v2).

#### Las 3 decisiones LOCKED del Bloque 3 R4 (D-018)

```
4.3.1 Authorization workflows         ✅ LOCKED
      → B) Workflow completo (7 capacidades coordinadas)
      → 7 CAPACIDADES:
        1. Approval policies declarativas (workspace.approval_policies JSONB)
        2. Dry-run preview cuando posible
        3. Role-based approver (owner/admin/member)
        4. Remember decision (max 30d, 50/workspace, NO destructive)
        5. Revocation window 5 segundos post-approval
        6. Break-glass urgent token (TTL 1h, single-use, audit fuerte)
        7. Dashboard + multi-channel (Telegram → email 120s escalation)
      → 4 DECISIONES per policy: auto_approve/auto_reject/require_approval/block
      → 3 DEFAULTS workspace onboarding LOCKED:
        • auto_approve_readonly (priority 100)
        • require_owner_for_destructive (priority 150)
        • default_require_approval (priority 1)
      → 4 TABLAS SQL nuevas
      → 7 MÉTRICAS PROMETHEUS nuevas
      → Foundation R9 SOC2 path

4.3.2 Versioning + rollback           ✅ LOCKED
      → A) SemVer + Docker SHA + workspace-level config
      → 3 PILARES:
        1. SemVer human-readable (MAJOR.MINOR.PATCH)
        2. Docker SHA pinned producción (inmutabilidad)
        3. Workspace-level config (workspace.mcp_server_versions JSONB)
      → 4 RELEASE CHANNELS: stable/beta/canary/exact SemVer
      → Multi-version containers concurrentes
      → Cleanup cron mensual: versions >90d sin uso removidas
      → Rollback strategy: manual v1, automatic v2, blue-green v3
      → Deprecation 3 fases: 30d soft + 15d hard + removal (TOOL_DEPRECATED ErrorType)
      → 3 TABLAS SQL nuevas
      → 5 MÉTRICAS PROMETHEUS nuevas

4.3.3 Testing & sandbox               ✅ LOCKED ⭐ CIERRA R4 v1
      → A) Framework completo (5 capas testing coordinadas)
      → 5 CAPAS:
        1. Unit tests (per tool isolated) — pytest async
        2. Integration tests (tool ↔ stack) — VCR.py recordings
        3. E2E tests (tool ↔ agent ↔ workflow) — sandbox real
        4. Sandbox environments — shadow services
        5. Golden dataset integration — B4 3.4.3 obligatoria
      → COVERAGE TARGETS: 85% custom, 70% wrappers, 100% security paths
      → MOCK STRATEGY 3 layers: Python / VCR.py / sandbox real
      → SHADOW SERVICES LOCKED:
        • GitHub org "for3s-sandbox" + sandbox bot token
        • Telegram bot "@For3sSandboxBot"
        • Filesystem /var/lib/for3s/sandbox/
        • HTTP httpbin.org + VCR fixtures
      → WORKSPACE SANDBOX TIER:
        • workspace.is_sandbox = true
        • Free, opt-in, max 1 per cliente
        • Limits estrictos: 5 RPM/5K TPM, 1 GB FS, $5/mes hard cap
        • Auto-cleanup >30 días sin uso
      → CI/CD FOUNDATION R10:
        • GitHub Actions PR + push main + cron weekly
        • Jobs: unit + integration + e2e_smoke + eval_golden + security_scan
        • Coverage fail-under 85%
        • Trivy + bandit
      → REGRESSION SCHEDULE:
        • Arq cron domingo 3 AM
        • Full golden dataset + 1% LLM-judge sample
        • Alert Brian Telegram si degradation >5%
      → EVAL B4 3.4.3 INTEGRATION OBLIGATORIA
      → 2 TABLAS SQL nuevas
      → 6 MÉTRICAS PROMETHEUS nuevas
```

#### Estructura código extendida post-B3

```
for3s_os/
├── tools/
│   ├── authorization.py            → 4.3.1 AuthorizationOrchestrator
│   ├── policy_engine.py            → 4.3.1 policy matching
│   ├── remember_engine.py          → 4.3.1 remember decisions
│   └── break_glass.py               → 4.3.1 urgent tokens
├── mcp/
│   ├── version_router.py            → 4.3.2 VersionRouter
│   └── deprecation_checker.py       → 4.3.2 Arq cron
└── ...

tests/                                → 4.3.3 (NEW)
├── unit/
│   ├── mcp/{filesystem,http,telegram}/
│   ├── secrets/
│   └── tools/
├── integration/
├── e2e/
│   ├── smoke/
│   └── workflows/
└── fixtures/
    ├── github_responses/             ← VCR.py recordings
    ├── synthetic_data/
    └── workspace_factories.py

scripts/
└── rollback_mcp.sh                   → 4.3.2 Brian CLI

.github/workflows/
└── test_mcp_servers.yml              → 4.3.3 CI/CD foundation R10
```

#### Patrones obligatorios añadidos R4 B3

```
✓ 7 capacidades authorization coordinadas
✓ Approval timeout 300s (P3 reused)
✓ Revocation window 5s post-approval
✓ Break-glass single-use TTL 1h + SECURITY_ALARM
✓ Remember max 30d TTL + NO destructive + 50/workspace
✓ Escalation Telegram → email después 120s
✓ Defaults secure-by-default workspace onboarding
✓ SemVer disciplina (MAJOR/MINOR/PATCH semantics)
✓ Docker SHA pinned producción (inmutabilidad)
✓ Workspace-level pinning per server JSONB
✓ Multi-version containers cleanup cron 90d
✓ Rollback CLI Brian + multi-version siempre 2-3 disponibles
✓ Deprecation 3 fases (30d soft + 15d hard + removal)
✓ TOOL_DEPRECATED ErrorType (R3 B3 3.3.3 reused)
✓ Coverage 85% custom / 70% wrappers / 100% security
✓ Mocks 3 layers (Python unit / VCR integration / sandbox E2E)
✓ Shadow services LOCKED
✓ Workspace sandbox tier free + limits estrictos
✓ CI GitHub Actions: PR + push + cron weekly
✓ Eval B4 3.4.3 integration blocking deploy
✓ Regression Arq cron domingo 3 AM
✓ Audit cada decision + version call + test run
```

#### Costo total v1 FINAL (R1+R2+R3 100%+R4 v1 100%)

```
SUBTOTAL R1+R2+R3 100%+R4 B1+B2:              ~$62-77/mes
R4 BLOQUE 3 INCREMENTAL:
   Authorization (todo en código):              $0
   Versioning (Docker SHA):                     $0
   Testing framework:                            $0
   Haiku regression weekly:                     +$2/mes
─────────────────────────────────────────────────────────
TOTAL v1 FINAL:                                 ~$64-79/mes

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$58
   → 6.6% del techo
   → MARGEN 93.4% para R5-R10

Verificación P5 cap LLM ($50-200/mes):
   Total LLM v1 FINAL: $63-73/mes
   → 32-37% del cap medio
   → Margen $127-137 escalado workspaces
```

#### Cobertura Grafo Maestro post-R4 v1 100%

```
NODOS servidos:
   ✅ Nodo 1 Hipocampo (R3 B2 context)
   ✅ Nodo 3 PFC (pleno orquesta 57 tools)
   ✅✅ Nodo 4 Cuerpo Calloso (PLENO R4 v1)
   ✅ Nodo 5 Memoria Largo (R3 B2 context)
   ✅ Nodo 6 Sistema Sensorial (Telegram bidireccional)
   ✅ Nodo 10 CLS (Haiku CLS + tmpl + eval + regression)
   🟡 Nodo 2 Cerebelo Skills auto (foundation R4 testing)
   🟡 Nodo 8 Tálamo (foundation R5)
   🟡 Nodo 9 Dual-Process Check (preparación R5)
   🟡 Nodo 11 Neuromoduladores (R3+R4 signals)

PILARES post-R4 v1 100%:
   ✅ Pilar 1 Seguridad COMPLETO:
      - SSRF 5-capa, path traversal, signature validation
      - Authorization 7 capacidades + audit inmutable
      - Versioning audit defendible SHA + SemVer
      - Tests security 100% paths críticos
      - Multi-tenant container + network isolation
      - Secrets KEK hierarchy
      - Break-glass audit fuerte SOC2-defendible
   
   ✅ Pilar 2 Escalabilidad COMPLETO:
      - Container shared stateless
      - Resource quotas per tier
      - Rate limit per workspace+resource
      - Hot-reload sin downtime
      - Multi-version concurrente
      - Testing automated escala con tools
      - Sandbox para learning sin afectar prod
   
   ✅ Pilar 3 Autonomía:
      - 57 tools agente disponibles
      - Discovery dinámico
      - Approval flow human-in-loop
      - Versioning per workspace (cliente self-service)
      - Testing automated permite iteración rápida
      - Sandbox experimentación
      - 🟡 Skills auto v3+ (Nodo 2 Cerebelo)

ANCLAS LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → per-workspace policies + versions + quotas + sandbox
   2.B Open Core       → SDKs abiertos completos (MIT/BSD/Apache/LGPLv3)
   3.D Equipo pequeño  → 4 containers + automation + Brian disciplina sin SRE
```

#### Filosofía emergente Bloque 3 R4

```
"Disciplina operacional como diferenciador comercial.
La diferencia entre 'wrapper de Claude bonito' y
'plataforma enterprise SOC2-defendible' está en cómo
se gobiernan, versionan y testean las tools. B3 es el
bloque que cierra ese gap."

PROPORCIÓN R4 v1 VALIDADA:
   • 25% oficial / 75% custom (Principio Arquitectónico)
   • Governance + Versioning + Testing = 3 pilares operacionales
   • Foundation R10 CI/CD natural extension
```

#### Foundation entregada a rondas futuras (R4 v1 100%)

```
R5 Orchestration / Multi-Agent (próxima):
   ✅ 57 tools registradas + governance + versioning + testing
   ✅ AgentDelegationTool foundation (B2 3.2.4)
   ✅ Container workspace per cliente
   ✅ Telegram canal bidireccional
   ✅ Approval flow para sub-agent actions
   ✅ Tool routing per workspace (foundation Tálamo)
   ✅ Versioning permite agentes diferentes per workspace

R6 Memory Stack extensions:
   ✅ Filesystem indexable como memoria
   ✅ Telegram conversations → memoria episódica
   ✅ Tools metrics → memoria semántica
   ✅ Versioning audit → memoria histórica

R7 Frontend / Channel:
   ✅✅ PlatformAdapter ABC (Hermes patterns multi-canal)
   ✅ Telegram primer canal validado
   ✅ Approval dashboard cliente
   ✅ Sandbox dashboard cliente
   ✅ Versioning dashboard (cliente self-service)
   ✅ Multi-canal v2 sin reescribir core

R8 Observability completa:
   ✅ ~60 métricas Prometheus nuevas R4
   ✅ Audit chain extendido completo
   ✅ Foundation Grafana dashboards
   ✅ Alerting rules específicas

R9 Security/Compliance:
   ✅✅ OWASP LLM Top 10 compliance
   ✅✅ Authorization governance defendible SOC2
   ✅ Audit inmutable versioning
   ✅ Penetration testing foundation (sandbox + property-based v2)
   ✅ Secrets KEK hierarchy
   ✅ Tools eval safety + golden datasets

R10 CI/CD / Deploy:
   ✅✅ Testing framework completo READY
   ✅✅ GitHub Actions foundation READY
   ✅✅ Docker SHA pinned READY
   ✅ Versioning + rollback strategy READY
   ✅ Sandbox environments pre-prod READY
   ✅ Compliance audit defendible READY
```

#### Riesgos legítimos aceptados (12 consolidados B3)

```
Authorization (4):
1. Policy mal escrita = security hole
   Mitigación: defaults LOCKED secure + validation Pydantic + audit changes
2. Remember decision abused
   Mitigación: max 30d TTL + NO destructive + max 50 + audit alerts
3. Break-glass token leak
   Mitigación: single-use + TTL 1h + SECURITY_ALARM
4. Revocation race condition
   Mitigación: 5s window + async tool execution + audit too_late

Versioning (4):
5. Multi-version containers consumen RAM
   Mitigación: cleanup cron 90d + resource limits + monitor
6. Breaking change MAJOR no documentado
   Mitigación: SemVer disciplina + breaking_changes JSONB + email
7. Rollback no funciona (target corrupted)
   Mitigación: verify pull + test staging + multi-version siempre 2-3
8. CI/CD missing v1 (Brian manual)
   Mitigación: CLI scripts robustos + R10 automatiza

Testing (4):
9. Tests flaky CI
   Mitigación: aislamiento fixtures + retry 3x + quarantine investigate
10. Mock fixtures desactualizados
    Mitigación: re-record mensual + schema validation + audit
11. Cliente confunde sandbox vs producción
    Mitigación: banner SANDBOX + email warning + bot username diferente
12. Coverage drops cuando agregan features
    Mitigación: fail-under 85% CI + code review obligatorio
```

#### Protocolo Bidireccional aplicado (OPCIÓN 1 — cierre formal completo)

Spillovers EJECUTADOS (2026-06-06):

```
Mente/ (privado):
✅ for3s-inter/07-operations/decision-log.md + D-018
✅ Mente/Cuerpo/Ronda_04_Bloque_3_Tool_Lifecycle.md (detallado)
✅ Mente/Cuerpo/Ronda_04_Tools_MCP_Layer.md (master 100% CERRADO)
✅ Mente/Doc/Estado_Sesion_Continuidad.md (este §3.1.sedecies)

for3s-inter/ (público formal):
✅ 09-technical-architecture/tools-mcp-layer.md (sub-doc consolidado)
✅ 09-technical-architecture/mcp-framework-discovery.md (R4 B1)
✅ 09-technical-architecture/mcp-servers-core.md (R4 B2)
✅ 09-technical-architecture/tool-lifecycle.md (R4 B3)
✅ 09-technical-architecture/README.md (R4 → ✅ v1 CERRADO 100%)
✅ 02-product/mvp-scope.md (Tools stack annotation FINAL)
✅ 05-finance/unit-economics.md (refresh costo total FINAL)
```

#### R4 v1 — STATUS FINAL

```
╔══════════════════════════════════════════════════════════════╗
║   ✅✅✅ R4 v1 — TOOLS/MCP LAYER 100% CERRADO ✅✅✅            ║
║                                                                ║
║   Bloque 1 ✅ LOCKED (4/4) — D-016                              ║
║   Bloque 2 ✅ LOCKED (4/4) — D-017                              ║
║   Bloque 3 ✅ LOCKED (3/3) — D-018 ⭐ CIERRA R4 v1               ║
║   Bloque 4 ⏳ DIFERIDO v2 (Multi-Domain Expansion)              ║
║                                                                  ║
║   TOTAL: 11/11 sub-temas LOCKED (100%)                          ║
║   Tiempo total: 2026-06-06 (1 día)                               ║
║                                                                  ║
║   COSTO v1 FINAL: ~$64-79/mes                                    ║
║   % techo Pilot Light: 6.6% (margen 93.4%)                       ║
║   57 tools concretas disponibles                                  ║
║   Compliance: OWASP LLM Top 10 + SOC2 path                       ║
╚══════════════════════════════════════════════════════════════╝
```

#### Próximo paso inmediato (post-R4 v1)

**Iniciar R5 — Orchestration / Multi-Agent**

R4 v1 entregó foundation:
- 57 tools registradas + governance + versioning + testing
- AgentDelegationTool foundation (B2 3.2.4)
- Container workspace per cliente (multi-tenant)
- Telegram canal bidireccional (PlatformAdapter ABC)
- Approval flow human-in-loop (P3)
- Tool routing per workspace (foundation Nodo 8 Tálamo)

R5 decisiones a tomar:
- Nodo 8 Tálamo router amplio (tool selection inteligente)
- Nodo 9 Dual-Process Check (Sistema 1 vs Sistema 2 Kahneman)
- Nodo 7 DMN idle compute (consolidación nocturna)
- Multi-Agent Network lifecycle
- Sub-agent containers (Capa 3 extensible)
- Agent-to-agent communication patterns
- Sub-agent permission inheritance

---

> ⚠️ **NOTA ARQUITECTÓNICA: Sub-tema 4.3 MOVIDO de R2 a R4 (2026-06-01)**
>
> Originalmente Bloque 4 tenía 4 sub-temas (4.1-4.4). Durante el debate de 4.3 (Code repo access), Brian identificó correctamente que era una decisión específica al **wedge QA** (GitHub/GitLab para análisis de PRs), NO una decisión genérica de **For3s OS plataforma**.
>
> Decisión LOCKED: **Sub-tema 4.3 se MUEVE a R4 (Tools/MCP Layer)** donde corresponde arquitectónicamente.
>
> Razones:
> - For3s OS es plataforma reusable; integraciones específicas viven en R4
> - MCP (Model Context Protocol) ES el estándar Anthropic para tools
> - Git, Slack, Notion, Jira, etc. serán MCP servers — no decisiones core del Data Layer
> - Hermes-style: providers pluggables, no hardcoded en core
>
> Impacto:
> - Bloque 4 ahora tiene **3 sub-temas** (4.1, 4.2, 4.4)
> - R2 total: **20 sub-temas** (era 21)
> - R4 (Tools/MCP) decidirá: GitHub MCP server, GitLab MCP server, etc.
>
> Cifras de progreso "21 sub-temas" en docs anteriores son **históricas**; las nuevas son **20 sub-temas**.

> ⚠️ **NOTA TRANSVERSAL: Costos en §3.1.quinquies, .sexies, .septies sobrescritos por D-009 (§3.1.octies)**
>
> Los snapshots de §3.1.quinquies, .sexies y .septies mencionan "Hetzner CX42 ~USD 25/mes" y "TOTAL USD ~63/mes" reflejando la decisión LOCKED EN ESE MOMENTO. Sin embargo, **D-009 (§3.1.octies)** lockeó posteriormente el despliegue LOCAL en hardware de Brian, lo que hace que el costo real v1 sea **USD ~43/mes (no USD ~63/mes)**.
>
> Las cifras "USD ~63" son históricas (audit trail). El costo vigente real es **USD ~43/mes**.
>
> Stack técnico (B1+B2+B3 completo) NO cambia. Solo el host físico de despliegue.

### 3.1.quinquies — RONDA 2 BLOQUE 1 LOCKED (2026-06-01) — Storage Foundation

**Ronda 2 — Data Layer arrancó con 5 preguntas contextuales y luego abrió el Bloque 1 — Storage Foundation.**

#### Pre-rondas: 5 preguntas contextuales resueltas

```
P1 — Volumen v1                       ✅ LOCKED
      ~50-200 PRs, ~100-500 episodios,
      ~20-50 skills, ~10-30 outputs por workspace.
      → Vector store y BD a escala chica v1.

P2 — AI+infra <25% del pilot revenue  ✅ LOCKED (regla dura)
      → Descarta automáticamente Pinecone/managed caros.

P3 — Workspace isolation              ✅ LOCKED
      → (b) Schema-per-tenant v1.
      → Migración futura a (c) Database-per-tenant
        cuando llegue cliente enterprise.

P4 — Encryption at rest               ✅ LOCKED
      → (c) Híbrido: app-layer AES-GCM + filesystem LUKS.
      → Defense in depth. Cumple mvp-scope §9.1.

P5 — Event Sourcing                   ✅ LOCKED
      → (3) Híbrido:
         ES en Hipocampo, Skills, Audit chain.
         CRUD en Workspaces, Users, RBAC, KG state, etc.
```

#### Bloque 1 — Storage Foundation: 6/6 sub-temas LOCKED

```
1.1 BD relacional principal             ✅ LOCKED
      → PostgreSQL 16+ (self-hosted Hetzner CX32 ~USD 13/mes)
      → Razón: único que hostea AGE + pgvector + RLS + schemas.

1.2 Knowledge Graph                     ✅ LOCKED
      → Apache AGE (v1) → Neo4j (v3 si escala)
      → Razón: 0 servicios extra, Apache 2.0,
        joins nativos KG↔SQL en una sola transacción.

1.3 Vector store                        ✅ LOCKED
      → pgvector + HNSW (v1) → Qdrant (v3 si escala)
      → Razón: 0 servicios extra, joins nativos
        vector↔KG↔SQL, coherencia con 1.2.

1.4 ORM                                 ✅ LOCKED
      → SQLAlchemy 2 + Pydantic v2 (separados)
      → Razón: estándar Python 19 años, soporte oficial
        pgvector, listeners para hooks ES, multi-schema.

1.5 Migraciones                         ✅ LOCKED
      → Single Alembic, multi-schema iteration
      → Razón: una fuente de verdad, autogenerate con
        SQLAlchemy 2, env.py custom itera schemas.

1.6 Event Sourcing tablas               ✅ LOCKED
      → Diseño por aggregate (no tabla única)
      → Tablas: episodes_events, skills_events, audit_events
        + episodes_state, skills_state (projections)
      → Payload JSONB + columnas BYTEA cifradas (P4)
      → UUID v7 + sequence_number por aggregate
      → Hash chain SOLO en audit_events
      → Inmutabilidad por trigger Postgres + grants restringidos
      → SIN snapshots v1 (refactor a v2 si replay >100ms)
      → SIN particionado v1 (schemas P3 ya particionan)
```

#### Stack final del Data Layer v1

```
┌──────────────────────────────────────────────────────┐
│   PostgreSQL 16+ (single instance, Hetzner CX32)      │
│   ~USD 13/mes — cabe en P2 <25% holgado               │
│                                                        │
│   EXTENSIONES:                                         │
│     ✓ AGE (Apache 2.0)        → Nodo 1 KG con Cypher  │
│     ✓ pgvector + HNSW (BSD)   → Nodo 2 Hipocampo      │
│     ✓ pgcrypto                → P4 encryption          │
│                                                        │
│   SCHEMA: shared                                       │
│     • workspaces, users, api_keys, RBAC (CRUD)         │
│     • audit_events (ES + hash chain)                   │
│     • AGE graph: conceptos globales                    │
│                                                        │
│   SCHEMA: wks_X (uno por cliente)                      │
│     • episodes_events + episodes_state (ES + CRUD)     │
│     • skills_events + skills_state (ES + CRUD)         │
│     • pgvector embeddings (HNSW index)                 │
│     • AGE subgraph: KG por workspace                   │
│     • outputs, configs (CRUD)                          │
│                                                        │
│   CAPA Python:                                         │
│     • SQLAlchemy 2 + asyncpg                           │
│     • Pydantic v2 para API                             │
│     • Alembic con env.py custom multi-schema           │
└──────────────────────────────────────────────────────┘
```

#### Cobertura del Grafo Maestro

```
Nodos servidos por Bloque 1:
   ✅ Nodo 1 KG (Apache AGE)
   ✅ Nodo 2 Hipocampo (pgvector + ES tables)
   ✅ Nodo 4 Skills (skills_events ES)
   ✅ Nodo 5 Ganglios Basales (skills_state CRUD)
   ✅ Nodo 9 Pattern Separation (HNSW index)
   ✅ Pilar 1 Seguridad (workspace iso + audit + encryption)
   🟡 Pilar 2 Escalabilidad (foundation OK, pool/cache R3)
   ⏳ Nodo 6 Microglía (Bloque 2 sub-tema 2.5)
   ⏳ Nodo 10 CLS (Bloque 2 sub-tema 2.6)
   ⏳ Nodo 3 PFC, Nodo 7 DMN, Nodo 8 Amígdala, Nodo 11 (R5+)

Anclas LOCKED respetadas: 3/3 ✅
   • 1.D Dedicated SaaS  ✓
   • 2.B Open Core       ✓ (todas licencias permisivas)
   • 3.D Equipo pequeño  ✓ (0 servicios extra)
```

#### Evaluación honesta de Bloque 1 (2026-06-01)

Brian pidió evaluación brutal. Score promedio: **8.9/10**.

```
Fortalezas:
   • Coherencia arquitectónica 9.5/10
   • Cost vs P2 10/10 (holgado)
   • Open Core compliance 10/10
   • Performance v1 a escala 10/10
   • Migración futura planeada 8.5/10

Riesgos legítimos aceptados conscientemente (5):
   1. Apache AGE es joven (5 años vs Neo4j 18) — mitigar con
      migración planeada v3.
   2. Postgres como SPOF/bottleneck único — mitigar con
      connection pooling (3.3) + DB-per-tenant (P3 v2).
   3. ES Híbrido deuda cognitiva — documentar decision flowchart
      ES vs CRUD para devs futuros.
   4. HNSW RAM-hungry — monitor desde día 1, scale-up
      CX32→CX52→CCX22 cuando RAM se aprieta.
   5. Memory framework aún no cerrado — lo resuelve Bloque 2
      sub-tema 2.1.

Comparación con Hermes:
   For3s es MÁS sofisticado donde TIENE que serlo
   (multi-tenant, compliance B2B, audit forensic).
   For3s es MENOS modular en provider de vector que Hermes;
   mitigable con abstracción en Bloque 2.1.

Veredicto: Avanzar a Bloque 2 con conciencia de los 5 riesgos.
   NINGUNO es bloqueante. TODOS son conocidos y planeables.
```

#### Protocolo Bidireccional aplicado

Spillovers identificados hacia `for3s-inter/` y decisión de Brian:

```
S5 — decision-log.md D-005 + D-006        ✅ ESCRITO 2026-06-01
S4 — 09-technical-architecture/ + README  ✅ CREADO 2026-06-01
S1 — 03-security/encryption-strategy.md   ⏳ DIFERIDO hasta cierre R2
S2 — 03-security/data-handling-policy.md  ⏳ DIFERIDO hasta cierre R2
S3 — 03-security/access-control-model.md  ⏳ DIFERIDO hasta cierre R2
S6 — 05-finance/unit-economics.md         ⏳ DIFERIDO hasta cierre R2
S7-S9 — backup, observability, DR         ⏳ DIFERIDOS a Bloque 4 / R8
```

#### Documentos formales generados (2026-06-01)

```
✅ Mente/Cuerpo/Ronda_02_Data_Layer.md
   → Master de R2 con resumen ejecutivo + nav a sub-documentos.
   → Incluye 5 preguntas contextuales LOCKED + status bloques 2-4.
   → Apéndice §10: Schema SQL consolidado completo (B1+B2).

✅ Mente/Cuerpo/Ronda_02_Bloque_1_Storage_Foundation.md
   → Sub-documento detallado de Bloque 1.
   → 15 secciones, 6 sub-temas con candidatos, tablas comparativas,
     razones LOCKED, esquemas SQL concretos, riesgos legítimos.

✅ Mente/Cuerpo/Ronda_02_Bloque_2_Memory_Architecture.md
   → Sub-documento detallado de Bloque 2.
   → 16 secciones, 7 sub-temas con debate completo.
   → Incluye exploraciones futuras documentadas.

✅ Mente/Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md  ⭐ CANÓNICO
   → DOCUMENTO MAESTRO del bridge filosofía ↔ código.
   → 21 secciones, 11 nodos con detalle exhaustivo.
   → Tabla maestra 11×8, diagrama visual, diccionario bilingüe.
   → Flujos cross-nodo, excepciones inmutables, protocolo de actualización.
   → Lectura OBLIGATORIA para devs antes de tocar memory/.

✅ for3s-inter/09-technical-architecture/compute-runtime.md
   → Contraparte público-formal de R1.

✅ for3s-inter/09-technical-architecture/storage-foundation.md
   → Contraparte público-formal de R2 Bloque 1.

✅ for3s-inter/09-technical-architecture/memory-architecture.md
   → Contraparte público-formal de R2 Bloque 2.

Patrón para bloques futuros (B+A):
   • Master Ronda_02_Data_Layer.md se actualiza al cerrar cada bloque
   • Cada bloque tiene su sub-documento detallado
     - Ronda_02_Bloque_2_Memory_Architecture.md (al cerrar B2)
     - Ronda_02_Bloque_3_Performance_Async.md (al cerrar B3)
     - Ronda_02_Bloque_4_Files_External.md (al cerrar B4)
```

#### Próximo paso inmediato

**Arrancar R2 Bloque 2 — Memory Architecture** con 7 sub-temas:

```
2.1 Memory framework (Honcho vs Mem0 vs Zep vs custom vs hybrid)
2.2 Embeddings (modelo + dimensiones)
2.3 Vector indexing (HNSW vs IVF vs flat) — parcialmente decidido
2.4 Memory tiers (working/short/long-term)
2.5 Forgetting strategy (Microglía)
2.6 CLS consolidation job (sleep cycle)
2.7 Mapeo Nodo Cerebral ↔ Tabla SQL (bridge filosofía/código)
```

Tensión esperada en 2.1 (memory framework). Modo de trabajo confirmado: **B+A** (bloques + sub-temas explícitos uno por uno).

---

### 3.1.quater — PROTOCOLO BIDIRECCIONAL Mente/ ↔ for3s-inter/ (LOCKED 2026-05-30)

**Marco mental confirmado por Brian:**

```
   For3s OS (la plataforma técnica grande)  →  vive en Mente/
       │
       └── For3s QA (primer nicho comercial)  →  vive en for3s-inter/

   NO son productos separados.
   For3s OS hace funcionar For3s QA.
   Más adelante se fusionan formalmente.
```

**Estado del árbol (auditoría 2026-05-30):**

- `Mente/` (For3s OS): **94% completo** para R2 (Grafo Maestro define todos los nodos)
- `for3s-inter/` (For3s QA): **40% completo** (foundation + product + commercial sólidos, técnico/financiero/legal vacíos)
- `for3s-inter/09-technical-architecture/`: **carpeta NO EXISTE** (planeada en README pero no creada)

**Decisión LOCKED de Brian (2026-05-30):**

> "Con forme vayamos avanzando en el R2 podemos ir rellenando y actualizando cosas de for3s-inter, en especial las cosas que teníamos pendientes. Ya que ahorita actualizaríamos de la versión For3s OS, falta el lado For3s QA. Podríamos avanzar y dejar pendiente y más adelante fusionarlo y que sea uno mismo."

**Protocolo operativo de las 10 rondas técnicas:**

```
   Durante CADA ronda (R2 a R10):

   PASO 1 — Debate y decisión técnica en Mente/Cuerpo/
   ─────────────────────────────────────────────────
   • Debatimos opciones (modo A o B según ronda)
   • Decisión LOCKED por Brian
   • Generamos Ronda_NN_*.md en Mente/Cuerpo/

   PASO 2 — Identificar SPILLOVER hacia for3s-inter/
   ─────────────────────────────────────────────────
   Al cerrar cada ronda, identifico qué docs de
   for3s-inter/ pueden ahora rellenarse o actualizarse
   con la decisión técnica recién tomada.

   PASO 3 — Brian decide spillover por item
   ─────────────────────────────────────────────────
   Para CADA doc activado, Brian decide:
   • (a) Escribirlo ahora antes de la siguiente ronda
   • (b) Backlog, pasar a la siguiente ronda
   • (c) Dejar para después de las 10 rondas
   (No se asume — siempre se pregunta.)

   PASO 4 — Loguear pendientes en este documento
   ─────────────────────────────────────────────────
   Items que quedan en backlog se anotan en §3.X
   "Backlog spillover For3s QA" para que cualquier
   Claude futuro pueda retomar.
```

**Regla de oro del protocolo:**

> NO escribimos en for3s-inter/ lo que NO está LOCKED técnicamente en Mente/.
> Esto evita escribir vapor (promesas comerciales sin sustento técnico real).

**Carpeta `for3s-inter/09-technical-architecture/`:**

Cuando cerremos R2, crearemos esta carpeta + un README.md ahí que apunte (no duplique) a `Mente/Cuerpo/Ronda_*.md`. **Esto es el primer puente formal entre For3s OS y For3s QA.**

### 3.1.ter — REGLA OPERATIVA LOCKED (aplicar en TODAS las rondas)

Brian estableció durante R1:

> "El expertise se contrata. La tecnología se elige por criterio técnico, no por preferencia del founder. La fuente de verdad es For3s_OS_Grafo_Maestro.md."

**Implicación para próximas rondas:**

```
   En cada ronda técnica:

   1. La pregunta es siempre:
      "¿Qué tecnología construye MEJOR el Grafo Maestro?"

   2. NO se pondera:
      ✗ "¿Qué sabe Brian?"
      ✗ "¿Qué prefiere el founder?"
      ✗ "¿Qué es más rápido de aprender?"
      ✗ "¿Qué evita contratar?"

   3. SI hay gap de expertise: identificar el rol específico
      a contratar (no cambiar la tecnología por evitar contratar).
```

**Próximo paso esperado:** arrancar **Ronda 2 — Data Layer** en modo B (alta tensión, debate exhaustivo). Brian indicará cuándo arrancar.

### 3.2 Decisiones técnicas pendientes (actualizado 2026-06-01)

**Estado actual:** De las 5 tensiones originales del filtro, **4 están RESUELTAS** vía Rondas 1 + 2 (Bloques 1+2). Solo 1 queda parcialmente abierta.

```
   1. MONOLÍTICA vs MICROSERVICIOS                    ✅ RESUELTA
      Decisión: Monolito modular Python en uv workspaces (R1)
      Evolución a microservicios POSIBLE en v3+ si necesario.
      Fuente: Ronda_01_Compute_Lenguaje.md

   2. STACK TYPESCRIPT vs PYTHON                       ✅ RESUELTA
      Decisión: Python 3.12+ LOCKED en R1 (2026-05-30)
      Comparación: Python 41 vs TS 35-41 vs Rust 38 vs Go 37
      Fuente: Ronda_01_Compute_Lenguaje.md + D-006

   3. OPENCLAW vs CONSTRUIR DESDE CERO                 ✅ RESUELTA
      Decisión: For3s OS construido independiente
      OpenClaw queda como producto separado de Brian
      Stack For3s OS no comparte código con OpenClaw

   4. MEMORIA DE AGENTES (stack en capas)              ✅ RESUELTA
      Decisión LOCKED en R2 Bloques 1+2 (2026-06-01):
        • BD relacional: PostgreSQL 16+ (B1 1.1)
        • KG: Apache AGE → Neo4j v3 (B1 1.2)
        • Vector: pgvector + HNSW → Qdrant v3 (B1 1.3)
        • Memory framework: Custom + composables (B2 2.1)
        • Embeddings: Stella local + OpenAI fallback (B2 2.2)
        • Memory tiers: 3 tiers clásico (B2 2.4)
        • Forgetting: Soft+Decay+Archive (B2 2.5)
        • CLS: Híbrido HDBSCAN + Haiku 4.5 (B2 2.6)
      Fuente: Ronda_02_Bloque_1_Storage_Foundation.md
               + Ronda_02_Bloque_2_Memory_Architecture.md
               + D-006 + D-007

   5. DEDICATED SAAS vs HARDWARE EXISTENTE              🟡 PARCIAL
      Decisión LOCKED hardware: Hetzner CX42 self-hosted (~$25/mes)
      Bloque 1 + B2 sub-tema 2.2 (upgrade CX32 → CX42)
      PENDIENTE: estrategia de despliegue cuando >5 clientes:
        • Migrar a managed Postgres (Supabase/Railway)?
        • Mantener self-hosted con upgrade CCX22?
        • Cliente enterprise → DB-per-tenant (P3 v2)?
      Esta decisión queda para R10 (CI/CD / Deploy) o cuando
      llegue el primer cliente que la fuerce.
```

**Tensiones nuevas surgidas durante R2 (todas LOCKED en sub-temas):**

```
   P1 — Volumen estimado v1                            ✅ LOCKED (R2 pre)
   P2 — AI+infra <25% pilot revenue                    ✅ LOCKED (R2 pre)
   P3 — Workspace isolation (schema-per-tenant)        ✅ LOCKED (R2 pre)
   P4 — Encryption at rest (híbrido)                   ✅ LOCKED (R2 pre + D-005)
   P5 — Event Sourcing (híbrido por aggregate)         ✅ LOCKED (R2 pre + B1 1.6)
```

### 3.3 Las 3 preguntas del README §7 pendientes

```
   Pregunta 1: ¿La interpretación de las 3 capas
              (Alma/Cerebro/Cuerpo) coincide con tu intención?
              Específicamente ¿"Alma" = por qué/valores, o algo distinto?

   Pregunta 2: ¿Esto es para Brian (sistema personal de pensamiento),
              para For3s (sistema de la empresa), o para ambos?

   Pregunta 3: ¿Mente/ reemplaza, complementa o convive con
              for3s-inter/ y marca-personal/?
              (El README §2 propone "convive y precede")
```

Brian aún NO ha respondido estas 3 preguntas. No bloquean trabajo pero conviene cerrarlas pronto.

### 3.4 Items abiertos del post-pivot-roadmap (for3s-inter)

**Phase 1 — Complete Company OS (1-2 weeks):** parcial
- ✅ Foundation docs v0.2.0
- ✅ Pivot brief 2026-05-18
- ❌ client-archetypes.md
- ❌ ideal-customer-profile.md (parcial)
- ❌ first-paid-pilot-offer.md
- ❌ mvp-scope.md (parcial)

**Phase 2 — Customer Discovery (4-6 semanas):** NO iniciada
- ❌ Lista de 30-50 prospects LATAM
- ❌ 10 discovery conversations
- ❌ Documentación de buyer urgency/pricing/security objections

**Phase 3 — First Paid Pilots:** NO iniciada
**Phase 4 — Site Relaunch:** NO iniciada (depende de Fase 3)

---

## 4. REGLAS DE CONVERSACIÓN CON BRIAN

Estas son las reglas de juego que Brian estableció explícitamente. **Respétalas como código.**

### 4.1 Reglas explícitas que Brian estableció

```
   ✓ "Si no te pregunto por algo es porque no lo sé y quiero saberlo"
     → No diluyas información. Si veo algo importante que no me preguntó,
       lo traigo. Esta es la regla más fuerte.

   ✓ "Vamos a fondo. No me des versiones suavizadas"
     → No marketing. No floreos. Honestidad técnica brutal.

   ✓ "Documenta TODO sin perder nada"
     → Capturar es preservar valor. Mejor verboso que perder contexto.

   ✓ "Hoy no desarrollamos, solo analizamos y discutimos"
     → En ciertos chats Brian quiere análisis puro, no implementación.
       Pregunta antes de asumir.

   ✓ "No intuyas. Si no sabes, lee primero"
     → Antes de responder con asunciones, leer archivos relevantes.
       Verificar contra Grafo Maestro siempre.
```

### 4.2 Anti-patrones que Brian rechazó

```
   ✗ Marketing language ("revolutionary", "leverage", "empower")
   ✗ Conclusiones prematuras antes de tener todos los inputs
   ✗ Asumir que los borradores históricos son "fuente de verdad"
   ✗ Ofrecer servicios/funciones que no se aplican (TodoWrite, ScheduleWakeup,
     deep-research como tooling) — solo usar cuando pide
   ✗ Respuestas largas cuando una corta basta (excepto análisis profundos)
```

### 4.3 Formato preferido por Brian

- Español primario, inglés ocasional
- Tablas comparativas cuando hay >3 opciones
- Diagramas ASCII para arquitectura
- Listas numeradas para decisiones
- Bold para énfasis estratégico
- Honestidad explícita sobre lo que NO sabemos

### 4.4 Estructura de carpetas (`Mente/`)

Definida en el README. Cada capa tiene su rol:
- **Alma/** = por qué, valores, dirección de fondo (lo no negociable)
- **Cerebro/** = marcos teóricos, modelos mentales, análisis
- **Cuerpo/** = implementación ejecutable, código, planes técnicos
- **Doc/** = transversal (cruza Alma+Cerebro+Cuerpo)

Si dudas dónde guardar algo, usa el árbol de decisión del README §4 "Protocolo ¿Dónde guardo esto?"

---

## 5. CRONOLOGÍA DE TRABAJO (sesiones registradas)

Para entender la evolución del pensamiento de Brian:

```
   2026-05-15  → Borrador FOR3S-STACK-DEFINED.md (mayo histórico)
   2026-05-17  → Foundation docs v0.2.0 publicados en for3s-inter
   2026-05-18  → PIVOTE: For3s general → For3s QA wedge
                 7 decisiones lockeadas
                 Founder identity corregida (Brian López)
                 FOR3S-RECURSOS-ACTUALES.md generado
   2026-05-28  → Sesión profunda Mente/ comienza
                 Vision_For3s_Frontier.md
                 Primeros_Pasos.md
                 Cerebro_Humano_acercamiento1.md + acercamiento2.md
                 Arquitectura_Grafo_vs_Loop.md
                 For3s_OS_Grafo_Maestro.md ⭐ pieza maestra
   2026-05-30  → Hermes_Arquitectura_Completa.md (Mente/Cuerpo/)
                 Captura de 11 lotes de infografías
                 Banco_Infografias_Completo.md
                 Banco_Diario_Mayo_2026.md
                 Banco_Filtro_Alineacion.md
                 Estadística honesta de avance
                 Este documento (Estado_Sesion_Continuidad.md)
```

---

## 6. CONCEPTOS QUE BRIAN USA Y SU SIGNIFICADO

Glosario rápido de términos que aparecen repetidamente y necesitan interpretación correcta:

| Término | Significado |
|---|---|
| **For3s** | La empresa |
| **For3s OS** | La plataforma agentic cerebral completa (visión) |
| **For3s QA** | Primer producto/wedge — agente de QA enterprise |
| **Agentic AI** | Categoría: equipo de AI workers coordinados (NO LLM solo, NO RAG solo, NO AI Agent solo) |
| **Grafo Maestro** | El documento For3s_OS_Grafo_Maestro.md — la verdad arquitectónica |
| **11 nodos cerebrales** | Las piezas funcionales del Grafo Maestro |
| **3 pilares** | Seguridad E2E + Escalabilidad por nodo + Autonomía Generativa |
| **MCP** | Model Context Protocol — "USB-C de los agentes" (Brian considera pieza fundacional) |
| **Workspace** | Aislamiento criptográfico por cliente |
| **Skills procedurales** | Memoria procedural (Ganglios Basales artificiales) |
| **Inmortalidad** | Concepto propio de Brian — export/import portable de agentes |
| **Herencia** | Concepto propio de Brian — templates de agentes base+override |
| **Fruterito Personal/Empleado/Design** | Sus 3 agentes operativos personales con OpenClaw |
| **OpenClaw** | Motor de agentes que Brian construyó previamente |
| **for3s-server** | Su hardware físico (32GB RAM, 1TB NVMe, IP Tailscale 100.112.177.53) |
| **WSL2 BrayanETH** | Su máquina de desarrollo (IP Tailscale 100.88.66.23) |
| **Pivote** | El cambio del 2026-05-18 de "LATAM-first agent infra" → "QA wedge" |
| **El moat** | Flywheel B2B: Distribución + Data + Modelos + Outcomes |
| **El banco** | Las 81+ infografías + 3 docs diarios |

---

## 7. SEÑALES DE ALARMA (cuándo parar y preguntar)

Como agente que retoma conversación, **NUNCA hagas estas cosas sin preguntar primero a Brian**:

1. **Implementar código** sin confirmación explícita ("¿procedo a escribir código?")
2. **Modificar `for3s-inter/`** — son decisiones LOCKED de empresa
3. **Hacer commits a git** sin pedirlo
4. **Mover archivos** entre `Alma/`, `Cerebro/`, `Cuerpo/`, `Doc/` sin justificarlo
5. **Cerrar decisiones técnicas** sin que Brian las apruebe explícitamente
6. **Asumir respuesta a las 3 preguntas pendientes** del README §7
7. **Asumir A/B/C** sobre las próximas semanas (Brian no ha respondido)
8. **Tratar el diario de mayo 2026 como fuente de verdad** — NO LO ES (es histórico)
9. **Inventar consulting con clientes** que no han pasado — 0 pilots aún
10. **Saltarse `for3s-inter/security-principles.md`** — define qué es no-negociable

Si dudas, **pregunta**. Brian prefiere una pausa breve a un avance incorrecto.

---

## 8. PRÓXIMO PASO INMEDIATO (lo que sigue cuando Brian retome)

**Probabilidad alta** (lo más probable que pase):

1. Brian lee este documento + lee el README actualizado
2. Aprueba el formato o pide ajustes
3. **Responde la opción A/B/C** sobre próximas 30 días
4. Empezamos según su elección:
   - Si A → Rondas comprimidas (3 rondas concentradas)
   - Si B → Rondas completas (10 rondas)
   - Si C → Build first (saltarse rondas, decisiones rápidas, código)

**Probabilidad media:**
- Brian pide más estadística o profundización en algún aspecto
- Brian decide responder las 3 preguntas pendientes del README §7
- Brian decide arrancar el inventario de las 23 skills de Fruterito Empleado

**Probabilidad baja pero posible:**
- Brian pide replantear el Grafo Maestro
- Brian pide cambiar las 3 anclas estratégicas
- Brian aborta el plan actual y pivota

---

## 9. CHECKLIST DE RETOMADA (uso de Claude/agente)

Cuando un Claude nuevo (o el mismo Claude tras compactación) retoma la conversación:

```
   [ ] LEÍ Estado_Sesion_Continuidad.md (este documento) completo
   [ ] LEÍ Mente/memory/archive/README.md (índice maestro)
   [ ] LEÍ For3s_OS_Grafo_Maestro.md (la verdad arquitectónica)
   [ ] LEÍ Vision_For3s_Frontier.md (el por qué)
   [ ] LEÍ Banco_Filtro_Alineacion.md (KEEP/DROP de tecnologías)
   [ ] CONFIRMÉ con Brian dónde quedamos antes de proponer algo nuevo
   [ ] RESPETO las reglas de conversación del §4
   [ ] NO ASUMÍ decisiones que Brian no ha aprobado
   [ ] TRATÉ el diario de mayo 2026 como histórico, NO fuente de verdad
   [ ] APLIQUÉ el filtro del Grafo Maestro a propuestas nuevas
```

Si todo check, puedes continuar la conversación con Brian sin perder contexto.

---

## 10. ACTUALIZACIÓN DE ESTE DOCUMENTO

Este documento se actualiza al **final de cada sesión importante**. La regla:

**Si la sesión introduce algo de lo siguiente, actualizar este doc:**

- Una decisión técnica LOCKED nueva
- Una respuesta a las 3 preguntas pendientes
- Un cambio en las anclas estratégicas
- Un avance medible en el % de producto
- Una nueva regla de conversación de Brian
- Una pieza nueva en el árbol de documentos
- Un pivote o cambio de dirección
- Una respuesta A/B/C sobre próximas 30 días

**Si NO se actualiza:** la próxima sesión retomada arrancará con info desactualizada y se va a perder tiempo recapitulando.

**Última actualización:** 2026-05-30 (decisión Opción B + respuesta a 3 preguntas del README §7 + apertura de las 10 rondas técnicas)

---

## 3.1.septendecies — R5 ORCHESTRATION / MULTI-AGENT 100% CERRADO (2026-06-06)

Esta sub-sección documenta el cierre completo de R5 en una sola sesión (4 bloques · 14/14 sub-temas · 4 decisiones LOCKED: D-019 a D-022).

### Pre-preguntas LOCKED

| # | Pregunta | Decisión |
|---|---|---|
| P1 | Single-agent vs Multi-agent | **C — Híbrido** (single default + multi on-demand) |
| P2 | Imperativo vs Autónomo | **C — Híbrido** (esqueleto imperativo + ramas LLM) |
| P3 | Idle DMN | **B+C híbrido refinado** (verbatim Brian: "elegir y restringir pero piense cuando no activos") |

### Decisiones LOCKED Round 5

| Decisión | Sub-tema | Pick |
|---|---|---|
| **D-019** R5 B1 Tálamo & Routing | 5.1.1, 5.1.2, 5.1.3, 5.1.4 | Tool Selection B+C, Context Routing C+D, Subgraph 3 modos GM, Neuromoduladores 4 modos GM |
| **D-020** R5 B2 Dual-Process Check | 5.2.1, 5.2.2, 5.2.3 | S1/S2 multi-señal, LLM Tier C+HISTORY-AWARE Brian ⭐, Fast Path 3 layers |
| **D-021** R5 B3 Multi-Agent Network | 5.3.1, 5.3.2, 5.3.3, 5.3.4 | Hub-and-spoke 5 specialists, Lifecycle HARDENED **18 capas**, asyncio.Queue+broadcast, Cost control 7 layers |
| **D-022** R5 B4 DMN + R5 100% CERRADO | 5.4.1, 5.4.2, 5.4.3 | Scheduler híbrido, 8 tasks declarativas ⚠️ refinamiento pendiente, 9 controles cliente |

### Documentos creados/actualizados

**Mente/Cuerpo/:**
- ✅ `Ronda_05_Orchestration_Multi_Agent.md` (master, 12 secciones)
- ✅ `Ronda_05_Bloque_1_Talamo_Routing.md`
- ✅ `Ronda_05_Bloque_2_Dual_Process_Check.md`
- ✅ `Ronda_05_Bloque_3_Multi_Agent_Network.md` (incluye 18 capas hardening)
- ✅ `Ronda_05_Bloque_4_DMN_Default_Mode.md` (incluye flag refinamiento 5.4.2)

**for3s-inter/09-technical-architecture/:**
- ✅ `orchestration-multi-agent.md` (consolidado)
- ✅ `thalamus-routing.md` (B1)
- ✅ `dual-process-check.md` (B2)
- ✅ `multi-agent-network.md` (B3)
- ✅ `dmn-default-mode.md` (B4)

**Otros:**
- ✅ `../for3s-inter/07-operations/decision-log.md` — D-019 a D-022 agregadas
- ✅ `../for3s-inter/02-product/mvp-scope.md` — stack annotation R5 100%
- ✅ `../for3s-inter/05-finance/unit-economics.md` — costo total v1 FINAL post-R5 actualizado
- ✅ `../for3s-inter/09-technical-architecture/README.md` — R5 marked CERRADO
- ✅ Memoria global `project_dmn_tasks_critical_refinement.md` — flag refinamiento 5.4.2

### Cobertura Grafo Maestro post-R5

```
✅ Nodo 1 Workspace Gate (R4 parcial, R9 completar)
✅ Nodo 2 PFC (R3 parcial, R6 completar)
✅ Nodo 3 Hipocampo (R2 ✅)
✅ Nodo 4 Knowledge Graph (R2 ✅)
✅ Nodo 5 Microglía (R2 ✅)
✅ Nodo 6 DMN (R5 B4 ✅) ⭐ NEW
🟡 Nodo 7 Amígdala (defer R9 Security)
✅ Nodo 8 Tálamo (R5 B1 ✅) ⭐ NEW
✅ Nodo 9 Dual-Process Check (R5 B2 ✅) ⭐ NEW
✅ Nodo 10 Consolidación CLS (R2 ✅)
✅ Nodo 11 Neuromoduladores (R5 B1.4 ✅) ⭐ NEW
✅ Multi-Agent Network (R5 B3 ✅) ⭐ NEW

NODOS COMPLETOS: 8/11 + Multi-Agent + 7 edges principales
```

### Costo total v1 FINAL post-R5

```
Subtotal R1+R2+R3+R4 v1 100% : ~$64-79/mes
R5 B1 Tálamo                  : $0
R5 B2 Dual-Process            : +$2
R5 B3 Multi-Agent             : +$3-5
R5 B4 DMN                     : +$5-10
─────────────────────────────────────
TOTAL v1 FINAL post-R5        : ~$74-96/mes

% techo Pilot Light P2: 9.7% (margen 90.3%)
% cap P5 LLM: 37-45% (margen $110-127)
Recursos servidor: ~5 GB RAM (de 30 GB)
```

### ⚠️ Refinamiento crítico pendiente

**5.4.2 DMN Tasks Declarativas:** LOCKED v1 (8 tasks) PERO Brian marcó refinamiento profundo pre-programación.

Memoria global: `project_dmn_tasks_critical_refinement.md`

Plan: crear `Ronda_05_DMN_Tasks_Detailed.md` antes de R5 programación con:
- Pseudocode completo por las 8 tasks
- Schemas Pydantic input/output
- Trigger thresholds defendibles
- Eval criteria valor per task (ROI medible)
- Interaction graph entre tasks
- Auto-improvement loop end-to-end
- Cost ROI per task
- v2-v3 expansion path

### Próximo paso

**R6 — Memory Stack Extensions** (próxima ronda):
- Nodo 2 PFC completar (R3 parcial)
- Knowledge Graph schema avanzado
- Hipocampo time-aware queries
- Forgetting policies refined
- Memory observability dashboard
- Eval framework memory regresión

Programación NO arranca hasta R9 o R10 cerrados (Brian instrucción).

---

## 3.1.octodecies — R6 MEMORY STACK EXTENSIONS 100% CERRADO (2026-06-07) ⭐ Pilar 3 ACTIVADO

Esta sub-sección documenta el cierre completo de R6 en una sola sesión (4 bloques · 13/13 sub-temas · 4 decisiones LOCKED: D-023 a D-026).

### Pre-preguntas LOCKED

| # | Pregunta | Decisión |
|---|---|---|
| P1 | Skill schema | **C+A** Híbrido (metadata Pydantic + markdown body filesystem) |
| P2 | Skill promotion | **A+C+B** Triple (auto WS + Brian core + cliente flex + threshold) |
| P3 | Cross-workspace | **B** Stack común opt-in |

### Decisiones LOCKED Round 6

| Decisión | Sub-tema | Pick |
|---|---|---|
| **D-023** R6 B1 PFC Orchestrator | 6.1.1, 6.1.2, 6.1.3, 6.1.4 | Plan-then-execute + 8 signals confidence + estratificado re-plan + 7 fases skill promotion |
| **D-024** R6 B2 Ganglios Basales / Skills ⭐ Pilar 3 | 6.2.1, 6.2.2, 6.2.3, 6.2.4, 6.2.5 | Schema híbrido + GO plan-template + NO-GO 3-niveles + Dopaminergic 7 signals + Lifecycle manager |
| **D-025** R6 B3 Memory Extensions | 6.3.1, 6.3.2, 6.3.3 | Time-aware DSL + Forgetting GDPR multi-dim + Dashboard HTMX completo |
| **D-026** R6 B4 Memory Eval + R6 100% CERRADO | 6.4.1 | Multi-layer 4 layers regression |

### Documentos creados/actualizados

**Mente/Cuerpo/:**
- ✅ `Ronda_06_Memory_Stack_Extensions.md` (master, 13 secciones)
- ✅ `Ronda_06_Bloque_1_PFC_Orchestrator.md`
- ✅ `Ronda_06_Bloque_2_Ganglios_Basales_Skills.md` ⭐ NÚCLEO Pilar 3
- ✅ `Ronda_06_Bloque_3_Memory_Extensions.md`
- ✅ `Ronda_06_Bloque_4_Memory_Eval.md` (incluye flag pre-código)

**for3s-inter/09-technical-architecture/:**
- ✅ `memory-stack-extensions.md` (consolidado)
- ✅ `pfc-orchestrator.md` (B1)
- ✅ `ganglios-basales-skills.md` (B2 ⭐ Pilar 3)
- ✅ `memory-extensions.md` (B3)
- ✅ `memory-eval.md` (B4)

**Otros:**
- ✅ `../for3s-inter/07-operations/decision-log.md` — D-023 a D-026 agregadas
- ✅ `../for3s-inter/02-product/mvp-scope.md` — stack annotation R6 100%
- ✅ `../for3s-inter/05-finance/unit-economics.md` — costo total v1 FINAL post-R6
- ✅ `../for3s-inter/09-technical-architecture/README.md` — R6 marked CERRADO
- ✅ Memoria global `project_r6_critical_pre_code_review.md` (flag pre-código)

### Cobertura Grafo Maestro post-R6

```
✅ Nodo 1 Knowledge Graph (R2)
✅ Nodo 2 Hipocampo (R2 + R6 6.3.1 time-aware) — EXTENDIDO
✅ Nodo 3 PFC / Orchestrator (R3+R5+R6 B1) — COMPLETO 100% ⭐
✅ Nodo 4 Ganglios Basales / Skills (R6 B2) — COMPLETO 100% NUEVO ⭐⭐
✅ Nodo 5 Microglía (R2 + R6 6.3.2 forgetting refined) — EXTENDIDO
✅ Nodo 6 DMN (R5)
🟡 Nodo 7 Amígdala (defer R9 Security)
✅ Nodo 8 Tálamo (R5)
✅ Nodo 9 Dual-Process Check (R5)
✅ Nodo 10 Consolidación CLS (R2)
✅ Nodo 11 Neuromoduladores (R5)

NODOS COMPLETOS: 10/11 (solo Amígdala R9 pending)
```

### Pilar 3 Autonomía Generativa ACTIVADO ⭐⭐⭐

Capacidad #1 (Generar skills nuevas) 100% v1 OPERATIVA:
- ✅ Plans exitosos → SkillCandidate (DMN detection)
- ✅ LLM genera SkillSpec
- ✅ Sandbox isolation 7 días
- ✅ Evaluación PASS/MARGINAL/FAIL
- ✅ Promoción 3-tier (workspace auto + core Brian + common opt-in)
- ✅ Vida útil con dopaminergic scoring
- ✅ Auto-decline + microglía archive
- ✅ Auto NO-GO from failures

**Esto NO existe en NINGÚN agente actual** (Grafo Maestro Pilar 3).

### Costo total v1 FINAL post-R6

```
Subtotal R1+R2+R3+R4 v1+R5 100% : ~$74-96/mes
R6 B1 PFC planning Sonnet        : +$3-5
R6 B2 Skills + dopaminergic      : +$1
R6 B3 Memory extensions          : +$0 reused
R6 B4 Memory eval Haiku          : +$2-3
─────────────────────────────────────────
TOTAL v1 FINAL post-R6           : ~$80-105/mes

% techo Pilot Light P2: 10.5% (margen 89.5%)
% cap P5 LLM: 40-50% (margen $100-120)
Recursos servidor: ~5.5 GB RAM (de 30 GB)
```

### ⚠️ Flag global pre-código CRÍTICO

**`project_r6_critical_pre_code_review.md`** (memoria global)

Brian quote verbatim (2026-06-07): "NOTA IMPORTANTE VOLVER A REVISAR Y PLANIFICAR CUANDO ESTEMOS REALIZANDO CODIGO TODO EL R6 POR QUE ES UN R EXTREMANDAMENTE IMPORTANTE"

Plan: crear `Ronda_06_Pre_Code_Review_Detailed.md` antes de programar R6 con:
- Pseudocode completo por cada sub-tema
- Schemas Pydantic formal input/output
- Trigger thresholds calibrados con razonamiento
- Eval criteria valor per decisión
- Interaction graph cross-sub-temas
- Auto-improvement loop end-to-end
- Cost ROI per task estimado vs medido

### Próximo paso

**R7 — Frontend / Channel** (próxima ronda):
- Dashboard cliente expansion (6.3.3 v2)
- Telegram adapter producción (R4 4.2.4 reused)
- API REST completo
- WebSocket support

Programación NO arranca hasta R9/R10 cerrados + re-revisión R6 obligatoria.

---

## 3.1.novodecies — R7 FRONTEND / CHANNEL 100% CERRADO (2026-06-08) ⭐ Pilar 1 Seguridad COMPLETO

Esta sub-sección documenta el cierre completo de R7 en una sola sesión (4 bloques · 12/12 sub-temas · 4 decisiones LOCKED: D-027 a D-030).

### Pre-preguntas LOCKED

| # | Pregunta | Decisión |
|---|---|---|
| P1 | Channels INPUT v1 | **C** Telegram + REST + GitHub webhook |
| P2 | Output Gate strict vs pragmatic | **C** Híbrido pragmatic default + strict opt-in |
| P3 | Dashboard expansion v1 | **C** Progressive enhancement |

### Decisiones LOCKED Round 7

| Decisión | Sub-tema | Pick |
|---|---|---|
| **D-027** R7 B1 Channels de Entrada | 7.1.1, 7.1.2, 7.1.3 | Telegram production webhook 8 components + REST API formal 8 components + GitHub App formal 8 components ⭐ wedge QA central |
| **D-028** R7 B2 Output Gate ⭐ Pilar 1 COMPLETO | 7.2.1, 7.2.2, 7.2.3 | Output signing híbrido (HMAC default + Ed25519 strict opt-in) + Response format Pydantic QA Pack + 4 renderers + Streaming 25+ events + 4 channel adapters |
| **D-029** R7 B3 Auth & RBAC Cross-Channel | 7.3.1, 7.3.2, 7.3.3 | Identity central + 6 credential types + UnifiedAuthenticator + RBAC hierarchical 35+ permissions + 5 system roles + custom workspace roles + Sessions DB per-channel strategy + access/refresh rotation |
| **D-030** R7 B4 Dashboard + Notifications + R7 100% CERRADO | 7.4.1, 7.4.2, 7.4.3 | Dashboard module system (8+ modules) + global search + Notification system multi-channel (15+ events + 4 channels + preferences + digest) + PWA complete (install + service worker + push system-level + offline queue) |

### Documentos creados/actualizados

**Mente/Cuerpo/:**
- ✅ `Ronda_07_Frontend_Channel.md` (master, 12 secciones)
- ✅ `Ronda_07_Bloque_1_Channels_Entrada.md`
- ✅ `Ronda_07_Bloque_2_Output_Gate.md` ⭐ Pilar 1 COMPLETO
- ✅ `Ronda_07_Bloque_3_Auth_RBAC.md`
- ✅ `Ronda_07_Bloque_4_Dashboard_Notifications.md` (CIERRA R7)

**for3s-inter/09-technical-architecture/:**
- ✅ `frontend-channel.md` (consolidado)
- ✅ `channels-input.md` (B1)
- ✅ `output-gate.md` (B2 ⭐ Pilar 1)
- ✅ `auth-rbac.md` (B3)
- ✅ `dashboard-notifications.md` (B4)

**Otros:**
- ✅ `../for3s-inter/07-operations/decision-log.md` — D-027 a D-030 agregadas
- ✅ `../for3s-inter/02-product/mvp-scope.md` — stack annotation R7 100%
- ✅ `../for3s-inter/05-finance/unit-economics.md` — costo total v1 FINAL post-R7
- ✅ `../for3s-inter/09-technical-architecture/README.md` — R7 marked CERRADO

### Grafo Maestro layers materializados post-R7

```
✅ INPUT (Usuario / API) — R7 B1
✅ Workspace Gate — R4 + R7 Auth
✅ Tálamo (Nodo 8) — R5
🟡 Amígdala (Nodo 7) — defer R9 Security
✅ PFC Orchestrator (Nodo 3) — R3 + R5 + R6
✅ Hipocampo (Nodo 2) — R2 + R6
✅ Knowledge Graph (Nodo 1) — R2
✅ Ganglios Basales / Skills (Nodo 4) — R6 ⭐
✅ Multi-Agent Network — R5
✅ Dual-Process Check (Nodo 9) — R5
✅ OUTPUT GATE — R7 B2 ⭐ NEW
✅ OUTPUT (Usuario / API) — R7 B2 ⭐ NEW
✅ DMN (Nodo 6) — R5
✅ Microglía (Nodo 5) — R2 + R6
✅ Consolidación CLS (Nodo 10) — R2
✅ Neuromoduladores (Nodo 11) — R5

NODOS COMPLETOS: 10/11 (solo Amígdala R9 pending)
LAYERS GRAFO MAESTRO: TODOS los principales materializados v1
```

### Pilar 1 Seguridad COMPLETO ⭐⭐⭐

Grafo Maestro Pilar 1 (Encriptación end-to-end + zero-trust + workspace boundaries):

| Componente | Status | Implementación |
|---|---|---|
| Encryption at rest | ✅ R2 B4 | LUKS + app-layer AES-GCM (R4 4.1.3 KEK) |
| Workspace boundaries | ✅ R2 + R7 | RLS Postgres + 3-layer skill isolation + RBAC |
| **Output Gate** | ✅ **R7 B2** | Híbrido signing + trace + encrypt |
| **Zero-trust auth** | ✅ **R7 B3** | Identity central + RBAC + sessions |
| Audit infrastructure | ✅ R3 B4 + R7 | Cryptographic chain + per identity |
| Revocation real-time | ✅ R4 4.3.1 + R7 7.3 | Cross-channel cascade |

**Pilar 1 100% v1 completo.** Solo falta Amígdala (R9).

### Costo total v1 FINAL post-R7

```
Subtotal R1+R2+R3+R4 v1+R5+R6 100% : ~$80-105/mes
R7 B1 Channels (reused stack)       : $0
R7 B2 Output Gate (crypto local)    : $0
R7 B3 Auth + RBAC + Sessions        : $0
R7 B4 Dashboard expansion (HTMX)    : $0
R7 B4 Notifications SMTP/SendGrid   : +$0-2
R7 B4 PWA (local assets)            : $0
─────────────────────────────────────────
TOTAL v1 FINAL post-R7              : ~$80-107/mes

% techo Pilot Light P2: 10.9% (margen 89.1%)
% cap P5 LLM: 40-50% (margen $100-120)
Recursos servidor: ~6 GB RAM (de 30 GB)
```

### Postgres tables agregadas R7 (15+)

Channels (5): telegram_identities, api_keys, webhook_configs, github_installations, github_webhook_deliveries
Output Gate (2): workspace_signing_keys, output_signatures
Auth (5): identities, identity_credentials, roles, identity_role_assignments, sessions
Notifications (4): notifications, notification_preferences, notification_deliveries, in_app_notifications
PWA (1): push_subscriptions

### Próximo paso

**R8 — Observability completa** (próxima ronda):
- Prometheus métricas expand unified (R3 B4 + R5 + R6 + R7)
- Grafana dashboards (Brian internal)
- Audit log retention policies
- Alarms multi-channel (R7 7.4.2 reused)
- Performance metrics per channel + per identity
- Pilar 2 Escalabilidad materializado
- SLO/SLA tracking

Programación NO arranca hasta R9/R10 cerrados + re-revisión R6 pre-código obligatoria.

---

## 3.1.duodecies — R8 OBSERVABILIDAD COMPLETA 100% CERRADO (2026-06-08) ⭐ Pilar 2 Scalability Foundation

### Síntesis

**R8 — Observabilidad Completa** queda LOCKED 100%: 12/12 sub-temas, 4/4 bloques. Materializa **Grafo Maestro §6.4 (Audit Infrastructure LITERAL) + §6.5 (ObsCompleta) + Pilar 2 §7 (Scalability foundation)**. Brian ahora tiene visibilidad 30-second-glance, compliance SOC2/GDPR ready, clientes self-service SLO compliance.

### Pre-preguntas R8 LOCKED

- **P1** Stack obs → **C — Prometheus + Loki + Tempo + Grafana** (CNCF standard, self-hosted)
- **P2** Audit storage → **C+B — Postgres + WAL + R2 archive** (triple redundancy GM §6.4)
- **P3** SLO/SLA scope v1 → **B — Client self-service básico** (no enterprise legal v1)

### Stack lockeado (4 bloques)

**B1 Unified Metrics (Foundation Pilar 2):**
- 8.1.1 Métricas per nodo C — 11 nodos GM + 5 categorías + cardinality control ~3,500 series + ScalingIndicatorsCollector 10s
- 8.1.2 Cross-cutting C — Request E2E + Workspace aggregates + Identity top-10 + Tempo tracing correlation ~1,650 series
- 8.1.3 Unit economics C — CostAggregator Redis sliding + P5CapEnforcer warn80%/block100% + ForecastEngine + BurnRateDetector + Pilar 2 §7.3 trajectory $0.80 → $0.20 validation
- **GRAND TOTAL ~5,150 series Prometheus** (handle 10K+)

**B2 Grafana Dashboards (Brian Internal):**
- 8.2.1 Operations C — 5 sections + drill-down (30-sec glance)
- 8.2.2 Analytics C — 4 sections + drill-down (Cost + Eval + Skills + DMN ⚠️ caveat 5.4.2)
- 8.2.3 Pilar 2 Scalability C — 5 sections + capacity simulator (what-if + spot eligibility + sharding candidates)

**B3 Audit Infrastructure (GM §6.4 LITERAL):**
- 8.3.1 Chain Criptográfico C — SHA-256 hash_prev/hash_self + Postgres TRIPLE GUARD triggers (UPDATE/DELETE/TRUNCATE blocked) + WAL secondary + R2 tertiary + RLS 3 roles + ChainVerificationJob
- 8.3.2 Retention C — Hot Postgres 90d + Warm Postgres 1y + Cold R2 .jsonl.gz perpetuo + GDPR pseudonymization view-based (no chain break)
- 8.3.3 Query Engine C — 7 components + 6 compliance templates (SOC2 + GDPR + workspace + critical + identity + cost) + Chain Verification API + Smart Restore Planner + Materialized Views

**B4 SLO/SLA + Alerts + Incidents:**
- 8.4.1 SLO/SLA C — 3 tiers (pilot 95% / standard 99.5% / enterprise 99.9% refund_eligible) + per-channel additive + error budget hourly + self-service API + 4 Prometheus rules
- 8.4.2 Alerts Aggregation C — AM + 8 components (Ingestor + Dedup + Group + Cascade + Routing + Silence + Ack + Escalation) cross-system R5+R6+R7+R8
- 8.4.3 Incident Management C — 7 states + 4 severity + 4 runbooks pre-built + status page público + postmortem auto-template (5 whys) + MTTR/MTBF/MTTA

### Pilar 2 Scalability Foundation establecida

- ScalingIndicatorsCollector → Pilar 2 §7.5 capacity signals
- Per-node strategy categorization (stateless+replicas / worker_pool / sharded / spot_eligible)
- Capacity simulator what-if pre-scaling decisions
- Unit economics trajectory tracking ($0.80 v1 → $0.20 v2)
- SLO-aware decisions guardrails (error budgets)

### Compliance-ready post-R8

- SOC2 audit trail provable (cryptographic chain + SHA-256 manifest per R2 day)
- GDPR data lineage trackable + right-to-be-forgotten (pseudonymization view-based)
- Forensics post-incident reliable (3-tier retention perpetuo cold R2)
- 6 compliance reports pre-built automatizados

### Costo v1 actualizado post-R8

```
Subtotal post-R7 baseline:                 USD ~80-107/mes
+ Prometheus + Loki + Tempo + Grafana:    +USD ~5-8/mes (self-hosted)
+ R2 audit cold storage (post 1y warm):   +USD ~2-3/mes
+ Postgres partitioning overhead:          +USD ~5-8/mes
+ Alertmanager + custom aggregator:        $0 (incluido)
─────────────────────────────────────────────────
TOTAL v1 FINAL post-R8:                    USD ~95-130/mes
% techo Pilot Light P2:                    13.7% (margen 86.3%)
% cap P5 LLM:                              40-50% (margen $100-120)
Recursos servidor:                         ~8 GB RAM (de 30 GB)
Overhead R8 stack:                         ~2 GB RAM (Prom + Loki + Tempo + Grafana)
```

### Postgres tables agregadas R8

audit_events (partitioned monthly) + audit_events_archive + audit_events_pseudonymized + request_records + incidents + incident_timeline_entries + postmortems + status_page_entries + alerts + alert_acks + alert_silences

### Audit events nuevos R8 (~50)

- B1 (8): cardinality + scaling indicators + P5 cap + burn rate + Pilar 2 compliance
- B2 (8): dashboard views + drill-downs + annotations + capacity simulator
- B3 (13): chain integrity + WAL + RBAC + archive + cold export + GDPR + query + export + reports
- B4 (26): SLO compliance + error budget + alerts ingested/dedup/grouped/cascade/routed/silenced/acked/escalated + incidents (11 lifecycle events)

### Docs producidos

✅ `Mente/Cuerpo/Ronda_08_Observabilidad_Completa.md` (master)
✅ `Mente/Cuerpo/Ronda_08_B1_Unified_Metrics.md`
✅ `Mente/Cuerpo/Ronda_08_B2_Grafana_Dashboards.md`
✅ `Mente/Cuerpo/Ronda_08_B3_Audit_Infrastructure.md`
✅ `Mente/Cuerpo/Ronda_08_B4_SLO_Alerts_Incidents.md`
✅ `for3s-inter/09-technical-architecture/observability-metrics.md`
✅ `for3s-inter/09-technical-architecture/observability-dashboards.md`
✅ `for3s-inter/09-technical-architecture/audit-infrastructure.md`
✅ `for3s-inter/09-technical-architecture/slo-sla-framework.md`
✅ `for3s-inter/09-technical-architecture/incident-management.md`
✅ `for3s-inter/07-operations/decision-log.md` (D-031, D-032, D-033, D-034)
✅ `for3s-inter/02-product/mvp-scope.md` (anotación R8 100% + costos updated)
✅ `for3s-inter/05-finance/unit-economics.md` (post-R8 costos)
✅ `for3s-inter/09-technical-architecture/README.md` (R8 row + sub-docs)
✅ `Mente/memory/Estado_Sesion_Continuidad.md` (este §3.1.duodecies)

### Flags carry-forward (PERSISTEN post-R8)

⚠️ **DMN 5.4.2 REFINAMIENTO PENDIENTE** — memory `project_dmn_tasks_critical_refinement` — 8.2.2 Analytics DMN section v1 con caveat, requiere re-review pre-código profundo.

⚠️ **R6 PRE-CODE REVIEW CRÍTICO** — memory `project_r6_critical_pre_code_review` — Memory Stack Extensions completo necesita replanificación pre-programación.

Ambos flags persistirán hasta atender pre-programación POST-R10.

### Próximo paso

**R9 — Security/Compliance** (penúltima ronda):
- Amygdala Node 7 (último nodo cerebral pendiente): threat detection + anomaly response
- Security audit completo (uses 8.3.3 compliance reports)
- Compliance framework formal: SOC2 + GDPR + (potencial) HIPAA per workspace tier
- Threat model formal: STRIDE + DREAD per componente
- Penetration testing plan
- Incident response security playbooks (extiende 8.4.3 runbooks)

Después R9 → R10 CI/CD/Deploy (cierre) → **programación arranca POST-R10**.

---

## 3.1.R9 — R9 SECURITY / COMPLIANCE 100% CERRADO (2026-06-09) ⭐ 11/11 NODOS + Pilar 1 COMPLETO (INPUT+OUTPUT)

> **Nota numeración:** las secciones §3.1 usaron numeración latina (…septendecies/octodecies/novodecies) y R8 quedó etiquetado §3.1.duodecies por error de secuencia. Para evitar ambigüedad, R9 usa etiqueta explícita §3.1.R9. R8 = §3.1.duodecies (línea ~4429). Orden cronológico real: R5(septendecies) → R6(octodecies) → R7(novodecies) → R8(duodecies, mal numerado) → R9(esta sección).

### Síntesis

**R9 — Security / Compliance** queda LOCKED 100%: 9/9 sub-temas, 3/3 bloques + 3 pre-preguntas (todas C). Cierra el **último nodo cerebral (Amígdala Node 7) → 11/11 NODOS COMPLETOS** y **Pilar 1 Seguridad de verdad** (perímetro INPUT + OUTPUT). Programa compliance audit-ready (SOC2 + GDPR) vendible enterprise.

### Pre-preguntas R9 LOCKED (C/C/C)

- **P1** Alcance Amígdala → **C — Completo multi-capa** (input scanner + anomaly + coordinator → cierra Node 7)
- **P2** Compliance → **C — SOC2 + GDPR readiness program** (audit-ready, cert real v2)
- **P3** Pentest+IR → **C — Threat model + pentest plan + security playbooks**

### Stack lockeado (3 bloques)

**B1 Amígdala (Node 7 — ÚLTIMO NODO CEREBRAL):**
- 9.1.1 Input Threat Scanner C — 5 capas fail-fast (heurística ~1ms → normalización anti-evasión decode/dehomoglyph → LLM Haiku classifier solo suspicious ~10% → canary tokens exfil → external content sanitization PR/files/webhooks) · OWASP LLM01+LLM06 · ~3ms+$0.0001 promedio · fast-path defensivo
- 9.1.2 Anomaly Detection C — 4 detectores (rate vs EWMA + conversational escalation gradual-jailbreak + behavioral deviation credential-compromise + privilege probing RBAC denials) · baselines EWMA per-identity + cold-start learning mode · acción graduada (block/challenge/monitor/pass) · behavioral window Redis TTL 1h privacy
- 9.1.3 Threat Coordinator C — ThreatLevel 5 niveles DEFCON (CLEAR→CRITICAL) · respuesta proporcional · fast-path brain bypass · MODULA cerebro (Amígdala→Tálamo EMERGENCIA/MINIMO + Amígdala→Neuromod HIGH_ATTENTION + Amígdala→Microglia threat_context) · tool restrictions dinámicas

**B2 Threat Model + Pentest + IR:**
- 9.2.1 Threat Model C — STRIDE+DREAD 14 componentes + 3 trust boundaries + DREAD scoring + OWASP 10/10 + living doc
- 9.2.2 Pentest Plan C — 5 dimensiones (scope 4 capas + toolkit AI-aware garak/promptfoo + custom attack suite = regression test + cadencia + self/contratado) · ejecución post-código
- 9.2.3 Security Playbooks C — 8 PICERL (breach + injection + credential + audit-tampering + secrets + insider + supply-chain + DoS) + ForensicsKit R2 WORM + GDPR 72h notification + auto-trigger Amígdala

**B3 Compliance Framework:**
- 9.3.1 SOC2 Control Mapping C — 5 TSC (Security CC1-CC9 + Availability + Confidentiality + PI + Privacy) → controles R1-R9 + evidence binding (8.3.3 auto-gen) · ⭐ SALES WEDGE
- 9.3.2 GDPR Program C — DSAR 6 derechos (Art 15-21) + consent (Art 6/7) + DPA (Art 28) + RoPA (Art 30) + privacy data flow · doble propósito (Privacy TSC)
- 9.3.3 Evidence + Gap + Readiness C — EvidenceCollector + GapAnalyzer + ReadinessScorecard (verdict objetivo) + Monitor (drift weekly) + AuditPack 1-click

### Pilar 1 cierre (perímetro completo)

```
INPUT → [AMÍGDALA 9.1.x] → Tálamo → PFC/MA → ... → [MICROGLIA eval] → [R7 OUTPUT GATE] → response
        ↑ INPUT GUARD (R9)                            ↑ OUTPUT GUARD (R5/R6 + R7)
```
- Justificación: threat model STRIDE+DREAD (9.2.1)
- Validación: pentest + custom attack suite (9.2.2)
- Respuesta: security playbooks PICERL (9.2.3)
- Compliance: SOC2 + GDPR audit-ready (B3)

### OWASP LLM Top 10: 10/10 covered

LLM01 (Amígdala scanner) · LLM02 (Output Gate+Microglia) · LLM04 (token bucket+rate+DoS playbook) · LLM05 (MCP SHA+Trivy+supply chain playbook) · LLM06 (canary+RLS+KEK+breach playbook) · LLM07 (tool authz+sandbox) · LLM08 (RBAC+tool restrictions) · LLM09 (confidence+Microglia) · LLM10 (LOCAL+auth+audit). LLM03 N/A (no fine-tuning).

### Compliance readiness v1 (honesto)

- SOC2 ~85-90% NEARLY_READY (planned: CC7.1 pentest exec post-código, A1.3 DR testing R10)
- GDPR ~88-92% NEARLY_READY (pending: DPA lawyer review pre-primer-deal-EU)
- → AUDIT_READY tras ejecución post-código. Cert real (auditor externo) = v2.

### Costo v1 actualizado post-R9

```
Subtotal post-R8 baseline:                 USD ~95-130/mes
+ Amígdala Haiku classifier (~10% inputs): +USD ~0-2/mes
─────────────────────────────────────────────────
TOTAL v1 FINAL post-R9:                    USD ~95-132/mes
% techo Pilot Light P2:                    13.9% (margen 86.1%)
Recursos servidor:                         ~8.5 GB RAM (de 30 GB)
Overhead R9:                               ~500 MB (Amígdala + behavioral windows)
```

Costos seguridad EJECUCIÓN (post-revenue, no v1): pentest externo anual ~$5-15K · SOC2 cert ~$10-30K (v2) · DPA lawyer ~$1-3K una vez · Vanta/Drata opcional ~$10-20K/año (v2).

### ~35 audit events nuevos R9

- B1 Amígdala (15): threat_blocked/suspicious/canary/external + anomaly_blocked/challenge/monitored/credential_compromise/privilege_probing/baseline_learning + fast_path/threat_level/brain_modulation/tool_restriction/challenge
- B2 Security IR (6): security_incident_declared · forensic_snapshot_captured · breach_notification_assessed/deadline_set · security_playbook_step_completed · insider_threat_breakglass_activated
- B3 Compliance (14): soc2_control_tested/evidence_collected/gap_identified + gdpr_dsar_received/fulfilled/deadline_warning + gdpr_consent_granted/withdrawn + gdpr_legal_hold_blocked_erasure + gdpr_ropa_updated + compliance_evidence_collected/gap_identified/readiness_computed/drift_detected + audit_pack_generated

### Docs producidos

✅ `Mente/Cuerpo/Ronda_09_Security_Compliance.md` (master)
✅ `Mente/Cuerpo/Ronda_09_B1_Amigdala.md`
✅ `Mente/Cuerpo/Ronda_09_B2_Threat_Pentest_IR.md`
✅ `Mente/Cuerpo/Ronda_09_B3_Compliance_Framework.md`
✅ `for3s-inter/09-technical-architecture/amygdala-threat-detection.md`
✅ `for3s-inter/09-technical-architecture/threat-model.md`
✅ `for3s-inter/09-technical-architecture/pentest-plan.md`
✅ `for3s-inter/09-technical-architecture/security-playbooks.md`
✅ `for3s-inter/09-technical-architecture/soc2-control-mapping.md`
✅ `for3s-inter/09-technical-architecture/gdpr-program.md`
✅ `for3s-inter/09-technical-architecture/compliance-readiness.md`
✅ `for3s-inter/07-operations/decision-log.md` (D-035, D-036, D-037)
✅ `for3s-inter/02-product/mvp-scope.md` (R9 row + 11/11 nodos + Pilar 1 completo + costos)
✅ `for3s-inter/05-finance/unit-economics.md` (post-R9 costos)
✅ `for3s-inter/09-technical-architecture/README.md` (R9 row + 7 sub-docs)
✅ `Mente/memory/Estado_Sesion_Continuidad.md` (esta §3.1.R9)

### Items ejecución post-código (LOCKED como plan)

- Pentest ejecución (automated CI + manual red team + external anual)
- Custom AI attack suite (payloads + correr contra staging = regression test)
- Security playbooks runtime (ForensicsKit + breach notification operativos)
- DPA lawyer review (pre-primer-deal-EU)
- SOC2 cert real (auditor externo, v2)
- Recovery/DR testing (SOC2 A1.3, post-R10)
- Amígdala patterns/baselines tuning (tráfico real + DMN auto-update)

### Flags carry-forward (PERSISTEN post-R9)

⚠️ **DMN 5.4.2 REFINAMIENTO** — memory `project_dmn_tasks_critical_refinement` — re-review pre-código profundo 8 DMN tasks.
⚠️ **R6 PRE-CODE REVIEW CRÍTICO** — memory `project_r6_critical_pre_code_review` — Memory Stack Extensions replanificación pre-implementación.
⭐ **SOC2 SALES WEDGE** — memory `project_soc2_sales_wedge` — resaltar en página/marketing como certificado de calidad B2B. 5 TSC ya mapeadas (9.3.1).

### Próximo paso

**R10 — CI/CD / Deploy** (ÚLTIMA ronda técnica):
- CI/CD pipeline (GitHub Actions, foundation R4)
- Deploy LOCAL + Cloudflare Tunnel (D-009) + systemd
- Backup/recovery operacional (DR testing → cierra SOC2 A1.3)
- Migration/rollback + secrets bootstrap (KEK R4)
- Observability deploy (Prometheus+Loki+Tempo+Grafana stack R8)
- Security hardening deploy (Amígdala + threat model controls R9)
- Pre-flight checklist (compliance readiness R9 B3)

**Después R10 → PROGRAMACIÓN ARRANCA** (con re-revisión obligatoria R6 + DMN 5.4.2).

---

## 3.1.R10 — R10 CI/CD/DEPLOY 100% CERRADO (2026-06-09) 🏆 ÚLTIMA RONDA — LAS 10 RONDAS TÉCNICAS COMPLETAS

### Síntesis

**R10 — CI/CD / Deploy** queda LOCKED 100%: 9/9 sub-temas, 3/3 bloques + 3 pre-preguntas. **ES LA ÚLTIMA RONDA TÉCNICA → LAS 10 RONDAS DE FOR3S OS ESTÁN COMPLETAS.** El sistema es DEPLOYABLE + OPERABLE + RECUPERABLE. Cierra el último gap compliance (SOC2 A1.3). El diseño está cerrado.

### Pre-preguntas R10 LOCKED

- **P1** Deploy/Runtime → **B — Híbrido** (systemd app/workers + Postgres/Valkey nativos + Docker MCP/observability)
- **P2** CI/CD → **B — CD completo con gates** (tests + security + build → staging → smoke → prod auto + rollback)
- **P3** Backup/DR → **C — DR completo + recovery testing + RTO/RPO** (cierra SOC2 A1.3)

### Stack lockeado (3 bloques)

**B1 CI/CD Pipeline:**
- 10.1.1 CI Pipeline C — 7 stages fail-fast (lint+secret-scan → unit → SAST Bandit/Semgrep/Trivy → integration → E2E+eval+memory-regression+custom-attack-suite+garak+promptfoo → **PILAR 3 GATE human approval** → compliance gate) · GitHub Actions
- 10.1.2 Build + Staging C — build versionado (R4 SemVer+SHA, artifact tamper-proof) + staging idéntico + migration dry-run anonimizado (8.3.2) + 10 smoke tests + promotion gate + release channels
- 10.1.3 Prod Deploy + Rollback C — graceful (drain + rolling + graceful app) + health gate (smoke + SLO 5min) + auto-rollback + migration expand/contract

**B2 Deploy + Infra:**
- 10.2.1 Runtime C — híbrido systemd (app/workers/DB, deps+auto-restart+cgroups+hardening) + Docker (MCP/observability) bajo systemd · ~8.5GB/30GB
- 10.2.2 Networking C — **dual-plane**: Cloudflare Tunnel (clientes, WAF+TLS+rate-limit+DDoS) + **Tailscale (admin Brian, red privada, ya instalado)** · Grafana público eliminado · mejora SOC2 CC6.6 · memory project_dual_plane_networking
- 10.2.3 Secrets + Observability C — Master KEK OFFLINE bootstrap (TPM/USB) + systemd LoadCredential (Brian nunca ve plaintext) + rotación + observability provisioning declarativo R8

**B3 Backup/DR/Ops:**
- 10.3.1 Backup C — 3-2-1 (Postgres base+WAL PITR + disco externo + R2 offsite) + chain-preserving + GDPR-aware + anti-ransomware
- 10.3.2 DR Testing C — programado (semanal auto + trimestral/semestral/anual) + RTO/RPO por tier + 5 escenarios + recovery runbooks PICERL · **⭐ CIERRA SOC2 A1.3**
- 10.3.3 Pre-Flight + Ops C — pre-flight checklist 11 checks (gate 10.1.3) + 12 ops runbooks + índice maestro + bus factor mitigation (Git + ONBOARDING.md + break-glass)

### Pipeline end-to-end

```
push → CI 7 stages → build artifact → staging + migration dry-run + smoke →
promotion gate → pre-flight 11 checks + snapshot → prod deploy graceful →
health gate (SLO 5min) → ✅ production / ❌ auto-rollback + incident
```

### Networking dual-plane (decisión destacada)

Tailscale ENTRA como admin plane (Brian ya instalado). Cloudflare Tunnel = data plane clientes. Grafana público (Cloudflare Access) ELIMINADO → solo tailnet privada. Memory: `project_dual_plane_networking`.

### SOC2 A1.3 cerrado

recovery testing: planned → IMPLEMENTED → SOC2 readiness ~85-90% → **~90-95%**. RTO/RPO medidos defendibles enterprise.

### Costo v1 FINAL post-R10

```
Subtotal post-R9:              USD ~95-132/mes
+ Backup R2:                   +USD ~2-5/mes
+ CI/CD + Cloudflare + Tailscale: $0 (free tiers + TPM existente)
─────────────────────────────────────────
TOTAL v1 FINAL post-R10:       USD ~97-137/mes
% techo Pilot Light P2:        ~14.3% (margen 85.7%)
```

### ~38 audit events nuevos R10
CI/CD (14) + Deploy/Infra (11) + Backup/DR/Ops (13)

### 🏆 MILESTONE — LAS 10 RONDAS TÉCNICAS COMPLETAS

```
R1 Compute · R2 Data · R3 Model/LLM · R4 Tools/MCP · R5 Orchestration ·
R6 Memory · R7 Frontend/Channel · R8 Observabilidad · R9 Security/Compliance ·
R10 CI/CD/Deploy  →  TODAS 100% CERRADAS

• 11/11 nodos cerebrales completos
• Pilar 1 Seguridad COMPLETO (INPUT Amígdala + OUTPUT Gate)
• Pilar 2 Scalability Foundation
• Pilar 3 Autonomía Generativa ACTIVADO
• Compliance SOC2 ~90-95% + GDPR ~88-92% audit-ready
• Deployable + Operable + Recuperable
• Costo v1 ~$97-137/mo
```

### Docs producidos R10

✅ `Mente/Cuerpo/Ronda_10_CICD_Deploy.md` (master) + 3 sub-docs (B1/B2/B3)
✅ `for3s-inter/09-technical-architecture/`: cicd-pipeline.md + runtime-architecture.md + networking-tunnel.md + secrets-observability-deploy.md + backup-dr.md + operations-runbooks.md (6)
✅ `for3s-inter/07-operations/decision-log.md` (D-038, D-039, D-040)
✅ `for3s-inter/02-product/mvp-scope.md` (R10 + 10/10 rondas + costos)
✅ `for3s-inter/05-finance/unit-economics.md` (post-R10 final)
✅ `for3s-inter/09-technical-architecture/README.md` (R10 row + 6 sub-docs + tabla 100%)
✅ `Mente/memory/Estado_Sesion_Continuidad.md` (esta §3.1.R10)
✅ MILESTONE: threat-model.md CC6.6 (dual-plane) + compliance-readiness.md (A1.3 cerrado)

### ⚠️⚠️ PRÓXIMO PASO CRÍTICO — PRE-PROGRAMACIÓN ⚠️⚠️

**El diseño (R1-R10) está completo. ANTES de escribir código, instrucciones LOCKED de Brian exigen DOS revisiones:**

1. ⚠️ **RE-REVISIÓN R6 CRÍTICA** (memory: `project_r6_critical_pre_code_review`) — Memory Stack Extensions completo necesita replanificación pre-código. Núcleo Pilar 3.
2. ⚠️ **DMN 5.4.2 REFINAMIENTO** (memory: `project_dmn_tasks_critical_refinement`) — 8 DMN tasks atención profunda pre-código.

**Después de esas dos revisiones → ARRANCA PROGRAMACIÓN.**

Secuencia sugerida programación (foundation-first): R10 CI/CD montado temprano → R1 compute → R2 data → R3 LLM → R4 tools → R5 orchestration → R6 memory (post re-review) → R7 channels → R8 observability → R9 security → deploy.

### Flags carry-forward (PERSISTEN)
⚠️ `project_r6_critical_pre_code_review` · ⚠️ `project_dmn_tasks_critical_refinement` · ⭐ `project_soc2_sales_wedge` · `project_dual_plane_networking`

---

## CIERRE

Este es el **documento de continuidad de For3s**. Lo escribí porque Brian pidió defensivamente que cualquier futuro Claude pueda retomar la conversación sin perder contexto.

**Si lo lees, ya tienes 90% del contexto operativo necesario.** El otro 10% está en los 5 documentos prioritarios del §2.

**Regla de oro:** ante duda, pregunta a Brian. NO inventes contexto. NO asumas decisiones. NO trates documentos históricos como fuente de verdad.

---

**Fin del documento de continuidad.**