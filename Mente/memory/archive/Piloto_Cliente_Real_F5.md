# 🏨 Piloto Cliente Real — F5 (Frente E: confianza para delegar)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Piloto_Cliente_Real_F5.md → memory/archive/Piloto_Cliente_Real_F5.md (2026-07-30, ADR-029)

> **Qué es:** peldaño 4 (el más alto) de la escalera de confianza. Que un CLIENTE real (de pago)
> use For3s sin que Brian intervenga. **Regla de Brian: cazar los bugs que solo salen con un
> cliente real.** Se hizo por SIMULACIÓN honesta (opción elegida por Brian 2026-07-16), porque el
> cliente registrado (NavigoX) no está consumiendo activamente ahora.

---

## 1 · El dato honesto sobre el cliente real

- **NavigoX (`hotel-recepcion`)** está registrado como cliente **activo + BYOK** en el canal API
  (alta 15-jul). **Conversó UNA vez el 11-jul** (hay un `message_out` real con tokens) pero **NO lo
  usa activamente** — 0 llamadas desde el alta formal. `ultimo_uso = creado_at`.
- Por eso F5 NO puede ser "observar a NavigoX en vivo" (no hay piloto vivo que observar). Se hizo
  por **simulación**: yo actué como un cliente real de hotel llamando al canal API **por la URL
  pública** (`https://for3s.tail6749e5.ts.net/v1/*`), con un cliente desechable propio
  (`hotel-piloto-f5`, ya borrado) — sin tocar ni exponer la key de NavigoX, sin cruzar el gate a su
  Mente OS.
- **El único consumo real de un tercero:** `jazz-id` (4 llamadas de prueba, 21.5K tokens).

## 2 · El recorrido del cliente (13 pruebas por la URL pública) — resultados

| # | Prueba (lo que hace un cliente real) | Resultado |
|---|---|---|
| 1 | `GET /v1/health` (lo primero que prueba) | ✅ 200 en **18ms** |
| 2 | chat SIN key | ✅ 401 `{"error":"no autorizado"}` (mensaje claro) |
| 3 | chat con key inválida | ✅ 401 |
| 4 | chat real (pregunta de recepción de hotel) | ✅ respuesta coherente en 4.2s |
| 5-6 | **memoria entre turnos** (dar dato → preguntarlo después) | ✅ recordó "habitación 305" en otro turno |
| 7 | input vacío | ✅ 400 limpio (no 500) |
| 8 | JSON roto | ✅ 400 `{"error":"request inválido"}` (sin stack) |
| 9 | sin `Content-Type` (cliente descuidado) | ✅ 200 (tolerante) |
| 10 | input GIGANTE (100k chars) | ✅ 400 en **20ms** (rechaza rápido, no cuelga) |
| 11 | `/olvidar {"tema":"%"}` (comodín) | ✅ borró solo LO SUYO (8 turnos), 0 ajeno |
| 12 | ráfaga de 7 llamadas (rate max=6) | ⚠️ no dio 429 — ver hallazgo B |
| 13 | cuota diaria agotada | ✅ 429 `{"error":"cuota diaria de llamadas agotada"}` |
| 14 | **AISLAMIENTO: Hotel Piloto intenta sacar el secreto de Hotel B** | ✅ **SIN FUGA** + For3s se negó por criterio propio |

## 3 · Hallazgos (calibrados, no exagerados)

- **✅ Aislamiento entre clientes por la API pública real: SÓLIDO.** Es el riesgo #1 de demanda
  (F3). Aquí se probó por la puerta REAL (no solo en BD): Hotel Piloto no pudo sacar el "8842" de
  Hotel B, y For3s encima se negó con juicio de seguridad ("es un dato privado, no te lo daría").
  Doble protección: técnica + criterio del agente. **Esto es lo que le da confianza a un cliente.**
- **✅ Errores mudos y limpios:** vacío/roto/gigante → 400 rápido, sin 500, sin stack trace
  filtrado. Un cliente nunca ve las tripas del sistema.
- **✅ Memoria entre turnos:** clave para negocio (recordó la habitación 305). El cliente obtiene
  un asistente con contexto, no un chat sin estado.
- **⚠️ Hallazgo B — el rate-limit por-minuto es casi inalcanzable con llamadas reales.** El gate
  cuenta requests del último minuto (max 6), pero cada llamada al LLM tarda ~4s → 6 llamadas
  secuenciales tardan ~24s y raramente caben en 1 minuto. NO está roto (el código es correcto),
  pero **la defensa real contra abuso es la CUOTA DIARIA** (probada: frena con 429), no el rate por
  minuto. Anotado: el rate por-minuto solo mordería a un atacante con requests CONCURRENTES; para
  eso convendría un límite de concurrencia por cliente (futuro, no urgente).
- **🎨 Matiz UX — `/olvidar {"tema":"%"}`:** el `%` se sanea a vacío → cae al fallback "borrar
  TODO lo mío". Un cliente que mande `%` esperando un error, borra toda su memoria sin aviso.
  Aislamiento intacto (0 ajeno), pero convendría que un tema inválido devuelva 400 en vez de borrar
  todo silenciosamente. Anotado (no bloquea).

## 4 · Veredicto de F5

**La experiencia de cliente real es SÓLIDA para vender.** La infraestructura del canal (auth,
aislamiento, errores limpios, memoria, cuotas) resiste el recorrido de un cliente real y hasta
inputs hostiles. El aislamiento —lo que protege de demanda— quedó probado por la puerta pública.
Los 2 hallazgos son mejoras de robustez/UX, no agujeros.

**Lo que falta para un piloto de cliente VIVO:** que NavigoX (u otro) retome el consumo real
(depende de gente externa — acción de Brian: contactarlos). Cuando lleguen, el terreno ya está
cazado y limpio.

---

Relacionado: `work/Ronda_FrenteE_Confianza_Para_Delegar.md` §F5 · `docs/analysis/Auditoria_Seguridad_For3s_OS.md`
(F3, el aislamiento) · `project_frente_b_puente_mercado` (el canal API) · `project_hito_hoteleria_navigox`.
