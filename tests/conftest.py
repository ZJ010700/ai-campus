"""
测试公共 fixtures。

提供测试数据库、测试客户端、测试用户等公共测试依赖。
"""
import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_async_session
from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from main import app

# =============================================================================
# 测试数据库配置
# =============================================================================

# 使用 SQLite 作为测试数据库（异步）
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 创建测试引擎
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

# 创建测试会话工厂
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """
    创建事件循环，整个测试 session 共享。

    pytest-asyncio 需要一个事件循环来运行异步测试。
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    创建测试数据库会话。

    每个测试函数都会：
    1. 创建所有表
    2. 生成一个数据库会话
    3. 测试结束后回滚并删除所有表
    """
    # 创建所有表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建会话
    async with TestSessionLocal() as session:
        yield session

    # 删除所有表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    创建测试 HTTP 客户端。

    使用 httpx.AsyncClient 配合 ASGITransport，
    将数据库会话注入到应用的依赖中。
    """
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """
    创建测试用户。

    返回一个已持久化到测试数据库的用户对象。
    """
    user = User(
        username="testuser",
        email="testuser@example.com",
        password_hash=get_password_hash("testpassword123"),
        nickname="测试用户",
        role="student",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_user_token(test_user: User) -> str:
    """
    生成测试用户的 JWT access token。
    """
    return create_access_token(data={"sub": str(test_user.id)})


@pytest_asyncio.fixture(scope="function")
async def auth_headers(test_user_token: str) -> dict:
    """
    生成认证请求头。

    返回包含 Authorization Bearer token 的请求头字典。
    """
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest_asyncio.fixture(scope="function")
async def auth_client(
    client: AsyncClient, auth_headers: dict
) -> AsyncGenerator[AsyncClient, None]:
    """
    创建带认证的测试客户端。

    所有请求会自动附带 Authorization 头。
    """
    client.headers.update(auth_headers)
    yield client
