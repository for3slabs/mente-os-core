# Anexo R3 — Control por USO (no por tiempo): repo enorme en sub-bloques

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_03_Anexo_Control_Por_Uso_Subbloques.md → work/Ronda_03_Anexo_Control_Por_Uso_Subbloques.md (2026-07-30, ADR-029)

## Purpose

Anexo R3 — Control por USO (no por tiempo): repo enorme en sub-bloques


> **Tipo:** documento de diseño de implementación (anexo de R3, LLM layer).
> **Estado:** APROBADO por Brian (2026-06-14) — versión simple primero.
> **Origen:** Brian. El control anti-rate-limit actual es POR TIEMPO
> (`ESPACIADO_ENTRE_VUELTAS = 3.0s`). Brian pide cambiarlo a control POR USO:
> una fila donde el siguiente sub-bloque pasa a Claude SOLO cuando el anterior
> terminó, no "cada cierto tiempo".
> **Relación:** es la versión simple del hallazgo de fondo **H-C** (sistema de
> pensamiento por etapas). La versión completa de H-C queda para una Ronda futura.

---

## 0. El problema (lo que Brian detectó)

Hoy controlamos el rate-limit **por tiempo**: `sleep(3.0s)` entre vueltas del
loop tool-use. Brian: *"debes controlar por USO, no por tiempo."*

**Por qué el tiempo es una adivinanza:**
- Si Claude tarda 1s, los 3s desperdician 2s (lento sin motivo).
- Si Claude tarda 5s, los 3s no alcanzan → igual hay riesgo de ráfaga.
- El tiempo no sabe nada del uso real de Claude → o sobra o falta.

**La causa raíz del fallo con repos enormes (confirmada en el código):**
- Un análisis de repo cabe HOY en UN solo `run_tool_loop` con `MAX_TOOL_ROUNDS=5`.
- Un repo enorme tiene cientos de archivos → 5 vueltas no alcanzan → se queda
  corto. Y si subiéramos el tope, encadenaría muchas llamadas pesadas (cada
  vuelta reenvía historial + schemas) → ESO satura el rate-limit por-minuto.

---

## 1. La idea de Brian (control por uso = fila de 1)

```
REPO ENORME                          ← "bloque grande"
   ├── archivo_1                     ← sub-bloques
   ├── archivo_2
   ├── archivo_3
   └── ... archivo_N
```

**Regla:** un sub-bloque pasa a Claude **solo si Claude está libre**.
No "cada X segundos" — sino "cuando el anterior TERMINÓ".

```
archivo_1 → Claude lo procesa     (Claude ocupado)
archivo_2 → ESPERA                (Claude ocupado, NO entra)
   ...Claude termina el 1...
archivo_1 → For3s GUARDA/ACOMODA en el servidor  ← aquí se libera el turno
archivo_2 → Claude                (ahora sí, porque se liberó)
archivo_3 → ESPERA
   ...
→ reporte final ARMADO desde lo acomodado en el servidor
```

Como una caja de banco con UN cajero: nadie pasa hasta que el de adelante
terminó. **Imposible saturar porque nunca hay 2 a la vez en Claude.**

**Trade-off que Brian acepta explícitamente:** tarda más en contestar. No
importa. Lo que importa es **cero ráfagas, cero 429**. No queremos "todo
rápido"; queremos "todo sin saturar".

---

## 2. La segunda mitad: la carga se mueve a For3s, no a Claude

Cada sub-bloque que termina **no se queda esperando todo junto al final**. Su
información llega "poco a poco" y For3s la va **acomodando/reconstruyendo** en
el servidor (tablas `gh_resources` / `gh_files`) mientras el siguiente
sub-bloque corre.

- **Claude** solo ve un sub-bloque a la vez (lectura/análisis de 1 archivo).
- **El armado del rompecabezas** (juntar todo en un panorama del repo) pasa en
  el **servidor For3s**, donde NO hay rate-limit.
- → La saturación posible se mueve de Claude (caro, limitado) al servidor
  (barato, nuestro).

Esto es la semilla del "sistema de pensamiento" de H-C: For3s deja de mandar el
repo de golpe y empieza a construir conocimiento en su propia memoria por etapas.

---

## 3. Decisiones de diseño (respondidas por Brian)

```
   • Granularidad del sub-bloque: POR ARCHIVO. Cada sub-bloque = 1 archivo del
     repo (natural con get_file_contents del MCP). Se reconstruye archivo a archivo.
   • Señal de "TERMINÓ": Claude respondió Y For3s ya guardó/acomodó en BD.
     Recién ahí entra el siguiente. Garantiza que la reconstrucción nunca se
     queda atrás del flujo.
   • Feedback UX: PROGRESO INCREMENTAL en Telegram ("procesando 3/20...") +
     reporte final. Conecta con H-A (multi-mensaje) ya iniciado.
```

---

## 4. Lo que se REUSA (no reinventar)

- **`gh_lock` (asyncio.Lock)** de `telegram_channel.py` → YA es el semáforo;
  pasa de "serializar tareas" a "serializar sub-bloques dentro de una tarea".
- **`gh_resources` / `gh_files`** (migración 004) → YA es donde se acomoda la
  reconstrucción.
- **`save_gh_tool_calls()`** → el punto exacto donde "se guarda y se libera el turno".
- **`run_tool_loop`** → se reusa por sub-bloque (mini-loop de pocas vueltas para
  leer + analizar 1 archivo), no se reescribe.

## 5. Lo que se CONSTRUYE (nuevo)

Un orquestador de sub-bloques (`subbloques.py`):
1. Lista los archivos del repo (1 llamada: árbol/contenido raíz del repo).
2. Arma la cola de sub-bloques = lista de archivos.
3. Por cada archivo, EN SERIE (await secuencial = control por uso):
   a. lee+analiza el archivo (mini run_tool_loop acotado).
   b. guarda/acomoda en `gh_resources` (aquí "termina" el sub-bloque).
   c. 📲 progreso `i/N` a Telegram.
4. Al final: arma el reporte desde lo acomodado en BD.

**El control por uso es el `await` secuencial**: el `for` no avanza al siguiente
archivo hasta que el `await` del actual (procesar + guardar) terminó. Es la fila
de 1, sin `sleep`.

## 6. El `ESPACIADO_ENTRE_VUELTAS = 3.0` (qué pasa con él)

- DENTRO de un mini-loop por archivo, las vueltas ya son por uso (cada `await
  complete_with_tools` espera a Claude). El `sleep(3.0)` era un colchón ADICIONAL
  por tiempo.
- Decisión: **bajarlo o quitarlo** dentro del flujo por sub-bloques (el control
  ya es por uso). Se puede dejar como red de seguridad mínima (ej. 0.5s) solo
  para no martillar, pero ya NO es el mecanismo principal.

---

## 7. Alcance de esta versión simple (vs H-C completo)

ESTA versión simple resuelve: repos enormes sin saturar + reconstrucción
incremental en el servidor + progreso al usuario.

QUEDA para H-C completo (Ronda futura): el "sistema de pensamiento" estructurado
tipo Mente OS (estados ricos, etapas semánticas análisis→testeo→PoC,
priorización de qué archivos leer primero, resúmenes jerárquicos). Detalle en
`memory/archive/For3s_LO_QUE_NO_PUEDE_HACER.md` (H-C).

---

## 8. Lo que NO hacemos (descartado con razón)
- ❌ Control por tiempo como mecanismo principal (es adivinanza — esto lo reemplaza).
- ❌ Procesar todos los archivos en paralelo (ráfaga = 429; justo lo que evitamos).
- ❌ Mandar el repo completo de golpe a Claude (no cabe / satura).
- ❌ Subir MAX_TOOL_ROUNDS sin límite (encadenaría llamadas pesadas → satura).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde v1).
