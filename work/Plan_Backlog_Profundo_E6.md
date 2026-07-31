# 🔬 PLAN E6 — BACKLOG PROFUNDO: los 3,876 archivos restantes, UNO POR UNO

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Plan_Backlog_Profundo_E6.md → work/Plan_Backlog_Profundo_E6.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-05 · **Estado:** PLAN detallado — ⛔ nada ejecutado (arranca con la orden de Brian)
> **La orden de Brian:** "no quiero que los analices solo por encima. Necesito un análisis de
> cada uno pero DETALLADO, todo, no omitir nada — ni archivos ni imágenes ni nada. Ve archivo
> por archivo, NO todos de una vez: uno por uno, para precisión mayor."
> **Extensión del HITO ENTRENAMIENTO** (E6). Destino: @For3s_Brian_bot. Manifiesto = tablero.

---

## 0 · PRINCIPIOS DE E6 (los mismos del hito + los nuevos de Brian)

1. **UNO POR UNO**: cada archivo se procesa individualmente y deja SU veredicto registrado
   en el manifiesto (`detalle.e6 = {tipo_real, resumen, veredicto, lote}`). Nunca "por lote
   ciego" — los lotes solo agrupan commits/reversa, no el análisis.
2. **Nada se omite**: al cierre, los 3,876 tienen análisis individual. La consulta de
   control: `WHERE decision='backlog' AND NOT detalle ? 'e6'` debe dar **0**.
3. Todo importado lleva fecha ORIGEN + lote reversible (`e6-*`) + redacción de secretos.
4. Ritmo por presupuesto: lo LOCAL ($0: extracción, hashes, magic bytes) sin límite; lo
   que gasta CUPO (visión de imágenes, destilado LLM) con presupuesto diario y gate.
5. Material original read-only. dry-run antes de cada fase. Batería al cierre de cada fase.

---

## 1 · LAS 6 FASES (ordenadas por valor/insumo)

### F1 · DOCX/PDF — el oro inmediato (52 archivos · 5.6 MB · $0 extracción)
**Qué son:** 6 docx de Genomad (economía GMD, modelo de negocio, servicios/tarifas,
breeding, MVP, agents) · guiones de sesiones 2-5 (teleprompter) · FRUTERITO-SISTEMA/
HISTORIAL/CHECKPOINTS .docx · 8 PDFs de media.
**Proceso POR ARCHIVO:**
1. Extraer texto (python-docx / pypdf en contenedor efímero — se instalan en el momento).
2. **Dedup por CONTENIDO contra lo ya importado**: muchos docx son la versión Word de un
   .md YA dentro (FRUTERITO-SISTEMA.docx ↔ .md) → si el texto es ≥90% igual, veredicto
   `duplicado-contenido` (no re-importar; registrado). Si difiere, se importa LO NUEVO.
3. Redactar secretos → episodio con fecha origen (lote `e6-docs`) → manifiesto.
4. Ficha individual: nombre · qué es · veredicto · si entró y por qué.
**Entregable:** 52 fichas + los episodios nuevos. **Esfuerzo:** 1 sesión. **Cupo:** ~$0.

### F2 · "OTROS" — triage forense que ENCOGE el problema (1,645 · 17 MB · $0)
**Qué son:** sin-extensión (muchos de `media/inbound` con nombres uuid — pueden ser
imágenes o docs SIN extensión), .bak, .tmp, .sample, .lock, .gitignore…
**Proceso POR ARCHIVO:**
1. **Magic bytes** (tipo REAL, no la extensión): un sin-extensión puede ser JPEG→ va a F4,
   texto→ se lee y clasifica aquí mismo, zip/docx→ F1.
2. `.bak`: diff contra su original — si difiere, extraer SOLO lo único; si no, duplicado.
3. `.sample`/.tmp/.lock/0-bytes: veredicto individual `basura-confirmada` (uno a uno, no
   por patrón ciego — se registra qué ES cada uno).
4. Texto hallado con valor → episodio (lote `e6-otros`).
**Nota:** esta fase RECLASIFICA — al terminar, los conteos de F1/F4 crecen con lo que
estaba escondido sin extensión. **Esfuerzo:** 1 sesión. **Cupo:** $0.

### F3 · CÓDIGO — catálogo de reconstrucción archivo por archivo (591 · 2.6 MB)
**Regla LOCKED:** el código NO se memoriza como código (se reconstruye aparte). Pero
Brian quiere CADA archivo analizado → el entregable es el **CATÁLOGO**:
**Proceso POR ARCHIVO:** ruta · proyecto al que pertenece · qué hace (por nombre + head
del archivo + imports; LLM ligero SOLO para los ambiguos) · estado (completo/fragmento) ·
¿vale reconstruirlo?
**+ 1 episodio-RESUMEN por PROYECTO** (godinez-ai, regenmon, meetup, smart-router,
token-saver, aws-persistence, temp-reporte…) → la memoria sabe QUÉ código existió y qué
hacía, sin cargar el código.
**Entregable:** `work/Entrenamiento_Catalogo_Codigo.md` (591 filas) + ~10 episodios-resumen.
**Esfuerzo:** 1-2 sesiones. **Cupo:** bajo (LLM solo en ambiguos).

### F4 · FOTOS/IMÁGENES — visión una por una, con presupuesto (1,402 · 124 MB · LA CARA)
**Qué son:** 1,234 jpg + png de `media/inbound` — lo que Brian mandó por Telegram
(pizarras, pantallas, eventos, documentos fotografiados).
**Proceso en 2 pasos:**
1. **Triage local $0 (todas):** dimensiones, tamaño, fecha, duplicado-perceptual (hash de
   imagen), y CONTEXTO — correlacionar el uuid del archivo con el mensaje de la sesión
   donde se mandó (la conversación ya está en memoria → sabemos QUÉ se hablaba cuando se
   mandó cada foto). Clasificar: screenshot-con-texto / documento-fotografiado / foto-evento
   / meme-trivial.
2. **Visión LLM UNA POR UNA (solo las que valen):** screenshots y documentos primero →
   descripción + texto extraído → episodio con fecha origen + contexto (lote `e6-fotos`).
   Fotos de eventos → descripción breve. Triviales → veredicto individual `sin-valor`.
   **PRESUPUESTO:** ~100-150 imágenes/día (vigilando el pin de cupo, horario valle),
   **GATE Brian tras el triage**: ver el desglose (cuántas de cada clase) y aprobar
   cuáles clases pasan a visión. Estimación: si ~40% valen → ~550 × visión ≈ 4-6 días
   de presupuesto tranquilo.
**Esfuerzo:** triage 1 sesión + visión repartida. **Cupo:** el mayor del plan → gate.

### F5 · AUDIO/VIDEO — transcripción local (4 archivos · $0)
2 notas de voz .ogg + 1 .mp4 + 1 extra: **faster-whisper CPU** en contenedor efímero
(modelo small, local, $0) → transcripción → redactar → episodio con fecha origen (lote
`e6-av`). El mp4: extraer audio (ffmpeg) → mismo tubo + 2-3 frames a visión si aporta.
**Esfuerzo:** media sesión.

### F6 · CIERRE E6
1. Verificación de cobertura: **0 archivos backlog sin `detalle.e6`** (la prueba del
   "nada omitido", igual que el manifiesto lo fue en E5).
2. Re-embeber lotes e6-* → noches de CLS digieren lo nuevo.
3. Examen de conocimiento E6 (preguntas sobre los docx Genomad, una foto-pizarra, el
   catálogo de código). 4. Batería §5-BIS + bitácora + commit firmado.

---

## 2 · ORDEN Y CALENDARIO PROPUESTO

| Fase | Qué | Esfuerzo | Cupo | Gate Brian |
|---|---|---|---|---|
| F1 docx/pdf | 52 uno a uno | 1 sesión | ~$0 | ver fichas |
| F2 otros/triage | 1,645 uno a uno | 1 sesión | $0 | ver reclasificación |
| F3 código | 591 → catálogo | 1-2 sesiones | bajo | ver catálogo |
| F4 fotos | 1,402: triage $0 → visión presupuestada | 1 + varios días | **ALTO** | ⭐ tras triage: qué clases pasan a visión |
| F5 audio | 4 | media sesión | $0 | — |
| F6 cierre | cobertura 0 + examen | media sesión | bajo | veredicto final |

**Total: ~4-5 sesiones de trabajo + la visión de fotos repartida en días** (por el cupo).
Al terminar: **asimilación textual y visual ≈ 100%** de lo asimilable — los 11,664 con
análisis individual real, no por encima.

## 3 · MECÁNICA (reusa el tubo del hito)

- Módulo nuevo `entrenamiento_backlog.py` (comandos: `e6-docs`, `e6-triage`, `e6-codigo`,
  `e6-fotos-triage`, `e6-fotos-vision <n>`, `e6-av`, `e6-cierre` — todos dry-run default).
- Contenedor efímero con material :ro (+ KEK solo si toca vault). Progreso en el
  manifiesto (`detalle.e6`) → reanudable en cualquier punto, auditable archivo por archivo.
- Reversible: lotes `e6-docs`/`e6-otros`/`e6-fotos`/`e6-av` (misma reversa demostrada de E0).
- Riesgos: docx corruptos (defensivo: ficha "ilegible", no rompe) · visión cara (presupuesto
  + gate) · fotos con secretos visibles (la visión REDACTA igual que el texto: si ve un
  token/password en un screenshot → `[SECRETO visible en imagen]`, nunca se transcribe).

*Cruza con: `work/Plan_Implementacion_Entrenamiento.md` (E0-E5b) · `work/Entrenamiento_Ejecucion_Reporte.md` ·
manifiesto en BD de brian. ⛔ Arranca fase por fase con orden de Brian.*
