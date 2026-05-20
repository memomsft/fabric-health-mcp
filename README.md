# fabric-health-mcp

> MCP server para health assessment conversacional de ambientes **Microsoft Fabric**.

**Autor:** Guillermo Ramirez · Solution Engineer, Cloud Data & AI · Microsoft  
**Versión:** 0.1.0 · **Licencia:** MIT

Analiza tu tenant de Fabric en lenguaje natural desde VS Code + GitHub Copilot.  
Sin dashboards adicionales. Sin herramientas externas. Solo tu cliente de IA y este servidor.

---

## ¿Qué evalúa?

### v0.1 — Infraestructura, Governance e Items

| Dimensión | Qué revisa |
|-----------|-----------|
| **Capacidades** | Estado, SKU sizing, administradores asignados |
| **Workspaces** | Capacidad asignada, roles, usuarios, workspaces huérfanos |
| **Items** | Inventario por tipo, items sin descripción, distribución de workloads |
| **Resumen ejecutivo** | Findings críticos consolidados + estado general 🟢🟡🔴 |
| **Reporte** | Health report exportado a Markdown |

### Roadmap

| Versión | Dimensión | Qué agrega |
|---------|-----------|-----------|
| v0.2 | **Data Freshness** | Pipelines fallidos, semantic models sin refresh |
| v0.3 | **Adopción** | Items sin uso en 30/60/90 días (Activity Events API) |
| v0.4 | **Maturity Score** | Labels, endorsement, lineage por workspace |

---

## Arquitectura

```
AI Client (VS Code + GitHub Copilot)
         │
         │  MCP stdio
         ▼
fabric-health-mcp  (Python — corre local)
├── list_all_capacities / analyze_capacity_health
├── list_all_workspaces / analyze_workspace_score
├── get_tenant_items_summary / list_workspace_items
├── analyze_workspaces_items_batch
├── get_full_tenant_summary
└── generate_tenant_health_report
         │
         │  REST API (HTTPS)
         ▼
Microsoft Fabric Admin API          Power BI Admin API
api.fabric.microsoft.com/v1         api.powerbi.com/v1.0/myorg
```

**Auth:** `az login` — credenciales del usuario vía `AzureCliCredential`.  
**Sin secrets. Sin Service Principals. Sin datos que salgan de tu máquina.**

---

## Requisitos

- Python 3.10+
- Azure CLI
- VS Code con extensión GitHub Copilot
- Rol **Fabric Administrator** en el tenant

---

## Instalación rápida

```bash
git clone https://github.com/memomsft/fabric-health-mcp
cd fabric-health-mcp
pip install -e .
az login
```

Agrega en VS Code (`Ctrl+Shift+P → MCP: Open User Configuration`):

```json
{
  "servers": {
    "fabric-health": {
      "command": "python",
      "args": ["-m", "fabric_health_mcp.server"]
    }
  }
}
```

> **Windows con Anaconda:** usa el path completo de Python.  
> Ver [docs/setup.md](docs/setup.md) para instrucciones detalladas.

Abre VS Code desde la carpeta del proyecto para que Copilot priorice este MCP:
```bash
code .
```

---

## Uso

En Copilot Chat (modo **Agent**):

```
¿Cuál es el estado de salud de mis capacidades de Fabric?
```

```
¿Hay workspaces huérfanos o sin usuarios asignados en mi tenant?
```

```
¿Qué workspaces tienen peor governance de items?
```

```
Genera el reporte completo de salud del tenant
```

Ver más ejemplos en [docs/sample-prompts.md](docs/sample-prompts.md).

---

## Tools disponibles (9)

| Tool | Descripción |
|------|-------------|
| `list_all_capacities` | Inventario de capacidades con SKU, estado y admins |
| `analyze_capacity_health` | Health score (0-100) de una capacidad |
| `list_all_workspaces` | Inventario de workspaces con flags de riesgo |
| `analyze_workspace_score` | Governance score (0-100) de un workspace |
| `get_tenant_items_summary` | Overview de items del tenant por tipo y workload |
| `list_workspace_items` | Items de un workspace con detección de governance gaps |
| `analyze_workspaces_items_batch` | Comparativo de items entre múltiples workspaces |
| `get_full_tenant_summary` | Resumen ejecutivo del tenant |
| `generate_tenant_health_report` | Reporte Markdown completo |

---

## Documentación

- [Setup detallado Windows y Mac](docs/setup.md)
- [Referencia de tools](docs/tools-reference.md)
- [Prompts validados](docs/sample-prompts.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Contribuir](CONTRIBUTING.md)

---

## Notas técnicas

- **CU utilization en tiempo real** no está disponible vía REST API. Usa la [Fabric Capacity Metrics App](https://learn.microsoft.com/fabric/enterprise/metrics-app).
- **Admins de capacidad** se obtienen vía Power BI Admin API (`/admin/capacities`) — la Fabric API no los expone.
- **GET /capacities/{id}** no está soportado — el servidor filtra desde la lista completa.
- Los reportes se guardan en `reports/` — carpeta excluida del `.gitignore`.

---

*Construido con [MCP](https://modelcontextprotocol.io) · [azure-identity](https://pypi.org/project/azure-identity/) · [httpx](https://www.python-httpx.org/)*
