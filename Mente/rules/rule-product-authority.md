# RULE · PRODUCT AUTHORITY — quién manda al verificar For3s OS
**Status:** current · **Type:** rule · **Updated:** 2026-08-12 · **Owner:** brian
**Language:** español (documento de INSTANCIA — describe el producto de Brian, no el motor)
**Applies to:** todo trabajo sobre `for3slabs/for3s` (For3s OS), en el servidor o en un clon
**Verified by:** `bin/test-f0-f6`
---

## Purpose

**Cuando se verifica o construye For3s OS, `Cerebro/` es la autoridad — y dentro de él,
`Cerebro/For3s_OS_Grafo_Maestro.md` manda sobre cómo funciona el sistema.**

> **Brian, 2026-08-10:** *"Para la construcción y verificación de For3s OS vamos a tomar dentro de
> Mente OS el Cerebro como fuente mayor de verdad. No significa que sea solo eso, sino que le tomes
> más importancia en algunas cosas, en especial a For3s OS Grafo Maestro y cómo es que funciona."*

⛔ **No es exclusividad, es PRECEDENCIA.** Los demás documentos siguen valiendo; lo que cambia es
quién gana cuando dos se contradicen.

---

## 1 · EL ORDEN DE PRECEDENCIA — al juzgar el PRODUCTO

| # | Autoridad | Qué decide |
|---|---|---|
| **1** | `Cerebro/For3s_OS_Grafo_Maestro.md` | ⭐ **CÓMO FUNCIONA**: los 11 nodos, los 24 edges, los 3 pilares, las reglas de autonomía y los límites duros |
| **2** | Las rondas técnicas (`work/Ronda_*`) | **CON QUÉ se construye** — el propio grafo cede aquí (§0: *"donde una tecnología difiera de lo lockeado en una ronda, MANDA LA RONDA"*) |
| **3** | El resto de `Cerebro/` | el marco: `Arquitectura_Grafo_vs_Loop` · `Mapeo_Nodo_Cerebral_Tabla_SQL` · los acercamientos |
| **4** | `vision/` | el PARA QUÉ y el mercado — no decide arquitectura |
| **5** | El código | ⚠️ **el código no es autoridad: es lo que se AUDITA.** Que algo esté escrito no prueba que deba existir |

⭐ **El #5 es el que da sentido a esta regla.** Sin ella, auditar el producto degenera en *"el código
dice X, así que X es lo correcto"* — y ese es exactamente el defecto que se busca: **código que
funciona sin que nadie sepa si debía estar ahí.**

---

## 2 · ⭐⭐ EL EJE TEMPORAL — contra qué se juzga NO es lo mismo que cuándo se exige

⭐ **El §1 responde CONTRA QUÉ se juzga. Esta sección responde CUÁNDO se exige.** Son dos
preguntas distintas, y confundirlas produce un veredicto inútil.

### 2.1 · 🔴 Por qué existe — medido, no supuesto

**El 2026-08-12 se auditó For3s OS con las dos varas. El resultado:**

| Vara | Veredicto | ¿Sirve? |
|---|---|---|
| El Grafo Maestro **completo** (el destino) | **15 de 15 tablas ausentes** · 7 piezas mayores sin construir · **24 hallazgos** | 🔴 **declara en rojo un sistema que corre a diario** |
| El código como autoridad | todo verde por definición | 🔴 no mide nada — es el defecto que el §1 #5 prohíbe |
| ⭐ **El gate de la fase en curso** | **pasa 6 de 6** · **4 hallazgos** que importan hoy | ✅ **discrimina y es accionable** |

⭐⭐ **Los otros 20 hallazgos no eran falsos: eran PREMATUROS.** Y eso es más peligroso —
**un hallazgo prematuro se ve idéntico a uno urgente**, y entierra a los que sí importan.

### 2.2 · ⭐ LA REGLA

> **Un sistema en construcción por fases se audita contra el gate de SU fase, nunca contra el
> destino final.**

**La autoridad temporal es `memory/archive/Plan_Maestro_Programacion.md`** — define 6 fases
foundation-first, y **cada una tiene su gate objetivo escrito**.

⛔ **El §1 no cambia:** el Grafo sigue mandando sobre **qué debe existir**. El Plan Maestro manda
sobre **qué se exige hoy**. **Ninguno reemplaza al otro.**

### 2.3 · Cómo se sabe en qué fase está el producto

⭐ **Lo declara la CAMPAÑA en su `§F Shared context`, y esta regla obliga a leerlo antes de
juzgar.**

⛔ **No se deduce, no se estima y no se mide en cada bloque.** Un solo sitio lo declara; lo mueve
Brian cuando el sistema avanza de fase.

⚠️ **Y si la campaña NO lo declara, ese es el primer hallazgo** — auditar sin saber la fase
produce los 24 hallazgos de §2.1.

### 2.4 · Qué se hace con lo que falta pero es de una fase POSTERIOR

**Se registra como FUTURO, no como hallazgo.** Sección aparte en el informe:

```markdown
### ⬜ AUSENTE POR FASE — no es deuda, es calendario

| Pieza | ¿Quién la trae? |
|---|---|
| Output Gate firmado | Fase 4 (R7 B2) |
| Prometheus + 5,150 series | Fase 4 (R8 B1) |
| Amígdala (nodo 7) | Fase 5 (R9 B1) |
```

| | |
|---|---|
| ⛔ **NO cuenta** en el veredicto del bloque | no es un defecto: es trabajo no empezado |
| ⛔ **NO detiene** nada | los 5 criterios de 🔴 crítico son otra cosa |
| ✅ **Pero SÍ se escribe** | ⭐ **razón medida:** la Amígdala ausente la encontraron **5 métodos independientes** en la misma auditoría. **Lo que no se registra se re-descubre.** |

---

## 3 · LA PREGUNTA QUE SE HACE ANTE CADA PIEZA

**No** *"¿esto funciona?"* — eso ya lo respondió el MVP.

| Pregunta | Contra qué se contesta |
|---|---|
| **¿A qué nodo del grafo pertenece?** | §4 del grafo — los 11 nodos |
| **¿Qué edge implementa, y qué fluye por él?** | §5 — los 24 edges |
| **¿Respeta los 3 pilares?** | §1 — seguridad · escalabilidad · autonomía |
| **Si no encaja en ningún nodo, ¿por qué existe?** | 🙋 se pregunta a Brian. **No se borra ni se justifica solo** |

⛔ **Una pieza que no pertenece a ningún nodo NO es automáticamente basura**, y tampoco se salva
sola: es un hallazgo que se registra y lo decide Brian (ADR-003).

---

## 4 · ⚠️ LOS TRES PILARES SON EL LISTÓN, Y EL LISTÓN SUBIÓ

El grafo los declara **propiedades estructurales, no features añadidas**: cada nodo y cada edge los
lleva dentro.

> **Brian, 2026-08-10:** *"No es algo que 5 personas lo tendrán, va a ser para miles de millones
> de personas."*

⭐ **Eso mueve el criterio de "funciona" a "aguanta".** Un MVP demuestra que el camino existe; un
producto demuestra que resiste. Las 6 dimensiones de `rules/qa-dimensions.md` se aplican **con esa
vara**, no con la del MVP.

---

## 5 · 🔴 EL HUECO QUE ESTA REGLA DESTAPA — y que hay que cerrar antes

**Medido el 2026-08-10, escribiendo esta regla:**

| Qué | Estado |
|---|---|
| El grafo se declara *"FUENTE DE VERDAD ARQUITECTÓNICA"* | ✅ en su línea 7 |
| Su cabecera cumple el contrato de documento | 🔴 **NO** — sin `Status`, `Type` ni `Updated` |
| Algún validador lo vigila | 🔴 **NO** — `bin/check-blocks` marca `Cerebro/` como **LEGACY exento** |
| Tamaño | **1,279 líneas** |

⭐ **La autoridad del producto es, hoy, el único documento importante que ningún check mira.** Era
coherente mientras `Cerebro/` fuese v1 en espera de migración; **deja de serlo en el momento en que
se convierte en la vara con la que se juzga el código.**

⛔ **No se migra `Cerebro/` entero por esto** — es historia del diseño y migrarla en bloque es
justo el error que `blk-split-architecture` cometió (74% duplicado). **Lo que sí:** el Grafo Maestro
recibe su cabecera y entra en la auditoría, porque es el único que va a decidir.

---

## 6 · ⛔ DÓNDE SE TRABAJA Y HASTA DÓNDE LLEGA — el alcance, decidido

> **Brian, 2026-08-10:** *"Vamos a trabajar en el servidor de For3s, y precisamente la instancia
> que modificaremos será `@For3s_Brian_bot`. Hasta que terminemos con este agente vamos a empezar
> a propagar las actualizaciones. No vamos a actualizar todo el sistema de For3s OS hasta que
> `@For3s_Brian_bot` lo tratemos todo primero."*

| | |
|---|---|
| **Dónde** | 🖥️ el **servidor** `for3s` — no el clon local |
| **Sobre qué** | 🧪 **UNA instancia: `brian`** (`@For3s_Brian_bot`) |
| **Cuándo se propaga** | ⛔ **solo cuando esa instancia esté terminada**, no antes |

⚠️ **El clon local NO es la verdad.** Medido el 2026-08-10: `for3s/For3s-OS/` está en el commit del
**23-jul —18 días desfasado— y con 1 commit sin empujar**. Auditar ahí sería juzgar código viejo,
que es exactamente el error que este trabajo existe para evitar.

⛔ **Las otras 4 instancias no se tocan.** Comparten máquina, imagen y **un solo cupo de suscripción
Claude**: una acción mal dirigida en el servidor apaga el bot de otra persona. `brian` es la
instancia de pruebas **porque su microglía está OFF a propósito** y su dueño es quien decide.

⭐ **Por qué una y no todas:** propagar un cambio no verificado a 5 instancias multiplica el daño
por 5 y hace imposible saber cuál rompió qué. Una instancia primero **es la red de seguridad**, no
lentitud.

---

Related: `Cerebro/For3s_OS_Grafo_Maestro.md` (la autoridad) · `rules/qa-dimensions.md` (las 6
dimensiones con las que se juzga) · `principles/owner-3-validation.md` (quién puede negarse a
cerrar) · `memory/pendiente-agosto-2026.md` (la deuda del producto).
