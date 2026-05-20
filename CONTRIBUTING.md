# Contributing — fabric-health-mcp

Gracias por tu interés en contribuir. Este proyecto sigue un modelo simple de contribución.

## Estructura del proyecto

```
fabric-health-mcp/
├── src/fabric_health_mcp/
│   ├── fabric_client.py      # Cliente HTTP base — Fabric + PowerBI APIs
│   ├── server.py             # Entry point MCP — registro de tools
│   └── tools/
│       ├── capacity.py       # Tools de capacidades
│       ├── workspaces.py     # Tools de workspaces
│       ├── items.py          # Tools de items
│       └── summary.py        # Resumen ejecutivo y reporte
├── docs/                     # Documentación
├── .github/                  # Copilot instructions
└── mcp_config/               # Ejemplos de configuración
```

## Cómo agregar una nueva tool

1. Crea o edita un archivo en `src/fabric_health_mcp/tools/`
2. Implementa la función `async def mi_tool(...) -> str` — siempre devuelve JSON como string
3. Registra la tool en `server.py` con el decorador `@mcp.tool()`
4. Documenta la tool en `docs/tools-reference.md`
5. Agrega prompts de ejemplo en `docs/sample-prompts.md`

## Convenciones

- **Idioma:** código en inglés, docstrings y comentarios en español
- **Output:** todas las tools devuelven `json.dumps(..., ensure_ascii=False, indent=2)`
- **Errores:** siempre captura excepciones y devuelve `_error(e)` — nunca lanzar excepciones al LLM
- **Auth:** usa siempre `FabricClient` — nunca manejar tokens directamente en las tools
- **Naming:** `get_*` para consultas, `analyze_*` para scoring, `generate_*` para output

## Roadmap de contribuciones bienvenidas

- `tools/freshness.py` — pipeline runs, semantic model refresh history (v0.2)
- `tools/adoption.py` — Activity Events API, items sin uso (v0.3)
- `tools/governance.py` — sensitivity labels, endorsement rate (v0.3)
- Soporte para Azure Databricks workspaces (v1.0)

## Reportar bugs

Abre un Issue en GitHub con:
- El prompt que usaste
- El error que recibiste
- El endpoint de la API que falló (si aplica)
