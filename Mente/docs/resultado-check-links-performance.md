# RESULTADO · ejecución del plan de rendimiento de `check-links`
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian

## Purpose

Lo que pasó al EJECUTAR `docs/plan-check-links-performance.md`: los números medidos y los defectos
que cada fase destapó. El plan dice qué se iba a hacer; este archivo dice qué ocurrió.

⭐ **Partido del plan el 2026-08-05** porque juntos pasaban de 400 líneas, y
`principles/expertise/doc-structure.md` §2.1 (criterio de Brian, ese mismo día) dice que **un
documento sobre su techo DEBE partirse, y las mitades apuntarse**. Esta es una de las dos mitades.

---

## Resumen

| | ANTES | DESPUÉS |
|---|---|---|
| `bin/check-links` | 47.20s | **0.550s** |
| `bin/test-f0-f6` | 1m 10s | **15.6s** |
| `bin/generate-metrics` | 2m 31s | **13.5s** |

**Salida idéntica byte a byte** · mismo código de salida · batería **175/0**, igual que antes.

---

### ✅ F0 · EJECUTADA — resultado y los 2 defectos que destapó

**Sonda:** `docs/f0-probe-check-links.py` — carga las funciones REALES de `bin/check-links`
(no las reimplementa) y compara ambas estrategias. **`check-links` no se tocó.**

```
citas extraídas: 866 · no resuelven localmente: 626
   nombre desnudo (rama cara): 419 · con '/' (barata): 207

RESULTADO   same=626   diff=0
   glob (actual):  47.20s
   índice:          0.16s
   factor:         292.7x
```

#### 🔴 DEFECTO 1 — la primera versión de la sonda NO MEDÍA

Sabotée el criterio (`== 1` → `>= 1`, que es *perdonar citas ambiguas*) y la sonda **siguió dando
0 diferencias**. Causa medida: de las 419 citas desnudas **solo UNA es ambigua** (el nombre SKILL), y un
repo anterior (`.claude/`) ya la resolvía, así que la función retornaba antes.
**Un verde que no distingue los dos criterios es un verde vacío** — `principles/expertise/val-functional.md` §2.2
condición 3, aplicada a mi propia sonda. Añadida `F0-bis` con 3 nombres que **sí** discriminan.

#### 🔴 DEFECTO 2 — `glob` y `os.walk` NO ven lo mismo

`F0-bis` destapó una diferencia REAL: **`glob` no desciende a directorios ocultos; `os.walk` sí.**

```
glob ve:     44,437 archivos
os.walk ve:  46,066 archivos
diferencia:   6,036   (For3s-OS 1,590 · for3s-inter 127 · marca-personal 4,319)
```

**Consecuencia si no se hubiera detectado:** **layout** tiene 1 coincidencia visible para glob y
**2** para os.walk (la segunda en `.claude/`). El índice lo habría declarado **ambiguo** y roto una
cita que hoy se perdona. **Un cambio de rendimiento alterando el veredicto: el fallo del v1.**
✅ Corregido en la sonda podando `dn[:] = [x for x in dn if not x.startswith(".")]`.

#### ✅ Verificación final — la sonda caza el sabotaje

Con el criterio relajado a `>= 1`, F0-bis reporta:
**readme** (112 coincidencias) y **HISTORY** (21) → **el índice PERDONA, criterio roto**.
**La sonda mide en las dos direcciones.**

> ⭐ **Lo que F0 demuestra, y es más que un número:** la aceleración es viable **y** el camino
> ingenuo habría roto el validador en silencio. Los 292× solo valen porque la poda de ocultos
> está dentro.

---

### ✅ F1 · EJECUTADA — 47.20s → 0.550s (86x)

| Medición | ANTES | DESPUÉS |
|---|---|---|
| `bin/check-links` | 47.20s | **0.550s** |
| `bin/test-f0-f6` | 1m 10s | **15.6s** |
| `bin/generate-metrics` | 2m 31s | **13.5s** |

**Salida IDÉNTICA byte a byte** (`diff` sin diferencias) · exit code **0**, igual que antes.

#### 🔬 Verificado rompiéndolo, no solo viéndolo verde

| Prueba | Resultado |
|---|---|
| ¿Detecta una cita rota real? | ✅ reporta la ruta inexistente por su nombre |
| ¿**Rechaza los ambiguos**? | ✅ rechaza los dos nombres con 112 y 21 coincidencias — **el criterio `==1` se preserva** |

#### ✅ F4 · la batería §5-BIS del sistema completo — 7/7

| # | Verificación | Resultado |
|---|---|---|
| 1 | ruta de edición barata | hooks a **0.039s / 0.041s** |
| 2 | puerta del COMMIT | exit **0** con el árbol al día · **bloquea** con el índice desfasado |
| 3 | puerta del CIERRE | funciona (bloquea por sesión sin registrar, correcto) |
| 4 | la batería entera | **175 / 0 — idéntico** |
| 5 | las métricas publican lo mismo | `battery 175/0 · criterion holes 0` |
| 6 | 🔴 **el lock sigue protegiendo** | segunda corrida **RECHAZADA** · lock **liberado** solo |
| 7 | 🔴 restos de sonda | **ninguno** |

#### 🔬 F4-bis · los 3 casos límite que la primera versión NO probó

Añadidos al revisar F4 (Brian, 2026-08-05). **El hueco real: F1 se había probado SOLO en la
máquina de Brian, con los cuatro repos hermanos presentes.**

| # | Caso | Por qué importa | Resultado |
|---|---|---|---|
| 8 | Un repo hermano **que no existe** | `mente.config.yml` puede declarar un `outside` ausente en otra máquina | ✅ devuelve `{}` y sigue — **no explota** |
| 9 | La **caché** entre llamadas | si no cachea, el índice se reconstruye por cita y el arreglo no sirve | ✅ **0.243s** la primera · **0.000002s** la segunda |
| 10 | ⭐ Entorno **SIN hermanos** — CI o clon ajeno | es el escenario de la prueba de campo pendiente | ✅ funciona. Reporta 8 citas rotas, y **medido: las 8 son memorias del harness** (`project_*`), **no repos hermanos** → **F1 no las afecta**, y el CI ya las tenía exentas y nombradas |

> ⭐ **Por qué el caso 10 era el que faltaba:** un arreglo verificado solo donde vive su autor es
> un arreglo sin prueba de campo — el mismo hueco que arrastra Mente OS entero. Ahora está medido
> en el entorno donde no hay nada alrededor.

---


---

Related: `docs/plan-check-links-performance.md` (el plan que esto ejecuta — la otra mitad) ·
`docs/f0-probe-check-links.py` (la sonda de F0) · `bin/check-links` (la pieza) ·
`principles/expertise/val-functional.md` §2.2 (qué cuenta como prueba).
