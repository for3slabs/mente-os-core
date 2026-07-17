# 📋 PLAN DE IMPLEMENTACIÓN — HITO ENTRENAMIENTO (a profundidad, por LÍNEA DE TIEMPO)

> **Fecha:** 2026-07-05 · **Estado:** PLAN — ⛔ nada ejecutado (arranca cuando Brian dé la orden)
> **Ejecuta el flujo:** `Flujo_Extraccion_Entrenamiento.md` (FE0–FE8) — este plan lo ORDENA
> en etapas ejecutables con la instrucción nueva de Brian: **extracción CRONOLÓGICA, de lo
> más antiguo a lo más actual, siguiendo una línea de tiempo para que no existan fallos.**
> **Meta:** 6 agentes OpenClaw → 1 For3s OS (@For3s_Brian_bot). TODO analizado y asimilado.

---

## 0 · LA IDEA RECTORA: importar en el ORDEN en que se vivió

**Descubrimiento que valida la instrucción de Brian:** los agentes OpenClaw NO fueron
secuenciales — fueron CONTEMPORÁNEOS (main, dev, watchdog, empleado convivieron feb→abr
2026, hablando de los mismos proyectos). Si importáramos agente-por-agente, la memoria de
brian recibiría abril de dev ANTES que febrero de main → conceptos sin sus causas,
consolidación desordenada, contradicciones temporales = FALLOS.

**Por eso el import es UNA sola línea de tiempo GLOBAL** (todas las fuentes mezcladas,
ordenadas por fecha real de origen), en OLAS cronológicas. Así la memoria de brian crece
como una vida vivida: cada noche el CLS consolida un periodo ANTES de que llegue el
siguiente — exactamente como un cerebro que duerme entre días. Las etapas de
infraestructura (censo, secretos, identidad, skills) sí son por-etapa porque no son
memoria episódica.

```
INFRA (E0-E2)            LÍNEA DE TIEMPO (E3: olas 1→N)                CIERRE (E4-E5)
censo TOTAL de las       ┌──────────────────────────────────┐          skills → examen
2 raíces + secretos  ──► │ ola feb → 🌙 → ola mar-1 → 🌙 →   │  ──►    global → microglía
al vault + identidad     │ ola mar-2 → 🌙 → ola abr → 🌙     │          ON → batería → docs
(el "lente") con gate    └──────────────────────────────────┘
                          cada 🌙 = noches de CLS/DMN digiriendo
```

---

## 1 · ETAPA E0 — INFRAESTRUCTURA Y RED DE SEGURIDAD (FE0 + construir el extractor base)

**Objetivo:** poder importar Y DESHACER, demostrado, antes de tocar nada real.

| Paso | Qué se hace | Verificación afirmativa |
|---|---|---|
| E0.1 | Backup completo BD brian (`pg_dump` etiquetado `pre-entrenamiento`) al host | restore de prueba en BD temporal |
| E0.2 | Migración **033** (import_manifiesto + import_lotes, aditiva) | migra en brian; Foresito NO la corre aún (le llegará con su ciclo normal) |
| E0.3 | Módulo `for3s_core/entrenamiento.py` v1: runner de etapas + dry-run default + logging a manifiesto | tests unitarios; ruff/ty verdes |
| E0.4 | **Prueba de reversa EN VACÍO**: lote de 3 episodios de juguete → aplicar → deshacer → BD byte-igual | diff de conteos + hashes antes/después |
| E0.5 | Decisión técnica de FE0: ¿columna aditiva `import_lote` en episodes_events o convención en contenido? (elegir la reversa más limpia) | documentada en el commit |

**Gate Brian E0:** ver la reversa funcionando. · **Esfuerzo:** 1 sesión de trabajo.

## 2 · ETAPA E1 — CENSO TOTAL + LÍNEA DE TIEMPO MAESTRA (FE1, read-only)

**Objetivo:** las DOS raíces completas (principal 5,786 + wsl 5,878 = 11,664 archivos) en
el manifiesto, CADA archivo con bloque, hash, duplicado-de… **y FECHA DE ORIGEN** — el
insumo de la cronología.

| Paso | Qué se hace |
|---|---|
| E1.1 | Walker sobre `/material` (:ro): las 2 raíces → manifiesto en BD (11,664 filas) |
| E1.2 | **Datación de cada unidad**: sesiones .jsonl → timestamp del PRIMER y ÚLTIMO mensaje (rango) · diarios → su fecha del nombre · docs → mtime + fecha interna si la hay · media → fecha de recepción. Se guarda `fecha_ini/fecha_fin` en `detalle` |
| E1.3 | Dedup por hash ENTRE raíces (main está en ambas; workspace-empleado comparte raíz .md) → `duplicado_de` |
| E1.4 | Detector de secretos v1 (ruta + contenido: `sk-`, `ghp_`, token Telegram, base64 largos, `password[:=]`, PEM, .env) → bloque=SECRETO. Los 47+ censados DEBEN caer (check contra radiografías) |
| E1.5 | Radiografía de `Fruterito-wsl` (la gemela pendiente) sale de este censo → doc en Mente OS |
| E1.6 | **REPORTE LÍNEA DE TIEMPO MAESTRA**: histograma mensual del material completo (¿cuánto material hay de cada mes, de qué agente?) → define las OLAS de E3 con datos, no a ojo |

**Gate Brian E1:** aprobar manifiesto (totales por bloque/decisión) + mapa de olas propuesto.
**Esfuerzo:** 1-2 sesiones. Cero escritura en memoria.

## 3 · ETAPA E2 — SECRETOS AL VAULT + IDENTIDAD (FE2 + FE3; el "lente" antes que los recuerdos)

**Por qué antes de la línea de tiempo:** (a) los secretos deben estar en el vault para que
las olas rediten `[SECRETO→vault:nombre]`; (b) la identidad es el LENTE con el que brian
interpretará las memorias — no es memoria episódica, es quién la recibe. No rompe la
cronología: no inserta episodios.

| Paso | Qué se hace | Gate |
|---|---|---|
| E2.1 | TODOS los secretos → vault cifrado de brian (nombres canónicos `oc.<agente>.<qué>`) + inventario legible para Brian (sin valores) | Brian revisa inventario |
| E2.2 | Parsear B1 (SOUL/IDENTITY/ETHICS/AGENTS/… de principal + los de wsl: empleado, for3s-design) → **borradores ADAPTADOS** de `persona/IDENTITY.md` + `REGLAS_USUARIO.md` + `mente-os/` de brian | ⭐ **Brian aprueba el borrador ANTES de escribirse** |
| E2.3 | USER.md + brian-prefs → propuestas de **perfil P1** (pipeline existente con gate) | gate P1 |
| E2.4 | HISTORIAL-COMPLETO / FRUTERITO-SISTEMA / MEMORY.md → unidades narrativas FECHADAS que se ENCOLAN para sus olas (no se insertan aquí — respetan la cronología) | — |

**Esfuerzo:** 1-2 sesiones (la adaptación de identidad es artesanal, con Brian).

## 4 · ETAPA E3 — ⭐ LA LÍNEA DE TIEMPO (FE4+FE5+FE7 fusionadas en OLAS cronológicas)

**El corazón del entrenamiento.** Cada OLA = un periodo (quincena/mes según el histograma
E1.6) con TODO el material de TODAS las fuentes de ese periodo, importado junto:

```
OLA k (ej. "2026-03 · 1ª quincena"):
 1. SELECT del manifiesto: unidades con fecha en el periodo (sesiones, diarios,
    docs, media-docs) de TODAS las fuentes, orden fecha_ini ASC
 2. dry-run del paquete → reporte (episodios/conceptos que generaría) → ojo humano
 3. aplicar por lotes (1 sesión-origen o ≤25 docs por lote, reversibles)
    · conversaciones: árbol→secuencia · cron-runs → 1 resumen/día · secretos
      redactados · toolResults truncados con criterio
    · diarios del periodo → episodios con su fecha · temáticas/learnings → grafo
    · docs del periodo → semántica + conceptos ligados a su proyecto
 4. re-embeber el lote (BGE local, sin gastar cupo LLM)
 5. 🌙 DEJAR 1-2 NOCHES: CLS consolida el periodo al grafo · DMN detecta patrones ·
    perfil/estilo infieren · (el cerebro digiere ANTES de la siguiente ola)
 6. EXAMEN de la ola: 5-10 preguntas sobre ESE periodo a @For3s_Brian_bot
    (generadas durante la extracción, con respuesta esperada) → 100% o se investiga
 7. marcar ola en manifiesto → commit de control
```

**Olas previstas** (se ajustan con E1.6): `pre-feb` (historia narrada del HISTORIAL) →
`feb-2026` (nacimiento: main/dev arrancan, archive feb, media feb) → `mar-1` → `mar-2`
(el pico: 20749 watchdog + 17096 dev viven aquí) → `abr-2026` (el final de la era OpenClaw).

**Reglas de ritmo:** máx 1 ola aplicada por día natural (las noches SON parte del método) ·
cupo OAuth compartido con Foresito → aplicar olas en horas valle y vigilar el pin ·
sin procesos de fondo: cada lote es un run puntual que termina.

**Esfuerzo:** ~5 olas × (1 aplicación + 1-2 noches) ≈ **1-2 semanas calendario** (trabajo
activo bajo; el reloj lo marcan las noches de consolidación — a propósito).

## 5 · ETAPA E4 — SKILLS (FE6, el estado final destilado)

Después de la línea de tiempo (las skills son el RESULTADO destilado de esa historia, y el
matcher funciona mejor con el grafo ya poblado): las 16 de principal + mode_* de wsl →
una por una: leer → destilar → gate Brian (¿skill H12 viva / conocimiento al grafo /
descartar?) → crear con embedding + procedencia. Scripts → backlog_herramientas.md.
**Esfuerzo:** 1-2 sesiones.

## 6 · ETAPA E5 — CIERRE GLOBAL (FE8 sobre TODO)

1. **Manifiesto: 0 filas sin decisión** en las 2 raíces (la prueba del "absolutamente todo
   analizado y asimilado" — cada uno de los 11,664 archivos tiene destino registrado).
2. **Examen GLOBAL** (~40 preguntas cruzando periodos y fuentes: historia, proyectos,
   personas, lecciones, skills) → @For3s_Brian_bot responde de SU memoria.
3. Encender **microglía real** (`FOR3S_MICROGLIA_CONFIRMAR=true` en brian) — ahora sí, que
   el olvido natural trabaje sobre memoria ya consolidada.
4. Batería §5-BIS completa + /salud 0 FAIL + Foresito intacto + pin de cupo sano.
5. Docs: Bitácora + RETOMAR + memoria del hito + backlog herramientas + fotos B7 (decisión
   Brian). Commits firmados. version.py bump.
6. **Veredicto:** 6 agentes → 1 For3s OS. Material original intacto como respaldo eterno.

---

## 7 · RIESGOS ESPECÍFICOS DE LA CRONOLOGÍA (y su mitigación)

| Riesgo | Mitigación |
|---|---|
| Fechas mal detectadas → unidad en ola equivocada | E1.2 guarda rango fecha_ini/fin + validación: sesión cuyo rango cruza olas se parte por mensajes, no por archivo |
| Duplicados principal↔wsl entran 2 veces (main vive en ambos) | dedup por hash en E1.3 + a nivel sesión por uuid-origen (el mismo uuid no entra 2 veces) |
| El CLS nocturno no alcanza a digerir una ola grande | tope de episodios/ola; si la ola excede, se parte en sub-olas; verificar consolidación (conceptos nuevos en grafo) antes de la siguiente |
| Saturar el cupo compartido (Foresito + brian + extracción) | embeddings = locales (gratis); LLM solo en destilación narrativa puntual; olas en horas valle; pin vigilado; pausa si 5h > 60% |
| Secretos que el detector v1 no conoce | v1 se calibra contra los 47+ conocidos (100% recall exigido) + barrido post-import (`grep` de patrones sobre lo insertado) |
| Un lote corrompe memoria a mitad de ola | lotes chicos reversibles + backup E0.1 + reversa demostrada ANTES de empezar |
| Deriva del plan (material wsl sorprende en E1) | el gate E1 re-calibra olas ANTES de importar nada |

## 8 · RESUMEN EJECUTIVO DEL CALENDARIO

| Etapa | Contenido | Esfuerzo | Gate |
|---|---|---|---|
| E0 | infra + reversa demostrada | 1 sesión | ver reversa |
| E1 | censo 11,664 + línea de tiempo maestra + radiografía wsl | 1-2 sesiones | manifiesto + olas |
| E2 | secretos→vault + identidad adaptada + perfil | 1-2 sesiones | ⭐ borrador identidad |
| E3 | **olas cronológicas** feb→abr con noches de digestión | 1-2 semanas calendario | examen por ola |
| E4 | skills H12 | 1-2 sesiones | skill por skill |
| E5 | cierre: examen global + microglía ON + batería | 1 sesión | veredicto |

**Total estimado: ~2-3 semanas calendario** (el grueso son las noches de consolidación de
E3 — el ritmo biológico del método, no tiempo muerto).

---

*Ejecuta: `Flujo_Extraccion_Entrenamiento.md` · Bloques: `Entrenamiento_Bloques_…Dev.md` ·
Ronda: `Ronda_Entrenamiento_Plan_Maestro.md` · Radiografías principal/dev. Método F en cada
etapa: investigar → construir defensivo → batería → commit firmado → server-primero.
⛔ REGLA VIVA: no empieza E0 hasta la orden explícita de Brian.*
