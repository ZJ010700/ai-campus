"""
反馈服务。

处理用户反馈的创建、查询、统计等业务逻辑。
"""
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate
from app.utils.logger import logger


async def create_feedback(
    db: AsyncSession, user_id: int, feedback_in: FeedbackCreate
) -> dict:
    """
    创建反馈。

    Args:
        db: 数据库会话
        user_id: 用户ID
        feedback_in: 反馈数据

    Returns:
        创建的反馈
    """
    logger.info(f"创建反馈: user={user_id}, rating={feedback_in.rating}")

    feedback = Feedback(
        user_id=user_id,
        conversation_id=feedback_in.conversation_id,
        rating=feedback_in.rating,
        content=feedback_in.content,
    )
    db.add(feedback)
    await db.flush()
    await db.refresh(feedback)

    return feedback


async def get_user_feedbacks(
    db: AsyncSession, user_id: int, page: int, page_size: int
) -> dict:
    """
    获取用户的反馈列表。

    Args:
        db: 数据库会话
        user_id: 用户ID
        page: 页码
        page_size: 每页数量

    Returns:
        反馈列表
    """
    conditions = [Feedback.user_id == user_id]

    count_stmt = select(func.count(Feedback.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    query_stmt = (
        select(Feedback)
        .where(*conditions)
        .order_by(Feedback.created_at.desc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    feedbacks = result.scalars().all()

    return {
        "items": feedbacks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_feedback(
    db: AsyncSession, feedback_id: int
) -> Optional[Feedback]:
    """
    获取反馈详情。

    Args:
        db: 数据库会话
        feedback_id: 反馈ID

    Returns:
        反馈对象或 None
    """
    stmt = select(Feedback).where(Feedback.id == feedback_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_feedbacks(
    db: AsyncSession,
    page: int,
    page_size: int,
    rating: Optional[int] = None,
) -> dict:
    """
    获取所有反馈列表。

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        rating: 评分筛选

    Returns:
        反馈列表
    """
    conditions = []
    if rating:
        conditions.append(Feedback.rating == rating)

    count_stmt = select(func.count(Feedback.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    query_stmt = (
        select(Feedback)
        .where(*conditions)
        .order_by(Feedback.created_at.desc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    feedbacks = result.scalars().all()

    return {
        "items": feedbacks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_feedback_stats(db: AsyncSession) -> dict:
    """
    获取反馈统计数据。

    Args:
        db: 数据库会话

    Returns:
        统计数据
    """
    # 总数和平均分
    stats_stmt = select(
        func.count(Feedback.id).label("total_count"),
        func.avg(Feedback.rating).label("average_rating"),
    )
    stats_result = await db.execute(stats_stmt)
    stats_row = stats_result.one()

    # 评分分布
    distribution_stmt = select(
        Feedback.rating,
        func.count(Feedback.id).label("count"),
    ).group_by(Feedback.rating)
    distribution_result = await db.execute(distribution_stmt)
    distribution_rows = distribution_result.all()

    rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for row in distribution_rows:
        rating_distribution[row.rating] = row.count

    return {
        "total_count": stats_row.total_count or 0,
        "average_rating": round(float(stats_row.average_rating or 0), 2),
        "rating_distribution": rating_distribution,
    }
