# 🔄 Carril de Mejora Continua — CONFIANZA para delegar (Frente E vivo)

> **Origen (Brian, 2026-07-16):** *"me gustó la dinámica. Este frente no lo quiero cerrar como
> terminado — siento que es algo repetitivo que vamos a ir mejorando. Lo cerramos COMO PENDIENTE,
> pero creamos un MD conectado a PENDIENTES para poder REPETIRLO más adelante (no ahora) con esta
> estructura. Evolucionamos un pendiente a algo más."*
>
> **Qué es este archivo:** el frente E (confianza para delegar) demostró ser un **ciclo**, no una
> tarea de una sola vez. Este MD guarda la ESTRUCTURA del ciclo para reactivarlo cuando Brian quiera
> ganar otra vuelta de confianza. Cada vuelta deja evidencia y mejora un poco más. Conectado con
> `Doc/PENDIENTES.md` §Frente E y `project_frente_e_confianza_delegar`.
>
> **⛔ NO se ejecuta solo.** Es un carril DORMIDO que Brian despierta cuando lo sienta ("más
> adelante, no ahora"). Nace de un sentimiento genuino de Brian, y el sentimiento manda.

---

## 1 · La dinámica que funcionó (el patrón a repetir)

Lo que a Brian le gustó del Frente E, destilado en 5 pasos. **Cada vuelta del carril repite esto:**

1. **ESCUCHAR el sentimiento.** Brian dice qué le da o le quita confianza HOY (no lo que "debería").
   El sentimiento es el dato de entrada, no un capricho a corregir.
2. **CONSTRUIR evidencia visible.** Una pieza que haga el trabajo de For3s VISIBLE y verificable
   (expediente, carril, panel, reporte…). La confianza se gana viéndola, no creyéndola.
3. **CAZAR bugs como tercero real.** Recorrer lo construido como lo haría quien NO lo hizo (un
   tester, un cliente, un input hostil). Los peores bugs salen aquí. Regla de Brian: *"empieza a
   encontrar errores y bugs"*.
4. **PROBAR TODO el flujo (no el carril).** Antes de dar algo por bueno: batería §5-BIS + E2E de
   punta a punta + bordes. *"Puede haber errores y bugs"* → verificación afirmativa, cero "más o menos".
5. **DEVOLVER la pregunta a Brian.** *"¿Ya lo soltarías?"* Su respuesta define si esa vuelta cierra
   o si falta algo. Se registra la vuelta y se duerme el carril hasta la próxima.

> El método técnico de cada pieza sigue siendo el Estándar de Fases "F"
> (`Cuerpo/ESTANDAR_Metodo_Fases_F.md`). Este carril es la CAPA DE ARRIBA: por qué y cuándo se
> arranca otra vuelta, no cómo se construye cada fase.

## 2 · Cómo reactivar el carril (cuando Brian diga "otra vuelta de confianza")

1. Leer este MD + `project_frente_e_confianza_delegar` (la memoria del frente) + la última vuelta
   registrada abajo (§4).
2. Preguntar a Brian el **sentimiento actual**: ¿qué le falta HOY para confiar más / soltar más?
   (paso 1 de la dinámica). NO asumir; el frente nació de un sentimiento, cada vuelta también.
3. Diseñar la vuelta como una mini-Ronda (F0 ligero): qué pieza de evidencia + cómo se caza + cómo
   se prueba. Aprobar con Brian.
4. Ejecutar los 5 pasos (§1). Server-primero, commits firmados, batería §5-BIS.
5. Registrar la vuelta en §4 y actualizar PENDIENTES. Dormir el carril.

## 3 · Semillas para próximas vueltas (candidatas — Brian elige, NO hacer aún)

Del propio Frente E quedaron abiertas cosas que son material natural para vueltas futuras:

- **Pilotos VIVOS (dependen de gente externa):** Jazz usa su bot varios días + un cliente real
  (NavigoX u otro) retoma el consumo → observar uso real, no simulado. Cuando pase, hay una vuelta
  clara: cazar los bugs que solo el uso real de un tercero destapa + recoger su feedback.
- **F-A2 · sub-agentes en paralelo → A HECHO / C DIFERIDO (2026-07-16).** Análisis honesto
  (`Cuerpo/Ronda_FA2_Subagentes_Paralelos_Mision.md`): el freno real NO es el código sino el cupo
  Claude compartido (1 para las 5). **A (hecho, `8798190`):** `CONCURRENCIA_MAX` del equipo por ENV
  `FOR3S_EQUIPO_CONC_MAX` (default 2; las internas lo suben). **C (diferido):** el planner completo
  de sub-agentes rinde cuando BYOK quite el freno del cupo → semilla para reactivar entonces.
- **Propagar a las otras instancias** — F1-F6+A+SEC-4c ya en las 5 (2026-07-16).
- **✅ Mejoras de robustez/UX — LAS 3 RESUELTAS 2026-07-16** (commits `7b83deb`+`1737fd0`):
  - ✅ `/salud` en instancia virgen → ⚠️ aviso "sin uso aún" (no 🔴).
  - ✅ rate-limit → **límite de concurrencia por cliente** (semáforo, FOR3S_API_CONC_MAX).
  - ✅ `/olvidar {"tema":"%"}` → 400 (tema inválido no borra todo).
- **Confianza para que trabaje SOLO más (peldaño 4 aún tierno):** hoy hace trabajo nocturno; una
  vuelta futura podría darle misiones autónomas acotadas con reporte, ampliando cuánto se le suelta.
- **Modelito que aprende qué memoria es valiosa** (requiere volumen de datos; línea futura ya
  anotada en PENDIENTES). Encaja aquí cuando haya uso real.

## 4 · Registro de vueltas (bitácora del carril)

Cada vuelta que se complete se anota aquí (lo nuevo arriba): fecha · sentimiento de entrada · qué
se construyó · bugs cazados · veredicto de Brian.

| # | Fecha | Sentimiento de entrada | Qué se construyó | Bugs cazados | Veredicto de Brian |
|---|---|---|---|---|---|
| 1 | 2026-07-15/16 | *"No me animé a delegar ni a que lo prueben. No siento que esté bien."* | Escalera F1-F6+A: expediente · carril /mision (Opus+progreso+veredicto humano) · auditoría de seguridad (sin error crítico-legal) · piloto jazz · piloto cliente (simulación) · v0.18.0 CONFIANZA | E1 menú invisible · E2 doble typing · E3 respuesta vacía por truncado | *"Me gusta, lo tengo que probar"* → cerrado COMO PENDIENTE (dinámica repetible, este carril) |

## 5 · Estado del carril

**🟡 DORMIDO (cerrado como pendiente vivo).** La vuelta 1 quedó completa y verificada; Brian la
va a probar en uso real. La próxima vuelta se despierta cuando Brian lo sienta — típicamente
cuando un piloto vivo destape algo, o cuando quiera soltar un peldaño más. No hay prisa: el
sentimiento marca el momento.

---

Relacionado: `Doc/PENDIENTES.md` §Frente E · `Cuerpo/Ronda_FrenteE_Confianza_Para_Delegar.md`
(la vuelta 1 completa) · `project_frente_e_confianza_delegar` (memoria) · `Doc/Piloto_Tester_Jazz_F4.md`
· `Doc/Piloto_Cliente_Real_F5.md` · `Doc/Auditoria_Seguridad_For3s_OS.md` ·
`Cuerpo/ESTANDAR_Metodo_Fases_F.md` (el método técnico de cada pieza).
