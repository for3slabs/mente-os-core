# 🧩 Plan detallado — Pieza C: conectores OAuth (la joya — "conecto y mi agente lo usa")

> **Pendiente madre:** Conectores self-service (`Alma/Vision_Conectores_SelfService_Panel_Agente.md`).
> **Método pieza por pieza** (Brian 2026-07-20). Pieza C = 4ª que se construye (tras E, A, B).
> **LA JOYA del pendiente.** Visión alineada + decisiones tomadas (Brian, 2026-07-20).
> Este plan → aprobar → construir. Proyectos: For3s OS (server) + sitio (`marca-personal`).

---

## 0 · Qué resuelve (visión alineada con Brian)

El corazón del pendiente: el usuario pica **"Conectar GitHub"** → OAuth del proveedor → su token
llega SOLO (sin pasar por Brian) → **su agente lo USA** cuando le pide algo de GitHub desde la web.
"Ya quedó, ya tengo integrada esta herramienta." GitHub end-to-end como patrón; los demás
conectores se replican después.

## 1 · Decisiones tomadas (Brian, 2026-07-20)

- **C-D1 · Alcance:** **GitHub end-to-end, 1 conector real** (patrón completo, no medio flujo).
- **C-D2 · Dónde vive el token:** **vault de la instancia** (SecretStore del canal API, como los
  BYOK de Claude), cifrado, ligado a `client_id = correo`. Coherente con "conectores en la instancia".
- **C-D3 · C INCLUYE resolver S3:** el canal API hoy usa `Conversation.send` PLANO, sin tools →
  aunque el usuario conecte su GitHub, el agente NO lo usaría por la web. C le da **tool-loop al
  canal API** con el token del usuario inyectado. Círculo cerrado: "el agente lo usa".

## 2 · Terreno investigado (2026-07-20) — el hallazgo que definió C

- **El MCP de GitHub autentica POR REQUEST:** `mcp_client.py` arma `headers={"Authorization":
  f"Bearer {pat}"}` en cada conexión. Hoy usa un PAT global (env `GITHUB_PAT` = el de Brian), pero
  el diseño YA soporta un token por-llamada → se puede inyectar el del usuario. ✅ viable.
- **El canal API (`_responder`) usa `Conversation.send` PLANO**, no `send_with_tools`. `send_with_tools`
  + `run_tool_loop` existen (los usa Telegram), pero el canal no los llama. **Este es el S3.**
- **SecretStore** (`secret_store.py`): `set_secret/get_secret(workspace, name)`, AES-256-GCM, por
  workspace. Los BYOK viven como `byok_<client_id>` en workspace `api`. Patrón: `gh_<correo>`.
- **Sitio:** ya hay infra OAuth+PKCE (`lib/demo/oauth.ts`, cookie httpOnly del verifier) — hecha
  para el OAuth de Claude (interno/prohibido), pero el PATRÓN PKCE se reusa para GitHub (legal).
- **ConnectorsPanel:** UI muerta (botones "Conectar" que no conectan). GitHub es el 1º a cablear.

## 3 · Contratos con otras piezas

- **C usa A+B:** la identidad es `client_id = correo` (A) por el hilo del canal (B). El token
  GitHub se liga a ese mismo correo. Cero identidad nueva.
- **C reusa el vault BYOK** (mismo SecretStore) y el **MCP GitHub** (mismo server, otro token).
- **C deja el patrón para D y más conectores:** el flujo OAuth→vault→uso es replicable (Drive,
  etc.). D (API keys f3k_) es distinto (no OAuth), pero comparte el panel self-service.

## 4 · Plan por fases

### FRENTE 1 — S3: tool-loop en el canal API (para que el agente USE herramientas por la web)

**C1 · El canal API corre el tool-loop con el token del usuario.**
- En `_responder` del canal, cuando el mensaje "huele a github/código" (reusar `huele_a_github`),
  usar `send_with_tools` en vez de `send`, construyendo el `GitHubMCPClient` con el **token del
  usuario** (leído del vault `gh_<client_id>`); si no tiene token conectado → sin tools (o aviso
  "conecta GitHub primero"). El resto de mensajes siguen por `send` plano (barato).
- *Investigar terreno:* ya hecho (§2). Reusar `run_tool_loop`/`send_with_tools` de Telegram.
- *Red:* usuario SIN GitHub conectado pide algo de GitHub → responde "conecta primero" (no rompe).
  Usuario CON token → el agente lee su repo. Otro usuario NO usa el token del primero (aislamiento).

**C2 · Salvaguarda de seguridad del tool-loop en el canal.**
- El tool-loop del canal debe respetar el aislamiento: el token que inyecta es SOLO el del
  `client_id` de ESA request (de la sesión, como en B). Writes de GitHub: decidir si el canal
  permite writes (Telegram las confirma con botón; el canal no tiene botón) → **v1 solo lectura**
  (read-only MCP), writes fuera de alcance de C (más seguro). *Red:* el canal nunca ejecuta un
  write sin confirmación.

### FRENTE 2 — el OAuth de GitHub (conectar de verdad)

**C3 · OAuth App de For3s en GitHub (registro, una vez).**
- Registrar una GitHub OAuth App (o GitHub App) con callback al sitio. Client ID/Secret en env del
  sitio (`GITHUB_OAUTH_CLIENT_ID/SECRET`). Scopes mínimos (repo read para v1). **Pregunta abierta:
  ¿en qué cuenta/org se registra la app?** (Brian decide — probablemente for3slabs o su cuenta).

**C4 · Flujo OAuth en el sitio (reusa el patrón PKCE existente).**
- `POST /api/demo/connectors/github/start` → genera state + guarda en cookie httpOnly → redirige a
  GitHub authorize. `GET /api/demo/connectors/github/callback` → valida state → intercambia code por
  token (server-side, con el client secret) → **manda el token al canal API** (`POST /v1/token` NO,
  ese es Claude; se necesita un endpoint nuevo `/v1/conector` o reusar SecretStore vía un endpoint)
  para guardarlo cifrado como `gh_<correo>`. El token va descifrado 1 vez por el túnel, el canal lo
  cifra en su vault. El correo sale de la SESIÓN (no del body).
- *Nuevo endpoint en el canal:* `POST /v1/conector` `{tipo:"github", token}` con X-Client-Id=correo
  → guarda `gh_<client_id>` en el vault (scope propio). Auth con la key demo. Fail-closed.
- *Red:* state inválido → 403; callback sin sesión → 401; token guardado cifrado (verificable).

**C5 · El panel refleja el estado REAL.**
- ConnectorsPanel: el botón GitHub "Conectar" abre el OAuth; tras conectar muestra **"Conectado"**
  consultando el estado real (endpoint `GET /v1/conector?tipo=github` con X-Client-Id → ¿hay
  `gh_<correo>` en el vault?). **Desconectar** (visión: quitar también es del usuario) → borra el
  secreto del vault. *Red:* conectar→Conectado; desconectar→vuelve a Conectar; estado por usuario.

**C6 · El pago: E2E "conecto y mi agente lo usa".**
- Usuario conecta su GitHub en el panel → va al Chat → "resume mi repo X" → el agente (por el
  tool-loop de C1, con SU token) lee el repo y responde. **Este es el círculo cerrado de la visión.**

## 5 · Batería (§5-BIS)
- Server: canal con tool-loop — usuario con token usa GitHub, sin token → aviso; aislamiento
  (token de A no lo usa B); read-only (sin writes sin confirmar). `/v1/conector` guarda/lee/borra
  cifrado. Sin regresión de Telegram (que ya usa tools) ni de NavigoX. Tests + ty/ruff. Tríada firmada.
- Sitio: build/lint. OAuth start→redirect; callback con state válido→token guardado; state
  inválido→403; sin sesión→401. Panel: Conectado/Desconectar real.
- E2E del pago (C6): conectar GitHub real → chat usa el repo. Con la web real.

## 5-BIS · CONSTRUCCIÓN (2026-07-20) ✅ + verificación

**FRENTE 1 (server, código For3s) — S3 resuelto:**
- `api_channel._responder`: si el mensaje `huele_a_github` Y el usuario tiene su token
  (`github_<client_id>` en el vault) → `send_with_tools` con `GitHubMCPClient(su_token, read_only)`.
  Sin token → `send` plano. Aislado: SOLO el token del client_id de esa request.
- Endpoint `/v1/conector` (POST guarda / GET estado / DELETE desconecta) — cifrado en el vault,
  scope `byok`, tipos lista-blanca (`github`). `SecretStore.delete_secret` nuevo (auditado).
- **E2E verde:** ciclo guardar→leer→borrar; **aislamiento** (A conecta, B no lo ve); gitlab→400;
  270 tests (+2), ruff ✅, ty sin diagnósticos nuevos (el de `_AgenteBYOK` es pre-existente).

**FRENTE 2 (sitio) — OAuth GitHub:**
- `lib/demo/githubOAuth.ts` (authorize URL + exchange code→token, secret solo server-side) +
  `for3sChat.ts` (guardar/estado/borrar conector) + endpoints
  `/api/demo/connectors/github/{start,callback,route}` (state CSRF en cookie httpOnly, correo de la
  SESIÓN) + `ConnectorsPanel` con estado REAL (Conectar/Conectado/Desconectar, GitHub live, resto
  placeholder) + i18n.
- **Verificado sin la app:** start sin credenciales→503 (degrada), sin sesión→401, estado→200
  {connected:false} (consulta el vault real del general). Build/lint verdes.

**⏳ Falta SOLO (Brian):** registrar la GitHub OAuth App en **fruterito101** (guía:
`marca-personal/Mente/Doc/GUIA_Registrar_GitHub_OAuth_App.md`) + pegar CLIENT_ID/SECRET en
`.env.local`. Con eso, C6 (el pago: conectar→chat usa el repo) se prueba end-to-end.

**🐛 Cazados:** `delete_secret` no existía en SecretStore → agregado. El error "sin github_token
en el vault" al arrancar el general es PRE-EXISTENTE (el general nunca tuvo PAT global; manejado
defensivo) — de hecho C lo vuelve irrelevante (cada usuario trae el suyo).

## 6 · Fuera de alcance de C
- Otros conectores (Drive/Canva/…) — se replican con el patrón de C. · Writes de GitHub por la web
  (v1 read-only). · API keys f3k_ self-service (D). · La app OAuth de cada proveedor más allá de GitHub.

## 7 · Riesgos vigilados
- **Aislamiento del token:** el tool-loop inyecta SOLO el token del client_id de la request (de la
  sesión). Si se confunde, un usuario usaría el GitHub de otro. FAIL-CLOSED, verificado E2E.
- **El client secret de GitHub:** solo server-side (sitio), nunca al navegador. El code→token se
  hace en el callback server-side.
- **Token en tránsito sitio→canal:** descifrado 1 vez por el túnel tailnet, el canal lo re-cifra.
- **S3 no debe romper Telegram:** el tool-loop del canal es additivo; el de Telegram no se toca.
- **Scopes mínimos:** repo read para v1; no pedir permisos de más (principio de menor privilegio).
- **Rate-limit / abuso:** el canal ya tiene rate-limit por cliente; el tool-loop hereda eso.

## 8 · Decisiones que Brian aprueba (plan → construir)
| # | Decisión | Nota |
|---|---|---|
| 1 | ¿Registrar la GitHub OAuth App en qué cuenta/org? | for3slabs o cuenta de Brian (C3) |
| 2 | v1 read-only (sin writes por la web) | recomendado por seguridad |
| 3 | Endpoint nuevo `/v1/conector` en el canal | para guardar/leer/borrar el token del conector |
| 4 | Orden: Frente 1 (S3/tool-loop) → Frente 2 (OAuth) | o al revés; propongo S3 primero (desbloquea el "usa") |

---

*Relacionado: `Alma/Vision_Conectores_SelfService_Panel_Agente.md` (§C) · piezas A (identidad) y B
(chat) ya listas · S3 (reportado en `Cuerpo/Ronda_Maestro_Puentes_C_D.md` §barrido) · memoria
`project_conectores_selfservice`.*
