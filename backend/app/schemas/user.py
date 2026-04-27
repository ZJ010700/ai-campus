"""
用户相关 Pydantic schemas。
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """用户基础 schema。"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    nickname: Optional[str] = Field(None, max_length=100, description="昵称")


class UserCreate(UserBase):
    """用户注册 schema。"""
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class UserUpdate(BaseModel):
    """用户更新 schema。"""
    nickname: Optional[str] = Field(None, max_length=100, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="头像URL")
    email: Optional[EmailStr] = Field(None, description="邮箱")


class UserChangePassword(BaseModel):
    """修改密码 schema。"""
    old_password: str = Field(..., min_length=6, description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=128, description="新密码")


class UserResponse(BaseModel):
    """用户响应 schema。"""
    id: int
    username: str
    email: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserBrief(BaseModel):
    """用户简要信息 schema。"""
    id: int
    username: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str

    model_config = {"from_attributes": True}
