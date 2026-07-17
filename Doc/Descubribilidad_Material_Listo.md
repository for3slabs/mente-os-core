# 📢 Material LISTO para descubribilidad (copy-paste) — For3s OS

> Todo en INGLÉS (audiencia dev global). Lo que Brian tiene que hacer a mano (PRs a listas externas,
> posts en redes) — ya escrito para copiar y pegar. Actualizado 2026-07-04.

---

## 1. AWESOME-LISTS — dónde meter For3s (PRs a repos externos)

Los "awesome-lists" son puertas de entrada: dev las leen para descubrir herramientas, y los LLMs las
indexan (ayuda a GEO). Hacer un PR a cada una añadiendo For3s.

**Listas objetivo (por prioridad):**
1. `e2b-dev/awesome-ai-agents` — la más relevante (agentes de IA).
2. `kyrolabs/awesome-agents` — agentes.
3. `Shubhamsaboo/awesome-llm-apps` — apps LLM.
4. `awesome-selfhosted/awesome-selfhosted` — self-hosted (sección Automation/AI).
5. `hesreallyhim/awesome-claude-code` u otras "awesome-claude" — construido sobre Claude.
6. `punkpeye/awesome-mcp-servers` si aplica (usa MCP).

**Entrada para copiar (formato estándar de awesome-lists):**
```
[For3s OS](https://github.com/fruterito101/for3s) - Self-hosted AI agent / second brain built on Claude: semantic memory + knowledge graph (Apache AGE + pgvector), a living identity that adapts to you, multi-agent team, self-modification, and enterprise-grade trust. AGPL-3.0. `Python`
```

**Cómo:** fork de la lista → añadir la línea en la sección correcta (orden alfabético si lo piden) →
PR con título claro ("Add For3s OS"). Revisa el CONTRIBUTING de cada lista (algunas exigen ≥N stars —
esas déjalas para cuando tengas más).

---

## 2. POST DE LANZAMIENTO (para X / LinkedIn / Reddit)

**Versión corta (X/Twitter):**
```
Most "AI agents" are a chatbot with extra steps.

For3s OS goes deep 🧠
· real memory: semantic + a knowledge graph
· an identity that adapts to YOU (on its own)
· runs code, reads/writes GitHub
· edits its own code (safely)
· immutable audit, offline keys

Self-hosted. Your data, your server.
Open source (AGPL): github.com/fruterito101/for3s
```

**Versión Reddit (r/selfhosted, r/LocalLLaMA) — título:**
```
For3s OS — a self-hosted AI agent with real memory (knowledge graph), an identity that adapts to you, and self-modification. Open source.
```
**Cuerpo:** explica el "why" (no es un chatbot), lista features, el `curl|sh`, y pide feedback honesto
(a Reddit le gusta que preguntes, no que vendas). Enlaza el repo + la landing.

---

## 3. TEXTOS BREVES REUTILIZABLES

**Tagline (1 línea):**
`A self-hosted AI agent that remembers, learns, works in a team, and improves itself — your data, your server.`

**Pitch (2 líneas):**
`For3s OS is a second brain built on Claude — not a stateless chatbot. Real semantic memory + a knowledge graph, a living identity that adapts to you, multi-agent teamwork, self-modification, and enterprise-grade trust. Self-hosted, open source (AGPL-3.0).`

**El diferenciador vs otros (para comparaciones):**
`Where most agents are broad (many channels, many tools), For3s goes deep: a real knowledge graph + biological-style forgetting, a layered identity that adapts to you with a blinded core, self-modification of its own code, and verifiable trust (immutable audit, offline KEK, signed releases + SBOM).`

---

## 4. LINKS OFICIALES (para pegar donde haga falta)
- **Repo:** https://github.com/fruterito101/for3s
- **Landing (GitHub Pages):** https://fruterito101.github.io/for3s/
- **Perfil:** https://github.com/fruterito101
- **Release actual:** v0.15.0 "Identidad Viva"
- **Install:** `curl -fsSL https://install.for3s.dev | sh`

---

## 5. CHECKLIST de descubribilidad (marcar al hacer)
- [x] Perfil README · [x] Release v0.15.0 · [x] README top-tier · [x] GitHub Pages · [x] Discussions
- [ ] Grabar GIF de demo → meterlo en README + landing
- [ ] PRs a awesome-lists (§1)
- [ ] Post de lanzamiento (§2) — idealmente el día de la charla o justo después (aprovechar el momento)
- [ ] Web for3s.vercel.app reescrita para el agente (en inglés + SEO/schema)
- [ ] Primeras stars (charla + comunidades Frutero)

---

## 6. CREAR LA ORG DE FOR3S (acción de Brian — GitHub no deja por API)
**Nombres LIBRES** (verificado 2026-07-04): `for3s-os` ⭐ (recomendado), for3sos, for3s-ai, for3slabs.
(`for3s` está ocupado.) **fruteroclub** existe pero Brian quiere org PROPIA de For3s.
- **Crear:** github.com/organizations/plan → plan **Free** → nombre `for3s-os`.
- **Mover el repo:** `fruterito101/for3s` → Settings → "Transfer ownership" → org `for3s-os`.
  GitHub **redirige la URL vieja automáticamente** (no rompe links).
- **Después:** avisar → yo re-apunto perfil README, landing de Pages, badges, homepage a la nueva URL.
- **Timing:** mejor YA (hay margen antes del evento) que con prisa el día de la charla.

## 7. GITHUB SPONSORS (acción de Brian — requiere config de pagos)
- github.com/sponsors → "Join the waitlist / Set up" → onboarding con Stripe (cuenta bancaria).
- Da el botón "Sponsor" + `is:sponsorable` (qualifier de búsqueda de la doc de GitHub).
- No urgente; hazlo cuando quieras monetizar/recibir apoyo.

---

Relacionado: `Analisis_GitHub_Descubribilidad_2026-07-04.md` · PENDIENTES §DESCUBRIBILIDAD.
