# Ronda 4 — Bloque 3: Tool Lifecycle

**Sub-documento detallado de R4 — Tools/MCP Layer. Bloque 3 de 4 (CIERRA R4 v1).**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-06
**Estatus:** ✅ LOCKED (3/3 sub-temas) — **CIERRA R4 v1 100%**
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

**Dependencias resueltas en R4 B1 + B2:**
- ✅ mcp SDK + Discovery + Docker multi-tenant + Secrets KEK (B1)
- ✅ 4 MCP servers operativos + ~57 tools (B2)
- ✅ Principio Arquitectónico LOCKED validado 3 veces

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 4.3.1 — Tool authorization workflows](#3-sub-tema-431--tool-authorization-workflows)
4. [Sub-tema 4.3.2 — Tool versioning + rollback](#4-sub-tema-432--tool-versioning--rollback)
5. [Sub-tema 4.3.3 — Tool testing & sandbox](#5-sub-tema-433--tool-testing--sandbox)
6. [Stack final consolidado](#6-stack-final-consolidado)
7. [Cobertura del Grafo Maestro](#7-cobertura-del-grafo-maestro)
8. [Costo total post-Bloque 3](#8-costo-total-post-bloque-3)
9. [Cierre R4 v1 — síntesis final](#9-cierre-r4-v1--síntesis-final)
10. [Implicaciones en rondas futuras](#10-implicaciones-en-rondas-futuras)
11. [Riesgos legítimos aceptados](#11-riesgos-legítimos-aceptados)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 3 — TOOL LIFECYCLE                                    ║
║   3 sub-temas LOCKED el 2026-06-06                             ║
║   ⭐ CIERRA R4 v1 100% (11/11 sub-temas)                        ║
║                                                                ║
║   4.3.1 Authorization workflows  → B) 7 capacidades coord.      ║
║   4.3.2 Versioning + rollback    → A) SemVer + SHA + ws config  ║
║   4.3.3 Testing & sandbox         → A) Framework 5 capas         ║
║                                                                  ║
║   Foundation cerrada para:                                       ║
║   • R5 Orchestration / Multi-Agent                                ║
║   • R6 Memory Stack extensions                                    ║
║   • R7 Frontend / Channel (multi-canal via PlatformAdapter ABC)  ║
║   • R8 Observability (~60 métricas R4)                            ║
║   • R9 Security/Compliance (OWASP + SOC2 path defendible)         ║
║   • R10 CI/CD/Deploy (5 capas testing + SHA pinning)               ║
║                                                                  ║
║   Costo incremental B3 R4:      ~+$2/mes (Haiku regression)       ║
║   Costo total v1 FINAL:          ~USD 64-79/mes                    ║
║   % techo Pilot Light:            6.6% (margen 93.4%)              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Disciplina operacional como diferenciador comercial.
La diferencia entre 'wrapper de Claude bonito' y
'plataforma enterprise SOC2-defendible' está en cómo
se gobiernan, versionan y testean las tools. B3 es el
bloque que cierra ese gap."
```

Las 3 decisiones convergen en patrones consistentes:

```
1. GOVERNANCE OPERACIONAL (4.3.1)
   → 7 capacidades coordinadas: policies + dry-run + roles +
     remember + revocation + break-glass + dashboard
   → Foundation enterprise B2B compliance

2. EVOLUCIÓN CONTROLADA (4.3.2)
   → SemVer human-readable + Docker SHA inmutable
   → Workspace pinning (cliente self-service)
   → Rollback rápido
   → Audit defendible

3. CALIDAD AUTOMATIZADA (4.3.3)
   → 5 capas testing coordinadas
   → Sandbox para learning + demos
   → CI/CD foundation natural
   → Eval framework B4 3.4.3 integration

4. INTEGRACIÓN PROFUNDA CON R1-R3 + R4 B1+B2
   → Reusa Postgres, Valkey, Arq, Jinja2, Telegram
   → Extiende Permission model (B2 3.2.4)
   → Extiende ErrorType taxonomy (B3 3.3.3)
   → Extiende Prometheus + audit chain

5. FOUNDATION COMERCIAL DEFINITIVA
   → Compliance B2B SOC2/ISO27001 path
   → Cliente self-service (sandbox, version pinning, policies)
   → Brian disciplina sin SRE team
```

### Por qué esta filosofía importa

**Para Pilar 1 Seguridad:** Authorization 7 capacidades + Versioning audit + Testing 100% security paths = OWASP LLM Top 10 cumplido + SOC2 defendible.

**Para Pilar 2 Escalabilidad:** Testing automatizado escala con tools count + Versioning permite multi-version concurrente sin breaking + Authorization policies se adaptan per workspace tier.

**Para Pilar 3 Autonomía:** Agente puede ejecutar tools autónomamente sabiendo que están testeadas, versionadas y autorizadas según policies declarativas del workspace.

---

## 3. Sub-tema 4.3.1 — Tool authorization workflows

### Decisión LOCKED

```
B) Workflow completo (7 capacidades coordinadas)
```

### Razón

P3 LOCKED dijo "Permission + whitelist + human-in-loop opcional". B2 implementó base. B3 4.3.1 cierra el gap operacional para producción enterprise B2B con governance defendible.

### 7 Capacidades coordinadas LOCKED

```
CAPACIDAD 1: Approval policies declarativas
   • workspace.approval_policies JSONB
   • 4 decisiones por policy:
     - auto_approve (sin pausa)
     - auto_reject (sin preguntar)
     - require_approval (human-in-loop)
     - block (reject + security_alarm)
   • Match patterns: tool_name, tool_class, args.X
   • Priority-based evaluation (highest wins)

CAPACIDAD 2: Dry-run preview cuando posible
   • Tools nativas (GitHub merges?dry_run=true)
   • Telegram inline keyboard CON preview
   • Audit "no_dry_run_available" si no soporta

CAPACIDAD 3: Role-based approver
   • 3 roles: owner / admin / member
   • Approver_role per policy:
     - any_member, requesting_user, admin, owner
   • Notify Telegram al rol superior si no satisfecho

CAPACIDAD 4: Remember decision (con safety limits)
   • Sugerencia post 3 approvals mismo pattern
   • SAFETY LIMITS LOCKED:
     - MAX TTL: 30 días
     - MAX policies remember: 50 per workspace
     - NO remember para destructive
     - Auto-revoke si role cambia
     - Audit cada remember

CAPACIDAD 5: Revocation window
   • 5 segundos post-approval
   • Telegram muestra botón REVERT durante window
   • Audit revocation events

CAPACIDAD 6: Break-glass urgent token
   • UUID + workspace_id + reason
   • TTL 1 hora, single-use
   • Audit SECURITY_ALARM fuerte
   • Brian Telegram crítico al generar
   • Compliance-defendible (audit log review)

CAPACIDAD 7: Dashboard + multi-channel notifications
   • Dashboard /workspaces/{id}/approvals
   • Channels: Telegram primary, email fallback, dashboard always
   • Escalation: Telegram → email después 120s sin respuesta
```

### Defaults LOCKED workspace onboarding

```
1. auto_approve_readonly (priority 100)
   • Tools class 'readonly' → auto

2. require_owner_for_destructive (priority 150)
   • Tools class 'destructive' → require owner approval

3. default_require_approval (priority 1)
   • Resto → require any_member approval
```

### Schema SQL

```sql
ALTER TABLE shared.workspaces ADD COLUMN
    approval_policies JSONB NOT NULL DEFAULT '[]';

ALTER TABLE shared.workspace_telegram_users ADD COLUMN
    role TEXT NOT NULL DEFAULT 'member'
    CHECK (role IN ('owner', 'admin', 'member'));

CREATE TABLE shared.approval_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES shared.workspaces(id),
    tool_call_id UUID NOT NULL,
    tool_name TEXT NOT NULL,
    args JSONB,
    dry_run_preview TEXT,
    policy_matched TEXT,
    decision TEXT NOT NULL,
    decided_by_user_id UUID,
    decided_by_role TEXT,
    decided_at TIMESTAMPTZ,
    decided_via TEXT,
    remember_decision_until TIMESTAMPTZ,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    executed_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    audit_event_id UUID NOT NULL REFERENCES audit_events(id)
);

CREATE TABLE shared.remember_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES shared.workspaces(id),
    pattern JSONB NOT NULL,
    created_by_user_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    uses_count INTEGER DEFAULT 0,
    revoked_at TIMESTAMPTZ,
    UNIQUE (workspace_id, pattern)
);

CREATE TABLE shared.break_glass_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token TEXT NOT NULL UNIQUE,
    workspace_id UUID NOT NULL,
    created_by_user_id UUID NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    used_for_tool TEXT,
    audit_event_id UUID NOT NULL REFERENCES audit_events(id)
);
```

### Reglas duras LOCKED 4.3.1

```
✅ 7 capacidades coordinadas
✅ Approval timeout: 300s (5 min, P3 LOCKED reused)
✅ Revocation window: 5 segundos post-approval
✅ Escalation: Telegram → email después 120s
✅ Break-glass TTL: 3600s (1 hora), single-use
✅ Remember max TTL: 30 días
✅ Remember max policies: 50 per workspace
✅ NO remember para destructive (siempre fresh)
✅ 4 tablas SQL nuevas
✅ Defaults secure-by-default (3 policies LOCKED onboarding)
✅ Audit obligatorio policy_matched + decision + channel
✅ 7 métricas Prometheus nuevas
✅ Foundation R9 SOC2 path
```

---

## 4. Sub-tema 4.3.2 — Tool versioning + rollback

### Decisión LOCKED

```
A) SemVer + Docker SHA + workspace-level config
```

### Razón

Tools evolucionan. APIs cambian. Bugs aparecen. Versioning sistemático con audit inmutable es prerequisite producción enterprise.

### 3 Pilares coordinados

```
PILAR 1: SemVer human-readable
   • MAJOR.MINOR.PATCH (breaking/feature/fix)
   • Tags Docker: 1.0.0, 1.0, 1, stable, beta, canary

PILAR 2: Docker SHA pinned producción
   • image: for3s/mcp-X@sha256:abc...
   • Inmutabilidad real
   • Audit compliance defendible

PILAR 3: Workspace-level config
   • workspace.mcp_server_versions JSONB
   • Per-cliente pinning + release channels
   • Cliente self-service
```

### Release channels LOCKED

```
• stable  → producción default, conservative
• beta    → opt-in, ~1 semana testing
• canary  → opt-in, daily releases
• <exact> → SemVer específico
```

### Arquitectura multi-version

```
Containers per version corren simultáneos:
   mcp-github-0.6.2
   mcp-github-0.7.0
   mcp-github-stable
   mcp-github-beta

VersionRouter routes workspace → endpoint correcto
Cleanup cron mensual: versions >90 días sin uso removidas
```

### Rollback strategy

```
v1: MANUAL via Brian CLI script (scripts/rollback_mcp.sh)
v2: Automatic si error rate >X% trigger
v3: Blue-green deployment (R10)
```

### Deprecation process

```
FASE 1: SOFT (30 días) — logs warning + dashboard banner
FASE 2: HARD (15 días) — email cliente + Telegram Brian
FASE 3: REMOVAL — TOOL_DEPRECATED ErrorType (R3 B3 3.3.3)
```

### Schema SQL

```sql
ALTER TABLE shared.workspaces ADD COLUMN
    mcp_server_versions JSONB NOT NULL DEFAULT '{
        "github":     "stable",
        "filesystem": "stable",
        "http":       "stable",
        "telegram":   "stable"
    }'::JSONB;

ALTER TABLE shared.workspaces ADD COLUMN
    mcp_version_pinned_at TIMESTAMPTZ;

CREATE TABLE shared.mcp_server_releases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    server_name TEXT NOT NULL,
    semver TEXT NOT NULL,
    docker_sha TEXT NOT NULL,
    release_channel TEXT NOT NULL,
    released_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deprecated_at TIMESTAMPTZ,
    removed_at TIMESTAMPTZ,
    release_notes TEXT,
    breaking_changes JSONB,
    UNIQUE (server_name, semver)
);

CREATE TABLE shared.tool_call_versions (
    audit_event_id UUID NOT NULL REFERENCES audit_events(id),
    workspace_id UUID NOT NULL,
    server_name TEXT NOT NULL,
    semver TEXT NOT NULL,
    docker_sha TEXT NOT NULL,
    called_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Reglas duras LOCKED 4.3.2

```
✅ SemVer (MAJOR.MINOR.PATCH)
✅ Docker SHA pinned producción inmutable
✅ 4 release channels: stable / beta / canary / exact
✅ Workspace-level pinning JSONB
✅ Multi-version containers concurrentes
✅ Cleanup cron: versions >90d sin uso removidas
✅ Rollback manual v1, automatic v2, blue-green v3
✅ Deprecation: 30d soft + 15d hard + removal
✅ TOOL_DEPRECATED ErrorType integrado R3 B3
✅ Audit inmutable SHA + SemVer per call
✅ 5 métricas Prometheus nuevas
✅ Foundation R10 CI/CD
```

---

## 5. Sub-tema 4.3.3 — Tool testing & sandbox

### Decisión LOCKED

```
A) Framework completo (5 capas testing coordinadas)
```

### Razón

Custom tools (filesystem, HTTP, telegram) tienen security crítica. Sin testing automated, SSRF bypass, path traversal y signature bypass no son detectados. Foundation R10 CI/CD natural extension.

### 5 Capas testing coordinadas

```
CAPA 1: UNIT TESTS (per tool isolated)
   • Framework: pytest async + pytest-cov
   • Coverage: 85% custom, 70% wrappers, 100% security paths
   • Mocks Python (unittest.mock + Pydantic)

CAPA 2: INTEGRATION TESTS (tool ↔ stack)
   • Tools usan stack For3s real (SecretsManager, Permission, Audit)
   • VCR.py recordings deterministic
   • Re-record cuando schema cambia

CAPA 3: E2E TESTS (tool ↔ agent ↔ workflow)
   • Workflow completo: user message → agent → tool → response
   • Sandbox shadow services real
   • LLM calls Haiku barato (cap budget E2E)

CAPA 4: SANDBOX ENVIRONMENTS
   • Brian test pre-deploy
   • CI ejecuta tests
   • Cliente probar tools antes activar
   • Demos sin afectar producción

CAPA 5: GOLDEN DATASET INTEGRATION (B4 3.4.3 obligatoria)
   • Tools nuevas DEBEN agregar samples golden_datasets
   • CI ejecuta eval framework antes deploy
   • Regression check semanal Arq cron domingo 3 AM
```

### Shadow services LOCKED v1

```
GitHub:     org "for3s-sandbox" + test_repos + sandbox bot token
Telegram:   bot "@For3sSandboxBot"
Filesystem: /var/lib/for3s/sandbox/workspaces
HTTP:       httpbin.org real + VCR fixtures
```

### Workspace sandbox tier LOCKED

```
LIMITS sandbox tier:
   • Max 1 sandbox per cliente
   • Cost cap: $5/mes (HARD)
   • Token bucket: 5 RPM / 5K TPM
   • Filesystem: 1 GB quota
   • Tools accessible: all (con sandbox endpoints)
   • Auto-cleanup: workspace data >30 días sin uso

UX FLOW:
   1. Cliente crea cuenta For3s
   2. Auto-provision workspace_sandbox (incluido free)
   3. Cliente prueba tools sin afectar producción
   4. Si cliente quiere producción → upgrade tier
```

### CI/CD pipeline foundation (R10)

```yaml
GitHub Actions workflow:
   - unit_tests (coverage 85% mínimo)
   - integration_tests (VCR fixtures)
   - e2e_smoke (sandbox)
   - eval_golden (B4 3.4.3 integration blocking)
   - security_scan (Trivy + bandit)
   - regression_full (Arq cron domingo 3 AM)
```

### Schema SQL

```sql
ALTER TABLE shared.workspaces ADD COLUMN
    is_sandbox BOOLEAN NOT NULL DEFAULT false;

CREATE TABLE shared.tool_test_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_type TEXT NOT NULL,
    tool_name TEXT,
    server_name TEXT,
    server_semver TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    total_tests INTEGER,
    passed INTEGER,
    failed INTEGER,
    skipped INTEGER,
    coverage_pct NUMERIC(5,2),
    triggered_by TEXT,
    audit_event_id UUID,
    metadata JSONB
);
```

### Reglas duras LOCKED 4.3.3

```
✅ 5 capas testing coordinadas
✅ Framework pytest async + pytest-cov
✅ Coverage: 85% custom, 70% wrappers, 100% security
✅ Mocks 3 layers (Python / VCR / sandbox real)
✅ Shadow services LOCKED (GitHub + Telegram + FS + HTTP)
✅ Workspace sandbox tier (opt-in, free, $5 hard cap, max 1/cliente)
✅ CI/CD GitHub Actions foundation R10
✅ Regression Arq cron domingo 3 AM + alert >5%
✅ Eval B4 3.4.3 integration obligatoria
✅ Audit tool_test_runs per ejecución
✅ 6 métricas Prometheus nuevas
✅ Security testing 100% paths críticos
```

---

## 6. Stack final consolidado Bloque 3

```
COMPONENTE                              DECISIÓN                          COSTO
─────────────────────────────────────────────────────────────────────────────
Authorization workflows                 B) 7 capacidades coordinadas      $0
   • policies declarativas JSONB
   • dry-run preview cuando posible
   • role-based approver (owner/admin/member)
   • remember decision (max 30d, 50/workspace, NO destructive)
   • revocation window 5s
   • break-glass token 1h single-use
   • dashboard + multi-channel (Telegram → email 120s)
   • 4 tablas SQL nuevas

Versioning + rollback                   A) SemVer + Docker SHA + workspace$0
   • SemVer (MAJOR.MINOR.PATCH)
   • Docker SHA pinned producción
   • 4 release channels: stable/beta/canary/exact
   • Workspace-level config JSONB
   • Multi-version containers concurrentes
   • Cleanup cron 90d sin uso
   • Rollback manual v1, automatic v2
   • Deprecation 3 fases: 30d soft + 15d hard + removal
   • 3 tablas SQL nuevas

Testing & sandbox                       A) Framework 5 capas              ~+$2/mes
   • Unit + Integration + E2E + Sandbox + Eval
   • pytest async + pytest-cov
   • Coverage 85% custom, 70% wrappers, 100% security
   • Mocks 3 layers
   • Shadow services (GitHub/Telegram/FS/HTTP)
   • Workspace sandbox tier (free, limits)
   • CI/CD GitHub Actions foundation R10
   • Regression cron domingo 3 AM
   • 2 tablas SQL nuevas
─────────────────────────────────────────────────────────────────────────────
TOTAL incremental B3 R4                                                   ~+$2/mes
TOTAL v1 FINAL (R1+R2+R3 100%+R4 v1 100%)                                ~$64-79/mes
```

### Tablas SQL Bloque 3 (9 nuevas)

```
Authorization (4):
   • workspace.approval_policies JSONB
   • shared.approval_decisions
   • shared.remember_decisions
   • shared.break_glass_tokens

Versioning (3):
   • workspace.mcp_server_versions JSONB
   • shared.mcp_server_releases
   • shared.tool_call_versions

Testing (2):
   • workspace.is_sandbox BOOLEAN
   • shared.tool_test_runs
```

### Métricas Prometheus Bloque 3 (18 nuevas)

```
Authorization (7):
   tool_authorization_requests_total
   tool_approval_latency_seconds
   tool_approval_timeout_total
   tool_approval_revoked_total
   tool_remember_hits_total
   tool_break_glass_used_total
   tool_policy_blocked_total

Versioning (5):
   tool_version_calls_total
   tool_version_usage_workspaces
   tool_deprecated_usage_total
   tool_rollback_events_total
   tool_version_channel_distribution

Testing (6):
   test_runs_total
   test_duration_seconds
   test_coverage_pct
   test_failures_total
   regression_degradation_pct
   sandbox_usage_total
```

---

## 7. Cobertura del Grafo Maestro

### Nodos servidos por Bloque 3 R4

```
NODO                                 STATUS POST-B3 R4
──────────────────────────────────────────────────────────
Nodo 4 Cuerpo Calloso (Tool Bus)    ✅✅ PLENO (R4 v1 completo)
Nodo 2 Cerebelo (Skills auto v3)    🟡 foundation (testing framework lista)
Nodo 3 PFC (Orchestrator)            ✅ orquesta + governance
```

### Pilares — Cobertura por B3 R4

```
Pilar 1 — Seguridad E2E
   ✅ Authorization 7 capacidades (4.3.1)
   ✅ Break-glass audit fuerte SOC2-defendible
   ✅ Versioning audit inmutable SHA per call
   ✅ Testing security 100% paths críticos
   ✅ Sandbox aislamiento learning

Pilar 2 — Escalabilidad por nodo
   ✅ Policies declarativas escalan con workspaces
   ✅ Multi-version containers concurrentes
   ✅ Testing framework escala con tools count
   ✅ Cleanup automatizado

Pilar 3 — Autonomía Generativa
   ✅ Agente decide tools con governance clara
   ✅ Versioning permite agentes diferentes per workspace
   ✅ Testing automated permite Brian iterar rápido
   ✅ Foundation Skills auto v3+ (Nodo 2 Cerebelo)
```

---

## 8. Costo total post-Bloque 3

```
SUBTOTAL R1+R2+R3 100% + R4 B1+B2:                  ~$62-77/mes

R4 BLOQUE 3 INCREMENTAL:
   Authorization (todo en código):                   $0
   Versioning (Docker SHA + workspace config):       $0
   Testing framework (pytest + GitHub Actions):      $0
   Haiku regression weekly cron:                     ~+$2/mes
─────────────────────────────────────────────────────────────
TOTAL v1 FINAL (R1+R2+R3 100%+R4 v1 100%):          ~$64-79/mes

Verificación P2 <25%:
   Pilot Light $3,500 → techo $875
   Consumo v1 (3 sem): ~$58
   → 6.6% del techo
   → MARGEN 93.4% para R5-R10
```

---

## 9. Cierre R4 v1 — síntesis final

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅✅✅ R4 v1 — TOOLS/MCP LAYER 100% CERRADO ✅✅✅            ║
║                                                                ║
║   11/11 sub-temas LOCKED (B1+B2+B3 operativos)                  ║
║   3/3 bloques LOCKED                                            ║
║   3 decisiones logged (D-016, D-017, D-018)                      ║
║   1 día de debate (2026-06-06)                                   ║
║                                                                  ║
║   B4 ⏳ DIFERIDO v2 (Multi-Domain Expansion):                    ║
║   • Slack, Notion, Google Drive, Calendar                        ║
║   • Health, Finance, Legal MCP servers per dominio               ║
║   • Foundation lista (Principio Arquitectónico + Hermes)         ║
║                                                                  ║
║   ─────────────────────────────────────────────────────       ║
║                                                                  ║
║   FOUNDATION ENTREGADA:                                          ║
║                                                                  ║
║   • R5 Orchestration       — 57 tools + AgentDelegation          ║
║   • R6 Memory extensions    — filesystem indexable + telegram    ║
║   • R7 Frontend / Channel   — PlatformAdapter ABC multi-canal    ║
║   • R8 Observability        — ~60 métricas R4 + audit chain      ║
║   • R9 Security/Compliance  — OWASP + SOC2 path defendible       ║
║   • R10 CI/CD / Deploy      — Testing 5 capas + SHA pinning      ║
║                                                                  ║
║   ─────────────────────────────────────────────────────       ║
║                                                                  ║
║   MÉTRICAS FINALES R4 v1:                                        ║
║                                                                  ║
║   • Costo total v1: ~$64-79/mes                                   ║
║   • % techo P2 Pilot Light: 6.6% (margen 93.4%)                  ║
║   • % cap P5 LLM: 32-37% (margen $127-137)                       ║
║   • 57 tools concretas disponibles                                 ║
║   • Recursos R4: ~3.5 GB RAM (de 30 GB)                          ║
║   • Capacidad: ~40 Pilot Light o ~10 Pilot Pro                    ║
║   • Compliance: OWASP LLM Top 10 + SOC2 path                      ║
║                                                                  ║
║   ─────────────────────────────────────────────────────       ║
║                                                                  ║
║   PRÓXIMO PASO: Iniciar R5 — Orchestration / Multi-Agent         ║
║   (después de cierre formal FASE 2 público-formal)                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 10. Implicaciones en rondas futuras

### Para R5 — Orchestration / Multi-Agent

```
✅ 57 tools registradas + governance + versioning + testing
✅ AgentDelegationTool foundation (B2 3.2.4)
✅ Container workspace per cliente
✅ Telegram canal bidireccional
✅ Approval flow para sub-agent actions
✅ Tool routing per workspace (foundation Tálamo)
✅ Versioning permite agentes diferentes per workspace
```

### Para R6 — Memory Stack extensions

```
✅ Filesystem indexable como memoria (Filesystem MCP)
✅ Telegram conversations → memoria episódica
✅ Tools metrics → memoria semántica
✅ Versioning audit → memoria histórica
✅ Authorization decisions → contexto agente
```

### Para R7 — Frontend / Channel

```
✅✅ PlatformAdapter ABC (Hermes patterns)
✅ Telegram primer canal validado
✅ Approval dashboard cliente
✅ Sandbox dashboard cliente
✅ Versioning dashboard (cliente self-service)
✅ Multi-canal v2 sin reescribir core (Discord, Slack, WhatsApp)
```

### Para R8 — Observability completa

```
✅ ~60 métricas Prometheus nuevas R4 (todos sub-temas)
✅ Audit chain extendido per MCP + auth + version + test
✅ Foundation Grafana dashboards
✅ Alerting rules específicas (SSRF, auth_failure, regression)
```

### Para R9 — Security / Compliance

```
✅✅ OWASP LLM Top 10 compliance (HTTP SSRF + path + signature)
✅✅ Authorization governance defendible SOC2
✅ Audit inmutable versioning compliance
✅ Penetration testing foundation (sandbox + property-based defer v2)
✅ Secrets KEK hierarchy defense in depth
✅ Tools eval safety + golden datasets
```

### Para R10 — CI/CD / Deploy

```
✅✅ Testing framework completo (5 capas) READY
✅✅ GitHub Actions foundation READY
✅✅ Docker SHA pinned (immutable deploys) READY
✅ Versioning + rollback strategy READY
✅ Sandbox environments para pre-prod READY
✅ Provisioning scripts foundation READY
✅ Compliance audit defendible READY
```

---

## 11. Riesgos legítimos aceptados

12 riesgos B3 R4 identificados consolidados.

### Authorization (4)

```
R1. Policy mal escrita = security hole
    IMPACTO: ALTO | MITIGACIÓN: defaults LOCKED secure-by-default + validation Pydantic + tests + audit changes

R2. Remember decision abused
    IMPACTO: MEDIO | MITIGACIÓN: max 30d TTL + NO destructive + max 50/workspace + audit alerts

R3. Break-glass token leak
    IMPACTO: CRÍTICO | MITIGACIÓN: single-use + TTL 1h + SECURITY_ALARM + Brian Telegram

R4. Revocation race condition
    IMPACTO: MEDIO | MITIGACIÓN: 5s window + async tool execution + audit too_late events
```

### Versioning (4)

```
R5. Multi-version containers consumen RAM
    IMPACTO: MEDIO | MITIGACIÓN: cleanup cron 90d + resource limits 200MB + Prometheus monitor

R6. Breaking change MAJOR no documentado
    IMPACTO: ALTO | MITIGACIÓN: SemVer disciplina + breaking_changes JSONB + email proactive

R7. Rollback no funciona (target corrupted)
    IMPACTO: ALTO | MITIGACIÓN: verify pull + test staging + multi-version siempre 2-3

R8. CI/CD missing v1 (Brian manual)
    IMPACTO: BAJO | MITIGACIÓN: CLI scripts robustos + manual checklists + R10 automatiza
```

### Testing (4)

```
R9. Tests flaky CI
    IMPACTO: ALTO | MITIGACIÓN: aislamiento fixtures + retry 3x conocidos + quarantine investigate

R10. Mock fixtures desactualizados
     IMPACTO: MEDIO | MITIGACIÓN: re-record mensual + schema validation + audit timestamp

R11. Cliente confunde sandbox vs producción
     IMPACTO: MEDIO | MITIGACIÓN: banner SANDBOX + email warning promote + bot username diferente

R12. Coverage drops cuando agregan features
     IMPACTO: BAJO | MITIGACIÓN: fail-under 85% CI + code review obligatorio + Brian disciplina
```