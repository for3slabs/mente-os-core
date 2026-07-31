# 🔒 RONDA — SEC-4c: contenedor non-root con PERFIL por instancia (interna/expuesta)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_SEC4c_NonRoot_Perfil_Instancia.md → work/Ronda_SEC4c_NonRoot_Perfil_Instancia.md (2026-07-30, ADR-029)

> **Estado: ✅ COMPLETO 2026-07-16 (commits `c37ae1f`→`021292e` firmados, tríada `021292e`, CI verde).**
>
> **VEREDICTO FINAL:** las 5 instancias con su perfil correcto — Foresito/brian = interna (root),
> general/jazz/mashe = expuesta (non-root uid 1000). Verificado EN VIVO en non-root: KEK descifra
> ("cerebro conectado"), modelo BGE-M3 carga (dim 1024), backup escribe, execute_code, panel 200,
> /salud 0 FAIL, memoria OK, **host 100% intacto**. `/soy` muestra el perfil. pytest 249 (5 nuevos).
>
> **5 BUGS cazados probando en jazz primero (la red de seguridad funcionó):** (1) worker corría root
> (command arq no pasaba por el perfil → worker-entrypoint.sh); (2) backups en /root inaccesibles →
> /app/for3s-backups; (3) 🚨 **CATASTRÓFICO: `chown -R` sobre bind mounts cambió los permisos del
> HOST** (rompió ~/.for3s + backups de las 5 instancias) → reparado + rediseño uid=1000 (=host) SIN
> chown de bind mounts; (4) volúmenes docker con dueño viejo → chown quirúrgico solo de los internos;
> (5) el compose no pasaba FOR3S_PERFIL al contenedor (solo en .env) → brian quedaba non-root.
> **LECCIÓN LOCKED:** nunca `chown -R` un bind mount del host; el usuario del contenedor comparte uid
> con el host. `.trivyignore` DS002 actualizado con la justificación honesta del diseño nuevo.
> **Origen (Brian, 2026-07-16):** el Dockerfile.agent corre como root. Brian quiere blindar las
> instancias EXPUESTAS (non-root) pero conservar poder en las INTERNAS de la empresa
> (@For3s_OS_bot = Foresito, @For3s_Brian_bot = brian, "nunca serán expuestas"). Decisión de
> diseño (AskUserQuestion 2026-07-16): **PERFIL POR INSTANCIA** — cada instancia declara si es
> `interna` (root) o `expuesta` (non-root); seguro por defecto (`expuesta`).
> **Método:** `rules/ESTANDAR_Metodo_Fases_F.md`. **Regla madre:** explicar → aprobar → construir.

---

## 1 · La visión en palabras de Brian (el contrato)

- *"@For3s_OS_bot y @For3s_Brian_bot deben poder cambiar entre root y non-root, porque esos son
  los internos de la empresa, nunca van a ser expuestos."*
- Rebotado técnicamente (y aprobado): un comando NO puede cambiar el usuario EN CALIENTE (el
  usuario se fija al arrancar el contenedor; darle al proceso el poder de escalar = volverlo root
  de facto = pierde el blindaje). La intención SÍ se logra con **perfil por instancia**: internas
  arrancan root, expuestas arrancan non-root; el modo se cambia editando el `.env` + recreando.

## 2 · La matriz de perfiles (LOCKED con Brian)

| Instancia | Bot | Perfil | Usuario runtime | Por qué |
|---|---|---|---|---|
| Foresito | @For3s_OS_bot | `interna` | **root** | Interna de la empresa, nunca expuesta |
| brian | @For3s_Brian_bot | `interna` | **root** | Interna, personal de Brian |
| general | @For3s_General_bot | `expuesta` | **non-root** | Pública (puerta abierta) |
| jazz | @For3s_Jazzita_bot | `expuesta` | **non-root** | De tercero |
| mashe | @For3s_Mashe_bot | `expuesta` | **non-root** | De tercero |
| clientes futuros | — | `expuesta` (default) | **non-root** | Blindadas por defecto |

**Seguro por defecto:** sin `FOR3S_PERFIL` declarado → `expuesta` (non-root). Nunca se expone algo
como root por olvido. Solo las 2 internas declaran `FOR3S_PERFIL=interna` en su `.env`.

## 3 · El terreno REAL (investigado 2026-07-16 — lo que hace esto delicado)

| Elemento | Dónde vive hoy (root) | El riesgo al cambiar de usuario |
|---|---|---|
| **master.key (KEK)** | `secret_store.py:17` la busca en **`Path.home()/.for3s/master.key`** | ⚠️ **EL RIESGO #1.** `Path.home()` = `/root` para root, `/home/for3s` para non-root → cambiaría de sitio → **el bot NO descifra los tokens = bot muerto** |
| **Volumen KEK** | monta a `/root/.for3s` (3 servicios: agent, worker, admin) | non-root no puede leer ahí sin `chown` |
| **Modelo BGE-M3** | `Dockerfile:46` en `/root/.cache/huggingface`; HF usa `Path.home()/.cache` | non-root buscaría en `/home/for3s/.cache` → **modelo no carga = sin memoria semántica** |
| **Backups** | volumen a `/root/for3s-backups`; `backup.py` corre pg_dump | non-root no escribe ahí sin chown |
| **/app/mods, /app/persona** | volúmenes (auto-mod + capa usuario) | non-root necesita ser dueño para escribir |
| **/app/factory, /app** | horneado root en el build | el entrypoint (cp) necesita permiso de escritura en el core |

**Consumidores que NO se pueden romper:** los 3 servicios (agent, worker, admin) comparten imagen y
montan la KEK. El worker corre pg_dump (backups). El admin (solo general) sirve el panel. Las 5
instancias usan la MISMA imagen `for3s-agent:local` + el mismo `docker-compose.instancia.yml`
(Foresito usa `docker-compose.yml`, casi idéntico).

**Ya existe** (reuso, no reinventar): el patrón `FOR3S_SOLO_CONSOLA` (el entrypoint ya bifurca por
ENV) · el guardián que ya hace `cp`/`mkdir` en el arranque · `for3s-ctl` (control de instancias por
el host, por si luego se quiere un `for3s modo`).

## 4 · La solución técnica (cómo se logra sin romper la KEK)

**Clave del diseño: NO cambiar dónde vive nada. Cambiar QUIÉN es dueño, solo si `expuesta`.**

1. **Build (Dockerfile, como root — sin límite):** crear usuario `for3s` (uid fijo, ej. 10001) +
   instalar `gosu` (baja privilegios de forma segura, es el estándar). La imagen **sigue arrancando
   como root** (el CMD/entrypoint arranca root); el entrypoint decide bajar o no. Así una imagen
   sirve a AMBOS perfiles.
2. **Fijar HF_HOME por ENV** a una ruta estable (`/app/.cache/huggingface`) y COPIAR el modelo ahí
   (no a `/root/.cache`) → deja de depender de `Path.home()`. Vale para root Y non-root.
3. **Fijar la ruta de la KEK por ENV** (`FOR3S_STATE_HOME=/app/.for3s`, ya montado) en vez de
   `Path.home()/.for3s` → `secret_store.py` lee de ahí. Deja de depender del usuario. (El volumen
   `/app/.for3s` ya existe en TODOS los composes — línea 85/120.) ⭐ Esto **mata el riesgo #1**: la
   KEK ya no se mueve al cambiar de usuario.
4. **Entrypoint (F2):** al arrancar (como root), leer `FOR3S_PERFIL`:
   - `interna` → seguir como root (comportamiento actual, cero cambio).
   - `expuesta` → `chown -R for3s` de las carpetas del bot (`/app`, `/app/.for3s`, `/app/.cache`,
     backups) y **`exec gosu for3s`** el resto del arranque → el bot corre non-root, dueño de lo suyo.
5. **/soy (F4):** mostrar el perfil + usuario ("perfil: interna · root" / "expuesta · non-root") —
   transparencia (Brian sabe en qué modo corre cada bot).

**Por qué es seguro Y cumple la intención de Brian:**
- Expuestas: non-root → un exploit no escala (pasa Trivy). Sin puerta de escalada.
- Internas: root cuando lo necesiten, bajo control de Brian (nunca las ve un cliente).
- Instalar libs de trabajo en caliente → ya va al **sandbox aislado** (otro contenedor). El agente
  non-root no necesita instalar nada en runtime (sus libs vienen horneadas en el build = root).

## 5 · FASES (cada una: qué construye + cómo se verifica)

- **F1 · Dockerfile: usuario + gosu + rutas por ENV (build).**
  Añadir: `useradd for3s` (uid 10001) · `apt-get install gosu` · `ENV HF_HOME=/app/.cache/huggingface`
  + COPY del modelo ahí · `ENV FOR3S_STATE_HOME=/app/.for3s` · preparar dirs con permisos. La imagen
  sigue arrancando root. **Verifica:** rebuild OK · el modelo carga desde la ruta nueva (root) ·
  arranque normal de una instancia INTERNA sin cambios (regresión: root sigue igual).
- **F2 · secret_store + embeddings: leer la ruta por ENV (no Path.home()).**
  `secret_store.py`: master_key_path por `FOR3S_STATE_HOME` (fallback a `Path.home()/.for3s` =
  compat). Defensivo. **Verifica:** la KEK descifra los tokens en root (sin cambio) + test unitario.
- **F3 · entrypoint: bifurcación por perfil + gosu.**
  Leer `FOR3S_PERFIL` (default `expuesta`); si `expuesta` → chown + `exec gosu for3s "$0" "$@"`
  (re-ejecuta el guardián ya como for3s). **PROBAR EN jazz** (expuesta, apagada, bajo riesgo).
- **F4 · VERIFICACIÓN CRÍTICA en jazz (la red de seguridad):** con jazz en modo `expuesta` non-root,
  verificación AFIRMATIVA de:
  1. ⭐ **la KEK descifra los tokens** (el bot arranca y conecta a Claude/GitHub) — el riesgo #1.
  2. el modelo BGE-M3 carga (embeddings vivos, dim 1024).
  3. backups: pg_dump escribe (worker).
  4. auto-modificación: escribe/lee `/app/mods` (el guardián aplica overlays).
  5. `/salud` 0 FAIL · migraciones aplican · arranque sano.
  6. el proceso corre como `for3s` (no root): `docker exec … whoami` = for3s.
  Si CUALQUIERA falla → NO se propaga; se arregla en jazz primero.
- **F5 · /soy muestra el perfil + propagar a las 5.**
  general/jazz/mashe → `FOR3S_PERFIL=expuesta` (non-root). Foresito/brian → `FOR3S_PERFIL=interna`
  (root, sin cambio de comportamiento). Recrear cada una + verificar arranque + /salud.
- **F6 · CIERRE:** batería §5-BIS del sistema completo · commit firmado · tríada · CI verde (Trivy
  ya no marca el misconfig de root en las expuestas) · version bump si aplica · Bitácora + memoria.

⚠️ **Nota de alcance:** F3/F4 son el corazón del riesgo (la KEK). Se prueban en jazz (desechable)
antes de tocar las que Brian usa. Server-primero en todo.

## 6 · Decisiones abiertas (Brian confirma en la aprobación)

1. **¿Apruebas el plan F1→F6 y la matriz de perfiles §2?**
2. **¿Probamos en jazz primero** (recomendado: apagada, de tercero, bajo riesgo) o en otra?
3. **¿uid del usuario `for3s`** = 10001 (o alguno que Brian prefiera para alinear con el host)?
4. Opcional futuro (NO ahora): un `for3s modo <inst> interna|expuesta` que edite el `.env` + recree
   en un paso (hoy se hace a mano editando el `.env`). Se anota como mejora si Brian lo quiere.

## 7 · Criterio de éxito

Las 3 expuestas (general/jazz/mashe) corren **non-root**, blindadas, con **la KEK descifrando, el
modelo cargando, backups y auto-mod funcionando** (verificado, no asumido). Las 2 internas
(Foresito/brian) siguen root sin cambio. Trivy deja de marcar el misconfig en las expuestas. Cero
regresión. Brian puede ver el modo de cada bot con `/soy`.

---

Relacionado: `rules/ESTANDAR_Metodo_Fases_F.md` · `project_ci_verde_seguridad` (SEC-4c salió de ahí)
· `project_multi_instancia` (el gestor `for3s` + los perfiles) · `reference_servidor_for3s` ·
[[feedback_explicar_antes_de_implementar]] · [[feedback_flujo_server_primero]].
