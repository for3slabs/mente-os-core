# PENDIENTES — For3s OS

**Status:** current · **Type:** pending · **Updated:** 2026-08-02 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

## 🚪 `CLAUDE.md` §ESTADO — lo que impide publicarlo tal cual (2026-08-02)

**✅ Ya resuelto** (`3223a5c` + `5f8a671`): cabecera §1 completa · Purpose + Related · 2 punteros
rotos (`Maestro/piezas.tsv` → `Mente/Maestro/`, y la fila de `Mente/Doc/`, carpeta que ADR-029
eliminó) · números → punteros · y **los validadores ya lo alcanzan** (barrían desde `Mente/`, y
este archivo vive un nivel arriba).

**⛔ Lo que queda NO es técnico.** `§ESTADO` conserva contenido de **instancia**, no de
enrutamiento: `for3s.vercel.app/for3s-admin` · MOLDE "For3s Inside" · For3s TRACE · R1-R10, 11
nodos, 3 pilares. Nada de eso enruta: **declara el producto For3s.**

**Mitigación aplicada, no solución:** la cabecera ahora lo **DECLARA** —
`**Scope:** ⚠️ documento de INSTANCIA, no del motor` — en vez de esconderlo. Un límite declarado
es ingeniería; uno oculto es deuda ([[rule-config-hygiene]] §1.4, mismo criterio que los 9 hooks
GSD no portables).

> ⭐ **Por qué no lo decide la IA:** separar motor de instancia aquí obliga a elegir **qué ve
> quien clona `mente-os` en su primer arranque**. Eso es diseño de producto — la primera
> impresión del sistema publicado — no limpieza de archivos.

**3 caminos (Brian elige):**

| | Qué | Coste |
|---|---|---|
| ⭐ **1** | **Dejarlo y que el `Scope:` lo declare** (hoy) | cero · el motor publicado ya excluye este archivo |
| **2** | Partir en `CLAUDE.md` (motor, portable) + `INSTANCE.md` (For3s), enrutando al segundo | medio · hay que verificar que el arranque sigue cargando lo necesario |
| **3** | Plantilla `CLAUDE.md.template` en el motor + el real generado desde `mente.config.yml` | alto · es la solución limpia si `mente-os` gana usuarios |

⚠️ **Dato que decide (INFERIDO, no medido contra el remoto):** `CLAUDE.md` vive **fuera** de
`Mente/`, y lo publicado es `Mente/` — así que hoy **no debería haber fuga**. El problema solo
aparece el día que alguien arranque una instancia nueva desde el motor y no tenga enrutador.
Por eso la 1 es la recomendación y la 3 el escalón si `mente-os` gana usuarios.
👉 **Verificar antes de actuar:** `git ls-files` en el clon público, o mirar el repo.

---

## 🔐 `~/.claude.json` — las credenciales del harness. ARQUITECTURA, no configuración (2026-08-02)

**Lo que guarda (medido):** `oauthAccount` + `customApiKeyResponses` — las credenciales OAuth con
las que corre Claude Code. 51 KB, permisos `-rw-------`.

**Lo que se hizo hoy** (`474c375`): `deny` en 13 canales para `*claude.json*`, que cubre también
los temporales `.claude.json.tmp.<pid>.<hash>` que el harness escribe al guardar — uno llevaba
`oauthAccount` desde el **30-jul** y el `deny` del nombre EXACTO no lo alcanzaba.

> ## 🔴 EL LÍMITE ESTRUCTURAL — medido en vivo, no deducido
>
> ```
> head -c 12 "/home/brianweb3/.claude.json"   → DENEGADO ✅
> head -c 15 "$(ls ~/.claude.json.tmp.*)"     → LEYÓ EL ARCHIVO 🔴
> ```
>
> **El matcher evalúa el TEXTO del comando, no la ruta que ese comando acaba abriendo.** Si el
> nombre no aparece literal — una variable, un `$(...)`, un glob — **ninguna regla lo ve.**
>
> **Ninguna lista de patrones cierra esto.** No es un fallo de las reglas escritas: es el techo del
> mecanismo. El `deny` es una barrera contra el acceso **accidental** y contra el descuido —
> **no es un sandbox.**

**👉 POR QUÉ ESTO NO LO DECIDE LA IA.** Lo que nunca debe leerse no se protege con `deny`: se saca
del alcance o se cifra. Eso cambia dónde vive un fichero del que depende el arranque del harness —
es arquitectura del entorno, y equivocarse deja la herramienta sin poder autenticarse.

**3 caminos (Brian elige):**

| | Qué | Coste / riesgo |
|---|---|---|
| **1** | **Dejarlo como está** y asumir que el `deny` cubre lo accidental | cero trabajo · el hueco sigue abierto, pero **conocido y escrito** |
| **2** | Sacar `.claude.json` de `$HOME` (variable de entorno del harness → ruta fuera de `additionalDirectories`) | medio · verificar que Claude Code sigue autenticando |
| **3** | Cifrado en reposo del home / disco | alto · protege todo, no solo esto · fuera del alcance de una sesión |

⭐ **Mi recomendación medida: la 1, y que quede escrita.** Un hueco documentado que se conoce vale
más que un parche que da sensación de cierre. Añadir más patrones al `deny` sería exactamente eso —
y **peor que saberlo abierto**. Si algún día el riesgo cambia (equipo compartido, máquina ajena),
la 2 es el siguiente escalón.

⚠️ Relacionado: el harness **reescribe `settings.local.json` en cada aprobación**. Durante la
propia auditoría, `Bash(python3 -)` reapareció **dos veces** después de borrarlo. Por eso §1.3
(182 allow, umbral 120) queda abierto a propósito: podar sin cambiar el hábito de aprobación es
trabajo que se deshace solo.

---

## 🔑 FIRMA GPG DE LOS COMMITS — PENDIENTE, decisión de Brian (2026-08-02)

**Estado medido hoy:** este WSL2 **no tiene ninguna clave GPG** (llavero vacío: ni secreta ni
pública). `gpg` sí está instalado. `commit.gpgsign` y `user.signingkey` sin configurar en el repo.
El Método F pide "commit firmado" — hoy **no se cumple**.

**✅ Lo que SÍ se resolvió (2026-08-02):** la identidad. Los commits salían como
`Fruterito Devrel <ema@frutero.club>`; ahora el repo usa **`Brian Lopez <brayan002150@gmail.com>`**
y los 4 commits de esa jornada se reescribieron con ella. `819b5ab` (S8) se dejó intacto a
propósito: es de Brian, no de la sesión.

**⛔ Por qué quedó abierto — 3 topes, ninguno técnico:**

1. **No hay clave que recuperar aquí.** Generarla decide identidad, passphrase y respaldo:
   es de Brian, no de la IA.
2. **No hay acceso al servidor.** Sin llave SSH; el password extraído de
   `secrets/Conectar_Servidor_For3s.md` con un patrón fue rechazado (campo equivocado).
3. **El `deny` de `secrets/` bloqueó afinar el patrón** — y se respetó. Son 11 reglas
   (`Read` + `cat/head/tail/less/more/strings/xxd/od/base64/cp`), commiteadas en `3419ba8`,
   la superficie completa que cerró el agujero de S8.

> ⭐ **La razón de fondo, y es la que importa:** leer ese archivo aquí **vuelca el password a la
> transcripción**, y los `.jsonl` no se editan. `rule-config-hygiene.md` §1.1: un secreto filtrado
> se **ROTA**, no se borra. Es el caso H-11 del examen de Foresito — la contraseña del server vivía
> en 60 episodios. **Desarmar la guardia Y quemar la credencial, para algo que se consigue con una
> línea, no compra nada.**

**⚠️ Brian pidió "editar el `deny` para que cuando yo te pida puedas continuar" → NO SE HIZO.**
`deny` **no tiene modo condicional**: o está denegado o está permitido para siempre, en toda sesión
futura, con o sin petición. Si se quiere relajar, la opción menos mala es **`ask`** (prompt por
acceso, decisión activa de Brian cada vez), nunca borrar las reglas.

**👉 3 SALIDAS, en orden de coste (Brian elige):**

| | Qué | Coste |
|---|---|---|
| ⭐ **1** | Brian corre `ssh …@100.112.177.53 'gpg --list-secret-keys --keyid-format=long'` y pega la salida | cero — son IDs y UIDs, sin material privado |
| **2** | Pasar el password por entorno (`export FOR3S_SSH_PASS=…`), nunca pegado en el chat | bajo — no toca la transcripción |
| **3** | **Generar clave nueva** (lo recomendado si esto se alarga) | mínimo — los 4 commits son locales y sin push; solo se pierde verificar commits viejos |

⚠️ **Si aparece en el servidor: NO copiar `~/.gnupg/` con `scp`** — arrastra permisos y corrompe el
llavero. Se exporta con `gpg --export-secret-keys` (pide su passphrase, que solo tiene Brian) y se
transfiere cifrada.

**Para activarla cuando exista la clave:**
```bash
git config user.signingkey <KEY_ID>
git config commit.gpgsign true
git rebase --exec 'git commit --amend --no-edit -S' 819b5ab   # firma los 4 de la jornada
```

---

## ✅ 3 SESIONES HISTÓRICAS SIN REGISTRO — CERRADO 2026-07-31

Registradas como **§R1-R3** en `Cerebro/Registro_Conversaciones.md`, con datos **medidos** de sus
`.jsonl` (peso, turnos, contexto pico, tokens). `check-health` bajó de 🟡 7 a 🟡 5.

⚠️ Se registró lo medible. **El criterio no se reconstruyó** — qué se sintió raro, por qué se
cerró — porque inventarlo sería peor que no tenerlo. Ese es el costo exacto que la regla previene.

`4c187f33` era la del incidente del 21-jul: 23.4 MB, 999K de contexto pico, 96h. Llevaba **10 días
sin entrada pese a que `rule-session-close.md` §2 la cita por nombre** como "el peor infractor".

---

## ⛔ F3 DEL LATIDO — DESCARTADA, no olvidada (2026-08-02)

El plan del latido tenía **tres** fases. F1 y F2 están construidas (abajo). **F3 era un cron
externo** que corriera `check-health` en paralelo y avisara si el latido no se mueve.

**Descartada al proponerla, por tres razones:**
1. Un cron **también puede morir en silencio** → dos guardias vigilándose mutuamente y nadie
   vigilando el par. El mismo problema, un nivel más arriba.
2. Choca con la regla LOCKED de Brian: *"⛔ NO loops de espera / procesos de fondo"*
   (`RETOMAR.md`).
3. F1+F2 ya cierran el caso: no detectan *en el momento* —eso es imposible desde dentro— pero
   lo hacen **imposible de ignorar** la primera vez que se corre cualquier validador.

**Lo único que F3 aportaría:** detección **sin que estés**. Hoy si dejas de trabajar dos semanas
y el hook muere, no te enteras hasta que vuelvas.

> 🟡 **El error de método que la destapó:** al terminar F2 no dije que F3 quedaba descartada, ni
> la anoté. Brian tuvo que preguntar *"¿pero no teníamos F3?"*. **Una decisión que solo vive en
> la conversación muere con ella** — que es exactamente lo que este sistema existe para evitar.

---

## ✅ EL LATIDO — F1 y F2 CONSTRUIDAS (2026-07-31)

**F1 · `SessionStart`:** estampa `.heartbeat`; `check-health` avisa 🔴 a los ≥3 días.
**F2 · las 3 puertas:** cada una estampa `.beats/<nombre>` cuando dispara; 🔴 si una lleva
≥7 días muda respecto a la última sesión viva.

**Lo que decidió el diseño de F2 — la evidencia que la justificó:** el día que se construyó,
`gate-handoff` había bloqueado 3 lanzamientos (prueba de que dispara) y, tras decenas de
ediciones, **no había forma de saber si `gate-critical` había corrido una sola vez**.

**El coste, medido antes de elegir el diseño:** Write+Edit disparó **97 veces** en esa sesión.
Estampar en cada llamada = ~194 escrituras en el camino caliente. Por eso el latido **solo
escribe cuando cambia el día**: una por puerta por día, y una lectura sin escritura las otras
96 veces. Verificado en la batería: 5 llamadas seguidas, **cero escrituras**.

**La comparación es contra la última sesión, no contra hoy** — las puertas solo disparan cuando
trabajas, así que "callada mientras nadie estuvo" no es un fallo. El fallo es una puerta muda
en un día en que la sesión sí estuvo viva.

**⚠️ Lo que ninguna fase cubre:** si se borran el hook **y** su latido a la vez, esto no lo
distingue de una instalación nueva. Es sabotaje deliberado, no deriva — y contra eso ningún
guardia interno protege.

---

## 🟡 2 LISTAS FIJAS QUE NO URGEN — de la auditoría del 2026-07-31

Se auditaron **las 22 enumeraciones** de los validadores con un criterio: *¿esto se puede medir
en vez de listar?* Resultado: **19 están bien**, 1 era grave (ya arreglada: `GUARDS` vigilaba 9
de 21) y estas 2 quedan anotadas.

**① `LIMITS` está escrita DOS VECES** — en `bin/check-blocks:34` y `bin/check-health:241`.
Hoy son idénticas (verificado). Pero es exactamente lo que `expertise/doc-structure.md` llama
*"una tabla duplicada es un puntero esperando a divergir"*, con el precedente medido de la tabla
de decisiones que divergió **75 vs 37 filas**.
**Por qué no se arregla hoy:** no ha divergido en dos días de uso intenso. Refactorizar sin
evidencia de daño es trabajo sin retorno. **La señal para hacerlo:** la primera vez que difieran.

**② `check-structure:REQUIRED_DIRS` declara 7 carpetas; en disco hay 13.**
Faltan `memory/` `work/` `vision/` `bridges/` `Cerebro/` `Maestro/`. Consecuencia real: si se
borra `memory/` —donde vive `RETOMAR.md`— el validador de estructura **no lo nota**.
**Por qué no urge:** `check-health` sí vigila `RETOMAR.md` por otra vía. Es cobertura solapada,
no un hueco abierto.

> ⭐ **La regla que salió de la auditoría, y vale más que los dos arreglos:**
> una lista que enumera **lo PROTEGIDO** debe medirse; una que enumera **lo PERMITIDO** puede
> escribirse, siempre que lo desconocido **falle cerrado**.
>
> `SENSITIVE` enumeraba lo protegido y fallaba abriendo → mordió (expuso el token de GitHub).
> `READ_ONLY` de `gate-handoff` enumera lo permitido y falla cerrando → es segura por diseño.

---

## 📦 TRANSFER MODULES — anotado, NO construir hoy (2026-07-31)

**Qué es:** empaquetar un trabajo completo para entregarlo a un tercero, con reporte de redacción
de secretos. La referencia externa lo tiene en 14 archivos + `verify_tm.sh`.

**Por qué NO se construye ahora — decisión de Brian, con razón medida:** los Transfer Modules
resuelven *entregar trabajo a otra organización*. For3s OS hoy tiene **un solo dueño**, y los
puentes a otros Mente OS ya están resueltos por el gate (`bridges/Puentes_Mente_OS.md`).
Construirlo ahora sería **maquinaria antes de tener el problema** — el orden que el v2 existe
para evitar (*piloto antes que maquinaria*).

**Cuándo reabrirlo:** cuando haya un tercero real a quien entregar un bloque cerrado. La señal
concreta sería un cliente que pida el trabajo, no solo su resultado.

Contexto: `docs/analysis-internos-v1.md` · comparación medida del 2026-07-31 (sesión S8).

---

## 🔌 CONECTORES SELF-SERVICE + IDENTIDAD POR CORREO — ⭐ NUEVO PENDIENTE GRANDE (Brian 2026-07-20)

> **El problema:** toda integración de herramientas pasa por Brian (ineficiente, no escala) y el
> panel de la demo (`for3s.vercel.app/demo` → Conectores) es pura UI sin comunicación con el agente.
> **La visión completa:** `Alma/Vision_Conectores_SelfService_Panel_Agente.md` (capturada, con el
> terreno del sitio ya leído). **Hito GRANDE → se ejecuta PIEZA POR PIEZA (regla Brian
> 2026-07-20, visión §4): por cada pieza → alinear visión (Brian+yo) → plan DETALLADO de esa
> pieza → aprobar → construir → batería. NO un plan global. Brian marca cuándo y qué pieza.**

- [x] **A · Correo admin por instancia ✅ CONSTRUIDA (2026-07-20, 2ª pieza):** migr 047
  (`admin_email` en `owner`, aditiva) + OwnerStore (get/set/sync + norm) + siembra por ENV
  `FOR3S_ADMIN_EMAIL` + endpoint **`/v1/whoami`** (lo consume B) + `/soy` muestra el correo.
  Correos vivos: **Foresito=fruterito101** · **brian=brayan002150** · general=null (multi-tenant,
  pieza B). E2E verde en las 3 vivas, owner_id intacto. 3 bugs cazados (owner_id=0 falso · tipo
  sucio · compose equivocado). Tríada `b6aad52`. Plan: `Cuerpo/Plan_Pieza_A_Correo_Admin_Instancia.md`.
  ⏳ jazz/mashe: correos pendientes de Brian (su ENV vacío = admin_email null, inofensivo).
- [x] **B · General multi-tenant real ✅ CONSTRUIDA (2026-07-20, 3ª pieza):** ⭐ **LA DEMO WEB
  CONVERSA CON FOR3S POR 1ª VEZ** (el "usarlo" de la visión, que no existía). `/api/demo/general/chat`
  → canal del general (Funnel público) con X-Client-Id=**correo de la sesión** (no del body,
  fail-closed) → hilo aislado (AI1). Agente COMPARTIDO, cada correo su memoria. BYOK: al guardar la
  key se registra en `/v1/token` → responde con SU billing. ChatPanel (sección Chat, 1ª del shell).
  E2E: aislamiento PROBADO (A guarda dato, B no lo ve, A lo recuerda). Commit LOCAL sitio `8232e32`
  (SIN push, espera orden). Plan: `Cuerpo/Plan_Pieza_B_General_Multitenant.md`.
> 🔴 **AUDITORÍA INTEGRAL (2026-07-20):** el flujo completo encadenado destapó un BUG TRÁGICO de aislamiento (correos con puntos/+ colisionaban usuarios en el canal por _limpiar_id) → FIX  (hash estable), E2E verificado, sitio . Regla nueva: probar el flujo COMPLETO con datos reales (memoria feedback_probar_flujo_completo_encadenado).
- [🔨] **C · Conectores que SÍ conectan — FRENTE 1 ✅ + FRENTE 2 ✅ código (2026-07-20, 4ª pieza):** GitHub end-to-end. **F1 (server, tríada `3c3e35b`):** canal API con tool-loop POR USUARIO (token del vault, read-only, aislado) — resuelve S3. Endpoint `/v1/conector` (guarda/lee/borra cifrado) + `SecretStore.delete_secret`. E2E: ciclo + aislamiento verificados. **F2 (sitio, commit local `017871d`):** OAuth GitHub (start/callback state CSRF), token cifrado en vault por correo, `ConnectorsPanel` estado real (Conectar/Conectado/Desconectar). Verificado sin app (503/401/200). Plan: `Cuerpo/Plan_Pieza_C_Conectores_OAuth.md`. ⏳ **FALTA (Brian):** registrar GitHub OAuth App en fruterito101 + pegar credenciales (guía `marca-personal/Mente/Doc/GUIA_Registrar_GitHub_OAuth_App.md`) → luego C6 (conectar→chat usa el repo) E2E. Sitio SIN push (espera orden).
  (Visión C: botón→OAuth proveedor→credencial cifrada por usuario→el agente la usa→panel estado
  real. OAuth de proveedores=legal; OAuth de suscripción Claude sigue PROHIBIDO — la vía es que el
  usuario pegue su API key, ya construido.)
- [x] **D · API keys de For3s self-service ✅ CONSTRUIDA (2026-07-20, 5ª y ÚLTIMA):** endpoint `/v1/miskeys` (canal, tríada `cbf5d37`) — genera/lista/revoca, tope 3, aislamiento de propiedad por prefijo `::key-`, colisión de nombres resuelta, key plana 1 vez. Reusa `api_admin`. Sitio (`9f00442`, pusheado): `ApiKeysPanel` "Mis API keys" (generar con nombre/copiar/revocar). E2E: tope, B no toca las de A (403), la key CONSUME For3s, sin regresión. Plan: `Cuerpo/Plan_Pieza_D_API_Keys_Self_Service.md`.
> ✅✅ **PENDIENTE CONECTORES SELF-SERVICE COMPLETO (5/5 piezas): E · A · B · C(código, falta OAuth App) · D.**

- [x] **E · UN solo concentrado admin + responsivo ✅ CONSTRUIDO (2026-07-20, 1ª pieza):**
  `/demo-admin` absorbido como pestaña "Demo" en `/for3s-admin` (una sola llave = token de control,
  validado server-side con caché 60s) + tabs con scroll horizontal + header apilado en móvil.
  `/demo-admin`, `/api/demo/admin/auth`, `AdminDashboard.tsx`, `checkAdminPassword` eliminados.
  Build+lint verdes, 401 fail-closed, sin regresión. 3 bugs propios cazados. Plan+resultado:
  `marca-personal/Mente/Doc/Plan_Pieza_E_Concentrado_Admin.md`. **✅ PUSHEADO** (sitio
  `ElBrAyAn1967/For3s` main `d585144`). **✅ E2E completo:** caso positivo verificado (200 + tabla
  real de personas). El bloqueo de infra se resolvió: el Postgres demo NO escuchaba en tailnet
  porque arrancó antes que `tailscale0` en boot → `systemctl restart postgresql@16-main` lo fijó.
  ⚠️ **Deuda de mantenimiento del server (no urgente):** el bind se pierde si el server reinicia;
  fix duradero = `After=tailscaled` en el unit de PG o esperar la IP en ExecStartPre.
- **La experiencia (Brian):** *"1. registro nombre y correo · 2. conectar herramientas ·
  3. usarlo — todo del lado usuario"* — incluido QUITAR conectores (revoca y el agente lo suelta).
- Reusar: cifrado AES-256-GCM de la demo · canal API · puerta H8 · molde For3s Inside · vault ·
  panel /for3s-admin · Maestro (rama Mente OS por persona).
- Preguntas abiertas en la visión §3 (correo brian, dónde viven los tokens, OAuth apps de For3s,
  contenedores demo vacíos vs instancias reales, orden de conectores).

> **Qué es:** lista única y consolidada de todo lo que está PENDIENTE, por prioridad.
> Para que nada se pierda y se vea de un vistazo qué falta. Punteado desde RETOMAR.md.
> **Actualizar** al cerrar/abrir pendientes. Marcar ✅ cuando se cierre (no borrar — deja rastro).

**Última actualización:** 2026-07-13 (añadida §POST-INCUBATHON: 5 frentes de campo + bug del equipo).

---

## 🌐 SUPER-CEREBRO CONECTADO (Brian 2026-07-17) — ⭐ EL PENDIENTE ESTRATÉGICO MÁS GRANDE

> **Origen:** la información está demasiado centralizada (server for3s + `~/for3s`) y nadie más puede
> ponerse a la par. **Visión completa:** `Alma/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md`.
> Son DOS pendientes distintos. **Solo VISIÓN capturada — NO diseñar/construir hasta que Brian diga
> (arranca con Ronda F0, es un hito grande).**

### 🅰️ Entrenar a @For3s_OS_bot (Foresito) con TODO lo que llevamos
- [ ] **Foresito, el agente INTERNO de la empresa, NO está entrenado con lo que existe** (`~/for3s`:
  Mente OS, código, decisiones, historia + el server + más). brian sí tiene memoria potente (~22K
  episodios); Foresito, que debería "saberlo todo" de la empresa, es el que menos sabe. Reusa el arte
  del hito ENTRENAMIENTO (absorber memoria sin perderla, ya probado en brian). Cruza con 🅱️ (el
  Maestro sería la fuente que Foresito lee).

### 🅱️ MENTE OS MAESTRO — la super-memoria conectada → ✅✅ COMPLETO F1→F5 (2026-07-17). Evoluciona a CARRIL.
> **Motor entero construido y verificado E2E + primer piloto real (Jazz) funcionando.**
> Detalle: `Cuerpo/Ronda_Mente_OS_Maestro.md` · memoria `project_mente_os_maestro_f1_f2`.
> Repo `for3slabs/mente-os-maestro` (privado). **Ya no es visión: es un sistema vivo.**
- [x] **El controlador LIGERO que APUNTA (no replica) — regla madre "no replicamos, conectamos".**
  - [x] **F1 registro** — `Maestro/registro.md` apunta a 6 ramas (For3s OS, marca-personal, Foresito, instancias, NavigoX-gate, Diseño Jazz). Sin copiar nada.
  - [x] **F2 puentes** — comando `maestro`: A (git efímero `leer`/`grep`, no deja clones) + B (canal API vivo `vivo`, pregunta al agente). Rama madre versionada (`mente-os-for3s`, 166 docs, secretos excluidos).
  - [x] **Bienvenida** — `BIENVENIDA.md`: la IA que clona LEE CLAUDE.md/.claude/.agents + PREGUNTA (rama existente o nueva) + exige DESCRIPCIÓN (por qué ocupa Mente OS + qué hará). Fail-closed.
  - [x] **F3 crear rama** — `mente-os-nueva`: genera {Alma,Cerebro,Cuerpo,Doc}+RETOMAR desde plantilla orientadora, descripción obligatoria, ficha para el registro.
  - [x] **F4 permisos** — `Maestro/permisos.md` + puerta en `maestro`: por persona/carril, fail-closed, reusa H8. Colaborador ve SOLO su carril.
  - [x] **F5 piloto Jazz** — rama REAL `mente-os-diseno-jazz` (privado) creada, registrada, con permiso. E2E: Jazz ve su rama, NO ve el núcleo; brian ve todo.
- [x] **Puentes C+D ✅ CONSTRUIDOS (2026-07-19/20)** — búsqueda semántica + grafo de Mente OS sobre
  UN núcleo anti-duplicación (`Cuerpo/Ronda_Maestro_Puentes_C_D.md`). Índice en Foresito
  (`/v1/maestro/*`), CLI `maestro indexar|subir|buscar --contexto|grafo`. Barrido sistémico S1-S3:
  S1 skills amputadas [:1500] → fix 8000 propagado a las 3 vivas · S2 huele_a_maestro · S3 abierto.
- **Carril de mejora continua** (dormido): sumar más ramas · Jazz clona y usa en vivo · S3 (canal
  API con tools) si Brian decide.

### 📌 PENDIENTES DE BRIAN (él los hace — registrados 2026-07-20, cierre puentes C+D)
- [ ] **Smoke por Telegram a @For3s_OS_bot:** decirle *"busca en el maestro dónde se explica cómo
  dar permisos a una rama"* — debe EJECUTAR la búsqueda (tool-loop + /v1/maestro/buscar) y citar
  `rama:ruta`, no narrarla. Es el último eslabón E2E conversacional de los puentes C+D.
- [ ] **Probar en @For3s_Brian_bot una skill del entrenamiento** (tick-coord, monad, godinez…):
  primera vez que las ve COMPLETAS (S1 las amputaba al 19% desde el día uno). Comparar calidad.
- [ ] **Decidir S3** (canal API sin tools → el modelo NARRA e inventa ejecuciones; afecta la promesa
  del canal para clientes API como NavigoX): ¿darle tool-loop al canal API o documentar el límite?

## 🎯 POST-INCUBATHON — Frentes de campo (Brian 2026-07-13, tras ganar 2º lugar) ⭐ NUEVO

> **Origen:** experiencia REAL de mercado + sentimientos genuinos de Brian como programador tras
> ganar 2º lugar de 200. Doc madre: `Alma/Aprendizajes_De_Campo_Post_Incubathon.md`. Atacar uno
> por uno (nada de golpe). Orden tentativo: A → D → B → (C+E). El bug del equipo (abajo) es concreto
> y ya tiene fix en diseño.

### ✅ FRENTE A — Consumo de tokens — ANALIZADO A FONDO 2026-07-13 (forense mensaje-por-mensaje)
- **CONFIRMADO con evidencia del jsonl** (sesión `2a5131d3`, 278MB, 53,907 líneas, viva desde el
  28-MAYO sin /clear = 47 días): el contexto vivo llegó a **~980K tokens** (ventana [1m] → nunca
  compactó). El **TTL del caché de Anthropic era 5 minutos** → cualquier pausa >5 min re-escribía
  TODO el contexto (~1M tokens) a precio premium de cache-write.
- **El jueves 9-jul hubo 5 cache-misses de ~935-980K c/u en opus-4-8** (03:10 · 04:43 · 18:01 ·
  19:37 · 19:51) = 5.1M tokens cache-write + 13M cache-read en ~15 mensajes reales (>$100-200
  equivalente API en 1 día). **Los 3 fatales de la tarde:** "hola" (970K) → "define for3s" (975K)
  → "oye estoy ocupando el bot" (980K + error = cupo agotado). Literalmente "hola" costó ~1M tokens.
- **Hipótesis DESCARTADAS con evidencia:** NO proceso de fondo al cerrar, NO entrenamiento nocturno
  (cero requests en los huecos idle 04:43→18:01). El /model a fable-5 fue DESPUÉS de agotarse.
- **Solución LOCKED y ACTIVA:** /clear al cerrar cada bloque (moderado por Claude, no por Brian) +
  vigilar tamaño de sesión (sana <15MB) + actualizar RETOMAR.md antes de cada /clear. Con contexto
  chico (~20-30K), un cache-miss cuesta centavos en vez de ~1M tokens. El /clear del 13-jul ya mató
  a la sesión monstruo. Memoria: `feedback_moderar_consumo_sesion`.

### 🔵 FRENTE D — Valor de retorno (el MADRE) → 🟢 HITO H13 "DEVUELVE" EN CONSTRUCCIÓN (F1 ✅)
- Sentimiento de Brian: *"For3s es un chat que contesta y guarda memoria solamente."* ✅ Rebotado:
  no es que valga poco, es que lo usó como TUBO y **nunca lo vio DEVOLVER valor**.
- **Ronda aprobada 2026-07-13** (`Cuerpo/Ronda_H13_Devuelve_Valor_Retorno.md`). LOCKED: digest+
  contextual · estreno solo `brian` · extender DMN (clase VALOR) · máx 1-2 proactivos/día.
- **F1 ✅ motor de insights (commit `17dbd01` firmado, server):** migración 036 (valor_on OFF default
  + tabla insights) + insights.py (mina por sesión, anti-alucinación: seqs validados contra BD,
  silencio antes que relleno) + task insight_mining (sonnet, throttle 6h) + /dmn valor on|off + 10
  tests. **Probado E2E en brian:** 3 insights REALES de la memoria entrenada (cabos sueltos, conf
  0.75-0.88), 0 seqs alucinados, batería §5-BIS 1115 OK/0 FAIL. 🐛 **2 bugs latentes cazados:**
  set_clase/correr_ciclo con `else` ciego (clase desconocida caía en generativas) → cerrados.
- **F2 ✅ digest diario proactivo (commit `15fc29d` firmado, server):** migración 037 (proactivo +
  via) + armar_digest/para_digest (blindaje multi-usuario: jamás insights de miembros al dueño) +
  job_digest_valor (cron 08:00 Mx, gates fail-closed, silencio antes que relleno) + /proactivo
  on|off + audit. **E2E real: digest ENTREGADO por Telegram a Brian.** 🐛 BUG pre-existente cazado
  (2 capas): alertas PR2 del worker MUDAS en instancias de plantilla (_alertar_dueno sin fallback
  ENV + composes sin TELEGRAM_BOT_TOKEN en worker) → arreglado, repara jazz/mashe/general también.
- **F3 ✅ "por cierto" contextual (commit `90a6256` firmado, server):** migración 038 (embedding
  en insights) + por_cierto() (barato→caro, gates fail-closed, umbral 0.55 con margen medido) +
  inyección defensiva en conversation.py. ⭐ Refactor: `_SQL_PERTENENCIA` punto único del blindaje
  BUG-14 (digest+contextual). E2E completo ✓. **Prueba en vivo pendiente:** insight #5 (backup
  offsite) quedó `nuevo` — Brian escribe del backup al bot y debe mencionarlo.
- **F3 verificada EN VIVO** (turno real de Brian: sim=0.70 desde el tema incubathon, respuesta
  tejió insight+memoria, cero errores). **F4 ✅ feedback (commit `33ee9bc` firmado, server):**
  botones ✅/❌ en digest y /insights, marcar_feedback con pertenencia punto único (ajeno
  rechazado E2E), Insight.via, stats de utilidad = semilla del modelito. ty devuelto a línea
  base (3 diagnósticos nuevos míos cazados y arreglados).
- **⏳ Sigue: F5 cierre del hito** — batería §5-BIS final + version bump (v0.16.0) + CHANGELOG +
  Bitácora + decisión de Brian sobre propagación a otras instancias. Carril "urgente" diferido
  (anotar en deuda si no entra en F5).
- 🐞 Deuda menor anotada (pre-existente, NO de F1): 9 archivos no pasan `ruff format --check`
  (entrenamiento_*, api_channel, specialists, telegram_channel ~2736).

### 🟠 FRENTE B — El puente / capa API NO está listo para mercado
Preguntas SIN definir que salieron del campo (base construida: canal API caja negra):
- **¿Un solo puente o uno por cliente?** ¿Todos comparten el mismo o cada quien el suyo?
- **¿Cuánto tráfico soporta? ¿Para cuántos usuarios?** Consumo varía por industria.
- **Inestabilidad:** el puente se cae seguido (túnel Cloudflare quick = frágil, ya verificado).
- **Panel de administración (web app segura):** Brian como DUEÑO no puede ver quién consume, ni
  activar/denegar accesos. Falta un panel de control.
- **Pendiente:** diseño de arquitectura de mercado del puente + panel admin.

### 🟡 FRENTE C — Multi-canal → 🔄 CARRIL VIVO DORMIDO (Brian 2026-07-16)
> **Brian 2026-07-16:** *"multi-canal es un poco complicado, tenemos que hacer integraciones algo
> pesadas... hay que sentarlos."* → evolucionado a CARRIL (dinámica de sumar UN canal por vuelta,
> no de golpe). **MD:** `work/Carril_Multicanal.md` (los 5 pasos + reactivación + semillas).
Usarlo solo como capa de API lo limitó. La gente pedía (semillas del carril):
- Contestar en **grupos de WhatsApp** (⭐ el más pedido; informes especiales).
- Mandar **correos electrónicos**; flujos correo + redes sociales.
- Analizar **qué clientes recurren más a un comercio** (capacidad analítica, cruza con For3s Trace).
- Diseño a detalle ya registrado en §BRECHAS OPENCLAW (OC-C1..C7) / §BRECHAS HERMES (HG-1..3).
  El carril decide CUÁNDO y CUÁL canal. Dormido hasta que Brian lo despierte.

### 🟣 FRENTE E — Confianza para delegar/entregar → 🔄 CARRIL VIVO DORMIDO (vuelta 1 ✅, v0.18.0)
> **Brian 2026-07-16:** *"me gustó la dinámica, NO lo cierro como terminado — es repetitivo, lo
> iremos mejorando. Lo cierro COMO PENDIENTE y evolucionamos el pendiente a un CARRIL repetible."*
> **→ Estructura del ciclo para repetirlo más adelante: `work/Carril_Mejora_Continua_Confianza.md`.**
> Se despierta cuando Brian lo sienta (típ. un piloto vivo destapa algo, o quiere soltar un peldaño
> más). NO ejecutar solo. La vuelta 1 (escalera F1-F6+A) quedó completa; Brian la va a probar en uso real.
- Vuelta 1: elegido por Brian 2026-07-15. Escalera de confianza. Ronda:
  `Cuerpo/Ronda_FrenteE_Confianza_Para_Delegar.md`. Memoria: `project_frente_e_confianza_delegar`.
- **F1 ✅ EXPEDIENTE** (73583a0) · **F2 ✅ CARRIL /mision** (7842c8e) · **F3 ✅ AUDITORÍA SEGURIDAD**
  (d3e71ef: veredicto NO hay error crítico-legal; `docs/analysis/Auditoria_Seguridad_For3s_OS.md`) ·
  **F4 ✅ PILOTO jazz** (c51a267; `memory/archive/Piloto_Tester_Jazz_F4.md`).
- **⏳ Abiertos del frente:**
  - [~] 🐌 **`/mision` tarda ~4min → ATACADO 2026-07-16 (commits `5de8ec4` + `edf59fd`).** Medido:
    el **99% es el LLM** (2+ llamadas EN SERIE; sandbox 0.1s, esperas 0.5s) → NO hay ineficiencia
    técnica, la misión ES trabajo pesado. Aplicado: (1) **progreso EN VIVO** (hook `on_vuelta` →
    mensaje editable con fase+tiempo). (2) **Benchmark de modelos** (pedido de Brian): Haiku 202s
    (el más lento, más vueltas) · Sonnet 49s pero FALLABA · Opus 101s 5/5. **Brian eligió Opus solo
    en /mision** (proxy `_AgenteBYOK`, no contamina el canal). (3) **🐛 BUG-E3 arreglado:**
    `stop=max_tokens` devolvía respuesta VACÍA silenciosa → ahora avisa; + max_tokens 4096→8192.
  - [ ] ⭐ **F-A2 (mejora futura, mayor — idea de Brian): partir misiones complejas al EQUIPO
    multi-agente.** Hoy el carril hace las llamadas al LLM en SERIE. El equipo (`correr_equipo`,
    H8) ya paraleliza con `asyncio.gather` y ya reporta progreso (`on_progreso`) → routear
    misión→equipo bajaría el tiempo de PARED real (no solo la percepción). Cambio de motor:
    routing + síntesis por secciones. No urgente (el progreso en vivo ya alivió la queja).
  - [ ] 🎨 **`/salud` en instancia recién encendida muestra 🔴** ("no hay turnos", "no hay backups")
    = estado natural de instancia virgen, pero un tester lo lee como "roto". Distinguir vacío-nuevo
    de fallo-real.
  - [ ] Jazz da /start + usa el bot varios días + feedback (peldaño 3 en vivo).
  - [~] **F5 piloto cliente real → HECHO por SIMULACIÓN 2026-07-16** (`memory/archive/Piloto_Cliente_Real_F5.md`).
    NavigoX registrado pero no consume activamente → simulé el recorrido de cliente por la URL
    pública (14 pruebas). Aislamiento entre clientes SÓLIDO por la puerta real, errores limpios,
    memoria entre turnos, cuota diaria frena. **2 hallazgos anotados:** (a) rate por-minuto casi
    inalcanzable con llamadas reales (la defensa es la cuota diaria; para abuso concurrente
    convendría límite de concurrencia por cliente, futuro) · (b) `/olvidar {"tema":"%"}` borra
    todo lo del cliente en vez de devolver 400 (tema inválido debería rechazarse). ⏳ Falta piloto
    VIVO: que NavigoX retome consumo (acción de Brian, gente externa).
  - [ ] **F6 cierre** — re-preguntar el sentimiento a Brian ("¿ya lo soltarías?"). La métrica ES él.
  - [ ] Propagar F1-F4 a las otras instancias (hoy en general+jazz; brian/mashe/Foresito no).

### 🔴 BUG-EQUIPO — El equipo multi-agente NO hereda la identidad de For3s (VERIFICADO en código)
- **Cazado** auditando la conversación del domingo (RNN/LSTM): los 5 specialists dijeron *"for3s OS
  no está definido"* e imaginaron un kernel. Se lanzan EN FRÍO.
- **Evidencia:** `specialists.py:252` `prompt = f"[{rol}]\n\n{entrada}"` — sin identidad ni memoria;
  `specialists.py` no importa `identidad`; el sintetizador tampoco. Cadena: `telegram_channel.py:1442
  correr_equipo(texto)` → `multiagente.py:206 correr_specialist(rol, tarea)` → prompt sin contexto.
- **Impacto:** respuestas genéricas/descontextualizadas cuando la tarea es sobre el propio For3s;
  desperdicia tokens. Detalle: `docs/analysis/Analisis_Conversacion_Domingo_RNN_LSTM.md`.
- **FIX DISEÑADO (F0 listo, espera aprobación de Brian):** `Cuerpo/Diseno_Fix_Equipo_Sin_Identidad.md`.
  Resumen: inyectar una "cápsula de contexto" ligera (~150 tokens, NO la identidad completa de ~3.7K)
  a cada specialist. Cambio de 1 función + 1 línea. Costo +~750 tokens/corrida. Reversible. La
  memoria del equipo (que reciban contexto de la memoria de For3s) queda como fase FUTURA separada.

### 🔵 LÍNEA FUTURA — Modelo que aprende qué memoria es valiosa (NO construir hoy)
- Brian: *"SÍ me importa — un modelo que aprenda de tus datos qué episodios resultan valiosos."*
- **NO es un LSTM.** Mini-clasificador sobre features del episodio (frecuencia, recencia, si se
  reusó, feedback del usuario, centralidad en el grafo). Mejora el scoring de memoria (hoy son reglas).
- **Requisito:** miles de episodios reales con señal de "valioso". Hoy sería sobre-ingeniería.
- **Cuándo:** con volumen real de uso. Encaja con Frente D (mejor scoring = más valor devuelto).

### ✅ RUIDO ACLARADO — deep learning / RNN / LSTM NO aplica
- Obsoleto desde Transformers (2017). For3s ya usa DL donde importa (embeddings BGE-M3). El "proceso
  neuronal" es metáfora de la heurística (microglía/CLS/grafo) — y está bien que NO sea red neuronal
  (reglas+grafo son auditables/encriptables, lo que las empresas quieren). No perseguirlo.

---

## 🔴🌐 DESCUBRIBILIDAD (SEO / AEO / GEO) → 🔄 CARRIL VIVO DORMIDO + parte CERRADA (Brian 2026-07-16)

> **Brian 2026-07-16:** *"generar stars, awesome-lists, GitHub Sponsors y grabar el GIF/vídeo demo:
> DÉJALOS COMO COMPLETADOS — van a tardar demasiado en retomarse. Landing + SEO + AEO + analítica:
> eso va a un CARRIL de mejora continua."* → dividido en:
> - ✅ **CERRADOS (retirados, no se retoman):** generar stars · awesome-lists · GitHub Sponsors · GIF demo.
> - 🔄 **CARRIL "Presencia/Descubribilidad"** (landing + SEO + AEO + analítica): dinámica repetible,
>   dormido hasta que Brian lo despierte. **MD:** `work/Carril_Presencia_Descubribilidad.md`.
>
> **(histórico)** Brian (2026-07-04, CRÍTICO): "no tenemos NADA de SEO... también en GitHub no aparece
> el repositorio... es MUY importante darnos a conocer." De nada sirve el mejor agente si NADIE lo encuentra.

**Las 3 capas de descubribilidad hoy (el marco SEO→AEO→GEO):**
- **SEO** (aparecer en Google) — rankear en la página 1.
- **AEO** (Answer Engine Optimization) — estar en el "AI Overview" / answer box de Google.
- **GEO** (Generative Engine Optimization) — que ChatGPT/Claude/Perplexity te RECOMIENDEN cuando alguien
  pregunta "¿qué agente self-hosted uso?". Esta es la nueva batalla y For3s no está en ninguna.

**🔍 DIAGNÓSTICO REAL (verificado 2026-07-04):**
- **GitHub `fruterito101/for3s`:** SÍ tiene description + 14 topics (ai-agents, self-hosted, claude,
  knowledge-graph, rag…) + homepage. PERO solo **3 stars** → GitHub NO lo muestra en búsquedas/topics
  con pocas stars + repo <90 días (Maintained bajo). "No aparece" = falta señal social (stars/tráfico),
  no metadata. Además: sin GitHub Pages, sin releases visibles en la portada.
- **⚠️ HALLAZGO GRAVE:** `for3s.vercel.app` (el homepage del repo) es la web de **"For3s QA"
  (marca-personal)**, NO de For3s OS el AGENTE. Un visitante que llega del repo NO encuentra el producto.
  Y esa web NO tiene: meta description, schema.org (JSON-LD Product/SoftwareApplication/FAQ), sitemap.xml,
  robots.txt, blog/docs. **Cero SEO/AEO/GEO estructurado.**

**PENDIENTES CONCRETOS — repartidos (Brian 2026-07-16):**
- [→🔄] **Decidir la landing de For3s OS** → al **carril Presencia** (`work/Carril_Presencia_Descubribilidad.md`).
- [→🔄] **SEO base** (title/meta/keywords, sitemap, robots, Open Graph) → al carril Presencia.
- [→🔄] **AEO** (FAQ real + schema.org FAQPage + SoftwareApplication) → al carril Presencia.
- [~] **GEO base HECHA 2026-07-04** — comparativa For3s vs Hermes (schema Article+FAQPage) + README rico +
      PR a awesome-ai-agents. (Lo que faltaba —más posts/awesome-lists— quedó CERRADO abajo.)
- [→🔄] **Analítica** (de dónde llega la gente; ya hay Microsoft Clarity en marca-personal) → al carril Presencia.

**✅ CERRADOS por Brian 2026-07-16 (retirados, NO se retoman — "tardan demasiado"):**
- [x] ⭐ **Generar stars** — CERRADO (se dará solo con el uso/charlas; no es tarea que persigamos).
- [x] **awesome-lists** — CERRADO (el PR a awesome-ai-agents quedó abierto; no perseguimos más listas).
- [x] **GitHub Sponsors** — CERRADO (requiere config de pagos de Brian; fuera de foco).
- [x] **Grabar el GIF/vídeo de demo del README** — CERRADO (no se retoma por ahora).

### 🐙 GITHUB — por qué NO nos posicionamos (análisis vs la doc OFICIAL de GitHub, 2026-07-04)

> **Brian (URGENTE):** "en GitHub no aparece el repositorio aunque sea público. Los programadores tienen
> que conocerlo." Leí la doc oficial de GitHub (topics, búsqueda, README, perfiles) y la crucé con el repo.

**🔑 VERDAD DE FONDO (confirmada por la doc):** GitHub **NO documenta su algoritmo de ranking** (secreto),
PERO de lo que sí publica + cómo funciona el sort "best match": **GitHub posiciona por SEÑAL SOCIAL
(stars/forks/tráfico/actividad/edad), NO por metadata.** Nuestra metadata está BIEN; nuestra señal social
es casi CERO. "No aparece" = falta popularidad, no falta configuración.

**🔍 AUDITORÍA del repo `fruterito101/for3s` (verificado 2026-07-04):**
| Elemento | Estado | Veredicto |
|---|---|---|
| Description | ✅ buena | OK |
| Topics | ✅ 14/20 (ai-agents, self-hosted, claude…) | OK (límite doc: 20, lowercase, ≤50 chars) |
| README con badges/imágenes | ✅ 6 elementos | OK |
| Social preview (Open Graph) | ✅ existe | OK |
| License | ✅ AGPL-3.0 | OK |
| Releases | ✅ 1 (v0.14.0) — falta v0.15.0 | actualizar |
| **⭐ STARS** | 🔴 **3** | **EL problema #1** |
| Forks / Watchers | 🔴 0 / 0 | señal social nula |
| Homepage | 🔴 apunta a for3s.vercel.app = web de **QA, NO del agente** | MAL |
| GitHub Pages | ❌ No | oportunidad perdida (sitio + Google) |
| Discussions / Wiki | ❌ No | menos "comunidad viva" (señal que GitHub valora) |
| Perfil README (`fruterito101/fruterito101`) | 🔴 404 | la doc: "aparece auto en tu perfil" — no existe |
| Cuenta | ⚠️ Usuario personal (2 followers) | poca autoridad (no es org) |
| Edad | ⚠️ creado 2026-06-27 (<90 días) | GitHub/Scorecard penaliza repos nuevos |

**Las 4 razones REALES de por qué no aparece:**
1. **Pocas stars → invisible en "best match"** (el sort por defecto pondera popularidad). 3 stars = debajo
   de miles. Nadie ordena por "más nuevo".
2. **Repo nuevo + cuenta personal 2 followers** = poca autoridad, sin red que amplifique.
3. **Homepage al lugar equivocado** (web de QA, no del agente) → pierde al visitante que sí llega.
4. **Cero puertas de entrada** fuera del repo (sin perfil README, sin awesome-lists, sin Discussions, sin Pages).

**✅ PLAN GITHUB (orden de impacto, lo que la doc dice que SÍ mueve la aguja) — PENDIENTES:**
- [x] ✅ **⭐ GENERAR STARS — CERRADO por Brian 2026-07-16** (retirado: se dará solo con uso/charlas; no es
      tarea a perseguir). Compartir en comunidades (Frutero, X, Reddit r/selfhosted, HN, Discords) queda como
      algo orgánico, no un pendiente activo.
- [x] ✅ **Perfil README** `fruterito101/fruterito101` CREADO 2026-07-04 (público, en INGLÉS, enfocado en
      For3s OS + badges + link + "why not a chatbot"). Aparece auto en el perfil.
- [~] **Homepage del repo** — Brian decidió DEJARLO en for3s.vercel.app pero **MODIFICAR ESA WEB** para el
      agente (en inglés) → ver §WEB abajo (⚠️ es marca-personal, otro proyecto: confirmar alcance).
- [x] ✅ **GitHub Pages ON** 2026-07-04 → **https://fruterito101.github.io/for3s/** (landing técnica en
      INGLÉS con SEO completo: meta/keywords/Open Graph/schema.org SoftwareApplication+FAQPage). Sirve
      desde `docs/index.html`. Responde HTTP 200. Google la indexará (superficie SEO extra). Commit 23dacb0.
- [x] ✅ **Discussions ON** 2026-07-04 (has_discussions=true) — comunidad + soporte público.
- [~] **awesome-lists** — ⏳ **PR ABIERTO 2026-07-04:** `e2b-dev/awesome-ai-agents#1200` (Add For3s OS,
      mergeable, formato correcto + orden alfabético). Esperando review del mantenedor. Las demás listas
      (awesome-selfhosted, etc.) DIFERIDAS: son estrictas con proyectos nuevos/pocas stars → postular cuando
      For3s tenga más tracción (tras la charla). Material en `memory/archive/Descubribilidad_Material_Listo.md`.
- [x] ✅ **Release v0.15.0 "Identidad Viva"** PUBLICADO 2026-07-04 (tag firmado GPG + notas en inglés +
      SBOM/Sigstore). Releases visibles: v0.15.0, v0.14.0.
- [x] ✅ **README top-tier** 2026-07-04 (commit 00ebe80): tagline en INGLÉS + "Why For3s?" (diferenciador) +
      placeholder de demo. ⏳ FALTA (Brian): grabar el GIF/vídeo de demo y meterlo.
- [x] ✅ **🌐 WEB DEL AGENTE — HECHA 2026-07-04.** Ruta `/for3s-os` EN VIVO en `for3s.vercel.app/for3s-os`
      (SSR, inglés, modo oscuro). SEO (metadata/canonical/OG) + AEO (schema SoftwareApplication + FAQPage) +
      GEO (comparativa vs Hermes) + sitemap + link en navbar. Resuelve el hueco #1: el agente antes estaba en
      modo oscuro client-side que Google NO veía; ahora es página server-side indexable. NO tocó la home de QA
      (aditivo). 5 fases F1-F5 verificadas. Plan: `memory/archive/Plan_Web_for3s_Agente_SEO.md`. FALTA: que Google indexe
      (tiempo) + señal (charla). Opcional: migrar a for3s.com/.ai cuando se compre.
- [x] ✅ **ORG PROPIA `for3slabs` CREADA + repo transferido 2026-07-04.** El repo oficial es ahora
      **`github.com/for3slabs/for3s`** (era fruterito101/for3s; GitHub redirige la URL vieja 301). Todo
      re-apuntado: README badges/links + landing Pages (`for3slabs.github.io/for3s`) + perfil README +
      remote del server. Todo conservado (topics, discussions, pages, release). Commits 607a115 firmado.
      ⚠️ **NUEVA URL OFICIAL: for3slabs/for3s** — actualizar en memoria [[project_repo_oficial_for3s]].
- [x] ✅ **GitHub Sponsors — CERRADO por Brian 2026-07-16** (retirado, fuera de foco). Requería config de
      pagos (Stripe) — acción manual de Brian; si algún día lo quiere, github.com/sponsors → onboarding.
- [x] ✅ **Discussions con post de bienvenida** 2026-07-04 — categorías (Announcements/Q&A/Ideas/Show&tell) +
      post "Welcome to For3s OS 🦊" en inglés (discussions/7). Cuando llegue gente ve comunidad viva, no desierto.

⚠️ **Cruza con:** DIST-1 (plan de lanzamiento), DIST-3 (dominio install.for3s.dev + landing), la charla
VALIDACION_WEB3 (una charla = tráfico + stars). **Prioridad: (1) landing del AGENTE + (2) generar stars
(charla). Sin señal social, GitHub no nos muestra por más metadata que tengamos.**
Memoria: [[project_repo_oficial_for3s]]. Análisis completo: `docs/analysis/Analisis_GitHub_Descubribilidad_2026-07-04.md`.

---

## 🎤 VALIDACION_WEB3 — Charla/Taller "Dale un trabajo a tu agente" — ✅ CERRADO (Brian 2026-07-14)

> ✅ **CERRADO POR ORDEN DE BRIAN (2026-07-14): "dalo como terminado — todo eso".** El bloque
> completo de la charla (batería pre-demo, guion, slides, plan B, instalador para asistentes)
> queda TERMINADO/retirado de pendientes. Rastro histórico abajo (no borrar). Doc de trabajo:
> `Cuerpo/Charla_Web3_Plan_Maestro.md`. El foco pasa a los Frentes post-Incubathon (B siguiente).
>
> **⏰ FECHA LÍMITE:** jueves de la semana del ~10-17 de julio 2026 (AI x Blockchain Day).
> **⏱️ DURACIÓN CONFIRMADA por Mel (2026-07-04): 25 minutos.** → charla + demo en vivo (NO taller hands-on largo).

**Qué es (Brian):** Brian dará una **charla / taller / presentación** en el evento **AI x Blockchain Day**,
en el track "**Dale un trabajo a tu agente**" (uno de los 4 talleres: Fundamentos de IA · Lanza tu propio
agente (Pi Coding Agent) · **Dale un trabajo a tu agente** ← elegido · Haz que tu agente cobre por su trabajo).
**Objetivo: DEMOSTRAR EN VIVO el valor de un agente TAN POTENTE como For3s OS.** Foresito es la prueba viva.

**Por qué encaja perfecto (el evento está hecho para For3s):** los paneles del mismo día son
"Identidad después de la explosión de bots 🤖" y "Cuando los agentes AI tienen wallets 💸" → For3s ya
responde a eso: es un AGENTE (no bot), con IDENTIDAD VIVA (v0.15, se adapta), memoria real, auto-conciencia,
ejecuta código, trabaja solo de noche. El mensaje: **"no es un chatbot con esteroides, es un agente que
recuerda, aprende, se cuida solo y hace trabajo real — self-hosted, tus datos, tu server".**

**Qué demostrar (el arsenal de For3s como valor real de "darle un trabajo a tu agente"):**
- 🧠 **Memoria real** — "¿en qué quedamos?" → retoma de verdad (no un LLM sin estado).
- 🎭 **Identidad viva (v0.15)** — "sé más breve" → se acopla al instante; "¿cómo te has adaptado a mí?" → transparencia.
- ⚡ **Ejecuta código real** — le pides un cálculo/script y lo CORRE en su sandbox (agente-desarrollador).
- 🐙 **GitHub real** — analiza un repo, cuenta PRs/issues exacto, crea un issue (con confirmación).
- 🤝 **Equipo multi-agente** — "analiza a fondo" → 5 specialists en paralelo + síntesis.
- 🌙 **Trabaja solo** — de noche se mantiene y se mejora (backup, consolida, olvida, sueña).
- 🪞 **Se conoce y se auto-modifica** — /soy, /cambios, /modificar (dentro de su caja).
- 🔒 **Confianza enterprise** — auditoría inmutable, KEK offline, CI de confianza (SBOM/Sigstore/Scorecard).

**Pendientes concretos para armarlo (cuando Brian lo diga):**
- [ ] ⭐🔴 **VERIFICAR FOR3S OS E2E ANTES DE LA CHARLA (Brian 2026-07-04) — que la demo NO falle en vivo.**
      Batería §5-BIS completa + probarlo EN TELEGRAM a fondo (no solo tests): memoria ("¿en qué quedamos?"
      retoma) · identidad viva ("sé más breve" → se acopla; "¿cómo te has adaptado a mí?") · **ejecuta
      código real** (un cálculo → corre en el sandbox) · **GitHub** (analiza repo / cuenta PRs / crea issue) ·
      /soy /salud (todo 🟢) · equipo multi-agente ("analiza a fondo") · velocidad (que no tarde de más con
      sonnet). Verificar CADA mensaje que irá en el guion de la demo, con el modelo que se usará en vivo.
      Objetivo: cero sorpresas el jueves. Cruza con el guion de la demo + el Plan B. **Correr esta batería
      1-2 días antes del evento** (For3s se auto-modifica de noche → re-verificar cerca de la fecha).
- [ ] Confirmar con Mel: día exacto, hora y **DURACIÓN** del slot (define cuánto contenido cabe). ✅ 25 min.
- [ ] Definir formato: ¿taller hands-on (la gente instala/prueba) o presentación + demo en vivo?
- [ ] Guion de la demo en vivo (secuencia de mensajes a Foresito que muestren el "wow" — reusar
      `memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md` como base de qué escribirle).
- [ ] Narrativa/slides: el porqué (agente vs bot, self-hosted, tus datos) + el arsenal + el cierre.
- [ ] ¿Instalador listo para que la gente lo pruebe? (cruza con DIST-2: probar `curl|sh` en Linux limpio).
- [ ] Plan B por si falla la red del evento (demo grabada / instancia local).

Memoria: [[project_hito_identidad_viva]] (la identidad viva es el highlight) ·
[[For3s_Bot_vs_Agente_vs_Hermes]] (el argumento agente vs bot) · Doc/PLAN_PRUEBAS_EXHAUSTIVO.md (guion base).

---

**Fase actual:** 🟢 **CERO bugs abiertos, nada crítico pendiente.** Cerrados los grandes bloques:
✅ MVP · H5-H12 · DMN · metacognición · APRENDE · PULIR H8 · PROFESIONALIZACIÓN (8/10) · intern-os
AI1-AI7 · 16 bugs + barrido F1-F5 · **REDISEÑO MEMORIA (F1-F5 + M1-M4, sin deuda)** · **AUTO-CONCIENCIA
(AC1-AC4 + guardián)**. Lo que QUEDA = crecimiento (3 bloques grandes con Ronda: ENTRENAMIENTO ·
PRODUCTO DISTRIBUIBLE · MULTI-INSTANCIA) + deuda no-urgente de hitos completos (H9 D1-8, H10 HP1-6) +
11 diferidos conscientes (§EXTRAS). version.py v0.13.0. Todo en producción + GitHub firmado.

---

## 📦 EXTRAS — pendientes CONCRETOS diferidos por decisión (Brian 2026-07-01)

> **Qué es:** apartado donde vamos dejando pendientes concretos y bien acotados que Brian decidió
> DIFERIR a propósito (normalmente sub-sistemas grandes que se retoman como su propio bloque, o
> mejoras puntuales que no urgen). NO son "olvidos" ni "deuda por hacer ya" — son decisiones de
> "esto sí, pero después". Se sacan de su bloque original y se centralizan aquí para tenerlos a la
> vista sin que ensucien los bloques activos.

- [⏸️] **BYOK · Credenciales por usuario (bring your own key) — diferido (era el área H de PULIR H8).**
  Cada PERSONA del equipo tiene su PROPIA API key de suscripción → su consumo va a SU cuenta, no a
  una sola. Lo que se COMPARTE es el BOT (interfaz + lógica + equipo); lo que NO se comparte es la
  key ni el gasto. Requiere: (1) guardar la key de cada miembro cifrada con KEK (una por persona);
  (2) pedirla cuando entra al equipo (¿al cruzar la puerta?); (3) usar la key correcta según QUIÉN
  habla en CADA llamada a Claude (incl. el equipo multi-agente — hoy usa 1 credencial fija del
  arranque); (4) medir cupo/consumo POR persona (habilita el A2 con cupo real de cada quien).
  Sub-sistema completo, cruza con la puerta (C) y la memoria por persona (D). Hoy la write de un
  miembro se ejecuta con el PAT del DUEÑO; con BYOK usará la del miembro. **Diferido por Brian
  (2026-06-24): es un sub-sistema grande, se retoma como su propio bloque/diseño. NO atacar hasta
  que Brian lo diga.** Diseñar a fondo (cómo se pide la key, seguridad, qué pasa si alguien no tiene).

- [⏸️] **PR5 · DATOS de producto/empresa — diferido (era de PROFESIONALIZACIÓN).** Retención,
  actividad comercial, qué funciona como producto. ⚠️ BLOQUEADO POR REALIDAD: hoy solo hay 2 usuarios
  (Brian + Sme G). Medir "retención/negocio" con 2 personas = inventar datos (over-engineering).
  Reactivar cuando haya más usuarios/testers reales. La infra base ya existe (PR3 /datos mide
  actividad/tokens/personas). NO es deuda por hacer, es esperar a tener con qué.

- [⏸️] **HA-3 · H7 enrutamiento automático (Tálamo/Dual-Process) — diferido (era de PROFESIONALIZACIÓN).**
  Solo existe `/model` manual (✅ funciona, 3 modelos: Haiku/Sonnet/Opus). El enrutamiento
  Haiku-barato/Opus-caro según complejidad está a medias — el propio `modelos.py` dice "se construye
  después". Decisión consciente: su beneficio (ahorro de costo) NO aplica a la suscripción plana; se
  retoma con API de pago/clientes. Registrado para no olvidar que H7 está a medias.

- [⏸️] **PR8 · SISTEMA DE ENTRENAMIENTO / migrar otros agentes — diferido (era de PROFESIONALIZACIÓN).**
  Importar la memoria de los 6 agentes propios a Foresito. ⛔ Regla de Brian: "NO empezar hasta pulir
  TODO". Es un bloque grande completo (= todo el bloque §ENTRENAMIENTO E1-E4). Se retoma como bloque
  propio cuando Brian lo diga. Cruza con la migración de Foresito (mismo arte: mover memoria sin
  perder) y con REDISEÑO MEMORIA.

- [⏸️] **PR9 · UX / dividir telegram_channel — diferido (era de PROFESIONALIZACIÓN).** "Se siente MVP,
  no producto": organización + comportamiento + UX. ✅ PR9.0 (sincronización del repo de la verdad)
  YA hecho 2026-06-30. Lo que QUEDA: (1) **dividir `telegram_channel.py` (~3350 L)** en módulos por
  extracción incremental (NO big-bang; es el archivo VIVO del bot — un error rompe Telegram; verificar
  import+arranque entre cada extracción); (2) pulir comportamiento/organización general (óptica de
  producto terminado). ⚠️ Refactor DELICADO: sesión dedicada, archivo por archivo, con el bot
  verificado vivo tras cada paso. Junto con REDISEÑO MEMORIA = los 2 bloques grandes dejados al final.

- [⏸️] **DIST-1 · Plan de lanzamiento / descubrimiento — diferido (era de DISTRIBUCIÓN).** Cuando el
  `curl|sh` esté validado en limpio → armar el plan para que la gente DESCUBRA For3s: dónde compartirlo
  (r/selfhosted, Hacker News, X, Discords de IA), cómo (post de lanzamiento), en qué orden. Las config
  de GitHub (topics/README/license) CONVIERTEN cuando llega gente, pero NO traen tráfico solas — eso lo
  da el lanzamiento + las primeras ⭐ stars. NO empezar hasta que el producto esté validado.

- [⏸️] **DIST-2 · Probar `curl|sh` en máquina Linux LIMPIA — diferido (era de DISTRIBUCIÓN).** Lo único
  no probable en el server (donde Docker ya está). Es el MAYOR RIESGO de la distribución — idealmente el
  primer "tester" real. Requiere una máquina Linux limpia.

- [⏸️] **DIST-3 · Dominio install.for3s.dev + landing — diferido (era de DISTRIBUCIÓN, etapa 2).** Hoy
  el curl iría al raw de GitHub; el dominio + landing es la capa de producto/marketing de la instalación.

- [⏸️] **DIST-4 · v1.1: GitHub-MCP + render como hermanos de red en el instalador — diferido (era de
  DISTRIBUCIÓN, Opción B).** En el SERVER ya corren como hermanos de red (BUG-9/9b); esto es incluirlos
  en el PRODUCTO DISTRIBUIBLE (hoy el núcleo instalable va sin ellos). Cruza con P1-P10 (distribuible).

- [⏸️] **DIST-5 · Monetización del Open Core — diferido (era de DISTRIBUCIÓN).** Modelo definido, NO
  implementado: planes, licencia comercial activa, billing. Necesario para "producto que vende", no
  solo open source. Cruza con MULTI-INSTANCIA (base del SaaS) y BYOK (consumo por persona).

- [⏸️] **MS-1b · Arreglo FÍSICO del adaptador de red del server — diferido (era de MANTENIMIENTO).**
  MS-1 quedó RESUELTO en software (el WiFi Intel 8260 es la salida principal, estable). Lo único que
  queda es FÍSICO y requiere acceso físico de Brian al server: el adaptador USB-Ethernet ASIX AX88772A
  sigue `Link detected: no` y ciclando 10/100 → cable defectuoso/flojo o adaptador degradado. Acciones:
  cambiar el cable · probar otro puerto USB · reemplazar por chip RTL8153 o AX88179 USB3 Gigabit (mejor
  soportados). ⚠️ NO URGE: el WiFi cubre la red del server. Backup del netplan guardado.
  Memoria: [[project_mantenimiento_servidor]].

- [⏸️] **MI-EXTRA-1 · SaaS remoto multi-tenant — diferido (Brian 2026-07-02, surgió de MULTI-INSTANCIA).**
  Además del gestor LOCAL de instancias (MULTI-INSTANCIA, que SÍ atacamos ahora), a futuro For3s OS
  servirá clientes POR INTERNET como SaaS multi-tenant — algo INTERNO de For3s OS (Brian lo opera para
  sus clientes remotos). Distinto del gestor local (varios For3s en TU máquina). Requiere routing web,
  auth remoto, dominios, billing (cruza con DIST-5 monetización). Se retoma como bloque propio más
  adelante. NO ahora.

- [x] **MI-EXTRA-2 · ⭐ Botón WEB para encender/apagar instancias — ✅ CERRADO 2026-07-14 (Frente B
  F4.b, commit `2164376`).** Construido `for3s-ctl`: mini-agente HTTP en el host (systemd) que corre
  el gestor `for3s` — flota + encender/apagar por `https://for3s.tail6749e5.ts.net:8443/ctl`
  (tailnet-only + token, CORS estricto). El panel F4.c le pone los botones. Foresito = solo lectura
  (nave nodriza por terminal); general critica:true. Verificado E2E (ciclo real mashe, 409 en
  concurrencia, kill -9 revive <4s, /salud lo vigila con alerta). ⚠️ El toggle 1:1 de la demo del
  sitio (Vercel, `lib/demo/container.ts`) sigue NO-OP: cablearlo = exponer /ctl a internet
  (decisión de Brian pendiente). Ronda: `Cuerpo/Ronda_FrenteB_Puente_Mercado.md` §F4.b.

- [⏸️] **EC-EXTRA-1 · Backend de ejecución LOCAL / SSH (fuera de la caja) — diferido (Brian 2026-07-02).**
  El bloque EXECUTE_CODE (agente-desarrollador) corre TODO dentro de la caja Docker (seguro). Hermes
  además ofrece backends que SALEN a la máquina real: `local` (ejecuta en el host), `SSH` (máquina
  remota), y cloud (Daytona/Modal/Singularity). Esos backends dan más poder pero ROMPEN el aislamiento
  (el agente tocaría el host / otra máquina). Diferido a propósito: primero el sandbox seguro en la
  caja; los backends local/SSH/cloud se evalúan después, con su propio diseño de seguridad. Cruza con
  la paridad Hermes (execute_code multi-backend) y el modelo sin-DinD.

---

## 🐛 BUGS Y CÓDIGO HUÉRFANO — hallazgos de PR4-A (auditoría a fondo, Brian 2026-06-29) — varios CRÍTICOS

> **Origen:** PR4-A (diagnóstico a fondo "mirar lo que nadie mira"). Verificados contra código +
> BD real + logs del worker. Cada uno es un pendiente para ARREGLAR (PR4-A solo diagnosticó; el
> arreglo es su propio paso con OK de Brian). ⚠️ Varios son del CICLO NOCTURNO y se rompieron con
> la contenerización SIN que nadie se enterara → confirma PR2 (falta monitoreo).

### 🔴 AUDITORÍA CRÍTICA DE ERRORES (barrido F1-F5, Brian 2026-06-30) — usuarios + sistema

- [x] ✅ **BUG-19 · MEZCLA DE MEMORIA ENTRE USUARIOS EN EL GRAFO — RESUELTO 2026-07-01 (en el server).**
      🔍 Cazado siendo curioso tras limpiar `sessions` (Brian: "puede haber errores"). El grafo (kg.py)
      identificaba los nodos `Episodio` SOLO por `seq` (`MERGE (e:Episodio {seq:N})`), SIN session_id.
      Los seq se SOLAPAN entre sesiones (Sme G 1-26, brian:backend 1-8, Brian 1-692) → el seq:5 de una
      persona se fundía con el seq:5 de otra en el MISMO nodo = MEZCLA de memoria entre usuarios en el
      grafo. ⚠️ BUG LATENTE que **BUG-18 (CLS multi-sesión que YO arreglé) activaría** en la 1ª
      consolidación nocturna de un miembro (hoy solo `brian` había consolidado → sin mezcla aún, cazado
      a tiempo). FIX: (1) `kg.registrar_concepto` + `escribir_concepto` (consolidator) ahora pasan y
      usan `session_id` → `MERGE (e:Episodio {seq:N, session_id:'...'})` (nodos separados por sesión);
      (2) `episodios_de_concepto` devuelve session_id; (3) backfill: los 601 Episodios viejos (todos de
      brian) → session_id='brian'. Probado E2E: seq=5 de 2 sesiones = 2 nodos separados (antes 1).
      Grafo coherente (601 con session_id), bot sano. Permanente (repo+rebuild). ⚠️ Deuda menor anotada:
      `hilo_status` y `corridas_equipo` NO tienen FK a `sessions` (integridad sin proteger; hoy sanos).

- [x] ✅ **BUG-18 · CICLO NOCTURNO era SINGLE-SESSION — RESUELTO 2026-06-30 (en el server).** Cazado al
      investigar los hermanos del cron (Brian: "hay cosas que aún no llegas a ver"). CLS (consolidar) y
      Microglía (olvidar) operaban SOLO sobre `SESSION_OWNER='brian'` → **la memoria de los MIEMBROS
      (Sme G: 26 turnos) y de otros temas del dueño (brian:backend: 8) NUNCA se consolidaba al grafo ni
      se podaba** (verificado en BD: 26/26 y 8/8 sin consolidar). En un producto multi-usuario, la
      memoria de los miembros nunca maduraba. (job_relevance SÍ iteraba todas las sesiones — solo
      CLS/microglía estaban atrás.) FIX: helper `_sesiones_vivas()` (DISTINCT session_id con embedding)
      + job_cls y job_microglia ahora iteran TODAS las sesiones (defensivo: una sesión que falle no
      frena al resto). Seguro: consolidar/olvidar ya reciben session_id y olvidar filtra estricto por
      session_id (no borra de otras). Probado EN VIVO: el CLS ahora ve las 3 sesiones. Rebuild + recrear
      worker → permanente. ⚠️ EN EL SERVER — repo/GitHub pendiente de orden de Brian.
- [x] ✅ **BUG-17 · FUGA DE HISTORIAL al TRANSFERIR + inconsistencia de nombres — RESUELTO DE RAÍZ 2026-07-01.**
      La mini-migración se HIZO (con backup 14M + transacción atómica). Desacoplé los 3 roles de la
      cadena 'brian': (1) MEMORIA → migré 1232 filas (6 tablas) + 601 Episodios del grafo de
      brian/brian:backend a tg:1923367928/tg:1923367928:backend; (2) CÓDIGO → `_base_sesion` liga la
      sesión a la IDENTIDAD (`tg:<uid>`) para TODOS incl. el dueño → al transferir ya NO se hereda
      historial (fuga cerrada de raíz, no solo mitigada); (3) CIFRADO → secrets sigue en
      workspace_id='brian' INTACTO (verificado: GitHub MCP conectó = tokens descifran). 🔍 La curiosidad
      cazó 2 trampas durante la migración (la transacción las revirtió): colisión de seq con el residuo
      tg:1923367928 (16 turnos borrados del 28-jun) y colisión de PK en hilo_status → resueltas borrando
      el residuo primero. Sesiones ahora TODAS `tg:<uid>` (cero 'brian') = inconsistencia de nombres
      también RESUELTA. `/transferir_dueno` sigue deshabilitado (guard) — reactivarlo es el último paso
      menor (ahora ya es seguro reactivar, pero requiere que transferir también mueva las sesiones del
      viejo dueño; anotar). 8 contenedores sanos, permanente (rebuild). ⚠️ EN EL SERVER.
      --- (histórico) MITIGADO 2026-06-30: ---
      🔍 ANÁLISIS A FONDO (Brian: "hay inconsistencias de la información"): la cadena `'brian'` hace
      **3 TRABAJOS ACOPLADOS por accidente histórico**: (1) **workspace de CIFRADO** de secrets
      (`derive_workspace_key(master,'brian')` → si se toca, los tokens NO se descifran = bot muerto);
      (2) **clave de CONFIG** (`sessions.id='brian'` con last_repo + modelo); (3) **sesión de MEMORIA**
      (7 tablas: episodes_events, gh_resources, corridas_equipo, consulted_files, consulted_web,
      hilo_status + la tabla `sessions` padre). Las FKs hacia `sessions` son NO ACTION → renombrar exige
      orden estricto (crear sessions.id nuevo → mover hijas → borrar viejo). EL BUG: al transferir, el
      nuevo dueño hereda `_base_sesion`='brian' = el historial privado del viejo (659 turnos); el viejo
      pasa a tg:<uid> y pierde el suyo. `transferir()` NO renombra sesiones.
      ✅ **MITIGACIÓN SEGURA HECHA (2026-06-30):** `/transferir_dueno` DESHABILITADO con aviso claro
      (guard tras el check de admin) → nadie puede disparar la fuga. En el repo + imagen (permanente).
      Verificado. ⏳ **FIX DE RAÍZ PENDIENTE (sesión dedicada):** DESACOPLAR identidad-de-sesión del
      workspace-de-cifrado (mini-migración de arquitectura): separar el rol "memoria" del rol "cifrado"
      de 'brian'; ligar la sesión del dueño a su user_id (tg:<uid>) como todos; migrar las 7 tablas +
      sessions con orden de FKs + backup; ajustar _base_sesion y SESSION_OWNER (worker). NO forzar con
      prisa (riesgo de romper el descifrado de tokens). Cruza con MULTI-INSTANCIA y REDISEÑO MEMORIA.

> 🚨 **HALLAZGO MAYOR DEL BARRIDO DE DEUDAS MENORES (2026-06-30):** al ir a cerrar HA-7 (agent/worker
> imágenes distintas) se descubrió que **aplicar fixes con `docker cp` es EFÍMERO** — al recrear el
> agent (durante BUG-15 con `docker compose up`) se PERDIERON en el contenedor los fixes de HA-1, HA-5
> y **BUG-14 (¡la fuga de privacidad quedó REABIERTA en producción!)**, porque solo vivían en docker cp.
> LECCIÓN CRÍTICA: los fixes deben ir al REPO `~/for3s-os` + REBUILD de la imagen, no solo docker cp.
> SOLUCIÓN: se consolidaron TODOS los fixes en el repo (skills/governor/memory/analytics/telegram_channel
> + migración 025 + .dockerignore) → REBUILD de la imagen → recrear agent+worker → fixes PERMANENTES
> y resistentes a reinicios. Verificado: BUG-14 cerrado de nuevo (scope Sme G sobre brian = 0). 7
> contenedores sanos, agent=worker misma imagen. ⚠️ EN EL SERVER — repo local/GitHub pendiente de orden.
> Deudas menores cerradas EN ESTE BARRIDO: HA-1b (cableada ultimas_corridas a /diagnostico) · HA-4
> (.dockerignore creado + borrados todos los .bak incl. un .env.bak con 2 secretos) · HA-7 (rebuild =
> misma imagen) · requiere_aprobacion (decisión: NO borrar — es API de permisos válida no cableada, se
> deja para cuando el modelo de roles crezca; documentada, no es basura).
- [x] ✅ **BUG-14 · FUGA DE PRIVACIDAD en el scope de memoria — RESUELTO 2026-06-30 (en el server).**
      🔴 El más crítico del barrido. El filtro de `buscar_semantico` incluía `OR owner_user_id IS NULL`
      → trataba los 667 turnos legado del DUEÑO (owner_user_id NULL) como "visibles para cualquiera".
      Probado EN VIVO: scope de Sme G sobre la sesión `brian` devolvía turnos PRIVADOS de Brian
      (godinez-studio, Excel de usuarios...). La única defensa era el `session_id` (1 sola capa).
      FIX (2 partes): (1) backup + backfill `owner_user_id=1923367928` en los 667 turnos legado de las
      sesiones del dueño (brian, brian:backend) — Sme G intacta; (2) quitado el `OR owner_user_id IS
      NULL` del scope (memory.py) → privacidad por construcción, no depende del session_id. Verificado
      E2E: [1] scope Sme G sobre brian = 0 (sin fuga) · [2] dueño ve lo suyo = 3 · [3] Sme G ve lo
      suyo = 3. Agent+worker sincronizados, reiniciado sano. ⚠️ EN EL SERVER — repo/GitHub pendiente
      de orden de Brian ([[feedback_flujo_server_primero]]).
- [x] ✅ **BUG-15 · Conflict de doble instancia en reinicios — RESUELTO 2026-06-30 (en el server).**
      🔍 CAUSA RAÍZ (análisis a fondo de los elementos que se comunican con Telegram): el command del
      agent era `["sh","-c","... migrate && python -m ...telegram_channel"]` → **PID 1 = `sh`**, Python
      era hijo (PID 10). En `docker restart`, SIGTERM lo recibía el SHELL, que NO lo propaga a su hijo
      por `&&` → Python nunca apagaba limpio → tras 10s Docker hacía SIGKILL → el bot moría sin soltar
      el `getUpdates` de Telegram → la instancia nueva chocaba = `telegram.error.Conflict: terminated
      by other getUpdates`. (Telegram solo permite 1 getUpdates por token.) FIX (docker-compose.yml):
      (1) `&& exec python -m ...telegram_channel` → Python REEMPLAZA al shell = **PID 1**, recibe
      SIGTERM directo y apaga limpio; (2) `stop_grace_period: 25s` → tiempo para que PTB suelte el
      polling antes del SIGKILL. Verificado E2E: PID 1 ahora=python (antes=sh); reinicié el agent →
      **CERO Conflict** (antes salía en cada reinicio). 7 contenedores sanos. ⚠️ EN EL SERVER —
      repo/GitHub pendiente de orden de Brian.
- [x] ✅ **BUG-16 · Gate de aprobación — INVESTIGADO, NO ES BUG (2026-06-30, en el server).** El
      barrido multi-usuario sospechó que el gate "miembro propone → encargado aprueba" no estaba
      cableado (la función `requiere_aprobacion` está huérfana). Investigación a fondo de las conexiones
      hermanas: el gate SÍ está completo y FUNCIONA. Flujo real verificado: `_proponer_write` (bifurca
      por rol con `_es_admin`) → miembro va a `_proponer_write_miembro` → `crear_solicitud` (tabla
      solicitudes) + avisa al encargado con [✅/❌] → `on_gate_select` (aprobar valida rol EN BD,
      fail-closed) → `ejecutar_write` (hermano MCP write) → audit `github_write_gate` → avisa al
      solicitante. PROBADO E2E: [miembro NO puede auto-aprobarse → None + log "NO es encargado"] +
      [encargado aprueba → estado aprobada]. Lección (3ª vez en la sesión, como HA-1): un diagnóstico
      de "no cableado" debe verificarse EN VIVO antes de creerlo. Hallazgos menores reales:
      `requiere_aprobacion` (equipo.py:76) es huérfana de verdad (decisor alternativo no usado, la
      decisión la toma `_es_admin` — borrar o ignorar); skills de un miembro (/aprende) son GLOBALES
      (aplican también al dueño) — intencional + pasan por el scanner del governor, pero es una decisión
      de diseño a revisar (¿debería una skill de Sme G entrar en las conversaciones de Brian?).

- [x] ✅ **Inconsistencia de convención de sesión (F4) — RESUELTA DE RAÍZ 2026-07-01 (con BUG-17).**
      Ya NO hay `brian`/`brian:backend` — todas las sesiones son `tg:<uid>` (dueño incluido). Se migró
      la memoria (BD+grafo) + `_base_sesion` liga a la identidad. Ver BUG-17 arriba. --- (histórico) ---
      miembro usa `tg:7740601619`. Nombres mezclados. No rompe (están separadas), pero frágil — un
      cambio de convención podría cruzar sesiones (conecta con BUG-14). Unificar a un esquema único
      (ej. `tg:<uid>` para todos) en una migración cuidada. Menor. **Es la misma raíz que BUG-17
      (`brian` hardcodeado = 3 roles acoplados). El fix de raíz cierra ambos → sesión dedicada.**
      ✅ **PASO 1 HECHO 2026-07-01 (bajo riesgo):** LIMPIEZA de basura en `sessions` — se borraron 33
      sesiones de test/prueba (test-*, brian-test, diag_repro, test-h12-*, sess-p2) + 59 episodes
      huérfanos, en transacción con backup (pre_limpieza_sessions_*.sql). Quedan SOLO las 4 reales
      (brian, brian:backend, tg:1923367928, tg:7740601619). Secrets/cifrado NO tocado (intacto, 2
      tokens). Bot sano. Esto NO resuelve el bug de raíz (sigue pendiente la mini-migración) pero deja
      la BD limpia para verlo mejor y evita arrastrar basura al fix futuro.
- ✅ **Barrido F1/F3/F5 SANO:** F1 las respuestas "no puedo" son legítimas (honestidad/privacidad
      funcionan: "no puedo decirte eso, Sme G es otra persona 🔒"). F5 26 comandos, sin fantasmas.
      HA-6 GitHub E2E verificado (search_repositories + get_file_contents OK).

### 🔴 BUGS CRÍTICOS (arreglar pronto)

- [x] ✅ **BUG-1 · DECAY de memoria — ARREGLADO Y VERIFICADO 2026-06-29.** Añadido `job_relevance`
      a tasks.py (cron 02:45 Mx, ANTES de Microglía) que recalcula `relevance` de TODAS las sesiones
      con embedding (no solo brian — también cierra el hallazgo "cron solo-brian"). Constante
      HORA_RELEVANCE_UTC + functions + cron_jobs. Verificado en vivo: `job_relevance` recalculó 34
      sesiones / 758 turnos → relevance NULL 245→0 (758/758 con valor), Sme G y brian:backend que
      estaban 100% NULL ahora tienen decay. La cadena del olvido queda completa (CLS✅ + relevance✅ +
      microglía). ⚠️ Nota: el olvido real empezará a tener candidatos ~mediados de julio (cuando los
      turnos cumplan 30 días); hoy 0 candidatos = correcto. ⭐ ADEMÁS se arregló de raíz el
      Dockerfile: el modelo BGE-M3 ahora se COPIA de caché local (docker/model-cache/) en vez de
      descargarse de internet en cada build → builds rápidos y robustos ante la red inestable del
      server (los cortes de red truncaban el build). Modelo movido ANTES del COPY del código.
      Backups .bak/.bak2 de tasks.py y Dockerfile.agent guardados.

- [ ] ~~BUG-1 (texto original)~~ **DECAY de memoria MUERTO (H6 incompleto) — afecta MEMORIA.** `relevance.py` tiene
      `recalcular_relevance_lote()` pero NADIE la llama (búsqueda vacía en todo el repo) y NO está
      en el cron (`tasks.py`). El "Sub-paso 10" (conectar el recálculo al cron) quedó a medias.
      EVIDENCIA BD: 515 turnos con relevance TODOS en decil 10 (0.91-0.99, congelados desde 22-jun)
      + 245 nuevos con relevance NULL. La microglía filtra `relevance IS NOT NULL AND relevance < X`
      → siempre 0 candidatos (log: `Microglía candidatos=0`). **Foresito NUNCA olvida por relevancia.**
      ARREGLO (🔵 EN CURSO 2026-06-29): añadido `job_relevance` a tasks.py (cron 02:45 Mx, ANTES de
      Microglía 03:00) que recalcula `relevance` de TODAS las sesiones con embedding (no solo brian —
      también ataca el hallazgo "cron solo-brian"). Constante HORA_RELEVANCE_UTC + registrado en
      functions + cron_jobs. Sintaxis OK. Probado en seco: recalcular_relevance_lote('brian') tocó
      649 filas, NULL 136→2, valores recalculados (decay actuando). ⏳ FALTA: rebuild imagen (el código
      se HORNEA, no se monta) + recrear worker + verificar el job en vivo en todas las sesiones.
      ⚠️ Nota: nada cumple 30 días aún → no habrá candidatos de olvido hasta ~mediados de julio, pero
      el decay ya quedará vivo y listo. Cruza con MEM-1/MEM-3 (rediseño memoria).

- [x] ✅ **BUG-5 · BACKUP automático ROTO — ARREGLADO Y VERIFICADO 2026-06-29.** Causa confirmada:
      `pg_dump` NO estaba en la imagen `for3s-agent` (donde corre el worker) → `job_backup` daba
      `FileNotFoundError` desde la contenerización (28-jun; antes, suelto, funcionaba — había
      backups auto del 20 al 27-jun en el host). ARREGLO: añadido `postgresql-client` a
      Dockerfile.agent + rebuild. Verificado: pg_dump 17.10 en el worker, backup manual disparado
      OK (15M, 760 turnos), restaura a BD temporal con los 760 turnos (el único "error" del restore
      = `transaction_timeout` de PG17 ignorado por PG16, inofensivo). ⏳ Pendiente menor: activar
      offsite (sigue bloqueado por Tailscale, ver H6-backup-offsite).

- [x] ✅ **BUG-6 · Carpeta de backups SIN volumen — ARREGLADO 2026-06-29.** Montado
      `/home/brianweb3/for3s-backups:/root/for3s-backups` en agent Y worker (docker-compose). YAML
      validado. Verificado: el backup nuevo (auto_for3s_20260629_044328.sql) cae en el HOST, ya no
      es efímero. Backups (.bak) de Dockerfile.agent y docker-compose.yml guardados.

- [x] ✅ **BUG-8 · CLS consolida 0 conceptos — ARREGLADO Y VERIFICADO 2026-06-29.** CAUSA RAÍZ
      (no era el LLM): **catálogo de Apache AGE corrupto tras la migración a contenedores.** Al
      restaurar el dump, el schema `for3s_kg` recibió OID nuevo (17318) pero `ag_catalog.ag_graph.
      graphid` conservó el viejo (19195) → AGE buscaba el grafo por 19195, no existía → toda escritura
      por la wrapper `cypher_write` fallaba con `graph with oid 19195 does not exist` (silencioso,
      grafo defensivo). El LLM de CLS SÍ creaba los conceptos; lo que fallaba era ESCRIBIRLOS al grafo.
      ARREGLO (backup previo + transacción): drop FK fk_graph_oid → UPDATE ag_graph.graphid y
      ag_label.graph (17 filas) de 19195→17318 → recrear FK. VERIFICADO: graphid=oid coinciden, grafo
      viejo INTACTO (559 Episodios + 62 Conceptos), wrapper escribe OK, CLS real ahora da
      `clusters=3 conceptos=3 marcados=31` (antes 0/0), pendientes 90→59, consolidated 559→590. El
      grafo VUELVE A CRECER. ⚠️ Bug clásico de AGE con pg_dump/restore (el graphid no se re-mapea al
      restaurar) → documentar para futuras migraciones (MULTI-INSTANCIA, ENTRENAMIENTO). Cruza con la
      migración de Foresito.

- [~] **BUG-9 · GitHub MCP HERMANO de red — ✅ PARTE GITHUB HECHA Y VERIFICADA 2026-06-29.**
      SOLUCIÓN "hermanos de red" v1.1 (aprobada por Brian). Hecho: (1) 2 servicios nuevos en
      docker-compose — `github-mcp` (http --read-only) y `github-mcp-write` (http) — corren el
      github-mcp-server oficial en modo HTTP :8082. (2) `mcp_client.py` reescrito stdio→HTTP
      (streamablehttp_client + PAT en header Authorization; URLs por env FOR3S_GITHUB_MCP_URL /
      _WRITE_URL; interfaz pública IDÉNTICA → cero cambios en conversation/subbloques/tool_loop/
      telegram). (3) agent depende de los hermanos (depends_on). VERIFICADO E2E: el bot loguea
      "GitHub MCP conectado", 0 errores docker, 21 read tools + 37 write tools, call_tool real contó
      4230 PRs de cli/cli. El bot NO toca docker (seguridad intacta). ⭐ ADEMÁS rebuild ahora ~25s
      (antes ~10min) por el fix del modelo en caché. Backups .bak guardados.
      🔍 HALLAZGOS del análisis de hermanos: (A) ✅ depends_on añadido (arranque ordenado).
      (B) ⚠️ healthcheck NO posible: la imagen github-mcp-server es DISTROLESS (sin /bin/sh ni
      wget) → healthcheck con CMD-SHELL falla; se quitó, queda restart:unless-stopped. El health
      real será por HTTP externo (PR2 monitoreo). (C) ✅ hermanos NO exponen puertos al host (solo
      red interna, seguro). ⏳ FALTA la 2ª parte (render/web_fetch) → ver BUG-9b abajo.

- [x] ✅ **BUG-9b · render/web_fetch HERMANO de red — HECHO Y VERIFICADO E2E 2026-06-29.** Hecho:
      (1) `docker/render/render_http.py` NUEVO — servidor HTTP (stdlib, ThreadingHTTPServer) que
      recibe `GET /?url=...` y devuelve {ok,titulo,texto} usando el render Playwright existente +
      endpoint `/health` para PR2. (2) Dockerfile.render: ENTRYPOINT script → CMD server HTTP,
      EXPOSE 8080. (3) servicio `render` en docker-compose (hermano, build local) + agent depende de
      él. (4) `web_fetch.py` _render_headless: `docker run` → `httpx.get(http://render:8080/?url=)`
      (env FOR3S_RENDER_URL). VERIFICADO E2E: render health 200, example.com + react.dev renderizan
      (SPA con JS), fetch_url("react.dev") devolvió 8772 chars con contenido real. El bot NO toca
      docker. ⚠️ cold-start: el 1er render tras arrancar tarda (Chromium calienta), luego va bien.
      🎉 **BUG-9 COMPLETO: GitHub MCP (read+write) + render, los 3 hermanos de red. 7 contenedores,
      0 errores docker.** Backups .bak guardados.

- [ ] ~~BUG-9 (texto original)~~ **GitHub MCP + web_fetch ROTOS en el contenedor (intentan lanzar `docker`).**
      Hallazgo 2026-06-29 (panorama). El bot NO tiene docker (decisión sin-DinD). PERO 3 componentes
      hermanos siguen invocando `docker run`: (1) `mcp_client.py` config_github lanza
      `docker run github-mcp-server` → **GitHub CAÍDO** (analizar repos falla con
      `FileNotFoundError: docker`); (2) `web_fetch.py` _render_headless lanza `docker run for3s-render`
      → web fetch de SPAs/JS degradado (solo httpx, sin render); (3) `sandbox.py` (= BUG-2, ya muerto).
      Es exactamente lo que la auditoría PR4-C anticipó y lo que está registrado como "v1.1 hermanos
      de red". ARREGLO (diseño, NO parche): conectar GitHub-MCP y render como contenedores HERMANOS
      vía red (no DinD) — NO darle docker al bot (rompería el diseño de seguridad de Brian). Es trabajo
      de v1.1. ⚠️ Mientras tanto: el bot degrada (traga el error), no se cae, pero SIN GitHub real.
      PATRÓN: 3er bug "funcionaba suelto → roto al contenerizar → nadie se enteró" (con BUG-5 y BUG-8)
      → refuerza PR2 (monitoreo). Cruza con [[project_fase_pretesters]] (Opción B v1.1) y H8/MCP.

- [~] **BUG-2 · `sandbox.py` — DIFERIDO (no borrar) 2026-06-29.** Análisis: NO es solo "código
      muerto" a borrar — es una CAPACIDAD útil (lint objetivo de PRs con ruff en contenedor Docker
      ENDURECIDO: --network none, --read-only, --user, límites CPU/mem/pids) que quedó desconectada
      al migrar a GitHub MCP. Decisión: NO borrarla (se perdería el diseño de aislamiento ya escrito);
      DIFERIR hasta el flujo de PR-review completo, y entonces volverla HERMANO de red (como BUG-9,
      ya no puede usar `docker run`). Hasta entonces queda inerte (no estorba). 🧹 SÍ se limpió basura
      relacionada: 3 .pyc huérfanos en __pycache__ de módulos ya borrados (github_tool, pr_review,
      ratelimit). Cruza con BUG-9 (patrón hermano) y PR7 (revisar Hs).
- [x] ✅ **BUG-10 · embeddings NO precargaban — RESUELTO 2026-06-29.** Eran 3 problemas en capas,
      todos causados por la extracción de caché del modelo que hice en BUG-1 (docker/model-cache):
      (1) el modelo quedó PARTIDO en 2 snapshots (config en `5617a9f`, pesos `.safetensors` en
      `9a0624b`) → ST cargaba del de config y no hallaba los pesos. FIX: copié el safetensors (2.2GB)
      al snapshot con config. (2) `sentence_transformers` TOCABA INTERNET al cargar (verificar
      metadatos HF) → con red inestable, fallaba. FIX: `HF_HUB_OFFLINE=1` + `TRANSFORMERS_OFFLINE=1`
      en Dockerfile.agent. (3) caché negativa `.no_exist/model.safetensors` (0 bytes) que MENTÍA
      "el archivo no existe" aunque sí estaba → con offline, HF le creía. FIX: borré `.no_exist`.
      VERIFICADO: "modelo de embeddings precargado (memoria semántica lista)" + embed 1024 dims +
      /salud 0 fallas. ⭐ Ahora la memoria semántica es ROBUSTA ante cortes de red (offline real).
      Lección: un fix (BUG-1 extracción de caché) introdujo este bug → verificar efectos colaterales.

> ✅ **VERIFICACIÓN DE INTEGRACIONES (PR2, 2026-06-29) — resultado:** GitHub MCP read (lee archivos
> reales + 🔒 rechaza writes), GitHub MCP write (37 tools), render (SPA + caso límite degrada limpio),
> tool_loop completo (bot contó 4234 PRs e2e), Claude responde, Valkey ping, KEK descifra ambos
> secretos, worker con TODOS los crons VERDES (backup/CLS/relevance/microglía/status/dmn, 0 errores
> = los 8 bugs confirmados arreglados EN PRODUCCIÓN). Único hallazgo: BUG-10 (embeddings precarga).

- [x] ✅ **BUG-3 · 16 turnos huérfanos — RESUELTO 2026-06-29.** Eran TUS turnos (Brian, owner_id
      1923367928) de la conversación del 28-jun cuando Foresito "olvidó todo" (el bug del mount, ya
      arreglado en la migración) → cayeron en sesión `tg:1923367928` en vez de `brian`. CONFIRMADO
      que el routing del owner YA funciona (90 turnos recientes de brian etiquetados con tu user_id
      correcto). Soft-delete (reversible) de los 16 con backup previo. Sesión queda 0 vivos / 16
      borrados. ✅ INTEGRIDAD verificada de paso: 0 turnos sin embedding, audit chain ÍNTEGRA (1514
      verificadas), 0 seq duplicados → los datos están sanos, no hay error grande oculto.
- [~] ~~BUG-2 original~~ **DECIDIDO (ver BUG-2 arriba, línea 668): DIFERIR, no borrar.** `sandbox.py`
      NO es basura — es una capacidad útil (lint aislado de PRs con diseño de aislamiento ya escrito) que
      quedó desconectada al migrar a GitHub MCP. Se difiere hasta el flujo de PR-review (volverla hermano
      de red). Queda inerte, no estorba. Confirmado 2026-07-16: sin acción, decisión LOCKED correcta.

### 🟡 BUGS MENORES / LIMPIEZA

- [x] ✅ **BUG-3 · huérfanos + basura de test — RESUELTO 2026-06-30.** (1) los 16 turnos huérfanos
      de `tg:1923367928` (del bug de la migración) soft-deleted ✅. (2) 🔍 LA CURIOSIDAD destapó MÁS:
      ~30 sesiones `test-*` + `brian-test` + `diag_repro` (59 turnos, de los días de dev 12-13 jun,
      con contenido basura "a"/"b"/"hola") estaban VIVAS en producción + con embedding + relevance →
      el cron las procesaba y contaminaban /salud hilos (mostraba 34 sesiones). Soft-deleted con
      backup previo (reversible). VERIFICADO: /salud hilos ahora muestra 3 sesiones REALES (brian,
      Sme G, brian:backend) en vez de 34. Integridad confirmada (0 roles inválidos/contenido vacío/
      seq nulos; no contaminaban grafo ni gh_resources). BD de producción limpia.
- [x] ✅ ~~BUG-3 (texto original)~~ **YA RESUELTO (ver BUG-3 arriba, línea 707): soft-deleted 2026-06-30.**
      Los 16 turnos huérfanos de `tg:1923367928` se soft-borraron. Confirmado 2026-07-16: query en la BD de
      brian/Foresito devuelve 0 filas → ya no existen. Sin acción pendiente.

- [x] ✅ **BUG-4 · Owner frágil — RESUELTO 2026-06-30 (en PR6.1).** La identidad del dueño dependía
      SOLO de `telegram_owner.json` en cwd → causó "Foresito olvidó todo" en la migración. FIX:
      la BD es ahora la FUENTE DE VERDAD del owner (tabla `owner`, migr 024); el JSON queda como
      caché. OwnerStore.sync_con_bd() en setup() carga el owner de la BD + repara el JSON. VERIFICADO
      E2E: simulé el bug (sin JSON) → get_owner None/is_authorized False; tras sync → recuperado de
      la BD (1923367928), JSON reparado solo. Ya no puede volver a pasar (la BD viaja con backups).

- [x] ✅ **BUG-13 · `/diagnostico` leía la sesión del DUEÑO (fuga de privacidad) — ARREGLADO 2026-06-29 (en PR10.2).** El /diagnostico viejo hacía `load_history(_owner_session)` SIEMPRE → un miembro habría visto los turnos de Brian. FIX: usar `_sesion_de(user)` (sesión real del usuario, respeta aislamiento H8/AI1). Verificado: miembro ve solo lo suyo. Era solo-admin además; ahora abierto a todos como auto-diagnóstico personal.
- [x] ✅ **BUG-12 · `/estado` visible pero bloqueado — ARREGLADO 2026-06-29 (en PR10.1).** Detectado
      2026-06-29 en el análisis de hermanos de comandos (PR10). `/estado` está en `_MENU_BASICO` (lo
      ven TODOS los usuarios) PERO su handler chequea `_es_admin` → "⛔ Comando solo para el dueño".
      Un miembro lo ve en su menú, lo pulsa, y recibe rechazo → experiencia confusa. FIX: o quitarlo
      del menú básico (solo admin), o abrirlo a todos (es info de salud no sensible: uptime/modelo).
      Verificado que /start y /cupo NO tienen el problema (chequean _autorizar, no _es_admin — eran
      falsos positivos del grep). Se arregla dentro de PR10. Cruza con PR9 (UX producto).

### ✅ FUNCIONES HUÉRFANAS DE MEMORIA — TODAS CABLEADAS 2026-07-01 (EN PRODUCCIÓN)

> ⚠️ Brian: "estas son importantes para la parte de las MEMORIAS, súper importantes." Eran capacidades
> de NAVEGACIÓN DEL GRAFO/memoria construidas pero desenchufadas. **YA ENCHUFADAS todas** (verificado
> en vivo 2026-07-01, commit 3b001ee firmado + horneado + push a GitHub):

| Función | Módulo | Qué hace | Estado |
|---|---|---|---|
| `recalcular_relevance_lote` | relevance.py | recalcular el decay de memoria | ✅ = BUG-1 (job_relevance al cron, sano: 693/702 con relevance) |
| `lint_archivos` | sandbox.py | lint de PR en contenedor | ⏸️ = BUG-2 (diferido a propósito, no basura; con el flujo PR-review) |
| **`episodios_de_concepto`** | kg.py | navegar grafo: concepto → sus episodios | ✅ cableada en M2 (variante `_con_sesion` aislada por sesión) |
| **`recursos_de_repo`** | kg.py | navegar grafo: repo → sus issues/PRs | ✅ cableada (inyecta issues/PRs del repo activo; 0 datos hoy, lista) |
| **`repos_de_owner`** | kg.py | navegar grafo: owner → sus repos | ✅ cableada (+ nueva `kg.owners()`; "qué repos he visto de X") |
| **`get_last_repo` / `set_last_repo`** | memory.py | recordar el último repo visto | ✅ cableadas (set al leer repo · get resuelve "ese repo"/"sus issues") |
| `requiere_aprobacion` | equipo.py | ¿esta acción necesita gate de aprobación? | ⚠️ NO cableada — decisión: la toma `_es_admin`; API alternativa no usada (no es bug, ver BUG-16) |

> 🎉 **Todas las de MEMORIA cerradas:** las 3 de `kg.py` (episodios/recursos/repos_de_owner) + `kg.owners()`
> nueva + `get/set_last_repo` de memory.py. El grafo YA se navega en la recuperación (M2/M3 cascada +
> el bloque de "repo activo" en send()). Ninguna capacidad de navegación de memoria quedó desenchufada.
> Solo quedan sin cablear (a propósito): `lint_archivos` (BUG-2 diferido) y `requiere_aprobacion` (no-bug).
> ✅ Aclarado: `backup_y_rotar` NO es huérfana (job_backup la llama); `verify_chain`/`md_to_telegram` en tests.

> **Orden sugerido de arreglo:** BUG-5+BUG-6 (backup, lo más urgente) → BUG-1 (decay) → BUG-8 (CLS)
> → cablear las 3 funciones de grafo (MEM) → BUG-2/BUG-3 (limpieza) → BUG-4 (a PR6). Todos: NADA sin
> OK de Brian (PR4-A solo diagnosticó). Detalle del diagnóstico en la sección PR4 arriba + memoria
> [[project_pr4a_bugs_memoria]].

---

## 🧠 REDISEÑO DE LA CAPA DE MEMORIA — "cerebro real, no 5 silos" (Brian 2026-06-29) — ARQUITECTURA MAYOR, debatir tipo Ronda

> **Origen:** revisando el doc PR4 (los diagramas de memoria), Brian detectó 3 debilidades reales
> de arquitectura en cómo For3s maneja la memoria. Las 3 apuntan a lo mismo: la capa de memoria
> son **silos sueltos**, no un cerebro conectado y jerárquico. ⚠️ Es material de una RONDA de
> diseño completa (como las R1-R10). NO tocar código — debatir→diseñar→aprobar primero.
>
> ✅ **RONDA DE DISEÑO HECHA 2026-07-01 → `Cuerpo/Ronda_Rediseno_Memoria_Plan.md`.** Análisis a
> profundidad (BD+código real, Brian "todo se hizo por separado, no es producto"). Encontró la RAÍZ:
> **fragmentación de IDENTIDAD** (5 formas de identificar a la persona: telegram_user_id/user_id/
> owner_user_id/session_id/sessions.id) + **17 de 25 tablas son silos SIN FK** (perfil_usuario,
> hilo_status, temas no se conocen entre sí) + recuperación en paralelo (14 funciones vuelcan crudo
> en send()) + sin capa central (16 módulos tocan tablas directo). **PLAN de 5 fases** (menor→mayor
> riesgo): F1 identidad unificada · F2 capa de acceso central · F3 conectar (FKs+vista maestra=MEM-1) ·
> F4 cascada (MEM-3, la mejora mayor, lo más delicado) · F5 temas de equipo (MEM-2). NO se ha tocado
> código — cada fase se construye con OK de Brian. Detalle completo en el doc de la Ronda.
>
> ✅ **REDISEÑO MEMORIA COMPLETO (2026-07-01): F1-F5 + M1-M4 hechos y EN PRODUCCIÓN.** Detalle en la Ronda.
> · ✅ **F1** identidad — migr 026 tabla `personas` (ancla canónica) + sincronización (agregar_miembro/
>   set_owner_bd la mantienen; probado que no se desincroniza).
> · ✅ **F2** fachada — módulo `memoria.py` (coordina las 5 capas tras 1 identidad; persona()+sesion_de()).
> · ✅ **F3** conectar (MEM-1 base) — migr 027: backfill 563 legado + 4 FKs NULLABLE a personas (probado:
>   NULL pasa, inválido se rechaza; integridad sin romper flujos).
> · ✅ **F4** cascada precisión — cortacircuitos (triviales no buscan) + umbral 0.75→0.55 + RE-RANKING por
>   palabra clave (cortó ruido cumpleaños 629→0 sin mutilar relevantes). Más precisión medida.
> · ✅ **F5** temas de equipo (MEM-2) — camino B (sesión compartida `eq:<id>:<tema>`) + UX completa
>   (pasos 1-5): equipo_id cableado end-to-end · estado_persona (migr 029) · comando `/tema equipo`
>   con control de acceso (anti-salto de equipo) · `_sesion_de` usa la sesión de equipo · banner UX.
>   Probado E2E (aislamiento verificado: imposible ver privado de otro / saltar de equipo). EN PRODUCCIÓN.
> · ✅ **M1** corte de relevancia global — el grafo trae los conceptos DEL TEMA de la query (no 25
>   arbitrarios de 63); si ninguno aplica → no inyecta. Panorama puro sigue trayendo todo.
> · ✅ **M2** grafo navegable (MEM-1 cerrado) — `episodios_de_concepto_con_sesion` + `turnos_por_seq`
>   (aislado por sesión) → concepto→episodios REALES como evidencia. Cerró las funciones huérfanas del grafo.
> · ✅ **M3** cascada semántica→grafo — los recuerdos que la semántica destila informan QUÉ conceptos
>   del grafo traer (mejor que la query cruda). Conservador (2 recuerdos más cercanos + tope palabras).
> · ✅ **M4** ensamblaje único (MEM-3 cerrado) — `memoria.recordar()` ensambla la cascada de memoria
>   (semántica→grafo→episodios) en 1 punto; send() la llama en 1 línea. Probado equivalencia byte-a-byte.
> ⚠️ TODO en el SERVER (repo `~/for3s-os` + horneado en la imagen) — SIN sincronizar a GitHub (lote grande:
>   migr 026/027/028/029 + memoria.py/temas.py + cambios en conversation/kg/memory/telegram_channel).

- [x] ✅ **MEM-1 · CONECTADO 2026-07-01 (F3 + M2).** Las memorias ya se conectan: F3 puso 4 FKs
      nullable a `personas` (perfil/temas/miembros/episodes) + backfill; M2 cableó el grafo navegable
      (concepto→episodios reales, aislado por sesión) → las funciones huérfanas del grafo
      (episodios_de_concepto/turnos_por_seq) se enchufaron a la recuperación. La memoria episódica y
      la conceptual (grafo) YA se entrelazan en la cascada. --- (texto original abajo) ---
      Hoy
      `episodes_events`, `for3s_kg`, `sessions`, `perfil_usuario`, `hilo_status` viven en el mismo
      Postgres pero SIN relaciones formales (foreign keys) ni un índice/capa maestra que las una.
      Cada módulo las lee por separado y las pega en conversation.py. Quedó así por construir
      hito-por-hito sin diseño unificador. ⚠️ Brian: "si son memorias deberían estar conectadas, o
      debería existir algo capaz de mejorar esta estructura". En un cerebro la memoria episódica /
      semántica / conceptual están ENTRELAZADAS (un recuerdo activa conceptos relacionados); aquí
      están en silos. → Diseñar una capa que las relacione (FKs + índice maestro + recuperación
      cruzada). Cruza con PR1 (claridad) y MEM-3.

- [x] ✅ **MEM-2 · TEMAS DE EQUIPO CONSTRUIDOS 2026-07-01 (F5, camino B) — EN PRODUCCIÓN.** Ya existen
      temas COMPARTIDOS de equipo: `/tema equipo <nombre>` entra a un canal compartido `eq:<id>:<tema>`
      donde todos los miembros ven/escriben lo mismo (como Slack); `/tema salir` vuelve al hilo privado.
      Control de acceso fail-closed (imposible entrar al tema de otro equipo), aislamiento verificado.
      Los temas PRIVADOS por persona siguen intactos. --- (texto original abajo) --- Aclaración: el "general"
      privado por persona YA existe (Brian=`brian`, Sme G=`tg-<id>`, hilos distintos y aislados —
      el diagrama de PR4 los dibujaba mal, apuntando ambos a una caja "general"; CORREGIR el
      diagrama). Lo que NO existe y Brian quiere: que un TEMA pueda ser COMPARTIDO entre personas
      (Brian crea un tema, Sme G lo ve y se suma al MISMO hilo, colaboran juntos — como un canal de
      Slack). Hoy los temas son privados por persona (`brian:backend` ≠ `tg-<id>:backend`, no se
      ven). El único espacio "común" hoy es el CONOCIMIENTO (grafo), no un hilo de conversación
      compartido. → Diseñar "temas de equipo" (hilo compartido) además del general privado por
      persona. Cruza con H8 (equipo) y MULTI-INSTANCIA.

- [x] ✅ **MEM-3 · CASCADA CONSTRUIDA 2026-07-01 (M1+M3+M4) — EN PRODUCCIÓN.** La recuperación ya no
      es 5 volcados en paralelo: M1 corta lo irrelevante (el grafo trae solo lo del tema), M3 encadena
      (la semántica informa qué conceptos del grafo traer), M4 unifica el ensamblaje en
      `memoria.recordar()` (semántica→grafo→episodios en 1 punto). ✅ DEUDA FINA CERRADA 2026-07-02
      (commit 10f63a9): recordar() recibe history y absorbe también línea-de-tiempo + retomar → el
      bloque de memoria inicial completo en 1 punto (verificado byte-a-byte). hilo_status y perfil se
      quedan en send() a propósito (su orden entre capas no-memoria importa). **MEM-3 cerrado del todo.**
      --- (texto original abajo) --- Brian: "es atacar al
      cerebro por 5 frentes a la vez". Hoy episódica + semántica + grafo + perfil + hilo_status
      apuntan TODAS a conversation.py que las junta de golpe en el prompt → ruido, menos precisión,
      más tokens. Un cerebro real recupera en CASCADA/jerárquico (hipocampo→corteza): cada capa
      REFINA lo de la anterior antes de pasar a la siguiente, hasta producir UN contexto limpio y
      preciso. → Rediseñar la recuperación de memoria como filtros encadenados (episódica → destila
      → semántica → enriquece → grafo → contextualiza → perfil → contexto final), no 5 volcados en
      paralelo. Es la mejora de PRECISIÓN más grande de la memoria. Cruza con H10-PLANEA (confianza)
      y el DMN (consolidación).

- ✅ **Aclarado (NO es problema):** la AUDITORÍA (`audit_events`) está separada A PROPÓSITO y debe
      seguir así. NO es "memoria para pensar" — es la caja negra inmutable (seguridad/forense). En
      el cerebro sería el registro, no el razonamiento. Bien diseñada.

> **Resumen:** las 3 (MEM-1 conectar, MEM-2 temas de equipo, MEM-3 cascada) = la capa de memoria
> necesita un REDISEÑO para ser un cerebro de verdad (conectada + jerárquica + en cascada), no 5
> silos. Es una RONDA de diseño. Relacionado: memoria [[project_rediseno_memoria_cerebro]] ·
> PR4 (la auditoría que lo destapó) · H5/H6 (memoria actual) · PR1 (claridad).

---

## 🎓 ENTRENAMIENTO — ✅ EJECUTADO E0→E5b (2026-07-05) — solo queda el CIERRE FINAL

> **✅ ESTADO REAL (2026-07-05):** el hito se EJECUTÓ COMPLETO sobre **@For3s_Brian_bot**
> (instancia `brian`, el 2º For3s OS del server — PERSONAL de Brian; Foresito=empresa intacto):
> **31,576 episodios** cronológicos (ene→may, fecha ORIGEN real, 0 secretos crudos) + **15 skills
> vivas** + **38 secretos al vault** + identidad Fruterito en persona/ (gate Brian) + manifiesto
> **11,664/11,664 decididos (0 pendientes)**. Digestión: 20 pasadas CLS manuales = 49% consolidado
> (669 conceptos), cola 16,143 al CLS nocturno. 7 bugs de producto cazados (migr 033/034, FK
> personas, incluir_import, escaping Cypher, KEK efímera, plantilla instancia).
> **Reporte completo: `work/Entrenamiento_Ejecucion_Reporte.md`** · flujo/plan en Cuerpo/.
>
> **⏳ CIERRE FINAL pendiente (lo de CÓDIGO ya se hizo 2026-07-16):**
> - [x] ✅ **(3) microglía ON en brian** — activada 2026-07-16 (`FOR3S_MICROGLIA_CONFIRMAR=true`).
>   Dry-run previo: 240 candidatos de 21,674 vivos (1.1%), todo basura técnica del E6 (hooks git,
>   .json sueltos). Soft-delete recuperable; corre en el ciclo nocturno.
> - **⏳ QUEDA (depende de Brian/tiempo, NO código):** (1) verificar cola nocturna · (2) examen
>   global ~40 preguntas (tras 2-3 noches de digestión) · (5) **974 fotos medianas a visión**
>   ("tarda demasiado"; por tandas ~150 con `e6-vision`, reanudable) · (6) E6-F5 audio + F6 cierre E6
>   · (7) GitHub PAT para brian (opcional). El version bump no urge (se hará al cerrar E6 completo).

*(Contexto histórico de la visión y el plan original ⬇️ — E1-E4 de abajo = ejecutados)*

> **La visión (Brian):** Brian tiene **6 agentes OpenClaw** que entrenó por meses (un mar de
> conocimiento, contexto, memorias y herramientas) y que por temas económicos ya no usa. La meta:
> **deshacer/desglosar a los 6 agentes a profundidad** — leyéndolos archivo por archivo, tomando
> notas de TODO — y usar ese conocimiento como ENTRENAMIENTO para mejorar For3s OS. Resultado final:
> **pasar de tener 6 agentes a tener UNO SOLO (For3s OS / Foresito) que contenga TODO** — sus
> memorias, episodios, conocimiento. "Debes de tener 6 agentes → vamos a tener 1 pero con For3s OS."
>
> ⏸️ **REGLA LOCKED:** NO empezar el entrenamiento hasta que Brian diga "ya estamos listos".
> PRIMERO hay que terminar y PULIR a profundidad TODOS los pendientes (PR1-PR10 profesionalización,
> PR4, etc.). El entrenamiento es la recompensa final, después de tener For3s sólido como producto.

**✅ FASE 0 HECHA (2026-06-29): material ya en el servidor.** Todo copiado a `~/entrenamiento/`
(en el HOST de for3s, FUERA de contenedores, fuera de todo):
- `~/entrenamiento/Fruterito-principal/` (291M, 5786 archivos — la copia de `C:\...\Downloads\.openclaw` de Windows)
- `~/entrenamiento/Fruterito-wsl/` (194M, 5878 archivos — la copia de `~/.openclaw` del WSL2)

**Los 6 agentes REALES (verificado por identidad + sesiones, 2026-06-29):**
| Agente | Carpeta | Memoria | Entrenamiento |
|---|---|---|---|
| 🍍 Fruterito Personal (DevRel) | Fruterito-wsl/agents/main + Fruterito-principal/agents/main | 40 sesiones · **6045 turnos** · 23MB | 🟢🟢 mucho |
| 🍊 Fruterito Empleado (Product Lead→CEO) | Fruterito-wsl/workspace-empleado | **708 docs .md** | 🟢🟢 muchísimo conocimiento |
| 🔥 For3s Design | Fruterito-wsl/workspace-for3s-design | 16 docs .md (identidad rica) | 🟡 medio |
| 📰 Watchdog | Fruterito-principal/agents/watchdog | 17 sesiones · **20749 turnos** · 17MB | 🟢🟢🟢 el que más conversación |
| 🔴 Cipher | Fruterito-wsl/agents/cipher | 2 sesiones · 61 turnos | 🔴 casi sin usar |
| 🔵 Helix | Fruterito-wsl/agents/helix | 2 sesiones · 107 turnos | 🔴 casi sin usar |

- **2 formatos de memoria:** sesiones `.jsonl` (conversación cruda → mapea a `episodes_events`)
  · docs `.md` (conocimiento destilado → mapea a skills/conceptos del grafo).
- ⚠️ **SECRETOS:** hay `credentials/`, `device.json` (llaves privadas) y un botToken de Telegram
  en texto plano. NUNCA deben entrar a la memoria de Foresito — son credenciales, no conocimiento.

**Plan a futuro (debatir tipo Ronda cuando Brian dé luz verde):**
- [ ] **E1 · Desglosar agente por agente a profundidad** (leer TODO, tomar notas de cada uno).
      Prioridad por volumen: Fruterito Personal + Watchdog + Fruterito Empleado (el 99% del mar);
      Cipher/Helix casi vacíos (opcional).
- [ ] **E2 · Mapear cada cosa a su capa de For3s** (igual arte que la migración de Foresito):
      sesiones .jsonl → episodes_events (+ re-embeber + consolidar al grafo) · docs .md →
      skills/conceptos · herramientas = NO se importan, se reconstruyen aparte (otro trabajo).
- [ ] **E3 · Curar antes de aprender** (calidad sobre cantidad; NO meter todo de golpe al autogen
      — el governor H11 frena, pero hay que filtrar qué vale la pena para no generar skills basura).
- [ ] **E4 · Importar a Foresito** con lo ya construido (APRENDE H12 + autogen + curación nocturna
      consolidan al grafo). Resultado: 6 agentes → 1 For3s OS con todo.
- Cruza con: PR8 (sistema de entrenamiento/importar agentes) — de hecho ESTO es PR8 a fondo ·
  la migración de Foresito (mismo arte de mover memoria sin perder) · H5/H6 (memoria+consolidación).
- Refs: material en `~/entrenamiento/`. Memoria: [[project_entrenamiento_6_agentes]].

---

## 🧬 BRECHAS OPENCLAW → PENDIENTES A DESARROLLAR (Brian 2026-07-04) — registrados, NO desarrollar aún

> **Origen:** comparación profunda For3s OS vs OpenClaw (`docs/analysis/Comparacion_For3s_OS_vs_OpenClaw_Construccion.md`,
> ambos lados verificados: material real de OpenClaw + código vivo de For3s). Brian: "todos estos
> márcalos como pendientes que vamos a desarrollar… AHORITA NO los vamos a desarrollar, pero
> déjalos como pendientes." Sin fecha — Brian marca el momento. Cada uno merece su mini-diseño
> (Fases F) al arrancarlo. Detalle/contexto de cada brecha: doc de comparación §1-§5.

### 🔄 ESTADO
- [ ] **OC-E1 · /reset ligero de conversación** — borrón del CONTEXTO conversacional del hilo
      conservando memoria/perfil (hoy /reiniciar es del SERVICIO, no del hilo).
- [ ] **OC-E2 · Sesiones aisladas desechables** para trabajo programado/subagentes — cada corrida
      = mini-sesión que muere (`sessionTarget: isolated` de OpenClaw). ES la pieza que necesita el
      CRON CONVERSACIONAL (§FUTURO línea ~2028) — construirlas juntas.
- [ ] **OC-E3 · Trazar cambios de modelo/razonamiento EN el hilo** — hoy /model cambia global y no
      queda registrado en la conversación (OpenClaw: eventos model_change/thinking_level_change).
- [ ] **OC-E4 · Snapshot de skills/estado por sesión** — qué skills/config veía el agente en ese
      momento; para depurar "por qué respondió así" (OpenClaw: skillsSnapshot en sessions.json).

### 📡 COMUNICACIÓN
- [ ] **OC-C1 · Multi-canal (Discord PRIMERO)** — era la sala de máquinas del agente dev (guilds
      con permisos por canal). = el pendiente ⭐ MULTI-CANAL de §FUTURO (línea ~2036), ahora con
      referencia concreta: config `channels.discord` de openclaw.json (guilds/channels/requireMention).
- [ ] **OC-C2 · Hilos nativos del canal → temas** — mapear topics de Telegram (y threads futuros)
      a temas/sesiones: `message_thread_id` → `sesion_de(uid, tema)`. El rail de temas YA existe,
      falta el cable (hoy telegram_channel.py ni lee message_thread_id).
- [ ] **OC-C3 · Tool `message` proactiva** — que el agente pueda escribirle al dueño por decisión
      propia (resultado de trabajo, hallazgo), gobernada por governor + allowlist. Hoy solo alertas
      cableadas (health). OpenClaw: tool message, 64 usos reales en dev.
- [ ] **OC-C4 · Streaming/edición parcial de respuestas largas** — ver crecer la respuesta
      (OpenClaw: `streaming: "partial"` editando el mensaje). UX.
- [ ] **OC-C5 · Salida de archivos al chat** — generar y MANDAR .md/.docx/.pdf (send_document).
      For3s ya crea archivos en el sandbox pero no puede entregarlos.
- [ ] **OC-C6 · Entrada de VOZ** — revertir la decisión de diseño "audio fuera" (multimodal.py):
      transcripción de notas de voz. (Ya existía nota en §FUTURO sobre voz — unificar al construir.)
- [ ] **OC-C7 · Multi-cuenta/bindings** — varios bots (personal/dev/watchdog) sirviendo agentes o
      modos distintos desde UNA instalación (OpenClaw: channels.accounts + bindings agente↔cuenta).
      Hoy eso exige multi-instancia completa.

### 🗺️ MAPEO DE INFORMACIÓN / MEMORIA
- [ ] **OC-M1 · ⭐ Diario/bitácora propia del agente** — que Foresito ESCRIBA su día ("qué aprendí,
      qué quedó pendiente") en lugar legible; casa natural: persona/mente-os/Doc/. La pieza de
      OpenClaw con más alma (diarios memory/AAAA-MM-DD.md + archivado). El diario_cambios actual
      solo registra auto-mods de código. Rail: DMN nocturno puede redactarlo.
- [ ] **OC-M2 · Learnings por tema/proyecto** — "learnings.md del proyecto X": resumen curado y
      ACUMULATIVO por tema (OpenClaw: memory/acompanante/<proyecto>/learnings.md). Rails: temas +
      tema_estado (C1) ya existen.
- [ ] **OC-M3 · Índice de memoria curado de largo plazo** — el "MEMORY.md" de Foresito: resumen
      maestro SIEMPRE presente que el propio agente mantenga. Hoy inyectamos lo RELEVANTE al turno;
      falta lo PERMANENTE elegido por él (OpenClaw: 15K chars siempre en prompt).
- [ ] **OC-M4 · memory_search como TOOL del loop** — que el AGENTE decida buscar más memoria a
      mitad del razonamiento (hoy la recuperación corre 1 vez, antes del turno).
      `memoria.recordar()` ya es la fachada — exponerla como tool.
- [ ] **OC-M5 · Skills como paquetes portables + marketplace** — skills con scripts/assets
      ejecutables, instalables/publicables (el clawhub de OpenClaw). Las nuestras son conocimiento
      en BD, no herramientas empaquetadas. Visión producto (grande).

- *(Del mismo análisis quedaron 2 brechas menores de BD/debug NO incluidas en la lista de Brian:
  systemPromptReport por turno + exportar memoria a .md legible — viven en el doc §2, sumar si él quiere.)*
- Cruza con: §FUTURO (cron conversacional OC-E2 · multi-canal OC-C1 · voz OC-C6 — mismos temas,
  NO duplicar al construir) · HITO ENTRENAMIENTO (las radiografías son la fuente) · Identidad Viva
  (persona/mente-os = casa de OC-M1/M2/M3).
- ⚠️ **Varios OC-* tienen MATICES añadidos por el análisis de Hermes** → ver §BRECHAS HERMES
  (justo abajo): al construir un OC-*, leer también su ampliación HG-*.

---

## ⚔️ BRECHAS HERMES → PENDIENTES A DESARROLLAR (Brian 2026-07-04) — registrados, NO desarrollar aún

> **Origen:** comparación profunda de CONSTRUCCIÓN For3s OS vs hermes-agent
> (`docs/analysis/Comparacion_For3s_OS_vs_Hermes_Construccion.md` — repo real clonado: 2,823 .py, 25+
> plataformas, ~60 tools). Brian: "registra todo lo que nos falta como pendientes, TODOS."
> Sin fecha — Brian marca el momento. Cada uno con su mini-diseño (Fases F) al arrancar.
> ⭐ **Máxima validación**: 3 brechas coinciden EXACTO entre OpenClaw y Hermes → agente autor
> de su memoria legible · cron conversacional con sesiones aisladas · multi-canal/proactividad/voz.

### Ampliaciones a brechas YA registradas (no duplicar — construir JUNTO con su OC-*)
- [ ] **HG-1 → amplía OC-C1 (multi-canal):** hacerlo con el patrón Hermes — capa de canal como
      CONTRATO formal (clase base + registry + UN gateway para N plataformas, `ADDING_A_PLATFORM.md`)
      + **continuidad cross-canal** (la MISMA conversación sigue de Telegram a consola a Discord;
      sesiones etiquetadas por source en un store único).
- [ ] **HG-2 → amplía OC-C6 (voz):** no solo ENTRADA (transcripción); también **SALIDA — TTS y
      voice_mode interactivo** (Hermes: transcription_tools + tts_tool + voice_mode).
- [ ] **HG-3 → = OC-C3/C4/C5** (send_message proactivo · streaming · media out) — sin cambios,
      Hermes confirma las tres.
- [ ] **HG-5 → amplía OC-M4 (memory_search tool):** además de memoria semántica bajo demanda,
      tool para HOJEAR la propia historia conversacional cruda (Hermes session_search: 3 modos
      discovery/scroll/bookends sobre FTS, costo LLM cero; nosotros lo haríamos sobre Postgres).
- [ ] **HG-6 → amplía OC-M1/M3 (memoria curada del agente):** matiz de diseño CLAVE de Hermes —
      el MEMORY/USER curado entra al prompt como **snapshot CONGELADO por sesión** (escrituras a
      mitad de sesión van a disco pero NO tocan el prompt → preserva el prefix cache; refresca al
      siguiente arranque). Copiar este patrón al construir OC-M1/M3.
- [ ] **HG-9 → amplía OC-M5 (skills-paquete/marketplace):** con el modelo de seguridad de Hermes:
      lockfile de PROCEDENCIA + cuarentena + auditoría AST de skills instaladas (skills_guard) +
      estándar abierto agentskills.io.
- [ ] **HG-10 → amplía OC-E2/cron conversacional:** sumar **catálogo de SUGERENCIAS** (el agente
      propone automatizaciones: suggestion_catalog) + blueprints (recetas) + output persistido por
      corrida (`cron/output/<job>/<ts>.md`) + delivery del resultado a cualquier canal.
- [ ] **HG-17 → ya en §EXTRAS como H·BYOK** (multi-proveedor de modelos) — Hermes lo valida
      (adapters Anthropic/Bedrock/Gemini/OpenAI + `hermes model` en vivo + credential_pool).

### 🆕 Brechas NUEVAS (no estaban en OpenClaw)
- [ ] **HG-4 · TUI de consola seria** — nuestro modo consola es plano; Hermes trae TUI real:
      autocomplete de comandos, multiline, historial, interrupt-and-redirect, streaming de tool
      output. (chica)
- [ ] **HG-7 · ⭐ NUDGES de persistencia y skills EN el turno** — el loop de conversación empuja
      periódicamente al agente a (a) persistir conocimiento importante y (b) crear skill tras
      tarea compleja (skill_nudge_interval). Hoy nosotros esperamos a la NOCHE (DMN); el nudge
      cierra el loop de aprendizaje en caliente. (media, MUCHO valor)
- [ ] **HG-8 · ⭐ CURATOR de skills por inactividad** — agente de fondo que se dispara cuando el
      sistema está idle (no cron) y MANTIENE las skills creadas: consolida duplicadas, archiva
      muertas, parcha rotas, con estado propio. Nuestro DMN crea skills pero nadie las mantiene.
      Rail: dmn_idle ya existe. (media)
- [ ] **HG-11 · todo/kanban como TOOL del agente** — que el AGENTE gestione su lista de trabajo
      como herramienta del loop (Hermes: todo_tool + kanban con watchers). Nuestro tema_estado
      (C1) es comando del USUARIO; falta la versión agente. (chica)
- [ ] **HG-12 · clarify estructurado como tool** — H10 metacognición YA detecta baja confianza;
      falta exponer "pedir aclaración con opciones estructuradas" como tool del loop en vez de
      solo texto libre. (chica)
- [ ] **HG-13 · checkpoints de archivos en el sandbox** — snapshot automático antes de que el
      agente edite un archivo (checkpoint_manager) → deshacer barato por archivo. (chica)
- [ ] **HG-14 · ⭐ execute_code que llama TOOLS vía RPC** — la idea más potente de Hermes: el
      modelo escribe UN script Python que invoca las tools del agente (stub autogenerado, socket)
      → un pipeline de N turnos se colapsa a 1 turno con costo de contexto CERO. Encaja natural
      con nuestro sandbox por HTTP (EC-3). (grande)
- [ ] **HG-15 · toolsets restringidos por contexto** — qué tools ve el agente según canal/rol/
      subagente (Hermes: toolsets configurables + toolset restringido por hijo delegado). Hoy
      nuestro tool-loop es uno solo; cruza con H8 (subagentes) y multiusuario (roles). (media)
- [ ] **HG-16 · browser / computer-use / web_search / generación de imagen** — por partes:
      web_search como tool del loop (hoy solo web_fetch reactivo) → browser real (Hermes:
      Camoufox/CDP con supervisor) → computer_use → image/video gen. (grande, por fases)
- [ ] **HG-18 · i18n del agente** — respuestas/UI en idioma configurable (Hermes: locales/).
      Hoy Foresito es es-MX nativo; importa para DISTRIBUCIÓN. (chica)

- **Lo que For3s tiene y Hermes NO** (no perder el piso, verificado en su código): grafo AGE con
  consolidación+olvido · DMN generativo · metacognición · governor · audit inmutable + KEK ·
  multi-USUARIO roles/gate · equipo specialists+synthesizer · auto-modificación con guardián ·
  /salud E2E · multi-instancia.
- Cruza con: §BRECHAS OPENCLAW (arriba — los OC-*) · §EXTRAS (H·BYOK=HG-17, EC-EXTRA-1 backend
  SSH) · §FUTURO (cron/multi-canal/voz) · H8 (HG-15) · H10 (HG-12) · DMN (HG-7/HG-8).

---

## 🚨 PROFESIONALIZACIÓN — "ser PRODUCTO de verdad, no MVP" (Brian 2026-06-28) — CRÍTICO

> **El hallazgo de Brian (tras migrar Foresito a contenedores):** For3s OS *funciona*, pero
> NO se comporta ni se gestiona como un producto. Falta claridad, observabilidad, datos,
> profesionalismo. "Ya funciona, falta profesionalismo y claridad." Son 10 frentes (PR1-PR10).
> ⚠️ NO resolver de golpe — atacar uno por uno, debatir→decidir→código→testeo. Varios son
> CRÍTICOS para soltar a testers/clientes. Origen: la migración destapó bugs (owner/sesión)
> que NO se detectaron por falta de monitoreo → confirma la urgencia de PR2.

- [x] ✅ **PR1 · CLARIDAD del código — HECHO 2026-06-29.** Entregable: `memory/archive/PR1_Mapa_Codigo_Claridad.md`
      — el mapa de REFERENCIA del código, verificado POST sesión de bugs (refleja todo lo arreglado).
      Contiene: estado del producto (47 módulos, 7 contenedores, 23 migraciones) · las 5 CAPAS del
      código (entrada/orquestación/dominio/base/utilidades) · tabla de los 47 módulos uno por uno
      (líneas · qué hace · usado_por · estado 🟢/🟠/🔴) · capacidades CONSTRUIDAS pero SIN CABLEAR
      (las funciones de grafo episodios_de_concepto/etc. — clave para MEM-3) · las 23 migraciones ·
      los 7 contenedores (con los hermanos de red) · los bugs de la sesión por módulo afectado ·
      HALLAZGOS de deuda. ⚠️ Hallazgos clave: (1) version.py DESACTUALIZADO (v0.12.0/H10, no refleja
      PR2/PR10/bugs) → tarea: subir versión · (2) telegram_channel.py = 3090 líneas/usa 29 módulos =
      cuello de complejidad (dividir en PR9) · (3) sandbox muerto · (4) llm.py lo usan 12 (núcleo
      crítico). Conclusión: código SANO (capas ordenadas, casi todo conectado); la sesión mejoró la
      salud. Base para PR7 y PR8. Cruza con PR4-C.
- [x] ✅ **PR2 · 🔴 SALUD / MONITOREO — COMPLETO 2026-06-30 (incl. PR2.3 Grafana).** Construido `health.py`
      (monitoreo END-TO-END, opción "infiere por efectos", sin tablas nuevas ni tocar el cron) +
      comando `/salud` (solo dueño). VIGILA TODO lo que Brian pidió: 🔗 LA LÍNEA mensaje→memoria
      (message_in/out gap 24h, KEK/secrets, metacognición, línea viva) · 🧠 subsistemas (BD, backup
      reciente, decay, embeddings, audit chain) · 📊 grafo (crece + catálogo AGE) · 🔌 integraciones
      (GitHub MCP read+write, render — los hermanos por HTTP) · 🌙 nocturno (DMN, decay aplicado) ·
      💰 TOKENS por persona + global (honesto: avisa del legado sin autor) · 🧵 hilos (reales vs test,
      actividad). VERIFICADO en vivo: reporte completo corre, todo ✅ verde (prueba de que los 8 bugs
      de hoy quedaron arreglados). 🧹 De paso limpió basura: nodos de prueba del grafo (WrapTest/
      TestNode/FixTest del diagnóstico de BUG-8). Cada check es defensivo (una falla no rompe el
      reporte).
      ✅ **PR2.1b HECHO Y VERIFICADO 2026-06-29:** vistas detalladas `/salud <sección>` (linea,
      tokens, nocturno, grafo, integraciones, subsistemas, hilos) vía `health.reporte_seccion` —
      para no saturar el chat. ⭐ Antes de construir AUDITÉ las fuentes y cacé inconsistencias:
      (1) 🔴 mi salud_linea miraba la señal MUERTA `gh_fetched` (del flujo viejo borrado) en vez de
      la REAL → arreglado: ahora mide el uso de GitHub por `message_out.detail.tools` (verificado:
      "último uso hace 58h", no los falsos 16 días). RESULTÓ que NO había bug en los hermanos —
      conversation SÍ audita las tools en message_out + las guarda en gh_resources; el bug era de mi
      health.py (señal obsoleta). (2) salud_tokens ahora avisa de 53 respuestas con tokens=0 (sin
      medir, honesto). (3) salud_nocturno honesto: dmn_corridas NO tiene timestamp (solo ms) → dice
      "sin fecha, ver PR2.2" + infiere backup por efecto (disco). Verificado en vivo las 3 vistas.
      ✅ **PR2.2a HECHO Y VERIFICADO 2026-06-29:** tabla `cron_corridas` (migración 023) con
      TIMESTAMP real (job, ok, resultado, ms, creado_at) + decorador `@registra_corrida(nombre)` en
      tasks.py aplicado a 7 jobs (backup, cls, status, relevance, microglia, curar_skills, dmn_noche
      — NO dmn_idle que corre cada 30min) que registra cada corrida sin tocar la lógica del job +
      `salud_nocturno` ahora LEE cron_corridas (fecha real por job: "backup hace 0h ok", distingue
      ok/fail, honesto si un job no ha corrido). ANÁLISIS previo confirmó la raíz: NINGÚN job_*
      registraba corrida (solo logs efímeros de Arq); el worker SÍ puede leer el bot_token (KEK) →
      la conexión para alertar existe. Verificado: backup+relevance registraron en cron_corridas con
      ms y timestamp; /salud nocturno los muestra. Worker rebuildeado y sano.
      ✅ **PR2.2b HECHO Y VERIFICADO 2026-06-29 → PR2 prácticamente COMPLETO:** `job_health_check`
      nocturno (cron 04:30 Mx, tras todos los jobs) que corre health.reporte_completo y, SI hay 🔴
      FALLAS (solo fallas, NO avisos ⚠️ → cero spam, decisión Brian opción a), ALERTA al dueño por
      Telegram. Helper `_alertar_dueno(texto)` (worker → API Telegram: lee owner_id del json montado
      + bot token por KEK). VERIFICADO E2E: (1) con todo OK → "todo OK (sin alerta)" no molesta; (2)
      simulé falla (paré render) → "2 fallas → alerta ENVIADA" + llegó el mensaje 🚨 a Telegram con
      las líneas 🔴. El círculo del monitoreo CERRADO: un subsistema roto YA NO pasa en silencio (la
      lección de los 9 bugs). Análisis previo confirmó la cadena sin bugs: worker ve owner_id en
      /app/.for3s, lee token KEK, sendMessage HTTP 200, health.reporte corre en worker y alcanza los
      hermanos por red. Registrado en cron_corridas con el decorador. 7 contenedores sanos.
      ✅ **PR2.3 GRAFANA HECHO Y VERIFICADO 2026-06-30 → PR2 COMPLETO.** Grafana como 8º contenedor
      hermano (grafana/grafana:11.3.0) en la red for3s_net, datasource PostgreSQL PROVISIONADO
      (docker/grafana/datasources/for3s.yml) + dashboard "For3s OS — Salud & Actividad" provisionado
      con 4 paneles (actividad turnos/día · tokens/día · ciclo nocturno por job ok/fallo · audit por
      tipo). SOLO 127.0.0.1:3000 (no expuesto a internet, se accede por Tailscale — mantiene la regla
      "Grafana público eliminado"). Verificado E2E vía API: "Database Connection OK" + dashboard con 4
      paneles cargado + Grafana health 200. 🔍 La curiosidad (Brian: "hay cosas mal conectadas") cazó
      antes de montarlo una INCONSISTENCIA real: `job_dmn_idle` era el ÚNICO de los 9 jobs SIN
      `@registra_corrida` → sus corridas eran invisibles en cron_corridas/salud/Grafana. ARREGLADO
      (ahora los 9 registran). Resto de datos verificados consistentes (ms poblado, audit ts 0 nulos,
      tokens con el 7% ya avisado). ⚠️ EN EL SERVER — repo/GitHub al día tras sincronizar hoy; este
      cambio (Grafana+dmn_idle) pendiente de sincronizar cuando Brian lo ordene. Cruza con H14 OJOS.
      → **PROFESIONALIZACIÓN: 8/10** (PR1 PR2 PR3 PR4 PR6 PR7 PR10 + PR2.3). Quedan PR5 (necesita
      usuarios), PR8 (entrenamiento, no antes de pulir), PR9 (UX/telegram_channel) + HA-3 (H7 futuro).
- [~] **PR3 · 🔴 DATOS / ANALÍTICA — PR3.1 HECHO Y VERIFICADO 2026-06-30.** Construido `analytics.py`
      + comando `/datos` (dueño): 5 secciones REALES — actividad turnos/día · consumo tokens/día +
      total · repos recurrentes · capacidades usadas · actividad por persona. 🔍 La auditoría
      ELEMENTO POR ELEMENTO (curiosidad, como pidió Brian) evitó DATOS FALSOS: (1) gh_resources tiene
      1 fila POR ARCHIVO (515 'file') no por consulta → "EVVM 98 veces" habría sido FALSO (inflado
      x5); se cuenta por SESIONES distintas (→ "1 consulta", real) + filtra repo '/' vacío. (2) tokens:
      avisa "7% sin medir" (no finge exacto). (3) por persona: avisa "563 turnos legado sin autor".
      (4) solo cuenta turnos vivos (la basura soft-deleted no infla). Verificado E2E con datos reales.
      Distinto de /salud tokens (estado) → esto es TENDENCIAS/uso. ⏳ FALTA solo PR3.2/PR5 (métricas
      de negocio: retención, etc. — cuando haya más usuarios). Sin esto Brian "no sabía nada del uso".
- [x] ~~PR3 (texto original — YA RESUELTO por PR3.1)~~ **DATOS / ANALÍTICA (no sabemos NADA).** No conocemos: consumo (tokens/costo),
      temas más recurrentes, uso por usuario, qué se usa y qué no, métricas de producto. "Sabemos
      que funciona pero no sabemos nada." Necesario como empresa Y como herramienta. Cruza con
      PR5, H9-d (ROI), H14.
- [~] **PR4 · 🔴 BUGS de memoria y usuarios + AUDITORÍA carpeta-por-archivo.** Hay varios bugs
      en memorias/usuarios (ej. el owner→sesión vacía de la migración; los 16 turnos huérfanos en
      tg:1923367928; sesión 'brian' vs tg:id del dueño). Necesita una SESIÓN DE ANÁLISIS A DETALLE:
      carpeta por carpeta, archivo por archivo, cómo se conecta cada uno con otro y por qué.
      Se dividió en 3 PARTES (Brian 2026-06-28, ir UNO POR UNO, punto por punto):
      - **Parte A · BUGS de memoria/usuarios** (diagnosticar los fallos vivos): owner→sesión vacía
        (parcheado en migración pero diseño frágil → PR6) · 16 turnos huérfanos en tg:1923367928 ·
        asimetría sesión 'brian' (dueño) vs tg:<id> (miembros). AUDITAR + listar (arreglar = puntos
        aparte después). ⏳ pendiente.
      - **Parte B · AUDITORÍA del FLUJO memoria/usuario — ✅ HECHA 2026-06-28.** Entregable
        `memory/archive/PR4_Flujo_Usuario_Memoria.md` (estilo godinez-studio/onboarding-flow, verificado
        contra el código real). Tiene **10 diagramas mermaid** (todos válidos para GitHub) +
        caso de uso end-to-end "Un día con Foresito" (11 escenas) + diagrama de secuencia de un
        turno real. Cubre: flujo usuario · identidad/3 llaves · HILOS (persona×tema) · MEMORIA a
        detalle (5 capas + olvido) · interacción de TOOLS (GitHub MCP + write gate) · COMPONENTES
        H5-H12 · ciclo nocturno · governor.
      - **Parte C · AUDITORÍA TOTAL de los 46 módulos — ✅ HECHA 2026-06-28** (en el mismo doc).
        Contenedores (4) + grafo de dependencias USA/USADO_POR de los 46 módulos + tabla uno-por-uno
        + mapa por capas. 🔴 HALLAZGOS: `sandbox.py` = CÓDIGO MUERTO (nadie lo ejecuta, solo
        comentarios) · `relevance.py` = HUÉRFANO sospechoso (su columna se lee en microglía pero
        nadie importa el módulo → ¿el decay de memoria corre? posible bug silencioso de H6).
      - **Parte A · diagnóstico de bugs vivos — EN CURSO (2026-06-29).** Hallazgos confirmados:
        - 🔴 **BUG #1 CONFIRMADO: el DECAY de memoria está MUERTO (H6 incompleto).**
          `relevance.py` tiene `recalcular_relevance_lote()` pero **NADIE la llama** (búsqueda
          vacía en todo el repo) y `tasks.py` NO la tiene en el cron → el "Sub-paso 10" (conectar
          el recálculo al cron nocturno) quedó a medias. EVIDENCIA en la BD de Foresito: 515 turnos
          con relevance TODOS en el decil 10 (0.91-0.99, congelados desde el 22-jun) + 245 turnos
          nuevos con relevance NULL (nacen sin ella y nadie se la pone). La microglía LEE
          `relevance` (filtro `relevance IS NOT NULL AND relevance < X`) → nunca encuentra
          candidatos → **Foresito NUNCA olvida por relevancia** (solo 2 soft-deleted en 760). El
          refuerzo en caliente (veces_recuperado=195, last_accessed=234) SÍ vive; lo muerto es el
          recálculo en frío. ARREGLO (cuando Brian diga): agregar job al cron que llame
          recalcular_relevance_lote por sesión antes de la microglía (~15 líneas, conecta lo ya
          construido). ⏳ pendiente de arreglar (PR4-A solo diagnostica).
        - 🔴 BUG #2: `sandbox.py` código muerto (confirmado en Parte C) — decidir borrar/cablear.
        - 🟡 BUG #3: 16 turnos huérfanos en sesión `tg:1923367928` (del bug de la migración) — limpiar.
        - 🟡 BUG #4: owner frágil (json en cwd) — documentado, se arregla en PR6.
        - 🔴 **BUG #5 CONFIRMADO (GRAVE): el BACKUP automático está ROTO desde la contenerización.**
          Log del worker cada noche: `job_backup ● 'backup error: FileNotFoundError'`. Causa:
          `pg_dump` NO está instalado en la imagen `for3s-agent` (el worker corre ahí). `hacer_backup`
          lo llama por subproceso → falla siempre. **Foresito NO tiene backups automáticos desde que
          se contenerizó** (último real = manual 23-jun). ADEMÁS: aunque se arreglara pg_dump, la
          carpeta `~/for3s-backups` (→ `/root/for3s-backups` en el contenedor) NO está montada como
          volumen → el backup quedaría atrapado en el contenedor efímero (BUG #6). ARREGLO: (a)
          añadir postgresql-client a Dockerfile.agent + (b) montar volumen de backups al host + (c)
          activar offsite. CRÍTICO — es la red de seguridad.
        - 🟡 **BUG #8 (NUEVO): CLS consolida 0 conceptos.** Log: `job_cls ● 'clusters=3 conceptos=0
          marcados=0 (pendientes_eval=90)'`. La consolidación nocturna CORRE pero genera 0 conceptos
          (encuentra 3 clusters pero no los convierte). El grafo no crece desde ~28-jun. Investigar
          por qué (¿el LLM de CLS falla en el contenedor? ¿OAuth/system? ¿umbral de cluster?).
        - ✅ Lo que SÍ funciona del cron: job_status (4/4 hilos), job_curar_skills, job_dmn_idle, y
          el refuerzo en caliente (veces_recuperado=195, last_accessed=234 en la BD).
        - 📌 BARRIDO de funciones huérfanas hecho: confirmadas SIN usar en código ni tests:
          `episodios_de_concepto`, `recursos_de_repo`, `repos_de_owner` (kg navegación grafo),
          `get_last_repo`/`set_last_repo` (memory), `requiere_aprobacion` (equipo), `lint_archivos`
          (sandbox, solo test) — capacidades construidas pero desenchufadas (revisar en PR1).
        - ⚠️ PATRÓN DE FONDO: los 3 bugs graves (relevance, backup, CLS) son del CICLO NOCTURNO
          (H6/H9) y varios se rompieron/empeoraron con la CONTENERIZACIÓN. Nadie se enteró =
          confirma PR2 (falta monitoreo/salud). El cron "corre" pero produce basura silenciosamente.
        El nº real de módulos es **46** (no 45).
      - **Parte C · AUDITORÍA TOTAL de los 45 módulos, UNO POR UNO a detalle** (Brian 2026-06-28).
        Recorrer cada uno de los 45 módulos de `for3s_core/` (agent, aprende, audit, backup, cache,
        cli, concurrency, confidence, config, consolidator, conversation, cost_control, crypto, db,
        dmn, dmn_tasks, embeddings, equipo, gh_ficha, governor, handoff, hilo_status, kg, llm,
        mcp_client, md_html, memory, microglia, modelos, multiagente, multimodal, perfil, relevance,
        sandbox, secret_store, skills, specialists, subbloques, tasks, telegram_channel, temas,
        text_normalize, tiempo, tool_loop, version, web_fetch) documentando por cada uno: qué hace ·
        de quién depende (imports) · quién lo usa · estado (vivo/huérfano/parcial) · bugs/deudas.
        Es la versión COMPLETA de la auditoría (B es solo el subconjunto memoria/usuario). Entregable:
        `Doc/PR4_Mapa_Modulos_Completo.md`. ⏳ pendiente — empezar tras cerrar la Parte B. Cruza con
        PR1 (claridad: qué se conecta a qué) y PR7 (revisar cada H).
- [⏸️] **PR5 · DATOS de producto/empresa → MOVIDO a §EXTRAS** (2026-07-01). Diferido: necesita más
      usuarios. Detalle completo en la sección EXTRAS.
- [~] **PR6 · 🔴 MANEJO DE DUEÑOS — PR6.1 HECHO Y VERIFICADO 2026-06-30.** El owner era frágil
      (json suelto en cwd → la migración lo rompió). ✅ **PR6.1: persistencia robusta** — tabla
      `owner` en BD (migr 024) = FUENTE DE VERDAD (la BD siempre montada + viaja con backups); JSON
      como caché; OwnerStore con CACHÉ en memoria (no leer disco 18×/turno) + `sync_con_bd()` en
      setup (carga de BD + repara JSON) + `set_owner_bd()` (persiste en BD). CIERRA BUG-4 (verificado:
      sin JSON, el owner se recupera de la BD). 🔍 El análisis curioso confirmó: /start protege el
      owner (no se puede robar, solo si owner None) ✅; owner del bot = encargado del equipo ✅;
      get_owner leía disco 18×/turno → ahora cacheado. ⏳ FALTA **PR6.2** (futuro): transferencia de
      dueño, multi-owner/admins extra, recuperación explícita. Cruza con AUTO-CONCIENCIA y multi-tenant.
- [x] ✅ **PR7 · REVISAR A DETALLE CADA H (H1-H12) — COMPLETO 2026-06-30.** Pasamos lista a los 12
      hitos EN EL CONTENEDOR VIVO (sondas de solo lectura: BD+AGE+logs+audit), filosofía "completo en
      código ≠ funciona en el contenedor". Reporte maestro: `memory/archive/PR7_Revision_Hitos.md`. **Resultado:
      12/12 revisados · 11 ✅ funcionan · 1 🟡 parcial por diseño (H7) · 0 rotos.** Los 12 bugs siguen
      arreglados. ⭐ cadena audit íntegra (1576 eventos, 0 eslabones rotos). H5 grafo creció 35→63
      conceptos. H12 tiene 1 skill AUTO-generada por el DMN en uso.

  > 🔴 **PENDIENTES DE ANÁLISIS DE LOS H — lo que PR7 destapó y SIGUE por resolver (Brian pidió
  > registrarlos, 2026-06-30):** ninguno ROMPE la ejecución hoy, pero son deudas reales a atacar
  > uno por uno con la misma curiosidad. Atacar en sesión futura cuando Brian diga.

  - [x] ✅ **HA-1 · H8 · costo del equipo ahora visible en /datos — RESUELTO 2026-06-30 (commit 5afe6dc).**
        🔍 **PR7 reportó MAL este bug:** dijo "el equipo no escribe en audit". FALSO — el equipo SÍ tiene
        observabilidad RICA, pero en tabla DEDICADA `corridas_equipo` + `corrida_reportes` (no en
        audit_events; por eso PR7 no la vio): `handoff.registrar_corrida` guarda familia, n_specialists,
        n_ok, segundos, tokens_in/out por corrida Y por specialist. Hay 1 corrida real (cli/cli, 25-jun,
        5/5 ok, 7969 tokens). **El bug REAL (más sutil):** NADIE leía esa tabla (ni /datos ni /salud) →
        el costo del equipo era invisible (capacidad construida sin cablear, mismo patrón que las
        funciones huérfanas). FIX: nueva sección `datos_equipo()` en analytics.py → /datos muestra
        corridas/tokens/familia/éxito del equipo. Probado EN VIVO (reporte de 6 secciones OK + caso 0
        con rollback + agent reiniciado sano). Sincronizado agent=worker=local=GitHub.
  - [x] ✅ **HA-1b · CABLEADA 2026-06-30** — `handoff.ultimas_corridas()` ahora se usa en /diagnostico (sección "Equipo en tu hilo", solo metadatos de TU sesión = respeta aislamiento). Era huérfana (cazado al resolver HA-1, 2026-06-30).**
        Definida en handoff.py:89 ("qué analizó el equipo") pero NADIE la llama (ni código ni tests) —
        la otra mitad de la lectura del equipo nunca se cableó. Opciones: (a) cablearla a un comando
        tipo `/equipo` o a /diagnostico (mostrar las últimas corridas del hilo); (b) borrarla si no
        aporta. Menor, no urgente. Patrón recurrente: lecturas construidas y desenchufadas.
  - [x] ✅ **HA-2 · H8 · Sme G sin perfil — INVESTIGADO, NO ES BUG (2026-06-30).** Diagnóstico de
        lectura: (1) Sme G SÍ interactuó (26 turnos, 23-jun) — no es falta de actividad. (2) El
        cableado del modelado FUNCIONA para miembros: los 3 `Conversation()` (líneas 2092/2602/3122 de
        telegram_channel) pasan `telegram_user_id=user.id` para dueño Y miembro por igual; nunca llega
        None. (3) El modelado auto (`conversation.py:714`) es CONSERVADOR por diseño: solo guarda
        perfil cuando `detectar_afirmacion()` (perfil.py) encuentra una frase clara de auto-descripción
        ("soy backend", "prefiero X"). (4) Verificado en BD: Sme G NUNCA escribió una frase así (0
        mensajes con soy/prefiero/trabajo/me dedico) → 0 capturas → sin perfil. **CORRECTO** (no
        inventa perfiles sin señal). Brian tiene perfil porque se fijó explícito (rol "tu dueño").
        💡 **Mejora futura opcional (NO bug):** inferir el perfil del estilo/contenido de los turnos,
        no solo de afirmaciones explícitas → cruza con REDISEÑO MEMORIA + paridad Hermes P1 (modelar
        al usuario). Decisión de diseño, no urgente.
  - [⏸️] **HA-3 · H7 enrutamiento automático → MOVIDO a §EXTRAS** (2026-07-01). Diferido: su beneficio
        (ahorro de costo) no aplica a la suscripción plana; se retoma con API de pago. Detalle en EXTRAS.
  - [x] ✅ **HA-4 · RESUELTO 2026-06-30** — borrados todos los .bak del repo (incl. un .env.bak con 2 secretos) + creado .dockerignore (cubre pycache/bak/secretos) → la imagen ya no arrastra basura. ~10 archivos `.bak` horneados en la imagen del contenedor.**
        `telegram_channel.py.bak.pr10/pr103/pr2/pr6`, `tasks.py.bak/.bak.pr22`, `health.py.bak`,
        `mcp_client.py.bak`, `web_fetch.py.bak`, `version.py.bak` — basura de mis ediciones. NO afecta
        ejecución (Python importa el .py), pero ensucia la imagen y confunde auditorías. Borrar del
        repo/imagen. → mover a PR9 (UX/limpieza) cuando se ataque.
  - [x] ✅ **HA-5 · H12 · skills duplicadas + matcher mal diseñado — RESUELTO 2026-06-30 (en el server).**
        Brian intuyó "el sistema de skills tiene errores de reconexión y mal diseño, varios bugs" —
        CORRECTO. Investigación a fondo destapó 3 problemas reales (no 1):
        (1) **2 skills duplicadas** (deploy bot→server, una usuario id20 + una auto id21).
        (2) **FRENO 4 anti-duplicados era exact-match de nombre** → causa raíz: nombres distintos
            ('...-botservicio' vs '...-bot-en-servidor') no se detectaban como duplicado.
        (3) ⭐ **`buscar_relevantes` matcheaba por palabras sueltas ≥4 letras con OR** → frágil en
            AMBOS sentidos: falsos POSITIVOS (1 palabra común como 'servidor' inyectaba la skill) y
            falsos NEGATIVOS (no cruza idiomas: 'despliego el bot' NO matcheaba 'deploy bot servidor').
        (— bug de fechas ultimo_uso<creada = FALSA ALARMA mía, leí mal las columnas.)
        **FIX (raíz, no parche):** matcher SEMÁNTICO con embeddings BGE-M3 (la infra de H5):
        · migración 025 (columna embedding vector(1024) + índice HNSW en skills)
        · crear() genera embedding (defensivo: NULL si no hay modelo → fallback)
        · buscar_relevantes reescrito: distancia coseno, umbral 0.55, con FALLBACK al matcher por
          palabras (con umbral ≥1 hit nombre / ≥2 desc) si no hay embeddings
        · backfill de las 2 skills existentes
        · FRENO 4 endurecido: exact-match + similitud Jaccard de nombre ≥70%
        · deduplicado: skill auto (id21) → archived (recuperable); queda 1 activa (usuario id20).
        **Probado a fondo (5/6):** despliego/deploy/actualizar-producción ahora SÍ aplican (antes no);
        hola/capital-de-Francia se descartan; FRENO 4 bloquea duplicados similares. El 6º ('logs del
        servidor' dist 0.395) es borderline legítimo (la skill menciona logs) — Brian decidió aceptarlo
        (umbral 0.55, inyectar de más es barato). Agent+worker sincronizados, agent reiniciado sano.
        ⚠️ EN EL SERVER — repo local/GitHub pendiente de orden de Brian ([[feedback_flujo_server_primero]]).
        💡 Deuda menor restante: el FRENO 4 usa Jaccard de nombre (no embedding); podría usar el
        embedding de skill para dedup semántico aún más fino. No urgente.
  - [x] ✅ **HA-6 · VERIFICADO E2E 2026-06-30** — prueba de humo de GitHub tras la contenerización:
        `search_repositories` (17 repos, encontró fruterito101/for3s) + `get_file_contents` (README
        descargado, 2675 chars) vía el hermano MCP read. El camino completo de GitHub funciona. Antes
        marcado por "uso bajo desde 13-22 jun" — ya confirmado sano.
  - [x] ✅ **HA-7 · RESUELTO 2026-06-30** — rebuild de la imagen + recrear agent+worker → misma imagen (b9c5a49), fixes permanentes. agent y worker corrían IMÁGENES DISTINTAS (cazado 2026-06-30).** El agent corre
        `for3s-agent:local` (build nuevo con PR2/3/6); el worker corre una build VIEJA (por hash) →
        su telegram_channel.py quedó atrás (3164 L vs 3328). NO rompe (el worker solo corre el cron, no
        los comandos del bot), pero conviene un `docker compose up -d --build worker` algún día para
        alinearlos. Riesgo: si una corrida nocturna usara código que solo está en el agent, fallaría.
- [⏸️] **PR8 · SISTEMA DE ENTRENAMIENTO / migrar otros agentes → MOVIDO a §EXTRAS** (2026-07-01).
      Diferido: regla "no antes de pulir todo" + es bloque grande (=§ENTRENAMIENTO). Detalle en EXTRAS.
- [⏸️] **PR9 · UX/dividir telegram_channel → MOVIDO a §EXTRAS** (2026-07-01). PR9.0 (sincronización
      del repo) ✅ ya hecho 2026-06-30. Lo que QUEDA (dividir telegram_channel ~3350 L + pulir UX) es
      bloque grande delicado → diferido a EXTRAS. Detalle completo en la sección EXTRAS.
- [x] ✅ **PR10 · 🔴 COMANDOS DE SOPORTE/AUTO-DIAGNÓSTICO — COMPLETO 2026-06-29.** El usuario
      tendrá errores; NO puede depender de "habla con Brayan". ✅ **PR10.1: comando `/ayuda`** (para
      TODOS, dueño y miembros): qué es For3s + cómo usarlo + comandos SEGÚN EL ROL + sección "¿algo
      no funciona?" (primer auxilio: red inestable, memoria por tema, GitHub/web caído, /salud para
      el dueño). Antes NO existía ningún comando de ayuda. 🔍 El análisis de hermanos (curiosidad,
      como pidió Brian) cazó **BUG-12** (`/estado` estaba en el menú básico pero bloqueado a admin →
      un miembro lo veía y recibía "solo dueño"): ✅ ARREGLADO (abierto a todos, info no sensible).
      Verificado: sistema de comandos consistente (19 registrados=19 menú=todos con handler, sin
      fantasmas). Bot rebuildeado y sano. ⏳ FALTA: **PR10.2** /diagnostico mejorado y para usuarios
      (hoy solo-dueño y básico) · **PR10.3** errores útiles + auto-recuperación + /reconectar.
      Cruza con PR2 y PR9 (UX).
      ✅ **PR10.2 HECHO Y VERIFICADO 2026-06-29:** `/diagnostico` reescrito = AUTO-DIAGNÓSTICO
      PERSONAL para CUALQUIER usuario (antes solo-dueño y básico). Cada quien ve SU situación: rol
      (dueño/miembro), su hilo actual + turnos recientes, su perfil, sus temas, estado de servicios.
      🔍 El análisis "de principio a fin" cazó **BUG-13** (fuga de privacidad): el /diagnostico viejo
      leía SIEMPRE la sesión fija `_owner_session` ('brian') → un miembro habría visto los turnos del
      DUEÑO. ✅ ARREGLADO: usa `_sesion_de(user)` (la sesión real de quien pregunta, respeta el
      aislamiento H8/AI1). Verificado E2E: dueño ve hilo 'brian'; miembro Sme G ve SU hilo
      tg:7740601619 (NO el de brian) → aislamiento confirmado.
      ✅ **PR10.3a HECHO Y VERIFICADO 2026-06-29:** comando `/reconectar` (dueño) = auto-recuperación
      de integraciones SIN reinicio total. Reconecta el GitHub MCP (sesión persistente) + VERIFICA
      los hermanos de red (github-mcp-write, render) por HTTP y reporta cuáles viven. 🔍 El análisis
      profundo del manejo de errores reveló: el flujo PRINCIPAL de mensajes está bien blindado
      (Timeout/RateLimit/ServidorSobrecargado/genérico TODOS avisan ✅); el hueco era `/reiniciar`
      solo reconectaba GitHub (no verificaba render) + NO existía `/reconectar`. PRUEBAS A PROFUNDIDAD
      (capturar bugs): (1) todo OK ✅ · (2) render caído → /reconectar lo detecta "🔴 no responde"
      (no miente) ✅ · (3) web_fetch con render caído DEGRADA limpio (react.dev cargó por httpx, no
      rompió) ✅ · (4) /salud con render caído detecta la falla, COHERENTE con /reconectar ✅. NO se
      hallaron bugs nuevos en este flujo (robusto ante caída de hermanos). ✅ **PR10.3b HECHO 2026-06-29:**
      el `on_error` global ahora, además de loguear, AVISA al usuario en errores no-red ("❌ Algo
      falló de mi lado... reintenta; el dueño puede usar /salud o /reconectar") en vez de dejarlo
      esperando en silencio. Defensivo (el aviso nunca rompe el handler). Verificado: Update +
      _responder_seguro en scope, sintaxis OK, bot sano. 🎉 **PR10 COMPLETO** (soporte/auto-diagnóstico:
      /ayuda + /diagnostico personal + /reconectar + errores que avisan). El usuario ya NO depende
      de "habla con Brayan".

> ## ✅ BLOQUE PROFESIONALIZACIÓN CERRADO — 8/10 hechos, 4 movidos a §EXTRAS (2026-07-01)
> **HECHOS (8):** ✅ PR1 (claridad) · PR2 (monitoreo, COMPLETO con PR2.3 Grafana) · PR3 (datos) ·
> PR4 (auditoría) · PR6 (dueños) · PR7 (revisión hitos) · PR10 (soporte) · PR2.3 (Grafana).
> **MOVIDOS A §EXTRAS (diferidos por decisión, 2026-07-01):** PR5 (datos empresa, necesita usuarios) ·
> PR8 (entrenamiento, regla no-antes-de-pulir) · PR9 (UX/dividir telegram_channel, bloque grande) ·
> HA-3 (H7 enrutamiento, futuro). Ver detalle en §EXTRAS (arriba del doc).
> Los 6 hallazgos HA-1..HA-7 de PR7 TODOS resueltos (HA-3 a EXTRAS). El barrido crítico F1-F5 cerró
> BUG-14/15/18 y mitigó BUG-17. **→ BLOQUE PROFESIONALIZACIÓN CERRADO (0 activos aquí).**

---

## 🔧 PULIR H8 — ✅ CERRADO 2026-07-01 (7/8 áreas; H·BYOK movida a §EXTRAS)

> Las áreas a pulir de H8. ESTADO FINAL: ✅ A (UX equipo) · ✅ B (disparo sugerir-con-botón) ·
> ✅ C (puerta: avisos + sacar/kick) · ✅ D (memoria híbrida) · ✅ E (gate ejecución real) ·
> ✅ F (menú/comandos, cerrado 2026-07-01 con `/equipo`) · ✅ G (robustez bajo carga; multi-tenant
> diferido a propósito). **→ BLOQUE CERRADO.** La única área no hecha, **H·BYOK**, se movió al
> apartado **§EXTRAS** (sub-sistema grande, diferido por decisión de Brian — se retoma aparte).

- [x] ✅ **A · Equipo multi-agente (UX) — CERRADO 2026-06-24.** Base hecha al inicio (progreso
  vivo + línea de gasto tiempo/tokens/cupo). PULIDO PRO 2026-06-24 con 4 mejoras: A-i progreso
  de 3 ESTADOS por specialist (⏳ en cola · 🔄 en curso · 🟢 listo · 🔴 falló) — el motor
  (multiagente.correr_equipo) emite evento "trabajando" al arrancar cada uno (verificado: inicio
  +5 trabajando +5 fin); A-ii "escribiendo…" de Telegram durante toda la corrida (señal de
  actividad, se cancela en finally); A-iii encabezado limpio "📋 Informe del equipo" antes del
  contenido; A-iv caso 0/N (todos fallan) → aviso honesto "el equipo no pudo completar... reintenta"
  en vez de informe pobre. 132 tests, bot activo. Aditivo + defensivo (progreso cosmético nunca rompe).
- [x] ✅ **B · Disparo automático — CERRADO 2026-06-24.** DECIDIDO (Brian): SUGERIR con botón
  (no lanzar solo) → cero gasto sorpresa + descubrible + tú decides. 3 NIVELES: (1) gatillo
  DIRECTO (`_amerita_equipo`, 17 frases "analiza a fondo/lanza el equipo"...) → corre YA; (2)
  SEÑAL SUAVE (`_sugiere_equipo` NUEVO: comparar/evaluar/riesgos/pros-contras/decidir-entre/
  analiza X/audita; mín 15 chars, no en saludos) → OFRECE botón [🤝 Lanzar equipo][💬 Responde
  tú solo]; (3) charla normal → 1 agente. Callback `on_equipo_sugerido` (guarda texto original
  como las write pendientes; solo quien pidió decide; oferta NO-bloqueante: si la ignora y sigue,
  responde normal) + `_responder_agente_simple`. Verificado: directos 3/3, suaves 5/5, charla 5/5
  (no dispara). 132 tests, bot activo. Aditivo (no toca el disparo directo).
- [x] ✅ **C · Multi-usuario / puerta — CERRADO 2026-06-24.** Responde la observación de Brian
  "¿cómo sé quién entró?". Ya existían: mensajes abrir/cerrar puerta (/invitar), aviso puerta
  cerrada, /miembros (consulta pasiva, AI7). PULIDO 2026-06-24: cuando alguien ACABA DE ENTRAR
  por la puerta (motivo 'puerta_abierta' = recién registrado, solo 1ª vez): C-ii BIENVENIDA al
  que entra ("👋 ¡Bienvenida/o al equipo, <nombre>!... tu conversación es privada y separada");
  C-i AVISO PROACTIVO al encargado (context.bot.send_message a su chat por owner_id: "👤 <nombre>
  se unió al equipo (por la puerta abierta) · ahora son N"). `_bienvenida_y_aviso` defensivo
  (cada parte su try, nunca rompe el flujo; si el encargado bloqueó al bot, se ignora). 132 tests,
  bot activo.
  ✅ **C-v SACAR/DENEGAR MIEMBROS — CERRADO 2026-06-24** (ya no pospuesto). DECIDIDO: botón
  [🚫 Sacar] por miembro en /miembros + confirmación + soft-remove + DENEGADO real (no re-entra
  por puerta abierta). migración 017 (columna `expulsado`). equipo.py: `sacar_miembro` (soft-remove
  activo=false+expulsado=true, verifica en BD que quien saca es ENCARGADO, NO autosaca, NO saca a
  otro encargado) + `agregar_miembro(reinvitar=)` (re-invitación del encargado limpia expulsado; por
  puerta NO re-admite expulsado) + `autorizar` devuelve 'expulsado' (sacado=denegado aunque puerta
  abierta). telegram_channel: on_miembros con botones por miembro (no el encargado) + on_kick
  (confirmación) + on_kick_confirm (ejecuta, audita 'miembro_sacado', avisa al sacado). Historial
  del sacado se CONSERVA; conocimiento del equipo se queda. Reversible (re-invitar). VERIFICADO 9/9
  checks. 132 tests, bot activo.
- [x] ✅ **D · Memoria híbrida — CERRADO 2026-06-25.** El aislamiento privado/común ya
  estaba (AI1 scope_user_id + #6 hilo por usuario). Lo que faltaba y se construyó: que el
  bot se GUÍE POR TIEMPO Y AUTOR (refuerzo Brian 2026-06-23), no solo por semántica. 3 piezas
  (debatir→decidir→código→testeo): **D-1** memory.Turn + load_history traen created_at +
  telegram_user_id (retrocompat, default None) + conversation inyecta bloque "LÍNEA DE TIEMPO"
  (últimos 12 turnos con fecha+autor, NO contamina los mensajes a Claude; test 14/14). **D-2**
  detector `_es_pregunta_retomar` (regex flexible 'en/dónde [...] quedamos|dejamos' + frases:
  "ponme al día", "recapitula", "qué hicimos"... — tolera 'en que NOS quedamos') + bloque "LO
  ÚLTIMO QUE TRABAJARON" (últimos 4 turnos crudos, 400 chars, orden cronológico, excluye la
  propia pregunta; test 26/26). **D-3** FOR3S_ROLE: "guíate por el turno MÁS RECIENTE, no por
  lo parecido; no mezcles hilos". Suite 132, bot activo. ⭐ FIX en vivo: el detector no cazaba
  "en que NOS quedamos" (frase exacta) → regex flexible. VERIFICADO en vivo (Brian): detector
  dispara + bloque cronológico inyectado. (texto original del pendiente abajo ⬇️)
- [x] ✅ **D (orig) · Memoria híbrida — CERRADO** (ver "D · CERRADO 2026-06-25" arriba: línea de tiempo +
  autor + retomar; reforzado en REDISEÑO MEMORIA F1-F5). Este es el TEXTO ORIGINAL del pendiente:
  Que lo privado vs común se sienta natural; que el bot
  SEPA de quién es lo que recuerda y no mezcle; scope correcto al guardar/recuperar
  por persona dentro de un equipo.
  ⭐ REFUERZO BRIAN (2026-06-23): el bot debe GUIARSE POR FECHAS (timestamp) Y AUTOR
  al retomar/responder, no solo por cercanía semántica. Causa del bug #6 fue
  justamente que NO se guiaba por fecha ni usuario → revolvía. Ya hay datos (created_at
  + telegram_user_id por turno tras #6); falta USARLOS: al "¿en qué quedamos?" mirar
  MI turno más reciente CON su fecha; al recuperar memoria, respetar autor+fecha.
  Verificación de integridad hecha 2026-06-23: hilos brian/tg:<id> con desorden
  fecha-vs-seq=0, 0 cruces entre hilos, turnos de Ella movidos a su hilo (26),
  par #591-592 contaminado soft-deleted. Backup /tmp/backup_episodes_premove.sql.

  ⭐⭐ **BUG CRÍTICO #6 — HILO POR USUARIO (Brian 2026-06-23, prioridad).** HOY todos
  comparten UN solo hilo (`owner_session="brian"` fijo) → cuando Brian escribe, el bot
  CONTINÚA el hilo de otra persona (¡peligroso!). VISIÓN BRIAN: cada quien su PROPIO
  hilo; lo que comparten es el CONOCIMIENTO (lo aprendido), no la conversación.
  Ejemplo: Brian=backend, Ella=frontend; si Brian necesita frontend NO molesta a Ella
  ni hereda sus errores — usa lo que el agente APRENDIÓ de ella (grafo/CLS). Por eso
  existe la fase "se cuida"/Cerebro: ahí se nutre el conocimiento común.
  SEPARAR 3 cosas hoy pegadas: HILO (privado/persona) · MEMORIA (híbrida) · CONOCIMIENTO
  (común, grafo/CLS). DISEÑO DECIDIDO:
  • session_id POR usuario derivado del user_id (ej. "tg:<id>"). Hoy 1 sesión para todos.
  • D1: conservar el historial del dueño → mapear sesión "brian" → su user_id (no pierde nada).
  • D2: solo lo CONSOLIDADO se comparte (grafo/CLS de noche); el hilo crudo es privado.
    La memoria semántica cruda NO se comparte entre personas — coincide con fase Cerebro.
  • D3: #6 ahora (hilos + quién escribió en BD #3); BYOK (apartado H, key por persona) después.
  Arregla además #3 (en BD se ve quién escribió, cada turno con su session_id). Tocar
  los puntos con _owner_session en telegram_channel.py (conversación/memoria), NO el
  grafo. record_turn ya soporta owner_user_id (S10c). Aditivo + compat con el dueño.

  🔬 AUDITORÍA 2026-06-23 (datos reales BD) confirmó la causa raíz: TODO cae en la
  sesión 'brian' (589 turnos). con owner_user_id=0 y equipo_id=0 (NADIE etiquetado).
  NO existe columna del user_id de quién mandó cada turno → solo session_id='brian'
  para todos. EVIDENCIA: turnos #565-590 mezclan a Sme G (user 7740601619, miembro)
  con informes de equipo de Brian INTERCALADOS en el mismo hilo; en #589 ella pregunta
  "¿cómo se llama la otra persona del equipo?" y el bot no sabe (#590). SÍ funcionan:
  puerta (Sme G entró ok), menú por rol, equipo multi-agente. REFUERZO AL DISEÑO: además
  de session_id por usuario, AÑADIR columna `telegram_user_id` (o reutilizar
  owner_user_id) en episodes_events + escribirla en cada record_turn, para poder
  responder con certeza "quién escribió esto" (#3). Informe completo en chat 2026-06-23.
- [x] ✅ **E · Gate de aprobación — EJECUCIÓN REAL CERRADO 2026-06-24 (= cierra AI3-parte 2).**
  DECIDIDO: flujo completo miembro→encargado→ejecución, write con PAT del DUEÑO por ahora
  (cambiará a la del miembro con BYOK/apartado H — anotado). Construido: `_proponer_write` bifurca
  por ROL — DUEÑO confirma él mismo (flujo de siempre); MIEMBRO → `_proponer_write_miembro` crea
  solicitud con payload {tool,args,solicitante} + avisa al encargado con [✅ Aprobar][❌ Rechazar]
  (proactivo) + avisa al miembro "enviado a aprobación". `on_gate_select` al APROBAR: lee payload →
  ejecuta_write REAL (whitelist dura) + audita 'github_write_gate' + avisa al miembro del resultado;
  al rechazar avisa al miembro. Seguridad: solo encargado aprueba (verificado en BD), whitelist 4
  writes. VERIFICADO 7/7 checks (payload guardado/devuelto, miembro no auto-aprueba, rechazo avisa).
  132 tests, bot activo. ⭐ Con esto el gate de H8 queda 100% funcional. ⏳ BYOK: cambiar credencial
  de ejecución a la del miembro (apartado H).
- [x] ✅ **F · Comandos / menú — CERRADO 2026-07-01.** Menú por-rol ya estaba. De lo que pedía:
  `/ayuda` ✅ (PR10, lista explicada) · `/miembros` ✅ · faltaba **`/equipo` (lanzar equipo manual)**
  → CONSTRUIDO 2026-07-01: comando `on_equipo` (`/equipo <tarea>`) que dispara el equipo multi-agente
  sin depender de frases-gatillo ni del botón sugerido, en el menú básico (todos). 🔍 Análisis de
  comportamiento a fondo (Brian: "puede haber bugs inusuales") — 4 salvaguardas: (1) `_autorizar`
  primero (sin esto un no-autorizado dispararía el equipo = agujero de gasto); (2) exige tarea (≥5
  chars, /equipo vacío explica el uso); (3) valida provider/agent listo (⚠️ CAZADO: `_correr_equipo_inner`
  NO valida provider None → lo checo en on_equipo para no fallar feo); (4) pasa sesión+scope+autor de
  la persona (aislamiento, como el flujo normal). Reusa `_correr_equipo_y_responder` (lock/cola global
  ya probado). Verificado: compila, importa, on_equipo en la clase, bot reinicia sano, menú publicado.
  Permanente (repo + rebuild + recrear, no docker cp). ⚠️ EN EL SERVER — repo/GitHub pendiente de
  sincronizar cuando Brian ordene. → **PULIR H8: 7/8 áreas cerradas (A-G), solo falta H (BYOK, diferido).**
- [~] **G · "Distribuido" — ROBUSTEZ BAJO CARGA hecha 2026-06-24; multi-tenant DIFERIDO.**
  DECIDIDO (Brian): "robustez bajo carga ahora, multi-tenant después (cuando haya 2º cliente)".
  Distinción clave: multi-USUARIO (varias personas 1 equipo) ✅ YA hecho (H8 S10 + AI1-7) ≠
  multi-TENANT (varios clientes aislados) ⬜ diferido. HECHO HOY (G-a robustez): semáforo GLOBAL
  de equipos — solo UNA corrida de equipo (5 specialists) a la vez en todo el bot (self._equipo_lock),
  las demás en cola con aviso (máx 3 en espera); evita que varias personas disparen equipos en
  paralelo → anti-429 OAuth Tier 1. La charla normal (1 agente) NO se afecta. _correr_equipo_y_responder
  ahora envuelve _correr_equipo_inner con el lock. VERIFICADO con test de concurrencia: 3 corridas
  simultáneas → serializadas (máx 1 a la vez), 2 avisos de cola, contador a 0. G-b cost-control 7
  capas (ya defensivo) + G-c aislamiento de fallo (timeout global por equipo + try/except del caller)
  YA cubiertos. 132 tests, bot activo.
  ⏳ DIFERIDO a cuando haya 2º cliente real: multi-tenant REAL (RLS Postgres por workspace +
  anomaly-kill) = el pendiente [[H8-aislamiento-multitenant]]. Cimientos listos (workspace_id en
  tablas, cost_control por workspace). Cruza con producto distribuible P1-P10.
- [⏸️] **H · Credenciales por usuario (BYOK) → MOVIDO a §EXTRAS** (ver #1 de EXTRAS). ⭐ decisión Brian
  2026-06-23.** → ⏸️ **MOVIDO a §EXTRAS** (2026-07-01): sub-sistema grande, diferido por decisión
  de Brian, se retoma como su propio bloque. Ver detalle completo en la sección EXTRAS abajo.

---

## 🧬 ADOPTAR de intern-os → CÓDIGO PURO en For3s (Brian 2026-06-23) — 7 pendientes

> **Estrategia (Brian):** intern-os resuelve cosas con SKILL (markdown + scripts bash,
> 0 infra). For3s las hará en CÓDIGO PURO Y DURO (Python + PostgreSQL, integrado al
> núcleo). Descomponer intern-os FRAGMENTO POR FRAGMENTO y adoptar lo útil para llevar
> For3s a mejor punto. Ya tenemos el código de intern-os clonado
> (`~/Frutero-Empresa/Frutero/intern-os/`) → sin problema de "no encuentro el código".
> Análisis base: `docs/analysis-internos-v1_vs_For3s_OS.md`. ⚠️ Registrados como pendientes;
> se atacan de uno en uno (debatir → decidir → código → testeo), respetando fase pulido H8.

- [x] ✅ **AI1 · DOCTRINA DE AISLAMIENTO — HECHO 2026-06-23.** DECIDIDO: ambas mitades
  (doctrina + conectar scope). HALLAZGO en el análisis: el `scope_user_id` (S10c) EXISTÍA pero
  NO se aplicaba en el flujo real (buscar_semantico se llamaba sin él) → hueco "código existe
  pero no se usa". CERRADO: (1) `conversation.py` Conversation acepta `scope_user_id` y lo pasa
  a las 2 llamadas de buscar_semantico (2ª capa de aislamiento sobre el session_id). (2)
  telegram_channel `_scope_de(user)`: dueño→None (ve todo lo suyo + legado NULL, compat),
  miembro→user_id (solo su privada + común, NUNCA lo de otro); usado en ambos Conversation
  (on_message + on_adjunto). (3) FOR3S_ROLE: sección "AISLAMIENTO ENTRE PERSONAS Y TEMAS"
  (5 reglas: no asumir de otro hilo, no mezclar/continuar conversación ajena, lo compartido
  es el CONOCIMIENTO no el chat crudo, ante duda preguntar, no inventar conexiones).
  VERIFICADO con embeddings reales: Ana(miembro) NO ve lo privado de Luis; dueño(scope=None)
  ve TODO incl. su legado NULL (historial intacto). 132 tests, bot activo.
- [x] ✅ **AI2 · Shared-thread inbox (CÓDIGO) — HECHO 2026-06-23.** Temas por persona en
  Telegram (un chat = varios hilos/temas). DECIDIDO: temas EXPLÍCITOS por comando, default
  'general' opt-in. Construido punto a punto + verificado: (1) migración 014 tabla `temas`
  (user_id, nombre, activo, UNIQUE); (2) `temas.py` TemaStore (activo/cambiar/listar +
  normalizar_nombre con acentos→ascii, fail-safe a 'general'); (3) telegram_channel:
  `_sesion_de` AHORA ASYNC = base(#6) + sufijo tema (':<tema>', general=sin sufijo→conserva
  historial 'brian'); comandos /tema /temas + botones (on_tema/on_temas/on_tema_select);
  en _MENU_BASICO (todos). (4) E2E: brian→brian, brian+backend→brian:backend, ella+frontend→
  tg:<id>:frontend, aislado, general conserva historial. session_id = tg:<uid>:<tema>. BD v14,
  132 tests, bot activo. Cada persona×tema = hilo separado; conocimiento (grafo/CLS) se comparte.
- [x] ✅ **AI3 · ⭐⭐⭐ Handoff → CÓDIGO auditable — COMPLETO (parte 1 audit + parte 2 gate).**
  DECIDIDO: DB-backed (no archivos — tenemos Postgres) + audit trail primero + texto completo
  de cada specialist. Construido punto a punto + verificado: (1) migración 015 tablas
  `corridas_equipo` (sesión/autor/tarea/familia/n_ok/tokens/segundos/informe) + `corrida_reportes`
  (por specialist: nombre/ok/tokens/texto COMPLETO, CASCADE); (2) `handoff.py` registrar_corrida()
  TRANSACCIONAL + defensivo (audit NUNCA rompe entrega) + separación de escritura (el HUB/
  coordinador escribe, los specialists no) + ultimas_corridas() para trazabilidad; (3) cableado
  en _correr_equipo_y_responder tras sintetizar (usa sesión #6/AI2 + autor). BD v15, 132 tests,
  bot activo. Probado con fake: corrida+reportes+tokens+CASCADE OK.
  ✅ PARTE 2 CERRADA 2026-06-24 (en apartado E): gate ejecución real — miembro propone write →
  encargado aprueba → se ejecuta con PAT del dueño + avisa al miembro. Ver apartado E arriba.
  🎉 **AI3 COMPLETO (parte 1 audit + parte 2 gate).**
- [x] ✅ **AI4 · Auto-inyectar estado + cierre (CÓDIGO) — HECHO 2026-06-23.** DECIDIDO: STATUS
  por hilo + auto-retomar; se regenera de noche (con H6, cero costo de día); se inyecta solo al
  retomar tras inactividad (>3h). Para3s NO tiene SessionStart como Claude Code (bot siempre on)
  → se tradujo a "RETOMAR.md por hilo". Construido a detalle + verificado: (1) migración 016
  tabla `hilo_status` (session_id PK, texto, actualizado_at); (2) `hilo_status.py`: get/guardar +
  generar_status (resume últimos turnos vía LLM OAuth-safe, min 4 turnos, defensivo) + debe_inyectar
  (solo si último turno >3h) + hilos_activos; (3) conversation.py inyecta el STATUS al contexto en
  send() cuando debe_inyectar (como memoria/grafo/versión); (4) job_status nocturno en tasks.py
  (02:30 México, DESPUÉS de CLS, espacia 3s anti-429) + registrado en WorkerSettings + cron.
  VERIFICADO con LLM real: job corrió "2/2 hilos resumidos", STATUS de calidad y AISLADOS por hilo
  (brian=auditoría bugs, tg:<id>=planificación del día). BD v16, 132 tests, bot+worker activos.
- [x] ✅ **AI5 · version-self-awareness (CÓDIGO) — HECHO 2026-06-23. CIERRA P4 + G4.**
  DECIDIDO: versión por HITOS+semver + inyección al detectar la pregunta. Construido +
  verificado: (1) `version.py` fuente única (VERSION=0.8.3, HITO=H8 EQUIPO, CHANGELOG
  estructurado H1→H8 con qué trae cada uno, resumen()/resumen_corto(), lee schema_version
  de BD como dato técnico); (2) `conversation.py` _es_pregunta_version() (detecta "qué
  versión/cuándo te actualizaron/qué hay nuevo/hitos/novedades", 8/8 casos OK) + inyección
  del resumen al contexto en send() (como memoria/grafo, defensivo); (3) comando `/version`
  (cualquier usuario, cero tokens LLM) + en _MENU_BASICO. 132 tests, bot activo. El agente ya
  puede responder su versión/cambios con datos reales sin inventar. MANTENER: actualizar
  version.py al cerrar cada hito/pulido. ⚠️ Esto cierra también P4 y G4-version-self-awareness.
- [x] ✅ **AI6 · Disciplina de tamaño + tiered (CÓDIGO) — HECHO 2026-06-23. CIERRA G5.**
  DECIDIDO: tiered inteligente (corto por defecto, completo si relevante). For3s YA tenía topes
  (12 turnos, 300 chars/recuerdo, top_n 3, conceptos[:25]) → no había bloat agudo; AI6 afinó el
  BALANCE. Construido en conversation._formatear_recuerdos: `_chars_por_relevancia(dist)` escalones
  (dist<0.35→700 chars, 0.35-0.55→450, 0.55-0.75→300) → lo MUY relevante llega casi completo
  (cierra G5: ya no se fragmenta lo importante), lo lejano corto (no infla). + tope GLOBAL del
  bloque `_MAX_CHARS_BLOQUE_RECUERDOS=2500` (anti-bloat real) + orden por relevancia (lo mejor
  entra primero si se llega al tope). VERIFICADO: escalones OK, relevante 700/lejano 300, tope
  global corta de verdad (6 ofrecidos→4 entran, 2438≤2500), orden correcto. 132 tests, bot activo.
  ⚠️ Cierra G5-recuerdos-fragmentados.
- [x] ✅ **AI7 · Registry de hilos (CÓDIGO) — HECHO 2026-06-23.** DECIDIDO: /miembros + /hilos
  (vista de equipo). Construido a detalle (profesional, reusando datos existentes, DRY):
  (1) `temas.py` HiloInfo + resumen_hilos(user_id, base_sesion): cada tema + actividad real
  (último turno + nº turnos, LEFT del episodes_events), incluye 'general' implícito, orden activo
  →reciente; (2) telegram_channel: `/miembros` (solo encargado, reusa equipo.miembros + puerta;
  si single-owner sugiere /invitar) + `/hilos` (cada persona, sus hilos con actividad) + helper
  `_humanizar_fecha` (hoy/ayer/hace N días/sem); menú por ROL (hilos→básico, miembros→admin).
  VERIFICADO datos reales: /miembros→👑encargado+👤Sme G; /hilos→general 565 msgs ayer; menú/
  fechas OK. RESPONDE la observación original de Brian "¿cómo sé quién entró?" (apartado C).
  ⭐ **4 MEJORAS PRO (2026-06-24, cierre profesional):** M1 nombre real del encargado (asegurar_equipo
  recibe nombre_encargado + AUTO-CURA filas viejas con nombre NULL — ya no sale "(sin nombre)") ·
  M2 /miembros y /hilos en el menú por rol · M3 HEALTH: /miembros muestra última actividad por
  miembro (LEFT JOIN episodes_events: 'activo hoy/hace N días') · M4 aislamiento de /hilos
  verificado (cada persona ve SOLO sus hilos). VERIFICADO 8/8 checks + 132 tests, bot activo.
  🎉 **ADOPCIÓN intern-os COMPLETA: AI1-AI7 todos cerrados.**

> **Orden sugerido (para cuando se diseñe):** AI2 (shared-thread inbox, es nuestro caso exacto) +
> AI3 (handoff para gate E) son los más urgentes dado que estamos en pulido H8 multi-usuario. AI5
> cierra P4/G4 de un golpe. AI1/AI4/AI6/AI7 refuerzan disciplina. NO empezar sin debatir+decidir
> cada uno (regla de Brian). Cada uno: fragmento intern-os → traducir a código For3s → testeo.

## 🔍 ANALIZAR A PROFUNDIDAD `intern-os` (Brian 2026-06-23) — tarea pendiente

> **Tarea:** auditar a fondo el repo `intern-os` de Frutero para identificar qué cosas
> tiene RESUELTAS que For3s OS aún NO ha mejorado, y traer esos aprendizajes a For3s.
> Surgió justo después de arreglar el bug de HILOS por usuario en For3s (#6): intern-os
> ya maneja hilos (shared-thread inbox, ver su CHANGELOG) + muchas otras cosas.
> ⚠️ NO analizar ahora — registrado para retomar cuando Brian diga.

- [x] ✅ **Análisis profundo intern-os vs For3s OS — HECHO 2026-07-01.** Auditoría a fondo del repo
  clonado local (`~/Frutero-Empresa/Frutero/intern-os/` v0.4.1): README, FRAMEWORK, CHANGELOG,
  templates, scripts. Reporte completo: `docs/analysis/Analisis_intern-os_para_For3s.md`. HALLAZGO: es un
  framework de coordinación por archivos markdown/bash (workstreams ligados a 1 hilo, estado en
  archivos, resolución por thread_id EXACTO, isolated handoff, shared-thread inbox) — complementario
  al motor cerebral de For3s, no competidor. For3s YA absorbió su capa de hilos/handoff (AI1-AI7,
  2026-06-23). **3 CONCEPTOS VALIOSOS a traer como código PROPIO (mapa listo, NO implementado):**
  C1 estado operativo por tema/proyecto (fase/next/blockers) · C2 registro de DECISIONES
  (decisión+rationale+impacto+estado) · C3 resolución determinista de hilo (exacto→semántico, encaja
  en MEM-3 cascada). Los 3 cruzan con REDISEÑO MEMORIA. Cuando Brian decida construir → código propio,
  sin referencias externas ([[feedback_cero_referencias_externas]]).
- [x] ✅ **C1 · Estado operativo por tema — HECHO 2026-07-02.** Migr 031 `tema_estado` + módulo
  `tema_estado.py` (Store fail-safe + formatear + parsear) + comando `/estado_tema` (consulta y
  `/estado_tema fase: X | proximo: Y | bloqueo: Z`, combina campos) + inyección al contexto (el bot
  sabe "en qué punto va el proyecto"). Es "un RETOMAR.md por tema", distinto de hilo_status (narrativo).
  Híbrido (manual + inyección auto). Aislado por sesión, aditivo, fail-safe. Verificado E2E contra BD viva.
- [x] ✅ **C2 · Registro de DECISIONES — HECHO 2026-07-02.** Migr 032 `decisiones` (CHECK estado) +
  módulo `decisiones.py` (registrar/listar/buscar/cambiar_estado + audit) + comandos `/decidi <título>
  :: <por qué> :: <impacto>`, `/decisiones`, `/decision <id> superada|revertida` + detección auto de
  "¿por qué decidimos X?" → inyecta las decisiones con rationale (el bot responde el porqué real, no
  inventa). Decisión de Brian: responde auto, REGISTRA solo con /decidi (no inventa decisiones).
  Aislado por sesión (probado: no ves ni cambias decisiones de otro tema), audita cada una. E2E OK.
- [x] ✅ **C3 · Resolución determinista de hilo — HECHO 2026-07-02.** Investigación a fondo de la
  cascada (M1-M4): la SESIÓN ya se resuelve exacta en todas las capas (blindado por M2/AI1); lo difuso
  era el matcher de CONCEPTOS del grafo (`_concepto_relevante`, por palabras compartidas). C3 añade capa
  EXACTA previa: `_conceptos_exactos()` detecta labels nombrados LITERAL en la query (límites de palabra,
  acentos, min 3 chars) → van PRIMERO y garantizados (no los pierde el corte [:25]); difuso después.
  ENFOQUE LIMPIO: query como PARÁMETRO explícito (NO estado global mutable — evité un bug de carrera
  entre usuarios concurrentes). Aditivo: sin match exacto = idéntico a hoy (cero regresión). Verificado
  9/9 casos borde + E2E contra grafo vivo (63 conceptos) + análisis de concurrencia (8 recordar paralelo
  sin carreras). 🎉 **BLOQUE intern-os COMPLETO: AI1-AI7 + C1-C2-C3.**
- [x] ✅ **HALLAZGO nombre del dueño NULL — RESUELTO 2026-07-02 (captura automática).** Causa raíz:
  `set_owner_bd` insertaba en `personas` solo (telegram_user_id, rol), nunca el nombre → dueño con
  nombre=NULL (la AUTO-CURA de AI7-M1 solo tocaba `equipo_miembros` al invitar/lanzar, no al registrar
  al dueño). FIX (3 puntos): (1) `set_owner_bd(pool, user_id, nombre)` escribe el nombre en personas con
  `COALESCE(personas.nombre, EXCLUDED.nombre)` (no pisa); (2) on_start pasa `user.full_name`; (3)
  `_curar_nombre_persona(user)` en `_autorizar` — si el dueño tiene nombre NULL, lo rellena con el
  full_name de Telegram (barato: UPDATE solo si NULL). Nunca inventa (usa el nombre real del perfil),
  COALESCE (no pisa uno puesto a mano), fail-safe. Verificado E2E (rellena si NULL, NO pisa, idempotente).
  ⚠️ La fila real de Brian se cura SOLA en su próximo mensaje al bot (no se tocó a mano = no inventar).

## 📦 FOR3S OS COMO PRODUCTO DISTRIBUIBLE (P1-P10) — ✅ COMPLETO 2026-07-02 (10/10)

> ✅ **BLOQUE CERRADO 2026-07-02.** Al debatirlo se vio que 8 de los 10 ya estaban
> hechos por bloques posteriores (PRE-TESTERS, MULTI-INSTANCIA, AUTO-CONCIENCIA,
> EXECUTE_CODE — estos 10 se escribieron el 2026-06-23, ANTES de construirlos). Solo
> **P4** (self-version-awareness) y **P7** (encarpetado documentado) eran brechas reales
> → se atacaron y verificaron E2E. version.py subió a **v0.14.0** "PRODUCTO DISTRIBUIBLE".
>
> **El gran salto (logrado):** de "demo que solo corre en nuestra máquina" a un PRODUCTO
> instalable con UNA línea (`curl|sh`) que despliega BD+contenedores+lógica ordenados.

- [x] **P1 · Versión de prueba en GitHub (H0→H8).** ✅ Cerrado por PRE-TESTERS + repo
  oficial `fruterito101/for3s`: el avance está en GitHub como versión instalable.
- [x] **P2 · Repositorio público bien configurado (atribución al ORIGINAL).** ✅ Cerrado
  por PRE-TESTERS: LICENSE (AGPL-3.0), README, NOTICE, SECURITY.md, CONTRIBUTING.md,
  CHANGELOG.md — con atribución al original (Brian).
- [x] **P3 · Apartado de instalación con OPCIONES a llenar.** ✅ Cerrado por PRE-TESTERS:
  `install.sh` con wizard ("siguiente, siguiente, listo") + KEK automática.
- [x] **P4 · Control de versiones del agente (self-version-awareness).** ✅ HECHO 2026-07-02.
  `version.py` = fuente única (VERSION/HITO/FASE + CHANGELOG que el agente lee) + `/version`
  + inyección automática cuando preguntan (ya existía de AI5, cerraba P4+G4). **Brecha real
  cerrada:** (P4.a) changelog puesto al día → v0.14.0 "PRODUCTO DISTRIBUIBLE" con los 4
  bloques nuevos (memoria/auto-conciencia/multi-instancia/execute); (P4.b) **changelog VIVO**:
  `auto_cambios_recientes()`+`formatear_auto_cambios()` leen `diario_cambios` (origen='propio')
  → cuando el agente se auto-modifica (AC3) lo reporta en su versión, SIN reescribir el archivo
  fábrica (respeta el guardián). Cableado en conversation.py + telegram_channel.py. Verificado
  E2E contra BD viva + horneado en el contenedor (arrancó sano, guardián OK).
- [x] **P5 · For3s OS conoce su CÓDIGO FUENTE (con restricciones).** ✅ Cerrado por
  AUTO-CONCIENCIA: `/introspeccion` `/soy` (ve su código/infra en vivo) + `/modificar`
  `/modificar_bd` (edita con LÍNEAS ROJAS: nunca governor/audit/KEK).
- [x] **P6 · Espacio propio dentro de su contenedor (su "computadora").** ✅ Cerrado por
  EXECUTE_CODE: sandbox hermano + workspace PERSISTENTE (crea/edita/guarda; sobrevive).
- [x] **P7 · Sistema de encarpetado estandarizado.** ✅ HECHO 2026-07-02. `ESTRUCTURA.md`
  en la raíz del repo: mapa de todos los directorios + tabla "¿dónde pongo mi archivo nuevo?"
  (módulo→for3s_core, migración→migrations/NNN, comando→telegram_channel, servicio→docker/,
  prueba→tests/, etc.). Documentación, cero riesgo.
- [x] **P8 · Instalar programas.** ✅ Cerrado por EXECUTE_CODE (pip/npm en el sandbox, red
  abierta) + `install.sh` (dependencias del host).
- [x] **P9 · Instalador "primera vez" despliega TODO ordenado.** ✅ Cerrado por PRE-TESTERS:
  `install.sh` + `docker-compose.yml` despliegan BD+contenedores+migraciones E2E ordenados.
- [x] **P10 · Contenerizar el código actual + ordenar la construcción.** ✅ Cerrado por
  PRE-TESTERS: docker-compose (Postgres+AGE+pgvector, valkey, agent, worker, MCP, render,
  sandbox, grafana) + Dockerfiles horneados. + ordenado por P7 (ESTRUCTURA.md).

> **Cierre 2026-07-02:** 10/10. La distribución (P1/P2/P3/P9/P10) + el sandbox propio
> (P6/P8) + self-awareness/auto-edición (P4/P5) + encarpetado (P7) están todos hechos.
> Lo que queda del "producto público" son EXTRAS diferidos (DIST-1..5: probar curl|sh en
> Linux limpio, dominio+landing, v1.1 hermanos en instalador, monetización) — NO parte de
> P1-P10. version.py = v0.14.0.

---

## 🧠 AUTO-CONCIENCIA + AUTO-MODIFICACIÓN — ✅ COMPLETO 2026-07-01 (EN PRODUCCIÓN)

> ✅ **BLOQUE CERRADO.** Debatido (modo debate primero) + construido fase por fase + probado E2E y en
> vivo. Diseño: `Cuerpo/Ronda_Auto_Conciencia_Automod_Plan.md`. Las 4 fases (AC1-AC4) + guardián de
> arranque. El agente se conoce (`/introspeccion` `/soy`), detecta qué cambió (`/cambios`), edita su
> CÓDIGO (`/modificar` `/revertir`) y su BD (`/modificar_bd`) DENTRO de su caja (contenedor local,
> NUNCA GitHub), actuando solo con control ESTRUCTURAL. Doble red: entorno de prueba (previene) +
> guardián (rescata: revierte a fábrica + avisa). Líneas rojas: governor/audit/KEK. 5 commits firmados
> en GitHub (a5b1a14·029cb8e·8b7a800·2496355·1eaccfd). AC1-AC4 abajo = ✅ hechos.


> **El hallazgo de Brian (textual):** hoy el agente NO reconoce sus propias mejoras —
> *"tú se lo tienes que agregar, tú le tienes que decir en qué actualización va; el
> agente no puede tocar su propia infraestructura. ESO ESTÁ MAL."* La visión correcta:
> **el agente debe reconocer SOLO que le alteraron su lógica interna (no porque yo se lo
> dije), saber TODO lo que tiene, y poder ALTERAR su propio código y su base de datos,
> siendo consciente de ello.** Es la diferencia entre "le edito FOR3S_ROLE y le aviso"
> (dependiente de mí) vs "él detecta el cambio y se auto-modifica" (autónomo).
>
> ⚠️ Es un SUB-SISTEMA GRANDE y de MÁXIMO CUIDADO (código auto-modificante = territorio
> del Pilar 3 / governor H11 que ya existe). Registrado como pendiente; se DEBATE y diseña
> tipo Ronda antes de tocar nada. Cruza con: P4/P5 (producto: self-version-awareness +
> conocer su código fuente), H10-12 APRENDE (governor/freno YA construido = la base de
> seguridad para esto), y la deuda "matcher/audit de skills".

- [x] ✅ **AC1 · Auto-detección de cambios en su propia lógica.** Que el agente note SOLO
      que algo en su código/lógica/personalidad cambió desde la última vez (ej. hash/diff
      de FOR3S_ROLE, de los módulos core, del schema de BD) y lo RECONOZCA en el chat sin
      que nadie se lo diga. Hoy AI5 (version.py) es ESTÁTICO: yo edito el changelog a mano y
      él lo lee. Esto es lo contrario: él DETECTA el cambio. Posible base: firmar/hashear los
      archivos core + comparar al arrancar + un "diario de cambios" que el propio sistema
      escribe cuando se detecta una alteración.
- [x] ✅ **AC2 · Conciencia total de lo que tiene (introspección real).** Que el agente sepa
      —y pueda decir— qué módulos tiene, qué tablas/columnas hay en su BD, qué migraciones
      corrió, qué skills/jobs/comandos existen. No una ficha que yo escribí, sino consultado
      de su propia infraestructura en vivo. Cruza con P5 (conoce su código fuente).
- [x] ✅ **AC3 · Auto-modificación de su CÓDIGO (con el freno puesto).** Que el agente pueda
      editar su propio código fuente — con RESTRICCIONES duras (qué sí/qué no puede tocar),
      pasando por el GOVERNOR (H11: scanner + kill switch + gate al dueño) y dejando audit
      inmutable. NUNCA tocar: KEK/secrets, el propio governor, la audit chain. Es la
      extensión natural de H12 (hoy auto-genera SKILLS; esto sería auto-modificar CÓDIGO).
- [x] ✅ **AC4 · Auto-modificación de su BASE DE DATOS (con el freno puesto).** Que el agente
      pueda proponer/aplicar cambios a su esquema (nuevas tablas/columnas/migraciones) de
      forma consciente y gobernada (governor + gate + backup previo + audit). Máximo cuidado:
      una migración mala rompe todo → backup obligatorio antes + dry-run + aprobación.

> **Orden lógico (para cuando se diseñe):** AC1+AC2 primero (CONCIENCIA: detectar y conocer,
> bajo riesgo) → AC3+AC4 después (ACTUAR sobre sí mismo, alto riesgo, exige el governor H11
> ya construido + gate + backup + audit). REGLA DE ORO: nada de auto-modificación sin el
> freno (H11) y sin aprobación del dueño. Se DEBATE a fondo (tipo Ronda) antes de programar.
> Relacionado: [[H10-H12 APRENDE]] (governor ya existe) · P4 · P5 · Grafo §8.4 HARD NO-GO.

---

## 🌙 H9 SUEÑA (DMN) — PENDIENTES / DEUDA (Brian 2026-06-26)

> H9 quedó COMPLETO en su estructura (motor + 8 tasks + ROI + /dmn, ver
> `Cuerpo/H9_SUENA_Plan_Maestro_DMN.md`), PERO varias tasks se entregaron como STUB
> HONESTO (declaran su estado, NO fingen trabajo) porque la infra que necesitan aún no
> existe, y hay piezas del diseño R5 que se difirieron. Aquí queda la deuda real para
> retomar. NO urge: las housekeeping reales (embeddings/CLS/eval) ya funcionan; estas
> son mejoras y completar lo stub.

- [ ] **H9-D1 · cache_prewarming REAL — requiere stats de hit/miss en cache.py.** Hoy
      `cache.py` solo tiene get/set, no cuenta aciertos/fallos → el task es STUB (trigger
      siempre False). Falta: (1) contadores de hit/miss por patrón en Valkey; (2)
      `cache.stats_recientes(pool, ws)` (hit_rate + misses recurrentes); (3) que la action
      pre-compute respuestas a los patrones frecuentes que fallan. Outcome medible: hit-rate
      antes vs después (ROI real). Diseño base: R5 §3.2.
- [ ] **H9-D2 · routing_learning REAL — requiere router multi-modelo.** STUB hoy: For3s no
      tiene enrutamiento multi-modelo activo (H7 enrutamiento BLOQUEADO por decisión —
      suscripción plana). Sin rutas que aprender, el task no aplica. Se llena cuando exista
      routing real (API key de pago / cliente). Cruza con H7. Diseño: R5 §3.4.
- [ ] **H9-D3 · eval_regression_detection con GOLDEN SET formal.** v1 usa una métrica simple
      (% respuestas vacías 24h) como proxy. Falta el framework de eval real (R3 §4.4): golden
      set + baseline + score + REGRESSION_THRESHOLD + alerta. Es el GUARDIÁN de la calidad de
      todo el sistema → importante cuando haya clientes. Cruza con H14 (observabilidad) y R8.
- [ ] **H9-D4 · prompt_improvement REAL = AUTO-CONCIENCIA AC3.** STUB hoy (trigger False):
      auto-proponer cambios a la PROPIA personalidad/prompts es máximo cuidado. Se construye
      junto con el pendiente [[AUTO-CONCIENCIA AC3]] (auto-modificar código): propondría
      mejoras de prompt a `dmn_propuestas`, NUNCA auto-editaría FOR3S_ROLE. Diseño: R5 §4.3.
- [ ] **H9-D5 · "valor medible" fino del ROI (R5 §6 completo).** H9-d v1 mide costo + corridas
      + recomendación simple (keep/revisar). Falta el VALOR por task con su métrica propia
      (cache→hit-rate↑, eval→bugs cazados, consolidation→calidad del KG, hypothesis→hipótesis
      confirmadas) para un ratio valor/costo real + auto-suggest disable. Tabla en R5 §6.
- [ ] **H9-D6 · auto-improvement loop de las generativas (R5 §5).** Hoy las generativas dejan
      propuestas y el dueño decide. El diseño R5 §5 contempla un loop: propuesta → governor →
      review → approval → promote → MEDIR resultado → realimentar. Falta el "medir + realimentar"
      (cerrar el lazo de aprendizaje). Reusa el governor (H11) ya construido.
- [ ] **H9-D7 · interaction graph entre tasks (R5 §7).** v1 corre las 8 tasks independientes.
      R5 §7 define contratos entre ellas (ej. embedding_precompute alimenta a
      memory_consolidation; eval_regression vigila a las demás). Orquestar dependencias.
- [ ] **H9-D8 · pattern_detection afinado.** Hoy reusa proponer_skill_auto de H12 con un
      trigger simple (≥10 turnos/24h + autogen ON). Falta detección REAL de patrones repetidos
      (no solo "hay material") — agrupar tareas similares recurrentes antes de proponer skill.

> **Orden sugerido (cuando se retome):** H9-D1 (cache, útil y bajo riesgo) → H9-D3 (eval/golden
> set, importante para clientes) → H9-D5/D6 (ROI fino + loop, cierran el aprendizaje) →
> H9-D2/D4 (esperan H7 / AC3). Todas NO urgen: el DMN ya se mantiene solo con lo real de H9-b.
> Detalle de cada una en el diseño R5 (`Ronda_05_DMN_Tasks_Detailed.md`) + plan H9.

---

## 🧠 H10-PLANEA (metacognición) — PENDIENTES / DEUDA (Brian 2026-06-26)

> H10-PLANEA v1 COMPLETO (confidence scoring + "sé cuándo no sé" en chat, ver
> `Cuerpo/H10_PLANEA_Plan_Maestro_Metacognicion.md`). El R6 §6.1 define más de lo que
> entró en v1; aquí la deuda. NO urge: el comportamiento honesto ya funciona en el chat.

- [ ] **HP1 · Señales 4/5/6/8 reales** (hoy neutras honestas): cost_accuracy (medir estimado
      vs real por turno), plan_consistency (requiere plan-then-execute formal HP4),
      multi_agent_consensus (calcular cuando corre el equipo H8), rule_eval (requiere golden
      set = misma deuda H9-D3). Cada una se llena sin tocar el resto. R6 §6.1.2.
- [ ] **HP2 · Confidence en tool-loop GitHub y en el equipo.** v1 solo aplica en
      conversation.send (chat). Falta evaluar confianza en send_with_tools (¿las tools dieron
      lo esperado?) y en las corridas de equipo (consensus entre specialists). R6 §6.1.2.
- [ ] **HP3 · llm_self_report más fino.** v1 infiere la confianza del FRASEO de la respuesta
      (marcadores de duda, sin 2ª llamada LLM). Opción futura: pedir al modelo un score
      explícito de confianza (más preciso pero +1 llamada/turno). Calibrar costo-vs-precisión.
- [ ] **HP4 · Plan-then-execute formal (motor PFC completo).** v1 mide confianza del TURNO,
      no descompone en un PFCPlan con steps/checkpoints (R6 §6.1.1). El motor de planeación
      multi-step (plan → ejecutar paso a paso → checkpoint) es grande; v1 es la metacognición
      "ligera". Se construye cuando se necesite ejecución compleja gobernada por confianza.
- [ ] **HP5 · Check loop con RE_PLAN_PARTIAL.** v1 en baja confianza solo AVISA / pide
      aclaración. El R6 §6.1.3 define re-planear automático (preservando steps exitosos,
      budget de re-plans, escalado por severidad). Requiere HP4. Decisión Brian: v1 solo avisa.
- [ ] **HP6 · Workspace controls del confidence** (R6 §5.4.3): human_in_loop_on_critical,
      max_re_plans_per_plan, thresholds por workspace. Para multi-tenant / clientes.

> **Orden sugerido:** HP3 (self-report fino, barato) → HP2 (cubrir tool-loop/equipo) →
> HP1 (señales reales conforme llegue su infra) → HP4/HP5 (motor PFC + re-plan, grande) →
> HP6 (multi-tenant). NO urgen: el "sé cuándo no sé" en chat ya da el valor principal.
> Detalle: `Ronda_06_Bloque_1_PFC_Orchestrator.md` + plan H10-PLANEA.

---

## 🚀 DISTRIBUCIÓN / PRODUCTO (Brian 2026-06-27)

> ✅ HECHO: repo oficial público `github.com/fruterito101/for3s` ("el repo de la verdad"),
> AGPL + firmado + gobernanza completa. Ver memoria [[project_repo_oficial_for3s]] y
> [[project_fase_pretesters]]. ⭐ REGLA LOCKED: cada actualización YA VERIFICADA se sube ahí.

> ⏸️ **Los 5 pendientes de esta sección se MOVIERON a §EXTRAS (Brian 2026-07-01):** Plan de
> descubrimiento · Probar `curl|sh` en Linux limpio · Dominio+landing · v1.1 hermanos de red ·
> Monetización Open Core. Ver detalle en la sección §EXTRAS (arriba del doc).

---

## 🏢 MULTI-INSTANCIA — ✅ COMPLETO 2026-07-02 (MI-1 + MI-2 + MI-3, EN PRODUCCIÓN)

> ✅ **CONSTRUIDO Y VERIFICADO** → `Cuerpo/Ronda_Multi_Instancia_Plan.md`. Gestor LOCAL: comando
> `for3s` (agregar / entrar = chat de consola de esa instancia / encender / apagar / borrar) para
> varios For3s aislados en la máquina (personal + clientes). **Aislamiento TOTAL** vía `docker compose
> -p for3s-<nombre>` (plantilla `docker-compose.instancia.yml`, NO toca Foresito) + estado por
> instancia en `~/.for3s/<nombre>/` + modo solo-consola. El comando nace con el instalador (install.sh
> lo pone en el PATH; uninstall.sh baja todas las instancias). **Verificado E2E:** instancia aislada
> creada, su BD/KEK separadas de Foresito, chat responde, borrar limpia, Foresito INTACTO. 7 bugs
> cazados (5 hardcodeos de aislamiento + KEK base64 + loop por token inválido). Commits firmados
> 7a71e55·61df2cf·cc87f7d. Diferido a §EXTRAS: MI-EXTRA-1 SaaS remoto · MI-EXTRA-2 botón web on/off.
> Los 3 items de abajo = las fases, ya HECHAS.

> **El problema:** hoy un servidor corre **UN solo** For3s OS (el contenedor de Foresito).
> Pero Brian quiere poder correr **VARIOS For3s OS aislados a la vez** en el mismo servidor,
> cada uno en su(s) propio(s) contenedor(es) — como los 4 demos que ya existían
> (`for3s-demo-general/brian/mashe/jazz`, hoy parados) + el Foresito en uso. **Esa estructura
> de "más contenedores / más perfiles de For3s" NO EXISTE todavía** y es algo importante.
>
> ⚠️ Estado de los 4 demos (2026-06-28): **PARADOS** (`docker stop`, quedan `Exited`, NO borrados =
> recuperables). Brian: dejarlos así. Cuando terminemos los pendientes y el sistema esté
> adecuado → con ellos vamos a **crear algo nuevo** = esta estructura multi-instancia.

- [x] ✅ **Diseñar la estructura multi-instancia** (debatir tipo Ronda antes de codear). Preguntas clave:
      - ¿Cada perfil = su propio docker-compose (stack completo: agent+worker+postgres+valkey)
        aislado, o comparten Postgres/Valkey con esquemas/DBs separadas por perfil? (trade-off:
        aislamiento total vs RAM — el server tiene ~19GB; cada stack completo pesa).
      - ¿Cómo se nombra/enruta cada perfil? (puertos, redes Docker, KEK por perfil en `~/.for3s/<perfil>/`,
        `.env` por perfil, token de Telegram distinto por perfil).
      - ¿Cómo se crea/arranca/para/borra un perfil? (¿un comando `for3s create <perfil>`?
        ¿plantilla de compose parametrizada por nombre?).
      - ¿Cómo se garantiza el AISLAMIENTO de memoria entre perfiles? (cada uno su BD/KEK/grafo;
        NUNCA se cruzan datos — igual de estricto que el aislamiento multi-usuario de H8).
      - Healthcheck/monitoreo por perfil (cruza con PR2 salud) + límites de RAM por contenedor.
- [x] ✅ **Decidir relación con multi-usuario (H8):** H8 = varios USUARIOS dentro de UN For3s
      (memoria híbrida privada/común). Esto es distinto: varios FOR3S enteros aislados. Aclarar
      cuándo usar cada uno (¿un perfil multi-instancia POR cliente/empresa, y dentro de él H8
      para su equipo?). Probablemente multi-instancia = capa de "tenant/empresa", H8 = capa de
      "equipo dentro del tenant".
- [x] ✅ **Implementar** (MI-1+MI-2+MI-3 hechos 2026-07-02): plantilla + tooling para levantar N perfiles.
- ⚠️ Cruza fuerte con: distribución (cada tester/cliente podría ser un perfil) · PR2 salud
      (monitorear N stacks) · PR6 dueños · el modelo de negocio (multi-tenant = base del SaaS).
- Refs: los 4 demos parados son el material de partida. Memoria: [[project_multi_instancia]].

---

## 🖥️ MANTENIMIENTO DEL SERVIDOR (Brian 2026-06-29) — NOSOTROS damos mantenimiento al server

> Brian: "le tenemos que dar mantenimiento del servidor". Dos problemas detectados el 29-jun
> durante la sesión de bugs. NO son físicos → son driver/software → SE PUEDEN solucionar.
> Nos afectaron toda la sesión (cortaron builds, SSH, /salud). Diagnóstico técnico capturado.

- [x] ✅ **MS-1 · RESUELTO (software) 2026-06-30 — WiFi principal + asix respaldo + fixes a fondo.**
      La red del server salía SOLO por el adaptador USB-Ethernet ASIX AX88772A (0b95:772a) que
      ciclaba Link Up/Down → cortaba builds/SSH/envíos. **SOLUCIÓN:**
      1. ✅ **Activado el WiFi Intel 8260** (`wlp1s0`) como salida PRINCIPAL — estaba DOWN por RF-kill
         (`soft=1`); desbloqueado vía /sys + systemd-rfkill (persiste reinicios) + netplan
         (00-installer-config.yaml, WiFi `optional:true`, red HUAWEI_Wi-Fi5). IP 192.168.3.11,
         **metric 600** (preferida sobre el asix metric 1024). El tráfico YA va por WiFi (verificado
         `ip route get 8.8.8.8` → dev wlp1s0). La red del server YA NO depende del asix.
      2. ✅ **Fixes a fondo del asix** (causas reales de "muere bajo carga / se va solo"): USB
         autosuspend desactivado (era 2000ms → `control on` + autosuspend `-1`) + **regla udev
         persistente** `/etc/udev/rules.d/99-asix-nopower.rules` (se aplica sola al reconectar →
         resuelve el "conectar/desconectar manual") + autoneg probado.
      3. 🔧 **Lo que QUEDA es FÍSICO → MOVIDO a §EXTRAS (Brian 2026-07-01).** El asix sigue
         `Link detected: no` (cable defectuoso/flojo o adaptador degradado). NO urge (el WiFi cubre)
         y requiere acceso físico de Brian → diferido a EXTRAS. Detalle completo en la sección §EXTRAS.

- [x] ✅ **MS-2 · RESUELTO 2026-06-30 (por MS-1).** Era síntoma de MS-1 (el reporte de /salud se
      genera bien pero no se enviaba cuando la red caía). Con el WiFi estable como principal, la red
      del server ya no parpadea → /salud y las respuestas del bot llegan. ⭐ VALIDÓ el monitoreo:
      la alerta "Render: ConnectError" que llegó fue real (parpadeo de red), Foresito avisó solo.
      ⏳ Mejora opcional futura (no urge): encolar+reenviar respuestas del bot ante cualquier corte
      de red (robustez extra; hoy reintenta 5x con _responder_seguro).

---

## 🔴 SEGURIDAD (crítico — atender pronto)

- [x] ✅ **SEC-1 · TOKEN DE GITHUB EXPUESTO — RIESGO ACEPTADO POR BRIAN (decisión consciente, 2026-06-30).**
      Cazado al sincronizar el repo de la verdad (PR9): el remoto `backup` de `~/for3s-os` tiene un
      token OAuth `gho_...` EN TEXTO PLANO en la URL (visible con `git remote -v`). ⛔ **Brian decidió
      NO rotarlo, conociendo el riesgo** → marcado como completado/cerrado por decisión del dueño, NO
      es un olvido. Si en el futuro cambia de opinión: rotar en GitHub (Settings → Developer settings)
      + reconfigurar el remoto sin token en la URL (credential helper / deploy key SSH / GH_TOKEN env).
- [x] ✅ **SEC-2 · Dependabot RESUELTO 2026-06-30 (commit firmado 32f68db).** Era
      `pydantic-settings` (GHSA-4xgf-cpjx-pc3j, CVSS 5.3 medium): `NestedSecretsSettingsSource` sigue
      symlinks fuera de `secrets_dir`. 🔍 Análisis a fondo: (1) NO usamos esa función (usamos KEK +
      SecretStore propio) → riesgo real ~nulo; (2) el contenedor YA corría 2.14.2 (parcheado), pero el
      `uv.lock` estaba en 2.14.1 → Dependabot miraba el lock. FIX: `uv lock --upgrade-package
      pydantic-settings certifi` → lock alineado con lo que corre (pydantic-settings 2.14.2 + certifi
      2026.6.17, diff quirúrgico de 12 líneas). Pusheado; Dependabot auto-cierra al re-escanear.
      🔍 **Auditoría de COMPONENTES HERMANOS (Brian pidió, 2026-06-30):** los 7 contenedores SANOS ·
      MCP read+write conectan (21 tools c/u, el write casi nunca se ejerce pero funciona) · render OK
      (`{"ok":true}`) · NINGÚN proceso hermano roto. Hallazgos menores: (a) agent y worker corren
      IMÁGENES DISTINTAS (worker en build vieja por hash, agent `:local` — worker no necesita comandos
      del bot, no rompe pero conviene rebuild del worker algún día); (b) el lock estaba desfasado del
      contenedor en 2 paquetes, no 1 (certifi también). Sin más alertas Dependabot.

### 🚨 CONFIANZA DE PRODUCTO — 4 URGENTES (Brian 2026-07-03, elegidos tras análisis de internet)

> **Contexto:** análisis (NIST/OWASP + Microsoft Agent Governance Toolkit + OpenSSF) de qué necesita
> For3s para ser un PRODUCTO con valor de confianza/seguridad/cripto. For3s YA tiene la parte difícil
> (audit inmutable + hash chain = lo que Asqav vende como novedad 2026; KEK offline; commits+releases
> firmados GPG; Dependabot). **Lo que FALTA es hacerlo VISIBLE y verificable por terceros.** Estas 4 dan
> el mayor salto de confianza por menos esfuerzo. **TODAS GRATIS** (repo público). Marcadas URGENTES por
> Brian. Análisis completo: `memory/archive/For3s_Bot_vs_Agente_vs_Hermes.md` + fuentes en la memoria de la sesión.

- [x] ✅ **🚨 SEC-3 · OpenSSF Scorecard — HECHO 2026-07-03. Score inicial 5.7/10.** Workflow
      `.github/workflows/scorecard.yml` (actions PINEADAS POR SHA, permisos mínimos, semanal+branch_protection)
      + badge en README + dependabot.yml + permisos explícitos en ci.yml + **branch protection en main**
      (CI debe pasar + sin force-push/deletion) + Dependabot security updates activado. **Score real por check:**
      ✅ 10/10: Token-Permissions · Dependency-Update-Tool · Security-Policy · License · Vulnerabilities ·
      Dangerous-Workflow · Binary-Artifacts. 🟡 Branch-Protection 3 (subió de 0; el resto = reviewers, NO
      aplica a 1 dev). 🟡 Pinned-Dependencies 1 (→ sub-tarea abajo). ❌ SAST 0 (→ SEC-6 CodeQL), Fuzzing 0
      (→ QA-2 Hypothesis), Signed-Releases -1 (→ SEC-5, no hay releases aún), CII-Best-Practices 0,
      Maintained 0 (solo porque el repo tiene <90 días → sube solo con el tiempo). Commits bda9ccd/8b0013b.
  - [x] ✅ **SEC-3b · Pinear las 5 imágenes Docker por SHA — YA HECHO** (verificado 2026-07-16): las 5 FROM
        tienen su `@sha256:...` — python:3.12-slim@sha256:423ed6ab (agent/workspace/sandbox) · apache/age
        :release_PG16_1.6.0@sha256:16aa423d (postgres) · playwright:v1.60.0-noble@sha256:9bd26ad9 (render).
        Imagen inmutable (imposible que un `:tag` traiga algo distinto en el próximo build). Sube Pinned-Deps.
- [x] ✅ **🚨 SEC-4 · Container scanning (Trivy) — HECHO 2026-07-03.** Workflow `.github/workflows/trivy.yml`
      (actions pineadas por SHA), diseño en 2 modos por el tamaño real (imagen agent = **13.2GB**, no cabe
      construirla en el runner gratis): **fs-scan** (deps uv.lock + secretos) BLOQUEANTE + **config-scan**
      (los 5 Dockerfiles, misconfig IaC) informativo → ambos SIEMPRE, rápidos; **image-scan** SOLO manual
      (`workflow_dispatch`, construye la sandbox 580MB como demo). GRATIS. 1er run verde. 🔍 **Hallazgos:**
      (a) ✅ deps `uv.lock = 0 vulnerabilidades` (limpio → fs-scan pasó a bloqueante); (b) 🟡 2 Dockerfiles
      con misconfig HIGH → ver SEC-4b abajo. Commits 2b8e96a/4472e3d. Cruza con CI-3 (build docker).
  - [x] ✅ **SEC-4b · Endurecer el agent a non-root → RESUELTO por SEC-4c (2026-07-16).** Las instancias
        EXPUESTAS corren non-root (usuario for3s uid 1000, gosu); las internas root por perfil. Ver
        `Cuerpo/Ronda_SEC4c_NonRoot_Perfil_Instancia.md` + [[feedback_nunca_chown_bind_mount]]. render
        (Playwright) ya era non-root desde antes. El `.trivyignore` DS002 se actualizó con la justificación
        honesta (Trivy = análisis estático → ve root; el descenso a non-root es dinámico en el entrypoint).
- [x] ✅ **🚨 SEC-5 · SBOM + Sigstore — HECHO 2026-07-03.** Workflow `.github/workflows/release.yml` (actions
      pineadas por SHA), dispara en tag `v*` (+ workflow_dispatch para probar): (a) **SBOM** del código fuente
      con syft en 2 formatos (SPDX + CycloneDX) = inventario de componentes; (b) **firma Sigstore/cosign**
      keyless (OIDC, sin llaves que gestionar, complementa el GPG de Brian); (c) **GitHub Release** con SBOM +
      firmas adjuntas (solo en tag real). Diseño adaptado a For3s: se distribuye por código+Docker (curl|sh),
      NO como paquete pip → SBOM del código fuente. **Verificado con workflow_dispatch:** SBOM (ambos formatos)
      + firma Sigstore + artifact = todo verde. Commits 4fb08c8/d81217e.
      **✅ RELEASE REAL CREADO Y VERIFICADO (2026-07-03):** se creó el tag **v0.14.0 firmado GPG** (1er release
      oficial del producto, coincide con version.py) → disparó el workflow → **GitHub Release v0.14.0 publicado**
      con 4 assets: for3s-sbom.spdx.json + for3s-sbom.cdx.json + sus 2 firmas .sigstore.json. Esto RESUELVE el
      status 400 anterior (workflow_dispatch corría sobre rama sin tag; el step Create Release ahora es
      condicional a `refs/tags/`). Sube Signed-Releases del Scorecard (era -1, ahora hay release firmado).
      Aviso menor: upload-artifact usa Node 20 (deprecado) → Dependabot lo actualiza solo. Opcional futuro:
      SLSA provenance (`*.intoto.jsonl`, nivel oro). 🎉 **LOS 4 URGENTES DE CONFIANZA (SEC-3/4/5/6) COMPLETOS.**
- [x] ✅ **🚨 SEC-6 · CodeQL — HECHO 2026-07-03.** Workflow `.github/workflows/codeql.yml` (actions pineadas
      por SHA, permisos mínimos): analiza **python** (security-extended) + **actions** (los workflows), sin
      build (Python interpretado). Matriz 2 lenguajes, ambos ✅ en el 1er run (58s). GRATIS repo público.
      Sube el check SAST del Scorecard (0→10). 🔍 **CAZÓ 1 alerta REAL que bandit NO detectó:**
      `py/incomplete-url-substring-sanitization` en `_quitar_urls_no_github` (`"github.com" in url` → un
      `evil-github.com.attacker.io` pasaría como github). FIX: verificar github.com como HOST real (regex
      `^https?://([^/]+\.)?github\.com([/:?#]|$)`). Riesgo era cosmético (filtro de texto, no seguridad) pero
      se arregló bien = CodeQL limpio. Verificado E2E (github real pasa, evil-github/tvazteca NO). Commits
      52a80b4/07a3dfa. **Demostró su valor: el análisis de flujo encuentra lo que el escaneo de patrones no.**

> **Prioridad:** SEC-3 (Scorecard = el sello visible) + SEC-4 (Trivy = hueco real) primero. SEC-5 (SBOM/
> Sigstore) + SEC-6 (CodeQL) después. Las 4 GRATIS. For3s ya tiene la cripto difícil (audit/KEK/GPG); esto
> la hace VERIFICABLE por terceros = el salto de "tengo seguridad" a "puedes confiar, aquí está la prueba".
> ⚠️ NADA de cara al usuario en producción — son workflows de CI (calidad/confianza del repo).

- ✅ **Rotar tokens expuestos en chat** (Brian, 2026-06-18): rotados los 3 tokens
      (Claude OAuth, bot Telegram, OpenCode) en sus plataformas + actualizado el
      SecretStore/.env del bot. Los valores viejos expuestos en chat ya NO sirven.
- ✅ **PAT de GitHub migrado a `ghp_` clásico** (2026-06-18): de `gho_` (gh CLI) a
      PAT clásico `ghp_` scope `repo` + 90 días. Guardado cifrado en SecretStore,
      bot reiniciado, GitHub verificado OK.
- ✅ **PAT expuesto en chat → ROTADO** (Brian, 2026-06-18): el `ghp_` que se pegó en
      la conversación fue manejado/rotado por Brian de su lado. Cerrado.

---

## 🟡 DEUDA TÉCNICA del MVP (atender durante el pulido)

- ✅ **Tests de los módulos nuevos** (2026-06-18): 37 tests de lógica pura (sin red)
      en `tests/test_pulido_mvp.py` — cubren subbloques (categorías, capas de
      ejecución, reparto simple/profundo, recencia), md_html (conversor MD→HTML,
      escape, balance de tags), tiempo (zonas), web_fetch (parseo HTML), y los
      detectores org/repo/modo de conversation. Suite total: 101 pasan + 4 skip.
- ✅ **test_h4.py migrado** (2026-06-18): se quitaron los tests del artesanal
      (github_tool); quedan los vigentes (crypto/KEK + sandbox). Lo nuevo se cubre
      en test_pulido_mvp.py.
- ⏸️ **Imagen del CI sin Apache AGE** (grafo) — POSPUESTO A H5 (decisión Brian
      2026-06-18). AGE es para el grafo de H5, que NO existe aún; el código de hoy
      no usa AGE. Cambiar la imagen ahora sería preparar algo sin usar. Se hace
      cuando se construya H5.

### 🧪 MEJORAS DE CI/CD (Brian 2026-07-03) — subir el nivel de "producto serio"

> **Contexto:** el CI (GitHub Actions) tiene hoy 3 checks: (1) **Lint+Types+Tests** (ruff + pytest,
> el que cazó el bug de seguridad de _autorizar el 2026-07-03), (2) **SAST bandit** (escáner de
> seguridad), (3) **Pilar 3 Gate** (check propio del governor, esqueleto). Funciona y demostró su
> valor. Estas 5 mejoras lo llevan a nivel producto. NINGUNA es urgente (el CI ya está verde).

> **✅ CERRADO 2026-07-16 (tarde) — CI 100% VERDE + secret scanning.** Al atacar este bloque se cazó
> que el CI llevaba en ROJO desde v0.17.0 (~2 versiones, nadie lo vio). Commits `5b47cb9`→`ba5fef5`
> firmados, tríada en `ba5fef5`. Detalle en `memory/Bitacora_Progreso.md` (2026-07-16 tarde).

- [x] ✅ **CI-1 · Secret scanning (gitleaks) — HECHO Y VERDE.** gitleaks bloqueante en el job security
      (binario pinned v8.28) + `.gitleaks.toml` (allowlist de 3 falsos positivos verificados). Verificado
      a FONDO: detecta secretos reales y bloquea (exit 1); el historial público está LIMPIO (0 secretos
      reales en 195 commits). ⭐ Casi se commitea "teatro de seguridad" (el 1er config desactivaba las
      reglas sin querer) — la curiosidad lo cazó. Conecta con la higiene del token de hoy.
- [x] ✅ **CI-2 · Coverage — CERRADO 2026-07-16.** `pytest --cov` + umbral **ANTI-RETROCESO
      `--cov-fail-under=15`** (cobertura real ~19%; For3s es I/O-pesado, mucho se prueba E2E server-primero,
      así que un 15% realista bloquea si cae mucho —ej. borran tests— sin teatro de "100% coverage").
- [~] **CI-3 · Build de Docker en el CI** — parcial: trivy-image construye la imagen sandbox (manual);
      la imagen agent (13GB) no cabe en el runner (decisión consciente). **Ahora el CI SÍ buildea
      `docker/Dockerfile.postgres`** (para las migraciones E2E con AGE). Un build de la imagen agent
      completa sigue diferido por tamaño.
- [x] ✅ **CI-4 · Badge de CI — HECHO.** Ya había badges (CI/CodeQL/Trivy/Scorecard); el de tests decía
      "141 passing" (mentira, son 244) → cambiado a "tests-passing" sin número (no vuelve a mentir).
- [x] ✅ **CI-5 · pip-audit — YA existía + reforzado.** El job security ya corre pip-audit. Se ignoró
      PYSEC-2026-3447 (setuptools<83) con justificación (su fix arrastra torch 2.12→2.13 = core de
      embeddings, más riesgo que la vuln). Dependabot cubre pip + github-actions.

> **Bugs del CI cazados y arreglados en el mismo pase (rojo desde v0.17.0):** Format check (16 archivos
> de deuda → ruff format) · bandit (3 falsos positivos → nosec inline) · **Migraciones E2E fallaban por
> falta de AGE en el CI** (imagen pgvector sin age → ahora buildea la imagen de producción con age+pgvector;
> NO afectaba producción). **SEC-4c (Dockerfile non-root) queda para sesión dedicada** (delicado: toca
> paths de volúmenes/KEK/modelo de las 5 instancias).

### 🛡️ BLINDAJE DE CALIDAD — las 3 de MÁS IMPACTO (Brian 2026-07-03, PRIORITARIAS)

> **Contexto:** más allá de ruff/bandit, hay herramientas más POTENTES para un agente con BD + estados +
> texto libre. Brian eligió las 3 de mayor impacto. **TODAS GRATIS** (open-source + CI de repo público es
> ilimitado gratis). Habrían cazado varios bugs de la sesión 2026-07-02/03. Ninguna urgente; el CI ya está
> verde. Análisis completo: [[project_sesion_bugs_2026-07-02]] + este documento.

- [x] ✅ **QA-1 · Test de migraciones E2E en el CI — HECHO 2026-07-03.** Step "Migraciones E2E" en el job
      `quality` del ci.yml: sobre la BD LIMPIA que el CI ya levanta (pgvector/pgvector:pg16 + pgcrypto+vector),
      aplica las 32 migraciones desde 0 (`uv run python -m for3s_core.cli migrate`) + **verifica afirmativamente**
      que schema_version llega a 32 (falla el CI si no). Va antes de pytest (idempotente). Verificado en el CI:
      `migraciones en disco: 32 | schema_version aplicada: 32 | OK`. Ninguna migración usa AGE en SQL real
      (solo comentario en 001) → el CI las aplica todas sin AGE. 🐛 **cazó un acoplamiento al construirlo:**
      `cli migrate` exigía ANTHROPIC_TOKEN (cargaba Settings completo) → arreglado: `migrate_only` lee
      DATABASE_URL del entorno directo, sin token (más robusto; el guardián que usa migrate sigue OK).
      Commits b6aff6c/342fd09. **Habría cazado los bugs de BD de la sesión (FK perfil→personas).**
- [x] ✅ **QA-2 · Hypothesis (property-based testing) — HECHO 2026-07-03.** `tests/test_property_based.py`
      (9 tests) + `hypothesis>=6` en dev deps. Hypothesis genera cientos de inputs raros y busca el que rompe.
      Propiedad universal: NINGUNA función de texto libre crashea con ningún input. Cubre: `parsear_comando`
      (C1), `parsear_decidi` (C2), `huele_a_codigo`/`huele_a_github`, `_es_pregunta_*`, `_norm_texto`,
      `_conceptos_exactos` (C3). 🐛 **Hypothesis cazó un bug REAL que jamás habría probado a mano:**
      `_norm_texto` hacía `.lower()` ANTES de NFKD → un carácter unicode raro (`𝐀` matemático) quedaba en
      mayúscula tras NFKD → fix: lower DESPUÉS de NFKD→ascii. (+ ajusté deadline=None en los tests que
      compilan regex la 1ª vez = falso positivo de timing, no bug.) 141 tests pasan (132+9), CI verde.
      Commits 132559b. **Demostró su valor: encontró un caso Unicode que ni imaginé.** Extra futuro: stateful
      testing para equipo/puerta/roles (secuencias de acciones).
- [x] ✅ **QA-3 · type-check estricto (gradual) — HECHO 2026-07-03.** Step "Types críticos (ty, BLOQUEA)" en
      el ci.yml: `ty check` BLOQUEANTE sobre los 5 módulos nuevos/críticos (memoria, perfil, tema_estado,
      decisiones, execute) que están LIMPIOS (0 errores). Un bug de tipo NUEVO ahí (ej. el FK perfil→personas)
      rompe el CI. 🔍 hallazgo: `ty` reporta **72 diagnostics en todo el repo** (25 invalid-argument-type,
      17 unresolved-attribute, etc. — mezcla de reales + ruido de ty experimental que no maneja bien asyncpg/
      tipos dinámicos). Hacerlos TODOS bloqueantes rompería el CI → enfoque GRADUAL: bloquea los críticos,
      el resto sigue en el paso informativo. CI verde. Commit febd647.
  - [ ] **QA-3b · Limpiar los 72 errores de tipo del resto del repo (gradual, para ampliar el bloqueo).**
        Módulo por módulo, arreglar los diagnostics reales de `ty` (o `# type: ignore` justificado en el ruido
        de ty experimental) → ir ampliando la lista de módulos del step bloqueante hasta cubrir todo. No urgente.

> **Prioridad:** QA-1 (migraciones, el hueco más grande + más barato) → QA-2 (Hypothesis, caza bugs de texto
> libre) → QA-3 (mypy, gradual). Las 3 GRATIS. Habrían cazado bugs REALES de la sesión 2026-07-02/03.
> **Lo único que costaría tokens** (NO en esta lista, es aparte): evals de LLM (promptfoo/deepeval) que ya
> tiene semilla en el DMN (`eval_regression`) — ese consume cupo, los QA-1/2/3 son 100% gratis.

### 📊 ESTADO CONSOLIDADO DEL CI — 🎉 RONDA 100% CERRADA (2026-07-03)

> Brian pidió (2026-07-03) barrer TODO el CI. **La ronda de CI de confianza está COMPLETA y pusheada
> firmada a GitHub (5 checks verdes).** Detalle vivo en la memoria [[project_sesion_bugs_2026-07-02]].

**✅ LOS 5 WORKFLOWS EN VERDE (verificado):** CI (quality: ruff+format+ty-crítico+migraciones-E2E+
Hypothesis+pytest, 141 tests · security: SAST+deps+gate) · CodeQL · Trivy · Scorecard · Release. Cada uno
cazó algo real. (+ trivy-image.yml manual, workflow aparte que no ensucia los checks del push.)

**✅ TODO HECHO:** SEC-3 Scorecard (5.7/10) · SEC-4 Trivy · SEC-5 SBOM+Sigstore (release v0.14.0 firmado) ·
SEC-6 CodeQL · QA-1 migraciones E2E · QA-2 Hypothesis · **QA-3/3b/3b-v3 ty-crítico bloqueante sobre TODO el
core (cero módulos sucios, cero `type: ignore`)** · CI-2 coverage · CI-4 badges · CI-5 pip-audit · SEC-3b
imágenes pineadas · SEC-4b render non-root · SEC-4c agent root justificado · RENDER-1 límites · Dependabot #2
mergeado · branch protection en main.

**✅ LIMPIEZA "CARA DE PRODUCTO" (2026-07-03, tras duda de Brian "¿es demasiado CI?"):** análisis → NO es
bloat (es el estándar de producto serio), pero sobraba ruido visual. (1) agrupé SAST+pip-audit+Pilar 3 Gate
en 1 job `Seguridad (SAST + deps + gate)`; (2) saqué el Trivy image-scan (13GB, manual) a `trivy-image.yml`
propio → ya no sale "Skipped" en cada push; (3) branch protection al nuevo nombre. De 8 checks a los
esenciales, cobertura intacta. El Pilar 3 Gate se QUEDA (dormido = freno de auto-generación H11/H12 =
diferenciador del producto). Commit 2118907 firmado. **Docs del repo:** CHANGELOG 0.13/0.14 + badge Trivy (063d9f6).

- [x] ✅ **SEC-4c RESUELTO 2026-07-16** (commits `c37ae1f`→`021292e`, tríada `021292e`, CI verde):
  contenedor non-root con **PERFIL POR INSTANCIA** (Brian: internas de la empresa con poder, expuestas
  blindadas). `FOR3S_PERFIL=interna`(root)/`expuesta`(non-root); DEFAULT SEGURO=expuesta. Usuario `for3s`
  uid 1000 (=host, dueño natural de los bind mounts) + gosu; KEK/modelo por ENV (no Path.home()). `/soy`
  muestra el perfil. **Matriz:** Foresito/brian=root, general/jazz/mashe=non-root. Verificado en vivo
  (KEK descifra, modelo, backup, execute_code, panel, /salud 0 FAIL, host intacto). 5 bugs cazados en
  jazz (1 catastrófico: chown -R rompió el HOST → [[feedback_nunca_chown_bind_mount]]). `.trivyignore`
  DS002 actualizado con la justificación honesta (Trivy = análisis estático; el descenso a non-root es
  dinámico). Ronda: `Cuerpo/Ronda_SEC4c_NonRoot_Perfil_Instancia.md`.

**🔍 Hallazgos del hito FOR3S_ROLE (2026-07-04, registrados, no urgentes):**
- [x] ✅ **CUPO-PIN RESUELTO 2026-07-04** (commit 1183602, verificado EN VIVO por Brian) — el pin de
  cupo se quedaba congelado (46%) porque apuntaba a un mensaje >48h que Telegram no deja editar; el viejo
  seguía fijado tapando el nuevo. FIX: _unpin_viejo() des-fija el pin viejo al fallar el edit. Ahora se
  actualiza en vivo (9% real). Los headers de Anthropic siempre llegaron bien.
- [x] ✅ **MODS-VOL RESUELTO 2026-07-04** (commit 0ac215b) — `/app/mods` ahora es volumen for3s-mods
  (agent+worker); las auto-mods de código persisten en rebuild. Verificado E2E (marcador sobrevive reinicio). ~~ → las auto-modificaciones de código de AC
  (auto-modificación AC1-AC4) NO persisten tras un `docker compose up` con rebuild (viven solo en el
  filesystem del contenedor). Afecta a AC, NO al hito (la capa persona SÍ persiste, volumen `for3s-persona`).
  Fix: montar `/app/mods` como volumen nombrado (como se hizo con persona en F2). Bajo riesgo.
- [x] ✅ **SALUD-MCP RESUELTO 2026-07-04** (commit 0ac215b) — el 401 del MCP ya se lee como "vivo
  (requiere sesión MCP, normal)"; nunca fue un fallo. ~~salud_integraciones reporta MCP 401** con un GET pelón aunque el MCP esté SANO
  (el handshake real da 21 tools read). Falso negativo del chequeo de /salud (usa GET simple en vez del
  handshake streamable-http del MCP). Cosmético — el MCP funciona. Fix: que el chequeo use el cliente MCP
  real o acepte 401/406 como "vivo pero requiere sesión".

**🔍 REVISADO — NO son errores (aclarado en el barrido):**
- Las **18 "alertas" de code-scanning** son del propio **Scorecard** (sus checks suben como alertas), NO
  vulnerabilidades del código. Las 3 "high" = CodeReview, Maintained, BranchProtection → **no aplican a un
  proyecto de 1 dev** (review 2+ personas, repo <90 días). Esperado, no se arreglan.
- El "X exit code 1" que a veces se ve en el job quality = el step `ty` INFORMATIVO de los 72 errores viejos
  (tiene continue-on-error) → NO rompe el CI (conclusión global = success).
- El aviso "Node 20 deprecado" en upload-artifact (Release) → Dependabot lo actualiza solo.

**✅ CERRADO 2026-07-03 (2ª tanda):**
- **CI-2 coverage** — pytest `--cov=for3s_core` en el CI. Baseline 17% (honesto: módulos LLM/integración
  sin tests unitarios — equipo/dmn/multiagente). Reporta, no bloquea aún.
- **CI-5 pip-audit** — job `deps-audit`: exporta deps (sin el paquete local) + pip-audit. Verificado:
  "No known vulnerabilities" (279 deps). Complementa Dependabot.
- **Dependabot PRs: 4/5 MERGEADOS** (setup-uv, scorecard-action, codeql-action, upload-artifact — este
  arregló el aviso Node 20). Falta #2 (checkout 4→7): bloqueado por branch-protection strict (rama
  desactualizada) → se le pidió `@dependabot rebase`, se completa solo. ✅ los 5 workflows siguen verdes
  tras los merges. ⭐ **La branch protection PROBÓ que funciona** (bloqueó merges de ramas no actualizadas).

**⏳ PENDIENTES REALES que quedan (DELICADOS — requieren rebuild/E2E, no meter al vuelo):**
- **SEC-3b** — pinear las 5 imágenes Docker por SHA (Scorecard dio los SHA; requiere rebuild + prueba E2E
  de que el bot arranca con la imagen pineada).
- [x] ✅ **SEC-4b (render) — HECHO 2026-07-03.** `USER pwuser` (uid 1001, non-root que trae la imagen
  Playwright) en docker/render/Dockerfile. Verificado E2E: render corre como pwuser + renderizó example.com
  de verdad (Chromium lanza non-root OK). Cierra el DS-0002 del render.
- [x] ✅ **SEC-4c — RESUELTO 2026-07-16 (sesión dedicada hecha).** Contenedor non-root con **PERFIL POR
  INSTANCIA** (Foresito/brian=interna root; general/jazz/mashe=expuesta non-root uid 1000; gosu). KEK y
  modelo por ENV (FOR3S_STATE_HOME/HF_HOME, no Path.home()). `/soy` muestra el perfil. Verificado en vivo
  (KEK descifra, modelo, backup, /salud 0 FAIL, host intacto). 5 bugs cazados en jazz (1 catastrófico:
  chown -R rompió el HOST → [[feedback_nunca_chown_bind_mount]]). `.trivyignore` DS002 actualizado.
  Commits `c37ae1f`→`021292e`. Ronda: `Cuerpo/Ronda_SEC4c_NonRoot_Perfil_Instancia.md`.
- [x] ✅ **RENDER-1 — HECHO 2026-07-03.** El render NO tenía mem_limit/pids_limit en el compose (solo el
  sandbox; el grep engañaba) → causaba los 2× "can't start new thread". Fix: `mem_limit: 1536m` +
  `pids_limit: 512` (Playwright necesita más holgura que el sandbox). Verificado: límites aplicados
  (mem 1.5G/pids 512) + render sano + renderiza. Ya no es vulnerable a picos de threads.
- [x] ✅ **SEC-3b — HECHO 2026-07-03.** Las 5 imágenes Docker pineadas por SHA (python:3.12-slim@423ed6ab en
  agent/workspace/sandbox · apache/age@16aa423d postgres · playwright@9bd26ad9 render). SHA VERIFICADOS vía
  docker pull = imágenes actuales → cero cambio. Rebuild agent + E2E: guardián/KEK/migración/embeddings OK,
  9 hermanos sanos. 🐛 cazado: comentario inline en FROM rompía el parse de Docker → comentario aparte. Sube
  Pinned-Dependencies del Scorecard. Commit 7653aba.
- [x] ✅ **QA-3b — HECHO 2026-07-03 (v1).** Los 72 errores de ty se concentran en solo 6 archivos
  (telegram_channel 59, conversation 12, equipo, audit, mcp_client, etc.). Los **36 módulos restantes están
  LIMPIOS** → el step ty-crítico del CI se amplió de 5 a **36 módulos bloqueantes** (memoria, kg, dmn,
  governor, health, execute, backup, crypto…). Un bug de tipo nuevo en cualquiera rompe el CI. CI verde.
  Commit 1df3126. **QA-3b v2 (queda):** limpiar los 6 archivos sucios (gradual) e ir sumándolos al bloqueo.
- [x] ✅ **CI-4 — HECHO 2026-07-03.** Badges CodeQL + "tests 141 passing" en el README (SIN el % de coverage,
  que en 17% se ve mal y daña la percepción — decisión honesta). README con 5 badges: CI · CodeQL · tests ·
  Scorecard · License. Commit 85eefba.
- [x] ✅ **QA-3b v2 — HECHO 2026-07-03. Cazó 2 bugs REALES de tipo:** (1) `perfil_infer._provider` usaba
  `Settings()` sin args (crasheaba al correr la inferencia nocturna) → `load_settings()`; (2) el protocolo
  abstracto `LLMProvider.complete` no declaraba `adjuntos` (multimodal) → añadido. Tras arreglarlos, de 6
  archivos sucios quedan solo **3** (telegram_channel 59, conversation 7, cache 1); los 9 recién limpiados
  (equipo, audit, mcp_client, subbloques, secret_store, perfil_infer, tool_loop, llm, agent) SUMADOS al
  ty-crítico → **~45 módulos bloqueantes**. 141 tests pasan. Commit 85eefba.
  - [ ] **QA-3b v3 (queda, menor):** limpiar los 3 sucios finales — telegram_channel (59, el grande, gradual),
        conversation (7), cache (1, invalid-return-type). No urgente.
- [ ] **#2 Dependabot (checkout 4→7)** — bloqueado por branch-protection strict (rama desactualizada tras
  mis pushes); Dependabot lo rebasa solo, se completa cuando su CI termine. Bajo riesgo, sin acción.

**🔍 barrido de HERMANOS (2026-07-03):** render 2× "can't start new thread" → CAUSA hallada (sin límites) →
RENDER-1 ✅ + SEC-4b render ✅. postgres: 5 "errores" = mis queries de diagnóstico (NO bugs). agent/worker/
valkey/sandbox: 0 errores. 9 hermanos estables.

---

## 🟢 FUTURO (post-pulido / hitos siguientes)

- ✅ **Borrado lo artesanal** (`github_tool.py` + `pr_review.py`, 2026-06-18):
      eliminados (nadie en producción los usaba — verificado; el bot corre 100%
      por MCP). Recuperables vía git si hiciera falta. ⚠️ OJO: esto NO declara
      cerrada la fase MVP — seguimos en pulido (decisión Brian 2026-06-18).
- [x] **Write tools de GitHub (subconjunto SEGURO con confirmación)** ✅ CERRADO
      2026-06-18 — For3s pasa de read-only a poder ESCRIBIR, pero SOLO 4 write
      reversibles y SIEMPRE con confirmación por botón: `add_issue_comment`,
      `create_issue`, `create_pull_request`, `create_pull_request_review`.
      Arquitectura de seguridad (decisiones Brian, fieles a R4.2.1):
      • El cliente MCP de lectura sigue read-only SIEMPRE. La escritura usa un
        contenedor MCP write-capable EFÍMERO (mcp_client.ejecutar_write) que se
        levanta solo para la write ya confirmada y se cierra → mínima superficie.
      • GATE DE INTENCIÓN (tool_loop.py): el agente PROPONE la write (schemas
        inyectados), pero el loop NO la ejecuta — la captura como accion_pendiente.
      • WHITELIST DURA (WRITE_TOOLS_PERMITIDAS): cualquier otra write/destructive
        (merge, delete_repository, push_files…) → RECHAZO duro, nunca se ejecuta.
      • Confirmación por InlineKeyboard en Telegram (✅/❌) con preview de qué hará
        + expiración 5 min + solo el dueño confirma. Audit inmutable github_write.
      Verificado E2E: el agente propuso add_issue_comment con args correctos,
      tool_calls ejecutadas=[] (NO escribió), texto "confirma abajo". 5 tests de
      seguridad. NADA destructivo (sin merge/delete/create repo/push). PAT ghp_ ya
      tenía scope repo+workflow (no se tocó). Las 5 write restantes + 4 destructive
      siguen DIFERIDAS (necesitan el workflow de approval policies completo de R4.2.1).
- [x] **Cache Valkey de lecturas de GitHub** ✅ CERRADO 2026-06-18 — de las 3
      features de R4.2.1 que estaban juntas, esta era la única lista y útil ahora
      (Valkey ya corría). `cache.py`: capa async sobre Valkey, TTL por tool fiel a
      R4.2.1 (get_file_contents 300s, list_* 30s, search_code 900s…), NEVER_CACHE
      + write tools nunca cachean, key con workspace_id (multi-tenant futuro).
      DEFENSIVA: si Valkey falla, degrada a sin-cache (el bot nunca se cae).
      Integrado en tool_loop (solo READ; las write siguen en su camino de
      confirmación). Verificado E2E: 1ª lectura MISS→GitHub (0.56s), 2ª lectura
      HIT desde Valkey (0.000s), contenido idéntico. 7 tests. Cliente redis 8.0.
- [ ] **Webhooks GitHub async + multi-tenant** — SIGUEN DIFERIDOS (H futuros, como
      R4 los escalonó). Análisis 2026-06-18 confirmó BLOQUEADORES reales:
      • **Ingreso de red:** GitHub no puede mandar webhooks al server (red
        doméstica que parpadea, IP inestable). Falta desplegar Cloudflare Tunnel
        (está en diseño R10, NO desplegado). Solo hay Tailscale (plano admin).
      • **Hueco de diseño:** R4.2.1 define el TRANSPORTE del webhook (recibir/
        validar HMAC/encolar con Arq) pero NUNCA qué HACE el bot con el evento
        (¿auto-review PR? ¿notificar? ¿comentar?). Hay que DISEÑAR eso primero.
      • **Multi-tenant** es el cimiento de ambas (webhook usa /{workspace_id},
        cache key usa workspace_id) y es un refactor grande: hoy todo cableado a
        owner_session="brian"; el esquema de secrets/audit ya está namespaced por
        workspace (cripto por workspace ✅) pero sessions/episodes_events NO, y
        OwnerStore es single-owner. Solo vale la pena con un 2º cliente real.
      Orden recomendado cuando se retome: (1) definir qué procesan los webhooks,
      (2) multi-tenant real, (3) Cloudflare Tunnel, (4) webhooks.
- [x] **Conteos GitHub muy grandes** ✅ CERRADO 2026-06-18 — diagnóstico: el agente
      contaba PAGINANDO con list_* (30-100/página) → un repo con 4000 PRs necesitaba
      ~140 vueltas pero el loop corta a MAX_TOOL_ROUNDS=5 → parcial. Fix correcto
      (NO subir las vueltas, que dispara rate-limit): dar la HERRAMIENTA adecuada.
      Se añadieron `search_issues` + `search_pull_requests` a MVP_TOOLS (tool_loop.py):
      devuelven `total_count` EXACTO en 1 sola llamada (query 'repo:o/n is:closed'
      + perPage=1). Guía en TOOL_DIRECTIVE para usar search SOLO para contar (no
      para listar). Peso schemas +31%, mitigado por prompt caching. Verificado E2E:
      el agente eligió search_pull_requests y respondió 4206 PRs cerrados de cli/cli
      (número exacto real). 3 tests nuevos. MAX_TOOL_ROUNDS sigue en 5.
- [ ] **Mini-agente HTTP en el server for3s para control de contenedores (demo del sitio).**
      La demo del sitio público (marca-personal) tiene un toggle "encender/apagar agente"
      por usuario 1:1 (Jazz/Mashe/Brian) que debe hacer `docker start/stop` de su
      contenedor `for3s-demo-<kind>` en el server. PROBLEMA: la web corre en Vercel,
      que NO está en la red Tailscale del server → no puede ejecutar `docker` directo.
      Hoy el toggle solo guarda el estado en BD (`demo_users.agent_on`) y despacha la
      orden SI existe un controlador HTTP; sin él es NO-OP (la UI funciona, pero el
      contenedor real no se toca → `dispatched: false`).
      **Falta construir:** un mini-servicio HTTP en el server for3s que reciba
      `{name, action: start|stop}` (autenticado con token) y ejecute el docker localmente.
      Luego setear en Vercel `DEMO_AGENT_CONTROL_URL` + `DEMO_AGENT_CONTROL_TOKEN`.
      El puente del lado web ya está listo: `marca-personal/lib/demo/container.ts`.
      (Trabajo de Fase 2 de la demo. Anotado aquí porque toca infra del server/agente.)

### Límites/capacidades conocidos a retomar más adelante (Brian 2026-06-18)
> NO son fallos — son cosas que el bot HOY no hace y que retomaremos cuando toque.

**Grupo A — límites del WEB FETCH (mejorables con ingeniería):**
- [x] **Redirects / links cortos** ✅ CERRADO 2026-06-18 — diagnóstico: httpx YA
      seguía los redirects (a.co/bit.ly/amzn.to → destino). El problema real era
      doble y se separó: (1) no se EXPONÍA la URL final → ahora `fetch_url`
      captura `resp.url` y antepone `ENLACE FINAL: …` al contenido (transparencia:
      For3s dice a dónde llevaba el link corto); (2) el destino suele BLOQUEAR bots
      (Amazon, Cloudflare) → nuevo `_huele_a_antibot` da aviso HONESTO incluyendo
      la URL final ("ese link lleva a X pero bloquea accesos automáticos"), igual
      criterio que login: NO peleamos el anti-bot. 5 tests nuevos. Verificado en
      vivo (Amazon→aviso+URL, httpbin redirect→muestra ENLACE FINAL).
- [x] **Renderizar JavaScript** ✅ CERRADO 2026-06-18 — `web_fetch.py` ahora es
      híbrido: httpx primero (rápido, páginas con HTML servidor); si el contenido
      viene pobre (< 350 chars = SPA cáscara), cae al contenedor Docker
      **`for3s-render`** (imagen oficial Playwright + Chromium headless) que ejecuta
      el JS y devuelve el texto YA pintado. Verificado: react.dev renderiza vía el
      contenedor (2.6s). El contenedor sortea que el host es Ubuntu 26.04 (Playwright
      aún no tiene build nativo para esa versión). Dockerfile+render.py en
      `~/for3s-os/docker/render/`. 4 tests nuevos en `test_pulido_mvp.py`.
- [x] **Páginas con login / anti-bot** ✅ CERRADO 2026-06-18 (con criterio honesto) —
      decisión de Brian: NO pelear contra muros de sesión/anti-bot. Si la página
      exige login, For3s lo **dice honestamente** ("requiere iniciar sesión, no
      puedo entrar; pégame el texto o un enlace público") en vez de fingir que la
      leyó. Detección por señales (`_huele_a_login`). Login real con credenciales
      queda fuera de scope (futuro, si alguna vez se justifica).

**Grupo B — capacidades NUEVAS (features de hitos futuros):**
- [x] **Multimodal: imágenes + PDF + Word + Excel** ✅ CERRADO 2026-06-18 — For3s
      ya LEE adjuntos (antes solo texto). `multimodal.py`: imágenes (jpg/png/gif/
      webp) y PDF van NATIVOS a Claude (visión/lectura, base64) — PDF usa el beta
      `pdfs-2024-09-25`; Word (.docx, python-docx) y Excel (.xlsx, openpyxl) se
      extraen a texto. Handlers `on_adjunto` en Telegram (PHOTO + Document.ALL).
      `llm.complete()` y `Conversation.send()` aceptan `adjuntos`. 9 tests nuevos.
      Verificado E2E contra la API real con OAuth+sonnet-4-6: imagen→"Rojo",
      PDF→leyó el texto interno. El base64 NO se guarda en memoria (solo una nota).
- ⏸️ **Multimodal: AUDIO** (notas de voz / mp3) — DESCARTADO POR AHORA (decisión
      Brian 2026-06-18): Whisper local pesa ~1-2GB de modelo + CPU para algo que
      "no van a ocupar demasiado" → no justifica los recursos. Si en el futuro se
      vuelve necesario, la vía sería faster-whisper local (sin costo por uso, sin
      mandar el audio a terceros). No es un pendiente abierto, es una decisión.
- [ ] **Sistema tipo Notion / notas estructuradas** — hoy solo hay historial
      conversacional en Postgres, no un sistema de notas/conocimiento navegable.
      (Relacionado con H-C sistema de pensamiento.)
- [ ] **⚡ CACHE 1h para los 5 agentes For3s (Brian 2026-07-07)** — mejora REAL derivada de la
      investigación del cache de Anthropic. En los agentes For3s SÍ controlamos `llm.py`, así que
      aplicar `cache_control {"ttl":"1h"}` al system prompt (identidad+memoria, la parte estable y
      grande) → cuando un agente está idle < 1h su prefijo se mantiene caliente 12× más → **menos
      reenvíos = menos consumo de la suscripción COMPARTIDA** (1 cupo para los 5). Verificar primero
      que el provider ya usa cache breakpoints; medir cache_read_input_tokens antes/después. Aditivo,
      riesgo bajo. Detalle: `memory/archive/Investigacion_Cache_Anthropic_ClaudeCode.md` §4-A.
- [ ] **⚡ RE-EVALUAR cache/keep-alive de Claude Code (Brian 2026-07-07, revisión periódica)** — la
      idea de Brian (un "cron sombra" que refresque el cache de Anthropic cada 5 min para no reenviar
      la conversación al retomar) es CONCEPTUALMENTE correcta (cada cache-read resetea el TTL de 5min)
      pero HOY NO es construible: Claude Code no expone ningún setting de cache/TTL/keep-alive ni
      ningún hook por timer/idle (verificado en las 3 fuentes oficiales), y un cron externo no puede
      acceder al prefijo exacto de la sesión. **Re-checar cuando Claude Code evolucione** si aparece
      un setting de TTL, hook de timer, o API para refrescar el cache de la sesión → ahí la idea se
      vuelve construible. Mientras: `/clear` estratégico entre bloques (ya LOCKED). ⛔ NO reintentar
      el cron externo (imposible por diseño; razón en el doc). Detalle:
      `memory/archive/Investigacion_Cache_Anthropic_ClaudeCode.md`.
- [ ] **🎭 IDENTIDADES SECUNDARIAS de OpenClaw → rasgos a la personalidad de brian (Brian 2026-07-05)** —
      ⛔ REGLA LOCKED: la personalidad de @For3s_Brian_bot NO se altera por ahora (queda el alma
      Fruterito DevRel/dev tal como se aprobó en E2). Las identidades del 🍊 Empleado (Product
      Lead→CEO) y 🔥 For3s Design ("orchestrator of human connection through pixels") están DENTRO
      como MEMORIA (consultables), NO como personalidad. Este pendiente = evaluar A FUTURO (fuera
      del hito ENTRENAMIENTO, cuando Brian diga) si algunos rasgos ejecutivos/de diseño se fusionan
      a persona/ — siempre con borrador + gate de Brian, como E2. Refs: radiografías Empleado y
      Design_Cipher_Helix.
- [ ] **⭐ CRON CONVERSACIONAL / recordatorios en lenguaje natural (Brian 2026-07-03; reafirmado 2026-07-04)** —
      que el usuario diga "recuérdame cada lunes", "revisa el repo X cada mañana" y For3s programe la tarea
      SOLO. HOY For3s tiene jobs FIJOS (los 11 nocturnos: backup/cls/microglia/perfil/estilo…) pero NO cron
      conversacional (el usuario no puede crear tareas programadas hablando). **Es una de las 2 brechas para
      paridad de AGENTE completo con Hermes** (que sí tiene "automatizaciones programadas con cron scheduler
      en lenguaje natural"). NO es una capacidad de agencia que falte (For3s ya es agente autónomo) — es una
      FORMA de expresar tareas. Relacionado con H-G subagente async + los jobs existentes (tasks.py/Arq).
      Detalle del análisis bot→agente: `memory/archive/For3s_Bot_vs_Agente_vs_Hermes.md`.
      **⭐ MODELO DE REFERENCIA (hallazgo radiografía 2026-07-04):** OpenClaw SÍ lo tenía — en
      `~/entrenamiento/Fruterito-principal/cron/jobs.json` hay un job REAL creado dinámicamente
      (`godinez-studio-tickets-monitor`): agente `dev` · cada 30 min · payload = instrucción en LENGUAJE
      NATURAL ("revisa tickets de fruteroclub/godinez-studio, compara con el estado guardado, avisa a Brian
      SOLO si hay cambios, actualiza el estado") · `sessionTarget: isolated` (no contamina la conversación) ·
      `wakeMode` + `enabled` + estado propio (`nextRunAtMs`) + `cron/runs/*.jsonl` (log por corrida). Diseño
      a copiar cuando se construya el nuestro: tabla `cron_jobs` en BD (no archivo) + payload en lenguaje
      natural que corre por el tool-loop en sesión aislada + registro tipo `cron_corridas` (ya existe, PR2) +
      gate del governor + comandos /recordar-cada o detección conversacional. Ver
      `docs/analysis/Radiografia_Fruterito_Principal.md` §5. ⚠️ Construir JUNTO con OC-E2 (sesiones aisladas
      desechables, §BRECHAS OPENCLAW) — son la misma pieza.
- [ ] **⭐ MULTI-CANAL (Brian 2026-07-03)** — hoy For3s solo vive en Telegram + consola. Hermes está en
      Telegram/Discord/Slack/WhatsApp/Signal/CLI. **Es la OTRA brecha para paridad de agente completo.**
      No afecta la agencia (For3s ya actúa/aprende/es autónomo), solo la OMNIPRESENCIA. Diseñar una capa
      de canal genérica (el core ya está desacoplado del canal). Cruza con distribución/producto.
      ⚠️ = OC-C1 (§BRECHAS OPENCLAW): Discord PRIMERO, con la config real de OpenClaw como referencia.
- [ ] **Escribir/crear/editar en GitHub** — ✅ create_issue/PR/comment funcionan (fix 2026-07-03: el MCP
      renombró tools, traducido en mcp_client). Ampliar a más write tools = futuro.

---

## ⚠️ AL PROGRAMAR HITOS FUTUROS (recordatorios de diseño)

- [ ] **R6 al programar:** ejecutar plan E + medir PFC_PLANNING_COST real + cargar
      HARD NO-GO §8.4 + governor ANTES de auto-generación de skills.
- [ ] **DMN 5.4.2 al programar:** implementar 8 action_fn + auto-improvement loop
      enchufado al governor.
- [ ] **2 reglas de oro:** (1) CI/CD temprano (Fase 0, no al final);
      (2) Meta-Orchestrator/governor DEBE existir ANTES de activar auto-gen (R6).
- [ ] ⭐ **PARIDAD HERMES al programar cada hito:** llevar las 5 capacidades P1-P5
      (ver sección "⭐ PARIDAD CON HERMES") al MISMO nivel de detalle que Hermes,
      en su hito ancla: **H3-H4** → P4 (MCP arbitrarios) · **H4** → P3 (ejecución de
      código) · **H5** → P1 (modelar al usuario, REQUIERE diseño previo) · **H8** →
      P2 (sub-agentes paralelo) · **H10-H12** → P5 (skills auto-generables). Directriz
      de Brian: son prioritarias, no opcionales.

---

## ✅ CERRADOS (rastro — no borrar)

- ✅ Endurecimiento H4 (2026-06-14): identidad honesta, issues, Bug E (canal),
  Bug H (token fuera de logs + cifrado), warning shutdown (doc), Bug F (refs cortas),
  Bug G (cupo), identidad segundo cerebro.
- ✅ Migración GitHub → MCP (2026-06-14): 7 pasos, en producción.
- ✅ Pulido: "escribiendo..." persistente, Fallo 1 (usar tool no anunciarla),
  Fallo 2 (conteos que paginan).
- ✅ H-A (no abortar tareas largas + aviso + multi-mensaje básico).
- ✅ H-F (forzar ejecución de tools, ya NO inventa) + normalización de texto
  (mayús/acentos) + limpiar_urls.
- ✅ Identidad honestidad de fraseo + aviso de error garantizado.
- ✅ Comandos admin Telegram: /estado /diagnostico /reiniciar /reiniciar_duro.
- ✅ Sistema anti-rate-limit A+B+C (espaciar + caching + cola serial).

### Sesiones 2026-06-15 a 18 — pulido profundo del análisis de GitHub + robustez

- ✅ **Identidad REAL** (2026-06-16/17): For3s sabe qué es For3s (Brian López,
  Frutero, 10 rondas, MVP, Mente OS) + aclaración del Hermes de Frutero (NO el de
  Nous Research) → ficha curada en FOR3S_ROLE. Verificado en vivo. (Causa raíz: el
  bot era amnésico de sí mismo y confundía al competidor.)
- ✅ **Control por USO, no por tiempo** (Anexo R3): repo enorme → sub-bloques,
  fila/lotes, presupuesto de tiempo, mensaje editable. Arreglado el cuelgue de
  acquire() (50min→25s).
- ✅ **Ficha de repo** (gh_ficha): About + lenguajes % + deployments + contributors
  vía REST con el PAT. Datos = los de la web de GitHub. Verificado.
- ✅ **Detección de ORGANIZACIONES** (github.com/NOMBRE sin /repo): lista repos y
  pregunta cuál (antes Claude alucinaba un repo y colgaba). Verificado.
- ✅ **Lectura por CATEGORÍAS** README→config→doc→src→test→otro, src completo (ya no
  cortaba el código por un cap arbitrario), orden por RECENCIA de commits.
- ✅ **DOS MODOS de análisis** (2026-06-17): SIMPLE (capas de ejecución
  afuera→adentro, pocos archivos clave, contexto para NO programadores + vulns, sin
  números) y PROFUNDO (capas+recencia, todo el código, con cobertura). Detección por
  palabras clave. Verificados en vivo.
- ✅ **Web fetch** de URLs públicas NO-GitHub (Luma, blogs, Amazon): For3s las LEE y
  responde (antes era cuadrado: "ábrela tú"). Verificado.
- ✅ **Web fetch HÍBRIDO con render de JS** (2026-06-18): httpx primero (rápido); si
  la página es una SPA cáscara (<350 chars), cae al contenedor Docker `for3s-render`
  (Playwright + Chromium headless) que ejecuta el JS y devuelve el texto pintado.
  Login → aviso honesto (no pelea anti-bot). Verificado (react.dev rinde, 2.6s).
- ✅ **MULTIMODAL: imágenes + PDF + Word + Excel** (2026-06-18): For3s lee adjuntos.
  Imágenes y PDF nativos a Claude (visión/lectura, beta `pdfs`); Word/Excel se
  extraen a texto (python-docx/openpyxl). `multimodal.py` + `on_adjunto` (Telegram
  PHOTO+Document) + `complete()/send()` con `adjuntos`. Verificado E2E con la API
  real (imagen→color, PDF→texto interno). Audio descartado por recursos.
- ✅ **Web fetch: redirects + anti-bot honesto** (2026-06-18): expone `ENLACE FINAL`
  tras seguir links cortos (a.co/bit.ly/amzn.to) y avisa honesto cuando el destino
  bloquea bots (Amazon/Cloudflare) diciendo a dónde llevaba el link. NO pelea el
  anti-bot (mismo criterio que login). 5 tests. Verificado en vivo.
- ✅ **Conteos GitHub exactos** (2026-06-18): search_issues + search_pull_requests
  en MVP_TOOLS → total_count exacto en 1 llamada (antes paginaba con list_* y se
  agotaba el loop). Verificado E2E: 4206 PRs cerrados de cli/cli. NO se subió
  MAX_TOOL_ROUNDS (eso dispara rate-limit; el fix es la herramienta correcta).
- ✅ **Write tools seguras con confirmación** (2026-06-18): comentar + crear
  issue/PR/review, todo reversible y con botón ✅/❌ (InlineKeyboard). Gate de
  intención (propone, no ejecuta) + whitelist dura (rechaza merge/delete/push) +
  contenedor MCP write-capable efímero + audit github_write. Cliente de lectura
  sigue read-only. Verificado E2E (propone sin ejecutar). 5 tests de seguridad.
- ✅ **Cache Valkey de lecturas GitHub** (2026-06-18): cache.py async sobre Valkey
  (ya corría), TTL por tool, write/never-cache excluidas, key con workspace_id,
  degrada si Valkey falla. Verificado E2E: 2ª lectura HIT 0.000s sin tocar GitHub.
  7 tests. (Webhooks + multi-tenant siguen diferidos: bloqueadores de red/diseño.)
- ✅ **Markdown → HTML de Telegram**: código en bloques `<pre>` reales, no crudo.
  Fix de 3 bugs (split del HTML, <pre> literal de Claude, límite 4096).
- ✅ **Error handler de red + reintentos** (2026-06-17): el servidor está en red
  doméstica (parpadea); el bot ya NO muere ni ensucia logs con NetworkError/TimedOut.
  Typing robusto + _responder_seguro 5 intentos backoff + _enviar_html reintenta por
  chunk distinguiendo red vs HTML malo. (La red de casa en sí no se arregla por código.)
- ✅ **"CONTINÚA" real** (2026-06-17): si un mapeo se corta por tiempo, guarda los
  archivos faltantes (sessions.meta) y al decir "continúa con lo faltante" RELEE de
  verdad lo que faltó, con marcador (antes improvisaba sin leer). Parche manual de H-G.
- ✅ **Guardado en orden** del mapeo (gh_resources fiel al orden de lectura, no
  desordenado por los lotes paralelos).
- ✅ **Hora LOCAL del usuario** (2026-06-18, módulo tiempo.py): el servidor corre en
  UTC pero el bot ahora usa la hora del USUARIO (deducida del language_code, default
  CDMX) inyectada al prompt. Verificado: UTC 03:42 → CDMX 21:42. Extensible a /zona
  por usuario para multi-tenant.
- ✅ **"Continúa" visual unificado** (2026-06-18, VERIFICADO EN VIVO): la continuación
  se veía mal (mensajes nuevos + lista de archivos). Ahora usa el MISMO render por
  categorías que el inicio (helper compartido `crear_progreso_categorias`): 1 mensaje
  editable, bolas 🟢🟡⚪ por categoría, encabezado "🔄 Continuando", sin lista de
  archivos. + bug del denominador arreglado (las bolas sí llegan a verde).

## ⭐ PARIDAD CON HERMES — 5 capacidades PRIORITARIAS (Brian 2026-06-18)

> **Directriz de Brian:** estas 5 capacidades (que Hermes de Nous `NousResearch/
> hermes-agent` SÍ tiene y For3s OS NO) son de SUMA IMPORTANCIA — For3s debe
> tenerlas al MISMO nivel de detalle que Hermes. Surgieron de la tabla comparativa
> "qué tiene Hermes y For3s no". **Hallazgo clave del análisis:** 4 de las 5 YA
> están DISEÑADAS en las rondas (solo acotadas en v1) — NO son features nuevas
> sueltas, son puntos del plan que hay que IMPLEMENTAR/AMPLIAR al detalle de Hermes.
> Solo 1 ("modelar al usuario") es un gap de diseño real. Cada una anclada abajo a
> su hito/ronda del plan de desarrollo (Mapa_Construccion_Incremental + las R).

- [x] ✅ **P1 · MODELAR AL USUARIO — COMPLETO 2026-07-02 (v1 24-jun + v2 inferencia nocturna 02-jul).**
  🎉 **La ÚNICA de las 5 que era gap de diseño real → CERRADA.** Con las 5 paridades Hermes: P1 ✅
  (perfil declarado + inferido con gate), P2 ✅ (equipo H8), P3 ✅ (execute_code), P4 ✅ (MCP), P5 ✅
  (skills). v2 detalle arriba ⬆️.
  DECIDIDO (v1): HÍBRIDO (persona dice + bot infiere/confirma) · perfil FLEXIBLE (campos clave
  rol/stack/estilo/zona + rasgos libres JSONB) · por PERSONA global. Construido: migración 018
  (tabla `perfil_usuario`, PK telegram_user_id) + `perfil.py` (PerfilStore get/set_campo/add_rasgo/
  resumen + detectar_afirmacion: "soy X"→rol, "prefiero Y"→rasgo, filtra falsos positivos como
  "soy claro/honesto") + conversation.py: INYECCIÓN del perfil al contexto en cada turno con autor
  (2g) + CAPTURA explícita al guardar turno del user + comando `/perfil` (ver/editar: `/perfil rol
  backend`) en _MENU_BASICO. El bot adapta sus respuestas a quién es cada persona. VERIFICADO: store
  6/6, detector OK, E2E captura+inyección. 132 tests, BD v18, bot activo.
  ⏳ 2ª PASADA pendiente: INFERENCIA NOCTURNA (que el bot proponga rasgos solo, de noche con H6/CLS).
  (texto original del pendiente abajo ⬇️)
- [x] ✅ **P1 v2 · INFERENCIA NOCTURNA DEL PERFIL — HECHO 2026-07-02 (completa la paridad Hermes
  "dialectic user modeling").** Ahora el bot no solo aprende cuando dices "soy X": de noche OBSERVA
  cómo interactúa cada persona e INFIERE rasgos candidatos (rol/stack/estilo/zona/rasgo libre). NUNCA
  los aplica solo → los deja como PROPUESTA con gate ✅/❌ (reusa dmn_propuestas). Al APROBAR, se aplican
  al perfil (resolver_propuesta extendido); al descartar, no. Módulo `perfil_infer.py` (inferir_persona
  + parseo JSON robusto + no re-proponer lo conocido + aplicar_propuesta_perfil) + `job_perfil` nocturno
  (03:45 Mx, tras curar-skills) OPT-IN (`FOR3S_PERFIL_INFER=on`, off por defecto como las generativas
  del DMN) + OAuth-safe (system=''). 🐛 el test cazó un bug de FK (perfil_usuario→personas): aplicar
  ahora ASEGURA la persona antes de escribir. Verificado E2E (parseo→propuesta→aprobar aplica→descartar
  no aplica→no re-propone) + análisis de comportamiento (9 hermanos sanos, opt-in respetado, audit 0
  rotos). Decisión Brian: propone+gate (no auto-aplica), off por defecto. **P1 Hermes COMPLETO.**

- [x] ✅ **P2 · SUB-AGENTES EN PARALELO — HECHO (H8 EQUIPO).** multiagente.py + specialists.py
      (5 specialists en paralelo + Synthesizer), verificado en vivo. (texto original de diseño abajo)
      ✅ **YA DISEÑADA y LOCKED** — Nodo Multi-Agent Network, **R5 Bloque 3** →
      **Hito H8 ("EQUIPO")**. Diseño: hub-and-spoke, spawn N specialists en paralelo
      (cap 5 v1), message bus, 18 capas defense-in-depth, `asyncio.create_task`.
      ⚠️ Matiz v1: 5 specialists FIJOS (code_analyzer, security_auditor,
      test_generator, performance_analyzer, doc_writer). Sub-agentes DINÁMICOS
      (arbitrarios, como Hermes con delegate_task+Kanban) = capacidad generativa #3,
      DIFERIDA a v3 (Grafo §8.1, gobernada por Meta-Orchestrator). Relacionado con
      [[H-G]] subagente async. Punto: **H8** (v1 fija) → dinámicos tras H12.

- [ ] **P3 · EJECUTAR CÓDIGO REAL** (terminal/código en entornos aislados, no solo
      lint — Hermes corre en 6 entornos: local/Docker/SSH/Modal/Daytona…).
      ⚠️ **PARCIAL** — hay base pero NO ejecución arbitraria: sandbox de SKILLS
      (ejecuta planes generados, no código libre, R6 B2 §6.2.5 → H12) + Docker
      multi-tenant 3 capas para aislar workspaces (R4 B1 → H4/H8). Falta: un MCP de
      ejecución/terminal arbitrario. El aislamiento Docker de H4/H8 es la BASE sobre
      la que montarlo. → Punto: extender MCP servers core cerca de **H4** + hardening
      H8. (Requiere pieza nueva, pero sobre cimiento ya diseñado.)

- [~] ✅ **P4 · CONECTAR CUALQUIER MCP — FASE 1 HECHA 2026-06-24 (Bloque 4).** DECIDIDO:
  refactor a MCP genérico + config, GitHub como único server (cero riesgo). Construido en
  mcp_client.py: `MCPServerConfig` (nombre/command/args/env) + `MCPClient` GENÉRICO
  (start/aclose/tools_for_anthropic/call_tool para CUALQUIER server stdio) + `config_github()` +
  `GitHubMCPClient` ahora SUBCLASE de MCPClient (misma firma __init__(pat,read_only=), compat total).
  VERIFICADO: GitHubMCPClient es MCPClient, interfaz intacta, GitHub conecta read-only idéntico tras
  reinicio, y se puede crear un MCP arbitrario desde config (probado fs/npx). 132 tests, bot activo.
  ⏳ FASE 2 (cuando haya 2º MCP real): solo agregar su MCPServerConfig + registro de tools dinámico
  (hoy MVP_TOOLS fijo de GitHub) + disparo (hoy huele_a_github). El framework ya lo soporta.
  (texto original abajo ⬇️)
- [~] **P4 · CONECTAR CUALQUIER MCP (texto original — fase 1 ✅ hecha arriba, falta ampliar).**
  (no solo GitHub — Hermes enchufa cualquier
      servidor MCP + OAuth).
      ✅ **YA DISEÑADA — framework extensible LOCKED** — Nodo Tools/MCP Layer,
      **R4 Bloque 1** (framework + discovery) y **B2** (servers core) → **Hitos H3**
      (MCP SDK + Discovery) y **H4** (primeros servers). "MCP es un protocolo, no una
      library" (R4 B1 §4.1.1); discovery híbrido con 5 triggers de hot-reload sin
      downtime. Añadir un server = editar `config/mcp_servers.yaml` → hot-reload.
      ⚠️ v1 = 4 core (GitHub/Telegram/FS/HTTP); más servers (Slack/Notion/Google) =
      R4 Bloque 4 Multi-Domain, DIFERIDO a v2 pero SIN refactor (el framework ya los
      soporta). Punto: base en **H3**, primeros en **H4**, MCP arbitrarios = activar v2.

- [x] ✅ **P5 · PLUGINS / SKILLS EXTENSIBLES — HECHO (H10-H12 APRENDE).** skills.py + governor.py +
  aprende.py (crea/gobierna/cura skills), verificado en vivo. (texto original de análisis abajo)
  ⭐ ANÁLISIS HECHO 2026-06-24 del learning
  loop de Hermes (Nous) → `docs/analysis/Analisis_LearningLoop_Hermes_para_For3s.md`. HALLAZGO: For3s ya
  tiene ~60% del PATRÓN (curator≈CLS/Microglía H6, background_review≈fork aislado H8, provenance≈
  ContextVar H8 S9). Faltan: motor /learn (prompt que instruye al agente a destilar skill con sus
  tools) + skill_manage (crear/editar SKILL.md) + governor R6 construido. RUTA (orden LOCKED freno-
  antes-que-motor): H10 skills básicas+skill_manage → H11 GOVERNOR (scanner seguridad estilo
  skills_guard + lifecycle + provenance) → H12 motor auto-gen (/learn + auto-mejora reusando H6+H8).
  Grande pero no de cero; NO urgente (tras pulir + Bloque 3). Brian preguntó "¿podemos hacer como
  intern-os?" → SÍ, análisis listo, adaptación = H10-12 cuando toque.
  ✅ **FASE B (PLAN MAESTRO) HECHA 2026-06-24 → `memory/archive/H10-H12_Plan_Maestro_APRENDE.md`.** Decisiones
  LOCKED: skill=SKILL.md+scripts (receta, NO código auto-ejecutado) · /aprende manual + auto-mejora
  background · governor = Meta-Orchestrator R6 COMPLETO (6 frenos+kill switch) · lifecycle = curación
  nocturna reusando H6. Orden LOCKED H10(skill_manage+uso)→H11(GOVERNOR, freno antes que motor)→
  H12(/aprende + auto-mejora). Reusa ~60% infra (H6+H8+ContextVar+gate+audit). Listo para construir
  cuando toque.
  (texto original abajo ⬇️)
- [x] ✅ **P5 · PLUGINS / SKILLS EXTENSIBLES — HECHO (H10-12, texto original abajo).**
  (añadir habilidades nuevas — Hermes se
      AUTO-crea skills tras tareas y las mejora; "learning loop").
      ✅ **YA DISEÑADA y LOCKED** — es el corazón del Pilar 3 (Autonomía Generativa).
      Nodo **4 Ganglios Basales (Skills)**, **R6 B2** (skills+storage+lifecycle) +
      **R6 B1** (PFC, promoción 7 fases) + **R6 Pre-Code §A** (Meta-Orchestrator
      governor) → **Hitos H10→H11→H12** (orden sagrado: el FRENO H11 antes del
      MOTOR H12). For3s ESCRIBE sus propias skills (capacidad #1), lifecycle 7 fases
      gobernado, 3 tiers (workspace/core/common_stack) + 6 frenos + kill switch.
      ⚠️ NO hay marketplace externo de terceros en v1 (el "compartir" es
      common_stack interno con opt-in). Punto: **H12 ("APRENDE")**, con H10+H11 como
      prerequisitos OBLIGATORIOS. ⚠️ Recordatorio LOCKED: governor ANTES de auto-gen.

> **Resumen de anclaje al plan:** P4→H3-H4 · P3→H4(+H8) · P2→H8 · P1→H5(o H13) ·
> P5→H10-H11-H12. Es decir: ya están repartidas en el camino de construcción
> existente (no rompen el orden foundation-first). La única que necesita DISEÑO
> previo es P1 (modelar al usuario). Detalle de la comparación: tabla "qué tiene
> Hermes y For3s no" + `Comparacion_Funcional_For3s_OS_vs_Hermes.md`.

---

## 🟢 HALLAZGOS DE FONDO PENDIENTES (necesitan diseño tipo Ronda)

- [x] ✅ **G6-repos-no-se-enlistan CERRADO 2026-06-24.** Destapado en prueba real: el bot tenía
      16 repos en `gh_resources` pero al pedir "enlístame los repos" recordaba solo 2 (los de su
      memoria semántica/grafo). FIX (misma técnica que AI1/AI5): `memory.repos_analizados(session_id)`
      consulta gh_resources (repos distintos por hilo, por recencia, defensivo) + `conversation.
      _es_pregunta_repos` (detector: menciona repo/repositorio + intención listar/recordar; NO
      dispara en "analiza este repo X" ni charla) + inyección de la lista REAL al contexto en
      send() (como grafo/versión/STATUS). VERIFICADO: detector 6/6 casos, lista trae los 16 repos
      reales (cli/cli, donutbrowser, godinez-ai, aider, orb-hardware, evvm, etc.). 132 tests, bot
      activo. Hueco preexistente de H5, NO de AI1-AI7.

- [ ] **H8-aislamiento-multitenant** (Brian 2026-06-23) **Activar las 2 capas de aislamiento de
      H8 que quedaron PREPARADAS pero inactivas (dependen de multi-tenant).** En H8 S9 se
      construyeron las capas de aislamiento que aplican a single-user (whitelist enforcement,
      mutation guard read-only, KEK scoping, ContextVar — todas ACTIVAS). Estas 2 quedaron
      preparadas/documentadas pero NO activas porque protegen contra fuga ENTRE CLIENTES, que
      hoy no existen (single-user):
      1. **Postgres Row-Level Security (capa 4):** que un specialist solo vea las filas de SU
         workspace. Requiere el concepto de workspace (multi-tenant) en las tablas + políticas RLS
         en Postgres. Hoy todo es workspace "default".
      2. **Anomaly detection + emergency kill (capa 7 del grupo aislamiento):** si un specialist
         hace algo anómalo (accesos raros, patrón sospechoso), matarlo. Es para producción
         multi-tenant de alta carga / superficie de ataque real.
      **CUÁNDO retomar:** cuando se construya multi-tenant (varios clientes/empresas en un mismo
      For3s) — ahí estas 2 capas se vuelven necesarias de verdad. Revisar A DETALLE el diseño
      LOCKED R5 B3 §5.3.2 (grupo aislamiento, capas 4 y 7). Relacionado con el multi-usuario de
      H8 S10 (que es un primer paso hacia multi-tenant) y con Webhooks+multi-tenant (ya en lista).
      NO urge mientras For3s sea single-user / un solo equipo. Detalle de obra: Doc/H8_Plan_Maestro_EQUIPO.md §2.

- [x] ✅ **G4-version-self-awareness CERRADO 2026-06-23 (por AI5).** El agente ya SABE su
      versión/hito/cambios: `version.py` (fuente única + changelog H1→H8) + detector de pregunta
      + inyección al contexto + comando /version. Responde "¿qué versión eres? ¿qué hay nuevo?"
      con datos reales sin inventar. Mismo fix que P4. Detalle: sección "🧬 ADOPTAR de intern-os"
      AI5 arriba.

- [x] ✅ **G5-recuerdos-fragmentados CERRADO 2026-06-23 (por AI6).** Tiered por relevancia: el
      recuerdo muy relevante (dist<0.35) llega hasta 700 chars (casi completo, ya no se fragmenta
      lo importante); el lejano queda en 300 (no infla) + tope global del bloque 2500. Justo la
      opción (a)+(b) que se proponía. Detalle: sección AI6 arriba. (Texto original abajo ⬇️)
- [~] **G5-recuerdos-fragmentados** (Brian 2026-06-22, lo detectó el propio agente) — **Los
      recuerdos semánticos llegan CORTADOS** (se ven los `...`), el bot puede perder contexto.
      ⚠️ CAUSA CONOCIDA (no es misterio): es el tope `_MAX_CHARS_RECUERDO = 300` en
      conversation.py — se puso a propósito para no inflar el contexto inyectado. Es un trade-off
      ajustable: subir el tope da más contexto por recuerdo pero pesa más tokens (y con OAuth
      Tier 1 el límite es bajo). Opciones al retomar: (a) subir el tope con criterio (ej. 600-800);
      (b) recuperar el episodio COMPLETO solo cuando el recuerdo es muy relevante (dist baja);
      (c) traer el turno fuente entero on-demand si el bot lo necesita. Decidir balance
      contexto-vs-tokens. NO urge: hoy 300 chars suele bastar para el panorama.

- [x] ✅ **529-overloaded CERRADO** (2026-06-22) — El bot ya NO se queda mudo cuando Anthropic
      se satura. Diagnóstico confirmado en auditoría: el 529/503/502/500 son errores TRANSITORIOS
      del servidor de Anthropic (no del cliente ni del cupo); `_post` solo manejaba el 429 → los
      5xx reventaban en `raise_for_status()` y dejaban al bot mudo (hueco real 440-448).
      FIX (llm.py): nueva excepción `ServidorSobrecargado` + `_HTTP_TRANSITORIOS=(500,502,503,529)`
      → `_post` los reintenta con BACKOFF exponencial (2,4,8,16s, cap 60s) y, si persisten, lanza
      ServidorSobrecargado (mensaje amable, no traceback). telegram_channel.py: handler que muestra
      "🌩️ Anthropic está saturado... reintenta en un momentito" en vez del error feo. 2 tests
      nuevos en test_h1.py (reintenta+lanza / se recupera si responde). Suite: 130 tests. Verificado
      arranque limpio del bot.

- [ ] 🟡 **H6-backup-offsite — CÓDIGO LISTO, bloqueado por Tailscale SSH** (Brian 2026-06-22).
      El MECANISMO está construido y probado: `backup.py` tiene `copiar_offsite()` (rsync+SSH,
      DEFENSIVA: si el destino no responde, NO rompe el backup local) integrado en `backup_y_rotar`.
      Destino elegido: el WSL2 de Brian = `brayaneth` (100.88.66.23, usuario brianweb3) →
      `~/for3s-backups-offsite`. Clave SSH del server ya generada (`~/.ssh/id_ed25519`) y
      autorizada en el WSL2. Config por env `FOR3S_BACKUP_OFFSITE` (hoy COMENTADA en .env).
      ⚠️ **BLOQUEADOR REAL:** Tailscale SSH intercepta la conexión server→WSL2 y exige login
      por NAVEGADOR (mensaje "Tailscale SSH requires an additional check, visit login.tailscale
      .com/..."). Un job automático no puede completar ese login → el rsync se cuelga (falla
      defensivo, el backup local sí se hace). Verificado que el código falla limpio sin activar
      (132 tests, backup local intacto). DEJADO COMO PENDIENTE por Brian (2026-06-22).
      **⭐ PASO EXACTO PARA ACTIVAR (cuando se retome):**
      1. Tailscale panel → Access controls → JSON editor. En el bloque `"ssh"`, la regla actual
         tiene `"action": "check"` (eso es lo que cuelga). Cambiarla a `"action": "accept"`
         (con `"src":["autogroup:member"], "dst":["autogroup:self"], "users":["autogroup:nonroot"]`).
         Es seguro: dst=autogroup:self = solo entre las máquinas del MISMO dueño (Brian). Guardar.
      2. En el server: descomentar `FOR3S_BACKUP_OFFSITE=brianweb3@100.88.66.23:~/for3s-backups-offsite`
         en `~/for3s-os/.env` (hoy está comentada con #) + reiniciar `for3s-worker.service`.
      3. Verificar: disparar job_backup a mano → confirmar que el .sql llega a ~/for3s-backups-offsite
         del WSL2 (brayaneth). El destino, clave SSH del server y carpeta YA están listos.
      Alternativa si Tailscale complica: bucket nube (S3/Backblaze) o `tailscale up --ssh=false`
      en brayaneth para usar su sshd nativo. NO urge: backup local protege; activar antes de que
      la Microglía tenga candidatos reales (episodios >30d, en semanas).

- [x] ✅ **429-system-prompt CERRADO** (2026-06-22) — Investigado a fondo. HALLAZGO TRANQUILIZADOR:
      los flujos de GitHub (tool_loop desde conversation.py:481, subbloques.py:310 y :509) **YA
      estaban OAuth-safe** (bajo OAuth ponen `system=""` y el rol en el user message). Es decir:
      los 429 que se sufrían al analizar repos/PDFs grandes NO eran el falso-429 por system custom
      — eran **rate-limit REAL por volumen** (analizar un repo grande hace muchas llamadas → satura
      el límite de Sonnet Tier 1 30k/8k tok-min). Eso ya se maneja con backoff (429-real) y, si
      persiste, aviso amigable.
      LO QUE SÍ SE MEJORÓ (valor real): `llm.py _post()` ahora **distingue los DOS tipos de 429**
      por su firma: (a) 429-REAL (con retry-after) → log [429-RATE], reintenta con backoff; (b)
      429-FALSO (system custom rechazado: 'message:Error' sin retry-after) → log [429-SYSTEM],
      NO reintenta en vano (sería inútil), avisa de una. Así, si vuelve a pasar, el log dice cuál
      es. 2 tests nuevos (test_h1.py: falso no reintenta / real sí reintenta). Suite 132 tests.
      Regla permanente confirmada: con OAuth, instrucciones en user message + system="" (ya aplicada
      en todo el código). Relacionado: [[project_tooluse_oauth_ratelimit]].
      ⭐ **AUDITORÍA TOTAL + BLINDAJE (2026-06-22):** se revisaron los 10 sitios del código que
      llaman al LLM (agent.py ×2, consolidator, conversation ×3, subbloques ×2, tool_loop ×2).
      TODOS ya OAuth-safe (system="" bajo OAuth). PERO el patrón estaba repetido en 6 sitios →
      frágil ante un flujo futuro. BLINDAJE preventivo en `llm.py _build_system`: en OAuth, si
      llega un system NO vacío, NO lo concatena (eso disparaba el 429) → lo IGNORA + loguea
      [429-GUARD] con el flujo culpable. Última línea de defensa: degrada en vez de romper.
      Verificado en vivo: pasar system custom en OAuth → log de aviso + respuesta 200 OK (no 429).
      Test actualizado (test_oauth_system_es_solo_identidad). Ahora es IMPOSIBLE que el 429-system
      tumbe el bot, venga de donde venga.

- [x] ✅ **H6-formula-relevance CERRADO → v2 (2026-06-22)** — Brian eligió "uso real: lo que se
      recupera, se conserva". Implementado el REFUERZO POR USO REAL (antes era neutro):
      (1) migración 009 → columna `veces_recuperado INT DEFAULT 0`; (2) `memory.tocar_recuerdos`
      ahora SUMA 1 al contador cada vez que un recuerdo se recupera (además de refrescar
      last_accessed); (3) `relevance.py` la fórmula usa el contador real: `relevance = decay ×
      (1 + 0.1×min(veces_recuperado,5))`, tope refuerzo +50%, vida media 90d, piso 0.15.
      Verificado E2E: episodio recuperado 6 veces → relevance 0.993→1.000 (sí resiste el olvido).
      Datos de prueba reseteados. 132 tests. Resultado: lo MÁS usado resiste mejor el olvido de la
      Microglía, como la memoria humana. Parámetros ajustables en relevance.py.

- [x] ✅ **H5-mem-matiz CERRADO** (2026-06-22) — el bot ya no es tajante de más sin caer en
      inventar. FIX (FOR3S_ROLE, directriz "JUICIO AL RESPONDER SOBRE LO QUE HAN TRABAJADO"):
      antes de un 'no' rotundo, revisa memoria/conceptos y distingue lo EXACTO vs lo RELACIONADO;
      si hay algo relacionado real, lo ofrece ('de eso exacto no, pero sí trabajamos en X');
      si NO hay nada, dice 'no' limpio. EQUILIBRIO crítico: nunca inventa la conexión. Decisión
      Brian: equilibrado. Verificado E2E con 2 casos: (A) "¿bugs que vimos?" → ofrece los repos
      reales analizados (godinez-studio/Aider/DonutBrowser) + invita a pegar URL; (B) "¿servidor
      de Minecraft?" (nunca pasó) → "No, eso no está en mi memoria — y no voy a inventar que sí
      pasó". Ambos correctos. 130 tests.
- [ ] **H-B** GitHub como CUENTA PROPIA (depende de H-D).
- [ ] **H-C** sistema de pensamiento (estructura tipo Mente OS) + multi-mensaje
      SEMÁNTICO por etapas (mensaje por etapa: análisis→testeo→PoC).
- [ ] **H-G** (Brian 2026-06-17) **SUBAGENTE ASÍNCRONO para repos enormes.**
      Problema: el análisis "a profundidad" SIEMPRE tarda (repo enorme, leer todo
      el código). Hoy es síncrono → bloquea la conversación y el presupuesto de
      tiempo (5 min) solo alcanza ~10/74 de src. La solución NO es darle más
      tiempo al flujo actual. Es de OTRA CAPA, post-MVP: un **subagente en
      segundo plano** que analice el repo COMPLETO por detrás, mientras el agente
      principal de Telegram **sigue trabajando con el usuario sin bloquearse**, y
      solo AVISA cuando termina (notificación, como el pin del cupo). Subprocesos
      en paralelo → el uso de For3s nunca se frena, sin importar el tamaño del
      repo. Es arquitectura multi-agente/async (lo que Hermes tiene y For3s no
      todavía — ver Comparacion_Funcional_For3s_OS_vs_Hermes.md). Requiere diseño
      tipo Ronda antes de programar.
- Detalle completo: `memory/archive/For3s_LO_QUE_NO_PUEDE_HACER.md`.
---

## 🔴 PENDIENTE v2 · RENOMBRADO A LA CONVENCIÓN INGLESA (2026-07-27)

**Decisión de Brian:** *"no renombramos a los 208, eso será un pendiente de v2."*
**Estándar ya escrito:** `rules/NAMING_CONVENTION.md` (en inglés, §7.4 tiene el plan completo).

**Alcance medido:** 208 archivos · 7 carpetas · 185 con guion bajo · 194 con mayúsculas ·
**97 vivos / ~97 fósiles**.

**Renombrado propuesto:** `Alma/`→`principles/` · `Cerebro/`→`rules/` · `Cuerpo/`→`blocks/` ·
`Doc/`→`docs/` · `Maestro/`→`registry/` · `Tickets/`→`bridges/` · `secrets/`→`secrets/` + `bin/`.

**⚠️ Requisitos antes de abrirlo:**
1. commit limpio (sin él no hay rollback: `git mv` solo rastrea si el contenido no cambia)
2. actualizar punteros: `CLAUDE.md` (13 líneas) · `Maestro/punteros.tsv` · `memory/RETOMAR.md`
3. barrer las ~87 memorias (fuera de git, sin historial para revertir)
4. **validador** que pruebe que ningún puntero quedó huérfano

**⭐ Recomendación:** 3 tramos — carpetas → ~97 vivos → **fósiles a `docs/archive/` SIN renombrar**
(archivarlos conserva la señal vivo/fósil que hoy solo da la fecha de modificación).

**Se abre junto con la reestructuración del Mente OS Maestro** (Brian: *"lo vamos a reestructurar y
dentro de ello vamos a corregir los nombres"*).
**Mientras tanto: todo lo NUEVO nace con la convención; lo viejo se renombra al tocarse.**
---

## 🔴 PENDIENTE v2 · REESTRUCTURACIÓN DEL MENTE OS MAESTRO (2026-07-27)

**Origen:** Brian pidió evaluar el Maestro *"porque de eso viene lo de NavigoX"*. La evaluación
confirmó el diagnóstico: **el gate protegía la puerta, no la pared.**

### ✅ Lo que se PROBÓ y funciona (no supuesto — ejecutado)

| Prueba | Resultado |
|---|---|
| `maestro leer navigox` | ⛔ GATE bloqueó |
| `MAESTRO_USER=nadie` sobre `for3s` | ⛔ fail-closed bloqueó |
| `MAESTRO_USER=jazz` sobre `for3s` (núcleo) | ⛔ bloqueó — **carril respetado** |
| Sincronía con su repo | ✅ `master...origin/master`, sin divergencia |

### 🔴 EL FALLO DE ARQUITECTURA — dos sistemas de permisos que no se hablan

```
maestro leer navigox        →  ⛔ BLOQUEA   (gate en maestro_lib.sh)
Read(~/5M-incubathon/**)    →  ✅ PERMITÍA  (additionalDirectories de settings.local.json)
```

**El gate a nivel de COMANDO no protege nada si el filesystem está abierto.** Nunca se usó
`maestro leer navigox` para acceder: se leyeron las rutas directamente, y por ahí no había candado.

**Es el agujero exacto de las 6 violaciones de scope del 21-jul** (`marca-personal/Mente/`):
la regla de `CLAUDE.md` lo prohibía, el permiso técnico lo permitía. **El código gana al documento.**

**✅ MITIGADO 2026-07-27:** añadidas 6 reglas `deny` en `for3s/.claude/settings.local.json`
(Read/Edit/Write sobre `~/5M-incubathon/**` y `marca-personal/Mente/**`). Es un parche correcto,
**no la solución de raíz.**

### 🔴 `Maestro/registro.md` MIENTE

| Dice | Realidad medida |
|---|---|
| For3s OS: **173 docs, 4.5 MB** | **195 docs, 17 MB** |
| **5 ramas** en `Maestro/punteros.tsv` | **6 descritas** en `Maestro/registro.md` |

⚠️ **Gravedad:** **Foresito lo lee EN VIVO** por GitHub MCP (puente E). El agente maestro —examinado
al 98.8%— está informando cifras falsas. Mismo patrón que el `README.md`: escrito a mano → se
desincroniza.

Y el propio `Maestro/punteros.tsv` declara la regla que no se cumple: *"aquí NO se duplica la tabla, la
sincronía a mano murió"*.

### 📋 LOS 4 PUNTOS DEL BLOQUE

| # | Qué | Por qué |
|---|---|---|
| 1 | **Un solo origen de permisos** (o dos generados del mismo) | hoy `Maestro/permisos.md` y `settings.local.json` se contradicen — y se contradecían |
| 2 | **`Maestro/registro.md` GENERADO, no escrito** | miente en las cifras que Foresito lee en vivo |
| 3 | **`Maestro/punteros.tsv` como fuente única real** | el registro debe referenciarlo, no duplicarlo (su propia regla) |
| 4 | **Nombres nuevos:** `Maestro/`→`registry/` · `Tickets/`→`bridges/` | `NAMING_CONVENTION.md` |

### ⚠️ Requisitos y dependencias

- **Cruza con el pendiente de renombrado** (los 208 archivos) — Brian: *"lo vamos a reestructurar y
  dentro de ello vamos a corregir los nombres"*. **Se abren juntos.**
- **Avisar a Foresito:** está entrenado con 1,829 episodios que citan las rutas viejas. Renombrar sin
  actualizar su puente = el agente maestro apunta a rutas fantasma.
- **Reusa `bin/generate-index`** (F7 del plan v2) para el punto 2 — no se inventa mecanismo nuevo.

### Carril

**BLOQUE COMPLETO** (§5 de la arquitectura): toca permisos, scripts, el registro, los nombres y un
agente entrenado. **Cinco sistemas.** No son tickets sueltos.
---

## 🔴 PENDIENTE v2 · LIMPIEZA DE CONFIGURACIÓN (2026-07-27)

**El MECANISMO ya está escrito** (§12-SEPTIES de la arquitectura + F5-5 del plan): 4 reglas que
impiden que la config vuelva a degradarse. **Este pendiente es limpiar LO YA ACUMULADO.**

### ✅ Ya hecho el 2026-07-27 (lo urgente)

| Acción | Resultado |
|---|---|
| Purgar la contraseña del server de `settings.local.json` | **331 entradas eliminadas** · allow 1341→1010 |
| Redactar el secreto en 3 memorias | ✅ |
| Crear `for3s/.gitignore` (no existía) | 40 líneas · cubre `settings.local.json`, secretos, repos anidados |
| 6 reglas `deny` (NavigoX + `marca-personal/Mente`) | el gate pasó de doctrina a candado |
| Limpiar `.claude/` | 464 MB → 442 MB (999 archivos viejos + cache de mayo) |

### ⚠️ RIESGO ASUMIDO — la contraseña NO se rota (decisión de Brian 2026-07-27)

> Brian: *"la contraseña del servidor no la vamos a rotar, corro el riesgo, porque ahorita no es mi
> foco rotar contraseñas — mi foco es otro."*

**Estado del riesgo:** la contraseña estuvo **331 veces** en `settings.local.json` (ya purgado) y
**sigue en el `.jsonl` de la sesión** — los transcripts no se editan. **Purgar no invalida.**

**Mitigante que lo hace defendible:** el servidor es **Tailscale-only** — no está expuesto a
internet. Para usar la contraseña hay que estar dentro del tailnet.

**🔴 CUÁNDO DEJA DE SER DEFENDIBLE — rotar ANTES de:**
- abrir el **Tailscale Funnel** al exterior (ya pasó una vez: `feedback_tailscale_serve_apaga_funnel`)
- dar acceso al tailnet a alguien más
- publicar cualquier repo que arrastre un `.jsonl` o el `settings.local.json`

**Precedente:** el hallazgo H-11 del examen de Foresito fue el mismo caso (la contraseña en 60
episodios de 2 instancias) y **entonces sí se rotó**. La diferencia hoy es el foco, no el riesgo.

### ✅ LIMPIEZA EJECUTADA el 2026-07-27 (era más barata de lo estimado)

| Qué | Antes | Ahora |
|---|---|---|
| `allow` | **1,341** | **127** (−91%) |
| `deny` | 0 | **6** |
| `additionalDirectories` | 9 | **4** |
| Secreto en texto plano | 331 líneas | **0** |
| `.claude/` en disco | 464 MB | 442 MB |

**Criterio conservador aplicado — NO se colapsó todo al mínimo teórico:**

| Conservado literal | Por qué |
|---|---|
| Los **15 `Bash(rm ...)`** | `Bash(rm *)` autorizaría borrar cualquier cosa sin preguntar |
| Skill · Read · Edit · Write específicos | granularidad útil, no redundancia |

**Los 234 `sshpass` → 1 entrada con la forma correcta:**
```
Bash(sshpass -p "$FOR3S_SSH_PASS" *)
```
> Las 234 originales **ya no servían**: al purgar el password quedaron como plantillas con un valor
> que no coincide con ningún comando real. La nueva **referencia la variable** — es la regla 1
> (§12-S.1) aplicada en la práctica.

**Rutas: 9 → 4.** Fuera 3 **muertas** (`/tmp/h2` · un scratchpad de la sesión muerta el 13-jul ·
un `__pycache__`) y 2 que **contradecían el `deny`** (`5M-incubathon` · `marca-personal/Mente/Alma`).

**Reversión:** 2 respaldos en el scratchpad de la sesión (pre-purga y pre-limpieza).

> ⚠️ **Efecto esperado:** Claude Code puede preguntar por algún comando que antes pasaba solo.
> Se aprueba una vez y queda guardado — **ahora con la forma correcta**, no como la variante 235.

### 📋 Lo que SIGUE pendiente

| # | Qué | Medido |
|---|---|---|
| 1 | **689 rutas absolutas → portables** | `$CLAUDE_PROJECT_DIR` / `$HOME` — nadie más puede usar esto |
| 2 | **Documentar los 9 hooks GSD como no portables** | rutas absolutas de un sistema externo: límite **declarado**, no oculto |
| 3 | Revisar los 127 restantes con la prueba de §12-S.3 | *¿autoriza algo que ninguna otra ya autoriza?* |

**Cruza con:** el pendiente de renombrado (208 archivos) y la reestructuración del Maestro.
**No bloquea el v2** — el mecanismo (§12-SEPTIES) ya impide que empeore.
---

## 🟡 PENDIENTE v2 · LO QUE QUEDÓ ABIERTO DE F0 (2026-07-27)

**F0 se cerró** (4/4 tickets) pero dejó 4 cosas sin hacer:

| # | Qué falta | Quién | Bloquea |
|---|---|---|---|
| 1 | **§6 de `owner-0-voice.md` — "Brian's additions"** está en blanco a propósito | ⭐ **Brian** | nada — la voz ya funciona con las 8 reglas medidas |
| 2 | **Verificar la voz en una sesión nueva** — los output styles cargan al arrancar, no en caliente | los dos | nada |
| 3 | **Las 26 decisiones están DUPLICADAS** en Arquitectura §17.1 y Visión §6 | IA | 🔴 **ya empezaron a desincronizarse** |
| 4 | **No existe estándar para tomar decisiones nuevas** | ver bloque siguiente | 🔴 sí |

### Sobre el #1 — qué va en §6 de la voz

Las 8 reglas actuales salen de **observación con evidencia** (lo medido el 27-jul). §6 es para
**criterio de Brian** que no se observó: nivel de detalle técnico que prefiere · cuándo quiere que se
le cuestione vs. cuándo quiere ejecución · términos que le molestan · cuánto contexto asumir.

### Sobre el #3 — la duplicación ya es un problema real

`Arquitectura §17.1` y `Visión §6` **contienen la misma tabla de decisiones.** Medido: 75 filas vs
37 — **ya divergieron.** Es exactamente el fallo que el v2 existe para eliminar
(`Maestro/punteros.tsv`: *"aquí NO se duplica la tabla, la sincronía a mano murió"*).

**Arreglo:** una sola fuente (`docs/DECISIONS.md`) y los otros dos documentos la **apuntan**.
Cruza con el bloque siguiente.

---

## ✅ CERRADO 2026-07-29 · ESTÁNDAR PARA TOMAR DECISIONES (ADR)

**HECHO:** `rules/contract-adr.md` (el estándar) + **27 ADR individuales** en `rules/decisions/`
(`ADR-001` a `ADR-027`, numeración sin huecos) + **`docs/DECISIONS.md` generado** (55 líneas).
**Validado contra el contrato:** los 27 tienen los 6 campos, `status` válido, y `Evidence` y
`Reverting` no vacías.

**Queda solo (tras F7):** borrar las tablas duplicadas de `Arquitectura §17.1` y `Visión §6`.
Ya llevan el aviso de que la fuente única es `docs/DECISIONS.md` — **no se borran ahora porque son
la única copia legible hasta que `bin/generate-index` exista.**

<details><summary>Diagnóstico original (histórico)</summary>

## 🔴 PENDIENTE v2 · ESTÁNDAR PARA TOMAR DECISIONES (ADR) — 2026-07-27

> **Brian:** *"para generar una nueva decisión o una nueva regla o ruta, ¿existe un estándar que
> podamos crear para que no se salga de control?"*

**Respuesta: hoy NO existe.** Se tomaron **26 decisiones en una sesión** sin ningún estándar:
viven en una tabla, sin fecha individual, sin autor, sin motivo trazable, **duplicadas en 2 sitios**.

### El problema, medido

| Síntoma | Dato |
|---|---|
| Decisiones tomadas hoy | **26** |
| Con fecha individual | ❌ solo "2026-07-27" en el título de la tabla |
| Con el motivo trazable | 🟡 en el cuerpo del documento, no en la decisión |
| Duplicadas en 2 documentos | 🔴 **sí — 75 vs 37 filas, ya divergieron** |
| Con archivo propio y reversible | ❌ ninguna |
| ¿Se puede saber qué decisión invalidó a otra? | ❌ no |

**Precedente del propio proyecto:** `CLAUDE.md` gobierna todo y tiene **1 solo commit** en su
historia. Las reglas cambiaron muchas veces y **ninguna dejó rastro**. Este pendiente evita que el
v2 repita eso.

### El estándar propuesto — ADR (Architecture Decision Record)

Ya está adoptado como convención de nombres (`NAMING_CONVENTION.md` §4.2: `ADR-NNN-nombre.md`).
Falta **el mecanismo**.

**Un archivo por decisión**, en `rules/decisions/`, con 6 campos fijos:

```markdown
# ADR-009 · Single file per block

date: 2026-07-27
status: accepted          # proposed | accepted | superseded | reverted
decided-by: brian
supersedes: —             # ADR-NNN si reemplaza a otra
context:    por qué se planteó (el problema, con datos)
decision:   qué se decidió, en una frase
rationale:  por qué esta y no la alternativa
evidence:   el dato que la respalda
reverting:  cómo se deshace si sale mal
```

### Las 3 reglas del estándar

| # | Regla | Qué evita |
|---|---|---|
| 1 | **Una decisión = un archivo.** Nunca una fila en una tabla compartida | la duplicación que ya ocurrió |
| 2 | **`docs/DECISIONS.md` se GENERA** desde los ADR — nadie la escribe a mano | que el índice mienta |
| 3 | **Una decisión no se edita: se SUPERSEDE** con otra que la apunta | perder el historial de por qué cambió |

### Qué aplica a reglas y rutas (no solo a decisiones)

| Objeto nuevo | Requisito mínimo |
|---|---|
| **Decisión** | ADR con los 6 campos |
| **Regla** (`rules/rule-*.md`) | nace de un ADR que la justifica · la regla apunta a su ADR |
| **Ruta** (`additionalDirectories`, puntero) | comentario con **fecha + motivo** (§12-S.2) · pasa la prueba de no-redundancia (§12-S.3) |
| **Validador** (`bin/*`) | ADR que explique qué comprueba y por qué |

### Trabajo que implica

| Tramo | Qué |
|---|---|
| 1 | Escribir `rules/contract-adr.md` — la plantilla y las 3 reglas |
| 2 | **Migrar las 26 decisiones** de hoy a ADR individuales |
| 3 | `bin/generate-index` genera `docs/DECISIONS.md` desde los ADR |
| 4 | Quitar las tablas duplicadas de Arquitectura §17.1 y Visión §6 → dejar el puntero |

**Carril:** bloque completo. **Cruza con** el pendiente de renombrado y la reestructuración del Maestro.
**Prioridad:** alta — cada decisión nueva que se tome sin este estándar agrava la deuda.

</details>

---

## 🔴 PENDIENTE v2 · PARTIR LA ARQUITECTURA (2026-07-29)

**La regla ya está escrita** (§3.2-QUATER: arquitectura ≤800 líneas). **Este pendiente es aplicarla.**

**Estado:** `Cuerpo/Arquitectura_Mente_OS_v2_Bloques.md` = **2,454 líneas** · límite 800 → **3× el límite.**
Creció de 995 a 2,347 en **una sola sesión** (+1,352).

### 🤖 EVIDENCIA DEL VALIDADOR (2026-07-29) — ya no es opinión

`bin/check-blocks` lo confirma solo:
```
Cuerpo/Arquitectura_Mente_OS_v2_Bloques.md
   2454 lines — over the architecture limit of 800
   12 grown section(s) → split signal: 0-BIS, 0-BIS.1 … 12-BIS, 12-TER, 12-QUATER,
                                        12-QUINQUIES, 12-SEXIES, 12-SEPTIES
```

> ⚠️ **El validador NO lo veía al principio:** la exención por carpeta legacy (`Cuerpo/`) tapaba el
> archivo más importante del v2. **Corregido:** un archivo con header `**Type:**` se valida **donde
> sea que viva** — optar por el contrato pesa más que la carpeta.
> **Es el único archivo del sistema con la señal de partir.** Los otros 3 avisos eran secciones
> `-bis` añadidas después (owner-3, visión, plan) y **ya se renumeraron.**

### Los 5 documentos que contiene, por sus propios nombres

| Sección | Qué es realmente |
|---|---|
| `12-TER` validadores | manual de herramientas |
| `12-QUATER` garantía de lectura | mecanismo de aplicación |
| `12-QUINQUIES` veredicto de calidad | **el sistema de QA** |
| `12-SEXIES` la voz | **el estándar de comunicación** |
| `12-SEPTIES` higiene de config | **el manual de configuración** |

**Cinco documentos que crecieron dentro de uno.** Prueba directa de la regla:
*un archivo se parte cuando contiene dos cosas distintas — el límite es la señal.*

### Por qué NO se hizo el 2026-07-29

Sesión de **74 horas** con **contexto máximo 726K** (umbral rojo: 500K) y **14 API errors** — el mismo
patrón del incidente del 21-jul (835K, 11 errors, **6 violaciones de scope no detectadas**).

> **Partir un documento de 2,347 líneas requiere sostener el mapa de qué sección referencia a cuál.**
> Es exactamente el trabajo que peor sale con el contexto saturado. **Se aplazó a propósito.**

**Criterio aplicado:** *lo que solo AÑADE es reversible por omisión; lo que MUEVE requiere no
equivocarse.* Se escribió la regla (añade) y se aplazó la partición (mueve).

### El corte propuesto — por CONTENIDO, no por tamaño

| Documento nuevo | Qué se lleva | Aprox |
|---|---|---|
| `blocks/architecture-core.md` | §0-BIS idioma · §1-§8 (bloque, owners, lanes, ciclo, fix≠patch, friction) | ~700 |
| `rules/learning-system.md` | §9 expertise · §10 aprendizaje (10.1-10.6) | ~250 |
| `rules/context-and-validators.md` | §11 contexto/tiers · §12-TER/QUATER/QUINQUIES/SEXIES/SEPTIES | ~900 → **partir en 2** |
| `docs/architecture-status.md` | §13 sistemas · §14 migración · §15 no se toca · §16 principios · §17 pendientes | ~300 |

### 🔴 El riesgo real — y por qué necesita validador

**Un enlace roto en markdown NO da error.** Se rompe en silencio y se descubre semanas después.

**Referencias que hay que reapuntar:**

| Origen | Referencias a secciones |
|---|---|
| Dentro del propio documento (`§12-T.1`, `§3.2-TER`, `§11.4`…) | **decenas** |
| `docs/plan-v2-rollout.md` | varias |
| `Vision_Mente_OS_v2...md` | varias |
| `rules/qa-dimensions.md` · `contract-adr.md` · los 3 `expertise/*` | varias |
| Las memorias | varias |

**Procedimiento obligatorio:**
1. Inventariar **todas** las referencias `§` antes de mover nada
2. Mover por documento, **verificando tras cada uno**
3. Reapuntar las referencias con la nueva ruta
4. **Validador** que pruebe que ninguna `§` quedó huérfana ← sin esto no se cierra

### ⏱️ ESFUERZO — lleva tiempo y prueba/error (Brian, 2026-07-29)

> Brian: *"eso va a llevar tiempo y prueba y error."*

**No es un refactor mecánico.** Un `sed` masivo no sirve: cada referencia `§` hay que decidirla, y
algunas secciones se referencian entre sí a través del corte.

| Por qué es prueba y error | |
|---|---|
| **El corte no se sabe hasta intentarlo** | §12-QUINQUIES (QA) referencia §12-Q.3 y §12-T.1 — puede que no se dejen separar |
| **`context-and-validators.md` sale a ~900 líneas** | ya excede el límite → hay que partirlo otra vez, y no está claro dónde |
| **Se descubre al mover** | igual que F3-5 del plan: *"si el diseño falla, se corrige AQUÍ"* |
| **Los enlaces rotos no avisan** | cada iteración necesita el validador para saber si quedó bien |

**Método recomendado — iterativo, no de una pasada:**
1. Inventariar referencias · **construir el validador PRIMERO** (sin él no se puede iterar)
2. Mover **el documento más independiente** (`learning-system.md`) → validar → ajustar
3. Repetir con el siguiente, aprendiendo del anterior
4. Dejar `architecture-core.md` **para el final** — es el que más referencias recibe

> ⭐ **El validador va primero, no al final.** Es lo que convierte prueba-y-error en iteración
> controlada: sin él, cada intento fallido se descubre semanas después.

**Carril:** bloque completo. **Requisito:** contexto limpio (<200K) al empezar.
**Estimación honesta:** varias sesiones. No se cierra en una.

---

## 🟡 PENDIENTE v2 · ROTAR ESTE ARCHIVO POR CIERRE (2026-07-29)

**La regla ya está escrita** (§3.2-QUATER de la arquitectura). **Este pendiente es aplicarla a este
mismo archivo.**

**Estado medido:** **3,213 líneas · 253 KB.** El archivo donde se registran los pendientes es, él
mismo, uno de los pendientes.

### La regla

| | |
|---|---|
| **Límite** | ninguno — es append-only, un pendiente no se borra porque el archivo creció |
| **Rotación** | **por CIERRE, no por fecha** — un pendiente de enero puede seguir abierto en diciembre |
| **Destino de lo cerrado** | `docs/archive/pendientes-<año>.md`, con su fecha de cierre |
| **Contenido de `PENDIENTES.md`** | **solo lo ABIERTO** |

### ⭐ Por qué importa

**El tamaño pasa a ser una métrica útil: si crece, la deuda crece.**
Hoy no dice nada porque mezcla lo abierto con lo ya resuelto.

### Trabajo

1. Recorrer el archivo separando cerrado de abierto (hay marcas `✅ CERRADO` / `RESUELTO`)
2. Mover lo cerrado a `docs/archive/pendientes-2026.md` con su fecha
3. `check-health` avisa si un item cerrado vuelve a colarse

**Carril:** tarea, no bloque completo — **nada referencia secciones internas de este archivo**
(a diferencia de partir la arquitectura, que tiene decenas de `§` apuntándole).
**Requisito:** ninguno especial. Se puede hacer en cualquier sesión.

---

## 🔴 PENDIENTE v2 · EL SISTEMA DE ENCARPETADO NO ESTÁ TERMINADO (2026-07-29)

> **Duda de Brian:** *"¿cuándo modificamos el sistema de encarpetado para que Mente OS tenga el
> sistema nuevo?"* — la respuesta era incómoda: **estaba pasando ya, a medias, sin decisión explícita.**

### Estado real — encarpetado MIXTO

| Nueva (convención) | Archivos | Vieja | Archivos |
|---|---|---|---|
| `principles/` | 8 | `Alma/` | 7 |
| `rules/` | 39 | `Cerebro/` | 6 |
| `docs/` | 5 | `Doc/` | **75** |
| `blocks/` | 0 (creada, vacía) | `Cuerpo/` | **85** |
| `bin/` | ⬜ **no existe** | — | — |

**Los tres pares conviven con archivos en ambos lados.** La decisión 16 dice *"la estructura nueva
CONVIVE"* y se aplicó literal — técnicamente correcto, **prácticamente confuso**: hay dos sitios
plausibles para cada cosa.

### ✅ Hecho el 2026-07-29 — los 5 mal ubicados

Se movieron los que eran baratos (≤10 referencias, escritos ese mismo día):

| De | A | refs reapuntadas |
|---|---|---|
| `Cerebro/NAMING_CONVENTION.md` | `rules/NAMING_CONVENTION.md` | 10 |
| `Alma/Vision_Mente_OS_v2_...md` | `principles/vision-mente-os-v2.md` | 6 |
| `Cuerpo/Plan_Implementacion_...md` | `docs/plan-v2-rollout.md` | 5 |
| `Doc/Analisis_Comparativo_...md` | `docs/analysis-frameworks-v2.md` | 2 |
| `Doc/Analisis_internOS_v1_...md` | `docs/analysis-internos-v1.md` | 6 |

**Verificado: 0 punteros huérfanos** (20 archivos actualizados, incluidas memorias y `CLAUDE.md`).

> ⭐ **El caso que lo motivó:** `NAMING_CONVENTION.md` vivía en `Cerebro/` — **el estándar de nombres
> incumplía el estándar de nombres.**

### 🔴 LO QUE FALTA

| # | Qué | Bloqueo |
|---|---|---|
| 1 | **`Arquitectura_Mente_OS_v2_Bloques.md` → `blocks/architecture-v2.md`** | 🔴 **42 referencias** — no es barato. Cruza con el pendiente de PARTIR la arquitectura: **conviene mover y partir en la misma operación** |
| 2 | **`bin/` no existe** | se crea en F4/F5 con el primer validador |
| 3 | **`Maestro/` → `registry/`** | cruza con la reestructuración del Maestro (sub-repo con su propio git) |
| 4 | **`Tickets/` → `bridges/`** | 6 archivos, congelados desde 14-jun |
| 5 | **`secrets/` → `secrets/`** | ⚠️ ignorado por `.gitignore` — hay que actualizar el patrón ANTES de mover |
| 6 | **Los ~160 archivos de `Cuerpo/` y `Doc/`** | el pendiente de renombrado — por demanda |
| 7 | **Marcar los ~97 fósiles** con `Status: fossil` y moverlos a `docs/archive/` | hoy nada distingue vivo de fósil salvo la fecha |

### ⚠️ Riesgos identificados

- **`secrets/` → `secrets/`**: si se mueve sin actualizar `.gitignore` primero, **los secretos
  quedan rastreables**. El orden importa: gitignore → mover → verificar.
- **`Maestro/`** tiene su propio `.git` y `Mente/.gitignore` lo excluye. Renombrarlo afecta a
  `Maestro/punteros.tsv` y al puente E de Foresito.
- **Convivencia prolongada = confusión.** Cuanto más tiempo con los pares duplicados, más
  probable que algo nuevo nazca en la carpeta vieja.

### Criterio para continuar

**Un archivo se mueve cuando: (a) se toca por otro motivo, o (b) tiene ≤10 referencias.**
Todo lo demás espera al bloque de renombrado, que **se abre junto con la reestructuración del Maestro**.

---

## ✅ CERRADO 2026-07-30 · 3 DOCS DE LA DEMO SECUESTRADOS

**RESUELTO.** Brian ejecutó los `mv` (el `deny` protege ese directorio de la IA a propósito) y la IA
verificó y commiteó.

| Archivo | Destino | Bytes |
|---|---|---|
| `Demo_For3s_Avance.md` | `blocks/active/demo/docs/demo-progress.md` | 10,592 ✅ |
| `GUIA_Registrar_GitHub_OAuth_App.md` | `docs/guide-github-oauth-app.md` | 2,738 ✅ |
| **`Plan_Pieza_E_Concentrado_Admin.md`** | `docs/plan-piece-e-admin.md` | 10,948 ✅ |

**Íntegros byte a byte.** Commits en `marca-personal`: `fb3c8d3` + `a3b7ff5`.
⚠️ **2 commits SIN PUSH** — Vercel despliega de `main`, así que el push es decisión de Brian.

### 🔴 2 hallazgos que aparecieron al ejecutar

**① Era una violación MÁS de las contadas.** `Plan_Pieza_E` también lo escribió la IA el 2026-07-20
(4 ediciones entre 18:45 y 19:06, del jsonl). **Yo solo había contado los archivos con "Demo" o
"GUIA" en el nombre** — el criterio de búsqueda era el nombre, no el contenido.

**② El `mv` rompió git.** Los 6 archivos estaban rastreados en `marca-personal`. Mencioné `git mv`
como opcional cuando no lo era. Resuelto con `git add -A` + commit.

> ⭐ **Lo que enseñó:** un archivo mal ubicado **no se detecta por su nombre.** Los 3 que quedaron
> (`README`, `Impeccable_Workflow`, `Estado_Sesion_Continuidad`) son de junio y de marca-personal —
> legítimos. Los 3 movidos eran todos del 20-21 de julio: **la fecha delató el origen, no el nombre.**

### ✅ LOS 2 HALLAZGOS, SOLUCIONADOS EN EL SISTEMA (2026-07-30)

No se arreglaron "con cuidado la próxima vez" — se arreglaron con código y con una regla.

**① Detección por ORIGEN, no por nombre → `bin/check-health --misplaced`**

Cruza **dos señales medibles**: fecha de modificación dentro de una ventana de incidente conocida
(2026-07-20/21) **+** vocabulario de For3s OS en el contenido (`For3s OS`, `Pieza E`, `api_channel`…).

**Probado retrospectivamente** contra el estado del 29-jul: cazó **los 2** (incluido
`Plan_Pieza_E`, el que mi búsqueda por nombre perdió) y **no marcó** el `README.md` de junio.
**Cero falsos positivos.**

**② `git mv` obligatorio → `rules/rule-moving-files.md`**

Secuencia de 5 pasos donde *"¿está rastreado?"* es el **paso 1**, no un consejo:
`git ls-files` → `git mv` si está rastreado → repuntar referencias → verificar 0 huérfanos → commit.
+ verificación afirmativa: **bytes antes == bytes después**, no *"se movió bien"*.

> ⭐ **La lección de método:** *"comprueba si está rastreado"* mencionado de pasada **es un paso que
> se va a saltar.** Un condicional dicho al vuelo no es un procedimiento.

**Bonus:** los 3 archivos recuperados recibieron su header del contrato, y ahí salió el dato útil —
**solo 1 de los 3 está vivo**: `guide-github-oauth-app.md` (paso operativo pendiente de Brian).
Los otros 2 son `fossil`.

<details><summary>Diagnóstico original</summary>

## 🟡 PENDIENTE (histórico) · 3 DOCS DE LA DEMO SECUESTRADOS (2026-07-29)

**Hallado en F3** al medir qué afecta cada límite del bloque `demo`.

### El problema

`marca-personal/Mente/Doc/` contiene **documentación de la demo** — pero ese directorio está
**doblemente bloqueado**: prohibido por `CLAUDE.md:24` y con `deny` técnico en
`settings.local.json` desde 2026-07-29.

| Archivo bloqueado | Qué es |
|---|---|
| `Demo_For3s_Avance.md` | avance de la demo |
| `GUIA_Registrar_GitHub_OAuth_App.md` | guía operativa que Brian necesita para la OAuth App |
| `Estado_Sesion_Continuidad.md` | (de marca-personal, no de For3s OS) |

### De dónde salieron

**Los escribí yo el 2026-07-21, durante el incidente de degradación.** Fueron 2 de las
**6 violaciones de scope** de esa sesión (contexto 835K). **Están en el sitio equivocado desde
entonces y nadie lo limpió.**

### Por qué importa

**El límite es correcto; la ubicación de los archivos no.** Hoy hay información operativa de la demo
que **es técnicamente imposible de leer** — y la `GUIA_Registrar_GitHub_OAuth_App.md` es un paso que
Brian necesita ejecutar.

> ⭐ **No es un conflicto del diseño: es basura del incidente del 21-jul.** El `deny` de hoy no creó
> el problema — lo hizo visible.

### El arreglo

1. **Brian levanta el `deny` temporalmente** (o los mueve él mismo — es su directorio)
2. Mover los 2 que son de la demo → `blocks/active/demo/docs/`
3. Dejar `Estado_Sesion_Continuidad.md` donde está (es de marca-personal, ahí pertenece)
4. Restaurar el `deny`

**Carril:** tarea. **Requisito:** Brian, porque el `deny` lo protege de mí a propósito.
**Nota:** yo no puedo hacerlo solo — y eso es el diseño funcionando, no un obstáculo.

</details>

---

## 🔴 PENDIENTE v2 · MIGRAR A LAS 3 JERARQUÍAS DE REGLAS (2026-07-29)

> **Brian:** *"el sistema NO SOLO LO VOY A OCUPAR PARA DEMO, y entonces el resto de lo que haga va a
> estar contagiado con esas reglas… existirían 3 jerarquías: universales, por proyecto y por bloque,
> **como POO con sistemas de herencia**."*

**La regla ya está escrita:** `rules/rule-inheritance.md`. **Falta aplicarla.**

### El problema medido

De las **8 no-negociables** de `base-rules.md`, solo **5 son universales**:

| 🏢 Está en el nivel equivocado | Solo importa si… |
|---|---|
| Never read another Mente OS without the gate | trabajas cerca de NavigoX |
| Server-first / push manual | el repo tiene deploy automático |

Y `CLAUDE.md` tiene **3 reglas de proyecto inyectadas en cada sesión**:
`NO tocar marca-personal/Mente` · `NO mezclar con For3s QA` · `NO leer ~/5M-incubathon`.

> 🔴 **La consecuencia:** si Jazz clona Mente OS para diseño, **hereda una regla sobre NavigoX** —
> un proyecto que no es suyo. Contamina cualquier trabajo que no sea For3s OS.

### El modelo

```
🌐 UNIVERSAL   Mente/base-rules.md          las 5 de conducta · aplican SIEMPRE
🏢 PROJECT     <proyecto>/PROJECT-RULES.md  🔴 NO EXISTE AÚN
📦 BLOCK       BLOCK.md §B                  ✅ ya existe
```

**Herencia: solo ADD o TIGHTEN, nunca LOOSEN.** Un bloque no puede concederse lo que el padre prohibió.
**Suma entre bloques:** solo por conexión DECLARADA en §C; si hay conflicto, **gana la más estricta**.

### Los 4 pasos — el ORDEN importa

| # | Paso | ⚠️ |
|---|---|---|
| 1 | Crear `PROJECT-RULES.md` de For3s OS **con** las 3 de `CLAUDE.md` + las 2 de `base-rules` | **PRIMERO** |
| 2 | Quitar esas 3 de `CLAUDE.md` y marcar las 2 en `base-rules` | después |
| 3 | `CLAUDE.md` pasa a ser **enrutador**, no almacén de reglas | |
| 4 | `bin/check-blocks`: detectar reglas en el nivel equivocado y bloques que repiten heredadas | |

> 🔴 **Crear antes de quitar.** Si se quita de `CLAUDE.md` primero, una sesión intermedia **pierde la
> regla del todo** — y el gate de NavigoX protege consumo de tokens.

### Por qué no se hizo hoy

Toca `CLAUDE.md` (se inyecta en cada sesión) y `base-rules.md` (la puerta del sistema). Un error ahí
**afecta a todas las sesiones siguientes**, no solo a un bloque. **Carril: bloque completo.**

**Nota:** el bloque `demo` ya separa `⛔ OUT` (propio) de `🌐 System-wide rules` (heredadas) — se hizo
en F3, así que el patrón está probado antes de la migración.

### 🟡 `plan-v2-rollout.md` en 413/400 líneas (2026-07-30)

Pasó su límite al documentar F4. Se sacaron 2 secciones que eran bitácora, no plan
(`docs/f4-execution-log.md`) y bajó de 460 → 413. **Faltan 13 líneas.**

**NO se sigue recortando a mordidas** — eso es el patrón de parche que `rule-fix-not-patch.md`
prohíbe. El límite es la SEÑAL (ADR-027): el plan tiene 9 fases y crecerá con F5-F8, así que la
partición correcta es **una fase = un archivo** cuando cierre F5, no cortar líneas hoy.

**Cuándo:** al cerrar F5.

### 🟡 31 warnings de rutas sin raíz en 18 archivos (medido 2026-07-30)

`bin/check-blocks` reporta 31 🟡: rutas escritas sueltas (`owner-2-dev.md`) en vez de desde la raíz
de Mente (`principles/owner-2-dev.md`). **Preexistentes**, no introducidos por F4 — están en
`base-rules.md`, los 3 `principles/owner-*`, `rules/*`, la arquitectura y los docs recuperados.

**Por qué importa:** una ruta suelta no se puede seguir desde otro directorio, y es lo que hace que
un puntero muera silenciosamente al mover un archivo.

**Cuándo:** junto al renombrado de los 208 — es el mismo barrido de rutas.

### 🟡 los ADRs no están enlazados desde ningún índice (medido 2026-07-30)

`bin/grade-block t-docs` (tipo `docs`) sobre `rules/decisions/` cazó **1 huérfano real**: el propio
ADR-028 que se acababa de escribir. Nadie lo enlazaba. Se cerró citándolo desde
`contract-block.md`, **pero el patrón sigue abierto**: cada ADR nuevo nace huérfano hasta que
alguien se acuerda de enlazarlo a mano.

**La causa raíz:** `contract-adr.md` dice que el índice es GENERADO, y el generador no existe.

**El arreglo real:** el índice de ADRs se genera en F7 (`docs/INDEX.md`). Hasta entonces, correr
`bin/grade-block` con un bloque `docs` sobre `rules/decisions/` detecta los huérfanos.

**Cuándo:** F7 (generar índices).

### 🔴 la demo tiene 0 archivos de test en TODO el sitio (medido 2026-07-30)

`bin/grade-block demo` → 🔴 MVP. Dos rojos: `ConnectClaude.tsx` huérfano (ya es el sub-bloque 10 del
bloque demo) y **cero tests**. El sub-bloque 8 existe para esto y sigue `open`.

**Por qué está aquí y no solo en el bloque:** es la razón #1 por la que la demo no puede entregarse
como producto, y sobrevive a que el bloque se cierre.

**Cuándo:** sub-bloque 8 del bloque demo — Brian marca el momento.

