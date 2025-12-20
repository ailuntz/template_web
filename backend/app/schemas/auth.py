from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int | None = None


class TokenPayload(BaseModel):
    """Token payload schema."""

    sub: str | None = None
    exp: int | None = None


class LoginRequest(BaseModel):
    """Login request schema."""

    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str
