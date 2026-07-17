# 🐙 Análisis: por qué For3s NO se posiciona en GitHub (vs doc oficial, 2026-07-04)

> **Brian (URGENTE):** "en GitHub no aparece el repositorio aunque sea público. Los programadores tienen
> que conocerlo, y no es así. Necesito un análisis a detalle de toda la documentación, no omitas nada."
> **Método:** leí la doc OFICIAL de GitHub (docs.github.com) sobre topics, búsqueda de repos, README y
> perfiles, y la crucé contra el estado REAL del repo `fruterito101/for3s` (verificado por API).

---

## 0. LA VERDAD DE FONDO (lo más importante)

**GitHub NO documenta su algoritmo de ranking — es secreto a propósito.** La doc de "searching for
repositories" es explícita en los QUALIFIERS (stars:, forks:, pushed:, topic:, language:, is:public…)
pero **silenciosa sobre CÓMO se ordena el "best match"** (el sort por defecto). Sin embargo, de lo que sí
publica + cómo funciona en la práctica, la conclusión es inequívoca:

> **GitHub posiciona por SEÑAL SOCIAL (stars, forks, tráfico, actividad reciente, edad/autoridad), NO por
> metadata.** Nuestra metadata (topics/description/README/license) está BIEN. Nuestra señal social es casi
> CERO. **"No aparece" = falta popularidad, no falta configuración.**

Esto encaja con lo que ya vimos en el OpenSSF Scorecard: el check "Maintained" penaliza repos <90 días.
GitHub premia lo que la comunidad YA validó (stars) — es un problema de arranque (cold start), no de setup.

---

## 1. QUÉ DICE LA DOC OFICIAL (a detalle, sin omitir)

### 1.1 · Topics (classifying-your-repository-with-topics)
- **Máximo 20 topics.** Formato: lowercase, números y guiones, ≤50 caracteres.
- Buenos topics = propósito, área temática, comunidad, lenguaje del repo.
- Descubribilidad: los usuarios pueden **buscar repos por topic** y navegar `github.com/topics/`. Los
  topics aparecen en la portada del repo → clic lleva a "topics relacionados + otros repos del topic".
- GitHub **auto-sugiere topics** analizando el contenido de repos PÚBLICOS (los privados no).
- Los nombres de topic son SIEMPRE públicos.
- **La doc NO especifica** algoritmo de ranking de topic pages, criterios de "featured", ni cómo el About
  (description/website) influye en la búsqueda más allá de ser editable.

### 1.2 · Búsqueda de repos (searching-for-repositories)
- **Qualifiers de contenido:** `in:name`, `in:description`, `in:readme`, `topic:`.
- **Qualifiers de métricas:** `stars:`, `forks:`, `followers:`, `size:`.
- **Temporales:** `created:`, `pushed:` (ISO8601). `pushed:` ordena por commit más reciente.
- **Técnicos:** `language:`, `license:`, `is:public/is:private`, `archived:`, `template:`, `mirror:`,
  `is:sponsorable`.
- **⚠️ La doc NO explica** cómo funciona "best match", si stars/forks influyen en el orden, ni qué señales
  usa el ranking. (Silencio deliberado = el algoritmo es secreto. Pero los qualifiers `stars:`/`forks:`
  existen porque la popularidad ES el eje de descubrimiento.)

### 1.3 · README (about-readmes)
- Es "lo primero que ve un visitante". GitHub lo surface en orden: `.github/` → raíz → `docs/`.
- Debe cubrir: propósito, cómo empezar, soporte, cómo contribuir.
- ⭐ **Perfil README:** un README en un repo público con el MISMO nombre que tu usuario (`user/user`)
  **aparece automáticamente en tu página de perfil.**
- La doc (en esa página) no detalla indexación de búsqueda ni Open Graph — pero el README SÍ es indexable
  (existe el qualifier `in:readme`), así que las keywords del README importan para la búsqueda.

### 1.4 · Otras features de descubribilidad (mencionadas en la doc de GitHub)
- **Social preview (Open Graph):** imagen al compartir el link del repo (X/LinkedIn/Slack).
- **GitHub Pages:** sitio hosteado desde el repo (indexable por Google → SEO).
- **Releases:** versiones publicadas, visibles en la portada.
- **Discussions / Wiki:** señales de comunidad viva.
- **Pinned repos:** destacar en el perfil.
- **Sponsors:** `is:sponsorable` es qualifier de búsqueda.

---

## 2. AUDITORÍA DEL REPO (verificado por API, 2026-07-04)

| Elemento (de la doc) | Estado real | Veredicto |
|---|---|---|
| Description | ✅ "For3s OS - The self-hosted AI second brain…" | OK |
| Topics | ✅ 14/20 | OK (dentro del límite, bien elegidos) |
| README con badges/imágenes | ✅ 6 elementos visuales | OK |
| Social preview (Open Graph) | ✅ HTTP 200 | OK |
| License | ✅ AGPL-3.0 | OK |
| Releases | ✅ 1 (v0.14.0) | ⚠️ falta v0.15.0 |
| **⭐ Stars** | 🔴 **3** | **PROBLEMA #1** |
| Forks / Watchers | 🔴 0 / 0 | señal social nula |
| Homepage | 🔴 for3s.vercel.app = web de QA, NO del agente | MAL |
| GitHub Pages | ❌ False | oportunidad perdida |
| Discussions / Wiki | ❌ False / False | menos comunidad |
| Perfil README (`fruterito101/fruterito101`) | 🔴 404 | no existe |
| Cuenta | ⚠️ Usuario personal, 2 followers, 25 repos públicos | poca autoridad |
| Edad | ⚠️ creado 2026-06-27 (<90 días) | penalización de "nuevo" |
| Lenguaje | Python | OK |

---

## 3. LAS 4 RAZONES REALES DE POR QUÉ NO APARECE

1. **Pocas stars → invisible en el sort por defecto.** Con 3 stars, el repo queda debajo de miles con
   cientos/miles. Nadie busca y ordena por "más reciente"; ven los top. GitHub premia validación social.
2. **Repo nuevo + cuenta personal con 2 followers.** Poca autoridad, sin red que amplifique. El Scorecard
   ya marcaba "Maintained" bajo por <90 días.
3. **Homepage al lugar equivocado.** Quien llega al repo y hace clic en el sitio → cae en la web de For3s
   QA (marca-personal), no del agente. Se pierde al visitante justo cuando lo tenías.
4. **Cero puertas de entrada externas.** Sin perfil README, sin awesome-lists, sin Discussions, sin Pages.
   GitHub te encuentra si YA sabes que existes; no hay canales nuevos de descubrimiento.

---

## 4. PLAN DE ACCIÓN (orden de impacto — lo que la doc dice que SÍ mueve la aguja)

**FASE 1 — arreglar lo que engaña/pierde visitantes (barato, ya):**
1. Arreglar el **homepage** del repo → al sitio del agente (o quitar el de QA hasta tener uno).
2. Crear **perfil README** `fruterito101/fruterito101` (aparece auto en el perfil, gratis).
3. Actualizar **Release a v0.15.0** con notas atractivas.
4. **README top-tier**: demo GIF arriba, "por qué For3s vs otros", quick-start `curl|sh`.

**FASE 2 — abrir puertas de entrada:**
5. **GitHub Pages ON** → sitio del agente (indexable por Google).
6. **Discussions ON** → comunidad + soporte público.
7. PRs a **awesome-lists** (awesome-selfhosted, awesome-ai-agents, awesome-claude).

**FASE 3 — generar la SEÑAL (lo que de verdad posiciona):**
8. ⭐ **STARS**: compartir en Frutero, X, Reddit (r/selfhosted, r/LocalLLaMA), HN, Discords de IA.
9. ⚡ **La charla del jueves (AI x Blockchain Day) = el primer empujón real.** Una demo buena → la gente
   va al repo y da star en vivo. Es la mejor oportunidad de arrancar la señal social.
10. (Opcional) mover a una **ORG** (frutero) para más autoridad · **GitHub Sponsors**.

---

## 5. CONCLUSIÓN EN UNA LÍNEA

**No estamos mal configurados — estamos invisibles porque GitHub posiciona por POPULARIDAD (stars/tráfico/
actividad), y ahí tenemos casi cero. La solución NO es "más SEO en el repo" — es GENERAR SEÑAL: stars,
comunidad y puertas de entrada. La charla del jueves es la primera y mejor palanca para arrancarla.**

Cruza con: PENDIENTES §DESCUBRIBILIDAD (SEO/AEO/GEO) · DIST-1/DIST-3 · VALIDACION_WEB3 (la charla).
Memoria: [[project_repo_oficial_for3s]].
