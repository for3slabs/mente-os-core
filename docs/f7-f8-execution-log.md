# F7 + F8 · execution log

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Phases:** F7 (generate) · F8 (second pilot) · **Plan:** `docs/plan-v2-rollout.md`
---

## Purpose

What actually happened when F7 and F8 ran. The plan says what they ARE; this says what they DID.
Split out on 2026-07-30 when the plan crossed its 400-line limit — two distinct things in one file
(ADR-027). **Moved, not trimmed.**

## F7 · GENERAR — el índice que no puede mentir

✅ **CERRADO 2026-07-30.**

| Ticket | Resultado |
|---|---|
| **F7-1** | `bin/generate-index` → `docs/INDEX.md` — 257 documentos por carpeta |
| **F7-2** | `docs/STATES.md` — cada bloque con estado, carril, progreso, dueño y **salud MEDIDA** |
| **F7-3** | `memory/archive/README.md` marcado superseded (enrutaba por el criterio pre-v2) |

**Criterio de cierre — *"el índice se regenera solo y refleja la realidad"*:** ✅ `--check` sale 0
cuando está al día, 1 cuando no, y **caza una edición a mano**.

### ⭐ Cerró la mentira más cara del sistema

`Maestro/registro.md` afirmaba **173 docs cuando había 257** — y Foresito lo lee EN VIVO por MCP,
así que servía números falsos a producción. Llevaba meses así porque **nadie lo generaba**.

No se corrigió el número a mano: se le puso el valor medido **más la razón** de por qué ese campo
se mide y no se recuerda.

> **Un índice a mano no envejece ruidosamente. Envejece en silencio y se sigue leyendo como verdad.**

---

## F8 · SEGUNDO PILOTO — bloque nuevo desde cero

✅ **F8-1 · F8-2 · F8-3 CERRADOS 2026-07-30** con `blk-split-architecture-2026-07`.
⬜ **F8-4 pendiente** — solo lo puede ejecutar la sesión SIGUIENTE.

### El resultado

Arquitectura de **2496 → 632 líneas**. 5 piezas nuevas, todas bajo su límite de 800.
**Cero líneas perdidas, verificado tras cada uno de los 5 cortes.** Veredicto **🟢 PRODUCT**.
Primer bloque cerrado y archivado del sistema.

### ⭐ Lo que un segundo piloto sirve para encontrar

La demo se migró CON su historia, así que nunca ejercitó el minuto cero. Este sí — y encontró:

| Hallazgo | Por qué importa |
|---|---|
| 🔴 **La contraseña SSH real de Brian** en la arquitectura desde el 27-jul, dentro de un ejemplo de *"qué NO hacer"* | Sobrevivió a toda auditoría porque **ningún validador medía ese archivo**. Una contraseña dentro de un mal ejemplo sigue siendo una contraseña |
| **El carril que el scaffold adivinó estaba mal** | Puso `direct`; medido eran **46 dependientes** = `full-block`. El carril se mide, no se supone |
| `grade-block` no contaba archivos sueltos en el scope | Reportaba `NOTHING MEASURED` midiendo bien |
| `rules/contract-archive.md` no decía que sus archivos llevan cabecera | Lo descubrió **el primer cierre real**, no la teoría |

### La lección de la partición

⭐ **El sufijo `-BIS`/`-TER` nunca fue un capricho de nombres — era el archivo diciendo que contenía
dos cosas distintas.** Las 12 secciones crecidas mapearon **exactamente** sobre los cortes. Al
volverse cada grupo su propio archivo, los sufijos dejaron de significar algo y se renumeraron:
conservarlos habría sido guardar la cicatriz de un problema ya resuelto.

**Un puntero en el lugar vence a un borrado:** cada sección extraída dejó un stub diciendo a dónde
fue y por qué, así los 46 documentos que citan la entrada siguen resolviendo sin una sola edición.

---

> ✅ **F4 CERRADO 2026-07-30.** Y con él los 3 validadores que faltaban del diseño:
> `bin/grade-block` · `bin/flag-stale` · `bin/check-sufficiency`.
>
> **El veredicto real de la demo: 🔴 MVP.** Dos rojos: `ConnectClaude.tsx` (145 líneas, 0
> importadores, desde el 16-jun) y **0 archivos de test en todo el sitio**.
> Escrito en `blocks/active/demo/BLOCK.md` §G-BIS, **reproducible con un comando.**
>
> ⭐ **Esto es lo que Brian pedía desde el principio:** la respuesta a *"¿es producto o MVP?"* con
> números que no cambian con el `/clear`.

---

Related: `docs/plan-v2-rollout.md` · `docs/f4-execution-log.md` · `docs/f5-execution-log.md` ·
`docs/f6-execution-log.md` · `blocks/archive/split-architecture_2026-07/SUMMARY.md`.
