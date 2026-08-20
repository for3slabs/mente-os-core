# 🌐 RONDA F0 — MENTE OS MAESTRO (el super-cerebro conectado)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

## Purpose

🌐 RONDA F0 — MENTE OS MAESTRO (el super-cerebro conectado)


> **Estado: ✅✅ COMPLETO F1→F5 (2026-07-17).** El super-cerebro conectado ya vive. Motor entero
> construido y verificado E2E; primer piloto real (Jazz) funcionando. Evoluciona a CARRIL (mejora
> continua) + queda enganchado a Pendiente A (entrenar Foresito con el Maestro).
>
> **LO CONSTRUIDO (todo en `Mente/Maestro/`, repo `for3slabs/mente-os-maestro` privado):**
> - **F1 registro** (`Maestro/registro.md`): apunta a 5 ramas (For3s OS, marca-personal, Foresito, instancias, NavigoX-gate) + Diseño Jazz.
> - **F2 puentes**: `maestro` — A (git efímero, `leer`/`grep`, no replica) + B (canal API vivo, `vivo`). Rama madre versionada en `mente-os-core`.
> - **Bienvenida** (`Maestro/BIENVENIDA.md`): protocolo de onboarding al clonar (lee CLAUDE.md/.claude/.agents + pregunta rama/descripción obligatoria).
> - **F3 crear rama** (`mente-os-nueva`): genera {Alma,Cerebro,Cuerpo,Doc}+RETOMAR desde plantilla, descripción obligatoria, ficha para registro.
> - **F4 permisos** (`Maestro/permisos.md` + puerta en `maestro`): por persona/carril, fail-closed, reusa H8. Colaborador ve solo su carril.
> - **F5 piloto Jazz**: rama REAL `mente-os-diseno-jazz` (privado) creada, registrada, con permiso. E2E: Jazz ve su rama, NO ve el núcleo.
>
> **Pendiente (post-cierre):** F6 fino (este doc) · engancharlo a Pendiente A (Foresito lee el Maestro, puente E) · Jazz clona y usa cuando quiera.

> **[HISTÓRICO] Estado inicial: ARQUITECTURA APROBADA por Brian 2026-07-17.** Es el pendiente
> estratégico MÁS GRANDE.
>
> **DECISIONES LOCKED (Brian 2026-07-17):**
> 1. **Maestro NUEVO** (no promover `~/for3s/Mente`). **LIGERO: tiene lo IMPORTANTE + reglas, y
>    APUNTA a lo ya creado.** Regla madre del Maestro: *"no replicamos información, la CONECTAMOS."*
>    Apuntar en vez de copiar es lo que hace que la conexión exista sin volverse un monstruo de tokens.
> 2. **Las 3 formas de conexión conviven, por fases. ARRANQUE = GIT** (el Maestro apunta a cada rama
>    por git = versionado + colaboración para Jazz). Luego se suma índice/rutas (lo que no es git) y
>    el canal API en fase 2 (instancias en vivo).
> 3. **Unidireccional** (Maestro LEE las ramas) + **permisos por persona/carril** (reusa roles H8).
> 4. **El Maestro APUNTA a Foresito** — Foresito es una rama/consumidor del Maestro (Pendiente A se
>    alimenta del Maestro).
> 5. **Fases F1→F6 aprobadas. F1 (el registro) es el primer paso.**
> **Origen/visión:** `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md` (el contrato).
> **Método:** `rules/ESTANDAR_Metodo_Fases_F.md` — explicar → **aprobar** → construir. NADA se
> construye hasta que Brian apruebe la arquitectura y las decisiones abiertas (§4).

---

## 1 · Recordatorio del objetivo (en una frase)

Un **Mente OS MAESTRO** que sea el cerebro CONTROLADOR: conoce TODOS los Mente OS regados (hoy
desconectados), permite **crear ramas nuevas** (ej. el Mente OS de Diseño de Jazz), las **lee/
conecta**, y **gestiona permisos por persona** — para que For3s deje de ser "el proyecto de Brian"
y sea **colaborable**, sin que nadie esté "a un mar de diferencia".

## 2 · El terreno REAL (investigado 2026-07-17 — sobre esto se diseña, no sobre teoría)

| Mente OS | Ruta | Tamaño | Estado | Rol futuro |
|---|---|---|---|---|
| **For3s OS** (el principal) | `~/for3s/Mente` | 4.3 MB · 169 docs · **NO en git** | el más rico | ⭐ candidato a MAESTRO (o su semilla) |
| Marca personal / QA | `~/for3s/marca-personal/Mente` | 128 KB · 5 docs | ⚠️ OTRO proyecto | rama SEPARADA (scope aparte, gate) |
| Clon del repo | `~/for3s/For3s-OS` | — | **NO es Mente OS** (es código) | no aplica — corrección al mapa de la visión |
| Instancias (brian/general/jazz/mashe/Foresito) | volumen `persona/mente-os/` c/u | por diseño | ya existe el patrón "mini Mente OS por instancia" | ramas (una por agente) |
| Server for3s | la BD de cada instancia (22K episodios en brian) | — | memoria VIVA (episodios+grafo) | fuente que el Maestro indexa |

**Hallazgos que MOLDEAN el diseño:**
1. `~/for3s/Mente` **no está en git** → hoy no hay versionado ni sincronización. Cualquier "conexión"
   parte de aquí (git sería la base natural del control de versiones + colaboración).
2. **Ya existe el patrón `mente-os/{Alma,Cerebro,Cuerpo,Doc}` por instancia** (hito Identidad Viva) —
   o sea, "un Mente OS ramificado por agente/persona" NO es nuevo; ya está el molde. El Maestro lo
   ESCALA, no lo inventa.
3. **`memory/RETOMAR.md` ya es un embrión del Maestro:** un índice ligero que apunta a todo lo demás. El
   Maestro es "un RETOMAR de RETOMARs" — un índice de índices que sabe de todas las ramas.
4. **El grafo de memoria (AGE) ya conecta conceptos** dentro de una instancia (814 conceptos, 18K
   relaciones en brian). El Maestro es el mismo principio UN NIVEL ARRIBA: conectar Mente OS, no solo
   conceptos.

## 3 · La arquitectura propuesta (a debatir)

**Principio rector: el Maestro es un ÍNDICE + GRAFO de Mente OS, NO una copia gigante de todo.**
No mueve ni duplica los 169 docs de cada rama; los **apunta, indexa y sabe qué tiene cada uno**.
Así se conecta sin volverse un monstruo de mantenimiento (y sin el consumo de tokens que Brian
teme). Tres piezas:

1. **EL REGISTRO (el corazón).** Un manifiesto central (`Maestro/registro.md` o una tabla) que lista
   cada Mente OS rama: nombre · ruta/ubicación · dueño · carril (diseño/código/negocio) · permisos ·
   un resumen de qué contiene (auto-generado leyendo su RETOMAR). El Maestro "sabe todo" = conoce
   este registro, no memoriza cada doc.
2. **EL PUENTE (cómo se conectan).** Opciones en §4.2 — la recomendada: **git submodules o un repo
   contenedor** (cada rama es un repo; el Maestro los referencia y puede leer/pull). Reusa lo que ya
   sabemos (git, la tríada). Alternativa: el canal API de For3s como puente vivo entre instancias.
3. **LA PUERTA DE PERMISOS.** Reusa el modelo de roles/puerta de For3s (H8: dueño/miembro + gate).
   Cada rama declara quién puede leer/escribir. Jazz ve y toca SOLO su rama de Diseño; el Maestro ve
   todo pero un colaborador ve su carril. Fail-closed (sin permiso, no ve).

**Cómo se "genera" una rama nueva (el caso Jazz):** un comando/plantilla `mente-os nueva <nombre>
--carril diseño --dueño jazz` → crea la estructura `{Alma,Cerebro,Cuerpo,Doc}` desde una plantilla
+ la registra en el Maestro + fija permisos. Jazz arranca con un Mente OS que "ya sabe qué show"
(la plantilla la orienta), en su carril, sin miedo a romper el de Brian (aislada + permisos).

## 4 · DECISIONES ABIERTAS (Brian decide — esto define el diseño)

### 4.1 · ¿El Maestro es NUEVO o se promueve `~/for3s/Mente`?
- **(a) Promover `~/for3s/Mente` a Maestro** (recomendado): ya es el más rico; se le añade la capa
  "Maestro/" (registro + puente + permisos) encima. Menos trabajo, cero migración.
- **(b) Maestro NUEVO por encima:** un `~/mente-maestro/` limpio que indexa a `~/for3s/Mente` como
  una rama más. Más limpio conceptualmente (el Maestro no es "un proyecto"), más trabajo inicial.

### 4.2 · ¿CÓMO se conectan técnicamente las ramas?
- **(a) Git (submodules / repo contenedor)** (recomendado): cada Mente OS = un repo; el Maestro los
  referencia, puede `pull` para leer. Versionado + colaboración + la tríada que ya dominamos. Jazz
  clona SU rama, no todo.
- **(b) Índice + rutas (sin git):** el registro apunta a rutas locales/remotas; el Maestro lee por
  filesystem/rsync. Más simple, sin versionado ni colaboración remota real.
- **(c) El canal API de For3s como puente vivo:** los Mente OS "hablan" por HTTP (reusa el canal
  API). Potente para memoria VIVA (episodios), pero más complejo; quizá fase 2.

### 4.3 · ¿"Leer" es unidireccional o bidireccional?
- **(a) Maestro lee las ramas** (unidireccional, recomendado para empezar): el Maestro sabe qué hay
  en cada una; las ramas no escriben al Maestro. Seguro y simple.
- **(b) Bidireccional:** las ramas también aportan al Maestro (ej. una decisión de Jazz sube al
  registro). Más potente, más riesgo de conflictos. Fase 2.

### 4.4 · Permisos: ¿por carril, por persona, o reusar la puerta de For3s (H8)?
Recomendado: **por persona + carril**, reusando el modelo de roles de For3s (ya probado). Cada rama
declara dueño + colaboradores + qué carril.

### 4.5 · ¿Relación con Foresito (Pendiente A)?
El Maestro sería **la fuente que Foresito (y los agentes) leen** para "saberlo todo". O sea:
Pendiente A (entrenar Foresito) se ALIMENTA del Maestro. ¿Se diseñan juntos o A espera a B?

## 5 · FASES propuestas (cuando Brian apruebe la arquitectura)

- **F1 · El REGISTRO** — crear la capa `Maestro/` (registro de ramas + esquema: nombre/ruta/dueño/
  carril/permisos/resumen). Registrar los Mente OS que YA existen (For3s, marca-personal, instancias).
  Verifica: el registro lista todas las ramas reales con su resumen auto-leído del RETOMAR.
- **F2 · EL PUENTE** — implementar la conexión elegida (§4.2). Que el Maestro pueda LEER una rama
  (ej. abrir el RETOMAR de marca-personal desde el Maestro). Verifica: el Maestro lee una rama real.
- **F3 · GENERAR RAMA NUEVA** — el comando/plantilla `mente-os nueva` (el caso Jazz/Diseño). Crea la
  estructura + registra + permisos. Verifica: se crea una rama de prueba, el Maestro la detecta.
- **F4 · PERMISOS** — la puerta (§4.4). Un colaborador ve solo su carril. Verifica: un "usuario Jazz"
  ve la rama de Diseño y NO la de código.
- **F5 · PILOTO JAZZ** — crear la rama de Diseño REAL de Jazz, con su plantilla orientadora, y que
  ella la use. Verifica: Jazz arranca sin "no sé qué show" (depende de gente externa).
- **F6 · CIERRE** — doc + memoria + (si aplica) integrar con Foresito (Pendiente A).

⚠️ **Alcance/riesgos:** NO leer `~/5M-incubathon/` (NavigoX, otro Mente OS con gate) sin permiso ·
`marca-personal` es OTRO proyecto (rama separada, confirmar antes de tocar) · cuidar el consumo de
tokens (por eso el Maestro INDEXA, no copia) · server-primero para lo que toque instancias.

## 6 · Lo que necesito de Brian para arrancar F1

1. **§4.1** ¿Promover `~/for3s/Mente` a Maestro (a), o Maestro nuevo (b)?
2. **§4.2** ¿Puente por git (a), índice+rutas (b), o canal API (c)?
3. **§4.3/4.4** ¿Empezamos unidireccional + permisos por persona/carril? (recomendado)
4. **§4.5** ¿Mente OS Maestro (B) primero y Foresito (A) después, o al revés?
5. ¿Apruebas las fases F1→F6 y que F1 (el registro) sea el primer paso concreto?

---

Relacionado: `vision/Vision_Mente_OS_Maestro_Y_Foresito_Entrenado.md` (visión) · `project_super_cerebro_conectado`
(memoria) · `Cerebro/For3s_OS_Grafo_Maestro.md` (arquitectura actual) · `project_hito_identidad_viva`
(el patrón mente-os/ por instancia) · `project_hito_entrenamiento` (para Pendiente A) ·
[[feedback_for3s_inter_scope]] · [[feedback_puente_mentes_os_gate]] (⛔ gate a otros Mente OS).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde v1, ADR-029).
