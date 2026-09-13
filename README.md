# digitaloceantest

This repo contains a FastAPI usage API for event ingestion, quota checks, and app plan reporting.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /health`
- `GET /api/v1/quota-plan`
- `POST /api/v1/events`
- `POST /api/v1/usage`
- `GET /api/v1/usage?app_id=<app_id>`
- `GET /api/v1/apps/{app_id}/usage`

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H 'Content-Type: application/json' \
  -d '{
    "app_id": "demo-app",
    "plan_id": "starter",
    "no_of_req": 150,
    "quota": "basic",
    "resource_type": "requests",
    "client_event_id": "evt-001",
    "version": 1
  }'
```

## DigitalOcean App Platform

Use these runtime settings in DigitalOcean:

- Build command:
  ```bash
  pip install -r requirements.txt
  ```
- Run command:
  ```bash
  uvicorn src.main:app --host 0.0.0.0 --port 8000
  ```
- Port: `8000`
- Health check path: `/health`

## Environment variables

```bash
ENV=production
BASIC_RPS=5000
PRO_RPS=12000
```
