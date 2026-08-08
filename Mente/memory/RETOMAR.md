# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-07 · **Owner:** brian
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

### 🆕 ⭐ UN CLON YA VERIFICA EL MOTOR: **10 fallos → 1** (2026-08-07, S13)

🏁 **BLOQUE CERRADO Y ARCHIVADO 2026-08-07** en `blocks/archive/separacion-motor-instancia_2026-08/`
(5/5 · 🟡 cierra: capa 2 **6/6 🟢** con evidencia · capa 1 🔴 por el límite del medidor, ver §K).
👉 **Queda 1 solo bloque activo: `demo`.**

📊 El recorrido medido en un clon limpio, tras `bin/init`:
`10 → 7` (familia D 5-6) → `6` (additionalDirectories) → `2` (WORKSPACE) → **1**.

⭐ **El hallazgo que da la vuelta al problema:** la hipótesis era mover 221 archivos de instancia
a una carpeta aparte. **Medido: ninguno estorbaba.** Lo que fallaba eran los CHECKS que los
interrogaban mal — mover archivos habría escondido el defecto en vez de corregirlo. Por eso
`instance/` NO se creó y el §B del bloque se corrigió.

**4 defectos reales del motor** (familia D casos 5-8, `rules/rule-checks-must-measure.md`) que la
etiqueta *"son fallos de la instancia de Brian"* llevaba meses tapando. 🔴 El peor:
`grade-block archived` — bajo `pipefail` el pipe tomaba el exit `2` del veredicto 🔴 MVP **aunque
el `grep` acertara**: exigía **la nota que saca en la máquina de su autor**, un check atado a la
instancia **sin nombrarla una sola vez**.

También: `docs/WORKSPACE.md` sale del repo y `bin/init` lo GENERA (su línea 3 lo declaraba desde el
05-ago y nadie lo hacía cumplir) · `check-links` deja de llamar rotas a 12 citas que resuelven en
repos hermanos ausentes · `owner == "Maestro"` hardcodeado en `check-structure` corregido.

**🔴 El único rojo que queda en un clon es la respuesta CORRECTA:** `check-clear-ready
registered=no` — la sesión de un árbol recién nacido no está registrada. Verde ahí sería mentir.

**🆕 Cierre (08-07):** PR #12 mergeado + 3 arreglos (matcher de `hooks/pre-edit-standards.py`,
fósiles en `bin/check-clear-ready`, línea fantasma en `bin/check-health`). Batería **198/0**.

**✅ CIERRE (08-07):** PRs #12·#13·#14 mergeados. Bloque **5/5** — clon de master: 6 fallos → **1**
tras `bin/init`, y ese 1 (`registered=no`) es la respuesta correcta. graphify **4/6**: #5 y #6
⏸️ diferidos, miden un producto que nadie externo ha instalado. 🔑 GPG sigue siendo tuya.

**👉 PRÓXIMO PASO: la PRUEBA DE CAMPO** — que alguien ajeno instale el sistema. **Cero
instalaciones externas verificadas**; sin eso, graphify #5-#6 solo se medirían a sí mismos.

🔬 **Cerrarlo destapó 5 defectos en los DOS medidores — corregidos el 08-07** (detalle en el §K del
bloque archivado y en `memory/PENDIENTES.md`): `grade-block` marcaba `runbook NO` **con el documento
escrito** (📊 🔴 MVP → 🟢 PRODUCT sin tocar un documento) · `generate-index` subdeclaraba a todos
(📊 `demo` **6/7 → 11/12**). ⭐ **Se arregló quien LEE, no quien escribe:** falsear el §B para
complacer al medidor habría convertido el veredicto en decoración. Verificado por sabotaje.

---

### 🆕 🔴 LA DEMO PASÓ DE 0 A 4 TESTS — y uno **falla a propósito** (2026-08-05)

`plan-tests-demo` **CERRADO 🟢 PRODUCTO** y archivado. Los **4 caminos críticos escritos**:
② autorizar · ① entrar · ③ hablar · ④ apagar. **Suite: 15 pasan · 8 saltados · 1 FALLA.**
⏸️ Los 8 saltados esperan una **rama de Neon de test** — `DEMO_DATABASE_URL` es PRODUCCIÓN
(medido: 4 instancias vivas), así que los tests de integración **se saltan** en vez de caer ahí.
🔬 **Cada test se VIO FALLAR antes de creerle** (sabotaje + restaurar byte a byte); en ④ eso destapó que **mi propio caso no discriminaba**. ⚠️ **④ iba a probar el archivo equivocado** (`container.ts`): la regla *"solo el dueño"* vive en `app/api/demo/general/agent/route.ts`.
🔬 **2 defectos del MOTOR de paso:** `check-applied` no seguía punteros de un bloque partido, y daba por aplicado un estándar por palabras **sueltas** (preexistente, verificado contra HEAD). Corregidos y reprobados. Detalle: `blocks/active/demo/BLOCK.md` §G.
🔴 **El rojo ES la entrega:** `DEV_FALLBACK` autoriza `jazz@example.com`, una dirección que nadie
controla (`expected false, received true`). ⛔ **No lo "arregles" debilitando el assert** — su verde
es la definición de cerrar `blocks/active/demo` §F-7, y eso necesita un dato que solo tiene Brian:
**quién es dueño de jazz y de mashe.**
📊 demo: `test files` **0 → 1** — cae uno de sus 2 rojos (queda el muerto `ConnectClaude.tsx`). Corredor: **Vitest 4.1.10**.
⛔ **Nada commiteado ni empujado** — Vercel despliega `marca-personal` desde `main`: lo decide Brian.
🔬 **Un validador lee la CELDA, no la intención** — el matiz va en la descripción; la celda, UNA palabra.

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
  Visión: `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`.
- 🎯 **APRENDIZAJES DE CAMPO post-Incubathon** (`vision/Aprendizajes_De_Campo_Post_Incubathon.md`):
  🔴A ✅ · 🔵D ✅ · 🟠B ✅ · 🟣E ✅ · 🟡C multi-canal PENDIENTE (sin urgencia).
- **Congelados hasta orden de Brian** (NO empujar): brechas OpenClaw/Hermes · identidades
  secundarias · descubribilidad (SEO/AEO/GEO).
- **Deuda no urgente:** H9 D1-D8 · H10 HP1-HP6 · UX. Lista completa: **`memory/PENDIENTES.md`**.

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
| **TODOS los pendientes a detalle** | `memory/PENDIENTES.md` |
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
