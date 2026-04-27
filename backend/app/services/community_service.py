"""
社区服务。

处理二手交易、拼车、失物招领等社区功能的业务逻辑。
"""
import json
from typing import Optional

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community import CommunityPost
from app.schemas.community import CommunityPostCreate, CommunityPostUpdate
from app.utils.logger import logger


async def create_post(
    db: AsyncSession, user_id: int, post_in: CommunityPostCreate
) -> dict:
    """
    创建社区帖子。

    Args:
        db: 数据库会话
        user_id: 用户ID
        post_in: 帖子创建数据

    Returns:
        创建的帖子
    """
    logger.info(f"创建社区帖子: user={user_id}, type={post_in.type}")

    post = CommunityPost(
        user_id=user_id,
        type=post_in.type,
        title=post_in.title,
        content=post_in.content,
        images=json.dumps(post_in.images) if post_in.images else None,
        contact_info=post_in.contact_info,
        location=post_in.location,
        price=post_in.price,
        status="active",
    )
    db.add(post)
    await db.flush()
    await db.refresh(post)

    return post


async def list_posts(
    db: AsyncSession,
    post_type: Optional[str],
    keyword: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    """
    获取帖子列表。

    Args:
        db: 数据库会话
        post_type: 帖子类型筛选
        keyword: 搜索关键词
        page: 页码
        page_size: 每页数量

    Returns:
        帖子列表
    """
    conditions = [CommunityPost.status == "active"]
    if post_type:
        conditions.append(CommunityPost.type == post_type)
    if keyword:
        conditions.append(
            (CommunityPost.title.contains(keyword))
            | (CommunityPost.content.contains(keyword))
        )

    # 查询总数
    count_stmt = select(func.count(CommunityPost.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 查询数据（关联用户信息）
    query_stmt = (
        select(CommunityPost)
        .where(*conditions)
        .order_by(CommunityPost.created_at.desc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    posts = result.scalars().all()

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_post(db: AsyncSession, post_id: int) -> Optional[dict]:
    """
    获取帖子详情。

    Args:
        db: 数据库会话
        post_id: 帖子ID

    Returns:
        帖子详情或 None
    """
    stmt = select(CommunityPost).where(CommunityPost.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    return post


async def update_post(
    db: AsyncSession,
    post_id: int,
    user_id: int,
    post_update: CommunityPostUpdate,
) -> Optional[dict]:
    """
    更新帖子。

    Args:
        db: 数据库会话
        post_id: 帖子ID
        user_id: 用户ID
        post_update: 更新数据

    Returns:
        更新后的帖子或 None
    """
    stmt = select(CommunityPost).where(
        CommunityPost.id == post_id,
        CommunityPost.user_id == user_id,
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        return None

    update_data = post_update.model_dump(exclude_unset=True)
    if "images" in update_data and update_data["images"] is not None:
        update_data["images"] = json.dumps(update_data["images"])

    for field, value in update_data.items():
        setattr(post, field, value)

    db.add(post)
    await db.flush()
    await db.refresh(post)
    return post


async def delete_post(
    db: AsyncSession, post_id: int, user_id: int
) -> bool:
    """
    删除帖子。

    Args:
        db: 数据库会话
        post_id: 帖子ID
        user_id: 用户ID

    Returns:
        是否删除成功
    """
    stmt = select(CommunityPost).where(
        CommunityPost.id == post_id,
        CommunityPost.user_id == user_id,
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        return False

    delete_stmt = delete(CommunityPost).where(CommunityPost.id == post_id)
    await db.execute(delete_stmt)
    await db.flush()
    return True


async def get_my_posts(
    db: AsyncSession,
    user_id: int,
    post_type: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    """
    获取用户的帖子列表。

    Args:
        db: 数据库会话
        user_id: 用户ID
        post_type: 帖子类型筛选
        page: 页码
        page_size: 每页数量

    Returns:
        帖子列表
    """
    conditions = [CommunityPost.user_id == user_id]
    if post_type:
        conditions.append(CommunityPost.type == post_type)

    count_stmt = select(func.count(CommunityPost.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    query_stmt = (
        select(CommunityPost)
        .where(*conditions)
        .order_by(CommunityPost.created_at.desc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    posts = result.scalars().all()

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def close_post(
    db: AsyncSession, post_id: int, user_id: int
) -> Optional[dict]:
    """
    关闭帖子。

    Args:
        db: 数据库会话
        post_id: 帖子ID
        user_id: 用户ID

    Returns:
        更新后的帖子或 None
    """
    stmt = select(CommunityPost).where(
        CommunityPost.id == post_id,
        CommunityPost.user_id == user_id,
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        return None

    post.status = "closed"
    db.add(post)
    await db.flush()
    await db.refresh(post)
    return post
