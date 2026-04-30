from __future__ import annotations

import os
from agents.mcp import MCPServerStreamableHttp
from agents.mcp.server import MCPServerStreamableHttpParams


MCP_SERVER_URL = os.getenv(
    "MCP_SERVER_URL",
    "https://order-mcp-74afyau24q-uc.a.run.app/mcp"
)


def create_order_mcp_server() -> MCPServerStreamableHttp:
    """
    Creates a Streamable HTTP MCP server connection
    for Meridian's order system.
    """

    params: MCPServerStreamableHttpParams = {
        "url": MCP_SERVER_URL,
        "headers": {
            "Content-Type": "application/json"
        },
        "timeout": 60.0,
        "sse_read_timeout": 300.0,
        "ignore_initialized_notification_failure": True,
    }

    return MCPServerStreamableHttp(
        params=params,
        cache_tools_list=True,
        name="order-mcp",
        client_session_timeout_seconds=60.0,
    )