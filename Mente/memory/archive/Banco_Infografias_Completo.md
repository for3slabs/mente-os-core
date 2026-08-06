# Banco Completo de Infografías — Punto de Partida For3s

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Registro exhaustivo de las 81+ infografías compartidas por Brian López en sesión de captura (lotes 1-11)**

**Owner:** Brian López
**Fecha de captura:** 2026-05-28 al 2026-05-30
**Estatus:** Documento de referencia histórica. Banco crudo de inputs.
**Capa:** Doc — transversal (cruza Alma + Cerebro + Cuerpo)
**Propósito:** Preservar a profundidad TODAS las infografías que Brian compartió como contexto para construir For3s OS. Es la "biblioteca de inputs" del proyecto, no la verdad absoluta del stack.

**Documentos hermanos:**
- [Banco_Diario_Mayo_2026.md](Banco_Diario_Mayo_2026.md) — los 3 docs de borrador histórico de Brian
- [Banco_Filtro_Alineacion.md](Banco_Filtro_Alineacion.md) — qué se queda y qué se va contra el Grafo Maestro

**Documento ancla (filtro de verdad):**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md)

---

## Cómo está organizado este documento

El banco tiene **81+ infografías** distribuidas en **11 lotes** que Brian compartió secuencialmente. Las organizo en **22 buckets temáticos** finales. Cada infografía tiene:

- Número (#1, #2, ...)
- Título exacto
- Fuente (naiker.codes, techwith.ram, otros)
- Bucket temático asignado
- Resumen denso de contenido
- Tecnologías/herramientas mencionadas explícitamente
- Relevancia preliminar para For3s OS (no es decisión final — eso vive en `Banco_Filtro_Alineacion.md`)

---

## Tabla de contenidos

1. [Resumen ejecutivo del banco](#1-resumen-ejecutivo-del-banco)
2. [Los 22 buckets temáticos finales](#2-los-22-buckets-temáticos-finales)
3. [Bucket A — Fundamentos Web / API REST](#3-bucket-a--fundamentos-web--api-rest)
4. [Bucket B — Concurrencia / Performance / Memoria](#4-bucket-b--concurrencia--performance--memoria)
5. [Bucket C — Frontend / Rendering](#5-bucket-c--frontend--rendering)
6. [Bucket D — Teoría Matemática / ML / Algoritmos](#6-bucket-d--teoría-matemática--ml--algoritmos)
7. [Bucket E — Bases de Datos y Patrones de Datos](#7-bucket-e--bases-de-datos-y-patrones-de-datos)
8. [Bucket F — APIs / Backend Best Practices](#8-bucket-f--apis--backend-best-practices)
9. [Bucket G — Ingeniería Software / Calidad / Arquitectura](#9-bucket-g--ingeniería-software--calidad--arquitectura)
10. [Bucket H — Fundamentos de Cómputo](#10-bucket-h--fundamentos-de-cómputo)
11. [Bucket I — Seguridad / Auth / Secrets / Criptografía](#11-bucket-i--seguridad--auth--secrets--criptografía)
12. [Bucket J — AI-Native Development / Claude / MCP](#12-bucket-j--ai-native-development--claude--mcp)
13. [Bucket K — Estructuras de Datos y Algoritmos](#13-bucket-k--estructuras-de-datos-y-algoritmos)
14. [Bucket L — IA / Panorama / Taxonomía / Agents / RAG](#14-bucket-l--ia--panorama--taxonomía--agents--rag)
15. [Bucket M — Arquitectura de Sistemas](#15-bucket-m--arquitectura-de-sistemas)
16. [Bucket N — Infraestructura AI](#16-bucket-n--infraestructura-ai)
17. [Bucket O — Paradigmas de Programación](#17-bucket-o--paradigmas-de-programación)
18. [Bucket P — Streaming / Event-Driven](#18-bucket-p--streaming--event-driven)
19. [Bucket Q — Cloud / Deployment / Serverless](#19-bucket-q--cloud--deployment--serverless)
20. [Bucket R — Edge / Distributed Computing](#20-bucket-r--edge--distributed-computing)
21. [Bucket S — Observability](#21-bucket-s--observability)
22. [Bucket T — Workflow Automation Real](#22-bucket-t--workflow-automation-real)
23. [Bucket U — Procesamiento de Datos Masivos](#23-bucket-u--procesamiento-de-datos-masivos)
24. [Bucket V — Estrategia de Negocio y Moat](#24-bucket-v--estrategia-de-negocio-y-moat)
25. [Bucket Ruido / Contexto](#25-bucket-ruido--contexto)
26. [Patrones macro emergentes del banco](#26-patrones-macro-emergentes-del-banco)

---

## 1. Resumen ejecutivo del banco

```
   ╔══════════════════════════════════════════════════════════╗
   ║         BANCO COMPLETO DE INFOGRAFÍAS — FOR3S             ║
   ╠══════════════════════════════════════════════════════════╣
   ║                                                          ║
   ║  Total infografías:        81+                            ║
   ║  Lotes compartidos:        11                             ║
   ║  Fuentes principales:                                    ║
   ║    • naiker.codes         (~55 infografías)              ║
   ║    • techwith.ram         (5 — serie Gaussian Process)   ║
   ║    • Charlie Hills        (1 — Claude 31 skills SMB)     ║
   ║    • Lost in the Woods    (1 — Local vs Cloud AI)        ║
   ║    • LuMay AI             (1 — 9 AI Skills 2026)         ║
   ║    • McKinsey & Company   (1 — Agentic Orchestration)    ║
   ║    • Data Science 4 Biz   (1 — RegLog/XGBoost/NN)        ║
   ║    • ai._kid (Instagram)  (1 — ChatGPT→Claude)           ║
   ║    • foroblockchain       (1 — Moat flywheel)            ║
   ║    • Anthropic/Claude     (varias — Cowork, /goal)       ║
   ║    • godofprompt          (1 — /goal cheat sheet)        ║
   ║    • Anthropic AI Master  (1 — AI Infra Master Tree)     ║
   ║    • Nainsi Dwivedi       (1 — Hermes complete guide)    ║
   ║                                                          ║
   ║  Buckets temáticos:        22 + ruido                    ║
   ║                                                          ║
   ║  Estado: BANCO CERRADO, listo para filtro de alineación  ║
   ║                                                          ║
   ╚══════════════════════════════════════════════════════════╝
```

**Observación crítica de fuentes:** El banco está fuertemente sesgado hacia el creador **naiker.codes** (~68% del contenido). Esto NO es un defecto — es señal de que Brian consume sistemáticamente contenido de este creador específico, lo que implica un **sesgo técnico consistente** del banco:

- Estilo chalkboard (pizarra) con 5 pasos + 8-9 secciones por infografía
- Stack moderno orientado a **JavaScript/TypeScript + Node.js + PostgreSQL**
- Fuerte presencia de patrones de arquitectura clásicos (Clean, DRY, SOLID implícito)
- Énfasis en **seguridad operacional** (cookies HttpOnly, env vars, secret managers, HTTPS everywhere)
- Cobertura completa del ecosistema **AI-native moderno** (MCP, Claude Code, agentes, RAG)

---

## 2. Los 22 buckets temáticos finales

Después de 11 lotes de análisis, las infografías se organizan así:

| Bucket | Tema | # infografías | Densidad estratégica |
|---|---|---|---|
| A | Fundamentos Web / API REST | 7 | Alta (base operativa) |
| B | Concurrencia / Performance / Memoria | 5 | Media (relevante para escalabilidad) |
| C | Frontend / Rendering | 5 | Media (UI del dashboard) |
| D | Teoría Matemática / ML / Algoritmos | 9 | Baja-Media (mayormente contexto) |
| E | Bases de Datos y Patrones de Datos | 7 | **MUY ALTA** (data layer) |
| F | APIs / Backend Best Practices | 6 | Alta |
| G | Ingeniería SW / Calidad / Arquitectura | 5 | **MUY ALTA** (Clean Arch, DRY, DI) |
| H | Fundamentos de Cómputo | 2 | Baja (contexto) |
| I | Seguridad / Auth / Secrets / Criptografía | 6 | **MUY ALTA** (pilar 1 For3s) |
| J | AI-Native Development / Claude / MCP | 7 | **MUY ALTA** (stack agentic) |
| K | Estructuras de Datos y Algoritmos | 2 | Baja |
| L | IA / Panorama / Agents / RAG | 8 | **MUY ALTA** (taxonomía) |
| M | Arquitectura de Sistemas | 3 | **MUY ALTA** (mono vs micro, McKinsey) |
| N | Infraestructura AI | 3 | **MUY ALTA** (Master Tree, Hermes) |
| O | Paradigmas de Programación | 1 | Media (reactiva) |
| P | Streaming / Event-Driven | 2 | Alta (Event Sourcing crítico) |
| Q | Cloud / Deployment / Serverless | 1 | Alta (Q1 Lambda+GCP+Azure+Cloudflare) |
| R | Edge / Distributed Computing | 1 | Baja-Media |
| S | Observability | 1 | **MUY ALTA** (pilar operativo) |
| T | Workflow Automation Real | 1 | Alta (n8n caso real) |
| U | Procesamiento Datos Masivos | 1 | Media (Polars si Python) |
| V | Estrategia Negocio y Moat | 1 | **MÁXIMA** (flywheel) |
| Ruido | Contexto Facebook/repeticiones | 4 | N/A |

---

## 3. Bucket A — Fundamentos Web / API REST

**7 infografías. Densidad estratégica: ALTA.**

### A1 — Tema 4: Códigos HTTP — ¿Qué significan? (#1)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 1

**Contenido:**
- 5 categorías HTTP: 1xx informativos, 2xx éxito, 3xx redirección, 4xx error cliente, 5xx error servidor
- Códigos más usados: 200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503
- 6 ejemplos prácticos GET/POST con códigos de respuesta
- Cómo leer códigos rápidamente: "2xx todo bien, 3xx sigue camino, 4xx error tuyo, 5xx error servidor"
- Consejos: revisar código antes que mensaje, no todos los errores son 4xx/5xx (hay excepciones), devolver código correcto en APIs

**Tecnologías:** HTTP/1.1

### A2 — Tema 2: Métodos HTTP — ¿Para qué sirven? (#2)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 1

**Contenido:**
- 6 métodos principales: GET (obtener), POST (crear), PUT (actualizar completo), PATCH (actualizar parcial), DELETE (eliminar), HEAD (solo headers)
- Analogía restaurante: GET=ver menú, POST=hacer pedido, PUT=cambiar pedido, DELETE=cancelar
- Relación CRUD: CREATE=POST, READ=GET, UPDATE=PUT/PATCH, DELETE=DELETE
- Regla de oro: "Usar el método correcto hace tu API más clara, segura y fácil de mantener"
- Diagrama cliente↔servidor con flechas direccionales

**Tecnologías:** HTTP, JSON, APIs REST

### A3 — Tema 3: CRUD Completo — Las 4 operaciones básicas (#3)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 1

**Contenido:**
- CRUD = Create, Read, Update, Delete
- Tabla completa: operación + método HTTP + qué hace + ejemplo URL + ejemplo body JSON
- Flujo: Cliente → Servidor → Base de Datos (con flechas bidireccionales)
- 6 ejemplos rápidos: POST /usuarios, GET /usuarios, GET /usuarios/1, PUT /usuarios/1, PATCH /usuarios/1, DELETE /usuarios/1
- "Es la base de casi todas las funcionalidades"
- "Es la base de todas las APIs REST"

**Tecnologías:** HTTP, JSON, REST

### A4 — ¿Qué es un Endpoint? (#4)

**Fuente:** naiker.codes
**Lote:** 1

**Contenido:**
- Endpoint = URL específica que permite acceder a funciones/datos de una API
- "La puerta de entrada a un servicio web"
- Flujo: Cliente envía request → /api → Endpoint recibe petición → Servidor procesa datos → Devuelve respuesta
- 5 métodos comunes: GET, POST, PUT, DELETE
- Uso real: apps móviles, frontend web, microservicios, APIs REST
- Analogía edificio con puertas numeradas (101=info usuarios, 102=crear pedido, 103=listar productos, 104=eliminar registro)
- **Fórmula:** Endpoint = URL + API + Comunicación

**Tecnologías:** HTTP, REST

### A5 — Tema 1: ¿Qué es una API REST? (#13)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 2

**Contenido:**
- API REST = Representational State Transfer, comunicación HTTP entre apps
- 6 características REST: basado en HTTP, **sin estado (stateless)**, usa recursos (URLs), respuestas en formato estándar (JSON/XML), fácil, **escalable y flexible**
- Ejemplo: `GET /api/usuarios/1` → respuesta JSON con id/nombre/email
- Cliente puede ser navegador, app, mobile
- "Es la base de Google, Facebook, Twitter, GitHub"

**Tecnologías:** HTTP, JSON, XML, REST

### A6 — PATCH vs PUT — ¿Cuál usar? (#20)

**Fuente:** naiker.codes
**Lote:** 3

**Contenido:**
- **PATCH:** actualiza parcialmente, solo envía campos que cambiaron, idempotencia no garantizada
- **PUT:** reemplaza completamente, envía todos los campos, idempotencia sí
- Tabla comparativa: alcance (parcial vs total), datos enviados (solo cambios vs todos), efecto (modifica parte vs reemplaza completo), idempotencia (no vs sí)
- Ejemplos código de cada uno
- **Advertencia crítica:** "NO SON INTERCAMBIABLES. Usa el método correcto para evitar errores y pérdida de datos"

**Tecnologías:** HTTP, REST, JSON

### A7 — REST API Methods con código real (#56, repetido en #87)

**Fuente:** No identificado (estilo card moderna oscura)
**Lote:** 7 (y repetido en lote 11)

**Contenido:**
- 5 core REST methods con código JavaScript fetch() real
- GET https://jsonplaceholder.typicode.com/users → response.json()
- POST con headers Content-Type application/json + body JSON.stringify
- PUT con method "PUT" y body completo
- PATCH con method "PATCH" y body parcial
- DELETE con method "DELETE"
- Quick Reference Table: método + action + ejemplo
- Common Routes Example: GET/POST /users, PUT/PATCH/DELETE /users/1
- HTTP Status Codes: 200, 201, 400, 401, 404, 500
- Pro Tip: "Use the right method for the right action to keep your API clean, efficient, and easy to maintain"

**Tecnologías:** JavaScript, fetch API, jsonplaceholder.typicode.com, HTTP

**Observación:** Esta infografía aparece **2 veces** en el banco. Señal fuerte de fundacionalidad.

---

## 4. Bucket B — Concurrencia / Performance / Memoria

**5 infografías. Densidad estratégica: MEDIA.**

### B1 — ¿Qué es un Hilo (Thread)? (#5)

**Fuente:** naiker.codes
**Lote:** 1

**Contenido:**
- Hilo = unidad de ejecución que permite múltiples tareas dentro de un programa
- Diferencia sin hilos (secuencial) vs con hilos (paralelo)
- Cómo funciona: programa inicia → se crean hilos → tareas simultáneas → resultados se combinan
- Ventajas: apps más rápidas, mejor rendimiento, menos bloqueos, experiencia fluida
- Problemas comunes: **race conditions, deadlocks, sincronización, consumo CPU**
- Analogía chef cocinando varios platos
- Arquitectura: aplicación → Thread Manager → CPU núcleos → tareas ejecución
- **Fórmula:** Threads = Multitarea + Velocidad + Concurrencia

**Tecnologías:** Sistemas operativos, programación concurrente

### B2 — Heap vs Stack — Gestión de memoria (#14)

**Fuente:** naiker.codes
**Lote:** 2

**Contenido:**
- **Stack:** memoria rápida, variables temporales, llamadas de funciones, LIFO, tamaño limitado
- **Heap:** memoria dinámica, objetos creados en runtime, más flexible, objetos grandes
- Stack: función inicia → variables → stack organiza → función termina
- Heap: objeto se crea → Heap reserva memoria → programa usa → Garbage Collector limpia
- Ejemplos: `int x = 5` → Stack | `new Usuario()` → Heap
- Uso real: **Java, C#**, aplicaciones grandes, videojuegos
- Analogía: Stack = mesa de trabajo temporal | Heap = almacén gigante
- Sesgo del autor: "Muy importante en Java"

**Tecnologías:** Java, C#, JavaScript, gestión de memoria

### B3 — Debouncing — técnica de performance (#16)

**Fuente:** naiker.codes
**Lote:** 2

**Contenido:**
- Debouncing = retrasa ejecución de función hasta que usuario deja de hacer algo
- Optimiza búsquedas, mejora rendimiento, **reduce peticiones API**, evita ejecuciones innecesarias
- Cómo funciona 4 pasos: usuario escribe → función espera ms → si sigue interactuando se reinicia tiempo → solo ejecuta al detenerse
- Dónde se usa: inputs de búsqueda, resize ventana, scroll, autocomplete
- **Código JavaScript ejemplo:**
  ```javascript
  let timeout;
  input.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      console.log("Buscar...");
    }, 500);
  });
  ```
- Sin debounce: ejecuta en cada tecla, llamada a API por cada letra
- Con debounce: ejecuta solo al detenerse, una sola llamada

**Tecnologías:** JavaScript, performance patterns

### B4 — Memoization (#18)

**Fuente:** naiker.codes
**Lote:** 3

**Contenido:**
- Memoization = técnica que guarda resultados de funciones para no recalcularlos
- "Más velocidad y menos procesamiento"
- 3 pasos: función calcula una vez → guarda en cache → si recibe mismos datos reutiliza
- Dónde se usa: **React (useMemo)**, cálculos complejos, filtros grandes, APIs y cache
- **Código JS ejemplo (manual):**
  ```javascript
  const cache = {};
  function sum(num) {
    if (cache[num]) return cache[num];
    cache[num] = num + 10;
    return cache[num];
  }
  ```
- **Código React useMemo:**
  ```javascript
  import { useMemo } from "react";
  const result = useMemo(() => heavyCalculation(data), [data]);
  ```
- Tips: usar useMemo en React, NO memorizar todo (solo costoso), ideal para filtros/búsquedas/transformaciones, combinar con cache

**Tecnologías:** JavaScript, React, useMemo, caching

### B5 — Garbage Collector (#25)

**Fuente:** naiker.codes
**Lote:** 4

**Contenido:**
- GC = sistema que libera automáticamente memoria de objetos no usados
- 4 pasos: objetos se crean → programa deja de usarlos → GC detecta basura → memoria se libera
- **Lenguajes mencionados explícitamente con GC:** Java, Python, C#, JavaScript
- Ventajas: menos errores, memoria optimizada, mayor estabilidad, desarrollo fácil
- **Problemas posibles:** pausas de rendimiento, uso excesivo de memoria, objetos retenidos, leaks indirectos
- Analogía: robot que limpia automáticamente cosas viejas
- "GC = Memoria + Limpieza + Optimización"
- **Detalle crítico:** menciona Java/Python/C#/JS pero NO Rust (sin GC, ownership) ni Go (tiene GC pero perfil distinto)

**Tecnologías:** Java, Python, C#, JavaScript

---

## 5. Bucket C — Frontend / Rendering

**5 infografías. Densidad estratégica: MEDIA.**

### C1 — Frontend Responsive (#15)

**Fuente:** naiker.codes
**Lote:** 2

**Contenido:**
- Técnica de diseño web que adapta interfaces a móviles, tablets, computadoras
- 4 técnicas: **Media Queries, Flexbox, CSS Grid, Unidades flexibles** (em/rem/%/vw/vh)
- Flujo: usuario abre web → pantalla detectada → CSS responsive actúa → layout se adapta
- Ventajas: mejor UX, accesibilidad, optimización móvil
- Analogía: agua que cambia de forma según el recipiente
- "Responsive = Flexibilidad + UX + Adaptación"

**Tecnologías:** CSS, HTML

### C2 — Virtual DOM (#17)

**Fuente:** naiker.codes
**Lote:** 3

**Contenido:**
- Virtual DOM = copia virtual del DOM real que React usa
- Optimiza cambios en pantalla
- 4 pasos: React crea copia virtual → detecta cambios entre versiones → compara diferencias (**diffing algorithm**) → actualiza solo lo que cambió
- Nodos: nuevo, eliminado, modificado
- **Dónde se utiliza:** React, **React Native**, librerías modernas UI
- Tips pro: usar keys correctamente, evitar renders innecesarios (React.memo, useMemo, useCallback), memorizar componentes pesados, mantener componentes pequeños
- "Virtual DOM = render optimizado + mejor rendimiento"

**Tecnologías:** React, React Native, JavaScript

### C3 — CSR (Client Side Rendering) (#32)

**Fuente:** naiker.codes
**Lote:** 4

**Contenido:**
- CSR = navegador renderiza la app usando JavaScript
- Crear apps dinámicas, mejorar interacción, **reducir carga del servidor**, manejar SPAs
- 4 pasos: navegador recibe HTML básico → descarga JavaScript → **React/Vue renderiza** → interfaz aparece dinámicamente
- **Dónde se utiliza:** React, **Vue**, SPAs modernas, Dashboards
- Características: render en navegador, alta interactividad, menos carga servidor, navegación rápida
- **Desventajas críticas:**
  - SEO más complejo (contenido carga con JS, no en HTML inicial)
  - Carga inicial más lenta
  - **Dependencia de JavaScript (si JS falla, app puede no funcionar)**
- Tips pro: **código dividido (Code Splitting)**, **optimiza el bundle**, **prefetch de rutas**, **cuida SEO (usa SSR o SSG)**

**Tecnologías:** React, Vue, JavaScript, SPAs, Code Splitting, SSR, SSG

### C4 — Local Storage (#33)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 4

**Contenido:**
- Local Storage = API HTML5 para guardar datos clave-valor en navegador con persistencia
- 5 operaciones básicas con código JS: setItem, getItem, removeItem, clear
- **Tabla comparativa Local Storage vs Cookies:**
  - Tamaño: 5-10MB vs 4KB
  - Envío al servidor: NO vs Sí (cada petición HTTP)
  - Persistencia: hasta eliminación manual vs fecha expiración
  - Accesibilidad: JavaScript vs automática
  - Uso típico: datos no sensibles/preferencias vs sesiones/auth
- Datos por origen (dominio y protocolo), cada sitio tiene espacio independiente
- Cuándo usar: preferencias usuario, datos formularios, sesiones persistentes, carritos, configs
- Solo strings, pero puedes guardar JSON con JSON.stringify/parse
- **Consideraciones críticas:**
  - NO guardes datos sensibles
  - Usuarios pueden limpiar storage
  - NO compatible modo incógnito permanente
  - "Úsalo para mejorar, no para guardar información crítica"

**Tecnologías:** HTML5, JavaScript, Web Storage API

### C5 — Blazor — C# para frontend (#78)

**Fuente:** naiker.codes
**Lote:** 10

**Contenido:**
- Blazor = framework .NET para apps web interactivas usando **C# en lugar de JavaScript**
- Permite frontends que se ejecutan en navegador con **WebAssembly** o servidor
- 7 características: Solo C#, WebAssembly, Interactividad, Reutilizable, Componentes (Razor), Seguro, Multiplataforma
- 2 modos de renderizado:
  - **Blazor WebAssembly (CLIENTE):** ejecuta completamente en navegador, usa WebAssembly, ideal SPAs/PWAs, mayor carga inicial
  - **Blazor Server (SERVIDOR):** ejecuta en servidor, UI se actualiza por **SignalR** en tiempo real, menor carga inicial, requiere conexión, ideal intranets
- Ejemplos código Razor (Counter.razor con @page, @code)
- Herramientas: Visual Studio, VS Code, dotnet CLI, Hot Reload
- Integración .NET completa: ASP.NET Core, Entity Framework Core, Identity, gRPC, SignalR
- Ejecución: navegadores modernos, Cloud (Azure, AWS), Cross-platform (Web, PWA, Desktop)
- "Un solo lenguaje, infinitas posibilidades. C# en todo el stack"

**Tecnologías:** .NET, C#, WebAssembly, Razor, ASP.NET Core, SignalR, Entity Framework

---

## 6. Bucket D — Teoría Matemática / ML / Algoritmos

**9 infografías. Densidad estratégica: BAJA-MEDIA.**

### D1-D6 — Serie completa Neural Network as Gaussian Process (techwith.ram)

**6 slides de serie matemática profunda.** Lotes 1 y 2.

**D1 — Slide 01: Introduction (#8)** — "Did you know that a neural network with infinite width behaves like a Gaussian Process (GP)?"

**D2 — Slide 02: The Big Idea (#7)** — "A neural network with infinitely many hidden units induces a distribution over functions. Instead of learning a single function, the network represents a distribution over all possible functions. Infinite-width neural networks ≈ Gaussian Processes over functions"

**D3 — Slide 03: Key Intuition (#9)** — Por Teorema del Límite Central, output de red se vuelve Gaussiano en cada input cuando ancho tiende a infinito. Finite width = complex/non-Gaussian, Infinite width = Gaussian distribution.

**D4 — Slide 04: From Network to GP (#10)** — Una NN infinitamente ancha con pesos aleatorios induce un GP. 3 pasos: pick inputs X → network outputs joint Gaussian → completely described by mean & kernel. f(x) ~ GP(m(x), k(x,x')). m(x) = mean function, k(x,x') = covariance (kernel). Bridge: deep learning ↔ Bayesian non-parametrics.

**D5 — Slide 05: What This Means in Practice (#11)** — 4 beneficios prácticos: Uncertainty Quantification, Better Generalization (anti-overfit), Data Efficiency (con datasets pequeños), Theoretical Insights (marco probabilístico). f(·) ~ GP(m(·), k(·,·)).

**D6 — A Neural Network as a Gaussian Process (#12)** — Slide final con CÓDIGO PYTHON ejecutable:
```python
import torch
import gpytorch
from gpytorch.kernels import RBFKernel

X = torch.linspace(-3, 3, 100).unsqueeze(-1)
kernel = RBFKernel()
K = kernel(X)
```
Key takeaway: "Una NN infinitamente ancha es un GP con kernel determinado por su arquitectura."

**Tecnologías:** PyTorch, GPyTorch, matemática Bayesiana

### D7 — Neural Networks chart de Fjodor van Veen 2016 (#40)

**Fuente:** asimovinstitute.org / Medium
**Lote:** 5

**Contenido:**
- "A mostly complete chart of Neural Networks"
- Leyenda células: Backfed Input, Input, Noisy Input, Hidden, Probabilistic Hidden, Spiking Hidden, Output, Match Input Output, Recurrent, Memory, Different Memory, Kernel, Convolution or Pool
- **27 arquitecturas catalogadas:**
  - Perceptron (P), Feed Forward (FF), Radial Basis Network (RBF), Deep Feed Forward (DFF)
  - RNN, **LSTM**, Gated Recurrent Unit (GRU)
  - **Auto Encoder (AE)**, Variational AE (VAE), Denoising AE (DAE), Sparse AE (SAE)
  - Markov Chain (MC), Hopfield, Boltzmann Machine (BM), Restricted BM (RBM), Deep Belief Network (DBN)
  - Deep Convolutional Network (DCN), Deconvolutional, Deep Convolutional Inverse Graphics Network (DCIGN)
  - **GAN**, Liquid State Machine (LSM), Extreme Learning Machine (ELM), Echo State Network (ESN)
  - Deep Residual Network (DRN), Kohonen, **SVM**, **Neural Turing Machine (NTM)**
- **Detalle crítico:** **Transformers NO aparecen** (paper 2017, posterior a este chart)

**Tecnologías:** ML clásico, teoría de redes neuronales

### D8 — Las Capas de la IA (iceberg) (#30)

**Fuente:** No identificado (artwork con personaje)
**Lote:** 4

**Contenido:**
- "Todo el mundo usa IA. Casi nadie entiende cómo funciona"
- "Estamos aquí (2026)" señala la cima del iceberg
- **6 capas de superficie a fondo:**
  - **Capa 6 — IA Agéntica (2026):** Memoria, Planificación, Uso de herramientas, Ejecución autónoma. "IA que no solo responde. Actúa."
  - **Capa 5 — IA Generativa:** Modelos de lenguaje, Modelos de difusión, Modelos multimodales, Autocodificadores variacionales
  - **Capa 4 — Aprendizaje Profundo:** Transformadores, LSTM, RNN, Redes convolucionales, Autocodificadores
  - **Capa 3 — Redes Neuronales:** Perceptrones, Funciones costo, Retropropagación, Funciones activación, Capas ocultas
  - **Capa 2 — Aprendizaje Automático:** Supervisado, No supervisado, Clasificación, Regresión, **Refuerzo**
  - **Capa 1 — IA Clásica (1950s):** IA simbólica, Sistemas expertos, Representación conocimiento, Lógica y razonamiento
- "For3s OS opera en Capa 6 (Agéntica), construido sobre las 5 capas previas"

**Tecnologías:** Visión completa del campo de IA

### D9 — Tema 37: Machine Learning fundamentals (#45)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 6

**Contenido:**
- ML = rama de IA que permite a máquinas aprender patrones de datos sin programación explícita
- 6 pasos: recolecta datos → prepara datos → elige algoritmo → entrena modelo → predicciones → evalúa y mejora
- Ejemplo práctico: clasificar SPAM (datos etiquetados → vectorización → entrenamiento → predicción)
- 3 tipos ML:
  - **Supervisado:** datos etiquetados (Clasificación, Regresión)
  - **No supervisado:** sin etiquetas (Clustering, Reducción dimensionalidad)
  - **Por refuerzo:** prueba y error con recompensas (Juegos, Robótica)
- Algoritmos populares: Regresión Lineal, Regresión Logística, Árboles de decisión, **Random Forest**, **SVM**, **K-Means**
- Métricas: Exactitud (Accuracy), Precisión, Recall (Sensibilidad), F1-Score, Error (MSE, MAE)
- Dónde se usa: Recomendaciones (Netflix, YouTube, Spotify), Salud, Finanzas (fraude), Transporte, Marketing
- Desafíos: datos de calidad, sobreajuste (overfitting), falta datos, explicabilidad (cajas negras), ética y sesgo

**Tecnologías:** Machine Learning clásico, métricas de evaluación

### D10 — Reconocimiento Facial (#46)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 6

**Contenido:**
- Tecnología de IA que identifica/verifica a una persona por su rostro
- 5 pasos: captura imagen → detección rostro → extracción características (mapa biométrico) → comparación con BD → decisión
- **Tecnologías clave:** IA + ML (Deep Learning), Visión por Computadora, **CNN (Redes Neuronales Convolucionales)**, procesamiento tiempo real, bases datos biométricas seguras
- Puntos biométricos: frente, cejas, ojos, nariz, mejillas, boca, mandíbula, contorno facial
- 2 tipos:
  - **Verificación (1:1):** ¿eres quien dices ser? (desbloqueo móvil)
  - **Identificación (1:N):** ¿quién eres? (cámaras seguridad)
- Protección datos: cifrado, plantillas biométricas (no imágenes), auth local, consentimiento, políticas estrictas, **GDPR**
- Detección de vida (Anti-Spoofing): movimiento, profundidad 3D, parpadeos
- Pipeline: CNN → Procesamiento imágenes → Extracción características → Comparación biométrica → BD segura

**Tecnologías:** CNN, Deep Learning, Visión computacional, GDPR

### D11 — Búsqueda Binaria (#80)

**Fuente:** No identificado (estilo educativo claro)
**Lote:** 10

**Contenido:**
- Algoritmo eficiente para encontrar elemento en lista ordenada
- "Dividir para conquistar" — en cada paso reduce problema a la mitad
- Pseudocódigo con inicio/fin/medio, comparación con valor objetivo
- Implementación Python completa:
  ```python
  def busqueda_binaria(lista, objetivo):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
      medio = (inicio + fin) // 2
      if lista[medio] == objetivo:
        return medio
      elif lista[medio] < objetivo:
        inicio = medio + 1
      else:
        fin = medio - 1
    return -1
  ```
- Complejidad: O(1) mejor, O(log n) promedio y peor, O(1) espacial
- Ventajas: eficiente listas grandes, reduce comparaciones, O(log n)
- Desventajas: solo listas ordenadas, requiere acceso aleatorio, no en listas enlazadas
- Aplicaciones: BD indexadas, motores búsqueda internos, diccionarios, **algoritmos IA/ML (búsquedas espacios ordenados)**, estructuras avanzadas (B-Tree, Heaps)

**Tecnologías:** Algoritmos, Python

### D12 — Regresión Logística vs XGBoost vs Red Neuronal (#82)

**Fuente:** Data Science 4 Business
**Lote:** 11

**Contenido:**
- Imagen visual de 3 modelos ML clásicos en pizarras:
  - **Regresión Logística** — clasificación binaria, curva sigmoide, alta interpretabilidad
  - **XGBoost** — Gradient Boosting Trees, ensemble, alta precisión Kaggle
  - **Red Neuronal** — multi-layer perceptron, deep learning, no lineal
- Conceptual visual, NO técnica detallada
- Confirma taxonomía iceberg de IA #30

**Tecnologías:** Regresión Logística, XGBoost, Deep Learning

---

## 7. Bucket E — Bases de Datos y Patrones de Datos

**7 infografías. Densidad estratégica: MUY ALTA.**

### E1 — ACID (#24)

**Fuente:** No identificado (estilo neón oscuro)
**Lote:** 3

**Contenido:**
- ACID = propiedades que garantizan **confiabilidad de transacciones** en BD
- **A — Atomicidad:** la transacción se completa por entero o no se realiza en absoluto
- **C — Consistencia:** transacción lleva BD de un estado válido a otro estado válido
- **I — Aislamiento:** transacciones concurrentes no se interfieren entre sí
- **D — Durabilidad:** una vez confirmada, cambios permanecen incluso ante fallas
- "ACID garantiza datos íntegros, confiables y siempre correctos"

**Tecnologías:** PostgreSQL, MySQL, Oracle, SQL Server (implícitos)

### E2 — Event Sourcing (#50)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 7

**Contenido:**
- "Guardar TODO lo que pasa en un sistema"
- Patrón donde cambios de estado se guardan como **secuencia de eventos** en vez de solo el estado actual
- "Cada evento representa algo que sucedió en el sistema"
- Resultado: **historial completo, auditable y reconstruible**
- 5 pasos: ocurre algo → se genera evento → se guarda en Event Store → se actualiza modelo de lectura (proyecciones) → puede reconstruir estado completo
- Eventos ejemplo: UsuarioCreado, ProductoAgregado, PagoRealizado, EstadoCambiado
- Por qué usar Event Sourcing:
  - Historial completo
  - **Auditoría y trazabilidad total**
  - Reproducir y depurar problemas
  - Reconstruir estado actual
  - **Base perfecta para CQRS y microservicios**
- Enfoque tradicional vs Event Sourcing (comparación visual)
- **EVENT SOURCING + CQRS:**
  - ESCRITURA (Command): valida + genera eventos → Event Store
  - LECTURA (Query): proyecciones crean vistas optimizadas → BD de lectura
- Ejemplo transferencia bancaria con 4 eventos: CuentaDebitada, CuentaAcreditada, ComisionAplicada, NotificacionEnviada
- Dónde se usa: e-commerce, banca/finanzas, juegos online, salud, **auditoría/cumplimiento**, **SaaS empresariales**
- Buenas prácticas: eventos inmutables, versiones, esquema claro, monitorear tamaño Event Store, snapshots si muchos eventos, probar reconstrucción
- Desafíos: curva aprendizaje alta, complejidad inicial, Event Store crece, disciplina diseño, no ideal para todos los casos

**Tecnologías:** Event Sourcing, CQRS

### E3 — Streaming de Datos (#54)

**Fuente:** naiker.codes
**Lote:** 7

**Contenido:**
- Streaming = datos se generan/envían/procesan/consumen en tiempo real continuo
- 5 pasos: Generación → Publicación → Procesamiento → Distribución → Consumo
- "Todo en milisegundos. Sin esperar al final del flujo."
- Arquitectura:
  - **FUENTES:** Apps, Sensores, Logs, Clicks, IoT
  - **INGESTA:** **Apache Kafka, Pulsar, Kinesis, MQTT, NATS**
  - **PROCESAMIENTO:** **Flink, Spark Streams, Kafka Streams**
  - **ALMACENAMIENTO:** BD, Data Lakes, Search Engines
  - **CONSUMO:** Dashboards, Apps, Alertas, **ML/IA**
- **5 PLATAFORMAS POPULARES:**
  - **Apache Kafka** — más usada del mundo
  - **Apache Pulsar** — escalable, multi-tenant, open source
  - **AWS Kinesis** — administrado por AWS
  - **Google Pub/Sub** — totalmente administrado
  - **Redpanda** — alternativa moderna a Kafka, más rápida y simple
- Tipos:
  - **Streaming en tiempo real:** procesamiento inmediato (chats, trading, alertas)
  - **Micro-batch:** pequeños lotes cada pocos segundos (análisis, reportes, dashboards)
- Características: baja latencia (ms), procesamiento continuo 24/7, escalable (millones eventos/s), tolerancia fallos, eventos ordenados por clave
- Ejemplos reales: Netflix (video tiempo real), Twitch (video/chats), Spotify (música/recomendaciones), autos con sensores, bancos detectando fraudes

**Tecnologías:** Kafka, Pulsar, Kinesis, Pub/Sub, Redpanda, Flink, Spark Streams, Kafka Streams, MQTT, NATS

### E4 — Normalización en SQL (#67)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 9

**Contenido:**
- Proceso de organizar datos en tablas relacionadas para reducir redundancia y mejorar integridad
- Objetivos: evitar duplicados, facilitar mantenimiento, mejorar consistencia, optimizar almacenamiento, consultas eficientes
- **5 Formas Normales:**
  - **1FN:** eliminar grupos repetitivos, valores atómicos
  - **2FN:** cumplir 1FN + eliminar dependencias parciales
  - **3FN:** cumplir 2FN + eliminar dependencias transitivas
  - **BCNF (Boyce-Codd):** más estricta que 3FN, cada determinante = clave candidata
  - **4FN:** eliminar dependencias multivaluadas
- Ejemplo "de caos a orden": tabla única → 4 tablas relacionadas con FK
- 3 anomalías que evita: Inserción, Actualización, Eliminación
- Buenas prácticas:
  - Normaliza hasta 3FN en la mayoría
  - No normalices en exceso (puede perder rendimiento)
  - **Denormaliza solo si es necesario para reportes o rendimiento**
  - Usa claves primarias y foráneas correctamente
  - Diseña bien desde el inicio
- "Normalización = Menos duplicados + Más integridad + Mejor rendimiento + Bases de datos profesionales"

**Tecnologías:** SQL, RDBMS

### E5 — N+1 Query Problem (#76)

**Fuente:** No identificado (estilo Django/neon)
**Lote:** 10

**Contenido:**
- "The Silent Performance Killer"
- "Works fine in dev. Dies in production"
- Problema: 1 query para lista (N) + 1 query adicional por cada objeto para data relacionada
- Por qué es malo: demasiadas queries, app lenta, alta carga BD, pobre escalabilidad
- Ejemplo Django: User + Post con ForeignKey, loop accediendo a post.user.name → genera N+1 queries
- **SOLUCIÓN → select_related() en Django:**
  ```python
  posts = Post.objects.select_related("user")
  for post in posts:
      print(post.user.name)
  ```
  Resultado: 1 query optimizado con JOIN
- Para ManyToMany: prefetch_related()
- **Tabla select_related vs prefetch_related:**
  - select_related: ForeignKey/OneToOne, Single JOIN, SQL JOIN
  - prefetch_related: ManyToMany/Reverse FK, Multiple Queries, Separate + Python join
- Detección: Django Debug Toolbar, contar queries, monitor logs, **assertNumQueries() en tests**
- Best practices: usar select_related para FK/OneToOne, prefetch_related para M2M/Reverse FK, siempre test API performance, **check query count in development**, optimize before scaling
- Real-world impact: faster APIs, lower database load, better scalability
- "Always think about queries. Optimize early, not later. Good queries = High performance. Performance is a feature."

**Tecnologías:** Django ORM, SQL, JOIN

### E6 — Vector Database (#64)

**Fuente:** naiker.codes
**Lote:** 8

**Contenido:**
- "La base de datos diseñada para inteligencia artificial"
- Almacena datos como **vectores numéricos (embeddings)**, busca por significado no por palabras exactas
- 5 pasos: datos (textos/imágenes/audios) → Embeddings (modelo IA convierte a vectores) → Almacenamiento → Búsqueda (consulta también se convierte en vector) → Resultados (más similares en significado)
- "La clave es la SIMILARIDAD entre vectores (cercanía en espacio vectorial)"
- ¿Qué es un embedding?: representación numérica que captura significado del dato en un vector
  - Ejemplo: "El gato duerme en el sofá" → `[0.23, -0.11, 0.67, ..., -0.35, 0.91]`
- Cómo busca: consulta "perro jugando en parque" → convierte a vector → devuelve puntos más cercanos
- Para qué se usa:
  - Chatbots inteligentes
  - **Búsqueda semántica**
  - Sistemas recomendación
  - **Asistentes con memoria** (recuperan contexto)
  - Búsqueda de imágenes por contenido
- Características: vectores (no texto), búsqueda similitud semántica, alta escalabilidad/velocidad, ideal IA/ML, soporta metadatos/filtros/permisos
- **5 BASES DE DATOS VECTORIALES POPULARES:**
  - **Pinecone**
  - **Weaviate**
  - **Milvus**
  - **Qdrant**
  - **Chroma**

**Tecnologías:** Pinecone, Weaviate, Milvus, Qdrant, Chroma, embeddings

### E7 — Stored Procedures (#73)

**Fuente:** No identificado (estilo neón)
**Lote:** 9

**Contenido:**
- Rutina almacenada en BD con instrucciones SQL precompiladas
- Para qué sirve: operaciones complejas, reglas negocio, validaciones, tareas repetitivas, reportes dinámicos
- Ventajas: mejor rendimiento (precompilado), reduce tráfico red, reutilización código, mayor seguridad, mantenimiento centralizado
- Sintaxis básica SQL:
  ```sql
  CREATE PROCEDURE NombreProcedimiento (@Parametro INT)
  AS
  BEGIN
    SELECT * FROM Tabla WHERE Columna = @Parametro;
  END
  GO
  ```
- Tipos de parámetros: IN (entrada), OUT (salida), INOUT (entrada/salida)
- Buenas prácticas: nombres claros, validar parámetros, **manejar errores con TRY...CATCH**, documentar, evitar lógica innecesaria
- Ideal para: alto tráfico, sistemas seguros, procesos negocio críticos, integración sistemas

**Tecnologías:** SQL Server, PostgreSQL, MySQL

---

## 8. Bucket F — APIs / Backend Best Practices

**6 infografías. Densidad estratégica: ALTA.**

### F1 — Base64 en JSON: advertencia (#19)

**Fuente:** No identificado (estilo neón)
**Lote:** 3

**Contenido:**
- Advertencia crítica: imagen de 100 KB en Base64 (JSON) crece a 133 KB = **33% más grande**
- 5 advertencias adicionales:
  1. **Cadenas muy grandes pueden superar límites del servidor** (limit_max_len, max_allowed_packet, request size)
  2. Aumenta uso ancho de banda y memoria
  3. Más tiempo procesamiento y mayor latencia
  4. JSON con Base64 difícil de leer/depurar/mantener
  5. Mayor uso de recursos en BD y logs
- **Solución:**
  - Usar **carga multiparte (multipart/form-data)**
  - O subir a **almacenamiento (S3, GCS, etc.)** y enviar solo URL/ID
- "Optimiza, no sobrecargues. Tu API y tu servidor te lo agradecerán."

**Tecnologías:** S3, GCS, multipart/form-data, JSON

### F2 — Serialización (#22)

**Fuente:** naiker.codes
**Lote:** 3

**Contenido:**
- Proceso de convertir objetos en texto/binario para almacenar/transmitir datos
- 4 pasos: objeto creado → serializa → viaja por red → reconstruye
- **4 formatos comunes:**
  - **JSON** (texto)
  - **XML** (texto)
  - **BSON** (binario)
  - **Binario** crudo
- Uso real: APIs REST, microservicios, BD, apps móviles
- Ejemplo: objeto Usuario → SERIALIZACIÓN → `{"nombre": "Ana", "edad": 22}`
- Analogía: empacar/desempacar
- "Serialización = Objetos + Datos + Comunicación"

**Tecnologías:** JSON, XML, BSON

### F3 — Web Scraping (#36)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 5

**Contenido:**
- Web Scraping = extraer datos de páginas web automáticamente
- "Convierte datos no estructurados de la web en información útil y estructurada"
- 6 pasos: enviar petición → recibir HTML → analizar HTML → extraer datos → almacenar datos → usar datos
- Conceptos clave: Scraper/Bot, HTML, Selectores (CSS, XPath), Datos, Automatización
- **Ejemplo Python con BeautifulSoup:**
  ```python
  import requests
  from bs4 import BeautifulSoup

  url = "https://tienda.com/productos"
  respuesta = requests.get(url)
  soup = BeautifulSoup(respuesta.text, 'html.parser')

  productos = soup.select('.producto')
  for p in productos:
      nombre = p.select_one('.nombre').text.strip()
      precio = p.select_one('.precio').text.strip()
      print(nombre, precio)
  ```
- **5 herramientas populares:**
  - **BeautifulSoup** — extrae HTML/XML
  - **Scrapy** — framework completo para gran escala
  - **Selenium** — automatiza navegadores
  - **Puppeteer/Playwright** — Chrome/Chromium scraping avanzado
  - **Octoparse/ParseHub** — no-code visual
- Para qué se usa: comparación precios, análisis mercado, generación leads, monitoreo contenido, investigación académica
- Tipos sitios: Estáticos (HTML fijo) vs Dinámicos (JavaScript, requiere Selenium/Puppeteer)
- Ética y límites: respeta robots.txt, NO sobrecargues servidores, USA datos públicos, CUMPLE LA LEY
- Desafíos: bloqueos IP, CAPTCHAs, contenido dinámico, estructuras cambiantes, paginación

**Tecnologías:** BeautifulSoup, Scrapy, Selenium, Puppeteer, Playwright, Python, robots.txt

### F4 — Sockets (#53)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 7

**Contenido:**
- Socket = extremo de comunicación entre dos programas en distintos dispositivos
- Permite enviar/recibir datos usando IP y puerto
- 5 pasos: crear socket → conectar/escuchar → enviar datos → recibir datos → cerrar conexión
- IP y Puertos:
  - IP identifica dispositivo (192.168.1.10)
  - Puerto identifica aplicación (8080)
- **Puertos comunes:**
  - 21 FTP, 80 HTTP, 443 HTTPS, 22 SSH, 3306 MySQL, **5432 PostgreSQL**
- Tipos:
  - **SOCKET TCP (STREAM):** conexión orientada, confiable, asegura orden/sin errores, 3-way handshake (SYN→SYN-ACK→ACK), chats/webs/emails
  - **SOCKET UDP (DGRAM):** sin conexión, no confiable, más rápido, ideal videojuegos/streaming/llamadas
- Ejemplos Python TCP servidor + cliente con código
- "SOCKET = Conexión + Comunicación + Tiempo Real + Sin Límites"

**Tecnologías:** TCP, UDP, Python sockets, HTTP, HTTPS, SSH, PostgreSQL

### F5 — API Gateway (#62)

**Fuente:** naiker.codes
**Lote:** 8

**Contenido:**
- "El guardia de seguridad de las APIs"
- Servidor que actúa como **punto de entrada único** para todas las solicitudes hacia microservicios
- Se encarga de enrutar, proteger, optimizar, gestionar tráfico
- 5 pasos: cliente envía → gateway recibe/aplica reglas → enruta al microservicio → microservicio procesa → gateway devuelve respuesta
- **6 FUNCIONES PRINCIPALES:**
  1. **Autenticación y Autorización** (JWT, OAuth2, API Keys)
  2. **Rate Limiting** (límite por usuario/IP)
  3. **Enrutamiento Inteligente** (al microservicio correcto)
  4. **Agregación de Respuestas** (combina múltiples servicios)
  5. **Transformación de Datos** (modifica request/response)
  6. **Monitoreo y Analíticas** (métricas, logs, errores)
- Ejemplo Rate Limiting: 100 req/min/user, si excede → 429 Too Many Requests
- **Desafíos críticos:**
  - **Punto único de falla (SPOF)**
  - Puede ser cuello de botella
  - Complejidad adicional
  - Requiere monitoreo + alta disponibilidad
- Seguridad centralizada: validación tokens/permisos, RBAC, enmascaramiento info sensible, **políticas CORS y headers seguridad**
- "API Gateway = Entrada Única + Seguridad + Gestión Tráfico + Escalabilidad + Mejor Experiencia"

**Tecnologías:** Kong, NGINX, JWT, OAuth2, API Keys, CORS

### F6 — Login completo end-to-end (#58)

**Fuente:** No identificado (estilo neón oscuro)
**Lote:** 8

**Contenido:**
- 3 componentes: CLIENTE (FRONTEND) → BACKEND (SERVIDOR) → BASE DE DATOS
- **Tecnologías comunes:**
  - Frontend: React, Vue, Angular
  - Backend: Node.js, Python, PHP, Java
  - BD: MySQL, PostgreSQL, MongoDB
  - Auth: JWT, Sessions, Cookies
- 8 pasos completos del flujo de login
- Casos error: 404/401 si usuario no existe, 401 si password no coincide
- **Regla crítica:** "La contraseña NUNCA se almacena en texto plano. Siempre debe guardarse hasheada"
- Token uso: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`
- Tipos auth:
  - **JWT (Stateless):** token contiene info firmada, ideal APIs/escalabilidad
  - **Sessions (Stateful):** servidor guarda sesión, ideal apps tradicionales
- **Buenas prácticas:**
  - Usa HTTPS siempre
  - Hashea contraseñas (**bcrypt, argon2**)
  - Usa JWT con expiración
  - No expongas info sensible
  - Limita intentos login (**rate limiting**)

**Tecnologías:** React, Vue, Angular, Node.js, Python, PHP, Java, MySQL, PostgreSQL, MongoDB, JWT, bcrypt, argon2

---

## 9. Bucket G — Ingeniería SW / Calidad / Arquitectura

**5 infografías. Densidad estratégica: MUY ALTA.**

### G1 — Refactorizar (#21)

**Fuente:** No identificado (estilo neón verde)
**Lote:** 3

**Contenido:**
- "Refactorizar = mejorar el código por dentro sin cambiar lo que hace por fuera"
- 3 beneficios: más legible, más ordenado, más mantenible
- Ejemplo ANTES (duplicación) vs DESPUÉS (extracción función común):
  - ANTES: `enviarEmail()` y `enviarSMS()` ambas con `validarUsuario(); guardarLog();`
  - DESPUÉS: `prepararEnvio()` función común, reusada por ambas
- Es ejemplo de **DRY + extracción de función**
- "Mejor código hoy, menos problemas mañana"

**Tecnologías:** JavaScript (ejemplo), patrones de refactorización

### G2 — Clean Architecture (#49)

**Fuente:** No identificado (estilo dibujado a mano)
**Lote:** 6

**Contenido:**
- "Dependencias hacia ADENTRO, valor hacia AFUERA"
- Flexibilidad, testabilidad y escalabilidad
- **EL PROBLEMA:** sistemas acoplados a frameworks y detalles externos. Sistema caótico Controller↔UI↔Framework↔DB↔Email↔External API↔Business Rules.
  - ✗ Difícil de cambiar
  - ✗ Difícil de probar
  - ✗ Alto acoplamiento
  - ✗ Cualquier cambio rompe algo
- **LA SOLUCIÓN — 4 capas concéntricas (de afuera hacia adentro):**
  - **Capa 1 — PRESENTATION:** UI, Controllers, Presenters
  - **Capa 2 — INFRASTRUCTURE:** Implementaciones de Interfaces
  - **Capa 3 — APPLICATION:** Casos de Uso (Interfaz de Aplicación)
  - **Capa 4 (centro) — DOMAIN:** Entidades y Reglas del Negocio
- **REGLA DE ORO:** "El código fuente en las dependencias siempre debe apuntar hacia adentro, hacia las reglas del negocio."
- Adapters: Presentation (Web, Mobile, CLI), Infrastructure (SQL DB, MongoDB, Email, External API)
- **4 beneficios:**
  - Independiente de frameworks
  - Fácil de cambiar
  - Fácil de probar
  - Diseñado para crecer
- "Los frameworks cambian. Las necesidades del negocio también. Pero una buena arquitectura te permite evolucionar sin reescribir tu producto."
- Sin Clean Architecture vs Con Clean Architecture (comparación visual)
- "Arquitectura no es escribir más código. Es tomar mejores decisiones hoy, para tener mañana."

**Tecnologías:** Patrones arquitectónicos, agnóstico de lenguaje

### G3 — Acoplamiento en programación (#55)

**Fuente:** naiker.codes
**Lote:** 7

**Contenido:**
- "El error invisible que vuelve difícil mantener una app"
- Grado de dependencia entre módulos/clases/funciones/componentes
- Objetivo: **bajo acoplamiento + alta cohesión**
- **6 TIPOS (de peor a mejor):**
  1. **Acoplamiento de Contenido:** módulo modifica directamente código interno de otro (muy difícil)
  2. **Acoplamiento Común:** comparten datos globales (efectos inesperados)
  3. **Acoplamiento Externo:** dependencia de formatos/archivos/APIs (cambios externos afectan)
  4. **Acoplamiento de Control:** módulo controla flujo interno de otro (difícil entender/reutilizar)
  5. **Acoplamiento de Sello (Stamp):** pasa estructura completa pero usa solo parte (mejor, mejorable)
  6. **Acoplamiento por Datos:** solo comparten datos necesarios (✅ IDEAL)
- Ejemplo alto acoplamiento: UsuarioController → UsuarioRepository → MySQLConnection (rígido)
- Ejemplo bajo acoplamiento: UsuarioController → IUsuarioRepository (interfaz) → UsuarioRepositoryMySQL (flexible)
- Buenas prácticas:
  - Usa interfaces y abstracciones
  - Aplica **inyección de dependencias**
  - Separa responsabilidades (**SRP - Principio SOLID**)
  - Evita variables globales y estados compartidos
  - Comunica módulos con contratos claros
- Dónde se ve: clases/objetos, módulos/librerías, servicios (microservicios), BD/aplicación, APIs/consumidores
- "Bajo Acoplamiento = Código Flexible + Fácil de Mantener + Menos Errores + Equipos Productivos"

**Tecnologías:** Patrones SOLID, interfaces, inyección dependencias

### G4 — Principio DRY (#68)

**Fuente:** naiker.codes
**Lote:** 9

**Contenido:**
- DRY = Don't Repeat Yourself
- "La regla que evita copiar y pegar código"
- "Cada pieza de lógica debe tener una única representación en el sistema"
- Importante por: menos errores, más mantenible, más reutilizable, más eficiente, mejor calidad
- Ejemplo SIN DRY: `calcularTotalCarrito1` y `calcularTotalCarrito2` con misma lógica duplicada
- Ejemplo CON DRY: una sola función `calcularTotalCarrito` reusada
- **5 maneras de aplicar DRY:**
  1. Usa funciones
  2. Crea módulos
  3. Usa clases y componentes
  4. Configuración y constantes
  5. Plantillas y snippets
- DRY en áreas: JavaScript (funciones), Python (funciones reutilizables), SQL (vistas, procedimientos), HTML (componentes/plantillas), APIs (endpoints/lógica compartida)
- Qué pasa si no usas DRY: más líneas innecesarias, más tiempo cambios, mayor probabilidad errores, código difícil mantener, proyectos más costosos
- "Duplicar código hoy, es sufrir mañana"

**Tecnologías:** JavaScript, Python, SQL, HTML — agnóstico

### G5 — Dependency Injection (#75)

**Fuente:** naiker.codes
**Lote:** 10

**Contenido:**
- "El patrón que hace Angular tan poderoso y organizado"
- Patrón que permite que un objeto reciba sus dependencias desde fuera, en lugar de crearlas por sí mismo
- 3 pasos: Componente necesita servicio → Angular proporciona instancia → Componente usa sin crear
- 5 razones por qué es importante:
  - Código desacoplado
  - Más escalable
  - **Fácil de probar** (pruebas unitarias)
  - Servicios compartidos
  - Arquitectura enterprise
- Ejemplo TypeScript Angular:
  ```typescript
  @Injectable({providedIn: 'root'})
  export class UsuarioService {...}

  @Component({...})
  export class ListaComponent {
    constructor(private usuarioService: UsuarioService) {}
  }
  ```
- Sin DI: alto acoplamiento, difícil probar, código duplicado, mantenibilidad baja
- Con DI: código limpio/desacoplado, fácil probar, reutilizable, escalable/mantenible
- Dónde se usa en Angular: Servicios, Guards, Interceptors, Pipes, Resolvers, Directivas
- "La inyección de dependencias es la clave de una arquitectura limpia y profesional"

**Tecnologías:** Angular, TypeScript — patrón aplicable a cualquier lenguaje

### G6 — Servicios en Angular (#83) — aplicación práctica de DI

**Fuente:** naiker.codes
**Lote:** 11

**Contenido:**
- "La forma profesional de organizar aplicaciones Angular"
- Servicio = clase que contiene lógica reutilizable, se comparte entre componentes
- 5 razones para usar servicios: lógica reutilizable, separación responsabilidades, fácil mantenimiento, conectividad APIs, DI
- Flujo: Componente → Servicio → Recursos/API → datos vuelven al componente
- Ejemplo TypeScript práctico con HttpClient y RxJS
- 3 tipos:
  - **Global** (`providedIn: 'root'`): toda la app
  - **Módulo** (`providers: []`): solo en módulo
  - **Local** (providers en componente): instancia única
- Beneficios: apps escalables, menos código duplicado, modular, **pruebas sencillas**, mejor rendimiento

**Tecnologías:** Angular, TypeScript, HttpClient, RxJS

---

## 10. Bucket H — Fundamentos de Cómputo

**2 infografías. Densidad estratégica: BAJA.**

### H1 — Potencias de 2 / unidades de almacenamiento (#23)

**Fuente:** No identificado (estilo neón)
**Lote:** 3

**Contenido:**
- Por qué unidades como 128, 256, 512: multiplicación por duplicación del 2 (base binaria)
- Secuencia: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048... (potencias de 2)
- Cada unidad doble de anterior porque computadoras usan bits (0 y 1)
- **Unidades reales base 2:**
  - 1 KB = 2¹⁰ bytes = 1,024 bytes
  - 1 MB = 2²⁰ bytes = 1,048,576 bytes
  - 1 GB = 2³⁰ bytes = 1,073,741,824 bytes
  - 1 TB = 2⁴⁰ bytes
  - 1 PB = 2⁵⁰ bytes
- **Advertencia:** "A veces fabricantes usan base 10 (1KB = 1,000 bytes), pero el sistema usa base 2. Por eso la capacidad real puede ser menor a la prometida."

**Tecnologías:** Fundamentos cómputo

### H2 — Microcontroladores (#38)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 5

**Contenido:**
- Mini computadora integrada en un solo chip (procesador, memoria, periféricos I/O)
- Para tareas específicas de control y automatización en sistemas embebidos
- Cómo funciona 6 pasos: lee entradas → procesa datos → toma decisiones → genera salidas → controla dispositivos → repite ciclo
- **5 microcontroladores populares:**
  - **Arduino UNO** (ATmega328P)
  - **ESP32** (Wi-Fi + Bluetooth, ideal IoT)
  - **STM32** (industrial/profesional)
  - **PIC (Microchip)** (control industrial/embebidos)
  - **Raspberry Pi Pico** (RP2040)
- Especs Arduino UNO: ATmega328P, 5V, 14 pines digitales (6 PWM), 6 analógicos, 32KB Flash, 2KB SRAM, 16MHz
- Protocolos: I2C, SPI, UART, Bluetooth, Wi-Fi
- Programación: Arduino IDE, PlatformIO → compila → carga vía USB → ejecuta en bucle
- Aplicaciones: casas inteligentes, Industria 4.0, agricultura inteligente, wearables, automatización hogar
- **Relevancia para For3s:** indirecta — patrón "lee → procesa → decide → genera salida → repite ciclo" es **cómo opera un agente cognitivo**

**Tecnologías:** Arduino, ESP32, STM32, PIC, Raspberry Pi Pico, IoT

---

## 11. Bucket I — Seguridad / Auth / Secrets / Criptografía

**6 infografías. Densidad estratégica: MUY ALTA.**

### I1 — Login con JWT (#26)

**Fuente:** naiker.codes
**Lote:** 4

**Contenido:**
- JWT (JSON Web Token) = estándar que permite autenticar usuarios mediante **tokens firmados digitalmente**
- 5 claves: basado en tokens, usado en APIs, **sin estado (stateless)**, firmado digitalmente, seguro si se implementa correctamente
- 5 pasos: usuario envía credenciales → servidor valida → genera JWT → token al cliente → cliente lo usa en futuras peticiones
- Header HTTP: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- "El servidor NO guarda sesiones; la información va dentro del token y se verifica con la firma"
- Dónde se usa: APIs REST, web modernas, apps móviles, **microservicios**, sistemas distribuidos
- Ventajas: escalable, sin almacenamiento sesión, ideal sistemas distribuidos, eficiente, multi-plataforma
- **Estructura JWT:** Header (algoritmo + tipo) + Payload (datos + claims: sub, name, role, exp) + Signature (firma digital)
- Ejemplo payload: `{"sub": "1234567890", "name": "Juan Pérez", "role": "user", "exp": 1715616000}`
- Flujo: cliente envía JWT en Header → servidor verifica firma → acceso autorizado
- Analogía: carnet digital firmado

**Tecnologías:** JWT, Bearer Token, HTTP Authorization

### I2 — Cookies con seguridad (#35)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 5

**Contenido:**
- Cookie = archivo pequeño de texto que sitio guarda en navegador
- 5 pasos: solicitud → respuesta → almacenamiento → solicitud futura → reconocimiento
- Ejemplo práctico login: `Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure`
- **Tabla COOKIES vs LOCAL STORAGE:**
  - Tamaño: 4KB vs 5-10MB
  - Envío servidor: Sí (cada petición) vs NO
  - Persistencia: depende vs hasta eliminar
  - Accesibilidad: automática vs JavaScript
- Tipos: Sesión (eliminan al cerrar) + Persistentes (fecha expiración)
- Estructura: `nombre=valor; atributo1=valor1; ...`
- **Atributos importantes:**
  - **Expires/Max-Age:** fecha expiración
  - **Path:** ruta válida
  - **Domain:** dominio válido
  - **Secure:** solo HTTPS
  - **HttpOnly:** no accesible desde JavaScript ⭐ (protege XSS)
  - **SameSite:** controla peticiones cruzadas ⭐ (protege CSRF)
- Ejemplo real HTTP response:
  ```
  HTTP/1.1 200 OK
  Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=3600
  ```
- **Buenas prácticas SEGURIDAD:**
  - Usar siempre HTTPS
  - Marcar cookies como HttpOnly
  - Establecer SameSite para evitar CSRF
  - Definir fecha expiración adecuada
  - No almacenar contraseñas en cookies
  - Usar cookies sesión para datos sensibles
  - Informar usuario sobre uso (política privacidad)

**Tecnologías:** HTTP, cookies, HttpOnly, SameSite, Secure, HTTPS

### I3 — DNS over HTTPS (DoH) (#39)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 5

**Contenido:**
- DoH = protocolo que permite hacer consultas DNS a través de conexiones HTTPS cifradas
- Impide que terceros vean/modifiquen consultas DNS
- "DoH = privacidad + seguridad + confianza en cada consulta"
- 6 pasos: consulta DNS → navegador con DoH → resolutor DoH → respuesta cifrada → conexión establecida → navegación segura
- Conceptos clave: DNS, DoH, **Cifrado TLS/SSL**, Privacidad usuario, Integridad datos (previene DNS spoofing)
- DoH vs DNS Tradicional:
  - DNS Tradicional (UDP/TCP 53): cualquiera ve consultas, manipula respuestas, registra actividad
  - DoH (HTTPS 443): solo el resolutor puede ver/procesar/responder seguro
- **5 Servicios DoH populares:**
  - **Cloudflare:** `https://cloudflare-dns.com/dns-query`
  - **Google Public DNS:** `https://dns.google/dns-query`
  - **Quad9:** `https://dns.quad9.net/dns-query`
  - **NextDNS:** `https://dns.nextdns.io`
  - **AdGuard DNS:** `https://adguard-dns.com/dns-query`
- Ejemplo JSON: `{"name": "www.ejemplo.com", "type": "A"}`
- Casos uso: navegación privada, empresas, escuelas/universidades, hogares, viajes (evitar censura)
- Limitaciones: no 100% anónimo, confía en proveedor, no reemplaza otras medidas (VPN, HTTPS)

**Tecnologías:** DNS, HTTPS, TLS/SSL, Cloudflare DNS, Google Public DNS, Quad9, NextDNS, AdGuard DNS

### I4 — Variables de entorno + Secret Managers (#44)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 6

**Contenido:**
- Variable de entorno = valor fuera del código accesible en runtime
- "Donde las apps esconden información importante"
- Por qué importante: protege info sensible (API Keys, contraseñas, tokens), permite configurar por ambiente, facilita despliegue, evita exponer secretos
- **Tipos de info:**
  - **API Keys** (Stripe, Maps)
  - **Credenciales** (BD)
  - **URLs y Endpoints**
  - **Secretos y Tokens** (JWT secrets, salts)
  - **Configuraciones** (modos, timeouts, feature flags)
- **3 AMBIENTES estándar:**
  - **DESARROLLO (.env.development):** DB_HOST=localhost, DEBUG=true
  - **STAGING (.env.staging):** DB_HOST=staging-db, DEBUG=false
  - **PRODUCCIÓN (.env.production):** DB_HOST=prod-db, DEBUG=false
- Ejemplos Node.js + Python con dotenv y os.getenv
- Ejemplo .env completo con DB_HOST/PORT/USER/PASS/NAME, PORT, NODE_ENV, API_URL, JWT_SECRET, S3_BUCKET
- **Advertencia crítica:** "Este archivo NO se debe subir al repositorio. Agrega a .gitignore"
- **Buenas prácticas:**
  - Nunca subas .env al repo
  - Usa .env.example con variables ejemplo sin valores reales
  - **Usa secretos seguros en producción (AWS Secrets Manager, Vault, etc.)**
  - Aplica principio mínimo privilegio
  - Rota claves y secretos periódicamente
- **4 HERRAMIENTAS POPULARES:**
  - **dotenv** (cargar en desarrollo)
  - **AWS Secrets Manager**
  - **HashiCorp Vault**
  - **Google Secret Manager**
- MAL ejemplo vs BUEN ejemplo (hardcoded vs process.env)

**Tecnologías:** dotenv, AWS Secrets Manager, HashiCorp Vault, Google Secret Manager

### I5 — Funciones Hash (#52)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 7

**Contenido:**
- Hash = algoritmo matemático que toma cualquier dato y genera cadena de tamaño fijo
- "La huella digital de los datos"
- Unidireccional: fácil generar hash, casi imposible obtener dato original
- 5 pasos: entrada → algoritmo hash → salida única (longitud fija) → cambio mínimo = hash diferente → verificación
- Características clave:
  - **Determinística:** mismo dato → mismo hash
  - Rápida
  - Unidireccional
  - **Resistente a colisiones**
  - **Efecto avalancha:** pequeños cambios → hashes muy diferentes
- **5 Algoritmos populares:**
  - **MD5** — 128 bits, **ya no recomendado**
  - **SHA-1** — 160 bits, **en desuso**
  - **SHA-256** — 256 bits, **muy seguro y usado ampliamente** ⭐
  - **SHA-512** — 512 bits, mayor seguridad
  - **BLAKE2 / BLAKE3** — modernos, rápidos, seguros ⭐
- Usos principales: almacenamiento seguro contraseñas, verificación integridad archivos, firmas digitales, **transacciones blockchain**, detección manipulación
- Hash en contraseñas: "Las contraseñas se almacenan como hashes, nunca en texto plano"
- Riesgos: si algoritmo es débil puede romperse, ataques colisión, no usar para cifrado (no reversible)

**Tecnologías:** MD5, SHA-1, SHA-256, SHA-512, BLAKE2, BLAKE3

---

## 12. Bucket J — AI-Native Development / Claude / MCP

**7 infografías. Densidad estratégica: MUY ALTA.**

### J1 — Claude Code /goal v2.1.139+ (#27)

**Fuente:** code.claude.com/docs/en/goal | @godofprompt
**Lote:** 4

**Contenido:**
- "Tell Claude what done looks like. It keeps working until it gets there."
- Loop: You define finish line → Claude works → Second AI checks: done yet? → Yes (Done) / No (keep going)
- **3 elementos de un buen goal:**
  1. **A clear finish line** ("the signup form works on mobile and desktop")
  2. **A way to verify** ("Lighthouse score is above 90")
  3. **Boundaries** ("don't modify the homepage design")
- Good vs Too vague examples
- **Template:** `/goal [task] until [finish line], verified by [check], while [boundaries], or stop after [limit]`
- Comandos: `/goal [condition]` (set), `/goal` (check progress), `/goal clear` (stop early), `claude -p "/goal ..."` (hands-free), `--resume`, `pair with auto mode` (full autopilot)

**Tecnologías:** Claude Code CLI

### J2 — Claude Code Project Structure (#31)

**Fuente:** Anthropic AI
**Lote:** 4

**Contenido:**
- "A clean, production-ready structure for Claude Code projects that scale"
- 5 propiedades: AI-Native Development, MCP Ready, Modular & Scalable, **Secure by Default**, Built for Production
- **Estructura completa my_project/:**
  - CLAUDE.md
  - .claude/ (settings.json, settings.local.json, commands/ con review.md, deploy.md, test-all.md, bootstrap.md)
  - skills/ (code-review/SKILL.md, text-writer/, security-audit/, refactor/)
  - agents/ (code-reviewer.yml, test-writer.yml, security-auditor.yml, devops-sre.yml)
  - plugins/ (manifest.json, my-plugin/)
  - .mcp.json
  - components/ (auth/, dashboard/, search/)
  - services/ (api.ts, auth.ts, database.ts)
  - utils/, types/, tests/ (unit, integration, e2e), docs/ (architecture.md, api-reference.md, onboarding.md), scripts/ (setup.sh, deploy.sh, seed.db.sh)
  - package.json, tsconfig.json, .env.example, .gitignore, Dockerfile, README.md
- **Key Components:** CLAUDE.md (project memory), .claude/ (config), commands/ (slash commands), skills/ (auto-activated), .mcp.json (MCP server config), agents/ (subagents)
- **CLAUDE.md essentials:** project conventions, tech stack overview, testing requirements, git workflow, security rules, file naming, review checklist
- **Extension types:** Skills, Hooks, MCP, Subagents, Agent Teams, Plugins
- **Hook events:** PreToolUse, PostToolUse, SessionStart, SessionEnd, PreCommit, Notification
- **settings.json structure** con permissions (allow/deny), hooks (PreToolUse + PostToolUse con commands), env (MAX_THINKING_TOKENS=10000, CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50)
- **.mcp.json structure** con mcpServers github (`npx @anthropic-ai/mcp-github` + GITHUB_TOKEN) y postgres
- **Popular MCP servers:** GitHub, JIRA/Linear, Slack, PostgreSQL, Playwright, Filesystem
- **Best practices:** Iterative Development, Clear Skill Documentation, Modular Skill Design, **Secure Secret Handling**, Regular Testing & Auditing
- **Getting Started:** `npm i -g @anthropic-ai/claude-code` → `cd your-project && claude` → Create CLAUDE.md → Add slash commands → Configure MCP → Add skills
- **Context management:** 0-60% (Work normally), 50-70% (Monitor), 70-80% (Run compact), 80%+ (Clear mandatory)
- **TECH STACK declarado:** Next.js 14, TypeScript, Tailwind, Supabase for auth & database, Prisma ORM, tRPC API layer, ESLint + Prettier, Zod for validation, Playwright for testing
- **CONVENTIONS:** Always write tests before code, conventional commits, never commit to main, lint + typecheck before PR, components small/focused, prefer server components
- **SECURITY:** No secrets in code/logs, validate user inputs, parameterized queries, row-level security, environment variables, rotate secrets
- **WORKFLOW:** Branch from develop → Create feature branch → Write tests → Implement → Review & refactor → Merge via PR
- **Estructura src:** /components, /services, /utils, /types, /app, /tests

**Tecnologías:** Claude Code, MCP, Next.js 14, TypeScript, Tailwind, Supabase, Prisma, tRPC, ESLint, Prettier, Zod, Playwright

### J3 — Claude Code OS pixel art (#37)

**Fuente:** No identificado (pixel art retro)
**Lote:** 5

**Contenido:**
- "7 items · 5 min setup · Works on any project"
- Vista pixel-art tipo OS retro
- Estructura: `.claude/`, `hooks/`, `rules/`, `agents/`, `skills/`, `commands/`, `CLAUDE.md`, `memory/archive/README.md`, `.claude/settings.json`
- "Follow + Comment 'Claude OS' to GET it FREE"
- Resumen visual de la misma idea que #31

**Tecnologías:** Claude Code

### J4 — Claude for small business — 31 skills (#34)

**Fuente:** Charlie Hills @ charliehills.substack.com
**Lote:** 5

**Contenido:**
- "Anthropic launched 31 pre-built skills for small business owners"
- **Plugs into 12 tools:** QuickBooks, PayPal, HubSpot, Canva, Stripe, Slack, Square, Microsoft, Gmail, Google Calendar, Google Drive
- **31 skills en 6 categorías:**
  - **MONEY (10):** /cash-flow-snapshot, /plan-payroll, /margin-analyzer, /price-check, /invoice-chase, /month-heads-up, /month-end-prep, /close-month, /tax-prep, /tax-season-organizer
  - **SALES & CRM (6):** /call-list, /lead-triage, /crm-cleanup, /crm-maintenance, /sales-brief, /quarterly-review
  - **MARKETING (3):** /content-strategy, /canva-creator, /run-campaign
  - **CUSTOMERS (4):** /customer-pulse, /customer-pulse-check, /handle-complaint, /ticket-deflector
  - **BRIEFINGS (3):** /monday-brief, /friday-brief, /business-pulse
  - **SETUP, HIRING & LEGAL (5):** /smb-router, /smb-onboard, /job-post-builder, /contract-review, /review-contract
- Cada skill conectada a integraciones específicas con iconos

**Tecnologías:** Claude Skills, integraciones SMB

### J5 — AI Agent cheat sheet — How to Create AI Agent using Claude (#48)

**Fuente:** No identificado (estilo card moderna)
**Lote:** 6

**Contenido:**
- "A complete cheat sheet to build smart & powerful AI Agents"
- **AI Agent:** "Intelligent system that can understand goals, plan steps, use tools, remember context and take action with minimal human input"
- 4 atributos: Autonomous, Goal Oriented, Uses Tools, Learns & Improves
- **AI Agent Creation Workflow — 7 pasos:**
  1. Define Goal
  2. Design Behavior
  3. Choose Tools
  4. Write System Prompt
  5. Build & Test
  6. Deploy
  7. Improve
- **KEY FORMULA:** Clear Goal + Good Instructions + Right Tools + Memory + Testing = Powerful AI Agent
- 6 steps detallados con ejemplos (research agent)
- **Useful Claude Features:** Projects, Long Context, Artifacts, Tool Use, Memory
- Use cases: Research & Summaries, Business Automation, Content & Marketing, Education & Learning, Personal Productivity

**Tecnologías:** Claude Projects, Tool Use, Memory, MCP implícito

### J6 — Prompt Engineering (#70)

**Fuente:** naiker.codes
**Lote:** 9

**Contenido:**
- "La habilidad más importante en la era de la IA"
- Prompt Engineering = arte de crear instrucciones claras/específicas/efectivas
- 5 pasos: define objetivo → da contexto → da instrucciones → genera respuesta → mejora y ajusta
- **5 ingredientes de un buen prompt:**
  1. **ROL** (experto, profesor, asistente)
  2. **CONTEXTO**
  3. **TAREA**
  4. **FORMATO** (lista, tabla, pasos)
  5. **EJEMPLOS** (opcional)
- Ejemplo prompt efectivo completo (marketing digital + redes sociales + Instagram)
- Tips: sé específico, divide tareas complejas, itera y mejora, usa ejemplos, evita ambigüedad
- **REGLA DE ORO:** "Un buen prompt no es suerte, es estrategia"

**Tecnologías:** Prompt engineering (agnóstico)

### J7 — MCP (Model Context Protocol) (#66, repetido en #77)

**Fuente:** naiker.codes
**Lote:** 9 (repetido en lote 10)

**Contenido:**
- "La tecnología que permite que la IA use herramientas reales"
- "Conecta IA con herramientas, APIs, archivos y más, de forma segura y estándar"
- MCP = protocolo abierto para que IA se conecte con herramientas externas
- **"Piensa en MCP como el 'USB-C' de los agentes inteligentes"** ⭐ (analogía clave)
- 5 pasos: descubrimiento → conexión → ejecución → respuesta → contexto actualizado
- "MCP permite que la IA no solo hable, sino que ACTÚE en el mundo real"
- Para qué sirve: conectar IA con APIs, leer/escribir/buscar archivos/BD, ejecutar código/scripts, enviar correos/mensajes/notificaciones, automatizar tareas complejas
- **Arquitectura MCP típica:**
  - MODELO IA (GPT-4, Claude, Gemini, LLaMA) → Solicita acción
  - CLIENTE MCP (descubre, conecta, ejecuta, recibe)
  - Protocolo MCP
  - SERVIDOR MCP (APIs, archivos, BD, herramientas personalizadas)
  - HERRAMIENTAS (APIs REST/GraphQL, archivos TXT/PDF/CSV, BD SQL/NoSQL, código/scripts, Email/Slack/Drive)
- Ejemplos de uso: IA+API (clima, bolsa, noticias), IA+Archivos (leer docs, reportes), IA+Código (scripts, pruebas), IA+BD (consultar, insertar, actualizar), IA+Automatización (emails, tareas, flujos)
- **"MCP es la base para el futuro de los agentes IA autónomos y productivos"**
- **CLIENTES MCP (EJEMPLOS):**
  - **OpenAI Agents SDK**
  - **Claude Desktop** ⭐
  - **Cursor**
  - **Continue**
  - **Ollama**
- **SERVIDORES MCP (EJEMPLOS):**
  - **Filesystem Server**
  - **PostgreSQL Server**
  - **GitHub Server**
  - **Slack Server**
  - **Custom Server**
- Beneficios: mayor capacidad acción, respuestas precisas, integración flexible, automatización avanzada, escalabilidad/modularidad
- **EL FUTURO ES AGÉNTICO:** "MCP permite que la IA deje de estar aislada y se convierta en un verdadero asistente digital capaz de interactuar con el mundo real"
- **APARECE 2 VECES en el banco — señal fuerte de fundacionalidad**

**Tecnologías:** MCP, OpenAI Agents SDK, Claude Desktop, Cursor, Continue, Ollama, GitHub, PostgreSQL, Slack

---

## 13. Bucket K — Estructuras de Datos y Algoritmos

**2 infografías. Densidad estratégica: BAJA.**

### K1 — Nodo (#29)

**Fuente:** naiker.codes
**Lote:** 4

**Contenido:**
- Unidad básica que almacena datos y conexiones hacia otros elementos
- Esquema: Dato + Referencia (next) → apunta al siguiente nodo
- Partes: Dato (información), Referencia (apunta a otro nodo), Puntero (dirección memoria), Conexión (une nodos)
- Cómo funciona: almacena valor → apunta otro nodo → se crean conexiones → forma estructuras
- Ejemplo visual: `[10 | next] → [20 | next]`
- **Uso real:** listas enlazadas, **árboles**, **grafos**, redes
- Ventajas: estructuras dinámicas, flexibilidad, **escalabilidad**, organización eficiente
- Analogía: vagón de tren conectado a otros
- **Detalle crítico:** menciona explícitamente **grafos** como uso real

**Tecnologías:** Estructuras de datos clásicas

### K2 — Búsqueda Binaria (ver D11) — también algoritmo

---

## 14. Bucket L — IA / Panorama / Taxonomía / Agents / RAG

**8 infografías. Densidad estratégica: MUY ALTA.**

### L1 — Las 6 Capas de la IA (iceberg) (#30) — ver D8

### L2 — 9 AI Skills to Master in 2026 (#43)

**Fuente:** LuMay AI
**Lote:** 6

**Contenido:**
- Diagrama radial con AI en centro y 9 ramas

**1. LLM Evaluation & Management** — Tools: **Helicone, TruLens, PromptLayer**
**2. Prompt Engineering** — Tools: ChatGPT, Claude, Gemini
**3. AI Workflow Automation** — Tools: **Zapier, Make, n8n** ⭐
**4. AI Agents** — Tools: **CrewAI, AutoGen, LangGraph** ⭐
**5. Retrieval-Augmented Generation (RAG)** — Tools: **LangChain, Vectara, LlamaIndex** ⭐
**6. Fine-Tuning and Custom GPTs** — Tools: **Cohere, Hugging Face, OpenAI GPT Builder**
**7. Multimodal AI** — Tools: GPT-4, Grok, Gemini
**8. AI Video Generation** — Tools: Runway, Pika, OpusClip
**9. AI Tool Stacking** — Tools: Notion, Zapier, ClickUp

**Tecnologías:** **Ecosistema completo AI**: Helicone, TruLens, PromptLayer, Zapier, Make, n8n, CrewAI, AutoGen, LangGraph, LangChain, Vectara, LlamaIndex, Cohere, Hugging Face, OpenAI GPT Builder, Runway, Pika, OpusClip, Notion, ClickUp

### L3 — IA Generativa (#59)

**Fuente:** naiker.codes
**Lote:** 8

**Contenido:**
- IA capaz de generar contenido nuevo y original a partir de patrones aprendidos
- "No solo entiende información, también puede crearla"
- 5 pasos: entrena → aprende patrones → genera → refina → entrega
- "La calidad depende de los datos, el modelo y el prompt"
- ¿Qué puede generar?: Texto, Imágenes, Audio, Video
- ¿Qué lo hace posible?: Modelos lenguaje (GPT), Redes neuronales, Grandes datos
- Ejemplos populares: ChatGPT, Midjourney, DALL-E, Suno
- "La IA generativa NO reemplaza a las personas, MULTIPLICA lo que podemos crear"

**Tecnologías:** ChatGPT, Midjourney, DALL-E, Suno

### L4 — AI Agents canónico (#60)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 8

**Contenido:**
- "La nueva generación de inteligencias artificiales"
- AI Agent = IA autónoma que percibe entorno, toma decisiones, usa herramientas, ejecuta acciones
- "No solo responde, actúa y resuelve"
- **Ciclo continuo en 5 pasos:** Percibe → Piensa → Decide → Actúa → Aprende
- **5 COMPONENTES CLAVE:**
  1. **Modelo de IA** (el cerebro)
  2. **Herramientas** (APIs, buscadores, código, calculadoras, funciones, BD)
  3. **Memoria** (mantener contexto, aprender)
  4. **Objetivos** (metas claras)
  5. **Guardrails** (reglas, límites, filtros) ⭐
- Ejemplos: ChatGPT Agent, Auto-GPT, Claude Agent, Copilot Agent
- Dónde se usan: empresas/productividad, e-commerce/marketing, educación, **salud y análisis datos**, finanzas/trading, **desarrollo y DevOps**
- "Los AI Agents no son el futuro, SON EL PRESENTE"

**Tecnologías:** ChatGPT Agent, Auto-GPT, Claude Agent, Copilot Agent

### L5 — RAG (Retrieval-Augmented Generation) (#65)

**Fuente:** naiker.codes
**Lote:** 8

**Contenido:**
- **RAG = Retrieval-Augmented Generation (Recuperación + Generación Aumentada)**
- "Cómo las IA ahora pueden buscar información real"
- "En lugar de responder solo con lo que 'sabe' el modelo, busca en fuentes externas"
- "Respuestas más precisas, actualizadas y confiables"
- 5 pasos: pregunta usuario → recuperación → aumento contexto → generación → respuesta
- "RAG permite que la IA use información real en tiempo real para responder mejor"
- **Arquitectura típica:**
  - Fuentes información (PDF, TXT, DOCX, web, BD, APIs)
  - Ingesta y embeddings
  - Base vectorial (índice)
  - Recuperación semántica
  - Generación aumentada
  - Respuesta final
- Por qué importante:
  - Respuestas basadas info real/actualizada
  - **Reduce alucinaciones**
  - **Permite usar conocimiento privado/empresa**
  - Ideal chatbots/asistentes/agentes
  - Escalable, flexible, fácil mantener
- Casos uso: chatbots soporte, asistentes legales/médicos, búsqueda BD conocimiento, **análisis docs/contratos**, educación/tutoring, investigación
- Ejemplos: Chatbot corporativo, Asistente legal, IA investigación, Asistente médico
- Componentes: Documentos, Embeddings (modelos), Base vectorial (Vector DB), Retriever, Modelo lenguaje (LLM), Generación
- **HERRAMIENTAS:**
  - **LangChain**
  - **LlamaIndex**
  - **Pinecone**
  - **Weaviate**
  - **Chroma**
  - **Milvus**

**Tecnologías:** LangChain, LlamaIndex, Pinecone, Weaviate, Chroma, Milvus, embeddings, Vector DBs

### L6 — LLM vs RAG vs AI Agent vs Agentic AI (#79)

**Fuente:** No identificado (tabla extensa)
**Lote:** 10

**Contenido:**
- Tabla maestra que separa 4 categorías
- **LLM:** smart text generator. Architecture: pregunta → AI brain → answer. Components: one AI model. Use: writing emails, posts. Tool integration: works alone. Memory: forgets after chat. Cost: cheapest. Implementation: hours. Examples: ChatGPT, Jasper, Copy.ai
- **RAG:** AI that searches docs. Architecture: pregunta → searches files → reads → writes answer. Components: AI + searchable library. Tool: reads docs, no actions. Memory: looks up fresh, no recall. Cost: medium. Implementation: 1-3 days. Examples: Perplexity, company chatbots
- **AI Agent:** AI helper that plans, uses tools. Architecture: goal → plan → tools → checks → adjusts → finishes. Components: brain + tools (search, calculator, file). Tool: web search, sheets, email. Memory: remembers in earlier steps. Cost: more expensive. Implementation: 3-5 days. Examples: AutoGPT, coding assistants
- **Agentic AI:** **team of AI workers** with different jobs. Architecture: goal → manager assigns → researcher AI → writer AI → reviewer AI → team delivers. Components: multiple workers + shared memory + manager. Tool: each member uses tools needed. **Memory: whole team shares info.** Automation: **runs entire projects start to finish**. Cost: **most expensive**. Implementation: **1-2 weeks or more**. Examples: **Microsoft AutoGen, CrewAI, team-based AI systems**
- 14 dimensiones de comparación detalladas

**Tecnologías:** ChatGPT/Jasper/Copy.ai (LLM), Perplexity (RAG), AutoGPT (Agent), AutoGen/CrewAI (Agentic)

### L7 — Hermes Agent complete guide visual (#51)

**Fuente:** Nainsi Dwivedi
**Lote:** 7

**Contenido:**
- "The self-improving AI agent that learns, remembers, and works for you 24/7"
- 3 atributos: Learns & Improves, Remembers Everything (three-tier memory), Works 24/7

**1. WHAT IS HERMES AGENT?**
- "Autonomous AI agent with built-in learning loop"
- 6 capacidades: Self-Evolving Skills, Three-Tier Memory, GEPA Optimization, Runs Anywhere (Local/Docker/SSH/Modal/Daytona/Singularity), Multi-Model Support (OpenRouter/OpenAI/Claude/Gemini/Llama/Local), Multiple Platforms (CLI/Telegram/Discord/Slack/WhatsApp/20+)
- "Hermes packages a gateway around a learning agent. OpenClaw packages an agent around a messaging gateway." ⭐ CITA CLAVE

**2. HOW IT'S BUILT**
- Everything flows through one core: AIAgent class
- Flujo: Build System Prompt → Check Compression → API Call (Interruptible) → Execute Tools → Loop (Up to 90 Turns)
- 6 Terminal Backends, Universal Model Support (200+ models), 90-Turn Safety Cap

**3. BEFORE MEMORY: WHO IS THE AGENT?**
- SOUL.md define identity, tone, core principles. First in system prompt (Slot #1)
- "Without identity, every agent feels the same. SOUL.md makes each agent uniquely yours"

**4. THE MEMORY SYSTEM: THREE TIERS** ⭐⭐⭐
- **TIER 1: Core Memory (Always in Context)** — MEMORY.md (2,200 chars) + USER.md (1,375 chars). Fast/Tiny/Essential
- **TIER 2: Session Search (FTS5)** — Full-text search across all past conversations with LLM summarization. Searchable/Unlimited/On-Demand
- **TIER 3: External Memory Providers** — 8 pluggable providers: **Notion, Obsidian, Roam, MongoDB, Qdrant, Redis, Zep, Chroma**. Deep/Persistent/Synced
- "Critical facts in Tier 1. Everything else searchable. Deep memory optional"

**5. SELF-EVOLVING SKILLS**
- Skills are Markdown + YAML
- Progressive Disclosure: Level 0 (names+desc ~3k tokens), Level 1 (full skill on demand), Level 2 (drill references)
- Self-Improvement Loop: Solve → Save as skill → Reuse → Get better
- The Curator: Garbage collection. Auto-archives stale. Never auto-deletes.

**6. GEPA: EVOLVING SKILLS OFFLINE** ⭐
- "Genetic-Pareto Prompt Evolution using execution traces"
- 6 pasos: Read Current Skill → Generate Dataset → Run GEPA Optimizer → Evaluate Candidates → Apply Constraints → PR with Best Variant
- Why GEPA? Agents self-rate poorly, prevents skill regression, offline optimization no runtime cost, PR-based safe/reviewable/reversible
- "No GPU required. Cost: $2-10 per run. Published at ICLR 2026"

**7. GETTING STARTED**
- Install: `curl -fsSL https://raw.githubusercontent.com/nousresearch/hermes-agent/main/scripts/install.sh | bash`
- Setup Wizard: `hermes setup`, Start: `hermes`, Connect Telegram: bot token via @BotFather
- What lives in `~/.hermes/`: SOUL.md, memory/, skills/, sessions/, state.db (SQLite+FTS5), cron/, config.yaml, .env

**8. GOING FROM 1 TO 10 AGENTS**
- Profiles = fully isolated agents
- Flow: Create Profiles → Add Telegram Bots → Define SOUL.md → Schedule Work → Let Them Work
- Example Team: Designer (Pixel) · Programmer (Neo) · Researcher (Pulse)

**9. CUSTOMIZING YOUR AGENTS**
- Programmer: routes execution via Claude Code CLI
- Designer: teach visual style with reference images, Nano Banana via OpenRouter
- Researcher: daily ArXiv digest, GitHub+News+Papers+Social Pulse, Perplexity+Tavily+Exa

**10. CRON: SCHEDULING MADE SIMPLE**
- Describe in English. Hermes handles schedule
- One-shot, Recurring, Cron Expressions, With Nudges, Chained Jobs

**Tecnologías:** Hermes Agent, Python 3.11+, SQLite+FTS5, Notion, Obsidian, Roam, MongoDB, Qdrant, Redis, Zep, Chroma, OpenRouter, Claude Code CLI, Perplexity, Tavily, Exa, GEPA

### L8 — Anatomía de una Carpeta Claude (#86)

**Fuente:** Anthropic / Claude Cowork (Opus 4.6)
**Lote:** 11

**Contenido:**
- "La carpeta que reemplazó mis prompts"
- **CLAUDE COWORK/** — estructura de 6 secciones:
  1. **SOBRE MÍ/**
     - `about-me.md`
     - `anti-ai-writing-style.md`
     - "Quién eres. Cómo escribes. Qué nunca dirías. El 80% de este archivo debe ser lo que rechazas. **Sabor = límites.**"
  2. **PROYECTOS/**
     - `[una subcarpeta por proyecto]/` con `brief.md`, `referencias/`, `borradores/`
     - "Claude lee todo esto antes de empezar"
  3. **PLANTILLAS/**
     - "El patrón, no el contenido. Claude lo estudia antes de crear cualquier cosa"
  4. **SALIDAS DE CLAUDE/**
     - "La única carpeta en la que Claude escribe"
  5. **INSTRUCCIONES GLOBALES/**
     - "Se configura una vez, se ejecuta siempre. Le indicas a Claude cómo comportarse. Nunca vuelves a escribirlo"
  6. **EL ÚNICO PROMPT**
     - "Quiero [TAREA] para que [CRITERIO DE ÉXITO]"
     - "El 80% de mis chats empiezan así. Claude te hace las preguntas"
- **Cita clave:** "Cuanto más contexto le des a través de archivos, menos prompts necesitas"

**Tecnologías:** Claude (Opus 4.6), Anthropic ecosistema

---

## 15. Bucket M — Arquitectura de Sistemas

**3 infografías. Densidad estratégica: MUY ALTA.**

### M1 — Monolítica vs Microservicios (#41)

**Fuente:** naiker.codes
**Lote:** 5

**Contenido:**
- "Dos formas completamente distintas de construir software"
- "No hay una mejor que otra, depende del proyecto, equipo y objetivos"
- **MONOLÍTICA:** toda la app construida como único bloque que se despliega junto. Frontend + Lógica Negocio + BD Acceso + Auth + Notif. BD única.
- **MICROSERVICIOS:** app dividida en servicios pequeños, independientes, especializados. Servicios separados de Usuarios/Pedidos/Pagos/Notificaciones/Inventario. Cada uno con su BD.
- **Tabla comparativa 7 dimensiones:** Despliegue, **Escalabilidad**, Desarrollo, Tecnología, Tolerancia fallos, Mantenimiento, Rendimiento
- Ventajas/Desventajas de cada uno
- **CUÁNDO USAR CADA UNA:**
  - **MONOLÍTICA SI:** proyecto pequeño/mediano, equipo pequeño, lanzar rápido (MVP), dominio simple
  - **MICROSERVICIOS SI:** proyecto grande/crecerá, escalar partes específicas, equipos múltiples paralelos, alta disponibilidad/resilencia
- **INFRAESTRUCTURA TÍPICA:**
  - Monolítica: 1 servidor, 1 app, 1 BD
  - Microservicios: múltiples servicios, **contenedores (Docker)**, **orquestación (Kubernetes)**, BDs distribuidas
- **TECNOLOGÍAS COMUNES:**
  - **MONOLÍTICA:** Java + Spring Boot, .NET + ASP.NET, PHP + Laravel, Node.js + Express, Ruby on Rails
  - **MICROSERVICIOS:** Docker, Kubernetes, API Gateway (Kong, NGINX), Mensajería (RabbitMQ, Kafka), Service Mesh (Istio)
- Consideraciones críticas:
  - No dividir por dividir
  - Diseño basado en dominio del negocio (**DDD**)
  - **Monitoreo, logging, trazabilidad clave**
  - **Cultura DevOps y automatización esenciales**
- "Elige la que resuellva tu problema, no la que está de moda"

**Tecnologías:** Docker, Kubernetes, Java+Spring, .NET, PHP+Laravel, Node.js+Express, Ruby on Rails, Kong, NGINX, RabbitMQ, Kafka, Istio, DDD

### M2 — Clean Architecture (#49) — ver G2

### M3 — Agentic Orchestration Layer (McKinsey) (#81)

**Fuente:** McKinsey & Company
**Lote:** 10

**Contenido:**
- "The agentic orchestration layer directs workflows"
- "Agentic workflow, illustrative"
- Diagrama de 3 niveles:
  1. **Enterprise context** (alimenta orchestration + workforce) — "Information on enterprise context readily available, allowing agents to learn and adapt"
  2. **Agentic orchestration layer** (centro de control) — "Routes the right agents to tasks and provides right context"
  3. **Agentic workforce** — Múltiples Agents trabajando juntos
  4. **Toolbox and data connections** (base) — Conecta con: Legacy systems (ERP), Purpose-built solutions (forecasting), Data repository (data lake), Applications (email, web search)
- Validación enterprise del modelo agentic

**Tecnologías:** Arquitectura conceptual McKinsey

---

## 16. Bucket N — Infraestructura AI

**3 infografías. Densidad estratégica: MUY ALTA.**

### N1 — Local AI vs Cloud AI (#42)

**Fuente:** Lost in the Woods Digital
**Lote:** 6

**Contenido:**
- "Which is right for you? There is no 'best' option. Just what's best for you"
- **LOCAL AI:** "Run AI on your own hardware. Yours. Private. No Limits."
- **CLOUD AI:** "Run AI on remote servers. Powerful. Accessible. Anywhere."
- **Tabla comparativa 8 dimensiones:**
  - Cost: One-time hardware vs Pay-as-you-go
  - Privacy: 100% private vs Data leaves your control
  - Internet: Works offline vs Requires internet
  - Performance: Depends on hardware vs Extremely powerful
  - Customization: Full control vs Limited
  - Model Access: Use what you want vs Limited/locked
  - Scalability: Limited by hardware vs Instant scalability
  - Best for: Privacy-focused/tinkerers/developers vs Beginners/businesses/fast results
- **LOCAL AI = FREEDOM** (you own/control/yours)
- **CLOUD AI = CONVENIENCE** (access/scale/easy)

**Tecnologías:** Conceptual

### N2 — AI Infrastructure Master Tree (#57)

**Fuente:** No identificado (estilo tarjeta moderna)
**Lote:** 7

**Contenido:**
- "Most people think AI is just a model. The real moat is the infrastructure stack around it"
- **9 CAPAS:**

**01 COMPUTE LAYER**
- GPUs: H100, B200, MI300X, TPU v5
- Inference Engines: vLLM, TensorRT-LLM, **Ollama**, llama.cpp
- Optimization: Quantization, KV Cache, Speculative Decoding, Flash Attention

**02 MODEL LAYER**
- Frontier: GPT-4.1, **Claude**, Gemini, DeepSeek
- Open: Llama, Qwen, Mistral, Gemma
- Fine-Tuning: LoRA, RLHF, DPO, Synthetic Data

**03 DATA LAYER** ⭐
- Data Pipelines, Chunking, Embeddings, **Vector Databases**, **Knowledge Graphs**, Real-Time Streams

**04 AGENT RUNTIME** ⭐
- **LangGraph, CrewAI, OpenAI Agents SDK, AutoGen, MCP, Workflow Engines**

**05 TOOLING LAYER**
- Web Search, Browser Use, Code Execution, APIs, Databases, File Systems

**06 DEPLOYMENT LAYER** ⭐
- **Docker, Kubernetes, Serverless GPUs, Edge Inference, Cloudflare Workers, HuggingFace Spaces**

**07 OBSERVABILITY**
- Logs, Traces, Evaluations, **Hallucination Detection**, **Latency Tracking**, **Cost Monitoring**

**08 SECURITY LAYER** ⭐
- **Sandboxing, Permission Systems, Secret Management, Guardrails, Human Approval, Jailbreak Protection**

**09 THE FUTURE**
- AI Browsers, **AI Operating Systems** ⭐, Autonomous Research Labs, AI Employees, One-Person Unicorns

- Cita: "AI is evolving from tools to teams to ecosystems. Build the stack. Own the future"

**Tecnologías:** Stack completo de IA empresarial

### N3 — Hermes Agent complete guide (#51) — ver L7

---

## 17. Bucket O — Paradigmas de Programación

**1 infografía. Densidad estratégica: MEDIA.**

### O1 — Programación Reactiva (#47)

**Fuente:** naiker.codes (chalkboard)
**Lote:** 6

**Contenido:**
- "Programar reaccionando a eventos"
- Paradigma basado en flujos de datos asíncronos y propagación de cambios
- "En lugar de ejecutar línea por línea, tu aplicación reacciona a eventos y datos que cambian en tiempo real"
- 5 pasos: fuente eventos → stream/observable → operadores → suscripción → reacción
- Características clave:
  - Basada en flujos de datos
  - Asíncrona y no bloqueante
  - Responde a eventos tiempo real
  - Tolerante a fallos
  - Escalable y modular
  - Menos código, más declarativo
- Dónde se usa:
  - **Frontend:** interfaces reactivas, búsqueda tiempo real, formularios dinámicos, notificaciones, animaciones
  - **Backend:** APIs tiempo real, procesamiento streams, **microservicios reactivos**, sistemas mensajería, IoT
- Reactivo vs Imperativo:
  - Imperativo: pides → esperas → procesas → otra cosa
  - Reactivo: te suscribes → recibes → reaccionas → todo fluye
- **Ejemplo RxJS (JavaScript):**
  ```javascript
  import { fromEvent } from 'rxjs';
  import { map, filter } from 'rxjs/operators';
  fromEvent(document, 'click')
    .pipe(map(event => event.clientX), filter(x => x > 300))
    .subscribe(x => console.log('Clic en X:', x));
  ```
- **Librerías populares:**
  - **RxJS** (JavaScript)
  - **Project Reactor** (Java)
  - **Akka Streams** (Scala/Java)
  - **Kotlin Flow**
  - **Swift Combine** (iOS)
- Ejemplos reales: Netflix, Spotify, Mercado Libre, Google Maps

**Tecnologías:** RxJS, Project Reactor, Akka Streams, Kotlin Flow, Swift Combine

---

## 18. Bucket P — Streaming / Event-Driven

**2 infografías. Densidad estratégica: ALTA.**

### P1 — Event Sourcing (#50) — ver E2
### P2 — Streaming de Datos (#54) — ver E3

---

## 19. Bucket Q — Cloud / Deployment / Serverless

**1 infografía. Densidad estratégica: ALTA.**

### Q1 — Serverless (#61)

**Fuente:** naiker.codes
**Lote:** 8

**Contenido:**
- "Programar sin administrar servidores. Ejecuta tu código en la nube sin preocuparte por la infraestructura"
- Modelo donde escribes/ejecutas código sin aprovisionar ni administrar servidores
- Proveedor cloud se encarga de infraestructura, escalado, disponibilidad, mantenimiento
- "No significa que no hay servidores, significa que no los gestionas tú"
- 5 pasos: despliegas función → se activa por evento (HTTP/archivo/mensaje/clic/IoT) → se ejecuta código → devuelve resultado → escala y se detiene solo
- "Paga solo por las ejecuciones y el tiempo de cómputo utilizado"
- **Arquitectura típica:**
  - FUENTES EVENTOS: HTTP/HTTPS, Archivos (S3/GCS), BD, Colas/Mensajes, IoT/Dispositivos, Programaciones (Cron)
  - FUNCIONES SERVERLESS: código se ejecuta independiente y bajo demanda
  - SERVICIOS GESTIONADOS: BD, Almacenamiento, Auth, Notificaciones, APIs
  - RESULTADOS/CLIENTES: Apps web, móviles, APIs, Dashboards, Sistemas externos
- **PLATAFORMAS SERVERLESS POR PROVIDER:**
  - **AWS:** Lambda, API Gateway, DynamoDB, S3, EventBridge
  - **Google Cloud:** Cloud Functions, Cloud Run, Firestore, Pub/Sub, Cloud Storage
  - **Azure:** Azure Functions, Azure Static Web Apps, Cosmos DB, Event Grid, Blob Storage
  - **Edge/CDN:** **Cloudflare Workers, Vercel Functions, Netlify Functions, Fastly Compute@Edge**
- Características clave: funciones event-driven, ejecuciones ephemeras, sin estado (Stateless), concurrencia masiva, integración nativa, monitoreo integrado
- Consideraciones: ejecución con tiempo límite, no ideal procesos largos, dependencia proveedor cloud
- Ideal para: Microservicios, APIs/Webhooks, Eventos/colas, Procesamiento datos, Prototipos/MVPs

**Tecnologías:** AWS Lambda/API Gateway/DynamoDB/S3/EventBridge, GCP Cloud Functions/Run/Firestore/Pub-Sub/Storage, Azure Functions/Static Web Apps/Cosmos DB, Cloudflare Workers, Vercel Functions, Netlify Functions, Fastly Compute@Edge

---

## 20. Bucket R — Edge / Distributed Computing

**1 infografía. Densidad estratégica: BAJA-MEDIA.**

### R1 — Edge Computing (#63)

**Fuente:** naiker.codes
**Lote:** 8

**Contenido:**
- "La nube ahora está más cerca que nunca"
- Modelo computación distribuida que lleva procesamiento/análisis cerca del dispositivo
- "Menos distancia = Menor latencia = Mejores experiencias"
- 5 pasos: generación datos → procesamiento en borde (EDGE) → decisión inmediata → envío a nube (opcional) → acciones/retroalimentación
- EDGE vs CLOUD:
  - Cloud (centralizado): centros de datos remotos, mayor latencia, depende internet, más ancho banda, análisis masivo
  - Edge (distribuido): procesamiento cerca usuario, menor latencia, funciona con conexión limitada, menos ancho banda, ideal tiempo real
- Arquitectura: Dispositivos borde → Edge Gateway/Nodo Local → Red Local (5G, Wi-Fi 6, LAN) → Nube Central (opcional) → Apps/usuarios
- Casos uso: ciudades inteligentes, vehículos autónomos, fábricas industriales, salud conectada, retail inteligente, agricultura precisión, video vigilancia
- **TECNOLOGÍAS CLAVE:**
  - **Contenedores (Docker)**
  - **Microservicios**
  - **Kubernetes (K3s)** ⭐ — versión light para edge
  - **IA en el borde (TinyML)** ⭐
  - **Redes 5G y Wi-Fi 6**
  - **Protocolos ligeros (MQTT, CoAP)**

**Tecnologías:** Docker, K3s, TinyML, 5G, Wi-Fi 6, MQTT, CoAP

---

## 21. Bucket S — Observability

**1 infografía. Densidad estratégica: MUY ALTA.**

### S1 — Observability completa (#69)

**Fuente:** naiker.codes
**Lote:** 9

**Contenido:**
- "Cómo las empresas detectan problemas antes de que exploten"
- "Visibilidad completa del estado interno de un sistema"
- Capacidad de entender el estado interno a partir de datos que genera
- "Va más allá del monitoreo tradicional: permite descubrir la **causa raíz**"
- "No se trata solo de saber QUÉ falló, sino POR QUÉ y DÓNDE ocurrió"
- 5 pasos: se generan datos → recolectan (agentes/integraciones) → correlacionan → analizan (tiempo real, anomalías) → actúa (alertas)
- **3 PILARES DE OBSERVABILITY:**
  - **LOGS (registros):** eventos discretos. Ejemplos: errores, advertencias, eventos negocio, auditorías
  - **MÉTRICAS:** datos numéricos agregados. Ejemplos: CPU/memoria/disco, RPS/latencia/throughput, uso servicios, tasa errores
  - **TRACES (trazas):** rastreo peticiones a través de servicios. Ejemplos: tiempo respuesta servicio, cuellos botella, dependencias fallidas
- Por qué importante:
  - Detecta problemas antes de afectar usuarios
  - **Reduce MTTD (Mean Time To Detection)**
  - **Acelera MTTR (Mean Time To Resolution)**
  - Mejora UX
  - Visibilidad sistemas distribuidos
  - Decisiones basadas datos reales
- "Sin observability, estás volando a ciegas"
- Arquitectura: Fuentes (Apps/Infra/Contenedores/Cloud) → Colección (agentes/exporters/sidecars) → Procesamiento/Almacenamiento → Visualización/Alertas → Acción
- **HERRAMIENTAS POPULARES POR CATEGORÍA:**
  - **LOGS:** Grafana Loki, ELK Stack, Splunk, Datadog Logs
  - **MÉTRICAS:** Prometheus, Grafana, Datadog Metrics, New Relic
  - **TRACES:** Jaeger, Zipkin, AWS X-Ray, Datadog APM
  - **PLATAFORMAS COMPLETAS:** Datadog, New Relic, Dynatrace, Honeycomb
- Buenas prácticas: instrumenta desde inicio, centraliza datos, **usa estándares abiertos (OpenTelemetry)** ⭐, dashboards útiles/simples, alertas inteligentes (sin ruido), revisa y mejora

**Tecnologías:** Grafana Loki, ELK Stack, Splunk, Prometheus, Grafana, Datadog, New Relic, Jaeger, Zipkin, AWS X-Ray, Dynatrace, Honeycomb, **OpenTelemetry** ⭐

---

## 22. Bucket T — Workflow Automation Real

**1 infografía. Densidad estratégica: ALTA.**

### T1 — n8n LinkedIn Scraper + Cold Email Engine (#72)

**Fuente:** No identificado (n8n workflow real)
**Lote:** 9

**Contenido:**
- "AI-Powered LinkedIn Job Scraper & Cold Email Lead Engine"
- "Full n8n Workflow"
- 6 etapas:
  1. **INPUT & JOB SEARCH:** Google Sheets → Set/Filter → Build Search Queries → Loop Over Queries → HTTP Request (LinkedIn)
  2. **SCRAPE JOBS & EXTRACT DATA:** HTML Extract → Split In Batches → Extract Job Data → Merge Results → Remove Duplicates
  3. **GET COMPANY & PEOPLE DETAILS:** Extract Company Info → Find People (LinkedIn) → Extract People Data → Merge → Filter Ideal Prospects
  4. **ENRICH & FIND EMAILS:** Enrich Company (Clearbit) → Enrich Person (Clearbit) → Find Email (Snov.io/Hunter) → Validate → Filter Valid
  5. **GENERATE PERSONALIZED COLD EMAILS:** Get Email Templates → AI Generate (OpenAI) → Set Email Variables → Add to Campaign → Update Lead Status
  6. **SEND & TRACK EMAILS:** Send Email (SMTP/Resend) → Wait/Delay → Check Email Activity → Update Lead → Log to Google Sheets/CRM
- **INTEGRATIONS USED:** LinkedIn, Google Sheets, Clearbit, Snov.io/Hunter, OpenAI, SMTP/Resend, n8n
- OUTPUTS: Job Listings, Companies Data, People/Decision Makers, Verified Emails, Personalized Cold Emails, Email Tracking

**Tecnologías:** n8n, LinkedIn API, Google Sheets, Clearbit, Snov.io, Hunter, OpenAI API, SMTP, Resend

---

## 23. Bucket U — Procesamiento de Datos Masivos

**1 infografía. Densidad estratégica: MEDIA (depende de lenguaje elegido).**

### U1 — Polars vs Pandas (#74)

**Fuente:** naiker.codes
**Lote:** 10

**Contenido:**
- "¿Por qué Polars está reemplazando a Pandas?"
- "La nueva librería que está acelerando el análisis de datos masivos"
- Polars = librería DataFrames **escrita en Rust con bindings Python**
- "Polars combina la facilidad de uso de Pandas con el rendimiento de herramientas Big Data"
- **5 razones:**
  1. **Rendimiento extremo** — hasta 10x-100x más rápida que Pandas
  2. **Paralelismo nativo** — aprovecha todos los núcleos CPU automáticamente
  3. **Menor uso de memoria** — estructuras eficientes + lazy evaluation
  4. **API moderna y expresiva**
  5. **Ecosistema en crecimiento** — compatibilidad PyArrow, SQL
- **Tabla comparativa Polars vs Pandas:**
  - Lenguaje interno: **Rust** vs Python/C
  - Velocidad: Muy alta (10x-100x) vs Media
  - Paralelismo: Nativo (multihilo) vs Limitado
  - Uso memoria: Bajo vs Alto
  - Lazy Execution: **Sí (default)** vs No (solo eager)
  - Big Data: Excelente vs Limitado
  - PyArrow: Total vs Parcial
  - Escalabilidad: Alta vs Media
- Ejemplo código Pandas vs Polars (filter + group_by + agg)
- ¿Por qué tan rápida?:
  1. Escrita en Rust
  2. Ejecución paralela
  3. Columnar por diseño (Apache Arrow)
  4. Lazy evaluation
  5. Optimizaciones avanzadas (predicate pushdown, projection pushdown)
- Dónde se usa: análisis datos gran escala, **ETL/ELT**, BI/dashboards, ML preprocesamiento, **log analytics/observabilidad**, finanzas/trading, ciencia datos
- Ecosistema:
  - Apache Arrow (estándar columnar)
  - API 100% Pythonic
  - SQL con Polars SQL
  - Parquet, IPC, CSV, JSON
  - Integración PyTorch, Scikit-learn, Streamlit
- Buenas prácticas: usa LazyFrame, selecciona solo columnas necesarias, filtra temprano, **usa Parquet para almacenamiento**, aprovecha paralelismo, mantén Polars actualizado

**Tecnologías:** Polars, Rust, Apache Arrow, PyArrow, Parquet, Python

---

## 24. Bucket V — Estrategia de Negocio y Moat

**1 infografía. Densidad estratégica: MÁXIMA.**

### V1 — El Moat: Flywheel B2B (#85)

**Fuente:** Screenshot de pantalla / contexto B2B SaaS
**Lote:** 11

**Contenido:**
- "El moat: el flywheel que nadie puede copiar"
- "Cada vuelta hace más profundo el moat. **El que entra tarde, no alcanza.**"
- Diagrama de flywheel de 4 cuadrantes:
  - **Distribución:** "Relaciones B2B construidas en años. **No se compran con capital.**"
  - **Data:** "**Outcome data propietaria acumulada en cada interacción.**"
  - **Modelos:** "Modelos entrenados con data real. **Mejoran solos con el tiempo.**"
  - **Outcomes:** "Resultados medibles que justifican precios premium y retención."
- **Es vista de estrategia de negocio**, no técnica
- Mapea PERFECTO con For3s OS:
  - Distribución: Brian López + red LATAM
  - Data: outcome data propietaria por cada workflow QA
  - Modelos: skills auto-evolving + agents mejoran con uso
  - Outcomes: métricas medibles (bugs evitados, tiempo ahorrado)

**Tecnologías:** Modelo de negocio B2B SaaS de IA

---

## 25. Bucket Ruido / Contexto

**4 infografías. Sin valor técnico nuevo.**

### Z1 — Screenshot de Facebook con post de Endpoint (#6) — Lote 1
- Contexto social, sin info técnica nueva
- naiker.codes en Facebook, 69 likes, 18 comentarios

### Z2 — REST API Methods (#56 repetido en #87) — ya cubierto en A7
- Aparece 2 veces, refuerza fundacionalidad

### Z3 — MCP (#66 repetido en #77) — ya cubierto en J7
- Aparece 2 veces, refuerza fundacionalidad

### Z4 — Transición ChatGPT→Claude (#84)

**Fuente:** ai._kid (Instagram)
**Lote:** 11

**Contenido:**
- Captura Instagram mostrando transición de workflow personal
- Tabla ANTES vs DESPUÉS:
  - ChatGPT → **Claude** (mejor razonamiento)
  - Cursor → **Claude Code** (perspectivas profundas)
  - Figma → **Claude Design** (diseño mejorado por IA)
  - n8n → **Claude Routine** (automatización inteligente)
- 165 likes, 77 compartidos
- "Hace 2 días"
- **Testimonial, no técnico**, pero confirma tendencia mercado: usuarios migrando a ecosistema Anthropic consolidado

---

## 26. Patrones macro emergentes del banco

### Patrón 1 — Stack TypeScript-first (predominante)

El banco está fuertemente orientado a **JavaScript/TypeScript + Node.js**:
- React, Vue, Angular (frontend)
- Node.js + Express (backend)
- JavaScript code samples en muchas infografías

**Pero también aparecen:**
- Python (BeautifulSoup, Django, Polars binding, scripts)
- Java/Spring Boot, .NET, PHP/Laravel, Ruby on Rails (alternativas monolíticas)
- C# (Blazor)
- Rust (Polars internamente)

### Patrón 2 — Anthropic / Claude ecosystem fuerte

Múltiples infografías centradas en:
- Claude Code (/goal, Project Structure, OS pixel art)
- Claude Skills (31 SMB skills)
- MCP (Model Context Protocol)
- Anatomía Carpeta Claude (Cowork)
- AI Agent cheat sheet con Claude
- Transición ChatGPT → Claude

**Implicación:** Brian consume sistemáticamente contenido del ecosistema Anthropic.

### Patrón 3 — Patrones de arquitectura clásicos

- Clean Architecture
- Monolítica vs Microservicios
- Event Sourcing + CQRS
- API Gateway
- Streaming / Reactive
- Edge Computing / Serverless

### Patrón 4 — Seguridad operacional fuerte

- JWT, Cookies (HttpOnly/SameSite/Secure)
- Hash functions (SHA-256, BLAKE3)
- Variables de entorno + Secret Managers
- DNS over HTTPS
- HTTPS everywhere
- Login completo con bcrypt/argon2

### Patrón 5 — AI-Native ecosystem completo

- LangChain, LlamaIndex (RAG)
- CrewAI, AutoGen, LangGraph (Agents)
- Helicone, TruLens, PromptLayer (Eval)
- Zapier, Make, n8n (Automation)
- MCP (Standard tools)
- Vector DBs (Pinecone, Weaviate, Milvus, Qdrant, Chroma)

### Patrón 6 — Repeticiones señalan fundacionalidad

- **MCP** aparece 2 veces (#66, #77)
- **REST API Methods** aparece 2 veces (#56, #87)
- **Endpoint** aparece en 2 contextos (#4, #6 screenshot Facebook)

### Patrón 7 — Estrategia de negocio explícita

- Moat / Flywheel B2B (#85) — pieza estratégica única
- McKinsey Agentic Orchestration (#81) — validación enterprise
- 31 Skills Claude SMB (#34) — patrón de productización

---

**Fin del banco completo de infografías.**

**Próximos pasos:**
- Ver [Banco_Diario_Mayo_2026.md](Banco_Diario_Mayo_2026.md) para los 3 docs históricos de Brian
- Ver [Banco_Filtro_Alineacion.md](Banco_Filtro_Alineacion.md) para qué se queda y qué se va contra el Grafo Maestro