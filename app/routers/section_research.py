from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project

router = APIRouter()


@router.get("/projects/{pid}/research")
def research_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    return templates.TemplateResponse(
        request, "sections/research.html",
        {"project": project},
    )


@router.post("/projects/{pid}/research")
def save_research(
    pid: int,
    research_methods: str = Form(""),
    scoring_anchors: str = Form(""),
    db: Session = Depends(get_db),
):
    project = db.get(Project, pid)
    if project:
        project.research_methods = research_methods
        project.scoring_anchors = scoring_anchors
        db.commit()
    return {"ok": True}
