from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.user_profile import UserProfile, UserSegment

router = APIRouter()


@router.get("/projects/{pid}/who")
def who_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    profiles = db.query(UserProfile).filter_by(project_id=pid).all()
    segments = db.query(UserSegment).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/who.html",
        {"project": project, "profiles": profiles, "segments": segments},
    )


@router.post("/projects/{pid}/who/profile")
def add_profile(
    pid: int,
    target_user: str = Form(""),
    age: str = Form(""),
    gender: str = Form(""),
    occupation: str = Form(""),
    income: str = Form(""),
    region: str = Form(""),
    digital_ability: str = Form(""),
    spending_power: str = Form(""),
    typical_traits: str = Form(""),
    evidence: str = Form(""),
    status: str = Form("假设"),
    db: Session = Depends(get_db),
):
    profile = UserProfile(
        project_id=pid, target_user=target_user, age=age, gender=gender,
        occupation=occupation, income=income, region=region,
        digital_ability=digital_ability, spending_power=spending_power,
        typical_traits=typical_traits, evidence=evidence, status=status,
    )
    db.add(profile)
    db.commit()
    return {"ok": True, "id": profile.id}


@router.post("/projects/{pid}/who/segment")
def add_segment(
    pid: int,
    user_type: str = Form(...),
    traits: str = Form(""),
    proportion: str = Form(""),
    priority: str = Form(""),
    evidence: str = Form(""),
    db: Session = Depends(get_db),
):
    seg = UserSegment(
        project_id=pid, user_type=user_type, traits=traits,
        proportion=proportion, priority=priority, evidence=evidence,
    )
    db.add(seg)
    db.commit()
    return {"ok": True, "id": seg.id}


@router.post("/projects/{pid}/who/profile/{pid2}/delete")
def delete_profile(pid: int, pid2: int, db: Session = Depends(get_db)):
    p = db.get(UserProfile, pid2)
    if p and p.project_id == pid:
        db.delete(p)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/who/segment/{sid}/delete")
def delete_segment(pid: int, sid: int, db: Session = Depends(get_db)):
    s = db.get(UserSegment, sid)
    if s and s.project_id == pid:
        db.delete(s)
        db.commit()
    return {"ok": True}
