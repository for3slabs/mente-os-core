# 🟣 RONDA — Frente E: CONFIANZA PARA DELEGAR (la escalera de confianza)

> **Estado: ✅ APROBADA por Brian 2026-07-15 ("ok arrancamos") — F1 EN CONSTRUCCIÓN.**
> **Origen:** Frente E de los Aprendizajes de Campo post-Incubathon
> (`Alma/Aprendizajes_De_Campo_Post_Incubathon.md` §2). Brian eligió atacarlo 2026-07-15
> (Frente C multi-canal queda pendiente sin urgencia — integraciones pesadas, "hay que sentarlos").
> **Método:** `Cuerpo/ESTANDAR_Metodo_Fases_F.md`.

---

## 1 · La visión en palabras de Brian (el contrato)

- Sábado del Incubathon: *"No me animé a delegar la programación a For3s ni a que lo prueben.
  No siento que esté bien — es un sentimiento genuino."*
- Entrevista F0 (2026-07-15) — **¿qué significa "delegar/soltar For3s"?** Brian marcó LAS CUATRO:
  1. **Delegarle programación** (que haga trabajo de código real y confiar en el resultado).
  2. **Que otros lo prueben** (testers/gente de confianza sin miedo a que falle).
  3. **Entregarlo a clientes** (frente a clientes reales de pago sin supervisarlo él).
  4. **Que trabaje solo** (tareas de fondo/proactivas sin revisar cada cosa).
- **¿De dónde viene HOY la desconfianza?** Marcó las cuatro raíces (no ve el trabajo · miedo a
  fallo en vivo · nunca lo ha puesto a prueba · el sentimiento persiste) **+ el matiz clave,
  literal:** *"con clientes reales o situaciones reales no se ha probado; se hicieron pruebas de
  que funciona y error con bugs pero solo eso, no con clientes."*

## 2 · Diagnóstico (por qué la desconfianza es RACIONAL, no un bug de Brian)

For3s tiene verificación **técnica** de sobra: ~1115 tests, batería §5-BIS, CI de confianza
(SBOM/Sigstore/Scorecard), /salud 0 FAIL, carga probada a 2000 concurrentes. **Pero tiene CERO
kilometraje en misiones reales presenciadas.** La confianza humana no se fabrica con suites de
tests: se GANA viendo al sistema hacer trabajo real, con evidencia, y sobrevivir a sus errores.

La desconfianza de Brian es la respuesta CORRECTA a un sistema sin historial de servicio. Por eso
este frente NO es "arreglar For3s" — es construir **la escalera por la que For3s se gana la
confianza, peldaño por peldaño, con evidencia visible de cada uno.**

Los frentes D (valor de retorno) y B (panel/control) ya atacaron 2 fuentes de la desconfianza,
pero ninguno toca el hueco central: **no hay registro visible del TRABAJO que For3s hace y de si
lo hizo bien** (el panel muestra consumo del canal API, no calidad de trabajo).

## 3 · Qué existe YA (tabla de reuso — no reinventar)

| Necesidad del frente | ¿For3s ya lo tiene? | Dónde |
|---|---|---|
| Registro inmutable de acciones | ✅ audit (no UPDATE/DELETE) | pilar audit |
| Corridas de trabajo nocturno | ✅ cron_corridas (migr 023) + @registra_corrida | PR2 |
| Corridas del equipo multi-agente | ✅ corridas_equipo | H8 |
| Ejecutar código real aislado | ✅ execute_code + for3s-sandbox (EC-1..4) | paridad P3 |
| Gate "propone → aprueba" | ✅ gate GitHub write (solicitudes + fail-closed) | BUG-16 verificado |
| Observabilidad para el dueño | ✅ panel admin + alertas + Trace | Frente B F4/F6 |
| Insights/feedback de utilidad | ✅ H13 (insights + botones ✅/❌) | H13 F4 |
| Testers listos | ✅ instancias jazz (dueña real) y mashe, verificadas E2E, apagadas | multi-instancia |
| Cliente real consumiendo | ✅ NavigoX (hotel-recepcion) por canal API | Frente B |
| Salud del sistema E2E | ✅ /salud 0 FAIL + alerta al dueño | PR2 |

**Lo que NO existe:** un **expediente unificado de misiones** ("hoja de servicio": qué se le
delegó, qué hizo, cómo se verificó, resultado) ni un **carril formal de misiones reales** que
convierta trabajo delegado en historial. Todo lo de arriba son piezas — falta el hilo.

## 4 · La propuesta: ESCALERA DE CONFIANZA (4 peldaños = los 4 "delegar" de Brian)

Orden de menor a mayor riesgo/exposición. Cada peldaño produce EVIDENCIA en el expediente antes
de subir al siguiente. Brian es la métrica final: el frente cierra cuando el sentimiento cambia.

1. **Peldaño 1 — Que trabaje solo Y SE VEA.** Ya trabaja solo (DMN, CLS, backups, digest); lo que
   falta es que Brian VEA ese trabajo como hoja de servicio, no como logs.
2. **Peldaño 2 — Delegarle programación.** Misiones de código reales, supervisadas, con
   verificación y red de seguridad; el resultado (bueno o malo) queda en el expediente.
3. **Peldaño 3 — Que otros lo prueben.** Piloto con tester de confianza (jazz — instancia lista,
   dueña real) con protocolo de observación.
4. **Peldaño 4 — Situación real con cliente.** 1 caso real acotado (NavigoX ya consume el canal
   API) con inicio/fin y reporte.

## 5 · Fases propuestas (cada una: qué construye + cómo se verifica)

- **F1 · EXPEDIENTE DE MISIONES (la hoja de servicio). ✅ HECHA 2026-07-15 (commit `73583a0`
  firmado, server).** Construido: migración 045 (tabla `misiones`: pedido/qué hizo/cómo se
  verificó/resultado/errores/refs) + `expediente.py` punto único (`abrir_mision`/`cerrar_mision`/
  `hoja_de_servicio()` agregando misiones+cron_corridas+corridas_equipo+diario_cambios+insights,
  fuentes caídas REPORTADAS) + `/expediente` Telegram (solo dueño) + `GET /adm/expediente` en el
  admin API + pestaña "Expediente" en el panel (marca-personal local, build Next OK — deploy
  espera orden). **Evidencia:** pytest 234 passed (10 nuevos) · E2E misión real id=1 abierta→
  cerrada→re-cierre rechazado · hoja real: 296 corridas nocturnas 296 OK · panel 200 con token/
  401 sin token · /salud 0 FAIL · memoria escribir→embeber(1024)→recuperar por significado ·
  reconexión valkey OK. **🐛 Hallazgo:** `execute.py` NO deja rastro en BD (el trabajo de código
  delegado es invisible — F2 lo cablea). ⏳ Prueba en vivo de Brian: `/expediente` en
  @For3s_General_bot.
- **F2 · CARRIL DE MISIONES DE PROGRAMACIÓN. ✅ HECHA 2026-07-15 (commit `7842c8e` firmado,
  server).** `/mision <pedido>` (solo dueño) → For3s trabaja con tools REALES → responde TODO el
  flujo (dirección de Brian: "comunícate con todo el flujo, no solo una línea" + "encuentra bugs
  y errores"): PLAN→EJECUCIÓN→VERIFICACIÓN→ENTREGA→ERRORES → expediente → **veredicto ✅/❌ de
  Brian** (solo entregada→verificada|fallida; For3s NO se auto-verifica). Construido: `mision.py`
  (contrato+parseo puros) + botones misok/misno + `conversation.ultimas_tools` + **tool_loop
  tolera mcp=None** (misiones con sandbox aunque la instancia no tenga GitHub — caso general) +
  fuente `ejecuciones` en la hoja (cierra el hallazgo F1). **Evidencia:** pytest 244 (10 nuevos) ·
  E2E BD veredicto (5 transiciones correctas) · **E2E CARRIL con LLM real: misión primos → 2
  execute_code → el modelo se auto-verificó con 2 algoritmos independientes (24133=24133) → 5/5
  secciones → verificada** · /salud 0 FAIL · datos limpios. ⏳ Misiones REALES en vivo: Brian
  las define y corre `/mision` en Telegram.
- **F3 · RED DE SEGURIDAD VISIBLE + AUDITORÍA DE EXPOSICIÓN A DEMANDA. ✅ HECHA 2026-07-15
  (commit `d3e71ef` firmado, server SIN push).** Brian pidió el giro: *"¿existe un error crítico
  que si alguien compra mis servicios pueda haber demanda?"* → auditoría del código real + pentest
  EN VIVO (no opinión). **Veredicto: NO hay error crítico-legal.** El riesgo #1 (fuga de datos
  entre clientes) DEMOSTRADO cerrado (pentest: 4 ataques, 0 fugas). Pilares probados: audit
  inmutable (DELETE directo rechazado por trigger) · AES-256-GCM+HKDF por workspace · audit sin
  PII · auth timing-safe. **🔴→✅ Hallazgo cazado+arreglado (riesgo medio):** el sandbox alcanzaba
  postgres/valkey y salía a internet (la BD rechaza sin password → datos NO se filtraban, pero
  defensa-en-profundidad ausente) → **red segmentada** (`sandbox_net` solo agent↔sandbox;
  verificado: `gaierror` al buscar la BD, `execute_code`=5050 intacto). Doc:
  `Doc/Auditoria_Seguridad_For3s_OS.md`. Batería §5-BIS: pytest 244, /salud 0 FAIL, pentest
  SÓLIDO de nuevo.
- **F4 · PILOTO TESTER (jazz). ✅ HECHA 2026-07-16 (commit `c51a267` firmado, server SIN push).**
  jazz encendida con imagen v0.17.0+F1-F3 (migr 42-45, red sandbox segmentada, /mision+/expediente).
  **Regla de Brian: F4 = CAZAR bugs de tester real. 2 bugs cazados+arreglados:** BUG-E1 (/mision y
  /expediente NO en el menú admin = invisibles) · BUG-E2 (bug propio de F2: @con_typing quedó en
  on_mision = doble typing, y on_expediente sin él). 3 vectores investigados SANOS (embeddings frío,
  puerta cerrada por defecto, red sandbox). Doc: `Doc/Piloto_Tester_Jazz_F4.md`. Verificado en vivo
  en jazz (menú 29 cmds, expediente E2E). ⏳ Falta (Jazz): dar /start + usar el bot varios días +
  feedback. Hallazgos UX anotados: /salud en instancia virgen muestra 🔴 (confunde) · /mision ~4min.
- **F5 · PILOTO CLIENTE REAL. ✅ HECHA 2026-07-16 (por SIMULACIÓN honesta — server SIN cambios de
  código).** Dato real: NavigoX (`hotel-recepcion`) está registrado + conversó 1 vez (11-jul) pero
  NO consume activamente (0 llamadas desde el alta) → no hay piloto vivo que observar. Brian eligió
  **simular el recorrido del cliente**: actué como cliente de hotel por la URL PÚBLICA
  (`/v1/*`) con un cliente desechable (ya borrado), 14 pruebas cazando bugs. **Resultados:**
  aislamiento entre clientes SÓLIDO por la puerta real (Hotel Piloto no sacó el secreto de Hotel B
  + For3s se negó por criterio) · errores mudos/limpios (400 sin stack) · memoria entre turnos ✅ ·
  cuota diaria frena (429). **2 hallazgos (mejoras, no agujeros):** rate por-minuto casi
  inalcanzable con llamadas reales (la defensa real es la cuota diaria) · `/olvidar {"tema":"%"}`
  borra todo lo suyo en vez de 400. Doc: `Doc/Piloto_Cliente_Real_F5.md`. Datos limpios. ⏳ Falta
  (Brian): que NavigoX retome consumo real (gente externa) para un piloto VIVO.
- **F6 · CIERRE. ✅ HECHA 2026-07-16 (commit `19b6552` firmado, server SIN push).** Regla de Brian:
  probar TODO el flujo antes de cerrar. **Prueba E2E de punta a punta:** flujo completo F1-F5 =
  16/16 checks + bordes/casos límite = 11/11 (incl. inyección SQL en el pedido → guardado literal,
  tabla intacta). Batería §5-BIS del sistema completo: pytest 244, ruff limpio (mis 7 archivos ok),
  /salud 0 FAIL, memoria+reconexión, chat normal sigue en Sonnet (frente E no lo contaminó).
  **v0.18.0 CONFIANZA** horneada (rebuild final, el bot reporta el hito). **La métrica final es
  Brian** → ver §7 (la pregunta "¿ya lo soltarías?" se la hace Claude a Brian al entregar).

---

## ✅ VEREDICTO FINAL DEL FRENTE (2026-07-16)

**Frente E COMPLETO: F1-F6 + A, todo verificado EN VIVO.** La escalera de confianza construida
peldaño a peldaño con evidencia:
- **F1 expediente** (73583a0) · **F2 carril /mision** (7842c8e) · **F3 auditoría de seguridad**
  (d3e71ef — sin error crítico-legal, aislamiento probado por pentest) · **F4 piloto jazz**
  (c51a267) · **A lentitud** (5de8ec4 progreso + edf59fd Opus/BUG-E3) · **F5 piloto cliente**
  (simulación — aislamiento sólido por la puerta pública real) · **F6 cierre** (19b6552, v0.18.0).
- **3 bugs de producto cazados** en la caza-bugs (menú invisible · doble typing · respuesta vacía
  por truncado) + hallazgos anotados (rate por-minuto, /olvidar %, /salud instancia virgen, F-A2).
- **Pendiente de gente externa (no de código):** que Jazz use su bot varios días + que un cliente
  real (NavigoX) retome consumo → piloto VIVO. Falta propagar F1-A a brian/mashe/Foresito.
- **La pregunta a Brian (F0→F6):** *"¿ya lo soltarías?"* — con expediente + carril + seguridad
  probada + pilotos, ¿cambió el sentimiento de "no siento que esté bien"? Si persiste → F0 de nuevo.

⚠️ Notas de alcance: F4/F5 dependen de personas externas (jazz, cliente) → sus tiempos no los
controla el código; se diseñan para no bloquear (F1-F3 son autónomas). Server-primero en todo.

## 6 · Decisiones abiertas (Brian decide en la aprobación)

1. **¿Apruebas la escalera y el orden F1→F6?** (o reordenar/quitar fases)
2. **Las 2-3 misiones de programación reales de F2** — las eliges tú (algo que de verdad
   delegarías: un script, un fix, un análisis de repo).
3. **F4: ¿encender jazz como primer tester?** (instancia lista; ella la enciende cuando quiera)
4. **F5: ¿NavigoX como situación real, u otro?** (⚠️ su Mente OS está CERRADO — si hace falta
   contexto de NavigoX, se abre puente con `acceder mente navigox`).

## 7 · Criterio de éxito del frente

NO es "0 bugs" (eso ya existe). Es: **Brian delegó misiones reales, vio la evidencia, vio al
sistema contener sus fallos, y el sentimiento cambió de "no siento que esté bien" a "lo suelto".**
Si tras la escalera el sentimiento persiste → F0 de nuevo con lo aprendido (el sentimiento manda).

---

Relacionado: [[project_aprendizajes_campo_post_incubathon]] · [[project_hito_h13_devuelve]] ·
[[project_frente_b_puente_mercado]] · [[project_multi_instancia]] · [[project_execute_code]] ·
`Cuerpo/ESTANDAR_Metodo_Fases_F.md` · [[feedback_explicar_antes_de_implementar]].
