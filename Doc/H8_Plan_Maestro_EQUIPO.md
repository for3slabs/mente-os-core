# H8 — "EQUIPO": Plan Maestro de Construcción (Multi-Agente, 5 specialists paralelo)

> **Qué es:** plan de obra de H8, el hito que convierte a For3s de UN agente a un
> EQUIPO de specialists trabajando en paralelo sobre un problema (análisis de PR/repo
> desde varios ángulos QA). Es el **hito más pesado del bloque** (~6-7 días, 18 capas
> defense-in-depth). Materializa el Nodo Multi-Agent Network. Diseño LOCKED: R5 B3.
>
> **Regla:** como H5/H6 — cada sub-paso se EXPLICA, se construye aislado, se VERIFICA,
> se pide OK de Brian, tests, y se avanza de UNO en UNO. NUNCA todo de golpe.

**Fecha de plan:** 2026-06-23 · **Estado:** 📋 PLAN — construcción no iniciada
**Servidor:** `for3s` · **Diseño LOCKED:** R5 Bloque 3 (4 sub-temas, 18 capas)
**Decisión de Brian:** H8 COMPLETO (5 specialists paralelo + 18 capas), no la versión lite.
**Predecesor:** H7 parcial (/model hecho, enrutamiento bloqueado).

---

## §0 — Qué es H8 (la idea)

De un agente solo → a un **equipo hub-and-spoke**:
```
        🧠 HUB (orquestador): analiza la tarea, decide qué specialists
              │ spawn EN PARALELO (asyncio.create_task, cap 5 v1)
   ┌──────────┬────────┬────────┬──────────┐
   🔍Code   🔒Security 🧪Test  ⚡Perf    📝Doc
   Analyzer  Auditor  Generator Analyzer Writer
   └──────────┴── message bus (asyncio.Queue) ──┴─────┘
              │ reportan al HUB
        🧩 SYNTHESIZER: combina los N análisis en 1 reporte
```
DEMO: le pasas un PR → ves los 5 specialists analizándolo a la vez + el synthesizer
combinando → reporte QA completo (qué hace + vulns + tests + perf + docs). Más rápido
y más completo que un solo agente.

---

## §1 — Los 4 sub-temas LOCKED (R5 B3)

| Sub-tema | Qué define |
|---|---|
| **5.3.1 Estructura** | Hub-and-spoke + 5 specialists (code_analyzer, security_auditor, test_generator, performance_analyzer, doc_writer). Cap 5 v1. Híbrido single+multi on-demand. |
| **5.3.2 Lifecycle HARDENED** | `asyncio.create_task` per specialist + **18 capas defense-in-depth** (3 grupos: aislamiento·7, no-bloqueo·5, memoria·6). |
| **5.3.3 Communication** | message bus `asyncio.Queue` (hub_inbox + inbox por specialist) + event broadcast. |
| **5.3.4 Cost Control** | 7 capas de enforcement + budget cap mensual multi-agente. |

---

## §2 — Las 18 capas defense-in-depth (resumen)

**Grupo A — AISLAMIENTO (7 capas):** que un specialist no vea datos de otro/de otro
cliente. ContextVar isolation · tools whitelist runtime · **KEK scoping (master NUNCA
en specialist)** · Postgres Row-Level Security · resource quotas (Semaphore) · mutation
guards (default read-only) · anomaly detection + emergency kill.

**Grupo B — NO BLOQUEO (5 capas):** que un specialist colgado no congele a los demás.
Static check CI · tool protocol async-only · anyio thread pool con CapacityLimiter ·
event loop stall detector · process circuit breaker.

**Grupo C — MEMORIA (6 capas):** que 5 agentes en paralelo no exploten la RAM. Weak
refs · resource bounds declarativos · memory metrics realtime · RSS threshold alert ·
restart preventivo (3 triggers) · leak forensics.

---

## §3 — ⚠️ TENSIONES REALES con el setup actual (honestidad, decididas con Brian)

Brian eligió H8 completo conociendo estas tensiones. Se documentan para no olvidarlas:

1. **Rate-limit ×5:** 5 specialists en paralelo = 5 llamadas LLM simultáneas. El OAuth
   de Brian es Tier 1 (Sonnet 30k/8k tok-min) → topará el 429. **Mitigación:** spawn con
   COLA/espaciado (los 5 existen pero se serializan parcialmente para no topar) + el
   backoff anti-429 ya construido. El "paralelo puro" llega con tier alto/API key.
2. **18 capas vs single-user:** las capas cross-workspace (RLS, KEK por specialist)
   protegen contra FUGA ENTRE CLIENTES, que hoy no existen (single-user). **Decisión:**
   construir las que SÍ aplican a single-user (quotas, timeouts, anomaly kill, memoria,
   tools whitelist) ahora; las cross-workspace PREPARADAS pero inactivas hasta multi-tenant.
3. **Multi-tenant es prerequisito parcial:** el aislamiento real necesita workspaces
   (diferido). Se construye la base; el aislamiento full-cliente se completa con multi-tenant.
4. **Costo ×5:** 5 agentes = 5× consumo. El cost control (5.3.4) + budget cap es OBLIGATORIO
   antes de soltar el spawn — el freno antes que el motor.

---

## §3.4 — DOS FAMILIAS DE SPECIALISTS (visión de Brian, agregada 2026-06-23)

⭐ **HUECO del diseño LOCKED detectado por Brian:** los 5 specialists de R5 B3 son TODOS
de código/QA (Code/Security/Test/Perf/Doc). Pero For3s es SEGUNDO CEREBRO UNIVERSAL
([[project_for3s_segundo_cerebro_scope]]): ayuda con LO QUE SEA, no solo código. Una
persona que NO programa (escribe, investiga, decide, organiza) NO tenía equipo de
specialists. Brian: "¿qué pasa con el resto?". CORRECTO — se expande el diseño.

**SOLUCIÓN (decisión Brian): 2 FAMILIAS de specialists, el Hub elige según la tarea:**

| Familia | Specialists | Para tareas de... |
|---|---|---|
| 🐙 **Técnica/QA** (la del LOCKED) | code_analyzer · security_auditor · test_generator · performance_analyzer · doc_writer | código, repos, PRs, QA |
| 🧠 **General/Conocimiento** (NUEVA) | investigador · escritor · analista · planificador · crítico/revisor | escribir, investigar, decidir, planear, organizar |

**Propuesta de la familia general** (a afinar al construir S1):
- **investigador** — busca/sintetiza información, fuentes, contexto (usa web fetch).
- **escritor** — redacta/mejora textos (correos, docs, propuestas, contenido).
- **analista** — descompone un problema, pros/contras, datos, decisiones.
- **planificador** — estructura planes, pasos, roadmaps, organiza ideas.
- **crítico/revisor** — cuestiona, detecta huecos, mejora (el "abogado del diablo").

**El HUB (S4) decide la familia:** si la tarea es código/repo (URL GitHub, "analiza este
PR") → familia técnica; si es general ("ayúdame a estructurar este plan", "investiga X",
"escribe esta propuesta") → familia general. La detección reusa el `huele_a_github` ya
existente + heurística de intención. Specialists DINÁMICOS (que el equipo define los suyos)
= v2 (diferido, es la capacidad generativa #3 del Grafo).

---

## §3.5 — MULTI-USUARIO POR AGENTE (visión de Brian, agregada 2026-06-23)

⭐ **NUEVO EJE de H8 (decisión de Brian):** hoy 1 For3s OS = 1 persona. En H8, un MISMO
agente For3s lo podrán usar VARIAS personas. OJO: esto es DISTINTO del multi-agente
(specialists = 5 IAs internas). Aquí son **humanos reales** compartiendo un agente.

**Niveles:**
- **Solo (1 persona):** como hoy. Sin cambios.
- **Dúo (2 personas):** **mismos privilegios** entre sí (iguales, sin jerarquía).
- **Equipo (5-10 personas):** existen **ROLES** + un **ENCARGADO** (admin/líder).

**Memoria = HÍBRIDA (decisión Brian):**
- **Común del equipo:** lo que se trabaja en el espacio compartido lo ven todos
  (análisis de repos, decisiones, historial común) → For3s como "segundo cerebro DEL EQUIPO".
- **Privada por persona:** cada quien puede tener notas/hilos privados que solo ve él
  (+ quizá el encargado). Combina cerebro común + privacidad individual.

**El ENCARGADO (admin) — decisión Brian:**
- Gestiona accesos: **añade/quita** personas del equipo, **define roles**.
- **Aprueba acciones sensibles**: escribir en GitHub, borrar, etc. (los miembros las
  PROPONEN, el encargado las confirma). Modelo admin/miembro clásico.

**⭐ CONTROL DE ACCESO = modelo "PUERTA" (decisión Brian 2026-06-23, gran UX):**
`/invitar` NO pide user_ids (mala UX, la gente no sabe qué es eso). Es un INTERRUPTOR
de puerta:
- 🟢 **Puerta ABIERTA** (`/invitar` activa): cualquiera que le escriba al bot ENTRA al
  equipo y queda registrado como miembro.
- 🔴 **Puerta CERRADA** (default + `/invitar` desactiva): nadie nuevo entra; solo usan el
  bot los que YA están dentro (dueño + miembros registrados).
- Flujo: encargado abre puerta → las personas escriben al bot y entran → encargado cierra
  puerta → equipo fijo. Cero fricción técnica (nadie maneja user_ids), mantiene fail-closed.
- ⏳ **SACAR a alguien del grupo / denegar acceso = se diseña MÁS ADELANTE** (es un agente
  colaborativo; esa parte —kick/ban— se define después, Brian 2026-06-23).

⚠️ **NOTA ARQUITECTÓNICA:** esto es, en el diseño LOCKED, parte de **multi-tenant +
identidad/RBAC** (R7 B3, estaba diferido a ~H13). Brian decidió ADELANTAR una parte a H8
porque el aislamiento multi-agente (las 18 capas) y el multi-usuario se tocan: ambos
necesitan saber "quién es quién" y "qué puede ver/hacer cada quien". Se construye la
FOUNDATION del multi-usuario en H8; el multi-tenant completo (multi-empresa, billing por
workspace) sigue siendo posterior. Hoy For3s ya tiene piezas base: `OwnerStore` (dueño),
`identities`/`identity_credentials` (R7 B3, para auth), audit namespaced. Falta: el
concepto de EQUIPO (varios usuarios en un espacio) + roles + permisos por rol + memoria
con scope (común/privado) + el gate de aprobación del encargado.

**Relación con las 18 capas:** el aislamiento por-usuario (quién ve qué memoria) reusa
la misma maquinaria de aislamiento de los specialists (ContextVar, RLS, scoping). Por eso
encaja en H8 y no rompe el orden — es la misma "defensa en profundidad" aplicada a humanos.

---

## §4 — SUB-PASOS propuestos (orden, foundation-first)

> Cada uno: explicar → construir aislado → verificar → OK Brian → tests → auditar.

- **S0** Backup pre-H8 (dump verificado + snapshot código). Punto de retorno.
- **S1** Definir los specialists de las DOS FAMILIAS (§3.4): técnica (5: code/security/
  test/perf/doc) + general (5: investigador/escritor/analista/planificador/crítico).
  Cada uno = SpecialistDefinition (nombre, familia, system_prompt, tools permitidas,
  límites). Aislado, SIN spawn aún. Verificar el catálogo completo.
- **S2** UN specialist end-to-end (ej. security_auditor): que analice un input y devuelva
  su parte, con sus límites (timeout, token budget). Prueba de concepto del rate-limit.
- **S3** Message bus (asyncio.Queue: hub_inbox + inbox por specialist). Verificar comunicación.
- **S4** Hub orquestador: decide la FAMILIA (técnica vs general, §3.4) + qué specialists +
  los spawn (con COLA anti-429) + recoge reportes.
- **S5** Synthesizer: combina los N reportes en 1 respuesta coherente.
- **S6** Capas de NO-BLOQUEO (timeouts, circuit breaker, stall detector) — que un colgado no tumbe.
- **S7** Capas de MEMORIA (quotas, RSS alert, restart preventivo) — que 5 no exploten RAM.
- **S8** Cost control 7 capas + budget cap (el freno) — ANTES de soltar el paralelo real.
- **S9** Capas de AISLAMIENTO single-user (ContextVar, tools whitelist, KEK scoping, anomaly kill).
- **S10** Capas cross-workspace (RLS, etc.) PREPARADAS pero inactivas (multi-tenant futuro).

  --- MULTI-USUARIO (§3.5, reusa el aislamiento de arriba) ---
- **S10a** Concepto de EQUIPO: tabla(s) para un espacio compartido con varios usuarios
  (equipo + miembros + rol de cada uno). Hoy solo hay OwnerStore single-owner → extender.
- **S10b** ROLES + permisos: encargado(admin) vs miembro. El encargado añade/quita personas
  y define roles. Permisos por rol (quién puede qué).
- **S10c** MEMORIA con scope (híbrida): memoria COMÚN del equipo (todos ven) + PRIVADA por
  persona (solo el dueño + encargado). Reusa el scoping/aislamiento de las capas.
- **S10d** GATE de aprobación del encargado: acciones sensibles (write GitHub, borrar) que
  un miembro PROPONE → el encargado CONFIRMA. Reusa el flujo de confirmación por botón ya hecho.
- **S10e** Dúo: caso de 2 personas con mismos privilegios (sin jerarquía) — verificar que
  funciona como caso simple del modelo de equipo.

  --- cierre ---
- **S11** Integración al bot: comando/flujo para disparar el análisis multi-agente de un PR
  + comandos de equipo (invitar, ver roles) para el encargado.
- **S12** Prueba E2E real (un PR → los 5 specialists → synthesizer) + prueba multi-usuario
  (equipo con encargado + miembro, memoria común/privada, gate de aprobación) + auditoría + docs.

---

## §5 — Estado de los sub-pasos

| # | Sub-paso | Estado |
|---|---|---|
| 0-12 | (ver §4) | ⬜ pendientes — empezar por S0 |

---

**Regla permanente H8:** el FRENO (cost control + aislamiento + no-bloqueo) se construye
ANTES de soltar el spawn paralelo real. 5 agentes sin frenos = riesgo de runaway de costo,
fuga de datos, o RAM explotada. Foundation-first, como todo For3s.