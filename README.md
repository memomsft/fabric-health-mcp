# fabric-health-mcp

> MCP server para health assessment conversacional de ambientes **Microsoft Fabric**.

**Autor:** Guillermo Ramirez · Solution Engineer, Cloud Data & AI · Microsoft  
**Versión:** 0.1.0 · **Licencia:** MIT · **Estado:** Beta

Analiza tu tenant de Fabric en lenguaje natural desde VS Code + GitHub Copilot.  
Sin dashboards adicionales. Sin herramientas externas. Solo tu cliente de IA y este servidor.

---

## Demo

> _"¿Cuántos items de Fabric no tienen descripción y cuáles son los más críticos?"_

```
📊 Análisis completado — 63 items en 6 workspaces

Workspace             Total   Sin doc   % sin doc
─────────────────────────────────────────────────
WS_Logistics            17       9        53% 🔴
Refacciones             11       6        55% 🔴
powerbi-mcp-demo         3       2        67% 🔴
Fabric-IQ-Manufactura   22       6        27% 🟡
zava-planning            8       2        25% 🟡

⚠️ Acción recomendada: documentar los 9 items de WS_Logistics
   para facilitar gobierno y transferencia de conocimiento.
```

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
         │  MCP stdio
         ▼
fabric-health-mcp  (Python — local)
├── list_all_capacities / analyze_capacity_health
├── list_all_workspaces / analyze_workspace_score  
├── get_tenant_items_summary / list_workspace_items
├── analyze_workspaces_items_batch
├── get_full_tenant_summary
└── generate_tenant_health_report
         │  HTTPS
         ├─────────────────────────────────┐
         ▼                                 ▼
Fabric Admin API              Power BI Admin API
workspaces · items            admins de capacidad
```

Ver explicación completa en [docs/architecture.md](docs/architecture.md).

**Sin secrets. Sin Service Principals. Sin datos que salgan de tu máquina.**

---

## Cómo se calcula el score

Cada recurso recibe un score de **0 a 100** restando puntos por condiciones negativas:

**Capacidades**

| Condición | Impacto |
|-----------|---------|
| Suspendida | -40 |
| Pausada | -20 |
| SKU ≤ F4 | -15 |
| Sin admins | -20 |

**Workspaces**

| Condición | Impacto |
|-----------|---------|
| Sin capacidad asignada | -30 |
| Sin Admin asignado | -25 |
| Sin usuarios (huérfano) | -15 |

**Grades:** A (≥90) · B (≥75) · C (≥60) · D (≥40) · F (<40)

> **Nota:** Estos pesos son una estimación razonable para identificar riesgos comunes.
> No representan un estándar oficial de Microsoft — interprétalos como guía orientativa.

---

## Requisitos

- Python 3.10+
- Azure CLI (`az --version`)
- VS Code con extensión GitHub Copilot
- Rol **Fabric Administrator** en el tenant

---

## Instalación

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
      "type": "stdio",
      "command": "python",
      "args": ["-m", "fabric_health_mcp.server"]
    }
  }
}
```

> **Windows con Anaconda:** usa el path completo de Python (`conda run where python`).  
> Ver [docs/setup.md](docs/setup.md) para instrucciones detalladas.

Abre VS Code desde la carpeta del proyecto:
```bash
code .
```

Verifica que el servidor está corriendo:
```
Ctrl+Shift+P → MCP: List Servers → fabric-health: Running (9 tools)
```

---

## Uso

En Copilot Chat modo **Agent**:

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
¿Qué tipo de workloads está usando más mi tenant — datos, BI o AI?
```
```
Genera el reporte completo de salud del tenant
```


Ver más en [docs/sample-prompts.md](docs/sample-prompts.md).

---

## Tools (9)

| Tool | Descripción |
|------|-------------|
| `list_all_capacities` | Inventario con SKU, estado y admins |
| `analyze_capacity_health` | Health score (0-100) de una capacidad |
| `list_all_workspaces` | Inventario con flags de riesgo |
| `analyze_workspace_score` | Governance score (0-100) de un workspace |
| `get_tenant_items_summary` | Overview de items por tipo y workload |
| `list_workspace_items` | Items de un workspace con governance gaps |
| `analyze_workspaces_items_batch` | Comparativo entre múltiples workspaces |
| `get_full_tenant_summary` | Resumen ejecutivo del tenant |
| `generate_tenant_health_report` | Reporte Markdown completo |

Ver detalles en [docs/tools-reference.md](docs/tools-reference.md).

---

## Documentación

| Doc | Contenido |
|-----|-----------|
| [docs/setup.md](docs/setup.md) | Setup paso a paso Windows y Mac |
| [docs/architecture.md](docs/architecture.md) | Arquitectura y cálculo de scores |
| [docs/tools-reference.md](docs/tools-reference.md) | Referencia de las 9 tools |
| [docs/sample-prompts.md](docs/sample-prompts.md) | Prompts validados |
| [SECURITY.md](SECURITY.md) | Qué hace y qué no hace con tus datos |
| [CHANGELOG.md](CHANGELOG.md) | Historial de versiones |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Cómo contribuir |

---

## Notas técnicas

- **CU utilization en tiempo real** no disponible vía REST API — usa la [Fabric Capacity Metrics App](https://learn.microsoft.com/fabric/enterprise/metrics-app).
- **GET /v1/capacities/{id}** no soportado — el servidor filtra desde la lista completa.
- **Admins de capacidad** se obtienen via Power BI Admin API — la Fabric API no los expone.
- Los reportes se guardan en `reports/` — excluidos del `.gitignore`.

---

*Construido con [MCP](https://modelcontextprotocol.io) · [azure-identity](https://pypi.org/project/azure-identity/) · [httpx](https://www.python-httpx.org/)*
