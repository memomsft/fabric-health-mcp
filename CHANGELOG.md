# Changelog

## [0.1.0] — 2026-05-20

### Primera versión — Infraestructura, Governance e Items

**Tools incluidas (9):**
- `list_all_capacities` — inventario de capacidades con admins via Power BI Admin API
- `analyze_capacity_health` — health score (0-100) de una capacidad
- `list_all_workspaces` — inventario con flags de riesgo
- `analyze_workspace_score` — governance score (0-100) de un workspace
- `list_workspace_items` — items de un workspace con detección de governance gaps
- `analyze_workspaces_items_batch` — comparativo de items entre workspaces
- `get_tenant_items_summary` — overview de items del tenant por tipo
- `get_full_tenant_summary` — resumen ejecutivo del tenant
- `generate_tenant_health_report` — reporte Markdown completo

**Hallazgos de API (validados contra tenant real):**
- `GET /v1/capacities/{id}` no está soportado → se filtra desde la lista completa
- `GET /v1/admin/workspaces` devuelve vacío → usar `GET /v1/workspaces`
- Admins de capacidad no expuestos en Fabric API → usar Power BI Admin API `/admin/capacities`
- Campo `sku` puede ser string `"F8"` u objeto `{"name": "F8"}` → normalizado con `isinstance`
- Tipos de workspace personal: `"Personal"` y `"PersonalGroup"` (ambos)
- `ManagedIdentityCredential` lanza WinError 5 en Windows local → excluido, usar `AzureCliCredential`

**Auth:**
- `ChainedTokenCredential(AzureCliCredential, VisualStudioCodeCredential)`
- Fabric API scope: `https://api.fabric.microsoft.com/.default`
- Power BI API scope: `https://analysis.windows.net/powerbi/api/.default`

---

## Roadmap

### [0.2.0] — Data Freshness
- Pipelines fallidos en las últimas 24/48h
- Semantic models sin refresh programado
- Lakehouses sin actividad reciente

### [0.3.0] — Adopción
- Items sin acceso en 30/60/90 días (Activity Events API)
- Score de adopción por workspace

### [0.4.0] — Maturity Score
- Sensitivity labels coverage
- Endorsement rate (Promoted/Certified)
- Lineage coverage
- Score de madurez consolidado por workspace

### [0.5.0] — Delta Lake Health
- `analyze_lakehouse_health` — DESCRIBE DETAIL por tabla (small files, tamaño)
- `get_delta_optimization_score` — tablas sin OPTIMIZE o VACUUM reciente
- `get_tables_without_zordering` — tablas candidatas a Z-ORDER
- Conecta via SQL Analytics Endpoint del Lakehouse
