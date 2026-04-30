import hashlib
import logging

from fastapi import APIRouter, HTTPException

from ...schemas import VerifyRequest
from ..mcp.verify_customer import (
    VerifyMcpError,
    auth_stub_enabled,
    verify_customer_pin,
)

logger = logging.getLogger(__name__)

router = APIRouter()


def _prototype_customer(email: str) -> dict[str, str]:
    """Only used when AUTH_MCP_STUB=1 (no MCP / offline demos)."""
    local = email.split("@", 1)[0].replace(".", " ").strip() or "Customer"
    name = local.title()
    digest = hashlib.sha256(email.encode()).hexdigest()[:12]
    cid = f"cust-{digest}"
    return {
        "id": cid,
        "customer_id": cid,
        "email": email,
        "pin": "",
        "name": name,
        "role": "demo",
    }


@router.post("/auth/verify")
async def verify_customer_route(body: VerifyRequest) -> dict[str, str]:
    """
    Authenticates via MCP tool **verify_customer_pin** (email + PIN).
    """
    email = body.email.strip()
    pin = body.pin.strip()
    if not email or not pin:
        raise HTTPException(
            status_code=400,
            detail="Email and PIN are required",
        )

    if auth_stub_enabled():
        logger.warning("AUTH_MCP_STUB is set — using prototype auth, not MCP")
        return _prototype_customer(email)

    try:
        return await verify_customer_pin(email, pin)
    except VerifyMcpError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("MCP verify_customer_pin failed")
        raise HTTPException(
            status_code=502,
            detail="Could not reach authentication service. Try again later.",
        ) from exc
