import os
import shutil
from datetime import datetime

DATA_DIR = "docs/data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.csv")

def rotate_history():
    if not os.path.exists(HISTORY_FILE):
        print("Soubor history.csv neexistuje.")
        return

    # Název archivu podle měsíce
    now = datetime.utcnow()
    archive_name = os.path.join(DATA_DIR, f"history_{now.strftime('%Y_%m')}.csv")

    # Přesun do archivního souboru
    shutil.move(HISTORY_FILE, archive_name)
    print(f"Přesunuto do {archive_name}")

    # Založ nový prázdný history.csv s hlavičkou
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("timestamp,source,temp_c,humidity_pct\n")
    print(f"Založen nový {HISTORY_FILE}")


if __name__ == "__main__":
    rotate_history()
