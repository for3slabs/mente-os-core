# LA VERDAD DE V1 — qué es For3s OS realmente, medido

**Status:** current · **Type:** analysis · **Updated:** 2026-08-12 · **Owner:** brian
**Level:** 📕 **EL DOCUMENTO DE LA VERDAD** — lo que el sistema ES, contra lo que dice ser
**Verified by:** cada afirmación lleva su medición; se re-mide con `bin/conectar-servidor`
**Exempt:** size, split-signal · ⭐ **DOCUMENTO DE LA VERDAD — orden de Brian 2026-08-12:**
*"crea un nuevo MD que detalle a lujo de precisión TODO absolutamente todo lo analizado, hazlo lo
más grande posible… va a ser nuestro MD de la verdad de v1"*. Partirlo destruiría su función: es
**el único lugar donde el sistema se ve entero y de una vez.**

## Purpose

> **Brian, 2026-08-12:** *"Ya leímos todo Mente OS y podemos decir qué está pasando con todo lo
> que tenemos."*

Este documento responde una sola pregunta, sin adornos: **¿qué es For3s OS de verdad, hoy?**

Nace de **50 auditorías** ejecutadas contra el servidor entre el 11 y el 12 de agosto de 2026:
15 de componentes (A1-A15) · 20 de uso real con los datos de Brian (A16-A35) · 15 de comportamiento
y canales (C1-C15) · más la lectura de **~45,000 líneas** de `Mente/` — el 100% de lo que gobierna,
decide o registra.

⛔ **Lo que este documento NO hace:** decidir, planificar ni proponer trabajo. Solo **declara lo
que hay**, con su evidencia y su fecha.

---

## 📑 ÍNDICE

| § | Qué responde |
|---|---|
| **0** | 🎯 **LA VERDAD EN UNA PÁGINA** — si solo lees una sección, esta |
| **1** | Qué es For3s OS: las 3 identidades que conviven |
| **2** | El inventario físico completo |
| **3** | Los 11 nodos: cuáles existen, cuáles no, y dónde vive cada uno |
| **4** | Los 16 hitos: 13 construidos, 3 no |
| **5** | Las 7 ventajas defendibles: cuáles son reales |
| **6** | Los datos: 33,908 memorias y qué pasa con ellas |
| **7** | Lo que corre de noche: el cerebro nocturno, medido |
| **8** | Los canales: cómo se comunica el sistema consigo mismo |
| **9** | Seguridad: lo bueno, lo grave y lo ausente |
| **10** | Rendimiento y coste real |
| **11** | ⭐ **EL DIAGNÓSTICO: por qué el diseño y el código divergieron** |
| **12** | 📋 **LOS 24 HALLAZGOS** — y por qué solo 4 importan hoy |
| **13** | ✅ **LO QUE ESTÁ BIEN** — 14 fortalezas que no se tocan |
| **14** | ⚠️ Mis 8 errores en esta auditoría, corregidos |
| **15** | Las 34 lecciones (L-01 a L-34) |
| **16** | Lo que sigue sin medir |
| **17** | Cómo se re-mide todo esto |

---

## 0 · 🎯 LA VERDAD EN UNA PÁGINA

```
╔════════════════════════════════════════════════════════════════════════════╗
║                      FOR3S OS — LA VERDAD, 2026-08-12                       ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  QUÉ ES:  un agente-cerebro de 11 nodos, self-hosted, en producción        ║
║           28 contenedores · 3 instancias · 112 archivos .py · 47 migr.     ║
║                                                                            ║
║  ESTADO:  13 de 16 hitos construidos · pasa 6/6 el gate de su Fase 1       ║
║           9 de 11 nodos con archivo propio                                  ║
║           construido en 2 MESES lo que su plan estimaba en 6-7             ║
║                                                                            ║
║  LO QUE FALTA (y NO es deuda: es Fase 4-5 del plan):                       ║
║           🔴 Amígdala (nodo 7)  · 🔴 Tálamo (nodo 8)                        ║
║           🔴 Output Gate · 🔴 Auth/RBAC · 🔴 Prometheus · 🔴 eval            ║
║                                                                            ║
║  LO QUE FALLA DE VERDAD, HOY (4 de 24 hallazgos):                          ║
║           🔴 H-01  el contenido de las conversaciones está EN CLARO         ║
║           🟠 H-02  el contador de recuperación no cuenta lo importado       ║
║           🔴 H-04  el digest de insights lleva 29 días sin entregar         ║
║           🔴 H-03  una instancia huérfana con 2,782 memorias y token roto   ║
║                                                                            ║
║  LO QUE ESTÁ EXCELENTE:                                                     ║
║           ⭐ la microglía — 41% podado · SUPERÓ al estado del arte           ║
║           ⭐ la cadena de auditoría — 12,908 eventos, hash íntegro           ║
║           ⭐ el aislamiento — más fuerte que lo diseñado                     ║
║           ⭐ el grafo — 31,037 nodos · 91.3% consolidado                     ║
║                                                                            ║
║  LA FRASE:  For3s OS no está roto ni abandonado. Está en la Fase 1-3 de    ║
║             un plan de 6, adelantado en calendario, con 2 defectos reales  ║
║             y un diseño que corre 3 fases por delante del código.          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## 1 · QUÉ ES FOR3S OS — las 3 identidades que conviven

⭐ **Medido: el nombre "For3s OS" designa tres cosas distintas, y confundirlas es la causa de
media confusión en el repo.**

| # | Identidad | Qué es | Dónde vive | Estado |
|---|---|---|---|---|
| **1** | **El DISEÑO** | 10 rondas · 40 decisiones LOCKED · 11 nodos · 24 edges · 3 pilares | `work/Ronda_*` (65 archivos, 32,377 líneas) | ✅ **100% cerrado** (30-may → 9-jun) |
| **2** | **El CÓDIGO** | 112 `.py` · 48 `.sql` · 28 contenedores | servidor `for3s`, `~/for3s-os` | 🟢 **en producción** |
| **3** | **La INSTANCIA de Brian** | 33,908 memorias · 12,908 eventos · 16 skills | BD de `for3s-brian-postgres-1` | 🟢 **viva** |

**Las 3 son ciertas. Ninguna describe a las otras dos.**

| Se pregunta… | Responde… |
|---|---|
| *"¿For3s OS tiene Output Gate?"* | **el DISEÑO sí** (R7 B2, LOCKED) · **el CÓDIGO no** |
| *"¿Tiene 11 nodos?"* | **el DISEÑO sí** · **el CÓDIGO 9 de 11** |
| *"¿Recuerda?"* | **la INSTANCIA sí**: 33,908 episodios, 91.3% al grafo |

---

## 2 · EL INVENTARIO FÍSICO COMPLETO

### 2.1 · El código

| Capa | Cuánto | Dónde |
|---|---|---|
| **Núcleo `for3s_core`** | **76 archivos · 26,939 líneas** | `packages/for3s-core/src/for3s_core/` — **plano, sin subcarpetas** |
| Tests | **28 archivos** | `tests/` |
| Fuera del núcleo | **8** | `scripts/` (3) · `docker/render` (2) · `docker/sandbox` (1) · SDK molde (1) · `src/for3s_os` (1) |
| **Migraciones SQL** | **47** — todas aplicadas | `for3s_core/migrations/` |
| Docker | 2 compose · **5 Dockerfiles** · 4 shell | `docker/` |
| CI | **4 workflows** (`release` · `scorecard` · `trivy` ×2) | `.github/workflows/` |
| Documentación | 22 `.md` + un sitio web | raíz y `docs/` |
| **TOTAL** | **112 `.py` · 48 `.sql`** | |

⚠️ **Corrección registrada:** la primera auditoría reportó *"76 archivos"* como el total del
sistema. **Son 76 del núcleo.** Miró una carpeta y habló del todo.

### 2.2 · La distribución del peso

| Tramo | Archivos |
|---|---|
| **> 800 líneas** | **3** |
| 400 - 800 | 15 |
| 150 - 400 | 34 |
| < 150 | 24 |

**Los 3 gigantes = 28% del núcleo:**

| Archivo | Líneas | % | Qué es |
|---|---|---|---|
| `telegram_channel.py` | **4,570** | **17%** | ⚠️ la puerta que Brian usa a diario |
| `conversation.py` | 1,871 | 7% | el que decide qué hace el agente por turno |
| `api_channel.py` | 1,146 | 4% | el canal que se vende |

⭐ **Y el contraste que define la forma del sistema:** `agent.py` tiene **90 líneas**.
**El agente es 50 veces más pequeño que su puerta.** La lógica no vive en el agente: vive en el canal.

📊 **`telegram_channel.py` se declaró deuda en junio con 3,350 líneas. Hoy tiene 4,570: creció
36% DESPUÉS de señalarse.**

### 2.3 · La higiene — mejor de lo esperado

| Medida | Resultado |
|---|---|
| Funciones | 492 |
| **Con docstring** | **76 / 76** ✅ |
| **Con type hints** | **76 / 76** ✅ |

⭐ **El problema de For3s OS no es higiene.** Está documentado y tipado al 100%.

### 2.4 · 🔴 La cobertura de tests, con dos medidas

| Medida | Qué dice | Cuántos |
|---|---|---|
| Sin mención en ningún test | ningún test nombra el módulo | **28 de 75** |
| ⭐ **Cero líneas ejecutadas** (`.coverage` real) | la corrida de tests no tocó ni una línea | **36 de 76 (47%)** |

**Los mayores sin ejecutar:** `tasks` (722) · `entrenamiento_backlog` (643) · `consolidator` (603) ·
`dmn_tasks` (503) · `health` (486) · **`governor` (444)** · `entrenamiento_repo` (404) ·
**`multiagente` (397)**.

⚠️ **El gobernador que frena al sistema y el equipo multi-agente no se ejercitan.**

### 2.5 · El despliegue

**28 contenedores vivos · 10 servicios distintos · 3 instancias.**

| Servicio | Copias |
|---|---|
| `agent` · `worker` · `postgres` · `valkey` · `grafana` · `sandbox` · `render` · `github-mcp` · `github-mcp-write` | **3 cada uno** |
| `admin` | **1** ⚠️ solo en `general` |

**Recursos del servidor:** RAM **18 GB** (3.8 en uso) · disco 937 GB (172 usados, 20%) ·
los 3 `agent` consumen ~900 MB cada uno (cargan BGE-M3).

⚠️ **Medido: 18 GB, no los 32 GB que el diario de mayo declaraba.**

### 2.6 · 🟠 La tercera instancia — huérfana

| | |
|---|---|
| Nombre | `for3s-agent-1` — **sin prefijo, sin dueño declarado** |
| Datos | **2,782 memorias** · 2,494 eventos de auditoría |
| Servicios propios | `postgres` `valkey` `grafana` `worker` `sandbox` |
| RAM | **933 MB** — la que más consume de las tres |
| 🔴 Su token | `TELEGRAM_BOT_TOKEN=# migr…` — **un comentario, no un token** |

**Lleva horas corriendo, guarda datos, y su bot no puede conectarse.**

---

## 3 · LOS 11 NODOS — cuáles existen y dónde vive cada uno

⭐⭐ **El mapa que la campaña necesita.** El documento canónico (`Mapeo_Nodo_Cerebral_Tabla_SQL`)
declara rutas con carpetas (`memory/…`, `orchestrator/…`) — **las 10 están muertas: el código es
plano.** Este es el mapa real, medido archivo por archivo:

| # | Nodo cerebral | Archivo REAL | Líneas | |
|---|---|---|---|---|
| **1** | Knowledge Graph (Neocorteza) | `kg.py` | 250 | ✅ |
| **2** | Hipocampo + Pattern Separation | `memory.py` | 716 | ✅ |
| **3** | PFC / Orquestador | `conversation.py` | **1,871** | ✅ |
| **4** | Ganglios Basales / Skills | `skills.py` | 292 | ✅ |
| **5** | Microglía (olvido) | `microglia.py` | 215 | ✅ |
| **6** | DMN (procesamiento offline) | `dmn.py` | 423 | ✅ |
| **7** | **Amígdala** (valoración rápida) | — | — | 🔴 **NO EXISTE** |
| **8** | **Tálamo** (router) | — | — | 🔴 **NO EXISTE** |
| **9** | Dual-Process Check | `confidence.py` | 274 | ✅ |
| **10** | Consolidación CLS | `consolidator.py` | 603 | ✅ |
| **11** | Neuromoduladores | `relevance.py` | 116 | ✅ |

📊 **9 de 11 = 82% con archivo propio.**

### 3.1 · La numeración canónica — y su trampa

`Mapeo` §0 avisa: **su propio cuerpo (§5-§19) usa numeración VIEJA.** El cuerpo modeló *"Action
Selection"* y *"Pattern Separation"* como nodos numerados; **el Grafo NO los numera** — son
funciones del Nodo 4 y del Nodo 2. Eso corrió la numeración y **dejó fuera a Tálamo y
Dual-Process**.

⚠️ **Un bloque que lea *"Nodo 8 — Amígdala"* en el cuerpo está leyendo el nodo 7 canónico.**

### 3.2 · 🔴 La Amígdala, capa por capa

El diseño (R9 B1) especifica **5 capas fail-fast**. Medido:

| Capa | ¿Existe? |
|---|---|
| 1 · patrones de injection **sobre la entrada** | 🟠 el patrón existe en `governor.py:123` — **solo escanea SKILLS NUEVAS** |
| 2 · normalización anti-evasión (base64, homoglifos, zero-width) | 🟠 `unicodedata` en `conversation.py` — **para normalizar palabras clave**, no como defensa |
| 3 · clasificador LLM (Haiku) | 🔴 no existe |
| 4 · canary tokens | 🔴 no existe |
| 5 · sanitización de contenido externo | 🔴 no existe |

🔬 **Verificado en el camino real: `Conversation.send()` recibe el mensaje y lo procesa sin
pasarlo por ningún escáner.**

🔴 **Sin adornos: For3s OS no tiene defensa contra prompt injection en la entrada del usuario.**

⭐⭐ **Y la neurociencia lo predijo en mayo** (`Cerebro/Cerebro_Humano_acercamiento2.md` §4.2, caso del
paciente S.M.): *"un agente sin amígdala trataría todos los bugs como iguales. **No sabría que un
bug de seguridad es más urgente que uno cosmético**."*

### 3.3 · La arquitectura real, según quién depende de quién

**Los cimientos** (si se rompen, cae todo):

| Módulo | Cuántos dependen |
|---|---|
| **`llm`** | **15** |
| **`audit`** | **14** |
| **`config`** | **10** |
| `memory` | 8 |
| `kg` · `conversation` | 6 |

**Los orquestadores:**

| Módulo | Dependencias | De ellas **perezosas** |
|---|---|---|
| `telegram_channel` | 41 | **26** |
| `conversation` | 21 | 13 |
| `tasks` | 17 | **16** |
| `api_channel` | 10 | **10 — todas** |

⭐⭐ **Dato que explica por qué nadie sabe cómo está construido For3s OS:** la mayoría de
dependencias son **imports perezosos dentro de funciones**, no en la cabecera. **El grafo real es
invisible para cualquier herramienta que lea solo las primeras líneas.**

**Las raíces** — 5 módulos que nadie importa **porque arrancan solos**: `telegram_channel` ·
`cli` · `api_admin_http` · `sandbox` · `entrenamiento_repo` (verificado: tiene `__main__` en la
línea 403). ✅ **No hay código muerto en el núcleo.**

---

## 4 · LOS 16 HITOS — 13 construidos

⭐ **El orden de obra real** (`Mapa_Construccion_Incremental`), medido contra el servidor.
**El tablero publica 3 de 18; la realidad es otra:**

| Hito | Tablero (11-jun) | **Medido (12-ago)** | Evidencia |
|---|---|---|---|
| **H1** HABLA | ✅ | ✅ | `agent.py` + `llm.py` |
| **H2** RECUERDA | 🔴 sin marcar | ✅ | **33,908 episodios** |
| **H3** TELEGRAM | ✅ | ✅ | 4,570 líneas |
| **H4** TIENE MANOS ★ | 🔴 sin marcar | ✅ | acciones de GitHub auditadas |
| **H5** MEMORIA REAL | ⬜ | ✅ | `kg.py` + **30,997 nodos AGE** |
| **H6** SE CUIDA | ⬜ | ✅ | microglía + consolidator + backup |
| **H7** DECIDE | ⬜ | 🔴 | **Tálamo ausente** — diferido en `PENDIENTES` |
| **H8** EQUIPO | ⬜ | ✅ | `multiagente.py` + `specialists.py` |
| **H9** SUEÑA | ⬜ | ✅ | **3,295 corridas DMN** |
| **H10** PLANEA | ⬜ | ✅ | `confidence.py` |
| **H11** EL FRENO | ⬜ | 🟡 | `governor.py` — **3 de 6 frenos reales** |
| **H12** APRENDE | ⬜ | ✅ | **16 skills** |
| **H13** CARA FORMAL | ⬜ | 🟡 | canal API ✅ · **Output Gate 🔴** |
| **H14** OJOS | ⬜ | 🟡 | Grafana ✅ · **Prometheus 🔴** |
| **H15** DEFENSAS | ⬜ | 🔴 | **Amígdala ausente** |
| **H16** PRODUCCIÓN | ⬜ | ✅ | **28 contenedores** |

📊 **13 de 16.**

### 4.1 · Y el gate de Fase 1 pasa 6 de 6

El Plan Maestro define un **gate objetivo por fase**. El de Fase 1, medido:

| Criterio | Medido | |
|---|---|---|
| Memoria persiste (episodios + KG + vector) | 33,908 episodios · **33,908 con embedding** | ✅ |
| CLS consolida a KG | **30,959 consolidados** · corrió ayer | ✅ |
| Microglía poda sin tocar audit | **13,974 podados** · corrió ayer | ✅ |
| Audit hash chain inmutable | **12,908 eventos, TODOS con hash** | ✅ |
| Costo medido | 79 corridas · **$5.17** | ✅ |
| PR de GitHub end-to-end | **14 acciones auditadas** | ✅ |

⭐⭐⭐ **For3s OS PASA el gate de Fase 1 de su propio plan.**

### 4.2 · Y va adelantado en calendario

| | |
|---|---|
| Sistema completo, **estimado** | ~9-10 meses |
| **MVP pilotable, estimado** | **~3-3.5 meses** |
| **Realidad medida** | **~2 meses de código** (primeras migraciones 5-jul) con MVP + cerebro + aprendizaje |

⭐⭐⭐ **For3s OS construyó en 2 meses lo que su propio plan estimaba en 6-7.**

---

## 5 · LAS 7 VENTAJAS DEFENDIBLES — cuáles son reales

La Visión declara 7 ventajas técnicas. Cruzadas con el código:

| # | Ventaja | Medido | |
|---|---|---|---|
| **1** | **PFC artificial** (metacognición) | `confidence.py` · **4 de 8 señales** · corre cada turno | 🟡 |
| **2** | **Knowledge Graph + Pattern Separation** | **31,037 nodos · 31,230 edges · 91.3% consolidado** | 🟢 |
| **3** | **Ganglios basales / skills emergentes** | 16 skills · 🔴 **sin NO-GO, sin dopaminergic, sin lifecycle** | 🟠 |
| **4** | ⭐ **Microglía artificial** | **13,974 podados (41%)** · decay real 0.225-0.916 · **4,230 candidatos** | 🟢🟢 |
| **5** | **DMN** (offline) | **3,295 corridas** · 5 tareas reales + 3 stubs | 🟢 |
| **6** | **Amígdala** | 🔴 **NO EXISTE** | 🔴 |
| **7** | **Grafo end-to-end** | 9 de 11 nodos · 🔴 **sin Tálamo** | 🟡 |

📊 **3 reales · 3 parciales · 1 ausente.**

### 5.1 · ⭐⭐⭐ Dónde For3s superó al estado del arte

`Arquitectura_Grafo_vs_Loop` §15.1 (mayo) listó los **7 problemas que nadie ha resuelto**. Uno:

> *"**Memory leak en agentes longevos.** Sin microglía artificial (poda), la memoria crece
> infinitamente. **Nadie la implementa bien.**"*

⭐⭐⭐ **For3s la implementó y funciona: 41% podado, con audit de cada olvido.** Es el único punto
donde el sistema **superó al estado del arte que su propio diseño describía.**

### 5.2 · Las 4 señales de confianza que faltan — declaradas desde junio

`H10_PLANEA` §1 (26-jun) las lista con su causa:

| Señal | Estado | Por qué |
|---|---|---|
| `llm_self_report` · `tool_success` · `schema_valid` · `historical` | ✅ **4 implementadas** | |
| `cost_accuracy` | ⚠️ neutra | *"no medimos estimado vs real por turno"* |
| `plan_consistency` | ⚠️ neutra | *"no hay plan-then-execute formal"* |
| `multi_agent_consensus` | ⚠️ neutra | *"solo aplica cuando corre el equipo"* |
| `rule_eval` | ⚠️ neutra | *"requiere golden set formal"* |

⭐ Con su definición: *"**Neutra = contribución honesta:** no suma ni resta señal falsa."*

---

## 6 · LOS DATOS — 33,908 memorias y qué pasa con ellas

### 6.1 · El censo: 49 tablas, 31 con datos, 18 vacías

| Tabla | Filas |
|---|---|
| `episodes_events` | **33,908** |
| `DERIVED_FROM` (grafo AGE) | 31,230 |
| `Episodio` (grafo AGE) | 31,037 |
| `audit_events` | 12,908 |
| `import_manifiesto` | 11,927 |
| `dmn_corridas` | 3,295 |
| `sessions` | **2,072** |
| `Concepto` | 1,342 |
| `cron_corridas` | 1,053 |
| `secrets` | 38 · `api_consumo` 35 · `skills`/`personas` 16 · `insights`/`api_clients` 15 |

### 6.2 · El ciclo de la memoria

| Medida | Valor |
|---|---|
| Memorias totales | **33,908** |
| **Importadas** (5-jul, 11 lotes) | **33,737 · 99.5%** |
| **Conversación real por Telegram** | **134 mensajes** |
| Por API | 37 |
| Consolidadas al grafo | **30,959 (91.3%)** ✅ |
| Podadas por la microglía | **13,974 (41%)** |
| Con embedding | **33,908 / 33,908** ✅ |
| 🔴 Con `veces_recuperado > 0` | **21** |
| Última memoria escrita | **30-jul** |
| Última conversación real | **25-jul** |

**La proporción del uso real:** 624,702 tokens de entrada contra 23,490 de salida — **26:1**.

### 6.3 · 🟠 H-02, con su diagnóstico correcto

⚠️ **Este hallazgo se diagnosticó mal DOS veces antes de medirse bien.** La versión correcta:

**La búsqueda SÍ alcanza las memorias importadas.** `memory.py:255-266` tiene un parámetro
explícito, `incluir_import`, añadido el **5-jul en E5b** con este comentario:

> *"suma el corpus IMPORTADO (`channel='import'`, sesiones `oc:*`) del MISMO humano — **sin esto,
> la memoria heredada de otros agentes era invisible para el chat** (bug cazado en E5b)"*

🔬 **Probado en vivo:** `recordar("que sabes de godinez studio")` devuelve **2,436 caracteres**
con material de `fruterito-principal` del 25-mar y 4-abr.

🔴 **El defecto real es OTRO — la asimetría lectura/escritura:**

| | Filtro |
|---|---|
| **BÚSQUEDA** (`buscar_semantico`) | `session_id = $1` **OR `channel = 'import'`** ← cruza |
| **CONTADOR** (`tocar_recuerdos`) | `session_id = $1` ← **no cruza** |

**Un recuerdo importado se recupera y nunca se marca.** El `UPDATE` toca 0 filas, y la función es
defensiva (*"cualquier error se traga"*), así que nadie se entera.

⚠️ **Y la consecuencia NO es cosmética.** El docstring de `tocar_recuerdos`: *"usar un recuerdo lo
refresca Y cuenta el uso → **lo muy recuperado resiste mejor el olvido**"*.

🔴 **Un recuerdo importado que se usa cada día sigue envejeciendo como si nadie lo tocara.**
📊 **Y ya hay 4,230 episodios con `relevance < 0.3`** — el umbral de poda.

⭐⭐ **El sistema podría BORRAR lo que sí usa.**

### 6.4 · El origen de las 33,737 — los 6 agentes OpenClaw

| Agente | Turnos | Qué era |
|---|---|---|
| 📰 **watchdog** | **20,749** | se reseteaba cada madrugada (job diario) |
| 🔨 **dev** | **17,096** | ⭐ *"nadie lo tenía censado"* · el desarrollador de Godínez Studio |
| 🍍 **main** (Personal) | **6,045** | lo cotidiano de Brian · la serie INMORTALIDAD |
| 👔 empleado | 708 docs | ⚠️ **el mismo workspace sincronizado** |
| 🔴 cipher · 🔵 helix | 61 · 107 | casi sin usar |

⭐ **El hallazgo que redujo el trabajo a la mitad:** *"wsl es en su mayoría un ESPEJO del
principal. **6,600 de 11,664 archivos son duplicados exactos (sha256)**."*

**Y la disciplina del import:** `11,664 / 11,664 decididos, 0 pendientes` — cada archivo con
veredicto. **19 archivos de secreto detectados y enviados al vault, no a la memoria.**

### 6.5 · 🔴 Las 18 tablas vacías — con su migración de origen

| Tabla | Migración | Qué capacidad no se usa |
|---|---|---|
| **`decisiones`** | `032` | ⭐ **el sistema no decide nada** |
| **`trace_events`** · **`trace_alertas`** | `042` · `043` | ⭐ **For3s TRACE no registra** — se presentó en el Incubathon |
| `misiones` | `045` | el Frente E "confianza para delegar" |
| `governor_bloqueos` | `020` | el gobernador nunca ha bloqueado nada |
| `maestro_chunks` | `046` | el índice maestro |
| `gh_files` · `gh_resources` | `004` | GitHub MCP sin datos |
| `estado_persona` · `tema_estado` · `temas_equipo` · `solicitudes` · `consulted_web` · `api_waitlist` | varias | |
| `_ag_label_*` (4) | `034` | internas de AGE — vacías es normal |

⭐ **33,908 episodios guardados y `decisiones` en cero.** El sistema **recuerda muchísimo y no
decide nada.**

### 6.6 · Lo que sabe de Brian — con un error

```json
{ "nombre": "Brian",
  "rol": "jazz",          ← 🔴 la instancia borrada el 6-ago
  "zona": "México (CST/CDT)",
  "estilo": "Español MX. Quiere corrección ortográfica con el error mostrado.
             Avisar SIEMPRE antes de operaciones de BD." }
```

✅ **El campo `estilo` capturó reglas reales.** Conoce **16 personas** con sus roles.

### 6.7 · 🔴 Los insights: encontró valor y se lo quedó

**15 generados · 9 nunca entregados.** Entre los retenidos:

- *"**Lanzas tareas y las cancelas antes de que terminen**"* (patrón)
- *"**Consumo de tokens como fricción recurrente**"* (patrón)
- *"PR #129 quedó sin mergear"* · *"UX Fixes #3-#12 sin tocar"*

⭐ **Todos del 13-14 de julio. Hace 29 días que no genera ninguno.**

---

## 7 · EL CEREBRO NOCTURNO — trabaja mucho, hace poco

### 7.1 · El dato global

**3,295 corridas del DMN. Hicieron algo 135 veces. El 4.1%.**

### 7.2 · Por tarea (7 días)

| Tarea | Intentos | Corrió | Por qué |
|---|---|---|---|
| **`cache_prewarming`** | 114 | 🔴 **0** | `trigger_ok=false` siempre |
| **`embedding_precompute`** | 114 | 🔴 **0** | idem |
| **`routing_learning`** | 114 | 🔴 **0** | idem |
| `insight_mining` | 114 | 11 | *"sin nada que valga (silencio antes que relleno)"* |
| `memory_consolidation` | 1 | 1 | ✅ |
| `eval_regression_detection` | 1 | 1 | *"v1 métrica simple (golden set = deuda)"* |

⭐⭐ **Y la causa está escrita en el propio código** (`dmn_tasks.py:11-14`):

> *"**STUBS HONESTOS** (sin infra todavía — **NO fingen trabajo, lo declaran en su outcome**):
> `routing_learning` (no hay router multi-modelo: **H7 enrutamiento bloqueado**) ·
> `eval_regression_detection` (no hay golden set formal)."*

⚠️ **No son un bug: son límites declarados.** 🔴 **El defecto real es de telemetría: un stub
honesto y una tarea rota se registran idénticos.**

### 7.3 · Qué hace el sistema con su tiempo

**Auditoría de 7 días: 486 acciones.**

| Acción | Veces | % |
|---|---|---|
| **`microglia_forget`** | **484** | **99.6%** |
| `cls_consolidation` | 2 | 0.4% |

**Histórico: 11,455 de 12,908 (89%) son la microglía olvidando.**

### 7.4 · 🔴 Los 13 jobs del cron — y el worker que vive media jornada

| Job | Hora UTC | Última corrida |
|---|---|---|
| 11 jobs | 05:00-10:00 | **ayer** ✅ |
| `health_check` | 10:30 | 26-jul |
| 🔴 **`digest_valor`** | **14:00** | **14-jul · 29 días** |

**Corridas por hora UTC, 7 días:**

```
00h ██████████ 10     12h ░░░░░░░░░░  0
01h ██████████ 10     13h ░░░░░░░░░░  0
02h ██████████ 10  →  14h ░░░░░░░░░░  0  ← digest_valor AQUÍ
03h ██████████ 10     15h ░░░░░░░░░░  0
04h ████████    8     16h ░░░░░░░░░░  0
05h ███████     7     17h ░░░░░░░░░░  0
06h ██████      6     18h ░░░░░░░░░░  0
07h █████       5     19h ████        4
08h ██          2     20h ████████    8
09h ██          2     21h ██████████ 10
10h █           1     22h ██████████ 10
11h ░░░░░░░░░░  0     23h ██████████ 10
```

⭐⭐ **Ocho horas de silencio absoluto (11h-18h UTC), todos los días.** No es un fallo de código:
**el servidor es una laptop que se apaga.** `RestartCount=0`.

⭐⭐⭐ **Esto explica H-04 (los 9 insights retenidos):** su cartero está programado **a una hora en
la que el sistema no existe**. Su último registro: *"envío falló — insights quedan 'nuevo'
(reintento mañana)"*. **El mañana nunca llegó.** Y `proactivo=true`: **no lo apagó Brian.**

---

## 8 · LOS CANALES — cómo se comunica el sistema consigo mismo

| # | Canal | Qué conecta | Estado |
|---|---|---|---|
| 1 | **`Conversation`** | Telegram **y** API → el agente | 🟢 **bien conectado** |
| 2 | **`arq` sobre Valkey db1** | quien encola → el worker | 🟡 unidireccional |
| 3 | **La base de datos** | todos escriben, todos leen | 🟡 sin avisos |
| 4 | **HTTP crudo a `api.telegram.org`** | el worker → Brian | 🔴 camino paralelo |
| — | `MessageBus` | **nadie** | 🔴 **muerto** |
| — | Valkey pub/sub | — | 🔴 no existe |
| — | Postgres `LISTEN/NOTIFY` | — | 🔴 no existe |

✅ **Los dos canales de usuario SÍ convergen.** `api_channel.py:1068` lo dice en su docstring:
*"El MISMO camino que Telegram"*. **Ese cable está bien.**

### 8.1 · ⭐ El `MessageBus` — infraestructura completa que nadie usa

`multiagente.py:37` implementa un bus con: **buzón central del Hub** (cola de 1000) · **un buzón
por specialist** (100 cada uno) · **broadcast** · **backpressure**.

**Y su docstring declara su límite:** *"UN bus por batch (una corrida del equipo sobre una tarea)"*.

| Medida | Resultado |
|---|---|
| Quién importa `MessageBus` | 🔴 **nadie** |
| `asyncio.Queue` fuera de multiagente | 🔴 **cero** |
| Quién arranca `multiagente` | **solo `telegram_channel`** |

**Y contra su propio diseño (R5 B3):**

| | Diseño | Código |
|---|---|---|
| Tipos de mensaje | **10** | **3** |
| Patrones | **4** (incluido `specialist ↔ specialist`) | **3** — sin peer-to-peer |
| Rate limit por specialist | ✅ TokenBucket 50 msg/s | 🔴 no existe |
| Detección cross-batch | ✅ `SECURITY_VIOLATION` | 🔴 no existe |

### 8.2 · El cuello de botella

**`run_tool_loop` se llama desde UN solo sitio:** `conversation.py:1610`.

| Pieza | Qué gobierna | Quién la usa |
|---|---|---|
| `ConcurrencyManager` (444 líneas) | tokens por minuto, anti-429 | 🔴 **solo `llm.py`** |
| Semáforo de multiagente | **2 specialists** a la vez | solo dentro de multiagente |
| Valkey | 🔴 **solo caché** (`get`/`set`) | 5 módulos |

**Nada limita cuántas peticiones distintas atiende el sistema a la vez.**

### 8.3 · El veredicto por componente

| Componente | Cómo recibe | Cómo responde | |
|---|---|---|---|
| Telegram ↔ agente | `Conversation` | directo | 🟢 |
| API ↔ agente | `Conversation` | directo | 🟢 |
| Worker | `arq`/Valkey | 🔴 HTTP crudo a Telegram | 🟡 |
| Multi-agente | solo Telegram | bus interno y efímero | 🔴 |
| DMN | cron | escribe en BD | 🔴 **sin avisar a nadie** |
| Insights | lee BD | job de las 14:00 | 🔴 **muerto 29 días** |
| Microglía | cron | audita | 🟢 |

⭐ **El patrón: todo lo que corre DENTRO de una petición está bien conectado. Todo lo que corre
POR SU CUENTA escribe en la BD y no tiene forma de avisar a nadie.**

---

## 9 · SEGURIDAD — lo bueno, lo grave y lo ausente

### 9.1 · ✅ Lo que está bien

| Aspecto | Evidencia |
|---|---|
| **Secretos cifrados** | tabla `secrets` con `nonce` + `ciphertext` · **sin columna en claro** · 38 secretos |
| **Cadena de auditoría íntegra** | **12,908 eventos, TODOS con `hash_self` Y `hash_prev`** · **2 triggers** anti UPDATE/DELETE |
| **Aislamiento físico** | volúmenes `pgdata` separados por instancia · `brian` 33,908 vs `general` 18 |
| **Filtro por sesión** | las consultas a contenido usan `WHERE session_id = $1` — verificado leyendo las 4 sospechosas |

`crypto.py` implementa correctamente `load_or_create_master_key` · `derive_workspace_key` ·
`encrypt` · `decrypt`. **La criptografía está bien hecha.**

### 9.2 · 🔴 H-01 — el contenido de las conversaciones EN CLARO

**Leído directamente de la BD, sin descifrar nada:**

```
SELECT left(content,60) FROM episodes_events WHERE channel='telegram' AND role='user'…
→ "En lo que lo arreglas, te voy a dar información de máxima pr…"
→ "[imagen: foto.jpg] Sigue diciendo que es privado"
```

| | |
|---|---|
| Texto en claro | **15 MB** |
| Embeddings | 133 MB |
| BD total | 471 MB |

**Quién usa `crypto.py`:** solo `secret_store.py` y `automod.py`.
**Cifrado sobre `content`:** 🔴 **cero coincidencias.**

⭐⭐ **Y no es un olvido de implementación: es una decisión LOCKED sin implementar.**
**R2 B1 §1.6 (D-006), textual:** *"Payload JSONB + **columnas BYTEA cifradas (P4)**"*.
**Y P4 quedó LOCKED como:** *"híbrido app-layer AES-GCM + filesystem LUKS — defense in depth"*.

⭐⭐⭐ **Además viola una anti-visión declarada NO-NEGOCIABLE** (`Vision_For3s_Frontier` §9 #9):
*"For3s NO será una empresa que sacrifica seguridad por velocidad. **Security designed in.
No-negociable.**"*

⚠️ **Ironía medida:** uno de esos mensajes en claro dice literalmente *"Sigue diciendo que es
privado"*.

### 9.3 · La anti-visión #8, también incumplida — con su causa

*"For3s NO será dependiente de un solo proveedor de LLM. **Multi-provider desde día 1.**"*

🔴 **Realidad: Claude + fallback OpenAI, sin local.**

⭐ **Y la causa está documentada desde el día 1** (ticket `001_H1_HABLA`):

> *"⚠️ Suscripción OAuth solo permite rol For3s en el mensaje (no system); para rol en system →
> **API key** (clientes la necesitan igual)."*

⭐⭐ **Y la solución existe, PROBADA:** `work/SPIKE_OpenCode_segundo_proveedor.md` (11-jun) validó
end-to-end `For3s → opencode serve :4096 → LLM → OK`, dando acceso a GPT/Gemini/locales/Zen.
**Decisión: diferir a H7** — el mismo hito que tiene el Tálamo ausente. **OpenCode sigue instalado
y dormido en el servidor.**

### 9.4 · 🔴 Un secreto marcado para rotar hace 2 meses

El mismo spike: *"⚠️ **Key Zen `sk-vR316…` EXPUESTA en chat → ROTAR**"*.

**Medido: la rotación NO aparece en ningún archivo de pendientes.** Lleva desde el **11-jun**
declarada en un documento de trabajo y en ningún sitio donde alguien la vea.

⛔ **No sé si Brian la rotó por su cuenta.**

### 9.5 · El workspace único

Los 12,908 eventos de auditoría viven en `workspace_id = 'default'`. **Un solo workspace**, aunque
el código soporta varios (`derive_workspace_key` existe y funciona).

---

## 10 · RENDIMIENTO Y COSTE REAL

### 10.1 · Latencia — la cola es 18× la mediana

| Medida | Valor |
|---|---|
| **p50** | **2,770 ms** |
| **p90** | **49,966 ms** |
| **max** | **278,999 ms** (279 segundos) |
| **Ratio p90/p50** | **18×** |

⭐ **Valida la advertencia del paper de Stream RAG:** un sistema con p50 de 2.7s parece rápido;
su p90 de 50s dice que **una de cada diez veces el usuario espera casi un minuto.**

### 10.2 · Duración por job

| Job | n | p50 | max |
|---|---|---|---|
| `dmn_idle` | 856 | 73 ms | **279,050 ms** |
| `cls` | 20 | 39,732 ms | 221,310 ms |
| `status` | 20 | 12,336 ms | 31,245 ms |
| `relevance` | 19 | 8,081 ms | 18,665 ms |
| `backup` | 25 | 3,960 ms | 13,495 ms |

### 10.3 · Coste

| | |
|---|---|
| **Total del DMN** | **$5.17** (79 corridas con coste) |
| El más caro | `insight_mining` — **$3.72** en 62 corridas |
| ⚠️ `embedding_precompute` | **$0** pero **61,944 ms de media** — 62 s por corrida |
| Canal API | 35 llamadas · 193,622 tokens · última el 30-jul |

📊 **Y el diseño proyectaba $97-137/mes.** El coste real es de dos órdenes de magnitud menor —
porque el sistema corre con **suscripción**, no con API de pago.

### 10.4 · 🔴 Lo que NO se mide

| Camino | Mide su tiempo | Percentiles |
|---|---|---|
| `api_metering.py` — **lo que se cobra** | ✅ | ✅ p50 · p95 · max |
| `agent.py` — **el agente** | 🔴 | 🔴 |
| `tool_loop.py` | 🔴 | 🔴 |
| `multiagente.py` | 🔴 | 🔴 |

**De 76 archivos, solo 6 miden su propio tiempo.**

⭐ **En una frase: lo que se COBRA está medido; lo que se USA, no.**

**Instrumentación general:** 43 de 76 registran errores · 18 tienen timeout · 12 tienen reintento.
**El log de 24h del agente `brian`: 27 líneas, 4 con error.**

⚠️ **27 líneas en 24 horas no es silencio sano: es ausencia de instrumentación.**

---

## 11 · ⭐ EL DIAGNÓSTICO — por qué el diseño y el código divergieron

### 11.1 · La prueba dura: 15 de 15 tablas del diseño no existen

| Tabla del diseño | Ronda | ¿Existe? |
|---|---|---|
| `workspaces` | R2 B1 · el eje del multi-tenant | 🔴 |
| `workspace_secrets` · `secret_usage_audit` | R4 B1 (KEK) | 🔴 |
| `workspace_signing_keys` · `output_signatures` | R7 B2 (Output Gate) | 🔴 |
| `identities` · `identity_credentials` · `roles` | R7 B3 (Auth/RBAC) | 🔴 |
| `incidents` · `postmortems` · `alerts` | R8 B4 | 🔴 |
| `request_records` | R8 B1 | 🔴 |
| `eval_runs` · `eval_results` · `golden_datasets` | R3 B4 | 🔴 |
| `cost_alarms` · `cost_anomalies` | R3 B4 | 🔴 |
| `skills_events` · `episodes_state` | R2 B1 (Event Sourcing) | 🔴 |
| `audit_events_archive` | R8 B3 | 🔴 |

**La BD real tiene 41 tablas. Ninguna de las 15 está entre ellas.**

### 11.2 · ⭐⭐ El patrón: la fidelidad decae según se sube la pila

| Ronda | Capa | Fidelidad |
|---|---|---|
| **R1** Compute | el suelo | 🟢🟢 **la más fiel** — Python 3.12 exacto · `arq` · `mcp` · Valkey |
| **R2** Data | cimiento | 🟢 los 3 (PG+AGE+pgvector) · audit inmutable · el olvido funciona |
| **R3** LLM | motor | 🟡 Anthropic ✅ · 🔴 sin SSE, sin circuit breaker, sin eval |
| **R4** Tools/MCP | herramientas | 🟡 **1 de 4** servidores MCP |
| **R5** Orquestación | coordinación | 🟡 multiagente sí · 🔴 Tálamo no · bus a un tercio |
| **R6** Memoria/Skills | inteligencia | 🟡 skills sí · 🔴 NO-GO no · 3 de 6 frenos neutros |
| **R7** Frontend | interfaz | 🔴 Output Gate no · Auth/RBAC no |
| **R8** Observabilidad | visibilidad | 🔴 **cero Prometheus** |
| **R9** Seguridad | perímetro | 🔴 **la Amígdala NO EXISTE** |
| **R10** CI/CD | entrega | 🟡 4 workflows contra 7 stages |

⭐⭐⭐ **La fidelidad decae monotónicamente. Y no es negligencia: es ORDEN DE CONSTRUCCIÓN.**

El Plan Maestro define **6 fases foundation-first**:

```
FASE 0 Setup+CI  →  FASE 1 MVP cerebral  →  FASE 2 Coordinación
FASE 3 Autonomía →  FASE 4 Interfaz/obs  →  FASE 5 Seguridad/deploy
```

⭐ **R7, R8 y R9 faltan porque son Fases 4-5 y POR PLAN van al final.**

### 11.3 · ⭐⭐⭐ Y el sistema YA declaró la divergencia — en junio

**Grafo Maestro §0, añadido el 2026-06-10, dos meses antes de esta auditoría:**

> *"**Regla de precedencia: donde una tecnología nombrada abajo difiera de lo lockeado en una
> ronda, MANDA LA RONDA.** Este documento conserva la autoridad CONCEPTUAL; la autoridad TÉCNICA
> vive en las rondas."*

**§0.1 lista 8 cambios uno por uno:** Neo4j→**Apache AGE** · Qdrant→**pgvector** ·
Kafka→**Valkey+Arq** · LangGraph→**asyncio custom** · SQLAlchemy→**asyncpg directo**.

**§0.2 declara 3 desviaciones estructurales:** monolito modular (no microservicios) ·
**Pilar 3 v1 = solo la capacidad generativa #1** · sin ORM.

**§0.3 resolvió el "11/11" antes que yo:**

> *"Los 11 nodos **EXISTEN en v1 (ancho completo del grafo), pero a una profundidad ≈40%**…
> **11/11 = ancho · ~40% = profundidad v1.**"*

### 11.4 · ⭐⭐⭐ Entonces ¿por qué nadie vio el hueco?

**Existe una auditoría de alineación del 2026-06-09 que da 9.2/10 y declara "11/11 nodos
CERRADOS". Es seria: 872 líneas, metodología declarada, ronda por ronda.**

**Y la causa está en su propia §2.1:**

> *"Cada documento maestro de ronda se evaluó contra: **Grafo Maestro**… y **Visión**…"*

⭐⭐⭐ **Comparó DOCUMENTOS contra DOCUMENTOS. El código nunca entró.**

```
VISIÓN ──✅──> GRAFO ──✅ 9.2/10──> LAS 10 RONDAS ──🔴 sin medir──> EL CÓDIGO
                                    ↑                              ↑
                          aquí llegó la auditoría         aquí nadie miró
```

### 11.5 · Y el documento que predijo todo esto — en mayo

`Arquitectura_Grafo_vs_Loop` §13 propuso **3 capas de construcción**:

| Capa | Qué entrega | Condición para subir |
|---|---|---|
| **1 · MVP** | loop + memoria en grafo · multi-salto | — |
| **2 · v1** | LangGraph · paralelismo · multi-agente | ⭐ *"**después de 1-2 pilots cerrados**"* |
| **3 · v2** | ToT · Reflexion · **DMN** · **microglía** | — |

📊 **Pilots cerrados: 0.**

⭐⭐⭐ **For3s OS está exactamente donde la Capa 1 predijo, con partes de la 3 adelantadas.
No se quedó corto: se detuvo donde su propio diseño decía que debía detenerse hasta tener un
piloto. Lo que faltó fue DECLARARLO.**

### 11.6 · 🔴 Tres tableros de progreso, los tres congelados

| Tablero | Publica | Realidad |
|---|---|---|
| `bridges/000_PLAN_MAESTRO_TICKETS` | **5 / 18 peldaños** | |
| `Mapa_Construccion_Incremental` | **3 / 18** | **13 de 16 hitos** |
| Grafo Maestro | **11/11 nodos** | **9 de 11 con archivo** |

⭐ **Ninguno mintió al escribirse. Los tres se quedaron quietos mientras el sistema avanzaba dos
meses.**

⛔ **Conclusión operativa: ningún tablero sirve como fuente de estado. La única fuente fiable es
medir el servidor.**

---

## 12 · 📋 LOS 24 HALLAZGOS — y por qué solo 4 importan hoy

### 12.1 · El catálogo completo

**🔴 CRÍTICOS (5)**

| # | Hallazgo | Evidencia | § |
|---|---|---|---|
| **H-01** | **Contenido de conversaciones EN CLARO** | 15 MB legibles · `crypto.py` no lo toca · contradice R2 B1 §1.6 y la anti-visión #9 | 9.2 |
| **H-02** | **El contador de recuperación no cuenta lo importado** | `tocar_recuerdos` filtra por `session_id`; la búsqueda no | 6.3 |
| **H-03** | **Instancia huérfana** | 2,782 memorias · 933 MB · `TELEGRAM_BOT_TOKEN=# migr…` | 2.6 |
| **H-04** | **Digest de insights muerto 29 días** | worker apagado 8h/día; `digest_valor` a las 14:00 UTC | 7.4 |
| **H-05** | **ID de Telegram hardcodeado** | `_TG_BRIAN = 1923367928` en 2 archivos, **8+ usos**, sin salida por ENV | 12.3 |

**🟠 GRAVES (9)**

| # | Hallazgo | § |
|---|---|---|
| **H-06** | 3 tareas del DMN con 0 corridas de 114 — **son stubs declarados** | 7.2 |
| **H-07** | 9 de 15 insights nunca entregados | 6.7 |
| **H-08** | `MessageBus` existe y nadie lo usa — **y está a 1/3 de su diseño** | 8.1 |
| **H-09** | **36 de 76 módulos con CERO líneas ejecutadas** | 2.4 |
| **H-10** | 28 de 75 módulos sin mención en tests | 2.4 |
| **H-11** | **p90 = 18× el p50** | 10.1 |
| **H-12** | El camino del agente no mide su tiempo | 10.4 |
| **H-13** | Perfil de Brian dice `rol: jazz` | 6.6 |
| **H-14** | 18 tablas vacías = 18 capacidades apagadas | 6.5 |

**🟡 MEDIOS (10)**

| # | Hallazgo |
|---|---|
| **H-15** | `telegram_channel.py` 4,570 líneas — **creció 36% tras declararse deuda** |
| **H-16** | El agente son 90 líneas y su canal 4,570 |
| **H-17** | Grafo de dependencias invisible (imports perezosos) |
| **H-18** | Tres convenciones de fecha: `creado_at` · `created_at` · `ts` |
| **H-19** | Servicio `admin` solo en una instancia |
| **H-20** | `NetworkError` de Telegram cada ~4 min |
| **H-21** | 27 líneas de log en 24h |
| **H-22** | `embedding_precompute` tarda 62 s de media |
| **H-23** | 3 skills nunca usadas · último uso global 26-jul |
| **H-24** | Un solo `workspace_id` (`default`) |

### 12.2 · ⭐⭐ Con la vara correcta, solo 4 importan hoy

**La vara no es el Grafo ni el código: es el GATE DE LA FASE EN CURSO.**

| Vara | Veredicto | ¿Útil? |
|---|---|---|
| El Grafo completo (Fase 5) | 15/15 tablas ausentes | 🔴 declara en rojo un sistema que funciona |
| El código como autoridad | todo verde | 🔴 no mide nada |
| ⭐ **El gate de la fase en curso** | **6 de 6** | ✅ **discrimina y es accionable** |

| Hallazgo | Por qué importa HOY | Bloque de la campaña |
|---|---|---|
| 🔴🔴 **H-01** contenido en claro | viola una anti-visión **no-negociable** · **empeora cada día** | **1 · `seguridad`** |
| 🟠 **H-02** contador asimétrico | el sistema **podría borrar lo que sí usa** | **2 · `memoria`** |
| 🔴 **H-04** digest muerto | Fase 3, en curso | **3 · `cerebro`** |
| 🔴 **H-03** instancia huérfana | operación · consume 933 MB | **4 · `despliegue`** |

⭐⭐⭐ **Los 4 caen exactamente en los 4 primeros bloques que Brian priorizó por instinto.**

**Los otros 20 no son falsos — son PREMATUROS.** Output Gate · RBAC · Prometheus · Amígdala ·
Event Sourcing · schema-per-tenant son **Fases 4-5**, no deuda de hoy.

⚠️ **Y eso es más peligroso que ser falsos: un hallazgo prematuro se ve idéntico a uno urgente.**

### 12.3 · 🔴 H-05 con detalle — la vara del público

```
entrenamiento_backlog.py:27   _TG_BRIAN = 1923367928
entrenamiento_olas.py:36      _TG_BRIAN = 1923367928
```

**Usado 8+ veces** como `telegram_user_id` (líneas 126, 239, 270, 394, 548, 614 de
`entrenamiento_backlog`; 180, 195 de `entrenamiento_olas`).

**Comparación que muestra el criterio correcto:**

```python
config.py:42   owner_session: str = "brian"                              # default
config.py:71   os.environ.get("FOR3S_OWNER_SESSION", "brian").strip()    # ✅ salida por ENV
```

⭐ **`config.py` sí tiene salida. `_TG_BRIAN` no tiene ninguna.**

⭐⭐ **Y el mismo defecto existe en Mente OS** (pendiente V2-8: *"un clon ajeno hereda el nombre de
Brian en sus reglas de proyecto"*). **Los dos sistemas tienen la misma enfermedad.**

---

## 13 · ✅ LO QUE ESTÁ BIEN — 14 fortalezas que no se tocan

**Un catálogo de hallazgos sin esta sección lee como si todo estuviera mal. No lo está.**

| # | Fortaleza | Evidencia |
|---|---|---|
| **B-01** | **Secretos cifrados de verdad** | `nonce` + `ciphertext`, sin columna en claro |
| **B-02** | **Cadena de auditoría íntegra** | **12,908 eventos**, todos con `hash_self` y `hash_prev` · **2 triggers** |
| **B-03** | **Aislamiento físico entre instancias** | volúmenes `pgdata` separados |
| **B-04** | **Aislamiento por sesión en las consultas** | verificado leyendo las 4 sospechosas |
| **B-05** | **Consolidación al grafo al 91.3%** | 30,959 de 33,908 |
| **B-06** | **Documentación y tipado al 100%** | 76/76 |
| **B-07** | **Los dos canales de usuario convergen** | declarado en el docstring de `api_channel` |
| **B-08** | ⭐ **La microglía funciona** | **41% podado**, con audit de cada olvido |
| **B-09** | **El canal que se vende SÍ está medido** | `api_metering` con p50/p95/max |
| **B-10** | **Backpressure bien diseñado** | el `MessageBus` avisa en vez de reventar la RAM |
| **B-11** | **El perfil capturó reglas reales** | *"Avisar SIEMPRE antes de operaciones de BD"* |
| **B-12** | **Sin código muerto en el núcleo** | los 5 sin importadores son entrypoints verificados |
| **B-13** | **Las 47 migraciones aplicadas y versionadas** | tabla `schema_version` completa |
| **B-14** | **`crypto.py` bien implementado** | derivación por workspace, nonce por mensaje |

### 13.1 · Y tres que merecen decirse aparte

1. ⭐⭐⭐ **La microglía superó al estado del arte** que su propio diseño describía (§5.1).
2. ⭐⭐ **El aislamiento multi-tenant se logró con OTRA forma** — contenedor + BD por instancia en
   vez de schema-per-tenant. **Es MÁS aislado que lo diseñado, no menos.**
3. ⭐⭐ **La disciplina del import:** 11,664 de 11,664 archivos con veredicto, 0 pendientes, y 19
   secretos detectados y desviados al vault.

---

## 14 · ⚠️ MIS 8 ERRORES EN ESTA AUDITORÍA — corregidos

**Una auditoría que no declara sus errores no es una auditoría: es una opinión larga.**

| # | Lo que afirmé | Lo que era | Cómo se detectó |
|---|---|---|---|
| **E-1** | *"76 archivos"* como total del sistema | son 76 **del núcleo**; hay **112 `.py` + 48 `.sql`** | contar sin filtrar por carpeta |
| **E-2** | *"43 módulos huérfanos"* | **5**, y 4 son entrypoints | el regex no leía `from for3s_core import a, b, c` ni imports perezosos |
| **E-3** | *"`entrenamiento_repo` es código muerto"* | tiene `__main__` en la línea 403 | buscar `__main__` antes de afirmar |
| **E-4** | *"36 consultas sin filtro de dueño"* | **ninguna** — el `WHERE` está en la línea siguiente | leer el contexto, no una línea |
| **E-5** | *"el servidor está caído"* | llevaba **8h48m encendido**; no leí `secrets/` | Brian lo corrigió |
| **E-6** | *"3 tareas del DMN son un fallo silencioso"* | **son stubs declarados en el código** | leer la cabecera del módulo |
| **E-7** | 🔴 *"la memoria está INALCANZABLE"* | **falso** — `incluir_import` cruza sesiones desde julio | **ejecutar `recordar()` en vivo** |
| **E-8** | *"un proceso OpenCode no declarado corriendo"* | el `pgrep` **se detectaba a sí mismo** | verificar con `ps aux` **antes** de escribir |

⭐⭐ **El patrón de E-1 a E-4 y E-7: medir una parte y hablar del todo, o inferir del esquema en
vez de ejecutar el código.**

⭐ **E-8 es el único donde la segunda medición ocurrió ANTES del hallazgo, no después.** Esa es la
diferencia entre un método que funciona y uno que no.

---

## 15 · LAS 34 LECCIONES

### 15.1 · Las que ya causaron daño real

| # | Lección | De dónde salió |
|---|---|---|
| **L-01** | Una regla en código se cumple 100%; en documento, 40-60% | la ley del proyecto |
| **L-02** | Un check debe **verse fallar** antes de que su verde valga | `val-functional` §2.2 |
| **L-03** | La sesión muere de **EDAD**, no de peso | R1 (96h) · R2 (76h) · R3 (11 días) |
| **L-04** | **Registrar el cierre NO es cerrar** | S11 siguió viva 46h y llegó a 1,000,030 tokens |
| **L-05** | **Verificar FUERA del árbol del autor** | 195/0 aquí, **22 fallos en un clon** |
| **L-06** | Una explicación cómoda para un rojo es cómo un bug sobrevive | meses tapando 4 defectos del motor |
| **L-07** | Un límite no verificado es una suposición disfrazada | "bloqueado" resuelto en 1 hora |
| **L-08** | ⛔ **Nunca inventar criterio: preguntar** | ADR-003 · ADR-014 |

### 15.2 · Las de método

| # | Lección |
|---|---|
| **L-09** | Antes de AÑADIR una regla, busca la que **CAUSA** el bug |
| **L-10** | **Presencia ≠ uso** — que exista no es que se llame |
| **L-11** | Un validador lee la **CELDA**, no la intención |
| **L-12** | El archivo que se lee **PRIMERO** era el menos vigilado |
| **L-13** | Un **puntero en su sitio** vence a un borrado |
| **L-14** | Mover archivos puede **ESCONDER** el defecto |
| **L-15** | Medir una parte y hablar del todo |
| **L-16** | Dos formas de decir lo mismo son **dos reglas** |
| **L-17** | Un **default** nunca apunta a algo con dueño |
| **L-18** | Rota el **ARCHIVO**, no el pendiente |
| **L-19** | Un **squash merge** borra trabajo ya empujado |
| **L-20** | Una contraseña en un ejemplo de mala práctica **sigue siendo una contraseña** |

### 15.3 · Las que salieron de esta auditoría

| # | Lección |
|---|---|
| **L-21** | Antes de construir un pendiente viejo, **medir si ya está hecho** |
| **L-22** | Un hito que declara "completo" debe decir **COMPLETO EN QUÉ**: diseñado, construido o verificado |
| **L-23** | Diseñar diez capas de golpe produce **un mapa preciso de un territorio que aún no existe** |
| **L-24** | ⭐ Una cadena de coherencia se rompe **en el eslabón que nadie mide** |
| **L-25** | Antes de reportar un hallazgo, **buscar si el sistema ya lo documentó** |
| **L-26** | ⭐ Un sistema por fases se audita contra el gate de **SU fase**, nunca contra el destino |
| **L-27** | Un dato que ninguna consulta alcanza es **indistinguible de uno que no existe** |
| **L-28** | Un tablero que no se actualiza **miente a la baja** |
| **L-29** | Un sistema con **tres tableros tiene cero tableros** |
| **L-30** | Una herramienta usada solo sobre sí misma **no está probada: está calibrada** |
| **L-31** | Una migración fiel al origen puede **romper el destino** |
| **L-32** | ⭐ Un esquema describe lo que se **PUEDE** consultar, no lo que el código consulta |
| **L-33** | ⭐ Cuando una función **LEE** con un criterio y otra **ESCRIBE** con otro, el sistema funciona y miente a la vez |
| **L-34** | Un modelo de referencia bien elegido **predice los síntomas de sus propias ausencias** |

---

## 16 · LO QUE SIGUE SIN MEDIR

**Declarado, no escondido.**

| Hueco | Por qué importa | Cómo se mediría |
|---|---|---|
| **La vara "solo Brian sabe usarlo"** | 1 de las 4 pruebas del público, sin auditar | revisar los comandos de `telegram_channel` y ver cuáles se autodocumentan |
| **Qué código corre en PRODUCCIÓN** | `.coverage` es de tests del 16-jul, no del sistema vivo | instrumentar el agente |
| **Los 24 edges del Grafo** | la fase 3 los recorrerá | trazar cada edge con datos reales |
| **Por qué `trigger_ok=false` siempre** | en las 3 tareas del DMN | leer la condición de disparo de cada una |
| **Si `general` y la 3ª instancia tienen los mismos fallos** | se auditó `brian` a fondo | repetir §6-§10 sobre ellas |
| **El rendimiento bajo carga** | todo lo medido es con 1 usuario | prueba de carga |
| **Si la clave Zen se rotó** | marcada hace 2 meses | preguntar a Brian |

---

## 17 · CÓMO SE RE-MIDE TODO ESTO

⚠️ **Cada número lleva fecha. El sistema sigue corriendo: `dmn_corridas` y `cron_corridas` crecen
cada noche.**

**El acceso:** `bin/conectar-servidor` — lee `secrets/Conectar_Servidor_For3s.md` y entra.

```bash
# El estado de la instancia
Mente/bin/conectar-servidor 'docker exec for3s-brian-postgres-1 psql -U for3s -d for3s \
  -c "SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC"'

# El gate de Fase 1
Mente/bin/conectar-servidor 'docker exec for3s-brian-postgres-1 psql -U for3s -d for3s \
  -c "SELECT count(*) FILTER (WHERE consolidated_to_kg) consolidados,
             count(*) FILTER (WHERE deleted_at IS NOT NULL) podados,
             count(*) FILTER (WHERE veces_recuperado>0) recuperados
      FROM episodes_events"'

# Los nodos con archivo
Mente/bin/conectar-servidor 'cd ~/for3s-os/packages/for3s-core/src/for3s_core && \
  ls kg.py memory.py conversation.py skills.py microglia.py dmn.py confidence.py \
     consolidator.py relevance.py amigdala.py talamo.py 2>&1'
```

⭐ **Regla de esta auditoría, y debería ser la de la campaña: un número sin comando que lo
produzca no entra.**

---

Related: `campaigns/producto-for3s-os/CAMPAIGN.md` (la campaña que usa este documento) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` (el terreno del código, con las 35 pasadas) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-MENTE-OS-CONOCIMIENTO.md` (el terreno del conocimiento, 33 secciones) ·
`Cerebro/For3s_OS_Grafo_Maestro.md` §0 (la autoridad conceptual, con su declaración de divergencia) ·
`memory/archive/Plan_Maestro_Programacion.md` (las 6 fases y sus gates) ·
`memory/archive/Mapa_Construccion_Incremental.md` (los 16 hitos) ·
`bin/conectar-servidor` (cómo re-medir todo esto).
