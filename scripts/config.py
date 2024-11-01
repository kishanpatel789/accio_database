from pathlib import Path

CONTROL = {
    "book": 1,
    "chapter": 1,
    "character": 1,
    "movie": 1,
    "potion": 1,
    "spell": 1,
}

API_SERVER = "https://api.potterdb.com"
PROJECT_DIR = Path(__file__).parents[1].resolve()
CSV_DIR = PROJECT_DIR / "data/csv"
SQLITE_DIR = PROJECT_DIR / "data/sqlite"
DB_PATH = SQLITE_DIR / "potter.db"
ERROR_FILE_PATH = PROJECT_DIR / "errors.txt"