from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.insight import Insight
from app.models.pain import PainPoint

router = APIRouter()


@router.get("/projects/{pid}/insight")
def insight_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    insights = db.query(Insight).filter_by(project_id=pid).all()
    pains = db.query(PainPoint).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/insight.html",
        {"project": project, "insights": insights, "pains": pains},
    )


@router.post("/projects/{pid}/insight")
def add_insight(
    pid: int,
    insight: str = Form(...),
    supporting_pains: str = Form(""),
    meaning: str = Form(""),
    status: str = Form("假设"),
    db: Session = Depends(get_db),
):
    i = Insight(
        project_id=pid, insight=insight,
        supporting_pains=supporting_pains, meaning=meaning, status=status,
    )
    db.add(i)
    db.commit()
    return {"ok": True, "id": i.id}


@router.post("/projects/{pid}/insight/{iid}/delete")
def delete_insight(pid: int, iid: int, db: Session = Depends(get_db)):
    i = db.get(Insight, iid)
    if i and i.project_id == pid:
        db.delete(i)
        db.commit()
    return {"ok": True}
