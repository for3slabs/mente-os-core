# 🧩 Plan detallado — Pieza D: API keys f3k_ self-service (tu For3s en tu app)

> **Pendiente madre:** Conectores self-service (`Alma/Vision_Conectores_SelfService_Panel_Agente.md`).
> **Método pieza por pieza** (Brian 2026-07-20). Pieza D = 5ª y ÚLTIMA (tras E, A, B, C).
> **Visión alineada + decisiones tomadas (Brian, 2026-07-20). Este plan → aprobar → construir.**
> Proyectos: For3s OS (server) + sitio (`marca-personal`). La más ACOTADA (motor ya existe).

---

## 0 · Qué resuelve (visión alineada con Brian)

Hoy las API keys `f3k_` las genera Brian desde `/for3s-admin` (+ Nuevo cliente). D pone eso en el
**panel del USUARIO**: pone un NOMBRE → se genera SU key, **tope 3 por persona**, revocables por él.
La key le da acceso PROGRAMÁTICO a su For3s (consumir el canal API en su código, como NavigoX):
"lleva tu For3s a tu app".

## 1 · Decisiones tomadas (Brian, 2026-07-20)

- **D-D1 · Propósito:** la key f3k_ = credencial de **consumo API** del usuario (integrar For3s en
  su producto). Distinta de la key de Claude (BYOK, pieza B) y de los conectores (C).
- **D-D2 · Dónde viven:** en `api_clients` del general, `client_id` derivado del correo con el
  **mismo `clientIdDeCorreo` del fix de aislamiento** (unicidad estable). Reusa `api_admin`.
- **D-D3 · Reglas:** solo pone NOMBRE · **tope 3 keys** · las revoca él mismo.

## 2 · Terreno investigado (2026-07-20)

- **`api_admin` ya tiene el motor** (Frente B): `generar_key()` (f3k_ + sha256), `alta(client_id,
  nombre, scopes)`, `listar(pool)`, `cambiar_estado(client_id, "revocado", motivo)`. La key plana
  se muestra UNA vez; solo se guarda el hash. Lo usa `/for3s-admin` hoy.
- **`clientIdDeCorreo`** (sitio, fix aislamiento): `u` + sha256(correo)[:24]. D lo reusa para
  ligar las keys al usuario. Un usuario = un prefijo de client_id; sus keys = `<prefijo>-<n>`.
- **Aislamiento:** la clave del bug ya resuelto — el usuario A jamás ve/revoca las keys de B.

## 3 · Contratos con otras piezas

- **D reusa A+B:** identidad por correo (A) vía `clientIdDeCorreo` (fix de B). Cero identidad nueva.
- **D reusa el motor api_admin** (Frente B) — no reimplementa generación/hash/revocación.
- **D es independiente de C:** las keys f3k_ (consumo API) ≠ conectores OAuth (herramientas). Ambas
  cuelgan del mismo correo pero son cosas distintas. D no toca C.

## 4 · Plan por fases

### D1 · Endpoint self-service en el canal: `/v1/miskeys`
- `GET /v1/miskeys` (auth key demo + X-Client-Id=correo hasheado) → lista las keys del usuario
  (nombre, hint/últimos, estado, creada) — NUNCA la key plana.
- `POST /v1/miskeys {nombre}` → si tiene <3 activas → `api_admin.alta` con
  `client_id = <prefijo_correo>-<slug_nombre>` → devuelve la key plana UNA vez. Si ya tiene 3 → 409.
- `DELETE /v1/miskeys {client_id}` → verifica que ESA key es del usuario (prefijo coincide) →
  `cambiar_estado(..., "revocado")`. FAIL-CLOSED: no puede revocar la de otro.
- *Investigar terreno:* ya hecho (§2). Reusa `api_admin`. *Red:* tope 3 (la 4ª→409); un usuario
  no lista ni revoca las de otro (prefijo); key plana solo al crear.

### D2 · El puente en el sitio: `/api/demo/general/keys`
- Endpoints del sitio (GET/POST/DELETE) que llaman a `/v1/miskeys` con `X-Client-Id` =
  `clientIdDeCorreo(sess.email)` (de la sesión, no del body). Reusa el patrón de `for3sChat.ts`.
- *Red:* sin sesión→401; el correo sale de la sesión.

### D3 · La UI: apartado "Mis API keys" en el panel
- En el shell (nueva sección o dentro de Perfil): lista de keys (nombre, estado, revocar) + campo
  "nombre" + botón "Generar". Al generar, muestra la key plana UNA vez con aviso "cópiala ahora, no
  se vuelve a mostrar" (como el panel admin). Diseño con `impeccable`, patrón de los otros paneles.
- *Red:* generar→aparece la key una vez; revocar→desaparece de la lista; tope 3 (botón se deshabilita).

## 5 · Batería (§5-BIS)
- Server: `/v1/miskeys` — crear (key plana 1 vez), listar (sin plana), revocar (solo la propia),
  tope 3 (4ª→409), aislamiento (A no ve/revoca las de B). Tests + ruff/ty. Sin regresión de
  `/for3s-admin` (que usa el mismo api_admin) ni de NavigoX. Tríada firmada.
- Sitio: build/lint. Endpoints con sesión→ok, sin sesión→401. UI: generar/listar/revocar/tope.
- E2E: usuario genera su key → la usa en `POST /v1/chat X-API-Key: f3k_...` → responde (su For3s).

## 5-BIS · CONSTRUCCIÓN (2026-07-20) ✅ + auditoría E2E

**Construido:**
- **D1 (server, tríada `cbf5d37`):** `/v1/miskeys` en el canal (GET lista / POST genera / DELETE
  revoca). Reusa `api_admin`. Aislamiento de propiedad por prefijo `<client_id>::key-` (el `::` no
  sale de `_limpiar_id` → nadie toca las de otro). Tope 3 activas. Colisión de nombres resuelta
  (client_id lleva sufijo `secrets.token_hex(4)`, no solo el slug). Key plana 1 vez.
- **D2/D3 (sitio, commit local `9f00442`):** `/api/demo/general/keys` (correo de la sesión →
  `clientIdDeCorreo`) + `ApiKeysPanel` (sección "API keys": generar/listar/revocar, tope 3,
  "cópiala ahora") + i18n. Fix de un cascading-render del useEffect (React 19, cazado por lint).

**Auditoría E2E (verde):** lista vacía → 2 keys mismo nombre no colisionan → **tope 3 (4ª→409)** →
**B no ve las de A** → **B revoca la de A → 403 "no es tu key"** → revocar libera cupo → **la key
CONSUME For3s de verdad** ("Hola desde mi key") → revocada→403 → sin regresión (5 clientes reales
intactos) → 0 errores nuevos (el "sin github_token" es pre-existente de C). Los 4 riesgos
(propiedad, tope, colisión, key plana) SÓLIDOS.

## 6 · Fuera de alcance de D
- Conectores (C) · el BYOK de Claude (B) · cuotas/rate por key (ya existen en el motor; D usa los
  defaults) · scopes avanzados (D da el scope estándar `chat`).

## 7 · Riesgos vigilados
- **Aislamiento de propiedad:** revocar/listar SOLO las del prefijo del correo del usuario.
  FAIL-CLOSED (nadie toca las de otro). Verificado E2E.
- **Tope 3 real:** contar SOLO las activas del usuario (revocadas no cuentan). La 4ª→409.
- **La key plana:** se muestra 1 vez (solo el hash se guarda). El sitio la reenvía al navegador
  UNA vez para que el usuario la copie; no se persiste en el sitio.
- **Colisión de nombres:** dos keys con el mismo nombre → el client_id incluye un sufijo único
  (no solo el slug del nombre) para no pisar `api_key_hash` de la anterior.

---

*Relacionado: `Alma/...Panel_Agente.md` (§D) · piezas A/B/C · motor `api_admin` (Frente B,
`project_frente_b_puente_mercado`) · `clientIdDeCorreo` (fix aislamiento) ·
memoria `project_conectores_selfservice`.*
