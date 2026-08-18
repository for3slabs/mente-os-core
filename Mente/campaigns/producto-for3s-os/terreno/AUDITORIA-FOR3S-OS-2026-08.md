# AUDITORÍA DE FOR3S OS — el terreno medido antes de reconstruir

**Status:** current · **Type:** analysis · **Updated:** 2026-08-12 · **Owner:** brian
**Level:** 📚 REFERENCIA DE CAMPAÑA — la lee `campaigns/producto-for3s-os/`; no dicta reglas, aporta HECHOS
**Verified by:** cada número lleva su comando; se re-mide con `bin/conectar-servidor`
**Exempt:** size, split-signal · ⭐ **REFERENCIA DE TERRENO — decisión de Brian 2026-08-12:**
*"no importa el tamaño del MD, hazlo lo más grande y detallado posible… no omitas nada"*. Partirlo
rompería lo que lo hace útil: **un solo lugar donde está TODO lo que se sabe de For3s OS medido.**
La campaña entra aquí a resolver "¿qué sabemos de X?" — partirlo obligaría a buscar en 5 archivos
y a que cada uno declarara su propia autoridad sobre el mismo sistema.

## Purpose

Que la campaña **no entre a ciegas**. Todo lo que sigue está **medido en el servidor `for3s`**
entre el 11 y el 12 de agosto de 2026, sobre el código real y la base de datos real de la
instancia `brian`. Ningún número viene de un documento; cada uno viene de un comando.

> **Brian, 2026-08-12:** *"For3s OS funciona sí, pero no sé cómo es que se construyó. Hubo muchos
> procesos que están bien, algunos mal, algunos que no tengo idea."*

**Lo que este documento responde:** qué existe · qué se usa de verdad · qué está conectado ·
qué está roto · y **con qué evidencia se afirma cada cosa**.

**Lo que este documento NO hace:** decidir. No propone arreglos ni prioriza. La autoridad para
eso es `Cerebro/For3s_OS_Grafo_Maestro.md` (`rules/rule-product-authority.md`).

---

## 📑 ÍNDICE

| § | Qué entrega |
|---|---|
| **0** | Cómo se midió — y por qué se puede repetir |
| **1** | El inventario: qué existe, contado |
| **2** | La arquitectura real: quién depende de quién |
| **3** | Los 12 componentes, con su peso y sus piezas |
| **4** | El despliegue: 28 contenedores, 3 instancias |
| **5** | Los datos: qué guardó de Brian y qué hizo con ellos |
| **6** | El cerebro nocturno: trabaja mucho, hace poco |
| **7** | Los canales: qué está conectado y qué está aislado |
| **8** | Seguridad y privacidad: lo bueno y lo grave |
| **9** | Rendimiento y coste, medidos |
| **10** | La historia constructiva: 47 migraciones |
| **11** | La vara del público: qué falla para "miles de millones" |
| **12** | 📋 **Catálogo completo de hallazgos** — 24, con gravedad y evidencia |
| **13** | ⚠️ Errores que cometí midiendo, y cómo se corrigieron |
| **14** | Qué queda sin medir — declarado, no escondido |
| **15** | Cómo usa esto la campaña |
| **16** | ⛔ Los 18 archivos grandes — decisión APLAZADA con recordatorio |

---

## 0 · CÓMO SE MIDIÓ

**35 pasadas de auditoría** desde ángulos distintos, en tres tandas:

| Tanda | Pasadas | Eje |
|---|---|---|
| **A** | 15 | **¿Qué existe?** — archivos, dependencias, estructura |
| **B** | 20 | **¿Qué se usa?** — la BD real con los datos de Brian dentro |
| **C** | 15 | **¿Qué está conectado?** — canales, buses, concurrencia |
| **D** | 5 | **Cerrar huecos** — lo que las tandas anteriores dejaron abierto |

**El acceso:** `Mente/bin/conectar-servidor` — lee `secrets/Conectar_Servidor_For3s.md` y entra.
⭐ Ese script nació de un fallo de esta misma sesión: la IA intentó `ssh` desnudo, falló, y
**reportó el servidor como caído estando encendido**. El dato existía; el procedimiento no.
Ahora el procedimiento es código, y por eso cualquier número de aquí **se puede volver a medir**.

**Regla que se siguió:** un número sin comando que lo produzca no entra. Cuando algo no se pudo
verificar, se dice en §14 en lugar de omitirlo.

---

## 1 · EL INVENTARIO — qué existe, contado

### 1.1 · Las capas

| Capa | Cuánto | Dónde |
|---|---|---|
| **Núcleo** `for3s_core` | **76 archivos** · **26,939 líneas** | `packages/for3s-core/src/for3s_core/` |
| **Tests** | **28 archivos** | `tests/` |
| Fuera del núcleo | **8** | `scripts/` (3) · `docker/render` (2) · `docker/sandbox` (1) · SDK molde (1) · `src/for3s_os` (1) |
| **Migraciones SQL** | **47** | `for3s_core/migrations/` |
| Docker | **2** compose · **5** Dockerfiles · 4 shell | `docker/` |
| CI | **6** workflows | `.github/workflows/` |
| Documentación | **22** `.md` + un sitio web | raíz y `docs/` |
| **TOTAL medible** | **112 `.py` · 48 `.sql`** | |

⚠️ **Una corrección que importa para la campaña:** una auditoría anterior reportó *"76 archivos"*
como el total del sistema. Son 76 **del núcleo**. El sistema tiene 112 `.py` y 48 `.sql`. Mirar
una carpeta y hablar del sistema entero es exactamente el error que esta referencia existe para
evitar.

### 1.2 · La distribución del peso

| Tramo | Archivos |
|---|---|
| **> 800 líneas** | **3** |
| 400 - 800 | 15 |
| 150 - 400 | 34 |
| < 150 | 24 |

**Los tres gigantes concentran el 28% del núcleo:**

| Archivo | Líneas | % | Qué es |
|---|---|---|---|
| `telegram_channel.py` | **4,570** | **17%** | ⚠️ la puerta que Brian usa a diario |
| `conversation.py` | 1,871 | 7% | el que decide qué hace el agente en cada turno |
| `api_channel.py` | 1,146 | 4% | el canal que se vende |

⭐ **Y el contraste que define la forma del sistema:** `agent.py` tiene **90 líneas**.
**El agente es 50 veces más pequeño que su puerta de entrada.** La lógica no vive en el agente:
vive en el canal.

### 1.3 · La higiene — mejor de lo esperado

| Medida | Resultado |
|---|---|
| Funciones | 492 |
| **Con docstring** | **76 / 76** ✅ |
| **Con type hints** | **76 / 76** ✅ |

⭐ **Dato que corrige una expectativa:** el código **no está sin documentar**. Está documentado y
tipado al 100%. **El problema de For3s OS no es higiene.**

---

## 2 · LA ARQUITECTURA REAL — quién depende de quién

Esto **no estaba escrito en ninguna parte**. Sale de leer los imports de los 76 archivos.

### 2.1 · ⭐ Por qué el grafo era invisible

El primer intento de mapear dependencias dio **43 módulos huérfanos**. Era **falso**. La causa:

```python
# Lo que un detector ingenuo ve (cabecera del archivo):
from for3s_core.agent import Agent

# Lo que NO ve, y es la mayoría:
from for3s_core import audit, db, identidad, memory, multimodal, tiempo   # multi-módulo
    from for3s_core import multiagente        # ← DENTRO de una función (perezoso)
```

**Imports perezosos medidos (dentro de funciones, no en la cabecera):**

| Módulo | Dependencias | De ellas perezosas |
|---|---|---|
| `telegram_channel` | 41 | **26** |
| `conversation` | 21 | 13 |
| `tasks` | 17 | **16** |
| `dmn_tasks` | 11 | 9 |
| `api_channel` | 10 | **10 — todas** |

⭐ **Esta es la razón medida de que nadie sepa cómo está construido For3s OS.** El grafo real
es invisible para cualquier herramienta que lea solo las cabeceras. La estructura existe, pero
**está escondida dentro de los cuerpos de las funciones.**

### 2.2 · Los cimientos — si se rompen, cae todo

| Módulo | Cuántos dependen de él |
|---|---|
| **`llm`** | **15** |
| **`audit`** | **14** |
| **`config`** | **10** |
| `memory` | 8 |
| `kg` · `conversation` | 6 |
| `embeddings` · `mcp_client` · `skills` | 5 |
| `dmn` · `db` · `perfil` · `insights` · `entrenamiento_olas` · `identidad` · `secret_store` · `modelos` | 4 |

### 2.3 · Los orquestadores — los que llaman a todos

`telegram_channel` (41) · `conversation` (21) · `tasks` (17) · `dmn_tasks` (11) · `api_channel` (10)

### 2.4 · Las raíces — 5 módulos que nadie importa

`telegram_channel` · `cli` · `api_admin_http` · `sandbox` · `entrenamiento_repo`

✅ **Los cinco son entrypoints legítimos.** `entrenamiento_repo` fue sospechoso de código muerto
hasta que se verificó: tiene `if __name__ == "__main__"` en la **línea 403**. **No hay código
muerto en el núcleo.**

---

## 3 · LOS 12 COMPONENTES

Agrupados por lo que **hacen** y por cómo se llaman entre ellos:

| # | Componente | Piezas | Líneas |
|---|---|---|---|
| **1** | **Canal Telegram** | `telegram_channel` `md_html` `multimodal` | **4,570+** |
| **2** | **Canal API** (lo que se vende) | `api_channel` `api_admin` `api_admin_http` `api_metering` `api_waitlist` | 2,048 |
| **3** | **Agente** | `agent` `tool_loop` `llm` `modelos` `conversation` | 3,166 |
| **4** | **Multi-agente** | `multiagente` `specialists` `equipo` `handoff` | 1,282 |
| **5** | **Memoria** | `memory` `memoria` `kg` `embeddings` `consolidator` `microglia` `relevance` `cache` | 2,270 |
| **6** | **Cerebro / decisión** | `dmn` `dmn_tasks` `decisiones` `confidence` `governor` `insights` `aprende` | 2,543 |
| **7** | **Identidad y perfil** | `identidad` `perfil` `perfil_infer` `expediente` `mision` `introspeccion` | 1,486 |
| **8** | **Entrenamiento** | 8 módulos `entrenamiento_*` | 2,192 |
| **9** | **Seguridad** | `crypto` `secret_store` `audit` `sandbox` `execute` | 470 |
| **10** | **Datos** | `db` `config` + 47 migraciones | — |
| **11** | **Trazabilidad** | `trace` `analytics` `health` `version` | 1,400 |
| **12** | **Infra / despliegue** | 5 Dockerfiles · 2 compose · CLI `for3s` · `install.sh` · 6 CI | — |

⚠️ **Cinco de estos doce no aparecían en el mapa mental de Brian** cuando nombró los bloques que
esperaba: entrenamiento, multi-agente, identidad, trazabilidad e infra. **Existen y pesan
8,352 líneas juntos — el 31% del núcleo.**

---

## 4 · EL DESPLIEGUE — 28 contenedores, 3 instancias

### 4.1 · La topología medida

**28 contenedores vivos · 10 servicios distintos · 3 instancias.**

| Servicio | Copias | Para qué |
|---|---|---|
| `agent` | 3 | el bot |
| `worker` | 3 | los jobs nocturnos (`arq`) |
| `postgres` | 3 | la BD (una por instancia) |
| `valkey` | 3 | caché |
| `grafana` | 3 | métricas |
| `sandbox` | 3 | ejecución aislada de código |
| `render` | 3 | render de imágenes |
| `github-mcp` + `github-mcp-write` | 3+3 | acceso a GitHub |
| `admin` | **1** | ⚠️ **solo en `general`** |

⚠️ **El servicio `admin` existe solo en una instancia.** Ningún documento declara esa asimetría.

### 4.2 · 🟠 La tercera instancia — huérfana

La campaña declara instancias `brian` y `general`. **Hay una tercera**, sin prefijo:

| | |
|---|---|
| Nombre | `for3s-agent-1` — sin dueño declarado |
| Datos | **2,782 memorias** · 2,494 eventos de auditoría |
| Servicios propios | `postgres` `valkey` `grafana` `worker` `sandbox` |
| RAM | **933 MB** — la que más consume de las tres |
| 🔴 Su token | `TELEGRAM_BOT_TOKEN=# migr…` — **un comentario, no un token** |

**Lleva horas corriendo, guarda datos, y su bot no puede conectarse a Telegram.**

### 4.3 · Recursos del servidor

| | |
|---|---|
| RAM | 18 GB · 3.8 GB en uso |
| Disco | 937 GB · 172 GB usados (20%) |
| Los 3 `agent` | ~900 MB cada uno (cargan BGE-M3 en memoria) |

⚠️ **Ambos agentes registran `Red Telegram inestable (NetworkError) — reintenta solo` cada ~4 min.**

---

## 5 · LOS DATOS — qué guardó de Brian y qué hizo con ellos

Esta es la sección que la campaña más necesita: **el sistema ya se usó, y sus datos cuentan una
historia que el código no cuenta.**

### 5.1 · El censo: 49 tablas

**31 con datos · 18 vacías.**

| Tabla | Filas | Qué significa |
|---|---|---|
| `episodes_events` | **33,908** | la memoria |
| `DERIVED_FROM` (grafo AGE) | 31,230 | las relaciones del grafo |
| `Episodio` (grafo AGE) | 31,037 | los nodos del grafo |
| `audit_events` | 12,908 | la auditoría encadenada |
| `import_manifiesto` | 11,927 | el material de entrenamiento |
| `dmn_corridas` | 3,275 | el cerebro nocturno |
| `sessions` | 2,072 | las sesiones |
| `Concepto` | 1,342 | conceptos del grafo |
| `cron_corridas` | 1,053 | los jobs |
| `secrets` | 38 | los secretos (cifrados) |
| `api_consumo` | 35 | consumo del canal API |
| `skills` · `personas` | 16 · 16 | habilidades y gente |
| `insights` · `api_clients` | 15 · 15 | lo aprendido y los clientes |
| `perfil_usuario` · `owner` · `temas` | 1 · 1 · 1 | |

### 5.2 · 🔴 El ciclo de la memoria — el hallazgo central

| Medida | Valor |
|---|---|
| Memorias totales | **33,908** |
| De ellas **importadas** (5-jul, 11 lotes) | **33,737 · 99.5%** |
| **Conversación real por Telegram** | **134 mensajes** |
| Por API | 37 |
| Consolidadas al grafo | 30,959 (**91.3%**) ✅ |
| Borradas por la microglía | 13,974 (41%) |
| 🔴 **Nunca recuperadas** | **33,887 de 33,908 · 99.94%** |
| Recuperadas alguna vez | **21** |
| Última memoria escrita | **30-jul** |
| Última conversación real | **25-jul** |

⭐⭐ **El diagnóstico del 13-jul, ahora con número:** *"se usó como TUBO y nunca devolvió valor"*.

**El sistema guarda excelente y recupera casi nunca.** La entrada funciona (33,908 guardadas), la
consolidación funciona (91.3% al grafo), el olvido funciona (41% podado). **El camino de vuelta
—recuperar una memoria cuando sirve— está muerto en la práctica: 0.06%.**

### 5.3 · La proporción del uso real

| | |
|---|---|
| Tokens de entrada (Telegram) | **624,702** |
| Tokens de salida | **23,490** |
| **Proporción** | **26 : 1** |

**Brian da mucho contexto y recibe poco.** Modelo usado: `claude-sonnet-4-6`.

### 5.4 · Cuándo se usó cada cosa

| Tabla | Última | Días sin uso |
|---|---|---|
| `dmn_corridas` · `cron_corridas` | hoy | **0** ✅ |
| `audit_events` | ayer | 1 ✅ |
| `api_clients` | 31-jul | 12 |
| `episodes_events` · `api_consumo` | 30-jul | **13** 🔴 |
| `equipos` | 25-jul | 18 |
| `insights` | 14-jul | **29** 🔴 |
| `temas` | 09-jul | 34 |
| `perfil_usuario` · `owner` · `secrets` | 05-jul | **38** |

⚠️ **El sistema trabaja de noche (461 corridas del DMN en 7 días) pero no guarda memoria nueva
hace 13 días.** Trabaja sobre material que ya no crece.

### 5.5 · Lo que sabe de Brian — con un error

```json
{
  "telegram_user_id": 1923367928,
  "nombre": "Brian",
  "rol": "jazz",          ← 🔴 la instancia borrada el 6-ago
  "zona": "México (CST/CDT)",
  "estilo": "Español MX. Quiere corrección ortográfica con el error mostrado.
             Avisar SIEMPRE antes de operaciones de BD.",
  "rasgos": ["founder de Frutero", "persona de confianza: Jazz Criptec…"]
}
```

✅ **El campo `estilo` es correcto y valioso** — capturó reglas reales de trabajo.
🔴 **El campo `rol` dice `jazz`** — una instancia que ya no existe.
Conoce además **16 personas** con sus roles.

### 5.6 · 🔴 Los insights: encontró valor y se lo quedó

**15 generados · 9 nunca entregados.**

| Fecha | Tipo | Título | Entregado |
|---|---|---|---|
| 14-jul | propuesta | Antes del lunes: verificar el estado real del repo del bootcamp | 🔴 **NO** |
| 14-jul | **patrón** | **Lanzas tareas y las cancelas antes de que terminen** | 🔴 **NO** |
| 14-jul | **patrón** | **Consumo de tokens como fricción recurrente** | 🔴 **NO** |
| 14-jul | cabo_suelto | UX Fixes #3-#12 sin tocar | 🔴 **NO** |
| 14-jul | cabo_suelto | PR #129 quedó sin mergear | 🔴 **NO** |
| 14-jul | cabo_suelto | La app demo quedó sin confirmar que funciona | 🔴 **NO** |
| 14-jul | cabo_suelto | Godinez Studio: cambios sin commit | 🔴 **NO** |
| 14-jul | cabo_suelto | Dashboard pendiente: gráfico de tokens | 🔴 **NO** |
| 13-14 jul | varios | 6 más | ✅ sí |

⭐ **El sistema detectó cosas ciertas y útiles sobre cómo trabaja Brian — y se las guardó.**
Los dos patrones no entregados describen fricciones reales que Brian ha mencionado por su cuenta.
**Ninguno se ha generado desde el 14 de julio.** La causa está en §7.4.

### 5.7 · Las skills

**16 registradas · 3 nunca usadas · último uso global: 26-jul.**

Las más usadas: `acompanante` (8) · `genomad` (7) · `genomad-chain-agent` (7) · `audit-code` (3).
Sin usar nunca: `marketing-designer` · `monad-blitz-projects` · `seleccion-de-arquitectura-rnnlstm`.

### 5.8 · 🔴 Las 18 tablas vacías — con su migración de origen

Cada una es **una capacidad que se construyó y nunca se encendió:**

| Tabla | Migración | Capacidad sin usar |
|---|---|---|
| **`decisiones`** | `032` | ⭐ **el sistema no decide nada** |
| **`trace_events`** · **`trace_alertas`** | `042` · `043` | ⭐ **For3s TRACE no registra** — se presentó en el Incubathon |
| `misiones` | `045_expediente` | el Frente E "confianza para delegar" |
| `governor_bloqueos` | `020` | el gobernador nunca ha bloqueado nada |
| `maestro_chunks` | `046` | el índice maestro |
| `gh_files` · `gh_resources` | `004` | GitHub MCP sin datos |
| `estado_persona` | `029` | estado por persona |
| `tema_estado` | `031` | estado por tema |
| `temas_equipo` | `028` | temas del equipo |
| `solicitudes` | `012` | solicitudes |
| `consulted_web` | `006` | consultas web registradas |
| `api_waitlist` | `041` | lista de espera del API |
| `_ag_label_*` (4) | `034_age_grafo` | internas de AGE (vacías es normal) |

⭐ **33,908 episodios guardados y `decisiones` en cero.** El sistema **recuerda muchísimo y no
decide nada.**

---

## 6 · EL CEREBRO NOCTURNO — trabaja mucho, hace poco

### 6.1 · El dato global

**3,275 corridas del DMN. Hicieron algo 135 veces. El 4.1%.**

### 6.2 · Por tarea (7 días)

| Tarea | Intentos | Corrió | Motivo |
|---|---|---|---|
| **`cache_prewarming`** | 114 | 🔴 **0** | `trigger_ok=false` **siempre** |
| **`embedding_precompute`** | 114 | 🔴 **0** | `trigger_ok=false` **siempre** |
| **`routing_learning`** | 114 | 🔴 **0** | `trigger_ok=false` **siempre** |
| `insight_mining` | 114 | 11 | *"sin nada que valga (silencio antes que relleno)"* |
| `memory_consolidation` | 1 | 1 | ✅ |
| `eval_regression_detection` | 1 | 1 | *"v1 métrica simple (golden set formal = deuda)"* |
| `hypothesis_generation` | 1 | 0 | trigger false |
| `pattern_detection` | 1 | 0 | trigger false |
| `prompt_improvement` | 1 | 0 | trigger false |

⚠️⚠️ **Tres tareas se despiertan 114 veces cada 7 días y NUNCA han hecho nada.** No fallan: su
**disparador nunca se cumple**. Y eso **no aparece en ningún log de error** — se registra como
corrida normal, con `ok=true`. **Un fallo silencioso perfecto.**

### 6.3 · Qué hace el sistema con su tiempo

**Auditoría de 7 días: 486 acciones.**

| Acción | Veces | % |
|---|---|---|
| **`microglia_forget`** | **484** | **99.6%** |
| `cls_consolidation` | 2 | 0.4% |

**Histórico: 11,455 de 12,908 acciones (89%) son la microglía olvidando.**

⭐ **El sistema pasa el 89% de su actividad registrada olvidando.** El olvido funciona bien —
pero es casi lo único que hace de forma medible.

### 6.4 · Los 13 jobs del cron

| Job | Hora UTC | Última corrida | Estado |
|---|---|---|---|
| `dmn_idle` | cada 30 min | **hoy** | ✅ |
| `backup` | 07:00 | ayer | ✅ |
| `cls` | 08:00 | ayer | ✅ |
| `status` | 08:30 | ayer | ✅ |
| `relevance` | 08:45 | ayer | ✅ |
| `microglia` | 09:00 | ayer | ✅ |
| `trace_alertas` | 09:15 | ayer | ✅ |
| `curar_skills` | 09:30 | ayer | ✅ |
| `job_perfil` | 09:45 | ayer | ✅ |
| `job_estilo` | 09:50 | ayer | ✅ |
| `dmn_noche` | 10:00 | ayer | ✅ |
| **`health_check`** | **10:30** | **26-jul** | 🟠 17 días |
| 🔴 **`digest_valor`** | **14:00** | **14-jul** | 🔴 **29 días** |

**La causa de los dos muertos está en §7.4** — y no es un bug de código.

---

## 7 · LOS CANALES — qué está conectado y qué está aislado

Esta sección responde a la pregunta de Brian: *"debería haber 7 o más canales de comunicación
pero solo existe uno, porque los componentes se hicieron por separado"*.

**Medido: hay 4 canales, no 1. Pero ninguno es bidireccional entre componentes.**

### 7.1 · Los canales que existen

| # | Canal | Qué conecta | Estado |
|---|---|---|---|
| 1 | **`Conversation`** | Telegram **y** API → el agente | 🟢 **bien conectado** |
| 2 | **`arq` sobre Valkey db1** | quien encola → el worker | 🟡 unidireccional |
| 3 | **La base de datos** | todos escriben, todos leen | 🟡 sin avisos |
| 4 | **HTTP crudo a `api.telegram.org`** | el worker → Brian | 🔴 camino paralelo |
| — | `MessageBus` | **nadie** | 🔴 **muerto** |
| — | Valkey pub/sub | — | 🔴 **no existe** |
| — | Postgres `LISTEN/NOTIFY` | — | 🔴 **no existe** |

✅ **Corrección a la hipótesis, con evidencia:** los dos canales de usuario **sí convergen**.
`api_channel.py:1068` lo dice literalmente en su docstring: *"El MISMO camino que Telegram
(_responder_agente_simple): Conversation+send"*. Ambos usan `Conversation`. **Ese cable está bien.**

**Lo que falta es comunicación entre COMPONENTES DE FONDO**, que es distinto.

### 7.2 · ⭐ El `MessageBus` — el ejemplo de Brian, encontrado literal

`multiagente.py:37` implementa un **bus de mensajes completo y bien diseñado**:

```python
class MessageBus:
    """El correo interno del equipo (R5 B3 §5.3.3). UN bus por "batch" (una corrida
    del equipo sobre una tarea). Buzón central del Hub + un buzón por specialist +
    broadcast a todos. Colas con maxsize → si se llenan, hay backpressure."""

    HUB_INBOX_MAXSIZE = 1000
    SPECIALIST_INBOX_MAXSIZE = 100
```

**Lo que ofrece:** buzón central del Hub · un buzón por specialist · broadcast a todos
("cancelen") · **backpressure** (avisa en vez de reventar la RAM) · colas con tope.

| Medida | Resultado |
|---|---|
| Quién importa `MessageBus` | 🔴 **nadie** |
| `asyncio.Queue` fuera de `multiagente` | 🔴 **cero** |
| Quién arranca `multiagente` | **solo `telegram_channel`** |

⭐⭐ **Este es exactamente el patrón que Brian describió:** la infraestructura para que N
componentes se hablen **existe, funciona, y vive encerrada dentro de un solo componente que la
crea y la destruye en cada uso.** Su propio docstring declara el límite: *"UN bus por batch"*.

### 7.3 · El punto único de ejecución

**`run_tool_loop` se llama desde UN solo sitio:** `conversation.py:1610`.
**Todo el trabajo del agente pasa por ahí.**

Y el control de concurrencia que existe **no controla eso**:

| Pieza | Qué gobierna | Quién la usa |
|---|---|---|
| `ConcurrencyManager` (444 líneas) | tokens por minuto, anti-429 | 🔴 **solo `llm.py`** |
| Semáforo de `multiagente` | 2 specialists a la vez (`FOR3S_EQUIPO_CONC_MAX`) | solo dentro de multiagente |
| Valkey | 🔴 **solo caché** (`get`/`set`) | 5 módulos |
| `asyncio.Lock` en telegram | GitHub y equipo | telegram_channel |

**Nada limita cuántas peticiones distintas atiende el sistema a la vez.** No hay cola de entrada,
no hay prioridad, no hay backpressure fuera del bus encerrado.

### 7.4 · 🔴 El worker vive media jornada — la causa raíz

**Corridas de `dmn_idle` por hora UTC, 7 días:**

```
00h ██████████ 10     12h ░░░░░░░░░░  0
01h ██████████ 10     13h ░░░░░░░░░░  0
02h ██████████ 10  →  14h ░░░░░░░░░░  0  ← digest_valor programado AQUÍ
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

⭐ **Ocho horas de silencio absoluto (11h-18h UTC), todos los días, 7 días seguidos.**

**No es un fallo de código: el servidor es una laptop que se apaga por el día.**
Confirmado: `RestartCount=0`, el worker arrancó a las 19:45 UTC y nunca ha reiniciado.

**La consecuencia exacta:**

| Job | Hora UTC | ¿Cae en la ventana viva? | Última |
|---|---|---|---|
| 11 jobs | 05:00-10:00 | ✅ sí | ayer |
| `health_check` | 10:30 | ⚠️ el borde | 26-jul |
| **`digest_valor`** | **14:00** | 🔴 **NO — centro del agujero** | **14-jul** |

⭐⭐ **Esto explica los 9 insights retenidos.** No es que el sistema no quisiera entregarlos:
**su cartero está programado a una hora en la que el sistema no existe.** Su último registro dice
*"envío falló — insights quedan 'nuevo' (reintento mañana)"*. **El mañana nunca llegó.**

Y `proactivo=true` en el perfil: **Brian no lo apagó.**

### 7.5 · Veredicto por componente

| Componente | Cómo recibe | Cómo responde | Veredicto |
|---|---|---|---|
| Telegram ↔ agente | `Conversation` | directo | 🟢 conectado |
| API ↔ agente | `Conversation` | directo | 🟢 conectado |
| Worker ← quien encola | `arq`/Valkey | 🔴 HTTP crudo a Telegram (`tasks.py:475`) | 🟡 medio cable |
| Multi-agente | solo Telegram | `MessageBus` interno y efímero | 🔴 **aislado** |
| DMN | cron horario | escribe en BD | 🔴 **sin avisar a nadie** |
| Insights | lee BD | job de las 14:00 | 🔴 **muerto 29 días** |
| Microglía | cron | audita | 🟢 funciona |

⭐ **El patrón, en una frase: todo lo que corre DENTRO de una petición de usuario está bien
conectado. Todo lo que corre POR SU CUENTA escribe en la BD y no tiene forma de avisar a nadie.**

---

## 8 · SEGURIDAD Y PRIVACIDAD

### 8.1 · ✅ Lo que está bien — y hay que decirlo

| Aspecto | Estado | Evidencia |
|---|---|---|
| **Secretos** | ✅ **cifrados** | tabla `secrets` con columnas `nonce` + `ciphertext`; **no existe columna en claro** |
| **Cadena de auditoría** | ✅ **íntegra** | 12,908 eventos, **todos** con `hash_self` **y** `hash_prev` |
| **Aislamiento físico** | ✅ **confirmado** | volúmenes `pgdata` separados por instancia |
| **Aislamiento de datos** | ✅ **verificado** | `brian` 33,908 episodios vs `general` 18 |
| **Filtro por sesión** | ✅ **presente** | las consultas a contenido usan `WHERE session_id = $1` |

`crypto.py` implementa correctamente: `load_or_create_master_key` · `derive_workspace_key` ·
`encrypt` · `decrypt`. **La criptografía está bien hecha.**

### 8.2 · 🔴 El hallazgo más grave: el contenido en claro

**El contenido de las conversaciones de Brian está EN CLARO en la base de datos.**

Evidencia — leído directamente, sin descifrar nada:

```
SELECT left(content,60) FROM episodes_events WHERE channel='telegram' AND role='user'…
→ "En lo que lo arreglas, te voy a dar información de máxima pr…"
→ "[imagen: foto.jpg] Sigue diciendo que es privado"
```

| Medida | Valor |
|---|---|
| Texto de conversaciones **en claro** | **15 MB** |
| Embeddings | 133 MB |
| BD total | 471 MB |

**Quién usa `crypto.py`:** solo `secret_store.py` y `automod.py`.
**Búsqueda de cifrado sobre `content`:** 🔴 **cero coincidencias.**

⭐ **Esto contradice el Pilar 1 del Grafo Maestro**, que declara cifrado end-to-end. La
criptografía existe y funciona; **el contenido de las conversaciones nunca pasa por ella.**

⚠️ **Uno de esos mensajes en claro dice literalmente: *"Sigue diciendo que es privado"*.**

### 8.3 · El workspace único

Los 12,908 eventos de auditoría viven en `workspace_id = 'default'`. **Un solo workspace**, aunque
el código soporta varios (`derive_workspace_key` existe y funciona).

---

## 9 · RENDIMIENTO Y COSTE

### 9.1 · Latencia — la cola es 18× la mediana

| Medida | Valor |
|---|---|
| **p50** | **2,770 ms** |
| **p90** | **49,966 ms** |
| **max** | **278,999 ms** (279 segundos) |
| **Ratio p90/p50** | **18×** |

⭐ **Esto valida la advertencia del paper de Stream RAG:** el promedio miente. Un sistema con
p50 de 2.7s parece rápido; su p90 de 50s dice que **una de cada diez veces el usuario espera casi
un minuto.**

### 9.2 · Duración por job

| Job | n | p50 | max |
|---|---|---|---|
| `dmn_idle` | 856 | 73 ms | **279,050 ms** |
| `cls` | 20 | 39,732 ms | 221,310 ms |
| `status` | 20 | 12,336 ms | 31,245 ms |
| `relevance` | 19 | 8,081 ms | 18,665 ms |
| `job_perfil` | 17 | 8,876 ms | 16,069 ms |
| `backup` | 25 | 3,960 ms | 13,495 ms |
| `microglia` | 19 | 1,619 ms | 6,071 ms |

### 9.3 · Coste real

| | |
|---|---|
| **Coste total del DMN** | **$5.17** (79 corridas con coste) |
| El más caro | `insight_mining` — **$3.72** en 62 corridas |
| `memory_consolidation` | $1.20 en 12 corridas |
| `pattern_detection` | $0.25 en 5 corridas |
| ⚠️ `embedding_precompute` | **$0.00** pero **61,944 ms de media** — 62 segundos por corrida |

**Canal API:** 35 llamadas · 193,622 tokens · última el 30-jul.

### 9.4 · 🔴 Lo que NO se mide

| Camino | Mide su tiempo | Percentiles |
|---|---|---|
| `api_metering.py` — **lo que se cobra** | ✅ | ✅ p50 · p95 · max |
| `agent.py` — **el agente** | 🔴 **no** | 🔴 |
| `tool_loop.py` — el bucle de herramientas | 🔴 **no** | 🔴 |
| `multiagente.py` — el equipo | 🔴 **no** | 🔴 |

**De 76 archivos, solo 6 miden su propio tiempo.**

⭐ **En una frase: lo que se COBRA está medido; lo que se USA, no.** Nadie sabe cuánto tarda
For3s en responderle a Brian, ni en qué etapa se va el tiempo.

**Instrumentación general:** 43 de 76 registran errores · 18 tienen timeout · 12 tienen reintento.

**El log de 24h del agente `brian`: 27 líneas, 4 con error.**
⚠️ 27 líneas en 24 horas **no es silencio sano: es ausencia de instrumentación.** Un fallo
intermitente sería invisible.

---

## 10 · LA HISTORIA CONSTRUCTIVA — 47 migraciones

Las migraciones son **el registro cronológico de cómo se construyó For3s OS**. Las 47 están
aplicadas (tabla `schema_version`).

| # | Migración | Qué añadió |
|---|---|---|
| 001-002 | inicial · secrets | la base y los secretos |
| 003-009 | channel · github · consulted · embeddings · governance · veces_recuperado | el turno, GitHub, la memoria semántica |
| 010-013 | multiusuario · memoria_scope · solicitudes · hilo_por_usuario | **el salto a varios usuarios** |
| 014-017 | temas · corridas_equipo · hilo_status · expulsion | los temas y el equipo |
| 018-020 | perfil_usuario · skills · **governor** | el perfil, las habilidades y **los frenos** |
| 021-023 | **dmn** · dmn_propuestas · cron_corridas | **el cerebro nocturno** |
| 024-027 | owner · skills_embedding · personas · conectar_memoria | el dueño y la gente |
| 028-031 | temas_equipo · estado_persona · diario_cambios · tema_estado | el estado por persona y tema |
| **032** | **decisiones** | 🔴 **el sistema decidiría — la tabla sigue vacía** |
| 033-034 | entrenamiento · **age_grafo** | el entrenamiento y **el grafo AGE** |
| 035-041 | api_clients · insights · valor_entrega · insights_embedding · api_acceso · api_consumo · api_waitlist | **el canal que se vende** |
| **042-044** | **trace_events · trace_alertas · trace_alertas_ricas** | 🔴 **For3s TRACE — las tablas siguen vacías** |
| 045-047 | expediente · maestro_indice · owner_admin_email | el Frente E y el índice maestro |

**Fechas clave:**

| | |
|---|---|
| Primera aplicación (001-0XX de golpe) | **05-jul 03:32** |
| `045_expediente` | 16-jul |
| `046_maestro_indice` | 20-jul 05:21 |
| **`047_owner_admin_email` (última)** | **20-jul 19:34** |

⭐ **El esquema lleva 22 días congelado.** El 5-jul se aplicaron decenas de migraciones en
segundos — eso es una **reconstrucción de BD desde cero**, no una evolución gradual. Explica por
qué las fechas de `owner`, `perfil_usuario` y `secrets` son todas del 5-jul.

⚠️ **Tres convenciones de nombres conviviendo** en el mismo esquema: `creado_at` (19 tablas) ·
`created_at` (`episodes_events`, `secrets`) · `ts` (`audit_events`). **Cualquier consulta genérica
sobre fechas falla en al menos una tabla.**

---

## 11 · LA VARA DEL PÚBLICO

> **Brian, 2026-08-11:** *"El sistema For3s OS es para que el público lo pueda ocupar, no solo yo.
> La información es mía pero la lógica de For3s OS debe ser tan profesional y adaptable para el
> público en general."*

Esa vara define **cuatro pruebas**. Esto es lo medido contra cada una:

### 11.1 · 🔴 Algo hardcodeado a Brian

```python
entrenamiento_backlog.py:27   _TG_BRIAN = 1923367928
entrenamiento_olas.py:36      _TG_BRIAN = 1923367928
```

**El ID de Telegram de Brian, literal en el código**, usado **8+ veces** como `telegram_user_id`
(líneas 126, 239, 270, 394, 548, 614 de `entrenamiento_backlog`; 180, 195 de `entrenamiento_olas`).

**Otro usuario instala For3s y esos módulos escriben contra el ID de Brian.**

⚠️ Comparación que muestra el criterio correcto:

```python
config.py:42   owner_session: str = "brian"                              # default
config.py:71   os.environ.get("FOR3S_OWNER_SESSION", "brian").strip()    # ✅ con salida por ENV
```

`config.py` **sí** tiene salida por variable de entorno. `_TG_BRIAN` **no tiene ninguna.**

### 11.2 · 🟠 Algo que solo Brian sabe usar

**No verificado sistemáticamente.** Indicio: `telegram_channel.py` tiene 4,570 líneas con decenas
de comandos; no se auditó si cada uno se documenta a sí mismo. **Queda en §14.**

### 11.3 · 🟠 Algo que no escala a miles

| Indicio | Medida |
|---|---|
| Cada instancia carga BGE-M3 en RAM | **~900 MB por agente** |
| Sin límite de peticiones concurrentes | §7.3 |
| Semáforo del equipo | 2 specialists — conservador por cupo compartido de Claude |
| 3 instancias en una laptop | 28 contenedores, 3.8 GB de 18 GB |

⚠️ **A 900 MB por instancia, esta máquina soporta ~20 instancias. El criterio de Brian es "miles
de millones de personas".** El modelo actual es **una instancia completa por usuario** — cada uno
con su Postgres, su Valkey, su Grafana, su agente y su worker.

### 11.4 · 🔴 Algo que expone datos de otro

| Prueba | Resultado |
|---|---|
| Aislamiento físico entre instancias | ✅ volúmenes separados |
| Consultas a contenido sin filtro de dueño | ✅ **ninguna** — todas usan `WHERE session_id = $1` |
| 🔴 **Contenido cifrado en reposo** | 🔴 **NO — 15 MB en claro** |

**El aislamiento entre usuarios está bien. La protección del dato en reposo no existe.**

---

## 12 · 📋 CATÁLOGO COMPLETO DE HALLAZGOS

24 hallazgos, ordenados por gravedad. **Cada uno con su evidencia y dónde verificarlo.**

### 🔴 CRÍTICOS (5)

| # | Hallazgo | Evidencia | § |
|---|---|---|---|
| **H-01** | **Contenido de conversaciones EN CLARO** | 15 MB legibles; `crypto.py` solo lo usan `secret_store` y `automod`; cero coincidencias de cifrado sobre `content`. Contradice el Pilar 1. | 8.2 |
| **H-02** | **Memoria con 0.06% de recuperación** | 33,887 de 33,908 nunca recuperadas; solo 21 con `last_accessed` | 5.2 |
| **H-03** | **Instancia huérfana consumiendo recursos** | `for3s-agent-1`: 2,782 memorias, 933 MB, `TELEGRAM_BOT_TOKEN=# migr…` | 4.2 |
| **H-04** | **Worker muerto 8h/día → entrega de insights muerta 29 días** | 0 corridas de 11h-18h UTC en 7 días; `digest_valor` programado a las 14:00 | 7.4 |
| **H-05** | **ID de Telegram de Brian hardcodeado** | `_TG_BRIAN = 1923367928` en 2 archivos, 8+ usos, sin salida por ENV | 11.1 |

### 🟠 GRAVES (9)

| # | Hallazgo | Evidencia | § |
|---|---|---|---|
| **H-06** | **3 tareas del DMN con 0 corridas de 114** | `cache_prewarming` · `embedding_precompute` · `routing_learning` — `trigger_ok=false` siempre, sin log de error | 6.2 |
| **H-07** | **9 de 15 insights nunca entregados** | incluidos 2 patrones ciertos sobre cómo trabaja Brian | 5.6 |
| **H-08** | **`MessageBus` existe y nadie lo usa** | cero importadores; efímero por diseño ("UN bus por batch") | 7.2 |
| **H-09** | **36 de 76 módulos con CERO líneas ejecutadas** | medido en `.coverage` del 16-jul; incluye `tasks` (722), `governor` (444), `multiagente` (397) | 12.1 |
| **H-10** | **28 de 75 módulos sin mención en ningún test** | `tasks` · `consolidator` · `dmn_tasks` · `health` · `governor` · `multiagente` | 12.1 |
| **H-11** | **p90 = 18× el p50** | 2,770 ms vs 49,966 ms; max 279 s | 9.1 |
| **H-12** | **El camino del agente no mide su tiempo** | `agent` · `tool_loop` · `multiagente` = 0 instrumentación; solo lo cobrado se mide | 9.4 |
| **H-13** | **Perfil de Brian dice `rol: jazz`** | instancia borrada el 6-ago | 5.5 |
| **H-14** | **18 tablas vacías = 18 capacidades apagadas** | `decisiones`, `trace_events`, `misiones`, `governor_bloqueos`… | 5.8 |

### 🟡 MEDIOS (10)

| # | Hallazgo | Evidencia | § |
|---|---|---|---|
| **H-15** | `telegram_channel.py` con 4,570 líneas (17% del núcleo) | 2.4× el siguiente; es la puerta diaria de Brian | 1.2 |
| **H-16** | El agente son 90 líneas y su canal 4,570 | la lógica vive en el canal, no en el agente | 1.2 |
| **H-17** | Grafo de dependencias invisible | mayoría de imports son perezosos dentro de funciones | 2.1 |
| **H-18** | Tres convenciones de fecha en el mismo esquema | `creado_at` · `created_at` · `ts` | 10 |
| **H-19** | Servicio `admin` solo en una instancia | asimetría no declarada en ningún documento | 4.1 |
| **H-20** | `NetworkError` de Telegram cada ~4 min | en las dos instancias vivas | 4.3 |
| **H-21** | 27 líneas de log en 24h | ausencia de instrumentación, no silencio sano | 9.4 |
| **H-22** | `embedding_precompute` tarda 62 s de media | y no dispara desde hace un mes | 9.3 |
| **H-23** | 3 skills nunca usadas · último uso global 26-jul | de 16 registradas | 5.7 |
| **H-24** | Un solo `workspace_id` (`default`) | aunque el código soporta varios | 8.3 |

### 12.1 · Nota sobre H-09 y H-10 — dos medidas distintas

| Medida | Qué dice | Cuántos |
|---|---|---|
| **Sin mención en tests** (análisis estático) | ningún test nombra el módulo | **28 de 75** |
| **Cero líneas ejecutadas** (`.coverage`, real) | la corrida de tests no tocó ni una línea | **36 de 76** |

⭐ **La segunda es más dura y más honesta**: un módulo puede estar *mencionado* en un test y aun
así no ejecutarse. **36 de 76 módulos (47%) no se ejecutaron en la corrida de cobertura del 16-jul.**

Los mayores sin ejecutar: `tasks` (722) · `entrenamiento_backlog` (643) · `consolidator` (603) ·
`dmn_tasks` (503) · `health` (486) · `governor` (444) · `entrenamiento_repo` (404) ·
`multiagente` (397) · `aprende` (356) · `entrenamiento_olas` (345).

### 12.2 · ✅ LO QUE ESTÁ BIEN — y no se debe romper

**Un catálogo de hallazgos sin esta sección lee como si todo estuviera mal. No lo está.**

| # | Fortaleza | Evidencia |
|---|---|---|
| **B-01** | **Secretos cifrados de verdad** | `nonce` + `ciphertext`, sin columna en claro |
| **B-02** | **Cadena de auditoría íntegra** | 12,908 eventos, **todos** con `hash_self` y `hash_prev` |
| **B-03** | **Aislamiento físico entre instancias** | volúmenes `pgdata` separados |
| **B-04** | **Aislamiento por sesión en las consultas** | todas las que devuelven contenido usan `WHERE session_id = $1` |
| **B-05** | **Consolidación al grafo al 91.3%** | 30,959 de 33,908 |
| **B-06** | **Documentación y tipado al 100%** | 76/76 con docstring y type hints |
| **B-07** | **Los dos canales de usuario convergen** | Telegram y API comparten `Conversation` |
| **B-08** | **La microglía funciona** | 41% de memoria podada, con auditoría de cada olvido |
| **B-09** | **El canal que se vende SÍ está medido** | `api_metering` con p50/p95/max, excluyendo errores |
| **B-10** | **Backpressure bien diseñado** | el `MessageBus` avisa en vez de reventar la RAM |
| **B-11** | **El perfil capturó reglas reales** | *"Avisar SIEMPRE antes de operaciones de BD"* |
| **B-12** | **Sin código muerto en el núcleo** | los 5 sin importadores son entrypoints verificados |
| **B-13** | **Las 47 migraciones aplicadas y versionadas** | tabla `schema_version` completa |
| **B-14** | **`crypto.py` está bien implementado** | derivación de clave por workspace, nonce por mensaje |

---

## 13 · ⚠️ ERRORES QUE COMETÍ MIDIENDO

**Esta sección existe porque una referencia que oculta sus errores no es fiable.** Cada uno se
corrigió antes de que entrara al catálogo.

| # | Lo que afirmé | Lo que era | Cómo se detectó |
|---|---|---|---|
| **E-1** | *"76 archivos"* como total del sistema | 76 son **del núcleo**; el sistema tiene 112 `.py` + 48 `.sql` | contar sin filtrar por carpeta |
| **E-2** | *"43 módulos huérfanos"* | **5**, y 4 son entrypoints | el regex no leía `from for3s_core import a, b, c` ni imports perezosos |
| **E-3** | *"`entrenamiento_repo` es código muerto"* | tiene `__main__` en la línea 403 — **es un entrypoint** | buscar `__main__` antes de afirmar |
| **E-4** | *"36 consultas sin filtro de dueño"* | **ninguna** — todas usan `WHERE session_id=$1` en la línea siguiente | leer el contexto, no solo la primera línea |
| **E-5** | *"el servidor está caído"* | llevaba **8h48m encendido**; no leí `secrets/` | Brian lo corrigió; ahora es `bin/conectar-servidor` |

⭐ **El patrón de los cinco: medir una parte y hablar del todo.** E-1 miró una carpeta, E-2 una
forma de import, E-4 una línea de SQL. **La lección para la campaña: cuando un número parezca
alarmante, medirlo por segunda vez desde otro ángulo antes de actuar sobre él.**

---

## 14 · QUÉ QUEDA SIN MEDIR

**Declarado, no escondido.** La campaña debe saber dónde NO hay terreno firme.

| Hueco | Por qué importa | Cómo se mediría |
|---|---|---|
| **La vara "solo Brian sabe usarlo"** | es 1 de las 4 pruebas del público y no se auditó | revisar los comandos de `telegram_channel` y ver cuáles se autodocumentan |
| **Qué código corre en PRODUCCIÓN** | `.coverage` es de tests del 16-jul, no del sistema vivo | instrumentar el agente (es la sub-fase B2 del plan de comportamiento) |
| **Los 24 edges del Grafo** | la fase 3 los recorrerá; hoy no se sabe cuáles fluyen | trazar cada edge con datos reales |
| **Las 4 tablas `_ag_label_*` vacías** | podrían ser normales de AGE o síntoma | consultar la documentación de Apache AGE |
| **Por qué `trigger_ok=false` siempre** | 3 tareas del DMN sin correr nunca | leer la condición de disparo de cada una |
| **Si `general` y la 3ª instancia tienen los mismos fallos** | se auditó `brian` a fondo, las otras solo por encima | repetir §5-§9 sobre ellas |
| **El rendimiento bajo carga** | todo lo medido es con 1 usuario | prueba de carga (fuera del alcance de la campaña hoy) |

---

## 15 · CÓMO USA ESTO LA CAMPAÑA

**Este documento es TERRENO, no plan.** No dice qué hacer; dice qué hay.

| La campaña pregunta… | Lo responde… |
|---|---|
| ¿qué componentes existen? | §3 — los 12, con piezas y peso |
| ¿qué se usa de verdad? | §5 — los datos reales |
| ¿qué está conectado? | §7 — los 4 canales y el veredicto por componente |
| ¿qué está roto? | §12 — los 24 hallazgos con gravedad |
| ¿qué NO hay que romper? | §12.2 — las 14 fortalezas |
| ¿dónde no sabemos nada? | §14 — los 7 huecos declarados |
| ¿me puedo fiar de este número? | §0 (cómo se midió) y §13 (los errores corregidos) |

⛔ **Lo que este documento NO decide:** qué se arregla primero, cómo se agrupan los bloques, ni
qué vara aplica. Eso lo dicta `campaigns/producto-for3s-os/CAMPAIGN.md` y su autoridad,
`Cerebro/For3s_OS_Grafo_Maestro.md`.

⚠️ **Caducidad:** cada número tiene fecha. El sistema sigue corriendo — `dmn_corridas` y
`cron_corridas` crecen cada noche. **Antes de usar un número para decidir, si tiene más de dos
semanas, re-medirlo con `bin/conectar-servidor`.**

---

## 16 · ⛔ LOS 18 ARCHIVOS GRANDES — decisión APLAZADA con recordatorio

> **Brian, 2026-08-12:** *"Se parte, aún no tenemos que empezar a avanzar con la campaña para
> decidir; **recuérdamelo cuando lleguemos a ese archivo y los otros que tienen mucho código**."*

⚠️ **Esto NO es una lista de archivos a partir.** Es una lista de **preguntas pendientes**. La
decisión se toma **al llegar a cada uno**, con la fase 2 ya medida — no ahora, en abstracto.

⛔ **La obligación concreta:** el bloque que dueñe uno de estos archivos **no cierra su fase 2 sin
preguntarle a Brian** si se parte. `rules/rule-inheritance.md`: en duda, gana la más estricta.

| Líneas | Archivo | Bloque dueño |
|---|---|---|
| **4,570** | `telegram_channel.py` | `canal-telegram` |
| **1,871** | `conversation.py` | `agente` |
| **1,146** | `api_channel.py` | `canal-api` |
| 722 | `tasks.py` | `cerebro` |
| 716 | `memory.py` | `memoria` |
| 643 | `entrenamiento_backlog.py` | `entrenamiento` |
| 623 | `subbloques.py` | `agente` |
| 603 | `consolidator.py` | `memoria` |
| 578 | `identidad.py` | `identidad` |
| 505 | `insights.py` | `cerebro` |
| 503 | `dmn_tasks.py` | `cerebro` |
| 486 | `health.py` | `observabilidad` |
| 486 | `equipo.py` | `multiagente` |
| 444 | `governor.py` | `cerebro` |
| 432 | `trace.py` | `observabilidad` |
| 429 | `tool_loop.py` | `agente` |
| 423 | `dmn.py` | `cerebro` |
| 404 | `entrenamiento_repo.py` | `entrenamiento` |

**Reparto por bloque:** `cerebro` **5** · `agente` 3 · `memoria` 2 · `observabilidad` 2 ·
`entrenamiento` 2 · `canal-telegram` 1 · `canal-api` 1 · `identidad` 1 · `multiagente` 1.

⭐ **Dato para la decisión, no para actuar hoy:** `cerebro` dueña 5 de los 18 (2,597 líneas
repartidas). No es un gigante único como `telegram_channel`, sino **cinco piezas medianas** — y
eso probablemente pide una respuesta distinta a la de un archivo de 4,570 líneas.

⚠️ **El contexto que Brian ya fijó (2026-08-11):** la fase 2 **MARCA y documenta, no parte** —
partir es desarrollo y esta campaña verifica. Esta decisión aplazada es sobre **si se hace una
excepción** en algún caso, y esa excepción la decide Brian, no la campaña.


---

Related: `campaigns/producto-for3s-os/CAMPAIGN.md` (la campaña que lo usa) ·
`Cerebro/For3s_OS_Grafo_Maestro.md` (la autoridad sobre cómo DEBERÍA funcionar) ·
`rules/rule-product-authority.md` (el orden de precedencia) ·
`docs/plans/PLAN-fase-comportamiento.md` (el plan que nació del primer barrido) ·
`bin/conectar-servidor` (cómo re-medir todo esto) ·
`memory/pendiente-agosto-2026.md` (los 74 pendientes declarados).