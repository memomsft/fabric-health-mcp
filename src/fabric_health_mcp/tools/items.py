"""
Tools de items — Fabric Health MCP v0.1

Endpoints:
  GET /v1/workspaces/{id}/items        → items de un workspace
  GET /v1/admin/items                  → todos los items del tenant (requiere Fabric Admin)

Tipos de items en Fabric: Lakehouse, Warehouse, Pipeline, Notebook,
Report, SemanticModel, Eventstream, KQLDatabase, SparkJobDefinition, etc.
"""

import json
from fabric_health_mcp.fabric_client import FabricClient

_client = FabricClient()

# Items considerados "de datos" — más relevantes para governance
DATA_ITEM_TYPES = {
    "Lakehouse", "Warehouse", "Pipeline", "Dataflow",
    "Notebook", "SparkJobDefinition", "KQLDatabase",
    "Eventstream", "SemanticModel",
}


async def get_workspace_items(workspace_id: str) -> str:
    """
    Lista todos los items de un workspace con su tipo y metadata.
    Útil para entender qué tan activo y complejo es un workspace.

    Args:
        workspace_id: ID del workspace (obtener con list_all_workspaces)
    """
    try:
        data = await _client.get(f"/workspaces/{workspace_id}/items")
        items = data.get("value", [])

        if not items:
            return json.dumps({
                "workspace_id": workspace_id,
                "message": "No se encontraron items en este workspace.",
            }, ensure_ascii=False, indent=2)

        # Agrupar por tipo
        by_type: dict[str, list] = {}
        for item in items:
            item_type = item.get("type", "Unknown")
            if item_type not in by_type:
                by_type[item_type] = []
            by_type[item_type].append({
                "id": item.get("id"),
                "name": item.get("displayName"),
                "description": item.get("description", ""),
            })

        # Items de datos sin descripción (posible falta de documentación)
        no_description = [
            item.get("displayName")
            for item in items
            if item.get("type") in DATA_ITEM_TYPES and not item.get("description")
        ]

        return json.dumps({
            "workspace_id": workspace_id,
            "total_items": len(items),
            "by_type": {k: {"count": len(v), "items": v} for k, v in sorted(by_type.items())},
            "data_items_without_description": {
                "count": len(no_description),
                "items": no_description[:10],
            },
            "tip": "Items sin descripción son difíciles de gobernar — considera documentarlos."
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _error(e)


async def get_workspace_items_batch(workspace_ids: list[str]) -> str:
    """
    Analiza items de múltiples workspaces en paralelo.
    Devuelve un resumen comparativo por workspace.

    Args:
        workspace_ids: Lista de IDs de workspaces
    """
    import asyncio

    try:
        tasks = [get_workspace_items(ws_id) for ws_id in workspace_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        summary = []
        for ws_id, result in zip(workspace_ids, results):
            if isinstance(result, Exception):
                summary.append({"workspace_id": ws_id, "error": str(result)})
            else:
                data = json.loads(result)
                summary.append({
                    "workspace_id": ws_id,
                    "total_items": data.get("total_items", 0),
                    "by_type": {k: v["count"] for k, v in data.get("by_type", {}).items()},
                    "items_without_description": data.get(
                        "data_items_without_description", {}
                    ).get("count", 0),
                })

        # Ordenar por total de items descendente
        summary.sort(key=lambda x: x.get("total_items", 0), reverse=True)

        return json.dumps({
            "total_workspaces_analyzed": len(summary),
            "workspaces": summary,
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _error(e)


async def get_tenant_items_overview() -> str:
    """
    Resumen de todos los items del tenant agrupados por tipo.
    Requiere rol Fabric Administrator.
    Útil para entender la distribución y madurez del uso de Fabric.
    """
    try:
        # Primero obtenemos todos los workspaces
        workspaces = await _client.get_paginated("/workspaces")

        if not workspaces:
            return json.dumps({
                "message": "No se encontraron workspaces."
            }, ensure_ascii=False, indent=2)

        import asyncio

        # Items de todos los workspaces en paralelo (máx 10 a la vez)
        semaphore = asyncio.Semaphore(10)

        async def fetch_items(ws):
            async with semaphore:
                try:
                    data = await _client.get(f"/workspaces/{ws['id']}/items")
                    return ws.get("displayName"), data.get("value", [])
                except Exception:
                    return ws.get("displayName"), []

        tasks = [fetch_items(ws) for ws in workspaces]
        results = await asyncio.gather(*tasks)

        # Consolidar
        total_by_type: dict[str, int] = {}
        total_items = 0
        workspaces_with_items = 0

        for ws_name, items in results:
            if items:
                workspaces_with_items += 1
            total_items += len(items)
            for item in items:
                item_type = item.get("type", "Unknown")
                total_by_type[item_type] = total_by_type.get(item_type, 0) + 1

        # Ordenar por cantidad
        sorted_types = sorted(total_by_type.items(), key=lambda x: x[1], reverse=True)

        return json.dumps({
            "tenant_items_overview": {
                "total_workspaces": len(workspaces),
                "workspaces_with_items": workspaces_with_items,
                "total_items": total_items,
                "by_type": dict(sorted_types),
                "insight": _items_insight(total_by_type),
            }
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _error(e)


def _items_insight(by_type: dict) -> str:
    """Genera un insight basado en la distribución de items."""
    insights = []

    lakehouses = by_type.get("Lakehouse", 0)
    pipelines = by_type.get("Pipeline", 0)
    notebooks = by_type.get("Notebook", 0)
    reports = by_type.get("Report", 0)
    semantic_models = by_type.get("SemanticModel", 0)

    if lakehouses > 0 and pipelines == 0 and notebooks == 0:
        insights.append("Hay Lakehouses sin pipelines ni notebooks — posible ingesta manual.")
    if reports > 0 and semantic_models == 0:
        insights.append("Hay reports sin semantic models explícitos — pueden estar usando datasets heredados.")
    if notebooks > 0 and lakehouses == 0:
        insights.append("Hay notebooks sin Lakehouses — posible uso ad-hoc sin capa de datos estructurada.")

    return " | ".join(insights) if insights else "Distribución de items sin alertas obvias."


def _error(e: Exception) -> str:
    return json.dumps({
        "error": str(e),
        "tip": "Verifica que hayas corrido 'az login' y que tu cuenta tenga rol Fabric Administrator."
    }, ensure_ascii=False, indent=2)
