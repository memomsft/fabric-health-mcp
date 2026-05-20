# Changelog

## [0.1.0] — 2026-05-20

### Primera versión pública

**Tools incluidas:**
- `list_all_capacities` — inventario de capacidades del tenant
- `analyze_capacity_health` — health score de una capacidad (0-100)
- `list_all_workspaces` — inventario de workspaces con flags de riesgo
- `analyze_workspace_score` — governance score de un workspace (0-100)
- `get_full_tenant_summary` — resumen ejecutivo del tenant
- `generate_tenant_health_report` — genera reporte Markdown

**Fixes conocidos:**
- Auth: `ManagedIdentityCredential` excluido explícitamente (WinError 5 en Windows local)
- API: SKU parseado como string o objeto según respuesta de la API

**Limitaciones conocidas:**
- CU utilization en tiempo real no disponible vía REST API
- Activity Events API (adopción) pendiente para v0.2
- Governance/Purview score pendiente para v0.3

---

## Roadmap

### [0.2.0] — Data Freshness
- Pipelines fallidos en las últimas 24/48h
- Semantic models sin refresh programado
- Lakehouses sin actividad reciente

### [0.3.0] — Adopción
- Items sin acceso en 30/60/90 días (Activity Events API)
- Workspaces con baja actividad
- Score de adopción por workspace

### [0.4.0] — Maturity Score
- % items con sensitivity label
- % items endorsed
- Lineage coverage
- Score de madurez consolidado por workspace y tenant
