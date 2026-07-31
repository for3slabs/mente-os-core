# 🔧 Diseño del Fix — BUG-EQUIPO: el equipo multi-agente no hereda la identidad de For3s

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Diseno_Fix_Equipo_Sin_Identidad.md → work/Diseno_Fix_Equipo_Sin_Identidad.md (2026-07-30, ADR-029)

## Purpose

🔧 Diseño del Fix — BUG-EQUIPO: el equipo multi-agente no hereda la identidad de For3s


> **Método:** Fase F0 (Ronda de diseño). Explicar → **aprobar** → construir. NO se toca código
> hasta que Brian apruebe este diseño. Bug confirmado en código: `Doc/Analisis_Conversacion_Domingo_
> RNN_LSTM.md` + memoria `project_bug_equipo_sin_identidad`.

---

## 1 · El problema (recordatorio de 1 línea)

Los 5 specialists se lanzan EN FRÍO: reciben `prompt = f"[{rol}]\n\n{pregunta}"` — sin saber qué es
For3s ni acceso a su memoria. Por eso respondieron *"for3s OS no está definido"* e imaginaron un kernel.

---

## 2 · La restricción que MANDA el diseño (dato medido)

`identidad.ensamblar()` = **~3,747 tokens**. Inyectarla a los 5 specialists = **~18,737 tokens/corrida
SOLO de identidad** → más que triplica el costo actual (~7-8K). **INVIABLE meter la identidad completa.**

→ **Decisión de diseño:** inyectar un **RESUMEN mínimo** de identidad (~150-200 tokens): las 3-4 líneas
que responden "¿qué es For3s?". ×5 = ~1K tokens extra/corrida = aceptable.

---

## 3 · La solución (2 piezas, mínima y defensiva)

### Pieza 1 — Una "cápsula de contexto" ligera (nueva función en `identidad.py`)
```python
def capsula_equipo() -> str:
    """Resumen MÍNIMO de qué es For3s, para inyectar a los specialists sin explotar
    el costo (la identidad completa son ~3.7K tokens; esto ~150). Un párrafo, no la
    máscara completa: solo lo necesario para que el especialista NO alucine 'no sé
    qué es esto'."""
    return (
        "CONTEXTO DEL SISTEMA (no lo repitas, úsalo para no descontextualizar): "
        "For3s OS es un agente de IA 'segundo cerebro', self-hosted y contenerizado, "
        "con memoria real (episodios + grafo de conocimiento + consolidación tipo sueño), "
        "skills, sandbox de código, multi-instancia y equipo multi-agente (tú eres parte "
        "de ese equipo). NO es un sistema operativo de kernel. Cuando la tarea sea sobre "
        "'For3s' o 'for3s OS', se refiere a ESTE sistema.\n\n"
    )
```
- Vive en `identidad.py` (junto al ensamblador — un solo lugar dueño de la identidad).
- Texto corto y estable. Deriva del mismo SOUL, pero resumido a mano (no se auto-genera para no
  arrastrar los 3.7K).

### Pieza 2 — Inyectarla en el prompt del specialist (`specialists.py`)
Cambio de UNA línea en `correr_specialist` (~línea 252):
```python
# ANTES:
prompt = f"[{definicion.rol}]\n\n{entrada}"
# DESPUÉS:
from for3s_core import identidad
prompt = f"{identidad.capsula_equipo()}[{definicion.rol}]\n\n{entrada}"
```
- Import local (dentro de la función) para no crear dependencia circular ni costo de import global.
- El `system=""` se mantiene (regla OAuth-safe del 429). La cápsula va en el USER message, como el rol.

### (Opcional, F2) — El sintetizador también
`sintetizar()` combina los informes. Podría recibir la misma cápsula para que el informe final esté
contextualizado. Menor prioridad (los specialists ya vienen contextualizados). Se decide tras F1.

---

## 4 · Lo que este fix NO hace (alcance acotado a propósito)

- ❌ NO inyecta la **memoria/grafo** de For3s a los specialists (eso es más caro y complejo: qué
  memoria, cuánta, relevante a qué). Se deja como **fase futura** (ver §6). El fix de HOY resuelve el
  "no sé qué es For3s"; el acceso a memoria del equipo es otro pendiente.
- ❌ NO cambia la mecánica del equipo (paralelismo, síntesis, cost control) — todo eso funciona.
- ❌ NO toca líneas rojas (governor/audit/KEK).

---

## 5 · Red de seguridad + verificación (batería §5-BIS)

- **Reusa** el patrón existente (rol en USER message, system="") — cero cambio de arquitectura.
- **Costo acotado y medido:** cápsula ~150 tokens ×5 = ~750 tokens/corrida (vs ~18.7K de la identidad
  completa). Verificar en la corrida real que el total sube <1K.
- **Verificación afirmativa (cuando se construya):**
  1. Volver a lanzar el equipo con "analiza tu estructura de for3s OS" → los specialists YA NO deben
     decir "no está definido" ni hablar de kernel; deben contextualizar sobre el agente real.
  2. Correr una tarea que NO dependa de la identidad ("compara httpx vs requests") → sigue funcionando
     igual (no rompe lo que ya servía).
  3. `/salud` 0 FAIL · tests del equipo verdes · arranque real OK · el resto del sistema intacto.
  4. Confirmar el costo real de la corrida (que subió ~750, no ~18K).
- **Reversible:** es un cambio aditivo de 1 función + 1 línea. Revertir = quitar la cápsula del prompt.

---

## 6 · Fase futura (NO en este fix) — Memoria del equipo

Que los specialists reciban CONTEXTO DE MEMORIA relevante a la tarea (no solo "qué es For3s", sino
"qué sabe For3s de esto"). Requiere: decidir qué memoria traer (semántica sobre la tarea), cuánta
(presupuesto de tokens), y si va a todos o solo a algunos specialists. Conecta con el Frente D (valor
de retorno) y con el rediseño de memoria. → pendiente separado.

---

## 7 · Plan de ejecución (cuando Brian apruebe)

1. **F1:** agregar `capsula_equipo()` a `identidad.py` + inyectarla en `specialists.py` (1 línea).
2. Batería §5-BIS (las 4 verificaciones de §5) en el server.
3. Commit firmado (server-primero). Push solo con orden de Brian.
4. **F2 (opcional):** cápsula también al sintetizador, si en F1 se ve que hace falta.

> **Estimación:** cambio pequeño y quirúrgico (1 función corta + 1 línea + verificación). No es un
> hito grande — es un fix acotado. La parte cara sería la fase futura (memoria del equipo, §6), que
> NO entra aquí.

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Diseno_Fix_Equipo_Sin_Identidad.md`).
