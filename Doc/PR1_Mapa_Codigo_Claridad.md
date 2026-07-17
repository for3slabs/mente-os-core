# PR1 · Mapa de Claridad del Código — For3s OS

> **Qué es:** el documento de REFERENCIA de qué es qué en For3s OS. Responde: qué módulos
> están vivos, cuáles son entry points, cuáles tienen capacidades sin cablear, qué está muerto.
> Por cada módulo: qué hace · de quién depende · quién lo usa · estado. Verificado contra el
> código real (2026-06-29, POST sesión de bugs — refleja todo lo arreglado).
>
> Complementa: PR4-B (flujo memoria/usuario) + PR4-C (auditoría inicial). Esto es el mapa
> CONSOLIDADO y ACTUAL. Base para PR7 (revisar cada H) y PR8 (entrenamiento).

## 0. Estado del producto (de un vistazo)

- **47 módulos** Python en `packages/for3s-core/src/for3s_core/`
- **7 contenedores** (docker-compose): agent · worker · postgres · valkey · github-mcp · github-mcp-write · render
- **23 migraciones** de BD (001 → 023)
- **version.py:** v0.12.0 / "H10 PLANEA" ⚠️ DESACTUALIZADO (no refleja PR2/PR10/bugs de jun-29 → tarea: actualizar)

## 1. CAPAS del código (los de abajo no dependen de los de arriba)

```
ENTRADA (entry points, nadie los importa — se EJECUTAN):
  telegram_channel (3090 L, usa 29) · cli (126 L) · tasks (476 L, worker) · dmn_tasks (456 L)

ORQUESTACIÓN:
  conversation (1285 L, usa 16) · multiagente (405) · subbloques (658) · dmn (404) · health (399)

DOMINIO (memoria, equipo, skills, tools, soporte):
  memory · kg · consolidator · microglia · relevance · equipo · temas · perfil · hilo_status
  skills · governor · aprende · tool_loop · mcp_client · specialists · cost_control · handoff
  confidence · modelos

BASE (infra, casi nadie depende de ellos):
  agent · llm (usado por 12!) · db · config (usado por 9) · audit (usado por 7) · crypto
  secret_store · embeddings · cache · concurrency · backup · sandbox

UTILIDADES (puras):
  md_html · text_normalize · tiempo · web_fetch · gh_ficha · multimodal · version
```

## 2. Los 47 módulos — tabla completa (qué hace · usa · usado_por · estado)

> Estado: 🟢 vivo · 🟢▶ entry point · 🟠 capacidad parcial/sin cablear · 🔴 muerto

| Módulo (L) | Qué hace | usado_por | estado |
|---|---|---|---|
| **telegram_channel** (3090) | EL ORQUESTADOR / puerta de Telegram. 20 comandos. | — (entry) | 🟢▶ el mayor; candidato a dividir (PR9) |
| **cli** (126) | Terminal con memoria | — (entry) | 🟢▶ |
| **tasks** (476) | Worker: 8 jobs nocturnos + cron_corridas (PR2.2a) + health_check (PR2.2b) | — (entry) | 🟢▶ |
| **dmn_tasks** (456) | Las 8 tasks del DMN | — (entry DMN) | 🟢▶ |
| **conversation** (1285) | Motor de conversación: arma contexto (todas las memorias) | 4 | 🟢 2º más acoplado |
| **memory** (658) | Memoria episódica + semántica (record/load/buscar) | 7 | 🟢 núcleo |
| **subbloques** (658) | Análisis de repos grandes por uso | 2 | 🟢 |
| **equipo** (482) | Multi-usuario (H8): roles, puerta | 1 | 🟢 |
| **consolidator** (475) | CLS: consolida episodios→grafo (de noche) | 2 | 🟢 (BUG-8 arreglado) |
| **multiagente** (405) | Red multi-agente (H8) | 1 | 🟢 |
| **dmn** (404) | DMN "SUEÑA" (H9) | 2 | 🟢 |
| **health** (399) | ⭐ NUEVO (PR2): monitoreo end-to-end /salud | 2 | 🟢 |
| **governor** (427) | GOVERNOR (H11): freno de skills | 3 | 🟢 |
| **llm** (375) | Capa LLM (Claude OAuth) | **12** | 🟢 el más reutilizado — núcleo crítico |
| **tool_loop** (371) | Loop tool-use GitHub | 2 | 🟢 (BUG-9 hermano red) |
| **aprende** (367) | MOTOR /aprende (H12) | 3 | 🟢 |
| **specialists** (297) | Catálogo de specialists | 1 | 🟢 |
| **confidence** (276) | Metacognición (H10-PLANEA) | 1 | 🟢 |
| **agent** (244) | Arma prompt + llama LLM | 3 | 🟢 |
| **web_fetch** (238) | Fetch web (httpx + render hermano) | 1 | 🟢 (BUG-9b hermano red) |
| **microglia** (216) | Olvido inteligente (H6) | 1 | 🟢 (depende de relevance, BUG-1) |
| **kg** (210) | Knowledge Graph (AGE) | 4 | 🟢 (BUG-8 catálogo arreglado) |
| **multimodal** (211) | Lee adjuntos (img/PDF/Word/Excel) | 1 | 🟢 |
| **concurrency** (208) | Anti-429 (token bucket) | 1 (llm) | 🟢 |
| **perfil** (178) | Perfil de usuario (P1) | 2 | 🟢 |
| **skills** (178) | Skills (H10) | 4 | 🟢 |
| **mcp_client** (178) | Cliente MCP (HTTP a hermanos) | 4 | 🟢 (BUG-9: stdio→HTTP) |
| **version** (162) | version-self-awareness | 2 | 🟠 desactualizado (v0.12.0) |
| **hilo_status** (145) | STATUS por hilo (AI4) | 2 | 🟢 |
| **gh_ficha** (144) | Ficha de repo GitHub | 1 | 🟢 |
| **temas** (143) | Temas/hilos por persona (AI2) | 1 | 🟢 |
| **backup** (142) | Backup BD (H6) | 1 | 🟢 (BUG-5/6 arreglado) |
| **cost_control** (124) | 7 capas freno equipo (H8) | 1 | 🟢 |
| **modelos** (113) | Registro modelos LLM (/model) | 1 | 🟢 |
| **relevance** (116) | Cálculo decay para microglía | 1 (tasks) | 🟢 (BUG-1: ya conectado al cron) |
| **cache** (109) | Cache Valkey lecturas GitHub | 3 | 🟢 |
| **audit** (105) | Audit chain inmutable | 7 | 🟢 |
| **sandbox** (105) | Lint de PR en contenedor | **0** | 🔴 MUERTO (BUG-2, diferido a hermano futuro) |
| **md_html** (103) | Markdown→HTML Telegram | 1 | 🟢 |
| **handoff** (100) | Audit trail equipo (AI3) | 1 | 🟢 |
| **config** (79) | Lee secrets/env | **9** | 🟢 |
| **db** (76) | Conexión Postgres | 3 | 🟢 |
| **crypto** (69) | KEK (cifrado secretos) | 1 | 🟢 |
| **secret_store** (67) | Almacén secretos cifrados | 2 | 🟢 |
| **embeddings** (66) | BGE-M3 texto→vector | 2 | 🟢 (BUG-10: HF offline) |
| **text_normalize** (65) | Normaliza texto | 2 | 🟢 |
| **tiempo** (85) | Hora local del usuario | 2 | 🟢 |

## 3. Capacidades CONSTRUIDAS pero SIN CABLEAR (🟠 — el código existe, no se usa)

> Estas son funciones huérfanas — útiles, pero nunca enchufadas. PR1 las visibiliza para
> decidir si cablearlas (varias son CLAVE para el rediseño de memoria MEM-1/MEM-3).

- 🧠 **`kg.episodios_de_concepto` / `recursos_de_repo` / `repos_de_owner`** — navegación del grafo
  (concepto→episodios, repo→recursos, owner→repos). Existen pero la recuperación de contexto NO las
  usa → el grafo se puede navegar pero no se navega. Clave para MEM-3 (memoria en cascada).
- 🧠 **`memory.get_last_repo` / `set_last_repo`** — recordar el último repo visto. Sin cablear.
- **`equipo.requiere_aprobacion`** — lógica de permisos sin usar.
- **`sandbox.lint_archivos`** — 🔴 código muerto (BUG-2, diferido).

## 4. MIGRACIONES de BD (el esquema, 23) — qué añadió cada una

```
001 inicial · 002 secrets · 003 channel_por_turno · 004 github_resources · 005 gh_kind_list
006 consulted · 007 embeddings · 008 memory_governance · 009 veces_recuperado · 010 multiusuario
011 memoria_scope · 012 solicitudes · 013 hilo_por_usuario · 014 temas · 015 corridas_equipo
016 hilo_status · 017 expulsion · 018 perfil_usuario · 019 skills · 020 governor · 021 dmn
022 dmn_propuestas · 023 cron_corridas (⭐ PR2.2a, la última)
```

## 5. INFRAESTRUCTURA — los 7 contenedores

| Servicio | Imagen | Rol | Notas |
|---|---|---|---|
| postgres | for3s-postgres:local | toda la memoria | AGE+pgvector+pgcrypto horneados |
| valkey | valkey:8 | cache + cola jobs | |
| agent | for3s-agent:local | EL BOT | modelo BGE-M3 horneado (caché local, offline) |
| worker | for3s-agent:local | jobs nocturnos | misma imagen, cmd distinto |
| github-mcp | github-mcp-server | GitHub read | ⭐ hermano de red (BUG-9) |
| github-mcp-write | github-mcp-server | GitHub write | ⭐ hermano de red (BUG-9) |
| render | for3s-render:local | web/JS (Chromium) | ⭐ hermano de red (BUG-9b) |

## 6. BUGS cerrados esta sesión (29-jun) — afectaron estos módulos

| Bug | Módulo(s) | Qué era |
|---|---|---|
| BUG-1 | relevance, tasks, microglia | decay no se ejecutaba (no estaba en el cron) |
| BUG-5/6 | backup, Dockerfile, compose | backup roto (sin pg_dump / sin volumen) |
| BUG-8 | kg, consolidator | CLS no escribía al grafo (catálogo AGE corrupto) |
| BUG-9/9b | mcp_client, web_fetch, compose | GitHub/render rotos → hermanos de red |
| BUG-10 | embeddings, Dockerfile | modelo no precargaba (snapshot/HF/caché) |
| BUG-12 | telegram_channel | /estado visible pero bloqueado |
| BUG-13 | telegram_channel | /diagnostico fuga de privacidad |

## 7. Hallazgos / deuda de claridad (para atender)

1. ⚠️ **version.py desactualizado** (v0.12.0 / H10 PLANEA) — no refleja PR2/PR10/bugs. Tarea: subir versión + changelog.
2. ⚠️ **telegram_channel.py = 3090 líneas, usa 29 módulos** — el cuello de complejidad. Candidato #1 a dividir (PR9 UX / refactor).
3. 🟠 **Capacidades de grafo sin cablear** (sección 3) — clave para el rediseño de memoria.
4. 🔴 **sandbox.py muerto** — decidir borrar o re-cablear como hermano (BUG-2).
5. **llm.py lo usan 12 módulos** — núcleo crítico, cualquier cambio ahí afecta todo. Tratar con cuidado.

---

> **Conclusión:** el código está SANO en general (capas bien ordenadas, casi todo conectado). La
> sesión de bugs mejoró la salud (relevance ya conectado, hermanos de red, etc.). La deuda real es:
> version.py al día, dividir telegram_channel, cablear las capacidades de grafo, decidir sandbox.
> Este doc es la base para PR7 (revisar cada H) y PR8 (entrenamiento).
