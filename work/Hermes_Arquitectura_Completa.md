# Hermes Agent — Arquitectura Técnica Completa

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Hermes_Arquitectura_Completa.md → work/Hermes_Arquitectura_Completa.md (2026-07-30, ADR-029)

## Purpose

Hermes Agent — Arquitectura Técnica Completa


> ⚠️ **DOCUMENTO REFERENCIAL HISTÓRICO (actualizado 2026-06-01)**
>
> Este documento sirvió como **referencia técnica inicial** durante la planeación de For3s OS (Ronda 0 — análisis de candidatos arquitectónicos). For3s OS **divergió significativamente** de Hermes en Rondas 1 y 2 (Bloques 1+2):
>
> - **R1 LOCKED:** Python 3.12+ (Hermes también, ✅ coincidencia validada)
> - **R2 B1 LOCKED:** PostgreSQL + AGE + pgvector (Hermes usa SQLite — divergencia por multi-tenancy)
> - **R2 B2 LOCKED:** Custom memory framework + Stella local embeddings (Hermes usa Qdrant/Chroma opc.)
>
> **Para arquitectura ACTUAL de For3s OS, ver:**
> - [`work/Ronda_01_Compute_Lenguaje.md`](work/Ronda_01_Compute_Lenguaje.md) — runtime + stack
> - [`work/Ronda_02_Bloque_1_Storage_Foundation.md`](work/Ronda_02_Bloque_1_Storage_Foundation.md) — storage layer
> - [`work/Ronda_02_Bloque_2_Memory_Architecture.md`](work/Ronda_02_Bloque_2_Memory_Architecture.md) — memory architecture
>
> Hermes sigue siendo válido como **fuente de inspiración** para el modelo cliente Telegram, sesiones persistentes, tier memory architecture, y validación empírica de Python como stack para agentes en producción.

---

**Reporte exhaustivo de cómo está construido Hermes Agent de Nous Research, para usar como base técnica de For3s OS**

**Owner:** Brian López
**Fecha:** 2026-05-30
**Estatus:** Reporte de inteligencia técnica. Iteración 1.
**Capa:** Cuerpo — implementación ejecutable.
**Propósito:** Mapear con precisión cómo está construido Hermes, qué tecnologías usa, por qué es tan fácil de instalar, y qué de eso For3s OS debe heredar / mejorar / descartar.
**Fuentes:** Documentación oficial de Hermes, repositorio en GitHub (NousResearch/hermes-agent), pyproject.toml v0.15.1, script install.sh, DeepWiki técnico, blogs especializados.
**Documentos relacionados:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md)
- [Mente/Cerebro/Arquitectura_Grafo_vs_Loop.md](../Cerebro/Arquitectura_Grafo_vs_Loop.md)
- [Mente/vision/Vision_For3s_Frontier.md](../vision/Vision_For3s_Frontier.md)
- [Mente/vision/Primeros_Pasos.md](../vision/Primeros_Pasos.md)

---

## Por qué este documento existe

Llegamos a un punto donde necesitas **conocer al competidor a nivel técnico exacto** para poder superarlo. Marketing no basta. Tienes que saber:

- En qué lenguaje está escrito
- Qué frameworks usa
- Cómo está organizado el código
- Cómo persiste datos
- Cómo se comunica con LLMs
- Cómo orquesta tools y subagentes
- **Por qué el instalador es una sola línea y funciona**

Sin esta inteligencia técnica, "For3s mejor que Hermes" es ambición vacía. Con esta inteligencia, es **roadmap concreto**.

---

## Tabla de contenidos

1. [Resumen ejecutivo en 30 segundos](#1-resumen-ejecutivo-en-30-segundos)
2. [Stack tecnológico exacto](#2-stack-tecnológico-exacto)
3. [Estructura del repositorio y archivos clave](#3-estructura-del-repositorio-y-archivos-clave)
4. [Arquitectura de los 3 modos de ejecución](#4-arquitectura-de-los-3-modos-de-ejecución)
5. [El núcleo: AIAgent y el loop de conversación](#5-el-núcleo-aiagent-y-el-loop-de-conversación)
6. [Sistema de proveedores LLM (abstracción)](#6-sistema-de-proveedores-llm-abstracción)
7. [Sistema de tools (70+ herramientas auto-registradas)](#7-sistema-de-tools-70-herramientas-auto-registradas)
8. [Sistema de memoria (SQLite + FTS5 + Markdown)](#8-sistema-de-memoria-sqlite--fts5--markdown)
9. [Sistema de skills (auto-generadas y persistentes)](#9-sistema-de-skills-auto-generadas-y-persistentes)
10. [Sistema de subagentes y backends de ejecución](#10-sistema-de-subagentes-y-backends-de-ejecución)
11. [Gateway de mensajería (20+ plataformas)](#11-gateway-de-mensajería-20-plataformas)
12. [Sistema de prompts con caching y compresión](#12-sistema-de-prompts-con-caching-y-compresión)
13. [Configuración, profiles y HERMES_HOME](#13-configuración-profiles-y-hermes_home)
14. [Por qué el instalador es UNA LÍNEA y funciona](#14-por-qué-el-instalador-es-una-línea-y-funciona)
15. [Lo que Hermes hace BIEN — qué heredar](#15-lo-que-hermes-hace-bien--qué-heredar)
16. [Lo que Hermes hace MAL — qué NO heredar](#16-lo-que-hermes-hace-mal--qué-no-heredar)
17. [El gap que For3s OS debe llenar](#17-el-gap-que-for3s-os-debe-llenar)
18. [Plan de construcción inspirado en Hermes](#18-plan-de-construcción-inspirado-en-hermes)
19. [Fuentes](#19-fuentes)

---

## 1. Resumen ejecutivo en 30 segundos

```
   ┌────────────────────────────────────────────────────────┐
   │  HERMES AGENT v0.15.1 — RESUMEN TÉCNICO                 │
   ├────────────────────────────────────────────────────────┤
   │                                                        │
   │  Lenguaje:        Python 3.11+                         │
   │  Build tool:      setuptools + uv                      │
   │  Licencia:        MIT (open source completo)           │
   │  Repo:            github.com/NousResearch/hermes-agent │
   │  Tamaño:          70+ tools, 20+ messaging adapters,   │
   │                   ~5,000-10,000 líneas Python estimado │
   │                                                        │
   │  Memoria:         SQLite + FTS5 (full-text search)     │
   │                   + Markdown files (MEMORY.md, USER.md)│
   │                                                        │
   │  LLMs:            Abstracción de 3 APIs (Anthropic     │
   │                   Messages, OpenAI Chat Completions,   │
   │                   Codex Responses)                     │
   │                   18+ proveedores soportados           │
   │                                                        │
   │  Backends:        6 (Local, Docker, SSH, Modal,        │
   │                   Daytona, Singularity)                │
   │                                                        │
   │  Plataformas:     20+ (Telegram, Discord, Slack,       │
   │                   WhatsApp, Signal, Email, SMS, etc.)  │
   │                                                        │
   │  Instalación:     curl | bash                          │
   │                   Auto-instala: Python, Node, uv,      │
   │                   SQLite, ripgrep, ffmpeg              │
   │                                                        │
   │  Tiempo a corriendo: ~2-5 minutos                      │
   │  Tiempo a configurado: ~15-30 minutos                  │
   │                                                        │
   └────────────────────────────────────────────────────────┘
```

**El insight más importante:** Hermes NO es "un agente". Es **un framework de agente con un excelente onboarding**. La razón por la que es tan fácil de instalar es **diseño deliberado del installer**, no porque el agente sea simple.

---

## 2. Stack tecnológico exacto

Extraído del `pyproject.toml` real (v0.15.1).

### 2.1 Lenguaje y runtime

- **Python 3.11+** (requisito duro, falla si tienes versión menor)
- **Node.js v22 LTS** (para ciertos tools — ripgrep config, MCP servers, ACP)
- **SQLite con FTS5** (para memoria y búsqueda full-text)

### 2.2 Dependencias core (siempre instaladas)

```python
openai==2.24.0                # SDK base — usa formato OpenAI como denominador común
python-dotenv==1.2.2          # Variables de entorno .env
fire==0.7.1                   # CLI auto-generado desde funciones
httpx[socks]==0.28.1          # HTTP cliente moderno, async
rich==14.3.3                  # Terminal UI (colores, tablas, paneles)
tenacity==9.1.4               # Retries con backoff exponencial
pyyaml==6.0.3                 # Config files
ruamel.yaml==0.18.17          # YAML con preservación de comentarios
requests==2.33.0              # HTTP sincrónico legacy
jinja2==3.1.6                 # Template engine para prompts
pydantic==2.13.4              # Validación de tipos y schemas
prompt_toolkit==3.0.52        # REPL interactivo avanzado
croniter==6.0.0               # Cron scheduling
PyJWT[crypto]==2.12.1         # JWT auth para gateway
psutil==7.2.2                 # System monitoring
tzdata==2025.3                # (solo Windows) timezone data
```

**Observación crítica:** NO usan LangChain, NO usan LangGraph, NO usan LlamaIndex, NO usan CrewAI. **Construyeron todo desde cero sobre los SDKs base.** Eso es deliberado — máxima control, mínima dependencia de frameworks que cambian.

### 2.3 Dependencias opcionales (grupos extras)

Estos NO se instalan por default. Se activan con `pip install hermes-agent[grupo]`:

| Grupo | Para qué sirve | Tamaño aprox |
|---|---|---|
| `anthropic` | Claude API nativa | Liviano |
| `messaging` | Telegram + Discord + Slack | Pesado |
| `matrix` | Matrix protocol con encryption | Pesado |
| `web` | FastAPI server para webhook gateway | Medio |
| `voice` | Whisper local + sounddevice | Muy pesado |
| `tts-premium` | ElevenLabs API | Liviano |
| `mcp` | Model Context Protocol | Medio |
| `acp` | Agent Client Protocol (IDEs) | Liviano |
| `modal` | Cloud deployment Modal.com | Medio |
| `daytona` | Cloud deployment Daytona | Medio |
| `bedrock` | AWS Bedrock | Medio |
| `azure-identity` | Azure AD auth | Liviano |
| `google` | Google APIs (Gmail, Docs) | Pesado |
| `youtube` | YouTube transcripts | Liviano |
| `firecrawl` | Web scraping avanzado | Liviano |
| `exa` | Web search Exa.ai | Liviano |
| `fal` | fal.ai image gen | Liviano |
| `honcho` | User modeling cross-session | Medio |
| `homeassistant` | Home Assistant integration | Liviano |
| `feishu`, `dingtalk`, `wecom` | Apps chinas | Medio |
| `termux` | Android via Termux | Liviano |
| `all` | Composite de todo lo importante | Muy pesado |

**Patrón estratégico:** la instalación base es **mínima**. Cada feature pesada es opt-in. Esto es **la razón principal del onboarding rápido** — no instalas lo que no necesitas.

### 2.4 Dependencias de desarrollo

```python
debugpy==1.8.20      # Debugger
pytest==9.0.2        # Testing framework
pytest-asyncio       # Async tests
pytest-timeout       # Timeouts en tests (30s default)
ty==0.0.21           # Type checker rápido (alternativa a mypy)
ruff==0.15.10        # Linter/formatter ultrarrápido (Rust)
```

**Observación:** usan **ty** en lugar de mypy y **ruff** en lugar de black/flake8/isort. Son **las herramientas más modernas y rápidas** del ecosistema Python actual. Eso indica equipo técnico al día.

### 2.5 Entry points (comandos instalados)

```
hermes        → hermes_cli.main:main      # CLI principal interactivo
hermes-agent  → run_agent:main            # Agente headless / API
hermes-acp    → acp_adapter.entry:main    # IDE protocol
```

Tres binarios. Tres modos. Una sola base de código.

---

## 3. Estructura del repositorio y archivos clave

Reconstrucción del layout basada en docs + DeepWiki + análisis de imports.

```
hermes-agent/
├── pyproject.toml           # Config build + deps
├── setup-hermes.sh          # Script setup interactivo
├── scripts/
│   └── install.sh           # Installer cross-platform (UNA LÍNEA)
│
├── run_agent.py             # ⭐ AIAgent class — el núcleo
├── cli.py                   # ⭐ HermesCLI — terminal UI interactiva
├── model_tools.py           # ⭐ Tool discovery + dispatch
├── toolsets.py              # Agrupaciones de tools (28 toolsets)
├── hermes_state.py          # ⭐ SQLite session/state database
│
├── agent/                   # ⭐ Lógica core del agente
│   ├── prompt_builder.py    # Construcción de system prompt
│   ├── context_engine.py    # Abstracción pluggable de contexto
│   ├── context_compressor.py # Compresión lossy cuando supera umbral
│   ├── prompt_caching.py    # Anthropic prefix caching
│   ├── auxiliary_client.py  # LLM auxiliar para side tasks
│   ├── anthropic_adapter.py # Conversión a Messages API
│   ├── memory_manager.py    # Orquesta memory providers
│   ├── memory_provider.py   # ABC para providers de memoria
│   ├── trajectory.py        # Export ShareGPT para training data
│   └── transports/          # ⭐ Abstracción de transporte LLM
│       ├── base.py          # ProviderTransport ABC
│       ├── anthropic.py     # AnthropicTransport
│       ├── chat_completions.py # OpenAI-compatible
│       ├── responses_api.py # Codex Responses API
│       └── bedrock.py       # AWS Bedrock
│
├── tools/                   # ⭐ 70+ tools en 28 toolsets
│   ├── registry.py          # ⭐ Auto-registración al import
│   ├── terminal_tool.py     # 6 backends de ejecución
│   ├── browser_tool.py      # 10 herramientas de browser
│   ├── web_tools.py         # Search + extraction
│   ├── file_tools.py        # Read/write/patch files
│   ├── mcp_tool.py          # Cliente MCP dinámico
│   ├── delegate_tool.py     # Spawn de subagentes
│   ├── skill_manage.py      # Crear/editar/aplicar skills
│   ├── execute_code.py      # Programmatic Tool Calling
│   └── ... (66+ tools más)
│
├── hermes_cli/              # CLI específico
│   ├── main.py              # Entry point CLI
│   ├── config.py            # Config con env overrides
│   ├── setup.py             # Wizard interactivo
│   ├── skills_config.py     # Per-platform skill enable/disable
│   └── tools_config.py      # Per-platform tool enable/disable
│
├── gateway/                 # ⭐ Mensajería multi-plataforma
│   ├── run.py               # GatewayRunner API server
│   ├── session.py           # Conversation persistence
│   └── platforms/           # 20 adapters
│       ├── telegram.py
│       ├── discord.py
│       ├── slack.py
│       ├── whatsapp.py
│       ├── signal.py
│       ├── matrix.py
│       ├── mattermost.py
│       ├── email.py
│       ├── sms.py
│       ├── dingtalk.py
│       ├── feishu.py
│       ├── wechat.py
│       ├── qq.py
│       ├── teams.py
│       ├── google_chat.py
│       ├── homeassistant.py
│       ├── webhook.py
│       └── api_server.py
│
├── acp_adapter/             # IDE integration (Zed, VS Code, JetBrains)
│   └── entry.py             # JSON-RPC over stdio
│
├── cron/                    # Scheduled jobs
│   └── jobs.json            # First-class agent tasks
│
├── plugins/                 # Plugin ecosystem
│   ├── memory/              # Memory providers pluggable
│   └── context_engine/      # Context engines pluggable
│
└── runtime_provider.py      # Resolución (provider, model) → API config
```

**Lectura clave:** ~10-15 archivos centrales hacen el trabajo pesado. El resto son tools individuales y adapters. **Hermes no es un monolito gigante — es una colección de módulos pequeños bien organizados.**

### 3.1 Los 7 archivos más importantes

Si tuvieras que entender Hermes en una tarde, leerías estos en orden:

1. **`run_agent.py`** — AIAgent class, el loop de conversación
2. **`model_tools.py`** — cómo se descubren y despachan tools
3. **`hermes_state.py`** — schema SQLite, persistencia
4. **`agent/prompt_builder.py`** — cómo se construye el system prompt
5. **`agent/transports/base.py`** — abstracción de LLM providers
6. **`tools/registry.py`** — patrón de auto-registración
7. **`cli.py`** — cómo se conecta todo en la UI terminal

---

## 4. Arquitectura de los 3 modos de ejecución

Hermes tiene **un solo cerebro** (AIAgent) que se expone de 3 formas:

```
   ╔════════════════════════════════════════════════════════╗
   ║          AIAgent (run_agent.py)                         ║
   ║  ┌───────────────────────────────────────────────┐     ║
   ║  │  Conversation loop                            │     ║
   ║  │  Tool dispatch                                │     ║
   ║  │  State persistence (SQLite)                   │     ║
   ║  │  Prompt building                              │     ║
   ║  │  Provider abstraction                         │     ║
   ║  └───────────────────────────────────────────────┘     ║
   ╚═══════════╤═══════════════╤═══════════════╤════════════╝
               │               │               │
       ┌───────┴────┐   ┌──────┴────┐   ┌─────┴──────┐
       ▼            ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐
   │  CLI   │  │ GATEWAY │  │   ACP   │  │  WEB UI  │
   │        │  │         │  │         │  │ (opcional)│
   │ cli.py │  │ gateway │  │ acp_    │  │          │
   │        │  │ /run.py │  │ adapter │  │          │
   └────────┘  └─────────┘  └─────────┘  └──────────┘
   Terminal    Telegram     Zed          Browser
   interactivo Discord      VS Code      dashboard
   con Rich    Slack...     JetBrains
```

### 4.1 Modo CLI (`cli.py`)

- Terminal interactivo con TUI basado en `rich` + `prompt_toolkit`
- Comandos slash (`/model`, `/setup`, `/help`)
- Streaming de respuestas
- Color sintáctico para code blocks
- Session se guarda en SQLite al cerrar
- Resume automático al abrir

### 4.2 Modo Gateway (`gateway/run.py`)

- HTTP/webhook server (FastAPI cuando `[web]` está instalado)
- Recibe mensajes de 20+ plataformas
- Sesión por usuario por plataforma
- Authorization (qué usuarios pueden hablar con el agente)
- Cross-session mirroring (mismo usuario en Telegram y Discord = una conversación)
- DM pairing automático

### 4.3 Modo ACP (`acp_adapter/entry.py`)

- Agent Client Protocol over JSON-RPC over stdio
- Editor habla con Hermes como un LSP
- UI nativa del editor (no terminal)
- Soporta Zed, VS Code, JetBrains

**Insight de diseño:** los 3 modos comparten el mismo `AIAgent`. **Cambias la interfaz, no el cerebro.** Esto es lo que les permite mantener consistency de comportamiento en todas las plataformas.

---

## 5. El núcleo: AIAgent y el loop de conversación

Esta es la pieza central. Si entiendes esto, entiendes Hermes.

### 5.1 La clase AIAgent

```python
# Reconstrucción simplificada basada en docs

class AIAgent:
    def __init__(
        self,
        provider: str,
        model: str,
        session_id: str | None = None,
        history: list | None = None,
        skills: list | None = None,
        max_iterations: int = 50,
    ):
        self.provider_config = resolve_provider(provider, model)
        self.transport = get_transport(self.provider_config.api_mode)
        self.state = HermesState(session_id)
        self.budget = IterationBudget(max_iterations)
        self.skills = load_skills(skills)
        self.memory = MemoryManager(session_id)
        self.tools = discover_tools()  # auto-registered at import

    def chat(self, message: str) -> str:
        """Single message convenience method."""
        return self.run_conversation(message)

    def run_conversation(self, message: str) -> str:
        # 1. Build prompt
        system_prompt = prompt_builder.build(
            skills=self.skills,
            memory=self.memory,
            tools=self.tools,
            session=self.state,
        )

        # 2. Add user message to history
        self.state.add_message("user", message)

        # 3. Iterative loop
        while self.budget.remaining():
            # 3a. Call LLM via transport abstraction
            response = self.transport.call(
                system=system_prompt,
                messages=self.state.messages,
                tools=self.tools,
            )

            # 3b. Save assistant turn
            self.state.add_message("assistant", response)

            # 3c. Tool calls?
            if response.has_tool_calls:
                for tool_call in response.tool_calls:
                    result = self.handle_function_call(tool_call)
                    self.state.add_tool_result(result)
                self.budget.consume()
                continue  # loop back to LLM

            # 3d. No more tools, we're done
            break

        # 4. Persist final state
        self.state.commit()
        self.memory.update_from_session(self.state)

        return response.text

    def handle_function_call(self, call) -> Any:
        tool = self.tools.get(call.name)
        env = self.resolve_environment(tool)  # local/docker/ssh/etc
        return tool.execute(call.arguments, env=env)
```

**Lo que esta clase orquesta:**

1. **Prompt building** — tier-based (estable + contexto + volátil)
2. **Transport call** — abstrae si es Anthropic/OpenAI/Bedrock
3. **Tool dispatch** — encuentra el tool, lo ejecuta en el environment correcto
4. **State persistence** — SQLite con FTS5
5. **Memory update** — sincroniza con MEMORY.md + Honcho si está
6. **Iteration budget** — evita loops infinitos

### 5.2 IterationBudget

```python
class IterationBudget:
    """Previene loops infinitos de tool calls."""

    def __init__(self, max_iterations: int = 50):
        self.max = max_iterations
        self.used = 0

    def remaining(self) -> int:
        return self.max - self.used

    def consume(self):
        self.used += 1
        if self.used >= self.max:
            raise IterationBudgetExceeded()
```

**Detalle importante:** Hermes tiene un budget HARD (50 iteraciones por default). Si una conversación necesita más, falla explícitamente en lugar de quemar tokens infinitamente.

### 5.3 El loop visual

```
   User: "Analiza este código"
        │
        ▼
   ┌────────────────────────────┐
   │  Prompt Builder            │
   │  Ensambla system prompt:   │
   │   - Identity (estable)     │
   │   - Tool guidance          │
   │   - Skills disponibles     │
   │   - Memoria (volátil)      │
   │   - Mensaje del usuario    │
   └─────────────┬──────────────┘
                 │
                 ▼
   ┌────────────────────────────┐
   │  Transport.call()          │
   │  Convierte a formato del   │
   │  provider activo y envía   │
   └─────────────┬──────────────┘
                 │
                 ▼
   ┌────────────────────────────┐
   │  LLM Response              │
   │  ¿Tool calls?              │
   └──┬────────────────────┬────┘
      │ SÍ                 │ NO
      ▼                    ▼
   ┌──────────┐    ┌──────────────┐
   │ Execute  │    │ Return text  │
   │ tool en  │    │ to user      │
   │ env      │    └──────────────┘
   │ (local/  │
   │  docker) │
   └────┬─────┘
        │
        ▼
   ┌──────────────┐
   │ Add result   │
   │ to history   │
   │ + consume    │
   │   budget     │
   └──────┬───────┘
          │
          └──► loop back to LLM
```

---

## 6. Sistema de proveedores LLM (abstracción)

Esta es una de las piezas más inteligentes de Hermes.

### 6.1 El problema que resuelve

Cada proveedor de LLM tiene API distinta:
- **Anthropic:** `/v1/messages` con formato Messages
- **OpenAI:** `/v1/chat/completions` con formato Chat
- **OpenAI legacy:** `/v1/responses` (Codex Responses)
- **Bedrock:** wrapper AWS sobre Anthropic
- **OpenRouter:** wrapper sobre 100+ modelos
- **Azure:** OAuth diferente
- **Custom endpoints:** locales (LM Studio, vLLM)

Si tu agente solo habla un formato, estás casado con un proveedor. Hermes resuelve esto con **3 transportes que normalizan todo**.

### 6.2 La abstracción ProviderTransport

```python
# agent/transports/base.py

class ProviderTransport(ABC):
    """ABC que cada transport implementa."""

    @abstractmethod
    def convert_messages(self, messages: list) -> Any:
        """De formato Hermes a formato del provider."""

    @abstractmethod
    def convert_tools(self, tools: list) -> Any:
        """De tools registrados a formato del provider."""

    @abstractmethod
    def assemble_kwargs(self, **kwargs) -> dict:
        """Args específicos del provider."""

    @abstractmethod
    def call(self, system: str, messages: list, tools: list):
        """Llama al API y normaliza respuesta."""

    @abstractmethod
    def normalize_response(self, raw: Any) -> NormalizedResponse:
        """Respuesta uniforme sin importar provider."""
```

### 6.3 Las 3 implementaciones

```python
# agent/transports/anthropic.py
class AnthropicTransport(ProviderTransport):
    """Para Anthropic Messages API directo."""
    api_mode = "anthropic_messages"

# agent/transports/chat_completions.py
class ChatCompletionsTransport(ProviderTransport):
    """Para OpenAI Chat Completions y compatibles.
    Sirve para: OpenAI, OpenRouter, LM Studio, vLLM,
                Together, Groq, Fireworks, Mistral, Nous Portal..."""
    api_mode = "chat_completions"

# agent/transports/responses_api.py
class ResponsesApiTransport(ProviderTransport):
    """Para Codex/legacy Responses API."""
    api_mode = "codex_responses"

# agent/transports/bedrock.py
class BedrockTransport(ProviderTransport):
    """AWS Bedrock — usa formato Anthropic pero auth IAM."""
    api_mode = "bedrock"
```

### 6.4 El resolver

```python
# runtime_provider.py

def resolve_provider(provider: str, model: str) -> ProviderConfig:
    """
    Maps (provider, model) → (api_mode, api_key, base_url).

    Soporta 18+ proveedores:
    - anthropic
    - openai
    - openrouter
    - nous_portal
    - bedrock
    - azure
    - mistral
    - groq
    - together
    - fireworks
    - perplexity
    - cohere
    - google_gemini
    - local (LM Studio, vLLM, Ollama)
    - custom (cualquier OpenAI-compatible endpoint)
    - ...
    """
    config = PROVIDER_REGISTRY[provider]
    return ProviderConfig(
        api_mode=config.api_mode,
        api_key=resolve_credentials(provider),
        base_url=config.base_url,
        model=resolve_model_alias(model, provider),
    )
```

### 6.5 Lo que esto te da

**Para el usuario:** cambia de Claude a GPT-4 a un LLM local con un comando:

```bash
hermes model anthropic claude-3.5-sonnet
hermes model openai gpt-4o
hermes model local llama-3.1-70b   # corre en tu máquina
```

**Para el desarrollador:** agregar un proveedor nuevo = una clase de ~200 líneas implementando `ProviderTransport`.

**Esta es la razón principal por la que Hermes evita la "lección 5.7 del founder-thesis" (riesgo de dependencia externa).** Tienen abstracción real, no marketing.

---

## 7. Sistema de tools (70+ herramientas auto-registradas)

Esta es **la parte más elegante de Hermes** desde perspectiva de ingeniería.

### 7.1 El patrón de auto-registración

```python
# tools/registry.py

_REGISTRY: dict[str, Tool] = {}

def register(name: str, schema: dict):
    """Decorador para registrar una tool."""
    def decorator(func):
        _REGISTRY[name] = Tool(name=name, schema=schema, fn=func)
        return func
    return decorator

def get_all_tools() -> list[Tool]:
    return list(_REGISTRY.values())
```

### 7.2 Cómo se registra una tool

```python
# tools/file_tools.py

from tools.registry import register

@register(
    name="read_file",
    schema={
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "encoding": {"type": "string", "default": "utf-8"},
        },
        "required": ["path"],
    },
)
def read_file(path: str, encoding: str = "utf-8") -> str:
    with open(path, encoding=encoding) as f:
        return f.read()
```

**Eso es todo.** El decorador `@register` añade la tool al registry al momento del import.

### 7.3 El descubrimiento mágico

```python
# model_tools.py

import tools  # ← este import dispara los registers de TODAS las tools

def get_available_tools() -> list[Tool]:
    return registry.get_all_tools()
```

**Aquí está la magia:** `import tools` ejecuta el `__init__.py` del paquete, que importa todos los archivos de tools, que ejecutan los `@register`. **Cuando `AIAgent` se crea, las 70+ tools ya están ahí.**

No hay listas manuales que mantener. No hay configuración. Añades un archivo nuevo a `tools/` y queda disponible.

### 7.4 Las 28 toolsets

Los 70+ tools se agrupan en 28 "toolsets" (`toolsets.py`):

```python
TOOLSETS = {
    "file_ops": ["read_file", "write_file", "patch_file", "list_dir", ...],
    "terminal": ["execute_command", "background_process", ...],
    "browser": ["navigate", "click", "type", "screenshot", ...],
    "web_search": ["search", "extract", "summarize_url", ...],
    "mcp": ["mcp_call", "mcp_list_tools", ...],
    "delegate": ["spawn_subagent", "join_subagent", ...],
    "skills": ["skill_create", "skill_apply", "skill_list", ...],
    "code_exec": ["execute_code", "execute_in_sandbox", ...],
    "memory": ["recall", "remember", "forget", ...],
    "voice": ["speak", "transcribe", ...],
    "vision": ["describe_image", "detect_objects", ...],
    "scheduling": ["schedule_job", "list_jobs", ...],
    "kanban": ["create_task", "update_task", "list_board", ...],
    # ... 15 más
}
```

El usuario puede habilitar/deshabilitar toolsets enteros con `hermes tools`.

### 7.5 Los tools críticos a entender

**`terminal_tool.py`** — el más importante:
- Ejecuta comandos en uno de 6 backends
- Local: subprocess directo
- Docker: contenedor con namespace isolation
- SSH: máquina remota
- Modal: serverless en Modal.com
- Daytona: serverless en Daytona
- Singularity: HPC clusters

**`delegate_tool.py`** — spawn de subagentes:
- Crea un AIAgent nuevo con conversación aislada
- Le da una tarea
- Espera output (o suelta para paralelo)
- Hasta 8 subagentes paralelos (ThreadPoolExecutor)

**`skill_manage.py`** — el corazón del aprendizaje:
- `skill_create(name, description, steps)` → escribe markdown en `~/.hermes/skills/`
- `skill_apply(name, context)` → carga skill y la usa en el prompt
- `skill_list()` → lista todas las skills disponibles
- Skills son markdown plano — el agente las escribe, el usuario las puede editar

**`mcp_tool.py`** — Model Context Protocol:
- Cliente MCP dinámico
- Permite conectar a servers MCP arbitrarios
- Los tools del MCP server aparecen como tools nativos
- Filtros configurables (qué tools del MCP exponer)

---

## 8. Sistema de memoria (SQLite + FTS5 + Markdown)

Hermes mezcla **dos sistemas de memoria distintos** intencionalmente.

### 8.1 Memoria episódica: SQLite + FTS5

Toda conversación se guarda en SQLite con full-text search:

```sql
-- Schema simplificado (reconstrucción)

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    platform TEXT,           -- cli, telegram, discord, etc
    user_id TEXT,
    profile TEXT,            -- per-profile isolation
    parent_session_id TEXT,  -- lineage para compresiones
    metadata JSON
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id),
    role TEXT,               -- user, assistant, tool
    content TEXT,
    tool_calls JSON,         -- si role=assistant con tools
    tool_call_id TEXT,       -- si role=tool
    timestamp TIMESTAMP,
    iteration INTEGER        -- # en el budget
);

-- FTS5 virtual table para búsqueda full-text
CREATE VIRTUAL TABLE messages_fts USING fts5(
    content,
    session_id UNINDEXED,
    role UNINDEXED,
    tokenize = 'porter unicode61'
);
```

**Lo que esto permite:**
- Buscar "todas las veces que el usuario habló de X" en milisegundos
- Resume sesión exacta al reabrir
- Cross-session search ("¿cuándo trabajamos en Y?")
- Lineage tracking (sesión comprimida → sesión original)

### 8.2 Memoria semántica: archivos Markdown

Pero la memoria "destilada" sobre el usuario vive en **archivos markdown**:

```
~/.hermes/
├── MEMORY.md      # Hechos consolidados, preferencias, decisiones
├── USER.md        # Modelo del usuario (perfil)
├── SOUL.md        # Identidad/persona del agente
└── skills/
    ├── skill_1.md
    ├── skill_2.md
    └── ...
```

**Por qué markdown y no más SQLite:**
1. Humano puede leer/editar
2. Git-friendly (versionado natural)
3. Portable (mueves archivos = mueves memoria)
4. Auditable (ves exactamente qué "sabe" el agente sobre ti)

### 8.3 El memory manager

```python
# agent/memory_manager.py

class MemoryManager:
    """Orquesta múltiples memory providers."""

    def __init__(self, session_id: str):
        self.providers = []  # pluggable
        self.session_id = session_id

    def register_provider(self, provider: MemoryProvider):
        self.providers.append(provider)

    def recall(self, query: str) -> list[Memory]:
        """Trae memorias relevantes desde TODOS los providers."""
        results = []
        for p in self.providers:
            results.extend(p.recall(query, session=self.session_id))
        return self._rank_and_dedupe(results)

    def update_from_session(self, state: HermesState):
        """Después de una sesión, propaga lo aprendido a providers."""
        for p in self.providers:
            p.update(state)
```

### 8.4 Memory providers pluggables

`agent/memory_provider.py` define una ABC. Cualquiera puede escribir un provider:

```python
class MemoryProvider(ABC):
    @abstractmethod
    def recall(self, query: str, session: str) -> list[Memory]: ...

    @abstractmethod
    def update(self, state: HermesState) -> None: ...
```

Providers que vienen con Hermes:
- **SQLiteMemoryProvider** — el default, FTS5 search
- **MarkdownMemoryProvider** — lee MEMORY.md y USER.md
- **HonchoMemoryProvider** — opcional, usa honcho.dev para "dialectic user modeling"

### 8.5 Honcho — la pieza interesante

[Honcho](https://honcho.dev) es un servicio externo que Hermes integra opcionalmente para:

- **Dialectic user modeling** — construye modelo del usuario inferido
- Cross-session continuity más rica que SQLite plano
- Modelo del usuario evoluciona con cada interacción

Es un **producto separado**, no parte de Hermes. Lo integran via plugin.

### 8.6 Las "periodic nudges"

Aquí está una pieza única de Hermes:

```python
# Pseudocódigo conceptual

class MemoryNudger:
    """Periódicamente sugiere al agente actualizar su memoria."""

    def should_nudge(self, session: HermesState) -> bool:
        # ¿Pasaron N turnos sin actualizar memoria?
        # ¿Hay info importante no consolidada?
        # ¿El usuario mencionó algo personal?
        return ...

    def inject_nudge(self, prompt: str) -> str:
        """Añade al prompt: 'Consider updating MEMORY.md if X'."""
        return prompt + NUDGE_TEMPLATE
```

**El agente literalmente se recuerda a sí mismo de mantener su memoria al día.** Esto es el "self-improving" en acción.

---

## 9. Sistema de skills (auto-generadas y persistentes)

Esta es la pieza más cerebral de Hermes — equivalente a los ganglios basales.

### 9.1 Qué es una skill

Una skill es un **archivo markdown** que describe cómo resolver un tipo de problema:

```markdown
# skill: deploy_python_app

## Cuándo aplicar
Cuando el usuario pide deploy de una app Python a producción.

## Pasos
1. Verifica que existe requirements.txt o pyproject.toml
2. Detecta plataforma deseada (Heroku/Railway/Modal/Fly.io)
3. Crea archivos de config específicos
4. Ejecuta deploy
5. Verifica health check post-deploy

## Aprendizajes acumulados
- Si la app usa SQLite, Railway > Heroku (Heroku no persiste)
- Modal funciona mejor para apps async
- Fly.io requiere Dockerfile, otros no

## Herramientas que uso
- read_file, list_dir
- execute_command
- web_search (para troubleshooting)
```

### 9.2 Cómo nace una skill

```python
# Conceptual — basado en docs de skill_manage.py

class SkillManager:
    def detect_skill_opportunity(self, session: HermesState):
        """Detecta si esta sesión califica para nueva skill."""
        if self._task_completed_successfully(session):
            if self._pattern_seen_before(session, threshold=3):
                if not self._skill_already_exists(session.intent):
                    return True
        return False

    def create_skill_from_session(self, session: HermesState) -> Skill:
        """Genera skill desde sesión exitosa."""
        # 1. LLM extrae los pasos genéricos
        steps = self._llm_extract_steps(session)
        # 2. LLM identifica trigger ("cuándo aplicar")
        trigger = self._llm_extract_trigger(session)
        # 3. LLM identifica herramientas usadas
        tools_used = self._collect_tools(session)
        # 4. Escribe markdown
        skill_md = SKILL_TEMPLATE.format(
            name=session.intent,
            trigger=trigger,
            steps=steps,
            tools=tools_used,
        )
        # 5. Guarda en ~/.hermes/skills/
        Path(SKILLS_DIR / f"{name}.md").write_text(skill_md)
```

### 9.3 Cómo se aplica una skill

```python
# Conceptual

def build_prompt_with_skills(query: str, available_skills: list):
    relevant = match_skills(query, available_skills)
    if relevant:
        prompt_addition = "Para esta tarea, considera las skills:\n"
        for skill in relevant:
            prompt_addition += f"\n## {skill.name}\n{skill.content}"
        return query + prompt_addition
    return query
```

La skill se **inyecta al system prompt** cuando es relevante. El LLM la usa como guía.

### 9.4 Por qué esto es genial

- **Markdown plain** — auditable, editable, portable
- **Auto-generado** — el agente aprende sin código nuevo
- **Compartible** — skills se pueden subir al "Skills Hub" (agentskills.io)
- **Open standard** — compatible con otros agentes futuros

### 9.5 Por qué esto es limitado (oportunidad For3s)

- **Sin vía NO-GO** — solo aprende qué hacer, no qué evitar
- **Sin especialización por dominio** — skills son genéricas
- **Sin scoring dopaminérgico real** — no hay refuerzo por éxito vs fallo
- **Sin combinación inteligente** — skills se aplican una por una, no se componen
- **Sin sandbox** — nuevas skills van directo a producción

For3s OS puede mejorar EXACTAMENTE estos 5 puntos. Esa es ventaja técnica directa.

---

## 10. Sistema de subagentes y backends de ejecución

### 10.1 Los 6 backends

```python
TERMINAL_BACKENDS = {
    "local":      LocalBackend(),       # subprocess en máquina actual
    "docker":     DockerBackend(),       # contenedor isolated
    "ssh":        SSHBackend(),          # máquina remota
    "modal":      ModalBackend(),        # serverless cloud
    "daytona":    DaytonaBackend(),      # serverless dev environments
    "singularity": SingularityBackend(), # HPC clusters
}
```

Cada uno implementa la misma interfaz:

```python
class Backend(ABC):
    @abstractmethod
    def execute(self, command: str, cwd: str | None = None) -> Result:
        """Ejecuta comando en este backend."""

    @abstractmethod
    def upload(self, local_path: str, remote_path: str): ...

    @abstractmethod
    def download(self, remote_path: str, local_path: str): ...
```

### 10.2 Por qué importa

El mismo agente puede:
- Correr código **localmente** para tareas rápidas
- Spawn **Docker** para isolation cuando es código riesgoso
- Conectar **SSH** a un VPS del usuario
- **Modal** para tareas que necesitan GPU
- **Daytona** para dev environments efímeros

**Sin re-escribir nada.** El usuario configura el backend, el agente lo usa transparente.

### 10.3 Subagentes paralelos

```python
# tools/delegate_tool.py — conceptual

@register("delegate")
def delegate(task: str, subagent_id: str = None) -> str:
    """Spawn subagente para tarea específica."""
    subagent = AIAgent(
        provider=parent_agent.provider,
        model=parent_agent.model,
        session_id=f"sub_{uuid.uuid4()}",
        history=[],  # ← conversación aislada
    )
    return subagent.chat(task)

# Con ThreadPoolExecutor para paralelo
def parallel_delegate(tasks: list[str]) -> list[str]:
    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(delegate, tasks))
```

**Hasta 8 subagentes paralelos.** Cada uno tiene su propia conversación, su propio context window, su propio budget de iteraciones.

### 10.4 Container hardening

En modo Docker, Hermes aplica:
- Namespace isolation (PID, network, mount)
- Read-only filesystem por default (con mounts específicos)
- No root inside container
- Network restrictions configurable
- Resource limits (CPU, memory)

Esto es **importante para For3s** — es el modelo de seguridad que sirve cuando el agente ejecuta código del cliente.

---

## 11. Gateway de mensajería (20+ plataformas)

### 11.1 La arquitectura

```
   ┌─────────────────────────────────────────────────────┐
   │   GatewayRunner (gateway/run.py)                    │
   │   FastAPI server, recibe webhooks/eventos           │
   └────────────────────┬────────────────────────────────┘
                        │
              ┌─────────┴─────────┐
              │  Platform Router  │
              └─────────┬─────────┘
                        │
   ┌────────────────────┼────────────────────────────┐
   │                    │                            │
   ▼                    ▼                            ▼
┌────────┐         ┌────────┐                  ┌────────┐
│Telegram│         │Discord │     ...          │Signal  │
│adapter │         │adapter │     20+          │adapter │
└───┬────┘         └───┬────┘                  └───┬────┘
    │                  │                           │
    └──────────────────┼───────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │ Session Manager│
              │ (gateway/      │
              │  session.py)   │
              └────────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │    AIAgent     │
              │  (run_agent.py)│
              └────────────────┘
```

### 11.2 Patrón de adapter

Cada plataforma implementa:

```python
class PlatformAdapter(ABC):
    @abstractmethod
    async def on_message(self, event: dict) -> None:
        """Callback cuando llega mensaje en esta plataforma."""

    @abstractmethod
    async def send_message(self, user_id: str, text: str) -> None: ...

    @abstractmethod
    async def authorize(self, user_id: str) -> bool:
        """¿Este usuario puede hablar con el agente?"""

    @abstractmethod
    def normalize_event(self, raw: dict) -> Message:
        """De formato plataforma a formato Hermes."""
```

### 11.3 Cross-platform mirroring

Lo más impresionante: **el mismo usuario en Telegram y Discord = una conversación**.

```python
# gateway/session.py — conceptual

def resolve_session(event: PlatformEvent) -> Session:
    user = link_user_across_platforms(event)  # ← magic
    return get_or_create_session(user.canonical_id)

def link_user_across_platforms(event):
    # Cliente confirma identidad (login email, OAuth, código)
    # Después: telegram_id → user.canonical_id
    # Después: discord_id → mismo user.canonical_id
    ...
```

Esto es **una capacidad enterprise enorme** que parece simple pero requiere infraestructura.

### 11.4 Qué plataformas soporta

Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email (IMAP/SMTP), SMS (Twilio), DingTalk, Feishu, WeCom, Weixin, QQ Bot, Microsoft Teams, Google Chat, Home Assistant, Webhook genérico, REST API server.

**No están todos al mismo nivel de polish.** Telegram/Discord/Slack están maduros. Otros son más experimentales.

---

## 12. Sistema de prompts con caching y compresión

### 12.1 Construcción tier-based

```python
# agent/prompt_builder.py — conceptual

def build_prompt(skills, memory, tools, session) -> str:
    parts = []

    # TIER 1: Estable (cacheable indefinidamente)
    parts.append(SOUL_MD)                    # identidad
    parts.append(TOOL_GUIDANCE)              # cómo usar tools
    parts.append(format_skills(skills))      # skills disponibles

    # TIER 2: Contexto (cacheable por sesión)
    parts.append(format_attachments(session))  # archivos cargados

    # TIER 3: Volátil (cambia siempre)
    parts.append(format_memory(memory))      # MEMORY.md, USER.md
    parts.append(format_profile())           # perfil del usuario
    parts.append(format_timestamp())         # tiempo actual

    return CACHE_BREAKPOINT.join(parts)
```

### 12.2 Anthropic Prefix Caching

```python
# agent/prompt_caching.py

def insert_cache_breakpoints(prompt_parts: list) -> list:
    """
    Anthropic permite marcar puntos del prompt como cacheables.
    Si el prefijo no cambia entre llamadas, Anthropic NO lo
    reprocesa — ahorra hasta 90% de costo y latencia.
    """
    return [
        {"type": "text", "text": part, "cache_control": {"type": "ephemeral"}}
        if i < len(prompt_parts) - 1 else  # último parte no cacheable
        {"type": "text", "text": part}
        for i, part in enumerate(prompt_parts)
    ]
```

**Esto es 90% más barato para Tier 1 + Tier 2** si no cambian entre turns.

### 12.3 Context compressor

```python
# agent/context_compressor.py

def compress_if_needed(messages: list, token_threshold: int = 60_000):
    if estimate_tokens(messages) > token_threshold:
        # Resume las primeras N/2 mensajes en uno solo
        old_messages = messages[:len(messages)//2]
        summary = llm_summarize(old_messages, target_tokens=2_000)
        return [
            {"role": "system", "content": f"[CONVERSATION SUMMARY]\n{summary}"},
            *messages[len(messages)//2:]
        ]
    return messages
```

**Cuando el contexto crece mucho:** comprime la mitad vieja en un resumen, mantiene la mitad reciente intacta.

**Lineage tracking:** la sesión comprimida apunta a la sesión original para que puedas recuperar detalles si es necesario.

---

## 13. Configuración, profiles y HERMES_HOME

### 13.1 La estructura de directorio

```
~/.hermes/                  # ← HERMES_HOME
├── config.yaml             # Settings principales
├── .env                    # API keys y secrets (gitignored)
├── SOUL.md                 # Identidad/persona del agente
├── MEMORY.md               # Memoria consolidada
├── USER.md                 # Perfil del usuario
├── auth.json               # OAuth tokens
├── memory.db               # SQLite con FTS5
├── memory.db-shm           # SQLite shared memory
├── memory.db-wal           # SQLite write-ahead log
├── sessions/               # Sesiones por plataforma
│   ├── cli/
│   ├── telegram/
│   └── ...
├── skills/                 # Skills auto-generadas
│   ├── skill_1.md
│   └── ...
├── plugins/                # Plugins instalados
│   ├── memory/
│   └── context_engine/
├── hermes-agent/           # Código fuente (cuando se instala git)
├── node/                   # Node.js portable
└── logs/
    └── hermes.log
```

### 13.2 config.yaml ejemplo

```yaml
# ~/.hermes/config.yaml

model:
  provider: anthropic
  name: claude-3-5-sonnet-20241022

skills:
  enabled: true
  auto_load: true
  hub_sync: false

memory:
  enabled: true
  storage: "sqlite"
  path: "~/.hermes/memory.db"
  honcho:
    enabled: false
    workspace_id: ""

tools:
  enabled_toolsets:
    - file_ops
    - terminal
    - browser
    - web_search
    - delegate
    - skills

terminal:
  default_backend: local
  docker:
    image: "hermes/sandbox:latest"
    read_only: true
  ssh:
    profiles:
      production:
        host: example.com
        user: deploy

gateway:
  enabled: false
  platforms:
    telegram:
      enabled: false
      token: ${TELEGRAM_BOT_TOKEN}
    discord:
      enabled: false
      token: ${DISCORD_BOT_TOKEN}

iteration_budget: 50
context_compression_threshold: 60000
```

### 13.3 Profiles (multi-tenant en mismo equipo)

```bash
hermes -p personal      # usa ~/.hermes-personal/
hermes -p work          # usa ~/.hermes-work/
hermes -p client_acme   # usa ~/.hermes-client_acme/
```

**Cada profile = completo aislamiento.** Memoria, skills, sesiones, config, gateway PID — todo separado.

Esta es la base de cómo Hermes maneja "workspaces" — aunque NO con encryption per-workspace como tendrá For3s.

---

## 14. Por qué el instalador es UNA LÍNEA y funciona

Esto es lo que me pediste entender específicamente. Es **la respuesta más importante** del documento.

### 14.1 La línea mágica

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Esto descarga un script de ~600 líneas de bash y lo ejecuta. Resultado: en ~2 minutos tienes Hermes corriendo.

### 14.2 Lo que hace el installer paso a paso

```
   1. CLEAN ENVIRONMENT
      • Limpia PYTHONPATH, PYTHONHOME (evitar conflictos)
      • Set UV_NO_CONFIG=1

   2. DETECT OS
      • Lee /etc/os-release en Linux
      • Detecta Termux (Android)
      • Detecta macOS
      • Para Windows: redirige a install.ps1

   3. RESOLVE INSTALL LAYOUT
      • Non-root user → ~/.hermes/hermes-agent + ~/.local/bin
      • Root on Linux → /usr/local/lib + /usr/local/bin (FHS)
      • Termux → ~/.hermes/hermes-agent + $PREFIX/bin

   4. INSTALL uv (Astral)
      • Si no existe: curl https://astral.sh/uv/install.sh | sh
      • uv = pip/venv en Rust, 10-100× más rápido

   5. INSTALL PYTHON 3.11+
      • uv puede DESCARGAR Python si no existe
      • ensure_fts5() verifica SQLite tiene FTS5 compilado
      • Si no: re-instala Python via uv

   6. INSTALL GIT
      • Si no existe: prompts apt/dnf/pacman según distro

   7. INSTALL NODE.JS v22
      • Resuelve latest 22.x desde nodejs.org/dist
      • Descarga tarball, extrae a ~/.hermes/node/
      • Crea symlinks en ~/.local/bin

   8. INSTALL RIPGREP + FFMPEG
      • ripgrep: cargo install si está, sino apt/dnf/pacman
      • ffmpeg: package manager

   9. NETWORK CHECK
      • Verifica pypi.org y duckduckgo.com con curl
      • Falla early si no hay conectividad

   10. CLONE REPO
       • git clone https://github.com/NousResearch/hermes-agent.git
       • Si ya existe: git pull con stash automático
       • Checkout main (o branch especificado)

   11. CREATE VENV + INSTALL
       • uv venv ~/.hermes/hermes-agent/.venv
       • uv pip install -e .
       • Instala dependencias core

   12. CREATE COMMAND SYMLINK
       • ln -s ... ~/.local/bin/hermes
       • Usuario puede ejecutar `hermes` desde cualquier lado

   13. RUN SETUP WIZARD
       • hermes setup interactivo
       • Pregunta provider LLM
       • Pregunta API keys
       • Genera ~/.hermes/config.yaml inicial
```

### 14.3 Por qué funciona — los 7 trucos

**Truco 1: uv en lugar de pip**
- uv es 10-100× más rápido que pip
- Puede instalar Python por sí mismo (no necesitas Python para instalar Python)
- Resuelve dependencias en paralelo

**Truco 2: Auto-detect OS y distros**
- No asume nada
- Cada distro tiene su comando (apt vs dnf vs pacman vs brew)
- Termux y WSL2 también soportados

**Truco 3: Bundled Node.js**
- No depende del Node del sistema
- Descarga su propia versión a `~/.hermes/node/`
- Evita conflictos con otros proyectos

**Truco 4: Sudo opcional**
- Por default, instala como user (no root)
- Solo pide sudo para apt/dnf/pacman si falta dependencia del sistema
- Lee de /dev/tty para passwords incluso en non-interactive

**Truco 5: Verificaciones explícitas**
- ensure_fts5() — verifica que SQLite tiene FTS5
- Network check — falla early si no hay internet
- Git check — verifica antes de clonar

**Truco 6: Graceful degradation**
- Si Playwright no se puede instalar → browser tools no disponibles pero Hermes corre
- Si ffmpeg no se puede instalar → voz no funciona pero el resto sí
- NO falla completamente por dependencias opcionales

**Truco 7: Self-healing en re-runs**
- Si ya está instalado, hace `git pull` con stash
- Si una dep falló, la re-intenta
- Idempotente — corres dos veces, sigue funcionando

### 14.4 Lo que For3s OS necesita copiar de esto

**Sí copiar:**
- ✓ One-line installer
- ✓ uv como base
- ✓ Auto-detect OS/distro
- ✓ Bundled deps (Node, Python si necesario)
- ✓ Graceful degradation
- ✓ Idempotencia
- ✓ ensure_fts5() o equivalente para deps críticas
- ✓ Network check early
- ✓ Wizard interactivo post-install

**Mejorar:**
- ⭐ Verificación criptográfica del installer (firmas)
- ⭐ Audit log del proceso de instalación
- ⭐ Versioning explícito (instalar versión X, no main)
- ⭐ Rollback automático si algo falla
- ⭐ Pre-flight check (¿el sistema tiene los requisitos?)
- ⭐ Telemetry opt-in para mejorar el installer

---

## 15. Lo que Hermes hace BIEN — qué heredar

Inventario táctico de lo que vale la pena copiar.

### 15.1 Patrones de diseño (heredar 100%)

| Patrón | Por qué es bueno |
|---|---|
| **One AIAgent class** | Una sola fuente de comportamiento, múltiples interfaces |
| **ProviderTransport abstraction** | Multi-LLM real desde día 1 (lección 5.7 del founder-thesis) |
| **Tool auto-registration** | Añadir tool = añadir archivo, sin listas que mantener |
| **Tier-based prompt + caching** | 90% menos costo en Tier 1+2 estables |
| **IterationBudget** | Hard cap previene loops infinitos costosos |
| **Profile isolation** | Multi-tenant trivial (1 user, N profiles) |
| **Pluggable memory providers** | Cambia backend de memoria sin tocar agente |
| **Plain markdown skills** | Auditable, portable, editable por humano |
| **6 execution backends** | Local + cloud + remoto + sandbox sin re-escribir |
| **Cross-platform messaging gateway** | Misma conversación en N plataformas |

### 15.2 Tecnología (heredar)

- ✓ **Python 3.11+** — versión moderna con typing decente
- ✓ **uv** en lugar de pip
- ✓ **SQLite + FTS5** para memoria episódica local-first
- ✓ **httpx** async para HTTP
- ✓ **Rich + prompt_toolkit** para TUI
- ✓ **Pydantic** para validación de tipos
- ✓ **Jinja2** para templates de prompts
- ✓ **Tenacity** para retries

### 15.3 Infraestructura (heredar concepto)

- ✓ One-line installer con auto-deps
- ✓ HERMES_HOME pattern (XDG-like)
- ✓ config.yaml + .env separation
- ✓ MIT license + open core
- ✓ Plugin ecosystem
- ✓ Entry points en pyproject (CLI commands)

### 15.4 Documentación (heredar)

- ✓ Docs site con installation explícita
- ✓ Architecture doc para developers
- ✓ Quickstart de 5 minutos
- ✓ DeepWiki-style code documentation
- ✓ Guías por plataforma

---

## 16. Lo que Hermes hace MAL — qué NO heredar

Aquí están los errores arquitectónicos. Cada uno es **oportunidad For3s**.

### 16.1 Errores de seguridad

| Error | Por qué importa | Cómo For3s lo resuelve |
|---|---|---|
| **No hay encryption at rest** del SQLite | El user controla el SQLite plain | E2E encryption desde día 1 (security-principles §5.6) |
| **API keys en .env plain** | Acceso filesystem = acceso a keys | Key Vault con OS keychain |
| **Tools ejecutan código sin sandbox por default** | local backend = subprocess en host | Default a Docker isolation |
| **No audit log estructurado** | Solo logs de aplicación | Audit log criptográfico (For3s §6.4) |
| **No workspace boundaries por encryption** | Profiles son aislamiento por path, no crypto | Per-workspace keys |
| **No RBAC** | Un user = todos los permisos | RBAC desde diseño (security-principles §5.4) |

### 16.2 Errores de arquitectura cognitiva

| Error | Por qué importa | Cómo For3s lo resuelve |
|---|---|---|
| **Loop secuencial** | No aprovecha paralelismo estructural | Grafo end-to-end (Grafo_vs_Loop §13) |
| **Sin pattern separation real** | FTS5 + texto = eventos similares colapsan | Pattern separation con metadata rica |
| **Sin metacognición** | "Confidence" no existe, siempre responde | PFC artificial explícito (For3s §3) |
| **Sin amígdala / valoración rápida** | Todo se trata igual | Triaje rápido para criticidad |
| **Sin DMN / procesamiento offline** | Solo procesa con input | Reflexión continua en background |
| **Sin microglía / olvido inteligente** | SQLite crece infinito | Poda activa de memoria |
| **Skills solo vía GO** | Aprende qué hacer, no qué evitar | Vía NO-GO explícita |
| **Sin neuromoduladores** | Siempre procesa igual | Modos globales (concentración, exploración) |

### 16.3 Errores de escalabilidad

| Error | Por qué importa | Cómo For3s lo resuelve |
|---|---|---|
| **SQLite es single-writer** | No escala más allá de 1 máquina | Sharding por workspace + DB distribuida |
| **Memoria toda en local** | No funciona con teams | Memoria centralizada cifrada |
| **Subagentes con ThreadPoolExecutor** | Limitado a 1 máquina | Distributed task queue (Redis/Kafka) |
| **Sin caching de tool results** | Misma operación se re-ejecuta | Cache con TTL por tool |
| **Sin métricas operacionales** | No sabes qué cuesta cada feature | Observability completa |

### 16.4 Errores de autonomía generativa

| Error | Por qué importa | Cómo For3s lo resuelve |
|---|---|---|
| **Skills se crean sin sandbox** | Skill mala = bug en producción inmediato | Sandbox + evaluación antes de promoción |
| **Sin evaluación de valor de skill** | No sabes si una skill ayuda o estorba | Métricas de impacto por skill |
| **Sin poda de skills inútiles** | Acumulación infinita | Microglía artificial sobre skills también |
| **Sin generación de nuevos sub-agentes** | Solo aprende skills, no estructuras | Meta-orchestrator que propone nodos |
| **Sin niveles de aprobación** | Lo que aprende lo usa, sin revisión | Tabla de niveles de autonomía (For3s §8.3) |

### 16.5 El gran error filosófico

**Hermes optimizó para "agente que crece contigo".** Eso es bonito para uso personal.

**For3s necesita optimizar para "agente que paga su factura enterprise".** Eso requiere:
- Trazabilidad criptográfica
- Audit total
- Workspace isolation por crypto
- Compliance-readiness
- Predictabilidad
- Multi-tenant real
- SLA garantizables

Hermes es **una herramienta personal con potencial enterprise**. For3s es **infraestructura enterprise con conveniencia personal**. La diferencia define todo.

---

## 17. El gap que For3s OS debe llenar

Resumen táctico. Esto es lo que For3s OS HACE que Hermes NO:

```
   ╔════════════════════════════════════════════════════════╗
   ║   FOR3S OS vs HERMES — GAP TÉCNICO                      ║
   ╠════════════════════════════════════════════════════════╣
   ║                                                        ║
   ║   1. ARQUITECTURA                                      ║
   ║      Hermes: loop con LLM central + tools             ║
   ║      For3s:  grafo multi-nodo con 11 sistemas         ║
   ║                                                        ║
   ║   2. SEGURIDAD                                         ║
   ║      Hermes: file isolation, no E2E crypto            ║
   ║      For3s:  E2E desde día 1 + audit cryptográfico   ║
   ║                                                        ║
   ║   3. MEMORIA                                           ║
   ║      Hermes: SQLite FTS5 + markdown                   ║
   ║      For3s:  Knowledge Graph + pattern separation     ║
   ║              + microglía + consolidación CLS          ║
   ║                                                        ║
   ║   4. SKILLS                                            ║
   ║      Hermes: vía GO genérica                          ║
   ║      For3s:  vía GO + NO-GO especializada QA          ║
   ║              + sandbox + evaluación                   ║
   ║                                                        ║
   ║   5. METACOGNICIÓN                                     ║
   ║      Hermes: NO existe                                ║
   ║      For3s:  PFC artificial con confidence checks    ║
   ║                                                        ║
   ║   6. PROCESAMIENTO OFFLINE                             ║
   ║      Hermes: NO existe                                ║
   ║      For3s:  DMN artificial activo                    ║
   ║                                                        ║
   ║   7. AUTONOMÍA GENERATIVA                              ║
   ║      Hermes: solo skills                              ║
   ║      For3s:  skills + sub-agentes + relaciones KG    ║
   ║              + modos globales (con aprobación)        ║
   ║                                                        ║
   ║   8. ESCALABILIDAD                                     ║
   ║      Hermes: single-user, single-machine              ║
   ║      For3s:  multi-tenant, distributed                ║
   ║                                                        ║
   ║   9. ESPECIALIZACIÓN                                   ║
   ║      Hermes: general purpose                          ║
   ║      For3s:  QA-first, vertical específico            ║
   ║                                                        ║
   ║   10. AUDITABILIDAD                                    ║
   ║       Hermes: logs de aplicación                      ║
   ║       For3s:  crypto chain + workspace audit         ║
   ║                                                        ║
   ╚════════════════════════════════════════════════════════╝
```

---

## 18. Plan de construcción inspirado en Hermes

Concreto, ejecutable, basado en lo que aprendimos.

### 18.1 Fase 0 — Setup (semana 1-2)

Heredar la base operativa de Hermes:

- [ ] Repo Python con pyproject.toml estilo Hermes
- [ ] Setup con uv (no pip)
- [ ] Estructura de directorios similar (`for3s_os/`, `tools/`, `agent/`, etc.)
- [ ] CI con ruff + ty + pytest
- [ ] One-line installer script (copiar estructura, no contenido)
- [ ] FOR3S_HOME pattern (similar a HERMES_HOME pero con encryption layer)

### 18.2 Fase 1 — Núcleo (semanas 3-8)

Construir las 3 piezas no-negociables del MVP cerebral:

**1. `For3sAgent` class (análogo a AIAgent pero con metacognición)**

```python
class For3sAgent:
    def run_conversation(self, message: str) -> Response:
        # 1. Workspace gate (auth + decrypt)
        ctx = workspace_gate.authorize(message)

        # 2. Triaje rápido (amígdala)
        priority = amygdala.assess(message, ctx)

        # 3. Routing (tálamo)
        subgraph = thalamus.route(message, priority)

        # 4. PFC orchestrator con metacognición
        plan = pfc.plan(message, ctx, subgraph)
        if plan.confidence < THRESHOLD:
            return ask_human(plan.uncertainties)

        # 5. Multi-agent paralelo (si subgraph lo requiere)
        results = multi_agent.execute(plan)

        # 6. Confidence check
        if results.confidence < THRESHOLD:
            return ask_human(results.uncertainties)

        # 7. Output con audit + sign
        return output_gate.sign(results, ctx)
```

**2. Knowledge Graph (Neo4j) con workspace boundaries**

```python
class WorkspaceKG:
    def __init__(self, workspace_id: str, encryption_key: bytes):
        self.driver = neo4j_driver(workspace_id)  # sharded
        self.crypto = WorkspaceCrypto(encryption_key)

    def add_entity(self, entity: Entity):
        encrypted = self.crypto.encrypt(entity)
        self.driver.run(...)

    def query(self, cypher: str, **params):
        # Audit: log this query
        audit.log("kg_query", workspace=self.workspace_id, query=cypher)
        return self.driver.run(cypher, **params)
```

**3. PFC con metacognición real**

```python
class PFCOrchestrator:
    def evaluate_confidence(self, plan, evidence) -> float:
        # LLM auxiliar evalúa: ¿qué tan seguro estoy?
        # Métricas: completitud de info, contradicciones,
        #           skills disponibles, casos similares
        return aux_llm.score(plan, evidence)

    def decide_next_action(self, state):
        confidence = self.evaluate_confidence(state.plan, state.evidence)
        if confidence < THRESHOLD_HIGH:
            return DecisionAction.ask_human(reason=state.uncertainties)
        if state.complexity > THRESHOLD_DEEP:
            return DecisionAction.tree_of_thoughts(state)
        return DecisionAction.execute(state.plan)
```

### 18.3 Fase 2 — Diferenciadores (meses 3-6)

- [ ] Microglía artificial (background job)
- [ ] Skills con vía GO + NO-GO
- [ ] Sandbox de skills nuevas
- [ ] Consolidación CLS automática
- [ ] Multi-agent grafo real con LangGraph o custom

### 18.4 Fase 3 — Escala y enterprise (meses 6-12)

- [ ] DMN artificial activo
- [ ] RBAC completo
- [ ] Audit cryptographic chain
- [ ] Per-workspace keys con vault
- [ ] Multi-tenant distributed
- [ ] Compliance-ready (SOC2 prep)

### 18.5 Heredar el patrón one-line installer

```bash
# for3s install script (target)
curl -fsSL https://for3s.ai/install.sh | bash

# Que haga:
# 1. Verificar firma del script (Hermes NO lo hace, For3s sí)
# 2. Pre-flight check del sistema
# 3. Instalar uv, Python 3.11+, Node, etc (igual que Hermes)
# 4. Instalar For3s OS desde repo verificado
# 5. Setup wizard con encryption keys per-workspace
# 6. Audit del proceso de instalación
# 7. Rollback si algo falla
```

---

## 19. Fuentes

### Documentación oficial Hermes

- [Hermes Agent — Página principal](https://hermes-agent.nousresearch.com/)
- [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/)
- [Architecture | Hermes Agent](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [Installation | Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Quickstart | Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
- [Using Hermes as a Python Library](https://hermes-agent.nousresearch.com/docs/guides/python-library)
- [Learning Path | Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/learning-path)

### Repositorio GitHub

- [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- [pyproject.toml](https://github.com/NousResearch/hermes-agent/blob/main/pyproject.toml)
- [scripts/install.sh](https://github.com/NousResearch/hermes-agent/blob/main/scripts/install.sh)
- [website/docs/getting-started/installation.md](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md)
- [AGENTS.md](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md)
- [CONTRIBUTING.md](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [setup-hermes.sh](https://github.com/NousResearch/hermes-agent/blob/main/setup-hermes.sh)
- [hermes-agent-self-evolution (repo separado)](https://github.com/NousResearch/hermes-agent-self-evolution)

### Análisis técnicos externos

- [DeepWiki: NousResearch/hermes-agent](https://deepwiki.com/NousResearch/hermes-agent)
- [hermes-agent en PyPI](https://pypi.org/project/hermes-agent/)
- [DataCamp: Nous Research Hermes Agent Setup & Tutorial](https://www.datacamp.com/tutorial/hermes-agent)
- [NxCode: Hermes Agent Complete Guide 2026](https://www.nxcode.io/resources/news/hermes-agent-complete-guide-self-improving-ai-2026)
- [CloudBlast: How to Install Hermes Agent on Linux/macOS/WSL2](https://cloudblast.io/article/How-to-Install-Hermes-Agent-on-Linux,-macOS,-and-WSL2:-Complete-Setup-Guide)
- [Tools4All: Hermes Agent Setup Guide](https://tools4all.ai/posts/hermes-agent-setup-guide)
- [heyuan110: Hermes Agent v0.9 Review](https://www.heyuan110.com/posts/ai/2026-04-14-hermes-agent-guide/)
- [Lushbinary: Hermes Agent Developer Guide](https://lushbinary.com/blog/hermes-agent-developer-guide-setup-skills-self-improving-ai/)
- [HundredTabs: Hermes Agent Setup Guide](https://hundredtabs.com/blog/hermes-agent-setup-guide)
- [Blake Crosley: Hermes Agent v0.15 Reference](https://blakecrosley.com/guides/hermes)
- [BrainCuber: Hermes Agent Setup Complete Tutorial](https://www.braincuber.com/tutorial/hermes-agent-setup-tutorial)
- [i-scoop.eu: Hermes Agent from Nous Research](https://www.i-scoop.eu/hermes-agent-from-nous-research/)
- [hermes-growth.dev: Hermes Agent in 2026](https://hermes-growth.dev/blog/hermes-agent-persistent-memory-practical-guide-2026)
- [mudrii/hermes-agent-docs](https://github.com/mudrii/hermes-agent-docs)

### Dependencias clave referenciadas

- [Honcho.dev](https://honcho.dev) — Dialectic user modeling
- [Astral uv](https://github.com/astral-sh/uv) — Python package manager
- [Model Context Protocol](https://modelcontextprotocol.io) — Standard tool protocol
- [Agent Client Protocol](https://github.com/zed-industries/agent-client-protocol) — IDE protocol
- [agentskills.io](https://agentskills.io) — Open skills standard

---

## Cierre

Brian, este reporte es **inteligencia técnica accionable**. Tienes en una página:

- **Cómo está construido Hermes** (stack, archivos, patrones)
- **Por qué es tan fácil de instalar** (los 7 trucos del installer)
- **Qué hace bien** (heredar)
- **Qué hace mal** (oportunidad For3s)
- **Cómo construir For3s OS usando esto como base**

**El takeaway estratégico:** Hermes es un excelente framework de agente personal/builder. Pero arquitectónicamente tiene **10 huecos críticos** (los de §16) que un agente enterprise necesita. Cada hueco es una ventaja For3s.

**No vas a competir con Hermes en su mismo juego.** Vas a construir **el juego siguiente** — donde Hermes no juega.

Lo que sí copias literal:
- One-line installer
- AIAgent class pattern
- Provider abstraction
- Tool auto-registration
- Profile isolation pattern
- Plugin ecosystem
- uv como base

Lo que reemplazas categóricamente:
- Loop → Grafo
- File isolation → E2E encryption per workspace
- Skills GO solo → Skills GO + NO-GO + sandbox
- Sin metacognición → PFC artificial
- Sin DMN → Procesamiento offline activo
- Sin microglía → Olvido inteligente
- General purpose → Especializado QA
- Single-tenant → Multi-tenant cryptographic

---

**Próximos pasos lógicos:**

1. **Hacer un clone real de Hermes localmente** y leer el código. Esto te da intuición directa sobre el código que el reporte solo describe.
2. **Generar `Mente/Cuerpo/01-arquitectura-general-for3s-qa.md`** que decida concretamente: ¿forkeamos Hermes o construimos paralelo? Hay argumentos para ambos.
3. **Generar `Mente/Cuerpo/02-installer-for3s.md`** con el script bash real que usaremos.
4. **Decidir el stack final** basado en este reporte (lock-in decisions).

---

**Fin del reporte.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Hermes_Arquitectura_Completa.md`).
