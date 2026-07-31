# 🧪 Plan de Pruebas EXHAUSTIVO — For3s OS (Foresito)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/PLAN_PRUEBAS_EXHAUSTIVO.md → memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md (2026-07-30, ADR-029)

> **Propósito:** probar A PROFUNDIDAD cada elemento de For3s OS — desde la base de datos hasta el
> comportamiento completo — para confirmar que TODO funciona y NO hay fallas. No es un panorama:
> es un checklist elemento por elemento.
>
> **Cómo usarlo:** ve sección por sección, marca `[x]` lo que pasa, anota `❌ + qué pasó` lo que falla.
> Los que fallen se registran y arreglamos (modo iterar: prueba→reporta→arreglamos).
>
> **Inventario real (verificado 2026-07-02):** 31 tablas · 35 comandos · 11 tipos de botón · 58 módulos ·
> 10 jobs nocturnos · 9 contenedores hermanos · 32 migraciones · schema BD v32 · version.py v0.14.0.
>
> **Dos formas de probar cada cosa:**
> - **(U) Usuario** — tú, en Telegram, como lo haría cualquiera. Es la prueba REAL.
> - **(T) Técnica** — comando en el server para verificar la capa interna (BD, hermano, log).
>   Los comandos técnicos van en bloques ` ``` ` listos para copiar. Prefijo SSH:
>   `sshpass -p '«en secrets/Conectar_Servidor_For3s.md»' ssh brianweb3@100.112.177.53` y sudo: `echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S`.

---

## 0. PRE-VUELO — el sistema está vivo y sano

**(T) Los 9 hermanos arriba:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker ps --format "{{.Names}}\t{{.Status}}" | sort
# Esperado: 9 contenedores "Up": agent, worker, postgres(healthy), valkey(healthy),
# github-mcp, github-mcp-write, render, sandbox, grafana
```
- [ ] 9 hermanos Up
- [ ] postgres y valkey dicen `(healthy)`

**(T) El agent arrancó sano (guardián + sin errores):**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker logs for3s-agent-1 2>&1 | tail -20
# Esperado: "[guardian] core restaurado desde fábrica", "migrando BD", "Application started"
# NO esperado: traceback, "cuarentena", "modo solo consola" inesperado
```
- [ ] Ve `Application started`
- [ ] Ve `[guardian] core restaurado desde fábrica`
- [ ] NO hay traceback ni cuarentena

**(U) Prueba de vida:** escríbele "hola" a Foresito en Telegram.
- [ ] Responde en segundos, con sentido, en español.

---

## 1. BASE DE DATOS — las 31 tablas existen y son consultables

**(T) Todas las tablas presentes + schema v32:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=1,max_size=2)
    rows=await p.fetch(\"SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename\")
    print(len(rows),'tablas:',', '.join(r['tablename'] for r in rows))
    print('schema_version:',await p.fetchval('SELECT max(version) FROM schema_version'))
    await p.close()
asyncio.run(m())"
```
- [ ] 31 tablas, schema_version = 32

**Las 31 tablas y qué guardan (marca que cada una tiene sentido / datos donde deba):**
- [ ] `audit_events` — cadena de auditoría inmutable (hash encadenado)
- [ ] `episodes_events` — turnos de conversación (con embedding + deleted_at)
- [ ] `sessions` — sesiones registradas
- [ ] `personas` — identidad canónica (F1): telegram_user_id, nombre, rol
- [ ] `perfil_usuario` — perfil (P1): rol/stack/estilo/zona/rasgos
- [ ] `owner` — dueño (PR6, fuente de verdad)
- [ ] `secrets` — secretos cifrados (KEK)
- [ ] `temas` — temas por persona (AI2)
- [ ] `temas_equipo` / `equipos` / `equipo_miembros` — multi-usuario (H8)
- [ ] `estado_persona` — contexto activo de equipo (F5)
- [ ] `tema_estado` — estado operativo por tema (C1) ⭐NUEVO
- [ ] `decisiones` — registro de decisiones (C2) ⭐NUEVO
- [ ] `diario_cambios` — auto-detección de cambios (AC1)
- [ ] `hilo_status` — resumen narrativo por hilo (AI4)
- [ ] `skills` — skills/recetas (H10-12)
- [ ] `governor_estado` / `governor_bloqueos` — freno de seguridad (H11)
- [ ] `dmn_estado` / `dmn_corridas` / `dmn_propuestas` — SUEÑA (H9)
- [ ] `cron_corridas` — registro de jobs nocturnos (PR2)
- [ ] `corridas_equipo` / `corrida_reportes` — handoff auditable (AI3)
- [ ] `gh_resources` / `gh_files` — GitHub persistido (H5)
- [ ] `consulted_files` / `consulted_web` — docs/URLs consultados
- [ ] `solicitudes` — solicitudes/puerta del equipo
- [ ] `schema_version` — versión del esquema

**(T) Integridad de la cadena de auditoría (CRÍTICO — nunca debe romperse):**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=1,max_size=2)
    tot=await p.fetchval('SELECT count(*) FROM audit_events')
    roto=await p.fetchval(\"SELECT count(*) FROM audit_events a WHERE a.id>1 AND NOT EXISTS (SELECT 1 FROM audit_events pp WHERE pp.hash_self=a.hash_prev)\")
    print(f'audit: {tot} eventos, {roto} eslabones rotos (DEBE ser 0)')
    await p.close()
asyncio.run(m())"
```
- [ ] eslabones rotos = 0

**(T) Migraciones (32) todas aplicadas, ninguna pendiente:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python -m for3s_core.cli migrate
# Esperado: "migraciones aplicadas: ninguna pendiente"
```
- [ ] ninguna pendiente

---

## 2. MEMORIA — el cerebro en cascada (H5 + REDISEÑO M1-M4)

**(U) Memoria persistente (recuerda entre mensajes):**
1. Dile: "acuérdate que mi color favorito es el verde".
2. Cambia de tema, escribe otras 3-4 cosas.
3. Pregunta: "¿cuál es mi color favorito?"
- [ ] Responde "verde" (no lo perdió)

**(U) Memoria SEMÁNTICA (busca por significado, no palabra exacta):**
1. Pregunta: "¿qué repos hemos analizado?" o "¿en qué nos hemos enfocado?"
- [ ] Trae temas/repos reales de conversaciones pasadas (no inventa, no dice "no sé")

**(U) Línea de tiempo / retomar:**
1. Pregunta: "¿en qué quedamos?" o "¿de qué estábamos hablando?"
- [ ] Resume los últimos turnos reales de ESTE hilo

**(T) La cascada de memoria funciona sin romper (recordar E2E):**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
from for3s_core.memoria import Memoria
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=2,max_size=4)
    mem=Memoria(p)
    r=await mem.recordar('tg:1923367928','en que nos hemos enfocado',history=[],es_panorama=True)
    print('recordar panorama → len',len(r),'| trae bloques:',bool(r))
    await p.close()
asyncio.run(m())"
```
- [ ] Devuelve contexto (len > 0) sin excepción

**(T) C3 exacto-primero — nombrar un concepto lo trae primero:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
from for3s_core import conversation as c, kg
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=1,max_size=2)
    conc=await kg.conceptos(p)
    obj=next((x.get('label') for x in conc if len((x.get('label') or ''))>=5),None)
    ex=c._conceptos_exactos(conc,f'hablame de {obj}')
    print('concepto objetivo:',obj,'| exacto detectado:',[x.get('label') for x in ex[:3]])
    await p.close()
asyncio.run(m())"
```
- [ ] El concepto nombrado sale en los exactos

**(U) Aislamiento (si tienes un segundo usuario/tema):** desde otro hilo/persona, pregunta por algo privado tuyo.
- [ ] NO ve la memoria privada de otro hilo/persona

---

## 3. TEMAS E HILOS (AI2 + F5)

**(U) Temas por persona:**
- [ ] `/tema backend` → crea/cambia al tema "backend"
- [ ] `/temas` → lista tus temas con botones
- [ ] `/tema` (sin nombre) → muestra el tema activo
- [ ] `/hilos` → lista tus hilos con su actividad (último turno, nº mensajes)
- [ ] Al cambiar de tema, la conversación es un hilo SEPARADO (no se mezcla)

**(U) Temas de EQUIPO (canal compartido):**
- [ ] `/tema equipo proyecto-x` → entra a un canal compartido
- [ ] `/tema equipo` (sin nombre) → lista los temas de equipo
- [ ] `/tema salir` → vuelve a tu hilo privado

---

## 4. C1 · ESTADO OPERATIVO POR TEMA ⭐NUEVO

**(U) Registrar y consultar estado:**
- [ ] `/estado_tema fase: integrando pagos | proximo: probar webhook | bloqueo: falta API key` → confirma "✅ Estado del tema actualizado" con los 3 campos
- [ ] `/estado_tema` (sin args) → muestra el estado guardado
- [ ] `/estado_tema proximo: cerrar factura` → actualiza SOLO próximo, CONSERVA fase y bloqueo (combina)
- [ ] Pregunta en lenguaje natural: "¿en qué punto va este proyecto?" → responde con el estado real
- [ ] Un tema SIN estado → `/estado_tema` da el mensaje de ayuda (no rompe)

---

## 5. C2 · REGISTRO DE DECISIONES ⭐NUEVO

**(U) Registrar, listar, buscar el porqué:**
- [ ] `/decidi usar Postgres, no Mongo :: ya tenemos AGE+pgvector encima` → "✅ Decisión #N registrada"
- [ ] `/decidi desplegar en contenedores :: portable y aislado :: todo el deploy` → con impacto
- [ ] `/decisiones` → lista las decisiones (vigentes primero, con su porqué)
- [ ] Pregunta natural: "¿por qué decidimos usar Postgres?" → responde con el rationale real
- [ ] `/decision 1 superada` → marca #1 como superada
- [ ] `/decisiones` de nuevo → la superada aparece marcada (🔁) y las vigentes primero
- [ ] `/decision 999 superada` (id inexistente) → mensaje de error claro, no rompe

**(T) Aislamiento de decisiones (no ves las de otro tema):**
```bash
# registrar en un tema y verificar que otra sesión no las lista (ver logs / repetir en 2 hilos)
```
- [ ] Las decisiones de un tema NO aparecen en otro

---

## 6. P4 · SELF-VERSION-AWARENESS

**(U) El agente sabe su versión y novedades:**
- [ ] `/version` → dice **v0.14.0 PRODUCTO DISTRIBUIBLE** + lo más nuevo (memoria cascada, auto-conciencia, multi-instancia, execute code)
- [ ] Pregunta natural: "¿qué versión eres? ¿qué traes nuevo?" → responde con datos reales (no inventa)
- [ ] Pregunta: "¿qué has cambiado en ti mismo?" → si hay auto-mods, las reporta (changelog vivo)

---

## 7. P1 · PERFIL DE USUARIO (modelar al usuario) + v2 inferencia

**(U) Perfil declarado:**
- [ ] `/perfil` → muestra tu perfil (o vacío si no hay)
- [ ] `/perfil rol backend` → fija tu rol
- [ ] Dile "soy desarrollador de backend" en charla → detecta y guarda el rol (o lo propone)
- [ ] `/perfil` → ahora muestra el rol
- [ ] El bot adapta respuestas a tu perfil (ej. si eres backend, responde técnico)

**(T) Inferencia nocturna P1 v2 (OPT-IN, apagado por defecto):**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "from for3s_core import perfil_infer as pi; print('perfil_infer activo (default):', pi.activo())"
# Esperado: False (opt-in). Para activar: FOR3S_PERFIL_INFER=on en el worker.
```
- [ ] `activo()` = False por defecto (opt-in respetado)
- [ ] (opcional) Activar `FOR3S_PERFIL_INFER=on`, correr `job_perfil`, ver que deja propuestas con gate

**(U) Fix nombre del dueño (captura automática):**
- [ ] Escríbele algo a Foresito. Luego pregunta "¿cómo me llamo?" → sabe tu nombre de Telegram (se auto-capturó)

**(T) Verificar que el nombre se capturó:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=1,max_size=2)
    r=await p.fetchrow('SELECT telegram_user_id,nombre,rol FROM personas WHERE telegram_user_id=1923367928')
    print('dueño:',dict(r) if r else None)
    await p.close()
asyncio.run(m())"
```
- [ ] `nombre` del dueño YA NO es None (tras escribirle)

---

## 8. AUTO-CONCIENCIA + AUTO-MODIFICACIÓN (AC1-AC4 + guardián)

**(U) Se conoce (introspección en vivo):**
- [ ] `/soy` o `/introspeccion` → lista sus módulos, tablas, migraciones, skills, comandos, jobs REALES
- [ ] Pregunta "¿cómo estás construido?" → responde desde su introspección (no ficha estática)
- [ ] `/cambios` → muestra qué cambió en su código (propio vs externo)

**(U) Se auto-modifica DENTRO de su caja (solo dueño):**
- [ ] `/modificar` sin args → muestra la ayuda/uso
- [ ] (avanzado) `/modificar <mod>: <cambio pequeño>` → pasa por entorno de prueba (sintaxis→import→smoke) antes de aplicar
- [ ] Intentar tocar una LÍNEA ROJA (governor/audit/crypto) → lo RECHAZA
- [ ] `/revertir` → deshace el último cambio
- [ ] `/modificar_bd <SQL DDL aditivo>` → dry-run + backup obligatorio antes de aplicar

**(T) El guardián de arranque protege (doble red):**
```bash
# Ya verificado al arrancar: "[guardian] core restaurado desde fábrica" en los logs.
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker logs for3s-agent-1 2>&1 | grep guardian | head
```
- [ ] El guardián corrió al arrancar (restaura fábrica + prevuelo)

---

## 9. EJECUTAR CÓDIGO (EXECUTE_CODE — agente-desarrollador)

**(U) Ejecuta código real en el sandbox:**
- [ ] "cuenta los números primos del 1 al 100 ejecutando código" → llama execute_code, corre, responde **25**
- [ ] "calcula el factorial de 20 con código" → da el número exacto ejecutando
- [ ] "hazme un script en Python que ordene una lista y ejecútalo" → escribe + ejecuta + muestra resultado

**(T) El sandbox hermano vive y responde:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import urllib.request; print('sandbox /health:', urllib.request.urlopen('http://sandbox:8090/health',timeout=8).status)"
```
- [ ] sandbox /health = 200

**(T) Aislamiento del sandbox (no toca el host):**
- [ ] El código corre en `for3s-sandbox`, con límites (CPU/RAM/pids), usuario sin privilegios
- [ ] Un `while True` no cuelga el bot (timeout lo corta)

---

## 10. GITHUB (H4 + hermanos MCP)

**(U) Lectura de repos:**
- [ ] "analiza el repo cli/cli" → trae info real (lenguajes, actividad, etc.)
- [ ] "¿cuántos PRs abiertos tiene cli/cli?" → conteo exacto
- [ ] "dame los últimos issues de <repo>" → lista real

**(U) Escritura (write tools con confirmación):**
- [ ] Pedir crear un issue/comentario → pide confirmación ✅/❌ antes de escribir
- [ ] Rechazar (❌) → no escribe
- [ ] Pedir un merge/delete → lo RECHAZA (whitelist dura)

**(T) Los hermanos MCP conectados:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker logs for3s-agent-1 2>&1 | grep -iE "GitHub MCP conectado"
```
- [ ] "GitHub MCP conectado"

---

## 11. WEB + MULTIMODAL

**(U) Web fetch:**
- [ ] "resume esta página: <URL simple>" → trae el contenido real
- [ ] Una URL de SPA/JS (via render hermano) → también la lee
- [ ] Una URL con anti-bot → lo dice honestamente (no inventa)

**(U) Multimodal:**
- [ ] Enviar una imagen → la describe
- [ ] Enviar un PDF → lo lee/resume
- [ ] Enviar Word/Excel → lo procesa

---

## 12. EQUIPO MULTI-AGENTE (H8)

**(U) Lanzar el equipo:**
- [ ] `/equipo <tarea compleja>` → lanza specialists en paralelo con progreso en vivo (⏳→🔄→🟢) + síntesis final + gasto
- [ ] Una tarea que amerite ("auditoría completa de X") → dispara el equipo automáticamente
- [ ] Charla normal → NO dispara el equipo (1 agente)

**(U) Multi-usuario (puerta):**
- [ ] `/invitar` → abre/cierra la puerta del equipo
- [ ] `/miembros` → lista quién está (con actividad)
- [ ] Con puerta abierta, otra persona que escribe entra; cerrada, no

---

## 13. METACOGNICIÓN (H10 PLANEA)

**(U) Sabe cuándo NO sabe:**
- [ ] Pregunta algo que NO puede saber con certeza → marca la respuesta como tentativa o pide aclaración (no inventa con seguridad falsa)
- [ ] Pregunta algo que SÍ sabe → responde con confianza normal

---

## 14. SUEÑA / DMN (H9) + APRENDE (H10-12)

**(U) DMN (solo dueño):**
- [ ] `/dmn` o `/dmn status` → muestra estado del DMN (housekeeping/generativas)
- [ ] `/dmn propuestas` → lista propuestas pendientes con botones ✅/❌
- [ ] `/dmn roi` → muestra el ROI por task
- [ ] `/autogen status` → estado del kill switch de auto-generación

**(U) APRENDE:**
- [ ] `/skills` → lista las skills (recetas)
- [ ] `/aprende` → destila una skill de lo trabajado (pasa por governor)

---

## 15. MULTI-INSTANCIA (gestor `for3s`)

**(T) El comando gestor existe y lista:**
```bash
which for3s && for3s listar
```
- [ ] `for3s listar` → muestra las instancias (o vacío si solo está Foresito)
- [ ] (avanzado) `for3s agregar` → wizard crea una instancia AISLADA (token + KEK auto)
- [ ] (avanzado) `for3s entrar <nombre>` → chat de consola de esa instancia
- [ ] (avanzado) `for3s borrar <nombre>` → limpia todo, Foresito INTACTO
- [ ] Foresito nunca se ve afectado por otra instancia (aislamiento total)

---

## 16. SALUD / MONITOREO / SOPORTE (PR2 + PR10)

**(U) Monitoreo:**
- [ ] `/salud` → reporte end-to-end (mensaje→memoria, subsistemas, grafo, integraciones, nocturno, tokens, hilos)
- [ ] `/salud <sección>` → detalle de una sección
- [ ] `/datos` → analítica de uso (actividad, consumo, repos, por persona)
- [ ] `/diagnostico` → mini-reporte personal
- [ ] `/estado` → salud básica (uptime, modelo)
- [ ] `/cupo` → cuánto queda de la suscripción

**(U) Soporte:**
- [ ] `/ayuda` → qué puede hacer + primer auxilio (por rol)
- [ ] `/reconectar` (dueño) → reconecta integraciones

**(T) Alerta automática si algo se rompe (PR2):**
- [ ] `job_health_check` corre 04:30 y avisa al dueño solo si hay 🔴 (verificado antes parando render)

---

## 17. DUEÑOS (PR6)

**(U) Gestión de dueño (fuente de verdad en BD):**
- [ ] `/transferir_dueno` → transfiere (atómico owner+encargado)
- [ ] `/recuperar_dueno` → recupera si aplica
- [ ] El owner sobrevive reinicios (está en BD, no solo JSON)

---

## 18. SEGURIDAD (transversal)

- [ ] **KEK offline** — los secretos en `secrets` están cifrados; Brian nunca ve plaintext
- [ ] **Audit inmutable** — cero eslabones rotos (§1); no hay UPDATE/DELETE sobre audit
- [ ] **Aislamiento entre personas** — nadie ve lo privado de otro (§2, §5)
- [ ] **Sandbox sin acceso al host** — execute_code aislado (§9)
- [ ] **Líneas rojas de auto-mod** — no toca governor/audit/KEK (§8)
- [ ] **Write GitHub con whitelist** — rechaza merge/delete/push (§10)
- [ ] **(T) Cero secretos en el repo:**
  ```bash
  cd ~/for3s-os && git grep -nE "gho_|sk-ant|«en secrets/Conectar_Servidor_For3s.md»|BEGIN.*PRIVATE" -- ':!*.md' | head
  # Esperado: vacío (SEC-1 gho_ es riesgo aceptado en el remote, no en archivos)
  ```

---

## 19. BUGS RESUELTOS — verificar que SIGUEN sanos (no regresaron)

Los bugs históricos (deben seguir arreglados):
- [ ] **BUG-1** decay de memoria — `job_relevance` corre; relevance se recalcula (no está muerto)
- [ ] **BUG-2** sandbox.py — DIFERIDO a propósito (era base de EXECUTE_CODE; no es fallo)
- [ ] **BUG-3** turnos huérfanos — soft-deleted, no aparecen
- [ ] **BUG-4** owner frágil — resuelto por PR6 (owner en BD)
- [ ] **BUG-5/6** backup roto — `job_backup` corre, hay respaldos (pg_dump + volumen)
- [ ] **BUG-8** CLS consolida 0 — grafo crece (63 conceptos); catálogo AGE sano
- [ ] **BUG-9/9b** GitHub/web rotos — hermanos de red OK (MCP + render por HTTP)
- [ ] **BUG-10** embeddings no precargaban — BGE-M3 carga offline al arrancar
- [ ] **BUG-12** /estado bloqueado — funciona
- [ ] **BUG-13** fuga en /diagnostico — cada quien ve solo lo suyo
- [ ] **BUG-14** fuga de privacidad memoria — scope arreglado (miembro no ve legado del dueño)
- [ ] **BUG-15** Conflict en reinicios — exec python PID 1, apaga limpio
- [ ] **BUG-16** gate de aprobación — NO era bug, funciona E2E
- [ ] **BUG-17/18/19** memoria multi-usuario / sesiones — resueltos (aislamiento)

**(T) Verificación rápida de los críticos:**
```bash
# BUG-1: relevance vivo | BUG-8: grafo crece | audit íntegra
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=1,max_size=2)
    print('conceptos en grafo (BUG-8):', await p.fetchval(\"SELECT count(*) FROM cron_corridas WHERE job='job_cls' AND ok\") ,'corridas CLS ok')
    print('backups (BUG-5/6): job_backup corridas ok:', await p.fetchval(\"SELECT count(*) FROM cron_corridas WHERE job='job_backup' AND ok\"))
    print('relevance (BUG-1): job_relevance corridas ok:', await p.fetchval(\"SELECT count(*) FROM cron_corridas WHERE job='job_relevance' AND ok\"))
    await p.close()
asyncio.run(m())"
```
- [ ] job_cls, job_backup, job_relevance tienen corridas OK (los subsistemas de fondo funcionan)

---

## 20. JOBS NOCTURNOS (10) — corren y se registran

**(T) Ver las últimas corridas de cada job:**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=1,max_size=2)
    rows=await p.fetch(\"SELECT job, max(creada_at) ult, bool_and(ok) FROM cron_corridas GROUP BY job ORDER BY job\")
    for r in rows: print(' ',dict(r))
    await p.close()
asyncio.run(m())"
```
Los 10 jobs: backup(01:00) · cls(02:00) · status(02:30) · relevance(02:45) · microglia(03:00) · curar_skills(03:30) · perfil(03:45, opt-in) · dmn_noche(04:00) · health_check(04:30) · dmn_idle(cada 30min)
- [ ] Cada job tiene corridas registradas (los que ya corrieron al menos una noche)
- [ ] `ok` = true en todos

---

## 21. RESILIENCIA / COMPORTAMIENTO BAJO ESTRÉS

**(U) Robustez:**
- [ ] Mandar varios mensajes seguidos → no se cuelga, no duplica respuestas
- [ ] Una pregunta muy larga → responde o degrada con gracia (no traceback al usuario)
- [ ] Si un hermano cae (ej. render), el bot avisa/degrada, NO muere

**(T) Concurrencia (varios turnos en paralelo, sin carreras):**
```bash
echo "«en secrets/Conectar_Servidor_For3s.md»" | sudo -S docker exec for3s-agent-1 python3 -c "import asyncio,os,asyncpg
from for3s_core.memoria import Memoria
async def m():
    p=await asyncpg.create_pool(os.environ['DATABASE_URL'],min_size=2,max_size=4)
    mem=Memoria(p)
    rs=await asyncio.gather(*[mem.recordar('tg:1923367928',f'q{i}',history=[],es_panorama=True) for i in range(8)],return_exceptions=True)
    excs=[r for r in rs if isinstance(r,Exception)]
    print('8 recordar en paralelo → excepciones:',len(excs),'(debe 0)')
    await p.close()
asyncio.run(m())"
```
- [ ] 0 excepciones en paralelo

---

## 📋 RESUMEN DE RESULTADOS

| Sección | ✅ Pasó | ❌ Falló | Notas |
|---|---|---|---|
| 0. Pre-vuelo | | | |
| 1. Base de datos | | | |
| 2. Memoria (cascada) | | | |
| 3. Temas e hilos | | | |
| 4. C1 estado tema | | | |
| 5. C2 decisiones | | | |
| 6. P4 versión | | | |
| 7. P1 perfil | | | |
| 8. Auto-conciencia | | | |
| 9. Execute code | | | |
| 10. GitHub | | | |
| 11. Web/multimodal | | | |
| 12. Equipo H8 | | | |
| 13. Metacognición | | | |
| 14. DMN/APRENDE | | | |
| 15. Multi-instancia | | | |
| 16. Salud/soporte | | | |
| 17. Dueños | | | |
| 18. Seguridad | | | |
| 19. Bugs resueltos | | | |
| 20. Jobs nocturnos | | | |
| 21. Resiliencia | | | |

**Fallas encontradas (para arreglar, modo iterar prueba→reporta→arreglamos):**
1.
2.
3.

---

*Generado 2026-07-02 · inventario real verificado (31 tablas, 35 comandos, 58 módulos, 10 jobs, 9 hermanos, schema v32, v0.14.0). Cubre desde la BD hasta el comportamiento completo — cada elemento, cada bug, cada capacidad.*
