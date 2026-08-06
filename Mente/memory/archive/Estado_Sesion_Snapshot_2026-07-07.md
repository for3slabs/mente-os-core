# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

> **Propósito:** este es el ÚNICO archivo que necesitas leer al retomar la conversación con Brian. Es pequeño a propósito (ahorro de tokens). Si necesitas más detalle, al final hay punteros a dónde buscarlo. **NO leas el Estado_Sesion completo (200KB) salvo que un puntero te mande ahí.**

**Última actualización:** 2026-07-05 (🎓 **HITO ENTRENAMIENTO EN CURSO — E0-E2 ✅ + Olas 1-2 de E3 aplicadas** · 🏢 **2 AGENTES en el server**).

## 🔴🌐 URGENTE — DESCUBRIBILIDAD (SEO/AEO/GEO) "nadie nos encuentra" (Brian 2026-07-04)
For3s OS no tiene descubribilidad: **cero SEO/AEO/GEO**. 🔍 Diagnóstico: el repo `fruterito101/for3s` SÍ
tiene topics/description pero solo 3 stars (GitHub no lo muestra sin señal social) · ⚠️ **GRAVE:
`for3s.vercel.app` es la web de "For3s QA" (marca-personal), NO del AGENTE** → quien llega del repo no
encuentra el producto · esa web no tiene meta/schema.org/sitemap. **Hueco #1: definir una landing del
AGENTE.** Luego SEO base + AEO (schema FAQPage/SoftwareApplication) + GEO (que ChatGPT/Claude recomienden
For3s: docs/comparativas indexables + awesome-lists) + primeras stars. Detalle en PENDIENTES §DESCUBRIBILIDAD.
Cruza con DIST-1/DIST-3 + la charla (= tráfico). **NO arrancar hasta que Brian diga; solo tenerlo presente.**

## ⏰ PENDIENTE CON FECHA — VALIDACION_WEB3 (charla AI x Blockchain Day, jueves ~10-17 jul, 25 min)
Brian dará un **taller/charla "Dale un trabajo a tu agente"** en el evento **AI x Blockchain Day** →
**demostrar en vivo el valor de For3s OS** como agente potente (memoria real, identidad viva, ejecuta
código, GitHub, equipo, trabaja solo, self-hosted). El evento encaja perfecto (paneles de "identidad tras
la explosión de bots" y "agentes con wallets"). Duración: 25 min. Falta: guion de demo + slides +
⭐🔴 **VERIFICAR FOR3S OS E2E EN TELEGRAM 1-2 días antes (que la demo NO falle en vivo)** — batería §5-BIS +
probar cada mensaje del guion con el modelo real. Detalle en PENDIENTES.md §VALIDACION_WEB3.

## 🎓 LO MÁS RECIENTE (2026-07-05) — HITO ENTRENAMIENTO EN CURSO + 2 AGENTES EN EL SERVER

**🏢 SEGUNDO AGENTE CREADO (prueba de fuego MULTI-INSTANCIA REAL):** ahora hay 2 For3s OS
completos e independientes en el server: **Foresito** (`@For3s_OS_bot`, proyecto `for3s`, agente
de la EMPRESA) y **brian** (`@For3s_Brian_bot`, proyecto `for3s-brian`, el PERSONAL de Brian —
recibe el entrenamiento). Misma imagen v0.15.0, cero comunicación entre ellos, misma suscripción
Claude (cupo COMPARTIDO). Bugs cazados al crearlo: plantilla instancia sin volúmenes persona/mods
(53f520a) · gestor sin modo no-interactivo (--token/--owner) · **BUG instalación fresca: FK
personas rompía el 1er mensaje del dueño** (842b6d1) · flags OPT-IN no llegaban a contenedores
(ff11ee9: de paso se descubrió que la MICROGLÍA de Foresito llevaba en SIMULACRO desde la
contenedorización — restaurada). brian a MÁX POTENCIAL: estilo+perfil inferido ON, /autogen ON,
/dmn generativas ON, identidad Fruterito adaptada; microglía OFF a propósito hasta post-entrenamiento.

**🎓 HITO ENTRENAMIENTO (6 agentes OpenClaw → 1 For3s OS) — EN CURSO, destino @For3s_Brian_bot:**
- **Docs del hito:** `work/Ronda_Entrenamiento_Plan_Maestro.md` (etapas E0-E5, LÍNEA DE TIEMPO
  global en olas cronológicas — los agentes fueron CONTEMPORÁNEOS, importar por-agente rompería
  la causalidad) · `Cuerpo/Flujo_Extraccion_Entrenamiento.md` (el tubo FE0-FE8 repetible) ·
  radiografías principal/dev/wsl + `Entrenamiento_Bloques_…Dev.md` (7 bloques + capa secretos).
- **✅ E0 (866b00c):** migr 033 (import_manifiesto/import_lotes/episodes.import_lote) + módulo
  `entrenamiento.py` (lotes reversibles, created_at=fecha ORIGEN) + backup pre-entrenamiento
  verificado + **REVERSA DEMOSTRADA en vacío** (cazó bug FK sessions).
- **✅ E1 (cc12697):** CENSO forense de las 2 raíces — 11,664 archivos al manifiesto con hash/
  bloque/fecha/dup. Hallazgos: wsl = ESPEJO del principal (6,600 dups; "734 docs del empleado" =
  5 únicos) · 67 secretos por ruta + 81 embebidos · línea de tiempo ene→may 2026 → 5 olas.
- **✅ E2 (fe5374a):** 38 secretos únicos → VAULT cifrado de brian (descifrado verificado;
  LECCIÓN KEK: todo docker run que toque el vault DEBE montar ~/.for3s/brian) + identidad
  Fruterito ADAPTADA a persona/ con gate de Brian (ensamblador 16,510 chars, núcleo blindado
  intacto, respondió "alma de Fruterito" E2E) + perfil P1 de Brian (Jazz Criptec, prefs).
- **🔄 E3 LÍNEA DE TIEMPO (en curso):** **Ola 1 génesis ene-feb APLICADA** (403fd65: 2,506
  episodios, 3 bugs cazados con deshacer/reaplicar: clasificación memoria/backlog/basura +
  redactor endurecido hasta 0 secretos crudos + mask OpenClaw) · **Ola 2 mar-1-15 APLICADA**
  (ca24ed3: 17,135 episodios EL PICO; único hit = placeholder ghp_xxx de docs, no secreto).
  **Total: 19,643 episodios** con fechas reales. Manifiesto: 8,496 pendientes (olas 3-5).
- **✅ E3 COMPLETO (las 5 olas):** 31,576 episodios (ene→may 2026, fechas ORIGEN reales, 100%
  embebidos, 0 secretos crudos). **✅ E4 (c8d42fd):** 15 skills VIVAS (matcher semántico 3/3:
  hackathon→hackathon-mode, PR→audit-code, Genomad→genomad). **✅ E5 CIERRE (72df024):**
  manifiesto **11,664/11,664 decididos, 0 pendientes** (GAP cazado: 42 docs B1 —HISTORIAL,
  ETHICS, REPORTE-FRUTERO— no entraban en olas → lote e5-b1). Examen pre-digestión: Genomad ✅
  PERFECTO · Godínez Studio ✅ (citó su skill) · Vibecoding ❌ aún (necesita CLS) y fue HONESTO.
- **✅ E5b DIGESTIÓN ARRANCADA A MANO (2026-07-05, decisión Brian: pasadas manuales + híbrido):**
  **20 pasadas CLS → 15,433/31,576 consolidados (49%)**, cronología digerida ene→ABRIL EN ORDEN
  (incl. la sesión final de dev c27178c0), **669 conceptos** al grafo. Cola 16,143 al nocturno. 3 BUGS cazados: **migr 034** (grafo AGE faltaba en instalación
  fresca — el CLS consolidaba 0 SIEMPRE en frescas, invisible; 04ef6ff) · **fix incluir_import**
  (BUG MAYOR: buscar_semantico filtraba por sesión → los 31K importados eran INVISIBLES al chat;
  el examen aprobaba por las SKILLS; fix aditivo fail-closed en memory/memoria; 8d24238; examen
  Vibecoding APROBADO con conciencia temporal "hace ~5 meses") · deuda menor: kg write revienta
  con APÓSTROFES en labels (escaping Cypher, 1/560, defensivo siguió — fix pendiente). Anti-529:
  presupuesto 40 + pausa 6s = cero 529.
- **✅ fix apóstrofes HECHO (917bb99):** kg._esc escapaba al estilo SQL (''), Cypher escapa con
  BACKSLASH → labels con apóstrofes reventaban el write. E2E verificado (apóstrofe + backslash
  escritos y leídos intactos). El CLS nocturno ya digiere con el escape sano.
- **🔬 E6 BACKLOG PROFUNDO (Brian: archivo por archivo, nada omitido — plan
  `Cuerpo/Plan_Backlog_Profundo_E6.md`):** curación WATCHDOG hecha (11,419→286 señal pura, 97.5%
  ruido soft-deleted recuperable, 18 conceptos-heartbeat fuera del grafo; 09a2b67) · **F1 docx/pdf ✅
  (a77bf5a): 52/52 uno por uno, 46 importados (Genomad completo, guiones, cotización, ARVI), 6
  gemelos, fichas en detalle.e6** · **F2 triage ✅ (33605cd): 1,827 uno por uno por magic bytes —
  930 prosas RESCATADAS (hackathons por ciudad, FRUTERO BUILDERS SPRINT oculta sin extensión),
  514 config, 377 git-objects, cobertura 0 sin ficha** · **F3 código ✅ (37e6492): 591 uno por uno →
  `work/Entrenamiento_Catalogo_Codigo.md` (15 proyectos) + 15 episodios-resumen** · **F4.1 triage
  fotos ✅ (a0247e2): 1,402/1,402 con dims+phash+clase — 48 screenshots + 47 fotos-grandes = 95
  candidatas visión 1ª prioridad · 1,074 medianas (2ª) · 133 dups-visuales · 100 iconos** ·
  **F4.3 visión ✅ parcial (67130c2)**: 95 top + 100 muestreo medianas = **195 fotos en memoria**
  (0 errores, 0 secretos; leyó Studio/Genomad/Godínez.AI/GitHub/roles de la salchichonería) ·
  ⏸️ **PENDIENTE (decisión Brian 2026-07-05: "tarda demasiado")**: las **974 medianas restantes** —
  densidad de valor ALTA confirmada por muestreo; retomar por tandas de ~150 con
  `docker run … e6-vision` (reanudable, salta las ya vistas) cuando Brian diga · **F5 audio ✅
  (e06cb6f): 3/4 transcritos con whisper local (notas de voz de Brian a Fruterito), mp4 ilegible
  registrado** → **F6 cierre + examen E6** (tras noches de digestión).
  Avance global: análisis individual ~100% (solo falta VISIÓN de fotos + audio) · texto 100% ·
  digestión 33% (nocturna).
- **⏳ AL RETOMAR — cierre final del hito:** (1) la COLA (eps sin consolidar) la termina el CLS nocturno
  solo (varias noches; verificar avance con `consolidated_to_kg`) · (2) EXAMEN GLOBAL final ·
  (3) microglía ON en brian (FOR3S_MICROGLIA_CONFIRMAR=true + recrear) · (4) batería §5-BIS +
  Bitácora + version bump + decisión fotos B7. Las 2 raíces ya entraron completas — los 6
  agentes OpenClaw estaban DENTRO de ellas; no hay más fuentes.
- ⚠️ Commits del hito FIRMADOS en server (~27 ahead), **SIN push** (regla server-primero).

**📋 También (2026-07-04/05):** brechas OpenClaw (OC-E/C/M, 16) y Hermes (HG-1..18) REGISTRADAS
en PENDIENTES (comparaciones de construcción con código real: `Comparacion_For3s_OS_vs_Hermes_
Construccion.md` + OpenClaw) — NO desarrollar hasta que Brian diga · doc maestro para la web:
`memory/archive/For3s_OS_Completo_Vision_Web.md` (✅ hoy vs 🔜 roadmap) · pendiente CRON CONVERSACIONAL
enriquecido con el jobs.json real de OpenClaw como referencia.

---

## 🎭 (anterior, 2026-07-04) — HITO RECONSTRUCCIÓN FOR3S_ROLE ✅ COMPLETO (v0.15.0)

La personalidad de For3s pasó de un STRING MONOLÍTICO (~200 líneas en agent.py) a una **IDENTIDAD EN
CAPAS con un ensamblador único** (`identidad.py`, patrón memoria.recordar() = una sola voz coherente,
no silos). 8 fases F1-F7, cada una con la batería §5-BIS (TODO el sistema, no el carril):
- **F1** capas + ensamblador único (byte-IDÉNTICO al original = red de seguridad) · **F2** máscara
  editable en `/app/persona/IDENTITY.md` (en caliente, sin rebuild) + validador de líneas rojas ·
  **F3** auto-adaptación EXPLÍCITA ("sé más breve" → se acopla al instante + aviso 🎭) · **F4** INFERIDA
  nocturna (job_estilo observa tu estilo y se ajusta solo; probado con LLM real: captó el estilo de
  Brian) · **F5** MENTE OS del usuario heredable (Alma/Cerebro/Cuerpo/Doc + pendientes) · **F6**
  transparencia ("¿cómo te has adaptado a mí?") · **F7** CAPACIDADES viva + v0.15.0.
- **Núcleo BLINDADO**: base (aislamiento/honestidad/KEK) SIEMPRE gana; la capa usuario no la anula.
- **DOS MUNDOS** (regla de Brian): BASE FOR3S (nuestra, código, inmutable) vs CAPA USUARIO (suya, .md).
- 8 commits FIRMADOS, **EN SERVER SIN PUSH** (regla server-primero). Ronda:
  `Cuerpo/Ronda_Reconstruccion_FOR3S_ROLE.md`. Memoria: [[project_hito_identidad_viva]].

## ✅ (2026-07-03) — RONDA CI DE CONFIANZA 100% CERRADA (cero módulos ty-dirty)

Detalle de esa ronda ⬇️ (QA-3b v3 + CI limpio + confianza SEC-3/4/5/6):

**QA-3b v3 ✅:** limpiados los 3 ÚLTIMOS módulos ty-dirty con fixes REALES (cero `type: ignore`):
cache.py (cast str en get) · conversation.py (provider.model público + `Agent(provider: ClaudeProvider)`) ·
**telegram_channel.py 59→0** (`TypedDict _ProgCat` + properties `pool`/`agente`/`mcp` con assert + guards
defensivos uid/pat/provider/args/_equipo) · llm.py (model+adjuntos en el protocolo). 🐛 bug que introduje y
cacé: la 1ª inserción de properties partió `__init__` (código huérfano, `pin_store` indefinido) → reubicadas
antes de `setup()`. **El gate ty-crítico BLOQUEANTE del CI ahora cubre TODO el core (cero módulos sucios)** —
un bug de tipo nuevo en cualquier módulo rompe el CI. Verificado: 141 tests verdes, ruff/format/ty limpios,
**rebuild + Foresito arranca OK** (properties no disparan assert). **Pusheado a GitHub firmado (aa36b4f), CI
verde.** **Dependabot #2 ✅ mergeado** (checkout 4→7); server rebasado sobre backup/main (reconciliado).

**🧹 CI más limpio = cara de PRODUCTO (2026-07-03, tras duda de Brian "¿es demasiado CI?"):** analicé los 8
checks → veredicto: NO es bloat, es el estándar de producto serio, pero sobraba RUIDO visual. Acciones:
(1) **agrupé** SAST(bandit)+pip-audit+Pilar 3 Gate en UN job `Seguridad (SAST + deps + gate)` (antes 3 checks
sueltos); (2) **saqué** el Trivy image-scan (13GB, solo manual) a `trivy-image.yml` propio con solo
workflow_dispatch → ya NO sale "Skipped" en cada push; (3) branch protection actualizada al nuevo nombre.
Resultado: de 8 checks a los esenciales, cobertura INTACTA. Commit **2118907 firmado**, 5 checks verdes.
El Pilar 3 Gate se QUEDA (dormido): es el freno de despliegue para código que For3s se auto-genere (H11/H12)
= diferenciador del producto, no bloat. **Docs del repo actualizados (063d9f6):** CHANGELOG 0.13.0/0.14.0 +
ronda CI de confianza (inglés) + badge Trivy en README.

🎉 **RONDA CI DE CONFIANZA 100% CERRADA:** 5 workflows verdes (checks limpios) · TODO el core ty-bloqueante ·
4 urgentes de confianza (Scorecard/Trivy/SBOM+Sigstore/CodeQL) · release v0.14.0 firmado · 5 imágenes pineadas ·
9 hermanos endurecidos. Cada check del CI cazó bugs reales. Memoria: [[project_sesion_bugs_2026-07-02]].

## 🐛 (2026-07-03) — 10 BUGS ARREGLADOS (sesión de pruebas) + bot→AGENTE

**Contexto:** Brian probó For3s a fondo en Telegram y reportó 11 hallazgos ("no funciona nada", tarda,
comandos, memoria, estados…). Los tracé mensaje-por-mensaje (screenshot + timeline de logs + BD + código)
y arreglé 10 bugs, cazando 4 extra. Docs: `memory/archive/REPORTE_MAESTRO_BUGS_2026-07-02.md` (maestro) ·
`AUTOPSIA_MENSAJES_2026-07-02.md`. Memoria: [[project_sesion_bugs_2026-07-02]].

**🔥 HALLAZGO CENTRAL:** el bug raíz era **cache → 127.0.0.1 hardcodeado** (no leía VALKEY_HOST). Cada op
fallaba en 3.84s → "no funciona nada" era LENTITUD, no ausencia. Muchos "bugs" eran funciones sanas que se
sentían rotas por la lentitud.

**✅ 10 FIXES (todos verificados E2E + horneados, 7 rebuilds):**
1. cache 127.0.0.1 (raíz lentitud) · 2. typing en comandos (@con_typing) · 3. parser /estado_tema tolerante ·
4. detector versión +13 frases · 5. **MEMORIA PRIMERO** (va a memoria antes que GitHub) · 6. huele_a_codigo
(no dispara con "me gusta python") · 7. **create_issue** (el MCP renombró tools → traducción) · 8. alerta
proactiva de consumo al 80% · 9. **alucina "Brayan"** (nombre desde personas) · 10. centralizar modelos +
🐛 bug oculto cost-control (opus-4-8 daba $0). + verificación: tools de lectura GitHub sanas.

**🧠 bot → AGENTE (Brian preguntó):** For3s YA NO es bot, es AGENTE (10/12 criterios de Hermes + 2 que
Hermes NO tiene: auto-modificación, multi-instancia). Doc: `For3s_Bot_vs_Agente_vs_Hermes.md`. FOR3S_ROLE
actualizado: se reconoce agente. **2 brechas para paridad TOTAL (registradas en PENDIENTES §FUTURO, NO son
agencia):** ⭐ multi-canal (solo Telegram+consola) · ⭐ cron conversacional ("recuérdame cada lunes").

**✅ Sincronizado a GitHub 2026-07-03** (con orden de Brian, regla server-primero). Server + local + GitHub
en el mismo commit.

**🔴 EL CI CAZÓ UN BUG DE SEGURIDAD (2026-07-03):** al arreglar el CI (ruff/bandit fallaban), los tests
destaparon que mi fix del nombre rompió la INDENTACIÓN de `_autorizar` → el `return True, "dueño"` quedó
FUERA del `if is_authorized` → **el bot autorizaba a CUALQUIER extraño como dueño**. 4 tests de seguridad
lo cazaron. Arreglado (return dentro del if), 132 tests pasan, **CI 100% VERDE (commit 35a3de2)**. Lección:
el CI vale — atrapó lo que las pruebas del server no vieron (en prod _pool existe, el bug no se notaba).
El CI fallaba desde varios commits porque desarrollamos en el server (sin ruff/bandit). Ahora verde.
**5 mejoras de CI registradas** (PENDIENTES §SEGURIDAD→MEJORAS DE CI): CI-1 secret scanning ⭐ · CI-2
coverage · CI-3 build docker en CI · CI-4 badge README · CI-5 pip-audit. Ninguna urgente.
**+ 3 de BLINDAJE DE CALIDAD (Brian eligió, PRIORITARIAS, TODAS GRATIS)** en PENDIENTES §BLINDAJE DE
CALIDAD: **QA-1 ⭐⭐ test de migraciones E2E** (32 migraciones sin probar = hueco más grande) · **QA-2 ⭐⭐
Hypothesis** (property-based para parsers/detectores de texto libre) · **QA-3 ⭐ mypy estricto** (subir ty
de informativo a bloquea). Las 3 habrían cazado bugs reales de esta sesión. Aparte (cuesta tokens): evals
de LLM (semilla en el DMN). Repo público = CI ilimitado gratis.

**🚨 + 4 URGENTES de CONFIANZA DE PRODUCTO (Brian eligió tras análisis de internet NIST/OWASP/Microsoft/
OpenSSF, TODAS GRATIS)** en PENDIENTES §SEGURIDAD→CONFIANZA DE PRODUCTO: **SEC-3 ⭐⭐⭐ OpenSSF Scorecard**
(el badge/número que la industria mira para confiar) · **SEC-4 ⭐⭐⭐ Trivy container scan** (HUECO REAL: la
imagen Docker no se escanea hoy) · **SEC-5 ⭐⭐ SBOM+Sigstore** (supply chain firmada, estándar 2026) ·
**SEC-6 ⭐⭐ CodeQL** (SAST más potente que bandit). For3s YA tiene la cripto difícil (audit/hash-chain/KEK/
GPG = lo que Asqav vende como novedad); esto la hace VERIFICABLE por terceros = el salto a producto de
confianza. Prioridad: SEC-3 + SEC-4 primero.
**📋 PLAN DE OBRA del CI:** `Cuerpo/Ronda_CI_Confianza_Plan.md` — 10 pasos por impacto/esfuerzo. Todo gratis
(repo público). Cruza con SOC2-readiness.
**✅ SEC-3 OpenSSF Scorecard HECHO (2026-07-03) — score inicial 5.7/10.** workflow scorecard.yml (pineado
por SHA, semanal) + badge README + dependabot.yml + permisos ci.yml + **branch protection en main** (CI
debe pasar, sin force-push) + Dependabot security updates ON. 10/10 en Token-Permissions/Dependency-Update/
Security-Policy/License/Vulnerabilities/Dangerous-Workflow/Binary-Artifacts. Falta: SAST(→SEC-6 CodeQL),
Fuzzing(→QA-2), Signed-Releases(→SEC-5), Pinned-Deps(→SEC-3b, SHA ya identificados por el propio Scorecard).
🐛 Dependabot ya abrió 3 PRs solo (actualizar actions) = funciona.
**✅ SEC-6 CodeQL HECHO (2026-07-03):** workflow codeql.yml (python security-extended + actions, pineado,
sin build) — 1er run verde. 🔍 CAZÓ 1 alerta REAL que bandit NO vio: `py/incomplete-url-substring-
sanitization` (`"github.com" in url` → evil-github pasaría) → arreglado (verifica host real). Sube SAST del
Scorecard 0→10. Demostró su valor. Commits 52a80b4/07a3dfa.
**✅ SEC-4 Trivy HECHO (2026-07-03):** workflow trivy.yml en 2 modos (imagen agent=13.2GB, no cabe en
runner): fs-scan (deps+secrets) BLOQUEANTE + config-scan (Dockerfiles) informativo SIEMPRE; image-scan
manual. 🔍 hallazgos: deps uv.lock=0 vulns ✅; 2 Dockerfiles (agent+render) corren como ROOT (DS-0002 HIGH)
→ SEC-4b (endurecer a non-root, delicado por KEK/overlays/migración → con prueba E2E). Commits 2b8e96a/4472e3d.
**✅ SEC-5 SBOM+Sigstore HECHO (2026-07-03):** workflow release.yml (tag v*): SBOM syft (SPDX+CycloneDX) +
firma Sigstore/cosign keyless + GitHub Release. Adaptado a For3s (curl|sh, no pip → SBOM del código).
**✅ RELEASE REAL v0.14.0 CREADO** (tag firmado GPG → GitHub Release publicado con 4 assets: 2 SBOM + 2 firmas
Sigstore). 1er release oficial del producto. Resuelto el status 400 (Create Release condicional a refs/tags/).
🎉 **LOS 4 URGENTES DE CONFIANZA COMPLETOS (SEC-3 Scorecard + SEC-4 Trivy + SEC-5 SBOM/Sigstore + SEC-6
CodeQL).** 5 workflows: ci, codeql, release, scorecard, trivy. Cada CI cazó algo real (SHA imágenes, bug URL,
root Dockerfiles). **Pendientes rápidos acumulados:** SEC-3b (pinear 5 imágenes) + SEC-4b (Dockerfiles
non-root) — hallazgos de los propios CI, delicados, con prueba E2E.
**✅ QA-1 migraciones E2E HECHO (2026-07-03):** step en el job quality — aplica las 32 migraciones sobre BD
limpia del CI + verifica schema_version=32 (CI verde: "32|32|OK"). 🐛 cazó un acoplamiento: `cli migrate`
exigía ANTHROPIC_TOKEN → arreglado (lee DATABASE_URL directo, sin token; guardián sigue OK). b6aff6c/342fd09.
**✅ QA-2 Hypothesis HECHO (2026-07-03):** tests/test_property_based.py (9 tests, hypothesis>=6) para
parsers/detectores de texto libre. 🐛 cazó un bug REAL: `_norm_texto` hacía .lower() antes de NFKD → 𝐀
(unicode matemático) quedaba mayúscula → fix (lower después de NFKD). 141 tests pasan, CI verde. 132559b.
**✅ QA-3 ty-crítico HECHO (2026-07-03):** step "Types críticos (ty, BLOQUEA)" sobre los 5 módulos limpios
(memoria/perfil/tema_estado/decisiones/execute) — un bug de tipo nuevo ahí rompe el CI. 72 errores viejos en
el resto (mezcla de ruido de ty) → siguen informativos (QA-3b: limpiar gradual). Commit febd647.
**🎉 RONDA CI DE CONFIANZA — LOS 5 WORKFLOWS EN VERDE:** CI + CodeQL + Trivy + Scorecard + Release. Hecho:
SEC-3/4/5/6 + QA-1/2/3 + branch protection + Dependabot. Barrido exhaustivo (Brian pidió): las 18 "alertas"
de code-scanning son del propio Scorecard (no bugs; las 3 high = CodeReview/Maintained/BranchProtection NO
aplican a 1 dev). **Pendientes reales (no urgentes, nada rompe):** QA-3b (72 tipos), SEC-3b (pinear imágenes),
SEC-4b (Dockerfiles non-root), CI-2 coverage, CI-5 pip-audit. Detalle: PENDIENTES §ESTADO CONSOLIDADO DEL CI.
**✅ 2ª TANDA (2026-07-03):** CI-2 coverage (17% baseline) + CI-5 pip-audit (0 vulns, 279 deps) HECHOS ·
Dependabot 4/5 PRs mergeados (actions actualizadas + aviso Node 20 resuelto; #2 checkout se completa solo,
branch-protection lo bloqueó por rama desactualizada = protección funcionando). Los 5 workflows verdes tras
Dependabot. 🔍 barrido de HERMANOS: render tuvo 2 picos "can't start new thread" (sano ahora; sin límites de
recursos → RENDER-1 endurecer con mem/pids_limit, no urgente); resto de hermanos limpios.
**✅ 3ª TANDA (2026-07-03):** RENDER-1 ✅ (render sin límites → causaba "can't start new thread"; fix
mem_limit 1536m + pids_limit 512, verificado) · SEC-4b render ✅ (USER pwuser non-root, verificado
renderizando example.com). Reconciliados los 2 remotos tras los merges de Dependabot (todos en 23ea70a).
**✅ 4ª TANDA — LOS 3 DELICADOS HECHOS (2026-07-03):**
- **SEC-3b ✅** las 5 imágenes pineadas por SHA (verificados vía docker pull = imágenes actuales, cero cambio).
  Rebuild+E2E: guardián/KEK/migración/embeddings OK. 🐛 comentario inline en FROM rompía el parse → aparte.
- **SEC-4c ✅** agent como root ACEPTADO con justificación (.trivyignore DS-0002): el aislamiento real de
  ejecución ya lo da el sandbox hermano non-root; el agent necesita permisos amplios (modelo/KEK/guardián/
  worker). render SÍ es non-root (SEC-4b). Decisión de seguridad honesta, cero riesgo al arranque.
- **QA-3b ✅ v1** los 72 errores de ty están en solo 6 archivos; los **36 módulos limpios** ahora bloquean
  en el CI (era 5). QA-3b v2: limpiar los 6 sucios gradual.
**✅ 5ª TANDA — pendientes menores CERRADOS (2026-07-03):**
- **CI-4 ✅** README con 5 badges (CI/CodeQL/tests-141/Scorecard/License; sin coverage% que en 17% se ve mal).
- **QA-3b v2 ✅** cazó 2 bugs REALES de tipo: perfil_infer usaba `Settings()` sin args (crasheaba) →
  load_settings(); el protocolo LLMProvider.complete no declaraba `adjuntos` (multimodal) → añadido. De 6
  archivos sucios quedan 3 (telegram_channel 59, conversation 7, cache 1); ty-crítico ahora bloquea **~45
  módulos**. Queda QA-3b v3 (los 3 sucios finales, gradual, menor).
- #2 Dependabot checkout: se completa solo (branch-protection strict).
🎉 **RONDA CI DE CONFIANZA COMPLETA.** 5 workflows verdes, ~45 módulos con type-check bloqueante, release
firmado, 9 hermanos endurecidos. Cada CI cazó bugs reales. Solo queda deuda menor no urgente (QA-3b v3).

**🧭 Estado global:** cero bugs abiertos (los 11 de Brian + 4 extra cerrados). Bloques cerrados: REDISEÑO
MEMORIA · AUTO-CONCIENCIA · MULTI-INSTANCIA · EXECUTE_CODE · PRODUCTO DISTRIBUIBLE · intern-os · PARIDAD
HERMES 5/5. **Queda 1 bloque grande:** ENTRENAMIENTO (E1-E4). + 2 brechas de agente (multi-canal, cron).

---

## ⭐ (anterior, 2026-07-02) — PARIDAD HERMES COMPLETA (5/5): P1 v2 inferencia nocturna del perfil

**Contexto:** Brian: "vamos a atacar Paridad Hermes P1 (modelar al usuario)". Era la ÚNICA de las 5 que
seguía como gap real. P1 v1 (perfil declarado) ya estaba; faltaba la 2ª pasada = INFERENCIA NOCTURNA
("dialectic user modeling" de Hermes). Debate → Brian: propone+gate (no auto-aplica), OFF por defecto.

**✅ EN PRODUCCIÓN. Memoria: [[project_paridad_hermes_completa]].**
- **P1 v2** — el bot de noche OBSERVA cómo interactúa cada persona e INFIERE rasgos (rol/stack/estilo/
  zona/rasgo) → los deja como PROPUESTA con gate ✅/❌ (reusa dmn_propuestas); al aprobar se aplican al
  perfil, al descartar no. Módulo `perfil_infer.py` + `job_perfil` nocturno (03:45 Mx) OPT-IN
  (`FOR3S_PERFIL_INFER=on`, off default) + `resolver_propuesta` (dmn.py) extendido para aplicar perfil.
  OAuth-safe. 🐛 el test cazó un bug de FK (perfil_usuario→personas) → aplicar asegura la persona antes.
  Verificado E2E (parseo→propuesta→aprobar aplica→descartar no→no re-propone) + análisis de comportamiento
  (9 hermanos sanos, opt-in respetado, audit 0 rotos). Agent+worker rebuild (misma imagen).
- **🎉 LAS 5 PARIDADES HERMES CERRADAS:** P1 modelar usuario ✅ · P2 sub-agentes (H8) ✅ · P3 ejecutar
  código (EXECUTE_CODE) ✅ · P4 MCP ✅ · P5 skills (H10-12) ✅.
- ⚠️ En el SERVER (`~/for3s-os`), horneado, **SIN push a GitHub** (regla [[feedback_flujo_server_primero]]).
  Para activar P1 v2: `FOR3S_PERFIL_INFER=on` en el worker.

**🧭 Estado global:** cero bugs abiertos. Bloques cerrados: REDISEÑO MEMORIA · AUTO-CONCIENCIA ·
MULTI-INSTANCIA · EXECUTE_CODE · PRODUCTO DISTRIBUIBLE · intern-os (AI1-AI7+C1-C2-C3) · **PARIDAD HERMES
(5/5)**. **Queda 1 bloque grande:** ENTRENAMIENTO (E1-E4, NO antes de pulir todo).

---

## 🧬 (anterior, 2026-07-02) — BLOQUE intern-os COMPLETO (C1+C2+C3) + análisis de comportamiento

**Contexto (debate primero):** Brian: "vamos a atacar 6. intern-os — adoptar". El análisis previo ya
estaba hecho (`docs/analysis/Analisis_intern-os_para_For3s.md`); AI1-AI7 ya en producción (jun). Quedaban los 3
conceptos de gestión de estado de trabajo. Brian eligió: los 3, híbrido manual+auto.

**✅ EN PRODUCCIÓN. Memoria: [[project_intern_os_adopcion]]. schema BD v32.**
- **C1 · Estado operativo por tema** — migr 031 `tema_estado` + `/estado_tema` (consulta / `fase: X |
  proximo: Y | bloqueo: Z`, combina) + inyección al contexto. "Un RETOMAR.md por tema". E2E OK.
- **C2 · Registro de DECISIONES** — migr 032 `decisiones` + `/decidi <título> :: <por qué> :: <impacto>`,
  `/decisiones`, `/decision <id> superada|revertida` + detección auto "¿por qué decidimos X?" → inyecta
  el porqué (responde auto, REGISTRA solo con /decidi = no inventa). Aislado + audita. E2E OK.
- **C3 · Resolución determinista (exacto-primero)** — investigué a fondo la cascada M1-M4: la SESIÓN ya
  era exacta (M2/AI1); lo difuso era el matcher de CONCEPTOS del grafo. C3 = `_conceptos_exactos()`
  (labels nombrados LITERAL → PRIMERO y garantizados; difuso después). ⚠️ enfoque LIMPIO: query por
  PARÁMETRO, NO estado global (evité un bug de carrera concurrente que tenía mi 1er borrador). Aditivo,
  cero regresión. 9/9 casos borde + E2E grafo vivo (63 conceptos).
- **🔬 ANÁLISIS DE COMPORTAMIENTO Y ACCIÓN (pedido de Brian):** testeo profundo de la cascada completa
  (C1+C2+C3 sobre M1-M4) con hermanos + principales. TODO pasó: recordar() no rompe, panorama+C3 prioriza
  el exacto, aislamiento C1/C2, **8 recordar() en PARALELO sin carreras**, audit íntegra (1783 ev, 0
  rotos), 9 hermanos sanos (sandbox /health 200, MCP conectado).
- **✅ FIX nombre del dueño (a raíz del análisis):** el DUEÑO tenía `nombre=NULL` (set_owner_bd nunca lo
  escribía). FIX captura automática: set_owner_bd(nombre) con COALESCE + on_start pasa full_name +
  `_curar_nombre_persona` en _autorizar (rellena si NULL con el full_name de Telegram). Nunca inventa, no
  pisa, fail-safe. E2E OK. La fila de Brian se cura SOLA en su próximo mensaje (no se tocó a mano).
- ⚠️ En el SERVER (`~/for3s-os`), horneado, **SIN push a GitHub** (regla [[feedback_flujo_server_primero]]).

**🧭 Estado global:** cero bugs abiertos. Bloques grandes cerrados:
REDISEÑO MEMORIA · AUTO-CONCIENCIA · MULTI-INSTANCIA · EXECUTE_CODE · PRODUCTO DISTRIBUIBLE · **intern-os
(AI1-AI7 + C1-C2-C3)**. **Queda 1 bloque grande:** ENTRENAMIENTO (E1-E4, NO antes de pulir todo).

---

## 📦 (anterior, 2026-07-02) — BLOQUE PRODUCTO DISTRIBUIBLE COMPLETO (P1-P10, 10/10)

**Contexto (debate primero):** Brian: "vamos a atacar PRODUCTO DISTRIBUIBLE (P1-P10)". Al debatirlo se
vio que **8 de los 10 YA estaban hechos** por bloques posteriores (P1-P10 se escribieron el 2026-06-23,
ANTES de construir PRE-TESTERS/MULTI-INSTANCIA/AUTO-CONCIENCIA/EXECUTE_CODE). Brian eligió: "solo atacar
las 2 brechas reales (P4+P7) y marcar los otros 8 como ✅".

**✅ EN PRODUCCIÓN. version.py subió a v0.14.0 "PRODUCTO DISTRIBUIBLE". Memoria: [[project_producto_distribuible]].**
- **8 ya cerrados:** P1/P2/P3/P9/P10 (PRE-TESTERS: repo instalable+AGPL+wizard+compose) · P5 (AUTO-CONCIENCIA:
  /introspeccion,/soy,/modificar con líneas rojas) · P6/P8 (EXECUTE_CODE: sandbox+workspace persistente, pip/npm).
- **P4 · self-version-awareness → HECHO.** version.py ya era la fuente única (AI5 cerró P4+G4). Brechas cerradas:
  (P4.a) changelog al día → v0.14.0 con los 4 bloques nuevos; (P4.b) **changelog VIVO** = `auto_cambios_recientes()`
  + `formatear_auto_cambios()` leen `diario_cambios` (origen='propio', migr 030) → cuando el agente se
  auto-modifica (AC3) lo REPORTA en su versión, SIN reescribir el archivo fábrica (respeta el guardián).
  Cableado en conversation.py + telegram_channel.py. **Verificado E2E contra BD viva** (insert→leer→limpiar,
  0→1→0 PASS) + rebuild + recreado (arrancó SANO: `[guardian] core restaurado`, `[AC1] detecté 3 cambios`).
- **P7 · encarpetado → HECHO.** `ESTRUCTURA.md` en la raíz del repo: mapa de directorios + tabla "¿dónde pongo
  mi archivo nuevo?" (módulo→for3s_core, migración→migrations/NNN, comando→telegram_channel, servicio→docker/…).
- **NO parte de P1-P10 (quedan en §EXTRAS):** DIST-1..5 (probar curl|sh en Linux limpio, dominio+landing,
  v1.1 hermanos en instalador, monetización).
- ⚠️ Hecho en el SERVER (`~/for3s-os`), **SIN push a GitHub** (regla [[feedback_flujo_server_primero]]).

**🧭 Estado global:** cero bugs abiertos. Bloques grandes cerrados: REDISEÑO MEMORIA · AUTO-CONCIENCIA ·
MULTI-INSTANCIA · EXECUTE_CODE · **PRODUCTO DISTRIBUIBLE**. **Queda 1 bloque grande:** ENTRENAMIENTO
(E1-E4, absorber 6 agentes, NO antes de pulir todo) + deuda no-urgente (H9/H10) + §EXTRAS (14 diferidos).

---

## 🛠️ (anterior, 2026-07-02) — BLOQUE EXECUTE_CODE COMPLETO (EC-1..EC-4) + Foresito reconoce lo nuevo

**Contexto (modo debate primero):** Brian preguntó dónde darle al agente la capacidad de "hacer código,
instalar, crear archivos, correr código" — analizamos Hermes (Nous). Decidió: paridad Hermes en
`execute_code` — For3s escribe código → lo EJECUTA en un SANDBOX aislado → responde; instala libs; crea
proyectos; **actúa solo**; TODO dentro de su caja (sandbox SEPARADO, hermano de red, respeta sin-DinD).

**✅ EN PRODUCCIÓN. Diseño: `Cuerpo/Ronda_Execute_Code_Plan.md`. Commits 66d165a·3c595ca·6c43e4a·6abd82c·8f31e00.**
- **EC-1** hermano `for3s-sandbox` (imagen ligera 111MB: python/bash/node, usuario sin privilegios) +
  servidor HTTP `/run` con límites del SO (RLIMIT_CPU/AS/NPROC, sin docker run = sin-DinD). 🐛 cazado:
  Node muere con RLIMIT_AS bajo (V8 CodeRange) → fix `--max-old-space-size`.
- **EC-2** al compose como hermano permanente + **workspace PERSISTENTE** (volumen) + instalar deps
  (pip/npm). 🔒 red ABIERTA (decisión de Brian: es su agente, aislado del host).
- **EC-3 (estrella)** tool `execute_code` en el tool-loop + detector `huele_a_codigo` + `usa_tools =
  huele_a_github OR huele_a_codigo`. **Verificado E2E con LLM real:** "cuenta primos 1-100 ejecutando
  código" → el modelo llamó execute_code → el sandbox corrió → respondió 25. Foresito es agente-desarrollador.
- **EC-4** un sandbox por instancia (multi-instancia, workspace aislado por `-p`) + `/salud` VIGILA el
  sandbox. Pruebas rigurosas: 4 hermanos ✅ por /salud; 🐛 cazó render degradado (reiniciado); aislamiento
  cruzado verificado (2 instancias, workspaces no se cruzan); sin huérfanos; Foresito intacto.
- **🧠 FOR3S_ROLE actualizado (commit 8f31e00):** Foresito ya reconoce TODO lo nuevo (execute_code,
  auto-conciencia, auto-modificación, memoria en cascada, multi-instancia) — antes "ocupaba el roll viejo"
  (declaraba hasta APRENDE + sandbox como "linter ruff"). Verificado en vivo: listó sus capacidades nuevas.
- **Diferido a §EXTRAS:** EC-EXTRA-1 backend LOCAL/SSH/cloud (sale de la caja al host/otra máquina).

**🧭 Estado global:** cero bugs abiertos. Bloques grandes cerrados: REDISEÑO MEMORIA · AUTO-CONCIENCIA ·
MULTI-INSTANCIA · **EXECUTE_CODE**. Foresito = agente-desarrollador que se conoce, se auto-modifica,
ejecuta código en sandbox, y corre como varias instancias aisladas. **Queda 1 bloque grande:**
ENTRENAMIENTO (E1-E4, absorber 6 agentes) + deuda no-urgente (H9/H10) + §EXTRAS (14 diferidos).

---

## 🏢 (anterior, 2026-07-02) — BLOQUE MULTI-INSTANCIA COMPLETO (MI-1 + MI-2 + MI-3)

**Contexto (modo debate primero):** Brian quería correr VARIOS For3s OS aislados en su máquina (uso
personal + clientes). Aclaró: gestor LOCAL (NO SaaS remoto), comando `for3s` con menú (agregar / entrar
= chat de consola de esa instancia / encender-apagar / borrar), aislamiento TOTAL, solo las encendidas,
unido al instalador. Construido fase por fase con "sé curioso + encuentra bugs".

**✅ EN PRODUCCIÓN. Diseño: `Cuerpo/Ronda_Multi_Instancia_Plan.md`. Commits firmados 7a71e55·61df2cf·cc87f7d.**
- **MI-1 gestor `for3s`** (script del HOST): listar · agregar (wizard: token Telegram + dueño + KEK auto +
  token Claude heredado) · entrar (chat de consola) · encender/apagar · borrar. Orquesta `docker compose
  -p for3s-<nombre>` con la PLANTILLA `docker-compose.instancia.yml` (NO toca el compose de Foresito).
  Estado por instancia en `~/.for3s/<nombre>/`. El agente NO toca Docker (el gestor vive en el host, sin-DinD).
- **MI-2 modo bot** verificado (token→bot, vacío→modo solo consola) + validación del token Telegram (getMe)
  antes de crear.
- **MI-3** el comando `for3s` nace con el instalador (install.sh lo pone en el PATH; uninstall.sh baja
  TODAS las instancias for3s-* + quita el comando).
- 🔍 **7 bugs cazados por curiosidad:** 5 hardcodeos de aislamiento en el compose (name de proyecto fijo ·
  red for3s_net fija · puerto Grafana 3000 · 2× mounts de estado) → plantilla parametrizada; + 2 en vivo
  (KEK debe ser 32 bytes crudos no base64 · token inválido dejaba loop → validación previa).
- **Verificado E2E:** instancia `testmi` creada aislada → su Postgres/KEK/estado SEPARADOS de Foresito
  (escribir en una NO aparece en la otra) → `for3s entrar` respondió en su chat → `for3s borrar` limpió
  todo → **Foresito INTACTO (714 turnos) durante TODO el proceso.** Aislamiento total confirmado.
- **Diferido a §EXTRAS:** MI-EXTRA-1 SaaS remoto multi-tenant · MI-EXTRA-2 ⭐ botón WEB encender/apagar.

**🧭 Estado global:** cero bugs abiertos. Cerrados hoy/ayer: REDISEÑO MEMORIA (F1-F5+M1-M4, sin deuda) ·
AUTO-CONCIENCIA (AC1-AC4+guardián) · MULTI-INSTANCIA (MI-1-3). **Quedan 2 bloques grandes:** ENTRENAMIENTO
(E1-E4) y PRODUCTO DISTRIBUIBLE (P1-P10) — ambos con Ronda/debate primero. §EXTRAS = 13 diferidos.

---

## 🧠 (anterior, 2026-07-01) — BLOQUE AUTO-CONCIENCIA + AUTO-MODIFICACIÓN COMPLETO (AC1-AC4 + guardián)

**Contexto:** Brian abrió este bloque en modo DEBATE primero (él expresa la visión, yo escucho y debato, luego preguntas). Decidió: el agente se auto-modifica DENTRO de su caja (contenedor local, NUNCA GitHub), ACTÚA SOLO (control estructural, no permiso paso a paso), + agregó el ENTORNO DE PRUEBA (probar antes, aplicar solo si pasa). Construido fase por fase con "sé curioso + experimenta + encuentra bugs" — cazó bugs reales antes de que explotaran.

**✅ EN PRODUCCIÓN — las 4 fases + guardián. Diseño: `Cuerpo/Ronda_Auto_Conciencia_Automod_Plan.md`.**
- **AC2** introspección — se conoce EN VIVO (módulos/tablas/migr/skills/comandos/jobs). `/introspeccion` (`/soy`) + auto en el chat ("¿cómo estás construido?"). Mejora AI5 (era estático). 🐛 cazó: la columna era `lifecycle` no `estado` (habría reportado "0 skills"=mentira).
- **AC1** auto-detección — al arrancar hashea su código y detecta SOLO qué cambió, distingue 🔧'yo lo cambié' vs 📥'me lo cambiaron desde fuera'. Diario (`/cambios`, migr 030 tabla diario_cambios). Verificado en vivo (toqué un archivo, lo detectó y clasificó).
- **AC3** auto-mod CÓDIGO — `/modificar <mod>: <qué>` (solo dueño) edita su código LOCAL. Red: líneas rojas (nunca governor/audit/KEK/automod) + ⭐ENTORNO DE PRUEBA aislado 3 capas (sintaxis→import→smoke) + punto de guardado + overlay persistente + `/revertir`. 🐛 cazó: el import solo no basta (módulo vaciado importa OK pero rompe→hizo falta el smoke); el scanner del governor da falsos positivos con código (bloqueaba por mencionar 'KEK')→se quitó. E2E con LLM real: se auto-modificó de verdad, siguió sano.
- **GUARDIÁN de arranque** (`docker/entrypoint.sh` + `/app/factory`) — si una auto-mod rompe el arranque → cuarentena + restaura de fábrica + avisa al dueño. Rompe el LOOP DE MUERTE. 🐛 cazó: el código es COPY (no pip -e)→no había copia de fábrica→se horneó /app/factory. Probado en vivo: overlay roto→recuperado+avisó.
- **AC4** auto-mod BD — `/modificar_bd <SQL>` (solo dueño). La más delicada (toca DATOS). Red: líneas rojas (audit/owner/secrets/schema_version) + solo DDL aditivo + BACKUP obligatorio + dry-run (tx+rollback). 🐛 clave: un DROP COLUMN pasa el dry-run pero borra datos→backup obligatorio. 13/13 + 6/6 evasiones bloqueadas + producción (modificó su BD con backup real).

**Doble red:** entorno de prueba (PREVIENE) + guardián (RESCATA). Introspección ahora reporta 53 módulos/31 comandos = **el agente se ve a sí mismo con las capacidades nuevas** (auto-conciencia real).
**Commits firmados en GitHub (oficial+privado):** a5b1a14·029cb8e·8b7a800·2496355·1eaccfd.
**Forma de trabajo del bloque (LOCKED):** DEBATE primero → preguntas → construir. Brian: "primero pregúntame si estoy listo para las preguntas".

---

## 🧠 (anterior, 2026-07-01) — REDISEÑO DE MEMORIA COMPLETO + F5 temas de equipo + limpieza de pendientes

**Contexto:** Brian: "existen tantos errores porque todo se hizo por separado; no es un sistema que pueda estar como producto. Analiza todo y determinemos un plan." → Ronda de diseño (`Cuerpo/Ronda_Rediseno_Memoria_Plan.md`) + construcción completa, fase por fase, con "sé curioso con los hermanos" en cada una (destapó bugs reales antes de que explotaran).

**✅ REDISEÑO MEMORIA COMPLETO (F1-F5 + M1-M4) — EN PRODUCCIÓN.** La capa de memoria pasó de **5 silos volcados en paralelo** a **un cerebro conectado y en cascada, con 1 punto de ensamblaje**. Cierra MEM-1, MEM-2, MEM-3.
- **F1** identidad canónica (migr 026 tabla `personas`) · **F2** fachada `memoria.py` · **F3** conectar (migr 027, 4 FKs nullable + backfill 563) · **F4** precisión (cortacircuitos triviales + umbral 0.55 + re-ranking por palabra clave).
- **F5 TEMAS DE EQUIPO (camino B) + UX completa (pasos 1-5) — EN PRODUCCIÓN:** `/tema equipo <nombre>` = canal COMPARTIDO `eq:<id>:<tema>` (todos los miembros ven/escriben lo mismo, como Slack); `/tema salir` vuelve al hilo privado; `/tema equipo` lista. Piezas: `equipo_id` cableado end-to-end (Conversation + 2 puntos de escritura) · tabla `estado_persona` (migr 029) · comando con **control de acceso fail-closed** (probado: imposible ver privado de otro / saltar a otro equipo — inyección `99:hackeo` normalizada) · `_sesion_de` usa la sesión de equipo con prioridad · banner UX en `/hilos`. Bug latente cazado y cerrado: todo turno en sesión `eq:` DEBE llevar equipo_id o el miembro no lo ve.
- **M1** corte de relevancia global — el grafo trae los conceptos DEL TEMA (no 25 arbitrarios de 63); si nada aplica no inyecta; panorama puro sigue trayendo todo.
- **M2** grafo navegable (**cierra MEM-1**) — `episodios_de_concepto_con_sesion` + `turnos_por_seq` (aislado por sesión) → concepto→episodios REALES como evidencia. Enchufó las funciones huérfanas del grafo. ⚠️ Curiosidad clave: la vieja `episodios_de_concepto` devolvía seq SIN session_id (ambiguo tras BUG-19) → cablearla cruda habría re-mezclado memoria entre personas; la variante nueva preserva la sesión.
- **M3** cascada semántica→grafo — los recuerdos que la semántica destila informan QUÉ conceptos traer (mejor que la query cruda; "cli" 63→9 conceptos, "issues" 57→16). Conservador (2 recuerdos más cercanos + tope palabras + genéricas filtradas, medido con probes).
- **M4** ensamblaje único (**cierra MEM-3**) — `memoria.recordar()` ensambla la cascada de memoria (semántica→grafo→episodios) en 1 punto; `send()` la llama en 1 línea (antes ~40 líneas dispersas). **Probado por equivalencia byte-a-byte** con el código viejo (5/5) → refactor sin cambio de comportamiento.
- **Rebuild hecho** → todo horneado en la imagen, 8 contenedores sanos, `Application started`, smoke test OK.

**🗂️ LIMPIEZA DE PENDIENTES (2026-07-01):** se movieron 6 más a §EXTRAS: **DIST-1** plan de descubrimiento · **DIST-2** probar `curl|sh` en Linux limpio · **DIST-3** dominio+landing · **DIST-4** v1.1 hermanos de red en el instalador · **DIST-5** monetización Open Core · **MS-1b** arreglo FÍSICO del adaptador asix (requiere acceso físico de Brian, no urge, WiFi cubre). §EXTRAS ahora = 11 diferidos (BYOK, PR5, PR8, PR9, HA-3, DIST-1..5, MS-1b).

**✅ FUNCIONES HUÉRFANAS DE MEMORIA — TODAS CABLEADAS (2026-07-01, commit 3b001ee firmado + push):** el último grupo de "bugs" que quedaba. Verificado en vivo que los críticos ya estaban sanos (BUG-1 decay 693/702 con relevance · BUG-9 render ok · BUG-3 resuelto). Lo único real eran 4 funciones de navegación de memoria desenchufadas → CABLEADAS: `get/set_last_repo` (recuerda el repo activo por sesión → resuelve "ese repo"/"sus issues") · `repos_de_owner` + nueva `kg.owners()` ("qué repos he visto de X" desde el grafo) · `recursos_de_repo` (issues/PRs del repo activo; 0 datos hoy, lista). `episodios_de_concepto` ya se cableó en M2. Solo quedan sin cablear a propósito: `lint_archivos` (BUG-2 diferido) y `requiere_aprobacion` (no-bug). **Ninguna capacidad de navegación de memoria quedó desconectada.** E2E 4/4 + horneado + GitHub.

**🐛 ESTADO DE BUGS: cero abiertos reales.** Solo BUG-2 (diferido consciente) + deuda fina M3/M4 (con PR9).

**⚠️ TODO EN EL SERVER (repo `~/for3s-os` + horneado en la imagen) — SIN sincronizar a GitHub.** Lote grande pendiente de push (solo cuando Brian ordene, regla [[feedback_flujo_server_primero]]): migr 026/027/028/029 + `memoria.py`/`temas.py` + cambios en `conversation/kg/memory/telegram_channel`. Detalle de la Ronda: `Cuerpo/Ronda_Rediseno_Memoria_Plan.md`.

---

### (2026-06-30) 🏆 **SESIÓN MARATÓNICA** — 7/10 PR + 16 bugs + auditoría crítica + mantenimiento server.
**(LO MÁS RECIENTE 30-jun) 🚨 AUDITORÍA CRÍTICA DE ERRORES (barrido F1-F5) + 2 bugs CRÍTICOS + hallazgo MAYOR:**
- 🔴 **BUG-14 FUGA DE PRIVACIDAD (resuelto)** — el scope de memoria (`buscar_semantico`) tenía `OR owner_user_id IS NULL` → exponía los 667 turnos legado PRIVADOS del dueño a los miembros. FIX: backfill (atribuir legado a Brian) + quitar el OR NULL. Verificado: 0 fuga.
- 🟡 **BUG-15 Conflict en reinicios (resuelto)** — command `sh -c` hacía PID 1=sh (no propaga SIGTERM) → bot moría sin soltar getUpdates → Conflict. FIX: `exec python` (PID 1=python) + stop_grace_period 25s.
- ✅ **BUG-16 gate de aprobación** investigado = NO era bug (funciona E2E: miembro propone→encargado aprueba).
- 🚨 **HALLAZGO MAYOR / LECCIÓN CRÍTICA: aplicar fixes con `docker cp` es EFÍMERO.** Al recrear el agent se PERDIERON HA-1/HA-5 y **BUG-14 quedó REABIERTO en producción** (solo vivían en docker cp). REGLA: los fixes van al REPO `~/for3s-os` + REBUILD de la imagen, NUNCA solo docker cp. Se consolidó TODO en el repo + rebuild + recrear agent+worker → fixes PERMANENTES, agent=worker misma imagen (b9c5a49).
- ✅ **Deudas menores cerradas:** HA-1 (datos_equipo en /datos) · HA-1b (ultimas_corridas en /diagnostico) · HA-2 (Sme G sin perfil = no-bug) · HA-4 (.dockerignore + borrados .bak incl. .env.bak con secretos) · HA-5 (matcher skills SEMÁNTICO con embeddings + governor jaccard + migr 025) · HA-6 (GitHub E2E verificado) · HA-7 (rebuild=misma imagen). Quedan: HA-3 (H7 enrutamiento, futuro) · inconsistencia nombres de sesión (menor).
- ⚠️ **TODO EN EL SERVER, sin sincronizar al repo/GitHub.** Regla LOCKED nueva ([[feedback_flujo_server_primero]]): desarrollar+probar en el server; repo local + push SOLO cuando Brian lo ordene. Lote grande pendiente de sincronizar: HA-1, HA-1b, HA-5, BUG-14, BUG-15, HA-4, migr 025.

**(30-jun) ✅ PROFESIONALIZACIÓN 7/10:** PR1·PR2·PR3·PR4·PR6·PR7·PR10 HECHOS. Hoy se cerraron:
**(A) ✅ PR6 DUEÑOS** (owner en BD = fuente de verdad, cierra BUG-4 el último bug grave + transferencia ATÓMICA owner+encargado, previno un bug latente de desincronización). **(B) ✅ PR3 DATOS/ANALÍTICA** (`analytics.py` + `/datos`: actividad/consumo/repos/capacidades/por-persona; ⭐ datos HONESTOS — la auditoría profunda evitó un dato FALSO: repos inflados x5 porque gh_resources tiene 1 fila por archivo → se cuenta por sesiones distintas; avisa de lo no medido). **(C) ✅ PR7 REVISIÓN DE HITOS** (`memory/archive/PR7_Revision_Hitos.md`: los 12 hitos verificados EN CONTENEDOR VIVO, filosofía "completo en código ≠ funciona en el contenedor". **12/12: 11 ✅ funcionan, H7 🟡 parcial por diseño, 0 rotos.** ⭐ cadena audit ÍNTEGRA 1576 eventos/0 rotos. H5 grafo creció 35→63 conceptos. H12 tiene 1 skill AUTO-generada por el DMN en uso. **Cazó 6 deudas registradas como HA-1..HA-6 en PENDIENTES** "ANÁLISIS DE LOS H": HA-1 equipo multiagente sin audit (no se mide su costo) · HA-2 Sme G miembro sin perfil_usuario · HA-3 H7 enrutamiento auto no construido (futuro) · HA-4 ~10 .bak en la imagen · HA-5 2 skills deploy duplicadas · HA-6 GitHub sin uso reciente (prueba humo). Ninguna ROMPE; se atacan una por una). **(D) ✅ MS-1 MANTENIMIENTO SERVIDOR** (ver abajo). **(E) ✅ PR9.0 SINCRONIZACIÓN DEL REPO DE LA VERDAD** (al arrancar PR9, la curiosidad destapó que TODO el trabajo de la semana —PR2/3/6/10 + 12 bugs— vivía SOLO en el contenedor; el repo `~/for3s-os` estaba `[ahead 34]` sin pushear; los 2 contenedores agent/worker desincronizados. → repo LOCAL + SERVER + GitHub sincronizados; **35 commits FIRMADOS** con la clave GPG de Brian pusheados a `github.com/fruterito101/for3s`, commit `5b91f59`. Si el server muere ya NO se pierde nada. HA-4 .bak resuelto de paso). **QUEDAN 3 PR:** PR5 datos-empresa (necesita más usuarios) · PR8 entrenamiento (NO antes de pulir) · PR9 lo grande = dividir telegram_channel ~3328 L (refactor delicado, sesión dedicada) + HA-1 audit del equipo.
**🛡️ HALLAZGOS DE SEGURIDAD (PENDIENTES §SEGURIDAD) — AMBOS CERRADOS:** **SEC-1** token GitHub `gho_...` expuesto en `git remote -v` del server → ⛔ **Brian decidió NO rotar (riesgo ACEPTADO, cerrado — NO reabrir).** **SEC-2** ✅ Dependabot RESUELTO (commit `32f68db`): era pydantic-settings (no usamos la función vulnerable; el contenedor ya corría 2.14.2, solo el uv.lock estaba en 2.14.1 → alineado + certifi al día). 🔍 Auditoría de HERMANOS: 7 contenedores sanos, MCP read+write 21 tools, render OK, sin más vulns. Cazó **HA-7** (agent y worker corren imágenes distintas — rebuild worker algún día, no rompe).
**(ANTERIOR, mismo bloque) 🐛✅ SESIÓN MAYOR DE BUGS + PR2 MONITOREO** — la más productiva de saneamiento.
**(0) 🐛 9 BUGS RESUELTOS (PR4-A, todos verificados E2E):** auditoría "mirar lo que nadie mira" destapó que la CONTENERIZACIÓN rompió cosas EN SILENCIO. 🔴 BUG-5/6 backup roto (faltaba pg_dump → sin respaldos; FIX postgresql-client + volumen) · 🔴 BUG-8 CLS consolida 0 (catálogo AGE corrupto post-restore graphid 19195≠OID; FIX reparar ag_graph+ag_label) · 🔴 BUG-1 decay muerto (relevance nunca al cron; FIX job_relevance 02:45 todas las sesiones) · 🔴 BUG-9/9b GitHub MCP + render rotos (el bot hacía docker run sin DinD; FIX "HERMANOS DE RED" = github-mcp read+write + render como servicios HTTP del compose, mcp_client/web_fetch a HTTP) · BUG-3 16 huérfanos soft-deleted · BUG-2 sandbox diferido · BUG-10 embeddings no precargaban (snapshot partido + HF online + .no_exist; FIX offline). ⭐ Mejora raíz: Dockerfile modelo en caché local (builds 25s). Server se reinició → 7 contenedores revivieron solos. Memoria: project_pr4a_bugs_memoria.
**(0b) ✅ PR2 SALUD/MONITOREO COMPLETO** (solo falta PR2.3 Grafana, futuro): `/salud` end-to-end (línea mensaje→memoria + subsistemas + grafo + integraciones + nocturno + TOKENS por persona + hilos) + `/salud <sección>` + tabla cron_corridas (migr 023, timestamp) + @registra_corrida en 7 jobs + 🚨 ALERTA AUTOMÁTICA al dueño por Telegram si hay 🔴 fallas (job_health_check 04:30, cero spam, verificado E2E). El círculo cerrado: un subsistema roto YA NO pasa en silencio. Memoria: project_pr2_monitoreo.
**(0c) ✅ PR10 SOPORTE/AUTO-DIAGNÓSTICO COMPLETO** ("el usuario no depende de Brayan"): `/ayuda` (todos, por rol + primer auxilio) · `/diagnostico` personal (cada quien lo suyo) · `/reconectar` (auto-recuperación de integraciones, dueño) · on_error que AVISA en errores no-red. Cazó BUG-12 (/estado bloqueado) y BUG-13 (fuga de privacidad en /diagnostico). Total sesión: **11 bugs resueltos**.
**(0d) ✅ MANTENIMIENTO SERVIDOR RESUELTO (30-jun):** la red del server salía SOLO por el adaptador asix inestable (cortaba builds/SSH/envíos). FIX: activado el **WiFi Intel 8260 como salida PRINCIPAL** (estaba bloqueado por RF-kill; desbloqueado + netplan + persistente; metric 600, el tráfico YA va por WiFi → la red NO depende del asix) + fixes a fondo del asix (autosuspend off + udev persistente). Lo único que QUEDA es FÍSICO (Brian, acceso físico): cambiar cable / reemplazar adaptador asix (sigue Link detected:no = cable/hardware degradado). NO urge: el WiFi cubre. Memoria: project_mantenimiento_servidor.
**Estado actual: 7 contenedores sanos** (agent, worker, postgres, valkey, github-mcp, github-mcp-write, render). Foresito contenerizado, monitoreado, auto-alertado, CON SOPORTE de usuario, resiliente a reinicios. **version.py = v0.13.0 / PROFESIONALIZACIÓN** (actualizado 30-jun, /version lo reporta).
**⛔ REGLA CRÍTICA NUEVA (30-jun, incidente de cuota):** NUNCA bucles de espera largos ni procesos de fondo contra el servidor inestable (MS-1) — consumieron cuota sin que Brian hiciera nada → session limit con 60% usado. Si un comando al server falla por red al 1er intento → PARAR y dejar pendiente, NO reintentar en loop. Memoria: feedback_no_loops_espera_servidor.
**Anteriores (2026-06-28):** 📦🔄🚨 **DISTRIBUCIÓN + MIGRACIÓN + PROFESIONALIZACIÓN** — tres hitos grandes encadenados:
**(1) 📦 FASE PRE-TESTERS / DISTRIBUCIÓN COMPLETA (2026-06-27):** For3s OS pasó de "corre en el server" a "un tester lo instala en su Linux con `curl|sh`". 8 componentes (identidad limpia · docker-compose 4 servicios con Postgres-AGE-pgvector HORNEADOS + imagen agente 9.63GB con BGE-M3 horneado, SIN DinD = "contenedores hermanos" idea de Brian · instalador+wizard+uninstall+KEK auto · repo público+README+TESTING). v1 = núcleo (Opción B); GitHub-MCP/render → v1.1 hermanos. Plan: Cuerpo/Fase_PreTesters_Plan.md. Memoria: project_fase_pretesters.
**(2) ⚖️📦 REPO OFICIAL PÚBLICO + LICENCIA (2026-06-27):** `github.com/fruterito101/for3s` = **EL REPO DE LA VERDAD** (regla LOCKED: cada actualización YA VERIFICADA se sube ahí). Tu código H5→H12+DMN+metacognición, que solo vivía en el server, ahora respaldado. AGPL-3.0 + NOTICE copyright Brian Jovany López Pérez + 46 headers + commits firmados GPG + release v0.1.0 firmado = autoría indiscutible. Gobernanza completa EN inglés. CI verde + secret scanning + push protection. Memoria: project_repo_oficial_for3s.
**(3) 🔄 MIGRACIÓN DE FORESITO A CONTENEDORES — EXITOSA (2026-06-28):** Foresito (el For3s de producción de Brian en Telegram) corría SUELTO con systemd → migrado a contenedores conservando TODA su memoria (738 turnos + grafo AGE 559 Episodios/54 Conceptos + secrets vía KEK). 5 fases con backup verificado + rollback. 🐛 BUG cazado/resuelto: el `telegram_owner.json` vive en `/app/.for3s` (no montado) → el bot no reconocía al dueño → mensajes a sesión vacía. FIX: montar `~/.for3s`→`/app/.for3s`. La memoria NUNCA estuvo en riesgo. Verificado en vivo (recuerda 15/22/25/27 jun + "pizza 🍕"). Sme G (miembro) intacta. ✅ Fase 5 cerrada (systemd viejo disabled, rollback preservado, contenedor con restart auto). **MIGRACIÓN 100% COMPLETA.** Plan: Cuerpo/Migracion_Foresito_Contenedores_Plan.md.
**(4) 🚨 FASE PROFESIONALIZACIÓN identificada (CRÍTICO, lo siguiente grande):** For3s *funciona* pero NO se gestiona como producto. 10 frentes PR1-PR10 en PENDIENTES §PROFESIONALIZACIÓN: PR1 claridad código · PR2🔴 salud/monitoreo · PR3🔴 datos/analítica · PR4🔴 bugs memoria+auditoría archivo×archivo · PR5 datos empresa · PR6🔴 dueños (frágil, lo probó la migración) · PR7 revisar cada H · PR8 entrenamiento/importar 2 agentes · PR9 UX producto · PR10🔴 comandos soporte. Orden sugerido: PR4+PR1 → PR2 → PR10 → PR3/PR5 → PR6 → PR7 → PR8 → PR9. NADA de golpe. Memoria: project_profesionalizacion.
**Anteriores (íntegros):** 🧠 **H10-PLANEA "METACOGNICIÓN" v1 COMPLETO** — "sé cuándo NO sé": el agente mide su confianza antes de afirmar; si duda, lo dice/pide aclaración en vez de inventar. confidence.py (5 niveles + 8 señales R6: reales llm_self_report/tool_success/schema_valid/historical, 4 neutras honestas que no diluyen, ⭐regla de tope: la duda del modelo es el techo del score) + integración conversation.send paso 3b (baja conf→nota tentativa) + FOR3S_ROLE METACOGNICIÓN. Test 16/16 (cazó bug calibración). version.py **v0.12.0 (HITO H10 PLANEA)**, bot activo. Plan+cierre: Cuerpo/H10_PLANEA_Plan_Maestro_Metacognicion.md. Deuda HP1-HP6 en PENDIENTES. ⚠️ ojo numeración: este es "H10 PLANEA" del mapa (PFC), distinto de H10-12=APRENDE/skills. **Anterior:** 🌙 **H9 "SUEÑA" (DMN) COMPLETO** — For3s trabaja solo cuando estás inactivo. 4 fases: H9-a motor (dmn.py + migr 021 dmn_estado/dmn_corridas, idle detection real, 2 jobs Arq nocturno 04:00 + idle cada 30 min, /dmn) · H9-b 5 housekeeping (dmn_tasks.py: embedding_precompute REAL embebió 17, memory_consolidation REUSA CLS H6, eval_regression métrica; cache+routing stubs honestos) · H9-c 3 generativas (+migr 022 dmn_propuestas: pattern REUSA proponer_skill_auto H12, hypothesis Opus→propuesta, prompt_improvement stub=AC3; triple freno generativas_on OFF default+solo_noche+governor; /dmn propuestas botones ✅/❌) · H9-d ROI (/dmn roi keep/revisar). Tests 13+18+17+7. **BD v22, version.py v0.11.0 (HITO H9 SUEÑA), bot+worker activos.** ⚠️ housekeeping ON / generativas OFF (no se mejora solo hasta /dmn generativas on). Plan+cierre: Cuerpo/H9_SUENA_Plan_Maestro_DMN.md. 📌 También: registrado pendiente mayor AUTO-CONCIENCIA AC1-AC4 (memoria project_auto_conciencia_automod). **Anterior:** 🎉 **H10-H12 "APRENDE" COMPLETO** — la "joya" de Hermes adaptada a CÓDIGO PROPIO: For3s crea, gobierna y cura sus propias skills. **✅ H10 SKILLS** (migr 019 + skills.py SkillStore + el agente aplica la skill al contexto + /skills). **✅ H11 GOVERNOR** (el FRENO): migr 020 (governor_estado kill switch default OFF + governor_bloqueos) · governor.py SkillEcosystemGovernor = SCANNER ~17 regex FAIL-CLOSED + FRENO 1 gen≤3/día + FRENO 4 no-duplicar + FRENO 5 ≤100 + HOOKS honestos 2/3/6 + PROVENANCE + GATE evaluar_skill_nueva + /autogen on|off|status. Test 24/24. **✅ H12 APRENDE** (el MOTOR, módulo aprende.py): P1 `/aprende` destila SKILL.md de la conversación → governor → SkillStore (LLM real 10/10) · P2 auto-mejora background (provenance auto, si /autogen OFF ni llama al LLM; si pasa nace en stale + GATE al dueño botones ✅/❌; disparada tras corrida de equipo; 10/10) · P3 curación nocturna job Arq 03:30 (auto sin uso active→stale 30d→archived 90d, recuperable, intocables usuario/pinned/usadas; 8/8). **BD v20, version.py v0.10.0 (HITO H12 APRENDE), bot+worker activos (6 jobs/5 crons).** ⚠️ Auto-gen sigue OFF por defecto: H12 da la capacidad, el dueño la enciende con `/autogen on`. Decisiones LOCKED: P1→P2→P3 por riesgo · fuente=conversación · P2 tras kill switch OFF. Plan: Doc/H10-H12_Plan_Maestro_APRENDE.md. ✅ **VERIFICADO E2E EN VIVO 2026-06-25** (Brian en Telegram, trazabilidad mensaje por mensaje): H11 kill switch + /aprende(skill #20) + auto-mejora(skill #21→gate aprobado) + H10 uso real (contador 0→1 prueba limpia) + 🔧 FIX personalidad (agent.py reconoce H10-12: "Sí, aprendo"). Detalle: Cuerpo/H10_H11_H12_APRENDE_Referencia_Tecnica.md §6.bis. 📌 3 deudas: matcher por palabras (no semántico) · FRENO 4 exact-match (duplicado semántico pasa) · /aprende+gate sin audit chain. Anteriores: 🎉 MVP + 🧠 H5 + 🌙 H6 + 🤝 H8 + pulido H8 (AI1-AI7 código propio, CERO refs externas).)
**Mantenido por:** Claude (actualizar al cierre de cada sesión importante)

---

## 1. Quién + qué (10 segundos)

- **Brian López** (founder, NO "Aguilar"). Email ema@frutero.club.
- **Proyecto:** For3s OS — plataforma/agente "segundo cerebro" universal (11 nodos cerebrales + 3 pilares).
- **Trabajamos en:** `/home/brianweb3/for3s/Mente/` = **"Mente OS"**. NO tocar `marca-personal/Mente/`.
- **Fuente de verdad arquitectónica:** `Cerebro/For3s_OS_Grafo_Maestro.md`.

## 2. Dónde quedamos (estado vigente)

```
🏆 DISEÑO 100% LOCKED (R1-R10) + auditoría + 3 refuerzos pre-código (2026-06-09)
🎉 ✅✅✅ MVP CERRADO (2026-06-19) — decisión de Brian tras pruebas en vivo + auditoría de salud.
   C0·C1·H1 HABLA·H2 RECUERDA·H3 TELEGRAM·H4 TIENE MANOS + pulido profundo (15-19 jun).
   Bot en producción: sonnet-4-6 OAuth, token cifrado KEK, BD migraciones v6, 128 tests verdes,
   audit chain íntegra (718 entradas verificadas). Respaldo del cierre:
   Doc/Auditoria_Salud_MVP_2026-06-19.md + Doc/Changelog_Pulido_MVP_2026-06.md.

🧠 ✅ H5 "MEMORIA REAL" COMPLETO (2026-06-20) — 1ª fase post-MVP. Doc técnico completo +
   5 reglas de AGE: Doc/H5_Infra_Memoria_AGE_pgvector.md. Lo construido (8 sub-pasos):
   ✅ pgvector 0.8.2 + Apache AGE 1.6 (grafo for3s_kg) + embeddings BGE-M3 (NO Stella —
      multilingüe español+código; Stella daba bugs en CPU y era solo-inglés). schema v7.
   ✅ MEMORIA SEMÁNTICA: el bot busca por SIGNIFICADO en todo el historial (no solo 12 turnos).
      memory.buscar_semantico + columna embedding(1024)+HNSW + backfill de los 438 turnos.
   ✅ KNOWLEDGE GRAPH (kg.py): registra/navega repos·owners·issues·PRs; se puebla al leer GitHub.
   ✅ INTEGRADO al bot: recuerdos al contexto (A) + cada turno nuevo se embebe en background,
      TODOS los flujos (B/B-ext) + grafo se puebla (C). Modelo precargado al arranque.
   ✅ AFINADO: solo_usuario=True cortó un bucle de auto-confirmación; el bot ya NO infla.
   ⚠️ BGE-M3 en CPU es LENTO (~3s/turno, carga ~160s) → todo embedding es BACKGROUND, modelo
      precargado 1 vez. ⏳ Pendiente menor "H5-mem-matiz" (PENDIENTES.md): juicio del bot sobre
      "qué cuenta como haber hablado de un tema". H6 (CLS) llenará el grafo automáticamente.

🌙 🔄 H6 "SE CUIDA" — 11/13 SUB-PASOS (2026-06-20) — 2ª fase post-MVP. Memoria que se
   mantiene sola de noche: CLS consolida episodios→conceptos al grafo + Microglía olvida ruido
   viejo ya consolidado (soft-delete recuperable, NUNCA toca audit). Plan de obra SUPER detallado:
   Doc/H6_Plan_Maestro_SE_CUIDA.md (tiene tabla de estado + hallazgos). **MÁS DELICADO que H5
   porque BORRA datos** → cada sub-paso: backup→construir→verificar aislado→OK Brian→tests.
   ✅ S0-S3 infra: backup pre-H6 (restauración verificada) · scheduler Arq (Valkey db1, cache en db0)
      · migración 008 schema v8 (soft-delete recuperable, memory.py filtra borrados) · relevance+decay.
   ✅ S4-S7 MOTOR CLS COMPLETO: clustering HDBSCAN + concepto (sonnet-4-6) + escritura al grafo +
      orquestador (anti-429: provider único+pausa 3s+tope). **Consolidación masiva ya corrida: grafo
      0→35 conceptos / 390 episodios. Quedan 15 = ruido (no consolidable). Audit íntegro (792).**
   ✅ S8-S9 MOTOR MICROGLÍA COMPLETO: evaluar_candidatos (3 condiciones, solo SELECT) + olvidar
      (DOBLE CANDADO confirmar=True, soft-delete recuperable, tope 50, audita) + recuperar().
      Verificado en transacción con rollback (0 datos reales tocados). ⛔ nunca hard-delete/audit.
   ✅ S10 CRON nocturno: tasks.py jobs job_cls (08:00 UTC=2AM Mx) + job_microglia (09:00 UTC=3AM Mx,
      DRY-RUN por env FOR3S_MICROGLIA_CONFIRMAR=false). Server en UTC. Jobs verificados a mano.
   ✅ S11 BACKUP 3-2-1 foundation: backup.py (pg_dump verificado + rotación últimos 14, no toca
      manuales) + job_backup nocturno (07:00 UTC=1AM Mx, antes de CLS). ⏳ off-site pendiente.
   ✅ S12 PRUEBA NOCTURNA + CIERRE: simulación de la noche completa E2E (backup→CLS→Microglía
      dry-run vía worker). Audit íntegro (794), 0 borrados, 35 conceptos, 128 tests. Microglía
      dry-run ahora deja evento en audit. 🎉 **H6 COMPLETO 13/13.**
   ⏱️ CRON NOCTURNO ACTIVO: 01:00 backup · 02:00 CLS · 03:00 Microglía (hora México).
   🔴 OLVIDO REAL ACTIVADO (2026-06-20): FOR3S_MICROGLIA_CONFIRMAR=true. Microglía YA borra
      (soft-delete recuperable) de noche. Seguro hoy (0 candidatos = datos recientes); empezará
      a podar cuando haya episodios >30d + relevance<0.3 + consolidados. Tope bajado a 20/noche.
      ⚠️ Fix: el worker NO heredaba el .env por systemd → tasks.py hace _load_dotenv() al importar.
      ⏳ off-site del backup PENDIENTE — activar antes de que haya candidatos reales.
   ⚠️ HALLAZGO CLAVE (resuelto): el 429 del OAuth NO es siempre rate-limit — el OAuth RECHAZA
      system prompts custom (falso "429 Error"). Fix: instrucción en user message, system="". Tarea
      pendiente de revisar en flujos GitHub: PENDIENTES.md "429-system-prompt".
   Decisiones LOCKED: CLS=sonnet-4-6 (env FOR3S_CLS_MODEL) · Microglía arranca DRY-RUN varias
   noches antes de borrar real (cambiar FOR3S_MICROGLIA_CONFIRMAR=true cuando Brian dé OK).
   Pendientes menores: H6-formula-relevance (Brian define fórmula afinada) + H5-mem-matiz.

   CAPACIDADES (MVP + H5, todo verificado en vivo):
   ✅ Chat con MEMORIA persistente (Telegram+CLI) + MEMORIA SEMÁNTICA (busca por significado) ← H5
   ✅ ANÁLISIS de repos GitHub: 2 modos (SIMPLE/PROFUNDO) + por categorías + recencia + ficha + orgs
   ✅ CONTEOS exactos (search_* → total_count en 1 llamada, 4206 PRs cli/cli verif)
   ✅ WRITE TOOLS seguras: comentar/crear issue/PR/review con botón ✅/❌ + whitelist dura
      (rechaza merge/delete/push) + contenedor MCP write efímero + audit github_write. Lectura read-only.
   ✅ MULTIMODAL: imágenes + PDF + Word + Excel (audio descartado por recursos)
   ✅ WEB FETCH híbrido: httpx + contenedor Docker for3s-render (Playwright/Chromium) para SPAs
      + login/anti-bot honestos + redirects con ENLACE FINAL
   ✅ CACHE VALKEY de lecturas GitHub (TTL por tool, degrada si falla)
   ✅ APARTADOS Archivos/Web (migración 006): registro ligero de qué docs/URLs te mandan,
      con consulted_at. SIN binarios/HTML.
   ✅ Robustez: error handler de red, anti-rate-limit A+B+C, comandos admin, hora local del usuario,
      audit inmutable + cifrado KEK. Detalle trazable en el Changelog.

   ⚠️ Hallazgo permanente: la suscripción OAuth NO expone rate-limit por-minuto (solo cupo 5h/7d)
      → bucket local a ciegas, por eso se espacia. Al probar tool-use en ráfaga, espaciar ≥20s.
   ⚠️ El server está en red DOMÉSTICA (parpadea NetworkError) → el bot lo absorbe (no muere).
      Solución de fondo = mover a VPS (a futuro, no bloquea).
```

- 11/11 nodos cerebrales completos
- Pilar 1 Seguridad COMPLETO (INPUT Amígdala + OUTPUT Gate) · Pilar 2 Scalability Foundation · Pilar 3 Autonomía Generativa ACTIVADO + GOBERNADO (Meta-Orchestrator)
- Compliance SOC2 ~90-95% + GDPR ~88-92% audit-ready
- Deployable + Operable + Recuperable
- Costo v1 ~$97-137/mo (margen 85.7% bajo P2)

**Auditoría de coherencia completada 2026-06-09 (4 entregables):**
- ✅ `docs/analysis/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md` — alineación diseño vs Grafo/Visión (veredicto 9.2/10)
- ✅ `docs/analysis/Reporte_Maestro_Consolidado_R1-R10.md` — los 10 R como UN sistema (tech concuerda, ~8 columnas vertebrales reusadas, costos, flujo de datos)
- ✅ `memory/archive/Plan_Maestro_Programacion.md` — **el ORDEN de construcción** (6 fases foundation-first + 3 diagramas + mapa flujo datos + gates + MVP vs diferido)
- ✅ `memory/archive/Estimacion_Tiempo_Por_Subtema.md` — **el TIEMPO** (~100 sub-temas estimados; ver §3 abajo)

## 3. Próximo paso esperado

**🧭 ESTADO 2026-07-01:** REDISEÑO MEMORIA cerrado (F1-F5 + M1-M4, en producción). PROFESIONALIZACIÓN
cerrada (8/10, 4 en EXTRAS). PULIR H8 cerrado (7/8, BYOK en EXTRAS). **§EXTRAS = 11 diferidos.**
**Pendiente inmediato SIN bloque:** sincronizar el lote grande a GitHub (solo con orden de Brian).
**Bloques grandes por abrir (Ronda de diseño antes de codear):** ENTRENAMIENTO (E1-E4) · AUTO-CONCIENCIA
(AC1-AC4) · PRODUCTO DISTRIBUIBLE (P1-P10) · MULTI-INSTANCIA. **Deuda no-urgente:** H9 D1-D8 · H10
HP1-HP6 · intern-os C1-C3 · deuda fina M3/M4 (encadenar perfil/hilo_status en recordar, va con PR9).
Lista completa a detalle: `memory/PENDIENTES.md`.

---

### (histórico) 🚨 FASE PROFESIONALIZACIÓN (PR1-PR10) — 7/10 HECHOS. Avance al 2026-06-30:
- ✅ **PR1** (claridad: `memory/archive/PR1_Mapa_Codigo_Claridad.md` — 47 módulos por capas, estado, deuda).
- ✅ **PR2** (salud/monitoreo: /salud + cron_corridas + alerta automática; falta solo PR2.3 Grafana).
- ✅ **PR3** (datos/analítica: `analytics.py` + /datos — actividad, consumo, repos, capacidades,
  por persona; datos HONESTOS, evitó el dato falso de repos inflados x5).
- ✅ **PR4** (auditoría: flujo memoria/usuario + 47 módulos + los 12 bugs).
- ✅ **PR6** (dueños: owner en BD robusto cierra BUG-4 + transferencia atómica /transferir_dueno).
- ✅ **PR7** (revisión hitos: `memory/archive/PR7_Revision_Hitos.md` — 12/12 verificados EN CONTENEDOR VIVO:
  11 ✅ funcionan, H7 🟡 parcial por diseño, 0 rotos. Cadena audit íntegra. Cazó 2 deudas de
  observabilidad: equipo multiagente sin audit + Sme G sin perfil).
- ✅ **PR10** (soporte: /ayuda + /diagnostico personal + /reconectar + on_error avisa).
- ⏳ **PENDIENTES:** **PR5** datos empresa (= PR3.2, necesita más usuarios) · **PR8** entrenamiento
  (absorber 6 agentes, NO antes de pulir) · **PR9** UX producto (incluye dividir telegram_channel
  ~3300 L; + limpiar ~10 .bak en imagen + instrumentar audit del equipo = deuda de PR7).
- Lista completa: `memory/PENDIENTES.md` §PROFESIONALIZACIÓN + §BUGS + §MANTENIMIENTO.

**✅ MIGRACIÓN 100% CERRADA (2026-06-28):** Fase 5 ejecutada — systemd viejo `disabled`+`inactive`
(ya no arranca solo, cero choque de tokens), unit files + Postgres viejo PRESERVADOS como
rollback unos días, contenedores con `restart: unless-stopped` (arrancan solos en reinicio).
Solo queda 5.4 días después: limpiar Postgres del sistema viejo (NO urgente).

**Otros frentes abiertos (no empezados — debatir antes de codear):**
- 🏢 **MULTI-INSTANCIA** (Brian 2026-06-28, IMPORTANTE) — estructura para correr VARIOS For3s
  OS aislados en un server, cada uno en su contenedor (hoy NO existe; 1 server = 1 For3s). Es
  la capa "tenant/empresa" = base del SaaS, distinta de H8 (multi-usuario dentro de UN For3s).
  Material: 4 demos `for3s-demo-*` PARADOS (recuperables). Debatir tipo Ronda antes de codear.
  Memoria project_multi_instancia. Cruza con distribución, PR2 salud, PR6 dueños, negocio.
- 🧠 **AUTO-CONCIENCIA + AUTO-MODIFICACIÓN** AC1-AC4 (memoria project_auto_conciencia_automod) —
  cruza con PR6 (dueños) y H11 governor.
- **Bloque 1 H — BYOK** (1 API key por persona) · **Bloque 4 P3** (ejecutar código real).
- Deuda fina: H9-D1..D8 · HP1-HP6 (H10-PLANEA) · gate-auto en tool-loop de miembros (H8) ·
  backup-offsite (Tailscale) · limpiar orphan 16 turnos de `tg:1923367928` (cosmético).
- **Distribución v1.1:** probar install en Linux limpio · dominio install.for3s.dev ·
  GitHub-MCP/render como hermanos · monetización Open Core.
- ⚠️ Forma de trabajo LOCKED: DEBATIR cada sub-paso antes de codear → OK Brian → código →
  testeo. Uno a la vez. Todo lo de cara a GitHub en INGLÉS. Preguntas como TEXTO (no ventana UI).

---
### (histórico) 🤝 H8 "EQUIPO" — CERRADO. Construido + probado (LLMs reales):
- **Motor multi-agente (S0-S9):** Hub lanza N specialists en paralelo (gobernado: semáforo
  CONCURRENCIA_MAX=2 + pausa anti-429) + Synthesizer combina + 18 capas de blindaje (aislamiento
  read-only/whitelist/KEK-scoping/timeout global/RAM) + cost_control 7 capas. 2 familias:
  TÉCNICA (5: code/security/test/perf/doc) y GENERAL (5: investigador/escritor/analista/
  planificador/crítico) — For3s es segundo cerebro UNIVERSAL, no solo código. Archivos:
  specialists.py · multiagente.py · cost_control.py. Verificado: 5/5 OK, síntesis 6614 chars, 100s.
- **Multi-usuario (S10):** módulo equipo.py + migraciones 010-012. (a) tablas equipo/miembros +
  ⭐ modelo PUERTA: `/invitar` = interruptor abrir/cerrar (NO pide user_ids — gran UX); abierta=
  quien escriba entra, cerrada=solo dueño+miembros ya dentro. (b) roles encargado/miembro + matriz
  de permisos (miembro PROPONE acciones sensibles). (c) memoria HÍBRIDA: privado por persona +
  común del equipo, aislado a nivel SQL (probado con embeddings: nadie ve lo privado de otro). (d)
  gate de aprobación: solo el encargado aprueba/rechaza (verificado en BD, fail-closed). (e) el bot
  DISTINGUE usuarios en Telegram (_autorizar aditivo: dueño/miembro/puerta).
- **Disparo del equipo (S11):** AUTOMÁTICO cuando convenga (decisión Brian) pero CONSERVADOR —
  solo dispara con señales fuertes ("analiza a fondo", "auditoría completa", "lanza el equipo"...);
  charla normal y preguntas simples siguen con 1 agente. Avisa antes (transparencia del gasto),
  gobernado por las 7 capas de cost-control. 0 falsos positivos verificados.
- ⏳ **Pendiente fino (NO bloquea H8):** ejecución AUTOMÁTICA del gate aprobado (que un MIEMBRO
  dispare una propuesta de write que vaya al encargado, en el tool-loop). El botón aprobar/rechazar
  YA funciona y audita; falta distinguir rol dentro del tool-loop de escritura (código sensible).
- **TODO aditivo y fail-closed:** sin usar /invitar, For3s sigue single-owner EXACTO como hoy.

**👉 SIGUIENTE:** cerrar S12 (este doc + Bitácora ya actualizados) → H8 cerrado. Luego Brian
PRUEBA en Telegram (lanzar el equipo, abrir/cerrar puerta) y, si todo bien, elegir próximo hito.

---

### (histórico) 🎉 H6 "SE CUIDA" COMPLETO (13/13). For3s se mantiene solo de noche: backup + consolida
(CLS) + evalúa olvido (Microglía, en dry-run). Anteriores ✅: MVP CERRADO + H5 MEMORIA REAL.
Doc/H6_Plan_Maestro_SE_CUIDA.md tiene el detalle + tabla de estado + hallazgos.

**🔧 FASE ACTUAL (Brian 2026-06-20): PULIR/PROBAR H5+H6 — NO avanzar Hitos.** Brian prueba en
Telegram, reporta fallos, iteramos. NO sugerir H7 hasta que diga que está pulido.
**PULIDO HECHO (2026-06-22):** auditoría de conversaciones 19-22 jun reveló que la PERSONALIDAD
(FOR3S_ROLE) seguía siendo del MVP viejo → el bot NO reconocía sus capacidades nuevas (decía
"soy solo texto", "no puedo recuperar sesiones"). ✅ ARREGLADO: (1) FOR3S_ROLE reescrito —
reconoce multimodal/write-GitHub/H5/H6 (verificado en vivo); (2) grafo de conceptos H6 ahora se
inyecta al chat en preguntas panorámicas (verificado E2E: lista Aider/DonutBrowser/RISC Zero...).
✅ 529-overloaded ARREGLADO (los 5xx de Anthropic se reintentan con backoff + aviso amable, ya no
deja el bot mudo; 2 tests, suite 130). ✅ Repetir-respuestas-largas ARREGLADO (FOR3S_ROLE:
naturalidad — si repites la misma pregunta, resume breve + ofrece detalle, en vez de soltar todo;
verificado: 2ª respuesta 338→233 chars, tono humano). ✅ H5-mem-matiz ARREGLADO (juicio
equilibrado: ante un 'no', ofrece lo RELACIONADO real si lo hay, 'no' limpio si no, nunca
inventa; verificado 2 casos). ✅ MEMORIA-SOLO-PREGUNTAS ARREGLADO (2026-06-22, auditoría
profunda): "¿qué repos analizamos?" fallaba porque solo_usuario=True recuperaba las propias
PREGUNTAS del usuario (se parecen entre sí) en vez de las RESPUESTAS con info. Fix: buscar
TAMBIÉN respuestas del assistant (nuevo param solo_asistente + doble búsqueda combinada en
send()). Verificado E2E: ahora lista godinez-studio/Aider/DonutBrowser/cli/cli/RISC Zero reales.
🎉 **PULIDO H5/H6 COMPLETO — 6/6 hallazgos resueltos. CICLO NOCTURNO VERIFICADO CORRIENDO SOLO
(no es demo): anoche backup 07:00 + CLS consolidó 45 eps + Microglía 09:00, todo automático.**

**PULIDO DE INFRA (2026-06-22) — casi todo cerrado:** ✅ 529-overloaded · ✅ 429-system-prompt
(auditoría total de 10 flujos LLM = todos OAuth-safe + BLINDAJE en el provider) · ✅ H6-formula-
relevance v2 (refuerzo por uso REAL: lo recuperado resiste el olvido, migración 009 + contador
veces_recuperado). 🟡 SOLO queda backup-offsite: código LISTO pero bloqueado por Tailscale SSH
(exige login web) → activar con regla ACL de Tailscale + descomentar FOR3S_BACKUP_OFFSITE.

**ESTADO H7 (2026-06-23):** ✅ /model de For3s HECHO (verifica modelos del token + selección
manual con botones estilo Claude Code, persiste, aplica en caliente; los 3 modelos —Haiku/
Sonnet/Opus— responden con el OAuth). ⛔ **H7 enrutamiento automático BLOQUEADO** (su beneficio
estrella = ahorro de costo NO aplica a la suscripción plana + riesgo OAuth multi-modelo; se
retoma con API key de pago/clientes). **PRÓXIMO HITO: H8 EQUIPO** (multi-agente: 5 specialists
analizando un PR en paralelo — lo más "wow" para el wedge QA).

**👉 OPCIONES:**
1. **H8 EQUIPO** (siguiente hito real: multi-agente, R5 B3, 18 capas). ← elegido por Brian
2. (opcional) fast-path/cache de H7 — velocidad + ahorro de cuota, sí aplica a la suscripción.
2. **Las 4 capacidades P2-P5 de paridad Hermes** (§3.1 + PENDIENTES.md).

**Forma de trabajo (Brian la fijó):** explicar la lógica ANTES de codear, esperar su OK,
construir aislado, verificar, tests, y AVANZAR DE UNO EN UNO (no varios sub-pasos de golpe).

**Otras opciones (cuando H6 termine):**
- Las 4 capacidades P2-P5 de paridad Hermes (P2 sub-agentes→H8, P3 código→H4, P4 MCP, P5 skills). §3.1 + PENDIENTES.
- Pendientes menores: "H5-mem-matiz" + "H6-formula-relevance" (Brian definirá la fórmula afinada de decay).

**Cómo monitorear lo que hace el bot (para diagnosticar):** los datos NO van a los logs de httpx (silenciados). Fuentes reales: `episodes_events` (turnos, columna `channel`), `audit_events` (message_in/out + `detail.tools` + `github_write`), `gh_resources` (GitHub persistido), `consulted_files`/`consulted_web` (docs/URLs que mandan, con `consulted_at`). Conectar: `db.connect(settings.database_url)`. Logs del bot: `sudo journalctl -u for3s-telegram`.

**Estado del bot:** corriendo, sonnet-4-6 vía OAuth, token cifrado (KEK), GitHub MCP read-only, **BD migraciones v6**, 128 tests verdes. Comandos admin: /cupo /estado /diagnostico /reiniciar /reiniciar_duro (solo dueño). Anti-rate-limit A+B+C + cache Valkey activos.

**⚠️ Reglas activas:** NUNCA implementar sin explicar+aprobar. Modelo del bot = sonnet-4-6 (NO bug). OAuth de suscripción FUNCIONA. tool-use en ráfaga → espaciar ≥20s. Tokens ya rotados (2026-06-18). Memoria a fondo + BD a profundidad = Brian quiere revisarlas con cuidado MÁS ADELANTE (no tocar el motor sin su OK explícito).

**Fallos abiertos:** ninguno. Todos los reportados en las pruebas (PDF grande, routing write, falso positivo web→GitHub) están cerrados y reprobados en vivo.

**📋 PENDIENTES (lista consolidada):** ver `memory/PENDIENTES.md`. Seguridad ✅ cerrada. Lo abierto es POST-MVP: las 5 capacidades P1-P5 (paridad Hermes, prioritarias), webhooks+multi-tenant (diferidos por bloqueadores de red/diseño), mini-agente HTTP demo, Notion/cron/otros canales, hallazgos de fondo H-B/C/D/G.

Estado del repo: `~/for3s-os` en el servidor + GitHub privado `fruterito101/for3s-os` (CI verde). Cada hito = ticket en `Mente/Tickets/`. Auth LLM: OAuth-suscripción cuenta SEPARADA — el rol For3s va en el mensaje user (no system) en OAuth.

## 3.1 ⭐ PRIORIDAD post-MVP: las 5 capacidades de paridad con Hermes (Brian 2026-06-18)

Surgieron de comparar For3s vs `NousResearch/hermes-agent` v0.16.0. Brian las marcó PRIORITARIAS, "al mismo detalle que Hermes". 4/5 ya diseñadas (solo implementar); solo P1 necesita diseño nuevo. Detalle completo en PENDIENTES.md §"PARIDAD CON HERMES".
- **P1 · Modelar al usuario** (perfil persistente entre sesiones) — ⚠️ ÚNICA sin diseño → **empezar aquí** (mini-ronda, ancla H5/H13).
- **P2 · Sub-agentes en paralelo** — ✅ diseñada (R5 B3) → H8.
- **P3 · Ejecutar código real** (terminal/sandbox) — ⚠️ parcial → H4(+H8).
- **P4 · Conectar cualquier MCP** (no solo GitHub) — ✅ diseñada (R4) → H3-H4.
- **P5 · Plugins/skills auto-generables** — ✅ diseñada (R6) → H10→H11→H12.

**🔨 Plan de construcción (EL DE OBRA — LEER PRIMERO al construir):**
- ⭐ `memory/archive/Mapa_Construccion_Incremental.md` — **EL DOCUMENTO DE OBRA.** 2 cimientos (C0 servidor, C1 esqueleto) + 16 hitos VERTICALES demoables (H1 HABLA → H16 PRODUCCIÓN). Cada hito termina en un DEMO que se ve funcionando en el servidor for3s. Es el ORDEN real de ensamblaje. **Se construye en for3s (LEY), un hito a la vez, NUNCA implementar sin explicar+aprobar primero.** **C0·C1·H1·H2·H3·H4 ✅ = MVP CERRADO.** Próximo: H5+ (memoria real/KG), pero la PRIORIDAD de Brian son las 5 capacidades P1-P5 (§3.1) — varias se anclan a H5/H8/H12.
- `memory/archive/Plan_Maestro_Programacion.md` — el MARCO de fases/gates/MVP-vs-diferido (sigue vigente; el Mapa Incremental lo re-rebana en vertical).
- `memory/archive/Estimacion_Tiempo_Por_Subtema.md` — cuánto tarda cada sub-tema.
- `Ronda_06_Pre_Code_Review_Detailed.md` §E — orden interno de R6 (la más delicada).
- **Los R (R1-R10) = BIBLIOTECA técnica**, NO el orden. El orden es el Mapa Incremental.

**Estimación de tiempo (Brian solo, full-time, exp alta — DERIVADA, ±30%):**
```
   Sistema completo:    ~9-10 meses
   ★ MVP pilotable:     ~3.5-4 meses (R2+R3+R4 → "PR analizado con memoria")
   ▲ Hito Telegram:     ~6 semanas (LOCKED R1 §10 — 1er "se ve algo")
   Camino crítico:      R1→R2→R3→R4→R5→R6→R10
   Con 1 contratado desde Fase 2: ~7-8 meses
```

**🖥️ Servidor for3s (CONSTRUCCIÓN EN CURSO):** Tailscale `for3s` (100.112.177.53), SSH `brianweb3`/password. Ubuntu 26.04, 8 cores, ~19GB RAM, 878GB disco. **Ya instalado (C0):** uv+Python3.12 · Docker · PG16+AGE+pgvector+pgcrypto · Valkey. **Ya construido (C1+H1+H2):** monorepo `~/for3s-os` · BD+rol `for3s` · agente que habla con Claude + memoria persistente + audit chain. Detalle vivo: memoria `reference_servidor_for3s`.

**(En paralelo) mejora de Mente OS:** cold-start brief (este archivo) + bitácora. Ver `memory/Bitacora_Progreso.md`.

## 4. Flags activos (NO olvidar)

- ⭐ **SOC2 = sales wedge** — resaltar como "certificado de calidad B2B" en página/marketing más adelante. (memory: `project_soc2_sales_wedge`)
- **Networking dual-plane** — Cloudflare Tunnel (clientes) + Tailscale (admin Brian, ya instalado). Grafana público eliminado. (memory: `project_dual_plane_networking`)
- ⚠️ **R6 re-review HECHA** pero al programar: ejecutar plan E + medir PFC_PLANNING_COST real + cargar HARD NO-GO §8.4 + governor antes de auto-gen.
- ⚠️ **DMN 5.4.2 refinamiento HECHO** pero al programar: implementar 8 action_fn + auto-improvement loop enchufado al governor.
- 🔢 **Numeración nodos CANÓNICA** (reconciliada 2026-06-09): 1=KG, 2=Hipocampo(+Pattern Sep), 3=PFC, 4=Ganglios/Skills(+Action Sel), 5=Microglía, 6=DMN, 7=Amígdala, 8=Tálamo, 9=Dual-Process, 10=CLS, 11=Neuromod. Autoridad = Grafo §4 = Visión §6.1. Mapeo §0 manda. (memory: `project_node_numbering_canonical`)
- 🧭 **Grafo Maestro tiene §0 (2026-06-10) — leerlo ANTES del resto del Grafo.** Regla de precedencia: el Grafo = autoridad CONCEPTUAL (nodos/edges/pilares/reglas §8.3-8.4); la autoridad TÉCNICA = las rondas (el Grafo nombra tecnología pre-rondas: Neo4j/Kafka/LangGraph → ver mapa de cambios en §0.1). v1 = monolito modular + solo capacidad generativa #1 (§0.2). Cobertura: 11/11 nodos = ancho, ~40% = profundidad v1 (§0.3).
- ⚠️ **2 reglas de oro al programar:** (1) CI/CD en Fase 0 (temprano, no al final); (2) Meta-Orchestrator/governor DEBE existir ANTES de activar auto-generación de skills (R6).

## 5. Reglas de oro con Brian

- Este chat = SOLO For3s OS (carpeta Mente OS). NO mezclar con For3s QA (rama aparte) ni marca-personal.
- Modificaciones fuera de `for3s-inter/` → preguntar antes.
- Master KEK SIEMPRE offline. Brian nunca ve plaintext secrets. Audit inmutable.
- Ante duda → preguntar a Brian. NO inventar contexto. NO tratar docs históricos como fuente de verdad.

## 6. Estado de costo/tokens (lo que motivó este archivo)

Brian notó que retomar tras pausa larga consume muchos tokens (cache miss de Anthropic reenvía la conversación entera, no que se relea Mente OS). Solución: leer ESTE archivo (~5KB) al retomar en vez del Estado_Sesion (200KB) + usar `/clear` cuando la conversación crezca (Mente OS guarda todo → es seguro vaciar).

---

## 📍 PUNTEROS — si necesitas MÁS que este brief

| Necesitas... | Lee... |
|---|---|
| El diseño arquitectónico maestro (11 nodos + 3 pilares) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| **El ORDEN de programación (6 fases + diagramas + flujo datos + gates)** | `Mente/memory/archive/Plan_Maestro_Programacion.md` |
| **El TIEMPO de programación (~100 sub-temas estimados)** | `Mente/memory/archive/Estimacion_Tiempo_Por_Subtema.md` |
| Alineación diseño vs Grafo/Visión (veredicto 9.2/10) | `Mente/docs/analysis/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md` |
| Los 10 R consolidados como UN sistema (tech/costos/flujo) | `Mente/docs/analysis/Reporte_Maestro_Consolidado_R1-R10.md` |
| Numeración canónica de nodos (tabla vieja→nueva) | `Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md` §0 |
| ⭐ **H10-H12 APRENDE a detalle (el plano para modificarlos)** | `Mente/Cuerpo/H10_H11_H12_APRENDE_Referencia_Tecnica.md` |
| 🌙 **H9 SUEÑA (DMN) — plan maestro + CIERRE (COMPLETO 2026-06-26)** | `Mente/Cuerpo/H9_SUENA_Plan_Maestro_DMN.md` |
| 🧠 **H10-PLANEA (metacognición "sé cuándo no sé") — plan + CIERRE (COMPLETO 2026-06-26)** | `Mente/Cuerpo/H10_PLANEA_Plan_Maestro_Metacognicion.md` |
| 📦 **Fase Pre-Testers / distribución (8 componentes + diagrama contenedores)** | `Mente/Cuerpo/Fase_PreTesters_Plan.md` |
| 🔄 **Migración de Foresito a contenedores (5 fases + rollback + decisiones)** | `Mente/Cuerpo/Migracion_Foresito_Contenedores_Plan.md` |
| 🚨 **Profesionalización PR1-PR10 + todo lo pendiente** | `Mente/memory/PENDIENTES.md` §"PROFESIONALIZACIÓN" |
| ✅ **PR7 — revisión de los 12 hitos en contenedor vivo (evidencia real + 6 deudas HA)** | `Mente/memory/archive/PR7_Revision_Hitos.md` |
| 🗺️ **PR1 — mapa del código (47 módulos por capas, qué conecta a qué)** | `Mente/memory/archive/PR1_Mapa_Codigo_Claridad.md` |
| 🧠 **PR4 — flujo usuario/memoria archivo×archivo + caso de uso + 47 módulos** | `Mente/memory/archive/PR4_Flujo_Usuario_Memoria.md` |
| Detalle de una ronda técnica específica (R1-R10) | `Mente/Cuerpo/Ronda_XX_*.md` |
| El historial cronológico de cierres de ronda | `Mente/memory/Estado_Sesion_Continuidad.md` §3.1.x (al final) |
| Estado/reglas/contexto completo (snapshot grande) | `Mente/memory/Estado_Sesion_Continuidad.md` (200KB — solo si imprescindible) |
| Decisiones de empresa LOCKED (D-001 a D-040) | `for3s-inter/07-operations/decision-log.md` |
| Bitácora de progreso (qué pasó cada periodo) | `Mente/memory/Bitacora_Progreso.md` |
| Pre-code review Pilar 3 (Meta-Orchestrator) | `Mente/Cuerpo/Ronda_06_Pre_Code_Review_Detailed.md` |
| Refinamiento DMN (8 tasks detalladas) | `Mente/Cuerpo/Ronda_05_DMN_Tasks_Detailed.md` |
| Visión estratégica (por qué) | `Mente/Alma/Vision_For3s_Frontier.md` |

**Regla:** lee solo el puntero que necesites. No leas todo "por si acaso" — eso es lo que gasta tokens.