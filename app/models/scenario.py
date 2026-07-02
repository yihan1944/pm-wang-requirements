from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Scenario(Base):
    """Section 2.1 & 2.3: Core usage scenarios."""
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    target_user_id: Mapped[int | None] = mapped_column(ForeignKey("user_profiles.id"))
    name: Mapped[str] = mapped_column(String(200))
    time_desc: Mapped[str | None] = mapped_column(String(100))
    location: Mapped[str | None] = mapped_column(String(100))
    trigger_event: Mapped[str | None] = mapped_column(Text)
    frequency: Mapped[str | None] = mapped_column(String(50))
    user_behavior: Mapped[str | None] = mapped_column(Text)
    user_goal: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="scenarios")  # noqa: F821
    target_user: Mapped["UserProfile"] = relationship()  # noqa: F821


class BehaviorPath(Base):
    """Section 2.2: User behavior path nodes."""
    __tablename__ = "behavior_paths"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    step_name: Mapped[str] = mapped_column(String(50))  # 触发需求/寻找方案/选择产品/使用产品/完成目标
    step_order: Mapped[int] = mapped_column(Integer)
    churn_risk: Mapped[str | None] = mapped_column(Text)
    alternative_actions: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="behavior_paths")  # noqa: F821
