# CONNECTIONS · blk-separacion-motor-instancia-2026-08
**Status:** current · **Type:** analysis · **Updated:** 2026-08-07 · **Owner:** brian

## Purpose

Qué otro trabajo queda afectado por este bloque, para que quien lo lea después sepa dónde
propagó — y dónde deliberadamente no.

---

## Afectado

| Qué | Cómo |
|---|---|
| `bin/init` | ahora **poda** los `additionalDirectories` muertos y **genera** `docs/WORKSPACE.md`. Cualquier cambio en el arranque de una instancia pasa por él |
| `docs/WORKSPACE.md` | **sale del repo**: es un documento de instancia, se genera. Ya no viaja con el motor |
| `bin/test-f0-f6` | los checks de instancia se saltan lo ausente en 🟡 en vez de fallar. Cambió el significado de un rojo en un clon |
| `bin/check-links` | un repo hermano ausente ya no es cita rota (12 → 0 en el clon) |
| `bin/check-structure` | `owner == "Maestro"` hardcodeado, corregido |
| `hooks/pre-edit-standards.py` | el matcher pasó de subcadena a SEGMENTOS de ruta, y solo lee el tramo anterior al guion largo. **Afecta a qué estándares recibe el editor en TODOS los bloques** |
| `rules/rule-checks-must-measure.md` §D | la familia D creció con los casos 5-8, medidos aquí |
| `memory/PENDIENTES.md` | recibe la deuda de `grade-block` (ver abajo) |

## NO afectado, y es deliberado

- **`Mente/Cerebro/`** — es el grafo del producto For3s OS, no la instancia de Mente OS. El §B
  lo prohibía explícitamente.
- **La historia de git** — Brian, 2026-08-07: **opción C, no A ni B.** Partir la historia se paga
  una vez y no se deshace. El tradeoff aceptado por escrito: el repo público seguirá conteniendo
  la instancia hasta que se decida A.
- **`marca-personal/`** — otro repo, y el bloque solo lo nombró para decir de quién NO era. Esa
  mención destapó el bug del hook, pero el bloque no tocó nada ahí.
- **`blk-demo`** — su §C lo declaraba como dependiente por los `§F import counts`, que eran 1 de
  los 7 rojos del clon. **Resuelto sin tocar el bloque `demo`**: el check dejó de exigirlos.

## Lo que queda abierto para otros

1. ⭐ **Prueba de campo por un tercero** — cero instalaciones externas verificadas. Sin eso, lo
   que se midió es el mecanismo, no la experiencia de otro dueño.
2. **`bin/grade-block` no puede medir un bloque cuyo scope son ARCHIVOS sueltos** —
   `infra_evidence()` recorre directorios, así que `runbook`/`rollback` salen 🔴 aunque el
   documento exista. 🙋 Decisión de Brian: cambiar cómo se puntúa afecta a todos los bloques ya
   calificados. Registrado en `memory/PENDIENTES.md`.
3. **La separación real** (opción A, motor publicable en limpio) — otro bloque, después de éste.

---

Related: `blocks/archive/separacion-motor-instancia_2026-08/SUMMARY.md` ·
`blocks/archive/separacion-motor-instancia_2026-08/BLOCK.md` ·
`rules/rule-checks-must-measure.md` · `memory/PENDIENTES.md`.
