"""
校园信息查询接口。

提供校园公告、活动、通知等信息查询功能。
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services import campus_service

router = APIRouter()


@router.get(
    "/announcements",
    summary="获取校园公告",
    description="获取校园公告列表，支持分页和关键词搜索",
)
async def get_announcements(
    keyword: str = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取校园公告列表。"""
    result = await campus_service.get_announcements(keyword, page, page_size)
    return result


@router.get(
    "/activities",
    summary="获取校园活动",
    description="获取校园活动列表",
)
async def get_activities(
    category: str = Query(None, description="活动类别"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取校园活动列表。"""
    result = await campus_service.get_activities(category, page, page_size)
    return result


@router.get(
    "/notices",
    summary="获取通知",
    description="获取校园通知列表",
)
async def get_notices(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取校园通知列表。"""
    result = await campus_service.get_notices(page, page_size)
    return result


@router.get(
    "/search",
    summary="搜索校园信息",
    description="综合搜索校园信息（公告、活动、通知等）",
)
async def search_campus_info(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """搜索校园信息。"""
    result = await campus_service.search_info(keyword, page, page_size)
    return result


@router.get(
    "/calendar",
    summary="获取校园日历",
    description="获取校园重要日期和事件日历",
)
async def get_campus_calendar(
    month: int = Query(None, ge=1, le=12, description="月份"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取校园日历。"""
    result = await campus_service.get_calendar(month)
    return result


@router.post(
    "/subscribe",
    summary="订阅校园信息",
    description="订阅感兴趣的校园信息类别和关键词",
)
async def subscribe_info(
    category: str = Query(..., description="订阅类别"),
    keyword: str = Query(..., description="订阅关键词"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """订阅校园信息。"""
    result = await campus_service.subscribe_info(db, current_user.id, category, keyword)
    return result
