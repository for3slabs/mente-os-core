# ARCHITECTURE · validators, quality, voice and hygiene

**Status:** current · **Type:** architecture · **Updated:** 2026-07-30 · **Owner:** brian
**Part of:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` (§12-TER … §12-SEPTIES) ·
**Block:** `blk-split-architecture-2026-07`

## Purpose

The five sections that answer *how the system enforces itself*: the validators, how a file is
guaranteed to be read, the quality verdict, the voice, and configuration hygiene.

Extracted verbatim on 2026-07-30 — 758 lines, the heaviest group in the document, and all five are
**grown sections** (`-TER`, `-QUATER`, `-QUINQUIES`, `-SEXIES`, `-SEPTIES`): the suffix itself was
the split signal (ADR-027).

⚠️ **Moved, not rewritten.**

---

## 1 · ⭐ LOS VALIDADORES — la respuesta al bloqueante A

> **LA DOCTRINA ES DOCUMENTO. LA VERIFICACIÓN ES SCRIPT.**

**El problema que resuelve.** La ley medida de este sistema:

| Forma de la regla | Cumplimiento medido |
|---|---|
| **Código** (gate de Puentes, permisos fail-closed) | ✅ **100%** |
| **Documento** (Método F, registro pre-`/clear`, índice) | 🔴 **falla 40-60%** |

**La solución no es llevar el criterio a código** — el criterio es de Brian y debe seguir siendo
legible y evolutivo. **La solución es llevar la VERIFICACIÓN a código.**

El script **no decide nada**. Solo comprueba **lo comprobable**:

```
   ¿existe el archivo?          ¿tiene los campos obligatorios?
   ¿cabe en su límite?          ¿el ID es único?
   ¿está obsoleto?              ¿las conexiones apuntan a bloques reales?
```

### Los 4 validadores

| Validador | Qué comprueba | Cuándo corre |
|---|---|---|
| **`revisar-bloques`** | archivos presentes · campos obligatorios · **límites de tamaño** · ID único · conexiones válidas | al abrir y al cerrar |
| **`generar-indice`** | 🤖 produce `docs/INDEX.md` y `docs/STATES.md` **desde los bloques reales** | tras cualquier cambio |
| **`avisar-obsoletos`** | detecta `estado.md` sin actualizar y bloques activos sin movimiento | periódico |
| **`verificar-suficiencia`** | ⭐ ¿las secciones **A-E** bastan para reiniciar? (§11.4) | al cerrar un bloque |
| **`grade-block`** | ⭐⭐ **dead code · duplication · tests · dependents · cycles** (§12-Q.4) | al cerrar · a demanda |
| **`check-health`** | ⭐⭐ **el SISTEMA se audita solo**: permisos contradictorios · índices que mienten · higiene · contexto (§12-T.3) | 🤖 **`SessionStart`, sin pedirlo** |

> ⭐ **Los validadores no solo verifican: COMPLETAN lo derivable** (§12-T.1) — pero nunca el criterio.
> Y cuando una puerta bloquea, se emite un **RECIBO DE APROBACIÓN** (§12-T.2).

### 12-T.1 · ⭐ VALIDADORES QUE COMPLETAN, no solo verifican *(incorporado 2026-07-27)*

**Origen:** referencia externa madura — su middleware *"compromete y abre el PR automáticamente **si
el agente no lo hizo**"*. No solo comprueba: **completa el paso omitido.**

**Por qué nos importa, medido:** la regla *"sin registro no hay `/clear`"* existe desde el 14-jul y
**se incumplió 5 de 11 veces**. Un validador que solo avisa habría avisado 5 veces… y seguiríamos
con 5 sesiones sin registrar.

| Situación | Validador que solo **verifica** | Validador que **completa** |
|---|---|---|
| `estado.md` sin actualizar al cerrar | 🔴 "falta actualizar" | ✅ **lo escribe** con lo que sabe · marca `auto:` |
| Índice desincronizado | 🔴 "el índice miente" | ✅ **lo regenera** |
| Bloque cerrado sin resumen | 🔴 "falta el resumen" | ✅ **redacta un borrador** para que Brian lo revise |
| Sub-bloque sin declarar dependientes | 🔴 "falta el grafo" | ✅ **lo calcula por grep** y lo propone |

**Regla dura de esta capacidad:**

> **Completar es para lo DERIVABLE, nunca para el criterio.**

| ✅ Se puede completar | ⛔ NUNCA se completa |
|---|---|
| el grafo de dependientes (se calcula) | los **límites qué SÍ / qué NO** (es alcance) |
| el índice y los estados (son derivados) | las **decisiones y su rationale** (es criterio) |
| el conteo de líneas, tests, duplicación | el **veredicto de calidad** (§12-QUINQUIES) |
| un borrador de resumen, marcado `auto:` | los **estándares obligatorios** del bloque |

> Todo lo autocompletado se marca **`auto:`** para que se distinga de lo que escribió una persona.
> **Un campo autocompletado que se hace pasar por decidido es peor que un campo vacío.**

### 12-T.2 · ⭐ RECIBO DE APROBACIÓN — cuando una puerta bloquea

**Origen:** referencia externa — *"superficies de aprobación compactas que muestran los cambios
propuestos **antes** de ejecutar"*.

**El hueco que cierra:** el v2 tiene 3 puertas que bloquean (§12-QUATER), pero **no tenía forma de
presentar el cambio para que Brian apruebe de un vistazo**. Bloquear sin dar salida es fricción.

```
🔴 PUERTA CERRADA · editar pieza con dependientes

  pieza:        lib/demo/userStore.ts
  propaga a:    session.ts · for3sChat.ts · admin.ts · route.ts · accountStore.ts
  bloque:       blq-demo-2026-07
  estándar:     Cerebro/REGLA_Fix_No_Parche.md

  lo que se quiere cambiar:
    → resolver la instancia real en vez de leer `kind` de la cookie

  evaluación de la construcción (§7):
    ✔ causa raíz identificada: `kind` se usa como si fuera la instancia
    ✔ los 6 sitios afectados están mapeados
    ✔ solución propuesta: un punto único que resuelvan los 6

  ┌──────────────────────────────────────────────┐
  │  [ APROBAR ]   [ VER LOS 6 SITIOS ]   [ NO ] │
  └──────────────────────────────────────────────┘
```

**Tres reglas del recibo:**
1. **Cabe en una pantalla.** Si no cabe, el cambio es demasiado grande y hay que partirlo.
2. **Muestra la propagación**, no solo el archivo — es lo que Brian no podía ver antes.
3. **Incluye la evaluación de la construcción** (§7): sin ella, la puerta no se abre.

> **El recibo convierte el bloqueo en una decisión informada de 10 segundos**, en vez de un muro.

### 12-T.3 · ⭐⭐ `check-health` — EL SISTEMA SE AUDITA SOLO

> **Brian, 2026-07-27:** *"el usuario no te debe decir 'oye, realiza esta conexión' o 'limpia la
> basura' — es algo que ya deberíamos estar automatizando."*

**La regla que sale de ahí:**

> ## Si hay que PEDIRLO, no está automatizado.

#### El problema que resuelve — tres fallos con la misma causa

| Fallo | Cuánto llevaba así | ¿Quién lo encontró? |
|---|---|---|
| `additionalDirectories` daba acceso a NavigoX, contradiciendo el gate | **semanas** | Brian, preguntando |
| `Maestro/registro.md` decía 173 docs / 4.5 MB · realidad 195 / 17 MB | desde el 17-jul | Brian, preguntando |
| 999 archivos de `file-history` >30 días · `cleanupPeriodDays` sin fijar | meses | Brian, preguntando |

> **Los tres son el mismo fallo: nada vigila el estado del sistema.**
> El v2 tenía validadores para los **bloques** y ninguno para **su propia salud**.

#### Qué comprueba

```
bin/check-health

  🔴 PERMISSIONS
     · additionalDirectories contradicting a deny rule      ← the NavigoX hole
     · allow entries pointing at paths that no longer exist
     · deny missing for any gated branch in pointers.tsv

  🔴 TRUTH
     · registro.md figures vs measured reality
     · docs/INDEX.md older than the blocks it indexes
     · pointers.tsv rows whose index file does not exist

  🟡 HYGIENE
     · file-history entries older than cleanupPeriodDays
     · empty directories
     · cleanupPeriodDays not set
     · files over their declared size limit (§3.2-bis)

  🟡 SESSION
     · live context over 200K / 500K  ← the 21-jul threshold
     · session open longer than 48h
     · repeated "Connection closed mid-response"
```

#### Las reglas del validador

**① No arregla nada — REPORTA.** Misma doctrina que `grade-block`: *la doctrina es documento, la
verificación es script*. Excepción: lo **derivable** puede completarse (§12-T.1), marcado `auto:`.

**② Corre SOLO, en el hook `SessionStart`.** No se invoca. Aparece al arrancar.
> ⚠️ **Debe ser barato** (<1s) o se vuelve fricción en cada arranque y alguien lo desactiva.

**③ ⛔ NUNCA borra evidencia forense.** Los `.jsonl` de sesión **no se tocan**: de ahí salió el
incidente del 21-jul que no estaba documentado en ningún sitio. **Reporta el peso, no lo limpia.**

**④ Silencio cuando todo está bien.** Si no hay hallazgos, no imprime nada. Un validador que habla
siempre se ignora siempre.

#### Precedente real — la limpieza del 2026-07-27

Primera pasada manual, para calibrar qué debe detectar:

| Encontrado | Acción |
|---|---|
| 999 archivos de `file-history` >30 días (~19 MB) | ✅ borrados |
| `cache/changelog.md` del 04-mayo (268 KB) | ✅ borrado |
| `paste-cache/` vacía | ✅ borrada |
| `.claude/` total | **464 MB → 442 MB** |
| `projects/*.jsonl` (371 MB) | ⛔ **NO se tocó — evidencia forense** |
| `get-shit-done/` (3.1 MB, sin tocar desde mayo) | ⛔ **NO se tocó — dependencia de 9 hooks** |

> **Lo que esta pasada enseñó:** *"sin tocar desde mayo"* **no significa basura.** `get-shit-done/`
> lleva meses quieto y alimenta los 9 hooks activos. **El criterio no es la fecha: es si algo depende
> de ello.** El validador debe distinguir *viejo* de *huérfano*.

### Qué NO hacen los validadores

- **No** juzgan si el código es bueno → eso es el Encargado 2.
- **No** deciden el carril → eso lo decide la propagación (§5).
- **No** aprueban ni rechazan trabajo → eso es de Brian.
- **No** completan nada que sea criterio, alcance o veredicto → solo lo **derivable** (§12-T.1).

> **Su único poder es negarse a dejar cerrar un bloque mal formado.** Con eso basta: es la diferencia
> entre una regla que se cumple y una que se olvida.

### El índice que no puede mentir

**Hoy:** `memory/archive/README.md` inventaría **35 de 188 documentos** — regla incumplida ~150 veces, y lista
"R2-R10 pendientes" cuando están todas LOCKED.

**En el v2:** `docs/INDEX.md` y `docs/STATES.md` se **generan**. Incluyen por bloque:
nombre · estado · fase · dueño · **salud** · ruta · última actualización.

> Es el mismo criterio que Brian ya aplicó en `Maestro/punteros.tsv` — *"aquí NO se duplica la tabla:
> la sincronía a mano murió"*. **Ese criterio ya existe en el sistema; aquí solo se extiende.**

---

### 12.0-BIS · ⭐ EL DIAGRAMA ILUSTRA — `piezas.tsv` DEFINE *(corregido 2026-07-30)*

> **Brian:** *"¿podemos hacer un sistema de apuntado para no duplicación?"* — sí, y ya existía:
> `Maestro/punteros.tsv` declara en su cabecera *"registro.md la REFERENCIA (no la duplica)"*.
> `piezas.tsv` extiende ese mismo criterio a las piezas del sistema.

**El diagrama de arriba describía dos archivos en `Tickets/` que nunca se mudaron ahí.** No fue
descuido: **medido 2026-07-30, 11 documentos declaraban dónde viven esos 2 archivos, con 29
menciones.** Mover uno obligaba a corregir 29 lugares a mano. Nadie lo hace, y el diagrama miente.

| | |
|---|---|
| ⭐ **La verdad** | `piezas.tsv` — 17 piezas: ruta · dueño · clase · qué es |
| **Este diagrama** | ilustra la forma. **No define rutas** |
| **Quién lo verifica** | 🤖 `bin/check-structure` la lee; `bin/test-f0-f6` prueba que mover un archivo + actualizar UNA línea basta |

**Por qué el gate NO se mudó a `Tickets/`:** `Maestro/punteros.tsv` lo leen `maestro`, `Maestro/maestro_lib.sh` e
`Maestro/indexador.py` — sacarlo de `Maestro/` rompe 3 consumidores para ganar simetría en un dibujo.
Y `Tickets/` guarda otra cosa: 6 tickets de H1-H4 del 17-jul.

> ⭐ **La regla:** cuando el diseño y la realidad no coinciden, **gana la realidad** — y se corrige
> el documento. Un diagrama que describe lo que no existe es la misma clase de mentira que
> `Maestro/registro.md` afirmando 173 documentos cuando había 257.

---

## 2 · ⭐⭐ CÓMO SE GARANTIZA QUE UN ARCHIVO SE LEA

> **La pregunta de Brian (2026-07-27):** *"¿cómo sabe que realmente ese es el carril o el archivo
> que tiene que leer, sin omitir? Porque si no, va a pasar lo del Método F, que nunca se leyó
> aunque se puso."*

**Es la pregunta que decide si el v2 funciona o repite el fracaso.**

### El problema, con precisión

Hay **tres cosas distintas** que se confunden:

| | Qué es | ¿Se cumple hoy? |
|---|---|---|
| **Existir** | el archivo está escrito | ✅ el Método F existe desde 04-jul |
| **Ser encontrable** | se sabe que existe y dónde | ✅ `CLAUDE.md` lo menciona |
| **SER LEÍDO** | **entra en contexto en el momento correcto** | 🔴 **falló en 2 de 5 sesiones** |

**El Método F cumplía las dos primeras y falló la tercera.**

> ⚠️ **Lo que lo hace invisible:** la IA **no sabe lo que no leyó**. Sin abrir el estándar no siente
> que le falte nada — trabaja con lo que tiene y **suena igual de segura**. Es el mismo mecanismo de
> la degradación del 21-jul.

### Por qué las soluciones obvias no bastan

| Intento | Qué pasa |
|---|---|
| *"que CLAUDE.md diga que hay que leerlo"* | **ya lo dice. Falló.** |
| *"meter los estándares en CLAUDE.md"* | ~15 archivos → el arranque pasa de 38K a cientos de miles de tokens. **Reproduce el problema de consumo del 9-jul** |

> **El conflicto de fondo:** lo que se **inyecta** se cumple (100%) pero cuesta tokens siempre;
> lo que se lee **a demanda** es barato pero depende del criterio de la IA (falla 40-60%).
> **Ninguna sirve sola.**

### La solución: 4 CAPAS ✅ *(aprobado por Brian 2026-07-27)*

Cada capa cubre el fallo de la anterior:

```
   ┌─────────────────────────────────────────────────────────────┐
   │ A · ENRUTADOR en CLAUDE.md            ~15 líneas · siempre  │
   │   "si tocas backend → carga expertise/dev-backend.md ANTES"     │
   │   ✔ barato · ✔ siempre presente · ✘ aún depende de la IA    │
   └───────────────────────────┬─────────────────────────────────┘
                               ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ B · EL BLOQUE DECLARA sus estándares   §D del BLOQUE.md     │
   │   el estándar viaja CON el trabajo, no en un índice general │
   │   ✔ específico del trabajo · ✘ lo escribe quien abre        │
   └───────────────────────────┬─────────────────────────────────┘
                               ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ D · HOOK del harness       ANTES de editar un archivo       │
   │   detecta el tipo de trabajo → INYECTA el estándar          │
   │   o BLOQUEA la acción                                       │
   │   ⭐ ÚNICA capa que NO depende del criterio de la IA         │
   └───────────────────────────┬─────────────────────────────────┘
                               ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ C · VALIDADOR al cerrar    red de seguridad                 │
   │   sin rastro de que se aplicó el estándar → no cierra       │
   │   ✔ verificable · ✘ llega tarde (el código ya está escrito) │
   └─────────────────────────────────────────────────────────────┘
```

**Sobre la portabilidad:** el hook (D) es **aceleración, no fundamento**. Con otra IA sin hooks
quedan A + B + C y el sistema **sigue funcionando** — con menos garantía. *El protocolo es portátil;
el hook es el turbo cuando existe.*

### ⭐ LAS 3 PUERTAS CERRADAS ✅ *(decidido con Brian)*

El hook tiene **tres respuestas**:

| | Qué hace | Cuándo |
|---|---|---|
| 🟢 **PASAR** | nada, sigo | cambio trivial |
| 🟡 **AVISAR** | **inyecta el estándar** en contexto y lo registra · sigo trabajando | la mayoría de los casos |
| 🔴 **BLOQUEAR** | **la acción NO se ejecuta** hasta cumplir algo | solo 3 casos |

**Solo se bloquean tres acciones, cada una con su razón medida:**

| Acción bloqueada | Por qué | Evidencia |
|---|---|---|
| **Editar una pieza con dependientes declarados** | es el mecanismo exacto del fix-sobre-fix | `userStore.ts` ×21 · **42%** de commits = fixes |
| **Tocar la base de datos** | propaga a todo lo que lee la tabla y no se ve venir | Brian: *"si no tenemos control estamos mal"* |
| **Cerrar un bloque sin pasar suficiencia** | la próxima sesión arrancaría ciega **sin saberlo** | *"no, así no iba"* · 5/11 sesiones sin registrar |

**Ejemplo real de bloqueo:**

```
Intento:   Edit lib/demo/userStore.ts
             ↓
Hook:      ¿esta pieza tiene dependientes declarados? → SÍ, 5
             ↓
🔴 BLOQUEADO
   "userStore.ts propaga a: session.ts · for3sChat.ts · admin.ts ·
    route.ts · accountStore.ts
    Antes de editar: evalúa la construcción completa (§7 fix ≠ parche).
    Si ya lo hiciste, declara el alcance en el bloque."
```

> **Sin el bloqueo, eso mismo fue:** edito un archivo → funciona → cierro → y 4 commits después
> *"barrido completo del patrón"*. **Los 21 toques a `userStore.ts` empezaron exactamente así.**

**Por qué solo tres:** es la lógica del gate de Puentes — **protege UNA sola cosa y por eso se cumple
el 100% de las veces**. Si se bloquean veinte cosas, el sistema estorba, se desactiva, y volvemos al
inicio. **Pocas puertas cerradas, bien elegidas.**

> **Bloquear no es prohibir:** es *"para aquí, haz esto primero, y sigue"*. Brian siempre puede
> ordenar que se pase igual.

---

## 3 · ⭐⭐⭐ EL VEREDICTO DE CALIDAD — QA dentro de Mente OS

> **El dolor que resuelve (Brian, 2026-07-27):** *"en la demo, ANTES del clear me dijo 'todo está
> perfecto, me encantó'. Le di clear y me dijo 'sí está bien lo que se hizo, mejoró, pero aún sigue
> roto'. Y en mi cabeza estoy pensando: ¿me mientes o qué está pasando? **Ese dolor es el que más
> me impide trabajar en estos momentos.** Ya no es ver si funciona, es ver si lo que está escrito
> es un producto o es un MVP hecho para que funcione, hecho por IA."*

### 12-Q.1 · La evidencia — está medida, no es una impresión

| Momento | Lo que dije |
|---|---|
| 24-jul 21:15 · sesión 1, inicio | *"el sistema **está completo**"* |
| 26-jul 06:24 · sesión 1, cierre | *"tiene el estado completo para retomar **sin perder nada**"* |
| **26-jul 06:33 · sesión 2, tras `/clear`** | *"lo que está mal es que este archivo **lo implementa a medias**"* |
| 26-jul 23:59 · sesión 2, cierre | *"🔴 **lo que sigue siendo de MVP**"* |

> **9 minutos separan "completo, sin perder nada" de "lo implementa a medias".**
> Lo único que ocurrió entre medias fue un `/clear`.

### 12-Q.2 · Por qué pasa — no es mentira, es que el juicio no valía nada

**Los dos juicios eran sinceros. Ninguno era fiable.** Tres sesgos lo explican:

| Sesgo | Qué ocurre |
|---|---|
| **Esfuerzo reciente** | acabo de arreglar 5 cosas → mi contexto dice "arreglé, arreglé" → concluyo "está bien". **Medí cuánto trabajé, no cómo quedó** |
| **Solo veo lo que toqué** | toqué 6 de 40 archivos → mi juicio cubre 6. Digo "está completo" queriendo decir "**lo que toqué** está completo" |
| **Tras el `/clear` desaparece el sesgo** | leo el archivo sin recordar que costó 21 commits → veo lo que vería un tercero |

> ⭐ **Ese "tercero" es el juicio correcto. El problema es que hoy solo aparece por accidente,
> después de un `/clear`.**

**Y la conexión que Brian identificó:** *"¿está todo conectado?"* y *"¿lo que dices está bien, está
bien?"* **son la misma pregunta.** Ambas piden un juicio que **no dependa de quién lo emite ni de
cuándo**. Hoy el veredicto es una opinión, y una opinión que cambia con el contexto **no es un
veredicto: es un estado de ánimo**.

### 12-Q.3 · LA REGLA MADRE DE ESTA SECCIÓN

> ## 🚫 La IA NO declara "está bien". La IA REPORTA LA MEDICIÓN.

Un bloque no se cierra con un adjetivo. Se cierra con **una calificación reproducible**.

### 12-Q.4 · CAPA 1 — QA MEDIBLE (script · sin criterio humano)

Lo que un script puede comprobar sin opinar:

| Métrica | Qué detecta | Ataca |
|---|---|---|
| **Archivos sin consumidor** | nadie los importa | ⭐ **código muerto** |
| **Exports nunca importados** | función escrita y jamás usada | ⭐ *"lo dejé por si acaso"* |
| **Bloques de código duplicados** | la misma lógica en 2+ sitios | ⭐ **redundancia** |
| **Archivos tocados sin test** | cambio sin red | *"solo funciona lo indispensable"* |
| **Dependientes no declarados** | el bloque miente sobre su grafo | fix-sobre-fix |
| **Ciclos de importación** | arquitectura enredada | deuda estructural |
| **Cobertura de caminos críticos** | los 5 flujos que importan | los tapones de la demo |

**Salida — el mismo resultado antes y después del `/clear`:**

```
BLOQUE DEMO — calificación medida · 2026-07-27
  archivos sin consumidor (código muerto):        3  🔴
  exports nunca importados:                       7  🔴
  bloques duplicados (≥8 líneas):                 2  🟡
  archivos tocados sin test:                      8  🔴
  dependientes no declarados en el bloque:        1  🔴
  ciclos de importación:                          0  🟢
  cobertura de caminos críticos:                0/5  🔴
  ──────────────────────────────────────────────────
  VEREDICTO MEDIBLE: 🔴 MVP — no es producto
```

**Tres propiedades que lo cambian todo:**
1. **No depende del contexto** → mismo comando, mismo resultado. **Aquí muere la contradicción.**
2. **Cubre TODO el bloque**, no solo lo que se tocó (los 40 archivos, no los 6).
3. **Brian puede reproducirlo** → no hay que creerle a la IA: se corre y se ve.

### 12-Q.5 · ⭐⭐ CAPA 2 — QA DE CRITERIO (la revisión del senior)

> **Brian, 2026-07-27:** *"esto lo necesito, le diste al clavo. Que la arquitectura es correcta, si
> el diseño de datos es bueno, si la abstracción es la adecuada, si el nombre es claro. **Porque así
> v2 se diferencia**: no cumplimos con solo lo que nos dijo la IA, cumplimos porque sabemos qué
> requerimientos necesitas. **Tenemos QA como uno de los elementos internos de Mente OS y eso vale
> oro.** Que no sea 'me lo dio la IA y no sé', sino que **se sienta hecho por un senior de 50 años
> de experiencia**."*

**Esto es lo que diferencia al v2.** Lo medible lo tiene cualquier linter. **Lo que ningún linter
tiene es el criterio de un senior — y ese criterio es lo que Brian aporta y el sistema aplica.**

#### Cómo se convierte criterio en algo verificable

Un criterio suelto (*"la arquitectura debe ser correcta"*) **no sirve** — es tan vago como "está
bien". Cada criterio se declara con **3 partes**:

| Parte | Para qué |
|---|---|
| **La pregunta** | qué se juzga, en una frase concreta |
| **La evidencia exigida** | 🔴 **qué hay que MOSTRAR** para responder — no basta afirmar |
| **El fallo típico** | cómo se ve cuando está mal (viene de casos reales) |

> ⭐ **La evidencia es lo que impide que la IA se autoapruebe.** No se puede responder "sí, la
> arquitectura es correcta": hay que **mostrar el árbol de dependencias**. La respuesta sin
> evidencia **no cuenta**.

#### Las 6 dimensiones de criterio

| # | Dimensión | La pregunta | Evidencia exigida |
|---|---|---|---|
| **1** | **Arquitectura** | ¿cada pieza tiene una sola responsabilidad y está en la capa correcta? | el árbol de dependencias + señalar qué pieza haría fallar a cuántas |
| **2** | **Diseño de datos** | ¿el esquema representa el dominio? ¿normalizado? ¿los estados imposibles son imposibles? | el esquema real + un caso que el modelo NO puede representar mal |
| **3** | **Abstracción** | ¿está al nivel correcto — ni copiada 3 veces ni generalizada de más? | los sitios donde se repite, o los usos reales de la abstracción |
| **4** | **Nombres** | ¿el nombre dice lo que hace, sin leer el cuerpo? | 3 nombres del bloque explicados sin abrir el archivo |
| **5** | **Contratos** | ¿las interfaces entre piezas están declaradas? ¿los errores son parte del contrato? | la firma real + qué pasa cuando falla |
| **6** | **Necesidad** | 🔴 ¿**cada archivo que existe TIENE que existir**? | por cada archivo nuevo: quién lo consume y por qué no podía vivir en otro sitio |

> **La dimensión 6 es la respuesta directa a Brian:** *"que lo que está es necesario, y no se lo
> inventó, o lo quiso mover, o dijo 'ah, lo dejo aquí por si lo necesitamos'"*.

#### Salida de la capa 2

```
BLOQUE DEMO — revisión de criterio · 2026-07-27
  1 arquitectura ... 🟡  userStore concentra 5 responsabilidades
                         evidencia: árbol adjunto · 5 módulos dependen de él
  2 datos ......... 🟢  esquema normalizado, 7 FKs, sin estados imposibles
                         evidencia: schema.sql + caso "invitado sin dueño" imposible
  3 abstracción ... 🔴  "resolver instancia" copiado en 6 sitios
                         evidencia: rutas de las 6 copias
  4 nombres ....... 🟡  `kind` no dice qué distingue
                         evidencia: 3 nombres explicados; `kind` requiere leer el cuerpo
  5 contratos ..... 🔴  4 funciones sin declarar qué pasa al fallar
                         evidencia: firmas sin tipo de error
  6 necesidad ..... 🔴  accountStore.ts: 0 consumidores tras la migración
                         evidencia: grep sin resultados
  ──────────────────────────────────────────────────────────────
  VEREDICTO DE CRITERIO: 🔴 no pasa — 3 dimensiones en rojo
```

#### De dónde sale el criterio

| Quién | Qué aporta |
|---|---|
| **Brian** | ⭐ **el criterio** — qué exige un senior en backend, frontend y BD (`Alma/expertise/*`) |
| **La IA** | aplicar ese criterio y **traer la evidencia**, no emitir opinión propia |

> **Es la misma regla de §9.1: la IA no inventa criterio.** Aquí además **no puede autoaprobarse**,
> porque cada respuesta exige evidencia mostrable.

### 12-Q.6 · EL VEREDICTO FINAL DEL BLOQUE

```
   ┌──────────────────────────────────────────────┐
   │ CAPA 1 · MEDIBLE   (script)                  │
   │ código muerto · duplicación · tests · grafo  │
   └───────────────────┬──────────────────────────┘
                       ▼
   ┌──────────────────────────────────────────────┐
   │ CAPA 2 · CRITERIO  (6 dimensiones + prueba)  │
   │ arquitectura · datos · abstracción · nombres │
   │ contratos · NECESIDAD                        │
   └───────────────────┬──────────────────────────┘
                       ▼
        ┌────────────────────────────────┐
        │ 🟢 PRODUCTO   · ambas en verde │
        │ 🟡 CASI       · sin rojos      │
        │ 🔴 MVP        · algún rojo     │
        └────────────────────────────────┘
```

**Reglas de cierre:**
- El veredicto se **escribe en el bloque con fecha** (campo `calificación`).
- 🔴 en cualquier capa → **el bloque no se cierra como producto**. Puede cerrarse marcado
  explícitamente como **MVP**, con la deuda listada — *lo que no se puede es cerrarlo diciendo
  "está bien"*.
- **La comparación entre veredictos** (hoy vs el anterior) responde *"¿mejoramos o empeoramos?"*
  con números, no con impresiones.

> ⭐ **Lo que esto le da a Brian:** ya no *"me lo dijo la IA y no sé"*. Es **QA como elemento interno
> de Mente OS**: requisitos declarados por él, verificados con evidencia, reproducibles. **Se siente
> hecho por un senior porque el criterio ES de un senior — el sistema solo garantiza que se aplique
> siempre, y no solo cuando la IA se acuerda.**

---

## 4 · ⭐⭐ LA VOZ — cómo se comunica Mente OS

> **Brian, 2026-07-27:** *"necesito tenerlo, porque debe existir esa diferencia, ocupando Mente OS."*
>
> **El principio:** si Mente OS gobierna **cómo se construye**, también debe gobernar
> **cómo se comunica**. Un sistema que produce código de senior y lo explica como un folleto
> genérico está a medias.

### 12-S.1 · El hallazgo — no hay nada configurado

Medido en este entorno (2026-07-27):

| Capa | Estado |
|---|---|
| `CLAUDE.md` del proyecto | 🔴 **cero reglas de tono o estilo** — solo arranque, scope, seguridad |
| `~/.claude/output-styles/` | 🔴 **la carpeta no existe** |
| `.claude/settings.json` (proyecto y global) | 🔴 sin `outputStyle` |
| Hooks activos en el entorno | ✅ **9 hooks funcionando** (sistema externo) |

> **Conclusión:** *"se siente hecho por IA"* **no viene de un archivo mal configurado. Viene de que
> nadie escribió el archivo.** Se estaba recibiendo el comportamiento por defecto, sin ninguna
> instrucción de forma.
>
> ✅ **Y el mecanismo está probado:** ya hay 9 hooks corriendo en este entorno. La capa D de
> §12-QUATER no es una hipótesis — es algo que aquí ya funciona.

### 12-S.2 · Dónde vive la voz

| Archivo | Alcance | Precedencia |
|---|---|---|
| `~/.claude/output-styles/for3s.md` | **todos** los proyectos de Brian | reemplaza parte del prompt de sistema |
| `principles/owner-0-voice.md` | **este** Mente OS | se inyecta vía `CLAUDE.md` |
| `.claude/settings.json` → `"outputStyle": "for3s"` | activa el estilo global | — |

> ⚠️ **Nota de portabilidad:** `output-styles` es específico de Claude Code. Por eso **el contenido
> canónico vive en `principles/owner-0-voice.md`** (portátil, cualquier IA lo lee) y el `output-style`
> es solo **el vehículo** que lo aplica aquí. Mismo criterio que los hooks: *aceleración, no fundamento*.

### 12-S.3 · ⭐ El contenido — reglas NEGATIVAS y verificables

**La lección de diseño:** *"sé claro y directo"* **no cambia nada** — es exactamente el tipo de
instrucción vaga que produce el problema. **Lo que funciona son prohibiciones concretas.**

| # | Regla | Qué elimina |
|---|---|---|
| 1 | **No abrir validando** (*"excelente pregunta"*, *"tienes toda la razón"*). Ir al contenido | apertura de relleno |
| 2 | **Comprometerse con UNA recomendación.** Si hay opciones, elegir y decir por qué. Prohibido *"depende"* sin resolver | el hedging que no decide |
| 3 | **Decir "no lo sé"** en vez de generalizar | seguridad falsa |
| 4 | **Viñetas solo si hay lista real.** No 3 puntos por costumbre | estructura decorativa |
| 5 | **No cerrar repitiendo** lo ya dicho | el párrafo-resumen inútil |
| 6 | **Prohibido:** *"es importante destacar"*, *"cabe mencionar"*, *"en resumen"*, *"profundizar"* | muletillas delatoras |
| 7 | ⭐ **Afirmación de hecho sin verificar = prohibida.** Se mide, o se dice que no se midió | 🔴 **la más importante** |
| 8 | **Omitir lo que no importa.** Cubrir el ángulo que importa, no todos | el exceso que delata |

> ⭐ **La regla 7 es la misma del veredicto de calidad (§12-Q.3):**
> **la IA no declara — reporta la medición.** Aplicada al texto en vez de al código.
>
> Por eso la voz **no es cosmética**: es la misma doctrina de evidencia, en otra superficie.

### 12-S.4 · Por qué es la misma enfermedad que el código

Brian usó **la misma frase** para las dos cosas: *"se siente hecho por IA"*.

| Texto hecho por IA | Código hecho por IA |
|---|---|
| dice mucho, decide nada | funciona, no está bien hecho |
| tres viñetas por costumbre | archivos donde cayeron |
| repite en vez de profundizar | lógica repetida en 6 sitios |
| suena seguro sin serlo | *"está completo"* → *"a medias"* |
| formato en lugar de criterio | patrón en lugar de arquitectura |

> **Causa común: producir la forma correcta sin el juicio detrás.**
> Y el antídoto es el mismo en ambos casos: **que haya algo verificable detrás de cada afirmación.**

### 12-S.5 · Por qué es el ENCARGADO 0 y no un cuarto encargado

Los encargados son **tres y no pueden ser más** (regla de Brian). La voz **no es un cuarto**:
es **transversal** — gobierna cómo los tres se comunican, no qué hacen.

```
        ┌──────── ENCARGADO 0 · LA VOZ ────────┐
        │  (transversal — no es un cuarto)     │
        └──┬─────────────┬─────────────┬───────┘
           ▼             ▼             ▼
      ① documentación ② desarrollo ③ validación
```

Por eso se numera **0**: precede a los tres y no compite con ellos.

---

## 5 · ⭐⭐⭐ HIGIENE DE CONFIGURACIÓN — las 4 reglas

> **El patrón común de los 3 fallos del 2026-07-27:** en los tres la regla existía o era obvia.
> **Lo que faltaba era el mecanismo.** Misma historia que el Método F.

| Fallo medido | La convención existía | Faltaba |
|---|---|---|
| Password **331 veces** en `settings.local.json` | `secrets/` era el sitio correcto | **nada obligó a referenciarlo** |
| **689 rutas absolutas** `/home/brianweb3/` | — | **nada exigió portabilidad** |
| `additionalDirectories` daba acceso a NavigoX | el gate lo prohibía | **nada pidió justificar la ruta** |

---

### 12-S.1 · REGLA 1 — Los secretos se REFERENCIAN, nunca se pegan

```
⛔  sshpass -p '<LA-CONTRASEÑA-REAL>' ssh brianweb3@for3s
✅  sshpass -p "$FOR3S_SSH_PASS" ssh brianweb3@for3s
```

**Por qué es una regla y no un consejo:** al aprobar un comando, Claude Code **lo archiva literal**
como permiso permanente. Un secreto pegado en un comando aprobado **queda grabado para siempre**.
Medido: **331 entradas** con la contraseña del servidor, en un archivo **sin `.gitignore`**.

| Dónde vive un secreto | Estado |
|---|---|
| `secrets/` (antes `secrets/`) | ✅ ignorado por git |
| Variable de entorno | ✅ nunca en disco |
| **Un comando aprobado** | 🔴 **prohibido** |
| **Un archivo de settings** | 🔴 **prohibido** |

> ⚠️ **Purgar no invalida.** El secreto purgado el 27-jul **sigue en el `.jsonl` de la sesión**
> (los transcripts no se editan). **Todo secreto que se filtró se ROTA, no solo se borra.**

---

### 12-S.2 · REGLA 2 — Toda ruta declara su POR QUÉ

> **Brian:** *"cuando cargue una nueva ruta debe tener un por qué en especial, no solo por cargar."*

**Ninguna ruta entra sin justificación.** Formato obligatorio:

```jsonc
"additionalDirectories": [
  // 2026-07-27 · el proyecto entero · trabajo diario
  "$CLAUDE_PROJECT_DIR"
]
```

**Estado medido de las 9 entradas actuales — ninguna tenía justificación:**

| Entrada | Veredicto |
|---|---|
| `/tmp/h2` | 🔴 **no existe** |
| `.../2a5131d3/scratchpad` | 🔴 **no existe** — sesión muerta el 13-jul |
| `.../repo-backend/__pycache__` | 🔴 **no existe** + contradecía el gate |
| `5M-incubathon` | 🔴 **contradecía el gate de NavigoX** |
| `for3s/Mente/Cuerpo` · `Mente/Doc` · `marca-personal/*` ×2 | 🟡 **4 entradas, misma raíz** |
| `/tmp` | ✅ legítima |

---

### 12-S.3 · ⭐⭐ REGLA 3 — UN MECANISMO, UNA ENTRADA

> **Brian:** *"que las rutas no se creen por crear... aunque se ocupen para otras cosas eso no
> importa, es el mismo mecanismo. **No buscamos volumen, buscamos claridad y certeza.**"*

#### La prueba que decide si una entrada merece existir

> ## ¿Esta entrada autoriza algo que NINGUNA otra ya autoriza?
> Si no → **no entra.**

#### Tres criterios, todos verificables por script

| # | Criterio | Ejemplo medido |
|---|---|---|
| 1 | **Sin solapamiento** — si A contiene a B, B no entra | `/tmp` ya contenía `/tmp/h2` · `5M-incubathon` ya contenía su `__pycache__` |
| 2 | **Sin rutas muertas** — la ruta existe o se borra | **3 de 9** no existían |
| 3 | **Una entrada por MECANISMO, no por invocación** | **234** entradas `Bash(sshpass...)` para un solo mecanismo |

#### La evidencia de por qué esta regla existe

**Los 1,010 permisos agrupados por mecanismo:**

| Patrón | Entradas | Debería ser |
|---|---|---|
| `Bash(sshpass...)` | **234** | 1 |
| `Bash(curl...)` | **139** | 1-2 |
| `Bash(python3...)` | **101** | 1 |
| `Bash(awk...)` · `grep` · `node` | 161 | 3 |

> **234 entradas para "usar sshpass" no es una lista de permisos: es un registro de cada vez que se
> dijo sí.** El mecanismo es uno; las entradas son 234.
>
> **La granularidad correcta es el MECANISMO, no el comando.** `Bash(sshpass *)`, no 234 variantes.

**Con esta regla: las 9 rutas serían 2 · los 1,010 permisos serían ~30.**

---

### 12-S.4 · REGLA 4 — Rutas portables

**Medido:** 689 rutas `/home/brianweb3/` en `settings.local.json` · **9 de 9 hooks** con ruta
absoluta. **Nadie más puede usar esto.**

| ⛔ No portable | ✅ Portable |
|---|---|
| `/home/brianweb3/for3s/Mente` | `$CLAUDE_PROJECT_DIR/Mente` |
| `/home/brianweb3/.claude/hooks/x.js` | `$HOME/.claude/hooks/x.js` |

> ⚠️ **Excepción honesta:** los 9 hooks son de un sistema externo (GSD) con rutas absolutas propias.
> **Se documentan como no portables** en vez de fingir que se arreglan. Un límite declarado es
> ingeniería; un límite oculto es deuda.

---

### 12-S.5 · Lo que `check-health` añade por estas reglas

```
🔴 SECRETS
   · secret-looking values inside settings files
   · secrets pasted into approved commands
   · a secret present in both secrets/ and anywhere else

🔴 PORTABILITY
   · absolute paths tied to one machine
   · additionalDirectories entries with no declared reason

🔴 REDUNDANCY                                    ← regla 3
   · overlapping paths (A contains B)
   · dead paths (target does not exist)
   · N allow entries collapsible into one mechanism
```

> **Los tres fallos del 27-jul habrían salido en el primer arranque.** Vivieron semanas porque
> nada mira.

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (entry point) ·
`docs/architecture/block-anatomy.md` · `bin/check-blocks` · `bin/grade-block` ·
`bin/check-health` · `principles/owner-0-voice.md` · ⭐ **`rules/rule-config-hygiene.md`** (§12-S
lives there as an enforceable rule — this section is its origin, not its home).
