# H10 — PLANEA (metacognición: "sé cuándo NO sé") — Plan Maestro a Detalle

> **Qué es:** plan de obra de H10-PLANEA, debatido y LOCKED con Brian (2026-06-26),
> ANTES de codear. For3s evalúa su PROPIA confianza antes de responder: si es alta,
> responde normal; si es baja, en vez de inventar lo DICE / pide aclaración / marca su
> respuesta como tentativa. Es la metacognición — lo que refuerza la honestidad que
> Brian valora ("que no invente").
>
> ⚠️ NOMBRE: en el mapa de construcción este hito es "H10 PLANEA". Las etiquetas
> H10/H11/H12 ya se usaron para el ciclo APRENDE (skills) → aquí se le dice
> **H10-PLANEA** para no confundir. Numéricamente es PFC + confidence del R6.
>
> **Diseño LOCKED base:** `Ronda_06_Bloque_1_PFC_Orchestrator.md` (8 señales, 5 niveles,
> check loop) + `Ronda_06_Pre_Code_Review_Detailed.md`. Este doc ATERRIZA ese diseño a la
> realidad ACTUAL de For3s (audit, tools, sin golden set, equipo solo a veces).
>
> NO es código — es el orden de construcción. Se ejecuta por fases, debatir→código→testeo.

---

## 0. Decisiones LOCKED (Brian 2026-06-26, debate cerrado)

| Decisión | Elección |
|---|---|
| Señales de confianza | **Las 4 con infra REAL** (peso real) + las 4 sin infra como **contribución neutra declarada** (honesto, mismo criterio que H9). NO inventar datos. |
| Acción en BAJA confianza | **Lo DICE / pide aclaración / marca tentativo** (honestidad). NO re-planear aún (eso es deuda). |
| Dónde aplica v1 | **`conversation.send`** (la respuesta de chat principal). Después: tool-loop, equipo. |

**Principio:** el valor de v1 es el COMPORTAMIENTO "sé cuándo no sé", no el motor PFC
completo (plan-then-execute formal). Lo barato y demostrable primero.

---

## 1. Las 8 señales (R6 §6.1.2) — cuáles tienen infra HOY

| # | Señal | Peso (R6) | ¿Infra hoy? | Fuente real |
|---|-------|-----------|-------------|-------------|
| 1 | llm_self_report | 1.0 | ✅ SÍ | el modelo declara su confianza (se le pide) |
| 2 | tool_success | 2.0 | ✅ SÍ | ¿las tools del turno funcionaron? (tool_loop) |
| 3 | schema_valid | 2.5 | ✅ SÍ | ¿la salida estructurada parseó bien? |
| 7 | historical | 2.5 | ✅ SÍ (parcial) | audit_events: confianza/errores recientes |
| 4 | cost_accuracy | 1.5 | ⚠️ neutra | no medimos estimado vs real por turno aún |
| 5 | plan_consistency | 2.0 | ⚠️ neutra | no hay plan-then-execute formal (deuda) |
| 6 | multi_agent_consensus | 3.0 | ⚠️ neutra | solo aplica cuando corre el equipo (H8), no en chat |
| 8 | rule_eval | 3.0 | ⚠️ neutra | requiere golden set formal (= deuda H9-D3) |

**Neutra = contribución honesta:** no suma ni resta señal falsa; se documenta que está
pendiente de infra. Cuando exista, se llena sin tocar el resto.

## 2. Niveles (R6 §6.1.2)
```
HIGH        0.90+     → responde normal
MED_HIGH    0.70-0.89 → responde normal
MEDIUM      0.50-0.69 → responde + nota leve si aplica
LOW         0.30-0.49 → marca TENTATIVO / ofrece verificar
CRITICAL    <0.30     → lo dice claro: "no estoy seguro, aclárame X" (no inventa)
```

## 3. Plan de construcción por FASES

### H10-PLANEA-a — Módulo `confidence.py` (el cálculo)
- `ConfidenceScore` + `ConfidenceLevel` (5 niveles, umbrales R6).
- Señales como funciones puras: cada una devuelve (valor 0-1, peso, disponible).
  Las 4 reales calculan de verdad; las 4 neutras devuelven disponible=False.
- `agregar(señales)` → score ponderado SOLO sobre las disponibles (no diluir con neutras).
- DEFENSIVO: si algo falla, devuelve MEDIUM (no bloquea el turno).
- Audit: `confidence_calculated` (reusa audit chain).

### H10-PLANEA-b — Integración en `conversation.send`
- Tras generar la respuesta (o antes de enviarla), calcular el confidence del turno con
  las señales del contexto (tool_success del tool-loop, schema_valid si hubo, historical).
- Para llm_self_report: pedir al modelo —de forma barata— que marque su confianza, o
  inferirla de su propio fraseo. (v1: una señal ligera, sin 2ª llamada cara.)
- Si nivel LOW/CRITICAL → inyectar al contexto/respuesta una NOTA de honestidad
  ("marca esto como tentativo / pide aclaración"), reforzando FOR3S_ROLE.
- DEFENSIVO: el confidence NUNCA rompe la respuesta; si falla, responde normal.

### H10-PLANEA-c — Test + verificación
- Test: señales reales calculan, neutras no diluyen, niveles correctos, agregación.
- Verificación en vivo: pregunta ambigua/desconocida → el bot marca incertidumbre en vez
  de inventar; pregunta clara → responde con seguridad normal.

---

## 4. Lo que NO entra en v1 (deuda consciente → irá a PENDIENTES)

- **Plan-then-execute formal** (PFCPlan, steps, checkpoints) — el motor PFC completo (R6
  §6.1.1). v1 mide confianza del turno, no descompone en plan multi-step.
- **Check loop con RE_PLAN_PARTIAL** (re-planear automático) — v1 solo avisa/pide aclaración.
- Señales 4/5/6/8 reales (cost_accuracy, plan_consistency, multi_agent_consensus, rule_eval).
- Confidence en tool-loop GitHub y en el equipo (v1 = solo chat).
- Workspace controls (human_in_loop_on_critical, max_re_plans) del R6 §5.4.3.

---

## 5. Mapa de archivos

- **NUEVO `confidence.py`** — el scoring (señales + niveles + agregación). Separado, como
  governor.py / dmn.py.
- **conversation.py** — integración en send (calcular + inyectar nota si baja confianza).
- **agent.py (FOR3S_ROLE)** — reforzar: ante confianza baja, ser honesto/tentativo.
- **version.py** — bump al cerrar.

> Refs: Ronda_06_Bloque_1_PFC_Orchestrator.md (8 señales, niveles, check loop) ·
> Ronda_06_Pre_Code_Review_Detailed.md · cruza con H9-D3 (golden set para rule_eval) y
> H8 (consensus para multi_agent). Es el Nodo PFC del cerebro (metacognición).

---

## ✅ H10-PLANEA CONSTRUIDO — CIERRE (2026-06-26)

COMPLETO v1 (3 fases). version.py **v0.12.0** (HITO "H10 PLANEA"), bot activo, suite 132/4.

- **H10-PLANEA-a ✅** `confidence.py`: `ConfidenceScore` + `ConfidenceLevel` (5 niveles R6) +
  8 señales (SIGNAL_WEIGHTS R6). REALES: llm_self_report (mide marcadores de duda en el
  texto, sin 2ª llamada LLM), tool_success, schema_valid, historical (tasa error 24h del
  audit). NEUTRAS honestas (no diluyen): cost_accuracy, plan_consistency,
  multi_agent_consensus, rule_eval. `agregar` pondera solo disponibles + ⭐ REGLA DE TOPE:
  si el modelo expresó duda (self_report<0.65), su duda es el techo del score (el histórico
  general no la tapa). `evaluar_respuesta_chat` helper + audit `confidence_calculated`.
- **H10-PLANEA-b ✅** integración en `conversation.send` (paso 3b): tras generar, evalúa el
  confidence; si CRITICAL y el texto NO fue ya honesto, antepone nota "_⚠️ no estoy del todo
  seguro, verifícalo_". + FOR3S_ROLE reforzado (sección METACOGNICIÓN "sé cuándo no sé").
  DEFENSIVO: nunca rompe el turno.
- **H10-PLANEA-c ✅** test 16/16 (niveles, señales, neutras-no-diluyen, ponderación, tope,
  evaluar_respuesta_chat real con BD). ⭐ Bug de calibración cazado y corregido: la respuesta
  insegura daba MED_HIGH porque el histórico (peso 2.5) tapaba al self_report (peso 1.0) →
  fix: regla de tope (self_report bajo = techo del score).

⚠️ **Calibración v1:** confidence sobre la respuesta de CHAT (send), acción = honestidad
(no re-planear). Deuda en PENDIENTES §"H10-PLANEA — PENDIENTES" (HP1-HP6).
