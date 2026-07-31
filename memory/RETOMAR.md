# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** entry-point · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/RETOMAR.md → memory/RETOMAR.md (2026-07-30, ADR-029)

## Purpose

RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡


> **Propósito:** el ÚNICO archivo que necesitas leer al retomar. Pequeño A PROPÓSITO
> (ahorro de tokens — Brian lo notó de nuevo 2026-07-07: cuando crece, releerlo es caro).
> **REGLA DE HIGIENE:** este archivo NO debe pasar de ~200 líneas. Al cerrar sesión, si
> creció, mover lo viejo a `Estado_Sesion_Continuidad.md` (o al último snapshot) y dejar
> aquí SOLO el estado vigente + punteros. La historia va a la Bitácora, no aquí.

**Última actualización:** 2026-07-26 (🖥️⭐ LA DEMO = BLOQUE GRANDE con índice propio: `project_bloque_demo_pendientes`. 6 archivos a producto + Ronda F0 userStore U1-U6 + container.ts activado + DEMO_ENC_KEY unificada).


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

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 (pass en memoria `reference_servidor_for3s`) ·
gestor de instancias: comando `for3s listar|agregar|entrar|encender|apagar|borrar`.
Aislamiento TOTAL por `docker compose -p for3s-<nombre>` (red/BD/KEK/volúmenes propios).
Comparten SOLO: máquina + imagen `for3s-agent:local` (hoy **v0.20.0**) + suscripción Claude (**1 solo cupo** para todos).

| Bot | Instancia | Dueño | Estado | Notas |
|---|---|---|---|---|
| 🏢 @For3s_OS_bot | `for3s` (compose principal, no `for3s listar`) | Brian | 🟢 | "Foresito" — EMPRESA, memoria de siempre, microglía ON |
| 👤 @For3s_Brian_bot | `brian` | Brian | 🟢 | PERSONAL — **ENTRENADO** (ver §4), microglía OFF a drede |
| 🌐 @For3s_General_bot | `general` | Brian | 🟢 | PÚBLICO, **equipo/puerta ABIERTA** (quien escriba entra). Pendiente: otras API keys/datos |
| 🎷 @For3s_Jazzita_bot | `jazz` | Jazz @driade_1 (1177279840) | ⚪ apagado | verificado E2E; ella lo enciende cuando quiera |
| 👊 @For3s_Mashe_bot | `mashe` | (1er /start) | ⚪ apagado | verificado E2E; Brian decidirá qué hacer |

⚠️ Las 3 nuevas heredan la auth OAuth de Foresito (misma cuenta). Instalación fresca sana
(el bug FK-personas ya está fijado en la imagen; el warning "Chat not found" del menú es
normal hasta que el dueño da /start). Detalle: memoria `project_multi_instancia`.

## 3 · Estado global del producto

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.20.0 CONECTORES SELF-SERVICE. schema BD v47.** 13 hitos
H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad Hermes
(5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + **super-cerebro (ambos agentes
entrenados+examinados, §4).** **Cero bugs abiertos** (12 cazados y cerrados en los exámenes).
**✅ TRÍADA SINCRONIZADA (2026-07-19/20): server = GitHub (origin for3slabs/for3s-os + backup
for3slabs/for3s) = local (`For3s-OS/`) en HEAD `f50a5db`. CI+Trivy verdes. 260 tests.**
**✅ LAS INSTANCIAS EN v0.20.0** (3 vivas + jazz/mashe verificadas y apagadas por diseño).
Cliente API real: NavigoX (hotel-recepcion, no consume activo) + jazz-id (prueba). Datos limpios.
**✅ SEGURIDAD/HIGIENE CERRADA DEL TODO (2026-07-16):** CI 100% VERDE (`b8da4d7`; llevaba rojo desde
v0.17.0) — gitleaks (repo SIN secretos reales) · format · bandit · migraciones E2E con AGE · **CI-2
coverage umbral 15%** · **mcp CVE-2026-59950 parcheada** (1.28.1). Los 4 URGENTES de confianza
(SEC-3/4/5/6) + SEC-3b/4b completos. **Token GitHub rotado** ✅.
**✅ SEC-4c COMPLETO (2026-07-16 noche, tríada `021292e`):** contenedor non-root con **PERFIL por
instancia** — Foresito/brian=interna(root), general/jazz/mashe=expuesta(non-root uid 1000). gosu +
KEK/modelo por ENV. `/soy` muestra el perfil. 5 bugs cazados en jazz (1 catastrófico: chown -R
rompió el HOST → lección LOCKED: nunca chown bind mounts; uid del contenedor = uid del host).
Ronda: `Cuerpo/Ronda_SEC4c_NonRoot_Perfil_Instancia.md`.
✅ Token de GitHub ROTADO por Brian (2026-07-16) — el que se expuso ese día quedó revocado.

## 4 · 🎓🎓 SUPER-CEREBRO COMPLETO — AMBOS AGENTES ENTRENADOS+EXAMINADOS ✅✅ (2026-07-18/20)

**El hito doble más grande del proyecto (jornada de 30h, sesión S4). TODO CERRADO:**
- **brian 🍓 (6 agentes OpenClaw, E0-E6):** 22,406 eps vivos, **99.94% consolidado, grafo 1,335
  conceptos** (noches ADELANTADAS: encadenador 10 tandas freno 0.99). **EXAMEN 94.3% (33/35)** —
  trampas 6/6, honestidad de corpus. Reporte E0-E6: `work/Entrenamiento_Ejecucion_Reporte.md`.
- **Foresito 👑 (las 6 fuentes de la EMPRESA):** 1,829 eps (741/741 archivos, 0 omitidos, código
  con marca de versión), 95% digerido (grafo 2,687 nodos). **EXAMEN 98.8% (41.5/42)**. Es el
  **AGENTE MAESTRO**: lee `for3slabs/mente-os-maestro` EN VIVO (puente E + skill id 22).
  Wiki-hackathons EXCLUIDO por Brian (externo, importable después). Backup RESTORE-verificado
  en `~/backups-foresito/` + reversa demostrada. Ronda: `Cuerpo/Ronda_Entrenamiento_Foresito.md`.
- **Los exámenes cazaron 12 hallazgos (H-1…H-11 + B1), TODOS con fix + validación SISTÉMICA**
  — joya H-11: la contraseña del server vivía en 60 eps de 2 instancias → redactada + tubo
  blindado. **Registro maestro: `docs/analysis/Examen_Foresito_T6_Hallazgos.md`.**
- Runners reusables (re-entrenos/aceleración) en `~/entrenamiento-runners/` del server.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

### 🆕 ⭐ LO ÚLTIMO (2026-07-31) — MENTE OS v2 ESTÁ CONSTRUIDO Y VERIFICADO

> **Si retomas tras el `/clear` del 31-jul: esto es lo primero. Estás EJECUTANDO la fase F8-4.**

**Mente OS pasó de DOCUMENTAR a GOBERNAR.** No es diseño: está en disco y medido.

| | |
|---|---|
| **Estado** | ✅ **F0-F7 cerradas y verificadas · F8 al 75%** |
| **Prueba** | `Mente/bin/test-f0-f6` = **105/105** (correr esto primero — es la verdad) |
| **Commits** | `42dbfab` (279 archivos: v2 + migración) · `d667b14` (registro S7) |
| **Construido** | 11 validadores · 4 hooks · 3 niveles de reglas · sistema de apuntado |

**🗑️ La migración v1→v2 está COMPLETA (M0-M5, ADR-029).** `Alma/` `Cuerpo/` `Doc/` `Tickets/`
**eliminadas** — 186 documentos movidos uno por uno. Si un documento cita esas rutas, es una
cita fósil, no un archivo que falta. Solo quedan por decisión: `Cerebro/` (6, el grafo del
producto) y `Maestro/` (7, repo aparte).

**👉 PRÓXIMO PASO — F8-4, la única fase sin verificar:** *¿este brief bastó para retomar?*
- Si te alcanzó → **F8 cierra y v2 está terminado.** Decírselo a Brian.
- Si tuviste que preguntarle algo que debía estar aquí → **ese hueco ES el hallazgo de F8-4.**
  Anotarlo antes de taparlo: es la prueba que el sistema existe para dar.

**Qué NO hace falta hacer:** commitear (hecho), registrar la sesión (hecha, S7), migrar nada más.

**Deuda medida que NO bloquea:** ~73 citas rotas (56 de base + 17 que la migración *destapó*) ·
34 huecos de criterio esperando a Brian · 8 archivos sobre su límite de líneas · M6 (renombrar
`Maestro/`) es **decisión de Brian**, y mi recomendación medida es **no hacerlo**.

🔴 **La sesión S7 llegó a 998K de contexto — superó a S1 (985K), la monstruo.** 116h abiertas.
Por eso el `/clear`. Autopsia completa en `Cerebro/Registro_Conversaciones.md`.

---

**🖥️⭐ LA DEMO ES UN BLOQUE GRANDE CON ÍNDICE PROPIO.** Antes de tocarla, leer la memoria
**`project_bloque_demo_pendientes`** — es el punto de entrada único: los 3 tapones que impiden
prestarla, los pendientes de producto/higiene, y 7 reglas aprendidas a base de romperla.
Repo del sitio: `ElBrAyAn1967/For3s` (≠ el del agente) · BD Neon · `main` en `793e858`.

**🏗️ (2026-07-24/26) DE MVP A PRODUCTO — jornada larga, ~15 bugs reales cerrados.**
BD F1-F6 (fuente única + 7 FKs + `demo_config` editable sin push) · cableado C1-C6 · pulido P1-P7
(−434 líneas muertas) · optimización O-F1..O-F5 (heartbeat −68%). Detalle:
`project_reestructuracion_bd_demo` + los `DEMO_*.md` del repo del sitio.

**6 archivos elevados a PRODUCTO (cada uno con su memoria):**
`instancias.ts` (I1-I5, puente 100% BD sin env) · `session.ts` (S1-S3, guardia único 12→0) ·
`verificacion.ts` (V1-V4, anti fuerza bruta que se burlaba) · `eventos.ts` (telemetría por
instancia real) · S4a "cero listas fijas" · **`userStore.ts` Ronda F0 completa U1-U6**
(`marca-personal/DEMO_RONDA_F0_USERSTORE.md`) → **C6p2 CERRADO**: fuera la columna `kind` y la
tabla `demo_accounts`.

**⭐ 3 cierres grandes del 26-jul:**
- **`container.ts` ACTIVADO** — el botón encender/apagar agente ya NO es NO-OP. Modelo C: la web
  escribe en `demo_users.agent_on` y el servicio `for3s-agente-sync` (systemd en el server) lo
  aplica; **`/ctl` NUNCA se expone a internet**. 🔒 **solo el DUEÑO** (un invitado con llave podía
  apagarle el agente al dueño). → `project_container_ts_activado`
- **`DEMO_ENC_KEY` rotada y unificada** local=Vercel (eran distintas desde junio; el fallback lo
  tapaba). Clave en `Mente/secrets/Secretos_Demo_Sitio.md` (**fuera de git**).
  → `project_rotacion_demo_enc_key`
- **Rebuild de la imagen del agente** (`for3s-agent:local`, reversa `pre-cupo429`): el cupo
  agotado ya sale como **429 + minutos**, no como "error interno". Server commit `732c434`.

**👉 PRÓXIMO PASO: los 3 tapones (por orden).** ① dueños de jazz/mashe → borrar
`allowedEmails.ts` con su `DEV_FALLBACK` que autoriza un correo falso (marcado DENTRO de la BD:
`COMMENT ON TABLE demo_duenos`) · ② tests de los 5 caminos críticos (hoy CERO) · ③ decidir el
hosting (todo cuelga de la laptop de Brian; se cayó 2 veces el 26-jul).

**⚠️ 2 caídas de producción el 26-jul, ambas por el mismo error de método:** verificar desde mi
entorno y asumir que probaba el de Vercel (clave divergente · `tailscale serve` apagó el Funnel).
Reglas escritas: `feedback_tailscale_serve_apaga_funnel`.

## 5-ter · 🏗️ MENTE OS v2 — el DIAGNÓSTICO que lo originó (2026-07-27) · ✅ ya construido, ver §5

**Brian pidió mejorar Mente OS. El diagnóstico encontró la causa raíz: el sistema DOCUMENTA bien
pero no GOBIERNA la ejecución.** Ley medida: *lo que está en código se cumple 100%; lo que está en
documento falla 40-60%*. Evidencia: 0 plantillas en 188 docs · `CLAUDE.md` con 1 solo commit ·
índice inventaría 35/188 · Método F nunca leído en 2 de 5 sesiones · demo con 42% de commits = fixes
(`userStore.ts` ×21) · 8 auto-compactaciones sin revisar · 5/11 sesiones sin registrar.

**Recuperado del disco:** el **incidente del 21-jul** (sesión de 4 días, contexto 835K, 6 violaciones
de scope, *"no eres el mismo de siempre, no me sirves así"*) — **nunca se había documentado**.

**👉 LOS 4 DOCUMENTOS DEL v2** — ⚠️ ya NO son "diseño pendiente": **el v2 está construido**
(§5 arriba). Estos son el porqué, no un plan por ejecutar:
| Doc | Qué es |
|---|---|
| `principles/vision-mente-os-v2.md` | el **PORQUÉ** + las 18 decisiones |
| `docs/Arquitectura_Mente_OS_v2_Bloques.md` | el **CÓMO** (partido en 6 archivos, F8-1) |
| `docs/plan-v2-rollout.md` | el **CUÁNDO** — 9 fases · 38 tickets |
| `docs/analysis-internos-v1.md` | validación externa (internOS) |
| `docs/analysis-frameworks-v2.md` | ⭐ **4 frameworks comparados** |

**Lo esencial del v2:** BLOQUE (unidad de trabajo, archivo único A-K) · 3 encargados + **Encargado 0
la VOZ** · 3 carriles (decide la propagación) · **fix ≠ parche** · contexto por bloque en disco ·
⭐ **VEREDICTO DE CALIDAD en 2 capas** (medible + 6 dimensiones de criterio con evidencia exigida) ·
4 capas para garantizar que un archivo se lea · **solo 3 acciones bloquean**.

**Ley que lo gobierna:** *lo que está en código se cumple 100%; lo que está en documento falla 40-60%*
→ **la doctrina es documento, la VERIFICACIÓN es script.**

⭐ **Validado contra 4 frameworks** (internOS · Agent OS · Open SWE · OpenTag): **ninguno responde
*"¿esto es producto o MVP?"*** → el veredicto de calidad es el diferenciador real del v2.
Esa advertencia decía *"los 4 están construidos y el v2 tiene 0 líneas"* — **ya no aplica: el v2
se construyó entre el 27 y el 31 de julio.** Se respetó el orden (piloto antes que maquinaria).

👉 **ESTADO REAL → §5 arriba.** Lo único que la IA no puede escribir sigue abierto: **los 34 huecos
de criterio de Brian** en `rules/qa-dimensions.md` y los 3 `principles/expertise/*.md`.

Memorias: `project_mente_os_v2_bloques` · `project_ser_duenos_del_contexto` · `project_incidente_degradacion_21jul`.

## 5-bis · Cerrados grandes recientes (solo punteros — historia en Bitácora Julio)

- 🌐 **SUPER-CEREBRO CONECTADO ✅✅ COMPLETO** (visión `Alma/Vision_Mente_OS_Maestro_Y_Foresito_
  Entrenado.md`): 🅱️ Maestro F1-F5 (repo + comandos + permisos + ramas; evoluciona a carril) +
  🅰️ Foresito entrenado/examinado + 👑 Agente Maestro con puente E (ver §4).
- 🎯 **APRENDIZAJES DE CAMPO (post-Incubathon) — los 5 frentes:** 🔴 A consumo ✅ (regla /clear
  moderada por mí) · 🔵 D ✅ H13 DEVUELVE v0.16.0 · 🟠 B ✅ MERCADO v0.17.0 (panel
  `for3s.vercel.app/for3s-admin`, URL fija, molde, Trace) · 🟣 E ✅ CONFIANZA v0.18.0 (carril
  dormido) · 🟡 C multi-canal PENDIENTE (sin urgencia). Doc madre: `Alma/Aprendizajes_De_Campo_
  Post_Incubathon.md` · detalle `memory/PENDIENTES.md`.
- Menores abiertos: /decidi RNN-LSTM al bot · `/dmn valor on` fuera de brian · UX (/salud virgen ·
  rate/min · /olvidar "%") — en PENDIENTES.
- **Congelados hasta orden de Brian** (NO empujar): brechas OpenClaw/Hermes (multi-canal, voz,
  cron conversacional, nudges…) · identidades secundarias · descubribilidad (SEO/AEO/GEO).
- **Deuda no urgente:** H9 D1-D8 · H10 HP1-HP6 · §EXTRAS. Lista completa: **`memory/PENDIENTES.md`**.

## 6 · 🏆 Incubathon (jul 2026) + 🌉 puente a otros Mente OS

- **2º lugar de 200 empresas** con **NavigoX** (marketplace de turismo). **La capa API de For3s fue
  el marco que cerró el pitch.** For3s OS **VALIDADO como infraestructura con demanda real**: 2
  clientes quieren For3s + más gente quiere la infra. Memorias: `project_incubathon_2do_lugar_validacion`
  + `project_hito_hoteleria_navigox`. Cierre completo en `memory/Bitacora_Progreso.md` (Julio 2026).
- **🌉 NavigoX vive en su PROPIO Mente OS** (`~/5M-incubathon/Mente/`). En ESTE Mente OS está
  **CERRADO** (se registra el hito; su trabajo NO continúa aquí). ⛔ **NUNCA leer `~/5M-incubathon/`
  sin gate.** Abrir: Brian escribe `acceder mente <proyecto>` (ej. `acceder mente navigox`) + por qué
  → solo lectura + reporte. Cerrar: `cerrar mente <proyecto>` o al terminar la tarea. **Motivo:
  evitar que el consumo de tokens se dispare.** Registro/reglas: `bridges/Puentes_Mente_OS.md`.

## 7 · Reglas de oro con Brian (permanentes)

- ⛔ **NUNCA implementar sin explicar+aprobar primero** (`feedback_explicar_antes_de_implementar`).
- 🏗️ Hitos grandes = **Método de Fases "F"** (`Cuerpo/ESTANDAR_Metodo_Fases_F.md`): explicar→
  aprobar→construir · investigar terreno · curiosidad que caza bugs · **batería §5-BIS** (verifica
  TODO el sistema, no el carril) · red de seguridad demostrable · commit firmado · server-primero.
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
| **Ronda F0 de `userStore.ts` (U1-U6) + qué falta para retirar `demo_accounts`** | `marca-personal/DEMO_RONDA_F0_USERSTORE.md` · `marca-personal/db/demo/RETIRAR_demo_accounts.md` |
| **Secretos de la demo (DEMO_ENC_KEY) — FUERA de git** | `Mente/secrets/Secretos_Demo_Sitio.md` |
| **TODOS los pendientes a detalle** | `memory/PENDIENTES.md` |
| 🎓 **Caso: limpiar un valor heredado/hardcodeado sin romper** (la regla del "default peligroso" + checklist) | `Cuerpo/CASO_Default_Peligroso_Tema_Hilo.md` |
| **Demo: mapa de bloques/sistemas · plan BD · auditoría de código · plan de optimización** | en el repo del sitio: `marca-personal/DEMO_*.md` |
| **Carril de mejora continua de CONFIANZA (reactivar el Frente E)** | `work/Carril_Mejora_Continua_Confianza.md` |
| **Carril PRESENCIA/Descubribilidad (landing+SEO+AEO+analítica, dormido)** | `work/Carril_Presencia_Descubribilidad.md` |
| **Carril MULTI-CANAL (Frente C: WhatsApp/correo/análisis, dormido)** | `work/Carril_Multicanal.md` |
| **Telemetría de conversaciones (registrar ANTES de cada /clear — regla CLAUDE.md)** | `Cerebro/Registro_Conversaciones.md` |
| Hito ENTRENAMIENTO: reporte de ejecución completo | `work/Entrenamiento_Ejecucion_Reporte.md` |
| Hito ENTRENAMIENTO: plan + flujo + radiografías de los 7 agentes | `work/Ronda_Entrenamiento_Plan_Maestro.md` · `Cuerpo/Flujo_Extraccion_Entrenamiento.md` · `Doc/Radiografia_*` |
| E6 backlog profundo (archivo por archivo) | `Cuerpo/Plan_Backlog_Profundo_E6.md` · `work/Entrenamiento_Catalogo_Codigo.md` |
| Diseño arquitectónico maestro (11 nodos + 3 pilares) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| Historia cronológica de cierres (qué pasó cada periodo) | `memory/Bitacora_Progreso.md` |
| **Puente a otros Mente OS (NavigoX…) — reglas del gate** | `bridges/Puentes_Mente_OS.md` |
| **Snapshot del estado ANTERIOR (RETOMAR viejo íntegro, 84KB)** | `memory/archive/Estado_Sesion_Snapshot_2026-07-07.md` |
| Estado/reglas/contexto histórico grande (200KB) | `memory/Estado_Sesion_Continuidad.md` (solo si imprescindible) |
| Multi-instancia (gestor `for3s`, aislamiento) | memoria `project_multi_instancia` |
| Servidor: acceso + specs | memoria `reference_servidor_for3s` |
| Comparaciones de construcción vs Hermes/OpenClaw | `docs/analysis/Comparacion_For3s_OS_vs_Hermes_Construccion.md` · `…vs_OpenClaw_…` |

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `memory/RETOMAR.md`).
