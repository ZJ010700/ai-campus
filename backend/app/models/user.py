"""
用户模型。

对应数据库表 users。
"""
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    """用户模型。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False, comment="用户名"
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False, comment="邮箱"
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="密码哈希"
    )
    nickname: Mapped[str] = mapped_column(
        String(100), nullable=True, comment="昵称"
    )
    avatar_url: Mapped[str] = mapped_column(
        String(500), nullable=True, comment="头像URL"
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="student",
        comment="角色: student/teacher/admin",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否激活"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )

    # 关系
    conversations = relationship(
        "Conversation", back_populates="user", lazy="selectin"
    )
    feedbacks = relationship(
        "Feedback", back_populates="user", lazy="selectin"
    )
    subscriptions = relationship(
        "Subscription", back_populates="user", lazy="selectin"
    )
    community_posts = relationship(
        "CommunityPost", back_populates="user", lazy="selectin"
    )
    service_requests = relationship(
        "ServiceRequest", back_populates="user", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
