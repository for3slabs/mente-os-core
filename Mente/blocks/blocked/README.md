# blocks/blocked/ — los bloques que esperan a alguien
**Status:** current · **Type:** contract · **Updated:** 2026-08-07 · **Owner:** brian

## Purpose

Dónde vive un bloque que **no puede avanzar** porque espera un dato, una decisión o un permiso
que su dueño no tiene. Existe para que "bloqueado" sea un ESTADO con sitio propio, no un bloque
activo que lleva semanas sin moverse.

> 🔴 **Este archivo existe por una razón mecánica, no decorativa:** git **no versiona
> directorios vacíos**. El directorio estaba en la máquina de Brian y el check
> `blocks/blocked/ exists` pasaba aquí — pero **en cualquier clon salía en rojo**, porque nunca
> viajaba. Medido el 2026-08-07 clonando el repo: era 1 de los 21 fallos.
>
> ⭐ Un directorio que solo existe donde se creó no es parte del sistema: es parte de esa
> máquina.

---

## 1 · Cuándo entra un bloque aquí

Cuando su §E declara un `blockers:` que **nombra a quién puede levantarlo** y esa persona no es
quien está trabajando. `rules/block-lifecycle.md` §5 lo dice: *un blocker sin dueño no es un
blocker, es un bloque abandonado*.

```markdown
## State
status: blocked
blockers: sub-bloque 5 depende de decidir el hosting → BRIAN
```

## 2 · Cómo sale

- **Se desbloquea** → vuelve a `blocks/active/`.
- **Se cierra sin hacerlo** → va a `blocks/archive/` con su §K explicando por qué no se hizo.
  ⛔ Nunca se borra: una decisión de no hacer algo es información, igual que hacerlo.

⚠️ `bin/flag-stale` marca un bloque que lleva **14 días** bloqueado. No lo mueve — avisa, porque
un bloqueo que nadie revisa deja de ser un bloqueo y pasa a ser un olvido.

---

Related: `rules/block-lifecycle.md` §5 (cuándo se bloquea y quién lo levanta) ·
`rules/contract-block.md` (los campos del §E) · `bin/flag-stale` (el que avisa).
