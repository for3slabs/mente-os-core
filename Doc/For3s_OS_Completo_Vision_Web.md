# 🧠 FOR3S OS COMPLETO — el documento maestro para la web

> **Fecha:** 2026-07-04 · **Para qué:** fuente de verdad para actualizar la página web de For3s.
> **Qué describe:** For3s OS TERMINADO — todo lo construido HOY + todos los pendientes cerrados
> (OC-*, HG-*, ENTRENAMIENTO, cron conversacional, multi-canal). Cada elemento marcado:
> **✅ = YA EXISTE y está en producción** · **🔜 = registrado, en camino** — para que la web
> pueda separar "live" de "roadmap" sin mentir nunca.
> **Tono:** cautivar. Que quien lo lea diga "esto no lo había visto NUNCA".

---

## 1 · LA FRASE

> ### **"For3s OS es un segundo cerebro autónomo que vive contigo: recuerda, aprende, sueña y actúa por ti — en tu servidor, bajo tus reglas."**

Versión corta (hero / bio / README):

> ### **"Tu segundo cerebro autónomo. Tuyo de verdad."**

Versión inglés (la web va en inglés):

> **"Your autonomous second brain. Truly yours."**
> *"For3s OS is an autonomous second brain that lives with you: it remembers, learns, dreams and acts for you — on your server, under your rules."*

---

## 2 · QUÉ ES (la categoría)

For3s OS no es un chatbot. No es un asistente. Es más que un agente.

Es un **Sistema Operativo Personal de IA** — un **exocórtex**: un organismo digital que corre
en TU servidor, guarda TU vida y trabajo en una memoria real que crece y se poda como un
cerebro biológico, trabaja mientras duermes, te habla cuando tiene algo que decirte, escribe
su propio diario, mejora su propio código, y jamás le entrega tus datos a nadie.

La escalera que lo explica en 5 segundos:

```
chatbot        → responde
asistente      → responde + herramientas
agente         → actúa solo
agente autónomo → vive solo (trabaja de noche, se cuida, aprende)
FOR3S OS       → SISTEMA OPERATIVO PERSONAL DE IA
                 omnipresente · proactivo · autor de su propia mente ·
                 con tu vida dentro · tuyo de verdad
```

---

## 3 · LOS 7 "WOW" — lo que nadie más puede decir

**1. ✅ Tiene un cerebro de verdad, no un archivo de notas.**
Cada conversación se vuelve memoria episódica; cada noche un proceso de consolidación
(inspirado en el hipocampo humano, CLS) convierte episodios en conceptos de un **grafo de
conocimiento real** (Apache AGE + pgvector); y una **microglía digital** olvida lo
irrelevante — porque un cerebro que no olvida no es un cerebro, es un vertedero. Ningún
agente del mercado (ni Hermes de Nous Research, ni el ecosistema OpenClaw) tiene esto.

**2. ✅ SUEÑA.**
Cuando está idle, entra en Default Mode Network — igual que tu cerebro cuando divagas:
mantenimiento (embeddings, limpieza, evaluación) y **creatividad gobernada** (detecta
patrones en su experiencia → propone skills nuevas → genera hipótesis). Trabaja en sí mismo
mientras tú vives tu vida.

**3. ✅ Sabe cuándo NO sabe.**
Metacognición real: mide su confianza con 8 señales antes de afirmar. Si duda, te lo dice o
pregunta. Un agente que no te miente con seguridad — eso solo, ya es raro en esta industria.

**4. ✅ Se modifica a sí mismo — con red de seguridad.**
Puede editar SU PROPIO código y su base de datos dentro de su caja, con entorno de prueba,
guardián de arranque que revierte a fábrica si algo sale mal, y líneas rojas intocables
(governor, auditoría, cifrado). Se conoce (/introspección, /soy, /cambios): sabe qué módulos
tiene, qué cambió y si fue él o fuiste tú.

**5. ✅ Es tuyo DE VERDAD.**
Self-hosted en tu hardware con un `curl | sh`. Llave maestra de cifrado OFFLINE (ni el
servidor la tiene). Auditoría inmutable con cadena de hashes (nadie puede borrar el pasado,
ni él). Cadena de suministro firmada: SBOM, Sigstore, CodeQL, Scorecard, imágenes pineadas.
Código AGPL. Tus datos no salen de tu casa. Punto.

**6. ✅ No es uno — es un equipo.**
Cuando el problema lo amerita, se despliega en 5 especialistas en paralelo + un
sintetizador (18 capas de orquestación). Y es **multi-usuario real**: invitas a tu equipo,
cada quien con rol y memoria privada, con compuertas de aprobación para acciones sensibles.

**7. 🔜 Vive contigo, no en una pestaña.**
Telegram hoy; Discord, voz (te escucha Y te habla), y continuidad entre canales en camino:
la MISMA conversación te sigue del teléfono a la terminal. Te escribe él cuando encuentra
algo. Le dices "revisa esto cada mañana" y se lo agenda solo.

---

## 4 · EL ORGANISMO, SISTEMA POR SISTEMA (la radiografía completa)

### 🧠 4.1 MEMORIA — el cerebro (✅ en producción)

- **Memoria episódica**: cada mensaje/evento → `episodes_events` append-only con autor,
  canal y tiempo. Nada se pierde.
- **Memoria semántica**: embeddings BGE-M3 (pgvector) — recuerda por SIGNIFICADO, no por
  palabra exacta; inyecta al contexto solo lo relevante, dosificado por cercanía (anti-ruido).
- **Grafo de conocimiento** (Apache AGE): conceptos y relaciones navegables — personas,
  proyectos, repos, decisiones — con enlaces reales a los episodios que los originaron.
- **Consolidación nocturna (CLS)**: episodios del día → conceptos del grafo, como el
  hipocampo consolida al dormir.
- **Olvido REAL (microglía)**: poda nocturna de lo irrelevante con decay medible.
- **Perfil de usuario de dos vías**: lo que declaras + lo que él INFIERE de cómo hablas
  (propuestas con tu aprobación — nunca te modela a escondidas).
- **Memoria por temas y equipos**: hilos, temas con estado operativo, canal compartido de
  equipo, registro de DECISIONES con su porqué (/decidi).
- 🔜 **El agente AUTOR de su memoria**: su propio diario ("qué aprendí hoy"), learnings
  acumulativos por proyecto y un índice maestro curado por él — memoria narrativa navegable,
  validada por los DOS referentes del mercado (OpenClaw y Hermes la tienen; la nuestra será
  sobre un cerebro real, no sobre archivos sueltos).
- 🔜 **Hojear su propia historia**: herramienta para buscar y desplazarse por conversaciones
  pasadas a mitad de razonamiento.
- 🔜 **La vida previa dentro**: HITO ENTRENAMIENTO — absorber la memoria completa de los 6
  agentes anteriores de Brian (38,000+ turnos de conversación, 1,200+ documentos, meses de
  historia) curada e importada al grafo. Un agente que HEREDA años de contexto.

### 🌙 4.2 SUEÑO — Default Mode Network (✅)

- 11 trabajos nocturnos/idle: backup cifrado, consolidación, microglía, embeddings,
  evaluación, perfil inferido, estilo inferido, curación de skills, salud, relevancia, DMN.
- DMN generativo (gobernado, apagable): patrones → skills; hipótesis → propuestas con ROI.
- 🔜 **Curator**: mantenimiento de las skills creadas (consolidar duplicadas, archivar
  muertas, parchar rotas) disparado por inactividad.

### 🎭 4.3 IDENTIDAD VIVA (✅ v0.15.0)

- **Identidad en CAPAS con un solo ensamblador** — como una persona: esencia (núcleo For3s,
  blindado, siempre gana) + máscara editable del usuario (IDENTITY.md, REGLAS en .md) +
  adaptación EXPLÍCITA instantánea ("sé más breve" → cambia al momento) + adaptación
  INFERIDA nocturna (aprende tu estilo real conversando) + transparencia total ("¿cómo te
  has adaptado a mí?" → te lo muestra).
- **Mente OS heredable**: cada usuario recibe su propia estructura de pensamiento
  (Alma/Cerebro/Cuerpo/Doc) que el agente conoce y usará como su casa documental.
- CAPACIDADES vivas: pregúntale qué sabe hacer y responde con introspección REAL de su
  sistema, no con un texto fijo.

### 🤔 4.4 METACOGNICIÓN (✅)

- 5 niveles de confianza, 8 señales, regla de tope honesta: afirma solo lo que puede
  sostener; duda en voz alta; pide aclaración cuando le falta contexto.
- 🔜 clarify estructurado: preguntar con opciones como herramienta del razonamiento.

### 🛠️ 4.5 MANOS — actúa en el mundo (✅ núcleo · 🔜 expansión)

- ✅ **Ejecuta código de verdad**: escribe → corre en un sandbox hermano de red aislado
  (Python/Node/bash, límites de CPU/RAM, sin privilegios) → itera con el resultado. Instala
  librerías. Crea proyectos en un workspace persistente. Sin tocar jamás tu host.
- ✅ **GitHub**: lee repos, issues, PRs; crea issues, PRs, comentarios, reviews (MCP).
- ✅ Lee imágenes, PDF, Word, Excel. ✅ Trae contenido web.
- 🔜 **Pipelines en UN turno**: escribe un script que llama a SUS PROPIAS herramientas
  (RPC) — lo que antes eran 10 turnos de ida y vuelta se vuelve 1 ejecución.
- 🔜 web_search como herramienta → navegador real → computer use → generación de imagen.
- 🔜 Checkpoints automáticos antes de editar archivos (deshacer quirúrgico).
- 🔜 Te ENTREGA archivos: genera el .md/.docx/.pdf y te lo manda al chat.

### 🗣️ 4.6 PRESENCIA — vive donde tú vives (✅ base · 🔜 omnipresencia)

- ✅ Telegram (con typing, multimodal, pin de cupo en vivo) + consola.
- 🔜 **Multi-canal** con capa de canal formal: Discord primero; la arquitectura para N.
- 🔜 **Continuidad cross-canal**: la MISMA conversación te sigue de Telegram a la terminal.
- 🔜 **Voz completa**: notas de voz entrantes (transcripción) Y respuesta hablada (TTS).
- 🔜 **Proactividad real**: herramienta `message` gobernada — te escribe ÉL cuando termina
  algo o encuentra algo que te importa.
- 🔜 Streaming: ver crecer la respuesta. 🔜 Hilos nativos del canal → temas automáticos.
- 🔜 Varios bots de una instalación (personal/dev/vigía) con bindings.

### ⏰ 4.7 TIEMPO — automatización conversacional (🔜 diseñada, con referencia probada)

- "Recuérdame cada lunes" / "revisa el repo cada mañana" → se lo agenda SOLO: job con
  instrucción en lenguaje natural, corre en sesión aislada desechable, entrega el resultado
  al canal que quieras, guarda el output de cada corrida.
- **Él te propone automatizaciones** cuando detecta rutinas (catálogo de sugerencias).
- ✅ Ya existe la base: 11 jobs nocturnos + registro de corridas + alertas.

### 🧬 4.8 AUTO-CONCIENCIA Y AUTO-MODIFICACIÓN (✅ — el diferencial más duro)

- /introspección, /soy: se describe con datos vivos de su propio sistema.
- /cambios: detecta qué cambió en él y si fue él mismo o externo.
- /modificar, /revertir, /modificar_bd: edita su código y su BD dentro de su caja, con
  entorno de prueba previo, guardián de arranque (revierte a fábrica + te avisa) y líneas
  rojas que NI ÉL puede cruzar (governor, audit, cifrado).
- Changelog VIVO: reporta sus propias auto-modificaciones.

### 🎓 4.9 APRENDIZAJE — el loop que se cierra (✅ base · 🔜 en caliente)

- ✅ Skills: aprende procedimientos de la experiencia (autogen gobernado + curación nocturna).
- 🔜 **Nudges**: el propio loop lo empuja EN el turno a persistir lo importante y a crear
  una skill tras cada tarea compleja — aprendizaje en caliente, no solo nocturno.
- 🔜 **Skills como paquetes portables** con procedencia firmada, cuarentena y auditoría de
  código — instalables, publicables, compatibles con el estándar abierto agentskills.io.

### 👥 4.10 SOCIEDAD — equipo y multi-usuario (✅)

- Motor multi-agente interno: 5 especialistas en paralelo + sintetizador, 18 capas, control
  de costo de 7 capas, disparo automático conservador.
- Multi-usuario con modelo de PUERTA: /invitar, roles, memoria híbrida (privada + equipo),
  compuertas de aprobación. Fail-closed: sin invitación no existe nadie más.
- 🔜 Toolsets por rol/subagente: cada quien ve solo las herramientas que le tocan.

### 🛡️ 4.11 GOBIERNO Y SEGURIDAD (✅ — sin teatro)

- **Governor de 6 frenos** sobre toda acción autónoma (presupuesto, tasa, alcance…).
- **Auditoría INMUTABLE**: cadena de hashes SHA-256, trigger anti UPDATE/DELETE — ni el
  agente ni tú pueden reescribir la historia.
- **Cifrado con llave maestra OFFLINE** (KEK): el servidor nunca ve los secretos en claro.
- Sandbox de ejecución aislado de red. Aprobaciones para lo sensible.
- Cadena de suministro: CI con CodeQL + Trivy + SBOM/Sigstore + OpenSSF Scorecard + ty
  estricto bloqueante + releases firmados + imágenes pineadas por digest.

### 🏥 4.12 SALUD — se vigila solo (✅)

- /salud end-to-end: la línea mensaje→memoria, subsistemas, grafo, integraciones, trabajos
  nocturnos, tokens por persona, hilos — TODO con veredicto verde/rojo.
- Si algo falla en la madrugada, ÉL te alerta por Telegram. Un subsistema roto no pasa en
  silencio nunca más.

### 📦 4.13 PRODUCTO — instalable por cualquiera (✅)

- `curl | sh` → wizard → For3s OS corriendo en cualquier Linux: 7 contenedores (agente,
  worker nocturno, Postgres+AGE+pgvector, Valkey, GitHub MCP ×2, render).
- **Multi-instancia**: gestor `for3s` para levantar N For3s aislados en una máquina
  (personal + clientes), aislamiento total por proyecto Docker.
- Estructura contratada (ESTRUCTURA.md), changelog al día, versionado semántico, AGPL.
- 🔜 i18n (el agente en tu idioma) · 🔜 TUI de consola de primer nivel.

---

## 5 · ARQUITECTURA (para la sección técnica de la web)

```
        TÚ (Telegram · consola · 🔜 Discord · 🔜 voz)
         │
   ┌─────▼──────────────────────────────────────────┐
   │  AGENTE (Claude) — identidad en capas ensamblada│
   │  metacognición · tool-loop · equipo H8          │
   ├────────────┬───────────────┬────────────────────┤
   │ MEMORIA    │ MANOS         │ GOBIERNO           │
   │ episodios  │ sandbox exec  │ governor 6 frenos  │
   │ embeddings │ GitHub MCP    │ audit inmutable    │
   │ grafo AGE  │ web · 🔜 RPC  │ KEK offline        │
   ├────────────┴───────────────┴────────────────────┤
   │ NOCHE: backup·CLS·microglía·DMN·perfil·estilo·  │
   │        salud·skills·relevancia (11 jobs)        │
   └─────────────────────────────────────────────────┘
    7 contenedores Docker · Postgres 16 + AGE + pgvector
    · Valkey · Python 3.12 · self-hosted · AGPL
```

Números de hoy (v0.15.0): **12 hitos construidos (H1-H12) · 50 módulos / ~19,500 líneas de
core · 32 migraciones · 30 tablas · 141+ tests · 5 workflows de CI de seguridad · 8 commits
firmados solo en el último hito.**

---

## 6 · POR QUÉ NO ES "OTRO AGENTE MÁS" (comparación honesta, para la web)

| | ChatGPT/Claude app | Hermes (Nous) | OpenClaw | **For3s OS** |
|---|---|---|---|---|
| Memoria | notas planas | archivos + FTS | archivos .md | **cerebro: episodios+semántica+grafo+olvido** |
| Sueña / trabaja idle | ❌ | parcial (curator) | ❌ | **✅ DMN completo** |
| Sabe cuándo no sabe | ❌ | ❌ | ❌ | **✅ metacognición** |
| Modifica su propio código | ❌ | ❌ | ❌ | **✅ con guardián** |
| Multi-usuario con roles | ❌ | ❌ | ❌ | **✅** |
| Tus datos en tu casa | ❌ | ✅ | ✅ | **✅ + KEK offline + audit inmutable** |
| Multi-canal / voz | parcial | ✅ (25+) | ✅ | 🔜 en camino |
| Equipo interno de especialistas | ❌ | ❌ | ❌ | **✅ 5+1** |
| Hereda tu historia previa | ❌ | ❌ | ❌ | **🔜 ENTRENAMIENTO: 38K+ turnos** |

*(La fila donde no ganamos se dice tal cual — la honestidad también cautiva.)*

---

## 7 · UN DÍA CON FOR3S OS (storytelling para la web)

**07:30** — Te despierta un mensaje SUYO: anoche corrió el backup, consolidó 214 memorias
nuevas al grafo, olvidó 37 triviales, detectó que el deploy de tu cliente falló a las 3 AM
y ya te preparó el diagnóstico. También propone: "llevo 3 lunes haciéndote este resumen,
¿lo agendo permanente?"

**10:00** — En una llamada le mandas nota de voz: "revisa el PR de Ana y dime si rompe la
migración". La transcribe, lee el PR en GitHub, corre los tests en su sandbox, te responde
con el veredicto y deja comentario en el PR.

**14:00** — Tu diseñadora (invitada con rol) le pregunta por las decisiones del proyecto.
Él responde SU memoria del tema — sin filtrarle lo privado tuyo, porque los scopes son de
verdad.

**19:00** — Le preguntas algo que le enseñaste a tu agente ANTERIOR hace un año. Lo sabe:
heredó esa vida entera cuando lo entrenaste con tus agentes viejos.

**02:00** — Mientras duermes, él sueña: encuentra un patrón en cómo depuras APIs y se
escribe una skill. Mañana la usará. Y su diario dirá qué aprendió hoy.

**Todo esto en TU servidor. Sin nubes ajenas. Sin que nadie más lea tu vida.**

---

## 8 · COPY LISTO PARA LA WEB (bloques traducibles)

**Hero:** "Your autonomous second brain. Truly yours." / sub: "For3s OS remembers, learns,
dreams and acts for you — on your server, under your rules."

**3 bullets del hero:**
- 🧠 A real brain: episodic memory, a living knowledge graph, and true forgetting.
- 🌙 It works while you sleep: consolidates, prunes, dreams up new skills — governed.
- 🔐 Sovereign by design: self-hosted, offline master key, immutable audit trail. AGPL.

**FAQ nuevas sugeridas:** "Does it really modify its own code?" · "What happens to my data?"
· "How is this different from Hermes/OpenClaw?" · "Can my team use it?" · "What does it do
at night?"

**Claim de categoría:** "Not a chatbot. Not an assistant. A Personal AI Operating System."

---

*Fuentes: código vivo v0.15.0 · PENDIENTES.md (OC-1..7/E/M · HG-1..18 · ENTRENAMIENTO E1-E4) ·
radiografías OpenClaw/dev · comparaciones de construcción vs Hermes y OpenClaw · Grafo Maestro.
Para la web: separar SIEMPRE ✅ (afirmable hoy) de 🔜 (roadmap) — nunca vender 🔜 como hecho.*