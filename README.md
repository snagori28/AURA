# AURA

Autonomous Understanding & Reasoning Agent

This repository contains a modular reasoning framework powered by LLMs and a Neo4j memory graph. The backend is implemented with FastAPI and the frontend is a small Next.js interface.

## Backend

Modules live in `backend/` and include agents for planning, memory access, clarification, reasoning, explanations and feedback. The main API is exposed through `api_interface.py`.

Run the API:

```bash
uvicorn backend.api_interface:app --reload
```

Environment variables `OPENAI_API_KEY` and optionally `NEO4J_URI`, `NEO4J_USER`,
and `NEO4J_PASSWORD` are required. Copy `\.env.example` to `\.env` and fill in
your credentials before starting the service. When `MemoryAgent` is created
without explicit parameters it reads these values from the environment.

## Frontend

A small Next.js application with a ChatGPT‑style interface lives in `frontend/`.
Run with:

```bash
cd frontend
npm install
npm run dev
```

Create a `.env.local` file inside `frontend/` and define `BACKEND_URL` pointing
to the running FastAPI server (defaults to `http://localhost:8000`). Frontend
API routes proxy requests to this URL so the user never interacts with the
backend endpoints directly.

## Tests

Unit tests use mocked LLM and Neo4j responses and can be executed with:

```bash
pytest
```

## Quick Start (Windows)

1. Copy `\.env.example` to `\.env` and add your OpenAI and Neo4j credentials.
2. Run `setup.bat` to create a Python virtual environment and install backend and frontend dependencies.
3. Launch the application with `start.bat`. This opens the FastAPI backend and Next.js frontend in separate windows.
4. Stop all services with `stop.bat`.

The frontend still requires a `frontend/.env.local` file containing `BACKEND_URL=http://localhost:8000` (or your custom port).
