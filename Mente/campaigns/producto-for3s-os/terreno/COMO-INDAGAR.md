# CÓMO INDAGAR — la guía de arranque de la campaña

**Status:** current · **Type:** analysis · **Updated:** 2026-08-12 · **Owner:** brian
**Level:** 🧭 **LA PUERTA DEL TERRENO** — qué leer, en qué orden, y cómo verificar antes de afirmar
**Verified by:** `bin/check-campaigns` · `bin/test-f0-f6` (check 30)
**Exempt:** size, split-signal · ⭐ **Orden de Brian 2026-08-12:** *"actualiza la información que
tenemos para la campaña de tal manera que sepa todo el contexto desde ahora hasta que se inició
todo y sepa cómo indagar"*. Partirlo rompería su función: es **el mapa de entrada completo**.

## Purpose

**Un bloque de esta campaña arranca en frío y necesita tres cosas: saber qué pasó, saber contra
qué se juzga, y saber cómo medir sin inventar.** Este documento las da en ese orden.

⛔ **No decide nada.** El CAMPAIGN ordena, el plan de las 3 fases define el método, y el
terreno mide. **Esto solo enseña a leerlos.**

---

## 📑 ÍNDICE

| § | Qué responde |
|---|---|
| **1** | 🕐 **LA LÍNEA DE TIEMPO** — de mayo 2026 a hoy, en 6 etapas |
| **2** | 🧭 **QUÉ LEER Y EN QUÉ ORDEN** — la ruta mínima y la completa |
| **3** | ⚖️ **LAS 5 AUTORIDADES** — quién manda sobre qué |
| **4** | 🔬 **CÓMO INDAGAR** — las 7 técnicas que esta auditoría usó |
| **5** | ⛔ **LOS 8 ERRORES YA COMETIDOS** — para no repetirlos |
| **6** | 📊 **LOS NÚMEROS VIVOS** — cuáles caducan y cómo re-medirlos |
| **7** | 🚦 **ANTES DE ABRIR UN BLOQUE** — la lista de arranque |

---

## 1 · 🕐 LA LÍNEA DE TIEMPO — de dónde viene todo

**Seis etapas, cada una con su fecha medida y lo que dejó.**

### 1.1 · Mayo 2026 — el origen, antes de que hubiera nada

**3 documentos de Brian** (`memory/archive/Banco_Diario_Mayo_2026.md`): `FOR3S-STACK-DEFINED` ·
`FOR3S-SERVER-ARCHITECTURE` · `FOR3S-RECURSOS-ACTUALES`.

| Lo que declaraban | Qué pasó después |
|---|---|
| **Node.js + TypeScript** como backend | 🔴 **revertido** a Python 3.12 (R1, 30-may) |
| **OpenClaw como motor de agentes** | 🔴 **revertido** — se construyó motor propio |
| Ubuntu 26.04 · Docker · Tailscale · PG16 | ✅ **siguen hoy** |
| 3 agentes: Personal, Empleado, Design | ⭐ **absorbidos** — sus memorias viven en `brian` |
| **Inmortalidad** y **Herencia** (conceptos de Brian) | ⭐ **el Grafo Maestro los absorbió** |

⚠️ **Y ya entonces el propio material detectó 4 contradicciones internas** (`§5.3` del Banco):
Auth asumida vs pendiente · ubicación de agentes en *"CONFLICTO REAL"* · memoria con 3 estados ·
capacidad 10 vs 20-30 agentes. ⭐ **La disciplina de cruzar documentos existe en este repo desde
mayo. Lo que no existía era cruzarlos contra el CÓDIGO.**

### 1.2 · 30-may → 9-jun · las 10 rondas de diseño — **10 días**

**65 archivos · 32,377 líneas · 40 decisiones LOCKED (D-001 a D-040) · 11 nodos · 24 edges ·
3 pilares.** Coste proyectado: **$97-137/mes** para multi-tenant con SOC2.

⭐ **El diseño de For3s OS no es vago: es exhaustivo.** Cada ronda tiene pre-preguntas,
candidatos evaluados, filtro por las 3 anclas, decisión LOCKED, implicaciones y riesgos numerados.

🔴 **Y dejó dos banderas que Brian exigió y nunca se cerraron:**

> *"El diseño (R1-R10) está completo. **ANTES de escribir código, instrucciones LOCKED de Brian
> exigen DOS revisiones.**"*

| Bandera | Palabras de Brian | Estado |
|---|---|---|
| **RE-REVISIÓN R6** | *"VOLVER A REVISAR Y PLANIFICAR CUANDO ESTEMOS REALIZANDO CODIGO TODO EL R6 POR QUE ES UN R EXTREMANDAMENTE IMPORTANTE"* | 🔴 nunca se hizo |
| **DMN 5.4.2** | replanificación profunda de las 8 tareas | 🔴 nunca se hizo |

**Se arrastraron como `carry-forward` por SEIS rondas. Se programó igual.**

### 1.3 · 9-10 jun · las auditorías de coherencia y los planes

| Documento | Qué dejó |
|---|---|
| `docs/analysis/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md` | veredicto **9.2/10** · *"11/11 nodos CERRADOS"* |
| `docs/analysis/Reporte_Maestro_Consolidado_R1-R10.md` | el stack unificado + **9 refuerzos pre-código** |
| `memory/archive/Plan_Maestro_Programacion.md` | ⭐ **las 6 fases con su GATE** |
| `memory/archive/Estimacion_Tiempo_Por_Subtema.md` | **~9-10 meses** el sistema · **~3-3.5 meses** el MVP |
| Grafo Maestro **§0** (añadido el 10-jun) | ⭐ **declara la divergencia diseño↔código** |

⭐⭐ **El Grafo §0 es la pieza que más ahorra tiempo a un bloque nuevo.** Declara: *"donde una
tecnología difiera de lo lockeado en una ronda, **MANDA LA RONDA**"*, lista **8 cambios
tecnológicos** uno por uno, y resuelve el "11/11" así: ***"11/11 = ancho · ~40% = profundidad v1"***.

### 1.4 · 10-jun → 11-jun · arranca el código, y el sistema de tickets

`bridges/000_PLAN_MAESTRO_TICKETS.md` declara **las 3 brújulas en orden de autoridad** y abre
`C0` · `C1` · `H1` · `H2` · `H3`.

🔴 **Y ahí se detuvo.** El sistema de tickets publica **`5/18 peldaños`** desde el 11-jun. **Medido
hoy: 13 de 16 hitos construidos.** El trabajo migró a los bloques de Mente OS v2 en julio y
**nadie cerró el sistema anterior**.

### 1.5 · 5-jul · el entrenamiento — 33,737 memorias entran de golpe

**Los 6 agentes OpenClaw** (watchdog 20,749 turnos · dev 17,096 · main 6,045 · empleado ·
cipher · helix) se importan a la instancia `brian`.

📊 **Disciplina medida: `11,664 / 11,664` archivos decididos, 0 pendientes.** Cada uno con
veredicto (importado · duplicado · descartado · secreto). **19 secretos al vault, no a la memoria.**

⭐ **Y un hallazgo que redujo el trabajo a la mitad:** *"6,600 de los 11,664 archivos son
duplicados exactos (sha256)"*. **Se midió antes de importar.**

### 1.6 · 11-ago → 12-ago · las 50 auditorías y esta campaña

**35 pasadas contra For3s OS** (componentes · uso real · comportamiento) + **la lectura de
~45,000 líneas de Mente OS**. Producen los 3 documentos de `terreno/` y **la vara de la campaña**.

---

## 2 · 🧭 QUÉ LEER Y EN QUÉ ORDEN

### 2.1 · ⚡ La ruta MÍNIMA — 20 minutos, y basta para abrir un bloque

| # | Documento | Qué te da |
|---|---|---|
| **1** | `campaigns/producto-for3s-os/CAMPAIGN.md` | la misión, los 12 bloques, la vara, dónde se trabaja |
| **2** | 📕 `campaigns/producto-for3s-os/terreno/LA-VERDAD-DE-V1.md` **§0** | **el veredicto en una página** |
| **3** | `docs/plans/PLAN-3-fases.md` | el método: qué mira cada fase, qué entrega un bloque, qué detiene |
| **4** | este documento **§4 y §7** | cómo medir · la lista antes de abrir |

⭐ **Con esos cuatro, un bloque arranca sin preguntar nada.**

### 2.2 · La ruta COMPLETA — por si el bloque toca algo delicado

| Si vas a tocar… | Lee… |
|---|---|
| **cualquier nodo del Grafo** | `campaigns/producto-for3s-os/terreno/AUDITORIA-MENTE-OS-CONOCIMIENTO.md` **§19** — el mapa nodo→archivo REAL |
| **la memoria** | ese mismo, **§24 · §29 · §30** — el arco completo de H-02, con dos errores míos corregidos |
| **seguridad** | `campaigns/producto-for3s-os/terreno/LA-VERDAD-DE-V1.md` **§9** · y **§32** de la memoria (el diagnóstico diferencial) |
| **una decisión de diseño** | `Cerebro/For3s_OS_Grafo_Maestro.md` **§0** primero, luego la ronda que la lockeó |
| **algo que "falta"** | `rules/rule-product-authority.md` **§2.4** — puede ser Fase 4-5, no deuda |
| **un archivo >400 líneas** | `campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` **§16** — y ⛔ **preguntar a Brian** |

---

## 3 · ⚖️ LAS 5 AUTORIDADES — quién manda sobre qué

⭐ **Cinco preguntas distintas, cinco documentos distintos. Confundirlas es el error más caro.**

| Pregunta | Autoridad | Dónde |
|---|---|---|
| **¿QUÉ debe existir y por qué?** | el Grafo Maestro (con su §0) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| **¿CON QUÉ se construye?** | las 10 rondas — **el Grafo cede aquí** | `work/Ronda_*` |
| ⭐ **¿QUÉ SE EXIGE HOY?** | el Plan Maestro — **6 fases con gate** | `memory/archive/Plan_Maestro_Programacion.md` |
| ⭐ **¿EN QUÉ ORDEN se ensambla?** | el Mapa de Construcción — H1..H16 | `memory/archive/Mapa_Construccion_Incremental.md` |
| **¿CÓMO se recorre esta campaña?** | el plan de las 3 fases | `docs/plans/PLAN-3-fases.md` |

⛔ **Y el código NO es autoridad: es lo que se AUDITA** (`rules/rule-product-authority.md` §1 #5).

### 3.1 · ⭐⭐ La vara temporal, en una frase

> **Un sistema en construcción por fases se audita contra el gate de SU fase, nunca contra el
> destino final.**

📊 **Medido el 12-ago, con las tres varas:**

| Vara | Veredicto | ¿Sirve? |
|---|---|---|
| El Grafo **completo** (Fase 5) | 15/15 tablas ausentes · **24 hallazgos** | 🔴 declara en rojo un sistema que corre a diario |
| El código como autoridad | todo verde | 🔴 no mide nada |
| ⭐ **El gate de la fase en curso** | **6 de 6** · **4 hallazgos** | ✅ **discrimina y es accionable** |

⚠️ **Los otros 20 no eran falsos: eran PREMATUROS.** Y eso es peor — **un hallazgo prematuro se
ve idéntico a uno urgente**, y entierra a los que sí importan.

---

## 4 · 🔬 CÓMO INDAGAR — las 7 técnicas que esta auditoría usó

**No son consejos: son los métodos que produjeron los hallazgos que sobrevivieron.**

### 4.1 · Ejecutar, no inferir del esquema

⛔ **El error más caro de esta auditoría** (§29 de la memoria): leí el filtro documentado de
`buscar_semantico` y concluí *"la memoria está inalcanzable"*. **Datos correctos, conclusión falsa.**

```bash
# ❌ MAL: leer el esquema y deducir
grep "WHERE session_id" memory.py

# ✅ BIEN: ejecutar la función y ver qué devuelve
Mente/bin/conectar-servidor 'docker exec for3s-brian-agent-1 python3 -c "
import asyncio,os,asyncpg
from for3s_core.memoria import Memoria
async def m():
    p=await asyncpg.create_pool(os.environ[\"DATABASE_URL\"])
    print(len(await Memoria(p).recordar(\"tg:1923367928\",\"tu pregunta\",history=[])))
asyncio.run(m())"'
```

> **L-32 · Un esquema describe lo que se PUEDE consultar, no lo que el código consulta.**

### 4.2 · Cruzar el camino de LECTURA con el de ESCRITURA

⭐ **Así se encontró el defecto real de H-02** (§30): `buscar_semantico` cruza sesiones
(`incluir_import`), pero `tocar_recuerdos` filtra por `session_id`. **Un recuerdo se recupera y
nunca se marca.**

> **L-33 · Cuando una función LEE con un criterio y otra ESCRIBE con otro, el sistema funciona y
> miente a la vez.** Solo aparece leyendo las dos juntas.

### 4.3 · Medir en la BD viva, nunca en el clon

```bash
Mente/bin/conectar-servidor 'docker exec for3s-brian-postgres-1 psql -U for3s -d for3s \
  -c "SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 15"'
```

⚠️ **El clon local está 18 días desfasado** (medido 10-ago). `rule-product-authority` §6 lo prohíbe.

### 4.4 · Buscar si el sistema ya lo documentó

⭐ **Cuatro de mis "hallazgos" ya estaban resueltos por escrito** en el Grafo §0 (§21 de la
memoria). El sistema anticipó mi confusión exacta y la resolvió el 10-jun.

```bash
grep -rn "<el tema>" Mente/Cerebro/For3s_OS_Grafo_Maestro.md Mente/rules/ Mente/memory/archive/
```

> **L-25 · Un "descubrimiento" que ya está escrito no es un hallazgo: es una lectura incompleta.**

### 4.5 · Confirmar por 2+ métodos independientes

⭐ **La Amígdala y el Tálamo ausentes los encontraron CINCO métodos distintos** (tablas de BD ·
mapa nodo→archivo · escalera de hitos · las 7 ventajas · el diagnóstico neurocientífico).
**Eso convierte un hallazgo en evidencia.**

### 4.6 · Verificar antes de escribir, no después

🔬 **Ejemplo real (§31):** mi `pgrep -f "opencode serve"` dio positivo e iba a reportar *"un
proceso no declarado corriendo"*. **Lo verifiqué con `ps aux` primero: el `pgrep` se detectaba a
sí mismo.**

### 4.7 · Cada número lleva su comando

⛔ **Un número sin el comando que lo produce no entra.** Es la regla de esta auditoría y debería
ser la de cada bloque (`rules/rule-checks-must-measure.md`).

---

## 5 · ⛔ LOS 8 ERRORES YA COMETIDOS — no repetirlos

**Están en `campaigns/producto-for3s-os/terreno/LA-VERDAD-DE-V1.md` §14. Resumidos aquí porque son la trampa más probable:**

| # | Lo que se afirmó | Lo que era | La lección |
|---|---|---|---|
| **E-1** | *"76 archivos"* como total | son 76 **del núcleo**; hay **112 `.py`** | contar sin filtrar por carpeta |
| **E-2** | *"43 módulos huérfanos"* | **5**, y 4 son entrypoints | el regex no leía imports perezosos |
| **E-3** | *"`entrenamiento_repo` es código muerto"* | tiene `__main__` en la línea 403 | buscar `__main__` antes de afirmar |
| **E-4** | *"36 consultas sin filtro de dueño"* | **ninguna** — el `WHERE` está en la línea siguiente | leer el contexto, no una línea |
| **E-5** | *"el servidor está caído"* | llevaba **8h48m encendido** | no leí `secrets/` |
| **E-6** | *"3 tareas del DMN son un fallo"* | **son stubs declarados en el código** | leer la cabecera del módulo |
| 🔴 **E-7** | *"la memoria está INALCANZABLE"* | **falso** — `incluir_import` cruza sesiones | **ejecutar la función** |
| **E-8** | *"un proceso no declarado corriendo"* | el `pgrep` se detectaba a sí mismo | verificar **antes** de escribir |

⭐ **El patrón de E-1 a E-4 y E-7: medir una parte y hablar del todo, o inferir del esquema en vez
de ejecutar el código.**

---

## 6 · 📊 LOS NÚMEROS VIVOS — cuáles caducan

⚠️ **Las lecciones no caducan. Los números sí.** El sistema corre cada noche: `dmn_corridas` y
`cron_corridas` crecen, la microglía poda, el CLS consolida.

| Número | Valor al 2026-08-12 | Cómo re-medirlo |
|---|---|---|
| Episodios | 33,908 | `SELECT count(*) FROM episodes_events` |
| Consolidados al grafo | 30,959 (91.3%) | `… FILTER (WHERE consolidated_to_kg)` |
| Podados | 13,974 (41%) | `… FILTER (WHERE deleted_at IS NOT NULL)` |
| Candidatos a poda | **4,230** | `… WHERE relevance < 0.3` |
| Eventos de auditoría | 12,908 | `SELECT count(*) FROM audit_events` |
| Corridas DMN | 3,295 | `SELECT count(*) FROM dmn_corridas` |
| Contenedores | 28 | `docker ps -q \| wc -l` |
| Batería de Mente OS | ver `docs/METRICS.md` | ⛔ **nunca copiar el número** |

⭐ **Y los que NO cambian:** los 40 LOCKED de las rondas · los 30 ADRs · las 34 lecciones · las
3 leyes de construcción · el gate de cada fase.

---

## 7 · 🚦 ANTES DE ABRIR UN BLOQUE — la lista

**Siete comprobaciones. Ninguna cuesta más de un minuto.**

| | Comprobación | Por qué |
|---|---|---|
| **1** | ¿Leí el `campaigns/producto-for3s-os/CAMPAIGN.md` y sé **en qué fase** está For3s OS? | sin la fase, se audita contra el destino (§3.1) |
| **2** | ¿Sé **qué archivos** toca mi bloque, y que **ningún otro los reclama**? | dos bloques sobre el mismo archivo → el hook entrega los estándares equivocados |
| **3** | ¿Leí lo que el terreno **ya midió** sobre esas piezas? | evita re-descubrir · **L-25** |
| **4** | ¿Mi `campaign_phase` es `1`? | ⛔ saltar fase es 🔴 en `check-campaigns` |
| **5** | ¿Sé dónde dejar mi archivo de hallazgos? | `hallazgos/<bloque>-fase-<n>.md` — el nombre es la ruta |
| **6** | ¿Tengo claros los **5 criterios de 🔴 crítico**? | `docs/plans/PLAN-3-fases.md` §4 — uno detiene el bloque |
| **7** | ¿Mi bloque toca un archivo **>400 líneas**? | ⛔ **preguntar a Brian antes de cerrar la fase 2** |

### 7.1 · ⭐⭐ Y la que no está en ninguna lista

> **La campaña `producto-for3s-os` es la PRIMERA VEZ que Mente OS v2 gobierna trabajo de
> producto.** Sus 5 bloques archivados son el motor auditándose a sí mismo.

⚠️ **Precedente medido (L-05):** la batería daba **195/0 aquí y 22 fallos en un clon**. **Un
sistema que solo se ha probado sobre sí mismo falla al salir de sí mismo. Ya pasó una vez.**

⭐ **Por eso el `§K Closing` del primer bloque debería declarar DOS cosas:** qué se arregló de
For3s OS **y qué falló o funcionó del motor al gobernarlo.**

---

Related: `campaigns/producto-for3s-os/CAMPAIGN.md` (la misión y los 12 bloques) ·
`campaigns/producto-for3s-os/terreno/LA-VERDAD-DE-V1.md` (📕 qué es For3s OS, medido) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` (el terreno del código) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-MENTE-OS-CONOCIMIENTO.md` (el terreno del conocimiento, 33 §) ·
`docs/plans/PLAN-3-fases.md` (el método de las 3 miradas) ·
`rules/rule-product-authority.md` (las autoridades y la vara temporal) ·
`Cerebro/For3s_OS_Grafo_Maestro.md` §0 (la divergencia declarada) ·
`memory/archive/Plan_Maestro_Programacion.md` (las 6 fases y sus gates).
