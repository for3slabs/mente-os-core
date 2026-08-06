# 🔑 CREAR LA RAMA DE NEON PARA TESTS — 3 pasos, ~2 minutos
**Status:** current · **Type:** analysis · **Updated:** 2026-08-06 · **Owner:** brian
**Block:** `blocks/active/demo` §F-8 · **Desbloquea:** 13 tests de integración

## Purpose

Lo único que falta para que los **13 tests de integración** de la demo dejen de saltarse. El
trabajo de código está hecho y verificado; falta un dato que solo puede dar Brian, porque la
cuenta de Neon es suya.

---

## 1 · Por qué hace falta una rama y no vale la base actual

🔴 **Medido 2026-08-06: `DEMO_DATABASE_URL` apunta a la Neon de PRODUCCIÓN** — la misma que
sirve `for3s.vercel.app`, con 4 instancias reales. Un test que escribe ahí borra filas vivas.

Por eso los tests leen **`DEMO_DATABASE_URL_TEST`** y, si falta, **se saltan**. Nunca caen de
vuelta: un default que apunta a algo con dueño es el error de `rules/case-dangerous-default.md`.

⭐ **Una rama de Neon es la respuesta correcta, no un rodeo:** se crea al instante, cuesta
prácticamente nada y es una copia real del esquema — así los tests miden el sistema de verdad
(`principles/expertise/val-functional.md` §2.3) sin tocar nada vivo.

---

## 2 · Los 3 pasos

### ① Crear la rama (en la consola de Neon)

**Proyecto:** el que contiene el endpoint `ep-plain-morning-atn5lyzx` (región `us-east-1.aws`,
base `neondb`).

```
Neon console → Branches → New branch
    Parent branch:  main / production
    Name:           test
```

### ② Copiar la cadena de conexión

Neon la muestra al crear la rama. Es la del **pooler**, igual que la de producción pero con el
endpoint de la rama nueva.

### ③ Pegarla en el archivo (Brian, una sola vez)

```bash
cd ~/for3s/marca-personal
echo 'DEMO_DATABASE_URL_TEST=postgresql://…LA-CADENA-DE-LA-RAMA…' > .env.test.local
```

⛔ **Ese archivo NO se commitea** — lo cubre `.env*` en el `.gitignore` (verificado con
`git check-ignore`). ⚠️ Y va en `marca-personal/`, **no** en `Mente/`.

---

## 3 · Comprobar que funcionó

```bash
cd ~/for3s/marca-personal && npx vitest run
```

| | antes | después |
|---|---|---|
| pasan | 10 | **23** |
| saltados | **13** | 0 |
| fallan | 0 | 0 |

Si siguen saliendo 13 saltados, la variable no se está leyendo: comprobar que el archivo se
llama exactamente `.env.test.local` y que la línea empieza por `DEMO_DATABASE_URL_TEST=`.

---

## 4 · Lo que ya está hecho y verificado (no hay que tocarlo)

- **`vitest.config.ts` carga `.env.test.local`.** 🔴 Vitest **no** lee ningún `.env` por su
  cuenta — medido el 2026-08-06. Sin ese cableado, pegar la cadena no habría servido de nada y
  los tests habrían seguido saltándose **sin decir por qué**: el peor fallo, el que parece éxito.
  Probado en las dos direcciones: sin archivo → se saltan; con una cadena falsa → intentan
  conectar de verdad (`ECONNREFUSED`).
- ⛔ **Solo se lee `.env.test.local`, jamás `.env.local`** — esa última lleva la URL de
  producción.
- **Los tests corren en serie** (`singleFork`): comparten una base y en paralelo se pisarían.
- **Ninguno manda correo:** `enviarCodigo` hace el INSERT antes de mirar `RESEND_API_KEY`.
- **Cada test limpia lo que escribe** y usa correos `@for3s.invalid`, un TLD que RFC 2606
  reserva para que nunca resuelva.

---

## 5 · Qué se desbloquea, en concreto

| Camino | Tests | Lo que empieza a vigilarse |
|---|---|---|
| ① ENTRAR | 7 | ⭐ la **regresión de V2**: gastar los 5 intentos, pulsar reenviar y comprobar que el contador **no** vuelve a cero. Ese bug abría la fuerza bruta |
| ② AUTORIZAR | 5 | que un correo desconocido no entre a una 1:1, y que un dueño solo entre a SU oficina |
| ③ HABLAR | 1 | que un correo sin canal falle CLARO en vez de caer al agente de otro |

---

Related: `blocks/active/demo/docs/como-correr-los-tests.md` (la guía general) ·
`memory/PENDIENTES.md` §B1 (el bloqueo) · `blocks/active/demo/BLOCK.md` §F-8.
