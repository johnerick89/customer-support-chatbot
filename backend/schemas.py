from typing import Literal

from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    email: str = Field(min_length=1)
    pin: str = Field(min_length=1)


class ChatHistoryItem(BaseModel):
    """One prior turn in the browser session (user or assistant)."""

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class StreamRequest(BaseModel):
    """Chat turn from an authenticated browser session."""

    message: str = Field(min_length=1)
    history: list[ChatHistoryItem] = Field(
        default_factory=list,
        description="Completed turns before `message` (alternating user/assistant).",
    )
    customer_id: str = Field(
        min_length=1,
        description="Stable customer id from /auth/verify (same as Customer.id).",
    )
    customer_name: str | None = None
    customer_email: str | None = None
    customer_role: str | None = None
