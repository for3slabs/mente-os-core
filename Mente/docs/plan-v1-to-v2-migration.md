# PLAN · migración completa v1 → v2

**Status:** current · **Type:** plan · **Updated:** 2026-07-30 · **Owner:** brian
**Aprobado por Brian:** 2026-07-30 (ADR-029) · **Precede a:** el renombrado de los 208 archivos
---

## Purpose

Sacar el sistema de la estructura v1 y dejarlo entero en v2. **Archivo por archivo**, encontrando
los errores de cada uno y decidiendo dónde encaja — no un `git mv` masivo.

> **Brian, 2026-07-30:** *"sigo viendo que estamos ocupando v1"* — y tiene razón: **el 72% de los
> documentos vive en carpetas v1.**

---

## 0 · EL TERRENO — medido 2026-07-30, no estimado

| Carpeta v1 | Docs | Sin cabecera de contrato |
|---|---|---|
| `Cuerpo/` | 85 | 84 |
| `Doc/` | 75 | 74 |
| `Alma/` | 7 | 7 |
| `Maestro/` | 7 | 7 |
| `Cerebro/` | 6 | 6 |
| `Tickets/` | 6 | 6 |
| **TOTAL** | **186** | **184** |

### 🔴 El número que gobierna este plan

```
1,586 citas a documentos v1, repartidas en 209 documentos
```

**Mover un archivo no es mover un archivo: es reescribir sus citas.** Los 8 más citados:

| Citas | Documento |
|---|---|
| 80 | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| 72 | `memory/PENDIENTES.md` |
| 66 | `docs/Arquitectura_Mente_OS_v2_Bloques.md` |
| 63 | `memory/RETOMAR.md` |
| 59 | `memory/archive/README.md` |
| 48 | `memory/Estado_Sesion_Continuidad.md` |
| 41 | `Maestro/registro.md` |
| 23 | `vision/Primeros_Pasos.md` |

⚠️ **Dos veces el 2026-07-30 un barrido masivo de rutas rompió citas reales** — 4 nombres
corrompidos dentro de `Maestro/` y 28 rutas relativas válidas "completadas" a absolutas
inexistentes. **Este plan existe para que no haya una tercera.**

---

## 1 · EL MAPA — dónde encaja cada carpeta

| v1 | → v2 | Docs | Criterio |
|---|---|---|---|
| `Alma/` | **`vision/`** | 7 | el porqué estratégico |
| `Cuerpo/` | **`work/`** + algunos a `rules/` | 85 | rondas y planes ejecutados |
| `Doc/` | **`memory/`** + algunos a `docs/` | 75 | ver §2 — es la más mezclada |
| `Maestro/` | **`registry/`** | 7 | ⚠️ **repo aparte** — ver §4 |
| `Tickets/` | **`bridges/`** | 6 | `rules/NAMING_CONVENTION.md` §57 |
| `Cerebro/` | ⛔ **NO se migra** | 6 | ver abajo |

### ⛔ Por qué `Cerebro/` NO se toca

`Cerebro/For3s_OS_Grafo_Maestro.md` es la **fuente de verdad arquitectónica de For3s OS** — el
producto, no el método. `Mente OS` es cómo se trabaja; `For3s OS` es lo que se construye.
**Mezclarlos es peor que la inconsistencia de nombres.**

Excepción: `Cerebro/Registro_Conversaciones.md` es de Mente OS (la regla del `/clear` lo exige)
→ evaluar en la fase M4.

---

## 2 · `Doc/` — la más mezclada, clasificada archivo por archivo

75 documentos que NO son una sola cosa:

| Qué es | Docs | Destino | Tipo declarado |
|---|---|---|---|
| 🔴 **arranque** — `memory/RETOMAR.md` | 1 | queda donde está | `entry-point` |
| 📌 **memoria viva** — `PENDIENTES` · `Bitacora_Progreso` · `Estado_Sesion_Continuidad` | 3 | `memory/` | `append-only` |
| 🔬 **análisis** — `Analisis_*` `Comparacion_*` `Reporte_*` `Examen_*` | 25 | `docs/analysis/` | `analysis` |
| 📋 **rondas e informes** — `Carril_*` `Changelog_*` `PR*` `Entrenamiento_*` | 17 | `work/` | `analysis` |
| 📸 **snapshots** | 1 | `memory/archive/` | `fossil` |
| ⚪ **fósil** — `memory/archive/README.md` (ya superseded) | 1 | `memory/archive/` | `fossil` |
| ❓ **por clasificar** | 27 | ⬜ **uno por uno** | ⬜ |

⭐ **Los 27 "por clasificar" son el corazón del trabajo.** Cada uno necesita leerse para decidir si
es análisis, ronda, fósil o algo que ya no aplica. **No se clasifican por el nombre** — ese fue el
error que dejó tres documentos de For3s OS dentro de `marca-personal/Mente`.

---

## 3 · LAS FASES — de menos a más riesgo

> ⭐ **Regla de orden:** primero lo que nadie cita, al final lo que citan 80 veces. Cada fase deja
> el sistema en verde antes de la siguiente.

### M0 · El candado (antes de mover nada)

| | |
|---|---|
| **M0-1** | `bin/check-links` — verifica que **toda** cita interna resuelva. Hoy esa verificación vive dentro de `bin/test-f0-f6`; se saca a su propio validador para poder correrla tras **cada** archivo |
| **M0-2** | ✅ **HECHO** — `bin/migrate-doc`: `git mv` + cabecera + reescribe las citas en sus 4 formas + verifica + **revierte si rompe** |
| **M0-3** | ✅ **Línea base congelada 2026-07-30: 59 citas rotas** — ver abajo |

### ✅ M0-1 y M0-3 HECHOS (2026-07-30)

`bin/check-links` construido y calibrado. **Calibrarlo fue el trabajo real**: la primera versión
reportaba **775 citas rotas**, de las cuales **casi ninguna era un defecto**.

| Se descartó | Por qué NO es un enlace roto | Cuántas |
|---|---|---|
| nombres sueltos que existen en otra carpeta | es una ruta **ambigua**, y `bin/check-blocks` ya lo reporta como 🟡 | 266 |
| documentos que describen OTROS sistemas | `Radiografia_Fruterito_*` describe OpenClaw, `Hermes_*` describe Hermes: esos nombres son el **sujeto**, no un enlace | 284 |
| archivos `.py`/`.sh`/`.json` | viven en el repo del agente. Citar `conversation.py` es nombrar un módulo | 85 |
| `docs/INDEX.md`, `docs/STATES.md` | los **genera** F7 | — |
| URLs y rutas absolutas | no son rutas del sistema | — |

> ⭐ **Un validador que reporta 775 no-defectos es un validador que nadie lee.** La misma regla que
> hizo bajar los falsos positivos del solapamiento de scope.

**🔴 LÍNEA BASE: 56 citas rotas REALES** — apuntan a documentos que no existen en ninguna parte
(`Cerebro_Humano_acercamiento3.md`, `spec-quality-verdict.md`, `pointers.tsv`…).
**Esa es la deuda de partida.** Si al terminar la migración hay más de 56, la migración rompió algo.

**Cierra cuando:** `bin/migrate-doc` mueve un archivo de prueba y lo revierte sin dejar rastro.

> ✅ **M0 CERRADO 2026-07-30.** Probado en ambas direcciones: mueve y verifica · y ante una ruptura
> forzada **revirtió el archivo a su origen sin dejar rastro**.
>
> 🔴 **Y la prueba de reversa enseñó algo que casi cuesta caro:** la primera versión revertía con
> `git checkout -- .` — que deshace **TODO lo no commiteado**, incluidos `bin/` y `hooks/`.
> Tumbó silenciosamente los fixes de **6 validadores** (`grade-block`, `check-health`,
> `check-blocks`, `check-sufficiency`, `pre-commit`, y el bloque demo). La batería pasó de 103/103
> a **13 fallos**, y hubo que restaurarlos uno por uno.
>
> ⭐ **La regla que quedó: un revert debe ser tan estrecho como el cambio.** `migrate-doc` ahora
> revierte **solo los `.md` que tocó** — nunca código, nunca algo que no movió.

### M1 · Los fósiles — ✅ **CERRADO 2026-07-30**

**145 documentos movidos**, ninguno renombrado. `Alma/` quedó vacía.

| Destino | Docs |
|---|---|
| `work/` | 76 |
| `memory/archive/` | 35 |
| `docs/analysis/` | 22 |
| `vision/` | 7 |
| `bridges/` | 5 |

🔴 **Corrección al plan: NO eran 157 con cero citas — eran 13.** Los otros 143 se citaban **entre
ellos**. `bin/migrate-doc` los reescribió, pero el riesgo era mayor que el estimado.

### ⭐ Los 6 hallazgos de M1 — todos del validador, ninguno de leer

| # | Hallazgo |
|---|---|
| 1 | **La deuda que un documento YA traía no la causó la migración.** `migrate-doc` comparaba el total global y revertía todo archivo con citas rotas preexistentes — 3 de los primeros 40. Ahora juzga **lo que el movimiento rompe, no lo que hereda** |
| 2 | **La exención sigue al DOCUMENTO, no a la carpeta.** Una radiografía de OpenClaw sigue describiendo OpenClaw después de moverse; al salir de `Doc/` sus citas se volvían falsos positivos y `migrate-doc` la revertía para siempre |
| 3 | **El índice generado no se audita a sí mismo.** Entre un movimiento y el siguiente `generate-index`, `docs/INDEX.md` nombra rutas viejas: eso es retraso del generador, no un defecto |
| 4 | **La cabecera se reconoce por `**Type:**`, no por `Status`.** 16 documentos ya usaban `**Status:**` con otro significado (*"3/3 sub-temas LOCKED"*) y quedaron sin tipo |
| 5 | ⭐ **Un documento histórico no se parte: se marca `fossil`.** 50 pasaban de 300 líneas con tipo `analysis`. Partir un registro de lo que pasó **lo falsea** |
| 6 | **Un fósil se consulta, no se mantiene.** Exigirle Purpose/Related a 156 archivados es trabajo que nadie leerá — y 67 warnings que nadie atiende es cómo un validador se vuelve ruido |

**Línea base de citas rotas: 56 → 73.** Las que subieron son deudas preexistentes que las carpetas
legacy ocultaban: **la migración no las creó, las destapó.**

### M2 · `Tickets/` y `Alma/` — ✅ **CERRADO 2026-07-30**

M1 ya se había llevado casi todo. M2 movió los **4 restantes** y **borró las dos carpetas**:

| Qué | Destino |
|---|---|
| `work/SPIKE_OpenCode_segundo_proveedor.md` | `work/` — es investigación, no un puente |
| 3 binarios (`.docx`, 2 `.html`) | `vision/assets/` |

🗑️ **`Alma/` y `Tickets/` ELIMINADAS.** Dos carpetas v1 menos.

### ⭐ Los 3 hallazgos de M2

| # | Hallazgo |
|---|---|
| 1 | **`migrate-doc` solo maneja `.md`.** Los 3 binarios (150 KB de `.docx` y `.html`) fueron con `git mv` + actualización manual de citas. El plan no contemplaba archivos que no son documentos |
| 2 | 🔴 **Punto ciego del candado:** las carpetas creadas en M1 (`vision/` `work/` `memory/` `bridges/`) **no estaban en la lista auditada** — una cita rota dentro de ellas pasaba desapercibida. Justo donde la migración deja cada archivo. Probado: ahora se detecta |
| 3 | **Colisión de nombre:** `memory/<fecha>.md` son los diarios de **OpenClaw**, no de nuestra `memory/` nueva. Elegir ese nombre en M1 creó falsos positivos que hubo que distinguir |

**Carpetas v1 restantes: `Cerebro/` (6, se queda) · `Cuerpo/` (9) · `Doc/` (18) · `Maestro/` (7).**

### M3 · `Doc/` — ✅ **CERRADO 2026-07-30**

M1 y M2 ya se habían llevado 57. M3 movió **13 de los 18 restantes**, leídos uno por uno.

| Destino | Docs | Ejemplos |
|---|---|---|
| `docs/analysis/` | 6 | los 2 análisis de internOS · comparativa Hermes · examen Foresito · `For3s_OS_En_Bloques` |
| `work/` | 5 | los 3 carriles · los 2 de entrenamiento |
| `vision/` | 1 | `vision/Primeros_Pasos.md` — documento fundacional del 28-may |
| `bridges/` | 1 | ⭐ `bridges/Puentes_Mente_OS.md` — **el gate**, y `bridges/` es literalmente su nombre |
| `memory/archive/` | 1 | el snapshot del 7-jul |

**`Doc/` pasó de 75 → 5 documentos.**

### ⭐ Los 3 hallazgos de M3

| # | Hallazgo |
|---|---|
| 1 | ⭐ **`Maestro/piezas.tsv` hizo su trabajo:** al mover el gate, `check-structure` lo reclamó de inmediato. **Una línea cambiada y todo siguió** — que era exactamente la promesa del sistema de apuntado |
| 2 | 🔴 **El revert restauraba a HEAD archivos migrados en un lote ANTERIOR**, deshaciendo ese trabajo en silencio. Costó 16 cabeceras. `migrate-doc` ahora **respeta lo ya migrado**: no revierte un archivo cuyo estado actual lleva rastro de migración y HEAD no |
| 3 | **`memory/archive/README.md` es de riesgo M5, no M3:** medido, **85 citas en 23 documentos**. Revirtió correctamente y se dejó para su fase |

**Los 5 que quedan en `Doc/` son todos de M5** — la memoria viva y el punto de entrada:
`memory/RETOMAR.md` (26 citas) · `memory/PENDIENTES.md` (38) · `memory/Estado_Sesion_Continuidad.md` (22) ·
`memory/archive/README.md` (85) · `memory/Bitacora_Progreso.md` (11).

### M4 · `Cuerpo/` (85 docs) — el volumen

El grueso. Las `Ronda_*` a `work/`, las que son regla (`rules/ESTANDAR_Metodo_Fases_F.md`) a `rules/`.
⚠️ `Cuerpo/architecture/` **ya es v2** — solo cambia la carpeta contenedora.

### M5 · Los 5 más citados — ✅ **CERRADO 2026-07-30**

**463 citas reescritas** en el orden previsto: de menor a mayor riesgo, `RETOMAR.md` al final.

| # | Documento | Citas | Destino |
|---|---|---|---|
| 1 | `memory/Bitacora_Progreso.md` | 32 | `memory/` |
| 2 | `memory/Estado_Sesion_Continuidad.md` | 110 | `memory/` |
| 3 | `README.md` | 87 | `memory/archive/` — ya superseded en F7 |
| 4 | `memory/PENDIENTES.md` | 138 | `memory/` |
| 5 | ⭐ `RETOMAR.md` | 106 | `memory/` — **el punto de entrada** |

🗑️ **`Doc/` ELIMINADA.** Cuarta y última carpeta v1 de documentos.

**Arranque verificado:** `CLAUDE.md` → `Mente/memory/RETOMAR.md` ✅ · el archivo existe ✅ ·
`Maestro/punteros.tsv` (que lee Foresito por MCP) actualizado ✅.

### ⭐ Los 4 hallazgos de M5 — el más importante de toda la migración

| # | Hallazgo |
|---|---|
| 1 | 🔴🔴 **`migrate-doc` comparaba TOTALES, no conjuntos.** Reportaba 30 citas rotas cuando el movimiento solo añadía 1 — y revertía por deuda que el documento ya traía. `README.md` revirtió **tres veces** por esto. Ahora compara el **conjunto de pares (archivo, cita)** y responde la única pregunta que importa: *¿qué añadió ESTE movimiento?* |
| 2 | 🔴 **`migrate-doc` no veía fuera de `Mente/`.** `CLAUDE.md` y `PROJECT-RULES.md` viven en la raíz del proyecto y son **lo que se inyecta en cada sesión**. Mover `memory/Estado_Sesion_Continuidad.md` dejó la regla de arranque *"NO leer ese archivo"* apuntando a la nada |
| 3 | ⭐ **El aviso que salvó el arranque:** al mover `RETOMAR.md`, el validador reportó `pointers.tsv`. Investigado, era real — **`Maestro/punteros.tsv` apuntaba a `Doc/RETOMAR.md`**, y lo lee Foresito EN VIVO por MCP. Sin ese aviso, el índice de la rama `for3s` habría quedado roto en producción |
| 4 | **Corrupciones zombi:** dos rutas malas volvieron **cuatro veces** — cada revert restaura la versión de HEAD que las contiene. Ya son un check permanente de la batería; mueren de verdad al commitear |

### M6 · `Maestro/` — 🟡 **RENOMBRE SUSPENDIDO · deuda real CERRADA (2026-07-30)**

Brian aprobó el renombre en ADR-029. **Al medir el terreno aparecieron 3 hechos que no estaban
sobre la mesa cuando decidió** — se los reporto en vez de ejecutar a ciegas:

| # | Lo medido | Por qué cambia la decisión |
|---|---|---|
| 1 | El repo remoto se llama **`mente-os-maestro`** | Renombrar la carpeta local **no cambia GitHub**. Quedaría `registry/` apuntando a `mente-os-maestro.git` — **dos nombres para lo mismo**, peor que la inconsistencia actual |
| 2 | `Maestro/` **no es una carpeta de Mente OS: es otro sistema** | Los otros 4 renombres movían documentos dentro del mismo repo. Este mueve el punto de montaje de un repo con vida propia |
| 3 | El nombre está en su **identidad**, no en su ruta | Sus documentos dicen *"el Mente OS Maestro"*, el script se llama `maestro`, la librería `Maestro/maestro_lib.sh`. Renombrar solo la carpeta deja el sistema hablando de algo que ya no existe |

> ⭐ **Renombrarlo bien no es mover una carpeta: es renombrar un sistema entero** — repo remoto,
> comando, librería y documentos. Eso es un bloque propio, no la última fase de esta migración.

### ✅ Lo que SÍ era deuda real, y quedó cerrado

🔴 **`Maestro/indexador.py` estaba roto.** Su regex buscaba `Alma|Cerebro|Cuerpo|Doc|Maestro` — y tres de
esas carpetas **fueron eliminadas** en M1-M5. **El indexador no encontraba NADA de la estructura
v2, y Foresito lee su salida EN VIVO por MCP.**

Ahora busca las carpetas que existen: `vision · work · rules · docs · memory · bridges ·
principles · blocks · Cerebro · Maestro`. Verificado con rutas reales de las 3 clases.

**Los 3 consumidores resuelven su ruta con `dirname`** — no dependen del nombre de la carpeta, así
que un renombre futuro no los rompería. Eso queda medido para cuando se decida.

---

## 4 · ✅ LAS 4 DECISIONES — resueltas por Brian 2026-07-30 (ADR-029)

| # | Decisión | Resuelto |
|---|---|---|
| **1** | `Maestro/` → `registry/` | 🟡 **SUSPENDIDO tras medir** — el repo REMOTO se llama `mente-os-maestro`; renombrar solo la carpeta crea dos nombres para lo mismo. Es un bloque propio (renombrar un sistema), no una fase de esta migración. **Decisión de Brian pendiente** |
| **2** | `Cerebro/` | ✅ **SE QUEDA.** Es la verdad arquitectónica de **For3s OS** (el producto), no de Mente OS (el método) |
| **3** | Los 157 fósiles | ✅ **SE ARCHIVAN, no se borran.** Son la historia del proyecto, y **conservan su nombre**: un fósil renombrado pierde su trazabilidad |
| **4** | Traducir nombres al inglés | ✅ **NO en esta migración.** Mover y renombrar a la vez duplica el riesgo sobre los mismos archivos. El renombrado de 208 sigue siendo un bloque aparte |

---

## 5 · CÓMO SE VERIFICA CADA PASO

**Tras CADA archivo movido, no al final:**

```bash
bin/check-links          # 0 citas rotas — el candado
bin/check-structure      # el árbol sigue siendo el declarado
bin/generate-index       # los índices reflejan la realidad
bin/test-f0-f6           # 103/103
```

> ⭐ **La lección que hace este plan distinto de un `sed`** (aprendida dos veces el 2026-07-30):
> una reescritura masiva no es segura porque el mapeo esté bien — **es segura cuando algo verifica
> el resultado después.** Y **una ruta relativa que resuelve desde su propio directorio es
> correcta: completarla es el bug.**

---

## 6 · LO QUE NO HACE ESTE PLAN

⛔ **No renombra archivos al inglés** — es el pendiente de los 208, otro bloque.
⛔ **No reescribe contenido** — mueve y actualiza citas. Un movimiento que también edita hace
imposible distinguir un `mv` de un cambio en la revisión.
⛔ **No toca `marca-personal/Mente/`** ni `~/5M-incubathon/` — el gate sigue en pie.

---

## 7 · ESTIMACIÓN HONESTA

| Fase | Docs | Riesgo |
|---|---|---|
| M0 candado | — | 🟢 |
| M1 fósiles | 157 | 🟢 nadie los cita |
| M2 Tickets+Alma | 13 | 🟢 |
| M3 Doc/ | 75 | 🟡 27 requieren lectura individual |
| M4 Cuerpo/ | 85 | 🟡 volumen |
| M5 los 8 críticos | 8 | 🔴 1,586 citas |
| M6 Maestro/ | 7 | 🔴 repo aparte |

**No doy estimación en horas.** Lo que sí está medido: **186 documentos y 1,586 citas.** M1 es
mecánica; M5 es de uno en uno con verificación entre cada paso.

---

Related: `rules/NAMING_CONVENTION.md` (los nombres destino) ·
`rules/decisions/ADR-008-migration-on-demand.md` (la regla que este plan supera) ·
`docs/plan-v2-rollout.md` · `memory/PENDIENTES.md` (el renombrado de 208).
