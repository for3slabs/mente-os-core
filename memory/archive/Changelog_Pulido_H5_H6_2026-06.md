# Changelog — Pulido de H5/H6 (post-cierre H6, junio 2026)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Changelog_Pulido_H5_H6_2026-06.md → memory/archive/Changelog_Pulido_H5_H6_2026-06.md (2026-07-30, ADR-029)

> **Qué es:** registro consolidado de la fase de PULIDO de H5 (memoria real) + H6
> (se cuida solo), realizada tras cerrar H6. Misma filosofía que el pulido del MVP:
> Brian prueba en Telegram, reporta/auditamos, arreglamos iterando. **Cada arreglo:
> diagnóstico por detrás → fix → verificación en vivo → tests → documentar.**
>
> **Disparador clave (Brian):** "aunque los códigos estén listos y probados, si el
> agente no reconoce sus nuevas actualizaciones es donde empezamos a fallar." Esta
> fase cerró justo esa brecha entre "el código existe" y "el agente lo reconoce y usa".

**Fecha:** 2026-06-20 → 2026-06-22 · **Estado:** ✅ fase COMPLETA (1 pendiente de config: backup-offsite)
**Servidor:** `for3s` · 132 tests verdes · bot + worker vivos · todo en producción.

---

## §1 — El problema raíz que arrancó la fase

Auditoría de las conversaciones de Telegram (19-22 jun) reveló: el código tenía
H4-write, multimodal, H5 (memoria semántica) y H6 (grafo + consolidación), **pero la
PERSONALIDAD del agente (`FOR3S_ROLE`) seguía siendo la del MVP temprano.** El bot
respondía "soy solo texto", "no puedo recuperar sesiones anteriores", no mencionaba
sus capacidades nuevas. La funcionalidad estaba; el agente **no se reconocía capaz**.

---

## §2 — Arreglos FUNCIONALES (el agente reconoce y USA sus habilidades)

| # | Arreglo | Qué cambió | Verificación |
|---|---|---|---|
| 1 | **Personalidad actualizada** | `agent.py` FOR3S_ROLE reescrito: reconoce memoria semántica (H5), grafo + auto-organización nocturna (H6), GitHub leer/escribir, multimodal, cron. Movió fuera de "no puedo" lo que sí hace. | En vivo: lista correctamente todas sus capacidades |
| 2 | **Grafo H6 conectado al chat** | `conversation.py`: detectado que CLS LLENABA el grafo pero el bot NO lo LEÍA. Ahora en preguntas panorámicas inyecta el resumen de conceptos consolidados (`_es_pregunta_panorama` + `_formatear_conceptos` + `kg.conceptos`). | E2E: "¿en qué nos enfocamos?" → responde desde los 35 conceptos |
| 3 | **Memoria semántica: traía preguntas, no info** | `conversation.py` + `memory.py`: con `solo_usuario=True` el bot recuperaba sus PROPIAS preguntas (se parecen entre sí) en vez de las RESPUESTAS con info. Fix: doble búsqueda combinada (nuevo param `solo_asistente=True` para traer respuestas con datos + búsqueda general). | E2E: "¿qué repos analizamos?" → lista godinez-studio/Aider/DonutBrowser/cli/cli reales |
| 4 | **No repetir respuestas largas** | FOR3S_ROLE: directriz de NATURALIDAD — si se repite la misma pregunta, resumir breve + ofrecer detalle, no soltar el bloque completo. | En vivo: 2ª respuesta 338→233 chars, tono humano |
| 5 | **Juicio honesto sin ser tajante (mem-matiz)** | FOR3S_ROLE: ante un "no", distinguir lo EXACTO vs lo RELACIONADO; ofrecer lo relacionado real si lo hay, "no" limpio si no, NUNCA inventar. | E2E 2 casos: "bugs?"→ofrece repos reales; "Minecraft?"→"no, no invento" |
| 6 | **Memoria-meta (fallo intermitente)** | `conversation.py` `_formatear_recuerdos`: al repetir una pregunta, el bot recuperaba sus respuestas-META previas ("ya preguntaste", "no tengo registro") como memoria → bucle de auto-contaminación. Fix: filtro `_PREFIJOS_META_RUIDO` descarta esas respuestas-ruido. | E2E: misma pregunta 3× seguidas → las 3 traen repos reales, consistente |
| 6b | **Memoria SIN fecha (el bot no sabía CUÁNDO)** | El agente sabía QUÉ se dijo pero no CUÁNDO (se equivocó: dijo "hace rato" cuando fueron 5 días). Los recuerdos llegaban sin timestamp. Fix: `RecuerdoRelevante` + SELECT traen `created_at`; `_formatear_recuerdos` muestra fecha absoluta+relativa `[15 jun 2026, hace 7 días]`; FOR3S_ROLE instruye usarla. Ahora cada fragmento de memoria tiene su fecha = "mapa de cuándo se dijo qué". | E2E: bloque muestra `(Usuario [22 jun 2026, hoy]) ...` |

---

## §3 — Arreglos de ROBUSTEZ (infra)

| # | Arreglo | Qué cambió | Tests |
|---|---|---|---|
| 7 | **529-overloaded** | `llm.py`: el 529 (Anthropic sobrecargado) y otros 5xx transitorios reventaban en raise_for_status → bot MUDO (hueco real en la prueba). Fix: nueva excepción `ServidorSobrecargado` + reintento con backoff exponencial (500/502/503/529); aviso amable en Telegram en vez de traceback. | +2 tests |
| 8 | **429-system-prompt** | Auditoría TOTAL de los 10 sitios que llaman al LLM → todos YA OAuth-safe (los 429 al analizar repos grandes eran rate-limit REAL por volumen, no system custom). Mejoras: `_post` distingue 429-real (con retry-after→reintenta) vs 429-falso ('Error' sin retry-after→no reintenta, log [429-SYSTEM]). + **BLINDAJE** en `_build_system`: en OAuth, si llega system custom lo IGNORA + log [429-GUARD] → imposible que el 429-system tumbe el bot venga de donde venga. | +2 tests |
| 9 | **H6-formula-relevance v2** | Refuerzo por USO real (antes neutro): migración 009 (`veces_recuperado`), `tocar_recuerdos` suma 1 por recuperación, la fórmula usa el contador `relevance = decay × (1+0.1×min(usos,5))`. Lo más usado resiste mejor el olvido. | E2E: episodio recuperado 6× → 0.993→1.000 |

---

## §4 — Pendiente que quedó (config, no código)

- 🟡 **backup-offsite:** el código del off-site (rsync a brayaneth/WSL2) está LISTO y probado
  (falla defensivo, backup local intacto). Bloqueado por **Tailscale SSH** (su regla está en
  `action: check` = exige login web; un job automático no puede). Para activar: cambiar a
  `action: accept` en el JSON de Tailscale ACL (Access controls → JSON editor → bloque "ssh")
  + descomentar `FOR3S_BACKUP_OFFSITE` en el .env del server. Detalle paso-a-paso en PENDIENTES.md.

---

## §5 — Verificación del ciclo nocturno (NO es demo)

Confirmado en logs del worker: el ciclo "se cuida solo" **corrió SOLO** la madrugada del 22:
```
07:00 UTC (1 AM Mx) → backup OK (auto_for3s_20260622_070000.sql, archivo real)
08:00 UTC (2 AM Mx) → CLS: clusters=3, conceptos=3, marcados=45 (consolidó episodios nuevos)
09:00 UTC (3 AM Mx) → Microglía [REAL]: candidatos=0, olvidados=0 (correcto, nada viejo aún)
```
Olvido real activado (FOR3S_MICROGLIA_CONFIRMAR=true), seguro hoy (0 candidatos = datos jóvenes).

---

## §6 — Archivos tocados en el server (esta fase)

- `agent.py` — FOR3S_ROLE: capacidades actualizadas + naturalidad + juicio honesto.
- `conversation.py` — grafo al chat + doble búsqueda de memoria + filtro meta-ruido.
- `memory.py` — `solo_asistente` + `tocar_recuerdos` cuenta veces_recuperado + `marcar_consolidados`.
- `relevance.py` — fórmula v2 con refuerzo por uso real.
- `llm.py` — manejo 529 + diagnóstico 429-dual + blindaje system custom.
- `telegram_channel.py` — handler `ServidorSobrecargado` (aviso amable).
- `backup.py` — `copiar_offsite` (listo, off-site desactivado por Tailscale).
- `tasks.py` — carga .env al importar (fix del worker).
- `migrations/009_veces_recuperado.sql` (schema v9).
- `tests/test_h1.py` — +4 tests (529 ×2, 429 ×2).

---

## §7 — Veredicto

El agente pasó de "el código está pero el bot no lo reconoce" a **reconocer Y usar todas
sus habilidades**, con la memoria funcionando end-to-end (recibe → embebe → consolida de
noche → consulta) y robustez ante errores de Anthropic. La preocupación de fondo de Brian
quedó resuelta. Siguiente: H7 (DECIDE) cuando se dé por cerrada la fase.