from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    email: str = Field(min_length=1)
    pin: str = Field(min_length=1)


class StreamRequest(BaseModel):
    """Chat turn from an authenticated browser session."""

    message: str = Field(min_length=1)
    customer_id: str = Field(
        min_length=1,
        description="Stable customer id from /auth/verify (same as Customer.id).",
    )
    customer_name: str | None = None
    customer_email: str | None = None
