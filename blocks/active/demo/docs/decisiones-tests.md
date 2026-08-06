# DECISIONES de los tests de los 4 caminos · bloque `demo`
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian
**Block:** `blocks/active/demo` §G · **Split:** 2026-08-05, `doc-structure.md`

## Purpose

Las decisiones del §F-8 (los tests de los 4 caminos críticos), movidas ÍNTEGRAS desde el §G cuando
el BLOCK.md pasó su techo de 200 líneas. ⛔ Nada se resumió ni se borró.

---

- ⭐ 2026-08-05 · **④ POWER: el plan apuntaba al archivo EQUIVOCADO, y medirlo antes lo evitó.**
  El plan mandaba probar `lib/demo/container.ts`; ahí **no vive la autorización** — solo encola la
  intención. La regla *"solo el dueño"* se hace cumplir en `app/api/demo/general/agent/route.ts`
  (32-39) contra `demo_duenos`. Un test contra `container.ts` habría dado **verde sin tocar la regla
  que importa**: cobertura que tranquiliza sin proteger, el peor resultado posible. Lo que sí se
  probó: el contrato del despacho asíncrono (`false` = *en camino*, nunca *hecho* — el NO-OP viejo
  fingía éxito y la UI mentía) y que la vía HTTP directa **no** esté configurada (expondría el plano
  admin tailnet-only, la opción A descartada). El 403 al invitado queda declarado en §F-8, no fingido.
- 🔬 2026-08-05 · **Mi propia sonda de ④ no discriminaba, y lo cacé al usarla.** El test de colisión
  de contenedores usaba `["jazz","mashe","brian","general"]`: un sabotaje que truncaba el nombre a
  1 carácter **no lo ponía en rojo**, porque esas cuatro ya empiezan por letras distintas. Corregido
  a pares que comparten prefijo (`brian`/`brian-2`); el mismo sabotaje ahora saca **2 tests en rojo**.
  ⚠️ **Un caso de prueba que no puede distinguir el fallo es decoración**, aunque el test pase.

---

Related: `blocks/active/demo/BLOCK.md` §F-8 · `blocks/active/demo/docs/como-correr-los-tests.md`
(cómo se ejecutan) · `blocks/archive/plan-tests-demo_2026-08/docs/plan-critical-paths.md` (el plan).
