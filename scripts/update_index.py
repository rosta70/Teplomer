# scripts/update_index.py
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

INDEX_FILE = "index.json" # Předpokládáme, že je v kořenu repozitáře
DATA_DIR = "docs/data"

def update_index():
    # Použijeme stejnou logiku pro zjištění názvu minulého měsíce
    now = datetime.utcnow()
    previous_month = now - relativedelta(months=1)
    
    # Název nově archivovaného souboru (relativní cesta)
    new_file_name = f"{DATA_DIR}/history_{previous_month.strftime('%Y_%m')}.csv"
    
    data = {}
    
    # 1. Načtení stávajícího JSON souboru
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Soubor {INDEX_FILE} nenalezen. Vytvářím novou strukturu.")
        # Lze případně vytvořit základní strukturu, pokud neexistuje

    # Zajištění, že existuje klíč "history_files" a je to seznam
    if "history_files" not in data or not isinstance(data["history_files"], list):
        data["history_files"] = []
    
    # 2. Přidání nové cesty, pokud už tam není
    # Přidáme cestu k novému archivnímu souboru
    # Můžete také přidat cestu k prázdnému history.csv pro aktuální data
    
    files_to_add = [
        new_file_name,
        f"{DATA_DIR}/history.csv" # Prázdný soubor
    ]

    for filename in files_to_add:
        # Použijte set(data["history_files"]) pro efektivní kontrolu duplicit
        if filename not in data["history_files"]:
            data["history_files"].append(filename)

    # Volitelné: Setřídit soubory, aby byly v logickém pořadí (starší > novější)
    data["history_files"].sort()
    
    # 3. Uložení upraveného JSON souboru
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        # indent=2 pro hezké formátování
        json.dump(data, f, indent=2) 
    print(f"Aktualizován {INDEX_FILE} s novým archivním souborem: {new_file_name}")

if __name__ == "__main__":
    update_index()
