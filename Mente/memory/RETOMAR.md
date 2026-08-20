# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-18 · **Owner:** brian
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

## 2 · Servidor `for3s` — 3 FOR3S OS al mismo tiempo

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 · **cómo entrar: `secrets/Conectar_Servidor_For3s.md`**
· gestor `for3s listar|agregar|entrar|encender|apagar|borrar`. Aislamiento TOTAL por
`docker compose -p for3s-<nombre>`. Comparten SOLO: máquina + imagen + suscripción Claude
(**1 solo cupo**). ⭐ **El código del producto vive en `~/for3s-os`** en el servidor — esa es la
FUENTE. Tiene **2 remotos, a propósito**: `origin` → `for3slabs/for3s-os` (el taller) y `backup` →
`for3slabs/for3s` (el respaldo del producto verificado). ⛔ **Se empuja a los DOS**; a uno solo
los deja divergentes. Medido en el servidor 2026-08-19, no leído de un documento.

| Bot | Instancia | Estado |
|---|---|---|
| 🏢 @For3s_OS_bot | `for3s` | 🟢 "Foresito" — EMPRESA, microglía ON |
| 👤 @For3s_Brian_bot | `brian` | 🟢 PERSONAL — **ENTRENADO** (§4) · ⭐ **la que se trabaja** |
| 🌐 @For3s_General_bot | `general` | 🟢 PÚBLICO, puerta ABIERTA |

🔴 **`jazz` y `mashe` NO EXISTEN — Brian las borró el 2026-08-06** (*"son ruido y no se han
ocupado"*, `blocks/active/demo` §G). Esta tabla las siguió listando 4 días y **la IA repitió el
dato como si fuera cierto**: un número copiado a mano es correcto exactamente una vez.
📏 **Verificado en el servidor 2026-08-10:** `for3s listar` devuelve 2 encendidas + Foresito.

## 3 · Estado global del producto

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.20.0 CONECTORES SELF-SERVICE · schema BD v47.**
13 hitos H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad
Hermes (5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + super-cerebro (§4).
**Cero bugs abiertos.**

- **✅ TRÍADA SINCRONIZADA** — ⭐ **re-medida y RESTAURADA el 2026-08-19**: server = `origin`
  (`for3slabs/for3s-os`) = `backup` (`for3slabs/for3s`), los tres en **`732c434`**.
  ⚠️ **Estuvo ROTA 24 días y este archivo no se enteró:** declaraba `f50a5db` (19-jul) mientras el
  servidor tenía 2 commits firmados sin empujar (23 y 26-jul). Un HEAD escrito a mano es correcto
  exactamente una vez — se lee con `git rev-parse`, no de aquí.
- **✅ SEGURIDAD CERRADA** (16-jul): CI verde · SEC-3/4/5/6 + 3b/4b · token rotado · **SEC-4c**
  non-root por instancia. 🔒 **nunca `chown -R` un bind mount** (`feedback_nunca_chown_bind_mount`).

## 4 · 🎓🎓 SUPER-CEREBRO — ambos agentes entrenados+examinados ✅ (18/20-jul)

**brian 🍓** 22,406 eps · examen **94.3%**. **Foresito 👑** 1,829 eps · grafo 2,687 nodos · examen
**98.8%** · es el **AGENTE MAESTRO** (lee `for3slabs/mente-os-maestro` EN VIVO). Los exámenes
cazaron **12 hallazgos con fix sistémico** (H-11: la contraseña del server vivía en 60 eps →
redactada). 👉 `project_entrenamiento_foresito` · `work/Entrenamiento_Ejecucion_Reporte.md`.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

### 📕 LA VERDAD DE V1 — sabemos qué es For3s OS, medido (2026-08-12, S13)

**50 auditorías al servidor + ~45,000 líneas de Mente OS leídas** (el 100% de lo que gobierna,
decide o registra). Nacen 3 documentos en `campaigns/producto-for3s-os/` — **4,715 líneas**:
📕 `campaigns/producto-for3s-os/terreno/LA-VERDAD-DE-V1.md` (**entrar por aquí**) · `campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` (el código) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-MENTE-OS-CONOCIMIENTO.md` (el conocimiento, 33 §).

> ⭐⭐⭐ **EL VEREDICTO:** For3s OS **no está roto ni abandonado**. Está en la **Fase 1-3 de un
> plan de 6**, pasa **6/6** el gate de su fase, tiene **13 de 16 hitos**, y **va adelantado**:
> ~2 meses de código contra 6-7 estimados.

⭐⭐ **LA VARA DE LA CAMPAÑA, resuelta por medición:** ni el Grafo ni el código — **el GATE DE LA
FASE EN CURSO** (`memory/archive/Plan_Maestro_Programacion.md`). Contra el Grafo completo faltan
**15 de 15 tablas** (rojo inútil); contra el gate: **6/6**, y los 24 hallazgos **se reducen a 4**.

**Los 4 que importan, en los 4 primeros bloques:** 🔴 **H-01** contenido EN CLARO (`seguridad`,
y viola la anti-visión #9 *no-negociable*) · 🟠 **H-02** la búsqueda cruza sesiones y el contador
no → **podría borrar lo que sí usa** (`memoria`) · 🔴 **H-04** digest muerto 29d, el worker está
apagado 8h/día (`cerebro`) · 🔴 **H-03** instancia huérfana, 933 MB (`despliegue`).

🔴 **Los 2 nodos ausentes:** Amígdala (7) y Tálamo (8) — confirmados por 5 métodos independientes.
⭐ **Lo que superó al estado del arte:** la microglía — **41% podado** con audit de cada olvido.

🆕 **El airlock** (`rule-pr-batching` §5): 3 niveles de revisión. **El agente ya no para en cada
PR** — nivel 1 sigue solo; el merge sigue siendo humano en los tres.

✅ **HECHO (13/14-ago):** el plan de las 3 fases (`docs/plans/PLAN-3-fases.md`) · la vara temporal
en `rules/rule-product-authority.md` §2 · el campo `campaign_phase:` en `rules/contract-block.md` · su
validador en `bin/check-campaigns` (4 comprobaciones, verificado por sabotaje) · el **DOSSIER para
el consultor** (`vision/DOSSIER-SISTEMA-COMPLETO-2026-08.md`, 1,016 líneas).

🆕 **BLOQUE 1 DE 12 · `seguridad` — VA 6/11** (18-ago). ⛔ **NO está cerrado.**
✅ **La mitad que MIDE, completa (6/6):** Fase 1 cerrada con veredicto por dimensión en
`campaigns/producto-for3s-os/hallazgos/seguridad-fase-1.md` — **5 de 6 en 🟢**.
⭐⭐ **La frase del bloque: la seguridad está bien CONSTRUIDA y mal CABLEADA.** `crypto.py` está
bien hecho, la master key custodiada (32 B, `600`, fuera del repo), la cadena de auditoría
verificada eslabón a eslabón (12,963 + sabotaje) y el sandbox resistió 5 ataques. **Lo que falla
es que el contenido nunca pasa por la cripto.**
⬜ **La mitad que ARREGLA, sin empezar (0/5):** SB-7 capa `contenido.py` → SB-8 los 2 escritores →
SB-9 los 9 lectores → SB-10 migrar 15 MB. ⭐ **El orden NO es negociable:** SB-9 antes que SB-10, o
el sistema queda leyendo cifrado con código que espera texto plano.
✅ **Rollback PROBADO:** dump 131 MB restaurado → 33,908 filas (BD desechable, eliminada).

🔴 **EL PATRÓN QUE APARECIÓ 3 VECES — el hallazgo más importante de la semana:**
| Caso | La pieza existe | Y nadie pasa por ella |
|---|---|---|
| H-01 | `crypto.py` funciona | el contenido no se cifra |
| workspaces | `derive_workspace_key()` funciona | hay **1 solo** |
| **BYOK** (18-ago) | **`LLMProvider(ABC)` existe** | **12 archivos instancian `ClaudeProvider` directo** |
⭐ *"Se construye la pieza y no se conecta."* **Tres veces ya no es un cable suelto: es cómo se ha
venido trabajando.** ⚠️ Y el 3º **bloquea una venta**: sin eso, un cliente no puede poner su propio
LLM y el cupo de suscripción (uno solo, compartido por 3 instancias) es un techo duro.

🆕 **SB-3 DERRIBÓ UNA PREMISA MÍA:** afirmé 3 veces que H-01 crecía a diario. **Falso** — 99.5% es
importado (ene-may), lo vivo son 81 kB y lleva 16 días parado. H-01 **no gana por urgencia, gana
por gravedad**. ⭐ La Fase 1 existe para eso: si el arreglo hubiera ido antes, habríamos cifrado
con la urgencia equivocada.

⭐ **Reparto del territorio = opción A** (un archivo, un dueño): el `hooks/pre-edit-standards.py` se
queda con **el primer** bloque que reclama un archivo, así que dos dueños dan la vara equivocada.

🆕 **S15 · LA JORNADA DEL CANDADO (18-ago) — motor, no producto.** El bloque `seguridad` **sigue
en 6/11**: SB-7 no se empezó. Lo que sí cambió es que el sistema ya no pierde trabajo en silencio:

- ⛔ **LA BASE DE UN PR ES `master`, SIEMPRE** — `bin/check-pr-base` lo RECHAZA si no lo es, y la
  excepción *"unless explicitly stacked"* del anti-patrón #8 quedó **ANULADA**. Regla:
  `rules/rule-pr-base.md` (3ª hermana). 🔴 **Nació de un daño real ese día:** encadené el PR #33
  sobre una rama con PR abierto, el squash rompió el parentesco y **329 líneas quedaron fuera de
  `master` con la etiqueta MERGED puesta**. ⭐ Verificar un merge **por CONTENIDO, nunca por la
  etiqueta** — así se descubrió.
- ✅ **El falso `session open` está muerto** — medía el `.jsonl` más nuevo por mtime, que tras un
  `/clear` es el ANTERIOR. Ahora resuelve por `session_id`.
- ✅ **Un clon del motor vuelve a pasar su batería** (18 fallos → 0). ⚠️ **Un clon necesita
  `bin/init`**: `CLAUDE.md`, `PROJECT-RULES.md` y `WORKSPACE.md` se GENERAN, no viajan.
- ⚠️ **Las horas de `Registro_Conversaciones.md` van en LOCAL (CST), nunca en UTC** — 6 filas
  las tenían mal; ya hay validador.

### LO ANTERIOR (en `memory/Bitacora_Progreso.md`)

El ciclo de 12 etapas · el clon que verifica el motor · los 111 pendientes rotados · el bloque
MOTOR 9/11. **Todo cerrado y archivado** — se consulta, no bloquea.

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
| **TODOS los pendientes a detalle** | 🗓️ `memory/pendiente-<mes>-<año>.md` (rota mensual) · `memory/PENDIENTES.md` = histórico congelado |
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
