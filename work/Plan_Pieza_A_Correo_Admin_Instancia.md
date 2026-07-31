# 🧩 Plan detallado — Pieza A: correo admin por instancia (el puente identidad web ↔ instancia)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Plan_Pieza_A_Correo_Admin_Instancia.md → work/Plan_Pieza_A_Correo_Admin_Instancia.md (2026-07-30, ADR-029)

## Purpose

🧩 Plan detallado — Pieza A: correo admin por instancia (el puente identidad web ↔ instancia)


> **Pendiente madre:** Conectores self-service (`vision/Vision_Conectores_SelfService_Panel_Agente.md`).
> **Método pieza por pieza** (regla Brian 2026-07-20). Pieza A = 2ª que se construye (tras E).
> **Visión alineada + decisiones tomadas (Brian, 2026-07-20). Este plan → aprobar → construir.**
> Proyecto: For3s OS (server). Creado 2026-07-20.

---

## 0 · Qué resuelve (visión alineada con Brian)

Hoy la identidad del "dueño" de una instancia es un **`owner_id` de Telegram (numérico)** — quien
da el primer `/start`. **No existe correo.** La demo web usa **correo** (registro de la demo,
`for3s_demo`). Son dos mundos sin puente.

**La pieza A crea ese puente:** cada instancia guarda el **correo de su admin**. Así, cuando ese
correo entra a la demo web, el sistema sabe **a qué instancia real pertenece** → base de la
decisión raíz (la demo habla con instancias REALES) y de B (general multi-tenant), C (conectores),
D (API keys self-service).

## 1 · Decisiones tomadas (Brian, 2026-07-20)

- **A-D1 · Propósito:** el correo es el **PUENTE identidad web ↔ instancia** (no una etiqueta suelta).
- **A-D2 · Dónde vive:** en la **instancia** — columna `admin_email` en la tabla `owner` de su BD.
  La instancia es dueña de su identidad; la web la consulta por el canal API.

## 2 · Terreno investigado (2026-07-20, server)

- **Tabla `owner`** (migr `024_owner.sql`): `workspace TEXT PK DEFAULT 'default'`, `owner_id BIGINT`,
  timestamps. 1 fila (single-owner). `workspace` ya está pensado para multi-tenant futuro (útil para B).
- **`OwnerStore`** (`telegram_channel.py:363`): BD = fuente de verdad + JSON caché + caché memoria.
  Métodos: `get_owner()` (sync), `sync_con_bd()`, `set_owner()`, `set_owner_bd()`, `transferir()`.
- **Canal API** (`For3s-OS/.../api_channel.py`): `/v1/health`, `/v1/chat`, `/v1/maestro/*`. Tiene `_identidad(auth)`
  y `_health`. NO expone hoy el correo admin (no existe).
- **Correos objetivo:** brian→brayan002150@gmail.com · Foresito→fruterito101@gmail.com ·
  jazz/mashe→pendientes de Brian. General → NO tiene correo fijo (su admin depende del usuario, es
  pieza B; A solo maneja las instancias de dueño único).

## 3 · Contratos con otras piezas (para que NO se construya por separado)

- **Contrato A→B:** la columna `admin_email` en `owner` sirve para instancias de dueño único
  (brian/foresito/jazz/mashe). Para **general** (multi-tenant, muchos correos), B usará la MISMA
  columna pero por-usuario en su tabla de personas/hilos — A deja el patrón, B lo eleva. La columna
  `workspace` de `owner` es el gancho.
- **Contrato A→web:** el correo se consulta por el canal API (`/v1/whoami` nuevo, §4.3). El sitio
  NO lee la BD de la instancia directo — habla por la puerta (coherente con "un cliente más del API").
- **Contrato A→C/D:** una vez que la web sabe qué instancia es del correo, C/D cuelgan de esa
  identidad (los conectores y API keys se ligan a la instancia que A identificó).

## 4 · Plan por fases

### A1 · Migración: `admin_email` en la tabla `owner`
- Migración nueva (`047_owner_admin_email.sql`): `ALTER TABLE owner ADD COLUMN IF NOT EXISTS
  admin_email TEXT;` — normalizado a minúsculas por convención (como la demo). Idempotente.
- *Investigar terreno:* la tabla ya existe en todas las instancias (migr 024). ADD COLUMN IF NOT
  EXISTS es seguro y no toca `owner_id`. *Red:* migración corre en fresco y en instancia viva sin romper.

### A2 · OwnerStore sabe leer/escribir el correo
- Ampliar `OwnerStore`: `get_admin_email()` (sync, con caché igual que `get_owner`) +
  `set_admin_email_bd(pool, email)` (normaliza minúsculas, upsert en la fila `default`).
- *Defensivo:* si la columna no existe (instancia sin migrar) → cae a None, no rompe (patrón
  de `sync_con_bd`). El correo es aditivo: sin él, todo sigue como hoy.
- *Red:* set/get round-trip; email None cuando no configurado; normalización (Mayús→minús).

### A3 · Sembrar el correo de cada instancia (config, no hardcode)
- **Cómo entra el correo la 1ª vez:** por **ENV** `FOR3S_ADMIN_EMAIL` en el `.env` de cada
  instancia (como `FOR3S_PERFIL`). En `setup()`/`start()`, si la BD no tiene `admin_email` y el
  ENV lo trae → se siembra (patrón de `sync_con_bd` que migra JSON→BD). **Fuente de verdad = BD**
  (viaja con backups); el ENV solo siembra. Así cambiarlo después no exige redeploy (se puede por
  comando/API), pero el arranque lo deja listo.
- Sembrar: brian→brayan002150@gmail.com · Foresito→fruterito101@gmail.com. jazz/mashe cuando Brian
  dé los correos (dejar el ENV vacío hasta entonces → admin_email None, inofensivo).
- *Red:* instancia con ENV → BD tiene el correo tras arrancar; sin ENV → None sin romper.

### A4 · Exponer el correo por el canal API (`/v1/whoami`)
- Endpoint nuevo `GET /v1/whoami` (auth con la key demo/cliente, como `/v1/maestro/salud`):
  devuelve `{ instancia, admin_email, perfil }` — SIN datos sensibles (el correo del admin NO es
  secreto; es identidad de contacto). Fail-closed: sin auth → 401.
- Este es el endpoint que el sitio (pieza B) consultará para mapear correo→instancia.
- *Red:* whoami con auth → 200 + correo correcto; sin auth → 401; instancia sin correo → email null.

### A5 · Comando de dueño para ver/cambiar su correo (opcional, Telegram)
- `/soy` ya muestra identidad; sumar el `admin_email` a su salida. Comando `/correo <email>` (solo
  el owner) para fijarlo/cambiarlo sin redeploy → llama `set_admin_email_bd`. Auditado.
- *Decidir con Brian al construir:* ¿hace falta el comando ya, o basta el ENV+API por ahora?

## 5 · Batería (§5-BIS)
- Tests: OwnerStore get/set email (round-trip, None, normalización) + migración idempotente.
- Arranque real de una instancia con `FOR3S_ADMIN_EMAIL` → BD tiene el correo · `/v1/whoami`
  responde con él · sin ENV → email null sin romper · `/soy` lo muestra.
- Verificar en las 3 vivas (brian/foresito/general): brian y foresito con su correo, general con
  null (correcto, su admin es por-usuario = pieza B). `/salud` 0 FAIL. Sin regresión del owner_id.
- Tríada + firma. Server-primero (push solo con orden).

## 5-BIS · CONSTRUCCIÓN (2026-07-20) — bugs cazados + estado

**Construido:** migración 047 (`admin_email` en `owner`) · `OwnerStore` con
`get_admin_email`/`set_admin_email_bd`/`sync_admin_email_bd` + `_norm_email` · siembra por ENV
`FOR3S_ADMIN_EMAIL` en `setup()` + compose + `.env` (foresito=fruterito101, brian=brayan002150) ·
`/v1/whoami` en el canal API · `/soy` muestra el correo · 3 tests nuevos (269 verdes) · ruff/ty ✅.

**🐛 3 bugs cazados en MI código durante la construcción (curiosidad que caza bugs):**
1. **`set_admin_email_bd` creaba fila `owner` con `owner_id=0` falso** si no había owner aún
   (INSERT+COALESCE). Corregido a UPDATE puro: si no hay fila, el correo queda en caché y se
   persiste cuando llega el /start (vía `set_owner_bd`, que ahora lleva el email pendiente con
   `COALESCE(owner.admin_email, EXCLUDED...)` para no pisar uno existente).
2. **Tipo sucio `str | None | bool`** con sentinel `False` → `ty` marcó `Literal[True]` no
   asignable. Reescrito a dos campos limpios: `_email_cache: str | None` + `_email_synced: bool`.
3. **General NO debe recibir correo:** su `.env` se dejó SIN `FOR3S_ADMIN_EMAIL` a propósito
   (su admin es por-usuario = pieza B). Verificado que arranca con admin_email None sin romper.

## 6 · Fuera de alcance de la pieza A
- General multi-tenant (B) · conectores (C) · API keys self-service (D) · el mapeo real
  correo→instancia EN LA WEB (eso lo consume B usando el `/v1/whoami` que A construye).

## 7 · Riesgos vigilados
- **No romper el owner_id existente:** admin_email es ADITIVO; la autorización sigue por owner_id.
- **Correos de jazz/mashe faltan:** dejar su ENV vacío → admin_email None, sin efecto. Se llenan
  cuando Brian los dé (sin redeploy si se usa el comando/API).
- **General NO debe tener admin_email fijo:** su identidad es por-usuario (B). A no le pone correo.

---

*Relacionado: `vision/Vision_Conectores_SelfService_Panel_Agente.md` (§A + §2-BIS decisión raíz) ·
`blocks/active/demo/docs/plan-piece-e-admin.md` (pieza previa) · memoria `project_conectores_selfservice`.*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Plan_Pieza_A_Correo_Admin_Instancia.md`).
