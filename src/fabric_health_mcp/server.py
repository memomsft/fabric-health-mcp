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
from fabric_health_mcp.tools.capacity import list_capacities, get_capacity_health
from fabric_health_mcp.tools.workspaces import list_workspaces, get_workspace_score
from fabric_health_mcp.tools.summary import get_tenant_summary, generate_health_report
from fabric_health_mcp.tools.items import get_workspace_items, get_workspace_items_batch, get_tenant_items_overview

mcp = FastMCP(
    "fabric-health-mcp",
    instructions=(
        "Eres un experto en Microsoft Fabric. Usas estas tools para analizar "
        "la salud, configuración y governance de ambientes Fabric. "
        "Flujo recomendado: primero get_tenant_summary para una visión general, "
        "luego herramientas específicas para profundizar. "
        "Responde en español con recomendaciones concretas y accionables."
    )
)

# ── Capacidades ──────────────────────────────────────────────────────────────

@mcp.tool()
async def list_all_capacities() -> str:
    """
    Lista todas las capacidades de Fabric del tenant.
    Muestra ID, nombre, SKU, CU máximos, estado y región.
    """
    return await list_capacities()


@mcp.tool()
async def analyze_capacity_health(capacity_id: str) -> str:
    """
    Health score (0-100) de una capacidad específica.
    Evalúa estado, SKU sizing y governance de administradores.

    Args:
        capacity_id: ID de la capacidad (obtener con list_all_capacities)
    """
    return await get_capacity_health(capacity_id)


# ── Workspaces ────────────────────────────────────────────────────────────────

@mcp.tool()
async def list_all_workspaces() -> str:
    """
    Inventario de todos los workspaces del tenant.
    Identifica workspaces sin capacidad y workspaces personales.
    Requiere rol Fabric Administrator.
    """
    return await list_workspaces()


@mcp.tool()
async def analyze_workspace_score(workspace_id: str) -> str:
    """
    Governance score (0-100) de un workspace específico.
    Evalúa roles, usuarios, capacidad asignada y estado.

    Args:
        workspace_id: ID del workspace (obtener con list_all_workspaces)
    """
    return await get_workspace_score(workspace_id)


# ── Resumen y Reporte ─────────────────────────────────────────────────────────

@mcp.tool()
async def get_full_tenant_summary() -> str:
    """
    Resumen ejecutivo del tenant: capacidades, workspaces y findings críticos.
    Punto de entrada recomendado para el health assessment completo.
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
async def list_workspace_items(workspace_id: str) -> str:
    """
    Lista todos los items de un workspace agrupados por tipo.
    Detecta items de datos sin descripción (riesgo de governance).

    Args:
        workspace_id: ID del workspace (obtener con list_all_workspaces)
    """
    return await get_workspace_items(workspace_id)


@mcp.tool()
async def analyze_workspaces_items_batch(workspace_ids: list[str]) -> str:
    """
    Analiza items de múltiples workspaces en paralelo.
    Devuelve ranking comparativo por cantidad y tipo de items.

    Args:
        workspace_ids: Lista de IDs de workspaces a analizar
    """
    return await get_workspace_items_batch(workspace_ids)


@mcp.tool()
async def get_tenant_items_summary() -> str:
    """
    Resumen de todos los items del tenant agrupados por tipo.
    Muestra distribución de Lakehouses, Pipelines, Reports, etc.
    Incluye insights sobre madurez del uso de Fabric.
    """
    return await get_tenant_items_overview()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    mcp.run()


if __name__ == "__main__":
    main()
