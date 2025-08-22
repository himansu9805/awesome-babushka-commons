"""Pydantic models for authentication-related payloads."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class CurrentUser(BaseModel):
    """Model for the authenticated user payload.

    Fields:
    - username: optional username string
    - email: optional email address (validated)
    - active: whether the user is active (defaults to True)
    - verified: whether the user's email is verified (defaults to False)
    """

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    active: bool = True
    verified: bool = False

    class Config:
        anystr_strip_whitespace = True
        extra = "ignore"
