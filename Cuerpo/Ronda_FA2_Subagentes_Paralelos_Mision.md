# ⚡ MINI-RONDA — F-A2: sub-agentes en paralelo para /mision (bajar el tiempo REAL)

> **Estado: ✅ DECIDIDO por Brian 2026-07-16 — A (quick-win) HECHO + C (F-A2 completo) DIFERIDO hasta BYOK.**
>
> - **A · Quick-win HECHO** (commit pendiente): `CONCURRENCIA_MAX` del equipo ahora CONFIGURABLE por
>   ENV `FOR3S_EQUIPO_CONC_MAX` (default 2 = seguro para las compartidas). Las internas con cupo
>   holgado (Foresito/brian) lo suben en su `.env` para misiones más rápidas. Verificado: ENV=5→5,
>   sin ENV→2.
> - **C · F-A2 completo DIFERIDO:** el planner de sub-agentes rinde de verdad cuando el cupo deje de
>   ser el freno = con **BYOK** (cupo por cliente, ya en §EXTRAS). Queda como semilla del carril de
>   Confianza para reactivar entonces.
>
> Semilla del carril de Confianza (Frente E).
> **Origen:** medimos que el 99% del tiempo de `/mision` es el LLM (2 llamadas a sonnet/opus EN
> SERIE). El progreso en vivo alivió la PERCEPCIÓN; F-A2 buscaría bajar el tiempo de PARED REAL.

---

## 1 · El terreno REAL (investigado 2026-07-16 — honestidad antes de construir)

- **Ya existe un equipo multi-agente** (`multiagente.correr_equipo`): lanza specialists EN PARALELO
  con `asyncio.gather`, gobernado por `CONCURRENCIA_MAX=2` (solo 2 a la vez) + timeout 180s + un
  Synthesizer que junta los reportes. Reporta progreso (`on_progreso`).
- **PERO los specialists NO son sub-tareas de la misión** — son ROLES FIJOS (backend/frontend/etc.)
  que analizan la MISMA pregunta desde ángulos distintos (hub-and-spoke). Sirve para "analiza a
  fondo X", no para "parte esta tarea de código en pasos y hazlos en paralelo".
- **El cuello real:** `CONCURRENCIA_MAX=2` existe porque las 5 instancias comparten UNA suscripción
  Claude (1 cupo). Más paralelismo = más riesgo de 429. El paralelismo está TOPADO por el rate-limit
  de la cuenta, no por el código.

## 2 · El análisis honesto (¿F-A2 vale la pena HOY?)

**Lo que F-A2 daría:** una misión que se puede partir en N pasos independientes correría esos pasos
en paralelo → tiempo de pared ≈ el paso más lento, no la suma. Para una misión de 4 sub-tareas de
30s cada una: de 120s (serie) a ~30s (paralelo).

**Lo que lo limita HOY (los frenos reales):**
1. **La suscripción compartida (1 cupo, `CONCURRENCIA_MAX=2`):** correr 4 sub-agentes a la vez sube
   el riesgo de 429 → habría que serializar a 2, reduciendo la ganancia. El paralelismo real está
   capado por la cuenta, no por el diseño.
2. **No toda misión se parte bien:** "arregla este bug" es secuencial por naturaleza (entender →
   arreglar → verificar). El paralelismo ayuda a misiones tipo "analiza estos 5 módulos" o "prueba
   estos 4 casos" — un subconjunto.
3. **Complejidad nueva:** un planner que DIVIDA la misión en sub-tareas (con LLM) + las orqueste +
   sintetice los resultados en las 5 secciones. Es un motor nuevo, con sus propios modos de fallo
   (sub-tareas mal partidas, síntesis que pierde contexto).

## 3 · Opciones (Brian decide)

- **A · Quick-win SIN F-A2 (recomendado como primer paso):** subir `CONCURRENCIA_MAX` **solo cuando
  la instancia es la interna con cupo holgado**, y/o bajar `max_tokens` del carril cuando la misión
  es simple. Cambio de 1-2 líneas, cero motor nuevo. Ataca el freno #1 sin el riesgo del planner.
- **B · F-A2 completo (motor de sub-agentes):** planner que parte la misión → orquesta en paralelo
  (gobernado por el cupo) → sintetiza. Es una Ronda propia (F1 planner, F2 orquestación, F3 síntesis,
  F4 verificación). Ganancia real en misiones partibles, pero complejo y capado por la suscripción.
- **C · Diferir F-A2:** el progreso en vivo ya quitó la sensación de "colgado"; el tiempo real solo
  molesta en misiones largas, que son pocas. Dejar F-A2 anotado hasta que /mision se use mucho o
  haya cupo dedicado (cuando los clientes traigan su propia key = BYOK, el cupo deja de ser el freno).

## 4 · Recomendación honesta

**F-A2 completo (B) NO es el mejor uso del tiempo HOY** porque su ganancia está capada por la
suscripción compartida (el freno real es el cupo, no el código). **Recomiendo A o C:** un quick-win
de configuración (A) da algo de mejora sin motor nuevo, o diferir (C) hasta que BYOK quite el freno
del cupo — entonces F-A2 rinde de verdad. Construir el planner completo ahora sería sobre-ingeniería
que choca con el rate-limit de la cuenta.

**Decisión de Brian:** ¿A (quick-win config), B (F-A2 completo pese al cupo), o C (diferir hasta BYOK)?

---

Relacionado: `Doc/Carril_Mejora_Continua_Confianza.md` (F-A2 = semilla) · `project_h8_equipo_avance`
(el equipo multi-agente) · §EXTRAS BYOK (el cupo por cliente que quitaría el freno) ·
[[feedback_explicar_antes_de_implementar]].
