# H9 — SUEÑA (DMN: trabaja solo en idle) — Plan Maestro a Detalle

> **Qué es este doc:** el plan de obra de H9, debatido y LOCKED con Brian (2026-06-25),
> ANTES de escribir código. For3s, cuando nadie lo usa, trabaja en background: se
> mantiene, detecta patrones, pre-computa. Es el DMN ("modo por defecto del cerebro",
> Nodo 6). Junto con las Skills (Nodo 4, H10-12) forma el Pilar 3 (autonomía generativa),
> ambos gobernados por el MISMO governor (H11).
>
> **Fuente de verdad del diseño:** `Ronda_05_Bloque_4_DMN_Default_Mode.md` +
> `Ronda_05_DMN_Tasks_Detailed.md` (los 8 trigger_fn/action_fn + ROI + auto-improvement).
> Este doc ATERRIZA ese diseño a la realidad ACTUAL de For3s (BD v20, worker Arq, governor
> H11 ya construido, CLS de H6, embeddings BGE-M3, cache Valkey).
>
> ⚠️ NO es código — es el orden de construcción. Se ejecuta por fases, debatir→código→
> testeo cada una, igual que H10-12. Documentación primero (regla de Brian 2026-06-25).

---

## 0. Decisiones LOCKED (Brian 2026-06-25, debate cerrado)

| Decisión | Elección |
|---|---|
| Alcance | **Las 8 tasks completas** (5 housekeeping + 3 generativas) |
| Disparo | **IDLE REAL** (tras N min sin actividad) + las ligeras también en idle de DÍA |
| memory_consolidation | **REUSA el CLS de H6** (no reimplementar — una sola lógica de consolidación) |
| Generativas | **Pasan por el GOVERNOR (H11) + gate al dueño** (misma maquinaria que skills) |
| Verificación | **Dejar idle + comprobar en BD/logs** que corrió y dejó su outcome |
| Orden interno | **H9-a motor → H9-b housekeeping → H9-c generativas → H9-d ROI** (freno antes que motor) |

**Regla de oro (heredada de H10-12):** las tasks GENERATIVAS (se auto-mejoran) NUNCA
auto-aplican en v1 → governor + gate + audit. Las HOUSEKEEPING (se mantienen) auto-aplican
porque su outcome es directo y medible (si degrada, eval_regression lo caza).

---

## 1. Lo que se REUSA (no construir de cero — ~50% ya existe)

| Pieza del DMN | Infra existente de For3s | Archivo |
|---|---|---|
| Ejecución en background | **Worker Arq + cron** (H6) | tasks.py / WorkerSettings |
| memory_consolidation | **CLS** (H6, ya consolida episodios→grafo) | consolidator.py / job_cls |
| Gobierno de las generativas | **Governor H11** (scanner+kill switch+gate) | governor.py |
| Gate al dueño | **H8 gate** (botones ✅/❌, on_skill_gate de H12) | telegram_channel.py |
| embeddings | **BGE-M3** (ya precarga, ya embebe en background) | embeddings.py / memory.py |
| cache | **Valkey** (cache.py, TTL por tool, hit/miss) | cache.py |
| audit inmutable | **audit chain** (KEK) | audit.py |
| idle/actividad | **created_at en episodes_events** (último turno = última actividad) | memory.py |

⚠️ Lo que NO existe y hay que construir: **idle detection** (cuánto lleva sin uso),
**scheduler oportunista de día**, **ROI tracker per task**, y las **7 tasks** que aún no
están (solo memory_consolidation existe vía CLS).

---

## 2. Las 8 tasks — clasificación LOCKED (R5 §2)

```
🟢 HOUSEKEEPING (5) — "se mantiene solo", bajo riesgo, AUTO-APLICA, sin review:
   • embedding_precompute    (LOW   · $0)      → embebe lo pendiente
   • cache_prewarming        (LOW   · $0.15)   → calienta patrones frecuentes que fallan
   • memory_consolidation    (MEDIUM· $0.10)   → REUSA CLS de H6 (episodios→grafo)
   • routing_learning        (LOW   · $0.05)   → enriquece histórico de routing (no decide)
   • eval_regression_detect  (MEDIUM· $0.05)   → GUARDIÁN: detecta si la calidad degrada

🔴 GENERATIVAS (3) — "se mejora solo", alto riesgo, GOVERNOR + GATE obligatorio:
   • pattern_detection       (MEDIUM· $0.05)   → detecta patrones → propone skill (a H12)
   • hypothesis_generation   (HIGH  · $0.50 Opus) → hipótesis ("este módulo tiende a romper")
   • prompt_improvement      (HIGH  · $0.20)   → propone mejoras a prompts → gate dueño
```

Cada task: `trigger_fn` (¿vale correr ahora?) → `action_fn` (hace el trabajo) →
`outcome_metric` (qué produjo, medible). Detalle fiel en R5 §3-4.

---

## 3. Plan de construcción por FASES (orden LOCKED)

### H9-a — MOTOR DMN (el esqueleto, bajo riesgo)
**Meta:** que exista el "modo idle" + dónde se registra qué corrió. Sin tasks aún.
- **Idle detection:** `ultima_actividad(ws)` = max(created_at) de episodes_events. "Idle"
  = sin turnos en ≥ N min (config, ej. FOR3S_DMN_IDLE_MIN=15). Reusa la columna existente.
- **Scheduler:** dos vías (decisión LOCKED "ambos"): (1) corre tasks LIGERAS ($0) cuando
  detecta idle de DÍA; (2) corre TODAS de noche (ya hay cron). El worker Arq las dispara.
- **Migración:** tabla `dmn_corridas` (task, ws, trigger_ok, outcome JSONB, costo, ms,
  creado_at) — el registro de cada corrida, base del ROI (H9-d) y de la verificación.
- **Estado/kill switch:** flag `FOR3S_DMN_OFF` + (opcional) estado en BD, como el governor.
  Default: DMN housekeeping ON, generativas OFF hasta calibrar (conservador).
- **Audit:** evento `dmn_task_run` por corrida.
- **Demo:** dejar idle → en log aparece "DMN despertó (idle 15m)", aunque aún no haga tasks.

### H9-b — 5 HOUSEKEEPING (seguras, auto-aplican)
**Meta:** el sistema se mantiene solo. Outcome medible directo, sin review.
- `embedding_precompute` — embebe items pendientes (episodios/skills sin embedding). $0,
  idempotente, cero riesgo. trigger: hay pendientes.
- `cache_prewarming` — pre-computa respuestas a patrones frecuentes con baja hit-rate.
  trigger: hit_rate<0.5 + ≥3 misses recurrentes. Reusa cache.py + stats.
- `memory_consolidation` — **invoca el CLS de H6** (consolidator.py / lógica de job_cls).
  trigger: ≥20 episodios sin consolidar. NO reimplementa: una sola lógica.
- `routing_learning` — enriquece el histórico de routing (no cambia decisiones). ⚠️ hoy
  For3s no tiene router multi-modelo activo (H7 enrutamiento BLOQUEADO) → esta task puede
  quedar como STUB/no-op honesto hasta que exista routing real. (Anotar, no forzar.)
- `eval_regression_detection` — GUARDIÁN: corre un golden set vs baseline, alerta si la
  calidad cae. ⚠️ For3s aún no tiene framework de eval/golden set formal → v1 puede ser
  una métrica simple (ej. tasa de errores/429, longitud media) o quedar como cimiento.
- **Demo:** idle → embeddings pendientes pasan a 0, cache se calienta, métrica registrada.

### H9-c — 3 GENERATIVAS (con el freno puesto, alto cuidado)
**Meta:** el sistema se mejora solo — PERO nada se aplica sin governor + gate.
- `pattern_detection` — detecta patrones repetidos en el uso → propone una SKILL → la manda
  al flujo H12 (proponer_skill_auto → governor → gate). ⭐ Conexión directa con lo construido.
- `hypothesis_generation` — genera hipótesis ("este módulo tiende a romper"); usa Opus ($).
  → review queue / aviso al dueño (NO auto-actúa).
- `prompt_improvement` — propone mejoras a prompts del sistema → gate al dueño (NUNCA
  auto-edita FOR3S_ROLE; cruza con el pendiente AUTO-CONCIENCIA AC3).
- **Todas:** trigger conservador + governor.can_generate (kill switch) + gate. Audit.
- **Demo:** dejar idle con historial rico → propone 1 patrón/hipótesis → llega al dueño
  con botones; sin aprobar, no pasa nada.

### H9-d — ROI TRACKING (cada task se gana su lugar)
**Meta:** ninguna task gasta sin aportar. (R5 §6)
- Por task: `outcome_metric` + `valor_medible` vs `costo` → ratio. Si valor < costo →
  sugiere disable. Sobre la tabla `dmn_corridas`.
- Reporte: comando `/dmn status` (estado idle + últimas corridas + ROI por task) — como
  `/autogen status`. Solo dueño.
- **Demo:** tras unos días, `/dmn status` muestra qué tasks aportan y cuáles sobran.

---

## 4. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| DMN corre y gasta sin aportar | ROI tracker (H9-d) + kill switch + generativas OFF por defecto |
| Generativa propone algo dañino | Governor H11 (scanner) + gate al dueño + audit (igual que skills) |
| Solapamiento con CLS de H6 | memory_consolidation REUSA el CLS (decisión LOCKED) |
| Idle mal detectado (corre mientras se usa) | umbral N min sobre created_at real + lock global (como equipo) |
| hypothesis_generation cara (Opus) | trigger conservador + tope diario + ROI la apaga si no confirma |
| routing/eval sin infra real aún | v1 honesto: stub/no-op documentado hasta que exista routing/eval |

---

## 5. Lo que NO entra en H9 v1 (deuda consciente)

- Router multi-modelo real para routing_learning (H7 enrutamiento sigue BLOQUEADO).
- Framework de eval/golden set formal para eval_regression (hoy no existe → métrica simple).
- Auto-aplicar prompt_improvement sin gate (eso es AUTO-CONCIENCIA AC3, pendiente aparte).
- Interaction graph completo entre tasks (R5 §7) — v1 corre tasks independientes.

---

## 6. Mapa de archivos (dónde vivirá H9)

- **NUEVO `dmn.py`** — motor: idle detection, scheduler, las 8 tasks (trigger/action),
  registro de corridas. (Separado, como skills.py/governor.py/aprende.py.)
- **migración 021** — tabla `dmn_corridas` (+ estado/kill switch si va a BD).
- **tasks.py** — job(s) Arq del DMN: nocturno (todas) + chequeo de idle de día (ligeras).
- **telegram_channel.py** — comando `/dmn status` (+ `/dmn on|off` opcional).
- **governor.py / aprende.py** — las generativas se enchufan aquí (reuso, no duplicar).
- **version.py** — bump al cerrar H9.

> Refs: Ronda_05_Bloque_4_DMN_Default_Mode.md · Ronda_05_DMN_Tasks_Detailed.md (los 8
> action_fn + ROI + auto-improvement loop §5) · Ronda_06 §A (governor que las gobierna) ·
> H10_H11_H12_APRENDE_Referencia_Tecnica.md (la otra mitad del Pilar 3, ya construida).

---

## ✅ H9 CONSTRUIDO — CIERRE (2026-06-26)

H9 COMPLETO en 4 fases (debatir→código→testeo cada una). BD v22, version.py **v0.11.0**
(HITO "H9 SUEÑA"), bot+worker activos, suite 132 passed/4 skipped.

- **H9-a ✅ Motor DMN** (`dmn.py` + migración 021): idle detection real (`minutos_idle`
  reusa created_at) · `correr_ciclo` (gating por clase + por tarea pesada/día, defensivo:
  una task que explota no tumba el resto) · `dmn_estado` (kill switch por clase: housekeeping
  ON / generativas OFF default) · `dmn_corridas` (registro append-only) · 2 jobs Arq
  (`job_dmn_noche` 04:00 todas + `job_dmn_idle` cada 30 min, solo si idle, ligeras) · comando
  `/dmn`. Test 13/13.
- **H9-b ✅ 5 Housekeeping** (`dmn_tasks.py`): REALES = embedding_precompute ($0, embebió 17
  reales) · memory_consolidation (REUSA el CLS de H6, no reimplementa) · eval_regression
  (v1 métrica simple: % respuestas vacías 24h). STUBS HONESTOS (no fingen) = cache_prewarming
  (sin stats hit/miss aún) · routing_learning (sin router multi-modelo, H7 bloqueado). Test 18/18.
- **H9-c ✅ 3 Generativas** (+ migración 022 `dmn_propuestas`): pattern_detection REUSA
  `proponer_skill_auto` de H12 (governor + stale + gate) · hypothesis_generation REAL con Opus
  (1×/día → deja propuesta en `dmn_propuestas`, NO auto-actúa) · prompt_improvement STUB
  honesto (cruza con AUTO-CONCIENCIA AC3). Triple freno: `generativas_on` (default OFF) +
  solo_noche + governor. El worker no notifica por Telegram: deja propuestas en BD → `/dmn
  propuestas` con botones ✅/❌ (`on_dmn_propuesta`). Test 17/17.
- **H9-d ✅ ROI tracking**: `roi_por_task` (sobre dmn_corridas, ventana 30d) → keep / revisar
  (gastó sin producir) / sin-datos. `/dmn roi`. Test 7/7.

⚠️ **Estado seguro:** housekeeping ON (se mantiene solo, bajo riesgo), generativas OFF
(no se mejora solo hasta que el dueño haga `/dmn generativas on`). El cron nocturno completo:
01:00 backup · 02:00 CLS · 02:30 STATUS · 03:00 Microglía · 03:30 curar_skills · 04:00 DMN
+ DMN idle cada 30 min de día.

**Deuda consciente (documentada en §5):** cache stats reales · router para routing_learning ·
golden set formal para eval_regression · prompt_improvement = AUTO-CONCIENCIA AC3 (pendiente).
