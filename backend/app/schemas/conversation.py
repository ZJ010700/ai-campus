"""
对话相关 Pydantic schemas。
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    """创建对话 schema。"""
    title: str = Field("新对话", max_length=255, description="对话标题")
    module_type: str = Field(
        "campus",
        description="模块类型: academic/campus/daily/community/mental_health",
    )


class ConversationUpdate(BaseModel):
    """更新对话 schema。"""
    title: Optional[str] = Field(None, max_length=255, description="对话标题")


class ConversationResponse(BaseModel):
    """对话响应 schema。"""
    id: int
    user_id: int
    title: str
    module_type: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationListResponse(BaseModel):
    """对话列表响应 schema。"""
    id: int
    title: str
    module_type: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}
