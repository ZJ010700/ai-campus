"""
反馈相关 Pydantic schemas。
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    """创建反馈 schema。"""
    conversation_id: Optional[int] = Field(None, description="关联对话ID")
    rating: int = Field(..., ge=1, le=5, description="评分 1-5")
    content: Optional[str] = Field(None, max_length=1000, description="反馈内容")


class FeedbackResponse(BaseModel):
    """反馈响应 schema。"""
    id: int
    user_id: int
    conversation_id: Optional[int] = None
    rating: int
    content: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackStats(BaseModel):
    """反馈统计 schema。"""
    total_count: int = 0
    average_rating: float = 0.0
    rating_distribution: dict[int, int] = Field(
        default_factory=lambda: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    )
