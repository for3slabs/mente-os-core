# 🌐 Plan de implementación — Web for3s.vercel.app para el AGENTE (SEO/AEO/GEO)

> **Pendiente (Brian 2026-07-04):** modificar la landing `for3s.vercel.app` (hoy es de "For3s QA")
> para que represente al AGENTE For3s OS, en INGLÉS, con SEO/AEO/GEO a fondo.
> ⚠️ **Es `marca-personal/` (otro proyecto).** ✅ **Brian AUTORIZÓ tocar marca-personal para ESTE trabajo**
> (2026-07-04, solo la web del agente + SEO). Dominio: se queda for3s.vercel.app por ahora; migrar a
> for3s.com/.ai cuando se compre (Vercel lo apunta sin rehacer). Arquitectura: modo claro=QA, oscuro=OS.

---

## 0. DIAGNÓSTICO DEL TERRENO (verificado, solo lectura)

**Stack:** Next.js (App Router) + React + Microsoft Clarity (analítica ya integrada).
**Estructura:** `app/[locale]/` — ya tiene **i18n con locales `["es", "en"]`** ✅.
**Contenido:** vive en `messages/es.json` + `messages/en.json` (separado del código, fácil de editar) ✅.
**SEO base:** `app/robots.ts` + `app/sitemap.ts` YA existen (Next.js) ✅. Pero **el layout/page NO tiene
metadata** (title/description/OpenGraph) → ese es el hueco #1 de SEO.
**Contenido hoy:** "For3s QA — Convierte contexto desordenado en QA claro" (mensaje de QA, no del agente).

**Lo bueno:** la web ya está preparada (i18n en/es + textos en JSON + robots/sitemap). NO partimos de cero;
es adaptar, no reconstruir.

---

## 1. ⭐ ARQUITECTURA REAL (Brian aclaró — la web YA tiene 2 modos)

**La web YA está diseñada con 2 modos vía ThemeToggle:**
- **Modo CLARO (light) = For3s QA** — el wedge B2B.
- **Modo OSCURO (dark) = For3s OS** — el AGENTE. ⭐ este es el que hay que mejorar.

Cada sección tiene su versión: `HeroDark`/(Light), `SkillsDark`/`SkillsLight`, `TimelineDark`/`TimelineLight`,
`FaqDark`/`FaqLight`, `ProjectsDark`/`ProjectsLight`. El toggle (`ThemeToggle` + `useTheme`, guarda en
localStorage) cambia entre las 2 experiencias completas.

**➡️ Entonces el trabajo NO es crear una página nueva — es MEJORAR el modo oscuro (For3s OS) + su SEO.**

**Estado del modo OS hoy (verificado a fondo):**
- ✅ `HeroDark` existe y es de ALTA CALIDAD (framer-motion, tokens de diseño, badge de versión, headline,
  `InstallBlock` como CTA). Reusable directo.
- ✅ `InstallBlock` (el CTA con el `curl|sh`) existe. Reusable.
- ⚠️ **Solo Hero tiene Dark/Light.** Las demás secciones (Skills, Timeline, Faq, Projects, About) NO tienen
  versión Dark — usan claves `t("os.xxx")` que apuntan al bloque `os` de en.json que está **VACÍO ({})**.
- ✅ Existe ruta `/docs` (stub de 24 líneas) + i18n en/es + robots.ts + sitemap.ts + Clarity.
- Sistema de diseño (tokens, brand colors, componentes) YA existe y es bueno → reusar, no reinventar.

**Conclusión:** el modo OS está PARCIAL (hero excelente, resto del contenido del agente sin escribir). Para
`/for3s-os` reusamos HeroDark + InstallBlock + el sistema de diseño, y construimos las secciones que faltan
(features, why-vs-chatbot, FAQ, comparativa) con contenido en inglés (reusando README/landing Pages/comparativa).

### 🔴 EL PROBLEMA SEO CENTRAL (lo más importante que descubrí)
El modo (claro/oscuro) se elige en el **NAVEGADOR (client-side, localStorage)**. Pero el SEO (metadata,
schema, contenido que Google lee) es **server-side (SSR)** y es **UNO SOLO para toda la página** (la default,
probablemente el modo QA/light). → **Google/ChatGPT ven SOLO la versión QA. El contenido del agente en modo
oscuro NO es indexable.** Aunque el agente exista en la web, para SEO/AEO/GEO es INVISIBLE.

**Esto hay que resolverlo.** Opciones (a decidir en F0):
- **A · Ruta propia del agente** (`/for3s-os` o `/agent`, SSR, siempre modo oscuro) → contenido del agente
  indexable de verdad. **Recomendado** (Google la crawlea como página real).
- **B · Contenido del agente SIEMPRE en el HTML** (ambos modos en el DOM, se muestra/oculta por CSS) →
  Google lo ve. Menos limpio.
- **C · Detectar modo por query param/cookie server-side** → complejo.

➡️ **Recomendación: A** — una ruta `/for3s-os` (o `/agent`) renderizada server-side, siempre en modo oscuro,
en inglés, con TODO el SEO/AEO/GEO. El toggle de la home sigue igual (QA/OS visual); la ruta dedicada es la
que Google/LLMs indexan. Así el agente por fin es descubrible.

---

## 2. QUÉ SE CONSTRUYE (por capa de descubribilidad)

### 🔵 SEO — aparecer en Google
- **Metadata en el layout/page** (Next.js `metadata` export): title + description con keywords
  ("self-hosted AI agent", "AI second brain", "Claude agent", "Hermes alternative").
- **OpenGraph + Twitter card** — para que se vea bien al compartir en X/LinkedIn.
- **Actualizar `app/sitemap.ts`** — incluir la nueva página del agente.
- **`app/robots.ts`** — confirmar que permite crawling + apunta al sitemap.
- **Canonical URLs** por página (Next.js `alternates.canonical`).
- **Contenido real** con H1/H2, keywords naturales, texto sustancioso (Google premia contenido).

### 🟡 AEO — answer box / AI Overview
- **schema.org JSON-LD** en la página del agente: `SoftwareApplication` + `FAQPage` (3-5 Q&A reales:
  "¿qué es?", "¿self-hosted?", "¿vs chatbot?", "¿open source?"). Habilita rich snippets.
- **Sección FAQ visible** (no solo el schema) — la gente Y los buscadores la leen.

### 🟢 GEO — que ChatGPT/Claude recomienden
- **Página comparativa** ("For3s vs X") indexable — los LLMs la leen para recomendar. (Ya tenemos una
  base en `for3slabs.github.io/for3s/vs-hermes.html`; se puede portar/enlazar).
- **Contenido en inglés, claro, factual** — los LLMs citan fuentes bien estructuradas.
- **Enlaces al repo/GitHub** (autoridad cruzada) + a la landing de Pages.

### 📊 Analítica (ya existe)
- Microsoft Clarity YA está → verificar que trackea la página nueva (medir de dónde llega la gente).

---

## 3. FASES (método de fases F — cada una explicar→construir→verificar)

- **F0 · APROBACIÓN** — Brian confirma: alcance (A/B/C) + dominio final (¿for3s.vercel.app se queda o
  migra a for3s.com/for3sos.com/for3s.ai cuando se compre?) + tono. ⚠️ hasta aquí solo lectura.
- **F1 · CONTENIDO EN INGLÉS ✅ COMPLETO (2026-07-04).** Bloque `For3sOS` añadido a `messages/en.json` +
  `es.json` (aditivo, en inglés): meta (title/description SEO), badge (v0.15.0/Living Identity), hero,
  why-vs-chatbot, 6 features, install, 4 FAQ (para el schema AEO), compare, footer. Reusa README/landing/
  comparativa. Verificado: bloques viejos 100% intactos (20→21), JSON válido en Node/Next. NO rompe la home.
- **F2 · LA RUTA `/for3s-os` ✅ COMPLETO (2026-07-04).** Página SSR `app/[locale]/for3s-os/page.tsx`,
  autocontenida, modo oscuro forzado (`className="dark"`), lee del bloque For3sOS. Secciones: hero (badge
  v0.15.0 + CTAs) + why-vs-chatbot + 6 features (con iconos lucide) + install + FAQ (`<details>`) + compare
  (link a vs-hermes) + footer. Reusa el patrón de la home + tokens de diseño existentes. **Incluye ya el SEO
  (F3): metadata export (title/desc/canonical/OG/twitter) + JSON-LD SoftwareApplication + FAQPage.**
  Verificado: `tsc` sin errores + `npm run build` OK → genera `/en/for3s-os` y `/es/for3s-os` como páginas
  ESTÁTICAS (SSG, indexables). El HTML server-side CONTIENE el contenido ("self-hosted AI agent" ×27,
  "knowledge graph" ×36) + el schema (SoftwareApplication + FAQPage) → Google/LLMs SÍ lo ven. Cambios
  acotados: solo messages/*.json + la ruta nueva. La home y el modo oscuro actual intactos.
- **F3 · SEO técnico ✅ (hecho junto con F2)** — metadata export + JSON-LD SoftwareApplication + FAQPage
  en la ruta /for3s-os.
- **F4 · SITEMAP + ENLACE + GEO ✅ COMPLETO (2026-07-04).** (1) `app/sitemap.ts`: añadida entrada /for3s-os
  (priority 0.95, con alternates i18n) → Google la descubre. (2) `Navbar.tsx`: link "For3s OS" → /for3s-os
  en el modo oscuro (darkLinkKeys) + labels en en/es.json → enlace interno desde toda la web. (3) GEO: la
  ruta enlaza a la comparativa vs-hermes. Verificado: tsc sin errores + `npm run build` OK + sitemap.xml
  generado CONTIENE /for3s-os (×3: home+en+alternates). Cambios acotados: sitemap.ts + Navbar.tsx +
  messages + ruta. Home/modo-oscuro actual intactos.
- **F5 · DESPLEGAR + VERIFICAR EN VIVO ✅ COMPLETO (2026-07-04).** Deploy = push a `ElBrAyAn1967/For3s`
  (rama main) → Vercel auto-despliega. Build limpio antes del push (180 páginas). Commit 5934a78 pusheado.
  **VERIFICADO EN VIVO:** `for3s.vercel.app/for3s-os` y `/en/for3s-os` → HTTP 200. El HTML en producción
  CONTIENE el contenido ("self-hosted AI agent" ×27, "knowledge graph" ×36) + el schema (SoftwareApplication
  + FAQPage) + title/meta correctos → Google/LLMs SÍ lo ven. Cambios acotados, home/modo-oscuro intactos.

---

## ✅✅ HITO WEB DEL AGENTE — 100% COMPLETO (2026-07-04)
La landing del AGENTE For3s OS ya existe, en inglés, indexable, EN VIVO en `for3s.vercel.app/for3s-os`. Tapa
el hueco #1 de descubribilidad: antes el agente estaba en un modo oscuro client-side que Google no veía; ahora
es una página server-side con SEO (metadata/canonical/OG) + AEO (schema SoftwareApplication + FAQPage) + GEO
(comparativa vs Hermes enlazada), en el sitemap y enlazada desde el navbar. 5 fases F1-F5, cada una verificada.
NO tocó la home de QA ni el modo oscuro actual (aditivo). Falta (Brian): que Google indexe (tiempo) + señal
(charla/stars) + opcional migrar a for3s.com/.ai. Memoria: la web del agente ya es descubrible.

---

## 4. PRINCIPIOS (respetar reglas del proyecto)
- ⚠️ **marca-personal es otro proyecto** — NO tocar hasta aprobación explícita de Brian (regla CLAUDE.md).
- **En inglés** (audiencia dev global) — reusar el i18n `en` que ya existe.
- **No romper lo de QA** (opción B recomendada: sumar, no destruir).
- **Reusar lo ya escrito** — README, landing Pages, comparativa vs-hermes (no reinventar el copy).
- Verificar con herramientas reales (Rich Results Test, Lighthouse) antes de dar por bueno.

---

## 5. LO QUE BRIAN DEBE DECIDIR (para arrancar F0)
1. **Alcance:** ¿A (pivotar), B (página aparte, recomendado), o C (por idioma)?
2. **Dominio:** ¿se queda for3s.vercel.app o se planea migrar a for3s.com/.ai cuando se compre?
3. **¿Se puede tocar marca-personal ya?** (confirmación explícita para levantar la regla de "no tocar").

Relacionado: `Analisis_GitHub_Descubribilidad_2026-07-04.md` · `Comparacion_For3s_OS_vs_Hermes_2026-07-04.md` ·
la landing de Pages (`for3slabs.github.io/for3s/`) · PENDIENTES §DESCUBRIBILIDAD.
