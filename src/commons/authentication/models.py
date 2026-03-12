"""Pydantic models for authentication-related payloads."""

from pydantic import BaseModel, EmailStr


class CurrentUser(BaseModel):
    """Model for the authenticated user payload.

    Fields:
    - username: username string
    - email: email address
    - active: whether the user is active (defaults to True)
    - verified: whether the user's email is verified (defaults to False)
    """

    username: str
    email: EmailStr
    active: bool = True
    verified: bool = False

    class Config:
        anystr_strip_whitespace = True
        extra = "ignore"
