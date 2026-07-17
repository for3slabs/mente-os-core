# Ronda 10 — Bloque 2 — Deploy + Infra

**Sub-documento de R10.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_10_CICD_Deploy.md](Ronda_10_CICD_Deploy.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED)
**Fecha cierre:** 2026-06-09

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Entregable |
|---|---|---|
| 10.2.1 Runtime Architecture | C — Híbrido completo (systemd + Docker) | deploy/systemd/*.service + docker-compose.yml |
| 10.2.2 Networking | C — Cloudflare + Tailscale dual-plane | cloudflared.yml + Tailscale config |
| 10.2.3 Secrets + Observability | C — TPM/USB KEK + rotación + observability provisioning | secrets_bootstrap.py + observability/provisioning/ |

---

## 10.2.1 — Runtime Architecture (= P1=B detallado)

**Decisión LOCKED:** **C — Híbrido completo (systemd nativo + Docker gestionado)**

### Capa nativa (systemd)
- `postgresql.service` (~4-6GB) + `valkey.service` (~1GB) — performance DB nativa
- `for3s-app.service`: uvicorn, deps Postgres+Valkey, auto-restart, MemoryMax 4G, CPUQuota 200%, graceful reload (ExecReload HUP), hardening (NoNewPrivileges + ProtectSystem=strict + User=for3s)
- `for3s-worker@.service`: template unit (N instancias escalables), MemoryMax 2G
- `for3s-backup.timer` (10.3.1)

### Capa Docker (compose bajo systemd)
- MCP servers (R4 SHA-pinned, aislamiento multi-tenant)
- Observability: Prometheus + Loki + Tempo + Grafana + Alertmanager (R8)
- `for3s-docker.service` gestiona compose (auto-start + restart)

### Arranque ordenado (dependency graph)
1. postgresql + valkey → 2. docker (MCP+obs) → 3. app → 4. workers → 5. backup timer

### Networking interno
todo localhost/bridge, NADA expuesto salvo Cloudflare Tunnel (10.2.2)

### Logging unificado
journald (systemd) + Docker json-file → Loki (R8) via promtail/alloy

### Resource budget (30GB total)
Postgres 4-6 + App 4 + Workers 2×N + Valkey 1 + MCP 2 + Observability 2 + OS 5 = ~8.5GB (headroom amplio)

### Audit events
`service_started/stopped/restarted` · `service_crash_detected` · `resource_limit_exceeded`

### Métricas
`service_uptime_seconds` · `service_restarts_total` · `service_memory/cpu` (node_exporter cgroups)

### Reusa
P1=B + D-009 + R4 MCP Docker + R8 observability + R1 uvicorn + R2 Arq

---

## 10.2.2 — Networking (Dual-Plane)

**Decisión LOCKED:** **C — Cloudflare Tunnel (data plane) + Tailscale (admin plane)** ⭐ mejora vs Cloudflare Access

### DATA PLANE (clientes externos) → Cloudflare Tunnel
- `api.for3s.ai` → app:8000 (REST + Telegram + GitHub webhooks R7)
- `status.for3s.ai` → status page (R8 8.4.3)
- TLS estricto Full (extremo a extremo) + HSTS + min TLS 1.2
- WAF (OWASP Core Rule Set) — filtra obvio ANTES de Amígdala
- Rate limit borde (complementa R3 token bucket + 9.1.2 Amígdala rate)
- DDoS protection + bot management
- Cero puertos abiertos · IP Brian oculta · sin fricción cliente

### ADMIN/OPS PLANE (solo Brian) → Tailscale
- SSH (administración) + Grafana/observability + Postgres directo + CI self-hosted runner
- WireGuard mesh privado · NUNCA toca internet público
- **Brian ya tiene Tailscale instalado** (cero fricción)
- REEMPLAZA Cloudflare Access para Grafana (`grafana.for3s.ai` público ELIMINADO)

### Defensa en capas
Borde (CF WAF) → Amígdala (R9 semántico) → RBAC (R7) → token bucket (R3)

### Mejora SOC2 CC6.6 (boundary protection)
Admin por red privada (Tailscale) > admin público → más defendible en auditoría

### Health check + failover
CF health check /health → si origen down sirve status page · tunnel auto-reconnect · `cloudflared` como systemd service

### Audit events
`tunnel_connected/disconnected` · `tailscale_admin_access` · `edge_waf_blocked`

### Reusa
D-009 Cloudflare + for3s.ai + Tailscale (Brian instalado) + 10.2.1 runtime + R7 channels/RBAC + R9 Amígdala + R8 status/métricas + R3 token bucket
`$0` (Cloudflare free + Tailscale free ≤100 devices)

**Memoria:** `project_dual_plane_networking`

---

## 10.2.3 — Secrets Bootstrap + Observability Deploy

**Decisión LOCKED:** **C — TPM/USB KEK + rotación + observability provisioning**

### Bootstrap Master KEK (memoria LOCKED: offline, nunca en server)
- **PRINCIPAL: TPM 2.0** unseal (auto tras reboot, KEK sellada al chip, inútil si roban disco)
- **FALLBACK: USB/passphrase** (semi-manual, break-glass R9 insider)
- **BACKUP: OFFLINE** USB cifrado en caja fuerte física

### Secrets injection runtime
- Master KEK → memoria only (nunca disco) → deriva Workspace KEKs on-demand (R4)
- systemd `LoadCredentialEncrypted` (tmpfs RAM, NO EnvironmentFile plano)
- Docker secrets (no en image)
- **Brian NUNCA ve plaintext** (memoria LOCKED) ✓

### Secrets bootstrappeados
Master KEK + Workspace KEKs + DB passwords + LLM API keys (R3/R6) + tunnel creds (10.2.2) + Grafana admin + webhook HMAC (R7) + notification creds (R7)

### Rotación
- Workspace KEK: lazy re-encrypt sin downtime
- API keys: grace period (viejo+nuevo válidos)
- DB: coordinada (deploy window)
- Master KEK: manual excepcional (break-glass + re-seal TPM)

### Observability deploy (R8 provisioning declarativo, Git)
- Prometheus: scrape targets (app + node_exporter + cAdvisor) + alerting rules (R8 8.4.1 SLO + R9 security)
- Loki: promtail/alloy (journald + Docker → Loki) + retention
- Tempo: OTel receiver (R8 8.1.2 tracing)
- Grafana: datasources + dashboards JSON (R8 8.2.x) + admin pwd (bootstrap) + **acceso SOLO Tailscale** (10.2.2)
- Alertmanager: routing → app webhook (R8 8.4.2)

### CI/CD secrets
GitHub Actions secrets (deploy keys) — NUNCA Master KEK (server bootstrappea su propia)

### Defense in depth (memoria LOCKED)
KEK offline + secrets cifrados at-rest + memoria runtime + Brian no plaintext + audit sin valores + RBAC app-only

### Audit events
`secrets_bootstrap_completed` (sin KEK) · `secret_injected` (sin valor) · `secret_rotated` (sin valor) · `secrets_bootstrap_failed` · `observability_provisioned`

### Métricas
`secrets_bootstrap_duration_seconds` · `secret_rotations_total` (type) · `secrets_decrypt_total` (sin valores)

### Reusa
R4 KEK hierarchy + R9 insider playbook (break-glass + KEK offline) + 10.2.1 runtime (systemd LoadCredential + Docker secrets) + 10.2.2 Tailscale (Grafana access) + R8 observability
`$0` (TPM hardware existente, sin servicio externo anti-D-009)