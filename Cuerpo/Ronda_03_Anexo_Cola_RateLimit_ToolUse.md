# Anexo R3 — Cola anti-rate-limit para tool-use (For3s → Claude)

> **Tipo:** documento de diseño de implementación (anexo de R3, LLM layer).
> **Estado:** PROPUESTA — pendiente aprobación de Brian antes de programar.
> **Fecha:** 2026-06-14.
> **Origen:** Brian, probando el bot, topa rate-limit constantemente al hacer
> consultas GitHub seguidas (tool-use). Pidió un sistema de cola/seccionado
> para no saturar el rate-limit de Claude.

---

## 0. El problema (verificado)

Al hacer varias consultas GitHub seguidas, For3s topa el rate-limit de Claude:
`429 rate_limit_error` con `message:"Error"`, sin `retry-after`. El cupo de 5h
puede estar al 41% y aun así topar — es el límite **por-minuto** (ITPM, input
tokens per minute) el que se satura, NO la cuota semanal.

**Por qué el tool-use lo agrava (investigación 2026 + nuestro audit):**
- Los **schemas de las tools cuentan como input tokens** (4 tools ≈ 6-10k chars).
- El **loop hace 3-5 llamadas SEGUIDAS** (una por vuelta tool→result→tool).
- Cada llamada reenvía el historial + los schemas → ráfaga de ITPM alto.
- → El token bucket por-minuto de Anthropic se agota en segundos.

**Hallazgos clave de la investigación (confirman el rumbo):**
- NO existe "refrescar" el rate-limit manualmente. Es un **token bucket** que
  se repone solo con el tiempo (ventana deslizante). → La solución es ESPACIAR.
- Los headers traen `anthropic-ratelimit-*-remaining` y `*-reset-at` → se puede
  auto-regular leyéndolos (saber cuánto falta antes de topar).
- **prompt caching reduce 75-90% del ITPM** de contenido repetido (schemas de
  tools + system) → arma poderosa.
- Message Batches API NO sirve (solo API key de pago, no OAuth de suscripción).

---

## 1. Lo que YA tenemos (no reinventar) — `concurrency.py` (R3)

El `ConcurrencyManager` (195 líneas) ya implementa el sistema de 3 capas:
- **CAPA 1** token bucket local preventivo (RPM/ITPM/OTPM por modelo).
- **CAPA 2** lee los headers de Anthropic y ajusta el ritmo.
- **CAPA 3** backoff con retry-after exacto.
- **+ modo cortés** (reserva margen para otros consumidores de la cuenta).

**El hueco:** el tool-use (`complete_with_tools`) pasa por `_post` → usa el
manager, PERO la estimación de tokens (`est_in`) es GRUESA y NO cuenta el peso
de los schemas de tools ni las llamadas en ráfaga del loop. → el bucket cree
que hay cuota cuando no la hay → deja pasar → topa el 429 real.

---

## 2. Diseño propuesto (3 partes, incremental)

### PARTE A — Conectar bien el tool-use al manager (el arreglo base)
- En `complete_with_tools`: estimar `est_in` REAL incluyendo el tamaño de los
  schemas de tools (no solo el de messages). Así el bucket sabe el peso real.
- En `tool_loop`: cada vuelta es una llamada; el manager ya las espacia vía
  `acquire()`. Asegurar que el loop respete el `wait_time` del bucket ENTRE
  vueltas (seccionado natural — tu idea de "cada X seg").
- Leer `reset-at` de los headers para esperas exactas (no adivinar).

### PARTE B — Cola de procesos (tu idea de "seccionar")
- Una **cola asíncrona** a nivel del canal: si llega un análisis GitHub
  mientras otro corre (o el bucket no tiene cuota), se ENCOLA en vez de
  mandarse de golpe.
- Se procesan de a uno (o N controlado), respetando el bucket → nunca ráfaga.
- El usuario recibe feedback: "📋 En cola, lo proceso en cuanto se libere
  cuota" (mejor que un 429 seco).
- Implementación: `asyncio.Queue` + un worker que consume respetando el manager.

### PARTE C — Prompt caching (reducir el consumo de raíz)
- Marcar los schemas de tools + el system con `cache_control` (Anthropic
  prompt caching). El contenido repetido (schemas, identidad) se cachea →
  cuenta ~10% de su ITPM real en llamadas siguientes.
- Funciona con OAuth de suscripción (verificado en la investigación).
- → Reduce 75-90% el ITPM de las llamadas del loop (que reenvían lo mismo).
- Requiere ajustar el payload de `complete_with_tools` (header beta + bloques
  con cache_control).

---

## 3. Orden de implementación incremental

```
   PASO 1 (Parte A) — estimación real de tokens + espaciado del loop.
            El arreglo más directo. Resuelve ~70%. Bajo riesgo.
   PASO 2 (Parte C) — prompt caching de schemas+system. Gran reducción de ITPM.
            Medio riesgo (tocar el payload). Verificar que OAuth lo acepte.
   PASO 3 (Parte B) — cola de procesos con feedback al usuario.
            Más código nuevo. El más robusto ante ráfagas reales.
```

Cada paso: explicar a Brian → aprobar → implementar → Brian prueba → commit.

---

## 4. Lo que NO hacemos (descartado con razón)
- ❌ "Refrescar" el rate-limit manualmente → no existe (token bucket temporal).
- ❌ Message Batches API → solo API key de pago, no OAuth de suscripción.
- ❌ Cambiar a API key → fuera de alcance (Brian usa OAuth verificado).

---

## 5. Alineación con R3 LOCKED
R3 ya diseñó el Token Bucket + circuit breaker + cost control. Este anexo NO
contradice R3: implementa lo que faltaba conectar (tool-use) + añade la cola
(que R3 contemplaba como "carriles") + prompt caching (optimización). El
`ConcurrencyManager` es la base; esto lo completa.

---

## 6. Decisión pendiente (Brian)
- [ ] Aprobar el enfoque de 3 partes (A conectar + C caching + B cola).
- [ ] ¿Empezamos por Paso 1 (Parte A, el arreglo base) y probamos antes de seguir?
- [ ] ¿La cola (Parte B) da feedback "en cola" al usuario, o procesa en silencio?
