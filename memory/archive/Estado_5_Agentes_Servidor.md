# 🖥️ Estado de los 5 For3s OS en el servidor — con episodios a detalle

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Estado_5_Agentes_Servidor.md → memory/archive/Estado_5_Agentes_Servidor.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-08 (datos REALES leídos de cada BD, tras encender el server).
> Servidor `for3s` (Tailscale 100.112.177.53) · 18 GB RAM (3.6 usada) · 744 GB libres.
> 5 For3s OS aislados (red/BD/KEK/volúmenes propios) · comparten 1 suscripción Claude.

---

## 📊 TABLA MAESTRA — todo de un vistazo

| Instancia | Bot | Estado | Episodios (vivos) | Consolidados al grafo | Conceptos | Embeddings | Skills | Secretos vault | Personas |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 🏢 **foresito** | @For3s_OS_bot | 🟢 | **820** (de 822) | 716 | **74** | — | 2 | 2 | 2 |
| 👤 **brian** | @For3s_Brian_bot | 🟢 | **21,640** (de 32,773) | 8,136 | **690** | 32,773 | 15 | 38 | 1 |
| 🌐 **general** | @For3s_General_bot | 🟢 | **2** | 0 | 0 | 2 | 0 | 0 | 1 |
| 🎷 **jazz** | @For3s_Jazzita_bot | ⚪ apagada | 0 (nace vacía) | 0 | 0 | 0 | 0 | 0 | — |
| 👊 **mashe** | @For3s_Mashe_bot | ⚪ apagada | 0 (nace vacía) | 0 | 0 | 0 | 0 | 0 | — |

> Nota: jazz y mashe se crearon vacías y siguen apagadas (a propósito). No se encendieron para
> contar — nacen con 0 episodios; sus valores serán 0 hasta que sus dueños las usen.

---

## 🏢 FORESITO (@For3s_OS_bot) — el agente de la EMPRESA

- **Episodios:** 822 totales · **820 vivos** · 2 soft-deleted (microglía ON).
- **Consolidados al grafo:** 716 (87% de los vivos — memoria bien digerida).
- **Conceptos en el grafo:** 74 (personas, repos, proyectos, decisiones de la empresa).
- **Skills:** 2 · **Secretos en vault:** 2 (github_token, telegram_bot_token) · **Personas:** 2 (Brian + Sme G).
- **Schema BD:** v32 (NO tiene la migr 033 del entrenamiento — ese es solo de brian).
- **Naturaleza:** memoria "orgánica" de meses de uso real de Brian con la empresa. Microglía ON
  (olvida lo irrelevante de noche). Es el agente maduro y estable.

## 👤 BRIAN (@For3s_Brian_bot) — el PERSONAL, entrenado con Fruterito

- **Episodios:** 32,773 totales · **21,640 vivos** · 11,133 soft-deleted (curación de Watchdog).
- **Importados del entrenamiento:** 32,763 (casi todo — es el agente que recibió los 6 agentes OpenClaw).
- **Con embedding:** 32,773 (100% — memoria semántica completa).
- **Consolidados al grafo:** **8,136 (~38%)** — sube cada noche solo (CLS nocturno digiriendo).
- **Conceptos en el grafo:** **690** (los más de todos — la vida de Fruterito hecha conceptos).
- **Skills:** 15 (las de OpenClaw: genomad, hackathon-mode, cracked-dev, audit-code…).
- **Secretos en vault:** 38 (los del material OpenClaw, cifrados).
- **Personas:** 1 (Brian).
- **Naturaleza:** el agente con MÁS memoria del server — heredó 6 agentes. Microglía OFF a
  propósito (para no olvidar material recién importado hasta terminar la digestión).
- **⏳ En proceso:** digestión al grafo (38%→100% con las noches) + E6 backlog (fotos medianas).

## 🌐 GENERAL (@For3s_General_bot) — el PÚBLICO, equipo abierto

- **Episodios:** 2 vivos (recién nacido, casi virgen).
- **Consolidados/conceptos:** 0 (aún no ha tenido conversación real).
- **Skills/secretos:** 0 · **Personas:** 1 (Brian, el dueño).
- **Naturaleza:** memoria virgen, con la PUERTA del equipo ABIERTA (quien le escriba entra con
  rol y memoria privada). Listo para que tu gente lo use. Pendiente: otras API keys/datos.

## 🎷 JAZZ (@For3s_Jazzita_bot) · 👊 MASHE (@For3s_Mashe_bot) — APAGADAS

- **Estado:** ⚪ apagadas (creadas, verificadas E2E, listas). Nacen con 0 episodios.
- **jazz:** dueña Jazz (@driade_1) — ella la encenderá cuando quiera (`for3s encender jazz`).
- **mashe:** dueño al primer /start — Brian decidirá qué hacer con ella.
- Existen en disco (sus volúmenes pgdata están), no consumen cupo mientras apagadas.

---

## 🔗 Lo que comparten vs lo aislado

- **Aislado por instancia:** red · base de datos · KEK (cifrado) · volúmenes · memoria. Cero cruce.
- **Compartido:** la máquina · la imagen v0.15.0 · **1 sola suscripción Claude** (⚠️ 1 cupo para
  las encendidas — si necesitas cupo, `for3s apagar general`).

## 📈 Lectura rápida

- **brian es el gigante** (21,640 vivos, 690 conceptos, 15 skills, 38 secretos) — todo el
  entrenamiento vive ahí, digiriéndose solo.
- **foresito es el maduro y sano** (820 episodios bien consolidados al 87%, microglía activa).
- **general está virgen** listo para tu equipo.
- **jazz/mashe dormidas** listas para sus dueños.

*Comando para re-verificar: `for3s listar` + queries a cada `for3s-<n>-postgres-1`.*
