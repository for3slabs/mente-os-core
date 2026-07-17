# 🛠️ RONDA — EXECUTE_CODE (agente-desarrollador con sandbox hermano)

**Fecha:** 2026-07-02
**Origen (Brian 2026-07-02):** Brian quiere que For3s tenga **paridad Hermes en `execute_code`** — un
agente-desarrollador completo: le pides "hazme un script/proyecto que haga X" → lo escribe, lo ejecuta,
te da el resultado; si necesita una librería, la instala solo. Surgió del bloque PRODUCTO DISTRIBUIBLE
(P6 sandbox + P8 instalar programas + P3-Hermes ejecutar código) y del análisis de Hermes (Nous).
**Estado:** DISEÑO (debatido y LOCKED con Brian 2026-07-02). Cada fase con OK de Brian, probada E2E,
misma disciplina que REDISEÑO MEMORIA / AUTO-CONCIENCIA / MULTI-INSTANCIA.

---

## 0. La visión (LOCKED con Brian)

For3s como **agente-desarrollador dentro de su caja**:
- Le pides algo que requiere correr código → lo **escribe**, lo **ejecuta** en un sandbox, te da el
  **resultado** — todo de corrido (**actúa solo**). Si falta una librería, **la instala solo**.
- Puede **crear proyectos** (workspace persistente), crear/editar archivos, correr código real.
- Todo en un **sandbox SEPARADO y aislado** (no en el cerebro del agente): si el código se descontrola,
  solo se rompe el sandbox — la memoria/código/BD de Foresito quedan intactos.

### Decisiones LOCKED (debate + preguntas 2026-07-02)
| Tema | Decisión |
|---|---|
| Qué es | paridad Hermes `execute_code`: escribe→ejecuta→resultado, instala solo, crea proyectos |
| Aislamiento | Sandbox SEPARADO del cerebro (no en el contenedor del agente) |
| Técnica | **Hermano de red HTTP** `for3s-sandbox` (patrón render/MCP) → respeta sin-DinD (el agente NO toca Docker, le habla por HTTP) |
| Endurecimiento | límites: timeout · RAM · CPU · pids (anti fork-bomb) · usuario sin privilegios. Reusa el diseño de `sandbox.py` (BUG-2) |
| Lenguajes v1 | **Python + Bash + Node/JS** (con pip/npm para instalar) |
| Persistencia | **Workspace PERSISTENTE** (`~/.for3s/workspace`) → crea proyectos reales que perduran entre ejecuciones |
| Disparo | **Tool `execute_code`** (el MODELO decide cuándo usarla, como las tools de GitHub) — actúa solo |
| Gate | **Actúa solo** — el sandbox aislado ES el control estructural (igual filosofía que AUTO-CONCIENCIA) |

### Diferido a §EXTRAS
- **EC-EXTRA-1** backend LOCAL / SSH / cloud (Daytona/Modal) — sale de la caja al host/otra máquina;
  se evalúa después con su propio diseño de seguridad. v1 = solo sandbox en la caja.

---

## 1. Análisis del terreno REAL (verificado en vivo 2026-07-02)

Lo que FUNDA el diseño (por qué es viable y reusa mucho):
1. **`sandbox.py` YA existe** (BUG-2, diferido "para volverlo hermano de red cuando llegue el flujo de
   ejecución" — ESTE es ese momento). Ya trae el ENDURECIMIENTO diseñado: `--network none`,
   `--read-only`, `--user 10001` (sin privilegios), `--memory`/`--cpus`, `--pids-limit` (anti
   fork-bomb), `timeout`. Se reusa/evoluciona esa base (hoy corre `ruff`; ahora correrá código).
2. **El hermano `render` es la PLANTILLA exacta:** `docker/render/render_http.py` = servidor HTTP
   (stdlib) que recibe una petición, ejecuta algo (Playwright) y devuelve el resultado. El sandbox
   es lo mismo pero ejecutando código. Reusa Dockerfile + patrón HTTP + endpoint /health (PR2).
3. **El agente ya sabe usar tools por el MODELO** (tool-loop de GitHub MCP): `execute_code` se añade
   como una tool más → el modelo decide cuándo llamarla. Cero infra nueva de decisión.
4. **Hermanos por red = patrón probado 3 veces** (github-mcp read, github-mcp-write, render) → el
   agente NO toca Docker, le habla por HTTP. sin-DinD respetado.
5. **For3s ya tiene casi toda la paridad Hermes:** memoria (H5/H6+rediseño), aprende (H10-12), equipo
   (H8), MCP (P4), auto-modificación (AC1-4). `execute_code` es LA pieza grande que falta para ser
   "un agente 100%" tipo Hermes.

---

## 2. Arquitectura del diseño

### 2.1 El hermano `for3s-sandbox` (contenedor de ejecución aislado)
- Nuevo servicio en el compose (como github-mcp/render): imagen con Python+Bash+Node + pip/npm.
- Servidor HTTP (stdlib, patrón render_http.py): `POST /run {codigo, lenguaje, timeout?}` →
  ejecuta con LÍMITES (timeout, RAM, CPU, pids, usuario sin privilegios) → responde
  `{ok, stdout, stderr, exit_code, archivos_nuevos?}`. + `/health` (PR2).
- **Aislamiento:** su propio contenedor, límites de recursos, red controlada. Si el código se
  descontrola (bug/fork-bomb/RAM) → solo afecta a ESTE hermano (reiniciable), NO al agente.
- **Workspace PERSISTENTE:** volumen `~/.for3s/workspace` montado en el sandbox → los proyectos/
  archivos perduran entre ejecuciones (crea proyecto → instala deps → sigue trabajándolo → lo corre).
  Aislado del cerebro del agente (que vive en otro contenedor) pero persistente para el trabajo.

### 2.2 El cliente en el agente (`execute_code` como tool)
- Módulo `execute.py` (cliente HTTP al hermano, como mcp_client/web_fetch): manda el código, recibe
  el resultado. Defensivo (si el sandbox cae, degrada: "no pude ejecutar", no rompe el turno).
- Se registra como **tool `execute_code`** en el tool-loop (junto a las de GitHub) → el MODELO la
  llama cuando la tarea requiere correr código. Actúa solo (escribe→ejecuta→lee→responde).
- Instalar librerías: el código puede incluir `pip install`/`npm install` (corre en el sandbox, con
  red controlada para los repos de paquetes). Decisión de red en la fase (¿pip sí, resto no?).

### 2.3 Multi-instancia (cruza con MI)
- Cada instancia de For3s (MULTI-INSTANCIA) tendría SU propio sandbox hermano + workspace aislado
  (mismo patrón `-p for3s-<nombre>`). El código del cliente A nunca toca el workspace del cliente B.

---

## 3. Las fases (orden sugerido: de menor a mayor riesgo)

### FASE EC-1 · ✅ HECHO Y VERIFICADO 2026-07-02 (commit 66d165a)
Contenedor `for3s-sandbox` (imagen LIGERA 111MB: python-slim+node+bash, usuario sin privilegios uid
10001) + servidor HTTP `sandbox_http.py` (patrón render_http.py): `POST /run {codigo, lenguaje, timeout,
mem_mb}` → ejecuta con LÍMITES del SO (RLIMIT_CPU/AS/NPROC vía preexec_fn) → `{ok, stdout, stderr,
exit_code}` + `/health`. NO usa `docker run` (el hermano YA es el contenedor) → respeta sin-DinD.
- 🔍 Experimentos que fundaron el diseño (en vivo): `resource.setrlimit` corta de verdad (while-True→
  CPU exit -9, come-RAM→MemoryError, fork-bomb→contenido, el contenedor sobrevive); prlimit/timeout sin docker.
- 🐛 **BUG cazado y corregido:** Node (V8) reserva mucha memoria virtual al arrancar (CodeRange) →
  RLIMIT_AS de 512MB lo mata con "Fatal process OOM" ANTES de correr. Fix: para node NO aplicar
  RLIMIT_AS estricto; limitar el heap con `--max-old-space-size` (la forma correcta de limitar Node).
- **Verificado E2E 5/5:** python (`4`), bash (`ok-bash`), node (`42`), while-True cortado por timeout,
  lenguaje no soportado rechazado limpio. Foresito intacto (no se tocó). 3 lenguajes de v1 ✅.
- ⏳ Falta (EC-2+): workspace persistente + instalar deps (hoy la ejecución es efímera).

### FASE EC-2 · ✅ HECHO Y VERIFICADO 2026-07-02 (commit 3c595ca)
El sandbox pasó de standalone a HERMANO de red permanente del compose:
- servicio `sandbox` en docker-compose.yml (aditivo, NO toca los servicios de Foresito) con volumen
  PERSISTENTE `for3s_sandbox_ws:/home/sandbox/workspace` + `mem_limit 1200m` + `pids_limit 256` (2ª
  capa anti fork-bomb sobre los RLIMIT del proceso). El agent depende de él + `FOR3S_SANDBOX_URL=
  http://sandbox:8090` (para EC-3).
- **Verificado en vivo:** (a) persistencia: el workspace sobrevive al recrear el contenedor (volumen
  nombrado); (b) instalar deps: `pip install cowsay` → se instala y se usa; (c) el AGENT alcanza al
  sandbox por la red interna (`http://sandbox:8090/health` ok); (d) los scripts temporales se limpian
  (0 basura); (e) Foresito INTACTO. Bash y Node ya venían de EC-1.
- 🔒 **DECISIÓN LOCKED (Brian):** red ABIERTA en el sandbox (pip/npm install + el código puede consultar
  APIs/descargar) — el control es que es el agente de Brian (no expuesto a terceros) + aislamiento
  fuerte del host + límites de recursos. Es el modelo Hermes. (Verificado: el código alcanza example.com.)
- ⏳ Falta (EC-3): la tool `execute_code` en el agente (que el modelo la use sola).

### FASE EC-3 · ✅ HECHO Y VERIFICADO 2026-07-02 (commit 6c43e4a) — LA FASE ESTRELLA
Foresito ya es un **agente-desarrollador**: escribe código, lo ejecuta en el sandbox hermano, responde.
- `execute.py` (nuevo): cliente HTTP al hermano (como web_fetch↔render) + `EXECUTE_TOOL_SCHEMA`. Defensivo.
- `tool_loop.py`: registra `execute_code` en las tools + la ejecuta llamando al sandbox por HTTP
  (to_thread). NO es tool MCP ni write con gate → el sandbox aislado ES el control (actúa solo, sin-DinD).
- `conversation.py`: detector `huele_a_codigo` (script/ejecuta/analiza datos/instala/calcula...).
- `telegram_channel.py`: `usa_tools = huele_a_github OR huele_a_codigo` → el tool-loop se activa también
  cuando el mensaje pide código (antes solo con GitHub).
- **Verificado E2E con LLM real:** "cuenta los primos entre 1 y 100 ejecutando código" → el modelo llamó
  `execute_code` → el sandbox corrió Python → Foresito respondió **25** (correcto). Detector 10/10 (6+/4−).
  execute.py habla con el sandbox (sum 0..100=5050). Foresito intacto.
- ⏳ Falta (EC-4): un sandbox por instancia (multi-instancia) + endurecimiento/health final.

### FASE EC-4 · ✅ HECHO Y VERIFICADO 2026-07-02 (commit 6abd82c) — CIERRA EL BLOQUE
- `docker-compose.instancia.yml` regenerado desde el compose de Foresito (con el sandbox) → cada
  instancia de MULTI-INSTANCIA tiene SU PROPIO sandbox + workspace aislado (`for3s-<nombre>_sandbox_ws`).
- `health.py`: /salud (PR2) ahora VIGILA el sandbox por HTTP (junto a MCP/render) → caído ya no pasa en silencio.
- **PRUEBAS RIGUROSAS (todos los elementos + conexiones hermanas):** /salud las 4 integraciones ✅ (MCP,
  MCP write, Render, Sandbox); 🐛 la curiosidad cazó el hermano RENDER degradado (RemoteProtocolError/
  Cannot fork tras 4h) → reiniciado → sano (valor de PR2); AISLAMIENTO cruzado verificado: 2ª instancia
  (ectest) con su propio sandbox → su workspace NO ve los archivos del de Foresito y viceversa (no se
  cruzan); ectest borrada sin huérfanos; 9 contenedores sanos; Foresito intacto.

---

## ✅ EXECUTE_CODE COMPLETO (2026-07-02)
EC-1 (hermano sandbox con límites) + EC-2 (workspace persistente + instalar deps) + EC-3 (tool
`execute_code` — Foresito es agente-desarrollador, verificado con LLM real) + EC-4 (sandbox por
instancia + /salud lo vigila). Foresito escribe código, lo ejecuta en un sandbox aislado, instala libs,
crea proyectos — actúa solo, sin tocar el host (sin-DinD). Paridad Hermes execute_code cumplida (P3/P6/P8).
Commits firmados: 66d165a·3c595ca·6c43e4a·6abd82c. Diferido a EXTRAS: EC-EXTRA-1 backend local/SSH/cloud.

---

## 4. Riesgos identificados (curiosidad) y mitigación

| Riesgo | Mitigación |
|---|---|
| Código malicioso/roto se descontrola | Sandbox SEPARADO + límites (timeout/RAM/CPU/pids) → solo se rompe el sandbox |
| El código sale de la caja y toca el host | `--network` controlada + `--read-only` fuera del workspace + usuario sin privilegios + sin-DinD |
| Fork-bomb / agota recursos del server | `--pids-limit` + `--memory`/`--cpus` (ya en sandbox.py) |
| Instalar libs = acceso a red arbitrario | Red del sandbox limitada a repos de paquetes (pip/npm); evaluar en EC-2 |
| El agente toca Docker (viola sin-DinD) | El sandbox es hermano de red; el agente solo habla HTTP (patrón probado) |
| Un cliente ve el código/proyecto de otro | Sandbox + workspace por instancia (MULTI-INSTANCIA, -p) |
| El sandbox afecta al cerebro del agente | Contenedor SEPARADO — el agente (memoria/BD/código) vive en otro contenedor |

---

## 5. Lo que NO hace este diseño (fuera de alcance, a propósito)
- NO ejecuta en el host ni por SSH ni en cloud (→ EC-EXTRA-1). v1 = solo el sandbox en la caja.
- NO le da al agente acceso a Docker (el sandbox es hermano de red).
- El código NO puede salir del sandbox ni tocar la memoria/código del agente.

---

## 6. Relacionado
- Paridad Hermes P3 (ejecutar código real) — este bloque LO cumple · P6 (sandbox propio) · P8
  (instalar programas) del bloque PRODUCTO DISTRIBUIBLE · BUG-2 `sandbox.py` (la base a evolucionar) ·
  BUG-9/9b hermanos de red (el patrón) · H8 EQUIPO (los specialists podrían usar execute_code) ·
  MULTI-INSTANCIA (un sandbox por instancia) · AUTO-CONCIENCIA (misma filosofía: poder dentro de la caja).
- Memoria: [[project_execute_code]] (a crear). EXTRAS: EC-EXTRA-1 (backend local/SSH/cloud).