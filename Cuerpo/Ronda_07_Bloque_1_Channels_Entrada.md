# Ronda 7 — Bloque 1 — Channels de Entrada

**Sub-doc detallado del Bloque 1 de R7.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Status:** ✅ **3/3 sub-temas LOCKED**
**Master doc:** [Ronda_07_Frontend_Channel.md](Ronda_07_Frontend_Channel.md)
**Materializa:** Grafo Maestro INPUT layer (PR · Query · Comando · Webhook · CI/CD)

---

## 1. Propósito

Channels INPUT = puertas de entrada a For3s OS. Sin estos:
- Cliente no puede interactuar
- Telegram bot R4 4.2.4 (tool) no funciona como interfaz cliente
- Wedge QA central (PR analysis automático) imposible
- Integraciones B2B externas bloqueadas

---

## 2. Sub-tema 7.1.1 — Telegram Production (C — Webhook 8 components)

### 8 Core Components

1. **TelegramProductionAdapter** (main coordinator)
2. **TelegramIdentityMapper** (user → workspace + role)
3. **TelegramConversationStore** (Valkey state TTL 24h)
4. **TelegramRateLimiter** (Token Bucket per user/ws)
5. **TelegramCommandRegistry** (auto-discovery /help)
6. **Long-running handler** (Arq queue + delayed delivery)
7. **Secret token validation** (security HMAC)
8. **FastAPI webhook endpoint**

### Flow per message (9 steps)

```
1. Telegram → POST /telegram/webhook + secret token
2. Validate secret token
3. Parse update
4. Identity mapping (telegram_user_id → workspace + role)
5. Rate limit check (user + workspace)
6. Load conversation state (Valkey)
7. Route to backend (R5 + R6 reused)
8. Deliver response (short/medium/long)
9. Update conversation state
```

### Postgres table NEW

```sql
CREATE TABLE telegram_identities (
    telegram_user_id BIGINT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    role TEXT NOT NULL,
    active BOOLEAN DEFAULT true,
    invited_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
);
```

### Audit events (6)
- `telegram_message_received`
- `telegram_long_running_queued`
- `telegram_user_registered`
- `telegram_unknown_user_attempted`
- `telegram_rate_limit_exceeded`
- `SECURITY_telegram_webhook_invalid_secret`

### Stack reused
- R4 4.2.4 Hermes patterns + PTB
- R2 B3 Valkey + Arq
- R3 B3 Token Bucket + SSE
- R4 4.3.1 Authorization
- R5 + R6 routing + planning
- Cloudflare Tunnel D-009 LOCKED

---

## 3. Sub-tema 7.1.2 — REST API Formal (C — 8 components + OpenAPI)

### 8 Core Components

1. **APIVersioning** (URL-based v1, v2)
2. **APIAuthentication** (api_key + bearer + OAuth2)
3. **APIKeyManager** (f3s_ prefix + scopes + expires)
4. **APIPagination** (cursor-based)
5. **APIErrorEnvelope** (consistent + trace_id)
6. **APIRateLimiter** (per API key per endpoint)
7. **StreamingEndpoint** (SSE R3 B3 reused)
8. **WebhookOutbound** (HMAC signed callbacks)

### URL Structure

```
/api/v1/* — cliente endpoints (auth required)
/admin/v1/* — Brian only
/webhooks/incoming/* — inbound webhooks
/api/v1/system/{health,version} — sin auth
/api/v1/openapi.json — spec auto-generated
/docs — Swagger UI
/redoc — ReDoc UI
```

### 11 Endpoint Groups

```
workspaces/ (CRUD)
queries/ (POST sync/async/stream + GET + cancel)
skills/ (GET + toggle + feedback + approve)
dmn/ (status + outputs + settings)
plans/ (list + detail + confidence)
forgetting/ (policy + GDPR + legal hold)
cost/ (current + forecast + breakdown)
eval/ (recent + regression)
audit/ (search + export)
webhooks/ (configure + test)
system/ (health + version + openapi)
```

### Queries endpoint modes
- **sync**: wait response (max 60s)
- **async**: return job_id, poll
- **stream**: SSE streaming

### Postgres tables NEW (2)

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    key_hash TEXT UNIQUE NOT NULL,
    scopes TEXT[] NOT NULL,
    active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP,
    created_by TEXT NOT NULL
);

CREATE TABLE webhook_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id TEXT NOT NULL,
    url TEXT NOT NULL,
    events TEXT[] NOT NULL,
    secret_hash TEXT NOT NULL,
    active BOOLEAN DEFAULT true,
    failure_count INT DEFAULT 0
);
```

### Audit events (7)
- `api_request_received`
- `api_authentication_failed`
- `api_rate_limit_exceeded`
- `api_key_created`
- `api_key_revoked`
- `webhook_outbound_triggered`
- `webhook_outbound_failed`

### SDK generation
- OpenAPI 3.0 spec auto-generated FastAPI
- openapi-generator: Python + TypeScript v1
- Go SDK defer v2

### Stack reused
- R3 B3 SSE + Token Bucket
- R4 4.3.1 Authorization
- R5 + R6 routing + planning
- R6 6.3.3 dashboard endpoints internos formalized

---

## 4. Sub-tema 7.1.3 — GitHub Webhook Integration (C — GitHub App 8 components)

### 8 Core Components

1. **GitHub App registration** (Brian ONE TIME setup)
2. **GitHubAppClient** (JWT + installation tokens + cache)
3. **GitHubWebhookReceiver** (validate + dedup + dispatch)
4. **Installation Mapper** (installation_id → workspace_id)
5. **Event Handlers** (4 event types v1)
6. **Async Processing** (Arq jobs)
7. **Installation Callback** (cliente install flow)
8. **Manual Replay Endpoint** (debugging)

### Webhook flow (11 steps)

```
1. GitHub event → POST /webhooks/incoming/github
2. Read raw body (signature validation)
3. Verify HMAC SHA256
4. Parse payload
5. Map installation_id → workspace_id
6. Dedup check (delivery_id Valkey TTL 24h)
7. Record delivery (Postgres audit)
8. Enqueue Arq job
9. Return 200 OK <10s
10. Arq worker procesa async (via PFC R6)
11. Post comment back via GitHub MCP (R4 4.2.1)
```

### Install flow

```
1. Cliente: https://github.com/apps/for3s-os → Install
2. Selecciona repos (single/multiple/all)
3. GitHub redirect /github/callback?installation_id=X&state=workspace_id
4. For3s OS persist installation
5. Redirect dashboard /dashboard?installed=github
```

### Permissions least privilege
- Repository: Pull requests (read & write)
- Repository: Contents (read)
- Repository: Issues (read & write)
- Repository: Checks (read & write)
- Repository: Actions (read)

### Events v1 supported
- `pull_request` (opened, synchronized, reopened)
- `pull_request_review`
- `issue_comment` (@for3s-bot mention)
- `workflow_run` (completed)

### Postgres tables NEW (2)

```sql
CREATE TABLE github_installations (
    installation_id BIGINT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    account_login TEXT NOT NULL,
    account_type TEXT NOT NULL,
    repository_selection TEXT NOT NULL,
    repositories JSONB,
    permissions JSONB,
    events JSONB,
    active BOOLEAN DEFAULT true,
    installed_by TEXT NOT NULL,
    installed_at TIMESTAMP DEFAULT NOW(),
    suspended_at TIMESTAMP
);

CREATE TABLE github_webhook_deliveries (
    delivery_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    installation_id BIGINT NOT NULL,
    event_type TEXT NOT NULL,
    action TEXT,
    repo_full_name TEXT,
    received_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    processing_status TEXT,
    payload JSONB
);
```

### Audit events (8)
- `github_webhook_received`
- `github_app_installed`
- `github_pr_analysis_completed`
- `github_webhook_replayed`
- `github_webhook_processing_failed`
- `SECURITY_github_webhook_invalid_signature`
- `github_webhook_duplicate_delivery`
- `github_event_unsupported`

### Stack reused
- R2 B3 Valkey (token cache + dedup) + Arq
- R4 4.2.1 GitHub MCP (post comments)
- R4 4.3.1 Authorization
- R5 + R6 routing + planning
- R7 7.1.2 REST API patterns

---

## 5. Eventos audit Bloque 1

Total events nuevos R7 B1: **~21 events**

Telegram (7.1.1): 6 events
REST API (7.1.2): 7 events
GitHub (7.1.3): 8 events

Todos workspace-scoped, payload preview ≤200 chars.

---

**Bloque 1 ✅ CERRADO — Foundation Grafo Maestro INPUT layer v1.**