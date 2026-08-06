# Ronda 1 — Compute (Lenguaje + Runtime + Package Manager)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Primera de las 10 rondas técnicas. Decisión LOCKED del stack base de For3s OS.**

**Owner:** Brian López
**Fecha:** 2026-05-30
**Estatus:** ✅ LOCKED
**Modo de debate:** A (yo propongo recomendación, Brian decide)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — fuente de verdad técnica
- [Mente/Doc/Banco_Filtro_Alineacion.md](memory/archive/Banco_Filtro_Alineacion.md) — candidatos filtrados
- [Mente/Doc/Estado_Sesion_Continuidad.md](memory/Estado_Sesion_Continuidad.md) — protocolo operativo

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core
- 3.D — Equipo pequeño contratado (2-3 personas)

**Regla de decisión LOCKED en esta ronda:**
> "La fuente de verdad es el Grafo Maestro. El expertise se contrata. La tecnología se elige por criterio técnico, no por preferencia del founder."

---

## Tabla de contenidos

1. [Decisión LOCKED](#1-decisión-locked)
2. [Contexto — qué es esta capa y por qué importa](#2-contexto--qué-es-esta-capa-y-por-qué-importa)
3. [Restricciones operativas de Brian](#3-restricciones-operativas-de-brian)
4. [Candidatos evaluados](#4-candidatos-evaluados)
5. [Tabla comparativa contra el Grafo Maestro](#5-tabla-comparativa-contra-el-grafo-maestro)
6. [Por qué Python (criterio técnico, sin sesgo de expertise)](#6-por-qué-python-criterio-técnico-sin-sesgo-de-expertise)
7. [Por qué se descartaron los demás](#7-por-qué-se-descartaron-los-demás)
8. [Stack Python específico — sub-decisiones LOCKED](#8-stack-python-específico--sub-decisiones-locked)
9. [Estructura de directorio del proyecto](#9-estructura-de-directorio-del-proyecto)
10. [Plan de validación — primer hito visible](#10-plan-de-validación--primer-hito-visible)
11. [Implicaciones en otras rondas](#11-implicaciones-en-otras-rondas)
12. [Pendientes y trade-offs aceptados](#12-pendientes-y-trade-offs-aceptados)
13. [Cómo se conecta con el diario de mayo 2026](#13-cómo-se-conecta-con-el-diario-de-mayo-2026)

---

## 1. Decisión LOCKED

```
   ╔══════════════════════════════════════════════════════════╗
   ║                                                          ║
   ║   RONDA 1 — DECISIÓN LOCKED 2026-05-30                    ║
   ║                                                          ║
   ║   🐍 LENGUAJE BASE:    Python 3.12+ (fallback 3.11)       ║
   ║   📦 PACKAGE MANAGER:  uv (Astral, Rust-based)            ║
   ║   🌐 FRAMEWORK WEB:    FastAPI                            ║
   ║   🔍 VALIDACIÓN:       Pydantic v2                        ║
   ║   ✅ TYPE CHECKER:     ty (Astral) con pyright fallback   ║
   ║   🧹 LINTER/FORMAT:    ruff (Astral, Rust-based)          ║
   ║   🧪 TESTING:          pytest + pytest-asyncio + timeout  ║
   ║   ⚡ ASYNC:            asyncio + anyio                    ║
   ║   📂 MONOREPO:         uv workspaces                      ║
   ║   🖥️  CLI/TUI:          rich + prompt_toolkit              ║
   ║                                                          ║
   ║   FRONTEND v1:                                            ║
   ║   ❌ NO React/Vue/Angular                                 ║
   ║   ✅ Telegram (python-telegram-bot)                       ║
   ║   ✅ Dashboard sencillo (Streamlit o FastAPI+HTMX)        ║
   ║   ⏸️  Frontend web pulido = roadmap futuro                 ║
   ║                                                          ║
   ╚══════════════════════════════════════════════════════════╝
```

**Stack confirmado en una línea:**

> Python 3.12 + uv + FastAPI + Pydantic v2 + ty + ruff + pytest + rich, con interfaces vía Telegram/WhatsApp y dashboard interno en Streamlit/HTMX.

---

## 2. Contexto — qué es esta capa y por qué importa

R1 es la decisión más bloqueante de las 10 rondas. Define:

- Qué frameworks AI están disponibles después (R2 Data, R3 Model, R6 Agent Runtime)
- Qué librerías nativas tenemos para el Grafo Maestro
- Qué velocidad de desarrollo tiene el equipo
- Qué perfil técnico se contrata (Ancla 3.D)
- Qué tan directo se extiende/integra con Hermes (referencia técnica)
- Qué imágenes Docker / deployment strategy aplica (R5 Deployment)

**Si se elige mal aquí, las siguientes 9 rondas se complican o tienen que reciclar decisiones.**

### Qué dice el Grafo Maestro sobre esta capa

El Grafo Maestro NO especifica un lenguaje único. Especifica que:

- Cada nodo cerebral es un servicio independiente (§pilar 2 Escalabilidad)
- LLM (Claude Sonnet) + LangGraph aparecen en Nodo 3 PFC como referencia técnica
- Skills procedurales son markdown + YAML (Nodo 4)
- Vector DB (Qdrant/pgvector) en Nodo 2
- Jobs periódicos para Microglía, DMN, Consolidación (Nodos 5, 6, 10)
- Multi-platform integration (input vía PR/Query/Comando/Webhook/CI/CD)

El Grafo es **lenguaje-agnóstico en superficie**, pero las primitivas mencionadas (LangGraph, Qdrant, Claude SDK) tienen su mejor expresión en el ecosistema Python.

---

## 3. Restricciones operativas de Brian

Decisiones que Brian aclaró durante el debate de R1 y que filtraron la decisión:

### 3.1 Frontend NO es el producto en v1

**Aclaración textual de Brian:**
> "Frontend ahorita no vamos a hacer tanto, solo para pruebas. Vamos a ocupar lo que hace OpenClaw, Hermes — que lo conectamos a una app como Telegram o WhatsApp o creamos un dashboard sencillo para prueba de funcionamiento y escalabilidad."

**Implicación:** Frontend web rico (React/Vue/Angular + TypeScript) **NO es necesario en v1**. Se descarta como driver para TypeScript en el stack core.

**Dashboard web pulido:** mencionado como objetivo de fase futura — probablemente v3 cuando For3s OS sea SaaS B2B vendible vía dashboard.

### 3.2 La fuente de verdad técnica es el Grafo Maestro, no el expertise del founder

**Aclaración textual de Brian:**
> "Mi error fue no haber preguntado y asumido de lo que yo sé. Lo que yo sé es una cosa que se puede tomar en consideración. Pero el punto de verdad es qué tecnología es capaz de hacer realidad For3s_OS_Grafo_Maestro.md. Esa es la fuente de verdad. Si yo no sé un lenguaje pero es ideal o es necesario para la construcción, no importa, se contrata a alguien experto en ese tema. El expertise es algo que puedo conseguir, lo que importa es que sea la tecnología correcta para hacerlo realidad."

**Implicación:** **Brian es Python expert** se considera, pero NO es el factor decisivo. La decisión se justifica con criterio técnico independiente.

### 3.3 Primer hito visible alineado con su visión

Brian confirmó:

> "¿Aceptas que el primer hito visible será 'For3s OS corriendo en Telegram igual que Hermes' en ~4-6 semanas? Sí, lo necesito."

**Implicación:** El plan de validación de R1 debe incluir un milestone Telegram en 4-6 semanas.

---

## 4. Candidatos evaluados

A diferencia del análisis inicial (Python vs TypeScript solo), se evaluaron **5 lenguajes serios** contra el Grafo Maestro:

| Candidato | Por qué se consideró |
|---|---|
| **Python 3.12+** | Ecosistema AI dominante. Hermes (referencia técnica) es Python. OpenClaw (motor previo de Brian) es Python. MCP SDK Python first-class. |
| **TypeScript / Node.js 22** | Type safety brutal. Frontend unificado (si lo hubiera). Edge computing. Diario mayo de Brian lo declaraba "DEFINIDO". |
| **Rust** | Performance C++. Memory safety. Lo que Anthropic usa en su core backend. Polars y uv internamente en Rust. |
| **Go** | Concurrencia masiva sin GIL. Simplicidad operativa. Imágenes Docker pequeñas. Lo que usa Docker/Kubernetes. |
| **Elixir / Erlang BEAM** | Concurrencia distribuida nativa. Fault tolerance enterprise. Lo que usa WhatsApp para escalar a 900M usuarios con 50 ingenieros. |

**Híbrido Python + TypeScript** se evaluó como opción adicional pero se descartó (ver §7.6).

---

## 5. Tabla comparativa contra el Grafo Maestro

Evaluación contra las 10 dimensiones críticas del Grafo Maestro. Escala: ⭐ (1) a ⭐⭐⭐⭐⭐ (5).

| Dimensión del Grafo | Python | TypeScript | Rust | Go | Elixir/BEAM |
|---|---|---|---|---|---|
| **1. Orquestar agentes IA (LLM calls, multi-agent)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| **2. Pattern separation + Vector DB** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **3. Concurrencia masiva** | ⭐⭐⭐ (GIL) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **4. Seguridad criptográfica E2E** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **5. Skills auto-generadas (Hermes GEPA-style)** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| **6. Workspace isolation + sharding** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **7. Procesos de fondo continuos (Microglía/DMN/CLS)** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **8. Auditoría inmutable (Event Sourcing + chain)** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **9. Multi-platform messaging (Telegram/WhatsApp/etc)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **10. Escalabilidad horizontal por nodo** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **TOTAL** | **41** | **35** | **40** | **41** | **41** |

### Lectura honesta

**Empate técnico:** Python = Go = Elixir/BEAM (41 puntos cada uno).

**Rust:** 40 puntos (1 menos por ecosistema AI inmaduro).

**TypeScript:** 35 puntos (último por ecosistema AI lag de 6-12 meses vs Python).

---

## 6. Por qué Python (criterio técnico, sin sesgo de expertise)

Si Python, Go y Elixir empatan en 41 puntos, ¿por qué Python gana?

**No es por el expertise de Brian.** Es por 4 razones técnicas independientes:

### Razón 1 — Ecosistema AI dominante con primitivas listas

Las primitivas que el Grafo Maestro necesita ya existen maduras en Python:

| Pieza del Grafo | Librería Python | Equivalente Go/Elixir |
|---|---|---|
| Nodo 3 PFC (orquestación) | LangGraph oficial | NO existe maduro |
| Nodo 1 KG | Neo4j Python driver | drivers existen pero menos rico |
| Nodo 2 Hipocampo | qdrant-client, weaviate-client, chromadb | SDKs limitados o ausentes |
| Embeddings | sentence-transformers, OpenAI embeddings | reimplementar o llamar Python |
| Nodo 4 Skills | Markdown + YAML (cualquier lenguaje) | igual |
| Multi-agent | CrewAI, AutoGen, LangGraph | NO existen maduros |
| RAG (Bucket L del banco) | LangChain, LlamaIndex, Vectara | versiones JS limitadas, otros ausentes |

**Reescribir esto en Go/Elixir/Rust = años de trabajo para 2-3 personas (Ancla 3.D rota).**

### Razón 2 — Hermes (referencia técnica) ya validó Python para este caso de uso

Hermes Agent (Nous Research) hace **exactamente** lo que For3s OS necesita en v1:
- Multi-platform messaging (20+ plataformas incluido Telegram)
- Skills auto-generadas con GEPA (paper ICLR 2026)
- Three-tier memory (Core + Session FTS5 + External providers)
- Multi-model support (200+ models)
- 6 backends de ejecución (Local, Docker, SSH, Modal, Daytona, Singularity)

Hermes está **100% en Python**. Si para extender o aprender de Hermes elegimos otro lenguaje, perdemos esta referencia técnica directa.

### Razón 3 — OpenClaw + outcome data previo en Python

Brian construyó OpenClaw en Python. Los 3 agentes operativos (Fruterito Personal, Empleado, Design) corren OpenClaw. El outcome data acumulado son:
- 200+ sesiones de Fruterito Personal
- 65 sesiones + **23 skills desarrollados** en Fruterito Empleado
- 5,892 archivos en backup Google Drive

**Esto es capital técnico Python existente.** Si elegimos otro lenguaje, se descarta. Si elegimos Python, se reutiliza.

### Razón 4 — MCP SDK Python es first-class

El Model Context Protocol (MCP) apareció **2 veces en el banco** (#66 y #77) — señal de fundacionalidad para Brian. Anthropic publica primero el SDK Python, después el TypeScript. Los servers MCP populares (filesystem, postgres, github, slack) tienen referencias de implementación en Python.

For3s OS será MCP-native. Python = integración first-class con Claude/Anthropic.

### Resumen de las 4 razones

```
   ╔══════════════════════════════════════════════════════════╗
   ║   PYTHON GANA POR CRITERIO TÉCNICO PURO                    ║
   ║   (sin recurrir al expertise de Brian):                    ║
   ║                                                          ║
   ║   1. Ecosistema AI dominante con primitivas maduras       ║
   ║   2. Hermes (referencia técnica) ya validó Python         ║
   ║   3. OpenClaw + 23 skills = capital técnico Python        ║
   ║   4. MCP SDK Python first-class con Anthropic             ║
   ║                                                          ║
   ║   El expertise de Brian es bonus operativo,                ║
   ║   no la razón técnica.                                    ║
   ║                                                          ║
   ╚══════════════════════════════════════════════════════════╝
```

---

## 7. Por qué se descartaron los demás

### 7.1 ❌ TypeScript / Node.js

**Razones del descarte:**

- Ecosistema AI Python lidera 6-12 meses vs TS (LangChain Python > LangChain.js)
- No hay frontend rico en v1 (Brian aclaró: solo Telegram + dashboard simple) → 60% del caso para TS desaparece
- Type safety brutal (mejor que Python) no compensa la ausencia de primitivas AI
- Bus factor del equipo (Brian master Python, competente TS) hacia Python
- Hermes / OpenClaw no usan TS

**¿Cuándo se podría reconsiderar?** En v3 si For3s OS necesita dashboard web pulido tipo SaaS B2B vendible. En ese momento se añade frontend React/TS sin tocar el core Python.

### 7.2 ❌ Rust

**Razones del descarte:**

- Curva de aprendizaje brutal (lifetimes, borrow checker)
- Ecosistema AI casi nulo (algunas crates pero nada como LangGraph)
- Equipo de 2-3 personas + Rust = años para productividad (Ancla 3.D rota)
- Reescribir todo lo que Hermes hace = no viable

**¿Cuándo se podría reconsiderar?** Para componentes específicos de performance crítico (criptografía custom, sandboxing, audit chain) podría ser un microservicio Rust llamado desde Python — pero no como lenguaje principal.

### 7.3 ❌ Go

**Razones del descarte:**

- Ecosistema AI muy débil (mejor que Rust pero muy detrás de Python)
- Type system primitivo (sin generics maduros hasta 1.18, aún limitado)
- Reescribir LangGraph en Go = no viable para equipo de 3
- Para llamar LLMs / Vector DBs se acabaría usando Python como subprocess de todas formas

**¿Cuándo se podría reconsiderar?** Como sandboxing layer (Pilar 3 Autonomía Generativa) si Docker exec resulta insuficiente. Microservicio Go para skill execution sandboxed podría tener sentido en v2+.

### 7.4 ❌ Elixir / Erlang BEAM

**Razones del descarte:**

- Ecosistema AI casi inexistente (Bumblebee limitado)
- Pool de talento en LATAM muy pequeño (Ancla 3.D rota)
- Reescribir LangGraph en Elixir = no viable
- A pesar de su excepcional concurrencia y fault tolerance, perdemos el ecosistema AI

**¿Cuándo se podría reconsiderar?** Si For3s OS llegara a escala WhatsApp (>10M usuarios concurrentes), Elixir/BEAM podría ser justificable para el message broker. Irrelevante en v1-v3.

### 7.5 ❌ Otros (Ruby, Java/Kotlin, .NET, etc.)

- **Ruby** — ecosistema AI casi nulo, perfil declinante en LATAM
- **Java / Kotlin con Spring AI** — Spring AI existe pero ecosistema agentes inmaduro, verbose vs Python
- **.NET con Semantic Kernel** — Microsoft empuja .NET para AI pero comunidad limitada, perfil enterprise lento para startup
- **Crystal, Zig, Nim** — comunidades demasiado pequeñas para equipo de 3

### 7.6 ❌ Híbrido Python + TypeScript

**Razones del descarte (8 puntos de fractura identificados):**

1. Schemas duplicados sin ROI (Pydantic + Zod sincronizados manualmente o codegen frágil)
2. Comunicación inter-servicio sin necesidad (chat-first tolera latencia humana 1-3 seg)
3. Onboarding de devs futuros se duplica (3-4 semanas vs 1-2 semanas)
4. Deployment multiplicado (2 Dockerfiles, 2 pipelines CI/CD)
5. Auth flow doble entre Hono y FastAPI
6. Observability fragmentada
7. Bus factor en TS = 1 (Brian no es expert TS)
8. Tiempo perdido en decisiones técnicas duplicadas

**Decisión:** mono-Python en core. Si en futuro (v3+) se justifica TypeScript para frontend rico, se añade entonces como capa separada que habla con backend Python vía REST/WebSocket.

---

## 8. Stack Python específico — sub-decisiones LOCKED

### 8.1 Versión de Python

**LOCKED: Python 3.12+ con fallback a 3.11 si alguna librería crítica no soporta 3.12**

Razones:
- 3.12 trae mejoras de performance significativas (10-60% más rápido en muchas operaciones)
- Better error messages
- Type system mejor (PEP 695 type parameters)
- 3.11 sigue siendo compatibilidad máxima si alguna lib AI tarda en actualizar
- 3.13 aún muy reciente, evitar bleeding edge en v1

### 8.2 Package Manager

**LOCKED: uv (Astral)**

Razones:
- Escrito en Rust, 10-100× más rápido que pip
- Lo que usa Hermes (referencia técnica)
- Resuelve dependencias en paralelo
- Puede instalar Python por sí mismo (no necesitas Python para instalar Python)
- pyproject.toml como single source de configuración
- uv workspaces para monorepo

Descartados:
- **poetry** — estándar histórico pero más lento, menos moderno
- **pip-tools** — clásico, manual, no integra workspace
- **pdm / hatch** — alternativas válidas pero menos momentum que uv
- **rye** — buena alternativa pero menor adopción que uv

### 8.3 Framework Web

**LOCKED: FastAPI**

Razones:
- Estándar de facto en Python para APIs modernas
- Pydantic v2 nativo (validación tipos)
- OpenAPI auto-generado (útil si futuro añadimos frontend con codegen)
- async/await nativo
- Comunidad gigantesca, tutoriales abundantes
- Madurez probada en producción enterprise

Descartados:
- **Starlette** — base de FastAPI, más bajo nivel, demasiado boilerplate
- **Litestar** — alternativa moderna con MSGSpec, menos maduro
- **Django** — overkill para For3s OS (admin/templating no necesario)
- **Flask** — sin async nativo, menos moderno
- **Sanic / Quart** — adopción menor

### 8.4 Validación / Schemas

**LOCKED: Pydantic v2**

Razones:
- Escrito internamente en Rust → ultra rápido (5-50× más rápido que v1)
- Native integration con FastAPI
- Type-safe runtime + static
- Standard del ecosistema AI Python (LangChain, LlamaIndex lo usan)
- Excelente para schemas de skills, workspaces, eventos

Descartados:
- **MSGSpec** — más rápido que Pydantic pero ecosystem fit menor
- **attrs** — no runtime validation
- **dataclasses** estándar — muy básico para For3s OS
- **marshmallow** — más viejo, menos performante

### 8.5 Type Checker

**LOCKED: ty (Astral) con pyright como fallback**

Razones:
- ty es ultrarrápido (escrito en Rust)
- Lo que usa Hermes (consistencia con referencia)
- Astral mantiene también ruff y uv = ecosystem aligned
- Pyright como fallback si ty (v0.0.21) tiene gaps por inmadurez

Descartados:
- **mypy** — estándar histórico pero lento
- **pyre (Facebook)** — abandonado parcialmente
- Solo tener ts sin fallback es riesgoso (es joven)

### 8.6 Linter / Formatter

**LOCKED: ruff (Astral)**

Razones:
- Escrito en Rust, 10-100× más rápido que black + flake8 + isort + pyupgrade combinados
- Reemplaza 7+ herramientas en una sola
- Lo que usa Hermes (consistencia)
- Configuración mínima en pyproject.toml

Descartados:
- **black + flake8 + isort + pylint** — stack tradicional pero fragmentado y lento
- **autopep8** — más limitado

### 8.7 Testing

**LOCKED: pytest + pytest-asyncio + pytest-timeout**

Razones:
- Estándar de facto en Python
- pytest-asyncio para tests async (FastAPI + LangGraph)
- pytest-timeout para evitar tests colgados (30s default como Hermes)
- Ecosistema gigante de plugins

Descartados:
- **unittest** — más viejo, menos ergonómico
- **nose** — abandonado

### 8.8 Async runtime

**LOCKED: asyncio (nativo) + anyio para abstracción**

Razones:
- asyncio es nativo de Python 3.11+, ya excelente
- anyio permite escribir código que funciona con asyncio Y trio
- Compatible con FastAPI y LangGraph

Descartados:
- **trio** — solo trio sería innecesariamente restrictivo
- **uvloop** — ya viene integrado con uvicorn por default

### 8.9 CLI / TUI

**LOCKED: rich + prompt_toolkit**

Razones:
- Lo que usa Hermes para su CLI
- rich: colores, tablas, paneles, spinners, progress bars
- prompt_toolkit: REPL interactivo, completion, history
- DX moderna para CLI de desarrollo y dashboards en terminal

Descartados:
- **textual** — bueno para TUI complejas, overkill para v1
- **click + colorama** — más básico
- **questionary** — solo prompts

### 8.10 Monorepo

**LOCKED: uv workspaces**

Razones:
- Nativo de uv (mismo tool)
- Simple, sin overhead
- Lo que recomienda Astral para monorepos
- Alineado con el patrón Hermes

Descartados:
- **Polylith** — más elegante pero curva de aprendizaje
- **Multi-repo desde día 1** — overhead para equipo de 3

### 8.11 Servidor ASGI

**LOCKED: uvicorn (con workers)**

Razones:
- Estándar para FastAPI
- Performance excelente
- uvloop integrado por default
- Gunicorn como process manager para workers en producción

---

## 9. Estructura de directorio del proyecto

```
for3s-platform/                          # ← raíz del monorepo
│
├── pyproject.toml                       # ← uv workspace root
├── uv.lock                              # ← lockfile
├── .python-version                      # ← Python 3.12
├── .env.example                         # ← variables ejemplo
├── .gitignore
├── README.md
├── CLAUDE.md                            # ← memoria del proyecto (Claude Code pattern)
│
├── apps/                                # ← aplicaciones desplegables
│   ├── api/                             # ← FastAPI backend (R6+)
│   │   ├── pyproject.toml
│   │   └── src/for3s_api/
│   │
│   ├── agent_runtime/                   # ← Core del agente (PFC + nodos)
│   │   ├── pyproject.toml
│   │   └── src/for3s_agent/
│   │
│   ├── worker/                          # ← Jobs background (Microglía, DMN, CLS)
│   │   ├── pyproject.toml
│   │   └── src/for3s_worker/
│   │
│   ├── dashboard/                       # ← Dashboard interno Streamlit/HTMX
│   │   ├── pyproject.toml
│   │   └── src/for3s_dashboard/
│   │
│   └── telegram_bot/                    # ← Integración Telegram (primer hito)
│       ├── pyproject.toml
│       └── src/for3s_telegram/
│
├── packages/                            # ← librerías compartidas internas
│   ├── core/                            # ← lógica del grafo, primitives
│   │   ├── pyproject.toml
│   │   └── src/for3s_core/
│   │
│   ├── shared/                          # ← tipos, utils, schemas comunes
│   │   ├── pyproject.toml
│   │   └── src/for3s_shared/
│   │
│   ├── db/                              # ← SQLAlchemy schemas, migraciones
│   │   ├── pyproject.toml
│   │   └── src/for3s_db/
│   │
│   └── mcp_server/                      # ← MCP server implementation
│       ├── pyproject.toml
│       └── src/for3s_mcp/
│
├── tools/                               # ← scripts de operación
│   ├── install.sh                       # ← installer one-line (Hermes pattern)
│   ├── setup_wizard.py                  # ← wizard interactivo
│   └── ...
│
├── docs/                                # ← documentación técnica
│   ├── architecture.md
│   ├── deployment.md
│   └── onboarding.md
│
└── tests/                               # ← tests del workspace root
    ├── integration/
    └── e2e/
```

### Convenciones

- Cada `app/` y `package/` es un workspace member de uv
- `pyproject.toml` raíz define el workspace
- Cada paquete usa **src layout** (mejor práctica Python 2026)
- Names siguen convención `for3s_*` para evitar colisiones con PyPI
- `CLAUDE.md` en raíz para que Claude Code tenga contexto del proyecto

---

## 10. Plan de validación — primer hito visible

**Meta:** Replicar lo que Hermes hace (CLI + Telegram) en For3s OS para validar el stack en producción real.

### Cronograma 4-6 semanas

#### Semana 1 — Setup y agente mínimo (CLI básico)

```bash
# Init del proyecto
mkdir for3s-platform && cd for3s-platform
uv init
uv add anthropic langgraph pydantic rich prompt_toolkit

# Crear primer agente mínimo
# apps/agent_runtime/src/for3s_agent/main.py
# - Loop interactivo en terminal
# - LLM call a Claude
# - Sin memoria persistente aún
# - Sin tools aún

uv run for3s-agent
```

**Entregable:** Brian habla con For3s OS desde terminal local.

#### Semana 2 — CLI rico (Hermes-style)

```python
# Añadir rich + prompt_toolkit
# - Streaming de respuestas
# - Comandos slash (/help, /reset, /model)
# - Colores y paneles
# - History de comandos
```

**Entregable:** CLI con UX comparable a Hermes/Claude Code.

#### Semana 3 — Persistencia básica (SQLite + FTS5)

```python
# packages/db/src/for3s_db/
# - Schema SQLAlchemy básico
# - Sessions table
# - Messages table
# - FTS5 index para búsqueda

# apps/agent_runtime/src/for3s_agent/
# - Session resume al reabrir
# - Búsqueda de sesiones previas
```

**Entregable:** Sesiones persistentes que sobreviven al cierre.

#### Semana 4 — Integración Telegram

```bash
uv add python-telegram-bot[webhooks]

# apps/telegram_bot/src/for3s_telegram/
# - Bot creado vía @BotFather
# - Auth de usuarios (whitelist por user_id)
# - Webhook o polling
# - Conecta al agent_runtime
```

**Entregable:** **Brian habla con For3s OS desde Telegram, 24/7.**

#### Semana 5 — Profiles (multi-agente)

```python
# Patrón Hermes: profiles aislados
# - hermes-style: `for3s profile create personal --clone`
# - Cada profile con su SOUL.md, memoria, skills
# - Cambio de profile sin reiniciar
```

**Entregable:** Múltiples agentes For3s OS coexistiendo (1 server, N agentes).

#### Semana 6 — Setup wizard + installer

```bash
# tools/install.sh — one-line installer (Hermes pattern)
# tools/setup_wizard.py — config interactiva (modelo, keys, Telegram)

curl -fsSL https://raw.githubusercontent.com/[org]/for3s/main/install.sh | bash
for3s setup
```

**Entregable:** Cualquiera puede instalar For3s OS en ~5 minutos.

### Criterios de éxito del hito 4-6 semanas

✅ For3s OS corre en consola con CLI rico (rich + prompt_toolkit)
✅ Brian habla con For3s OS desde Telegram
✅ Sesiones persistentes en SQLite + FTS5
✅ Multi-profile (al menos 2 agentes simultáneos)
✅ Instalación one-line desde script bash
✅ Stack Python validado en producción real

### Lo que NO está en este hito (es para rondas/fases siguientes)

❌ Knowledge Graph (R2)
❌ Vector DB (R2)
❌ Multi-agent grafo paralelo (R6)
❌ Skills auto-generadas (R6)
❌ Microglía / DMN / Consolidación (R6 fase 2)
❌ Multi-tenant con encryption per-workspace (R4)
❌ Dashboard web pulido (v3)

**Este hito es solo "alcanzar paridad básica con Hermes para validar el stack".** El Grafo Maestro completo se construye encima en rondas siguientes.

---

## 11. Implicaciones en otras rondas

La decisión Python en R1 condiciona las siguientes 9 rondas:

| Ronda | Implicación |
|---|---|
| **R2 Data** | ORM = SQLAlchemy 2 + Alembic. Vector DB drivers Python (qdrant-client, weaviate-client). Knowledge Graph: neo4j Python driver. Polars Python para procesamiento masivo. Redis: redis-py. |
| **R3 Model** | Anthropic SDK Python first-class. LangGraph Python oficial. Multi-provider abstraction posible con LangChain o construir custom. |
| **R4 Security** | `cryptography` library Python para crypto. `pynacl` para libsodium bindings. `python-jose` o `pyjwt` para JWT. HashiCorp Vault Python client. |
| **R5 Deployment** | Docker images Python (slim, alpine, distroless). uvicorn + gunicorn para production. Multistage builds para tamaño optimizado. |
| **R6 Agent Runtime** | LangGraph Python como framework principal. MCP SDK Python. Skills en markdown + YAML (igual Hermes). |
| **R7 Tooling** | MCP servers Python (filesystem, postgres, github, custom). Playwright Python para browser. |
| **R8 Cloud Infra** | Cualquier cloud sirve. AWS/GCP/Azure/Hetzner. Python imágenes Docker estándar. |
| **R9 Observability** | OpenTelemetry Python SDK. Loguru o structlog para logging estructurado. Prometheus client Python. |
| **R10 CI/CD** | GitHub Actions con uv. Tests con pytest. Coverage con pytest-cov. ruff en CI. |

---

## 12. Pendientes y trade-offs aceptados

### 12.1 Pendientes para R2+

- Vector DB específico (Qdrant vs pgvector vs Weaviate vs Pinecone vs Chroma)
- Knowledge Graph DB específico (Neo4j vs Memgraph)
- ORM elección final (SQLAlchemy 2 vs SQLModel)
- Migration tool (Alembic confirmado)
- Cache strategy (Redis confirmado pero detalles en R2)

### 12.2 Trade-offs aceptados con la decisión Python

```
   ⚠️ TRADE-OFFS QUE ASUMIMOS:

   1. GIL (Global Interpreter Lock)
      → Mitigable con multiprocessing + workers
      → Igual que Hermes — funciona en producción

   2. Performance bruta menor que Rust/Go
      → Aceptable para chat-first (latencia humana 1-3 seg)
      → Para CPU-bound crítico, microservicios Rust después

   3. Imágenes Docker más pesadas (200-500MB vs 50-150MB Node)
      → Optimizable con multistage builds + python:slim
      → Aceptable para deployment dedicado

   4. Type safety menos estricta que TypeScript
      → Mitigable con Pydantic v2 + ty + strict mypy
      → Aceptable con disciplina de equipo

   5. No frontend nativo
      → Streamlit/HTMX cubren dashboard interno
      → Frontend pulido = decisión futura v3+
```

### 12.3 Cuándo reevaluar esta decisión

R1 se LOCKEA pero se reevaluaría si:

- Hermes/Nous Research pivotara a otro lenguaje (improbable)
- Anthropic deprecara SDK Python (improbable, es first-class)
- Brian contratara un equipo 100% Go/Elixir y Brian dejara el core (improbable v1)
- Algún nodo específico del Grafo demuestra ser imposible/lento en Python (entonces se extrae a microservicio en lenguaje apropiado)

**El stack Python NO impide añadir componentes Rust/Go en el futuro vía microservicios.** Pero el core es Python.

---

## 13. Cómo se conecta con el diario de mayo 2026

El diario de Brian (`FOR3S-STACK-DEFINED.md`) declaraba en mayo:

> Backend: Node.js 22 LTS + Hono 4.x + Drizzle ORM 0.45+ + Zod 3.24+ + TypeScript 5.7+

**Decisión R1 contradice el diario en backend.** Esto es deliberado y consistente con lo que Brian estableció:

> "Los documentos son ideas que tenía. Ya hace tiempo, entiéndelos que son como mi diario de lo que pensaba hace 3 meses atrás. **No lo tomes como fuente de verdad absoluta.**"

**El diario era TypeScript-first; la decisión actual es Python-first.** Esto refleja:

1. El pensamiento del founder evolucionó en 3 meses (es normal)
2. El Grafo Maestro vino después y es la nueva fuente de verdad
3. La regla "expertise se contrata, criterio técnico decide" se aplicó

**No hay contradicción operativa — hay evolución de pensamiento.**

### Lo que del diario SÍ sigue válido para R1

Algunos componentes del diario son lenguaje-agnósticos y siguen aplicando:

- **Docker + Docker Compose** ✅ — se mantiene (R5 confirmará)
- **PostgreSQL 16** ✅ — probable para R2 Data
- **Redis 7** ✅ — probable para R2 cache
- **Tailscale** ✅ — red privada operativa
- **Ubuntu Server 26.04** ✅ — base del for3s-server
- **Filosofía self-hosted + open core** ✅ — alineado con Ancla 2.B

### Lo que del diario se descarta para R1

- ❌ Node.js 22 LTS → reemplazado por Python 3.12
- ❌ Hono 4.x → reemplazado por FastAPI
- ❌ Drizzle ORM → reemplazado por SQLAlchemy 2 (decisión final en R2)
- ❌ Zod 3.24 → reemplazado por Pydantic v2
- ❌ TypeScript 5.7 → no aplica para backend
- ❌ pnpm + Turborepo → reemplazado por uv workspaces

**React 19 + Vite + Tailwind del diario se reconsidera cuando llegue el momento del dashboard pulido (v3+).**

---

## Cierre

**Ronda 1 cerrada. Python LOCKED.**

```
   ╔══════════════════════════════════════════════════════════╗
   ║                                                          ║
   ║   PRÓXIMO PASO: Ronda 2 — Data Layer                       ║
   ║                                                          ║
   ║   Decisiones que aborda:                                  ║
   ║   • PostgreSQL como BD relacional principal               ║
   ║   • Vector DB (Qdrant / pgvector / Weaviate / Chroma)     ║
   ║   • Knowledge Graph (Neo4j / Memgraph)                    ║
   ║   • Memoria de agentes (Honcho / Mem0 / Zep / custom)     ║
   ║   • Cache (Redis confirmado)                              ║
   ║   • Event Sourcing SÍ/NO                                  ║
   ║   • ORM (SQLAlchemy 2 vs SQLModel)                        ║
   ║                                                          ║
   ║   Modo de debate: B (alta tensión, conversamos)           ║
   ║                                                          ║
   ║   Antes de generar el .md, debatimos las opciones.         ║
   ║                                                          ║
   ╚══════════════════════════════════════════════════════════╝
```

**Brian, dime cuando estés listo para arrancar el debate de R2 Data Layer.**

---

**Fin de Ronda 1.**