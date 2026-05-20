# Tools Reference — fabric-health-mcp

Documentación de las 9 tools expuestas por el servidor MCP.

---

## Capacidades

### `list_all_capacities`
Lista todas las capacidades de Fabric del tenant.

**Requiere:** Fabric Administrator  
**API:** `GET /v1/capacities` + `GET /powerbi/admin/capacities` (para admins)

**Output:**
```json
{
  "total_capacities": 4,
  "capacities": [
    {
      "id": "xxxx",
      "display_name": "hackmx",
      "sku": "F8",
      "max_cu": 8,
      "state": "Active",
      "region": "West US 3",
      "admins": ["admin@empresa.com"]
    }
  ]
}
```

---

### `analyze_capacity_health`
Health score (0-100) de una capacidad específica.

**Args:** `capacity_id` (string) — obtener con `list_all_capacities`  
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

---

## Workspaces

### `list_all_workspaces`
Inventario completo de workspaces con flags de riesgo.

**Requiere:** Fabric Administrator  
**API:** `GET /v1/workspaces`

**Output incluye:**
- Total de workspaces
- Workspaces sin capacidad asignada
- Workspaces personales (My Workspace)

---

### `analyze_workspace_score`
Governance score (0-100) de un workspace específico.

**Args:** `workspace_id` (string)  
**API:** `GET /v1/workspaces/{id}` + `GET /v1/admin/workspaces/{id}/users`

**Score breakdown:**

| Condición | Impacto |
|-----------|---------|
| Sin capacidad asignada | -30 |
| Estado Deleted | -50 |
| Sin Admin asignado | -25 |
| Más de 3 Admins | -10 |
| Sin usuarios asignados | -15 |

---

## Items

### `list_workspace_items`
Lista todos los items de un workspace agrupados por tipo.

**Args:** `workspace_id` (string)  
**API:** `GET /v1/workspaces/{id}/items`

**Detecta:** items de datos sin descripción (riesgo de governance)

**Tipos de items:** Lakehouse, Warehouse, Pipeline, Notebook, SemanticModel, Report, DataAgent, Eventhouse, KQLDatabase, Reflex, Ontology, CopyJob, SQLDatabase, SQLEndpoint

---

### `analyze_workspaces_items_batch`
Analiza items de múltiples workspaces en paralelo.

**Args:** `workspace_ids` (list[string])  
**Output:** ranking comparativo por cantidad y tipo de items

---

### `get_tenant_items_summary`
Overview de todos los items del tenant agrupados por tipo.

**API:** `GET /v1/workspaces` + `GET /v1/workspaces/{id}/items` por cada workspace  
**Incluye:** insights sobre madurez del uso de Fabric (data engineering vs BI vs AI)

---

## Resumen y Reporte

### `get_full_tenant_summary`
Resumen ejecutivo del tenant — punto de entrada recomendado.

Agrega: capacidades + workspaces + findings críticos + estado general (🟢/🟡/🔴)

---

### `generate_tenant_health_report`
Genera un reporte de salud completo en formato Markdown.

**Output:** archivo `reports/health_report_YYYYMMDD_HHMM.md`  
**Incluye:** capacidades, workspaces, findings críticos, roadmap de versiones

> Los reportes generados están excluidos del `.gitignore` — no se suben a GitHub.
