# 🔌 VISIÓN — Conectores self-service: el panel y el agente POR FIN se hablan

> **Origen (Brian, 2026-07-20):** *"el flujo de cómo conectábamos herramientas a For3s OS era a
> través de MÍ — que yo las implementara o incorporara. Eso es ineficiente y complicado. Vamos a
> mejorar: que los usuarios de la demo puedan picar CONECTAR y que su agente/rama entienda que ya
> tiene esas herramientas conectadas."* Este doc captura la VISIÓN — el diseño fino va en su
> Ronda F0 cuando Brian diga "arranca". Es un pendiente GRANDE (método de fases F).

---

## 0 · El problema de fondo

1. **Toda integración pasa por Brian.** Conectar una herramienta (GitHub, Drive, Canva…) a un
   For3s OS = pedírselo a Brian y que él la meta a mano. No escala, no es producto.
2. **El panel de la demo está muerto.** `for3s.vercel.app/demo` ya tiene shell + Perfil +
   Conectores (GitHub, Vercel, Adobe ×2, Canva, Drive, PC, Telegram) — pero es PURA UI:
   **cero comunicación panel ↔ agente**. El botón "Conectar" no conecta nada.
3. **El modelo a imitar existe:** el flujo OAuth de GitHub con Claude ("Authorize Claude" →
   un click → la app recibe el token y ya puede actuar). Ese es el estándar de UX que For3s
   debe dar: **un botón → el proveedor entrega la credencial → el agente la tiene**.

## 1 · La visión (las 3 piezas)

### A · Identidad ADMIN por instancia = un correo
Cada instancia tiene UN correo que es su admin:
| Instancia | Correo admin |
|---|---|
| brian | **brayan002150@gmail.com** ✅ (confirmado por Brian 2026-07-20) |
| Foresito | fruterito101@gmail.com |
| jazz | correo demo (Brian lo dará; configurar IGUAL que las otras) |
| mashe | correo demo (Brian lo dará; configurar IGUAL que las otras) |

### B · General = agente COMPARTIDO, todo lo demás POR USUARIO
Hoy quien entra a general ya genera su rama (hilos/scope por persona — doctrina AI1). Esa
lógica se ELEVA: cada usuario de general tiene **su propio correo de acceso** (el que puso al
entrar a la demo), **sus propias API keys** y **sus propios conectores**. Lo ÚNICO compartido
es el agente. General se vuelve de verdad multi-tenant por correo.

### C · Conectores que SÍ conectan (el corazón)
- Botón "Conectar" → **OAuth del proveedor** (patrón GitHub Authorize) → el token/credencial
  llega SOLO (sin pedírselo a Brian, sin pegar keys a mano donde el proveedor dé OAuth).
- La credencial se guarda **cifrada y ligada al usuario/rama/instancia** (reglas de siempre:
  Brian nunca ve plaintext, vault, audit).
- **El agente de esa instancia/rama SE ENTERA:** a partir de ese momento tiene la herramienta
  disponible (ej. GitHub → su MCP ya existe en For3s OS; Drive/Canva/etc. se irán sumando).
- El panel refleja el estado real (Conectado/No conectado) leyendo del agente, no de mentira.
- No están casi ninguna de las integraciones del panel: se cablea **conector por conector**
  (GitHub primero — MCP ya existe), avanzando.
- **La experiencia completa en 3 pasos (Brian, 2026-07-20):** *"1. registro nombre y correo ·
  2. conectar herramientas · 3. usarlo — en tres sencillos pasos queda todo, y TODO del lado
  del usuario."* La persona conecta y dice "ya quedó, ya tengo integrada esta herramienta".
- **Quitar también es del usuario:** desconectar un conector = igual de fácil que conectarlo
  (un botón; la credencial se revoca/borra de su vault; el agente deja de tener la herramienta).

### D · API keys de For3s SELF-SERVICE (Brian, 2026-07-20)
Hoy las keys `f3k_` las genera Brian desde el panel admin (`/for3s-admin` → Clientes →
"+ Nuevo cliente"). La visión: **un apartado "Genera mi API key de For3s" en el panel del
USUARIO** — la misma mecánica del admin pero self-service:
- El usuario solo pone un **NOMBRE** para la key → se genera ligada a SU cuenta (su correo).
- **Tope: 3 API keys por persona.** (Y puede revocarlas él mismo, coherente con "quitar
  también es del usuario".)
- Reusa el motor que ya existe (api_clients: hash sha256, scopes, estado, cuotas — Frente B);
  lo nuevo es la puerta self-service ligada a la identidad por correo de la pieza B.

## 2 · Lo que YA existe para reusar (terreno leído 2026-07-20)

**Del lado sitio (`marca-personal`, doc `Mente/Doc/Demo_For3s_Avance.md`):**
- `/demo` real: registro nombre+correo normalizado, sesiones persistentes, capacidad 10+waitlist,
  demos 1:1 por token secreto (jazz/mashe/brian), shell con Perfil/Conectores.
- **API key de Claude por usuario ya cifrada** (AES-256-GCM server-side, `api_key_enc` +
  hint, nunca vuelve al navegador) → **el patrón exacto para guardar credenciales de conectores**.
- BD `for3s_demo` separada (Postgres nativo del server, vía Tailscale) + dashboard `/demo-admin`.
- 4 contenedores demo VACÍOS (`for3s-demo-{jazz,mashe,brian,general}`) esperando For3s.
- ⚠️ Cumplimiento: OAuth de suscripción de Claude PROHIBIDO por Anthropic para terceros —
  la vía legal es que el usuario pegue SU API key (ya implementado). Los OAuth de esta visión
  son de los PROVEEDORES (GitHub/Google/etc.), eso sí es estándar y legal.

**Del lado For3s OS:**
- Canal API por instancia + panel `/for3s-admin` (enciende/apaga instancias — captura de Brian).
- Puerta H8 (roles/fail-closed) + hilos por usuario en general (AI1) + molde For3s Inside
  (contrato+SDK) + secret store/vault (H-11 blindó el tubo) + MCP GitHub vivo + Maestro
  (ramas Mente OS por persona — cruza con la rama de cada usuario).

## 3 · Preguntas abiertas (para la Ronda F0)

1. ~~Correo de brian~~ → ✅ **brayan002150@gmail.com** (confirmado 2026-07-20).
2. Correos demo de jazz/mashe — Brian los dará.
3. ¿Los conectores viven en la BD de cada instancia (vault propio, aislamiento total) o en
   `for3s_demo` (cerca del panel)? — instinto: en la instancia (el agente es quien los usa),
   el panel solo consulta por el canal API.
4. OAuth apps propias: hay que REGISTRAR una app OAuth de For3s en cada proveedor (GitHub
   App/OAuth App, Google Cloud para Drive, etc.) con sus callbacks al sitio. ¿Cuenta/org dueña?
5. Relación contenedores demo vacíos ↔ instancias reales del server: ¿la demo habla con las
   instancias REALES vía canal API, o se les mete For3s a los 4 vacíos? (la visión de Brian
   apunta a instancias reales + general multi-tenant).
6. Orden de conectores: GitHub primero (MCP listo). ¿Luego? (Drive/Telegram parecen naturales).

## 4 · Estado

**🎯 VISIÓN CAPTURADA (2026-07-20) — NO diseñar ni construir hasta que Brian diga.** Arranca
con Ronda F0 (explicar → aprobar → construir). Registrado en `Doc/PENDIENTES.md`.

Relacionado: `marca-personal/Mente/Doc/Demo_For3s_Avance.md` (terreno del sitio, LEÍDO con
permiso de Brian 2026-07-20) · [[project_frente_b_puente_mercado]] (canal API producto) ·
[[project_molde_for3s_inside]] · [[project_multi_instancia]] · [[project_maestro_puentes_c_d]].
