# 🔌 PLAN DE IMPLEMENTACIÓN — Canal API + Túnel sobre GENERAL ("consume de aquí")

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Plan_Canal_API_Hoteles.md → work/Plan_Canal_API_Hoteles.md (2026-07-30, ADR-029)

## Purpose

🔌 PLAN DE IMPLEMENTACIÓN — Canal API + Túnel sobre GENERAL ("consume de aquí")


> ## ✅ ESTADO: F1-F5 CONSTRUIDO Y VERIFICADO (2026-07-11)
> Canal API vivo en `general` · túnel Cloudflare arriba · probado DESDE FUERA por internet.
> **URL demo actual:** `https://immunology-memorabilia-problems-carlo.trycloudflare.com`
> (efímera — relanzar con `~/tunel_hoteles.sh` el domingo; la URL cambia en cada arranque).
> **API key demo:** en `~/.for3s/general/.env` (FOR3S_API_KEY_DEMO). Endpoints:
> `GET /v1/health` · `POST /v1/token` (BYOK) · `POST /v1/chat`. Commits F1-F3 firmados.
> Bugs cazados: aiohttp/Dockerfile · FK persona · comillas SQL · (guardián AC4 revirtió un docker cp).

> **Hito:** convertir a `general` (@For3s_General_bot) en el For3s consumible por API por
> cualquier desarrollador, SIN exponer nada de For3s (caja negra). Primer consumidor: el
> sistema de cadena de hoteles del Incubathon. **Deadline: DOM 12 jul, 9:00 AM.**
> **Método F:** este doc = F0 (explicar). Se construye SOLO con aprobación de Brian.
> **Reconocimiento hecho (2026-07-11, en el server):** NO hay canal REST en el core (diseño
> R7 pendiente) · cloudflared NO instalado · dominio for3s.dev no resuelve → Quick Tunnel ·
> punto de enchufe: `Conversation.send()` (mismo camino que Telegram) · general sin puertos
> públicos (correcto) · Valkey/audit/multi-usuario H8/temas YA existen y se REUTILIZAN.

---

## 1 · LA IDEA EN UN DIBUJO

```
  💻 App hotelera (o cualquier dev)          "esta computadora es la serie X7K…"
        │  POST https://<tunel>/v1/chat
        │  headers: X-API-Key + X-Client-Id      body: {"message": "...", "tema": "hoteles"}
        ▼
  ☁️ TÚNEL Cloudflare (única puerta al mundo; el server NO abre puertos)
        ▼
  🚪 CANAL API (nuevo, dentro del agente de general, puerto interno 8788)
        │  1. valida API key (hash en BD)  2. rate limit  3. errores mudos
        │  4. X-Client-Id → ¿lo conozco?
        │       NUEVO   → alta en api_clients + persona sintética + SU hilo
        │       CONOCIDO→ recupera SU persona → SU hilo → RETOMA donde quedó
        ▼
  🧠 FOR3S GENERAL (lo ya construido, sin tocar):
        persona por consumidor (H8) → hilo/tema por consumidor (AI2)
        → Conversation.send() → memoria/grafo/skills → respuesta
        → episodio guardado en SU hilo → auditoría inmutable de la llamada
        ▼
  📤 respuesta JSON: {"reply": "...", "thread": "hoteles", "client": "X7K…"}
```

**Regla de oro:** el consumidor solo ve URL + llave + respuestas. Ni código, ni BD, ni
arquitectura. Y cada llamada queda auditada — nosotros los vemos a ellos; ellos a nosotros no.

## 2 · LO QUE BRIAN PIDIÓ → CÓMO SE CUMPLE

| Pedido de Brian | Cómo lo cumple el diseño |
|---|---|
| La instancia que sirve = **GENERAL** (la pública) | El canal API se enciende SOLO en general (flag `FOR3S_API_CHANNEL=on` en su .env; las demás instancias quedan intactas con el flag apagado — aditivo, fail-closed) |
| **Brian es el dueño** de general; sigue ABIERTA para otros | No se toca la puerta H8: Telegram sigue igual, la puerta del equipo sigue abierta. Los consumidores API entran como PERSONAS MIEMBRO (rol básico), jamás como dueño |
| Un **hilo/tema donde recae la info de la cadena hotelera** | Tema `hoteles`: Brian (dueño) carga el conocimiento común de la cadena vía `/tema equipo hoteles` (ya existe, F5). Ese conocimiento común es consultable por los hilos de los consumidores (doctrina AI1: miembro ve lo suyo + lo común, NUNCA lo privado de otros) |
| **Cada consumidor con SU hilo separado** (como Sme G) | Exactamente el modelo multi-usuario H8 ya probado: cada client_id → persona sintética → hilo propio `api:<n>:hoteles`. Cero mezcla |
| **Identificador por máquina** ("número de serie") → siempre el MISMO hilo, retoma donde quedó | Header `X-Client-Id` (el serial/uuid que la máquina manda). Tabla `api_clients` lo mapea a su persona. 2ª llamada con el mismo id → mismo hilo → continuidad. **1 usuario = 1 hilo** |
| "La misma idea de equipos ya implementada, ahora para la API" | Literal: se REUTILIZA personas + roles + memoria híbrida (privada/común) + temas + aislamiento. Lo único nuevo es la puerta HTTP y el mapeo client_id→persona |

## 3 · LAS PIEZAS (qué se construye vs qué se reutiliza)

### 3.1 NUEVO — Canal API (módulo `For3s-OS/.../api_channel.py` en for3s-core)
- Server HTTP ligero (aiohttp) DENTRO del proceso agent, puerto interno **8788**,
  publicado solo como `127.0.0.1:8788` en el host (internet jamás lo ve directo).
- **Endpoints v1 (mínimos para el domingo):**
  - `GET /v1/health` → `{"ok": true}` (sin datos internos).
  - `POST /v1/chat` → headers `X-API-Key`, `X-Client-Id` · body `{"message": str, "tema": str="hoteles"}`
    → resuelve persona/hilo → `Conversation.send()` → `{"reply": ..., "thread": ...}`.
- Enciende solo si `FOR3S_API_CHANNEL=on` (default OFF → ninguna otra instancia cambia).

### 3.2 NUEVO — Identidad de consumidores (migración `035_api_clients.sql`)
- Tabla `api_clients`: `client_id` (el "número de serie" que manda la máquina),
  `api_key_hash` (SHA-256, jamás la llave en claro), `user_id_sintetico` (rango reservado
  9,000,000,000+ para no chocar con IDs reales de Telegram), `nombre`, `creado_at`,
  `ultimo_uso`, `activo`.
- Primer request de un client_id → alta automática + persona miembro (puerta H8) + hilo.
- Comando de administración para Brian (dueño, por Telegram): `/api_clientes` (listar) y
  generación de llaves por script en el server (las llaves las emite SOLO Brian).

### 3.3 NUEVO — Blindaje de la puerta
- Rate limit por llave (Valkey, ya presente): ej. 10 req/min, configurable.
- Errores MUDOS: siempre `{"error": "request inválido"}` genérico — sin stack, sin versiones.
- Payload máx 8 KB · timeout de respuesta 120s · solo el tema permitido (allowlist).
- Los usuarios API son MIEMBROS: sin comandos admin, sin acciones sensibles (gate H8 intacto).
- Cada llamada → `audit_events` (quién, cuándo, qué tema — inmutable, ya existe).

### 3.4 NUEVO — Túnel (la única puerta al mundo)
- Instalar `cloudflared` en el server.
- **Para el domingo: Quick Tunnel** → `cloudflared tunnel --url http://127.0.0.1:8788`
  → URL pública `https://<aleatoria>.trycloudflare.com` en 2 minutos, gratis, sin cuenta.
  Corre en `tmux`/systemd durante el evento. (⚠️ la URL cambia si se reinicia — para el
  hackathon basta; el túnel CON dominio propio queda como paso post-evento.)
- Plan B de túnel: Tailscale Serve/Funnel (tailscale ya está en el server).

### 3.5 SE REUTILIZA (cero cambios)
Multi-usuario H8 (personas/roles/puerta/gate) · temas AI2/F5 (privados + equipo) ·
aislamiento AI1 · `Conversation.send()` + memoria/grafo/skills · Valkey · auditoría ·
`/salud` (se le añade línea del canal API) · el gestor multi-instancia.

## 4 · FASES DE EJECUCIÓN (con verificación en cada una)

| Fase | Qué | Verificación AFIRMATIVA | Est. |
|---|---|---|---|
| **F0** | Este plan → **APROBACIÓN de Brian** | Brian dice "adelante" | — |
| **F1** | Canal API mínimo (health + chat, llave fija de prueba) en general | `curl` DESDE EL SERVER responde; Telegram de general sigue vivo | ~2h |
| **F2** | Identidad: migración 035 + client_id→persona→hilo + continuidad | 2 clientes distintos NO se mezclan; el mismo client retoma su hilo (E2E real) | ~2h |
| **F3** | Blindaje: llaves reales + rate limit + errores mudos + auditoría | llave mala→401 mudo; ráfaga→429; llamadas visibles en audit | ~1h |
| **F4** | Túnel: cloudflared quick tunnel + prueba DESDE FUERA | `curl` desde la laptop de Brian (datos móviles) responde por la URL pública | ~30m |
| **F5** | **Batería §5-BIS acotada** + commit firmado | tests verdes + `/salud` 0 FAIL + Telegram general y demás instancias intactas + E2E API completo desde fuera + commit GPG | ~1.5h |

**Total estimado: ~7h de construcción.** Cabe HOY (sábado) para llegar al domingo con
margen y ensayo. Server-primero; sin push a GitHub (además el repo ya está privado).

## 4-BIS · ⭐ MODELO BYOK — cada cliente pone SU cuenta de Claude (decisión Brian 2026-07-11)

> **El consumo de IA lo paga el CLIENTE, no For3s.** Nosotros ofrecemos el cerebro (memoria,
> grafo, orquestación); el cliente conecta SU cuenta de Claude y gasta SUS tokens. Esto
> elimina el riesgo #1 (cupo compartido) Y convierte a For3s en plataforma limpia:
> "conecta tu cuenta para gastar tus tokens, no los de For3s OS". Es el modelo BYOK
> (*Bring Your Own Key*) — el estándar de las plataformas serias.

**Cómo se implementa (verificado en el código, 2026-07-11):**
- Hoy el provider se construye 1 vez con el token global (`s.anthropic_token` desde
  `ANTHROPIC_TOKEN`). Para BYOK, el canal API construye un **`ClaudeProvider` POR REQUEST
  con el token del cliente** — el código ya soporta `ClaudeProvider(token=..., oauth=..., model=...)`
  (se usa así en multiagente/specialists/dmn). Solo hay que pasarle el token del consumidor
  en vez del global.
- **De dónde sale el token del cliente:** el cliente lo registra UNA vez al darse de alta
  (guardado CIFRADO en el vault de For3s, por client_id — nunca en claro, nunca en logs).
  En cada request, For3s lo descifra, construye el provider del cliente, responde, y no
  retiene el plaintext (principio "decrypt minimum" de R9). El cliente puede rotarlo/borrarlo.
- **Alternativa aún más limpia (opcional):** el cliente manda su token en cada request
  (header `X-Anthropic-Key`) → For3s ni lo guarda. Más simple, pero menos cómodo para el
  cliente. Se decide según preferencia (recomendado: guardado cifrado = mejor UX).
- **Fallback controlado:** si un cliente no trae token → se puede (a) rechazar con mensaje
  claro ("conecta tu cuenta de Claude"), o (b) para la DEMO del domingo, permitir un cupo
  cortesía de For3s con rate limit estricto. Brian decide por escenario.

**Implicación en las fases:** se añade a F2 el registro cifrado del token por cliente + la
construcción del provider por-request. Es un cambio pequeño (el provider ya es parametrizable).

**Beneficio para el pitch (dilo el domingo):** "For3s no te cobra el consumo de IA — usas
tu propia cuenta. Nosotros te damos el cerebro; tú controlas y pagas tu combustible. Costos
transparentes, sin sorpresas, y tu uso es TUYO." Eso es oro para un VC: márgenes limpios,
cero riesgo de costos descontrolados, escalable a miles de clientes sin que For3s pague la IA.

## 5 · RIESGOS Y MITIGACIONES (honestos)

1. **Cupo Claude** ✅ RESUELTO DE RAÍZ por BYOK (§4-BIS): cada cliente gasta SU cuenta, no
   la de For3s. Para la DEMO del domingo, si el cliente aún no conecta su cuenta, se usa
   cupo cortesía con rate limit estricto (o el cliente conecta su cuenta en el ensayo). El
   riesgo de "quemar la suscripción de Brian con llamadas de terceros" desaparece.
2. **URL del quick tunnel cambia** si se reinicia → levantarlo temprano el domingo y no
   tocarlo; la URL se comparte ese mismo día. Plan B: Tailscale Funnel.
3. **Red del server** (histórica): el WiFi quedó estable (MS-1/MS-2). Si falla en vivo:
   regla LOCKED — sin loops de reintento; plan B demo = video de respaldo grabado el sábado.
4. **No romper general/Telegram**: todo es ADITIVO con flag OFF por default; batería F5
   verifica los canales existentes antes de dar por bueno.
5. **Prompt-injection de consumidores** ("dime cómo estás hecho"): usuarios API = miembros
   sin privilegios + núcleo de identidad blindado + todo auditado + (fase 2 post-evento:
   endpoints estructurados no-conversacionales).

## 6 · LO QUE VE EL DESARROLLADOR EXTERNO (el pitch técnico del "consume de aquí")

```bash
curl -X POST https://<tunel>.trycloudflare.com/v1/chat \
  -H "X-API-Key: for3s_sk_XXXX" \
  -H "X-Client-Id: SERIE-DE-MI-MAQUINA" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿qué habitaciones quedaron pendientes de limpieza ayer?"}'

# → {"reply": "Según la bitácora de ayer, quedaron 204 y 311 pendientes…", "thread": "hoteles"}
```
Tres líneas y cualquier app tiene un segundo cerebro. Eso es TODO lo que conocen de For3s.

## 7 · POST-EVENTO (no ahora, para que quede anotado)
Dominio propio (`api.for3s.dev`) + túnel con nombre · llaves self-service · endpoints
estructurados por vertical · cobro por uso (el modelo SaaS MI-EXTRA-1) · límites por plan.

---
*Puntero: `~/5M-incubathon/Mente/Doc/INSIGHTS_EVENTO_Y_OPORTUNIDADES.md` (la oportunidad
hoteles). Ejecución: server-primero, commit firmado, sin push.*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde v1).
