from pathlib import Path

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    load_dotenv = None

env_path = Path(__file__).resolve().parent.parent / ".env"
if load_dotenv and env_path.exists():
    load_dotenv(env_path)
