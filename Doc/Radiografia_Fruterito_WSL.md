# 🩻 RADIOGRAFÍA — `Fruterito-wsl/` (generada por el CENSO E1, 2026-07-05)

> **Fuente:** censo automático E1 del HITO ENTRENAMIENTO (import_manifiesto en la BD de
> brian: 11,664 archivos censados, hasheados, datados y deduplicados entre las 2 raíces).
> Detalle archivo-por-archivo: consultable en la BD (`SELECT * FROM import_manifiesto
> WHERE fuente='fruterito-wsl'`). Gemela de `Radiografia_Fruterito_Principal.md`.

## ⭐ EL HALLAZGO MAYOR: wsl es en su mayoría un ESPEJO del principal

**6,600 de los 11,664 archivos totales son duplicados exactos (sha256) entre raíces.**
- `Fruterito-wsl/.openclaw/` = copia COMPLETA del workspace del principal (2,995 archivos
  B5 + 655 B4 + 111 B2 + 27 B1 → **0 únicos**).
- `workspace-empleado/` — el supuesto "mar de 734 docs" — es el MISMO workspace
  sincronizado: de sus 1,011 archivos B5 solo **5 son únicos**; de sus 113 B2, solo 5.
  🍊 El "Fruterito Empleado" compartía el cerebro documental con el Personal.
- Consecuencia para el entrenamiento: **cero riesgo de doble-import** (el manifiesto ya
  marca `duplicado_de`) y el volumen REAL a importar es mucho menor de lo censado a mano.

## Lo ÚNICO que wsl aporta (archivos sin duplicado, por bloque)

| Bloque | Únicos | Peso | Qué es |
|---|---:|---:|---|
| **B3 conversaciones** | 48 | 26.8 MB | 🥇 EL TESORO: las sesiones del `agents/main` (el Fruterito Personal REAL, 6,045 turnos) + cipher + helix + únicos del backup-20260404 |
| **B4 skills** | 414 | 17.4 MB | skills/mode_{ahorro,normal,turbo,ultra} de raíz + skills del empleado no presentes en principal |
| **B7 media** | 97 | 8.8 MB | media propia de wsl |
| **B6 runtime** | 38 | 9.2 MB | browser/ (8.4MB), completions, flows, tasks, sqlite |
| **B1 identidad** | 27 | 257 KB | workspace-for3s-design (8) + raíces únicas de empleado (12) + workspace propio (7) |
| **B2 memoria escrita** | 12 | 44 KB | diarios/memoria no presentes en principal |
| **B5 conocimiento** | 15 | 81 KB | lo poquito de docs realmente nuevo |
| **SECRETO** | 19 | 34 KB | credentials/ (6 telegram-*.json), identity/, auth-profiles, .env |

## Secretos (detector v1, TODO el material)

**67 archivos-secreto por ruta** (vs 47 del censo manual — el detector cazó 20 más:
los 5 backups de openclaw.json con botTokens, paired.json, device-auth…) + **81 archivos
con secretos EMBEBIDOS** en su contenido (flagueados para redacción línea a línea en las
olas). Lista completa en `import_manifiesto WHERE bloque='SECRETO'`.

## Línea de tiempo maestra (histograma del censo — define las OLAS de E3)

```
2026-01  arranque (4 sesiones)          │ OLA 1 · "génesis" (ene+feb)
2026-02  nacimiento: B1 47 · B2 90 ·    │   identidad temprana + 1ros diarios
         B3 31 · B5 4504* · B7 383      │   (*B5 datado por mtime: proyectos)
2026-03  EL PICO: B2 210 · B3 101 ·     │ OLA 2 · mar 1-15
         B5 2483 · B7 914               │ OLA 3 · mar 16-31 (lo más denso)
2026-04  el final: B3 108 · B2 37       │ OLA 4 · abril (cierre de la era)
2026-05  residuo mtime: 66 unidades     │ OLA 5 · residuo/verificación
```
*(B2/B3 con fecha REAL interna; B5/B7 por mtime — suficiente para asignar ola.)*

## Correcciones al censo manual previo

1. "Empleado = 708 docs propios" → FALSO: es espejo del workspace personal (5 únicos).
2. El main real vive en wsl (48 archivos únicos de sesión) — confirmado.
3. Secretos reales = 67 por ruta (no 47) + 81 embebidos.

*Manifiesto vivo en BD de brian · Plan: `Plan_Implementacion_Entrenamiento.md` · E1 ✅*
