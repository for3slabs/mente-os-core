# Ronda 10 — Bloque 1 — CI/CD Pipeline

**Sub-documento de R10.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_10_CICD_Deploy.md](Ronda_10_CICD_Deploy.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED)
**Fecha cierre:** 2026-06-09

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Entregable |
|---|---|---|
| 10.1.1 CI Pipeline | C — Completo + security + Pilar 3 + compliance | .github/workflows/ci.yml |
| 10.1.2 Build + Staging | C — Build versionado + staging + smoke + dry-run | staging.yml + scripts/deploy/staging/ |
| 10.1.3 Prod Deploy + Rollback | C — Graceful + health gate + rollback + migration safety | deploy-prod.yml + scripts/deploy/prod/ |

---

## 10.1.1 — CI Pipeline

**Decisión LOCKED:** **C — Completo + security gates + Pilar 3 reforzado + compliance gate**

### 7 stages fail-fast (GitHub Actions, barato → caro)

| Stage | Tiempo | Contenido |
|-------|--------|-----------|
| 1. Fast checks | ~30s | ruff (lint+format) + gitleaks (secret scan) + mypy |
| 2. Unit tests | ~2-3min | pytest unit (R4 capa 1) + coverage gate >80% |
| 3. Security SAST+dep | ~2min (∥ stage 2) | Bandit + Semgrep + Trivy (bloquea severity ≥ HIGH) |
| 4. Integration | ~5min | Alembic + pytest integration (Postgres + Valkey efímeros) |
| 5. E2E+Eval+AISec | ~10min | pytest E2E + eval framework (R3 B4 + R6) + memory regression (R6 B4, 7 canaries) + **custom attack suite (R9 — valida Amígdala)** + garak + promptfoo |
| 6. PILAR 3 GATE | conditional | si `[skill-gen]`: DMN NO-GO + sandbox shadow + eval threshold + **HUMAN APPROVAL Brian** |
| 7. Compliance gate | ~1min | readiness check (R9 9.3.3) + threat model check (R9 9.2.1) |

### Pilar 3 Gate (CRÍTICO For3s)
El código auto-generado (skills, Pilar 3) NUNCA llega a prod sin:
- DMN NO-GO check (R6 GO/NO-GO)
- Sandbox shadow test (R4 capa 4)
- Eval threshold más alto que código humano (≥0.9)
- **Human approval de Brian** (environment protection rule — jamás auto-merge)

### Fail-fast + paralelo + cache
- Stage 1 falla → no corre el resto
- unit ∥ security-sast · cache deps (uv)
- ~15-20min full · ~3min si falla temprano

### Audit events
`ci_pipeline_run` · `ci_security_finding` · `ci_pilar3_gate_triggered` · `ci_compliance_gate_result` · `ci_secret_detected` (critical)

### Métricas
`ci_runs_total` (status) · `ci_duration_seconds` (stage) · `ci_security_findings_total` (severity, tool) · `ci_pilar3_gates_total` (result)

### Reusa
R4 testing 5 capas + GitHub Actions foundation · R9 security tools (Bandit/Semgrep/Trivy/garak/promptfoo/attack suite) + 9.3.3 readiness + 9.2.1 threat model · R6 DMN NO-GO + eval + memory regression · R8 audit + métricas

---

## 10.1.2 — Build + Staging Deploy

**Decisión LOCKED:** **C — Build reproducible versionado + staging idéntico + smoke + migration dry-run**

### Build (R4 SemVer + Docker SHA)
- App Python: `uv build` + `uv.lock` (reproducible)
- MCP servers: Docker images SHA-pinned (R4)
- Observability: imágenes oficiales pinned
- `BuildArtifact` tamper-proof (integrity_hash + ci_run_id link a 10.1.1) → registry local + R2

### Staging idéntico a prod (runtime híbrido P1=B)
- systemd staging + Postgres/Valkey staging + Docker staging
- Config `staging.env` (KEK staging aislado, scale reducida)
- Data: copia anonimizada de prod (8.3.2 pseudonym) o sintética

### Migration dry-run (crítico)
```python
class MigrationValidator:
    async def dry_run(self, artifact):
        # 1. Restaura snapshot anonimizado prod en staging (8.3.2)
        # 2. Aplica migraciones Alembic
        # 3. Verifica integridad + rollback funciona
        # 4. Mide duración (downtime prod estimate)
        # → falla → BLOQUEA promoción a prod
```

### Smoke tests (10 checks)
health · db_connectivity · amygdala_active · thalamus_routing · llm_gateway_reachable · prometheus_scraping · audit_chain_writing · e2e_simple_query · amygdala_blocks_injection · auth_required

### Promotion gate
migration dry-run OK + smoke OK → "staging-validated" → 10.1.3

### Release channels (R4)
dev / beta / stable / locked (workspace pinning enterprise)

### Audit events
`build_artifact_created` · `staging_deploy_started` · `migration_dry_run_result` · `smoke_tests_result` · `staging_deploy_validated`

### Reusa
R4 versioning + 10.1.1 CI + R8 observability (staging stack + smoke metrics) + 8.3.2 pseudonymization + 10.3.1 backup snapshot

---

## 10.1.3 — Prod Deploy + Rollback

**Decisión LOCKED:** **C — Graceful + health gate + rollback automático + migration safety**

### Flujo
```
artifact validated (10.1.2) →
  PRE-FLIGHT (10.3.3 checklist + snapshot 10.3.1) →
  MIGRATION (expand/contract safety) →
  ROLLING DEPLOY (drain + restart workers uno a uno + graceful app) →
  HEALTH GATE (smoke + SLO observación 5min) →
    ✅ healthy → production + Grafana annotation + notify Brian
    ❌ unhealthy → AUTO-ROLLBACK + incident (8.4.3) + alert
```

### Migration safety (expand/contract)
- EXPAND (deploy N): añade columna nueva, compatible hacia atrás
- CONTRACT (deploy N+1, días después): elimina vieja cuando nadie usa
- → rollback sin perder data

### Health gate
```python
class PostDeployHealthGate:
    OBSERVATION_WINDOW_MINUTES = 5
    # smoke tests (10.1.2) en prod + observa SLO (R8 8.4.1) 5min
    # error_rate > 0.05 o latency_p95 > target*1.5 → rollback
```

### Auto-rollback
re-deploy artifact anterior (validado, instantáneo) + data compatible (expand/contract) + incident SEV2 (8.4.3) + alert Brian

### Zero-downtime best-effort v1
- Workers rolling (siempre activos) + app graceful reload (~5s blip, SLO permite)
- True zero-downtime (load balancer) → v2 multi-instancia

### P2=B (auto código humano)
Deploy prod auto tras gates. Pilar 3 (auto-código) ya gated en 10.1.1 (human approval). systemd graceful (ExecReload HUP).

### Audit events
`prod_deploy_started` · `prod_migration_applied` · `prod_health_gate_result` · `prod_deploy_succeeded` · `prod_rollback_executed`

### Métricas
`prod_deploys_total` (status) · `prod_deploy_duration_seconds` · `prod_rollbacks_total` (cause) · `deploy_downtime_seconds`

### Reusa
10.1.2 artifact + R8 8.4.1 SLO (health gate) + 8.4.3 incidents (rollback) + 8.2.2 Grafana annotations + R7 7.4.2 notifications + 10.3.1 backup + 10.3.3 pre-flight + P1=B systemd/Docker