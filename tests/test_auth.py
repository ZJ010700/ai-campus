"""
认证接口测试。

测试用户注册、登录、刷新令牌等接口。
"""
import pytest
from httpx import AsyncClient


class TestRegister:
    """用户注册接口测试。"""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """测试正常注册流程。"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert data["is_active"] is True

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client: AsyncClient, test_user: User):
        """测试重复用户名注册。"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "another@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "用户名已被注册" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: User):
        """测试重复邮箱注册。"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "anotheruser",
                "email": "testuser@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "邮箱已被注册" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_short_password(self, client: AsyncClient):
        """测试密码过短。"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "shortpwd",
                "email": "shortpwd@example.com",
                "password": "123",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        """测试无效邮箱格式。"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "bademail",
                "email": "not-an-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422


class TestLogin:
    """用户登录接口测试。"""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user: User):
        """测试正常登录流程。"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    @pytest.mark.asyncio
    async def test_login_with_email(self, client: AsyncClient, test_user: User):
        """测试使用邮箱登录。"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser@example.com",
                "password": "testpassword123",
            },
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user: User):
        """测试错误密码。"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """测试不存在的用户。"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "password123",
            },
        )
        assert response.status_code == 401


class TestRefreshToken:
    """刷新令牌接口测试。"""

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client: AsyncClient, test_user: User):
        """测试正常刷新令牌。"""
        # 先登录获取 refresh_token
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123",
            },
        )
        refresh_token = login_response.json()["refresh_token"]

        # 使用 refresh_token 获取新 token
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, client: AsyncClient):
        """测试无效的刷新令牌。"""
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid-token-string"},
        )
        assert response.status_code == 401


# 需要导入 User 类型以供 type hint 使用
from app.models.user import User
