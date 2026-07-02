from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data.db"
EXPORTS_DIR = BASE_DIR / "exports"
TEMPLATES_MD_DIR = BASE_DIR / "templates"
