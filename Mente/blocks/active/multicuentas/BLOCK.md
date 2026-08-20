# BLOCK · multicuentas

<!-- ══ A · IDENTITY ══ required to OPEN · ≤6 lines ══ -->
id: blk-multicuentas-2026-08
type: infra
intent: que Mente OS sepa QUÉ cuenta usa cada repo, POR QUÉ existe y CÓMO se accede — hoy vive en memoria humana
status: active · lane: direct · owner: brian
created: 2026-08-19 · updated: 2026-08-19

<!-- ══ B · SCOPE ══ required to OPEN · ≤20 lines ══ -->
## ✅ IN
- 🆕 **cuentas.tsv** (F1) — el registro: una fila por repo (cuenta · rol · por qué existe · remoto)
- **secrets/Acceder_Cuenta_&lt;cuenta&gt;.md** — 🆕 3 guías (fruterito101 · for3slabs · ElBrAyAn1967)
- **bin/check-accounts** — 🆕 el validador que compara lo escrito contra `git remote -v`
- **bin/conectar-cuenta** — 🆕 el que resuelve credencial por repo, como `bin/conectar-servidor`
- **hooks/gate-accounts.py** — 🆕 la puerta: un push a un repo no registrado se detiene
- `secrets/README.md` · `piezas.tsv` · `CAPABILITIES.md` — declarar lo nuevo

## ⛔ OUT
- ⛔ **NO se escribe NINGÚN token, contraseña ni valor de credencial en ningún archivo de este bloque.**
  Las guías dicen DÓNDE vive y CÓMO se pide — nunca QUÉ es (`PROJECT-RULES.md` §5)
- ⛔ **NO se rota ni revoca ninguna credencial** — es decisión de Brian, no del bloque
- ⛔ NO se toca `~/.git-credentials-for3s` del servidor (es del producto, no del motor)
- ⛔ NO se toca el Key Vault del producto — DERIVED: `secrets/README.md` separa "acceso de Brian"
  de "secrets del sistema"; este bloque es solo lo primero
- ⛔ NO se crean, borran ni cambian de visibilidad repos en GitHub

## 🌐 System-wide rules that also apply (inherited, not owned here)
- `PROJECT-RULES.md` §5: `secrets/` 700 · archivos 600 · gitignored
- `base-rules.md` #4: los secretos se REFERENCIAN, nunca se pegan
- `CAPABILITIES.md` §1: `bin/` y `hooks/` son MOTOR — cambio gated, se avisa

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: nada. Es infraestructura del motor, no de la campaña del producto
- DEPENDED ON BY: `seguridad` (sus PRs de SB-7..SB-10 empujan a los 2 remotos) ·
  `demo` (vive en `ElBrAyAn1967/For3s`, otra cuenta)
- ISOLATED FROM: los 12 bloques de `campaigns/producto-for3s-os` — este es MOTOR, no producto
- 🔴 CRITICAL PIECE: **hooks/gate-accounts.py** — si bloquea de más, ningún push sale

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤12 lines ══ -->
## Required standards
- rules/rule-checks-must-measure.md
- rules/rule-shipping-flow.md
- rules/rule-pr-base.md
- rules/rule-config-hygiene.md
- rules/contract-document.md
- principles/expertise/val-integration.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: **F1-F6 CONSTRUIDAS** — plan aprobado por Brian el 2026-08-19
next: cerrar el bloque (§K) tras una jornada de uso real de la puerta
blockers: ninguno
progress: **6/6 fases** · batería 249 → **260** (+11) · 6 sabotajes probados
updated: 2026-08-20

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | pieza | dependents | status |
|---|---|---|---|---|
| 1 | **cuentas.tsv** — el registro, una fila por repo | Mente/cuentas.tsv | 0 | ✅ done |
| 2 | **bin/check-accounts** — compara lo escrito vs `git remote -v` | bin/ | 0 | ✅ done |
| 3 | las 3 guías **Acceder_Cuenta_*.md** en `secrets/` | secrets/ | 0 | ✅ done |
| 4 | **bin/conectar-cuenta** — resuelve credencial por repo | bin/ | 0 | ✅ done |
| 5 | **hooks/gate-accounts.py** — detiene un push a repo no registrado | hooks/ | 0 | ✅ done |
| 6 | cablear: `piezas.tsv` · `CAPABILITIES.md` · batería §F7 · settings.json | varios | 0 | ✅ done |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- ⭐ 2026-08-19 · **El bloque es `infra`, no `code`.** Rationale: `ADR-028` — `grade-block` mide
  tests e importadores; sobre guías y un `.tsv` daría 🔴 MVP para siempre por medir lo que no
  aplica. `infra` mide runbook, rollback y "secretos referenciados, no pegados".
- ⭐ 2026-08-19 · **El registro es un `.tsv`, no un `.md`.** Rationale: `piezas.tsv` ya probó el
  patrón — una máquina lo lee sin parsear prosa, y mover algo cuesta una línea.
- ⭐⭐ 2026-08-19 · **Las guías NO llevan el valor del secreto, solo la RUTA.** Rationale:
  `Conectar_Servidor_For3s.md` sí lleva la contraseña en claro y por eso la carpeta es 700 y
  está fuera de git. ⚠️ Replicar eso 3 veces multiplica por 3 la superficie expuesta. Las nuevas
  guías dicen *dónde* vive el token y *cómo* pedirlo — nunca cuál es.
- ⭐ 2026-08-19 · **El validador compara contra `git remote -v`, no contra otro documento.**
  Rationale: el defecto que originó este bloque fue exactamente ese — 3 documentos decían 3 repos
  distintos y ninguno se comparó con la máquina durante 31 días.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- ⚠️ 2026-08-19 · **El bloque nace de un fallo del propio sistema, no del producto.** Ningún
  validador comparaba lo escrito sobre repos contra `git remote -v`, así que `PROJECT-RULES.md`
  citó un repo que dejó de ser oficial **46 días** y la memoria llamó *"copia vieja"* al que el
  servidor usa como `origin` **31 días**. ⭐ Es la ley del sistema aplicada a sí mismo: una regla
  sin validador se cumple 40-60%.

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-19 · Bloque abierto. Terreno YA medido en el servidor, no heredado: `git remote -v`
  declara `origin`→`for3s-os` y `backup`→`for3s`; los 2 commits atrasados empujados a ambos
  (tríada real en `732c434`); 3 cuentas identificadas (`fruterito101` · `for3slabs` ·
  `ElBrAyAn1967`, esta última hallada en `Maestro/punteros.tsv`, no en las listas de GitHub).

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context

**El hueco, en una frase: Mente OS gobierna cómo se trabaja, pero no sabe con qué cuenta se empuja.**

### Lo que existe hoy, medido

| Pieza | Estado |
|---|---|
| `secrets/Conectar_Servidor_For3s.md` | ✅ el patrón que funciona — guía paso a paso, fuera de git |
| `hooks/gate-secrets.py` | ✅ la puerta: lease para leer, **ask siempre** para escribir |
| `secrets/.access-log.md` | ✅ toda lectura queda registrada |
| `Maestro/punteros.tsv` | 🟡 lo más cercano a un registro — 5 ramas con URL y dueño |
| **un registro de CUENTAS** | 🔴 **no existe** |
| **un validador que lo verifique** | 🔴 **no existe** |

⭐ **La mecánica de seguridad ya está resuelta y probada** — `gate-secrets` + lease + log. Este
bloque **no inventa un modelo nuevo**: extiende el que ya funciona a un segundo tipo de acceso.

### Las 3 cuentas y por qué existe cada una

| Cuenta | Para qué | Evidencia |
|---|---|---|
| `for3slabs` | ⭐ la ORG — producto (`for3s`, `for3s-os`) y Mente OS | mudanza del 4-jul por descubribilidad |
| `fruterito101` | personal + el motor MIT publicado (`mente-os`) | 301 histórico del producto |
| `ElBrAyAn1967` | **el sitio/demo** (Next.js) — no el agente | `Maestro/punteros.tsv` |

### Por qué esto no es opcional

Brian, 2026-08-19: *"va a haber muchos repositorios, muchas cuentas... no podemos tener un sistema
que no pueda controlar eso"*. ⭐ **Y no es solo suyo:** el plan debe servir a **cualquiera** que
clone Mente OS — por eso el registro y las guías son de INSTANCIA (se generan), y el validador,
el resolutor y la puerta son MOTOR (viajan con el clon).

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — el bloque acaba de abrirse)
