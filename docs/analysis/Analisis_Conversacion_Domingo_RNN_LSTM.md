# 🔬 Análisis — Conversación del domingo (RNN/LSTM) + auditoría de procesos

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Analisis_Conversacion_Domingo_RNN_LSTM.md → docs/analysis/Analisis_Conversacion_Domingo_RNN_LSTM.md (2026-07-30, ADR-029)

## Purpose

🔬 Análisis — Conversación del domingo (RNN/LSTM) + auditoría de procesos


> **Qué es:** análisis de la conversación real Brian ↔ @For3s_Brian_bot del domingo 12-jul sobre
> deep learning RNN/LSTM, MÁS la auditoría de si los procesos detrás están conectados y funcionando.
> Pedido por Brian 2026-07-13 ("siento que hay bugs o están mal conectados"). **Verificado en el
> código real del server** (no especulación). Relacionado: [[Aprendizajes_De_Campo_Post_Incubathon]].

---

## 1 · Qué pasó en la conversación (resumen)

Brian le preguntó a For3s por RNN/LSTM. Secuencia de procesos que se dispararon:
1. "Sé experto en RNN/LSTM" → **activó una skill** (`seleccion-de-arquitectura-rnnlstm...`). ✅
2. "Analiza tu estructura de for3s OS" → **lanzó el EQUIPO multi-agente** (5 especialistas, 63s,
   ~6,946 tokens). Resultado: los 5 dijeron **"for3s OS no está definido"** e imaginaron un OS de
   kernel (hablan de "kernel panic", "scheduler", "memory allocator"). 🔴
3. "Cómo integrar RNN/LSTM" → equipo otra vez (78s, ~8,061 tokens). Mismo bloqueo + riesgos genéricos.
4. "En qué lo podemos ocupar en for3s" → For3s **respondió SOLO** (sin equipo) y dio un análisis
   EXCELENTE y contextualizado ("agente con memoria, skills, grafo, sandbox, multi-instancia") con 4
   casos de uso reales + riesgos + candados anti-alucinación. ✅

**El contraste es la pista:** el For3s SOLO sabe quién es; el EQUIPO no.

---

## 2 · 🔴 BUG CONFIRMADO — El equipo multi-agente NO hereda la identidad ni la memoria de For3s

**Severidad: ALTA.** El equipo se lanza "en frío": cada especialista solo recibe su rol genérico +
la pregunta cruda del usuario. NO recibe qué es For3s, ni su memoria, ni su grafo. Por eso los 5
especialistas no supieron qué es "for3s OS" y especularon con un kernel.

**Evidencia en el código (server `~/for3s-os`, verificado 2026-07-13):**
- `telegram_channel.py:1442` → `multiagente.correr_equipo(texto, ...)` — pasa solo `texto` (mensaje crudo).
- `multiagente.py:206` → `correr_specialist(definicion, tarea, ...)` — pasa rol + tarea, nada más.
- `specialists.py:252` → `prompt = f"[{definicion.rol}]\n\n{entrada}"` — **SIN identidad, SIN memoria.**
- `specialists.py` **NO importa** `identidad` (el módulo que ensambla quién es For3s).
- El **sintetizador** (`multiagente.py:323 sintetizar`) tampoco recibe identidad.

**La cadena completa (ningún eslabón inyecta contexto de For3s):**
```
Usuario → correr_equipo(texto) → correr_specialist(rol, tarea) → prompt = [rol] + pregunta
```

**Impacto real:**
- El equipo da respuestas GENÉRICAS y descontextualizadas cuando la pregunta es sobre el propio For3s
  (o sobre algo que vive en su memoria). Desperdicia tokens en análisis inútil (~15K tokens en 2
  corridas que concluyeron "no sé qué es for3s").
- Cuando la pregunta NO depende de la identidad (ej. "compara dos librerías") el equipo funciona bien
  — por eso no siempre se nota. El bug se manifiesta cuando la tarea requiere saber qué es For3s.

**Fix (a diseñar, no urgente-crítico pero importante):** inyectar en el prompt de cada especialista
(y del sintetizador) un bloque mínimo de identidad de For3s (qué es el sistema) + opcionalmente el
contexto de memoria relevante a la tarea. Reusar el ensamblador de `identidad.py`. Cuidar el costo
(no meter TODA la identidad a los 5 — un resumen). **Va a la lista de bugs/pendientes.**

---

## 3 · Sobre el análisis de RNN/LSTM que dio For3s (calidad del contenido)

El For3s SOLO (paso 4) dio un análisis **técnicamente correcto y honesto**, coincide con nuestro
propio veredicto ([[Aprendizajes_De_Campo_Post_Incubathon]] §3):
- Los 4 casos donde SÍ tendría sentido (memoria predictiva, detección de anomalías, routing, predicción
  de skill) — todos de **bajo riesgo, en background, modo sugerencia**.
- Lo que NO tocar (core de memoria, grafo, auditoría inmutable). ✅ correcto.
- Reconoció el riesgo de **alucinación de LSTM** (predicción con alta confianza pero equivocada) y
  propuso 5 candados (umbral de confianza, modo sugerencia, monitoreo de drift, detector OOD,
  auditoría). Análisis maduro.
- **Coincide con nuestro veredicto:** RNN/LSTM clásico NO es el camino; lo valioso es "aprender de
  tus datos" (ver §4), no meter un LSTM. For3s mismo lo dijo bien.

---

## 4 · 🔵 LÍNEA FUTURA (documentada, NO construir hoy) — Modelo que aprende qué memoria es valiosa

Brian: *"SÍ me importa esto — un modelo que aprenda de tus datos qué episodios resultan valiosos."*

**La idea (bien dirigida, a diferencia de LSTM):** hoy el "scoring" de importancia de la memoria
(qué guardar/consolidar/olvidar) son **reglas/heurísticas** (microglía, decay, relevancia). En el
futuro se podría entrenar un **mini-clasificador** que aprenda de los datos reales de For3s qué
episodios resultaron valiosos (se re-consultaron, llevaron a acción útil, el usuario los confirmó).

- **NO es un LSTM.** Es un clasificador simple sobre features del episodio (frecuencia de uso,
  recencia, si se re-consultó, feedback del usuario, centralidad en el grafo).
- **Input que YA existe:** cada episodio + su historia de uso. Falta capturar la **señal de "valioso"**
  (thumbs up/down, si se reusó, si llevó a algo).
- **Requisito:** miles de episodios reales con señal. Hoy sería sobre-ingeniería (los datos aún son
  jóvenes). **Cuándo:** cuando haya volumen real de uso (varios usuarios/meses).
- **Riesgo:** bajo si es solo para *rankear* memoria (si rankea mal, trae contexto menos útil, no
  rompe nada). Igual que dijo For3s: modo sugerencia + umbral + nunca en el path crítico sin supervisión.

**Estado:** 🔵 línea futura registrada. No se construye hoy (frentes uno por uno). Encaja con el
Frente D (valor de retorno) — un mejor scoring de memoria = mejor contexto = más valor devuelto.

---

## 5 · Conclusión de la auditoría (respuesta directa a Brian)

**¿Los procesos están conectados y funcionando al 100%?** Casi — con 1 bug real:
- ✅ **Skills** — se activan bien (la skill de RNN/LSTM se seleccionó correcta).
- ✅ **For3s solo (chat + memoria)** — funciona y sabe quién es.
- ✅ **Equipo multi-agente** — se lanza, corre en paralelo, sintetiza, reporta tokens/cupo. La
  mecánica funciona.
- 🔴 **PERO el equipo NO hereda la identidad/memoria de For3s** → da respuestas descontextualizadas
  cuando la tarea es sobre el propio sistema. **Tu instinto era correcto: hay algo mal conectado.**

**Acción:** el bug del equipo va a la lista de pendientes/bugs para diseñar el fix (inyectar identidad
+ contexto a los specialists). El modelito de memoria queda como línea futura (§4).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `docs/analysis/Analisis_Conversacion_Domingo_RNN_LSTM.md`).
