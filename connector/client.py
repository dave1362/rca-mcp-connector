"""
RCA-MCP Public Connector — HTTP Forwarding Client
====================================================
Thin async HTTP client that forwards MCP tool calls to the private
RCA-MCP API endpoint. Contains zero business logic — every tool call
is a JSON pass-through to the private API, which owns all analytical
depth, security enforcement, and tier gating.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict

import httpx


class RCAMCPClient:
    """
    Thin async HTTP client that forwards MCP tool calls
    to the private RCA-MCP API endpoint.
    """

    DEFAULT_API_URL = "https://rcamcp-production.up.railway.app"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        # Never raise here -- construction (and therefore importing this
        # module / starting the MCP server) must succeed even with no env
        # vars set, so the server can be installed/inspected/started
        # before a real API key is configured. A missing key degrades to
        # a clear per-call error from call() below instead of crashing
        # the whole process at import time.
        self._base = (
            base_url or os.environ.get("RCA_MCP_API_URL") or self.DEFAULT_API_URL
        ).rstrip("/")
        self._api_key = api_key or os.environ.get("RCA_MCP_API_KEY", "")
        if not self._api_key:
            print(
                "RCA-MCP: RCA_MCP_API_KEY not set. Tool calls will fail until "
                "it's configured -- see "
                "https://github.com/dave1362/rca-mcp-connector#quick-start-2-minutes",
                file=sys.stderr,
            )
        self._headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "X-RCA-MCP-Version": "3.0",
        }

    async def call(self, endpoint: str, payload: Dict[str, Any]) -> str:
        """Forward a tool call to the private API. Returns JSON string."""
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(120.0, connect=10.0)
        ) as http:
            try:
                resp = await http.post(
                    f"{self._base}/v1/{endpoint}",
                    json=payload,
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.text
            except httpx.HTTPStatusError as e:
                return f'{{"status":"error","error":"API error {e.response.status_code}: {e.response.text[:200]}"}}'
            except httpx.TimeoutException:
                return '{"status":"error","error":"Request timed out after 120s."}'
            except Exception as e:
                return f'{{"status":"error","error":"Connection failed: {str(e)}"}}'
