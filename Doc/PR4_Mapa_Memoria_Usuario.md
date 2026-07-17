# PR4 · Parte B — Mapa DETALLADO del flujo Memoria/Usuario (archivo×archivo)

> **Qué es:** el camino REAL que recorre un mensaje tuyo en Telegram, archivo por
> archivo, función por función, con los datos exactos que viajan entre ellos.
> Verificado leyendo el código en el server (2026-06-28). NO es alto nivel: aquí
> se ve QUÉ función llama a QUÉ función y CON QUÉ parámetros.
>
> Foco: identidad → sesión → memoria → BD (la zona de los bugs de PR4-A).
> Archivos cubiertos: telegram_channel.py · equipo.py · temas.py · conversation.py ·
> memory.py · perfil.py · embeddings.py · db.py · (kg.py / hilo_status.py / version.py
> como inyecciones de contexto).

---

## DIAGRAMA DETALLADO — comunicación real entre archivos

```
 TÚ (Telegram) ──"hola, ¿en qué quedamos?"──►  python-telegram-bot
                                                       │ update
                                                       ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║ telegram_channel.py :: TelegramChannel.on_message(update, context)   [L2086]   ║
║ ── EL ORQUESTADOR. Todo pasa por aquí. ──                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
   │
   │ (1) ¿QUIÉN ERES? — autorización fail-closed
   ├──────────────►  self._autorizar(user)                              [L729]
   │                   │
   │                   ├─► OwnerStore.is_authorized(uid)                [L339]
   │                   │     └─ lee ~/.for3s/telegram_owner.json (en cwd=/app/.for3s)
   │                   │        ⚠️ AQUÍ VIVIÓ EL BUG: si el json no se encuentra,
   │                   │           devuelve False → te trata como desconocido.
   │                   │
   │                   └─► (si no eres dueño) equipo.py :: EquipoStore.autorizar(
   │                         owner, uid, nombre)                        [equipo.py]
   │                         └─ consulta tablas equipo/miembros + estado puerta
   │                       devuelve (ok, motivo: "dueño"|"miembro"|"puerta_abierta"
   │                                              |"puerta_cerrada"|"privado")
   │                   ⛔ si ok=False → responde "privado/puerta cerrada" y CORTA.
   │
   │ (2) ¿CUÁL ES TU SESIÓN? — la "llave" de tu memoria
   ├──────────────►  self._sesion_de(user)                             [L704]
   │                   │
   │                   ├─► self._base_sesion(user)                     [L696]
   │                   │     if is_authorized(uid):  return "brian"   ◄─ DUEÑO
   │                   │     else:                    return f"tg:{uid}" ◄─ MIEMBRO
   │                   │     ⚠️ asimetría 'brian' vs 'tg:<id>' = origen del bug PR4-A
   │                   │
   │                   └─► temas.py :: TemaStore.activo(uid)          [temas.py]
   │                         tema == 'general'  → session_id = base ("brian")
   │                         tema == 'backend'  → session_id = "brian:backend"
   │                       RESULTADO: session_id  (ej. "brian")
   │
   │ (3) ¿QUÉ SCOPE DE MEMORIA? — 2ª capa de aislamiento (AI1)
   ├──────────────►  self._scope_de(user)                             [L719]
   │                   DUEÑO   → None   (ve TODO lo suyo + legado NULL)
   │                   MIEMBRO → uid    (solo su privada + común, nunca lo de otro)
   │
   │ (4) construye el motor de conversación con esas 3 llaves
   ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║ conversation.py :: Conversation(pool, agent, session_id,                       ║
║                     channel="telegram", telegram_user_id=uid,                  ║
║                     scope_user_id=scope)                            [L602]      ║
╚══════════════════════════════════════════════════════════════════════════════╝
   │ on_message llama →  convo.send(texto, ...)                        [L682]
   │
   │ (5) asegura que la sesión existe
   ├──────────────►  memory.ensure_session(pool, session_id, channel) [memory L38]
   │                   └─ INSERT INTO sessions (id, channel)  (si no existe)
   │
   │ (6) CAPTURA de perfil (¿dijiste "soy backend"?)
   ├──────────────►  perfil.py :: detectar_afirmacion(texto)          [perfil L?]
   │                   └─ PerfilStore.set_campo / add_rasgo            [perfil.py]
   │                      → tabla perfil_usuario (PK telegram_user_id)
   │
   │ (7) GUARDA tu turno (escritura de memoria)  ◄══ NÚCLEO ESCRITURA
   ├──────────────►  memory.record_turn(pool, session_id,             [memory L51]
   │                     role="user", content=texto,
   │                     channel, owner_user_id, equipo_id,
   │                     telegram_user_id=uid)
   │                   └─ INSERT INTO episodes_events                  [memory L90]
   │                        (session_id, seq, role, content, ...,
   │                         owner_user_id, equipo_id, telegram_user_id)
   │                   └─ (background) _embeber_bg → memory.embeddear_turno
   │                        → embeddings.embed(content)  [BGE-M3, ~3s]
   │                        → UPDATE episodes_events SET embedding     [memory L290]
   │
   │ (8) RECONSTRUYE el contexto para Claude  ◄══ NÚCLEO LECTURA
   ├──► memory.load_history(pool, session_id, last_n=MAX_HISTORY)     [memory L110]
   │       └─ SELECT ... FROM episodes_events WHERE session_id=$1     [memory L127]
   │          (los últimos N turnos crudos de ESTA sesión)
   │
   ├──► memory.buscar_semantico(pool, session_id, query,             [memory L167]
   │       solo_usuario=..., scope_user_id=scope)
   │       └─ embeddings.embed(query) → vector
   │       └─ SELECT ... WHERE session_id=$1                          [memory L233]
   │          AND embedding IS NOT NULL AND deleted_at IS NULL
   │          [+ si scope_user_id: AND (owner_user_id=scope            ◄═ AISLAMIENTO
   │             OR equipo_id IS NOT NULL OR owner_user_id IS NULL)]
   │          ORDER BY embedding <=> query  (distancia coseno, HNSW)
   │
   ├──► kg.py :: kg.conceptos(pool)        (grafo consolidado H6)     [conv L809]
   ├──► perfil.py :: PerfilStore.resumen(uid)   (quién eres)         [conv L?]
   ├──► hilo_status.py :: debe_inyectar/get   (retomar tras pausa)   [conv L841]
   └──► version.py :: resumen()               (si preguntas versión)  [conv L?]
   │
   │   TODO lo anterior se ENSAMBLA en un solo prompt
   ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║ agent.py :: Agent  →  llm.py :: ClaudeProvider  →  API Claude (OAuth)           ║
╚══════════════════════════════════════════════════════════════════════════════╝
   │ respuesta del modelo
   │ (9) GUARDA la respuesta (mismo record_turn, role="assistant")   [memory L51]
   ▼
 TÚ (Telegram)  ◄── respuesta ── _responder_seguro / md_a_html_telegram

────────────────────────────────────────────────────────────────────────────────
 PostgreSQL (db.py :: pool)  ── la conexión que comparten TODOS los de arriba ──
   episodes_events  (TUS TURNOS: session_id, seq, role, content, embedding,
                     owner_user_id, equipo_id, telegram_user_id, deleted_at)
   sessions         (id, channel)        perfil_usuario (telegram_user_id, ...)
   for3s_kg.*       (grafo de conceptos)  + tablas equipo/miembros/temas
────────────────────────────────────────────────────────────────────────────────
```

---

## Cómo leer las "llaves" que viajan (lo más importante)

Tres valores se calculan al inicio en `telegram_channel.py` y **viajan juntos** por todo
el resto del flujo. Entenderlos es entender el aislamiento de memoria entero:

| Llave | Quién la calcula | Dueño | Miembro | Para qué sirve |
|---|---|---|---|---|
| **session_id** | `_sesion_de` [L704] | `"brian"` (+tema) | `"tg:<id>"` (+tema) | el HILO: separa conversaciones |
| **scope_user_id** | `_scope_de` [L719] | `None` | `<id>` | el FILTRO semántico: qué recuerdos ve |
| **telegram_user_id** | `user.id` directo | `<id>` | `<id>` | el AUTOR: quién escribió cada turno (#3) |

> ⚠️ **La fragilidad (PR4-A):** la identidad del dueño depende 100% de que
> `OwnerStore.is_authorized()` [L339] lea bien `telegram_owner.json`. Si falla esa
> lectura, las 3 llaves salen como "miembro" → `session_id="tg:<id>"` (sesión vacía)
> → pareces haber perdido la memoria. **Eso fue exactamente el bug de la migración.**

---

## Estado de las conexiones (preliminar — se confirma en B.1-B.4)

| Conexión | Estado |
|---|---|
| on_message → _autorizar → OwnerStore/equipo | ⚠️ frágil (depende de json en cwd) |
| _sesion_de → _base_sesion → temas | ✅ conectado |
| Conversation → record_turn → episodes_events | ✅ conectado |
| Conversation → buscar_semantico (con scope) | ✅ conectado (AI1 verificado) |
| Conversation → perfil/kg/hilo_status/version | ✅ conectado (inyecciones) |

*(B.1-B.4 verifican cada una a fondo; B.5 cierra el documento.)*