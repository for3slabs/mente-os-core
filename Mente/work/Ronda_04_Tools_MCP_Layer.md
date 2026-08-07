# Ronda 4 — Tools / MCP Layer (Master)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Cuarta de las 10 rondas técnicas. Documento maestro de R4.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-06
**Última actualización:** 2026-06-06
**Estatus:** ✅ **R4 v1 CERRADO 100%** (Bloques 1-3 LOCKED · Bloque 4 DIFERIDO v2)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — §4 Nodo 4 Ganglios Basales/Skills (R4 da el Tool Bus = infraestructura de ejecución del Nodo 4)
- [Mente/Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md](../Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md) — Nodo 4 mapeo
- [Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md](Ronda_03_Model_LLM_Layer.md) — R3 100% CERRADO (foundation tools)
- [Mente/Doc/Estado_Sesion_Continuidad.md](memory/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Sub-documentos detallados:**
- ✅ [Ronda_04_Bloque_1_MCP_Framework_Discovery.md](Ronda_04_Bloque_1_MCP_Framework_Discovery.md) — MCP Framework & Discovery (4/4 LOCKED)
- ✅ [Ronda_04_Bloque_2_MCP_Servers_Core.md](Ronda_04_Bloque_2_MCP_Servers_Core.md) — MCP Servers Core (4/4 LOCKED)
- ✅ [Ronda_04_Bloque_3_Tool_Lifecycle.md](Ronda_04_Bloque_3_Tool_Lifecycle.md) — Tool Lifecycle (3/3 LOCKED) ⭐ CIERRA R4 v1
- ⏳ Ronda_04_Bloque_4_Multi_Domain_Expansion.md (DIFERIDO v2)

**Decisiones loggeadas en for3s-inter:**
- [D-016 — Stack MCP Framework & Discovery LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-017 — Stack MCP Servers Core LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-018 — Stack Tool Lifecycle LOCKED + R4 v1 100% CERRADO](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño (preferir simplicidad operacional)

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes
- P3 — Workspace isolation
- P4 — Encryption at rest

---

## Tabla de contenidos

1. [Propósito de R4](#1-propósito-de-r4)
2. [Pre-preguntas P1-P3 LOCKED](#2-pre-preguntas-p1-p3-locked)
3. [Aclaración arquitectónica](#3-aclaración-arquitectónica)
4. [Estructura B+A — 4 bloques · ~11 sub-temas](#4-estructura-ba--4-bloques--11-sub-temas)
5. [Resumen ejecutivo Bloque 1 — MCP Framework & Discovery](#5-resumen-ejecutivo-bloque-1--mcp-framework--discovery)
6. [Status Bloques 2, 3, 4](#6-status-bloques-2-3-4)
7. [Cobertura del Grafo Maestro](#7-cobertura-del-grafo-maestro)
8. [Costo total v1 actualizado (post-R4 B1)](#8-costo-total-v1-actualizado-post-r4-b1)
9. [Spillovers hacia for3s-inter/](#9-spillovers-hacia-for3s-inter)
10. [Próximo paso](#10-próximo-paso)

---

## 1. Propósito de R4

R4 — Tools / MCP Layer define las **MANOS del agente For3s OS**. Es donde el agente deja de "solo razonar" y empieza a "actuar en el mundo real".

### Lo que R4 materializa del Grafo Maestro

```
   ╔══════════════════════════════════════════════════════════╗
   ║   PIEZAS DEL GRAFO MAESTRO ATERRIZADAS EN R4              ║
   ║                                                          ║
   ║   • Tool Bus — infraestructura de EJECUCIÓN de tools     ║
   ║     (NO es un nodo cerebral numerado; es el sustrato      ║
   ║      sobre el que el Nodo 4 Ganglios Basales/Skills       ║
   ║      ejecuta acciones en el mundo real)                   ║
   ║   • Nodo 4 — Ganglios Basales / Skills (R4 da las MANOS;  ║
   ║     las skills auto-generadas las cierra R6 B2)           ║
   ║   • Nodo 3 — PFC (orquesta tool calls)                    ║
   ║   • Pilar 1 — Seguridad E2E (containers + secrets)        ║
   ║   • Pilar 2 — Escalabilidad por nodo (Docker isolation)   ║
   ║   • Pilar 3 — Autonomía Generativa (tools extensibles)    ║
   ╚══════════════════════════════════════════════════════════╝

   > ⚠️ NOTA NUMERACIÓN (reconciliada 2026-06-09): versiones previas de
   > este doc decían "Nodo 4 = Cuerpo Calloso" y "Nodo 2 = Cerebelo".
   > Esos nombres NO existen en el Grafo Maestro. Numeración canónica
   > (Grafo Maestro = Visión §6.1): Nodo 2 = Hipocampo, Nodo 4 = Ganglios
   > Basales/Skills. El "Tool Bus" es infraestructura del Nodo 4, no un
   > nodo aparte. Ver Mapeo_Nodo_Cerebral_Tabla_SQL.md §0.
```

### Relación con R1-R3

- **R1** Compute/Lenguaje (Python 3.12 + asyncio + anyio + FastAPI + Pydantic v2)
- **R2** Data Layer (PostgreSQL + Valkey + memory tiers + backup) — 100% CERRADO
- **R3** Model/LLM Layer (Claude Sonnet/Opus + caching + streaming + observability + eval) — 100% CERRADO
- **R4** Tools/MCP Layer (MCP framework + Docker multi-tenant + secrets) — EN CURSO

R4 sin R1-R3 = manos sin cuerpo.
R1-R3 sin R4 = cuerpo sin manos (solo puede hablar, no actuar).

---

## 2. Pre-preguntas P1-P3 LOCKED

Antes de los sub-temas técnicos, R4 abrió con 3 preguntas contextuales que definieron el espacio de soluciones.

### P1 — MCP servers v1 ✅ LOCKED (revisado)

```
GitHub + Filesystem + HTTP + Telegram (compromise)
   • GitHub: wedge QA primario
   • Filesystem: file ops universal
   • HTTP/Fetch: web access universal (research, scraping, APIs sin SDK)
   • Telegram bot: Brian comm personal + foundation R7
   • Slack y otros: defer a R4 v2 cuando llegue cliente enterprise específico
```

**Razón compromise:** balance entre time-to-revenue (GitHub para QA wedge) + foundation universal (Filesystem + HTTP) + canal interacción Brian (Telegram). Slack defer porque pertenece más a R7 Frontend.

### P2 — MCP hosting v1 ✅ LOCKED

```
LOCAL primero, cloud opcional v2
   • v1 todos LOCAL en servidor Brian (D-009)
   • Código diseñado abstraction-aware
   • Cuando v2 necesario, mover sin reescribir (solo cambiar config)
   • Cumple D-009 LOCAL + compliance B2B máximo
```

### P3 — Tool authorization v1 ✅ LOCKED

```
Permission + whitelist + human-in-loop opcional
   • Tools NO sensibles: ejecutan directo (whitelist allowed_tools)
   • Tools SENSIBLES (require_confirmation=True): pausan agente
     → Envían Telegram a Brian/usuario para aprobar
     → Timeout 5 min → rechazo automático
   • Foundation enterprise B2B (compliance valora esto)
   • Defendible auditoría (cada acción aprobada loggeada)
```

---

## 3. Aclaración arquitectónica

Durante R4 Bloque 1, Brian introdujo un constraint comercial crítico:

```
"Clientes quieren seguridad y privacidad"
```

Esto pivoteó la arquitectura hosting de systemd simple a **Docker Multi-tenant 3 capas** con container exclusivo per cliente. La decisión fue:

```
NO usar Kubernetes v1 (over-engineering masivo):
   • 8 semanas setup vs 3-4 días Docker
   • 3 GB RAM overhead vs 500 MB Docker
   • NO da más security/privacy que Docker
   • Cliente enterprise NO lo exige hoy
   • Brian solo: K8s requires equipo SRE

SÍ usar Docker con multi-tenant pattern:
   • Container per cliente = aislamiento físico real
   • Tools compartidos stateless = recursos eficientes
   • 3-layer isolation (DB + container + network) = compliance pitch
   • BYOC enabled = diferenciador venta enterprise
   • K8s-ready foundation (8 best practices Dockerfile)
   • Migration K8s futura: 2 semanas vs 8 si empiezas K8s ahora
```

Aplica retroactivamente: R4 Bloque 1 sienta foundation comercial — wedge QA + foundation universal + canal interacción + compliance B2B defendible.

---

## 4. Estructura B+A — 4 bloques · ~11 sub-temas

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 1 — MCP FRAMEWORK & DISCOVERY (4 sub-temas) ✅ LOCKED ║
║   ────────────────────────────────────────────────             ║
║   4.1.1 MCP client framework selection                          ║
║   4.1.2 Tool discovery / registration runtime                   ║
║   4.1.3 MCP server hosting (Docker multi-tenant)                 ║
║   4.1.4 Tool authentication & secrets management                 ║
║                                                                  ║
║   BLOQUE 2 — MCP SERVERS CORE (4 sub-temas) ⏳ Pendiente        ║
║   ─────────────────────────────────────────────                  ║
║   4.2.1 GitHub MCP server (wedge QA primary)                     ║
║   4.2.2 Filesystem MCP server                                    ║
║   4.2.3 HTTP/Fetch MCP server (web access)                       ║
║   4.2.4 Telegram bot integration                                 ║
║                                                                  ║
║   BLOQUE 3 — TOOL LIFECYCLE (3 sub-temas) ⏳ Pendiente           ║
║   ────────────────────────────────────────                       ║
║   4.3.1 Tool authorization workflows (human-in-loop, dry-run)    ║
║   4.3.2 Tool versioning + rollback                                ║
║   4.3.3 Tool testing & sandbox                                    ║
║                                                                  ║
║   BLOQUE 4 — MULTI-DOMAIN EXPANSION (3 sub-temas) ⏳ DEFER v2    ║
║   ────────────────────────────────────────────────                ║
║   4.4.1 Slack/Notion MCP servers                                  ║
║   4.4.2 Google Drive/Calendar MCP servers                         ║
║   4.4.3 Health/Finance/Legal MCP servers per dominio              ║
║                                                                  ║
║   TOTAL R4 v1: Bloques 1-3 (~11 sub-temas)                       ║
║   Bloque 4 defer a R4 v2 cuando wedge QA esté maduro              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

### Modo operativo B+A

Mismo patrón que R2 y R3: bloques temáticos con sub-temas explícitos. Cada sub-tema sigue estructura ⑦ con profundidad R2 (contexto, mapeo, 5 candidatos, tabla comparativa, casos de uso, recomendación, decisión).

---

## 5. Resumen ejecutivo Bloque 1 — MCP Framework & Discovery

**Documento detallado:** [Ronda_04_Bloque_1_MCP_Framework_Discovery.md](Ronda_04_Bloque_1_MCP_Framework_Discovery.md)

### Las 4 decisiones LOCKED

```
4.1.1 MCP client framework        → mcp Python SDK oficial Anthropic
4.1.2 Tool discovery               → Híbrido A+C (static + 5 triggers event-driven)
4.1.3 MCP server hosting           → Docker Multi-tenant 3 capas
4.1.4 Tool authentication+secrets  → PostgreSQL encrypted + KEK hierarchy
```

### Filosofía emergente del Bloque 1

```
"Foundation aislada y defendible. Los 4 sub-temas convergen
en una arquitectura multi-tenant donde cada cliente tiene
container propio, secrets cifrados con KEK derivada, tools
compartidos stateless con audit per-uso, y hot-reload
event-driven sin downtime."

   • mcp SDK OFICIAL (4.1.1)
   • DISCOVERY HÍBRIDO A+C (4.1.2)
   • MULTI-TENANT DOCKER (4.1.3)
   • SECRETS ENCRYPTED + KEK (4.1.4)
```

### Stack final consolidado Bloque 1

```
PYTHON LIBRARIES (nuevas R4 B1):
   • mcp >=1.0,<2.0 (MIT, MCP SDK oficial Anthropic)
   • cryptography (BSD, AES-256-GCM + HKDF)
   • watchfiles (MIT, file watcher hot-reload)

ARQUITECTURA DOCKER 3 CAPAS:
   • Capa 1 systemd (host): PostgreSQL + Valkey + Prometheus + Docker daemon
   • Capa 2 containers compartidos:
     - For3s core: for3s-api, for3s-arq, for3s-orchestrator
     - MCP tools shared: mcp-github, mcp-filesystem, mcp-http, mcp-telegram
   • Capa 3 containers exclusivos per cliente:
     - workspace-{cliente} con volumes + secrets + memory privados

NETWORKING (4 Docker bridges):
   • for3s-public-net: único entry externo
   • for3s-core-net: internal core services
   • for3s-mcp-net: internal MCP tools
   • workspace-{cliente}-net: aislamiento per cliente

AISLAMIENTO 3 NIVELES:
   • Lógico: schema per workspace en PostgreSQL (R2 B1)
   • Físico: container Docker per cliente (NEW R4)
   • Red: Docker network per cliente (NEW R4)

RESOURCE QUOTAS DOCKER per tier:
   • Pilot Light: 512 MB RAM, 0.5 CPU
   • Pilot Pro: 2 GB RAM, 2 CPU
   • Enterprise: custom

SECRETS KEY HIERARCHY:
   • Master KEK: /etc/for3s/master_key (chmod 400)
   • Workspace KEK: HKDF-SHA256(master, workspace_id)
   • Per-secret: AES-256-GCM cifrado con workspace KEK + nonce
   • Backup OFFLINE: USB hardware + paper safe + succession plan

DISCOVERY HOT-RELOAD (5 triggers event-driven):
   1. Admin endpoint POST /admin/mcp/reload/{server}
   2. File watcher mcp_servers.yaml (watchfiles MIT)
   3. MCP push notification (list_changed spec)
   4. Workspace allowed_tools change hook
   5. Background retry exitoso auto-reload

   Sin TTL temporal (NO "reset cada rato")
   _refresh_lock asyncio.Lock anti race conditions
   Rollback automático si reload falla
   Rate limit: max 1 reload/server/10s
```

### Score honesto Bloque 1 R4

```
9.5/10 — Excelente

Fortalezas:
   • Foundation comercial sólida (3-layer isolation defendible)
   • Diferenciador enterprise B2B (BYOC + container per cliente)
   • Coherencia con R1-R3 10/10 (patterns reused)
   • Cumplimiento Anclas 10/10 (1.D + 2.B + 3.D respetadas)
   • Compliance B2B (P3 + P4 + SOC2-defendible)
   • Cost vs P2 10/10 ($0 infra incremental)
   • Future-proofing 9.5/10 (K8s-ready foundation)
   • Hot-reload sin downtime (productividad operacional)
   • Secrets defense in depth (Brian nunca ve plaintext)

Áreas de vigilancia:
   • Master KEK loss (backup discipline crítico)
   • Cardinality Docker networks a escala
   • Container provisioning automation requires testing
   • Multi-tenant Docker requires Brian familiarity
```

---

## 6. Status Bloques 2, 3, 4

### Bloque 2 — MCP Servers Core ✅ LOCKED 2026-06-06

**Documento detallado:** [Ronda_04_Bloque_2_MCP_Servers_Core.md](Ronda_04_Bloque_2_MCP_Servers_Core.md)

**Las 4 decisiones LOCKED:**

```
4.2.1 GitHub MCP       → A) Oficial Anthropic (@modelcontextprotocol/server-github)
4.2.2 Filesystem MCP   → B) Custom Python (FastMCP) con permission model
4.2.3 HTTP MCP         → B) Custom Python con SSRF 5-capa
4.2.4 Telegram MCP     → B) Custom Python (PTB) + patrones Hermes adaptados
```

**Filosofía emergente:**

> "Composición sobre reinvención. Tools donde comunidad MCP ya hizo el trabajo (GitHub): usar oficial. Tools donde aislamiento multi-tenant, security crítico, o lógica For3s-specific son requirements (Filesystem, HTTP, Telegram): construir custom Python con FastMCP y reusar learnings probados en producción (Hermes patterns)."

**Principio Arquitectónico LOCKED VALIDADO 3 VECES:**
- 1 oficial (GitHub) — tool madura comunidad
- 3 custom Python (Filesystem, HTTP, Telegram) — niche/For3s-specific

**Tools concretas habilitadas (~57 total):**
- GitHub MCP (oficial): 26 tools
- Filesystem MCP (custom): 12 tools
- HTTP MCP (custom): 6 tools
- Telegram MCP (custom + Hermes): 8 tools
- Core LOCAL (B2 3.2.4): 5 tools

**Patrones Hermes reusados en Telegram (7):**
1. PlatformAdapter ABC (foundation R7 multi-canal)
2. GatewayRunner FastAPI (webhook handler)
3. NormalizedMessage (agente NO acoplado al canal)
4. Authorize pattern
5. Session persistence (adapted Postgres)
6. Cross-platform user linking foundation v2
7. Config-driven enable

**Score honesto B2 R4:**

```
9.5/10 — Excelente

Fortalezas:
   • Principio Arquitectónico validado 3 veces
   • 1 oficial + 3 custom = composición sobre reinvención
   • Hermes patterns reusados (Telegram) = menos riesgo
   • Cumplimiento Anclas 10/10 (1.D + 2.B + 3.D)
   • Foundation R7 multi-canal gratis (PlatformAdapter ABC)
   • OWASP LLM Top 10 compliance (HTTP SSRF 5-capa)
   • Compliance B2B fuerte (path validation + signature + KEK)
   • 57 tools concretas disponibles agentes
   • Costo $0 infra (todo open source)

Áreas de vigilancia:
   • SSRF bypass novel techniques (mitigado tests + bug bounty)
   • Path traversal custom code (mitigado property-based testing)
   • Master KEK loss critical (B1 reused mitigation)
   • PAT cliente expire (mitigado auto-rotation)
```

### Bloque 3 — Tool Lifecycle ✅ LOCKED 2026-06-06 ⭐ CIERRA R4 v1

**Documento detallado:** [Ronda_04_Bloque_3_Tool_Lifecycle.md](Ronda_04_Bloque_3_Tool_Lifecycle.md)

**Las 3 decisiones LOCKED:**

```
4.3.1 Authorization workflows  → B) 7 capacidades coordinadas
4.3.2 Versioning + rollback    → A) SemVer + Docker SHA + workspace config
4.3.3 Testing & sandbox         → A) Framework 5 capas
```

**Filosofía emergente:**

> "Disciplina operacional como diferenciador comercial. La diferencia entre 'wrapper de Claude bonito' y 'plataforma enterprise SOC2-defendible' está en cómo se gobiernan, versionan y testean las tools. B3 es el bloque que cierra ese gap."

**Patrones clave:**
- Authorization 7 capacidades (policies + dry-run + roles + remember + revocation + break-glass + dashboard)
- 4 decisiones per policy: auto_approve, auto_reject, require_approval, block
- 3 defaults secure-by-default workspace onboarding
- Versioning SemVer + Docker SHA + workspace pinning
- 4 release channels: stable / beta / canary / exact
- Multi-version containers concurrentes + cleanup cron 90d
- Rollback manual v1, automatic v2, blue-green v3
- Deprecation 3 fases: 30d soft + 15d hard + removal
- Testing 5 capas (unit + integration + E2E + sandbox + eval B4 3.4.3)
- Coverage: 85% custom, 70% wrappers, 100% security paths
- Shadow services LOCKED (GitHub org + Telegram bot + filesystem sandbox + httpbin)
- Workspace sandbox tier (free, opt-in, 1/cliente, $5 hard cap)
- CI/CD GitHub Actions foundation R10

**Foundation entregada a R5-R10:**
- R5 Orchestration: 57 tools + governance + versioning + testing ready
- R6 Memory: filesystem indexable + telegram conversations + versioning audit
- R7 Frontend: approval dashboard + sandbox dashboard + version selection UI
- R8 Observability: ~18 métricas nuevas B3 (~60 total R4)
- R9 Security/Compliance: OWASP LLM Top 10 + SOC2 path defendible
- R10 CI/CD: testing framework + SHA pinning + sandbox pre-prod ready

**Score honesto B3 R4:**

```
9.5/10 — Excelente

Fortalezas:
   • 7 capacidades authorization coordinadas
   • SemVer + SHA inmutabilidad audit
   • 5 capas testing + sandbox + eval integration
   • Coverage targets estrictos
   • Foundation R10 CI/CD natural
   • Compliance SOC2 defendible
   • Cliente self-service (sandbox, versions, policies)
   • Reusa stack completo (Telegram, Postgres, Arq, Jinja2)
   • Cumple Anclas 10/10 (3/3 respetadas)

Áreas de vigilancia:
   • Authorization complexity (7 capacidades)
   • Multi-version RAM (~1.6 GB extra)
   • Tests flaky CI requires discipline
   • Eval framework B4 3.4.3 integration crítico
```

---

## R4 v1 — STATUS FINAL POST-B3

```
╔══════════════════════════════════════════════════════════════╗
║   ✅✅✅ R4 v1 — TOOLS/MCP LAYER 100% CERRADO ✅✅✅            ║
║                                                                ║
║   Bloque 1 ✅ LOCKED (4/4) — D-016                              ║
║   Bloque 2 ✅ LOCKED (4/4) — D-017                              ║
║   Bloque 3 ✅ LOCKED (3/3) — D-018 ⭐ CIERRA R4 v1               ║
║   Bloque 4 ⏳ DIFERIDO v2                                       ║
║                                                                  ║
║   TOTAL: 11/11 sub-temas LOCKED (100%)                          ║
╚══════════════════════════════════════════════════════════════╝
```

### Bloque 4 — Multi-Domain Expansion ⏳ DIFERIDO v2

**Estatus:** ⏳ DEFER R4 v2. NO se debate en R4 v1.

**Razón diferimiento:** wedge QA es el foco v1. Slack/Notion/Google/Health/Finance/Legal MCP servers tienen sentido cuando llegue cliente enterprise específico que los requiera. Foundation Multi-tenant Docker (B1) + Principio Arquitectónico LOCKED (B2 4.2.1 PARTE 2) + Hermes PlatformAdapter ABC (B2 4.2.4) ya permite agregar nuevos MCP servers sin tocar lo existente.

**Triggers reconsiderar B4 v2:**
- >10 pilots activos
- Cliente enterprise pide integración específica
- Wedge QA maduro y validado
- Multi-dominio activo (salud, finanzas, legal)

### Bloque 4 — Multi-Domain Expansion ⏳ DEFER v2

**Estatus:** ⏳ DIFERIDO a R4 v2. NO se debate en R4 v1.

**Razón diferimiento:** wedge QA es el foco v1. Slack/Notion/Google/Health MCP servers tienen sentido cuando llegue cliente enterprise específico que los requiera. Foundation Multi-tenant Docker ya permite agregar nuevos MCP servers sin tocar lo existente.

**Trigger reconsiderar v2:**
- >10 pilots activos
- Cliente enterprise pide integración específica
- Wedge QA maduro y validado

---

## 7. Cobertura del Grafo Maestro

### Nodos servidos por R4 (incluyendo bloques futuros)

```
NODO                                BLOQUE 1   BLOQUE 2   BLOQUE 3
──────────────────────────────────────────────────────────────────
Tool Bus (infra del Nodo 4)         ✅ infra   ✅ servers ✅ lifecycle
Nodo 4 Ganglios Basales/Skills      🟡 found   🟡 found    🟡 (skills cierran R6)
Nodo 3 PFC (Orchestrator)            ✅ secrets ✅ inject   ✅ approve
Nodo 8 Tálamo (router R5)            🟡 found   —           —

R4 da el Tool Bus = infraestructura de ejecución del Nodo 4 Ganglios Basales.
Las Skills auto-generadas (Nodo 4) son foundation aquí; cierran en R6 B2.
(Numeración canónica: Nodo 4 = Ganglios Basales/Skills. Ver Mapeo §0.)
```

### Pilares — Cobertura por R4

```
Pilar 1 — Seguridad E2E
   ✅ Container per cliente (B1 4.1.3) aislamiento físico
   ✅ Network per cliente (B1 4.1.3) red aislada
   ✅ Secrets cifrados KEK hierarchy (B1 4.1.4)
   ✅ Audit per-secret-usage (B1 4.1.4)
   ✅ Permission model granular (B2 3.2.4 reused)
   ⏳ Human-in-loop approvals (B3 4.3.1)
   ⏳ Tool versioning + audit (B3 4.3.2)

Pilar 2 — Escalabilidad por nodo
   ✅ Resource quotas Docker per tier (B1 4.1.3)
   ✅ Tools compartidos stateless (B1 4.1.3)
   ✅ Hot-reload sin downtime (B1 4.1.2)
   ⏳ Tools concretas escalan independiente (B2)

Pilar 3 — Autonomía Generativa
   ✅ MCP tools extensibles (B1 4.1.1)
   ✅ Discovery dinámico (B1 4.1.2)
   ⏳ Tools agregan sin código (B2-B3)
   ⏳ Meta-Orchestrator activa tools nuevas v3+
```

### Anclas LOCKED — Status post-R4 B1

```
1.D Dedicated SaaS  ✅ container per cliente + tier quotas
2.B Open Core       ✅ SDKs abiertos (mcp MIT, cryptography BSD, watchfiles MIT)
3.D Equipo pequeño  ✅ Docker simplicidad + hot-reload + scripts automation
```

---

## 8. Costo total v1 actualizado (post-R4 B1)

```
Hardware Linux LOCAL Brian:                   USD 0
Electricidad servidor 24/7:                   USD ~5/mes
Cloudflare Tunnel + R2:                       USD 0 (free tier)
Dominio for3s.ai:                             USD ~$1/mes
PostgreSQL + AGE + pgvector + pgcrypto:       USD 0
Custom memory + Stella + HDBSCAN:             USD 0
Valkey + Arq + pgbouncer:                     USD 0
asyncio + anyio + librerías pool:             USD 0
Backup tools:                                  USD 0
OpenAI fallback embeddings:                   USD <1/mes
Claude Haiku 4.5 (CLS, R2):                    USD ~37/mes
Claude Sonnet 4.6 (principal R3 B1):           USD ~50/mes
Caching maduro saving (R3 B2):                 USD ~-31/mes
Tool overhead (R3 B2):                          USD ~+6/mes
Resilience saving (R3 B3):                      USD ~-5-10/mes
Claude Haiku eval (R3 B4):                      USD ~5-15/mes
─────────────────────────────────────────────────────────────
SUBTOTAL R1+R2+R3 100%:                       USD ~62-77/mes

R4 BLOQUE 1 INCREMENTAL:
Docker daemon + cryptography + watchfiles:    USD 0 (todo open source)
mcp SDK oficial:                                USD 0 (MIT)
PostgreSQL secrets table:                       USD 0 (ya en stack)
─────────────────────────────────────────────────────────────
TOTAL v1 (post-R4 B1):                         USD ~62-77/mes (sin cambio)
```

### Vs constraint P2 <25% pilot revenue

```
Pilot Light USD 3,500 (3 semanas)
   Techo AI+infra: USD 875 (25%)
   Consumo v1 (3 sem): USD ~55
   → 6.3% del techo
   → MARGEN 93.7% disponible para R4 B2+B3 + R5-R10

Pilot Pro USD 8,000 (3 semanas)
   Techo: USD 2,000
   Consumo v1: USD ~55
   → 2.8% del techo
   → MARGEN 97.2%
```

### Recursos servidor R4 B1

```
RAM:
   Docker daemon: ~500 MB
   4 MCP containers shared (200 MB cap each): ~800 MB
   N workspace containers (per tier):
      • Pilot Light: 512 MB cada
      • Pilot Pro: 2 GB cada
   Secrets crypto cache: <50 MB
   
TOTAL R4 B1 base: ~1.5 GB + scaling per workspace

Capacidad servidor Brian (30 GB RAM):
   ~40 workspaces Pilot Light simultáneos
   ~10 workspaces Pilot Pro simultáneos
   Suficiente para v1 (3-5 pilots → 20-30 clientes total)
```

---

## 9. Spillovers hacia for3s-inter/

Aplicando **Protocolo Bidireccional** (Estado_Sesion §3.1.quater):

### Spillovers escritos al cerrar Bloque 1 R4 (2026-06-06)

```
✅ for3s-inter/07-operations/decision-log.md
   + D-016 (Stack MCP Framework & Discovery LOCKED)

✅ Mente/Cuerpo/Ronda_04_Tools_MCP_Layer.md (este master)
✅ Mente/Cuerpo/Ronda_04_Bloque_1_MCP_Framework_Discovery.md (detallado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.quaterdecies
```

### Spillovers escritos al cerrar Bloque 2 R4 (2026-06-06)

```
✅ for3s-inter/07-operations/decision-log.md
   + D-017 (Stack MCP Servers Core LOCKED)

✅ Mente/Cuerpo/Ronda_04_Bloque_2_MCP_Servers_Core.md (detallado)
✅ Mente/Cuerpo/Ronda_04_Tools_MCP_Layer.md (este master actualizado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.quindecies
```

### Spillovers escritos al cerrar Bloque 3 R4 (2026-06-06) ⭐ CIERRA R4 v1

```
✅ for3s-inter/07-operations/decision-log.md
   + D-018 (Stack Tool Lifecycle LOCKED + R4 v1 100% CERRADO)

✅ Mente/Cuerpo/Ronda_04_Bloque_3_Tool_Lifecycle.md (detallado)
✅ Mente/Cuerpo/Ronda_04_Tools_MCP_Layer.md (este master 100% CERRADO)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.sedecies
✅ for3s-inter/09-technical-architecture/tools-mcp-layer.md (sub-doc consolidado)
✅ 3 sub-docs públicos R4:
   • mcp-framework-discovery.md (R4 B1)
   • mcp-servers-core.md (R4 B2)
   • tool-lifecycle.md (R4 B3)
✅ for3s-inter/09-technical-architecture/README.md (R4 → ✅ v1 CERRADO 100%)
✅ for3s-inter/02-product/mvp-scope.md (Tools stack annotation FINAL)
✅ for3s-inter/05-finance/unit-economics.md (refresh costo total FINAL)
```

### Spillovers DIFERIDOS hasta cierre R4 completo

```
⏳ for3s-inter/09-technical-architecture/tools-mcp-layer.md
   (sub-doc dedicado público-formal, mejor visión holística)

⏳ Actualizar for3s-inter/09-technical-architecture/README.md
   (sección R4 cuando cierre completo Bloques 1-3)

⏳ Actualizar for3s-inter/02-product/mvp-scope.md
   (Tools stack annotation final)

⏳ Actualizar for3s-inter/05-finance/unit-economics.md
   (refresh recursos servidor post-R4)
```

Razón del diferimiento: decisiones de Bloques 2-3 informarán docs públicos. Patrón replicado de R2 + R3 (sub-docs por bloque internos, doc público al cierre ronda completa).

---

## 10. Próximo paso

**R4 v1 100% CERRADO** — los 3 bloques operativos LOCKED, 11/11 sub-temas, 3 decisiones (D-016, D-017, D-018). B4 Multi-Domain Expansion diferido v2.

**FASE 2 cierre formal EJECUTADA:**
- ✅ `../for3s-inter/09-technical-architecture/tools-mcp-layer.md` (sub-doc consolidado público)
- ✅ 3 sub-docs públicos R4 por bloque
- ✅ `../for3s-inter/09-technical-architecture/README.md` (R4 → ✅ v1 CERRADO 100%)
- ✅ `../for3s-inter/02-product/mvp-scope.md` (Tools stack annotation FINAL)
- ✅ `../for3s-inter/05-finance/unit-economics.md` (costo total FINAL)

**Después de cierre R4 v1:**
- Iniciar **R5 — Orchestration / Multi-Agent** (siguiente ronda)
  - Foundation lista: 57 tools + AgentDelegationTool + Telegram bidireccional + Container workspace per cliente
  - Decisiones a tomar: Nodo 8 Tálamo router + Nodo 9 Dual-Process Check + Multi-Agent lifecycle