from datetime import datetime

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Research section
    research_methods: Mapped[str | None] = mapped_column(Text)  # JSON
    scoring_anchors: Mapped[str | None] = mapped_column(Text)  # JSON

    # Relationships
    user_profiles: Mapped[list["UserProfile"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    user_segments: Mapped[list["UserSegment"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    scenarios: Mapped[list["Scenario"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    behavior_paths: Mapped[list["BehaviorPath"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    jobs: Mapped[list["Job"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    user_goals: Mapped[list["UserGoal"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    need_classifications: Mapped[list["NeedClassification"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    pain_points: Mapped[list["PainPoint"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    unmet_needs: Mapped[list["UnmetNeed"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    insights: Mapped[list["Insight"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    opportunities: Mapped[list["Opportunity"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    capabilities: Mapped[list["Capability"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    mvp_items: Mapped[list["MVPItem"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
    requirement_docs: Mapped[list["RequirementDoc"]] = relationship(back_populates="project", cascade="all, delete-orphan")  # noqa: F821
