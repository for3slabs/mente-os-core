# CAMPAIGN · producto-for3s-os

id: cmp-producto-for3s-os-2026-08
status: active · owner: brian
created: 2026-08-10 · updated: 2026-08-10

## Mission

Llevar **For3s OS de MVP que funciona a PRODUCTO que se puede usar**. No se desarrolla nada nuevo:
se **limpia, valida, prueba y verifica** lo que ya existe, con Mente OS v2 como herramienta.

> **Brian, 2026-08-10:** *"Sabes que funciona, ahora nos toca limpiar, validar, probar y volverlo
> un producto."* · *"No es algo que 5 personas lo tendrán, va a ser para miles de millones."*

**Termina cuando:** el código pasa las 6 dimensiones de QA **con la vara de producto**, y Brian
confía en delegarle trabajo — el Frente E que el Incubathon dejó abierto.

## Authority

⭐ `Cerebro/For3s_OS_Grafo_Maestro.md` — **CÓMO FUNCIONA** · las rondas — **CON QUÉ** · el código
**se AUDITA, no manda**. Orden completo: `rules/rule-product-authority.md`.

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
| orquestacion-multiagente | el vocabulario multi-agente que v2 no tiene | blocked |

⬜ **Los demás los decide Brian.** El número es **dinámico** (`rules/contract-campaign.md` §2):
sale del trabajo, no del formulario. Se declara uno para abrir; crece según la misión lo pida.

⭐ **EL MÉTODO, aprobado 2026-08-11:** 3 fases sobre el mismo código con distinta mirada
(nodos → carpetas → flujos), **más una 4ª de COMPORTAMIENTO que va PARTIDA**: declarar las
fronteras **antes** de la fase 1, e instrumentar **después** de las tres.
👉 `docs/plans/PLAN-fase-comportamiento.md` — nace del barrido medido en el servidor: de 76
archivos, **solo 6 miden su tiempo**, y el camino del agente (`agent` · `tool_loop` · `multiagente`)
mide **cero**. Lo que se cobra está medido; lo que se usa, no.

## Shared context

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

**Por qué existe esta campaña.** El Incubathon destapó fallos de sistema y de lógica, y la
conclusión de Brian no fue *"arreglo esos"* sino ⭐ ***"si estoy viendo esto, ¿cómo estará lo que se
construyó?"***. Por eso primero se verifica y no se construye.
El sentimiento de fondo, documentado el 13-jul: *"For3s es un chat que contesta y guarda memoria"*
— y el diagnóstico que Brian confirmó: **no vale poco; se usó como TUBO y nunca devolvió valor.**

**La deuda, medida** (`memory/pendiente-agosto-2026.md`): **74 pendientes** → 🔴 **4 urgentes**
(bugs PR4-A · seguridad · decay de memoria muerto · GitHub MCP roto) · 🟠 14 · 🟢 **52 pausados por
decisión de Brian**.

**El orden que no se altera:** primero For3s OS queda bien, línea por línea, y se sabe que lo escrito
**se ocupa de verdad**. **Después** —y solo entonces— Mente OS v2 entra dentro sustituyendo al v1.

## Channel

| hecho | lo aporta | lo necesitan | fecha |
|---|---|---|---|

⬜ Vacío a propósito: se llena cuando un bloque necesite un hecho de otro. ⛔ El canal **no relaja**
`rules/rule-isolation.md` §1 — permite leer el HECHO ya redactado, nunca los archivos del hermano.

## Closing

(pending — la campaña acaba de abrirse)
