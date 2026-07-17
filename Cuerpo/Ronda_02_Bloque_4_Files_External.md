# Ronda 2 — Bloque 4: Files & External Data

**Sub-documento detallado de R2 — Data Layer. Bloque 4 de 4 (ÚLTIMO).**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-01
**Estatus:** ✅ LOCKED (3/3 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema)
**Documento padre:** [Ronda_02_Data_Layer.md](Ronda_02_Data_Layer.md)
**Sesión:** 2026-06-01

> ⚠️ **CIERRE R2 COMPLETO:** Este bloque CIERRA Ronda 2 — Data Layer al 100% (20/20 sub-temas LOCKED).

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core
- 3.D — Equipo pequeño

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P4 — Encryption híbrida (LUKS + app-layer)
- mvp-scope §11 — Retención 12 meses

**Decisiones previas que afectan B4:**
- R1: Python 3.12 + asyncio (jobs backup)
- B1 1.1: PostgreSQL (pg_dump)
- B1 1.6: Event Sourcing + audit chain (debe backupearse)
- B2 2.5: Forgetting con archive (TTL backup)
- B3 3.2: Arq (jobs de backup automation)
- B3 3.4: Patterns async (CapacityLimiter para uploads R2)
- D-009: Despliegue LOCAL Linux (USB local primary)

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 4.1 — File storage](#3-sub-tema-41--file-storage)
4. [Sub-tema 4.2 — S3 provider](#4-sub-tema-42--s3-provider)
5. [Sub-tema 4.3 — Code repo access](#5-sub-tema-43--movido-a-r4-toolsmcp-d-010)
6. [Sub-tema 4.4 — Backup strategy](#6-sub-tema-44--backup-strategy)
7. [Stack final consolidado](#7-stack-final-consolidado)
8. [Cobertura del Grafo Maestro](#8-cobertura-del-grafo-maestro)
9. [Costo total v1 FINAL](#9-costo-total-v1-final)
10. [Exploraciones futuras NO adoptadas v1](#10-exploraciones-futuras-no-adoptadas-v1)
11. [Implicaciones en rondas siguientes (R3-R10)](#11-implicaciones-en-rondas-siguientes-r3-r10)
12. [Cierre R2 — Filosofía consolidada](#12-cierre-r2--filosofía-consolidada)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 4 — FILES & EXTERNAL DATA                             ║
║   3 sub-temas LOCKED el 2026-06-01                             ║
║                                                                ║
║   4.1 File storage     → Filesystem local + Postgres metadata  ║
║   4.2 S3 provider      → NO S3 v1 (defer a v2-v3)              ║
║   4.4 Backup strategy  → Local USB + Cloudflare R2 (3-2-1)     ║
║                                                                ║
║   ⏭️ 4.3 movido a R4 Tools/MCP (D-010 — Git wedge-specific)   ║
║                                                                ║
║   Servicios extra añadidos: 0 (R2 free tier free)              ║
║   Costo incremental B4: USD 0 (todo gratis para v1)             ║
║   Costo total v1 FINAL (R1+R2 + D-009): USD ~43/mes             ║
║   % techo Pilot Light: 3.7% (margen 96.3%)                      ║
║                                                                ║
║   ⭐ CIERRA R2 — DATA LAYER 100% (20/20 sub-temas LOCKED)       ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Aprovechar al máximo D-009 LOCAL + Cloudflare ecosystem ya en stack."
```

Las 3 decisiones convergen en patrones consistentes:

```
1. STORAGE LOCAL PRIMARY (4.1)
   → Filesystem local aprovecha 1 TB disco D-009
   → Postgres queda lean (solo metadata)
   → Streaming eficiente sin overhead

2. CLOUD OPCIONAL Y SECUNDARIO (4.2 + 4.4)
   → S3 primario: NO v1 (4.2)
   → S3 backup secundario: SÍ via Cloudflare R2 (4.4)
   → Compliance LOCAL preservado (cifrado pre-upload)

3. 3-2-1 BACKUP RULE (4.4)
   → 3 copias, 2 medios, 1 offsite
   → Compliance B2B enterprise ready
   → Free tier R2 cubre v1 sin costo

4. ENCRYPTION END-TO-END (P4 aplicado)
   → LUKS filesystem subyacente
   → age (modern crypto) para cloud uploads
   → Llave private OFFLINE

5. APROVECHAR ECOSYSTEM CLOUDFLARE
   → Tunnel D-009 + R2 backup = mismo provider
   → Cero costo recurring v1
   → Future-proof v2 sin migración
```

### Por qué esta filosofía importa

**Para Pilar 1 Seguridad:** Compliance B2B exige offsite backup. 3-2-1 rule + encryption end-to-end satisfacen requirements enterprise.

**Para D-009 LOCAL:** El backup local USB aprovecha hardware Brian. El cloud secundario protege contra worst case sin romper compliance LOCAL (cifrado pre-upload).

**Para Anclas:** Cero servicios extra de infra, costos free tier para v1, scope mínimo.

---

## 3. Sub-tema 4.1 — File storage

### Decisión LOCKED

```
Filesystem local + metadata Postgres
```

### Contexto

For3s OS necesita guardar **archivos binarios** (outputs del agente, exports, audit dumps) que NO son datos estructurados de tablas. Decisión: ¿dónde viven los archivos?

### Mapeo al Grafo Maestro

- **Pilar 1 Seguridad:** archivos sensibles necesitan P4 encryption + RBAC
- **Pilar 2 Escalabilidad:** filesystem escala con disco (1 TB)
- **Nodo 8 Amígdala:** policy engine decide acceso a files
- **Audit chain:** cada acceso a archivo sensible → audit

### Candidatos evaluados

```
A) BLOB en PostgreSQL           ⚠️ Infla Postgres, backup pesado
B) Filesystem local + metadata   ✅ ELEGIDO
C) S3-compatible (cloud/MinIO)   ❌ Rompe D-009 LOCAL / overkill v1
D) Híbrido BLOB chicos + FS      ❌ Sobre-ingeniería v1
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A: BLOB   │B: FS     │C: S3     │D: Híbr.  │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Open-source              │  ✅✅✅   │  ✅✅✅   │  ⚠️/N/A  │  ✅✅✅   │
│ Costo v1 mensual         │   $0     │   $0     │  $0-2    │   $0     │
│ Servicios extra          │    0     │    0     │   +1     │    0     │
│ Backup unificado         │  ✅✅✅   │  ⚠️     │   ❌    │   ⚠️     │
│ Streaming eficiente      │   ⚠️     │  ✅✅✅   │  ✅✅✅   │  ✅✅    │
│ Postgres lean            │   ❌    │  ✅✅✅   │  ✅✅✅   │  ✅✅    │
│ Compliance D-009 LOCAL   │  ✅✅✅   │  ✅✅✅   │  ⚠️     │  ✅✅    │
│ Match D-009 LOCAL        │  ✅✅    │  ✅✅✅   │   ❌    │  ✅✅    │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **Alineación PERFECTA con D-009 LOCAL** — aprovecha 1 TB disco
2. **Postgres lean** — backup pg_dump rápido
3. **Streaming eficiente** — FastAPI FileResponse usa sendfile()
4. **Escala hasta v3** sin refactor (1 TB cabe años)
5. **Encryption híbrida P4** — LUKS + app-layer en archivos sensibles
6. **Workspace isolation** por filesystem permissions
7. **SHA256 hash** detecta corrupción

### Configuración LOCKED v1

**Ubicación:**
```
/var/lib/for3s/files/
├── wks_A/
│   ├── outputs/         → 2026/06/01/<uuid>-report.md
│   ├── exports/         → 2026/06/02/<uuid>-full-export.json
│   └── audit-dumps/     → 2026/05/<uuid>-monthly.json.gpg
├── wks_B/
└── wks_C/
```

**Permisos:**
- Dueño: `for3s_app:for3s_app`
- Modo: `0700` (solo dueño lee/escribe)
- LUKS encriptación de disco subyacente (P4 filesystem layer)

**Tabla Postgres (metadata):**

```sql
CREATE TABLE wks_X.file_metadata (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    episode_id      UUID,
    file_type       TEXT NOT NULL,
    filename        TEXT NOT NULL,
    mime_type       TEXT NOT NULL,
    relative_path   TEXT NOT NULL,
    size_bytes      BIGINT NOT NULL,
    sha256_hash     BYTEA NOT NULL,
    encryption_kid  TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    deleted_at      TIMESTAMPTZ,
    expires_at      TIMESTAMPTZ  -- TTL opcional
);
```

**Encryption (P4 híbrido):**
- **Capa 1 (LUKS):** disco completo cifrado
- **Capa 2 (app-layer AES-GCM):** archivos críticos cifrados ANTES de escribir
  - `file_type IN ('audit_dump', 'export', 'sensitive_output')`
- `encryption_kid` identifica la key usada

**Estructura módulo:**

```
for3s_os/infrastructure/files.py:
   • FileStorage.store()      → saga pattern (FS + DB)
   • FileStorage.retrieve()    → stream con RBAC check
   • FileStorage.delete()      → soft delete primero
   • OrphanedFilesWorker       → cleanup nightly vía Arq
```

**Meta-audit obligatorio:**
- Cada operación file → `INSERT shared.audit_events`
- `action: 'file:store' / 'file:retrieve' / 'file:delete'`
- Payload: `{ workspace_id, file_id, file_type, size_bytes, actor_id, sha256_hash }`

### Path futuro

```
v1: Filesystem local + metadata Postgres
v2: añadir lifecycle policies + compression si necesario
v3: evaluar S3/MinIO si >100 GB o cliente exige escala
```

---

## 4. Sub-tema 4.2 — S3 provider

### Decisión LOCKED

```
NO S3 en v1 — diferir a 4.4 si solo backup
```

### Contexto

Con 4.1 LOCKED (filesystem local), la pregunta real es: ¿usamos S3-compatible para algo (backup secundario, sharing, escala futura)?

### Mapeo al Grafo Maestro

- **Pilar 1 Seguridad:** si cloud, datos salen del LOCAL (compliance pregunta)
- **Pilar 2 Escalabilidad:** S3 escala infinito (relevante v3)
- **Backup strategy:** 4.4 podría usar S3 como destino offsite

### Candidatos evaluados

```
A) NO S3 v1 (defer a 4.4)            ✅ ELEGIDO
B) Cloudflare R2 solo backup         (decisión real en 4.4)
C) MinIO self-hosted                  ❌ Sobre-ingeniería v1
```

### Razones de la decisión

1. **Alineación PERFECTA con D-009 LOCAL** — cero compromiso compliance
2. **Cero servicios extra** — respeta 3.D al máximo
3. **Filesystem local (4.1) basta v1** — volumen ~3 GB es trivial
4. **Decisión backup va en 4.4** — lugar correcto para discusión
5. **Velocidad de desarrollo** — sin setup S3 v1
6. **Migración path planeado** — refactor v2-v3 si necesario

### Triggers para activar S3 en v2-v3

**v2 (Cloudflare R2 primer opción):**
- Decisión 4.4 lockea backup cloud secundario
- Cliente pide export archivos >100 MB
- Disco USB backup fail rate >5%

**v3 (evaluar AWS S3 / Backblaze B2):**
- Volumen archivos >100 GB sostenido
- Cliente enterprise exige replicación multi-region
- Necesidad CDN para assets públicos
- Pre-signed URLs para reducir bandwidth servidor

### Migración path

```
Si v2 activa R2 (solo backup):
1. Setup cuenta R2 (~30 min, Cloudflare ya en stack)
2. Añadir aioboto3 SDK
3. Backup script extiende con upload R2
4. NO TOCA storage primary (filesystem local)

Si v3 migra primary a S3:
1. Refactor FileStorage class (~2 días)
2. Migration script: filesystem → S3
3. Lifecycle policies + CDN si necesario
```

---

## 5. Sub-tema 4.3 — MOVIDO a R4 Tools/MCP (D-010)

### Decisión LOCKED

```
Sub-tema 4.3 (Code repo access) MOVIDO de R2 a R4 (Tools/MCP Layer)
```

### Razón del movimiento

Durante el debate de 4.3, Brian identificó correctamente que era una decisión específica al **wedge For3s QA** (GitHub/GitLab para análisis de PRs), NO una decisión genérica de la **plataforma For3s OS**.

For3s OS = plataforma. For3s QA = primer wedge. Las integraciones específicas (Git, Slack, Notion, etc.) son **MCP servers** reutilizables por cualquier wedge futuro, no decisiones core del Data Layer.

### Decisión arquitectónica (D-010)

- **For3s OS** queda agnóstico de integraciones específicas
- **R4 (Tools/MCP Layer)** decide MCP servers (Git, Slack, etc.)
- Cada wedge futuro reutiliza los MCP servers que necesite
- MCP es el estándar Anthropic (stack R1 ya incluye anthropic SDK)
- Hermes-style: providers pluggables, no hardcoded

### Impacto

- Bloque 4 queda con **3 sub-temas** (era 4)
- R2 total: **20 sub-temas** (era 21)
- 4.3 → R4 (Tools/MCP Layer) cuando llegue esa ronda

Ver `decision-log.md D-010` para detalle completo.

---

## 6. Sub-tema 4.4 — Backup strategy

### Decisión LOCKED

```
Local USB + Cloudflare R2 offsite (3-2-1 rule)
```

### Contexto

Backup es la **última línea de defensa** contra pérdida de datos. Compliance B2B exige plan claro de recovery. Con D-009 LOCAL, el servidor es SPOF físico (incendio/robo/falla disco), por lo que el offsite cloud se vuelve más crítico que en setup cloud.

### Mapeo al Grafo Maestro

- **Pilar 1 Seguridad:** razón de ser, backup encryption obligatorio
- **Pilar 2 Escalabilidad:** backup debe escalar con datos
- **Pilar 3 Autonomía:** sin backup, agente no puede ser confiado
- **TODOS los nodos** protegidos: KG, Hipocampo, Skills, Microglía, CLS, audit

### Candidatos evaluados

```
A) Local-only mínimo (USB único)        ⚠️ SPOF físico
B) Local + Cloud R2 offsite              ✅ ELEGIDO (3-2-1)
C) PITR continuo                          ❌ Overkill v1
D) Múltiples destinos (USB + R2 + USB2)  ❌ Overkill v1
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A: USB    │B: USB+R2 │C: PITR   │D: 3 dest │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Costo v1 mensual         │   $0     │   $0     │   $0     │   $0     │
│ Setup time               │ ~2 hrs   │ ~4 hrs   │ ~2-3 días│ ~6 hrs   │
│ RPO (data loss máx)      │   24h    │   24h    │   ~5 seg │   24h    │
│ RTO (tiempo recovery)    │  ~30 min │  ~1-2 hrs│  ~1 hora │  ~30 min │
│ 3-2-1 backup rule        │   ❌    │   ✅✅   │   ❌    │  ✅✅✅   │
│ Sobrevive incendio/robo  │   ❌    │   ✅✅   │   ❌    │  ✅✅✅   │
│ Compliance B2B           │  ⚠️ baja │  ✅✅    │  ✅✅    │  ✅✅✅   │
│ Free tier R2 v1 cubre    │   N/A    │   ✅✅   │   N/A    │  ✅✅    │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **3-2-1 backup rule** satisfecho (3 copias, 2 medios, 1 offsite)
2. **Compliance B2B enterprise ready** — offsite obligatorio
3. **Sobrevive worst case** (incendio/robo/falla disco)
4. **Free tier R2 cubre v1** (~3-5 GB backup)
5. **Cero egress charges** (restore gratis)
6. **Aprovecha Cloudflare ya en stack** (Tunnel D-009)
7. **Encryption end-to-end** (age + LUKS)
8. **Compatible D-009 LOCAL** (cifrado pre-upload)

### Configuración LOCKED v1

**DESTINOS (3-2-1 rule):**

```
1. Live: PostgreSQL + filesystem en disco CX42 local
2. Local: disco USB externo 2 TB conectado al servidor
3. Offsite: Cloudflare R2 (age encrypted pre-upload)
```

**FRECUENCIA:**

```
• Nightly 4 AM: pg_dump + rsync filesystem → USB local
• Nightly 5 AM: encrypt + upload R2
• Weekly Dom 6 AM: verify restore desde R2
• Monthly día 1 7 AM: rotación completa
```

**RETENCIÓN (compliance mvp-scope §11):**

```
• Daily backups: últimos 7
• Weekly backups: últimos 4
• Monthly backups: últimos 12
• TOTAL ~23 backups por workspace
```

**ENCRYPTION (P4 aplicado):**

- **Local USB:** LUKS filesystem encryption
- **Cloud R2:** age (X25519 + ChaCha20-Poly1305) PRE-upload
- **Llaves:** par age generado en setup
  - Public key en servidor (encrypt-only)
  - Private key OFFLINE en seguridad física

**HERRAMIENTAS:**

- pg_dump / pg_dumpall (Postgres oficial)
- rsync (filesystem)
- tar + gzip (configs + secrets)
- age (encryption modern)
- rclone (upload R2)
- systemd timers (scheduling)
- Arq jobs (meta-audit + monitoring vía B3 3.2)

**RPO/RTO LOCKED v1:**

```
• RPO: 24 horas (nightly backup)
• RTO: ~30 min desde USB local
• RTO: ~2-4 horas desde R2 (download + decrypt + restore)
```

**Scripts:**

```
/usr/local/bin/
├── for3s-backup-nightly.sh    → pg_dump + rsync local USB
├── for3s-backup-cloud.sh       → encrypt + upload R2
├── for3s-backup-rotate.sh      → rotación 7+4+12
├── for3s-backup-verify.sh      → SHA256 + test restore
└── for3s-backup-restore.sh     → restore desde local o R2

/etc/systemd/system/
├── for3s-backup-nightly.service  + .timer (4 AM diario)
├── for3s-backup-cloud.service     + .timer (5 AM diario)
└── for3s-backup-verify.service    + .timer (6 AM domingos)

/var/lib/for3s/secrets/
├── backup-encrypt.age           → public key (en servidor)
├── backup-decrypt.age            → private key (OFFLINE!)
├── r2-credentials.enc            → rclone config cifrado
└── files-passphrase.enc          → rclone crypt passphrase
```

**R2 BUCKET layout:**

```
r2:for3s-backups/
├── postgres/         → 2026-06-01.sql.gz.age
├── files/            → rclone crypt mirror
├── configs/          → 2026-06-01.tar.gz.age
└── manifests/        → manifest_2026-06-01.txt.sig
```

**META-AUDIT obligatorio:**

```sql
-- Cada backup run → INSERT shared.audit_events:
INSERT INTO shared.audit_events
(action, resource_type, payload)
VALUES (
  'backup:nightly_local' / 'backup:cloud_upload' /
  'backup:verify' / 'backup:rotation',
  'backup',
  {
    backup_date: '2026-06-01',
    size_bytes: 3221225472,
    sha256: '...',
    destinations: ['usb_local', 'r2_cloud'],
    encryption: 'age + luks',
    duration_seconds: 142,
    outcome: 'success'
  }
);
```

### Compliance answers preparadas para cliente

| Pregunta cliente | Respuesta For3s |
|---|---|
| "¿Dónde están mis backups?" | "3 copias: live + USB local (LUKS) + Cloudflare R2 (age cifrado pre-upload)" |
| "¿Cuánto tiempo puedo perder máximo?" | "24 horas (RPO). Backup nightly a 4 AM." |
| "¿Cuánto tiempo toma restaurar?" | "~30 min desde USB local, ~2-4 horas desde cloud." |
| "¿Quién tiene acceso a backups?" | "Solo Brian. Llave decrypt OFFLINE. R2 ve bytes opacos." |
| "¿Cuánto tiempo guardan backups?" | "12 meses (compliance §11). Rotación 7+4+12." |
| "¿Verificación regular?" | "SHA256 manifest nightly + restore test semanal desde R2." |

### Path futuro

```
v1: Local USB + R2 cloud + age encryption
v2: añadir Backblaze B2 como secondary cloud si necesario
v3: PITR si cliente enterprise demanda RPO <1h
```

---

## 7. Stack final consolidado

```
COMPONENTE B4                  DECISIÓN                            COSTO
──────────────────────────────────────────────────────────────────────
File storage                   Filesystem /var/lib/for3s/files/    USD 0
File metadata                  Postgres wks_X.file_metadata        USD 0
S3 v1                          NINGUNO (defer v2-v3)               USD 0
Backup local primary           Disco USB externo 2 TB + LUKS       USD 0 (USB ya comprado)
Backup cloud offsite           Cloudflare R2 free tier              USD 0 (10 GB cubre v1)
Encryption local               LUKS filesystem                     USD 0
Encryption cloud               age (X25519 + ChaCha20-Poly1305)    USD 0
Upload tool                    rclone (MIT)                        USD 0
Scheduling                     systemd timers                      USD 0
Meta-audit                     Arq job (B3 3.2)                    USD 0
──────────────────────────────────────────────────────────────────────
TOTAL incremental B4                                                USD 0
TOTAL v1 (R1 + R2 completo)                                         USD ~43/mo
```

### Servicios systemd v1 actualizado (post-B4)

```
Procesos systemd v1:
   1. PostgreSQL 16             (~3 GB RAM)
   2. pgbouncer                 (~30 MB RAM)
   3. Valkey                    (~100 MB RAM)
   4. FastAPI worker (uvicorn)   (~500 MB RAM)
   5. Arq worker                 (~300 MB RAM con Stella cargado)
   6. cloudflared (Tunnel)       (~50 MB RAM)
   ─────────────────────────────────────────────────
   Total RAM usage v1:           ~4 GB (de 30 GB)
   Holgura:                      26 GB (87%)

Systemd timers v1 (B4):
   • for3s-backup-nightly.timer    (4 AM diario)
   • for3s-backup-cloud.timer      (5 AM diario)
   • for3s-backup-verify.timer     (6 AM domingos)
   • for3s-backup-rotate.timer     (7 AM día 1 mes)
```

---

## 8. Cobertura del Grafo Maestro

### B4 es CAPA TRANSVERSAL — protege todo el sistema

```
PILAR                            STATUS POST-R2 COMPLETO
─────────────────────────────────────────────────────────
Pilar 1 Seguridad E2E            ✅ + backup offsite cifrado
Pilar 2 Escalabilidad             ✅ COMPLETO (B3 + B4)
Pilar 3 Autonomía Generativa     ✅ + backup garantiza continuidad
```

### Nodos cerebrales — B4 protege TODO

```
✅ Nodo 1 KG (AGE graphs)              → pg_dump completo
✅ Nodo 2 Hipocampo (episodes)          → pg_dump + filesystem
✅ Nodo 4 Skills (skills tables)        → pg_dump
✅ Nodo 6 Microglía (archived data)     → pg_dump + filesystem
✅ Nodo 9 Pattern Separation (HNSW)     → pg_dump
✅ Nodo 10 CLS (concepts)               → pg_dump
✅ Audit chain (Pilar 1 §6.4)           → pg_dump (hash chain intacto)
✅ Files (outputs, exports, audit)      → rsync filesystem
✅ Configs (postgres, valkey, etc.)     → tar archives
✅ Secrets (cifrados)                   → tar archives encrypted

Anclas LOCKED: 3/3 respetadas ✅
   1.D Dedicated SaaS  → backup per workspace via pg_dump per schema
   2.B Open Core       → pg_dump, rsync, age, rclone, systemd — todos open
   3.D Equipo pequeño  → automatización completa via systemd + Arq
```

---

## 9. Costo total v1 FINAL

```
HARDWARE (D-009 LOCAL):
   Hardware Linux Brian:               USD 0
   Electricidad servidor 24/7:         USD ~5/mes

DOMINIO + NETWORK:
   Cloudflare Tunnel:                   USD 0 (free)
   Dominio for3s.ai:                    USD ~$1/mes ($10/año)

R2 BLOQUE 1 (Storage Foundation):
   PostgreSQL + AGE + pgvector + pgcrypto: USD 0

R2 BLOQUE 2 (Memory Architecture):
   Custom memory module:               USD 0
   Stella embeddings local:            USD 0
   HDBSCAN clustering:                  USD 0
   OpenAI fallback embeddings:         USD <1/mes
   Claude Haiku 4.5 (CLS):              USD ~37/mes

R2 BLOQUE 3 (Performance & Async):
   pgbouncer:                           USD 0
   Valkey:                              USD 0
   Arq + asyncio + anyio:               USD 0

R2 BLOQUE 4 (Files & External):
   Filesystem local:                    USD 0
   Cloudflare R2 backup:                USD 0 (free tier)
   age + rclone + systemd:              USD 0
──────────────────────────────────────────────────
TOTAL v1 FINAL:                         USD ~43/mes
```

### Compras únicas (no recurring)

```
UPS básico (Cyberpower o APC):         USD ~80-150 una vez
Disco externo USB 2 TB (backup):       USD ~60 una vez
Dominio for3s.ai (registro inicial):   USD ~10 una vez
──────────────────────────────────────────
TOTAL una vez:                          USD ~150-220
```

### Verificación P2 <25% pilot revenue

```
Pilot Light USD 3,500 (3 semanas)
   Techo AI+infra: USD 875 (25%)
   Consumo real v1 (3 sem): USD ~32
   → 3.7% del techo
   → MARGEN 96.3% disponible para R3+R4+R8+R9

Pilot Pro USD 8,000 (3 semanas)
   Techo: USD 2,000
   Consumo v1: USD ~32
   → 1.6% del techo
   → MARGEN 98.4%

CONCLUSIÓN: infra v1 holgada por ~27x.
Espacio enorme para:
   • R3: LLM principal (Claude Opus ~$200-500/mes)
   • R4: MCP tools
   • R8: Observability
   • R9: Security/Compliance
```

---

## 10. Exploraciones futuras NO adoptadas v1

### 📚 Sub-tema 4.1 — File storage alternativos

```
📚 Candidato A — BLOB en PostgreSQL
   • Cuándo: archivos chicos críticos donde atomic transaction es valor
   • Costo: Postgres infla rápido

📚 Candidato C — S3-compatible
   • Cuándo: v3 cuando volumen >100 GB sostenido
   • Recomendación: Cloudflare R2 si migración cloud

📚 Candidato D — Híbrido
   • Cuándo: v2 si métricas muestran heterogeneidad tamaños

📚 Lifecycle policies automáticas
   • v2: archivos viejos → soft delete → hard delete según TTL

📚 Pre-signed URLs para download directo
   • v2: bandwidth tu servidor saturado

📚 Replicación geográfica
   • v3: enterprise multi-region

📚 Compression automática (gzip/zstd)
   • v2: archivos JSON/text grandes ocupan demasiado
```

### 📚 Sub-tema 4.2 — S3 provider alternativos

```
📚 Cloudflare R2 — backup offsite secundario (PRIMER OPCIÓN v2)
   • Cuándo: si 4.4 decide backup cloud necesario
   • YA ACTIVADO via decisión 4.4 LOCKED

📚 Backblaze B2 — alternativa más barata
   • Cuándo: backup volume >50 GB sostenido

📚 AWS S3 — para clientes enterprise específicos
   • Cuándo: cliente enterprise demanda AWS

📚 MinIO self-hosted
   • Cuándo: cliente exige S3 API + compliance no permite cloud

📚 Pre-signed URLs para download
   • Cuándo: bandwidth saturado

📚 Lifecycle policies (archive después N días)
   • Cuándo: compliance retention obligatorio

📚 CDN para assets públicos
   • Cuándo: sitio público For3s necesita CDN

📚 Cross-region replication
   • Cuándo: cliente enterprise multi-region
```

### 📚 Sub-tema 4.4 — Backup strategy alternativos

```
📚 PITR (Point-In-Time Recovery)
   • Cuándo: cliente enterprise financial demanda RPO <1h
   • Setup: ~2-3 días
   • Beneficio: RPO ~5 seg

📚 Múltiples destinos físicos
   • Cuándo: cliente enterprise requiere redundancia geográfica
   • Adicional: segundo USB rotado físicamente

📚 Backblaze B2 como secondary cloud
   • Cuándo: cliente demanda multi-cloud backup

📚 pg_basebackup + pgBackRest
   • Cuándo: backup volume >100 GB sostenido
   • Beneficio: backup incremental block-level

📚 Replicación logical Postgres
   • Cuándo: enterprise HA requirement
   • Beneficio: hot standby + failover

📚 Encryption KMS managed
   • Cuándo: compliance enterprise demanda KMS auditable
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**

---

## 11. Implicaciones en rondas siguientes (R3-R10)

### Para R3 — Model/LLM Layer

```
✅ Claude Haiku 4.5 ya USADO en CLS (B2 2.6)
   → R3 puede confirmar Haiku para CLS + decidir LLM principal
✅ anthropic SDK ya integrado
✅ Patterns async + CapacityLimiter listos para LLM calls
✅ Costos margen 96.3% del techo P2 disponible

R3 decidirá:
   • LLM principal para razonamiento del agente
   • Routing entre Claude / GPT / Gemini
   • Local LLM como fallback (Llama, Qwen)
   • Estrategia multi-model
```

### Para R4 — Tools / MCP Layer

```
✅ MCP SDK Python disponible (R1 LOCKED)
✅ Sub-tema 4.3 RECIBIDO de R2 (D-010)

R4 decidirá:
   • GitHub MCP server (para wedge QA)
   • GitLab MCP server (para wedge QA)
   • Slack/Notion/Jira MCP servers (futuros wedges)
   • Custom MCP servers per cliente
   • Auth strategies (OAuth, PAT, App tokens)
   • Webhook handlers
   • Rate limiting per MCP
```

### Para R5 — Orchestration

```
✅ Working Memory (Tier 1) foundation (B2 2.4)
✅ Patterns async + structured concurrency listos
✅ Nodo 3 PFC parcialmente mapeado

R5 decidirá:
   • Orquestador completo del agente
   • Planning + metacognición
   • Dual-process check (sistema 1 vs 2)
   • Action selector (Nodo 5)
   • DMN — idle compute (Nodo 7)
   • Neuromoduladores dinámicos (Nodo 11)
```

### Para R6 — Memory Stack extensiones

```
✅ Foundation completa en R2 B2

R6 decidirá:
   • Extensiones de memoria si necesarias
   • Posibles patterns avanzados
```

### Para R7 — Frontend / Channel

```
✅ Telegram bot LOCKED en R1
✅ Streamlit dashboard como opción

R7 decidirá:
   • Telegram bot details
   • Dashboard inicial
   • Notification strategies
```

### Para R8 — Observability

```
✅ Métricas obligatorias identificadas:
   • pgbouncer SHOW POOLS
   • Postgres pg_stat_*
   • Valkey INFO clients
   • Arq jobs metrics
   • Stella embeddings latency
   • HNSW recall periódico
   • Backup success rate
   • Cost per workspace (Claude Haiku CLS)

R8 decidirá:
   • Stack observability (Prometheus + Grafana, ...)
   • Logging structured (structlog)
   • Tracing (OpenTelemetry)
   • Alerting
```

### Para R9 — Security / Compliance

```
✅ Foundation completa:
   • RBAC tables (B1)
   • Audit chain inmutable (Pilar 1 §6.4)
   • Encryption híbrida P4
   • Workspace isolation (P3)
   • Rate limiting (B3 3.1)
   • Backup encrypted offsite (B4 4.4)

R9 decidirá:
   • Policy engine completo (Nodo 8 Amígdala)
   • Compliance reports automation
   • SOC2 / ISO27001 readiness
   • Data retention enforcement
   • Encryption key rotation
```

### Para R10 — CI/CD / Deploy

```
✅ Stack v1 COMPLETO listo para deployment script

R10 decidirá:
   • Deployment pipeline
   • Setup automation (Ansible/scripts)
   • Cloudflare Tunnel configuration
   • R2 bucket setup
   • Systemd services activation
   • Backup automation activation
   • Monitoring setup
   • Plan de recuperación operacional documentado
```

---

## 12. Cierre R2 — Filosofía consolidada

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   FILOSOFÍA CONSOLIDADA DE R2 — DATA LAYER                     ║
║                                                                ║
║   Después de 20 sub-temas LOCKED en 4 bloques + 5 decisiones    ║
║   cross-bloque (D-005 a D-010), R2 destila esta filosofía:      ║
║                                                                ║
║   1. CENTRALIZAR EN POSTGRESQL (B1)                              ║
║      Una sola BD hostea SQL + KG (AGE) + Vector (pgvector) +    ║
║      ES tables + audit chain. Reduce dramáticamente overhead    ║
║      operacional para equipo pequeño.                            ║
║                                                                  ║
║   2. CUSTOM CORE + LIBRERÍAS COMPOSABLES (B2)                   ║
║      Memory framework propio (control 100%) + librerías         ║
║      pequeñas reutilizables (pgvector-python, sentence-          ║
║      transformers, hdbscan, anthropic SDK).                      ║
║                                                                  ║
║   3. MAPEO 1:1 CON CEREBRO (B2 2.7)                             ║
║      3 tiers explícitos (Working/Short/Long) = Nodo 3 PFC /     ║
║      Nodo 2 Hipocampo / Nodo 1 KG. Documento canónico           ║
║      Mapeo_Nodo_Cerebral_Tabla_SQL.md.                          ║
║                                                                  ║
║   4. PRIVACY-FIRST (B2 + D-009)                                 ║
║      Stella embeddings LOCAL + despliegue LOCAL = datos del     ║
║      cliente jamás salen del hardware Brian.                     ║
║                                                                  ║
║   5. SCOPE MÍNIMO + PREPARACIÓN ESCALA (B3)                     ║
║      Valkey scope mínimo (2 propósitos) + pgbouncer desde       ║
║      día 1 (escala sin refactor) + Arq async-native.            ║
║                                                                  ║
║   6. LOCAL PRIMARY + CLOUD SECONDARY (B4 + D-009)               ║
║      Storage primary LOCAL (D-009 + 4.1). Backup local USB +    ║
║      cloud R2 (4.4) = 3-2-1 rule + compliance B2B.              ║
║                                                                  ║
║   7. OPEN CORE PURO (todas decisiones)                          ║
║      Todas licencias permisivas: BSD, MIT, Apache 2.0, ISC,     ║
║      PostgreSQL License. Cero BSL ni GPL-viral. Cero closed-    ║
║      source en core.                                             ║
║                                                                  ║
║   8. CERO SERVICIOS EXTRA INFRA                                 ║
║      Postgres + Valkey + pgbouncer + Cloudflare Tunnel = todo   ║
║      en mismo Linux LOCAL. +2 procesos systemd locales.         ║
║      Cero overhead operacional adicional.                       ║
║                                                                  ║
║   9. COSTO HOLGADO EN P2 <25%                                   ║
║      USD ~43/mes vs USD 875 techo Pilot Light = 3.7%.           ║
║      Margen 96.3% para R3 LLM + R4 MCP + R8 + R9.               ║
║                                                                  ║
║   10. ABSTRACCIÓN OS vs WEDGE (D-010)                           ║
║       For3s OS = plataforma reusable. For3s QA = primer wedge.  ║
║       Integraciones específicas (Git, Slack) en R4 Tools/MCP,   ║
║       no en core Data Layer.                                     ║
║                                                                  ║
║   ─────────────────────────────────────────────                ║
║                                                                  ║
║   COBERTURA GRAFO MAESTRO POST-R2:                              ║
║                                                                  ║
║   ✅ FULLY MAPPED (6 nodos):                                    ║
║      Nodo 1 KG, Nodo 2 Hipocampo, Nodo 4 Skills,                ║
║      Nodo 6 Microglía, Nodo 9 Pattern Separation, Nodo 10 CLS   ║
║                                                                  ║
║   🟡 FOUNDATION READY (4 nodos — cierran R3+R5+R9):             ║
║      Nodo 3 PFC, Nodo 5 Action Sel, Nodo 8 Amígdala,            ║
║      Nodo 11 Neuromoduladores                                    ║
║                                                                  ║
║   ⏳ PENDIENTE (1 nodo — R5):                                    ║
║      Nodo 7 DMN (Default Mode Network)                          ║
║                                                                  ║
║   PILARES: 3/3 cubiertos ✅                                     ║
║   ANCLAS LOCKED: 3/3 respetadas ✅                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Cierre del Bloque 4 y R2 COMPLETO

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ BLOQUE 4 — FILES & EXTERNAL DATA CERRADO                  ║
║   ✅ RONDA 2 — DATA LAYER 100% CERRADO                          ║
║                                                                ║
║   3/3 sub-temas LOCKED en B4                                    ║
║   20/20 sub-temas LOCKED en R2                                  ║
║   + D-005, D-009, D-010 decisiones cross-bloque                  ║
║                                                                ║
║   Costo total v1 FINAL: USD ~43/mes                              ║
║   % techo Pilot Light: 3.7%                                      ║
║   Margen disponible R3+R4+R8+R9: 96.3%                           ║
║                                                                ║
║   Próximo: R3 — Model/LLM Layer (decisión LLM principal)         ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```