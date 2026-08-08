# 🗺️ PLAN · V2-3 — la frontera motor/instancia debe VERSE en el árbol
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-3
**Orden:** 2 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`) — se desbloquea al cerrar V2-1
**Depende de:** V2-1 (la arquitectura declara cuál es el árbol objetivo)
---

## Purpose

Que un clon **vea** qué es motor y qué es instancia mirando el árbol, en vez de tener que aprenderlo
leyendo documentación.

---

## 1 · EL ESTADO REAL — medido 2026-08-08

**14 carpetas en la raíz de `Mente/`**, mezcladas sin ninguna marca que las separe:

| Carpeta | Qué es |
|---|---|
| `bin/` `hooks/` `rules/` `principles/` `templates/` | 🔧 **MOTOR** — universal, se clona tal cual |
| `Cerebro/` `memory/` `secrets/` `work/` `vision/` `blocks/` `bridges/` | 🏠 **INSTANCIA** — de Brian |
| `docs/` | ⚠️ **MEZCLADA** — contratos del motor + bitácoras de esta instancia |
| `Maestro/` | otro repo (sub-repo con su propio `.git`) |

🔴 **El hallazgo que destapó escribir este plan:** la definición de la frontera —*"el ENGINE es
universal y se clona tal cual; la instancia es tuya"* (Brian, 2026-07-31)— **vive en el docstring de
`bin/mente_config.py`**. No está en `mente.config.yml`, ni en `CAPABILITIES.md`, ni en el árbol.
⭐ **Una frontera que solo existe en un comentario de código es una frontera que nadie consulta.**

---

## 2 · POR QUÉ IMPORTA, Y POR QUÉ NO ES URGENTE

**Importa:** un dueño nuevo no sabe qué puede editar. `blk-separacion-motor-instancia` ya demostró
(2026-08-07) que **mover archivos NO era lo que hacía falta** — lo que fallaba eran los checks que
los interrogaban mal, y eso ya está corregido. Lo que queda es que la línea **se vea**.

**No es urgente:** el sistema funciona hoy sin ella. Un clon ajeno saca **197/1** y ese 1 es la
respuesta correcta. Esto es legibilidad, no corrección.

---

## 3 · EL TRABAJO — 2 pasos, y el primero puede bastar

### Paso 1 · DECLARAR la frontera donde se consulta (barato, reversible)

**Archivos de referencia** (no ley): `mente.config.yml` · `CAPABILITIES.md` · `piezas.tsv`.

Que `mente.config.yml` liste explícitamente qué carpetas son motor y cuáles instancia, y que
`bin/mente_config.py` **lea esa declaración** en vez de llevarla en su docstring. La línea pasa de
comentario a **dato consultable por cualquier validador**.

### Paso 2 · MOVER, solo si el paso 1 no basta 🙋 decisión de Brian

Agrupar en `engine/` e `instance/`. ⛔ **No se hace sin decidirlo:** rompe **55 citas** al menos
(las de la arquitectura) y `blk-separacion-motor-instancia` ya midió que **ninguno de los 221
archivos estorbaba**. Mover por estética repite el error que ese bloque evitó.

---

## 4 · CÓMO SE VERÍA FALLAR

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Declarar `bin/` como instancia en el config | un check debe **negarse**: el motor no puede ser instancia |
| 2 | Añadir una carpeta nueva sin clasificar | debe avisar: *"carpeta sin declarar de qué lado está"* |
| 3 | Borrar la declaración del config | `mente_config` debe fallar ruidosamente, **nunca asumir un valor por defecto** |

⭐ **El 3 es el que importa:** una frontera que se auto-completa en silencio deja de ser una
frontera. `principles/owner-3-validation.md`: *fallar ruidosamente*.

---

## 5 · QUÉ CHECK LO VIGILA DESPUÉS

**Toda carpeta de la raíz está declarada de un lado o del otro.** Sin él, la carpeta 15 nace sin
clasificar y la frontera se erosiona sola — que es exactamente cómo llegó a estar mezclada.

---

## 6 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No mueve nada sin decisión explícita de Brian** (paso 2).
- ⛔ **No toca `Cerebro/`** — es el producto For3s OS, no la instancia de Mente OS.
- ⛔ **No parte `docs/`** aunque esté mezclada: separarla es otro pendiente y arrastra citas.

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` · `docs/plans/PLAN-V2-1-arquitectura.md` (lo desbloquea) ·
`blocks/archive/separacion-motor-instancia_2026-08/SUMMARY.md` (por qué mover no era la cura) ·
`bin/mente_config.py` (donde hoy vive la frontera, y no debería).
