from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.scenario import Scenario, BehaviorPath
from app.models.user_profile import UserProfile

router = APIRouter()


@router.get("/projects/{pid}/scene")
def scene_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    scenarios = db.query(Scenario).filter_by(project_id=pid).all()
    paths = db.query(BehaviorPath).filter_by(project_id=pid).order_by(BehaviorPath.step_order).all()
    profiles = db.query(UserProfile).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/scene.html",
        {"project": project, "scenarios": scenarios, "paths": paths, "profiles": profiles},
    )


@router.post("/projects/{pid}/scene/scenario")
def add_scenario(
    pid: int,
    name: str = Form(...),
    target_user_id: int = Form(0),
    time_desc: str = Form(""),
    location: str = Form(""),
    trigger_event: str = Form(""),
    frequency: str = Form(""),
    user_behavior: str = Form(""),
    user_goal: str = Form(""),
    db: Session = Depends(get_db),
):
    s = Scenario(
        project_id=pid, name=name, time_desc=time_desc, location=location,
        trigger_event=trigger_event, frequency=frequency,
        user_behavior=user_behavior, user_goal=user_goal,
        target_user_id=target_user_id if target_user_id else None,
    )
    db.add(s)
    db.commit()
    return {"ok": True, "id": s.id}


@router.post("/projects/{pid}/scene/path")
def add_path(
    pid: int,
    step_name: str = Form(...),
    step_order: int = Form(0),
    churn_risk: str = Form(""),
    alternative_actions: str = Form(""),
    db: Session = Depends(get_db),
):
    p = BehaviorPath(
        project_id=pid, step_name=step_name, step_order=step_order,
        churn_risk=churn_risk, alternative_actions=alternative_actions,
    )
    db.add(p)
    db.commit()
    return {"ok": True, "id": p.id}


@router.post("/projects/{pid}/scene/scenario/{sid}/delete")
def delete_scenario(pid: int, sid: int, db: Session = Depends(get_db)):
    s = db.get(Scenario, sid)
    if s and s.project_id == pid:
        db.delete(s)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/scene/path/{bid}/delete")
def delete_path(pid: int, bid: int, db: Session = Depends(get_db)):
    p = db.get(BehaviorPath, bid)
    if p and p.project_id == pid:
        db.delete(p)
        db.commit()
    return {"ok": True}
