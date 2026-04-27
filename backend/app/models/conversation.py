"""
对话模型。

对应数据库表 conversations。
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Conversation(Base):
    """对话模型。"""

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, default="新对话", comment="对话标题"
    )
    module_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="campus",
        comment="模块类型: academic/campus/daily/community/mental_health",
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
    user = relationship("User", back_populates="conversations")
    messages = relationship(
        "Message", back_populates="conversation", lazy="selectin", order_by="Message.created_at"
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title='{self.title}', module='{self.module_type}')>"
