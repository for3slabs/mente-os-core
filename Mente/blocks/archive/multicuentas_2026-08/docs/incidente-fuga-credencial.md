# INCIDENTE · la contraseña del servidor en un repo público

**Status:** current · **Type:** case · **Updated:** 2026-08-20 · **Owner:** brian
**Block:** `blocks/archive/multicuentas_2026-08/BLOCK.md`

## Purpose

Qué pasó, qué se hizo, **qué sigue abierto** y qué decide Brian. Se escribe porque el incidente
tiene un residuo que ningún comando cierra, y un residuo no escrito es un residuo olvidado.

---

## 1 · Qué pasó

La contraseña del servidor `for3s` vivía **en texto plano** en 4 archivos versionados de
`for3slabs/mente-os-for3s`, **un repo PÚBLICO**. 20 ocurrencias, 2 commits del historial.

Lo cazó `bin/check-accounts` — el primer validador que compara documentos contra la máquina.
⭐ Uno de los hits era una entrada de bitácora que **documentaba esta misma fuga**: al escribirla,
la copió a un archivo nuevo.

## 2 · Qué se hizo

| Acción | Verificación |
|---|---|
| Copia de seguridad doble | espejo 135/135 commits + tarball con `secrets/` |
| 20 ocurrencias redactadas | 0 en el árbol de trabajo |
| Historial reescrito (`git filter-repo`) | 0 commits, 0 blobs en local |
| Force-push tras medir 0 forks | verificado por contenido |
| 🔒 **Repo pasado a PRIVADO** | `private: true`, medido |

## 3 · 🔴 EL ERROR DE VERIFICACIÓN — la lección más cara

Reporté *"los commits huérfanos no tienen contenido servible"* tras probar la ruta
`contents/...?ref=<sha>`, que devolvía 404. **La conclusión era falsa.**

La vía real es `git/blobs/<sha>` — la que usaría cualquiera que buscase el dato:

```
21f3406eaf → 🔴 SERVIDO (135231 bytes)
877cece7b1 → 🔴 SERVIDO (17743 bytes)   ← contiene la contraseña, verificado
03f4a0663e → 🔴 SERVIDO (23216 bytes)
```

⭐ **Probé UNA vía y concluí sobre TODAS.** Un 404 en un camino no es una puerta cerrada: es un
camino cerrado. La regla que se salta: *no afirmar sin medir* — medí, pero medí lo que no era.

## 4 · ⬜ LO QUE SIGUE ABIERTO

**Los objetos huérfanos siguen en el servidor de GitHub.** No hay comando de git que los borre:
viven en su almacenamiento hasta que su recolección de basura los retire. Lo único que cambió
—y es lo que corta el acceso hoy— es que **el repo ya no es público**.

| Riesgo | Estado |
|---|---|
| Acceso anónimo a los blobs | 🔒 **cortado** — el repo es privado |
| Los objetos en el servidor de GitHub | ⬜ siguen ahí hasta su GC |
| La contraseña, ya expuesta | ⚠️ **no rotada** — decisión consciente de Brian (2026-08-20) |

## 5 · 🙋 LO QUE DECIDE BRIAN

1. **¿Volver a público?** Antes de eso conviene que GitHub Support purgue los huérfanos —
   es la única vía que los elimina de verdad. Mientras el repo sea privado, no urge.
2. **¿Rotar la contraseña?** Sigue siendo el único acto que invalida lo ya expuesto.
   Brian dijo que no es relevante para él; queda registrado como riesgo aceptado.

⛔ **Sin rotación, cerrar el repo reduce la exposición pero no la revierte:** cualquiera que lo
haya clonado mientras era público conserva el historial.

---

Related: `../BLOCK.md` · `runbook-y-rollback.md` (dónde están las copias) ·
`../../../../secrets/README.md` · `../../../../PROJECT-RULES.md` §5.
