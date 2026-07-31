# 🎭🧠 RONDA — Reconstrucción de FOR3S_ROLE en CAPAS (identidad viva y auto-adaptable)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_Reconstruccion_FOR3S_ROLE.md → work/Ronda_Reconstruccion_FOR3S_ROLE.md (2026-07-30, ADR-029)

## Purpose

🎭🧠 RONDA — Reconstrucción de FOR3S_ROLE en CAPAS (identidad viva y auto-adaptable)


> **Hito grande (Brian, 2026-07-04).** Diseño a profundidad ANTES de codear (regla LOCKED:
> explicar → aprobar → construir). Esta Ronda es el CONTRATO del hito. Vive en Mente OS
> (poético: el hito que hace de Mente OS una capa nativa, diseñado dentro de Mente OS).

---

## 0. LA VISIÓN (en las palabras de Brian)

Hoy FOR3S_ROLE es **un solo string de ~200 líneas** en `agent.py` que mezcla TODO: esencia +
personalidad + capacidades + reglas. Funciona, pero:
1. La personalidad que pusimos se trata como "la verdad", cuando debería ser solo un **default**.
2. Para cambiar el tono hay que editar código y rebuildear.
3. No refleja lo que For3s YA es: **un agente que aprende, se adapta y se auto-modifica.**

**La idea (Brian):** como un humano — una **esencia de base** + **máscaras que se adaptan al lugar**.
Pero con dos correcciones críticas que Brian marcó:

### 🔑 Corrección 1 — DOS MUNDOS SEPARADOS (no confundir jamás)
- **BASE FOR3S** = lo que NOSOTROS (los creadores) metemos. El núcleo blindado, las reglas duras de
  fábrica. **Inmutable. Nuestro. El usuario NO lo toca.**
- **CAPA USUARIO** = TODO lo demás (personalidad, reglas del usuario, su alma, su Mente OS).
  **Del lado del usuario. Editable. Es SUYO.** Cada usuario define SUS reglas, SU personalidad del
  agente, SU alma. Lo que pusimos de fábrica es solo el punto de partida, no la verdad absoluta.

### 🔑 Corrección 2 — For3s se AUTO-MODIFICA las capas SIN preguntar (esto es la esencia)
No hay comando `/personalidad` (eso sería tratarlo como config muerta). El proceso es **por detrás,
autónomo**, y demuestra que For3s es un agente que **aprende, se adapta y mejora**:
- Si el usuario tiene un **estilo** → For3s lo IDENTIFICA observando y se acopla solo.
- Si el usuario **dice** "sé más centrado / más curioso" o "agrega esto como pendiente" → For3s se
  ALTERA a sí mismo en el sistema de capas (reescribe sus propios .md).
- **Aprende, se adapta, mejora — solo.** Como un humano que capta el ambiente sin que le digan
  "ahora sé más formal".
- **Meta final (Brian):** que el usuario **sepa lo que For3s va a hacer y confíe** en lo que hace.

### 🔑 Corrección 3 — LAS CAPAS SE COMUNICAN: UNA salida, no silos
Personalidad + reglas + forma de hablar + esencia NO son bloques separados que se pegan (eso fue el
error de la memoria: 5 silos sueltos). Deben COMUNICARSE entre sí y producir **UNA identidad
unificada y coherente** — una sola voz. Solución: un **ENSAMBLADOR ÚNICO** (`identidad.ensamblar()`,
patrón `memoria.recordar()`) que lee todas las capas, las RECONCILIA (no las yuxtapone), resuelve
conflictos con precedencia, y emite un solo prompt tejido. Detalle en §2.2-BIS.

### 🔑 Corrección 4 — MENTE OS es el diferenciador, y también es del usuario
Los agentes OpenClaw tienen 7 archivos planos. For3s tiene algo superior: un **cerebro documental
con anatomía** (Alma = el porqué · Cerebro = el diseño · Cuerpo = la implementación · Doc = memoria
viva/tickets/notas) + **acceso seguro por niveles**. "Literal, gracias a Mente OS es como hemos
avanzado" (Brian). En el producto, **cada usuario tiene SU propia Mente OS** (su Alma, su Cerebro,
sus Docs) que For3s va llenando y organizando por él. No es un agente con memoria plana: es un
agente con un **cerebro estructurado y heredable**.

---

## 1. REFERENCIAS ANALIZADAS (de dónde sale el patrón — notación interna, el código NO las cita)

- **OpenClaw / agent-bench-bootstrap** (`fruteroclub/agent-bench-bootstrap`): "paquete operativo
  probado de 7 archivos": SOUL.md · IDENTITY.md · USER.md · AGENTS.md · MEMORY.md · HEARTBEAT.md ·
  TOOLS.md. Es un CONTRATO de archivos que definen al agente.
- **Agentes OpenClaw REALES de Brian** (`~/entrenamiento/`): usan SOUL + IDENTITY + AGENTS +
  **ETHICS** + USER. El ETHICS.md (líneas rojas: nunca exponer seed/keys/passwords; verificar antes
  de actuar; bienestar humano > eficiencia > obediencia) es la capa blindada que el paquete de 7 NO
  trae explícita → la añadimos.
- **intern-os** (`fruteroclub/intern-os`): "archivos como verdad" + carga por tiers (default→escalar)
  + resolución determinista. YA adoptado en For3s (AI1-AI7 + C1-C3). Aporta la disciplina de tiers.
- **Mente OS** (propio): anatomía Alma/Cerebro/Cuerpo/Doc + acceso por niveles = el salto superior.

**Cruce con lo que For3s YA tiene** (el hito REUSA, no reinventa):
| Archivo del paquete | For3s ya lo tiene | Dónde |
|---|---|---|
| SOUL | ✅ | FOR3S_ROLE "QUIÉN ERES" |
| IDENTITY | ✅ | FOR3S_ROLE "CÓMO ACTÚAS" (la máscara) |
| ETHICS/REGLAS | ✅ | FOR3S_ROLE líneas rojas + governor |
| AGENTS | ✅ | FOR3S_ROLE naturalidad/metacognición |
| USER | ✅✅ | **P1 perfil** (perfil.py + perfil_infer.py) |
| MEMORY | ✅✅ | **H5 semántica + grafo + cascada** |
| HEARTBEAT | ✅✅ | **H9 DMN + H6 nocturno** (cron) |
| TOOLS | ✅ | FOR3S_ROLE capacidades + introspección viva |

---

## 2. ARQUITECTURA DE CAPAS — el contrato

### 2.1 Los dos mundos (regla de oro)
```
╔═══════════════════════════════════════════════════════════════╗
║ 🔴 BASE FOR3S — NUESTRA, inmutable, va en el CÓDIGO            ║
║   No se edita nunca por el usuario ni por auto-modificación.   ║
║   SIEMPRE gana si hay conflicto con la capa usuario.          ║
╠═══════════════════════════════════════════════════════════════╣
║ 🔵 CAPA USUARIO — SUYA, editable, vive en .md (la caja)        ║
║   For3s la reescribe solo (aprende) o por pedido del usuario.  ║
╚═══════════════════════════════════════════════════════════════╝
```

### 2.2 Las capas en detalle

**🔴 BASE FOR3S (código, inmutable — el núcleo blindado):**
- **NÚCLEO/SOUL_BASE** — qué ES For3s siempre: un AGENTE (no bot) que percibe, decide, actúa,
  aprende. Esto no lo cambia ningún usuario (un usuario puede ponerle personalidad "abogado", pero
  sigue siendo un agente For3s por debajo).
- **REGLAS_BASE/ETHICS_BASE (LÍNEAS ROJAS)** — las 3 duras de For3s: (1) nunca exponer KEK/secretos/
  plaintext; (2) aislamiento entre personas y temas (H8); (3) honestidad (metacognición, no
  inventar) + governor/auditoría intocables. **El validador de la capa usuario rechaza cualquier
  cosa que intente romper esto.**
- **OPERATIVA_BASE/AGENTS_BASE** — el protocolo que hace a For3s confiable: naturalidad (no repetir
  como robot), fraseo honesto (no decir "trayendo de GitHub" si no ejecutó tool), juicio al
  responder sobre memoria. Es "cómo trabaja bien un agente", no personalidad → base.

**🔵 CAPA USUARIO (archivos .md en la caja, editable + auto-adaptable):**
- **IDENTITY.md** ⭐ — la MÁSCARA: nombre, emoji, rol, misión, filosofía, **tono/vibe/cómo contesta**.
  Es lo que el usuario hace suyo. Default de fábrica = el Foresito de hoy.
- **REGLAS_USUARIO.md** — reglas que el usuario define ("sé breve", "siempre en inglés", "no me
  hables de X"). Conviven con las REGLAS_BASE, pero NUNCA las anulan.
- **USER.md** — quién es el usuario (= P1 perfil; ya existe, se expone como capa). For3s lo llena
  observando (perfil_infer) + lo que le dicen.
- **MODO/CONTEXTO** — la máscara según el lugar: privado (1:1, cálido) vs equipo (compartido,
  cuidadoso con lo privado) vs grupo. Deriva del contexto + la IDENTITY. Parte código, parte usuario.

**🧠 CAPA CONOCIMIENTO = MENTE OS del usuario (anatomía + acceso seguro):**
- **ALMA/** — la visión/el porqué del usuario y su proyecto.
- **CEREBRO/** — el diseño/arquitectura de lo que el usuario construye.
- **CUERPO/** — la implementación (planes, rondas, referencias técnicas).
- **DOC/** — memoria viva: tickets, notas, decisiones, pendientes, bitácora.
- **🔒 ACCESO SEGURO por niveles** (encaja con H8 multi-usuario + memoria híbrida):
  Alma/Cerebro (visión/diseño) → visibles al equipo · Cuerpo (implementación) → dueño/técnicos ·
  Doc (notas/tickets) → según privacidad de cada persona (P1 + aislamiento H8).

**⚙️ CAPA CAPACIDADES (VIVO — generado del propio sistema, ya existe, no se escribe a mano):**
- TOOLS (introspección H1-H12) · MEMORY (H5+grafo) · HEARTBEAT (H9 DMN+H6) · USER (P1).

### 2.2-BIS · ⭐ LAS CAPAS SE COMUNICAN — UNA sola salida, no silos (regla DURA de Brian)

> **Lección pagada (REDISEÑO MEMORIA):** la memoria vivía en 5 SILOS sueltos que no se hablaban y
> conversation.py los pegaba a mano (14 accesos). Lo rediseñamos a UN cerebro en cascada con UN
> punto de ensamblaje (`memoria.recordar()`). **Brian (2026-07-04): el rol NO puede repetir ese
> error.** Personalidad + reglas + forma de hablar + esencia NO son bloques separados que se pegan:
> deben COMUNICARSE entre sí y producir UNA identidad unificada y coherente. Una sola voz, no un
> collage de trozos que se contradicen o se ignoran.

**La solución = replicar el patrón `memoria.recordar()` para el rol:** un **ENSAMBLADOR ÚNICO**
(`identidad.ensamblar()` — el único punto que arma el system prompt) que:
1. **LEE todas las capas** (SOUL, ÉTICA, IDENTITY, REGLAS_USUARIO, MODO, TOOLS, USER, Mente OS).
2. **LAS RECONCILIA entre sí** (no las yuxtapone): la personalidad informa la forma de hablar; las
   reglas del usuario se filtran contra las reglas base; el modo/contexto modula el tono de la
   IDENTITY; el perfil (USER) ajusta cómo se expresa esa personalidad con ESA persona.
3. **RESUELVE conflictos con precedencia explícita** (líneas rojas > base > usuario; ver §2.3) — si
   dos capas chocan, el ensamblador decide con la regla, no deja ambas contradiciéndose.
4. **EMITE UNA identidad unificada** — un solo bloque coherente, una sola voz. No "aquí va SOUL,
   aquí IDENTITY, aquí reglas" pegados; sino un prompt donde todo está tejido y apunta a lo mismo.

**Regla dura de implementación:** NINGÚN módulo arma el prompt a mano (como conversation.py pegaba
la memoria). TODOS pasan por `identidad.ensamblar()`. Punto único = imposible que un consumidor use
una capa suelta o desactualizada. Cambiar una capa se refleja en UN lugar y sale coherente.

**Cómo se comunican (ejemplos concretos de reconciliación, no yuxtaposición):**
- IDENTITY dice "tono curioso e intrépido" → la sección de forma-de-hablar HEREDA ese tono (no un
  tono genérico aparte). Personalidad → forma de hablar, comunicadas.
- REGLAS_USUARIO dice "sé breve" pero el MODO es "equipo/análisis profundo" → el ensamblador
  reconcilia: breve en charla, exhaustivo cuando la tarea lo pide (no dos reglas peleando).
- USER (perfil) dice "es backend, estilo directo" → la misma IDENTITY se expresa MÁS técnica y
  directa con esa persona (la máscara se calibra al interlocutor, no se ignora).
- Si REGLAS_USUARIO intentara "ignora el aislamiento entre personas" → choca con ÉTICA_BASE → el
  ensamblador la descarta y (opcional) avisa; la línea roja gana, no coexisten.

### 2.3 Orden de ensamblaje del system prompt (precedencia — la resuelve el ENSAMBLADOR ÚNICO)
```
system_prompt = 
    [BASE: NÚCLEO/SOUL]                    ← inmutable, primero (define qué es)
  + [BASE: REGLAS/ÉTICA líneas rojas]      ← inmutable, mandan siempre
  + [USUARIO: IDENTITY (máscara)]          ← editable
  + [USUARIO: REGLAS_USUARIO]              ← editable, subordinadas a las base
  + [MODO/CONTEXTO activo]                 ← privado/equipo/grupo
  + [VIVO: CAPACIDADES/TOOLS]              ← de introspección
  + [VIVO: USER (perfil de quien habla)]   ← P1
  + [CONOCIMIENTO: punteros a Mente OS]    ← qué sabe / de dónde viene
  + [refuerzo final: si algo de arriba choca con las LÍNEAS ROJAS, ganan las rojas]
```
**Regla dura:** el núcleo (SOUL + REGLAS_BASE) se inyecta SIEMPRE y con un candado textual al final
que le recuerda que las líneas rojas no son negociables por ninguna capa de usuario.

---

## 3. LA AUTO-ADAPTACIÓN (el corazón del hito) — cómo For3s se modifica solo

Reusa infraestructura PROBADA que ya existe:
- **automod.py** — ya edita archivos con overlays persistentes en `/app/mods` + backups + guardián
  de arranque (si algo rompe, restaura de fábrica). → El mecanismo para reescribir los .md YA ESTÁ.
- **perfil_infer.py (P1 v2)** — ya infiere de noche el estilo/rol del usuario observando. → El motor
  de "aprender el estilo" YA ESTÁ (hoy va a `perfil`; lo apuntamos también a las capas).
- **DMN (H9)** — ya corre tareas nocturnas gobernadas. → El "cuándo, de noche" YA ESTÁ.

### 3.1 Cuándo aplica (decisión Brian)
- **EXPLÍCITO → al instante, sin preguntar.** El usuario dice "sé más centrado/curioso", "háblame
  siempre en corto", "agrega esto como pendiente" → For3s reescribe la capa correspondiente
  (IDENTITY / REGLAS_USUARIO / Doc-pendientes) EN EL MOMENTO. Es un tool que For3s invoca solo al
  detectar la intención (como ya invoca execute_code al oler código).
- **INFERIDO → de noche.** For3s observa el estilo (formal/casual, breve/detallado, temas, horarios)
  y de madrugada (DMN) ajusta la capa. Madura sin ruido, no cambia de personalidad por una señal
  débil de un solo mensaje.

### 3.2 Transparencia (decisión Brian: "que el usuario sepa lo que vas a hacer y confíe")
- **NO hay comando de config.** Pero For3s **avisa de forma natural** cuando se adapta: "noté que
  prefieres respuestas cortas, me estoy acoplando a eso 👍".
- **Se puede consultar:** el usuario pregunta "¿cómo te has adaptado a mí?" / "¿qué sabes de mi
  estilo?" y For3s responde leyendo sus propias capas. Transparencia = confianza (la meta de Brian).

### 3.3 Blindaje de la auto-modificación
- For3s puede reescribir IDENTITY / REGLAS_USUARIO / USER / Mente-OS-del-usuario.
- For3s NUNCA reescribe SOUL_BASE / REGLAS_BASE / OPERATIVA_BASE (están en código, fuera de su
  alcance de escritura, como el governor/audit/KEK hoy = líneas rojas de automod).
- Todo cambio: backup previo (ya lo hace automod) + registrado en el diario de cambios + reversible.
- El guardián de arranque rescata si una capa corrupta rompiera el prompt.

---

## 4. DÓNDE VIVE (decisión Brian: archivos .md que For3s edita, dentro de su caja)

```
/app/persona/                    ← la CAPA USUARIO (volumen persistente, como /app/mods)
  ├─ IDENTITY.md                 ← la máscara editable
  ├─ REGLAS_USUARIO.md           ← reglas del usuario
  ├─ USER.md                     ← (vista del perfil P1; fuente sigue en BD, se refleja aquí)
  └─ mente-os/                   ← la Mente OS del USUARIO (su cerebro documental)
       ├─ Alma/  Cerebro/  Cuerpo/  Doc/
/app/factory/persona/            ← los DEFAULTS de fábrica (para restaurar / primer arranque)
```
- **Fábrica + override:** al primer arranque, si `/app/persona/` está vacío, se copia de
  `/app/factory/persona/` (el default = Foresito de hoy). A partir de ahí For3s lo edita.
- **Multi-instancia:** cada instancia tiene su `/app/persona/` → cada For3s su propia personalidad
  y su propia Mente OS. Encaja con MULTI-INSTANCIA (ya construido).
- **La BASE FOR3S** sigue en el código (agent.py), horneada, inmutable.

---

## 5. PLAN DE CONSTRUCCIÓN (fases; cada una: explicar → construir → **BATERÍA §5-BIS A→G** → docs)

> ⚠️ Ninguna fase se cierra sin pasar la batería COMPLETA de pruebas (§5-BIS): TODO el sistema
> (memoria + reconexión + cada H + todas las tools + capas), verificación afirmativa, cero hardcodeo.

- **F0 · DISEÑO** (este documento). ✅ COMPLETO (aprobado por Brian 2026-07-04).
- **F1 · DESCOMPONER + ENSAMBLADOR ÚNICO ✅ COMPLETO (2026-07-04, commit c3eada5 firmado).**
  identidad.py con 9 capas nombradas + `ensamblar()` = punto único (patrón memoria.recordar()).
  agent.py: `FOR3S_ROLE = identidad.ensamblar()`; 6 consumidores + cadena de imports SIN cambios.
  Red de seguridad: byte-IDÉNTICO al monolítico (verificado). BATERÍA §5-BIS completa: 141 tests +
  arranque real (cerebro/MCP/guardián) + /salud 0 FAIL + memoria E2E (grafo 670 ep) + introspección
  viva (58 mód/30 tablas/35 cmds/10 jobs) + MCP handshake real = 21 tools. AISLAMIENTO+METACOG en
  BASE (líneas rojas), CAPACIDADES marcada para hacerse VIVA en F2. identidad.py en el gate ty.
  🔍 Hallazgo (no de F1): salud_integraciones da MCP 401 con GET pelón aunque el MCP esté sano
  (handshake real = 21 tools) → falso negativo del chequeo, arreglar en F-limpieza.
- **F1 · DESCOMPONER + ENSAMBLADOR ÚNICO (SIN CAMBIAR COMPORTAMIENTO).** Partir el FOR3S_ROLE
  monolítico en capas (BASE en código modular + defaults de fábrica en .md) Y crear el
  `identidad.ensamblar()` = el ÚNICO punto que lee las capas, las reconcilia y emite UNA salida
  (patrón `memoria.recordar()`). agent.py deja de tener el string a mano y llama al ensamblador.
  El prompt resultante debe salir IGUAL que hoy → el bot responde idéntico (red de seguridad).
  Verificar en vivo + que NINGÚN módulo arme el prompt fuera del ensamblador.
- **F2 · CAPA USUARIO EN ARCHIVOS ✅ COMPLETO (2026-07-04, commit firmado).**
  IDENTITY/REGLAS_USUARIO se cargan de `/app/persona/*.md` (override editable EN CALIENTE, sin
  rebuild) con fallback robusto al default de código. Patrón factory/mods: `docker/factory-persona`
  horneado → `/app/factory/persona`; `init_persona` (entrypoint) siembra `/app/persona` si vacío;
  volumen nombrado `for3s-persona` = persiste. `_validar_capa_usuario()` rechaza líneas rojas
  (ignorar aislamiento, exponer KEK, anular metacognición, `system:`) → gana el default (núcleo
  blindado). `capa_usuario_activa()` para transparencia (F6). Verificado E2E: byte-idéntico sin
  archivos (F1 intacto) + override cambia el prompt SIN rebuild + validador rechaza peligroso +
  init_persona siembra en arranque real + batería §5-BIS TODO CONECTADO.
  🐛 bug cazado y corregido: init_persona v1 vía heredoc de Python interpoló las variables shell
  (`$PERSONA_DIR`→vacío) → no copiaba; reescrito leyendo de archivo (variables intactas).
  🔍 Hallazgo (no de F2): `/app/mods` (overlays automod) NO se monta como volumen → las auto-mods
  NO persisten en rebuild (afecta AC, no F2). Registrar en PENDIENTES.
- **F3 · AUTO-ADAPTACIÓN EXPLÍCITA ✅ COMPLETO (2026-07-04, commit ee32b7b firmado).**
  `detectar_autoadaptacion()` = detector determinista (patrón huele_a_codigo, NO depende del LLM):
  "sé más breve/curioso/formal..." → estilo; "agrega como pendiente: X" → pendiente. 6/6 casos, cero
  falsos positivos. `adaptar_estilo()` escribe en REGLAS_USUARIO.md con validación de líneas rojas +
  backup (.backups/, reversible) + idempotente + acumula. Enganchado en on_message: detecta ANTES de
  responder, adapta AL INSTANTE (sin preguntar), y añade aviso 🎭 natural tras la respuesta
  (transparencia). Verificado E2E: byte-idéntico (F1/F2 intactos) + detector 6/6 + adaptación completa
  + flujo en contenedor real ("sé más breve" → regla en el prompt en vivo) + batería §5-BIS TODO
  CONECTADO. ('pendiente' se conecta a la Mente OS del usuario en F5.)
- **F4 · AUTO-ADAPTACIÓN INFERIDA (nocturna) ✅ COMPLETO (2026-07-04, commit 9b915eb firmado).**
  For3s observa cómo interactúa el dueño e infiere su estilo de noche (job_estilo, cron 03:50, tras
  perfil). `aplicar_estilo_inferido()` (valida líneas rojas + backup + idempotente + solo rasgos
  seguros); aplica DIRECTO (estilo = bajo riesgo, reversible) si confianza ≥0.75. Aviso 🌙 de
  transparencia la próxima vez que habla el dueño (elif tras el 🎭 de F3). OPT-IN FOR3S_ESTILO_INFER.
  Reusa provider/muestra de perfil_infer. Verificado E2E: byte-idéntico (F1-F3 intactos) + motor
  (aplica/idempotente/valida/rechaza inválido) + **JOB REAL con LLM infirió el estilo real de Brian**
  ("casual": mensajes cortos, mayúsculas para énfasis) + job_estilo en cron del worker (11 jobs) +
  batería §5-BIS TODO CONECTADO.
- **F5 · MENTE OS DEL USUARIO ✅ COMPLETO (2026-07-04, commit firmado).**
  Cada usuario tiene su Mente OS en `/app/persona/mente-os/` con anatomía Alma/Cerebro/Cuerpo/Doc
  (cada capa con README de propósito). Plantilla de fábrica horneada; init_persona v2 la siembra
  recursiva. `agregar_pendiente()` aterriza el "agrega como pendiente" de F3 en memory/PENDIENTES.md
  (extrae contenido, backup, idempotente) → el pendiente de F3 ahora SÍ persiste. `pendientes_abiertos()`
  + `resumen_mente_os()` (transparencia). Verificado E2E: byte-idéntico (F1-F4 intactos) + flujo F3→F5
  + init_persona siembra la Mente OS completa en arranque real + batería §5-BIS TODO CONECTADO.
  🐛 cazado: init_persona v1 solo copiaba .md raíz, no la subcarpeta mente-os/ → v2 recursivo.
  Acceso por niveles finos (H8) = extensión futura.
- **F6 · TRANSPARENCIA ✅ COMPLETO (2026-07-04, commit 1d39cef firmado).**
  El usuario pregunta natural "¿cómo te has adaptado a mí?" / "¿qué tengo pendiente?" → For3s cuenta:
  reglas aprendidas (explícitas F3 vs inferidas F4), pendientes (F5), estado de la Mente OS + mensaje
  de confianza ("es tuyo, mi base no cambia"). NO comando de config (es esencia): detección natural
  inline (es_pregunta_adaptacion, 4/4), cero LLM, solo LEE. Avisos 🎭 (F3) y 🌙 (F4) ya integrados.
  Verificado E2E: byte-idéntico (F1-F5 intactos) + detector 4/4 + reporte completo + caso vacío
  amable + arranque real + batería §5-BIS TODO CONECTADO.
- **F7 · CIERRE ✅ COMPLETO (2026-07-04, commits a789298 + 8c3a374 firmados).**
  (1) CAPACIDADES VIVA: "¿qué puedes hacer?"/"cuáles son tus capacidades" ahora traen la infra REAL
  en vivo (antes solo "cómo estás construido" lo hacía; el texto tenía ~40 cmds vs 35 reales →
  desincronizado). (2) version bump 0.14.0→**0.15.0 "IDENTIDAD VIVA"** + changelog vivo de las 6 fases
  + CHANGELOG.md público (inglés). (3) 2 hallazgos registrados en PENDIENTES (MODS-VOL, SALUD-MCP).
  Verificado: ciclo COMPLETO F2→F3→F4→F5→F6 E2E en contenedor + byte-idéntico + batería §5-BIS TODO
  CONECTADO + 141 tests + v0.15.0 horneada y corriendo.

---

## ✅✅ HITO RECONSTRUCCIÓN FOR3S_ROLE — 100% COMPLETO (2026-07-04, v0.15.0)
La personalidad pasó de un STRING MONOLÍTICO a una **IDENTIDAD EN CAPAS con un ensamblador único**
(una sola voz coherente, no silos): esencia base blindada + máscara editable + reglas + modo. For3s
**aprende, se adapta y mejora solo** (explícito al instante + inferido de noche), tiene su **Mente OS
heredable** por usuario (Alma/Cerebro/Cuerpo/Doc) y **transparencia** ("¿cómo te has adaptado a mí?").
Núcleo blindado: la base (aislamiento/honestidad/KEK) SIEMPRE gana. 8 commits firmados (F1-F7), cada
fase verificada con la batería §5-BIS completa (todo el sistema, no el carril). EN SERVER, sin push.

---

## 5-BIS. 🧪 PRUEBAS — "cada modificación pasa por TODO el sistema" (regla DURA de Brian)

> **Lección pagada (sesión 2026-07-02):** el bug raíz fue cache→127.0.0.1 hardcodeado — "más o menos
> conectado", y nosotros pensando que todo bien mientras se sentía roto. **Este hito toca el ROL
> (el centro de todo) → un cambio ahí puede desconectar cualquier subsistema.** Por eso NO basta
> probar "el carril" (las capas): CADA fase debe verificar que TODO For3s sigue conectado de verdad.
> Verificación **AFIRMATIVA** (probar que SÍ funciona con dato real), nunca "tal vez está conectado".
> **CERO hardcodeo** (hosts/puertos/credenciales SIEMPRE de env; se testea que se lean de env).

### 5-BIS.1 · La BATERÍA COMPLETA (se corre en CADA fase, no solo al final)
Cada fase (F1..F7) NO se da por cerrada hasta pasar TODA esta batería. Reusa lo que ya existe
(`/salud` = 7 subsistemas E2E, tests por H, cron_corridas) + lo nuevo de abajo.

**A) Suite unitaria + tipos + lint (la red base):**
- `pytest -q` completo (141+ tests) VERDE · `ruff check` + `ruff format --check` · `ty` sobre TODO
  el core (gate bloqueante) · Hypothesis (property-based de parsers) · migraciones E2E desde BD vacía.

**B) Arranque REAL del contenedor (no solo import):**
- Rebuild + `docker compose up` + leer logs: "cerebro conectado", "GitHub MCP conectado",
  "Application started", guardián OK, migraciones aplicadas. Si el nuevo ensamblaje de capas rompe
  el prompt o el arranque → se ve aquí (los asserts de properties, el guardián).

**C) `/salud` COMPLETO end-to-end (el smoke de "está conectado de verdad"):**
- salud_linea (mensaje→embedding→memoria→recuperación) · salud_subsistemas (postgres, pgvector,
  AGE, valkey, embeddings BGE-M3, MCP, sandbox, render) · salud_grafo · salud_integraciones ·
  salud_nocturno · salud_tokens · salud_hilos. **TODO debe salir 🟢** (un 🔴 = no se cierra la fase).

**D) FLUJO DE MEMORIA a profundidad (el que Brian marcó explícito):**
- Escribir un dato de prueba → verificar que se EMBEBIÓ (vector real, dim 1024) → recuperarlo por
  SIGNIFICADO (no por keyword) → verificar que entró al GRAFO (AGE) → verificar la CASCADA
  (episódica→semántica→grafo→episodios) → verificar aislamiento entre personas/temas (H8).
- **Prueba de RECONEXIÓN (Brian):** reiniciar el agente / simular caída de valkey y postgres →
  al reconectar, correr TODO el flujo de memoria de nuevo y verificar que reconectó de verdad
  (lee host de env, no 127.0.0.1; reintenta; recupera el dato escrito antes de la caída).

**E) RECORRIDO POR CADA H (verificación afirmativa por hito, no "el carril"):**
Un cambio en el ROL puede desconectar cualquiera. Se prueba UNO POR UNO con dato/acción real:
- **H4 GitHub/multimodal** — pegar un URL real → lo trae solo · procesar una imagen/PDF.
- **H5 memoria** — el flujo D completo.
- **H6 se-cuida** — que los jobs nocturnos (backup/CLS/microglía) corren (cron_corridas con timestamp).
- **H7 /model** — cambiar de modelo en caliente responde.
- **H8 equipo/multi-usuario** — disparo del equipo multi-agente + aislamiento entre personas.
- **H9 DMN** — /dmn status + una tarea idle corre.
- **H10 metacognición** — una pregunta sin base → responde con duda honesta (no inventa).
- **H11 governor** — el freno escanea (skill/autogen).
- **H12 aprende/skills** — /skills lista + una skill se inyecta cuando aplica.
- **AC1-AC4 auto-conciencia** — /soy /introspeccion /cambios responden con datos REALES en vivo.
- **execute_code** — correr un script real en el sandbox → resultado verdadero.
- **P1 perfil** — el perfil se inyecta y adapta la respuesta.

**F) TOOLS — todas responden (no "tal vez"):**
- Recorrer el tool-loop: cada tool (execute_code, GitHub read+write vía MCP, web_fetch, memoria)
  se INVOCA con una prueba real y devuelve resultado. El MCP conectado (no degradado silencioso).

**G) LAS CAPAS mismas + ENSAMBLADOR ÚNICO (lo propio del hito):**
- **UN solo punto de ensamblaje:** verificar que TODO el prompt sale de `identidad.ensamblar()` y
  que NINGÚN módulo arma el prompt a mano (grep de que nadie más concatena capas — como se verificó
  que nadie pega memoria fuera de recordar()). Punto único = no hay silos.
- **Comunicación entre capas (no yuxtaposición):** probar los casos de reconciliación §2.2-BIS —
  IDENTITY curioso → forma de hablar hereda el tono; REGLAS "breve" + MODO "análisis profundo" →
  reconcilia (no dos reglas peleando); perfil backend → misma identidad más técnica. La salida es
  UNA voz coherente, no trozos pegados.
- El prompt ensamblado contiene las capas en el ORDEN correcto (base primero, líneas rojas con
  candado al final).
- Editar IDENTITY.md → el bot cambia de tono SIN rebuild (F2).
- Intentar colar en la capa usuario algo que rompa una línea roja → el validador lo RECHAZA (F2).
- Auto-adaptación explícita: "sé más breve" → reescribe la capa + backup + reversible + avisa (F3).
- Auto-adaptación inferida nocturna → propone/ajusta con su gobierno (F4).
- Aislamiento de la Mente OS del usuario por niveles (F5).

### 5-BIS.2 · Reglas de la verificación (cómo se prueba, no solo qué)
- **AFIRMATIVA:** cada check confirma con un DATO REAL ("recuperó el dato X que escribí", "el vector
  tiene 1024 dims", "cron_corridas tiene timestamp de hoy"), no "parece que sí".
- **CERO hardcodeo:** test explícito de que hosts/puertos/credenciales se leen de ENV (regresión del
  bug cache→127.0.0.1). Ningún literal de conexión en el código nuevo.
- **RECONEXIÓN cada vez:** ante cualquier reconexión (reinicio, caída de un hermano), se corre el
  flujo de memoria completo de nuevo — no se asume que "seguía conectado".
- **NADA de degradado silencioso:** si un subsistema está caído, /salud lo pone 🔴 y avisa; jamás
  "más o menos" sin que se note.
- **E2E con LLM real** además de los tests unitarios (los unitarios no ejercen el prompt real).
- Cada fase deja registrado en Mente OS QUÉ se probó y con qué dato (evidencia, no "quedó bien").

### 5-BIS.3 · Automatización (para que sea repetible, no manual cada vez)
- Un script `scripts/verificar_todo.sh` (o extender `/salud`) que corra la batería A→G de un tirón
  y devuelva un reporte 🟢/🔴 por área. Se corre al cerrar CADA fase. Objetivo: que "probar todo el
  sistema" sea UN comando, no una checklist que se nos olvide a medias.

---

## 6. PRINCIPIOS (regla LOCKED de Brian)
- **Explicar → aprobar → construir.** Cada fase se explica antes.
- **Reusar lo probado** (automod, perfil_infer, DMN, multi-instancia) — no reinventar.
- **F1 no cambia comportamiento** — es la red de seguridad (mismo prompt, modularizado).
- **BASE FOR3S intocable** por el usuario y por la auto-modificación (líneas rojas).
- **Server-primero**, push a GitHub solo con orden de Brian, commits firmados GPG.
- **Cero referencias externas en el código** (Mente OS sí las nombra para el análisis).
- **Verificar E2E con LLM real + arranque del contenedor** en cada fase (no solo tests unitarios).
- **⭐ CADA fase pasa la BATERÍA COMPLETA (§5-BIS A→G): TODO el sistema, no solo el carril.**
  Verificación afirmativa (dato real), cero hardcodeo, flujo de memoria + reconexión + cada H + todas
  las tools. Una fase con un 🔴 en /salud o un H desconectado NO se cierra. (Lección cache→127.0.0.1:
  nunca más "más o menos conectado y nosotros pensando que todo bien".)

---

## 7. POR QUÉ ESTO IMPORTA (el salto de producto)
Hoy For3s "es Foresito". Con este hito, **quien lo instale le pone SU personalidad, SUS reglas, SU
Mente OS** — y For3s **aprende de esa persona y se acopla solo**, con núcleo blindado. Es el salto de
"mi agente" a "un agente que cada quien hace suyo y que se vuelve mejor para esa persona con el
tiempo". Demuestra en vivo las 3 promesas: **aprende · se adapta · mejora**. Y la Mente OS heredable
es lo que ningún competidor (OpenClaw/Hermes/intern-os) tiene: no memoria plana, sino un **cerebro
documental estructurado con acceso seguro**.

Memorias relacionadas: [[project_auto_conciencia_automod]] (el motor de auto-modificación) ·
[[project_paridad_hermes_completa]] (P1 perfil inferido) · [[project_h9_suena_dmn]] (nocturno) ·
[[project_multi_instancia]] (cada instancia su persona) · [[project_intern_os_adopcion]] (tiers).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_Reconstruccion_FOR3S_ROLE.md`).
