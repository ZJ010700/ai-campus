"""
服务请求相关 Pydantic schemas。
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ServiceRequestCreate(BaseModel):
    """创建服务请求 schema。"""
    type: str = Field(
        ...,
        description="服务类型: repair/library/other",
    )
    title: str = Field(..., min_length=1, max_length=255, description="标题")
    description: str = Field(..., min_length=1, max_length=5000, description="详细描述")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    contact_info: Optional[str] = Field(None, max_length=255, description="联系方式")
    images: Optional[list[str]] = Field(None, description="图片URL列表")


class ServiceRequestUpdate(BaseModel):
    """更新服务请求 schema。"""
    status: Optional[str] = Field(
        None, description="状态: pending/processing/completed/cancelled"
    )
    resolution: Optional[str] = Field(None, max_length=2000, description="处理结果")


class ServiceRequestResponse(BaseModel):
    """服务请求响应 schema。"""
    id: int
    user_id: int
    type: str
    title: str
    description: str
    status: str
    location: Optional[str] = None
    contact_info: Optional[str] = None
    images: Optional[str] = None
    handler_id: Optional[int] = None
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ServiceRequestList(BaseModel):
    """服务请求列表响应 schema。"""
    items: list[ServiceRequestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
