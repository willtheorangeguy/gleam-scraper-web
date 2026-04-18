# gleam-web-app

Self-hostable web UI for listing Gleam competitions, backed by the `gleam-scraper` project as a dependency.

## Project relationship

- This repository is the web/API layer.
- `gleam-scraper` remains the source of truth for scraping/cache/database logic.
- No scraper code is copied into this repo.

## Local development

1. Copy environment file:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
uvicorn app.main:app --reload
```

Open: `http://localhost:8000`

## Docker (self-host)

1. Create `.env` from `.env.example`.
2. Build and run:

```bash
docker compose up --build
```

Open: `http://localhost:8000`

## Endpoints

- `GET /` - HTML UI for browsing competitions
- `POST /refresh` - Force refresh scraped competitions
- `GET /api/competitions` - JSON list API (`q` and `force_refresh` query params supported)

