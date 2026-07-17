# Ronda 7 — Frontend / Channel (Master)

**Séptima de las 10 rondas técnicas. Documento maestro de R7.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-07
**Última actualización:** 2026-06-07
**Estatus:** ✅ **R7 CERRADO 100%** (4 bloques · 12/12 sub-temas LOCKED)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — INPUT layer + OUTPUT GATE + OUTPUT layer
- [Mente/Cuerpo/Ronda_06_Memory_Stack_Extensions.md](Ronda_06_Memory_Stack_Extensions.md) — R6 100% CERRADO
- [Mente/Cuerpo/Ronda_05_Orchestration_Multi_Agent.md](Ronda_05_Orchestration_Multi_Agent.md) — R5 100% CERRADO
- [Mente/Doc/Estado_Sesion_Continuidad.md](../Doc/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Sub-documentos detallados:**
- ✅ [Ronda_07_Bloque_1_Channels_Entrada.md](Ronda_07_Bloque_1_Channels_Entrada.md) — Channels de Entrada (3/3 LOCKED)
- ✅ [Ronda_07_Bloque_2_Output_Gate.md](Ronda_07_Bloque_2_Output_Gate.md) — Output Gate Pilar 1 (3/3 LOCKED)
- ✅ [Ronda_07_Bloque_3_Auth_RBAC.md](Ronda_07_Bloque_3_Auth_RBAC.md) — Auth & RBAC Cross-Channel (3/3 LOCKED)
- ✅ [Ronda_07_Bloque_4_Dashboard_Notifications.md](Ronda_07_Bloque_4_Dashboard_Notifications.md) — Dashboard + Notifications (3/3 LOCKED) ⭐ CIERRA R7

**Decisiones loggeadas en for3s-inter:**
- [D-027 — Stack Channels de Entrada LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-028 — Stack Output Gate LOCKED + Pilar 1 completo](../../for3s-inter/07-operations/decision-log.md)
- [D-029 — Stack Auth & RBAC Cross-Channel LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-030 — Stack Dashboard + Notifications LOCKED + R7 100% CERRADO](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core
- 3.D — Equipo pequeño (cliente self-service)

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes
- P3 — Workspace isolation
- P4 — Encryption at rest

---

## Tabla de contenidos

1. [Propósito de R7](#1-propósito-de-r7)
2. [Pre-preguntas P1-P3 LOCKED](#2-pre-preguntas-p1-p3-locked)
3. [Estructura B+A — 4 bloques · 12 sub-temas](#3-estructura-ba--4-bloques--12-sub-temas)
4. [Resumen ejecutivo Bloque 1 — Channels de Entrada](#4-resumen-ejecutivo-bloque-1)
5. [Resumen ejecutivo Bloque 2 — Output Gate](#5-resumen-ejecutivo-bloque-2)
6. [Resumen ejecutivo Bloque 3 — Auth & RBAC](#6-resumen-ejecutivo-bloque-3)
7. [Resumen ejecutivo Bloque 4 — Dashboard + Notifications](#7-resumen-ejecutivo-bloque-4)
8. [Cobertura del Grafo Maestro](#8-cobertura-del-grafo-maestro)
9. [Pilar 1 Seguridad COMPLETO](#9-pilar-1-seguridad-completo)
10. [Costo total v1 actualizado post-R7](#10-costo-total-v1-actualizado-post-r7)
11. [Riesgos consolidados R7 + mitigaciones](#11-riesgos-consolidados)
12. [Próximos pasos R8](#12-próximos-pasos-r8)

---

## 1. Propósito de R7

R7 — Frontend / Channel es la **interfaz al mundo exterior** de For3s OS. Rondas anteriores construyeron el cerebro completo (R1-R6, 10/11 nodos Grafo Maestro). R7 expone ese cerebro a:

- **INPUT layer:** PR · Query · Comando · Webhook · CI/CD (Grafo Maestro líneas 173-175)
- **OUTPUT layer:** QA Pack + Trace + Confidence + Audit (Grafo Maestro líneas 274-277)
- **OUTPUT GATE:** Firma criptográfica + Trace completo + Encripta (Pilar 1 — Grafo Maestro líneas 266-271)

**R7 responde:** ¿cómo USUARIO/CLIENTE interactúa con For3s OS?

Sin R7, For3s OS es un cerebro encerrado. Con R7, es un sistema accesible cross-channel multi-tenant compliance-defendible.

---

## 2. Pre-preguntas P1-P3 LOCKED

| # | Pregunta | Decisión | Justificación |
|---|---|---|---|
| **P1** | Channels INPUT v1 | **C — Telegram + REST + GitHub webhook** | Cubre wedge QA central + integraciones B2B |
| **P2** | Output Gate strict vs pragmatic | **C — Híbrido pragmatic default + strict opt-in** | Compliance gradiente per tier |
| **P3** | Dashboard expansion v1 | **C — Progressive enhancement** | Cliente self-service activate sections on-demand |

---

## 3. Estructura B+A — 4 bloques · 12 sub-temas

```
BLOQUE 1 — CHANNELS DE ENTRADA
   7.1.1 ✅ Telegram production (C — Webhook 8 components)
   7.1.2 ✅ REST API formal (C — 8 components + OpenAPI)
   7.1.3 ✅ GitHub webhook integration (C — GitHub App 8 components)

BLOQUE 2 — OUTPUT GATE (Pilar 1 Seguridad)
   7.2.1 ✅ Output signing + trace + encrypt (C — Híbrido P2 LOCKED)
   7.2.2 ✅ Response format estructurado (C — Pydantic + 4 renderers)
   7.2.3 ✅ Streaming output unificado (C — 25+ events + 4 adapters)

BLOQUE 3 — AUTH & RBAC CROSS-CHANNEL
   7.3.1 ✅ Authentication unificado (C — Identity central + credentials)
   7.3.2 ✅ RBAC roles + permissions (C — Hierarchical + workspace + composition)
   7.3.3 ✅ Session management + refresh (C — Sessions DB + per-channel)

BLOQUE 4 — DASHBOARD + NOTIFICATIONS
   7.4.1 ✅ Dashboard v2 expansion (C — Module system + global search + charts)
   7.4.2 ✅ Notification system (C — Formal multi-channel + preferences + digest)
   7.4.3 ✅ PWA + responsive (C — PWA completo + push system-level)

TOTAL R7: 4 bloques · 12 sub-temas · 12/12 LOCKED ✅
```

---

## 4. Resumen ejecutivo Bloque 1 — Channels de Entrada

**Materializa: Grafo Maestro INPUT layer (PR · Query · Comando · Webhook · CI/CD)**

### 7.1.1 — Telegram Production: Webhook 8 components
- Webhook /telegram/webhook + secret_token validation
- TelegramProductionAdapter coordinator
- TelegramIdentityMapper (user → workspace + role)
- TelegramConversationStore (Valkey TTL 24h)
- TelegramRateLimiter (Token Bucket per user + workspace)
- TelegramCommandRegistry (auto-discovery /help)
- Long-running handler (Arq queue + delayed delivery)
- POSTGRES: `telegram_identities`
- Cloudflare Tunnel D-009 compatible

### 7.1.2 — REST API Formal: 8 components + OpenAPI
- APIVersioning (URL-based v1, v2)
- APIAuthentication (api_key + bearer + OAuth2)
- APIKeyManager (f3s_ prefix + scopes + expires)
- APIPagination (cursor-based)
- APIErrorEnvelope (consistent + trace_id)
- APIRateLimiter (per API key per endpoint)
- StreamingEndpoint (SSE R3 B3 reused)
- WebhookOutbound (HMAC signed callbacks)
- 11 endpoint groups: workspaces, queries, skills, dmn, plans, forgetting, cost, eval, audit, webhooks, system
- POSTGRES: `api_keys`, `webhook_configs`
- OpenAPI 3.0 spec auto-generated + SDK generation

### 7.1.3 — GitHub Webhook: GitHub App 8 components ⭐ wedge QA central
- GitHub App formal (1-click install multi-repo)
- GitHubAppClient (JWT + installation tokens + cache)
- GitHubWebhookReceiver (HMAC signature + dedup + dispatch)
- Installation Mapper (installation_id → workspace_id)
- 4 event handlers: pull_request, review, issue_comment, workflow_run
- Async processing (Arq jobs, no GitHub timeout)
- Installation callback + manual replay endpoint
- POSTGRES: `github_installations`, `github_webhook_deliveries`
- Permissions least privilege explicit

---

## 5. Resumen ejecutivo Bloque 2 — Output Gate

**Materializa: Grafo Maestro Output Gate (Pilar 1) líneas 266-271**

### 7.2.1 — Output Signing + Trace + Encrypt: Híbrido P2 LOCKED
- **TIER PRAGMATIC** (default 80% workspaces):
  - HMAC-SHA256 signature
  - Trace básico (plan_id + nodes + confidence + cost)
  - TLS 1.3 transport
  - Overhead <10ms
- **TIER STRICT** (enterprise opt-in):
  - Ed25519 signature (non-repudiation)
  - Trace completo (every node + reasoning)
  - AES-256-GCM payload encrypt (KEK R4 4.1.3 reused)
  - Overhead 50-100ms
  - Key rotation supported
- 5 components: OutputGate + WorkspaceKeyManager + SignatureStore + OutputVerifier + TraceBuilder
- POSTGRES: `workspace_signing_keys`, `output_signatures`
- Verification SDK cliente

### 7.2.2 — Response Format Estructurado: Pydantic + 4 renderers
- **QA Pack universal** (Grafo Maestro literal):
  - 8 Pydantic models (QAPack + Section + Item + Location + Attachment + Action + Metadata + Error)
  - sections + items + attachments + actions structured
  - metadata rica (confidence + cost + performance + trace)
- **4 RENDERERS:**
  - TelegramRenderer (markdown max 4k + dashboard link)
  - APIRenderer (JSON OpenAPI)
  - GitHubRenderer (markdown collapsible + suggestions)
  - DashboardRenderer (HTML Jinja2 rich UI)
- QAPackRendererRegistry (channel → renderer auto)
- Versioning qa_pack_version "1.0"
- Multi-language ready (i18n field)

### 7.2.3 — Streaming Output Unificado: 25+ events + 4 adapters
- **25+ StreamEventType:**
  - Lifecycle (STREAM_START/END/ERROR/CANCELLED/HEARTBEAT)
  - PFC (PLAN_GENERATED, STEP_*, RE_PLAN_TRIGGERED, COMPLETED)
  - Skills (APPLIED, FALLBACK_TO_PLANNING)
  - Multi-Agent (SPECIALIST_*, CONSOLIDATING)
  - LLM (TEXT_DELTA, TOOL_USE)
  - Metadata (CONFIDENCE_UPDATED, COST_UPDATE)
  - QA Pack (SECTION_ADDED, ITEM_FOUND, QA_PACK_FINAL)
  - Final (SIGNED_OUTPUT)
- **4 channel adapters:**
  - SSEStreamAdapter (REST)
  - TelegramStreamAdapter (typing + edit msg + rate limit)
  - GitHubStreamAdapter (check_run progress + PR comment)
  - DashboardStreamAdapter (HTMX SSE)
- StreamingExecutor wraps PFCExecutor
- StreamCancellationManager + StreamHeartbeat (R3 B3 reused)
- Progress percentage + cumulative cost tracking

---

## 6. Resumen ejecutivo Bloque 3 — Auth & RBAC Cross-Channel

### 7.3.1 — Authentication Unificado: Identity central + multi-credential
- 3 Pydantic models: Identity + IdentityCredential + AuthContext
- 6 credential types: telegram, api_key, bearer_jwt, oauth2_session, github_app, cli_token
- UnifiedAuthenticator 7-step pipeline
- 3 channel adapters refactored (Telegram + API + GitHub)
- Credential management API (add/revoke/list)
- Migration scripts desde R7 B1 tables
- POSTGRES: `identities`, `identity_credentials`
- Cache Valkey 5min identity + 1min credential

### 7.3.2 — RBAC Roles + Permissions: Hierarchical + workspace-scoped
- PermissionCatalog 35+ permissions formales
- 5 system roles: workspace_admin, editor, viewer, auditor, brian_admin
- Custom workspace-scoped roles (cliente self-service)
- Inheritance + composition + conditional permissions
- Identity × Credential scope intersection
- @require_permission decorator DRY
- POSTGRES: `roles`, `identity_role_assignments`
- Cache identity_roles Valkey TTL 5min

### 7.3.3 — Session Management + Refresh: Sessions DB + per-channel
- 5 per-channel strategies:
  - dashboard: 1h access + 7d refresh, sliding, CSRF, cookies
  - api: 1h access + 30d refresh, fixed
  - telegram: 30d access, sliding, no refresh
  - github_webhook: stateless
  - cli: 90d access, fixed
- Access + refresh token rotation security
- Cached permissions snapshot per session
- Cascade credential → sessions revocation
- POSTGRES: `sessions`
- Cache Valkey ~1ms lookup
- CSRF protection browser
- Cleanup cron daily 2 AM (>30d delete)

---

## 7. Resumen ejecutivo Bloque 4 — Dashboard + Notifications

### 7.4.1 — Dashboard v2 Expansion: Module system + global search
- 8+ modules (overview, skills, dmn, cost, audit v1 default + memory, plans, forgetting, eval, identities, integrations, settings v2 on-demand)
- ModuleActivationManager (cliente self-service)
- Permission-based filtering automatic
- Tier-aware (enterprise modules)
- Global search 5+ resources parallel
- Charts rich (Chart.js + Plotly CDN)
- Customization (theme + i18n + layout)
- Settings UI integrates TODOS R7 sub-temas
- Performance (virtualization + lazy load + cache)
- ALTER workspaces: `activated_modules`, `dashboard_settings`

### 7.4.2 — Notification System Multi-Channel
- NotificationEventCatalog 15+ events v1 (CRITICAL/IMPORTANT/INFO)
- 4 channels: email + webhook + in_app + telegram
- NotificationPreference per identity per event
- NotificationOrchestrator (central coordinator)
- DigestAggregator (cron daily 9 AM per timezone)
- DeadLetterQueue (retry + dead letter)
- Quiet hours timezone-aware
- Rate limit (10/20/50 per urgency)
- i18n templates ready
- Unsubscribe one-click (compliance)
- POSTGRES: `notifications`, `notification_preferences`, `notification_deliveries`, `in_app_notifications`

### 7.4.3 — PWA + Mobile-Responsive
- PWA Manifest (install home screen iOS 16.4+ / Android)
- Service Worker 4 cache strategies (network-first, cache-first, stale-while-revalidate, offline fallback)
- PushSubscriptionManager (VAPID keys, system-level notifications)
- PushChannel extends 7.4.2 CHANNEL_REGISTRY
- Background sync IndexedDB offline queue
- Mobile-first responsive Tailwind
- Bottom nav + FAB + gestures + pull-to-refresh
- Native APIs (camera + share + clipboard + WebAuthn)
- POSTGRES: `push_subscriptions`
- iOS limitation mitigated via Telegram fallback (R7 7.1.1)

---

## 8. Cobertura del Grafo Maestro

**Grafo Maestro layers materializados post-R7:**

| Layer | Status | Sub-tema |
|---|---|---|
| **INPUT (Usuario / API)** | ✅ **Completo** | R7 B1 (Telegram + REST + GitHub) |
| **WORKSPACE GATE** | ✅ R4 + R7 Auth | R4 4.1.3 + R7 7.3.x |
| **TÁLAMO** | ✅ R5 | R5 B1 |
| **AMÍGDALA** | ⏳ R9 Security | R9 |
| **PFC ORCHESTRATOR** | ✅ R3 + R5 + R6 | R6 B1 |
| **HIPOCAMPO + KG + GB** | ✅ R2 + R6 | R2 + R6 B2 + B3 |
| **MULTI-AGENT NETWORK** | ✅ R5 | R5 B3 |
| **DUAL-PROCESS CHECK** | ✅ R5 | R5 B2 |
| **OUTPUT GATE** | ✅ **Completo** | R7 B2 (signing + trace + encrypt) |
| **OUTPUT (Usuario / API)** | ✅ **Completo** | R7 B2 (QA Pack + Trace + Confidence + Audit) |
| **DMN + Microglía + CLS + Neuromods** | ✅ R2 + R5 + R6 | R2 + R5 B4 + R6 B3 |

**Nodos cerebrales 10/11 completos** (solo Amígdala R9 pending).

---

## 9. Pilar 1 Seguridad COMPLETO ⭐

Grafo Maestro Pilar 1 (Encriptación end-to-end + zero-trust + workspace boundaries):

| Componente | Status | Implementación |
|---|---|---|
| **Encryption at rest** | ✅ R2 B4 | LUKS + app-layer AES-GCM (R4 4.1.3 KEK) |
| **Workspace boundaries** | ✅ R2 + R7 | RLS Postgres + 3-layer skill isolation + RBAC |
| **Output Gate** | ✅ **R7 B2** | Híbrido signing + trace + encrypt |
| **Zero-trust auth** | ✅ **R7 B3** | Identity central + RBAC + sessions |
| **Audit infrastructure** | ✅ R3 B4 + R7 | Cryptographic chain + per identity |
| **Revocation real-time** | ✅ R4 4.3.1 + R7 7.3 | Cross-channel cascade |

**Pilar 1 100% v1 completo.** Solo falta Amígdala (R9 Security layer adicional).

---

## 10. Costo total v1 actualizado post-R7

| Componente | Costo USD/mes |
|---|---|
| Subtotal R1+R2+R3+R4 v1+R5+R6 100% | ~$80-105/mes |
| R7 B1 Channels (Telegram + REST + GitHub) | $0 (reused stack) |
| R7 B2 Output Gate (cryptography lib local) | $0 |
| R7 B3 Auth + RBAC + Sessions | $0 (reused R4 4.3.1) |
| R7 B4 Dashboard expansion (HTMX) | $0 (reused) |
| R7 B4 Notifications (SMTP local o SendGrid free 100/day) | $0-2 |
| R7 B4 PWA (assets local serve) | $0 |
| **TOTAL v1 FINAL post-R7** | **~$80-107/mes** |

**Verificación P2 <25%:**
- Pilot Light $3,500 → techo $875
- Consumo v1 post-R7: ~$95
- **10.9% del techo → margen 89.1%** para R8-R10

**Verificación P5 cap LLM ($50-200/mes):**
- LLM total post-R7: ~$80-100/mes (R7 no añade LLM)
- **40-50% del cap → margen $100-120 escalado workspaces**

**Recursos servidor post-R7: ~6 GB RAM (de 30 GB)**
- R7 B1 channels: ~150 MB (Telegram + GitHub clients + bots)
- R7 B2 Output Gate: ~50 MB (signing infrastructure)
- R7 B3 Auth + RBAC + Sessions: ~100 MB (Valkey cache)
- R7 B4 Notifications + PWA: ~100 MB
- Total R7 overhead: ~400 MB

**Compliance v1 post-R7:**
- OWASP LLM Top 10
- SOC2 path real (audit + retention + 9 DMN controls + 18 multi-agent + GDPR + Output Gate signing)
- Pilar 1 Seguridad COMPLETO
- Pilar 3 Autonomía Generativa ACTIVADO
- Zero-trust auth real cross-channel
- Audit defendible per request

---

## 11. Riesgos consolidados R7 + mitigaciones

| Riesgo | Capa | Mitigación |
|---|---|---|
| Telegram bot mal config (spam) | B1 | Rate limiting per user + workspace + audit |
| REST API rate limit too strict/loose | B1 | Per-endpoint customization + tuning post-data |
| GitHub App permissions over-broad | B1 | Least privilege explicit + cliente revoke |
| HMAC secret leak | B2 | Workspace-scoped + rotation supported |
| Ed25519 keys lost (strict tier) | B2 | Backup keys + recovery flow + dual-version |
| Stream events overflow cliente | B2 | Backpressure async iterator + max events |
| Identity migration data loss | B3 | SQL migration scripts + rollback tested |
| RBAC permission proliferation | B3 | Catalog 35+ fixed + system roles + audit |
| Session hijack (token leak) | B3 | HTTPS + httponly + samesite + rotation refresh |
| Push notification spam | B4 | Rate limit + digest + quiet hours + unsubscribe |
| Dashboard module decisions UX | B4 | Defaults sensatos + wizard |
| PWA iOS limitations | B4 | Telegram fallback channel + monitor iOS adoption |
| SMTP local breakage | B4 | SendGrid free tier fallback + audit failures |

---

## 12. Próximos pasos R8

R8 — Observability completa (planeado):
- Prometheus métricas expand (R3 B4 + R5 + R6 + R7 unified)
- Grafana dashboards (Brian internal)
- Audit log retention policies (long-term storage)
- Alarms multi-channel (R7 7.4.2 reused)
- Performance metrics per channel + per identity
- Pilar 2 Escalabilidad materialized
- SLO/SLA tracking
- Cost forecasting refined (R3 B4 4.4.2 expand)

R9 — Security / Compliance:
- Nodo 7 Amígdala (último nodo Grafo Maestro)
- SOC2 evidence collection
- Penetration testing
- Compliance audit reports
- GDPR full audit
- Threat modeling refinements

R10 — CI/CD / Deploy:
- GitHub Actions R4 B3 + R7 7.1.3 workflow_run integration
- Multi-env (dev/staging/prod)
- Blue-green deploy
- Foundation Meta-Orchestrator (Pilar 3 capacidades 2+3+4)

**Programación arranca post-R9 o R10 (per instrucción Brian).**

---

**R7 ✅ CERRADO 100% — Pilar 1 Seguridad COMPLETO + interfaz cross-channel multi-tenant v1.**