# 🎫 Ticket 003 — H3 "TELEGRAM"

> **Hito H3 del Mapa de Construcción Incremental — ▲ HITO LOCKED (R1 §10).** For3s sale de la terminal y vive en Telegram: le escribes al bot desde el celular y responde con el MISMO cerebro (memoria H2 + Claude H1 + audit). Primer momento "se ve como producto".

**Épica:** A — MVP Pilotable
**Estado:** 🟢 CERRADO-OK · DEMO PASADO 2026-06-11 (Brian desde su celular: /start dueño + respuesta ~4s + memoria compartida verificada)
**Abierto:** 2026-06-11
**Owner:** Brian López · construido en servidor for3s
**Brújulas:** Grafo (INPUT Telegram → flujo) · Plan Maestro (Fase 1, R4 parcial) · Mapa H3

---

## 🎯 Objetivo

Bot de Telegram conectado al cerebro existente (conversation.py). Solo Brian primero (allowlist fail-closed), multi-persona después.

## ⚙️ Decisiones alineadas con Brian (2026-06-11)

```
   • Conexión: POLLING (no webhook) — no expone puertos; patrón Hermes.
   • Acceso:   allowlist FAIL-CLOSED. El PRIMER /start registra al dueño
               (Brian); todo lo demás queda bloqueado. Multi-user después (H13).
   • Memoria:  COMPARTIDA con el CLI — el dueño usa la sesión "brian" en
               ambos canales (CLI y Telegram recuerdan lo mismo). Otros
               usuarios futuros → sesión propia tg-<chat_id>.
   • Arranque: servicio systemd permanente (vive siempre, restart on-failure).
   • Token bot: 8963177147:AA... (en .env; ⚠️ expuesto en chat → regenerar
               en BotFather al cerrar H3).
```

## 🔬 Análisis previo del Telegram de HERMES (código fuente clonado)

```
   gateway/platforms/telegram.py = 6,251 líneas (núcleo útil ~200 para H3):
   • python-telegram-bot (Application + handlers) — misma lib lockeada R4 ✅
   • POLLING con start_polling + delete_webhook al arrancar (evita conflictos)
   • Allowlist fail-closed: "no allowlist means deny by default" (l.557)
   • Sesión por chat_id · split de respuestas a 4,096 chars (límite Telegram)
   → Lecciones aplicadas a For3s: delete_webhook, fail-closed, split 4096.
```

## 🧱 Qué se produce / qué se altera

```
   NUEVO:    telegram_channel.py (canal+polling+authz+split) · owner store ·
             systemd unit for3s-telegram.service · tests
   SE TOCA:  config.py (+TELEGRAM_BOT_TOKEN, +owner session) · pyproject (dep)
   INTACTO:  agent.py · llm.py · audit.py · memory.py · conversation.py · cli.py
   → mayormente ADITIVO: el cerebro H1+H2 no se reescribe, solo gana una puerta.
```

## 📋 Sub-tickets (estado vivo)

```
   [x] H3.1  PTB 22.7 + token en .env + config (telegram_bot_token/owner_session) ✅
   [x] H3.2  telegram_channel.py completo ✅ (fix: return Settings era 1 línea,
             el parche inicial de config no matcheó → corregido)
   [x] H3.3  Memoria compartida VERIFICADA: sesión brian mezcla turnos CLI
             (22:36, 22:40) + Telegram (01:16) ✅
   [x] H3.4  7 tests sin red → 29 totales verdes ✅
   [x] H3.5  systemd active + enabled (sobrevive reinicios) ✅
   [x] H3.6  DEMO PASADO: /start → dueño 1923367928 (Brian🍓🥭) → "HOLA COMO
             ESTAS" → Claude 200 en ~3s → respuesta en el celular. Audit #40/#41,
             cadena íntegra (41). commit e12d24b CI verde ✅
```

## ✅ DEMO de cierre

```
   1. Brian le escribe /start al bot desde su celular → queda registrado dueño.
   2. Pregunta algo → For3s responde EN TELEGRAM.
   3. "¿qué te dije antes?" → RECUERDA (memoria compartida con el CLI).
   4. Otro usuario (si probara) → bloqueado (fail-closed).
   5. Todo quedó en el audit chain.
```

---

## 📓 BITÁCORA VIVA

```
   2026-06-11 · Ticket abierto. Hermes clonado y analizado (patrón polling +
                fail-closed + split 4096). Token recibido. Decisiones alineadas.
```
## 📓 BITÁCORA — cierre (forense del demo)

```
   2026-06-11 · DEMO real de Brian: timeline 01:15:11 arranque systemd →
                01:16:37 /start (dueño registrado) → 01:16:48 mensaje →
                01:16:51 Claude 200 (~3s) → 01:16:52 respuesta. ~4s e2e.
   2026-06-11 · QUÉ FUNCIONÓ: los 11 parámetros (polling, delete_webhook,
                dueño, fail-closed, typing, OAuth, memoria compartida,
                audit íntegro 41 entradas, systemd).
   2026-06-11 · HALLAZGOS: (1) cosmético — markdown crudo (**) visible en
                Telegram, falta parse_mode/limpieza; (2) sesión brian
                etiquetada channel=cli, turnos TG sin marcar canal (H13);
                (3) 16 sesiones test-* basura de tests de integración →
                limpiar/auto-limpiar. Ninguno grave.
   2026-06-11 · BUG resuelto durante construcción: parche de config.py no
                matcheó el return Settings de 1 línea → servicio arrancó
                sin token → corregido y reiniciado.
```
