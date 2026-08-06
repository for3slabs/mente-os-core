# For3s OS — arranque

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-02 · **Owner:** brian
**Level:** 🚪 el ARRANQUE — lo carga Claude Code solo; no hereda ni es heredado (no lleva reglas)
**Verified by:** `Mente/bin/check-links` · `Mente/bin/test-f0-f6` (§F6 · router + métricas)
**Scope:** ⚠️ documento de INSTANCIA, no del motor — el motor publicado es `mente-os` (MIT)

## Purpose

Enrutar el arranque de una sesión: **a dónde ir a leer**, qué corre solo y qué regla manda.
No guarda reglas ni estado — los apunta, para que el valor se lea de donde se mide.

> Claude Code lee este archivo automáticamente al iniciar cada sesión.
> **Es un ENRUTADOR, no un almacén de reglas.** Apunta a dónde viven; no las repite.
> Una regla escrita aquí no tiene nivel declarado — y ese era el bug (`Mente/rules/rule-inheritance.md`).

---

## 🚀 ARRANQUE (hacer SIEMPRE, sin que Brian lo pida)

1. **LEER PRIMERO** `Mente/memory/RETOMAR.md` (~5 KB) — el cold-start brief: dónde quedamos + próximo
   paso + flags + punteros. **En ~90% de los casos es TODO lo que necesitas.**
2. ⛔ **NO leer** `Mente/memory/Estado_Sesion_Continuidad.md` (200 KB) salvo que un puntero de RETOMAR
   lo mande explícitamente. Leerlo "por si acaso" gasta tokens (medido por Brian, 2026-06-09).
3. **Si hay un bloque activo** → cargar su Tier 1 (`§A-E` de `Mente/blocks/active/*/BLOCK.md`).
   Si `§A-E` no alcanza → **decirlo, no inferir.**
4. Si Brian dice "lee RETOMAR" → ese archivo + sus punteros.

**Por qué:** retomar tras una pausa reenvía la conversación completa (cache miss) = caro. Mente OS
guarda todo en disco, así que `/clear` es seguro **cuando la sesión está registrada** (§ regla abajo).

---

## 🧭 ENRUTADOR DE REGLAS — 3 niveles, se heredan hacia abajo

```
🌐 UNIVERSAL   Mente/base-rules.md        cualquier proyecto · desde la primera respuesta
      │ hereda (puede AÑADIR o ENDURECER — nunca RELAJAR)
      ▼
🏢 PROYECTO    PROJECT-RULES.md           esto es For3s OS: el gate, server-first, el scope
      │ hereda
      ▼
📦 BLOQUE      Mente/blocks/active/<n>/BLOCK.md §B    solo mientras ese bloque esté abierto
```

| Qué necesitas | Dónde está |
|---|---|
| **Conducta** — no afirmar sin medir · no inventar criterio · explicar antes de construir | `Mente/base-rules.md` |
| **Este proyecto** — scope, el gate a otros Mente OS, server-first, seguridad, identidad | **`PROJECT-RULES.md`** |
| **La voz** — cómo se comunica Mente OS | `Mente/principles/owner-0-voice.md` (vehículo: `outputStyle: "for3s"`) |
| **Trabajo grande** — método de fases F | `Mente/rules/ESTANDAR_Metodo_Fases_F.md` |
| **Abrir/cerrar un bloque** | `Mente/rules/block-lifecycle.md` |
| **Qué estándar aplica al código que voy a tocar** | 🤖 el hook `Mente/hooks/pre-edit-standards.py` lo inyecta solo |
| **Arquitectura del sistema** | `Mente/Cerebro/For3s_OS_Grafo_Maestro.md` |
| 🤖 **QUÉ PUEDO EJECUTAR y qué NO puedo tocar** — los 15 validadores, las 3 puertas, la línea motor/instancia | ⭐ `Mente/CAPABILITIES.md` |
| 🗺️ **Dónde está cada cosa de ESTA máquina** — repos, qué está cerrado, dónde viven los secretos (nunca su valor) | `Mente/docs/WORKSPACE.md` |
| 🚢 **Cómo se sube un PR** — rama → verificar → PR → ⛔ no mergear (cualquier disciplina) | `Mente/rules/rule-shipping-flow.md` |

> ⭐ **Las reglas se SUMAN, nunca se relajan.** Dos bloques comparten reglas solo si uno declara al
> otro en su `§C`. En conflicto, **gana la más estricta.**

---

## 🤖 LO QUE EL SISTEMA VERIFICA SOLO (no hay que pedirlo)

| Cuándo | Qué corre |
|---|---|
| al iniciar sesión | `Mente/hooks/session-start.sh` → salud + estructura + índices + bloques a la deriva. **Habla solo en 🔴** |
| antes de editar | `Mente/hooks/pre-edit-standards.py` → inyecta los `§D` del bloque dueño |
| antes de editar | `Mente/hooks/gate-critical.py` → 🔴 BD sin rollback · 🔴 cerrar bloque insuficiente · ⚠️ pieza con dependientes |
| antes de un commit | `Mente/hooks/pre-commit.sh` → 🔴 **BLOQUEA** un bloque que viola su contrato |
| ¿esto es producto o MVP? | `Mente/bin/grade-block <bloque>` → veredicto **medido**, nunca opinión |
| ¿el árbol es el declarado? | `Mente/bin/check-structure` → lee `Mente/Maestro/piezas.tsv` |
| regenerar los índices | `Mente/bin/generate-index` → 🤖 `docs/INDEX.md` + `docs/STATES.md` |
| antes de `/clear` | `Mente/bin/check-clear-ready` → 🔴 se niega si algo se perdería |
| **el sistema completo** | `Mente/bin/test-f0-f6` → lo único que importa es `failed: 0` · el conteo vive en `Mente/docs/METRICS.md` (`battery.checks`) |

⭐ **La ley medida de este sistema:** una regla en código se cumple 100%; una regla solo en documento
se cumple 40-60%. **Por eso la doctrina es un documento y la VERIFICACIÓN es un script.**

---

## ⛔ REGLA `/clear` — registrar ANTES de cerrar

Cuando Brian avise que va a dar `/clear` (o yo lo proponga), **antes** hay que registrar la sesión
que muere en `Mente/Cerebro/Registro_Conversaciones.md`: fila en el índice + su autopsia.

**Verificarlo con `Mente/bin/check-clear-ready`** — se niega si falta.
Regla completa: `Mente/rules/rule-session-close.md`. Origen: la sesión de 278 MB del 9-jul.

> `/clear` es un **corte, no un guardado.** Lo que no está en disco se pierde sin aviso.
> Ese es el origen de *"antes del clear me dijo todo perfecto, después me dijo sigue roto"*.

---

## 🗂️ DÓNDE VIVE CADA COSA

| Carpeta | Qué |
|---|---|
| `Mente/base-rules.md` · `PROJECT-RULES.md` | 🌐 y 🏢 las reglas, por nivel |
| `Mente/blocks/` | 📦 el trabajo — `active/` `blocked/` `archive/` |
| `Mente/rules/` | contratos + reglas + `decisions/` (los ADRs) |
| `Mente/principles/` | los dueños (owner-0..3) + `expertise/` |
| `Mente/bin/` · `Mente/hooks/` | 🤖 los validadores y las puertas |
| `Mente/docs/` | planes, análisis, bitácoras de fase · 🤖 `Mente/docs/INDEX.md` y `Mente/docs/STATES.md` generados |
| `Mente/Maestro/piezas.tsv` | ⭐ **dónde vive cada pieza clave** — mover algo cuesta 1 línea |
| `Mente/vision/` `work/` `memory/` `bridges/` | 🆕 visión · trabajo cerrado · memoria viva · el gate |
| `Mente/Cerebro/` | el grafo de For3s OS (el producto — NO se migra) |

---

## 📌 ESTADO

> ⚠️ **Esta sección NO lleva números.** Un enrutador que declara estado se desfasa: el 30-jul se
> congelaron aquí el conteo de la batería, la versión del producto y el avance de la última fase —
> los tres ya eran falsos. Un número copiado es correcto **exactamente una vez**. Aquí solo van
> punteros: el valor se lee del archivo que lo mide, así que no puede quedar desfasado.

**Diseño 100% LOCKED** (R1-R10, 11 nodos, 3 pilares). **For3s OS EN PRODUCCIÓN** — bot Telegram
contenerizado, multi-instancia. Panel admin en `for3s.vercel.app/for3s-admin`.
**MOLDE "For3s Inside"** y **For3s TRACE** en `molde/`.

**Mente OS v2** = el sistema de bloques que gobierna este repo: validadores + hooks + 3 niveles de
reglas. **La prueba viva es `Mente/bin/test-f0-f6`; lo único que importa es `failed: 0`.**

| Necesitas… | Léelo de… |
|---|---|
| ⭐ **estado real + próximo paso** | `Mente/memory/RETOMAR.md` |
| cualquier **número vivo** (batería, huecos, permisos, citas) | 🤖 `Mente/docs/METRICS.md` |
| versión del producto · fases cerradas · qué bloques hay | `Mente/memory/RETOMAR.md` §5 |
| pendientes abiertos | `Mente/memory/PENDIENTES.md` |

---

Related: `PROJECT-RULES.md` (🏢 el nivel de proyecto que este enrutador declara) · `Mente/base-rules.md` (🌐 universal) · `Mente/memory/RETOMAR.md` (el estado real) · `Mente/rules/rule-inheritance.md` (por qué aquí NO van reglas) · `Mente/rules/contract-document.md` (la forma que este archivo cumple).
