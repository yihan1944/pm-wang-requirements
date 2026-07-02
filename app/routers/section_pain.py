from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.pain import PainPoint, Competitor, UnmetNeed

router = APIRouter()


@router.get("/projects/{pid}/pain")
def pain_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    pains = db.query(PainPoint).filter_by(project_id=pid).all()
    competitors = db.query(Competitor).filter_by(project_id=pid).all()
    unmet = db.query(UnmetNeed).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/pain.html",
        {"project": project, "pains": pains, "competitors": competitors, "unmet": unmet},
    )


@router.post("/projects/{pid}/pain/point")
def add_pain(
    pid: int,
    flow_stage: str = Form(""),
    current_behavior: str = Form(""),
    problem: str = Form(""),
    severity: str = Form("中"),
    frequency: str = Form("中"),
    root_cause: str = Form(""),
    user_impact: str = Form(""),
    evidence: str = Form(""),
    status: str = Form("假设"),
    db: Session = Depends(get_db),
):
    p = PainPoint(
        project_id=pid, flow_stage=flow_stage, current_behavior=current_behavior,
        problem=problem, severity=severity, frequency=frequency,
        root_cause=root_cause, user_impact=user_impact, evidence=evidence, status=status,
    )
    db.add(p)
    db.commit()
    return {"ok": True, "id": p.id}


@router.post("/projects/{pid}/pain/competitor")
def add_competitor(
    pid: int,
    name: str = Form(...),
    solution: str = Form(""),
    advantages: str = Form(""),
    limitations: str = Form(""),
    satisfaction: str = Form("中"),
    db: Session = Depends(get_db),
):
    c = Competitor(
        project_id=pid, name=name, solution=solution,
        advantages=advantages, limitations=limitations, satisfaction=satisfaction,
    )
    db.add(c)
    db.commit()
    return {"ok": True, "id": c.id}


@router.post("/projects/{pid}/pain/unmet")
def add_unmet(
    pid: int,
    need: str = Form(...),
    current_alternative: str = Form(""),
    satisfaction: str = Form("低"),
    evidence: str = Form(""),
    db: Session = Depends(get_db),
):
    u = UnmetNeed(
        project_id=pid, need=need, current_alternative=current_alternative,
        satisfaction=satisfaction, evidence=evidence,
    )
    db.add(u)
    db.commit()
    return {"ok": True, "id": u.id}


@router.post("/projects/{pid}/pain/point/{pid2}/delete")
def delete_pain(pid: int, pid2: int, db: Session = Depends(get_db)):
    p = db.get(PainPoint, pid2)
    if p and p.project_id == pid:
        db.delete(p)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/pain/competitor/{cid}/delete")
def delete_competitor(pid: int, cid: int, db: Session = Depends(get_db)):
    c = db.get(Competitor, cid)
    if c and c.project_id == pid:
        db.delete(c)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/pain/unmet/{uid}/delete")
def delete_unmet(pid: int, uid: int, db: Session = Depends(get_db)):
    u = db.get(UnmetNeed, uid)
    if u and u.project_id == pid:
        db.delete(u)
        db.commit()
    return {"ok": True}
