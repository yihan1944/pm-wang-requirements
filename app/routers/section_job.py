from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.job import Job, UserGoal, NeedClassification
from app.models.scenario import Scenario

router = APIRouter()


@router.get("/projects/{pid}/job")
def job_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    jobs = db.query(Job).filter_by(project_id=pid).all()
    goals = db.query(UserGoal).filter_by(project_id=pid).all()
    needs = db.query(NeedClassification).filter_by(project_id=pid).all()
    scenes = db.query(Scenario).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/job.html",
        {"project": project, "jobs": jobs, "goals": goals, "needs": needs, "scenes": scenes},
    )


@router.post("/projects/{pid}/job/jtbd")
def add_job(
    pid: int,
    scene_id: int = Form(0),
    when: str = Form(""),
    i_want: str = Form(""),
    so_that: str = Form(""),
    evidence: str = Form(""),
    db: Session = Depends(get_db),
):
    j = Job(project_id=pid, when=when, i_want=i_want, so_that=so_that, evidence=evidence,
            scene_id=scene_id if scene_id else None)
    db.add(j)
    db.commit()
    return {"ok": True, "id": j.id}


@router.post("/projects/{pid}/job/goal")
def add_goal(
    pid: int,
    priority: str = Form(...),
    goal: str = Form(...),
    evidence: str = Form(""),
    db: Session = Depends(get_db),
):
    g = UserGoal(project_id=pid, priority=priority, goal=goal, evidence=evidence)
    db.add(g)
    db.commit()
    return {"ok": True, "id": g.id}


@router.post("/projects/{pid}/job/need")
def add_need(
    pid: int,
    need_type: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    n = NeedClassification(project_id=pid, need_type=need_type, content=content)
    db.add(n)
    db.commit()
    return {"ok": True, "id": n.id}


@router.post("/projects/{pid}/job/jtbd/{jid}/delete")
def delete_job(pid: int, jid: int, db: Session = Depends(get_db)):
    j = db.get(Job, jid)
    if j and j.project_id == pid:
        db.delete(j)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/job/goal/{gid}/delete")
def delete_goal(pid: int, gid: int, db: Session = Depends(get_db)):
    g = db.get(UserGoal, gid)
    if g and g.project_id == pid:
        db.delete(g)
        db.commit()
    return {"ok": True}


@router.post("/projects/{pid}/job/need/{nid}/delete")
def delete_need(pid: int, nid: int, db: Session = Depends(get_db)):
    n = db.get(NeedClassification, nid)
    if n and n.project_id == pid:
        db.delete(n)
        db.commit()
    return {"ok": True}
