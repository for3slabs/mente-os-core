# 📡 Carril de Mejora Continua — MULTI-CANAL (Frente C, dormido)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Carril_Multicanal.md → work/Carril_Multicanal.md (2026-07-30, ADR-029)

## Purpose

📡 Carril de Mejora Continua — MULTI-CANAL (Frente C, dormido)


> **Origen (Brian, 2026-07-16):** el Frente C (post-Incubathon) — *"For3s se quedó CORTO como solo
> una capa de API; la gente pedía cosas que For3s DEBERÍA hacer: contestar en grupos de WhatsApp,
> mandar correos, analizar qué clientes recurren más a un comercio."* Brian lo pospuso: *"es un
> poco complicado, tenemos que hacer integraciones algo pesadas... hay que sentarlos."* → se
> evoluciona a CARRIL (dinámica de ir sumando canales uno por uno), no un pendiente de golpe.
>
> **⛔ DORMIDO.** No se ejecuta solo. Cada canal es una integración pesada que Brian decide cuándo
> arrancar. Conectado con `memory/PENDIENTES.md` §FRENTE C y las brechas OC-C*/HG-* (multi-canal).

---

## 1 · La dinámica (el ciclo a repetir por CADA canal)

For3s hoy vive en **Telegram + consola + canal API**. Cada vuelta suma UN canal nuevo, sin romper
los existentes:

1. **ELEGIR el canal** que más valor da ahora (WhatsApp, correo, un análisis) — decisión de Brian.
2. **INVESTIGAR la integración** (API del canal, auth, límites, coste, qué se rompe).
3. **CONSTRUIR con el patrón de canal** (como el `telegram_channel`/`api_channel` ya existentes —
   reusar la arquitectura de canal, no reinventar). Método de fases si es grande.
4. **AISLAR:** el canal nuevo NO debe tumbar Telegram/API (aditivo, fail-closed) + respetar el
   scope de memoria por persona (doctrina AI1) + el perfil de seguridad de la instancia.
5. **VERIFICAR E2E** + registrar la vuelta (§4) + dormir el carril.

## 2 · Cómo reactivar (cuando Brian diga "vamos a multi-canal")

1. Leer este MD + `memory/PENDIENTES.md` §FRENTE C + las brechas OC-C1..C7 / HG-1..3 (el detalle de
   diseño ya registrado, congelado).
2. Preguntar a Brian QUÉ canal arrancar (no asumir — cada uno es integración pesada).
3. Mini-Ronda F0 del canal → aprobar → construir con el patrón de canal → verificar E2E → registrar.
4. ⚠️ Reusar: `telegram_channel.py` y `For3s-OS/.../api_channel.py` son el molde de "cómo se conecta un canal".

## 3 · Semillas para próximas vueltas (Brian elige el canal, NO hacer aún)

- **WhatsApp** (⭐ el más pedido en campo): contestar en grupos, informes especiales. Integración
  pesada (WhatsApp Business API / proveedor). Cruza con OC-C1 (multi-canal) / HG-1 (patrón Hermes).
- **Correo electrónico:** flujos de correo (recibir/enviar), + redes sociales. Cruza OC-C1.
- **Análisis de negocio:** "qué clientes recurren más a un comercio y cuáles no" — no es un canal,
  es una capacidad analítica sobre la trazabilidad (cruza con For3s Trace, ya construido). Podría
  ser una vuelta propia.
- **Voz** (entrada/salida): revertir la decisión "audio fuera" (multimodal.py) + TTS. Cruza OC-C6 / HG-2.
- **Discord** (era la sala de máquinas del agente dev OpenClaw). Cruza OC-C1 (Discord primero).

> Todas estas están registradas a detalle en `memory/PENDIENTES.md` §BRECHAS OPENCLAW/HERMES
> (OC-C1..C7, HG-1..3) — ahí está el diseño; este carril decide CUÁNDO y CUÁL.

## 4 · Registro de vueltas (bitácora del carril)

| # | Fecha | Canal elegido | Qué se construyó | Resultado |
|---|---|---|---|---|
| — | — | (ninguna vuelta aún — carril nace dormido) | — | — |

## 5 · Estado del carril

**🟡 DORMIDO (nace dormido).** For3s vive en Telegram + consola + API. La primera vuelta se despierta
cuando Brian decida qué canal sumar (probablemente WhatsApp, el más pedido). Cada canal es una
integración pesada — sin prisa, uno por uno.

---

Relacionado: `memory/PENDIENTES.md` §FRENTE C + §BRECHAS OPENCLAW (OC-C1..C7) + §BRECHAS HERMES (HG-1..3)
· `vision/Aprendizajes_De_Campo_Post_Incubathon.md` (el origen del Frente C) ·
[[feedback_evolucionar_pendiente_a_carril]] · [[project_frente_b_puente_mercado]] (el canal API =
el molde de "cómo se conecta un canal") · [[project_for3s_trace]] (para el análisis de negocio).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Carril_Multicanal.md`).
