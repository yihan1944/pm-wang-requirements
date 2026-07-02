from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import StreamingResponse
from urllib.parse import quote
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import templates
from app.models.project import Project
from app.models.requirement import RequirementDoc
from app.services.export import export_project_markdown

router = APIRouter()


@router.get("/projects/{pid}/requirement")
def requirement_page(request: Request, pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    docs = db.query(RequirementDoc).filter_by(project_id=pid).all()
    return templates.TemplateResponse(
        request, "sections/requirement.html",
        {"project": project, "docs": docs},
    )


@router.post("/projects/{pid}/requirement")
def add_requirement(
    pid: int,
    section: str = Form(...),
    subsection: str = Form(""),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    d = RequirementDoc(project_id=pid, section=section, subsection=subsection, content=content)
    db.add(d)
    db.commit()
    return {"ok": True, "id": d.id}


@router.post("/projects/{pid}/requirement/{did}/delete")
def delete_requirement(pid: int, did: int, db: Session = Depends(get_db)):
    d = db.get(RequirementDoc, did)
    if d and d.project_id == pid:
        db.delete(d)
        db.commit()
    return {"ok": True}


@router.get("/projects/{pid}/export")
def export_markdown(pid: int, db: Session = Depends(get_db)):
    project = db.get(Project, pid)
    if not project:
        return {"error": "Project not found"}
    md_content = export_project_markdown(project, db)
    filename = f"{project.name}-需求分析.md"
    encoded_filename = quote(filename)
    return StreamingResponse(
        iter([md_content]),
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8'{encoded_filename}"
        },
    )
