"""
Tools de workspaces — Fabric Health MCP v0.1

Endpoints:
  GET /v1/admin/workspaces
  GET /v1/admin/workspaces/{id}/users

Requiere rol: Fabric Administrator
"""

import json
from fabric_health_mcp.fabric_client import FabricClient

_client = FabricClient()


async def list_workspaces() -> str:
    """
    Inventario de todos los workspaces del tenant.
    Identifica workspaces sin capacidad asignada y workspaces personales.
    """
    try:
        workspaces = await _client.get_paginated("/workspaces")

        if not workspaces:
            return json.dumps({
                "message": "No se encontraron workspaces o no tienes permisos de Fabric Admin."
            }, ensure_ascii=False, indent=2)

        no_capacity = []
        personal = []
        summary = []

        for ws in workspaces:
            ws_type = ws.get("type", "Unknown")
            cap_id = ws.get("capacityId")
            entry = {
                "id": ws.get("id"),
                "name": ws.get("displayName"),
                "type": ws_type,
                "state": ws.get("state"),
                "capacity_id": cap_id or "Sin asignar",
            }
            summary.append(entry)

            if not cap_id and ws_type not in ("PersonalGroup", "Personal"):
                no_capacity.append(ws.get("displayName"))
            if ws_type in ("PersonalGroup", "Personal"):
                personal.append(ws.get("displayName"))

        return json.dumps({
            "total_workspaces": len(summary),
            "without_capacity": len(no_capacity),
            "personal_workspaces": len(personal),
            "alert_without_capacity": no_capacity[:10],
            "workspaces": summary,
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _error(e)


async def get_workspace_score(workspace_id: str) -> str:
    """
    Governance score (0-100) de un workspace específico.
    Evalúa: capacidad asignada, roles, usuarios, estado.
    """
    try:
        ws = await _client.get(f"/workspaces/{workspace_id}")
        ws_name = ws.get("displayName") or ws.get("name", workspace_id)
        ws_type = ws.get("type", "Unknown")
        cap_id = ws.get("capacityId")
        state = ws.get("state", "Unknown")

        users_data = await _client.get(f"/admin/workspaces/{workspace_id}/users")
        users = users_data.get("accessDetails", users_data.get("value", []))

        score = 100
        findings = []
        recommendations = []

        # Capacidad
        if not cap_id and ws_type not in ("PersonalGroup", "Personal"):
            score -= 30
            findings.append("CRÍTICO: Workspace sin capacidad de Fabric asignada.")
            recommendations.append("Asigna una capacidad F SKU — sin ella los workloads de Fabric no pueden ejecutarse.")

        # Estado
        if state == "Deleted":
            score -= 50
            findings.append("CRÍTICO: Workspace en estado Deleted.")
        elif state == "Active":
            findings.append("OK: Workspace activo.")

        # Roles
        role_counts = {}
        for user in users:
            role = user.get("workspaceAccessDetails", {}).get("workspaceRole", "Unknown")
            role_counts[role] = role_counts.get(role, 0) + 1

        admins = role_counts.get("Admin", 0)

        if admins == 0:
            score -= 25
            findings.append("CRÍTICO: Sin Admin asignado al workspace.")
            recommendations.append("Asigna al menos un Admin para garantizar gobierno.")
        elif admins > 3:
            score -= 10
            findings.append(f"ADVERTENCIA: {admins} Admins asignados — considera reducirlos.")

        if len(users) == 0:
            score -= 15
            findings.append("ADVERTENCIA: Sin usuarios asignados — posible workspace huérfano.")
            recommendations.append("Si no está en uso, considera eliminarlo para liberar recursos.")

        score = max(0, score)

        return json.dumps({
            "workspace_id": workspace_id,
            "display_name": ws_name,
            "type": ws_type,
            "state": state,
            "capacity_id": cap_id or "Sin asignar",
            "users": {
                "total": len(users),
                "by_role": role_counts,
            },
            "health_score": score,
            "grade": _grade(score),
            "findings": findings,
            "recommendations": recommendations,
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _error(e)


def _grade(score: int) -> str:
    if score >= 90: return "A — Excelente"
    elif score >= 75: return "B — Bueno"
    elif score >= 60: return "C — Atención requerida"
    elif score >= 40: return "D — Riesgo alto"
    else: return "F — Crítico"


def _error(e: Exception) -> str:
    return json.dumps({
        "error": str(e),
        "tip": "Verifica que hayas corrido 'az login' y que tu cuenta tenga rol Fabric Administrator."
    }, ensure_ascii=False, indent=2)
