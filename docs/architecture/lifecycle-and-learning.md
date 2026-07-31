# ARCHITECTURE · lifecycle and learning

**Status:** current · **Type:** architecture · **Updated:** 2026-07-30 · **Owner:** brian
**Part of:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` (§6, §7, §10) ·
**Block:** `blk-split-architecture-2026-07`

## Purpose

How a block LIVES — open, work, close — and how an error becomes a form instead of staying an
anecdote. Grouped because they are the same thing seen twice: §6-§7 are the lifecycle of the work,
§10 is the lifecycle of what the work taught.

Extracted verbatim on 2026-07-30 (415 lines). ⚠️ **Moved, not rewritten.**

---

## 6 · CICLO DE VIDA DE UN BLOQUE

### 6.1 · EL PROCESO COMPLETO — de "hola" a bloque cerrado

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  A · ARRANQUE (cualquier IA · ~38-40K tokens)                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
   ┌───────────────────────┐
   │ 1 REGLAS BASE         │  automático · lo mínimo indispensable
   ├───────────────────────┤
   │ 2 CONTEXTO            │  qué se estaba haciendo
   ├───────────────────────┤
   │ 3 RETOMAR.md          │  lo último realizado
   ├───────────────────────┤
   │ 4 ¿QUÉ ARQUITECTO?    │  ¿qué perfil pide esta tarea?
   ├───────────────────────┤
   │ 5 HERRAMIENTAS        │
   └──────────┬────────────┘
              ▼
       ┌─────────────────────────────┐
       │ ¿Hay BLOQUE ACTIVO?         │
       └──────┬───────────────┬──────┘
         SÍ   │               │   NO
              ▼               ▼
     ┌─────────────────┐  ┌──────────────────┐
     │ CARGAR bloque   │  │ CREAR bloque     │
     │ ⚠ si falta algo │  │ · intención      │
     │   DECIRLO en    │  │ · límites SÍ/NO  │
     │   voz alta      │  │ · conexiones     │
     │   (no inferir)  │  │ · sub-bloques    │
     └────────┬────────┘  └────────┬─────────┘
              └────────┬───────────┘
                       ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  B · ELECCIÓN DE CARRIL — la decide la PROPAGACIÓN, no la IA                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
              ┌──────────────────────────────────────┐
              │ ¿Lo que se toca tiene DEPENDIENTES   │
              │  declarados en el grafo?             │
              └───────┬──────────────────────┬───────┘
                  SÍ  │                      │  NO
                      ▼                      ▼
            ┌──────────────────┐   ┌──────────────────────┐
            │ BLOQUE COMPLETO  │   │ ¿diseño nuevo?       │
            │ (los 3 encargados)│   └───┬──────────────┬───┘
            └────────┬─────────┘    NO  │              │ SÍ
                     │                  ▼              ▼
                     │           ┌────────────┐  ┌──────────────┐
                     │           │  DIRECTO   │  │    TAREA     │
                     │           │ solo valida│  │ Des.→Valida  │
                     │           └──────┬─────┘  └──────┬───────┘
                     ▼                  │               │
╔═══════════════════════════════════════════════════════════════════════════════╗
║  C · EL CICLO DE LOS 3 ENCARGADOS (mismo nivel · aplican a la vez)             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                     │
        ┌────────────▼─────────────┐
        │  ¿QUÉ SE QUIERE HACER?   │
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐
        │  SE ANALIZA              │
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐      ¿existe conexión con otro bloque?
        │  SE COMPARA con bloques  │◄──── evita duplicar
        └────────────┬─────────────┘      detecta propagación
                     ▼
   ╭─────────────────────────────────────╮
   │ ① PLAN DE IMPLEMENTACIÓN            │  ENCARGADO 1 · documentación
   │    apartados base por defecto       │  (al final puede añadir más
   │                                     │   si el panorama cambió)
   ╰──────────────────┬──────────────────╯
                      ▼
   ╭─────────────────────────────────────╮
   │ ② ANÁLISIS DEL PLAN                 │  ENCARGADO 2 · desarrollo
   │    ¿cumple mis criterios?           │
   ╰──────┬───────────────────────┬──────╯
     cumple│                      │NO cumple
          │                       │
          │        ⟲ RETROCESO ───┘
          │        regresa a ① a mejorarse
          ▼
   ╭─────────────────────────────────────╮
   │ ③ DESARROLLO EJECUTA                │  backend O frontend
   │    uno primero, luego el otro       │  ← estándares por disciplina
   │    ▸ cada iteración = PUNTO DE      │    (sistema de expertise)
   │      GUARDADO del bloque            │
   ╰──────────────────┬──────────────────╯
                      ▼
   ╭─────────────────────────────────────╮
   │ ④ VALIDACIÓN DEL FLUJO              │  ENCARGADO 3
   │    que NADA quede suelto            │
   │    que lo que existe funcione       │
   │    y esté CONECTADO                 │
   ╰──────┬───────────────────────┬──────╯
     pasa │                       │ no pasa
          │                       └──⟲ vuelve a ③
          ▼
        ┌──────────────────────────────┐
        │ ¿QUEDAN SUB-BLOQUES ABIERTOS?│
        └────┬────────────────────┬────┘
         SÍ  │                    │ NO
             │                    ▼
             │       ╔═══════════════════════════════════════════════════════════╗
             │       ║  D · CIERRE                                               ║
             │       ╚═══════════════════════════════════════════════════════════╝
             │         ┌────────────────────────────────┐
             │         │ BLOQUE CERRADO → ARCHIVADO     │
             │         │  · resumen detallado           │
             │         │  · conexiones con otros bloques│
             │         │  · experiencia de memoria      │
             │         │  · roces → propuestas a Brian  │
             │         └───────────────┬────────────────┘
             │                         ▼
             │              ┌─────────────────────┐
             │              │ CONSULTABLE por los │
             │              │ próximos bloques    │
             │              └─────────────────────┘
             │
             └──⟲ el bloque grande NO AVANZA
                  hasta cerrar los pequeños
```

### 6.1-bis · ⭐ EL CIERRE ES UN PROCEDIMIENTO, no una intención

**El fallo que corrige, medido:** 5 de 11 sesiones **nunca se registraron** · 8 auto-compactaciones
sin revisar. La regla *"sin registro no hay /clear"* existe desde el 14-jul y **se incumplió el 45%
de las veces** — porque dependía de acordarse.

```
   CERRAR UN BLOQUE — pasos fijos, en orden
   ═══════════════════════════════════════════════════════════
   1. CONSOLIDAR contexto.md      → curado a ≤80 líneas
                                    (el detalle largo se muda a docs/)
   2. CURAR decisiones            → cada una con su rationale
   3. RESOLVER roces              → suben a Brian como propuestas
   4. VERIFICAR SUFICIENCIA       → ⭐ ¿el Tier 1 basta para reiniciar?
                                       NO ─▶ el bloque NO se cierra
   5. ESCRIBIR RESUMEN            → qué se hizo · qué se aprendió
   6. DECLARAR CONEXIONES         → qué bloques quedan afectados
   7. ARCHIVAR                    → _archivados/<BLOQUE>_<fecha>/
   8. REGENERAR índice y estados  → 🤖 automático, nunca a mano
```

> **Regla dura:** *consolidar ANTES del cierre, no después.* Un cierre que depende de que alguien
> se acuerde al final es el cierre que ya falló 5 de 11 veces.

### 6.2 · DÓNDE VIVE EL CONTEXTO (y por qué `/clear` deja de doler)

```
        HOY                                    v2
   ────────────────                    ────────────────────

   ┌──────────────┐                    ┌──────────────┐
   │ CONVERSACIÓN │ ← fuente           │ CONVERSACIÓN │ ← caché
   │              │   de verdad        │              │   desechable
   │ · alcance    │                    └──────┬───────┘
   │ · criterio   │                           │ lee/escribe
   │ · grafo      │                           ▼
   └──────┬───────┘                    ┌──────────────────┐
          │                            │  BLOQUE (disco)  │ ← fuente
        /clear                         │  · límites SÍ/NO │   de verdad
          │                            │  · decisiones    │
          ▼                            │  · conexiones    │
      ✗ TODO MUERE                     │  · guardados     │
                                       └────────┬─────────┘
   RETOMAR sobrevive pero                       │
   solo dice "dónde                           /clear
   quedamos", no "qué                           │
   estábamos construyendo"                      ▼
                                          ✓ NADA SE PIERDE
   → la IA RECONSTRUYE                      se recarga del bloque
     por inferencia
     y suena segura                       ⚠ si el bloque está
   → "no, así no iba"                       incompleto: SE DICE,
                                             no se infiere
```

---

## 7 · BLOQUE MEJORADO — la regla anti fix-sobre-fix

> *"¿Qué pasa si a un bloque se le implementa un fix o mejora? **No se crea un código o solución
> arriba solo para tapar el problema.** Se evalúa la construcción; a partir de saber todo el
> contexto del código se establece cómo solucionar el error. Si se tiene que pensar o hacerlo por
> otro medio, está bien. **Lo que no está bien es tener decenas de código sin orden**, porque
> tendremos problemas de redundancia."*

### Procedimiento obligatorio ante un fix

1. **NO** escribir la solución encima.
2. **Evaluar la construcción** existente.
3. **Conocer TODO el contexto del código** antes de decidir.
4. **Elegir la solución real** — aunque implique otro camino.
5. El bloque debe contener **la información necesaria para conectarse con otros bloques**.
6. Esa es **la secuencia a repetir e iterar con el humano**.

### Justificación medida (la demo)

| Evidencia | Dato |
|---|---|
| Commits que son fixes | **25 de 60 (42%)** |
| `userStore.ts` tocado | **21 veces** |
| `for3sChat.ts` tocado | 14 veces |
| Prueba textual | *"barrido completo del patrón cookie kind ≠ instancia real"* llegó **4 commits después** de *"guardar la API key en la instancia REAL"* → se arregló el síntoma, no la causa, y hubo que volver |

### 7.1 · EJEMPLO — el mismo bug, mal y bien resuelto

**Caso real: "la API key se guarda en el sitio equivocado".**

```
❌ COMO SE HIZO (fix-sobre-fix)
   1. Bug reportado: la key del dueño se guarda mal
   2. Se busca DÓNDE falla → un archivo
   3. Se corrige AHÍ                          → commit d5dc778
   4. Aparece otro síntoma parecido           → commit 6310bcf
   5. Aparece otro más                        → commit 5326bb6
   6. Se descubre que el patrón estaba en TODOS lados
   7. "barrido completo del patrón"           → commit b61e3d0
   ⤷ 4 commits para un solo problema · userStore.ts terminó con 21 toques
```

```
✅ COMO LO HARÍA EL BLOQUE MEJORADO
   1. Bug reportado: la key del dueño se guarda mal
   2. NO tocar nada todavía
   3. EVALUAR LA CONSTRUCCIÓN:
      ¿de dónde sale "kind"? ¿quién más lo usa para identificar la instancia?
      → grep: aparece en 6 archivos
   4. ENTENDER EL CONTEXTO COMPLETO:
      la causa NO es "este archivo guarda mal"
      la causa es "kind (cookie) se usa como si fuera la instancia real"
   5. DECIDIR LA SOLUCIÓN REAL:
      un punto único que resuelva la instancia real → los 6 sitios lo usan
   6. UN cambio, 6 sitios corregidos, causa eliminada
   ⤷ 1 commit · el patrón no puede reaparecer
```

**La diferencia no es esfuerzo: es el paso 3.** El fix-sobre-fix pregunta *"¿dónde falla?"*.
El bloque mejorado pregunta *"¿por qué existe este fallo y dónde más vive?"*.

> Este mismo criterio ya está probado en Mente OS: `memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` §2
> — *"el código suele decir de dónde viene. Antes de teorizar: grep + leer el comentario +
> contrastar con Mente OS. En 3 comandos se supo el origen exacto."*

---

## 10 · EL SISTEMA DE APRENDIZAJE DE ERRORES

> **Brian, 2026-07-27:** *"Tenemos que evaluar cómo hacer que esos errores no solo sean errores,
> sean forma que ya aprendió, o ver la forma de mejorar este apartado."*

### 10.1 · El precedente que ya funcionó

`memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` convirtió un error real en **método reutilizable con
checklist**: síntoma → origen → el error que casi se comete → la lección como regla → checklist
para la próxima vez.

**Salió bien, pero fue un accidente feliz.** Lo que falta es que sea **sistemático**.

### 10.2 · Las tres fuentes de aprendizaje

| Fuente | Qué produce |
|---|---|
| **Errores cazados** | un caso reutilizable con checklist |
| **Roces con reglas** (§8) | propuesta de mejora de la regla |
| **Bloques archivados** | experiencia consultable (*"detallado todo como experiencia de memoria"*) |

### 10.3 · EJEMPLO — de error suelto a forma aprendida

**El recorrido completo con un caso real (el default `hoteles`):**

```
① ERROR DETECTADO
   Brian: "no sé de dónde viene este hoteleria, no entiendo"

② SE RASTREA (no se teoriza)
   grep → api_channel.py: TEMA_DEFAULT = "hoteles"  # fase Incubathon
   El comentario dice el origen. 3 comandos, causa exacta.

③ SE INTENTA UN FIX... Y BRIAN LO CAZA
   Propuesta: cambiar default a "general" (parecía neutro)
   Brian: "general únicamente es para los dueños... eso está mal"
   → habría mandado invitados al hilo PRIVADO del dueño

④ SE EXTRAE LA REGLA (aquí nace el aprendizaje)
   ⭐ "Un default NUNCA debe apuntar a algo que tenga dueño o
      significado reservado. El default es un cajón neutro."

⑤ SE VUELVE CONSULTABLE
   → memory/archive/CASO_Default_Peligroso_Tema_Hilo.md + checklist de 7 pasos
   → memoria feedback_default_nunca_apunta_a_algo_con_dueno

⑥ SE APLICA LA PRÓXIMA VEZ
   Antes de elegir CUALQUIER default: "¿este nombre significa algo
   para alguien?" Si sí → otro.
```

**Lo que hoy falla es el paso ⑥.** Los pasos ① a ⑤ ya ocurrieron y quedaron bien escritos.
Pero **nada garantiza que se consulte** antes del próximo default. Un aprendizaje que no se
consulta **no es aprendizaje: es un archivo**.

> **Por eso el sistema de aprendizaje no es "escribir más casos" — es asegurar que el caso
> LLEGUE al bloque que lo necesita.** El Encargado 2 debería recibir los casos aplicables a su
> disciplina antes de empezar, no después de romper algo.

### 10.4 · ✅ CÓMO SE CONSULTA EL APRENDIZAJE *(decidido 2026-07-27)*

> **El problema (§10.3):** los pasos ① a ⑤ ya funcionan — el caso se escribe bien. **Falla el ⑥:
> que se consulte la próxima vez.** Un aprendizaje que no se consulta no es aprendizaje: es un archivo.

**Decisión: EL MISMO MECANISMO QUE LOS ESTÁNDARES.** No se inventa uno nuevo.

```
   1 · EL BLOQUE LOS DECLARA        sección §D de BLOQUE.md
       ## Estándares obligatorios
       - Alma/expertise/base_datos.md          ← estándar
       - rules/case-dangerous-default.md  ← ⭐ CASO
                    ↓
   2 · EL HOOK LOS INYECTA          antes de editar (capa D, §12-QUATER)
       "vas a elegir un default → aquí está el caso que ya te mordió"
                    ↓
   3 · EL VALIDADOR LO COMPRUEBA    al cerrar
       ¿se aplicó lo declarado?
```

**Por qué reusar el mecanismo y no crear otro:**
- Los casos **son estándares**, solo que nacidos de un error propio en vez de del criterio previo.
- Un segundo mecanismo sería **otro sitio donde algo se puede omitir** — justo lo que hay que evitar.
- Reusa las 4 capas ya decididas: **el caso viaja CON el trabajo**, no vive en un índice general.

**Sigue pendiente de definir en la Ronda F0:**
- ¿Cuándo un error **merece** convertirse en caso? (no todos lo merecen)
- ¿Cómo se detecta que una regla estorbó **3 veces** y debe revisarse? (§8.1)

---

### 10.5 · ✅ CUÁNDO UN ERROR MERECE SER CASO — *F0-1, decidido 2026-07-27*

**El problema que resuelve:** si todo error se vuelve caso, en tres meses hay 80 y **ninguno se
consulta** — sería el nuevo `memory/PENDIENTES.md`. Si ninguno lo hace, los errores se repiten.

#### La prueba de las 3 preguntas — debe cumplir LAS TRES

| # | Pregunta | Qué filtra |
|---|---|---|
| 1 | **¿Volvería a pasar en otro sitio?** | si es único de ese archivo es un **fix**; si es patrón, es **caso** |
| 2 | **¿La causa fue un CRITERIO equivocado**, no un descuido? | un typo no enseña nada; *"el default apuntaba a algo con dueño"* sí |
| 3 | **¿Se puede escribir como regla accionable** que evite el error **antes** de cometerlo? | si no se puede, es una **anécdota** |

#### Calibración con errores reales — para que el criterio no sea abstracto

| Error real | ¿Caso? | Por qué |
|---|---|---|
| Default `general` rompía el aislamiento | ✅ **sí** | patrón + criterio equivocado + regla clara |
| "Reenviar código" burlaba el anti-fuerza-bruta | ✅ **sí** | *"resetear un contador es resetear la defensa"* |
| `tailscale serve` apagó el Funnel | ✅ **sí** | *"probar desde local ≠ probar producción"* |
| `chown -R` en bind mount rompió el HOST | ✅ **sí** | regla ya escrita y LOCKED |
| Heredoc que se comió las variables | ❌ **no** | fix técnico; ya vive en el Método F |
| `DEMO_ENC_KEY` divergente | 🟡 **el patrón sí** | *"un fallback que tapa una divergencia"*; el incidente no |

#### Dos reglas duras que acompañan

**① Umbral automático por repetición.** Si el mismo **tipo** de error aparece **2 veces**, se vuelve
caso **aunque no pase las 3 preguntas**. *La repetición es evidencia por sí sola.*

**② Límite de 12 casos activos.** Al llegar a 13 → **fusionar o archivar**.
> Sin límite, la carpeta de casos se convierte en el archivo de 240 KB que nadie lee.
> **Misma lección: el único archivo con límite es el único que no se desbordó.**

---

### 10.6 · ✅ CÓMO SE DETECTA UNA REGLA QUE ESTORBA — *F0-2, decidido 2026-07-27*

**Principio: que sea ARITMÉTICA, no interpretación.** Un mecanismo que exige juicio para dispararse,
no se dispara.

#### El registro del roce — línea estructurada de 4 campos

```
2026-07-27 · regla: server-primero · bloque: blq-demo · motivo: fix urgente ya verificado
```

**fecha · regla · bloque · motivo.** `revisar-bloques` los cuenta (§12-TER).

#### El disparo

```
regla "server-primero": 3 roces · blq-demo · blq-panel · blq-trace
🔔 REVISIÓN DE REGLA — 3 bloques distintos
```

#### Los dos detalles que hacen que funcione

**① BLOQUES DISTINTOS, no repeticiones.**
3 roces en el **mismo** bloque = fricción puntual de esa tarea.
3 roces en **bloques distintos** = **la regla está mal**.
> Sin esta distinción, cualquier tarea larga dispararía falsas alarmas y el mecanismo se ignoraría.

**② NO CADUCA.**
Si los 3 roces se acumulan en seis meses, sigue siendo señal.
> **El problema no es la velocidad de la fricción: es su recurrencia.**

#### Qué pasa al dispararse

⛔ **La regla NO se cambia automáticamente.** Se **eleva a Brian** con los 3 roces y sus motivos.
Él decide: **ajustar** · **mantener con excepción documentada** · **eliminar**.

> Coherente con el principio madre — *"no existen reglas inmutables, existen apuntadores a reglas:
> estándares mejorando con criterios del usuario"*. **El sistema detecta; Brian decide.**

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (entry point) ·
`rules/block-lifecycle.md` (the executable rule) · `rules/contract-archive.md` ·
`rules/rule-fix-not-patch.md` · `rules/case-dangerous-default.md`.
