# 🎓 HITO ENTRENAMIENTO — REPORTE MAESTRO DE EJECUCIÓN (2026-07-04 → 07-05)

> **Qué es este doc:** el registro COMPLETO de cómo se ejecutó el hito ENTRENAMIENTO
> (6 agentes OpenClaw → 1 For3s OS), con resultados REALES, bugs cazados y estado final.
> **Diseño previo:** `Cuerpo/Plan_Implementacion_Entrenamiento.md` (etapas) ·
> `Cuerpo/Flujo_Extraccion_Entrenamiento.md` (el tubo FE0-FE8) ·
> `Cuerpo/Ronda_Entrenamiento_Plan_Maestro.md` (F0) · radiografías (censo).
> **Destino:** @For3s_Brian_bot (instancia `brian` — el For3s OS PERSONAL de Brian).

---

## 0 · Los DOS AGENTES (contexto previo al hito, mismo día)

Antes de entrenar se creó el **segundo For3s OS del server** (prueba de fuego REAL del
sistema MULTI-INSTANCIA): **Foresito** (`@For3s_OS_bot`, proyecto docker `for3s`, agente
de la EMPRESA) y **brian** (`@For3s_Brian_bot`, proyecto `for3s-brian`, PERSONAL, recibe
el entrenamiento). Misma imagen v0.15.0, aislamiento total (red/BD/volúmenes/KEK), misma
suscripción Claude (cupo compartido). **4 bugs de producto cazados al crearlo:**
1. Plantilla `docker-compose.instancia.yml` ATRÁS de la última versión (sin volúmenes
   persona/mods de Identidad Viva) → paridad aplicada (53f520a).
2. Gestor `for3s` sin modo no-interactivo → flags `--token/--owner/--claude` + fix del
   dispatch que se comía los flags.
3. **BUG instalación fresca:** el primer mensaje del dueño reventaba con FK
   `fk_episodes_persona` (el camino `sync_con_bd` que migra el owner JSON→BD no sembraba
   `personas`) → fix 842b6d1. Le pasaba a TODO tester con owner preconfigurado.
4. Flags OPT-IN (estilo/perfil/microglía) NO llegaban a los contenedores (los composes no
   los pasaban) → passthrough ff11ee9. De paso: **la microglía de FORESITO llevaba en
   SIMULACRO desde la contenedorización** (confirmar=False silencioso) → restaurada.

brian quedó a **máximo potencial**: `FOR3S_ESTILO_INFER=on` + `FOR3S_PERFIL_INFER=on` +
`/autogen on` + `/dmn generativas on` (Brian los activó por Telegram) · microglía OFF a
propósito hasta terminar la digestión · GitHub sin PAT (opcional, pendiente).

---

## 1 · RESUMEN EJECUTIVO — qué quedó dentro de @For3s_Brian_bot

| Qué | Cuánto | Dónde |
|---|---|---|
| Episodios (memoria episódica) | **31,576** con fecha ORIGEN real (2026-01-29 → 05-30) | `episodes_events` (channel='import', sesiones `oc:*`, lote reversible) |
| Embeddings | **100%** (BGE local, $0) | columna `embedding` |
| Conceptos del grafo | **669** (49% digerido; la cola sigue de noche) | AGE `for3s_kg` |
| Skills VIVAS | **15** con matcher semántico | tabla `skills`, categoria=openclaw |
| Secretos | **38 únicos cifrados** (67 detectados, 29 dups) | vault `secrets` (KEK de brian) |
| Identidad | Fruterito ADAPTADO (gate de Brian) | `persona/IDENTITY.md` + `REGLAS_USUARIO.md` |
| Perfil | prefs de Brian + Jazz Criptec | perfil P1 |
| Manifiesto | **11,664/11,664 decididos — 0 pendientes** | `import_manifiesto` |

**Decisión rectora (Brian):** extracción por **LÍNEA DE TIEMPO GLOBAL** (lo más antiguo →
lo más actual, TODAS las fuentes mezcladas). Validada por el hallazgo de que los agentes
OpenClaw fueron CONTEMPORÁNEOS (importar por-agente rompería la causalidad).

## 2 · LAS ETAPAS EJECUTADAS (commits firmados, server, SIN push)

- **E0 infra (866b00c):** migr 033 (`import_manifiesto` + `import_lotes` + col
  `episodes_events.import_lote`) · módulo `entrenamiento.py` (lotes reversibles,
  transacción única, `created_at`=fecha ORIGEN, dry-run default) · backup pre-entrenamiento
  con RESTORE verificado (31 tablas) · **REVERSA DEMOSTRADA en vacío** — y cazó su 1er bug
  ANTES del material real (FK episodes→sessions: el importador upserta la sesión origen).
- **E1 censo (cc12697):** `entrenamiento_censo.py` — walker de las 2 raíces → 11,664
  archivos con hash/bloque(B1-B7|SECRETO)/fecha_ini-fin/duplicado_de. **Hallazgos:** wsl =
  ESPEJO del principal (6,600 dups exactos; el "mar de 734 docs del Empleado" = 5 únicos) ·
  67 secretos por ruta (20 MÁS que el censo manual) + 81 con secretos embebidos · línea de
  tiempo ene→may → 5 olas. Generó `Doc/Radiografia_Fruterito_WSL.md`.
- **E2 secretos+identidad (fe5374a):** `entrenamiento_secretos.py` — 38 únicos al vault
  (nombres canónicos `oc.<agente>.<qué>`, descifrado VERIFICADO). ⚠️ **LECCIÓN KEK:** el
  1er intento cifró con una KEK generada al vuelo (el docker run efímero no montaba
  `~/.for3s/brian`) → InvalidTag → re-cifrado con la correcta; regla documentada en el
  Flujo. · Identidad: SOUL/IDENTITY/USER de Fruterito ADAPTADOS (no copiados) a los
  borradores que Brian APROBÓ → escritos a `persona/` (ensamblador 16,510 chars, núcleo
  blindado intacto, E2E: "soy… con alma de Fruterito") + hechos de Brian al perfil P1.
- **E3 línea de tiempo (403fd65 + ca24ed3 + registro):** `entrenamiento_olas.py` — parser
  jsonl OpenClaw (árbol parentId→secuencia, thinking descartado, toolResults truncados
  800ch, cron-runs → 1 resumen/día) + parser .md + **redacción de secretos línea a línea**
  + clasificación memoria/backlog/basura. **5 olas aplicadas:** génesis 2,506 · mar-1
  17,135 (pico) · mar-2 9,243 · abril 2,631 · residuo 17 = 31,532 (+42 e5-b1 +2 chat).
  3 iteraciones deshacer/reaplicar hasta CERO secretos crudos (redactor endurecido:
  sk-/ghp_/pat/JWT/genéricos + el mask de OpenClaw `sk-ant-o...X`). Backfill embeddings
  local completo.
- **E4 skills (c8d42fd):** `entrenamiento_skills.py` — cada SKILL.md único → skill H12
  viva vía SkillStore (embedding, provenance=usuario → curator no las toca). 15 skills.
  `mode_*` (runtime OpenClaw) → backlog. **Examen matcher 3/3** (hackathon Monad →
  hackathon-mode+monad-development · auditar PR → audit-code · breeding → genomad+chain-agent).
- **E5 cierre (72df024):** `cerrar_manifiesto()` — **GAP cazado:** 42 docs B1
  (HISTORIAL-COMPLETO, ETHICS, REPORTE-FRUTERO-CLUB, análisis CEO, PLAN-INMORTALIDAD…) no
  entraban en ninguna ola (filtro B2/B3/B5/B7) → lote `e5-b1`. Resto decidido: 5,298
  duplicados · 1,756 basura · 3,876 backlog. **MANIFIESTO: 0 sin decisión.**

## 3 · E5b DIGESTIÓN (decisión Brian: manual por pasadas + híbrido + anti-529)

**20 pasadas CLS manuales** (`/tmp/pasada_cls.py` en el worker: presupuesto de conceptos
por pasada, orden cronológico, reanudable; tras ver un 529: presupuesto 40 + pausa 6s =
**cero 529 desde entonces**). Resultado: **15,433/31,576 consolidados (49%) · 669
conceptos** · cronología digerida ene→ABRIL en orden (incl. la sesión final de dev).
Calidad observada: de "Saludos iniciales" (génesis) a "DevRel Frutero", "Identidad
Fruterito DevRel" (marzo) — el grafo madura como maduró la vida real.
**La cola (16,143 eps) la termina el CLS nocturno solo** (job 08:00 UTC, varias noches).

### Los 3 BUGS DE PRODUCTO que la digestión manual cazó (su mayor valor)

1. **Migr 034 (04ef6ff):** el grafo AGE (`for3s_kg` + `cypher_write/read/read_json`) se
   creó A MANO en Foresito (H5) y NUNCA entró a migraciones → **toda instalación fresca
   nacía con el grafo ROTO en silencio** (kg marca "no crítico"; el CLS consolidaba 0
   SIEMPRE). Fix idempotente con las definiciones exactas de Foresito.
2. **Fix `incluir_import` (8d24238) — EL BUG MAYOR del hito:** `buscar_semantico` filtra
   por sesión → los 31K importados eran INVISIBLES para el chat del dueño (el examen
   "aprobaba" Genomad/Godínez por las SKILLS, no por los episodios; Vibecoding sin skill
   lo destapó). Fix aditivo fail-closed (el corpus `channel='import'` del MISMO humano se
   suma; miembros solo ven imports con SU id; Foresito sin imports = idéntico).
   **Examen post-fix APROBADO con conciencia temporal:** "hace ~5 meses trabajamos en el
   VibeCoding Bootcamp… 2 semanas, de idea a app desplegada…".
3. **Fix escaping Cypher (917bb99):** `kg._esc` escapaba al estilo SQL (`''`) pero Cypher
   escapa con BACKSLASH → labels con apóstrofes reventaban el write (Foresito nunca lo
   pisó: labels en español sin comillas; el material OpenClaw sí). E2E verificado con el
   caso exacto + backslash, escritos y leídos intactos.

También manejados en vivo: racha de ConnectError (red doméstica) → fallback heurístico
sin caída · JSON inválido del LLM → fallback (defensivo H6 demostrado 2 veces).

## 4 · MECÁNICA REPETIBLE (si algún día hay más material)

```
contenedor efímero (docker run --rm · material :ro · red for3s-brian_default
  · SI toca vault: -v ~/.for3s/brian:/root/.for3s:ro ← LECCIÓN KEK)
python -m for3s_core.entrenamiento <censo | secretos[-aplicar] |
  ola[-aplicar] <n> <desde> <hasta> | skills[-aplicar] | cierre[-aplicar] | reversa-vacio>
digestión: docker exec for3s-brian-worker-1 python /tmp/pasada_cls.py <conceptos> <sesiones> <pausa>
reversa: entrenamiento.lote_deshacer(pool, lote_id)  — quirúrgica, demostrada
```
Módulos (en el repo, con tests): `entrenamiento.py` · `entrenamiento_censo.py` ·
`entrenamiento_secretos.py` · `entrenamiento_olas.py` · `entrenamiento_skills.py`.

## 5 · LO QUE QUEDA (cierre final, en RETOMAR)

1. Cola de digestión → CLS nocturno (verificar `consolidated_to_kg` en días siguientes).
2. **Examen global** (~40 preguntas) cuando el grafo madure (2-3 noches).
3. **Microglía ON** en brian (`FOR3S_MICROGLIA_CONFIRMAR=true` en `~/.for3s/brian/.env`
   + recrear agent/worker).
4. Batería §5-BIS final + version bump + decisión de Brian sobre las 1,234 fotos B7.
5. ~12 commits del hito firmados en server, **SIN push** (regla server-primero).

**Veredicto al corte:** de 6 agentes OpenClaw → 1 For3s OS personal con la vida de
Fruterito dentro: memoria episódica completa y VISIBLE, mitad del grafo digerido y
creciendo cada noche, skills vivas, secretos al vault, identidad heredada. El material
original en `~/entrenamiento/` queda INTACTO como respaldo eterno.
