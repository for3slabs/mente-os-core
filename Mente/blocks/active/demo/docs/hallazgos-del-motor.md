# HALLAZGOS DEL MOTOR encontrados desde el bloque `demo`
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian
**Block:** `blocks/active/demo` §G · **Split:** 2026-08-05, `doc-structure.md`

## Purpose

Defectos de **Mente OS**, no de la demo, que salieron trabajando este bloque. Viven aquí porque
el §G pasó su techo y porque no son decisiones sobre la demo: son correcciones al motor que
gobierna todos los bloques. ⛔ Movidos ÍNTEGROS, sin resumir.

---

- 🔴 2026-08-05 · **`bin/check-applied` tenía un FALSO POSITIVO — preexistente, no lo introdujo este
  bloque** (verificado contra HEAD: la línea era idéntica). Aceptaba un estándar como *aplicado* si
  las palabras de su nombre aparecían SUELTAS en cualquier parte de la evidencia. Sonda: declaré
  `rule-session-close.md` en este bloque, que jamás lo usó → **el check lo dio por ✅** (el §G
  menciona `session.ts` y `closed` por motivos ajenos). Corregido a exigir el nombre del estándar.
  Reprobado: la sonda ahora sale 🟡 y los 9 reales siguen ✅.
- ⭐ 2026-08-05 · **Este BLOCK.md se PARTIÓ al pasar su techo (206 → 165 líneas)** y eso destapó un
  segundo defecto: `check-applied` leía solo el §G, así que al mover las 7 decisiones de julio a
  `blocks/active/demo/docs/decisions-julio.md` **3 estándares pasaron a leerse como nunca
  aplicados.** 🔬 **La lección: un puntero que una máquina no sigue no es un puntero.** Una regla
  que manda partir documentos y un check que solo lee una de las mitades no pueden tener razón los
  dos. Ahora el check sigue los punteros a `blocks/…md`.

### 🔴 2026-08-05 · `check-sufficiency` leía la palabra ESPAÑOLA "todo" como el marcador `TODO`

Un §E perfectamente respondido — *"next: todo lo abierto espera un dato de Brian"* — se reportaba
como **placeholder**. Los bloques se escriben en español y `TODO` con `re.I` casa dentro de "todo".
⚠️ **El mensaje decía lo contrario de lo que pasaba**: mandaba a rellenar un hueco inexistente.

⚠️ **`\b` NO lo arregla** — "todo" y "TODO" son las mismas cuatro letras. Lo intenté primero y lo
comprobé antes de darlo por bueno: seguía en rojo. **La mayúscula ES la señal.** Corregido quitando
`re.I` de los marcadores con letras. Reprobado en ambas direcciones.

### 🔴 2026-08-05 · Dos checks de la batería CADUCARON solos al tener éxito el trabajo

`demo verdict exit code (2 = 🔴 MVP)` y `verdict forgery` usaban el bloque `demo` como ejemplo de
bloque ROJO. El día que dejó de estarlo, **los dos se cayeron sin que nada estuviera mal**.

⭐ **Un check cuyo sujeto es trabajo en curso caduca solo.** Reescritos sobre lo invariante:
① el exit code concuerda con el veredicto medido, **sea cual sea** (0 product · 1 close · 2 MVP —
mi primera versión solo contemplaba dos y falló) · ② la medición contradice el veredicto escrito,
cualquiera que este sea.

🔬 **Dos intentos fallidos, ambos comprobados antes de confiar en ellos:** un bloque sonda con un
huérfano fabricado daba `⬜ NOTHING MEASURED` (el escáner no ve un `.ts` suelto), y un `sed` de
sustitución no escribía nada porque `blocks/active/demo/BLOCK.md` **no tiene** línea de veredicto (`grep -c` = 0)
— habría sido un verde falso. La versión final AÑADE la línea y la retira siempre; verificado con
md5 que el bloque queda intacto.

---

Related: `blocks/active/demo/BLOCK.md` §G (las decisiones del bloque) ·
`rules/rule-checks-must-measure.md` (la familia a la que pertenecen los tres).
