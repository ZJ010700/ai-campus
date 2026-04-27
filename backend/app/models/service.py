"""
服务请求模型。

对应数据库表 service_requests。
包含报修、图书馆服务、其他服务请求。
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ServiceRequest(Base):
    """服务请求模型。"""

    __tablename__ = "service_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="服务类型: repair/library/other",
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="标题"
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False, comment="详细描述"
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="状态: pending/processing/completed/cancelled",
    )
    location: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="地点"
    )
    contact_info: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="联系方式"
    )
    images: Mapped[str] = mapped_column(
        Text, nullable=True, comment="图片URL列表(JSON数组)"
    )
    handler_id: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="处理人ID"
    )
    resolution: Mapped[str] = mapped_column(
        Text, nullable=True, comment="处理结果"
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
    user = relationship("User", back_populates="service_requests")

    def __repr__(self) -> str:
        return (
            f"<ServiceRequest(id={self.id}, type='{self.type}', "
            f"title='{self.title}', status='{self.status}')>"
        )
