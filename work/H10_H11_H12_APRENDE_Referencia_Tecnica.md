# H10-H11-H12 "APRENDE" — Referencia Técnica Detallada

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/H10_H11_H12_APRENDE_Referencia_Tecnica.md → work/H10_H11_H12_APRENDE_Referencia_Tecnica.md (2026-07-30, ADR-029)

## Purpose

H10-H11-H12 "APRENDE" — Referencia Técnica Detallada


> **Propósito:** documento de obra de lo que SE CONSTRUYÓ en el ciclo APRENDE (skills
> auto-generables y gobernadas). Pensado para que Brian pueda **modificar H10/H11/H12 a
> detalle más adelante** sabiendo exactamente qué hay, dónde, y por qué. Es fiel al
> CÓDIGO VIVO en el servidor (verificado 2026-06-25, BD v20). NO es un resumen ejecutivo
> — es el plano.
>
> **Origen:** la "joya" de Hermes (skills auto-generables) adaptada a CÓDIGO PROPIO de
> For3s + el diseño LOCKED R6 (Meta-Orchestrator). Análisis previo:
> `docs/analysis/Analisis_LearningLoop_Hermes_para_For3s.md`. Plan de obra (vista alto nivel):
> `memory/archive/H10-H12_Plan_Maestro_APRENDE.md`. Diseño del governor: `work/Ronda_06_Pre_Code_Review_Detailed.md` §A.
>
> **Fecha de construcción:** H10, H11 y H12 hechos 2026-06-24/25. version.py = **v0.10.0**,
> HITO "H12 APRENDE". Bot + worker activos. Suite del proyecto: 132 passed / 4 skipped.

---

## 0. Mapa rápido (qué tocar para cambiar qué)

| Quiero cambiar… | Archivo | Símbolo |
|---|---|---|
| Cómo se ALMACENA/lee una skill | `for3s_core/skills.py` | `SkillStore`, `SkillInfo`, `normalizar_nombre` |
| Esquema de la tabla skills | `migrations/019_skills.sql` | tabla `skills` |
| El FRENO (scanner, frenos, kill switch) | `for3s_core/governor.py` | `SkillEcosystemGovernor`, `escanear`, `_PATRONES_PELIGROSOS` |
| Esquema del governor (estado + auditoría) | `migrations/020_governor.sql` | `governor_estado`, `governor_bloqueos` |
| El MOTOR (/aprende, auto-mejora, curación) | `for3s_core/aprende.py` | `aprender_de_conversacion`, `proponer_skill_auto`, `curar_skills` |
| Cómo el agente USA una skill (inyección) | `for3s_core/conversation.py` | bloque "2h) H10 SKILLS" (~línea 635) |
| Comandos Telegram + gate + disparador | `for3s_core/telegram_channel.py` | `on_skills`, `on_aprende`, `on_autogen`, `on_skill_gate`, `_auto_mejora_background` |
| Job nocturno de curación | `for3s_core/tasks.py` | `job_curar_skills`, `HORA_CURAR_SKILLS_UTC`, `WorkerSettings` |
| Versión/changelog visible | `for3s_core/version.py` | `VERSION`, `CHANGELOG[0]` |

**Ruta base del código (servidor `for3s`):**
`/home/brianweb3/for3s-os/packages/for3s-core/src/for3s_core/`

**Principio de separación (respetarlo al modificar):**
`skills.py` = almacén · `governor.py` = freno · `aprende.py` = motor. NO mezclar. El motor
LLAMA al governor y al store; el store y el governor no conocen al motor.

---

## 1. H10 — SKILLS (tener + usar) ✅

**Meta:** For3s puede TENER y USAR skills (recetas). Cimiento. NADA se auto-genera (eso es H12).

### 1.1 Tabla `skills` (migración 019, BD v19)

```
id            BIGINT IDENTITY PK
nombre        TEXT   -- slug normalizado, único por categoría
categoria     TEXT   DEFAULT 'general'
descripcion   TEXT   -- una línea (para el listado, carga progresiva)
contenido     TEXT   -- el SKILL.md COMPLETO (markdown)
tags          JSONB  DEFAULT '[]'
version       TEXT   DEFAULT '0.1.0'
lifecycle     TEXT   DEFAULT 'active'   -- active | stale | archived
provenance    TEXT   DEFAULT 'usuario'  -- usuario | auto   ⭐ clave de seguridad
pinned        BOOLEAN DEFAULT false     -- pinned se salta la curación
creada_por    BIGINT -- telegram_user_id (NULL = sistema/CLI)
veces_usada   INT    DEFAULT 0
ultimo_uso    TIMESTAMPTZ
creada_at     TIMESTAMPTZ DEFAULT now()
actualizada_at TIMESTAMPTZ DEFAULT now()
UNIQUE (categoria, nombre)
```
Índices: `idx_skills_activas` (parcial lifecycle='active'), `idx_skills_provenance` (provenance, lifecycle).

⚠️ La tabla se diseñó para TODO el hito (no re-migrar): `lifecycle`/`provenance`/`pinned`/
`veces_usada` ya estaban pensados para H11/H12.

### 1.2 `skills.py` — `SkillStore` (asyncpg, sin ORM)

| Método | Qué hace | Nota |
|---|---|---|
| `crear(nombre, contenido, *, categoria, descripcion, tags, provenance, creada_por)` | INSERT idempotente (upsert por `UNIQUE(categoria,nombre)`); devuelve `id` | ON CONFLICT actualiza contenido/desc/tags y fuerza `lifecycle='active'` |
| `listar(*, solo_activas=True)` | metadata sin contenido (carga progresiva, disciplina AI6) | devuelve `list[SkillInfo]`; defensivo (nunca rompe el turno) |
| `ver(nombre, *, categoria=None)` | skill COMPLETA (con `contenido`) como `dict` | sin categoría: la activa más reciente con ese nombre |
| `registrar_uso(skill_id)` | `veces_usada += 1`, `ultimo_uso = now()` | fire-and-forget; lo usado resiste la curación |
| `buscar_relevantes(texto, *, limite=3)` | match por palabras (≥4 chars) contra nombre/desc/tags vía regex `~` | ordena por `veces_usada DESC`; defensivo |

`normalizar_nombre`: slug seguro (NFKD → ascii → minúsculas → `[a-z0-9-]`, máx 64). ⚠️ usa
`unicodedata.normalize("NFKD")` para no perder acentos mal (bug histórico "Día"→"da").
Constantes: `PROV_USUARIO="usuario"`, `PROV_AUTO="auto"`.

### 1.3 El agente USA la skill — inyección en `conversation.py`

Bloque **"2h) H10 SKILLS"** dentro de `Conversation.send()` (~línea 635). Mismo patrón que
las otras inyecciones (memoria/grafo/perfil/version):
1. `SkillStore.buscar_relevantes(message, limite=2)` — ¿alguna skill aplica al mensaje?
2. Para cada una: `ver()` el contenido completo, recorta a **1500 chars**, `registrar_uso()`.
3. Inyecta un bloque al `contexto_final` con encabezado "SKILL(S) QUE APLICAN A ESTO
   (recetas reutilizables — sigue sus pasos…)".
4. **DEFENSIVO**: todo en `try/except` — si falla, el turno sigue sin skills.

### 1.4 Comando `/skills`

`on_skills` (telegram_channel ~1066): `/skills` lista (con 👤 usuario / 🤖 auto por
provenance); `/skills <nombre>` muestra el SKILL.md completo. En `_MENU_BASICO` (para todos).

---

## 2. H11 — GOVERNOR (el FRENO) ✅

**Meta:** el control que DEBE existir ANTES del motor (regla LOCKED R6 §A / Grafo §8.4).
Sin freno, no hay auto-generación. **Decisiones LOCKED (debate Brian 2026-06-25):**
scanner + 3 frenos reales + hooks honestos · scanner muy conservador (bloquea+avisa) ·
kill switch SOLO del dueño vía `/autogen`.

### 2.1 Esquema (migración 020, BD v20)

**`governor_estado`** (singleton por workspace, hoy 1: 'default'):
```
workspace    TEXT PK DEFAULT 'default'
autogen_on   BOOLEAN DEFAULT false   ⭐ KILL SWITCH. Default APAGADA.
cambiado_por BIGINT  -- telegram_user_id del dueño
cambiado_at  TIMESTAMPTZ DEFAULT now()
motivo       TEXT
```
Fila 'default' se inserta sola (ON CONFLICT DO NOTHING).

**`governor_bloqueos`** (append-only, auditoría de cada rechazo):
```
id BIGINT IDENTITY PK · workspace · freno (scanner|generacion|duplicado|activas|killswitch)
· motivo · skill_nombre · provenance · creada_por · creado_at
```
Índice: `idx_governor_bloqueos_fecha (creado_at DESC)`.

### 2.2 `governor.py` — constantes calibradas (v1 muy conservadora)

```python
MAX_NEW_SKILLS_AUTO_PER_DAY = 3   # FRENO 1 — techo auto-gen/día/workspace
MAX_ACTIVE_SKILLS = 100           # FRENO 5 — techo de complejidad
ENV_AUTOGEN_OFF = "FOR3S_AUTOGEN_OFF"  # flag de emergencia (si está, MANDA y apaga)
WORKSPACE_DEFAULT = "default"
```
⚠️ Para endurecer/relajar: cambiar estos números. R6 sugería 5/día y 100 activas; bajé
auto/día a 3 por conservadurismo v1. (R6 también define umbrales de los frenos 2/3/6 —
ver §2.5 hooks.)

### 2.3 El SCANNER (`escanear()` + `_PATRONES_PELIGROSOS`) — EL CORAZÓN

Función pura síncrona `escanear(contenido, *, nombre, descripcion) -> Veredicto`. Revisa
los 3 campos juntos contra ~17 regex. **FAIL-CLOSED**: si el escaneo lanza excepción,
devuelve `permitido=False` (la seguridad nunca se salta por un error). Reporta TODOS los
hallazgos (no se detiene en el primero).

Familias de patrones en `_PATRONES_PELIGROSOS` (lista de `(regex, etiqueta)`):
- **Destrucción:** `rm -rf`, `mkfs/dd/shred/wipefs`, fork bomb, `DROP/TRUNCATE`, `>/dev/sd*`, `chmod -R 777 /`.
- **Descarga+ejecución:** `curl|wget|fetch … | sh`, `eval/exec(base64|requests.get|urllib|fetch)`.
- **Exfiltración de secretos (CRÍTICO For3s):** `KEK/master_key/private_key/secret_store`,
  `.env/id_rsa/.ssh//credentials/secrets.*`, `ANTHROPIC_TOKEN/TELEGRAM_BOT_TOKEN/DATABASE_URL/sk-ant-`,
  `env|curl/nc/wget`.
- **Persistencia:** `crontab/systemctl enable//etc/cron/@reboot/launchctl/.bashrc/.profile/authorized_keys`,
  reverse/bind shell (`nc -e`, `/dev/tcp/`).
- **Prompt-injection:** "ignora … instrucciones anteriores" (es), "ignore all previous
  instructions / disregard system prompt / you are now DAN" (en), "revela tu system prompt".

⚠️ Para añadir patrones: agregar tuplas a `_PATRONES_PELIGROSOS`. Es la primera barrera y
la más importante. Muy conservador a propósito (un falso positivo bloquea algo inocente,
que el dueño puede crear a mano; un falso negativo deja pasar algo peligroso).

### 2.4 `SkillEcosystemGovernor` — métodos

| Método | Tipo | Qué hace |
|---|---|---|
| `autogen_permitida()` | kill switch | lee `FOR3S_AUTOGEN_OFF` (manda) y luego `governor_estado.autogen_on`. **Fail-closed**: si no puede leer, devuelve False. |
| `set_autogen(on, *, por, motivo)` | kill switch | upsert en `governor_estado`. Persistido. |
| `can_generate()` | **FRENO 1** | niega si kill switch off **o** ya hay ≥3 skills `auto` creadas hoy (`creada_at >= date_trunc('day', now())`). |
| `check_contradictions(nombre, categoria)` | **FRENO 4** | niega si ya existe skill activa con ese `(categoria, slug)`. v1 = exact-match; la versión semántica (pgvector) es trabajo futuro. |
| `active_budget_ok()` | **FRENO 5** | niega si hay ≥100 skills activas. |
| `should_explore()` | **HOOK F2** | neutro (devuelve permitido). Requiere scoring dopaminérgico (futuro). |
| `no_go_budget_ok()` | **HOOK F3** | neutro. Requiere reglas NO-GO (futuro). |
| `independent_eval(skill)` | **HOOK F6** | neutro. Requiere sandbox de skills (futuro). |
| `evaluar_skill_nueva(*, nombre, contenido, categoria, descripcion, provenance, creada_por)` | **GATE ÚNICO** | puerta de entrada (ver §2.6). |
| `_registrar_bloqueo(...)` | auditoría | INSERT en `governor_bloqueos` (defensivo). |
| `health_report()` | observabilidad | `EcosystemHealth`: autogen_on, active_skills, new_skills_auto_today, bloqueos_today, veredicto. |

`Veredicto` (dataclass): `permitido`, `freno`, `motivo`, `detalle` (hallazgos del scanner).
`__bool__` = `permitido` → permite `if veredicto:`.

`EcosystemHealth.veredicto`: **FROZEN** (autogen off) · **THROTTLED** (techo diario o
activas alcanzado) · **HEALTHY**.

### 2.5 Hooks honestos (frenos 2/3/6) — NO son frenos falsos

Son puntos de extensión EXPLÍCITOS del R6 §A.6 ("envuelve, no reescribe"). Hoy devuelven
veredicto neutro porque la maquinaria que los activa NO existe aún:
- **F2 should_explore** (anti lock-in, epsilon-greedy 10%) → necesita scoring de skills.
- **F3 no_go_budget_ok** (techo/expiración de reglas NO-GO) → necesita reglas NO-GO.
- **F6 independent_eval** (golden set + 2ª opinión, no juez-y-parte) → necesita sandbox.

⚠️ Cuando se construyan esas piezas, llenar estos métodos (no crear nuevos). R6 §A.3 tiene
los umbrales originales: EXPLORATION_EPSILON=0.10, NO_GO_REVIEW_INTERVAL_DAYS=30,
NO_GO_FALSE_POSITIVE_THRESHOLD=0.2, NO_GO_MAX=50, CONTRADICTION_SIMILARITY_THRESHOLD=0.85.

### 2.6 Flujo del gate único `evaluar_skill_nueva()`

```
1) SCANNER (SIEMPRE, usuario o auto). Si falla → registra bloqueo + niega.
2) Si provenance == 'auto':
     can_generate()      (kill switch + techo diario)   → si niega: registra + corta
     active_budget_ok()  (techo de activas)             → si niega: registra + corta
3) check_contradictions() (duplicado, para TODOS)        → si niega: registra + corta
4) permitido=True
```
**PROVENANCE es la clave:** las skills `usuario` solo pasan scanner + duplicado (el dueño
tiene autoridad, no le aplicamos techos de auto-gen). Las `auto` pasan los frenos completos.

### 2.7 Comando `/autogen` (solo dueño)

`on_autogen` (telegram ~1180): `/autogen on|off` cambia el kill switch (`set_autogen`);
`/autogen status` (default) muestra el `health_report` con emoji 🟢/🟡/🔴. En `_MENU_ADMIN`.

---

## 3. H12 — MOTOR (/aprende + auto-mejora + curación) ✅

**Meta:** For3s crea y mejora skills solo. SOLO tras H11. **Decisiones LOCKED:** P1→P2→P3
por riesgo · fuente = la conversación actual · P2 construida pero tras el kill switch OFF.
Todo el motor vive en `aprende.py` (no toca skills.py ni governor.py).

### 3.1 Constantes (`aprende.py`)

```python
TURNOS_FUENTE = 12          # turnos recientes que se le dan al LLM como fuente
MAX_TOKENS_DESTILAR = 1200  # tope de la destilación (una skill es corta)
DIAS_ACTIVE_A_STALE = 30    # P3: auto activa sin uso 30d → stale
DIAS_STALE_A_ARCHIVED = 90  # P3: auto stale sin uso 90d → archived
```

### 3.2 Destilación (interno, compartido por P1 y P2)

- `_INSTRUCCION`: prompt que pide al PROPIO For3s destilar UNA skill y responder **SOLO un
  JSON** `{vale, nombre, categoria, descripcion, tags, contenido}` (o `{vale:false, motivo}`).
  El SKILL.md va dentro de `contenido` (título + "## Cuándo usarla" + "## Pasos").
- `_extraer_json(texto)`: tolerante a fences ```` ```json ````; si falla, busca el primer
  `{...}` balanceado (`_primer_objeto`).
- `_material_de_turnos(turnos, *, foco)`: arma el bloque MATERIAL (roles Usuario/For3s) +
  un foco opcional del dueño.
- `_destilar(provider, material)`: llama `provider.complete(prompt, system="", max_tokens=
  MAX_TOKENS_DESTILAR)` en `asyncio.to_thread` (complete es síncrono/httpx). **OAuth-safe**:
  instrucción en el user message, `system=""` (regla 429-system de For3s). Devuelve dict o None.
- `_guardar_con_governor(pool, datos, *, provenance, creada_por)`: valida nombre/contenido →
  `governor.evaluar_skill_nueva(...)` → si pasa, `SkillStore.crear(...)`. Devuelve
  `ResultadoAprende(ok, mensaje, skill_id, nombre, categoria, requiere_gate)`.

### 3.3 P1 — `/aprende [foco]` (manual del humano)

`aprender_de_conversacion(pool, provider, session_id, *, creada_por, foco="")`:
1. `memory.load_history(pool, session_id, last_n=12)` — los turnos del hilo actual.
2. `_destilar(...)` → si no hay JSON válido o `vale:false`, reporta sin guardar.
3. `_guardar_con_governor(..., provenance="usuario")` — **el scanner SIEMPRE corre** (una
   charla puede contener un secreto), pero sin techos de auto-gen (lo pidió un humano).

**Telegram:** `on_aprende` (~1143). En `_MENU_BASICO` (para TODOS los autorizados, también
miembros — pueden enseñar recetas de su trabajo). Usa `_sesion_de(user)` (hilo por usuario +
tema, #6/AI2) y `creada_por=user.id`. Verificado con LLM real: destiló 'deploy-bot-for3s-server'.

### 3.4 P2 — auto-mejora en background (tras el kill switch OFF)

`proponer_skill_auto(pool, provider, session_id, *, creada_por)`:
1. **Freno duro de entrada:** `governor.can_generate()` — si /autogen OFF, **NI llama al
   LLM** (ahorra tokens + respeta el kill switch). Verificado en test.
2. Si pasa: `_destilar` → `_guardar_con_governor(..., provenance="auto")`.
3. Si se guardó: la skill se **fuerza a `lifecycle='stale'`** (NO se inyecta al chat) y se
   marca `requiere_gate=True`. Nada auto-generado entra en uso sin aprobación humana.

**Gate (P2):**
- `aprobar_skill(pool, skill_id)`: `stale → active` (solo si provenance='auto' y estaba stale). Devuelve nombre o None.
- `rechazar_skill(pool, skill_id)`: `stale → archived` (recuperable, nunca borra).

**Telegram:**
- Disparador: en `_correr_equipo_y_responder` (tras una corrida de equipo = señal de tarea
  compleja), `asyncio.create_task(self._auto_mejora_background(msg, sesion, autor_id))`.
- `_auto_mejora_background` (~836): llama `proponer_skill_auto`; si propone, manda al DUEÑO
  (`owner_id`) un mensaje con botones **✅ Activar** (`skok:<id>`) / **❌ Descartar** (`skno:<id>`).
  Defensivo: nunca tumba el bot, nunca toca el chat principal salvo ese aviso.
- `on_skill_gate` (~867, patrón `^sk(ok|no):`): solo el dueño (`_es_admin`); aprobar/rechazar.

⚠️ Hoy INERTE: como el kill switch está OFF por defecto, P2 no genera nada hasta que el
dueño haga `/autogen on`. Esa es la barrera intencional.

### 3.5 P3 — curación nocturna (reusa H6)

`curar_skills(pool, *, confirmar=True) -> ResultadoCuracion(a_stale, a_archived)`:
- `active + auto + NOT pinned + veces_usada=0 + ultimo_uso NULL + actualizada_at < now()-30d` → **stale**
- `stale  + auto + NOT pinned + veces_usada=0 + ultimo_uso NULL + actualizada_at < now()-90d` → **archived**
- `confirmar=False` = DRY-RUN (solo cuenta, no mueve).
- **Intocables:** provenance='usuario', pinned, usadas (veces_usada>0 o ultimo_uso), y las
  **propuestas recientes del gate** (están en stale pero son recientes → no caen en el corte
  de 90d). Recuperable, nunca hard-delete. Es el `curator` de Hermes / filosofía Microglía H6.

**Job Arq:** `job_curar_skills` (tasks.py) + `HORA_CURAR_SKILLS_UTC = 9` → cron 03:30 México
(después de Microglía 03:00). Registrado en `WorkerSettings.functions` + `cron_jobs`
(`minute=30`). Worker: 6 jobs / 5 crons.

---

## 4. Estado nocturno completo (orden de los jobs)

```
01:00 Mx  job_backup        (red de seguridad antes de borrar nada)
02:00 Mx  job_cls           (consolida episodios → conceptos al grafo)   H6
02:30 Mx  job_status        (auto-retomar STATUS por hilo)               AI4
03:00 Mx  job_microglia     (olvido de memoria, soft-delete)            H6
03:30 Mx  job_curar_skills  (degrada skills auto sin uso)               H12 P3  ← NUEVO
```

---

## 5. Comandos Telegram del ciclo APRENDE

| Comando | Quién | Handler | Menú |
|---|---|---|---|
| `/skills` · `/skills <n>` | todos | `on_skills` | básico |
| `/aprende [foco]` | todos | `on_aprende` | básico |
| `/autogen on\|off\|status` | dueño | `on_autogen` | admin |
| botones ✅/❌ skill propuesta | dueño | `on_skill_gate` (`^sk(ok\|no):`) | (callback) |

---

## 6. Tests (qué cubren — para no romperlos al modificar)

Los tests fueron de verificación (BD/LLM reales sobre el server, no en la suite del repo;
la suite del repo sigue en 132 passed / 4 skipped sin regresión). Cobertura lograda:
- **H11 governor (24/24):** scanner (9 casos: inocente pasa + rm-rf/curl|sh/KEK/token/cron/
  prompt-inj es+en/multi-hallazgo), kill switch, gate usuario/auto, duplicado, techo diario,
  provenance (usuario no topa techo de auto), hooks neutros, auditoría, health.
- **H12 P1 (10/10):** _extraer_json, _material_de_turnos, destilar+guardar real (skill con
  pasos, provenance=usuario), y fuente peligrosa → NO se guardó (LLM rehusó + scanner 2ª capa).
- **H12 P2 (10/10):** OFF no llama al LLM, ON propone en stale + requiere_gate, no aparece
  activa hasta aprobar, aprobar→active, re-aprobar no-op, rechazar→archived.
- **H12 P3 (8/8):** dry-run cuenta sin mover, active vieja→stale, stale vieja→archived,
  usada resiste, usuario intocable, pinned intocable, reciente (gate) no se toca.

---

## 6.bis Verificación E2E EN VIVO (Brian en Telegram, 2026-06-25)

Brian probó el ciclo completo en producción. Trazabilidad cruzada (BD + logs + audit):

- **H11 kill switch** ✅ — `/autogen on` (19:50:58) y `on/off` (08:42) quedaron en
  `governor_estado` con su `cambiado_por=1923367928`. 0 tokens (no usa LLM).
- **H12-P1 `/aprende`** ✅ — 19:52:27 log `[skills] creada deploy/pipeline-...-botservicio
  (prov=usuario)` → **skill #20** real, contenido fiel a lo que Brian escribió (5 pasos +
  tip). El mensaje fuente gastó 10251 in / 357 out tokens.
- **H12-P2 auto-mejora** ✅ (lo más fuerte) — cadena verificada en logs: "analiza a fondo
  cli/cli" (19:53:39) → equipo familia técnica 5/5 ok en 60.5s (💰 7969 tokens, in 469/out
  7500) → synthesizer + `handoff corrida=3` (19:55:18) → 19:55:27 `[skills] creada
  deploy/pipeline-...-en-servidor (prov=auto)` = **skill #21 auto** nacida en stale →
  19:55:52 actualizada a active = **gate aprobado por Brian** (botón ✅).
- **H10 uso real de skill** ✅ — primera prueba fue inconcluyente (preguntó deploy justo tras
  explicarlo → no se distinguía skill de contexto; `veces_usada=0`). Re-prueba LIMPIA: se
  reseteó el contador a 0, Brian metió 2 mensajes de otro tema (clima, Rust/Go) y luego
  "¿cómo despliego el bot al servidor?" (20:11:20) → **`veces_usada` 0→1 en ambas skills,
  `ultimo_uso=20:11:20`**. Como el deploy NO estaba en el contexto inmediato, la respuesta
  solo pudo salir de la skill inyectada (H10). Prueba dura = el contador.
- **Personalidad reconoce H10-12** ✅ — hallazgo: el bot decía "no tengo actualizaciones"
  (FOR3S_ROLE congelado en H8). FIX en `agent.py`: identidad H1-H8→H1-H12 + bloque de
  capacidad "APRENDER SKILLS/RECETAS (H10-H12)" + comandos /skills//aprende//autogen.
  Verificado en vivo (20:13-20:14): "¿qué nuevas capacidades tienes?" → menciona Skills/
  Aprende como NUEVO; "¿tú aprendes?" → "Sí, aprendo — y no es metáfora… el ciclo H10-H12".

**Hallazgos de la prueba (para cuando se modifique a detalle):**
1. ⚠️ **El matcher de skills es POR PALABRAS, no semántico** (`buscar_relevantes` regex `~`):
   "subir nueva versión a producción" NO macheó la skill de deploy (no comparte la palabra
   "deploy/desplegar"). La búsqueda semántica de skills (embeddings/pgvector) es trabajo futuro.
2. ⚠️ **2 skills casi-duplicadas** (#20 usuario "...botservicio" + #21 auto "...bot-en-servidor")
   NO se bloquearon como duplicado porque el slug difiere. Confirma la deuda §8: el FRENO 4 es
   exact-match `(categoria, nombre)`; la contradicción SEMÁNTICA es futura.
3. ⚠️ **No hay evento en la audit chain (`audit_events`) para /aprende ni para el gate de
   skills** — quedan en su tabla + logs, pero no en la cadena inmutable. Mejora posible para
   trazabilidad completa.
4. ✅ Con la memoria semántica activa, H10 (skill) y H5 (memoria) pueden traer lo mismo a la
   vez — no se aíslan al 100% en chat, pero el contador `veces_usada` prueba que la skill se
   activó.

---

## 7. Decisiones LOCKED (no re-litigar sin querer al modificar)

1. **Orden sagrado H10 → H11 → H12** (el freno antes del motor; R6 / Grafo §8.4).
2. **Skill = SKILL.md** (receta markdown que el agente aplica con sus tools), NO código
   arbitrario auto-ejecutado. Por eso una skill no "corre"; el agente la lee y sigue sus pasos.
3. **Scanner muy conservador, FAIL-CLOSED.** Bloquea + avisa.
4. **Kill switch SOLO del dueño** (`/autogen`), persistido en BD, + flag de emergencia
   `FOR3S_AUTOGEN_OFF`. **Default: auto-gen APAGADA.**
5. **Provenance manda:** el governor/curator SOLO gestiona skills `auto`. Las `usuario` son
   intocables (salvo scanner+duplicado al crearlas).
6. **Auto-generado → gate al dueño** (nace en stale, no se usa hasta aprobar).
7. **/aprende manual → directo** (lo pidió un humano), pero pasa el scanner.
8. **Fuente de /aprende = la conversación actual** (los 12 turnos del hilo).
9. **Frenos 2/3/6 = hooks honestos** (no implementados aún; requieren scoring/NO-GO/sandbox).
10. **Calibración v1:** 3 auto/día, 100 activas, 30d→stale, 90d→archived.
11. **CERO referencias externas en el código** (intern-os/Hermes/OpenClaw/Frutero solo en
    docs privados de Mente OS, nunca en código distribuible).

---

## 8. Lo que NO se construyó (deuda consciente, para cuando modifiques a detalle)

- Frenos 2/3/6 reales (necesitan: scoring dopaminérgico de skills, reglas NO-GO con
  expiración, sandbox de evaluación independiente). Hoy hooks neutros.
- Contradicción **semántica** (F4): hoy exact-match `(categoria, nombre)`. La versión por
  similitud de embeddings (pgvector, umbral 0.85 del R6) es futura.
- `/aprende` desde **repo o URL** (hoy solo la conversación). El plan lo contempla.
- Multi-workspace real (hoy 1 workspace 'default'; el esquema ya soporta varios).
- Auto-mejora que **parchea** una skill existente (hoy solo crea nuevas; un parche sería
  editar el contenido + bump de version).
- Reporte de salud del ecosistema en un dashboard (R8 §8.2.2); hoy solo `/autogen status`.
- **Matcher de skills semántico** (uso, H10): hoy `buscar_relevantes` es match por palabras
  (regex `~`, palabras ≥4 chars). No machea sinónimos ("subir a producción" ≠ "deploy").
  Migrar a embeddings/pgvector lo haría robusto (confirmado en la prueba en vivo 2026-06-25).
- **Audit chain para /aprende y gate de skills**: hoy quedan en la tabla `skills` + logs, NO
  en `audit_events` (cadena inmutable). Añadirlo daría trazabilidad completa como en GitHub-write.

> Refs cruzadas: `memory/archive/H10-H12_Plan_Maestro_APRENDE.md` (plan + estado) ·
> `work/Ronda_06_Pre_Code_Review_Detailed.md` §A (diseño del governor, umbrales originales) ·
> `docs/analysis/Analisis_LearningLoop_Hermes_para_For3s.md` (de dónde salió la idea) ·
> memoria `project_analizar_intern_os`.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/H10_H11_H12_APRENDE_Referencia_Tecnica.md`).
