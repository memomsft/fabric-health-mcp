"""
Tool de resumen ejecutivo — Fabric Health MCP v0.1
Agrega datos de capacidades y workspaces en un único resumen del tenant.
"""

import json
from fabric_health_mcp.tools.capacity import list_capacities, get_capacity_health
from fabric_health_mcp.tools.workspaces import list_workspaces


async def get_tenant_summary() -> str:
    """
    Resumen ejecutivo del tenant: capacidades, workspaces y findings críticos.
    Úsalo como punto de entrada para el health assessment completo.
    """
    try:
        # Capacidades
        caps_raw = json.loads(await list_capacities())
        capacities = caps_raw.get("capacities", [])

        cap_scores = []
        for cap in capacities:
            cap_id = cap.get("id")
            if cap_id:
                health_raw = json.loads(await get_capacity_health(cap_id))
                cap_scores.append({
                    "name": cap.get("display_name"),
                    "sku": cap.get("sku"),
                    "state": cap.get("state"),
                    "score": health_raw.get("health_score"),
                    "grade": health_raw.get("grade"),
                    "critical_findings": [
                        f for f in health_raw.get("findings", [])
                        if f.startswith("CRÍTICO")
                    ],
                })

        # Workspaces
        ws_raw = json.loads(await list_workspaces())
        total_ws = ws_raw.get("total_workspaces", 0)
        without_capacity = ws_raw.get("without_capacity", 0)
        personal_ws = ws_raw.get("personal_workspaces", 0)
        alert_ws = ws_raw.get("alert_without_capacity", [])

        # Score global de capacidades
        scores = [c["score"] for c in cap_scores if c["score"] is not None]
        avg_cap_score = round(sum(scores) / len(scores)) if scores else 0

        critical_caps = [c for c in cap_scores if c["score"] is not None and c["score"] < 60]

        # Findings críticos consolidados
        all_critical = []
        for c in cap_scores:
            for f in c.get("critical_findings", []):
                all_critical.append(f"[Capacidad: {c['name']}] {f}")

        if without_capacity > 0:
            all_critical.append(
                f"[Workspaces] {without_capacity} workspace(s) sin capacidad de Fabric asignada: "
                f"{', '.join(alert_ws[:5])}"
            )

        return json.dumps({
            "tenant_summary": {
                "capacities": {
                    "total": len(capacities),
                    "avg_health_score": avg_cap_score,
                    "critical_count": len(critical_caps),
                    "detail": cap_scores,
                },
                "workspaces": {
                    "total": total_ws,
                    "without_capacity": without_capacity,
                    "personal": personal_ws,
                    "health_note": (
                        f"{without_capacity} workspace(s) sin capacidad asignada"
                        if without_capacity > 0 else "Todos los workspaces tienen capacidad asignada"
                    ),
                },
                "critical_findings": all_critical,
                "overall_status": _overall_status(avg_cap_score, len(critical_caps), without_capacity),
            }
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


async def generate_health_report() -> str:
    """
    Genera un reporte de salud completo en formato Markdown.
    El archivo se guarda en el workspace actual como health_report_FECHA.md
    """
    import os
    from datetime import datetime

    try:
        summary_raw = json.loads(await get_tenant_summary())
        summary = summary_raw.get("tenant_summary", {})

        caps = summary.get("capacities", {})
        ws = summary.get("workspaces", {})
        findings = summary.get("critical_findings", [])
        status = summary.get("overall_status", "Desconocido")
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        file_date = datetime.now().strftime("%Y%m%d_%H%M")

        lines = [
            f"# Fabric Health Report",
            f"",
            f"**Generado:** {date_str}  ",
            f"**Estado general:** {status}",
            f"",
            f"---",
            f"",
            f"## Resumen Ejecutivo",
            f"",
            f"| Dimensión | Valor |",
            f"|-----------|-------|",
            f"| Capacidades | {caps.get('total', 0)} total — Score promedio: {caps.get('avg_health_score', 0)}/100 |",
            f"| Workspaces | {ws.get('total', 0)} total — {ws.get('without_capacity', 0)} sin capacidad asignada |",
            f"| Findings críticos | {len(findings)} |",
            f"",
            f"---",
            f"",
            f"## Capacidades",
            f"",
            f"| Nombre | SKU | Estado | Score | Grade |",
            f"|--------|-----|--------|-------|-------|",
        ]

        for cap in caps.get("detail", []):
            lines.append(
                f"| {cap.get('name')} | {cap.get('sku')} | {cap.get('state')} "
                f"| {cap.get('score')}/100 | {cap.get('grade')} |"
            )

        lines += [
            f"",
            f"---",
            f"",
            f"## Workspaces",
            f"",
            f"| Métrica | Valor |",
            f"|---------|-------|",
            f"| Total workspaces | {ws.get('total', 0)} |",
            f"| Sin capacidad asignada | {ws.get('without_capacity', 0)} |",
            f"| Workspaces personales | {ws.get('personal', 0)} |",
            f"",
        ]

        if findings:
            lines += [
                f"---",
                f"",
                f"## ⚠️ Findings Críticos",
                f"",
            ]
            for f in findings:
                lines.append(f"- {f}")
            lines.append("")

        lines += [
            f"---",
            f"",
            f"## Roadmap de Próximas Versiones",
            f"",
            f"- **v0.2:** Data Freshness — pipelines fallidos, semantic models sin refresh",
            f"- **v0.3:** Adopción — items sin uso en 30/60/90 días",
            f"- **v0.4:** Maturity Score completo por workspace",
            f"",
            f"---",
            f"*Generado por fabric-health-mcp v0.1*",
        ]

        content = "\n".join(lines)

        # Guardar archivo
        reports_dir = os.environ.get("FABRIC_HEALTH_REPORTS_DIR", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"health_report_{file_date}.md"
        filepath = os.path.join(reports_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return json.dumps({
            "success": True,
            "file": filepath,
            "message": f"Reporte generado: {filepath}",
            "preview": content[:500] + "..."
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


def _overall_status(avg_score: int, critical_caps: int, ws_no_cap: int) -> str:
    if critical_caps > 0 or avg_score < 60:
        return "🔴 Crítico — Requiere atención inmediata"
    elif avg_score < 75 or ws_no_cap > 5:
        return "🟡 Advertencia — Revisar findings"
    else:
        return "🟢 Saludable"
