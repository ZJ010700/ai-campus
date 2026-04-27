"""
用户管理接口。

提供用户信息查询、更新、密码修改等功能。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import (
    get_current_active_user,
    get_current_admin_user,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.user import (
    UserBrief,
    UserChangePassword,
    UserResponse,
    UserUpdate,
)
from app.services import user_service

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="获取当前用户信息",
    description="获取当前登录用户的详细信息",
)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """获取当前登录用户的信息。"""
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="更新当前用户信息",
    description="更新当前登录用户的昵称、头像等信息",
)
async def update_current_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    """更新当前用户信息。"""
    user = await user_service.update_user(db, current_user.id, user_update)
    return user


@router.post(
    "/me/change-password",
    summary="修改密码",
    description="修改当前用户的密码",
)
async def change_password(
    password_data: UserChangePassword,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """修改当前用户密码。"""
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误",
        )

    # 更新密码
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.add(current_user)
    await db.flush()
    await db.refresh(current_user)

    return {"message": "密码修改成功"}


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="获取用户信息",
    description="根据用户ID获取用户信息（管理员权限）",
)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> User:
    """根据ID获取用户信息。"""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    return user


@router.get(
    "/",
    response_model=dict,
    summary="获取用户列表",
    description="分页获取用户列表（管理员权限）",
)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    role: str = Query(None, description="按角色筛选"),
    is_active: bool = Query(None, description="按激活状态筛选"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> dict:
    """分页获取用户列表。"""
    result = await user_service.list_users(db, page, page_size, role, is_active)
    return result


@router.put(
    "/{user_id}/activate",
    summary="激活用户",
    description="激活指定用户（管理员权限）",
)
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> dict:
    """激活用户。"""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    user.is_active = True
    db.add(user)
    await db.flush()
    return {"message": "用户已激活"}


@router.put(
    "/{user_id}/deactivate",
    summary="禁用用户",
    description="禁用指定用户（管理员权限）",
)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> dict:
    """禁用用户。"""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    user.is_active = False
    db.add(user)
    await db.flush()
    return {"message": "用户已禁用"}
