# 🧠 VISIÓN — Mente OS v2: de archivo que documenta a sistema que gobierna
**Status:** current · **Type:** architecture · **Updated:** 2026-07-29 · **Owner:** brian
> **Autor de la visión:** Brian López · **Fecha:** 2026-07-27
> **Estatus:** ✅ **VISIÓN CERRADA · 26 DECISIONES TOMADAS** — pendiente de la fase F0 y aprobación
> para construir. **Nada construido.**
> **Capa:** Alma (el POR QUÉ).
>
> **Los otros 3 documentos del v2:**
> - 🏗️ **El plano:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` (1,856 líneas · el CÓMO)
> - 🗺️ **El plan:** `docs/plan-v2-rollout.md` (9 fases · 38 tickets · el CUÁNDO)
> - 🔬 **Las referencias:** `docs/analysis-internos-v1.md` +
>   `docs/analysis-frameworks-v2.md` (**4 frameworks comparados**)
---

## 0 · La frase que resume todo (Brian, 2026-07-27)

> **"ESTANDARIZAR, TRAZABILIZAR, SABER DÓNDE ESTÁ LA DATA. CONTROLAR LOS PROCESOS DE LA IA.
> EJECUTA INSTRUCCIONES CLARAS, NO LO DEJAMOS QUE LO HAGA ÉL SOLO."**

Mente OS hoy **documenta bien** — eso se conserva, es su mayor logro. Lo que le falta es
**gobernar la ejecución**. La v2 no reemplaza al documentador: le añade el control de procesos.

---

## 1 · POR QUÉ estamos mejorando (el diagnóstico que lo motiva)

Todo lo de abajo está medido, no supuesto. Evidencia completa en
[[project_ser_duenos_del_contexto]] y [[project_incidente_degradacion_21jul]].

### 1.1 · No existe estándar de nada (Brian, literal)
> *"se documenta lo que se hace, está bien, pero la forma, los estándares que debe seguir esa
> documentación no la tenemos... todo está hecho como la IA quiso, es decir tú, nunca ocupaste
> nada como base, eso me preocupa."*

**Medido:** 0 plantillas en 188 documentos · solo 15/188 declaran cuándo se actualizaron ·
`CLAUDE.md` (que gobierna todo) tiene **1 solo commit** en su historia: las reglas cambian sin
dejar rastro · el índice maestro `memory/archive/README.md` inventaría ~35 de 188 (regla incumplida ~150 veces).

### 1.2 · La IA escribe código sin metodología (el dolor de la demo)
> *"sabe escribir código pero no sabe qué hacer, no tiene una metodología, no sabe sobre
> protocolos, estructura de datos... soluciona por solucionar, tiene demasiadas redundancias...
> como producto no sirve, esto no sirve para venta, solo se reirán porque es vibecoding."*

**Medido en la demo:** 25 de 60 commits son fixes (**42%**) · `userStore.ts` tocado **21 veces** ·
`for3sChat.ts` 14 veces. Prueba textual del fix-sobre-fix: el commit *"barrido completo del patrón
cookie kind ≠ instancia real"* llegó **4 commits después** de *"guardar la API key en la instancia
REAL"* — se arregló el síntoma, no la causa, y hubo que volver.

### 1.3 · El único estándar que existe es pasivo y no cubre calidad interna
El **Método de Fases F** (LOCKED 2026-07-04) gobierna proceso y verificación funcional, pero:
- **No hay nada que lo exija** — ningún hook, gate ni check. Medido: en 2 de 5 sesiones
  analizadas **nunca se leyó**, incluida la de la demo (1,276 requests, 0 lecturas).
- **Cero líneas** sobre diseño de datos, estructura de carpetas, protocolos entre piezas,
  duplicación o convenciones de nombres. → Se puede aprobar la batería §5-BIS completa y entregar
  algo que funciona por fuera y está mal por dentro. **Verifica que funcione, nunca que esté bien hecho.**

### 1.4 · El contexto muere y con él el alcance
Lo que sobrevive a `/clear`: el estado y los hechos. Lo que **NO** sobrevive: el **alcance**
("qué construimos y qué queda fuera"), el **criterio** ("por qué así") y el **grafo**
("qué toco y hasta dónde propaga").

**Medido:** 8 auto-compactaciones sin revisar (7-jun, 30-jun, 1-jul, 3-jul, 23-jul…) ·
5 de 11 sesiones nunca registradas · **Brian repitió el mismo diagnóstico 5 veces**
(26-jun, 23-jul, 24-jul, 26-jul, 27-jul) y se perdió cada vez.

Peor que perderlo: **la IA lo reconstruye por inferencia y suena igual de segura.**

### 1.5 · El sistema no tiene defensas activas (el incidente del 21-jul)
Sesión de 4 días, contexto hasta **835K** (umbral rojo: 500K), **6 violaciones de scope**
escribiendo en `marca-personal/Mente/` (prohibido en CLAUDE.md). Brian:
*"NO ERES EL MISMO DE SIEMPRE... NO ME SIRVES ASÍ."*

El umbral estaba escrito y no pudo aplicarse. El scope estaba escrito y no pudo protegerse.

### 1.6 · La ley que explica todos los casos
| Mecanismo | Forma | Cumplimiento medido |
|---|---|---|
| Gate NavigoX, permisos fail-closed | **código** | ✅ 100% |
| Método F, registro pre-/clear, índice | **documento** | 🔴 falla 40-60% |

> **Lo que está en código se cumple siempre. Lo que está en documento falla la mitad de las veces.**
> No es falta de voluntad: **un documento no puede negarse.**

---

## 2 · Los 8 cambios de fondo de la v2

### ① Portabilidad — Mente OS sin dueño tecnológico
> *"un sistema que sin importar qué IA ocupes puedas ocupar Mente OS."*

El arranque automático (`CLAUDE.md` + protocolo) deja de depender de Claude Code. Cualquier IA
que lea el protocolo puede operar el sistema. **Mente OS deja de ser un accesorio de una herramienta.**

### ② El BLOQUE como unidad atómica de todo
> *"Cada vez que existe algo que asignar es un bloque y ese bloque debe tener reglas."*

Toda acción vive en un bloque que declara **qué SÍ y qué NO se puede hacer**, sus conexiones con
otros bloques, y su estado. **Varios bloques abiertos, uno solo en ejecución.** Sub-bloques que
deben cerrarse antes de que avance el grande.

### ③ Los 3 ENCARGADOS — simultáneos y del mismo nivel
> *"Van a existir más estándares pero nunca puede ser mayor a 3 porque si no el sistema no entiende."*

**1. Estilo/formato de documentación · 2. Desarrollo · 3. Validación del flujo funcional.**
Sin jerarquía entre ellos. Con **retroceso**: si Desarrollo no aprueba el plan, vuelve al paso
anterior a mejorarse. El límite de 3 es una decisión de diseño deliberada, no una limitación.

### ④ Fix ≠ parche (ataca el fix-sobre-fix)
> *"No se crea un código o solución arriba solo para tapar el problema. Se evalúa la construcción,
> a partir de saber todo el contexto del código se establece cómo solucionar el error."*

Ante un fallo: entender el contexto completo del código → decidir la solución real → aunque
implique otro camino. **Lo que no está bien es acumular decenas de código sin orden.**

### ⑤ Ser dueños del contexto POR BLOQUE
> *"Necesitamos guardar caché por bloque y contexto por bloque... tener contexto unitario y global."*

El contexto deja de vivir en la conversación y pasa a vivir en el bloque, en disco.
**El disco es la fuente de verdad; la conversación es caché desechable.** Así `/clear` deja de doler.

### ⑥ ⭐⭐⭐ EL VEREDICTO DE CALIDAD — QA dentro de Mente OS
> *"En la demo, ANTES del clear me dijo 'todo está perfecto'. Le di clear y me dijo 'sí está bien,
> mejoró, pero aún sigue roto'. ¿Me mientes o qué pasa? **Ese dolor es el que más me impide
> trabajar.** Ya no es ver si funciona, es ver si lo que está escrito es un producto o es un MVP
> hecho para que funcione, hecho por IA."*

**Medido:** 9 minutos separan *"el sistema está completo"* de *"lo implementa a medias"*. Lo único
que pasó entre medias fue un `/clear`.

> ## 🚫 La IA no declara "está bien". La IA REPORTA LA MEDICIÓN.

Dos capas: **① medible por script** (código muerto · duplicación · tests · grafo) y
**② criterio de senior** — 6 dimensiones (arquitectura · datos · abstracción · nombres · contratos ·
**necesidad**), cada una con **evidencia exigida** que impide que la IA se autoapruebe.

> **Brian:** *"así v2 se diferencia... tenemos QA como uno de los elementos internos de Mente OS y
> eso vale oro. Que no sea 'me lo dio la IA y no sé', sino que **se sienta hecho por un senior de
> 50 años de experiencia**."*

### ⑦ ⭐⭐ LA VOZ — Mente OS también gobierna cómo se comunica
> *"Necesito tenerlo, porque debe existir esa diferencia, ocupando Mente OS."*

**Medido:** `CLAUDE.md` sin reglas de estilo · `output-styles/` inexistente · `.claude/settings.json` sin
`outputStyle`. **Ese *"se siente hecho por IA"* no viene de un archivo mal configurado: viene de
que nadie escribió el archivo.**

8 reglas **negativas y verificables** (Encargado 0, transversal). La séptima es la misma doctrina
del punto ⑥: **afirmación sin verificar = prohibida.**

> **Es la misma enfermedad que el código:** producir la forma correcta sin el juicio detrás.

---

### ⑧ ⭐⭐ IDIOMA — inglés para la máquina, español para el pensamiento
> *"Cuando tengamos que poner instrucciones de texto, todo será en inglés — inglés de Estados Unidos."*

**Todo lo que la IA lee como INSTRUCCIÓN va en 🇺🇸 inglés de EE.UU.**: `CLAUDE.md` · los output
styles · los 4 owners · los contratos · las reglas · los casos · **`BLOCK.md`** · la salida de los
validadores. **El pensamiento de Brian sigue en 🇪🇸**: visión, plan, análisis, RETOMAR, bitácora,
memorias y las conversaciones.

**Vocabulario canónico traducido:** block · sub-block · owner-0/1/2/3 · lane · scope IN/OUT ·
friction · quality verdict · sufficiency check · checkpoint.

> **El criterio de corte:** *¿esto lo lee la IA para SABER QUÉ HACER, o lo lee un humano para
> ENTENDER QUÉ PASÓ?* Lo primero en inglés, lo segundo en español.
> Detalle: `rules/NAMING_CONVENTION.md` · arquitectura §0-BIS.

---

## 3 · El principio que cruza todo: mejora continua

> **"EL SISTEMA FUNCIONA A TRAVÉS DE MEJORA CONTINUA. NO EXISTEN REGLAS INMUTABLES, EXISTEN
> APUNTADORES A REGLAS. NO SE LLAMAN POR PALABRAS RESERVADAS. DEBEMOS TENER ESTÁNDARES PERO
> MEJORANDO CON CRITERIOS DEL USUARIO."**

Tres consecuencias de diseño:
- **Apuntadores, no copias.** Una regla vive en un sitio y todo lo demás la apunta (mismo criterio
  que ya funciona en `Maestro/punteros.tsv`: *"la sincronía a mano murió"*).
- **Sin palabras reservadas.** Nada se invoca por un nombre mágico que colisione o se congele.
- **Los estándares evolucionan** con el criterio de Brian. Un estándar inmutable se vuelve fósil.

---

## 4 · Lo que la v2 debe lograr (criterios de éxito)

| # | Objetivo | Hoy | Cómo se mide que se logró |
|---|---|---|---|
| 1 | **Estandarizar** | 0 plantillas | Todo bloque/documento nace de un contrato |
| 2 | **Trazabilizar** | 5/11 sesiones sin registro | Todo proceso deja rastro verificable |
| 3 | **Saber dónde está la data** | índice miente (~35/188) | Índice generado, no escrito a mano |
| 4 | **Controlar el proceso de la IA** | "lo hace él solo" | La IA ejecuta instrucciones claras del bloque |
| 5 | **Ser dueño del contexto** | muere con `/clear` | El bloque en disco reconstruye el contexto |
| 6 | **Matar el fix-sobre-fix** | userStore ×21 | Se evalúa la construcción antes de tocar |
| 7 | **Portabilidad** | atado a Claude Code | Otra IA opera Mente OS con el mismo protocolo |
| 8 | **Conservar lo que ya funciona** | documenta bien | La capacidad documental **no se degrada** |
| 9 | ⭐ **Saber si es producto o MVP** | opinión que cambia con el `/clear` | veredicto **medido y reproducible** |
| 10 | ⭐ **Que no se sienta hecho por IA** | sin reglas de voz configuradas | 8 reglas negativas aplicadas siempre |
| 11 | ⭐ **Que el sistema se vigile solo** | 3 fallos vivieron semanas hasta que Brian preguntó | `check-health` corre en cada arranque · **si hay que pedirlo, no está automatizado** |

---

## 5 · Lo que NO se toca (ya funciona — no reinventar)

- **La capacidad documental** — es el mayor logro de Mente OS. La v2 la conserva íntegra.
- **El gate de Puentes** (`acceder mente <proyecto>`) — verificado: se cumple.
- **Los permisos fail-closed del Maestro** — código real, 100% de cumplimiento.
- **El Registro de Conversaciones** — telemetría con umbrales calibrados con datos reales.
- **El cold-start brief** — arrancar cuesta ~38-40K tokens, constante. Funciona.
- **La regla madre del Método F** (explicar→aprobar→construir) — se conserva y se hace exigible.

---

## 6 · ⭐ VALIDACIÓN EXTERNA — 4 frameworks comparados

Se analizaron **internOS · Agent OS · Open SWE · OpenTag** (detalle en
`docs/analysis-frameworks-v2.md`). Tres conclusiones que sostienen el v2:

**① El veredicto de calidad es un hueco REAL del mercado.**
Cuatro frameworks maduros, en producción, y **ninguno responde *"¿esto es producto o MVP?"***.
Todos resuelven **coordinación**; ninguno **verificación de calidad interna**.
→ No es una obsesión de Brian: **es el diferenciador del v2.**

**② El enforcement duro queda validado por contraste.**
Agent OS aplica estándares *"sin enforcement pesado"* — el camino que el v2 rechazó con datos
(código 100% · documento 40-60%). Saber que otro proyecto tomó el camino contrario convierte la
decisión del v2 en **postura consciente, no exceso**.

**③ El criterio debe venir de Brian, nunca del código existente.**
Agent OS extrae estándares del código que ya existe. Aplicado a la demo, **extraería el vibecoding**
(`userStore.ts` ×21 se volvería el estándar). La decisión 3 no se toca.

> 🔴 **Y la lección incómoda:** los cuatro **están construidos y funcionando**. El v2 tiene el mejor
> diseño y **cero líneas escritas**. Es el patrón que nos trajo aquí — diseñar mucho antes de validar
> poco. El plan lo previene, **pero solo si se respeta.**

---

## 7 · ✅ LAS DECISIONES CERRADAS (2026-07-27)

> 🤖 **FUENTE ÚNICA: `docs/DECISIONS.md`** (generado desde los 27 ADR de `rules/decisions/`).
> Esta tabla es un resumen de lectura. Se borra en F7.

| # | Decisión |
|---|---|
| 1 | **BLOQUE = unidad de trabajo** que agrupa tareas con la misma relación · **SUB-BLOQUE = tarea → una pieza de código** |
| 2 | Es para que **la IA trabaje mejor con reglas de expertos** + que **cualquiera tenga el mismo criterio** |
| 3 | **El criterio lo diseña Brian.** La IA solo le da forma. ⛔ *La IA no inventa criterio* |
| 4 | **3 CARRILES de fricción** · el carril lo decide **la propagación, no la IA** |
| 5 | **Roce con reglas:** cumplir → registrar → seguir → proponer al cerrar. Excepción: daño real |
| 6 | Los bloques viven en **Mente OS versionado en git** |
| 7 | Bloque cerrado **se archiva como experiencia consultable** (no muere) |
| 8 | **Migración POR DEMANDA.** Piloto deliberado: la DEMO |
| 9 | **ARCHIVO ÚNICO por bloque** (secciones A-K, ≤150 líneas) |
| 10 | **PROGRESIVO con MÍNIMO DURO**: 4 campos al abrir, todo al cerrar |
| 11 | **4 CAPAS** para garantizar que un archivo se lea (enrutador · bloque · hook · validador) |
| 12 | **Solo 3 acciones BLOQUEAN.** Todo lo demás avisa |
| 13 | ⭐ **VEREDICTO DE CALIDAD en 2 capas** — medible + criterio con evidencia exigida |
| 14 | **Brian aporta las 6 dimensiones de QA** por disciplina |
| 15 | **Anidamiento: máximo 3 niveles** (`BLOQUE › GRUPO › SUB-BLOQUE`) |
| 16 | **La estructura nueva CONVIVE** — cero punteros rotos |
| 17 | **El aprendizaje se consulta con el mismo mecanismo que los estándares** |
| 18 | ⭐ **ENCARGADO 0 · LA VOZ** — Mente OS también gobierna cómo se comunica |
| 19 | ⭐ **Los validadores COMPLETAN lo derivable** (marcado `auto:`), nunca el criterio |
| 20 | ⭐ **RECIBO DE APROBACIÓN** cuando una puerta bloquea — 1 pantalla, con la propagación |
| 21 | **Un error es CASO** si pasa 3 preguntas · umbral a las 2 repeticiones · máx 12 casos activos |
| 22 | **Regla que estorba** = 3 roces en bloques DISTINTOS · no caduca · se eleva a Brian |
| 23 | ⭐⭐ **IDIOMA: instrucciones en 🇺🇸 inglés de EE.UU. · pensamiento de Brian en 🇪🇸** |
| 24 | ⭐⭐ **`check-health` audita el sistema SOLO en cada arranque** — *si hay que pedirlo, no está automatizado*. Nunca borra evidencia forense |
| 25 | ⭐⭐⭐ **4 reglas de higiene de config:** secretos se referencian · toda ruta declara su por qué · **un mecanismo una entrada** · rutas portables |
| 26 | **Granularidad de un permiso = el MECANISMO, no la invocación** (234 entradas eran 1) |

### Lo único que queda abierto (fase F0 del plan)
1. ¿Cuándo un error **merece** convertirse en caso? (no todos lo merecen)
2. ¿Cómo se detecta que una regla estorbó **3 veces** y debe revisarse?

---

👉 **SIGUIENTE PASO: la fase F0** del `docs/plan-v2-rollout.md` — cerrar las 2
preguntas y aprobar el orden. Después **F1: el criterio de Brian**, que es lo único que bloquea todo
lo demás.

Relacionado: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (el plano) ·
[[project_ser_duenos_del_contexto]] · [[project_incidente_degradacion_21jul]] ·
[[feedback_estandar_metodo_fases_f]] · `rules/ESTANDAR_Metodo_Fases_F.md` (lo que se absorbe).

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (cómo se construyó lo que esta visión pedía) · `docs/architecture/how-it-runs.md` (el flujo vivo) · `CAPABILITIES.md`.
