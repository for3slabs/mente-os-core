# 📊 Registro de Conversaciones — telemetría de sesiones de Claude Code

> **Qué es:** el historial clínico de cada conversación (sesión) de Claude Code de este proyecto:
> cuándo inició/cerró, peso, temas, problemas, y **en qué momento el consumo empezó a crecer de
> forma excesiva o aparecieron cosas raras**. Nació del incidente del jueves 9-jul (3 mensajes →
> 100% del cupo) — la sesión monstruo nos enseñó que sin telemetría no se ve venir.
>
> **⚡ REGLA (en CLAUDE.md, obligatoria):** cuando Brian dé `/clear`, ANTES de cerrar se registra
> aquí la sesión que muere: fila en la tabla + sección con su autopsia. Sin registro no hay /clear.

**Owner:** Brian López · **Inicio del registro:** 2026-07-14 · **Capa:** Cerebro (telemetría)

---

## 🚦 Umbrales y señales de alerta (calibrados con datos reales)

| Señal | 🟢 Sano | 🟡 Vigilar | 🔴 Actuar (/clear ya) |
|---|---|---|---|
| Peso del jsonl | < 15 MB | 15-50 MB | > 50 MB |
| Contexto vivo por request | < 200K tokens | 200-500K | > 500K (con [1m]; a 1M cada cache-miss ≈ $) |
| Edad de la sesión | días | 1-2 semanas | semanas/meses sin /clear |
| Cache-miss (input o cache_write ≈ contexto completo) | esporádico | tras cada pausa | cada pausa >5 min con contexto grande |
| "Cosas raras" | — | respuestas que mezclan temas viejos | errores/límites (`<synthetic>`), cupo agotado |

**La física del costo:** el peso en disco NO es el problema directo — lo es el **contexto vivo**:
cada pausa mayor al TTL del caché (5 min default / 1h a veces) re-escribe TODO el contexto a precio
premium. Contexto de 1M = "hola" cuesta ~1M tokens. Contexto de 30K = centavos. Por eso: /clear al
cerrar bloques (RETOMAR.md guarda el estado, no se pierde nada).

---

## 📒 Índice de sesiones

| # | ID (corto) | Inicio | Fin | Peso | Msjs Brian | Contexto máx | Veredicto |
|---|---|---|---|---|---|---|---|
| S1 | `2a5131d3` | 2026-05-28 | 2026-07-13 | **278 MB** 🔴 | ~2,900 turnos | **~985K tokens** 🔴 | LA MONSTRUO — causó el incidente del jueves |
| S2 | `3f5bbe0d` | 2026-07-13 20:28 | 2026-07-14 06:03 | 3.4 MB 🟢 | ~26 | **549K 🔴** | Maratón H13+Frente B — productiva; /clear al cruzar el umbral rojo de contexto |
| S3 | `c9ef4299` | 2026-07-14 ~11:00 | 2026-07-15 (activa) | 8.7 MB 🟢 | ~40 | ~n/d | **La jornada MERCADO** — v0.17.0: Frente B F4-F6 + Molde For3s Inside (M1-M4) + For3s Trace completo + panel temporal. ~22 commits, ~10 bugs (1 SEC grave). Sana; sin señales raras |

### S3 · `c9ef4299` — la jornada MERCADO (v0.17.0)
- **Temas:** arranque en Frente B F4 (panel admin Railway) → F5 carga (2000 conc, 2 races cazados) →
  F6 estándar datos + /v1/olvidar. Luego **Molde For3s Inside** (M1 contrato · M2 SDK · M3 onboarding
  · M4 trazabilidad) con auditoría caza-bugs (🔴 SEC: inyección LIKE en /v1/olvidar, EXPLOTADO+fix).
  Luego **For3s Trace** completo (T1 vocabulario · T2a-c recibir/analizar/alertar · alertas ricas con
  punto exacto en el panel · T3 ejemplo). Panel: uso por temporalidad. Duda del GIL resuelta.
- **Salud de la sesión:** 8.7 MB (🟢 <15), sin `<synthetic>`, sin mezcla de temas viejos, sin cupo
  agotado. Muchos rebuilds del contenedor (esperados). Consumo estable — no creció excesivo.
- **Cierre:** v0.17.0 commiteada, tríada `ccc3fb0`, Mente OS actualizado (Bitácora + RETOMAR
  comprimido a 193 líneas + CLAUDE.md + 3 memorias nuevas). Listo para /clear si Brian lo pide.

---

## S1 · `2a5131d3` — LA SESIÓN MONSTRUO (28-may → 13-jul-2026, 47 días)

- **Peso final:** 278 MB · 53,907 líneas · ~35 días activos. 21× más grande que cualquier otra.
- **Temas (toda la vida del proyecto):** rondas de diseño R1-R10 → construcción C0-C1 → hitos
  H1-H12 → contenerización → profesionalización PR1-PR10 → rediseño memoria → identidad viva →
  multi-instancia → entrenamiento E0-E6 → canal API → Incubathon → post-Incubathon.
- **📈 Cuándo empezó el crecimiento excesivo (autopsia por fases):**
  - **28-may → 8-jun:** sana. Modelo opus-4-7, contexto chico, cache-reads < 100M/día.
  - **9-jun:** primer salto — cambio a opus-4-8 + días de 300M tokens de cache-read. Señal 🟡.
  - **14-jun en adelante:** días de ~500M cache-read; el contexto por request crece sin freno
    (la ventana [1m] permite crecer sin compactar — nunca hubo /clear).
  - **3-jul (pico):** 918M tokens de cache-read en UN día.
  - **8-jul:** contexto vivo ~915K tokens. Cada mensaje arrastraba una novela.
  - **🔴 9-jul (EL INCIDENTE):** 5 cache-misses de ~935-980K tokens c/u (03:10 · 04:43 · 18:01 ·
    19:37 · 19:51) porque el TTL era 5 min y cada pausa re-escribía TODO. Los 3 fatales de la
    tarde: "hola" (970K) → "define for3s" (975K) → "oye estoy ocupando el bot" (980K + error =
    **cupo agotado, día perdido**). Equivalente API del día: >$100-200. El /model a fable-5 fue
    DESPUÉS, ya sin cupo.
- **Cosas raras detectadas:** respuestas lentas al final · el error `<synthetic>` (límite) ·
  compactación forzada 23:14 del 9-jul ("ran out of context").
- **Problema raíz (3 factores):** 47 días sin /clear + ventana [1m] sin compactación + TTL 5 min.
- **Descartado con evidencia:** NO proceso de fondo, NO entrenamiento nocturno (cero requests en
  huecos idle). Forense completo: PENDIENTES §Frente A + memoria `feedback_moderar_consumo_sesion`.
- **Cierre:** /clear el 2026-07-13 ~14:28. El archivo queda en disco como evidencia histórica.

## S2 · `3f5bbe0d` — Maratón H13 DEVUELVE + Frente B (13-jul 20:28 → 14-jul 06:03, ~10h)

- **Peso:** 3.4 MB · 1,214 líneas · ~26 mensajes de Brian (+ trabajo autónomo MUY intensivo).
- **Consumo:** cache_write 4.0M · cache_read 170M · output 941K. **Contexto máx 549K 🔴** —
  cruzó el umbral rojo (500K con [1m]) al final; por eso el /clear ANTES de F4 (bloque grande nuevo).
- **Temas:** Frente A cerrado (forense del incidente del jueves) → **HITO H13 "DEVUELVE" completo
  F0→F5** (v0.16.0: mina + digest + por-cierto contextual + feedback) → fix BUG-EQUIPO sellado +
  push (`06c5f99`) + 4 instancias a v0.16.0 → creación de ESTE registro (regla /clear) → **FRENTE B
  F0-F3**: Ronda del puente de mercado (13 bugs + comparativo túneles) · F1 demo con URL FIJA
  (Tailscale Funnel `for3s.tail6749e5.ts.net`, `2bf4a99`) · F2 control de acceso preciso
  (estados/keys f3k_/scopes, `79b156d`) · F3 cuotas + metering persistente (`330b891`).
- **📈 Consumo excesivo:** creció linealmente por el maratón (nada anómalo — trabajo real denso);
  el contexto pasó de ~430K (H13) a 549K (Frente B). Sin cache-misses catastróficos.
- **Cosas raras:** ninguna del sistema. Bugs de MIS scripts de prueba (heredoc que escapó comillas
  — el que advierte el Método F — y chr() enredado); resueltos con archivos + scp. TTL caché 1h.
- **⚠️ NOTA:** Brian reactivó `claude-fable-5[1m]` a mitad (el modelo caro del incidente) → razón
  extra para el /clear con contexto ya en 🔴.
- **Cierre:** /clear tras este registro, ANTES de arrancar F4 (panel admin). RETOMAR.md fresco.
  6 commits del Frente A/B en server SIN push (H13 ya pusheado en 06c5f99).

---

## 📋 Plantilla para registrar una sesión (copiar al cerrar)

```markdown
## SN · `<id-corto>` — <apodo> (<inicio> → <fin>)
- **Peso:** X MB · N líneas · ~N mensajes de Brian.
- **Consumo:** cache_write · cache_read · output · contexto máx por request.
- **Temas:** qué se trabajó (bloques grandes).
- **📈 Consumo excesivo:** ¿cuándo empezó a crecer? ¿hubo cache-misses grandes? (si fue sana: "no").
- **Cosas raras:** errores, lentitud, mezcla de temas, límites (si nada: "ninguna").
- **Cierre:** por qué se cerró (fin de bloque / peso / incidente) + RETOMAR actualizado ✓.
```

> **Cómo medir** (comando de referencia): el jsonl vive en
> `~/.claude/projects/-home-brianweb3-for3s/<id>.jsonl` — peso con `ls -lh`, y tokens/contexto
> leyendo los campos `usage` de los mensajes assistant (script en la memoria del incidente).
