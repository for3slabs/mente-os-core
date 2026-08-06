# CONNECTIONS · blk-distribucion-2026-08
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian

## Purpose

Qué otro trabajo queda afectado por este bloque, para que quien lo lea después sepa dónde
propagó — y dónde deliberadamente no.

---

## Afectado

| Qué | Cómo |
|---|---|
| `bin/init` · `templates/` · `CAPABILITIES.md` | **nacieron aquí**. Cualquier cambio en el arranque de una instancia pasa por ellos |
| `.claude/settings.json` | 24 reglas `ask` portables sobre `$CLAUDE_PROJECT_DIR` — sustituyeron 3 rutas absolutas |
| `bin/test-f0-f6` | se le quitó `-home-brianweb3-for3s` hardcodeado: **el motor viajaba con la identidad de un usuario** |
| `memory/PENDIENTES.md` §🚪 | este bloque es el mecanismo que cierra ese pendiente documental |

## NO afectado, y es deliberado

- **`blk-demo`** — vive en `marca-personal/`, otro repo. Ninguna pieza declarada en ambos §B
  (`rules/rule-isolation.md`).
- **`Mente/Cerebro/`** — es el grafo del producto For3s, no el motor. Su §B lo prohibía.

## Lo que queda abierto para otros

1. **Prueba de campo por un tercero** — el clon lo probó la IA en esta máquina.
2. **2 decisiones de Brian**, sin cambios: firma GPG · `~/.claude.json` (el `deny` lee el TEXTO del
   comando, así que `"$(ls …)"` lo esquiva — **no es un sandbox**).

---

Related: `blocks/archive/distribucion_2026-08/SUMMARY.md` · `blocks/archive/distribucion_2026-08/BLOCK.md` · `rules/rule-isolation.md` ·
`memory/PENDIENTES.md`.
