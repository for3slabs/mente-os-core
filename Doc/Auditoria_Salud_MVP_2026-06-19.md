# Auditoría de salud del MVP — For3s OS (2026-06-19)

> **Qué es:** informe de salud técnico del sistema completo, hecho por detrás
> (procesos, BD, integridad de auditoría, features, errores) tras la ronda de
> pruebas en vivo de Brian. **Propósito:** respaldar con datos reales la decisión
> de declarar (o no) el MVP cerrado. NO es de memoria — todo verificado contra el
> servidor `for3s` en producción el 2026-06-19.

**Veredicto en una línea:** ✅ **Sistema sano y estable. Cero errores reales
activos. Los 3 fallos reportados + 2 fixes posteriores (routing write, falso
positivo web→GitHub) CERRADOS y verificados EN VIVO. Apartados Archivos/Web
(migración 006) poblándose correctamente con timestamp. Cadena de auditoría
íntegra (718 entradas). En posición sólida para cerrar el MVP.**

> **Actualización:** este informe se amplió tras una 2ª ronda de pruebas de Brian
> (ver §4b). Lo verificado original (§1-§4) sigue vigente; §4b añade lo nuevo.

---

## 1. Salud del sistema

| Área | Estado | Detalle |
|---|---|---|
| Servicios | ✅ todos `active` | for3s-telegram · valkey-server · postgresql |
| Recursos bot | ✅ holgado | 97 MB RAM · 0.2% CPU |
| Recursos server | ✅ holgado | 17 GB RAM libres de 18 · disco 3% (18/937 GB) |
| Procesos MCP | ✅ limpio | 1 solo contenedor MCP (sin huérfanos) |
| Base de datos | ✅ sana | schema v5 · 426 turnos · 703 audit · 467 gh_resources |
| Suite de tests | ✅ verde | **126 passed, 4 skipped, 0 fallos** |
| Errores reales desde último reinicio (01:20 UTC) | ✅ **0** | solo ruido cosmético de arranque (Updater.stop warning) |

---

## 2. Integridad de seguridad (la garantía B2B)

- ✅ **Cadena de auditoría ÍNTEGRA:** `audit.verify_chain() = (True, 703)`. Las 703
  entradas verifican criptográficamente (SHA-256 encadenado). La inmutabilidad
  (append-only, sin UPDATE/DELETE) funciona de verdad.
- ✅ Secretos cifrados por workspace (KEK), master key offline.
- ✅ El `github_write` (escritura confirmada) quedó auditado con args + result + URL.

Distribución de acciones en el audit (703 total): secret_read 216 · message_in 202
· message_out 178 · (tests 84) · gh_fetched 9 · gh_fetch_failed 6 · secret_set 3 ·
pr_fetched 2 · **github_write 1** · otros 2.

---

## 3. Los 3 fallos reportados — CERRADOS y verificados EN VIVO

| Fallo | Causa raíz | Fix | Verificación en producción |
|---|---|---|---|
| **A — PDF grande no se leía** | provider timeout 60s → `httpcore.ReadTimeout` con base64 grande | timeout 180s + aviso si >8 MB | ✅ El PDF que fallaba ("La Biblioteca de la Medianoche") se leyó completo (turno 368, resumió la trama real). **0 errores de adjunto desde el fix.** |
| **B — "soy solo texto"** | consecuencia de A (sin contenido, el modelo improvisaba) | se cura con A | ✅ ya no aparece |
| **C — comentar en repo fallaba** | routing: URL de repo → análisis en vez de write | detector `quiere_escribir` → fuerza flujo de tools | ✅ comentario real escrito en `fruterito101/Proyecto#1`, `github_write ok=True` en audit, comentario visible en GitHub |

---

## 4. Las 5 features del pulido — activas en el bot vivo

Verificado por introspección del proceso en producción (no solo por import):

- ✅ **Conteos exactos:** 8 read tools incl. search_issues/search_pull_requests
- ✅ **Write tools:** 4 permitidas (add_issue_comment, create_issue,
  create_pull_request, create_pull_request_review) + whitelist dura
- ✅ **Timeout 180s:** confirmado en el código fuente del bot vivo (setup pasa
  `timeout=180.0` explícito)
- ✅ **Multimodal:** límite nativo 8 MB (aviso honesto si se supera)
- ✅ **Web fetch híbrido:** umbral SPA 350 (cae a render headless)
- ✅ **Cache Valkey:** funcionando (hits=3/misses=4 reales; keys expiran por TTL,
  comportamiento esperado)

---

## 4b. Avance posterior — apartados Archivos/Web + 2 fixes (verificado EN VIVO)

Tras la auditoría inicial, Brian pidió y probó nuevas piezas. Todo verificado
contra la BD en producción (no de memoria):

**Migración 006 — apartados ligeros (schema v5 → v6):**
- ✅ `consulted_files` (tipo + nombre + resumen + `consulted_at`) — **1 fila real**
  guardada en vivo (Word `mi-pase-reporte-analisis-datos.docx`, 02:17:53).
- ✅ `consulted_web` (url + título + descripción + `consulted_at`) — **3 filas
  reales** (openclaw.ai + 2 de tiktok.com, incl. una con query params largos).
- ✅ **Ligereza confirmada:** resumen/descripción topados a 2000 chars, SIN
  binarios ni HTML. El más largo = 2000 (truncado por diseño).
- ✅ **Columna de tiempo:** `consulted_at` TIMESTAMPTZ en ambas (UTC, offset 0).
- ✅ **Correlación perfecta:** 3 webs esperadas = 3 guardadas; 1 archivo = 1
  guardado. Nada perdido ni duplicado.

**Fix routing write (comentar):** un URL de repo desviaba "comenta…" a análisis.
→ detector `quiere_escribir` fuerza el flujo de tools. ✅ Verificado: comentario
real escrito en `fruterito101/Proyecto#1` + `github_write` en audit.

**Fix falso positivo web→GitHub:** `huele_a_github` confundía `dominio.com/path`
con `owner/repo` (tvazteca/tiktok no se leían). → `_quitar_urls_no_github` antes de
evaluar. ✅ Verificado EN VIVO: tiktok.com ahora entra al flujo web (turnos
373-376); github.com/owner/repo + repos en texto humano siguen detectándose.
Validado contra 17 casos aislados (0 fallos).

**Estado de tests tras estos cambios:** 128 passed, 4 skipped. Cadena de auditoría
re-verificada: **(True, 718)** — íntegra tras migración 006 + fixes.

---

## 5. Observaciones menores (NO bloqueantes)

- ⚠️ **Red doméstica parpadea:** `NetworkError` intermitente en logs. El error
  handler lo absorbe (el bot NO muere ni ensucia). Solución de fondo = mover server
  a VPS (a futuro). No bloquea nada hoy.
- ℹ️ **Ruido cosmético de arranque:** `RuntimeWarning: Updater.stop` + `server run
  cancelled` al reiniciar — documentado como conocido, no es error.
- ℹ️ **workspace_id:** datos en `default`/`brian` (mono-tenant, como debe ser hoy).
  El esquema ya está namespaced para multi-tenant futuro.
- ℹ️ **Resumen de archivos topado a 2000 chars** (por diseño, "ligero"). Si se
  quisieran resúmenes más largos para documentos, subir `_MAX_RESUMEN` en memory.py.
  Hoy es suficiente para "saber qué te mandaron".

---

## 6. Conclusión

El sistema pasó la auditoría profunda sin hallazgos críticos ni medios. Lo que
Brian reportó como fallos está cerrado y **verificado con sus propias pruebas en
vivo** (no solo tests). La integridad criptográfica del audit — el diferenciador
de confianza de For3s — está demostrada (`verify_chain` OK sobre 703 entradas).

**Recomendación:** el MVP es técnicamente **declarable como cerrado**. El criterio
de cierre (ver `PENDIENTES.md` / análisis previo): (a) features nuevas probadas en
vivo sin fallos bloqueantes ✅, (b) todo lo demás (P1-P5 paridad Hermes, webhooks,
multi-tenant, cron…) clasificado como post-MVP ✅. Ambos se cumplen.

La decisión formal de cierre es de Brian. Este informe es el respaldo técnico.

> Trazabilidad de los cambios: `Doc/Changelog_Pulido_MVP_2026-06.md`.
> Pendientes y clasificación MVP/post-MVP: `Doc/PENDIENTES.md`.