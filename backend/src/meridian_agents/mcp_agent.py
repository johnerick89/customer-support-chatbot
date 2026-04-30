from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from typing import Any

from agents import Runner
from agents.mcp import MCPServerManager
from agents.result import RunResultStreaming

from ...schemas import ChatHistoryItem
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

    def _session_context_message(
        self,
        *,
        customer_id: Any,
        customer_name: Any,
        customer_email: Any,
        customer_role: Any,
    ) -> str:
        return f"""
You are a customer support assistant for Meridian Electronics.

Authenticated customer:
- Name: {customer_name}
- Customer ID: {customer_id}
- Email: {customer_email or "(not provided)"}
- Role: {customer_role or "(not provided)"}

You can:
- search products
- list products
- check orders (use customer_id for the authenticated shopper)
- place orders (must confirm first)
""".strip()

    def _model_input(
        self,
        *,
        session_context: str,
        history: Sequence[ChatHistoryItem],
        prompt: str,
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = [
            {"role": "developer", "content": session_context},
        ]
        for turn in history:
            items.append({"role": turn.role, "content": turn.content})
        items.append({"role": "user", "content": prompt})
        return items

    async def stream(
        self,
        prompt: str,
        *,
        customer: dict[str, Any],
        history: Sequence[ChatHistoryItem] | None = None,
    ) -> AsyncIterator[str]:
        customer_id = customer.get("customer_id")
        customer_name = customer.get("name")
        customer_email = customer.get("email")
        customer_role = customer.get("role")

        session_context = self._session_context_message(
            customer_id=customer_id,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_role=customer_role,
        )
        turns = list(history) if history else []
        model_input = self._model_input(
            session_context=session_context,
            history=turns,
            prompt=prompt,
        )

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
            result = Runner.run_streamed(agent, model_input)

            async for chunk in _stream_text(result):
                yield chunk
