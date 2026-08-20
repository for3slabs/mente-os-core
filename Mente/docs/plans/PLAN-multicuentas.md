# PLAN · Sistema de multi-cuentas para Mente OS v2

**Status:** current · **Type:** plan · **Updated:** 2026-08-19 · **Owner:** brian
**Block:** `blocks/active/multicuentas/BLOCK.md` · **Verified by:** **bin/check-accounts** — ⬜ la crea la F2 de este mismo plan
**Level:** 🔧 MOTOR — viaja con el clon · el registro y las guías son 📦 INSTANCIA

## Purpose

Que Mente OS sepa **qué cuenta usa cada repo, por qué existe y cómo se accede** — de forma segura,
verificable y para cualquiera que clone el motor, no solo para Brian.

> **Brian, 2026-08-19:** *"va a haber muchos repositorios, muchas cuentas que debemos de tener
> control y saber a detalle por qué existen y de dónde están saliendo los commits y hacia dónde.
> No podemos tener un sistema que no pueda controlar eso."*

---

## 0 · EL PROBLEMA, MEDIDO — no es hipotético

Este plan nace de un fallo real del sistema sobre sí mismo:

| Documento | Decía | Realidad en la máquina | Días equivocado |
|---|---|---|---|
| `PROJECT-RULES.md` §4 | `fruterito101/for3s` es el repo de la verdad | movido a `for3slabs` el 4-jul | **46** |
| `project_repo_oficial_for3s` | `for3s-os` es *"copia vieja, archivar"* | es el `origin` del servidor | **31** |
| `RETOMAR.md` §3 | tríada sincronizada en `f50a5db` | 2 commits sin empujar desde el 23-jul | **24** |

⭐ **La causa raíz es una sola:** ningún validador comparaba lo escrito contra `git remote -v`.
Es la ley del propio sistema aplicada a sí mismo — *una regla sin validador se cumple 40-60%*.

**El coste medido:** 2 commits firmados vivieron 24 días fuera de GitHub. Si el servidor muere,
se pierden. No es teoría: el 30-jun ya pasó con **34 commits**.

---

## 1 · QUÉ SE CONSTRUYE — 6 piezas, y qué mitad es cuál

```
🔧 MOTOR — viaja con el clon, cualquiera lo hereda
   bin/check-accounts       el validador   → ¿lo escrito coincide con la máquina?
   bin/conectar-cuenta      el resolutor   → ¿con qué credencial toco este repo?
   hooks/gate-accounts.py   la puerta      → detiene un push a un repo no registrado

📦 INSTANCIA — se genera para CADA usuario, nunca viaja
   cuentas.tsv                        el registro de ESTA persona
   secrets/Acceder_Cuenta_<x>.md      una guía por cuenta
   secrets/.access-log.md             ya existe — se extiende
```

⭐ **Por qué esta división es el producto:** si el registro viajara en el clon, quien clone Mente OS
heredaría las cuentas de Brian — exactamente la contaminación que `rules/rule-inheritance.md` existe para
impedir. El motor sabe **cómo** gobernar cuentas; la instancia dice **cuáles**.

---

## 2 · F1 · **cuentas.tsv** — el registro

Una fila por repo. TSV y no Markdown por la misma razón que `piezas.tsv`: una máquina lo lee sin
parsear prosa, y añadir un repo cuesta una línea.

```
# repo	cuenta	rol	remoto	por_que_existe	guia
for3slabs/for3s-os	for3slabs	taller	origin	el servidor empuja aquí a diario	Acceder_Cuenta_for3slabs.md
for3slabs/for3s	for3slabs	backup	backup	respaldo del producto verificado	Acceder_Cuenta_for3slabs.md
for3slabs/mente-os-for3s	for3slabs	motor	origin	este sistema	Acceder_Cuenta_for3slabs.md
for3slabs/mente-os-maestro	for3slabs	control	—	apunta a las 5 ramas sin replicarlas	Acceder_Cuenta_for3slabs.md
ElBrAyAn1967/For3s	ElBrAyAn1967	sitio	origin	la demo/web Next.js — NO el agente	Acceder_Cuenta_ElBrAyAn1967.md
fruterito101/mente-os	fruterito101	publicado	origin	el motor MIT para terceros	Acceder_Cuenta_fruterito101.md
```

⭐ **La columna `por_que_existe` es obligatoria y es el corazón del registro.** Brian: *"cada uno de
los repositorios debe de tener un por qué de su existencia, si no es basura."* Un repo que no puede
justificar su fila **se archiva o se borra** — la fila es la prueba de que alguien lo pensó.

⛔ **La columna `guia` apunta al archivo; NUNCA hay un token en este `.tsv`.** El registro va en git;
las guías, no.

---

## 3 · F2 · **bin/check-accounts** — el validador que cierra el agujero

**La comprobación central, la que ningún documento tenía:**

| # | Qué mide | Cómo |
|---|---|---|
| 1 | 🔴 **cada remoto real está registrado** | `git remote -v` → ¿su URL está en **cuentas.tsv**? |
| 2 | 🔴 **cada fila apunta a un repo que existe** | resuelve la URL; un 404 es una fila fósil |
| 3 | 🔴 **ninguna fila sin `por_que_existe`** | un repo sin porqué es basura declarada |
| 4 | 🔴 **su `guia` existe en `secrets/`** | una guía citada y ausente es un acceso que nadie puede repetir |
| 5 | 🟡 **un repo con 2 remotos declara ambos** | el defecto de hoy: se empuja a uno y divergen |
| 6 | 🔴 **ningún `.tsv` ni guía contiene algo con forma de token** | regex `ghp_|gho_|github_pat_|-----BEGIN` |

**Probado por sabotaje** (`rule-checks-must-measure.md`): se añade un remoto no registrado y debe
ponerse 🔴; se borra un `por_que_existe` y debe ponerse 🔴. **Un check solo visto en verde no cuenta.**

---

## 4 · F3 · Las guías `secrets/Acceder_Cuenta_<cuenta>.md`

Tres archivos, misma forma que `Conectar_Servidor_For3s.md` (el patrón probado): pasos numerados,
comandos copiables, verificación al final.

**La diferencia crítica con la guía del servidor:**

| | `Conectar_Servidor_For3s.md` (hoy) | `Acceder_Cuenta_*.md` (nuevo) |
|---|---|---|
| Credencial | ⚠️ contraseña **en claro** | ⛔ **nunca el valor** |
| Qué dice | *"la contraseña es X"* | *"el token vive en `<ruta>`; se pide así"* |

⭐⭐ **Por qué NO se replica el patrón entero:** la guía del servidor lleva la contraseña en texto
plano, y por eso la carpeta es `700` y está fuera de git. **Copiar eso 3 veces multiplica por 3 la
superficie expuesta.** Las guías nuevas son **punteros**: dicen dónde vive y cómo pedirlo.

Cada guía lleva: qué cuenta es · qué repos abre · dónde vive su credencial · cómo verificar que
funciona (`gh auth status`) · qué hacer si falla · **cuándo NO usarla**.

---

## 5 · F4 · **bin/conectar-cuenta** — cómo lo pide el LLM, de forma segura

Espejo de `bin/conectar-servidor`, que ya funciona.

```bash
bin/conectar-cuenta for3slabs/for3s-os      # → qué cuenta, qué guía, si hay credencial viva
```

**El contrato de seguridad, en 4 reglas:**

| Regla | Por qué |
|---|---|
| ⛔ **nunca imprime el valor de una credencial** | imprime la RUTA y el estado (`viva`/`ausente`) |
| ✅ **lee la credencial solo con lease vivo** | reusa `gate-secrets.py`, ya probado |
| ✅ **toda invocación va a `.access-log.md`** | quién, qué repo, cuándo — ya existe la bitácora |
| 🔴 **repo no registrado → exit 2 y no resuelve nada** | fail-closed: ante duda, no da acceso |

⭐ **Esto es lo que responde *"cómo lo va a solicitar el LLM"*:** el agente **nunca** pide un token.
Pide *"conéctame a este repo"*, y el motor decide si puede, con qué cuenta y deja el rastro.

---

## 6 · F5 · **hooks/gate-accounts.py** — la puerta

Se dispara **antes de un `git push`, `gh pr create` o `gh repo`**.

| Situación | Respuesta |
|---|---|
| push a un repo **registrado**, con su cuenta correcta | ✅ allow |
| push a un repo con **2 remotos** y solo se empuja a 1 | 🟡 **ask** — *"`backup` quedará atrás. ¿Sigo?"* |
| push a un repo **NO registrado** | 🔴 **exit 2** — *"regístralo en **cuentas.tsv** primero"* |
| cualquier operación que **crearía o borraría** un repo | 🔴 **exit 2** — es de Brian |

⭐ **La fila 🟡 es el bug de hoy convertido en candado.** El 23-jul se empujó a un remoto y no al
otro, y nada avisó durante 24 días.

**Cuando la puerta bloquea, su mensaje ES el recibo** (`ADR-030`): qué repo, por qué se detuvo, y
el comando exacto para resolverlo.

---

## 7 · F6 · Cablear — que nada quede suelto

| Dónde | Qué se declara |
|---|---|
| `piezas.tsv` | las 3 piezas nuevas de motor (lo exige la batería) |
| `CAPABILITIES.md` §2 | los 2 comandos nuevos, con la pregunta que responden |
| `CAPABILITIES.md` §3 | `gate-accounts` en la tabla de puertas |
| `.claude/settings.json` | el hook registrado — **`deny` idéntico en ambos settings** (`rule-config-hygiene` §1.6) |
| `bin/test-f0-f6` | ⭐ **§F7 nuevo: los 6 checks + los 2 sabotajes** |
| `secrets/README.md` | la tabla "qué hay aquí" lista las 3 guías |
| `bin/init` | genera **cuentas.tsv** vacío con cabecera para un clon nuevo |
| `PROJECT-RULES.md` | apunta al registro en vez de nombrar repos a mano |

⛔ **F6 no es opcional.** Una pieza construida y no cableada es el patrón que este proyecto ya
documentó **3 veces** (`crypto.py`, workspaces, BYOK): *se construye la pieza y nadie pasa por ella*.

---

## 8 · ORDEN, Y POR QUÉ NO ES NEGOCIABLE

```
F1 registro → F2 validador → F3 guías → F4 resolutor → F5 puerta → F6 cableado
```

⭐ **F2 antes que F3-F5** porque el validador es lo que impide que el registro nazca ya mintiendo —
que es exactamente lo que pasó con los 3 documentos.
⭐ **F5 al final** porque una puerta sobre un registro incompleto **bloquea trabajo legítimo**, y una
puerta que estorba se termina desactivando.

**Cada fase entra por su PR contra `master`** (`rule-pr-base.md`) — ⛔ no se encadenan.

---

## 9 · LO QUE ESTE PLAN NO HACE

| No hace | Por qué |
|---|---|
| ⛔ escribir un token en ningún archivo | `PROJECT-RULES.md` §5 |
| ⛔ rotar o revocar credenciales | decisión de Brian |
| ⛔ crear, borrar o cambiar visibilidad de repos | ídem |
| ⛔ tocar el Key Vault del producto | `secrets/README.md` separa acceso-de-Brian de secrets-del-sistema |
| ⛔ decidir qué repos sobran | el registro **expone** los sin-porqué; Brian decide |

---

## 10 · CÓMO SE SABRÁ QUE FUNCIONÓ

| Prueba | Verde si |
|---|---|
| **bin/check-accounts** | 0 errores, y **falla al sabotearlo** en las 2 direcciones |
| Un remoto no registrado | la puerta lo detiene con su recibo |
| Empujar a 1 de 2 remotos | avisa antes, no 24 días después |
| `bin/test-f0-f6` | §F7 verde · `failed: 0` |
| ⭐ **Un clon limpio** | `bin/init` genera **cuentas.tsv** vacío y `check-accounts` pide llenarlo — **sin heredar las cuentas de Brian** |

---

Related: `blocks/active/multicuentas/BLOCK.md` · `secrets/README.md` · `hooks/gate-secrets.py`
(el patrón de lease que se reusa) · `rules/rule-checks-must-measure.md` · `rules/rule-config-hygiene.md` ·
`CAPABILITIES.md` · `Maestro/punteros.tsv` (donde apareció la 3ª cuenta).
