# PLAN · LAS 3 FASES — el método con el que se audita For3s OS

**Status:** current · **Type:** plan · **Updated:** 2026-08-12 · **Owner:** brian
**Verified by:** `bin/check-campaigns` · el campo `fase:` (por construir, §7)
**Campaña:** `campaigns/producto-for3s-os/CAMPAIGN.md`

## Purpose

**Cómo se recorre For3s OS tres veces, con tres miradas distintas, sin perder el hilo.**

⛔ **Este documento NO ejecuta nada.** Define el método: qué mira cada fase, qué entrega un bloque
para poder decir que la pasó, qué detiene el trabajo y dónde vive cada archivo. **Se aprueba antes
de construir** (`ESTANDAR_Metodo_Fases_F`: explicar → aprobar → construir).

---

## 1 · LA FIGURA — una fase NO es un bloque

> **Brian, 2026-08-11:** *"No mezcles los bloques con las fases. Existen fases y todos los bloques
> N van a ser tratados a partir de la estructura de cada una de las fases, de tal manera que
> tendremos 3 corridas de fases con N número de bloques."*

⭐ **Una fase es una MIRADA — un método de auditar. Los bloques se tratan según la estructura de
esa fase.**

```
CAMPAÑA producto-for3s-os
  │
  ├─ FASE 1 · mirada NODOS       → los 12 bloques, uno a uno
  ├─ FASE 2 · mirada ESTRUCTURA  → los MISMOS 12, otra mirada
  └─ FASE 3 · mirada EDGES       → los MISMOS 12, tercera mirada
```

**Decisiones que rigen la figura** (Brian, 2026-08-11):

| | |
|---|---|
| Los bloques son **los mismos** en las 3 corridas | un bloque pasa 3 veces · **no cierra hasta las 3** |
| El recorrido es **secuencial por fase** | TODOS pasan la 1, luego todos la 2 · al acabar cada corrida hay un mapa completo del sistema bajo esa mirada |
| La fase se registra **en el bloque + validador** | campo `fase:` en su cabecera · un check impide que salte fases |

---

## 2 · LAS 3 MIRADAS

| Fase | Mirada | Su estructura | Autoridad |
|---|---|---|---|
| **1** | **NODOS** | los 11 nodos cerebrales | `Cerebro/For3s_OS_Grafo_Maestro.md` §4 |
| **2** | **ESTRUCTURA** | declarado vs real, componente por componente | el árbol + `piezas.tsv` |
| **3** | **EDGES** | los 24 edges — qué fluye por cada uno | `Cerebro/For3s_OS_Grafo_Maestro.md` §5 |

### 2.1 · Fase 1 — NODOS

**Pregunta:** *¿cada nodo del Grafo existe, hace lo declarado, y con qué evidencia?*

⭐ **El mapa nodo→archivo ya está medido** (`campaigns/producto-for3s-os/terreno/AUDITORIA-MENTE-OS-CONOCIMIENTO.md` §19.2) —
**la fase 1 no lo descubre: lo verifica y lo profundiza.**

⚠️ **Y arranca sabiendo que 2 nodos no existen** (Amígdala y Tálamo, confirmados por 5 métodos).
**Eso no es un hallazgo de la fase 1: es su punto de partida.**

### 2.2 · Fase 2 — ESTRUCTURA

**Pregunta:** *¿la organización real corresponde a la declarada, y cada pieza hace UNA cosa?*

> **Brian, 2026-08-11:** *"No puedes sobresaturar un archivo. Vamos a tener que auditar componente
> por componente y verificar la construcción."*

⛔ **La fase 2 MARCA y documenta; NO parte.** Partir es desarrollo, y esta campaña verifica.
**Documenta qué responsabilidades mezcla cada gigante y dónde estarían las costuras.**

⚠️ **OBLIGACIÓN — la decisión aplazada de Brian:**

> *"Se parte, aún no tenemos que empezar a avanzar con la campaña para decidir; **recuérdamelo
> cuando lleguemos a ese archivo y los otros que tienen mucho código**."*

⛔ **Ningún bloque cierra su fase 2 sin preguntarle a Brian si su archivo se parte.** La lista de
los 18 archivos >400 líneas con su bloque dueño está en
`campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` §16.

### 2.3 · Fase 3 — EDGES

**Pregunta:** *¿ese flujo existe de verdad, y pasan datos por él?*

Recorre los 24 edges del Grafo §5. **Un edge muerto explica un flujo roto** — por eso va después
de conocer los nodos y la estructura.

---

## 3 · LO QUE ENTREGA UN BLOQUE PARA PASAR UNA FASE

> **Brian, 2026-08-12:** *"Un veredicto por nodo con evidencias y también por bloque, ambos."*

**Dos niveles, obligatorios los dos.**

### 3.1 · Nivel 1 — veredicto POR NODO (o por pieza)

Cada nodo que el bloque toca produce **cuatro respuestas medidas**, cada una con su comando:

```markdown
### Nodo 2 · Hipocampo → `memory.py` (716 líneas)

| Pregunta | Respuesta | Evidencia |
|---|---|---|
| ¿existe el archivo? | ✅ | `ls memory.py` → 716 líneas |
| ¿hace lo que el Grafo declara? | ✅ | 33,908 episodios · 33,908 con embedding |
| ¿su tabla tiene datos? | ✅ | `episodes_events` = 33,908 filas |
| ¿pasa las 4 pruebas del público? | 🔴 | contenido EN CLARO (H-01) |
```

⭐ **La cuarta pregunta es la vara del público de Brian**, y aplica en las tres fases:

| Falla si… | Por qué |
|---|---|
| hay algo **hardcodeado a `brian`** | otro usuario lo instala y funciona como si fuera Brian |
| hay algo **que solo Brian sabe usar** | un usuario nuevo no descubre que existe |
| hay algo **que no escala a miles** | *"no es algo que 5 personas lo tendrán"* |
| hay algo **que expone datos de otro** | la información de cada usuario es suya |

### 3.2 · Nivel 2 — veredicto POR BLOQUE

Además de los veredictos por nodo, el bloque cierra su fase con **un veredicto agregado**:

```markdown
## Fase 1 · veredicto del bloque `memoria`

**🟡 PARCIAL** — 2 nodos verificados (2 Hipocampo · 5 Microglía), ambos existen y funcionan.

| Hallazgo | Gravedad | Detiene |
|---|---|---|
| H-01 contenido en claro | 🔴 secreto expuesto | **SÍ** |
| H-02 el contador no cuenta lo importado | 🔴 puede destruir datos | **SÍ** |
| falta `legal_hold` | 🟡 | no |

**Fase 1: NO PASA** — 2 críticos detienen el bloque.
```

⛔ **Un veredicto sin evidencia no cuenta.** `rules/rule-checks-must-measure.md`: un número sin
comando que lo produzca es una opinión con formato de dato.

---

## 4 · LOS 5 CRITERIOS DE 🔴 CRÍTICO — lo que DETIENE un bloque

> **Brian, 2026-08-12**, los cinco.

| # | Criterio | Por qué · precedente medido |
|---|---|---|
| **1** | **Expone datos de un usuario a otro** | **BUG-14** (2026-06-30) nació de relajar una condición de un `WHERE`: el scope de un miembro devolvía turnos privados de Brian |
| **2** | **Puede destruir o perder datos** | **H-02 medido**: la microglía podría podar material importado que SÍ se usa · **4,230 episodios ya están bajo el umbral de poda** |
| **3** | **Un secreto en claro o expuesto** | **H-01**: 15 MB de conversaciones legibles sin descifrar · y la clave Zen marcada para rotar hace 2 meses |
| **4** | **Rompe el agente en producción** | el servidor es la vía diaria de Brian · `telegram_channel.py` es la puerta |
| **5** | 🟠 **Deuda que crece — NO detiene, se ESCALA** | ver §4.1 |

### 4.1 · ⭐ La quinta categoría — la que Brian añadió

> **Brian, 2026-08-12:** *"Repetir la lógica haciendo cuellos de botella, mala redacción en código
> como redundancia… no es crítico pero si se va estirando ese error se convierte en crítico."*

**Tratamiento LOCKED: no detiene el bloque, pero se registra APARTE con su medida de HOY.**

```markdown
## 🟠 DEUDA QUE CRECE — bloque `canal-telegram`

| Pieza | Medida ANTERIOR | Medida HOY | Δ |
|---|---|---|---|
| `telegram_channel.py` | 3,350 líneas (jun) | **4,570** (ago) | **+36%** |
```

⭐⭐ **Por qué se separa de los hallazgos normales, medido:** `telegram_channel.py` **se declaró
deuda en junio con 3,350 líneas y hoy tiene 4,570 — creció 36% DESPUÉS de señalarse.**
**Un hallazgo entre otros 24 no se ve crecer. Uno en su propia sección, con dos medidas, sí.**

⛔ **Y por eso NO detiene:** For3s OS tiene 36 de 76 módulos sin ejecutar y 3 archivos >1,000
líneas. **Si la deuda detuviera, casi todos los bloques quedarían parados el primer día** — y una
puerta que bloquea el trabajo normal se acaba quitando (`rules/rule-friction.md`).

---

## 5 · CÓMO SE CIERRA UNA FASE

> **Brian, 2026-08-12:** *"El gate cierra, tú puedes reabrir."*

⭐ **Es el nivel 2 del airlock** (`rules/rule-pr-batching.md` §5).

```
el bloque cumple la lista de terminado de su fase
        ↓
  el gate la CIERRA — no espera a Brian
        ↓
  el bloque avanza (o queda listo para la siguiente corrida)
        ↓
  ⭐ Brian puede REABRIRLA cuando la revise
```

**Y las dos excepciones que sí paran:**

| Situación | Qué pasa |
|---|---|
| 🔴 **un crítico de §4** | **el bloque se DETIENE** hasta resolverlo · los otros 11 siguen |
| ⛔ **fase 2 con un archivo grande** | **pregunta obligatoria a Brian** antes de cerrar (§2.2) |

⛔ **Lo que el gate NO relaja:** un bloque **no cierra del todo hasta pasar las 3 fases**
(decisión de Brian, 2026-08-11).

---

## 6 · EL ENCARPETADO — dónde vive cada archivo

> **Brian, 2026-08-12:** *"Créale una estructura de encarpetado para que sepa dónde dejar los
> archivos y cómo buscarlos a lo largo de una campaña, y exista orden y profesionalismo."*

**Organizado POR TIPO DE DOCUMENTO** — cada carpeta responde a una pregunta distinta:

```
campaigns/producto-for3s-os/
│
├── CAMPAIGN.md              ⭐ LA PUERTA — misión, autoridad, los 12 bloques, la vara
│
├── terreno/                 📚 lo MEDIDO ANTES de empezar (no cambia con las fases)
│   ├── LA-VERDAD-DE-V1.md          📕 qué es For3s OS, medido — ENTRAR POR AQUÍ
│   ├── AUDITORIA-FOR3S-OS-2026-08.md    el terreno del código (35 pasadas)
│   └── AUDITORIA-MENTE-OS-CONOCIMIENTO.md  el terreno del conocimiento (33 §)
│
├── fases/                   🔍 UN informe por corrida completa (12 bloques cada uno)
│   ├── FASE-1-nodos.md
│   ├── FASE-2-estructura.md
│   └── FASE-3-edges.md
│
└── hallazgos/               🔴 lo que SALE de cada bloque en cada fase
    ├── seguridad-fase-1.md
    ├── memoria-fase-1.md
    └── <bloque>-fase-<n>.md
```

### 6.1 · La regla de cada carpeta

| Carpeta | Contiene | ⛔ NO contiene |
|---|---|---|
| **raíz** | solo el CAMPAIGN y este plan | ningún informe ni hallazgo |
| **`terreno/`** | lo medido **antes** de la campaña · **no se reescribe**, se re-mide | veredictos de fase |
| **`fases/`** | el mapa agregado de una corrida · **12 bloques en un documento** | el detalle por bloque |
| **`hallazgos/`** | un archivo por **bloque × fase** · el veredicto por nodo + el del bloque | el agregado de la fase |

### 6.2 · Cómo se busca

| Se pregunta… | Se abre… |
|---|---|
| *"¿qué es For3s OS?"* | la verdad de v1, en **terreno** |
| *"¿cómo quedó la fase 1 completa?"* | el informe de esa fase, en **fases** |
| *"¿qué encontró `memoria` en la fase 1?"* | su archivo en **hallazgos**, nombrado `<bloque>-fase-<n>` |
| *"¿qué bloques hay y en qué orden?"* | `campaigns/producto-for3s-os/CAMPAIGN.md` |

⭐ **El nombre del archivo es la ruta de búsqueda:** `<bloque>-fase-<n>.md` se adivina sin
consultar un índice.

---

## 7 · LO QUE FALTA CONSTRUIR — y no es este documento

⛔ **Este plan es el método. Lo que sigue son piezas separadas, cada una con su verificación:**

| # | Pieza | Por qué |
|---|---|---|
| **1** | **La vara en `rules/rule-product-authority.md`** | el gate de la fase hoy solo vive en el `CAMPAIGN`; una regla no declarada **no se hereda a los bloques** |
| **2** | **El campo `fase:` en `rules/contract-block.md`** | sigue el patrón que `check-blocks` ya usa (`id:` `status:` `type:` `intent:`) |
| **3** | **El check en `bin/check-blocks`** | ⭐ la ley: una regla en documento se cumple 40-60% · debe verificar que **no se salte fases** y que **no cierre sin las 3** |
| **4** | **Los 12 `BLOCK.md`** | `bin/check-campaigns` exige que un bloque declarado **exista en disco** |
| **5** | **Mover `terreno/`** | los 3 documentos están hoy en la raíz de la campaña |

⚠️ **Nota:** el árbol de §6 es el **destino**, no el estado de hoy — las carpetas se crean en el
punto 5. Por eso este plan no cita esas rutas como si existieran.

⚠️ **Y un parámetro que NO se decidió y hará falta antes del punto 4:** el `§B scope` de cada
bloque — **qué archivos exactos toca**. Con 76 archivos y 12 bloques el reparto no es obvio, y
**si dos bloques reclaman el mismo archivo, `hooks/pre-edit-standards.py` entrega los estándares
equivocados** (pasó ya, documentado en `blocks/archive/separacion-motor-instancia_2026-08`).

---

## 8 · CÓMO SE VERÁ QUE ESTE PLAN FUNCIONA

🔬 **La prueba, cuando el primer bloque corra su fase 1:**

| | |
|---|---|
| ✅ | produce **veredicto por nodo Y por bloque**, cada uno con su comando |
| ✅ | sus archivos caen en **hallazgos**, nombrados `<bloque>-fase-1`, **sin que nadie decida dónde** |
| ✅ | si encuentra un 🔴 de §4, **se detiene solo** y los otros bloques siguen |
| ✅ | si encuentra deuda que crece, **la reporta aparte con dos medidas** |
| 🔬 | y **el gate cierra la fase sin esperar a Brian** — que es lo que el airlock existe para lograr |

⛔ **Si el primer bloque necesita que alguien le diga dónde guardar un archivo o qué formato usar,
este plan falló** — y se corrige aquí, no en el bloque.

---

Related: `campaigns/producto-for3s-os/CAMPAIGN.md` (la campaña: misión, 12 bloques, la vara) ·
`campaigns/producto-for3s-os/terreno/LA-VERDAD-DE-V1.md` (qué es For3s OS, medido) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` §16 (los 18 archivos grandes) ·
`rules/contract-campaign.md` (la forma de una campaña) ·
`rules/rule-product-authority.md` (la autoridad · ⚠️ le falta la vara de la fase) ·
`rules/rule-pr-batching.md` §5 (el airlock de 3 niveles) ·
`rules/rule-checks-must-measure.md` (por qué un veredicto sin evidencia no cuenta) ·
`memory/archive/Plan_Maestro_Programacion.md` (las 6 fases y sus gates — de donde sale la vara).
