# 🏗️ ESTÁNDAR — El Método de Fases "F" (cómo construimos hitos en For3s OS)

**Status:** current · **Type:** rule · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/ESTANDAR_Metodo_Fases_F.md → rules/ESTANDAR_Metodo_Fases_F.md (2026-07-30, ADR-029)

## Purpose

🏗️ ESTÁNDAR — El Método de Fases "F" (cómo construimos hitos en For3s OS)


> **Origen (Brian, 2026-07-04):** "me gustó MUCHO cómo tomaste cada F, lo necesito como un
> estándar en Mente OS que puedas ocupar siempre que lo necesites." Este documento destila la
> forma de trabajo que usamos en el Hito Reconstrucción FOR3S_ROLE (F1-F7, v0.15.0) para que sea
> **el método por defecto de todo hito grande.** Léelo al arrancar cualquier construcción mayor.

---

## 0. LA REGLA MADRE
**Explicar → aprobar → construir.** Nunca se codea un hito/fase sin explicarlo antes y esperar
el OK de Brian. Cada fase se anuncia, se construye, se verifica y se documenta antes de la siguiente.

---

## 1. ANTES DE CODEAR: diseñar la Ronda (F0)
Todo hito grande empieza con una **Ronda de diseño a profundidad** en `Cuerpo/Ronda_*.md`
ANTES de tocar código:
- Captura la **visión en palabras del propio Brian** (citas literales — son el contrato).
- Investiga **referencias reales** (repos, material de entrenamiento) — notación interna; el código
  que salga NO cita fuentes externas (regla LOCKED).
- **Reusa lo que ya existe** (mapéalo en una tabla: "¿For3s ya lo tiene? ¿dónde?"). No reinventar.
- Define las **fases F1..Fn**, cada una con: qué construye + cómo se verifica.
- Si hay decisiones de arquitectura → preguntar con `AskUserQuestion` (opciones concretas +
  recomendación), NO asumir.
- Cierra pidiendo aprobación. Solo entonces arranca F1.

---

## 2. EL RITMO DE CADA FASE (F1, F2, …)
Cada fase sigue SIEMPRE este ciclo. Es lo que a Brian le gustó — replicarlo tal cual:

### 2.1 · INVESTIGAR EL TERRENO (primero, siempre)
Antes de escribir una línea: **leer el código real** que se va a tocar y sus alrededores.
- ¿Quién USA lo que voy a cambiar? (grep de consumidores → no romperlos).
- ¿Qué patrón ya existe para esto? (reusarlo, no inventar uno nuevo).
- Ver las firmas/estructuras REALES (no asumir de memoria).

### 2.2 · CURIOSIDAD EXTREMA — "ver lo que nadie ve"
Esta es la parte clave del estándar (Brian: "sé curioso a extremos, busca lo que los demás no").
- No dar nada por bueno sin probarlo, ni por malo sin investigarlo. Ej. real: un `/salud` decía
  "MCP 401" → al probar el handshake real dio 21 tools = era falso negativo, no un fallo.
- Al construir, **buscar activamente el bug** que introduje o que ya estaba latente.
- Cuando algo "más o menos funciona" → PARAR e investigar. El "más o menos conectado" es el
  enemigo (lección cache→127.0.0.1: pensábamos que todo bien y era lentitud por hardcodeo).

### 2.3 · CONSTRUIR con las reglas de calidad
- **Cero hardcodeo**: hosts/puertos/credenciales SIEMPRE de ENV (y testear que se leen de ENV).
- **Defensivo total**: cada función nueva nunca rompe el turno/arranque (try/except con fallback).
- **Red de seguridad primero**: si se refactoriza algo vivo, el resultado debe ser demostrablemente
  equivalente (ej. F1: el prompt salió **byte-idéntico** al original, verificado programáticamente).
- **Un punto único** para cosas que antes estaban dispersas (patrón `memoria.recordar()` /
  `identidad.ensamblar()`): que sea imposible dejar un silo suelto.
- **Editar con precisión**: para cambios grandes o con caracteres delicados, escribir un script
  Python que haga el reemplazo exacto y **verifique** el resultado (no editar 200 líneas a ojo).
  ⚠️ NUNCA escribir shell scripts vía heredoc de Python (interpola `$variables` → las vacía;
  mordió 2 veces). Subir el fragmento como archivo con `scp` y leerlo, o `cat >>`.

### 2.4 · LA BATERÍA §5-BIS — "cada modificación pasa por TODO el sistema"
Regla DURA de Brian: **no basta probar el carril; hay que verificar que TODO sigue conectado.**
Ninguna fase se cierra sin pasar TODA la batería (verificación AFIRMATIVA con dato real, no "parece"):
- **A · Suite base**: `pytest -q` + `ruff check` + `ruff format --check` + `ty` (gate) + Hypothesis.
- **B · Arranque real**: rebuild + `docker compose up` + leer logs ("cerebro conectado", "MCP
  conectado", "Application started", guardián OK). No basta el import — el arranque real.
- **C · /salud completo**: los subsistemas E2E → **0 FAIL** o la fase no se cierra.
- **D · Memoria a fondo**: escribir→embeber→recuperar por significado→grafo→cascada + **prueba de
  RECONEXIÓN** (reiniciar/caída de un hermano → correr el flujo de nuevo, confirmar que reconecta
  de env, no de un host hardcodeado).
- **E · Cada H**: recorrer los hitos (H4-H12 + AC + execute_code + P1) con acción/dato REAL, no solo
  el subsistema tocado. Un cambio en el centro puede desconectar cualquiera.
- **F · Tools**: cada tool se invoca con prueba real (MCP con handshake real, no GET pelón).
- **G · Lo propio de la fase**: verificar la funcionalidad nueva end-to-end + con LLM real cuando
  aplique (los tests unitarios no ejercen el prompt/comportamiento real).
- **Verificación afirmativa**: cada check confirma con un dato ("recuperó X", "vector=1024 dims",
  "cron_corridas con timestamp de hoy", "21 tools"), nunca "parece que sí".

### 2.5 · CERRAR LA FASE
- Si algún check da 🔴 o un H quedó desconectado → **la fase NO se cierra.** Arreglar primero.
- **Commit firmado GPG** (key B1B99321918F3C29) con mensaje que cuente: qué se construyó, cómo se
  verificó (con los números reales), y los BUGS/HALLAZGOS cazados (honestidad total, incl. bugs propios).
- Actualizar la Ronda marcando la fase ✅ con evidencia.
- **Server-primero**: todo queda en el server; push a GitHub SOLO con orden explícita de Brian.

---

## 3. AL CERRAR EL HITO (última F)
- Version bump (`version.py` VERSION + HITO + changelog vivo) + `CHANGELOG.md` público (inglés).
- Documentar en Mente OS: Ronda ✅ + banner de hito completo + **memoria** del proyecto + RETOMAR +
  Bitácora. Registrar los hallazgos no-urgentes en PENDIENTES.
- Rebuild final para hornear la versión + verificar que corre en el contenedor.
- Un diagrama/artifact si ayuda a comunicar (CodeViz para arquitectura, Artifact para comparativas).

---

## 4. LOS 4 PRINCIPIOS QUE HICIERON QUE FUNCIONARA (el corazón del estándar)
1. **Curiosidad que caza bugs.** Cada fase del hito FOR3S_ROLE cazó un bug real (heredoc que comió
   variables ×2, detector incompleto, init_persona sin recursión) — porque se buscó activamente, no
   se asumió. "Ver lo que nadie ve."
2. **Verificación afirmativa de TODO el sistema.** No el carril: memoria + reconexión + cada H +
   todas las tools + arranque real. Con dato real, cero "más o menos".
3. **Red de seguridad demostrable.** Refactorizar algo vivo = probar que el resultado es equivalente
   (byte-idéntico, mismo comportamiento) antes de avanzar.
4. **Reusar lo probado, no reinventar.** Cada hito se apoya en motores que ya funcionan (automod,
   perfil_infer, DMN, memoria.recordar) y los apunta a lo nuevo.

---

## 5. CHECKLIST RÁPIDO (para pegar mentalmente en cada fase)
```
[ ] investigué el código real + quién lo usa (no romper consumidores)
[ ] reuso un patrón existente (no reinvento)
[ ] cero hardcodeo (todo de ENV)
[ ] construí defensivo (nunca rompe el arranque/turno)
[ ] si refactoricé algo vivo → verifiqué equivalencia (byte-idéntico / mismo comportamiento)
[ ] BATERÍA §5-BIS completa: A tests · B arranque real · C /salud 0 FAIL · D memoria+reconexión
    · E cada H · F tools · G lo nuevo E2E — TODO afirmativo, cero "parece"
[ ] cacé y reporté los bugs (incl. los míos) con honestidad
[ ] commit firmado GPG con evidencia real en el mensaje
[ ] Ronda actualizada ✅ + (al cerrar hito) version/CHANGELOG/memoria/RETOMAR
[ ] server-primero: push a GitHub SOLO si Brian lo pide
```

---

Relacionado: [[project_hito_identidad_viva]] (el hito que originó este estándar) ·
`work/Ronda_Reconstruccion_FOR3S_ROLE.md` (§5-BIS batería detallada) ·
[[feedback_flujo_server_primero]] · [[feedback_no_loops_espera_servidor]] ·
[[feedback_explicar_antes_de_implementar]] (la regla madre).

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `rules/ESTANDAR_Metodo_Fases_F.md`).
