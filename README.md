# fabric-health-mcp

> MCP server para health assessment conversacional de ambientes **Microsoft Fabric**.

Analiza tu tenant de Fabric usando lenguaje natural desde VS Code + GitHub Copilot.  
Sin dashboards adicionales, sin herramientas externas — solo tu cliente de IA y este servidor.

---

## ¿Qué evalúa?

### v0.1 — Infraestructura y Governance

| Dimensión | Qué revisa |
|-----------|-----------|
| **Capacidades** | Estado, SKU sizing, administradores asignados |
| **Workspaces** | Capacidad asignada, roles, usuarios, workspaces huérfanos |
| **Resumen ejecutivo** | Findings críticos consolidados del tenant |
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
├── list_all_capacities
├── analyze_capacity_health
├── list_all_workspaces
├── analyze_workspace_score
├── get_full_tenant_summary
└── generate_tenant_health_report
         │
         │  REST API (HTTPS)
         ▼
Microsoft Fabric Admin API
(api.fabric.microsoft.com/v1)
```

**Autenticación:** `az login` — usa las credenciales del usuario vía `AzureCliCredential`.  
**Sin secrets. Sin Service Principals. Sin datos que salgan de tu máquina.**

---

## Requisitos

- Python 3.10+
- Azure CLI (`az --version`)
- VS Code con extensión GitHub Copilot
- Rol **Fabric Administrator** en el tenant

---

## Instalación rápida

```bash
git clone https://github.com/TU_ORG/fabric-health-mcp
cd fabric-health-mcp
pip install -e .
az login
```

Luego agrega en VS Code (`Ctrl+Shift+P → MCP: Open User Configuration`):

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

---

## Uso

En Copilot Chat (modo **Agent**):

```
Genera un resumen de salud de mi tenant de Fabric
```

```
¿Cuántos workspaces no tienen capacidad de Fabric asignada?
```

```
Genera el reporte completo y guárdalo como Markdown
```

Ver más ejemplos en [docs/sample-prompts.md](docs/sample-prompts.md).

---

## Tools disponibles

| Tool | Descripción |
|------|-------------|
| `list_all_capacities` | Inventario de capacidades con SKU y estado |
| `analyze_capacity_health` | Health score (0-100) de una capacidad |
| `list_all_workspaces` | Inventario de workspaces con flags de riesgo |
| `analyze_workspace_score` | Governance score (0-100) de un workspace |
| `get_full_tenant_summary` | Resumen ejecutivo del tenant |
| `generate_tenant_health_report` | Reporte Markdown completo |

---

## Documentación

- [Setup detallado Windows y Mac](docs/setup.md)
- [Referencia de tools](docs/tools-reference.md)
- [Prompts de ejemplo](docs/sample-prompts.md)
- [Seguridad](SECURITY.md)
- [Changelog](CHANGELOG.md)

---

## Notas técnicas

- **CU utilization en tiempo real** no está disponible vía REST API.  
  Para eso usa la [Fabric Capacity Metrics App](https://learn.microsoft.com/fabric/enterprise/metrics-app).
- Los reportes generados se guardan en `reports/` — carpeta excluida del `.gitignore`.
- El servidor corre 100% local. Ningún dato sale hacia servicios externos.
