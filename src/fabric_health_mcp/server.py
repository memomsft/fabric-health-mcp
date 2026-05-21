"""
Fabric Health MCP Server — v0.1
MCP server para health assessment de ambientes Microsoft Fabric.

Uso:
    python -m fabric_health_mcp.server

Requisitos:
    - az login con cuenta que tenga rol Fabric Administrator
    - Ver README.md para configuración en VS Code / Claude Desktop
"""

from mcp.server.fastmcp import FastMCP
from fabric_health_mcp.tools.capacity import get_capacity_health
from fabric_health_mcp.tools.workspaces import get_workspace_score
from fabric_health_mcp.tools.summary import get_tenant_summary, generate_health_report
from fabric_health_mcp.tools.items import get_workspace_items_batch, get_tenant_items_overview

mcp = FastMCP(
    "fabric-health-mcp",
    instructions=(
        "Eres un experto en Microsoft Fabric especializado en health assessment. "
        "Este servidor es complementario al Fabric Core MCP oficial de Microsoft — "
        "mientras el Core MCP gestiona recursos, este MCP los evalúa y puntúa. "
        "Flujo recomendado: primero get_full_tenant_summary para visión general, "
        "luego tools específicas para profundizar en findings críticos. "
        "Responde en español con recomendaciones concretas y accionables. "
        "Para listar workspaces, capacidades o items usa el Fabric Core MCP oficial."
    )
)

# ── Capacidades ──────────────────────────────────────────────────────────────

@mcp.tool()
async def analyze_capacity_health(capacity_id: str) -> str:
    """
    Health score (0-100) de una capacidad específica.
    Evalúa estado, SKU sizing y governance de administradores.
    Usa list_capacities del Fabric Core MCP para obtener los IDs.

    Args:
        capacity_id: ID de la capacidad
    """
    return await get_capacity_health(capacity_id)


# ── Workspaces ────────────────────────────────────────────────────────────────

@mcp.tool()
async def analyze_workspace_score(workspace_id: str) -> str:
    """
    Governance score (0-100) de un workspace específico.
    Evalúa roles, usuarios, capacidad asignada y estado.
    Usa list_workspaces del Fabric Core MCP para obtener los IDs.

    Args:
        workspace_id: ID del workspace
    """
    return await get_workspace_score(workspace_id)


# ── Resumen y Reporte ─────────────────────────────────────────────────────────

@mcp.tool()
async def get_full_tenant_summary() -> str:
    """
    Resumen ejecutivo del tenant: capacidades, workspaces y findings críticos.
    Punto de entrada recomendado — agrega health scores de todo el tenant.
    """
    return await get_tenant_summary()


@mcp.tool()
async def generate_tenant_health_report() -> str:
    """
    Genera un reporte de salud completo en formato Markdown.
    Guarda el archivo health_report_FECHA.md en la carpeta reports/.
    """
    return await generate_health_report()


# ── Items ─────────────────────────────────────────────────────────────────────

@mcp.tool()
async def analyze_workspaces_items_batch(workspace_ids: list[str]) -> str:
    """
    Analiza governance de items en múltiples workspaces en paralelo.
    Detecta items sin descripción y compara governance entre workspaces.
    Usa list_workspaces del Fabric Core MCP para obtener los IDs.

    Args:
        workspace_ids: Lista de IDs de workspaces a analizar
    """
    return await get_workspace_items_batch(workspace_ids)


@mcp.tool()
async def get_tenant_items_summary() -> str:
    """
    Overview de governance de items del tenant.
    Distribución por tipo, items sin descripción, insights de madurez.
    Identifica si el tenant es data-heavy, BI-heavy o AI-heavy.
    """
    return await get_tenant_items_overview()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    mcp.run()


if __name__ == "__main__":
    main()
