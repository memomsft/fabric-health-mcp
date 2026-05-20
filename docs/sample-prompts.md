# Prompts de Ejemplo

Todos los prompts deben ejecutarse en **Copilot Chat modo Agent** en VS Code.

---

## Assessment completo (recomendado para empezar)

```
Genera un resumen de salud de mi tenant de Fabric
```

```
Genera el reporte completo de salud del tenant y guárdalo como Markdown
```

---

## Capacidades

```
Lista todas las capacidades de Fabric de mi tenant
```

```
Analiza la salud de la capacidad con ID [capacity_id]
```

```
¿Alguna de mis capacidades está en estado crítico o pausado?
```

```
¿El SKU de mis capacidades es adecuado para cargas de producción?
```

---

## Workspaces

```
¿Cuántos workspaces no tienen capacidad de Fabric asignada?
```

```
Evalúa el workspace con ID [workspace_id]
```

```
¿Hay workspaces huérfanos sin usuarios asignados que podría eliminar?
```

---

## Flujo de demo para cliente

```
1. "Dame un resumen ejecutivo del tenant de Fabric"
2. "¿Cuáles son los findings más críticos?"
3. "Analiza en detalle la capacidad [nombre]"
4. "Genera el reporte final en Markdown"
```
