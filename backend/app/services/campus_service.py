"""
校园信息服务。

处理校园公告、活动、通知等信息的查询和订阅。
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import Subscription
from app.utils.logger import logger


async def get_announcements(
    keyword: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    """
    获取校园公告列表。

    Args:
        keyword: 搜索关键词
        page: 页码
        page_size: 每页数量

    Returns:
        公告列表
    """
    logger.info(f"获取校园公告: keyword={keyword}, page={page}")

    # 模拟公告数据（实际应从数据库或外部API获取）
    announcements = [
        {
            "id": 1,
            "title": "关于2026年春季学期开学安排的通知",
            "content": "根据学校安排，2026年春季学期将于2月25日正式开学...",
            "author": "教务处",
            "publish_date": "2026-02-20",
            "category": "教务",
        },
        {
            "id": 2,
            "title": "图书馆开放时间调整通知",
            "content": "自3月1日起，图书馆开放时间调整为7:00-22:30...",
            "author": "图书馆",
            "publish_date": "2026-02-18",
            "category": "后勤",
        },
        {
            "id": 3,
            "title": "校园网络升级维护公告",
            "content": "为提升网络服务质量，将于本周六进行网络升级维护...",
            "author": "信息中心",
            "publish_date": "2026-02-15",
            "category": "技术",
        },
        {
            "id": 4,
            "title": "关于举办第十届校园科技节的通知",
            "content": "为激发学生创新热情，学校定于4月举办第十届校园科技节...",
            "author": "学生处",
            "publish_date": "2026-02-10",
            "category": "活动",
        },
        {
            "id": 5,
            "title": "2026年暑期社会实践报名通知",
            "content": "2026年暑期社会实践项目现已开始报名，请各学院组织学生积极参与...",
            "author": "团委",
            "publish_date": "2026-02-08",
            "category": "实践",
        },
    ]

    # 关键词过滤
    if keyword:
        announcements = [
            a for a in announcements
            if keyword in a["title"] or keyword in a["content"]
        ]

    total = len(announcements)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = announcements[start:end]

    return {
        "items": paginated,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_activities(
    category: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    """
    获取校园活动列表。

    Args:
        category: 活动类别
        page: 页码
        page_size: 每页数量

    Returns:
        活动列表
    """
    logger.info(f"获取校园活动: category={category}, page={page}")

    activities = [
        {
            "id": 1,
            "title": "春季校园马拉松",
            "description": "一年一度的校园马拉松赛事，全程5公里，欢迎全校师生参加。",
            "date": "2026-03-15",
            "location": "校园主环道",
            "category": "体育",
            "organizer": "体育部",
            "status": "报名中",
        },
        {
            "id": 2,
            "title": "AI技术讲座：大语言模型的前沿应用",
            "description": "邀请业界专家分享大语言模型在教育和科研领域的最新应用。",
            "date": "2026-03-20",
            "location": "学术报告厅",
            "category": "学术",
            "organizer": "计算机学院",
            "status": "报名中",
        },
        {
            "id": 3,
            "title": "校园歌手大赛",
            "description": "展示你的音乐才华，赢取丰厚奖品！",
            "date": "2026-04-10",
            "location": "大学生活动中心",
            "category": "文艺",
            "organizer": "学生会",
            "status": "即将开始",
        },
        {
            "id": 4,
            "title": "创业经验分享会",
            "description": "优秀校友分享创业历程和经验，助力学生创新创业。",
            "date": "2026-04-15",
            "location": "创新创业学院",
            "category": "创业",
            "organizer": "创新创业学院",
            "status": "报名中",
        },
    ]

    if category:
        activities = [a for a in activities if a["category"] == category]

    total = len(activities)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = activities[start:end]

    return {
        "items": paginated,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_notices(page: int, page_size: int) -> dict:
    """获取校园通知列表。"""
    logger.info(f"获取校园通知: page={page}")

    notices = [
        {
            "id": 1,
            "title": "关于缴纳2026年春季学费的通知",
            "content": "请各位同学于3月1日前完成学费缴纳...",
            "priority": "高",
            "publish_date": "2026-02-20",
        },
        {
            "id": 2,
            "title": "校园卡充值系统升级通知",
            "content": "校园卡充值系统将于本周末升级，届时暂停充值服务...",
            "priority": "中",
            "publish_date": "2026-02-18",
        },
    ]

    total = len(notices)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": notices[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def search_info(keyword: str, page: int, page_size: int) -> dict:
    """
    综合搜索校园信息。

    Args:
        keyword: 搜索关键词
        page: 页码
        page_size: 每页数量

    Returns:
        搜索结果
    """
    logger.info(f"搜索校园信息: keyword={keyword}")

    # 模拟搜索结果
    results = [
        {
            "id": 1,
            "type": "announcement",
            "title": f"包含'{keyword}'的公告",
            "snippet": f"这是一条与'{keyword}'相关的校园公告内容...",
            "date": "2026-02-20",
        },
        {
            "id": 2,
            "type": "activity",
            "title": f"包含'{keyword}'的活动",
            "snippet": f"这是一条与'{keyword}'相关的校园活动信息...",
            "date": "2026-03-15",
        },
    ]

    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": results[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "keyword": keyword,
    }


async def get_calendar(month: Optional[int]) -> dict:
    """
    获取校园日历。

    Args:
        month: 月份

    Returns:
        日历事件列表
    """
    logger.info(f"获取校园日历: month={month}")

    events = [
        {
            "date": "2026-03-01",
            "title": "春季学期教学周开始",
            "type": "academic",
        },
        {
            "date": "2026-03-15",
            "title": "校园马拉松",
            "type": "activity",
        },
        {
            "date": "2026-04-04",
            "title": "清明节假期",
            "type": "holiday",
        },
        {
            "date": "2026-04-15",
            "title": "期中考试周",
            "type": "exam",
        },
        {
            "date": "2026-05-01",
            "title": "劳动节假期",
            "type": "holiday",
        },
        {
            "date": "2026-06-20",
            "title": "期末考试周",
            "type": "exam",
        },
        {
            "date": "2026-07-01",
            "title": "暑假开始",
            "type": "holiday",
        },
    ]

    if month:
        events = [e for e in events if int(e["date"].split("-")[1]) == month]

    return {
        "events": events,
        "month": month,
    }


async def subscribe_info(
    db: AsyncSession, user_id: int, category: str, keyword: str
) -> dict:
    """
    订阅校园信息。

    Args:
        db: 数据库会话
        user_id: 用户ID
        category: 订阅类别
        keyword: 订阅关键词

    Returns:
        订阅结果
    """
    logger.info(f"用户 {user_id} 订阅信息: category={category}, keyword={keyword}")

    subscription = Subscription(
        user_id=user_id,
        category=category,
        keyword=keyword,
        is_active=True,
    )
    db.add(subscription)
    await db.flush()

    return {
        "message": "订阅成功",
        "category": category,
        "keyword": keyword,
    }
