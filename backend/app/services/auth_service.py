"""
认证服务。

处理用户注册、登录等认证相关业务逻辑。
"""
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import (
    get_current_user,
    get_password_hash,
)
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    创建新用户。

    Args:
        db: 数据库会话
        user_in: 用户注册数据

    Returns:
        创建的用户对象
    """
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        nickname=user_in.nickname or user_in.username,
        role="student",
        is_active=True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    根据ID获取用户。

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        用户对象或 None
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    根据用户名获取用户。

    Args:
        db: 数据库会话
        username: 用户名

    Returns:
        用户对象或 None
    """
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    根据邮箱获取用户。

    Args:
        db: 数据库会话
        email: 邮箱

    Returns:
        用户对象或 None
    """
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 供 API 层 Depends 使用的快捷方法
get_current_user_dep = Depends(get_current_user)
