# FASE PRE-TESTERS / DISTRIBUCIÓN — Plan Maestro

> **Qué es:** plan de obra para pasar de "For3s corre solo en el servidor de Brian" a
> "un tester lo replica en SU máquina y nos ayuda a encontrar lo que no vemos".
> Activa el Bloque 3 (Producto Distribuible, P1-P10) + 2 piezas nuevas: INVENTARIO del
> sistema + IDENTIDAD única de For3s (sin nada personal de Brian).
>
> **Método LOCKED (Brian 2026-06-26):** ir POCO A POCO, componente por componente —
> identificar → debatir → decidir COMPORTAMIENTO y ORDEN de cada uno → siguiente.
> Las preguntas se dan como TEXTO (incisos + recomendación), Brian responde por escrito
> (las ventanas de pregunta le tapan la lectura). NADA de código hasta cerrar el debate.
>
> **Decisiones LOCKED de marco (Brian 2026-06-26):**
> - Fase Pre-Testers = Bloque 3 + inventario + identidad.
> - Empezar por el INVENTARIO (qué tengo y cómo está construido).
> - Instalador v1 = LOCAL con docker-compose (dominio install.for3s.dev + landing pública
>   = etapa 2, no ahora).

---

## 1. INVENTARIO REAL DEL SISTEMA (foto 2026-06-26, del código y BD vivos)

### 1.1 Código — 44 módulos, ~12.700 líneas (`packages/for3s-core/src/for3s_core/`)

| Grupo | Módulos | Función |
|---|---|---|
| Núcleo/infra | config · db · crypto · secret_store · audit · cli | arranque, BD, cifrado KEK, auditoría |
| Cerebro/LLM | llm · agent · conversation · modelos · tool_loop | hablar con Claude, el turno, herramientas |
| Memoria (H5/H6) | memory · embeddings · kg · consolidator · microglia · relevance | semántica, grafo AGE, consolidación, olvido |
| Canal | telegram_channel (2606 líneas, el mayor) · md_html · tiempo | Telegram + render |
| GitHub/web | mcp_client · gh_ficha · subbloques · web_fetch · multimodal · sandbox · cache | leer/escribir GitHub, web, archivos |
| Equipo (H8) | equipo · multiagente · specialists · cost_control · concurrency · handoff | multi-agente + multi-usuario |
| Perfil/hilos | perfil · temas · hilo_status | quién es cada quien, temas |
| APRENDE (H10-12) | skills · governor · aprende | skills + freno + motor |
| SUEÑA (H9) | dmn · dmn_tasks | trabajo en idle |
| PLANEA (H10-P) | confidence | metacognición |
| Worker (H6) | tasks · backup | jobs nocturnos |
| Versión | version | self-awareness |

### 1.2 Base de datos — 23 tablas, schema v22, 22 migraciones numeradas
`audit_events · sessions · episodes_events · secrets · gh_resources · gh_files ·
consulted_files · consulted_web · equipos · equipo_miembros · solicitudes · temas ·
corridas_equipo · corrida_reportes · hilo_status · perfil_usuario · skills ·
governor_estado · governor_bloqueos · dmn_corridas · dmn_estado · dmn_propuestas ·
schema_version`
Migraciones: 001_inicial → 022_dmn_propuestas (se aplican en orden por número).

### 1.3 Servicios e infra (lo que corre hoy)
- **2 servicios systemd:** `for3s-telegram` (bot) + `for3s-worker` (jobs Arq nocturnos).
- **Infra base:** PostgreSQL 16 (+ Apache AGE + pgvector) · Valkey · Docker.
- **Contenedores hoy:** github-mcp-server + 4 de demo (alpine) + (render Playwright para web).
- **Deps Python:** asyncpg · cryptography · httpx · python-telegram-bot · rich · (uv build).

### 1.4 Configuración (lo que un tester tendría que llenar)
`ANTHROPIC_TOKEN` · `DATABASE_URL` · `TELEGRAM_BOT_TOKEN` · `FOR3S_AUTH_MODE` ·
`FOR3S_MODEL` · `FOR3S_OWNER_SESSION` · VALKEY_HOST/PORT/DB · FOR3S_MICROGLIA_CONFIRMAR ·
(flags DMN/autogen).

### 1.5 Lo que YA existe de distribución (hallazgo) — y su estado real
- **`install.sh`** (raíz del repo): esqueleto de 13 líneas. Solo instala `uv` y dice
  "el installer completo llega después". ⚠️ NO despliega nada aún + tiene comentario
  "patrón heredado de Hermes" → VIOLA la regla cero-refs-externas, hay que limpiarlo.
- **`docker/Dockerfile.workspace`**: Dockerfile suelto (probable sandbox del agente, P6).
- **`docker/render/`**: contenedor Playwright para web fetch (ya funciona, de H4).
- **NO hay docker-compose** ni Dockerfile del agente/postgres/valkey → la contenerización
  del sistema completo NO existe. Hoy corre con systemd directo en el server.
- También en el repo: carpetas `apps/`, `scripts/`, `src/`, `tests/` (revisar al tocar cada una).

---

## 2. DEBATE POR COMPONENTES (orden + comportamiento de cada uno)

### ✅ Componente 1 — LA BASE (contenedores + servicios) — DECIDIDO 2026-06-26

**Decisiones LOCKED (Brian):**
- **Todo en docker-compose, 4 servicios:**
  1. `postgres` → imagen con **AGE + pgvector ya incluidos** (no compilar nada en cada máquina).
  2. `valkey` → imagen oficial.
  3. `for3s-agent` → el bot.
  4. `for3s-worker` → los jobs nocturnos.
- **agent y worker = MISMA imagen, distinto comando** (build una vez, menos que mantener).
- El tester levanta TODO con un comando → máxima replicabilidad.

**Orden de arranque (comportamiento):**
```
1. postgres arranca → healthcheck READY
2. valkey arranca
3. for3s-agent: espera postgres READY → corre las 22 migraciones → arranca el bot
4. for3s-worker: espera postgres+valkey → arranca los jobs Arq
```

### ✅ Componente 2 — BASE DE DATOS + migraciones — DECIDIDO 2026-06-26

**Decisiones LOCKED (Brian):**
- **2.A = Migraciones automáticas al arrancar el agente.** El contenedor `for3s-agent`
  llama a `db.apply_migrations()` (función que YA existe) antes de levantar el bot: aplica
  solo las pendientes, en orden, idempotente. El tester no hace nada.
- **2.B = Imagen de Postgres con AGE + pgvector ya horneados.** Cero compilación en la
  máquina del tester (compilar AGE es la causa #1 de "no me arrancó"). Las extensiones se
  activan con CREATE EXTENSION en la migración 001.
- **2.C = Arranca VACÍO.** Solo el esquema (23 tablas), sin datos. Cada tester estrena su
  propio cerebro en blanco. Los datos de Brian (memoria, secretos, repos) NUNCA viajan en
  el paquete distribuible (privacidad + es lo correcto del producto). Ejemplos → README.

**Comportamiento:** el tester levanta el contenedor → Postgres arranca con extensiones ya
dentro → el agente corre las 22 migraciones solo → BD lista y vacía. Sin instalar ni compilar.

### ✅ Componente 3 — SECRETOS + WIZARD de instalación — DECIDIDO 2026-06-26

**Contexto LOCKED:** testers = desarrolladores que traen SUS propias API keys e instalan
For3s en su local. **El cifrado de la tabla `secrets` SE QUEDA** (decisión de Brian: le gusta,
permanece). Flujo del instalador = wizard interactivo tras `curl -fsSL install.for3s.dev | sh`.

**Decisiones LOCKED (Brian):**
- **3.A = El wizard GENERA una KEK única automáticamente** en la 1ª instalación, guardada en
  un archivo protegido del host del tester (ej. ~/.for3s/kek), FUERA de los contenedores/BD.
  Cifra la key de Claude en la tabla `secrets`. El tester no gestiona nada de KEK. El cifrado
  se mantiene 100% y la KEK queda separada de la BD (respeta el espíritu de la regla de oro).
  Para producción/clientes se mantiene el modo KEK-offline estricto.
- **3.B = Aviso de riesgo CON confirmación explícita** ("esto es riesgoso, bajo tu
  responsabilidad" → el instalador no avanza hasta aceptar).
- **3.C = El wizard pide (orden):** 1) aviso→aceptar · 2) nombre de su For3s OS · 3) API key
  de Claude (OBLIGATORIA) · 4) token de Telegram (OBLIGATORIO — la interfaz es Telegram).
  El **PAT de GitHub = OPCIONAL, como una integración** que se conecta después (si no lo pone,
  For3s arranca igual y la parte de GitHub queda desactivada, degrada limpio).
- Por detrás del wizard: genera KEK → levanta contenedores → crea tablas (22 migraciones) →
  configura todo solo. La key y el token quedan cifrados en `secrets`.

**Sub-punto resuelto:** la interfaz del tester ES Telegram (por eso el token es obligatorio).
Cada tester crea su propio bot de Telegram y mete ese token. (CLI local queda como vía
secundaria si se quiere, pero el camino principal = Telegram.)
⚠️ Matiz tras Componente 4: el PAT de GitHub es opcional (no todos tienen GitHub), PERO la
CAPACIDAD de GitHub-MCP/render SÍ viene instalada en todos (son base, ver Componente 4).

### ✅ Componente 4 — IMAGEN del AGENTE + WORKER — DECIDIDO 2026-06-26

**Contexto LOCKED clave (Brian):** las integraciones que lanzan contenedores (GitHub MCP,
render Playwright) NO son extras opcionales — son **BASE de For3s OS**, las construimos para
que TODO el público las tenga. Deben venir funcionando en cada instalación de tester.

**Decisiones LOCKED (Brian):**
- **4.A = Imagen COMPLETA que resuelve Docker-dentro-de-Docker (DinD).** For3s desde su
  contenedor lanza los contenedores de GitHub-MCP y render → la imagen y el compose deben
  soportarlo. NO es la slim mínima; incluye lo necesario para orquestar contenedores hijos.
- **4.B = Resolver DinD CON SEGURIDAD REFORZADA.** ⚠️ Brian reconoce que dar al contenedor
  acceso al Docker del host es PELIGROSO → se blinda (no se deja crudo). Es la decisión de
  seguridad más fuerte de esta fase. Al construir, el blindaje es PRIORIDAD #1:
  opciones a evaluar (rootless Docker / socket-proxy con allowlist de comandos / Sysbox /
  contenedores hijos con límites estrictos + sin privilegios). Cruza con el governor/Amígdala.
- **4.C = Healthchecks + arranque COMPONENTE POR COMPONENTE, en orden.** Si uno falla, NO se
  sigue con el siguiente (arrancar todo a la vez se rompe). depends_on: service_healthy en
  compose + reintento defensivo en el código. Materializa el orden del Componente 1.

⚠️ **DEUDA/RIESGO registrado:** el DinD seguro es el punto más delicado de toda la fase.
Requiere su propio mini-debate de seguridad al construir (qué mecanismo exacto de aislamiento).

### ✅ Componente 5 — EL INSTALADOR (curl|sh) — DECIDIDO 2026-06-26

**Contexto LOCKED clave (Brian):** el tester tiene una máquina **Linux LIMPIA — NADA
instalado** (ni Docker ni nada), solo Linux. El instalador debe dejarla lista de cero.
Esto activa P8 ("instalar programas") como parte central del instalador.

**El punto elegante del diseño:** como TODO va en contenedores (C1), en el HOST el
instalador solo necesita poner **Docker**; el resto (Postgres, Valkey, Python, código)
vive dentro de los contenedores → el instalador es simple: instala Docker → levanta compose.

**Flujo (de cero a corriendo):**
```
curl -fsSL install.for3s.dev | sh   (Linux limpio)
 1. ⚠️ aviso de riesgo + necesita sudo → aceptar
 2. detecta la distro
 3. INSTALA Docker + Compose (si falta)
 4. WIZARD: nombre · key Claude · token Telegram · PAT GitHub (opcional)
 5. por detrás: genera KEK → levanta 4 contenedores EN ORDEN → migraciones → cifra keys
 6. ✅ "Listo, tu For3s 'X' corre — escríbele en Telegram"
```

**Decisiones LOCKED (Brian):**
- **5.A = El instalador INSTALA Docker automáticamente** (máquina limpia, no solo verifica).
  Requiere sudo → se avisa en el paso de riesgo.
- **5.B = v1 soporta Ubuntu/Debian** (el propio entorno de For3s, fácil de probar de verdad).
  Otras distros → aviso honesto "llega pronto". Incremental.
- **5.C = Reescribir install.sh entero desde cero**, limpio, SIN referencias externas (hoy
  tiene "patrón heredado de Hermes" → fuera), con identidad propia. Nace alineado a la regla.

### ✅ Componente 6 — IDENTIDAD ÚNICA DE FOR3S — DECIDIDO 2026-06-26

**Contexto:** For3s necesita identidad propia, autónoma, comercializable — sin nada
relacionado a Brian — para distribuirse. Dos capas: (1) identidad del PRODUCTO (fija, la
marca "For3s OS") + (2) identidad de la INSTANCIA (el nombre que cada tester le pone en el
wizard + cómo se adapta por perfil/memoria).

**Decisiones LOCKED (Brian):**
- **6.A = Auditoría COMPLETA de todo lo distribuible** (código, FOR3S_ROLE, mensajes del bot,
  README, install.sh) → quitar/neutralizar cualquier referencia personal (Brian, Frutero,
  email, historia). Lo que queda en Mente OS (privado) NO viaja, ahí puede seguir su nombre.
- **6.B = Personalidad de producto NEUTRA con carácter propio** (segundo cerebro honesto,
  QA/código + universal) que luego se adapta por usuario vía perfil/memoria. NO en blanco.
- **6.C = La identidad/limpieza se cierra ANTES de cualquier cosa pública** (requisito previo
  al Componente 7 / repo público — una vez público, el nombre quedaría expuesto).

⚠️ Cruza con la regla LOCKED "cero referencias externas" y con [[project_founder_identity]].

### ✅ Componente 7 — REPO PÚBLICO + README + POST-INSTALACIÓN — DECIDIDO 2026-06-26

**Decisiones LOCKED (Brian):**
- **7.A = Repo público NUEVO y limpio**, separado del privado actual (fruterito101/for3s-os
  tiene historial con posibles refs personales/secretos viejos → NO hacerlo público). El
  privado = taller; el nuevo público = producto, solo lo distribuible ya auditado (C6).
- **7.B = README de producto enfocado:** qué es + qué hace (capacidades) + comando de
  instalación + requisitos (Ubuntu/Debian + API keys) + "¿y luego qué?". Conciso, para
  arrancar rápido. La doc técnica profunda va aparte / en Mente OS.
- **7.C = Guía de primeros pasos + KIT DE TESTER:** tras instalar → abre Telegram, /start,
  prueba [lista], reporta [link/formato]. Incluye QUÉ feedback se necesita (bugs, lo confuso,
  lo que no sirvió) — es el objetivo de la fase: "identificar lo que yo no puedo ver".

### ✅ Componente 8 — DESINSTALACIÓN LIMPIA (uninstall) — AÑADIDO 2026-06-26

**Contexto:** Brian preguntó "si el usuario quiere eliminar For3s OS, ¿borra todo de un
golpe?". Aclaración técnica importante: NO es un Docker grande con dockers chicos dentro —
son contenedores HERMANOS (agent/worker/postgres/valkey) agrupados por el docker-compose
(etiqueta de proyecto, no una caja física). Los hijos DinD (MCP/render) son efímeros.

**El problema:** `docker compose down -v` borra contenedores + datos + red, PERO NO borra:
(a) la KEK + config en `~/.for3s/` (viven en el host, fuera de Docker), (b) las imágenes en
caché, (c) Docker mismo. → Hace falta un uninstall que limpie TODO de un golpe.

**Decisión LOCKED (Brian 2026-06-26): añadir DESINSTALACIÓN LIMPIA al plan.**
- Un comando de uninstall hace, de un golpe:
  1. `docker compose down -v` → contenedores + volúmenes (BD/memoria) + red interna.
  2. borra `~/.for3s/` → la KEK 🔑 + config del host.
  3. (opcional, preguntando) limpiar imágenes en caché para liberar disco.
  4. NO desinstala Docker (es del sistema del tester; se avisa que quedó).
- Deja la máquina como antes de instalar For3s (salvo Docker).
- ⚠️ Avisar claro: "esto borra TODO — tu memoria, skills, conversaciones — irreversible".
  Cruza con la regla de backup (ofrecer export antes de borrar = mejora futura).
- Ubicación: parte del instalador (C5) — ej. `curl ... | sh -s uninstall` o un script
  `for3s-uninstall` que el instalador deja en el sistema. Se decide al construir C5.

---

## 🎉 DEBATE COMPLETO — los 8 componentes cerrados (2026-06-26)

C1 base (4 contenedores compose) · C2 BD (migraciones auto + AGE/pgvector horneados + vacío) ·
C3 secretos+wizard (KEK auto, cifrado se mantiene, aviso riesgo, nombre/Claude/Telegram +
GitHub opcional) · C4 imagen agent+worker (DinD CON seguridad, integraciones son base,
arranque por orden) · C5 instalador (Linux limpio → instala Docker, Ubuntu/Debian v1, script
limpio) · C6 identidad única (auditoría total, personalidad neutra de producto, antes de
público) · C7 repo público nuevo + README producto + kit de tester · C8 desinstalación limpia
(compose down -v + borra ~/.for3s/, deja la máquina como antes).

**SIGUIENTE:** construir, componente por componente con su testeo (orden de construcción en §5).
Diagrama de empaquetado visual → §6.

---

## 3. Las 2 piezas NUEVAS (no estaban en P1-P10)

- **Inventario del sistema** (§1) — ✅ hecho hoy, es el punto de partida.
- **Identidad única de For3s** — homogeneizar TODOS los textos de rol para que For3s tenga
  identidad propia, comercializable, SIN nada relacionado a Brian, siguiendo las reglas ya
  vistas (cero refs externas + honestidad). Cruza con FOR3S_ROLE (agent.py) y con P2 (repo).

---

## 4. Mapeo a lo ya documentado (no se pierde nada)
- Bloque 3 (P1-P10) en `PENDIENTES.md §"PRODUCTO DISTRIBUIBLE"` — esta fase lo ejecuta.
- Cruza con H16 PRODUCCIÓN (deploy/contenedores/networking) del mapa, pero v1 = LOCAL
  (sin Cloudflare/dominio/DR aún — eso es H16 producción real).
- Identidad ↔ regla [[CERO referencias externas]] + memoria de scope.

---

## 6. DIAGRAMA DE EMPAQUETADO (referencia visual oficial — aprobado Brian 2026-06-26)

> Cómo se ven los componentes en sus contenedores (cajas dentro de cajas + comunicación).
> NO es el código — es el mapa visual para verificar que la arquitectura está bien.

### Vista 1 — La máquina del tester (de afuera hacia adentro)
```
╔══════════════════════════════════════════════════════════════════════╗
║  💻  MÁQUINA LINUX DEL TESTER (Ubuntu/Debian, limpia)                  ║
║   ~/.for3s/kek  🔑 ← la KEK vive AQUÍ, en el host (fuera de Docker)    ║
║   .env / config  📄 ← nombre, refs a las keys                          ║
║  ┌──────────────────────────────────────────────────────────────┐   ║
║  │  🐳 DOCKER  (lo único que el instalador pone en el host)        │   ║
║  │   ┌─────────────────────┐      ┌──────────────────────┐       │   ║
║  │   │ 📦 for3s-agent       │      │ 📦 for3s-worker      │       │   ║
║  │   │  (el bot Telegram)   │      │  (jobs nocturnos Arq)│       │   ║
║  │   │  ── misma imagen ────┼──────┼──── distinto comando │       │   ║
║  │   │  (NO lanza Docker)   │      └──────────┬───────────┘       │   ║
║  │   └───────┬──────────────┘                 │                   │   ║
║  │   ┌ ─ ─ ─ ▼ ─ ─ ─ ─ ─ ─ ─┐  (v1.1, HERMANOS de red,           │   ║
║  │     📦 github-mcp · 📦 render   NO hijos — el agente se          │   ║
║  │   └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘   conecta, no los lanza)            │   ║
║  │           │       │                        │                   │   ║
║  │   ┌───────▼───────▼────────────────────────▼─────────┐        │   ║
║  │   │  📦 postgres (PG16+AGE+pgvector)   📦 valkey       │        │   ║
║  │   │  ← 23 tablas, cifradas             ← cache+cola    │        │   ║
║  │   └───────────────────────────────────────────────────┘        │   ║
║  │   🔒 todo se habla por la RED INTERNA de Docker (privada)       │   ║
║  └──────────────────────────────────────────────────────────────┘   ║
║   📱 El tester habla con su For3s por TELEGRAM (su propio bot)         ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Vista 2 — Quién habla con quién
```
   📱 Telegram (tester)
        ▼
   ┌──────────────┐   lee/escribe    ┌──────────────┐
   │ for3s-agent  │ ───────────────▶ │  postgres    │ (memoria, skills, todo)
   │  (el bot)    │ ◀─────────────── │  23 tablas   │
   └───┬───┬──────┘                  └──────────────┘ ▲
       │   │ cache                            ┌───────┴──────┐
       │   ▼  ┌──────────┐  encola jobs       │ for3s-worker │ (backup,
       │      │ valkey   │ ◀──────────────────│ (nocturno)   │  CLS, DMN)
       │      └──────────┘                    └──────────────┘
       │ lanza cuando necesita (DinD):
       ├──▶ 📦 MCP GitHub  · └──▶ 📦 render
   🔑 La KEK (host) descifra las keys cuando el agent las necesita
```

### Vista 3 — Orden de arranque
```
  curl | sh
   1️⃣ instala Docker
   2️⃣ wizard (nombre · Claude · Telegram · GitHub?)
   3️⃣ genera KEK 🔑
   4️⃣ ARRANQUE POR ORDEN (si uno falla, NO sigue):
        ① postgres ✅healthy → ② valkey ✅healthy →
        ③ for3s-agent: 22 migraciones → cifra keys → bot ✅ →
        ④ for3s-worker: jobs ✅
   5️⃣ "✅ Listo, tu For3s 'Nova' corre — escríbele en Telegram"
```

---

## 7. CONSTRUCCIÓN (orden LOCKED Brian: empezar por C6 identidad)

Orden de construcción decidido: **1) C6 identidad → 2) C1+C2+C4 contenedores →
3) C3+C5+C8 instalar/desinstalar → 4) C7 repo público.** (Lo limpio antes de lo público.)

### ✅ C6 — IDENTIDAD ÚNICA — CONSTRUIDO 2026-06-26 (limpieza TOTAL, opción Brian)
- **Auditoría:** 158 ocurrencias de refs personales clasificadas en 3 tipos: (a) `.venv`
  (terceros, no viajan, ignorar) · (b) `"brian"` FUNCIONAL (sesión del dueño: owner_session/
  SESSION_OWNER — NO se toca, rompería la memoria) · (c) ~149 comentarios de atribución.
- **Limpieza TOTAL** (Brian eligió opción 2): script `limpiar_identidad.py` (regex que
  protege líneas funcionales y neutraliza atribuciones en comentarios/docstrings) →
  **153 líneas limpiadas en 58 archivos**. "decisión Brian"→"decisión de diseño",
  "(Brian fecha)"→"(fecha)", "Brian"→"el dueño", etc. Backup previo del código hecho.
- **Rematado a mano:** migración 006 (BRIAN mayúsculas), ref a **Hermes** en aprende.py +
  install.sh (cero refs externas), ejemplos en tests, README reescrito (producto, sin nombre),
  ejemplo de IP en backup.py.
- **FOR3S_ROLE (lo que el agente DICE) = 0 refs persona.** README = identidad de producto.
- **VERIFICADO:** suite 132 passed · ruff OK · cero refs personales/externas en lo
  distribuible (salvo `"brian"` funcional de sesión, que es código no identidad) · bot activo.
- ⚠️ NOTA: `"brian"` sigue siendo la session_id del dueño en producción (cambiarla borraría
  su memoria). Se parametriza cuando se haga multi-tenant real. No afecta la distribución
  (cada tester tendrá su propia sesión).

### 🔄 C1+C2+C4 — CONTENEDORES — EN CONSTRUCCIÓN 2026-06-26

**⭐ CAMBIO DE DISEÑO CLAVE (idea de Brian — mejor que el DinD):** el agente NO lanza
contenedores. Las integraciones que lanzaban contenedores (GitHub-MCP, render) pasan a ser
**HERMANOS de red** declarados en el compose; el agente solo SE CONECTA a ellos. Esto
ELIMINA el riesgo del DinD (cero acceso al Docker del host) — más seguro Y más simple.
**Decisión LOCKED: Opción B** → v1 conteneriza el NÚCLEO (4 servicios = cerebro completo:
chat, memoria, skills, equipo, DMN, metacognición); GitHub/render llegan en **v1.1** como
hermanos de red (requiere convertir MCP stdio→HTTP + render a servicio HTTP).

**Construido y verificado:**
- ✅ `docker-compose.yml` — 4 servicios (postgres·valkey·agent·worker), red interna privada,
  volúmenes (for3s_pgdata/valkeydata), healthchecks + depends_on (orden: postgres→valkey→
  agent[migra+bot]→worker). `docker compose config` VÁLIDO.
- ✅ `docker/Dockerfile.postgres` — **CONSTRUIDA Y VERIFICADA**: apache/age:release_PG16_1.6.0
  + pgvector v0.8.0 compilado dentro. Confirmado: age--1.6.0 + vector 0.8.0 horneados (cero
  compilación en la máquina del tester). ⚠️ fix: faltaba ca-certificates para el git clone.
- ✅ `docker/Dockerfile.agent` — python:3.12-slim + uv + deps + pre-descarga BGE-M3 en build.
  SIN docker.io (ya no hay DinD). Imagen ~5-6GB por torch (la memoria real es core). El build
  completo (torch ~5GB, 10-20 min) se hará en la prueba E2E.
- ✅ `cli migrate` — nuevo subcomando: aplica migraciones y sale (lo usa el agent al arrancar,
  C2.A). Probado contra la BD real ("ninguna pendiente").
- ✅ `VALKEY_HOST/PORT` parametrizados por entorno (default 127.0.0.1 → en compose: 'valkey').

**✅ CERRADO con E2E REAL 2026-06-26:**
- Imagen del agente **construida completa** (torch 2.12.1+cu130 + transformers + BGE-M3 +
  for3s_core, todo importa). ⚠️ fix cazado: el `uv sync` instalaba en venv que Python no veía
  → cambiado a `uv pip install --system` con TODAS las deps reales.
- **E2E del compose de CERO** (Postgres limpio): postgres+valkey → healthy · extensiones
  `age 1.6.0` + `vector 0.8.0` activas · el agente corrió **las 22 migraciones solo**
  (`[1..22]`) → **23 tablas, schema v22** (idéntico a producción) · idempotente al reiniciar.
  El bot solo falló en el ÚLTIMO paso (token Telegram dummy rechazado = esperado, no di uno real).
- Producción (systemd) INTACTA — el compose vive aislado en su red, no tocó nada. Limpieza
  con `compose down -v` (probado: borra contenedores+volúmenes).
- ⚠️ **DEUDA registrada:** la imagen del agente pesa **16.2GB** (torch trajo TODO CUDA, inútil
  en CPU). Optimizar a torch-CPU bajaría a ~2-3GB → mejora importante antes de testers reales
  (descargar 16GB es mucho). Funciona, pero pesa. → añadir a PENDIENTES de la fase.

**🎉 Esto prueba que la distribución FUNCIONA de cero:** Postgres limpio + agente → BD
completa construida sola, sin intervención. Justo lo que viviría un tester.

### ✅ DEUDA imagen del agente — RESUELTA 2026-06-27 (decisión Brian: For3s COMPLETO)

El primer build dio **16.2GB** (torch con CUDA: ~14GB de libs nvidia inútiles en CPU).
- **Fix 1 — torch CPU-only** (índice https://download.pytorch.org/whl/cpu): 16.2 → 9.63GB
  (−6.5GB de CUDA que en CPU no se usa para NADA). Verificado: torch 2.12.1+cpu, cuda=False.
- **Decisión Brian (Opción 1): modelo BGE-M3 HORNEADO en la imagen** → For3s OS COMPLETO
  desde el primer arranque, cero esperas/descargas en runtime. El peso (9.63GB) no importa;
  la completitud sí. El modelo (~4.3GB safetensors) es peso irreducible si se hornea.
- **Imagen final: 9.63GB, COMPLETA y verificada:** torch-CPU + BGE-M3 horneado + todo el
  código importa (telegram·dmn·governor·confidence·memoria...). For3s entero, sin recortes.
- ⚠️ Bug de build cazado antes de testers: el `uv sync` instalaba en venv que Python no veía
  (imagen "exitosa" pero sin deps) → fix: `uv pip install --system` con TODAS las deps reales.

### ✅ C3+C5+C8 — INSTALADOR + WIZARD + UNINSTALL — CONSTRUIDO 2026-06-27

- ✅ **`install.sh`** (bash, una línea `curl|sh`): 1) aviso de riesgo + "acepto" (C3.B) ·
  2) detecta distro (Ubuntu/Debian v1, C5.B) · 3) instala Docker si falta (C5.A) ·
  4) clona el repo · 5) WIZARD: nombre + key Claude (oblig) + token Telegram (oblig) +
  PAT GitHub (opcional) (C3.C) · 6) genera .env (600) + password Postgres aleatorio ·
  7) `docker compose up -d --build` (orden lo maneja el compose, C4.C) · 8) "listo + cómo
  escribirle/ver logs/desinstalar". Sintaxis `sh -n` OK. Wizard probado: genera .env correcto.
- ✅ **`uninstall.sh`** (C8): confirma "borrar todo" → `compose down -v` (contenedores+datos) +
  borra `~/.for3s` (KEK+config) + opcional borrar imágenes (~10GB). Deja la máquina como antes.
  Sintaxis OK.
- ✅ **KEK reutilizada (3.A ya estaba):** `crypto.load_or_create_master_key` YA auto-genera
  `~/.for3s/master.key` (32 bytes, 600) si no existe → el wizard no la inventa. El compose
  monta `${HOME}/.for3s:/root/.for3s` en agent+worker para cifrar/descifrar. Compose válido.
- ⚠️ El install REAL de cero (instalar Docker en máquina LIMPIA) solo se prueba en una máquina
  limpia (en el server Docker ya está) → validado por sintaxis + lógica del wizard + diseño.

### ✅ C7 — REPO PÚBLICO + README + KIT DE TESTER — CONSTRUIDO 2026-06-27

- ✅ **7-I.A repo nuevo SIN historial:** paquete limpio preparado en `/tmp/for3s-public`
  (rsync de SOLO lo distribuible, excluyendo .git/.venv/.env*/.for3s/Mente/caches/*.bak/*.key).
  Listo para `git init` + primer commit. El historial privado (secretos/nombre) se queda en
  el repo taller. ⚠️ El `git push` real al GitHub público lo hace Brian (irreversible + sus
  credenciales) — el paquete queda preparado y verificado.
- ✅ **7-I.B .gitignore blindado:** cubre .env/.env.*/*.key/*.pem/.for3s/ (KEK) + Mente/ +
  *.bak + caches + datos locales. **VERIFICACIÓN DE SEGURIDAD pasada:** scan del paquete →
  cero secretos reales (los hits son tokens FICTICIOS de tests + el scanner del governor +
  docs de prefijos — todos benignos). Confirmado: .env/.for3s/Mente NO están en el paquete.
- ✅ **7-I.C TESTING.md (kit de tester):** guía con (a) instalar, (b) checklist de qué probar
  (arranque, /start, memoria, memoria-tras-reinicio, /aprende+/skills, "sabe cuándo no sabe",
  comandos, GitHub opcional, uninstall), (c) qué reportar (qué hacías/esperabas/pasó + entorno
  + logs + lo subjetivo), (d) dónde (GitHub Issues). README: link a TESTING + uninstall corregido.

---

## 🎉 FASE PRE-TESTERS — DISEÑO Y CONSTRUCCIÓN COMPLETOS (2026-06-27)

Los 8 componentes construidos y verificados. For3s OS pasa de "corre solo en el server de
Brian" a "un tester lo replica en su Linux con un comando". Resumen:
- C6 identidad limpia (cero refs personales/externas) ✅
- C1+C2+C4 contenedores (compose 4 servicios, Postgres+AGE+pgvector horneados, imagen agente
  completa 9.63GB torch-CPU, E2E migraciones, sin DinD = hermanos) ✅
- C3+C5+C8 instalador curl|sh (Docker auto + wizard + KEK auto) + uninstall ✅
- C7 repo público (paquete limpio verificado + .gitignore blindado + README + TESTING) ✅

**Lo que QUEDA (acciones de Brian, no código):**
1. `git push` del paquete `/tmp/for3s-public` a un repo público nuevo (con su cuenta).
2. (Etapa 2, diferida) dominio install.for3s.dev + landing pública (hoy: curl al raw de GitHub).
3. Probar el install REAL en una máquina Linux LIMPIA (lo único que no se puede probar en el
   server, donde Docker ya está) — idealmente el primer "tester" sea esa prueba en limpio.
4. v1.1: GitHub-MCP + render como hermanos de red (hoy núcleo sin ellos, Opción B).

> Estado: ✅ FASE PRE-TESTERS construida y verificada (8/8 componentes). For3s OS distribuible.