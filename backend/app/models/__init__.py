"""
数据库模型包。

导出所有 SQLAlchemy 模型，确保 Alembic 能正确检测到所有表。
"""
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.feedback import Feedback
from app.models.subscription import Subscription
from app.models.community import CommunityPost
from app.models.service import ServiceRequest

__all__ = [
    "User",
    "Conversation",
    "Message",
    "Feedback",
    "Subscription",
    "CommunityPost",
    "ServiceRequest",
]
