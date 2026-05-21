# Tools Reference — fabric-health-mcp

Documentación de las 6 tools de análisis expuestas por el servidor MCP.

> **Nota:** Para listar workspaces, capacidades e items usa el
> [Fabric Core MCP oficial](https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/core-remote/get-started-core).
> Este servidor es complementario — evalúa y puntúa, no lista ni gestiona.

---

## Capacidades

### `analyze_capacity_health`
Health score (0-100) de una capacidad específica.

**Args:** `capacity_id` (string) — obtener con `list_capacities` del Fabric Core MCP  
**API:** Filtra desde `GET /v1/capacities` (GET por ID no disponible en la API)

**Score breakdown:**

| Condición | Impacto |
|-----------|---------|
| Capacidad suspendida | -40 |
| Capacidad pausada | -20 |
| SKU ≤ F4 | -15 |
| Sin admins | -20 |
| Más de 5 admins | -5 |

**Grades:** A (90-100) · B (75-89) · C (60-74) · D (40-59) · F (0-39)

> Los pesos son una estimación razonable — no son un estándar oficial de Microsoft.

---

## Workspaces

### `analyze_workspace_score`
Governance score (0-100) de un workspace específico.

**Args:** `workspace_id` (string) — obtener con `list_workspaces` del Fabric Core MCP  
**API:** `GET /v1/workspaces/{id}` + `GET /v1/admin/workspaces/{id}/users`

**Score breakdown:**

| Condición | Impacto |
|-----------|---------|
| Sin capacidad asignada | -30 |
| Estado Deleted | -50 |
| Sin Admin asignado | -25 |
| Más de 3 Admins | -10 |
| Sin usuarios asignados | -15 |

> Los pesos son una estimación razonable — no son un estándar oficial de Microsoft.

---

## Items

### `analyze_workspaces_items_batch`
Analiza governance de items en múltiples workspaces en paralelo.

**Args:** `workspace_ids` (list[string]) — obtener con `list_workspaces` del Fabric Core MCP  
**Detecta:** items sin descripción, distribución por tipo  
**Output:** ranking comparativo de governance entre workspaces

### `get_tenant_items_summary`
Overview de governance de items del tenant agrupados por tipo.

**API:** `GET /v1/workspaces` + `GET /v1/workspaces/{id}/items` por cada workspace  
**Incluye:** insights sobre madurez — data-heavy vs BI-heavy vs AI-heavy

---

## Resumen y Reporte

### `get_full_tenant_summary`
Resumen ejecutivo del tenant — punto de entrada recomendado.

Agrega health scores de capacidades + workspaces + findings críticos + estado general 🟢🟡🔴

### `generate_tenant_health_report`
Genera un reporte de salud completo en formato Markdown.

**Output:** archivo `reports/health_report_YYYYMMDD_HHMM.md`  
**Incluye:** capacidades, workspaces, findings críticos, roadmap

> Los reportes generados están excluidos del `.gitignore` — no se suben a GitHub.
