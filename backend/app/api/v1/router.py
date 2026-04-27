"""
API v1 总路由。

聚合所有子路由模块。
"""
from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.chat import router as chat_router
from app.api.v1.campus_info import router as campus_info_router
from app.api.v1.academic import router as academic_router
from app.api.v1.daily_service import router as daily_service_router
from app.api.v1.community import router as community_router
from app.api.v1.mental_health import router as mental_health_router
from app.api.v1.feedback import router as feedback_router

api_router = APIRouter()

# 认证路由（无需登录）
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])

# 用户管理路由
api_router.include_router(users_router, prefix="/users", tags=["用户管理"])

# 对话管理路由
api_router.include_router(conversations_router, prefix="/conversations", tags=["对话管理"])

# AI 对话路由（核心）
api_router.include_router(chat_router, prefix="/chat", tags=["AI 对话"])

# 校园信息路由
api_router.include_router(campus_info_router, prefix="/campus", tags=["校园信息"])

# 学业助手路由
api_router.include_router(academic_router, prefix="/academic", tags=["学业助手"])

# 日常服务路由
api_router.include_router(daily_service_router, prefix="/daily", tags=["日常服务"])

# 社区路由
api_router.include_router(community_router, prefix="/community", tags=["社区"])

# 心理健康路由
api_router.include_router(mental_health_router, prefix="/mental-health", tags=["心理健康"])

# 反馈路由
api_router.include_router(feedback_router, prefix="/feedback", tags=["反馈"])
