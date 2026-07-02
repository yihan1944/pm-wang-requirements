from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Opportunity(Base):
    """Section 6.1: Product opportunity points."""
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    opportunity: Mapped[str] = mapped_column(Text)
    source_insight: Mapped[str | None] = mapped_column(Text)  # 引用5.1编号
    related_pain: Mapped[str | None] = mapped_column(Text)
    user_value: Mapped[str] = mapped_column(String(10))  # 高/中/低
    business_value: Mapped[str] = mapped_column(String(10))  # 高/中/低
    priority: Mapped[str] = mapped_column(String(10))  # P0/P1/P2
    status: Mapped[str] = mapped_column(String(20), default="假设")

    project: Mapped["Project"] = relationship(back_populates="opportunities")  # noqa: F821


class Capability(Base):
    """Section 6.2: Product capability suggestions."""
    __tablename__ = "capabilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    direction: Mapped[str] = mapped_column(String(20))  # 核心功能/体验优化/增值服务
    suggestion: Mapped[str] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="capabilities")  # noqa: F821


class MVPItem(Base):
    """Section 6.3: MVP suggestions."""
    __tablename__ = "mvp_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    feature: Mapped[str] = mapped_column(Text)
    goal: Mapped[str | None] = mapped_column(Text)
    validation_metric: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="mvp_items")  # noqa: F821
