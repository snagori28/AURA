@echo off
call env\Scripts\activate
start "BACKEND" uvicorn backend.api_interface:app --reload
start "FRONTEND" cmd /k "cd frontend && npm run dev"
