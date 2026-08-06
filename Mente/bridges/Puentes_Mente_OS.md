# 🌉 Puentes entre Mentes OS — Registro de apuntadores

**Status:** current · **Type:** rule · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Puentes_Mente_OS.md → bridges/Puentes_Mente_OS.md (2026-07-30, ADR-029)

## Purpose

🌉 Puentes entre Mentes OS — Registro de apuntadores


> **Capa de comunicación UNILATERAL y CONTROLADA entre distintos Mente OS.**
> Este Mente OS (For3s OS) puede *apuntar* a otros Mente OS externos, pero **NO los
> integra** — leerlos consume tokens, y el consumo se dispara si se leen "por si
> acaso". Por eso todo acceso pasa por un **gate explícito con frase + por qué**.

---

## ⛔ REGLA DURA (protege el consumo de tokens)

**NUNCA leas otro Mente OS de esta lista salvo que Brian lo pida explícitamente con la
frase de acceso.** No lo leas "por contexto", "por si acaso" ni para "entender mejor".
Cada acceso debe tener un **por qué** declarado. Este es el punto donde el consumo se
puede elevar demasiado — y eso es lo que MENOS queremos.

- Estos Mentes OS **NO forman parte de For3s OS**. Son proyectos separados con su propia
  memoria. Trabajar EN ellos = cambiarse a su directorio; aquí solo se los *apunta*.
- La comunicación es **unilateral**: For3s OS apunta hacia afuera. El otro Mente OS no
  necesita saber de este.

---

## 🔑 Cómo se abre el puente (gate)

**Frase de apertura:** `acceder mente <nombre-del-proyecto>`
(ej. `acceder mente navigox`) — genérica y escalable: sirve para cualquier proyecto de
la lista, usando su nombre.

Al recibir la frase:
1. Confirmar el **por qué** (para qué se necesita leer ese Mente OS).
2. Abrir el puente en modo **SOLO LECTURA + reporte**: leo lo mínimo necesario de
   `<ruta>/Mente/`, reporto lo relevante, y no escribo nada allá desde aquí (para
   editar ese Mente OS, Brian se pasa a ese proyecto).

## 🚪 Cómo se cierra el puente

Se cierra por **cualquiera** de las dos vías (lo que pase primero):
- **Frase de cierre:** `cerrar mente <nombre-del-proyecto>`.
- **Auto-cierre:** al terminar la tarea para la que se abrió.

Cerrado el puente, vuelvo al modo protegido: **no vuelvo a leer ese Mente OS sin re-abrir**.

---

## 📇 Mentes OS registrados

### NavigoX
- **Proyecto:** NavigoX / Hoteleria-Incubathon (marketplace de turismo — **2º lugar
  Incubathon jul 2026**, ver `memory/Bitacora_Progreso.md` y memoria del agente).
- **Ruta del Mente OS:** `/home/brianweb3/5M-incubathon/Mente/`
- **Directorio del proyecto:** `/home/brianweb3/5M-incubathon/`
- **Repo:** github.com/ElBrAyAn1967/Hoteleria-Incubathon · Deploy: Vercel.
- **Relación con For3s OS:** consume For3s como CEREBRO por API (caja negra). For3s
  NO se entrega; se OCUPA. NavigoX ya tiene su Mente OS propio (Alma/Cerebro/Cuerpo/Doc).
- **Frase de acceso:** `acceder mente navigox` · **cierre:** `cerrar mente navigox`.
- **Estado en ESTE Mente OS:** ✅ **CERRADO.** El hito (2º lugar + validación) queda
  registrado aquí como cierre; **el trabajo de NavigoX continúa en `~/5M-incubathon/`,
  NO aquí.**

<!-- Al agregar un Mente OS nuevo: copiar este bloque, poner nombre/ruta/frase reales. -->

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `bridges/Puentes_Mente_OS.md`).
