# Ronda 9 — Bloque 3 — Compliance Framework (SOC2 + GDPR) ⭐ CIERRA R9

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_09_B3_Compliance_Framework.md → work/Ronda_09_B3_Compliance_Framework.md (2026-07-30, ADR-029)

## Purpose

Ronda 9 — Bloque 3 — Compliance Framework (SOC2 + GDPR) ⭐ CIERRA R9


**Sub-documento de R9.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_09_Security_Compliance.md](work/Ronda_09_Security_Compliance.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED) — Cierra R9 al 100%
**Fecha cierre:** 2026-06-09

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Entregable |
|---|---|---|
| 9.3.1 SOC2 Control Mapping | C — 5 TSC + evidence binding | soc2-control-mapping.md |
| 9.3.2 GDPR Program | C — Programa completo | gdpr-program.md + dpa-template.md + ropa.md |
| 9.3.3 Evidence + Gap + Readiness | C — Collector + scorecard + monitor | compliance-readiness.md |

---

## 9.3.1 — SOC2 Control Mapping

**Decisión LOCKED:** **C — Mapping completo 5 TSC + evidence binding + control matrix + living**

### ⭐ NOTA COMERCIAL (memoria `project_soc2_sales_wedge`)
SOC2 = "certificado de calidad para software B2B". Resaltar en página/marketing como diferenciador enterprise. Pitch: empresa grande dice "no contrato tu SaaS hasta que pases SOC2"; SOC2 audita 5 áreas (Security/Availability/Processing Integrity/Confidentiality/Privacy); auditor externo revisa controles. NO inventar cert (es readiness v1) — comunicar "SOC2-ready" honestamente.

### Las 5 Trust Service Criteria
1. **Security** (Common Criteria CC1-CC9) — OBLIGATORIO — ¿proteges datos?
2. **Availability** (A) — ¿disponible cuando lo necesito?
3. **Processing Integrity** (PI) — ¿procesa correcto?
4. **Confidentiality** (C) — ¿mantienes secretos?
5. **Privacy** (P) — ¿manejas datos personales bien? (cruza GDPR 9.3.2)

### Common Criteria CC1-CC9 → controles R1-R9
| CC ref | Criterio | Controles For3s | Status |
|--------|----------|-----------------|--------|
| CC1 | Control Environment (governance) | threat model (9.2.1) + decision-log + ownership Brian | implemented |
| CC2 | Communication & Info | audit chain (8.3.1) + observability (R8) | implemented |
| CC3 | Risk Assessment | STRIDE+DREAD (9.2.1) | implemented |
| CC4 | Monitoring Activities | observability (R8 B1+B2) + pentest cadence (9.2.2) | implemented |
| CC5 | Control Activities | RBAC (R7) + Output Gate (R7) | implemented |
| CC6.1 | Logical Access | Auth (R7) + RBAC + Amígdala (R9) + sessions | implemented |
| CC6.2 | Registration/Deregister | Identity lifecycle (R7) + cascade revocation | implemented |
| CC6.3 | Access removal | R7 revocation + session expire | implemented |
| CC6.6 | Boundary protection | Amígdala (R9) + Cloudflare Tunnel + workspace isolation | implemented |
| CC6.7 | Data transmission | P4 encryption + Output Gate signing (R7) | implemented |
| CC6.8 | Malicious software prevention | Amígdala (R9) + Trivy (9.2.2) + MCP sandbox (R4) | implemented |
| CC7.1 | Vuln detection | Pentest (9.2.2) + SAST CI | planned* |
| CC7.2 | Security monitoring | Observability (R8) + Amígdala | implemented |
| CC7.3 | Incident evaluation | Incident mgmt (8.4.3) + security playbooks (9.2.3) | implemented |
| CC7.4 | Incident response | Security playbooks (9.2.3) PICERL | implemented |
| CC7.5 | Recovery | Backups (R2 B4) + playbooks | partial* |
| CC8.1 | Change management | Versioning (R4) + decision-log + threat model update | implemented |
| CC9.1 | Risk mitigation | Threat model + DREAD + Amígdala | implemented |
| CC9.2 | Vendor management | MCP SHA pin (R4) + LLM provider | implemented |
*planned/partial = ejecución post-código

### Additional categories
- **Availability**: A1.1 capacity → Pilar 2 (8.2.3) + SLO (8.4.1) · A1.2 backup/recovery → R2 B4 + retention (8.3.2) · A1.3 recovery testing → DR plan (R10, planned)
- **Confidentiality**: C1.1 → workspace isolation + KEK (R4) + RLS · C1.2 disposal → forgetting (R6) + retention (8.3.2) + GDPR pseudonym
- **Processing Integrity**: PI1.x → Output Gate (R7) + Microglia eval (R5/R6) + confidence (R6) + Amígdala input validation (R9)
- **Privacy**: P1-P8 → GDPR program (9.3.2)

### Control matrix + evidence binding
```python
class SOC2Control:
    tsc_ref, criterion, category
    for3s_controls            # ['R7:rbac', 'R9:amygdala']
    implementation_status     # implemented/partial/planned/gap
    evidence_event_types      # audit events que lo prueban
    evidence_query            # query R8 8.3.3
    owner, last_tested

# soc2_quarterly report (8.3.3) AUTO-GENERA evidencia real
# desde audit chain inmutable (8.3.1) — auditor recibe evidencia
```

### Audit events
- `soc2_control_tested`
- `soc2_evidence_collected`
- `soc2_gap_identified`

### Reusa
9.2.1 threat model (CC1/CC3/CC9) + R8 8.3.3 reports + 8.3.1 audit + TODOS controles R1-R9 + 9.2.2 pentest (CC7.1) + 9.2.3 playbooks (CC7.3/7.4)

### v2: integra Vanta/Drata (mapping prerequisito igual)

### Entregable
`for3s-inter/09-technical-architecture/soc2-control-mapping.md`

---

## 9.3.2 — GDPR Compliance Program

**Decisión LOCKED:** **C — Programa completo**

### 5 componentes

#### 1. DSAR Workflow (6 derechos Art 15-21)
```python
class DataSubjectRight(Enum):
    ACCESS = 'access'              # Art 15
    RECTIFICATION = 'rectification'# Art 16
    ERASURE = 'erasure'            # Art 17
    PORTABILITY = 'portability'    # Art 20
    RESTRICTION = 'restriction'    # Art 18
    OBJECTION = 'objection'        # Art 21

class DSARWorkflow:
    GDPR_DEADLINE_DAYS = 30  # Art 12
    # fulfill_access → R8 8.3.3 query (todo el identity)
    # fulfill_erasure → R8 8.3.2 pseudonym + R6 forgetting
    #   (respeta legal hold → restriction si aplica)
    # fulfill_portability → JSON estructurado machine-readable
```

#### 2. Consent Management (Art 6/7)
```python
class ConsentRecord:
    identity_id, purpose, legal_basis
    granted_at, withdrawn_at, policy_version
# Versionado + withdrawal → trigger erasure si aplica
```

#### 3. DPA Template (Art 28) — vendible EU
- For3s = data processor / cliente = data controller
- Subprocesadores: Anthropic (LLM) + Cloudflare (tunnel) + OpenAI (fallback)
- Security measures → ref SOC2 (9.3.1)
- Breach → ref 9.2.3 (72h)
- Data residency: LOCAL (Brian hardware) + R2
- ⚠️ Lawyer review pre-primer-deal-EU

#### 4. RoPA (Art 30 — Records of Processing Activities)
```python
class ProcessingActivity:
    activity, purpose, legal_basis
    data_categories, data_subjects, recipients
    retention_period          # link R6/R8
    security_measures         # link SOC2 9.3.1
    transfers
```

#### 5. Privacy Data Flow Mapping
PII inventory (identity/query/channel-id/usage) → ubicación + encryption + retention + erasure path. Cruza threat model 9.2.1.

### GDPR Articles → For3s (mapping Art 5-34)
| Article | For3s implementation |
|---------|---------------------|
| Art 5 minimization | R6 forgetting + R8 retention |
| Art 6/7 legal basis/consent | Consent manager (nuevo) |
| Art 15 access | DSAR access (R8 8.3.3 query) |
| Art 16 rectification | DSAR rectification (nuevo) |
| Art 17 erasure | R8 8.3.2 pseudonym + R6 forgetting |
| Art 18 restriction | DSAR restriction (nuevo) |
| Art 20 portability | DSAR portability (nuevo) |
| Art 28 processor | DPA template (nuevo) |
| Art 30 RoPA | RoPA document (nuevo) |
| Art 32 security | SOC2 mapping (9.3.1) + Pilar 1 |
| Art 33/34 breach | 9.2.3 breach notification (72h) |

### Doble propósito
Satisface SOC2 Privacy TSC (9.3.1).

### Dashboard module (R7 reused)
"Privacy/GDPR": DSARs pendientes + deadlines + consent records + RoPA viewer + self-service rights.

### Audit events
- `gdpr_dsar_received` / `fulfilled` / `deadline_warning`
- `gdpr_consent_granted` / `withdrawn`
- `gdpr_legal_hold_blocked_erasure`
- `gdpr_ropa_updated`

### Reusa
R8 8.3.2 pseudonym + 8.3.3 query + R6 forgetting/legal-hold + R7 identity/dashboard + 9.2.3 breach + 9.3.1 SOC2

### Entregables
`gdpr-program.md` + `dpa-template.md` (lawyer review) + `ropa.md` + `for3s_os/compliance/dsar_workflow.py` + `consent_manager.py`

---

## 9.3.3 — Evidence + Gap + Readiness

**Decisión LOCKED:** **C — Collector + gap analysis + readiness scorecard + continuous monitoring**

### 5 componentes

#### 1. ComplianceEvidenceCollector
```python
async def collect_for_control(self, control, period) -> ControlEvidence:
    # evidence_query (9.3.1/9.3.2) → R8 8.3.3 query → audit chain 8.3.1
    # operating_effectively = event_count > 0 (¿opera de verdad?)
    # EvidencePack tamper-proof (chain proof + integrity_hash)
```

#### 2. ComplianceGapAnalyzer
```python
# status gaps (gap/partial/planned) + no_evidence (drift detection)
# cruza threat model gaps (9.2.1) + pentest findings (9.2.2)
# priorizado (critical/high/medium)
```

#### 3. ReadinessScorecard
```python
class Verdict(Enum):
    AUDIT_READY      # >90% + 0 critical
    NEARLY_READY     # >75%
    IN_PROGRESS      # >50%
    EARLY_STAGE
# readiness_pct = implemented_with_evidence / total
# blocking_gaps explícitos
```

#### 4. ComplianceMonitor (weekly cron Arq)
Drift detection: si readiness baja >5% vs semana anterior → alert Brian + métrica.

#### 5. AuditPackGenerator (1-click)
control_mapping + evidence + gap_analysis + readiness + threat_model_summary + pentest_summary → PDF/JSON tamper-proof para cliente enterprise due diligence.

### Readiness dashboard (R8 8.2.2 + R7 module)
SOC2 + GDPR readiness gauges · gaps por prioridad · evidence freshness · drift timeline · 1-click audit pack.

### Resultado esperado v1 (honesto)
| Framework | Readiness | Verdict | Blocking |
|-----------|-----------|---------|----------|
| SOC2 | ~85-90% | NEARLY_READY | CC7.1 pentest exec (post-code), A1.3 DR testing (R10) |
| GDPR | ~88-92% | NEARLY_READY | DPA lawyer review (pre-EU deal) |

→ AUDIT_READY tras ejecución post-código.

### Audit events
- `compliance_evidence_collected` (framework, control)
- `compliance_gap_identified` (severity)
- `compliance_readiness_computed` (pct, verdict)
- `compliance_drift_detected` (warning)
- `audit_pack_generated`

### Métricas
- `compliance_readiness_pct` (framework)
- `compliance_gaps_total` (framework, severity)
- `compliance_evidence_freshness_days` (control)

### Reusa
R8 8.3.3 query + 8.3.1 audit + 8.2.2 dashboard + 9.3.1 SOC2 + 9.3.2 GDPR + 9.2.1 threat model + 9.2.2 pentest + R2 Arq + R7 dashboard

### Entregables
`compliance-readiness.md` + `for3s_os/compliance/evidence_collector.py` + `gap_analyzer.py` + `readiness_scorecard.py` + `audit_pack.py`

---

## Cobertura Compliance

| Framework | Status | Evidence |
|-----------|--------|----------|
| SOC2 (5 TSC) | NEARLY_READY ~85-90% | Control mapping + evidence binding + auto-gen reports |
| GDPR (Art 5-34) | NEARLY_READY ~88-92% | DSAR + consent + DPA + RoPA + breach |
| OWASP LLM Top 10 | 10/10 covered | Threat model 9.2.1 |

**Programa compliance audit-ready (vendible enterprise B2B). Cert real auditor externo = v2.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_09_B3_Compliance_Framework.md`).
