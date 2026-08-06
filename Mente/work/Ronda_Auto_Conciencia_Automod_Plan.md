# 🧠 RONDA — AUTO-CONCIENCIA + AUTO-MODIFICACIÓN (AC1-AC4)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_Auto_Conciencia_Automod_Plan.md → work/Ronda_Auto_Conciencia_Automod_Plan.md (2026-07-30, ADR-029)

## Purpose

🧠 RONDA — AUTO-CONCIENCIA + AUTO-MODIFICACIÓN (AC1-AC4)


**Fecha:** 2026-07-01
**Origen (Brian 2026-06-25):** "hoy el agente NO reconoce sus propias mejoras; yo se las tengo que
agregar, no puede tocar su propia infraestructura. ESO ESTÁ MAL." Visión: un organismo que **se
conoce y se auto-modifica dentro de su caja** (contenedor), en el equipo de cada usuario.
**Estado:** ✅ **CONSTRUIDO COMPLETO 2026-07-01 — EN PRODUCCIÓN.** Las 4 fases + guardián de arranque,
probadas E2E y en vivo. Commits firmados: a5b1a14 (AC2) · 029cb8e (AC1) · 8b7a800 (AC3) · 2496355
(guardián) · 1eaccfd (AC4). En GitHub (oficial + privado).
**Regla de oro:** nada de auto-modificación sin el freno y sin red de seguridad (guardián). ✅ cumplida.

## ✅ RESULTADO (2026-07-01) — el bloque completo, verificado
| Fase | Qué hace | Comando | Verificación |
|---|---|---|---|
| **AC2** introspección | se conoce en vivo (módulos/tablas/migr/skills/comandos/jobs) | `/introspeccion` `/soy` + chat | 7/7 · bug `lifecycle` cazado |
| **AC1** auto-detección | nota qué cambió + diario, distingue propio/externo | `/cambios` | 5/5 + en vivo (detectó cambio real) |
| **AC3** auto-mod código | edita su código local (líneas rojas + entorno de prueba) | `/modificar` `/revertir` | 11/11 + E2E con LLM real |
| **guardián** arranque | si una auto-mod rompe → revierte a fábrica + avisa | (entrypoint.sh) | probado: overlay roto → recuperado + avisó |
| **AC4** auto-mod BD | modifica esquema (líneas rojas + backup + dry-run) | `/modificar_bd` | 13/13 + 6/6 evasión + producción |

**Doble red de seguridad:** PREVENTIVA (entorno de prueba de AC3 detiene el cambio malo antes) +
RESCATE (guardián revierte a fábrica si algo se escapa). El loop de muerte está roto.

**🔍 Bugs/hallazgos que la curiosidad+experimentos cazaron (evitaron fallos reales):**
- AC2: la columna de estado de skills es `lifecycle`, no `estado` → habría reportado "0 skills" (mentira).
- AC3: el import SOLO no basta (un módulo vaciado importa OK pero rompe el bot) → hizo falta el SMOKE.
- AC3: el scanner del governor (para skills de texto) da falsos positivos con código (bloqueaba
  version.py por mencionar 'KEK') → freno de código = líneas rojas + entorno de prueba, no patrones.
- AC3: `provider.complete` NO es async → `asyncio.to_thread` (no congelar el bot).
- Guardián: el código es COPY (no pip -e) → no había copia de fábrica para restaurar → se horneó `/app/factory`.
- AC4: un DROP COLUMN es DDL válido (pasa dry-run) pero borra datos → backup obligatorio ANTES.
- AC4: probado contra 6 evasiones (2-statements, línea roja disfrazada, mayúsculas) → todo bloqueado.

---

## (diseño original — histórico, ya construido) 🔽

---

## 0. La visión (LOCKED con Brian)

For3s como **organismo que se conoce y se adapta dentro de su caja**:
- **SE CONOCE** — introspección real en vivo (no una ficha que yo escribo).
- **SE MODIFICA** — edita su propio código fuente LOCAL (el de SU contenedor), **NUNCA GitHub** ni
  el repo de la verdad. Cada instalación es un individuo que evoluciona solo, aislado.
- **ACTÚA SOLO** — no pide permiso paso a paso; el control es ESTRUCTURAL (la caja + líneas rojas +
  rollback + guardián), no un humano aprobando cada cambio. Como un cuerpo que se regenera solo pero
  con sistema inmune que mata lo que sale mal.
- **CONTENIDO** — el contenedor es la JAULA de seguridad: el daño máximo posible es ese equipo; el
  ADN original (GitHub) queda intacto y es la "versión de fábrica" para resetear.

### Decisiones LOCKED (debate 2026-07-01)
| Tema | Decisión |
|---|---|
| Alcance de "editar código" | Solo SU contenedor local (el del equipo del usuario). NUNCA GitHub/repo de la verdad. |
| Gate | **Actúa solo** (no pide permiso). Ventana del dueño = diario (AC1) + audit + comando revertir. |
| Disparo de AC3 | El dueño se lo pide EN CHAT ("modifica tu código para X"); el agente lo ejecuta solo. (Iniciativa propia por DMN = diferida, sería `/automod on` a futuro.) |
| Persistencia | Volumen persistente + código base intacto + rollback individual reversible. |
| AC1 | PROFUNDO — diario propio; distingue "yo lo cambié" vs "me lo cambiaron desde fuera". |
| AC2 | TODO — módulos, tablas, migraciones, skills, jobs, comandos, capacidades, en vivo. |
| AC2 cómo se expone | Comando `/introspección` (o `/soy`) + auto en el chat ("¿cómo estás construido?") + insumo interno para AC3/AC4. |
| AC3 (código) | Actúa solo, LIBRE (con guardián + governor + audit). |
| AC4 (BD) | Actúa solo PERO con auto-verificación extra: backup + dry-run obligatorio antes de aplicar. |
| Líneas rojas ABSOLUTAS | NUNCA: governor/freno · audit chain · KEK/secrets. (Un sistema no modifica su propio control.) |
| Guardián de arranque | Script supervisor EXTERNO (fuera del código auto-modificable). |
| ⭐ ENTORNO DE PRUEBA previo | Antes de aplicar: punto de guardado + probar en sandbox aislado; si NO pasa, NO se aplica al contenedor + ALERTA al usuario ("rompe el código"). Preventivo (Brian 2026-07-01). |
| Orden de obra | AC2 → AC1 → AC3 → AC4 (conciencia/lectura primero, actuar/delicado al final). |

---

## 1. Análisis del sistema REAL (verificado en vivo 2026-07-01, "ser curioso")

Antes de diseñar, se auditó el contenedor real. Hallazgos que FUNDAN el plan:

1. **El código `/app` está HORNEADO en la imagen, NO montado.** Bind mounts actuales: solo
   `~/.for3s` (config/secrets) y `~/for3s-backups`. → Editar `/app` es **EFÍMERO** (se pierde al
   recrear el contenedor). CONFIRMA la necesidad del **volumen de mods** que decidimos.
2. **`/app` es ESCRIBIBLE desde dentro** del contenedor. → El agente SÍ puede editar sus `.py` (base
   de AC3), pero hoy SIN ninguna protección. El diseño debe añadir el freno.
3. **Arranca con `sh -c "python -m cli migrate && exec python -m telegram_channel"`** — hay una fase
   de MIGRACIÓN antes del bot. AC4 (auto-mod BD) toca justo esa fase.
4. **`restart: unless-stopped`** — si el bot muere, Docker lo reinicia solo. ⚠️ RIESGO: si el código
   está roto (en el volumen de mods), Docker reinicia → recarga el código roto → **loop de muerte**.
   → El guardián NO puede ser el propio Python; debe ser EXTERNO y anterior.
5. **NO hay entrypoint script hoy** (command directo). → Hay que introducir un `entrypoint.sh`
   (horneado, intocable) = el lugar natural del guardián.
6. **Cimientos que YA existen y se reutilizan:**
   - `governor.py` → `escanear()` (scanner fail-closed, síncrono) + `Veredicto` + kill switch +
     gate. **El freno de AC3/AC4 se reusa de aquí, no se reinventa.**
   - `health.py` → `reporte_completo` = el **health check del guardián de arranque** (ya existe).
   - `audit.py` → cadena SHA-256 (`hash_self = SHA-256(hash_prev + contenido)`) = la línea roja
     inmutable, **ya criptográficamente protegida**. Cada auto-mod deja eslabón aquí.
   - 50 módulos `.py` + 29 migraciones = lo que AC2 introspecciona y AC3/AC4 pueden tocar.

---

## 2. Arquitectura del diseño

### 2.1 El volumen de mods (la persistencia)
- Nuevo bind mount: `~/.for3s/mods` → `/app/mods` (sobrevive recreaciones, es del EQUIPO del usuario).
- Las auto-modificaciones NO se escriben sobre `/app/.../*.py` de la imagen. Se guardan como
  **overlays** en `/app/mods/` (el archivo modificado + metadatos: qué, cuándo, por qué, hash del
  original sobre el que se aplicó).
- Al arrancar, el guardián **aplica los mods sobre el código base** (copia el overlay encima). El
  código base de la imagen queda INTACTO → rollback = ignorar/borrar el overlay. Rollback individual
  = borrar UN overlay.

### 2.2-BIS ⭐ ENTORNO DE PRUEBA PREVIO (Brian 2026-07-01) — "prueba antes, aplica solo si pasa"
**La pieza que hace el diseño seguro DE VERDAD.** Cambia la filosofía de "aplica y si falla revierte"
(reactivo) a **"prueba en un sandbox y aplica SOLO si pasa"** (preventivo) → el contenedor real NUNCA
llega a romperse porque el cambio malo se detiene ANTES de tocarlo.

Flujo de TODA modificación de código (AC3) antes de aplicarse al contenedor vivo:
```
1. PUNTO DE GUARDADO — se crea una copia de seguridad ANTES de tocar nada (save point del
   estado actual: el código base + los overlays vigentes → restaurable al 100%).
2. ENTORNO DE PRUEBA AISLADO (sin Docker, respeta el diseño sin-DinD): se aplica el cambio a una
   COPIA del código en un directorio temporal y se verifica en un SUBPROCESO Python limpio:
     a. sintaxis (ast.parse) del/los archivo(s) modificado(s)
     b. IMPORT del módulo modificado en un proceso aislado (¿carga sin romper?)
     c. mini-arranque de prueba + health check (reporte_completo) con timeout
   🔍 Verificado en vivo (2026-07-01): subproceso Python aislado SÍ puede validar sintaxis + importar
   un módulo sin tocar el proceso vivo → el "entorno de prueba" es real y ligero, dentro de la caja.
3. DECISIÓN:
   ✅ PASA las 3 verificaciones → recién ENTONCES se aplica el overlay al contenedor real.
   ❌ NO PASA → NO se ejecuta en el contenedor (queda intacto) + ALERTA al usuario:
      "No puedo aplicar ese cambio: rompe mi código. Lo probé en un entorno aislado y [falló
       sintaxis / no importa / no arranca]. Me quedo como estaba." + queda en audit + diario.
```
**Doble red:** el entorno de prueba PREVIENE (el 99% de los casos malos se detienen aquí, el
contenedor ni se entera); el guardián de arranque (2.2) es la ÚLTIMA línea por si algo se escapa
(ej. un fallo que solo aparece en el arranque real). Nunca se depende de una sola.

### 2.2 El guardián de arranque (el sistema inmune) — entrypoint.sh
Script bash horneado en la imagen (FUERA del código auto-modificable). Reemplaza el command actual:
```
entrypoint.sh (intocable):
  1. aplicar overlays de /app/mods sobre el código base
  2. arrancar el bot en modo prueba + correr health check (reporte_completo) con timeout
  3. si el health check PASA  → exec del bot normal (queda corriendo)
  4. si FALLA (o no arranca en N seg) → descartar overlays (mover a /app/mods/cuarentena)
     → reintentar con código de FÁBRICA → avisar al dueño ("revertí una auto-mod que me rompía")
```
Esto rompe el loop de muerte: el que repara vive FUERA del código que se puede romper.

### 2.3 El freno (reusa governor H11)
Toda auto-mod pasa por:
- `governor.escanear(contenido)` — scanner fail-closed (¿el código nuevo tiene patrones peligrosos?).
- Chequeo de LÍNEAS ROJAS — ¿el archivo/tabla objetivo es governor / audit / KEK? → BLOQUEO duro.
- (AC4) backup + dry-run obligatorio antes de aplicar a la BD.
- Registro en audit (eslabón inmutable) + en el diario (AC1).

### 2.4 Líneas rojas (lista dura, en código)
Archivos/recursos que el agente NUNCA puede tocar (fail-closed):
`governor.py`, `audit.py`, `crypto.py`/KEK, `secret_store.py`, el propio `entrypoint.sh`/guardián,
y las tablas `audit_events` / `owner` / secrets. Intento de tocarlos → bloqueo + audit del intento.

---

## 3. Las 4 fases (orden LOCKED: AC2 → AC1 → AC3 → AC4)

### FASE AC2 · INTROSPECCIÓN (se conoce en vivo) — 🟢 SOLO LECTURA, cero riesgo
Módulo nuevo `introspeccion.py` que consulta EN VIVO su propia infra:
- módulos .py (nombre, líneas, docstring) · tablas/columnas (information_schema) · migraciones
  aplicadas (schema_version) · skills (SkillStore) · jobs del cron · comandos registrados ·
  capacidades reales.
- Se expone: (a) comando `/introspección` (o `/soy`); (b) auto al chat cuando preguntan "¿cómo estás
  construido?/qué puedes hacer?" (inyecta datos reales, no ficha estática — mejora AI5); (c) es el
  INSUMO interno que AC3/AC4 usan para modificarse con criterio.
- Prueba: `/introspección` lista los 50 módulos/29 migraciones reales; el chat responde con datos
  verdaderos verificables contra la BD.

### FASE AC1 · AUTO-DETECCIÓN (nota qué cambió) — 🟢 lectura + diario
- Al arrancar, hashea sus archivos core y compara con el hash de la última vez (guardado en volumen).
- Detecta: qué archivos cambiaron desde ayer + DISTINGUE origen: si el cambio está en `/app/mods`
  con su firma → "yo me lo hice"; si el archivo base cambió sin overlay suyo → "me lo cambiaron
  desde fuera" (ej. un rebuild/actualización).
- **Diario de cambios** propio (tabla o archivo en volumen): cada cambio con qué/cuándo/por qué/origen.
- Se expone: lo menciona al arrancar/en el chat ("detecté que X cambió") + comando `/cambios`.
- Prueba: modifico un archivo → al reiniciar lo detecta y lo clasifica bien (yo vs fuera).

### FASE AC3 · AUTO-MODIFICACIÓN DE CÓDIGO — 🔴 delicado (con toda la red)
- Disparo: el dueño lo pide en chat ("modifica tu código para X"). Flujo completo (con el ENTORNO
  DE PRUEBA de §2.2-bis como corazón):
  1. lee su código (AC2) → genera el cambio
  2. `governor.escanear` + líneas rojas → BLOQUEO si peligroso/prohibido
  3. **PUNTO DE GUARDADO** (save point del estado actual)
  4. **ENTORNO DE PRUEBA AISLADO** (subproceso, sin Docker): sintaxis + import + mini-arranque/health
  5. DECISIÓN: ✅ pasa → aplica el overlay a `/app/mods` (real) · ❌ falla → NO aplica + ALERTA al
     usuario ("no puedo, rompe mi código") — el contenedor queda INTACTO
  6. audit (eslabón) + diario (AC1)
- `/revertir` (individual, al punto de guardado) y `/revertir todo` (a fábrica). El guardián (2.2) es
  la ÚLTIMA red por si un fallo solo aparece en el arranque real.
- Prueba E2E: (a) cambio válido reversible → pasa el entorno de prueba → se aplica → `/revertir` lo
  deshace; (b) cambio con error de sintaxis → el entorno de prueba lo caza → NO se aplica + alerta;
  (c) cambio que importa pero rompe el arranque → el entorno de prueba (mini-arranque) lo caza ANTES;
  (d) intento de tocar línea roja → BLOQUEADO por el governor; (e) caso extremo que se escapa → el
  guardián de arranque revierte solo.

### FASE AC4 · AUTO-MODIFICACIÓN DE BD — 🔴🔴 lo más delicado, al final
- Igual que AC3 pero para el esquema (nuevas tablas/columnas/migraciones). Auto-verificación EXTRA:
  **backup automático** (reusa backup.py) + **dry-run** en transacción con ROLLBACK obligatorio ANTES
  de aplicar real. Si el dry-run falla → no aplica. Nunca toca tablas de línea roja.
- Prueba E2E: pedirle agregar una columna → backup + dry-run OK → aplica → verifica → revierte con
  el backup. + migración mala → el dry-run la caza y NO aplica.

---

## 4. Riesgos identificados (curiosidad) y su mitigación

| Riesgo | Mitigación en el diseño |
|---|---|
| Un cambio malo rompe el contenedor real | ⭐ ENTORNO DE PRUEBA previo (§2.2-bis): se prueba en sandbox aislado; si falla NO se aplica + alerta. El contenedor real nunca llega a romperse |
| Loop de muerte (código roto + restart) | Guardián EXTERNO (entrypoint.sh) descarta mods y arranca de fábrica — ÚLTIMA red, tras el entorno de prueba |
| El agente modifica su propio freno | Líneas rojas duras (governor/audit/KEK intocables, fail-closed) |
| Cambio efímero se pierde | Volumen de mods persistente (sobrevive recreaciones) |
| Migración mala corrompe datos | AC4: backup + dry-run obligatorio antes de aplicar |
| "Actúa solo" sin visibilidad | AC1 diario + audit inmutable + `/cambios` + `/revertir` |
| No poder revertir un cambio | Overlays individuales reversibles; base intacta siempre |
| Daño se propaga | Contenido en la caja; GitHub (ADN original) intacto = reinstalar resetea |

---

## 5. Lo que NO hace este diseño (fuera de alcance, a propósito)
- NO toca GitHub ni el repo de la verdad (solo el contenedor local).
- NO se auto-modifica por iniciativa propia todavía (disparo = petición del dueño en chat). La
  iniciativa nocturna (DMN, = H9-D4 prompt_improvement) queda como extensión futura `/automod on`.
- NO puede tocar governor/audit/KEK (líneas rojas absolutas).

---

## 6. Relacionado
- H11 GOVERNOR (el freno, se reusa) · H12 APRENDE (auto-genera skills; AC3 sube el nivel a código) ·
  AI5 version-self-awareness (AC2 lo vuelve dinámico) · audit chain (línea roja) · H9-D4
  prompt_improvement (la iniciativa propia futura) · Grafo §8.4 HARD NO-GO · REDISEÑO MEMORIA (misma
  disciplina de construcción fase-por-fase con pruebas E2E).
- Memoria: [[project_auto_conciencia_automod]].

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_Auto_Conciencia_Automod_Plan.md`).
