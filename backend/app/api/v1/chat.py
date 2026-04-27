"""
AI 对话接口（核心）。

提供发送消息、获取AI回复、对话历史等功能。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.message import (
    ChatHistoryResponse,
    ChatRequest,
    ChatResponse,
    MessageResponse,
)
from app.services import chat_service, conversation_service

router = APIRouter()


@router.post(
    "/",
    response_model=ChatResponse,
    summary="发送消息并获取AI回复",
    description="向AI助手发送消息，获取智能回复",
)
async def chat(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatResponse:
    """
    发送消息并获取AI回复。

    - 如果未提供 conversation_id，则自动创建新对话
    - 消息会保存到数据库
    - AI 回复通过 LangChain + 通义千问生成
    """
    result = await chat_service.send_message(
        db=db,
        user_id=current_user.id,
        conversation_id=chat_request.conversation_id,
        message=chat_request.message,
        module_type=chat_request.module_type,
    )
    return result


@router.get(
    "/history/{conversation_id}",
    response_model=ChatHistoryResponse,
    summary="获取对话历史",
    description="获取指定对话的所有消息记录",
)
async def get_chat_history(
    conversation_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatHistoryResponse:
    """获取对话历史消息。"""
    # 验证对话归属
    conversation = await conversation_service.get_conversation(
        db, conversation_id, current_user.id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在",
        )

    history = await chat_service.get_chat_history(
        db, conversation_id, page, page_size
    )
    return history


@router.post(
    "/conversations",
    summary="创建新对话",
    description="创建新的AI对话会话",
)
async def create_chat_conversation(
    module_type: str = Query("campus", description="模块类型"),
    title: str = Query("新对话", description="对话标题"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """创建新的AI对话。"""
    from app.schemas.conversation import ConversationCreate

    conv_in = ConversationCreate(title=title, module_type=module_type)
    conversation = await conversation_service.create_conversation(
        db, current_user.id, conv_in
    )
    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
        "module_type": conversation.module_type,
        "created_at": str(conversation.created_at),
    }


@router.delete(
    "/history/{conversation_id}",
    summary="清空对话历史",
    description="清空指定对话的所有消息（保留对话本身）",
)
async def clear_chat_history(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """清空对话历史消息。"""
    # 验证对话归属
    conversation = await conversation_service.get_conversation(
        db, conversation_id, current_user.id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在",
        )

    deleted_count = await chat_service.clear_chat_history(db, conversation_id)
    return {
        "message": "对话历史已清空",
        "deleted_count": deleted_count,
    }
