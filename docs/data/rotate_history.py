
#!/usr/bin/env python3
import os
import shutil
import datetime
import json

# složka se soubory
DATA_DIR = os.path.dirname(__file__)
INDEX_FILE = os.path.join(DATA_DIR, "index.json")
SRC = os.path.join(DATA_DIR, "history.csv")

def update_index(new_file):
    """Aktualizuje index.json a přidá nový archivní soubor"""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            try:
                files = json.load(f)
            except json.JSONDecodeError:
                files = []
    else:
        files = []

    # vždy dej "history.csv" jako první
    if "history.csv" in files:
        files.remove("history.csv")
    files.insert(0, "history.csv")

    # přidej archivní soubor
    if new_file not in files:
        files.append(new_file)

    # ulož zpět
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=2, ensure_ascii=False)

    print("Aktualizovaný index.json:", files)

def rotate():
    if not os.path.exists(SRC):
        print("Soubor history.csv neexistuje.")
        return

    # název archivního souboru podle měsíce
    stamp = datetime.date.today().strftime("%Y_%m")
    dst = os.path.join(DATA_DIR, f"history_{stamp}.csv")

    # přejmenuj (přesuň) aktuální history.csv
    shutil.move(SRC, dst)
    print(f"Archivováno jako {dst}")

    # vytvoř nový prázdný history.csv s hlavičkou
    with open(SRC, "w", encoding="utf-8") as f:
        f.write("timestamp_iso,source,temp_c,humidity_pct\n")
    print("Vytvořen nový prázdný history.csv")

    # aktualizuj index.json
    update_index(os.path.basename(dst))

if __name__ == "__main__":
    rotate()
