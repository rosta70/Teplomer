import os
import csv
from datetime import datetime

DATA_DIR = "docs/data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.csv")

def rotate_history():
    if not os.path.exists(HISTORY_FILE):
        print("Soubor history.csv neexistuje, přeskočeno.")
        return

    # načíst aktuální data
    with open(HISTORY_FILE, "r") as f:
        rows = list(csv.reader(f))

    if not rows:
        print("Soubor history.csv je prázdný, přeskočeno.")
        return

    # zjistit aktuální měsíc
    now = datetime.utcnow()
    archive_name = f"history_{now.year}_{now.month:02d}.csv"
    archived = os.path.join(DATA_DIR, archive_name)

    # uložit data do měsíčního souboru (bez hlavičky)
    with open(archived, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # vymazat původní history.csv
    open(HISTORY_FILE, "w").close()

    # aktualizovat index.json
    index_file = os.path.join(DATA_DIR, "index.json")
    files = []
    if os.path.exists(index_file):
        import json
        with open(index_file, "r") as f:
            files = json.load(f)

    if archive_name not in files:
        files.insert(0, archive_name)  # nejnovější dopředu

    with open(index_file, "w") as f:
        import json
        json.dump(files, f, indent=2)

    print(f"Archivace dokončena: {archive_name}")

if __name__ == "__main__":
    rotate_history()
