# 🔎 Ronda — "For3s Trace": estándar universal de trazabilidad auto-detectable

> **Origen:** Brian corrigió M4 del molde (2026-07-15). M4 v1 trazaba UN tema definido a mano; la
> visión REAL (aprendida de NavigoX) es lo opuesto: **un estándar universal que detecta
> AUTOMÁTICAMENTE qué trazabilizar en CUALQUIER página de CUALQUIER nicho**, y si agregan un
> componente nuevo, el sistema lo detecta y lo conecta solo a For3s. Método de Fases F.

## 1 · La visión (palabras de Brian)
Todo el mundo crea páginas con los mismos componentes — registro, pagos, lista de espera, encuestas,
reservaciones, pasarelas, buscadores. Museos, hoteles, tiendas, restaurantes: **nichos distintos,
componentes que se repiten, y TODOS necesitan trazabilizar.** *"Lo que nos corresponde es
ESTANDARIZAR para poder trazabilizar todos esos componentes."* Cada componente tiene algo único (su
etiqueta o su llamado). Si tenemos el estándar, aunque el cliente cree más componentes, **el sistema
detecta que existe algo nuevo que trazabilizar**. El pitch: *"tienes tu página de cualquier nicho,
le metes la infra de For3s OS, y en automático tienes trazabilidad."*

## 2 · ⚠️ AJUSTE DE FOCO (Brian 2026-07-15): NO construimos el tracer del cliente
El código que traza en la página del cliente **es de ELLOS** (usan su servicio; el estándar T1 les
dice QUÉ mandar). **Nuestro valor = For3s RECIBE y ANALIZA lo trazado.** Somos "un poco metiches":
con el estándar pedimos cierta info, para poder analizarla. Cadena:
`cliente traza (su código, estándar T1) → For3s RECIBE → For3s ANALIZA ← aquí el valor`.

- **Pieza 1 · Vocabulario estándar (T1 ✅)** = QUÉ pedimos: catálogo de componentes trazables +
  el evento canónico. Es "ser metiches" con criterio (info estándar, no cualquier cosa).
- **Pieza 2 · El MOTOR DE ANÁLISIS (el foco real)** = qué hace For3s con lo trazado: resumir,
  detectar patrones/anomalías, alertar, y responder en lenguaje natural "¿qué pasó con X?".
- ~~Tracer del cliente + IA detectora de componentes~~ → **DESCARTADO como nuestro trabajo** (es del
  cliente). Podemos dar un ejemplo mínimo de referencia, pero no lo construimos ni lo mantenemos.

## 3 · Por qué es distinto (el diferenciador, confirmado en investigación)
El patrón data-attributes + schema de eventos versionado YA existe y es probado (Segment, GTM,
mParticle, RudderStack). **Lo que NADIE ha hecho es juntarlo con (a) auto-detección por IA de
componentes sin etiquetar y (b) una MEMORIA que razona (For3s), no solo un almacén de eventos.**
Ahí está el diferenciador de For3s Trace.

## 4 · Fases (reenfocadas tras el ajuste de Brian)
- **T1 · Vocabulario/catálogo estándar ✅** — QUÉ pedimos (el diccionario + evento canónico).
- **T2 · MOTOR DE ANÁLISIS** — lo que For3s HACE con los eventos trazados: recibirlos, guardarlos en
  el hilo de la entidad, y ANALIZAR (resumen del estado, patrones, anomalías/alertas, consulta NL
  "¿qué pasó con X?"). ← EL FOCO REAL. Reusa el canal API + la memoria de For3s.
- **T3 · (opcional) ejemplo de referencia** — un snippet mínimo de cómo el cliente manda eventos
  (para que vea el formato), SIN construirle su tracer. Referencia, no producto.
- ~~T4 paquete "mete y ya" / IA detectora~~ → fuera de nuestro alcance (es del lado cliente).

## 5 · Relación con lo ya construido
- Reusa el canal API del Frente B (`/v1/chat` como sumidero de eventos) + el molde For3s Inside
  (SDK, contrato, onboarding). For3s Trace es la CAPA de arriba: qué trazar y cómo detectarlo.
- Reemplaza/eleva M4 v1 (que trazaba un tema a mano) con el estándar automático.

## ✅ T1 CERRADA — vocabulario estándar (commit `1b272e1`)
- `molde/for3s-trace/VOCABULARIO.md` + `catalogo.json` (formato máquina para T2/T3): cómo se marca
  un componente (`data-for3s="<tipo>"` + `data-for3s-<campo>`), **15 tipos base** (registro/login/
  pago/reserva/waitlist/encuesta/busqueda/carrito/checkout/reseña/checkin/cancelacion/contacto/
  descarga/suscripcion) + **extensible** (`custom:`) + **versionado** (semver, `trace/v1`) + el
  evento canónico que llega a For3s.
- Apoyado en GA4 recommended events + schema.org (estándares de facto confirmados en investigación),
  pero para TRAZABILIDAD CON MEMORIA, no analytics.
- **VALIDADO:** cubre 6 nichos (hotel/museo/tienda/restaurante/eventos/saas) y **7/7 de los
  componentes que Brian nombró** (registro, pagos, waitlist, encuestas, reservaciones, pasarelas,
  búsqueda).

## ✅ T2a CERRADA — For3s recibe y analiza (commit `b4873b5`)
- **migración 042** `trace_events` (append-only, estructurada: client_id/tipo/entidad/campos/ts +
  índices por tipo+fecha y por entidad; aislada por cliente).
- **`trace.py`** motor único: `registrar` (fail-closed en tipo inválido, FILTRA campos sensibles
  siempre, defensivo) + `eventos_entidad` + `conteo_tipos` (base de T2b). Catálogo v1 (15 tipos +
  custom:), funciones puras testeadas.
- **`POST /v1/trace`** (recibe evento estructurado, mismo gate/aislamiento que /v1/chat) +
  **`POST /v1/analisis`** (For3s RAZONA sobre los eventos reales de una entidad → su estado, Nivel 2).
- **E2E real:** 3 eventos de una reserva trazados · typo `pagoo`→400 · campo sensible `card` NO se
  guardó (solo monto/moneda) · `/v1/analisis` dio el estado correcto razonando sobre los 3 eventos
  ("reserva pagada, check-in confirmado, falta checkout"), sin inventar. 222 tests. Fix B904 en SDK.

## ✅ T2b CERRADA — análisis del conjunto: patrones/anomalías (commit `7b70464`)
- **Motor HÍBRIDO anti-alucinación:** `trace.detectar_anomalias()` = REGLAS puras (números reales de
  la BD, cero IA): embudos rotos (registro→pago, checkout→pago, carrito→checkout, reserva→checkin
  con umbral+ratio), racha de cancelaciones, demanda sin conversión. `hechos_del_conjunto()` junta
  conteo + anomalías. Umbrales por ENV. La IA solo INTERPRETA los hechos (prioriza + recomienda), no
  inventa números.
- **`/v1/analisis` SIN entidad** = análisis del conjunto (T2b); CON entidad = estado (T2a). 4 tests.
- **🐛 BUG cazado con la prueba:** `/v1/trace` aplicaba el gate de CHAT (6/min) + contaba en
  api_consumo → los eventos de trazabilidad se auto-limitaban (de 13 solo entraban 6) y falseaban el
  análisis. FIX: el trace NO pasa por el rate de chat (un cliente traza muchos eventos/min
  legítimos); `rate_ok` propio y generoso (600/min) sobre trace_events, fail-open. Gates de
  estado/expiración se mantienen.
- **E2E post-fix:** 13/13 eventos entran · 2 anomalías con números exactos (embudo 8→1 alta, 4
  cancelaciones media) · For3s interpretó y recomendó sin inventar. 223 tests.

## ✅ T2c CERRADA — alertas proactivas (commit `80b301b`)
- For3s AVISA solo cuando detecta anomalías → van al ADMIN (Brian) por ahora (decisión de Brian).
  Reusa el worker nocturno de H13.
- **migración 043** tabla `trace_alertas` **SEPARADA de insights** (esa es memoria personal de
  Brian; estas son de CLIENTES → bug lógico de dueños evitado). **DEDUP DURO** por índice único
  (client_id, clave, dia) → imposible duplicar aunque el job corra 2 veces.
- `trace.py`: `generar_alertas` (barre clientes, detecta, crea con ON CONFLICT DO NOTHING) +
  `clientes_activos` + `alertas_pendientes`, defensivo. `tasks.py`: `job_trace_alertas` (cron 03:15 Mx).
- **🐛 BUG LÓGICO cazado (análisis a detalle):** el dedup usa `dia=current_date` pero el análisis
  miraba ventana RODANTE de 24h → desalineación temporal (re-alerta al cambiar de día / mal dedup a
  medianoche). FIX: `hechos_del_conjunto(desde_medianoche=True)` = ventana día calendario, alineada.
  El análisis manual `/v1/analisis` conserva la ventana rodante (ahí el usuario elige el rango).
- **E2E:** 8 reg/1 pago/5 cancel → 2 alertas (embudo alta + cancelaciones media); 2ª corrida = 0
  nuevas (DEDUP OK); números reales. 224 tests.

## ✅ ALERTAS RICAS EN EL PANEL (Piezas A+B+C, Brian: "sacar el mayor beneficio a la trazabilidad")
- **Pieza A ✅ (`d01cd79`)** — el PUNTO EXACTO: `afectados_embudo` (anti-join: quién hizo registro
  pero NUNCA pago = los atorados, con su ubicación url/componente) + `hechos_del_conjunto` enriquece
  cada embudo con paso/componente/afectados. Migr 044 (trace_alertas + paso/componente/afectados/
  n_afectados). Catálogo T1 ampliado con url/componente opcionales. E2E: 6 reg/1 pago → 5 atorados
  (u1 excluido correcto) con ubicación.
- **Piezas B+C ✅ (`db3bae8` server + `a64dc3d` panel)** — `GET /adm/alertas` (con punto exacto +
  INSTANCIA vía FOR3S_AGENT_NAME) + `POST /adm/alertas/<id>/vista`. Pestaña **Alertas** en el panel:
  severidad alta/media con color, cliente, punto (paso→componente), afectados desplegables con su
  ubicación, instancia, marcar vista.
- **🐛 BUG cazado en E2E:** el contenedor admin no tenía `FOR3S_AGENT_NAME` (compose no se lo pasaba)
  → instancia salía "?". FIX en el compose. Verificado: instancia=general, marcar vista OK.

## ✅ T3 CERRADA — ejemplo de referencia + README (commit `1b70f02`)
- SDK del molde (`for3s.ts`) extendido con `.trace(tipo, {entidad, campos})` y `.analizar(entidad?)`
  — el cliente usa el mismo SDK de M2 para trazar y analizar. tsc --strict OK.
- `molde/for3s-trace/ejemplo_trace.ts`: el FLUJO COMPLETO ejecutable (traza reserva → estado →
  simula embudo roto → For3s detecta el patrón). Probado vs API real.
- `molde/for3s-trace/README.md`: el estándar para entregar al cliente (3 pasos, vocabulario,
  privacidad, punto exacto, qué pone el cliente vs For3s).

## Estado
🎉🎉 **FRENTE FOR3S TRACE 100% COMPLETO.** T1 estándar/vocabulario · T2a recibir+estado · T2b
patrones/anomalías · T2c alertas proactivas · Piezas A+B+C alertas ricas en el panel (punto exacto +
afectados + instancia) · T3 ejemplo/README. El cliente traza → For3s recibe→analiza→detecta con el
punto exacto→avisa en el panel por instancia. **~8 bugs cazados** (LIKE injection SEC en M4, rate
matando eventos, desalineación temporal del dedup, admin sin AGENT_NAME…). **Pendiente futuro (no
urgente):** alertas al cliente directo (requiere su canal — cruza con Frente C multi-canal).
**Siguiente frente lo marca Brian.** ⚠️ NavigoX en `~/5M-incubathon/` CERRADO.
