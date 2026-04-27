"""
认证相关 Pydantic schemas。
"""
from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求 schema。"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., min_length=6, description="密码")


class TokenResponse(BaseModel):
    """Token 响应 schema。"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间（秒）")


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求 schema。"""
    refresh_token: str = Field(..., description="刷新令牌")


class TokenPayload(BaseModel):
    """Token 载荷 schema。"""
    sub: str
    type: str
    exp: Optional[int] = None
