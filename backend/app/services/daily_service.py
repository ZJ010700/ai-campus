"""
日常服务。

处理食堂菜单、图书馆服务、报修服务、天气查询、校车时刻等业务逻辑。
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import ServiceRequest
from app.schemas.service import ServiceRequestCreate
from app.utils.logger import logger


async def get_canteen_menu(
    canteen: Optional[str], meal_type: Optional[str]
) -> dict:
    """
    获取食堂菜单。

    Args:
        canteen: 食堂名称
        meal_type: 餐次 (breakfast/lunch/dinner)

    Returns:
        菜单数据
    """
    logger.info(f"获取食堂菜单: canteen={canteen}, meal={meal_type}")

    menus = {
        "一食堂": {
            "breakfast": [
                {"name": "豆浆", "price": "1.5", "tags": ["热饮", "豆制品"]},
                {"name": "油条", "price": "2.0", "tags": ["面食", "油炸"]},
                {"name": "包子（肉）", "price": "2.0", "tags": ["面食", "肉馅"]},
                {"name": "包子（素）", "price": "1.5", "tags": ["面食", "素馅"]},
                {"name": "鸡蛋饼", "price": "3.0", "tags": ["面食", "煎饼"]},
                {"name": "小米粥", "price": "1.0", "tags": ["热饮", "粥"]},
            ],
            "lunch": [
                {"name": "红烧肉", "price": "12.0", "tags": ["荤菜", "猪肉"]},
                {"name": "宫保鸡丁", "price": "10.0", "tags": ["荤菜", "鸡肉"]},
                {"name": "麻婆豆腐", "price": "6.0", "tags": ["素菜", "豆腐"]},
                {"name": "清炒时蔬", "price": "5.0", "tags": ["素菜", "蔬菜"]},
                {"name": "番茄蛋汤", "price": "3.0", "tags": ["汤类"]},
                {"name": "米饭", "price": "1.0", "tags": ["主食"]},
            ],
            "dinner": [
                {"name": "水煮鱼", "price": "15.0", "tags": ["荤菜", "鱼类"]},
                {"name": "回锅肉", "price": "11.0", "tags": ["荤菜", "猪肉"]},
                {"name": "蒜蓉西兰花", "price": "6.0", "tags": ["素菜", "蔬菜"]},
                {"name": "酸辣土豆丝", "price": "5.0", "tags": ["素菜", "土豆"]},
                {"name": "紫菜蛋花汤", "price": "3.0", "tags": ["汤类"]},
            ],
        },
        "二食堂": {
            "breakfast": [
                {"name": "牛奶", "price": "2.5", "tags": ["热饮", "奶制品"]},
                {"name": "面包", "price": "3.0", "tags": ["面食", "烘焙"]},
                {"name": "煎饺", "price": "4.0", "tags": ["面食", "饺子"]},
                {"name": "八宝粥", "price": "2.0", "tags": ["热饮", "粥"]},
            ],
            "lunch": [
                {"name": "糖醋里脊", "price": "13.0", "tags": ["荤菜", "猪肉"]},
                {"name": "鱼香肉丝", "price": "10.0", "tags": ["荤菜", "猪肉"]},
                {"name": "地三鲜", "price": "7.0", "tags": ["素菜", "蔬菜"]},
                {"name": "蛋花汤", "price": "2.0", "tags": ["汤类"]},
            ],
            "dinner": [
                {"name": "干锅花菜", "price": "8.0", "tags": ["素菜", "花菜"]},
                {"name": "酸菜鱼", "price": "16.0", "tags": ["荤菜", "鱼类"]},
                {"name": "炒饭", "price": "8.0", "tags": ["主食", "炒饭"]},
            ],
        },
    }

    result = {}
    target_canteens = [canteen] if canteen else list(menus.keys())
    for c in target_canteens:
        if c in menus:
            result[c] = {}
            target_meals = [meal_type] if meal_type else list(menus[c].keys())
            for m in target_meals:
                if m in menus[c]:
                    result[c][m] = menus[c][m]

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "canteens": result,
    }


async def get_canteens() -> dict:
    """获取食堂列表。"""
    canteens = [
        {
            "id": 1,
            "name": "一食堂",
            "location": "校园东区",
            "floors": 3,
            "business_hours": "06:30-21:00",
            "features": ["中式快餐", "面食", "特色小吃"],
            "rating": 4.3,
        },
        {
            "id": 2,
            "name": "二食堂",
            "location": "校园西区",
            "floors": 2,
            "business_hours": "06:30-20:30",
            "features": ["中式快餐", "西餐", "烘焙"],
            "rating": 4.5,
        },
        {
            "id": 3,
            "name": "清真食堂",
            "location": "校园北区",
            "floors": 1,
            "business_hours": "07:00-20:00",
            "features": ["清真菜", "西北风味"],
            "rating": 4.2,
        },
        {
            "id": 4,
            "name": "教工食堂",
            "location": "行政楼一楼",
            "floors": 1,
            "business_hours": "11:00-13:00, 17:00-19:00",
            "features": ["精致菜品", "包间"],
            "rating": 4.6,
        },
    ]

    return {"canteens": canteens}


async def get_library_seats(
    area: Optional[str], floor: Optional[int]
) -> dict:
    """
    查询图书馆座位。

    Args:
        area: 区域筛选
        floor: 楼层筛选

    Returns:
        座位状态
    """
    logger.info(f"查询图书馆座位: area={area}, floor={floor}")

    areas = [
        {
            "id": 1,
            "name": "一楼自习区",
            "floor": 1,
            "total_seats": 200,
            "available_seats": 45,
            "occupancy_rate": 0.775,
        },
        {
            "id": 2,
            "name": "二楼阅览区",
            "floor": 2,
            "total_seats": 150,
            "available_seats": 30,
            "occupancy_rate": 0.80,
        },
        {
            "id": 3,
            "name": "三楼电子阅览室",
            "floor": 3,
            "total_seats": 100,
            "available_seats": 55,
            "occupancy_rate": 0.45,
        },
        {
            "id": 4,
            "name": "四楼研讨室",
            "floor": 4,
            "total_seats": 50,
            "available_seats": 12,
            "occupancy_rate": 0.76,
        },
        {
            "id": 5,
            "name": "五楼静音自习区",
            "floor": 5,
            "total_seats": 120,
            "available_seats": 20,
            "occupancy_rate": 0.833,
        },
    ]

    if floor:
        areas = [a for a in areas if a["floor"] == floor]
    if area:
        areas = [a for a in areas if area in a["name"]]

    total_seats = sum(a["total_seats"] for a in areas)
    available_seats = sum(a["available_seats"] for a in areas)

    return {
        "areas": areas,
        "total_seats": total_seats,
        "available_seats": available_seats,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


async def search_books(
    keyword: str, page: int, page_size: int
) -> dict:
    """
    搜索图书。

    Args:
        keyword: 搜索关键词
        page: 页码
        page_size: 每页数量

    Returns:
        图书列表
    """
    logger.info(f"搜索图书: keyword={keyword}")

    books = [
        {
            "id": "B001",
            "title": "Python编程：从入门到实践",
            "author": "Eric Matthes",
            "isbn": "978-7-115-42802-8",
            "publisher": "人民邮电出版社",
            "category": "计算机",
            "location": "三楼 TP312/123",
            "status": "可借",
            "total": 5,
            "available": 3,
        },
        {
            "id": "B002",
            "title": "算法导论",
            "author": "Thomas H. Cormen",
            "isbn": "978-7-111-40701-0",
            "publisher": "机械工业出版社",
            "category": "计算机",
            "location": "三楼 TP301/456",
            "status": "可借",
            "total": 8,
            "available": 2,
        },
        {
            "id": "B003",
            "title": "深度学习",
            "author": "Ian Goodfellow",
            "isbn": "978-7-115-46170-4",
            "publisher": "人民邮电出版社",
            "category": "计算机",
            "location": "三楼 TP181/789",
            "status": "已借出",
            "total": 4,
            "available": 0,
        },
        {
            "id": "B004",
            "title": "人类简史",
            "author": "Yuval Noah Harari",
            "isbn": "978-7-5086-8tried-5",
            "publisher": "中信出版社",
            "category": "历史",
            "location": "二楼 K02/321",
            "status": "可借",
            "total": 6,
            "available": 4,
        },
    ]

    if keyword:
        books = [
            b for b in books
            if keyword in b["title"] or keyword in b["author"]
        ]

    total = len(books)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": books[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_borrowed_books() -> dict:
    """查询借阅记录。"""
    records = [
        {
            "book_id": "B001",
            "title": "Python编程：从入门到实践",
            "borrow_date": "2026-03-01",
            "due_date": "2026-04-01",
            "return_date": None,
            "status": "借阅中",
            "renew_count": 1,
        },
        {
            "book_id": "B004",
            "title": "人类简史",
            "borrow_date": "2026-02-15",
            "due_date": "2026-03-15",
            "return_date": "2026-03-10",
            "status": "已归还",
            "renew_count": 0,
        },
    ]

    return {
        "records": records,
        "total": len(records),
        "borrowing": len([r for r in records if r["status"] == "借阅中"]),
    }


async def create_service_request(
    db: AsyncSession, user_id: int, request_in: ServiceRequestCreate
) -> dict:
    """
    创建服务请求（报修等）。

    Args:
        db: 数据库会话
        user_id: 用户ID
        request_in: 服务请求数据

    Returns:
        创建的服务请求
    """
    logger.info(f"创建服务请求: user={user_id}, type={request_in.type}")

    import json

    service_request = ServiceRequest(
        user_id=user_id,
        type=request_in.type,
        title=request_in.title,
        description=request_in.description,
        location=request_in.location,
        contact_info=request_in.contact_info,
        images=json.dumps(request_in.images) if request_in.images else None,
        status="pending",
    )
    db.add(service_request)
    await db.flush()
    await db.refresh(service_request)

    return service_request


async def get_my_service_requests(
    db: AsyncSession,
    user_id: int,
    request_type: str,
    status_filter: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    """
    获取用户的服务请求列表。

    Args:
        db: 数据库会话
        user_id: 用户ID
        request_type: 请求类型
        status_filter: 状态筛选
        page: 页码
        page_size: 每页数量

    Returns:
        服务请求列表
    """
    conditions = [
        ServiceRequest.user_id == user_id,
        ServiceRequest.type == request_type,
    ]
    if status_filter:
        conditions.append(ServiceRequest.status == status_filter)

    count_stmt = select(func.count(ServiceRequest.id)).where(*conditions)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    query_stmt = (
        select(ServiceRequest)
        .where(*conditions)
        .order_by(ServiceRequest.created_at.desc())
    )
    offset = (page - 1) * page_size
    query_stmt = query_stmt.offset(offset).limit(page_size)
    result = await db.execute(query_stmt)
    requests = result.scalars().all()

    return {
        "items": requests,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def get_weather() -> dict:
    """获取天气信息。"""
    return {
        "location": "校园",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "weather": "多云",
        "temperature": "18-25C",
        "humidity": "65%",
        "wind": "东南风 3级",
        "suggestion": "天气适宜，建议穿着薄外套。",
    }


async def get_bus_schedule(route: Optional[str]) -> dict:
    """
    获取校车时刻表。

    Args:
        route: 线路筛选

    Returns:
        校车时刻表
    """
    schedules = [
        {
            "route": "主校区-南校区",
            "stops": ["主校区北门", "地铁站", "南校区东门"],
            "schedule": [
                {"departure": "07:00", "arrivals": ["07:15", "07:30"]},
                {"departure": "08:00", "arrivals": ["08:15", "08:30"]},
                {"departure": "12:00", "arrivals": ["12:15", "12:30"]},
                {"departure": "17:30", "arrivals": ["17:45", "18:00"]},
                {"departure": "21:00", "arrivals": ["21:15", "21:30"]},
            ],
        },
        {
            "route": "主校区-火车站",
            "stops": ["主校区南门", "火车站广场"],
            "schedule": [
                {"departure": "06:30", "arrivals": ["07:00"]},
                {"departure": "09:00", "arrivals": ["09:30"]},
                {"departure": "14:00", "arrivals": ["14:30"]},
                {"departure": "18:00", "arrivals": ["18:30"]},
            ],
        },
    ]

    if route:
        schedules = [s for s in schedules if route in s["route"]]

    return {"schedules": schedules}
