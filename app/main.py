import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gleam_scraper import competitions_to_dicts, init_database, list_competitions
from gleam_scraper.service import Competition

SCRAPER_MODE = os.getenv("SCRAPER_MODE", "auto")
TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    yield


app = FastAPI(
    title="Gleam Competitions Web App",
    description="Self-hostable web UI for browsing Gleam competitions",
    version="0.1.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


def _filter_competitions(
    competitions: List[Competition], search: str
) -> List[Competition]:
    if not search:
        return competitions

    query = search.lower()
    return [
        competition
        for competition in competitions
        if query in competition.title.lower() or query in competition.description.lower()
    ]


@app.get("/", response_class=HTMLResponse)
def index(request: Request, q: str = "", force_refresh: bool = False):
    competitions = list_competitions(
        force_refresh=force_refresh,
        scraper_mode=SCRAPER_MODE,
    )
    filtered_competitions = _filter_competitions(competitions, q)

    return TEMPLATES.TemplateResponse(
        request,
        "index.html",
        {
            "query": q,
            "count": len(filtered_competitions),
            "total_count": len(competitions),
            "competitions": competitions_to_dicts(filtered_competitions),
            "scraper_mode": SCRAPER_MODE,
        },
    )


@app.post("/refresh")
def refresh() -> RedirectResponse:
    list_competitions(force_refresh=True, scraper_mode=SCRAPER_MODE)
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/competitions")
def api_competitions(q: str = "", force_refresh: bool = False):
    competitions = list_competitions(
        force_refresh=force_refresh,
        scraper_mode=SCRAPER_MODE,
    )
    filtered_competitions = _filter_competitions(competitions, q)
    return competitions_to_dicts(filtered_competitions)

