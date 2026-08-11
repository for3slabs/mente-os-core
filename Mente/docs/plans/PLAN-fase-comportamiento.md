# 🗺️ PLAN · FASE 4 — EL COMPORTAMIENTO (lo que 3 fases de código no ven)
**Status:** current · **Type:** plan · **Updated:** 2026-08-11 · **Owner:** brian
**Campaña:** `campaigns/producto-for3s-os/CAMPAIGN.md`
**Origen:** 3 papers que Brian aportó el 2026-08-11 — TorchLean · Stream RAG · Scaling Self-Play
**Barrido que lo sostiene:** medido EN EL SERVIDOR el 2026-08-11, no leído de un documento
---

## Purpose

Las 3 fases de la campaña (nodos → carpetas → flujos) juzgan **el código**. Ninguna juzga **el
sistema corriendo**. Esta fase mide lo que solo se ve con For3s OS en marcha: **cuánto tarda, si
acierta, y qué está probado frente a qué se asume**.

> **Brian, 2026-08-11:** *"La latencia y ese tipo de cosas para nada fueron consideradas… son
> documentos que nos ayudan a entender un panorama en el cual no hemos construido."*

⛔ **Los papers NO son fuente de verdad.** La autoridad sigue siendo `Cerebro/For3s_OS_Grafo_Maestro.md`
(`rules/rule-product-authority.md`). De ellos se toma **vocabulario y método**, jamás el criterio.

---

## 1 · EL BARRIDO — qué es For3s OS hoy, medido

### 1.1 · La forma

| Medida | Valor |
|---|---|
| Archivos propios (`for3s_core`) | **76** · **26,939 líneas** |
| Funciones | **492** |
| Con docstring | **76 / 76** ✅ |
| Con type hints | **76 / 76** ✅ |

⭐ **Dato que corrige una expectativa:** el código **no está sin documentar**. Está documentado y
tipado al 100%. El problema no es higiene — es que **nadie mide qué hace cuando corre**.

### 1.2 · 🔴 Tres archivos concentran el peso

| Archivo | Líneas | % del total |
|---|---|---|
| `telegram_channel.py` | **4,570** | **17%** |
| `conversation.py` | 1,871 | 7% |
| `api_channel.py` | 1,146 | 4% |

📊 **Distribución:** 3 archivos >800 líneas · 15 entre 400-800 · 34 entre 150-400 · 24 <150.

⚠️ **`telegram_channel.py` es la puerta por la que Brian usa For3s todos los días**, y es el archivo
más grande del sistema por un factor de 2.4. Si algo se rompe ahí, se rompe la vía principal.

### 1.3 · 🔴 La instrumentación — el hueco central

| Qué | Cuántos de 76 |
|---|---|
| Registran errores (logging) | 43 |
| Tienen timeout | 18 |
| Tienen reintento | 12 |
| ⭐ **Miden su propio tiempo** | 🔴 **6** |

**Y de esos 6, el reparto importa más que el número:**

| Camino | Mide tiempo | Percentiles |
|---|---|---|
| `api_metering.py` — **el canal que se vende** | ✅ | ✅ **p50 · p95 · max**, excluyendo errores para no sesgar |
| `agent.py` — **el agente** | 🔴 **0** | 🔴 |
| `tool_loop.py` — el bucle de herramientas | 🔴 **0** | 🔴 |
| `multiagente.py` — el equipo | 🔴 **0** | 🔴 |

⭐ **El hallazgo del barrido, en una frase: lo que se COBRA está medido; lo que se USA, no.**
Nadie sabe cuánto tarda For3s en responderle a Brian, ni en qué etapa se va el tiempo.

### 1.4 · El sistema vivo — 24h del agente `brian`

| Medida | Valor |
|---|---|
| Líneas de log en 24h | **27** |
| De ellas, con error | **4** |
| Error real encontrado | `RuntimeError: sin github_token en el vault` |
| Otro | `Red Telegram inestable (NetworkError) — reintenta solo` |

⚠️ **27 líneas en 24 horas es un sistema que casi no habla de sí mismo.** No es silencio sano: es
ausencia de instrumentación. Un fallo intermitente sería invisible.

### 1.5 · La base de datos — qué se usa de verdad

| Tabla | Filas |
|---|---|
| `episodes_events` | **33,908** |
| `DERIVED_FROM` (grafo AGE) | **31,230** |
| `Episodio` (grafo AGE) | 31,037 |
| `audit_events` | 12,908 |
| `import_manifiesto` | 11,927 |
| `dmn_corridas` | 3,203 |
| `sessions` | 2,072 |
| `Concepto` (grafo) | 1,342 |
| `cron_corridas` | 1,035 |

🔴 **18 tablas VACÍAS**, y sus nombres dicen qué capacidad no se está usando:
`decisiones` · `misiones` · `estado_persona` · `tema_estado` · `temas_equipo` · `solicitudes` ·
`consulted_web` · `gh_files` · `gh_resources` · `maestro_chunks` · `governor_bloqueos` ·
`trace_events` · `trace_alertas` · `api_waitlist`.

⭐ **Esto es el diagnóstico del 13-jul, ahora con números:** *"se usó como TUBO y nunca devolvió
valor"*. **33,908 episodios guardados y `decisiones` en cero.** El sistema recuerda muchísimo y
**no decide nada** — la memoria entra y no sale.

⚠️ **`trace_events` y `trace_alertas` vacías** significa que **For3s TRACE no está registrando**, y
es una de las capacidades que se presentó en el Incubathon.

---

## 2 · LO QUE CADA PAPER APORTA — y qué se descarta

### 2.1 · 📄 Stream RAG → **la disciplina de medir**

⛔ **NO se adopta el streaming.** Su técnica —lanzar la consulta antes de que el usuario termine de
hablar— resuelve un problema que For3s no tiene hoy.

**Sí se adoptan tres disciplinas:**

| # | Disciplina | Su evidencia | Qué cambia aquí |
|---|---|---|---|
| **1** | **Partir la latencia por ETAPA** | no dicen *"tarda 5.90s"*: dicen consulta **0.59** · herramientas **2.78** · respuesta **2.52** | el cuello se ve sin adivinar — el suyo era traer páginas web, **no el modelo** |
| **2** | **P50 y P90, nunca promedio** | último token: **20.07s** en mediana, **48.16s** en P90 | el promedio habría escondido los 48 |
| **3** | ⭐ **La brecha entre canales** | mismo modelo: **39.6%** en texto vs **26.3%** en voz | ¿el Telegram de For3s responde peor que su API? **Nadie lo ha medido** |

⭐ **El #3 es el más aplicable y el menos obvio.** Ellos midieron el **mismo motor** por dos salidas
y encontraron 13 puntos de diferencia. For3s tiene exactamente esa forma: `telegram_channel.py`
(4,570 líneas) y `api_channel.py` (1,146) sobre el mismo núcleo.

### 2.2 · 📄 TorchLean → **el vocabulario y la lista de terminado**

**A · Los tres niveles de certeza.** Su convención de lectura, literal:

| Término | Qué significa |
|---|---|
| **Proved** | un teorema sobre la semántica declarada |
| **Checked** | un validador ejecutable comprueba un artefacto finito |
| **Boundary** | un runtime externo se usa **bajo supuesto explícito**, no confiado en silencio |

🔴 **El tercero es el que falta.** Hoy *"lo verifiqué"* y *"asumí que funciona"* se escriben igual.
For3s OS tiene fronteras reales sin declarar: la API de Claude, Telegram, el compilador de nada, el
vault de secretos. **`RuntimeError: sin github_token en el vault` es exactamente una frontera que
falló sin estar declarada.**

**B · La regla de 5 pasos.** Su forma de añadir una pieza — *"lo tratamos como un compromiso
completo"*: semántica → tipo → derivada → regla de verificación → backend numérico.
⭐ **Una pieza no está terminada hasta que trae las cinco.**

Eso es lo que le falta al 1:1 de la campaña: **la lista de qué debe traer un archivo para darse por
aprobado.** Traducida a For3s OS en §3.2.

**C · Su tesis central, que ya es tuya.** *"Una propiedad puede probarse sobre un objeto mientras el
sistema desplegado ejecuta otro."* Es lo mismo que decidiste en `rule-product-authority`: el grafo
manda, el código se audita. **Confirma la decisión, no la cambia.**

### 2.3 · 📄 Scaling Self-Play → **una lección, y es cara**

⛔ **Lo demás no aplica.** Auto-juego, RL, leyes de escala: For3s no entrena modelos.

⭐ **La lección que sí:** su generador **colapsó produciendo basura que puntuaba bien en su propia
métrica**. El 80% de sus problemas acabó siendo disyunciones enormes — **cumplían el criterio y no
servían para nada**. Su cura: **un juez independiente** que puntuaba si el resultado **servía al
objetivo**, no si cumplía la forma.

**Traducido a esta campaña:** si se mide solo *"pasa las 6 dimensiones"*, algo acabará optimizando
para eso. **El antídoto ya existe y hay que usarlo:** el criterio de cierre de la campaña no es
técnico — es *"Brian confía en delegarle trabajo"*. Ese es el juez independiente.

---

## 3 · LAS 5 SUB-FASES — cada una entrega UNA cosa verificable

> `principles/expertise/doc-planning.md`: una fase entrega **una** cosa verificable y declara de qué
> depende. Si entrega dos, no se sabe cuál falló.

> ⭐ **LA FASE VA PARTIDA EN DOS MOMENTOS** (Brian, 2026-08-11). No es una 4ª fase entera al final:
> **B1 va ANTES de la fase 1**, el resto al final.

| # | Sub-fase | Cuándo | Entrega | Cierra cuando |
|---|---|---|---|---|
| **B1** | **Declarar las fronteras** | ⭐ **ANTES de la fase 1** | cada dependencia externa marcada `Boundary` con su supuesto | 🔬 se corta una frontera y el sistema **dice cuál**, no *"error"* |
| **B2** | **Instrumentar el camino del agente** | tras las 3 fases | `agent.py` · `tool_loop.py` · `multiagente.py` miden su tiempo **por etapa** | 🔬 una consulta real produce el desglose por etapa |
| **B3** | **Percentiles, no promedios** | tras B2 | p50 · p90 · max, reusando el patrón de `api_metering` | 🔬 p90 ≠ p50 en los datos reales: si son iguales, no se está midiendo |
| **B4** | ⭐ **La brecha entre canales** | tras B2 | la misma pregunta por Telegram y por API, comparada | 🔬 se reporta la diferencia **con número**, aunque sea cero |
| **B5** | **Los presupuestos** | tras B3 · B4 | los números objetivo, **puestos con datos en la mano** (§6.1) | un check falla cuando el sistema los rebasa |

### 3.0 · ⭐ POR QUÉ B1 SE ADELANTA Y EL RESTO NO

**Declarar una frontera es ESCRIBIR, no instrumentar.** Por eso no se pierde si el archivo se mueve
después: un documento que dice *"`tool_loop` espera a la API de Claude"* sigue siendo cierto aunque
el archivo se parta en tres.

⚠️ **Instrumentar sí se perdería.** Si la fase 2 parte `telegram_channel.py` (**4,570 líneas**), el
código de medición puesto antes se mueve con él — trabajo tirado.

⭐ **Y lo que B1 le da a las 3 fases de código:** al auditar `tool_loop.py`, **saber que espera a
Claude cambia el juicio sobre su lentitud**. Sin eso, se juzga como código lento algo que es una
espera externa.

🔬 **El caso real que lo justifica:** el único error del agente en 24h fue
`RuntimeError: sin github_token en el vault` — **una frontera que falló sin estar declarada**.

### 3.1 · Por qué B1 va primero aunque parezca lo más pequeño

**Sin fronteras declaradas, todo lo demás miente.** Si `tool_loop` tarda 8 segundos, ¿es lento el
bucle o está esperando a Claude? 🔬 **Medido hoy: el error real del agente fue una frontera** —
`sin github_token en el vault`— y llegó como un `RuntimeError` genérico.

⭐ **Una latencia sin saber qué frontera la causó no es una medida: es un número sin dueño.**

### 3.2 · La lista de TERMINADO — la regla de 5 pasos de TorchLean, traducida

Un archivo de For3s OS **no está aprobado** hasta que trae las cinco:

| # | Paso | Traducido a For3s OS |
|---|---|---|
| 1 | **Semántica** | ¿a qué nodo del grafo pertenece y qué edge implementa? |
| 2 | **Tipo** | su contrato de entrada/salida es explícito (ya al 100%: 76/76) |
| 3 | **Comportamiento** | mide su tiempo, o declara por qué no le aplica |
| 4 | **Verificación** | tiene una prueba **que se vio fallar** |
| 5 | **Frontera** | declara qué runtime externo usa y bajo qué supuesto |

⭐ **Los pasos 3 y 5 son los nuevos.** Los 1, 2 y 4 ya están en las fases 1-3 de la campaña.

---

## 4 · CÓMO SE VERÍA FALLAR

⛔ `principles/expertise/val-functional.md` §2.2: *un check debe verse fallar antes de que su verde
signifique algo.*

| Sub-fase | Sabotaje | Debe pasar |
|---|---|---|
| B1 | quitar el token del vault | el error **nombra la frontera**, no `RuntimeError` pelado |
| B1-bis | añadir una dependencia externa sin declararla | un check la caza |
| B2 | una etapa sin instrumentar | el desglose no suma el total → se ve el hueco |
| B3 | reportar promedio en vez de percentil | ⚠️ **hoy nada lo impide** — es el hueco que B3 cierra |
| B4 | el mismo motor da respuestas distintas por canal | se reporta la diferencia, **no se explica sola** |
| B5 | rebasar el presupuesto | el check falla, y **dice en qué etapa** |

---

## 5 · ⚠️ LO QUE PUEDE SALIR MAL — dicho antes

| Riesgo | Por qué es real |
|---|---|
| **Instrumentar cambia lo medido** | medir tiempo añade tiempo. ⚠️ Hay que verificar que el coste sea despreciable, como se hizo con la herencia de campaña: **+0.4 ms, +1.4%** |
| **Optimizar el número, no el sistema** | la lección de Self-Play. El juez sigue siendo *"Brian confía en delegarle"* |
| **`telegram_channel.py` es el archivo más grande y el más usado** | instrumentarlo toca la vía principal. ⛔ Solo en la instancia `brian` |
| **Los presupuestos sin dueño caducan** | un número objetivo que nadie revisa se vuelve decoración |

---

## 6 · LAS 3 DECISIONES — RESPONDIDAS por Brian (2026-08-11)

### 6.1 · Los presupuestos → ⭐ **MEDIR PRIMERO, poner el número después**

⛔ **No se inventan ahora.** Se corre una semana con B2-B3 instrumentado y **el número se pone
sabiendo dónde está el sistema**.

**Por qué esta y no la otra:** un presupuesto inventado se convierte en decoración —nadie lo revisa
porque nadie sabe si era razonable. Uno puesto con datos **ya nace defendible**.

⚠️ **Los números del paper NO se copian:** su caso es **voz en tiempo real**, donde un silencio de
3s rompe la conversación. Telegram no tiene ese problema. Sus cifras (primer token 5.90s P50 ·
9.00s P90) sirven de referencia de FORMA —tres etapas, dos percentiles— nunca de valor.

**Las tres que se medirán, y luego se fijan:**

| Etapa | Qué mide |
|---|---|
| **Primera señal** | desde el mensaje hasta el *"escribiendo…"* |
| **Respuesta simple** | sin herramientas ni memoria |
| **Respuesta con trabajo** | con memoria, grafo y herramientas |

### 6.2 · Las 18 tablas vacías → ⭐ **se investigan DENTRO de la fase 1**

🔬 **Verificado el 2026-08-11, y cambia el diagnóstico:** las 6 tablas vacías que se revisaron
**tienen código que las escribe**.

| Tabla | El archivo que la llena | Filas |
|---|---|---|
| `decisiones` | **`decisiones.py`** | **0** |
| `misiones` | **`expediente.py`** | **0** |
| `trace_events` | **`trace.py`** (432 líneas) | **0** |

⛔ **No sobran: NUNCA HAN CORRIDO.** Existe el código, existe la tabla, y nadie los ha unido.

⭐ **`decisiones` en cero es el diagnóstico del 13-jul, literal:** el sistema guarda **33,908
episodios** y **no ha escrito una sola decisión**. *"No devuelve valor"* no es que falte código —
es que **el código que devuelve valor nunca se ejecuta**.

**Tres explicaciones posibles, y se MIDE cuál es:**

| # | Explicación | Qué significaría |
|---|---|---|
| A | el código nunca se conecta | huérfano — **el patrón del decay de memoria**: `recalcular_relevance_lote()` existe y nadie la llama |
| B | se llama y falla en silencio | peor: parece funcionar y no funciona |
| C | es para un flujo que no ocurre | la capacidad existe para un caso que nunca pasa |

**Cómo entra sin trabajo extra:** cuando la fase 1 llegue a `decisiones.py`, `expediente.py` o
`trace.py`, la pregunta *"¿a qué nodo pertenece?"* se amplía con **"¿y alguien lo llama?"**.
⛔ **No se borra nada todavía:** `trace.py` puede ser una capacidad apagada, no basura, y For3s
TRACE se presentó en el Incubathon.

### 6.3 · El orden → ⭐ **la fase va PARTIDA** (ver §3.0)

**B1 antes de la fase 1** · **B2-B5 después de las tres**. La razón completa en §3.0: declarar una
frontera es escribir y no se pierde; instrumentar sí se perdería si el archivo se parte después.

---

Related: `campaigns/producto-for3s-os/CAMPAIGN.md` (la misión que esta fase sirve) ·
`rules/rule-product-authority.md` (por qué los papers no son autoridad) ·
`rules/qa-dimensions.md` (las 6 dimensiones que esta fase complementa) ·
`principles/expertise/val-functional.md` §2.2 (verse fallar antes de creerle) ·
`vision/Aprendizajes_De_Campo_Post_Incubathon.md` (el Frente D que esto mide).