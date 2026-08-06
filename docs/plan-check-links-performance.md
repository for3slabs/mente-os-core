# PLAN · acelerar `check-links` sin cambiar qué considera roto
**Status:** current · **Type:** plan · **Updated:** 2026-08-05 · **Owner:** brian
**Verified by:** este plan se juzga contra `principles/expertise/doc-planning.md` (§2.5: cada
ticket lleva dato · comando · qué se vería si fallara · quién lo firma)
**Estado:** ✅ **F0 · F1 · F4 EJECUTADAS 2026-08-05.** F2 y F3 quedan **descartadas por innecesarias** — ver §9.

---

## Purpose

`bin/check-links` tarda **1m 01s** y es el **88%** del tiempo de todo Mente OS. Este plan lo baja a
segundos **sin cambiar una sola respuesta** del validador.

> ⛔ **El miedo que gobierna este plan** (Brian, 2026-08-05): *"si no lo hacemos bien vamos a tener
> los mismos fallos que antes de v1, que se suponía que sí pasaban y al detenernos a detalle
> resultó que no."* Un validador que va rápido y **perdona una cita rota de verdad** es peor que
> uno lento: reintroduce exactamente el fallo que el v2 existe para cerrar.
>
> **Por eso la fase F0 no toca nada** — solo prueba que la respuesta nueva es idéntica a la vieja,
> cita por cita. Si no lo es, el plan se detiene ahí.

---

## 1 · EL ESTADO MEDIDO — el ANTES, sin el cual no se puede saber si mejoró

Todo lo de esta sección está medido hoy, no estimado.

| Medición | Valor | Cómo |
|---|---|---|
| `check-links` | **1m 01s** | `time bin/check-links` |
| Los otros **6** validadores, sumados | **0.66s** | medidos uno a uno |
| `bin/test-f0-f6` | **1m 10s** | invoca `check-links` **una vez** (ver 🔴 corrección, §9) |
| `bin/generate-metrics` | **2m 31s** | corre la batería **y además** `check-links` otra vez |

### El perfilado — dónde se va el tiempo, exacto

```
in_sibling_repo()   →      1,980 llamadas
  glob recursivo    →      4,184 globs
    _rlistdir       → 14,730,455 llamadas
      tiempo        →        114 s  (99.8 % del total)
```

**La causa no está en Mente OS.** Está en que `glob.glob("**/nombre", recursive=True)` recorre
`../marca-personal`, que tiene **43,986 archivos**, y lo repite ~2,000 veces.

### 🔴 EL DATO QUE HACE ESTO DELICADO

| Citas | Cuántas | Rama que usan |
|---|---|---|
| Con `/` en la ruta | 220 | `os.path.exists` — barata, **no se toca** |
| **De nombre desnudo** | **558** | el glob recursivo — la cara |
| **De ésas, SALVADAS por el glob** | 🔴 **110** | nombres como AGENTS, CLAUDE, PENDIENTES o SKILL… |

> ⭐ **Si el índice difiere del glob en UNA sola de esas 110**, o aparecen citas rotas falsas
> (ruido que enseña a ignorar el rojo) o **se perdona una cita rota de verdad** (el fallo del v1).
> **Esa es toda la superficie de riesgo, y es medible antes de tocar nada.**

### La regla que NO puede cambiar

`in_sibling_repo` perdona un nombre desnudo **solo si el repo hermano contiene EXACTAMENTE UN
archivo con ese nombre**. Dos coincidencias = cita ambigua = defecto que se reporta.
**El índice debe preservar ese `len(hits) == 1` exacto**, no "si existe".

---

## 2 · ⭐ EL SISTEMA COMPLETO EN MARCHA — lo que el plan NO había medido

**Brian, 2026-08-05:** *"¿consideraste todos los procesos de Mente OS v2 con las nuevas
actualizaciones y lo que pasa cuando está haciendo distintas tareas?"* — **no, la primera versión
midió `check-links` aislado.** Esto es lo que faltaba, medido.

### A · La ruta de EDICIÓN — medida

Arranque **0.18s** · los 2 hooks antes de cada edición **0.023s / 0.024s** · `grade-block` sobre un
repo de 44k archivos **0.362s** · la puerta del commit **0.38s**.

> ✅ **HALLAZGO 1 — la ruta de edición está SANA.** Ningún hook llama a `check-links`
> (verificado: `grep` sobre `hooks/` da cero). El coste de trabajar es de **milisegundos**, y las
> nuevas puertas de hoy (P1, P2) **no lo empeoraron**: `pre-commit` pasó de 0.29s a 0.38s.

### B · Dónde SÍ duele

**El ciclo real de hoy** (editar → validar → regenerar): `generate-index` 0.071s + `check-blocks`
0.309s + **`check-links` 1m 04s** = el validador lento es el **99.4%** del ciclo.

> 🔴 **HALLAZGO 2 — el coste es MULTIPLICATIVO, no lineal.** `generate-metrics` (2m31) contiene la
> batería (1m10), que invoca `check-links`, y luego `generate-metrics` lo lanza otra vez.
> **Una sola orden de "regenera métricas" recorría los 43,986 archivos del vecino dos veces.**
> ⚠️ La primera versión decía *"cinco veces"* — era falso, ver la corrección en §9.

---

## 3 · 🔴 CONCURRENCIA Y PROCESOS — la parte que decide qué se prohíbe

### C · HALLAZGO 3 — la batería MUTA el árbol real

`bin/test-f0-f6` crea bloques sonda bajo `blocks/active/zz-*` y los borra al final. **No son
temporales aislados: son directorios en el árbol de verdad**, porque cada validador se ancla a su
propia ubicación y aislarlos exigiría reescribir trece.

Por eso toma un lock (`mkdir` atómico + `trap … EXIT INT TERM`) que **se niega en vez de esperar**:
una batería en cola parecería colgada. Y **reclama el lock si el dueño murió**, para que una
corrida matada no lo bloquee para siempre.

> ✅ **Auditado hoy: el lock está bien construido y NO produce zombies.** El `trap` cubre salida
> normal, fallo e interrupción. Comprobado: no hay restos `zz-*` en el árbol.
>
> ⚠️ **Pero define un límite duro para este plan:** **la batería no se puede paralelizar** ni
> ejecutar dos veces a la vez. Cualquier "optimización" que lance corridas concurrentes
> **corrompería el árbol** — es exactamente el fallo que Brian teme. **F1-F3 no tocan esto.**

### D · 🔴 HALLAZGO 4 — el defecto de concurrencia que YA existe

`generate-metrics` lanza la batería con `subprocess.run(timeout=300)`. Si otra batería está viva,
**la segunda es RECHAZADA (exit 1)** y `generate-metrics` publica los números de la corrida VIEJA
**sin avisar**. **Pasó tres veces en esta sesión** (ya registrado en `blocks/archive/distribucion_2026-08` §H).

⚠️ **Este plan NO lo arregla, y decirlo importa:** F1 lo hace *menos probable* (menos tiempo = menos
ventana de solape), **no imposible**. Queda como defecto abierto e independiente.

### E · ✅ HALLAZGO 5 — el timeout protege de verdad

`subprocess.run(..., timeout=300)` en las dos llamadas de `generate-metrics`. **Un proceso colgado
muere a los 5 minutos**, no se acumula. Con F1, ese margen pasa de ~2× a ~20× el tiempo real.

---

## 4 · LO QUE CUESTA LA ALTERNATIVA — medido, no supuesto

```
construir un índice {nombre: [rutas]} de los 5 repos hermanos:  0.18 s
nombres indexados:                                             24,816
```

**0.18s contra 114s.** El índice se construye una vez por ejecución y se consulta en memoria.

---

## 5 · LAS FASES — F0 no toca nada

> Cada fase entrega **UNA cosa verificable** y declara de qué depende (`principles/expertise/doc-planning.md` §2.1).

> ✅ **F0, F1 y F4 EJECUTADAS.** Los números medidos y los defectos que destaparon
> viven en **`docs/resultado-check-links-performance.md`** — este archivo es el DISEÑO.

### F0-ORIGINAL · el diseño que se ejecutó — ⛔ sin tocar `check-links`

**Depende de:** nada. **Entrega:** un script desechable que compara ambos métodos.

| Campo | Valor |
|---|---|
| **Qué hace** | para las **558** citas de nombre desnudo, calcula la respuesta por glob y por índice, y las compara **una a una** |
| **Dato de éxito** | **0 diferencias** sobre 558 |
| **Comando** | el script escribe `same=N diff=M` y lista cada diferencia con su cita |
| **Qué se vería si fallara** | `diff > 0`, con el nombre exacto de cada cita que discrepa |
| **Quién lo firma** | 🤖 el número — pero **si `diff > 0`, decide Brian** si se sigue |

> ⭐ **Esta fase es el plan entero.** Si F0 no da 0, **no se ejecuta F1** y el plan muere aquí.
> Es la aplicación literal de `principles/expertise/val-functional.md` §2.2: *un dato concreto que el sistema devolvió*,
> y de `principles/expertise/doc-planning.md` §2.2: *todo límite que el plan declare se mide antes de afirmarlo*.

---

### F1-ORIGINAL · el diseño que se ejecutó

**Depende de:** F0 en verde. **Entrega:** `in_sibling_repo` consultando un índice cacheado.

| Campo | Valor |
|---|---|
| **Qué cambia** | ~15 líneas: un índice `{nombre: [rutas]}` por repo, construido perezosamente y cacheado en un global |
| **Qué NO cambia** | la rama de citas **con `/`** (sigue con `os.path.exists`) · el criterio `len(hits) == 1` · los mensajes · los códigos de salida |
| **Dato de éxito** | `check-links` **< 5s** (hoy 61s) **y** *"every citation resolves (293 files checked)"* — **el mismo texto y el mismo número** |
| **Comando** | `time bin/check-links` |
| **Qué se vería si fallara** | un conteo distinto de 293, o citas rotas que hoy no existen |
| **Quién lo firma** | 🤖 medición · **Brian aprueba antes de escribir** |

⚠️ **Riesgo declarado — la caché puede envejecer dentro de una misma ejecución.** Si el proceso
tarda y alguien crea un archivo mientras corre, el índice no lo ve. **Aceptado**: `check-links`
pasará a durar segundos, y el glob actual tiene el mismo problema en una ventana mayor.

---

### ⛔ F2 · DESCARTADA — y el motivo que la descartaba era FALSO

**Depende de:** F1. **Entrega:** una invocación en vez de cinco.

| Campo | Valor |
|---|---|
| 🔴 **Qué se creía** | *"la batería llama a `check-links` 5 veces"* — **medido con `grep -c`, que cuenta TEXTO, no invocaciones**. Las otras 4 coincidencias (líneas 1265, 1278, 1365, 1442) son **menciones en comentarios** |
| ✅ **Lo real** | la batería lo invoca **UNA sola vez** (línea 1271). **No hay nada que quitar** |
| **Dato de éxito** | `bin/test-f0-f6` **< 20s** (hoy 1m 10s) |
| **Comando** | `time bin/test-f0-f6` · y `passed`/`failed` **idénticos a hoy: 175 / 0** |
| **Qué se vería si fallara** | un `passed` distinto de 175 → se rompió un check, no se aceleró |
| **Quién lo firma** | 🤖 el conteo de checks |

---

### F3 · `generate-metrics` DEJA DE MEDIR DOS VECES

**Depende de:** F2. **Entrega:** una lectura en vez de una segunda ejecución.

| Campo | Valor |
|---|---|
| **Qué cambia** | `generate-metrics` corre la batería (que ya contiene `check-links`) **y luego `check-links` otra vez**. Con F1 el ahorro es menor, así que **esta fase se reevalúa con el dato**, no se da por hecha |
| **Dato de éxito** | `generate-metrics` **< 30s** (hoy 2m 31s) |
| **Comando** | `time bin/generate-metrics` · y `battery.checks` / `links.broken` **iguales a hoy** |
| **Qué se vería si fallara** | `links.broken` distinto de 0 → la métrica dejó de medir lo que dice |
| **Quién lo firma** | 🤖 los valores publicados en `docs/METRICS.md` |

---

### F4 · ⭐ LA BATERÍA §5-BIS DEL SISTEMA COMPLETO — obligatoria, no opcional

**Depende de:** F1 (y de F2/F3 si se hacen). **Entrega:** la prueba de que **nada más** se rompió.

> ⭐ **Por qué existe esta fase:** *"no basta probar el carril; hay que verificar que TODO sigue
> conectado"* (Método F §2.4). F1 mide `check-links`; **F4 mide el sistema haciendo su trabajo.**
> Sin ella, el plan probaría el carril y nada más — exactamente lo que la regla prohíbe.

| # | Qué se verifica | Comando | Dato de éxito |
|---|---|---|---|
| 1 | La ruta de EDICIÓN sigue barata | los 2 hooks sobre un fichero de bloque | **< 0.1s** cada uno, como hoy |
| 2 | La puerta del COMMIT sigue funcionando | `bash hooks/pre-commit.sh` | exit **0** con el árbol al día · exit **1** con el índice desfasado |
| 3 | La puerta del CIERRE sigue funcionando | `bin/check-clear-ready` | detecta batería roja y resultado viejo |
| 4 | **La batería entera** | `bin/test-f0-f6` | **175 / 0**, idéntico |
| 5 | **Las métricas publican lo mismo** | `bin/generate-metrics` | `links.broken` **0** · `battery.checks` **175** |
| 6 | 🔴 **El lock sigue protegiendo** | lanzar 2 baterías a la vez | la segunda **se niega** (exit 1), **no** corrompe |
| 7 | 🔴 **No quedan restos de sonda** | `ls blocks/*/zz-*` | **vacío** |

**Qué se vería si fallara:** cualquier número distinto de los de hoy. **Quién lo firma:** 🤖 los
comandos — y **Brian ve la tabla antes de dar por cerrado el plan.**

---

## 6 · ⛔ LO QUE ESTE PLAN NO HACE

- **No toca la rama de citas con `/`** — 220 citas que ya son baratas.
- **No relaja el criterio de ambigüedad.** `len(hits) == 1` se preserva literal: dos coincidencias
  siguen siendo un defecto reportado, nunca un perdón por suerte.
- **No cambia mensajes ni códigos de salida** — `hooks/pre-commit.sh`, `bin/test-f0-f6` y
  `bin/generate-metrics` dependen de ellos.
- **No añade dependencias.** Solo stdlib, como exige el CI.
- **No borra ni mueve ningún archivo.** Todo el cambio vive dentro de una función.

---

## 7 · CÓMO SE REVIERTE

`git diff` de **un solo archivo** (`bin/check-links`). Sin migración, sin estado, sin efectos fuera
del proceso. **Revertible sin tocar a ningún consumidor** — la condición 4 de
`principles/expertise/val-integration.md` §2.1, que es la que suele saltarse.

---

## 8 · 🔴 LOS PROCESOS ZOMBIE — auditados uno por uno, no supuestos

> *"Si no lo hacemos bien va a haber procesos zombies."*

**Auditoría completa de dónde nacen procesos en Mente OS v2:**

| Pieza | ¿Lanza subprocesos? | ¿Puede dejar huérfanos? |
|---|---|---|
| `check-links` | ❌ **no** — solo `os.walk`/`glob` en su propio proceso | ✅ imposible |
| `check-blocks` · `check-health` · `grade-block` | dentro del proceso | ✅ |
| Los 4 hooks | ❌ no | ✅ |
| `test-f0-f6` | sí, invoca validadores | ✅ **lock con `trap … EXIT INT TERM`** + reclama el lock si el dueño murió |
| `generate-metrics` | sí — **2 llamadas** | ✅ **`timeout=300` en ambas** |

> ✅ **Conclusión medida: hoy Mente OS v2 no puede dejar procesos zombie.** Cada punto donde nace
> un proceso tiene su mecanismo — `trap` en la batería, `timeout` en las métricas — y ambos fueron
> leídos, no supuestos.

**Y F1 no cambia esa superficie:** sustituye `glob` por `os.walk` **dentro de la misma función y
el mismo proceso**. No añade ni un `subprocess`, ni un hilo, ni un fichero de estado.

### ⛔ LO QUE ESTE PLAN SE PROHÍBE, precisamente por eso

| Prohibido | Por qué |
|---|---|
| **Paralelizar la batería** | crea bloques sonda en el árbol REAL (§3-C). Dos corridas se corrompen: es el fallo que Brian teme, literal |
| **Cachear entre ejecuciones** (fichero de índice en disco) | una caché en disco que envejece **perdona citas rotas de verdad** — el fallo del v1. La caché vive **en memoria y muere con el proceso** |
| **Quitar el lock o el timeout** | son lo que hoy impide los zombies |

⚠️ **El defecto de concurrencia que este plan NO arregla** (§3-D): `generate-metrics` publica
números de una corrida vieja si otra batería está viva. F1 lo hace **menos probable**, no
imposible. Independiente, abierto y registrado.

---

## 9 · ⛔ F2 y F3 CERRADAS — no aplazadas

Revisadas a petición de Brian (2026-08-05) **con los números medidos, no con los estimados**.

### 🔴 F2 · el motivo por el que la descarté era FALSO — y eso importa más que la conclusión

**Lo que afirmé:** *"la batería llama a `check-links` 5 veces"*.
**Cómo lo "medí":** `grep -c check-links bin/test-f0-f6` → 5.
**Lo real:** **UNA sola invocación** (línea 1271). Las otras 4 son **menciones en comentarios**
(líneas 1265, 1278, 1365, 1442).

> ⭐ **`grep -c` cuenta cadenas, no ejecuciones.** Un número que parece medición y es una
> coincidencia de texto — el defecto exacto que `rules/rule-checks-must-measure.md` persigue,
> cometido por mí al justificar una decisión. **La conclusión aguanta, el razonamiento no.**

**F2 se cierra porque no hay nada que quitar**, no porque el ahorro fuera pequeño.

### F3 · el número exacto

```
generate-metrics 13.5s = batería 15.07s(*) + check-links 0.58s
                         (*) medido aparte; el total real es menor por solapes de E/S
```

F3 ahorraría **0.58s de 13.5s = 4%**, tocando el archivo que publica todos los números vivos.

⛔ **Y hay una razón mejor que el ahorro para NO hacerla:** si `generate-metrics` leyera el
resultado de la batería en vez de medirlo, **dejaría de ser una medición independiente**. Hoy son
dos mediciones que se contrastan — y esta sesión ya demostró que ese contraste caza desfases.

`principles/expertise/doc-planning.md` §2.6: *una fase que no cambia el resultado final es relleno*.

---

## 10 · EL ORDEN, Y POR QUÉ ESE

1. **F0 primero porque no toca nada.** Es la única fase que puede matar el plan, y cuesta minutos.
2. **F1 después porque es el 88% de la ganancia.** Con F1 hecho, F2 y F3 pueden dejar de valer la pena.
3. **F2 y F3 se reevalúan con el número de F1 en la mano** — no se prometen. Un plan que promete
   fases que quizá sobren es un plan con relleno (`principles/expertise/doc-planning.md` §2.6).
4. **F4 al final, siempre.** Es la única fase que mide el sistema **haciendo su trabajo**, no una
   pieza aislada. La primera versión de este plan no la tenía: medía `check-links` y daba por
   supuesto el resto. Brian lo señaló, y §2 es lo que salió de medirlo.

---

## 11 · 🙋 LO QUE DECIDE BRIAN

| Decisión | Opciones |
|---|---|
| **¿Se ejecuta F0?** | es la única que no toca nada — sin ella no hay evidencia para lo demás |
| **Si F0 da `diff > 0`** | ⛔ el plan se detiene y se reporta cada diferencia. **No se "arregla" el índice para que coincida** — eso sería ajustar la medición al resultado deseado |
| **F2 y F3** | se aprueban **después**, con el número de F1 medido — pueden sobrar |
| **F4 no se salta** | es la batería §5-BIS del sistema completo. Un plan que acelera y no verifica lo demás es el fallo del v1 con otra cara |

---

Related: `principles/expertise/doc-planning.md` (el criterio con el que se juzga este plan) ·
`principles/expertise/val-functional.md` §2.2 (qué cuenta como prueba) ·
`principles/expertise/val-integration.md` §2.1 (revertible sin tocar consumidores) ·
`bin/check-links` (la pieza) · `docs/METRICS.md` (donde vive el número).
