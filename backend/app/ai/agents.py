"""
多 Agent 调度器模块。
实现关键词 + LLM 双层路由策略。
"""
import re
from typing import Dict, List, Optional

from app.ai.prompts import AGENT_PROMPTS, MAIN_ROUTER_PROMPT
from app.ai.tools import TOOL_REGISTRY
from app.core.config import settings
from app.utils.logger import logger


class AgentDispatcher:
    """多 Agent 调度器。"""

    def __init__(self):
        self._keyword_rules = {
            "academic": ["课程", "选课", "考试", "成绩", "学分", "GPA", "绩点", "作业", "论文", "答辩", "毕业", "学位", "考研", "保研", "教学", "教务", "教材", "实验", "实习", "学习", "复习", "高数", "英语", "物理", "化学", "数学", "专业", "必修", "选修", "课表", "上课", "期中", "期末", "补考"],
            "campus": ["校园", "地图", "教学楼", "图书馆", "食堂", "宿舍", "操场", "校门", "地址", "位置", "怎么走", "在哪", "学院", "系", "校历", "开学", "放假", "通知", "公告", "新闻", "校长", "办公室", "行政", "招生", "就业", "校医院", "打印", "ATM"],
            "daily": ["菜单", "吃饭", "食堂", "外卖", "座位", "借书", "还书", "校车", "班车", "公交", "地铁", "天气", "报修", "维修", "充值", "缴费", "水电", "网络", "WiFi", "快递", "取件", "超市", "理发", "打印", "复印", "洗澡", "热水", "洗衣"],
            "community": ["活动", "比赛", "社团", "学生会", "讲座", "晚会", "运动会", "志愿者", "兼职", "实习", "二手", "交易", "失物", "招领", "拼车", "组队", "交友", "表白", "跳蚤", "集市", "投票", "报名", "演出", "展览", "电影", "音乐"],
            "mental_health": ["心理", "压力", "焦虑", "抑郁", "失眠", "情绪", "烦恼", "孤独", "迷茫", "困惑", "害怕", "紧张", "哭", "难过", "不开心", "想哭", "崩溃", "受不了", "自杀", "自残", "咨询", "心理医生", "心理咨询", "心理中心", "调节"],
        }
        self._keyword_tool_rules = {
            "query_canteen_menu": [{"keywords": ["菜单", "吃什么", "食堂", "午餐", "晚餐", "早餐", "饭"]}],
            "query_library_seats": [{"keywords": ["座位", "自习", "图书馆", "阅览室"]}],
            "query_course_schedule": [{"keywords": ["课表", "课程表", "上课时间", "今天有什么课"]}],
            "query_exam_schedule": [{"keywords": ["考试安排", "考试时间", "什么时候考试", "考场"]}],
            "query_weather": [{"keywords": ["天气", "温度", "下雨", "刮风"]}],
            "query_bus_schedule": [{"keywords": ["校车", "班车", "时刻表"]}],
            "search_books": [{"keywords": ["搜书", "找书", "图书搜索", "借阅"]}],
            "query_announcements": [{"keywords": ["公告", "通知", "最新消息"]}],
            "query_activities": [{"keywords": ["活动", "比赛", "讲座", "演出"]}],
        }

    def _match_keywords(self, message: str) -> Optional[str]:
        message_lower = message.lower()
        best_match = None
        best_score = 0
        for agent_type, keywords in self._keyword_rules.items():
            score = sum(1 for kw in keywords if kw in message_lower)
            if score > best_score:
                best_score = score
                best_match = agent_type
        if best_score >= 2:
            return best_match
        high_priority_keywords = {"心理", "自杀", "自残", "抑郁", "崩溃", "受不了", "心理咨询", "压力", "焦虑", "失眠"}
        for kw in high_priority_keywords:
            if kw in message_lower:
                return "mental_health"
        return None

    def _match_tools(self, message: str) -> List[Dict]:
        message_lower = message.lower()
        tool_calls = []
        for tool_name, rules in self._keyword_tool_rules.items():
            for rule in rules:
                keywords = rule["keywords"]
                if any(kw in message_lower for kw in keywords):
                    args = self._extract_tool_args(tool_name, message)
                    tool_calls.append({"name": tool_name, "args": args})
                    break
        return tool_calls

    def _extract_tool_args(self, tool_name: str, message: str) -> dict:
        args = {}
        if tool_name == "query_canteen_menu":
            for canteen in ["一食堂", "二食堂", "三食堂", "教工食堂"]:
                if canteen in message:
                    args["canteen"] = canteen
                    break
            meal_map = {"早餐": "breakfast", "午餐": "lunch", "晚餐": "dinner", "早饭": "breakfast", "午饭": "lunch", "晚饭": "dinner", "早上": "breakfast", "中午": "lunch", "晚上": "dinner"}
            for cn, en in meal_map.items():
                if cn in message:
                    args["meal_type"] = en
                    break
        elif tool_name == "query_library_seats":
            floor_match = re.search(r"(\d+)\s*楼", message)
            if floor_match:
                args["floor"] = int(floor_match.group(1))
        elif tool_name == "search_books":
            for kw in ["搜索", "查找", "找", "搜"]:
                idx = message.find(kw)
                if idx != -1:
                    keyword = message[idx + len(kw):].strip()
                    keyword = re.sub(r"[的了一是]", "", keyword).strip()
                    if keyword:
                        args["keyword"] = keyword
                    break
        return args

    async def _llm_route(self, message: str, module_type: str) -> Optional[str]:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage, SystemMessage
            llm = ChatOpenAI(model=settings.DASHSCOPE_MODEL, api_key=settings.DASHSCOPE_API_KEY, base_url=settings.DASHSCOPE_BASE_URL, temperature=0, max_tokens=50)
            route_prompt = f"""{MAIN_ROUTER_PROMPT}

请判断以下用户消息最应该由哪个 Agent 处理。只返回 Agent 类型名称。
可选类型：academic, campus, daily, community, mental_health
用户消息：{message}
当前模块：{module_type}"""
            response = await llm.ainvoke([SystemMessage(content=route_prompt), HumanMessage(content=message)])
            result = response.content.strip().lower()
            valid_types = {"academic", "campus", "daily", "community", "mental_health"}
            for valid_type in valid_types:
                if valid_type in result:
                    return valid_type
            return None
        except Exception as e:
            logger.warning(f"LLM 路由失败: {e}")
            return None

    async def route(self, message: str, module_type: str = "campus") -> Dict:
        result = {"agent_type": module_type, "tool_calls": [], "prompt_enhancement": ""}
        keyword_agent = self._match_keywords(message)
        if keyword_agent:
            result["agent_type"] = keyword_agent
            logger.info(f"关键词路由: {message[:30]}... -> {keyword_agent}")
        else:
            llm_agent = await self._llm_route(message, module_type)
            if llm_agent:
                result["agent_type"] = llm_agent
                logger.info(f"LLM 路由: {message[:30]}... -> {llm_agent}")
        agent_type = result["agent_type"]
        if agent_type in AGENT_PROMPTS:
            result["prompt_enhancement"] = AGENT_PROMPTS[agent_type]
        tool_calls = self._match_tools(message)
        if tool_calls:
            result["tool_calls"] = tool_calls
            logger.info(f"工具匹配: {message[:30]}... -> {[t['name'] for t in tool_calls]}")
        return result
