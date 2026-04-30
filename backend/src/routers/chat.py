from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ...schemas import StreamRequest
from ..meridian_agents.mcp_agent import MCPAgent

router = APIRouter()
_agent = MCPAgent()


async def _stream_response(body: StreamRequest) -> StreamingResponse:
    customer = {
        "customer_id": body.customer_id.strip(),
        "name": (body.customer_name or body.customer_email or "Customer").strip()
        or "Customer",
        "email": (body.customer_email or "").strip() or None,
    }

    async def generator():
        try:
            async for chunk in _agent.stream(
                prompt=body.message,
                customer=customer,
            ):
                yield chunk
        except Exception as exc:  # noqa: BLE001 — stream a safe error to the client
            yield f"[support error] {exc!s}"

    return StreamingResponse(generator(), media_type="text/plain")


@router.post("/stream")
async def stream_chat(body: StreamRequest) -> StreamingResponse:
    return await _stream_response(body)


@router.post("/api/stream")
async def stream_chat_api_prefix(body: StreamRequest) -> StreamingResponse:
    """Same handler; supports Next rewrite path `/api/stream` on Vercel."""
    return await _stream_response(body)
