# 🔌 Ronda Maestro — Puentes C (semántica) + D (grafo) sobre UN núcleo común

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_Maestro_Puentes_C_D.md → work/Ronda_Maestro_Puentes_C_D.md (2026-07-30, ADR-029)

## Purpose

🔌 Ronda Maestro — Puentes C (semántica) + D (grafo) sobre UN núcleo común


> **✅✅ ESTADO: CONSTRUIDO Y VERIFICADO E2E (2026-07-19/20).** Brian aprobó el diseño con las
> 6 recomendaciones (§8) y dio "continúa". TODO construido en la misma jornada:
> - **N0-N2 (local):** punteros.tsv (fuente única — mató la triplicación) · maestro_lib.sh
>   (puerta única; el dueño de rama ahora pasa por columna del tsv, mejora sobre v1) ·
>   indexador.py (una pasada → chunks id `rama:ruta#NNN` + enlaces/refs; cinturón anti-secretos
>   excluyó 5 chunks sospechosos; columna `indexar` fija el alcance de la decisión 3).
> - **N3 (server, commit `0cac57a` firmado, SIN push):** migración 046 (maestro_chunks pgvector
>   HNSW + grafo AGE `maestro_kg`) · módulo `maestro_indice.py` · superficie
>   `/v1/maestro/{salud,buscar,grafo}` · canal API de Foresito ENCENDIDO (era opt-in) con key
>   demo nueva · key al sandbox SOLO del compose principal (C3).
> - **C/D/híbrido E2E verdes:** semántica real (encontró permisos.md sin palabras literales) ·
>   jazz solo ve su carril · randito fail-closed · grafo con CONTIENE/REFIERE/ENLAZA
>   (los `[[enlaces]]` → Conceptos) + curadas de relaciones.md (DEPENDE_DE/USA) ·
>   `buscar --contexto` = C×D. Skill 22 de Foresito ampliado (usa la MISMA superficie).
> - **Batería:** 264 tests (4 nuevos) · ruff/format ✅ · ty 13 diagnósticos PRE-existentes
>   (0 míos) · auth 401 fail-closed · aislamiento sandbox intacto (alcanza agent:8788, NO postgres).
> - **🐛 4 cazados construyendo:** (1) valor de `--relaciones` colado como rama → KeyError ·
>   (2) regla AGE: el wrapper solo traga UNA columna/mapa (enteros pelones no castean) ·
>   (3) desvío de alcance: `--todo` indexó marca-personal → columna `indexar` en el tsv ·
>   (4) operativo: reinicié el agente con el one-shot dentro → lo mató; el diseño resumible
>   por hash lo salvó (relanzado, saltó lo hecho).
> - **Pendientes al cierre:** embebido de la rama for3s termina solo (~3.6K chunks, CPU local,
>   verificar con `maestro buscar` sobre for3s) · E2E conversacional de Foresito por Telegram
>   (smoke-test de Brian: "busca en el maestro dónde…") · push de for3s-os con la tríada cuando
>   Brian dé la orden · re-indexar tras push de los repos doc (`maestro indexar --todo && subir`).
>
> **🔬 BARRIDO SISTÉMICO POST-E2E (2026-07-20, pedido por Brian — patrón H-findings):**
> los bugs cazados en el E2E de Foresito se verificaron en TODAS las distribuciones:
> - **🔴 S1 — skills amputadas en silencio** (`conversation.py` inyectaba `contenido[:1500]`):
>   sistémico en v0.19.0. Víctima real: **brian con 16/16 skills del entrenamiento a 8,000
>   chars → el bot veía el 19% de cada receta desde el día uno**. Foresito 0/3 (skill 22
>   compactada) · general 0/0 · jazz/mashe apagadas. **FIX aprobado por Brian, opción (a):**
>   `SKILL_INYECCION_MAX = 8000` (fidelidad 100%; costo ~4K tokens SOLO cuando aplica una
>   skill, máx 2/turno) + test-guardia que delata si alguien lo vuelve a bajar.
> - **🟠 S2 — "busca/consulta…" no disparaba el tool-loop** (solo "ejecuta/corre"): fix
>   `huele_a_maestro` (aditivo, 6 tests) para las frases del Maestro; el patrón general
>   conservador se queda (decisión pendiente solo si Brian quiere ampliarlo).
> - **🟡 S3 — el canal API NO corre tools en NINGUNA instancia** (usa `send` plano por
>   diseño): al pedir ejecución por API el modelo NARRA e inventa resultados (Foresito
>   "reportó" un error de red que los logs desmintieron). Afecta la promesa del canal para
>   clientes (general/NavigoX). **Decisión de producto PENDIENTE de Brian — no se tocó.**
> - Extra cazado en la propagación: el mapeo de la key al sandbox estaba en el compose
>   COMPARTIDO → general/jazz/mashe la habrían heredado al recrear. Cerrado con
>   `FOR3S_SANDBOX_API_KEY` que SOLO define el .env del principal (fail-closed).
>
> **Diseño original aprobado (histórico):**
> Regla de Brian (2026-07-19, origen de esta ronda): *"quiero que todo esto de Mente OS Maestro
> esté conectado, que realmente tenga un flujo — que no se construya por separado y que cuando
> queramos acoplar nada falle, ni mandemos a llamar la misma acción varias veces por falta de
> arquitectura."* → C y D NO son dos proyectos: son dos salidas de UNA misma tubería.
> Método de Fases "F" (`rules/ESTANDAR_Metodo_Fases_F.md`). Creada 2026-07-19.

---

## 0 · Diagnóstico del terreno (por qué hace falta el núcleo ANTES de C y D)

Investigación 2026-07-19 sobre `Mente/Maestro/`. El Maestro v1 (F1-F5) funciona, pero ya tiene
**deuda de arquitectura que C y D multiplicarían** si se construyen encima tal cual:

1. **Punteros triplicados:** la lista de ramas vive en 3 lugares sincronizados A MANO —
   el heredoc `PUNTEROS` dentro del script `maestro` (líneas 16-22), la tabla §PUNTEROS GIT de
   `Maestro/registro.md` y la prosa por rama del mismo registro. El propio código dice *"sincronizar con
   registro.md"* = bug esperando. Si C y D leen ramas, serían el 4º y 5º lugar.
2. **Puerta de permisos encerrada en bash:** `_permiso_lectura()` vive dentro del script `maestro`
   y parsea `Maestro/permisos.md` con grep. C y D necesitan la MISMA puerta (una búsqueda que devuelva
   chunks de ramas que no puedes leer = fuga). Si cada puente re-implementa la puerta → divergen.
3. **Sin identidad de documento:** hoy se lee "lo que haya" en el clon efímero. C necesita chunks
   con ID estable, D necesita nodos con ID estable — si cada uno inventa su esquema de IDs, nunca
   se podrán cruzar (y el cruce C×D es el pago grande).

**Conclusión F0:** primero un **NÚCLEO (fases N)** que mate las 3 deudas y dé contratos únicos.
C y D se enchufan al núcleo, no al script v1.

---

## 1 · Lo que se REUSA (nada nuevo que ya exista)

| Pieza existente | La reusa |
|---|---|
| Clon efímero `--depth 1` (puente A) | El indexador N2 — misma técnica, cero replicación |
| Postgres + pgvector + BGE-M3 (instancias For3s) | Almacén C — mismo motor de embeddings del producto |
| Apache AGE + Cypher (grafo de memoria) | Almacén D — mismo motor, un grafo nuevo un nivel arriba |
| Canal API `/v1/*` (auth X-API-Key, cuotas) | Superficie única `/v1/maestro/*` |
| Modelo H8 de permisos (dueño/miembro/lector, fail-closed) | Puerta única N1 |
| Puente E (Foresito lee el Maestro, skill 22) | Foresito consume C y D por la MISMA API |
| Gate NavigoX (`feedback_puente_mentes_os_gate`) | El indexador lo respeta EN LA FUENTE |

---

## 2 · ARQUITECTURA — el flujo único (leer esto antes que los planes)

```
                    punteros.tsv  ←— UNA fuente de ramas (N0)
                         │
        ┌────────────────┼────────────────────┐
        ▼                ▼                    ▼
   maestro leer/grep   maestro indexar (N2)  mente-os-nueva
   (puente A, hoy)          │                (registra ahí mismo)
                            │  clon efímero → normaliza →
                            │  documentos con ID = rama:ruta#chunk
                            │
              ┌─────────────┴─────────────┐   ← UNA pasada, DOS salidas
              ▼                           ▼
      [C] embeddings BGE-M3        [D] nodos + aristas
       → pgvector                   → grafo AGE "maestro"
       (schema maestro)             (mismos IDs que C)
              │                           │
              └─────────────┬─────────────┘
                            ▼
                 /v1/maestro/*  (superficie API única, N3)
                 buscar · grafo · indexar · salud
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        maestro buscar  maestro grafo   Foresito 👑
        (CLI, C2)       (CLI, D3)       (skill, C3/D4)
                            │
                 PUERTA ÚNICA de permisos (N1)
                 filtra por carril ANTES de devolver, fail-closed
```

### Los 6 CONTRATOS anti-duplicación (la respuesta directa a la regla de Brian)

1. **Punteros = `Maestro/punteros.tsv`, un solo archivo.** `maestro`, `mente-os-nueva`, el indexador y el
   registro lo leen. La tabla de `Maestro/registro.md` pasa a decir "generada de punteros.tsv".
2. **Permisos = una sola función.** La puerta (modelo H8) vive UNA vez (lib `maestro_lib`); la
   llaman leer/grep/buscar/grafo/API. Nadie re-implementa el grep de permisos.md.
3. **Indexador = una sola pasada.** `maestro indexar` produce el documento normalizado y de ahí
   salen LAS DOS salidas (embedding + grafo). Jamás dos recorridos separados de las ramas.
4. **IDs = un solo esquema.** `rama:ruta#chunk` idéntico en pgvector y en AGE → un resultado de
   búsqueda (C) salta a su nodo (D) sin traducción. Este contrato es lo que hace posible C×D.
5. **API = una sola superficie.** `/v1/maestro/*`. El CLI y Foresito consumen LO MISMO — el skill
   de Foresito no es otra implementación, es otro cliente.
6. **Gate en la fuente.** NavigoX (y cualquier rama gate=1) NO entra al indexador: no hay
   embeddings ni nodos de contenido gateado que "limpiar después". Fail-closed desde el origen.

### Decisión de almacén (recomendación)

**Schema `maestro` dentro del Postgres de Foresito** (instancia `for3s`, compose principal).
- Por qué: Foresito ES el Agente Maestro (decisión Brian 2026-07-18) — su BD ya tiene pgvector +
  AGE + BGE-M3 cargado + backup RESTORE-verificado. El índice del Maestro es conocimiento de la
  empresa: le pertenece. Cero contenedores nuevos que mantener.
- Frontera dura: schema `maestro` SEPARADO de la memoria episódica de Foresito (sus episodios no
  se mezclan con el índice; el grafo AGE del Maestro es un grafo APARTE del de conceptos).
- Alternativa descartable: instancia dedicada `for3s-maestro` (más aislamiento, pero otro
  contenedor que cuidar y otro cupo de la suscripción — no se justifica hoy).

### El índice y la REGLA MADRE ("no replicamos, conectamos") — la única tensión, dicha de frente

La regla madre (REGLAS_MAESTRO §0) dice que el Maestro **nunca copia** contenido de las ramas.
Un índice semántico necesita, mínimo, embeddings por chunk; y para MOSTRAR resultados útiles,
normalmente el texto del chunk. Eso roza la regla. Cómo la respeta este diseño (en espíritu y
en letra):

- **El índice es un DERIVADO REGENERABLE, no una segunda fuente de verdad.** Se puede borrar
  entero y regenerar con `maestro indexar --todo`. La fuente sigue siendo la rama (git). Nada
  se edita en el índice; nadie lee el índice "en vez de" la rama — el resultado siempre cita
  `rama:ruta` y ahí vive la verdad.
- **Vive en el Postgres del server, NO en el repo del Maestro** — el Maestro en git sigue
  pesando KB (fiel a "ligero").
- **Decisión 6 para Brian — qué guarda el índice por chunk:**
  - **(a) embedding + texto del chunk** *(recomendada)*: resultados instantáneos con contexto.
    Es una copia TÉCNICA derivada (como el clon efímero, pero persistida como índice). Con la
    regla de derivado-regenerable + cinturón anti-secretos (§7), el espíritu queda intacto.
  - **(b) embedding + puntero SOLO** (purista): el texto se trae con clon efímero al momento de
    mostrar. Cero texto persistido, pero cada búsqueda paga un clon (lenta) y el híbrido D4 se
    encarece. Solo si Brian quiere la letra estricta de la regla madre.

---

## 3 · FASES N — el núcleo compartido (prerrequisito de C y D)

**N0 · Fuente única de punteros.** Crear `Maestro/punteros.tsv` (nombre|url|branch|índice|gate|carril|dueño).
Refactor: `maestro` lee el tsv (muere el heredoc) · `mente-os-nueva` agrega la fila al crear rama ·
`Maestro/registro.md` referencia el tsv. *Red de seguridad:* `maestro ramas` antes/después idéntico.

**N1 · Lib compartida + puerta única.** Extraer a `Maestro/maestro_lib` (bash o python, decidir en
construcción): `punteros()` · `permiso_lectura(user, rama)` · `clon_efimero(rama)`. `maestro` v1
pasa a consumir la lib. *Red:* los 5 casos E2E de F4 (brian pasa · randito fail-closed · jazz no ve
for3s · jazz sí ve diseno-jazz · gate primero) repetidos verdes.

**N2 · El indexador (una pasada).** `maestro indexar <rama>|--todo`: clon efímero → recorre `*.md`
→ chunks con ID `rama:ruta#chunk` + hash de contenido (idempotente: re-indexa SOLO lo cambiado) →
entrega el documento normalizado a los escritores C y D (en N2 aún no existen: escribe a un JSON
de staging que C1/D1 consumirán — así N2 se prueba solo). Respeta gate en la fuente (contrato 6).

**N3 · Superficie API.** Endpoints `/v1/maestro/salud` + `/v1/maestro/indexar` en la instancia
Foresito (patrón del canal API existente: X-API-Key + auditoría). `buscar`/`grafo` se suman en
C2/D3 — la superficie nace aquí para que TODO pase por ella desde el día uno.

---

## 4 · PLAN PUENTE C — búsqueda semántica global (fases C1-C4)

**Meta:** *"¿qué rama sabe de X?"* respondido por SIGNIFICADO, con permisos, desde CLI y Foresito.

- **C1 · Almacén + escritor de embeddings.** Migración: schema `maestro`, tabla `doc_chunk`
  (id, rama, ruta, chunk_texto, hash, embedding vector, indexado_en). El escritor C consume la
  salida de N2 y embebe con el BGE-M3 ya cargado en Foresito. *Red:* indexar rama `maestro`
  (pequeña) → contar chunks = archivos esperados; re-indexar sin cambios → 0 escrituras.
- **C2 · `maestro buscar "<pregunta>" [--rama <r>]`.** Endpoint `/v1/maestro/buscar`: embebe la
  pregunta → top-k por coseno → **filtra por la puerta única ANTES de devolver** (contrato 2:
  jazz busca → solo chunks de ramas de su carril; fail-closed). CLI = cliente del endpoint.
  *Red:* pregunta con sinónimos (sin palabras literales del doc) encuentra el doc correcto;
  `MAESTRO_USER=jazz` jamás recibe chunks de `for3s`.
- **C3 · Foresito busca en el Maestro.** Ampliar el skill agente-maestro (id 22): ante "¿dónde
  dice X?" llama `/v1/maestro/buscar` — MISMO endpoint, otro cliente (contrato 5). *Red:* pregunta
  E2E por Telegram a Foresito → responde citando rama+ruta.
- **C4 · Batería §5-BIS.** Todo el sistema, no el carril: tests + arranque real + /salud 0 FAIL +
  los 5 casos de permisos + gate navigox (indexador NUNCA lo tocó: 0 chunks) + E2E C2/C3 +
  regresión puente A/B intactos.

---

## 5 · PLAN PUENTE D — grafo de Mente OS (fases D1-D4)

**Meta:** las ramas como RED navegable (depende de / cruza con / gobernada por), cruzada con C.

- **D1 · Modelo + almacén del grafo.** Grafo AGE `maestro` (separado del de conceptos). Nodos:
  `Rama` · `Doc` · `Persona` · `Proyecto` · `Decision`. Aristas v1: `APUNTA_A` · `DEPENDE_DE` ·
  `GOBERNADA_POR` · `CRUZA_CON` · `DECIDE`. Los nodos `Doc` llevan los `chunk_ids` de C
  (contrato 4). Sembrado inicial DESDE `Maestro/punteros.tsv` + `Maestro/permisos.md` (ramas, dueños, carriles —
  cero captura manual). *Red:* Cypher "vecinos de diseno-jazz" devuelve jazz + carril diseño.
- **D2 · Extracción de relaciones (misma pasada de N2).** El escritor D consume LA MISMA salida
  del indexador que C (contrato 3) y saca aristas de: enlaces `[[...]]` · referencias a rutas
  (`Doc/X.md`, `Cuerpo/Y.md`) · menciones entre ramas. Más `Maestro/relaciones.md`: archivo
  DECLARATIVO versionado para relaciones curadas a mano ("diseno-jazz DEPENDE_DE for3s:nodo-UI")
  que el indexador ingiere — lo curado convive con lo automático sin tocar código. *Red:*
  indexar → arista conocida aparece; quitarla de relaciones.md + re-indexar → desaparece.
- **D3 · `maestro grafo <consulta>`.** Endpoint `/v1/maestro/grafo` + CLI: `vecinos <nodo>` ·
  `ruta <a> <b>` · `depende-de <rama>`. Puerta única aplicada a QUÉ nodos se devuelven (jazz ve
  el subgrafo de su carril). *Red:* los 5 casos de permisos sobre el grafo.
- **D4 · C×D — el pago: búsqueda híbrida.** `maestro buscar --contexto`: los top-k de C saltan a
  sus nodos D (mismos IDs) → expande 1 nivel de vecinos → respuesta = chunks + "esto se conecta
  con…". Foresito la usa (skill 22). **Este es el salto de buscador a super-cerebro navegable.**
  *Red:* E2E — pregunta sobre diseño devuelve chunks de diseno-jazz + su conexión al núcleo.

---

## 6 · Orden de construcción (entrelazado, no separado)

```
N0 → N1 → N2 → N3 → C1 → C2 → D1 → D2 → C3 → D3 → D4 → cierre (batería total + tríada)
```
- C1/C2 antes que D porque D4 (híbrido) necesita C vivo, y C valida el indexador con la salida
  más simple. D1 puede arrancar en paralelo a C2 si el staging de N2 ya está estable.
- **Cada fase:** investigar terreno → construir defensivo (cero hardcodeo, todo por ENV como el
  puente B) → su red de seguridad → commit firmado. **Server-primero** (push solo con orden).
- Al cierre: batería §5-BIS COMPLETA + actualizar `Maestro/registro.md`/`REGLAS_MAESTRO.md`/
  `ALTERNATIVAS_QUE_CONECTAR.md` (C y D pasan de "menú" a "construido") + RETOMAR + memoria.

## 7 · Riesgos vigilados

- **Consumo de tokens:** indexar NO llama al LLM (BGE-M3 es local). El único costo LLM es cuando
  Foresito responde usando los resultados — igual que hoy. Indexación manual (no cron) hasta que
  Brian apruebe metérsela al DMN nocturno.
- **Secretos:** el indexador solo ve lo que los repos ya exponen (los .gitignore de F2 ya excluyen
  secretos), y H-11 blindó el tubo — aún así, la batería incluye grep de patrones de secretos
  sobre `doc_chunk` como cinturón extra.
- **Peso:** el Maestro repo sigue en KB (el índice vive en Postgres del server, no en git).
- **No romper v1:** puentes A/B y los 5 casos F4 son parte de la red de CADA fase N.

## 8 · Decisiones que Brian aprueba (F0 → F1)

| # | Decisión | Recomendación |
|---|---|---|
| 1 | Almacén | Schema `maestro` en Postgres de Foresito (§2) |
| 2 | Cadencia de indexado | Manual (`maestro indexar`) hoy; DMN nocturno = mejora futura |
| 3 | Alcance inicial de ramas | `for3s` + `diseno-jazz` + `maestro` (el propio repo). `marca-personal` FUERA (otro proyecto, gate de scope). `navigox` FUERA (gate) |
| 4 | Orden | El de §6 (C primero, D encima, D4 los cruza) |
| 5 | Lib N1 | bash vs python — propongo decidirlo al investigar N1 (lo que menos fricción dé con el canal API) |
| 6 | Qué guarda el índice por chunk (§2, tensión con la regla madre) | (a) embedding + texto, como derivado regenerable — o (b) purista: solo embedding + puntero |

### Alineación verificada con el diseño original (2026-07-19)

Contrastado contra `REGLAS_MAESTRO.md` + `Alma/Vision_Mente_OS_Maestro_...md`:
- REGLAS §1 define al Maestro como **"el índice + GRAFO de todos los Mente OS"** → el puente D
  no es un agregado: es la mitad de la definición que aún no estaba construida.
- La visión §3 preguntaba literalmente *"¿un grafo de grafos? ¿el canal API como puente? ¿una BD
  que los une?"* → C y D son la respuesta de la Ronda F0 a esas preguntas abiertas.
- REGLAS §2.2: los puentes "conviven" y se suman → C y D se SUMAN a A/B/E, no los reemplazan.
- Unidireccional (§3), puerta H8 (§7), gate NavigoX (§3), rama autónoma (§3), marca-personal
  separada (§3): los 6 contratos de esta ronda los respetan uno a uno.
- Única tensión: el índice persistido vs "no replicar" → resuelta arriba (derivado regenerable,
  decisión 6).

---

*Relacionado: `Maestro/ALTERNATIVAS_QUE_CONECTAR.md` (el menú original) · `work/Ronda_Mente_OS_Maestro.md`
(F1-F5) · `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md` · memoria
`project_mente_os_maestro_f1_f2`.*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_Maestro_Puentes_C_D.md`).
