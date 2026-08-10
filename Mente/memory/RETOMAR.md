# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-10 · **Owner:** brian
**Migrated:** Doc/RETOMAR.md → memory/RETOMAR.md (2026-07-30, ADR-029)


## Purpose

El cold-start brief: el ÚNICO archivo que leer al retomar. Dónde quedamos, el próximo paso y los punteros. Máximo 250 líneas, lo aplica `bin/check-health`; al cerrar, la historia va a la Bitácora.

> **El ÚNICO archivo que necesitas leer al retomar.** Pequeño a propósito: **máximo 250 líneas**,
> lo aplica `bin/check-health`. Al cerrar, la historia va a la Bitácora, no aquí.
> ⚠️ **UNA sola fecha, la de la cabecera** (dos fue un hueco real de F8-4).

---

## 1 · Quién + qué (10 segundos)

- **Brian López** (founder, NO "Aguilar"). ema@frutero.club / brayan002150@gmail.com.
- **Proyecto = SOLO For3s OS.** Cerebro documental: `/home/brianweb3/for3s/Mente/` = **"Mente OS"**.
  ⛔ NO tocar `marca-personal/Mente/` (otro proyecto) sin permiso.
  ⛔ **NO leer `~/5M-incubathon/` (Mente OS de NavigoX) sin gate** — ver §7 (protege consumo).
- **Fuente de verdad arquitectónica:** `Cerebro/For3s_OS_Grafo_Maestro.md`.
- For3s OS = **agente "segundo cerebro" autónomo, self-hosted** en el servidor `for3s` (Telegram +
  consola, Python 3.12 + Postgres+AGE+pgvector, contenerizado). EN PRODUCCIÓN.

## 2 · Servidor `for3s` — 5 FOR3S OS al mismo tiempo

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 (pass en `reference_servidor_for3s`) · gestor
`for3s listar|agregar|entrar|encender|apagar|borrar`. Aislamiento TOTAL por
`docker compose -p for3s-<nombre>`. Comparten SOLO: máquina + imagen (**v0.20.0**) + suscripción
Claude (**1 solo cupo**).

| Bot | Instancia | Dueño | Estado |
|---|---|---|---|
| 🏢 @For3s_OS_bot | `for3s` | Brian | 🟢 "Foresito" — EMPRESA, microglía ON |
| 👤 @For3s_Brian_bot | `brian` | Brian | 🟢 PERSONAL — **ENTRENADO** (§4), microglía OFF a drede |
| 🌐 @For3s_General_bot | `general` | Brian | 🟢 PÚBLICO, puerta ABIERTA |
| 🎷 @For3s_Jazzita_bot | `jazz` | Jazz @driade_1 | ⚪ apagado — verificado E2E |
| 👊 @For3s_Mashe_bot | `mashe` | (1er /start) | ⚪ apagado — verificado E2E |

⚠️ Las 3 nuevas heredan la auth OAuth de Foresito → `project_multi_instancia`.

## 3 · Estado global del producto

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.20.0 CONECTORES SELF-SERVICE · schema BD v47.**
13 hitos H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad
Hermes (5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + super-cerebro (§4).
**Cero bugs abiertos.**

- **✅ TRÍADA SINCRONIZADA** (19/20-jul): server = GitHub (`for3slabs/for3s-os`) = local en HEAD
  `f50a5db`. CI+Trivy verdes · 260 tests.
- **✅ SEGURIDAD CERRADA** (16-jul): CI verde · SEC-3/4/5/6 + 3b/4b · token rotado · **SEC-4c**
  non-root por instancia. 🔒 **nunca `chown -R` un bind mount** (`feedback_nunca_chown_bind_mount`).

## 4 · 🎓🎓 SUPER-CEREBRO — ambos agentes entrenados+examinados ✅ (18/20-jul)

**brian 🍓** 22,406 eps · examen **94.3%**. **Foresito 👑** 1,829 eps · grafo 2,687 nodos · examen
**98.8%** · es el **AGENTE MAESTRO** (lee `for3slabs/mente-os-maestro` EN VIVO). Los exámenes
cazaron **12 hallazgos con fix sistémico** (H-11: la contraseña del server vivía en 60 eps →
redactada). 👉 `project_entrenamiento_foresito` · `work/Entrenamiento_Ejecucion_Reporte.md`.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

### 🆕 EL CICLO DE TRABAJO YA ES UN SISTEMA, NO UNA COSTUMBRE (2026-08-08/10)

📊 **Batería 199 → 220 · 0 fallos.** Clon ajeno: **209/1**, y ese 1 (`registered=no`) es la
respuesta correcta. Identidad en el clon: **0 menciones a Brian**, 11 al dueño real.

⭐ **Lo que cambió de raíz:** el ciclo declaraba hasta `⛔ STOP` y **terminaba ahí**. Conflicto,
merge y limpieza no estaban en ningún mapa — y un hueco del que nadie habla es indistinguible de
uno que no existe. Ahora son **12 etapas, cada una con su regla**, y un check falla si alguna se
queda sin dueño o apunta a una regla inexistente (`rules/rule-pr-batching.md` §4).

🆕 **4 reglas nuevas del ciclo:** `rule-pr-batching` (4 pendientes por PR · el último **cierra**
el bloque y apunta a los anteriores · **conflictos**: diagnosticar → rebase → `--force-with-lease`,
⛔ nunca en la web de GitHub) · `rule-post-merge-cleanup` (verificar que viajó, **luego** borrar) ·
`contract-pending` + `rule-pending-rotation` (los pendientes rotan por archivo cada mes).

🆕 **Ya no se pregunta si un PR se mergeó: se mira.** `bin/check-prs` al arrancar y
`hooks/watch-prs.py` antes de tocar git a mitad de sesión. ⛔ No es un cron: un cron dispara
cuando no hay nadie escuchando.

🗓️ **Los pendientes viven en `memory/pendiente-<mes>-<año>.md`** — 111 uno por uno (eran 27
agrupaciones), en 5 bloques. `PENDIENTES.md` quedó **congelado**.

🏁 **Bloque MOTOR cerrado 9/11.** Los 2 abiertos: el §6 de la voz (🙋 criterio de Brian) y el
renombrado (orden 7 de 7, ya desbloqueado).

**👉 PRÓXIMO PASO: la PRUEBA DE CAMPO** — que alguien ajeno instale el sistema. **Cero
instalaciones externas verificadas**: todo lo medido en un clon lo midió la IA en esta máquina.

### LO ANTERIOR · el clon ya verifica el motor (2026-08-07, S13)

`separacion-motor-instancia` **cerrado 5/5 y archivado**. Recorrido medido en un clon: `10 → 1`.
⭐ **El hallazgo que dio la vuelta al problema:** la hipótesis era mover 221 archivos de instancia;
**medido, ninguno estorbaba** — lo que fallaba eran los CHECKS que los interrogaban mal, y mover
archivos habría escondido el defecto. **4 defectos del motor** que la etiqueta *"son fallos de la
instancia de Brian"* llevaba meses tapando.
👉 Detalle: `blocks/archive/separacion-motor-instancia_2026-08/SUMMARY.md`.

### 🆕 LA DEMO: de 0 a 4 tests, con 23/23 en verde (2026-08-05/06)

`plan-tests-demo` cerró 🟢 PRODUCTO. Los 4 caminos críticos escritos (autorizar · entrar · hablar ·
apagar) y **23/23 en verde** contra la rama de Neon de test. 🔬 **Cada test se VIO FALLAR antes de
creerle** — en ④ eso destapó que mi propio caso no discriminaba, y que iba a probar el archivo
equivocado. 🔬 De paso, **2 defectos del MOTOR** (`check-applied`) corregidos.
📊 El bloque `demo` está **11/12**; su único pendiente vivo es §F-11 (rutas OAuth).
👉 Detalle y estado real: `blocks/active/demo/BLOCK.md`.

### ⚡ RENDIMIENTO: el sistema es **86x más rápido** (2026-08-05)

`check-links` **47.2s → 0.55s** · batería **1m10 → 15.6s** · métricas **2m31 → 13.5s**. Causa: un `glob` recursivo recorría los 43,986 archivos de `marca-personal` **por cada cita**. 🔬 F0 destapó 2 defectos silenciosos (mi sonda no medía; `glob` no ve ocultos, `os.walk` sí). → `docs/plan-check-links-performance.md`.

### 🆕 ⭐ LO ANTERIOR (2026-08-05, S11) — **LA CAPA 2 EXISTE Y `distribucion` CERRÓ 🟢 PRODUCTO**

**Sin commit — `Mente/` está en `.gitignore` de este repo (el motor se publica en `mente-os`).**

- 📜 **Las 6 dimensiones de QA, LLENAS** (`rules/qa-dimensions.md`, `draft` → `current`). La más
  dura, literal suya: *"NO PUEDE DEJAR CÓDIGO HUÉRFANO, MUERTO, SIN CONECTAR — Y ESO LO LOGRAMOS
  PROBANDO EL FLUJO A PROFUNDIDAD CON DATOS REALES"* (§2.5). **Él responde con casos, yo estructuro.**
- 🏁 **`distribucion` CERRADO 🟢 PRODUCTO** — primer bloque juzgado por **capa 2**. Archivado en
  `blocks/archive/distribucion_2026-08/` (su `SUMMARY.md` lleva qué se hizo y qué se aprendió).

- 🔌 **3ª ronda de cableado**: el criterio LLENO tampoco llegaba (2 `val-*` sin declarar, 2 dueños
  diciendo `pending` de lo lleno) → corregido + **2 checks** que lo impiden.
- 🏁⭐ **LOS 3 DUEÑOS CON CRITERIO PROPIO — huecos 66 → 3.** `principles/expertise/doc-structure.md` cerró el último:
  ⭐ **si un documento excede su techo DEBE partirse**, y las mitades se apuntan (endurece ADR-027) ·
  puntero siempre que el dato tenga dueño en otro sitio · `Status: current` es un contrato de 4
  términos (**quién lo verificó y con qué**) · ⛔ nunca borrar historia para que un check pase.
  **Los 3 restantes NO son criterio:** 2 punteros de índice + 1 falso positivo del contador.
- 🎓 **`principles/expertise/doc-planning.md` LLENO** — **todo límite que un plan declare se MIDE** · una fase entrega
  UNA cosa · ⛔ nada de fases "pulir" · **si tocar algo obliga a BD+frontend+backend, es UN BLOQUE**
  · un hueco real **se marca como pendiente asignado a Brian** · ⛔ *no omitas algo porque crees
  que ya lo sé*, ni te excuses con *"no sabía"*.
- 🔴 **Brian cazó un SESGO DE DISEÑO:** mi check exigía que todo criterio aterrizara en un bloque
  de código — *"los usuarios pueden hacer código o no, no es ley"*. Corregido + nace el bloque
  `plan-tests-demo` (`type: docs`), el primero que ejercita owner-1.
- 🎓⭐ **OWNER-2 COMPLETO** — `principles/expertise/dev-frontend.md`: **el servidor es dueño del estado, React lo
  refleja** · lo que el usuario decidió sobrevive al refresh · 🔴 **un control nunca miente** · el
  nombre dice qué MUESTRA · ⛔ secreto en el cliente, botón oculto como única autorización.
- 🎓 **`principles/expertise/dev-backend.md` LLENO** — **guardián único por regla** (`session.ts` 12→0) · el fallo
  esperable **es** el contrato · seguridad o dinero **se unifican siempre** · ⛔ endpoint genérico,
  exponer control, confiar en un id del cliente. 🔬 **El check de cableado me cazó a mí.**
- 🎓⭐ **OWNER-3 COMPLETO** — *fallar ruidosamente* · **los DATOS deciden** detener vs degradar ·
  *no se asume nada* · **ausencia de evidencia NO es evidencia** · *nunca cierres algo cuyo fallo
  no sabrías detectar*.
- 🎓 **`principles/expertise/dev-database.md` LLENO → fase F1 CERRADA.** 5 categorías que nunca viven en código · 4
  estados imposibles · **FK siempre** · 4 condiciones antes de una migración. ⭐ Su raíz: *"debe
  existir un PLAN DE IMPLEMENTACIÓN que valide por qué la tabla existe"*.
- 🧩 **2 skills externas desmanteladas** → bloque `expertise-programacion` **CERRADO 🟢 PRODUCTO**
  + nace `rules/rule-shipping-flow.md` (rama → verificar → PR → ⛔ no mergear), **transversal**.
- 🔧 **`grade-block`: 3 defectos** → arreglados + **5 self-tests** · nace **`docs/WORKSPACE.md`**.
- 🔌 **2ª ronda de cableado**: piezas escritas y no conectadas — **las 20 reglas ya tienen script**
  (eran 17) + `docs/WORKSPACE.md` con check propio. 🔬 Verificados **por reversión**.

✅ **P1·P2·P4·P5 HECHOS** (batería **173 → 175**): el commit **bloquea un índice desfasado** (cazó
3 derivas reales, la primera a mí) · `/clear` **lee la batería** y se niega si está roja · nace
**`VERSION` 0.1.0 + `CHANGELOG`** con 2 checks · `allow` declarado **por mecanismo**.
✅ **P3 HECHO: `.github/workflows/ci.yml`** (3 jobs) en `Mente/`, que **es su propio repo**.
Escribirlo destapó **4 defectos reales**: los 2 bloques archivados hoy **sin `SUMMARY.md` ni
`connections.md`** (nada de la batería lo vigilaba) y sus encabezados en español que el validador
no reconocía. 🔬 Medido antes: con `HOME` limpio fallan 3 checks que **leen la máquina, no el
motor** — el job los nombra uno a uno para que la exención no crezca sola.

**👉 PRÓXIMO PASO:** queda **1 bloque activo: `demo`** (6/10, 🔴 MVP). Sus 3 tapones siguen donde
los dejó el 26-jul (§5 "LO ANTERIOR"). Deuda abierta: **prueba de campo real** de `mente-os`
(alguien que no sea Brian clonando) · los **35 huecos** restantes (**solo queda owner-1**: `doc-planning` + `doc-structure`) · las 2 decisiones 🔑🔐 de abajo.

### LO ANTERIOR — S10 (voz) y S9 (instalador) → `memory/Bitacora_Progreso.md`

### LO ANTERIOR (2026-07-31, S7) — el v2 se construyó y F8-4 lo verificó

**Mente OS pasó de DOCUMENTAR a GOBERNAR.** F0-F8 cerradas · migración v1→v2 completa (M0-M5,
ADR-029): si un documento cita `Alma/` `Cuerpo/` `Doc/` `Tickets/` es **cita fósil**.
🖥️⭐ **La demo es un bloque grande con índice propio** — entrar por `project_bloque_demo_pendientes`.
👉 **Sus tapones vivos están en `blocks/active/demo` §F**, que es donde se miden.
📦 Detalle completo → `memory/Bitacora_Progreso.md` (movido el 2026-08-05).

## 5-ter · 🏗️ el PORQUÉ del v2 (diagnóstico 27-jul) · ✅ construido, ver §5

**Causa raíz:** documentaba bien, no GOBERNABA. **La ley:** *código = 100%, documento = 40-60%* →
**la doctrina es documento, la VERIFICACIÓN es script.** ⭐ El diferenciador: **veredicto en 2
capas** — validado contra 4 frameworks, **ninguno responde *"¿producto o MVP?"***.
👉 `principles/vision-mente-os-v2.md` · `docs/Arquitectura_Mente_OS_v2_Bloques.md` ·
`docs/plan-v2-rollout.md` · memoria `project_mente_os_v2_bloques`.

## 5-bis · Cerrados grandes recientes (solo punteros — historia en Bitácora Julio)

- 🌐 **SUPER-CEREBRO CONECTADO ✅** — Maestro F1-F5 + Foresito entrenado + 👑 Agente Maestro (§4).
- 🎯 **APRENDIZAJES post-Incubathon:** 🔴A ✅ · 🔵D ✅ · 🟠B ✅ · 🟣E ✅ · 🟡C multi-canal pendiente.
- ⭐ **Toda la deuda viva —congelados incluidos— está en 🗓️ `memory/pendiente-<mes>-<año>.md`**,
  por bloque y con prioridad. Ya no se lista aquí: dos listas de pendientes divergen.

## 6 · 🏆 Incubathon (jul 2026) + 🌉 puente a otros Mente OS

- **2º lugar de 200 empresas** con **NavigoX** — la capa API cerró el pitch → For3s OS VALIDADO
  como infraestructura con demanda real. `project_incubathon_2do_lugar_validacion` ·
  `project_hito_hoteleria_navigox`.
- **🌉 NavigoX vive en su PROPIO Mente OS** (`~/5M-incubathon/Mente/`), aquí **CERRADO**.
  ⛔ **NUNCA leerlo sin gate** — `acceder mente <proyecto>` + por qué → solo lectura; cerrar con
  `cerrar mente <proyecto>`. **Motivo: el consumo.** Reglas: `bridges/Puentes_Mente_OS.md`.

## 7 · Reglas de oro con Brian (permanentes)

- ⛔ **NUNCA implementar sin explicar+aprobar primero** (`feedback_explicar_antes_de_implementar`).
- 🏗️ Hitos grandes = **Método de Fases "F"** (`rules/ESTANDAR_Metodo_Fases_F.md`): explicar→aprobar
  →construir · investigar terreno · caza bugs · **batería §5-BIS** · red de seguridad · server-primero.
- 📏 **Server-primero:** desarrollar+probar en el server; push a GitHub SOLO con orden explícita.
- 🧹 **Rama mergeada = rama borrada** (local + remoto), **tras verificar que su trabajo viajó**.
  Solo 2 excepciones: migración de versión mayor · cambio de vida o muerte.
  `rules/rule-post-merge-cleanup.md` (Brian, 2026-08-07).
- ⛔ **NO loops de espera** contra el server que sigan si Brian cierra (gasta cuota) · **NO cambiar
  el modelo** (lo fija con /model; el bot corre sonnet-4-6, NO es bug) · **NO sesgar hacia
  charla/descubribilidad** — él marca el momento.
- 🔒 Master KEK offline · Brian nunca ve plaintext · audit inmutable · ante duda → preguntar.
- 🧹 **/clear es seguro cuando la conversación crezca** (Mente OS + memorias guardan todo).

---

## 📍 PUNTEROS — si necesitas MÁS que este brief

| Necesitas… | Lee… |
|---|---|
| **🖥️⭐ LA DEMO — índice maestro (ENTRAR POR AQUÍ)** | memoria `project_bloque_demo_pendientes` |
| **TODOS los pendientes a detalle** | 🗓️ `memory/pendiente-<mes>-<año>.md` (rota mensual) · `PENDIENTES.md` = histórico congelado |
| **Secretos de la demo (DEMO_ENC_KEY) — FUERA de git** | `secrets/Secretos_Demo_Sitio.md` |
| Demo: Ronda F0 · mapa · plan BD · auditoría | repo del sitio: `marca-personal/DEMO_*.md` |
| 🎓 Caso: limpiar un hardcodeo heredado sin romper | `memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` |
| **Telemetría de conversaciones (registrar ANTES del `/clear`)** | `Cerebro/Registro_Conversaciones.md` |
| Los 3 carriles dormidos · hito ENTRENAMIENTO | `work/Carril_*.md` · `work/Entrenamiento_*.md` |
| Diseño arquitectónico maestro (11 nodos + 3 pilares) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| Historia cronológica · comparaciones vs Hermes | `memory/Bitacora_Progreso.md` · `docs/analysis/Comparacion_For3s_OS_vs_*.md` |
| **Puente a otros Mente OS — reglas del gate** | `bridges/Puentes_Mente_OS.md` |
| Contexto histórico (solo si imprescindible) | `memory/Estado_Sesion_Continuidad.md` |
| Multi-instancia · servidor (acceso+specs) | `project_multi_instancia` · `reference_servidor_for3s` |

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `memory/RETOMAR.md`).
