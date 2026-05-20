# Copilot Instructions — Fabric Health MCP

## Contexto
Este repositorio contiene un MCP server para health assessment de Microsoft Fabric.
Cuando el usuario haga preguntas sobre salud, governance, capacidades, workspaces o items de Fabric,
usa **exclusivamente** el servidor MCP `fabric-health`.

## Reglas
- Nunca uses Azure MCP, Power BI MCP u otros servidores para tareas de Fabric health assessment
- Responde siempre en español
- Da recomendaciones concretas y accionables, no solo datos

## Tools disponibles en fabric-health

| Tool | Cuándo usarla |
|------|--------------|
| `get_full_tenant_summary` | Punto de entrada — visión general del tenant |
| `list_all_capacities` | Cuando pregunten por capacidades, SKUs, CUs |
| `analyze_capacity_health` | Health score de una capacidad específica |
| `list_all_workspaces` | Inventario de workspaces, workspaces sin capacidad |
| `analyze_workspace_score` | Governance score de un workspace específico |
| `get_tenant_items_summary` | Overview de items del tenant por tipo |
| `list_workspace_items` | Items de un workspace específico |
| `analyze_workspaces_items_batch` | Comparar items entre múltiples workspaces |
| `generate_tenant_health_report` | Generar reporte Markdown completo |

## Flujo recomendado
1. Empieza con `get_full_tenant_summary` para contexto general
2. Profundiza con tools específicas según lo que pregunte el usuario
3. Termina con `generate_tenant_health_report` si el usuario quiere un reporte
