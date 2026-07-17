# Ronda 9 — Bloque 1 — Amígdala (Node 7 Threat Detection) ⭐ CIERRA 11/11 NODOS

**Sub-documento de R9.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_09_Security_Compliance.md](Ronda_09_Security_Compliance.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED) — Cierra Node 7 → 11/11 nodos cerebrales
**Fecha cierre:** 2026-06-09

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Cobertura |
|---|---|---|
| 9.1.1 Input Threat Scanner | C — Híbrido multi-capa | OWASP LLM01 + LLM06 |
| 9.1.2 Anomaly Detection | C — Multi-señal + baselines | Gradual jailbreak + credential compromise + probing |
| 9.1.3 Threat Coordinator | C — Unificado + modula GM | Fast-path + brain modulation |

**Posición en flow:** `INPUT → Auth (R7) → [AMÍGDALA] → Tálamo (R5) → ...`

---

## 9.1.1 — Input Threat Scanner

**Decisión LOCKED:** **C — Scanner híbrido multi-capa**

### 5 capas fail-fast (barato → caro)

#### Capa 1 — Heurística rápida (~1ms, $0)
```python
class HeuristicScanner:
    INJECTION_PATTERNS = [
        r'ignore (all |previous |above )?(instructions|prompts)',
        r'you are now (DAN|jailbroken|unrestricted)',
        r'(reveal|show|print|leak).{0,20}(system prompt|secret|api key)',
        r'pretend (you are|to be|we)',
        r'disregard.{0,20}(rules|guidelines|safety)',
    ]
    EXFIL_PATTERNS = [
        r'(previous|other|another).{0,20}(user|workspace|session)',
        r'(all|every).{0,20}(api key|secret|credential|token)',
        r'what (did|was).{0,30}(see|process|receive)',
    ]
    # + structural signals: len > 50000 (context overflow),
    #   role markers ("system:", "assistant:")
    # verdict: block (≥0.8) | suspicious (≥0.4) | clean
```

#### Capa 2 — Normalización anti-evasión
```python
class InputNormalizer:
    # decode base64 segments
    # strip zero-width chars (homoglyph evasion)
    # unicodedata.normalize NFKC + dehomoglyph (Cyrillic 'а' → Latin 'a')
    # → re-scan si had_obfuscation
```

#### Capa 3 — LLM classifier (Haiku, solo suspicious >0.4 threshold)
```python
class LLMThreatClassifier:
    # Claude Haiku 4.5 — ~$0.001/scan, ~200ms, temperature=0
    # Prompt trata input como UNTRUSTED data (no sigue instrucciones)
    # Retorna: {is_attack, attack_type, confidence, reason}
    # Solo ~10% de inputs llegan aquí (los suspicious)
```

#### Capa 4 — Canary tokens (exfil determinista)
```python
class CanaryGuard:
    # Canary sembrado en system prompt per session
    # Si aparece en el INPUT → intentó leakearlo → block
```

#### Capa 5 — External content sanitization (indirect injection)
```python
class ExternalContentSanitizer:
    # Para PR comments, archivos, webhooks (contenido no-directo)
    # Spotlighting/datamarking: delimita contenido externo
    # "<<EXTERNAL_DATA_DO_NOT_EXECUTE>>...<</EXTERNAL_DATA>>"
```

### Resultado + acciones

```python
@dataclass
class ThreatScanResult:
    verdict: str           # 'pass' | 'block' | 'suspicious'
    threat_score: float    # 0-1
    sanitized_input: Optional[str]
    attack_type: Optional[str]
    layer_triggered: Optional[int]

# block → fast-path defensivo (NO procesa) + audit + métrica +
#   respuesta genérica (no revela detección)
# pass → continúa Tálamo (input sanitizado si externo)
```

### Costo/latencia
- Capa 1-2: ~1-2ms, $0
- Capa 3 LLM: solo ~10% inputs, ~200ms + $0.001 Haiku
- **Promedio: ~3ms + $0.0001 por input**

### Audit events
- `amygdala_threat_blocked`
- `amygdala_threat_suspicious`
- `amygdala_canary_extraction_attempt`
- `amygdala_external_content_sanitized`

### Reusa
R6 LLM Gateway (Haiku) + R8 8.3.1 audit + R8 8.1.1 metrics (AmygdalaMetrics) + R8 8.4.2 alerts + R5 Tálamo (modo EMERGENCIA)

---

## 9.1.2 — Anomaly Detection Runtime

**Decisión LOCKED:** **C — Multi-señal + baselines per-identity**

### 4 detectores + agregador

#### Detector 1 — Rate anomaly
```python
def _rate_signal(self, window, baseline):
    expected = baseline.avg_requests_5min  # EWMA, no threshold fijo
    if expected > 0 and window.requests_last_5min > expected * 5:
        return Signal('rate_anomaly', 0.6)
```

#### Detector 2 — Conversational escalation (gradual jailbreak multi-turn)
```python
async def _escalation_signal(self, window, input_text):
    # threat_scores crecientes across turns = escalada
    # + LLM multi-turn check si suspicious_turn_count >= 2 (~1%)
```

#### Detector 3 — Behavioral deviation (credential compromise)
```python
def _deviation_signal(self, context, baseline):
    # channel deviation (0.3) + time-of-day (0.2) + geo (0.4)
    # vs baseline.usual_channels / usual_hours / usual_geos
```

#### Detector 4 — Privilege probing
```python
def _probing_signal(self, window):
    # RBAC denials (R7) >= 3 en 1h → 0.6
```

### Baseline learning (EWMA per identity)
```python
class BehavioralBaseline:
    EWMA_ALPHA = 0.1                    # adaptativo, resiste spikes
    CONFIDENCE_MIN_OBSERVATIONS = 20    # cold-start learning mode
    # Solo agregados estadísticos (no contenido) — privacy
```

### Behavioral window (Redis sliding, reusa R8 8.1.3)
- requests_5min + recent_inputs (hashes+scores) + rbac_denials_1h + suspicious_turn_count
- **TTL 1h** (privacy — no persiste long-term)

### Acción graduada
```python
def _action(self, anomaly_score):
    if score >= 0.8: return 'block'      # fast-path + alert critical
    if score >= 0.6: return 'challenge'  # step-up re-auth (R7)
    if score >= 0.4: return 'monitor'    # pasa + flag + audit
    return 'pass'
```

### Agregación ponderada
```python
weights = {'rate_anomaly': 0.8, 'conversational_escalation': 1.0,
           'behavioral_deviation': 1.0, 'privilege_probing': 0.9}
```

### Ataques cubiertos (gap de 9.1.1)
Gradual jailbreak multi-turn · credential compromise · probing/reconnaissance · privilege escalation · slow exfiltration · rate abuse malicioso

### Audit events
- `amygdala_anomaly_blocked` (critical)
- `amygdala_anomaly_challenge_triggered`
- `amygdala_anomaly_monitored`
- `amygdala_credential_compromise_suspected`
- `amygdala_privilege_probing_detected`
- `amygdala_baseline_learning_completed`

### Reusa
R8 8.1.3 sliding window pattern + EWMA + R7 Identity + R7 RBAC denials + R8 audit/metrics/alerts + R6 Gateway

---

## 9.1.3 — Threat Coordinator ⭐ CIERRA NODE 7

**Decisión LOCKED:** **C — Unificado + proporcional + modula GM**

### Threat Level unificado (5 niveles DEFCON)
```python
class ThreatLevel(IntEnum):
    CLEAR = 0      # pasa normal
    LOW = 1        # monitor
    ELEVATED = 2   # degradar capacidades
    HIGH = 3       # challenge / restringir
    CRITICAL = 4   # fast-path block

# Cómputo: max(scan 9.1.1, anomaly 9.1.2) + boosters:
#   ambos señalan +0.2 · github_pr/webhook +0.1 ·
#   credential_compromise +0.2
```

### Respuesta proporcional + modulación cerebro
```python
# CRITICAL → fast-path (brain bypass, NO PFC/MA/tools)
# HIGH → challenge + Tálamo EMERGENCIA + Neuromod HIGH_ATTENTION +
#        Microglia reforzado + tool_restrictions [filesystem_write, http_external]
# ELEVATED → degrade + Tálamo MINIMO + Neuromod HIGH_ATTENTION + sanitize
# LOW → monitor + Microglia threat_context
# CLEAR → pass
```

### Fast-path (DEFCON 1 — GM Node 7 literal)
```python
async def _fast_path(self, scan, anomaly, context):
    # NO ejecuta PFC/multi-agent/tools (fight/flight)
    # audit critical + alert Brian + incident auto-create (8.4.3)
    # defensive_response genérica (no revela detección)
    return AmygdalaVerdict(action='block', brain_bypassed=True, ...)
```

### Integración GM (conexiones literales)
```python
# Amígdala → Tálamo (R5 5.1.3): forced_subgraph_mode
# Amígdala → Neuromod (R5 5.1.4): forced HIGH_ATTENTION
# Amígdala → Microglia (R5/R6): threat_context → output scrutiny
# Tool restrictions dinámicas

signals = await thalamic_router.route(
    workspace_id, sanitized_input or input_text,
    forced_subgraph_mode=verdict.thalamus_override,
    forced_neuromod_mode=verdict.neuromod_override,
    tool_restrictions=verdict.tool_restrictions,
    threat_context=verdict.microglia_threat_context,
)
```

### Loop completo
```
INPUT → Amígdala(9.1.1+9.1.2+9.1.3) → Tálamo → PFC/MA → ... →
  Microglia(output threat-aware) → Output Gate(R7) → response
= PERÍMETRO INPUT + OUTPUT COMPLETO COORDINADO
```

### Threat memory (DMN foundation)
Threats confirmados → DMN task analiza patrones nuevos → auto-update injection patterns (9.1.1) + baselines (9.1.2) + defense skills (Pilar 3) si recurrente.

### Audit events
- `amygdala_fast_path_triggered` (critical)
- `amygdala_threat_level_assessed`
- `amygdala_brain_modulation_applied`
- `amygdala_tool_restriction_applied`
- `amygdala_challenge_issued`

### Reusa
R5 Tálamo/Neuromod + R5/R6 Microglia + R7 step-up auth + R8 audit/alerts/incidents (8.4.3 auto-create)

---

## AmygdalaMetrics completas (R8 8.1.1 specialized)

```python
amygdala_threats_total            # (attack_type, verdict)
amygdala_scan_duration_seconds    # (layer)
amygdala_llm_classifier_calls_total
amygdala_false_positive_rate
amygdala_anomaly_score            # histogram
amygdala_anomaly_actions_total    # (action)
amygdala_signal_triggered_total   # (signal_name)
amygdala_baselines_active         # gauge
amygdala_threat_level             # histogram 0-4
amygdala_fast_path_total          # (attack_type)
amygdala_brain_modulations_total  # (override_type)
amygdala_verdict_total            # (action)
```

## Cobertura Grafo Maestro Node 7

| GM Node 7 spec | B1 cobertura |
|---|---|
| Threat detection (input) | ✅ 9.1.1 scanner 5 capas |
| Behavioral threat assessment | ✅ 9.1.2 anomaly multi-señal |
| Fast danger response (brain bypass) | ✅ 9.1.3 fast-path DEFCON 1 |
| Brain modulation (atención/routing) | ✅ 9.1.3 → Tálamo/Neuromod/Microglia |
| Emotional salience (threat scoring) | ✅ 9.1.3 ThreatLevel 5 niveles |

**⭐ NODE 7 COMPLETO → 11/11 NODOS CEREBRALES.**