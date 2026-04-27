"""
心理健康接口。

提供情绪倾听、压力管理、心理健康评估等功能。
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.message import ChatRequest, ChatResponse
from app.services import mental_health_service

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="心理伙伴对话",
    description="与心理健康AI伙伴进行对话",
)
async def mental_health_chat(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatResponse:
    """与心理伙伴AI进行对话。"""
    chat_request.module_type = "mental_health"
    from app.services import chat_service

    result = await chat_service.send_message(
        db=db,
        user_id=current_user.id,
        conversation_id=chat_request.conversation_id,
        message=chat_request.message,
        module_type="mental_health",
    )
    return result


@router.get(
    "/assessment",
    summary="心理健康评估",
    description="获取心理健康评估问卷",
)
async def get_assessment(
    assessment_type: str = Query("general", description="评估类型: general/stress/anxiety/depression"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取心理健康评估问卷。"""
    result = await mental_health_service.get_assessment(assessment_type)
    return result


@router.post(
    "/assessment/submit",
    summary="提交评估结果",
    description="提交心理健康评估结果",
)
async def submit_assessment(
    assessment_type: str = Query("general", description="评估类型"),
    answers: dict = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """提交评估结果。"""
    if answers is None:
        answers = {}
    result = await mental_health_service.submit_assessment(
        db, current_user.id, assessment_type, answers
    )
    return result


@router.get(
    "/resources",
    summary="获取心理资源",
    description="获取心理健康相关资源（文章、热线等）",
)
async def get_resources(
    category: str = Query(None, description="资源类别"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取心理健康资源。"""
    result = await mental_health_service.get_resources(category)
    return result


@router.get(
    "/tips",
    summary="获取心理小贴士",
    description="获取每日心理小贴士",
)
async def get_daily_tips(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取每日心理小贴士。"""
    result = await mental_health_service.get_daily_tips()
    return result


@router.get(
    "/history",
    summary="获取咨询历史",
    description="获取心理健康咨询历史记录",
)
async def get_consultation_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取咨询历史。"""
    result = await mental_health_service.get_history(
        db, current_user.id, page, page_size
    )
    return result
