# 🎯 Aprendizajes de Campo — Post-Incubathon (2do lugar)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Alma/Aprendizajes_De_Campo_Post_Incubathon.md → vision/Aprendizajes_De_Campo_Post_Incubathon.md (2026-07-30, ADR-029)

## Purpose

🎯 Aprendizajes de Campo — Post-Incubathon (2do lugar)


> **Qué es:** el mapa de todo lo que el Incubathon (2º lugar de 200) le enseñó a Brian sobre
> For3s OS **como producto que va a mercado**. NO es teoría — es **experiencia de campo** +
> sentimientos genuinos de Brian como programador. Captura el ruido, las dudas y las decisiones
> pendientes para irlas atacando una por una.
>
> **Origen:** sesión Brian ↔ Claude Code, 2026-07-13 (día después de ganar). Documento de tu amiga
> (asesora de empresas/VCs) que ayudó a Brian a definir el pitch → resonó con la gente.
> **Estado:** 🟡 EN CLARIFICACIÓN. Varios frentes rebotados, otros pendientes de rebotar.

---

## 0 · El pitch que enamoró (definición validada en campo)

La amiga asesora ayudó a Brian a articular For3s así (y la gente quedó ENCANTADA):

- **El problema:** las empresas manejan info sensible → **desconfían de flujos agénticos**. Además,
  lo que metes a los agentes (ChatGPT etc.) **se usa para entrenar modelos → sin privacidad**. Y los
  flujos de trabajo NO son generalizados: son **específicos de cada operación y sector**.
- **La oportunidad:** las empresas quieren un modelo de IA **seguro, escalable, confiable y efectivo**
  que siga sus flujos, con **trazabilidad y confianza de ejecución**.
- **Qué es For3s:** sistema agéntico que **encripta, resguarda y anonimiza** la info para el modelo de
  IA — **solo el agente y el usuario conocen la información**. Estructura agéntica escalable,
  confiable y encriptada que **trabaja como un cerebro humano**: cada conversación crea un **episodio**
  (una "neurona") que pasa por un **proceso neuronal** (heurística) que decide **qué importa vs. relleno
  empresarial** — según si se usa/no en cierto tiempo, si es relevante a lo actual, etc.
- **El wedge de producto:** *"flujos operativos personalizados, seguros y trazables, con un
  razonamiento de carácter neuronal."*

> ⭐ **Insight clave:** lo que vendió NO fue "un chat con memoria". Fue **seguridad + privacidad +
> trazabilidad + razonamiento tipo cerebro**. Ese es el diferenciador. (Ver §4 — el sentimiento de
> Brian de "es solo un chat" viene de cómo lo USÓ, no de lo que ES.)

---

## 1 · Cómo se dio el fin de semana (la experiencia de campo, día por día)

- **JUE 9** — La gente amó cómo Brian vendió For3s. 🔴 **Susto de consumo:** en Claude Code mandó
  **3 mensajes y 100% del consumo se agotó**; esperó todo el día. Sabe que cerró la app, mandó
  mensaje, cerró la compu y tardó en contestar. **HAY QUE ANALIZARLO A PROFUNDIDAD** (ver §2-A).
- **VIE 10** — Intriga: *"¿cómo doy For3s a las empresas? La memoria está padre pero ¿qué hace,
  solo resguarda? ¿Cuál es su función? Aún no hay un valor que devuelva."* (ver §4 — duda de valor).
- **SÁB 11** — Programó sobre Claude Code; **NO se animó a delegarlo a For3s OS** porque no le dio
  confianza que lo realizara **ni** que lo probaran. *"No siento que esté bien — es un sentimiento
  genuino."* (ver §4 — la confianza es un frente en sí mismo).
- **DOM 12** — 🏆 **GANARON 2º lugar.** Personas le recomendaron ver **deep learning / RNN / LSTM**
  → le causó ruido (ver §3 — ya rebotado). Y el sentimiento persistente: *"siento que For3s es un
  chat que contesta y guarda memoria solamente, y eso me preocupa."*

---

## 2 · LOS FRENTES (el mapa de trabajo — atacar uno por uno)

### 🔴 Frente A — Consumo de tokens (URGENTE, bloquea el trabajo)
El jueves: 3 mensajes → 100% del consumo, un día perdido. **Analizar a profundidad qué pasó.**
Hipótesis inicial (a verificar): ¿un proceso quedó corriendo al cerrar la app/compu? ¿reenvío de
conversación completa por cache miss? Relacionado con la regla `feedback_no_loops_espera_servidor`.
→ **PENDIENTE de análisis profundo.**

### 🟠 Frente B — El puente / capa API NO está listo para mercado
La capa API fue la solución para NO entregar el sistema (buen consejo: *"si lo dejas abierto te lo
van a volar y decir que es suyo — clonar y modificar es regalar tu trabajo"*). Pero para mercado,
faltan definir cosas GRANDES:
- **¿Un solo puente o uno por cliente?** ¿Todos comparten el mismo o cada quien el suyo?
- **¿Cuánto tráfico soporta? ¿Para cuántos usuarios?**
- **Inestabilidad:** el puente se cae seguido (túnel Cloudflare quick = frágil, ya verificado).
- **Panel de administración (web app):** Brian como DUEÑO no puede ver quién consume, ni activar/
  denegar accesos. Debería ser una **web app segura de administración**.
- **Consumo según industria:** la forma de consumir cambia por sector.
→ **PENDIENTE de diseño de arquitectura de mercado.** (Base ya construida: [[project_canal_api_caja_negra]].)

### 🟡 Frente C — For3s se quedó CORTO como "solo una capa"
Usarlo solo como capa de API **limitó** a Brian. La gente pedía cosas que For3s **DEBERÍA** hacer:
- Contestar en **grupos de WhatsApp** (informes especiales).
- Mandar **correos electrónicos**; flujos de correo + redes sociales.
- Analizar **qué clientes recurren más a un comercio** y cuáles no, para comunicarse con ellos.
→ For3s tiene el potencial (multi-canal, análisis) pero se quedó como tubo. **PENDIENTE: conectar
las capacidades reales, no solo servir la capa.** (Relacionado con brechas OC-*/HG-* multi-canal.)

### 🔵 Frente D — El VALOR DE RETORNO (la duda de fondo, la más importante)
Sentimiento genuino de Brian: *"For3s es un chat que contesta y guarda memoria solamente."*
**Rebote/diagnóstico (2026-07-13):** ✅ Brian confirmó "es exactamente eso" — **no es que For3s
valga poco, es que lo usó como TUBO y nunca lo vio DEVOLVER valor, solo guardar.**
- La memoria resguarda, pero **¿qué devuelve?** Aún no actúa sobre lo que sabe.
- **Lo que falta NO es arquitectura** (ver §3). Es la **capa de valor de retorno**: que For3s
  ACTÚE sobre su memoria — *"noté que llevas 3 días en X, ¿quieres que...?"*, *"detecté este patrón
  en tus clientes"*, propuestas proactivas basadas en lo que recuerda.
→ **ESTE es probablemente el frente estratégico madre.** Resolverlo cambia cómo se siente todo.

### 🟣 Frente E — CONFIANZA para delegar/entregar (sentimiento de programador)
Brian no se animó a delegar la programación a For3s ni a que lo prueben. *"No siento que esté bien."*
Es un **sentimiento genuino que hay que escuchar, no ignorar.** Puede venir de: falta de valor
demostrado (Frente D) + falta de control/observabilidad (Frente B, panel). → **PENDIENTE: definir
qué le daría a Brian la confianza de soltar For3s** (¿más pruebas visibles? ¿panel de control? ¿ver
el valor de retorno primero?).

---

## 2-BIS · 🔴 BUG CAZADO (2026-07-13) — El equipo multi-agente no hereda la identidad de For3s

Auditando la conversación del domingo (Brian preguntó a For3s por RNN/LSTM), se cazó un bug real
**verificado en el código del server**: cuando se lanza el EQUIPO multi-agente, los 5 especialistas
**NO reciben la identidad ni la memoria de For3s** — solo su rol genérico + la pregunta cruda. Por
eso dijeron "for3s OS no está definido" e imaginaron un kernel (kernel panic, scheduler). El For3s
SOLO sí sabe quién es; el equipo se lanza en frío. Evidencia: `specialists.py:252` prompt = `[rol] +
pregunta`, sin importar `identidad`. **Fix a diseñar:** inyectar identidad + contexto a los specialists.
Detalle completo: `docs/analysis/Analisis_Conversacion_Domingo_RNN_LSTM.md`. → va a la lista de bugs/pendientes.

## 3 · Ruido ACLARADO: deep learning / RNN / LSTM ✅ (rebotado 2026-07-13)

**Veredicto: es ruido bien intencionado pero MAL DIRIGIDO. No perseguirlo.**
- RNN/LSTM son arquitecturas de hace ~10-15 años para secuencias; **obsoletas desde 2017** (llegaron
  los Transformers = la "T" de GPT). Quien lo recomendó oyó "memoria + neuronas" e hizo el atajo
  mental "memoria = LSTM" — **no entendió el sistema.**
- **For3s YA usa deep learning donde importa:** los embeddings (BGE-M3) SON una red neuronal. Y el
  razonamiento lo da Claude (Transformer moderno) — meterle un LSTM encima sería un motor de 2010
  en un coche de 2026.
- El "proceso neuronal" de For3s es una **metáfora** de la heurística de memoria (microglía, decay,
  consolidación CLS) — **y está bien que NO sea una red neuronal literal**: reglas + embeddings +
  grafo son **transparentes, auditables y encriptables** — justo lo que las empresas quieren (una
  red neuronal es caja negra imposible de auditar).
- **Matiz honesto (futuro, no urgente):** el ÚNICO lugar donde ML real podría sumar es entrenar un
  mini-clasificador que aprenda de TUS datos qué memoria resultó valiosa — pero **solo con miles de
  usuarios y datos reales**. Hoy sería sobre-ingeniería. El concepto correcto es "aprender de tus
  datos", no "LSTM".
- **Conclusión:** no te falta arquitectura. Te falta que For3s **ACTÚE** (Frente D).

---

## 4 · Consejo estratégico validado en campo (de la amiga asesora + la gente)

- **NO entregues el sistema ni el repo.** *"Te lo van a querer volar y decir que es suyo. Clonar y
  modificar es regalar tu trabajo."* → For3s se **OCUPA/consume**, no se entrega. La **capa API** es
  la vía (por eso hay que pulirla para mercado — Frente B). Consistente con la regla de la caja negra.

---

## 5 · Próximos pasos (orden a decidir con Brian)

Brian quiere **atacar todos los frentes**, pero primero **rebotar** (experiencia de campo) y
**documentar** (ya estamos en campo, son sentimientos reales de programador). Orden tentativo:
1. 🔴 **Frente A (consumo tokens)** — urgente, bloquea el trabajo. Analizar a profundidad.
2. 🔵 **Frente D (valor de retorno)** — el madre; define cómo se siente todo lo demás.
3. 🟠 **Frente B (puente para mercado)** — necesario para dar For3s a clientes.
4. 🟡 **Frente C (For3s multi-canal)** + 🟣 **Frente E (confianza)** — se resuelven en parte con D y B.

> Lista viva. Cada frente se ataca uno por uno (regla de Brian: nada de golpe). Al cerrar cada uno,
> mover el aprendizaje a la Bitácora.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `vision/Aprendizajes_De_Campo_Post_Incubathon.md`).
