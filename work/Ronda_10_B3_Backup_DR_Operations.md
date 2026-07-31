# Ronda 10 — Bloque 3 — Backup/Recovery/DR + Operations ⭐ CIERRA R10 + 10 RONDAS

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_10_B3_Backup_DR_Operations.md → work/Ronda_10_B3_Backup_DR_Operations.md (2026-07-30, ADR-029)

## Purpose

Ronda 10 — Bloque 3 — Backup/Recovery/DR + Operations ⭐ CIERRA R10 + 10 RONDAS


**Sub-documento de R10.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_10_CICD_Deploy.md](work/Ronda_10_CICD_Deploy.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED) — Cierra R10 al 100% + las 10 rondas técnicas
**Fecha cierre:** 2026-06-09

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Entregable |
|---|---|---|
| 10.3.1 Backup Multi-Capa | C — 3-2-1 + WAL PITR + chain + GDPR + R2 | scripts/backup/ + systemd timers |
| 10.3.2 DR Testing | C — Programado + RTO/RPO + runbooks | scripts/dr/ + dr-runbooks/ ⭐ cierra SOC2 A1.3 |
| 10.3.3 Pre-Flight + Ops | C — Pre-flight + ops runbooks + índice | scripts/ops/preflight.py + runbook-index.md + ONBOARDING.md |

---

## 10.3.1 — Backup Multi-Capa

**Decisión LOCKED:** **C — Backup 3-2-1 + WAL archiving (PITR) + chain-preserving + GDPR-aware + R2 offsite**

### 3 capas (3-2-1)
| Capa | Storage | Contenido |
|------|---------|-----------|
| 1. Postgres | base backup semanal + WAL continuo | PITR (RPO minutos), reusa WAL de R8 8.3.1 |
| 2. Disco externo local (D-009 2TB) | base + WAL + filesystem | restore rápido sin internet |
| 3. R2 offsite | base + WAL + secrets cifrados | sobrevive incendio/robo/ransomware |

### Inventario respaldado
Postgres base (semanal) + WAL (continuo) + Valkey sessions (diario) + secrets cifrados (on-change) + filesystem skills/configs (diario) + audit cold (ya R2 8.3.2)

### Chain-preserving
audit_events con chain SHA-256 intacta en backup → post-restore ChainVerificationJob (8.3.1) valida → audit forensic-valid

### GDPR-aware
cifrado Workspace KEK + retención documentada (RoPA R9 9.3.2) + erasure window (dato expira)

### Anti-ransomware
R2 object versioning + write-only creds (no delete) + disco externo desconectable (air-gap parcial)

### Retention
WAL 7d · base 4 semanales + 3 mensuales · R2 alineado compliance

### Scheduling (systemd timers)
`for3s-backup-base.timer` (semanal) · WAL continuo (archive_command) · `for3s-backup-daily.timer` · `for3s-backup-r2-sync.timer`

### Verification
checksum + manifest + chain verify post-backup (10.3.2 hace el restore test real)

### Audit events
`backup_base_completed` · `backup_wal_archived` · `backup_r2_synced` · `backup_verification_result` · `backup_chain_integrity_verified`

### Métricas
`backup_last_success_timestamp` (type, alerta si stale) · `backup_size_bytes` (tier) · `backup_wal_lag_seconds` (RPO) · `backup_r2_sync_duration_seconds`

### Reusa
D-009 (disco ext + R2) + R8 8.3.1 WAL/chain + 8.3.2 R2 + R4 KEK + R9 9.3.2 GDPR + 10.2.1 systemd · alimenta 10.1.2 snapshot anonimizado
`~$2-5/mo`

---

## 10.3.2 — DR Testing + RTO/RPO ⭐ CIERRA SOC2 A1.3

**Decisión LOCKED:** **C — DR testing programado + RTO/RPO targets por tier + recovery runbook por escenario**

### RTO/RPO targets por tier (SLO R8 8.4.1)
| Tier | RTO | RPO |
|------|-----|-----|
| pilot_light | <24h | <24h |
| standard | <4h | <1h (WAL PITR) |
| enterprise | <1h | <15min |

v1 realista (1 máquina): RTO ~2-4h · RPO ~15min (archive_timeout 5min). v2 (réplica standby): RTO minutos (roadmap).

### 5 DR scenarios
`db_corruption` (PITR) · `disk_failure` (disco ext) · `ransomware` (R2 versioned) · `full_disaster` (R2 en HW nuevo) · `partial` (workspace selectivo)

### DR Test Runner
```python
class DRTestRunner:
    async def run_dr_test(self, scenario):
        # 1. Provisiona entorno DR aislado (staging/sandbox)
        # 2. Simula escenario + restaura de backups (10.3.1)
        # 3. Verifica: db_restored + chain_intact (8.3.1) +
        #    data_complete + smoke (10.1.2)
        # 4. Mide RTO/RPO real
        # 5. Compara vs targets → reporta
        # 6. Audit + compliance evidence (SOC2 A1.3, R9 9.3.3)
```

### Cadencia
- Semanal auto: restore smoke (DB_CORRUPTION PITR) → aislado
- Trimestral manual: full DR drill (FULL_DISASTER)
- Semestral: ransomware drill
- Anual: surprise drill (Brian sin avisar)

### Recovery runbooks PICERL (extiende R9 9.2.3)
- DR-1 DB Corruption (RTO ~1-2h)
- DR-2 Full Disaster (RTO ~4-8h, KEK break-glass 10.2.3, status page R8 8.4.3)
- DR-3 Ransomware (R2 versioned + ForensicsKit R9 9.2.3)
- DR-4 Partial (workspace selectivo, RTO ~30min)

### ⭐ Cierra SOC2 A1.3
recovery testing: planned → **IMPLEMENTED** → readiness SOC2 ~85-90% → **~90-95%** · RTO/RPO defendibles enterprise · audit pack (9.3.3) incluye DR results

### Desastre real = incident SEV1 (8.4.3) + runbook + status page + postmortem

### Audit events
`dr_test_started/completed/failed` · `recovery_runbook_executed` · `rto_target_missed` · `rpo_target_missed`

### Métricas
`dr_test_rto_seconds` (scenario) · `dr_test_rpo_seconds` (scenario) · `dr_tests_total` (scenario, passed) · `dr_target_compliance` (tier)

### Reusa
10.3.1 backups + R8 8.3.1 chain + 8.4.1 SLO/tiers + 8.4.3 incidents/status + R9 9.2.3 PICERL + 9.3.3 evidence + 9.3.1 SOC2 + 10.2.3 KEK break-glass + 10.1.2 staging/smoke

---

## 10.3.3 — Pre-Flight + Operational Runbooks

**Decisión LOCKED:** **C — Pre-flight automatizado + ops runbooks día-a-día + índice maestro**

### Parte 1 — Pre-flight checklist (11 checks, gate de 10.1.3)
Backup (reciente + verificado) · Estado (no incident 8.4.3 + SLO healthy 8.4.1 + error budget) · CI/CD (artifact validated 10.1.2 + security passed 10.1.1) · Compliance (readiness 9.3.3 + threat model current 9.2.1) · Capacidad (resource headroom 10.2.1 + DR test reciente 10.3.2)
→ deploy SOLO si passed (override manual documentado)

### Parte 2 — Ops runbooks (12 día-a-día)
| ID | Runbook |
|----|---------|
| OPS-1 | Onboard workspace |
| OPS-2 | Offboard workspace (GDPR erasure) |
| OPS-3 | Escalar workers |
| OPS-4 | Rotar secret (10.2.3) |
| OPS-5 | Migración manual |
| OPS-6 | Actualizar threat model (R9 9.2.1) |
| OPS-7 | Responder DSAR GDPR (R9 9.3.2) |
| OPS-8 | Generar audit pack (R9 9.3.3) |
| OPS-9 | Investigar alerta (dashboard → logs → trace) |
| OPS-10 | Mantenimiento programado |
| OPS-11 | Onboard miembro equipo (Tailscale + RBAC) |
| OPS-12 | Aprobar skill Pilar 3 (10.1.1 human approval) |

### Parte 3 — Índice maestro (runbook-index.md)
Todos los runbooks del sistema: Operational (OPS-1..12) + Security IR (8 PICERL R9 9.2.3) + DR (DR-1..4 R10 10.3.2) + Incident Ops (R8 8.4.3) + Deploy (10.1.3)

### Parte 4 — Bus factor mitigation (single-owner)
Runbooks versionados Git + ONBOARDING.md + break-glass documentado (R9 insider + 10.2.3 KEK)

### Parte 5 — Living
Lessons loop (cada incident/drill/deploy) + review trimestral

### Audit events
`preflight_checklist_result` · `preflight_override` (Brian + razón) · `ops_runbook_executed`

### Métricas
`preflight_checks_pass_rate` · `preflight_blocks_total` (check) · `ops_runbook_executions_total` (runbook)

### Reusa
10.1.3 (pre-flight es su gate) + 10.3.1 backup + 10.3.2 DR + R8 8.4.1 SLO + 8.4.3 incidents/runbooks + R9 9.2.3 playbooks + 9.2.1 threat model + 9.3.2 DSAR + 9.3.3 readiness + insider break-glass + 10.2.3 secrets

---

## Cierre R10 + 10 rondas técnicas

R10 B3 cierra:
- ✅ Backup resiliente (3-2-1)
- ✅ DR comprobado (testing real) → SOC2 A1.3 cerrado
- ✅ Sistema operable (pre-flight + runbooks + bus factor mitigation)

**Con R10 B3 → R10 100% + las 10 rondas técnicas de For3s OS COMPLETAS. El diseño está cerrado. Próximo: pre-programación (re-revisión R6 + DMN 5.4.2) → CÓDIGO.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_10_B3_Backup_DR_Operations.md`).
