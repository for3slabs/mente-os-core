# 📸 E6-F4 · Runner de tandas de VISIÓN de fotos (reanudable)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Entrenamiento_E6_Fotos_Runner_Tandas.md → memory/archive/Entrenamiento_E6_Fotos_Runner_Tandas.md (2026-07-30, ADR-029)

> **Qué es:** el mecanismo para procesar las **974 fotos** del backlog E6 por tandas de visión LLM.
> Reanudable (cada foto se marca en el manifiesto; las hechas se saltan solas). Documentado
> 2026-07-16 al arrancar la 1ª tanda. **Cruza con:** `work/Plan_Backlog_Profundo_E6.md` §F4.

---

## 1 · Estado (actualizar tras cada tanda)

- **✅✅ BACKLOG VACÍO 2026-07-18. Con visión: 1169 · Pendientes: 0.** (El total subió de 974 a 1169
  candidatas conforme se procesaban; TODAS con visión ahora.)
  **Sesión 2026-07-18:** 481→1169 con visión = **~688 fotos en el día**, TODAS 0 fallos. ~8 tandas de 100
  encadenadas. Cupo nunca tocó el freno (0.92); la ventana 5h se renovó varias veces (bajó a 0.07 al final).
  **Aprendizajes:** (1) bug /material §1-BIS resuelto. (2) el encadenador (watch en la sesión) muere si se
  cae el internet de Brian → el procesamiento en el server sigue, pero hay que re-armar el watch. (3) bug del
  watch: buscar "FREN" en el FIN daba falso positivo; correcto = leer `FIN (COMPLETA|FRENADA)` exacto.
  **Estado: hito de fotos E6 CERRADO.**
- Modelo: sonnet-4-6. Pausa 6s entre fotos. **Ritmo real: ~55s/foto** → tanda de 100 ≈ **~90 min**.
- **⚠️ CUPO — dato REAL de la tanda 1 (corregido):** 100 fotos subieron el **5h de 0.37→0.61 (~+0.24)**
  y el 7d de 0.33→0.36 (~+0.03). O sea: **100 fotos ≈ 24% de la ventana de 5h.** NO es despreciable
  (mi estimación inicial de "casi no se mueve" fue con pocas fotos, incorrecta). **Regla: máx 1 tanda
  de 100 por ventana de 5h, o tandas de 50, para no agotar el cupo de los bots.** El 7d aguanta bien.

## ⚠️ 1-BIS · BUG CAZADO 2026-07-17 (no repetir): FALTA montar /material
El runner busca las fotos en `/material/<BASE>/<ruta>` (BASES: `Fruterito-principal`, `Fruterito-wsl`).
Si NO montas el volumen, TODO da `FileNotFoundError` (0 procesadas, 0 cupo — el freno ni se activa).
**Las fotos viven en el host en `~/entrenamiento/`** → el montaje obligatorio es:
`-v ~/entrenamiento:/material:ro`. Comprobado: dentro del contenedor el archivo queda visible en
`/material/Fruterito-principal/media/inbound/file_*.jpg`.
**Además:** lanzar UNO solo con `--name tanda-fotos-e6` en modo `-d` (evita duplicados = doble cupo;
nombre fijo para no confundir cuál matar). Verificar `docker ps | grep -c run_tan == 0` antes de lanzar.

## 2 · Cómo lanzar UNA tanda (server, síncrona — NO de fondo)

La función es `entrenamiento_backlog.e6_fotos_vision(pool, material, limite=N, pausa=6.0)`. Se corre
en un contenedor EFÍMERO con el material montado read-only y la BD de brian. El runner
(`run_tanda_fotos.py`, en el scratchpad de la sesión) reporta pendientes + cupo antes/después.

```sh
# en el server, con la password/token del .env de brian:
POSTGRES_PASS=$(grep POSTGRES_PASSWORD ~/.for3s/brian/.env | cut -d= -f2-)
ANTH=$(grep -E '^ANTHROPIC_TOKEN=' ~/.for3s/brian/.env | cut -d= -f2-)
[ -z "$ANTH" ] && ANTH=$(grep -E '^ANTHROPIC_TOKEN=' ~/.for3s/.env | cut -d= -f2-)

docker run --rm --network for3s-brian_default \
  -e DATABASE_URL="postgresql://for3s:${POSTGRES_PASS}@postgres:5432/for3s" \
  -e ANTHROPIC_TOKEN="$ANTH" \
  -e FOR3S_STATE_HOME=/app/.for3s \
  -v /home/brianweb3/entrenamiento:/material:ro \
  -v /home/brianweb3/.for3s/brian:/app/.for3s:ro \
  -v /tmp/run_tanda_fotos.py:/tmp/run_tanda_fotos.py:ro \
  --entrypoint python for3s-agent:local /tmp/run_tanda_fotos.py
```

- **Reanudable:** el WHERE de `e6_fotos_vision` filtra `NOT (detalle->'e6' ? 'vision')` → cada corrida
  toma las siguientes N sin hacer. Si se corta a mitad, lo hecho queda; la próxima sigue donde iba.
- **NO dejar de fondo** que sobreviva al cierre de la sesión (regla anti-cuota). Vigilar con Monitor
  hasta que el contenedor efímero desaparezca.
- **Redacta secretos visibles:** si la visión ve un token/password en una imagen → `[SECRETO VISIBLE]`,
  nunca lo transcribe (verificado en el prompt + `redactar()`).

## 3 · Verificar el progreso / estado

```sh
# pendientes de visión (candidatas sin procesar):
docker exec for3s-brian-postgres-1 psql -U for3s -d for3s -tAc \
  "SELECT count(*) FROM import_manifiesto WHERE decision='backlog' \
   AND detalle->'e6'->>'clase' ILIKE '%candidata visión%' \
   AND NOT (detalle->'e6' ? 'vision')"

# fotos YA con visión (episodios del lote e6-fotos):
docker exec for3s-brian-postgres-1 psql -U for3s -d for3s -tAc \
  "SELECT count(*) FROM import_manifiesto WHERE decision='importado' AND lote_id='e6-fotos'"
```

## 4 · Bitácora de tandas

| # | Fecha | Fotos | Tiempo | Cupo (5h Δ) | Notas |
|---|---|---|---|---|---|
| 1 | 2026-07-16 | 100/100 ✅ | ~90 min | **+0.24** (0.37→0.61) | 0 fallidas · calidad alta (Godínez Studio, BotFather, genomad) · sin secretos · quedan 874 |
| 2 | 2026-07-16 | 50/50 ✅ | ~45 min | **+0.07** (0.63→0.70) | 0 fallidas · sin secretos · 345/974 |
| 3 | 2026-07-16 | 7 (cortada) | — | — | corté para lanzar tanda con freno |
| 4 | 2026-07-17 | 100/100 ✅ (con freno 0.92) | ~90 min | 0.76→0.91 | 🐛 1er intento falló por import 'redactar' (era entrenamiento_olas, no text_normalize) → corregido |
| 5 | 2026-07-17 | ~29 (freno 0.97) | ~25 min | 0.91→0.97 | freno protegió el cupo · **481/974 con visión, 688 pendientes** · paramos por hoy |

**🛡️ SALVAGUARDA (2026-07-17):** runner oficial ahora es `run_tanda_freno.py` (freno de cupo por ENV
`FOR3S_FRENO_CUPO_5H`, default 0.92) — para SOLO cuando el cupo 5h llega al límite, para NO dejar a
Brian sin bots. Evita el susto del Incubathon. Úsalo siempre en vez del `run_tanda_fotos.py` sin freno.

## 5 · Al terminar TODAS las 974

Cuando `pendientes = 0`: re-embeber el lote e6-fotos (las noches de CLS lo digieren al grafo) +
seguir con E6-F5 (audio) + F6 cierre (cobertura 0 sin `detalle.e6` + examen) + version bump.

---

Relacionado: `work/Plan_Backlog_Profundo_E6.md` (el plan) · `work/Entrenamiento_Ejecucion_Reporte.md`
· [[project_hito_entrenamiento]] · [[feedback_no_loops_espera_servidor]] (por qué NO de fondo).
