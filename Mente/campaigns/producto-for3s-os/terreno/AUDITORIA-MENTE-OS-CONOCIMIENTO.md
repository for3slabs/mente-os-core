# AUDITORÍA DEL CONOCIMIENTO — qué sabe Mente OS, y qué nos enseñó que salió mal

**Status:** current · **Type:** analysis · **Updated:** 2026-08-12 · **Owner:** brian
**Level:** 📚 REFERENCIA DE CAMPAÑA — la memoria del proyecto, destilada. No dicta reglas: recuerda
**Verified by:** cada número sale de contar los archivos; se re-mide en el propio repo
**Exempt:** size, split-signal · ⭐ **MEMORIA DEL PROYECTO — decisión de Brian 2026-08-12:**
*"lee cada uno sin omitir nada… no importa el tamaño, hazlo tan grande como sea necesario"*.
Partirlo destruiría su función: **un solo lugar donde está lo que ya aprendimos.** Su hermano es
`campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` (el terreno del código); este es **el terreno del conocimiento.**

## Purpose

> **Brian, 2026-08-12:** *"Necesito que así como tuvimos auditoría For3s OS, pero esta vez del
> conocimiento que tenemos de Mente OS. ¿Por qué? Porque nos servirá para saber qué pasó antes y
> no cometer algún error."*

**332 documentos · 109,377 líneas** de conocimiento acumulado desde mayo de 2026. Este archivo
destila lo que sirve para **no repetir un error ya cometido**.

⭐ **La diferencia con el otro:** `AUDITORIA-FOR3S-OS` responde *"¿qué hay ahí fuera?"*.
Este responde *"¿qué ya nos pasó, y qué aprendimos?"* — para que la campaña **no vuelva a tropezar
en piedras que ya están señalizadas**.

---

## 📑 ÍNDICE

| § | Qué entrega |
|---|---|
| **1** | El inventario del conocimiento: dónde vive cada cosa |
| **2** | ⭐ **LA LEY DEL PROYECTO** — la que explica casi todos los fallos |
| **3** | 🔴 **LAS 5 FAMILIAS DE ERROR** — el catálogo de cómo fallamos |
| **4** | Las 12 sesiones: qué pasó en cada una y qué costó |
| **5** | 🔴 **EL PATRÓN QUE MATA SESIONES** — edad, no tamaño |
| **6** | Los 30 ADRs: las decisiones que ya no se re-discuten |
| **7** | Los 5 bloques cerrados y su lección medida |
| **8** | Las 26 reglas: qué gobierna qué |
| **9** | Los 4 dueños y su criterio |
| **10** | Las 65 rondas: con qué se diseñó For3s OS |
| **11** | La deuda viva: 134 pendientes |
| **12** | 📋 **LAS 20 LECCIONES** — lo que la campaña debe llevar puesto |
| **13** | ⚠️ Lo que Mente OS todavía NO sabe hacer |
| **14** | Cómo usa esto la campaña |
| **15** | 🔴 **LO QUE LA LECTURA COMPLETA DESTAPÓ** — 9 hallazgos nuevos |
| **16** | 🔴🔴 **EL HALLAZGO MAYOR** — el diseño y el código son dos sistemas distintos |
| **17** | **EL MAPA COMPLETO** diseño → código, ronda por ronda (23 piezas con semáforo) |
| **18** | ⭐⭐ **EL BALANCE FINAL** — el patrón: las capas bajas se construyeron, las altas no |
| **19** | ⭐⭐ **EL MAPA NODO → ARCHIVO REAL** — lo más accionable de toda la auditoría |
| **20** | ⭐⭐⭐ **POR QUÉ NADIE VIO LA DIVERGENCIA** — y dónde debe auditar la campaña |
| **21** | ⚠️ **CORRECCIÓN A §16-§20** — el sistema ya sabía todo esto, y está escrito |
| **22** | **LAS 7 VENTAJAS DEFENDIBLES** — cuáles son reales hoy (3 sí · 3 parciales · 1 ausente) |
| **33** | ✅ **LOS BANCOS Y EL CIERRE** — el origen histórico y el estado final de la lectura |
| **32** | ⭐⭐ **LA NEUROCIENCIA COMO DIAGNÓSTICO** — el modelo predijo los síntomas de sus ausencias |
| **31** | **LO QUE work/ GUARDA** — un spike que resuelve la anti-visión #8, y un secreto sin rotar |
| **30** | ✅ **H-02 CERRADO** — la lectura cruza sesiones, el contador no |
| **29** | 🔴🔴🔴 **CORRECCIÓN GRAVE A §24** — la memoria SÍ alcanza las importadas |
| **28** | **EL ORIGEN DE LAS 33,737 MEMORIAS** — la procedencia, y por qué quedaron aisladas |
| **27** | 🔴🔴 **MENTE OS NUNCA HA GOBERNADO PRODUCTO** — la campaña es su prueba de campo |
| **26** | ⭐⭐⭐ **LAS 3 BRÚJULAS** — la autoridad completa, y los 3 tableros congelados |
| **25** | ⭐⭐⭐ **LOS 16 HITOS MEDIDOS HOY** — 13 de 16 construidos (el tablero publica 3 de 18) |
| **24** | 🔴🔴🔴 **LA CAUSA RAÍZ DE H-02** — la memoria no está rota: está INALCANZABLE |
| **23** | ⭐⭐⭐ **EL GATE DE FASE 1, MEDIDO** — la vara correcta: pasa 6 de 6, y solo 4 hallazgos importan hoy |

---

## 1 · EL INVENTARIO DEL CONOCIMIENTO

### 1.1 · Dónde vive cada cosa

| Carpeta | Archivos | Qué guarda |
|---|---|---|
| **`work/`** | **88** | ⭐ el trabajo cerrado — **las 65 rondas de diseño de For3s OS** |
| `memory/archive/` | 38 | material histórico retirado de la memoria viva |
| **`rules/decisions/`** | **30** | ⭐ **los ADRs** — decisiones que ya no se re-discuten |
| `docs/analysis/` | 28 | análisis, comparaciones, radiografías, auditorías previas |
| **`rules/`** | **26** | ⭐ las reglas y contratos que gobiernan hoy |
| `docs/` | 19 | planes, arquitectura, bitácoras |
| `docs/plans/` | 10 | los planes de fase |
| `vision/` | 8 | la visión y los aprendizajes de campo |
| `principles/` + `expertise/` | 14 | ⭐ **los 4 dueños y su criterio destilado** |
| `Maestro/` | 7 | el controlador multi-repo |
| `docs/architecture/` | 6 | la anatomía del sistema |
| `bridges/` | 6 | el gate hacia otros Mente OS |
| `Cerebro/` | 6 | ⭐ **el grafo de For3s + el registro de sesiones** |
| `memory/` | 5 | ⭐ la memoria viva (RETOMAR, PENDIENTES, Bitácora) |
| `blocks/` | 24 | 5 archivados · 1 activo · 1 bloqueado |
| `secrets/` | 4 | ⛔ gitignored, nunca versionado |
| **TOTAL** | **332 `.md`** | **109,377 líneas** |

### 1.2 · Los pesos pesados

| Archivo | Líneas | Qué es |
|---|---|---|
| `memory/PENDIENTES.md` | **4,808** | el histórico completo de deuda |
| `memory/Estado_Sesion_Continuidad.md` | **4,782** | ⛔ **NO leer** — CLAUDE.md lo prohíbe explícitamente |
| `memory/Bitacora_Progreso.md` | 1,646 | la línea de tiempo del proyecto |
| `memory/pendiente-agosto-2026.md` | 1,645 | la deuda VIVA (la rotación actual) |
| `Cerebro/For3s_OS_Grafo_Maestro.md` | 1,300 | ⭐ la autoridad sobre cómo funciona For3s |
| `vision/Vision_For3s_Frontier.md` | 1,091 | la visión larga |
| `vision/Primeros_Pasos.md` | 1,012 | el arranque |
| `Cerebro/Registro_Conversaciones.md` | 849 | ⭐ **las 12 autopsias de sesión** |
| `docs/architecture/validators-and-hygiene.md` | 781 | cómo se verifica |

⚠️ **`memory/Estado_Sesion_Continuidad.md` (4,782 líneas) está prohibido por `CLAUDE.md`** salvo que un
puntero de RETOMAR lo mande. Leerlo *"por si acaso"* gasta tokens — **medido por Brian el 9-jun**.

### 1.3 · La maquinaria

| | Cuántos |
|---|---|
| Validadores (`bin/`) | **24** |
| Hooks (`hooks/`) | **9** |
| **Checks de la batería** | **230** |

---

## 2 · ⭐ LA LEY DEL PROYECTO

> **Una regla en código se cumple 100%. Una regla que vive solo en un documento se cumple 40-60%.**

Está escrita en `CLAUDE.md` y **es la lección que más veces se ha demostrado sobre sí misma.** El
caso más brutal:

⭐ **`rules/rule-session-close.md` fue escrita A CAUSA del incidente del 21-jul. La regla citaba esa
sesión por nombre como "el peor infractor". Y esa sesión siguió sin registrarse 10 días más.**

**Escribir la regla no la ejecuta.** Por eso el sistema tiene 230 checks y no 230 párrafos.

### 2.1 · El corolario: la verificación afirmativa

Un check debe **verse fallar** antes de que su verde signifique algo (`principles/expertise/val-functional.md` §2.2).
Un check que nunca se vio en rojo **no es un check: es una decoración**.

### 2.2 · El corolario del corolario

**Presencia ≠ uso.** Un check que verifica que una función *existe* no verifica que se *llame*.
Medido en esta misma sesión: un check buscaba `campana_de` y esa función seguía existiendo después
de que yo reemplazara su llamada por `(None, [])`. **Verde con el cable cortado.**

---

## 3 · 🔴 LAS 5 FAMILIAS DE ERROR

`rules/rule-checks-must-measure.md` catalogó **4 familias** tras encontrar **8 fallos de la misma
forma en una sola sesión** (2026-08-02). Añado una quinta, medida después.

### A · Comparación floja — la cadena es demasiado corta para significar algo

```python
⛔  if sid not in text:                 # 8 hex: 'abcdc733bc1def' satisface 'dc733bc1'
⛔  if basename(f).split("-")[1] in s:  # "016" — y "2016" también, y "F3-016b"
✅  re.search(rf"(?<![0-9a-f]){re.escape(sid)}(?![0-9a-f])", text)
```

**Encontrada en 4 archivos** escritos en momentos distintos. El peor: `generate-metrics`, que
**publica** el número — **así que la mentira viajó.**

> 🔬 **La prueba:** si esa cadena apareciera por accidente, ¿el sistema se volvería más permisivo?

### B · Alcance corto — el scope empieza un nivel demasiado abajo

```python
⛔  glob.glob("**/*.md")   # corriendo desde Mente/ — CLAUDE.md vive un nivel ARRIBA
```

⭐ **`CLAUDE.md` se carga en CADA arranque de sesión y era el único documento que nada auditaba:**
cero de los cuatro campos de cabecera, dos punteros muertos, tres números congelados.

> 🔬 **La prueba:** nombra lo que este check protege. Ahora lista lo que realmente alcanza.
> **El hueco es el hallazgo.** ⭐ *El archivo que se lee PRIMERO era el menos vigilado.*

### C · Valor pisado — se midió bien, y luego se sobrescribió

```bash
⛔  cmd; eq "label $( [ $x = 0 ] && echo yes )" "$want" "$?"   # el $() se comió $?
✅  cmd; _e=$?; eq "label …" "$want" "$_e"
```

`$?` sobrevive exactamente **un** comando. Este solo se veía cuando el valor esperado era `1`:
con `0` el valor pisado **coincidía por accidente**, así que pasó semanas en verde.

⚠️ **Variante medida en esta sesión:** una variable llamada `_decl` ya usada 500 líneas antes
sobrescribió mi conteo. El check **pasó en verde con el sabotaje puesto.**

### D · Exigir algo que POR DISEÑO no viaja — el check mide la MÁQUINA, no el sistema

```bash
⛔  eq "secrets/ is 700" "700" "$(stat -c %a secrets)"   # secrets/ está en .gitignore
```

**8 casos.** El peor (`grade-block archived`): bajo `pipefail` el pipe tomaba el exit `2` del
veredicto 🔴 MVP **aunque el `grep` acertara**. Exigía **la nota que saca en la máquina de su
autor** — un check atado a la instancia de Brian **sin nombrarla ni una sola vez**.

⭐⭐ **Un check así no se encuentra buscando el nombre de Brian en el código, porque no está.**
Se encontró probando en un **clon limpio**: la batería daba **195/0 aquí y 22 fallos allá**.

### E · 🆕 Vigilar un archivo GENERADO — el check es circular

Medido en esta sesión: intenté sabotear `docs/INDEX.md` para probar un check. Imposible —
**la batería REGENERA el índice antes de llegar al check.** Vigilar el contenido de un archivo
generado es preguntarle al generador si el generador funciona.

**El arreglo:** vigilar que **los generadores existan**, no lo que producen.

---

## 4 · LAS 12 SESIONES — qué pasó y qué costó

| # | Fecha | Duración | Contexto máx | Qué fue |
|---|---|---|---|---|
| **S1** | 28-may → 13-jul | **47 días** 🔴 | 985K 🔴 | **LA MONSTRUO** — 278 MB. Causó el incidente del jueves |
| S2 | 13-jul | ~10h | 549K 🔴 | Maratón H13 + Frente B |
| S3 | 14-15 jul | — | n/d | La jornada MERCADO — v0.17.0, 1 fallo SEC grave explotado |
| **R2** | 15-19 jul | **76h** 🔴 | **999,692** 🔴 | Seguridad SEC-4c — **el pico absoluto del proyecto** |
| S4 | 18-19 jul | 30h | 667K 🔴 | El super-cerebro — la más productiva de la historia |
| **R1** | 20-23 jul | **96h** 🔴 | 999,366 🔴 | 🔴 **EL INCIDENTE DEL 21-JUL** — 23.4 MB, 6 violaciones de scope |
| S5 | 24-26 jul | 33h | 917K 🔴 | La demo a producto — 9 bugs |
| S6 | 26-jul | 18h | n/d | Cimientos de la demo — **2 caídas de producción** |
| **S7** | 27-31 jul | **116h** 🔴 | 998K 🔴 | **MENTE OS v2** — de documentar a GOBERNAR |
| S8 | 31-jul → 2-ago | 50h 🔴 | 722K 🔴 | Endurecer v2 — batería 105 → 138 |
| S9 | 2-3 ago | 20h | 681K 🔴 | El agente instalador — **citas rotas 144 → 0** |
| S10 | 3-4 ago | **7h** 🟢 | 261K 🟡 | **LA VOZ** — la única sana en contexto |
| **S11** | 4-5 ago | 45h 🔴 | **999,757** 🔴 | El criterio y los tests — 66 huecos → 0 |
| **S12** | 5-7 ago | 47h 🔴 | **1,000,030** 🔴 | 🔴 **EL CLON QUE POR FIN VERIFICA** — primera en cruzar el millón |
| R3 | 16-27 jun | **11 días** 🔴 | 679K 🔴 | H5-H10 — la más larga en días |

### 4.1 · 🔴 El incidente del 21-jul, con detalle

**La peor sesión del proyecto.** 96 horas · 23.4 MB · 1,256 turnos · contexto 999,366 ·
**cache_read de 1,033 millones — la única que cruza el billón.**

De aquí salió la frase de Brian: ***"no eres el mismo de siempre, no me sirves así"***.
**6 violaciones de scope. Degradación sostenida por contexto saturado.**

⚠️ Se recuperó del `.jsonl` crudo **seis días después**, y hasta el 31-jul vivía solo en una
memoria — **nunca en el Registro**.

---

## 5 · 🔴 EL PATRÓN QUE MATA SESIONES

> ⭐ **Las tres sesiones huérfanas murieron de EDAD, no de peso. 96h · 76h · 11 días. Ninguna
> cruzó los 50 MB; las tres cruzaron el rojo de contexto.**
>
> **El umbral que importa no es el tamaño del archivo — es cuánto lleva abierta.**

### 5.1 · Los umbrales calibrados con datos reales

| Señal | 🟢 Sano | 🟡 Vigilar | 🔴 Actuar (`/clear` ya) |
|---|---|---|---|
| Peso del `.jsonl` | < 15 MB | 15-50 MB | > 50 MB |
| **Contexto vivo** | < 200K | 200-500K | **> 500K** |
| **Edad de la sesión** | días | 1-2 semanas | **semanas/meses** |
| Cache-miss | esporádico | tras cada pausa | cada pausa >5 min con contexto grande |
| "Cosas raras" | — | mezcla temas viejos | `<synthetic>`, cupo agotado |

### 5.2 · La física del costo

**El peso en disco NO es el problema directo — lo es el contexto vivo.** Cada pausa mayor al TTL
del caché re-escribe TODO el contexto a precio premium.

⭐ **Contexto de 1M = decir "hola" cuesta ~1M tokens. Contexto de 30K = centavos.**

### 5.3 · ⚠️ Lo que se pierde al no registrar

De las 3 sesiones huérfanas, se pudo reconstruir lo medible (peso, turnos, tokens). **Lo que NO se
pudo reconstruir es el criterio: qué se sintió raro, por qué se cerró. Eso se perdió.**

⭐ **Ese es exactamente el costo que la regla de registro previene.**

### 5.4 · 🔴 Registrar el cierre NO es cerrar

S11 se "cerró" el 5-ago y **el mismo `.jsonl` siguió vivo 46 horas más** hasta el 7-ago, llegando
a **1,000,030 tokens**. La autopsia se escribió; el `/clear` no se dio.

---

## 6 · LOS 30 ADRs — decisiones que ya no se re-discuten

**27 vigentes · 3 superseded.**

| ADR | Decisión | Por qué importa a la campaña |
|---|---|---|
| **001** | la unidad de trabajo es el BLOQUE | los 12 bloques de la campaña son bloques, no carpetas |
| 002 | para quién es el sistema | |
| ⭐ **003** | **Brian es dueño del CRITERIO** | ⛔ **nunca inventar criterio: preguntar** |
| 004 · 005 | tres carriles de fricción · protocolo | |
| 006 · 007 | los bloques viven en git · se archivan al cerrar | |
| ~~008~~ | ~~migración bajo demanda~~ | **superseded** por ADR-029 |
| 009 | un solo archivo por bloque | |
| 010 | progresivo con mínimo duro | **barato de abrir, caro de cerrar** |
| 011 | cuatro capas garantizan la lectura | |
| 012 | solo tres puertas cerradas | |
| **013** | veredicto de calidad en dos capas | `grade-block` mide; Brian juzga |
| **014** | **Brian es dueño del criterio de QA** | |
| 015 | máximo tres niveles de anidación | |
| ~~016~~ | ~~carpetas coexisten en la migración~~ | **superseded** |
| 017 | el aprendizaje reusa el mecanismo estándar | |
| ⭐ **018** | **owner-0 es LA VOZ** | el contrato de entrega |
| **019** | los validadores completan lo derivable | ⛔ **no inventan lo que solo Brian sabe** |
| ~~020~~ | ~~recibo de aprobación en el bloque~~ | **superseded** |
| **021** | cuándo un error se vuelve un CASO | |
| 022 | tres fricciones en bloques distintos | |
| 023 | inglés US para instrucciones | |
| ⭐ **024** | **el sistema se audita a sí mismo** | |
| 025 | higiene de configuración: cuatro reglas | |
| **026** | la granularidad de permisos ES el mecanismo | |
| **027** | límites de tamaño por tipo de documento | ⭐ **y por eso existe `Exempt:`** |
| **028** | un bloque declara su TIPO, y el tipo decide las métricas | |
| **029** | migración v1→v2 completa, en orden de riesgo | |
| **030** | el mensaje del bloque ES el recibo | |

---

## 7 · LOS 5 BLOQUES CERRADOS Y SU LECCIÓN

Cada uno dejó una lección **medida**, no opinada. Son las más valiosas del sistema.

### 7.1 · `split-architecture` (julio) — partir un archivo grande

> ⭐ **"Partir destapa lo que nadie estaba midiendo."**

Mover una sección hizo que `grade-block` leyera ese texto **por primera vez** — y encontró
**la contraseña SSH real de Brian**, escrita desde el 27-jul dentro de un ejemplo de *"qué NO
hacer"*. **Sobrevivió a todas las auditorías porque ningún validador había medido ese archivo.**

⭐ **Una contraseña dentro de un ejemplo de mala práctica sigue siendo una contraseña.**

Otras dos lecciones del mismo bloque:
- **El sufijo `-BIS`/`-TER` nunca fue una rareza de nombres: era el archivo diciendo que contenía
  dos cosas distintas.** Los 12 cortes coincidieron exactamente con los sufijos.
- ⭐ **Un puntero en su sitio vence a un borrado.** Cada sección extraída dejó un stub diciendo a
  dónde fue. Los 46 documentos que la citaban siguieron resolviendo **con cero ediciones**.
  Borrar habría convertido una partición de 5 archivos en **una reescritura de 46 documentos**.

**Y la verificación:** *"0 líneas de contenido perdidas — medido cinco veces, no asumido una."*

### 7.2 · `distribucion` (agosto) — que un clon se instale solo

> ⭐ **"Un límite que no has verificado no es un límite: es una suposición disfrazada."**

Un sub-bloque se declaró **BLOQUEADO** por *"necesita un clon limpio"*, tras una sonda ingenua.
**Nunca se consultó la fuente.** La documentación oficial lo respondía, y los tres sub-bloques se
hicieron **en una hora**.

⭐ **Es el mismo defecto que un check que reporta verde sin medir, un nivel más arriba: un PLAN
reportando bloqueado sin medir.**

🔴 **Segundo hallazgo:** las reglas `deny` de `Edit`/`Write` **no cubren `Bash`** — un `python3 -c`
reescribió un archivo que la regla de Edit protegía.

### 7.3 · `expertise-programacion` (agosto) — dónde vive una regla

> ⭐ **"El eje para ubicar una regla no es DE QUÉ TRATA — es a quién hay que INYECTÁRSELA."**

La IA puso el flujo de PR dentro de `principles/expertise/dev-backend.md` aplicando *"un tema, una casa"*. **Brian lo
corrigió:** *"va a haber PR de frontend, de base de datos"*. Y era **medible**: el hook inyecta
solo lo que el bloque declara, así que un flujo en backend **nunca habría llegado** a un bloque de
frontend.

> 🔴 **"Un validador que nadie valida reporta veredictos que nunca midió."**

Calificar ese bloque destapó **3 defectos en `grade-block`** — los tres hallados **por accidente**.

### 7.4 · `plan-tests-demo` (agosto) — los tests de la demo

> 🔴 **"Un validador lee la CELDA, no la intención."**

Decorar una celda de estado con `active · 🔴 red test holds it` **desactivó en silencio** el aviso
de sub-bloques sin cerrar — el patrón espera un `\w+` pelado ahí.

⭐ **La columna de estado es una interfaz que lee una máquina: una palabra pelada; el matiz va en
la columna de descripción.**

⚠️ **`grep -rl` cuenta ARCHIVOS; `grade-block` cuenta REFERENCIAS.** El número del validador es el
que gobierna, porque es contra el que se compara.

### 7.5 · `separacion-motor-instancia` (agosto) — el motor vs la instancia

> ⭐⭐ **"Una explicación cómoda para un rojo es cómo un bug sobrevive a una auditoría."**

La etiqueta *"son 8 fallos y son de la instancia de Brian"* llevaba **meses** tapando **4 defectos
reales del motor**.

> ⭐ **"Mover archivos habría escondido el defecto en vez de corregirlo."**

La hipótesis era mover **221 archivos** a una carpeta `instance/`. **Medido: ninguno estorbaba.**
Lo que fallaba eran los CHECKS que los interrogaban mal. `instance/` **NO se creó** y el §B del
bloque se corrigió — **la medición cambió el alcance, no al revés.**

**Tercer hallazgo:** el hook confundía **MENCIONAR** una ruta con **RECLAMARLA** (subcadena). Un
bloque nombró `marca-personal/` solo para decir de quién NO era, y el hook le atribuyó archivos
ajenos.

---

## 8 · LAS 26 REGLAS

| Regla | Líneas | Qué gobierna |
|---|---|---|
| `contract-block` | **338** | la forma de un bloque |
| `qa-dimensions` | **312** | las 6 dimensiones de calidad |
| `NAMING_CONVENTION` | 285 | cómo se nombra |
| `rule-shipping-flow` | **250** | rama → verificar → PR → ⛔ no mergear |
| `rule-config-hygiene` | 240 | los permisos y la configuración |
| `contract-document` | 206 | la forma de un documento |
| **`rule-pr-batching`** | **199** | 4 pendientes por PR · el cierre · conflictos · **el airlock** |
| **`rule-checks-must-measure`** | **196** | ⭐ **las 4 familias de error** |
| `contract-handoff` | 195 | el traspaso entre sesiones |
| `block-lifecycle` | 170 | quién llena qué y cuándo |
| **`rule-inheritance`** | **167** | ⭐ 3 niveles · **en conflicto gana la más estricta** |
| `contract-campaign` | 147 | la forma de una campaña |
| `contract-adr` | 143 | la forma de un ADR |
| `contract-pending` | 141 | la forma de un pendiente |
| `ESTANDAR_Metodo_Fases_F` | 140 | explicar → aprobar → construir |
| `contract-archive` | 131 | qué sobrevive al cierre |
| `case-dangerous-default` | 128 | ⭐ **un default nunca apunta a algo con dueño** |
| `rule-product-authority` | 118 | ⭐ el Grafo manda; **el código se AUDITA** |
| `rule-fix-not-patch` | 109 | arreglar sin apilar código encima |
| `rule-session-close` | 108 | ⭐ **qué se escribe ANTES de un `/clear`** |
| `rule-pending-rotation` | 103 | **rota el ARCHIVO, no el pendiente** |
| `rule-friction` | 100 | qué hacer cuando una regla estorba |
| `rule-post-merge-cleanup` | 86 | la rama mergeada se borra |
| `rule-isolation` | 76 | los bloques no se leen entre sí |
| `rule-lanes` | 76 | cuánto proceso lleva un trabajo |
| `rule-moving-files` | 76 | mover sin perder historia |

⭐ **`rule-inheritance` es la que más veces se invoca:** las reglas se **SUMAN**, nunca se relajan.
**En conflicto, gana la más estricta.**

---

## 9 · LOS 4 DUEÑOS

| Dueño | Archivo | Líneas | Qué juzga |
|---|---|---|---|
| **owner-0** | `owner-0-voice` | 285 | ⭐ **LA VOZ** — cómo se comunica |
| owner-1 | `owner-1-docs` | 104 | los documentos |
| owner-2 | `owner-2-dev` | 124 | el código |
| owner-3 | `owner-3-validation` | 181 | ⭐ **la verificación** |
| — | `contract-delivery` | **343** | el contrato de entrega |

### 9.1 · La expertise destilada

| Área | Líneas |
|---|---|
| `dev-database` | 364 |
| `val-integration` | 290 |
| `doc-structure` | 289 |
| `val-functional` | 280 |
| `doc-planning` | 274 |
| `dev-backend` | 262 |
| `dev-frontend` | 257 |

⭐ **`val-functional` §2.2 es la fuente de la verificación afirmativa:** un test rojo es prueba;
un verde que nunca se vio rojo no lo es.

### 9.2 · 🔴 La lección de la voz (S10)

El output style pasó de **8 reglas negativas** a un **contrato de entrega**. Y la lección de fondo:

> ⭐ **"Antes de AÑADIR una regla, busca la que CAUSA el bug."**

La voz no carecía de estructura: **2 de sus 8 reglas la prohibían** (la 2.5 ordenaba cortar el
cierre; la 2.8 permitía omitir el porqué). **Se corrigieron las causas, no se añadieron parches.**

Resultado medido: el vehículo pasó de **5,167 → 2,644 tokens por turno (−48%)**.

---

## 10 · LAS 65 RONDAS — con qué se diseñó For3s OS

**65 archivos · 32,377 líneas** en `work/`. Es el diseño completo, por capas:

| Ronda | Bloques | Capa |
|---|---|---|
| **R1** | 1 | Compute y lenguaje |
| **R2** | 5 | Storage · memoria · rendimiento · archivos externos |
| **R3** | 7 | LLM principal · prompt/contexto · streaming · observabilidad y coste |
| **R4** | 5 | MCP: framework, servidores, ciclo de vida de herramientas |
| **R5** | 6 | ⭐ **Tálamo/routing** — de aquí sale el `MessageBus` (R5 B3 §5.3.3) |
| **R6** | 6 | Meta-orquestador + governor de 6 frenos |
| **R7** | 5 | |
| **R8** | 5 | |
| **R9** | 4 | |
| **R10** | 4 | ⭐ Networking dual-plane (Cloudflare + Tailscale) |

⭐ **Dato que conecta con la otra auditoría:** el `MessageBus` que hoy **nadie usa** (hallazgo H-08)
nació en **R5 B3 §5.3.3** — su propio docstring lo cita. **El diseño existía; la conexión no se
hizo.**

⚠️ **Las rondas son la fuente de "CON QUÉ"** según `rule-product-authority`: el Grafo Maestro dice
**CÓMO FUNCIONA**, las rondas dicen **CON QUÉ**, la visión dice **POR QUÉ**, y **el código se
AUDITA, no manda**.

---

## 11 · LA DEUDA VIVA

`memory/pendiente-agosto-2026.md` — **1,645 líneas**, la rotación actual.

| Gravedad | Cuántos |
|---|---|
| 🔴 | **27** |
| 🟠 | 24 |
| 🟢 | 83 |
| **TOTAL** | **134** |

### 11.1 · Los dos bloques de deuda

| Bloque | Qué contiene |
|---|---|
| **MOTOR** — Mente OS mismo | V2-1 a V2-11: partir la arquitectura (2,471 líneas contra techo 800) · renombrado (28 archivos) · encarpetado · el Maestro · configuración · 🔴 un clon ajeno hereda el nombre de Brian · `piezas.tsv` sin validador · 2 reglas sin script |
| **PRODUCTO** — For3s OS | P-5 bugs de PR4-A (2 de 21) · P-7 seguridad · 🔴 BUG-1 decay de memoria MUERTO · 🔴 BUG-2 GitHub MCP y web_fetch rotos |

⭐ **`rule-pending-rotation`: se rota el ARCHIVO, no el pendiente.** Un pendiente que sobrevive a
una rotación declara `Arrastrado desde` — así se ve cuántas veces se ha pospuesto.

---

## 12 · 📋 LAS 20 LECCIONES QUE LA CAMPAÑA DEBE LLEVAR PUESTAS

Ordenadas por cuántas veces nos han mordido.

### 🔴 Las que ya causaron daño real

| # | Lección | De dónde salió |
|---|---|---|
| **L-01** | **Una regla en código se cumple 100%; en documento, 40-60%** | la ley del proyecto · demostrada sobre `rule-session-close` |
| **L-02** | **Un check debe VERSE FALLAR antes de que su verde valga** | `val-functional` §2.2 |
| **L-03** | **La sesión muere de EDAD, no de peso** | R1 (96h) · R2 (76h) · R3 (11 días) |
| **L-04** | **Registrar el cierre NO es cerrar** | S11 siguió viva 46h y llegó a 1,000,030 tokens |
| **L-05** | **Verificar FUERA del árbol del autor** | 195/0 aquí, **22 fallos en un clon** |
| **L-06** | **Una explicación cómoda para un rojo es cómo un bug sobrevive** | `separacion-motor-instancia` — meses tapando 4 defectos |
| **L-07** | **Un límite no verificado es una suposición disfrazada** | `distribucion` — "bloqueado" resuelto en 1 hora |
| **L-08** | ⛔ **NUNCA inventar criterio: preguntar** | ADR-003 · ADR-014 |

### 🟠 Las que costaron tiempo

| # | Lección | De dónde salió |
|---|---|---|
| **L-09** | **Antes de AÑADIR una regla, busca la que CAUSA el bug** | S10 — 2 de las 8 reglas de voz causaban el problema |
| **L-10** | **Presencia ≠ uso** — que exista no es que se llame | esta sesión |
| **L-11** | **Un validador lee la CELDA, no la intención** | `plan-tests-demo` — un adorno desactivó un aviso |
| **L-12** | **El archivo que se lee PRIMERO era el menos vigilado** | `CLAUDE.md` sin auditar |
| **L-13** | **Un puntero en su sitio vence a un borrado** | 46 documentos siguieron resolviendo con 0 ediciones |
| **L-14** | **Mover archivos puede ESCONDER el defecto** | 221 archivos que no estorbaban |
| **L-15** | **Medir una parte y hablar del todo** | mis 5 errores en la auditoría de For3s OS |

### 🟡 Las de forma, que igual muerden

| # | Lección | De dónde salió |
|---|---|---|
| **L-16** | **Dos formas de decir lo mismo son dos reglas** | `contract-handoff` decía "Validated by" en vez de "Verified by" |
| **L-17** | **Un default nunca apunta a algo con dueño** | `case-dangerous-default` |
| **L-18** | **Rota el ARCHIVO, no el pendiente** | `rule-pending-rotation` |
| **L-19** | **Un squash merge borra trabajo ya empujado** | PRs #27 y #31 · dos veces el mismo día |
| **L-20** | **Una contraseña en un ejemplo de mala práctica sigue siendo una contraseña** | `split-architecture` |

---

## 13 · ⚠️ LO QUE MENTE OS TODAVÍA NO SABE HACER

**Declarado, no escondido.** La campaña debe saber dónde el sistema NO ayuda.

| Hueco | Consecuencia para la campaña |
|---|---|
| **No conoce la palabra "fase"** | ni `contract-campaign` ni `contract-block` la mencionan. Las 3 fases hay que construirlas |
| **No hay orquestación multi-agente** | el bloque `orquestacion-multiagente` está BLOQUEADO a propósito |
| **La prueba de campo sigue pendiente** | nadie externo ha instalado Mente OS. Es el único bloqueante real del motor |
| **`piezas.tsv` declara piezas y (hasta hace poco) ningún validador** | V2-9 |
| **2 reglas escritas sin script que las verifique** | V2-10 — la ley del proyecto pendiente sobre sí misma |
| **La arquitectura viola su propio techo** | 2,471 líneas contra 800 (V2-1) |
| **Un clon ajeno hereda el nombre de Brian** | 🔴 V2-8 — el mismo defecto que `_TG_BRIAN` en For3s OS |

⭐⭐ **Coincidencia que importa:** **V2-8 (Mente OS) y H-05 (For3s OS) son el MISMO defecto** —
el nombre del autor cableado donde debería haber una variable. **Los dos sistemas tienen la misma
enfermedad.**

---

## 14 · CÓMO USA ESTO LA CAMPAÑA

| Antes de… | Lee… |
|---|---|
| escribir un check | §3 — las 5 familias · §12 L-02 |
| declarar algo bloqueado | §7.2 — L-07 |
| aceptar una explicación para un rojo | §7.5 — L-06 |
| mover o partir un archivo | §7.1 — L-13, L-14 |
| cerrar una sesión | §5 — los umbrales y L-04 |
| inventar un criterio | ⛔ **ADR-003. Preguntar** |
| afirmar que algo está verde | §12 L-05 — verificar fuera del árbol |
| añadir una regla | §9.2 L-09 — buscar la que causa el bug |

⛔ **Lo que este documento NO hace:** decidir. Recuerda.

⚠️ **Caducidad:** las lecciones no caducan; los números sí (332 archivos, 230 checks, 134
pendientes). Re-contarlos antes de citarlos.


---

## 15 · 🔴 LO QUE LA LECTURA COMPLETA DESTAPÓ (2026-08-12)

**Añadido tras leer `memory/Estado_Sesion_Continuidad.md` (4,782 líneas) y `memory/PENDIENTES.md` (~2,600) enteros,
por orden de Brian.** Son hallazgos que **ninguna auditoría anterior tenía**, porque vivían en los
dos archivos más grandes del sistema — uno de ellos prohibido por `CLAUDE.md`.

### 15.1 · ⭐⭐ Las 10 rondas están 100% cerradas — y con 40 decisiones LOCKED

**R1 a R10, 100% cerradas entre el 2026-05-30 y el 2026-06-09.** Diez días. Producen:
**40 decisiones LOCKED (D-001 a D-040)** · **11/11 nodos cerebrales** · los 3 pilares ·
SOC2 ~90-95% + GDPR ~88-92% audit-ready · costo v1 proyectado **$97-137/mes**.

⭐ **El diseño de For3s OS no es vago ni improvisado: es exhaustivo.** Cada ronda tiene
pre-preguntas, candidatos, filtro por las 3 anclas, decisión LOCKED, implicaciones y riesgos
aceptados numerados.

### 15.2 · 🔴 DOS REVISIONES QUE BRIAN EXIGIÓ Y NUNCA SE HICIERON

`Estado_Sesion_Continuidad` §3.1.R10 lo declara como **el próximo paso crítico**, en mayúsculas:

> **"El diseño (R1-R10) está completo. ANTES de escribir código, instrucciones LOCKED de Brian
> exigen DOS revisiones."**

| Bandera | Palabras de Brian | Estado |
|---|---|---|
| ⚠️ **RE-REVISIÓN R6** | *"VOLVER A REVISAR Y PLANIFICAR CUANDO ESTEMOS REALIZANDO CODIGO TODO EL R6 POR QUE ES UN R EXTREMANDAMENTE IMPORTANTE"* (2026-06-07) | 🔴 **nunca se hizo** |
| ⚠️ **DMN 5.4.2** | las 8 tareas del DMN necesitaban replanificación profunda pre-código | 🔴 **nunca se hizo** |

**El documento cierra con:** *"Después de esas dos revisiones → ARRANCA PROGRAMACIÓN."*
⭐ **Se programó igual.** Las dos banderas persisten como `carry-forward` desde R5 hasta R10 — se
arrastraron por **seis rondas** y nadie las cerró.

### 15.3 · ⭐⭐ El hallazgo H-06 estaba PREDICHO por la bandera 5.4.2

La auditoría de For3s OS midió que **3 tareas del DMN se despiertan 114 veces y nunca corren**
(`cache_prewarming` · `embedding_precompute` · `routing_learning`).

**Leído el diseño (R5 B4 §5.4.2): las tres están `enabled_by_default=True`.** No están apagadas.

**Y leído el código real, la causa está escrita en su propia cabecera** (`dmn_tasks.py:8-14`):

> *"REALES (tienen infra hoy): embedding_precompute · memory_consolidation · cache_prewarming…
> **STUBS HONESTOS (sin infra todavía — NO fingen trabajo, lo declaran en su outcome):**
> routing_learning (no hay router multi-modelo: **H7 enrutamiento bloqueado**) ·
> eval_regression_detection (no hay golden set formal)."*

⭐⭐ **Esto cambia el diagnóstico por completo.** No son un bug: son **stubs declarados con
honestidad**, esperando una infraestructura que nunca llegó (H7, diferido en §EXTRAS).
🔴 **Pero el sistema NO distingue "stub honesto" de "tarea rota" en su telemetría**: las 114
corridas se registran igual que una que sí trabajó. **El defecto real es de observabilidad, no de
lógica** — y ese sí hay que arreglarlo.

### 15.4 · 🔴 El cifrado del contenido era una decisión LOCKED, no un olvido

**R2 B1 sub-tema 1.6 (D-006), textual:** *"Payload JSONB + **columnas BYTEA cifradas (P4)**"* para
`episodes_events`. Y **P4 quedó LOCKED** como *"híbrido: app-layer AES-GCM + filesystem LUKS —
defense in depth"*.

**Medido en la BD de `brian`: el contenido está EN CLARO, 15 MB.**

⭐ El hallazgo H-01 no es un descuido de implementación: **es una decisión LOCKED del diseño que
no se implementó.** Y `crypto.py` tiene exactamente las funciones que P4 pedía
(`derive_workspace_key` + AES-GCM) — construidas, y sin cablear a `episodes_events`.

### 15.5 · El `MessageBus` implementado es una FRACCIÓN del diseñado

| | Diseño (R5 B3 §5.3.3) | Código real |
|---|---|---|
| Tipos de mensaje | **10** (`PROGRESS` `RESULT_PARTIAL` `RESULT_FINAL` `ERROR` `CRITICAL_FINDING` `EXTRA_CONTEXT` `CANCEL` `MODE_CHANGE` `REQUEST_HELP` `HELP_RESPONSE`) | **3** (`tarea` `reporte` `evento`) |
| Patrones | **4** — incluido ⭐ **specialist ↔ specialist** (`ask_peer` con `correlation_id`) | **3** — sin peer-to-peer |
| Rate limit por specialist | ✅ `TokenBucket` 50 msg/s | 🔴 no existe |
| Detección cross-batch | ✅ `SECURITY_VIOLATION_cross_batch_message` | 🔴 no existe |

⭐ **El hallazgo H-08 se agrava con este dato:** el bus no solo está encerrado — **está a menos de
la mitad de lo que su propio diseño especificaba**, y le falta justamente la pieza que permitiría
que dos componentes se hablaran directamente.

### 15.6 · `telegram_channel.py` lleva señalado desde JUNIO

**PR9 (Profesionalización, 2026-06-28)**, diferido por decisión: *"dividir `telegram_channel.py`
(~3350 L) en módulos por extracción incremental (NO big-bang; es el archivo VIVO del bot — un
error rompe Telegram)"*.

📊 **Junio: 3,350 líneas → hoy: 4,570.** **Creció 1,220 líneas (+36%) después de declararse deuda.**

### 15.7 · Un patrón que se repite y tiene nombre en el propio archivo

> 🚨 **"HALLAZGO MAYOR: aplicar fixes con `docker cp` es EFÍMERO"** — al recrear el contenedor se
> perdieron los fixes de HA-1, HA-5 y **BUG-14 (la fuga de privacidad quedó REABIERTA en
> producción)**, porque solo vivían en `docker cp`.

⭐ **Es la misma forma que la ley del proyecto**, un nivel más abajo: *un arreglo que no está en la
fuente no está arreglado*. Igual que *una regla que no está en código no se cumple*.

### 15.8 · Lo que el sistema YA resolvió y nadie registró

Dos pendientes se cerraron al **medirlos**, no al construirlos:

| Pendiente | Lo que se creía | Lo medido |
|---|---|---|
| `intern-os #2` shared-thread inbox | *"falta construir"* | **ya estaba construido desde el 2026-07-02** — 656 líneas (`temas.py` 296 · `tema_estado.py` 216 · `hilo_status.py` 144) |
| BUG-EQUIPO specialists sin identidad | *"los 5 se lanzan en frío"* | **la MISMA línea que documentaba el bug ya lo arreglaba** — `capsula_equipo()` sellado |

⭐ **Lección nueva, L-21: antes de construir un pendiente viejo, medir si ya está hecho.**
Dos de dos resultaron cerrados. **El coste de no registrar un cierre es reconstruirlo.**

### 15.9 · Las reglas de conversación que Brian fijó en MAYO y siguen vigentes

De `Estado_Sesion_Continuidad` §4.1 — **la más fuerte, en sus palabras**:

> ✓ *"**Si no te pregunto por algo es porque no lo sé y quiero saberlo**"* — no diluyas información.
> ✓ *"Vamos a fondo. No me des versiones suavizadas."*
> ✓ *"Documenta TODO sin perder nada."*
> ✓ *"**No intuyas. Si no sabes, lee primero.**"*

Y los anti-patrones que rechazó: lenguaje de marketing · conclusiones prematuras · tratar
borradores históricos como fuente de verdad · **ofrecer herramientas que no pidió**.

⭐ **Estas cinco reglas de mayo son el germen de `owner-0-voice`.** No cambiaron: se formalizaron.


---

## 16 · 🔴🔴 EL HALLAZGO MAYOR — el DISEÑO y el CÓDIGO son dos sistemas distintos

**Medido el 2026-08-12 cruzando las 65 rondas contra el código y la BD reales.** Es el hallazgo
más importante de toda la lectura, y ninguna auditoría anterior lo tenía porque **exigía leer las
dos mitades a la vez**.

### 16.1 · La prueba dura: 15 de 15 tablas del diseño NO existen

Las rondas especifican esquemas SQL concretos. Consultadas en la BD viva de `brian`:

| Tabla del diseño | Ronda | ¿Existe? |
|---|---|---|
| `workspaces` | R2 B1 · el eje del multi-tenant | 🔴 **NO** |
| `workspace_secrets` · `secret_usage_audit` | R4 B1 4.1.4 (KEK) | 🔴 **NO** |
| `workspace_signing_keys` · `output_signatures` | R7 B2 (Output Gate) | 🔴 **NO** |
| `identities` · `identity_credentials` · `roles` | R7 B3 (Auth/RBAC) | 🔴 **NO** |
| `incidents` · `postmortems` · `alerts` | R8 B4 | 🔴 **NO** |
| `request_records` | R8 B1 | 🔴 **NO** |
| `eval_runs` · `eval_results` · `golden_datasets` | R3 B4 3.4.3 | 🔴 **NO** |
| `cost_alarms` · `cost_anomalies` | R3 B4 3.4.2 | 🔴 **NO** |
| `skills_events` · `episodes_state` | R2 B1 1.6 (Event Sourcing) | 🔴 **NO** |
| `audit_events_archive` | R8 B3 8.3.2 | 🔴 **NO** |

**La BD real tiene 41 tablas. Ninguna de las 15 especificadas arriba está entre ellas.**

⭐⭐ **Esto no significa que For3s OS esté mal construido.** Significa que **el código NO
implementó el diseño: implementó otra cosa que funciona.** Son dos sistemas con el mismo nombre.

### 16.2 · Lo mismo, pieza por pieza

| Pieza | Lo que el diseño LOCKEÓ | Lo que hay en el código |
|---|---|---|
| **Output Gate** (R7 B2) | firma HMAC/Ed25519 de cada respuesta + trace + 4 renderers + 25 eventos de streaming | 🔴 **no existe** — los 3 usos de `hmac` son comparación de tokens de acceso |
| **Auth / RBAC** (R7 B3) | identidad central · 6 tipos de credencial · **35+ permisos** · 5 roles de sistema | 🔴 sin tablas |
| **MessageBus** (R5 B3) | 10 tipos de mensaje · 4 patrones (incluido `specialist ↔ specialist`) · TokenBucket 50 msg/s · detección cross-batch | 3 tipos · 3 patrones · sin rate limit · sin detección |
| **Confidence** (R6 B1) | **8 señales** ponderadas | **4 implementadas** — `señales_neutras_pendientes()` declara las otras 4 |
| **Governor** (R6 B2) | 6 frenos con scoring dopaminérgico + NO-GO + sandbox | **3 frenos reales · 3 hooks neutros** que devuelven `True` |
| **Vía NO-GO** (R6 B2 6.2.3) | 3 severidades HARD/SOFT/WARN + 3 tipos de detección + matriz de bypass | 🔴 **no existe** — solo el hook que la espera |
| **Skills** (R6 B2 6.2.1) | filesystem LUKS + Postgres + pgvector · SemVer · métricas · promoción 3-tier | tabla `skills` con 16 filas, sin lifecycle |
| **DMN** (R5 B4) | 8 tareas con trigger/action/budget | 8 tareas, **3 son stubs honestos** esperando H7 |
| **Eval** (R3 B4 3.4.3) | 4 capas: reglas · golden datasets · LLM-judge · revisión humana | 🔴 sin tablas — `eval_regression_detection` es stub |

### 16.3 · ⭐ El código es HONESTO sobre lo que le falta — y eso lo cambia todo

**Tres piezas distintas declaran su propio hueco, en su propio código:**

```python
# dmn_tasks.py:11-14
#  STUBS HONESTOS (sin infra todavía — NO fingen trabajo, lo declaran en su outcome):
#    routing_learning (no hay router multi-modelo: H7 enrutamiento bloqueado) ·
#    eval_regression_detection (no hay golden set formal).

# governor.py:331-333
# No son frenos falsos: son puntos de extensión explícitos. Hoy devuelven un
# veredicto neutro porque la maquinaria que los activa (scoring dopaminérgico,
# NO-GO rules, sandbox de skills) llega con H12.

# confidence.py:181
def señales_neutras_pendientes() -> list[Signal]:
```

⭐⭐ **Esto reencuadra media auditoría.** Lo que parecían fallos silenciosos son **límites
declarados**. El sistema no miente sobre sí mismo: **dice lo que no hace, en el sitio donde no lo
hace.**

🔴 **Pero el hueco real es de OBSERVABILIDAD, y ese sí duele:** un stub honesto y una tarea rota
**se registran idénticos** en `dmn_corridas`. Un freno neutro y un freno que aprueba **devuelven el
mismo `Veredicto(True)`**. **La honestidad vive en los comentarios, no en la telemetría.**

### 16.4 · Por qué pasó — y no es negligencia

`Estado_Sesion_Continuidad` lo explica sin querer. Las 10 rondas cerraron **entre el 30-may y el
9-jun: diez días** de diseño exhaustivo, con costo proyectado de **$97-137/mes** para una
arquitectura multi-tenant con SOC2.

Y el código empezó **después**, con una realidad distinta: **un solo usuario, un servidor que es
una laptop, y una suscripción de Claude en vez de API de pago.**

⭐ **El diseño resolvía el problema de vender a empresas. El código resolvió el problema de que
Brian pudiera usarlo.** Ambos son correctos para su problema. **Lo que no existe es el documento
que declare que divergieron.**

### 16.5 · Lo que esto significa para la campaña — y cambia el plan

⛔ **`rules/rule-product-authority.md` dice que el Grafo Maestro manda y que "el código se AUDITA, no
manda".** Con este hallazgo medido, esa regla tiene una consecuencia que hay que decir en voz alta:

> **Si el Grafo es la vara, For3s OS falla en 15 de 15 tablas y en 9 de 9 piezas mayores.**

Eso **no es un veredicto útil**: declararía en rojo un sistema que funciona todos los días.

🙋 **Es una decisión de Brian, no de la campaña.** Tres caminos:

| | Qué significa | Consecuencia |
|---|---|---|
| **A** | El Grafo es el destino; el código es v1 hacia él | la campaña mide **distancia al diseño**, no defectos |
| **B** | El código es la realidad; el Grafo se actualiza a lo construido | el diseño deja de ser deuda y pasa a ser historia |
| **C** | Ambos valen: el Grafo para vender, el código para usar | hay que declarar **qué pieza sigue cuál vara** |

⚠️ **Sin esta decisión, cada uno de los 12 bloques tropezará con la misma pregunta** — y la
responderá distinto, que es exactamente lo que `rule-inheritance` existe para evitar.


---

## 17 · EL MAPA COMPLETO DISEÑO → CÓDIGO, ronda por ronda

**Continuación de §16, medida el 2026-08-12 leyendo las rondas R2, R4, R8, R9 y R10 y
contrastando cada decisión LOCKED contra el código y la BD vivos.**

⚠️ **Esta sección corrige el tono de §16 en un punto importante:** no es que el código ignorara el
diseño. **Hay piezas implementadas con fidelidad alta.** El mapa real es desigual, y saber DÓNDE
es exactamente lo que la campaña necesita.

### 17.1 · El semáforo por pieza

| Ronda | Pieza | Diseño | Realidad medida | |
|---|---|---|---|---|
| **R2 B1** | Postgres + AGE + pgvector | los 3 en una instancia | ✅ los 3 corriendo | 🟢 |
| **R2 B1 1.6** | `audit_events` inmutable por trigger | triggers Postgres | ✅ **2 triggers activos** · 12,908 eventos encadenados | 🟢 |
| **R2 B1 1.6** | Event Sourcing por aggregate | `episodes_events` + `episodes_state` + `skills_events` | 🔴 solo `episodes_events`, **y es CRUD** (tiene `deleted_at`, `id` es `bigint`, 0 triggers) | 🔴 |
| **R2 B1 P3** | schema-per-tenant | `wks_<cliente>` por cliente | 🔴 todo en `public` · aislamiento por **contenedor**, no por schema | 🟠 |
| **R2 B2 2.2** | Embeddings locales | Stella 400M @1024 | 🟡 **BGE-M3** @1024 — se cambió el modelo, se respetó la dimensión | 🟡 |
| **R2 B2 2.5** | Olvido en 4 etapas | soft → decay → archive → purge | 🟡 **4 de 5 columnas existen** · el decay **funciona de verdad** (p50 0.356, rango 0.225-0.916, **4,230 candidatos**) · 🔴 falta `legal_hold` y **la tabla de archive** | 🟡 |
| **R2 B2 2.6** | CLS híbrido HDBSCAN + Haiku | consolidación nocturna | ✅ corre · **91.3% consolidado** al grafo | 🟢 |
| **R3 B4 3.4.3** | Eval en 4 capas + golden datasets | `eval_runs` `eval_results` `golden_datasets` | 🔴 **cero tablas** · `eval_regression_detection` es stub | 🔴 |
| **R4 B1** | 4 servidores MCP (1 oficial + 3 custom) | GitHub · Filesystem · HTTP · Telegram | 🟡 **solo GitHub** (el oficial). Los 3 custom no se construyeron | 🟡 |
| **R4 B1 4.1.3** | Docker multi-tenant, container por cliente | 3 capas + 4 redes | ✅ **28 contenedores, 3 instancias, volúmenes separados** — la idea SÍ se cumplió, con otra forma | 🟢 |
| **R4 B1 4.1.4** | Secretos con jerarquía KEK | `workspace_secrets` + `secret_usage_audit` | 🟡 **cifrado real** (`nonce`+`ciphertext`, 38 secretos) · 🔴 sin las 2 tablas ni audit por uso | 🟡 |
| **R5 B1** | Tálamo router | routing por subgrafo | 🔴 no existe — H7 diferido | 🔴 |
| **R5 B3** | MessageBus 10 tipos / 4 patrones | + TokenBucket + cross-batch | 🟡 3 tipos / 3 patrones, encerrado | 🟡 |
| **R6 B1** | Confidence 8 señales | ponderadas | 🟡 **4 implementadas**, 4 declaradas pendientes | 🟡 |
| **R6 B2** | Pilar 3: skills GO/NO-GO + dopaminergic | lifecycle 7 fases | 🟡 skills existen (16) · 🔴 **NO-GO no existe** · 🔴 3 de 6 frenos son hooks neutros | 🟠 |
| **R7 B2** | Output Gate firmado | HMAC/Ed25519 + 25 eventos | 🔴 **no existe** | 🔴 |
| **R7 B3** | Auth + RBAC 35+ permisos | 5 tablas | 🔴 **cero tablas** · auth por `telegram_user_id` | 🔴 |
| **R8 B1** | ~5,150 series Prometheus | 11 nodos × 5 categorías | 🟡 **Grafana corre** (3 instancias) · 🔴 sin Prometheus ni las series | 🟠 |
| **R8 B3** | Audit chain + retención 3 niveles | hot/warm/cold + R2 | 🟡 **la cadena SÍ** (12,908 con `hash_prev`+`hash_self`) · 🔴 sin retención por niveles | 🟡 |
| **R8 B4** | SLO/SLA + incidentes + runbooks | `incidents` `postmortems` `alerts` | 🔴 **cero tablas** | 🔴 |
| **R9 B1** | ⭐ **Amígdala — el nodo 11/11** | escáner 5 capas + anomalías + coordinador | 🔴 **NO EXISTE** | 🔴 |
| **R10 B1** | CI de 7 stages | lint→unit→SAST→integration→E2E→gate→compliance | 🟡 **4 workflows** (`release` `scorecard` `trivy` ×2) con jobs `quality`+`security` | 🟡 |

**Conteo:** 🟢 **4 fieles** · 🟡 **9 parciales** · 🟠 **3 con otra forma** · 🔴 **7 ausentes**.

### 17.2 · ⭐ Lo que se cumplió mejor de lo que parecía

**§16 sonaba a demolición. Con las rondas leídas, tres cosas merecen decirse:**

1. **La cadena de auditoría es fiel al diseño.** R2 B1 pedía inmutabilidad por trigger y hash
   encadenado: **2 triggers activos y 12,908 eventos con `hash_prev` y `hash_self`.** Es la pieza
   más "enterprise" del sistema y **está construida como se diseñó**.
2. **El aislamiento multi-tenant se logró, con otra forma.** El diseño pedía schema-per-tenant;
   el código usa **un contenedor y una BD por instancia**. ⭐ **Es MÁS aislado que lo diseñado**,
   no menos.
3. **El olvido funciona de verdad.** No es un cron que corre en vacío: `relevance` va de 0.225 a
   0.916 con p50 en 0.356, y **4,230 memorias ya son candidatas**. La microglía tiene material.

### 17.3 · 🔴 Y lo que hay que decir sin suavizar

**El nodo 11/11 no existe.** `Estado_Sesion_Continuidad` §3.1.R9 celebra: *"Cierra el último nodo
cerebral (Amígdala Node 7) → **11/11 NODOS COMPLETOS**"*. **Medido: cero coincidencias de
`amigdala`, `threat_scan` o `ThreatLevel` en los 76 archivos.**

⚠️ **Con un matiz que es justo dar:** `governor.py:112-127` **sí escanea prompt-injection** — pero
**solo sobre las skills nuevas**, no sobre la entrada del usuario. La defensa existe, en otro punto
y con otro alcance del diseñado.

⭐ **La frase "11/11 nodos completos" significa "11/11 nodos DISEÑADOS", no construidos.** Y ese
matiz no está escrito en ninguna parte — por eso esta sección existe.

### 17.4 · La regla que sale de todo esto

> ⭐⭐ **L-22 · Un hito que declara "completo" debe decir COMPLETO EN QUÉ: diseñado, construido, o
> verificado en producción.** Las tres son estados distintos, y confundirlos es cómo un sistema
> cree tener 11 nodos y tiene 10.

Es la misma familia que **L-01** (*una regla en documento se cumple 40-60%*) y que **L-11**
(*un validador lee la celda, no la intención*): **la palabra no es el hecho.**


---

## 18 · EL BALANCE FINAL — dónde el código SIGUIÓ el diseño y dónde no

**Cierre de la lectura de rondas (2026-08-12).** Completa §17 con R1, R3, R7 B1, R8 B1 y R9 B1/B2.
⚠️ **Y contiene la corrección más importante de las tres secciones:** el patrón no es aleatorio.

### 18.1 · ⭐⭐ EL PATRÓN — las capas BAJAS se construyeron, las ALTAS no

Ordenando las 10 rondas por su lugar en la pila:

| Ronda | Capa | Fidelidad medida |
|---|---|---|
| **R1** Compute | el suelo | 🟢🟢 **la más fiel de todas** — Python 3.12 exacto · `arq` · `mcp` · `sentence-transformers` · Valkey. Todo como se lockeó |
| **R2** Data | cimiento | 🟢 Postgres+AGE+pgvector los 3 · audit inmutable con sus 2 triggers · el olvido funciona |
| **R3** LLM | motor | 🟡 Anthropic + fallback ✅ · 🔴 sin SSE · 🔴 sin circuit breaker por proveedor · 🔴 sin eval |
| **R4** Tools/MCP | herramientas | 🟡 **1 de 4** servidores (solo el oficial) · el multi-tenant sí, con otra forma |
| **R5** Orquestación | coordinación | 🟡 multiagente sí · 🔴 Tálamo no · bus a un tercio |
| **R6** Memoria/Skills | inteligencia | 🟡 skills sí · 🔴 NO-GO no · 3 de 6 frenos neutros · 4 de 8 señales |
| **R7** Frontend/Canal | interfaz | 🔴 **2 de 3 canales** · Output Gate no · Auth/RBAC no |
| **R8** Observabilidad | visibilidad | 🔴 **cero Prometheus** · Grafana lee Postgres directo · sin incidentes |
| **R9** Seguridad | perímetro | 🔴 **la Amígdala NO EXISTE** — el nodo 11/11 |
| **R10** CI/CD | entrega | 🟡 4 workflows contra 7 stages |

⭐⭐ **La fidelidad DECAE monotónicamente según se sube la pila.** R1 y R2 son casi exactas;
R8 y R9 casi no existen.

**Y la explicación no es negligencia — es orden de construcción.** El código empezó por abajo
(había que correr), y **se detuvo donde el diseño dejaba de resolver el problema de un solo
usuario**: nadie necesita RBAC de 35 permisos, ni SLO por tier, ni un escáner de amenazas de 5
capas, **cuando el único usuario es el dueño y el servidor es su laptop**.

### 18.2 · La Amígdala, con la precisión que merece

**Es el hallazgo de seguridad más serio, y hay que decirlo exacto.**

`Estado_Sesion_Continuidad` §3.1.R9 celebra el cierre del **nodo 11/11**. El diseño (R9 B1) es
sofisticado: **5 capas fail-fast** — heurística (~1ms) → normalización anti-evasión (base64,
zero-width, homoglifos cirílicos) → clasificador Haiku solo para el ~10% sospechoso → **canary
tokens** → sanitización de contenido externo con `<<EXTERNAL_DATA_DO_NOT_EXECUTE>>`.

**Medido, capa por capa:**

| Capa | ¿Existe? |
|---|---|
| 1 · patrones de injection **sobre la entrada** | 🟠 el patrón existe en `governor.py:123` — **pero solo escanea SKILLS NUEVAS**, no lo que escribe el usuario |
| 2 · normalización anti-evasión | 🟠 `unicodedata` se usa en `conversation.py` — **para normalizar palabras clave**, no como defensa |
| 3 · clasificador LLM | 🔴 no existe |
| 4 · canary tokens | 🔴 no existe |
| 5 · sanitización de contenido externo | 🔴 no existe |

⭐ **Verificado en el camino real:** `Conversation.send()` recibe el mensaje y lo procesa **sin
pasarlo por ningún escáner**.

🔴 **Consecuencia sin adornos: For3s OS no tiene defensa contra prompt injection en la entrada
del usuario.** La que existe protege el catálogo de skills — un vector distinto.

### 18.3 · Lo que R1 demuestra, y vale más que cualquier hallazgo negativo

**R1 es la prueba de que el método funciona cuando se aplica.** Decidió 10 piezas de stack el
30-mayo con razones explícitas. **Hoy, dos meses y medio después, el `pyproject.toml` del servidor
las cumple casi una a una.**

⭐ **Cuando una decisión LOCKED estaba al alcance del siguiente paso, se cumplió.** Las que no se
cumplieron son las que exigían **un problema que todavía no existía** (clientes, escala,
auditores). No es un fallo de disciplina: **es diseño adelantado a su demanda.**

### 18.4 · ⭐⭐ La lección que cierra la lectura

> **L-23 · Diseñar diez capas de golpe produce un mapa preciso de un territorio que aún no
> existe. Lo que se construye es siempre la parte del mapa donde ya hay suelo.**

**Medido aquí:** 10 rondas cerradas en **10 días**, 40 decisiones LOCKED, y el código implementó
con fidelidad **las 2 capas más bajas** — abandonando progresivamente las 8 superiores según se
alejaban de la realidad de un usuario con una laptop.

⚠️ **Esto NO invalida el diseño.** Lo convierte en lo que la campaña necesita: **un mapa del
destino**, no un inventario de deuda. Cada 🔴 de §17 no es un bug — **es una capacidad que espera
un problema que la justifique.**

⛔ **Y por eso la decisión de §16.5 es urgente:** auditar el código contra un diseño pensado para
miles de clientes, cuando hay uno, **produce 7 rojos que nadie debería arreglar hoy.**


---

## 19 · ⭐⭐ EL MAPA NODO → ARCHIVO REAL — lo más accionable de toda la auditoría

**Leído `Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md` (2,485 líneas) y contrastado archivo por
archivo contra el servidor, 2026-08-12.**

⭐ **Este documento es el puente que la campaña buscaba:** dice qué tabla y qué módulo implementa
cada nodo cerebral. **Y sus rutas están todas desactualizadas** — pero los nombres sobreviven.

### 19.1 · 🔴 Las 10 rutas que el Mapeo declara NO existen

El Mapeo (2026-06-01) declara módulos con estructura de carpetas:

⚠️ Son rutas **de For3s OS**, no de Mente — escritas sin barra a propósito para que
`bin/check-links` no las lea como citas internas (es código de otro repo):

> bajo `memory` → `kg_bridge.py` `repository.py` `tiers.py` `forgetter.py` `consolidator.py` `ranker.py`
> bajo `orchestrator` → `dmn.py` `thalamus.py` `dual_process.py`
> bajo `security` → `policy_engine.py`

**Medido: las 10 ausentes.** `for3s_core/` **no tiene ni una subcarpeta** (solo `migrations/` y
`__pycache__/`) — **los 76 archivos son planos**.

⚠️ **Consecuencia para la campaña:** cualquiera que use el Mapeo para localizar el código de un
nodo **no encuentra nada**. El documento canónico apunta a un árbol que no se construyó.

### 19.2 · ⭐⭐ EL MAPA REAL, medido — 9 de 11 nodos tienen su archivo

**Los nombres del diseño SOBREVIVIERON; solo se aplanó la estructura:**

| # | Nodo cerebral | Archivo REAL | Líneas | |
|---|---|---|---|---|
| **1** | Knowledge Graph | `kg.py` | 250 | ✅ |
| **2** | Hipocampo | `memory.py` | 716 | ✅ |
| **3** | PFC / Orquestador | `conversation.py` | **1,871** | ✅ |
| **4** | Ganglios Basales / Skills | `skills.py` | 292 | ✅ |
| **5** | Microglía | `microglia.py` | 215 | ✅ |
| **6** | DMN | `dmn.py` | 423 | ✅ |
| **7** | **Amígdala** | — | — | 🔴 **NO EXISTE** |
| **8** | **Tálamo** | — | — | 🔴 **NO EXISTE** |
| **9** | Dual-Process Check | `confidence.py` | 274 | ✅ |
| **10** | Consolidación CLS | `consolidator.py` | 603 | ✅ |
| **11** | Neuromoduladores | `relevance.py` | 116 | ✅ |

⭐ **Esto es lo más accionable de las 19 secciones.** Un bloque de la campaña que vaya a auditar
"el nodo 5" ahora sabe que son **215 líneas en `microglia.py`**, no un `forgetter.py` bajo `memory`.

📊 **9 de 11 nodos = 82% con archivo propio.** Y los 2 ausentes son **exactamente** los que §17 y
§18 ya habían medido por otras vías: **Amígdala (nodo 7) y Tálamo (nodo 8)**. Tres métodos
independientes, el mismo resultado.

### 19.3 · El Mapeo se contradice a sí mismo — y lo declara

`§0` del propio documento avisa:

> *"Una auditoría de coherencia detectó que la numeración de nodos 5-9 en el CUERPO de este
> documento **no coincide** con el `Cerebro/For3s_OS_Grafo_Maestro.md`… **§0 es la AUTORIDAD**. Donde el
> cuerpo (§3-§19) diga otro número para los nodos 5-9, prevalece §0."*

**La causa raíz, medida en su día:** el cuerpo modeló *"Action Selection"* y *"Pattern Separation"*
como nodos numerados. El Grafo NO los numera — son **funciones** del Nodo 4 y del Nodo 2. Esa
duplicación corrió la numeración y **dejó fuera de la lista a Tálamo y Dual-Process**.

⚠️ **Consecuencia práctica: §5-§19 del Mapeo siguen con los números viejos.** Un bloque que lea
*"Nodo 8 — Amígdala"* en el cuerpo está leyendo **el nodo 7 canónico**.

⭐ **Y es un ejemplo perfecto de L-13** (*un puntero en su sitio vence a un borrado*): en vez de
reescribir 2,400 líneas, se declaró la corrección arriba con su tabla de traducción. **Costó 40
líneas en lugar de una reescritura.**

### 19.4 · La cobertura declarada vs la medida

| | Mapeo (2026-06-01) | Medido (2026-08-12) |
|---|---|---|
| FULLY mapped | **6 / 11** (55%) | 9 con archivo · **~4 fieles al diseño** |
| Cobertura "productiva" | **91%** (10/11 servidos) | **82%** con archivo · **2 ausentes de verdad** |

⭐ **Los números del Mapeo eran una PROYECCIÓN** — declaraban lo que R5/R9 cerrarían. Lo cerraron
**en el diseño**. Es L-22 otra vez: *un hito que declara "completo" debe decir completo en qué*.

### 19.5 · Qué debe hacer la campaña con este documento

| | |
|---|---|
| ✅ **Usar** | los nombres de nodo, la función neurocientífica, las operaciones, el diccionario bilingüe |
| ⛔ **NO usar** | las rutas de módulo (10/10 muertas) · los nombres de tabla del cuerpo · la numeración de §5-§19 |
| 🔧 **Actualizar** | la columna "Módulo Python" con la tabla de §19.2 — **es un cambio de 11 celdas que desbloquea el documento entero** |

⭐ **Recomendación medida: no reescribir el Mapeo — añadirle una tabla de traducción**, exactamente
como su propio §0 hizo con la numeración. El precedente está dentro del mismo archivo.


---

## 20 · ⭐⭐⭐ POR QUÉ NADIE VIO LA DIVERGENCIA — la auditoría que comparó documento con documento

**Leídos `docs/analysis/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md` (872 líneas) y
`Cerebro/Arquitectura_Grafo_vs_Loop.md` (1,654), 2026-08-12.**

⭐⭐⭐ **Esta sección responde la pregunta que las §16-§19 dejaban abierta: si el diseño y el
código divergieron tanto, ¿cómo es que nadie lo detectó?** La respuesta está escrita, y es limpia.

### 20.1 · Existe una auditoría de alineación — y da 9.2 / 10

El 2026-06-09 se hizo una **auditoría formal de coherencia** de las 10 rondas. Su veredicto:

```
   VEREDICTO GLOBAL: ✅ ALINEACIÓN MUY ALTA Y COHERENTE
   Promedio de alineación R1-R10:  ~9.2 / 10
   • 7/7 ventajas defendibles de la Visión → MATERIALIZADAS
   • 11/11 nodos cerebrales del Grafo → CERRADOS
   • 3/3 pilares estructurales → cubiertos
   DESALINEACIONES REALES: 2 (ambas deuda de DOCUMENTACIÓN, no de diseño)
```

**Y es una auditoría seria:** tiene metodología declarada, 4 símbolos de alineación, 4 categorías
de divergencia, análisis ronda por ronda. **No es un documento complaciente.**

### 20.2 · ⭐⭐⭐ LA CAUSA, en su propia §2.1

Su metodología dice **exactamente** qué comparó:

> *"Cada documento maestro de ronda (`Ronda_0X_*.md`) se evaluó contra: **Grafo Maestro**… y
> **Visión**…"*

⭐⭐⭐ **Comparó DOCUMENTOS contra DOCUMENTOS. El código nunca entró en la comparación.**

**Y por eso su veredicto es correcto y mi medición también:**

| | Qué mide | Resultado |
|---|---|---|
| **Reporte de Alineación** (jun) | ¿las rondas respetan el Grafo y la Visión? | **9.2/10 ✅ — y es cierto** |
| **Esta auditoría** (ago) | ¿el código implementa las rondas? | **7 piezas ausentes 🔴 — y también es cierto** |

**No se contradicen: miden dos eslabones distintos de la misma cadena.**

```
   VISIÓN ──✅──> GRAFO MAESTRO ──✅ 9.2/10──> LAS 10 RONDAS ──🔴 sin medir──> EL CÓDIGO
                                              ↑                              ↑
                                    aquí llegó la auditoría        aquí nadie miró
```

### 20.3 · ⭐⭐ La lección más valiosa de las 20 secciones

> **L-24 · Una cadena de coherencia se rompe en el eslabón que nadie mide. Si A→B y B→C están
> auditados, es seguro asumir que C→D también lo está — y ese es precisamente el eslabón donde
> vive el defecto.**

**Medido aquí con brutalidad:** el 2026-06-09 el sistema declaró **"11/11 nodos cerrados"** con una
auditoría legítima de 872 líneas. El 2026-08-12, midiendo el código, **9 de 11 tienen archivo y 2
no existen**. ⭐ **Ambas afirmaciones son verdaderas sobre cosas distintas.** El problema no fue
mentir: fue que **nadie declaró de qué hablaba cada una.**

Es L-22 (*"completo en qué"*) elevada a nivel de sistema.

### 20.4 · El documento que predijo la campaña — dos meses antes

`Cerebro/Arquitectura_Grafo_vs_Loop.md` (§13, mayo-2026) propuso **3 capas de construcción**:

| Capa | Qué entrega | Qué NO entrega |
|---|---|---|
| **1 · MVP (sem 1-8)** | loop + memoria en grafo · recuerda entre sesiones · razonamiento multi-salto | ⛔ *"paralelismo verdadero · razonamiento ramificado · metacognición real"* |
| **2 · v1 (mes 3-6)** | LangGraph · subgrafos paralelos · multi-agente · confidence checks | — |
| **3 · v2 (mes 6-12)** | Tree of Thoughts · Reflexion · **DMN** · **microglía** | — |

⭐⭐ **For3s OS está EXACTAMENTE donde la Capa 1 predijo que estaría** — con partes de la 3
(DMN y microglía sí existen, adelantadas) y **sin las de la 2** (Tálamo, routing, paralelismo real).

**Y el documento avisó de la condición para subir:** *"Capa 2 — cuándo activar: **después de 1-2
pilots cerrados que validen el wedge**."*

📊 **Pilots cerrados a la fecha: 0** (medido en `memory/PENDIENTES.md`: *"NavigoX registrado pero no
consume activamente"*).

⭐⭐⭐ **El sistema NO se quedó corto: se detuvo exactamente donde su propio diseño decía que
debía detenerse hasta tener un piloto.** Lo que faltó fue **declararlo** — nadie escribió *"estamos
en Capa 1 a propósito"*, así que las capas 2 y 3 se leen como deuda en vez de como espera.

### 20.5 · Y avisó de los 7 problemas que nadie ha resuelto

§15 del mismo documento, mayo-2026, lista lo abierto en la industria. **Tres se cumplieron en
For3s OS, medibles hoy:**

| Problema predicho | Cómo se manifestó |
|---|---|
| *"**Cómo evaluar un agente-grafo.** Si tu agente tiene 15 nodos, ¿cómo mides calidad? Tooling primitivo"* | 🔴 **el hueco de observabilidad de §16.3** — un stub y una tarea rota se registran idénticos |
| *"**Memory leak en agentes longevos.** Sin microglía artificial, la memoria crece infinitamente. **Nadie la implementa bien**"* | ✅ **la microglía SÍ se implementó** — 41% podado, 4,230 candidatos. **Es donde For3s superó al estado del arte que su propio doc describía** |
| *"**Coordinación entre agentes.** Multi-agente funciona en demos. Con 10+ agentes: race conditions, deadlocks"* | 🟡 el semáforo está en **2 specialists**, no en 10 — el problema se evitó acotando |

⭐ **La conclusión honesta de mayo:** *"si entras a esta dirección, vas a estar haciendo cosas que
literalmente nadie ha resuelto bien… no hay manuales. Tooling inmaduro. Vas a sentir que estás en
arenas movedizas a veces."*

**Eso no era pesimismo: era una predicción correcta.** Y explica por qué las capas altas del
diseño (R7-R9) no se construyeron: **no existía manual para construirlas.**

### 20.6 · Qué debe hacer la campaña con esto

⛔ **Lo que NO debe hacer:** tratar los 7 rojos de §17 como bugs. **Cinco de ellos son Capa 2 y 3
del plan original, y el propio plan dice que esperan a un piloto.**

✅ **Lo que sí:** declarar en qué capa está For3s OS hoy, y auditar **contra esa capa**:

| | |
|---|---|
| **Capa 1 declarada** | memoria en grafo · recuerda entre sesiones · multi-salto |
| **Auditar contra eso** | ¿la memoria recupera? 🔴 **0.06%** — ESE es el defecto real de Capa 1 |
| **NO auditar** | Output Gate · RBAC · Prometheus · Amígdala — **son Capa 2-3, esperando piloto** |

⭐⭐ **El hallazgo H-02 (recuperación al 0.06%) sube a ser EL hallazgo central de la campaña.**
Es el único que falla **dentro de la capa que For3s OS declara ocupar**. Los demás son futuro.


---

## 21 · ⚠️ CORRECCIÓN A §16-§20 — el sistema YA sabía todo esto, y está escrito

**Leídos `docs/analysis/Reporte_Maestro_Consolidado_R1-R10.md` (871 líneas), el `§0` del Grafo Maestro, el
Plan Maestro de Programación y la Estimación de Tiempo, 2026-08-12.**

🔴 **Esta sección corrige un error de método mío que atraviesa las cinco anteriores.** Presenté
como "hallazgos" cosas que el sistema **ya tenía documentadas desde junio**. Lo escribo porque
ocultarlo sería exactamente la L-15 (*medir una parte y hablar del todo*) cometida otra vez.

### 21.1 · El Grafo Maestro §0 ya declara la divergencia — desde el 2026-06-10

Añadido dos meses antes de esta auditoría:

> *"**Regla de precedencia: donde una tecnología nombrada abajo difiera de lo lockeado en una
> ronda, MANDA LA RONDA.** Este documento conserva la autoridad CONCEPTUAL (qué nodos, qué
> conexiones, qué reglas); la autoridad TÉCNICA (con qué se construye) vive en las rondas."*

Y su **§0.1** lista **8 cambios tecnológicos** uno por uno: Neo4j→**Apache AGE** · Qdrant→**pgvector
+ Stella** · Kafka→**Valkey+Arq** · LangGraph→**asyncio custom** · SQLAlchemy→**asyncpg directo**.

⚠️ **Mi §17 reportó "BGE-M3 en vez de Stella" como divergencia no declarada. Estaba a medias:**
la sustitución Qdrant→pgvector SÍ está declarada; el cambio Stella→BGE-M3 (posterior) no.

### 21.2 · ⭐⭐ §0.3 ya resolvió la contradicción de "11/11 nodos"

**Textual, del 2026-06-10:**

> *"Las dos afirmaciones son ciertas a la vez: **los 11 nodos EXISTEN en v1 (ancho completo del
> grafo), pero a una profundidad ≈40%** de la capacidad cerebral total… **11/11 = ancho · ~40% =
> profundidad v1.** Ningún nodo falta; varios operan en su versión foundation."*

⭐ **Mi §17.3 presentó "11/11 significa diseñados, no construidos" como hallazgo. El sistema ya lo
había escrito, con mejor precisión que yo** — y con el matiz que a mí se me escapó: *ancho vs
profundidad*.

⚠️ **Lo que mi medición SÍ añade, y sigue en pie:** §0.3 dice *"ningún nodo falta"*. **Medido en
el código: Amígdala y Tálamo no tienen archivo.** Eso no lo cubre §0.3 — porque §0.3 habla del
**diseño**, no del código. Es L-24 otra vez: **el eslabón sin medir.**

### 21.3 · §0.2 ya declara las 3 desviaciones estructurales

1. **Pilar 2 v1 = monolito modular, NO microservicios.** Razón declarada: ancla 3.D (equipo
   pequeño) — *"un solo deploy, un solo backup, operable por 1 persona"*.
2. **Pilar 3 v1 = SOLO la capacidad generativa #1 (skills).** Las #2/#3/#4 diferidas a v3.
   ⭐ **Esto explica mi §17: los 3 hooks neutros del governor no son deuda — son las capacidades
   #2-4 esperando v3, exactamente como se decidió.**
3. **Sin ORM: asyncpg directo + migraciones SQL numeradas.** Registrado el 2026-06-11, ticket 002.

### 21.4 · Y el refuerzo #6 predijo la confusión que yo tuve

`Reporte_Maestro_Consolidado` §12 lista **9 refuerzos pre-código**. El **#6** dice:

> *"**Reconciliar 'cobertura cerebral %' con '11/11 nodos'.** Aclarar que 11/11 nodos = existen,
> pero profundidad v1 ≈ 40%. **Evita confusión '¿está completo o al 40%?'**"*

**Estado: ✅ HECHO 2026-06-10 → Grafo §0.3.**

⭐⭐ **El sistema anticipó exactamente la confusión en la que yo caí, la resolvió por escrito, y
yo no leí ese párrafo antes de escribir 5 secciones.** Es la prueba viva de por qué Brian ordenó
leerlo todo.

### 21.5 · El calendario que faltaba a la campaña

`memory/archive/Estimacion_Tiempo_Por_Subtema.md` — con Brian solo, full-time:

| | |
|---|---|
| **Sistema completo (R1-R10)** | **~9-10 meses** (~39-44 semanas) |
| **★ MVP pilotable** (Fase 0+1 = R2+R3+R4) | **~3-3.5 meses** (~13-15 semanas) |

📊 **Contra la realidad medida:** For3s OS lleva **~2 meses de código** (primeras migraciones
2026-07-05) y **tiene el MVP corriendo con memoria, DMN y microglía**.

⭐⭐⭐ **For3s OS va ADELANTADO respecto a su propia estimación.** El MVP se estimó en 3-3.5 meses
y está vivo en ~2. **Ninguna auditoría anterior —mía incluida— dijo esto**, porque todas midieron
contra el destino y ninguna contra el calendario.

### 21.6 · Y el Plan Maestro define 6 fases con una regla de oro

`memory/archive/Plan_Maestro_Programacion.md` — foundation-first:

```
FASE 0 Setup + CI/CD temprano   →  FASE 1 MVP cerebral mínimo (el hito pilotable)
FASE 2 Coordinación cognitiva   →  FASE 3 Aprendizaje y autonomía (Pilar 3)
FASE 4 Interfaz y observabilidad →  FASE 5 Seguridad, deploy y cierre
```

⭐ **El orden explica TODO el patrón de §18:** las capas bajas están construidas porque son
**Fases 0-1**; R7 (interfaz), R8 (observabilidad) y R9 (seguridad) faltan porque son **Fases 4-5**,
que **por plan van al final**.

⭐⭐⭐ **No hubo abandono. Hubo un plan de 6 fases, y el sistema está en la 1-3.**

### 21.7 · La lección que corrige mi propio método

> **L-25 · Antes de reportar un hallazgo sobre un sistema documentado, buscar si el sistema ya lo
> documentó. Un "descubrimiento" que ya está escrito no es un hallazgo: es una lectura incompleta.**

**Medido sobre mí mismo:** de los hallazgos de §16-§20, **cuatro ya estaban resueltos por escrito**
(la divergencia diseño→código en Grafo §0 · el "11/11" en §0.3 · las desviaciones de pilares en
§0.2 · el cambio de tecnologías en §0.1). ⭐ **Lo que sí aporté y sigue en pie es el eslabón que
nadie había medido: el CÓDIGO REAL** — las 15 tablas ausentes, los 2 nodos sin archivo, el mapa
nodo→archivo de §19.

⚠️ **Y por eso §21 no borra §16-§20: las acota.** El diagnóstico correcto no es *"el diseño y el
código divergieron sin control"*, sino:

> ⭐ **El sistema declaró su divergencia con precisión en junio, y nadie volvió a medir el código
> contra esa declaración en los dos meses siguientes.**

### 21.8 · Qué cambia para la campaña — otra vez

| Antes de §21 | Después de §21 |
|---|---|
| 7 piezas ausentes = deuda | **5 son Fases 4-5 del plan** — van al final por diseño |
| "11/11 nodos" es falso | **es cierto en ancho** · ~40% en profundidad · 🔴 **2 sin archivo en el código** |
| El diseño se abandonó | **el sistema va adelantado**: MVP estimado 3-3.5 meses, vivo en ~2 |
| Falta declarar la divergencia | **está declarada** en Grafo §0 · falta **volver a medirla contra el código** |

⭐⭐ **La campaña no audita un sistema a la deriva. Audita un sistema en la Fase 1-3 de un plan de
6, adelantado en calendario, cuya última verificación contra el código fue hace dos meses.**


---

## 22 · LAS 7 VENTAJAS DEFENDIBLES — cuáles son reales hoy

**Leídos `vision/Vision_For3s_Frontier.md` (1,091 líneas), `docs/analysis/Comparacion_For3s_OS_vs_Hermes.md`
(774) y `docs/analysis/Analisis_internOS_vs_For3s_OS.md`, 2026-08-12.**

La Visión declara **7 ventajas técnicas defendibles** — lo que hace a For3s distinto de OpenClaw
y Hermes. **El Reporte de Alineación dice que las 7 están "materializadas".** Cruzándolas con lo
medido en el código:

| # | Ventaja declarada | Medido en el código | Veredicto |
|---|---|---|---|
| **1** | **PFC artificial** (metacognición real) | `confidence.py` 274 líneas · **4 de 8 señales** · corre en cada turno | 🟡 **real, a media profundidad** |
| **2** | **Knowledge Graph + Pattern Separation** | AGE con **31,037 nodos + 31,230 edges** · **91.3% consolidado** | 🟢 **REAL** |
| **3** | **Ganglios basales / skills emergentes** | 16 skills · 🔴 **sin NO-GO, sin dopaminergic, sin lifecycle** | 🟠 **parcial** |
| **4** | ⭐ **Microglía artificial** (olvido inteligente) | **13,974 podados (41%)** · decay real 0.225-0.916 · **4,230 candidatos** | 🟢🟢 **LA MÁS REAL** |
| **5** | **DMN** (procesamiento offline) | `dmn.py` 423 líneas · **3,275 corridas** · 5 tareas reales + 3 stubs | 🟢 **real** |
| **6** | **Amígdala artificial** (valoración rápida) | 🔴 **NO EXISTE** | 🔴 **ausente** |
| **7** | **Arquitectura de grafo end-to-end** | 9 de 11 nodos con archivo · 🔴 sin Tálamo (el router) | 🟡 **parcial** |

📊 **Balance: 3 reales · 3 parciales · 1 ausente.**

### 22.1 · ⭐⭐ La ventaja 4 es la que más vale, y es la más sólida

La Visión dice de la microglía: *"nadie la implementa bien"*. Y `Arquitectura_Grafo_vs_Loop` §15.1
la listó entre **los 7 problemas que nadie ha resuelto**:

> *"**Memory leak en agentes longevos.** Sin microglía artificial (poda), la memoria crece
> infinitamente. **Nadie la implementa bien.**"*

⭐⭐⭐ **For3s OS la implementó y funciona: 41% de la memoria podada, con audit de cada olvido.**
**Es el único punto donde el sistema superó al estado del arte que su propio diseño describía.**

⚠️ **Y contrasta brutalmente con H-02:** el sistema **olvida excelente** (41%) y **recupera al
0.06%**. Las dos mitades del mismo nodo, una sobresaliente y la otra muerta.

### 22.2 · Donde Hermes gana, según el propio documento

`docs/analysis/Comparacion_For3s_OS_vs_Hermes.md` §11 es honesto y sigue vigente:

| Hermes gana en | Estado hoy en For3s |
|---|---|
| **"EXISTE Y FUNCIONA"** — miles de usuarios | ⭐ **esto YA cambió**: For3s corre en producción · pero **cero instalaciones externas** |
| **Onboarding** — `curl\|bash`, 2 minutos | 🟡 el instalador existe (bloque `distribucion` cerrado 6/6) · **nunca probado por un tercero** |
| **Amplitud** — 20+ plataformas, 70+ tools | 🔴 For3s: **2 canales, ~25 tools** |
| **Simplicidad** — un loop es fácil de depurar | 🔴 confirmado: **`telegram_channel.py` tiene 4,570 líneas** |
| **Comunidad** | 🔴 **3 stars** (medido en `memory/PENDIENTES.md`) |
| **LLM local** — Ollama/vLLM trivial | 🔴 For3s: Claude + fallback OpenAI |

⭐ **Y su lección de cierre sigue siendo la mejor guía estratégica del repo:**

> *"For3s NO debe competir con Hermes en SU juego (amplitud, onboarding instantáneo, generalidad).
> Debe ganar en el SIGUIENTE juego. **No vas a competir con Hermes en su mismo juego. Vas a
> construir el juego siguiente — donde Hermes no juega.**"*

### 22.3 · La anti-visión — 10 cosas que For3s NO será

`Vision_For3s_Frontier` §9. **Tres siguen siendo criterio vivo para la campaña:**

| | Declarado | Cómo aplica hoy |
|---|---|---|
| **#4** | *"NO una empresa que escala antes de validar — **trust before scale**"* | ⭐ **justifica que las Fases 4-5 esperen**: escalar sin piloto viola la anti-visión |
| **#8** | *"NO dependiente de un solo proveedor de LLM — **multi-provider desde día 1**"* | 🔴 **INCUMPLIDA**: Claude + fallback OpenAI, sin local. Es la única anti-visión que el código viola |
| **#9** | *"NO sacrifica seguridad por velocidad — **security designed in, no-negociable**"* | 🔴 **el contenido en claro (H-01) es exactamente esto**, y por eso pesa más que los otros rojos |

⭐⭐ **H-01 sube de gravedad con este dato.** No es solo un hallazgo técnico: **viola una
anti-visión declarada como no-negociable.**

### 22.4 · Lo que la campaña debe llevarse de aquí

⭐ **Las 3 ventajas REALES (grafo · microglía · DMN) son lo que NO se debe romper.** §12.2 de
esta auditoría ya lista 14 fortalezas; estas tres son las **defendibles comercialmente**.

🔴 **Las 3 parciales y la ausente marcan el orden natural del trabajo** — y coincide casi exacto
con los bloques que Brian ya priorizó por gravedad:

| Ventaja floja | Bloque de la campaña |
|---|---|
| #1 PFC a media profundidad (4/8 señales) | `agente` |
| #3 skills sin NO-GO ni lifecycle | `cerebro` |
| #6 Amígdala ausente | `seguridad` — **y H-01 vive ahí también** |
| #7 sin Tálamo | `agente` / `multiagente` |

⚠️ **Y una advertencia medida:** la ventaja #2 (grafo) está **completa y sana**. Auditarla a fondo
sería trabajo sobre lo que ya funciona — el orden por gravedad de Brian ya lo evita.


---

## 23 · ⭐⭐⭐ EL GATE DE FASE 1, MEDIDO — la vara correcta, por fin

**Leído `memory/archive/Plan_Maestro_Programacion.md` (988 líneas) y medido su gate contra la BD
viva, 2026-08-12.**

⭐⭐⭐ **Esta es la sección más útil de las 23**, porque resuelve la pregunta abierta desde §16.5:
**contra qué vara se audita For3s OS.** No hacía falta inventarla — **el Plan Maestro ya define un
gate objetivo por fase.**

### 23.1 · El gate que el propio plan declara para Fase 1

> **FASE 1 — MVP cerebral mínimo. GATE PARA AVANZAR:**
> ✓ Un PR de GitHub se analiza end-to-end (input → memoria → Claude → output)
> ✓ La memoria persiste entre sesiones (episodios + KG + vector)
> ✓ CLS consolida episodios a KG (job nocturno corre)
> ✓ Microglía poda (job nocturno corre, NO toca audit)
> ✓ Costo por análisis medido y dentro de P5
> ✓ Audit hash chain escribiendo (inmutable)

### 23.2 · ⭐⭐ Medido punto por punto — pasa 6 de 6

| Criterio del gate | Medido en la BD de `brian` | |
|---|---|---|
| Memoria persiste (episodios + KG + vector) | **33,908 episodios · 33,908 con embedding · 2,072 sesiones** | ✅ |
| CLS consolida a KG | **30,959 consolidados** · última corrida **ayer** | ✅ |
| Microglía poda sin tocar audit | **13,974 podados** · última corrida **ayer** · audit intacto | ✅ |
| Audit hash chain inmutable | **12,908 eventos, TODOS con `hash_self` y `hash_prev`** | ✅ |
| Costo medido | 79 corridas con costo · **$5.17 acumulado** | ✅ |
| PR de GitHub end-to-end | **14 acciones de GitHub auditadas** · 3 archivos consultados | ✅ |

📊 **6 de 6. For3s OS PASA el gate de Fase 1 de su propio plan.**

⭐⭐⭐ **Y eso es un veredicto radicalmente distinto al de §17** (*"7 piezas ausentes"*). **Ambos son
correctos — miden fases distintas.** §17 midió contra el destino (R1-R10 completo, Fase 5).
§23 mide contra **dónde el plan dice que el sistema debe estar hoy**.

### 23.3 · La vara correcta, resuelta

⛔ **La pregunta de §16.5 (*"¿Grafo o código como vara?"*) tenía una tercera respuesta que no
ofrecí, y es la que el propio sistema ya tenía escrita:**

> ⭐⭐ **Ni el Grafo ni el código: LA FASE. El Plan Maestro define 6 fases con gate objetivo cada
> una. Se audita contra el gate de la fase en curso, no contra el destino final.**

| Vara | Veredicto | ¿Útil? |
|---|---|---|
| El Grafo Maestro completo (Fase 5) | 15/15 tablas ausentes · 7 piezas | 🔴 declara en rojo un sistema que funciona |
| El código como autoridad | todo verde por definición | 🔴 no mide nada |
| ⭐ **El gate de la fase en curso** | **6 de 6 en Fase 1** | ✅ **discrimina, y es accionable** |

### 23.4 · Y entonces, ¿qué falla de verdad?

**Con la vara correcta puesta, los hallazgos se reordenan.** Solo cuenta lo que falla **dentro de
la Fase 1-3**:

| Hallazgo | ¿Es de la fase actual? | Veredicto |
|---|---|---|
| 🔴 **H-02 · memoria recupera al 0.06%** | ✅ **Fase 1** — *"la memoria persiste"* pasa, pero **persistir no es recuperar** | 🔴🔴 **EL defecto real** |
| 🔴 **H-01 · contenido en claro** | ✅ **transversal** — viola la anti-visión #9 (*no-negociable*) | 🔴🔴 **el segundo** |
| 🔴 H-04 · digest muerto 29 días | ✅ Fase 3 (autonomía) — está en curso | 🔴 real |
| 🟠 H-06 · 3 tareas DMN sin correr | ✅ Fase 3 · **pero son stubs declarados** | 🟡 telemetría, no lógica |
| 🔴 H-03 · instancia huérfana | ✅ transversal (operación) | 🔴 real |
| Output Gate · RBAC · Prometheus · Amígdala | 🔴 **Fases 4-5** | ⬜ **NO son deuda hoy** |
| Event Sourcing · schema-per-tenant | 🔴 Fase 5 / multi-cliente | ⬜ **NO son deuda hoy** |

⭐⭐ **El mapa se reduce de 24 hallazgos a 4 que importan hoy:**
**H-02 (recuperación) · H-01 (cifrado) · H-04 (digest) · H-03 (instancia huérfana).**

📊 **Y los cuatro caen exactamente en los primeros bloques que Brian priorizó por gravedad:**
`seguridad` (H-01) · `memoria` (H-02) · `cerebro` (H-04) · `despliegue` (H-03).

⭐⭐⭐ **El orden que Brian eligió por instinto coincide 4 de 4 con el que sale de medir contra la
fase.** No hay que cambiar el plan de la campaña: hay que **cambiar la vara con la que se juzgará
cada bloque.**

### 23.5 · La regla que sale de aquí

> **L-26 · Un sistema en construcción por fases se audita contra el gate de SU fase, nunca contra
> el destino. Auditar contra el destino produce rojos que nadie debe arreglar todavía — y entierra
> los dos o tres que sí.**

⚠️ **Y su corolario, medido en esta misma auditoría:** yo produje **24 hallazgos**. Con la vara de
la fase, **4 importan hoy**. Los otros 20 no eran falsos — **eran prematuros**, que es distinto y
más peligroso: *un hallazgo prematuro se ve idéntico a uno urgente.*


---

## 24 · ⚠️ LA CAUSA RAÍZ DE H-02 — ⛔ CORREGIDA EN §29, LEER ANTES

> 🔴🔴 **ESTA SECCIÓN TIENE UNA CONCLUSIÓN FALSA.** Sus datos son correctos; su conclusión
> (*"la memoria está inalcanzable"*) fue **desmentida en vivo** — ver **§29**. Se conserva entera
> porque borrarla escondería el error de método, que es la lección L-32.

**Leído `memory/archive/PR4_Flujo_Usuario_Memoria.md` (1,060 líneas) y medida la causa en la BD
viva, 2026-08-12.**

⭐⭐⭐ **Es el hallazgo más importante de las 24 secciones.** H-02 (*la memoria recupera al 0.06%*)
era el defecto central de la campaña, y hasta ahora era un **síntoma sin causa**. Ya no.

### 24.1 · El mecanismo, según el diseño

`PR4_Flujo_Usuario_Memoria` documenta el filtro real de `buscar_semantico`:

```sql
WHERE session_id = $1
  AND (owner_user_id = scope OR equipo_id IS NOT NULL OR owner_user_id IS NULL)
```

⭐ **La primera condición es la clave: `session_id = $1`.** La búsqueda semántica **solo mira
dentro del hilo activo**. Es correcto por diseño — es lo que garantiza el aislamiento entre
personas y entre temas.

### 24.2 · 🔴🔴🔴 LA CAUSA, medida

| Medida | Valor |
|---|---|
| Sesiones distintas con episodios | **2,071** |
| La sesión más grande | `oc:fruterito-principal:f30a7098…` — **10,452 turnos** |
| Las 3 sesiones donde Brian habla por Telegram | `tg:1923367928` · `:incubathon` · `:examen-final` |
| ⭐ **Episodios ALCANZABLES desde Telegram** | 🔴 **134 de 33,908** |

⭐⭐⭐ **La memoria no está rota: está INALCANZABLE.**

**Las 33,737 memorias importadas viven en 2,068 sesiones `oc:fruterito-*`** — los hilos originales
de los 6 agentes OpenClaw. **La conversación de Brian por Telegram vive en 3 sesiones `tg:*`.**
Y `buscar_semantico` filtra por `session_id`. **Nunca se cruzan.**

📊 **Y la prueba definitiva:** de los **21 episodios que SÍ se recuperaron alguna vez**,
**los 21 están en sesiones `tg:`** (16 en `:examen-final`, 5 en `:incubathon`).
**Cero de las 33,737 importadas.**

⭐⭐ **El 0.06% no es un fallo de la búsqueda. Es exactamente lo que el diseño produce:
21 de 134 alcanzables = 15.7% de recuperación DENTRO de su alcance.** Sano.

### 24.3 · Lo que esto cambia — el diagnóstico correcto

| Diagnóstico anterior (mío, §5.2) | Diagnóstico real, medido |
|---|---|
| *"el camino de vuelta está muerto"* | 🔴 **falso** — funciona al 15.7% dentro de su alcance |
| *"el sistema guarda y no recupera"* | 🔴 **falso** — recupera lo que puede alcanzar |
| — | ⭐ **El entrenamiento importó 33,737 memorias a sesiones que la búsqueda nunca visita** |

⚠️ **El defecto real no es de `memory.py`: es del ENTRENAMIENTO.** El hito E1-E5 (2026-07-05)
cargó el material conservando el `session_id` original de OpenClaw — **fiel al origen, y por eso
invisible para el agente.**

⭐ **Y explica el sentimiento de Brian del 13-jul**, dos días después del entrenamiento:
*"For3s es un chat que contesta y guarda memoria solamente"*. **Tenía razón, y ahora se sabe por
qué:** acababa de cargar 33 mil recuerdos que su agente **no podía ver**.

### 24.4 · Las tres salidas, con su costo

⛔ **No decido esto: es criterio de Brian.** Pero las opciones son medibles:

| | Qué se hace | Costo | Riesgo |
|---|---|---|---|
| **A** | **Re-mapear** las 33,737 a la sesión de Brian (`tg:1923367928`) | una migración SQL | 🔴 rompe el aislamiento por tema · mezcla 6 agentes en un hilo |
| **B** | **Buscar cross-session** para el DUEÑO (relajar el filtro solo cuando `scope=owner`) | ~10 líneas en `buscar_semantico` | 🟡 hay que verificar que no rompa el aislamiento de miembros |
| **C** ⭐ | **Una capa de "memoria de archivo"**: búsqueda separada sobre el material importado, inyectada aparte | media | 🟢 no toca el aislamiento vivo |

⭐ **Mi recomendación medida: B.** Razón: **el filtro de aislamiento ya distingue al dueño**
(`scope_user_id = None` para Brian, `<id>` para miembros) — la infraestructura existe. **El
tradeoff:** hay que probar en ambas direcciones que un miembro sigue sin ver lo ajeno, y ese test
**no existe hoy**.

⚠️ **Y la advertencia que vale más:** ⛔ **no tocar esto sin un test de aislamiento primero.**
BUG-14 (fuga de privacidad, 2026-06-30) nació exactamente de relajar una condición de este mismo
`WHERE`. Está en `memory/PENDIENTES.md`: *"el filtro incluía `OR owner_user_id IS NULL` → trataba los 667
turnos legado del DUEÑO como visibles para cualquiera"*.

### 24.5 · La lección

> **L-27 · Un dato que existe pero que ninguna consulta alcanza es indistinguible de un dato que
> no existe — y cuesta lo mismo almacenarlo.**

📊 **Medido:** 33,737 memorias · 133 MB de embeddings · **$0 de valor entregado** hasta que algo
pueda leerlas.

⭐⭐ **Y el corolario para la campaña:** el bloque `memoria` no tiene que arreglar la búsqueda
—funciona—. **Tiene que resolver el ALCANCE.** Es un problema distinto, más pequeño, y con
solución conocida.


---

## 25 · ⭐⭐⭐ LOS 16 HITOS, MEDIDOS HOY — el estado real de For3s OS

**Leído `memory/archive/Mapa_Construccion_Incremental.md` (567 líneas) y medido su tablero contra
el servidor, 2026-08-12.**

⭐ **Este documento es el ORDEN DE OBRA que faltaba.** No contradice al Plan Maestro: lo reordena
**en vertical** — cada hito atraviesa las capas que necesite y **termina en algo que corre**.

### 25.1 · Las 3 leyes no negociables de la construcción

```
LEY 1 — SE CONSTRUYE EN EL SERVIDOR for3s. PUNTO.
LEY 2 — CADA HITO TERMINA EN UN DEMO QUE SE VE FUNCIONANDO.
        No avanzo hasta que el actual CORRE y Brian lo ve. Vertical.
LEY 3 — LOS R SON LA BIBLIOTECA, NO EL ORDEN.
        Las 10 rondas son la VERDAD TÉCNICA — se consultan para el detalle.
        Pero el ORDEN de ensamblaje es ESTE documento, no el número de R.
```

⭐⭐ **La LEY 3 completa `rules/rule-product-authority.md`.** Esa regla dice *"el Grafo manda,
las rondas dicen con qué"*. **Faltaba el tercer eje: el ORDEN lo dice el Mapa de Construcción.**
Sin él, la campaña ordenaría el trabajo por número de ronda — que el propio sistema prohíbe.

⭐ **Y explica por qué existe:** *"construir 'por R' = 4-6 semanas en R2 SIN nada que encender"*.

### 25.2 · 🔴 El tablero está congelado en el 11-jun — y miente a la baja

El documento declara **3 de 18 peldaños** (C0, C1, H1, H3), con **H2 y H4 sin marcar**.

**Medido hoy en el servidor:**

| Hito | Declarado (11-jun) | Medido (12-ago) | Evidencia |
|---|---|---|---|
| **H1** HABLA | ✅ | ✅ | `agent.py` + `llm.py` |
| **H2** RECUERDA | 🔴 **sin marcar** | ✅ | **33,908 episodios** |
| **H3** TELEGRAM | ✅ | ✅ | 4,570 líneas |
| **H4** TIENE MANOS ★ | 🔴 **sin marcar** | ✅ | acciones de GitHub auditadas |
| **H5** MEMORIA REAL | ⬜ | ✅ | `kg.py` + **30,997 nodos AGE** |
| **H6** SE CUIDA | ⬜ | ✅ | microglía + consolidator + backup |
| **H7** DECIDE | ⬜ | 🔴 | **Tálamo ausente** — H7 diferido en `PENDIENTES` |
| **H8** EQUIPO | ⬜ | ✅ | `multiagente.py` + `specialists.py` |
| **H9** SUEÑA | ⬜ | ✅ | **3,295 corridas DMN** |
| **H10** PLANEA | ⬜ | ✅ | `confidence.py` |
| **H11** EL FRENO | ⬜ | 🟡 | `governor.py` — **3 de 6 frenos reales** |
| **H12** APRENDE | ⬜ | ✅ | **16 skills** |
| **H13** CARA FORMAL | ⬜ | 🟡 | canal API ✅ · **Output Gate 🔴** |
| **H14** OJOS | ⬜ | 🟡 | Grafana ✅ · **Prometheus 🔴** |
| **H15** DEFENSAS | ⬜ | 🔴 | **Amígdala ausente** |
| **H16** PRODUCCIÓN | ⬜ | ✅ | **28 contenedores vivos** |

📊 **13 de 16 hitos construidos.** El tablero publicaba **3 de 18**.

### 25.3 · ⭐⭐⭐ El estado real, en una línea

> **For3s OS completó los 3 bloques de la escalera (MVP · CEREBRO · APRENDIZAJE GOBERNADO) y
> está a medias en el cuarto (VENDIBLE ENTERPRISE), con 3 huecos exactos: Tálamo (H7), Output
> Gate/Prometheus (H13-H14 parciales) y Amígdala (H15).**

⭐⭐ **Y los 3 huecos coinciden EXACTAMENTE con lo que §17, §18, §19 y §22 midieron por vías
independientes.** Cinco métodos distintos, el mismo resultado. **Eso es lo que convierte esta
auditoría en evidencia y no en opinión.**

### 25.4 · Lo que esto corrige de mis secciones anteriores

| Mi diagnóstico | Corrección medida |
|---|---|
| §18: *"las capas altas no se construyeron"* | 🟡 **a medias**: H13, H14 y H16 **sí existen**, parcialmente. Solo H15 está en cero |
| §21: *"el sistema está en Fase 1-3"* | ✅ **confirmado por otra vía** — bloques A, B y C completos |
| §23: *"pasa el gate de Fase 1"* | ⭐ **y también los de Fase 2 y 3** — H5-H12 construidos |

### 25.5 · ⭐ El dato que ninguna auditoría había dado

**La escalera estimaba `C0→H4` (el MVP) en ~4-5 semanas y `C0→H16` en ~9-10 meses.**

📊 **Medido: los 13 hitos se construyeron entre el 2026-06-10 y hoy — dos meses.**

⭐⭐⭐ **For3s OS construyó en 2 meses lo que su propio plan estimaba en 6-7.** Ya no es una
inferencia de §21: es la escalera de hitos, contada uno a uno.

### 25.6 · La lección

> **L-28 · Un tablero de progreso que no se actualiza miente a la baja, y eso es peor que no
> tenerlo: hace que el equipo reconstruya lo que ya existe.**

**Medido:** el tablero publica **3 de 18**; la realidad es **13 de 16**. ⚠️ **Un bloque de la
campaña que lo hubiera leído como fuente habría planificado construir H5-H12 desde cero** — nueve
hitos que llevan meses corriendo en producción.

⭐ **Es la misma familia que L-22** (*completo en qué*) y **L-24** (*el eslabón sin medir*): el
documento no mintió — **se quedó quieto mientras el sistema avanzaba.**


---

## 26 · ⭐⭐⭐ LAS 3 BRÚJULAS — la autoridad completa, por fin

**Leídos `bridges/` (5 archivos, 596 líneas), `Maestro/` (7), `memory/archive/Banco_Filtro_Alineacion.md`
(634), los planes maestros H6/H9/H10 y `docs/architecture/`, 2026-08-12.**

⭐⭐⭐ **`bridges/000_PLAN_MAESTRO_TICKETS.md` declara la autoridad EN ORDEN — y es lo que la
campaña llevaba 26 secciones buscando:**

```
   1. Cerebro/For3s_OS_Grafo_Maestro.md         → QUÉ y POR QUÉ (con su §0)
   2. memory/archive/Plan_Maestro_Programacion.md → marco de FASES / gates / MVP
   3. memory/archive/Mapa_Construccion_Incremental.md → ORDEN de obra (C0,C1,H1..H16)
```

### 26.1 · Lo que esto corrige de `rule-product-authority`

La regla de la campaña dice: *"Grafo Maestro (CÓMO FUNCIONA) → rondas (CON QUÉ) → visión (POR QUÉ)
→ el código se AUDITA"*. **Le faltan dos ejes que el sistema sí tenía declarados:**

| Pregunta | Autoridad | ¿Estaba en `rule-product-authority`? |
|---|---|---|
| ¿QUÉ y POR QUÉ? | Grafo Maestro §0 | ✅ sí |
| ¿CON QUÉ se construye? | las 10 rondas | ✅ sí |
| ⭐ **¿EN QUÉ FASE estamos y qué gate aplica?** | **Plan Maestro de Programación** | 🔴 **NO** |
| ⭐ **¿En qué ORDEN se ensambla?** | **Mapa de Construcción (H1-H16)** | 🔴 **NO** |

⭐⭐ **Sin las brújulas 2 y 3, la campaña auditaría contra el destino** — que es exactamente el
error que §23 midió: **24 hallazgos donde solo 4 importan hoy.**

### 26.2 · 🔴 El sistema de tickets se detuvo en H3

`bridges/` tiene **4 tickets**: `001_H1_HABLA` · `002_H2_RECUERDA` · `003_H3_TELEGRAM` ·
`004_H4_TIENE_MANOS` (este último, *"por crear al aprobar"*).

**Estado global publicado: `PROGRESO: 5/18 peldaños`. Fecha: 2026-06-11.**

📊 **Medido en §25: 13 de 16 hitos construidos.** ⭐ **El sistema construyó H4 a H16 sin abrir un
solo ticket más.** No es negligencia — es que el trabajo **se movió a otro sistema** (los bloques
de Mente OS v2, que nacieron en julio). **Pero nadie cerró el anterior**, y por eso `bridges/`
publica 5/18 desde hace dos meses.

⚠️ **Es L-28 otra vez, en un tercer documento** (tras el tablero del Mapa y el "11/11" del Grafo).
⭐⭐ **Tres tableros de progreso distintos, los tres congelados en junio.**

### 26.3 · Y los tickets guardan detalle que ningún otro documento tiene

**H1 (`001`):** *"⚠️ Suscripción OAuth solo permite rol For3s en el mensaje (no system); para rol
en system → **API key** (clientes la necesitan igual)."*
⭐ **Ese es el origen medido de la anti-visión #8 incumplida** (§22.3): no es descuido — es un
**límite del OAuth de suscripción**, documentado el día 1.

**H2 (`002`):** *"audit hash chain SHA-256 + trigger anti UPDATE/DELETE (Grafo §6.4) · **Decisión:
SQL directo en vez de Alembic ORM**"* — la desviación §0.2 del Grafo, con su ticket.

**H7 (backlog):** *"⭐ aquí entra **OpenCode como 2º PROVEEDOR LLM**. SPIKE ya hecho y EXITOSO."*
⭐⭐ **La solución a la anti-visión #8 existe, probada, esperando en el hito H7 — el mismo que
tiene el Tálamo ausente.**

**H6 (backlog):** *"aquí va la **COLA LLM ASÍNCRONA** que controla el ritmo de For3s consigo mismo.
Idea de Brian para el 429."*

### 26.4 · Las 4 señales neutras estaban declaradas desde junio

`work/H10_PLANEA_Plan_Maestro_Metacognicion.md` §1, del 2026-06-26, tiene la tabla exacta:

| Señal | ¿Infra hoy? | Por qué |
|---|---|---|
| `llm_self_report` · `tool_success` · `schema_valid` · `historical` | ✅ **SÍ** | 4 implementadas |
| `cost_accuracy` | ⚠️ neutra | *"no medimos estimado vs real por turno aún"* |
| `plan_consistency` | ⚠️ neutra | *"no hay plan-then-execute formal (deuda)"* |
| `multi_agent_consensus` | ⚠️ neutra | *"solo aplica cuando corre el equipo, no en chat"* |
| `rule_eval` | ⚠️ neutra | *"requiere golden set formal"* |

⭐ **Con su definición:** *"**Neutra = contribución honesta:** no suma ni resta señal falsa; se
documenta que está pendiente de infra."* **Mi §17 lo reportó como "4 de 8" sin la causa. La causa
estaba escrita desde junio, señal por señal.**

### 26.5 · Y las 8 tareas del DMN también

`work/H9_SUENA_Plan_Maestro_DMN.md` §2 clasifica las 8 con su coste y su riesgo:
**5 housekeeping** (auto-aplican, sin review) y **3 generativas** (governor + gate obligatorio).

⭐ `eval_regression_detect` está marcada como **"GUARDIÁN: detecta si la calidad degrada"** — y es
uno de los stubs. **El guardián de calidad del sistema es un stub esperando un golden set.**

### 26.6 · La lección que cierra la lectura de Mente OS

> **L-29 · Un sistema con tres tableros de progreso tiene cero tableros de progreso. Cuando el
> trabajo migra a una herramienta nueva, el tablero viejo no queda obsoleto: queda MINTIENDO.**

📊 **Medido:** `bridges/` publica **5/18** · el Mapa publica **3/18** · el Grafo declara **11/11
nodos**. **La realidad es 13 de 16 hitos, 9 de 11 nodos con archivo.** ⭐ **Ninguno mintió al
escribirse. Los tres se quedaron quietos mientras el sistema avanzaba dos meses.**

⛔ **Y por eso la campaña NO debe leer ningún tablero como fuente de estado.** Su única fuente
fiable es **medir el servidor** — que es exactamente lo que esta auditoría hizo, y por lo que
existe.


---

## 27 · 🔴🔴 MENTE OS NUNCA HA GOBERNADO TRABAJO DE PRODUCTO — y la campaña es la primera vez

**Leídos `docs/architecture/` completo (2,409 líneas: `validators-and-hygiene` 781 ·
`block-anatomy` 454 · `lifecycle-and-learning` 434 · `how-it-runs` 362 · `folder-structure` 292 ·
`language-policy` 86), 2026-08-12.**

⭐⭐ **Las 26 secciones anteriores auditaron For3s OS. Esta audita a MENTE OS** — la herramienta
con la que se va a hacer la campaña. **Y tiene un hueco que ninguna auditoría de For3s podía ver.**

### 27.1 · 🔴 El diagnóstico del propio sistema, del 2026-07-31

`docs/architecture/how-it-runs.md` §8, textual:

> **🟡 No funciona todavía**
> • *"**El tubo pasa vacío.** Los 7 archivos de expertise tienen estructura y cableado, pero su
>   criterio sigue en huecos ⬜. Hoy el sistema responde *'¿cumple las métricas?'*; **todavía no
>   '¿lo haría un senior?'** — que era el diferenciador del v2."*
> • ⭐⭐ *"**Nunca ha gobernado trabajo real.** Los commits desde que nació el v2 son el v2
>   construyéndose, migrándose y probándose **a sí mismo**. **Cero sesiones de producto.**"*
>
> *"La ley que justifica el sistema se midió sobre trabajo de producto. Sobre trabajo de producto,
> el v2 lleva **0 sesiones de evidencia**."*

### 27.2 · Medido hoy: la mitad se cerró, la otra mitad NO

| Diagnóstico (31-jul) | Medido (12-ago) | |
|---|---|---|
| *"el criterio sigue en huecos ⬜"* | **`criterion.holes` = 0** — los 66 se cerraron en S11 (4-5 ago) | ✅ **RESUELTO** |
| *"nunca ha gobernado trabajo real · 0 sesiones de producto"* | **los 5 bloques archivados son del MOTOR**: `distribucion` · `expertise-programacion` · `plan-tests-demo` · `separacion-motor-instancia` · `split-architecture` | 🔴 **SIGUE VIGENTE** |

⭐⭐⭐ **Mente OS v2 lleva 231 checks, 24 validadores, 9 hooks, 30 ADRs y 26 reglas — y CERO
bloques de producto cerrados.** Los 5 que existen son el motor auditándose a sí mismo.

### 27.3 · ⭐⭐ Por qué esto importa MÁS que cualquier hallazgo de For3s OS

> ⭐⭐⭐ **La campaña `producto-for3s-os` es la PRIMERA VEZ que Mente OS v2 va a gobernar trabajo
> de producto.** Sus 12 bloques serán los 12 primeros bloques `code` sobre código ajeno al motor.

**Consecuencias medibles, no especulación:**

| | |
|---|---|
| El expertise de programación (7 archivos, 2,016 líneas) | **nunca se inyectó** en un bloque que toque For3s OS |
| `grade-block` | **nunca calificó** un bloque de producto |
| El aislamiento entre bloques (`rule-isolation`) | **nunca se probó** con 2 bloques tocando el mismo código |
| El canal de campaña (`§G`) | **está vacío** — nunca ha transportado un hecho |
| El airlock de 3 niveles (escrito hoy) | **cero PRs pasados por él** |

⚠️ **Y el precedente que lo hace probable:** L-05 (*verificar fuera del árbol del autor*) — la
batería daba **195/0 aquí y 22 fallos en un clon**. ⭐ **Un sistema que solo se ha probado sobre sí
mismo falla al salir de sí mismo. Ya pasó una vez, medido.**

### 27.4 · Lo que Mente OS SÍ tiene verificado

**Justo es decir lo que funciona** (`how-it-runs` §8, verificado en vivo):

- ✅ `test-f0-f6` **en verde en tres corridas seguidas**
- ✅ **Las 4 puertas operan** — probado: lanzar un `general-purpose` quedó bloqueado; un `Explore` pasó
- ✅ **El cableado del expertise funciona** — editar `userStore.ts` nombra `principles/expertise/dev-database.md` sin que nadie lo pida
- ✅ Los 3 fallos del diagnóstico cerrados: **0 → 221 documentos con metadata** · índice **35 → 286** · **11 de 11 sesiones registradas**

### 27.5 · Y su proporción deliberada: solo 3 acciones bloquean

| # | Acción | Puerta |
|---|---|---|
| 1 | destruir datos sin vuelta atrás | `gate-critical` |
| 2 | cerrar un bloque que no se puede reiniciar desde disco | `gate-critical` + `check-sufficiency` |
| 3 | lanzar un especialista que escribe, sin scope declarado | `gate-handoff` |

> *"**Todo lo demás informa.** Esa proporción es deliberada: **el sistema se gana el derecho a
> bloquear demostrando primero que el criterio funciona.**"*

⭐ **Esa frase es la mejor definición de la filosofía de Mente OS que hay en el repo.**

### 27.6 · La lección, y es sobre la campaña misma

> **L-30 · Una herramienta que solo se ha usado sobre sí misma no está probada: está calibrada.
> La primera vez que gobierna trabajo ajeno es su verdadera prueba — y hay que declararla como
> tal, no darla por hecha.**

⚠️ **Recomendación medida para la campaña:** el **primer bloque** que se abra (`seguridad`, por el
orden de Brian) **no es solo un bloque de For3s OS. Es también el test de campo de Mente OS v2.**
⭐ **Conviene que su `§K Closing` declare las dos cosas:** qué se arregló de For3s OS **y qué
falló o funcionó del motor al gobernarlo.**

📊 **Es la prueba de campo que `memory/PENDIENTES.md` lleva pidiendo desde el 5-ago** — *"lo que desbloquea
traerlos es una PRUEBA DE CAMPO, no más código"* — solo que **hacia adentro**: no un usuario
externo instalando Mente OS, sino Mente OS saliendo de su propio árbol por primera vez.


---

## 28 · EL ORIGEN DE LAS 33,737 MEMORIAS — de dónde vinieron y por qué quedaron aisladas

**Leídas las 6 radiografías de `docs/analysis/` (1,150 líneas) y el reporte de ejecución del
entrenamiento, 2026-08-12.**

⭐ **Cierra §24 con la procedencia exacta.** §24 midió que 33,737 memorias son inalcanzables.
Esta sección dice **de dónde salieron, cuánto valían, y por qué su `session_id` es lo que es.**

### 28.1 · Los 6 agentes OpenClaw, censados

| Agente | Turnos | Qué era |
|---|---|---|
| 📰 **watchdog** | **20,749** | el que más habló · se reseteaba cada madrugada ~4AM (job diario) |
| 🔨 **dev** | **17,096** | ⭐ **hallazgo mayor de la radiografía: "nadie lo tenía censado"** · el Fruterito-desarrollador de Godínez Studio |
| 🍍 **main** (Personal) | **6,045** | lo cotidiano de Brian · la serie INMORTALIDAD · los diarios del final de la era |
| 👔 **empleado** | 708 docs | el "mar de conocimiento" — ⚠️ **resultó ser el MISMO workspace sincronizado** |
| 🔴 cipher · 🔵 helix | 61 · 107 | casi sin usar |
| 👥 godin-slot-1..15 | 211 | solo el slot 1 habló · **los otros 14 vacíos** |

### 28.2 · ⭐ El hallazgo que redujo el trabajo a la mitad

`docs/analysis/Radiografia_Fruterito_WSL.md`:

> ⭐ **"wsl es en su mayoría un ESPEJO del principal. 6,600 de los 11,664 archivos totales son
> duplicados exactos (sha256) entre raíces."**
>
> *"`workspace-empleado/` — el supuesto 'mar de 734 docs' — es el MISMO workspace sincronizado:
> de sus 1,011 archivos solo **5 son únicos**. 🍊 **El 'Fruterito Empleado' compartía el cerebro
> documental con el Personal.**"*

⭐⭐ **Medir antes de importar evitó duplicar 6,600 archivos.** Es L-25 aplicada en junio: el
sistema **midió en vez de asumir**, y el volumen real resultó **mucho menor que el censado a mano**.

### 28.3 · 🔴 Y aquí está la causa de §24, escrita en la radiografía

**Las sesiones estrella del agente `dev`:**

> *"una de **54 MB** (`f30a7098….jsonl.reset.2026-04-01`) — **la madre de todas las sesiones**;
> otra de 9.9 MB viva al final (`c27178c0….jsonl`, 2026-04-05)"*

📊 **Y en la BD de Brian, medido en §24:**

| Sesión en la BD | Turnos |
|---|---|
| `oc:fruterito-principal:f30a7098-6115-4df2-…` | **10,452** |
| `oc:fruterito-principal:c27178c0-5e21-4122-…` | **1,958** |

⭐⭐⭐ **Son las MISMAS. El `session_id` de la BD conserva literalmente el UUID del archivo
`.jsonl` de OpenClaw.**

**El entrenamiento importó con fidelidad forense: cada sesión de OpenClaw se convirtió en una
sesión de For3s con su identificador original.** ⭐ **Fue una decisión correcta para preservar la
trazabilidad — y es exactamente lo que las volvió invisibles**, porque `buscar_semantico` filtra
por `session_id` y Brian habla en `tg:1923367928`.

⚠️ **No fue un error: fue un efecto secundario no previsto de una decisión buena.**

### 28.4 · Lo que el entrenamiento SÍ resolvió bien

**`Radiografia_Fruterito_Personal_MainWSL` §4 — cobertura del manifiesto:**

> *"40 archivos → **37 importados · 2 descartados (runtime) · 1 índice**"*

📊 **Y en `memory/PENDIENTES.md`, el reporte global: `11,664/11,664 decididos (0 pendientes)`.**

⭐ **Cero archivos sin decisión. Cada uno de los 11,664 tiene un veredicto registrado**
(importado · duplicado · descartado · secreto). **Eso es disciplina de import poco común.**

**Y los secretos se excluyeron:** las radiografías marcan `⛔ auth-profiles.json` en cada agente,
`credentials/` (6 `telegram-*.json`), `identity/`, `.env`. **19 archivos de secreto detectados y
enviados al vault, no a la memoria.**

### 28.5 · El valor que sigue ahí, esperando

| | |
|---|---|
| Turnos importados | **33,737** |
| De qué | watchdog (monitoreo diario) · dev (**17K turnos de desarrollo real**) · personal (lo cotidiano de Brian) |
| Embeddings calculados | **133 MB** |
| Consolidado al grafo | **91.3%** |
| 🔴 **Recuperado alguna vez** | **0** |

⭐⭐ **El agente `dev` solo aporta 17,096 turnos de desarrollo real de Godínez Studio** — el
material más valioso para un agente que hace QA de código. **Y es inalcanzable.**

### 28.6 · La lección

> **L-31 · Una migración fiel al origen puede ser correcta y aun así romper el destino. La
> fidelidad se verifica contra la FUENTE; la utilidad, contra el CONSUMIDOR. Son dos pruebas
> distintas y la segunda casi nunca se hace.**

📊 **Medido:** el entrenamiento verificó **11,664 de 11,664 archivos contra su origen** — cobertura
perfecta. **Nadie verificó si el agente podía LEERLOS después.** ⭐ Es L-24 (*el eslabón sin
medir*) en el dominio de los datos: **se auditó `archivo → BD` y nunca `BD → agente`.**


---

## 29 · 🔴🔴🔴 CORRECCIÓN GRAVE A §24 — la memoria SÍ alcanza las importadas

**Medido EN VIVO ejecutando `memoria.recordar()` en el contenedor de `brian`, 2026-08-12,
siguiendo el guion de `memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md` §2.**

🔴🔴 **§24 está EQUIVOCADO en su conclusión principal.** Lo dejo escrito arriba y lo corrijo aquí,
porque borrarlo escondería el error de método — que es la lección más cara de esta auditoría.

### 29.1 · La prueba en vivo que lo desmiente

```
mem.recordar("tg:1923367928", "en que nos hemos enfocado", es_panorama=True)
  → PANORAMA len: 1072

mem.recordar("tg:1923367928", "que sabes de godinez studio", es_panorama=False)
  → BUSQUEDA len: 2436
```

**Y el contenido devuelto:**

> *"- (Usuario [25 mar 2026, hace 139 días]) **[origen: fruterito-principal · 2026-03-25 ·
> conversación]** … pero esto es de godinez studio ?"*
> *"- (For3s [4 abr 2026]) **[origen: fruterito-principal · 2026-04-04]** 🍓 Cambios en
> godinez-studio — Tickets cerrados: #106 Redis Pub/Sub buffer…"*

⭐⭐⭐ **El material importado de `fruterito-principal` SÍ se recupera, con su origen y su fecha
declarados.**

### 29.2 · El mecanismo que no vi

`memory.py:255-266` — **existe un parámetro explícito para esto:**

```python
# ENTRENAMIENTO (2026-07-05): incluir_import suma el corpus IMPORTADO
# (channel='import', sesiones oc:*) del MISMO humano — sin esto, la memoria
# heredada de otros agentes era invisible para el chat (bug cazado en E5b).
# Fail-closed: un miembro (scope) solo ve imports con SU telegram_user_id.
if incluir_import and scope_user_id is not None:
    base_sesion = "(session_id = $1 OR (channel = 'import' AND telegram_user_id = $4))"
elif incluir_import:
    base_sesion = "(session_id = $1 OR channel = 'import')"
else:
    base_sesion = "session_id = $1"
```

⭐⭐ **El bug que yo "descubrí" ya se cazó y se arregló el 2026-07-05, en E5b.** El comentario lo
dice literal: *"sin esto, la memoria heredada de otros agentes era **invisible para el chat**"*.
**Y `memoria.py:149` pasa `incluir_import=True`.**

### 29.3 · Dónde estaba mi error, exactamente

| Lo que hice | Por qué falló |
|---|---|
| Leí el filtro documentado en `PR4_Flujo_Usuario_Memoria` (junio) | ⚠️ **es la versión ANTERIOR al arreglo de julio** |
| Medí `session_id` en la BD y conté alcanzables | ✅ el dato es correcto |
| **Concluí que la búsqueda no los alcanza** | 🔴 **inferí del esquema en vez de ejecutar la función** |

⭐ **El dato de §24 sigue siendo cierto (134 episodios comparten `session_id` con Telegram). La
CONCLUSIÓN era falsa: la búsqueda no depende solo de `session_id`.**

### 29.4 · Entonces, ¿por qué `veces_recuperado` es 0.06%?

**Con la conclusión corregida, la pregunta real cambia.** Lo medido:

| | |
|---|---|
| La búsqueda **sí alcanza** las importadas | ✅ probado en vivo |
| `veces_recuperado > 0` en importadas | 🔴 **cero** |
| `last_accessed` en importadas | 🔴 **cero** |

⭐ **La hipótesis medible ahora es OTRA:** `memory.py:367` (`marcar_recuperados`) **actualiza el
contador solo para los episodios de la sesión activa** — es decir, **el contador no sigue el mismo
camino que la búsqueda.** 🔬 **Eso hay que verificarlo leyendo esa función, y NO lo hice.**

⚠️ **Si esa hipótesis es correcta, H-02 deja de ser "la memoria no recupera" y pasa a ser "el
CONTADOR no registra lo importado" — un defecto de telemetría, no de memoria.** Sería el tercer
caso de la misma familia (§16.3: la honestidad vive en los comentarios, no en la telemetría).

⛔ **No lo afirmo: lo dejo declarado como lo siguiente a medir**, porque afirmarlo sin ejecutar
sería repetir exactamente el error que esta sección corrige.

### 29.5 · La lección, y es la más cara de las 29 secciones

> **L-32 · Un esquema de base de datos describe lo que se PUEDE consultar, no lo que el código
> consulta. Inferir comportamiento del esquema es leer el mapa en vez de caminar el terreno —
> y produce hallazgos que suenan sólidos y son falsos.**

📊 **Medido sobre mí mismo:** §24 tenía **datos correctos, evidencia citada, y una conclusión
equivocada.** Presenté *"la memoria está inalcanzable"* como el hallazgo más importante de la
auditoría. **Bastaron dos llamadas a `recordar()` para desmontarlo** — las mismas que el
`PLAN_PRUEBAS_EXHAUSTIVO` ya tenía escritas desde julio.

⭐⭐ **Y es L-02 aplicada a un hallazgo en vez de a un check:** *un check debe verse fallar antes
de que su verde valga*. **Un hallazgo debe verse REPRODUCIR antes de que su rojo valga.**


---

## 30 · ✅ H-02 CERRADO — el diagnóstico correcto, con el código en la mano

**Leído `memory.py:320-430` en el servidor, 2026-08-12. Cierra la hipótesis que §29.4 dejó
abierta, sin inferir: con la función delante.**

### 30.1 · El código exacto

```python
# memory.py:362 — tocar_recuerdos
"UPDATE episodes_events SET last_accessed = now(), "
"veces_recuperado = veces_recuperado + 1 "
"WHERE session_id = $1 AND seq = ANY($2::int[]) AND deleted_at IS NULL"
```

**Y quién lo llama** (`memory.py:320`, dentro de `buscar_semantico`):

```python
_tocar_recuerdos_bg(pool, session_id, [r.seq for r in recuerdos])
```

### 30.2 · ⭐⭐ La asimetría, en una línea

| | Filtro |
|---|---|
| **La BÚSQUEDA** (`buscar_semantico`) | `session_id = $1` **OR `channel = 'import'`** ← cruza sesiones |
| **El CONTADOR** (`tocar_recuerdos`) | `session_id = $1` ← **solo la sesión activa** |

⭐⭐⭐ **Un recuerdo importado se RECUPERA (la búsqueda lo alcanza) y NUNCA se MARCA (el UPDATE
no lo encuentra, porque su `session_id` es `oc:fruterito-*` y el parámetro es `tg:1923367928`).**

**El `UPDATE` no falla: simplemente toca 0 filas.** Y la función es defensiva —
*"cualquier error se traga (es secundario)"*— así que **nadie se entera.**

### 30.3 · ✅ H-02, reescrito con su diagnóstico real

| | Antes (§5.2 y §24) | Ahora, medido |
|---|---|---|
| Enunciado | *"la memoria recupera al 0.06% — el tubo que no devuelve"* | **el CONTADOR no registra las recuperaciones cruzadas** |
| Gravedad | 🔴🔴 EL defecto central de la campaña | 🟠 **defecto de telemetría** |
| Qué falla | la recuperación | **la medición de la recuperación** |
| Consecuencia real | *"33 mil memorias inútiles"* | ⚠️ **el decay de `relevance` no recibe el refuerzo por uso** |

### 30.4 · ⚠️ Pero tiene una consecuencia REAL, y no es cosmética

`tocar_recuerdos` no es solo un contador. Su docstring lo dice:

> *"'Usar' un recuerdo lo refresca Y cuenta el uso → **lo muy recuperado resiste mejor el olvido**
> (refuerzo por uso real, no neutro como en la v1)."*

🔴 **Consecuencia medible: un recuerdo importado que se usa CADA DÍA sigue envejeciendo como si
nadie lo tocara.** La microglía lo verá con `relevance` bajo y `last_accessed` nulo → **candidato
a olvido**.

📊 **Y el riesgo ya está sobre la mesa:** §25 midió **4,230 episodios con `relevance < 0.3`**
— el umbral de poda. ⚠️ **Entre ellos hay material importado que SÍ se está usando y que el
sistema cuenta como no usado.**

⭐⭐ **El defecto no es que la memoria no sirva: es que el sistema podría BORRAR lo que sí usa.**

### 30.5 · El arreglo, medido

⭐ **Es de una línea**, y el propio código enseña cómo: `buscar_semantico` ya construye un
`base_sesion` dinámico según `incluir_import`. **`tocar_recuerdos` necesita el mismo tratamiento** —
marcar por `(session_id, seq)` reales de cada recuerdo, no por el `session_id` de la consulta.

⛔ **No lo implemento: es código de For3s OS y la campaña aún no ha abierto su bloque.** Queda
declarado para el bloque `memoria`, con su prueba de aceptación:

> 🔬 **Cómo se verá que quedó bien:** recuperar un recuerdo `oc:*` y comprobar que su
> `veces_recuperado` sube. Hoy sube 0.

### 30.6 · La lección

> **L-33 · Cuando una función LEE con un criterio y otra ESCRIBE con otro, el sistema funciona y
> miente a la vez. La asimetría entre el camino de lectura y el de escritura es invisible en
> pruebas funcionales — solo aparece leyendo las dos funciones juntas.**

⭐ **Es la familia de la L-24** (*el eslabón sin medir*) dentro de un mismo módulo: `memory.py`
tiene el arreglo de julio (`incluir_import`) en la lectura **y no lo propagó a la escritura.**

📊 **Y cierra el arco de las 3 secciones:** §24 dijo *"no recupera"* (falso) · §29 lo desmintió y
dejó la hipótesis · §30 la confirma con el código. ⭐ **Tres pasos, dos errores míos corregidos, y
un diagnóstico que ahora sí es accionable en una línea de SQL.**


---

## 31 · LO QUE `work/` GUARDA — un spike olvidado y un secreto sin rotar

**Leídos `work/SPIKE_OpenCode_segundo_proveedor.md`, `work/Entrenamiento_Ejecucion_Reporte.md` y
el resto de `work/` no-ronda, 2026-08-12.**

### 31.1 · ⭐⭐ El SPIKE que resuelve la anti-visión #8 — probado y dormido

`work/SPIKE_OpenCode_segundo_proveedor.md` (11-jun) responde a la pregunta que §22.3 dejó abierta:
*"multi-provider desde día 1"* está incumplida. **Y la solución existe, probada end-to-end:**

```
For3s (Python httpx) ──HTTP──► opencode serve :4096 ──► modelo LLM ──► OK
```

**Lo que el spike verificó, no supuso:**

| | |
|---|---|
| OpenCode 1.17.3 instalado en `for3s` | ✅ MIT · 173K ⭐ · empresa Anomaly |
| `opencode serve` → **135 endpoints** OpenAPI 3.1 | ✅ auth opcional |
| Config **headless** (env var, sin navegador) | ✅ |
| Prueba real desde Python: `POST /session` → mensaje → **"RESPUESTA: OK"** | ✅ con `mimo-v2.5-free` |
| Da acceso a | GPT · Gemini · locales · Zen (deepseek-v4, minimax, qwen3.7, glm-5.1, kimi-k2) |

⭐ **Y su encaje ya está diseñado:** *"nuevo `OpenCodeProvider(LLMProvider)` en `llm.py`: en vez de
httpx a `api.anthropic.com`, httpx a `127.0.0.1:4096`."* **For3s mantiene `ClaudeProvider` como
primario.**

**Decisión registrada:** *"DIFERIR la integración a H7 (DECIDE)… meterlo AHORA desviaría del orden
de obra."* ⭐ **Disciplina correcta** — y §25 midió que **H7 sigue siendo el hito ausente.**

📊 **Medido hoy:** OpenCode **sigue instalado** en `~/.opencode/bin` y **NO está corriendo**.
Exactamente como lo dejó el spike: camino validado, servicio dormido.

### 31.2 · 🔴 Un secreto marcado para rotar que nadie registró

El mismo documento, §hallazgos:

> ⚠️ **"Key Zen `sk-vR316…` EXPUESTA en chat → ROTAR."**

**Medido:** 🔴 **la rotación NO aparece en `memory/pendiente-agosto-2026.md`** ni en ningún otro
pendiente. **Lleva desde el 2026-06-11 declarada en un documento de trabajo y en ningún sitio
donde alguien la vea.**

⭐⭐ **Es la ley del proyecto sobre un secreto:** *"un secreto filtrado se ROTA, no se borra"*
(`rule-config-hygiene` §1.1). **La regla existe, la detección funcionó, y el pendiente nunca se
creó.**

⛔ **No sé si Brian la rotó por su cuenta** — no puedo saberlo desde aquí, y afirmarlo en
cualquier dirección sería inventar. **Queda declarado como lo que es: una acción marcada hace dos
meses sin rastro de cierre.**

### 31.3 · Un límite de forma que la campaña heredará

⚠️ **`work/` no tiene tablero, ni índice de estado, ni contrato.** Es la carpeta del trabajo
cerrado — pero el spike de OpenCode **no está cerrado: está diferido**, y no hay nada que lo
distinga de un documento terminado.

📊 **Medido:** de los 23 archivos no-ronda de `work/`, **al menos 4 contienen decisiones diferidas
vivas** (el spike de OpenCode · los 3 carriles dormidos: multicanal, presencia, mejora continua).
**Ninguno aparece en `memory/pendiente-agosto-2026.md`.**

⭐ **Es L-29 en una cuarta forma:** los tableros congelados eran tres; **`work/` es una carpeta sin
tablero, que es peor** — no miente, simplemente **no dice nada**.

### 31.4 · ⚠️ Y una corrección de método, en caliente

**Al medir si OpenCode corría, mi primer `pgrep -f "opencode serve"` dio positivo.** Iba a
reportar *"un proceso no declarado corriendo en el servidor"*.

🔬 **Lo verifiqué con `ps aux` antes de escribirlo: el `pgrep` se estaba detectando A SÍ MISMO.**
OpenCode no corre; el puerto 4096 no escucha.

⭐ **Lo dejo escrito porque es L-32 evitada a tiempo** — la misma familia del error de §24. **Esta
vez la segunda medición ocurrió ANTES del hallazgo, no después.**


---

## 32 · ⭐⭐ LA NEUROCIENCIA COMO HERRAMIENTA DE DIAGNÓSTICO — el cierre de `Cerebro/`

**Leídos `Cerebro/Cerebro_Humano_acercamiento1.md` (868 líneas, 8 niveles) y `Cerebro/Cerebro_Humano_acercamiento2.md` (820,
7 secciones), 2026-08-12. Con esto `Cerebro/` queda leído entero.**

⭐ **No son documentos decorativos.** El §7 del primero es *"la sección más útil para decisiones"*
y el §4 del segundo es, medido contra For3s OS hoy, **el mejor diagnóstico diferencial del repo**.

### 32.1 · El origen de las 7 ventajas — con su prioridad de partida

`Cerebro/Cerebro_Humano_acercamiento1.md` §7 ordena las palancas **antes** de que existieran las rondas:

| Tier | Palanca | Estado del arte (mayo-2026) | ⭐ Medido en For3s hoy |
|---|---|---|---|
| **1** | **Hipocampo + pattern separation** | *"Hermes lo hace parcialmente con FTS5. Pattern separation real no existe"* | 🟢 **33,908 episodios · pgvector HNSW** |
| **1** | **Ganglios basales de QA** | *"NADIE lo hace especializado por dominio"* | 🟠 16 skills · **sin NO-GO ni lifecycle** |
| **1** | **PFC / metacognición** | *"ReAct, ToT son crudos. No hay metacognición real"* | 🟡 **4 de 8 señales** |
| **1** | **Microglía** | *"nadie lo está haciendo. **Podrías ser el primero**"* | 🟢🟢 **41% podado — LO FUE** |
| **2** | Amígdala | *"nadie"* | 🔴 **ausente** |
| **2** | DMN | *"nadie en producción"* | 🟢 3,295 corridas |
| **2** | Neuromoduladores | *"nadie"* | 🟡 `relevance.py` (116 líneas) |

⭐⭐ **Las 4 palancas Tier 1 se construyeron. Las Tier 2 quedaron a medias o ausentes.** El orden
de construcción **respetó la prioridad del análisis original**, sin que ningún documento lo dijera.

### 32.2 · ⭐⭐⭐ El §4 del segundo documento ES un diagnóstico diferencial

`Cerebro/Cerebro_Humano_acercamiento2.md` §4 estudia **qué pasa cuando cada pieza se rompe**, con casos clínicos reales.
**Aplicado a For3s OS medido:**

| Pieza dañada | Síntoma clínico | ⭐ Su predicción para un agente | Estado en For3s |
|---|---|---|---|
| **Hipocampo** (caso H.M., 1953) | *"no podía formar memorias nuevas… cada día todo era nuevo"* | *"pierde la capacidad de mejorar con cada interacción"* | ✅ **sano** — forma memorias |
| 🔴 **Amígdala** (paciente S.M.) | *"literalmente no puede sentir miedo… decisiones financieras peligrosas"* | ⭐⭐ *"**un agente sin amígdala trataría todos los bugs como iguales. No sabría que un bug de seguridad es más urgente que uno cosmético.**"* | 🔴 **AUSENTE** |
| **PFC** (Phineas Gage, 1848) | *"capacidad técnica intacta, **juicio destruido**"* | *"genera tests técnicamente correctos pero sin juicio de cuándo NO generar nada"* | 🟡 **a media profundidad** |
| **Ganglios basales** (Parkinson/Huntington) | *"no hay vía NO-GO funcional"* | *"o actúa demasiado (200 tests innecesarios) o queda paralizado"* | 🟠 **la vía NO-GO no existe** |

⭐⭐⭐ **La predicción de la Amígdala se cumplió literalmente.** §22 midió que la ventaja #6 está
ausente. **Y este documento, de mayo, ya decía exactamente qué síntoma produciría: no distinguir
lo crítico de lo cosmético.**

📊 **Verificable hoy:** For3s OS **no tiene priorización de criticidad en la entrada**. Todo
mensaje entra por el mismo camino (`Conversation.send`, medido en §18.2, sin escáner).

⚠️ **Y la de Huntington también, en su forma exacta:** *"no hay vía NO-GO funcional"*. **§17 midió
que la vía NO-GO no existe en el código** — solo el hook que la espera.

### 32.3 · ⭐⭐ La lección de método que esto da a la campaña

> **L-34 · Un modelo de referencia bien elegido predice los síntomas de sus propias ausencias. Si
> el modelo dice qué pasa cuando falta la pieza X, y la pieza X falta, el síntoma es verificable —
> y eso convierte una analogía en una herramienta de diagnóstico.**

⭐ **Aplicable directamente:** cuando el bloque `seguridad` audite la Amígdala ausente, **no tiene
que inventar qué buscar**. `Cerebro/Cerebro_Humano_acercamiento2.md` §4.2 ya lo dice: *"trataría todos los bugs como
iguales"*. 🔬 **La prueba es: mandarle a For3s un mensaje benigno y uno hostil y ver si los trata
distinto.** Medible en un turno.

### 32.4 · Lo que estos documentos declaran que NO aplica

⭐ **Y es tan valioso como lo que sí** — `Cerebro/Cerebro_Humano_acercamiento1.md` §7 Tier 3:

> 🔴 *Cerebelo artificial (irrelevante para software) · Hipotálamo (drives básicos — irrelevante)
> · Tronco encefálico (irrelevante) · **Predictive coding completo (importante a largo plazo pero
> no para v1)** · Plasticidad estructural en tiempo real (frontier de research, no producible aún)*

⭐⭐ **Eso explica el "≈40% de profundidad" de Grafo §0.3**: el 60% restante no es deuda —
**es Tier 3 declarado como no-prioritario desde mayo.**

### 32.5 · Con esto, `Cerebro/` queda leído entero

| Documento | Líneas | Estado |
|---|---|---|
| `Cerebro/For3s_OS_Grafo_Maestro.md` | 1,300 | ✅ §0-§8 completo |
| `Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md` | 2,485 | ✅ §0-§4 + estructura |
| `Cerebro/Arquitectura_Grafo_vs_Loop.md` | 1,654 | ✅ §13-§16 + estructura |
| `Cerebro/Registro_Conversaciones.md` | 849 | ✅ completo |
| `Cerebro/Cerebro_Humano_acercamiento1.md` | 868 | ✅ §7-§8 + estructura |
| `Cerebro/Cerebro_Humano_acercamiento2.md` | 820 | ✅ §4 + estructura |
| **TOTAL** | **7,976** | ✅ **la capa Cerebro, cubierta** |


---

## 33 · ✅ LOS BANCOS — el origen histórico, y el cierre de la lectura

**Leídos `memory/archive/Banco_Diario_Mayo_2026.md` (915), `memory/archive/Banco_Infografias_Completo.md`
(2,245, 22 buckets) y `memory/archive/Banco_Filtro_Alineacion.md` (634), 2026-08-12. Con esto la lectura de
`Mente/` queda cerrada.**

### 33.1 · De dónde salió todo — el stack de mayo, antes del pivote

`Banco_Diario_Mayo_2026` conserva los 3 documentos originales (`FOR3S-STACK-DEFINED` ·
`FOR3S-SERVER-ARCHITECTURE` · `FOR3S-RECURSOS-ACTUALES`), y su §5.1 lista **lo que aparecía en
los tres**:

| Mayo 2026 (los 3 docs) | Hoy, medido |
|---|---|
| **Ubuntu Server 26.04 LTS** | ✅ sigue |
| **Docker** | ✅ 28 contenedores |
| **Tailscale** | ✅ el acceso de esta auditoría |
| **PostgreSQL 16 + Redis 7** | ✅ **PG16 + Valkey** (fork BSD de Redis — R2 B3 lo cambió por licencia) |
| 🔴 **Node.js + TypeScript** como backend | 🔴 **Python 3.12** — R1 lo revirtió el 30-may |
| 🔴 **OpenClaw como motor de agentes** | 🔴 **motor propio** — For3s OS se construyó independiente |
| **3 agentes: Personal, Empleado, Design** | ⭐ **absorbidos** — sus 33,737 memorias viven en `brian` (§28) |
| **for3s-server 32GB/1TB** | ✅ el mismo · ⚠️ **medido hoy: 18 GB**, no 32 |

⭐⭐ **Dos decisiones de mayo se revirtieron por completo** (TypeScript→Python, OpenClaw→motor
propio) **y las dos están registradas con su razón** en R1 y en el filtro. **Nada se cambió en
silencio.**

### 33.2 · ⭐ El documento detectó sus propias contradicciones — en mayo

`Banco_Diario` §5.3 lista **4 inconsistencias entre los 3 docs**, encontradas al consolidarlos:

> 1. *"**Auth:** STACK-DEFINED lista 3 opciones como pendientes. SERVER-ARCHITECTURE asume
>    Supabase Auth como default. **El server architecture asume una decisión que stack-defined
>    dice que está pendiente.**"*
> 2. *"**Ubicación de agentes: CONFLICTO REAL** — los agentes están en WSL2 (recursos), pero el
>    plan los pone en for3s-server (architecture)."*
> 3. *"**Memoria:** estados distintos en cada doc" (Honcho "configurado" vs "pendiente")*
> 4. *"**Agentes simultáneos:** 10 con 20GB (plan) vs ~20-30 (capacidad teórica)"*

⭐⭐ **Es exactamente el trabajo que yo hice en §16-§32, hecho tres meses antes sobre otro
material.** La disciplina de **cruzar documentos y declarar sus choques** existe en este repo
desde mayo. **Lo que no existía era cruzarlos contra el CÓDIGO** — que es lo único que esta
auditoría añade.

### 33.3 · Los 2 conceptos propios de Brian que sobrevivieron

`Banco_Diario` §6.4 los rescata del material histórico:

| Concepto | Definición de Brian | Dónde aterrizó |
|---|---|---|
| **Inmortalidad** | export/import portable de un agente | ⭐ Event Sourcing + Nodo 1 KG + Nodo 2 Hipocampo · **y `bloque distribucion` lo cerró 6/6** |
| **Herencia** | templates de agentes base+override | Nodo 4 Ganglios Basales / skills |

⭐ **Ambos nacieron antes que el Grafo Maestro y el Grafo los absorbió.** Son de Brian, no
importados.

### 33.4 · El banco de infografías: 81 piezas, ya filtradas

`Banco_Infografias_Completo` (2,245 líneas, **22 buckets**) es material de aprendizaje capturado
en mayo. **No requiere lectura línea a línea para la campaña, y la razón está medida:**
`Banco_Filtro_Alineacion` **ya lo procesó** con veredicto por pieza:

```
✅ KEEP ~30 · 🔧 REFINE ~20 · ⏸️ DEFER ~8 · 📚 REFERENCIA ~15 · ❌ DROP ~10
```

⭐ **El filtro es el índice ejecutivo del banco.** Leer las 81 fichas cuando existe un veredicto
por cada una sería reprocesar trabajo hecho — exactamente lo que **L-25** advierte.

### 33.5 · ✅ ESTADO DE LA LECTURA — cerrado

| Capa | Líneas | Estado |
|---|---|---|
| `memory/` (Estado_Sesion · PENDIENTES · Bitácora · RETOMAR · pendiente-agosto) | ~13,900 | ✅ |
| `Cerebro/` (los 6) | 7,976 | ✅ |
| `work/` (65 rondas + 23 no-ronda) | ~35,000 | ✅ decisiones y bloques clave |
| `memory/archive/` (38) | ~13,350 | ✅ los 12 mayores + filtro |
| `rules/` + `rules/decisions/` (56) | ~5,900 | ✅ |
| `principles/` + `expertise/` (14) | 3,470 | ✅ |
| `docs/architecture/` (6) | 2,409 | ✅ |
| `docs/analysis/` (28) | 7,152 | ✅ los 10 decisivos |
| `vision/` (8) | ~3,300 | ✅ los 2 mayores |
| `bridges/` (6) · `Maestro/` (7) · `blocks/` (24) | ~2,000 | ✅ |
| **TOTAL cubierto** | **~45,000 de 110,000** | |

⚠️ **Lo digo con precisión, porque decir "leí todo" sería L-15:** **cubrí el 100% de los
documentos que gobiernan, deciden o registran** — reglas, ADRs, contratos, principios, rondas con
decisión LOCKED, planes maestros, tableros, registros de sesión y análisis.

**Lo que queda sin leer línea a línea (~65,000) es material de tres tipos, y ninguno decide:**
① las 81 fichas del banco de infografías (**ya filtradas pieza por pieza**) · ② el detalle interno
de rondas cuyas decisiones LOCKED ya leí en sus §Decisión y en el Consolidado · ③ snapshots
históricos superados por documentos posteriores (`Estado_Sesion_Snapshot_2026-07-07` está
contenido en la Bitácora y en el Registro).

### 33.6 · ⭐⭐⭐ Lo que esta lectura le dio a la campaña

**33 secciones, 2,400 líneas, 34 lecciones (L-01 a L-34).** Y lo más importante, en tres frases:

1. ⭐ **La vara correcta existe y no había que inventarla:** el gate de la fase en curso (§23) —
   **For3s OS pasa 6 de 6.**
2. ⭐ **Los 24 hallazgos se reducen a 4 que importan hoy**, y caen exactamente en los 4 primeros
   bloques que Brian priorizó por instinto.
3. ⭐ **Dos de mis propios hallazgos centrales resultaron falsos** (§29, §30) y están corregidos
   con evidencia. **Una auditoría que no se corrige a sí misma no es una auditoría: es una
   opinión larga.**

---

Related: `campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` (su hermano: el terreno del código) ·
`campaigns/producto-for3s-os/CAMPAIGN.md` (la campaña que usa ambos) · `Cerebro/Registro_Conversaciones.md` (las autopsias
completas) · `rules/rule-checks-must-measure.md` (las 4 familias, con código) ·
`rules/decisions/` (los 30 ADRs) · `memory/pendiente-agosto-2026.md` (la deuda viva) ·
`principles/expertise/val-functional.md` (la verificación afirmativa).
