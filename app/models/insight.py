from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Insight(Base):
    """Section 5.1: Core insights derived from pain points."""
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    insight: Mapped[str] = mapped_column(Text)
    supporting_pains: Mapped[str | None] = mapped_column(Text)  # 引用4.1/4.2编号
    meaning: Mapped[str | None] = mapped_column(Text)  # 洞察含义
    status: Mapped[str] = mapped_column(String(20), default="假设")

    project: Mapped["Project"] = relationship(back_populates="insights")  # noqa: F821
