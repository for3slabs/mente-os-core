# Ronda 4 — Bloque 2: MCP Servers Core

**Sub-documento detallado de R4 — Tools/MCP Layer. Bloque 2 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-06
**Estatus:** ✅ LOCKED (4/4 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema con profundidad R2)
**Documento padre:** [Ronda_04_Tools_MCP_Layer.md](Ronda_04_Tools_MCP_Layer.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes
- P3 — Workspace isolation
- P4 — Encryption at rest

**Pre-preguntas LOCKED Bloque 2:**
- B2-Q1: Confirma R4 B2 ✅
- B2-Q2: Orden 4.2.1 → 4.2.4 (GitHub crítico primero) ✅
- B2-Q3: Read+Write desde inicio (destructive con require_confirmation) ✅

**Dependencias resueltas en R4 B1:**
- ✅ mcp SDK oficial Anthropic (4.1.1)
- ✅ Discovery híbrido A+C event-driven (4.1.2)
- ✅ Docker Multi-tenant 3 capas (4.1.3)
- ✅ SecretsManager KEK hierarchy (4.1.4)

**Fuente de verdad:**
- [`For3s_OS_Grafo_Maestro.md`](../Cerebro/For3s_OS_Grafo_Maestro.md) §4 Nodo 4 Cuerpo Calloso
- [`Hermes_Arquitectura_Completa.md`](Hermes_Arquitectura_Completa.md) §11 (patrones Telegram)

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Principio arquitectónico LOCKED (4.2.1 PARTE 2) — validado 3 veces](#3-principio-arquitectónico-locked-421-parte-2--validado-3-veces)
4. [Sub-tema 4.2.1 — GitHub MCP server](#4-sub-tema-421--github-mcp-server)
5. [Sub-tema 4.2.2 — Filesystem MCP server](#5-sub-tema-422--filesystem-mcp-server)
6. [Sub-tema 4.2.3 — HTTP/Fetch MCP server](#6-sub-tema-423--httpfetch-mcp-server)
7. [Sub-tema 4.2.4 — Telegram MCP server (+ Hermes)](#7-sub-tema-424--telegram-mcp-server--hermes)
8. [Stack final consolidado](#8-stack-final-consolidado)
9. [Cobertura del Grafo Maestro](#9-cobertura-del-grafo-maestro)
10. [Costo total post-Bloque 2](#10-costo-total-post-bloque-2)
11. [Implicaciones en Bloque 3 y rondas futuras](#11-implicaciones-en-bloque-3-y-rondas-futuras)
12. [Riesgos legítimos aceptados](#12-riesgos-legítimos-aceptados)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 2 — MCP SERVERS CORE                                  ║
║   4 sub-temas LOCKED el 2026-06-06                             ║
║                                                                ║
║   4.2.1 GitHub MCP        → A) Oficial Anthropic                ║
║   4.2.2 Filesystem MCP    → B) Custom Python (FastMCP)          ║
║   4.2.3 HTTP MCP          → B) Custom Python (SSRF 5-capa)      ║
║   4.2.4 Telegram MCP      → B) Custom Python + Hermes patterns  ║
║                                                                  ║
║   Principio Arquitectónico LOCKED VALIDADO 3 veces.              ║
║   1 oficial + 3 custom = composición sobre reinvención.          ║
║                                                                  ║
║   Tools concretas habilitadas:                                   ║
║   • GitHub: 26 tools                                              ║
║   • Filesystem: 12 tools                                          ║
║   • HTTP: 6 tools                                                 ║
║   • Telegram: 8 tools                                             ║
║   • + Core LOCAL (B2 3.2.4): 5 tools                              ║
║   ────────────────────────────────                                ║
║   TOTAL: ~57 tools disponibles para agentes                       ║
║                                                                  ║
║   Costo incremental B2:           $0 infra                        ║
║   Recursos servidor B2:           ~950 MB RAM (4 containers)      ║
║   Setup tiempo total B2:          ~14-19 días dev Brian           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Composición sobre reinvención. Tools donde comunidad MCP ya
hizo el trabajo (GitHub): usar oficial. Tools donde aislamiento
multi-tenant, security crítico, o lógica For3s-specific son
requirements (Filesystem, HTTP, Telegram): construir custom
Python con FastMCP y reusar learnings probados en producción
(Hermes patterns)."
```

Las 4 decisiones convergen en patrones consistentes:

```
1. ÁRBOL DE DECISIÓN PRINCIPIO LOCKED (4.2.1 PARTE 2)
   → Aplicado 4 veces, validado 3 (FS, HTTP, Telegram)

2. UNIFORMIDAD CUSTOM PYTHON:
   → 3 custom servers usan MISMO template:
      • FastMCP framework
      • Pydantic v2 schemas
      • Audit obligatorio (R2 B1)
      • Healthcheck (K8s-ready)
      • Multi-stage Dockerfile non-root
      • Tests pytest async

3. SECRETS INJECTION PATTERN:
   → Per-request via SecretsManager (4.1.4)
   → NO env vars container (defense in depth)
   → Brian NUNCA ve plaintext

4. AUDIT + OBSERVABILITY UNIFORME:
   → Cada tool call → audit_events
   → Prometheus métricas obligatorias por server
   → Security alarms para anomalies

5. SENSITIVE TOOLS PATTERN:
   → require_confirmation=True (P3 LOCKED)
   → Inline keyboard Telegram para approval
   → Audit + rollback foundation

6. REUTILIZACIÓN HERMES (Telegram):
   → 7 patrones validados en producción reusados
   → Foundation R7 multi-canal gratis
   → Menos riesgo arquitectónico
```

### Por qué esta filosofía importa

**Para Pilar 1 Seguridad:** SSRF protection multi-capa HTTP + path traversal Filesystem + signature validation Telegram + permission per tool = defendible enterprise B2B SOC2.

**Para Pilar 2 Escalabilidad:** 4 containers shared stateless + workspace context per-call + cache responses (Valkey) = recursos eficientes a escala.

**Para Pilar 3 Autonomía:** Agente decide qué tool usar autónomamente, ejecuta dentro de boundaries seguros (permissions + confirmations), recibe outputs estructurados.

---

## 3. Principio Arquitectónico LOCKED (4.2.1 PARTE 2) — validado 3 veces

Establecido en 4.2.1 y aplicado en cada sub-tema siguiente:

```
   ÁRBOL DE DECISIÓN MCP SERVER:
   
   ¿El servicio tiene MCP server oficial Anthropic maduro?
   │
   ├─ SÍ ─► ¿Cobertura tools suficiente para nuestro use case?
   │       │
   │       ├─ SÍ ─► USAR OFICIAL (A)
   │       │       Ejemplos: GitHub (4.2.1) ✅
   │       │
   │       └─ NO ─► HÍBRIDO (E): Oficial + capa Python custom
   │
   ├─ NO, hay 3rd party community maduro ─►
   │       Evaluar madurez + license + maintenance
   │       Si OK → ADOPTAR con pin version
   │       Si NO → CUSTOM PYTHON (B)
   │
   └─ NO existe ─► CUSTOM PYTHON (B)
           Ejemplos:
           • Filesystem (4.2.2) — aislamiento multi-tenant ✅
           • HTTP (4.2.3) — SSRF protection ✅
           • Telegram (4.2.4) — multi-user routing + no oficial ✅
   
   CHECKLIST CONSTRUIR B:
      ✅ NO existe oficial maduro
      ✅ NO existe 3rd party community maduro
      ✅ Tool For3s-specific
      ✅ Servicio LATAM nicho
      ✅ Compliance regulatorio exige código auditable
      ✅ API interna cliente custom
      ✅ Necesitas agregar valor For3s sobre tool genérica
   
   TEMPLATE B (validado 3 veces):
      • FastMCP framework
      • Pydantic v2 schemas obligatorios
      • Audit logger (R2 B1) integration
      • Healthcheck obligatorio (K8s-ready)
      • TOOL_TIMEOUT respect (R2 B3)
      • Multi-stage Dockerfile non-root
      • Tests pytest async
```

### Resultados validación principio

```
   4.2.1 GitHub   → A oficial (GitHub maduro, cobertura suficiente)
   4.2.2 Filesystem → B custom (aislamiento workspace crítico)
   4.2.3 HTTP     → B custom (SSRF 5-capa crítico)
   4.2.4 Telegram → B custom (no oficial + multi-user routing)
   
   PROPORCIÓN: 1 oficial / 3 custom (25% / 75%)
   
   Esto es CONSISTENTE con la filosofía For3s OS:
   "Composición sobre reinvención, pero construir cuando
    aislamiento + security + For3s-specific son requirements."
```

---

## 4. Sub-tema 4.2.1 — GitHub MCP server

### Decisión LOCKED

```
A) MCP server oficial Anthropic (@modelcontextprotocol/server-github)
+ Principio Arquitectónico LOCKED PARTE 2 establecido aquí
```

### Razón

- GitHub es servicio MADURO con MCP server OFICIAL Anthropic
- Cobertura tools suficiente (26 tools out-of-box)
- Datos viven en github.com (no en for3s server) → aislamiento via PAT
- Wedge QA primary use case
- Brian no mantiene código GitHub-specific

### Stack final

```
Package: @modelcontextprotocol/server-github (>=0.6,<0.7 pinned SHA)
Container: Docker Capa 2 shared (4.1.3)
Transport: SSE localhost:7001
Auth: PAT per workspace via SecretsManager (4.1.4)
Multi-repo per workspace: workspace.github_allowed_repos[]
Cache responses: Valkey con TTL per tool type
Rate limit: per workspace via Token Bucket R3 B3 3.3.2
Webhook: /webhooks/github/{workspace_id} con HMAC validation
```

### 26 Tools clasificadas

```
READ-ONLY (14 tools, default whitelist):
   search_repositories, search_code, search_issues, search_users,
   get_file_contents, list_commits, list_issues, get_issue,
   get_pull_request, list_pull_requests, get_pull_request_files,
   get_pull_request_status, get_pull_request_comments, get_pull_request_reviews

WRITE (9 tools, audited):
   add_issue_comment, update_issue, create_branch, create_or_update_file,
   push_files, fork_repository, create_issue, create_pull_request,
   create_pull_request_review

DESTRUCTIVE (4 tools, require_confirmation=True):
   merge_pull_request, update_pull_request_branch,
   create_repository, delete_repository
```

### Cache strategy

```python
CACHEABLE_TOOLS_TTL = {
    'get_file_contents': 300,    # 5 min
    'get_pull_request': 60,       # 1 min
    'get_issue': 60,
    'list_commits': 180,          # 3 min
    'search_repositories': 1800,  # 30 min
    'search_code': 900,           # 15 min
    'list_pull_requests': 30,
    'list_issues': 30,
}

NEVER_CACHE = ['get_pull_request_status', 'get_pull_request_files']
ALL_WRITE_TOOLS_NO_CACHE = True
```

### Onboarding cliente self-service

```
1. Cliente accede dashboard → "Conectar GitHub"
2. Instrucciones:
   • Crear PAT en github.com/settings/tokens
   • Scope mínimo: 'repo'
   • Expiration: 90 días
3. Cliente pega PAT
4. For3s validates via GET /user
5. Detect available repos
6. Cliente selecciona repos en allowed_repos[]
7. Store PAT via SecretsManager (4.1.4)
8. Audit: github_onboarding_completed
```

### Webhook handling

```python
POST /webhooks/github/{workspace_id}
   1. Validate HMAC signature (workspace webhook_secret)
   2. Parse event_type (pull_request, push, issue, etc.)
   3. Enqueue Arq async task
   4. Return 200 inmediato (GitHub timeout 10s)
```

### Reglas duras LOCKED

```
✅ Package pinned >=0.6,<0.7
✅ Container Capa 2 shared
✅ PAT per workspace, scope mínimo 'repo'
✅ PAT expiration 90 días + auto-rotation reminder
✅ Auth injection per-request (NO env vars)
✅ Multi-repo via workspace.github_allowed_repos[]
✅ Repo allowlist enforcement ANTES de cada tool
✅ Sensitive tools (4) require_confirmation=True
✅ Cache responses con TTL configurado
✅ Write/destructive: NEVER cache
✅ Rate limit 1 RPM per tool call (Token Bucket)
✅ Webhook async vía Arq
✅ Audit obligatorio per call
✅ Métricas Prometheus específicas
```

---

## 5. Sub-tema 4.2.2 — Filesystem MCP server

### Decisión LOCKED

```
B) Custom Python MCP server (FastMCP) con permission model nuestro
```

### Razón (aplicación Principio Arquitectónico)

```
   Existe oficial @modelcontextprotocol/server-filesystem
   PERO oficial NO cubre:
   ❌ Aislamiento per workspace nativo
   ❌ Hidden files control granular (.env, .git, .ssh)
   ❌ Size limits configurable
   ❌ Backup before delete
   ❌ For3s-specific extensions
   
   → CUSTOM PYTHON (B) requerido
```

### Stack final

```
Image: for3s/mcp-filesystem:1.0.0 (build propio, pinned SHA)
Framework: FastMCP (MIT) + Pydantic v2 + aiofiles (BSD)
Container: Capa 2 shared
Transport: SSE localhost:7002
Workspace root: /var/lib/for3s/workspaces/{id}/files/
Trash folder: /var/lib/for3s/workspaces/{id}/trash/ (7 días recovery)
```

### Path security multi-capa

```python
def resolve_workspace_path(workspace_id: str, relative_path: str) -> Path:
    """Resolve y VALIDA path multi-capa."""
    workspace_root = WORKSPACES_ROOT / workspace_id / "files"
    
    # 1. Compose absoluto + resolve
    target = (workspace_root / relative_path).resolve()
    
    # 2. ANTI path traversal: dentro workspace_root
    target.relative_to(workspace_root.resolve())  # ValueError if escape
    
    # 3. Anti hidden files / patterns peligrosos
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, str(target.relative_to(workspace_root))):
            raise BlockedPathError(pattern)
    
    # 4. Extension check
    if target.suffix.lower() in BLOCKED_EXTENSIONS:
        raise BlockedPathError(target.suffix)
    
    return target
```

### Patterns blocked LOCKED v1

```
BLOCKED_PATTERNS:
   ^\.env           (env files)
   ^\.git/          (git directory)
   ^\.ssh/          (ssh keys)
   ^\.aws/          (AWS credentials)
   /credentials\.   (generic credentials)
   /secrets/        (secrets folders)
   \.pem$           (private keys)
   \.key$           (key files)

BLOCKED_EXTENSIONS: .exe, .dll, .so, .bin
```

### 12 Tools clasificadas

```
READ-ONLY (7 tools, default whitelist):
   read_file, read_multiple_files, list_directory,
   directory_tree, get_file_info, search_files, search_content

WRITE (4 tools, audited, auto-backup):
   write_file, edit_file, create_directory, move_file

DESTRUCTIVE (3 tools, require_confirmation=True):
   delete_file, delete_directory, rename_workspace_root
```

### Quotas per tier

```
Pilot Light:    10 GB total quota, 10 MB max file
Pilot Pro:      50 GB total quota, 10 MB max file
Enterprise:     custom (negociable)

Resource limits container (Docker):
   Memory: 200 MB
   CPU: 0.5
```

### Backup automático

```
Antes write overwrite: copia → .backup.{timestamp}
Antes delete: move → trash/{timestamp}_{filename}
Trash auto-purge: Arq cron diario, >7 días
Recovery: cliente puede restore desde trash 7 días
```

### Reglas duras LOCKED

```
✅ FastMCP + Pydantic v2 + aiofiles
✅ Container Capa 2 shared
✅ Workspace root per workspace
✅ Path validation OBLIGATORIA (resolve + relative_to)
✅ 8 patterns blocked + extensions whitelist per workspace
✅ Max file size 10 MB, total quota 10/50 GB
✅ 12 tools (7 read + 4 write + 3 destructive)
✅ Backup automático write/delete
✅ Trash recovery 7 días + auto-purge cron
✅ Binary handling: base64 + mime detection
✅ Path traversal attempts → SECURITY ALARM
✅ Audit obligatorio TODAS operaciones
✅ 9 métricas Prometheus específicas
```

---

## 6. Sub-tema 4.2.3 — HTTP/Fetch MCP server

### Decisión LOCKED

```
B) Custom Python MCP server (FastMCP) con SSRF 5-capa robusta
```

### Razón (aplicación Principio Arquitectónico)

```
   Existe oficial @modelcontextprotocol/server-fetch
   PERO oficial NO cubre OWASP LLM Top 10:
   ❌ SSRF protection básica (solo localhost)
   ❌ DNS rebinding protection
   ❌ Domain allowlist per workspace
   ❌ Rate limit per workspace+domain
   ❌ POST/PUT/DELETE methods
   ❌ Auth injection per workspace
   ❌ Response size limits
   ❌ Cache layer
   
   → CUSTOM PYTHON (B) con SSRF 5-capa
```

### Stack final

```
Image: for3s/mcp-http:1.0.0
Framework: FastMCP + Pydantic v2 + httpx (BSD) + trafilatura (Apache 2.0)
Container: Capa 2 shared
Transport: SSE localhost:7003
Resource: 300 MB RAM, 0.5 CPU
```

### SSRF 5-capa protection

```
CAPA 1: URL Validation
   • Schema check (http/https only, NO file/ftp/gopher)
   • URL length max 2048
   • Format valid

CAPA 2: Domain Policy
   • Workspace allowlist (si configured)
   • Global blocklist (malicious domains DB)
   • TLD restrictions

CAPA 3: DNS + IP Validation
   • Resolve DNS → all IPs
   • Reject 10 networks privadas:
     127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12,
     192.168.0.0/16, 169.254.0.0/16, 0.0.0.0/8,
     100.64.0.0/10, ::1/128, fc00::/7, fe80::/10
   • DNS rebinding: re-resolve before connect

CAPA 4: Rate Limit
   • Token Bucket per workspace+domain (R3 B3 3.3.2)
   • Pilot Light: 100/hour workspace, 50/hour per domain
   • Pilot Pro: 500/hour workspace, 100/hour per domain

CAPA 5: Method + Body Validation
   • GET/HEAD: always OK
   • POST/PUT/PATCH: require_confirmation=True
   • DELETE: require_confirmation=True
   • Body size limit 1 MB
```

### Blocked domains global

```
metadata.google.internal     (GCP metadata)
169.254.169.254              (AWS metadata)
+ lista actualizable
```

### 6 Tools clasificadas

```
READ-ONLY (2 tools, default whitelist):
   http_fetch (GET), http_head (HEAD metadata)

WRITE/MUTATE (3 tools, require_confirmation=True):
   http_post, http_put, http_patch

DESTRUCTIVE (1 tool, require_confirmation=True):
   http_delete
```

### Cache strategy

```
Solo cacheable: GET 200
Storage: Valkey
Default TTL: 300s
Respect Cache-Control headers
Cache key incluye workspace_id (NO shared)
```

### HTML processing

```
trafilatura.extract() → texto principal
Fallback: raw HTML si extracción falla
JSON parsed automático si content-type
Binary → base64 + mime
Max output chars: 50000
```

### Auth injection per workspace

```sql
workspace.http_auth_configs JSONB
-- {hostname: secret_name_to_inject_as_bearer}
-- Ej: {"api.openai.com": "openai_api_key"}
```

### Reglas duras LOCKED

```
✅ FastMCP + httpx + trafilatura
✅ Container Capa 2 shared
✅ SSRF protection 5-capa OBLIGATORIA
✅ 10 networks blocked + cloud metadata blocklist
✅ 6 tools (2 read + 3 write require_conf + 1 destructive)
✅ Limits: URL 2048, response 10 MB, body 1 MB, redirects 3
✅ Timeout: 30s (R2 B3 reused)
✅ Rate limits per tier
✅ Auth injection vía SecretsManager
✅ Cache solo GET 200 con Cache-Control respect
✅ HTML processing trafilatura
✅ SSRF blocked → SECURITY ALARM
✅ Workspace allowlist opcional
✅ Audit obligatorio + 8 métricas Prometheus
✅ OWASP LLM Top 10 compliance
```

---

## 7. Sub-tema 4.2.4 — Telegram MCP server (+ Hermes)

### Decisión LOCKED

```
B) Custom Python MCP server (FastMCP + PTB)
+ PATRONES HERMES adaptados multi-tenant
```

### Razón (aplicación Principio Arquitectónico)

```
   NO existe MCP server oficial Anthropic para Telegram
   Community MCP: madurez incierta
   For3s-specific: multi-user routing, approval flow P3
   Hermes ya validó arquitectura en producción
   
   → CUSTOM PYTHON (B) con reuso patrones Hermes
```

### Stack final

```
Image: for3s/mcp-telegram:1.0.0
Framework: FastMCP + python-telegram-bot 21.x (LGPLv3) + Pydantic v2
Container: Capa 2 shared
Transport: SSE localhost:7004
Resource: 250 MB RAM, 0.5 CPU
Bot strategy: 1 BOT PER WORKSPACE (no global)
Transport mode: WEBHOOK (no polling v1)
Reference: Mente/Cuerpo/Hermes_Arquitectura_Completa.md §11
```

### 7 Patrones Hermes reusados

```
1. PlatformAdapter ABC
   • Foundation R7 multi-canal (Discord, Slack v2)
   • Telegram es 1 adapter entre futuros 20+
   
2. GatewayRunner FastAPI
   • Webhook handler patrón validado
   • Platform Router enruta a adapter correcto
   
3. NormalizedMessage abstracta
   • Telegram raw → For3s Message genérico
   • Agente NO sabe del canal específico
   
4. Authorize pattern
   • adapter.authorize(user_id) → bool
   • workspace_user lookup
   
5. Session persistence
   • Hermes: sessions/{platform}/ folder
   • For3s: workspace_telegram_users table Postgres
   
6. Cross-platform user linking (foundation v2)
   • telegram_id → canonical_id → discord_id (futuro)
   
7. Config-driven enable
   • Hermes: gateway.platforms.telegram.enabled
   • For3s: workspace.telegram_bot_username (null = disabled)
```

### Adaptaciones For3s-specific

```
Hermes (single-user)        →  For3s (multi-tenant)
─────────────────────────────────────────────────────
Profile = 1 user             →  Workspace = N users
SQLite local                  →  Postgres central
1 bot global                  →  1 bot per workspace
Bot token plain               →  Bot token KEK cifrado
Authorize whitelist           →  Role-based (member/admin/owner)
Session folder                →  workspace_telegram_users table
                              +  telegram_approval_requests table
No approval flow              →  Inline keyboard P3 LOCKED
No audit chain                →  Audit chain inmutable (R2 B1)
Container process             →  Docker Capa 2 shared
```

### 8 Tools

```
OUTBOUND (agent → user):
   telegram_send_message
   telegram_send_approval_request (inline keyboard P3)
   telegram_send_document (sensitive: require_confirmation)
   telegram_edit_message
   telegram_typing_indicator

INBOUND queries (no envío, solo lookup):
   telegram_get_chat_info
   telegram_get_user_info
   telegram_get_updates (fallback polling)
```

### Webhook handler

```python
POST /webhooks/telegram/{workspace_id}
   1. Validate HMAC signature (workspace webhook_secret)
   2. Normalize via TelegramAdapter (Hermes pattern)
   3. Authorize user (workspace_telegram_users lookup)
   4. Enqueue Arq async task
   5. Return 200 inmediato (Telegram timeout 60s)
```

### Approval flow P3

```python
# Inline keyboard buttons
[✅ Aprobar] [❌ Rechazar]
[ℹ️ Detalles]

# approval_token único 5 min expiry
# Tabla telegram_approval_requests
# Auto-timeout reject si no responde
```

### Onboarding cliente self-service

```
1. Dashboard cliente: "Conectar Telegram"
2. Instrucciones BotFather:
   • /newbot
   • Nombre: "Acme QA Assistant"
   • Username: AcmeQABot
   • Copiar token
3. Cliente pega token
4. For3s validates via getMe
5. Store bot_token + webhook_secret via SecretsManager
6. setWebhook automático
7. Cliente comparte @AcmeQABot con team
8. Cada usuario /start → admin aprueba via dashboard
```

### Reglas duras LOCKED

```
✅ FastMCP + PTB 21.x (LGPLv3) + Hermes patterns
✅ Container Capa 2 shared
✅ Bot per workspace (no global)
✅ Webhook transport (Cloudflare Tunnel D-009)
✅ 7 patrones Hermes reusados
✅ 8 tools (outbound + inbound + approval)
✅ Multi-user routing via workspace_telegram_users table
✅ Approval flow inline keyboard P3
✅ Async processing Arq
✅ Signature validation HMAC obligatoria
✅ Unknown user → polite reject + audit
✅ Bot token vía SecretsManager (NUNCA logs)
✅ Rate limit Telegram respect
✅ Limits: msg 4096, caption 1024, approval TTL 300s
✅ 9 métricas Prometheus específicas
✅ 2 tablas SQL nuevas
✅ Foundation R7 Frontend multi-canal
```

---

## 8. Stack final consolidado

```
COMPONENTE                              DECISIÓN                          COSTO
─────────────────────────────────────────────────────────────────────────────
GitHub MCP server                       A) Oficial Anthropic              $0
   • @modelcontextprotocol/server-github (>=0.6,<0.7 pinned)
   • Container Capa 2 shared, SSE localhost:7001
   • 26 tools (read+write+destructive)
   • PAT per workspace via SecretsManager
   • Cache Valkey + Rate limit + Webhook
   • Setup: 3-4 días

Filesystem MCP server                   B) Custom Python (FastMCP)        $0
   • for3s/mcp-filesystem:1.0.0
   • FastMCP + Pydantic v2 + aiofiles (BSD)
   • Container Capa 2 shared, SSE localhost:7002
   • 12 tools (7 read + 4 write + 3 destructive)
   • Path validation multi-capa + 8 patterns blocked
   • Backup automático + trash recovery 7 días
   • Setup: 4-5 días

HTTP MCP server                         B) Custom Python (FastMCP+SSRF)   $0
   • for3s/mcp-http:1.0.0
   • FastMCP + httpx (BSD) + trafilatura (Apache 2.0)
   • Container Capa 2 shared, SSE localhost:7003
   • 6 tools (2 read + 3 write + 1 destructive)
   • SSRF 5-capa + 10 networks blocked
   • Auth injection via SecretsManager
   • Setup: 4-5 días

Telegram MCP server                     B) Custom Python (PTB+Hermes)     $0
   • for3s/mcp-telegram:1.0.0
   • FastMCP + python-telegram-bot 21.x (LGPLv3)
   • Container Capa 2 shared, SSE localhost:7004
   • 8 tools (outbound + inbound + approval)
   • 7 patrones Hermes adaptados multi-tenant
   • 1 bot per workspace + webhook + multi-user routing
   • Setup: 3-4 días (con Hermes ahorra 2 días)
─────────────────────────────────────────────────────────────────────────────
TOTAL incremental B2 R4                                                   ~$0/mes
TOTAL v1 (R1+R2+R3 100%+R4 B1+B2)                                       ~$62-77/mes
```

### Estructura módulo for3s_os/ extendida (post-B2)

```
for3s_os/
├── llm/                            → R3 (intacto)
├── secrets/                        → 4.1.4 (intacto)
├── mcp/                            → 4.1.1-4.1.3 (intacto)
├── admin/                          → 4.1.2 (intacto)
└── ...

containers/mcp-servers/             ← extendido B2
├── github/                          → Container oficial Anthropic
│   ├── Dockerfile (oficial server)
│   └── healthcheck
├── filesystem/                      → ⭐ Custom Python B2
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── server.py (FastMCP entry)
│   ├── policy.py (path validation)
│   ├── tools/ (read/write/destructive)
│   └── tests/
├── http/                            → ⭐ Custom Python B2
│   ├── Dockerfile
│   ├── server.py
│   ├── ssrf_validator.py (5-capa)
│   ├── rate_limiter.py
│   ├── tools/ (get/head/post/put/patch/delete)
│   └── tests/
└── telegram/                        → ⭐ Custom Python + Hermes B2
    ├── Dockerfile
    ├── server.py
    ├── adapter/ (Hermes PlatformAdapter)
    │   ├── base.py (ABC)
    │   ├── telegram.py (impl)
    │   ├── normalizer.py
    │   └── authorizer.py
    ├── tools/ (outbound/approval/inbound)
    ├── webhook/ (handler/signature/enqueue)
    ├── worker/ (process_message/process_callback)
    └── tests/

config/
└── mcp_servers.yaml                 → 4 servers configured

scripts/                              ← (intacto)
└── provision_workspace.sh
```

### Schema SQL extensiones B2

```sql
-- GitHub MCP (4.2.1)
ALTER TABLE shared.workspaces ADD COLUMN
    github_allowed_repos TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[];
ALTER TABLE shared.workspaces ADD COLUMN
    github_user TEXT;
ALTER TABLE shared.workspaces ADD COLUMN
    github_pat_expires_at TIMESTAMPTZ;

-- Filesystem MCP (4.2.2)
ALTER TABLE shared.workspaces ADD COLUMN
    filesystem_allowed_extensions TEXT[] NOT NULL 
    DEFAULT ARRAY['.txt','.md','.py','.js','.json','.yaml','.html','.css','.csv','.pdf','.docx','.xlsx','.png','.jpg','.svg']::TEXT[];
ALTER TABLE shared.workspaces ADD COLUMN
    filesystem_max_file_size_mb INTEGER NOT NULL DEFAULT 10;
ALTER TABLE shared.workspaces ADD COLUMN
    filesystem_total_quota_gb INTEGER NOT NULL DEFAULT 10;

-- HTTP MCP (4.2.3)
ALTER TABLE shared.workspaces ADD COLUMN
    http_domain_allowlist TEXT[] DEFAULT NULL;
ALTER TABLE shared.workspaces ADD COLUMN
    http_auth_configs JSONB DEFAULT '{}';

-- Telegram MCP (4.2.4)
ALTER TABLE shared.workspaces ADD COLUMN
    telegram_bot_username TEXT;
ALTER TABLE shared.workspaces ADD COLUMN
    telegram_webhook_configured_at TIMESTAMPTZ;

CREATE TABLE shared.workspace_telegram_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES shared.workspaces(id),
    workspace_user_id UUID NOT NULL,
    telegram_user_id BIGINT NOT NULL,
    telegram_username TEXT,
    telegram_chat_id BIGINT NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',
    permissions JSONB DEFAULT '{}',
    linked_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_active_at TIMESTAMPTZ,
    UNIQUE (workspace_id, telegram_user_id)
);

CREATE TABLE shared.telegram_approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    approval_token TEXT NOT NULL UNIQUE,
    workspace_id UUID NOT NULL,
    workspace_user_id UUID,
    tool_call_id UUID,
    action_description TEXT NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    decided_at TIMESTAMPTZ,
    decided_by_telegram_user_id BIGINT,
    decision TEXT,
    audit_event_id UUID
);
```

### Métricas Prometheus consolidadas B2 (~32 nuevas)

```
GitHub (8):
   github_api_calls_total, github_api_duration_seconds,
   github_cache_hits_total, github_rate_limit_remaining,
   github_pat_expiry_days_remaining, github_webhook_received_total,
   github_api_errors_total, github_pr_analysis_completed

Filesystem (9):
   filesystem_operations_total, filesystem_bytes_read_total,
   filesystem_bytes_written_total, filesystem_workspace_usage_bytes,
   filesystem_quota_remaining_pct, filesystem_path_traversal_blocked_total,
   filesystem_blocked_pattern_total, filesystem_backup_created_total,
   filesystem_delete_recovered_total

HTTP (8):
   http_requests_total, http_request_duration_seconds,
   http_response_bytes, http_cache_hits_total,
   http_ssrf_blocked_total, http_domain_denied_total,
   http_rate_limited_total, http_redirect_blocked_total

Telegram (9):
   telegram_messages_sent_total, telegram_messages_received_total,
   telegram_webhook_signature_invalid_total, telegram_unauthorized_user_total,
   telegram_approval_requests_total, telegram_api_calls_total,
   telegram_rate_limited_total, telegram_bot_health,
   telegram_webhook_processing_seconds
```

---

## 9. Cobertura del Grafo Maestro

### Nodos servidos por Bloque 2 R4

```
NODO                                 STATUS POST-B2 R4
──────────────────────────────────────────────────────
Nodo 4 Cuerpo Calloso (Tool Bus)    ✅ pleno (4 MCP servers operativos)
Nodo 6 Sistema Sensorial             ✅ Telegram canal bidireccional
Nodo 3 PFC (Orchestrator)            ✅ orquesta 57 tools concretas
Nodo 2 Cerebelo (Skills auto v3)    🟡 foundation (tools registradas)
Nodo 8 Tálamo (R5 routing)           🟡 foundation (tool selection v2)
```

### Pilares — Cobertura por B2 R4

```
Pilar 1 — Seguridad E2E
   ✅ SSRF 5-capa HTTP
   ✅ Path traversal protection Filesystem
   ✅ HMAC signature validation Telegram
   ✅ PAT KEK encryption GitHub
   ✅ Permission model per tool
   ✅ Require_confirmation destructive
   ✅ Audit chain inmutable per call
   ✅ Workspace allowlist enforcement

Pilar 2 — Escalabilidad por nodo
   ✅ Containers shared stateless (recursos eficientes)
   ✅ Cache responses (Valkey + TTL)
   ✅ Rate limit per workspace+resource
   ✅ Hot-reload sin downtime (B1)
   ✅ Resource quotas per tier

Pilar 3 — Autonomía Generativa
   ✅ 57 tools disponibles para agente
   ✅ Discovery dinámico hot-reload
   ✅ Permission boundaries claros
   ✅ Approval flow human-in-loop (P3)
   ✅ Foundation Skills auto v3+
```

### Anclas LOCKED — Verificación post-B2

```
1.D Dedicated SaaS  ✅ Per-workspace whitelist, allowed_repos, quotas
2.B Open Core       ✅ SDKs abiertos:
                       • @modelcontextprotocol/server-github (MIT)
                       • FastMCP (MIT)
                       • httpx (BSD)
                       • aiofiles (BSD)
                       • trafilatura (Apache 2.0)
                       • python-telegram-bot (LGPLv3)
3.D Equipo pequeño  ✅ 4 containers, hot-reload, scripts automation
                     ✅ Brian conoce stack (FastMCP, httpx, PTB)
                     ✅ NO infraestructura compleja (K8s defer v3)
```

---

## 10. Costo total post-Bloque 2

```
COMPONENTE                                          COSTO USD/mes
─────────────────────────────────────────────────────────────────
SUBTOTAL R1+R2+R3 100%+R4 B1:                       ~$62-77/mes

R4 BLOQUE 2 INCREMENTAL:
   GitHub MCP (oficial MIT):                        $0
   Filesystem MCP (custom FastMCP MIT):              $0
   HTTP MCP (custom + httpx BSD + trafilatura):      $0
   Telegram MCP (custom + PTB LGPLv3):               $0
─────────────────────────────────────────────────────────────────
TOTAL v1 (post-R4 B1+B2):                           ~$62-77/mes (sin cambio)
```

### Recursos servidor R4 B2

```
RAM:
   mcp-github:       200 MB
   mcp-filesystem:   200 MB
   mcp-http:         300 MB
   mcp-telegram:     250 MB
   ──────────────────────────
   TOTAL B2:         ~950 MB
   
   Acumulado R4 (B1 + B2):
   • B1 base: ~1.5 GB
   • B2 containers: ~950 MB
   ─────────────────────────
   TOTAL R4 v1: ~2.5 GB RAM

   De 30 GB disponibles servidor Brian:
   • Uso R4: ~8.3%
   • Disponible: ~25 GB (83%)

Capacidad post-R4 v1:
   ~40 workspaces Pilot Light simultáneos
   ~10 workspaces Pilot Pro simultáneos
   Suficiente v1 (3-5 pilots → 20-30 clientes)
```

### Tiempo setup B2

```
4.2.1 GitHub MCP (oficial):    3-4 días
4.2.2 Filesystem MCP (custom): 4-5 días
4.2.3 HTTP MCP (custom):       4-5 días
4.2.4 Telegram MCP (custom):   3-4 días (con Hermes ahorra 2)
──────────────────────────────────────────
TOTAL setup B2:                14-18 días dev Brian

ROI:
   Habilita wedge QA pilot (revenue $3,500-$8,000)
   57 tools disponibles agentes (universal multi-dominio)
   Foundation R7 Frontend (Telegram + PlatformAdapter ABC)
   Compliance B2B fuerte (SSRF + path validation + KEK)
```

---

## 11. Implicaciones en Bloque 3 y rondas futuras

### Para Bloque 3 R4 — Tool Lifecycle (siguiente)

```
✅ 57 tools registradas (foundation B2)
✅ Permission model granular per tool
✅ require_confirmation flag en sensitive (P3)
✅ Hot-reload event-driven (B1)
✅ Resource quotas Docker per tier

4.3.1 Tool authorization workflows:
   → Human-in-loop refinement (Telegram inline keyboard ready)
   → Dry-run para destructive operations
   → Approval workflow audit chain

4.3.2 Tool versioning + rollback:
   → Image SHA pinned (B2 K8s-ready)
   → Rollback via docker image tag
   → Audit version transitions

4.3.3 Tool testing & sandbox:
   → Container sandbox dedicado
   → Mock secrets (4.1.4) para tests
   → CI/CD integration foundation R10
```

### Para R5 — Orchestration / Multi-Agent

```
✅ MCP tools shared accesibles desde sub-agents
✅ Workspace isolation respetada
✅ Telegram canal bidireccional ready
✅ AgentDelegationTool foundation (B2 3.2.4)

R5 decidirá:
   • Nodo 8 Tálamo (routing inteligente 57 tools)
   • Multi-Agent Network lifecycle
   • Sub-agent containers (Capa 3 extensible)
```

### Para R6 — Memory Stack extensions

```
✅ Files indexables como memoria (Filesystem MCP)
✅ Conversaciones Telegram → memoria episódica

R6 decidirá:
   • File-to-memory indexing
   • Telegram conversation history
   • Cross-channel memory consolidation
```

### Para R7 — Frontend / Channel

```
✅✅ PlatformAdapter ABC (foundation multi-canal)
✅ NormalizedMessage abstracta
✅ Webhook handler pattern validado (Telegram)
✅ Approval flow P3 funcional

R7 decidirá:
   • Discord/Slack/WhatsApp adapters (sin reescribir core)
   • Web dashboard cliente
   • Mobile apps (futuro)
   • Multi-channel mirroring (foundation Hermes)
```

### Para R8 — Observability completa

```
✅ ~32 métricas Prometheus nuevas en B2
✅ Audit chain extendido per MCP server
✅ Docker container metrics nativos

R8 decidirá:
   • Grafana dashboards per MCP server
   • Alerting rules específicas
   • Cross-server tracing
```

### Para R9 — Security / Compliance

```
✅✅ SSRF protection 5-capa (HTTP)
✅✅ Path traversal protection (Filesystem)
✅ HMAC signature validation (Telegram, GitHub webhook)
✅ PAT/bot_token KEK encryption (4.1.4)
✅ Audit per-tool-call inmutable
✅ OWASP LLM Top 10 compliance HTTP

R9 decidirá:
   • Nodo 8 Amígdala (security checks pre-execution)
   • Prompt injection detection
   • Adversarial eval per tool
   • SOC2 / ISO27001 audit path (R4 B2 contribuye fuerte)
```

### Para R10 — CI/CD / Deploy

```
✅ Docker images custom build pattern (3 containers)
✅ Pinned SHA images (K8s-ready)
✅ Health checks formales
✅ Provisioning scripts foundation (B1)

R10 decidirá:
   • CI/CD pipeline GitHub Actions
   • Image scanning Trivy
   • Deploy strategy (canary, blue-green)
   • Rollback automation
```

---

## 12. Riesgos legítimos aceptados

12 riesgos B2 R4 identificados consolidados, todos mitigables.

### GitHub MCP

```
R1. GitHub MCP server abandonment Anthropic
    IMPACTO: ALTO | MITIGACIÓN: pin version + fork fallback + hybrid (E)

R2. PAT cliente expire/revoked
    IMPACTO: ALTO | MITIGACIÓN: auto-rotation reminder 7 días + health check

R3. PAT con scopes excesivos (admin:org leak)
    IMPACTO: ALTO | MITIGACIÓN: validation al store + recomendar scope 'repo'
```

### Filesystem MCP

```
R4. Path traversal bug en custom code
    IMPACTO: CRÍTICO | MITIGACIÓN: tests exhaustivos + code review + property-based
    + penetration testing pre-prod + audit security_alarm

R5. Volume mount mal configurado
    IMPACTO: CRÍTICO | MITIGACIÓN: provisioning idempotente + tests integration

R6. Workspace excede quota disco
    IMPACTO: MEDIO | MITIGACIÓN: Docker volume size limit + alarma 80% + dashboard
```

### HTTP MCP

```
R7. SSRF bypass via novel technique
    IMPACTO: CRÍTICO | MITIGACIÓN: 5-capa validation + tests CVE patterns
    + audit security_alarm + bug bounty v3

R8. DNS rebinding attack
    IMPACTO: ALTO | MITIGACIÓN: re-resolve antes connect + pin IP en httpx

R9. Cloud metadata IPv6 evasion
    IMPACTO: ALTO | MITIGACIÓN: IPv6 networks blocked + tests específicos
```

### Telegram MCP

```
R10. Bot token leak
     IMPACTO: CRÍTICO | MITIGACIÓN: SecretsManager AES-256-GCM + audit + rotation

R11. Webhook signature bypass attempt
     IMPACTO: ALTO | MITIGACIÓN: hmac.compare_digest timing-safe + audit alarm

R12. Multi-user routing bug Telegram
     IMPACTO: ALTO | MITIGACIÓN: workspace_id validate everywhere + tests cross-workspace
```

---

## Cierre del Bloque 2 R4

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ R4 BLOQUE 2 — MCP SERVERS CORE CERRADO                    ║
║                                                                ║
║   4/4 sub-temas LOCKED                                          ║
║   Score: 9.5/10 (excelente)                                      ║
║   Riesgos legítimos: 12 identificados, todos mitigables          ║
║   Spillover ejecutado:                                           ║
║      ✅ D-017 logged + master R4 actualizado + Estado §3.1.quind║
║      ⏳ Diferido: docs públicos hasta cierre R4 completo         ║
║                                                                  ║
║   Tools concretas disponibles:                                   ║
║   • GitHub: 26 tools (oficial)                                    ║
║   • Filesystem: 12 tools (custom)                                  ║
║   • HTTP: 6 tools (custom + SSRF)                                  ║
║   • Telegram: 8 tools (custom + Hermes)                            ║
║   • + Core LOCAL B2 3.2.4: 5 tools                                  ║
║   ───────────────────────────────────                              ║
║   TOTAL: ~57 tools para agentes                                    ║
║                                                                  ║
║   Costo incremental B2: $0 infra                                  ║
║   Recursos: ~950 MB RAM (4 containers)                            ║
║                                                                  ║
║   Próximo: R4 Bloque 3 — Tool Lifecycle (3 sub-temas)              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```