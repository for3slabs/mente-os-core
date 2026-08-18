# hallazgos/ — un archivo por BLOQUE × FASE

**Status:** current · **Type:** analysis · **Updated:** 2026-08-12 · **Owner:** brian

## Purpose

Lo que sale de cada bloque en cada corrida. **El nombre del archivo ES la ruta de búsqueda.**

```
<bloque>-fase-<n>.md   →   seguridad-fase-1   ·   memoria-fase-2
```

## Qué contiene cada archivo

Los **dos niveles de veredicto** que `docs/plans/PLAN-3-fases.md` §3 exige:

1. **Por nodo (o pieza)** — 4 respuestas medidas, cada una con su comando
2. **Por bloque** — el veredicto agregado + los hallazgos con su gravedad
3. **🟠 Deuda que crece** — sección aparte, con dos medidas (`docs/plans/PLAN-3-fases.md` §4.1)
4. **⬜ Ausente por fase** — lo de fases posteriores, que no cuenta ni detiene
   (`rules/rule-product-authority.md` §2.4)

## ⭐ Esta carpeta se prueba VIVA por su USO, no por su existencia

⚠️ **Brian, 2026-08-12:** *"verificar que realmente se esté ocupando y no sea un proceso zombie."*

`bin/check-campaigns` lo hace medible:

| Situación | Veredicto |
|---|---|
| carpeta vacía + todos los bloques en fase 1 | 🟢 **correcto** — nadie ha terminado una fase todavía |
| un bloque en fase **≥2** sin su archivo de la fase anterior | 🔴 **saltó una fase** |

⭐ **Una carpeta vacía no es un zombie si nadie ha llegado aún.** Lo que delata al zombie es un
bloque que dice haber avanzado **sin dejar el archivo que lo prueba.**

---

Related: `docs/plans/PLAN-3-fases.md` §6 · `rules/contract-block.md` (el campo `campaign_phase`) ·
`campaigns/producto-for3s-os/CAMPAIGN.md`.
