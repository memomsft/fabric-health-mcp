# Seguridad

## Qué hace este tool con tus datos

- **Lee** metadata de capacidades y workspaces vía Fabric Admin REST API
- **No modifica** ningún recurso — todas las operaciones son de solo lectura
- **No almacena** credenciales — usa `az login` / `AzureCliCredential`
- **No envía datos** a servicios externos — corre 100% local en tu máquina
- Los reportes `.md` se guardan localmente en la carpeta `reports/`

## Autenticación

Este tool usa `ChainedTokenCredential` de `azure-identity`:

1. `AzureCliCredential` — usa tu sesión activa de `az login`
2. `VisualStudioCodeCredential` — usa tu sesión de VS Code como fallback

**No se usan Service Principals ni secrets por defecto.**  
Si necesitas autenticación desatendida (CI/CD), puedes configurar variables de entorno — ver `.env.example`.

## Permisos requeridos

| Permiso | Para qué |
|---------|----------|
| Fabric Administrator | Leer workspaces, items y usuarios vía Admin API |
| Capacity Administrator | Leer métricas de capacidad (alternativo a Fabric Admin) |

El tool **no requiere** permisos de escritura en ningún momento.

## Buenas prácticas al usar este tool

- No compartas los reportes generados en canales públicos — contienen metadata del tenant
- Revisa el `.gitignore` antes de hacer commit — los reportes están excluidos por defecto
- Si usas Service Principal, rótalo periódicamente y usa el mínimo de permisos necesario

## Reportar vulnerabilidades

Si encuentras un problema de seguridad, por favor repórtalo directamente al autor en vez de abrir un Issue público.
