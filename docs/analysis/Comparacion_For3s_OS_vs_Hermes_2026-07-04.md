# ⚔️ For3s OS vs Hermes — Comparación a profundidad (2026-07-04)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Comparacion_For3s_OS_vs_Hermes_2026-07-04.md → docs/analysis/Comparacion_For3s_OS_vs_Hermes_2026-07-04.md (2026-07-30, ADR-029)

## Purpose

⚔️ For3s OS vs Hermes — Comparación a profundidad (2026-07-04)


> Comparación DETALLADA y actualizada: comportamiento, experiencia de usuario, cada capacidad.
> **For3s OS v0.15.0 "Identidad Viva"** (propio) vs **NousResearch/hermes-agent** (referencia, MIT).
> Fuente Hermes: repo oficial (fetch 2026-07-04). Fuente For3s: código real en producción.
> Notación interna de Mente OS (aquí se nombra la referencia; el código de For3s NO cita fuentes externas).

---

## 0. EN UNA FRASE
Ambos son **agentes reales** (no chatbots): autónomos, persistentes, ejecutan acciones, se mejoran.
- **Hermes** = agente **ANCHO**: muchos canales, muchos backends de ejecución, muchas integraciones. Un
  "cuchillo suizo" de agente personal, MIT, corre hasta en un VPS de $5.
- **For3s** = agente **PROFUNDO**: menos superficie, pero va MÁS HONDO en memoria (grafo + cascada),
  identidad (capas auto-adaptables), auto-modificación (edita su propio código) y confianza (auditoría
  inmutable + CI de nivel enterprise). Un "segundo cerebro" con corazón en QA.

**Metáfora:** Hermes es más **versátil** (hace de todo en todos lados); For3s es más **profundo y
confiable** (hace menos cosas pero con memoria/identidad/seguridad de otro nivel).

---

## 1. MEMORIA — cómo recuerda

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Episódica | FTS5 (búsqueda full-text) + resumen por LLM para recall entre sesiones | ✅ episodes_events + línea de tiempo + hilo_status (retomar) |
| Semántica | Perfiles de usuario (Honcho, "dialectic user modeling") | ✅ **embeddings BGE-M3 + pgvector (búsqueda por SIGNIFICADO real, 1024d)** |
| Grafo de conocimiento | ❌ NO (evita vector DBs, usa historiales buscables) | ✅ **Apache AGE — grafo de conceptos/repos/owners/episodios** |
| Consolidación | "nudges" periódicos | ✅ **CLS nocturno: episodios→conceptos + Microglía que olvida el ruido** |
| Cascada / ensamblaje | capas separadas | ✅ **1 punto de ensamblaje (memoria.recordar) en cascada** |

**Veredicto memoria:** For3s va MÁS PROFUNDO. Hermes recuerda buscando en el historial (FTS5) + modela
al usuario; For3s hace eso Y ADEMÁS tiene grafo de conocimiento navegable + búsqueda semántica vectorial +
un ciclo de olvido/consolidación biológico (CLS + microglía). Hermes es más simple (sin vector DB a
propósito); For3s es más "cerebro real".

---

## 2. IDENTIDAD / PERSONALIDAD — quién es y cómo se adapta

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Definición | `SOUL.md` (heredado de OpenClaw) | ✅ **identidad EN CAPAS** (SOUL+ética+operativa base blindada + IDENTITY editable) |
| Cambiar persona | `/personality [name]` (runtime, sin reinicio) | ✅ **archivo `/app/persona/IDENTITY.md` editable EN CALIENTE** (sin reinicio, sin comando) |
| Se adapta al usuario | user modeling refina "quién eres" entre sesiones | ✅ **auto-adaptación: explícita ("sé más breve"→al instante) + INFERIDA de noche** |
| Núcleo protegido | (no explícito) | ✅ **núcleo BLINDADO: líneas rojas que la capa usuario NUNCA anula** |
| Transparencia | (no explícito) | ✅ **"¿cómo te has adaptado a mí?" → te cuenta qué aprendió** |

**Veredicto identidad:** For3s va MÁS PROFUNDO (v0.15). Ambos tienen persona editable por .md (Hermes
`/personality`, For3s IDENTITY.md), PERO For3s la organiza en CAPAS con núcleo blindado + se auto-modifica
la personalidad solo (Hermes modela al usuario, pero no reescribe su propia máscara observándote) +
transparencia. For3s es el único que "aprende tu estilo y se acopla sin que se lo pidas, y te lo cuenta".

---

## 3. TOOLS Y ACCIONES — qué puede hacer

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Ejecutar código | **6 backends**: local, Docker, SSH, Singularity, Modal, Daytona | ⚠️ **1 backend: sandbox Docker aislado** (local/SSH diferidos, EC-EXTRA-1) |
| Web | Firecrawl + cloud browser + generación de imágenes (FAL) | ✅ web_fetch (render Playwright headless). Sin gen de imágenes |
| MCP | ✅ "conecta cualquier MCP server" | ✅ MCP (GitHub read/write). Menos amplio |
| GitHub | (vía tools genéricas) | ✅ **nativo: analiza repos 2 niveles, cuenta exacto PRs/issues, escribe con confirmación** |
| Multimodal | voz (STT/TTS) | ✅ **imágenes/PDF/Word/Excel**. Sin voz |
| Skills | `~/.hermes/skills/`, `/skill-name` shortcuts | ✅ skills + governor que las escanea + auto-curación nocturna |

**Veredicto tools:** Hermes va MÁS ANCHO. Tiene 40+ tools, 6 backends de ejecución (incl. cloud
serverless: Modal/Daytona), generación de imágenes, voz. For3s tiene menos superficie (1 sandbox, sin
voz/imágenes) pero MÁS profundo en lo suyo (GitHub nativo con conteos exactos, multimodal documentos,
governor sobre skills). Aquí Hermes claramente gana en amplitud.

---

## 4. EXPERIENCIA DE USUARIO — cómo lo usas

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Canales | **CLI TUI + Telegram + Discord + Slack + WhatsApp + Signal + Email** (gateway unificado) | ⚠️ **Telegram + consola** (multi-canal = hito futuro) |
| Continuidad entre canales | ✅ misma conversación en cualquier canal | (1 canal, no aplica aún) |
| Comandos | `/new /retry /model /skills /compress /usage` | `/soy /introspeccion /cambios /modificar /aprende /skills /tema /perfil /salud /model /dmn /invitar...` |
| Interrumpir tarea | ✅ mandar mensaje a mitad → redirige | (responde secuencial) |
| Multi-usuario | DM pairing | ✅ **multi-usuario con ROLES + puerta (/invitar) + memoria híbrida (privada + común)** |

**Veredicto UX:** Hermes va MÁS ANCHO en canales (6 plataformas + email, gateway unificado, continuidad
cross-canal, interrupción). For3s va más profundo en multi-USUARIO (roles/puerta/memoria híbrida — varias
personas comparten un For3s con aislamiento). Para "un agente personal en todos mis chats" Hermes gana;
para "un agente de equipo compartido con memoria por persona" For3s gana.

---

## 5. AUTONOMÍA — trabaja solo, se mejora

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Tareas programadas | cron con lenguaje natural ("reporte diario", "backup nocturno") + entrega a cualquier canal | ✅ **11 jobs nocturnos** (backup/CLS/olvido/perfil/estilo/DMN/health). ⚠️ cron CONVERSACIONAL = futuro |
| Auto-creación de skills | ✅ tras tareas complejas; se auto-mejoran con el uso | ✅ igual (H12 APRENDE) + **gobernado por governor** |
| Se mejora | closed-loop learning | ✅ **DMN ("sueña"): housekeeping + generativas gobernadas + ROI medible** |
| Trabaja sin el usuario | ✅ en cloud, desatendido | ✅ **de noche: se mantiene (memoria) + se mejora + ajusta su identidad** |

**Veredicto autonomía:** Empate técnico, con matices. Ambos: cron + auto-skills + trabajo desatendido.
Hermes: el cron acepta lenguaje natural y entrega a cualquier canal (más flexible para el usuario). For3s:
el trabajo nocturno es más RICO (alimenta memoria + identidad + salud, con gobierno y ROI), pero el cron
aún no es conversacional ("recuérdame cada lunes" = futuro). Hermes más flexible de expresar; For3s más
profundo en qué hace de noche.

---

## 6. MULTI-AGENTE / EQUIPO

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Sub-agentes paralelos | ✅ "spawn isolated subagents for parallel workstreams" | ✅ **5 specialists en paralelo + Synthesizer** (H8) |
| Orquestación | scripts Python que llaman tools por RPC | ✅ multiagente.py: 2 familias (técnica/general), disparo automático conservador |
| Coordinación | padre orquesta + agrega resultados | ✅ igual (padre sintetiza) |

**Veredicto equipo:** Empate. Ambos lanzan sub-agentes aislados en paralelo y sintetizan. Hermes vía
scripts RPC (más programable); For3s con 2 familias de specialists y disparo automático (más "listo para
usar"). Diferencia de estilo, no de fondo.

---

## 7. AUTO-MODIFICACIÓN — ⭐ donde For3s es ÚNICO

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Editar su propio código | ❌ NO | ✅ **/modificar: edita su código, lo prueba en aislado ANTES, reversible** |
| Editar su propia BD | ❌ NO | ✅ **/modificar_bd (backup + dry-run)** |
| Se conoce en vivo | (context files) | ✅ **/soy /introspeccion: consulta su infra REAL (módulos/tablas/jobs)** |
| Detecta cambios | ❌ | ✅ **/cambios: distingue "yo lo cambié" vs "me lo cambiaron"** |
| Guardián de rescate | ❌ | ✅ **si una auto-mod rompe el arranque, un guardián revierte a fábrica solo** |

**Veredicto:** For3s GANA claramente. Esta capacidad Hermes NO la tiene. For3s se conoce, detecta qué
cambió, y edita su PROPIO código/BD dentro de su caja (con doble red: prueba en aislado + guardián de
arranque). Es de las cosas que hacen a For3s "más agente" en el eje self-improving.

---

## 8. SEGURIDAD / CONFIANZA / SELF-HOSTING

| Aspecto | Hermes | For3s OS |
|---|---|---|
| Self-hosting | ✅ "corre en un VPS de $5", sin cloud obligatorio | ✅ self-hosted, `curl\|sh`, 9 contenedores (más pesado: BGE-M3, AGE) |
| Sandbox | Docker/Singularity | ✅ sandbox hermano non-root, aislado, sin red al host |
| Aprobación de acciones | ✅ command approval | ✅ **write de GitHub SIEMPRE con confirmación (botón); gate de aprobación en equipo** |
| Secretos | allowlist | ✅ **KEK OFFLINE (Brian nunca ve plaintext); secretos cifrados** |
| Auditoría | (no explícito) | ✅ **auditoría INMUTABLE (hash-chain, no UPDATE/DELETE)** |
| Supply chain / CI | MIT, sin CI de confianza documentado | ✅ **CI de confianza: SBOM + Sigstore + Scorecard + CodeQL + Trivy + commits firmados GPG** |
| Multi-instancia | (1 agente) | ✅ **varias instancias AISLADAS en la misma máquina (personal + clientes)** |

**Veredicto seguridad:** For3s GANA. Ambos self-hosted con sandbox y aprobación, pero For3s va mucho más
lejos en confianza VERIFICABLE: auditoría inmutable, KEK offline, CI con SBOM/firmas/Scorecard, multi-
instancia aislada. Es "confianza de nivel enterprise", el wedge del producto. Hermes es más ligero
(MIT, VPS de $5) pero no ofrece esa capa de auditabilidad/supply-chain.

---

## 9. CÓMO "LE DAS UN TRABAJO" (el eje de la charla)

| | Hermes | For3s OS |
|---|---|---|
| Lenguaje natural | ✅ escribes la tarea, elige tools | ✅ igual |
| Tarea programada | ✅ cron conversacional ("reporte diario") | ⚠️ jobs fijos (cron conversacional = futuro) |
| Contexto persistente | Context Files que moldean cada conversación | ✅ **Mente OS del usuario (Alma/Cerebro/Cuerpo/Doc) + perfil + temas/estado/decisiones** |
| Skills reutilizables | `/skill-name` | ✅ skills + /aprende (destila de lo trabajado) |
| Interrumpir/redirigir | ✅ mensaje a mitad | (secuencial) |

**Para "dale un trabajo a tu agente":** Hermes es más flexible para EXPRESAR el trabajo (cron natural,
interrumpir). For3s es más profundo en el CONTEXTO del trabajo (Mente OS estructurada + estado por tema +
decisiones con porqué). Hermes: "dile qué hacer, cuándo, en cualquier canal". For3s: "el agente ENTIENDE
tu proyecto a fondo (su cerebro documental) y recuerda por qué se decidió cada cosa".

---

## 10. TABLA RESUMEN — quién gana en qué

| Eje | Ganador | Por qué |
|---|---|---|
| Memoria | 🟢 **For3s** | grafo + semántica vectorial + CLS/olvido (Hermes: FTS5, sin grafo) |
| Identidad | 🟢 **For3s** | capas + auto-adapta + núcleo blindado + transparencia |
| Tools (amplitud) | 🔵 **Hermes** | 6 backends, cloud serverless, voz, imágenes, 40+ tools |
| Canales / UX | 🔵 **Hermes** | 6 plataformas + email + continuidad cross-canal + interrupción |
| Multi-usuario | 🟢 **For3s** | roles + puerta + memoria híbrida |
| Autonomía | 🟰 empate | ambos cron+skills; Hermes cron natural, For3s nocturno más rico |
| Multi-agente | 🟰 empate | ambos sub-agentes paralelos + síntesis |
| Auto-modificación | 🟢 **For3s** | edita su código/BD; Hermes NO |
| Seguridad/confianza | 🟢 **For3s** | audit inmutable + KEK + CI SBOM/firmas + multi-instancia |
| Ligereza / despliegue | 🔵 **Hermes** | MIT, VPS $5 (For3s: 9 contenedores, más pesado) |

---

## 11. CONCLUSIÓN

**No hay un "mejor" absoluto — son filosofías distintas:**
- **Hermes = amplitud.** El agente personal que quieres si valoras estar en TODOS tus canales, ejecutar
  en cualquier backend (incl. cloud), voz/imágenes, y correr ligero en un VPS. MIT, muy hackeable.
- **For3s = profundidad + confianza.** El agente que quieres si valoras un CEREBRO real (grafo + memoria
  semántica + olvido biológico), una IDENTIDAD que se adapta a ti y se blinda, que se AUTO-MODIFICA, y
  seguridad/auditabilidad de nivel enterprise (KEK offline, audit inmutable, CI firmado). Segundo cerebro
  con corazón en QA.

**Dónde For3s VA MÁS ALLÁ de Hermes (lo que Hermes NO tiene):**
1. Grafo de conocimiento navegable (AGE) + olvido biológico (CLS/microglía).
2. Identidad en capas auto-adaptable con núcleo blindado + transparencia.
3. **Auto-modificación de su propio código/BD** (con doble red de seguridad).
4. Multi-instancia aislada en la misma máquina.
5. Confianza verificable: auditoría inmutable + KEK offline + CI (SBOM/Sigstore/Scorecard).

**Las 2 brechas de For3s vs Hermes (NO son agencia, son forma):**
1. **Multi-canal** — Hermes está en 6 plataformas + email; For3s en Telegram + consola.
2. **Backends de ejecución** — Hermes tiene 6 (incl. cloud); For3s tiene 1 sandbox.
(+ menor: cron conversacional, voz/imágenes, interrumpir tarea — todo en §EXTRAS/FUTURO de For3s.)

Relacionado: [[For3s_Bot_vs_Agente_vs_Hermes]] · [[project_paridad_hermes_completa]] ·
[[project_hito_identidad_viva]] · `work/Hermes_Arquitectura_Completa.md` · `reference_hermes_es_nous`.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `docs/analysis/Comparacion_For3s_OS_vs_Hermes_2026-07-04.md`).
