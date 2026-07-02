from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserProfile(Base):
    """Section 1.1 & 1.2: Target user and user profiles."""
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    target_user: Mapped[str | None] = mapped_column(Text)  # 一句话描述

    # Profile dimensions
    age: Mapped[str | None] = mapped_column(String(50))
    gender: Mapped[str | None] = mapped_column(String(20))
    occupation: Mapped[str | None] = mapped_column(String(100))
    income: Mapped[str | None] = mapped_column(String(50))
    region: Mapped[str | None] = mapped_column(String(100))
    digital_ability: Mapped[str | None] = mapped_column(String(50))
    spending_power: Mapped[str | None] = mapped_column(String(50))
    typical_traits: Mapped[str | None] = mapped_column(Text)

    # Evidence and status
    evidence: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="假设")  # 已验证/待验证/假设

    project: Mapped["Project"] = relationship(back_populates="user_profiles")  # noqa: F821


class UserSegment(Base):
    """Section 1.3: User segmentation."""
    __tablename__ = "user_segments"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_type: Mapped[str] = mapped_column(String(50))  # 核心用户/重要用户/潜在用户
    traits: Mapped[str | None] = mapped_column(Text)
    proportion: Mapped[str | None] = mapped_column(String(20))
    priority: Mapped[str | None] = mapped_column(String(10))  # P0/P1/P2
    evidence: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="user_segments")  # noqa: F821
