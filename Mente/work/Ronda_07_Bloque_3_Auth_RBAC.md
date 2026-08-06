# Ronda 7 — Bloque 3 — Auth & RBAC Cross-Channel

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 3 de R7.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Estado original:** ✅ **3/3 sub-temas LOCKED**
**Master doc:** [Ronda_07_Frontend_Channel.md](work/Ronda_07_Frontend_Channel.md)
**Materializa:** Pilar 1 Seguridad zero-trust real cross-channel

---

## 1. Propósito

Pilar 1 Grafo Maestro requiere zero-trust real. Sin auth unificado cross-channel:
- Identity fragmentada (Telegram + API + GitHub no linked)
- Audit fragmentado per channel
- Permissions duplicadas inconsistentes
- Revocation no propaga cross-channel
- Cliente B2B abandona (UX)

---

## 2. Sub-tema 7.3.1 — Authentication Unificado (C — Identity central + multi-credential)

### Models (3 Pydantic)

```python
class Identity(BaseModel):
    identity_id: str
    workspace_id: str
    display_name: str
    email: Optional[str]
    active: bool
    created_at, last_active_at: datetime

class IdentityCredential(BaseModel):
    credential_id: str
    identity_id: str
    credential_type: str  # 6 types v1
    credential_value_hash: str
    channel: str
    label, scopes, expires_at: optional
    active, revoked_*: lifecycle

class AuthContext(BaseModel):
    identity_id, workspace_id, display_name
    credential_id, credential_type, channel
    roles, scopes
    authenticated_at, trace_id
```

### 6 Credential Types

| Type | Channel | Example |
|---|---|---|
| telegram | telegram | telegram_user_id |
| api_key | api | f3s_xxx... |
| bearer_jwt | api | JWT token |
| oauth2_session | dashboard | session cookie |
| github_app | github_webhook | installation_id |
| cli_token | cli | CLI long-lived |

### UnifiedAuthenticator Pipeline (7 steps)

```
1. Verify credential per type (hash lookup)
2. Check credential active + not expired
3. Get identity + active check
4. Resolve roles + effective scopes (R4 4.3.1 RBAC)
5. Update last_used + use_count
6. Build AuthContext
7. Audit success
```

### 3 Channel Adapters Refactored

```python
class TelegramAuthAdapter:
    async def authenticate_update(self, update) -> AuthContext:
        return await unified_authenticator.authenticate(
            credential_type='telegram',
            credential_value=str(update.effective_user.id),
            channel_context={...}
        )

class APIAuthAdapter:
    async def authenticate_request(self, request) -> AuthContext:
        # Try api_key → bearer_jwt → oauth2_session
        ...

class GitHubAuthAdapter:
    async def authenticate_webhook(self, installation_id, signature, body):
        # Verify HMAC + use unified
        ...
```

### Credential Management API

- `add_credential(identity_id, type, value, scopes, expires_at)`
- `revoke_credential(credential_id, revoked_by, reason)`
- `list_credentials_for_identity(identity_id)`

### Migration from R7 B1 tables

```sql
-- telegram_identities → identities + credentials
INSERT INTO identities (workspace_id, display_name, created_by)
SELECT DISTINCT workspace_id, 'Telegram ' || telegram_user_id, invited_by
FROM telegram_identities;

INSERT INTO identity_credentials (identity_id, credential_type, credential_value_hash, channel, scopes)
SELECT i.identity_id, 'telegram',
    encode(sha256(telegram_user_id::text::bytea), 'hex'),
    'telegram', ARRAY[ti.role]
FROM telegram_identities ti
JOIN identities i ON i.workspace_id = ti.workspace_id;

-- Similar for api_keys, github_installations
```

### Postgres tables NEW (2)

```sql
CREATE TABLE identities (
    identity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id TEXT NOT NULL,
    display_name TEXT NOT NULL,
    email TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP,
    created_by TEXT NOT NULL,
    deactivated_at TIMESTAMP,
    deactivated_by TEXT,
    deactivation_reason TEXT,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE identity_credentials (
    credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL,
    credential_type TEXT NOT NULL,
    credential_value_hash TEXT NOT NULL,
    channel TEXT NOT NULL,
    label TEXT,
    scopes TEXT[] DEFAULT '{}',
    expires_at TIMESTAMP,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP,
    use_count INT DEFAULT 0,
    revoked_at TIMESTAMP,
    revoked_by TEXT,
    revocation_reason TEXT,
    FOREIGN KEY (identity_id) REFERENCES identities(identity_id),
    UNIQUE (credential_type, credential_value_hash)
);
```

### Audit events (6)
- `auth_success`
- `auth_failed`
- `credential_added`
- `credential_revoked`
- `identity_created`
- `identity_deactivated`

### Performance
- Valkey cache identity 5min
- Valkey cache credential 1min

---

## 3. Sub-tema 7.3.2 — RBAC Roles + Permissions (C — Hierarchical + workspace-scoped)

### Permission Catalog: 35+ permissions formales

```python
class PermissionCatalog:
    PERMISSIONS = {
        # Queries
        'queries:submit_sync', 'queries:submit_async',
        'queries:cancel', 'queries:read_history',
        # Skills
        'skills:read', 'skills:toggle', 'skills:feedback',
        'skills:approve_core',
        # DMN
        'dmn:read_status', 'dmn:update_settings', 'dmn:approve_output',
        # Forgetting
        'forgetting:read_policy', 'forgetting:update_policy',
        'forgetting:gdpr_request', 'forgetting:legal_hold',
        # Cost
        'cost:read', 'cost:update_caps',
        # Audit
        'audit:read', 'audit:export',
        # Workspace
        'workspace:read', 'workspace:update',
        'workspace:invite_identity', 'workspace:manage_roles',
        # GitHub
        'github:configure', 'github:webhook_replay',
        # Webhooks
        'webhooks:read', 'webhooks:configure',
        # API keys
        'api_keys:create', 'api_keys:revoke', 'api_keys:list',
        # Admin
        'admin:global_view', 'admin:approve_common_stack',
        'admin:system_health',
    }
```

### 5 System Roles Default

| Role | Permissions |
|---|---|
| **workspace_admin** | All except admin:* |
| **workspace_editor** | submit queries + manage skills/dmn + read all |
| **workspace_viewer** | Read-only |
| **workspace_auditor** | Audit + compliance + forgetting read |
| **brian_admin** | ALL including admin:* |

### Custom Workspace Roles
- Cliente creates via API (`workspace:manage_roles`)
- Combines permissions + inherits_from
- Examples: "QA Lead", "Junior Dev"

### Identity × Credential Scope Intersection

```python
effective_permissions = (
    role_permissions(identity)
    & credential_scopes(credential)  # if provided
)
```

### Permission Decorator DRY

```python
@require_permission('queries:submit_async')
async def submit_query(workspace_id, request, auth=Depends(authenticate)):
    # Permission verified, audit auto
    ...
```

### Conditional Permissions
Patterns reused from R4 4.3.1:
- `time_window` (only during business hours)
- `resource_owner` (only if creator)
- `workspace_setting` (only if setting=True)

### RBAC Resolver

```python
class RBACResolver:
    async def get_roles_for_identity(identity) -> list[Role]:
        # Cache Valkey 5min
        # Resolve inheritance
        ...
    
    async def resolve_effective_permissions(identity, credential=None):
        roles = await self.get_roles_for_identity(identity)
        role_permissions = set(union all permissions)
        if credential:
            return role_permissions & set(credential.scopes)
        return role_permissions
    
    async def check_permission(auth_context, required, context=None) -> bool:
        if required in auth_context.scopes:
            return await self._check_conditional(...)
        return False  # deny-by-default
```

### Postgres tables NEW (2)

```sql
CREATE TABLE roles (
    role_id TEXT PRIMARY KEY,
    workspace_id TEXT,  -- NULL = global system role
    name TEXT NOT NULL,
    description TEXT,
    permissions TEXT[] NOT NULL DEFAULT '{}',
    inherits_from TEXT[] DEFAULT '{}',
    conditional_permissions JSONB DEFAULT '[]',
    active BOOLEAN DEFAULT true,
    is_system_role BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by TEXT,
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE identity_role_assignments (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL,
    role_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    assigned_at TIMESTAMP DEFAULT NOW(),
    assigned_by TEXT NOT NULL,
    expires_at TIMESTAMP,
    revoked_at TIMESTAMP,
    revoked_by TEXT,
    revocation_reason TEXT,
    UNIQUE (identity_id, role_id, workspace_id)
);
```

### Cache
- Valkey `identity_roles:{identity_id}` TTL 5min
- Invalidate on role change

### Audit events (7)
- `permission_granted` (per check)
- `permission_denied`
- `role_created`
- `role_updated`
- `role_deleted`
- `role_assigned`
- `role_revoked`

### Deny-by-default principle
Si permission NO en auth_context.scopes → deny + audit.

---

## 4. Sub-tema 7.3.3 — Session Management + Refresh (C — Sessions DB + per-channel)

### Session Model

```python
class Session(BaseModel):
    session_id: str
    identity_id, credential_id, workspace_id, channel: str
    
    access_token_hash: str
    refresh_token_hash: Optional[str]
    
    # Permissions snapshot (avoid re-resolve)
    cached_permissions: list[str]
    permissions_snapshot_at: datetime
    
    created_at, last_used_at, expires_at: datetime
    refresh_expires_at: Optional[datetime]
    
    device_info: dict
    
    revoked_at, revoked_by, revocation_reason: Optional
    active: bool = True
```

### 5 Per-Channel Strategies

| Channel | Access TTL | Refresh TTL | Sliding | CSRF |
|---|---|---|---|---|
| dashboard | 1h | 7d | ✅ | ✅ |
| api | 1h | 30d | ❌ | ❌ |
| telegram | 30d | none | ✅ | ❌ |
| github_webhook | stateless | n/a | n/a | n/a |
| cli | 90d | none | ❌ | ❌ |

### SessionManager Pipeline

```python
class SessionManager:
    async def create_session(auth_context, device_info) -> SessionCreated:
        # Generate access + refresh tokens
        # Resolve permissions snapshot (avoid re-resolve per request)
        # Persist DB + cache Valkey
    
    async def verify_session(access_token) -> Optional[AuthContext]:
        # Cache lookup first (Valkey ~1ms)
        # DB fallback if cache miss
        # Validate active + expires
        # Check credential still active (cascade)
        # Sliding window extend async
    
    async def refresh_session(refresh_token) -> Optional[SessionCreated]:
        # Token rotation security
        # Re-resolve permissions
        # New access + new refresh
    
    async def revoke_session(session_id, revoked_by, reason)
    async def revoke_all_sessions_for_identity(identity_id, ...)
    async def revoke_all_sessions_for_credential(credential_id, ...)  # cascade
```

### CSRF Protection (dashboard only)

```python
class CSRFTokenManager:
    CSRF_TOKEN_TTL = 3600
    async def generate_token(session_id) -> str
    async def verify_token(session_id, token) -> bool
```

### FastAPI Endpoints

```
POST   /auth/sessions (login)
POST   /auth/sessions/refresh
DELETE /auth/sessions/{id}
DELETE /auth/sessions (logout all)
GET    /auth/sessions (list active)
```

### Cascade Revocation
- Credential revoked (R7 7.3.1) → auto-revoke all sessions
- Role changed (R7 7.3.2) → invalidate cache + force refresh

### Postgres table NEW (1)

```sql
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL,
    credential_id UUID NOT NULL,
    workspace_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    
    access_token_hash TEXT NOT NULL,
    refresh_token_hash TEXT,
    
    cached_permissions TEXT[] NOT NULL DEFAULT '{}',
    permissions_snapshot_at TIMESTAMP NOT NULL,
    
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    refresh_expires_at TIMESTAMP,
    
    device_info JSONB DEFAULT '{}',
    
    revoked_at TIMESTAMP,
    revoked_by TEXT,
    revocation_reason TEXT,
    
    active BOOLEAN DEFAULT true,
    UNIQUE (access_token_hash)
);
```

### Cleanup Cron
Daily 2 AM (R2 B3 Arq reused). Delete expired > 30 days.

### Audit events (6)
- `session_created`
- `session_refreshed`
- `session_refresh_failed`
- `session_revoked`
- `all_sessions_revoked`
- `sessions_cleanup_completed`

### Performance
- Valkey cache `session:{token_hash}` ~1ms lookup
- DB fallback si cache miss
- Sliding update async (no bloquea request)

---

## 5. Eventos audit Bloque 3

Total events nuevos R7 B3: **~19 events**

Identity (7.3.1): 6 events
RBAC (7.3.2): 7 events
Sessions (7.3.3): 6 events

---

**Bloque 3 ✅ CERRADO — Foundation Pilar 1 zero-trust real cross-channel v1.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_07_Bloque_3_Auth_RBAC.md`).
