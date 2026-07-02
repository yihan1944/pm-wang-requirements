from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="消费者需求分析工具", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")

# Routers
from app.routers import projects, section_who, section_scene, section_job  # noqa: E402
from app.routers import section_pain, section_insight, section_opportunity, section_requirement  # noqa: E402
from app.routers import section_research, ai_assist  # noqa: E402

app.include_router(projects.router)
app.include_router(section_who.router)
app.include_router(section_scene.router)
app.include_router(section_job.router)
app.include_router(section_pain.router)
app.include_router(section_insight.router)
app.include_router(section_opportunity.router)
app.include_router(section_requirement.router)
app.include_router(section_research.router)
app.include_router(ai_assist.router)
