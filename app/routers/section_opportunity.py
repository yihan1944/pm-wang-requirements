from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.opportunity import Opportunity, Capability, MVPItem
from app.models.insight import Insight
from app.models.pain import PainPoint

router = APIRouter()


@router.get("/projects/{pid}/opportunity")
def opportunity_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    opps = db.query(Opportunity).filter_by(project_id=pid).all()
    caps = db.query(Capability).filter_by(project_id=pid).all()
    mvps = db.query(MVPItem).filter_by(project_id=pid).all()
    insights = db.query(Insight).filter_by(project_id=pid).all()
    pains = db.query(PainPoint).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/opportunity.html",
        {"project": project, "opportunities": opps, "capabilities": caps, "mvps": mvps, "insights": insights, "pains": pains},
    )


@router.post("/projects/{pid}/opportunity/point")
def add_opportunity(
    pid: int,
    opportunity: str = Form(...),
    source_insight: str = Form(""),
    related_pain: str = Form(""),
    user_value: str = Form("中"),
    business_value: str = Form("中"),
    priority: str = Form("P1"),
    status: str = Form("假设"),
    db: Session = Depends(get_db),
):
    o = Opportunity(
        project_id=pid, opportunity=opportunity, source_insight=source_insight,
        related_pain=related_pain, user_value=user_value, business_value=business_value,
        priority=priority, status=status,
    )
    db.add(o)
    db.commit()
    return {"ok": True, "id": o.id}


@router.post("/projects/{pid}/opportunity/capability")
def add_capability(
    pid: int,
    direction: str = Form(...),
    suggestion: str = Form(...),
    db: Session = Depends(get_db),
):
    c = Capability(project_id=pid, direction=direction, suggestion=suggestion)
    db.add(c)
    db.commit()
    return {"ok": True, "id": c.id}


@router.post("/projects/{pid}/opportunity/mvp")
def add_mvp(
    pid: int,
    feature: str = Form(...),
    goal: str = Form(""),
    validation_metric: str = Form(""),
    db: Session = Depends(get_db),
):
    m = MVPItem(project_id=pid, feature=feature, goal=goal, validation_metric=validation_metric)
    db.add(m)
    db.commit()
    return {"ok": True, "id": m.id}


@router.post("/projects/{pid}/opportunity/point/{oid}/delete")
def delete_opportunity(pid: int, oid: int, db: Session = Depends(get_db)):
    o = db.get(Opportunity, oid)
    if o and o.project_id == pid:
        db.delete(o)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/opportunity/capability/{cid}/delete")
def delete_capability(pid: int, cid: int, db: Session = Depends(get_db)):
    c = db.get(Capability, cid)
    if c and c.project_id == pid:
        db.delete(c)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/opportunity/mvp/{mid}/delete")
def delete_mvp(pid: int, mid: int, db: Session = Depends(get_db)):
    m = db.get(MVPItem, mid)
    if m and m.project_id == pid:
        db.delete(m)
        db.commit()
    return {"ok": True}
