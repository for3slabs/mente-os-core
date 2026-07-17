# Mente/Doc — Índice Maestro

**Owner:** Brian López
**Última actualización:** 2026-07-13 (añadido al inventario §5.1: Puentes_Mente_OS — capa/gate entre Mentes OS tras cierre del Incubathon)
**Estatus:** Activo

---

## 🚨 PROTOCOLO DE CONTINUIDAD (LEER PRIMERO SI RETOMAS LA CONVERSACIÓN)

**Si eres Claude/agente que retoma la conversación con Brian (o el mismo Claude tras compactación de contexto):**

### Paso 0 — Lee PRIMERO el cold-start brief (ahorro de tokens) ⚡

➡️ **[RETOMAR.md](RETOMAR.md)** ⬅️ — archivo PEQUEÑO (~5KB) con: dónde quedamos + próximo paso + flags + punteros.

**En el 90% de los casos, RETOMAR.md es TODO lo que necesitas para retomar.** Solo baja al Estado_Sesion (200KB) si un puntero de RETOMAR.md te manda ahí. Leer el Estado_Sesion completo "por si acaso" gasta tokens innecesarios (fue justo el problema que Brian detectó).

### Paso 1 — Si necesitas el snapshot completo, este documento

➡️ **[Estado_Sesion_Continuidad.md](Estado_Sesion_Continuidad.md)** ⬅️ (solo si RETOMAR.md no basta)

Este documento es **la memoria operativa cross-sesión** de todo el proyecto For3s. Contiene:
- Quién es Brian López (con identidad correcta, NO Aguilar)
- Qué es For3s, For3s OS y For3s QA (diferencias)
- Las 3 anclas estratégicas LOCKED (1.D, 2.B, 3.D)
- Estado real del producto (18% global, 5-8% valor al cliente)
- Las 5 tensiones técnicas pendientes
- Reglas de conversación con Brian (qué hacer, qué NO hacer)
- Próximo paso esperado en la conversación
- Checklist de retomada con 10 ítems

### Paso 2 — Lee el orden de prioridad

Si solo tienes tiempo para 5 documentos, léelos en este orden:

1. **`Mente/Doc/Estado_Sesion_Continuidad.md`** — saber dónde estamos
2. **`Mente/Cerebro/For3s_OS_Grafo_Maestro.md`** — la verdad arquitectónica (11 nodos + 3 pilares)
3. **`Mente/Alma/Vision_For3s_Frontier.md`** — el por qué estratégico
4. **`Mente/Doc/Banco_Filtro_Alineacion.md`** — qué tecnologías SÍ/NO
5. **`for3s-inter/07-operations/pivot-brief-2026-05-18.md`** — decisiones LOCKED de empresa

### Paso 3 — Antes de responder, confirma

Antes de proponer algo nuevo, **pregúntale a Brian dónde quedamos**. NO asumas. NO inventes contexto. NO trates documentos históricos (`/home/brianweb3/doc/FOR3S-*.md`) como fuente de verdad — son borradores de mayo 2026.

### Reglas no-negociables al retomar

```
   ✗ NO modificar for3s-inter/ sin permiso explícito
   ✗ NO escribir código sin pedir confirmación
   ✗ NO hacer commits a git sin pedirlo
   ✗ NO asumir respuestas a las 3 preguntas pendientes del README §7
   ✗ NO asumir A/B/C sobre próximas 30 días (Brian no ha respondido)
   ✗ NO marketing language, NO floreo, NO versiones suavizadas

   ✓ SÍ honestidad técnica brutal (regla explícita de Brian)
   ✓ SÍ "si no te pregunto es porque no lo sé y quiero saberlo"
   ✓ SÍ verificar contra For3s_OS_Grafo_Maestro.md siempre
   ✓ SÍ documentar todo sin perder contexto
   ✓ SÍ preguntar ante duda
```

**Si has leído `Estado_Sesion_Continuidad.md` y las reglas, puedes continuar la sesión sin perder contexto. Brian va a sentir continuidad real, no improvisación.**

---

## 1. Propósito de esta carpeta

`Mente/Doc/` es el **índice y la capa de documentos transversales** de la arquitectura `Mente/`. Vive en paralelo a `Alma/`, `Cerebro/` y `Cuerpo/`, no dentro de ninguna de ellas.

**Lo que vive aquí:**

- Documentos fundacionales que cruzan varias capas (no son puramente Alma, ni Cerebro, ni Cuerpo).
- Cristalizaciones de sesiones de discusión profundas que se quieren preservar a profundidad.
- Reglas de gobierno de la propia Mente.
- Índices y mapas de navegación.

**Lo que NO vive aquí:**

- Documentos puramente filosóficos / motivacionales → `Mente/Alma/`
- Documentos puramente teóricos / conceptuales → `Mente/Cerebro/`
- Documentos puramente ejecutables / operativos → `Mente/Cuerpo/`
- Documentos de empresa con estructura ya definida → siguen viviendo en `for3s-inter/`
- Documentos del sitio público → siguen viviendo en `Godinez/marca-personal/`

---

## 2. Cómo se relaciona Mente/ con los otros repos

Esta es la regla de precedencia y convivencia.

```
┌─────────────────────────────────────────────────────────────┐
│  Mente/        — La capa META: pensamiento del founder      │
│                  sobre For3s y sobre cómo piensa            │
│                                                             │
│  ├── Alma/     — Por qué, valores, intuición cruda          │
│  ├── Cerebro/  — Marcos teóricos, conceptos, mapas          │
│  ├── Cuerpo/   — Arquitecturas ejecutables, planes técnicos │
│  └── Doc/      — Transversal: índices, sesiones, gobierno   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
              ↓ alimenta y precede a
┌─────────────────────────────────────────────────────────────┐
│  for3s-inter/  — Company OS estructurado (LOCKED)           │
│                  decisiones operativas, ya formalizadas      │
└─────────────────────────────────────────────────────────────┘
              ↓ alimenta cuando hay evidencia
┌─────────────────────────────────────────────────────────────┐
│  Godinez/marca-personal/ — Sitio público                    │
│                            solo refleja lo que ya tiene      │
│                            evidencia y está LOCKED           │
└─────────────────────────────────────────────────────────────┘
```

**Regla de oro:** `Mente/` es donde se piensa. `for3s-inter/` es donde se decide. `Godinez/marca-personal/` es donde se muestra. Nunca se salta capas hacia adelante (no piensas en el sitio público). Sí se puede ir hacia atrás (una decisión de `for3s-inter/` puede revisitar un supuesto de `Mente/`).

---

## 3. Las 4 capas — qué va dónde

### 3.1 `Mente/Alma/` — El "por qué"

**Pregunta que responde:** ¿Por qué existe For3s? ¿Qué nunca cambia?

**Qué guardar:**
- Convicciones no-negociables del founder.
- Insights crudos antes de procesarlos racionalmente.
- Ideas-semilla que aún no son tesis pero pueden serlo.
- Reflexiones sobre identidad, propósito, dirección de fondo.
- Lo que distingue For3s de cualquier otra empresa de agentes.

**Qué NO guardar:**
- Análisis técnicos → van a `Cerebro/`.
- Planes ejecutables → van a `Cuerpo/`.
- Decisiones formales con fecha → van a `for3s-inter/07-operations/decision-log.md`.

**Cuándo escribir aquí:** cuando algo te resuene como "esto importa pero no sé todavía cómo formalizarlo". Captura primero, racionaliza después.

### 3.2 `Mente/Cerebro/` — El "qué pienso"

**Pregunta que responde:** ¿Qué entiendo del mundo, del problema, de la tecnología?

**Qué guardar:**
- Marcos teóricos (CLS, predictive coding, arquitecturas cerebrales).
- Mapas conceptuales (comparativas de agentes, de regiones cerebrales, de mercados).
- Análisis profundos de tecnologías, competidores, papers.
- Modelos mentales sobre cómo debería funcionar algo.
- Síntesis de aprendizaje (qué sé después de estudiar X).

**Qué NO guardar:**
- Convicciones puras → van a `Alma/`.
- Diseños técnicos concretos para construir → van a `Cuerpo/`.
- Documentos de producto formal → van a `for3s-inter/02-product/`.

**Cuándo escribir aquí:** cuando termines una sesión de aprendizaje, investigación, o discusión conceptual. El Cerebro es la biblioteca de modelos mentales.

### 3.3 `Mente/Cuerpo/` — El "qué hago"

**Pregunta que responde:** ¿Cómo se construye, se ejecuta, se materializa?

**Qué guardar:**
- Arquitecturas técnicas concretas (diagramas de sistema, stacks, decisiones de implementación).
- Bocetos de productos, prototipos, especificaciones técnicas.
- Planes de ejecución, secuencias de pasos.
- Diseños de experimentos.
- Conexiones entre marcos teóricos de `Cerebro/` y entregables reales.

**Qué NO guardar:**
- Roadmaps formales con fechas → van a `for3s-inter/07-operations/`.
- Specs de producto LOCKED → van a `for3s-inter/02-product/`.
- Código → va al repo correspondiente.

**Cuándo escribir aquí:** cuando un marco conceptual de `Cerebro/` esté listo para volverse plano de construcción. El Cuerpo es el puente entre pensar y hacer.

### 3.4 `Mente/Doc/` — Lo transversal

**Pregunta que responde:** ¿Qué cruza capas o gobierna la propia Mente?

**Qué guardar:**
- Cristalizaciones de sesiones de discusión que tocan Alma + Cerebro + Cuerpo.
- Índices, mapas, reglas de gobierno de la Mente.
- Documentos fundacionales que no caben limpiamente en una sola capa.
- Bitácoras de evolución del propio pensamiento.

**Cuándo escribir aquí:** cuando lo que tienes mezcla varias capas y separarlo lo rompería.

---

## 4. Protocolo "¿Dónde guardo esto?"

Cuando dudes dónde va un documento, aplica este árbol de decisión en orden:

1. **¿Es una decisión formal de empresa con fecha y owner?** → `for3s-inter/07-operations/decision-log.md`. NO va en `Mente/`.
2. **¿Es contenido para el sitio público?** → `Godinez/marca-personal/`. NO va en `Mente/`.
3. **¿Es código?** → repo correspondiente. NO va en `Mente/`.
4. **¿Cruza varias de las 3 capas Alma/Cerebro/Cuerpo y separarlo lo rompería?** → `Mente/Doc/`.
5. **¿Es un "por qué" no-negociable, una convicción, una intuición cruda?** → `Mente/Alma/`.
6. **¿Es un marco teórico, análisis, mapa conceptual, modelo mental?** → `Mente/Cerebro/`.
7. **¿Es un diseño técnico concreto, una arquitectura ejecutable, un plan de construcción?** → `Mente/Cuerpo/`.

Si después de las 7 preguntas sigues dudando, va a `Mente/Doc/` con una nota al inicio indicando por qué fue ambiguo. Eso mismo afina las reglas con el tiempo.

---

## 5. Inventario actual de documentos

### 5.1 `Mente/Doc/`

| Documento | Resumen | Fecha |
|---|---|---|
| [README.md](README.md) | Este índice maestro. Reglas de gobierno de `Mente/` + protocolo de continuidad al inicio. | 2026-05-30 |
| ⭐ [Estado_Sesion_Continuidad.md](Estado_Sesion_Continuidad.md) | **DOCUMENTO DE CONTINUIDAD CROSS-SESIÓN.** Leer SIEMPRE primero al retomar conversación. Quién es Brian, qué es For3s/For3s OS/For3s QA, 3 anclas LOCKED, estado real del producto (18% global, 5-8% valor cliente), 5 tensiones técnicas pendientes, reglas de conversación, próximo paso esperado, checklist de retomada con 10 ítems. **Si la conversación se compacta, este doc preserva todo el contexto operativo.** | 2026-05-30 |
| [Primeros_Pasos.md](Primeros_Pasos.md) | Cristalización de la primera sesión profunda. Memoria episódica/semántica, CLS, regiones del cerebro, análisis cerebral de OpenClaw y Hermes, conexión con las 7 lecciones del founder-thesis, decisión técnica oculta de For3s QA. **Base teórica fundacional.** | 2026-05-28 |
| [Banco_Infografias_Completo.md](Banco_Infografias_Completo.md) | Registro exhaustivo de las 81+ infografías compartidas por Brian en sesión de captura (lotes 1-11). Organizadas en 22 buckets temáticos con resumen denso por pieza, fuente, tecnologías mencionadas, y relevancia preliminar. Patrones macro detectados (stack TypeScript-first, ecosistema Anthropic, seguridad operacional fuerte). | 2026-05-30 |
| [Banco_Diario_Mayo_2026.md](Banco_Diario_Mayo_2026.md) | Preservación literal de los 3 documentos borrador de Brian (mayo 2026): FOR3S-STACK-DEFINED.md, FOR3S-SERVER-ARCHITECTURE.md, FOR3S-RECURSOS-ACTUALES.md. **NO fuente de verdad — diario histórico de hace 3 meses.** Hardware factual (for3s-server 32GB/1TB + WSL2), 200+ + 65 sesiones acumuladas, 23 skills, conceptos propios (Inmortalidad + Herencia), patrones de pensamiento del founder. Tensiones identificadas con el Grafo Maestro. | 2026-05-30 |
| [Banco_Filtro_Alineacion.md](Banco_Filtro_Alineacion.md) | **Filtro de decisión:** veredicto explícito KEEP/REFINE/DEFER/REFERENCIA/DROP sobre TODO el banco (infografías + diario) contra For3s_OS_Grafo_Maestro.md y las 3 anclas (1.D Dedicated SaaS, 2.B Open Core, 3.D Equipo pequeño). ~30 piezas KEEP, ~20 REFINE, ~8 DEFER, ~15 REFERENCIA, ~10 DROP. 5 tensiones arquitectónicas reales identificadas (monolítica vs microservicios, TypeScript vs Python, OpenClaw vs scratch, memoria stack, dedicated SaaS vs hardware actual). Plan de 10 rondas técnicas listo. | 2026-05-30 |
| ⚡ [RETOMAR.md](RETOMAR.md) | **Cold-start brief (~5KB) — leer PRIMERO al retomar.** Dónde quedamos + próximo paso + flags + punteros. Reemplaza leer el Estado_Sesion (200KB) en el 90% de los casos. **Estado: ✅ MVP CERRADO (2026-06-19). Próxima fase: H5+ / las 5 capacidades P1-P5 de paridad Hermes.** | 2026-06-19 |
| [Bitacora_Progreso.md](Bitacora_Progreso.md) | Registro cronológico de hitos por periodo (decisiones LOCKED, cierres de ronda, mejoras de proceso). Herencia mensual. Índice ligero; el detalle vive en Estado_Sesion. | 2026-06-09 |
| 🌉 [Puentes_Mente_OS.md](Puentes_Mente_OS.md) | **Capa de comunicación entre Mentes OS + registro de apuntadores.** Cómo acceder (con gate `acceder mente <proyecto>` + por qué, solo lectura) a otros Mente OS externos SIN integrarlos. Protege el consumo de tokens. Registrado: NavigoX (~/5M-incubathon/, CERRADO aquí). | 2026-07-13 |
| [Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md](Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md) | **Reporte maestro #1.** Alineación de cada ronda R1-R10 vs Grafo Maestro + Visión, con tablas. Veredicto ✅ 9.2/10. Cobertura 11 nodos / 7 ventajas / 3 pilares + mapa de dependencias + 3 diagramas de conexión. | 2026-06-09 |
| [Reporte_Maestro_Consolidado_R1-R10.md](Reporte_Maestro_Consolidado_R1-R10.md) | **Reporte maestro #2.** Las 10 R como UN sistema: ¿concuerda la tech? (sí, ~8 columnas vertebrales reusadas) + stack consolidado + mapa flujo datos end-to-end + costos ($97-137/mo) + contradicciones + 7 gaps + 9 refuerzos priorizados. | 2026-06-09 |
| [Plan_Maestro_Programacion.md](Plan_Maestro_Programacion.md) | **Reporte maestro #3 — el ORDEN de construcción (MARCO).** 6 fases foundation-first + 3 diagramas (Gantt, árbol dependencias, mapa flujo datos en 3 vistas) + gates de validación + MVP vs diferido + orden interno R6. 2 reglas de oro: CI/CD temprano + governor antes de auto-gen. | 2026-06-09 |
| 🔨 [Mapa_Construccion_Incremental.md](Mapa_Construccion_Incremental.md) | **EL DOCUMENTO DE OBRA (el orden REAL de ensamblaje).** Re-rebana el Plan Maestro en VERTICAL: 2 cimientos (C0 servidor, C1 esqueleto) + 16 hitos demoables (H1 HABLA → H16 PRODUCCIÓN), cada uno termina en un DEMO que se ve funcionando en el servidor for3s. Los R pasan a ser BIBLIOTECA; este doc es el orden. 3 leyes: se construye en for3s · cada hito = un demo · un hito a la vez. MVP pilotable en H4 (~4-5 sem). | 2026-06-10 |
| [Estimacion_Tiempo_Por_Subtema.md](Estimacion_Tiempo_Por_Subtema.md) | **Reporte maestro #4 — el TIEMPO.** ~100 sub-temas estimados (días-dev). Brian solo, full-time, exp alta. DERIVADO ±30%. Sistema completo ~9-10 meses · MVP pilotable ~3.5-4 meses · hito Telegram ~6 sem (LOCKED). 42% del esfuerzo en R2+R5+R6. | 2026-06-09 |
| 🔍 [Comparacion_For3s_OS_vs_Hermes.md](Comparacion_For3s_OS_vs_Hermes.md) | **Inteligencia competitiva.** For3s OS (diseño) vs Hermes Agent v0.15.1 (Nous Research, real). 15 secciones: 10 dimensiones técnicas, stack lado a lado, loop vs grafo, qué heredó For3s (~15 patrones), qué reemplazó (~15 decisiones), dónde gana cada uno. Honestidad: Hermes existe, For3s es diseño. | 2026-06-09 |
| 🔍 [Comparacion_Funcional_For3s_OS_vs_Hermes.md](Comparacion_Funcional_For3s_OS_vs_Hermes.md) | ⚠️ **MEZCLÓ 2 ELEMENTOS** (nota 2026-06-19): este doc puso datos de **Frutero OpenClaw** (otro elemento investigado aparte) bajo el título "Hermes". El Hermes REAL = `NousResearch/hermes-agent` (Nous). Sus cifras (18+ canales, voz, 16 agentes…) son de Frutero OpenClaw, no de Nous. Comparación REAL vs Nous → `PENDIENTES.md §"PARIDAD CON HERMES"` (P1-P5, 2026-06-19). Válido aquí: el NICHO de For3s (QA + auditabilidad + KEK). | 2026-06-15 |
| 🔍 [Comparacion_For3s_OS_vs_Godinez_Kukulcan_InternOS.md](Comparacion_For3s_OS_vs_Godinez_Kukulcan_InternOS.md) | **Inteligencia competitiva — ecosistema Frutero.** For3s OS vs Godínez.AI · Godínez Studio · Kukulcán Brain · internOS. Hallazgo clave: NO son competidores externos — son productos Frutero sobre OpenClaw. For3s opera en otra capa (motor cerebral vs el loop OpenClaw que comparten los 4). Qué hacen bien/mal cada uno vs For3s. **Inteligencia, NO directiva: el diseño de For3s no se toca.** | 2026-06-09 |
| 🚩 [Comparacion_For3s_OS_vs_Vertus_AI.md](Comparacion_For3s_OS_vs_Vertus_AI.md) | **Inteligencia competitiva — 🔴 humo / posible fraude.** vertus.ai (landing de 1 página, /about y /pricing = 404) se vende como "Superintelligence… advancing toward consciousness" con "51% returns" + captación de inversores + urgencia = anatomía de esquema de inversión. Sin equipo/papers/repo/entidad. Tabla comparativa (10 dims) + 4 banderas rojas + recomendación (aléjate; nada técnico que aprender). **Valor = el manual de lo que For3s NO debe ser** (su opuesto: honestidad H10, evidencia verificable). | 2026-07-02 |
| 🧠 [For3s_Bot_vs_Agente_vs_Hermes.md](For3s_Bot_vs_Agente_vs_Hermes.md) | **For3s pasó de BOT a AGENTE (2026-07-03).** Cruce vs NousResearch/hermes-agent con los 4 ejes de agente (autónomo/persistente/ejecuta/se-mejora). For3s cumple 10/12 criterios + 2 que Hermes NO tiene (auto-modificación, multi-instancia). Verificado con hechos de la sesión (creó issue #1, ejecutó código, 10 jobs nocturnos). Brechas para paridad total (NO son agencia): multi-canal + cron conversacional. FOR3S_ROLE actualizado para reconocerse agente. | 2026-07-03 |
| 🐛 [REPORTE_MAESTRO_BUGS_2026-07-02.md](REPORTE_MAESTRO_BUGS_2026-07-02.md) | **Reporte maestro de bugs de la sesión de pruebas.** Los 11 hallazgos de Brian trazados a causa raíz + 4 bugs extra cazados. 10 fixes aplicados (cache 127.0.0.1, memoria-primero, create_issue MCP renombrado, notificación consumo, alucina nombre, typing, parser C1, detector versión, cost-control opus-4-8=$0). + autopsia mensaje-por-mensaje + inventario de hardcodeos. | 2026-07-02 |
| 🔧 [Changelog_Pulido_MVP_2026-06.md](Changelog_Pulido_MVP_2026-06.md) | **CHANGELOG TÉCNICO TRAZABLE del pulido MVP (15-18 jun).** Si algo deja de funcionar, aquí está EXACTAMENTE qué se cambió, en qué archivo, por qué y cómo se verificó. 5 features grandes: web fetch híbrido (JS/SPA+anti-bot), multimodal (img/PDF/Word/Excel), conteos exactos (search tools), write tools con confirmación, cache Valkey. + 2 fixes post-prueba (timeout PDF grande, routing write). + checklist de verificación post-cambio + señales de arranque sano + ruido conocido. Suite: 126 passed. | 2026-06-19 |
| 🩺 [Auditoria_Salud_MVP_2026-06-19.md](Auditoria_Salud_MVP_2026-06-19.md) | **INFORME DE SALUD del MVP — respaldo técnico para el cierre.** Auditoría profunda por detrás tras las pruebas en vivo de Brian: procesos/recursos sanos, BD v5 íntegra, **cadena de auditoría verificada (True, 703 entradas)**, los 3 fallos reportados (PDF grande, "soy solo texto", comentar) CERRADOS y verificados en producción, 5 features activas en el bot vivo, 126 tests verdes, 0 errores reales. Veredicto: MVP técnicamente declarable como cerrado. La decisión formal es de Brian. | 2026-06-19 |
| 🧠 [H5_Infra_Memoria_AGE_pgvector.md](H5_Infra_Memoria_AGE_pgvector.md) | **🎉 H5 MEMORIA REAL COMPLETO (2026-06-20) — doc técnico + biblioteca de obra. Leer ANTES de tocar memoria/grafo/vectores.** 8 sub-pasos + integración (3 piezas) + afinado, todo EN PRODUCCIÓN. pgvector 0.8.2 + Apache AGE 1.6 + **BGE-M3** (no Stella — multilingüe). Memoria semántica (busca por significado) + Knowledge Graph + embedding de cada turno en background + grafo se puebla al leer GitHub + `solo_usuario` corta bucle de auto-confirmación. **6 TRAMPAS de AGE resueltas** (precarga, no search_path, funciones wrapper, palabras reservadas, RETURN 1 columna, RETURN int escalar→mapa). Lección: reemplazo masivo automático → lint+tests SIEMPRE. | 2026-06-20 |
| 🌙 [H6_Plan_Maestro_SE_CUIDA.md](H6_Plan_Maestro_SE_CUIDA.md) | **🎉 H6 "SE CUIDA" COMPLETO 13/13 (2026-06-20) — plan de obra + biblioteca. Leer ANTES de tocar CLS/Microglía/cron/backup.** For3s se mantiene solo de noche: backup 1AM + CLS consolida 2AM + Microglía olvida 3AM. CLS (clustering HDBSCAN + concepto sonnet-4-6 + escritura al grafo + orquestador anti-429) · Microglía (soft-delete recuperable, doble candado, audit intocable) · scheduler Arq (Valkey db1) · backup automático. Grafo: 35 conceptos/390 ep. Olvido REAL activado. ⚠️ Hallazgo clave: 429 OAuth = rechazo de system custom (no rate-limit) → fix system="". | 2026-06-22 |
| 🔧 [Changelog_Pulido_H5_H6_2026-06.md](Changelog_Pulido_H5_H6_2026-06.md) | **CHANGELOG TÉCNICO del PULIDO de H5/H6 (20-22 jun).** Cerró la brecha "el código existe pero el agente no lo reconoce". 6 arreglos funcionales (personalidad reconoce capacidades, grafo al chat, memoria semántica trae info real, naturalidad, juicio honesto, fix memoria-meta) + 3 de robustez (529 backoff, 429 blindado, refuerzo-por-uso v2) + ciclo nocturno verificado corriendo solo. Si algo deja de funcionar, aquí está qué se cambió y por qué. 132 tests. 1 pendiente: backup-offsite (config Tailscale). | 2026-06-22 |

### 5.2 `Mente/Alma/`

| Documento | Resumen | Fecha |
|---|---|---|
| [Vision_For3s_Frontier.md](../Alma/Vision_For3s_Frontier.md) | Declaración de visión fundacional de For3s. Articula por qué For3s no compite con OpenClaw/Hermes sino que define el siguiente paradigma de IA aplicada (arquitectura cognitiva completa con bases neurocientíficas). 13 secciones: diagnóstico del techo actual, tesis cerebral, diagrama maestro For3s OS vs estado del arte, las 7 ventajas técnicas defendibles (PFC, KG+pattern sep, ganglios basales QA, microglía, DMN, amígdala, grafo end-to-end), comparativa lado a lado de un agente actual vs For3s en mismo caso de uso, lista canónica de 11 piezas cerebrales de For3s, por qué QA es el wedge correcto, hoja de ruta en 5 fases hasta 2029+, anti-visión (lo que For3s NO será), métricas técnicas/comerciales/categóricas, riesgos honestos con mitigaciones, declaración de visión final en una página. **Documento norte que orienta todas las decisiones futuras.** | 2026-05-28 |

**Candidatos sugeridos** (no creados, solo idea):
- `convicciones_founder.md` — lo que nunca cambia sobre For3s.
- `manifiesto_for3s.md` — versión corta y pública de Vision_For3s_Frontier.md.

### 5.3 `Mente/Cerebro/`

| Documento | Resumen | Fecha |
|---|---|---|
| [Cerebro_Humano_acercamiento1.md](../Cerebro/Cerebro_Humano_acercamiento1.md) | Mapa visual y anatómico del cerebro humano completo en 8 niveles de zoom (macro → estructural → cortical → celular → sistemas → no-cubierto-antes → oportunidades → mapa final). Señaliza dónde la IA ya entró (🟢🟡🟠🔴), dónde están las palancas para For3s QA (⭐), y dónde está la frontier real (🧠). Cubre además ondas cerebrales, asimetría hemisférica, plasticidad estructural, glía/microglía, DMN, neuromodulación global y predictive coding. | 2026-05-28 |
| [Cerebro_Humano_acercamiento2.md](../Cerebro/Cerebro_Humano_acercamiento2.md) | Profundización en 6 territorios pendientes: (1) circuitos específicos del cerebro — hipocampo-PFC, ganglios basales GO/NO-GO, vía rápida/lenta de amígdala, dopamina mesolímbica, DMN, (2) conectoma — qué se conecta con qué, principios estructurales (small-world, hubs, bidireccionalidad), (3) neurociencia comparada — escala evolutiva, qué hace especial al cerebro humano, inteligencias no-humanas, (4) estados patológicos — H.M., Phineas Gage, Parkinson, Alzheimer, split-brain como ingeniería inversa, (5) BCIs — Neuralink, Synchron, qué se logra hoy, qué viene, (6) puente a `Mente/Cuerpo/` — inventario de 11 documentos técnicos pendientes, estructura propuesta, orden de construcción por fases. | 2026-05-28 |
| [Arquitectura_Grafo_vs_Loop.md](../Cerebro/Arquitectura_Grafo_vs_Loop.md) | Resuelve la pregunta arquitectónica más importante para For3s QA: ¿loop o grafo? 16 secciones cubriendo: por qué los agentes actuales se sienten lineales (loop con LLM paralelo escondido), los 3 niveles de "graphness" (memoria, ejecución, razonamiento), knowledge graphs y GraphRAG con profundidad técnica, LangGraph y workflow engines, Tree/Graph of Thoughts (frontier), arquitecturas no-lineales (MoE, SNN, Liquid NN, HDC, Mamba), multi-agent systems, por qué QA es naturalmente grafo, diseño concreto de Agente-Grafo para For3s QA, trade-offs honestos (costo 5-10×, latencia 2-3×), estrategia híbrida de 3 capas (MVP→v1→v2), stack tecnológico concreto, lo que nadie ha resuelto. | 2026-05-28 |
| [For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) | Mapa visual maestro de For3s OS como GRAFO COMPLETO de conexiones. Integra los 3 pilares estructurales (Seguridad/Encriptación E2E, Escalabilidad por nodo, Autonomía Generativa). 14 secciones con diagramas ASCII: el grafo maestro con 11 nodos cerebrales + procesos de fondo + meta-orchestrator + infraestructura de seguridad transversal; los 24 edges principales con payload, encryption, audit detallados; capa de seguridad en 5 niveles (key vault → E2E → workspace boundaries → audit → ZK); escalabilidad por nodo con economía unitaria que MEJORA con escala; capacidad generativa (cómo NACE una neurona nueva paso a paso + cómo nace un sistema de aprendizaje nuevo); 3 flujos completos (PR simple, PR crítico con human-in-loop, procesamiento nocturno); propiedades emergentes que crean nueva categoría. **Documento fundacional de arquitectura.** | 2026-05-28 |

**Candidatos sugeridos** (no creados, solo idea):
- `cls_y_memoria_de_agentes.md` — extraer de `Primeros_Pasos.md` la parte puramente teórica de CLS.
- `analisis_openclaw_hermes.md` — análisis cerebral comparado, como documento autónomo.
- `Cerebro_Humano_acercamiento3.md` — futura iteración: Free Energy Principle (Karl Friston), modelos matemáticos formales, hardware neuromórfico, embodied AI, conciencia artificial.

### 5.4 `Mente/Cuerpo/`

| Documento | Resumen | Fecha |
|---|---|---|
| [Hermes_Arquitectura_Completa.md](../Cuerpo/Hermes_Arquitectura_Completa.md) | Reporte de inteligencia técnica exhaustivo sobre Hermes Agent v0.15.1 de Nous Research. 19 secciones cubriendo: stack tecnológico exacto (Python 3.11+, uv, SQLite+FTS5, deps con versiones), estructura de repo con archivos clave, los 3 modos de ejecución (CLI/Gateway/ACP) sobre UN solo AIAgent, núcleo de loop de conversación con pseudocódigo, sistema de proveedores LLM (3 transports normalizando 18+ providers), sistema de tools con auto-registración (70+ en 28 toolsets), sistema de memoria dual (SQLite FTS5 + markdown), sistema de skills auto-generadas, 6 backends de ejecución (local/Docker/SSH/Modal/Daytona/Singularity), gateway de 20+ plataformas, prompts tier-based con caching Anthropic, configuración con HERMES_HOME y profiles, los 7 trucos del installer one-line, qué heredar (10 patrones), qué NO heredar (errores en seguridad/cognición/escalabilidad/autonomía), el gap For3s OS vs Hermes en 10 dimensiones, plan de construcción en 3 fases. **Base técnica para construir For3s OS.** | 2026-05-30 |
| ⭐ [Ronda_01_Compute_Lenguaje.md](../Cuerpo/Ronda_01_Compute_Lenguaje.md) | **Ronda 1 LOCKED.** Decisión técnica fundacional: Python 3.12 + uv + FastAPI + Pydantic v2 + ty + ruff + pytest + rich. Frontend = Telegram + dashboard simple Streamlit/HTMX (NO React/Vue en v1). Evaluación de 5 candidatos (Python, TypeScript, Rust, Go, Elixir/BEAM) contra el Grafo Maestro. Python gana 41 puntos, empata con Go y Elixir/BEAM, pero gana por 4 razones técnicas independientes (ecosistema AI, Hermes referencia, OpenClaw capital previo, MCP first-class). Stack específico con 11 sub-decisiones LOCKED. Estructura de directorio del proyecto. Plan de validación de 6 semanas hasta primer hito visible (For3s OS en Telegram igual que Hermes). Implicaciones en las 9 rondas siguientes. **Regla operativa LOCKED:** "El expertise se contrata. La tecnología se elige por criterio técnico, no por preferencia del founder. La fuente de verdad es el Grafo Maestro." | 2026-05-30 |

**Próximas rondas pendientes** (Mente/Cuerpo/Ronda_NN_*.md):
- R2 — Data Layer (PostgreSQL + Vector DB + KG + Memoria + Cache + Event Sourcing) — **Modo B (alta tensión)**
- R3 — Model LLM Abstraction (Claude + multi-provider) — Modo A
- R4 — Security (E2E + Vault + Workspaces + JWT) — Modo A
- R5 — Deployment (Containers + Orquestación) — Modo A
- R6 — Agent Runtime MCP (LangGraph + Skills + Multi-agent) — **Modo B (alta tensión)**
- R7 — Tooling (Web/Browser/Code/Git MCP servers) — Modo A
- R8 — Cloud Infra (Provider + Storage + CDN) — Modo A
- R9 — Observability (Logs + Metrics + Traces + OpenTelemetry) — Modo A
- R10 — CI/CD + Testing + 3 ambientes — Modo A

---

## 6. Reglas de mantenimiento de este índice

- **Cada vez que se agrega un documento a cualquier capa**, debe registrarse en la sección 5 de este README.
- **Cada vez que cambia una regla de gobierno**, se actualiza la sección correspondiente y se anota la fecha del cambio al inicio del documento.
- **Este README es append-mostly**, no se reescribe. Si una regla se invalida, se marca como obsoleta y se referencia la nueva en su lugar.
- **No se mueve un documento entre capas sin dejar nota** en este README de dónde estaba y por qué se movió.

---

## 7. Preguntas pendientes de validación con el founder

Estas tres preguntas quedaron abiertas en `Primeros_Pasos.md §15.4` y son las que afinarán todo el sistema:

1. **¿La interpretación de las 3 capas (Alma/Cerebro/Cuerpo) coincide con la intención original?** Específicamente: ¿"Alma" es el por qué/valores, o es algo distinto (p.ej. la intuición cruda, las ideas-semilla sin procesar)?
2. **¿Esto es para Brian (sistema personal de pensamiento), para For3s (sistema de la empresa), o para ambos?** La respuesta cambia qué entra dónde.
3. **¿`Mente/` reemplaza, complementa o convive con `for3s-inter/` y `Godinez/marca-personal/`?** La sección 2 de este README propone "convive y precede" — pendiente de confirmación.

Cuando estas tres se resuelvan, este README se actualiza para reflejar las definiciones finales.

---

## 8. Cierre

`Mente/` no es un repo más. Es la capa más alta del stack: donde el founder piensa antes de decidir, y decide antes de mostrar. Los otros repos (`for3s-inter/`, `Godinez/marca-personal/`) son consecuencias de lo que aquí se procesa.

La disciplina de mantener separadas las 4 capas (Alma, Cerebro, Cuerpo, Doc) es lo que evita que vuelva a pasar lo que pasó el 2026-05-18: que dos capas contradictorias hayan estado vivas en paralelo sin que nadie lo notara hasta la auditoría.

---

**Fin del índice maestro.**
