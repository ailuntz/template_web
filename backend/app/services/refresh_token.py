from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.refresh_token import RefreshToken


async def create_refresh_token_record(
    db: AsyncSession,
    user_id: int,
    token: str,
    token_family: str,
    device_info: str | None = None,
) -> RefreshToken:
    """Create a new refresh token record in the database."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )

    refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        token_family=token_family,
        expires_at=expires_at,
        device_info=device_info,
    )

    db.add(refresh_token)
    await db.flush()
    await db.refresh(refresh_token)
    return refresh_token


async def get_refresh_token(
    db: AsyncSession, token: str
) -> RefreshToken | None:
    """Get a refresh token record by token string."""
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    return result.scalar_one_or_none()


async def revoke_refresh_token(db: AsyncSession, token: RefreshToken) -> None:
    """Mark a refresh token as revoked."""
    token.revoked = True
    await db.flush()


async def revoke_all_user_tokens(db: AsyncSession, user_id: int) -> None:
    """Revoke all refresh tokens for a user."""
    await db.execute(
        delete(RefreshToken).where(RefreshToken.user_id == user_id)
    )
    await db.flush()


async def revoke_token_family(db: AsyncSession, token_family: str) -> None:
    """Revoke all tokens in a token family (for replay attack detection)."""
    await db.execute(
        delete(RefreshToken).where(RefreshToken.token_family == token_family)
    )
    await db.flush()


async def cleanup_expired_tokens(db: AsyncSession) -> int:
    """Delete expired refresh tokens from the database."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        delete(RefreshToken).where(RefreshToken.expires_at < now)
    )
    await db.flush()
    return result.rowcount
