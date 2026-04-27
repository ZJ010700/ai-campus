"""
学业助手接口。

提供选课推荐、考试日历、学业规划等功能。
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services import academic_service

router = APIRouter()


@router.get(
    "/courses",
    summary="获取课程列表",
    description="获取可选课程列表，支持搜索和筛选",
)
async def get_courses(
    keyword: str = Query(None, description="搜索关键词"),
    department: str = Query(None, description="院系筛选"),
    semester: str = Query(None, description="学期筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取课程列表。"""
    result = await academic_service.get_courses(
        keyword, department, semester, page, page_size
    )
    return result


@router.get(
    "/courses/recommend",
    summary="选课推荐",
    description="根据学生专业和兴趣推荐课程",
)
async def recommend_courses(
    major: str = Query(None, description="专业"),
    interest: str = Query(None, description="兴趣方向"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取选课推荐。"""
    result = await academic_service.recommend_courses(major, interest)
    return result


@router.get(
    "/schedule",
    summary="获取课程表",
    description="获取当前用户的课程表",
)
async def get_schedule(
    semester: str = Query(None, description="学期"),
    week: int = Query(None, ge=1, le=25, description="周次"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取课程表。"""
    result = await academic_service.get_schedule(semester, week)
    return result


@router.get(
    "/exams",
    summary="获取考试安排",
    description="获取考试日历和安排",
)
async def get_exams(
    semester: str = Query(None, description="学期"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取考试安排。"""
    result = await academic_service.get_exams(semester)
    return result


@router.get(
    "/grades",
    summary="获取成绩查询",
    description="查询学生成绩",
)
async def get_grades(
    semester: str = Query(None, description="学期筛选"),
    course_type: str = Query(None, description="课程类型"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """查询成绩。"""
    result = await academic_service.get_grades(semester, course_type)
    return result


@router.get(
    "/plan",
    summary="学业规划",
    description="获取学业规划建议",
)
async def get_academic_plan(
    major: str = Query(None, description="专业"),
    year: int = Query(None, description="年级"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """获取学业规划建议。"""
    result = await academic_service.get_academic_plan(major, year)
    return result
