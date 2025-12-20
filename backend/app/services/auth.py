from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_token_family,
)
from app.schemas.auth import Token
from app.services.refresh_token import (
    create_refresh_token_record,
    get_refresh_token,
    revoke_refresh_token,
    revoke_token_family,
)
from app.services.user import authenticate_user, get_user_by_id


async def login(
    db: AsyncSession, email: str, password: str, device_info: str | None = None
) -> Token | None:
    """Authenticate user and return access and refresh tokens."""
    user = await authenticate_user(db, email, password)
    if not user:
        return None

    # Generate access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    # Generate refresh token
    token_family = generate_token_family()
    refresh_token_jwt = create_refresh_token(
        data={"sub": str(user.id), "family": token_family}
    )

    # Store refresh token in database
    await create_refresh_token_record(
        db, user.id, refresh_token_jwt, token_family, device_info
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token_jwt,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
    )


async def refresh_access_token(
    db: AsyncSession, refresh_token: str, device_info: str | None = None
) -> Token | None:
    """Refresh access token using a valid refresh token."""
    # Decode refresh token
    payload = decode_refresh_token(refresh_token)
    if not payload:
        return None

    user_id = payload.get("sub")
    token_family = payload.get("family")
    if not user_id or not token_family:
        return None

    # Get refresh token from database
    token_record = await get_refresh_token(db, refresh_token)
    if not token_record:
        return None

    # Check if token is revoked (replay attack detection)
    if token_record.revoked:
        # Token has been revoked but is still valid - possible replay attack
        # Revoke entire token family
        await revoke_token_family(db, token_family)
        return None

    # Check if token is expired
    if token_record.expires_at < datetime.now(timezone.utc):
        return None

    # Get user
    user = await get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        return None

    # Revoke old refresh token
    await revoke_refresh_token(db, token_record)

    # Generate new access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    # Generate new refresh token (token rotation)
    new_refresh_token_jwt = create_refresh_token(
        data={"sub": str(user.id), "family": token_family}
    )

    # Store new refresh token in database
    await create_refresh_token_record(
        db, user.id, new_refresh_token_jwt, token_family, device_info
    )

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token_jwt,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
    )
