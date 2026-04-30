import hashlib

from fastapi import APIRouter, HTTPException

from ...schemas import VerifyRequest

router = APIRouter()


@router.post("/auth/verify")
async def verify_customer(body: VerifyRequest) -> dict[str, str]:
    """
    Prototype auth (hashed demo id). Production: MCP verify_customer_pin.
    Response matches frontend Customer + explicit customer_id for APIs.
    """
    email = body.email.strip()
    if not email or not body.pin:
        raise HTTPException(
            status_code=400,
            detail="Email and PIN are required",
        )

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
    }
