# 🎤 CHARLA "Dale un trabajo a tu agente" — Plan Maestro de trabajo (VALIDACION_WEB3)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Charla_Web3_Plan_Maestro.md → work/Charla_Web3_Plan_Maestro.md (2026-07-30, ADR-029)

## Purpose

🎤 CHARLA "Dale un trabajo a tu agente" — Plan Maestro de trabajo (VALIDACION_WEB3)


> **Doc VIVO** — se enriquece con info y decisiones nuevas conforme avanzamos (Brian 2026-07-07:
> "vamos a ir agregando nueva info y nuevas cosas a lo que rodea este pendiente").
> **Evento:** AI × Blockchain Day · track "Dale un trabajo a tu agente" · **25 min** (Mel).
> **Objetivo:** demostrar EN VIVO que Foresito es un AGENTE potente de verdad (no un chatbot).
> **Fuente base:** PENDIENTES §VALIDACION_WEB3 · `memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md` (guion base).

---

## 0 · ⏰ LO PRIMERO QUE FALTA CONFIRMAR (bloqueante)

- [ ] **¿La charla sigue en pie y CUÁNDO es exactamente?** El pendiente decía "jueves de la semana
      del ~10-17 jul". Hoy es 2026-07-07. → **confirmar fecha/hora exacta con Mel/organizadores.**
      Esto define TODO el calendario de preparación (la batería E2E va 1-2 días antes).

## 1 · EL MENSAJE (la narrativa central)

**"No es un chatbot con esteroides — es un agente que recuerda, aprende, se cuida solo y hace
trabajo real. Self-hosted: tus datos, tu servidor, tus reglas."**

Encaja con los paneles del evento ("Identidad después de la explosión de bots" · "Cuando los
agentes AI tienen wallets"): For3s YA responde a eso — agente con identidad viva, memoria,
auto-conciencia, ejecuta código, trabaja solo.

## 2 · EL ARSENAL (qué mostrar — cada uno es un "wow")

| # | Capacidad | Mensaje en vivo | Riesgo demo |
|---|---|---|---|
| 1 | 🧠 Memoria real | "¿en qué quedamos?" → retoma de verdad | bajo |
| 2 | 🎭 Identidad viva | "sé más breve" → se acopla al instante; "¿cómo te has adaptado?" | bajo |
| 3 | ⚡ Ejecuta código | pide un cálculo → lo CORRE en su sandbox | medio (velocidad) |
| 4 | 🐙 GitHub real | analiza repo / cuenta PRs exacto / crea issue con confirmación | medio (red) |
| 5 | 🤝 Equipo multi-agente | "analiza a fondo" → 5 specialists + síntesis | medio (tarda) |
| 6 | 🌙 Trabaja solo | mostrar /salud + evidencia del ciclo nocturno | bajo |
| 7 | 🪞 Se auto-modifica | /soy, /cambios (dentro de su caja) | bajo |
| 8 | 🔒 Confianza enterprise | audit inmutable + KEK + CI (SBOM/Sigstore/Scorecard) | slide, no demo |

## 3 · ENTREGABLES (checklist — se marca al avanzar)

- [ ] **Guion de la demo en vivo** — secuencia EXACTA de mensajes a Foresito (con la respuesta
      esperada de cada uno). Base: `memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md`. → doc aparte cuando arranquemos.
- [ ] **Slides / narrativa** — porqué (agente vs bot, self-hosted) + arsenal + cierre.
- [ ] **⭐🔴 Batería de verificación E2E** — probar CADA mensaje del guion EN TELEGRAM con el
      modelo real, 1-2 días antes (Foresito se auto-modifica de noche → verificar cerca de la fecha).
      Objetivo: cero sorpresas. §5-BIS completa + /salud 🟢.
- [ ] **Plan B** — demo grabada + instancia local, por si falla la red del evento.
- [ ] **¿Instalador para que la gente lo pruebe?** (cruza DIST-2: `curl|sh` en Linux limpio).
- [ ] Formato: presentación + demo en vivo (NO taller hands-on largo — 25 min no dan).

## 4 · ⚠️ RIESGOS ESPECÍFICOS DE LA DEMO EN VIVO (nuevos, a mitigar)

| Riesgo | Mitigación |
|---|---|
| **Red del evento falla** (Foresito vive en el server de Brian vía Telegram/Tailscale) | Plan B: demo grabada + verificar conectividad del venue antes |
| **Velocidad** — sonnet + equipo multi-agente pueden tardar en vivo (silencio incómodo) | ensayar tiempos; tener respuestas cortas primero; el equipo solo si hay margen |
| **Cupo compartido** — HOY hay 5 agentes en el server con 1 sola suscripción → una demo pesada podría toparse | ⚠️ NUEVO: apagar jazz/mashe/general durante la charla para que Foresito tenga el cupo; verificar % de cupo antes |
| **Foresito se auto-modificó de noche** y algo cambió | la batería 1-2 días antes lo caza; guardián de arranque como red |
| **La instancia equivocada** — con 5 bots, mostrar el correcto (@For3s_OS_bot = Foresito) | tenerlo claro en el guion |

## 5 · 📓 BITÁCORA DE ESTE PENDIENTE (se agrega info nueva aquí)

**2026-07-07 — apertura del doc de trabajo.**
- Brian decidió atacar VALIDACION_WEB3, enriqueciéndolo incrementalmente.
- ⚠️ **Contexto NUEVO desde que se creó el pendiente:** ahora hay **5 For3s OS** en el server
  (Foresito + brian + general + jazz + mashe) compartiendo 1 cupo → RIESGO nuevo para la demo
  (§4). Y **brian está a mitad del entrenamiento** (digestión nocturna en curso) → el ciclo
  nocturno del server está más cargado.
- ⚠️ **Server no respondió** (timeout SSH 2026-07-07 al verificar estado) → no se pudo checar el
  estado real de Foresito hoy. Reintentarlo cuando la red del server vuelva.
- [ ] PRÓXIMO: confirmar fecha exacta (§0) → luego decidir si arrancamos guion o batería.

---

*Cruza con: PENDIENTES §VALIDACION_WEB3 · `memory/archive/PLAN_PRUEBAS_EXHAUSTIVO.md` ·
memoria [[project_hito_identidad_viva]] · [[For3s_Bot_vs_Agente_vs_Hermes]].*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Charla_Web3_Plan_Maestro.md`).
