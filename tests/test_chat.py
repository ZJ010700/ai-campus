"""
AI 对话接口测试。

测试发送消息、获取对话历史、创建对话等接口。
"""
import pytest
from httpx import AsyncClient


class TestChat:
    """AI 对话接口测试。"""

    @pytest.mark.asyncio
    async def test_create_conversation(self, auth_client: AsyncClient):
        """测试创建新对话。"""
        response = await auth_client.post(
            "/api/v1/chat/conversations",
            params={
                "module_type": "campus",
                "title": "测试对话",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["title"] == "测试对话"
        assert data["module_type"] == "campus"

    @pytest.mark.asyncio
    async def test_send_message_unauthenticated(self, client: AsyncClient):
        """测试未认证用户发送消息。"""
        response = await client.post(
            "/api/v1/chat/",
            json={
                "message": "你好",
                "module_type": "campus",
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_send_message_missing_content(self, auth_client: AsyncClient):
        """测试发送空消息。"""
        response = await auth_client.post(
            "/api/v1/chat/",
            json={
                "message": "",
                "module_type": "campus",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_chat_history(self, auth_client: AsyncClient):
        """测试获取对话历史。"""
        # 先创建对话
        conv_response = await auth_client.post(
            "/api/v1/chat/conversations",
            params={
                "module_type": "campus",
                "title": "历史测试",
            },
        )
        conversation_id = conv_response.json()["conversation_id"]

        # 获取对话历史
        response = await auth_client.get(
            f"/api/v1/chat/history/{conversation_id}",
            params={"page": 1, "page_size": 50},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == conversation_id
        assert "messages" in data
        assert "total" in data

    @pytest.mark.asyncio
    async def test_get_chat_history_not_found(self, auth_client: AsyncClient):
        """测试获取不存在的对话历史。"""
        response = await auth_client.get(
            "/api/v1/chat/history/99999",
            params={"page": 1, "page_size": 50},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_chat_history_unauthenticated(self, client: AsyncClient):
        """测试未认证用户获取对话历史。"""
        response = await client.get(
            "/api/v1/chat/history/1",
            params={"page": 1, "page_size": 50},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_clear_chat_history(self, auth_client: AsyncClient):
        """测试清空对话历史。"""
        # 先创建对话
        conv_response = await auth_client.post(
            "/api/v1/chat/conversations",
            params={
                "module_type": "campus",
                "title": "清空测试",
            },
        )
        conversation_id = conv_response.json()["conversation_id"]

        # 清空对话历史
        response = await auth_client.delete(
            f"/api/v1/chat/history/{conversation_id}",
        )
        assert response.status_code == 200
        data = response.json()
        assert "deleted_count" in data
