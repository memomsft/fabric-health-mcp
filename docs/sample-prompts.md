# Prompts de Ejemplo — fabric-health-mcp

Prompts validados contra tenants reales. Ejecutar en **Copilot Chat modo Agent** en VS Code.

> **Tip:** Si tienes múltiples MCPs conectados, abre el proyecto en VS Code desde la carpeta
> `fabric-health-mcp` para que Copilot priorice el servidor correcto.

---

## Assessment completo

```
Genera un reporte ejecutivo de salud de mi tenant de Fabric.
Quiero saber: estado de mis capacidades, qué workspaces están en riesgo,
qué items no están gobernados, y las 3 acciones más urgentes que debería tomar hoy.
```

```
Actúa como consultor de Microsoft Fabric.
Analiza mi tenant y dame un plan de acción priorizado para las próximas 2 semanas.
```

---

## Capacidades

```
¿Cuál es el estado de salud de mis capacidades de Fabric?
```

```
¿Alguna de mis capacidades está en riesgo o mal configurada?
```

```
¿El SKU de mis capacidades es adecuado para cargas de producción?
```

---

## Workspaces

```
¿Hay workspaces huérfanos o sin usuarios asignados en mi tenant?
```

```
¿Cuántos workspaces no tienen capacidad de Fabric asignada?
```

```
Evalúa el governance del workspace [nombre o ID]
```

---

## Items y Governance

```
¿Cuántos items de Fabric no tienen descripción y cuáles son los más críticos para documentar primero?
```

```
¿Qué workspaces de mi tenant tienen peor governance de items?
```

```
¿Qué tipo de workloads está usando más mi tenant — datos, BI o AI?
```

```
¿Qué items de tipo DataAgent existen y en qué workspaces están?
```

---

## Reporte final

```
Genera el reporte completo de salud del tenant y guárdalo como Markdown
```

---

## Hallazgos reales (validados)

Estos prompts han devuelto insights reales en ambientes de prueba:

| Prompt | Insight obtenido |
|--------|-----------------|
| Items sin documentar | Detecta % de items sin descripción por workspace |
| Workloads más usados | Identifica si el tenant es data-heavy, BI-heavy o AI-heavy |
| Workspaces huérfanos | Encuentra workspaces sin usuarios asignados |
| Estado de capacidades | Detecta capacidades sin admins asignados |
| Overview de items | 63 items en 6 workspaces — Lakehouses dominante |
