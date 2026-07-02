from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PainPoint(Base):
    """Section 4.1 & 4.2: User pain points."""
    __tablename__ = "pain_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    # 4.1 fields
    flow_stage: Mapped[str | None] = mapped_column(String(50))
    current_behavior: Mapped[str | None] = mapped_column(Text)
    problem: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(10))  # 高/中/低
    frequency: Mapped[str] = mapped_column(String(10))  # 高/中/低
    # 4.2 fields
    root_cause: Mapped[str | None] = mapped_column(Text)
    user_impact: Mapped[str | None] = mapped_column(Text)
    evidence: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="假设")  # 已验证/待验证/假设

    project: Mapped["Project"] = relationship(back_populates="pain_points")  # noqa: F821


class Competitor(Base):
    """Section 4.3: Competitor and alternative solutions."""
    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(200))
    solution: Mapped[str | None] = mapped_column(Text)
    advantages: Mapped[str | None] = mapped_column(Text)
    limitations: Mapped[str | None] = mapped_column(Text)
    satisfaction: Mapped[str | None] = mapped_column(String(10))  # 高/中/低

    project: Mapped["Project"] = relationship(back_populates="competitors")  # noqa: F821


class UnmetNeed(Base):
    """Section 4.4: Unmet user needs."""
    __tablename__ = "unmet_needs"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    need: Mapped[str] = mapped_column(Text)
    current_alternative: Mapped[str | None] = mapped_column(Text)
    satisfaction: Mapped[str] = mapped_column(String(10))  # 高/中/低
    evidence: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="unmet_needs")  # noqa: F821
