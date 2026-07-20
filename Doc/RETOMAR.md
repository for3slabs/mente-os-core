# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

> **Propósito:** el ÚNICO archivo que necesitas leer al retomar. Pequeño A PROPÓSITO
> (ahorro de tokens — Brian lo notó de nuevo 2026-07-07: cuando crece, releerlo es caro).
> **REGLA DE HIGIENE:** este archivo NO debe pasar de ~200 líneas. Al cerrar sesión, si
> creció, mover lo viejo a `Estado_Sesion_Continuidad.md` (o al último snapshot) y dejar
> aquí SOLO el estado vigente + punteros. La historia va a la Bitácora, no aquí.

**Última actualización:** 2026-07-18 (Mente OS Maestro F1-F5 ✅ + fotos E6 backlog VACÍO ✅).

---

## 1 · Quién + qué (10 segundos)

- **Brian López** (founder, NO "Aguilar"). Email ema@frutero.club / brayan002150@gmail.com.
- **Proyecto = SOLO For3s OS.** Cerebro documental: `/home/brianweb3/for3s/Mente/` = **"Mente OS"**.
  ⛔ NO tocar `marca-personal/Mente/` (otro proyecto) sin permiso.
  ⛔ **NO leer `~/5M-incubathon/` (Mente OS de NavigoX) sin gate** — ver §7 (protege consumo).
- **Fuente de verdad arquitectónica:** `Mente/Cerebro/For3s_OS_Grafo_Maestro.md`.
- For3s OS = **agente "segundo cerebro" autónomo, self-hosted** en el servidor `for3s`
  (Telegram + consola, Python 3.12 + Postgres+AGE+pgvector, contenerizado). EN PRODUCCIÓN.

## 2 · Servidor `for3s` — 5 FOR3S OS al mismo tiempo (2026-07-07)

Tailscale `for3s` 100.112.177.53 · SSH brianweb3 (pass en memoria `reference_servidor_for3s`) ·
gestor de instancias: comando `for3s listar|agregar|entrar|encender|apagar|borrar`.
Aislamiento TOTAL por `docker compose -p for3s-<nombre>` (red/BD/KEK/volúmenes propios).
Comparten SOLO: máquina + imagen v0.15.0 + suscripción Claude (**1 solo cupo** para todos).

| Bot | Instancia | Dueño | Estado | Notas |
|---|---|---|---|---|
| 🏢 @For3s_OS_bot | `for3s` (compose principal, no `for3s listar`) | Brian | 🟢 | "Foresito" — EMPRESA, memoria de siempre, microglía ON |
| 👤 @For3s_Brian_bot | `brian` | Brian | 🟢 | PERSONAL — **ENTRENADO** (ver §4), microglía OFF a drede |
| 🌐 @For3s_General_bot | `general` | Brian | 🟢 | PÚBLICO, **equipo/puerta ABIERTA** (quien escriba entra). Pendiente: otras API keys/datos |
| 🎷 @For3s_Jazzita_bot | `jazz` | Jazz @driade_1 (1177279840) | ⚪ apagado | verificado E2E; ella lo enciende cuando quiera |
| 👊 @For3s_Mashe_bot | `mashe` | (1er /start) | ⚪ apagado | verificado E2E; Brian decidirá qué hacer |

⚠️ Las 3 nuevas heredan la auth OAuth de Foresito (misma cuenta). Instalación fresca sana
(el bug FK-personas ya está fijado en la imagen; el warning "Chat not found" del menú es
normal hasta que el dueño da /start). Detalle: memoria `project_multi_instancia`.

## 3 · Estado global del producto

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.18.0 CONFIANZA. schema BD v45.** 13 hitos
H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad Hermes
(5/5) + intern-os + CI + Frente B + Molde For3s Inside + For3s Trace + **Frente E CONFIANZA
(expediente + carril /mision + auditoría de seguridad).** **Cero bugs abiertos.**
**✅ TRÍADA SINCRONIZADA (2026-07-17): server = GitHub (origin for3slabs/for3s-os + backup
for3slabs/for3s) = local (`For3s-OS/`) en HEAD `8798190`. CI verde. 252 tests.**
**✅ LAS 5 INSTANCIAS EN v0.18.0** (Foresito/brian/general encendidas + jazz/mashe apagadas,
migraciones 39-45 aplicadas en cada BD). Cliente API real: NavigoX (hotel-recepcion, no consume
activo) + jazz-id (prueba). Datos limpios.
**✅ SEGURIDAD/HIGIENE CERRADA DEL TODO (2026-07-16):** CI 100% VERDE (`b8da4d7`; llevaba rojo desde
v0.17.0) — gitleaks (repo SIN secretos reales) · format · bandit · migraciones E2E con AGE · **CI-2
coverage umbral 15%** · **mcp CVE-2026-59950 parcheada** (1.28.1). Los 4 URGENTES de confianza
(SEC-3/4/5/6) + SEC-3b/4b completos. **Token GitHub rotado** ✅.
**✅ SEC-4c COMPLETO (2026-07-16 noche, tríada `021292e`):** contenedor non-root con **PERFIL por
instancia** — Foresito/brian=interna(root), general/jazz/mashe=expuesta(non-root uid 1000). gosu +
KEK/modelo por ENV. `/soy` muestra el perfil. 5 bugs cazados en jazz (1 catastrófico: chown -R
rompió el HOST → lección LOCKED: nunca chown bind mounts; uid del contenedor = uid del host).
Ronda: `Cuerpo/Ronda_SEC4c_NonRoot_Perfil_Instancia.md`.
✅ Token de GitHub ROTADO por Brian (2026-07-16) — el que se expuso ese día quedó revocado.

## 4 · 🎓 HITO ENTRENAMIENTO — casi cerrado (lo más reciente)

**6 agentes OpenClaw → @For3s_Brian_bot.** Material `~/entrenamiento/` (read-only, respaldo).
Ejecutado E0→E6 (commits firmados). **Estado: 11,664/11,664 archivos analizados 1×1.**
- E0-E5: censo + secretos→vault (38) + identidad Fruterito a persona/ + 5 olas cronológicas
  (~21.6K episodios tras curar Watchdog) + 15 skills + manifiesto 0 pendientes.
- E5b digestión: **grafo al 56% (18,984/33,737 eps · 19,827 conceptos), sube cada noche sola** (CLS 08:00 UTC).
- E6 backlog profundo (archivo por archivo): F1 docx/pdf ✅ · F2 triage ✅ · F3 código→catálogo ✅ ·
  **F4 fotos: ✅✅ BACKLOG VACÍO (1169 con visión, 0 pendientes)** · F5 audio ✅ (3/4 whisper local) · F6 cierre ⏳.
- **7 bugs de producto cazados** (migr 033/034 grafo AGE, FK personas, incluir_import, escaping
  Cypher, KEK efímera, plantilla instancia). Reporte: `Doc/Entrenamiento_Ejecucion_Reporte.md`.

**⏳ F6 CIERRE — plan LOCKED (Brian 2026-07-18, decisiones tomadas):** verificado en vivo el estado
real en la BD de `brian`: **manifiesto 11,664/11,664 · backlog sin `detalle.e6` = 0 (nada omitido ✅)
· episodios import 33,737 (embedding 99.99%) · grafo digerido 56% · lotes e6-docs 46/e6-otros 930/
e6-fotos 1169/e6-av 3.** Todas las fases del backlog E6 (F1-F5) ejecutadas. **QUEDA para cerrar:**
1. ⏳ **ESPERAR 2-3 NOCHES** (decisión Brian) a que el CLS suba el grafo a ~70-80% antes del examen.
2. 🎓 **Examen ~40 preguntas EN VIVO** al bot real (episodios/línea de tiempo · docx Genomad · una
   foto-pizarra con visión · catálogo de código · skills · identidad Fruterito). Umbral cierre ≥90%
   con conciencia temporal. Espaciado + vigilar cupo 5h, sin loops de fondo.
3. 🔋 **Batería §5-BIS** completa en `brian` (/salud 0 FAIL · chat normal intacto · memoria/reconexión).
4. 📌 **v0.19.0 "ENTRENADO"** (decisión Brian) + changelog + Bitácora + RETOMAR + memoria + commit
   firmado (server-primero, SIN push). (3) ✅ microglía ON en brian HECHA 2026-07-16. Memoria:
   `project_hito_entrenamiento`.

## 5 · 👉 PRÓXIMO PASO INMEDIATO (arrancar aquí tras /clear)

🚀 **v0.17.0 MERCADO — 3 frentes cerrados el 2026-07-15 (la jornada más grande post-Incubathon).**
Todo probado, tríada sincronizada en `ccc3fb0`, /salud 0 FAIL, datos limpios.

1. **🌉 FRENTE B COMPLETO (F1-F6)** — canal API → PRODUCTO. Panel en producción
   `for3s.vercel.app/for3s-admin` (login 2 tokens: FOR3S_ADMIN_TOKEN en `~/.for3s/general/.env` ·
   FOR3S_CTL_TOKEN en `~/.for3s/ctl.env`). Pestañas Resumen (uso por temporalidad hora/día/semana) ·
   Clientes · Waitlist · Instancias · Servidor tipo Railway · **Alertas**. Carga probada a 2000 conc.
   Ronda: `Cuerpo/Ronda_FrenteB_Puente_Mercado.md`. ⚠️ infra host: `/etc/sudoers.d/for3s-ctl`.
2. **🧩 MOLDE "For3s Inside" (M1-M4)** — capa reutilizable en `molde/for3s-inside/`: contrato OpenAPI
   + SDK TS/Py + onboarding + receta trazabilidad. Ronda: `Cuerpo/Ronda_Molde_For3s_Inside.md`.
   Memoria: `project_molde_for3s_inside`.
3. **🔎 FOR3S TRACE COMPLETO** — el cliente traza → For3s recibe/analiza/detecta anomalías con el
   PUNTO EXACTO (componente/paso/afectados/dónde) → alertas en el panel por instancia. En
   `molde/for3s-trace/`. Ronda: `Cuerpo/Ronda_For3s_Trace.md`. Memoria: `project_for3s_trace`.

**~10 bugs cazados** (1 SEC grave: inyección LIKE en `/v1/olvidar`). GIL aclarado
(`Doc/Analisis_Free_Threading_GIL.md`: no migrar a free-threading). Cliente API real: NavigoX + jazz-id.

**👉 PRÓXIMO PASO — 🟣 FRENTE E "CONFIANZA PARA DELEGAR" EN CONSTRUCCIÓN (elegido por Brian 2026-07-15):**
- **Ronda aprobada** (`Cuerpo/Ronda_FrenteE_Confianza_Para_Delegar.md`): escalera de confianza
  4 peldaños (trabaja solo Y SE VE → programación → testers → cliente real), fases F1-F6.
  Diagnóstico: la desconfianza es RACIONAL — hay verificación técnica de sobra pero CERO
  kilometraje en misiones reales presenciadas ("se probó que funciona, no con clientes").
- **F1 ✅ EXPEDIENTE (commit `73583a0`):** migración 045 (misiones) + expediente.py punto único +
  /expediente (probado EN VIVO por Brian ✓) + GET /adm/expediente + pestaña panel (pusheada a
  Vercel `85f1c76`, deploy automático). Batería §5-BIS pasada.
- **F2 ✅ CARRIL DE MISIONES (commit `7842c8e`, server SIN push):** `/mision <pedido>` (dueño) →
  For3s trabaja con tools reales → TODO el flujo (PLAN→EJECUCIÓN→VERIFICACIÓN→ENTREGA→ERRORES) →
  expediente → veredicto ✅/❌ de Brian (misok/misno; solo entregada→verificada|fallida).
  tool_loop tolera mcp=None (misiones con sandbox sin GitHub — general). Fuente `ejecuciones` en
  la hoja (cierra hallazgo execute invisible). **E2E con LLM real:** misión primos → 2
  execute_code → auto-verificación con 2 algoritmos (24133=24133) → 5/5 secciones → verificada.
- **F3 ✅ AUDITORÍA DE SEGURIDAD (commit `d3e71ef`, server SIN push):** Brian pidió *"¿hay error
  crítico que exponga a demanda si un cliente compra?"* → **Veredicto: NO.** Riesgo #1 (fuga entre
  clientes) DEMOSTRADO cerrado (pentest 4 ataques, 0 fugas) + audit inmutable (DELETE rechazado) +
  AES-256-GCM+HKDF + audit sin PII. **🔴→✅ hallazgo:** sandbox alcanzaba la BD/internet → red
  segmentada (`sandbox_net`, verificado gaierror). Doc: `Doc/Auditoria_Seguridad_For3s_OS.md`.
- **F4 ✅ PILOTO TESTER jazz (commit `c51a267`, server SIN push):** jazz encendida con
  v0.17.0+F1-F3. **2 bugs cazados (caza-bugs de tester real):** BUG-E1 (/mision y /expediente NO
  en menú admin = invisibles) + BUG-E2 (bug propio F2: @con_typing mal puesto → doble typing en
  mision, ausente en expediente). Doc: `Doc/Piloto_Tester_Jazz_F4.md`. ⏳ Falta (Jazz): /start +
  usar el bot + feedback.
- **A ✅ LENTITUD /mision ATACADA (commits `5de8ec4` + `edf59fd`, server SIN push):**
  - **Progreso EN VIVO** (`5de8ec4`): hook `on_vuelta` → mensaje editable con fase+tiempo ("🧠
    pensando paso N" / "⚡ ejecutando código"). El 99% del tiempo es el LLM (medido) → no hay
    ineficiencia, solo la percepción de colgado. Verificado (3 fases).
  - **Benchmark de modelos + Opus en el carril** (`edf59fd`, pedido de Brian): probé los 3.
    Haiku=202s (el más LENTO, más vueltas) · Sonnet=49s pero FALLABA (destapó BUG-E3) · Opus=101s
    5/5 secciones. **Brian eligió Opus SOLO para /mision** (proxy `_AgenteBYOK`, no contamina el
    canal — verificado: misión en opus, chat en sonnet). **🐛 BUG-E3 cazado+arreglado** (afectaba
    TODAS las misiones): `stop=max_tokens` devolvía respuesta VACÍA silenciosa → ahora AVISA
    ("respuesta cortada, pide el resto"). + max_tokens del carril 4096→8192.
  - ⭐ **F-A2 anotado** (idea de Brian, mejora mayor): partir misiones al equipo multi-agente
    (paraleliza) para bajar el tiempo de PARED real, no solo la percepción.
- **F5 ✅ PILOTO CLIENTE por SIMULACIÓN + F6 ✅ CIERRE (v0.18.0 CONFIANZA, commit `19b6552`):**
  F5 = recorrido de cliente por la URL pública (aislamiento entre clientes SÓLIDO por la puerta
  real, errores limpios, memoria, cuota frena). F6 = **prueba E2E de TODO el flujo** (16/16 + 11/11
  bordes incl. inyección SQL) + batería §5-BIS completa (244 tests, /salud 0 FAIL, chat normal
  intacto) + rebuild v0.18.0. Docs: `Doc/Piloto_Cliente_Real_F5.md`.

**🟣 FRENTE E → 🔄 CARRIL VIVO DORMIDO (vuelta 1 ✅).** Brian 2026-07-16: *"me gustó la dinámica,
no lo cierro como terminado — es repetitivo, lo iremos mejorando"* → evolucionado a un **carril de
mejora continua** repetible: `Doc/Carril_Mejora_Continua_Confianza.md` (los 5 pasos del ciclo +
cómo reactivarlo + bitácora de vueltas). Se despierta cuando Brian lo sienta. Vuelta 1 = escalera
F1-F6+A, 3 bugs cazados (E1 menú invisible · E2 doble typing · E3 respuesta vacía). Brian la va a
probar en uso real.
- **🎨 UX/mejoras abiertas (no bloquean):** /salud 🔴 en instancia virgen · rate por-minuto casi
  inalcanzable con LLM real (la defensa es la cuota diaria) · `/olvidar tema="%"` borra todo lo suyo.
- **⏳ PENDIENTE de gente externa:** Jazz usa su bot + NavigoX retoma consumo = pilotos VIVOS.
- **⏳ PRÓXIMO — Brian decide:** (a) propagar F1-A a brian/mashe/Foresito (hoy en general+jazz) ·
  (b) **F-A2** sub-agentes paralelos (bajar tiempo de PARED real) · (c) nuevo frente (🟡 C multi-canal).
- Frente C multi-canal: pendiente SIN urgencia (Brian: "integraciones pesadas, hay que sentarnos").
- También sigue en la mesa: **propagar v0.17.0** a brian/jazz/mashe/Foresito (solo corre en general).
⚠️ NavigoX vive en `~/5M-incubathon/`, CERRADO — no leerlo sin gate.

## 5-bis · Pendientes grandes (Brian marca el foco)

- 🌐 **⭐ SUPER-CEREBRO CONECTADO (Brian 2026-07-17).** Visión: `Alma/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`.
  - 🅱️ **MENTE OS MAESTRO → ✅✅ COMPLETO F1→F5 (2026-07-17).** El controlador ligero que APUNTA
    (no replica) ya vive: repo `for3slabs/mente-os-maestro` (privado) con `registro.md` + comandos
    `maestro` (puente A git efímero + B canal API vivo) + `mente-os-nueva` (crea ramas) + `permisos.md`
    (puerta por carril, fail-closed) + `BIENVENIDA.md` (onboarding al clonar). Ramas versionadas:
    `mente-os-for3s` (rama madre, 166 docs) + `mente-os-diseno-jazz` (piloto real). Detalle:
    `Cuerpo/Ronda_Mente_OS_Maestro.md` + memoria `project_mente_os_maestro_f1_f2`. **Evoluciona a CARRIL.**
  - 🅰️ **entrenar a Foresito (@For3s_OS_bot) con TODO → 🟢 EN CONSTRUCCIÓN (T0-T4 ✅ 2026-07-18).**
    Ronda aprobada por Brian: `Cuerpo/Ronda_Entrenamiento_Foresito.md` (plan + decisiones + bitácora).
    6 fuentes (Mente · for3s-inter · marca-personal CON permiso explícito · For3s-OS · ramas-mente-os ·
    raíz CLAUDE.md/.codeviz) = 741 archivos, TODOS analizados 1×1: **manifiesto 741/741 con decisión
    (0 omitidos)** → **1,829 episodios** (docs + código CRUDO con marca de versión — decisión Brian).
    **Wiki-hackathons (3,076 archivos EXTERNOS Monad Blitz, ~6.1M tokens) EXCLUIDO por Brian** (importable después).
    Red de seguridad: backup RESTORE-verificado `~/backups-foresito/` + reversa demostrada + snapshot
    :ro `~/entrenamiento-foresito/`. Módulo `entrenamiento_repo.py` commiteado (`385ac46`, server SIN
    push). **T5 ✅: embeddings 1,829/1,829 + digestión acelerada 95% (117 conceptos, grafo
    834→2,687 nodos, cupo +0.06)** vía `pasada_cls_repo.py`. **T6 ✅✅ EXAMEN APROBADO
    98.8% (41.5/42, 2026-07-19):** 42 preguntas exhaustivas por el tubo REAL — Maestro
    EN VIVO 4/4, bordes/trampas 5/5, canon con letra exacta. **Cosecha: 11 hallazgos
    (H-1…H-11) TODOS con fix + validación SISTÉMICA** (la joya: H-11, la contraseña del
    server vivía en 60 episodios de Foresito+brian → redactada + blindada de raíz).
    Commits server SIN push: `385ac46`+`c1f6d56`+`fafac3c`. Batería final: 260 tests ·
    /salud 0 FAIL Foresito y brian. Registro: `Doc/Examen_Foresito_T6_Hallazgos.md`.
    **✅ v0.19.0 "ENTRENADO" CERRADA Y DESPLEGADA (2026-07-19):** bump + changelog (CHANGELOG.md
    además backfilleado con 0.17/0.18 que faltaban) + **TRÍADA en `f50a5db`** (server = GitHub
    origin+backup = local) + **las 3 instancias vivas propagadas** (Foresito/brian/general,
    agent+worker en v0.19.0; jazz/mashe heredan al encender). **CI ✅ + Trivy ✅** (aviso nuevo
    torch PYSEC-2025-194 con ignore justificado; TODO validar torch 2.13). ⚠️ **CodeQL rojo
    DESDE EL 17** (pre-existente, pendiente aparte).
  - 🎓 **HITO ENTRENAMIENTO (brian) ✅✅ CERRADO (2026-07-19/20):** noches ADELANTADAS
    (encadenador 10 tandas, freno 0.99 por orden de Brian: 11,763→14 pendientes, 99.94%,
    grafo 814→1,335 conceptos, fallback cronológico + setsid) + **EXAMEN APROBADO 33/35 =
    94.3%** (trampas 6/6 — H-11 validado E2E: el bot VE "[SECRETO→vault]", no la contraseña;
    honestidad de corpus: Incubathon/H13 "no lo sé" CORRECTO). 🐛 B1 cazado+fixed: preguntas-META
    del corpus → conceptos canónicos "notas de voz"/"fotos" (re-examen ✓). **LOS DOS AGENTES
    ENTRENADOS, EXAMINADOS Y APROBADOS — super-cerebro COMPLETO.** Detalle:
    `Doc/Examen_Foresito_T6_Hallazgos.md` (registro maestro de los 12 hallazgos).
  - 👑 **FORESITO = EL AGENTE MAESTRO (decisión Brian 2026-07-18) + PUENTE E DINÁMICO ✅ VIVO:**
    mente maestra y agente maestro unidos. `GITHUB_PAT` en su .env → lee `for3slabs/mente-os-maestro`
    (registro/permisos/reglas) EN VIVO por su GitHub MCP (E2E ✅, incluso leyó su propio nombramiento
    recién pusheado `cfc0431`). Skill `agente-maestro` (id 22) = rol + reglas de oro (apuntar-no-replicar ·
    GATE NavigoX · fail-closed · solo lectura). 🐛 Bug producto cazado+fixed: /salud listaba 741
    sesiones import (~750 líneas) → corpus aparte + LIMIT 25. Detalle: Ronda_Entrenamiento_Foresito §6.

- 🎯 **APRENDIZAJES DE CAMPO (post-Incubathon, 2º lugar) — mapa de trabajo grande:** 5 frentes.
  **Doc madre:** `Alma/Aprendizajes_De_Campo_Post_Incubathon.md`. Detalle en `Doc/PENDIENTES.md`
  §POST-INCUBATHON. Estado (2026-07-13):
  - 🔴 **A consumo tokens → ✅ ANALIZADO (causa raíz):** la sesión de Claude Code creció a 278MB/72M
    tokens + modelo Fable5[1m] (el más caro) + caché frío al cerrar app = 3 msjs agotaron el cupo.
    **Solución LOCKED:** /clear al cerrar cada bloque, MODERADO POR MÍ automáticamente (Brian no carga
    la presión) + vigilar tamaño de sesión. Memoria: `feedback_moderar_consumo_sesion`.
  - 🔵 **D valor de retorno → 🟢 EN CONSTRUCCIÓN: hito H13 "DEVUELVE"** (Ronda aprobada 2026-07-13,
    `Cuerpo/Ronda_H13_Devuelve_Valor_Retorno.md`). Decisiones LOCKED: digest+contextual · estreno solo
    `brian` · extender DMN · máx 1-2 proactivos/día. **F1 ✅ (commit `17dbd01`, server):** motor de
    insights (clase VALOR del DMN + tabla insights + /dmn valor on|off) probado E2E en `brian` — 3
    insights reales de la memoria entrenada, 0 alucinados. **F2 ✅ (commit `15fc29d`): digest diario
    proactivo ENTREGADO de verdad por Telegram** (cron 08:00 Mx, /proactivo on|off, gates fail-closed,
    blindaje multi-usuario, audit). **3 bugs latentes cazados en el hito:** else ciego en set_clase/
    correr_ciclo + alertas PR2 del worker MUDAS en instancias de plantilla (sin fallback ENV + compose
    sin pasar TELEGRAM_BOT_TOKEN al worker — arreglado en ambos composes, repara también jazz/mashe/
    general). **F3 ✅ contextual VERIFICADA EN VIVO** (sim=0.70, tejió insight+memoria). **F4 ✅
    feedback** (Brian marcó "útil" en vivo). **F5 ✅ v0.16.0.** 4 bugs latentes cazados (else
    ciego DMN ×2 · alertas worker mudas · changelog sin 0.15.0). **TODO CERRADO 2026-07-14:**
    propagado a las 4 INSTANCIAS ✓ · fix equipo SELLADO con corrida real (5/5 conocen For3s) y
    commiteado ✓ · push GitHub + local sync (`06c5f99`) ✓. **Quedan (menores):** carril "urgente"
    diferido · sugerir a Brian dictar al bot `/decidi no perseguir RNN/LSTM` (el bot no sabe que
    es ruido descartado) · valor_on sigue OFF fuera de brian (encenderlo donde Brian quiera con
    `/dmn valor on`).
  - 🟠 **B puente/API para mercado → 🟢 EN CONSTRUCCIÓN** (`Cuerpo/Ronda_FrenteB_Puente_Mercado.md`):
    13 modos de fallo analizados. **LOCKED:** tenancy híbrido · BYOK obligatorio p/clientes · panel
    COMPLETO · URL: Funnel ya + dominio al 1er cliente. **F1 ✅ (commit `2bf4a99`, server SIN push):
    la demo tiene URL FIJA PARA SIEMPRE — `https://for3s.tail6749e5.ts.net`** (Funnel persistente,
    E2E desde internet 200/83ms, 401 sin key, check en /salud + alerta si cae — prueba negativa
    hecha, scripts frágiles deprecados). **F2 ✅ (`79b156d`): control PRECISO de acceso** — estados
    activo→suspendido→revocado (terminal) auditados + keys `f3k_` por cliente (identidad ES la key)
    + expiración + scopes + CLI api_admin. 🐛 Bug de resurrección cazado (revocación estaba rota).
    E2E por la URL pública 401/403/200. **F3 ✅ (`330b891`): cuotas + metering persistente** — tabla
    api_consumo (tokens/costo/ms por llamada) + gate rate/cuota en BD (mata el rate amnésico) +
    api_metering.resumen() para el panel. Mata bugs #4/#5/#7 de la Ronda. E2E: llamada→consumo real
    registrado, cuota→429. 🐛 cost_usd vs costo() cazado + código huérfano limpiado. **Sigue: F4
    PANEL ADMIN** (referencia Godinez: Next16/React19/Tailwind4, Convex→nuestro Postgres + waitlist
    + uso por persona). Luego F5 carga · F6 estándar de datos. La charla (VALIDACION_WEB3) CERRADA.
  - 🟡 **C multi-canal** (WhatsApp/correo/análisis) · 🟣 **E confianza para delegar** — pendientes.
  - 🔴 **BUG-EQUIPO → ✅ FIX construido+probado SOLO en `brian`** (capsula_equipo en identidad.py +
    1 línea en specialists.py; el specialist ya sabe qué es For3s). **Falta:** que Brian pruebe en
    Telegram → commit firmado → propagar al resto de instancias. Diseño: `Cuerpo/Diseno_Fix_Equipo_
    Sin_Identidad.md`. Memoria: `project_bug_equipo_sin_identidad`. RNN/LSTM aclarado (no aplica).
  - 🔵 Línea futura: modelito que aprende qué memoria es valiosa (no hoy, requiere volumen de datos).
- **Cerrar ENTRENAMIENTO** (§4 arriba) cuando Brian diga — mayormente esperar noches + examen.
- **✅ CHARLA AI×Blockchain CERRADA por Brian (2026-07-14)** — todo el bloque VALIDACION_WEB3
  dado por terminado. **🎯 FOCO ACTUAL: Frente B (puente/API para mercado + panel admin).**
- **Congelados hasta orden de Brian** (NO empujar): brechas OpenClaw/Hermes (OC-*, HG-*:
  multi-canal, voz, cron conversacional, nudges, curator…) · identidades secundarias
  (Empleado/Design → rasgos, con gate) · descubribilidad (SEO/AEO/GEO).
- **Deuda no urgente:** H9 D1-D8 · H10 HP1-HP6 · §EXTRAS (BYOK, PR9, DIST…).
- Lista COMPLETA y detallada: **`Doc/PENDIENTES.md`**.

## 6 · 🏆 Incubathon (jul 2026) + 🌉 puente a otros Mente OS

- **2º lugar de 200 empresas** con **NavigoX** (marketplace de turismo). **La capa API de For3s fue
  el marco que cerró el pitch.** For3s OS **VALIDADO como infraestructura con demanda real**: 2
  clientes quieren For3s + más gente quiere la infra. Memorias: `project_incubathon_2do_lugar_validacion`
  + `project_hito_hoteleria_navigox`. Cierre completo en `Doc/Bitacora_Progreso.md` (Julio 2026).
- **🌉 NavigoX vive en su PROPIO Mente OS** (`~/5M-incubathon/Mente/`). En ESTE Mente OS está
  **CERRADO** (se registra el hito; su trabajo NO continúa aquí). ⛔ **NUNCA leer `~/5M-incubathon/`
  sin gate.** Abrir: Brian escribe `acceder mente <proyecto>` (ej. `acceder mente navigox`) + por qué
  → solo lectura + reporte. Cerrar: `cerrar mente <proyecto>` o al terminar la tarea. **Motivo:
  evitar que el consumo de tokens se dispare.** Registro/reglas: `Doc/Puentes_Mente_OS.md`.

## 7 · Reglas de oro con Brian (permanentes)

- ⛔ **NUNCA implementar sin explicar+aprobar primero** (`feedback_explicar_antes_de_implementar`).
- 🏗️ Hitos grandes = **Método de Fases "F"** (`Cuerpo/ESTANDAR_Metodo_Fases_F.md`): explicar→
  aprobar→construir · investigar terreno · curiosidad que caza bugs · **batería §5-BIS** (verifica
  TODO el sistema, no el carril) · red de seguridad demostrable · commit firmado · server-primero.
- 📏 **Server-primero:** desarrollar+probar en el server; push a GitHub SOLO con orden explícita.
- ⛔ **NO loops de espera / procesos de fondo** contra el server que sigan si Brian cierra (gasta cuota).
- ⛔ **NO cambiar el modelo** (Brian lo fija con /model). Modelo del bot = sonnet-4-6 (NO bug).
- ⛔ **NO sesgar todo hacia la charla/descubribilidad** — importan pero NO son su foco; él marca el momento.
- 🔒 Master KEK offline · Brian nunca ve plaintext · audit inmutable · ante duda → preguntar.
- 🧹 **/clear es seguro cuando la conversación crezca** (Mente OS + memorias guardan todo).

---

## 📍 PUNTEROS — si necesitas MÁS que este brief

| Necesitas… | Lee… |
|---|---|
| **TODOS los pendientes a detalle** | `Doc/PENDIENTES.md` |
| **Carril de mejora continua de CONFIANZA (reactivar el Frente E)** | `Doc/Carril_Mejora_Continua_Confianza.md` |
| **Carril PRESENCIA/Descubribilidad (landing+SEO+AEO+analítica, dormido)** | `Doc/Carril_Presencia_Descubribilidad.md` |
| **Carril MULTI-CANAL (Frente C: WhatsApp/correo/análisis, dormido)** | `Doc/Carril_Multicanal.md` |
| **Telemetría de conversaciones (registrar ANTES de cada /clear — regla CLAUDE.md)** | `Cerebro/Registro_Conversaciones.md` |
| Hito ENTRENAMIENTO: reporte de ejecución completo | `Doc/Entrenamiento_Ejecucion_Reporte.md` |
| Hito ENTRENAMIENTO: plan + flujo + radiografías de los 7 agentes | `Cuerpo/Plan_Implementacion_Entrenamiento.md` · `Cuerpo/Flujo_Extraccion_Entrenamiento.md` · `Doc/Radiografia_*` |
| E6 backlog profundo (archivo por archivo) | `Cuerpo/Plan_Backlog_Profundo_E6.md` · `Doc/Entrenamiento_Catalogo_Codigo.md` |
| Diseño arquitectónico maestro (11 nodos + 3 pilares) | `Cerebro/For3s_OS_Grafo_Maestro.md` |
| Historia cronológica de cierres (qué pasó cada periodo) | `Doc/Bitacora_Progreso.md` |
| **Puente a otros Mente OS (NavigoX…) — reglas del gate** | `Doc/Puentes_Mente_OS.md` |
| **Snapshot del estado ANTERIOR (RETOMAR viejo íntegro, 84KB)** | `Doc/Estado_Sesion_Snapshot_2026-07-07.md` |
| Estado/reglas/contexto histórico grande (200KB) | `Doc/Estado_Sesion_Continuidad.md` (solo si imprescindible) |
| Multi-instancia (gestor `for3s`, aislamiento) | memoria `project_multi_instancia` |
| Servidor: acceso + specs | memoria `reference_servidor_for3s` |
| Comparaciones de construcción vs Hermes/OpenClaw | `Doc/Comparacion_For3s_OS_vs_Hermes_Construccion.md` · `…vs_OpenClaw_…` |
