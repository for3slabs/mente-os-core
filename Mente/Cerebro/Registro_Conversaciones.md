# 📊 Registro de Conversaciones — telemetría de sesiones de Claude Code

> **Qué es:** el historial clínico de cada conversación (sesión) de Claude Code de este proyecto:
> cuándo inició/cerró, peso, temas, problemas, y **en qué momento el consumo empezó a crecer de
> forma excesiva o aparecieron cosas raras**. Nació del incidente del jueves 9-jul (3 mensajes →
> 100% del cupo) — la sesión monstruo nos enseñó que sin telemetría no se ve venir.
>
> **⚡ REGLA (en CLAUDE.md, obligatoria):** cuando Brian dé `/clear`, ANTES de cerrar se registra
> aquí la sesión que muere: fila en la tabla + sección con su autopsia. Sin registro no hay /clear.

**Owner:** Brian López · **Inicio del registro:** 2026-07-14 · **Capa:** Cerebro (telemetría)

---

## 🚦 Umbrales y señales de alerta (calibrados con datos reales)

| Señal | 🟢 Sano | 🟡 Vigilar | 🔴 Actuar (/clear ya) |
|---|---|---|---|
| Peso del jsonl | < 15 MB | 15-50 MB | > 50 MB |
| Contexto vivo por request | < 200K tokens | 200-500K | > 500K (con [1m]; a 1M cada cache-miss ≈ $) |
| Edad de la sesión | días | 1-2 semanas | semanas/meses sin /clear |
| Cache-miss (input o cache_write ≈ contexto completo) | esporádico | tras cada pausa | cada pausa >5 min con contexto grande |
| "Cosas raras" | — | respuestas que mezclan temas viejos | errores/límites (`<synthetic>`), cupo agotado |

**La física del costo:** el peso en disco NO es el problema directo — lo es el **contexto vivo**:
cada pausa mayor al TTL del caché (5 min default / 1h a veces) re-escribe TODO el contexto a precio
premium. Contexto de 1M = "hola" cuesta ~1M tokens. Contexto de 30K = centavos. Por eso: /clear al
cerrar bloques (RETOMAR.md guarda el estado, no se pierde nada).

---

## 📒 Índice de sesiones

> ⚠️ **Las horas van en LOCAL (CST, UTC−6), nunca en UTC.** Medido 2026-08-18: S13 y S14 tenían
> escrita la hora UTC del `.jsonl` **etiquetada como local** — S14 decía cerrar 20:33 cuando el
> transcript cierra 20:36:53Z, que aquí son las **14:36**. Un desfase de 6h en la hora de cierre
> es indistinguible de una sesión que siguió viva media jornada más, y esa es exactamente la
> pregunta que este índice existe para responder. Las duraciones sí estaban bien calculadas: se
> corrigieron las horas, y de paso los spans reales medidos del transcript (111h y 150h).
>
> ⭐ **S13 y S14 comparten un solo `.jsonl` (`4c2f0014`), 262h sin corte** — 11 días, el récord
> del proyecto. Por eso el arranque del 18-ago midió 262h: **la suma de las dos jornadas**, no
> una sesión abierta. Dos filas sobre un mismo transcript son legítimas (la jornada es la unidad
> de trabajo, el `.jsonl` la del archivo) pero el lector debe saberlo, o lee un contador roto.

| # | ID (corto) | Inicio (local, CST) | Fin (local, CST) | Peso | Msjs Brian | Contexto máx | Veredicto |
|---|---|---|---|---|---|---|---|
| S1 | `2a5131d3` | 2026-05-28 | 2026-07-13 | **278 MB** 🔴 | ~2,900 turnos | **~985K tokens** 🔴 | LA MONSTRUO — causó el incidente del jueves |
| S2 | `3f5bbe0d` | 2026-07-13 20:28 | 2026-07-14 06:03 | 3.4 MB 🟢 | ~26 | **549K 🔴** | Maratón H13+Frente B — productiva; /clear al cruzar el umbral rojo de contexto |
| S3 | `c9ef4299` | 2026-07-14 ~11:00 | 2026-07-15 (activa) | 8.7 MB 🟢 | ~40 | ~n/d | **La jornada MERCADO** — v0.17.0: Frente B F4-F6 + Molde For3s Inside (M1-M4) + For3s Trace completo + panel temporal. ~22 commits, ~10 bugs (1 SEC grave). Sana; sin señales raras |
| S4 | `c154a2ba` | 2026-07-18 18:38 (Mx) | 2026-07-19 ~18:30 (Mx) | 4.2 MB 🟢 | ~29 | **667K 🔴** | **LA JORNADA DEL SUPER-CEREBRO (30h)** — entrenamiento+examen de AMBOS agentes, 12 fixes sistémicos, v0.19.0 desplegada total. La más productiva de la historia del proyecto; /clear al cierre por contexto rojo |
| S5 | `7e9ce3b7` | 2026-07-24 20:58 | 2026-07-26 ~06:22 (~33h) | 12 MB 🟢 | ~97 | **917K 🔴** | **LA JORNADA DEMO → PRODUCTO** — BD reestructurada (F1-F6) + cableado + pulido P1-P7 + optimización (heartbeat −68%) + 9 bugs. Sana en disco pero **contexto en rojo**: /clear recomendado al cerrar |
| S6 | `dac2ce13` | 2026-07-26 ~06:00 | 2026-07-26 ~23:50 (~18h) | 5.9 MB 🟢 | ~60 | ~n/d | **LA JORNADA DE LOS CIMIENTOS DE LA DEMO** — 6 archivos a producto + Ronda F0 `userStore` (U1-U6, C6p2 cerrado) + `container.ts` activado + `DEMO_ENC_KEY` unificada + rebuild del agente. ~15 bugs (3 de seguridad). **2 caídas de producción causadas por mí.** Sana en disco |
| S7 | `4fc1996c` | 2026-07-26 18:03 | 2026-07-31 13:51 (**~116h**) 🔴 | 12 MB 🟢 | 1,087 turnos | **998K tokens** 🔴 | **LA JORNADA DE MENTE OS v2** — el sistema pasa de documentar a GOBERNAR: 11 validadores + 4 hooks + 3 niveles de reglas + migración v1→v2 completa (M0-M5, 186 docs, 4 carpetas eliminadas). `test-f0-f6` = 105/105. **Contexto máximo del proyecto — supera a S1 (985K), la monstruo.** 9 bugs propios, todos cazados por validadores |
| S8 | `523998b8` | 2026-07-31 13:51 | 2026-08-02 16:43 (**~51h**) 🔴 | 5.6 MB 🟢 | 670 turnos | **722K** 🔴 | **LA JORNADA DE ENDURECER EL v2** — F8-4 pasó (el brief bastó) y luego 12 commits cerrando huecos que la propia auditoría destapó: el token de GitHub expuesto · el guardia que vigilaba 9 de 21 · el cableado de los hooks · el latido F1+F2. Mente OS v2 **publicado en GitHub**. Batería 105 → 138 |
| S10 | `1b9338a4` | 2026-08-03 12:51 | 2026-08-03 20:31 (**~8h**) 🟢 | 2.1 MB 🟢 | 237 turnos | **261K** 🟡 | **LA JORNADA DE LA VOZ** — el output style pasó de 8 reglas negativas a un CONTRATO DE ENTREGA: §6 de `owner-0-voice` (hueco de criterio de Brian) LLENO con sus palabras + 3 modos 🟢🟡🔵 + jerarquía de títulos + línea de salud + antes/después/puente + destinatario. **Se corrigieron las 2 reglas que CAUSABAN el problema** (la 2.5 ordenaba cortar el cierre; la 2.8 dejaba omitir el porqué). Vehículo adelgazado 5,167 → 2,644 tokens (**−48% por turno**). Sin commit |
| S9 | `dc733bc1` | 2026-08-02 16:43 | 2026-08-03 12:51 (**~20h**) 🟡 | 7.7 MB 🟢 | 1,637 turnos | **681K** 🔴 | **LA JORNADA DEL AGENTE INSTALADOR** — 8 hallazgos de una misma familia (checks que corrían, decían verde y no medían lo que decían) → plan de raíz F1-F4 + `rule-checks-must-measure`. Citas rotas 144 → **0**. Bypass del `deny` cerrado (python3/node/bun leían lo prohibido). Bloque `distribucion` abierto y **6/6 construido**: un clon con otro dueño se instala solo, probado en clon real. Batería 138 → 160 |
| S11 | `8b4bddcb` | 2026-08-04 02:31 | ⚠️ **NO cerró aquí** — el mismo `.jsonl` siguió vivo hasta 08-07 21:26 (ver S12) | 11.8 MB → 25 MB | 65 → 2,381 | **999,757 → 1,000,030** 🔴 | **LA JORNADA DEL CRITERIO Y LOS TESTS** — los 66 huecos de criterio de los 3 dueños **cerrados a 0** (Brian responde con casos reales, la IA estructura) + rendimiento **86x** (`check-links` 47.2s → 0.55s) + la demo pasa de **0 a 4 archivos de test**. Batería 160 → **178**. 🔴 **Contexto máximo de la historia del proyecto: supera a S7 (998K) y a S1 la monstruo (985K)** |
| S12 | `8b4bddcb` (mismo) | 2026-08-05 23:07 | 2026-08-07 22:41 (**~47h**) 🔴 | **27 MB** 🟡 | 2,499 turnos acum. | **1,000,030** 🔴 | **LA JORNADA DEL CLON QUE POR FIN VERIFICA** — la batería daba 195/0 aquí y **22 fallos en un clon**; lo destapó una auditoría externa, no el sistema. 12 PRs (#1-#12). Familia D crece a **8 casos**: el peor (`grade-block archived`) se ataba a la instancia **sin nombrarla**, por el exit code bajo `pipefail`. Clon **10 → 1 fallo**. 🔴 **Contexto máximo histórico: 1,000,030 — el primero en superar el millón**, por encima del 21-jul (999K) |
| S14 | `4c2f0014` | 2026-08-12 02:17 | 2026-08-18 14:36 (**~150h**) 🔴 | **41 MB** 🟡 | **3,526 turnos** (acum.) | **999,702** 🔴 | **LA JORNADA DEL PRIMER BLOQUE** — el DOSSIER para el consultor (1,016 líneas), las 3 piezas de regla, y **el bloque 1 de 12 abierto y llevado a 6/11**. ⭐ El hallazgo mayor: *"se construye la pieza y no se conecta"* apareció **3 veces** (cripto · workspaces · BYOK). 🔴 **cache_read 1,696M — nuevo máximo histórico, supera a S13 (1,347M)**. ⚠️ **Mismo `.jsonl` que S13: 11 días sin corte, el récord del proyecto.** 3 errores míos + 1 de forma que Brian corrigió dos veces |
| S13 | `4c2f0014` | 2026-08-07 17:05 | 2026-08-12 02:17 (**~111h**) 🔴 | **36 MB** 🟡 | 1,530 turnos | **999,702** 🔴 | **LA JORNADA DE LA VERDAD DE V1** — 50 auditorías al servidor + lectura de ~45,000 líneas de Mente OS. Nacen 3 documentos (4,715 líneas): el terreno del código, el del conocimiento y **`LA-VERDAD-DE-V1.md`**. ⭐ Se resolvió la VARA de la campaña (el gate de la fase, no el Grafo) y los 24 hallazgos se redujeron a **4**. 🔴 **cache_read 1,347M — el máximo histórico, supera al 21-jul (1,033M)**. 8 errores míos corregidos en voz alta |
| — | `4c187f33` | 2026-07-20 00:32 | 2026-07-23 23:42 (**~96h**) 🔴 | **23.4 MB** 🔴 | 1,256 turnos | **999K tokens** 🔴 | 🔴 **R1 · LA SESIÓN DEL INCIDENTE DEL 21-JUL** — registrada retroactivamente el 31-jul (S8). Es la que `rule-session-close.md` §2 cita como *"el peor infractor"*. Ver §R1 |
| — | `fa2c625f` | 2026-07-15 21:01 | 2026-07-19 00:38 (**~76h**) 🔴 | 10.1 MB 🟢 | 1,180 turnos | **999K tokens** 🔴 | 🔴 **R2 · LA JORNADA SEGURIDAD/SEC-4c** — registrada retroactivamente el 31-jul (S8). Ver §R2 |
| — | `b075269c` | 2026-06-16 05:43 | 2026-06-27 23:58 (**~11 días**) 🔴 | 12.9 MB 🟢 | 661 turnos | 679K 🔴 | 🔴 **R3 · LA JORNADA H5-H10** — registrada retroactivamente el 31-jul (S8). Ver §R3 |

### S3 · `c9ef4299` — la jornada MERCADO (v0.17.0)
- **Temas:** arranque en Frente B F4 (panel admin Railway) → F5 carga (2000 conc, 2 races cazados) →
  F6 estándar datos + /v1/olvidar. Luego **Molde For3s Inside** (M1 contrato · M2 SDK · M3 onboarding
  · M4 trazabilidad) con auditoría caza-bugs (🔴 SEC: inyección LIKE en /v1/olvidar, EXPLOTADO+fix).
  Luego **For3s Trace** completo (T1 vocabulario · T2a-c recibir/analizar/alertar · alertas ricas con
  punto exacto en el panel · T3 ejemplo). Panel: uso por temporalidad. Duda del GIL resuelta.
- **Salud de la sesión:** 8.7 MB (🟢 <15), sin `<synthetic>`, sin mezcla de temas viejos, sin cupo
  agotado. Muchos rebuilds del contenedor (esperados). Consumo estable — no creció excesivo.
- **Cierre:** v0.17.0 commiteada, tríada `ccc3fb0`, Mente OS actualizado (Bitácora + RETOMAR
  comprimido a 193 líneas + CLAUDE.md + 3 memorias nuevas). Listo para /clear si Brian lo pide.

---

## S1 · `2a5131d3` — LA SESIÓN MONSTRUO (28-may → 13-jul-2026, 47 días)

- **Peso final:** 278 MB · 53,907 líneas · ~35 días activos. 21× más grande que cualquier otra.
- **Temas (toda la vida del proyecto):** rondas de diseño R1-R10 → construcción C0-C1 → hitos
  H1-H12 → contenerización → profesionalización PR1-PR10 → rediseño memoria → identidad viva →
  multi-instancia → entrenamiento E0-E6 → canal API → Incubathon → post-Incubathon.
- **📈 Cuándo empezó el crecimiento excesivo (autopsia por fases):**
  - **28-may → 8-jun:** sana. Modelo opus-4-7, contexto chico, cache-reads < 100M/día.
  - **9-jun:** primer salto — cambio a opus-4-8 + días de 300M tokens de cache-read. Señal 🟡.
  - **14-jun en adelante:** días de ~500M cache-read; el contexto por request crece sin freno
    (la ventana [1m] permite crecer sin compactar — nunca hubo /clear).
  - **3-jul (pico):** 918M tokens de cache-read en UN día.
  - **8-jul:** contexto vivo ~915K tokens. Cada mensaje arrastraba una novela.
  - **🔴 9-jul (EL INCIDENTE):** 5 cache-misses de ~935-980K tokens c/u (03:10 · 04:43 · 18:01 ·
    19:37 · 19:51) porque el TTL era 5 min y cada pausa re-escribía TODO. Los 3 fatales de la
    tarde: "hola" (970K) → "define for3s" (975K) → "oye estoy ocupando el bot" (980K + error =
    **cupo agotado, día perdido**). Equivalente API del día: >$100-200. El /model a fable-5 fue
    DESPUÉS, ya sin cupo.
- **Cosas raras detectadas:** respuestas lentas al final · el error `<synthetic>` (límite) ·
  compactación forzada 23:14 del 9-jul ("ran out of context").
- **Problema raíz (3 factores):** 47 días sin /clear + ventana [1m] sin compactación + TTL 5 min.
- **Descartado con evidencia:** NO proceso de fondo, NO entrenamiento nocturno (cero requests en
  huecos idle). Forense completo: PENDIENTES §Frente A + memoria `feedback_moderar_consumo_sesion`.
- **Cierre:** /clear el 2026-07-13 ~14:28. El archivo queda en disco como evidencia histórica.

## S2 · `3f5bbe0d` — Maratón H13 DEVUELVE + Frente B (13-jul 20:28 → 14-jul 06:03, ~10h)

- **Peso:** 3.4 MB · 1,214 líneas · ~26 mensajes de Brian (+ trabajo autónomo MUY intensivo).
- **Consumo:** cache_write 4.0M · cache_read 170M · output 941K. **Contexto máx 549K 🔴** —
  cruzó el umbral rojo (500K con [1m]) al final; por eso el /clear ANTES de F4 (bloque grande nuevo).
- **Temas:** Frente A cerrado (forense del incidente del jueves) → **HITO H13 "DEVUELVE" completo
  F0→F5** (v0.16.0: mina + digest + por-cierto contextual + feedback) → fix BUG-EQUIPO sellado +
  push (`06c5f99`) + 4 instancias a v0.16.0 → creación de ESTE registro (regla /clear) → **FRENTE B
  F0-F3**: Ronda del puente de mercado (13 bugs + comparativo túneles) · F1 demo con URL FIJA
  (Tailscale Funnel `for3s.tail6749e5.ts.net`, `2bf4a99`) · F2 control de acceso preciso
  (estados/keys f3k_/scopes, `79b156d`) · F3 cuotas + metering persistente (`330b891`).
- **📈 Consumo excesivo:** creció linealmente por el maratón (nada anómalo — trabajo real denso);
  el contexto pasó de ~430K (H13) a 549K (Frente B). Sin cache-misses catastróficos.
- **Cosas raras:** ninguna del sistema. Bugs de MIS scripts de prueba (heredoc que escapó comillas
  — el que advierte el Método F — y chr() enredado); resueltos con archivos + scp. TTL caché 1h.
- **⚠️ NOTA:** Brian reactivó `claude-fable-5[1m]` a mitad (el modelo caro del incidente) → razón
  extra para el /clear con contexto ya en 🔴.
- **Cierre:** /clear tras este registro, ANTES de arrancar F4 (panel admin). RETOMAR.md fresco.
  6 commits del Frente A/B en server SIN push (H13 ya pusheado en 06c5f99).

---

## S4 · `c154a2ba` — LA JORNADA DEL SUPER-CEREBRO (2026-07-18 18:38 → 07-19 ~18:30 Mx, ~30h)
- **Peso:** 4.2 MB · 2,075 líneas · ~29 mensajes de Brian (sesión sobrevivió 2 reinicios de
  Claude Code + 1 reboot del server + varios cortes de red).
- **Consumo:** cache_write 4.2M · cache_read **354.7M** · output 967K · **contexto máx 667K 🔴**
  (muy por encima del umbral — /clear obligado al cierre; el costo se moderó porque la mayoría
  del trabajo pesado fue $0: censo/embeddings/clustering locales, y lo LLM fue con freno).
- **Temas (la jornada más grande del proyecto):** (1) ENTRENAMIENTO FORESITO T0-T6 completo
  (1,829 eps, digestión acelerada 95%) · (2) 👑 Foresito = AGENTE MAESTRO + puente E dinámico ·
  (3) EXAMEN Foresito 98.8% → **12 hallazgos H-1…H-11+B1 TODOS con fix sistémico** (joya H-11:
  contraseña del server en 60 eps de 2 instancias → redactada+blindada) · (4) noches ADELANTADAS
  de brian (encadenador 10 tandas, 11,763→14) · (5) EXAMEN brian 94.3% (trampas 6/6) ·
  (6) v0.19.0 ENTRENADO: bump+changelog+push tríada+propagación 5 instancias+CI verde ·
  (7) sync TOTAL (4 repos GitHub + server + local + Maestro).
- **📈 Consumo excesivo:** el contexto creció rojo por la duración (30h, ~35 vigías/tareas de
  fondo); el cache_read enorme = cientos de tool-calls ssh. Sin incidente de cupo: frenos
  funcionaron (el examen se auto-frenó a 0.90 una vez).
- **Cosas raras (todas cazadas y documentadas):** PermissionError enmascarado por mi grep del
  log ("la red" no era) · pkill que se AUTO-mataba (patrón en mi propio cmdline ssh) ·
  encadenador muerto por limpieza de sesión (→ setsid SIEMPRE) · builds muertos por cortes de
  red (→ nohup SIEMPRE) · rebuild que mató al backfill (secuenciar recreates).
- **Cierre:** hito doble CERRADO + ecosistema entero sincronizado + esta autopsia + RETOMAR
  podado → /clear seguro. Todo vive en: Bitácora (entrada completa) · `Doc/Examen_Foresito_
  T6_Hallazgos.md` · `work/Ronda_Entrenamiento_Foresito.md` · memorias actualizadas.

---

## S5 · `7e9ce3b7` — LA JORNADA DEMO → PRODUCTO (2026-07-24 20:58 → 07-26 ~06:22 Mx, ~33h)

- **Peso:** 12 MB 🟢 (2,985 líneas) · **Mensajes de Brian:** ~97 · **Contexto máx: ~917K 🔴**
- **Veredicto:** sana en disco, **contexto en ROJO** (cerca del umbral de la monstruo). La causa no
  fue una fuga: fue el volumen real de trabajo (33h, ~97 turnos, mucha lectura de código + BD).
- **Temas (en orden):** F0 en producción (Resend/Vercel) → auditoría de la BD de la demo →
  **reestructuración F1-F6** → cableado C1-C6p1 → verificación integral → **auditoría de código**
  → pulido P1-P7 → **optimización O-F1..O-F5** → refactor de `for3sChat.ts` → limpieza del tema
  `hoteles` → rebuild del agente → documentación.

### Qué se logró
- **BD de MVP a producto:** `demo_instancias` como fuente única (modo, cupo, puente URL+key
  cifrada) · 7 FKs · catálogo de estados · `demo_llaves` revocables · `demo_eventos` ·
  **`demo_config`** (parámetros editables con UPDATE, sin push). **Escalar = 1 INSERT** (probado).
- **Código pulido:** la instancia deja de ser lista fija (27 archivos) · UNA puerta de acceso
  (antes 3 fuentes) · un solo cupo · **−434 líneas** de subsistema muerto · `for3sChat.ts`
  refactorizado con capa base (**−79% de plomería**).
- **Optimización medida:** heartbeat 11→3-4 viajes a Neon (**−68%**), N+1 eliminado, freno de
  mantenimiento (260→4 en 60 s). Con 100 usuarios: 220→70 q/s.
- **9 bugs cazados y cerrados** (varios de seguridad/coherencia).

### Cosas raras / lecciones de la sesión
- **El contexto creció temprano y no bajó** — desde ~la mitad de la jornada ya era grande por
  leer código extenso (`userStore.ts` 485 líneas, `for3sChat.ts` 362) y volcados de BD. Señal para
  futuras jornadas de auditoría: leer por tramos y resumir, no arrastrar archivos enteros.
- **404 local que parecía la BD y era caché de `.next`** — costó rato; lección: 404 de FRAMEWORK
  (HTML) ≠ 404 de aplicación (JSON). Si caen varias rutas hermanas a la vez → es caché.
- **Un fix mío PELIGROSO que Brian cazó** — iba a poner `general` (hilo del dueño) como tema por
  defecto. De ahí salió el caso de estudio `memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` y la regla
  "un default nunca apunta a algo con dueño". **La revisión de Brian evitó un problema real.**
- **Dije "esto rompería cualquier cliente API" sin medirlo** — al comprobarlo, solo afectaba a las
  keys f3k_. Lección registrada: las afirmaciones de impacto se comprueban.
- **Rebuild del agente:** el primer intento no recreó el contenedor (compose equivocado); la vía
  correcta es `docker compose -p for3s-brian -f docker-compose.instancia.yml up -d --force-recreate`.

### Cierre
Todo pusheado: sitio `1c54a49` (ElBrAyAn1967/For3s) · Mente OS `d9d456c` (for3slabs/mente-os-for3s)
· agente reconstruido y `brian` reiniciado con el código nuevo (verificado en vivo: sin tema →
`sin-tema`, con tema → `general`). **`hoteles` eliminado del sistema.**
Documentación: 4 planes `DEMO_*.md` en el repo del sitio + caso de estudio + Bitácora + memorias.
⚠️ **/clear recomendado** al cerrar: el contexto quedó en rojo (~917K).

---

## 📋 Plantilla para registrar una sesión (copiar al cerrar)

```markdown
## SN · `<id-corto>` — <apodo> (<inicio> → <fin>)
- **Peso:** X MB · N líneas · ~N mensajes de Brian.
- **Consumo:** cache_write · cache_read · output · contexto máx por request.
- **Temas:** qué se trabajó (bloques grandes).
- **📈 Consumo excesivo:** ¿cuándo empezó a crecer? ¿hubo cache-misses grandes? (si fue sana: "no").
- **Cosas raras:** errores, lentitud, mezcla de temas, límites (si nada: "ninguna").
- **Cierre:** por qué se cerró (fin de bloque / peso / incidente) + RETOMAR actualizado ✓.
```

> **Cómo medir** (comando de referencia): el jsonl vive en
> `~/.claude/projects/-home-brianweb3-for3s/<id>.jsonl` — peso con `ls -lh`, y tokens/contexto
> leyendo los campos `usage` de los mensajes assistant (script en la memoria del incidente).

---

## S6 · `dac2ce13` — LA JORNADA DE LOS CIMIENTOS DE LA DEMO (2026-07-26, ~18h)

**Inicio/fin:** 2026-07-26 ~06:00 → ~23:50 (Mx) · **jsonl:** 5.9 MB 🟢 (2,394 líneas) ·
**mensajes de Brian:** ~60 · **veredicto: SANA en disco.** Muy por debajo del umbral (15 MB),
la mitad que S5. El trabajo fue de mucha herramienta y poco texto largo.

### Qué se hizo
Continuación directa de S5. Si S5 reestructuró la BD, S6 reestructuró **el código**:
- **6 archivos elevados a producto:** `instancias.ts` (I1-I5) · `session.ts` (S1-S3) ·
  `verificacion.ts` (V1-V4) · `eventos.ts` · S4a "cero listas fijas" · **`userStore.ts`
  Ronda F0 completa (U1-U6)** → **C6p2 CERRADO** (fuera la columna `kind` y `demo_accounts`).
- **`container.ts` ACTIVADO** (modelo C: la BD como buzón, `/ctl` nunca se expone).
- **`DEMO_ENC_KEY` rotada y unificada** local=Vercel (eran distintas desde junio).
- **Rebuild del agente** (`for3s-agent:local`): el cupo agotado ya sale como 429 + minutos.
- **La demo marcada como BLOQUE GRANDE** con índice maestro de pendientes.
- ~15 bugs reales, **3 de seguridad**: anti fuerza bruta burlable (reenviar código reseteaba
  el contador) · un invitado podía apagar el agente del dueño · eliminar persona no revocaba
  su llave.

### 🔴 Cosas raras / incidentes
1. **DOS caídas de producción, ambas causadas por mí y por el MISMO error de método:**
   verificar desde mi entorno y asumir que probaba el de Vercel.
   (a) retiré el fallback de env vars sin comparar la `DEMO_ENC_KEY` de Vercel — resultó
   distinta desde junio, y el fallback lo estaba tapando. (b) usé `tailscale serve` en vez de
   `funnel` al exponer jazz/mashe, y eso **degradó el Funnel entero a tailnet-only**: mis
   pruebas pasaban (estoy dentro del tailnet) mientras producción estaba caída.
   → Reglas escritas: `feedback_tailscale_serve_apaga_funnel` · `project_rotacion_demo_enc_key`.
2. **Borré 4 eventos reales de Brian** al limpiar datos de prueba con un filtro por tiempo
   demasiado amplio. Restaurados con sus valores y horas originales.
3. **SSH al server con timeouts repetidos** (enlace por relay, ~833ms). Se paró sin insistir,
   aplicando la regla de no hacer bucles contra el server.
4. **El patrón `await fetch` sin mirar la respuesta apareció TRES veces** en el mismo día
   (reenviarCodigo · toggle del agente · desconectarGithub). No es casualidad: es un hábito
   del código base. Quedan más en las partes no barridas.

### Consumo
Sin señales de crecimiento excesivo. El grueso fue Bash/Read/Edit con salidas cortas, no
lectura de archivos grandes. **No hubo lectura de `Estado_Sesion_Continuidad.md`** (200KB) ni
de otro Mente OS. El único gasto notable fue el rebuild de la imagen (328s, en segundo plano).

### Motivo de cierre
Brian cierra un bloque grande de trabajo, no por saturación. Estado documentado en
`project_bloque_demo_pendientes` (índice maestro) + RETOMAR §5 reescrito.

---

## S7 · `4fc1996c` — LA JORNADA DE MENTE OS v2 (2026-07-27 00:03 → 07-31 19:41, ~116h)

- **Peso:** 12 MB · 1,087 turnos de Brian.
- **Consumo:** cache_write 9.0M · cache_read **914.9M** · output 1.86M · **contexto máx 998,782 tokens**.
- **Temas:** Mente OS v2 completo (F4→F8-3) + migración v1→v2 (M0-M6).

### Qué se hizo

**El sistema pasa de DOCUMENTAR a GOBERNAR.** Es el bloque más grande del proyecto después
del propio For3s.

| Frente | Resultado |
|---|---|
| **F4 medir** | `bin/grade-block` — veredicto MEDIDO, nunca opinión. ADR-028: el TIPO del bloque decide el métrico |
| **F5 verificar** | 4 hooks. Solo `pre-commit` bloquea; los demás informan |
| **F6 garantizar lectura** | `pre-edit-standards.py` inyecta los §D del bloque dueño |
| **F7 índices** | `generate-index` → `docs/INDEX.md` + `docs/STATES.md` generados |
| **F8-1..3** | Primer bloque CERRADO y archivado: `split-architecture` 🟢 PRODUCT |
| **M0-M5** | 186 documentos migrados uno por uno. **4 carpetas v1 ELIMINADAS** |
| **3 niveles de reglas** | 🌐 `base-rules.md` → 🏢 `PROJECT-RULES.md` → 📦 `BLOCK.md §B` |
| **Sistema de apuntado** | `piezas.tsv` — mover una pieza cuesta 1 línea |

`bin/test-f0-f6` = **105/105**. 11 validadores, 4 hooks.

### 🔴 Cosas raras / incidentes

1. ⭐⭐ **LA CONTRASEÑA REAL DEL SERVIDOR (`«en secrets/Conectar_Servidor_For3s.md»`) llevaba en la arquitectura desde el
   27-jul**, dentro de un ejemplo de "qué NO hacer". Salió a la luz solo cuando partir el
   documento hizo que `grade-block` lo leyera. Redactada en los dos archivos.
2. ⭐ **`Maestro/punteros.tsv` apuntaba a `memory/RETOMAR.md`** — y Foresito lo lee EN VIVO por
   MCP. Lo cazó el validador al mover RETOMAR. Sin ese aviso: índice roto en producción.
3. 🔴 **`indexador.py` estaba roto**: su regex buscaba `Alma|Cerebro|Cuerpo|Doc|Maestro` y
   tres de esas carpetas fueron eliminadas en M1-M5. No encontraba NADA de la estructura v2.
4. 🔴 **Me rompí a mí mismo 3 veces con reescrituras masivas de rutas.** Un `git checkout -- .`
   en el revert de `migrate-doc` tumbó los fixes de 6 validadores en silencio: la batería pasó
   de 103/103 a 13 fallos. **Regla nueva: un revert debe ser tan estrecho como el cambio.**
5. **`migrate-doc` comparaba TOTALES, no conjuntos** — revertía por deuda que el documento ya
   traía. `README.md` revirtió tres veces por esto.

> ⭐ **Los 9 bugs los cazó un validador, ninguno leyendo.** Esa es la ley medida del sistema:
> una regla en código se cumple 100%, una regla en documento 40-60%.

### 📈 Consumo excesivo

🔴 **Sí, y es el dato más importante de esta sesión.** **998K de contexto máximo — supera a S1
(985K), la sesión monstruo que causó el incidente del 21-jul.** 116 horas abiertas: el hook de
arranque avisó a las 96h, exactamente el umbral del incidente.

**914 millones de cache_read** es la física del costo en vivo: cada pausa mayor al TTL
re-envía el contexto completo. El trabajo fue sano y quedó en disco — el problema es la
antigüedad de la sesión, no lo que se hizo en ella.

### Motivo de cierre

Bloque grande terminado y **commiteado** (`42dbfab`, 279 archivos). Se cierra por contexto en
rojo y por edad. El `/clear` es además **la prueba F8-4**: retomar tras un corte real es la
única fase de v2 que falta verificar.

---

## S8 · `523998b8` — LA JORNADA DE ENDURECER EL v2 (2026-07-31 19:51 → 08-02 22:09, ~50h)

**Peso:** 5.6 MB 🟢 · **670 turnos** · **contexto pico 722K** 🔴 · cache_read 476M · output 610K.
**12 commits** (9 en `Mente/`, 3 en la raíz). **Batería: 105 → 138 verificaciones.**

Empezó como la prueba F8-4 —¿basta el brief para retomar?— y se convirtió en una auditoría del
sistema contra sí mismo. **El brief bastó** (cero preguntas de estado), y lo que siguió fue
cerrar los huecos que la propia verificación destapó.

### 🔴 El hallazgo que más importó — el patrón, no los bugs

Cinco veces el mismo error, y **ninguna se vio como patrón hasta la cuarta**:

| Guardia | Vigilaba | No vigilaba |
|---|---|---|
| `check-clear-ready` | una ruta | si la ruta seguía existiendo (la borró la migración) |
| `deny` | Read/Edit/Write | **Bash** — `cat` leía lo que `Read` prohibía |
| `SENSITIVE` | 3 rutas de credenciales | **gh · aws · gnupg · 2 tokens sueltos** |
| `GUARDS` | 9 archivos | **los otros 12**, incluida la batería entera |
| hooks | que el archivo exista | **que siguiera registrado** |

> ⭐ **En los cinco, cada mitad estaba vigilada y NADIE vigilaba la costura** — que es
> literalmente la regla del proyecto: *"los bugs trágicos viven ENTRE las piezas"*.

**La regla que salió, y vale más que los cinco arreglos:** una lista que enumera lo **PROTEGIDO**
debe medirse; una que enumera lo **PERMITIDO** puede escribirse, si lo desconocido **falla
cerrado**. Se auditaron las 22 enumeraciones de los validadores: **19 estaban bien**, y varias
lo estaban a propósito.

### 🔴 Lo más grave: el token de GitHub estuvo expuesto

`Read(//home/**)` concedía todo `$HOME` y el `deny` cubría 5 objetivos. Quedaban al aire
`~/.config/gh/hosts.yml` (el token), `~/.aws/credentials`, `~/.gnupg`, y dos archivos sueltos
que **solo aparecieron cuando el guardia pasó a descubrir en vez de consultar una lista**.

El guardia existía y callaba. **No estaba roto: miraba el sitio equivocado.**

### Qué se construyó

- **Delegación acotada** — contrato + esquema + validador + **puerta que bloquea de verdad**
  (probada en vivo: me bloqueó a mí lanzar un `general-purpose`).
- **`session-wrap`** — la skill que está cerrando esta sesión. Primer uso real.
- **Apuntadores en vez de números** — `docs/METRICS.md` generado. Nació porque `SKILL.md`
  congeló `105/105` **horas después** de arreglar ese mismo bug en `RETOMAR.md`.
- **Motor / instancia separados** — `mente.config.yml`. Probado clonando de verdad.
- **El latido (F1+F2)** — el arranque y las 3 puertas dejan prueba de que siguen vivos.
- **Mente OS v2 PUBLICADO**: `github.com/fruterito101/mente-os`, MIT, 97 archivos, historial
  limpio desde cero. Escaneadas 14 categorías de datos sensibles antes de publicar.

### 🟡 Errores de método propios, para no repetirlos

1. **Rompí `settings.json` sin avisar antes.** Fue en copia y restaurado, y era la única forma
   de saber si los guardias avisan — pero tocar la config que gobierna el sistema merecía
   pedir permiso primero. Brian lo notó: *"¿por qué borras los hooks?"*
2. **Dije "20 commits" sin medirlos.** Eran 12. Un número estimado en una sesión cuya regla es
   *"no afirmar sin medir"*.
3. **Cumplí mi propia regla a medias el mismo día de escribirla.** `rule-config-hygiene` §1.5
   dice *"la superficie se declara completa, no por herramienta"* — la apliqué a las
   herramientas y no a los objetivos, y por eso el token siguió expuesto horas más.
4. **F3 del plan del latido quedó sin cerrar explícitamente.** La desaconsejé al proponerla y
   nunca dije que quedaba descartada; Brian tuvo que preguntar *"¿pero no teníamos F3?"*.

### 📈 Consumo

**722K de contexto pico** 🔴 — sobre el umbral rojo (500K). 50h abiertas. 476M de cache_read.
El peso en disco es sano (5.6 MB); **lo que está en rojo es la edad y el contexto**, que es
exactamente el patrón de las 3 sesiones huérfanas: mueren de edad, no de tamaño.

### Motivo de cierre

Contexto en rojo y 50h abiertas, con el precedente del 21-jul (999K, 4 días) que originó medio
sistema. Todo el trabajo está commiteado y verificado: **batería 138/138**.

**Peso:** 0.2 MB 🟢 · 17 turnos de Brian · **contexto máx 63K** 🟢 · cache_read 1.2M.
Comparación con el arranque de S7 (que abrió leyendo 200 KB de historia): esta arrancó leyendo
**un archivo de 272 líneas.** Ese contraste es el resultado de F8-4.

### El veredicto de F8-4: ✅ EL BRIEF BASTÓ

Brian dijo *"lee retomar"*. Con **solo** `memory/RETOMAR.md` quedó resuelto: quién es, qué es el
proyecto, dónde vive, en qué fase está, cuál es el próximo paso y qué NO hay que hacer.
**Cero preguntas a Brian sobre estado.** Lo que siguió fue *verificar*, no *averiguar*.

### 🔴 Los 3 huecos que la prueba destapó (el hallazgo que F8-4 existe para dar)

| # | Hueco | Por qué importa |
|---|---|---|
| 1 | El brief afirmaba `test-f0-f6` = **105/105**; la medición dio **104/105** | El número **no es estable a través de un `/clear`**: la batería incluye `check-clear-ready`, que evalúa la sesión VIVA. Tras cualquier corte arranca en 104 y solo llega a 105 al registrar. El brief congeló un valor variable y lo presentó como "la verdad" |
| 2 | RETOMAR tenía **272 líneas** violando su propia regla de ~200 | La regla estaba **escrita dentro del archivo que la incumple**, sin nada que la aplique. Ley medida del proyecto, otra vez |
| 3 | **Dos fechas de actualización en conflicto** (cabecera 30-jul · línea 17 26-jul · contenido 31-jul) | Al leer hubo que ignorar ambas y confiar en el cuerpo. Un brief cuya fecha no es fiable erosiona la confianza en el resto |

> ⚠️ **Falsa alarma corregida en la misma sesión:** el hueco #1 pareció un test mal escrito. No lo
> es — `test-f0-f6` líneas 277-287 **ya** se adapta al registro, con un comentario de alguien que
> antes cayó en fijar la constante. El test estaba bien; el brief estaba desactualizado.

### Qué se hizo

- Registradas **las 3 sesiones huérfanas** que `check-health` llevaba marcando (§R1-R3), incluida
  🔴 `4c187f33` — **la del incidente del 21-jul**, que `rule-session-close.md` §2 cita como *"el
  peor infractor"* y que **seguía sin entrada 10 días después de escribirse esa regla.**
- Tapados los 3 huecos del RETOMAR.

### Cosas raras

Ninguna. Sesión sana en todos los ejes.


## S14 · `4c2f0014` — LA JORNADA DEL PRIMER BLOQUE (2026-08-12 08:17 → 08-18 20:33, ~154h) 🔴

**41 MB** 🟡 · **3,526 turnos** (acumulados con S13, mismo `.jsonl`) · **contexto pico 999,702** 🔴
· **cache_read 1,696,388,727** 🔴 ⭐ **nuevo máximo del proyecto — supera a S13 (1,347M) y al
21-jul (1,033M)** · cache_write 22.7M · output 2.2M.

🔴 **11 DÍAS DE `.jsonl` SIN CORTE (07-ago 23:05 → 18-ago 20:33) — el récord del proyecto.**
S13 y S14 comparten sesión: S13 nunca se cortó, solo se registró. El incidente del 21-jul detonó
a las **96h**; esto es **3.8×** eso. ⭐ **No hubo degradación medible esta vez** — y esa es
exactamente la trampa: el patrón de las 3 sesiones huérfanas es que **mueren de EDAD, no de
tamaño** (96h · 76h · 11 días, ninguna sobre 50 MB). Se cierra por tiempo, no por trabajo
terminado.

### Qué se hizo

| Fase | Entregable |
|---|---|
| **El DOSSIER para el consultor** | `vision/DOSSIER-SISTEMA-COMPLETO-2026-08.md` — 1,016 líneas, 15 §. Abre con la carta que dice **dónde falló la consultoría anterior** |
| **Las 3 piezas de regla** | la vara temporal (`rules/rule-product-authority.md` §2) · el campo `campaign_phase:` · su validador con 4 comprobaciones |
| **El plan de 3 fases** | `docs/plans/PLAN-3-fases.md` — una fase es una MIRADA, no un bloque |
| **⭐ EL BLOQUE 1 DE 12** | `seguridad` abierto y llevado a **6/11** — Fase 1 cerrada con veredicto por dimensión |
| **La batería** | 231 → **235** · 4 checks nuevos, los 4 por sabotaje |

### ⭐ Las 4 cosas que no se re-litigan

1. **Reparto del territorio = opción A** (un archivo, un dueño). Razón MEDIDA, no preferencia:
   `hooks/pre-edit-standards.py` se queda con **el primer** bloque que reclama un archivo, así que
   dos dueños dan la vara equivocada. Salida para el caso legítimo: el `§Channel`.
2. **H-01 se arregla con una CAPA ÚNICA.** Descartada la opción rápida (9 lectores descifrando por
   su cuenta) porque **repetiría el defecto que el propio bloque diagnosticó**.
3. **El techo se mira AL CERRAR, no durante** (Brian): mirarlo a mitad cambia QUÉ se escribe.
   §B subido a 20 con su razón.
4. **SB-9 antes que SB-10.** Al revés el sistema queda leyendo cifrado con código que espera texto
   plano — roto ENTRE dos pasos.

### 🔴 EL HALLAZGO MAYOR: el patrón apareció 3 veces

| Caso | La pieza existe | Y nadie pasa por ella |
|---|---|---|
| H-01 | `crypto.py` funciona | el contenido no se cifra |
| workspaces | `derive_workspace_key()` funciona | hay 1 solo |
| **BYOK** | **`LLMProvider(ABC)` existe** | **12 archivos instancian `ClaudeProvider` directo** |

⭐ *"Se construye la pieza y no se conecta."* **Tres veces ya no es un cable suelto: es cómo se ha
venido trabajando.** Y el tercero **bloquea una venta** (BYOK).

### 🩺 AUTOPSIA — 3 errores míos, los 3 corregidos en origen

1. 🔴 **Afirmé 3 veces que H-01 crecía a diario. Falso.** 99.5% es importado (ene-may); lo vivo son
   81 kB, parado hace 16 días. Deduje del peso de la BD y **nunca medí la fecha de las filas**.
   ⭐ Lo cazó SB-3 — la Fase 1 tumbó una premisa del bloque que la ejecutaba. **Si el arreglo
   hubiera ido antes, habríamos cifrado con la urgencia equivocada.**
2. ⚠️ **Declaré el SSH "bloqueador de los 12" sin leer `secrets/Conectar_Servidor_For3s.md`**, que
   documenta el método y lista ese error exacto con su solución. Coste: una decisión pedida a
   Brian que no hacía falta pedirle.
3. ⚠️ **Dije "10+ escritores" y son 2.** Conté los que MENCIONAN la tabla. El trabajo real está en
   los **9 lectores** — dimensionaba mal el arreglo.

### 📉 Y un error de FORMA que Brian tuvo que corregir dos veces

*"No entiendo si ya estamos realizando el bloque"* y *"cuando un bloque va avanzando me tienes que
dar el estado del bloque y todo referente a ese bloque, no solamente decirme qué sigue"*.
⭐ **Causa:** reporté pasos y arreglos del motor mezclados, sin separar **producto** de **motor** y
sin dar el estado completo del bloque. **La regla que queda: al avanzar un bloque, se entrega su
estado, qué se hizo, por qué así y qué archivos se tocaron — nunca solo el siguiente paso.**

### 👉 Dónde queda

`seguridad` **6/11** · la mitad que MIDE completa, la que ARREGLA sin empezar · rollback probado
(131 MB → 33,908 filas) · **cero cambios en producción** · batería 235/235.

---

## S13 · `4c2f0014` — LA JORNADA DE LA VERDAD DE V1 (2026-08-07 23:05 → 08-12 08:17, ~105h)

**36 MB** 🟡 · **1,530 turnos** · **contexto pico 999,702** 🔴 · **cache_read 1,347,949,789** 🔴
(el máximo del proyecto — supera al 21-jul: 1,033M) · cache_write 15.6M · output 1.6M.

### Qué se hizo

| Fase | Entregable |
|---|---|
| **El airlock** | `rules/rule-pr-batching.md` §5 — 3 niveles de revisión. **El agente deja de esperar al humano en cada PR** |
| **35 auditorías a For3s OS** | A1-A15 componentes · A16-A35 uso real con los datos de Brian · C1-C15 comportamiento y canales |
| **La lectura de Mente OS** | ~45,000 de 110,000 líneas — **el 100% de lo que gobierna, decide o registra** |
| **3 documentos, 4,715 líneas** | `AUDITORIA-FOR3S-OS` (980) · `AUDITORIA-MENTE-OS-CONOCIMIENTO` (2,451, 33 §) · **`LA-VERDAD-DE-V1`** (1,136, 17 §) |
| **La campaña** | 12 bloques decididos · el orden por gravedad · **la VARA declarada** |
| **La batería** | 228 → **232** · 4 checks nuevos, los 4 verificados por sabotaje |

### ⭐ Las 3 decisiones que no se re-litigan

1. **La vara de la campaña NO es el Grafo ni el código: es el GATE DE LA FASE EN CURSO.**
   Medido: contra el Grafo completo, For3s OS falla **15 de 15 tablas** — un rojo que declararía
   muerto un sistema que corre a diario. Contra el gate de su Fase 1: **pasa 6 de 6**, y los 24
   hallazgos **se reducen a 4**.
2. **12 bloques, en orden de gravedad** (Brian): `seguridad` abre porque H-01 **empeora cada día**.
   Y `entrenamiento` entra pese a 38 días sin escribir: *"2,192 líneas sin auditar no se dejan
   fuera del producto"*.
3. **La decisión de partir los archivos grandes se APLAZA con recordatorio registrado** — los 18
   archivos >400 líneas y su bloque dueño quedan en `AUDITORIA-FOR3S-OS` §16, con la obligación de
   preguntar antes de cerrar cada fase 2.

### 🔴 Los hallazgos que cambian el trabajo

| | |
|---|---|
| **H-01** | el contenido de las conversaciones está **EN CLARO** (15 MB) — y no es un olvido: **R2 B1 §1.6 lo lockeó cifrado**, y viola la anti-visión #9, declarada *no-negociable* |
| **H-02** | la búsqueda **cruza sesiones** (`incluir_import`) pero el contador **no** → un recuerdo importado se recupera y nunca se marca · **el sistema podría borrar lo que sí usa** |
| **H-04** | el `digest_valor` está programado a las 14:00 UTC y **el worker está apagado 8h/día** (11h-18h): su cartero corre a una hora en la que el sistema no existe |
| **Los 2 nodos ausentes** | **Amígdala** (nodo 7) y **Tálamo** (nodo 8) — confirmados por **cinco métodos independientes** |
| **Tres tableros congelados** | `bridges/` publica 5/18 · el Mapa 3/18 · el Grafo 11/11 — la realidad es **13 de 16 hitos** |

### ⭐⭐ Lo que se descubrió y nadie sabía

- **For3s OS va ADELANTADO:** su plan estimaba el MVP en 3-3.5 meses y el sistema completo en
  9-10. **Lleva ~2 meses de código con MVP + cerebro + aprendizaje gobernado.**
- **La microglía superó al estado del arte** que su propio diseño describía (*"nadie la implementa
  bien"*): **41% de la memoria podada**, con audit de cada olvido.
- **Nadie vio la divergencia diseño↔código porque la auditoría de junio comparó DOCUMENTOS con
  DOCUMENTOS.** Su propia §2.1 lo dice. El código nunca entró en la comparación.
- **Mente OS v2 nunca ha gobernado trabajo de producto:** los 5 bloques archivados son del motor.
  **La campaña será su prueba de campo.**

### ⚠️ 8 errores míos, corregidos en voz alta

E-1 *"76 archivos"* eran del núcleo (son 112 `.py`) · E-2 *"43 huérfanos"* eran **5** · E-3
`entrenamiento_repo` no es código muerto · E-4 *"36 consultas sin filtro"* — **ninguna** ·
E-5 reporté el servidor caído **estando encendido** (no leí `secrets/`) · E-6 los stubs del DMN no
son un fallo · 🔴 **E-7 *"la memoria está INALCANZABLE"* — FALSO**, desmontado ejecutando
`recordar()` en vivo · E-8 un `pgrep` que se detectaba a sí mismo, **cazado antes de escribirlo**.

⭐ **El patrón: medir una parte y hablar del todo, o inferir del esquema en vez de ejecutar el
código.** De ahí salen **L-32** (*un esquema describe lo que se PUEDE consultar, no lo que el
código consulta*) y **L-33** (*cuando una función LEE con un criterio y otra ESCRIBE con otro, el
sistema funciona y miente a la vez*).

### 🔴 Consumo — cuándo empezó a crecer

**Desde el arranque.** No hubo un punto de inflexión: la sesión nació con contexto grande (venía
de una compactación) y **las 50 auditorías + la lectura de 45,000 líneas lo mantuvieron en el
techo durante 105 horas**. El pico de 999,702 se alcanzó y se sostuvo.

📊 **cache_read 1,347 millones — el máximo histórico del proyecto**, por encima de la sesión del
21-jul (1,033M) que causó el peor incidente.

⚠️ **Y sin embargo NO hubo degradación observable:** cero `<synthetic>`, cero mezcla de temas
viejos, cero violaciones de alcance. **Los 8 errores fueron de método (medir mal), no de
contexto.** ⭐ **Es la primera sesión >100h del proyecto que cruza el millón de cache_read sin
degradarse** — dato que merece registrarse, no celebrarse.

### Motivo del cierre

Trabajo en frontera natural: la lectura de Mente OS **cerrada**, los 3 documentos **escritos y
verificados**, la vara de la campaña **resuelta**. Lo siguiente (`PLAN-3-fases` + contratos +
validador de `fase:`) es **trabajo delicado de escritura de reglas** — exactamente lo que no
conviene hacer con 105h y 999K de contexto.

---

## S12 · `8b4bddcb` — LA JORNADA DEL CLON QUE POR FIN VERIFICA (2026-08-05 23:07 → 08-07 21:26, ~46h)

> ⚠️ **Mismo `.jsonl` que S11.** El registro declaró a S11 cerrada el 05-ago 23:07 y la sesión
> siguió viva **46 horas más**. Se separa en dos entradas porque el trabajo es distinto, pero
> **el archivo nunca se cortó**: la fila de S11 quedó corregida con esa advertencia.
> ⭐ Registrar el cierre no es cerrar. `/clear` es lo que corta.

### Consumo — medido del `.jsonl`, no estimado

| Señal | Valor | |
|---|---|---|
| peso | 25 MB | 🟡 (rojo a 50) |
| duración | **90.9 h** acumuladas | 🔴 |
| turnos de usuario | 2,381 | |
| **contexto pico** | **1,000,030** | 🔴 **máximo histórico del proyecto** |
| salida acumulada | 2,152,579 tokens | |
| cache read | 2,257 M tokens | |
| API connection errors | 5 (los ve `check-health`; 0 en el `.jsonl` como texto) | 🟡 |

🔴 **Es la primera sesión que supera el millón de contexto.** El incidente del 21-jul
(`project_incidente_degradacion_21jul`) ocurrió a **999K y 4 días**; ésta llegó a 1,000,030 y
3.8 días. **La marca se cruzó, no se rozó.**

### Cuándo empezó a crecer anormalmente

Desde el arranque: la sesión heredaba ya ~999K de S11 sin haber pasado por `/clear`. **No hubo
un momento de degradación — nació saturada.** Lo que la mantuvo utilizable fue que el trabajo
era de archivos pequeños y verificación por script, no de leer código masivo.

### Qué se hizo

**El hallazgo que define la jornada:** la batería daba **195/0 en la máquina de Brian y 22
fallos en un clon limpio**. Lo destapó **una auditoría externa, no el sistema** — nadie corría
la batería fuera de este árbol.

- **12 PRs abiertos y mergeados** (#1-#12) siguiendo el flujo rama → verificar → PR → ⛔ no
  mergear, tras la pregunta de Brian *"¿por qué el sistema de PRs no está integrado?"*. Se cerró
  el agujero con un candado en `pre-commit.sh` que bloquea commits directos a `master`.
- **`bin/verify-all`** — 8 frentes en una corrida, incluido F8: **correr la batería DENTRO de un
  clon**, lo único que ningún check interno puede sustituir.
- **Familia D crece de 4 a 8 casos.** Los 4 nuevos no nombran ningún archivo ausente, por eso
  sobrevivieron a la primera pasada. 🔴 El peor: `grade-block archived` fallaba porque bajo
  `pipefail` el pipe tomaba el exit `2` del veredicto 🔴 MVP **aunque el `grep` acertara** —
  decía medir *"¿sigue siendo calificable?"* y exigía **la nota que saca en la máquina de su
  autor**. ⭐ Un check puede atarse a la instancia **sin mencionarla una sola vez**.
- **Clon limpio: 22 → 10 → 1 fallo.** El único que queda es la respuesta CORRECTA
  (`check-clear-ready registered=no`: la sesión de un árbol recién nacido no está registrada).
- **Credencial de secrets atada al caché** (nace en `SessionStart`/`PostCompact`, muere al
  recargar contexto, fail-closed), **licencia AGPL-3.0**, **QUICKSTART** con números medidos,
  `piezas.tsv` sale de `Maestro/` y por fin viaja.

### Errores propios — de método, los que importan

- 🔴 **Reporté 195/0 desde el disco de Brian cuando un clon daba 22 fallos.** No lo cacé yo.
- 🔴 **El PR #4 perdió los `matcher` de los hooks** → `gate-handoff` bloqueó Bash/Read/Grep/Edit
  y **el sistema se cerró sobre sí mismo**; Brian tuvo que arreglarlo a mano en el IDE.
  Después, al darle solo el bloque `PreToolUse` para pegar, se perdieron 3 hooks más (7→4).
- 🔴 **Una prueba de `bin/init` sobrescribió el `mente.config.yml` vivo de Brian** con
  `{{OWNER}}` y no lo restauré. Lección escrita: *una prueba que escribe en un archivo vivo debe
  restaurarlo*.
- ⚠️ Varios sabotajes que **no discriminaban** (un `sys.exit(0)` que daba el mismo valor que el
  estado sano). *Un sabotaje que no cambia el comportamiento observable no prueba nada.*
- ⚠️ **La hipótesis de partida de la separación motor/instancia era falsa.** Se iban a mover 221
  archivos; medido, **ninguno estorbaba** — fallaban los checks que los interrogaban mal. Mover
  archivos habría escondido el defecto.

### Lo raro

**`check-links` en un clon es un indulto general** para las memorias del harness: probado con una
errata inventada, **no se cazó**. Se aceptó a conciencia y está escrito en el código, porque la
alternativa (20 citas correctas en rojo en cada clon) es cómo un validador se vuelve ruido.

### 🔴 La cola: 4 PRs más DESPUÉS del primer wrap

El wrap se corrió a las 21:26 y la sesión siguió **75 minutos y 118 turnos más**, porque Brian
pidió cerrar pendientes antes del corte. Lo que salió de esa cola:

- **PR #13** — el matcher de `hooks/pre-edit-standards.py` (mencionar ≠ reclamar) + 2 avisos que
  solo se podían callar **falseando el dato**: un `Type: fossil` al que se le exigía fecha de hoy,
  y `check-health` contando una **línea fantasma** (`count("\n") + 1`), con lo que un documento de
  250 líneas se reportaba como 251 y se recortaba algo que ya cumplía.
- **PR #14** — 3 registros que afirmaban cosas **ya falsas**: `graphify #4` pedía 2 decisiones
  tomadas hacía 2 días, y el §E de `demo` decía que §F-7 seguía abierto cuando su propia tabla §F
  lo daba por cerrado. ⭐ *Un pendiente ya hecho cuesta lo mismo que uno olvidado.*
- **PR #15** — bloque `separacion-motor-instancia` **5/5**, verificado en un clon de master
  mergeado: **6 fallos en frío → 1 tras `bin/init`**.

### 🔴 Y el defecto que se repitió DOS VECES el mismo día

**Un merge por squash desde una versión previa borró trabajo ya empujado.** Pasó dos veces:
① el PR #14 nació con conflictos porque el #13 se mergeó mientras había trabajo encima;
② al mergear el #14, el candado del anti-patrón #8 **desapareció de master** — el propio candado
que vigila ese defecto. Recuperado por cherry-pick.

⭐ `rules/rule-shipping-flow.md` lista *"un PR que depende de otro sin mergear"* como anti-patrón
**#8 desde el 05-ago**. Medido el 07-ago: **0 validadores, 0 checks, 1 sola mención**. Otra vez la
ley del sistema sobre sí mismo. Ahora `hooks/pre-commit.sh` avisa si la rama va por detrás —
**avisa, no bloquea**: ir detrás es normal mientras se trabaja, lo caro es enterarse en GitHub.

### ⏸️ Una decisión de NO hacer

graphify **#5 (benchmark) y #6 (memoria puntuada)** quedan diferidos. Razón medida, ya escrita en
el propio documento: miden un producto que **nadie externo ha instalado** — graphify tiene miles
de instalaciones verificadas y 1.8:1 de tests; Mente OS **cero y cero**. Lo que los desbloquea es
una **prueba de campo**, no más código.

### Por qué se cierra

Contexto clavado en **1,000,030** — récord del proyecto, por encima del umbral del incidente del
21-jul y **sin moverse en 75 minutos**: es el techo del harness, no una casualidad.
`check-health` reporta **6 API connection errors** (5 al primer wrap), la señal de saturación
creciendo. Frontera natural: **PRs #12·#13·#14 mergeados**, #15 abierto, batería 198/0, el bloque
5/5, nada a medias.

---

## S11 · `8b4bddcb` — LA JORNADA DEL CRITERIO Y LOS TESTS (2026-08-04 02:31 → 08-05 23:07, ~45h)

**Medido del `.jsonl`:** 11.8 MB 🟢 · 5,982 turnos · 65 mensajes de Brian ·
🔴 **contexto pico 999,757 tokens**. Batería **160 → 178**, `failed: 0` al cierre.
**Cero commits en `marca-personal` — todo en disco, por decisión explícita.**

### 🔴 LA SEÑAL QUE HAY QUE MIRAR PRIMERO

**999,757 tokens es el contexto más alto de la historia del proyecto.** Supera a S7 (998K) y a
S1, la sesión monstruo (985K). El disco está sano (11.8 MB 🟢) — el problema **nunca fue el
disco**: cada pausa larga con este contexto reescribe casi 1M de tokens a precio premium.

⭐ **Por qué no degradó como el 21-jul:** la sesión se compactó sola varias veces y el trabajo
sobrevivió **porque estaba en disco, no en la conversación**. Eso es exactamente lo que Mente OS
existe para hacer. Aun así, el umbral rojo se cruzó y se quedó ahí muchas horas.

### En qué acabó

Tres frentes, en este orden:

| Frente | Antes | Después | El puente |
|---|---|---|---|
| **Huecos de criterio** | 66 esperando a Brian | **0** | los 3 dueños + 7 disciplinas con criterio propio |
| **Rendimiento** | `check-links` 47.2s | **0.55s** (86x) | un `glob` recursivo recorría 43,986 archivos **por cada cita** |
| **Tests de la demo** | 🔴 **0 archivos** | 🟢 **4** | los 4 caminos críticos, 15 verdes · 8 saltados · 1 rojo a propósito |
| **Batería** | 160 checks | **178** | y cada check nuevo se vio fallar antes de creerle |

### ⭐ EL MÉTODO QUE FUNCIONÓ — y que Brian impuso

> *"la IA pregunta, Brian responde con casos reales, la IA estructura"* — **nunca al revés.**

Los 66 huecos no se llenaron con lo que yo creía correcto: se llenaron preguntando en ventana
emergente y estructurando **sus** respuestas. De ahí salieron reglas que yo no habría escrito:
*FK siempre, sin excepciones* · *los DATOS deciden detener-vs-degradar* · *ausencia de evidencia
no es evidencia* · *un control nunca miente* · ⛔ *una fuente de verdad no se parte por tamaño*.

### 🔬 LOS DEFECTOS QUE EL PROPIO SISTEMA ME CAZÓ

Ninguno lo encontré leyendo. **Todos salieron de romper algo a propósito y ver si el check se
ponía rojo.**

| Defecto | Cómo salió | Por qué importaba |
|---|---|---|
| `check-applied` daba ✅ por palabras **sueltas** | declaré `rule-session-close.md` en un bloque que jamás lo usó → **pasó** | **preexistente** (verificado contra HEAD): daba por aplicados estándares que nadie usó, en cualquier bloque |
| `check-applied` no seguía punteros | partí el BLOCK.md y 3 estándares pasaron a "nunca aplicados" | ⭐ **un puntero que una máquina no sigue no es un puntero** |
| `pre-edit-standards` enmudeció | decoré la celda de estado del §F con `active · 🔴 …` | un validador lee la **celda**, no la intención |
| `gate-critical` bloqueaba todo test con SQL | intentó escribir `entrar.test.ts` | la regla se escribió cuando no había tests; ahora exime **solo si el test nombra su propia base** |
| **mi propia sonda no discriminaba** | saboteé `containerName` y el test de colisión **no** se puso rojo | los 4 nombres ya empezaban por letras distintas — **un caso que no distingue el fallo es decoración** |

### 🔴 EL HALLAZGO QUE MÁS VALÍA

**`DEMO_DATABASE_URL` apunta a la Neon de PRODUCCIÓN** (4 instancias vivas, medido). Salió al
preparar los tests de integración. Sin medirlo, el primer test habría escrito en la base que
sirve `for3s.vercel.app`.

⭐ Y una corrección al plan que solo apareció midiendo: ④ POWER iba a probar `container.ts`,
**donde la autorización no vive** — está en el endpoint. Un test ahí habría dado verde sin
proteger nada: **cobertura que tranquiliza**.

### 🔴 EL ÚLTIMO HALLAZGO — una métrica que se creía a sí misma

Salió al documentar la sesión, no al construir. `check-clear-ready` decide su veredicto leyendo el
`battery.failed` de `docs/METRICS.md`… y la batería **contiene un check que lo ejecuta**. El lazo
se cierra:

```
METRICS failed=1 → check-clear-ready 🔴 → la batería lo cuenta
                 → generate-metrics reescribe failed=1 → …
```

**Medido tres corridas seguidas: `METRICS=2 → exit 1`, inmóvil, con todo lo demás en verde.** Un
fallo transitorio quedaba **congelado para siempre** y ningún arreglo del código real lo limpiaba.

⭐ Se descuenta en `bin/generate-metrics`, no en `check-clear-ready`: **allí no funcionaba**, porque
`METRICS.md` solo publica dos totales y no los nombres de los checks. Lo intenté primero en el sitio
equivocado y lo comprobé antes de darlo por bueno. Reprobado con una sonda: con 3 fallos reales
sigue saliendo exit 1.

### 🔴 Y UN SEGUNDO CICLO, de la misma familia

Al arreglar el primero apareció otro: el check *pre-commit passes on a healthy block* **fallaba por
efecto secundario de la propia batería.** La batería crea bloques sonda `zz-*` en el árbol real,
`generate-index` los recoge, y `pre-commit` rechaza un índice desfasado.

**Evidencia:** el md5 de `docs/INDEX.md` **cambia solo por correr la batería**. El síntoma
desconcertaba porque `./hooks/pre-commit.sh` a mano daba exit 0 — y el conteo **empeoraba solo**:
176/1 en una corrida, 175/2 en la siguiente.

⭐ **Los dos ciclos son la misma ley:** *un check no puede ser evidencia de sí mismo.* Arreglados,
la batería da **177/0 estable en corridas consecutivas** — antes oscilaba sin converger.

### La lección de método, repetida tres veces

`$?` después de una tubería mide el **último** comando, no el que importa. Me dio falsas alarmas
otra vez (`pre-commit`, la puerta de tests). Y `grep -rl` cuenta **archivos** mientras
`grade-block` cuenta **referencias** — gobierna el número del validador, porque es el que el
check compara.

### 🙋 Lo que quedó esperando a Brian

**3 bloqueos, todos con trabajo YA ESCRITO detrás** → `memory/PENDIENTES.md` §B1-B3:
la rama de Neon (8 tests saltados) · los dueños de jazz/mashe (el test rojo) · el push
(despliega a producción).

---

## S10 · `1b9338a4` — LA JORNADA DE LA VOZ (2026-08-03 18:51 → 08-04 01:32, ~7h)

**Medido del `.jsonl`:** 2.1 MB 🟢 · 237 turnos · **contexto pico 261K 🟡** · 207K tokens de
salida · 35.7M de lectura de caché. Batería en verde todo el día. **Cero commits — todo en disco.**

### Cómo empezó y en qué acabó

Brian abrió pidiendo retomar. El plan era ① cerrar `distribucion` y ② los huecos de criterio.
**Ninguno de los dos se tocó.** A los tres turnos preguntó otra cosa:

> *"se me hace muy escueta la respuesta, a veces mucho texto que no me ayuda porque no está
> dividido y no entiendo qué leer ni cómo leerlo… ni sé qué sigue ni cómo continuar y eso es
> frustrante."*

Eso desvió la sesión entera, y con razón: era un defecto real del sistema, no una preferencia.

### El hallazgo de raíz — la voz se saboteaba a sí misma

`~/.claude/output-styles/for3s.md` tenía **8 reglas, todas sobre qué NO hacer**. Cero sobre
estructura. Y dos de ellas **causaban** el problema que Brian reportaba:

| Regla | Decía | Efecto medido |
|---|---|---|
| **2.5** | *"nunca cierres repitiendo · termina en la última frase útil"* | me **ordenaba cortar el cierre** — justo lo que él necesitaba para saber qué sigue |
| **2.8** | *"omite lo que no importa"* | se leía como permiso para entregar hallazgos sin explicar |

⭐ **No faltaban reglas: sobraban dos mal escritas.** Añadir estructura sin corregirlas habría
dejado el contrato compitiendo contra el estilo, cumpliéndose a medias.

### §6 · BRIAN'S ADDITIONS — un hueco de criterio se llenó

`principles/owner-0-voice.md` §6 llevaba días marcado `⬜ PENDING · BRIAN`. Lo que él dictó durante la sesión
**era exactamente ese hueco**, así que se estructuró con sus citas y su autoría, siguiendo el
método que `qa-dimensions.md` §5 exige (*la IA pregunta, Brian responde, la IA estructura*):
la entrega no debe necesitar una segunda pregunta · radiografía, no bitácora · el largo no es el
enemigo · leer no debe cansar · registro ni condescendiente ni excluyente.

### Lo que se construyó, en capas

**① El contrato de entrega** (`§7`): 4 partes por apartado · jerarquía H1/H2/H3 · gráficos que
explican · techo de tamaño · lectura por niveles · bloque `📦 ENTREGA` con 🩺 salud, antes/después
/puente y la etiqueta escrita UNA vez.

**② Los 3 modos** (`§7.0`), la corrección que más faltaba: *"¿cómo cierro?"* eran dos líneas y
recibió índice, salud y seis campos. **El contrato no tenía noción de peso.** 🟢 BÁSICO (el
default de Claude Code) · 🟡 MEDIO · 🔵 BLOQUE, con el default en 🟢 — *sobre-formatear cuesta
atención en cada turno; sub-formatear cuesta una pregunta de seguimiento.*

**③ El respaldo externo** (`§8`): 5 reglas coinciden con doctrina publicada de Anthropic
(evidencia sobre afirmación · incertidumbre calibrada de la Constitución de enero 2026 · explicar
la lógica · todos para mostrar progreso). Y declara qué **NO** lo tiene: la estructura de
secciones, el bloque, el techo y los niveles son invención de este proyecto. **Anthropic no
publica plantilla de respuesta.**

### Consumo — el vehículo era la fuga, no lo que parecía

Brian avisó del gasto. Medido: el Artifact costaba ~6,678 tokens (44% CSS repetible), pero
**el vehículo se paga en CADA turno** y había crecido de ~1,100 a **5,167**. Adelgazado a **2,644
(−48%)** dejando solo la regla operativa; el porqué vive en la fuente canónica. Verificadas
16/16 reglas presentes tras comprimir.

### Errores propios

- **Repetí `✅ HECHO —` cuatro veces seguidas** en un mismo bloque. Brian: *"los hechos no
  deberías de repetir la palabra."* La etiqueta repetida deja de marcar frontera y se vuelve ruido.
- **No existía un H1.** Todo abría en `##` y vivía en un nivel plano: nada marcaba dónde empieza
  ni acaba una parte.
- **Apliqué formato de auditoría a una pregunta de dos líneas** — el fallo que originó los 3 modos.
- **Propuse Artifacts por iniciativa propia.** Brian: *"es todo sobre Claude Code, al menos que te
  diga lo contrario."* Retirados de ambos archivos y escrito como **prohibición explícita**, no
  como omisión: una regla ausente se rellena con lo que la IA crea razonable.
- 🔴 **Cité `intern-os` dentro de un archivo del MOTOR.** El motor se publica bajo MIT; una cita
  ahí arrastra linaje ajeno a cada clon. Purgado a 0 en ambos. ⭐ *Antes de citar una fuente
  externa: ¿este archivo viaja a otros repos?*
- ⭐ **Dejé `principles/owner-0-voice.md` en 582 líneas con un límite de 250** — el mismo día que escribí la
  regla del techo de tamaño. *La regla que escribes no se aplica sola al archivo donde la
  escribes.* Registrado en `PENDIENTES.md`, no resuelto.

### Consumo — dónde creció

Arranque normal y crecimiento lineal: 6 rondas de refinamiento del contrato, cada una releyendo
ambos archivos y corriendo la batería (≈2 min). **261K con 237 turnos en 7h: la sesión más sana
de las últimas cuatro** — comparar con S9 (681K) y S7 (998K).

### Lo raro

Nada anómalo. Un `Edit` falló dos veces por un archivo sin salto de línea final — resuelto con
`python3`, no es defecto del sistema.

### Por qué se cierra

Límite natural y **una razón de método**: el contrato pasó de 8 a ~24 reglas en una sola sesión y
**nunca ha gobernado una respuesta real** — todas las de hoy las maqueté a mano. Solo entra en
vigor en una sesión nueva. Brian, tras 6 rondas: *"me gusta más que como iniciamos pero no me
fascina"* — y la séptima ronda de diseño rinde menos que un día de uso real.

---

## S9 · `dc733bc1` — LA JORNADA DEL AGENTE INSTALADOR (2026-08-02 22:43 → 08-03 18:39, ~20h)

**Medido del `.jsonl`:** 7.7 MB 🟢 · 1,637 turnos · **contexto pico 681K 🔴** · 679K tokens de
salida · 586M de lectura de caché. Batería **138 → 160**. 37 commits locales, sin push.

### Qué se hizo, en tres bloques

**① El plan de raíz (F1-F4).** Empezó arreglando UN check roto y acabó encontrando que **8
hallazgos del día eran la misma familia**: un check que corre, reporta verde, y no mide lo que
dice medir. No checks ausentes — presentes, activos y en los que se confiaba.

| | |
|---|---|
| F1 | el guardia del `/clear` comparaba 8 hex como SUBCADENA — un hash de commit lo desarmaba |
| F2 | esa familia tenía **4 instancias**, no 1 (`check-blocks` · `check-clear-ready` · `check-health` · `generate-metrics`) |
| F3 | `rules/rule-checks-must-measure.md` — las 3 familias con sus casos medidos |
| F4 | sección `SELF-TEST` en la batería: rompe los guardias A PROPÓSITO y exige que canten |

**② Citas rotas 144 → 0.** El reparto es la conclusión: de 135 resueltas, **69 eran citas
CORRECTAS** que `check-links` contaba mal (nombres que un documento DISCUTE, roadmaps, memorias
del harness, repos hermanos) y 66 fósiles reales de la migración v1→v2. Cuando la cita es
correcta, cambiar la prosa es el error.

**③ Bloque `distribucion` — abierto y 6/6 construido.** Nace de Brian: *"esto está local para mí
y aun así tenemos errores. AÚN NO VEO QUE SEA ALGO QUE PODAMOS CONFIAR A QUE LA GENTE PUEDA
OCUPAR."* Y su reencuadre decisivo: **quien instala no es una persona, es un AGENTE.**
`bin/init` + plantillas + `CAPABILITIES.md` + la frontera motor/instancia como candado portable.
**Probado en un clon real**: otro dueño, 6 menciones suyas, CERO de Brian, y un hook del clon
corriendo contra su propia ruta.

### Seguridad — dos agujeros probados, no deducidos

- 🔴 `python3 -c "open('~/.ssh/...')"` **leyó** lo que el `deny` prohibía. `Bash(python3*)`,
  `perl`, `xargs`, `node`, `bun` estaban en `allow` y ejecutan código arbitrario.
- 🔴 `~/.claude.json` — `oauthAccount` del propio harness — **sin ninguna regla**. Su temporal
  `.tmp.<pid>` llevaba lo mismo desde el 30-jul. `deny` 67 → 212, `ask` creado (48 reglas).

### Errores propios, y son la parte que más enseña

- **Declaré un bloqueo que no existía.** Dije que el sub-bloque 1 necesitaba un clon limpio
  porque mi sonda resolvió a vacío. **No consulté la fuente.** La documentación lo respondía.
  ⭐ *Un límite que no has verificado no es un límite: es una suposición disfrazada.*
- **Escribí una prueba que no probaba nada.** La primera sonda del huérfano se llamó `zz-*`,
  nombre EXENTO por ser sonda de la batería: pasaba por construcción. Un check que no puede fallar.
- **Copié un defecto al arreglar su gemelo.** La simetría de ADRs comparaba `"016"` (y `2016` lo
  satisface). El defecto estaba en el check ORIGINAL y lo repliqué sin cuestionarlo — justo lo que
  `rule-fix-not-patch` §3 manda preguntar: *¿dónde MÁS vive?*
- **Mi comando de prueba quedó archivado como permiso permanente.** Al aprobarse, el harness
  escribió `Bash(python3 -c "print(open('/home/brianweb3/.ssh/known_hosts')…` en
  `settings.local.json`. §1.1 en vivo. Y reapareció **tres veces** al purgarlo.

### Consumo — dónde creció

Arranque normal. El contexto escaló a partir de la auditoría de los 29 ADRs uno por uno y no bajó:
a partir de ahí cada corrida de batería (≈2 min) y cada verificación cruzada sumaban. **681K de
pico con 1,637 turnos: murió de EDAD y de densidad, no de tamaño** — 7.7 MB es 🟢.

### Lo raro

Tres corridas de la batería dieron un fallo transitorio por **solaparse con `generate-metrics`**,
que la ejecuta internamente y toma el mismo lock. No es defecto: es el lock haciendo su trabajo,
pero conviene saberlo antes de creerse un rojo.

### Por qué se cierra

Límite natural: bloque 6/6 construido, plan de raíz completo, `check-health` sin 🔴 y batería en
verde. Lo que queda del bloque **no lo decide la IA** — prueba de campo real y la capa 2 del
veredicto (`qa-dimensions`, 9 huecos de criterio).

---

---

## 🔁 R1-R3 · LAS 3 SESIONES HUÉRFANAS (registradas retroactivamente el 2026-07-31, sesión S8)

> **Por qué existen estas 3 entradas.** `bin/check-health` las marcaba como *"past session over
> 2 MB with no entry"*. Se registran con lo medible del `.jsonl` (peso, turnos, contexto, tokens,
> fechas). ⚠️ **Lo que NO se puede reconstruir retroactivamente es el criterio**: qué se sintió
> raro, por qué se cerró. **Eso se perdió** — y ese es justamente el costo que la regla previene.

### 🔴 R1 · `4c187f33` — LA SESIÓN DEL INCIDENTE DEL 21-JUL (2026-07-20 00:32 → 07-23 23:42, ~96h)

**La más grande jamás registrada por peso: 23.4 MB** · 1,256 turnos · **contexto máx 999,366** 🔴 ·
cache_read **1,033 millones** (la única del proyecto que cruza el billón) · cache_write 16.9M ·
output 1.77M.

**Es la sesión del peor incidente del proyecto.** De aquí salió *"no eres el mismo de siempre, no
me sirves así"*: 6 violaciones de scope, degradación sostenida por contexto saturado. Se recuperó
del `.jsonl` crudo el 27-jul, **seis días después**, y hasta hoy vivía solo en la memoria
`project_incidente_degradacion_21jul` — **nunca en el Registro.**

**Lección medida:** la regla `rule-session-close.md` fue escrita *a causa* de esta sesión, la citó
por nombre como "el peor infractor"… y **la sesión siguió sin registrarse 10 días.** Escribir la
regla no la ejecuta. Es la ley del proyecto demostrada sobre sí misma.

### 🔴 R2 · `fa2c625f` — LA JORNADA SEGURIDAD / SEC-4c (2026-07-15 21:01 → 07-19 00:38, ~76h)

10.1 MB 🟢 en disco · 1,180 turnos · **contexto máx 999,692** 🔴 (el pico absoluto del proyecto) ·
cache_read 945M · cache_write 22.4M · output 1.71M.

Por fechas cubre el CI 100% verde (`b8da4d7`), los 4 urgentes de confianza SEC-3/4/5/6, **SEC-4c
non-root con perfil por instancia** (`021292e`) — incluido el `chown -R` que rompió el HOST — y la
rotación del token de GitHub. Empalma con el arranque de S4 (super-cerebro).

⚠️ **Sana en peso, roja en contexto y edad.** Mismo patrón que R1: 76h abiertas, 999K de pico.

### 🔴 R3 · `b075269c` — LA JORNADA H5-H10 (2026-06-16 05:43 → 06-27 23:58, ~11 días)

12.9 MB 🟢 · 661 turnos · contexto máx 679K 🔴 · cache_read 437M · cache_write 17.2M · output 665K.

**La sesión más larga en días de las tres** (11). Por fechas cubre H5 memoria real, H6 se cuida,
H8 equipo, H9 sueña (DMN), H10 planea, el rediseño de la capa de memoria y el arranque de
profesionalización PR1-PR10.

**El patrón que las une:** las tres murieron de **edad**, no de peso. 96h · 76h · 11 días.
Ninguna cruzó los 50 MB; las tres cruzaron el rojo de contexto. **El umbral que importa no es el
tamaño del archivo — es cuánto lleva abierta.**
