"""
通用工具函数模块。
"""
import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def generate_uuid() -> str:
    """生成 UUID 字符串。"""
    return str(uuid.uuid4())


def generate_short_uuid() -> str:
    """生成短 UUID 字符串（无连字符）。"""
    return uuid.uuid4().hex[:12]


def get_current_timestamp() -> datetime:
    """获取当前 UTC 时间。"""
    return datetime.now(timezone.utc)


def compute_md5(text: str) -> str:
    """计算字符串的 MD5 哈希值。"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本。

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后缀

    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def sanitize_html(text: str) -> str:
    """
    简单的 HTML 转义处理。

    Args:
        text: 原始文本

    Returns:
        转义后的文本
    """
    escape_map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
    }
    for char, replacement in escape_map.items():
        text = text.replace(char, replacement)
    return text


def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """
    简单的关键词提取（基于词频）。

    Args:
        text: 输入文本
        top_n: 返回前 N 个关键词

    Returns:
        关键词列表
    """
    # 移除标点符号和特殊字符
    cleaned = re.sub(r"[^\w\s\u4e00-\u9fff]", "", text)
    # 分词（简单按空格和中文分词）
    words = re.findall(r"[\w]+|[\u4e00-\u9fff]", cleaned)
    # 过滤停用词和短词
    stop_words = {
        "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都",
        "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
        "会", "着", "没有", "看", "好", "自己", "这", "他", "她", "它",
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "can", "could", "should", "may", "might", "must", "shall",
        "i", "you", "he", "she", "it", "we", "they", "me", "him",
        "her", "us", "them", "my", "your", "his", "its", "our", "their",
    }
    filtered = [w for w in words if w not in stop_words and len(w) > 1]
    # 统计词频
    word_count: Dict[str, int] = {}
    for word in filtered:
        word_count[word] = word_count.get(word, 0) + 1
    # 按词频排序
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:top_n]]


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    格式化日期时间。

    Args:
        dt: 日期时间对象

    Returns:
        格式化后的字符串
    """
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def paginate(items: List[Any], page: int, page_size: int) -> Dict[str, Any]:
    """
    分页工具函数。

    Args:
        items: 数据列表
        page: 当前页码（从 1 开始）
        page_size: 每页数量

    Returns:
        分页结果字典
    """
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


def calculate_tokens_estimate(text: str) -> int:
    """
    估算文本的 token 数量。

    简单估算：中文约 1.5 token/字，英文约 0.25 token/word。

    Args:
        text: 输入文本

    Returns:
        估算的 token 数量
    """
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    return int(chinese_chars * 1.5 + english_words * 1.3 + 10)


def build_response(
    success: bool = True,
    message: str = "操作成功",
    data: Optional[Any] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    构建统一响应格式。

    Args:
        success: 是否成功
        message: 响应消息
        data: 响应数据
        **kwargs: 额外字段

    Returns:
        响应字典
    """
    response: Dict[str, Any] = {
        "success": success,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    response.update(kwargs)
    return response
