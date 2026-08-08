# 🗺️ PLAN · V2-5 — limpieza de configuración
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-5
**Orden:** 6 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`) — 🟢 lo urgente se ejecutó el 27-jul
---

## Purpose

Cerrar el barrido de fondo de los permisos. **Lo que dolía ya está hecho**: `blk-distribucion`
convirtió 3 rutas absolutas en **24 reglas portables** sobre `$CLAUDE_PROJECT_DIR`, que era el daño
real (un clon nacía sin ninguna puerta viva, **en silencio**).

---

## 1 · EL ESTADO REAL — medido 2026-08-08

| Archivo | allow | deny | ask |
|---|---|---|---|
| `.claude/settings.json` (compartido) | **45** | **185** | **58** |

**El aviso vivo de `check-health`:** *"317 allow entries — granularity should be the mechanism, not
the invocation"* (`rules/rule-config-hygiene.md` §1.3).

🔴 **El hallazgo que destapó escribir este plan:** el aviso dice **317** y el archivo compartido
tiene **45**. Los otros ~272 están en `settings.local.json`, que **no viaja**. ⭐ **El validador suma
dos archivos y reporta un número que no corresponde a ninguno** — quien lea "317" y abra el
compartido no entiende nada.

⚠️ Y la asimetría es **a propósito**, ya decidida: `rules/rule-config-hygiene.md` §1.6 — *"`deny` vive en
los DOS archivos, `allow` no"*. Medido el 31-jul: 16 allow compartidos vs 199 locales. El aviso
castiga una decisión ya tomada.

---

## 2 · EL TRABAJO — 2 pasos, y el primero cambia el segundo

### Paso 1 · Que el aviso diga QUÉ archivo mide

**Archivos de referencia** (no ley): `bin/check-health` · `rules/rule-config-hygiene.md` §1.3 y §1.6.

Separar el conteo: *"45 en el compartido · 272 en el local"*. ⭐ **Un número agregado sobre dos
archivos con reglas distintas no es medir: es promediar cosas que no se comparan.**

### Paso 2 · Reducir de verdad, si tras el paso 1 sigue habiendo exceso

`allow` por **mecanismo**, no por invocación: una entrada que autoriza `bin/check-*` en vez de once
que autorizan cada validador.

---

## 3 · CÓMO SE VERÍA FALLAR

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Añadir 50 `allow` al compartido | el aviso debe subir y **nombrar el archivo compartido** |
| 2 | Añadir 50 al local | ⚠️ **hoy sube el mismo número** — el defecto que el paso 1 corrige |
| 3 | Borrar un `deny` de seguridad | 🔴 debe fallar: los `deny` son la superficie protegida, no cosmética |

---

## 4 · QUÉ CHECK LO VIGILA DESPUÉS

**El conteo se reporta por archivo, nunca sumado.** Sin eso, la próxima vez que alguien lea "317"
volverá a buscarlos en el sitio equivocado.

⚠️ El umbral es un **aviso, nunca un error**: cuántos permisos son demasiados es criterio de Brian
(ADR-003), y un validador que lo decida solo estaría inventando la política de seguridad.

---

## 5 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No toca los `deny`.** 185 reglas son la superficie protegida; quitar una es una decisión de
  seguridad, no limpieza.
- ⛔ **No unifica `allow` entre compartido y local.** La asimetría está decidida (§1.6).
- ⛔ **No toca `~/.claude.json`** — es otro pendiente (E-3) y es arquitectura, no configuración.

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` · `rules/rule-config-hygiene.md` §1.3 y §1.6 ·
`bin/check-health` (quien emite el aviso) · `blocks/archive/distribucion_2026-08/` (lo ya hecho).
