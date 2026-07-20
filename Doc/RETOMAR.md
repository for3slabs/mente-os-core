# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

> **Propósito:** el ÚNICO archivo que necesitas leer al retomar. Pequeño A PROPÓSITO
> (ahorro de tokens — Brian lo notó de nuevo 2026-07-07: cuando crece, releerlo es caro).
> **REGLA DE HIGIENE:** este archivo NO debe pasar de ~200 líneas. Al cerrar sesión, si
> creció, mover lo viejo a `Estado_Sesion_Continuidad.md` (o al último snapshot) y dejar
> aquí SOLO el estado vigente + punteros. La historia va a la Bitácora, no aquí.

**Última actualización:** 2026-07-20 (⭐ MAESTRO PUENTES C+D CONSTRUIDOS: búsqueda semántica + grafo de Mente OS sobre núcleo único — ver §5).


---

## 1 · Quién + qué (10 segundos)

- **Brian López** (founder, NO "Aguilar"). Email ema@frutero.club / brayan002150@gmail.com.
- **Proyecto = SOLO For3s OS.** Cerebro documental: `/home/brianweb3/for3s/Mente/` = **"Mente OS"**.
  ⛔ NO tocar `marca-personal/Mente/` (otro proyecto) sin permiso.
  ⛔ **NO leer `~/5M-incubathon/` (Mente OS de NavigoX) sin gate** — ver §7 (protege consumo).
- **Fuente de verdad arquitectónica:** `Mente/Cerebro/For3s_OS_Grafo_Maestro.md`.
- For3s OS = **agente "segundo cerebro" autónomo, self-hosted** en el servidor `for3s`
  (Telegram + consola, Python 3.12 + Postgres+AGE+pgvector, contenerizado). EN PRODUCCIÓN.

## 2 · Servidor `for3s` — 5 FOR3S OS al mismo tiempo (2026-07-07)

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 (pass en memoria `reference_servidor_for3s`) ·
gestor de instancias: comando `for3s listar|agregar|entrar|encender|apagar|borrar`.
Aislamiento TOTAL por `docker compose -p for3s-<nombre>` (red/BD/KEK/volúmenes propios).
Comparten SOLO: máquina + imagen `for3s-agent:local` (hoy v0.19.0) + suscripción Claude (**1 solo cupo** para todos).

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

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.19.0 ENTRENADO. schema BD v45.** 13 hitos
H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad Hermes
(5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + **super-cerebro (ambos agentes
entrenados+examinados, §4).** **Cero bugs abiertos** (12 cazados y cerrados en los exámenes).
**✅ TRÍADA SINCRONIZADA (2026-07-19/20): server = GitHub (origin for3slabs/for3s-os + backup
for3slabs/for3s) = local (`For3s-OS/`) en HEAD `f50a5db`. CI+Trivy verdes. 260 tests.**
**✅ LAS 5 INSTANCIAS EN v0.19.0** (3 vivas + jazz/mashe verificadas y apagadas por diseño).
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
  trampas 6/6, honestidad de corpus. Reporte E0-E6: `Doc/Entrenamiento_Ejecucion_Reporte.md`.
- **Foresito 👑 (las 6 fuentes de la EMPRESA):** 1,829 eps (741/741 archivos, 0 omitidos, código
  con marca de versión), 95% digerido (grafo 2,687 nodos). **EXAMEN 98.8% (41.5/42)**. Es el
  **AGENTE MAESTRO**: lee `for3slabs/mente-os-maestro` EN VIVO (puente E + skill id 22).
  Wiki-hackathons EXCLUIDO por Brian (externo, importable después). Backup RESTORE-verificado
  en `~/backups-foresito/` + reversa demostrada. Ronda: `Cuerpo/Ronda_Entrenamiento_Foresito.md`.
- **Los exámenes cazaron 12 hallazgos (H-1…H-11 + B1), TODOS con fix + validación SISTÉMICA**
  — joya H-11: la contraseña del server vivía en 60 eps de 2 instancias → redactada + tubo
  blindado. **Registro maestro: `Doc/Examen_Foresito_T6_Hallazgos.md`.**
- Runners reusables (re-entrenos/aceleración) en `~/entrenamiento-runners/` del server.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

**🚀 v0.19.0 "ENTRENADO" DESPLEGADA TOTAL (2026-07-19/20):** tríada de código en **`f50a5db`**
(server = GitHub origin `for3s-os` + backup `for3s` = local) · **las 5 instancias verificadas EN
VIVO** (3 vivas propagadas + jazz/mashe probadas con batería completa y devueltas a su estado) ·
CI ✅ + Trivy ✅ · Mente OS pusheado (`mente-os-for3s` `80aed31`) · Maestro al día (`8681d7c`).
Historia de v0.16→0.18 (MERCADO, Molde, Trace, Frente E): **Bitácora Julio** + `CHANGELOG.md`.

**⭐ NUEVO (2026-07-20) — MAESTRO PUENTES C+D ✅ CONSTRUIDOS Y E2E** (`Cuerpo/Ronda_Maestro_
Puentes_C_D.md`): el Maestro dejó de ser lista → es BUSCADOR semántico + RED navegable, todo
sobre UN núcleo (punteros.tsv + puerta única + un indexador + IDs compartidos + una superficie
`/v1/maestro/*` en Foresito). `maestro indexar --todo | subir | buscar "<preg>" [--contexto] |
grafo <nodo>`. Jazz solo ve su carril (probado). 4 bugs cazados. Server commit `0cac57a` firmado
**SIN push** (esperando orden). ⏳ colas: embebido rama for3s termina solo en el server ·
smoke-test de Brian a Foresito por Telegram ("busca en el maestro…") · re-indexar tras pushes.

**👉 PRÓXIMO PASO: Brian marca el foco.** Sobre la mesa:
- 🅰️ nuevo frente de producto (🟡 C multi-canal · F-A2 sub-agentes paralelos de /mision · carriles).
- ⏳ pilotos VIVOS externos: Jazz usa su bot (jazz verificada v0.19.0) + NavigoX retoma consumo.
- Pendientes técnicos menores: **CodeQL rojo desde el 17** (pre-existente) · validar torch 2.13
  (quitar 2 ignores pip-audit) · semillas de diseño H-4 (peso de respuestas propias en ranking) y
  H-6 (presupuesto chars por chunk) — Ronda si Brian quiere.

**🔄 Carriles vivos DORMIDOS** (se despiertan cuando Brian diga): Confianza
(`Doc/Carril_Mejora_Continua_Confianza.md`) · Presencia (`Doc/Carril_Presencia_Descubribilidad.md`)
· Multi-canal (`Doc/Carril_Multicanal.md`) · Maestro (evoluciona a carril).
⚠️ NavigoX vive en `~/5M-incubathon/`, CERRADO — no leerlo sin gate (§6).

## 5-bis · Cerrados grandes recientes (solo punteros — historia en Bitácora Julio)

- 🌐 **SUPER-CEREBRO CONECTADO ✅✅ COMPLETO** (visión `Alma/Vision_Mente_OS_Maestro_Y_Foresito_
  Entrenado.md`): 🅱️ Maestro F1-F5 (repo + comandos + permisos + ramas; evoluciona a carril) +
  🅰️ Foresito entrenado/examinado + 👑 Agente Maestro con puente E (ver §4).
- 🎯 **APRENDIZAJES DE CAMPO (post-Incubathon) — los 5 frentes:** 🔴 A consumo ✅ (regla /clear
  moderada por mí) · 🔵 D ✅ H13 DEVUELVE v0.16.0 · 🟠 B ✅ MERCADO v0.17.0 (panel
  `for3s.vercel.app/for3s-admin`, URL fija, molde, Trace) · 🟣 E ✅ CONFIANZA v0.18.0 (carril
  dormido) · 🟡 C multi-canal PENDIENTE (sin urgencia). Doc madre: `Alma/Aprendizajes_De_Campo_
  Post_Incubathon.md` · detalle `Doc/PENDIENTES.md`.
- Menores abiertos: /decidi RNN-LSTM al bot · `/dmn valor on` fuera de brian · UX (/salud virgen ·
  rate/min · /olvidar "%") — en PENDIENTES.
- **Congelados hasta orden de Brian** (NO empujar): brechas OpenClaw/Hermes (multi-canal, voz,
  cron conversacional, nudges…) · identidades secundarias · descubribilidad (SEO/AEO/GEO).
- **Deuda no urgente:** H9 D1-D8 · H10 HP1-HP6 · §EXTRAS. Lista completa: **`Doc/PENDIENTES.md`**.

## 6 · 🏆 Incubathon (jul 2026) + 🌉 puente a otros Mente OS

- **2º lugar de 200 empresas** con **NavigoX** (marketplace de turismo). **La capa API de For3s fue
  el marco que cerró el pitch.** For3s OS **VALIDADO como infraestructura con demanda real**: 2
  clientes quieren For3s + más gente quiere la infra. Memorias: `project_incubathon_2do_lugar_validacion`
  + `project_hito_hoteleria_navigox`. Cierre completo en `Doc/Bitacora_Progreso.md` (Julio 2026).
- **🌉 NavigoX vive en su PROPIO Mente OS** (`~/5M-incubathon/Mente/`). En ESTE Mente OS está
  **CERRADO** (se registra el hito; su trabajo NO continúa aquí). ⛔ **NUNCA leer `~/5M-incubathon/`
  sin gate.** Abrir: Brian escribe `acceder mente <proyecto>` (ej. `acceder mente navigox`) + por qué
  → solo lectura + reporte. Cerrar: `cerrar mente <proyecto>` o al terminar la tarea. **Motivo:
  evitar que el consumo de tokens se dispare.** Registro/reglas: `Doc/Puentes_Mente_OS.md`.

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
| **TODOS los pendientes a detalle** | `Doc/PENDIENTES.md` |
| **Carril de mejora continua de CONFIANZA (reactivar el Frente E)** | `Doc/Carril_Mejora_Continua_Confianza.md` |
| **Carril PRESENCIA/Descubribilidad (landing+SEO+AEO+analítica, dormido)** | `Doc/Carril_Presencia_Descubribilidad.md` |
| **Carril MULTI-CANAL (Frente C: WhatsApp/correo/análisis, dormido)** | `Doc/Carril_Multicanal.md` |
| **Telemetría de conversaciones (registrar ANTES de cada /clear — regla CLAUDE.md)** | `Cerebro/Registro_Conversaciones.md` |
| Hito ENTRENAMIENTO: reporte de ejecución completo | `Doc/Entrenamiento_Ejecucion_Reporte.md` |
| Hito ENTRENAMIENTO: plan + flujo + radiografías de los 7 agentes | `Cuerpo/Plan_Implementacion_Entrenamiento.md` · `Cuerpo/Flujo_Extraccion_Entrenamiento.md` · `Doc/Radiografia_*` |
| E6 backlog profundo (archivo por archivo) | `Cuerpo/Plan_Backlog_Profundo_E6.md` · `Doc/Entrenamiento_Catalogo_Codigo.md` |
| Diseño arquitectónico maestro (11 nodos + 3 pilares) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| Historia cronológica de cierres (qué pasó cada periodo) | `Doc/Bitacora_Progreso.md` |
| **Puente a otros Mente OS (NavigoX…) — reglas del gate** | `Doc/Puentes_Mente_OS.md` |
| **Snapshot del estado ANTERIOR (RETOMAR viejo íntegro, 84KB)** | `Doc/Estado_Sesion_Snapshot_2026-07-07.md` |
| Estado/reglas/contexto histórico grande (200KB) | `Doc/Estado_Sesion_Continuidad.md` (solo si imprescindible) |
| Multi-instancia (gestor `for3s`, aislamiento) | memoria `project_multi_instancia` |
| Servidor: acceso + specs | memoria `reference_servidor_for3s` |
| Comparaciones de construcción vs Hermes/OpenClaw | `Doc/Comparacion_For3s_OS_vs_Hermes_Construccion.md` · `…vs_OpenClaw_…` |
