# 🌉 Ronda de Diseño — FRENTE B: "El Puente de Mercado" (API + túneles + control + panel)

> **Qué es:** F0 del Frente B post-Incubathon — llevar el canal API de "demo que sobrevivió al
> Incubathon" a **PRODUCTO para clientes de pago**. Método: `ESTANDAR_Metodo_Fases_F.md`.
> **Origen:** Brian 2026-07-14 ("me gusta… analiza todos los bugs… dame una solución para los túneles").
> **Estado:** 🎉 **FRENTE B COMPLETO (F1→F6).** F1 `2bf4a99` · F2 `79b156d` · F3 `330b891` ·
> F4.a `1a058c4` · F4.b `2164376` · F4.c `292f8e8`+`5d5b3f9` · F4.e (panel Railway 4 capas)
> `1d50035`+`a6c5fd7` · **F5 carga `30ea6e1`** · **F6 estándar de datos `705e26e`**. Panel en
> producción (`for3s.vercel.app/for3s-admin`), estrenado por Brian. Server=GitHub(×2)=local
> sincronizados. **Total del Frente B: ~15 bugs cazados** (incl. 2 races de concurrencia que
> tocaban la línea roja del audit). **Siguiente frente lo marca Brian** (Ronda §5-bis de RETOMAR:
> C multi-canal · E confianza · o productizar NavigoX).

## ✅ F6 CERRADA — estándar de datos + borrado a petición (evidencia)

Bug #12 de la Ronda (pregunta de Brian: "¿cómo se trata la info? ¿hay un estándar?"). NO es código
nuevo mayormente, es **formalizar** — pero se construyó la pieza que faltaba para que el estándar
sea REAL, no aspiracional.
- **Doc `Doc/Estandar_De_Datos_For3s_v1.md`** (cara al cliente + checklist SOC2): qué datos toca
  For3s (uso/memoria/BYOK), cifrado en tránsito (TLS) y reposo (BYOK AES-256, KEK offline),
  aislamiento por cliente (identidad sintética 9e9+ · verificado), retención + borrado, audit
  inmutable, límites, y el **mapa de los 5 TSC de SOC2** (Security/Availability/Processing
  Integrity/Confidentiality/Privacy) con lo que YA se cumple vs futuro. Honesto por diseño.
- **`/v1/olvidar` construido** (commit `705e26e`): borrado A PETICIÓN self-service. El cliente con
  su key hace soft-delete de TODA su memoria (o un `{tema}`), devuelve turnos_borrados, auditado.
  **Aislamiento probado E2E:** cliente A borró sus 2 turnos → cliente B **INTACTO** (2 vivos);
  sin key → 401. Recuperable (deleted_at); purgado físico = ciclo nocturno (H6).
- **Futuro registrado:** cifrado at-rest de toda la BD · DPA formal · retención configurable ·
  política pública de privacidad. Nada urgente.

## ✅ F5 CERRADA — pruebas de carga + 2 bugs de concurrencia (evidencia)

Bug #10 de la Ronda ("medir en serio, cuántos al mismo tiempo"). Script `scripts/carga_f5.py`
(stdlib, 2 planos). Commit `30ea6e1`. **Informe completo: `Doc/Informe_Carga_F5.md`.**
- **Infra sólida:** 100% éxito hasta 200 concurrentes. Local ~1330 RPS techo (pico 3856); por el
  **túnel público ~465 RPS, 100% éxito hasta 100 concurrentes** (el túnel es el cuello de la infra).
- **LLM:** el techo lo marca el PROVEEDOR (como anticipó la Ronda): ~8-10 concurrentes/instancia
  = 100% éxito; a 12+ aparecen 529/rate transitorios de Claude (no bug nuestro). Latencia real de
  respuesta completa ~35-45s (sonnet razonando). Palancas de escala: BYOK + multi-instancia.
- **🐛 2 BUGS de concurrencia cazados POR la carga** (invisibles en uso normal, solo con escrituras
  simultáneas en la misma sesión): (1) **`record_turn`** — `MAX(seq)+1`+INSERT = race →
  UniqueViolation → 500 (40% éxito a 10 conc). Fix: seq dentro del `INSERT ... SELECT` + reintento.
  Verificado 20 conc = 100%. (2) **`audit.append`** — cadena hash se BIFURCABA bajo carga →
  "Audit chain ROTA" (154 eslabones, ¡la línea roja del proyecto!). Fix: `pg_advisory_xact_lock`
  serializa los append. Cadena reparada one-shot (con constancia) → verify_chain íntegra=True.
  Ambos re-probados bajo la MISMA carga sin reaparecer. **Siguen:** F6 estándar de datos.

## ✅ F4.e CERRADA — panel "Railway" del server: 4 capas (evidencia)

Pedido de Brian tras estrenar el panel: verlo tipo **Railway** (grafo de contenedores, uso en
vivo, entrar a un For3s y ver su cableado, control casi total). Construido POR CAPAS (aprobado):
- **C1 · Legible + vivo** (`d82d8e2`/`32a897d`): auto-refresh 10s (foco latiendo) + botón manual ·
  diccionario humano (`lib/servidorLabels.ts`: postgres→Base de datos, valkey→Cola, agent→El bot…)
  · contenedores agrupados por For3s con barras CPU/RAM. Backend enriquecido (rol/instancia/red/%).
- **C2 · Grafo Railway** (`4bfab34`): **`@xyflow/react`** (la de Railway). "Ver conexiones →" en
  cada For3s abre su grafo interno (bot al centro, BD/cola eje, aristas animadas en vivos), clic en
  contenedor → detalle (uso/imagen/red/puertos). Blindado el bug SSR de React Flow (dynamic
  ssr:false). Topología validada con foto REAL (general: 10 nodos, 9 edges, 0 huérfanos).
- **C3 · Control de contenedores** (`59b567a`/`2a87bf4`): reiniciar/parar/arrancar desde el detalle,
  con confirmación. `POST /contenedores/<n>/<accion>` docker + **lista negra dura** (nave nodriza
  Foresito 403) + existe(404) + lock(409) + verificación afirmativa + audit. E2E: intocable 403,
  fantasma 404, grafana reiniciado.
- **C4 · Servicios del host** (`b4ca6d1`/`1d50035`, la más delicada — Brian pidió start/stop real):
  reiniciar postgresql/valkey desde el panel vía `sudo systemctl`. `POST /servicios/<n>/<accion>` +
  **LISTA BLANCA** (`SVC_CONTROLABLES`) + docker/for3s-ctl/tailscaled **jamás** (aunque se lean) +
  **sudoers acotado** (`scripts/for3s-ctl-sudoers`: Cmnd_Alias, 6 comandos exactos, sin comodines)
  + verificación con reintento + audit. **⚠️ Infra host:** `/etc/sudoers.d/for3s-ctl` + unidad
  for3s-ctl SIN NoNewPrivileges/PrivateTmp + `FOR3S_CTL_SVC_CONTROLABLES` en ctl.env.
- **🐛 6 BUGS cazados probando** (Brian: "van a salir demasiados"): (1) topología del grafo — validada
  antes de UI · (2) SSR de React Flow rompe medidas → dynamic client-only · (3) sudoers con comandos
  en una línea NO daba NOPASSWD sin tty → Cmnd_Alias · (4) `NoNewPrivileges=true` de la unidad (mi
  endurecimiento de F4.b) bloqueaba `sudo -n` · (5) `PrivateTmp=true` rompía el timestamp de sudo ·
  (6) verificación afirmativa demasiado rápida (systemctl restart vuelve antes de 'active') → reintento.
- **Estado:** 218 tests server · ruff limpio · E2E real de las 4 capas por el tailnet · 5 servicios
  del host vivos tras las pruebas · clientes/waitlist limpios (solo NavigoX).

## ✅ F4.c CERRADA — el panel visual + waitlist pública (evidencia)

- **Panel `/for3s-admin`** en marca-personal (rama `panel-for3s-admin`, commit `e836453`, SIN
  merge): patrón demo-admin (wrapper server + cliente), noindex, tema claro/verde del sitio.
  El navegador de Brian habla DIRECTO al server por el tailnet (/adm + /ctl) — **en Vercel no
  vive ni un secreto ni un dato** (verificado con grep sobre HTML renderizado y bundle .next:
  0 fugas). Token solo en localStorage (logout lo borra). Secciones: Resumen (KPIs + barras SVG
  de llamadas/día con tooltip + latencias p50/p95 por cliente) · Clientes (alta con key UNA vez
  + estados con motivo + revocar con confirm TERMINAL + rotar + cuotas/scopes + logs) · Waitlist
  (filtros + contactar/descartar/CONVERTIR con alta prellenada) · Instancias (on/off real;
  foresito solo-terminal; general crítica con confirm).
- **`/for3s-os/acceso`**: formulario público de waitlist → POST directo al canal (sin backend
  en Vercel). Build + lint verdes (Next 16.2/React 19/Tailwind 4, reglas react-hooks nuevas).
- **🧪 SUITE DE FLUJOS COMPLETOS (`scripts/test-panel-flows.ts`): 41/41 pasos OK** — corre la
  MISMA lib de la UI contra el backend REAL: auth (2 tokens, admin≠ctl) · prospecto (sitio→
  dedupe→contactado→convertido; estado inventado rebota) · cliente completo (alta→**chat LLM
  real 200**→cuota=1→**429**→rotar→**key vieja 401**→suspender→**403**→reactivar→revocar
  TERMINAL→reactivar rebota 409) · instancias (flota, ciclo real mashe 6.7s/21.9s, foresito
  rebota 404) · errores (client_id basura 400, logs de inexistente = [], email inválido legible).
- **🐛 3 BUGS DE BACKEND cazados POR el panel** (commit `292f8e8`): (1) `/v1/waitlist` sin CORS —
  preflight 405 → el form del sitio moría al nacer en el navegador (curl no lo veía); fix con
  lista blanca FOR3S_API_CORS solo en ese endpoint. (2) canal público anunciaba `Server:
  Python/3.12 aiohttp/3.14.1` (fingerprinting) → `Server: for3s` en canal+admin. (3) for3s-ctl
  anunciaba `Python/3.x` → sys_version mudo. 206 tests server.
- **Hallazgo documentado (diseño F3, NO bug):** las llamadas RECHAZADAS (429/401/403) no se miden
  en api_consumo — el gate corta antes de registrar (medirlas retroalimentaría el rate). Mejora
  futura si se quiere visibilidad de abuso: tabla aparte de rechazos.
- **Para estrenarlo (Brian):** merge de la rama → deploy Vercel → abrir `/for3s-admin` desde una
  máquina del tailnet → pegar el token (está en `~/.for3s/general/.env` FOR3S_ADMIN_TOKEN; el de
  instancias en `~/.for3s/ctl.env`). En dev: `bun run dev` y localhost:3000 ya está en el CORS.

## ✅ F4.b CERRADA — for3s-ctl: instancias on/off desde el panel (cierra MI-EXTRA-2 ⭐)

- **Construido:** `scripts/for3s_ctl.py` (stdlib puro, host) — mini-agente HTTP de control de
  instancias como **systemd** (`scripts/for3s-ctl.service`, Restart=always, enabled). Superficie
  ENANA: `GET /ping` (sin token, /salud) · `GET /instancias` (estado real vía docker ps, regla de
  `for3s listar`) · `POST /instancias/<n>/encender|apagar` (corre EL GESTOR `for3s` — no reinventa).
  **NADA de borrar/crear/exec** (terminal a propósito). Cierra el pendiente "mini-agente HTTP".
- **Capas:** 127.0.0.1:8791 + serve `/ctl` tailnet-only · Bearer fail-closed tiempo-constante ·
  CORS estricto · whitelist dura (regex gestor + registro) · `FOR3S_CTL_PROTEGIDAS` · **Foresito
  visible pero control:false** (nave nodriza por terminal) · **general critica:true** (el panel
  avisa: apagarla tumba demo+admin, pero /ctl NO muere — es la vía de rescate) · lock por
  instancia (paralela → 409) · verificación AFIRMATIVA post-orden · salida docker muda ·
  actor saneado · audit append-only `~/.for3s/ctl-audit.log` + journald.
- **E2E real por el tailnet:** flota exacta (brian🟢/general🟢/jazz⚪/mashe⚪/foresito🟢-RO) ·
  **ciclo real mashe:** encender 7.1s (verificado docker ps) → apagar 12.1s (devuelta a apagada) ·
  2 órdenes en PARALELO → una ok/una 409 · fantasma 404 · borrar 404 · sin token 401 · CORS
  204/403 · **kill -9 → systemd revive <4s** · **negativa /salud:** stop → 🔴 502 (admin siguió ✅,
  checks independientes) → start → ✅ · /salud **87 checks 0 FAIL** · regresión total intacta ·
  10 tests nuevos (**205 total**) · ruff limpio · ty línea base.
- **Serve final:** `https://for3s.tail6749e5.ts.net:8443` → `/adm` (admin API) + `/ctl` (instancias),
  ambos tailnet-only; Funnel 443 (demo pública) intacto.
- **Nota honesta:** el toggle 1:1 de la demo del sitio (Vercel server-side) sigue NO-OP — Vercel no
  está en el tailnet; conectar ESO exigiría exponer /ctl a internet (decisión de Brian, no tomada).

## ✅ F4.a CERRADA — la puerta del panel: admin API (tailnet) + waitlist pública (evidencia)

- **Decisiones de Brian (2026-07-14, F4):** el panel VIVE en `~/for3s/marca-personal` (su sitio,
  Vercel, modo claro/verde) · conexión panel↔server por **Tailscale Serve HTTPS** (el navegador de
  Brian está en el tailnet — verificado: BrayanETH/brayan-eth) · waitlist con **endpoint público** ·
  instancias **control completo v1** combinando MI-EXTRA-2 + pendiente mini-agente HTTP.
- **Construido:** migración 041 (`api_waitlist`: nuevo→contactado→convertido|descartado, dedupe por
  email UNIQUE) · `api_waitlist.py` (registrar con rate por IP y GLOBAL contra BD + validación,
  fail-closed; listar; cambiar_estado auditado) · `POST /v1/waitlist` PÚBLICO en api_channel (sin
  key, mudo) · **`api_admin_http.py`**: puerta HTTP del panel, envolturas FINAS de api_admin/
  api_metering/api_waitlist (cero lógica duplicada) con Bearer token fail-closed + tiempo-constante,
  CORS estricto (for3s.ai), rutas con/sin prefijo `/adm`, `/ping` sin token para /salud ·
  `api_admin.editar` (cuotas/scopes) · `api_metering.serie/latencias/logs_cliente` (gráficas del
  panel) · compose: hermano `admin` OPT-IN (profile "admin", hoy solo general) en 127.0.0.1:8790 ·
  check "Plano admin (panel)" en /salud + alerta.
- **Infra:** `tailscale serve --bg --https=8443 --set-path=/adm http://127.0.0.1:8790` → **URL
  admin FIJA tailnet-only: `https://for3s.tail6749e5.ts.net:8443/adm`** (persistente; el Funnel
  público 443 intacto). Token/CORS/URL en `~/.for3s/general/.env` (FOR3S_ADMIN_*).
- **E2E real:** ping tailnet 200 · sin token 401 · clientes+series+latencias OK · waitlist por el
  Funnel público (dedupe sin duplicar, email inválido 400, rate 6º=429) · transición a contactado +
  audit (6 altas + 1 estado) · CORS bueno 204 / malo 403 · regresión canal (health 200, chat sin
  key 401) · **prueba negativa**: admin stop → /salud 🔴 502 → restaurado 200 · /salud 0 FAIL ·
  14 tests nuevos (195 total) · ruff limpio · ty línea base (12) · datos de prueba limpiados.
- **🐛 cazado antes de aplicar:** middleware de re-ruteo del prefijo /adm en aiohttp rompía
  `match_info` (re-resolver a mano no puebla la ruta) → sustituido por registro doble de rutas
  (con y sin prefijo), a prueba de versiones de `tailscale serve`.

## ✅ F3 CERRADA — cuotas + metering persistente (evidencia)

- **Construido:** migración 040 (tabla `api_consumo` append-only: cliente/tema/tokens/costo/byok/
  ms/estado + índice cliente+fecha · cuotas por cliente en api_clients) · `api_metering.py` punto
  único: `gate` (rate/min + cuota diaria req + cuota diaria tokens; BYOK no cuenta contra nuestro
  cupo pero SÍ se mide) + `registrar` (cada llamada, incl. error/timeout) + `resumen` (uso por
  cliente → panel F4) · api_channel usa el gate y registra el consumo real · 5 tests.
- **Mata 3 bugs de la Ronda:** #4 rate amnésico (memoria→BD, sobrevive reinicios) · #5 sin cuotas
  (cupo compartido blindado) · #7 sin metering (dato para facturar + panel).
- **🐛 cazados:** LLMResponse expone `cost_usd` (property), NO `costo()` — habría registrado costo
  0.0, corregido ANTES de aplicar. Código huérfano del rate viejo (deque/_hits/RATE_WINDOW)
  detectado por grep post-parche y limpiado.
- **E2E por la URL pública:** llamada real→200 + api_consumo con 5276/6 tokens, $0.0159, 2385ms ·
  cuota=2 → 3ª llamada 429 ("cuota diaria de llamadas agotada") · resumen() OK · 181 tests ·
  /salud 84 OK · 0 FAIL. Clientes de prueba limpiados.

## ✅ F2 CERRADA — control PRECISO de acceso (evidencia)

- **Construido:** migración 039 (estado activo→suspendido→revocado TERMINAL + motivo/quién/cuándo +
  api_key_hash sha256 + expiración + scopes) · `api_admin.py` + CLI (alta/suspender/reactivar/
  revocar/rotar/listar, cada transición al AUDIT inmutable) · `_autenticar` de 2 niveles en
  api_channel (demo = key compartida + id por header · **CLIENTE = key `f3k_` propia donde LA
  IDENTIDAD ES LA KEY**, no falseable) con gates expiración(401)/estado(403)/scope(403) · 12 tests.
- **🐛 BUG cazado (revocación rota por diseño):** `_cliente` filtraba `AND activo` → al no encontrar
  caía al ON CONFLICT que **RESUCITABA al cliente desactivado**. Ahora el estado manda ANTES de
  tocar persona/memoria. Regresión probada: suspendido con tier demo → 403.
- **E2E por la URL pública:** expirada→401 · viva→pasa · suspender→403 · reactivar→pasa · revocar→
  403 + reactivar RECHAZADO · bug-resurrección→403 · demo normal→200 (LLM real "OK") · audit 8
  transiciones · 176 tests · ty línea base · /salud 82 OK · 0 FAIL. Clientes de prueba limpiados.
- **📐 Panel F4 — referencia registrada** (Brian: "el panel de Godinez me encantó"): stack
  verificado = Next.js 16 + React 19 + Tailwind v4 + Convex + i18n + WaitlistForm. Nuestro panel:
  mismo stack de UI, Convex→nuestro Postgres, + lista de espera + uso por persona (ver §5 F4).

## ✅ F1 CERRADA — el puente de la demo con URL FIJA (evidencia)

- **Funnel habilitado por Brian** (link de admin) → `sudo tailscale funnel --bg 8788` →
  **URL FIJA PARA SIEMPRE: `https://for3s.tail6749e5.ts.net`** (config persistente en tailscaled,
  sobrevive reboots). Demo = general, como decidió Brian.
- **E2E real desde INTERNET:** /v1/health → 200 (83-114ms caliente; el 1er hit 14s = emisión TLS
  única) · /v1/chat sin key → 401 · puerto 8788 blindado en 127.0.0.1 (no LAN — el diseño aguantó).
- **Vigilancia:** check "Puente público (demo)" en salud_integraciones, env-gated
  (`FOR3S_API_PUBLIC_URL`, composes lo pasan a agent+worker) → health nocturno ALERTA si cae.
  **PRUEBA NEGATIVA hecha:** funnel off → 🔴 ConnectError detectado; restaurado → 200.
- **Scripts:** `~/tunel_demo.sh` (informa/verifica, no mata nada) · `~/tunel_hoteles.sh` DEPRECADO
  (era: quick tunnel + pkill fratricida).
- **Batería:** 170 tests · ruff · /salud general 80 OK · 0 FAIL · flota completa recreada
  (5 instancias unificadas; jazz/mashe actualizadas y devueltas a apagadas).
- 🐛 Bug menor cazado y documentado: `tailscale funnel` SIN sudo se cuelga en silencio
  (esperando elevación) — siempre con sudo.

---

## 1 · La visión en palabras de Brian (el contrato, 2026-07-14)

- *"Cloudflare está un poco complicado por lo que nos pasó cuando los estuvimos levantando."*
- *"Esta es una capa donde debemos —yo y tú— mantener un control MUY PRECISO de a quién le damos
  acceso y cómo lo quitamos."*
- *"NO porque se cayó el servidor se fue todo y se perdió todo — eso es IMPOSIBLE que nos pase.
  Si se le activa un túnel a alguien, ESE TÚNEL ES DE ÉL. Si se cae el servidor de For3s OS, ok,
  conexión inestable, pero NO le vamos a pasar otra vez links y URLs de nada. Eso es muy delicado —
  ya estamos en un punto de mercado y conseguir clientes."*
- *"Una capa capaz de TRAZABILIZAR todo proceso: API, cliente y administrador (nosotros)."*
- *"Considerar el USO de cada API, poner un LÍMITE, qué SÍ pueden hacer y qué NO se puede hacer
  si tienes API."*
- *"For3s GENERAL se queda como está — perfecto para las personas que buscan la DEMO. Ya pasando
  ese punto, levantamos uno más."*
- *"Saber cuántas personas pueden ocuparlo AL MISMO TIEMPO. Pruebas extensas: cuánto soporta
  realmente de tráfico entrante, puntos de latencia, cuellos de botella. Esto NO es un MVP —
  pensar como PRODUCTO."*
- *"¿Cómo se trata la información una vez consumiendo la API? ¿Hay un estándar?"*
- *"El flujo NavigoX me gustó (trazabilidad de cada proceso + encriptado → For3s) pero no está
  bien armado del todo — como producto deja que desear."* → futuro: formalizarlo.

## 2 · Terreno REAL (verificado en el server 2026-07-14)

**Lo que YA existe (canal API caja-negra, commits F1-F3):**
| Pieza | Estado |
|---|---|
| API HTTP sobre `general` (:8788) | ✅ funciona (cerró el pitch del Incubathon) |
| Identidad por máquina (`api_clients`, user_id 9e9+) | ✅ aislamiento de memoria ENTRE clientes (AI1) |
| BYOK (token Claude del cliente, cifrado en vault) | ✅ |
| Rate limit por cliente | ⚠️ EN MEMORIA (ver bugs) |
| Auditoría por llamada | ✅ base |
| Túnel | 🔴 QUICK tunnel (`trycloudflare.com`) — el frágil |

**El script actual (`~/tunel_hoteles.sh`) — la evidencia del dolor:** `pkill -f cloudflared` (mata
TODO túnel) → levanta quick tunnel → **URL ALEATORIA nueva en cada arranque** → grep de la URL para
compartirla a mano. Sin systemd, sin health-check, log en /tmp.

## 3 · 🐛 ANÁLISIS DE BUGS — todo lo que puede pasar (pedido explícito de Brian)

### 🔴 Críticos (algunos YA nos pasaron)
1. **URL efímera** — quick tunnel = URL nueva en CADA reinicio → re-pasar links a clientes
   (YA PASÓ; inaceptable en mercado). *El requisito #1 de Brian.*
2. **`pkill` fratricida** — el script mata TODOS los cloudflared: levantar el túnel de un cliente
   tumbaría el de los demás.
3. **Túnel huérfano** — no es servicio (systemd): reboot del server = túnel muerto hasta que
   alguien lo levante A MANO. Nadie se entera (sin check en /salud → mismo patrón del bug de
   "alertas mudas" que cazamos en H13).
4. **Rate limit amnésico** — vive en memoria del proceso: reinicio = contadores en cero; un
   cliente golpeado por el límite solo tiene que esperar a que reiniciemos. Y no se comparte
   entre workers/instancias.
5. **Sin CUOTAS reales** — rate limit por ventana ≠ límite de consumo: sin BYOK, un cliente puede
   quemarse el CUPO COMPARTIDO de la suscripción (¡el de las 5 instancias!) en un día.
6. **Revocación pobre** — `activo=false` existe pero: sin flujo formal (quién/cuándo/por qué),
   sin estados (activo→suspendido→revocado), sin re-activación auditada, y el túnel/URL sigue
   vivo aunque el cliente esté inactivo (superficie expuesta).

### 🟠 Serios
7. **Sin metering por cliente** — no hay tabla de consumo (llamadas, tokens, costo) → imposible
   facturar, detectar abuso o responder "¿cuánto usó el cliente X este mes?".
8. **Key de demo compartida por chat** — `FOR3S_API_KEY_DEMO` en .env: rotarla = re-pasar la
   nueva a todos (mismo problema de los links). Sin expiración, sin scopes.
9. **Sin permisos por key** — "qué SÍ y qué NO puedes hacer con API" no existe: toda key puede
   todo lo que expone el canal.
10. **Concurrencia desconocida** — el gestor de concurrencia (3 capas) protege del 429, pero
    NADIE ha medido: ¿cuántos clientes simultáneos? ¿latencia p50/p95? ¿cuello = LLM, BD, túnel?
11. **DoS superficial** — endpoint público con rate-limit débil; sin reglas WAF de Cloudflare
    (que el túnel nombrado SÍ permite configurar por hostname).

### 🟡 De producto/datos (la pregunta del "estándar")
12. **Tratamiento de la información sin política formal** — hoy REAL: TLS (túnel) + BYOK cifrado
    (KEK) + memoria aislada por cliente + audit inmutable. FALTA formalizar: retención, borrado a
    petición, anonimización, qué NO se guarda — el "estándar" que preguntó Brian (los estándares
    de la industria: cifrado en tránsito+reposo ✅ ya, minimización, DPA/acuerdo de datos, y el
    mapa SOC2 que YA tenemos de R9 como wedge).
13. **Flujo NavigoX sin productizar** — trazabilidad + encriptado→For3s funcionó pero fue
    artesanal; falta: contrato de API formal (spec), SDK/receta de integración, y onboarding
    repetible. (Registrado como FUTURO del Frente B, no fase de ahora.)

## 4 · 💡 LA SOLUCIÓN DE TÚNELES (la respuesta al requisito #1)

**Cloudflare NAMED TUNNELS (túneles nombrados) + dominio propio.** La diferencia de fondo:

| | Quick (hoy) 🔴 | Nombrado (propuesta) 🟢 |
|---|---|---|
| URL | aleatoria en cada arranque | **hostname DNS PROPIO, FIJO PARA SIEMPRE** (ej. `demo.api.for3s.xyz`) |
| Se cae el server | URL nueva → re-pasar links | **misma URL al volver** — el DNS apunta al túnel (UUID persistente), no a una IP |
| Identidad | nadie | credencial JSON persistente POR túnel ("el túnel es DE ÉL") |
| Arranque | a mano con script | **systemd** (`cloudflared service`) — sobrevive reboots |
| Control de acceso | ninguno | por hostname: WAF, rate-limit de borde, hasta Cloudflare Access |
| Revocar cliente | imposible sin tumbar todo | quitar SU hostname/túnel — los demás ni se enteran |

**Cómo queda la arquitectura propuesta (modelo híbrido demo/clientes):**
- **DEMO = `general`** (como dijo Brian): 1 túnel nombrado `demo.api.<dominio>` → general:8788.
  Key de demo con expiración y cuota chica. Para curiosos/prospectos.
- **CLIENTE DE PAGO = SU túnel**: al activar un cliente se crea SU túnel nombrado con SU
  credencial + SU hostname (`<cliente>.api.<dominio>`) apuntando a SU instancia (o a general
  con su key, según el plan). **"Ese túnel es de él"** — literal: revocarlo = borrar SU túnel y
  SU DNS, sin tocar a nadie. Si el server se cae, su URL lo espera al volver.
- **Cada túnel = servicio systemd** + check en /salud + alerta al dueño si cae (el canal de
  alertas que reparamos en H13).
- **⚠️ REQUISITO**: un DOMINIO en Cloudflare (~$10 USD/año). Sin dominio NO existe URL estable —
  es la pieza que falta (cruza con DIST-3 `install.for3s.dev`). → decisión de Brian.

## 5 · Fases propuestas (F1-F6)

- **F1 · Túnel nombrado + dominio (mata el bug #1-3):** comprar/conectar dominio a Cloudflare →
  túnel nombrado `demo.api.<dominio>` → general, como systemd + check /salud + alerta si cae.
  Verificación: reiniciar server → MISMA URL responde sola.
- **F2 · Control de acceso preciso (bugs #6, #8, #9):** estados del cliente (activo→suspendido→
  revocado, con quién/cuándo/porqué en audit) + keys con expiración/rotación + permisos por key
  (scopes v1: chat sí/no, memoria sí/no) + comandos de admin (y base del panel).
- **F3 · Cuotas + metering (bugs #4, #5, #7):** rate-limit PERSISTENTE (BD/valkey, no memoria) +
  cuota diaria/mensual por cliente (tokens y llamadas) + tabla de consumo por llamada (quién,
  cuándo, cuánto, costo) → el dato para facturar y para el panel.
- **F4 · Panel admin COMPLETO (web segura):** ver clientes/consumo/estado + gráficas + latencias +
  logs por cliente + activar/suspender/revocar + on/off por cliente/instancia. (Absorbe MI-EXTRA-2
  ⭐.) Acceso solo Brian (Tailscale plano admin, R10).
  **📐 REFERENCIA TECNOLÓGICA (Brian 2026-07-14: "el panel de Godinez me encantó"):** stack de
  `~/Frutero-Empresa/Godinez/godinez-ai` verificado — **Next.js 16 + React 19 + Tailwind v4 +
  Convex (realtime) + i18n + componentes por sección + WaitlistForm**. Nuestro panel: MISMO stack
  de UI (Next 16/React 19/Tailwind 4, componentes limpios) pero **Convex → nuestro Postgres**
  (self-hosted, privacidad — nada de datos de clientes en un tercero). Features pedidas por Brian:
  **lista de espera** (waitlist de prospectos) + **uso POR PERSONA**. Será diferente (otras cosas
  que analizar) pero esas tecnologías son las importantes.
- **F5 · Pruebas de carga (bug #10):** medir EN SERIO — clientes simultáneos, p50/p95 de
  latencia, cuellos (LLM vs BD vs túnel), y el número honesto de "cuántos al mismo tiempo".
  Con informe. (Ojo: For3s responde con LLM → la concurrencia real la marca el proveedor.)
- **F6 · Estándar de datos v1 (bug #12):** política formal de tratamiento (qué se guarda, cuánto,
  borrado a petición, BYOK, cifrado) — 1 doc para enseñar a clientes + checklist SOC2-wedge (R9).
- **FUTURO registrado (no fase):** productizar el flujo NavigoX (spec de API + SDK/receta +
  onboarding repetible) — "me gusta pero no está bien armado del todo".

---

## 6 · Decisiones de Brian (2026-07-14, vía AskUserQuestion)

| Decisión | Elección |
|---|---|
| Tenancy | **Híbrido**: demo compartida (general) + túnel PROPIO por cliente de pago |
| Límites | **BYOK OBLIGATORIO para clientes** (su gasto = su cuenta); demo con nuestra cuota chica + expiración |
| Panel v1 | **COMPLETO desde el inicio**: clientes, consumo, gráficas, latencias, logs por cliente, on/off |
| URL fija | "¿por qué dominios? busca alternativas y compara" → comparativo §7 abajo |

## 7 · 🔍 COMPARATIVO — alternativas para URL pública ESTABLE (pedido de Brian)

> **Por qué salió el "dominio":** el hostname público de un túnel NOMBRADO de Cloudflare exige
> una zona DNS TUYA en Cloudflare. El dominio no es branding — es el ANCLA del enrutamiento
> estable + WAF + hostname por cliente. Pero hay alternativas; comparadas con honestidad:

| Opción | Costo | URL fija | Hostname POR cliente | Controles de borde (WAF) | Veredicto |
|---|---|---|---|---|---|
| **A · Dominio + CF Named Tunnel** | ~$10 USD/**año** | ✅ para siempre | ✅ (`cliente.api.…` — revocación quirúrgica) | ✅ | **La de producto** — único costo real: $10/año |
| **B · Tailscale Funnel** (ya instalado; URL verificada: `for3s.tail6749e5.ts.net`) | $0 | ✅ | ❌ 1 URL por máquina (máx 3 puertos: 443/8443/10000) | ❌ | **Perfecta para la DEMO YA** · insuficiente para clientes (sin hostname propio, ancho de banda limitado, dominio "feo") |
| C · ngrok dominio estático | $8-10/**mes** ($96-120/año) | ✅ | ⚠️ pagando más | ⚠️ | Descartada: cuesta 10× el dominio AL AÑO |
| D · Front workers.dev + quick tunnel auto-actualizado | $0 | ✅ (el front) | ❌ | ⚠️ | Descartada: es un HACK — 2 piezas móviles y el quick sigue aleatorio detrás; reintroduce la fragilidad que queremos matar |
| E · VPS relay (frp/nginx) | $4-6/**mes** | ✅ | ✅ | manual | Descartada: más caro que el dominio + OTRO servidor que mantener |

**→ RECOMENDACIÓN (híbrida también aquí):**
- **HOY ($0): Funnel para la DEMO** — `https://for3s.tail6749e5.ts.net` fija, systemd-persistente,
  se configura en minutos. La demo deja de ser frágil YA sin gastar.
- **AL PRIMER CLIENTE DE PAGO ($10/año): dominio + túnel nombrado** — porque el requisito de Brian
  ("ese túnel es DE ÉL", revocación quirúrgica, control preciso) SOLO lo da el hostname por
  cliente, y eso solo lo da el dominio. $10/año contra un cliente de pago = redondeo.

**⏳ ESPERANDO:** OK de Brian al plan de URL (Funnel-ya + dominio-al-1er-cliente, o directo
dominio) + aprobación para arrancar F1.
