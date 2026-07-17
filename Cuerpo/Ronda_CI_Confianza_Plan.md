# 🛡️ Ronda CI — Plan de obra para el CI de confianza de For3s OS

> ## ✅ RONDA 100% COMPLETA (2026-07-03)
> Todo el plan ejecutado + verificado + pusheado firmado a GitHub (5 checks verdes):
> - **4 urgentes de confianza:** SEC-3 Scorecard (5.7/10) · SEC-4 Trivy · SEC-5 SBOM+Sigstore · SEC-6 CodeQL.
> - **3 de calidad:** QA-1 migraciones E2E · QA-2 Hypothesis · QA-3(+3b+v3) ty-crítico BLOQUEANTE sobre **TODO
>   el core** (cero módulos sucios, cero `type: ignore`).
> - **CI generales:** CI-2 coverage · CI-4 badges · CI-5 pip-audit (CI-1 secret scanning ya estaba; CI-3 build
>   docker en CI → EXTRAS, no aporta a este nivel).
> - **Delicados:** SEC-3b imágenes pineadas · SEC-4b/4c contenedores endurecidos · RENDER-1 límites · Dependabot #2.
> - **Limpieza cara-de-producto:** checks agrupados (Seguridad = 1 job) + Trivy image-scan a workflow manual
>   (sin "Skipped"). De 8 checks a los esenciales, cobertura intacta. El Pilar 3 Gate se queda (dormido =
>   diferenciador: freno de auto-generación H11/H12).
> - Release **v0.14.0 firmado GPG** (SBOM SPDX+CycloneDX + firmas Sigstore). Cada check cazó bugs reales.
> - Detalle vivo en la memoria [[project_sesion_bugs_2026-07-02]]. **El plan de abajo queda como registro
>   histórico del razonamiento.**

---

> **Objetivo (Brian 2026-07-03):** llevar For3s de "CI que funciona" a "CI de producto de confianza"
> con seguridad, criptografía y verificabilidad por terceros. Plan a PROFUNDIDAD, basado en el análisis
> del sistema REAL (CI actual + código + BD + 5 Dockerfiles + deps + tests) y del estándar de la industria
> (NIST SP 800-204D, OWASP CI/CD, Microsoft Agent Governance Toolkit, OpenSSF Scorecard).
>
> **Regla de oro:** For3s ya tiene la cripto DIFÍCIL (audit inmutable + hash chain, KEK offline, commits/
> releases firmados GPG, Dependabot). Este plan la hace **VISIBLE y VERIFICABLE por terceros** — el salto de
> "tengo seguridad" a "puedes confiar, aquí está la prueba". Cruza con SOC2-readiness ([[project_soc2_sales_wedge]]).

---

## 0. FOTOGRAFÍA DEL CI ACTUAL (verificado 2026-07-03)

`.github/workflows/ci.yml` — 3 jobs, dispara en `push:[main]` + `pull_request`:
1. **quality** (`Lint + Types + Tests`) — Postgres `pgvector/pgvector:pg16` como service + pgcrypto/vector →
   `uv sync` → ruff check → ruff format --check → ty check (informativo, no bloquea) → pytest. **132 tests.**
2. **security** (`SAST bandit`) — `uvx bandit -c pyproject.toml -r packages src scripts -ll` (Medium+High).
3. **pilar3-gate** — `scripts/pilar3_gate.py` (governor / código auto-generado).

**Lo que YA está bien:** BD real en el CI (no mocks), ruff+format bloquean, bandit con skips justificados,
gate propio del Pilar 3. Cazó un bug de seguridad real (2026-07-03, _autorizar).

**Terreno para los nuevos CI:**
- Python 3.12, uv (workspace: packages/* + apps/*), deps en pyproject (arq, mcp, redis, sentence-transformers…).
- **5 Dockerfiles:** Dockerfile.agent · docker/sandbox/Dockerfile · docker/render/Dockerfile ·
  Dockerfile.workspace · Dockerfile.postgres. + imágenes externas: valkey:8, github-mcp-server:latest,
  grafana:11.3.0. **← esto es lo que Trivy debe escanear (hoy NADIE lo escanea = hueco real).**
- 32 migraciones SQL, 58 módulos, audit inmutable, KEK, governor.
- Repo público `fruterito101/for3s` (AGPL) → **GitHub Actions ilimitado GRATIS + CodeQL/Scorecard gratis.**

---

## 1. LOS 4 URGENTES (SEC-3..SEC-6) — orden de ataque

### 🚨 FASE 1 — SEC-3 · OpenSSF Scorecard (PRIMERO: el sello de confianza visible)
**Qué:** workflow que puntúa el repo 0-10 en prácticas de seguridad + publica un badge en el README.
**Por qué primero:** es el número que la industria mira para confiar; da valor inmediato y visible; y sus
checks GUÍAN qué mejorar después (te dice qué te falta). Bajo esfuerzo, alto impacto.
**Cómo (workflow nuevo `.github/workflows/scorecard.yml`):**
- action oficial `ossf/scorecard-action@v2`, dispara en `schedule` (semanal) + `push:[main]` + `branch_protection_rule`.
- permisos: `security-events: write`, `id-token: write`, `contents: read`.
- publica resultado en la pestaña Security (SARIF) + `results.sarif`.
- badge en README: `[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/fruterito101/for3s/badge)](...)`.
**Qué medirá For3s (predicción de checks Scorecard):**
- ✅ probablemente bien: Signed-Releases (GPG), Dependency-Update-Tool (Dependabot), License, Security-Policy
  (SECURITY.md), CI-Tests, SAST (bandit+CodeQL cuando esté).
- 🟡 a mejorar: Branch-Protection (activar en main), Token-Permissions (pinear permisos en workflows),
  Pinned-Dependencies (pinear actions por SHA, no @v4), Fuzzing (→ conecta con QA-2 Hypothesis), Code-Review.
**Entregable:** badge visible + baseline de score. **Costo: $0.**

### 🚨 FASE 2 — SEC-4 · Trivy container scanning (HUECO REAL — cerrarlo)
**Qué:** escanear las imágenes Docker por vulnerabilidades del OS + librerías del sistema.
**Por qué:** For3s ES un producto contenerizado (agente + 8 hermanos). HOY la imagen agente (~9.63GB) NO se
escanea → cualquier CVE del base image (python:3.12-slim, postgres, etc.) pasa invisible.
**Cómo (job nuevo en ci.yml o workflow `trivy.yml`):**
- `aquasecurity/trivy-action@master` en 2 modos:
  1. **filesystem/repo scan** (deps + secrets + misconfig) — rápido, en cada push.
  2. **image scan** — construir la imagen agente y escanearla (cruza con CI-3 build docker). Puede ser en
     release, no en cada push (la imagen es grande).
- severity: `CRITICAL,HIGH` bloquea; `MEDIUM` informa (evitar ruido).
- escanear las 5 propias + avisar de las externas (valkey/grafana/mcp) que no controlamos.
- salida SARIF → pestaña Security.
**⚠️ ojo:** la imagen agente es 9.63GB → el image-scan tarda; hacerlo en release o nightly, no en cada PR.
**Entregable:** cero CVE CRITICAL/HIGH en imágenes propias (o excepciones justificadas). **Costo: $0.**

### 🚨 FASE 3 — SEC-6 · CodeQL (SAST profundo, sube el Scorecard)
**Qué:** análisis estático de GitHub (flujo de datos, inyecciones), más profundo que bandit.
**Por qué antes que SBOM:** es 1 workflow, gratis, y Scorecard lo valora (sube el score de la Fase 1).
**Cómo (`.github/workflows/codeql.yml`):**
- `github/codeql-action` (init → autobuild/none para Python → analyze), lenguaje `python`.
- dispara en push[main] + PR + schedule semanal. Salida a la pestaña Security.
- complementa bandit (no lo reemplaza): bandit = patrones conocidos rápidos; CodeQL = análisis de flujo.
**Entregable:** CodeQL activo, hallazgos triados. **Costo: $0.**

### 🚨 FASE 4 — SEC-5 · SBOM + Sigstore (supply chain firmada, estándar 2026)
**Qué:** (a) SBOM = inventario firmado de TODOS los componentes; (b) Sigstore = firma de releases sin llaves.
**Por qué al final:** es la más "de release" (no bloquea desarrollo diario) y la más compleja; conviene con
Scorecard ya midiendo (valora Signed-Releases con SLSA provenance = score 10).
**Cómo:**
- **SBOM:** `anchore/sbom-action` (usa syft) → genera SBOM en formato CycloneDX/SPDX por cada release,
  lo adjunta como asset. Formato estándar, dice "esto es exactamente lo que corre".
- **Sigstore/cosign:** `sigstore/cosign-installer` + firmar los artefactos de release (keyless, OIDC de
  GitHub). Complementa el GPG de Brian (no lo reemplaza).
- **SLSA provenance (opcional, nivel oro):** `slsa-framework/slsa-github-generator` → `*.intoto.jsonl`
  (prueba cripto de cómo/dónde se construyó). Es lo que usa el toolkit de agentes de Microsoft.
**Entregable:** cada release con SBOM + firma verificable. **Costo: $0.**

---

## 2. LAS 3 DE CALIDAD (QA-1..QA-3) — se integran al job `quality` existente

Ya registradas; el plan de CI las ordena así (van DENTRO del ci.yml actual, no workflows nuevos):
- **QA-1 · Migraciones E2E** — nuevo step en `quality`: sobre el Postgres del CI (ya existe), correr
  `uv run python -m for3s_core.cli migrate` sobre BD VACÍA → verificar que las 32 aplican + tablas OK.
  Es casi gratis (el service Postgres ya está levantado). **Habría cazado los bugs de BD de hoy.**
- **QA-2 · Hypothesis** — `pip install hypothesis` (dev dep) + tests property-based para parsers/detectores
  (tema_estado.parsear_comando, decisiones.parsear_decidi, conversation.huele_a_*, _conceptos_exactos).
  Corren dentro de pytest (ya en el CI). También sube el check "Fuzzing" del Scorecard.
- **QA-3 · mypy estricto** — subir `ty check` de `continue-on-error: true` a bloqueante, O migrar a mypy/
  pyright estricto. GRADUAL: primero módulos nuevos/críticos (memoria, perfil, tema_estado, decisiones,
  execute), el resto con ignore temporal. **Habría cazado el bug de FK.**

---

## 3. LAS 5 DE CI GENERALES (CI-1..CI-5) — dónde encajan

- **CI-1 secret scanning** → gitleaks/trufflehog como job + activar GitHub push protection (nativo, gratis).
  Sube el Scorecard. Complementa el blindaje manual (grep antes de commit).
- **CI-2 coverage** → `pytest-cov` en el step de tests + reporte. Opcional: umbral mínimo.
- **CI-3 build docker en CI** → job que hace `docker build` de Dockerfile.agent (verifica que construye).
  Se combina con SEC-4 (Trivy escanea lo que este build produce).
- **CI-4 badge README** → badges de CI + Scorecard + coverage en el README público (se ve pro).
- **CI-5 pip-audit** → `uv run pip-audit` como job (vulns de deps en cada push, además de Dependabot).

---

## 4. ORDEN DE EJECUCIÓN RECOMENDADO (por impacto/esfuerzo)

| # | Qué | Fase | Esfuerzo | Da |
|---|---|---|---|---|
| 1 | **SEC-3 Scorecard** + CI-4 badge | workflow nuevo | bajo | el sello de confianza visible + baseline |
| 2 | **CI-1 secret scanning** | job/nativo | bajo | seguridad repo público + sube Scorecard |
| 3 | **SEC-6 CodeQL** | workflow nuevo | bajo | SAST profundo + sube Scorecard |
| 4 | **QA-1 migraciones E2E** | step en quality | bajo | cierra el hueco de BD |
| 5 | **SEC-4 Trivy** (repo scan primero, image scan en release) | job | medio | cierra el hueco de contenedores |
| 6 | **QA-2 Hypothesis** | tests | medio | caza bugs de texto libre + Fuzzing en Scorecard |
| 7 | **CI-5 pip-audit** + **CI-2 coverage** | jobs | bajo | refuerzo deps + visibilidad |
| 8 | **SEC-5 SBOM + Sigstore** (+ SLSA) | workflow release | medio-alto | supply chain firmada (score 10) |
| 9 | **QA-3 mypy estricto** (gradual) | continuo | alto | tipos que bloquean |
| 10| **CI-3 build docker en CI** | job | medio | atrapa fallos de build |

**Todo GRATIS** (repo público). Único que consume tokens (NO en este plan, va aparte): evals de LLM
(promptfoo/deepeval, semilla en el DMN `eval_regression`).

---

## 5. PRINCIPIOS (forma de trabajo, regla LOCKED de Brian)

- **Uno por uno**, debatir/explicar antes de codear, verificar cada uno, no todo de golpe.
- **NADA de cara al usuario en producción** — son workflows de CI (calidad/confianza del repo).
- **Server-primero:** los workflows viven en el repo → se prueban con push a una rama o PR → observar el
  run en GitHub Actions → ajustar. (Los workflows SÍ tocan `.github/`, que va a GitHub por definición.)
- **No romper el CI verde actual:** cada nuevo check se añade sin tumbar los 3 que ya pasan.
- **Cruza con SOC2-readiness:** varios de estos (audit, signed releases, SBOM, SAST) son evidencia directa
  para los TSC de SOC2 (Security, Processing Integrity, Confidentiality). Documentar el mapeo al avanzar.

---

## 6. ESTADO OBJETIVO (cómo se ve el CI "de confianza" al terminar)

```
CI de For3s OS (repo público, todo gratis):
├── quality      → ruff + format + mypy(estricto) + pytest + migraciones E2E + Hypothesis + coverage
├── security     → bandit + CodeQL + secret scanning + pip-audit
├── containers   → Trivy (repo scan siempre; image scan en release)
├── supply-chain → SBOM (syft) + Sigstore (cosign) + SLSA provenance   [en release]
├── scorecard    → OpenSSF Scorecard (semanal) → badge en README
└── pilar3-gate  → governor (ya existe)

README: badges de CI ✓ · Scorecard 8+/10 · coverage % · License AGPL
Releases: firmados (GPG + Sigstore) + SBOM + provenance
= "producto de confianza verificable por terceros"
```

*Plan generado 2026-07-03 tras análisis a profundidad del sistema real (CI + código + BD + 5 Dockerfiles +
deps + tests + memorias). Fuentes: NIST SP 800-204D · OWASP CI/CD Cheat Sheet · Microsoft Agent Governance
Toolkit · OpenSSF Scorecard/SLSA/Sigstore. Pendientes: SEC-3..6 + QA-1..3 + CI-1..5 en PENDIENTES.md.*
