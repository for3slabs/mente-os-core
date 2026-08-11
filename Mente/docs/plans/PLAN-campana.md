# 🗺️ PLAN · LA CAMPAÑA — la figura que v2 no tiene
**Status:** current · **Type:** plan · **Updated:** 2026-08-10 · **Owner:** brian
**Pedido por:** Brian, 2026-08-10 — *"genera un plan de implementación para que v2 lo tenga
incorporado y nos ayude con este gran bloque… para que nunca pierda nada de contexto entre tareas.
Siempre va a saber sobre el mismo contexto porque es una campaña, todos los códigos van a ser
revisados con los mismos estándares."*
---

## Purpose

Diseñar **la CAMPAÑA**: un contenedor que agrupa varios bloques bajo una misma misión, un mismo
contexto y **los mismos estándares**. Sin ella, `PRODUCTO-FOR3S-OS` no cabe en v2.

⛔ **Este documento no construye nada.** Dice qué se construiría, en qué orden y cómo se verifica
cada parte. Se ejecuta cuando Brian lo apruebe.

---

## 1 · POR QUÉ HACE FALTA — el choque, medido 2026-08-10

| Lo que v2 declara hoy | Lo que la campaña necesita |
|---|---|
| Un bloque = **UN archivo**, máx. **200 líneas** | agrupar varios bloques bajo una misión |
| `§F` sub-bloques: máx. **20 filas** | el bloque de pendientes `PRODUCTO-FOR3S-OS` ya tiene **74** |
| Un sub-bloque = *"una tarea que ataca una pieza"* | aquí un hijo es **otro bloque entero**, con su propio ciclo |

⭐ **v2 se diseñó para bloques de UN tema.** Un bloque de bloques **no existe** — igual que no
existía el vocabulario de conflictos hasta ayer. Y el patrón es el mismo: *un hueco del que nadie
habla es indistinguible de uno que no existe.*

⚠️ **Sin esta figura solo hay dos salidas, y ninguna es lo pedido:** partir en 4 bloques sueltos y
**perder el paraguas** que dice que son la misma misión, o meter 74 filas en un `§F` de 20 y que el
sistema **bloquee el cierre**.

---

## 2 · QUÉ ES UNA CAMPAÑA — y qué NO es

**Una campaña agrupa bloques que comparten misión, autoridad y estándares.** No los ejecuta: los
**ordena** y les **presta contexto**.

| | Bloque | Campaña |
|---|---|---|
| Unidad | una relación de trabajo | **una misión** |
| Contiene | sub-bloques (tareas) | **bloques** |
| Vive en | `blocks/active/<n>/` | `campaigns/<n>/` |
| Cierra cuando | sus sub-bloques cierran + veredicto | **todos sus bloques cierran + su criterio propio** |

⛔ **Lo que la campaña NO hace:**
- No sustituye al bloque. Un bloque sigue siendo la unidad de trabajo y conserva su `§A-K`.
- No relaja ningún techo. Los bloques hijos siguen en 200 líneas y 20 sub-bloques.
- No decide criterio. La autoridad sigue siendo `Cerebro/` (`rules/rule-product-authority.md`).

---

## 3 · LOS DOS PROBLEMAS QUE RESUELVE — y cómo se mide cada uno

### 3.1 · «Que nunca pierda contexto entre tareas»

**Hoy:** el arranque carga el `§A-E` **del bloque activo** (`CLAUDE.md` §🚀). Al cambiar de bloque,
**el contexto del anterior se va** — y con él por qué se decidió lo que se decidió.

**Con campaña:** se carga el `§A-E` del bloque **y el contexto de su campaña**. Ese contexto es el
mismo para los 4 bloques hijos, así que **cambiar de bloque deja de reiniciar el porqué.**

📏 **Cómo se sabe que funcionó:** tras un `/clear`, trabajando en un bloque hijo, el sistema debe
responder sin preguntar: *a qué campaña pertenece · cuál es su autoridad · qué se decidió antes*.
⛔ Si hay que preguntarlo, no funcionó.

### 3.2 · «Todos los códigos revisados con los mismos estándares»

**Hoy:** `hooks/pre-edit-standards.py` inyecta el `§D` **del bloque dueño**. Dos bloques hermanos
pueden declarar `§D` distintos — y entonces **el mismo código se juzga con dos varas**.

**Con campaña:** el `§D` de la campaña **se hereda a todos sus bloques**, y un bloque hijo puede
**añadir**, nunca **quitar** (`rules/rule-inheritance.md`: las reglas se suman, en conflicto gana la
más estricta).

📏 **Cómo se sabe que funcionó:** editar un archivo de **cualquier** bloque hijo inyecta los
estándares de la campaña **más** los propios. 🔬 Se prueba quitando un estándar del `§D` de un hijo:
debe **seguir llegando** por herencia.

---

### 3.3 · 🆕 «Un bloque debe poder conocer el contexto de otro — sin interpretarlo distinto»

> **Brian, 2026-08-10:** *"Si un bloque quiere conocer el contexto de otro lo puede hacer, una
> forma de comunicación para que no se interprete de distintas maneras. Siempre la campaña lo va a
> regir, y aunque tengan contextos diferentes cada bloque o tarea, todo debe estar en comunicación
> y entender que lo que se realizó puede afectar o mejorar a algo. No se realiza a ciegas: se
> evalúa toda la campaña."*

**Hoy hay permiso, pero no canal.** `rules/rule-isolation.md` §1 prohíbe leer otro bloque **salvo
una conexión declarada en su `§C`**, y `§C` solo dice *qué* bloques se relacionan — **no qué se
comunicaron ni qué cambió por ello**. Ningún script lee esas conexiones para nada más que validarlas.

⭐ **El defecto que esto evita, y es el que Brian nombró:** dos bloques leen el mismo hecho y **lo
interpretan distinto**. Es el mismo patrón que las tablas de decisiones duplicadas (75 filas contra
37) — no falló la copia, falló que **cada lado la entendió a su manera**.

**Cómo funciona con campaña:**

| Nivel | Quién manda | Qué contiene |
|---|---|---|
| **Campaña** | ⭐ **rige siempre** | el contexto GRANDE: la misión, la autoridad, los estándares |
| **Bloque** | hereda de la campaña | su contexto propio, que **puede diferir** — y eso es legítimo |
| **Entre bloques** | 🆕 **el canal** | lo que un bloque necesita saber de otro **pasa por la campaña**, no por lectura directa |

⛔ **Por qué el canal pasa por la campaña y no de bloque a bloque:** si dos bloques se leen
directamente, cada uno interpreta lo que ve. Si el hecho **se declara una vez en la campaña**, los
dos leen la misma frase. **Una sola redacción, una sola interpretación.**

### 3.4 · 🆕 «No se trabaja a ciegas: se evalúa toda la campaña»

**Cerrar un bloque no es el final.** Al cerrarlo se responde: **¿qué otros bloques de esta campaña
quedan afectados — para bien o para mal?**

📏 **Cómo se sabe que funcionó:** al cerrar un bloque, su `§K` declara el impacto sobre los hermanos
**por nombre**, o dice explícitamente *"ninguno, y por esto"*. ⛔ Silencio no vale: hoy
`connections.md` ya pide eso al archivar, pero **solo mira hacia fuera del bloque, nunca hacia sus
hermanos de campaña**.

---

## 4 · LAS 8 FASES — cada una entrega UNA cosa verificable

> `principles/expertise/doc-planning.md`: *una fase entrega UNA cosa verificable, y declara de qué
> depende.* Si entrega dos, no se sabe cuál falló.

| # | Fase | Entrega | Depende de | Cierra cuando |
|---|---|---|---|---|
| **C1** | **El contrato** | `rules/contract-campaign.md`: qué secciones tiene, qué es obligatorio para abrir y para cerrar | — | `bin/check-blocks` valida una campaña de prueba |
| **C2** | **La herencia de estándares** | el `§D` de la campaña llega a todos sus bloques | C1 | 🔬 se quita un estándar de un hijo y **sigue llegando** |
| **C3** | **El contexto compartido** | el arranque carga campaña + bloque | C1 | 🔬 tras `/clear`, el sistema dice a qué campaña pertenece **sin preguntar** |
| **C4** | 🆕 **El canal entre bloques** | un hecho que un bloque necesita de otro se declara **una vez en la campaña**, no se lee del hermano | C1 · C3 | 🔬 dos bloques citan el mismo hecho y **producen la misma frase** — no dos redacciones |
| **C5** | 🆕 **La evaluación de impacto** | al cerrar un bloque, su `§K` declara qué hermanos quedan afectados — o *"ninguno, y por esto"* | C1 · C4 | 🔬 se cierra un bloque sin declarar impacto y **la puerta lo impide** |
| **C6** | **El validador** | `bin/check-campaigns` | C1 · C4 · C5 | 4 sabotajes: hijo huérfano · campaña sin autoridad · cierre con hijo abierto · cierre sin evaluar impacto |
| **C7** | **El cierre de campaña** | una campaña no cierra con bloques abiertos | C1 · C6 | 🔬 se intenta cerrar con un hijo abierto y **la puerta lo impide** |
| **C8** | **La primera campaña real** | `PRODUCTO-FOR3S-OS` abierta con sus bloques | C1-C7 | sus bloques declarados, su autoridad citada, batería en verde |

⭐ **C1 primero y sin discusión:** las otras siete escriben *sobre* el contrato. Empezar por el
validador sería validar una forma que aún no existe.

---

## 5 · CÓMO SE VERÍA FALLAR — los sabotajes, por fase

⛔ `principles/expertise/val-functional.md` §2.2: *un check debe verse fallar antes de que su verde
signifique algo.*

| Fase | Sabotaje | Debe pasar |
|---|---|---|
| C1 | campaña sin autoridad declarada | `check-blocks` la rechaza |
| C2 | quitar un estándar del `§D` de un hijo | **sigue llegando** por herencia |
| C2-bis | quitar el estándar de la CAMPAÑA | **deja de llegar a todos** — prueba que la herencia es real y no una copia |
| C3 | borrar el puntero a la campaña en un bloque | el arranque lo dice, **no lo adivina** |
| C4 | un bloque declara una campaña que no existe | 🔴 hijo huérfano |
| C4 | dos bloques citan el mismo hecho | **producen la misma frase**, no dos redacciones |
| C4-bis | un bloque lee a un hermano **sin** pasar por la campaña | 🔴 `rule-isolation` §1 ya lo prohíbe: el canal no lo relaja |
| C5 | cerrar un bloque sin declarar impacto en sus hermanos | ⛔ la puerta lo impide |
| C7 | cerrar la campaña con un hijo abierto | ⛔ la puerta lo impide |

⭐ **El C2-bis es el que importa:** si quitar el estándar de la campaña **no** lo quita de los
hijos, entonces se copió en vez de heredarse — y dos copias divergen. Es el mismo defecto que las
tablas de decisiones duplicadas (75 filas contra 37).

---

## 6 · ⚠️ LO QUE PUEDE SALIR MAL — dicho antes, no después

| Riesgo | Por qué es real |
|---|---|
| **Una capa más que nadie usa** | v2 ya tiene bloque · sub-bloque · pendiente · plan. La campaña es la quinta. **Si no ahorra trabajo desde el primer día, sobra** |
| **Herencia que se vuelve copia** | si el `§D` se copia al hijo en vez de leerse de la campaña, divergen. Lo cubre C2-bis |
| **La campaña como cajón** | si todo acaba siendo "de la campaña", deja de ordenar. Una campaña **declara sus bloques por nombre**; lo que no está, no pertenece |
| **Contexto que engorda** | cargar campaña + bloque en cada arranque cuesta tokens. ⚠️ El contexto de campaña necesita **techo propio**, y C3 debe medirlo — no basta con que funcione |

---

## 7 · LAS 3 DECISIONES — RESPONDIDAS por Brian (2026-08-10)

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Cuántos bloques tendrá una campaña? | ⭐ **DINÁMICO.** *"No lo sabemos hasta que empecemos a desarrollarlo… va a haber campañas con muchos bloques y algunas con pocos."* ⛔ El contrato **no fija un número**: fijarlo obligaría a inventar bloques para llenar el hueco, o a partir la misión para que quepa |
| 2 | ¿La campaña reemplaza al bloque de pendientes `PRODUCTO-FOR3S-OS`? | ⭐ **NO — son cosas distintas.** El pendiente registra QUÉ falta; la campaña ORGANIZA cómo se ataca. ⚠️ Comparten nombre: el contrato debe hacer que la campaña **apunte** a su bloque de pendientes, para que nadie los confunda |
| 3 | ¿`orquestacion-multiagente` es un bloque de esta campaña? | **NO, aún no.** Sigue bloqueado y se decidirá después |

⭐ **La 1 cambia el contrato:** una campaña se abre con **al menos un bloque declarado** y crece
según el trabajo lo pida. **Sin techo y sin suelo artificial** — el número lo dicta la misión, no el
formulario.

---

Related: `rules/contract-block.md` (los límites que este plan choca) ·
`rules/rule-product-authority.md` (la autoridad que la campaña hereda) ·
`principles/expertise/doc-planning.md` (por qué una fase entrega UNA cosa) ·
`rules/rule-inheritance.md` (las reglas se suman, nunca se relajan) ·
`memory/pendiente-agosto-2026.md` (los 74 pendientes que la campaña ordenará).
