from pathlib import Path

CONTROL = {
    "book": 1,
    "chapter": 0,
    "character": 0,
    "movie": 0,
    "potion": 0,
    "spell": 0,
}

API_SERVER = "https://api.potterdb.com"
PROJECT_DIR = Path(__file__).parents[1].resolve()
CSV_DIR = PROJECT_DIR / "data/csv"

DB_PATH = PROJECT_DIR / "potter.db"