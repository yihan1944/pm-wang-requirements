from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Job(Base):
    """Section 3.1: JTBD statements."""
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    scene_id: Mapped[int | None] = mapped_column(ForeignKey("scenarios.id"))
    when: Mapped[str | None] = mapped_column(Text)  # 当___的时候
    i_want: Mapped[str | None] = mapped_column(Text)  # 我希望___
    so_that: Mapped[str | None] = mapped_column(Text)  # 从而能够___
    evidence: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="jobs")  # noqa: F821
    scene: Mapped["Scenario"] = relationship()  # noqa: F821


class UserGoal(Base):
    """Section 3.2: Prioritized user goals."""
    __tablename__ = "user_goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    priority: Mapped[str] = mapped_column(String(10))  # P0/P1/P2
    goal: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="user_goals")  # noqa: F821


class NeedClassification(Base):
    """Section 3.3: User needs classification."""
    __tablename__ = "need_classifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    need_type: Mapped[str] = mapped_column(String(20))  # 功能/效率/情绪/社交/成长
    content: Mapped[str] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="need_classifications")  # noqa: F821
