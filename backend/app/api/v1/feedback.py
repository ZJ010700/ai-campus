"""
反馈接口。

提供用户反馈提交、查询、统计等功能。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse,
    FeedbackStats,
)
from app.services import feedback_service

router = APIRouter()


@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="提交反馈",
    description="提交对AI对话的反馈评价",
)
async def create_feedback(
    feedback_in: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """提交反馈。"""
    feedback = await feedback_service.create_feedback(
        db, current_user.id, feedback_in
    )
    return feedback


@router.get(
    "/my",
    summary="我的反馈",
    description="获取当前用户提交的所有反馈",
)
async def get_my_feedbacks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取我的反馈列表。"""
    result = await feedback_service.get_user_feedbacks(
        db, current_user.id, page, page_size
    )
    return result


@router.get(
    "/stats",
    response_model=FeedbackStats,
    summary="反馈统计",
    description="获取反馈统计数据（管理员权限）",
)
async def get_feedback_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> dict:
    """获取反馈统计。"""
    stats = await feedback_service.get_feedback_stats(db)
    return stats


@router.get(
    "/",
    summary="获取反馈列表",
    description="获取所有反馈列表（管理员权限）",
)
async def list_feedbacks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    rating: int = Query(None, ge=1, le=5, description="按评分筛选"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> dict:
    """获取反馈列表。"""
    result = await feedback_service.list_feedbacks(
        db, page, page_size, rating
    )
    return result


@router.get(
    "/{feedback_id}",
    response_model=FeedbackResponse,
    summary="获取反馈详情",
    description="根据ID获取反馈详情",
)
async def get_feedback(
    feedback_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> dict:
    """获取反馈详情。"""
    feedback = await feedback_service.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在",
        )
    return feedback
