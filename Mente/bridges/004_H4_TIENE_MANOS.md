# 🎫 Ticket 004 — H4 "TIENE MANOS" ★ cierra el MVP

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Tickets/004_H4_TIENE_MANOS.md → bridges/004_H4_TIENE_MANOS.md (2026-07-30, ADR-029)

> **Hito H4 del Mapa de Construcción Incremental.** For3s deja de analizar solo código pegado: le das la URL de un PR de GitHub y VA, lo lee solo, y entrega un REPORTE QA estructurado. Las manos del agente + el wedge QA del negocio.

**Épica:** A — MVP Pilotable (este hito la CIERRA)
**Estado:** 🟢 CERRADO (funcional + endurecido) — 2026-06-14
**Abierto:** 2026-06-12 · **Cerrado:** 2026-06-14
**Owner:** Brian López · construido en servidor for3s
**Brújulas:** Grafo (Nodo 4 manos + flujo "PR llega") · Plan Maestro (Fase 1, R4) · Mapa H4

---

## 🛡️ ENDURECIMIENTO H4 (2026-06-13/14) — fase de consolidación

Tras tener H4 funcional, Brian pidió ENDURECER todo el MVP (H4) antes de avanzar
a H5: probar, arreglar bugs temprano, pulir la infra. "Bug por bug, Brian prueba
entre cada uno." Resultado — todos verificados con uso real en Telegram:

```
   ✅ Identidad For3s — dejó de MENTIR sobre sus capacidades (decía "no tengo
      internet/memoria" comparándose con Hermes). Ahora declara lo que SÍ puede.
   ✅ Soporte ISSUES — detect_resource reconoce /issues/N + fetch_issue (triage).
   ✅ Bug E — canal por turno: la BD ahora distingue cli vs telegram (antes
      ON CONFLICT DO NOTHING dejaba todo en 'cli'). Migración 003. CLI y
      Telegram comparten memoria (sesión "brian") a propósito.
   ✅ Bug H — token de Telegram: fuera de logs (httpx→WARNING, 5243→0) + CIFRADO
      en SecretStore (KEK), ya no en .env plano. Logs viejos purgados.
   ✅ Warning shutdown PTB — investigado a fondo: es cosmético de la librería
      (no bug nuestro, el pool cierra bien). Documentado en teardown().
   ✅ Bug F — referencias cortas: "el PR 134" / "issue 10" sin URL → usa el
      último repo visto (sessions.meta). Detector conservador (no falsos
      positivos). Verificado en vivo (issue 10 traído por contexto).
   ✅ Bug G — cupo pin: no más editMessageText 400 ni parpadeo (no edita si el
      texto no cambió; maneja el 400 "not modified" como inofensivo).
   ✅ Identidad = SEGUNDO CEREBRO: no rechaza "fuera de mi scope". QA es su
      corazón pero ayuda con lo que sea (código, dudas, conversar). Alineado
      con Grafo Maestro (Cerebro_Humano, dinámica de aprendizaje).
```

**Estado del bot al cerrar:** corriendo en for3s, sonnet-4-6 vía OAuth, token
cifrado, logs limpios, migraciones BD v3, 64 tests + lint verdes.

**Hallazgo que abrió el siguiente capítulo:** al probar GitHub a fondo se vio
que es ARTESANAL (regex + API a mano, NO persiste datos) y se desvía de R4
LOCKED (que decidió GitHub MCP oficial). → Diseño de migración en
`work/Ronda_04_Anexo_GitHub_Migracion_MCP_Persistencia.md`.

---

## 🔌 MIGRACIÓN GitHub → MCP (2026-06-14) — COMPLETA, en producción

Se reemplazó la integración GitHub artesanal por el estándar: **GitHub MCP
server oficial + tool-use nativo** (el MODELO decide las tools, ya no el regex).
Alineado con R4.2.1 LOCKED. Los 7 pasos del anexo:

```
   ✅ P1 infra: cliente `mcp` (uv add mcp) + imagen ghcr.io/github/github-mcp-server
      v1.3.0 (Docker stdio --read-only). 21 tools de lectura.
   ✅ P2 persistencia: migración 004 → tablas gh_resources + gh_files (schema v4).
      Los datos de GitHub YA NO se tiran (antes se usaban 1 vez y se perdían).
   ✅ P3 puente: mcp_client.py (sesión MCP, PAT del SecretStore inyectado en
      runtime), llm.complete_with_tools() (+ manejo gracioso del 429),
      tool_loop.py (run_tool_loop: Claude pide tool → MCP → result → repite).
   ✅ P4-6 conectado al bot: conversation.send_with_tools() + huele_a_github()
      (tools solo si el msg lo amerita → ahorra rate-limit) +
      memory.save_gh_tool_calls() (persiste lo leído). telegram lanza/cierra el
      MCP en setup/teardown.
   ✅ P7: github_tool.py + pr_review.py marcados DEPRECADOS (NO borrados: red de
      seguridad durante el pulido; se borran al declarar el MVP pulido).
```

**Capacidades nuevas que esto habilitó:** LISTAR issues/PRs (antes imposible),
leer código completo (get_file_contents), y persistencia consultable para los H
futuros. **Hallazgo clave:** tool-use+OAuth consume el rate-limit instantáneo
rápido (payloads con schemas) → ráfaga=429; espaciado=OK. El bot real no topa.
(memorias: oauth_funciona_verificado, tooluse_oauth_ratelimit)

---

## 🔧 PULIENDO EL MVP H4 (2026-06-14 → en curso) — directriz de Brian

NO avanzar a H5+ hasta dejar el MVP muy pulido. Brian prueba a fondo en Telegram
(funcionalidad/autonomía/contestación/uso), reporta fallos, se arreglan iterando.
Fallos cazados y arreglados con pruebas reales:

```
   ✅ "escribiendo..." persistente (duraba 5s; análisis MCP tardan 30-60s →
      parecía colgado). Tarea de fondo que reenvía TYPING cada 4s.
   ✅ Fallo 1: For3s anunciaba "déjame revisar" sin EJECUTAR la tool →
      TOOL_DIRECTIVE (instruye usar la tool ya, no anunciarla).
   ✅ Fallo 2: conteos que paginan agotaban el loop ("no logré cerrar") →
      MAX_TOOL_ROUNDS 3→5 + respuesta parcial útil al agotar rondas.
   ✅ Normalización de texto (text_normalize.py): mayús/minús/acentos no
      afectan la detección (huele_a_github/detect_short_ref). + limpiar_urls
      (quita ?fbclid/utm_). Estándar para todo el sistema.
   ✅ H-A: no abortar tareas largas (timeout 120s→180s seguridad) + aviso
      inicial "🔍 Trabajando" + el resultado llega solo (multi-mensaje básico).
      Verificado: worldcoin/orb-hardware (58s, 4 tools, sin abortar).
   ✅ H-F: forzar ejecución de tools (tool_choice=any 1ª vuelta + prompt
      anti-invención). Causa raíz era el detector (no detectaba "ISSUES"
      plural ni nombres de repo) → arreglado con normalización. Ya NO inventa.
   ✅ Identidad SEGUNDO CEREBRO + honestidad de fraseo (no decir "trayendo"
      sin ejecutar tool en ese turno).
   ✅ Aviso de error SIEMPRE llega (_responder_seguro reintenta 3x) → nunca
      más "🔍 Trabajando" + silencio. Bug previo: el loop tragaba el
      RateLimitExceeded (except Exception: pass) → ahora lo re-lanza.
   ✅ COMANDOS de administración en Telegram (solo dueño/_es_admin, base rol
      admin futuro): /estado /diagnostico /reiniciar (suave, reconecta MCP)
      /reiniciar_duro (os._exit(1) → systemd Restart=on-failure lo revive).
   ✅ 🛡️ SISTEMA ANTI-RATE-LIMIT (A+B+C) — diseño en
      `work/Ronda_03_Anexo_Cola_RateLimit_ToolUse.md`:
      • A: espaciar loop 3s entre vueltas + contar schemas en el bucket (R3).
      • C: prompt caching de system+tools (75-90% menos input; VERIFICADO con
        OAuth: cache_creation→cache_read).
      • B: cola serial de tareas GitHub (asyncio.Lock, de a una) + feedback
        "📋 en cola" + máx 3 en espera. Charla normal sigue instantánea.
      HALLAZGO: la suscripción OAuth NO expone rate-limit por-minuto en
      headers (solo cupo 5h/7d) → bucket a ciegas → por eso espaciamos. No se
      puede "refrescar" el rate-limit (token bucket temporal).
```

(memorias: pulir_mvp_h4_antes_de_avanzar, hallazgos_estrategicos_h4_pulido,
tooluse_oauth_ratelimit)

---

## ⚙️ Decisiones alineadas con Brian (2026-06-12) — NIVEL PRODUCTO

```
   • GitHub: públicos + PRIVADOS. Token de la cuenta fruterito (el del WSL2,
     gh hosts.yml). Se guarda CIFRADO con KEK — NUNCA en texto plano.
   • UX: invocación NATURAL — pegas el URL del PR y For3s lo detecta solo.
   • Salida: REPORTE QA ESTRUCTURADO (📋 resumen → 🔴 críticos → 🟡 advertencias
     → 🟢 sugerencias → ⚖️ veredicto). Semilla del QA Pack de R7.
   • KEK foundation YA (R4): master key local protegida (~/.for3s/master.key
     600) → derivación HKDF por workspace → AES-256-GCM → secrets en BD.
     (El Master KEK offline TPM/USB llega en H16; esto es la v1 fiel a R4.)
   • Docker workspace YA, con FUNCIÓN REAL: el lint (ruff) del código del PR
     corre DENTRO del contenedor aislado → hallazgos objetivos se suman al
     análisis de Claude. Aislamiento con propósito, no teatro.
```

## 📋 Sub-tickets (estado vivo)

```
   [ ] H4.1  crypto.py — KEK: master key + HKDF + AES-256-GCM + tests
   [ ] H4.2  migración 002 (tabla secrets) + secrets.py (get/set cifrado)
   [ ] H4.3  GitHub token (fruterito) cifrado en BD del servidor
   [ ] H4.4  github_tool.py — parse URL PR + fetch (título/diff/archivos) +
             errores producto (404/privado/rate-limit) + truncado inteligente
   [ ] H4.5  Integración: detección natural de URL → tool → prompt QA → reporte
   [ ] H4.6  Docker: imagen for3s-workspace + ruff del PR en contenedor
   [ ] H4.7  Tests + guardianes + CI verde
   [ ] H4.8  DEMO ★: URL de PR real por Telegram → reporte QA completo
```

## ✅ DEMO de cierre (= MVP COMPLETO)

```
   1. Telegram: "analiza https://github.com/<repo>/pull/<n>"
   2. For3s detecta el URL → va a GitHub (token cifrado) → trae el PR
   3. Lint objetivo en contenedor Docker + análisis Claude
   4. Responde REPORTE QA estructurado con veredicto
   5. Pregunta de seguimiento → recuerda el contexto · todo en el audit
```

---

## 📓 BITÁCORA VIVA

```
   2026-06-12 · Ticket abierto. 4 decisiones producto alineadas. Arranca H4.1.
```