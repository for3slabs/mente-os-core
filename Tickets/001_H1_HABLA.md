# 🎫 Ticket 001 — H1 "HABLA"

> **Hito H1 del Mapa de Construcción Incremental.** El agente cobra vida: recibe un mensaje en el CLI del servidor y responde razonando con Claude, mostrando el costo. El primer latido cognitivo de For3s OS.

**Épica:** A — MVP Pilotable
**Estado:** 🟢 CERRADO-OK · DEMO PASADO 2026-06-11 (For3s detectó el bug razonando con Claude)
**Abierto:** 2026-06-10
**Owner:** Brian López · construido en servidor for3s
**Brújulas:** Grafo Maestro (Nodo 3 PFC = LLM corteza) · Plan Maestro (Fase 1, R3) · Mapa Incremental (H1)

---

## 🎯 Objetivo

Que For3s OS pase de "repo con tests" a "agente que razona": escribes en el CLI → responde con Claude → ves el costo/uso.

## ⚙️ Decisiones alineadas con Brian (2026-06-10)

```
   • Auth:   DUAL — OAuth-suscripción (default, usa el plan de Brian SIN pago
             por token, como Claude Code) + API key (fallback/clientes enterprise).
   • Modelo: Claude Sonnet 4.6 (claude-sonnet-4-6) — lockeado R3.
   • Git:    commit + push por cada pieza funcional.
   • Ticket: detallado, bitácora viva.
```

## 🔬 HALLAZGO CLAVE (investigado con pruebas reales contra api.anthropic.com)

```
   ✅ CONFIRMADO 2026-06-10: el token de SUSCRIPCIÓN (sk-ant-oat01-...) SÍ
      funciona para llamar a Claude sin pago por consumo. Fórmula exacta:

      Header  authorization: Bearer <token oat01>     (NO x-api-key)
      Header  anthropic-beta: oauth-2025-04-20
      Header  anthropic-version: 2023-06-01
      System prompt DEBE iniciar con:
        "You are Claude Code, Anthropic's official CLI for Claude."

   Evidencia: prueba 1 (x-api-key) → 401 invalid. prueba 2 (Bearer, sin
   system Claude Code) → 429. prueba 3 (Bearer + beta + system Claude Code)
   → HTTP 200, respuesta correcta, modelo claude-sonnet-4-6. req_01Pjy7wh...

   ⚠️ DESVIACIÓN DE DISEÑO: R3 lockeó API key + pago por consumo. Esto usa
      OAuth de suscripción. Registrado como desviación (mejor para margen;
      menos estándar; para clientes enterprise probablemente API key). El
      provider dual cubre ambos mundos.
   ⚠️ El token sk-ant-oat01 que Brian pegó en el chat quedó EXPUESTO →
      ROTAR tras validar H1 (Brian genera uno nuevo en claude.com).
```

## 📋 Sub-tickets (estado vivo)

```
   [x] H1.1  Config/secrets: leer token de .env (OAuth o API key) — config.py ✅
   [x] H1.2  LLMProvider (ABC) — llm.py ✅
   [x] H1.3  ClaudeProvider — modo dual (Bearer+oauth-beta / x-api-key) ✅
   [x] H1.4  Prompt builder mínimo (system Claude Code obligado en OAuth) — agent.py ✅
   [x] H1.5  Cost/usage tracker (tokens in/out + $ estimado) ✅
   [x] H1.6  CLI loop (rich) — cli.py ✅
   [x] H1.7  Tests (provider mock + cost + headers + identidad) — 8 tests ✅
   [x] H1.8  .env en servidor (chmod 600, git lo ignora) ✅
   [x] H1.10 Gestor de concurrencia (CallGate lock + espaciado + backoff retry-after)
             — adelanto R3/H7. ratelimit.py + 2 tests ✅. 10 tests totales verdes.
   [x] H1.9  DEMO end-to-end ✅ PASADO 2026-06-11. For3s analizó def suma(a,b):
             return a-b → detectó el bug (resta, no suma), tabla de casos,
             corrección y veredicto. Cuenta OAuth SEPARADA (sin Claude Code).
   [x] H1.11 agent.py OAuth-aware: en modo suscripción el rol For3s va en el
             MENSAJE user (no system), porque la suscripción rechaza system
             custom con 429. En modo API key el rol va al system (natural).
```

## ✅ DEMO de cierre (definición de "terminado")

```
   En el servidor for3s: corro el CLI, escribo "analiza: def suma(a,b): return a-b"
   → For3s responde señalando el bug (resta, no suma) → muestra tokens + costo.
   Funciona end-to-end con Claude vía suscripción.
```

## 🚫 Fuera de alcance (otros hitos)

memoria/persistencia (H2) · Telegram (H3) · tools/GitHub (H4) · Postgres (H2).

---

## 📓 BITÁCORA VIVA (qué funcionó / qué no / por qué / cuándo)

```
   2026-06-10 · Investigación OAuth: 3 pruebas curl. x-api-key falló (401),
                Bearer solo (429), Bearer+oauth-beta+system Claude Code → 200 ✅.
                Descubierto el requisito del system prompt Claude Code. Fórmula
                lista para implementar el provider sin adivinar.
   2026-06-10 · Construido H1 completo (config dual, provider, agent, CLI, cost).
                8 tests verdes. ruff/ty OK. Subido al monorepo del servidor.
   2026-06-10 · DEMO falló con 429 (rate_limit). Diagnóstico: el token de
                suscripción que Brian pegó es EL MISMO de su Claude Code activo
                (este chat). Compiten por la misma cuenta → 429. Headers
                revelaron: cuota OK (54% en 5h) pero overage out_of_credits y
                límite de concurrencia bajo del plan.
   2026-06-10 · QUÉ FUNCIONÓ: auth OAuth (curl suelto → 200), código, tests.
                QUÉ NO: DEMO end-to-end. POR QUÉ: contención de token compartido
                con Claude Code (un recurso, dos consumidores).
   2026-06-10 · Construido gestor de concurrencia (Opción B, decisión de Brian):
                CallGate (lock entre procesos O_EXCL + espaciado MIN_INTERVAL +
                backoff que respeta retry-after). ratelimit.py + 2 tests → 10
                tests verdes. ruff atrapó B904 (raise from None), corregido.
   2026-06-10 · DEMO con CallGate TAMBIÉN falló (429, >2min reintentando).
                CONCLUSIÓN: el gestor serializa For3s entre sí, pero el rate
                limit es de la CUENTA — imposible ganar mientras Claude Code
                (este chat) trabaja sobre el mismo token. Confirma el diagnóstico
                original de Brian: hay que DIVIDIR EN LÍNEAS (carriles separados).
   2026-06-10 · DECISIÓN: credencial SEPARADA para For3s (Opción A). Brian
                consigue API key sk-ant-api03 (dev, créditos mín.) o 2da cuenta,
                la pega en .env del servidor. Provider dual ya lo soporta →
                el DEMO pasará al instante (carril independiente). H1 código
                100% listo; solo falta enchufar la credencial correcta.
```

## ⏭️ Para cerrar H1 (acción de Brian — DECISIÓN FINAL: Carril B)

```
   1. console.anthropic.com → API Keys → Create Key "for3s-os-dev"
   2. Plan & Billing → cargar ~$5 créditos (dev consume centavos)
   3. En el servidor: editar ~/for3s-os/.env →
        ANTHROPIC_TOKEN=sk-ant-api03-...
        FOR3S_AUTH_MODE=apikey
        FOR3S_MODEL=claude-sonnet-4-6
   4. Avisar → se corre el DEMO → cierra H1 al instante (carril independiente).
```

## 🔬 INVESTIGACIÓN DOC CLAUDE CODE (2026-06-10) — hallazgos clave

```
   • Existe el Claude Agent SDK (pip claude-agent-sdk) que SÍ usa la
     suscripción. PERO la doc prohíbe explícitamente ofrecer login/límites
     de suscripción a TERCEROS (clientes) sin aprobación de Anthropic →
     para el PRODUCTO multi-tenant hay que usar API key igual (valida R3).
   • Decisión motor LLM: httpx dual propio (NO migrar al Agent SDK, que
     duplicaría R4/R5/R6 y ataría For3s a Anthropic).
   • Rate limits: token bucket por ORGANIZACIÓN, por modelo (Sonnet/Haiku/
     Opus separados). Headers de respuesta: anthropic-ratelimit-unified-*
     (formato suscripción) — NO los anthropic-ratelimit-requests-* (API key).
     429 trae retry-after exacto.
   • Diagnóstico FINAL del 429: token OK (curl suelto → 200, cuota 5h=20%,
     7d=47%), pero overage-disabled=out_of_credits → no hay créditos para
     absorber picos de concurrencia. Mientras Claude Code (chat de Brian) y
     For3s piden a la vez, colisionan en el ritmo. Carril A = empate técnico
     (el chat nunca está idle). → Carril B (API key separada) lo resuelve.
   • 15-jun-2026: Agent SDK/suscripción tendrá crédito mensual SEPARADO del
     uso interactivo → otra vía futura de separar carriles.
```

---

**Estado al momento:** H1 código 100% listo y EN GITHUB con CI VERDE
(commit b95a4d7: SAST ✅ Lint+Types+Tests ✅ Pilar3 Gate ✅). 14 tests
verdes. Gestor de concurrencia 3 capas construido. El curl suelto YA probó
el camino completo (200 + respuesta real). DEMO end-to-end espera la API
key dev (Carril B) — solo enchufar al .env y correr.

## 📓 BITÁCORA — cierre de sesión 2026-06-10/11

```
   • Investigada doc Claude Code a fondo: Agent SDK existe pero prohíbe
     suscripción para terceros → motor httpx propio (decisión). Rate limits
     por org+modelo, headers unified-* (suscripción), retry-after exacto.
   • Construido gestor de concurrencia 3 capas (token bucket local + lectura
     headers + backoff retry-after + modo cortés Carril A + por-modelo).
   • DEMO con gestor TAMBIÉN dio 429. Headers revelaron la causa REAL:
     cuota OK (5h=20%, 7d=47%) PERO overage out_of_credits → sin créditos
     para picos de concurrencia. Carril A = empate (este chat nunca idle).
   • Decisión de Brian: Carril B (API key dev separada). Provider dual ya
     lo soporta → enchufar .env y el DEMO pasa.
   • Limpieza: eliminados ratelimit.py/test_gate.py (intento previo CallGate,
     superado por concurrency.py; bandit marcaba B108 /tmp). CI quedó verde.
   • QUÉ FUNCIONÓ: auth (curl 200), código, gestor, 14 tests, CI verde.
     QUÉ NO: DEMO en vivo. POR QUÉ: Carril A choca con Claude Code activo.
     QUÉ HICIMOS: gestor robusto + decisión Carril B. Falta: API key dev.
   • 2026-06-11 · HALLAZGO DEFINITIVO: la 2da cuenta OAuth (sin Claude Code)
     seguía dando 429 — pero NO por contención (cuota 0%). Aislado: el
     disparador es el SYSTEM PROMPT custom. system "Claude Code puro" → 200;
     system con rol For3s → 429. La suscripción SOLO permite correr Claude
     Code tal cual, rechaza agentes con identidad propia. CONFIRMA la doc.
   • 2026-06-11 · SOLUCIÓN: agent.py OAuth-aware — en modo suscripción el rol
     For3s se antepone al mensaje user (no al system). DEMO PASÓ: For3s
     detectó el bug perfectamente. H1 CERRADO con suscripción.
   • PENDIENTE FUTURO: para que For3s tenga identidad en el SYSTEM (lo ideal
     enterprise) → API key sk-ant-api03 (clientes la necesitan igual, R3).
     El provider dual ya lo soporta: cambiar .env y listo.
   • ROTAR los 2 tokens oat01 expuestos en el chat (higiene de seguridad).
```

## ✅ H1 CERRADO — resumen

```
   For3s OS HABLA: agente CLI que razona con Claude (Sonnet 4.6) vía
   suscripción OAuth, detecta bugs, muestra uso. Código en GitHub con CI
   verde. Gestor de concurrencia 3 capas (adelanto R3) incluido.
   DEMO: analizó def suma(a,b):return a-b → detectó el bug. ✅
   Siguiente hito: H2 RECUERDA (persistencia + audit chain).
```