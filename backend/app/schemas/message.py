"""
消息相关 Pydantic schemas。
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """消息基础 schema。"""
    role: str = Field(..., description="角色: user/assistant/system")
    content: str = Field(..., min_length=1, description="消息内容")


class MessageCreate(MessageBase):
    """创建消息 schema。"""
    conversation_id: int = Field(..., description="对话ID")


class MessageResponse(BaseModel):
    """消息响应 schema。"""
    id: int
    conversation_id: int
    role: str
    content: str
    tokens_used: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    """聊天请求 schema。"""
    conversation_id: Optional[int] = Field(None, description="对话ID，为空则创建新对话")
    message: str = Field(..., min_length=1, max_length=5000, description="用户消息")
    module_type: str = Field(
        "campus",
        description="模块类型: academic/campus/daily/community/mental_health",
    )


class ChatResponse(BaseModel):
    """聊天响应 schema。"""
    conversation_id: int
    message_id: int
    content: str
    role: str = "assistant"
    tokens_used: Optional[int] = None
    created_at: Optional[datetime] = None


class ChatHistoryResponse(BaseModel):
    """聊天历史响应 schema。"""
    conversation_id: int
    title: str
    module_type: str
    messages: list[MessageResponse]
    total: int
