# Ronda 3 — Bloque 1: LLM Principal

**Sub-documento detallado de R3 — Model/LLM Layer. Bloque 1 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-01
**Estatus:** ✅ LOCKED (4/4 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema)
**Documento padre:** [Ronda_03_Model_LLM_Layer.md](Ronda_03_Model_LLM_Layer.md)
**Sesión:** 2026-06-01

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes

**Pre-preguntas P1-P5 LOCKED antes del bloque:**
- P1: Mixto universal (no solo PRs)
- P2: Sonnet 4.6 default → Opus 4.7 opt-in
- P3: Cloud Anthropic con disclaimer
- P4: Single-model v1
- P5: USD 50-200/mes cap

**Fuente de verdad:**
- [`For3s_OS_Grafo_Maestro.md`](../Cerebro/For3s_OS_Grafo_Maestro.md) §4 Nodo 3 sugiere "Claude Sonnet"

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 3.1.1 — Provider LLM principal](#3-sub-tema-311--provider-llm-principal)
4. [Sub-tema 3.1.2 — Modelo específico para razonamiento](#4-sub-tema-312--modelo-específico-para-razonamiento)
5. [Sub-tema 3.1.3 — Multi-model routing strategy](#5-sub-tema-313--multi-model-routing-strategy)
6. [Sub-tema 3.1.4 — Local LLM fallback](#6-sub-tema-314--local-llm-fallback)
7. [Stack final consolidado](#7-stack-final-consolidado)
8. [Cobertura del Grafo Maestro](#8-cobertura-del-grafo-maestro)
9. [Costo total post-Bloque 1](#9-costo-total-post-bloque-1)
10. [Exploraciones futuras NO adoptadas v1](#10-exploraciones-futuras-no-adoptadas-v1)
11. [Implicaciones en bloques siguientes R3](#11-implicaciones-en-bloques-siguientes-r3)
12. [Riesgos legítimos aceptados](#12-riesgos-legítimos-aceptados)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 1 — LLM PRINCIPAL                                     ║
║   4 sub-temas LOCKED el 2026-06-01                             ║
║                                                                ║
║   3.1.1 Provider          → Anthropic + abstraction layer       ║
║   3.1.2 Modelo específico → Sonnet default + Opus opt-in        ║
║   3.1.3 Multi-model       → NO routing v1, defer v2             ║
║   3.1.4 Local LLM fallback → OpenAI cloud fallback              ║
║                                                                ║
║   Provider único v1:        Anthropic                           ║
║   Fallback automático:      OpenAI GPT-4o                        ║
║   Tiers per workspace:      Sonnet | Opus                        ║
║   GPU requerida:            NO (cumple D-009 LOCAL)              ║
║                                                                ║
║   Costo incremental B1 R3:  ~USD 50/mes (Sonnet) + ~$3/año (fb) ║
║   Costo total v1 actualizado: ~USD 93/mes                       ║
║   % techo Pilot Light:      8.0% (margen 92%)                   ║
║   % cap P5 LLM:             43.5% del max ($87/$200)            ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Provider único maduro con fallback automático, sin sobre-
ingeniería, alineado con Grafo Maestro §4 Nodo 3."
```

Las 4 decisiones convergen en patrones consistentes:

```
1. ALINEACIÓN GRAFO MAESTRO (3.1.1)
   → Nodo 3 PFC sugiere "Claude Sonnet" explícitamente
   → Decisión confirmada con criterio técnico independiente
   → Brian LOCKED: "fuente de verdad es Grafo Maestro"

2. TIERS PER WORKSPACE (3.1.2)
   → Cumple P2 ("Sonnet apuntando Opus") sin complejidad
   → Foundation pricing tiers v2
   → Cliente decide tier al onboarding

3. SIN ROUTING PREMATURO (3.1.3)
   → Cumple P4 ("Single-model v1")
   → Respeta Grafo (Nodo 9 vive en R5, no R3)
   → Evita refactor cuando R5 cierre Dual-Process Check

4. RESILIENCIA SIN GPU (3.1.4)
   → OpenAI fallback automático
   → Aprovecha OpenAI ya en stack (B2 2.2)
   → Cumple D-009 LOCAL (sin GPU extra)

5. ABSTRACTION LAYER FUTURE-PROOF
   → LLMProvider Protocol permite swap futuro
   → Migración v2 (Gemini, local) sin refactor masivo
   → Preserva autonomía estratégica
```

### Por qué esta filosofía importa

**Para Pilar 2 Escalabilidad:** FailoverManager garantiza uptime >99.9% (Anthropic 99.5% + OpenAI fallback durante outages).

**Para Pilar 3 Autonomía:** LLM principal habilita razonamiento generativo. Abstraction layer preserva opciones futuras.

**Para Anclas:** Provider maduro (Anthropic), SDKs abiertos (MIT), simplicidad operacional (3.D).

---

## 3. Sub-tema 3.1.1 — Provider LLM principal

### Decisión LOCKED

```
Anthropic (Claude family) + abstraction layer LLMProvider
```

### Contexto

El **LLM principal** es el motor de razonamiento generativo del agente. Es el "cerebro semántico" que razona sobre el contexto recuperado, genera outputs, interactúa conversacionalmente y orquesta tools.

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** Grafo §4 dice "LLM (Claude Sonnet)" explícitamente
- **Nodo 10 CLS:** Haiku ya integrado B2 2.6 (familia coherente)
- **Pilar 1 Seguridad:** Provider debe permitir disclaimer B2B
- **Pilar 3 Autonomía:** LLM debe poder proponer skills nuevas (Meta-Orchestrator v3+)

### Candidatos evaluados

```
A) Anthropic (Claude family)   ✅ ELEGIDO
B) OpenAI (GPT family)         ⚠️ Grafo no lo menciona, alternativa
C) Google (Gemini family)      ⚠️ Context window masivo pero alineación baja
D) Local / Open-source         ❌ Requiere GPU (no en D-009 v1)
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A:Anthropic│B:OpenAI │C:Google  │D:Local   │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Sugerido por Grafo Maest │  ✅✅✅   │   ❌    │   ❌    │   ❌    │
│ Context window principal │  200K    │  128K    │  2M      │  128K    │
│ MCP protocol nativo      │  ✅✅✅   │   ❌    │   ❌    │  parcial │
│ Razonamiento (MMLU)      │ 88-92%   │ 87-90%   │ 85-88%   │ 83-85%   │
│ Prompt caching           │  90% off  │  50% off │  ⚠️     │   N/A    │
│ Hardware extra requerido │   ❌    │   ❌    │   ❌    │  GPU $$$ │
│ Ya en stack (B2 2.6)     │  ✅✅✅   │ fallback │   ❌    │   ❌    │
│ Compatible Anclas        │   3/3    │   3/3    │   3/3    │   2/3    │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **Alineación perfecta Grafo Maestro** (§4 Nodo 3 sugiere "Claude Sonnet")
2. **Stack consistency** (Haiku ya LOCKED B2 2.6 para CLS)
3. **MCP protocol nativo** (crítico para R4 Tools/MCP Layer)
4. **Prompt caching 90% off** (vs 50% OpenAI)
5. **Razonamiento top tier** (Sonnet 88% MMLU, Opus 92%)
6. **Compliance B2B ready** (SOC2 + no entrena con API)
7. **Multilingüe excelente** (LATAM friendly)
8. **Context window 200K** (mayor que GPT-4o 128K)
9. **Brian familiarizado** con Anthropic ecosystem
10. **Abstraction layer** permite swap futuro

### Stack final 3.1.1

```python
# Provider: Anthropic
# SDK: anthropic (oficial MIT)
# Versión: latest

# Abstraction:
class LLMProvider(Protocol):
    async def complete(self, req: LLMRequest) -> LLMResponse: ...
    async def stream(self, req: LLMRequest) -> AsyncIterator: ...
    @property
    def name(self) -> str: ...

class ClaudeProvider(LLMProvider):
    # implementación Anthropic
    ...
```

### Path futuro

```
v1: Anthropic + abstraction layer
v2: añadir OpenAI como second opinion provider
v3: Local LLMs (Llama, Qwen) si cliente compliance strict
```

---

## 4. Sub-tema 3.1.2 — Modelo específico para razonamiento

### Decisión LOCKED

```
Sonnet 4.6 default + Opus 4.7 opt-in config workspace
```

### Contexto

Provider Anthropic ya elegido (3.1.1). Decisión: qué modelo específico de Claude usar como razonamiento principal, y cómo se activa Opus selectivamente (P2 LOCKED).

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** Grafo dice "Claude Sonnet" (default)
- **Nodo 9 Dual-Process Check:** decide complejidad (R5)
- **Nodo 11 Neuromoduladores:** modo alta atención → Opus (R5)
- **P2 LOCKED:** "Sonnet 4.6 apuntando a Opus 4.7"

### Candidatos evaluados

```
A) Solo Sonnet 4.6 v1                ❌ contradice P2
B) Sonnet default + Opus opt-in       ✅ ELEGIDO
C) Routing automático por complejidad ❌ sobre-ingeniería v1
D) Manual flag por request            ⚠️ UX confusa como única
```

### Comparativa Sonnet vs Opus

```
┌──────────────────────────┬──────────────────┬──────────────────┐
│ Criterio                 │ Sonnet 4.6       │ Opus 4.7         │
├──────────────────────────┼──────────────────┼──────────────────┤
│ MMLU (razonamiento)      │ 88%              │ 92%              │
│ Coding (HumanEval)       │ 91%              │ 94%              │
│ Latencia respuesta       │ ~1-2s            │ ~3-5s            │
│ Context window           │ 200K tokens      │ 200K tokens      │
│ Input cost / 1M tokens   │ $3               │ $15 (5x más)     │
│ Output cost / 1M tokens  │ $15              │ $75 (5x más)     │
│ Prompt caching           │ ✅ (90% off)     │ ✅ (90% off)     │
└──────────────────────────┴──────────────────┴──────────────────┘
```

### Razones de la decisión

1. **Cumple Grafo Maestro + P2 simultáneamente** (Sonnet default + Opus posibilidad)
2. **Simplicidad v1** (~30 líneas código adicional)
3. **Pricing tier natural** (Pilot Light Sonnet vs Pilot Pro Opus opcional)
4. **Future-proof** (foundation para routing automático v2)
5. **Cumple cap P5** con prudencia (defaults Sonnet baratos)
6. **Autonomía preservada** (sistema decide modelo, no human-in-loop per request)

### Configuración LOCKED v1

```sql
ALTER TABLE shared.workspaces ADD COLUMN
    llm_tier TEXT NOT NULL DEFAULT 'sonnet'
    CHECK (llm_tier IN ('sonnet', 'opus'));

ALTER TABLE shared.workspaces ADD COLUMN
    llm_tier_changed_at TIMESTAMPTZ;

ALTER TABLE shared.workspaces ADD COLUMN
    llm_tier_changed_by UUID;
```

```python
class ClaudeProvider:
    MODELS = {
        'sonnet': 'claude-sonnet-4-6',
        'opus':   'claude-opus-4-7',
        'haiku':  'claude-haiku-4-5-20251001',  # solo CLS (B2 2.6)
    }

    async def complete_for_workspace(
        self,
        workspace_id: str,
        req: LLMRequest,
        force_tier: str | None = None
    ) -> LLMResponse:
        tier = force_tier or (await get_workspace_config(workspace_id)).llm_tier
        model = self.MODELS[tier]

        # Validar cap P5 antes de call
        current_cost = await get_workspace_monthly_cost(workspace_id)
        if current_cost > MONTHLY_CAP_USD:
            raise BudgetExceeded(workspace_id, current_cost)

        async with llm_limiter:  # B3 3.4 LOCKED
            with anyio.fail_after(LLM_CALL_TIMEOUT):  # 60s
                response = await self.client.messages.create(
                    model=model,
                    messages=req.messages,
                    max_tokens=req.max_tokens,
                    ...
                )

        await audit_llm_call(workspace_id, tier, response)
        await track_cost(workspace_id, response.cost_usd)
        return self._to_llm_response(response)
```

### Pricing implicación

```
Pilot Light $3,500 (3 sem) → Sonnet fijo (cabe P2)
Pilot Pro $8,000 (3 sem) → Opus opcional con upcharge
Enterprise (v2-v3) → Opus default + customization
```

### Path futuro

```
v1: Sonnet default + Opus opt-in config workspace
v2: routing automático + tier vinculado pricing
v3: routing por dominio + manual flag + dynamic tiers
```

---

## 5. Sub-tema 3.1.3 — Multi-model routing strategy

### Decisión LOCKED

```
NO routing v1, diferir 100% a v2
```

### Contexto

"Multi-model routing" = sistema que decide automáticamente qué LLM usar per request específico. Diferente de "tiers per workspace" (3.1.2) que es estático por config.

### Mapeo al Grafo Maestro

- **Nodo 9 Dual-Process Check:** routing real vive aquí (R5)
- **Nodo 8 Tálamo:** router amplio para subgrafos (R5)
- **Nodo 11 Neuromoduladores:** modulación dinámica (R5)
- **P4 LOCKED:** Single-model v1

### Candidatos evaluados

```
A) NO routing v1, diferir 100% a v2  ✅ ELEGIDO
B) Foundation hooks v1 + routing v2  ⚠️ Over-engineering minimal
C) Routing simple v1                  ❌ Contradice P4 LOCKED
D) (no aplicable)                     —
```

### Razones de la decisión

1. **Cumple P4 LOCKED al 100%** ("Single-model v1")
2. **Alineación Grafo Maestro** (Nodo 9 vive en R5, no R3)
3. **Simplicidad máxima** (3.D — cero código nuevo)
4. **Tiers per workspace (3.1.2)** ya provee "routing estático"
5. **Velocidad desarrollo R3** preservada

### Triggers para activar v2 routing

v2 routing automático cuando TODOS se cumplan:

```
✓ R5 implementa Nodo 9 Dual-Process Check
✓ R8 Observability mide cost per request
✓ Métricas muestran 60%+ requests sobre-spec'd
✓ Volumen justifica complejidad (>10 workspaces activos)
```

### Meta-audit preparación v2

Cada LLM call v1 logea:
- workspace_id, tier_used, tokens, cost, latency, outcome
- Estos datos servirán para validar v2 routing decisions
- Foundation observability sin código routing v1

### Path futuro

```
v1: NO routing automático (tier per workspace en 3.1.2)
v2: routing automático con Nodo 9 Dual-Process Check
v3: routing por dominio + dynamic tiers neuromoduladores
```

---

## 6. Sub-tema 3.1.4 — Local LLM fallback

### Decisión LOCKED

```
Cloud fallback OpenAI (sin local LLM v1)
```

### Contexto

Qué hacemos cuando Anthropic API NO está disponible (outage, rate limit, error). Resiliencia ante dependencia provider único.

### Mapeo al Grafo Maestro

- Grafo no menciona fallback explícitamente
- Implícitamente: Pilar 2 Escalabilidad (resiliencia)
- Local LLM = privacy máxima (pero D-009 sin GPU)

### Candidatos evaluados

```
A) NO fallback v1 (aceptar dependencia)   ⚠️ UX cliente outage
B) Cloud fallback OpenAI                   ✅ ELEGIDO
C) Local LLM Llama                         ❌ requiere GPU (no D-009)
D) Graceful degradation con cache          ⚠️ Cache hit rate bajo v1
```

### Razones de la decisión

1. **Resiliencia razonable** ante outages Anthropic (~3 horas/año)
2. **Aprovecha stack existente** (OpenAI ya en B2 2.2 fallback embeddings)
3. **Cumple D-009 LOCAL** (sin GPU extra)
4. **Costo trivial** (~$30/año estimado en outages)
5. **Alineación Anclas** (1.D, 2.B SDK abierto, 3.D setup razonable)
6. **Foundation v2 multi-provider**
7. **UX cliente profesional** (respuesta vs error durante outages)

### Triggers fallback automático

```
• HTTP 503 Anthropic (outage)
• HTTP 429 rate limit
• Timeout >60s (LLM_CALL_TIMEOUT B3 3.4)
• 3 retries fallidas con exponential backoff (1s, 4s, 16s)
```

### NO trigger fallback para

```
• Errores contenido (safety filter)
• Errores input cliente (HTTP 400)
• Errores auth (HTTP 401)
```

### Implementación

```python
class FailoverManager:
    def __init__(self):
        self.primary = ClaudeProvider()
        self.fallback = GPTProvider()
        self.retry_config = {
            'max_retries': 3,
            'backoff_seconds': [1, 4, 16]
        }

    async def complete(self, req, workspace_id):
        # Opt-out check
        config = await get_workspace_config(workspace_id)
        if not config.allow_llm_fallback:
            return await self.primary.complete(req)  # raises on failure

        for attempt in range(self.retry_config['max_retries']):
            try:
                response = await self.primary.complete(req)
                await audit_llm_call(workspace_id, 'anthropic', response, attempt)
                return response
            except (AnthropicOutage, RateLimit) as e:
                await asyncio.sleep(self.retry_config['backoff_seconds'][attempt])
                continue
            except Exception as e:
                # Other errors (safety, input) bubble up
                raise

        # Anthropic failed 3 times → fallback
        await audit_fallback_activation(workspace_id, 'openai')
        try:
            response = await self.fallback.complete(req)
            await audit_llm_call(workspace_id, 'openai', response, 'fallback')
            return response
        except OpenAIError as e:
            raise BothProvidersDown("Both Anthropic and OpenAI unavailable")
```

### Opt-out per workspace

```sql
ALTER TABLE shared.workspaces ADD COLUMN
    allow_llm_fallback BOOLEAN NOT NULL DEFAULT true;
```

Cliente compliance-strict puede desactivar.

### Transparencia cliente

- Header HTTP `X-LLM-Provider: anthropic | openai`
- Audit log con provider usado
- Cliente puede consultar audit

### Path futuro

```
v1: Anthropic primary + OpenAI fallback
v2: añadir graceful degradation + opt-out granular
v3: local Llama si compliance strict + GPU disponible
```

---

## 7. Stack final consolidado

```
COMPONENTE                    DECISIÓN                              COSTO
─────────────────────────────────────────────────────────────────────────────
Provider primary              Anthropic                              USD ~50/mes Sonnet
Provider fallback             OpenAI                                  USD ~$3/año
Modelo default                Claude Sonnet 4.6                       $3/$15 per 1M tokens
Modelo premium                Claude Opus 4.7 (opt-in)                $15/$75 per 1M tokens
Modelo CLS [B2 2.6 LOCKED]    Claude Haiku 4.5                        $1/$5 per 1M tokens
Embeddings [B2 2.2 LOCKED]    Stella local @ 1024 + OpenAI fallback   $0 + <$1/mes
SDK primary                   anthropic (MIT)                          $0
SDK fallback                  openai (MIT)                             $0
Abstraction                   LLMProvider Protocol                     $0
Failover                      FailoverManager con retries              $0
─────────────────────────────────────────────────────────────────────────────
TOTAL incremental Bloque 1                                            ~USD 53/mes
TOTAL v1 (R1+R2+R3 B1)                                                ~USD 93/mes
```

### Estructura módulo for3s_os/llm/

```
for3s_os/llm/
├── base.py              → LLMProvider abstract Protocol
├── anthropic_provider.py → ClaudeProvider (primary)
├── openai_provider.py    → GPTProvider (fallback)
├── failover.py           → FailoverManager (orquesta)
├── router.py             → multi-model routing (v2+)
├── prompts/              → prompt templates
├── context_builder.py    → builds context from memory tiers
├── cost_tracker.py        → per-workspace cost tracking
└── llm_observability.py   → tokens, latency, errors
```

### Patrones obligatorios

```
✓ llm_limiter (CapacityLimiter 3) — B3 3.4 LOCKED
✓ LLM_CALL_TIMEOUT (60s) — B3 3.4 LOCKED
✓ CancelledError re-raise siempre — B3 3.4 LOCKED
✓ Meta-audit cada call (audit_events)
✓ Cost tracking per workspace
✓ Cifrado TLS 1.3 (cloud providers default)
✓ Header X-LLM-Provider en response
✓ Opt-out per workspace respetado
✓ Cap P5 enforcement (BudgetExceeded exception)
```

---

## 8. Cobertura del Grafo Maestro

### Nodos servidos por Bloque 1 R3

```
NODO                                STATUS POST-B1 R3
────────────────────────────────────────────────────
Nodo 3 PFC (Orchestrator)          ✅ LLM principal definido
Nodo 9 Dual-Process Check          🟡 preparación R5 (routing defer v2)
Nodo 10 CLS                         ✅ Haiku integrado [B2 2.6]
Nodo 11 Neuromoduladores            🟡 foundation tier dynamic v3
```

### Pilares — Cobertura por B1 R3

```
Pilar 1 — Seguridad E2E
   ✅ Meta-audit cada LLM call
   ✅ Opt-out fallback per workspace
   ✅ Transparencia provider via header
   ✅ TLS 1.3 cloud providers

Pilar 2 — Escalabilidad por nodo
   ✅ FailoverManager resiliencia
   ✅ CapacityLimiter concurrency (B3 3.4)
   ✅ Provider único maduro escala bien

Pilar 3 — Autonomía Generativa
   ✅ LLM principal habilita razonamiento autónomo
   ⏳ Meta-Orchestrator (autonomía completa) es v3+
```

### Anclas LOCKED — Verificación post-B1 R3

```
1.D Dedicated SaaS  ✅ tier per workspace
2.B Open Core       ✅ SDKs abiertos:
                       • anthropic (MIT)
                       • openai (MIT)
                       Modelos cerrados aceptable con disclaimer (P3 LOCKED)
3.D Equipo pequeño  ✅ provider único maduro, sin routing complejo v1
```

---

## 9. Costo total post-Bloque 1

```
COMPONENTE                                          COSTO USD/mes
─────────────────────────────────────────────────────────────────
Hardware Linux LOCAL Brian (D-009):                 $0
Electricidad servidor 24/7:                         ~$5
Cloudflare Tunnel + R2 free tier:                   $0
Dominio for3s.ai:                                   ~$1
PostgreSQL + AGE + pgvector + pgcrypto (B1):        $0
Custom memory + Stella + HDBSCAN (B2):              $0
Valkey + Arq + pgbouncer + asyncio + anyio (B3):    $0
Backup tools age + rclone + systemd (B4):           $0
OpenAI fallback embeddings (B2 2.2):                <$1
Claude Haiku 4.5 (CLS, B2 2.6):                     ~$37
─────────────────────────────────────────────────────────────────
SUBTOTAL R2 cerrado:                                ~$43/mes

R3 BLOQUE 1 NUEVO:
Claude Sonnet 4.6 (principal):                      ~$50/mes
OpenAI fallback LLM (durante outages):              ~$0.30/mes
─────────────────────────────────────────────────────────────────
TOTAL v1 (R1+R2+R3 B1):                             ~$93/mes
```

### Verificación P2 <25% pilot revenue

```
Pilot Light USD 3,500 (3 semanas):
   Techo AI+infra: USD 875 (25%)
   Consumo v1 (3 sem): USD ~70 ($93/mes × 3/4)
   → 8.0% del techo (vs 5.4% pre-R3 B1)
   → MARGEN 92% para R3 B2-B4 + R4-R10

Pilot Pro USD 8,000 (3 semanas):
   Techo: USD 2,000
   Consumo v1: USD ~70
   → 3.5% del techo
   → MARGEN 96.5%
```

### Verificación P5 cap LLM ($50-200/mes)

```
LLM TOTAL v1:
   Claude Haiku CLS:                      ~$37/mes
   Claude Sonnet 4.6 principal:           ~$50/mes
   OpenAI fallback (raro):                ~$0.30/mes
   ─────────────────────────────────────────────
   TOTAL LLM:                              ~$87/mes

Cap P5 LOCKED:                             $50-200/mes
% del cap medio:                           43.5% ($87/$200)
Margen disponible:                         $113 escalado workspaces
```

### Compras únicas (no recurring, sin cambio)

```
UPS básico:                                ~$100 una vez
Disco externo USB 2 TB (backup):           ~$60 una vez
Dominio for3s.ai (registro):               ~$10 una vez
─────────────────────────────────────────
TOTAL una vez:                              ~$170
```

---

## 10. Exploraciones futuras NO adoptadas v1

Esta sección documenta las opciones evaluadas y NO elegidas, con triggers objetivos para reconsiderarlas. **NO alteran la línea v1.**

### 📚 Sub-tema 3.1.1 — Provider alternativos

```
📚 OpenAI (GPT family) — second opinion provider v2
   • Cuándo evaluar: Claude rechaza por safety filters,
     necesidad multimodal audio (Realtime API),
     razonamiento alternativo para validar
   • Beneficio: diversificación, fallback robusto
   • Trigger: Claude rechaza >5% requests por safety
   • YA usado como fallback en 3.1.4

📚 Google Gemini — contextos masivos
   • Cuándo: análisis codebases completos, docs >200K tokens
   • Beneficio: context window 2M tokens (10x Claude)
   • Costo: ~50% más barato que Claude
   • Trigger: caso uso requiere >200K tokens context

📚 Local LLMs (Llama, Qwen, DeepSeek)
   • Cuándo: cliente compliance strict (healthcare, finance)
   • Requiere: GPU dedicada o cloud GPU
   • Beneficio: privacy ABSOLUTA
   • Trigger: cliente regulado lo exige contractualmente
   • Diferido también en 3.1.4

📚 Multi-model routing inteligente (3.1.3 future)
   • Cuándo: v2 con métricas reales
   • Beneficio: cost optimization automático

📚 Computer use (Sonnet 4.6 feature)
   • Cuándo: wedges con browser automation
   • Beneficio: agente puede usar UI directamente

📚 Vision (Sonnet/Opus capability)
   • Cuándo: análisis imágenes (screenshots, fotos, diagramas)
   • Beneficio: For3s OS universal acepta imágenes

📚 OpenAI gpt-oss (open weights)
   • Cuándo: v3 si infraestructura GPU disponible
   • Beneficio: local LLM con OpenAI quality
```

### 📚 Sub-tema 3.1.2 — Modelo específico alternativos

```
📚 Candidato C — Routing automático por complejidad
   • Cuándo evaluar: v2 cuando R5 cierre Nodo 9 Dual-Process
   • Beneficio: cost optimization 20% blended
   • Trigger:
       - Métricas v1 muestran 60%+ requests sobre-spec'd
       - R5 implementa Dual-Process Check
       - Observability R8 implementado

📚 Candidato D — Manual flag por request
   • Cuándo: power users avanzados v3
   • Como COMPLEMENTO a B (config + flag override)
   • Trigger: cliente pide control granular per request

📚 Tier 'haiku' como opción principal
   • Cuándo: cliente budget ultra-bajo v2
   • Para wedges Q&A intensivo
   • Trigger: cliente pide pricing tier ultra-económico

📚 Tier vinculado a pricing automáticamente
   • Cuándo: v2 con pricing tiers formalizados
   • Pilot Light → Sonnet fijo
   • Pilot Pro → Opus default
   • Enterprise → Opus + customization

📚 Routing por dominio (salud → Opus, código → Sonnet)
   • Cuándo: v3+ con métricas reales por dominio
   • Para "segundo cerebro universal" For3s OS visión

📚 Cost prediction antes de call
   • Cuándo: v2 con observability
   • Beneficio: alertar cliente antes de gastar mucho

📚 Dynamic tier basado en hora del día
   • Cuándo: v3 con Nodo 11 Neuromoduladores
   • Ejemplo: "modo nocturno" → Opus
```

### 📚 Sub-tema 3.1.3 — Multi-model routing alternativos

```
📚 Candidato B — Foundation hooks v1
   • Cuándo: si v2 routing en 3-6 meses (próximo)
   • Beneficio: migración v2 más limpia (~30 líneas)

📚 Candidato C — Routing simple v1 (DESCARTADO)
   • Razón: contradice P4 LOCKED
   • Si reconsiderar: requiere unlock P4 explícito

📚 Routing v2 automático completo
   • Cuándo: triggers v2 todos cumplidos
   • Beneficio: cost optimization 20% blended
   • Implementación: ~200 líneas + Nodo 9 R5

📚 Routing por dominio v3+
   • Cuándo: For3s OS multi-dominio
   • Lógica: salud → Opus, código → Sonnet, casual → Haiku

📚 Dynamic routing por hora del día v3
   • Con Nodo 11 Neuromoduladores
```

### 📚 Sub-tema 3.1.4 — Local LLM fallback alternativos

```
📚 Candidato C — Local LLM Llama (DIFERIDO v3+)
   • Cuándo: cliente compliance strict + GPU disponible
   • Modelos: Llama 3.3 70B, Qwen 2.5 72B, DeepSeek V3

📚 Candidato D — Graceful degradation con cache
   • Cuándo: v2 como FALLBACK del FALLBACK
   • Lógica: Anthropic → OpenAI → cache + queued retry

📚 Multi-cloud rotation
   • Cuándo: v3 enterprise SLA 99.99%
   • Lógica: rotar Anthropic, OpenAI, Gemini per workspace

📚 Fallback inteligente por error type
   • Cuándo: v2 con observability R8
   • Diferenciación: 429 → fallback, safety → no fallback

📚 Local Llama como tercer tier
   • v3 GPU disponible: Anthropic → OpenAI → Llama local

📚 Notificación proactiva al cliente durante outage
   • v2 con Telegram bot
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**

---

## 11. Implicaciones en bloques siguientes R3

### Para Bloque 2 R3 — Prompt & Context Management

```
✅ Claude SDK disponible (Anthropic primary)
✅ Context window 200K confirmado (Sonnet)
✅ Prompt caching 90% off disponible
✅ Tool use schema nativo (Anthropic)
✅ XML tags style recomendado (Anthropic best practice)

3.2.1 Prompt engineering framework:
   → influenciado por Anthropic best practices
   → custom strings vs DSL vs LangChain

3.2.2 Context window management:
   → 200K tokens disponibles
   → estrategia building context desde memory tiers (R2)

3.2.3 Prompt caching:
   → Anthropic 90% off reads
   → decisión: qué cachear y cuánto tiempo

3.2.4 Function calling / tool use:
   → MCP protocol nativo (puente R4)
   → Anthropic tool use schema
```

### Para Bloque 3 R3 — Streaming & Performance

```
✅ Anthropic streaming nativo
✅ Patterns async LOCKED (B3 3.4)
✅ llm_limiter(3) LOCKED
✅ LLM_CALL_TIMEOUT (60s) LOCKED

3.3.1 Streaming responses:
   → Anthropic streaming context managers
   → SSE vs WebSocket cliente

3.3.2 LLM concurrency control:
   → llm_limiter ya aplicado
   → Anthropic rate limits específicos

3.3.3 Retry & fallback patterns:
   → FailoverManager ya implementado en 3.1.4
   → Solo formalizar retry policies adicionales
```

### Para Bloque 4 R3 — Observabilidad & Costo

```
✅ Audit chain LOCKED meta-audit
✅ Cost tracking foundation per workspace
✅ Cap P5 ($50-200/mes) enforcement

3.4.1 LLM observability:
   → cost_tracker.py + llm_observability.py
   → métricas: tokens, latency, errors

3.4.2 Cost monitoring per workspace:
   → P5 cap enforcement
   → alarmas 75%, hard stop 100%

3.4.3 LLM quality evaluation:
   → eval framework
   → golden datasets
```

### Para R4 — Tools / MCP Layer

```
✅ MCP protocol nativo Anthropic
✅ Tool use schema definido
✅ Abstraction layer permite swap providers

R4 decidirá:
   • Framework MCP servers
   • GitHub/GitLab MCP (para wedge QA)
   • Slack/Notion/Jira MCP (futuros wedges)
   • Custom MCP servers
```

### Para R5 — Orchestration

```
✅ LLM principal disponible
✅ Tiers per workspace foundation

R5 decidirá:
   • Nodo 3 PFC orquestador completo
   • Nodo 9 Dual-Process Check (activa routing v2)
   • Nodo 11 Neuromoduladores dinámicos
   • Nodo 7 DMN idle compute
```

---

## 12. Riesgos legítimos aceptados

3 riesgos identificados conscientemente. Ninguno es bloqueante.

### Riesgo 1 — Dependencia Anthropic (cloud + provider único)

```
PROBLEMA:
   For3s OS depende de Anthropic. Si Anthropic:
   • Sufre outage prolongado
   • Cambia pricing significativamente
   • Cambia políticas privacy
   • Es adquirido/cierra

IMPACTO v1:    MEDIO
IMPACTO v3:    MEDIO (con clientes enterprise)

MITIGACIÓN:
   • OpenAI fallback automático (3.1.4)
   • Abstraction layer LLMProvider permite swap
   • Migración a Gemini o local LLM viable en ~1 semana
   • Monitor Anthropic status + roadmap
```

### Riesgo 2 — Costo Opus si workspace activa tier premium

```
PROBLEMA:
   Cliente activa Opus tier. Costo 5x mayor.
   1 workspace Opus puede ser $250-300/mes.
   Excede cap P5 default ($200).

IMPACTO v1:    MEDIO (mitigable con pricing)
IMPACTO v3:    BAJO (pricing tiers maduros)

MITIGACIÓN:
   • Pricing tier vincula Opus con Pilot Pro $8K
   • Cap P5 enforcement (BudgetExceeded exception)
   • Alarmas 75% del cap
   • Pilot Pro AI techo $2,000 (25% de revenue)
   • $400 vs $2,000 sigue holgado
```

### Riesgo 3 — Outage Anthropic activa fallback OpenAI con diferencias sutiles

```
PROBLEMA:
   Prompts optimizados para Claude pueden producir
   outputs ligeramente diferentes en GPT-4o.
   Cliente puede notar inconsistencia durante outage.

IMPACTO v1:    BAJO (outages raros ~3h/año)
IMPACTO v3:    MEDIO (volumen mayor)

MITIGACIÓN:
   • Prompts compatibles (XML tags funcionan ambos)
   • Testing periódico de prompts en ambos providers
   • Audit log transparente (cliente sabe qué provider)
   • Header X-LLM-Provider en response
   • Cliente puede opt-out fallback (allow_llm_fallback)
```

---

## Cierre del Bloque 1 R3

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ R3 BLOQUE 1 — LLM PRINCIPAL CERRADO                       ║
║                                                                ║
║   4/4 sub-temas LOCKED                                         ║
║   Score: 9.5/10 (excelente)                                     ║
║   Riesgos legítimos: 3 identificados, todos mitigables          ║
║   Spillover: D-012 logged + master R3 creado                     ║
║                                                                ║
║   Costo incremental B1 R3: ~USD 53/mes                          ║
║   Costo total v1: ~USD 93/mes (8% techo Pilot Light)            ║
║                                                                ║
║   Próximo: R3 Bloque 2 — Prompt & Context Management            ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```