# 🔬 INVESTIGACIÓN — Cache de Anthropic para no releer la conversación (Claude Code)

> **Fecha:** 2026-07-07 · **Origen:** Brian detectó que al retomar Claude Code tras una pausa,
> el uso salta de ~1% a ~45% en un solo mensaje (capturas: Session 5hr pasó de 0% → 45%).
> **La idea de Brian:** un mecanismo (tipo cron cada 5 min) que consuma el MÍNIMO para mantener
> vivo el cache de Anthropic y NO tener que reenviar toda la conversación al retomar — sin afectar
> su chat, sus tareas ni su flujo. "Aprovechar el prefijo exacto de contenido."
> **Estado:** investigado a fondo en las 3 fuentes oficiales. Veredicto abajo. ⏸️ PENDIENTE.

---

## 0 · El problema, medido

- El **cache de Anthropic tiene TTL de 5 min de inactividad**. Mientras Brian escribe seguido
  (mensajes con < 5 min entre sí), el cache se mantiene y solo se paga lo nuevo (barato).
- Si Brian **tarda > 5 min** en responder → el cache EXPIRA → el siguiente mensaje debe
  **reenviar TODA la conversación** para reconstruir el contexto (cache miss). En una sesión
  de horas de trabajo (como las del entrenamiento) eso es el salto 0% → 45%.
- ⚠️ **No confundir con RETOMAR.md inflado** (ese era otro problema, ya resuelto el mismo día:
  RETOMAR pasó de 84KB → 6KB). El cache que muere aquí es **la CONVERSACIÓN ACUMULADA**, no
  Mente OS. RETOMAR ayuda al hacer `/clear` fresco; NO evita el cache-miss por espera.

---

## 1 · Cómo funciona el cache (doc oficial de prompt caching, verificado 2026-07-07)

- El cache reutiliza un **PREFIJO EXACTO** del prompt hasta un `cache_control` breakpoint
  (hash del contenido; 100% match byte a byte, incluido texto/imágenes/metadata).
- **Cada cache READ resetea el timer de 5 min** ("refreshed at no additional cost each time
  it's hit; each cache read resets the 5-minute timer"). → la idea de Brian es CONCEPTUALMENTE
  CORRECTA: tocar el cache lo mantiene vivo.
- **TTL de 1 hora disponible**: `"cache_control": {"type":"ephemeral","ttl":"1h"}` (cuesta 2x
  en la escritura; dura 12× más).
- **Pre-warming** con `max_tokens: 0`: mandar una petición que no genera output, solo calienta
  el cache. Existe — pero para TU propia app donde controlas el prompt.
- **Precios:** write 5m = 1.25x · write 1h = 2x · **read/refresh = 0.1x** (10% del base) ·
  mínimo cacheable Fable 5 = 512 tokens.

## 2 · Por qué el "cron cada 5 min" NO se puede en Claude Code (el muro real)

Investigado en las 3 capas donde podría estar el gatillo:

| Fuente oficial | Resultado |
|---|---|
| **Prompt caching (API)** | ✅ El mecanismo existe (refresh, TTL 1h, pre-warm). Tu intuición era buena. |
| **Settings de Claude Code** (`code.claude.com/docs/en/settings`) | ❌ **CERO** settings de caché/keep-alive/TTL. No hay `CLAUDE_CODE_CACHE` ni forma de configurar la ventana de 5 min. Lo más cercano: `autoCompactEnabled`, `MAX_THINKING_TOKENS`, `askUserQuestionTimeout` — nada sirve para esto. |
| **Hooks de Claude Code** (`code.claude.com/docs/en/hooks`) | ❌ De los 33 hooks, **NINGUNO dispara por timer/idle/periódico**. Todos reactivos (responden a acción del usuario). Literal: *"zero support for autonomous, timer-based, or idle-triggered notifications."* El único "wake" es `asyncRewake` y requiere que un hook YA esté corriendo por una acción del usuario. |

**Las 3 razones técnicas por las que el cron falla:**
1. **Acceso al prefijo:** para refrescar el cache de la sesión de Brian hay que reenviar el
   prefijo EXACTO de SU conversación. Esa conversación vive DENTRO del cliente de Claude Code
   (no en un archivo que un cron pueda leer/reenviar). Un cron externo no la tiene.
2. **Sin gatillo interno:** no existe hook que dispare solo cada 5 min para hacerlo desde dentro.
3. **Aunque se pudiera, no ahorra:** reenviar la conversación completa cada 5 min, sin parar,
   aunque sea a 0.1x (read), sobre horas de contexto, gasta MÁS que el reenvío puntual que se
   quiere evitar. El refresh barato solo lo es si el cache SIGUE vivo; si ya lo mantienes vivo
   cada 5 min para siempre, pagas el read gigante infinitas veces.

**Conclusión:** la API da las herramientas; **Claude Code NO expone el gatillo** para refrescar
el cache de tu sesión desde fuera. Es decisión de diseño de Anthropic (la sesión la controla el
cliente, no un script del usuario). El cron sombra, como se imaginó, **no es viable HOY.**

## 3 · Lo que SÍ funciona para el problema de Brian (sin construir nada)

- **Regla del cache de 5 min:** mientras Brian trabaje seguido (mensajes < 5 min), el cache se
  mantiene solo → cero reenvíos. El salto 0→45% ocurre SOLO tras pausas > 5 min.
- **`/clear` estratégico:** si Brian va a pausar > 5 min (comida, reunión), hacer `/clear` ANTES
  es más barato que volver a una conversación gigante. Al reabrir, Claude lee RETOMAR (6KB) y
  retoma con contexto completo, pero la conversación arranca liviana → el cache que puede morir
  es chico, no de horas. (Ya es la práctica LOCKED — [[feedback_cold_start_retomar]].)
- **Trabajar por BLOQUES:** cerrar un bloque ("E6 hecho") → `/clear` → RETOMAR devuelve al punto.

## 4 · ⏸️ PENDIENTES derivados de esta investigación

### PENDIENTE A — Cache 1h para los 5 agentes For3s (⭐ ganancia REAL, factible)
En los agentes For3s SÍ controlamos el código del provider (`llm.py`), así que SÍ tenemos el
gatillo. Aplicar `cache_control` con `"ttl":"1h"` al system prompt (identidad + memoria =
la parte estable y grande) → cuando un agente está idle < 1h, su prefijo se mantiene caliente
12× más → **menos reenvíos = menos consumo de la suscripción COMPARTIDA** (1 solo cupo para
los 5). Verificar primero que el provider ya usa cache breakpoints; medir `cache_read_input_tokens`
antes/después. Riesgo bajo, aditivo. Cruza con cost-control H8 y el cupo compartido.

### PENDIENTE B — Re-evaluar cuando cambie Claude Code (revisión periódica)
Anthropic evoluciona rápido. Re-checar en el futuro si aparece: un setting de TTL/keep-alive,
un hook de timer/idle, o una API para refrescar el cache de la sesión. Si aparece cualquiera,
la idea original de Brian (refresh sombra cada 5 min) se vuelve construible. Fuentes a re-leer:
`code.claude.com/docs/en/settings` · `.../hooks` · docs de prompt-caching.

### (Descartado, documentado para no reintentarlo) — Cron sombra externo
NO construir un cron/proceso externo que intente refrescar el cache de la sesión de Claude Code:
imposible por §2 (sin acceso al prefijo, sin gatillo interno, y no ahorraría). Si alguien lo
propone de nuevo, este doc es la razón.

---

*Fuentes (2026-07-07): platform.claude.com/docs prompt-caching · code.claude.com/docs/settings ·
code.claude.com/docs/hooks. Relacionado: [[feedback_cold_start_retomar]] (RETOMAR delgado + /clear)
· [[project_multi_instancia]] (los 5 agentes comparten 1 cupo).*
