# Ronda 4 — Bloque 1: MCP Framework & Discovery

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_04_Bloque_1_MCP_Framework_Discovery.md → work/Ronda_04_Bloque_1_MCP_Framework_Discovery.md (2026-07-30, ADR-029)

## Purpose

Ronda 4 — Bloque 1: MCP Framework & Discovery


**Sub-documento detallado de R4 — Tools/MCP Layer. Bloque 1 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-06
**Estatus:** ✅ LOCKED (4/4 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema con profundidad R2)
**Documento padre:** [Ronda_04_Tools_MCP_Layer.md](work/Ronda_04_Tools_MCP_Layer.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes
- P3 — Workspace isolation (schema + container + network)
- P4 — Encryption at rest (AES-256-GCM)

**Pre-preguntas P1-P3 LOCKED antes del bloque:**
- P1: GitHub + Filesystem + HTTP + Telegram (compromise)
- P2: LOCAL primero, cloud opcional v2
- P3: Permission + whitelist + human-in-loop opcional

**Dependencias resueltas en R1-R3:**
- ✅ Python 3.12 + FastAPI + Pydantic v2 + asyncio + anyio (R1)
- ✅ PostgreSQL + Valkey + audit_events + Arq cron (R2)
- ✅ LLMProvider abstraction pattern (R3 B1)
- ✅ ToolRegistry + ToolExecutor + Permission model (R3 B2 3.2.4)
- ✅ Cache Layer 3 invalidación (R3 B2 3.2.3)
- ✅ Resilience taxonomy ErrorType (R3 B3 3.3.3)
- ✅ Prometheus métricas + audit chain (R3 B4 3.4.1)

**Fuente de verdad:**
- [`For3s_OS_Grafo_Maestro.md`](../Cerebro/For3s_OS_Grafo_Maestro.md) §4 Nodo 4 Cuerpo Calloso + Pilar 1 + 2 + 3

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 4.1.1 — MCP client framework](#3-sub-tema-411--mcp-client-framework)
4. [Sub-tema 4.1.2 — Tool discovery / registration](#4-sub-tema-412--tool-discovery--registration)
5. [Sub-tema 4.1.3 — MCP server hosting](#5-sub-tema-413--mcp-server-hosting)
6. [Sub-tema 4.1.4 — Tool authentication & secrets](#6-sub-tema-414--tool-authentication--secrets)
7. [Stack final consolidado](#7-stack-final-consolidado)
8. [Cobertura del Grafo Maestro](#8-cobertura-del-grafo-maestro)
9. [Costo total post-Bloque 1](#9-costo-total-post-bloque-1)
10. [Exploraciones futuras NO adoptadas v1](#10-exploraciones-futuras-no-adoptadas-v1)
11. [Implicaciones en Bloques 2-3 y rondas futuras](#11-implicaciones-en-bloques-2-3-y-rondas-futuras)
12. [Riesgos legítimos aceptados](#12-riesgos-legítimos-aceptados)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 1 — MCP FRAMEWORK & DISCOVERY                         ║
║   4 sub-temas LOCKED el 2026-06-06                             ║
║                                                                ║
║   4.1.1 MCP client framework  → mcp SDK oficial Anthropic       ║
║   4.1.2 Tool discovery         → Híbrido A+C event-driven       ║
║   4.1.3 MCP server hosting     → Docker Multi-tenant 3 capas     ║
║   4.1.4 Tool auth + secrets    → PostgreSQL encrypted + KEK      ║
║                                                                  ║
║   Foundation entregada para:                                     ║
║   • R4 Bloque 2 MCP Servers Core                                 ║
║   • R4 Bloque 3 Tool Lifecycle                                   ║
║   • R5 Orchestration / Multi-Agent                                ║
║   • R7 Frontend (for3s-api único entry)                           ║
║   • R8 Observability (métricas containers)                         ║
║   • R9 Security/Compliance (3-layer isolation + KEK)                ║
║   • R10 CI/CD (Docker compose + provisioning scripts)              ║
║                                                                  ║
║   Costo incremental B1 R4:      $0 infra (todo open source)       ║
║   Costo total v1:                ~USD 62-77/mes (sin cambio)       ║
║   % techo Pilot Light:           6.3% (margen 93.7%)               ║
║   Recursos servidor:              +1.5 GB RAM base + per workspace ║
║                                                                  ║
║   Diferenciador comercial nuevo:                                  ║
║   • Container per cliente (aislamiento físico real)               ║
║   • Secrets KEK hierarchy (Brian nunca ve plaintext)              ║
║   • Compliance B2B 3-layer defendible SOC2/ISO27001                ║
║   • BYOC enabled (workspace exportable)                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Foundation aislada y defendible. Los 4 sub-temas convergen
en una arquitectura multi-tenant donde cada cliente tiene
container propio, secrets cifrados con KEK derivada, tools
compartidos stateless con audit per-uso, y hot-reload
event-driven sin downtime."
```

Las 4 decisiones convergen en patrones consistentes:

```
1. ESTÁNDAR INDUSTRY (4.1.1)
   → mcp SDK oficial Anthropic
   → No lock-in (abstraction layer interno MCPClient Protocol)
   → Foundation custom MCP servers v2

2. DISCOVERY SIN DOWNTIME (4.1.2)
   → Static config + startup discovery (lookup O(1))
   → 5 triggers event-driven hot-reload
   → SIN TTL temporal (no "reset cada rato")
   → Anti race conditions con asyncio.Lock

3. AISLAMIENTO FÍSICO PER CLIENTE (4.1.3)
   → Docker Multi-tenant 3 capas
   → Container EXCLUSIVO per workspace
   → Networking aislado per cliente
   → BYOC + 3-layer compliance

4. SECRETS DEFENSE IN DEPTH (4.1.4)
   → Master KEK separado de Postgres
   → Workspace KEK derivada (compromise no propaga)
   → Per-secret cifrado AES-256-GCM
   → Brian NUNCA ve plaintext
   → Audit per-uso SOC2-defendible

5. INTEGRACIÓN PROFUNDA CON R3
   → Reusa ToolRegistry + Permission model (B2 3.2.4)
   → Reusa Cache Layer 3 invalidación (B2 3.2.3)
   → Reusa ErrorType taxonomy (B3 3.3.3)
   → Reusa Prometheus + audit (B4 3.4.1)
```

### Por qué esta filosofía importa

**Para Pilar 1 Seguridad:** 3-layer isolation (DB + container + network) + secrets KEK hierarchy = compliance B2B fuerte, defendible SOC2/ISO27001.

**Para Pilar 2 Escalabilidad:** Containers compartidos para tools (recursos eficientes) + container per cliente (aislamiento físico) + resource quotas per tier (capacity planning).

**Para Pilar 3 Autonomía:** MCP estándar permite agregar tools sin tocar código. Discovery dinámico habilita extensibilidad. Foundation para Skills auto-generadas (Nodo 2 Cerebelo v3+).

---

## 3. Sub-tema 4.1.1 — MCP client framework

### Decisión LOCKED

```
mcp Python SDK oficial Anthropic (>=1.0,<2.0)
```

### Contexto

MCP es un protocolo, no una library. Necesitamos código Python que:
- Hable el protocolo MCP (stdio, SSE, websocket)
- Lance/conecte MCP servers
- Maneje request/response con MCP servers
- Convierta tool schemas MCP ↔ Anthropic tool_use schema
- Integre con ToolRegistry existente (B2 3.2.4)

### Candidatos evaluados

```
A) mcp Python SDK oficial Anthropic (PyPI: `mcp`)               ✅ ELEGIDO
B) FastMCP framework                                              ⚠️ Más para servers
C) langchain-mcp-adapters                                          ❌ Lock-in LangChain
D) Custom MCP client desde cero                                    ❌ Reinventar protocolo
E) anthropic-mcp wrapper third-party                              ⚠️ Menos maduro
```

### Estructura LOCKED

```python
# pyproject.toml
[project.dependencies]
mcp = ">=1.0,<2.0"  # MCP client/server SDK oficial Anthropic

# for3s_os/llm/tools/mcp_client.py
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

class MCPClient(Protocol):
    """Abstraction layer interno — permite swap v3 sin refactor."""
    async def connect(self, config: MCPServerConfig) -> ClientSession: ...
    async def list_tools(self, server_name: str) -> list[MCPTool]: ...
    async def call_tool(self, server_name: str, tool_name: str, args: dict) -> CallToolResult: ...
    async def shutdown(self) -> None: ...

class OfficialMCPClient(MCPClient):
    """Implementación v1 usando mcp SDK oficial."""
    # ...
```

### Reglas duras LOCKED

```
✅ Library: mcp SDK oficial Anthropic (>=1.0,<2.0, MIT)
✅ Abstraction layer interno: MCPClient Protocol
✅ Wrapper MCPServerTool adapta a Tool Protocol (B2 3.2.4)
✅ Transport v1: stdio (servers LOCAL P2)
✅ Transport ready v2: SSE + websocket (config-driven)
✅ Async-first (asyncio + anyio compatible R1)
✅ Pydantic v2 para configs (consistencia stack)
✅ Lifecycle: AsyncExitStack en FastAPI startup/shutdown
✅ Naming convention: "{server}_{tool}" (github_get_pr, fs_read_file)
✅ Audit cada mcp_server_connected + mcp_tool_registered + tool_call
✅ TOOL_TIMEOUT 30s aplica a MCP calls (R2 B3 LOCKED)
✅ ErrorType mapping: MCP errors → TOOL_EXTERNAL_API / TOOL_TIMEOUT
✅ require_confirmation flag heredado (P3 LOCKED)
✅ Permission check ANTES execute (no LLM-decided, B2 3.2.4)
```

---

## 4. Sub-tema 4.1.2 — Tool discovery / registration

### Decisión LOCKED

```
Híbrido A+C optimizado:
   • Foundation A (static config + startup + workspace whitelist)
   • + 5 triggers event-driven hot-reload (sin TTL temporal)
```

### Contexto

Tenemos potencialmente ~53 tools (4 MCP servers × ~10-15 tools cada + 5 core LOCAL). Problemas:
- Context window explosion (53 tools × 50 tokens = ~2,650 tokens)
- Workspace isolation (allowed_tools per cliente)
- Schema versioning (MCP servers actualizan)
- Hot-reload sin app restart

### Candidatos evaluados

```
A) Static config + startup + per-workspace whitelist            ⚠️ Sin hot-reload
B) Dynamic runtime discovery cada request                        ❌ Latency
C) Hybrid startup + lazy load TTL                                 ⚠️ "Reset cada rato"
D) Tool-as-config files (.toml per workspace)                    📚 Foundation v2
E) AI-powered tool selection con LLM mini                         📚 Futuro v3

✅ ELEGIDO: HÍBRIDO A+C optimizado (A + 5 triggers event-driven, sin TTL)
```

### Los 5 triggers event-driven LOCKED

```
TRIGGER 1: Admin endpoint manual
   POST /admin/mcp/reload/{server}
   → Solo refresca tools de ese server
   → Otros tools siguen disponibles uninterrupted

TRIGGER 2: Config file watcher
   Brian edita mcp_servers.yaml
   → watchfiles detecta cambio
   → Refresh solo servers cambiados

TRIGGER 3: MCP server push notification
   Server expone tools/list_changed (MCP spec)
   → Cliente recibe push → refresh ese server

TRIGGER 4: Workspace allowed_tools change
   Admin agrega tool a workspace.allowed_tools
   → Solo refresh ese workspace's resolved tools
   → Layer 3 cache invalida granular

TRIGGER 5: Background MCP retry exitoso
   Server que estaba caído reconectó
   → Auto-register sus tools (sin restart)
```

### Reglas duras LOCKED

```
✅ Static config: config/mcp_servers.yaml (Pydantic validation)
✅ Startup discovery: AsyncExitStack en FastAPI startup
✅ Discovery paralelo: asyncio.gather (todos servers concurrentes)
✅ Server failure NO bloquea app (log + Arq retry)
✅ Retry strategy: [10s, 60s, 5min, 30min] luego abandon
✅ Retry abandon → notify Brian Telegram crítico
✅ Per-workspace whitelist: workspace.allowed_tools TEXT[]
✅ 5 triggers event-driven LOCKED (lista arriba)
✅ _refresh_lock asyncio.Lock anti race conditions
✅ Rollback automático si reload falla
✅ Rate limit: max 1 reload per server per 10s
✅ Layer 3 cache invalidation granular per workspace
✅ Eventually consistent (próximo request reconstruye)
✅ Audit eventos completos
✅ NO TTL temporal (explícito: no "reset cada rato")
✅ Hot-reload health check cada 60s (config hash + server liveness)
```

### Admin endpoints LOCKED

```python
POST /admin/mcp/reload/{server_name}    # refresh granular
POST /admin/mcp/reload-all              # nuclear option
GET  /admin/mcp/status                  # estado actual
```

---

## 5. Sub-tema 4.1.3 — MCP server hosting

### Decisión LOCKED

```
Docker Multi-tenant 3 capas con container per cliente
```

### Contexto

Brian aportó constraint comercial crítico: "clientes quieren seguridad y privacidad". Esto pivoteó hosting de systemd simple a Docker Multi-tenant con container exclusivo por cliente.

### Candidatos evaluados

```
A) FastAPI subprocess (mcp SDK default)                          ⚠️ Lifecycle frágil
B) systemd services independientes                                ⚠️ Foundation comercial débil
C) Docker containers Multi-tenant 3 capas                         ✅ ELEGIDO
D) supervisord externo                                              ⚠️ Redundante con systemd
E) Kubernetes                                                        ❌ Massive overkill v1
```

### Arquitectura 3 capas LOCKED

```
   ╔═══════════════════════════════════════════════════════════════╗
   ║                  SERVIDOR LINUX BRIAN (D-009)                    ║
   ║                                                                 ║
   ║  ┌─────────────────────────────────────────────────────────┐   ║
   ║  │  CAPA 1: INFRAESTRUCTURA BASE (systemd, host)            │   ║
   ║  │  • PostgreSQL  • Valkey  • Prometheus  • Docker daemon   │   ║
   ║  └─────────────────────────────────────────────────────────┘   ║
   ║                                                                 ║
   ║  ┌─────────────────────────────────────────────────────────┐   ║
   ║  │  CAPA 2: FOR3S CORE SERVICES (containers compartidos)     │   ║
   ║  │                                                            │   ║
   ║  │  • for3s-api (FastAPI)                                     │   ║
   ║  │  • for3s-arq (worker)                                      │   ║
   ║  │  • for3s-orchestrator (LLM coordinator)                    │   ║
   ║  │                                                            │   ║
   ║  │  FOR3S SHARED MCP TOOLS (containers compartidos):           │   ║
   ║  │  • mcp-github      • mcp-http                              │   ║
   ║  │  • mcp-filesystem  • mcp-telegram                          │   ║
   ║  └─────────────────────────────────────────────────────────┘   ║
   ║                                                                 ║
   ║  ┌─────────────────────────────────────────────────────────┐   ║
   ║  │  CAPA 3: CLIENT WORKSPACES (1 container por cliente)      │   ║
   ║  │                                                            │   ║
   ║  │  • workspace-acme       • workspace-pilot42                │   ║
   ║  │  • workspace-saludco    • workspace-brian                  │   ║
   ║  │  (volumes + secrets + memory privados cada uno)             │   ║
   ║  └─────────────────────────────────────────────────────────┘   ║
   ║                                                                 ║
   ╚═══════════════════════════════════════════════════════════════╝
```

### Networking 4 Docker bridges LOCKED

```
1. for3s-public-net (bridge)
   • for3s-api expone puerto al exterior (vía Cloudflare Tunnel)
   • Único punto de entrada externa

2. for3s-core-net (bridge, internal)
   • for3s-api, for3s-arq, for3s-orchestrator
   • Comunicación entre core services

3. for3s-mcp-net (bridge, internal)
   • for3s-orchestrator + 4 MCP servers
   • MCP tools NO accesibles desde exterior
   • NO accesibles desde workspace containers directo

4. workspace-{cliente}-net (bridge, internal, per cliente)
   • workspace-{cliente} + for3s-api
   • Aislamiento per cliente
   • workspace-acme NO ve workspace-pilot42

REGLA DE ORO:
   Workspace containers SOLO hablan con for3s-api
   For3s-api orquesta todo lo demás
   MCP tools NUNCA expuestos al workspace directo
```

### Aislamiento 3 niveles LOCKED

```
1. AISLAMIENTO LÓGICO (DB):
   Schema separado en PostgreSQL per cliente (P3 LOCKED R2 B1)

2. AISLAMIENTO FÍSICO (CONTAINERS):
   Cada cliente tiene su container Docker exclusivo
   Si comprometen container, no ven los demás

3. AISLAMIENTO DE RED (DOCKER):
   Cada workspace tiene su network Docker
   Cliente A NO contacta cliente B a nivel red
```

### Resource quotas LOCKED per tier

```
Pilot Light:  512 MB RAM, 0.5 CPU, 10 GB disco
Pilot Pro:    2 GB RAM, 2.0 CPU, 50 GB disco
Enterprise:   custom (negociable per cliente)

Servidor Brian (30 GB RAM, 1 TB disco):
   ~40 workspaces Pilot Light simultáneos
   ~10 workspaces Pilot Pro simultáneos
   Suficiente v1 (3-5 pilots → 20-30 clientes)
```

### K8s-ready Docker (8 best practices LOCKED)

```
✅ HEALTHCHECK formal (HEALTHCHECK instruction)
✅ Imágenes pinned a SHA (no :latest)
✅ Configs via env vars + secrets explícitos
✅ Resource limits compose
✅ Logs a stdout/stderr (12-factor)
✅ Stateless containers (state en volumes)
✅ Multi-stage Dockerfiles (small images)
✅ Non-root user en container

= "K8s-ready Docker" sin pagar el costo K8s hoy
```

### Provisioning scripts LOCKED

```bash
provision_workspace.sh    # ~30s onboarding cliente nuevo
deprovision_workspace.sh  # kill switch físico
backup_workspace.sh       # per cliente
migrate_workspace_tier.sh # upgrade en segundos
```

### Reglas duras LOCKED

```
✅ Hosting: Docker containers (no systemd para tools)
✅ Arquitectura: Multi-tenant 3 capas
✅ Networking: 4 Docker bridges aislados
✅ Aislamiento 3 niveles (lógico DB + físico container + red Docker)
✅ Resource quotas Docker per tier
✅ Provisioning scripts automáticos
✅ MCP tools COMPARTIDOS (stateless multi-tenant)
✅ K8s-ready Docker (8 best practices)
✅ BYOC enabled: workspace containers exportables
✅ Compliance pitch: 3-layer isolation defendible
✅ Diagrama detallado DEFER fase implementación
✅ NO Kubernetes v1 (triggers objetivos defer v3+)
```

---

## 6. Sub-tema 4.1.4 — Tool authentication & secrets

### Decisión LOCKED

```
PostgreSQL encrypted secrets + Workspace KEK hierarchy
```

### Contexto

Cada MCP tool necesita autenticarse contra APIs externas. Cada workspace tiene secrets distintos. Compliance B2B exige:
- Brian NO ve secrets cliente
- Audit per-uso defendible SOC2
- Rotation cliente self-service
- Kill switch elimina secrets físicamente

### Candidatos evaluados

```
A) Env vars container per workspace (.env files)                  ⚠️ Compliance fail
B) PostgreSQL encrypted secrets table + workspace KEK             ✅ ELEGIDO
C) HashiCorp Vault external service                                ❌ Overkill v1
D) Docker secrets nativo (swarm)                                    ⚠️ Requires Swarm
E) Cloud SecretsManager (AWS/GCP)                                  ❌ Viola D-009 LOCAL
```

### Key hierarchy LOCKED

```
   MASTER KEK (en /etc/for3s/master_key, AES-256)
      │
      ├── deriva → Workspace KEK acme (HKDF-SHA256 + workspace_id)
      │       └── cifra → secrets acme en Postgres
      │
      ├── deriva → Workspace KEK pilot42
      │       └── cifra → secrets pilot42
      │
      └── deriva → Workspace KEK for3s_shared
              └── cifra → secrets compartidos (Anthropic API, etc.)

   Si master KEK rota → re-derivar todas las workspace KEKs
   Si workspace KEK rota → re-cifrar solo sus secrets
```

### Schema SQL LOCKED

```sql
CREATE TABLE shared.workspace_secrets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES shared.workspaces(id),
    secret_name TEXT NOT NULL,           -- 'github_token', 'openai_key'
    encrypted_value BYTEA NOT NULL,       -- AES-256-GCM cifrado
    nonce BYTEA NOT NULL,                 -- nonce per encrypt
    kek_version INTEGER NOT NULL,         -- para rotation
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    rotation_reminder_days INTEGER DEFAULT 90,
    UNIQUE (workspace_id, secret_name)
);

CREATE TABLE shared.secret_usage_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret_id UUID NOT NULL REFERENCES shared.workspace_secrets(id),
    used_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    used_by_container TEXT NOT NULL,      -- 'mcp-github', 'mcp-http'
    used_for_tool TEXT,                    -- 'github_get_pr'
    request_id UUID,
    audit_event_id UUID REFERENCES audit_events(id)
);
```

### Per-request flow LOCKED

```
1. Cliente Acme hace request al for3s-api
2. for3s-api enruta a workspace-acme container
3. workspace-acme procesa, decide llamar GitHub tool
4. workspace-acme → for3s-orchestrator: "ejecuta github_get_pr"
5. for3s-orchestrator:
   a. SecretsManager.get(workspace_id='acme', name='github_token')
   b. Lookup Postgres → encrypted_value + nonce
   c. Derive workspace_kek_acme = HKDF(master_kek, 'acme')
   d. plaintext = AES-256-GCM decrypt(encrypted, workspace_kek, nonce)
   e. Audit: secret_used by mcp-github for github_get_pr
6. for3s-orchestrator inyecta token en MCP call
7. mcp-github usa token, ejecuta API call GitHub
8. plaintext token NUNCA almacenado, solo memoria milisegundos
```

### Master KEK backup LOCKED

```
CRITICAL: si Brian pierde master_key → ALL secrets perdidos

Estrategia:
• Backup #1: USB hardware (Brian custodia, encrypted passphrase)
• Backup #2: paper print en safe (Shamir's Secret Sharing si compliance)
• Backup #3: clave familiar de confianza (succession plan)

NO backup en cloud (defeats LOCAL purpose)
NO backup junto al servidor (single point of failure)
```

### Reglas duras LOCKED

```
✅ Storage: PostgreSQL encrypted (shared.workspace_secrets)
✅ Encryption: AES-256-GCM con nonce random per encrypt
✅ Key hierarchy: Master + Workspace + Per-secret
✅ Master KEK: /etc/for3s/master_key (chmod 400, root)
✅ Master KEK backup OFFLINE obligatorio (USB + safe + succession)
✅ Workspace KEK: HKDF-SHA256(master, workspace_id)
✅ Library: cryptography (PyPA, BSD)
✅ Per-request flow: get() → decrypt memoria ms → use → discard
✅ Brian NUNCA ve plaintext secrets (defense in depth)
✅ Audit trail completo (secret_stored/used/rotated/deleted/expired)
✅ Cliente self-service rotation vía dashboard
✅ Auto-rotation reminders (Arq cron 7 días antes expiry)
✅ Kill switch: docker rm + DELETE FROM workspace_secrets cascade
✅ Compartidos for3s: workspace_id='for3s_shared' (admin-managed)
✅ Containers MCP NO acceden Postgres directo (reciben como params)
✅ Workspace containers NO acceden Postgres directo (vía for3s-api)
✅ Workspace KEK cache in-memory (no Valkey extra)
✅ Schema versioning kek_version (foundation rotation master)
✅ Compatible P3 + P4 + R2 B1 + 4.1.3
✅ Foundation R9 Security/Compliance estricto
```

---

## 7. Stack final consolidado

```
COMPONENTE                          DECISIÓN                              COSTO
─────────────────────────────────────────────────────────────────────────────
MCP SDK Python                       mcp >=1.0,<2.0 (MIT)                  $0
MCP transport v1                     stdio                                  $0
MCP transport ready v2               SSE + websocket                        $0
Discovery framework                   Static config + 5 triggers event-driven $0
File watcher                          watchfiles (MIT)                       $0
Hosting                               Docker containers                      $0
Multi-tenant pattern                  3 capas (infra/shared/client)          $0
Networking                            4 Docker bridges aislados              $0
Resource quotas                       Per tier (Pilot Light/Pro/Enterprise) $0
Provisioning scripts                  Bash + Python                          $0
Secrets storage                       PostgreSQL encrypted                    $0
Secrets encryption                    AES-256-GCM con cryptography (BSD)     $0
Key hierarchy                          Master + Workspace + Per-secret KEK    $0
Master KEK backup                      USB + paper safe + succession           $10 (USB único)
Per-request decrypt                    Memoria ms → discard plaintext          $0
Audit trail                            Tablas SQL nuevas + audit_events       $0
─────────────────────────────────────────────────────────────────────────────
TOTAL incremental B1 R4                                                     ~$0/mes
TOTAL v1 (R1+R2+R3 100%+R4 B1)                                            ~$62-77/mes
```

### Estructura módulo for3s_os/ extendida

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
│   │   ├── official.py             → OfficialMCPClient (usa mcp SDK)
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

### Patrones obligatorios añadidos B1 R4

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
✓ Networking aislado per cliente
✓ Resource quotas Docker per tier
✓ K8s-ready 8 best practices Dockerfile
✓ Master KEK chmod 400 + backup OFFLINE
✓ Workspace KEK HKDF derivation + cache in-memory
✓ Per-secret AES-256-GCM con nonce random
✓ Per-request decrypt memoria ms → discard
✓ Audit per-uso secret_usage_audit
✓ Cliente self-service rotation
✓ Auto-rotation reminders (Arq cron)
✓ Kill switch CASCADE delete
✓ Brian NUNCA ve plaintext (defense in depth)
✓ Compatible R3 patterns (ToolRegistry, Permission, ErrorType, Prometheus)
```

---

## 8. Cobertura del Grafo Maestro

### Nodos servidos por Bloque 1 R4

```
NODO                                STATUS POST-B1 R4
────────────────────────────────────────────────────
Nodo 4 Cuerpo Calloso (Tool Bus)    ✅ infraestructura completa
Nodo 3 PFC (Orchestrator)            ✅ orquesta tool calls + secrets
Nodo 2 Cerebelo (Skills auto v3)    🟡 foundation
Nodo 8 Tálamo (R5 routing)           🟡 foundation
```

### Pilares — Cobertura por B1 R4

```
Pilar 1 — Seguridad E2E
   ✅ Container per cliente (aislamiento físico)
   ✅ Network per cliente (aislamiento red)
   ✅ Secrets KEK hierarchy (defense in depth)
   ✅ Audit per-secret-usage SOC2-defendible
   ✅ Permission model granular (B2 3.2.4 reused)
   ✅ require_confirmation flag (P3 LOCKED)
   ✅ Brian NUNCA ve plaintext secrets
   ⏳ Human-in-loop workflows (B3 4.3.1)

Pilar 2 — Escalabilidad por nodo
   ✅ Docker containers compartidos (recursos eficientes)
   ✅ Resource quotas per tier
   ✅ Discovery hot-reload sin downtime
   ✅ Tools stateless multi-tenant
   ✅ Capacidad ~40 Pilot Light / ~10 Pilot Pro v1

Pilar 3 — Autonomía Generativa
   ✅ MCP estándar (extensibilidad protocolo)
   ✅ Discovery dinámico (agregar tools sin restart)
   ✅ Abstraction layer MCPClient (swap futuro)
   ⏳ Tools autoselect (B2 + R5)
   ⏳ Skills auto-generadas (Nodo 2 Cerebelo v3+)
```

### Anclas LOCKED — Verificación post-B1 R4

```
1.D Dedicated SaaS  ✅ container per cliente + tier quotas + workspace isolation
2.B Open Core       ✅ SDKs abiertos:
                       • mcp (MIT)
                       • cryptography (BSD)
                       • watchfiles (MIT)
                       • Docker (Apache 2.0)
                       • PostgreSQL (BSD-like)
3.D Equipo pequeño  ✅ Docker compose simplicidad
                     ✅ Hot-reload sin restart
                     ✅ Provisioning scripts automation
                     ✅ Brian conoce Docker (cero curva)
                     ✅ NO microservicios complejos
```

---

## 9. Costo total post-Bloque 1

```
COMPONENTE                                          COSTO USD/mes
─────────────────────────────────────────────────────────────────
SUBTOTAL R1+R2+R3 100%:                            ~$62-77/mes

R4 BLOQUE 1 INCREMENTAL:
   mcp SDK oficial:                                $0 (MIT)
   cryptography library:                            $0 (BSD)
   watchfiles library:                              $0 (MIT)
   Docker daemon + containers:                      $0 (Apache 2.0)
   PostgreSQL secrets table:                        $0 (ya en stack)
   Provisioning scripts:                            $0 (Bash + Python)
─────────────────────────────────────────────────────────────────
TOTAL v1 FINAL (post-R4 B1):                       ~$62-77/mes (sin cambio)
```

### Compras únicas adicionales B1 R4

```
USB hardware para Master KEK backup:    ~$10 una vez
(Brian custodia, encrypted passphrase)
```

### Recursos servidor R4 B1

```
RAM additional:
   Docker daemon: ~500 MB
   4 MCP containers shared: ~800 MB (200 MB cap each)
   Secrets crypto cache: <50 MB
   ─────────────────────────────────
   Base R4 B1: ~1.5 GB

   Per workspace container:
   • Pilot Light: 512 MB
   • Pilot Pro: 2 GB

Disco additional:
   Workspace volumes: ~10-50 GB per cliente (per tier)
   Docker images cache: ~5 GB
   Secrets DB: <100 KB per workspace

Capacidad total servidor Brian (30 GB RAM, 1 TB):
   ~40 workspaces Pilot Light simultáneos
   ~10 workspaces Pilot Pro simultáneos
   Suficiente v1 (3-5 pilots → 20-30 clientes)
```

### Verificación P2 <25% pilot revenue (FINAL post-R4 B1)

```
Pilot Light USD 3,500 (3 semanas):
   Techo: USD 875 (25%)
   Consumo v1 (3 sem): USD ~55
   → 6.3% del techo (sin cambio vs post-R3)
   → MARGEN 93.7% para R4 B2+B3 + R5-R10
```

---

## 10. Exploraciones futuras NO adoptadas v1

### 📚 Sub-tema 4.1.1 — MCP framework alternativos

```
📚 FastMCP framework
   • Cuándo: para CREAR custom MCP servers (R4 v2)
   • Como complemento de mcp SDK, no reemplazo
   • Decisión defer: si llegamos a custom servers v2

📚 LangChain-mcp-adapters
   • Cuándo: NUNCA (lock-in LangChain)

📚 Custom MCP client desde cero
   • Cuándo: NUNCA (reinventar protocolo)

📚 anthropic-mcp wrapper third-party
   • Cuándo: solo si killer feature específica aparece

📚 Migración v3 a otra library
   • Si mcp SDK evoluciona problemáticamente
   • Abstraction layer MCPClient permite swap
   • Trigger: breaking changes graves Anthropic
```

### 📚 Sub-tema 4.1.2 — Discovery alternativos

```
📚 Dynamic runtime discovery cada request
   • Cuándo: marketplace tools dinámicos
   • NO aplica For3s OS

📚 Hybrid C puro (TTL temporal)
   • Cuándo: NUNCA (Brian explícito: no "reset cada rato")

📚 Tool-as-config files .toml per workspace
   • Cuándo: v2 con >10 workspaces self-service
   • Beneficio: declarativo, git-trackable
   • Trigger: cliente pide config-as-code

📚 AI-powered tool selection (LLM mini decide)
   • Cuándo: v3 con >100 tools + Nodo 8 Tálamo R5
   • Beneficio: context window óptimo siempre

📚 Tool ranking ML
   • Cuándo: v3 con dataset histórico
   • Beneficio: prioridad tools per query type

📚 Cross-workspace tool sharing
   • Cuándo: v2 marketplace interno
   • Cliente comparte tool custom con otros
```

### 📚 Sub-tema 4.1.3 — Hosting alternativos

```
📚 systemd services puro (sin Docker)
   • Cuándo: NUNCA (perdimos compliance pitch)

📚 Docker SIN multi-tenant
   • Cuándo: dev local, MVP <3 clientes
   • Perdimos diferenciador venta

📚 Docker Swarm
   • Cuándo: v2 si necesitas multi-node sin K8s overhead
   • Migración: 1 día desde Docker compose

📚 Kubernetes
   • Cuándo: v3 con >20 clientes + equipo SRE
   • Migración: 2-4 semanas via kompose
   • Triggers objetivos:
     - >20 clientes simultáneos
     - Multi-región requerido
     - Equipo SRE dedicated
     - Cliente enterprise pide explícitamente

📚 Multi-region deployment
   • Cuándo: v3 con cliente LATAM + USA + EU
   • Implica K8s federation

📚 Container BYOC self-service portal
   • Cuándo: v3 enterprise marketplace
   • Cliente descarga workspace container

📚 Auto-scaling horizontal
   • Cuándo: v3 con tráfico real >100 req/sec
   • K8s native
```

### 📚 Sub-tema 4.1.4 — Secrets alternativos

```
📚 HashiCorp Vault
   • Cuándo: v3 con equipo SRE + compliance regulatorio
   • Triggers: HIPAA, PCI-DSS, FedRAMP

📚 Docker secrets nativo
   • Cuándo: si migras a Docker Swarm v2

📚 Cloud SecretsManager (AWS/GCP)
   • Cuándo: NUNCA (viola D-009 LOCAL)
   • Si migras cloud completo v3

📚 Hardware Security Module (HSM)
   • Cuándo: v3 enterprise compliance extremo
   • Beneficio: master KEK en hardware tamper-proof

📚 Multi-key encryption (dual control)
   • Cuándo: v3 cliente requiere 2-of-3 keys
   • Implementación: Shamir's Secret Sharing

📚 Customer-managed encryption keys (CMEK)
   • Cuándo: v3 enterprise BYOK
   • Cliente provee su master KEK
   • For3s solo cifra/descifra, no almacena master

📚 Auto-rotation con dynamic credentials
   • Cuándo: v2 si Vault adoptado
   • Beneficio: credentials temporales per request

📚 Time-bound secrets (auto-expire)
   • Cuándo: v2 para tokens API temporal access

📚 Secret sharing entre workspaces (controlled)
   • Cuándo: v3 enterprise marketplace
   • Cliente A comparte tool con cliente B con secret bridge
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**

---

## 11. Implicaciones en Bloques 2-3 y rondas futuras

### Para Bloque 2 R4 — MCP Servers Core (siguiente)

```
✅ mcp SDK ready (4.1.1)
✅ Discovery framework (4.1.2)
✅ Hosting Docker (4.1.3)
✅ Secrets injection per-request (4.1.4)

4.2.1 GitHub MCP server:
   → Container Docker shared
   → Auth via SecretsManager per workspace
   → Discovery automático tools GitHub

4.2.2 Filesystem MCP server:
   → Container Docker shared
   → Root path per workspace (volume mount)
   → Permission model granular

4.2.3 HTTP/Fetch MCP server:
   → Container Docker shared
   → Rate limits per workspace
   → Auth headers per call

4.2.4 Telegram bot integration:
   → Container Docker shared
   → Webhook vs polling decision
   → Multi-user routing per workspace
```

### Para Bloque 3 R4 — Tool Lifecycle

```
✅ Permission model granular (B2 3.2.4)
✅ require_confirmation flag (P3)
✅ Hot-reload event-driven (4.1.2)
✅ Resource quotas Docker (4.1.3)

4.3.1 Tool authorization workflows:
   → Human-in-loop vía Telegram (P3)
   → Dry-run para destructive
   → Approval workflow audit

4.3.2 Tool versioning + rollback:
   → Image SHA pinned (K8s-ready)
   → Rollback via docker image tag
   → Audit version transitions

4.3.3 Tool testing & sandbox:
   → Container sandbox dedicado
   → Mock secrets para tests
   → CI/CD integration foundation R10
```

### Para R5 — Orchestration / Multi-Agent

```
✅ Container workspace per cliente
✅ MCP tools shared stateless ready
✅ AgentDelegationTool foundation (B2 3.2.4)

R5 decidirá:
   • Nodo 8 Tálamo (router tools + agents)
   • Multi-Agent Network lifecycle
   • Sub-agent containers (Capa 3 extensible)
```

### Para R6 — Memory Stack extensions

```
✅ Container workspace tiene memoria privada
✅ Volumes per workspace aislados

R6 decidirá:
   • Memory tier extensions
   • Procedural memory (skills)
   • Semantic memory cross-workspace (con permission)
```

### Para R7 — Frontend / Channel

```
✅ for3s-api único entry point
✅ Dashboard cliente self-service ready
✅ Telegram MCP foundation (4.2.4)
✅ SSE protocol (R3 B3 3.3.1)

R7 decidirá:
   • Web dashboard framework
   • Mobile app (futuro)
   • Multi-channel routing
```

### Para R8 — Observability

```
✅ Prometheus métricas extendidas (~25 + MCP/secrets)
✅ Audit chain inmutable
✅ Docker container metrics nativos

R8 decidirá:
   • Grafana dashboards
   • Alerting rules
   • Distributed tracing
```

### Para R9 — Security / Compliance

```
✅✅ 3-layer isolation defendible SOC2/ISO27001
✅✅ Secrets KEK hierarchy (defense in depth)
✅ Audit per-secret-usage
✅ Permission model granular
✅ Anomaly detection (B4 3.4.2)

R9 decidirá:
   • Nodo 8 Amígdala (security checks pre-execution)
   • Prompt injection detection
   • SOC2 / ISO27001 audit path
   • Penetration testing
```

### Para R10 — CI/CD / Deploy

```
✅ Docker compose foundation
✅ Provisioning scripts foundation
✅ BYOC packaging trivial
✅ K8s-ready images

R10 decidirá:
   • CI/CD pipeline (GitHub Actions probable)
   • Deploy strategy (canary, blue-green)
   • Backup/restore automation
   • Image scanning (Trivy)
   • Vulnerability management
```

---

## 12. Riesgos legítimos aceptados

11 riesgos B1 R4 identificados, todos mitigables.

### Riesgo 1 — mcp SDK breaking changes v2.x

```
PROBLEMA: SDK evoluciona, breaking changes posibles
IMPACTO v1: BAJO (pin version)
MITIGACIÓN:
   • Pin >=1.0,<2.0 en pyproject.toml
   • Abstraction layer MCPClient permite swap
   • Monitor changelog Anthropic
```

### Riesgo 2 — MCP server crash deja sesión zombie

```
PROBLEMA: subprocess MCP server crashea, conexión queda
IMPACTO v1: BAJO
MITIGACIÓN:
   • AsyncExitStack garantiza cleanup
   • Health check periódico
   • Retry connection on call failure
```

### Riesgo 3 — Static config drift (config vs realidad)

```
PROBLEMA: mcp_servers.yaml diverge de MCP servers reales
IMPACTO v1: MEDIO
MITIGACIÓN:
   • Pydantic validation startup
   • Audit divergencia al startup
   • Version control git
   • Tests CI verifican config schema
```

### Riesgo 4 — Workspace allowed_tools referencia tool inexistente

```
PROBLEMA: admin agrega tool a workspace pero tool no existe
IMPACTO v1: BAJO
MITIGACIÓN:
   • Audit + Telegram alert si missing
   • Workspace creation valida contra registry
   • Dashboard muestra missing tools
```

### Riesgo 5 — Race conditions durante hot-reload

```
PROBLEMA: tool call en flight cuando reload sucede
IMPACTO v1: BAJO
MITIGACIÓN:
   • _refresh_lock asyncio.Lock (mutex)
   • Tools "in-flight" completan con schema viejo
   • Rollback si reload falla
```

### Riesgo 6 — Config file mal formado por edición Brian

```
PROBLEMA: mcp_servers.yaml syntax error
IMPACTO v1: BAJO
MITIGACIÓN:
   • Pydantic validation antes apply
   • Si falla → log + revert + audit + Telegram
   • Config NUNCA "rota a medias"
```

### Riesgo 7 — MCP push notifications spam

```
PROBLEMA: server defectuoso emite list_changed cada segundo
IMPACTO v1: BAJO (4 servers v1)
MITIGACIÓN:
   • Rate limit max 1 reload/server/10s
   • Alarm si reload rate >6/hora
```

### Riesgo 8 — Container Docker se crashea cliente

```
PROBLEMA: workspace container OOM o crash
IMPACTO v1: MEDIO (cliente afectado)
MITIGACIÓN:
   • Docker restart policy: always
   • Health check Docker nativo
   • Logs persistentes en volume (no en container)
   • Backup workspace permite restore rápido
```

### Riesgo 9 — Brian rompe arquitectura con setup error

```
PROBLEMA: docker-compose mal configurado
IMPACTO v1: ALTO (todos clientes afectados)
MITIGACIÓN:
   • Provisioning scripts idempotentes
   • Test environment separado
   • Ansible playbook (R10)
   • Pre-prod validation antes producción
```

### Riesgo 10 — Master KEK loss

```
PROBLEMA: pierde master_key → ALL secrets perdidos
IMPACTO v1: CRÍTICO (irrecuperable)
MITIGACIÓN:
   • Backup #1 USB hardware Brian custodia
   • Backup #2 paper safe
   • Backup #3 succession plan familiar
   • Setup ritual: verificar backup antes producción
   • Disaster recovery doc paso a paso
   • Brian Telegram weekly "verify backup integrity"
```

### Riesgo 11 — Performance overhead decrypt per request

```
PROBLEMA: cada secret access = Postgres lookup + AES decrypt
IMPACTO v1: BAJO (<2ms con AES-NI)
MITIGACIÓN:
   • workspace_kek_cache memoria
   • AES-NI hardware accel
   • Medido <2ms per decrypt
   • Prometheus métrica decrypt_duration_ms
```

---

## Cierre del Bloque 1 R4

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ R4 BLOQUE 1 — MCP FRAMEWORK & DISCOVERY CERRADO           ║
║                                                                ║
║   4/4 sub-temas LOCKED                                         ║
║   Score: 9.5/10 (excelente)                                     ║
║   Riesgos legítimos: 11 identificados, todos mitigables         ║
║   Spillover ejecutado:                                          ║
║      ✅ D-016 logged + master R4 creado + Estado §3.1.quaterdec ║
║      ⏳ Diferido: docs públicos hasta cierre R4 completo       ║
║                                                                ║
║   Costo incremental B1 R4: $0 infra                              ║
║   Costo total v1: ~USD 62-77/mes (sin cambio)                    ║
║   Recursos: +1.5 GB RAM base + per workspace                     ║
║                                                                  ║
║   Diferenciador comercial NUEVO:                                 ║
║   • Container per cliente (aislamiento físico real)              ║
║   • 3-layer compliance (DB + container + network)                ║
║   • Secrets KEK hierarchy (defense in depth)                     ║
║   • BYOC enabled                                                  ║
║   • K8s-ready foundation                                          ║
║                                                                  ║
║   Próximo: R4 Bloque 2 — MCP Servers Core (4 sub-temas)          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_04_Bloque_1_MCP_Framework_Discovery.md`).
