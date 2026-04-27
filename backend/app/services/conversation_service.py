"""
对话服务。

处理对话的创建、查询、更新、删除等业务逻辑。
"""
from typing import Optional

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationUpdate


async def create_conversation(
    db: AsyncSession, user_id: int, conv_in: ConversationCreate
) -> Conversation:
    """
    创建新对话。

    Args:
        db: 数据库会话
        user_id: 用户ID
        conv_in: 对话创建数据

    Returns:
        创建的对话对象
    """
    conversation = Conversation(
        user_id=user_id,
        title=conv_in.title,
        module_type=conv_in.module_type,
    )
    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    return conversation


async def get_conversation(
    db: AsyncSession, conversation_id: int, user_id: int
) -> Optional[Conversation]:
    """
    获取对话详情（验证归属）。

    Args:
        db: 数据库会话
        conversation_id: 对话ID
        user_id: 用户ID

    Returns:
        对话对象或 None
    """
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_conversations(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    page_size: int = 20,
    module_type: Optional[str] = None,
) -> dict:
    """
    获取用户的对话列表。

    Args:
        db: 数据库会话
        user_id: 用户ID
        page: 页码
        page_size: 每页数量
        module_type: 模块类型筛选

    Returns:
        分页结果字典
    """
    # 构建查询条件
    conditions = [Conversation.user_id == user_id]
    if module_type:
        conditions.append(Conversation.module_type == module_type)

    # 查询总数
    count_stmt = select(func.count(Conversation.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 查询对话列表，附带消息数量
    query_stmt = (
        select(
            Conversation,
            func.count(Message.id).label("message_count"),
        )
        .outerjoin(Message, Conversation.id == Message.conversation_id)
        .where(*conditions)
        .group_by(Conversation.id)
        .order_by(Conversation.updated_at.desc())
    )

    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    rows = result.all()

    items = []
    for row in rows:
        conv = row[0]
        msg_count = row[1]
        items.append({
            "id": conv.id,
            "title": conv.title,
            "module_type": conv.module_type,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": msg_count,
        })

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


async def update_conversation(
    db: AsyncSession,
    conversation_id: int,
    user_id: int,
    conv_update: ConversationUpdate,
) -> Optional[Conversation]:
    """
    更新对话信息。

    Args:
        db: 数据库会话
        conversation_id: 对话ID
        user_id: 用户ID
        conv_update: 更新数据

    Returns:
        更新后的对话对象或 None
    """
    conversation = await get_conversation(db, conversation_id, user_id)
    if not conversation:
        return None

    update_data = conv_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conversation, field, value)

    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    return conversation


async def delete_conversation(
    db: AsyncSession, conversation_id: int, user_id: int
) -> bool:
    """
    删除对话及其所有消息。

    Args:
        db: 数据库会话
        conversation_id: 对话ID
        user_id: 用户ID

    Returns:
        是否删除成功
    """
    conversation = await get_conversation(db, conversation_id, user_id)
    if not conversation:
        return False

    # 删除关联的消息
    delete_msg_stmt = delete(Message).where(
        Message.conversation_id == conversation_id
    )
    await db.execute(delete_msg_stmt)

    # 删除对话
    delete_conv_stmt = delete(Conversation).where(
        Conversation.id == conversation_id
    )
    await db.execute(delete_conv_stmt)
    await db.flush()
    return True
