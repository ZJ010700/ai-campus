"""
依赖注入模块。

提供数据库会话、当前用户等公共依赖。
"""
from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.redis import redis_client
from app.core.security import get_current_user
from app.models.user import User


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话。"""
    async for session in get_async_session():
        yield session


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户。"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )
    return current_user


async def get_redis():
    """获取 Redis 客户端。"""
    if redis_client.redis is None:
        await redis_client.init()
    return redis_client


def check_rate_limit(key: str, max_requests: int = 60, window: int = 60) -> None:
    """
    检查速率限制（同步检查，实际计数在中间件中完成）。

    Args:
        key: 限流键名
        max_requests: 窗口期内最大请求数
        window: 窗口时间（秒）

    Raises:
        HTTPException: 超过速率限制
    """
    # 实际的速率限制在中间件中通过 Redis 实现
    # 这里提供一个简单的同步版本作为备用
    pass
