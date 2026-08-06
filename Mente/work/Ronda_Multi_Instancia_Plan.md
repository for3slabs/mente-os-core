# 🏢 RONDA — MULTI-INSTANCIA (gestor local de varios For3s OS)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_Multi_Instancia_Plan.md → work/Ronda_Multi_Instancia_Plan.md (2026-07-30, ADR-029)

## Purpose

🏢 RONDA — MULTI-INSTANCIA (gestor local de varios For3s OS)


**Fecha:** 2026-07-02
**Origen (Brian 2026-06-28, debatido 2026-07-02):** hoy 1 servidor = 1 For3s. Brian quiere correr
VARIOS For3s OS aislados en su máquina, cada uno un contenedor completo e independiente — para uso
personal (varios suyos) y para clientes (uno por cliente). Gestionados con un comando `for3s`.
**Estado:** DISEÑO (debatido y LOCKED con Brian 2026-07-02). Cada fase se construye con OK de Brian,
probada E2E, misma disciplina que REDISEÑO MEMORIA / AUTO-CONCIENCIA.

---

## 0. La visión (LOCKED con Brian)

Un **gestor LOCAL de instancias** en la máquina del usuario:
- Comando `for3s` → **menú en la terminal**: "Agregar un nuevo For3s OS" · "Entrar a uno" (lista) ·
  (y start/stop de instancias).
- **"Entrar a uno"** = abrir una **consola/chat con ESE For3s** en la terminal (chat local directo).
- Cada For3s = **contenedor completo, AISLAMIENTO TOTAL** (su propio agent+worker+postgres+valkey,
  su memoria/KEK/dueño/grafo — NUNCA se cruzan con otra instancia).
- **Solo las que usas, encendidas** (las demás apagadas → no gastan RAM).
- **Bloque UNIDO al instalador**: el comando `for3s` nace con la instalación de For3s OS.

### Decisiones LOCKED (debate + preguntas 2026-07-02)
| Tema | Decisión |
|---|---|
| Caso de uso | Gestor LOCAL (varios For3s en TU máquina): personal + clientes. NO SaaS remoto (→ EXTRA). |
| Aislamiento | **TOTAL** — cada instancia su stack completo, cero contacto. |
| Ejecución | Solo las encendidas (start/stop; las demás Exited, como los demos parados). |
| "Entrar" | Abrir la **consola/chat** de esa instancia en la terminal (ya existe: `cli.py` REPL). |
| Instalador | **UNIDO** — `for3s` es parte de la instalación. |
| Técnica de aislamiento | **Un proyecto Compose por instancia** (`docker compose -p for3s-<nombre>` con el MISMO compose) → red/volúmenes/contenedores con prefijo → aislamiento total automático, sin chocar puertos. |
| Estado por instancia | **Carpeta `~/.for3s/<nombre>/`** (KEK master.key + owner) + volumen `for3s-<nombre>_pgdata` + backups `~/for3s-backups/<nombre>/`. Rutas/volúmenes distintos = datos 100% separados. |
| Wizard "Agregar" pide | nombre único · token de Telegram propio (o vacío=solo consola) · KEK auto-generada · dueño (telegram_user_id). |
| Orden de obra | Gestor `for3s` primero (sobre lo que ya existe) → probar 2ª instancia → unir al instalador. |

### Diferido a §EXTRAS (Brian 2026-07-02)
- **MI-EXTRA-1** SaaS remoto multi-tenant (clientes por internet, interno de For3s OS).
- **MI-EXTRA-2** ⭐ Botón WEB para encender/apagar instancias (sin terminal).

---

## 1. Análisis del terreno REAL (verificado en vivo 2026-07-02)

Lo que FUNDA el diseño (por qué es más simple de lo que el doc original asumía):
1. **La imagen `for3s-agent:local` (13.2GB) se COMPARTE** entre contenedores — Docker NO la duplica.
   N instancias = 1 sola imagen en disco. Lo que se multiplica es la RAM en ejecución (~2GB/agent
   por el modelo BGE-M3) → por eso "solo las encendidas" es la regla correcta. Server: 18GB RAM.
2. **`docker compose -p <proyecto>` YA aísla** todo: red interna propia, volúmenes y contenedores con
   prefijo del proyecto. Dos instancias con `-p` distinto NO chocan puertos (cada una su red interna
   `postgres:5432` / `valkey:6379` — el nombre es interno, no del host). → aislamiento total GRATIS.
3. **El chat de consola YA EXISTE:** `cli.py` tiene un REPL (`console.input("tú › ")`) + `Conversation`
   soporta `channel="cli"`. "Entrar al chat" = `docker exec -it for3s-<nombre>_agent_1 python -m
   for3s_core.cli`. No hay que construir el chat — solo orquestarlo.
4. **El estado por-instancia ya está desacoplado en `~/.for3s`** (KEK + owner) → basta con una
   subcarpeta por instancia. El compose ya monta `~/.for3s` — se parametriza a `~/.for3s/<nombre>`.
5. **Material de partida:** 4 demos parados (`for3s-demo-*`, Exited, recuperables).

**Conclusión:** MULTI-INSTANCIA NO requiere reescribir el stack. Es un ORQUESTADOR (`for3s`) que:
compone el mismo docker-compose.yml con `-p <nombre>` + un `.env`/estado por instancia. Reusa el
99% de lo que ya existe.

---

## 2. Arquitectura del diseño

### 2.1 Layout en disco (por instancia)
```
~/for3s-os/                      # el código + docker-compose.yml (compartido, la plantilla)
~/.for3s/<nombre>/               # estado AISLADO de la instancia
    master.key                   # KEK propia (generada al crear)
    telegram_owner.json          # dueño propio
    .env                         # config propia (token Telegram, nombre, dueño, POSTGRES_PASSWORD)
~/for3s-backups/<nombre>/        # backups propios
Docker (por instancia, prefijo for3s-<nombre>):
    red for3s-<nombre>_default · volumen for3s-<nombre>_pgdata · for3s-<nombre>_valkeydata
    contenedores for3s-<nombre>-agent-1 / -worker-1 / -postgres-1 / -valkey-1 / -mcp / -render
```

### 2.2 El comando `for3s` (el gestor) — un script que orquesta docker compose
Menú (o subcomandos):
- `for3s` (o `for3s menu`) → menú interactivo.
- **listar** → lee `~/.for3s/*/` → muestra instancias + su estado (encendida/apagada) [docker ps].
- **agregar `<nombre>`** → WIZARD: pide token Telegram (o vacío) + dueño → genera KEK →
  crea `~/.for3s/<nombre>/` + `.env` → `docker compose -p for3s-<nombre> up -d` (levanta el stack) →
  corre migraciones (el guardián/entrypoint ya lo hace).
- **entrar `<nombre>`** → si está apagada, la enciende → `docker exec -it for3s-<nombre>-agent-1
  python -m for3s_core.cli` (el chat de consola).
- **encender/apagar `<nombre>`** → `docker compose -p for3s-<nombre> start|stop`.
- **borrar `<nombre>`** → confirma → `docker compose -p for3s-<nombre> down -v` + borra `~/.for3s/<nombre>`.

⚠️ El gestor vive FUERA de los contenedores (en el host) — es una herramienta de línea de comandos
del usuario, no del agente. NO le da al agente acceso a Docker (respeta el diseño sin-DinD).

### 2.3 Parametrización del compose (lo único que cambia por instancia)
El `docker-compose.yml` ya usa variables (`${POSTGRES_PASSWORD}`, `${TELEGRAM_BOT_TOKEN}`,
`${ANTHROPIC_TOKEN}`). El gestor pasa `-p for3s-<nombre>` + `--env-file ~/.for3s/<nombre>/.env` +
sustituye el mount de `~/.for3s` por `~/.for3s/<nombre>`. Nada más. Un solo compose para todos.

---

## 3. Las fases (orden LOCKED)

### FASE MI-1 · El gestor `for3s` — ✅ HECHO Y VERIFICADO 2026-07-02 (commit 7a71e55)
Script `for3s` (bash) en el host: listar · agregar (wizard) · entrar (chat de consola) · encender ·
apagar · borrar. Orquesta `docker compose -p for3s-<nombre>` con la plantilla `docker-compose.instancia.yml`
(NO toca el compose de Foresito en producción). Estado por instancia en `~/.for3s/<nombre>/`.
- ⭐ 5 BUGS de aislamiento cazados por curiosidad ANTES de construir (hardcodeo en el compose):
  (1) `name: for3s` fijo → -p se ignoraba; (2) red `for3s_net` fija → instancias compartían red;
  (3) puerto Grafana 3000 fijo → choque; (4)(5) mounts de estado (KEK/owner) hardcodeados a una ruta.
  Fix: plantilla parametrizada (todo por variable, default = Foresito).
- 2 bugs cazados EN VIVO al probar: KEK generada en base64 (For3s espera 32 bytes CRUDOS, no b64 =
  45 chars → "master key corrupta"); agent en loop sin token Telegram → **modo SOLO CONSOLA** en el
  entrypoint (si no hay token, queda vivo dormido para `for3s entrar`, no arranca el bot).
- **Verificado E2E:** instancia `testmi` creada aislada → su Postgres/KEK/estado SEPARADOS de Foresito
  (escribir en una NO aparece en la otra) → `for3s entrar` responde en su chat → `for3s borrar` limpia
  todo → Foresito INTACTO (714 turnos) durante TODO el proceso. Aislamiento total confirmado.
- Decisión: el token de Claude se HEREDA del `.env` de la máquina por default (o se da uno propio para
  un cliente). ⚠️ El gestor vive en el HOST (no le da Docker al agente, respeta sin-DinD).

### FASE MI-2 · ✅ HECHO Y VERIFICADO 2026-07-02 (commit 61df2cf)
Probado el MODO BOT de una instancia (aislamiento ya probado en MI-1):
- **Bifurcación modo-bot ✅:** con token → el entrypoint arranca el bot; sin token → modo solo consola.
  El gestor genera el `.env` correcto. Verificado con token dummy (eligió modo-bot → InvalidToken, correcto).
- **🐛 Bug de robustez cazado y corregido:** un token de Telegram INVÁLIDO dejaba la instancia en LOOP
  de reinicio (RestartCount subiendo). Fix: el wizard VALIDA el token contra Telegram (`getMe`) ANTES
  de crear → si es inválido, avisa y NO crea nada (sin carpeta, sin contenedor, sin loop). Verificado.
- El bot real respondiendo por Telegram usa el MISMO agente/memoria ya verificado en MI-1 (chat de
  consola respondió) — solo cambia el canal (código maduro de Foresito). Probar con un token real es
  algo que Brian hace cuando lo necesite (bot desechable de @BotFather). Aislamiento total + modo-bot
  + validación de token = todo probado. **MI-2 cerrado.**

### FASE MI-3 · ✅ HECHO Y VERIFICADO 2026-07-02 (commit cc87f7d)
El comando `for3s` nace con la instalación, SIN tocar el flujo de 1ª instalación (Pre-Testers, probado):
- **install.sh** paso 7.5 nuevo: instala `for3s` en el PATH (`/usr/local/bin` con sudo si hay, si no
  `~/.local/bin` + aviso de PATH) + avisa "gestiona VARIOS For3s: `for3s`". El montaje de la 1ª
  instancia queda INTACTO. Verificado: el comando funciona desde cualquier lado (`for3s listar` en /tmp).
- **uninstall.sh** ahora baja TAMBIÉN todas las instancias del gestor (proyectos `for3s-*`, no solo la
  principal → evita huérfanas) + borra el estado de todas + quita el comando del PATH.
- ⚠️ El instalador COMPLETO (`curl|sh`, dominio, wizard extendido) es del bloque PRODUCTO DISTRIBUIBLE
  (P1-P10, aún no atacado). MI-3 solo integra el comando `for3s` al instalador YA existente.

---

## ✅ MULTI-INSTANCIA COMPLETO (2026-07-02)
MI-1 (gestor `for3s`) + MI-2 (modo bot + validación de token) + MI-3 (unido al instalador). El gestor
crea/gestiona varios For3s OS aislados en la máquina, aislamiento total verificado, cero riesgo a
Foresito. Commits firmados: 7a71e55 · 61df2cf · cc87f7d. Diferido a EXTRAS: MI-EXTRA-1 SaaS remoto ·
MI-EXTRA-2 botón web on/off.

---

## 4. Riesgos identificados (curiosidad) y mitigación

| Riesgo | Mitigación |
|---|---|
| RAM: N instancias encendidas agotan los 18GB | Regla "solo las encendidas" + el gestor avisa/limita cuántas activas |
| Choque de puertos entre instancias | `-p` da red interna propia; NO se exponen puertos al host (como hoy) |
| Cruce de memoria entre instancias | Postgres/KEK/volúmenes separados por `<nombre>` → imposible por construcción |
| Los hermanos MCP/render por instancia = mucho peso | Decidir en MI-1: ¿MCP/render compartidos o por instancia? (aislamiento total sugiere por instancia, pero se puede evaluar) |
| El agente NO debe poder tocar otras instancias | El gestor vive en el HOST, no en el contenedor; el agente sigue sin acceso a Docker (sin-DinD) |
| Borrar una instancia por error | `borrar` pide confirmación + el `down -v` solo afecta ese proyecto `-p` |

---

## 5. Lo que NO hace este diseño (fuera de alcance, a propósito)
- NO es SaaS remoto (→ MI-EXTRA-1). Es local, en la máquina del usuario.
- NO tiene botón web on/off (→ MI-EXTRA-2). El on/off es por CLI (`for3s`).
- NO le da al agente acceso a Docker (el gestor es del host, respeta sin-DinD).

---

## 6. Relacionado
- PRODUCTO DISTRIBUIBLE P1-P10 (el instalador; MI-3 se une ahí) · H8 (multi-USUARIO, capa distinta:
  esto es multi-TENANT) · PR2 salud (monitorear N stacks) · PR6 dueños (dueño por instancia) ·
  Fase Pre-Testers (la contenerización base que esto extiende) · el modelo de negocio.
- Memoria: [[project_multi_instancia]]. EXTRAS: MI-EXTRA-1 (SaaS) · MI-EXTRA-2 (botón web).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_Multi_Instancia_Plan.md`).
