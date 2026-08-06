# BLOCK · demo

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-demo-2026-07
type: code
intent: turn the web demo from an MVP into something that can be handed to a client
status: active · lane: full-block
owner: brian
created: 2026-07-24 · updated: 2026-07-29

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- marca-personal/lib/demo/*.ts · components/demo/* · components/for3s-admin/*
- marca-personal/app/api/demo/**
- marca-personal/tests/*.test.ts (§F-8; declarados ahí desde 2026-08-05, en el scope el 08-06:
  el §F los gobernaba y el §B no los cubría, así que los hooks enmudecían sobre ellos)
- Neon DB `for3s_demo` (demo_* tables)

## ⛔ OUT
<!-- Only limits SPECIFIC to this block. System-wide rules are not repeated here —
     they apply with or without a block and live in CLAUDE.md / base-rules.md.
     Repeating them made this block look like their source, which it is not. -->
- DO NOT touch the For3s-OS agent (`for3slabs/for3s`) — separate repo. This block only
  CONSUMES 5 endpoints: /v1/chat · /v1/conector · /v1/miskeys · /v1/oauth · /v1/token
- DO NOT change `api_channel.py` — DERIVED: it lives in the agent's repo, so by the
  block-lifecycle.md §2 test it is separate work, not a sub-block of this one
- DO NOT touch the admin panel's non-demo sections — outside this block's intent

## 🌐 System-wide rules that also apply (inherited, not owned here)
- `CLAUDE.md`: never touch marca-personal/Mente/ · never read ~/5M-incubathon/ without the gate
- `base-rules.md` #7: server-first — push to GitHub only on explicit order
  ⚠️ Vercel deploys from `main`, so **any push to main is a production deploy**

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: the For3s-OS agent via the API channel (`/v1/chat`) — not yet a block
- DEPENDED ON BY: none declared
- ISOLATED FROM: everything else in Mente OS
- 🔴 CRITICAL PIECES (imports measured 2026-07-29 with `bin/new-block --piece`):
  - lib/demo/session.ts → 12 · lib/demo/userStore.ts → 12
  - lib/demo/instancias.ts → 9 · for3sChat.ts → 6 · eventos.ts → 6

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
## Required standards
- rules/rule-fix-not-patch.md
- rules/rule-lanes.md
- rules/case-dangerous-default.md
- rules/rule-shipping-flow.md
- principles/expertise/dev-database.md
- principles/expertise/dev-backend.md
- principles/expertise/val-functional.md
- principles/expertise/val-integration.md
- principles/expertise/dev-frontend.md
<!-- dev-frontend was removed 2026-07-30 ("re-add when sub-block 10 touches a component") and
     re-added 2026-08-05: sub-block 10 IS that case — deleting components/demo/ConnectClaude.tsx,
     145 lines with 0 importers. The condition it set for its own return was met. -->

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: ⭐ LAYER 1 = 🟢 PRODUCT (2026-08-05). Los dos rojos cerrados: dead code 1→0, tests 0→4
next: todo lo abierto espera un dato de Brian — ver blockers
blockers: §F-9 hosting · §F-11 rutas OAuth dormidas · rama de Neon para 13 tests (§B1) → BRIAN
progress: 9/12 cerrados · §F-8 4/4 escritos · 🟢 **0 tests en rojo** (§F-7 cerrado por la raíz)
note: 🟢 PRODUCT es la CAPA 1 (medible); la capa 2 se corre AL CERRAR y el bloque NO cierra —
      §F-7 sigue abierto con un agujero de autorización real.
updated: 2026-08-05
note: the red test is the deliverable, not a defect — how to run them and what NOT to touch is
      `blocks/active/demo/docs/como-correr-los-tests.md`.

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | imports | status |
|---|---|---|---|---|
| 1 | DB-only bridge, no env (I1-I5) | lib/demo/instancias.ts | 9 | closed |
| 2 | single guard, 12 copies to 0 (S1-S3) | lib/demo/session.ts | 12 | closed |
| 3 | brute-force protection (V1-V4) | lib/demo/verificacion.ts | 3 | closed |
| 4 | safety net + identity without `kind` (U1-U6) | lib/demo/userStore.ts | 12 | closed |
| 5 | per-instance telemetry | lib/demo/eventos.ts | 6 | closed |
| 6 | real agent on/off, owner only (model C) | lib/demo/container.ts | 2 | closed |
| 7 | ⭐ CERRADO por la raíz: jazz/mashe BORRADAS y `allowedEmails.ts` eliminado | (archivo borrado) | 0 | ✅ closed |
| 8 | tests 4 caminos: ② ✅ · ③ ✅ · ④ ✅ · ① + integración esperan rama Neon → **`blocks/active/demo/docs/como-correr-los-tests.md`** | tests/apagar.test.ts | 0 | active |
| 9 | decide the hosting | (infrastructure) | 0 | blocked |
| 10 | delete the orphan (0 importers since 2026-06-16) | components/demo/ConnectClaude.tsx | 0 | ✅ closed |
| 11 | decidir si las 3 rutas OAuth + el guard se borran o siguen dormidas | lib/demo/oauthGuard.ts | 2 | BRIAN |
| 12 | error de eslint PREEXISTENTE (setState síncrono en un effect) | components/demo/ProfilePanel.tsx | 1 | ✅ closed |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- ⭐⭐ 2026-08-06 · **§F-7 CERRADO POR LA RAÍZ, no parcheando el assert.** Brian: *"elimina las
  instancias de jazz y mashe, son ruido y no se han ocupado"*. Medido antes de borrar: `jazz` 4
  episodios / 3 personas · `mashe` 8 / 4 — restos de las pruebas E2E de julio, **cero dueños
  registrados** en `demo_duenos`. Respaldadas (`pg_dump`, 46 tablas cada una, verificado) antes de
  ejecutar `for3s borrar`. Resultado: **0 volúmenes y 0 contenedores residuales**, `general` intacta.
  🟢 **Y con eso el agujero desapareció:** sin instancias 1:1 legado que compatibilizar,
  `lib/demo/allowedEmails.ts` perdió su razón de existir y se BORRÓ, junto con el paso *"autorizado
  por ENV"* de `resolverAcceso()`. Quedan 2 fuentes de verdad, ambas en BD: `demo_duenos` y
  `demo_llaves` — **ninguna se satisface con un correo inventado**.
  📊 **tests: 1 rojo → 0.** `bun run build` exit 0 · `tsc` exit 0.
- 🔬 2026-08-06 · **El test de ② pasó de puro a INTEGRACIÓN, y eso ES la mejora.** Antes se probaba
  sin BD porque la autorización vivía en una constante; ahora exige Postgres porque la verdad vive
  ahí. Sus 5 tests se suman a los saltados hasta la rama de Neon (§B1). ⚠️ **Menos verdes no siempre
  es peor**: el que se perdió medía un `DEV_FALLBACK` que no debería existir.
- ⚠️ 2026-08-06 · **jazz/mashe retiradas de 5 listas del código, cada una por su razón.**
  `INSTANCIAS_SEMILLA` es el fallback si Neon cae (degradar a una instancia borrada sería peor que
  no degradar) · `INSTANCIAS` valida el panel admin · `OAUTH_KINDS` sigue FIJA a propósito, ahora
  con solo `brian` · `accounts.ts` llevaba **tokens de dev en claro** para instancias que ya no
  existen: una credencial suelta, no compatibilidad. En la BD quedaron **inactivas, no borradas**
  (UPDATE reversible).
- ⭐ 2026-08-05 · **Sub-bloque 10 CERRADO: `ConnectClaude.tsx` borrado (145 líneas, 0 importadores).**
  Verificado antes de borrar: la única mención en todo el repo era su propia declaración. Borrado con
  `git rm` (la historia sobrevive) + copia fuera del repo. Comprobado después: **`tsc --noEmit` exit 0**
  y los tests igual que antes. **Veredicto del bloque: 🔴 MVP → 🟢 PRODUCT** (dead code 1 → 0,
  test files 0 → 4).
- 🔬 2026-08-05 · **El huérfano era la PUNTA de un árbol, no una hoja — y medirlo cambió el alcance.**
  Al borrarlo, las **3 rutas OAuth + `lib/demo/oauthGuard.ts`** (135 líneas más) quedan sin ningún
  consumidor de web. ⛔ **No se borraron**: `oauthGuard.ts` no es basura olvidada, es un **candado de
  seguridad** con el riesgo asumido por escrito y `OAUTH_KINDS` fija A PROPÓSITO (borrarlo eliminaría
  una capacidad que Brian decidió conservar para pruebas internas). Quedan **dormidas y seguras**: sin
  `DEMO_OAUTH_INTERNAL=1` devuelven 403. **Brian eligió el alcance del bloque, no el del árbol** →
  nuevo §F-11.
- ⭐ 2026-08-05 · **③ TALK se partió en dos mitades, y la línea es una MEDICIÓN.** Medido antes de
  escribir: `for3sChat.ts` cruza **dos** fronteras (Postgres vía `instancias`/`userStore`, y HTTP al
  agente por `fetch`). La mitad pura (`clientIdDeCorreo`) corre siempre; la de integración se salta
  igual que ①. ⛔ **No se simuló el `fetch`**: `val-functional.md` §2.3 — un mock de lo que cruza un
  proceso prueba el mock. Llamar al agente de verdad mandaría un mensaje a una instancia viva y
  gastaría cupo de Claude, así que queda **declarado como pendiente, no fingido**.
- 🔬 2026-08-05 · **El test de ③ se VIO FALLAR antes de creerle.** Se saboteó `clientIdDeCorreo` para
  reproducir el bug original (borrar `@ . +` en vez de hashear) y los 3 correos volvieron a
  colisionar: **2 tests en rojo**. Restaurado byte a byte (`git status` limpio). `val-functional.md`
  §2.2: *un check debe verse fallar antes de que su verde signifique algo* — un test que pasa a la
  primera y nunca se vio en rojo no ha demostrado nada.
- ⭐ 2026-08-05 · **`gate-critical.py` ahora exime a un test de integración — con condición.**
  La puerta bloqueó `tests/entrar.test.ts` por hacer `DELETE`/`UPDATE` desde un `.ts`. Era correcto:
  la regla se escribió cuando no existía ningún test. Pero un test de integración **debe** limpiar
  lo que escribe, y prohibirlo forzaría un `db()` simulado — que prueba el simulacro, no el freno
  (`val-functional.md` §2.3). **La exención NO es "es un test":** solo aplica si el archivo nombra
  una conexión dedicada (`DATABASE_URL_TEST`). Un test que alcanza la URL de producción **sigue
  bloqueado**, y ese es justo el caso que vale la pena cazar. Probado en los 3 casos: exento ✅ ·
  test sin variable dedicada → exit 2 ✅ · código de aplicación → exit 2 ✅.
- 🔴 2026-08-05 · **`DEMO_DATABASE_URL` apunta a Neon de PRODUCCIÓN** (medido: 4 instancias vivas,
  1 verificación en curso). Por eso ① lee `DEMO_DATABASE_URL_TEST` y **se salta** si falta, en vez
  de caer de vuelta. Un default que apunta a algo con dueño es el error ya registrado en
  `feedback_default_nunca_apunta_a_algo_con_dueno`.
- 2026-08-05 · **`dev-backend.md` added to §D** — this block declares `app/api/demo/**` in its
  Scope IN, so it **is** backend. Caught by the check written the same day (*every filled expertise
  file must reach an active block*): the criterion was written and nothing declared it, so the hook
  would never have delivered it. **The validator caught the AI, not the other way round.**
- 2026-08-05 · **owner-3's two disciplines added to §D** (`val-functional` · `val-integration`).
  Rationale: both were filled the same day and **no active block declared them**, so the hook never
  delivered them — filled criterion that reaches nobody governs nothing. They are not generic
  additions: **sub-block 8 is literally "tests for the 5 critical paths" with 0 test files today**,
  which is what `val-functional` judges (*what counts as proof*, and *a check that cannot fail is
  deleted*). And **sub-block 7 removes a `DEV_FALLBACK` that authorizes a fake email** — an
  authorization seam, which is `val-integration` §2.2: *identity is verified, never assumed*.
- 2026-08-05 · **`rules/rule-shipping-flow.md` added to §D.** Rationale: the rule was created the
  same day and **no active block declared it**, so `hooks/pre-edit-standards.py` — which injects
  only what §D lists — never delivered it. A shipping flow nobody is handed is not a flow.
  It matters most here: this block ships to `marca-personal`, where **Vercel deploys from `main`,
  so any push to main is a production deploy** (§B). The flow's rule 1 is exactly that anti-pattern.
- 📦 **Las 7 decisiones de JULIO (sub-bloques 1-6, cerrados) viven en
  `blocks/active/demo/docs/decisions-julio.md`** — movidas íntegras el 2026-08-05 al pasar este
  archivo su techo de 200 líneas. ⛔ Ninguna se resumió ni se borró (`doc-structure.md`).
- 📦 **Hallazgos del MOTOR → `blocks/active/demo/docs/hallazgos-del-motor.md`** (íntegros, 08-05).
- 📦 **Decisiones de los tests (§F-8) → `blocks/active/demo/docs/decisiones-tests.md`** (íntegras).

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- (none recorded)

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-07-26 · 1c54a49 · explicit topic sent by the site
- 2026-07-26 · 5f86bed · `kind` column and demo_accounts dropped
- 2026-07-26 · 793e858 · heartbeat + TTL — current HEAD of main

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context
Site repo `ElBrAyAn1967/For3s` — **not** the agent's. Branch `main` at `793e858`, clean.
Neon DB `for3s_demo`: `demo_instancias` is the single source of truth, 7 FKs, `demo_config`
editable without a push.
`DEMO_ENC_KEY` rotated and unified local=Vercel on 2026-07-26 — they had diverged since June
and a fallback was hiding it. Key lives in `Mente/secrets/`.
Reachable through the Tailscale Funnel — which means **it depends on Brian's laptop being on**.
Full chronology of the 2026-07-24/26 session: `memory/PENDIENTES.md` and the demo memories.

**Recovered docs** (moved here 2026-07-30 from `marca-personal/Mente/Doc/`, where the AI had
written them during the 2026-07-21 scope violations — see docs/):
- `blocks/active/demo/docs/demo-progress.md` — demo progress, June
- `blocks/active/demo/docs/guide-github-oauth-app.md` — ⭐ **operational step Brian still has to execute**
- `blocks/active/demo/docs/plan-piece-e-admin.md` — the Piece E admin plan

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — the block is still active)
