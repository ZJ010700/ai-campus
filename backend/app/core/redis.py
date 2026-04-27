"""
Redis 连接配置模块。

提供 Redis 连接池和常用操作封装。
"""
import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings


class RedisClient:
    """Redis 异步客户端封装。"""

    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def init(self) -> None:
        """初始化 Redis 连接。"""
        self.redis = aioredis.from_url(
            settings.REDIS_URL,
            password=settings.REDIS_PASSWORD or None,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )

    async def close(self) -> None:
        """关闭 Redis 连接。"""
        if self.redis:
            await self.redis.close()

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
    ) -> None:
        """
        设置键值对。

        Args:
            key: 键名
            value: 值（会自动序列化为 JSON）
            expire: 过期时间（秒）
        """
        if self.redis is None:
            await self.init()
        serialized = json.dumps(value, ensure_ascii=False)
        if expire:
            await self.redis.set(key, serialized, ex=expire)
        else:
            await self.redis.set(key, serialized)

    async def get(self, key: str) -> Optional[Any]:
        """
        获取键对应的值。

        Args:
            key: 键名

        Returns:
            反序列化后的值，键不存在时返回 None
        """
        if self.redis is None:
            await self.init()
        value = await self.redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def delete(self, key: str) -> None:
        """删除键。"""
        if self.redis is None:
            await self.init()
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """检查键是否存在。"""
        if self.redis is None:
            await self.init()
        return bool(await self.redis.exists(key))

    async def set_token_blacklist(self, token: str, expire: int) -> None:
        """
        将 token 加入黑名单。

        Args:
            token: JWT token
            expire: 过期时间（秒），应与 token 本身的过期时间一致
        """
        if self.redis is None:
            await self.init()
        await self.redis.set(f"blacklist:{token}", "1", ex=expire)

    async def is_token_blacklisted(self, token: str) -> bool:
        """
        检查 token 是否在黑名单中。

        Args:
            token: JWT token

        Returns:
            是否在黑名单中
        """
        if self.redis is None:
            await self.init()
        return bool(await self.redis.exists(f"blacklist:{token}"))

    async def cache_conversation(
        self,
        user_id: int,
        conversation_id: int,
        messages: list,
        expire: int = 3600,
    ) -> None:
        """
        缓存对话消息。

        Args:
            user_id: 用户 ID
            conversation_id: 对话 ID
            messages: 消息列表
            expire: 过期时间（秒）
        """
        if self.redis is None:
            await self.init()
        key = f"conversation:{user_id}:{conversation_id}"
        await self.redis.set(key, json.dumps(messages, ensure_ascii=False), ex=expire)

    async def get_cached_conversation(
        self, user_id: int, conversation_id: int
    ) -> Optional[list]:
        """
        获取缓存的对话消息。

        Args:
            user_id: 用户 ID
            conversation_id: 对话 ID

        Returns:
            缓存的消息列表，不存在时返回 None
        """
        if self.redis is None:
            await self.init()
        key = f"conversation:{user_id}:{conversation_id}"
        value = await self.redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def incr_rate_limit(self, key: str, expire: int = 60) -> int:
        """
        递增速率限制计数器。

        Args:
            key: 限流键名
            expire: 窗口过期时间（秒）

        Returns:
            当前计数
        """
        if self.redis is None:
            await self.init()
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, expire)
        results = await pipe.execute()
        return results[0]


# 全局 Redis 客户端单例
redis_client = RedisClient()
