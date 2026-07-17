# 🔬 SPIKE — OpenCode como 2º proveedor LLM de For3s

> **Spike de investigación (NO es un hito de obra).** Verificar si For3s puede usar OpenCode como segundo motor de IA (además de Claude), vía su modo servidor HTTP. Decisión de Brian: Camino A (2º proveedor por HTTP) + spike primero. Resultado abajo.

**Fecha:** 2026-06-11
**Estado:** 🟢 SPIKE EXITOSO — viable. Integración formal DIFERIDA a H7 (DECIDE).
**Brújulas:** R3 (Model/LLM Layer — multi-provider con fallback ya lockeado).

---

## 🎯 Pregunta del spike

¿Puede For3s (Python) usar OpenCode como 2º proveedor LLM, para tener GPT/
Gemini/locales/Zen + un carril independiente (anti-429) además de Claude?

## ✅ RESULTADO: SÍ, viable. Probado end-to-end en el servidor for3s.

```
   For3s (Python httpx) ──HTTP──► opencode serve :4096 ──► modelo LLM ──► OK
```

## 🔬 Qué se hizo y qué se descubrió

```
   1. Instalado OpenCode 1.17.3 en for3s (~/.opencode/bin, curl install). MIT.
   2. `opencode serve --port 4096` → servidor HTTP con OpenAPI 3.1, 135 endpoints
      (sesiones, mensajes, providers, eventos SSE...). Auth básica opcional
      (OPENCODE_SERVER_PASSWORD).
   3. Config headless del proveedor: env var (ej. OPENCODE_API_KEY para Zen,
      ANTHROPIC_API_KEY/OPENAI_API_KEY para otros) — NO requiere navegador.
      opencode.json acepta {env:VAR} y {file:~/path}.
   4. OpenCode Zen (key sk-vR316... de Brian) expone modelos: deepseek-v4,
      minimax, qwen3.7, glm-5.1, kimi-k2, mimo-v2.5 (free y pro).
   5. PRUEBA: desde Python, POST /session → crea sesión; POST /session/{id}/
      message con {model:{providerID,modelID}, parts:[{type:text,text}]} →
      respuesta. Con mimo-v2.5-free → "RESPUESTA: OK" ✅.
   6. Los modelos de PAGO de Zen dieron UnknownError = falta de créditos en la
      key (el gratis funcionó → el camino técnico es sólido, era saldo).
```

## 🧩 Cómo encajaría en For3s (Camino A — para H7)

```
   • Nuevo OpenCodeProvider(LLMProvider) en llm.py: en vez de httpx a
     api.anthropic.com, hace httpx a http://127.0.0.1:4096 (OpenCode server).
   • For3s mantiene su ClaudeProvider propio (H1) como primario.
   • OpenCode = 2º proveedor → da GPT/Gemini/locales/Zen + carril alterno.
   • Encaja con R3 (multi-provider + fallback) y con el tier-routing de R5/H7.
   • El server OpenCode corre como servicio en for3s (systemd, plano R10).
```

## ⚖️ Decisiones / hallazgos clave

```
   ✅ Viable técnicamente (probado).
   ✅ MIT, 173K ⭐, activísimo (release de ayer). Empresa: Anomaly.
   ✅ Soporta suscripción Claude Pro/Max Y ChatGPT Plus/Pro vía OAuth
      ("no respaldado oficialmente por Anthropic/OpenAI" — igual que Claude
      Code: sirve para uso propio, NO para vender a clientes sin permiso).
   ⚠️ SDK solo JS/TS → For3s usa el modo SERVIDOR (HTTP, agnóstico). Correcto.
   ⚠️ Añade un servicio más que correr/mantener (otro proceso, otro puerto).
   ⚠️ Key Zen sk-vR316... EXPUESTA en chat → ROTAR. Sin créditos en modelos pago.
```

## ⏭️ Decisión: DIFERIR la integración a H7 (DECIDE)

```
   El spike confirma que se PUEDE. Pero meterlo AHORA desviaría del orden de
   obra (toca cerrar el MVP: H3 Telegram + H4 PR). R5/H7 ya tenía planeado el
   tier-routing multi-modelo — ahí es donde OpenCode entra natural como 2º
   proveedor. Por ahora: spike documentado, OpenCode instalado en for3s,
   camino validado. Se retoma en H7.
```

---

**Estado:** spike cerrado-OK. OpenCode queda instalado en for3s (sin correr).
Integración formal = H7. Siguiente de obra = H3 TELEGRAM.