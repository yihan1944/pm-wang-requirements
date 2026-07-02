from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RequirementDoc(Base):
    """Final section: Synthesized requirement document fields."""
    __tablename__ = "requirement_docs"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    section: Mapped[str] = mapped_column(String(50))  # 背景/用户/场景/需求/痛点/机会/总结
    subsection: Mapped[str | None] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="requirement_docs")  # noqa: F821
