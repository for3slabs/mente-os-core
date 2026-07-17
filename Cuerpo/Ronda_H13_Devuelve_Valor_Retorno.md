# 🎁 Ronda de Diseño — H13 "DEVUELVE" (Capa de Valor de Retorno)

> **Qué es:** F0 del hito que ataca el **Frente D** post-Incubathon (el frente MADRE).
> **Origen:** Brian 2026-07-13 ("CONTINUEMOS CON EL D"). Doc madre:
> `Alma/Aprendizajes_De_Campo_Post_Incubathon.md` §Frente D. Método: `ESTANDAR_Metodo_Fases_F.md`.
> **Estado:** 🎉 **HITO COMPLETO (2026-07-14, v0.16.0)** — F1 `17dbd01` · F2 `15fc29d` ·
> F3 `90a6256` (verificada EN VIVO) · F4 `9c099ef` · F5 `ccc476a`. 5 commits firmados, SOLO
> server (sin push). Batería final: 170 tests · /salud 1115 OK · 0 FAIL. 4 bugs latentes cazados.
> **Quedan:** propagación a otras instancias (decisión Brian) · 1 corrida real del equipo
> (confirmar capsula_equipo en vivo) · carril "urgente" (diferido, anotado en PENDIENTES).

## ✅ F3 VERIFICADA EN VIVO (2026-07-14, turno real de Brian)

Brian escribió *"oye ¿cómo va el backup offsite del server?"* desde el TEMA
`tg:…:incubathon` → por-cierto #5 disparó con **sim=0.70** (pertenencia cruzó el tema
correctamente: el insight vivía en la sesión base), la respuesta TEJIÓ el insight con la memoria
entrenada (el backup de abril en Drive), `via=contextual` sellado, cero errores en el turno.

## ✅ F4 CERRADA (2026-07-14) — evidencia

- **Construido:** `teclado_feedback` (dict crudo p/ worker, numerado como el digest) ·
  `marcar_feedback` (solo desde `entregado` + PERTENENCIA punto único — nadie marca lo ajeno) ·
  `recientes()` + `Insight.via` aditivo · `_alertar_dueno(reply_markup=)` aditivo · el digest sale
  con botones ✅/❌ por insight · comando **`/insights`** (stats útiles/no/sin-marcar/en-cola +
  botones) · callback `insok:/insno:` (digest multi-insight: solo quita la fila tocada) · 6 tests.
- **Batería §5-BIS:** 170 tests · ruff · **ty devuelto a línea base 12** (los 3 nuevos eran MÍOS —
  cazados comparando contra baseline y arreglados: getattr defensivo en reply_markup + guard None
  en test) · /salud 1115 OK · 0 FAIL · E2E: ajeno rechazado ✓ dueño marca útil ✓ re-marca
  rechazada ✓ recientes con via ✓ **mensaje real con botones enviado a Brian** (marca #5 en vivo).
- **Semilla del modelito:** cada ✅/❌ queda en `insights.estado` (util/ignorado) + via — el
  dataset del futuro scoring aprendido de memoria (línea futura del doc madre).

## ✅ F3 CERRADA (2026-07-14) — evidencia

- **Construido:** migración 038 (insights.embedding vector(1024), calculado al minar con BGE-M3) ·
  `por_cierto()` en insights.py — orden barato→caro (sin candidatos = 1 query, CERO embeddings en
  el caso común), gates fail-closed (clase valor + /proactivo + pertenencia), match coseno umbral
  ENV 0.55, marca `via=contextual` · inyección en conversation.py tras `memoria.recordar()`
  (defensiva total, patrón del bloque AI5) · 6 tests nuevos.
- **⭐ Refactor de calidad (caza de bug FUTURO):** `_SQL_PERTENENCIA` = PUNTO ÚNICO del blindaje
  BUG-14 — el criterio de pertenencia iba a quedar DUPLICADO entre digest y por-cierto (SQL de
  seguridad duplicado = cuna de bugs latentes). para_digest migrado, equivalencia verificada E2E.
- **Batería §5-BIS:** 164 tests · ruff · ty (el "1" que salió = diagnóstico PRE-existente de
  api_channel apuntando a conversation.py:1084, verificado contra línea base) · arranque real
  migración=[38] · /salud 1115 OK · 0 FAIL · **E2E real con embeddings:** relevante → bloque +
  entregado(contextual) ✓ · irrelevante → None (sim 0.306 < 0.55, buen margen) ✓ · /proactivo
  off → None ✓ · clase valor off → None ✓ · para_digest post-refactor ✓.
- **⏳ Prueba EN VIVO pendiente (Brian):** quedó el insight #5 ("Verificar el backup offsite del
  servidor") en estado `nuevo` — escribirle a @For3s_Brian_bot algo como *"¿cómo va el backup
  offsite del server?"* y la respuesta debería mencionarlo con naturalidad.

## ✅ F2 CERRADA (2026-07-14) — evidencia

- **Construido:** migración 037 (perfil_usuario.proactivo + insights.via) · `armar_digest` +
  `para_digest` (blindaje multi-usuario: el digest del dueño JAMÁS incluye insights de sesiones de
  miembros) + `marcar_entregados` (solo tras envío exitoso) · `job_digest_valor` (cron 08:00 Mx,
  gates fail-closed: clase valor → /proactivo → hay insights; silencio antes que relleno) ·
  comando `/proactivo on|off` · audit por entrega · 5 tests nuevos.
- **🐛 BUG LATENTE PRE-EXISTENTE CAZADO (2 capas):** las alertas PR2 del worker estaban **MUDAS
  en instancias de plantilla** — (1) `_alertar_dueno` solo miraba el vault sin fallback a ENV
  (el agent sí resuelve vault→ENV); (2) NINGÚN compose pasaba `TELEGRAM_BOT_TOKEN` al servicio
  worker. Nadie lo notó porque las alertas solo salen cuando algo está 🔴. Arreglado en código +
  ambos composes → **también repara las alertas de salud de brian/jazz/mashe/general.**
- **Batería §5-BIS:** 158 tests · ruff · ty (0 míos) · arranque real (migración=[37], worker 25
  functions con cron digest_valor) · /salud 1115 OK · 0 FAIL · **E2E real: digest ENTREGADO por
  Telegram a Brian** (3 insights, via=digest), off→silencio sin perder nada, 2ª corrida→silencio,
  audit `valor_digest_enviado` ✓.
- **Nota de alcance:** el carril "urgente" (1/día extra para confianza ≥ alta) quedó DIFERIDO a
  F3/F5 — el freno "máx 1 digest + 1 urgente" era límite, no promesa; hoy solo existe el digest.

## ✅ F1 CERRADA (2026-07-13) — evidencia

- **Construido:** clase VALOR en dmn.py + migración 036 (valor_on OFF default + tabla insights) +
  módulo `insights.py` (punto único) + task `insight_mining` (sonnet, throttle 6h, máx 2
  sesiones/ciclo) + `/dmn valor on|off` + 10 tests nuevos.
- **🐛 2 BUGS LATENTES CAZADOS Y CERRADOS** (curiosidad de Brian: "se curioso"): `set_clase` y
  `correr_ciclo` usaban un `else` ciego → cualquier clase desconocida caía en GENERATIVAS
  (la 3ª clase habría corrido con el flag equivocado). Ahora: ValueError explícito / OFF fail-closed.
  Demostrado con test + E2E.
- **Batería §5-BIS:** A 153 tests + ruff + ty (0 diagnósticos míos) · B arranque real
  (migración=[36], cerebro conectado, 9 contenedores sanos) · C /salud **1115 OK · 0 FAIL** ·
  D semántica scope dueño 0 ajenos + corpus import OK (vía incluir_import) · G E2E real:
  **3 insights con base verificable de la memoria entrenada** (cabos sueltos, conf 0.75-0.88,
  **0 seqs alucinados**), throttle probado, corrida registrada clase=valor.
- **Estreno:** valor_on=ON SOLO en `brian` (vía set_clase real). Foresito/general intactos
  (siguen anclados a la imagen vieja; heredarán 036 con valor OFF cuando se recreen).
- **Hallazgo anotado (deuda menor, NO mía):** 9 archivos del repo no pasan `ruff format --check`
  (entrenamiento_*, api_channel, specialists, telegram_channel línea ~2736) — pre-existente.

---

## 1 · La visión en palabras de Brian (el contrato)

- *"Siento que For3s es un chat que contesta y guarda memoria solamente, y eso me preocupa."*
- *"La memoria está padre pero ¿qué hace, solo resguarda? ¿Cuál es su función? Aún no hay un
  valor que devuelva."*
- Rebote confirmado por Brian: **no es que For3s valga poco — lo usó como TUBO y nunca lo vio
  DEVOLVER valor.** Lo que falta: que For3s ACTÚE sobre su memoria — *"noté que llevas 3 días en X,
  ¿quieres que…?"*, *"detecté este patrón en tus clientes"*, propuestas proactivas.

**El diagnóstico fino (F0, 2026-07-13):** For3s ya "piensa" en segundo plano (DMN H9), pero todo lo
generativo apunta a **mejorarse a sí mismo** (skills, prompts, hipótesis) y sus propuestas mueren en
una tabla que solo se ve con /dmn. **Nunca cierra el círculo de volver al usuario con algo útil.**
Es un cerebro que sueña pero nunca te cuenta lo que soñó.

## 2 · Decisiones LOCKED (Brian, 2026-07-13, vía AskUserQuestion)

| Decisión | Elección |
|---|---|
| Entrega | **Digest proactivo (1/día) + contextual en conversación** |
| Estreno | **Solo instancia `brian`** (@For3s_Brian_bot, el laboratorio) → luego propagar |
| Motor | **Extender el DMN (H9)** — nueva clase de tareas; cero motor nuevo |
| Frenos | **Máx 1-2 mensajes proactivos/día** (digest + 1 urgente excepcional) |

## 3 · Terreno: qué se REUSA (verificado en el código del server 2026-07-13)

| Pieza | Dónde vive | Cómo se reusa |
|---|---|---|
| Canal proactivo al dueño | `tasks.py:~400-430` (alerta PR2: secret_store → bot token → sendMessage) | El digest sale por el MISMO camino |
| Motor idle + scheduler | `dmn.py` (trigger/action, `correr_ciclo`, kill switch `FOR3S_DMN_OFF`, idle 15min) | La task de mining es una DMNTask más |
| Clases con gate | `dmn.py` CLASE_HOUSEKEEPING / CLASE_GENERATIVA + `set_clase` | Se añade **CLASE_VALOR = "valor"** (3ª clase, ON/OFF en BD) |
| Propuestas + gate | migración `022_dmn_propuestas.sql` + `propuestas_pendientes` | Patrón de referencia para la tabla `insights` |
| Memoria minable | `memoria.recordar()` (cascada), grafo AGE (`kg.py`), `hilo_status`, `decisiones` | Materia prima del mining |
| Perfil del usuario | `perfil.py` + `perfil_infer.py` | El insight se adapta a quién eres |
| ROI por task | `dmn.roi_por_task` | Mide si la capa devuelve valor de verdad |
| Governor + audit | H11 | Frenos de costo + rastro inmutable de cada entrega |
| Botones ✅/❌ | patrón del gate de equipo (`on_gate_select`) | Feedback útil/no-útil por insight |

**Regla multi-usuario:** el mining es POR SESIÓN (`tg:<uid>`) y respeta el aislamiento ya blindado
(BUG-14/18/19): los insights de una persona salen SOLO de su memoria y se entregan SOLO a ella.

## 4 · Las fases

### F1 — Motor de insights (la mina)
- `dmn.py`: nueva **CLASE_VALOR** (junto a housekeeping/generativa), ON/OFF en BD por workspace
  (extender `_clases_activas`/`set_clase` + /dmn). Default: **OFF en todas, ON solo en `brian`**.
- Migración BD (v35): tabla **`insights`** — id, session_id, tipo (`patron` | `cabo_suelto` |
  `propuesta`), titulo, cuerpo, confianza, estado (`nuevo`→`entregado`→`util`/`ignorado`),
  episodios_origen, created_at, entregado_at.
- Task **`insight_mining`** (clase valor, sonnet): trigger = ≥N episodios nuevos desde el último
  mining de esa sesión; action = mira lo reciente (episodios + temas + decisiones + grafo + perfil)
  → 0-3 insights CON base real (prohibido inventar; si no hay nada, no hay insight). Defensivo:
  jamás tumba el ciclo.
- **Verificación:** correr en `brian` con la memoria real del entrenamiento → insights en BD con
  episodios_origen válidos; sesión ajena = 0 filas cruzadas.

### F2 — Digest proactivo (el mensajero)
- Job cron en `tasks.py` (patrón `@registra_corrida`): a hora configurable por ENV
  (`FOR3S_DIGEST_HORA_UTC`, default mañana Mx) toma insights `nuevo` con confianza ≥ umbral, arma
  UN mensaje breve y lo manda al dueño por el canal de alertas. Marca `entregado`.
- Frenos: **máx 1 digest + 1 urgente/día** (contador en BD) · comando **`/proactivo on|off`** por
  usuario (fail-closed: OFF = silencio total) · sin insights que valgan → NO manda nada (silencio
  antes que relleno).
- **Verificación:** digest real recibido en Telegram; con /proactivo off → cero mensajes; audit
  registra cada entrega.

### F3 — Valor en el turno (el "por cierto…")
- En el pipeline del turno (telegram_channel → ensamblado de contexto): si hay insight `nuevo`
  RELEVANTE al mensaje (match semántico con embeddings ≥ umbral), se monta como bloque ligero
  "💡 por cierto" para que la respuesta lo mencione con naturalidad. Marca `entregado`.
- Defensivo total: si falla el match, el turno sale normal (nunca rompe la conversación).
- **Verificación:** escribir de un tema con insight pendiente → lo menciona; tema sin relación →
  no mete ruido.

### F4 — Feedback + medición (la semilla del modelito)
- **`/insights`**: lista lo detectado + estado. Botones ✅ útil / ❌ no útil en cada entrega →
  estado `util`/`ignorado`.
- ROI: `roi_por_task` + tasa de utilidad. **Estos datos son la semilla del futuro mini-clasificador
  "qué memoria es valiosa"** (línea futura del doc madre — hoy NO se construye, solo se siembra).
- **Verificación:** marcar ✅/❌ actualiza estado; /insights refleja la verdad de la BD.

### F5 — Batería §5-BIS + cierre del hito
- Batería completa (A tests · B arranque · C /salud 0 FAIL · D memoria+reconexión · E cada H ·
  F tools · G lo nuevo E2E) en `brian`. Version bump + CHANGELOG + memoria + RETOMAR + Bitácora.
- Propagación al resto de instancias = decisión de Brian DESPUÉS de vivirlo unos días en `brian`.

## 5 · Riesgos y frenos

- **Spam/fatiga** → frenos duros de F2 (1-2/día, /proactivo, silencio antes que relleno). El
  peor enemigo del valor de retorno es el insight vacío: **mejor callar que decir nada.**
- **Costo tokens** → mining con sonnet sobre material acotado y gobernado (governor + ROI);
  clase OFF por default fuera de `brian`.
- **Privacidad** → mining por sesión, entrega solo al dueño de la memoria, audit inmutable.
- **Kill switch** → `FOR3S_DMN_OFF` (ENV, manda sobre BD) apaga TODO incl. la clase valor.

---

**⏳ ESPERANDO:** OK de Brian para arrancar F1 (server-primero, commit firmado por fase).
