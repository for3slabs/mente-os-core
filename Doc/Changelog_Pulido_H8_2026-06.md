# Changelog — Pulido H8 + Adopción a CÓDIGO PROPIO (2026-06-23/24)

> Fase de pulido de H8 (equipo multi-agente + multi-usuario). Brian declaró:
> "dejar H8 lo más perfecto, pulido, DISTRIBUIDO posible". Incluye la adopción de
> 7 aprendizajes (analizados de un sistema externo de referencia) traducidos a
> CÓDIGO PROPIO de For3s (Python + PostgreSQL), NO herramientas externas.
> ⚠️ El código NO contiene NINGUNA referencia a sistemas externos (ver §LIMPIEZA).

**Estado al cierre:** bot + worker activos · 132 tests · BD migraciones v16 ·
26 checks de integración pasando · For3s OS = desarrollo propio sin rastro externo.

---

## 1. Pulido H8 — área A (UX del equipo multi-agente)

- **Progreso EN VIVO** al lanzar el equipo: un mensaje que se edita mostrando cada
  specialist (⏳→🟢/🔴) conforme termina, en vez de ~100s de silencio.
- **Línea de gasto** al terminar: ⏱ tiempo · 🔢 tokens · 🔋 cupo.
- `multiagente.correr_equipo` acepta callback `on_progreso` (aditivo, defensivo).
- Verificado con fakes (5 eventos) + LLM real (5/5 specialists).

## 2. BUG CRÍTICO #6 — HILO POR USUARIO

**Problema:** todos compartían UNA sesión (`owner_session="brian"`) → al escribir,
el bot continuaba el hilo de OTRA persona. Lo destapó Brian probando con un 2º usuario.

**Fix:** migración 013 (columna `telegram_user_id` en episodes_events) + sesión por
persona derivada del user_id (`tg:<id>`; el dueño conserva `brian` = su historial).
`Conversation` y `record_turn` graban el autor de cada turno. En BD ahora se ve QUIÉN
escribió cada mensaje (#3). Se movieron los turnos de la 2ª persona de la sesión
`brian` a su propio hilo + limpieza del par contaminado (con backup).
Verificado en vivo: "en qué quedamos" ya retoma el hilo correcto, sin mezclar.

## 3. Adopción de 7 aprendizajes → CÓDIGO PROPIO (AI1-AI7)

> Analizados de un sistema externo de referencia (resuelve coordinación con
> markdown+scripts, 0 BD). For3s los reimplementó en CÓDIGO (Python+PostgreSQL),
> más robusto. NINGUNA dependencia ni referencia externa en el código.

### AI2 — Temas por persona (shared-thread inbox) ✅
- Un mismo chat de Telegram = varios hilos/temas separados. `/tema <nombre>`,
  `/temas` (botones), default `general` (opt-in). migración 014 (tabla `temas`).
- `session_id` = `tg:<uid>:<tema>` (general = sin sufijo → conserva historial).
- Cada tema = hilo separado; el conocimiento (grafo/CLS) se sigue compartiendo.

### AI1 — Doctrina de aislamiento ✅
- HALLAZGO: el filtro `scope_user_id` (S10c) EXISTÍA pero NO se aplicaba en el flujo.
- FIX: `Conversation` pasa `scope_user_id` a `buscar_semantico` (2ª capa sobre el
  session_id). `_scope_de(user)`: dueño→None (ve todo, compat legado NULL),
  miembro→su id (solo su privada + común, NUNCA lo de otro).
- + doctrina en la personalidad: 5 reglas (no asumir de otro hilo, no mezclar/
  continuar conversación ajena, lo compartido es el conocimiento no el chat crudo,
  ante duda preguntar, no inventar conexiones). Verificado con embeddings reales.

### AI3 (parte 1) — Audit trail del equipo (DB-backed) ✅
- migración 015 (`corridas_equipo` + `corrida_reportes`, texto completo por
  specialist, CASCADE). `handoff.py` registrar_corrida (transaccional, defensivo;
  separación de escritura: el coordinador escribe, los specialists no) +
  ultimas_corridas. Cada corrida del equipo queda auditada (antes se perdía en RAM).
- ⏳ Parte 2 (separación de escritura del gate) = cruza con apartado E, pendiente.

### AI4 — Auto-retomar (STATUS por hilo) ✅
- "RETOMAR.md automático" por conversación. migración 016 (`hilo_status`).
  `hilo_status.py`: genera STATUS curado por hilo (resume últimos turnos vía LLM
  OAuth-safe) + debe_inyectar (solo tras >3h inactividad) + hilos_activos.
- Inyección al contexto en `send()` al retomar. `job_status` nocturno (02:30, tras
  CLS, anti-429) en el worker. Verificado: "2/2 hilos resumidos", STATUS aislados.

### AI5 — Version-self-awareness ✅ (CIERRA P4 + G4)
- `version.py`: fuente única (VERSION + HITO + changelog estructurado H1→H8) +
  resumen(). Detector `_es_pregunta_version` + inyección + comando `/version`.
- El agente ya responde "¿qué versión eres? ¿qué hay nuevo?" con datos reales.

### AI6 — Disciplina de tamaño / tiered ✅ (CIERRA G5)
- `_formatear_recuerdos` ahora TIERED por relevancia: recuerdo muy relevante
  (dist<0.35)→700 chars (casi completo, ya no fragmenta lo importante), medio→450,
  lejano→300. + tope global del bloque 2500 (anti-bloat) + orden por relevancia.
- Cierra G5 (recuerdos cortados). For3s ya tenía topes; esto afinó el balance.

### AI7 — Registry/health de hilos ✅ (CERRADO 2026-06-24)
- `/miembros` (encargado): ve el equipo con nombre, rol, **última actividad** (health)
  y estado de la puerta. `/hilos` (cada persona): sus hilos/temas con actividad real
  (nº mensajes + cuándo). `temas.resumen_hilos` (HiloInfo, incluye 'general' implícito,
  orden activo-primero) + `equipo.miembros` enriquecido con última actividad (LEFT JOIN
  episodes_events).
- **4 mejoras pro (cierre profesional):** M1 nombre real del encargado (asegurar_equipo
  recibe nombre_encargado + AUTO-CURA filas viejas con nombre NULL — ya no "(sin nombre)") ·
  M2 ambos comandos en el menú por rol (/hilos→básico, /miembros→admin) · M3 health: última
  actividad por miembro ('activo hoy', 'hace N días') · M4 aislamiento de /hilos verificado
  (cada persona ve SOLO sus hilos). Verificado 8/8 checks + 132 tests.
- 🎉 **Con AI7 cerrado, la adopción AI1-AI7 está COMPLETA.**

## 4. Pendientes viejos CERRADOS de paso

- ✅ **P4** + **G4-version-self-awareness** → cerrados por AI5.
- ✅ **G5-recuerdos-fragmentados** → cerrado por AI6.
- ✅ **G6-repos-no-se-enlistan** (destapado en prueba real: el bot tenía 16 repos en
  gh_resources pero recordaba 2). FIX: `memory.repos_analizados` + detector
  `_es_pregunta_repos` + inyección de la lista REAL. Verificado: 16 repos.

## 5. Test de INTEGRACIÓN AI1-AI7 en conjunto

- 26 checks, 0 fallos, con embeddings + LLM reales. Escenario multi-usuario
  (Brian + 2ª persona, cada uno con temas): temas separados, aislamiento, STATUS
  independiente por hilo, audit no se filtra entre hilos. Confirma que los 7
  cooperan sin pisarse.

## 6. ⭐ LIMPIEZA — For3s OS = desarrollo propio (sin rastro externo)

Brian (regla crítica): "en ningún lugar del código debe haber relación entre For3s
OS y sistemas externos — cuando saquemos For3s debe ser EL desarrollo de For3s, no
la implementación de herramientas externas".

- Eliminadas TODAS las menciones en el código de: el sistema externo de referencia,
  Hermes, OpenClaw, y Frutero (incl. el bloque de identidad de la personalidad, el
  email, el User-Agent web y comentarios). Solo se tocó TEXTO; el código quedó
  intacto y funcional (132 tests).
- La personalidad del bot ahora dice solo "Eres For3s OS, un agente de IA"
  (identidad 100% del producto, sin atribución externa ni personal — decisión Brian).
- Verificación: búsqueda en TODO el código de esos términos → CERO resultados.
- La trazabilidad de "de dónde vino la idea" vive SOLO en Mente OS (docs privados,
  ver `Analisis_internOS_vs_For3s_OS.md`), NUNCA en el código distribuible.

## 7. Estado técnico al cierre

```
BD migraciones: v16 (013 telegram_user_id · 014 temas · 015 corridas_equipo ·
                016 hilo_status, además de las de H8 S10: 010-012)
Módulos nuevos: temas.py · handoff.py · hilo_status.py · version.py
Tests: 132 pasan · 26 checks de integración AI1-AI7
Servicios: for3s-telegram + for3s-worker activos
Comandos nuevos en Telegram: /tema · /temas · /version · /hilos · /miembros
Cron nocturno: backup 01:00 · CLS 02:00 · STATUS 02:30 (nuevo) · Microglía 03:00 (Mx)
```

## 8. Pendientes que siguen abiertos

- ✅ **AI1-AI7 COMPLETOS** (adopción cerrada).
- **AI3 parte 2** (separación de escritura del gate) — cruza con apartado E.
- **Pulido H8** áreas B, C, E (disparo, puerta UX/avisos, gate ejecución real).
- **H BYOK** (1 API key por persona) — sub-sistema grande pendiente.
- Producto distribuible P1-P10 · multi-tenant (G/H8-aislamiento) · backup-offsite.
