"""
Cliente base para Microsoft Fabric REST APIs.
Usa ChainedTokenCredential — compatible con az login y VS Code auth.
ManagedIdentityCredential excluido intencionalmente (WinError 5 en Windows local).
"""

import httpx
from azure.identity import AzureCliCredential, ChainedTokenCredential, VisualStudioCodeCredential
from typing import Any

FABRIC_BASE_URL = "https://api.fabric.microsoft.com/v1"
FABRIC_SCOPE = "https://api.fabric.microsoft.com/.default"

POWERBI_BASE_URL = "https://api.powerbi.com/v1.0/myorg"
POWERBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"


class FabricClient:
    def __init__(self):
        # Cadena explícita — evita ManagedIdentityCredential que lanza WinError 5
        # en máquinas Windows que no son VMs de Azure
        self._credential = ChainedTokenCredential(
            AzureCliCredential(),
            VisualStudioCodeCredential(),
        )

    def _get_headers(self) -> dict[str, str]:
        token = self._credential.get_token(FABRIC_SCOPE)
        return {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json",
        }

    async def get(self, path: str, params: dict | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{FABRIC_BASE_URL}{path}",
                headers=self._get_headers(),
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def get_powerbi(self, path: str) -> dict[str, Any]:
        """Llama a la PowerBI REST API (scope distinto al de Fabric)."""
        token = self._credential.get_token(POWERBI_SCOPE)
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{POWERBI_BASE_URL}{path}",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_paginated(self, path: str, value_key: str = "value") -> list[dict]:
        """Maneja paginación automáticamente para endpoints que devuelven listas."""
        results = []
        continuation_token = None

        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                params = {}
                if continuation_token:
                    params["continuationToken"] = continuation_token

                response = await client.get(
                    f"{FABRIC_BASE_URL}{path}",
                    headers=self._get_headers(),
                    params=params,
                )
                response.raise_for_status()
                data = response.json()
                results.extend(data.get(value_key, []))

                continuation_token = data.get("continuationToken")
                if not continuation_token:
                    break

        return results
