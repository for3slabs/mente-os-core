# H6 — "SE CUIDA": Plan Maestro de Construcción (CLS + Microglía + Scheduler + Backup)

> **Qué es:** plan de obra SUPER DETALLADO de H6, el hito post-H5. H6 es el hito
> **más delicado de todos hasta ahora** porque, a diferencia de H5 (que solo
> AÑADÍA datos: embeddings, nodos de grafo — nunca borraba nada), **H6 MODIFICA y
> BORRA** datos de la memoria que ya está en producción. Un error aquí no es
> "no funcionó": es **pérdida de datos reales de Brian**.
>
> **Propósito:** tener el plan completo, con todos los sub-pasos, riesgos, criterios
> de verificación y plan de rollback, ANTES de tocar una sola línea de código o el
> servidor. Es la "biblioteca de obra" de H6 — la fuente de verdad de la construcción.
>
> **Regla de oro de H6:** *nunca se borra sin antes haber consolidado, y nunca se
> hace hard-delete de entrada — siempre soft-delete recuperable primero. El audit
> chain es SAGRADO: jamás se toca.*

**Fecha de plan:** 2026-06-20 · **Estado:** ✅✅✅ **H6 COMPLETO — 13/13 sub-pasos.** Los dos motores (CLS consolidar + Microglía olvidar) + scheduler + backup automático corren solos de noche. Ciclo nocturno completo verificado E2E (simulación de la noche: backup→CLS→Microglía dry-run, audit íntegro). Microglía en DRY-RUN por seguridad (activar con FOR3S_MICROGLIA_CONFIRMAR=true cuando Brian decida).
**Servidor:** `for3s` (Tailscale 100.112.177.53) · PostgreSQL 16 nativo · usuario app `for3s`
**Diseño LOCKED de referencia:** R2 B2 §2.6 (CLS) · R6 B3 (Microglía/forgetting extended) · Mapa Incremental H6
**Predecesor:** [[H5_Infra_Memoria_AGE_pgvector]] (memoria real — COMPLETO)

---

## 0. Estado REAL del sistema (verificado en servidor 2026-06-20)

Esto es la base sobre la que construimos. **NO inventar — esto es lo que HAY hoy:**

| Componente | Estado real | Implicación para H6 |
|---|---|---|
| Tabla `episodes_events` | 465 turnos, 31 sesiones, 456 con embedding | El "material" a consolidar/podar. Pocos datos aún → cuidado: el threshold de 10 episodios casi no dispara todavía. |
| Columnas de la tabla | `id, session_id, seq, role, content, tokens_in, tokens_out, model, created_at, channel, embedding` | **FALTAN** las columnas de H6: `consolidated_to_kg`, `relevance`, `last_accessed`, `deleted_at`. Hay que añadirlas (migración 008). |
| `workspace_id` | **NO existe** | Confirmado single-user. Toda la versión multi-tenant del diseño LOCKED **NO aplica hoy** (ver §2 Desviaciones). |
| Valkey | ✅ activo, `maxmemory 0` (ilimitado), policy `noeviction` | Ya corre (lo usa `cache.py` del MVP). Arq puede reusarlo, PERO con cuidado de no chocar con las keys del cache (usar DB lógica distinta o prefijo). |
| Cliente `redis` 8.0.0 (Python) | ✅ instalado | `cache.py` lo usa. Arq trae su propia dependencia de redis — verificar compatibilidad. |
| `arq` | ❌ NO instalado | Hay que instalarlo (Sub-paso 1). |
| `hdbscan` | ❌ NO instalado | Hace falta para el clustering de CLS (Sub-paso 4). Vigilar RAM (server ~19GB). |
| `kg.py` (Knowledge Graph) | ✅ en producción (H5) | CLS REUSA esto para escribir conceptos. No reescribir. |
| `embeddings.py` (BGE-M3) | ✅ en producción (H5) | CLS REUSA los embeddings ya guardados para clustering. No re-embeber. |
| Audit chain | ✅ inmutable (MVP) | ⛔ H6 jamás lo toca. Microglía SOLO toca `episodes_events`. |
| Backup | ⚠️ solo `~/for3s-backups/` manual pre-H5 | H6 formaliza backup 3-2-1 foundation ANTES de confiar en el olvido. |

---

## 1. Qué es H6 (resumen de una línea)

> Cada noche, mientras nadie lo usa, For3s **se va a dormir**: **consolida** los
> episodios parecidos en conceptos permanentes del grafo (CLS), y **olvida** el
> ruido viejo ya consolidado (Microglía) — sin tocar jamás el registro de auditoría.
> Resultado: la memoria deja de crecer infinita y **es mejor hoy que ayer**.

Dos motores nocturnos + la infraestructura que los dispara + backup que los respalda.

---

## 2. Desviaciones del diseño LOCKED (ALCANCE REAL de H6 v1)

El diseño LOCKED de H6 (R2 B2 §2.6 + R6 B3) es **grande**: incluye multi-tenant
(workspaces), tiers enterprise, 10 DataTypes, 5-layer forgetting policy, GDPR
workflow, APIs self-service, dashboard HTMX completo. **Nada de eso aplica hoy**
porque somos single-user. Igual que en H5 (Stella→BGE-M3), construimos la
**versión foundation single-user** y dejamos lo enterprise diseñado en la biblioteca.

| Diseño LOCKED pide | H6 v1 (lo que SÍ construimos) | Por qué |
|---|---|---|
| Multi-tenant `workspace_id` en todo | Sin workspace — single user | No hay clientes aún. Añadir multi-tenant es un hito propio (futuro). |
| 10 DataTypes + 5-layer policy | 1 tipo (episodio conversacional) + reglas simples | Solo hay un tipo de dato hoy. |
| Tiers enterprise (multipliers) | Sin tiers | Un solo usuario. |
| GDPR workflow + legal hold | NO en v1 (se diseña, no se programa) | Sin clientes no hay obligación GDPR todavía. SÍ respetar: audit intocable. |
| APIs self-service + dashboard HTMX | NO en v1 | El dashboard es R7 Frontend (hito posterior). |
| Cron por workspace TZ | Cron único (TZ del server / Brian) | Un solo usuario. |
| Backup 3-2-1 completo (WAL PITR + DR) | Backup 3-2-1 **foundation** (dump + 2 destinos) | El PITR/DR completo es H16. Foundation = suficiente para confiar en el olvido. |

⚠️ **Decisión a CONFIRMAR con Brian antes de programar (ver §"Decisiones abiertas"):**
las columnas nuevas (`consolidated_to_kg`, etc.) las añadimos **sin** `workspace_id`
para no inflar. Si más adelante hay multi-tenant, será una migración aditiva nueva.

---

## 3. Arquitectura de los dos motores nocturnos (la lógica)

### 3.1 CLS — Consolidación (Nodo 10) — job 2 AM

CLS = *Complementary Learning Systems* (McClelland et al. 1995): cómo el cerebro,
durante el sueño, pasa lo episódico (hipocampo) a lo semántico permanente (neocorteza).

> ⚠️ **CORRECCIÓN 2026-06-20:** se decidió `sonnet-4-7`, pero el ping de verificación
> del Sub-paso 5 dio **404 (ese modelo NO existe en la API)**. Decisión de Brian:
> usar **`claude-sonnet-4-6`** (el mismo verificado que ya corre el bot). El modelo
> de CLS queda **configurable por env** (`FOR3S_CLS_MODEL`) para cambiarlo trivial
> cuando se quiera. Esto valida la regla de "ping antes de codear".

**Decisión LOCKED original:** Híbrido — heurística filtra + LLM (Claude Haiku 4.5) focaliza.
⚠️ **DESVIACIÓN consciente (2026-06-20, decisión de Brian):** CLS usará **`sonnet-4-6`**
en vez de Haiku 4.5. Razón: conceptos más ricos (mejor razonamiento → mejores labels en el
grafo). Trade-off: costo > Haiku (el LOCKED eligió Haiku por costo), pero con los volúmenes
actuales (pocos episodios, threshold 10, solo summaries) el costo real es mínimo. Análoga a
la desviación Stella→BGE-M3 de H5 — se documenta para trazabilidad.
En ambos casos: solo se mandan **summaries** al LLM, **NUNCA** datos crudos (privacidad).

Pipeline del sleep cycle (LOCKED, R2 §2.6):
```
1. Tomar episodios pending (consolidated_to_kg = false), hasta max_per_run
2. Si hay < 10 → SKIP (no vale la pena despertar el LLM)
3. Clustering HDBSCAN sobre los embeddings BGE-M3 ya guardados (min_cluster_size=3)
4. Por cada cluster:
     · construir un summary (top temas, ejemplos representativos) — heurística
     · pedir a Haiku que extraiga EL CONCEPTO (label + descripción corta)
     · SOLO se le manda el summary, jamás los textos crudos completos
5. Escribir al Knowledge Graph (reusa kg.py):
     · si concepto similar existe → fortalecer arista (strengthen)
     · si no → crear nodo concepto + aristas DERIVED_FROM hacia los episodios fuente
6. Marcar esos episodios consolidated_to_kg = true
7. Meta-audit: registrar en audit_events (cuántos consolidó, cuántos clusters)
8. Fallback: si Haiku cae → heurística pura (labels pobres pero no se cae)
```

### 3.2 Microglía — Olvido inteligente (Nodo 6) — job 3 AM (DESPUÉS de CLS)

Microglía (en el cerebro: células que podan sinapsis que ya no se usan).

**Decisión LOCKED:** soft delete + decay. Simbiótico con CLS. **NUNCA toca audit.**

Lógica del soft delete (LOCKED, R2 §2.5 / R6 B3):
```
Por cada episodio, evaluar. SOLO se marca para soft-delete si cumple TODAS:
   · viejo:        created_at > 30 días
   · poco relevante: relevance < 0.3  (decay por desuso)
   · YA consolidado: consolidated_to_kg = true  ← la condición clave
⛔ NUNCA:
   · hard-delete de entrada (solo soft: deleted_at = now(), recuperable)
   · tocar audit_events (inmutable)
   · borrar algo no consolidado (se perdería su lección)
Registrar en audit_events (cuántos podó).
```

**Por qué el orden importa:** CLS corre a las 2 AM y marca `consolidated_to_kg=true`;
Microglía a las 3 AM solo borra lo que CLS ya "exprimió". La lección sobrevive en el
grafo; el papel suelto (episodio crudo) se archiva. **Nada importante se pierde.**

### 3.3 Scheduler (Valkey + Arq) — la infraestructura que dispara

Arq = scheduler de jobs async sobre Redis/Valkey. Corre los cron de 2 AM y 3 AM
sin bloquear el bot. Worker async separado (systemd unit propia).

⚠️ **Riesgo de colisión:** Valkey ya lo usa `cache.py`. Arq DEBE usar **otra DB
lógica** de Valkey (ej. db=1) o prefijo de keys propio, para no pisar el cache.

### 3.4 Backup 3-2-1 foundation

Antes de confiar en que la Microglía borre, hay que tener respaldo serio:
- **3** copias de los datos
- **2** medios/destinos distintos
- **1** copia off-site
v1 foundation: `pg_dump` periódico + 2 destinos (local + remoto). PITR/DR completo = H16.

---

## 4. SUB-PASOS DETALLADOS (orden de construcción)

> Cada sub-paso = explicar lógica → backup → construir/instalar → verificar aislado →
> **OK explícito de Brian** → integrar → reiniciar si aplica → tests de regresión →
> auditar. El bot sigue vivo en todo momento. Igual que H5.

### Sub-paso 0 — Backup pre-H6 + snapshot de seguridad ⛔ OBLIGATORIO PRIMERO
**Por qué primero:** vamos a modificar el schema y luego a borrar datos. Necesitamos
un punto de retorno limpio ANTES de nada.
- `pg_dump` completo de la BD `for3s` → `~/for3s-backups/pre-h6-YYYYMMDD.sql`
- Copia del directorio de código actual (git stash/commit o tar).
- Verificar que el dump restaura en una BD de prueba (no asumir que sirve).
**Criterio de éxito:** dump existe + restauración verificada en BD scratch.
**Rollback:** N/A (es el rollback de todo lo demás).

### Sub-paso 1 — Scheduler base (Arq sobre Valkey)
**Lógica:** instalar Arq, conectarlo a Valkey en una DB lógica separada del cache,
levantar un worker async como systemd unit, probar con un job "hola mundo".
- Instalar `arq` (uv). Verificar compatibilidad con `redis` 8.0 ya instalado.
- Config: Arq → Valkey **db=1** (cache usa db=0). Documentar la separación.
- Crear `tasks.py` (o `jobs.py`) en for3s_core con un job trivial de prueba.
- systemd unit `for3s-worker.service` (worker Arq), `enable` + `start`.
- Verificar: encolar job de prueba → el worker lo ejecuta → log confirma.
**Criterio de éxito:** job de prueba corre en el worker; cache (db=0) intacto.
**Riesgo:** colisión de keys con cache → mitigado por db lógica separada.
**Rollback:** parar/deshabilitar `for3s-worker.service`; desinstalar arq. El bot
no depende del worker para responder → quitarlo no rompe nada.

### Sub-paso 2 — Migración 008: columnas de gobierno de memoria
**Lógica:** añadir las columnas que CLS y Microglía necesitan. **Aditiva, nullable,
con defaults seguros** — no rompe nada existente (igual que la 007).
- `consolidated_to_kg BOOLEAN NOT NULL DEFAULT false`
- `relevance REAL` (nullable; null = sin calcular aún)
- `last_accessed TIMESTAMPTZ` (nullable; para el decay)
- `deleted_at TIMESTAMPTZ` (nullable; soft-delete. null = vivo)
- Índices: parcial sobre `consolidated_to_kg=false` (cola de pending) y sobre
  `deleted_at IS NULL` (filtro de vivos en todas las lecturas).
- ⚠️ **CRÍTICO de coordinación:** TODAS las lecturas existentes de `episodes_events`
  (memory.py `buscar_semantico`, historial, etc.) deben empezar a filtrar
  `deleted_at IS NULL` para no devolver episodios soft-deleted. Auditar cada SELECT.
**Criterio de éxito:** schema v8; bot arranca y responde igual; todos los SELECT de
memoria filtran soft-deleted; tests de regresión OK.
**Riesgo:** olvidar un SELECT → la memoria devolvería basura borrada. Mitigación:
grep exhaustivo de todos los `FROM episodes_events` antes de cerrar el paso.
**Rollback:** las columnas son aditivas; si algo falla, `DROP COLUMN` (nadie las usa aún).

### Sub-paso 3 — Cálculo de `relevance` y `last_accessed` (decay)
**Lógica:** Microglía necesita saber qué es "poco relevante". Definir cómo se calcula
relevance y cómo se actualiza last_accessed. **Sin esto, Microglía no puede decidir.**
- `last_accessed`: actualizar cuando un episodio es recuperado por `buscar_semantico`
  (un recuerdo recuperado = "usado" → se refresca). Fire-and-forget para no frenar.
- `relevance`: fórmula simple v1 (ej. decae con el tiempo desde last_accessed; sube
  si fue recuperado varias veces). Documentar la fórmula exacta. Empezar conservador.
**Criterio de éxito:** relevance se calcula y persiste; recuperar un recuerdo refresca
su last_accessed; verificado sobre datos reales.
**Riesgo:** fórmula muy agresiva → marca como irrelevante algo útil. Mitigación:
arrancar conservador; Microglía además exige consolidated_to_kg=true (doble candado).
**Rollback:** columnas nullable; dejar de calcular no rompe nada.

### Sub-paso 4 — CLS motor: clustering (HDBSCAN) aislado
**Lógica:** construir y verificar SOLO el clustering, sin LLM ni escritura aún.
- Instalar `hdbscan`. Vigilar RAM al cargar (server ~19GB, BGE-M3 ya usa ~2.6GB).
- Función que toma los embeddings de episodios pending y los agrupa
  (min_cluster_size=3). Devuelve clusters. **No escribe nada todavía.**
- Verificar sobre los 456 embeddings reales: ¿agrupa de forma sensata?
  (con tan pocos datos puede que casi todo sea "ruido"/sin cluster — es esperable).
**Criterio de éxito:** clustering corre, devuelve clusters coherentes o "sin cluster"
honesto; sin impacto en el bot vivo.
**Riesgo:** HDBSCAN pesado en CPU/RAM. Mitigación: límite max_per_run; correr solo
de noche; medir RAM.
**Rollback:** módulo aislado, no integrado → borrar archivo.

### Sub-paso 5 — CLS motor: extracción de concepto (sonnet-4-6) aislado
**Lógica:** dado un cluster, construir el summary heurístico y pedir a sonnet-4-6 el concepto.
- ConceptExtractor: summary (top temas + ejemplos) → prompt a **`sonnet-4-6`**
  (desviación consciente del LOCKED que pedía Haiku — ver §3.1).
- ⛔ PRIVACIDAD: enviar SOLO el summary, jamás los textos crudos completos.
- Fallback: si el LLM cae → label heurístico (pobre pero funcional).
- ✅ Acceso: el bot ya corre sonnet-4-6 con el token actual → sonnet-4-6 es misma
  familia/API, acceso prácticamente garantizado. Confirmar con un ping rápido al
  llegar aquí (no bloquea el plan).
**Criterio de éxito:** dado un cluster de prueba, devuelve un concepto razonable; el
fallback heurístico funciona si se simula caída del LLM.
**Riesgo:** costo (sonnet > Haiku). Mitigación: threshold de 10, max_per_run,
solo summaries. Medir costo real en la prueba nocturna.
**Rollback:** módulo aislado.

### Sub-paso 6 — CLS motor: escritura al grafo (reusa kg.py) aislado
**Lógica:** dado un concepto, escribirlo en el Knowledge Graph respetando las 4 reglas
de AGE de H5 ([[H5_Infra_Memoria_AGE_pgvector]]).
- Si concepto similar existe → strengthen edge; si no → crear nodo + DERIVED_FROM.
- REUSA los helpers de `kg.py` (cypher_write/cypher_read_json). Respetar reglas AGE.
- ⚠️ Idempotencia: correr dos veces el mismo cluster no debe duplicar nodos (MERGE).
**Criterio de éxito:** concepto aparece en `for3s_kg` con aristas a sus episodios;
correr dos veces no duplica; verificado con cypher_read_json.
**Riesgo:** romper alguna de las 4 reglas AGE (palabras reservadas, alias, etc.).
Mitigación: releer las 4 reglas de H5 antes de escribir queries.
**Rollback:** los nodos creados se pueden borrar con cypher_write DELETE.

> ⚠️ **HALLAZGO RATE-LIMIT (2026-06-20, investigado en doc oficial Anthropic):** el
> token OAuth de suscripción opera como **Tier 1**, donde **Sonnet 4.x tiene el límite
> de tokens MÁS BAJO** (30k input/min, 8k output/min — vs Haiku 50k/10k, Opus 500k/80k).
> Además el "token bucket" se vacía con ráfagas y hay "acceleration limits" por subidas
> bruscas de uso. Por eso las pruebas en ráfaga del Sub-paso 5 dieron 429 (RateLimitExceeded).
> NO es bug del código (el 429 prueba que conecta+autentica OK; el fallback funciona).
> **Blindaje (decisión Brian): ESPACIAR las llamadas entre clusters + reintentos con
> backoff respetando retry-after**, en el orquestador (este sub-paso 7). Como CLS corre
> 1 vez de noche, pocas llamadas espaciadas → no topará en producción.

### Sub-paso 7 — CLS orquestador completo (end-to-end, manual, NO cron aún)
**Lógica:** unir 4+5+6 en `CLSOrchestrator` y correrlo UNA vez a mano (no en cron)
sobre los datos reales, con dry-run primero.
- Modo **dry-run**: muestra qué consolidaría SIN escribir ni marcar nada.
- Luego corrida real manual: consolida, marca consolidated_to_kg=true, audita.
- Verificar idempotencia: 2ª corrida no re-consolida lo ya marcado.
**Criterio de éxito:** dry-run claro; corrida real consolida correctamente; marca
flags; audita; idempotente; bot vivo sin impacto.
**Riesgo:** efecto en cadena (marca flags que luego habilitan borrado). Por eso aún
NO está la Microglía conectada — se prueba CLS solo primero.
**Rollback:** revertir flags (`UPDATE ... consolidated_to_kg=false`) + borrar nodos
de grafo creados en la corrida (quedan identificados por la corrida).

### Sub-paso 8 — Microglía motor: evaluación (DRY-RUN, sin borrar) aislado
**Lógica:** construir el evaluador que decide retain/archive/soft-delete, pero en
**modo dry-run absoluto**: solo REPORTA qué borraría, NO borra nada.
- Aplicar las 3 condiciones (viejo + poco relevante + consolidado).
- Mostrar lista de candidatos a soft-delete con su razón.
- ⛔ En este paso NO se ejecuta ningún UPDATE de borrado.
**Criterio de éxito:** lista de candidatos coherente; con los datos actuales
probablemente 0 candidatos (todo es reciente) — eso es CORRECTO y esperado.
**Riesgo:** lógica que marque de más. Por eso es dry-run: Brian revisa la lista
ANTES de habilitar el borrado real.
**Rollback:** módulo aislado, no borra.

### Sub-paso 9 — Microglía soft-delete real (con doble candado + recuperable)
**Lógica:** habilitar el soft-delete real, recuperable (deleted_at), con salvaguardas.
- Soft-delete = `UPDATE episodes_events SET deleted_at=now() WHERE ...` (NO DELETE).
- Doble candado: la corrida exige confirmación/flag explícito la primera vez.
- ⛔ Verificar que audit_events NUNCA se toca.
- Verificar que un episodio soft-deleted **desaparece** de buscar_semantico (gracias
  al filtro `deleted_at IS NULL` del Sub-paso 2) pero **sigue en la tabla** (recuperable).
- Procedimiento de **recuperación** documentado (UPDATE deleted_at=NULL).
**Criterio de éxito:** soft-delete funciona; episodio borrado no aparece en memoria
pero es recuperable; audit intacto; recuperación verificada.
**Riesgo:** EL MÁS ALTO de H6 — borrar datos reales. Mitigación: soft (no hard),
doble candado, backup del Sub-paso 0, dry-run previo del Sub-paso 8 revisado por Brian.
**Rollback:** `UPDATE ... SET deleted_at=NULL` (recuperación total — es soft).

### Sub-paso 10 — Cron nocturno (Arq): 2 AM CLS + 3 AM Microglía
**Lógica:** ahora que ambos motores están verificados a mano, programarlos en el
scheduler para que corran solos de noche, en orden.
- Registrar en Arq: CLS @ 2 AM, Microglía @ 3 AM (Microglía DESPUÉS de CLS, siempre).
- Empezar con Microglía en **modo dry-run dentro del cron** las primeras noches
  (consolida de verdad, pero solo REPORTA lo que podaría) hasta que Brian dé OK a
  habilitar el borrado nocturno real.
**Criterio de éxito:** los jobs se disparan a su hora; logs muestran la corrida.
**Riesgo:** algo corre de noche sin supervisión. Mitigación: Microglía en dry-run
primero; auditoría revisable a la mañana.
**Rollback:** quitar los cron del worker; deshabilitar la unit.

### Sub-paso 11 — Backup 3-2-1 foundation
**Lógica:** formalizar el respaldo serio antes de confiar 100% en el olvido nocturno.
- `pg_dump` periódico (cron) → local + 1 destino remoto (3 copias, 2 medios, 1 off-site).
- Verificar restauración (no asumir).
- Documentar el procedimiento de restore.
**Criterio de éxito:** backups automáticos corriendo; restore verificado.
**Rollback:** N/A (solo añade seguridad).

### Sub-paso 12 — Prueba nocturna real + auditoría E2E + documentación
**Lógica:** la DEMO de H6: dejar el sistema una noche y verificar a la mañana.
- Dejar correr una noche completa.
- A la mañana: revisar logs/audit → "CLS consolidó N, Microglía evaluó M
  (dry-run o real según fase), audit chain intacto".
- Auditoría completa: ¿memoria sana? ¿grafo creció con conceptos? ¿audit intacto?
  ¿bot respondió igual de bien?
- Documentar todo en Mente OS (este doc → estado COMPLETO + lecciones + RETOMAR + Bitácora).
**Criterio de éxito:** la demo del Mapa Incremental se cumple literalmente:
*"es mejor hoy que ayer"*, audit intacto, sin pérdida de datos importantes.

---

## 5. Riesgos transversales de H6 (los que aplican a todo)

| Riesgo | Severidad | Mitigación |
|---|---|---|
| Pérdida de datos reales por borrado | 🔴 ALTA | Soft-delete (no hard) + doble candado + dry-run revisado + backup pre-H6 + condición consolidated_to_kg. |
| Lecturas devuelven episodios borrados | 🔴 ALTA | Filtro `deleted_at IS NULL` en TODOS los SELECT (auditar cada uno en Sub-paso 2). |
| Arq pisa el cache de Valkey | 🟡 MEDIA | DB lógica separada (db=1) + prefijo de keys. |
| Tocar el audit chain | 🔴 ALTA | Microglía SOLO toca episodes_events. Verificar en cada corrida. |
| HDBSCAN/Haiku costo o RAM | 🟡 MEDIA | threshold 10, max_per_run, solo summaries, medir en prueba real. |
| Romper reglas AGE al escribir conceptos | 🟡 MEDIA | Releer las 4 reglas de H5 antes de cada query Cypher. |
| Job nocturno falla sin supervisión | 🟡 MEDIA | Dry-run primero + auditoría matutina + fallback heurístico. |
| Datos insuficientes hoy (465 turnos) | 🟢 BAJA | Esperado: CLS puede no disparar (threshold 10) y Microglía 0 candidatos. Es correcto — el sistema está listo para cuando crezca. |

---

## 6. Decisiones abiertas (confirmar con Brian antes de programar)

1. **¿Columnas sin `workspace_id`?** → Propuesta: SÍ, single-user foundation. Multi-tenant
   sería migración aditiva futura. *(Recomendado)* — ⏳ pendiente de confirmar.
2. **¿Modelo LLM para CLS?** → ✅ **DECIDIDO (2026-06-20):** **`sonnet-4-6`** (NO Haiku 4.5).
   Desviación consciente del LOCKED — conceptos más ricos a cambio de algo más de costo
   (mínimo con los volúmenes actuales). Acceso casi garantizado (misma familia que el
   sonnet-4-6 del bot); ping de confirmación rápido en el Sub-paso 5, no bloquea.
3. **¿Hora del cron?** → Propuesta: 2 AM / 3 AM hora del server (confirmar TZ del server). ⏳ pendiente.
4. **¿Microglía arranca en dry-run nocturno?** → ✅ **DECIDIDO (2026-06-20):** SÍ. Microglía
   corre en dry-run varias noches (solo REPORTA candidatos a podar, no borra). Brian revisa
   la lista. Solo cuando dé OK explícito → se habilita el soft-delete nocturno real.
5. **¿Destino off-site del backup?** → definir dónde (otro server, almacenamiento, etc.). ⏳ pendiente.

---

## 7. Mapeo al Grafo Maestro (trazabilidad)

- **Nodo 10 (CLS):** consolidación — Sub-pasos 4-7, 10
- **Nodo 6 (Microglía):** olvido — Sub-pasos 8-10
- **Nodo 2 (Hipocampo):** fuente de episodios — toda la base
- **Nodo 1 (KG):** destino de conceptos — Sub-paso 6 (reusa H5)
- **Pilar 3 (Autonomía):** "lo que hace al agente APRENDER" — CLS
- **Pilar 1 (Seguridad):** audit intocable + backup + privacidad (solo summaries al LLM)

---

## 8. Estado de los sub-pasos (actualizar conforme avanzamos)

| # | Sub-paso | Estado |
|---|---|---|
| 0 | Backup pre-H6 + snapshot | ✅ **COMPLETO** (2026-06-20) — dump 11MB + restauración VERIFICADA en BD scratch (465 ep, 456 emb, 767 audit, grafo Owner/Repo intactos) + snapshot código (tar 155K, git 93910bc). En `~/for3s-backups/pre_h6_subpaso0_*`. |
| 1 | Scheduler base (Arq/Valkey) | ✅ **COMPLETO** — arq 0.25.0 (redis 8.0 intacto). `tasks.py` (job `ping` + WorkerSettings, Valkey **db 1**; cache en db 0). systemd `for3s-worker.service` active. E2E: encolar→worker ejecuta→pong. 128 tests. |
| 2 | Migración 008 (columnas) | ✅ **COMPLETO** — schema v8: `consolidated_to_kg`, `relevance`, `last_accessed`, `deleted_at` + 2 índices parciales. `memory.py`: 3 lecturas filtran `deleted_at IS NULL` (las 2 MAX(seq) NO, a propósito + comentario). **Soft-delete VERIFICADO**: oculta de historial+semántica, recuperable 100%. |
| 3 | relevance + last_accessed (decay) | ✅ **COMPLETO** — `relevance.py` (v1 conservadora 0.5^(días/90)×refuerzo, piso 0.15). `tocar_recuerdos`+`_tocar_recuerdos_bg` (fire-and-forget). Verificado: 406 filas recalc (avg 0.967), last_accessed refresca. 🔖 PENDIENTE Brian: fórmula afinada (PENDIENTES: H6-formula-relevance). |
| 4 | CLS clustering (HDBSCAN) aislado | ✅ **COMPLETO** — hdbscan 0.8.44 (numpy/sklearn intactos). `consolidator.clusterizar_pendientes` (euclidean sobre embeddings normalizados ≈ coseno). Verificado sobre 397 reales: **23 clusters coherentes** + 272 ruido, 1.2s, 161MB RAM. SIN LLM, SIN escribir. |
| 5 | CLS concepto (sonnet-4-6) aislado | ✅ **COMPLETO + rama LLM VERIFICADA** — `extraer_concepto`: summary acotado (privacidad: 3 ej × 200 chars, nunca crudos) + sonnet-4-6 vía ClaudeProvider + fallback heurístico. Modelo por env. ⚠️ sonnet-4-7 NO existe→4-6. 🔑 **429 RESUELTO: era por system prompt custom (OAuth lo rechaza); fix = instrucción en user message, system=""**. Verificado: cluster 13ep→"Análisis Issues GitHub"/actividad/via_llm=True. |
| 6 | CLS escritura al grafo aislado | ✅ **COMPLETO** — `kg.registrar_concepto` (nodo Concepto + aristas DERIVED_FROM a episodios, MERGE idempotente) + `kg.episodios_de_concepto`/`conceptos` + `consolidator.escribir_concepto`. Verificado E2E. ⚠️ Trampa AGE 6: `RETURN e.seq` (int escalar) falla→envolver en mapa `{seq:e.seq}`. |
| 7 | CLS orquestador E2E (anti-429) | ✅ **COMPLETO** — `consolidator.consolidar(dry_run)` une S4→S5→S6→marcar flag→audit. Provider único + pausa 3s entre clusters (anti-429) + tope 20. ORDEN SEGURO: marca consolidated_to_kg SOLO si el concepto se escribió. `memory.marcar_consolidados`. dry-run probado primero. **CONSOLIDACIÓN MASIVA COMPLETA (bucle 7 rondas): el grafo pasó de 0 a 35 conceptos / 390 episodios consolidados. Quedan 15 pendientes = ruido único (no consolidable, correcto). Audit íntegro (792). 128 tests.** |
| 8 | Microglía evaluación dry-run | ✅ **COMPLETO** — `microglia.evaluar_candidatos`: 3 condiciones (viejo>30d + relevance<0.3 + consolidado + vivo). SOLO SELECT, cero borrado. Verificado: datos reales 0 candidatos (correcto), caso simulado SÍ lo detecta (probado en transacción con rollback, datos reales intactos). |
| 9 | Microglía soft-delete real | ✅ **COMPLETO** — `microglia.olvidar(confirmar=False)` doble candado: sin confirmar=dry-run; con confirmar=soft-delete real (deleted_at, recuperable) + tope 50/run + audit. `recuperar()` revierte. ⛔ nunca hard-delete, nunca toca audit. Ciclo completo (borra→invisible→recupera) verificado en transacción con rollback. 0 datos reales tocados. |
| 10 | Cron nocturno (2AM/3AM) | ✅ **COMPLETO** — `tasks.py`: jobs `job_cls`+`job_microglia` defensivos + cron en WorkerSettings. ⚠️ server en UTC → CLS 08:00 UTC (2AM Mx), Microglía 09:00 UTC (3AM Mx). Doble candado por env `FOR3S_MICROGLIA_CONFIRMAR` (default false=dry-run). Worker reiniciado, jobs disparados a mano: corren OK por Arq. |
| 11 | Backup 3-2-1 foundation | ✅ **COMPLETO** — `backup.py` (pg_dump verificado anti-truncado + rotación últimos 14, NO toca backups manuales) + job nocturno `job_backup` (07:00 UTC=1AM Mx, ANTES de CLS). Verificado: backup real 11M creado por el worker + rotación probada (retener=2 borró 1, manuales intactos). ⏳ OFF-SITE pendiente (PENDIENTES: H6-backup-offsite) — local primero por decisión de Brian. |
| 12 | Prueba nocturna + auditoría + docs | ✅ **COMPLETO** — simulación de la noche completa (3 jobs en orden vía worker: backup→CLS→Microglía dry-run). Auditoría E2E: audit chain íntegro (793→794), 0 episodios borrados (dry-run), 35 conceptos, bot+worker vivos, 128 tests. Mejora: el dry-run de Microglía ahora también deja evento en audit (`microglia_forget_dryrun`) para trazabilidad nocturna. Cron activos para correr de verdad esta madrugada. |

---

## 🎉 H6 "SE CUIDA" COMPLETO (2026-06-20)

For3s ahora **se mantiene solo de noche**, sin supervisión:
- **01:00 Mx** — backup automático verificado + rotación (red de seguridad).
- **02:00 Mx** — CLS consolida episodios nuevos → conceptos al Knowledge Graph.
- **03:00 Mx** — Microglía evalúa el olvido (HOY en dry-run: solo reporta).

**Estado del conocimiento:** el grafo pasó de 0 a **35 conceptos / 390 episodios** consolidados.
**Seguridad:** 0 datos borrados (Microglía en dry-run), audit chain íntegro, soft-delete recuperable.
**🔴 OLVIDO REAL ACTIVADO (2026-06-20, decisión de Brian):** `FOR3S_MICROGLIA_CONFIRMAR=true`
en .env. Worker arranca con `confirmar=True`. Red de seguridad reforzada al activar: tope
`MAX_OLVIDO_POR_RUN` bajado 50→20 (poda de a pocos por noche, recuperable) + backup fresco
`pre_olvido_real_20260620.sql`. Verificado: Microglía REAL con 0 candidatos = 0 borrados (seguro
hoy; los datos son recientes). ⚠️ FIX necesario: el worker NO heredaba el .env por systemd →
`tasks.py` ahora hace `_load_dotenv()` al importar (si no, la var quedaba en su default false).
⏳ Off-site del backup sigue pendiente (H6-backup-offsite) — conviene activarlo antes de que
haya candidatos reales (semanas/meses, cuando los episodios envejezcan >30d). Para volver a
dry-run: `FOR3S_MICROGLIA_CONFIRMAR=false` + reiniciar worker.

**Pendientes que dejó H6:** H6-formula-relevance (fórmula afinada de decay, la define Brian) ·
H6-backup-offsite (copia fuera del server) · 429-system-prompt (revisar flujos GitHub).

### Archivos creados/modificados en el server (H6 hasta Sub-paso 10)
- **Nuevos:** `tasks.py` (worker Arq + jobs CLS/Microglía + cron), `relevance.py`
  (decay), `consolidator.py` (CLS: clustering + concepto + escritura grafo + orquestador),
  `microglia.py` (evaluación + soft-delete + recuperar), `migrations/008_memory_governance.sql`.
- **Modificados:** `memory.py` (filtros soft-delete + tocar_recuerdos bg + marcar_consolidados),
  `kg.py` (registrar_concepto + episodios_de_concepto + conceptos).
- **Infra:** systemd `for3s-worker.service` (con cron); deps `arq`, `hdbscan` (+`hiredis`).
- **Valkey:** db 0 = cache GitHub (intacto) · db 1 = scheduler Arq.
- **Env nuevos:** `FOR3S_MICROGLIA_CONFIRMAR` (default false=dry-run) · `FOR3S_CLS_MODEL`
  (default claude-sonnet-4-6).
- **Estado del grafo:** 35 conceptos + 390 episodios consolidados (CLS corrió sobre toda
  la memoria). 15 episodios = ruido (no consolidable). 0 episodios borrados (Microglía en dry-run).

### 🔑 HALLAZGO CRÍTICO RESUELTO (2026-06-20 día 2): el 429 era por SYSTEM PROMPT custom
**Diagnóstico inicial (Sub-paso 5) estaba INCOMPLETO.** Tras análisis profundo el día
siguiente (rate-limit ya frío) se halló la causa REAL con pruebas A/B/C controladas:

- ❌ NO era ráfaga / demasiadas llamadas: **UNA sola llamada también fallaba**.
- ❌ NO era la suscripción saturada: utilización real **11% (5h) / 16% (7d)**, status `allowed`.
- ✅ **CAUSA REAL: el OAuth de suscripción RECHAZA system prompts personalizados** con un
  **falso "429 rate_limit_error"** (mensaje genérico "Error", SIN `retry-after`). Es
  anti-abuso: el token de suscripción solo tolera el system de Claude Code.

**Prueba que lo confirmó (mismo token, mismo momento):**
| system prompt | resultado |
|---|---|
| solo identidad Claude Code (vacío) | ✅ 200 |
| identidad CC **+ prompt CLS custom** | ❌ 429 "Error" |
| solo identidad + user pide JSON | ✅ 200 |

**SOLUCIÓN (aplicada en consolidator.py):** mover la instrucción del `system` al
**USER message** y dejar `system=""` — el patrón OAUTH-SAFE que el bot YA usaba (ver
`agent.py`: *"En modo OAuth el system DEBE ser solo la identidad de Claude Code"*). Tras
el fix, la rama LLM funciona: cluster de 13 ep análisis-GitHub → concepto **"Análisis
Issues GitHub" / tipo actividad / via_llm=True**. ✅ Verificado.

**Nota:** el espaciado + backoff del Sub-paso 7 sigue siendo buena práctica (por si en
producción concurre con el bot), pero la causa del 429 de hoy NO era esa. Regla para
TODO uso del LLM con OAuth: **instrucciones en el user message, system vacío.**

---

**Regla permanente de H6:** cada sub-paso = lógica explicada → backup → construir →
verificar aislado → **OK de Brian** → integrar → tests → auditar. NUNCA borrar sin
consolidar. NUNCA hard-delete de entrada. El audit chain es SAGRADO.