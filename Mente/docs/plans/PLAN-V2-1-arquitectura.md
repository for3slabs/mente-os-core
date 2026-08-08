# 🗺️ PLAN · V2-1 — la arquitectura no se parte, se declara
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-1
**Orden:** 1 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`) — es lo único que bloquea a otro (V2-3)
**Decisión de Brian, 2026-08-08:** declararla **fuente de verdad**; NO se parte
---

## Purpose

Cerrar V2-1 sin partir `docs/Arquitectura_Mente_OS_v2_Bloques.md`, y **arreglar el defecto real que
la medición destapó**: la exención ya está escrita y **un validador la respeta mientras otro no**.

---

## 1 · EL ESTADO REAL — medido 2026-08-08, no supuesto

| Qué | Medido |
|---|---|
| Tamaño del archivo | **2,471 líneas** (techo de `architecture`: 800) |
| Documentos que lo citan | **55** |
| Excepción en su cabecera | ✅ **YA ESCRITA** — `**Exempt:** size, split-signal` con su razón |
| `bin/check-blocks` | ✅ la **respeta** — no avisa |
| `bin/check-health` | 🔴 la **ignora** — sigue avisando *"2471 lines — over the architecture limit of 800"* |

> ⭐ **El pendiente estaba desfasado.** Decía *"partir la arquitectura"*; el trabajo real que queda
> es **cablear la exención en el segundo validador**. Escribir el plan es lo que lo destapó.

---

## 2 · POR QUÉ NO SE PARTE — la decisión, con su evidencia

`principles/expertise/doc-structure.md` §2.1 abre una excepción para una **fuente de verdad**: el
documento que otros citan **para RESOLVER una discusión**, no para consultar. Aquí lo citan 55.

🔬 **Y ya se intentó partir:** julio, `blk-split-architecture`. Resultado hoy: **74% duplicado**
entre las mitades, con **330 líneas viviendo solo en el original**. **La partición creó la
divergencia que debía evitar** — el mismo defecto que la excepción existe para prevenir.

⛔ **La excepción no es una puerta trasera:** obliga a nombrar QUÉ se exime y POR QUÉ, queda en el
diff, y **no cubre errores** — solo avisos de forma. Un `red()` nunca se exime.

---

## 3 · EL TRABAJO — 2 pasos

### Paso 1 · `check-health` debe leer `Exempt:` igual que `check-blocks`

**Archivos de referencia** (punto de partida, **no ley**): `bin/check-health` (~línea 385, el bucle
de `LIMITS`) · `bin/check-blocks` (~línea 69, `exenciones()` e `is_exempt()` ya escritas).

⭐ **No se duplica la lógica:** `check-blocks` ya sabe leer la cabecera. Copiar el regex a un segundo
archivo crea dos verdades que divergen — que es exactamente lo que este pendiente combate. **La
lectura de `Exempt:` debe vivir en UN sitio** y ambos validadores usarlo.

### Paso 2 · Cerrar el pendiente con su evidencia

`check-health` deja de avisar por este archivo, y **sigue avisando** por cualquier otro que rebase
su techo sin exención declarada.

---

## 4 · CÓMO SE VERÍA FALLAR — el sabotaje que da valor al verde

`principles/expertise/val-functional.md` §2.2: *un check debe verse fallar antes de que su verde
signifique algo.* Tres pruebas, en este orden:

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Quitar `**Exempt:**` de la cabecera de la arquitectura | `check-health` **vuelve a avisar** |
| 2 | Restaurarla | el aviso desaparece |
| 3 | Añadir `Exempt:` a un archivo cualquiera que rebase su techo | ⚠️ **debe seguir avisando** de los DEMÁS defectos: la exención cubre tamaño, no todo |

⛔ **El paso 3 es el que importa.** Una exención que perdona de más es tan defecto como el aviso
falso que corrige — medido esta semana con la exención de tests en `grade-block`.

---

## 5 · QUÉ CHECK LO VIGILA DESPUÉS

Un check en `bin/test-f0-f6`: **los dos validadores de techo coinciden sobre el mismo archivo.**

**Por qué hace falta y no basta con arreglarlo:** el defecto no fue que nadie escribiera la
exención — fue que **dos validadores leyeron el mismo archivo con criterios distintos y nadie los
comparó**. Sin este check, el próximo validador que mida tamaños vuelve a nacer sordo.

---

## 6 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No parte el archivo.** Decisión tomada, con la evidencia del intento de julio.
- ⛔ **No toca `docs/architecture/`** — las mitades de julio siguen ahí con su 74% duplicado. Es
  **otro pendiente**, no este: consolidarlas o borrarlas necesita decidir cuál manda, y eso es
  criterio de Brian.
- ⛔ **No sube el techo de 800.** Subirlo eximiría a todos en silencio; la exención declarada dice
  QUIÉN y POR QUÉ.

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` (el orden) · `principles/expertise/doc-structure.md` §2.1
(la excepción) · `docs/Arquitectura_Mente_OS_v2_Bloques.md` (el archivo) ·
`principles/expertise/val-functional.md` §2.2 (verse fallar antes de creerle).
