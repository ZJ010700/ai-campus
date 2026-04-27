"""
社区相关 Pydantic schemas。
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommunityPostCreate(BaseModel):
    """创建社区帖子 schema。"""
    type: str = Field(
        ...,
        description="帖子类型: second_hand/carpool/lost_found",
    )
    title: str = Field(..., min_length=1, max_length=255, description="标题")
    content: str = Field(..., min_length=1, max_length=5000, description="内容")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    contact_info: Optional[str] = Field(None, max_length=255, description="联系方式")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    price: Optional[str] = Field(None, max_length=50, description="价格（二手交易用）")


class CommunityPostUpdate(BaseModel):
    """更新社区帖子 schema。"""
    title: Optional[str] = Field(None, max_length=255, description="标题")
    content: Optional[str] = Field(None, max_length=5000, description="内容")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    status: Optional[str] = Field(None, description="状态: active/closed/expired")
    contact_info: Optional[str] = Field(None, max_length=255, description="联系方式")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    price: Optional[str] = Field(None, max_length=50, description="价格")


class CommunityPostResponse(BaseModel):
    """社区帖子响应 schema。"""
    id: int
    user_id: int
    type: str
    title: str
    content: str
    images: Optional[str] = None
    status: str
    contact_info: Optional[str] = None
    location: Optional[str] = None
    price: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None

    model_config = {"from_attributes": True}


class CommunityPostList(BaseModel):
    """社区帖子列表响应 schema。"""
    items: list[CommunityPostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
