"""
日常服务接口。

提供食堂菜单、图书馆服务、报修服务等功能。
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.service import (
    ServiceRequestCreate,
    ServiceRequestResponse,
)
from app.services import daily_service

router = APIRouter()


@router.get(
    "/canteen/menu",
    summary="获取食堂菜单",
    description="获取食堂今日菜单，支持按食堂和时段筛选",
)
async def get_canteen_menu(
    canteen: str = Query(None, description="食堂名称"),
    meal_type: str = Query(None, description="餐次: breakfast/lunch/dinner"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取食堂菜单。"""
    result = await daily_service.get_canteen_menu(canteen, meal_type)
    return result


@router.get(
    "/canteens",
    summary="获取食堂列表",
    description="获取所有食堂信息",
)
async def get_canteens(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取食堂列表。"""
    result = await daily_service.get_canteens()
    return result


@router.get(
    "/library/seats",
    summary="查询图书馆座位",
    description="查询图书馆座位实时状态",
)
async def get_library_seats(
    area: str = Query(None, description="区域筛选"),
    floor: int = Query(None, description="楼层"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """查询图书馆座位。"""
    result = await daily_service.get_library_seats(area, floor)
    return result


@router.get(
    "/library/books",
    summary="搜索图书",
    description="搜索图书馆藏书",
)
async def search_books(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """搜索图书。"""
    result = await daily_service.search_books(keyword, page, page_size)
    return result


@router.get(
    "/library/borrowed",
    summary="查询借阅记录",
    description="查询当前用户的借阅记录",
)
async def get_borrowed_books(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """查询借阅记录。"""
    result = await daily_service.get_borrowed_books()
    return result


@router.post(
    "/repair",
    response_model=ServiceRequestResponse,
    summary="提交报修申请",
    description="提交校园设施报修申请",
)
async def create_repair_request(
    repair_in: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """提交报修申请。"""
    result = await daily_service.create_service_request(
        db, current_user.id, repair_in
    )
    return result


@router.get(
    "/repair/my",
    summary="我的报修记录",
    description="查询当前用户的报修记录",
)
async def get_my_repairs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: str = Query(None, description="状态筛选"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """查询我的报修记录。"""
    result = await daily_service.get_my_service_requests(
        db, current_user.id, "repair", status, page, page_size
    )
    return result


@router.get(
    "/weather",
    summary="获取天气信息",
    description="获取校园天气信息",
)
async def get_weather(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取天气信息。"""
    result = await daily_service.get_weather()
    return result


@router.get(
    "/bus",
    summary="获取校车时刻表",
    description="获取校园班车时刻表",
)
async def get_bus_schedule(
    route: str = Query(None, description="线路筛选"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取校车时刻表。"""
    result = await daily_service.get_bus_schedule(route)
    return result
