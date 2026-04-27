"""
学业服务。

处理选课推荐、课程表、考试安排、成绩查询、学业规划等业务逻辑。
"""
from typing import Optional

from app.utils.logger import logger


async def get_courses(
    keyword: Optional[str],
    department: Optional[str],
    semester: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    """
    获取课程列表。

    Args:
        keyword: 搜索关键词
        department: 院系筛选
        semester: 学期筛选
        page: 页码
        page_size: 每页数量

    Returns:
        课程列表
    """
    logger.info(f"获取课程列表: keyword={keyword}, dept={department}")

    courses = [
        {
            "id": "CS101",
            "name": "计算机导论",
            "department": "计算机学院",
            "teacher": "张教授",
            "credits": 3,
            "time": "周一 3-4节",
            "location": "教学楼A301",
            "capacity": 150,
            "enrolled": 120,
            "semester": "2025-2026-2",
            "description": "介绍计算机科学的基本概念、原理和方法。",
        },
        {
            "id": "CS201",
            "name": "数据结构与算法",
            "department": "计算机学院",
            "teacher": "李教授",
            "credits": 4,
            "time": "周二 1-2节, 周四 3-4节",
            "location": "教学楼B205",
            "capacity": 120,
            "enrolled": 115,
            "semester": "2025-2026-2",
            "description": "学习常用数据结构和算法设计与分析方法。",
        },
        {
            "id": "MA101",
            "name": "高等数学",
            "department": "数学学院",
            "teacher": "王教授",
            "credits": 5,
            "time": "周一 1-2节, 周三 1-2节, 周五 1-2节",
            "location": "教学楼C101",
            "capacity": 200,
            "enrolled": 180,
            "semester": "2025-2026-2",
            "description": "微积分、级数、常微分方程等高等数学基础。",
        },
        {
            "id": "EN201",
            "name": "大学英语（四）",
            "department": "外语学院",
            "teacher": "陈老师",
            "credits": 2,
            "time": "周三 5-6节",
            "location": "外语楼302",
            "capacity": 50,
            "enrolled": 45,
            "semester": "2025-2026-2",
            "description": "提高英语听说读写综合能力。",
        },
        {
            "id": "PH101",
            "name": "大学物理",
            "department": "物理学院",
            "teacher": "刘教授",
            "credits": 4,
            "time": "周二 3-4节, 周四 1-2节",
            "location": "理学楼201",
            "capacity": 180,
            "enrolled": 160,
            "semester": "2025-2026-2",
            "description": "力学、热学、电磁学、光学等大学物理基础。",
        },
    ]

    # 筛选
    if keyword:
        courses = [
            c for c in courses
            if keyword in c["name"] or keyword in c["id"] or keyword in c["teacher"]
        ]
    if department:
        courses = [c for c in courses if department in c["department"]]
    if semester:
        courses = [c for c in courses if c["semester"] == semester]

    total = len(courses)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": courses[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def recommend_courses(
    major: Optional[str], interest: Optional[str]
) -> dict:
    """
    获取选课推荐。

    Args:
        major: 专业
        interest: 兴趣方向

    Returns:
        推荐课程列表
    """
    logger.info(f"获取选课推荐: major={major}, interest={interest}")

    recommendations = [
        {
            "course_id": "CS301",
            "course_name": "人工智能导论",
            "reason": "根据您对AI的兴趣推荐，该课程是AI方向的基础课程",
            "match_score": 95,
            "credits": 3,
            "difficulty": "中等",
        },
        {
            "course_id": "CS302",
            "course_name": "机器学习",
            "reason": "热门课程，与当前技术趋势高度相关",
            "match_score": 90,
            "credits": 3,
            "difficulty": "较难",
        },
        {
            "course_id": "CS205",
            "course_name": "Python程序设计",
            "reason": "编程基础课程，适合各专业学生学习",
            "match_score": 85,
            "credits": 2,
            "difficulty": "简单",
        },
    ]

    return {
        "recommendations": recommendations,
        "major": major,
        "interest": interest,
    }


async def get_schedule(semester: Optional[str], week: Optional[int]) -> dict:
    """
    获取课程表。

    Args:
        semester: 学期
        week: 周次

    Returns:
        课程表
    """
    logger.info(f"获取课程表: semester={semester}, week={week}")

    schedule = {
        "semester": semester or "2025-2026-2",
        "week": week or 1,
        "lessons": [
            {
                "day": 1,
                "period": "1-2节",
                "time": "08:00-09:40",
                "course_name": "高等数学",
                "location": "教学楼C101",
                "teacher": "王教授",
            },
            {
                "day": 1,
                "period": "3-4节",
                "time": "10:00-11:40",
                "course_name": "计算机导论",
                "location": "教学楼A301",
                "teacher": "张教授",
            },
            {
                "day": 2,
                "period": "1-2节",
                "time": "08:00-09:40",
                "course_name": "数据结构与算法",
                "location": "教学楼B205",
                "teacher": "李教授",
            },
            {
                "day": 2,
                "period": "3-4节",
                "time": "10:00-11:40",
                "course_name": "大学物理",
                "location": "理学楼201",
                "teacher": "刘教授",
            },
            {
                "day": 3,
                "period": "1-2节",
                "time": "08:00-09:40",
                "course_name": "高等数学",
                "location": "教学楼C101",
                "teacher": "王教授",
            },
            {
                "day": 3,
                "period": "5-6节",
                "time": "14:00-15:40",
                "course_name": "大学英语（四）",
                "location": "外语楼302",
                "teacher": "陈老师",
            },
            {
                "day": 4,
                "period": "1-2节",
                "time": "08:00-09:40",
                "course_name": "大学物理",
                "location": "理学楼201",
                "teacher": "刘教授",
            },
            {
                "day": 4,
                "period": "3-4节",
                "time": "10:00-11:40",
                "course_name": "数据结构与算法",
                "location": "教学楼B205",
                "teacher": "李教授",
            },
            {
                "day": 5,
                "period": "1-2节",
                "time": "08:00-09:40",
                "course_name": "高等数学",
                "location": "教学楼C101",
                "teacher": "王教授",
            },
        ],
    }

    return schedule


async def get_exams(semester: Optional[str]) -> dict:
    """
    获取考试安排。

    Args:
        semester: 学期

    Returns:
        考试安排列表
    """
    logger.info(f"获取考试安排: semester={semester}")

    exams = [
        {
            "course_name": "高等数学",
            "exam_date": "2026-04-20",
            "time": "09:00-11:00",
            "location": "教学楼C101",
            "seat": "A-15",
            "type": "闭卷",
        },
        {
            "course_name": "数据结构与算法",
            "exam_date": "2026-04-22",
            "time": "14:00-16:00",
            "location": "教学楼B205",
            "seat": "B-08",
            "type": "闭卷",
        },
        {
            "course_name": "大学物理",
            "exam_date": "2026-04-25",
            "time": "09:00-11:00",
            "location": "理学楼201",
            "seat": "C-22",
            "type": "闭卷",
        },
        {
            "course_name": "大学英语（四）",
            "exam_date": "2026-04-28",
            "time": "14:00-16:00",
            "location": "外语楼302",
            "seat": "D-11",
            "type": "笔试+听力",
        },
    ]

    return {
        "semester": semester or "2025-2026-2",
        "exams": exams,
    }


async def get_grades(
    semester: Optional[str], course_type: Optional[str]
) -> dict:
    """
    查询成绩。

    Args:
        semester: 学期筛选
        course_type: 课程类型筛选

    Returns:
        成绩列表
    """
    logger.info(f"查询成绩: semester={semester}, type={course_type}")

    grades = [
        {
            "course_id": "CS101",
            "course_name": "计算机导论",
            "credits": 3,
            "score": 92,
            "grade_point": 4.0,
            "level": "A",
            "semester": "2025-2026-1",
            "type": "必修",
        },
        {
            "course_id": "MA101",
            "course_name": "高等数学（上）",
            "credits": 5,
            "score": 85,
            "grade_point": 3.5,
            "level": "B+",
            "semester": "2025-2026-1",
            "type": "必修",
        },
        {
            "course_id": "EN101",
            "course_name": "大学英语（三）",
            "credits": 2,
            "score": 88,
            "grade_point": 3.7,
            "level": "A-",
            "semester": "2025-2026-1",
            "type": "必修",
        },
        {
            "course_id": "PE101",
            "course_name": "体育（一）",
            "credits": 1,
            "score": 90,
            "grade_point": 3.9,
            "level": "A-",
            "semester": "2025-2026-1",
            "type": "必修",
        },
    ]

    if semester:
        grades = [g for g in grades if g["semester"] == semester]
    if course_type:
        grades = [g for g in grades if g["type"] == course_type]

    total_credits = sum(g["credits"] for g in grades)
    weighted_sum = sum(g["score"] * g["credits"] for g in grades)
    gpa = weighted_sum / total_credits if total_credits > 0 else 0

    return {
        "grades": grades,
        "total_credits": total_credits,
        "gpa": round(gpa, 2),
        "semester": semester,
    }


async def get_academic_plan(
    major: Optional[str], year: Optional[int]
) -> dict:
    """
    获取学业规划建议。

    Args:
        major: 专业
        year: 年级

    Returns:
        学业规划建议
    """
    logger.info(f"获取学业规划: major={major}, year={year}")

    plan = {
        "major": major or "计算机科学与技术",
        "year": year or 1,
        "recommendations": [
            {
                "phase": "大一",
                "focus": "打好基础",
                "courses": ["高等数学", "程序设计基础", "大学英语", "线性代数"],
                "activities": ["加入1-2个社团", "参加编程竞赛入门"],
                "certifications": ["英语四级"],
            },
            {
                "phase": "大二",
                "focus": "专业核心",
                "courses": ["数据结构", "操作系统", "计算机网络", "数据库原理"],
                "activities": ["参加科研项目", "参加ACM/数学建模竞赛"],
                "certifications": ["英语六级", "计算机二级"],
            },
            {
                "phase": "大三",
                "focus": "方向深入",
                "courses": ["人工智能", "机器学习", "软件工程", "编译原理"],
                "activities": ["实习", "发表论文", "参加创新创业项目"],
                "certifications": ["相关技术认证"],
            },
            {
                "phase": "大四",
                "focus": "毕业规划",
                "courses": ["毕业设计"],
                "activities": ["秋招/考研/出国准备", "毕业实习"],
                "certifications": [],
            },
        ],
    }

    return plan
