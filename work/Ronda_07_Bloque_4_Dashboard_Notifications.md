# Ronda 7 — Bloque 4 — Dashboard + Notifications

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 4 de R7. ⭐ CIERRA R7 100%.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Estado original:** ✅ **3/3 sub-temas LOCKED**
**Master doc:** [Ronda_07_Frontend_Channel.md](work/Ronda_07_Frontend_Channel.md)
**Materializa:** Cross-device experience + notifications real + PWA installable

---

## 1. Propósito

R6 6.3.3 lockeó dashboard foundation HTMX minimal.
R7 B4 extiende para producción multi-tenant cliente self-service:
- v2 expansion modules on-demand (P3 R7 LOCKED)
- Notifications system formal multi-channel
- PWA install + mobile + push system-level

---

## 2. Sub-tema 7.4.1 — Dashboard v2 Expansion (C — Module system + global search + charts)

### Module System

```python
class DashboardModule(BaseModel):
    module_id, name, description, icon
    category: 'operations' | 'analytics' | 'admin'
    route_prefix: str
    sections: list[DashboardSection]
    required_permissions: list[str]
    enabled_by_default: bool
    enterprise_only: bool
    order: int
    badge: Optional[str]  # 'NEW' | 'BETA' | 'ENTERPRISE'
```

### 8+ MODULES

**V1 (default — R6 6.3.3):**
- overview (workspace summary)
- skills (GO/NO-GO + lifecycle)
- dmn (status + outputs + settings)
- cost (current + forecast + breakdown)
- audit (search + export)
- settings (general)

**V2 EXPANSION (on-demand):**
- memory (episodes, KG, temporal, health)
- plans (PFC plans history + confidence)
- forgetting (policies + custom rules + GDPR + legal hold)
- eval (recent + regression)
- identities (identities, roles, credentials, sessions)
- integrations (github, webhooks outbound)

### Module Activation Manager

```python
class ModuleActivationManager:
    async def get_active_modules(workspace_id, identity) -> list[DashboardModule]:
        # Filter by:
        # - workspace.activated_modules
        # - identity permissions
        # - tier (enterprise)
        # - module.enabled_by_default
    
    async def activate_module(workspace_id, module_id, activated_by)
    async def deactivate_module(workspace_id, module_id, deactivated_by)
```

### Global Search (5+ resources)

```python
class GlobalSearch:
    SEARCHABLE_RESOURCES = [
        ('queries', QueryHistorySearchAdapter),
        ('plans', PFCPlansSearchAdapter),
        ('skills', SkillsSearchAdapter),
        ('episodes', EpisodesSearchAdapter),  # R6 6.3.1 temporal
        ('audit', AuditSearchAdapter),
    ]
    
    async def search(workspace_id, query, resource_filter=None, limit=20):
        # Parallel adapter search
        # Relevance + recency ranking
```

### Charts Stack
- **Chart.js** (R6 reused): bar, line, doughnut, pie básico
- **Plotly.js** (CDN): heatmaps, sankey, treemap, 3D, network
- **D3.js**: only custom visualizations específicas

### Customization

```python
workspace.dashboard_settings = {
    'theme': 'light' | 'dark' | 'auto',
    'language': 'en' | 'es' | 'pt',  # i18n ready
    'compact_mode': bool,
    'sidebar_position': 'left' | 'right',
    'default_landing': 'overview' | 'queries' | ...,
}
```

### Settings UI Integra TODOS R7 sub-temas

```
/dashboard/settings/modules — activate/deactivate
/dashboard/settings/identities — link R7 7.3
/dashboard/settings/credentials — manage API keys
/dashboard/settings/sessions — list + revoke (R7 7.3.3)
/dashboard/settings/webhooks — webhooks outbound (R7 7.1.2)
/dashboard/settings/integrations/github — GitHub App (R7 7.1.3)
/dashboard/settings/notifications — notification preferences (7.4.2)
/dashboard/settings/dashboard — theme + i18n + layout
```

### Performance Optimizations
- Virtualized lists (long episodes/audits)
- Lazy load module bundles
- Pagination cursor-based (R7 7.1.2 reused)
- Cache aggregated metrics Valkey
- HTMX swap strategies optimized
- Skeleton loaders

### Postgres ALTER

```sql
ALTER TABLE workspaces ADD COLUMN activated_modules TEXT[] DEFAULT '{}';
ALTER TABLE workspaces ADD COLUMN dashboard_settings JSONB DEFAULT '{}';
```

### Audit events (3)
- `dashboard_module_activated`
- `dashboard_module_deactivated`
- `dashboard_global_search_performed`
- `dashboard_customization_updated`

### Stack reused
- R6 6.3.3 HTMX foundation
- R1 HTMX + Tailwind + Chart.js
- R7 7.1.x channels (integrations UI)
- R7 7.2.x output gate (QA Pack rendering)
- R7 7.3.x auth + RBAC + sessions (UI)
- R6 6.3.1 temporal queries (memory module)

---

## 3. Sub-tema 7.4.2 — Notification System Multi-Channel (C — Formal multi-channel)

### NotificationEventCatalog: 15+ events v1

**CRITICAL** (always instant, bypass quiet hours):
- security.cross_workspace_attempt
- security.credential_compromise_detected
- memory.regression_critical
- cost.cap_imminent

**IMPORTANT** (instant, respect quiet hours):
- plan.human_escalation_required
- skill.core_promotion_candidate
- gdpr.request_pending_review
- github.installation_suspended
- cost.threshold_75_reached

**INFO** (digest-compatible):
- skill.applied_first_time
- dmn.run_completed_with_insights
- workspace.identity_invited
- cost.threshold_50_reached

### NotificationPreference per identity

```python
class NotificationPreference(BaseModel):
    identity_id, workspace_id, event_type
    channels: list[str] = ['email', 'in_app']
    delivery_mode: 'instant' | 'digest_daily' | 'digest_weekly'
    suppressed: bool
    quiet_hours_enabled: bool
    quiet_hours_start, quiet_hours_end: int  # 0-23
    quiet_hours_timezone: str  # IANA tz
    webhook_url: Optional[str]
```

### 4 Channels v1

| Channel | Implementation |
|---|---|
| **email** | SMTP local o SendGrid free tier 100/day |
| **webhook** | R7 7.1.2 WebhookOutbound reused (HMAC) |
| **in_app** | Postgres + HTMX SSE real-time push |
| **telegram** | R7 7.1.1 reused, direct chat |

### NotificationOrchestrator Pipeline (7 steps per recipient)

```
1. Get preferences (default si no exist)
2. Check suppressed
3. Check delivery mode (CRITICAL bypass digest)
4. Check quiet hours (CRITICAL bypass)
5. Check rate limit (10/20/50 per urgency)
6. Send per channel + track delivery
7. Handle failures (retry exponential + dead letter)
```

### DigestAggregator
- Cron daily 9 AM per timezone (R2 B3 Arq)
- Aggregate pending notifications since last digest
- Render email digest con summary + details
- Update identity.last_digest_at

### Dead Letter Queue
- Max retries 3 exponential backoff (1, 2, 4 min)
- After max → dead letter
- Brian alert (oncall notification)

### Unsubscribe Flow
- `/unsubscribe/{notification_id}` endpoint (one-click compliance)
- Suppress future of event type for recipient
- Email header `List-Unsubscribe` included

### Postgres tables NEW (4)

```sql
CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    urgency TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    context JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notification_preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL,
    workspace_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    channels TEXT[] DEFAULT '{email, in_app}',
    delivery_mode TEXT DEFAULT 'instant',
    suppressed BOOLEAN DEFAULT false,
    suppressed_at TIMESTAMP,
    suppression_reason TEXT,
    quiet_hours_enabled BOOLEAN DEFAULT false,
    quiet_hours_start INT,
    quiet_hours_end INT,
    quiet_hours_timezone TEXT,
    webhook_url TEXT,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (identity_id, event_type)
);

CREATE TABLE notification_deliveries (
    delivery_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notification_id UUID NOT NULL,
    identity_id UUID NOT NULL,
    channel TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    reason TEXT,
    sent_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE in_app_notifications (
    in_app_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notification_id UUID NOT NULL,
    identity_id UUID NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    urgency TEXT NOT NULL,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Audit events (8)
- `notification_orchestrated`
- `notification_suppressed_by_preference`
- `notification_rate_limited`
- `notification_delivery_error`
- `notification_unsubscribed`
- `notification_dead_letter`
- `notification_digest_sent`
- `notification_preference_updated`

### Stack reused
- R7 7.1.1 Telegram bot (TelegramChannel)
- R7 7.1.2 WebhookOutbound (WebhookChannel)
- R7 7.2.3 SSE streaming events (in-app push)
- R7 7.3.x identity + RBAC + sessions (recipients)
- R2 B3 Valkey (rate limit) + Arq (digest cron + retry)

---

## 4. Sub-tema 7.4.3 — Mobile-Responsive + PWA Support (C — PWA completo)

### 8 Core Components

1. **Responsive Mobile-First** (Tailwind R6 extended)
2. **PWA Manifest** (/static/manifest.json)
3. **Service Worker** (4 cache strategies)
4. **PushSubscriptionManager** (backend VAPID)
5. **PushChannel** (extends 7.4.2 NotificationOrchestrator)
6. **Frontend PWA Registration** (install prompt + push subscribe)
7. **Offline Queue** (IndexedDB + background sync)
8. **Mobile-Specific Features** (bottom nav + FAB + gestures + native APIs)

### PWA Manifest

```json
{
  "name": "For3s OS",
  "short_name": "For3s",
  "display": "standalone",
  "icons": [192x192, 512x512 maskable],
  "shortcuts": [Submit Query, Skills],
  "categories": ["productivity", "developer"]
}
```

### Service Worker Cache Strategies

| Strategy | Routes | Behavior |
|---|---|---|
| **Network-first** | /api/* | Fresh data, cache fallback |
| **Cache-first** | /static/* | Assets long-cached |
| **Stale-while-revalidate** | /dashboard/* | Fast + update background |
| **Offline fallback** | /offline.html | When all fails |

### Push Notifications System-Level

```python
class PushSubscriptionManager:
    VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY, VAPID_EMAIL
    
    async def subscribe(identity_id, subscription: PushSubscriptionData)
    async def send_push(identity_id, notification) -> ChannelDeliveryResult
        # pywebpush library
        # Iterate subscriptions per identity
        # Handle 410 expired (delete subscription)


class PushChannel(NotificationChannel):
    """Add to 7.4.2 CHANNEL_REGISTRY['push']."""
    async def send(notification, recipient):
        return await push_subscription_manager.send_push(
            recipient.identity_id, notification,
        )
```

### Background Sync Offline Queue

```javascript
// IndexedDB pending-actions store
// HTMX intercept beforeRequest if offline
// Service worker sync on online event
// Auto-retry with conflict resolution
```

### Mobile-Specific Features
- Bottom navigation (replace sidebar mobile)
- Pull-to-refresh (HTMX trigger)
- Swipe gestures (action sheets)
- Touch targets 44px+ (Apple HIG)
- Floating Action Button (FAB submit query)
- Sheet modals (slide-up actions)
- Camera API (scan API key QR)
- Web Share API (share QA Pack)
- Clipboard API (copy code snippets)
- WebAuthn biometric (Face ID / fingerprint login)

### iOS Limitations Mitigated
- PWA install: iOS 16.4+ only
- Push notifications: iOS 16.4+ only
- Fallback: Telegram channel (R7 7.1.1) for older iOS users

### Endpoints NEW

```
GET    /static/manifest.json (PWA manifest)
GET    /static/service-worker.js
GET    /static/icons/icon-{192,512}.png
POST   /api/v1/push/subscribe
DELETE /api/v1/push/subscriptions/{id}
GET    /offline.html (fallback)
```

### Postgres table NEW (1)

```sql
CREATE TABLE push_subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL,
    endpoint TEXT NOT NULL,
    p256dh_key TEXT NOT NULL,
    auth_key TEXT NOT NULL,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (identity_id) REFERENCES identities(identity_id),
    UNIQUE (identity_id, endpoint)
);
```

### Audit events (6)
- `push_subscription_created`
- `push_subscription_revoked`
- `push_notification_sent`
- `pwa_installed` (analytics)
- `offline_action_queued`
- `offline_action_synced`

### Stack reused
- R6 6.3.3 Tailwind responsive base
- R7 7.4.1 Dashboard modules
- R7 7.4.2 NotificationChannel pattern (PushChannel)
- R2 B3 Valkey (push subscription cache)
- R7 7.1.1 Telegram (fallback iOS users)

---

## 5. Eventos audit Bloque 4

Total events nuevos R7 B4: **~17 events**

Dashboard v2 (7.4.1): 3 events
Notifications (7.4.2): 8 events
PWA (7.4.3): 6 events

---

**Bloque 4 ✅ CERRADO — Cross-device experience + notifications real v1. R7 100% CERRADO ⭐⭐⭐**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_07_Bloque_4_Dashboard_Notifications.md`).
