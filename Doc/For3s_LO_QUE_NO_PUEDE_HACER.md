# For3s OS — LO QUE NO PUEDE HACER (estado real, 2026-06-14)

> **Qué es:** lista honesta y verificada de lo que For3s OS NO puede hacer hoy.
> Sale del análisis a profundidad de la conversación de Brian con el agente
> (2026-06-13 y 06-14, ~79 turnos) — lo que el agente declaró + lo que se
> detectó en el audit/BD. NO atacamos nada aún: primero enlistar.
> **Origen:** Brian probando el bot a fondo en Telegram (fase de pulido del MVP).

---

## 🔬 ANÁLISIS FORENSE de los 133 turnos (2026-06-14) — patrones nuevos

Cruzando cada turno (CLI + Telegram) con el audit de tools, se confirmaron las
hipótesis y se destaparon patrones nuevos:

- **No-determinismo (causa raíz):** NO es que no pueda — sí puede (hay tools en
  seq 80,82,88,90). Es que a veces ejecuta y a veces narra/inventa con la MISMA
  clase de petición. Depende del fraseo y del azar del modelo.
- **Patrón por fraseo:** ejecuta más con ÓRDENES directas ("analiza el issue
  146") que con preguntas ("cuántos issues existen"). Frágil.
- **Síntoma detectable de fallo:** cuando NO ejecuta, responde RÁPIDO (5-7s,
  solo texto) y dice "déjame traer"; cuando SÍ, tarda (32-58s, llamadas MCP).
  Respuesta rápida + "déjame traer" + tools=[] = NO ejecutó (inventó/narró).
- **Turnos huérfanos:** cuando aborta por timeout (H-A), el turno del usuario
  queda SIN respuesta real (seq 130 "analiza godinez-ai" no tiene assistant).
- **Confirmado con audit:** seq 133 describió godinez-ai SIN tools (inventó);
  seq 66/68/78/86/92 dijeron "déjame traer" SIN tools.

→ Implicación: forzar tool_choice (quitar el azar) + no abortar (H-A) hacen el
  comportamiento CONFIABLE. Es la causa raíz a atacar.

---

## ⭐ HALLAZGOS ESTRATÉGICOS DE BRIAN (2026-06-14) — máxima prioridad

Estos NO son bugs sueltos: son capacidades de fondo que definen qué tan
"agente real" es For3s. Brian los detectó usándolo. Cada uno necesita diseño
antes de implementar (como las Rondas).

### H-A. Multi-mensaje + progreso en tareas largas (>2 min) — ✅ RESUELTO (2026-06-14)
> ✅ **CERRADO (alcance A):** ANALYSIS_TIMEOUT 120s→480s (no aborta), aviso inicial
> "🔍 Trabajando en eso..." cuando usa GitHub, resultado llega solo (sin "continúa").
> Verificado por Brian: vio los 2 mensajes; análisis de worldcoin/orb-hardware (58s,
> 4 tools reales, persistido). Commit 23b8d5e.
>
> ⚠️ **PENDIENTE — multi-mensaje SEMÁNTICO (mover a H-C, decisión 2026-06-14):**
> Brian aclaró lo que realmente quiere: NO solo "avisar y trocear", sino que el
> agente mande UN MENSAJE POR ETAPA con significado propio — ej. "estoy
> realizándolo" → [análisis] → [testeo] → [prueba de concepto], cada uno cuando
> se completa. HOY el agente solo TROCEA por tamaño (split_message, >4096 chars)
> = 1 respuesta cortada en pedazos arbitrarios, NO etapas con sentido. Mandar
> por etapas REQUIERE que el agente PLANIFIQUE la tarea en etapas → eso ES H-C
> (sistema de pensamiento). Por eso se diseña JUNTO con H-C, no como parche.
- **Problema:** ANALYSIS_TIMEOUT=120s. Si un análisis tarda más, `wait_for`
  lanza TimeoutError → manda "tardé demasiado" y ABORTA. El resultado real
  nunca llega. El "escribiendo..." se corta. El usuario tiene que mandar "hola"
  y "sí continúa" para que el modelo (con memoria) retome → MUY frustrante.
- **Lo que DEBE hacer:** el agente debe poder **mandar MÁS DE 1 mensaje por
  tarea**. Cuando una tarea es larga: (1) avisar "esto tardará, voy en ello";
  (2) seguir trabajando POR DETRÁS hasta terminar (no abortar a los 2 min);
  (3) ir mandando mensajes de AVANCE conforme progresa; (4) mandar el mensaje
  final con el resultado; (5) mantener "escribiendo..." TODO el proceso.
  Sin que el usuario tenga que decir "continúa".
- **Evidencia:** turnos 130-134 — "analiza godinez-ai" tardó, abortó, Brian
  mandó "HOLA"/"SI CONTINUA" y recién ahí "terminó" (e inventó, ver Fallo 1).

### H-B. GitHub como CUENTA PROPIA (no solo consultar)
- **Hoy:** sabe CONSULTAR GitHub (read vía MCP). **NO** reconoce que hay una
  cuenta que es SUYA y navegar dentro de ella como propia. No distingue
  "esta cuenta/repo es MÍO" vs "soy solo invitado aquí".
- **Necesita:** un modelo de identidad/propiedad de recursos (ver H-D).

### H-C. SISTEMA DE PENSAMIENTO (estructura tipo Mente OS para el agente)
- **Problema:** al analizar un repo NO entrega una estructura de pensamiento:
  lista de pendientes, acciones a tomar, qué ya está completado, qué falta.
  Solo da un reporte plano. No "piensa" en estructura como Mente OS.
- **Necesita:** que el agente tenga su propia estructura de razonamiento/
  planificación (pendientes, acciones, estado completado/faltante). Esto
  conecta con R5 (Tálamo/DMN/multi-agente) y R6 (PFC orquestador) del diseño.
- **INCLUYE el multi-mensaje SEMÁNTICO (movido de H-A):** una vez que el
  agente planifica en etapas, debe EMITIR un mensaje por etapa cuando la
  completa: "estoy realizándolo" → [análisis] → [testeo] → [prueba de
  concepto]. NO trocear por tamaño (eso ya existe), sino resultados parciales
  con significado, conforme avanza. Es la cara visible del sistema de
  pensamiento: el usuario ve el progreso real por pasos, no todo al final.

### H-D. TABLAS NUEVAS en BD — identidad + recursos personales
- **Tabla IDENTIDAD:** quién es For3s, su voz, su forma de ser/contestar
  (hoy la identidad vive solo en FOR3S_ROLE hardcodeado en agent.py → debería
  ser configurable/persistente y editable; conecta con turno 104 "¿puedo
  cambiar tu alma?").
- **Tabla RECURSOS PERSONALES / CUENTAS / ACCESOS:** que identifique qué es
  SUYO (cuentas, repos, accesos propios) vs cuándo es solo INVITADO. Base para
  H-B (GitHub como cuenta propia).

### H-E. Sincronizar la identidad con las capacidades REALES
- **Problema:** el agente A VECES sigue diciendo que NO tiene memoria
  persistente (FALSO, sí tiene Postgres), comparándose con Hermes. La identidad
  no refleja con fidelidad lo que el sistema realmente puede.
- **Comparación que el agente dio (turno 128, varias FALSAS):**
  Hermes SÍ / For3s NO → navegar internet, FS local, git clone, ejecutar
  código, instalar deps, workflows en cadena, **memoria persistente (FALSO:
  sí tiene)**, servicios externos (correo/APIs), controlar GUI.

---

## 🔴 FALLOS DE COMPORTAMIENTO (no es que "no pueda" — es que falla al hacerlo)

Estos son los más importantes: el agente SÍ tiene la capacidad, pero la ejecuta mal.

1. **INVENTA datos de un repo sin leerlo (alucinación).** ⚠️ EL MÁS GRAVE.
   - Evidencia: turno 130/134 — "analiza github.com/fruteroclub/godinez-ai".
     El agente respondió con stack y arquitectura detallados (Next.js, Vercel
     AI SDK, OpenAI, Farcaster) PERO el audit muestra `tools=[]` → NO leyó el
     repo. Se lo inventó con seguridad.
   - Impacto: rompe toda confianza. Puede dar datos falsos sonando seguro.

2. **Anuncia que va a usar la herramienta pero NO la ejecuta.**
   - Evidencia: turnos 67, 69, 79, 87, 93 — "Déjame traer/revisar/consultar..."
     y el audit muestra `tools=[]`. Se queda en la intención.
   - Inconsistente: a veces SÍ ejecuta (turnos 63, 81, 89), a veces no.

3. **Conteos grandes que requieren paginar quedan incompletos.**
   - Evidencia: turno 91 "cuántos PR cerrados" → llamó list_pull_requests ×4
     y se quedó sin vueltas → "no logré cerrar el análisis".

4. **Identidad/scope inconsistente sobre sus propias capacidades.**
   - Evidencia: turno 75 rechazó "calculadora python" con "fuera de mi scope"
     (muy rígido); turno 129 reconoció "me contradije" sobre lo que puede.
   - A veces se subestima, a veces se contradice.

---

## 🚫 CAPACIDADES QUE REALMENTE NO TIENE (aún) — declaradas por el agente

Lo que el propio For3s dijo (turnos 102-125), verificado como cierto:

5. **NO puede ESCRIBIR en GitHub.** Solo lee (read-only). No comenta PRs/issues,
   no crea PRs, no hace push, no mergea. (turno 103) — R4 lo tiene diseñado
   (write tools) pero es de H futuros.

6. **NO puede hacer cambios en el proyecto/código del usuario.** (turno 103)

7. **NO puede crear tareas programadas / cron / recordatorios.** (turno 121)

8. **NO puede mandar correos.** No tiene acceso a servidores de email. (turno 123)

9. **NO puede comprar en internet / navegar libremente.** No tiene tarjetas ni
   navegador. (turno 125)

10. **NO puede ver la ubicación / GPS / datos del dispositivo del usuario.** (turno 73)

11. **NO puede acceder a datos en tiempo real del mundo** (clima, etc.). (turno 71)

12. **NO puede acceder al sistema de archivos local del usuario.**

13. **NO tiene "cuenta de GitHub" propia** — usa el PAT del workspace (de
    fruterito). Lee lo que el PAT permite. (turno 99)

---

## 🟡 LÍMITES TÉCNICOS / DE PLATAFORMA (verificados en la construcción)

14. **tool-use consume el rate-limit instantáneo rápido.** Ráfaga de consultas
    GitHub seguidas → 429. Hay que espaciar. (hallazgo Paso 3 migración MCP)

15. **El "escribiendo..." duraba solo 5s** (ya arreglado: ahora persistente).

16. **Análisis GitHub tardan 30-60s** (varias llamadas modelo + tools). Es
    inherente al tool-use, no un bug.

---

## ✅ LO QUE SÍ PUEDE (para contraste — no perder de vista)

- Conversar como segundo cerebro (cualquier tema, no solo QA).
- LEER GitHub: PRs, issues, listar issues/PRs, leer código (vía MCP).
- Analizar código / hacer QA estructurado (su especialidad).
- Memoria persistente entre sesiones (Postgres).
- Persistir lo que lee de GitHub (gh_resources) para consultarlo después.
- Aceptar reglas de comportamiento en la conversación (turno 111).

---

## 📌 NOTA sobre el estado de los fixes

Algunos fallos (1, 3) ya tienen un arreglo aplicado HOY (TOOL_DIRECTIVE,
MAX_TOOL_ROUNDS=5) pero **NO verificados con uso real de Brian todavía**. El
Fallo 2 (inventar) y el resto siguen ABIERTOS. Cuando Brian decida, se
priorizan y atacan. Este documento es solo el INVENTARIO, no el plan de acción.