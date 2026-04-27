"""
对话管理接口。

提供对话的创建、查询、删除等功能。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationUpdate,
)
from app.services import conversation_service

router = APIRouter()


@router.post(
    "/",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建对话",
    description="创建新的对话",
)
async def create_conversation(
    conv_in: ConversationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Conversation:
    """创建新对话。"""
    conversation = await conversation_service.create_conversation(
        db, current_user.id, conv_in
    )
    return conversation


@router.get(
    "/",
    response_model=dict,
    summary="获取对话列表",
    description="获取当前用户的所有对话，支持分页和模块类型筛选",
)
async def list_conversations(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    module_type: str = Query(None, description="按模块类型筛选"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取当前用户的对话列表。"""
    result = await conversation_service.list_conversations(
        db, current_user.id, page, page_size, module_type
    )
    return result


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="获取对话详情",
    description="根据ID获取对话详细信息",
)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Conversation:
    """获取对话详情。"""
    conversation = await conversation_service.get_conversation(
        db, conversation_id, current_user.id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在",
        )
    return conversation


@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="更新对话",
    description="更新对话标题等信息",
)
async def update_conversation(
    conversation_id: int,
    conv_update: ConversationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Conversation:
    """更新对话信息。"""
    conversation = await conversation_service.update_conversation(
        db, conversation_id, current_user.id, conv_update
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在",
        )
    return conversation


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除对话",
    description="删除指定对话及其所有消息",
)
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """删除对话。"""
    success = await conversation_service.delete_conversation(
        db, conversation_id, current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在",
        )
