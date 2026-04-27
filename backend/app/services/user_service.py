"""
用户服务。

处理用户信息管理相关业务逻辑。
"""
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdate


async def update_user(
    db: AsyncSession, user_id: int, user_update: UserUpdate
) -> Optional[User]:
    """
    更新用户信息。

    Args:
        db: 数据库会话
        user_id: 用户ID
        user_update: 更新数据

    Returns:
        更新后的用户对象或 None
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

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


async def list_users(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> dict:
    """
    获取用户列表（分页）。

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        role: 角色筛选
        is_active: 激活状态筛选

    Returns:
        分页结果字典
    """
    # 构建查询条件
    conditions = []
    if role:
        conditions.append(User.role == role)
    if is_active is not None:
        conditions.append(User.is_active == is_active)

    # 查询总数
    count_stmt = select(func.count(User.id))
    for cond in conditions:
        count_stmt = count_stmt.where(cond)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 查询数据
    query_stmt = select(User).order_by(User.created_at.desc())
    for cond in conditions:
        query_stmt = query_stmt.where(cond)
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    users = result.scalars().all()

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": users,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
