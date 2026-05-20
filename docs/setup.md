# Guía de Setup — fabric-health-mcp

## Requisitos previos

| Requisito | Versión mínima | Verificar |
|-----------|---------------|-----------|
| Python | 3.10+ | `python --version` |
| Azure CLI | Cualquiera reciente | `az --version` |
| Rol en Fabric | Fabric Administrator | Portal Admin de Fabric |
| VS Code | Cualquiera reciente | Con extensión GitHub Copilot |

---

## Windows

### 1. Clonar el repositorio

```powershell
git clone https://github.com/memomsft/fabric-health-mcp
cd fabric-health-mcp
```

### 2. Instalar dependencias

```powershell
pip install -e .
```

> **Importante con Anaconda/Conda:**  
> Si tienes múltiples versiones de Python, verifica cuál usa pip:
> ```powershell
> conda run where python
> ```
> Anota el path de Conda — lo necesitarás en el paso 4.

### 3. Autenticación (una sola vez)

```powershell
az login
```

Se abre el browser. Inicia sesión con la cuenta que tenga rol **Fabric Administrator**.

### 4. Configurar VS Code + GitHub Copilot

```
Ctrl+Shift+P → MCP: Open User Configuration
```

Agrega el servidor dentro de `"servers"`:

```json
{
  "servers": {
    "fabric-health": {
      "type": "stdio",
      "command": "C:\\Users\\TU_USUARIO\\AppData\\Local\\anaconda3\\python.exe",
      "args": ["-m", "fabric_health_mcp.server"]
    }
  }
}
```

> Si no usas Anaconda y Python está en el PATH, usa `"python"` como command.

### 5. Abrir VS Code en la carpeta del proyecto

```powershell
code C:\ruta\a\fabric-health-mcp
```

Esto es importante — Copilot lee el archivo `.github/copilot-instructions.md` 
y sabe que debe usar el servidor `fabric-health` para preguntas de Fabric.

### 6. Verificar que el servidor está corriendo

```
Ctrl+Shift+P → MCP: List Servers
```

`fabric-health` debe aparecer en estado **Running** con **9 tools**.

### 7. Primer uso

En Copilot Chat (modo **Agent**):
```
¿Cuál es el estado de salud de mis capacidades de Fabric?
```

---

## macOS

### 1. Clonar e instalar

```bash
git clone https://github.com/memomsft/fabric-health-mcp
cd fabric-health-mcp
pip install -e .
az login
```

### 2. Configurar VS Code

```
Cmd+Shift+P → MCP: Open User Configuration
```

```json
{
  "servers": {
    "fabric-health": {
      "command": "python",
      "args": ["-m", "fabric_health_mcp.server"]
    }
  }
}
```

> Si usas pyenv o Conda en Mac:
> ```bash
> which python  # usa este path en el config
> ```

---

## Solución de problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: fabric_health_mcp` | VS Code usa Python diferente al de `pip install` | Usa el path completo de Python en `mcp.json` |
| `WinError 5 / ManagedIdentityCredential` | Versión vieja de `azure-identity` | `C:\ruta\anaconda3\python.exe -m pip install --upgrade azure-identity` |
| Servidor en estado Error | Ver logs en MCP: List Servers → Show Output | Revisar el traceback completo |
| Copilot usa otro MCP | Múltiples MCPs conectados | Abre VS Code desde la carpeta del proyecto |
| JSON inválido en mcp.json | Llave o coma faltante | Verifica que el JSON tiene todos los `}` cerrados |

---

## Notas de seguridad

- El servidor corre **100% local** — ningún dato sale hacia servicios externos
- Los reportes generados se guardan en `reports/` — excluidos del `.gitignore`
- No se almacenan credenciales — usa tu sesión activa de `az login`
- Ver [SECURITY.md](../SECURITY.md) para más detalles
