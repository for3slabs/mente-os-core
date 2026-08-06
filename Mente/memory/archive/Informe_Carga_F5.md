# 📊 Informe de Carga — Frente B F5 (canal API)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Informe_Carga_F5.md → memory/archive/Informe_Carga_F5.md (2026-07-30, ADR-029)

> **Qué es:** el "número honesto" que pidió Brian (Ronda §5, bug #10): cuánto aguanta
> el canal API de For3s, dónde está el cuello, y los 2 bugs de concurrencia que la
> carga cazó. Medido en el server `for3s` el 2026-07-15. Script: `scripts/carga_f5.py`.

## 1 · Método (2 planos, a propósito)

For3s responde con LLM y las 5 instancias comparten UN cupo de Claude, así que medir
`/v1/chat` a lo bruto quemaría el cupo y golpearía a los bots reales. Por eso dos planos:
- **HTTP/infra** (`/v1/health`, sin LLM): mide lo que NOSOTROS controlamos (túnel + aiohttp + red).
- **LLM** (`/v1/chat` real, controlado): latencia de respuesta completa + dónde topa el proveedor.

## 2 · Resultados — plano HTTP/infra

| Escenario | Concurrencia | RPS | Éxito | p50 | p95 | máx |
|---|---|---|---|---|---|---|
| Local (127.0.0.1) | 20 | **3856** | 100% | 4.9ms | 6.7ms | 40ms |
| Local | 50 | 1369 | 100% | 34ms | 63ms | 167ms |
| Local | 100 | 1329 | 100% | 70ms | 132ms | 275ms |
| Local | 200 | 1333 | 100% | 138ms | 271ms | 661ms |
| **Túnel público** (Funnel) | 20 | **466** | 100% | 41ms | 65ms | 108ms |
| Túnel | 50 | 464 | 100% | 103ms | 179ms | 284ms |
| Túnel | 100 | 461 | 100% | 194ms | 411ms | 762ms |

**Lecturas:**
- La infra es **sólida**: 100% de éxito hasta 200 concurrentes, sin un solo error HTTP.
- Techo local ~1330 RPS estable (1 event loop de aiohttp; a baja carga pica a ~3856).
- **El túnel es el cuello de la infra**: ~465 RPS techo por internet (vs 1330 local). Aun así,
  100% de éxito hasta 100 clientes simultáneos golpeando salud. Para un canal de API de negocio
  (no un CDN), 465 req/s de puerta es holgado.

## 3 · Resultados — plano LLM (respuesta real)

| Concurrentes | Éxito | Latencia p50 | Nota |
|---|---|---|---|
| 4 | 100% | ~35s | limpio |
| 8 | 100% | ~34s | limpio |
| 10 | 100% | ~37s | limpio (tras fix; antes 40%) |
| 20 | 100% | ~45s | limpio (tras fix) |
| 12+ (algunas corridas) | 83% | — | 529/rate transitorio del PROVEEDOR |

**El número honesto:** el canal atiende con seguridad **~8-10 llamadas LLM concurrentes** por
instancia antes de que **el proveedor (Claude), no For3s**, sea el límite. Es exactamente lo que
la Ronda anticipó: *"For3s responde con LLM → la concurrencia real la marca el proveedor"*.
La latencia de una respuesta completa es ~35-45s (sonnet-4-6 razonando + herramientas), no es
un chat de una línea. Para más volumen: BYOK (cada cliente con su cuenta = su propio techo) o
más instancias.

## 4 · 🐛 2 BUGS de concurrencia cazados POR la carga (el valor real de F5)

Ambos **invisibles en uso normal** — solo aparecen con escrituras simultáneas en la MISMA sesión
(p. ej. un cliente API con varias llamadas a la vez). Fix + verificación en commit `30ea6e1`.

1. **`record_turn` (memoria) — race del seq.** Era `SELECT MAX(seq)+1` y luego `INSERT` aparte:
   dos escrituras concurrentes leían el mismo MAX → ambas insertaban el mismo seq →
   `UniqueViolation(session_id, seq)` → **500**. A 10 concurrentes: 40% éxito, 6 fallos.
   **Fix:** el seq se calcula DENTRO del `INSERT ... SELECT` (atómico) + reintento con jitter ante
   la colisión residual. **Verificado:** 10 y 20 concurrentes → 100% éxito, 0 UniqueViolation.

2. **`audit.append` (cadena hash inmutable) — bifurcación de la cadena.** Era `SELECT último
   hash_self` + `INSERT`: bajo concurrencia dos filas leían el mismo `hash_prev` → la cadena se
   **bifurcaba** → `/salud` marcó "Audit chain ROTA" (154 eslabones). Es la línea roja del proyecto
   (audit inmutable). **Fix:** `pg_advisory_xact_lock` serializa los `append` entre sí (la cadena
   es secuencial por naturaleza — no hay forma concurrente de encadenar) sin bloquear otras tablas.
   **Reparación:** re-encadenado one-shot en orden original (con constancia en el propio audit) →
   `verify_chain` = íntegra=True, 700 entradas → 743 tras una nueva carga SIN romperse.

## 5 · Veredicto

- **Infra: producto, no MVP.** Cero errores HTTP hasta 200 concurrentes; el túnel da ~465 RPS por
  internet con 100% de éxito.
- **LLM: el techo lo pone el proveedor** (~8-10 concurrentes/instancia), como se diseñó. BYOK y
  multi-instancia son las palancas de escala.
- **F5 pagó su precio:** cazó 2 bugs de concurrencia reales y latentes (uno tocaba la línea roja del
  audit) que jamás habrían salido sin carga. Ambos cerrados y verificados bajo la misma carga.

**Pendiente futuro (no urgente):** si algún cliente necesitara >10 LLM concurrentes sostenidos,
evaluar un 2º worker/proceso del canal o pool de conexiones dedicado — hoy no hace falta.

---

## 6 · Prueba de ESTRÉS MÁXIMO (2026-07-15, pedido de Brian: "sube hasta romper")

Segunda ronda, subiendo mucho más que la primera. Rate del canal elevado a 200/min temporalmente
(cliente `carga-max`, cuota amplia); restaurado a 6/min al terminar.

**Infra HTTP (health) — NO se pudo romper:**
| Workers concurrentes | RPS | Éxito | p95 | máx |
|---|---|---|---|---|
| 300 | 3621 | 100% | 150ms | 1.2s |
| 500 | 3503 | 100% | 212ms | 6.0s |
| 800 | 3030 | 100% | 491ms | 1.1s |
| 1200 | 3359 | 100% | 3.1s | 5.2s |
| **2000** | **3206** | **100%** | 5.0s | 5.4s |
| Túnel público, 500 | 513 | 100% | 788ms | 6.7s |

→ **2000 conexiones simultáneas, 0 errores.** El único síntoma de estrés es la latencia p95 que
sube (a 2000w ~5s de espera), pero TODAS responden 200. La infra no es el cuello.

**LLM (chat real) — el quiebre real:**
| Concurrentes | Éxito | Tipo de fallo |
|---|---|---|
| 15 | 100% | — |
| 25 | 100% | — |
| **40** | **90%** | **504 (timeout de cola), NO error nuestro** |

→ El techo cómodo subió a **~25-30 LLM concurrentes/instancia**. A 40, 4 llamadas superaron los
130s de timeout porque el LLM procesa en cola — es el límite del PROVEEDOR, no un bug. La cola se
llena, no se corrompe.

**La prueba de fuego (lo que de verdad importaba):** tras +350 llamadas LLM concurrentes y hasta
2000 HTTP simultáneos:
- ✅ **0 UniqueViolation, 0 error 500** — los 2 fixes de concurrencia de F5 aguantaron el estrés.
- ✅ **cadena de audit ÍNTEGRA** (verify_chain=True, 1096 entradas) — la línea roja no se rompió
  ni bajo carga extrema.
- ✅ los 3 bots reales siguieron vivos, demo respondiendo, /salud sin 🔴.

**Bug menor cazado:** el compose no pasaba `FOR3S_API_RATE_MAX` al agent → el rate del canal era
inmutable (siempre 6/min). Arreglado (commit `4783b9c`): ahora configurable por `.env` (default 6).

**VEREDICTO FINAL:** infra de nivel producto — imposible de tumbar con 2000 conexiones. El único
límite es la concurrencia de respuestas de IA (~25-30/instancia), y las palancas de escala ya
existen: BYOK (cada cliente su cuenta) + multi-instancia. **El Frente B está probado como producto,
no como MVP.**
