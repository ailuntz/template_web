import pytest
from httpx import AsyncClient

from tests.conftest import TEST_REGISTRATION_INSTITUTION_CODE


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    """Test user registration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
            "institution_code": TEST_REGISTRATION_INSTITUTION_CODE,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    """Test registration with duplicate email."""
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "institution_code": TEST_REGISTRATION_INSTITUTION_CODE,
        },
    )

    # Second registration with same email
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password456",
            "institution_code": TEST_REGISTRATION_INSTITUTION_CODE,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_rejects_invalid_institution_code(client: AsyncClient) -> None:
    """Test registration with an invalid institution code."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-code@example.com",
            "password": "password123",
            "institution_code": "123123",
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid institution code"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    """Test successful login."""
    # Register user first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "logintest@example.com",
            "password": "password123",
            "institution_code": TEST_REGISTRATION_INSTITUTION_CODE,
        },
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "logintest@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
