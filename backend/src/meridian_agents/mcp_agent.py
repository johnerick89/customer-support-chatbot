from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from agents import Runner
from agents.mcp import MCPServerManager
from agents.result import RunResultStreaming

from ..mcp.mcp_client import create_order_mcp_server
from .customer_support_agent import create_customer_support_agent


async def _stream_text(result: RunResultStreaming) -> AsyncIterator[str]:
    async for event in result.stream_events():
        if (
            event.type == "raw_response_event"
            and event.data.type == "response.output_text.delta"
        ):
            yield event.data.delta


class MCPAgent:
    """
    OpenAI Agents SDK + Streamable HTTP MCP (Meridian order tools).
    """

    def __init__(self) -> None:
        self.server = create_order_mcp_server()

    async def stream(
        self,
        prompt: str,
        *,
        customer: dict[str, Any],
    ) -> AsyncIterator[str]:
        customer_id = customer.get("customer_id")
        customer_name = customer.get("name")
        customer_email = customer.get("email")

        enriched_prompt = f"""
You are a customer support assistant for Meridian Electronics.

Authenticated customer:
- Name: {customer_name}
- Customer ID: {customer_id}
- Email: {customer_email or "(not provided)"}

You can:
- search products
- list products
- check orders (use customer_id for the authenticated shopper)
- place orders (must confirm first)

User message:
{prompt}
"""

        async with MCPServerManager(
            [self.server],
            strict=False,
            connect_timeout_seconds=60.0,
        ) as manager:
            active_servers = manager.active_servers

            if not active_servers:
                err = manager.errors.get(self.server)
                yield f"Failed to connect to MCP server: {err}"
                return

            agent = create_customer_support_agent(active_servers)
            result = Runner.run_streamed(agent, enriched_prompt)

            async for chunk in _stream_text(result):
                yield chunk
