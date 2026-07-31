# H10-H12 "APRENDE" — Plan Maestro (skills auto-generables)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/H10-H12_Plan_Maestro_APRENDE.md → memory/archive/H10-H12_Plan_Maestro_APRENDE.md (2026-07-30, ADR-029)

> Fase B (diseño, Brian 2026-06-24): plan de obra para que For3s cree, gobierne y
> mejore sus propias skills — la "joya" de Hermes, adaptada a CÓDIGO PROPIO de For3s.
> Basado en el análisis del learning loop de Hermes (`docs/analysis/Analisis_LearningLoop_Hermes_para_For3s.md`)
> + el diseño LOCKED R6 (Meta-Orchestrator). NO es código — es el orden de construcción.
> Se ejecuta DESPUÉS de pulir + Bloque 3 (decisión Brian: es lo más grande).

---

## 0. Decisiones LOCKED (Brian 2026-06-24)

| Decisión | Elección |
|---|---|
| Qué es una skill | **SKILL.md + scripts** (receta markdown que el agente aplica con sus tools; portable, agentskills.io-compatible). NO código arbitrario auto-ejecutado. |
| Cómo se crea | **/aprende manual + auto-mejora silenciosa en background** (con governor) |
| Governor (freno) | **Meta-Orchestrator R6 COMPLETO** (6 frenos + kill switch + budget + rollback) |
| Lifecycle | **Curación nocturna reusando H6** (CLS/Microglía: active→stale→archivada, recuperable) |

⚠️ **REGLA LOCKED (R6, Grafo §8.4): el GOVERNOR (H11) DEBE existir ANTES del MOTOR (H12).**
Orden sagrado: H10 → H11 → H12. Hermes lo confirma (su skills_guard es el freno).

## 0.1 Lo que se REUSA (no construir de cero, ~60% del patrón)

| Componente del learning loop | Infra existente de For3s |
|---|---|
| Curación nocturna de skills | **H6 CLS/Microglía** (worker Arq, job nocturno, soft-delete recuperable) |
| Fork aislado para auto-mejora | **H8 specialists** (correr aislado + whitelist + mutation guard) |
| Provenance (auto vs usuario) | **H8 S9 `_ctx_specialist`** (ContextVar de aislamiento) |
| Gate de aprobación | **H8 gate** (miembro propone → encargado aprueba, ya con ejecución real E) |
| Cifrado/audit de lo generado | **KEK + audit chain** existentes |

---

## H10 — SKILLS BÁSICAS ✅ HECHO 2026-06-24

**Meta:** For3s puede TENER y USAR skills (recetas). Cimiento. CONSTRUIDO:
- **H10-a ✅** migración 019 tabla `skills` (DB-backed: nombre/categoria/descripcion/contenido
  SKILL.md/tags/version + lifecycle active|stale|archived + provenance usuario|auto + pinned +
  creada_por + veces_usada/ultimo_uso). Pensada para todo el hito (no re-migrar).
- **H10-b ✅** `skills.py` SkillStore: crear (idempotente upsert) / listar (metadata, carga
  progresiva) / ver (contenido completo) / registrar_uso / buscar_relevantes (match por
  palabras, anti-falso-positivo) + normalizar_nombre. Verificado 9/9.
- **H10-c ✅** el agente USA skills: conversation.py inyecta el SKILL.md de la(s) skill(s) que
  APLICAN al mensaje (match automático, carga progresiva máx 2×1500 chars) + registra uso.
  Defensivo. Mismo patrón que perfil/memoria/grafo.
- **H10-d ✅** comando `/skills` (lista con 👤/🤖 provenance) + `/skills <nombre>` (ver completa)
  en _MENU_BASICO. La CREACIÓN se difiere a H12 (/aprende).
- Estado: BD v19, 132 tests, bot activo. ⚠️ NADA se auto-genera aún (correcto, eso es H12).

---
### (diseño original H10 ⬇️)

**Meta:** For3s puede TENER y USAR skills (recetas), creadas/editadas a mano. Cimiento.

- **Estructura:** `skills/<categoria>/<nombre>/SKILL.md` (+ `scripts/`, `references/`).
  Frontmatter: name, description (≤una línea), version, tags. Compatible agentskills.io.
- **Tool `skill_manage`** (crear/listar/ver/editar SKILL.md + write_file de scripts).
- **Carga progresiva:** metadata en `skills_list`; instrucciones completas vía `skill_view`
  solo cuando se necesitan (no inflar contexto — disciplina AI6).
- **El agente las USA:** detecta cuándo una skill aplica → la carga → sigue sus pasos con
  sus tools (read_file, terminal, etc.). Comando `/skills` (listar) + `/<skill>` (invocar).
- **BD:** migración para tabla de skills (registro + lifecycle state + provenance + uso).
- **Demo H10:** crear una skill a mano, el agente la lista y la aplica en una tarea real.
- ⚠️ NADA se auto-genera aún. Solo almacenamiento + uso.

## H11 — GOVERNOR (el FRENO — Meta-Orchestrator R6) ✅ HECHO 2026-06-25

**Meta:** ANTES de permitir auto-generación, existe el control. Sin esto, H12 NO arranca.
CONSTRUIDO (debate→decidir→código→testeo). Decisiones LOCKED Brian 2026-06-25:
**scanner + 3 frenos reales + hooks honestos · scanner muy conservador (bloquea+avisa) ·
kill switch SOLO del dueño vía /autogen.** Fiel a R6 §A.6 ("envuelve, no reescribe").

- **H11-a ✅** migración 020: `governor_estado` (kill switch persistido, default auto-gen
  APAGADA) + `governor_bloqueos` (append-only, auditoría de todo rechazo). BD v20.
- **H11-b ✅** `governor.py` — `SkillEcosystemGovernor` + `escanear()` + `Veredicto` +
  `EcosystemHealth`:
  - **SCANNER (corazón)**: ~17 regex anti-patrones (rm -rf, mkfs/dd, fork bomb,
    DROP/TRUNCATE, curl|sh, eval(descargado), KEK/secret_store, .env/id_rsa,
    ANTHROPIC_TOKEN/DATABASE_URL, exfiltración env por red, cron/@reboot/bashrc,
    reverse shell, prompt-injection es+en, extraer system prompt). **FAIL-CLOSED**:
    ante error, BLOQUEA. Reporta TODOS los hallazgos.
  - **FRENO 1** `can_generate()` (kill switch + ≤3 auto/día) · **FRENO 4**
    `check_contradictions()` (no duplicar cat+nombre activa) · **FRENO 5**
    `active_budget_ok()` (≤100 activas).
  - **HOOKS H12** honestos (neutros hoy, documentados): FRENO 2 `should_explore`,
    FRENO 3 `no_go_budget_ok`, FRENO 6 `independent_eval` (requieren scoring/NO-GO/sandbox).
  - **KILL SWITCH**: `autogen_permitida()`/`set_autogen()` en BD + flag de emergencia
    `FOR3S_AUTOGEN_OFF` (si está, manda y apaga). Default APAGADA, fail-closed.
  - **PROVENANCE**: el governor SOLO aplica frenos de auto-gen a skills `auto`; las
    `usuario` son intocables (solo scanner + duplicado). Reusa columna de migración 019.
  - **GATE único** `evaluar_skill_nueva()`: scanner→(si auto: freno1+freno5)→duplicado,
    cada rechazo auditado. `health_report()` → HEALTHY|THROTTLED|FROZEN.
- **H11-c ✅** test BD real **24/24** (scanner 9 casos, kill switch, gate usuario/auto,
  duplicado, techo diario, provenance, hooks, auditoría, health). Sin RuntimeWarning.
- **H11-d ✅** comando `/autogen on|off|status` (solo dueño) en menú admin. `status` =
  reporte de salud sin tokens LLM. Bot reiniciado y activo.
- ⚠️ NADA se auto-genera aún (correcto, eso es H12). H11 solo instala el freno.

---
### (diseño original H11 ⬇️)

Reusa el diseño LOCKED R6 (Ronda_06_Pre_Code_Review_Detailed.md §A). Componentes:
- **6 frenos** (calibración muy conservadora v1): p.ej. límite de skills nuevas/día,
  presupuesto de tokens de auto-gen, no-tocar skills del usuario, no-duplicar, etc.
- **SCANNER de seguridad** (estilo Hermes skills_guard): regex anti-patrones (comandos
  destructivos, exfiltración, prompt-injection, persistencia) + trust level. Toda skill
  nueva pasa por aquí. Community/auto = más estricto.
- **PROVENANCE** (ContextVar, reusa H8 S9): marca skill como "auto-generada" vs "del usuario".
  El curator/governor SOLO gestiona las auto-generadas; las del usuario son intocables.
- **KILL SWITCH:** apagar la auto-generación entera con un flag/comando.
- **Failure modes (R6):** re-plan + rollback si una auto-gen sale mal.
- **Aprobación:** lo auto-generado en background → GATE al dueño (reusa H8 gate) antes de
  activarse. Lo /aprende manual del dueño → directo (él lo pidió).
- **Demo H11:** intentar crear una skill peligrosa → el scanner la bloquea; una auto-gen →
  pide aprobación; kill switch apaga todo.

## H12 — MOTOR DE AUTO-GENERACIÓN (/aprende + auto-mejora) ✅ HECHO 2026-06-25

**Meta:** For3s crea y mejora skills solo. SOLO tras H11 (el freno ya existe). CONSTRUIDO
en 3 piezas (debate→decidir→código→testeo, una a una). Decisiones LOCKED Brian 2026-06-25:
**P1→P2→P3 por riesgo · fuente = la conversación actual · P2 construida pero tras el kill
switch OFF.** Nuevo módulo `aprende.py` (motor) — NO toca skills.py (almacén) ni governor.py (freno).

- **P1 ✅ `/aprende [foco]` manual** — `aprender_de_conversacion()`: toma los últimos 12
  turnos del hilo (memory.load_history) → prompt OAuth-safe (system="") que pide al PROPIO
  For3s destilar un SKILL.md en JSON (vale/nombre/categoria/descripcion/tags/contenido) →
  `_extraer_json` tolerante (fences) → **governor.evaluar_skill_nueva(provenance='usuario')**
  → SkillStore.crear. El scanner SIEMPRE corre (una charla puede tener un secreto). Comando
  `/aprende` en menú básico (para todos, también miembros). Test LLM real **10/10**: destiló
  'deploy-bot-for3s-server' con pasos; ante fuente maliciosa NO guardó nada (LLM rehusó +
  scanner como 2ª capa).
- **P2 ✅ auto-mejora en background** — `proponer_skill_auto()` (provenance='auto'): freno
  duro de entrada `can_generate()` → si /autogen OFF, **ni llama al LLM** (ahorro + kill
  switch real). Si pasa, la skill NACE en `stale` (no se inyecta al chat) y va al **GATE del
  dueño**: aviso con botones ✅ Activar / ❌ Descartar (`on_skill_gate`, patrón H8).
  `aprobar_skill` stale→active · `rechazar_skill` stale→archived (recuperable). Disparador:
  tras una corrida de equipo (señal de tarea compleja) → `_auto_mejora_background` en
  asyncio.create_task (no bloquea la respuesta). Test **10/10** (FakeProvider): OFF no llama
  al LLM · ON propone en stale · aprobar/rechazar correctos. Hoy inerte (autogen OFF default).
- **P3 ✅ curación nocturna** (reusa H6) — `curar_skills()` + job Arq `job_curar_skills`
  (03:30 México, DESPUÉS de Microglía). Skills AUTO sin uso (veces_usada=0, ultimo_uso NULL):
  active→stale a los 30d, stale→archived a los 90d, por antigüedad de actualizada_at
  (recuperable, nunca hard-delete). **Intocables**: usuario, pinned, usadas, y las propuestas
  recientes del gate (no caen en el corte). DRY-RUN disponible. Test **8/8**. Worker reiniciado
  (6 jobs, 5 crons). Es el "curator" de Hermes.
- Estado: BD v20, **version.py v1.0.0** (HITO "H12 APRENDE"), bot + worker activos. ⚠️ La
  auto-generación sigue APAGADA por defecto (kill switch OFF) — H12 da la capacidad, el dueño
  decide cuándo encenderla con `/autogen on`.

---
### (diseño original H12 ⬇️)

**Meta:** For3s crea y mejora skills solo. SOLO tras H11 (el freno ya existe).

- **`/aprende <fuente>`** (estilo Hermes /learn, lo más simple/elegante): NO un motor
  separado — construye un PROMPT que instruye al PROPIO For3s a (1) juntar la fuente
  (la conversación actual / un repo / una URL, con sus tools) y (2) escribir un SKILL.md
  vía `skill_manage`. Pasa por el governor (H11) antes de guardar.
- **Auto-mejora en background** (reusa H8 fork + H6 nocturno): tras tareas complejas, un
  fork aislado se pregunta "¿vale guardar/mejorar una skill de esto?" → crea/parcha en
  background → governor + gate al dueño. NUNCA toca la conversación principal ni el cache.
- **Curación nocturna** (reusa H6): de noche, skills auto-creadas sin uso → active→stale
  (30d)→archivada (90d), recuperable; pinned/del-usuario intocables. Es el `curator` de Hermes.
- **Demo H12:** hacer un flujo con For3s → /aprende → genera una skill reutilizable; usarla
  después; de noche el sistema cura las que no se usan.

---

## Orden de construcción + esfuerzo

```
H10 (cimiento: skill_manage + uso)  →  H11 (GOVERNOR, el freno — NO saltar)  →  H12 (motor)
   mediano                              grande (R6 completo)                     mediano (reusa H6+H8)
```

- **NO partimos de cero:** ~60% del patrón ya existe (H6+H8+ContextVar+gate+audit).
- **Lo más grande:** H11 (Meta-Orchestrator R6 completo — 6 frenos + kill + rollback).
- **Lo más delicado:** que el agente escriba/aplique recetas propias → por eso H11 primero.
- **Cuándo:** después de pulir lo actual + Bloque 3 (producto). Hoy = plan listo, no construir.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Agente genera skill dañina | Scanner (H11) + gate del dueño + skills son recetas, no código auto-ejecutado |
| Acumulación de skills basura | Curación nocturna (H6) archiva sin uso |
| Auto-gen se desboca (costo) | 6 frenos R6 + budget + kill switch (H11) |
| Toca skills del usuario | Provenance (ContextVar): solo gestiona las auto-generadas |

## Veredicto

H10-H12 es la "joya" de Hermes adaptada a For3s, y **el diseño R6 de For3s ya lo anticipaba**.
Construible cuando toque, sobre la infra existente. El reporte de análisis valida la ruta.

> Refs: Analisis_LearningLoop_Hermes_para_For3s.md · Ronda_06_Pre_Code_Review_Detailed.md (R6) ·
> Ronda_05_DMN (auto-improvement). Hermes (Nous) = referencia analizada, no copiada.
