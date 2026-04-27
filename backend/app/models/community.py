"""
社区模型。

对应数据库表 community_posts。
包含二手交易、拼车、失物招领三种类型。
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CommunityPost(Base):
    """社区帖子模型。"""

    __tablename__ = "community_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="帖子类型: second_hand/carpool/lost_found",
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="标题"
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False, comment="内容"
    )
    images: Mapped[str] = mapped_column(
        Text, nullable=True, comment="图片URL列表(JSON数组)"
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        comment="状态: active/closed/expired",
    )
    contact_info: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="联系方式"
    )
    location: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="地点"
    )
    price: Mapped[str] = mapped_column(
        String(50), nullable=True, comment="价格（二手交易用）"
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
    user = relationship("User", back_populates="community_posts")

    def __repr__(self) -> str:
        return (
            f"<CommunityPost(id={self.id}, type='{self.type}', "
            f"title='{self.title}', status='{self.status}')>"
        )
