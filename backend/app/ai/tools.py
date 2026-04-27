"""
Agent 工具定义。

定义各 Agent 可调用的工具函数，如查询课程表、食堂菜单、图书馆座位等。
"""
from typing import Optional

from app.utils.logger import logger


class CampusTools:
    """校园服务工具集。"""

    @staticmethod
    async def query_canteen_menu(
        canteen: Optional[str] = None,
        meal_type: Optional[str] = None,
    ) -> str:
        """
        查询食堂菜单。

        Args:
            canteen: 食堂名称（如：一食堂、二食堂）
            meal_type: 餐次（breakfast/lunch/dinner）

        Returns:
            菜单信息字符串
        """
        logger.info(f"工具调用: 查询食堂菜单 canteen={canteen}, meal={meal_type}")

        menus = {
            "一食堂": {
                "breakfast": "豆浆1.5元、油条2元、包子(肉)2元、包子(素)1.5元、鸡蛋饼3元、小米粥1元",
                "lunch": "红烧肉12元、宫保鸡丁10元、麻婆豆腐6元、清炒时蔬5元、番茄蛋汤3元、米饭1元",
                "dinner": "水煮鱼15元、回锅肉11元、蒜蓉西兰花6元、酸辣土豆丝5元、紫菜蛋花汤3元",
            },
            "二食堂": {
                "breakfast": "牛奶2.5元、面包3元、煎饺4元、八宝粥2元",
                "lunch": "糖醋里脊13元、鱼香肉丝10元、地三鲜7元、蛋花汤2元",
                "dinner": "干锅花菜8元、酸菜鱼16元、炒饭8元",
            },
        }

        if canteen and canteen in menus:
            if meal_type and meal_type in menus[canteen]:
                return f"{canteen}{meal_type}菜单：{menus[canteen][meal_type]}"
            return f"{canteen}菜单：{menus[canteen]}"
        elif canteen:
            return f"未找到{canteen}的菜单信息。可用食堂：一食堂、二食堂"
        else:
            result = "各食堂菜单：\n"
            for name, meals in menus.items():
                result += f"\n【{name}】\n"
                for meal, items in meals.items():
                    meal_name = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐"}.get(meal, meal)
                    result += f"  {meal_name}：{items}\n"
            return result

    @staticmethod
    async def query_library_seats(
        area: Optional[str] = None,
        floor: Optional[int] = None,
    ) -> str:
        """
        查询图书馆座位。

        Args:
            area: 区域名称
            floor: 楼层

        Returns:
            座位信息字符串
        """
        logger.info(f"工具调用: 查询图书馆座位 area={area}, floor={floor}")

        areas = [
            {"name": "一楼自习区", "floor": 1, "total": 200, "available": 45},
            {"name": "二楼阅览区", "floor": 2, "total": 150, "available": 30},
            {"name": "三楼电子阅览室", "floor": 3, "total": 100, "available": 55},
            {"name": "四楼研讨室", "floor": 4, "total": 50, "available": 12},
            {"name": "五楼静音自习区", "floor": 5, "total": 120, "available": 20},
        ]

        if floor:
            areas = [a for a in areas if a["floor"] == floor]
        if area:
            areas = [a for a in areas if area in a["name"]]

        if not areas:
            return "未找到匹配的区域信息。"

        result = "图书馆座位实时状态：\n"
        for a in areas:
            rate = (a["total"] - a["available"]) / a["total"] * 100
            result += f"  {a['name']}：剩余 {a['available']}/{a['total']} 个座位（使用率 {rate:.0f}%）\n"

        return result

    @staticmethod
    async def query_course_schedule(
        semester: Optional[str] = None,
        week: Optional[int] = None,
    ) -> str:
        """
        查询课程表。

        Args:
            semester: 学期
            week: 周次

        Returns:
            课程表信息字符串
        """
        logger.info(f"工具调用: 查询课程表 semester={semester}, week={week}")

        schedule = """
周一：
  1-2节 08:00-09:40 高等数学 教学楼C101
  3-4节 10:00-11:40 计算机导论 教学楼A301
周二：
  1-2节 08:00-09:40 数据结构与算法 教学楼B205
  3-4节 10:00-11:40 大学物理 理学楼201
周三：
  1-2节 08:00-09:40 高等数学 教学楼C101
  5-6节 14:00-15:40 大学英语（四） 外语楼302
周四：
  1-2节 08:00-09:40 大学物理 理学楼201
  3-4节 10:00-11:40 数据结构与算法 教学楼B205
周五：
  1-2节 08:00-09:40 高等数学 教学楼C101
"""
        return f"课程表（{semester or '2025-2026-2'} 第{week or 1}周）：\n{schedule}"

    @staticmethod
    async def query_exam_schedule(semester: Optional[str] = None) -> str:
        """
        查询考试安排。

        Args:
            semester: 学期

        Returns:
            考试安排字符串
        """
        logger.info(f"工具调用: 查询考试安排 semester={semester}")

        exams = """
1. 高等数学 - 4月20日 09:00-11:00 教学楼C101 座位A-15 闭卷
2. 数据结构与算法 - 4月22日 14:00-16:00 教学楼B205 座位B-08 闭卷
3. 大学物理 - 4月25日 09:00-11:00 理学楼201 座位C-22 闭卷
4. 大学英语（四） - 4月28日 14:00-16:00 外语楼302 座位D-11 笔试+听力
"""
        return f"考试安排（{semester or '2025-2026-2'}）：\n{exams}"

    @staticmethod
    async def query_weather() -> str:
        """
        查询天气信息。

        Returns:
            天气信息字符串
        """
        logger.info("工具调用: 查询天气")

        return "今日天气：多云，温度18-25°C，湿度65%，东南风3级。天气适宜，建议穿着薄外套。"

    @staticmethod
    async def query_bus_schedule(route: Optional[str] = None) -> str:
        """
        查询校车时刻表。

        Args:
            route: 线路名称

        Returns:
            校车时刻表字符串
        """
        logger.info(f"工具调用: 查询校车时刻表 route={route}")

        schedules = """
【主校区-南校区】
  07:00 → 07:15(地铁站) → 07:30(南校区东门)
  08:00 → 08:15(地铁站) → 08:30(南校区东门)
  12:00 → 12:15(地铁站) → 12:30(南校区东门)
  17:30 → 17:45(地铁站) → 18:00(南校区东门)
  21:00 → 21:15(地铁站) → 21:30(南校区东门)

【主校区-火车站】
  06:30 → 07:00(火车站广场)
  09:00 → 09:30(火车站广场)
  14:00 → 14:30(火车站广场)
  18:00 → 18:30(火车站广场)
"""
        return f"校车时刻表：\n{schedules}"

    @staticmethod
    async def search_books(keyword: str) -> str:
        """
        搜索图书。

        Args:
            keyword: 搜索关键词

        Returns:
            图书搜索结果字符串
        """
        logger.info(f"工具调用: 搜索图书 keyword={keyword}")

        books = [
            f"《Python编程：从入门到实践》- Eric Matthes - 三楼 TP312/123 - 可借(3/5)",
            f"《算法导论》- Thomas H. Cormen - 三楼 TP301/456 - 可借(2/8)",
            f"《深度学习》- Ian Goodfellow - 三楼 TP181/789 - 已借出(0/4)",
        ]

        result = f"搜索'{keyword}'的结果：\n"
        for book in books:
            result += f"  {book}\n"
        return result

    @staticmethod
    async def query_announcements(keyword: Optional[str] = None) -> str:
        """
        查询校园公告。

        Args:
            keyword: 搜索关键词

        Returns:
            公告信息字符串
        """
        logger.info(f"工具调用: 查询校园公告 keyword={keyword}")

        announcements = [
            "【教务处】关于2026年春季学期开学安排的通知 (2月20日)",
            "【图书馆】图书馆开放时间调整通知 (2月18日)",
            "【信息中心】校园网络升级维护公告 (2月15日)",
            "【学生处】关于举办第十届校园科技节的通知 (2月10日)",
            "【团委】2026年暑期社会实践报名通知 (2月8日)",
        ]

        result = "最新校园公告：\n"
        for ann in announcements:
            result += f"  {ann}\n"
        return result

    @staticmethod
    async def query_activities(category: Optional[str] = None) -> str:
        """
        查询校园活动。

        Args:
            category: 活动类别

        Returns:
            活动信息字符串
        """
        logger.info(f"工具调用: 查询校园活动 category={category}")

        activities = [
            "【体育】春季校园马拉松 - 3月15日 校园主环道 - 报名中",
            "【学术】AI技术讲座：大语言模型的前沿应用 - 3月20日 学术报告厅 - 报名中",
            "【文艺】校园歌手大赛 - 4月10日 大学生活动中心 - 即将开始",
            "【创业】创业经验分享会 - 4月15日 创新创业学院 - 报名中",
        ]

        if category:
            activities = [a for a in activities if category in a]

        result = "近期校园活动：\n"
        for act in activities:
            result += f"  {act}\n"
        return result


# 工具名称到函数的映射
TOOL_REGISTRY = {
    "query_canteen_menu": CampusTools.query_canteen_menu,
    "query_library_seats": CampusTools.query_library_seats,
    "query_course_schedule": CampusTools.query_course_schedule,
    "query_exam_schedule": CampusTools.query_exam_schedule,
    "query_weather": CampusTools.query_weather,
    "query_bus_schedule": CampusTools.query_bus_schedule,
    "search_books": CampusTools.search_books,
    "query_announcements": CampusTools.query_announcements,
    "query_activities": CampusTools.query_activities,
}


# 工具描述（供 Agent 选择使用）
TOOL_DESCRIPTIONS = """
## 可用工具

1. **query_canteen_menu** - 查询食堂菜单
   参数：canteen(食堂名称,可选), meal_type(餐次breakfast/lunch/dinner,可选)

2. **query_library_seats** - 查询图书馆座位
   参数：area(区域名称,可选), floor(楼层,可选)

3. **query_course_schedule** - 查询课程表
   参数：semester(学期,可选), week(周次,可选)

4. **query_exam_schedule** - 查询考试安排
   参数：semester(学期,可选)

5. **query_weather** - 查询天气信息
   参数：无

6. **query_bus_schedule** - 查询校车时刻表
   参数：route(线路名称,可选)

7. **search_books** - 搜索图书
   参数：keyword(搜索关键词,必填)

8. **query_announcements** - 查询校园公告
   参数：keyword(搜索关键词,可选)

9. **query_activities** - 查询校园活动
   参数：category(活动类别,可选)
"""


async def execute_tool(tool_name: str, **kwargs) -> str:
    """
    执行指定工具。

    Args:
        tool_name: 工具名称
        **kwargs: 工具参数

    Returns:
        工具执行结果字符串
    """
    tool_func = TOOL_REGISTRY.get(tool_name)
    if tool_func is None:
        return f"未知工具: {tool_name}"

    try:
        result = await tool_func(**kwargs)
        return str(result)
    except Exception as e:
        logger.error(f"工具执行失败: {tool_name}, error: {e}")
        return f"工具执行失败: {str(e)}"
