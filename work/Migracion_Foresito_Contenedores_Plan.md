# Migración de Foresito → Contenedores — PLAN SUPER DETALLADO

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Migracion_Foresito_Contenedores_Plan.md → work/Migracion_Foresito_Contenedores_Plan.md (2026-07-30, ADR-029)

## Purpose

Migración de Foresito → Contenedores — PLAN SUPER DETALLADO


> **Qué es:** plan minucioso para convertir a **Foresito** (el For3s OS de producción que
> Brian usa por Telegram, corriendo SUELTO con systemd) a la **estructura contenerizada**
> (docker-compose, la misma del producto en GitHub) — **conservando TODA su memoria**.
>
> ⚠️ **Lo más delicado que hemos tocado:** la memoria real de Foresito (740 turnos +
> grafo + skills + perfil + audit). Regla absoluta: **nada se ejecuta sin backup verificado
> y sin aprobación de Brian.** Cero código hasta que el plan esté aprobado.
>
> Fecha: 2026-06-27. Estado: PLAN (no ejecutado).

---

## 0. El estado de HOY (lo que vamos a migrar)

**Foresito corre SUELTO (no contenerizado):**
```
servidor for3s:
  systemd → for3s-telegram (bot)   ← suelto
  systemd → for3s-worker (jobs)    ← suelto
  PostgreSQL del SISTEMA (localhost:5432/for3s)  ← suelto
  Valkey del SISTEMA               ← suelto
  código en ~/for3s-os             ← suelto
```

**Su memoria (lo SAGRADO que NO se puede perder) — BD de 25 MB en 3 esquemas:**
- **`public`** (23 tablas): episodes_events (740 turnos), audit_events (1455),
  dmn_corridas (161), skills (2), sessions (4), perfil/temas/governor/dmn_estado, etc.
- **`for3s_kg`** (15 tablas): el GRAFO de conocimiento (AGE) — Episodio (74), Concepto (10),
  DERIVED_FROM (74), DUENO_DE, Owner, Repo, etc.
- **`ag_catalog`** (2 tablas): catálogo de AGE (registra el grafo `for3s_kg`).
- **Extensiones:** age 1.6.0, pgvector 0.8.2, pgcrypto 1.3, plpgsql.

**Fuera de la BD (también hay que preservar):**
- **La KEK:** `~/.for3s/master.key` (cifra los secrets). SIN ella, los tokens cifrados
  en la tabla `secrets` son ilegibles. ⚠️ CRÍTICA.
- **`~/.for3s/`** otros: telegram_owner.json, telegram_cupo_pin.json.
- **El `.env`** (tokens en claro de arranque).

---

## 1. ⚠️ RIESGOS identificados (y su mitigación)

| Riesgo | Gravedad | Mitigación |
|---|---|---|
| Perder los 740 turnos / grafo al migrar | 🔴 CRÍTICO | Backup COMPLETO verificado ANTES de tocar nada + NO borrar el origen hasta validar |
| El grafo AGE (`for3s_kg`+`ag_catalog`) no migra con pg_dump simple | 🔴 ALTO | pg_dump de TODA la BD (no por tabla) incluye todos los esquemas; verificar que el grafo llegó |
| La KEK no llega al contenedor → secrets ilegibles | 🔴 ALTO | Montar `~/.for3s` como volumen en el contenedor (ya está en el compose); verificar descifrado |
| Choque de puertos (Postgres sistema 5432 vs contenedor) | 🟡 MEDIO | El compose usa red interna; el Postgres del contenedor NO expone 5432 al host |
| Downtime de Foresito durante la migración | 🟡 MEDIO | Ventana corta; Foresito queda abajo solo mientras se migra y valida |
| Versión de extensiones distinta (pgvector 0.8.2 sistema vs 0.8.0 imagen) | 🟡 MEDIO | Verificar compatibilidad; 0.8.0→0.8.2 es compatible hacia adelante |
| Reversibilidad (si algo sale mal, volver a Foresito-suelto) | 🟢 BAJO | NO se desinstala nada del sistema hasta validar 100%; rollback = re-encender systemd |

**REGLA DE ORO:** el Foresito-suelto actual **NO se apaga ni se borra** hasta que el
Foresito-contenedor esté **verificado funcionando con toda la memoria**. Si algo falla,
se re-enciende el systemd y volvemos al estado actual (cero pérdida).

---

## 2. PLAN POR FASES (cada una con verificación + punto de no-retorno marcado)

### FASE 0 — BACKUP TOTAL (red de seguridad, ANTES de todo) 🔴
- 0.1 `pg_dump` COMPLETO de la BD `for3s` (todos los esquemas: public + for3s_kg +
  ag_catalog) → archivo `.sql` con fecha.
- 0.2 Copiar `~/.for3s/` completo (KEK + jsons) a un backup aparte.
- 0.3 Copiar el `.env`.
- 0.4 **VERIFICAR el backup:** restaurarlo en una BD temporal de prueba y confirmar que los
  740 turnos + el grafo + los secrets están. SIN esta verificación, NO se sigue.
- 0.5 Guardar copia del backup FUERA del server (descarga local) — doble red.
- ✅ Gate: backup existe, restaura OK, copia externa hecha → continuar.

### FASE 1 — PREPARAR el contenedor (sin tocar Foresito-suelto aún)
- 1.1 Asegurar que las imágenes están construidas (for3s-agent + for3s-postgres ya lo están).
- 1.2 Ajustar el `.env` del compose con los tokens REALES de Foresito (Claude, Telegram).
- 1.3 Decisión de datos del Postgres del contenedor: arrancar el contenedor postgres VACÍO
  (solo esquema vía migraciones) y luego CARGAR el dump de Foresito encima. (Ver Fase 2.)
- 1.4 Confirmar que el compose monta `~/.for3s` (la KEK) — ya está en el diseño.
- ✅ Gate: imágenes listas, .env con datos reales, sin tocar producción aún.

### FASE 2 — MIGRAR LA MEMORIA (el corazón) 🔴 punto delicado
- 2.1 Levantar SOLO el contenedor `postgres` del compose (no el agente aún).
- 2.2 Dejar que cree la BD + extensiones (age/vector/pgcrypto) — verificar que están.
- 2.3 **Cargar el dump de Foresito** en el Postgres del contenedor (restore del .sql de Fase 0).
  ⚠️ Orden AGE: puede requerir `LOAD 'age'` + crear el grafo antes de cargar sus tablas, o
  que el dump traiga el grafo. Verificar el grafo `for3s_kg` tras el restore.
- 2.4 **VERIFICAR la memoria migrada:** contar turnos (=740), skills (=2), nodos del grafo
  (Episodio=74, Concepto=10), audit (=1455). Deben COINCIDIR con el origen.
- ✅ Gate: la BD del contenedor tiene EXACTAMENTE la memoria de Foresito → continuar.

### FASE 3 — ARRANCAR Foresito-contenedor (con Foresito-suelto AÚN vivo en paralelo)
- 3.1 ⚠️ PROBLEMA: dos bots con el MISMO token de Telegram NO pueden correr a la vez
  (Telegram solo permite un poller por token). → Hay que APAGAR el Foresito-suelto JUSTO
  antes de arrancar el contenedor (ventana de downtime corta).
- 3.2 Apagar systemd: `systemctl stop for3s-telegram for3s-worker` (NO disable aún — para
  poder revertir rápido).
- 3.3 Levantar el compose completo (agent + worker + postgres[ya con datos] + valkey).
- 3.4 El agente corre migraciones (no-op, ya están) + arranca el bot.
- ✅ Gate: el bot del contenedor responde en Telegram.

### FASE 4 — VERIFICACIÓN EN VIVO (que Foresito recuerde de verdad) 🔴
- 4.1 Brian escribe a Foresito por Telegram: ¿responde?
- 4.2 Prueba de MEMORIA: "¿en qué quedamos?" / preguntarle algo viejo → debe recordar
  (prueba que el grafo + episodios migraron y que la KEK descifra sus secrets).
- 4.3 Prueba de secrets: que use GitHub o algo que requiera un token cifrado → si funciona,
  la KEK migró bien.
- 4.4 Revisar logs del contenedor: sin errores de BD/KEK/grafo.
- ✅ Gate: Foresito-contenedor funciona con TODA su memoria → migración exitosa.

### FASE 5 — CIERRE (solo tras validar 100%)
- 5.1 `systemctl disable for3s-telegram for3s-worker` (ya no arrancan solos — el contenedor manda).
- 5.2 Dejar el systemd-Foresito como rollback disponible unos días (no borrar).
- 5.3 Documentar el cambio: Foresito ahora corre contenerizado (= estructura del producto).
- 5.4 (Opcional, días después) si todo estable: limpiar el Postgres del sistema viejo.

---

## 3. PLAN DE ROLLBACK (si algo sale mal en cualquier fase)
1. Apagar el compose: `docker compose down` (NO con -v — preservar el volumen por si acaso).
2. Re-encender Foresito-suelto: `systemctl start for3s-telegram for3s-worker`.
3. Foresito vuelve al estado actual EXACTO (su BD del sistema nunca se tocó — solo se leyó
   para el dump). Cero pérdida.
> Por esto la FASE 0 (backup) + NO borrar el origen son sagrados: el rollback siempre existe.

---

## 4. DECISIONES QUE BRIAN DEBE TOMAR (debatir antes de ejecutar)

- **D1 — ¿Cuándo migrar?** Hay una ventana de downtime (Fase 3): Foresito estará caído unos
  minutos mientras se apaga el systemd y arranca el contenedor. ¿Cuándo te conviene?
- **D2 — ¿El Postgres del contenedor reemplaza al del sistema, o conviven?** Recomiendo que
  el contenedor sea el nuevo hogar y el del sistema quede como respaldo unos días.
- **D3 — ¿Migramos también Valkey?** Valkey es solo cache/cola (no memoria permanente). Se
  puede arrancar vacío en el contenedor sin pérdida (se re-llena solo). Recomiendo: vacío.
- **D4 — ¿La KEK se queda en `~/.for3s` del host (montada al contenedor) o se mueve?**
  Recomiendo: se queda en el host, montada como volumen (más seguro, ya diseñado así).

---

## 5. Lo que NO se pierde (resumen tranquilizador)
Con este plan, Foresito conserva: sus 740 turnos · el grafo de conocimiento · sus 2 skills ·
su perfil · el audit chain (1455) · sus secrets (vía la KEK) · su identidad. Solo cambia
DÓNDE vive (de suelto → contenedor), no QUÉ es ni QUÉ recuerda.

> Refs: Fase_PreTesters_Plan.md (la estructura de contenedores del producto) ·
> memoria project_repo_oficial_for3s · H6 backup (backup.py existente reutilizable en Fase 0).

---

## ✅ DECISIONES TOMADAS (Brian 2026-06-27)
- **D1 = AHORA** (ejecutar al terminar el plan).
- **D2 = A** — Postgres del sistema queda como respaldo unos días, luego se limpia.
- **D3 = A** — Valkey arranca vacío en el contenedor (cache, se re-llena solo).
- **D4 = A** — KEK se queda en el host (~/.for3s) montada al contenedor.

---

## ✅ EJECUCIÓN COMPLETA — MIGRACIÓN CERRADA (2026-06-28)

**Fases 0-4 ✅** (ver Bitácora 2026-06-28): backup verificado · memoria migrada (738 turnos +
grafo AGE 559 Episodios/54 Conceptos) · systemd apagado + 4 contenedores arrancados · verificado
en vivo (Foresito recuerda 15/22/25/27 jun + "pizza 🍕", Sme G intacta). 🐛 bug owner→sesión
vacía cazado y resuelto (montar `~/.for3s`→`/app/.for3s`).

**FASE 5 ✅ CERRADA (2026-06-28):**
- 5.1 `systemctl disable for3s-telegram for3s-worker` → ✅ ahora `disabled` + `inactive`. El
  Foresito viejo YA NO arranca solo → **cero riesgo de choque de tokens en un reinicio**.
- 5.2 Unit files PRESERVADOS (`/etc/systemd/system/for3s-{telegram,worker}.service`) +
  Postgres del sistema intacto → **rollback completo sigue disponible** unos días
  (`systemctl start ...` revive el viejo). NO borrar todavía.
- 5.3 Documentado: **Foresito ahora corre CONTENERIZADO** (misma estructura del producto).
- ✅ Verificado: los 4 servicios del compose tienen `restart: unless-stopped` → el contenedor
  SÍ arranca solo en reinicio. Foresito nuevo = arranque automático; viejo = ya no. Coherente.
- ⏳ 5.4 (días después, cuando todo estable): limpiar el Postgres del sistema viejo + (opcional)
  borrar los unit files. NO urgente.

> 🎉 **MIGRACIÓN 100% COMPLETA.** Foresito vive ahora en contenedores conservando toda su
> memoria. Solo cambió DÓNDE vive, no QUÉ es ni QUÉ recuerda.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Migracion_Foresito_Contenedores_Plan.md`).
