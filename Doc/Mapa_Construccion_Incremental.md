# 🔨 Mapa de Construcción Incremental — For3s OS

> **EL documento de obra. No es teoría, no es diseño — es la escalera real de construcción.** Cada peldaño termina en algo que CORRE y que puedes VER funcionando (un DEMO). Terminas un hito → marcas ✅ → sigue el siguiente. Nunca "esto lo paro porque va en otro R". Aquí se construye en VERTICAL: cada hito atraviesa las capas que necesite y entrega algo vivo.

**Owner:** Brian López
**Fecha:** 2026-06-10
**Estatus:** 🟢 ACTIVO — documento de construcción en curso (NO planeación, NO pruebas)
**Capa:** Doc — ejecución de obra

---

## ⚖️ LAS 3 LEYES DE ESTA CONSTRUCCIÓN (no negociables)

```
   LEY 1 — SE CONSTRUYE EN EL SERVIDOR for3s. PUNTO.
           Tailscale `for3s` (100.112.177.53). Ya NO es prueba, ya NO es
           local-y-luego-vemos. For3s OS se construye y vive AHÍ desde el
           commit 1. (Acceso: Mente/Acceso_Seguro/Conectar_Servidor_For3s.md)

   LEY 2 — CADA HITO TERMINA EN UN DEMO QUE SE VE FUNCIONANDO.
           No avanzo al siguiente hito hasta que el actual CORRE y Brian lo
           ve. Nada de "tengo media capa hecha en 3 R distintos". Vertical.

   LEY 3 — LOS R SON LA BIBLIOTECA, NO EL ORDEN.
           Las 10 rondas (R1-R10) son la VERDAD TÉCNICA — se consultan para
           el detalle de diseño de cada pieza. Pero el ORDEN de ensamblaje
           es ESTE documento, no el número de R. El Grafo Maestro sigue
           siendo la fuente de verdad arquitectónica (con su §0).
```

---

## 📐 Por qué este documento existe (el problema que resuelve)

```
   DOCUMENTACIÓN TÉCNICA (los R)  →  organizada por CAPA (horizontal)
     "todo datos junto · todo LLM junto · todo tools junto"
     → perfecta para CONSULTAR el diseño · pésima como orden de obra
     → construir "por R" = 4-6 semanas en R2 SIN nada que encender

   PLAN DE IMPLEMENTACIÓN (este doc)  →  organizado por INCREMENTO (vertical)
     "cada paso atraviesa las capas que necesite y TERMINA EN ALGO QUE CORRE"
     → 'ya terminé esto y lo veo funcionando → ahora sigue esto'
     → escalable: cada peldaño se apoya en el anterior, sin saltos
```

**Este documento NO contradice al `Plan_Maestro_Programacion.md`** — lo reordena en vertical. El Plan Maestro define las fases, los gates y el MVP-vs-diferido (sigue vigente como marco); ESTE define la secuencia de hitos demoables. Mismo contenido, re-rebanado para construir sin esperar.

---

## Tabla de contenidos

1. [Cómo se lee y se usa este mapa](#1-cómo-se-lee-y-se-usa)
2. [LOS CIMIENTOS — qué se instala una vez](#2-los-cimientos)
3. [LA ESCALERA — los 16 hitos demoables](#3-la-escalera-de-hitos)
4. [Detalle hito por hito](#4-detalle-hito-por-hito)
5. [Lo transversal — qué vive desde el día 1](#5-lo-transversal)
6. [Tablero de progreso (marca aquí)](#6-tablero-de-progreso)
7. [Reglas de oro durante la obra](#7-reglas-de-oro)

---

## 1. Cómo se lee y se usa

Cada hito tiene 6 campos. Esto es lo que significa cada uno:

```
   HITO Hn — NOMBRE CORTO ("qué hace el sistema al terminarlo")
   ├─ 🎯 OBJETIVO:    qué capacidad nueva gana el sistema
   ├─ 🔨 SE CONSTRUYE: las piezas concretas a programar
   ├─ 📚 BIBLIOTECA:   qué R(s) consultar para el detalle técnico
   ├─ ✅ DEMO:         lo que Brian VE funcionando = "terminado"
   ├─ 🔓 DESBLOQUEA:   qué hito(s) se habilitan después
   └─ ⏱️ TAMAÑO:       estimación gruesa (días de obra)
```

**Regla de uso:** trabajas UN hito a la vez. Cuando el DEMO funciona en el servidor, marcas ✅ en el tablero (§6) y pasas al siguiente. Si algo del DEMO no corre, NO avanzas — se arregla primero.

---

## 2. LOS CIMIENTOS

Lo que tu lógica pedía: **"¿cuáles son los cimientos que necesito instalar?"** Esto se hace UNA vez, al principio, en el servidor for3s. Es lo único "horizontal" del plan — porque son herramientas, no producto.

### C0 — Preparar el servidor (instalar TODO lo instalable de una vez)

```
   🎯 Dejar el servidor for3s listo para recibir código. Instalar de una
      sola pasada todo lo que es "binario que se instala", para no estar
      parando después "ah, falta instalar X".

   🔨 SE INSTALA (en el servidor, con sudo):
      • uv (gestor Python) + Python 3.12 vía uv (el sistema trae 3.14;
        uv instala el 3.12 lockeado SIN tocar el del sistema)
      • Docker + docker compose (para contenedores de H-tardíos)
      • PostgreSQL 16 + extensiones: Apache AGE + pgvector + pgcrypto
      • Valkey (cache/broker)
      • Herramientas base: git (ya está), build-essential, curl (ya está)

   📚 BIBLIOTECA: R1 (stack) · R2 B1 (Postgres+extensiones) · R10 (runtime)
   ✅ DEMO: en el servidor corre `psql -c "SELECT version()"`, `docker run
            hello-world`, `uv --version`, `valkey-cli ping` → todos responden.
   🔓 DESBLOQUEA: C1
   ⏱️ TAMAÑO: ~1-2 días (mayormente instalación + verificación)
```

### C1 — Esqueleto del proyecto + red de seguridad (= la "Fase 0")

```
   🎯 El repositorio nace con disciplina industrial: estructura + CI verde
      + el enchufe del freno de autonomía, antes de escribir lógica.

   🔨 SE CONSTRUYE:
      • uv init + monorepo (apps/ packages/) + pyproject + uv.lock
      • CI local: ruff (lint) + ty (tipos) + pytest (tests) — comando verde
      • GitHub Actions: pipeline lint + unit + SAST (Bandit/Semgrep)
      • Pilar 3 GATE skeleton (vacío, reservado para H11/H12)
      • Installer base (one-line, versión mínima)

   📚 BIBLIOTECA: R1 (estructura) · R10 B1 (CI/CD) · R9 (SAST)
   ✅ DEMO: haces un push trivial → el CI corre solo y marca ✅ verde.
            La estructura de carpetas existe en el servidor.
   🔓 DESBLOQUEA: H1
   ⏱️ TAMAÑO: ~3-4 días
```

> Con C0 + C1 el servidor está vivo y el proyecto tiene cimientos. A partir
> de aquí, TODO hito entrega algo que se ve funcionando.

---

## 3. La escalera de hitos

Vista completa. Cada peldaño se apoya en el anterior. Las flechas = "construye encima de".

```
   ════════════════ MVP PILOTABLE (lo mostrable a un cliente) ════════════════
   C0 servidor → C1 esqueleto →
   H1 HABLA ───────► agente CLI responde con Claude
   H2 RECUERDA ────► persiste sesiones entre reinicios
   H3 TELEGRAM ────► vive en tu Telegram (▲ hito LOCKED R1, ~sem 6)
   H4 TIENE MANOS ─► analiza un PR real de GitHub
   ═══════════ ★ aquí ya tienes MVP en 4 rebanadas VISIBLES ★ ═══════════

   ════════════════ EL CEREBRO DE VERDAD (memoria + coordinación) ════════════
   H5 MEMORIA REAL ► vector search + Knowledge Graph (multi-hop)
   H6 SE CUIDA ────► CLS consolida + Microglía poda (jobs nocturnos)
   H7 DECIDE ──────► Tálamo + Dual-Process (Haiku barato vs Opus caro)
   H8 EQUIPO ──────► multi-agent: 5 specialists en paralelo
   H9 SUEÑA ───────► DMN trabaja solo cuando está idle

   ════════════════ APRENDIZAJE GOBERNADO (Pilar 3 — lo delicado) ════════════
   H10 PLANEA ─────► PFC + confidence ("sé cuándo NO sé")
   H11 EL FRENO ───► Meta-Orchestrator governor (ANTES de soltar el motor)
   H12 APRENDE ────► skills GO/NO-GO + auto-generación gobernada

   ════════════════ VENDIBLE ENTERPRISE (cara + ojos + defensas) ══════════════
   H13 CARA FORMAL ► channels + Output Gate firmado + auth/RBAC
   H14 OJOS ───────► Grafana: ves todo lo que pasa + audit consultable
   H15 DEFENSAS ───► Amígdala bloquea ataques (attack suite)
   H16 PRODUCCIÓN ─► deploy + DR + backup completo → CLIENTES REALES
```

---

## 4. Detalle hito por hito

### ─── BLOQUE A: MVP PILOTABLE ───

#### H1 — HABLA
```
   🎯 El sistema existe y responde: un agente que recibe un mensaje y
      contesta razonando con Claude. El "hola mundo" cerebral.
   🔨 SE CONSTRUYE:
      • Agent runtime mínimo (loop CLI con rich)
      • ClaudeProvider (Sonnet 4.6) + abstracción LLMProvider
      • Prompt builder básico (Jinja2) + cost tracking desde ya
   📚 BIBLIOTECA: R1 (runtime/CLI) · R3 B1+B2 (provider, prompts)
   ✅ DEMO: en el servidor corres el CLI, escribes "analiza esta función" y
            el agente responde con Claude. Ves el costo del request.
   🔓 DESBLOQUEA: H2
   ⏱️ TAMAÑO: ~3-4 días
```

#### H2 — RECUERDA
```
   🎯 El sistema deja de ser amnésico: guarda lo que pasó y lo recupera al
      reiniciar. Nace la persistencia (y con ella, el audit chain).
   🔨 SE CONSTRUYE:
      • PostgreSQL conectado (SQLAlchemy 2 + asyncpg + Alembic)
      • Tablas base: sessions, episodes_events (Event Sourcing) + triggers
      • audit_events hash chain (inmutable) ← arranca AQUÍ, no "en su R"
      • Working memory (in-process) + persistencia de sesión
   📚 BIBLIOTECA: R2 B1 (storage, ES, audit) · R2 B2 (tiers)
   ✅ DEMO: hablas con el agente, reinicias el proceso en el servidor,
            vuelves a entrar → recuerda la conversación anterior. Y ves
            que cada interacción quedó en el audit chain (inmutable).
   🔓 DESBLOQUEA: H3
   ⏱️ TAMAÑO: ~5-6 días
```

#### H3 — TELEGRAM (▲ hito LOCKED de R1 §10)
```
   🎯 For3s OS sale de la terminal y vive en tu Telegram. El primer "se ve
      como un producto". Es el hito de validación que R1 lockeó (~semana 6).
   🔨 SE CONSTRUYE:
      • Telegram MCP (custom + patrones Hermes/PlatformAdapter)
      • mcp SDK + Discovery (la base del sistema de tools)
      • Routing mensaje Telegram → agente → respuesta
   📚 BIBLIOTECA: R4 B1 (mcp SDK) · R4 B2 (Telegram MCP) · R1 §10 (cronograma)
   ✅ DEMO: le escribes a For3s desde tu Telegram (teléfono) y te responde
            con memoria. Se lo puedes mostrar a alguien en su celular.
   🔓 DESBLOQUEA: H4
   ⏱️ TAMAÑO: ~4-5 días
```

#### H4 — TIENE MANOS (→ MVP PILOTABLE COMPLETO)
```
   🎯 El sistema ACTÚA en el mundo real: lee y analiza un PR de GitHub.
      Aquí nace el wedge QA y se cierra el MVP que puedes pilotar.
   🔨 SE CONSTRUYE:
      • GitHub MCP (oficial) + auth + cache
      • Filesystem MCP + HTTP MCP (con SSRF guard básico)
      • KEK hierarchy (secrets cifrados — Master KEK offline)
      • Docker multi-tenant 3-capas (foundation: 1er workspace aislado)
   📚 BIBLIOTECA: R4 B1 (KEK, Docker) · R4 B2 (GitHub/FS/HTTP MCP)
   ✅ DEMO: le pasas un PR real de un repo de GitHub por Telegram, y For3s
            lo analiza end-to-end (lo lee → razona → responde con hallazgos),
            con la memoria y el audit funcionando. ★ ESTE ES EL MVP. ★
   🔓 DESBLOQUEA: H5 (y ya podrías poner un pilot a usarlo)
   ⏱️ TAMAÑO: ~5-7 días
```

### ─── BLOQUE B: EL CEREBRO DE VERDAD ───

#### H5 — MEMORIA REAL
```
   🎯 La memoria pasa de "guardar texto" a "entender": búsqueda semántica +
      grafo de conocimiento navegable.
   🔨 SE CONSTRUYE:
      • Stella embeddings LOCAL @1024 + pgvector + HNSW
      • Knowledge Graph (Apache AGE) + queries Cypher multi-hop
      • Hipocampo (episódica + pattern separation) completo
   📚 BIBLIOTECA: R2 B1 (AGE, pgvector) · R2 B2 (Stella, tiers, KG)
   ✅ DEMO: le preguntas "¿qué bugs parecidos hemos visto?" y encuentra
            episodios similares por significado (no por palabra exacta) +
            navega relaciones en el KG. Memoria que razona.
   🔓 DESBLOQUEA: H6
   ⏱️ TAMAÑO: ~6-7 días
```

#### H6 — SE CUIDA
```
   🎯 El sistema se mantiene solo: consolida lo importante y olvida el ruido,
      en jobs nocturnos. La memoria deja de crecer infinita.
   🔨 SE CONSTRUYE:
      • Valkey + Arq (jobs background) + pgbouncer
      • CLS: consolidación episódica→KG (HDBSCAN + Haiku, 2 AM)
      • Microglía: olvido inteligente (soft delete + decay, 3 AM, NO toca audit)
      • Backup 3-2-1 (foundation) ← protege los datos desde ya
   📚 BIBLIOTECA: R2 B2 (CLS, Microglía) · R2 B3 (Valkey/Arq) · R2 B4 (backup)
   ✅ DEMO: dejas el sistema corriendo una noche → a la mañana ves en logs
            que CLS consolidó N episodios al KG y Microglía podó M obsoletos,
            y el audit chain quedó intacto. "Es mejor hoy que ayer."
   🔓 DESBLOQUEA: H7
   ⏱️ TAMAÑO: ~5-6 días
```

#### H7 — DECIDE
```
   🎯 El sistema enruta solo: usa el modelo barato (Haiku) para lo simple y
      el caro (Opus) para lo complejo. Empieza a gobernar su propio costo.
   🔨 SE CONSTRUYE:
      • Tálamo (tool selection + context routing + 3 modos subgrafo)
      • Neuromoduladores (4 modos globales)
      • Dual-Process Check (S1/S2 + fast-path: cache→semántico→heurística)
      • Caching 4 capas (R3) enchufado aquí (-62% costo)
   📚 BIBLIOTECA: R5 B1 (Tálamo/Neuromod) · R5 B2 (Dual-Process) · R3 B2 (caching)
   ✅ DEMO: le mandas una query trivial → ves que usó Haiku (barato/rápido);
            le mandas una compleja → usó Opus. El costo por request baja
            visiblemente con el caching.
   🔓 DESBLOQUEA: H8
   ⏱️ TAMAÑO: ~5-6 días
```

#### H8 — EQUIPO
```
   🎯 De un agente a un equipo: 5 specialists trabajando en paralelo sobre
      un problema, con aislamiento total entre ellos.
   🔨 SE CONSTRUYE:
      • Multi-Agent Network (hub-and-spoke + 5 specialists)
      • 18 capas defense-in-depth (aislamiento + sin fuga cross-workspace)
      • Cost control multi-agent (7 layers, budget cap)
      • Message bus (asyncio.Queue v1)
   📚 BIBLIOTECA: R5 B3 (multi-agent completo, 18 capas)
   ✅ DEMO: le pasas un PR grande → ves los 5 specialists (Analyzer/History/
            Risk/Test/Reviewer) trabajando en paralelo y el Synthesizer
            combinando. Más rápido y más completo que un solo agente.
   🔓 DESBLOQUEA: H9
   ⏱️ TAMAÑO: ~6-7 días (el más pesado del bloque — 18 capas)
```

#### H9 — SUEÑA
```
   🎯 El sistema trabaja cuando nadie lo usa: en idle, reflexiona, pre-computa,
      detecta patrones. El DMN ("modo por defecto" del cerebro).
   🔨 SE CONSTRUYE:
      • Idle detection + DMN scheduler
      • Los 8 tasks del DMN (usar Ronda_05_DMN_Tasks_Detailed.md)
      • DMN budget + 9 controles
   📚 BIBLIOTECA: R5 B4 (DMN) · Ronda_05_DMN_Tasks_Detailed (los 8 action_fn)
   ✅ DEMO: dejas el workspace idle → ves que el DMN corrió: pre-computó
            embeddings, detectó un patrón ("este módulo tiende a romper"),
            y dejó hipótesis listas para el próximo request.
   🔓 DESBLOQUEA: H10
   ⏱️ TAMAÑO: ~5-6 días
```

### ─── BLOQUE C: APRENDIZAJE GOBERNADO (Pilar 3 — máximo cuidado) ───

> ⚠️ Este bloque es código auto-modificante. El orden interno es SAGRADO:
> el FRENO (H11) se construye ANTES de soltar el MOTOR (H12). Regla de oro
> del Plan Maestro + R6 §E.1. Bootstrap MUY conservador (shadow-heavy).

#### H10 — PLANEA
```
   🎯 El sistema planea antes de actuar y SABE CUÁNDO NO SABE. Nace la
      metacognición (lo que ningún agente actual tiene).
   🔨 SE CONSTRUYE (R6 pasos 1-3):
      • Skill schema + storage (Postgres + pgvector + RLS)
      • PFC core (plan-then-execute + executor + pre-flight)
      • Confidence scoring (8 señales) + check loop (re-plan/ask-human)
      • ⚠️ medir PFC_PLANNING_COST REAL aquí (no asumir $0.05)
   📚 BIBLIOTECA: R6 §E.1 pasos 1-3 · Ronda_06_Pre_Code_Review_Detailed
   ✅ DEMO: le das un problema ambiguo → en vez de inventar, dice "confianza
            0.62 < umbral, necesito que me aclares X" (ask-human). Y para uno
            claro, planea y ejecuta con confianza alta.
   🔓 DESBLOQUEA: H11
   ⏱️ TAMAÑO: ~6-7 días
```

#### H11 — EL FRENO (se construye ANTES que H12)
```
   🎯 El gobernador de la autonomía. ANTES de dejar que el sistema genere
      sus propias skills, se construye el freno que lo controla.
   🔨 SE CONSTRUYE (R6 paso 9 + bootstrap NO-GO):
      • Meta-Orchestrator (governor 6 frenos + kill switch)
      • Vía NO-GO (3 niveles HARD/SOFT/WARN) + HARD blocks §8.4 al startup
      • Conexión al Pilar 3 GATE skeleton (creado en C1) → ahora se llena
   📚 BIBLIOTECA: R6 §A (Meta-Orchestrator) · R6 §E.1 paso 5+9 · Grafo §8.3/8.4
   ✅ DEMO: pruebas el kill switch → congela la generación. Intentas una
            acción de la lista HARD NO-GO → la bloquea. El freno funciona
            ANTES de que exista el motor que frena.
   🔓 DESBLOQUEA: H12
   ⏱️ TAMAÑO: ~4-5 días
```

#### H12 — APRENDE
```
   🎯 El diferenciador total: el sistema escribe sus propias skills, las
      refuerza, las olvida — todo gobernado por el freno de H11.
   🔨 SE CONSTRUYE (R6 pasos 4-8, 10):
      • Skill application GO (skill_to_plan, shadow-heavy v1)
      • Dopaminergic scoring (TD-learning, decay 0.98)
      • Lifecycle manager (8 estados + sandbox eval independiente)
      • Plan→Skill promotion (7 fases) ← SOLO ahora, con el freno puesto
      • Failure handling (compensating actions + rollback)
   📚 BIBLIOTECA: R6 §E.1 pasos 4,6,7,8,10 · §D (failure)
   ✅ DEMO: resuelves 3 veces un problema similar → el sistema propone una
            skill nueva, la prueba en sandbox, y (con tu aprobación) la
            promueve. La próxima vez la aplica sola. APRENDIÓ.
   🔓 DESBLOQUEA: H13
   ⏱️ TAMAÑO: ~7-8 días
```

### ─── BLOQUE D: VENDIBLE ENTERPRISE ───

#### H13 — CARA FORMAL
```
   🎯 El sistema se expone profesionalmente: canales formales + cada output
      firmado criptográficamente (el sello que el cliente enterprise paga).
   🔨 SE CONSTRUYE:
      • Channels formales (Telegram prod + REST API + GitHub App)
      • Output Gate (firma HMAC/Ed25519 + trace + encrypt)
      • QA Pack universal + renderers · Auth/RBAC cross-channel (35+ permisos)
      • Dashboard v2
   📚 BIBLIOTECA: R7 completo (B1-B4)
   ✅ DEMO: mandas un análisis por REST API y por Telegram → ambos llegan
            FIRMADOS y verificables, con trace completo. El mismo usuario
            linkeado entre canales.
   🔓 DESBLOQUEA: H14
   ⏱️ TAMAÑO: ~6-7 días
```

#### H14 — OJOS
```
   🎯 Ves TODO lo que pasa dentro del sistema, en tiempo real, en dashboards.
      Y el audit es consultable para compliance.
   🔨 SE CONSTRUYE:
      • Prometheus (instrumenta los 11 nodos) + Grafana (3 dashboards)
      • Loki (logs) + Tempo (traces) + OpenTelemetry
      • Audit query engine + SLO/SLA tracking + alerts
   📚 BIBLIOTECA: R8 completo (B1-B4)
   ✅ DEMO: abres Grafana (vía Tailscale) y ves en vivo: requests, costo por
            workspace, latencia, qué nodos se activaron. Consultas el audit:
            "todas las decisiones del workspace X en junio".
   🔓 DESBLOQUEA: H15
   ⏱️ TAMAÑO: ~5-6 días
```

#### H15 — DEFENSAS
```
   🎯 El perímetro de seguridad: el sistema detecta y bloquea ataques antes
      de procesarlos. Cierra el Pilar 1.
   🔨 SE CONSTRUYE:
      • Amígdala (scanner 5 capas: heurística→Haiku→canary→sanitización)
      • Anomaly detection + Threat Coordinator (DEFCON)
      • Custom attack suite (regression) + threat model STRIDE+DREAD (doc)
      • SOC2 mapping + GDPR program (docs)
   📚 BIBLIOTECA: R9 completo (B1-B3)
   ✅ DEMO: le lanzas el attack suite (prompt injections, exfiltración) →
            la Amígdala bloquea cada uno y alerta. El sistema se defiende.
   🔓 DESBLOQUEA: H16
   ⏱️ TAMAÑO: ~6-7 días
```

#### H16 — PRODUCCIÓN
```
   🎯 For3s OS deployable, operable y recuperable. Listo para CLIENTES REALES.
   🔨 SE CONSTRUYE:
      • Runtime híbrido (systemd + Docker) formalizado
      • Networking dual-plane (Cloudflare Tunnel clientes + Tailscale admin)
      • Secrets KEK offline bootstrap (TPM/USB) verificado
      • Backup completo + WAL PITR + DR testing real (RTO/RPO medidos)
      • Pre-flight checklist + ops runbooks
   📚 BIBLIOTECA: R10 completo (B1-B4)
   ✅ DEMO: simulas un desastre (tiras la DB) → restauras desde backup y el
            sistema vuelve, con audit forense intacto. Pre-flight pasa los
            11 checks. Cloudflare expone el sistema a un cliente real.
   🔓 DESBLOQUEA: → CLIENTES / PILOTS REALES PAGANDO
   ⏱️ TAMAÑO: ~6-7 días
```

---

## 5. Lo transversal (vive desde el día 1, NO se deja "para su R")

Hay cosas que NO son un hito — son propiedades que arrancan temprano y crecen con cada hito. Esto es clave para que sea escalable y no "lo dejo para su R":

```
   ┌────────────────────┬──────────┬─────────────────────────────────────┐
   │ Transversal         │ Desde    │ Crece en                            │
   ├────────────────────┼──────────┼─────────────────────────────────────┤
   │ CI verde en c/push  │ C1       │ siempre (cada hito añade sus tests) │
   │ Cost tracking       │ H1       │ H7 (caching) · H14 (dashboards)     │
   │ Audit hash chain    │ H2       │ todos (cada decisión → audit)       │
   │ Workspace isolation │ H4       │ H8 (multi-agent) · H13 (RBAC)       │
   │ Backup              │ H6       │ H16 (WAL PITR + DR)                 │
   │ Tests de cada pieza │ cada hito│ nunca "después" — junto con el código│
   └────────────────────┴──────────┴─────────────────────────────────────┘
```

**Regla:** cuando un hito toca algo transversal, lo extiende — nunca lo pospone. El audit no "espera a R8": nace en H2 y R8 solo lo formaliza/visualiza.

---

## 6. Tablero de progreso (marca aquí conforme avanzas)

```
   CIMIENTOS
   [x] C0  Servidor preparado ✅ 2026-06-10 (uv 0.11.20 + Python 3.12.13 +
           Docker 29.5.3 + PG16.14[vector 0.8.2 · age 1.6.0 · pgcrypto 1.3] +
           Valkey 9.0.3 · todos enabled al boot · DEMO pasado en for3s)
   [x] C1  Esqueleto + CI verde + gate skeleton ✅ 2026-06-10
           (~/for3s-os en el servidor · repo PRIVADO github.com/fruterito101/
           for3s-os · commit 5d4a3a7 · CI 3 jobs verdes: Lint+Types+Tests ✓
           SAST bandit ✓ Pilar3-gate ✓ · ruff/ty/pytest verdes en server)

   MVP PILOTABLE  ◄── meta intermedia: cliente puede usarlo
   [x] H1  HABLA       ✅ 2026-06-11 — agente CLI razona con Claude Sonnet 4.6
           (suscripción OAuth) + gestor de concurrencia 3 capas. DEMO: detectó
           el bug en def suma(a,b):return a-b. CI verde. Ticket 001.
   [ ] H2  RECUERDA    (Postgres + audit chain)
   [x] H3  TELEGRAM    ✅ 2026-06-11 (▲ HITO LOCKED cumplido: @For3s_OS_bot
           vivo · polling+fail-closed+memoria compartida · demo ~4s e2e)
   [ ] H4  TIENE MANOS (GitHub PR + KEK + Docker) ★ MVP COMPLETO

   CEREBRO DE VERDAD
   [ ] H5  MEMORIA REAL (vector + KG)
   [ ] H6  SE CUIDA     (CLS + Microglía + backup)
   [ ] H7  DECIDE       (Tálamo + Dual-Process + caching)
   [ ] H8  EQUIPO       (multi-agent 5 specialists)
   [ ] H9  SUEÑA        (DMN 8 tasks)

   APRENDIZAJE GOBERNADO (Pilar 3)
   [ ] H10 PLANEA       (PFC + confidence)
   [ ] H11 EL FRENO     (governor) ◄── ANTES de H12
   [ ] H12 APRENDE      (skills auto-generadas gobernadas)

   VENDIBLE ENTERPRISE
   [ ] H13 CARA FORMAL  (channels + Output Gate firmado)
   [ ] H14 OJOS         (Grafana + audit query)
   [ ] H15 DEFENSAS     (Amígdala + attack suite)
   [ ] H16 PRODUCCIÓN   (deploy + DR) → CLIENTES REALES

   PROGRESO: ___ / 18 peldaños
```

**Estimación gruesa total** (Brian solo, full-time, ±30% — detalle en `Estimacion_Tiempo_Por_Subtema.md`):
- Hasta MVP (C0→H4): **~4-5 semanas** (el hito Telegram es ~sem 6 si se incluye pulido)
- Sistema completo (C0→H16): **~9-10 meses**

---

## 7. Reglas de oro durante la obra

```
   1. UN HITO A LA VEZ. No empezar H(n+1) hasta que el DEMO de H(n) corra
      en el servidor for3s.

   2. EL DEMO ES LA DEFINICIÓN DE "TERMINADO". No "creo que funciona" —
      se ve funcionando o no está terminado.

   3. ANTES DE CADA HITO: explicar de qué trata + esperar aprobación de
      Brian (regla permanente: NUNCA implementar primero).

   4. LOS R SON BIBLIOTECA. Se abren para el detalle técnico del hito
      actual, no para dictar el orden. El orden es ESTE documento.

   5. EL FRENO ANTES DEL MOTOR. H11 (governor) SIEMPRE antes de H12
      (auto-generación). No negociable.

   6. SE CONSTRUYE EN for3s. Cada hito se prueba en el servidor real,
      no en local "y luego subimos".

   7. TESTS Y AUDIT CON EL CÓDIGO, no después. Cada pieza nace con su test.

   8. SI UN DEMO NO CORRE, SE ARREGLA — no se avanza dejando deuda.
```

---

## Cierre

```
   ╔═══════════════════════════════════════════════════════════════════╗
   ║   ESTE ES EL MAPA DE OBRA. 2 cimientos + 16 hitos demoables.        ║
   ║                                                                    ║
   ║   Cada peldaño termina en algo que VES funcionando en el servidor  ║
   ║   for3s. Terminas → marcas ✅ → sigue el siguiente. Sin esperas,    ║
   ║   sin "esto va en otro R", sin avanzar a ciegas por capa.          ║
   ║                                                                    ║
   ║   MVP pilotable en ~4-5 semanas (H4). Sistema completo ~9-10 meses ║
   ║   (H16 → clientes reales).                                         ║
   ║                                                                    ║
   ║   Los R = la biblioteca técnica. El Grafo = la ley arquitectónica. ║
   ║   ESTE doc = el orden de construcción. Ya no planeamos. Construimos.║
   ╚═══════════════════════════════════════════════════════════════════╝
```

**El siguiente paso concreto:** explicar C0 (preparar el servidor) en detalle y, con tu aprobación, ejecutarlo en for3s.

---

**Fin del Mapa de Construcción Incremental.**