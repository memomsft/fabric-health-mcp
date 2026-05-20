"""
Tools de capacidad — Fabric Health MCP v0.1

Endpoints:
  GET /v1/capacities
  GET /v1/capacities/{capacityId}

Nota: CU utilization en tiempo real requiere la Fabric Capacity Metrics App.
      Este tool evalúa configuración y estado, no consumo histórico.
"""

import asyncio
import json
from fabric_health_mcp.fabric_client import FabricClient

_client = FabricClient()

SKU_CU_MAP = {
    "F2": 2, "F4": 4, "F8": 8, "F16": 16,
    "F32": 32, "F64": 64, "F128": 128,
    "F256": 256, "F512": 512, "F1024": 1024, "F2048": 2048,
    "P1": 8, "P2": 16, "P3": 32, "P4": 64,
    "PP3": None, "FTL4": None,  # SKUs especiales sin CU fijo
}


def _parse_sku(sku_raw) -> str:
    """La API puede devolver sku como string 'F8' o como objeto {'name': 'F8'}."""
    if isinstance(sku_raw, dict):
        return sku_raw.get("name", "Desconocido")
    return str(sku_raw) if sku_raw else "Desconocido"


async def _get_admins_map() -> dict[str, list[str]]:
    """
    Devuelve un dict {capacity_id: [admin_upn, ...]} usando la PowerBI Admin API,
    que sí expone el campo 'admins' (la Fabric API lo omite).
    """
    try:
        data = await _client.get_powerbi("/admin/capacities")
        return {cap["id"]: cap.get("admins", []) for cap in data.get("value", [])}
    except Exception:
        return {}


async def list_capacities() -> str:
    """Lista todas las capacidades del tenant con SKU, estado y región."""
    try:
        data = await _client.get("/capacities")
        capacities = data.get("value", [])

        if not capacities:
            return json.dumps({
                "message": "No se encontraron capacidades.",
                "tip": "Verifica que tu cuenta tenga rol Fabric Administrator."
            }, ensure_ascii=False, indent=2)

        admins_map = await _get_admins_map()

        summary = []
        for cap in capacities:
            sku_name = _parse_sku(cap.get("sku"))
            cap_id = cap.get("id")
            summary.append({
                "id": cap_id,
                "display_name": cap.get("displayName"),
                "sku": sku_name,
                "max_cu": SKU_CU_MAP.get(sku_name, "N/A"),
                "state": cap.get("state"),
                "region": cap.get("region"),
                "admins": admins_map.get(cap_id, []),
            })

        return json.dumps({
            "total_capacities": len(summary),
            "capacities": summary
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return _error(e)


async def get_capacity_health(capacity_id: str) -> str:
    """
    Health score (0-100) de una capacidad específica.
    Evalúa: estado, SKU sizing, y governance de administradores.
    """
    try:
        # GET /capacities/{id} no está soportado por la Fabric API — filtramos desde la lista
        data, admins_map = await asyncio.gather(
            _client.get("/capacities"),
            _get_admins_map(),
        )
        all_caps = data.get("value", [])
        cap = next((c for c in all_caps if c.get("id") == capacity_id), None)
        if cap is None:
            return json.dumps({"error": f"Capacidad '{capacity_id}' no encontrada."}, ensure_ascii=False, indent=2)

        sku_name = _parse_sku(cap.get("sku"))
        state = cap.get("state", "Unknown")
        display_name = cap.get("displayName", capacity_id)
        region = cap.get("region", "Desconocida")
        admins = admins_map.get(capacity_id, [])
        max_cu = SKU_CU_MAP.get(sku_name)

        score = 100
        findings = []
        recommendations = []

        # Estado
        if state == "Suspended":
            score -= 40
            findings.append("CRÍTICO: Capacidad suspendida — todos los workloads están detenidos.")
            recommendations.append("Revisa el estado de pago o límites de crédito en el portal de Azure.")
        elif state == "Paused":
            score -= 20
            findings.append("ADVERTENCIA: Capacidad pausada.")
            recommendations.append("Considera automatizar pause/resume con Azure Automation si es intencional fuera de horario.")
        elif state == "Active":
            findings.append("OK: Capacidad activa.")

        # SKU sizing
        if max_cu is not None and max_cu <= 4:
            score -= 15
            findings.append(f"ADVERTENCIA: SKU {sku_name} ({max_cu} CU) es pequeño para cargas productivas.")
            recommendations.append("Para producción se recomienda mínimo F8. Considera este SKU solo para dev/test.")

        # Admins
        if len(admins) == 0:
            score -= 20
            findings.append("CRÍTICO: Sin administradores asignados.")
            recommendations.append("Asigna al menos un administrador a esta capacidad.")
        elif len(admins) > 5:
            score -= 5
            findings.append(f"ADVERTENCIA: {len(admins)} administradores (principio de menor privilegio).")

        score = max(0, score)

        return json.dumps({
            "capacity_id": capacity_id,
            "display_name": display_name,
            "sku": sku_name,
            "max_cu": max_cu,
            "state": state,
            "region": region,
            "admins_count": len(admins),
            "health_score": score,
            "grade": _grade(score),
            "findings": findings,
            "recommendations": recommendations,
            "note": "Para CU utilization en tiempo real instala la Fabric Capacity Metrics App."
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
