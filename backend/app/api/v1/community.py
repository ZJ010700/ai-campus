"""
社区接口。

提供二手交易、拼车、失物招领等功能。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.community import (
    CommunityPostCreate,
    CommunityPostResponse,
    CommunityPostUpdate,
)
from app.services import community_service

router = APIRouter()


@router.post(
    "/posts",
    response_model=CommunityPostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="发布帖子",
    description="发布二手交易、拼车或失物招领帖子",
)
async def create_post(
    post_in: CommunityPostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """发布社区帖子。"""
    post = await community_service.create_post(db, current_user.id, post_in)
    return post


@router.get(
    "/posts",
    summary="获取帖子列表",
    description="获取社区帖子列表，支持类型筛选和分页",
)
async def list_posts(
    post_type: str = Query(None, description="帖子类型: second_hand/carpool/lost_found"),
    keyword: str = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取帖子列表。"""
    result = await community_service.list_posts(
        db, post_type, keyword, page, page_size
    )
    return result


@router.get(
    "/posts/{post_id}",
    response_model=CommunityPostResponse,
    summary="获取帖子详情",
    description="根据ID获取帖子详细信息",
)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取帖子详情。"""
    post = await community_service.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在",
        )
    return post


@router.put(
    "/posts/{post_id}",
    response_model=CommunityPostResponse,
    summary="更新帖子",
    description="更新自己发布的帖子",
)
async def update_post(
    post_id: int,
    post_update: CommunityPostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """更新帖子。"""
    post = await community_service.update_post(
        db, post_id, current_user.id, post_update
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权修改",
        )
    return post


@router.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除帖子",
    description="删除自己发布的帖子",
)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """删除帖子。"""
    success = await community_service.delete_post(db, post_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权删除",
        )


@router.get(
    "/my-posts",
    summary="我的帖子",
    description="获取当前用户发布的所有帖子",
)
async def get_my_posts(
    post_type: str = Query(None, description="帖子类型筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取我的帖子。"""
    result = await community_service.get_my_posts(
        db, current_user.id, post_type, page, page_size
    )
    return result


@router.post(
    "/posts/{post_id}/close",
    summary="关闭帖子",
    description="关闭自己发布的帖子（标记为已完成）",
)
async def close_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """关闭帖子。"""
    post = await community_service.close_post(db, post_id, current_user.id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权操作",
        )
    return {"message": "帖子已关闭"}
