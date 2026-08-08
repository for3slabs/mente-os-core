# PENDIENTES · agosto 2026

**Status:** current · **Type:** pending · **Updated:** 2026-08-08 · **Owner:** brian
**Shape:** `rules/contract-pending.md` · **Rotation:** `rules/rule-pending-rotation.md`
**Verified by:** `bin/check-pendings`
**Rotado desde:** `memory/PENDIENTES.md` (histórico, 4,794 líneas — ya no recibe escrituras)

## Purpose

Los pendientes VIVOS de agosto 2026. Los cerrados se quedan en el mes donde murieron; lo abierto se
reescribe íntegro cada mes (nunca punteros: un puntero roto hace invisible un pendiente).

> ⭐ **Este archivo ES la métrica.** Si el número no baja, la deuda no baja.

---

## BLOQUE · MOTOR · Mente OS mismo, la herramienta

**Análisis.** Mente OS es **la herramienta que construimos para que For3s OS funcione** — no un
proyecto aparte (Brian, 2026-08-08). v2 ya gobierna: 201 checks, 3 niveles de reglas, veredicto en
2 capas. Lo que queda son **piezas del v1 que nunca se migraron** y reglas escritas que nadie aplicó
a sí mismas.

**Plan global:** ✅ `docs/plans/PLAN-GLOBAL-motor.md` — el orden de los 7 y por qué.
Criterio de Brian (2026-08-08): **lo que desbloquea a otro primero**. Cada pendiente lleva
además su propio plan de implementación.

### V2-1 · Partir la arquitectura: 2,471 líneas contra un techo de 800

- **Prioridad:** 🔴 urgente
- **Estado:** cerrado
- **Creado:** 2026-07-29 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` · `rules/contract-document.md`
- **Plan:** `docs/plans/PLAN-V2-1-arquitectura.md`
- **Depende de:** —

**Descripción.** La regla `§3.2-QUATER` fija el techo de una arquitectura en **800 líneas**. Medido
el 2026-08-08: **2,471** — más de 3×. Es el archivo más citado del sistema, así que partirlo mal
rompe decenas de referencias `§`.
⚠️ **Ya se intentó una vez** (julio, `blk-split-architecture`) y el resultado hoy es **74% duplicado**
en `docs/architecture/` con 330 líneas viviendo solo en el original: **la partición creó la
divergencia que debía evitar**. Por eso `principles/expertise/doc-structure.md` §2.1 abrió la excepción de *fuente de
verdad* — y este archivo es candidato a reclamarla. ⭐ **La decisión previa no es cómo partirlo, sino
si debe partirse**, y esa es de Brian.

✅ **CERRADO 2026-08-08 — y el trabajo real no era partir nada.** Medido al implementarlo: la
excepción **ya estaba escrita** en la cabecera del archivo y `bin/check-blocks` la respetaba;
**`bin/check-health` la ignoraba** y seguía avisando del mismo documento. 🔴 **El sistema se
contradecía a sí mismo**, que es la forma más rápida de enseñar a ignorar avisos.
⭐ **La lectura de `Exempt:` se movió a `bin/mente_config.py`**, que ambos ya importaban: tener una
copia en un validador y ninguna en el otro **era la causa**, no el síntoma. Una regla interpretada
dos veces son dos reglas.
🔬 **Verificado por sabotaje en las dos direcciones:** sin la exención **ambos** avisan; con ella
**ambos** callan.

### V2-2 · Renombrado a la convención inglesa: quedan 28 archivos

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `rules/NAMING_CONVENTION.md` §7.4 (el plan completo ya escrito)
- **Plan:** `docs/plans/PLAN-V2-2-renombrado.md`
- **Depende de:** —

**Descripción.** Brian decidió en julio: *"no renombramos a los 208, eso será un pendiente de v2."*
📊 **Medido 2026-08-08: quedan 28**, no 208 — la migración v1→v2 se llevó la mayoría por el camino.
Bajó de 🔴 a 🟢 porque el daño real (rutas rotas al citar) ya lo cubren `check-links` y el candado de
citas de la batería.

✅ **RESUELTO EL CONFLICTO 2026-08-08** (Brian delegó la decisión). **Mandan los contratos:** un
contrato nombra un archivo para que **un validador lo encuentre** — renombrarlo rompe un mecanismo;
esta convención dice cómo se **lee** — perderla cuesta legibilidad, no función.
Queda escrito en `rules/NAMING_CONVENTION.md` §4.3-bis, con su límite: **solo cubre un nombre que un
contrato dicta por escrito**, no un archivo que a alguien le parezca importante.
⬜ **El renombrado en sí sigue abierto** — los ~16 archivos candidatos esperan su turno (orden 7 de 7).

### V2-3 · El sistema de encarpetado no está terminado

- **Prioridad:** 🟠 medio
- **Estado:** cerrado
- **Creado:** 2026-07-29 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `piezas.tsv` · `bin/check-structure` · la raíz de `Mente/`
- **Plan:** `docs/plans/PLAN-V2-3-encarpetado.md`
- **Depende de:** `V2-1` (la arquitectura declara el árbol objetivo)

**Descripción.** El encarpetado quedó **mixto**: 14 carpetas en la raíz de `Mente/`, unas del motor
(`bin/ hooks/ rules/ principles/`) y otras de la instancia (`Cerebro/ memory/ secrets/`), sin que la
frontera esté en el árbol. `mente.config.yml` ya declara esa línea desde el 31-jul y
`blk-separacion-motor-instancia` demostró que **mover archivos no era lo que hacía falta** — pero la
mezcla sigue haciendo que un clon tenga que aprenderla leyendo, no viéndola.

✅ **CERRADO 2026-08-08.** La frontera **sale del docstring y pasa a ser dato**: `frontier_engine` ·
`frontier_instance` · `frontier_mixed` en `mente.config.yml` y en su plantilla, leídas por
`cfg.frontier()`.
⚠️ **Se declaran como 3 claves planas, no como un bloque anidado**: el parser del config maneja DOS
niveles a propósito (*"un parser general escrito a mano es un generador de bugs"*), y un tercer
nivel **aplanaba los grupos en una sola lista** — perdiendo justo lo que se quería declarar. Medido
antes de elegir la forma.
🔬 **2 checks nuevos**, vistos en rojo por sabotaje: una carpeta sin clasificar hace caer la batería.
⛔ **No se movió ningún archivo** — `blk-separacion-motor-instancia` ya midió que ninguno estorbaba.

### V2-4 · Reestructuración del Mente OS Maestro

- **Prioridad:** 🟠 medio
- **Estado:** pausado
- **Creado:** 2026-07-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `Maestro/` (sub-repo con su propio git) · `bridges/Puentes_Mente_OS.md`
- **Plan:** `docs/plans/PLAN-V2-4-maestro.md`
- **Depende de:** —

**Descripción.** Brian pidió evaluar el Maestro *"porque de eso viene lo de NavigoX"*. Lo que se
probó **funciona** (permisos fail-closed, el controlador apunta en vez de replicar); lo que falta es
la reestructuración de fondo. **Pausado**, no muerto: Foresito lo lee EN VIVO como agente maestro,
así que tocarlo sin plan afecta a un agente en producción.

### V2-5 · Limpieza de configuración — lo urgente ya se hizo

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `.claude/settings.json` · `rules/rule-config-hygiene.md`
- **Plan:** `docs/plans/PLAN-V2-5-config.md`
- **Depende de:** —

**Descripción.** El mecanismo está escrito (arquitectura §12-SEPTIES + F5-5 del plan) y **lo urgente
se ejecutó el 27-jul**. Queda el barrido de fondo. Bajó a 🟢 porque `blk-distribucion` ya convirtió
las 3 rutas absolutas en **24 reglas portables** sobre `$CLAUDE_PROJECT_DIR`, que era el daño real.

### V2-6 · Lo que quedó abierto de F0

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-07-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `docs/plan-v2-rollout.md`
- **Plan:** `docs/plans/PLAN-V2-6-f0-abierto.md`
- **Depende de:** —

**Descripción.** F0 cerró 4/4 tickets pero dejó **4 cosas sin hacer** que nunca se convirtieron en
pendientes propios. ⚠️ **Requiere leer el plan antes de estimarlo**: la lista vive ahí, no aquí.

### V2-7 · La primera rotación de pendientes — ESTE trabajo

- **Prioridad:** 🔴 urgente
- **Estado:** cerrado
- **Creado:** 2026-07-29 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `memory/PENDIENTES.md` · `rules/contract-pending.md` · `bin/check-pendings`
- **Plan:** `docs/plans/PLAN-V2-7-rotacion.md`
- **Depende de:** —

**Descripción.** El archivo de pendientes era, él mismo, un pendiente: **4,794 líneas · 348 KB**,
mezclando 30 secciones cerradas con 46 abiertas. Se cierra cuando **los 87 ítems v1 estén migrados
a este formato** y `PENDIENTES.md` quede como histórico de solo lectura.
📊 Estado: contrato ✅ · regla ✅ · validador ✅ · bloques v2 ✅ · **bloques v1 ⬜ en curso**.

✅ **CERRADO 2026-08-08 — migrados UNO POR UNO**, decisión de Brian.
📊 **92 ítems** extraídos del histórico (no 87: el conteo anterior era una estimación), cada uno con
sus 3 fechas, prioridad, estado, archivos de referencia y **la línea exacta del histórico de la que
viene**. Los 8 pendientes que solo *agrupaban* desaparecen; los que describían trabajo concreto
(P-5 bugs · P-7 seguridad) se quedan.
🔬 **La aritmética cuadra exacta: 27 − 8 + 92 = 111.** Nada perdido, nada duplicado.
🔴 **Un defecto propio, cazado a tiempo:** el primer script cortaba *"desde `### X` hasta el
siguiente `###`"* y **saltaba por encima del encabezado `## BLOQUE` que vivía entre medias**,
borrándolo. Se reescribió cortando por LÍNEAS, con la regla de que un encabezado de bloque siempre
detiene el salto. Restaurado desde copia y reprobado.

### V2-8 · 🔴 Un clon ajeno hereda el nombre de Brian en sus reglas de proyecto

- **Prioridad:** 🔴 urgente
- **Estado:** cerrado
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** — (nació en la auditoría profunda del 08-08)
- **Archivos de referencia:** `bin/init` · `templates/` · `PROJECT-RULES.md` · `bin/test-f0-f6`
- **Plan:** —
- **Depende de:** —

**Descripción.** 🔬 **Medido en un clon limpio con un dueño ajeno** (`owner: Auditor Externo`):
`PROJECT-RULES.md` llega con **11 menciones a "Brian" y 0 al dueño real**. `bin/init` sin `--force`
detecta que el archivo `DIFFERS` y **se niega a regenerarlo**, que es la conducta correcta para no
pisar ediciones — pero **no dice que el archivo lleva la identidad de otra persona**, así que el
dueño nuevo no sabe que debe ejecutar `--force`.

📊 Recorrido medido: clon en frío **6 fallos** → `init` **2** → `init --force` **1** (y ese 1,
`registered=no`, es la respuesta correcta). Con `--force`: Brian **11 → 0**, dueño real **0 → 11**.

✅ **CERRADO 2026-08-08 — y la causa raíz era más profunda que el aviso.** Al abrir el código:
`CLAUDE.md` y `PROJECT-RULES.md` **estaban COMMITEADOS**, así que el clon los recibía *antes* de
que `init` corriera. Avisar no bastaba: **salieron del repo** (`.gitignore`), como `docs/WORKSPACE.md`
el 07-ago. Verificado primero que las plantillas los reproducen.
De paso, 2 defectos que solo se ven ejecutándolo: `init` copiaba la cabecera `<!-- PLANTILLA -->`
al archivo generado, y `DIFFERS` no distinguía *"lo edité yo"* de *"esto es de otra persona"*.
📊 **Medido en un clon nuevo con `owner: Auditor Externo`, sin `--force`:** "Brian" **11 → 0**,
dueño real **0 → 11** · batería del clon **197/1**, y ese 1 (`registered=no`) es la respuesta
correcta. ⭐ El README declara ahora `bin/init` como **paso uno**, con su coste escrito.

### V2-9 · `piezas.tsv` declara 23 piezas y ningún validador

- **Prioridad:** 🟠 medio
- **Estado:** cerrado
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** — (nació en la auditoría profunda del 08-08)
- **Archivos de referencia:** `piezas.tsv` · `bin/check-structure`
- **Plan:** —
- **Depende de:** —

**Descripción.** 🔬 **Sabotaje medido:** borré `bin/test-f0-f6` —la batería entera— y
`bin/check-structure` **no dijo absolutamente nada**. La causa no es el validador: `piezas.tsv`
declara 23 piezas (reglas, docs, arquitectura, memoria) y **ninguno de los 19 validadores de `bin/`**.
Sí detecta lo que sí declara: borrar `docs/STATES.md` produce el aviso correcto.

⚠️ **Consecuencia:** `piezas.tsv` es el archivo que existe para decir *"dónde vive cada pieza clave"*,
y las piezas que **hacen cumplir el sistema entero** no están en él. Si un validador desaparece —por
un merge, un rebase o un borrado— nadie avisa, y el sistema pierde una puerta **en silencio**.

✅ **CERRADO 2026-08-08.** Declaradas **20 piezas**: los 11 validadores, los 3 generadores, los 4
hooks, el instalador y la suite. 🔬 **Reprobado por sabotaje:** borrar `bin/test-f0-f6` pasa de
**silencio total** a `🔴 PIECE MOVED OR LOST · bateria`.

### V2-10 · 2 reglas escritas sin ningún script que las verifique

- **Prioridad:** 🟠 medio
- **Estado:** cerrado
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** — (nació en la auditoría profunda del 08-08)
- **Archivos de referencia:** `rules/ESTANDAR_Metodo_Fases_F.md` · `rules/case-dangerous-default.md` · `bin/test-f0-f6`
- **Plan:** —
- **Depende de:** —

**Descripción.** 📊 **Medido: 21 de 23 reglas tienen script; 2 no.** El registro del 05-ago decía
*"las 20 reglas ya tienen script"* y era cierto entonces — **se escribieron 3 reglas nuevas después
y el cableado no las siguió**.

⭐ **Por qué importa, con la ley del propio sistema:** *una regla en código se cumple 100%; una que
solo vive en un documento, 40-60%*. `ESTANDAR_Metodo_Fases_F` gobierna **cómo se hace todo trabajo
grande** y hoy se cumple por memoria. ⚠️ Es exactamente el defecto que destapó que
`rule-shipping-flow` se cumplió **0 de 15 veces** siendo solo documento.

✅ **CERRADO 2026-08-08 — con un matiz que cambia el check.** No se exige que un SCRIPT verifique
cada regla: hay reglas de **metodología** (cómo se trabaja) que ningún validador puede medir sin
inventar criterio (ADR-003). Se exige que la regla **LLEGUE a alguien** — un validador, un hook,
`base-rules.md` o el §D de un bloque. **Una regla que nadie nombra es una regla que nadie recibe.**
🔬 **Reprobado por sabotaje:** una regla nueva sin cablear hace caer el check.
⭐ Y así el conteo deja de envejecer: *"las 20 reglas ya tienen script"* era cierto el 05-ago y
falso tres reglas después. **Un número es correcto una vez; un check lo es siempre.**

### V2-11 · 🔴 `grade-block` contaba los TESTS como código muerto

- **Prioridad:** 🔴 urgente
- **Estado:** cerrado
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** 2026-08-08
- **Arrastrado desde:** — (nació en el diagnóstico del 08-08)
- **Archivos de referencia:** `bin/grade-block` (`dead_code`) · `bin/test-f0-f6`
- **Plan:** —
- **Depende de:** —

**Descripción.** 🔬 **Medido en `blk-demo`:** los **4 tests de caminos críticos** escritos días antes
(`apagar` · `hablar` · `autorizar` · `entrar`) aparecían como `dead files`, y el bloque caía de
🟢 PRODUCT a **🔴 MVP**. ⭐ **El veredicto empeoraba POR HABER ESCRITO TESTS** — apuntaba justo al
revés de lo que el sistema exige.

**La causa:** `dead_code` mide "0 importadores = muerto". Un corredor (vitest/pytest) recolecta los
tests **por nombre de archivo**, así que *nadie los importa nunca*: ese es su estado **sano**.

✅ **CERRADO el mismo día.** ⛔ **La exención NO es por carpeta** —eso perdonaría cualquier basura
bajo `tests/`— sino **por nombre que un corredor recolecta**: `.test` · `.spec` · `test_` ·
`conftest`. 🔬 **Probado en las dos direcciones** sobre un bloque de usar y tirar: el test se exime y
un huérfano en la misma carpeta **sigue contando**. 🔬 **Y visto en rojo por sabotaje**: sin la
exención, los 2 checks nuevos caen.
📊 `demo`: **4 → 0** archivos muertos · veredicto **🔴 MVP → 🟡** · batería **208 → 210**.

⭐ **El patrón, por tercera vez esta semana:** el archivo estaba bien y **el medidor leía mal**
(como `grade-block` con el runbook y `generate-index` con los `✅`). **Se corrige quien LEE.**

---

## BLOQUE · PRODUCTO-FOR3S-OS · el agente y su deuda

**Análisis.** El producto en producción: bot Telegram contenerizado, multi-instancia, canal API.
Su deuda viene de junio-julio y está **congelada por decisión de Brian** en su mayor parte
(*"registrados, NO desarrollar aún"*). ⚠️ Congelado **no** es cerrado: rota cada mes hasta que se
resuelva o se elimine con razón escrita.

**Plan global:** ⬜ **no escrito todavía** — se llamará `PLAN-GLOBAL-producto-for3s-os` cuando exista.

### P-5 · Bugs y código huérfano de PR4-A — quedan 2 de 21

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-06-29 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** ⚠️ los declara el registro histórico — **verificar contra código antes de tocar**
- **Plan:** —
- **Depende de:** —

**Descripción.** La auditoría a fondo *"mirar lo que nadie mira"* encontró 21 hallazgos, **19 ya
cerrados**. 🔴 Urgente porque el registro los marcaba *"varios CRÍTICOS"* y llevan mes y medio
abiertos. ⚠️ **Primer paso obligatorio: reverificar que siguen existiendo** — el código cambió mucho
desde el 29-jun y arrastrar un bug ya muerto es exactamente lo que esta rotación existe para evitar.

### P-7 · Seguridad — riesgos aceptados que hay que revisar

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-06-30 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** el registro histórico §SEGURIDAD
- **Plan:** ⬜ conviene
- **Depende de:** —

**Descripción.** La sección declara varios riesgos **aceptados a conciencia por Brian**, no
olvidados (ej. SEC-1, token de GitHub). 🔴 no porque estén rotos, sino porque **un riesgo aceptado
se revisa periódicamente**: lo que era defendible en junio con una demo interna deja de serlo el día
que un cliente externo dependa del sistema.

### BUG-1 · ~~BUG-1 (texto original)~~ **DECAY de memoria MUERTO (H6 incompleto) — afecta MEMORIA.**…

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-06-29 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1905)
- **Archivos de referencia:** ⚠️ verificar contra código antes de tocar
- **Plan:** —
- **Depende de:** —

**Descripción.** ~~BUG-1 (texto original)~~ **DECAY de memoria MUERTO (H6 incompleto) — afecta MEMORIA.** `relevance.py` tiene `recalcular_relevance_lote()` pero NADIE la llama (búsqueda vacía en todo el repo) y NO está en el cron (`tasks.py`). El "Sub-paso 10" (conectar el recálculo al cron) quedó a medias. EVIDENCIA BD: 515 turnos con relevance TODOS en decil 10 (0.91-0.99, congelados desde 22-jun) + 245 nuevos con relevance NULL. La microglía filtra `relevance IS NOT NULL AND relevance < X` → siempre 0 candidatos (log:

### BUG-2 · ~~BUG-9 (texto original)~~ **GitHub MCP + web_fetch ROTOS en el contenedor (intentan lanzar…

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-06-29 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1976)
- **Archivos de referencia:** ⚠️ verificar contra código antes de tocar
- **Plan:** —
- **Depende de:** —

**Descripción.** ~~BUG-9 (texto original)~~ **GitHub MCP + web_fetch ROTOS en el contenedor (intentan lanzar `docker`).** Hallazgo 2026-06-29 (panorama). El bot NO tiene docker (decisión sin-DinD). PERO 3 componentes hermanos siguen invocando `docker run`: (1) `mcp_client.py` config_github lanza `docker run github-mcp-server` → **GitHub CAÍDO** (analizar repos falla con `FileNotFoundError: docker`); (2) `web_fetch.py` _render_headless lanza `docker run for3s-render` → web fetch de SPAs/JS degradado (solo httpx, sin r

### O-1 · **OC-E1 · /reset ligero de conversación** — borrón del CONTEXTO conversacional del hilo

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2262)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-E1 · /reset ligero de conversación** — borrón del CONTEXTO conversacional del hilo conservando memoria/perfil (hoy /reiniciar es del SERVICIO, no del hilo).

### O-2 · **OC-E2 · Sesiones aisladas desechables** para trabajo programado/subagentes — cada corrida

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2264)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-E2 · Sesiones aisladas desechables** para trabajo programado/subagentes — cada corrida = mini-sesión que muere (`sessionTarget: isolated` de OpenClaw). ES la pieza que necesita el CRON CONVERSACIONAL (§FUTURO línea ~2028) — construirlas juntas.

### O-3 · **OC-E3 · Trazar cambios de modelo/razonamiento EN el hilo** — hoy /model cambia global y no

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2267)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-E3 · Trazar cambios de modelo/razonamiento EN el hilo** — hoy /model cambia global y no queda registrado en la conversación (OpenClaw: eventos model_change/thinking_level_change).

### O-4 · **OC-E4 · Snapshot de skills/estado por sesión** — qué skills/config veía el agente en ese

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2269)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-E4 · Snapshot de skills/estado por sesión** — qué skills/config veía el agente en ese momento; para depurar "por qué respondió así" (OpenClaw: skillsSnapshot en sessions.json).

### O-5 · **OC-C1 · Multi-canal (Discord PRIMERO)** — era la sala de máquinas del agente dev (guilds

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2273)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C1 · Multi-canal (Discord PRIMERO)** — era la sala de máquinas del agente dev (guilds con permisos por canal). = el pendiente ⭐ MULTI-CANAL de §FUTURO (línea ~2036), ahora con referencia concreta: config `channels.discord` de openclaw.json (guilds/channels/requireMention).

### O-6 · **OC-C2 · Hilos nativos del canal → temas** — mapear topics de Telegram (y threads futuros)

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2276)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C2 · Hilos nativos del canal → temas** — mapear topics de Telegram (y threads futuros) a temas/sesiones: `message_thread_id` → `sesion_de(uid, tema)`. El rail de temas YA existe, falta el cable (hoy telegram_channel.py ni lee message_thread_id).

### O-7 · **OC-C3 · Tool `message` proactiva** — que el agente pueda escribirle al dueño por decisión

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2279)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C3 · Tool `message` proactiva** — que el agente pueda escribirle al dueño por decisión propia (resultado de trabajo, hallazgo), gobernada por governor + allowlist. Hoy solo alertas cableadas (health). OpenClaw: tool message, 64 usos reales en dev.

### O-8 · **OC-C4 · Streaming/edición parcial de respuestas largas** — ver crecer la respuesta

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2282)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C4 · Streaming/edición parcial de respuestas largas** — ver crecer la respuesta (OpenClaw: `streaming: "partial"` editando el mensaje). UX.

### O-9 · **OC-C5 · Salida de archivos al chat** — generar y MANDAR .md/.docx/.pdf (send_document).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2284)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C5 · Salida de archivos al chat** — generar y MANDAR .md/.docx/.pdf (send_document). For3s ya crea archivos en el sandbox pero no puede entregarlos.

### O-10 · **OC-C6 · Entrada de VOZ** — revertir la decisión de diseño "audio fuera" (multimodal.py):

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2286)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C6 · Entrada de VOZ** — revertir la decisión de diseño "audio fuera" (multimodal.py): transcripción de notas de voz. (Ya existía nota en §FUTURO sobre voz — unificar al construir.)

### O-11 · **OC-C7 · Multi-cuenta/bindings** — varios bots (personal/dev/watchdog) sirviendo agentes o

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2288)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-C7 · Multi-cuenta/bindings** — varios bots (personal/dev/watchdog) sirviendo agentes o modos distintos desde UNA instalación (OpenClaw: channels.accounts + bindings agente↔cuenta). Hoy eso exige multi-instancia completa.

### O-12 · **OC-M1 · ⭐ Diario/bitácora propia del agente** — que Foresito ESCRIBA su día ("qué aprendí,

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2293)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-M1 · ⭐ Diario/bitácora propia del agente** — que Foresito ESCRIBA su día ("qué aprendí, qué quedó pendiente") en lugar legible; casa natural: persona/mente-os/Doc/. La pieza de OpenClaw con más alma (diarios memory/AAAA-MM-DD.md + archivado). El diario_cambios actual solo registra auto-mods de código. Rail: DMN nocturno puede redactarlo.

### O-13 · **OC-M2 · Learnings por tema/proyecto** — "learnings.md del proyecto X": resumen curado y

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2297)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-M2 · Learnings por tema/proyecto** — "learnings.md del proyecto X": resumen curado y ACUMULATIVO por tema (OpenClaw: memory/acompanante/<proyecto>/learnings.md). Rails: temas + tema_estado (C1) ya existen.

### O-14 · **OC-M3 · Índice de memoria curado de largo plazo** — el "MEMORY.md" de Foresito: resumen

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2300)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-M3 · Índice de memoria curado de largo plazo** — el "MEMORY.md" de Foresito: resumen maestro SIEMPRE presente que el propio agente mantenga. Hoy inyectamos lo RELEVANTE al turno; falta lo PERMANENTE elegido por él (OpenClaw: 15K chars siempre en prompt).

### O-15 · **OC-M4 · memory_search como TOOL del loop** — que el AGENTE decida buscar más memoria a

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2303)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-M4 · memory_search como TOOL del loop** — que el AGENTE decida buscar más memoria a mitad del razonamiento (hoy la recuperación corre 1 vez, antes del turno). `memoria.recordar()` ya es la fachada — exponerla como tool.

### O-16 · **OC-M5 · Skills como paquetes portables + marketplace** — skills con scripts/assets

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2306)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **OC-M5 · Skills como paquetes portables + marketplace** — skills con scripts/assets ejecutables, instalables/publicables (el clawhub de OpenClaw). Las nuestras son conocimiento en BD, no herramientas empaquetadas. Visión producto (grande).

### H-1 · **HG-1 → amplía OC-C1 (multi-canal):** hacerlo con el patrón Hermes — capa de canal como

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2330)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-1 → amplía OC-C1 (multi-canal):** hacerlo con el patrón Hermes — capa de canal como CONTRATO formal (clase base + registry + UN gateway para N plataformas, un documento "ADDING_A_PLATFORM" (así lo llama Hermes; aquí no existe)) + **continuidad cross-canal** (la MISMA conversación sigue de Telegram a consola a Discord; sesiones etiquetadas por source en un store único).

### H-2 · **HG-2 → amplía OC-C6 (voz):** no solo ENTRADA (transcripción); también **SALIDA — TTS y

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2334)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-2 → amplía OC-C6 (voz):** no solo ENTRADA (transcripción); también **SALIDA — TTS y voice_mode interactivo** (Hermes: transcription_tools + tts_tool + voice_mode).

### H-3 · **HG-3 → = OC-C3/C4/C5** (send_message proactivo · streaming · media out) — sin cambios,

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2336)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-3 → = OC-C3/C4/C5** (send_message proactivo · streaming · media out) — sin cambios, Hermes confirma las tres.

### H-4 · **HG-5 → amplía OC-M4 (memory_search tool):** además de memoria semántica bajo demanda,

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2338)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-5 → amplía OC-M4 (memory_search tool):** además de memoria semántica bajo demanda, tool para HOJEAR la propia historia conversacional cruda (Hermes session_search: 3 modos discovery/scroll/bookends sobre FTS, costo LLM cero; nosotros lo haríamos sobre Postgres).

### H-5 · **HG-6 → amplía OC-M1/M3 (memoria curada del agente):** matiz de diseño CLAVE de Hermes —

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2341)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-6 → amplía OC-M1/M3 (memoria curada del agente):** matiz de diseño CLAVE de Hermes — el MEMORY/USER curado entra al prompt como **snapshot CONGELADO por sesión** (escrituras a mitad de sesión van a disco pero NO tocan el prompt → preserva el prefix cache; refresca al siguiente arranque). Copiar este patrón al construir OC-M1/M3.

### H-6 · **HG-9 → amplía OC-M5 (skills-paquete/marketplace):** con el modelo de seguridad de Hermes:

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2345)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-9 → amplía OC-M5 (skills-paquete/marketplace):** con el modelo de seguridad de Hermes: lockfile de PROCEDENCIA + cuarentena + auditoría AST de skills instaladas (skills_guard) + estándar abierto agentskills.io.

### H-7 · **HG-10 → amplía OC-E2/cron conversacional:** sumar **catálogo de SUGERENCIAS** (el agente

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2348)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-10 → amplía OC-E2/cron conversacional:** sumar **catálogo de SUGERENCIAS** (el agente propone automatizaciones: suggestion_catalog) + blueprints (recetas) + output persistido por corrida (`cron/output/<job>/<ts>.md`) + delivery del resultado a cualquier canal.

### H-8 · **HG-17 → ya en §EXTRAS como H·BYOK** (multi-proveedor de modelos) — Hermes lo valida

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2351)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-17 → ya en §EXTRAS como H·BYOK** (multi-proveedor de modelos) — Hermes lo valida (adapters Anthropic/Bedrock/Gemini/OpenAI + `hermes model` en vivo + credential_pool).

### H-9 · **HG-4 · TUI de consola seria** — nuestro modo consola es plano; Hermes trae TUI real:

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2355)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-4 · TUI de consola seria** — nuestro modo consola es plano; Hermes trae TUI real: autocomplete de comandos, multiline, historial, interrupt-and-redirect, streaming de tool output. (chica)

### H-10 · **HG-7 · ⭐ NUDGES de persistencia y skills EN el turno** — el loop de conversación empuja

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2358)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-7 · ⭐ NUDGES de persistencia y skills EN el turno** — el loop de conversación empuja periódicamente al agente a (a) persistir conocimiento importante y (b) crear skill tras tarea compleja (skill_nudge_interval). Hoy nosotros esperamos a la NOCHE (DMN); el nudge cierra el loop de aprendizaje en caliente. (media, MUCHO valor)

### H-11 · **HG-8 · ⭐ CURATOR de skills por inactividad** — agente de fondo que se dispara cuando el

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2362)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-8 · ⭐ CURATOR de skills por inactividad** — agente de fondo que se dispara cuando el sistema está idle (no cron) y MANTIENE las skills creadas: consolida duplicadas, archiva muertas, parcha rotas, con estado propio. Nuestro DMN crea skills pero nadie las mantiene. Rail: dmn_idle ya existe. (media)

### H-12 · **HG-11 · todo/kanban como TOOL del agente** — que el AGENTE gestione su lista de trabajo

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2366)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-11 · todo/kanban como TOOL del agente** — que el AGENTE gestione su lista de trabajo como herramienta del loop (Hermes: todo_tool + kanban con watchers). Nuestro tema_estado (C1) es comando del USUARIO; falta la versión agente. (chica)

### H-13 · **HG-12 · clarify estructurado como tool** — H10 metacognición YA detecta baja confianza;

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2369)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-12 · clarify estructurado como tool** — H10 metacognición YA detecta baja confianza; falta exponer "pedir aclaración con opciones estructuradas" como tool del loop en vez de solo texto libre. (chica)

### H-14 · **HG-13 · checkpoints de archivos en el sandbox** — snapshot automático antes de que el

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2372)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-13 · checkpoints de archivos en el sandbox** — snapshot automático antes de que el agente edite un archivo (checkpoint_manager) → deshacer barato por archivo. (chica)

### H-15 · **HG-14 · ⭐ execute_code que llama TOOLS vía RPC** — la idea más potente de Hermes: el

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2374)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-14 · ⭐ execute_code que llama TOOLS vía RPC** — la idea más potente de Hermes: el modelo escribe UN script Python que invoca las tools del agente (stub autogenerado, socket) → un pipeline de N turnos se colapsa a 1 turno con costo de contexto CERO. Encaja natural con nuestro sandbox por HTTP (EC-3). (grande)

### H-16 · **HG-15 · toolsets restringidos por contexto** — qué tools ve el agente según canal/rol/

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2378)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-15 · toolsets restringidos por contexto** — qué tools ve el agente según canal/rol/ subagente (Hermes: toolsets configurables + toolset restringido por hijo delegado). Hoy nuestro tool-loop es uno solo; cruza con H8 (subagentes) y multiusuario (roles). (media)

### H-17 · **HG-16 · browser / computer-use / web_search / generación de imagen** — por partes:

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2381)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-16 · browser / computer-use / web_search / generación de imagen** — por partes: web_search como tool del loop (hoy solo web_fetch reactivo) → browser real (Hermes: Camoufox/CDP con supervisor) → computer_use → image/video gen. (grande, por fases)

### H-18 · **HG-18 · i18n del agente** — respuestas/UI en idioma configurable (Hermes: locales/).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2384)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **HG-18 · i18n del agente** — respuestas/UI en idioma configurable (Hermes: locales/). Hoy Foresito es es-MX nativo; importa para DISTRIBUCIÓN. (chica)

### H9-1 · **H9-D1 · cache_prewarming REAL — requiere stats de hit/miss en cache.py.** Hoy

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3100)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D1 · cache_prewarming REAL — requiere stats de hit/miss en cache.py.** Hoy `cache.py` solo tiene get/set, no cuenta aciertos/fallos → el task es STUB (trigger siempre False). Falta: (1) contadores de hit/miss por patrón en Valkey; (2) `cache.stats_recientes(pool, ws)` (hit_rate + misses recurrentes); (3) que la action pre-compute respuestas a los patrones frecuentes que fallan. Outcome medible: hit-rate antes vs después (ROI real). Diseño base: R5 §3.2.

### H9-2 · **H9-D2 · routing_learning REAL — requiere router multi-modelo.** STUB hoy: For3s no

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3106)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D2 · routing_learning REAL — requiere router multi-modelo.** STUB hoy: For3s no tiene enrutamiento multi-modelo activo (H7 enrutamiento BLOQUEADO por decisión — suscripción plana). Sin rutas que aprender, el task no aplica. Se llena cuando exista routing real (API key de pago / cliente). Cruza con H7. Diseño: R5 §3.4.

### H9-3 · **H9-D3 · eval_regression_detection con GOLDEN SET formal.** v1 usa una métrica simple

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3110)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D3 · eval_regression_detection con GOLDEN SET formal.** v1 usa una métrica simple (% respuestas vacías 24h) como proxy. Falta el framework de eval real (R3 §4.4): golden set + baseline + score + REGRESSION_THRESHOLD + alerta. Es el GUARDIÁN de la calidad de todo el sistema → importante cuando haya clientes. Cruza con H14 (observabilidad) y R8.

### H9-4 · **H9-D4 · prompt_improvement REAL = AUTO-CONCIENCIA AC3.** STUB hoy (trigger False):

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3114)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D4 · prompt_improvement REAL = AUTO-CONCIENCIA AC3.** STUB hoy (trigger False): auto-proponer cambios a la PROPIA personalidad/prompts es máximo cuidado. Se construye junto con el pendiente [[AUTO-CONCIENCIA AC3]] (auto-modificar código): propondría mejoras de prompt a `dmn_propuestas`, NUNCA auto-editaría FOR3S_ROLE. Diseño: R5 §4.3.

### H9-5 · **H9-D5 · "valor medible" fino del ROI (R5 §6 completo).** H9-d v1 mide costo + corridas

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3118)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D5 · "valor medible" fino del ROI (R5 §6 completo).** H9-d v1 mide costo + corridas + recomendación simple (keep/revisar). Falta el VALOR por task con su métrica propia (cache→hit-rate↑, eval→bugs cazados, consolidation→calidad del KG, hypothesis→hipótesis confirmadas) para un ratio valor/costo real + auto-suggest disable. Tabla en R5 §6.

### H9-6 · **H9-D6 · auto-improvement loop de las generativas (R5 §5).** Hoy las generativas dejan

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3122)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D6 · auto-improvement loop de las generativas (R5 §5).** Hoy las generativas dejan propuestas y el dueño decide. El diseño R5 §5 contempla un loop: propuesta → governor → review → approval → promote → MEDIR resultado → realimentar. Falta el "medir + realimentar" (cerrar el lazo de aprendizaje). Reusa el governor (H11) ya construido.

### H9-7 · **H9-D7 · interaction graph entre tasks (R5 §7).** v1 corre las 8 tasks independientes.

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3126)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D7 · interaction graph entre tasks (R5 §7).** v1 corre las 8 tasks independientes. R5 §7 define contratos entre ellas (ej. embedding_precompute alimenta a memory_consolidation; eval_regression vigila a las demás). Orquestar dependencias.

### H9-8 · **H9-D8 · pattern_detection afinado.** Hoy reusa proponer_skill_auto de H12 con un

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3129)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **H9-D8 · pattern_detection afinado.** Hoy reusa proponer_skill_auto de H12 con un trigger simple (≥10 turnos/24h + autogen ON). Falta detección REAL de patrones repetidos (no solo "hay material") — agrupar tareas similares recurrentes antes de proponer skill.

### H10-1 · **HP1 · Señales 4/5/6/8 reales** (hoy neutras honestas): cost_accuracy (medir estimado

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3146)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **HP1 · Señales 4/5/6/8 reales** (hoy neutras honestas): cost_accuracy (medir estimado vs real por turno), plan_consistency (requiere plan-then-execute formal HP4), multi_agent_consensus (calcular cuando corre el equipo H8), rule_eval (requiere golden set = misma deuda H9-D3). Cada una se llena sin tocar el resto. R6 §6.1.2.

### H10-2 · **HP2 · Confidence en tool-loop GitHub y en el equipo.** v1 solo aplica en

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3150)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **HP2 · Confidence en tool-loop GitHub y en el equipo.** v1 solo aplica en conversation.send (chat). Falta evaluar confianza en send_with_tools (¿las tools dieron lo esperado?) y en las corridas de equipo (consensus entre specialists). R6 §6.1.2.

### H10-3 · **HP3 · llm_self_report más fino.** v1 infiere la confianza del FRASEO de la respuesta

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3153)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **HP3 · llm_self_report más fino.** v1 infiere la confianza del FRASEO de la respuesta (marcadores de duda, sin 2ª llamada LLM). Opción futura: pedir al modelo un score explícito de confianza (más preciso pero +1 llamada/turno). Calibrar costo-vs-precisión.

### H10-4 · **HP4 · Plan-then-execute formal (motor PFC completo).** v1 mide confianza del TURNO,

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3156)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **HP4 · Plan-then-execute formal (motor PFC completo).** v1 mide confianza del TURNO, no descompone en un PFCPlan con steps/checkpoints (R6 §6.1.1). El motor de planeación multi-step (plan → ejecutar paso a paso → checkpoint) es grande; v1 es la metacognición "ligera". Se construye cuando se necesite ejecución compleja gobernada por confianza.

### H10-5 · **HP5 · Check loop con RE_PLAN_PARTIAL.** v1 en baja confianza solo AVISA / pide

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3160)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **HP5 · Check loop con RE_PLAN_PARTIAL.** v1 en baja confianza solo AVISA / pide aclaración. El R6 §6.1.3 define re-planear automático (preservando steps exitosos, budget de re-plans, escalado por severidad). Requiere HP4. Decisión Brian: v1 solo avisa.

### H10-6 · **HP6 · Workspace controls del confidence** (R6 §5.4.3): human_in_loop_on_critical,

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3163)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** —
- **Depende de:** —

**Descripción.** **HP6 · Workspace controls del confidence** (R6 §5.4.3): human_in_loop_on_critical, max_re_plans_per_plan, thresholds por workspace. Para multi-tenant / clientes.

### DT-1 · **QA-3b · Limpiar los 72 errores de tipo del resto del repo (gradual, para ampliar el…

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-06-18 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3441)
- **Archivos de referencia:** ⚠️ los declara el registro histórico
- **Plan:** —
- **Depende de:** —

**Descripción.** **QA-3b · Limpiar los 72 errores de tipo del resto del repo (gradual, para ampliar el bloqueo).** Módulo por módulo, arreglar los diagnostics reales de `ty` (o `# type: ignore` justificado en el ruido de ty experimental) → ir ampliando la lista de módulos del step bloqueante hasta cubrir todo. No urgente.

### DT-2 · **QA-3b v3 (queda, menor):** limpiar los 3 sucios finales — telegram_channel (59, el…

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-06-18 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3551)
- **Archivos de referencia:** ⚠️ los declara el registro histórico
- **Plan:** —
- **Depende de:** —

**Descripción.** **QA-3b v3 (queda, menor):** limpiar los 3 sucios finales — telegram_channel (59, el grande, gradual), conversation (7), cache (1, invalid-return-type). No urgente.

### DT-3 · **#2 Dependabot (checkout 4→7)** — bloqueado por branch-protection strict (rama…

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-06-18 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3553)
- **Archivos de referencia:** ⚠️ los declara el registro histórico
- **Plan:** —
- **Depende de:** —

**Descripción.** **#2 Dependabot (checkout 4→7)** — bloqueado por branch-protection strict (rama desactualizada tras mis pushes); Dependabot lo rebasa solo, se completa cuando su CI termine. Bajo riesgo, sin acción.

### F-1 · **Webhooks GitHub async + multi-tenant** — SIGUEN DIFERIDOS (H futuros, como

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3596)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **Webhooks GitHub async + multi-tenant** — SIGUEN DIFERIDOS (H futuros, como R4 los escalonó). Análisis 2026-06-18 confirmó BLOQUEADORES reales: • **Ingreso de red:** GitHub no puede mandar webhooks al server (red doméstica que parpadea, IP inestable). Falta desplegar Cloudflare Tunnel (está en diseño R10, NO desplegado). Solo hay Tailscale (plano admin). • **Hueco de diseño:** R4.2.1 define el TRANSPORTE del webhook (recibir/ validar HMAC/encolar con Arq) pero NUNCA qué H

### F-2 · **Mini-agente HTTP en el server for3s para control de contenedores (demo del sitio).**

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3621)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **Mini-agente HTTP en el server for3s para control de contenedores (demo del sitio).** La demo del sitio público (marca-personal) tiene un toggle "encender/apagar agente" por usuario 1:1 (Jazz/Mashe/Brian) que debe hacer `docker start/stop` de su contenedor `for3s-demo-<kind>` en el server. PROBLEMA: la web corre en Vercel, que NO está en la red Tailscale del server → no puede ejecutar `docker` directo. Hoy el toggle solo guarda el estado en BD (`demo_users.agent_on`) y despacha la

### F-3 · **Sistema tipo Notion / notas estructuradas** — hoy solo hay historial

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3677)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **Sistema tipo Notion / notas estructuradas** — hoy solo hay historial conversacional en Postgres, no un sistema de notas/conocimiento navegable. (Relacionado con H-C sistema de pensamiento.)

### F-4 · **⚡ CACHE 1h para los 5 agentes For3s (Brian 2026-07-07)** — mejora REAL derivada de la

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3680)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **⚡ CACHE 1h para los 5 agentes For3s (Brian 2026-07-07)** — mejora REAL derivada de la investigación del cache de Anthropic. En los agentes For3s SÍ controlamos `llm.py`, así que aplicar `cache_control {"ttl":"1h"}` al system prompt (identidad+memoria, la parte estable y grande) → cuando un agente está idle < 1h su prefijo se mantiene caliente 12× más → **menos reenvíos = menos consumo de la suscripción COMPARTIDA** (1 cupo para los 5). Verificar primero que el provider ya usa cache

### F-5 · **⚡ RE-EVALUAR cache/keep-alive de Claude Code (Brian 2026-07-07, revisión periódica)** — la

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3687)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **⚡ RE-EVALUAR cache/keep-alive de Claude Code (Brian 2026-07-07, revisión periódica)** — la idea de Brian (un "cron sombra" que refresque el cache de Anthropic cada 5 min para no reenviar la conversación al retomar) es CONCEPTUALMENTE correcta (cada cache-read resetea el TTL de 5min) pero HOY NO es construible: Claude Code no expone ningún setting de cache/TTL/keep-alive ni ningún hook por timer/idle (verificado en las 3 fuentes oficiales), y un cron externo no puede acceder al prefijo e

### F-6 · **🎭 IDENTIDADES SECUNDARIAS de OpenClaw → rasgos a la personalidad de brian (Brian…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3697)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **🎭 IDENTIDADES SECUNDARIAS de OpenClaw → rasgos a la personalidad de brian (Brian 2026-07-05)** — ⛔ REGLA LOCKED: la personalidad de @For3s_Brian_bot NO se altera por ahora (queda el alma Fruterito DevRel/dev tal como se aprobó en E2). Las identidades del 🍊 Empleado (Product Lead→CEO) y 🔥 For3s Design ("orchestrator of human connection through pixels") están DENTRO como MEMORIA (consultables), NO como personalidad. Este pendiente = evaluar A FUTURO (fuera del hito ENTRENAMIENTO, cuando Brian d

### F-7 · **⭐ CRON CONVERSACIONAL / recordatorios en lenguaje natural (Brian 2026-07-03; reafirmado…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3705)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **⭐ CRON CONVERSACIONAL / recordatorios en lenguaje natural (Brian 2026-07-03; reafirmado 2026-07-04)** — que el usuario diga "recuérdame cada lunes", "revisa el repo X cada mañana" y For3s programe la tarea SOLO. HOY For3s tiene jobs FIJOS (los 11 nocturnos: backup/cls/microglia/perfil/estilo…) pero NO cron conversacional (el usuario no puede crear tareas programadas hablando). **Es una de las 2 brechas para paridad de AGENTE completo con Hermes** (que sí tiene "automatizaciones programadas con cron

### F-8 · **⭐ MULTI-CANAL (Brian 2026-07-03)** — hoy For3s solo vive en Telegram + consola. Hermes…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3724)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **⭐ MULTI-CANAL (Brian 2026-07-03)** — hoy For3s solo vive en Telegram + consola. Hermes está en Telegram/Discord/Slack/WhatsApp/Signal/CLI. **Es la OTRA brecha para paridad de agente completo.** No afecta la agencia (For3s ya actúa/aprende/es autónomo), solo la OMNIPRESENCIA. Diseñar una capa de canal genérica (el core ya está desacoplado del canal). Cruza con distribución/producto. ⚠️ = OC-C1 (§BRECHAS OPENCLAW): Discord PRIMERO, con la config real de OpenClaw como referencia.

### F-9 · **Escribir/crear/editar en GitHub** — ✅ create_issue/PR/comment funcionan (fix 2026-07-03:…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3729)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **Escribir/crear/editar en GitHub** — ✅ create_issue/PR/comment funcionan (fix 2026-07-03: el MCP renombró tools, traducido en mcp_client). Ampliar a más write tools = futuro.

### F-10 · **R6 al programar:** ejecutar plan E + medir PFC_PLANNING_COST real + cargar

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3736)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **R6 al programar:** ejecutar plan E + medir PFC_PLANNING_COST real + cargar HARD NO-GO §8.4 + governor ANTES de auto-generación de skills.

### F-11 · **DMN 5.4.2 al programar:** implementar 8 action_fn + auto-improvement loop

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3738)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **DMN 5.4.2 al programar:** implementar 8 action_fn + auto-improvement loop enchufado al governor.

### F-12 · **2 reglas de oro:** (1) CI/CD temprano (Fase 0, no al final);

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3740)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** **2 reglas de oro:** (1) CI/CD temprano (Fase 0, no al final); (2) Meta-Orchestrator/governor DEBE existir ANTES de activar auto-gen (R6).

### F-13 · ⭐ **PARIDAD HERMES al programar cada hito:** llevar las 5 capacidades P1-P5

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3742)
- **Archivos de referencia:** el registro histórico §FUTURO
- **Plan:** —
- **Depende de:** —

**Descripción.** ⭐ **PARIDAD HERMES al programar cada hito:** llevar las 5 capacidades P1-P5 (ver sección "⭐ PARIDAD CON HERMES") al MISMO nivel de detalle que Hermes, en su hito ancla: **H3-H4** → P4 (MCP arbitrarios) · **H4** → P3 (ejecución de código) · **H5** → P1 (modelar al usuario, REQUIERE diseño previo) · **H8** → P2 (sub-agentes paralelo) · **H10-H12** → P5 (skills auto-generables). Directriz de Brian: son prioritarias, no opcionales.

### PH-1 · **P3 · EJECUTAR CÓDIGO REAL** (terminal/código en entornos aislados, no solo

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-06-18 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3882)
- **Archivos de referencia:** `docs/analysis/`
- **Plan:** —
- **Depende de:** —

**Descripción.** **P3 · EJECUTAR CÓDIGO REAL** (terminal/código en entornos aislados, no solo lint — Hermes corre en 6 entornos: local/Docker/SSH/Modal/Daytona…). ⚠️ **PARCIAL** — hay base pero NO ejecución arbitraria: sandbox de SKILLS (ejecuta planes generados, no código libre, R6 B2 §6.2.5 → H12) + Docker multi-tenant 3 capas para aislar workspaces (R4 B1 → H4/H8). Falta: un MCP de ejecución/terminal arbitrario. El aislamiento Docker de H4/H8 es la BASE sobre la que montarlo. → Punto: e

### HF-1 · **H8-aislamiento-multitenant** (Brian 2026-06-23) **Activar las 2 capas de aislamiento de

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 3964)
- **Archivos de referencia:** el registro histórico §HALLAZGOS DE FONDO
- **Plan:** —
- **Depende de:** —

**Descripción.** **H8-aislamiento-multitenant** (Brian 2026-06-23) **Activar las 2 capas de aislamiento de H8 que quedaron PREPARADAS pero inactivas (dependen de multi-tenant).** En H8 S9 se construyeron las capas de aislamiento que aplican a single-user (whitelist enforcement, mutation guard read-only, KEK scoping, ContextVar — todas ACTIVAS). Estas 2 quedaron preparadas/documentadas pero NO activas porque protegen contra fuga ENTRE CLIENTES, que hoy no existen (single-user): 1. **Postgres Row-Level S

### HF-2 · 🟡 **H6-backup-offsite — CÓDIGO LISTO, bloqueado por Tailscale SSH** (Brian 2026-06-22).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 4013)
- **Archivos de referencia:** el registro histórico §HALLAZGOS DE FONDO
- **Plan:** —
- **Depende de:** —

**Descripción.** 🟡 **H6-backup-offsite — CÓDIGO LISTO, bloqueado por Tailscale SSH** (Brian 2026-06-22). El MECANISMO está construido y probado: `backup.py` tiene `copiar_offsite()` (rsync+SSH, DEFENSIVA: si el destino no responde, NO rompe el backup local) integrado en `backup_y_rotar`. Destino elegido: el WSL2 de Brian = `brayaneth` (100.88.66.23, usuario brianweb3) → `~/for3s-backups-offsite`. Clave SSH del server ya generada (`~/.ssh/id_ed25519`) y autorizada en el WSL2. Config por env `FOR3S_BAC

### HF-3 · **H-B** GitHub como CUENTA PROPIA (depende de H-D).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 4080)
- **Archivos de referencia:** el registro histórico §HALLAZGOS DE FONDO
- **Plan:** —
- **Depende de:** —

**Descripción.** **H-B** GitHub como CUENTA PROPIA (depende de H-D).

### HF-4 · **H-C** sistema de pensamiento (estructura tipo Mente OS) + multi-mensaje

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 4081)
- **Archivos de referencia:** el registro histórico §HALLAZGOS DE FONDO
- **Plan:** —
- **Depende de:** —

**Descripción.** **H-C** sistema de pensamiento (estructura tipo Mente OS) + multi-mensaje SEMÁNTICO por etapas (mensaje por etapa: análisis→testeo→PoC).

### HF-5 · **H-G** (Brian 2026-06-17) **SUBAGENTE ASÍNCRONO para repos enormes.**

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 4083)
- **Archivos de referencia:** el registro histórico §HALLAZGOS DE FONDO
- **Plan:** —
- **Depende de:** —

**Descripción.** **H-G** (Brian 2026-06-17) **SUBAGENTE ASÍNCRONO para repos enormes.** Problema: el análisis "a profundidad" SIEMPRE tarda (repo enorme, leer todo el código). Hoy es síncrono → bloquea la conversación y el presupuesto de tiempo (5 min) solo alcanza ~10/74 de src. La solución NO es darle más tiempo al flujo actual. Es de OTRA CAPA, post-MVP: un **subagente en segundo plano** que analice el repo COMPLETO por detrás, mientras el agente principal de Telegram **sigue trab

---

## BLOQUE · ESTRATEGICO · lo que decide Brian, no la ingeniería

**Análisis.** Pendientes cuyo tapón **no es técnico**: esperan una decisión, una compra o una
oportunidad. Ninguno se desbloquea trabajando más.

**Plan global:** no aplica — un plan de implementación sobre una decisión ajena sería inventar
criterio (ADR-003).

### E-1 · ⭐ LA PRUEBA DE CAMPO — cero instalaciones externas

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-08-05 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `bin/init` · `CAPABILITIES.md` · `blocks/archive/distribucion_2026-08/`
- **Plan:** —
- **Depende de:** —

**Descripción.** ⭐ **El tapón único del motor.** Un clon ya verifica Mente OS sin exigir la
instancia de Brian (6 fallos → 1, y ese 1 es la respuesta correcta), **pero lo verificó la IA en
esta máquina**. Eso demuestra el mecanismo, **no la experiencia de otro dueño**. Sin una instalación
externa real, los pendientes de graphify #5-#6 solo se medirían a sí mismos.
🙋 **Necesita a Brian:** hace falta una persona ajena dispuesta a instalarlo.

### E-2 · Firma GPG de los commits

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-08-02 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** configuración de git · `rules/rule-shipping-flow.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** 🔑 **La llave es de Brian y solo él puede generarla o cederla.** Sin firma, un
commit del repo no prueba autoría — relevante el día que el motor se publique y alguien externo
tenga que confiar en su historia.

### E-3 · `~/.claude.json` — credenciales del harness, es ARQUITECTURA

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-08-02 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `rules/rule-config-hygiene.md` · `.claude/settings.json`
- **Plan:** —
- **Depende de:** —

**Descripción.** El archivo guarda credenciales del harness y **no es configuración: es
arquitectura**. ⚠️ Medido: el `deny` lee el **TEXTO** del comando, así que `"$(ls …)"` lo esquiva —
**no es un sandbox**, y tratarlo como tal es la suposición peligrosa.

### E-4 · Dominio propio — una compra que desbloquea tres frentes

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-07-23 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** configuración de Resend · el sitio en `marca-personal/`
- **Plan:** —
- **Depende de:** —

**Descripción.** UNA compra desbloquea: correos verificados en Resend (hoy `onboarding@resend.dev`
solo entrega al dueño de la cuenta) + SEO/web propia + branding. 🙋 **Brian marca el momento.**

### E-5 · Conectores self-service + identidad por correo

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-20 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `lib/demo/oauthGuard.ts` · las 3 rutas OAuth dormidas
- **Plan:** ⬜ lo necesita — es un pendiente grande
- **Depende de:** `BLOQUE · DEMO` §F-11 (las mismas rutas OAuth)

**Descripción.** Visión de OAuth de un botón + correo admin por instancia + `general` multi-tenant.
⛔ **No construir sin Ronda F0.** ⚠️ **Depende del bloque DEMO**: las 3 rutas OAuth que este pendiente
necesitaría son las mismas que allí están dormidas, así que **hay que leer los dos bloques** antes de
tocar una línea.

### SC-1 · **Foresito, el agente INTERNO de la empresa, NO está entrenado con lo que existe** (`~/for3s`:

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-17 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1287)
- **Archivos de referencia:** `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **Foresito, el agente INTERNO de la empresa, NO está entrenado con lo que existe** (`~/for3s`: Mente OS, código, decisiones, historia + el server + más). brian sí tiene memoria potente (~22K episodios); Foresito, que debería "saberlo todo" de la empresa, es el que menos sabe. Reusa el arte del hito ENTRENAMIENTO (absorber memoria sin perderla, ya probado en brian). Cruza con 🅱️ (el Maestro sería la fuente que Foresito lee).

### SC-2 · **Smoke por Telegram a @For3s_OS_bot:** decirle *"busca en el maestro dónde se explica cómo

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-17 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1312)
- **Archivos de referencia:** `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **Smoke por Telegram a @For3s_OS_bot:** decirle *"busca en el maestro dónde se explica cómo dar permisos a una rama"* — debe EJECUTAR la búsqueda (tool-loop + /v1/maestro/buscar) y citar `rama:ruta`, no narrarla. Es el último eslabón E2E conversacional de los puentes C+D.

### SC-3 · **Probar en @For3s_Brian_bot una skill del entrenamiento** (tick-coord, monad, godinez…):

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-17 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1315)
- **Archivos de referencia:** `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **Probar en @For3s_Brian_bot una skill del entrenamiento** (tick-coord, monad, godinez…): primera vez que las ve COMPLETAS (S1 las amputaba al 19% desde el día uno). Comparar calidad.

### SC-4 · **Decidir S3** (canal API sin tools → el modelo NARRA e inventa ejecuciones; afecta la promesa

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-17 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1317)
- **Archivos de referencia:** `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **Decidir S3** (canal API sin tools → el modelo NARRA e inventa ejecuciones; afecta la promesa del canal para clientes API como NavigoX): ¿darle tool-loop al canal API o documentar el límite?

### PI-1 · ⭐ **F-A2 (mejora futura, mayor — idea de Brian): partir misiones complejas al EQUIPO

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-13 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1415)
- **Archivos de referencia:** `vision/Aprendizajes_De_Campo_Post_Incubathon.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** ⭐ **F-A2 (mejora futura, mayor — idea de Brian): partir misiones complejas al EQUIPO multi-agente.** Hoy el carril hace las llamadas al LLM en SERIE. El equipo (`correr_equipo`, H8) ya paraleliza con `asyncio.gather` y ya reporta progreso (`on_progreso`) → routear misión→equipo bajaría el tiempo de PARED real (no solo la percepción). Cambio de motor: routing + síntesis por secciones. No urgente (el progreso en vivo ya alivió la queja).

### PI-2 · 🎨 **`/salud` en instancia recién encendida muestra 🔴** ("no hay turnos", "no hay backups")

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-13 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1420)
- **Archivos de referencia:** `vision/Aprendizajes_De_Campo_Post_Incubathon.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** 🎨 **`/salud` en instancia recién encendida muestra 🔴** ("no hay turnos", "no hay backups") = estado natural de instancia virgen, pero un tester lo lee como "roto". Distinguir vacío-nuevo de fallo-real.

### PI-3 · Jazz da /start + usa el bot varios días + feedback (peldaño 3 en vivo).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-13 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1423)
- **Archivos de referencia:** `vision/Aprendizajes_De_Campo_Post_Incubathon.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** Jazz da /start + usa el bot varios días + feedback (peldaño 3 en vivo).

### PI-4 · **F6 cierre** — re-preguntar el sentimiento a Brian ("¿ya lo soltarías?"). La métrica ES él.

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-13 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1432)
- **Archivos de referencia:** `vision/Aprendizajes_De_Campo_Post_Incubathon.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **F6 cierre** — re-preguntar el sentimiento a Brian ("¿ya lo soltarías?"). La métrica ES él.

### PI-5 · Propagar F1-F4 a las otras instancias (hoy en general+jazz; brian/mashe/Foresito no).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-13 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1433)
- **Archivos de referencia:** `vision/Aprendizajes_De_Campo_Post_Incubathon.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** Propagar F1-F4 a las otras instancias (hoy en general+jazz; brian/mashe/Foresito no).

### VW-1 · ⭐🔴 **VERIFICAR FOR3S OS E2E ANTES DE LA CHARLA (Brian 2026-07-04) — que la demo NO falle en…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1626)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** ⭐🔴 **VERIFICAR FOR3S OS E2E ANTES DE LA CHARLA (Brian 2026-07-04) — que la demo NO falle en vivo.** Batería §5-BIS completa + probarlo EN TELEGRAM a fondo (no solo tests): memoria ("¿en qué quedamos?" retoma) · identidad viva ("sé más breve" → se acopla; "¿cómo te has adaptado a mí?") · **ejecuta código real** (un cálculo → corre en el sandbox) · **GitHub** (analiza repo / cuenta PRs / crea issue) · /soy /salud (todo 🟢) · equipo multi-agente ("analiza a fondo") · velocidad (que no tarde de más c

### VW-2 · Confirmar con Mel: día exacto, hora y **DURACIÓN** del slot (define cuánto contenido cabe).…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1634)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** Confirmar con Mel: día exacto, hora y **DURACIÓN** del slot (define cuánto contenido cabe). ✅ 25 min.

### VW-3 · Definir formato: ¿taller hands-on (la gente instala/prueba) o presentación + demo en vivo?

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1635)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** Definir formato: ¿taller hands-on (la gente instala/prueba) o presentación + demo en vivo?

### VW-4 · Guion de la demo en vivo (secuencia de mensajes a Foresito que muestren el "wow" — reusar

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1636)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** Guion de la demo en vivo (secuencia de mensajes a Foresito que muestren el "wow" — reusar `memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md` como base de qué escribirle).

### VW-5 · Narrativa/slides: el porqué (agente vs bot, self-hosted, tus datos) + el arsenal + el cierre.

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1638)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** Narrativa/slides: el porqué (agente vs bot, self-hosted, tus datos) + el arsenal + el cierre.

### VW-6 · ¿Instalador listo para que la gente lo pruebe? (cruza con DIST-2: probar `curl|sh` en Linux…

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1639)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** ¿Instalador listo para que la gente lo pruebe? (cruza con DIST-2: probar `curl|sh` en Linux limpio).

### VW-7 · Plan B por si falla la red del evento (demo grabada / instancia local).

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-14 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 1640)
- **Archivos de referencia:** el registro histórico §VALIDACION_WEB3
- **Plan:** —
- **Depende de:** —

**Descripción.** Plan B por si falla la red del evento (demo grabada / instancia local).

### EN-1 · **E1 · Desglosar agente por agente a profundidad** (leer TODO, tomar notas de cada uno).

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-05 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2237)
- **Archivos de referencia:** `work/Entrenamiento_Ejecucion_Reporte.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **E1 · Desglosar agente por agente a profundidad** (leer TODO, tomar notas de cada uno). Prioridad por volumen: Fruterito Personal + Watchdog + Fruterito Empleado (el 99% del mar); Cipher/Helix casi vacíos (opcional).

### EN-2 · **E2 · Mapear cada cosa a su capa de For3s** (igual arte que la migración de Foresito):

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-05 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2240)
- **Archivos de referencia:** `work/Entrenamiento_Ejecucion_Reporte.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **E2 · Mapear cada cosa a su capa de For3s** (igual arte que la migración de Foresito): sesiones .jsonl → episodes_events (+ re-embeber + consolidar al grafo) · docs .md → skills/conceptos · herramientas = NO se importan, se reconstruyen aparte (otro trabajo).

### EN-3 · **E3 · Curar antes de aprender** (calidad sobre cantidad; NO meter todo de golpe al autogen

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-05 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2243)
- **Archivos de referencia:** `work/Entrenamiento_Ejecucion_Reporte.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **E3 · Curar antes de aprender** (calidad sobre cantidad; NO meter todo de golpe al autogen — el governor H11 frena, pero hay que filtrar qué vale la pena para no generar skills basura).

### EN-4 · **E4 · Importar a Foresito** con lo ya construido (APRENDE H12 + autogen + curación nocturna

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-05 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `memory/PENDIENTES.md` (histórico, línea 2245)
- **Archivos de referencia:** `work/Entrenamiento_Ejecucion_Reporte.md`
- **Plan:** —
- **Depende de:** —

**Descripción.** **E4 · Importar a Foresito** con lo ya construido (APRENDE H12 + autogen + curación nocturna consolidan al grafo). Resultado: 6 agentes → 1 For3s OS con todo.

---

## BLOQUE · DEMO · la demo web (bloque de trabajo ACTIVO)

**Análisis.** Único bloque de trabajo abierto en `blocks/active/demo`. Su avance se mide ahí, no
aquí: este bloque de pendientes solo registra lo que sobrevive al cierre.

**Plan global:** el propio `blocks/active/demo/BLOCK.md`

### D-1 · §F-11 · 3 rutas OAuth dormidas — reestructurar cómo se ejecuta

- **Prioridad:** 🟠 medio
- **Estado:** pausado
- **Creado:** 2026-08-05 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `lib/demo/oauthGuard.ts` (138 líneas) · las 3 rutas `app/api/demo/`
- **Plan:** el `BLOCK.md` de demo §G
- **Depende de:** `E-5` (conectores self-service usa estas mismas rutas)

**Descripción.** Sin consumidores web desde que se borró `ConnectClaude.tsx` (2026-08-05), pero
**no son basura**: `oauthGuard.ts` es un candado de seguridad con `OAUTH_KINDS` fija a propósito, y
borrarlo eliminaría una capacidad que Brian decidió conservar. **Seguras mientras no exista
`DEMO_OAUTH_INTERNAL=1`** — sin esa variable devuelven 403.
📌 Brian, 2026-08-06: *"se reestructura la forma de ejecutarlo, no se decide hoy."*

---

## BLOQUE · PENDIENTE-EXTRA · lo que no encaja en ningún bloque

**Análisis.** El cajón declarado. ⚠️ No es un vertedero: si un pendiente cae aquí, **primero se
investiga si algo va mal** (contract-pending §2); solo cuando se comprueba que no, se queda.

*Vacío a 2026-08-08.* Los 87 ítems del histórico encontraron bloque.

---

Related: `rules/contract-pending.md` · `rules/rule-pending-rotation.md` · `bin/check-pendings` ·
`memory/PENDIENTES.md` (histórico de solo lectura) · `memory/RETOMAR.md`.
