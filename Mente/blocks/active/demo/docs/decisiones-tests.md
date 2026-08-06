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

- ⭐ 2026-08-05 · **§F-12 CERRADO: `agentOn` deja de ser estado local y pasa a ser la prop.**
  El error (*setState síncrono en un effect → renders en cascada*) no era estilo: el componente
  **copiaba** `agentOn` a un `useState` y un `useEffect` la resincronizaba en cada latido —
  contradice `dev-frontend.md` §2 (**el servidor es dueño del estado**) y creaba un segundo valor
  que podía divergir. Verificado en la raíz antes de tocar: la verdad llega del heartbeat
  (`GeneralExperience.tsx:53` → `DemoShell` → la prop). El tránsito ("Encendiendo…") se **deriva
  del render**, así que el interruptor sigue sin mentir (el fix del 26-jul se conserva).
  📊 **eslint 5 problemas/1 error → 3/0** · `tsc` exit 0 · tests idénticos. 🔬 Los 6 puntos de
  `setBusyAgent` se conservan uno a uno: el botón no cambió, solo desapareció la copia.
- ⚠️ 2026-08-05 · **`kind` sigue en el contrato de `ProfilePanel`, sin desestructurar.** Sin uso
  desde que S4a la sustituyó por `esPago`. ⛔ No se retira del tipo (`DemoShell` la pasa: sería un
  cambio de API), ni se usa `_kind` (esta config de eslint no ignora el guion bajo y **no se toca
  `eslint.config.mjs` por un aviso**). No desestructurarla resuelve ambas sin tocar nada más.
- ⚠️ 2026-08-05 · **1 error de eslint PREEXISTENTE en `ProfilePanel.tsx`** (setState síncrono dentro
  de un effect → renders en cascada). Verificado contra HEAD: viene del commit `9c756e2` y este trabajo
  no lo tocó. **No se arregla aquí** — está fuera del sub-bloque 10; queda como §F-12.

- 🔬 2026-08-06 · **El test de ② pasó de puro a INTEGRACIÓN, y eso ES la mejora.** Antes se probaba
  sin BD porque la autorización vivía en una constante; ahora exige Postgres porque la verdad vive
  ahí. Sus 5 tests se suman a los saltados hasta la rama de Neon (§B1). ⚠️ **Menos verdes no siempre
  es peor**: el que se perdió medía un `DEV_FALLBACK` que no debería existir.
- ⚠️ 2026-08-06 · **jazz/mashe retiradas de 5 listas del código, cada una por su razón.**
  `INSTANCIAS_SEMILLA` es el fallback si Neon cae (degradar a una instancia borrada sería peor que
  no degradar) · `INSTANCIAS` valida el panel admin · `OAUTH_KINDS` sigue FIJA a propósito, ahora
  con solo `brian` · `accounts.ts` llevaba **tokens de dev en claro** para instancias que ya no
  existen: una credencial suelta, no compatibilidad. En la BD quedaron **inactivas, no borradas**
  (UPDATE reversible).

---

Related: `blocks/active/demo/BLOCK.md` §F-8 · `blocks/active/demo/docs/como-correr-los-tests.md`
(cómo se ejecutan) · `blocks/archive/plan-tests-demo_2026-08/docs/plan-critical-paths.md` (el plan).
