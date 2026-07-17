# Ronda 3 — Bloque 3: Streaming & Performance

**Sub-documento detallado de R3 — Model/LLM Layer. Bloque 3 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-03
**Estatus:** ✅ LOCKED (3/3 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema con profundidad R2)
**Documento padre:** [Ronda_03_Model_LLM_Layer.md](Ronda_03_Model_LLM_Layer.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes

**Dependencias resueltas en B1 + B2:**
- ✅ ClaudeProvider con streaming nativo (B1)
- ✅ FailoverManager Anthropic → OpenAI (B1 3.1.4)
- ✅ ContextBuilder con tokens estimados (B2 3.2.2)
- ✅ CacheManager 4 layers (B2 3.2.3)
- ✅ ToolExecutor loop estándar (B2 3.2.4)
- ✅ CapacityLimiter(3) global (R2 B3 LOCKED)
- ✅ LLM_CALL_TIMEOUT 60s (R2 B3 LOCKED)
- ✅ Valkey en stack (R2 B3 LOCKED)

**Fuente de verdad:**
- [`For3s_OS_Grafo_Maestro.md`](../Cerebro/For3s_OS_Grafo_Maestro.md) §4 Nodo 3 PFC + Nodo 6 Sistema Sensorial + Pilar 2

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 3.3.1 — Streaming responses](#3-sub-tema-331--streaming-responses)
4. [Sub-tema 3.3.2 — LLM concurrency control](#4-sub-tema-332--llm-concurrency-control)
5. [Sub-tema 3.3.3 — Retry & fallback patterns](#5-sub-tema-333--retry--fallback-patterns)
6. [Stack final consolidado](#6-stack-final-consolidado)
7. [Cobertura del Grafo Maestro](#7-cobertura-del-grafo-maestro)
8. [Costo total post-Bloque 3](#8-costo-total-post-bloque-3)
9. [Exploraciones futuras NO adoptadas v1](#9-exploraciones-futuras-no-adoptadas-v1)
10. [Implicaciones en Bloque 4 y rondas futuras](#10-implicaciones-en-bloque-4-y-rondas-futuras)
11. [Riesgos legítimos aceptados](#11-riesgos-legítimos-aceptados)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 3 — STREAMING & PERFORMANCE                           ║
║   3 sub-temas LOCKED el 2026-06-03                             ║
║                                                                ║
║   3.3.1 Streaming responses    → SSE (Server-Sent Events)       ║
║   3.3.2 LLM concurrency control → CapacityLimiter + TokenBucket ║
║   3.3.3 Retry & fallback        → Taxonomía + Policy + Circuit  ║
║                                                                ║
║   Foundation lista para:                                        ║
║   • R3 B4 Observabilidad LLM                                    ║
║   • R7 Frontend / Channel (streaming compatible)                ║
║   • R8 Observability (métricas obligatorias definidas)          ║
║   • R9 Security/Compliance (alarmas críticas mapeadas)          ║
║                                                                ║
║   Costo incremental B3 R3:      ~$0 infra (todo en código)       ║
║   Impacto LLM costs:              -10-15% (mejor manejo errores) ║
║   UX percepción velocidad:       3-10x mejor (TTFT streaming)     ║
║   Costo total v1:                 ~USD 62/mes (sin cambio neto)  ║
║   % techo Pilot Light:            5.4% (margen 94.6%)             ║
║   % cap P5 LLM:                   28% del max + enforcement auto  ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Resiliencia operacional sin sobre-ingeniería. Cada componente
del Bloque 3 maneja un tipo específico de falla con la mínima
complejidad necesaria. La UX percibida del usuario es lo más
importante — streaming hace que se sienta rápido, concurrency
control evita que se caiga, retry/fallback hace que se recupere."
```

Las 3 decisiones convergen en patrones consistentes:

```
1. UX MODERNA (3.3.1)
   → Streaming SSE estándar HTTP
   → Cancel anticipado, partial preserve
   → Foundation R7 frontend (web, Telegram, etc.)

2. ENFORCEMENT AUTOMÁTICO (3.3.2)
   → Token Bucket per workspace
   → Cap P5 LLM enforced sin intervención manual
   → Per-workspace fairness real
   → 95% reducción Anthropic 429s

3. ERRORES TRATADOS CORRECTAMENTE (3.3.3)
   → Taxonomía 14 ErrorTypes
   → RetryPolicy explícita por tipo (no genérica)
   → Circuit breaker anti-cascada
   → -10-15% costo LLM por errores mal manejados

4. INTEGRACIÓN PROFUNDA CON B1+B2
   → No duplica abstracciones existentes
   → Streaming usa ClaudeProvider nativo
   → Token bucket coordina con FailoverManager
   → Retry/fallback respeta opt-out workspace

5. FOUNDATION RONDAS FUTURAS
   → R7 streaming UX
   → R8 métricas obligatorias definidas
   → R9 alarmas críticas mapeadas
```

### Por qué esta filosofía importa

**Para Pilar 1 Seguridad:** audit chain inmutable de retry/fallback/circuit + idempotency tools + workspace fairness anti-DoS interno.

**Para Pilar 2 Escalabilidad:** streaming reduce memoria servidor (event-by-event vs full buffer), concurrency control evita saturación, circuit breaker fails-fast durante outages.

**Para Pilar 3 Autonomía:** agente decide qué error reintentar y qué fallar; tool calls heredan política de retry sin LLM re-loop completo.

---

## 3. Sub-tema 3.3.1 — Streaming responses

### Decisión LOCKED

```
SSE (Server-Sent Events) HTTP estándar
```

### Contexto

Sin streaming, usuario espera ciegamente 3-15s mirando "..." hasta respuesta completa. Con streaming, ve tokens en tiempo real. Para For3s OS universal (cualquier dominio):
- Conversaciones con razonamiento generan 500-2000 tokens
- A 50 tokens/s, esperar full = 10-40 segundos
- Streaming hace que el usuario "vea pensar" al agente

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** genera output que fluye al cliente
- **Nodo 6 Sistema Sensorial:** recibe input/devuelve output por canal
- **Pilar 2 Escalabilidad:** streaming reduce memoria servidor
- **Pilar 1 Seguridad:** preservar audit chain integrity

### Candidatos evaluados

```
A) NO streaming v1                              ❌ UX horrible
B) SSE (Server-Sent Events) HTTP                 ✅ ELEGIDO
C) WebSocket bidireccional                       ⚠️ Complejidad innecesaria
D) Streaming Anthropic SDK directo               ❌ Rompe abstraction
E) Hybrid SSE + WebSocket opt-in                 📚 Futuro v2-v3
```

### Eventos SSE LOCKED v1

```
event: stream_start
data: {"conversation_id": "uuid", "model": "claude-sonnet-4-6", "audit_event_id": "..."}

event: text_delta
data: {"delta": "El análisis", "index": 0}

event: tool_use_start
data: {"tool_name": "recall_memory", "tool_use_id": "tu_xxx"}

event: tool_use_complete
data: {"tool_use_id": "tu_xxx", "input": {...}}

event: tool_result
data: {"tool_use_id": "tu_xxx", "result": {...}}

event: message_complete
data: {"stop_reason": "end_turn", "usage": {...}}

event: fallback_activated
data: {"provider": "openai"}

event: stream_partial
data: {"audit_flag": "partial", "bytes_streamed": N, "reason": "..."}

event: error
data: {"error_type": "...", "message": "...", "retryable": bool}

event: stream_end
data: {"audit_event_id": "..."}
```

### Reglas duras LOCKED

```
✅ SSE como transport canónico v1
✅ event: + data: format (estándar SSE)
✅ JSON payload en cada data:
✅ Check is_disconnected() en cada event yield
✅ Audit start + cada event significativo + complete + cancelled
✅ CancelledError re-raise siempre (R2 B3 3.4)
✅ llm_limiter wrap completo del stream
✅ LLM_CALL_TIMEOUT 60s aplica a TOTAL stream
✅ Heartbeat ping cada 15s si silencio prolongado
✅ Failover OpenAI streaming compatible (adapter)
✅ Cache marker preservado en stream (B2 3.2.3)
✅ Tool use events expuestos vía SSE
✅ NO retry mid-stream (regla heredada por 3.3.3)
✅ Partial preserve con audit_flag si stream se interrumpe
```

### Performance characteristics

```
Latencia primer token (TTFT):
   Sin streaming:  3-10 segundos
   Con streaming:  ~500ms-1.5s  (3-10x mejor UX)

Throughput tokens:
   50-80 tokens/s en ambos (mismo total)
   Diferencia: los ves conforme llegan

Memoria servidor:
   Sin streaming:  buffer response completa
   Con streaming:  buffer mínimo (event-by-event)

Concurrent connections:
   Sin streaming:  ~100/instance
   Con streaming:  ~30-50/instance
   → llm_limiter(3) ya controla esto
```

### Cost impact

```
Streaming NO cambia costos LLM (mismo total tokens).
Pero AHORRA en cancels tempranos:

Sin streaming:
   Cliente espera 8s → recibe → "no era esto" → 100% cost

Con streaming:
   Cliente ve primer párrafo 1s → cancel → ~15-25% cost

Estimación ahorro mensual: ~10-15% LLM costs en producción real
```

---

## 4. Sub-tema 3.3.2 — LLM concurrency control

### Decisión LOCKED

```
Capa 1: CapacityLimiter(3) global [R2 B3 LOCKED reused]
Capa 2: Token Bucket per workspace en Valkey (NUEVO B3)
```

### Contexto

**Anthropic rate limits actuales (Sonnet 4.6 tier 1):**
- 50 requests/minute (RPM)
- 50,000 input tokens/minute (ITPM)
- 10,000 output tokens/minute (OTPM)

Sin control: 5 clientes paralelos → 3 quedan en queue Anthropic + 2 reciben 429 → fallback cascada → memory spike + latencias x5.

Con control: degradación gradual y predecible + cap P5 enforcement automático per workspace.

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** orquestador necesita saber su capacidad real
- **Nodo 8 Tálamo (R5):** router debe respetar capacidad LLM
- **Nodo 11 Neuromoduladores:** "stress level" = saturación LLM
- **Pilar 2 Escalabilidad:** concurrency es el throttle real
- **Pilar 1 Seguridad:** workspace fairness evita DoS interno
- **P5 cap LLM:** rate limit per workspace previene runaway

### Candidatos evaluados

```
A) Solo CapacityLimiter global (R2 B3 ya LOCKED)         ⚠️ Insuficiente
B) CapacityLimiter + Token Bucket per workspace           ✅ ELEGIDO
C) Queue distribuida con Redis/Valkey + priorities         ❌ Over-engineering
D) Rate limiter proactivo proxy (envoy / kong)             ❌ Externo, complejo
E) Backpressure adaptativo con métricas Anthropic          📚 Futuro v2-v3
```

### Arquitectura de 2 capas

```
CAPA 1 (global): llm_limiter CapacityLimiter(3)
   • "Máximo 3 calls simultáneos a Anthropic"
   • Reused de R2 B3 3.4
   • Zero dependencias adicionales

CAPA 2 (per workspace): Token Bucket en Valkey
   • bucket:rpm:workspace_id   → tokens, refill por minuto
   • bucket:tpm:workspace_id   → tokens, refill por minuto
   
   Tiers LOCKED v1:
      pilot_light:  10 RPM / 10K TPM
      pilot_pro:    50 RPM / 50K TPM
      enterprise:   100 RPM / 100K TPM (v2)
```

### Algoritmo Token Bucket

```
1. Pre-call:
   • take 1 token de bucket:rpm
   • take estimated_input_tokens de bucket:tpm
   • Si ambos OK → procede
   • Si vacío → wait max 30s con jitter o return 429

2. Refill automático:
   • Cada segundo Valkey rellena proporcional
   • Server-side timestamps (no client clock skew)

3. Post-call:
   • Ajustar tpm bucket con tokens reales
   • Refund excedente o force-take extra
```

### Estimación pre-call

```python
def estimate_input_tokens(context: LLMContext) -> int:
    # Anthropic: ~3.5 chars per token
    total_chars = sum(len(json.dumps(p)) for p in context.parts)
    estimated = total_chars / 3.5
    return int(estimated * 1.1)  # +10% margin
```

### Reglas duras LOCKED

```
✅ Capa 1 (CapacityLimiter global) ya LOCKED R2 B3 3.4
✅ Capa 2 (Token Bucket per workspace) NUEVA R3 B3 3.3.2
✅ Algoritmo: Token Bucket (NO Leaky Bucket)
✅ Storage: Valkey (sub-ms latency, ya en stack)
✅ Tiers LOCKED:
   pilot_light:  10 RPM / 10K TPM
   pilot_pro:    50 RPM / 50K TPM
✅ Estrategia exceso: wait max 30s, sino 429 Retry-After
✅ Tool calls: heredan workspace bucket (1 RPM/agent.invoke)
✅ Streaming: acquire UNA vez por stream
✅ Anthropic 429 → trigger fallback + penalize bucket
✅ Estimation pre-call: chars/3.5 × 1.1 margin
✅ Refund/adjust con tokens reales post-call
✅ Audit cada acquire/release/exceed
✅ Si Valkey down → solo CapacityLimiter activo + alarma
```

### Errores y backpressure

```python
class RateLimitExceeded(Exception):
    workspace_id: str
    dimension: str  # "rpm" | "tpm" | "global"
    retry_after: float  # seconds

# Headers HTTP:
# Retry-After: <seconds>
# X-RateLimit-Dimension: rpm|tpm|global
```

### Métricas obligatorias

```
concurrency_acquire_total{workspace_id, tier}
concurrency_acquire_wait_seconds{workspace_id}
concurrency_rate_limit_exceeded{workspace_id, dimension}
concurrency_anthropic_429_received{workspace_id}
token_bucket_rpm_remaining{workspace_id}
token_bucket_tpm_remaining{workspace_id}
capacity_limiter_in_flight
capacity_limiter_queue_depth
```

### Cost impact

```
Sin Capa 2:
   Pilot Light cliente "loco" → gasta Pilot Pro pricing
   $50 cap teórico → $150-200 real
   P5 enforcement: imposible
   Anthropic 429s: frecuentes en bursts

Con Capa 2:
   Pilot Light HARD-capped a 10 RPM / 10K TPM
   P5 enforcement: AUTOMÁTICO
   Anthropic 429s: ~95% eliminados
   Cost predictability: ALTA
```

---

## 5. Sub-tema 3.3.3 — Retry & fallback patterns

### Decisión LOCKED

```
Taxonomía 14 ErrorTypes + RetryPolicy per tipo + Circuit Breaker per provider
```

### Contexto

Errores LLM no son binarios. Son un **espectro**: network transient, rate limit, outage, timeout, safety filter, auth failure, tool errors, streaming interruption, etc. Tratarlos todos igual = retries inútiles, side effects duplicados, UX horrible.

**Lo que YA teníamos (insuficiente solo):**
- B1 3.1.4: FailoverManager Anthropic → OpenAI con 3 retries [1s, 4s, 16s]
- B2 3.2.4: ToolExecutor maneja errores tool específicamente
- R2 B3: LLM_CALL_TIMEOUT 60s + CancelledError re-raise

**Lo que añade B3 3.3.3:**
- Taxonomía exhaustiva de errores (14 tipos)
- Política de retry/fallback por TIPO
- Idempotency semantics
- Circuit breaker per provider
- Cliente-facing error messages

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** debe degradar gracefully si LLM falla
- **Nodo 8 Tálamo (R5):** router puede reintentar via path diferente
- **Nodo 11 Neuromoduladores:** "noradrenalina" = sistema en alerta
- **Pilar 1 Seguridad:** retry no debe duplicar tool calls destructivas
- **Pilar 2 Escalabilidad:** circuit breaker evita cascadas
- **Pilar 3 Autonomía:** agente "intenta otra cosa" autónomamente

### Candidatos evaluados

```
A) Solo retry simple Anthropic (extender B1 3.1.4)         ⚠️ Insuficiente
B) Taxonomía + retry/fallback por tipo + circuit breaker    ✅ ELEGIDO
C) Retry agresivo con cola + dead letter queue              ❌ Over-engineering
D) Solo cliente decide retry (sin retry servidor)            ❌ UX horrible
E) Adaptive retry con ML predictivo                          📚 Futuro v3
```

### Taxonomía LOCKED v1 — 14 ErrorTypes

```python
class ErrorType(Enum):
    # Transient — retry agresivo OK
    NETWORK_TRANSIENT       = "network_transient"
    PROVIDER_5XX            = "provider_5xx"
    TIMEOUT                 = "timeout"
    
    # Rate limit — retry con backoff específico
    RATE_LIMIT_PROVIDER     = "rate_limit_provider"     # 429 Anthropic
    RATE_LIMIT_CLIENT       = "rate_limit_client"        # 429 nuestro bucket
    
    # Permanent — NO retry, fallback selectivo
    AUTH_FAILURE            = "auth_failure"             # 401 — alarma
    BAD_REQUEST             = "bad_request"              # 400 — bug
    SAFETY_FILTER           = "safety_filter"            # 400 safety
    
    # Streaming-specific
    STREAM_INTERRUPTED      = "stream_interrupted"
    STREAM_TIMEOUT          = "stream_timeout"
    
    # Tool-specific (B2 3.2.4)
    TOOL_PERMISSION         = "tool_permission_denied"
    TOOL_VALIDATION         = "tool_validation_error"
    TOOL_EXTERNAL_API       = "tool_external_api_error"
    TOOL_TIMEOUT            = "tool_timeout"
```

### RetryPolicy per ErrorType LOCKED

```
NETWORK_TRANSIENT:    max=3, backoff=[0.5,2,8], jitter, fallback_after=2
PROVIDER_5XX:         max=2, backoff=[1,4], fallback_after=1
TIMEOUT:              max=1, backoff=[2], fallback_after=1
RATE_LIMIT_PROVIDER:  max=3, backoff=USE_RETRY_AFTER, penalize_bucket=True
RATE_LIMIT_CLIENT:    max=0, return_429
AUTH_FAILURE:         max=0, alarm_critical, fallback_after=0
BAD_REQUEST:          max=0, alarm_developer, return_500
SAFETY_FILTER:        max=0, return_400_explanation
STREAM_INTERRUPTED:   max=0, preserve_partial
STREAM_TIMEOUT:       max=0, cancel_stream
TOOL_PERMISSION:      max=0, tool_result_error
TOOL_TIMEOUT:         max=1, backoff=[1]
TOOL_EXTERNAL_API:    max=2, backoff=[1,3]
```

### Circuit Breaker per provider

```
ESTADOS:
   CLOSED    — funciona normal
   OPEN      — provider down, NO mandar requests (fail fast)
   HALF_OPEN — testing recovery, 1 request prueba

TRANSICIONES:
   CLOSED → OPEN:    5 errors 5xx/timeout en 60s window
   OPEN → HALF_OPEN: tras 30s sleep
   HALF_OPEN → CLOSED: prueba exitosa
   HALF_OPEN → OPEN:  prueba falla

BENEFICIOS:
   • Anthropic down 5 min → NO mandamos 100 requests fallidas
   • Failover OpenAI inmediato durante OPEN
   • Auto-recovery cuando provider se recupera
```

### Idempotency tools

```python
# Tools declaran si son safe-retry
class WriteMemoryTool(Tool):
    metadata = {'idempotent': True}  # OK retry, dedupe by id

class SendEmailTool(Tool):
    metadata = {'idempotent': False}  # NO retry, evita doble email
```

### Cliente-facing error mapping

```
ErrorType                  HTTP    Mensaje cliente
─────────────────────────────────────────────────────────────────────
NETWORK_TRANSIENT          503     Servicio temporalmente no disponible
RATE_LIMIT_CLIENT          429     Has excedido tu cuota, espera y reintenta
RATE_LIMIT_PROVIDER        503     Sistema saturado, reintenta en breve
AUTH_FAILURE               500     Error config sistema, contacta soporte
BAD_REQUEST                400     Request inválido, revisa parámetros
SAFETY_FILTER              400     Contenido rechazado por filtros, revisa query
STREAM_INTERRUPTED         200     Respuesta parcial — conexión interrumpida
TOOL_PERMISSION            200     Tool denegada — agente continuó sin ella

Headers obligatorios:
   Retry-After: <seconds>        (para 429 y 503)
   X-LLM-Provider: anthropic|openai
   X-Error-Type: <ErrorType>
```

### Reglas duras LOCKED

```
✅ Taxonomía 14 ErrorTypes LOCKED
✅ RetryPolicy per ErrorType (no negotiable)
✅ Circuit Breaker per provider (5 errors/60s → OPEN, 30s → HALF_OPEN)
✅ NO retry mid-stream (preserve partial + audit flag)
✅ Tool retry separado del LLM retry
✅ Idempotency declarada per tool (idempotent=True/False)
✅ Tools NO idempotentes → NO retry
✅ Headers cliente: Retry-After, X-LLM-Provider, X-Error-Type
✅ Audit cada retry + circuit state change + fallback activation
✅ Alarmas críticas (auth, both_down, circuit open prolongado)
✅ Penalize token bucket en rate_limit_provider (coord 3.3.2)
✅ Respect opt-out (allow_llm_fallback workspace flag)
✅ CancelledError re-raise siempre (R2 B3 3.4)
```

### Métricas obligatorias

```
llm_retry_attempts{workspace_id, provider, error_type}
llm_retry_success{workspace_id, provider, error_type, attempts_taken}
llm_retry_exhausted{workspace_id, provider, error_type}
llm_fallback_activated{workspace_id, from_provider, to_provider}
circuit_breaker_state{provider}        # 0=CLOSED, 1=HALF_OPEN, 2=OPEN
circuit_breaker_transitions{provider, from, to}
tool_retry_attempts{tool_name, error_type}
stream_partial_count{workspace_id}
auth_failure_count                      # alarma crítica
both_providers_down_count               # alarma crítica
```

### Cost impact

```
SIN resilience madura:
   • ~15-20% calls "desperdiciadas" en errores mal manejados

CON resilience B:
   • ~3-5% calls en error, todas justificadas

Ahorro mensual estimado: ~10-15% LLM costs
Beneficio principal: UX claro + observability + foundation R8/R9
```

---

## 6. Stack final consolidado

```
COMPONENTE                          DECISIÓN                          COSTO
─────────────────────────────────────────────────────────────────────────
Streaming transport                 SSE (Server-Sent Events) HTTP     $0
Framework streaming                 FastAPI + sse_starlette MIT       $0
Cancel mid-stream                   is_disconnected() check            $0
Heartbeat                           15s ping si silencio                $0
Concurrency Capa 1                  CapacityLimiter(3) [R2 B3 reused] $0
Concurrency Capa 2                  Token Bucket per workspace         $0 (Valkey)
Estimación tokens pre-call          chars/3.5 × 1.1                    $0
Refund post-call                    diff con números reales            $0
Tiers RPM/TPM                       LOCKED por workspace               $0
Error taxonomy                       14 ErrorTypes                       $0
Retry policies                       Per type explícita                  $0
Circuit breaker                      Per provider (Anthropic, OpenAI)    $0
Idempotency tools                    Metadata flag per tool             $0
Headers HTTP                          Retry-After, X-LLM-Provider, etc.  $0
Alarmas críticas                      Brian Telegram inmediato            $0
─────────────────────────────────────────────────────────────────────────
TOTAL incremental B3 R3                                                ~$0/mes
TOTAL v1 (R1+R2+R3 B1+B2+B3)                                          ~$62/mes
Impacto LLM costs                                                       -10-15%
```

### Estructura módulo for3s_os/llm/ extendida

```
for3s_os/llm/
├── base.py                         → LLMProvider Protocol (B1)
├── anthropic_provider.py           → ClaudeProvider (B1)
├── openai_provider.py              → GPTProvider fallback (B1)
├── failover.py                     → FailoverManager (B1 extendido B3)
├── prompts/                        → 3.2.1 framework (B2)
├── context_builder.py              → 3.2.2 (B2)
├── reranker.py                     → 3.2.2 (B2)
├── token_packer.py                 → 3.2.2 (B2)
├── cache.py                        → 3.2.3 (B2)
├── cache_invalidator.py            → 3.2.3 (B2)
├── tools/                          → 3.2.4 (B2)
├── streaming/                      → 3.3.1 NUEVO B3
│   ├── sse.py                      → SSE transport
│   ├── orchestrator.py             → StreamOrchestrator
│   ├── events.py                   → SSE event types LOCKED
│   └── heartbeat.py                → 15s ping
├── concurrency/                    → 3.3.2 NUEVO B3
│   ├── controller.py               → ConcurrencyController (2 capas)
│   ├── token_bucket.py             → Valkey-backed bucket
│   ├── tier_limits.py              → Tiers LOCKED
│   └── estimator.py                → Token estimation
├── resilience/                     → 3.3.3 NUEVO B3
│   ├── manager.py                  → ResilienceManager
│   ├── taxonomy.py                 → 14 ErrorTypes
│   ├── policies.py                 → RetryPolicy per type
│   ├── circuit_breaker.py          → Per-provider CB
│   ├── error_mapping.py            → Provider error → ErrorType
│   └── client_errors.py            → HTTP status + messages
├── cost_tracker.py                 → per-workspace (B1)
└── llm_observability.py            → métricas (B1, extendido B3)
```

### Patrones obligatorios añadidos B3

```
✓ SSE events estándar (event: + data:)
✓ is_disconnected() check cada yield
✓ llm_limiter wrap completo del stream
✓ Heartbeat 15s si silencio
✓ NO retry mid-stream
✓ Partial preserve con audit_flag
✓ Token Bucket acquire UNA vez por stream
✓ Estimation pre-call con margin 10%
✓ Refund/charge post-call con números reales
✓ Tiers per workspace LOCKED
✓ wait max 30s antes de 429
✓ Anthropic 429 → trigger fallback + penalize bucket
✓ Circuit breaker per provider (5/60s → OPEN, 30s → HALF_OPEN)
✓ NO retry types permanentes (auth, bad_request, safety)
✓ Tool retry separado del LLM retry
✓ Idempotency declarada per tool
✓ Headers cliente obligatorios (Retry-After, X-LLM-Provider, X-Error-Type)
✓ Alarmas críticas (auth, both_down, CB OPEN >5min)
✓ Audit cada retry + state change + fallback
✓ Respect allow_llm_fallback opt-out
```

---

## 7. Cobertura del Grafo Maestro

### Nodos servidos por Bloque 3 R3

```
NODO                                STATUS POST-B3 R3
────────────────────────────────────────────────────
Nodo 3 PFC (Orchestrator)          ✅ pleno (streaming + concurrency + resilience)
Nodo 6 Sistema Sensorial            🟡 foundation (streaming I/O)
Nodo 8 Tálamo                        🟡 foundation (concurrency awareness)
Nodo 11 Neuromoduladores            🟡 foundation (stress level = saturación)
```

### Pilares — Cobertura por B3 R3

```
Pilar 1 — Seguridad E2E
   ✅ Audit chain inmutable retry/fallback/circuit
   ✅ Idempotency tools preserve data integrity
   ✅ Workspace fairness anti-DoS interno
   ✅ Permission preservada en tool retry
   ✅ AUTH_FAILURE alarma crítica
   ✅ Audit transparente provider header

Pilar 2 — Escalabilidad por nodo
   ✅ Streaming reduce memoria servidor
   ✅ Token Bucket per workspace fairness
   ✅ Circuit breaker evita cascadas
   ✅ CapacityLimiter respeta Anthropic limits
   ✅ Failover OpenAI automático

Pilar 3 — Autonomía Generativa
   ✅ Agente decide qué error reintentar
   ✅ Tool retry separado del LLM loop
   ✅ Tools NO idempotentes respetadas
   ✅ Streaming permite cancel anticipado autónomo
```

### Anclas LOCKED — Verificación post-B3 R3

```
1.D Dedicated SaaS  ✅ tiers per workspace, fairness, opt-out fallback
2.B Open Core       ✅ sse_starlette MIT, asyncio stdlib, valkey-py MIT
3.D Equipo pequeño  ✅ todo en código vanilla Python sin DevOps
                     ✅ alarmas críticas a Brian directo Telegram
```

---

## 8. Costo total post-Bloque 3

```
COMPONENTE                                          COSTO USD/mes
─────────────────────────────────────────────────────────────────
SUBTOTAL R2 cerrado:                                ~$43/mes

R3 BLOQUE 1:
   Claude Sonnet 4.6 (principal):                   ~$50/mes
   OpenAI fallback LLM:                             ~$0.30/mes

R3 BLOQUE 2 (impacto neto caching):
   Caching maduro saving (-62%):                    ~-$31/mes
   Tool overhead (~20% calls):                      ~+$6/mes

R3 BLOQUE 3 (impacto neto resilience):
   Streaming SSE infra:                             $0
   Token Bucket infra:                              $0 (Valkey ya en stack)
   Resilience taxonomía:                            $0
   Reducción errors mal manejados:                  ~-$5-10/mes (estimado)
─────────────────────────────────────────────────────────────────
TOTAL v1 (R1+R2+R3 B1+B2+B3):                       ~$57-62/mes
```

### Verificación P2 <25% pilot revenue

```
Pilot Light USD 3,500 (3 semanas):
   Techo AI+infra: USD 875 (25%)
   Consumo v1 (3 sem): USD ~45
   → 5.1% del techo
   → MARGEN 94.9% para R3 B4 + R4-R10

Pilot Pro USD 8,000 (3 semanas):
   Techo: USD 2,000
   Consumo v1: USD ~45
   → 2.3% del techo
   → MARGEN 97.7%
```

### Verificación P5 cap LLM ($50-200/mes)

```
LLM TOTAL v1 con caching + token bucket:
   Pilot Light hard-capped: 10 RPM / 10K TPM
      Máximo teórico: ~$50/mes (exactamente cap inferior)
   Pilot Pro hard-capped: 50 RPM / 50K TPM
      Máximo teórico: ~$200/mes (cap superior)

Enforcement: AUTOMÁTICO per workspace
Margen: dentro cap por diseño (no por accidente)
```

---

## 9. Exploraciones futuras NO adoptadas v1

### 📚 Sub-tema 3.3.1 — Streaming alternativos

```
📚 Candidato A — NO streaming v1
   • Cuándo: NUNCA en producción
   • Solo para CLI tools/scripts batch

📚 Candidato C — WebSocket bidireccional
   • Cuándo: v3 si necesitamos input streaming desde cliente
   • Beneficio: cliente puede mandar data mid-conversation
   • Trigger: voice input / video streaming features
   • Costo: complejidad infra + Cloudflare Tunnel WS support

📚 Candidato D — Streaming Anthropic SDK directo
   • Cuándo: NUNCA (rompe abstraction layer B1)
   • Si reconsiderar: requiere unlock B1 3.1.1 LLMProvider

📚 Candidato E — Hybrid SSE + WebSocket opt-in
   • Cuándo: v2-v3 con features avanzadas
   • Beneficio: WS para clientes especiales, SSE default
   • Trigger: cliente enterprise pide WS

📚 Reconnect / Resume mid-stream
   • Cuándo: v2 con tráfico real que justifique
   • Beneficio: red mala no rompe UX
   • Implementación: Last-Event-ID header + cache de events
   • Foundation v1 ya preparada (Last-Event-ID param ignorado)

📚 Multiplexing streams (1 connection, N streams)
   • Cuándo: v3 con high concurrency desde mismo cliente
   • Beneficio: -50% overhead conexión

📚 Server push proactivo (notifications sin pull)
   • Cuándo: v3 con features Multi-Agent que generan eventos asíncronos
   • Beneficio: agente notifica al usuario sin que pregunte
```

### 📚 Sub-tema 3.3.2 — Concurrency alternativos

```
📚 Candidato A — Solo CapacityLimiter global
   • Cuándo: dev local solo Brian, MVP demo
   • NO para producción con múltiples workspaces

📚 Candidato C — Queue distribuida con priorities
   • Cuándo: v3 con >50 workspaces concurrentes
   • Beneficio: SLA tiers diferenciados
   • Trigger objetivo:
     - >50 workspaces activos
     - Necesidad priority queue
     - Tienes infra ops dedicada

📚 Candidato D — Rate limiter via proxy externo
   • Cuándo: v3 migración cloud K8s/Hetzner
   • Beneficio: cero código en app
   • Trigger: equipo SRE + migración cloud

📚 Candidato E — Backpressure adaptativo con métricas
   • Cuándo: v2 con R8 Observability LOCKED
   • Beneficio: auto-tuning sin manual intervention
   • Algoritmo: AIMD (Additive Increase, Multiplicative Decrease)
   • Trigger objetivo:
     - R8 cierra observability
     - >3 meses operación con baseline B
     - Métricas muestran subutilización

📚 Pricing-aware token bucket
   • Cuándo: v2 con pricing tiers maduros
   • Beneficio: tier upgrade automático según uso
   • Trigger: cliente sostenido al 90% bucket

📚 Per-tool token bucket separado
   • Cuándo: v3 si algunos tools son MUY costosos
   • Beneficio: prevenir runaway por tool específica
   • Ejemplo: tool MCP que llama API externa cara
```

### 📚 Sub-tema 3.3.3 — Resilience alternativos

```
📚 Candidato A — Solo retry simple
   • Cuándo: MVP demo, dev local
   • NO para producción

📚 Candidato C — Queue + Dead Letter Queue async
   • Cuándo: NUNCA para chat real-time
   • Sí para: email/notification/batch systems
   • Si For3s OS añade features async v3 → reconsiderar

📚 Candidato D — Solo cliente decide retry
   • Cuándo: NUNCA para For3s OS
   • Solo aplicable: library/SDK sofisticado

📚 Candidato E — Adaptive retry con ML predictivo
   • Cuándo: v3 con >1 año operación
   • Beneficio: óptimo retry strategy aprendido
   • Trigger objetivo:
     - Dataset histórico >100K errores clasificados
     - Performance B subóptima medida
     - ROI ML > complejidad mantención

📚 Bulkhead pattern (isolation por workspace)
   • Cuándo: v2-v3 si un workspace tira el sistema
   • Beneficio: workspace malicioso no afecta resto
   • Implementación: thread pool per workspace
   • Trigger: incident sostenido

📚 Hedging requests (mandar a 2 providers paralelo)
   • Cuándo: v3 enterprise con SLA estricto
   • Beneficio: latencia mejor (winner-takes-all)
   • Costo: 2x token cost (rechazar slow)

📚 Outbox pattern para idempotency
   • Cuándo: v2 con tools que llaman APIs externas
   • Beneficio: garantía at-least-once + dedupe
   • Implementación: tabla outbox + worker

📚 Saga pattern para tool sequences
   • Cuándo: v3 con workflows complejos multi-tool
   • Beneficio: compensaciones automáticas si falla mid-sequence
   • Ejemplo: send_email + write_memory → si segundo falla, deshacer email

📚 Chaos engineering automatizado
   • Cuándo: v3 con uptime >99.9% SLA
   • Beneficio: verificar resilience en producción
   • Tool: gremlin / litmus

📚 Self-healing automation
   • Cuándo: v3 con observability madura
   • Beneficio: auto-restart, auto-rollback, auto-scale
   • Trigger: alarmas resueltas automáticamente
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**

---

## 10. Implicaciones en Bloque 4 y rondas futuras

### Para Bloque 4 R3 — Observabilidad & Costo LLM (siguiente)

```
✅ Métricas obligatorias definidas (3.3.2 + 3.3.3 listas)
✅ Audit chain meta-audit completo
✅ Cost tracking foundation per workspace
✅ Token bucket = visibility per workspace nativa
✅ Circuit breaker = visibility provider health

3.4.1 LLM observability:
   → Métricas streaming (TTFT, throughput, partial)
   → Métricas concurrency (acquire wait, exceeded)
   → Métricas resilience (retry, fallback, circuit)
   → Aggregation per workspace

3.4.2 Cost monitoring per workspace:
   → P5 cap enforcement ya automático (3.3.2)
   → Alarmas 75% cap ($150/mes Pilot Pro)
   → Hard stop 100% cap ($200/mes)

3.4.3 LLM quality evaluation:
   → Eval framework
   → Golden datasets per dominio
   → A/B testing prompts (📚 v2)
```

### Para R4 — Tools / MCP Layer

```
✅ Tool retry separado del LLM retry (3.3.3)
✅ Idempotency metadata foundation
✅ Tool error types en taxonomía
✅ Streaming tool_use compatible (3.3.1)

R4 decidirá:
   • MCP client framework
   • Idempotency real por tool concreto
   • Tool authorization workflows
   • MCP server health monitoring
```

### Para R5 — Orchestration / Multi-Agent

```
✅ Streaming sub-agent invocation compatible
✅ Concurrency control hereda a sub-agents
✅ Circuit breaker scope: agent-level v1, sub-agent v2
✅ Resilience taxonomy reused para Nodo 9 Dual-Process

R5 decidirá:
   • Nodo 8 Tálamo (routing aware concurrency)
   • Nodo 9 Dual-Process Check (sistema 1 vs 2)
   • Multi-Agent Network lifecycle resilience
```

### Para R7 — Frontend / Channel

```
✅ Streaming SSE protocol LOCKED
✅ Eventos canónicos LOCKED
✅ Cancel API definida
✅ Heartbeat protocol
✅ Headers cliente estandarizados

R7 decidirá:
   • Frontend framework (Next.js, React, etc.)
   • EventSource API consumption
   • Reconnect strategy cliente
   • UX progress indicators
   • Telegram bot integration (Hermes-style)
```

### Para R8 — Observability

```
✅ Métricas obligatorias definidas (60+ entre B1+B2+B3)
✅ Audit chain inmutable
✅ Circuit breaker state observable
✅ Per-workspace metrics nativos

R8 decidirá:
   • Observability stack (Prometheus, Grafana, etc.)
   • Distributed tracing (OpenTelemetry)
   • Log aggregation
   • Dashboard layout
   • Alerting rules concretas
```

### Para R9 — Security / Compliance

```
✅ AUTH_FAILURE alarma crítica
✅ Workspace fairness anti-DoS interno
✅ Audit inmutable retries/fallbacks/circuit
✅ Idempotency tools preserve integrity

R9 decidirá:
   • Nodo 8 Amígdala (security checks)
   • Prompt injection detection
   • Rate limit refinement compliance
   • SOC2 / ISO27001 path
```

---

## 11. Riesgos legítimos aceptados

6 riesgos identificados conscientemente. Todos mitigables.

### Riesgo 1 — Cloudflare Tunnel buffer puede romper SSE

```
PROBLEMA:
   CF Tunnel puede bufferizar SSE, rompiendo "tiempo real".

IMPACTO v1:    MEDIO
IMPACTO v3:    BAJO (alternative transport si crece)

MITIGACIÓN:
   • sse_starlette con headers correctos
   • X-Accel-Buffering: no
   • Tests reales antes prod
   • Fallback a long-polling si CF rompe
```

### Riesgo 2 — Valkey down → fallback degraded

```
PROBLEMA:
   Token Bucket vive en Valkey. Si Valkey down → sin Capa 2.

IMPACTO v1:    BAJO (Valkey local muy estable)
IMPACTO v3:    MEDIO (más críticidad)

MITIGACIÓN:
   • Fallback automático a solo CapacityLimiter
   • Alarma Brian Telegram
   • Log warning per request
   • Valkey persistence + backup (R2 B3)
```

### Riesgo 3 — Token estimation mal calibrada

```
PROBLEMA:
   Heurística chars/3.5 × 1.1 puede sobre/sub-estimar.
   Workspace gasta más o menos de su bucket que real.

IMPACTO v1:    BAJO (margin 10% acepta error)
IMPACTO v3:    BAJO (refund post-call corrige)

MITIGACIÓN:
   • Refund/charge post-call con números reales
   • Ajustar heurística v2 con datos reales
   • Anthropic count_tokens endpoint opcional (cost extra)
```

### Riesgo 4 — Taxonomía error incompleta

```
PROBLEMA:
   Anthropic agrega nuevo error code → no clasificado.

IMPACTO v1:    BAJO (default NETWORK_TRANSIENT razonable)
IMPACTO v3:    MEDIO (más errores edge case)

MITIGACIÓN:
   • Default fallback NETWORK_TRANSIENT + log warning
   • Revisar ERROR_MAP mensualmente vs provider changelogs
   • Audit unknown error types
   • PR template requiere update mapping si nuevo type
```

### Riesgo 5 — Circuit breaker oscilante

```
PROBLEMA:
   State CLOSED ↔ OPEN ↔ CLOSED rápido por threshold mal calibrado.

IMPACTO v1:    BAJO (parámetros conservadores)
IMPACTO v3:    MEDIO (más tráfico amplifica)

MITIGACIÓN:
   • HALF_OPEN requires success consecutive
   • Threshold y window calibrables per provider
   • Alarma si state changes >10/hora
   • Audit detallado para tunear post-launch
```

### Riesgo 6 — Auth failure alarma fatiga

```
PROBLEMA:
   Si Anthropic rota keys o Brian las cambia, alarma 401 dispara.

IMPACTO v1:    BAJO (Brian = único user)
IMPACTO v3:    MEDIO (más usuarios, más alarmas)

MITIGACIÓN:
   • Distinguir 401 "expired" vs "invalid"
   • Auto-rotate si Brian configura key fallback (v2)
   • Cooldown alarmas (1/hora max)
   • Dashboard auth health (R8)
```

---

## Cierre del Bloque 3 R3

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ R3 BLOQUE 3 — STREAMING & PERFORMANCE CERRADO             ║
║                                                                ║
║   3/3 sub-temas LOCKED                                         ║
║   Score: 9.5/10 (excelente)                                     ║
║   Riesgos legítimos: 6 identificados, todos mitigables          ║
║   Spillover ejecutado:                                          ║
║      ✅ D-014 logged + master R3 updated + Estado §3.1.duodecies║
║      ⏳ Diferido: docs públicos for3s-inter/ hasta cierre R3   ║
║                                                                ║
║   Costo incremental B3 R3: ~$0 infra + -10-15% LLM costs        ║
║   Costo total v1: ~USD 57-62/mes (5.1% techo Pilot Light)       ║
║   UX percepción: 3-10x mejor por streaming                      ║
║   Cap P5 LLM: enforcement AUTOMÁTICO per workspace               ║
║   Resiliencia: 95% reducción Anthropic 429s                      ║
║                                                                ║
║   Próximo: R3 Bloque 4 — Observabilidad & Costo (3 sub-temas)  ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```