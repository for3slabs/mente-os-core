# HALLAZGO · seguridad · Fase 1 (NODOS)

**Status:** current · **Type:** analysis · **Updated:** 2026-08-14 · **Owner:** brian
**Bloque:** `blocks/active/seguridad/BLOCK.md` · **Campaña:** `campaigns/producto-for3s-os/CAMPAIGN.md`
**Fase:** 1 de 3 — ¿existe cada pieza que el Grafo declara, y hace lo que dice?
**Vara:** el gate de la **Fase 1** del `memory/archive/Plan_Maestro_Programacion.md`, no el Grafo completo
(`rules/rule-product-authority.md` §2)

## Purpose

**El veredicto medido de la capa de seguridad de For3s OS**, pieza por pieza, con el comando que
lo produjo. Cierra la Fase 1 del bloque `seguridad` — el primero de los 12 de la campaña.

⛔ **No arregla nada.** La Fase 1 mide; arreglar durante la medición la contamina.

---

## 1 · EL VEREDICTO EN UNA FRASE

> ⭐⭐ **La seguridad de For3s OS está bien CONSTRUIDA y mal CABLEADA.** Las 5 piezas existen,
> funcionan y resisten un ataque. Lo que falla es que **el contenido de las conversaciones nunca
> pasa por la criptografía que el propio sistema construyó.**

| Dimensión | Veredicto | Evidencia |
|---|---|---|
| Criptografía | 🟢 **cumple** | AES-256-GCM, nonce 12 B/mensaje, HKDF-SHA256 por workspace |
| Custodia de la llave | 🟢 **cumple** | `~/.for3s/master.key` · 32 B · `600` · fuera del repo |
| Secretos en BD | 🟢 **cumple** | 38 filas `nonce`+`ciphertext`, sin columna en claro |
| Cadena de auditoría | 🟢 **cumple** | 12,963 eslabones verificados **uno a uno** + sabotaje |
| Aislamiento del sandbox | 🟢 **cumple** | 5 ataques, los 5 contenidos |
| **Contenido de conversaciones** | 🔴 **NO cumple** | **15 MB legibles**, `encrypt(` en 1 solo sitio |

**5 de 6 dimensiones en verde.** La sexta es H-01.

---

## 2 · EL HALLAZGO 🔴 — H-01, contenido en claro

### Qué se midió

| Medida | Valor |
|---|---|
| Texto de conversaciones **en claro** | 🔴 **15 MB** (33,908 filas) |
| `encrypt(` en código de producción | 🔴 **1 solo sitio** — `secret_store.py:40` |
| Puntos que **ESCRIBEN** `content` | **2** — `memory.py:93` · `entrenamiento.py:73` |
| Archivos que **LEEN** `content` con SQL propio | 🔴 **9** |
| Capa central de acceso al contenido | 🔴 **no existe** |
| Consumidores de `crypto.py` | solo `secret_store.py` y `automod.py` |

Los 9 lectores: `insights` · `consolidator` · `microglia` · `hilo_status` · `perfil_infer` ·
`memory` · `dmn_tasks` · `entrenamiento` · `confidence`.

> ⚠️ **CORRECCIÓN a la primera versión de este documento (14-ago).** Decía *"10+ escritores"*.
> **Falso:** conté archivos que MENCIONAN la tabla, no los que escriben. Los escritores son **2**
> y el trabajo real está en los **9 lectores** — donde no había mirado. ⭐ El error importa porque
> **dimensionaba mal el arreglo**: cifrar los 2 INSERT sin tocar los 9 lectores rompe la memoria,
> la microglía, el consolidador y el perfil — **y no ruidosamente**: fallaría la próxima vez que
> el agente intente recordar.

### Por qué es un hallazgo de HOY y no de una fase futura

Dos autoridades independientes lo exigen, y las dos son de v1:

1. **El Grafo Maestro** (`Cerebro/For3s_OS_Grafo_Maestro.md:112`, Pilar 1 **LOCKED**):
   *"End-to-end encryption es requirement v1"* · ⭐ *"No es una capa encima del grafo.
   **Es propiedad de cada conexión.**"*
2. ⭐ **El propio módulo.** El docstring de `crypto.py` declara *"Los secretos **NUNCA** viven en
   texto plano en BD ni en el repo"* y *"**Decrypt minimum**: el plaintext existe solo el instante
   en que se usa"*. Se cumple para los 38 secretos; **no se cumple para los 15 MB.**

⭐ **La segunda es la que cierra la discusión:** descarta la lectura benigna de *"nunca se
pretendió cifrar el contenido"*. Sí se pretendió — está escrito en el código, y no se cableó.

⚠️ Uno de los mensajes legibles dice literalmente ***"Sigue diciendo que es privado"*** — la
distancia exacta entre lo que el sistema promete y lo que hace.

### 🔴 Y lo que este bloque CORRIGIÓ de sí mismo: H-01 no empeora solo

**Abrí este bloque afirmando tres veces que H-01 crecía cada día.** Medido: **es falso.**

| Origen | Filas | Tamaño | Rango de fechas |
|---|---|---|---|
| **Importado** (entrenamiento) | **33,737** | **15 MB** | 29-ene → 30-may |
| **Vivo** (uso real) | **171** | **81 kB** | 5-jul → 30-jul |

```
Crecimiento en los últimos 60 días ....  81 kB
Último mensaje real ...................  2026-07-30  (hace 16 días)
Junio y agosto ........................  CERO filas
```

⭐ **El criterio "severidad × velocidad" era correcto; el dato que le metí, no.** La velocidad
real es ~0, así que **H-01 no gana por urgencia: gana por gravedad.** 15 MB de conversaciones
legibles siguen expuestas hoy, crezcan o no.

⚠️ **De dónde salió el error:** lo deduje de que la BD pesaba 15 MB y el bot corría en producción.
**Nunca medí la fecha de las filas.**

---

## 3 · LAS 5 FORTALEZAS — medidas, no leídas

⭐ **Un informe que solo reporta lo roto enseña a desconfiar del veredicto entero**
(`rules/qa-dimensions.md`: veredicto por dimensión, no una nota global).

### 3.1 · La criptografía está bien hecha

`crypto.py` (69 líneas) exporta las 4 funciones declaradas: `load_or_create_master_key` ·
`derive_workspace_key` · `encrypt` · `decrypt`. AES-256-GCM con nonce aleatorio de 12 B por
mensaje y derivación HKDF-SHA256 por workspace.

### 3.2 · La llave maestra está bien custodiada

`~/.for3s/master.key` — **32 bytes**, permisos **`600`**, **fuera del repo**. Exactamente lo que
su propio docstring promete.

### 3.3 · Los secretos SÍ se cifran

Tabla `secrets`: **38 filas** con `nonce` + `ciphertext`. **No existe columna en claro.**

### 3.4 · La cadena de auditoría es íntegra — EJECUTADA, no contada

⚠️ Contar que 12,963 filas tienen sus 3 campos no nulos **no prueba que encadenen**. Se corrió
`audit.verify_chain()` dentro del contenedor:

```
INTEGRA: True | entradas: 12963
```

⭐ **Y verificada por SABOTAJE**, que es lo que convierte ese `True` en evidencia:

| Prueba | Resultado |
|---|---|
| hash recomputado == guardado | ✅ `True` |
| tras alterar un campo `detail` | 🔴 `False` — **detectado** |

⛔ Hecho **en memoria, sin tocar la tabla real**: sabotear el registro de auditoría de producción
para probar que funciona sería el peor cambio posible.

### 3.5 · El sandbox aísla — probado ATACÁNDOLO

Cinco ataques contra el contenedor vivo `for3s-brian-sandbox-1`:

| Ataque | Resultado |
|---|---|
| ¿corre como root? | ✅ no — `uid=10001(sandbox)` |
| ¿monta el socket de Docker? (escape total) | ✅ **no** |
| ¿alcanza la BD del agente? | ✅ no — `postgres` no resuelve |
| ¿ve los secretos del agente? | ✅ **cero envs** — ni Anthropic, ni Telegram, ni BD |
| ¿el timeout corta un bucle infinito? | ✅ **5.0 s exactos, exit `-9`** (SIGKILL) |
| ¿escribe fuera de su workspace? | ✅ no — `open("/etc/…","w")` → exit 1 |

El único env "sensible" que apareció es `GPG_KEY`: 40 caracteres hex = la **huella pública** de
firma de la imagen base de Python, no un secreto.

---

## 4 · LO ANOTADO, QUE NO ES HALLAZGO

### 4.1 · El sandbox tiene salida a internet — a propósito

Medido: `HTTP 200` a `example.com`. ⛔ **No es un defecto.** El compose lo declara con su razón:
*"Conserva salida a internet (pip/npm de execute_code); sin la red interna"*.

⭐ **Una decisión de diseño que se declara y se cumple no es deuda**
(`rules/rule-product-authority.md`). ⚠️ Lo que sí queda para el dueño: egreso abierto significa
que código generado por el LLM **podría exfiltrar lo que tenga a mano**. Hoy no tiene nada — el
riesgo depende de que eso siga siendo cierto.

### 4.2 · La auditoría cubre lo automático, no lo humano

| Actor | Eventos | % |
|---|---|---|
| `microglia` | 11,503 | **89%** |
| `cls_orchestrator` | 1,020 | 8% |
| `for3s` | 287 | 2% |
| **usuario** | **110** | **0.8%** |

En los últimos 7 días **solo corrió lo automático**: 532 podas · 8 consolidaciones · 1 alta de API.

⭐ **Cruzado con §2, el sesgo se explica solo:** no es que la auditoría ignore al humano — **el
humano lleva 16 días sin escribir.** La cadena registra fielmente un sistema que solo se habla a
sí mismo. Y es **lo único vivo** de esta capa: último evento **hoy**.

### 4.3 · Un solo workspace, aunque el código soporta varios

Los 12,963 eventos viven en `workspace_id = 'default'`. `derive_workspace_key` existe y funciona.
⚠️ **Capacidad construida y no cableada — el mismo patrón que H-01, en otro sitio.** Repetido dos
veces deja de ser *"un cable suelto"* y pasa a ser **una forma de trabajar**.

### 4.4 · Lo que NO se auditó, y por qué no es deuda

**Auth/RBAC · Output Gate · Prometheus** son **Fase 4-5** del plan → se registran **FUTURO**.
⭐ Medido: contra el Grafo completo, 24 hallazgos y 15/15 tablas ausentes sobre un sistema que
corre a diario; contra el gate de la fase, **6/6 y 4 accionables**. Los otros 20 eran prematuros
— y **uno prematuro se ve idéntico a uno urgente**, así que entierra a los que sí importan.

---

## 5 · LO QUE ESTA FASE ENSEÑÓ DEL MÉTODO

⭐ **La Fase 1 tumbó una premisa del propio bloque que la ejecuta.** Si el paso que midió el ritmo
hubiera ido después del arreglo, **habríamos cifrado 15 MB con la urgencia equivocada**. La fase
existe exactamente para eso: mirar los nodos antes de tocar nada.

⭐ **Y el primer sub-bloque —confirmar las rutas contra el servidor— se justificó solo:** las 5
rutas declaradas estaban mal en el prefijo. Con ese `§B`, `hooks/pre-edit-standards.py` no habría
reconocido ni un archivo y el editor habría trabajado sin estándares, **en silencio**.
**Un `§B` derivado no falla ruidosamente: falla callando.** Por eso ese paso va en los 12.

---

## 6 · ⭐ EL ARREGLO — decidido por Brian el 2026-08-14

> **Brian:** *"vamos por la capa única, de lo que solucionamos el problema a la perfección."*

### 6.1 · Por qué capa única y no que cada lector descifre

| Opción | Puntos a tocar | Veredicto |
|---|---|---|
| Cada lector descifra por su lado | 9 sitios independientes | ⛔ **descartada** |
| ⭐ **Capa única de acceso** | 1 módulo + 11 puntos que la usan | ✅ **elegida** |

⭐ **La razón no es preferencia, es coherencia con lo que este mismo bloque diagnosticó:** el
defecto de For3s OS es *"se construye la pieza y no se conecta"* (§4.3, el mismo patrón en dos
sitios). **Resolver H-01 dispersando el descifrado en 9 lugares sería cometer ese error mientras
se arregla su síntoma** — y crearía 9 sitios donde el próximo desarrollador puede olvidarse.

### 6.2 · Los 4 sub-bloques, en orden, con lo que cada uno arriesga

| # | Qué | Riesgo | Reversible |
|---|---|---|---|
| **SB-7** | `contenido.py` — la capa: cifra al escribir, descifra al leer | 🟢 código nuevo, nadie lo usa aún | sí |
| **SB-8** | los **2 escritores** pasan por la capa | 🟡 lo nuevo entra cifrado | sí — se apaga |
| **SB-9** | los **9 lectores** pasan por la capa | 🟠 toca el núcleo de la memoria | sí |
| **SB-10** | migrar los **15 MB** existentes | 🔴 **reescribe 33,908 filas** | ⚠️ solo con backup |

⭐ **El orden importa y no es negociable:** la capa antes que sus usuarios, los lectores **antes**
que la migración. Si SB-10 fuera antes que SB-9, el sistema quedaría leyendo datos cifrados con
código que espera texto plano — **roto entre dos pasos**.

### 6.3 · ✅ El rollback está PROBADO, no supuesto

```
dump ....................  pre-cifrado-h01-20260815-024048.dump  ·  131 MB
prueba de restauración ..  BD desechable → 33,908 filas ✅
BD de prueba ............  eliminada
```

⭐ **Un dump que nunca se restauró no es un rollback, es un archivo.** Además existe respaldo
automático diario (verificado: `auto_for3s_20260814_070000.sql`, 384 MB).

### 6.4 · Por qué cifrar es técnicamente viable

Medido: **cero búsquedas por texto** sobre `content` — sin `LIKE`, sin `tsvector`, **sin índice de
texto** en la tabla. La búsqueda semántica va por `embedding`. ⭐ **Nada del sistema depende de
leer `content` como texto buscable**, que es lo que normalmente impide cifrar una columna.

### 6.5 · 🟠 H-19 — el hallazgo que el arreglo destapa

**Los embeddings (133 MB) son vectores derivados del texto y quedan en claro.** Cifrar `content`
sin tocarlos deja el contenido **parcialmente reconstruible**.

⛔ **No entra en este arreglo, por decisión de Brian (14-ago):** cifrar embeddings rompe la
búsqueda por similitud — pgvector no compara vectores cifrados. **Es una decisión de arquitectura,
no parte de H-01.** Queda registrado como **SB-11** en el §F del bloque, bajo el radar de
`bin/generate-index`, que lo publica en `docs/STATES.md` en cada corrida.

---

## 7 · QUÉ SIGUE

**La Fase 2 (ESTRUCTURA)** mira cómo está escrito lo que aquí se midió: redundancia, cuellos de
botella, archivos que crecen. ⛔ **Ninguno de los 5 archivos de este bloque supera las 105 líneas**,
así que la pregunta de partir archivos grandes **no aplica aquí** — aplica a `canal-telegram`
(4,570) y `agente` (1,871).

🙋 **Decide Brian, con el hallazgo en la mano:** si H-01 se arregla ya (conectar la cripto en los
10+ escritores + migrar los 15 MB existentes) o se agenda. ⚠️ Migrar datos en producción exige su
OK explícito (`CLAUDE.md`), así que **este documento no lo propone: lo deja medido.**

---

Related: `blocks/active/seguridad/BLOCK.md` (el bloque que lo produjo) ·
`campaigns/producto-for3s-os/CAMPAIGN.md` (la campaña) ·
`docs/plans/PLAN-3-fases.md` (qué mira cada fase) ·
`campaigns/producto-for3s-os/terreno/AUDITORIA-FOR3S-OS-2026-08.md` (el terreno del 12-ago) ·
`rules/rule-product-authority.md` (la vara temporal) · `rules/qa-dimensions.md` (veredicto por dimensión).