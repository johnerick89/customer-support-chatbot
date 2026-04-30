"""Call MCP tool `verify_customer_pin` over Streamable HTTP."""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

import httpx
import mcp.types as types
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

from .mcp_client import MCP_SERVER_URL

logger = logging.getLogger(__name__)


class VerifyMcpError(Exception):
    """MCP rejected authentication or returned an error payload."""


def _first_str(data: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for k in keys:
        v = data.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return None


def _text_from_tool_result(result: types.CallToolResult) -> str:
    parts: list[str] = []
    for block in result.content:
        if isinstance(block, types.TextContent):
            parts.append(block.text)
        elif getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(p for p in parts if p).strip()


def parse_verify_customer_result_text(blob: str) -> dict[str, str]:
    """
    Parse MCP verify success text, e.g.:

        ✓ Customer verified: Donald Garcia
        Customer ID: 41c2903a-f1a5-47b7-a81d-86b50ade220f
        Email: donaldgarcia@example.net
        Role: admin
    """
    out: dict[str, str] = {}
    text = blob.strip()
    if not text:
        return out

    # Name (same line as "Customer verified:")
    m = re.search(
        r"(?:^|\n)\s*[^\n]*?Customer verified:\s*(.+?)\s*(?:\n|$)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if m:
        out["name"] = m.group(1).strip()

    m = re.search(
        r"(?:^|\n)\s*Customer ID:\s*([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\s*(?:\n|$)",
        text,
        flags=re.IGNORECASE,
    )
    if m:
        out["customer_id"] = m.group(1).strip()

    m = re.search(
        r"(?:^|\n)\s*Email:\s*(\S+)\s*(?:\n|$)",
        text,
        flags=re.IGNORECASE,
    )
    if m:
        out["email"] = m.group(1).strip()

    m = re.search(
        r"(?:^|\n)\s*Role:\s*(.+?)\s*(?:\n|$)",
        text,
        flags=re.IGNORECASE,
    )
    if m:
        out["role"] = m.group(1).strip()

    return out


def _merge_result_blob_into_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Expand ``result`` string field into flat keys when present."""
    merged = dict(data)
    raw = merged.get("result")
    if isinstance(raw, str) and "Customer ID:" in raw:
        for k, v in parse_verify_customer_result_text(raw).items():
            merged.setdefault(k, v)
    return merged


def _parse_tool_payload(result: types.CallToolResult) -> dict[str, Any]:
    data: dict[str, Any] = {}

    if result.structuredContent and isinstance(result.structuredContent, dict):
        data = dict(result.structuredContent)

    text = _text_from_tool_result(result)
    if text:
        try:
            parsed: Any = json.loads(text)
            if isinstance(parsed, dict):
                data = {**data, **parsed}
        except json.JSONDecodeError:
            parsed_lines = parse_verify_customer_result_text(text)
            if parsed_lines:
                data = {**data, **parsed_lines}

    return _merge_result_blob_into_dict(data)


def normalize_customer_session(payload: dict[str, Any]) -> dict[str, str]:
    """
    Map MCP verify_customer_pin output to the frontend Customer shape.
    Supports structured JSON, ``{\"result\": \"...multiline...\"}``, or flat keys.
    """
    payload = _merge_result_blob_into_dict(dict(payload))

    cid = _first_str(payload, ("customer_id", "id", "customerId"))
    if not cid:
        raise VerifyMcpError("verify_customer_pin did not return a customer id")

    email = _first_str(payload, ("email",)) or ""
    name = _first_str(payload, ("name", "full_name", "display_name", "customer_name")) or ""
    role = _first_str(payload, ("role",)) or ""

    out: dict[str, str] = {
        "id": cid,
        "customer_id": cid,
        "email": email,
        "name": name,
        "pin": "",
    }
    if role:
        out["role"] = role
    return out


async def verify_customer_pin(email: str, pin: str) -> dict[str, str]:
    """
    Authenticate via MCP `verify_customer_pin` (email + PIN).

    Raises:
        VerifyMcpError: invalid credentials or tool error text from MCP.
    """
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    timeout = httpx.Timeout(60.0, connect=20.0)

    async with httpx.AsyncClient(timeout=timeout, headers=headers) as http_client:
        async with streamable_http_client(
            MCP_SERVER_URL,
            http_client=http_client,
        ) as (read_stream, write_stream, _get_session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(
                    "verify_customer_pin",
                    arguments={"email": email, "pin": pin},
                )

    if result.isError:
        msg = _text_from_tool_result(result) or "Authentication failed"
        raise VerifyMcpError(msg)

    payload = _parse_tool_payload(result)
    if not payload:
        raise VerifyMcpError(
            _text_from_tool_result(result) or "Empty response from verify_customer_pin",
        )

    try:
        return normalize_customer_session(payload)
    except VerifyMcpError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected verify_customer_pin payload: %s", payload)
        raise VerifyMcpError(f"Invalid verify_customer_pin response: {exc!s}") from exc


def auth_stub_enabled() -> bool:
    """Local/demo only: skip MCP when AUTH_MCP_STUB=1."""
    return os.getenv("AUTH_MCP_STUB", "").strip() in ("1", "true", "yes")
