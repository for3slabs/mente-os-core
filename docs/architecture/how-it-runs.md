# 🚦 CÓMO FUNCIONA MENTE OS v2 — el flujo completo
**Status:** current · **Type:** architecture · **Updated:** 2026-07-31 · **Owner:** brian
**Purpose:** qué se dispara, cuándo, y qué pasa en cada rama. El mapa operativo.
**Medido en disco el 2026-07-31** — ninguna cifra de este documento viene de memoria.
---

> **La ley que decide qué va a script y qué queda escrito:**
> *una regla en código se cumple 100%; una regla que solo vive en un documento se cumple 40-60%.*
> Medida el 2026-07-27. Por eso **la doctrina es documento y la VERIFICACIÓN es script.**

Mente OS v2 no es una carpeta de documentos: son **4 hooks y 13 validadores** que corren en
momentos concretos.

---

## 1 · EL FLUJO COMPLETO DE UNA SESIÓN

```mermaid
flowchart TD
    START([Brian abre la sesión]) --> HEALTH[session-start.sh<br/>corre check-health]
    HEALTH --> HQ{¿algo en rojo?}
    HQ -->|no| SILENT[silencio total]
    HQ -->|sí| WARN[avisa: guardia desarmado ·<br/>sesión sin registrar · bloque a la deriva]
    SILENT --> WORK
    WARN --> WORK

    WORK{¿qué va a hacer?}
    WORK -->|editar un archivo| EDIT
    WORK -->|lanzar un especialista| AGENT
    WORK -->|commitear| COMMIT
    WORK -->|cerrar la sesión| CLOSE

    EDIT[momento 02 · §2] --> WORK
    AGENT[momento 03 · §3] --> WORK
    COMMIT[momento 04 · §4] --> WORK
    CLOSE[momento 05 · §5] --> END(["/clear seguro"])

    style START fill:#1f2937,stroke:#6b7280,color:#f9fafb
    style END fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style WARN fill:#7c2d12,stroke:#f97316,color:#fff7ed
    style WORK fill:#1e3a5f,stroke:#60a5fa,color:#eff6ff
```

**El hook de arranque está diseñado para callar.** Un guardia que avisa en cada sesión se ignora
en una semana, y un guardia ignorado no protege nada.

---

## 2 · MOMENTO 02 — vas a editar un archivo

**Disparo:** `PreToolUse(Write|Edit)` → dos hooks en cadena.

```mermaid
flowchart TD
    E(["Write / Edit sobre un archivo"]) --> H1[pre-edit-standards.py]
    H1 --> Q1{¿el archivo cae en<br/>el §B IN de un bloque?}
    Q1 -->|no| H2
    Q1 -->|sí| INJ[te nombra su §D:<br/>dev-database.md · rule-fix-not-patch.md …]
    INJ --> NOTE[⚠️ NUNCA bloquea]
    NOTE --> H2

    H2[gate-critical.py] --> Q2{¿SQL destructivo<br/>sin rollback?}
    Q2 -->|sí| B1[🔴 BLOQUEA]
    Q2 -->|no| Q3{¿SQL destructivo<br/>dentro de un .ts?}
    Q3 -->|sí| B2[🔴 BLOQUEA]
    Q3 -->|no| Q4{¿cierra un bloque<br/>sin suficiencia?}
    Q4 -->|sí| B3[🔴 BLOQUEA]
    Q4 -->|no| Q5{¿pieza con<br/>5+ dependientes?}
    Q5 -->|sí| W1[⚠️ avisa · el carril ya lo cubre]
    Q5 -->|no| OK([✅ la edición procede])
    W1 --> OK

    style E fill:#1f2937,stroke:#6b7280,color:#f9fafb
    style OK fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style B1 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style B2 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style B3 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style W1 fill:#7c2d12,stroke:#f97316,color:#fff7ed
    style NOTE fill:#7c2d12,stroke:#f97316,color:#fff7ed
```

**Por qué el primero nunca bloquea:** actúa por coincidencia de ruta. Bloquear con esa señal haría
insufrible editar, y una puerta insufrible se apaga.

**Por qué el último solo avisa:** se midió que son 5 archivos editados a diario y el carril de
propagación ya fuerza la evaluación. Una segunda parada no añade nada.

---

## 3 · MOMENTO 03 — vas a lanzar un especialista

**Disparo:** `PreToolUse(Agent|Task)` → `gate-handoff.py`

```mermaid
flowchart TD
    A(["Agent / Task"]) --> Q1{¿el especialista<br/>puede ESCRIBIR?}
    Q1 -->|no · Explore, Plan| W[⚠️ avisa · no necesita manifest]
    W --> PASS1([✅ pasa])

    Q1 -->|sí| Q2{¿MENTE_HANDOFF_BYPASS=1?}
    Q2 -->|sí| BYP[🟡 escape ruidoso:<br/>imprime qué deja sin registrar]
    BYP --> PASS2([✅ pasa])

    Q2 -->|no| Q3{¿hay un manifest<br/>en el bloque?}
    Q3 -->|no| BLK1[🔴 BLOQUEA]
    Q3 -->|sí| VER[corre bin/verify-handoff]

    VER --> Q4{exit code}
    Q4 -->|2 · malformado| BLK2[🔴 BLOQUEA<br/>arregla el manifest]
    Q4 -->|3 · binding falla| BLK3[🔴 BLOQUEA<br/>el bloque se movió o renombró]
    Q4 -->|0 · bounded| PASS3([✅ pasa · scope declarado])

    Q1 -->|tipo desconocido| BLK4[🔴 BLOQUEA · falla cerrado]

    style A fill:#1f2937,stroke:#6b7280,color:#f9fafb
    style PASS1 fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style PASS2 fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style PASS3 fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style BLK1 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style BLK2 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style BLK3 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style BLK4 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style W fill:#7c2d12,stroke:#f97316,color:#fff7ed
    style BYP fill:#78350f,stroke:#fbbf24,color:#fffbeb
```

**El nivel se midió, no se eligió.** Sobre todo el historial del proyecto:

| Herramienta | Llamadas |
|---|---|
| Bash | **9,786** |
| Edit | 3,289 |
| Read | 1,851 |
| **Agent** | **32** — 15 de ellas de solo lectura |

Esa medición **invirtió el diagnóstico**: el fallo del 20-jul no fue *delegar mal* — fue **no
delegar**, y meter 421 comandos en un solo contexto hasta llegar a 999K y provocar el incidente
del 21-jul. Bloquear también al lector barato empujaría de vuelta a ese comportamiento.

> ⭐ **Presencia no es cumplimiento.** Un manifest en disco no abre nada: la puerta corre
> `verify-handoff` y exige **exit 0**. Un manifest sin llenar deja la puerta cerrada.

---

## 4 · MOMENTO 04 — vas a commitear

**Disparo:** `.git/hooks/pre-commit` → `hooks/pre-commit.sh`

```mermaid
flowchart TD
    C([git commit]) --> FIND{¿hay un Mente<br/>alcanzable?}
    FIND -->|no| SKIP([✅ pasa · repo no gobernado])
    FIND -->|sí| RUN[corre bin/check-blocks]

    RUN --> Q{exit code}
    Q -->|0 · contrato cumplido| OK([✅ commit procede])
    Q -->|1 · lo viola| B1[🔴 BLOQUEA]
    Q -->|timeout 120s| B2[🔴 BLOQUEA]
    Q -->|otro · inesperado| B3[🔴 BLOQUEA · falla cerrado]

    style C fill:#1f2937,stroke:#6b7280,color:#f9fafb
    style OK fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style SKIP fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style B1 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style B2 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style B3 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
```

**La rama que importa es la última:** una salida inexplicada **no es un aprobado**. Si el validador
no puede correr, el commit no pasa.

---

## 5 · MOMENTO 05 — vas a cerrar la sesión

Dos mitades, y hacen falta las dos: `check-clear-ready` **se niega** (determinista), la skill
`session-wrap` **decide qué importó** (juicio, que ningún script puede).

```mermaid
flowchart TD
    S(["Brian: vamos a cerrar"]) --> WRAP[skill session-wrap]

    WRAP --> S1[① medir la sesión<br/>peso · turnos · contexto pico]
    S1 --> S2[② sintetizar qué importó<br/>decisiones · hallazgos · errores]
    S2 --> S3[③ 🔴 autopsia en<br/>Registro_Conversaciones.md]
    S3 --> S4[④ actualizar RETOMAR.md]
    S4 --> S5[⑤ memorias + PENDIENTES]
    S5 --> S6[⑥ bloque activo: §E · §G · §J]

    S6 --> CHK[bin/check-clear-ready]
    CHK --> Q1{¿la sesión<br/>tiene autopsia?}
    Q1 -->|no| B1[🔴 se niega]
    Q1 -->|sí| Q2{¿RETOMAR<br/>al día?}
    Q2 -->|no| W1[⚠️ avisa]
    Q2 -->|sí| GREEN
    W1 --> GREEN(["✅ safe to /clear"])

    style S fill:#1f2937,stroke:#6b7280,color:#f9fafb
    style S3 fill:#78350f,stroke:#fbbf24,color:#fffbeb
    style GREEN fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style B1 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style W1 fill:#7c2d12,stroke:#f97316,color:#fff7ed
```

**Por qué existe:** el peor fallo del proyecto. *"Todo está perfecto"* antes de un `/clear`,
*"sigue roto"* después. Mismo código, veredictos opuestos, minutos de diferencia.

Nada mintió: **`/clear` es un CORTE, no un guardado.** El primer veredicto vivía solo en la
conversación y murió con ella. El arreglo no es mejor memoria — es **negarse a cortar mientras el
veredicto viva solo en el contexto.**

---

## 6 · QUIÉN JUZGA QUÉ — el árbol de encargados

Tres encargados **en secuencia**. Cada uno tiene sus disciplinas (sus raíces), y **ninguno inventa
criterio**: lo carga.

```mermaid
flowchart LR
    subgraph O1 ["owner-1 · formato de documentación"]
        direction TB
        A1[planea<br/>rechaza lo que no se puede auditar]
        A1 --- D1[doc-planning]
        A1 --- D2[doc-structure]
    end

    subgraph O2 ["owner-2 · desarrollo"]
        direction TB
        A2[construye]
        A2 --- D3[dev-database]
        A2 --- D4[dev-backend]
        A2 --- D5[dev-frontend]
    end

    subgraph O3 ["owner-3 · validación de flujo"]
        direction TB
        A3[¿producto o MVP?]
        A3 --- D6[val-functional]
        A3 --- D7[val-integration]
    end

    O1 --> O2
    O2 -.->|⭐ VETO: devuelve el plan| O1
    O2 --> O3

    V[owner-0 · la voz<br/>fuera de la secuencia<br/>gobierna todo momento]

    style O1 fill:#1e293b,stroke:#64748b,color:#f1f5f9
    style O2 fill:#1e293b,stroke:#64748b,color:#f1f5f9
    style O3 fill:#1e293b,stroke:#64748b,color:#f1f5f9
    style V fill:#3b0764,stroke:#a855f7,color:#faf5ff
```

> **Brian, 2026-07-31, corrigiendo a la IA:** *"los expertise eran formato de documentación,
> desarrollador, validación de flujo funcional. Los 3 que pusiste van DENTRO de desarrollador —
> es una división como si fuera un árbol."*

**Por qué importa la distinción:** los encargados son la **secuencia** (quién actúa, en qué orden,
con qué veto). Las disciplinas son la **materia**. Al aplanarlos parecía que `dev-database` podía
devolverle un plan a owner-1 — no puede; ese veto es solo de owner-2.

---

## 7 · EL VEREDICTO DE CALIDAD — dos capas

```mermaid
flowchart TD
    CLOSE([se cierra un bloque]) --> C1{① funcional<br/>batería §5-BIS}
    C1 -->|falla| N1[🔴 NO cierra<br/>algo está roto]
    C1 -->|pasa| C2{② suficiencia<br/>¿§A-E bastan para reiniciar?}
    C2 -->|falla| N2[🔴 NO cierra<br/>aunque el código funcione]
    C2 -->|pasa| L1[capa 1 · bin/grade-block<br/>código muerto · duplicación · tests · grafo]

    L1 --> L2[capa 2 · qa-dimensions + expertise<br/>arquitectura · datos · abstracción<br/>nombres · contratos · necesidad]
    L2 --> V{veredicto}
    V -->|ambas verdes| P([🟢 PRODUCTO])
    V -->|alguna amarilla| M([🟡 CERCA])
    V -->|alguna roja| R([🔴 MVP · cierra con su deuda listada])

    style CLOSE fill:#1f2937,stroke:#6b7280,color:#f9fafb
    style P fill:#14532d,stroke:#22c55e,color:#f0fdf4
    style M fill:#78350f,stroke:#fbbf24,color:#fffbeb
    style R fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style N1 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style N2 fill:#7f1d1d,stroke:#ef4444,color:#fef2f2
    style L2 fill:#422006,stroke:#a16207,color:#fefce8
```

| Capa | Qué juzga | Quién la escribe | Estado |
|---|---|---|---|
| **1 · medible** | código muerto · duplicación · tests · grafo | ya es código (`bin/grade-block`) | ✅ **funciona hoy** |
| **2 · criterio** | las 6 dimensiones con evidencia exigida | **solo Brian** | ⬜ **66 huecos** |

> ⭐ Un 🔴 **no prohíbe cerrar el bloque.** Prohíbe cerrarlo **como producto**: cierra marcado MVP,
> con su deuda listada.

**Una dimensión no se contesta afirmándola** — se contesta mostrando la evidencia. Eso es lo que
impide que la IA se autoapruebe.

---

## 8 · QUÉ FUNCIONA Y QUÉ NO — medido 2026-07-31

### ✅ Funciona, verificado

- **`test-f0-f6` = 113/113**, cero fallas, en tres corridas seguidas.
- **Las 4 puertas operan.** Probado en vivo: lanzar un `general-purpose` quedó bloqueado; un
  `Explore` pasó y devolvió su respuesta.
- **El cableado del expertise funciona.** Editar `userStore.ts` nombra `dev-database.md` antes de
  la edición, sin que nadie lo pida.
- **Los tres fallos del diagnóstico se cerraron:** 0 → 221 documentos con metadata · índice de
  35 → 286 archivos · 5 de 11 sesiones sin registrar → **11 de 11**.

### 🟡 No funciona todavía

- **El tubo pasa vacío.** Los 7 archivos de expertise tienen estructura y cableado, pero su
  criterio son **66 huecos ⬜**. Hoy el sistema responde *"¿cumple las métricas?"*; todavía no
  *"¿lo haría un senior?"* — que era el diferenciador del v2.
- **Nunca ha gobernado trabajo real.** Los commits desde que nació el v2 son el v2 construyéndose,
  migrándose y probándose **a sí mismo**. Cero sesiones de producto. El propio bloque `demo` lo
  registra en su §E: *"untouched on 2026-07-31 — that session built Mente OS v2, not the demo"*.

> La ley que justifica el sistema se midió sobre trabajo de producto. Sobre trabajo de producto,
> el v2 lleva **0 sesiones de evidencia**.

---

## 9 · RESUMEN — solo 3 acciones bloquean

De todo el sistema, únicamente estas detienen el trabajo:

| # | Acción | Puerta |
|---|---|---|
| 1 | destruir datos sin vuelta atrás | `gate-critical` |
| 2 | cerrar un bloque que no se puede reiniciar desde disco | `gate-critical` + `check-sufficiency` |
| 3 | lanzar un especialista que escribe, sin scope declarado | `gate-handoff` |

Más dos negativas fuera del flujo de edición: `pre-commit` (un bloque que viola su contrato) y
`check-clear-ready` (cortar con algo sin guardar).

**Todo lo demás informa.** Esa proporción es deliberada: el sistema se gana el derecho a bloquear
demostrando primero que el criterio funciona.

---

Relacionado: `docs/architecture/` (el diseño completo) · `principles/owner-*.md` (los encargados) ·
`principles/expertise/` (las disciplinas) · `rules/qa-dimensions.md` (las 6 dimensiones) ·
`docs/PENDING-BRIAN.md` (los 66 huecos) · `rules/contract-handoff.md` (la puerta de delegación).
