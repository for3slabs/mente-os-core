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

## BLOQUE · MENTE-OS-V2 · migración y forma del motor

**Análisis.** Mente OS es **la herramienta que construimos para que For3s OS funcione** — no un
proyecto aparte (Brian, 2026-08-08). v2 ya gobierna: 201 checks, 3 niveles de reglas, veredicto en
2 capas. Lo que queda son **piezas del v1 que nunca se migraron** y reglas escritas que nadie aplicó
a sí mismas.

**Plan global:** ⬜ **no escrito todavía** — se llamará `PLAN-GLOBAL-mente-os-v2` cuando exista.
⚠️ El contrato lo exige para abrir un bloque; este bloque nació de una rotación, no de un análisis
nuevo, así que **la deuda es real y queda declarada** en vez de fingir un plan vacío.

### V2-1 · Partir la arquitectura: 2,471 líneas contra un techo de 800

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-07-29 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` · `rules/contract-document.md`
- **Plan:** ⬜ lo necesita — es grande y tiene decenas de `§` apuntándole
- **Depende de:** —

**Descripción.** La regla `§3.2-QUATER` fija el techo de una arquitectura en **800 líneas**. Medido
el 2026-08-08: **2,471** — más de 3×. Es el archivo más citado del sistema, así que partirlo mal
rompe decenas de referencias `§`.
⚠️ **Ya se intentó una vez** (julio, `blk-split-architecture`) y el resultado hoy es **74% duplicado**
en `docs/architecture/` con 330 líneas viviendo solo en el original: **la partición creó la
divergencia que debía evitar**. Por eso `principles/expertise/doc-structure.md` §2.1 abrió la excepción de *fuente de
verdad* — y este archivo es candidato a reclamarla. ⭐ **La decisión previa no es cómo partirlo, sino
si debe partirse**, y esa es de Brian.

### V2-2 · Renombrado a la convención inglesa: quedan 28 archivos

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-07-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `rules/NAMING_CONVENTION.md` §7.4 (el plan completo ya escrito)
- **Plan:** ya existe dentro del estándar
- **Depende de:** —

**Descripción.** Brian decidió en julio: *"no renombramos a los 208, eso será un pendiente de v2."*
📊 **Medido 2026-08-08: quedan 28**, no 208 — la migración v1→v2 se llevó la mayoría por el camino.
Bajó de 🔴 a 🟢 porque el daño real (rutas rotas al citar) ya lo cubren `check-links` y el candado de
citas de la batería.

### V2-3 · El sistema de encarpetado no está terminado

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-07-29 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `piezas.tsv` · `bin/check-structure` · la raíz de `Mente/`
- **Plan:** ⬜ conviene
- **Depende de:** `V2-1` (la arquitectura declara el árbol objetivo)

**Descripción.** El encarpetado quedó **mixto**: 14 carpetas en la raíz de `Mente/`, unas del motor
(`bin/ hooks/ rules/ principles/`) y otras de la instancia (`Cerebro/ memory/ secrets/`), sin que la
frontera esté en el árbol. `mente.config.yml` ya declara esa línea desde el 31-jul y
`blk-separacion-motor-instancia` demostró que **mover archivos no era lo que hacía falta** — pero la
mezcla sigue haciendo que un clon tenga que aprenderla leyendo, no viéndola.

### V2-4 · Reestructuración del Mente OS Maestro

- **Prioridad:** 🟠 medio
- **Estado:** pausado
- **Creado:** 2026-07-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `Maestro/` (sub-repo con su propio git) · `bridges/Puentes_Mente_OS.md`
- **Plan:** ⬜ lo necesita
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
- **Plan:** —
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
- **Plan:** existe (el rollout)
- **Depende de:** —

**Descripción.** F0 cerró 4/4 tickets pero dejó **4 cosas sin hacer** que nunca se convirtieron en
pendientes propios. ⚠️ **Requiere leer el plan antes de estimarlo**: la lista vive ahí, no aquí.

### V2-7 · La primera rotación de pendientes — ESTE trabajo

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-07-29 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `memory/PENDIENTES.md` · `rules/contract-pending.md` · `bin/check-pendings`
- **Plan:** —
- **Depende de:** —

**Descripción.** El archivo de pendientes era, él mismo, un pendiente: **4,794 líneas · 348 KB**,
mezclando 30 secciones cerradas con 46 abiertas. Se cierra cuando **los 87 ítems v1 estén migrados
a este formato** y `PENDIENTES.md` quede como histórico de solo lectura.
📊 Estado: contrato ✅ · regla ✅ · validador ✅ · bloques v2 ✅ · **bloques v1 ⬜ en curso**.

### V2-8 · 🔴 Un clon ajeno hereda el nombre de Brian en sus reglas de proyecto

- **Prioridad:** 🔴 urgente
- **Estado:** activo
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** —
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

⭐ **El mecanismo YA funciona; lo que falta es que el sistema lo diga.** Es la misma familia D de
`rules/rule-checks-must-measure.md` que cerró `separacion-motor-instancia`: un archivo del motor
arrastrando la instancia de su autor, y un check (`migrated rule: <owner>`) que sale 🔴 sin explicar
que la salida es una bandera.

### V2-9 · `piezas.tsv` declara 23 piezas y ningún validador

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** —
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

### V2-10 · 2 reglas escritas sin ningún script que las verifique

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-08-08 · **Modificado:** 2026-08-08 · **Cerrado:** —
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

---

## BLOQUE · PRODUCTO-FOR3S-OS · el agente y su deuda

**Análisis.** El producto en producción: bot Telegram contenerizado, multi-instancia, canal API.
Su deuda viene de junio-julio y está **congelada por decisión de Brian** en su mayor parte
(*"registrados, NO desarrollar aún"*). ⚠️ Congelado **no** es cerrado: rota cada mes hasta que se
resuelva o se elimine con razón escrita.

**Plan global:** ⬜ **no escrito todavía** — se llamará `PLAN-GLOBAL-producto-for3s-os` cuando exista.

### P-1 · Brechas Hermes — 18 capacidades registradas, sin desarrollar

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `docs/analysis/Comparacion_For3s_OS_vs_*.md`
- **Plan:** ⬜ lo necesita — 18 ítems anidados
- **Depende de:** —

**Descripción.** 18 capacidades que Hermes tiene y For3s no. Brian las registró explícitamente como
*"NO desarrollar aún"*. **Pausado a propósito, no olvidado.** La paridad prioritaria (5/5) ya se
cerró en julio; esto es el resto.

### P-2 · Brechas OpenClaw — 16 capacidades registradas, sin desarrollar

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-04 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `docs/analysis/` · material en `~/entrenamiento/`
- **Plan:** ⬜ lo necesita — 16 ítems anidados
- **Depende de:** `P-1` (misma naturaleza: comparativa de capacidades)

**Descripción.** Igual que P-1, con el ecosistema Frutero OpenClaw. ⚠️ **Depende de P-1**: se
evalúan juntas o se duplica el análisis de qué capacidad merece existir en For3s.

### P-3 · H9 SUEÑA (DMN) — deuda D1-D8

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** el módulo DMN del agente (repo `for3slabs/for3s-os`)
- **Plan:** ⬜ lo necesita — 8 ítems anidados
- **Depende de:** —

**Descripción.** H9 está **completo y en producción** (v0.11.0): trabaja en idle con 5 tareas de
housekeeping y 3 generativas gobernadas, estas últimas **OFF a propósito**. Los 8 pendientes son
deuda de pulido, no funcionalidad rota.

### P-4 · H10 PLANEA (metacognición) — deuda HP1-HP6

- **Prioridad:** 🟠 medio
- **Estado:** activo
- **Creado:** 2026-06-26 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** el módulo de metacognición (repo `for3slabs/for3s-os`)
- **Plan:** ⬜ conviene — 6 ítems anidados
- **Depende de:** `P-3` (ambos tocan el ciclo autónomo del agente)

**Descripción.** H10 cerró en v0.12.0 con su tesis: *"sé cuándo NO sé"* — el agente mide su
confianza antes de afirmar. Quedan 6 ítems de deuda.

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

### P-6 · Deuda técnica del MVP — quedan 3 de 21

- **Prioridad:** 🟢 sin prisa
- **Estado:** activo
- **Creado:** 2026-06-18 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** el registro histórico
- **Plan:** —
- **Depende de:** —

**Descripción.** 18 de 21 cerrados durante el pulido. Quedan 3, ninguno bloqueante.

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

### P-8 · Hitos futuros y hallazgos de fondo — 18 ítems que necesitan Ronda

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-06-27 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** el registro histórico §FUTURO · §HALLAZGOS DE FONDO
- **Plan:** ⬜ lo necesita
- **Depende de:** —

**Descripción.** Agrupa **9 de "Futuro (post-pulido)" + 5 de "Hallazgos de fondo" + 4 recordatorios
de diseño**. Los hallazgos de fondo *"necesitan diseño tipo Ronda"*, es decir: no son tareas, son
temas a debatir antes de existir.

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

### E-6 · Super-cerebro conectado — 4 de 12 abiertos

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-17 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`
- **Plan:** existe (la visión)
- **Depende de:** `V2-4` (el Maestro)

**Descripción.** 8 de 12 cerrados: Maestro F1-F5 ✅ + Foresito entrenado (98.8%) ✅ + agente maestro
✅. Quedan 4.

### E-7 · Post-Incubathon: multi-canal (🟡C) es el único frente vivo

- **Prioridad:** 🟢 sin prisa
- **Estado:** pausado
- **Creado:** 2026-07-13 · **Modificado:** 2026-08-08 · **Cerrado:** —
- **Arrastrado desde:** `PENDIENTES.md` (histórico)
- **Archivos de referencia:** `vision/Aprendizajes_De_Campo_Post_Incubathon.md`
- **Plan:** existe (el documento de aprendizajes)
- **Depende de:** —

**Descripción.** De los 5 frentes: 🔴A tokens ✅ · 🔵D valor ✅ · 🟠B puente ✅ · 🟣E confianza ✅ ·
**🟡C multi-canal PENDIENTE, sin urgencia.** Brian pidió explícitamente **no** sesgar hacia
descubribilidad/charla: él marca el momento.

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
