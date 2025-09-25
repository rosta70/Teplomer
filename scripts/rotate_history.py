import csv
import json
import shutil
from datetime import datetime
import pytz
from pathlib import Path

# Cesty
DATA_DIR = Path("docs/data")
HISTORY_FILE = DATA_DIR / "history.csv"
INDEX_FILE = DATA_DIR / "index.json"

tz = pytz.timezone("Europe/Prague")

def rotate():
    if not HISTORY_FILE.exists():
        print("Soubor history.csv neexistuje – není co archivovat.")
        return

    # Název archivu podle aktuálního měsíce
    now = datetime.now(tz)
    month_str = now.strftime("%Y_%m")
    archive_name = f"history_{month_str}.csv"
    archive_path = DATA_DIR / archive_name

    # Přesunout history.csv -> history_YYYY_MM.csv
    shutil.move(HISTORY_FILE, archive_path)
    print(f"Archivován {HISTORY_FILE} → {archive_path}")

    # Vytvořit nový prázdný history.csv s hlavičkou
    with open(HISTORY_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "source", "temp_c", "humidity_pct"])
    print(f"Vytvořen nový {HISTORY_FILE}")

    # Aktualizovat index.json
    files = [HISTORY_FILE.name] + sorted(
        [p.name for p in DATA_DIR.glob("history_*.csv")]
    )
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=2, ensure_ascii=False)
    print(f"Aktualizován {INDEX_FILE}")

if __name__ == "__main__":
    rotate()
