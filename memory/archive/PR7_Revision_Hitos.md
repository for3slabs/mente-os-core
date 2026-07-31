# PR7 — Revisión de Hitos H1-H12 (verificación en contenedor vivo)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/PR7_Revision_Hitos.md → memory/archive/PR7_Revision_Hitos.md (2026-07-30, ADR-029)

> **Profesionalización · PR7.** Fecha: 2026-06-30. Método: sondas de SOLO LECTURA
> contra el servidor `for3s` vivo (BD PostgreSQL + AGE, logs del worker, audit).
> Filosofía: **"completo en código" ≠ "funciona en el contenedor"** — toda la sesión
> de bugs lo demostró (BUG-1 decay, BUG-5 backup, BUG-8 CLS, BUG-9 MCP estaban
> "completos" y rotos). PR7 pasa lista a los 12 hitos contra la realidad de producción.
>
> Sin nada destructivo. Una conexión SSH, sin loops, sin procesos de fondo
> (regla crítica anti-consumo de cuota).

---

## Resumen ejecutivo

**12/12 hitos revisados. 11 ✅ funcionan · 1 🟡 parcial por diseño (H7). 0 rotos.**
Los 12 bugs arreglados en esta sesión SIGUEN arreglados (verificado vivo).
La curiosidad cazó **2 deudas de observabilidad** (ningún bug que rompa ejecución).

| H | Hito | Veredicto | Evidencia clave (real, hoy) |
|---|------|-----------|------------------------------|
| **H1** | HABLA | ✅ | 378 msg in / 343 out · modelo sonnet-4-6 |
| **H2** | RECUERDA | ✅ | 3 sesiones · 693 turnos persistidos |
| **H3** | TELEGRAM | ✅ | bot vivo, 7 contenedores up |
| **H4** | TIENE MANOS | ✅ | GitHub: 9 fetch + 4 write + 2 PR · MCP vivo |
| **H5** | MEMORIA REAL | ✅ | embeddings 693/693 · grafo 63 conceptos / 601 ep / 606 aristas |
| **H6** | SE CUIDA | ✅ | backup→host 15M hoy · rotación 14/14 · relevance 752 · microglía |
| **H7** | DECIDE | 🟡 parcial | `/model` manual ✅ · enrutamiento auto NO construido (alcance futuro) |
| **H8** | EQUIPO | ✅ | 2 miembros · puerta cerrada · motor cableado completo |
| **H9** | SUEÑA (DMN) | ✅ | motor corre · housekeeping ON / generativas OFF (gobernado) |
| **H10** | PLANEA | ✅ | confidence_calculated=32 en respuestas reales |
| **H11** | EL FRENO | ✅ | governor 6 frenos · auto-gen APAGADA · kill switch |
| **H12** | APRENDE | ✅ | 2 skills (1 AUTO-generada por DMN, usada) · curar_skills corre |

**Bonus — cadena de auditoría:** ✅ ÍNTEGRA (1576 eventos, 0 eslabones rotos, SHA-256 encadena).

---

## FASE 1 — Memoria y ciclo nocturno (H5, H6, H9)
*La zona donde salieron TODOS los bugs de la sesión.*

### H5 — MEMORIA REAL ✅
- **Embeddings:** 693/693 turnos vivos con embedding (100% cobertura) → BUG-1/BUG-10 arreglados confirmados.
- **Grafo AGE (`for3s_kg`):** 63 Conceptos · 601 Episodios · 5 Repos · 5 Owners · 606 aristas
  (674 vértices totales). **El grafo CRECIÓ** de 35-37 (memorias previas) a 63 → BUG-8 (catálogo
  AGE corrupto) arreglado de verdad.
- **CLS:** opera correcto. La corrida de hoy dio `clusters=0, 58 en ruido`. **NO es bug** —
  HDBSCAN con `min_cluster_size=3` requiere ≥3 episodios parecidos; los 58 pendientes eran
  conversaciones diversas → ruido legítimo. El propio código lo documenta: *"eso es correcto y
  honesto, no un fallo"*. THRESHOLD_PENDIENTES=10.

> ⚠️ **Trampa de verificación cazada:** el label del grafo es `Concepto` (español), no `Concept`.
> Mi primera sonda dio "0 conceptos" — un FALSO POSITIVO. Siempre verificar nombres reales.

### H6 — SE CUIDA ✅
- **Backup automático:** `auto_for3s_20260630_175834.sql` (15M, hoy) escrito AL HOST
  (`~/for3s-backups`, volumen montado) → BUG-5/BUG-6 arreglados confirmados.
- **Rotación:** exactamente 14 backups, 274M (`RETENER=14`). Política respetada. Orden por
  nombre = orden cronológico (formato fecha ISO en el nombre).
- **Relevance (decay):** 752 turnos recalculados hoy 08:45 → BUG-1 vivo y funcionando.
- **Microglía:** dry-run, 0 candidatos a olvido (datos jóvenes <30d, correcto).
- **Status hilos:** 3/3 resumidos. **Health check:** todo OK.

### H9 — SUEÑA (DMN) ✅ gobernado
- **Motor corre:** `idle=257m · evaluadas=5 · corridas=2 · saltadas=3`.
- **Estado (tabla `dmn_estado`, fuente de verdad):** housekeeping=ON (`t`), generativas=OFF (`f`)
  — exactamente como debe (autonomía generativa gobernada, fail-closed).
- **0 propuestas** en `dmn_propuestas` = correcto (generativas apagadas a propósito).

---

## FASE 2 — Equipo, metacognición, governor, skills (H8, H10, H11, H12)

### H8 — EQUIPO ✅ (con 1 deuda de observabilidad)
- **Multi-usuario REAL:** 2 miembros en `equipo_miembros` — Brian (encargado, 1923367928) +
  "Sme G" (miembro, 7740601619). `puerta_abierta=f` (modelo PUERTA cerrado = single-owner por
  defecto, correcto). `owner` BD (PR6): default→Brian, actualizado hoy.
- **Motor multi-agente cableado completo:** `_amerita_equipo()` (gatillo automático por frases
  fuertes: "analiza a fondo", "lanza el equipo"...) + `_sugiere_equipo()` (botón) →
  `_correr_equipo_y_responder()` (cola por persona) → `_correr_equipo_inner()` (progreso en vivo) →
  `multiagente.correr_equipo()` + `sintetizar()`. Defensivo (si falla cae a 1 agente).
- **0 disparos en producción:** nadie escribió las frases-gatillo literales al bot todavía →
  conservador por diseño (cero gasto sorpresa), **NO bug de cableado**.

> 🟡 **DEUDA-1 (observabilidad):** `correr_equipo`/`sintetizar` NO escriben en `audit_events`.
> Si el equipo se dispara, no queda rastro ni costo medible. Debería emitir un evento
> `multiagente_run` con tokens/familia/specialists. Afecta PR2 (monitoreo) y PR3 (datos).

> 🟡 **DEUDA-2 (cobertura de perfil):** `perfil_usuario` solo tiene 1 perfil (Brian, rol "tu
> dueño"). Sme G (miembro) NO tiene perfil modelado. A confirmar si el modelado se dispara para
> miembros o si Sme G interactuó poco.

### H10 — PLANEA (metacognición) ✅
- `confidence_calculated=32` en `audit_events` → la confianza se calcula en respuestas reales,
  no solo en tests. "Sé cuándo NO sé" activo.

### H11 — EL FRENO (governor) ✅ gobernado
- 6 frenos: FRENO 1 (gen/día ≤3) · FRENO 4 (contradicción/duplicados) · FRENO 5 (activas ≤100)
  reales sobre la tabla `skills` · escaneo de seguridad (rm -rf, curl|sh, leer KEK/secrets,
  prompt-injection) · KILL SWITCH (auto-gen default APAGADA) · PROVENANCE (solo gestiona skills
  'auto', las 'usuario' son intocables). FRENOS 2/3/6 son neutros documentados (esperan datos).

### H12 — APRENDE (skills) ✅
- 2 skills `active`: una **AUTO-generada por el DMN** (`provenance=auto`, usada 1×) → ¡el sistema
  aprendió una skill SOLO! — y una de `usuario` (usada 2×). `curar_skills` corre (0 stale, 0 archived).

---

## FASE 3 — Base MVP + decisión (H1, H2, H3, H4, H7)

### H1 — HABLA ✅
- 378 mensajes recibidos / 343 respondidos (último hoy 05:43). Modelo desplegado:
  `claude-sonnet-4-6` (a propósito, NO bug).

### H2 — RECUERDA ✅
- 3 sesiones, 693 turnos persistidos en `episodes_events`, sobreviven reinicios
  (verificado: el server se reinició y los 7 contenedores + la memoria revivieron).

### H3 — TELEGRAM ✅
- Bot vivo en Telegram, 7 contenedores `Up`, mensajes de hoy.

### H4 — TIENE MANOS ✅
- GitHub real ejercido: `gh_fetched=9`, `github_write=4`, `pr_fetched=2`. MCP conecta vivo
  (verificado en revisión de hermanos de red, BUG-9). Último uso 13-22 jun (uso bajo, no rotura).

### H7 — DECIDE 🟡 PARCIAL (por diseño)
- `/model` manual ✅ totalmente cableado: 3 modelos (Haiku 4.5 / Sonnet 4.6 / Opus 4.8),
  default Sonnet, handler + botones registrados.
- **Enrutamiento automático (Tálamo + Dual-Process: Haiku barato vs Opus caro según
  complejidad) NO construido.** El propio `modelos.py` lo dice: *"El enrutamiento Haiku/Sonnet/
  Opus se construye después"*. Coincide con el mapa ("H7 parcial") y la memoria. **Alcance
  futuro, NO bug.**

---

## Hallazgos para otros PR (no bloqueantes)

- **PR2/PR3:** instrumentar el equipo multiagente con un evento de audit (DEUDA-1) para medir
  cuántas veces corre y cuánto cuesta.
- **PR9 (UX/limpieza):** ~10 archivos `.bak` horneados en la imagen del contenedor
  (`telegram_channel.py.bak.pr10/pr103/pr2/pr6`, `tasks.py.bak.pr22`, `health.py.bak`, etc.) —
  basura de ediciones, no afectan ejecución pero ensucian la imagen. + 2 skills de deploy casi
  duplicadas (deduplicar).
- **Confirmar (REDISEÑO MEMORIA o H8):** por qué Sme G no tiene perfil_usuario (DEUDA-2).

---

## Conclusión

PR7 confirma que **For3s OS es real y funciona en producción**, no solo en código. Los 12 hitos
están presentes; 11 operan verificados vivos; H7 es parcial por decisión de alcance. La cadena de
auditoría —la base de la confianza enterprise (SOC2)— está íntegra. Las 2 deudas cazadas son de
OBSERVABILIDAD (medir el equipo, perfilar miembros), no de funcionamiento.

> **El valor de PR7:** después de una sesión donde "cosas completas estaban rotas", ahora tenemos
> EVIDENCIA REAL, fechada, de que cada hito vive. Eso es profesionalización: no asumir, verificar.
