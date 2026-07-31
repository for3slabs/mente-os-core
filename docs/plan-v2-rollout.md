# 🗺️ PLAN DE IMPLEMENTACIÓN — Mente OS v2
**Status:** current · **Type:** plan · **Updated:** 2026-07-31 · **Owner:** brian
> **Petición de Brian (2026-07-27):** *"necesitamos un plan de implementación con fases y tickets de
> desarrollo, de forma detallada, de tal manera que **sepa por qué se hizo esto primero antes que
> otro punto**."*
>
> **Estatus 2026-07-31:** ✅ **F0-F7 CERRADAS Y VERIFICADAS · F8 al 75%** — `bin/test-f0-f6` =
> **105/105**. 11 validadores · 4 hooks · 3 niveles de reglas. Commit `42dbfab` (279 archivos).
> Migración v1→v2 completa (M0-M5, ADR-029): `Alma/` `Cuerpo/` `Doc/` `Tickets/` **eliminadas**.
> **Falta F8-4:** retomar tras un `/clear` real — la prueba final del sistema.
> **Diseño:** `Arquitectura_Mente_OS_v2_Bloques.md` · **Visión:** `principles/vision-mente-os-v2.md`
---

## 0 · LAS 4 LEYES DEL ORDEN (por qué va en este orden y no en otro)

Cada fase se justifica con una de estas leyes. **Si un ticket no cumple ninguna, no entra todavía.**

| Ley | Enunciado | De dónde sale |
|---|---|---|
| **L1 · Primero lo que no puedo escribir yo** | el criterio de Brian bloquea todo lo demás; sin él, los validadores comprueban formularios vacíos | §9.1 *"la IA no inventa criterio"* |
| **L2 · Primero lo que se puede probar en algo real** | construir maquinaria sin un caso real es diseñar a ciegas — el error que nos trajo aquí | Decisión 8: la DEMO es el piloto |
| **L3 · La verificación antes que la automatización** | un validador que comprueba es barato y da valor ya; un hook que bloquea sin criterio claro estorba | §12-TER *"la doctrina es documento, la verificación es script"* |
| **L4 · Nada rompe lo que funciona** | 9 piezas del v1 tienen 100% de cumplimiento medido. Se añade al lado, nunca encima | §15 + §12.1 |

> **La ley que gobierna sobre todas:** *explicar → aprobar → construir*. Cada fase se cierra con
> aprobación de Brian antes de la siguiente.

---

## 1 · MAPA DE FASES

```
F0  RONDA DE DISEÑO         ← cerrar lo que falta · sin código
     │
F1  EL CRITERIO             ← ⭐ Brian escribe · L1
     │                         sin esto, todo lo demás mide el vacío
F2  EL CONTRATO             ← las plantillas · L1
     │
F3  EL PILOTO (DEMO)        ← ⭐ probar el diseño en lo real · L2
     │                         AQUÍ se descubre si el diseño sirve
F4  MEDIR                   ← calificar-bloque · L3
     │                         primer valor tangible: ¿producto o MVP?
F5  VERIFICAR               ← los otros 3 validadores · L3
     │
F6  GARANTIZAR LA LECTURA   ← enrutador + hooks · L3
     │                         lo último: bloquear sin criterio estorba
F7  GENERAR                 ← índice y estados · L4
     │
F8  SEGUNDO PILOTO          ← un bloque nuevo desde cero
```

**La lógica del orden en una frase:**
> **criterio → forma → probarlo en algo real → medirlo → verificarlo → exigirlo → automatizarlo.**

**Y la razón de que F6 (los hooks) vaya casi al final:** un hook que bloquea **sin que el criterio
esté escrito y probado** solo genera fricción sin valor. Bloquear es lo más intrusivo del sistema:
se gana el derecho a hacerlo **después** de demostrar que el criterio funciona.

---

## 2 · LAS FASES EN DETALLE

### F0 · RONDA DE DISEÑO — cerrar lo que falta

**Por qué primero:** quedan 2 preguntas abiertas del sistema de aprendizaje (§10.4) y hace falta
validar el plan completo. **Construir con preguntas abiertas es lo que nos trajo aquí.**

| Ticket | Qué | Quién | Estado |
|---|---|---|---|
| **F0-1** | ¿Cuándo un error **merece** ser caso? | Brian aprobó la recomendación | ✅ **CERRADO** → §10.5 |
| **F0-2** | ¿Cómo se detecta que una regla estorbó **3 veces**? | Brian aprobó la recomendación | ✅ **CERRADO** → §10.6 |
| **F0-3** | Revisar el plan y aprobar el orden | Brian | ⏳ pendiente |
| **F0-4** | ⭐ **THE VOICE** — `principles/owner-0-voice.md` + `.claude/output-styles/for3s.md` 🇺🇸 | IA redacta · Brian valida | ⏳ **listo para arrancar** |

**Lo decidido en F0-1 (§10.5):** prueba de **3 preguntas** (¿pasaría en otro sitio? ¿fue criterio
equivocado? ¿se puede escribir como regla accionable?) + **umbral automático a las 2 repeticiones**
+ **límite de 12 casos activos**.

**Lo decidido en F0-2 (§10.6):** roce con **4 campos** (fecha·regla·bloque·motivo) · dispara a los
**3 bloques DISTINTOS** (no repeticiones) · **no caduca** · **la regla no se cambia sola: se eleva a
Brian**.

**⭐ Por qué F0-4 (la voz) se movió aquí desde F1:** es lo único del plan que **no depende de nada**
— ni del criterio de backend, ni del contrato, ni del piloto. Y es lo que **se nota desde la
siguiente respuesta**. Mezclarlo con los 3 archivos de expertise (trabajo de Brian, más lento) le
quitaba el valor inmediato.

**Cierra cuando:** Brian aprueba el orden del plan y la voz está activa.

---

### F0.5 · EL ESTÁNDAR DE DECISIONES (ADR) ✅ *hecho 2026-07-27*

**Por qué antes de F1:** F1 genera decisiones nuevas (cada criterio fijado es una). Sin el estándar
se suman a las 26 que ya estaban **duplicadas en 2 documentos** (75 vs 37 filas, ya divergidas).

| Ticket | Qué | Estado |
|---|---|---|
| **F0.5-1** | `rules/contract-adr.md` — plantilla de 6 campos + las 3 reglas | ✅ **hecho** |
| **F0.5-2** | Migrar las decisiones a ADR individuales | ✅ **HECHO** — **27 ADR** en `rules/decisions/` + `docs/DECISIONS.md` generado |
| **F0.5-3** | Borrar las tablas duplicadas (Arquitectura §17.1 · Visión §6) | ⬜ **tras F7** — ya apuntan al índice como fuente única |

**Las 3 reglas:** una decisión = un archivo · el índice se **genera** · una decisión no se edita,
**se supersede**. Campos que la diferencian de un changelog: **`evidence`** y **`reverting`**.

---

### F1 · EL CRITERIO ⭐ — *lo único que bloquea todo lo demás*

**Por qué va primero (L1):** el sistema entero se apoya en el criterio de Brian.
- La **capa 2 de QA** (§12-Q.5) sin criterio es un formulario vacío.
- El **Encargado 2** sin estándares no puede vetar nada.
- Los **hooks** inyectarían archivos en blanco.

> **Es el cuello de botella real: es lo único que la IA no puede escribir.**
> Todo lo demás son ~19 archivos que la IA redacta a partir del plano.

| Ticket | Qué | Quién | Salida |
|---|---|---|---|
| **F1-1** | `rules/qa-dimensions.md` 🇺🇸 — las 6 dimensiones + evidencia exigida | ✅ **ESTRUCTURA HECHA** · criterio ⬜ Brian | 1 archivo |
| **F1-2** | `principles/expertise/dev-database.md` 🇺🇸 | ✅ **ESTRUCTURA HECHA** · criterio ⬜ Brian | 1 archivo |

> ✅ **CONSTRUIDO 2026-07-27 (estructura completa, cableada, con huecos marcados):**
> `rules/contract-adr.md` · `rules/qa-dimensions.md` · `principles/expertise/{database,backend,frontend}.md`
> · `docs/PENDING-BRIAN.md` (el índice único de huecos).
> **Todo consultando y conectado**: el bloque los declara en §D → el hook los inyecta → owner-3 los
> aplica → `check-blocks` verifica. **Solo falta el criterio de Brian.**

**⭐ F1 cierra con SOLO base de datos.** `backend.md` y `frontend.md` pasan a **F1-bis**, que corre
**en paralelo** con F2-F3.

**Por qué:** BD es donde Brian ya expresó más criterio (*"vamos a desarrollar una base de datos, no
un MVP pedorro"* · *"si no tenemos control estamos mal"*) y **es lo que más propaga**. Con esa sola
disciplina, F4 ya puede medir la parte que más duele. **Exigir las 3 antes de avanzar es un cuello
de botella innecesario.**

| Ticket | Qué | Cuándo |
|---|---|---|
| **F1-bis-1** | `principles/expertise/dev-backend.md` 🇺🇸 | ✅ estructura hecha · criterio ⬜ Brian |
| **F1-bis-2** | `principles/expertise/dev-frontend.md` 🇺🇸 | ✅ estructura hecha · criterio ⬜ Brian |

**⭐ MÉTODO (importante — no al revés):** la IA **pregunta primero**, Brian responde con **casos
reales**, y la IA estructura. Nunca *"la IA redacta y Brian corrige"*.

> **Por qué:** si la IA redacta primero, sale *"usa buenas prácticas"* — genérico e inútil. Si Brian
> responde *"un default nunca apunta a algo con dueño"*, sale **criterio real**.
> Es el riesgo #1 de esta fase (§5).

**Formato:** una disciplina por sesión · 6-8 preguntas (*"¿qué exiges de un esquema? ¿qué te hace
rechazar un PR? ¿cuál es el error que más ves?"*) → la IA lo convierte en las 6 dimensiones con su
evidencia exigida.

**Cierra cuando:** BD tiene criterio escrito con evidencia exigida (backend/frontend siguen en F1-bis).

---

### F2 · EL CONTRATO — las plantillas

**Por qué aquí:** con el criterio escrito ya se sabe qué debe exigir cada plantilla. Antes de F1
habrían salido genéricas.

| Ticket | Qué | Salida |
|---|---|---|
| **F2-1** | `rules/contract-block.md` 🇺🇸 — secciones A-K, límites, qué valida cada una | ✅ **HECHO** |
| **F2-2** | `rules/contract-document.md` 🇺🇸 — plantilla y metadata | ✅ **HECHO** |
| **F2-3** | `rules/rule-{lanes,fix-not-patch,friction,isolation}.md` 🇺🇸 | ✅ **HECHO** (4) |
| **F2-4** | `principles/owner-{1-docs,2-dev,3-validation}.md` 🇺🇸 | ✅ **HECHO** (3) |
| **F2-5** | `Mente/base-rules.md` 🇺🇸 — reglas mínimas **portátiles a cualquier IA** | ✅ **HECHO** |

### 🔍 AUDITORÍA F0-F2 (2026-07-29) — 3 graves cazados y cerrados

Los 3 graves (batería §5-BIS ausente · regla `/clear` no portada · ciclo de vida del bloque sin
definir) **cerrados el 2026-07-29.** 📄 Detalle en `docs/f4-execution-log.md`.

### F3 · EL PILOTO — la DEMO ⭐

**Por qué aquí y no al final (L2):** es donde se descubre si el diseño **sirve de verdad**.
Construir los validadores antes de tener un bloque real sería validar contra una hipótesis.

> **Decisión 8:** la demo es el piloto deliberado — es el bloque activo y el que más duele.

| Ticket | Qué | Salida |
|---|---|---|
| **F3-1** | `blocks/active/demo/BLOCK.md` 🇺🇸 — secciones A-D (el mínimo duro) con datos reales | mínimo duro |
| **F3-2** | Mapear el grafo real de sub-bloques y **sus dependientes** (`userStore.ts` → 5) | §F del bloque |
| **F3-3** | Recuperar decisiones históricas con su rationale (default `hoteles`, orden de despliegue…) | §G |
| **F3-4** | Completar E-J y probar la **suficiencia**: ¿A-E basta para reiniciar? | bloque completo |
| **F3-5** | 🔴 **Auditar el diseño contra la realidad**: ¿qué campo sobró? ¿cuál faltó? | ajustes a F2 |

> ⭐ **F3-5 es el ticket más importante de la fase.** Si el diseño falla, se corrige **aquí**,
> cuando cuesta barato — no después de construir la maquinaria encima.

**Cierra cuando:** el bloque DEMO existe, pasa la prueba de suficiencia, y el contrato quedó
ajustado con lo aprendido.

---

### F4 · MEDIR — `calificar-bloque` ⭐

**Por qué aquí (L3):** primer valor tangible. Responde la pregunta que más duele —
***¿la demo es producto o MVP?***— con números reproducibles antes y después del `/clear`.

| Ticket | Qué mide | Ataca |
|---|---|---|
| **F4-1** | `bin/grade-block`: archivos sin consumidor · exports nunca importados | ✅ **HECHO** |
| **F4-2** | bloques de código duplicados (≥8 líneas) | ✅ **HECHO** |
| **F4-3** | archivos sin test | ✅ **HECHO** |
| **F4-4** | dependientes no declarados · ciclos de importación | ✅ **HECHO** |
| **F4-5** | **Correrlo sobre la DEMO** y escribir el veredicto | ✅ **HECHO — 🔴 MVP** |

> ✅ **F4 CERRADO 2026-07-30.** Y con él los 3 validadores que faltaban del diseño:
> `bin/grade-block` · `bin/flag-stale` · `bin/check-sufficiency`.
>
> **El veredicto real de la demo: 🔴 MVP.** Dos rojos: `ConnectClaude.tsx` (145 líneas, 0
> importadores, desde el 16-jun) y **0 archivos de test en todo el sitio**.
> Escrito en `blocks/active/demo/BLOCK.md` §G-BIS, **reproducible con un comando.**
>
> ⭐ **Esto es lo que Brian pedía desde el principio:** la respuesta a *"¿es producto o MVP?"* con
> números que no cambian con el `/clear`.

### F4-6 · ⭐ del carril al SISTEMA (Brian, 2026-07-30)

> *"¿solo está para demo o para todo el sistema? porque lo vamos a ocupar en todo el sistema."*

**El hallazgo:** `grade-block` no tenía hardcodeo, pero todas sus métricas eran de código. Contra la
lista real de pendientes, **3 de 7 bloques habrían dado 🔴 MVP para siempre.** Un validador que nunca
puede pasar a verde se aprende a ignorar, y ahí la doctrina vuelve a ser un documento.

**La solución (ADR-028):** el bloque declara `type: code | docs | infra | data`; el tipo decide la
regla de medir. Lo que no aplica imprime `n/a` **con su razón**, y `n/a` nunca es 🟢.

📄 **Métricas por tipo, las 6 pruebas y el cableado:** `rules/contract-block.md` §A ·
`decisions/ADR-028-block-type-decides-metrics.md` · bitácora en `docs/f4-execution-log.md`.


> **F4-5 es el primer momento en que Brian obtiene lo que pidió:** un veredicto que no depende de
> mi estado de ánimo ni de si acabo de dar `/clear`.

**Cierra cuando:** la demo tiene una calificación medida, con fecha, reproducible por Brian.

---

### F5 · VERIFICAR — los otros 3 validadores

**Por qué después de F4:** F4 da valor solo (*"¿cómo está mi código?"*); estos protegen el proceso.
Sin bloques escritos, no tienen nada que verificar.

| Ticket | Validador | Qué comprueba |
|---|---|---|
| **F5-0** | ⭐ **completar lo derivable** (§12-T.1) + **recibo de aprobación** (§12-T.2) | los validadores no solo avisan |
| **F5-1** | `bin/check-blocks` | campos obligatorios · límites · ID único · **máx 3 niveles** · conexiones válidas |
| **F5-2** | `bin/check-sufficiency` | ¿las secciones A-E bastan para reiniciar? |
| **F5-3** | `bin/flag-stale` | `State` sin actualizar · bloques parados |
| **F5-4** | ⭐⭐ `bin/check-health` + engancharlo a `SessionStart` | **el sistema se audita solo** (§12-T.3) |
| **F5-5** | ⭐ las 4 reglas de higiene (arquitectura §12-SEPTIES) + los checks de secretos/portabilidad/redundancia en `check-health` | **impide que la config vuelva a degradarse** |

> ⭐ **F5-4 nace de un hallazgo real:** 3 fallos (los `additionalDirectories` con NavigoX, el
> `Maestro/registro.md` que miente, 999 archivos viejos) **vivieron semanas** y los encontró Brian
> preguntando. **Si hay que pedirlo, no está automatizado.**

**Cierra cuando:** los 3 corren sobre la demo sin falsos positivos.

---

### F6 · GARANTIZAR LA LECTURA — enrutador + hooks

**Por qué casi al final:** es la parte **más intrusiva** del sistema. Un hook que bloquea sin que el
criterio (F1) esté escrito y probado (F3-F4) **solo genera fricción sin valor** — y un sistema que
estorba se desactiva. *Se gana el derecho a bloquear después de demostrar que el criterio funciona.*

| Ticket | Qué | Capa |
|---|---|---|
| **F6-1** | Enrutador en `CLAUDE.md` (~15 líneas): qué estándar cargar según el trabajo | **A** |
| **F6-2** | Hook que **inyecta** el estándar declarado en §D antes de editar | **D** (avisar) |
| **F6-3** | 🔴 Hook que **BLOQUEA** las 3 acciones críticas | **D** (bloquear) |
| **F6-4** | Validador de aplicación al cerrar | **C** |

**F6-3 se construye de una en una**, midiendo fricción real:
1. editar pieza con dependientes declarados
2. tocar la base de datos
3. cerrar bloque sin pasar suficiencia

> **Regla de esta fase:** si una puerta estorba más de lo que protege, **se degrada a aviso**.

**Cierra cuando:** las 3 puertas funcionan y no estorban el trabajo normal.

---

### F7 · GENERAR — el índice que no puede mentir

| Ticket | Qué | Salida |
|---|---|---|
| **F7-1** | `bin/generate-index` → `docs/INDEX.md` desde los bloques reales | 🤖 generado |
| **F7-2** | `docs/STATES.md` — todos los bloques con fase, dueño y **salud** | 🤖 generado |
| **F7-3** | Marcar el `README.md` viejo como superseded (§5 y §7 obsoletos) | higiene |

**Cierra cuando:** el índice se regenera solo y refleja la realidad.

---

### F8 · SEGUNDO PILOTO — un bloque nuevo desde cero

**Por qué existe esta fase:** la demo se migró **con su historia**. Un bloque nuevo prueba el flujo
completo desde el minuto cero — que es el uso real del sistema.

| Ticket | Qué |
|---|---|
| **F8-1** | Abrir un bloque nuevo con el mínimo duro (4 campos, 2 minutos) |
| **F8-2** | Trabajarlo entero: los 3 encargados, el carril, los roces |
| **F8-3** | Cerrarlo con el procedimiento de 8 pasos + veredicto de calidad |
| **F8-4** | **Retomarlo tras un `/clear` real** y comprobar la suficiencia |

> ⭐ **F8-4 es la prueba final del sistema entero.** Si tras el `/clear` se puede retomar sin que
> Brian explique nada y sin que la IA infiera nada → **el v2 cumplió su promesa.**

---

## 3 · RESUMEN DE ESFUERZO

| Fase | Tickets | Quién carga el peso | Bloquea a |
|---|---|---|---|
| **F0** diseño | 4 (2 ✅ cerrados) | Brian decide | todo |
| **F1** criterio ⭐ | 2 | **Brian** (IA entrevista) | F2, F4, F6 |
| **F1-bis** backend+frontend | 2 | **Brian** | *(paralelo)* |
| **F2** contrato | 5 | IA | F3 |
| **F3** piloto ⭐ | 5 | IA + Brian valida | F4, F5 |
| **F4** medir ⭐ | 5 | IA | — |
| **F5** verificar | 6 | IA | F6 |
| **F6** lectura | 4 | IA | — |
| **F7** generar | 3 | IA | — |
| **F8** prueba final | 4 | los dos | — |
| **TOTAL** | **42 tickets** | | |

**Dónde está el trabajo de Brian:** **F1 completa** (su criterio) + validar F3 + aprobar cada fase.
**Todo lo demás lo construye la IA** a partir del plano.

---

## 4 · LOS 3 PUNTOS DE VALOR TEMPRANO

No hay que esperar a F8 para que el sistema sirva:

| Tras… | Brian ya tiene |
|---|---|
| **F0-4** | ⭐ **la VOZ activa** — el cambio más inmediato: se nota **desde la siguiente respuesta** |
| **F1** | su criterio de BD escrito — **utilizable aunque no se construya nada más** |
| **F3** | el bloque DEMO con límites, decisiones y grafo → *"ser dueño del contexto"* funcionando |
| **F4** | ⭐ **el veredicto medido de la demo**: ¿producto o MVP? Con números, no con opiniones |

---

## 5 · QUÉ PUEDE SALIR MAL (y qué se hace)

| Riesgo | Señal temprana | Respuesta |
|---|---|---|
| El criterio de F1 sale genérico | *"usa buenas prácticas"* en vez de *"un default nunca apunta a algo con dueño"* | volver a entrevistar con **casos reales** de la demo |
| El bloque DEMO es demasiado grande | no cabe en 150 líneas | partir en 2 bloques (`DEMO-WEB` y `DEMO-BD`) |
| Los validadores dan falsos positivos | ruido que se ignora | calibrar contra la demo antes de F6 |
| Los hooks estorban | Brian los desactiva | degradar a aviso (regla de F6) |
| **Se pierde el impulso a mitad** | fases sin cerrar | **cada fase da valor sola** (§4) — se puede parar en F4 |

---

## 6 · 🔴 BLOQUE APARTE — el renombrado a la convención inglesa

**Estándar ya escrito:** `rules/NAMING_CONVENTION.md` (2026-07-27).
**Aplicación:** todo lo NUEVO nace con la convención desde F0-4. **Lo viejo NO se renombra en masa.**

**Radio de impacto medido:**

| Qué apunta a las carpetas actuales | Cuántos |
|---|---|
| Rutas únicas citadas en documentos | **218** |
| Memorias con rutas (fuera de git) | **~87** |
| Líneas de `CLAUDE.md` con rutas | **13** |
| `Maestro/punteros.tsv` con `memory/RETOMAR.md` | 2 ramas |

**Por qué es un BLOQUE y no un ticket:**
- **Un enlace roto en markdown no da error** → se rompe en silencio y se descubre semanas después.
- **`Maestro/punteros.tsv`** hardcodea `memory/RETOMAR.md` → `maestro leer` deja de encontrar el índice.
- **Foresito lee el Maestro EN VIVO** y fue entrenado con 1,829 episodios que citan las rutas viejas
  → el agente maestro apuntaría a rutas fantasma.
- **Las ~87 memorias están fuera de git** → sin historial para revertir.

> Toca 218 puntos y propaga a 3 sistemas: es **carril de bloque completo** (§5 de la arquitectura),
> y **exige un validador** que pruebe que ningún puntero quedó huérfano.

### ✅ DECIDIDO (Brian, 2026-07-27): es un PENDIENTE, no una fase

> *"No renombramos a los 208, eso será un pendiente de v2."*

**Registrado en `memory/PENDIENTES.md`** · plan completo en `rules/NAMING_CONVENTION.md` §7.4.
Se abrirá **junto con la reestructuración del Mente OS Maestro**.

**Dato que cambia la forma del trabajo: de los 194 `.md`, solo 97 están vivos** (tocados desde
julio). Los otros ~97 son fósiles → **se archivan sin renombrar**, porque hoy la fecha de
modificación es la única señal que separa vivo de fósil, y un renombrado masivo la destruye.

**Mientras tanto:** todo lo NUEVO nace con la convención (desde F0-4); lo viejo se renombra
**al tocarse**. Es la misma migración por demanda de la decisión 8.

---

## 7 · LO QUE ESTE PLAN NO HACE

- **No reorganiza los 188 documentos** — la estructura nueva convive (§12.1).
- **No migra bloques viejos en masa** — por demanda (decisión 8).
- **No toca el v1 que funciona** — §15 lista las 9 piezas intocables.
- **No construye nada sin aprobación** — regla madre, fase por fase.

---

Relacionado: `Arquitectura_Mente_OS_v2_Bloques.md` (el diseño) ·
`principles/vision-mente-os-v2.md` (el porqué) ·
`docs/analysis-internos-v1.md` (referencia externa) ·
`ESTANDAR_Metodo_Fases_F.md` (el método que se absorbe) · [[project_mente_os_v2_bloques]].
