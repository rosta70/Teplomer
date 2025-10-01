import json
import os
from datetime import datetime
# Potřebujeme pro výpočet minulého měsíce
from dateutil.relativedelta import relativedelta 

# OPRAVENÁ CESTA: Odkazuje na umístění v repozitáři: Teplomer/docs/data/index.json
INDEX_FILE = "docs/data/index.json" 

def update_index():
    # 1. Výpočet názvu archivního souboru (stejná logika jako v rotate_history.py)
    now = datetime.utcnow()
    previous_month = now - relativedelta(months=1)
    
    # Název nově archivovaného souboru (např. history_2025_09.csv)
    # Předpokládáme, že index.json v /docs/data odkazuje na soubory uvnitř /docs/data
    new_archive_file_name = f"history_{previous_month.strftime('%Y_%m')}.csv"
    current_history_file_name = "history.csv"
    
    data = {}
    
    # 2. Načtení stávajícího JSON souboru
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Soubor {INDEX_FILE} úspěšně načten.")
    except FileNotFoundError:
        # Vytvoření prázdné struktury, pokud soubor neexistuje
        print(f"Varování: Soubor {INDEX_FILE} nenalezen. Vytvářím prázdnou strukturu.")
        data = {} 
    except json.JSONDecodeError:
        print(f"Chyba: Soubor {INDEX_FILE} obsahuje neplatný JSON. Vracím prázdnou strukturu.")
        data = {}
        
    # 3. Zajištění, že existuje klíč "history_files" a je to seznam
    if "history_files" not in data or not isinstance(data["history_files"], list):
        data["history_files"] = []
    
    # 4. Přidání/kontrola souborů
    files_to_manage = [new_archive_file_name, current_history_file_name]

    for filename in files_to_manage:
        if filename not in data["history_files"]:
            # Přidání nového archivního souboru na začátek seznamu (nebo kamkoli chcete)
            if filename == new_archive_file_name:
                data["history_files"].insert(0, filename)
            # Zajištění, že tam je odkaz i na aktuální history.csv (např. na konec)
            elif filename == current_history_file_name:
                data["history_files"].append(filename)
                
    # 5. Uložení upraveného JSON souboru
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        # indent=2 pro hezké formátování
        json.dump(data, f, indent=2) 
    print(f"Aktualizován {INDEX_FILE}. Přidán archiv: {new_archive_file_name}")

if __name__ == "__main__":
    update_index()
