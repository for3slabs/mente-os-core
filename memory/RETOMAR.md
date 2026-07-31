# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** entry-point · **Updated:** 2026-07-31 · **Owner:** brian
**Migrated:** Doc/RETOMAR.md → memory/RETOMAR.md (2026-07-30, ADR-029)

> **Propósito:** el ÚNICO archivo que necesitas leer al retomar. Pequeño A PROPÓSITO
> (releerlo es caro cuando crece). **REGLA DE HIGIENE: máximo ~200 líneas** — la aplica
> `bin/check-health`. Al cerrar, mover lo viejo a la Bitácora y dejar aquí SOLO el estado
> vigente + punteros. La historia NO va aquí.
>
> ⚠️ **UNA sola fecha, la de la cabecera.** Tener dos se destapó como hueco en F8-4 (S8).


---

## 1 · Quién + qué (10 segundos)

- **Brian López** (founder, NO "Aguilar"). Email ema@frutero.club / brayan002150@gmail.com.
- **Proyecto = SOLO For3s OS.** Cerebro documental: `/home/brianweb3/for3s/Mente/` = **"Mente OS"**.
  ⛔ NO tocar `marca-personal/Mente/` (otro proyecto) sin permiso.
  ⛔ **NO leer `~/5M-incubathon/` (Mente OS de NavigoX) sin gate** — ver §7 (protege consumo).
- **Fuente de verdad arquitectónica:** `Cerebro/For3s_OS_Grafo_Maestro.md`.
- For3s OS = **agente "segundo cerebro" autónomo, self-hosted** en el servidor `for3s`
  (Telegram + consola, Python 3.12 + Postgres+AGE+pgvector, contenerizado). EN PRODUCCIÓN.

## 2 · Servidor `for3s` — 5 FOR3S OS al mismo tiempo (2026-07-07)

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 (pass en `reference_servidor_for3s`) · gestor:
`for3s listar|agregar|entrar|encender|apagar|borrar`. Aislamiento TOTAL por
`docker compose -p for3s-<nombre>`. Comparten SOLO: máquina + imagen `for3s-agent:local`
(**v0.20.0**) + suscripción Claude (**1 solo cupo** para todas).

| Bot | Instancia | Dueño | Estado | Notas |
|---|---|---|---|---|
| 🏢 @For3s_OS_bot | `for3s` (compose principal, no `for3s listar`) | Brian | 🟢 | "Foresito" — EMPRESA, memoria de siempre, microglía ON |
| 👤 @For3s_Brian_bot | `brian` | Brian | 🟢 | PERSONAL — **ENTRENADO** (ver §4), microglía OFF a drede |
| 🌐 @For3s_General_bot | `general` | Brian | 🟢 | PÚBLICO, **equipo/puerta ABIERTA** (quien escriba entra). Pendiente: otras API keys/datos |
| 🎷 @For3s_Jazzita_bot | `jazz` | Jazz @driade_1 (1177279840) | ⚪ apagado | verificado E2E; ella lo enciende cuando quiera |
| 👊 @For3s_Mashe_bot | `mashe` | (1er /start) | ⚪ apagado | verificado E2E; Brian decidirá qué hacer |

⚠️ Las 3 nuevas heredan la auth OAuth de Foresito. El warning "Chat not found" es normal hasta
que el dueño da /start. Detalle: memoria `project_multi_instancia`.

## 3 · Estado global del producto

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.20.0 CONECTORES SELF-SERVICE · schema BD v47.**
13 hitos H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad
Hermes (5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + super-cerebro (§4).
**Cero bugs abiertos.**

- **✅ TRÍADA SINCRONIZADA** (19/20-jul): server = GitHub (origin `for3slabs/for3s-os` + backup
  `for3slabs/for3s`) = local (`For3s-OS/`) en HEAD `f50a5db`. CI+Trivy verdes · 260 tests.
- **✅ INSTANCIAS EN v0.20.0** — 3 vivas + jazz/mashe apagadas por diseño. Cliente API real:
  NavigoX (hotel-recepcion, sin consumo activo) + jazz-id (prueba). Datos limpios.
- **✅ SEGURIDAD CERRADA** (16-jul): CI 100% verde (`b8da4d7`) — gitleaks · format · bandit ·
  migraciones E2E con AGE · coverage 15% · **CVE-2026-59950 parcheada** (mcp 1.28.1).
  SEC-3/4/5/6 + 3b/4b completos · **token GitHub rotado**.
- **✅ SEC-4c** (`021292e`): non-root con **perfil por instancia** — Foresito/brian=interna(root),
  general/jazz/mashe=expuesta(non-root uid 1000). 5 bugs cazados, 1 catastrófico →
  🔒 **lección LOCKED: nunca `chown -R` un bind mount** (memoria `feedback_nunca_chown_bind_mount`).

## 4 · 🎓🎓 SUPER-CEREBRO — ambos agentes entrenados+examinados ✅ CERRADO (2026-07-18/20)

**brian 🍓** 22,406 eps · 99.94% consolidado · grafo 1,335 conceptos · **examen 94.3%**.
**Foresito 👑** 1,829 eps (741/741 archivos) · grafo 2,687 nodos · **examen 98.8%** · es el
**AGENTE MAESTRO** (lee `for3slabs/mente-os-maestro` EN VIVO, puente E + skill 22).
Los exámenes cazaron **12 hallazgos, todos con fix sistémico** (joya H-11: la contraseña del
server vivía en 60 eps → redactada + tubo blindado).
👉 Detalle: memoria `project_entrenamiento_foresito` · `docs/analysis/Examen_Foresito_T6_Hallazgos.md`
· `work/Entrenamiento_Ejecucion_Reporte.md` · runners en `~/entrenamiento-runners/` del server.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

### 🆕 ⭐ LO ÚLTIMO (2026-07-31) — MENTE OS v2 TERMINADO Y VERIFICADO

**Mente OS pasó de DOCUMENTAR a GOBERNAR.** No es diseño: está en disco y medido.

| | |
|---|---|
| **Estado** | ✅ **F0-F8 cerradas y verificadas — v2 TERMINADO** (F8-4 pasó el 31-jul, sesión S8) |
| **Prueba** | `Mente/bin/test-f0-f6` — **correr esto primero, es la verdad.** ⚠️ **No confíes en un número escrito aquí:** la batería incluye `check-clear-ready`, que mide la sesión VIVA. Tras un `/clear` da **104/105** hasta que registres la sesión; luego **105/105**. Un 104 recién retomado es lo ESPERADO, no una regresión |
| **Commits** | `42dbfab` (279 archivos: v2 + migración) · `d667b14` (registro S7) |
| **Construido** | 11 validadores · 4 hooks · 3 niveles de reglas · sistema de apuntado |

**🗑️ La migración v1→v2 está COMPLETA (M0-M5, ADR-029).** `Alma/` `Cuerpo/` `Doc/` `Tickets/`
**eliminadas** — 186 documentos movidos uno por uno. Si un documento cita esas rutas, es una
cita fósil, no un archivo que falta. Solo quedan por decisión: `Cerebro/` (6, el grafo del
producto) y `Maestro/` (7, repo aparte).

**✅ F8-4 PASÓ (31-jul, S8):** el primer retomar real tras un `/clear` — el brief bastó, **cero
preguntas de estado**. Destapó 3 huecos (ya tapados) y se registraron las **3 sesiones huérfanas**,
incluida `4c187f33`, la del incidente del 21-jul, sin entrada 10 días *pese a que la regla la cita
por nombre*. Autopsias: `Cerebro/Registro_Conversaciones.md` §S8 y §R1-R3.

**👉 PRÓXIMO PASO — lo decide Brian.** El v2 no tiene fases pendientes. Lo abierto:
① **los 34 huecos de criterio** en `rules/qa-dimensions.md` + los 3 `principles/expertise/*.md`
— **solo Brian puede escribirlos**, ninguna IA · ② volver a **la demo** (§ abajo, 3 tapones).

**Deuda medida que NO bloquea:** ~73 citas rotas (56 de base + 17 que la migración destapó) ·
7 archivos sobre su límite de líneas · M6 (renombrar `Maestro/`) es **decisión de Brian**, y mi
recomendación medida es **no hacerlo**.

---

**🖥️⭐ LA DEMO ES UN BLOQUE GRANDE CON ÍNDICE PROPIO.** Antes de tocarla, leer la memoria
**`project_bloque_demo_pendientes`** — es el punto de entrada único: los 3 tapones que impiden
prestarla, los pendientes de producto/higiene, y 7 reglas aprendidas a base de romperla.
Repo del sitio: `ElBrAyAn1967/For3s` (≠ el del agente) · BD Neon · `main` en `793e858`.

**🏗️ (24-26 jul) DE MVP A PRODUCTO — ~15 bugs reales cerrados.** BD F1-F6 · cableado C1-C6 ·
pulido P1-P7 (−434 líneas muertas) · optimización (heartbeat −68%) · **6 archivos elevados a
producto** (`instancias.ts` · `session.ts` · `verificacion.ts` · `eventos.ts` · S4a "cero listas
fijas" · `userStore.ts` U1-U6 → C6p2 cerrado) · **`container.ts` ACTIVADO** (encender/apagar ya
no es NO-OP; `/ctl` nunca se expone) · **`DEMO_ENC_KEY` unificada** local=Vercel.
👉 Todo el detalle vive en las memorias que lista `project_bloque_demo_pendientes`.

**👉 PRÓXIMO PASO: los 3 tapones (por orden).** ① dueños de jazz/mashe → borrar
`allowedEmails.ts` con su `DEV_FALLBACK` que autoriza un correo falso (marcado DENTRO de la BD:
`COMMENT ON TABLE demo_duenos`) · ② tests de los 5 caminos críticos (hoy CERO) · ③ decidir el
hosting (todo cuelga de la laptop de Brian; se cayó 2 veces el 26-jul).

**⚠️ 2 caídas de producción el 26-jul, mismo error de método:** verificar desde mi entorno y
asumir que probaba el de Vercel. Regla: `feedback_tailscale_serve_apaga_funnel`.

## 5-ter · 🏗️ MENTE OS v2 — el PORQUÉ (diagnóstico 27-jul) · ✅ construido y cerrado, ver §5

**Causa raíz hallada:** el sistema DOCUMENTABA bien pero no GOBERNABA la ejecución.
**Ley que lo gobierna todo:** *lo que está en código se cumple 100%; lo que está en documento
falla 40-60%* → **la doctrina es documento, la VERIFICACIÓN es script.**

**Lo esencial del v2:** BLOQUE (unidad de trabajo, archivo único A-K) · 3 encargados + **Encargado 0
la VOZ** · 3 carriles · **fix ≠ parche** · contexto por bloque en disco · ⭐ **VEREDICTO DE CALIDAD
en 2 capas** · 4 capas para garantizar que un archivo se lea · **solo 3 acciones bloquean**.
Validado contra 4 frameworks (internOS · Agent OS · Open SWE · OpenTag): **ninguno responde *"¿esto
es producto o MVP?"*** → ese veredicto es el diferenciador real.

👉 El porqué: `principles/vision-mente-os-v2.md` (18 decisiones) · `docs/Arquitectura_Mente_OS_v2_Bloques.md`
· `docs/plan-v2-rollout.md` · `docs/analysis-internos-v1.md` · `docs/analysis-frameworks-v2.md`.
Memorias: `project_mente_os_v2_bloques` · `project_ser_duenos_del_contexto` · `project_incidente_degradacion_21jul`.

## 5-bis · Cerrados grandes recientes (solo punteros — historia en Bitácora Julio)

- 🌐 **SUPER-CEREBRO CONECTADO ✅** — Maestro F1-F5 + Foresito entrenado + 👑 Agente Maestro con
  puente E (§4). Visión: `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`.
- 🎯 **APRENDIZAJES DE CAMPO post-Incubathon** (`vision/Aprendizajes_De_Campo_Post_Incubathon.md`):
  🔴A ✅ · 🔵D ✅ H13 v0.16.0 · 🟠B ✅ MERCADO v0.17.0 · 🟣E ✅ CONFIANZA v0.18.0 ·
  🟡C multi-canal PENDIENTE (sin urgencia).
- **Congelados hasta orden de Brian** (NO empujar): brechas OpenClaw/Hermes (multi-canal, voz,
  cron conversacional, nudges…) · identidades secundarias · descubribilidad (SEO/AEO/GEO).
- **Deuda no urgente + menores abiertos:** H9 D1-D8 · H10 HP1-HP6 · /decidi RNN-LSTM · `/dmn valor
  on` fuera de brian · UX. Lista completa: **`memory/PENDIENTES.md`**.

## 6 · 🏆 Incubathon (jul 2026) + 🌉 puente a otros Mente OS

- **2º lugar de 200 empresas** con **NavigoX**. **La capa API de For3s cerró el pitch** → For3s OS
  VALIDADO como infraestructura con demanda real (2 clientes lo quieren). Memorias:
  `project_incubathon_2do_lugar_validacion` · `project_hito_hoteleria_navigox`.
- **🌉 NavigoX vive en su PROPIO Mente OS** (`~/5M-incubathon/Mente/`); aquí está **CERRADO**.
  ⛔ **NUNCA leerlo sin gate** — Brian escribe `acceder mente <proyecto>` + por qué → solo lectura.
  Cerrar con `cerrar mente <proyecto>`. **Motivo: que el consumo no se dispare.**
  Reglas: `bridges/Puentes_Mente_OS.md`.

## 7 · Reglas de oro con Brian (permanentes)

- ⛔ **NUNCA implementar sin explicar+aprobar primero** (`feedback_explicar_antes_de_implementar`).
- 🏗️ Hitos grandes = **Método de Fases "F"** (`rules/ESTANDAR_Metodo_Fases_F.md`): explicar→aprobar→
  construir · investigar terreno · caza bugs · **batería §5-BIS** (verifica TODO, no el carril) ·
  red de seguridad demostrable · commit firmado · server-primero.
- 📏 **Server-primero:** desarrollar+probar en el server; push a GitHub SOLO con orden explícita.
- ⛔ **NO loops de espera / procesos de fondo** contra el server que sigan si Brian cierra (gasta cuota).
- ⛔ **NO cambiar el modelo** (Brian lo fija con /model). Modelo del bot = sonnet-4-6 (NO bug).
- ⛔ **NO sesgar todo hacia la charla/descubribilidad** — importan pero NO son su foco; él marca el momento.
- 🔒 Master KEK offline · Brian nunca ve plaintext · audit inmutable · ante duda → preguntar.
- 🧹 **/clear es seguro cuando la conversación crezca** (Mente OS + memorias guardan todo).

---

## 📍 PUNTEROS — si necesitas MÁS que este brief

| Necesitas… | Lee… |
|---|---|
| **🖥️⭐ LA DEMO — índice maestro de sus pendientes (ENTRAR POR AQUÍ)** | memoria `project_bloque_demo_pendientes` |
| **TODOS los pendientes a detalle** | `memory/PENDIENTES.md` |
| **Secretos de la demo (DEMO_ENC_KEY) — FUERA de git** | `Mente/secrets/Secretos_Demo_Sitio.md` |
| Demo: Ronda F0 `userStore` · mapa · plan BD · auditoría | repo del sitio: `marca-personal/DEMO_*.md` |
| 🎓 **Caso: limpiar un hardcodeo heredado sin romper** ("default peligroso" + checklist) | `memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` |
| **Telemetría de conversaciones (registrar ANTES de cada `/clear`)** | `Cerebro/Registro_Conversaciones.md` |
| **Los 3 carriles dormidos** (Confianza · Presencia/SEO · Multi-canal) | `work/Carril_*.md` |
| Hito ENTRENAMIENTO (reporte · plan · flujo · catálogo · radiografías) | `work/Entrenamiento_*.md` · `work/Ronda_Entrenamiento_Plan_Maestro.md` · `work/Flujo_Extraccion_Entrenamiento.md` · `work/Plan_Backlog_Profundo_E6.md` · `docs/analysis/Radiografia_*` |
| Diseño arquitectónico maestro (11 nodos + 3 pilares) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| Historia cronológica de cierres | `memory/Bitacora_Progreso.md` |
| **Puente a otros Mente OS (NavigoX…) — reglas del gate** | `bridges/Puentes_Mente_OS.md` |
| Snapshot del estado anterior (84 KB) · contexto histórico (200 KB) | `memory/archive/Estado_Sesion_Snapshot_2026-07-07.md` · `memory/Estado_Sesion_Continuidad.md` (solo si imprescindible) |
| Multi-instancia · servidor (acceso+specs) | memorias `project_multi_instancia` · `reference_servidor_for3s` |
| Comparaciones vs Hermes/OpenClaw | `docs/analysis/Comparacion_For3s_OS_vs_*.md` |

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `memory/RETOMAR.md`).
