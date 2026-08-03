# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-02 · **Owner:** brian
**Migrated:** Doc/RETOMAR.md → memory/RETOMAR.md (2026-07-30, ADR-029)

> **El ÚNICO archivo que necesitas leer al retomar.** Pequeño a propósito: **máximo 200 líneas**,
> lo aplica `bin/check-health`. Al cerrar, la historia va a la Bitácora, no aquí.
> ⚠️ **UNA sola fecha, la de la cabecera** (dos fue un hueco real de F8-4).

---

## 1 · Quién + qué (10 segundos)

- **Brian López** (founder, NO "Aguilar"). Email ema@frutero.club / brayan002150@gmail.com.
- **Proyecto = SOLO For3s OS.** Cerebro documental: `/home/brianweb3/for3s/Mente/` = **"Mente OS"**.
  ⛔ NO tocar `marca-personal/Mente/` (otro proyecto) sin permiso.
  ⛔ **NO leer `~/5M-incubathon/` (Mente OS de NavigoX) sin gate** — ver §7 (protege consumo).
- **Fuente de verdad arquitectónica:** `Cerebro/For3s_OS_Grafo_Maestro.md`.
- For3s OS = **agente "segundo cerebro" autónomo, self-hosted** en el servidor `for3s`
  (Telegram + consola, Python 3.12 + Postgres+AGE+pgvector, contenerizado). EN PRODUCCIÓN.

## 2 · Servidor `for3s` — 5 FOR3S OS al mismo tiempo

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 (pass en `reference_servidor_for3s`) · gestor:
`for3s listar|agregar|entrar|encender|apagar|borrar`. Aislamiento TOTAL por
`docker compose -p for3s-<nombre>`. Comparten SOLO: máquina + imagen (**v0.20.0**) + suscripción
Claude (**1 solo cupo** para todas).

| Bot | Instancia | Dueño | Estado |
|---|---|---|---|
| 🏢 @For3s_OS_bot | `for3s` | Brian | 🟢 "Foresito" — EMPRESA, microglía ON |
| 👤 @For3s_Brian_bot | `brian` | Brian | 🟢 PERSONAL — **ENTRENADO** (§4), microglía OFF a drede |
| 🌐 @For3s_General_bot | `general` | Brian | 🟢 PÚBLICO, puerta ABIERTA |
| 🎷 @For3s_Jazzita_bot | `jazz` | Jazz @driade_1 | ⚪ apagado — verificado E2E |
| 👊 @For3s_Mashe_bot | `mashe` | (1er /start) | ⚪ apagado — verificado E2E |

⚠️ Las 3 nuevas heredan la auth OAuth de Foresito. Detalle: memoria `project_multi_instancia`.

## 3 · Estado global del producto

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.20.0 CONECTORES SELF-SERVICE · schema BD v47.**
13 hitos H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad
Hermes (5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + super-cerebro (§4).
**Cero bugs abiertos.**

- **✅ TRÍADA SINCRONIZADA** (19/20-jul): server = GitHub (`for3slabs/for3s-os` + backup) = local
  en HEAD `f50a5db`. CI+Trivy verdes · 260 tests. Instancias en v0.20.0.
- **✅ SEGURIDAD CERRADA** (16-jul): CI 100% verde (`b8da4d7`) · SEC-3/4/5/6 + 3b/4b · token
  rotado · **SEC-4c** non-root con perfil por instancia (`021292e`).
  🔒 lección LOCKED: **nunca `chown -R` un bind mount** (`feedback_nunca_chown_bind_mount`).

## 4 · 🎓🎓 SUPER-CEREBRO — ambos agentes entrenados+examinados ✅ (18/20-jul)

**brian 🍓** 22,406 eps · 99.94% consolidado · **examen 94.3%**. **Foresito 👑** 1,829 eps ·
grafo 2,687 nodos · **examen 98.8%** · es el **AGENTE MAESTRO** (lee `for3slabs/mente-os-maestro`
EN VIVO). Los exámenes cazaron **12 hallazgos con fix sistémico** (joya H-11: la contraseña del
server vivía en 60 eps → redactada). 👉 `project_entrenamiento_foresito` ·
`docs/analysis/Examen_Foresito_T6_Hallazgos.md` · `work/Entrenamiento_Ejecucion_Reporte.md`.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

### 🆕 ⭐ LO ÚLTIMO (2026-08-02) — v2 ENDURECIDO Y **PUBLICADO**

**El v2 ya estaba terminado; esta jornada (S8, 50h) lo puso a prueba contra sí mismo.**
12 commits. **Batería 105 → 138.** Detalle: `Cerebro/Registro_Conversaciones.md` §S8.

| | |
|---|---|
| 🌍 **Público** | **`github.com/fruterito101/mente-os`** — MIT, 97 archivos, historial limpio. Solo el MOTOR: sin `work/` `memory/` `Cerebro/`, sin datos de clientes ni de terceros (14 categorías escaneadas antes de publicar) |
| 🔒 **Seguridad** | el token de GitHub, AWS y GPG estuvieron **expuestos**: `Read(//home/**)` con un `deny` de 5 objetivos. Cerrado — y el guardia ahora **descubre** credenciales en vez de consultar una lista de tres |
| 🫀 **El latido** | arranque y las 3 puertas dejan prueba de que siguen vivos (`.heartbeat` · `.beats/`). El silencio de un guardia dejó de ser indistinguible de la salud |
| 🔌 **Portable** | motor / instancia separados en `mente.config.yml`. Probado clonando de verdad |

> ⭐ **EL HALLAZGO QUE VALE MÁS QUE LOS ARREGLOS — el mismo error, 5 veces:**
> `check-clear-ready` vigilaba una ruta pero no si existía · el `deny` cubría 3 herramientas
> pero no Bash · `SENSITIVE` listaba 3 credenciales · `GUARDS` vigilaba 9 de 21 validadores ·
> los hooks se comprobaban en disco pero no su registro.
> **Cada mitad vigilada y nadie vigilando la costura.**
>
> **La regla:** una lista que enumera lo **PROTEGIDO** debe medirse; una que enumera lo
> **PERMITIDO** puede escribirse, si lo desconocido **falla cerrado**. (Auditadas las 22
> enumeraciones: 19 estaban bien, varias a propósito.) → `rules/rule-config-hygiene.md`

**🔑🔐 2 ABIERTOS, decide Brian** — FIRMA GPG (sin clave aquí; ✅ identidad ya es `Brian Lopez <brayan002150@gmail.com>`) · `~/.claude.json` guarda el OAuth del harness y **`deny` no es sandbox**: el matcher lee el TEXTO del comando, no la ruta — `"$(ls …)"` lo esquiva. Ambos con sus opciones en `PENDIENTES.md` §🔑 §🔐.

**👉 PRÓXIMO PASO — no hay deuda técnica que valga la pena.** Lo único abierto es lo que
ninguna IA puede escribir: **los huecos de criterio** (`docs/METRICS.md` · `criterion.holes`).
Recomendación medida: empezar por `principles/expertise/val-integration.md` — 6 casos tuyos ya en
la mesa, dos con producción caída. Son **8 huecos** (las 6 dimensiones de §2 + §3 + §4), no 2.

⚠️ **Y lo que sigue sin cambiar:** el v2 **nunca ha gobernado trabajo real de producto**. Los 12
commits de S8 son el sistema arreglándose a sí mismo. Cero sesiones de demo o de agente.

---

### LO ANTERIOR (2026-07-31) — el v2 se construyó y F8-4 lo verificó

**Mente OS pasó de DOCUMENTAR a GOBERNAR.** F0-F8 cerradas · commits `42dbfab` (279 archivos:
v2 + migración) y `d667b14`. **Prueba:** `Mente/bin/test-f0-f6` — lo único que importa es
`failed: 0`; el conteo vive en `docs/METRICS.md` (`battery.checks`), nunca escrito aquí.

**La migración v1→v2 está COMPLETA** (M0-M5, ADR-029): `Alma/` `Cuerpo/` `Doc/` `Tickets/`
eliminadas, 186 documentos movidos. Si un documento cita esas rutas es una **cita fósil**, no un
archivo que falta. Quedan por decisión: `Cerebro/` (el grafo del producto) y `Maestro/` (repo
aparte). **F8-4 pasó:** el brief bastó, cero preguntas de estado.

**Deuda medida que NO bloquea:** ~73 citas rotas · archivos sobre su límite · M6 (renombrar
`Maestro/`) es decisión de Brian y mi recomendación medida es **no hacerlo**.

---

**🖥️⭐ LA DEMO ES UN BLOQUE GRANDE CON ÍNDICE PROPIO.** Antes de tocarla, leer la memoria
**`project_bloque_demo_pendientes`** — punto de entrada único: los 3 tapones, los pendientes de
producto/higiene y 7 reglas aprendidas rompiéndola. Repo: `ElBrAyAn1967/For3s` · BD Neon.

**(24-26 jul) DE MVP A PRODUCTO — ~15 bugs cerrados:** BD F1-F6 · cableado · pulido (−434 líneas
muertas) · heartbeat −68% · **6 archivos elevados a producto** · `container.ts` ACTIVADO ·
`DEMO_ENC_KEY` unificada. Detalle en las memorias que lista el índice.

**👉 3 TAPONES (por orden):** ① dueños de jazz/mashe → borrar `allowedEmails.ts` con su
`DEV_FALLBACK` que autoriza un correo falso · ② tests de los 5 caminos críticos (hoy CERO) ·
③ decidir el hosting (todo cuelga de la laptop de Brian; se cayó 2 veces el 26-jul).

**⚠️ 2 caídas de producción, mismo error:** verificar desde mi entorno y asumir que probaba el de
Vercel. Regla: `feedback_tailscale_serve_apaga_funnel`.

## 5-ter · 🏗️ el PORQUÉ del v2 (diagnóstico 27-jul) · ✅ construido, ver §5

**Causa raíz:** el sistema DOCUMENTABA bien pero no GOBERNABA la ejecución.
**La ley:** *lo que está en código se cumple 100%; lo que está en documento falla 40-60%* →
**la doctrina es documento, la VERIFICACIÓN es script.**

**Lo esencial:** BLOQUE (archivo único A-K) · 3 encargados + Encargado 0 la VOZ · 3 carriles ·
fix ≠ parche · ⭐ **veredicto de calidad en 2 capas** · solo 3 acciones bloquean. Validado contra
4 frameworks: **ninguno responde *"¿producto o MVP?"*** → ese veredicto es el diferenciador.

👉 `principles/vision-mente-os-v2.md` · `docs/Arquitectura_Mente_OS_v2_Bloques.md` ·
`docs/plan-v2-rollout.md` · `docs/analysis-frameworks-v2.md`. Memorias:
`project_mente_os_v2_bloques` · `project_ser_duenos_del_contexto` · `project_incidente_degradacion_21jul`.

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
