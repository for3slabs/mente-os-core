# CÓMO SE CORREN LOS TESTS DE LA DEMO
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian
**Block:** `blocks/active/demo` §F-8 · **Verified by:** `npx vitest run` en `marca-personal/`

## Purpose

Qué hay que saber **antes** de correr o tocar los tests de la demo: por qué 8 se saltan, por qué
uno falla a propósito, y qué NO hay que hacer con ninguno de los dos. Sin esto, la reacción normal
ante la salida es equivocarse en las dos direcciones — "arreglar" el rojo y "activar" los saltados.

---

## 1 · La salida esperada HOY

```
Test Files  1 failed | 2 passed | 1 skipped (4)
     Tests  1 failed | 15 passed | 8 skipped (24)
```

🟢 **Eso es el estado sano.** Un `failed: 0` hoy significaría que alguien debilitó un assert.

| Archivo | Camino | Estado | Por qué |
|---|---|---|---|
| `tests/autorizar.test.ts` | ② autorizar | 5 ✅ · **1 🔴** | el rojo documenta un agujero ABIERTO |
| `tests/entrar.test.ts` | ① entrar | **7 ⏸️** | integración: necesita base de test |
| `tests/hablar.test.ts` | ③ hablar | 5 ✅ · **1 ⏸️** | la parte pura corre; la de BD no |
| `tests/apagar.test.ts` | ④ apagar | 5 ✅ | todo lo probable sin BD ni red |

---

## 2 · 🔴 EL ROJO NO SE ARREGLA — se cierra

```
FAIL  tests/autorizar.test.ts > 🔴 EL AGUJERO ABIERTO
  expected false, received true
```

`lib/demo/allowedEmails.ts` lleva un `DEV_FALLBACK` que autoriza `jazz@example.com` cuando falta la
variable de entorno — **un dominio que nadie controla.** El test afirma que debería rechazarse.
No se cumple, así que falla.

⛔ **Debilitar el assert lo convierte en decoración.** `val-functional.md` §2.2: *un check debe
verse fallar antes de que su verde signifique algo.* Aquí empieza rojo a propósito, y **su verde
ES la definición de cerrar el sub-bloque 7** — que necesita un dato que solo tiene Brian: quién es
dueño de jazz y de mashe.

---

## 3 · ⏸️ LOS 8 SALTADOS — y por qué saltarse es lo correcto

🔴 **Medido 2026-08-05: `DEMO_DATABASE_URL` apunta a la Neon de PRODUCCIÓN** que sirve
`for3s.vercel.app` — 4 instancias vivas, 1 verificación en curso. Un test que escribe ahí borra
filas reales.

Por eso los tests de integración leen **`DEMO_DATABASE_URL_TEST`**, y si falta **se saltan**. Nunca
caen de vuelta: un default que apunta a algo con dueño es el error registrado en
`rules/case-dangerous-default.md`.

### Para activarlos

1. Consola de Neon → **Branches** → **New branch** desde `main`.
2. La cadena de conexión va a `marca-personal/.env.test.local` (fuera de git):
   ```
   DEMO_DATABASE_URL_TEST=postgresql://…
   ```
3. `npx vitest run` — los 8 dejan de saltarse.

⭐ **La rama es lo correcto y no un rodeo:** Neon la crea al instante y a coste casi cero, y los
tests pueden escribir y borrar sin tocar nada vivo.

📧 **Ninguno manda correo.** `enviarCodigo` hace el INSERT **antes** de mirar `RESEND_API_KEY`
(`verificacion.ts:80-94`), así que sin esa key la lógica de BD se ejercita entera y cero correos
salen.

---

## 4 · ⛔ LO QUE NO SE HACE

- **No se simula `db()` ni `fetch`.** `val-functional.md` §2.3: donde cruza un proceso, solo cuenta
  el sistema real. Un mock probaría el mock — y los tres frenos de `verificacion.ts` viven en
  `demo_config` y en un `ON CONFLICT`, invisibles a cualquier simulacro.
- **No se llama al agente For3s de verdad.** Mandaría un mensaje a una instancia viva y gastaría
  cupo de Claude. Está declarado como pendiente, no fingido.
- **No se escribe un test con SQL destructivo sin nombrar su propia base.**
  `Mente/hooks/gate-critical.py` lo **bloquea al escribirlo** (exit 2, verificado).

---

## 5 · La regla al tocar cualquiera de ellos

> **Sabotea la pieza que el test vigila y comprueba que se pone rojo.** Luego restaura byte a byte
> y confirma con `git status`.

Se aplicó a los cuatro caminos el 2026-08-05, y en ④ destapó que **el propio caso de prueba no
discriminaba**: los cuatro nombres de instancia usados ya empezaban por letras distintas, así que
truncarlos no los hacía colisionar. **Un caso que no distingue el fallo es decoración, aunque el
test pase en verde.**

---

Related: `blocks/active/demo/BLOCK.md` §F-8 (el sub-bloque dueño) ·
`blocks/archive/plan-tests-demo_2026-08/docs/plan-critical-paths.md` (por qué estos 4 caminos) ·
`principles/expertise/val-functional.md` (qué cuenta como prueba) ·
`memory/PENDIENTES.md` §B1-B2 (los dos datos que faltan).
