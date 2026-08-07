# QUICKSTART — de clon a funcionando en 3 pasos
**Status:** current · **Type:** entry-point · **Updated:** 2026-08-07 · **Owner:** brian
**Verified by:** cada número de este archivo se midió corriendo los pasos en un clon real

## Purpose

Llevar a alguien que **no conoce este proyecto** de un `git clone` a un Mente OS que funciona.
Escrito para un extraño, no para su autor: si algo aquí solo se entiende sabiendo cómo trabaja
Brian, es un defecto de este archivo.

> ⭐ **Qué es Mente OS:** un motor que **gobierna** cómo se construye. No genera código: impone
> que lo construido se explique antes de hacerse, se verifique antes de cerrarse, y que las
> reglas se cumplan porque un script las bloquea — no porque alguien las recuerde.
>
> **La ley que lo explica todo:** *una regla en código se cumple 100%; una que solo vive en un
> documento, 40-60%.* Por eso la doctrina es documento y **la verificación es script**.

---

## 1 · Lo que necesitas antes

| | |
|---|---|
| **Python 3** y **bash** | los validadores están escritos en eso, sin dependencias externas |
| **git** | el sistema se apoya en él para saber qué cambió |
| **Claude Code** (opcional) | las puertas son sus hooks. Sin él el motor sigue verificando, pero nada bloquea |

⛔ **No hay `npm install` ni nada que compilar.** Si tienes Python y bash, ya puedes.

---

## 2 · Los 3 pasos

### ① Clona

```bash
git clone <url-del-repo> mi-mente
cd mi-mente
```

### ② Instala — ⚠️ en una terminal REAL

```bash
cd Mente
bin/init
```

Te va a **preguntar tu nombre**. Eso es deliberado: `ADR-003` dice que el criterio se pregunta,
nunca se adivina, y quién decide en una instancia es criterio.

> 🔴 **Si lo lanzas con una tubería o desde un script, se niega:**
> *"`owner name` has no default and there is no terminal to ask on"*.
> No es un fallo — es la negativa a inventar un dato que solo tú tienes.

`bin/init` hace tres cosas: crea tu `mente.config.yml`, genera `CLAUDE.md` y `PROJECT-RULES.md`
con tu nombre, y cablea **7 hooks** con rutas portables.

### ③ Comprueba

```bash
bin/test-f0-f6
```

---

## 3 · Qué vas a ver, y por qué NO es un error

Esto es lo que **de verdad** pasa, medido el 2026-08-07 en un clon limpio:

| Momento | Resultado |
|---|---|
| recién clonado | 177 pasan · **10 fallan** |
| tras `bin/init` | 180 pasan · **8 fallan** |

> ⚠️ **Sí: termina con 8 en rojo, y el sistema NO está roto.**

Los 8 tienen una causa común: **este repositorio trae la instancia de su autor** — sus bloques
de trabajo, su memoria, un `docs/WORKSPACE.md` que describe *su* máquina. Los checks verifican
esa instancia y tú no la tienes.

| Lo que falla | Por qué |
|---|---|
| `no dead paths in additionalDirectories` | apunta a proyectos vecinos de Brian |
| `block §F import counts` · `grade-block archived` | verifican SU bloque de trabajo, no el tuyo |
| `every repo WORKSPACE.md names` | describe SU máquina |
| `check-clear-ready … registered=no` | tu sesión aún no está en el registro |
| `nested repo detection` | busca un sub-repo que solo existe en su árbol |

⭐ **Es el sistema fallando CERRADO**, que es su diseño: ante algo sin configurar prefiere
gritar a asumir. Un motor que arrancara verde sin saber quién eres estaría inventando.

**Lo que sí importa:** `check-blocks` corre limpio en tu clon (**0 errores · 0 warnings**),
`check-health` reporta la versión, y las **3 puertas bloquean**. Puedes trabajar.

⚠️ `check-links` te dirá **unas 5 citas rotas**: apuntan a `Maestro/`, un repositorio hermano
que no viaja con éste. No son erratas — son punteros a algo que su autor sí tiene.

---

## 4 · Tu primer bloque — el ciclo completo

```bash
bin/new-block mi-primer-trabajo --type docs   # lo crea con su contrato §A-K
bin/check-sufficiency mi-primer-trabajo       # ¿se puede retomar leyendo solo §A-E?
bin/grade-block mi-primer-trabajo             # 🟢 producto o 🔴 MVP — MEDIDO, no opinado
```

Un **bloque** es una unidad de trabajo con contrato: qué entra, qué no, de qué depende, bajo
qué criterio se juzga y cuándo puede cerrarse. `rules/block-lifecycle.md` lo explica entero.

⛔ **Lo que el sistema te va a impedir**, y conviene saberlo antes de chocar:

- cerrar un bloque con sub-bloques abiertos → `gate-critical` lo **bloquea**
- una migración destructiva sin rollback → **bloqueada**
- commitear en `master` → **bloqueado** (rama → verificar → PR)
- leer `secrets/` sin permiso vivo → **pregunta**, y queda en bitácora

---

## 5 · Los comandos que vas a usar

| Necesitas… | Comando |
|---|---|
| ¿está sano el sistema? | `bin/check-health` |
| ¿todo apunta a algo que existe? | `bin/check-links` |
| ¿los bloques cumplen su contrato? | `bin/check-blocks` |
| ⭐ la verificación completa | `bin/test-f0-f6` — *lo único que importa es `failed: 0`* |
| la revisión de antes de un release | `bin/verify-all` (`--rapido` omite clon y demo) |
| ¿qué puedo ejecutar y qué no? | `Mente/CAPABILITIES.md` |

---

## 6 · Si algo sale mal

| Síntoma | Qué pasa |
|---|---|
| `bin/init` se niega a preguntar | lo lanzaste sin terminal. Córrelo directo, sin tuberías |
| más de 8 fallos tras el init | algo se rompió: `bin/check-health` lo nombra con su razón |
| un hook bloquea todo | mira `.claude/settings.json`: cada grupo de `PreToolUse` **debe** llevar `matcher`. Sin él, un hook corre en todas las herramientas |
| `check-links` reporta rotas | apuntan a `Maestro/`, `secrets/` o repos vecinos que no viajan — el validador ya las exime; si ves otras, son reales |

---

Related: `CLAUDE.md` (el enrutador que Claude Code lee al arrancar) · `PROJECT-RULES.md` (las
reglas de nivel proyecto) · `Mente/CAPABILITIES.md` (qué puede ejecutarse y qué está prohibido) ·
`Mente/rules/block-lifecycle.md` (abrir y cerrar un bloque) · `LICENSE` (AGPL-3.0).
