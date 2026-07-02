from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.services.validation import get_project_completion

router = APIRouter()


@router.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.updated_at.desc()).all()
    return templates.TemplateResponse(request, "index.html", {"projects": projects})


@router.get("/projects/new")
def project_create_form(request: Request):
    return templates.TemplateResponse(request, "project/create.html")


@router.post("/projects/new")
def project_create(name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    return RedirectResponse(url=f"/projects/{project.id}", status_code=303)


@router.get("/projects/{project_id}")
def project_dashboard(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        return RedirectResponse(url="/", status_code=303)
    completion = get_project_completion(project, db)
    return templates.TemplateResponse(
        request, "project/dashboard.html", {"project": project, "completion": completion},
    )


@router.post("/projects/{project_id}/delete")
def project_delete(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if project:
        db.delete(project)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
