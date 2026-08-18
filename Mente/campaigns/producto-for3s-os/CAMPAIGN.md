# CAMPAIGN · producto-for3s-os

id: cmp-producto-for3s-os-2026-08
status: active · owner: brian
created: 2026-08-10 · updated: 2026-08-12
exempt: size

> ⭐ **Brian, 2026-08-12:** *"no importa los techos, estos archivos tienen la funcionalidad de que
> los puedes alargar tanto como sea necesario."* Esta campaña carga el **contexto completo** que
> sus 12 bloques necesitan para arrancar en frío — el techo de 150 la partiría.

## Mission

Llevar **For3s OS de MVP que funciona a PRODUCTO que se puede usar**. No se desarrolla nada nuevo:
se **limpia, valida, prueba y verifica** lo que ya existe, con Mente OS v2 como herramienta.

> **Brian, 2026-08-10:** *"Sabes que funciona, ahora nos toca limpiar, validar, probar y volverlo
> un producto."* · *"No es algo que 5 personas lo tendrán, va a ser para miles de millones."*

**Termina cuando:** el código pasa las 6 dimensiones de QA **con la vara de producto**, y Brian
confía en delegarle trabajo — el Frente E que el Incubathon dejó abierto.

## Authority

⭐ `Cerebro/For3s_OS_Grafo_Maestro.md` — **CÓMO FUNCIONA** · las rondas — **CON QUÉ** ·
`memory/archive/Plan_Maestro_Programacion.md` — ⭐ **QUÉ SE EXIGE HOY (el gate por fase)** ·
`memory/archive/Mapa_Construccion_Incremental.md` — **EN QUÉ ORDEN** · el código **se AUDITA, no
manda**. Orden completo y vara temporal: `rules/rule-product-authority.md` §1 y §2.

🧭 **ENTRAR POR AQUÍ SI ES TU PRIMERA VEZ:** `terreno/COMO-INDAGAR.md` — la línea de tiempo desde
mayo-2026, la ruta de lectura mínima (20 min), las 7 técnicas de medición, los 8 errores ya
cometidos y la lista de 7 comprobaciones antes de abrir un bloque.
⚙️ **Y el MÉTODO de las 3 corridas:** `docs/plans/PLAN-3-fases.md` — qué mira cada fase, qué
entrega un bloque para pasarla, los 5 criterios de 🔴 crítico y dónde va cada archivo.

## Standards

- rules/rule-product-authority.md
- rules/qa-dimensions.md
- rules/rule-fix-not-patch.md
- rules/rule-isolation.md
- principles/owner-3-validation.md
- principles/expertise/val-functional.md
- principles/expertise/val-integration.md

## Blocks

| bloque | qué persigue | estado |
|---|---|---|
| **seguridad** | **que el dato sea de su dueño — 🔴 H-01, el 1 de 12** | **active · fase 1** |
| orquestacion-multiagente | el vocabulario multi-agente que v2 no tiene | blocked |

⭐ **LOS 12 ESTÁN DECIDIDOS (Brian, 2026-08-12) — el 1 abierto, 11 por abrir.**
⭐ **REPARTO DEL TERRITORIO: opción A — un archivo, un dueño** (Brian, 2026-08-14). Ningún archivo
lo reclaman dos bloques. Razón medida: `hooks/pre-edit-standards.py` se queda con **el primer
bloque que encuentra** reclamando un archivo, así que dos dueños hacen que el editor reciba la vara
equivocada — *"el daño no es un aviso de más, es el aviso CORRECTO que ya no llega"*. Cuando un
archivo sirva a dos capacidades, el que no lo dueña **pide el hecho por el `Channel`**, no lo abre.
⛔ **No se declaran aquí hasta que existan en `blocks/`:** `contract-campaign.md` §2 obliga a que
un bloque declarado EXISTA, y tiene razón — un hijo huérfano hace que el contexto apunte a nada.
👉 **El orden y el porqué de cada uno: `§F Shared context` de este mismo archivo.**

## Shared context

### ⭐ LOS 12 BLOQUES — decididos 2026-08-12, en orden de ataque

Salen de `AUDITORIA-FOR3S-OS-2026-08.md`, agrupados **por capacidad del producto** — lo que For3s
HACE para un usuario, no carpetas ni nodos del Grafo.

| # | bloque | qué persigue | lo que ya sabemos que arrastra |
|---|---|---|---|
| **1** | `seguridad` | que el dato sea de su dueño | 🔴 **H-01** 15 MB de conversaciones EN CLARO |
| **2** | `memoria` | que lo guardado se RECUPERE | 🔴 **H-02** 33,887 de 33,908 nunca recuperadas |
| **3** | `cerebro` | que decida y devuelva valor | 🔴 **H-04** digest muerto 29d · H-06 H-07 |
| **4** | `despliegue` | que arranque y se instale | 🔴 **H-03** instancia huérfana, 933 MB |
| 5 | `agente` | el turno: recibir → pensar → responder | H-11 p90=18×p50 · H-12 sin medir |
| 6 | `multiagente` | el equipo y su bus | H-08 el bus que nadie usa |
| 7 | `identidad` | quién es el usuario y quién el agente | H-13 `rol: jazz` · 🔴 H-05 hardcode |
| 8 | `entrenamiento` | el material que entra al sistema | origen de H-05 (`_TG_BRIAN`) |
| 9 | `canal-telegram` | la puerta diaria de Brian | H-15 4,570 líneas — el 17% |
| 10 | `canal-api` | lo que se vende | ✅ el único bien instrumentado (B-09) |
| 11 | `datos` | el esquema y su historia | H-18 tres convenciones de fecha |
| 12 | `observabilidad` | saber qué está pasando | H-12 solo 6 de 76 miden su tiempo |

⭐ **EL ORDEN ES POR GRAVEDAD** (Brian, 12-ago). Los 4 con hallazgo 🔴 abren, y **`seguridad` va
primero porque H-01 EMPEORA cada día**: cada mensaje nuevo se suma a los 15 MB en claro. Los
demás no empeoran solos.

⭐ **`entrenamiento` ENTRA** (Brian, 12-ago) — pese a que sus tablas llevan 38 días sin escribir.
Razón: es donde nació `_TG_BRIAN`, y **2,192 líneas sin auditar no se dejan fuera del producto.**

⛔ **DECISIÓN APLAZADA — partir los archivos grandes.** Brian, 12-ago: *"se parte, aún no tenemos
que empezar a avanzar con la campaña para decidir; **recuérdamelo cuando lleguemos a ese archivo
y los otros que tienen mucho código**."* ⚠️ **No se decide ahora: se decide al llegar.** Los 18
archivos >400 líneas y su bloque dueño están en `AUDITORIA-FOR3S-OS-2026-08.md` §16 — **cada
bloque que dueñe uno DEBE preguntárselo a Brian antes de cerrar su fase 2.**

**Dónde se trabaja — REGLA DE LA CAMPAÑA, medida en el servidor 2026-08-10:**

| | |
|---|---|
| **Servidor** | Tailscale `for3s` · `100.112.177.53` · usuario `brianweb3` |
| **Cómo entrar** | 🔑 `secrets/Conectar_Servidor_For3s.md` — ⛔ el valor NUNCA se escribe aquí |
| **El código** | `~/for3s-os` en el servidor · `for3slabs/for3s-os` · rama `main` · **12,876 archivos .py** |
| **La instancia** | 🧪 **`brian`** (`@For3s_Brian_bot`) — la única que se toca |
| **Las otras** | `for3s` (Foresito) y `general` · ⛔ **no se tocan** hasta terminar `brian` |

⭐ **Son 3 instancias, no 5.** `jazz` y `mashe` las borró Brian el 06-ago (*"son ruido"*), y
`RETOMAR.md` las siguió listando 4 días — la IA repitió el dato sin medirlo. **Verificado con
`for3s listar` en el servidor, no leído de un documento.**

⛔ **El clon local `For3s-OS/` NO se toca: es de Brian** (2026-08-10). Está 18 días desfasado y
con 1 commit sin empujar; **eso lo resuelve él**, no la campaña. La fuente es el servidor.

**Por qué existe.** El Incubathon destapó fallos, y la conclusión de Brian fue ⭐ ***"si estoy
viendo esto, ¿cómo estará lo que se construyó?"*** — por eso se verifica antes de construir.
⭐ **Y `LA-VERDAD-DE-V1.md` §6.3 responde el sentimiento del 13-jul** (*"un chat que contesta y
guarda memoria"*): **la memoria SÍ recupera; lo que falla es el contador que lo registra.**

📕 **LA VERDAD DE V1 — `LA-VERDAD-DE-V1.md` (aquí mismo). ENTRAR POR AQUÍ.** Lo que For3s OS ES
contra lo que dice ser: 17 secciones, 50 auditorías, cada número con su comando. Nace de la orden
de Brian (12-ago): *"detalla a lujo de precisión todo lo analizado… va a ser nuestro MD de la
verdad de v1"*.

> ⭐⭐⭐ **EL VEREDICTO, en una frase:** For3s OS **no está roto ni abandonado**. Está en la
> **Fase 1-3 de un plan de 6**, pasa **6/6** el gate de su fase, tiene **13 de 16 hitos**
> construidos, y **va adelantado**: 2 meses de código contra 6-7 estimados.

📍 **FASE EN CURSO DE FOR3S OS: 1-3 de 6** · **GATE VIGENTE: el de la Fase 1**
(`memory/archive/Plan_Maestro_Programacion.md`). ⛔ **Lo declara la campaña, lo mueve Brian** —
`rules/rule-product-authority.md` §2.3 obliga a leerlo antes de juzgar cualquier pieza.

⭐⭐ **LA VARA DE ESTA CAMPAÑA — decidida por medición, no por opinión** (`rules/rule-product-authority.md` §2):
ni el Grafo Maestro ni el código. **El GATE DE LA FASE EN CURSO.**

| Vara | Veredicto medido el 12-ago | ¿Sirve? |
|---|---|---|
| El Grafo **completo** (el destino, Fase 5) | **15 de 15 tablas ausentes** · **24 hallazgos** | 🔴 declara en rojo un sistema que corre a diario |
| El código como autoridad | todo verde por definición | 🔴 no mide nada |
| ⭐ **El gate de la fase en curso** | **pasa 6 de 6** · **4 hallazgos** que importan hoy | ✅ **discrimina y es accionable** |

⚠️ **Los otros 20 no eran falsos: eran PREMATUROS** — y un hallazgo prematuro se ve idéntico a uno
urgente, así que entierra a los que sí importan.

⛔ **Lo que NO se audita hoy:** Output Gate · Auth/RBAC · Prometheus · Amígdala · Event Sourcing ·
schema-per-tenant. **Son Fases 4-5 del plan** — se registran como ⬜ FUTURO, no como hallazgo
(`rules/rule-product-authority.md` §2.4).

**Los 4 que importan hoy, y caen en los 4 primeros bloques:**
🔴 **H-01** contenido en claro (`seguridad`) · 🟠 **H-02** el contador no cuenta lo importado
(`memoria`) · 🔴 **H-04** digest muerto 29 días (`cerebro`) · 🔴 **H-03** instancia huérfana
(`despliegue`).

⚠️ **Lo demás (Output Gate · RBAC · Prometheus · Amígdala) es Fase 4-5: NO es deuda de hoy.**

⭐ **EL TERRENO, MEDIDO — `AUDITORIA-FOR3S-OS-2026-08.md` (aquí mismo, en la campaña).** 35 pasadas sobre el
servidor: los 12 componentes, los 4 canales reales, **24 hallazgos con evidencia** y **14
fortalezas que NO se rompen**. Nace de la orden de Brian (2026-08-12): *"que sirvan como
referencia para la campaña, que no vamos a ciegas"*. ⛔ Aporta HECHOS, nunca criterio: la autoridad
sigue siendo el Grafo Maestro.

⭐ **LA MEMORIA — `AUDITORIA-MENTE-OS-CONOCIMIENTO.md` (aquí mismo).** 332 documentos y 109,377
líneas de Mente OS destilados: **las 5 familias de error**, las 12 autopsias de sesión, los 30
ADRs, la lección medida de cada bloque cerrado y **20 lecciones** que la campaña lleva puestas.
Brian, 12-ago: *"nos servirá para saber qué pasó antes y no cometer algún error"*.

**La deuda, medida** (`memory/pendiente-agosto-2026.md`): **74 pendientes** → 🔴 **4 urgentes**
(bugs PR4-A · seguridad · decay de memoria · GitHub MCP) · 🟠 14 · 🟢 **52 pausados por decisión
de Brian**. ⭐ **Pausado ≠ olvidado:** cada uno declara desde cuándo se arrastra.

**El orden que no se altera:** primero For3s OS queda bien, línea por línea, y se sabe que lo escrito
**se ocupa de verdad**. **Después** —y solo entonces— Mente OS v2 entra dentro sustituyendo al v1.

## Channel

| hecho | lo aporta | lo necesitan | fecha |
|---|---|---|---|

⬜ Vacío a propósito: se llena cuando un bloque necesite un hecho de otro. ⛔ El canal **no relaja**
`rules/rule-isolation.md` §1 — permite leer el HECHO ya redactado, nunca los archivos del hermano.

## Closing

(pending — la campaña acaba de abrirse)
