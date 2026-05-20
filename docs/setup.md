# Guía de Setup

## Requisitos previos

| Requisito | Versión mínima | Verificar |
|-----------|---------------|-----------|
| Python | 3.10+ | `python --version` |
| Azure CLI | Cualquiera reciente | `az --version` |
| Rol en Fabric | Fabric Administrator | Portal de Admin de Fabric |
| VS Code | Cualquiera reciente | Con extensión GitHub Copilot |

---

## Windows

### 1. Clonar el repositorio

```powershell
git clone https://github.com/TU_ORG/fabric-health-mcp
cd fabric-health-mcp
```

### 2. Instalar dependencias

```powershell
pip install -e .
```

> **Nota importante en Windows con Anaconda/Conda:**  
> Si tienes múltiples versiones de Python, verifica cuál usa pip:
> ```powershell
> conda run where python
> ```
> Anota el path de Conda (ej. `C:\Users\TU_USUARIO\AppData\Local\anaconda3\python.exe`).
> Lo necesitarás en el paso de configuración de VS Code.

### 3. Autenticación

```powershell
az login
```

Se abre el browser. Inicia sesión con la cuenta que tenga rol **Fabric Administrator**.

### 4. Configurar VS Code + GitHub Copilot

Abre el Command Palette en VS Code:
```
Ctrl + Shift + P → MCP: Open User Configuration
```

Agrega el servidor dentro de `"servers"`:

```json
{
  "servers": {
    "fabric-health": {
      "command": "C:\\Users\\TU_USUARIO\\AppData\\Local\\anaconda3\\python.exe",
      "args": ["-m", "fabric_health_mcp.server"]
    }
  }
}
```

> Si no usas Anaconda y Python está en el PATH, puedes usar simplemente `"python"` como command.

### 5. Verificar que el servidor está corriendo

```
Ctrl + Shift + P → MCP: List Servers
```

`fabric-health` debe aparecer en estado **Running**.

### 6. Primer uso

En Copilot Chat (modo **Agent**):
```
Genera un resumen de salud de mi tenant de Fabric
```

---

## macOS

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_ORG/fabric-health-mcp
cd fabric-health-mcp
```

### 2. Instalar dependencias

```bash
pip install -e .
```

### 3. Autenticación

```bash
az login
```

### 4. Configurar VS Code + GitHub Copilot

```
Cmd + Shift + P → MCP: Open User Configuration
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

> Si usas `pyenv` o Conda en Mac, usa el path completo:
> ```bash
> which python  # copia el output aquí
> ```

### 5. Verificar y usar

Igual que en Windows — `MCP: List Servers` y luego Copilot Chat en modo Agent.

---

## Solución de problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: fabric_health_mcp` | VS Code usa Python diferente al de `pip install` | Usa el path completo de Python en `mcp.json` |
| `WinError 5 / ManagedIdentityCredential` | Versión vieja de `azure-identity` | `pip install --upgrade azure-identity` con el Python correcto |
| `No se encontraron capacidades` | Cuenta sin rol Fabric Admin | Verifica permisos en el portal de Admin de Fabric |
| Servidor en estado Error en VS Code | Ver logs: `MCP: List Servers → Show Output` | Revisar el traceback completo |
