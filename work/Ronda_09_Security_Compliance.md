# Ronda 9 — Security / Compliance (Master)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_09_Security_Compliance.md → work/Ronda_09_Security_Compliance.md (2026-07-30, ADR-029)

## Purpose

Ronda 9 — Security / Compliance (Master)


**Novena de las 10 rondas técnicas. Documento maestro de R9.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-09
**Última actualización:** 2026-06-09
**Estatus:** ✅ **R9 CERRADO 100%** (3 bloques · 9/9 sub-temas LOCKED + 3 pre-preguntas)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — Nodo 7 Amígdala + §6 Seguridad multi-capa
- [Mente/work/Ronda_08_Observabilidad_Completa.md](work/Ronda_08_Observabilidad_Completa.md) — R8 100% CERRADO
- [Mente/work/Ronda_07_Frontend_Channel.md](work/Ronda_07_Frontend_Channel.md) — R7 100% CERRADO (Pilar 1 output)
- [Mente/memory/Estado_Sesion_Continuidad.md](../memory/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Sub-documentos detallados:**
- ✅ [Ronda_09_B1_Amigdala.md](work/Ronda_09_B1_Amigdala.md) — Amígdala Node 7 threat detection (3/3 LOCKED) ⭐ CIERRA 11/11 nodos
- ✅ [Ronda_09_B2_Threat_Pentest_IR.md](work/Ronda_09_B2_Threat_Pentest_IR.md) — Threat Model + Pentest + Incident Response (3/3 LOCKED)
- ✅ [Ronda_09_B3_Compliance_Framework.md](work/Ronda_09_B3_Compliance_Framework.md) — SOC2 + GDPR readiness (3/3 LOCKED) ⭐ CIERRA R9

**Decisiones loggeadas en for3s-inter:**
- [D-035 — Pre-preguntas R9 + B1 Amígdala LOCKED (Node 7 completo)](../../for3s-inter/07-operations/decision-log.md)
- [D-036 — B2 Threat Model + Pentest + IR LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-037 — B3 Compliance Framework LOCKED + R9 100% CERRADO](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core
- 3.D — Equipo pequeño (security self + contratado post-revenue)

**Constraints LOCKED aplicados:**
- D-009 — Minimal stack (sin Lakera/Vanta/SIEM externos v1; self-hostable)
- P3 — Workspace isolation (Amígdala refuerza + cross-workspace leak playbook)
- P4 — Encryption (Master KEK OFFLINE — insider threat playbook)
- OWASP LLM Top 10 — cobertura completa mapeada

**Pre-preguntas P1-P3 LOCKED:**

| # | Pregunta | Decisión | Justificación |
|---|---|---|---|
| **P1** | Alcance Amígdala v1 | **C — Completo multi-capa** | Input scanner + anomaly + coordinator → cierra Node 7 (11/11 nodos) |
| **P2** | Compliance framework | **C — SOC2 + GDPR readiness program** | Audit-ready vendible enterprise B2B (cert real auditor externo v2) |
| **P3** | Pentest + IR | **C — Threat model + pentest plan + playbooks** | STRIDE+DREAD + pentest AI-aware + security playbooks PICERL |

---

## Tabla de contenidos

1. [Propósito de R9](#1-propósito-de-r9)
2. [Estructura B+A — 3 bloques · 9 sub-temas](#2-estructura)
3. [Resumen ejecutivo Bloque 1 — Amígdala](#3-bloque-1-amígdala)
4. [Resumen ejecutivo Bloque 2 — Threat Model + Pentest + IR](#4-bloque-2)
5. [Resumen ejecutivo Bloque 3 — Compliance Framework](#5-bloque-3)
6. [Cobertura del Grafo Maestro](#6-cobertura-grafo-maestro)
7. [11/11 nodos cerebrales completos + Pilar 1 cierre](#7-pilar-1-cierre)
8. [Cobertura OWASP LLM Top 10](#8-owasp-coverage)
9. [Costo total v1 actualizado post-R9](#9-costo-post-r9)
10. [Riesgos consolidados R9 + mitigaciones](#10-riesgos)
11. [Items ejecución post-código](#11-post-codigo)
12. [Próximos pasos R10](#12-proximos-r10)
13. [Flags críticos carry-forward](#13-flags)

---

## 1. Propósito de R9

R9 — **Security / Compliance** es la penúltima ronda. Cumple tres funciones que las rondas anteriores dejaron pendientes:

1. **Cierra el último nodo cerebral (Amígdala Node 7):** las rondas R1-R8 construyeron 10/11 nodos. La Amígdala es el guardián del INPUT — detecta amenazas ANTES del procesamiento cognitivo (fast danger response). Sin ella, For3s OS procesaba TODO input, incluyendo ataques.

2. **Formaliza la seguridad (threat model + pentest + IR):** hasta R9, la seguridad fue "defense in depth" ad-hoc. R9 la hace AUDITABLE — STRIDE+DREAD justifica cada defensa, pentest la valida, security playbooks responden a incidents.

3. **Establece el programa compliance (SOC2 + GDPR):** R8 dio las herramientas (audit + reports). R9 las convierte en programa audit-ready vendible enterprise B2B.

**Resultado:** Pilar 1 Seguridad COMPLETO de verdad — perímetro INPUT (Amígdala) + OUTPUT (Microglia + R7 Output Gate), justificado formalmente, comprobable y compliance-ready.

---

## 2. Estructura

| Bloque | Sub-tema | Decisión LOCKED | Componentes clave |
|---|---|---|---|
| **B1 Amígdala (Node 7)** | 9.1.1 Input Threat Scanner | C — Híbrido multi-capa | 5 capas: heurística + normalize + LLM Haiku + canary + external sanitization |
| | 9.1.2 Anomaly Detection | C — Multi-señal + baselines per-identity | 4 detectores: rate + escalation + deviation + probing + EWMA baselines |
| | 9.1.3 Threat Coordinator | C — Unificado + proporcional + modula GM | 5 niveles DEFCON + fast-path + modula Tálamo/Neuromod/Microglia + tool restrictions |
| **B2 Threat + Pentest + IR** | 9.2.1 Threat Model | C — STRIDE+DREAD formal | 14 componentes + 3 trust boundaries + DREAD scoring + OWASP coverage + living doc |
| | 9.2.2 Pentest Plan | C — Programa formal | 4 capas scope + AI-aware (garak/promptfoo) + custom suite + cadencia + self/contratado |
| | 9.2.3 Security Playbooks | C — 8 playbooks + forensics + legal | PICERL + ForensicsKit (WORM) + GDPR 72h notification |
| **B3 Compliance Framework** | 9.3.1 SOC2 Control Mapping | C — 5 TSC + evidence binding | CC1-CC9 + Availability + Confidentiality + PI + Privacy → controles R1-R9 + evidence auto-gen |
| | 9.3.2 GDPR Program | C — Programa completo | DSAR 6 derechos + consent + DPA + RoPA + privacy data flow |
| | 9.3.3 Evidence + Gap + Readiness | C — Collector + gap + scorecard + monitor | EvidenceCollector + GapAnalyzer + ReadinessScorecard + Monitor + AuditPack 1-click |

---

## 3. Bloque 1 — Amígdala

Ver detalle en [Ronda_09_B1_Amigdala.md](work/Ronda_09_B1_Amigdala.md).

**Node 7 del Grafo Maestro — el último nodo cerebral.** Tres capas que forman el guardián del INPUT:

- **9.1.1 Input Threat Scanner:** 5 capas fail-fast (heurística ~1ms → normalización anti-evasión → LLM Haiku classifier solo suspicious ~10% → canary tokens exfil → external content sanitization para indirect injection en PR/files/webhooks). Cubre OWASP LLM01 (injection) + LLM06 (exfil). ~3ms + $0.0001 promedio.

- **9.1.2 Anomaly Detection:** 4 detectores (rate vs EWMA baseline + conversational escalation gradual jailbreak + behavioral deviation credential-compromise + privilege probing RBAC denials) con baselines per-identity adaptativos y acción graduada (block/challenge/monitor/pass). Cierra el gap conductual multi-request que 9.1.1 no ve. Privacy: behavioral window Redis TTL 1h + solo agregados.

- **9.1.3 Threat Coordinator:** unifica scan + anomaly + boosters en ThreatLevel 5 niveles tipo DEFCON (CLEAR→CRITICAL), respuesta proporcional que MODULA el cerebro vía conexiones literales del Grafo (Amígdala→Tálamo fuerza EMERGENCIA/MINIMO + Amígdala→Neuromod HIGH_ATTENTION + Amígdala→Microglia threat_context para output scrutiny), fast-path real (brain bypass cuando CRITICAL) + tool restrictions dinámicas. **CIERRA Node 7 → 11/11 nodos.**

---

## 4. Bloque 2

Ver detalle en [Ronda_09_B2_Threat_Pentest_IR.md](work/Ronda_09_B2_Threat_Pentest_IR.md).

**La seguridad ahora es entendida + comprobable + respondible:**

- **9.2.1 Threat Model STRIDE+DREAD:** metodología formal per ~14 componentes (3 trust boundaries External→Edge→Brain→Data), STRIDE 6 categorías × componente, DREAD scoring (priorización Critical/High/Med/Low), matriz mitigación → GAPS, cruce OWASP LLM Top 10 (10/10) + OWASP Top 10, living document. Valida retroactivamente que B1 Amígdala cerró gaps reales.

- **9.2.2 Pentest Plan:** 5 dimensiones (scope 4 capas AI+web+infra+audit priorizado DREAD + toolkit self-hostable con AI-specific garak/promptfoo + cadencia commit→release→trimestral→anual + self/contratado triggers + findings→remediation loop). Custom AI Attack Suite versionada = security regression test (valida Amígdala bloquea cada payload). Ejecución post-código.

- **9.2.3 Security Playbooks:** 8 playbooks PICERL (breach + injection success + credential compromise + audit tampering + secrets exposure + insider threat + supply chain + DoS) + ForensicsKit (snapshot audit+traces+logs → R2 WORM + chain of custody) + GDPR 72h legal notification workflow + auto-trigger desde Amígdala fast-path.

---

## 5. Bloque 3

Ver detalle en [Ronda_09_B3_Compliance_Framework.md](work/Ronda_09_B3_Compliance_Framework.md).

**Compliance audit-ready vendible enterprise:**

- **9.3.1 SOC2 Control Mapping:** 5 Trust Service Criteria completas (Security CC1-CC9 + Availability + Confidentiality + Processing Integrity + Privacy) mapeadas a controles R1-R9, con evidence binding (cada control → audit events que lo prueban, soc2_quarterly report 8.3.3 AUTO-GENERA evidencia real desde chain inmutable), gap detection, control matrix, living document. ⭐ **SOC2 = sales wedge** (memoria `project_soc2_sales_wedge`).

- **9.3.2 GDPR Program:** DSAR workflow 6 derechos (Art 15-21) + deadline 30d + consent management (Art 6/7) + DPA template (Art 28, vendible EU) + RoPA (Art 30) + privacy data flow mapping. Une piezas R6 forgetting + R8 pseudonymization + R7 identity + 9.2.3 breach. Doble propósito: satisface SOC2 Privacy TSC.

- **9.3.3 Evidence + Gap + Readiness:** EvidenceCollector (auto desde audit chain) + GapAnalyzer (cruza compliance + threat model + pentest) + ReadinessScorecard (veredicto objetivo AUDIT_READY >90% + 0 critical) + ComplianceMonitor (drift weekly) + AuditPack 1-click (cliente enterprise due diligence). Resultado v1 honesto: SOC2 ~85-90% + GDPR ~88-92% NEARLY_READY → AUDIT_READY post-código.

---

## 6. Cobertura Grafo Maestro

| Nodo / Sección GM | R9 cobertura | Sub-temas |
|---|---|---|
| **Nodo 7 Amígdala** | ✅ COMPLETO (threat detection + fast danger response + brain modulation) | 9.1.1 + 9.1.2 + 9.1.3 |
| §6 Seguridad multi-capa | ✅ Justificada formalmente (STRIDE+DREAD per componente) | 9.2.1 |
| Conexión Amígdala→Tálamo | ✅ Fuerza subgraph EMERGENCIA/MINIMO | 9.1.3 |
| Conexión Amígdala→Neuromod | ✅ Fuerza HIGH_ATTENTION | 9.1.3 |
| Conexión Amígdala→Microglia | ✅ threat_context → output scrutiny | 9.1.3 |
| Pilar 1 Seguridad | ✅ Perímetro INPUT + OUTPUT completo | Todo B1 + R7 + R5/R6 |

**⭐ 11/11 NODOS CEREBRALES COMPLETOS** (Amígdala cierra el cerebro).

---

## 7. Pilar 1 Cierre

R9 cierra Pilar 1 Seguridad de manera completa y verificable:

```
   PERÍMETRO COMPLETO:
   
   INPUT → [AMÍGDALA 9.1.x] → Tálamo → PFC/Multi-agent → ... →
     [MICROGLIA output eval] → [R7 OUTPUT GATE] → response
        ↑ INPUT GUARD (R9)         ↑ OUTPUT GUARD (R5/R6 + R7)
   
   • Input guard: Amígdala (scanner + anomaly + coordinator)
   • Output guard: Microglia (eval) + R7 Output Gate (signing+encrypt)
   • Coordinación: threat_context propagado input→output
   • Justificación: threat model STRIDE+DREAD (9.2.1)
   • Validación: pentest plan + custom attack suite (9.2.2)
   • Respuesta: security playbooks PICERL (9.2.3)
   • Compliance: SOC2 + GDPR audit-ready (B3)
```

**Pilar 1 era "completo operacional" post-R7 (output). R9 lo completa de verdad añadiendo el guardián de INPUT + justificación formal + validación + compliance.**

---

## 8. OWASP Coverage

| OWASP LLM Top 10 | For3s mitigation | Sub-tema |
|---|---|---|
| LLM01 Prompt Injection | Amígdala scanner (directo + indirecto) | 9.1.1 |
| LLM02 Insecure Output | Output Gate + Microglia | R7 + R5/R6 |
| LLM03 Training Poisoning | N/A (no fine-tuning) | — |
| LLM04 Model DoS | Token bucket + Amígdala rate + DoS playbook | R3 + 9.1.2 + 9.2.3 |
| LLM05 Supply Chain | MCP Docker SHA pin + Trivy + supply chain playbook | R4 + 9.2.2 + 9.2.3 |
| LLM06 Sensitive Info Disclosure | Canary + RLS + KEK + breach playbook | 9.1.1 + R4/R7 + 9.2.3 |
| LLM07 Insecure Plugin | Tool authz + sandbox + tool restrictions | R4 + 9.1.3 |
| LLM08 Excessive Agency | RBAC + tool restrictions Amígdala | R7 + 9.1.3 |
| LLM09 Overreliance | Confidence scoring + Microglia eval | R6 + R5 |
| LLM10 Model Theft | LOCAL deploy + auth + audit | D-009 + R7 + R8 |

**10/10 OWASP LLM Top 10 cubiertos** (vendible enterprise + compliance evidence).

---

## 9. Costo post-R9

| Componente | Costo mensual |
|---|---|
| Stack post-R8 baseline | $95-130 |
| Amígdala LLM Haiku classifier (~10% inputs suspicious) | +$0-2 |
| Threat model / pentest plan / playbooks (docs) | $0 |
| Compliance mapping + evidence + readiness | $0 (reusa R8 8.3.3) |
| **TOTAL post-R9 (10 users v1)** | **~$95-132/mo** |

**R9 es mayormente $0** (reusa stack lockeado). El único costo recurrente es el Haiku classifier de Amígdala (~$0.0001/request, solo ~10% inputs suspicious).

**Costos post-revenue (ejecución, no v1 base):**
- Pentest externo anual / pre-enterprise: ~$5-15K por engagement
- SOC2 cert real (auditor externo): ~$10-30K (v2)
- DPA lawyer review: ~$1-3K una vez (pre-primer-deal-EU)
- Vanta/Drata continuous compliance (opcional v2): ~$10-20K/año

---

## 10. Riesgos

| Riesgo | Mitigación |
|---|---|
| Amígdala falsos positivos (bloquea legítimos) | Acción graduada (challenge antes que block) + EWMA baselines + threshold tunable |
| Amígdala bypass (ataque pasa 5 capas) | Playbook 2 (injection success) + custom attack suite regression + lessons loop |
| Cold-start sin baseline (9.1.2) | Learning mode (20 obs mín, no bloquea sin baseline) |
| LLM classifier latencia/costo | Solo ~10% suspicious + Haiku barato |
| Threat model staleness | Living document + trigger features nuevas |
| Pentest no ejecutado v1 | Plan LOCKED, ejecución post-código (P3=C) + custom suite es regression test |
| Insider threat (Brian single-owner) | Break-glass + Master KEK OFFLINE (ya LOCKED) + 2-person rule v2 |
| DPA sin revisión legal | Lawyer review pre-primer-deal-EU (template listo) |
| Compliance % depende de evidencia runtime | v1 muestra estructura, % real post-deploy + honest verdict |
| Cert SOC2 real requiere auditor | P2=C es readiness, cert v2 (Vanta integra el mapping) |

---

## 11. Post-Código

Items que se LOCKEARON como plan pero se EJECUTAN post-código (per instrucción Brian: programación arranca POST-R10):

- **Pentest ejecución** (9.2.2): automated scans CI + manual red team + external anual
- **Custom AI attack suite** (9.2.2): implementar payloads + correr contra staging (regression test)
- **Security playbooks runtime** (9.2.3): ForensicsKit + breach notification operativos
- **DPA lawyer review** (9.3.2): revisión legal del template pre-primer-deal-EU
- **SOC2 cert real** (9.3.1): auditor externo (v2)
- **Recovery/DR testing** (SOC2 A1.3): post-R10 deploy
- **Amígdala patterns/baselines tuning**: con tráfico real + DMN auto-update

---

## 12. Próximos R10

**R10 — CI/CD / Deploy** será la ÚLTIMA ronda técnica. Cubre:

- CI/CD pipeline (GitHub Actions — foundation R4)
- Deploy LOCAL + Cloudflare Tunnel (D-009)
- systemd services + process management
- Backup/recovery operacional (DR testing → cierra SOC2 A1.3)
- Migration/rollback strategy
- Secrets management deploy (KEK bootstrap R4)
- Observability deploy (Prometheus+Loki+Tempo+Grafana stack R8)
- Security hardening deploy (Amígdala + threat model controls R9)
- Pre-flight checklist (compliance readiness R9 B3)

**Después R10 → PROGRAMACIÓN ARRANCA** (con re-revisión obligatoria R6 + DMN 5.4.2).

---

## 13. Flags

### ⚠️ DMN 5.4.2 REFINAMIENTO PENDIENTE
- **Memory:** `project_dmn_tasks_critical_refinement`
- Re-review pre-código profundo de 8 DMN tasks.

### ⚠️ R6 PRE-CODE REVIEW CRÍTICO
- **Memory:** `project_r6_critical_pre_code_review`
- Memory Stack Extensions necesita replanificación pre-implementación.

### ⭐ SOC2 SALES WEDGE
- **Memory:** `project_soc2_sales_wedge`
- SOC2 como "certificado de calidad B2B" → resaltar en página/marketing. 5 TSC ya mapeadas (9.3.1).

Todos persisten hasta pre-programación POST-R10.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_09_Security_Compliance.md`).
