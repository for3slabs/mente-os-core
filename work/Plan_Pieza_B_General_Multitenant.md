# 🧩 Plan detallado — Pieza B: general multi-tenant (la demo web POR FIN conversa con el agente)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Plan_Pieza_B_General_Multitenant.md → work/Plan_Pieza_B_General_Multitenant.md (2026-07-30, ADR-029)

## Purpose

🧩 Plan detallado — Pieza B: general multi-tenant (la demo web POR FIN conversa con el agente)


> **Pendiente madre:** Conectores self-service (`vision/Vision_Conectores_SelfService_Panel_Agente.md`).
> **Método pieza por pieza** (Brian 2026-07-20). Pieza B = 3ª que se construye (tras E, A).
> **Visión alineada + decisiones tomadas (Brian, 2026-07-20). Este plan → aprobar → construir.**
> Proyectos: sitio (`marca-personal`) + For3s OS (server). Creado 2026-07-20.

---

## 0 · Qué resuelve (visión alineada con Brian)

**El hallazgo que redefinió B:** hoy la demo web **NO conversa con For3s**. Registra al usuario,
guarda su API key cifrada, prende/apaga contenedores — pero **no existe "escríbele al agente y
responde"**. El paso 3 de la visión de Brian ("usarlo") no existe aún.

**B enciende ese flujo, multi-tenant:** el usuario de `general` escribe desde la web → va por el
canal API al agente **general vivo** (compartido) → con su correo como identidad → su hilo
**aislado** (doctrina AI1, ya existe). El agente es lo ÚNICO compartido; cada correo tiene su
memoria, sus keys, sus (futuros) conectores. Esto hace la demo VIVA y es la base de C y D.

## 1 · Decisiones tomadas (Brian, 2026-07-20)

- **B-D1 · Corazón de B:** construir la **conversación web ↔ general compartido** (no solo la
  identidad). Es el flujo que falta; sin él no hay "usarlo".
- **B-D2 · Key del chat = BYOK:** el agente responde con la **API key propia del usuario** (la que
  ya pegó, cifrada en la demo). Su billing paga. Legal, escalable, justo.
- **B-D3 · Identidad = correo** (de la pieza A): el correo del usuario es su `X-Client-Id` → su hilo.

## 2 · Terreno investigado (2026-07-20)

**Canal API de For3s (ya tiene casi todo):**
- Multi-tenancy AI1: `X-Client-Id` → persona sintética + hilo `api:<cliente>:<tema>` aislado.
  Mismo Client-Id → mismo hilo (retoma). `/v1/chat` responde. `/v1/olvidar` borra lo suyo.
- **BYOK completo:** `POST /v1/token` registra el token cifrado del cliente en el vault;
  `_provider_de` usa la key del cliente si `byok=true`, else cortesía. Descifra al vuelo, no retiene.
- General: canal API **ON** + key demo presente. Listo para recibir.
- Pieza A: `/v1/whoami` da la identidad de la instancia. `admin_email` de general = null (correcto).

**Sitio (`marca-personal`):**
- La demo ya cifra/descifra la API key del usuario (`lib/demo/crypto.ts`, `api_key_enc`) →
  el BYOK del usuario ya está guardado, falta ENVIARLO al canal API.
- Endpoints demo: register, apikey, profile, agent (prende/apaga, general→403), heartbeat…
  **NO hay `/chat`.** La web llega al server por `FOR3S_PUBLIC` (túnel/tailnet).
- Shell con Perfil/Conectores; falta la superficie de conversación.

## 3 · Contratos con otras piezas

- **B usa A:** el correo (identidad de A) es el `X-Client-Id`. Si un día se valida contra
  `/v1/whoami`, ya existe.
- **B habilita C/D:** una vez que el usuario conversa con SU hilo por SU correo, los conectores (C)
  y las API keys self-service (D) cuelgan de esa misma identidad (`X-Client-Id = correo`).
- **B reusa el canal API** (no crea otro camino): la web es un cliente más de `/v1/chat` (como
  NavigoX). Cero duplicación del motor de conversación.

## 4 · Plan por fases

### B1 · El puente de conversación: `/api/demo/general/chat` (sitio)
- Endpoint nuevo en el sitio: recibe `{ message }` del usuario logueado (sesión demo) →
  llama `POST {FOR3S_PUBLIC}/v1/chat` con `X-Client-Id: <correo>` + `X-API-Key: <key demo del
  general>` → devuelve `{ reply }`. El correo sale de la sesión (no se confía del body).
- *Investigar terreno:* ya hecho — reusa `readDemoSession`, `FOR3S_PUBLIC`, patrón de `for3sAdmin`.
- *Red:* sin sesión → 401; dos correos distintos → dos hilos aislados (no se ven).

### B2 · BYOK del usuario llega al canal (registro de su key)
- Cuando el usuario guarda su API key (endpoint `apikey` ya cifra en `api_key_enc`), B añade:
  registrar esa key en el canal API vía `POST /v1/token` para SU `X-Client-Id` (correo), de modo
  que `/v1/chat` responda con SU key (BYOK). La key viaja del sitio al canal **descifrada una vez**
  (server-side, nunca al navegador), el canal la re-cifra en su vault. Se marca el cliente `byok`.
- *Ojo seguridad:* la key se descifra en el server del sitio (donde ya está `DEMO_ENC_KEY`) y se
  manda al canal por el túnel; el canal la guarda en SU vault. Doble cifrado en reposo, plano solo
  en tránsito interno tailnet. Auditado.
- *Red:* usuario con key → chat usa su billing (verificable en el panel admin, columna BYOK);
  usuario sin key → cortesía For3s (fallback del canal, aunque B-D2 es BYOK, el canal ya degrada).

### B3 · La UI de conversación en el shell de la demo
- En el shell (hoy Perfil/Conectores), sumar la superficie de **chat**: caja de mensaje +
  historial de la sesión. Llama a `/api/demo/general/chat`. Diseño con la skill `impeccable`
  (coherente con el shell existente).
- *Red:* conversación real de ida y vuelta; el historial es el del hilo del usuario (retoma al volver).

### B4 · Aislamiento verificable (la prueba de fuego multi-tenant)
- Dos correos distintos en general → cada uno su hilo, su memoria; uno NO ve lo del otro
  (doctrina AI1, pero verificado E2E con la demo web real, no solo el canal).
- `/v1/olvidar` del usuario borra SOLO lo suyo.

## 5 · Batería (§5-BIS)
- Sitio: build/lint/types verdes. Endpoint chat: sin sesión→401, con sesión→reply real.
- E2E: usuario A (correo A) conversa → hilo A; usuario B → hilo B; A no ve B. BYOK: key de A
  usada para A (panel muestra BYOK+consumo de A). Sin key→cortesía.
- Server: canal API general responde `/v1/chat` con X-Client-Id=correo; `/v1/token` registra la
  key; sin regresión de NavigoX/otros clientes. Los otros bots intactos.
- Sitio pusheado (con orden) + server tríada si toca código de For3s (B casi todo es sitio +
  reuso del canal; si el canal necesita algo nuevo → server-primero + firma).

## 5-BIS · CONSTRUCCIÓN (2026-07-20) ✅ + verificación E2E

**Construido (casi todo sitio + reuso del canal):**
- `lib/demo/for3sChat.ts`: cliente del canal general (`chatGeneral` con X-Client-Id=correo +
  `registrarByok` para `/v1/token`). Llega por el Funnel público `for3s.tail6749e5.ts.net`.
- `app/api/demo/general/chat/route.ts`: el correo sale de la SESIÓN (httpOnly), NUNCA del body
  (riesgo #1 cerrado). Guards: sin sesión→401, vacío→400, >4000→400.
- `apikey/route.ts`: al guardar la key (solo general) → `registrarByok` best-effort (BYOK).
- `ChatPanel.tsx` (impeccable, patrón de BrainPanel): historial + caja, sección "Chat" 1ª del
  shell. i18n es/en (`Demo.shell.chat` + `nav.chat`).
- Config: `FOR3S_GENERAL_API_KEY` + `FOR3S_GENERAL_BASE` en `.env.local`.

**🔎 Hallazgo de arquitectura (clave):** el Funnel público (`for3s.tail6749e5.ts.net`) apunta a
`127.0.0.1:8788` del host = el canal de **general** (la instancia pública), NO Foresito (interno,
en su namespace sin mapeo al host). Correcto: general recibe a los usuarios de la demo.

**Batería E2E (con la web real, no solo el canal):**
- ✅ **LA DEMO WEB CONVERSA CON FOR3S POR 1ª VEZ** (el "usarlo" de la visión): usuario A escribió
  "¿qué es For3s OS?" → respuesta real del agente.
- ✅ **Aislamiento multi-tenant probado:** A guardó "color favorito=verde limón" en su hilo; B
  preguntó por su color → "No lo sé, nunca me lo mencionaste". A sí lo recuerda ("Verde limón") →
  su hilo persiste. Cada correo su memoria, agente compartido.
- ✅ sin sesión→401 · build/lint verdes · canal general health ok, 0 errores (sin regresión).
- Limpieza: hilos borrados con `/v1/olvidar` (200) + registros de prueba fuera de `for3s_demo`.

## 5-TER · 🔴 BUG TRÁGICO CAZADO EN AUDITORÍA INTEGRAL (2026-07-20) — FIX

Al probar el flujo COMPLETO encadenado (Brian pidió "prueba todo el flujo, he reconocido
errores y patrones"), salió una **fuga de aislamiento entre usuarios** que pieza-por-pieza NO
se veía (solo aparece con correos REALES):

- **Causa:** el canal API sanea el `X-Client-Id` con `_limpiar_id` (borra `@ . +`, trunca a 32).
  Los correos reales colapsan: `a+b.test@x.com`, `ab.test@x.com`, `a.b.test@x.com` → TODOS
  `abtestxcom` → **MISMO hilo / memoria / vault de conectores** = un usuario ve el chat de otro
  y podría usar su token de GitHub. Gmail usa puntos y `+` constantemente → el bug es común.
- **Confirmado en vivo:** la BD del general tenía `client_id` ya destrozados (`auditorexamplecom`…).
- **Fix (`for3sChat.ts`, commit sitio `950b51b`):** `clientIdDeCorreo(email)` = `u` +
  sha256(correo normalizado)[:24] → id `[a-z0-9]` estable, único, <32 (intacto por `_limpiar_id`).
  Las 5 funciones lo aplican INTERNAMENTE (ningún caller lo olvida). El correo se normaliza
  (minúsculas+trim) → mismo correo, mismo id siempre.
- **E2E verificado:** 2 correos que colisionaban ahora AISLADOS (X guarda "AZUL-42", Y no lo ve,
  X lo recuerda). Conectores heredan el fix. Barrido: ningún otro lugar manda correo crudo como id
  (molde/NavigoX usan ids de máquina, intactos). Datos de prueba destrozados limpiados de la BD.

## 6 · Fuera de alcance de B
- Conectores OAuth (C) · API keys self-service f3k_ del usuario (D — distinto del BYOK de Claude) ·
  el correo admin ya lo hizo A · retirar contenedores demo vacíos (limpieza).

## 7 · Riesgos vigilados
- **No romper el aislamiento AI1:** el correo como X-Client-Id debe ser único y salir de la SESIÓN
  (no del body) — si se confía del body, un usuario podría suplantar el hilo de otro. FAIL-CLOSED.
- **La key BYOK en tránsito:** solo por el túnel tailnet interno, descifrada 1 vez, auditada.
- **Cortesía vs BYOK:** B-D2 es BYOK; el canal ya cae a cortesía si no hay key (no rompe), pero el
  cupo de cortesía es 1 solo para todos → vigilar que general no se apoye en él a escala.
- **La demo web corre en tailnet** (como vimos en E): el chat funciona con el sitio en la máquina
  de Brian / o el túnel expuesto. Confirmar la ruta pública del general para producción.

---

*Relacionado: `vision/Vision_Conectores_SelfService_Panel_Agente.md` (§B + §2-BIS) ·
`work/Plan_Pieza_A_Correo_Admin_Instancia.md` (identidad, ya lista) ·
`marca-personal/Mente/Doc/Demo_For3s_Avance.md` · memoria `project_conectores_selfservice`.*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Plan_Pieza_B_General_Multitenant.md`).
