# RETOMAR — Cold-Start Brief (LEER ESTO PRIMERO) ⚡

> **Propósito:** el ÚNICO archivo que necesitas leer al retomar. Pequeño A PROPÓSITO
> (ahorro de tokens — Brian lo notó de nuevo 2026-07-07: cuando crece, releerlo es caro).
> **REGLA DE HIGIENE:** este archivo NO debe pasar de ~200 líneas. Al cerrar sesión, si
> creció, mover lo viejo a `Estado_Sesion_Continuidad.md` (o al último snapshot) y dejar
> aquí SOLO el estado vigente + punteros. La historia va a la Bitácora, no aquí.

**Última actualización:** 2026-07-23 (🎉 FRENTE F0 "enrutar correo→instancia" COMPLETO 4/4 + 🔴 fix red server (Telegram) + barra de uso por key + verificaciones profundas de la demo).


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
Comparten SOLO: máquina + imagen `for3s-agent:local` (hoy **v0.20.0**) + suscripción Claude (**1 solo cupo** para todos).

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

Diseño 100% LOCKED (R1-R10, 11 nodos, 3 pilares). **v0.20.0 CONECTORES SELF-SERVICE. schema BD v47.** 13 hitos
H1-H13 + Identidad Viva + Auto-conciencia + Multi-instancia + Execute-code + Paridad Hermes
(5/5) + intern-os + CI + Frente B + Molde + Trace + Frente E + **super-cerebro (ambos agentes
entrenados+examinados, §4).** **Cero bugs abiertos** (12 cazados y cerrados en los exámenes).
**✅ TRÍADA SINCRONIZADA (2026-07-19/20): server = GitHub (origin for3slabs/for3s-os + backup
for3slabs/for3s) = local (`For3s-OS/`) en HEAD `f50a5db`. CI+Trivy verdes. 260 tests.**
**✅ LAS INSTANCIAS EN v0.20.0** (3 vivas + jazz/mashe verificadas y apagadas por diseño).
Cliente API real: NavigoX (hotel-recepcion, no consume activo) + jazz-id (prueba). Datos limpios.
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

## 4 · 🎓🎓 SUPER-CEREBRO COMPLETO — AMBOS AGENTES ENTRENADOS+EXAMINADOS ✅✅ (2026-07-18/20)

**El hito doble más grande del proyecto (jornada de 30h, sesión S4). TODO CERRADO:**
- **brian 🍓 (6 agentes OpenClaw, E0-E6):** 22,406 eps vivos, **99.94% consolidado, grafo 1,335
  conceptos** (noches ADELANTADAS: encadenador 10 tandas freno 0.99). **EXAMEN 94.3% (33/35)** —
  trampas 6/6, honestidad de corpus. Reporte E0-E6: `Doc/Entrenamiento_Ejecucion_Reporte.md`.
- **Foresito 👑 (las 6 fuentes de la EMPRESA):** 1,829 eps (741/741 archivos, 0 omitidos, código
  con marca de versión), 95% digerido (grafo 2,687 nodos). **EXAMEN 98.8% (41.5/42)**. Es el
  **AGENTE MAESTRO**: lee `for3slabs/mente-os-maestro` EN VIVO (puente E + skill id 22).
  Wiki-hackathons EXCLUIDO por Brian (externo, importable después). Backup RESTORE-verificado
  en `~/backups-foresito/` + reversa demostrada. Ronda: `Cuerpo/Ronda_Entrenamiento_Foresito.md`.
- **Los exámenes cazaron 12 hallazgos (H-1…H-11 + B1), TODOS con fix + validación SISTÉMICA**
  — joya H-11: la contraseña del server vivía en 60 eps de 2 instancias → redactada + tubo
  blindado. **Registro maestro: `Doc/Examen_Foresito_T6_Hallazgos.md`.**
- Runners reusables (re-entrenos/aceleración) en `~/entrenamiento-runners/` del server.

## 5 · 👉 ESTADO ACTUAL + PRÓXIMO PASO (arrancar aquí tras /clear)

**🏗️ HOY (2026-07-24/26) — LA DEMO PASÓ DE MVP A PRODUCTO: BD reestructurada + código pulido
+ optimizado.** Jornada larga sobre `marca-personal` (repo `ElBrAyAn1967/For3s`, Neon PG18).
Detalle completo: memoria `project_reestructuracion_bd_demo` · planes en el propio repo del sitio
(`DEMO_MAPA_BLOQUES.md`, `DEMO_REESTRUCTURACION_PLAN_F0.md`, `DEMO_AUDITORIA_CODIGO.md`,
`DEMO_PLAN_OPTIMIZACION.md`). Método: **atómico por bloques, verificar antes de avanzar.**

- **BD (F1-F6) ✅** — `demo_instancias` = FUENTE ÚNICA DE VERDAD (modo, cupo, puente URL+key
  CIFRADA) + 7 FKs + catálogo de estados + `demo_llaves` (revocables) + `demo_eventos`
  (telemetría) + **`demo_config`** (parámetros editables con UPDATE, **sin push ni redeploy**).
  Fantasmas eliminadas. **Escalar = 1 INSERT** (probado con instancia 'acme').
  Verificada: integridad 7/7 · candados 8/8 · E2E 6/6 · endpoints 8/8 vivos.
- **CABLEADO (C1-C6p1) ✅** — el código lee de la BD: puente cifrado, doble-escritura,
  cupo en vivo, revocación, telemetría.
- **PULIDO (P1-P7) ✅** — P1 la instancia es un DATO (antes lista fija en 27 archivos: la BD
  escalaba y el código no) · P2 UNA puerta de acceso (`acceso.ts`; antes 3 fuentes en cascada) ·
  P3 un solo cupo · P4 **−434 líneas** de subsistema muerto · P5 código muerto + 🐛 bug de logout ·
  P6 correo real con Resend · P7 TODO va al agente del usuario (antes conectores/BYOK iban a general).
- **OPTIMIZACIÓN (O-F1..O-F5) ✅** — heartbeat **11→3-4 viajes a Neon (−68%)**, N+1 eliminado
  (10→1 UPDATE), memoización por operación, freno de mantenimiento (260→4 en 60 s).
  Con 100 usuarios: 220→70 q/s. **Regla madre: optimizar NO es romper** (build + comportamiento
  verificado idéntico en cada fase).
- **`for3sChat.ts` refactorizado** — capa base única `llamarAgente()`: plomería 116→24 líneas
  (−79%); un endpoint nuevo pasa de ~25 líneas a 3.
- **🐛 9 bugs cazados y cerrados** — dueño entraba sin código · refrescar rompía la sesión · key
  perdida al promover · rol nunca se actualizaba · hilos de homónimos colisionaban · keys f3k_ y
  BYOK iban al agente equivocado · cupo del panel hardcodeado · logout no limpiaba la cookie de
  dueño · tema `hoteles` heredado del Incubathon.
- **🎓 CASO DE ESTUDIO documentado** (reutilizable): `Cuerpo/CASO_Default_Peligroso_Tema_Hilo.md`
  — la regla "un default NUNCA debe apuntar a algo con dueño" + checklist para limpiar valores
  heredados. Salió de que Brian cazó un fix mío peligroso (`general` como default habría metido a
  cualquier cliente en el hilo privado del dueño).
- **Estado del código:** sitio pusheado hasta **`1c54a49`**. Agente: `api_channel.py` con el tema
  neutro listo en `~/for3s-os` del server (respaldo `.bak-tema`), **pendiente de rebuild de imagen**
  — NO urgente: el sitio ya manda el tema explícito, así que el fix ya funciona.
- **⏳ Pendientes de esta ronda:** C6 parte 2 (borrar columna `kind`, tabla `demo_accounts`, env
  vars del puente) · panel admin de dueños (`registrarDueno`/`listarDuenos` ya existen, sin UI) ·
  `container.ts` sigue NO-OP (encender/apagar agente) · identidad de instancia del agente
  (memoria `project_pendiente_identidad_instancia_agente`) · un hilo/key único por dueño.

---

**🎉 (2026-07-23) — FRENTE F0 "ENRUTAR CORREO→INSTANCIA" COMPLETO (4/4) + FIX RED SERVER + más:**

**🔴 FIX RED DEL SERVER (Telegram volvió):** los agentes NO respondían en Telegram
(desde 21-jul). Causa: el server prefería IPv6 pero NO tiene salida IPv6 real (solo
la de Tailscale, `fd7a:`) → `api.telegram.org` (que resuelve por IPv6) daba HTTP 000;
IPv4 funcionaba (302). NO fue la demo ni nuestros cambios (verificado: el commit
sospechoso no tocó red). Fix aplicado: `precedence ::ffff:0:0/96 100` en `/etc/gai.conf`
(respaldo `gai.conf.bak-ipv4fix`, reversible) → prefiere IPv4, **conserva IPv6/Tailscale**.
Reiniciados brian/foresito/general → Telegram conectado sin NetworkError. Verificado en vivo.

**🎉 FRENTE F0 "enrutar correo del dueño → su instancia" — 4/4 PIEZAS, probado E2E con
evidencia del server** (sitio `ElBrAyAn1967/For3s`, commits `a03833f`→`529786e`; server
preparado, no en repo). Cuando el dueño (ej. brayan002150@gmail.com) entra a la demo, lo
reconoce como dueño de brian, verifica por código, y lo enruta a SU instancia (no general):
- **P1 puente:** tabla Neon `demo_duenos` (correo→instancia) + `POST /api/demo/check-dueno`.
  Sembrado brayan002150→brian. Las instancias del server están AISLADAS → el mapa vive en Neon.
- **P2 verificación:** tabla `demo_verificaciones` (código HASHEADO, 10min, 5 intentos,
  un-solo-uso). Resend (`re_3Nec...` en .env.local, `RESEND_FROM=onboarding@resend.dev`).
  `verify/send` + `verify/check`. 6 defensas probadas.
- **P3 enrutador:** brian con canal API ON + su key propia + puerto fijo 8798 + ruta pública
  en Funnel `for3s.tail6749e5.ts.net/i/brian`. general intacto en `/`. `chatDueno()` enruta
  a la instancia del dueño verificado. Verificado: el chat llegó a BRIAN (hilo en su BD), NO general.
- **P4 UI:** `GeneralRegister` detecta dueño→pide código→entra. Correo cualquiera→general sin fricción.
- **⚠️ FALTA para producción:** en Vercel agregar `RESEND_API_KEY`, `RESEND_FROM`,
  `FOR3S_INST_BRIAN_KEY=for3s_sk_6de4db98f4bb265c29b478709d186333` · verificar dominio en
  Resend (onboarding@resend.dev solo manda a pruebas, no Gmail) · ROTAR keys expuestas (Resend + brian).

**📊 BARRA DE USO REAL POR API KEY f3k_ (server+sitio) COMPLETA:** `/v1/miskeys` expone
uso por key (llamadas/tokens/costo-cupo/serie desde `api_consumo`; cada key = su client_id).
Sitio pinta sparkline. **Server commit `8a5eb5e` = local `a699de6` (código byte-idéntico, md5
verificado) SIN push.**

**🔎 VERIFICACIONES PROFUNDAS de la demo (todo SANO, verificado en vivo):** aislamiento de
hilo por persona (`api:<hash-correo>:<tema>` / `tg:<uid>`, nadie accede al de otro) · concurrencia
(10+2 al mismo tiempo NO rompe, encola con "repartidor de carriles" concurrency.py; con BYOK cada
quien su cuota = sin fila) · el hilo por persona existe en TODAS las instancias (canal API en
general/foresito, Telegram en todas) · invitar equipo a brian por Telegram (`/invitar`) SÍ, por web
NO (era el frente F0). 2 hallazgos demo General registrados (BYOK fire-and-forget, tema "hoteles").

**⬇️ Contexto del 22-jul abajo. Sigue: cerrar F0 en producción (Vercel/Resend), o lo que Brian marque.**

---

**🖥️ (2026-07-22) — REDISEÑO DEMO ESCALABLE + PANEL CON "MÁS MANOS" (todo en el SITIO
`marca-personal`, repo `github.com/ElBrAyAn1967/For3s`, deploy Vercel `for3s.vercel.app`):**
Contexto: Brian PAUSÓ los pendientes grandes para volver For3s "operable sin él" (que pueda
decir "está listo para prestárselo a alguien"). Trabajo por PIEZA, Brian valida cada una.
- **Demo escalable (los links 1:1 salieron de variables de Vercel → a Neon):** BD Neon
  (`neondb`, la fuente de verdad de la demo, NO tailnet — Vercel no alcanza el tailnet).
  `demo_accounts` ganó `kind='privado'` + columnas (nombre/correo/instancia); `demo_users`
  ganó `kind_ui`. Botón **"＋ Agregar"** en `/for3s-admin`→Demo: crea 1:1 privada (genera
  link `/demo/<token>` en código) o General a mano. El link 1:1 ahora **funciona** (lee de
  Neon, no de Vercel). La 1:1 es un usuario más (vive en AMBAS tablas). Entrada a la demo
  NO se tocó (nombre+email igual). `foresito` NO es demo-able (instancia interna, riesgoso).
- **Panel "más manos":** editar persona (nombre/correo real) · colores por demo (jazz morado
  · mashe verde · brian amarillo · general gris) · filtros por instancia · **eliminar
  personas** (borra también su puerta 1:1) · **cambiar demo = MOCKUP honesto** (mueve solo
  `kind_ui`; el hilo real `kind` NO se mueve; Neon sabe la verdad).
- **Dentro de la demo:** chat responsivo (sin menú superior duplicado en desktop, se conserva
  Cerrar sesión, el chat ocupa el ancho) · conectores n8n + NotebookLM (arriba de Adobe) ·
  Perfil = pendiente.
- **📊 BARRA DE USO REAL POR API KEY f3k_ (server + sitio):** ⚠️ ÚNICO cambio en el SERVER hoy.
  El canal `/v1/miskeys` ahora expone por key: total_llamadas/total_tokens/costo_usd (solo
  NUESTRO cupo, byok=false)/serie por día — desde `api_consumo` (ya existía; cada key ES su
  client_id). El sitio pinta un **sparkline** (línea que sube/baja estilo GitHub) + los números.
  Verificado E2E con chat real (uso subió). **Server commit `8a5eb5e` SIN push (server-primero).**
  Sitio pusheado (commits `a03833f`→`05058b3` en ElBrAyAn1967/For3s).
- **Vercel Env Vars (Brian las limpió):** quedan 5 críticas (DEMO_DATABASE_URL→Neon,
  DEMO_ADMIN_PASSWORD, DEMO_ENC_KEY, FOR3S_GENERAL_API_KEY, FOR3S_GENERAL_BASE). Se quitaron
  DEMO_JAZZ/MASHE/BRIAN_TOKEN+EMAIL (ya viven en Neon). Demo verificada viva tras limpiar.
- **🔮 PENDIENTES NUEVOS registrados (memorias):** (a) **migrar hilos entre agentes** (el mockup
  cambiar-demo lo espera, NO codificado) · (b) **reconstruir encender/apagar agente 1:1** (Brian:
  importante pero se rehará de forma especial; vars DEMO_AGENT_CONTROL_URL/_TOKEN quedaron sin uso)
  · (c) barra de uso = COMPLETA hoy. Todos con Ronda F0 cuando Brian diga.
- **⚠️ Repo del SITIO ≠ repo de For3s OS:** el sitio vive en `ElBrAyAn1967/For3s` (marca-personal);
  el server/agente en `for3slabs/for3s(-os)`. HOY solo se tocó el sitio + 1 archivo del canal
  (`api_channel.py`) del server (commit local, sin push). La tríada de For3s OS sigue en `f50a5db`.

---

**🚀 v0.19.0 "ENTRENADO" DESPLEGADA TOTAL (2026-07-19/20):** tríada de código en **`f50a5db`**
(server = GitHub origin `for3s-os` + backup `for3s` = local) · **las 5 instancias verificadas EN
VIVO** (3 vivas propagadas + jazz/mashe probadas con batería completa y devueltas a su estado) ·
CI ✅ + Trivy ✅ · Mente OS pusheado (`mente-os-for3s` `80aed31`) · Maestro al día (`8681d7c`).
Historia de v0.16→0.18 (MERCADO, Molde, Trace, Frente E): **Bitácora Julio** + `CHANGELOG.md`.

**⭐ NUEVO (2026-07-20) — MAESTRO PUENTES C+D ✅ CONSTRUIDOS Y E2E** (`Cuerpo/Ronda_Maestro_
Puentes_C_D.md`): el Maestro dejó de ser lista → es BUSCADOR semántico + RED navegable, todo
sobre UN núcleo (punteros.tsv + puerta única + un indexador + IDs compartidos + una superficie
`/v1/maestro/*` en Foresito). `maestro indexar --todo | subir | buscar "<preg>" [--contexto] |
grafo <nodo>`. Jazz solo ve su carril (probado). 4 bugs cazados. Server commit `0cac57a` firmado
**SIN push** (esperando orden). ⏳ colas: embebido rama for3s termina solo en el server ·
smoke-test de Brian a Foresito por Telegram ("busca en el maestro…") · re-indexar tras pushes.

**📌 PENDIENTES DE BRIAN (2026-07-20, detalle en PENDIENTES.md §Super-cerebro):** ① smoke Telegram
a Foresito ("busca en el maestro dónde…" → debe EJECUTAR y citar rama:ruta) · ② probar en brian-bot
una skill del entrenamiento (primera vez completas tras el fix S1) · ③ decidir S3 (canal API sin
tools narra ejecuciones — ¿tool-loop para clientes API o documentar el límite?).

**👉 PRÓXIMO PASO: Brian marca el foco.** Sobre la mesa:
- 🔌 **⭐ NUEVO PENDIENTE GRANDE (2026-07-20): CONECTORES SELF-SERVICE** — que el usuario conecte
  herramientas con UN botón (OAuth del proveedor) y su agente/rama las tenga al instante, sin pasar
  por Brian; correo admin por instancia; general multi-tenant (solo comparten el agente). Visión:
  `Alma/Vision_Conectores_SelfService_Panel_Agente.md` · PENDIENTES §1. Arranca con Ronda F0.
- 🅰️ nuevo frente de producto (🟡 C multi-canal · F-A2 sub-agentes paralelos de /mision · carriles).
- ⏳ pilotos VIVOS externos: Jazz usa su bot (jazz verificada v0.19.0) + NavigoX retoma consumo.
- Pendientes técnicos menores: **CodeQL rojo desde el 17** (pre-existente) · validar torch 2.13
  (quitar 2 ignores pip-audit) · semillas de diseño H-4 (peso de respuestas propias en ranking) y
  H-6 (presupuesto chars por chunk) — Ronda si Brian quiere.

**🔄 Carriles vivos DORMIDOS** (se despiertan cuando Brian diga): Confianza
(`Doc/Carril_Mejora_Continua_Confianza.md`) · Presencia (`Doc/Carril_Presencia_Descubribilidad.md`)
· Multi-canal (`Doc/Carril_Multicanal.md`) · Maestro (evoluciona a carril).
⚠️ NavigoX vive en `~/5M-incubathon/`, CERRADO — no leerlo sin gate (§6).

## 5-bis · Cerrados grandes recientes (solo punteros — historia en Bitácora Julio)

- 🌐 **SUPER-CEREBRO CONECTADO ✅✅ COMPLETO** (visión `Alma/Vision_Mente_OS_Maestro_Y_Foresito_
  Entrenado.md`): 🅱️ Maestro F1-F5 (repo + comandos + permisos + ramas; evoluciona a carril) +
  🅰️ Foresito entrenado/examinado + 👑 Agente Maestro con puente E (ver §4).
- 🎯 **APRENDIZAJES DE CAMPO (post-Incubathon) — los 5 frentes:** 🔴 A consumo ✅ (regla /clear
  moderada por mí) · 🔵 D ✅ H13 DEVUELVE v0.16.0 · 🟠 B ✅ MERCADO v0.17.0 (panel
  `for3s.vercel.app/for3s-admin`, URL fija, molde, Trace) · 🟣 E ✅ CONFIANZA v0.18.0 (carril
  dormido) · 🟡 C multi-canal PENDIENTE (sin urgencia). Doc madre: `Alma/Aprendizajes_De_Campo_
  Post_Incubathon.md` · detalle `Doc/PENDIENTES.md`.
- Menores abiertos: /decidi RNN-LSTM al bot · `/dmn valor on` fuera de brian · UX (/salud virgen ·
  rate/min · /olvidar "%") — en PENDIENTES.
- **Congelados hasta orden de Brian** (NO empujar): brechas OpenClaw/Hermes (multi-canal, voz,
  cron conversacional, nudges…) · identidades secundarias · descubribilidad (SEO/AEO/GEO).
- **Deuda no urgente:** H9 D1-D8 · H10 HP1-HP6 · §EXTRAS. Lista completa: **`Doc/PENDIENTES.md`**.

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
| 🎓 **Caso: limpiar un valor heredado/hardcodeado sin romper** (la regla del "default peligroso" + checklist) | `Cuerpo/CASO_Default_Peligroso_Tema_Hilo.md` |
| **Demo: mapa de bloques/sistemas · plan BD · auditoría de código · plan de optimización** | en el repo del sitio: `marca-personal/DEMO_*.md` |
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
