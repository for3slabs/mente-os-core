# ARCHITECTURE · language policy

**Status:** current · **Type:** architecture · **Updated:** 2026-07-30 · **Owner:** brian
**Part of:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` (§0-BIS) · **ADR:** ADR-023 ·
**Block:** `blk-split-architecture-2026-07`

## Purpose

Which language each artefact is written in, and why. Instructions in US English because the LLM
reads them; Brian's thinking in Spanish because forcing a second language would degrade the
criterion, which is the expensive half.

Extracted verbatim on 2026-07-30 — it was `0-BIS` with four sub-sections, i.e. a grown section:
the suffix WAS the split signal (ADR-027). **Moved, not rewritten.**

---

## 1 · ⭐⭐ POLÍTICA DE IDIOMA *(decidido 2026-07-27)*

> **Brian:** *"cuando tengamos que poner instrucciones de texto, todo será en inglés — inglés de
> Estados Unidos."*

**La regla de reparto:**

| Qué | Idioma | Por qué |
|---|---|---|
| **Todo lo que la IA lee como INSTRUCCIÓN** | 🇺🇸 **inglés (US)** | la IA lo resuelve con precisión; es el idioma de todas las convenciones sobre las que se apoya |
| **El pensamiento de Brian** | 🇪🇸 **español** | es su criterio; forzarlo a otro idioma le quita matiz |

### 1.1 · Qué va en INGLÉS (US)

| Archivo | Tipo |
|---|---|
| `CLAUDE.md` + el enrutador (capa A) | instrucción · se inyecta |
| `.claude/output-styles/for3s.md` | instrucción · **el mayor peso del sistema** |
| `base-rules.md` | instrucción |
| `principles/owner-0-voice.md` · `owner-1-docs` · `owner-2-dev` · `owner-3-validation` | instrucción |
| `principles/expertise/{database,backend,frontend}.md` | instrucción |
| `rules/contract-*.md` · `rules/rule-*.md` · `rules/qa-dimensions.md` | instrucción |
| `rules/case-*.md` | instrucción (se inyecta antes de trabajar) |
| **`blocks/active/*/BLOCK.md`** ⭐ | **instrucción — la IA lo lee en cada arranque** |
| Nombres de archivos y carpetas | `rules/NAMING_CONVENTION.md` |
| Salida de los validadores (`bin/*`) | instrucción · mensajes de error |
| Commits, changelog público | ya era la práctica |

### 1.2 · Qué se queda en ESPAÑOL

`Vision_Mente_OS_v2` · `Plan_Implementacion` · los análisis comparativos · `memory/RETOMAR.md` ·
`Bitacora_Progreso` · `Registro_Conversaciones` · las memorias · **y las conversaciones con Brian**.

> **El criterio de corte:** *¿esto lo lee la IA para SABER QUÉ HACER, o lo lee un humano para
> ENTENDER QUÉ PASÓ?* Lo primero va en inglés. Lo segundo en español.

### 1.3 · ⭐ El vocabulario canónico — traducido

| Español (v1) | 🇺🇸 **Inglés (v2)** |
|---|---|
| bloque · sub-bloque | **block · sub-block** |
| encargado 0/1/2/3 | **owner-0 (voice) · owner-1 · owner-2 · owner-3** |
| carril: directo · tarea · bloque-completo | **lane: direct · task · full-block** |
| límites: qué SÍ / qué NO | **scope: IN / OUT** |
| roce (con una regla) | **friction** |
| veredicto de calidad | **quality verdict** |
| prueba de suficiencia | **sufficiency check** |
| fix ≠ parche | **fix ≠ patch** |
| propagación · dependientes | **propagation · dependents** |
| punto de guardado | **checkpoint** |
| estándar obligatorio | **required standard** |
| validador | **validator** |
| puerta cerrada | **closed gate** |
| recibo de aprobación | **approval receipt** |

> ⚠️ **Un solo término por concepto.** Prohibido mezclar (`lane` en un sitio y `carril` en otro):
> es exactamente la anarquía que el v2 existe para eliminar.

### 1.4 · Inglés de EE.UU., no británico

`behavior` (no *behaviour*) · `organize` (no *organise*) · `analyze` (no *analyse*) ·
`center` (no *centre*) · `license` (sustantivo y verbo).
**Fechas:** ISO `2026-07-27` siempre — evita la ambigüedad MM/DD vs DD/MM.

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (entry point) ·
`rules/decisions/ADR-023-us-english-for-instructions.md` (the decision) ·
`rules/NAMING_CONVENTION.md`.
