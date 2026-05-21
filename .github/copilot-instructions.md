# Copilot Instructions — fabric-health-mcp

## Contexto
Este servidor MCP es un **Assessment Layer** complementario al Fabric Core MCP oficial.
- **Fabric Core MCP oficial** → gestiona recursos (listar, crear, modificar)
- **fabric-health-mcp (este servidor)** → evalúa y puntúa recursos

## Reglas
- Para LISTAR workspaces, capacidades o items → usa el Fabric Core MCP oficial
- Para EVALUAR, PUNTUAR o ANALIZAR → usa fabric-health-mcp
- Nunca uses Azure MCP u otros servidores para tareas de Fabric health assessment
- Responde siempre en español con recomendaciones accionables

## Tools disponibles en fabric-health

| Tool | Cuándo usarla |
|------|--------------|
| `get_full_tenant_summary` | Punto de entrada — visión general del tenant |
| `analyze_capacity_health` | Health score de una capacidad específica |
| `analyze_workspace_score` | Governance score de un workspace específico |
| `get_tenant_items_summary` | Overview de governance de items del tenant |
| `analyze_workspaces_items_batch` | Comparar governance entre múltiples workspaces |
| `generate_tenant_health_report` | Generar reporte Markdown completo |

## Flujo recomendado
1. Usa `list_workspaces` / `list_capacities` del Core MCP para obtener IDs
2. Usa `get_full_tenant_summary` para visión general
3. Profundiza con tools de análisis específicas
4. Cierra con `generate_tenant_health_report`
