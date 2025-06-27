@echo off
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
cd frontend
npm install
cd ..
echo Setup complete. Fill in .env and frontend/.env.local before running start.bat.
