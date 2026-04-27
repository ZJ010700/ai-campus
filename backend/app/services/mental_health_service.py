"""
心理健康服务。

处理心理健康评估、资源推荐、咨询历史等业务逻辑。
"""
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.utils.logger import logger


async def get_assessment(assessment_type: str) -> dict:
    """
    获取心理健康评估问卷。

    Args:
        assessment_type: 评估类型

    Returns:
        评估问卷
    """
    logger.info(f"获取心理健康评估: type={assessment_type}")

    if assessment_type == "stress":
        questions = [
            {
                "id": 1,
                "question": "在过去两周内，你是否经常感到紧张或焦虑？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 2,
                "question": "你是否难以停止或控制担忧？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 3,
                "question": "你是否对各种各样的事情都过度担忧？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 4,
                "question": "你是否很难放松下来？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 5,
                "question": "你是否因为太不安而无法静坐？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
        ]
    elif assessment_type == "anxiety":
        questions = [
            {
                "id": 1,
                "question": "你是否容易感到烦躁或对小事发脾气？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 2,
                "question": "你是否感到心跳加速或心慌？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 3,
                "question": "你是否出现睡眠困难（入睡困难或早醒）？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
        ]
    elif assessment_type == "depression":
        questions = [
            {
                "id": 1,
                "question": "你是否对做事情失去兴趣或乐趣？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 2,
                "question": "你是否感到情绪低落、沮丧或绝望？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
            {
                "id": 3,
                "question": "你是否感到疲倦或没有活力？",
                "options": [
                    {"value": 0, "label": "从不"},
                    {"value": 1, "label": "偶尔"},
                    {"value": 2, "label": "经常"},
                    {"value": 3, "label": "总是"},
                ],
            },
        ]
    else:
        # 通用评估
        questions = [
            {
                "id": 1,
                "question": "在过去一个月中，你的整体情绪状态如何？",
                "options": [
                    {"value": 5, "label": "非常好"},
                    {"value": 4, "label": "比较好"},
                    {"value": 3, "label": "一般"},
                    {"value": 2, "label": "不太好"},
                    {"value": 1, "label": "很差"},
                ],
            },
            {
                "id": 2,
                "question": "你是否能有效地管理学习和生活中的压力？",
                "options": [
                    {"value": 5, "label": "完全可以"},
                    {"value": 4, "label": "基本可以"},
                    {"value": 3, "label": "一般"},
                    {"value": 2, "label": "不太能"},
                    {"value": 1, "label": "完全不能"},
                ],
            },
            {
                "id": 3,
                "question": "你的睡眠质量如何？",
                "options": [
                    {"value": 5, "label": "很好"},
                    {"value": 4, "label": "较好"},
                    {"value": 3, "label": "一般"},
                    {"value": 2, "label": "较差"},
                    {"value": 1, "label": "很差"},
                ],
            },
            {
                "id": 4,
                "question": "你是否经常感到孤独或与人疏远？",
                "options": [
                    {"value": 1, "label": "从不"},
                    {"value": 2, "label": "偶尔"},
                    {"value": 3, "label": "有时"},
                    {"value": 4, "label": "经常"},
                    {"value": 5, "label": "总是"},
                ],
            },
        ]

    return {
        "type": assessment_type,
        "title": {
            "general": "综合心理健康评估",
            "stress": "压力水平评估",
            "anxiety": "焦虑水平评估",
            "depression": "抑郁情绪评估",
        }.get(assessment_type, "心理健康评估"),
        "description": "请根据您最近两周的真实感受回答以下问题。",
        "questions": questions,
    }


async def submit_assessment(
    db: AsyncSession,
    user_id: int,
    assessment_type: str,
    answers: dict,
) -> dict:
    """
    提交评估结果。

    Args:
        db: 数据库会话
        user_id: 用户ID
        assessment_type: 评估类型
        answers: 答案

    Returns:
        评估结果
    """
    logger.info(f"提交心理健康评估: user={user_id}, type={assessment_type}")

    # 计算得分
    total_score = sum(answers.values()) if answers else 0
    max_score = len(answers) * 3 if answers else 1
    score_ratio = total_score / max_score if max_score > 0 else 0

    # 根据得分给出建议
    if score_ratio <= 0.3:
        level = "良好"
        suggestion = (
            "你的心理健康状况良好！继续保持积极的生活态度，"
            "适当运动、保持社交，有助于维持良好的心理状态。"
        )
    elif score_ratio <= 0.6:
        level = "一般"
        suggestion = (
            "你可能会感到一些压力或不适。建议尝试以下方法："
            "规律作息、适度运动、与朋友倾诉、尝试冥想或深呼吸练习。"
            "如果症状持续，建议咨询专业心理老师。"
        )
    else:
        level = "需要关注"
        suggestion = (
            "你的评估结果显示可能需要关注心理健康。"
            "强烈建议你联系学校心理咨询中心（电话：xxx-xxxx）"
            "预约专业咨询。记住，寻求帮助是勇敢的表现。"
        )

    return {
        "type": assessment_type,
        "score": total_score,
        "max_score": max_score,
        "level": level,
        "suggestion": suggestion,
        "submitted_at": str(__import__("datetime").datetime.now()),
    }


async def get_resources(category: Optional[str]) -> dict:
    """
    获取心理健康资源。

    Args:
        category: 资源类别

    Returns:
        资源列表
    """
    logger.info(f"获取心理资源: category={category}")

    resources = [
        {
            "id": 1,
            "title": "如何应对考试焦虑",
            "type": "article",
            "category": "学业心理",
            "summary": "了解考试焦虑的原因和应对策略，帮助你在考试中发挥最佳水平。",
            "url": "/resources/exam-anxiety",
        },
        {
            "id": 2,
            "title": "大学生压力管理指南",
            "type": "article",
            "category": "压力管理",
            "summary": "学习有效的压力管理技巧，平衡学习与生活。",
            "url": "/resources/stress-management",
        },
        {
            "id": 3,
            "title": "改善睡眠质量的方法",
            "type": "article",
            "category": "健康生活",
            "summary": "科学的方法帮助你改善睡眠，提高白天的精力和注意力。",
            "url": "/resources/sleep",
        },
        {
            "id": 4,
            "title": "人际交往与沟通技巧",
            "type": "article",
            "category": "人际关系",
            "summary": "提升你的社交能力，建立良好的人际关系。",
            "url": "/resources/social-skills",
        },
        {
            "id": 5,
            "title": "学校心理咨询中心",
            "type": "hotline",
            "category": "求助渠道",
            "summary": "专业心理咨询师提供免费咨询服务。",
            "contact": "电话：010-12345678",
            "address": "学生活动中心3楼",
            "hours": "周一至周五 8:30-17:00",
        },
        {
            "id": 6,
            "title": "24小时心理援助热线",
            "type": "hotline",
            "category": "求助渠道",
            "summary": "全国24小时心理危机干预热线。",
            "contact": "电话：400-161-9995",
        },
    ]

    if category:
        resources = [r for r in resources if r["category"] == category]

    return {
        "resources": resources,
        "total": len(resources),
    }


async def get_daily_tips() -> dict:
    """获取每日心理小贴士。"""
    tips = [
        {
            "tip": "每天花10分钟进行正念冥想，可以帮助减轻焦虑和压力。",
            "category": "冥想",
        },
        {
            "tip": "保持规律的作息时间，充足的睡眠是心理健康的基础。",
            "category": "睡眠",
        },
        {
            "tip": "当你感到压力大时，试试深呼吸：吸气4秒，屏息7秒，呼气8秒。",
            "category": "放松",
        },
        {
            "tip": "与朋友分享你的感受，社交支持是应对困难的重要资源。",
            "category": "社交",
        },
        {
            "tip": "设定小目标并逐步完成，可以增强你的成就感和自信心。",
            "category": "自我提升",
        },
        {
            "tip": "适当的体育锻炼可以释放内啡肽，改善情绪。",
            "category": "运动",
        },
        {
            "tip": "学会说'不'，保护自己的时间和精力边界。",
            "category": "边界",
        },
    ]

    # 根据日期选择一条
    import datetime
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    selected_tip = tips[day_of_year % len(tips)]

    return selected_tip


async def get_history(
    db: AsyncSession, user_id: int, page: int, page_size: int
) -> dict:
    """
    获取心理健康咨询历史。

    Args:
        db: 数据库会话
        user_id: 用户ID
        page: 页码
        page_size: 每页数量

    Returns:
        咨询历史列表
    """
    conditions = [
        Conversation.user_id == user_id,
        Conversation.module_type == "mental_health",
    ]

    count_stmt = select(func.count(Conversation.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    query_stmt = (
        select(Conversation)
        .where(*conditions)
        .order_by(Conversation.updated_at.desc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    conversations = result.scalars().all()

    return {
        "items": [
            {
                "id": c.id,
                "title": c.title,
                "created_at": str(c.created_at),
                "updated_at": str(c.updated_at),
            }
            for c in conversations
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }
