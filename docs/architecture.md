# Arquitectura — fabric-health-mcp

## Flujo general

```
AI Client (VS Code + GitHub Copilot)
         │
         │  MCP stdio (proceso local)
         ▼
fabric-health-mcp  (Python)
├── Auth: AzureCliCredential (az login)
├── Capacidades: list · analyze_health
├── Workspaces:  list · score
├── Items:       list · batch · overview
├── Resumen:     get_full_tenant_summary
└── Reporte:     generate_health_report (.md)
         │
         │  HTTPS · REST API
         ├──────────────────────────────────┐
         ▼                                  ▼
Fabric Admin API                  Power BI Admin API
api.fabric.microsoft.com/v1       api.powerbi.com/v1.0/myorg
workspaces · items                admins de capacidad
         │                                  │
         └──────────────┬───────────────────┘
                        ▼
              Microsoft Fabric Tenant
```

---

## Cómo funciona el scoring

Cada tool de análisis devuelve un **health score de 0 a 100** calculado
restando puntos por condiciones negativas encontradas.

### Score de capacidad (`analyze_capacity_health`)

| Condición | Puntos restados |
|-----------|----------------|
| Capacidad suspendida | -40 |
| Capacidad pausada | -20 |
| SKU ≤ F4 (muy pequeño para producción) | -15 |
| Sin administradores asignados | -20 |
| Más de 5 administradores | -5 |

### Score de workspace (`analyze_workspace_score`)

| Condición | Puntos restados |
|-----------|----------------|
| Sin capacidad de Fabric asignada | -30 |
| Estado Deleted | -50 |
| Sin Admin asignado | -25 |
| Más de 3 Admins | -10 |
| Sin usuarios asignados (huérfano) | -15 |

### Grades

| Score | Grade | Significado |
|-------|-------|-------------|
| 90-100 | A — Excelente | Sin issues críticos |
| 75-89 | B — Bueno | Issues menores |
| 60-74 | C — Atención requerida | Revisar findings |
| 40-59 | D — Riesgo alto | Acción pronto |
| 0-39 | F — Crítico | Acción inmediata |

### Estado general del tenant

El `get_full_tenant_summary` calcula el **estado general** basado en:

- 🔴 **Crítico** → alguna capacidad con score < 60, o score promedio < 60
- 🟡 **Advertencia** → score promedio < 75, o más de 5 workspaces sin capacidad
- 🟢 **Saludable** → sin issues críticos y score promedio ≥ 75

---

## Autenticación

El servidor usa `ChainedTokenCredential` de `azure-identity`:

```
1. AzureCliCredential      → usa tu sesión de az login
2. VisualStudioCodeCredential → usa tu sesión de VS Code como fallback
```

`ManagedIdentityCredential` está **excluido intencionalmente** — lanza
`WinError 5` en máquinas Windows que no son VMs de Azure.

### Scopes

| API | Scope |
|-----|-------|
| Fabric REST API | `https://api.fabric.microsoft.com/.default` |
| Power BI Admin API | `https://analysis.windows.net/powerbi/api/.default` |

---

## Decisiones de diseño

**¿Por qué filtrar capacidades desde la lista en vez de GET por ID?**  
`GET /v1/capacities/{id}` devuelve 400 en la API actual. El servidor
obtiene la lista completa y filtra por ID localmente.

**¿Por qué usar Power BI Admin API para admins de capacidad?**  
La Fabric API no expone el campo `admins` en el endpoint de capacidades.
La Power BI Admin API (`/admin/capacities`) sí lo devuelve.

**¿Por qué `ChainedTokenCredential` y no `DefaultAzureCredential`?**  
`DefaultAzureCredential` incluye `ManagedIdentityCredential` que intenta
conectarse a IMDS (metadata de Azure VMs) y falla con `WinError 5`
en Windows local, cortando la cadena antes de llegar a `AzureCliCredential`.
