# 🧩 Ronda — MOLDE "For3s Inside" (la capa reutilizable para clientes tipo NavigoX)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

## Purpose

🧩 Ronda — MOLDE "For3s Inside" (la capa reutilizable para clientes tipo NavigoX)


> **Qué es:** el siguiente frente tras el Frente B (Brian eligió "productizar NavigoX",
> 2026-07-15). NO es re-hacer NavigoX (eso vive en `~/5M-incubathon/`, cerrado aquí);
> es convertir la capa For3s del pitch en un **MOLDE reutilizable** — "una capa por si
> alguien de otra empresa quiere lo mismo, poder ocupar ese molde" (Brian). Método de Fases F.

## La visión de Brian (el contrato)
- NavigoX fue el PRIMER cliente (integración artesanal). El molde lo vuelve **repetible**:
  cualquier empresa toma la plantilla y For3s es el cerebro de su producto en minutos, no días.
- For3s se OCUPA, no se entrega (caja negra). El cliente jamás ve código/lógica/BD.

## Las 4 piezas del molde (viven en `molde/for3s-inside/` del repo)
- **M1 · Contrato de API** — spec OpenAPI 3.1 formal + README legible. La fuente de verdad.
- **M2 · SDK / receta** — cliente TS (y Python) listo para pegar: `for3s.chat(...)` en vez de
  fetch a mano. Manejo de errores/reintentos/identidad/BYOK resuelto.
- **M3 · Onboarding repetible** — comando/panel que arma el paquete del cliente (alta + key +
  cuota/scopes + [instancia] + entrega contrato+SDK) de una.
- **M4 · Receta de trazabilidad** — el patrón NavigoX (traza → cifra → For3s sin BD del cliente)
  como receta + ejemplo mínimo funcional.

## ✅ M1 CERRADA — contrato de API formal (commit `69b620b`)
- `molde/for3s-inside/for3s-api.yaml`: **OpenAPI 3.1** de los 4 endpoints reales (/v1/health,
  /v1/chat, /v1/token BYOK, /v1/olvidar) con request/response/errores/límites EXACTOS.
- `molde/for3s-inside/README.md`: guía legible para el cliente (3 pasos, curl de ejemplo,
  conceptos tema/errores/límites, patrón de trazabilidad, punteros al estándar de datos).
- **VALIDADO contra la API REAL (5/5):** health {ok:true} · 401 sin key · 400 msg vacío · chat
  {client,reply,thread} · olvidar {ok,turnos_borrados,tema}. El contrato dice la verdad.
- Cliente de prueba limpiado. Tríada sincronizada en `69b620b`.

## ✅ M2 CERRADA — SDK cliente TS + Python (commit `93c08e5`)
- `molde/for3s-inside/sdk/for3s.ts`: SDK TypeScript (Node/Deno/Bun/navegador, CERO deps).
  `new For3s({apiKey,baseUrl}).chat("...")`. **Errores TIPADOS** (`For3sError.kind`: auth/acceso/
  limite/timeout/invalido/red/servidor) → el cliente decide sin parsear strings. **Reintentos
  INTELIGENTES** (backoff+jitter SOLO en red/timeout; NUNCA reintenta 429/401 — lección de F5:
  reintentar un límite empeora). Pasa `tsc --strict`.
- `sdk/for3s.py`: paridad total (stdlib urllib, cero deps).
- `sdk/ejemplo.ts`: patrón cliente tipo NavigoX (memoria por hilo + errores por tipo + BYOK).
- **PROBADOS contra la API REAL (4/4 cada uno):** health · chat real con memoria (thread correcto)
  · key inválida → For3sError kind=auth no reintentable · olvidar. Clientes de prueba limpiados.

## ✅ M3 CERRADA — onboarding repetible + BUG cazado (commits `8d30ad1` server + `65f132c` panel)
- `api_admin.onboarding()`: da de alta un cliente NUEVO en UNA operación — normaliza nombre→id +
  **rechaza si ya existe** + fija key/expiración/scopes/cuotas de una + audit. + `normalizar_client_id`
  + `existe_cliente` (puras). CLI `onboarding` + el panel (`_alta`) ahora usa onboarding.
- El formulario "+ Nuevo cliente" del panel arma el paquete completo (id+nombre+expiración+cuotas);
  id repetido → 409 con mensaje claro, sin re-keyear a nadie.
- **🐛 BUG cazado (curiosidad de Brian):** `api_admin.alta` con ON CONFLICT DO UPDATE **re-generaba
  la key de un cliente EXISTENTE sin avisar** (confirmado en vivo: 2 altas del mismo id = 2 keys, la
  del cliente vivo moría). Onboarding lo blinda; alta cruda queda solo para re-key intencional.
- **🐛 2º hallazgo (patrón conocido):** el contenedor `admin` corría imagen VIEJA (el `--force-recreate`
  NO reconstruye) → la 1ª prueba del panel dio 200 en vez de 409. Rebuild del agent (imagen compartida)
  + recreate → arreglado. Lección "docker cp/imagen efímera" otra vez.
- **E2E por el panel (tailnet):** alta+cuotas OK · duplicado 409 · cuotas fijadas · la key del
  onboarding conversa de verdad. 218 tests. Clientes de prueba limpiados.

## ✅ M4 CERRADA + 🔴 AUDITORÍA CAZA-BUGS (Brian: "bugs más grandes") — commits `8c6673c`/`9a49d98`/`4778a12`
- **M4 receta de trazabilidad** (`4778a12`): `TRAZABILIDAD.md` (patrón NavigoX: traza→For3s como
  memoria sin BD del cliente, 3 pasos + diagrama) + `sdk/ejemplo_trazabilidad.ts`. **Probado vs API
  real:** For3s recordó el hilo completo e integró 3 eventos de una reserva en un resumen. tsc OK.
- **🔴 BUG DE SEGURIDAD cazado y EXPLOTADO (`8c6673c`):** `/v1/olvidar` usaba `session_id LIKE
  "api:<cliente>:%"`. `_limpiar_id` filtra `%` pero NO `_` (el otro comodín LIKE). PoC en vivo: un
  demo con `X-Client-Id: _` **borró la memoria del cliente `a`** (2→0). Viola aislamiento AI1 (línea
  roja). Fix: `_escapar_like()` + `LIKE ... ESCAPE '\'`. Post-fix: atacante borra 0, `a` intacto.
  Solo /v1/olvidar usaba LIKE con entrada del cliente (/v1/chat usa igualdad exacta).
- **🐛 2º bug (`9a49d98`): race TOCTOU en onboarding** — `existe_cliente()` + `alta()` en 2 pasos →
  dos onboardings concurrentes del mismo id re-keyeaban en silencio. Fix: `alta(solo_nuevo=True)` con
  ON CONFLICT DO NOTHING (atómico). Verificado: 5 onboardings paralelos del mismo id → 1 gana, 1 key.

## Estado
🎉 **MOLDE COMPLETO (M1 contrato + M2 SDK + M3 onboarding + M4 trazabilidad).** Un cliente tipo
NavigoX se integra con `molde/for3s-inside/` + su key, en minutos. **6 commits + 4 bugs cazados**
(alta re-key, admin imagen vieja, LIKE injection SEC, onboarding race). Tríada sincronizada `4778a12`.
**Siguiente frente lo marca Brian** (§5-bis: C multi-canal · E confianza).
⚠️ Recordar: NavigoX vive en OTRO Mente OS (`~/5M-incubathon/`), CERRADO — no leerlo sin gate.
El molde se construye AQUÍ con lo que ya sabemos del canal + la Ronda del Frente B.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde v1, ADR-029).
