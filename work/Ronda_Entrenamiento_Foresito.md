# 🎓 RONDA — ENTRENAMIENTO FORESITO (@For3s_OS_bot): el agente de la EMPRESA aprende TODO

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_Entrenamiento_Foresito.md → work/Ronda_Entrenamiento_Foresito.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-18 · **Estado:** ✅ PLAN APROBADO por Brian (en vivo) — en ejecución.
> **Por qué:** Foresito es el agente de la EMPRESA y hoy es el que MENOS sabe (hallazgo del
> super-cerebro, `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md` — este hito es el 🅰️,
> "el pago final del super-cerebro"). Brian 2026-07-18: *"debe entender de principio a fin,
> sin omitir nada, leer TODA la información archivo por archivo"*.
> **Método:** espejo del HITO ENTRENAMIENTO de brian (E0-E6, probado) adaptado a fuentes de
> REPO (no jsonl OpenClaw). Cruza con: `work/Plan_Implementacion_Entrenamiento.md` ·
> `work/Entrenamiento_Ejecucion_Reporte.md` · `work/Plan_Backlog_Profundo_E6.md`.

---

## 1 · LAS 4 FUENTES (censadas 2026-07-18, local BrayanETH `~/for3s/`)

| Fuente | Archivos reales | Volumen texto | Qué es |
|---|---|---|---|
| `Mente/` | 183 (176 md) | ~1,010K tokens | Cerebro documental For3s OS (Alma/Cerebro/Cuerpo/Doc) — **el oro** |
| `for3s-inter/` | 105 (103 md) | ~242K tokens | Documentación interna |
| `marca-personal/` | 216 (118 código web + 48 md) | ~373K tokens | Sitio público (código + marca) |
| `For3s-OS/` | 224 (107 py + 46 sql + 20 md) | ~373K tokens | El producto (repo tríada, HEAD `8798190` v0.18.0) |
| **TOTAL** | **~728** | **~2M tokens** | (excluyendo node_modules/.git/caches — 838M de ruido filtrado) |

## 2 · DECISIONES DE BRIAN (2026-07-18, gate pasado)

1. **marca-personal INCLUIDA** — permiso EXPLÍCITO que levanta la regla ⛔ del CLAUDE.md
   SOLO para este entrenamiento (lectura para entrenar; no se modifica ese proyecto).
2. **CÓDIGO CRUDO al grafo también** — a diferencia del hito brian (regla "catálogo, no
   código"), Foresito absorbe el CONTENIDO completo del código. Mitigación acordada: cada
   episodio de código lleva **marca de versión/commit** (sabrá QUÉ versión conoce; al
   evolucionar el repo habrá que re-entrenar o convivirá con código viejo marcado).
3. **Backup + reversa demostrada ANTES del material real** — Foresito está EN PRODUCCIÓN
   (memoria de la empresa desde el inicio); red de seguridad obligatoria.
4. Plan completo APROBADO ("SI APRUEBO EL PLAN Y CONTINUA").

## 3 · LAS FASES T0→T6

- **T0 · Infra + red de seguridad:** (a) verificar migr 033/034 en Foresito (v0.18.0 las
  trae, confirmar en vivo) · (b) backup BD con RESTORE verificado · (c) **reversa
  demostrada en vacío** · (d) snapshot del material local → server (`~/entrenamiento-foresito/`,
  read-only; las fuentes viven en la laptop de Brian, el entrenamiento corre en el server).
- **T1 · Censo 1×1:** walker de las 4 raíces (filtro de ruido) → manifiesto de Foresito con
  hash/tipo/fecha-origen-git/duplicado. $0.
- **T2 · Secretos:** barrido línea a línea ANTES de importar (hay .env locales y docs con
  datos aunque gitleaks diga "repo limpio") → vault de Foresito + redacción. Regla KEK del
  hito brian: montar `~/.for3s/.env`/estado correcto para cifrar con la KEK REAL.
- **T3 · Olas docs:** ~460 md/txt → episodios con fecha ORIGEN (git log) + lote reversible
  `ef-docs-*`, chunking de grandes (Estado_Sesion 200KB). dry-run default.
- **T4 · Código crudo:** ~290 archivos código → episodios chunked con **marca
  versión/commit** (lote `ef-codigo`). Redacción de secretos igual que docs.
- **T5 · Digestión:** embeddings BGE local $0 + CLS nocturno (varias noches; convive con la
  cola de brian) + pasadas manuales opcionales con freno `FOR3S_FRENO_CUPO_5H`.
- **T6 · Cierre:** cobertura 0-sin-analizar + examen (~40 preguntas: arquitectura,
  decisiones LOCKED, código, marca) + batería §5-BIS + bitácora + commit firmado.

## 4 · MECÁNICA (reuso del tubo probado)

```
contenedor efímero (docker run --rm · red del compose PRINCIPAL de Foresito ·
  material :ro · KEK de Foresito si toca vault)
módulos existentes: entrenamiento.py (lotes/reversa) · entrenamiento_censo.py ·
  entrenamiento_secretos.py — agnósticos de instancia, apuntados a la BD de Foresito
módulo NUEVO: entrenamiento_repo.py (parser de archivos de repo: chunking + fecha git +
  marca de versión; sustituye al parser jsonl de OpenClaw)
```

## 5 · RIESGOS Y GUARDAS

- **Cupo:** T0-T4 ≈ $0 (local). Lo caro = T5 (~2M tokens repartidos en noches de CLS, mismo
  patrón que digirió 31K episodios de brian). Sin loops de fondo; tandas con freno.
- **Producción:** Foresito sigue vivo durante el entrenamiento (lotes aditivos reversibles;
  el bug incluir_import ya está fijado en la imagen → los imports serán visibles).
- **Deriva de código:** el repo evoluciona; los episodios llevan commit-stamp. Re-entrenos
  futuros = nuevas olas `ef-*` (mismo tubo, reversible).
- **Secretos:** redacción endurecida del hito brian (sk-/ghp_/pat/JWT/genéricos) se reusa.
- Material original INTACTO (snapshot :ro). Manifiesto = tablero auditable archivo×archivo.

---

## 6 · BITÁCORA DE EJECUCIÓN

### 2026-07-18/19 — T0→T4 COMPLETOS en una sesión (todo $0, sin LLM)

- **T0 ✅ red de seguridad:** (a) Foresito schema v45, manifiesto virgen, 822 eps + 834
  conceptos propios · (b) backup `~/backups-foresito/foresito_pre_entrenamiento_20260719_0052.dump`
  (4.9M) con RESTORE verificado (40/40 tablas, 822/822 eps, 834/834 grafo) · (c) **reversa
  demostrada en vacío** en SU BD (822→+3→822, suma_ids idéntica) · (d) snapshot 727 archivos
  → server `~/entrenamiento-foresito/` (11M, :ro) + `fechas_git.json` (For3s-OS 224/224 con
  fecha git; Mente/inter por mtime — el repo `~/for3s` no tiene commits) + `versiones.json`
  (repo-os=8798190 v0.18.0 · repo-marca=85f1c76).
- **T1 ✅ censo:** módulo NUEVO `entrenamiento_repo.py` (efímero, montado en /tmp — se
  commitea al repo en T6). 727 archivos censados: 354 DOC · 313 CODIGO · 47 CONFIG · 9 MEDIA ·
  4 dups · 1 SECRETO.
- **T2 ✅ secretos:** único secreto REAL = `repo-marca/.env.local` (excluido). 5 falsos
  positivos de la regex v1 ("secret" en el nombre) reclasificados como contenido (secret_store.py,
  docs de observabilidad, .env.example). Embebidos: solo 2 placeholders `github_pat_exp…` (len 32,
  ejemplos de docs; redactar() los tapa igual). Regex afinada en el módulo.
- **T3 ✅ docs:** 354 docs → **1,101 episodios** (mente 731 · inter 225 · marca 115 · os 30),
  lotes `ef-docs-*`, fecha ORIGEN + cabecera de procedencia. **0 secretos crudos** (verificado
  con grep de patrones sobre los import).
- **T4 ✅ código+config:** 364 archivos → **670 episodios** con **marca de versión/commit** en
  cada cabecera, lotes `ef-codigo-*`. **Rescate del cazador de bugs:** los sin-extensión valiosos
  (Dockerfiles, gestor `for3s`, `maestro`/`mente-os-nueva`, .service, sudoers, LICENSE/NOTICE)
  y el docx `FOR3S_EXPLICADO_PARA_JAZZ` (extractor de E6) NO se quedaron fuera — el clasificador
  se afinó y entraron. **Cierre del manifiesto: 727/727 con decisión — 0 sin analizar ✅.**
- ⚠️ Nota honesta: al reusar `ef-docs-mente`/`ef-docs-os` en el rescate, el CONTADOR del lote
  quedó con el valor de la última corrida (cosmético; los episodios están bien etiquetados y la
  reversa por lote los borra todos; la reversa total es el backup T0b).
- **T5 🔄 en curso:** backfill de embeddings (BGE local, $0) DENTRO del worker por tandas
  (`/tmp/backfill_embeddings.py`, reanudable) — ~5.7s/ep en CPU → ~2.8h para los 1,771. La
  digestión al grafo la hace el CLS nocturno (varias noches; convive con la cola de brian).
- **T6 ⏳ pendiente:** examen (~40 preguntas) + batería §5-BIS + commit del módulo + bitácora.

**Total importado corrida 1: 1,771 episodios** (1,101 docs + 670 código) de 727 archivos,
100% con veredicto individual en el manifiesto.

### 2026-07-18 noche — CORRIDA 2 (pedido de Brian: "no omitas nada, son pocos episodios")

- Al revisar `~/for3s` COMPLETO aparecieron fuentes fuera de la lista original:
  **Wiki-hackathons (3,076 archivos, ~6.1M tokens)** + `ramas-mente-os` + raíz
  (CLAUDE.md, `.codeviz`, settings).
- **Decisión Brian: Wiki-hackathons EXCLUIDO por ahora** (es material EXTERNO scrapeado del
  Monad Blitz — 3× el corpus ya importado; meterlo crudo diluiría el grafo de la empresa con
  código ajeno y triplicaría las noches de CLS). Importable después con ola reversible propia.
- **Corrida 2 aplicada:** fuentes nuevas `repo-ramas` + `repo-raiz` → **+58 episodios**
  (14 docs: CLAUDE.md raíz, docs .codeviz For3s, rama diseno-jazz del Maestro · 44 config).
  **Manifiesto: 741/741 con decisión — 0 omitidos ✅.**
- Aclaración registrada sobre el "son pocos": los 1,771 contienen los 727 archivos COMPLETOS
  (troceados a 6,000 chars); el número se siente chico vs los 31K de brian porque aquéllos
  eran TURNOS de conversación, no archivos densos. No falta contenido de las fuentes listadas.

**TOTAL HITO: 1,829 episodios · manifiesto 741/741 · 6 fuentes (mente/inter/marca/os/ramas/raiz).**

### 2026-07-18 noche — T5 EMBEDDINGS ✅ + 👑 PUENTE E DINÁMICO (Foresito = AGENTE MAESTRO)

- **T5 embeddings ✅ COMPLETO: 1,829/1,829** (BGE local $0, tandas en el worker; sobrevivió a un
  corte de sesión — reanudable demostrado). Queda SOLO la digestión CLS nocturna.
- **👑 DECISIÓN DE BRIAN:** *"ya sé quién va a controlar el Mente OS Maestro… es @For3s_OS_bot —
  mente maestro y agente maestro se unen"*. Foresito = **EL AGENTE MAESTRO.**
- **PUENTE E DINÁMICO CONSTRUIDO Y VIVO (PE1-PE5):**
  1. `GITHUB_PAT` al .env de Foresito (su compose ya lo esperaba; token del credential store,
     alcance verificado HTTP 200 a los 3 repos mente-os) + agente/worker recreados.
  2. **E2E ✅:** Foresito leyó `Maestro/registro.md` de `for3slabs/mente-os-maestro` EN VIVO por su
     GitHub MCP (get_file_contents, 7.2K chars).
  3. **Skill `agente-maestro` (id 22, H12, provenance=usuario):** el rol + cómo consultar el
     Maestro en vivo + reglas de oro (apuntar-no-replicar · GATE NavigoX · permisos fail-closed ·
     solo lectura).
  4. **registro.md actualizado y PUSHEADO** (`cfc0431` en mente-os-maestro): Foresito §3 =
     AGENTE MAESTRO, Pendiente A resuelto. **Prueba REDONDA ✅: Foresito leyó su propio
     nombramiento recién pusheado** (cambio en repo → visible al instante = ciclo dinámico).
  5. **Batería:** /salud 0 FAIL · 258 tests passed.
- **🐛 BUG DE PRODUCTO #1 cazado por el entrenamiento:** `salud_hilos` listaba TODAS las
  sesiones sin límite → con 741 sesiones `repo:*` del import, /salud escupía ~750 líneas en
  Telegram. Fix: corpus import contado aparte (no listado 1×1) + LIMIT 25 defensivo. Suite verde.
- **Cierre del fix (madrugada 07-19, tras 1 desconexión de red que mató el 1er build):** rebuild
  relanzado con `nohup` en el server (lección: builds largos SIEMPRE desacoplados de la ssh) →
  imagen `18858ba1f8c6` con el fix → Foresito recreado → **/salud: "729 sesiones (4 conversación ·
  725 corpus import)", reporte de 53 líneas (antes ~780), 0 FAIL ✅** → commit **`c1f6d56`**
  (server SIN push). PE1-PE5 + T5 CERRADOS.

### 2026-07-19 madrugada — ⚡ DIGESTIÓN ACELERADA ✅ (Brian: "aceleremos las noches")

- **🐛 BUGS DE DISEÑO #2 y #3 cazados por el dry-run ($0) ANTES de gastar:**
  (2) el CLS consolida POR SESIÓN y salta <10 pendientes → con el corpus 1-archivo-1-sesión,
  **el nocturno JAMÁS habría digerido el 77%** (706 sesiones chicas, 1,417 eps) — las "2-3
  noches" eran ∞. (3) clustering global cronológico = mega-cluster raso (469 eps → 1 concepto).
- **Runner `pasada_cls_repo.py`** (en `~/entrenamiento-runners/`): agrupa por MÓDULO natural
  (fuente+directorio) → HDBSCAN dentro → parte >60 en sub-conceptos de ~40 → fallback
  módulo-entero para grupos chicos. Marca por id GLOBAL. Motor real del CLS (extraer/escribir/
  marcar intactos). Freno de cupo 0.92 + pausa 6s anti-529 + presupuesto/pasada + reanudable.
- **5 pasadas en UNA madrugada: 117 conceptos · 1,740/1,829 digeridos (95%) · cupo 5h
  0.36→0.42 (+0.06 TOTAL — casi gratis, max_tokens=150/concepto).** Grafo: 834 → **2,687 nodos**.
  Residuo 89 eps (5%) = ruido HDBSCAN legítimo (chunks únicos; viven en memoria semántica).
- Conceptos muestra: "Fundamentos empresa For3s" · "Arquetipos de clientes" · "Estrategia de
  mercado" · "Visión For3s Frontier" · "For3s explicado Jazz" · "Workflows seguridad CI/CD"…
- **⏳ QUEDA SOLO T6: examen ~40 preguntas + batería §5-BIS + version bump.** (El grafo YA está
  maduro — no hay que esperar noches.)
