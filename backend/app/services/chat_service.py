"""
AI 对话服务。

处理消息发送、AI 回复生成、对话历史管理等核心业务逻辑。
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.engine import AIEngine
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate
from app.schemas.message import ChatHistoryResponse, ChatResponse, MessageResponse
from app.services import conversation_service
from app.utils.helpers import calculate_tokens_estimate


async def send_message(
    db: AsyncSession,
    user_id: int,
    conversation_id: Optional[int],
    message: str,
    module_type: str = "campus",
) -> ChatResponse:
    """
    发送消息并获取AI回复。

    Args:
        db: 数据库会话
        user_id: 用户ID
        conversation_id: 对话ID（为空则创建新对话）
        message: 用户消息
        module_type: 模块类型

    Returns:
        AI 回复响应
    """
    # 如果没有对话ID，创建新对话
    if conversation_id is None:
        # 根据消息内容生成标题（取前20个字符）
        title = message[:20] + ("..." if len(message) > 20 else "")
        conv_in = ConversationCreate(title=title, module_type=module_type)
        conversation = await conversation_service.create_conversation(
            db, user_id, conv_in
        )
        conversation_id = conversation.id
    else:
        # 验证对话归属
        conversation = await conversation_service.get_conversation(
            db, conversation_id, user_id
        )
        if not conversation:
            raise ValueError("对话不存在")
        module_type = conversation.module_type

    # 保存用户消息
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message,
        tokens_used=calculate_tokens_estimate(message),
    )
    db.add(user_message)
    await db.flush()

    # 获取对话历史（最近10条消息作为上下文）
    history_stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(10)
    )
    history_result = await db.execute(history_stmt)
    history_messages = list(reversed(history_result.scalars().all()))

    # 构建对话上下文
    chat_history = []
    for msg in history_messages:
        chat_history.append({
            "role": msg.role,
            "content": msg.content,
        })

    # 调用AI引擎生成回复
    ai_engine = AIEngine()
    ai_response = await ai_engine.chat(
        message=message,
        module_type=module_type,
        chat_history=chat_history,
    )

    # 估算token使用量
    tokens_used = calculate_tokens_estimate(ai_response)

    # 保存AI回复
    assistant_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response,
        tokens_used=tokens_used,
    )
    db.add(assistant_message)
    await db.flush()
    await db.refresh(assistant_message)

    # 更新对话的更新时间
    conversation.updated_at = datetime.now(timezone.utc)
    db.add(conversation)
    await db.flush()

    return ChatResponse(
        conversation_id=conversation_id,
        message_id=assistant_message.id,
        content=ai_response,
        role="assistant",
        tokens_used=tokens_used,
        created_at=assistant_message.created_at,
    )


async def get_chat_history(
    db: AsyncSession,
    conversation_id: int,
    page: int = 1,
    page_size: int = 50,
) -> ChatHistoryResponse:
    """
    获取对话历史消息。

    Args:
        db: 数据库会话
        conversation_id: 对话ID
        page: 页码
        page_size: 每页数量

    Returns:
        对话历史响应
    """
    # 查询总数
    count_stmt = select(func.count(Message.id)).where(
        Message.conversation_id == conversation_id
    )
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 查询消息
    query_stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    messages = result.scalars().all()

    # 获取对话信息
    conv_stmt = select(Conversation).where(Conversation.id == conversation_id)
    conv_result = await db.execute(conv_stmt)
    conversation = conv_result.scalar_one_or_none()

    return ChatHistoryResponse(
        conversation_id=conversation_id,
        title=conversation.title if conversation else "",
        module_type=conversation.module_type if conversation else "",
        messages=[MessageResponse.model_validate(msg) for msg in messages],
        total=total,
    )


async def clear_chat_history(
    db: AsyncSession, conversation_id: int
) -> int:
    """
    清空对话历史消息。

    Args:
        db: 数据库会话
        conversation_id: 对话ID

    Returns:
        删除的消息数量
    """
    # 查询当前消息数量
    count_stmt = select(func.count(Message.id)).where(
        Message.conversation_id == conversation_id
    )
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 删除所有消息
    delete_stmt = delete(Message).where(
        Message.conversation_id == conversation_id
    )
    await db.execute(delete_stmt)
    await db.flush()

    return total
