import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta 

# Cesta k vašemu JSON souboru
INDEX_FILE = "docs/data/index.json" 

def update_index():
    # 1. Výpočet názvu nově archivovaného souboru (pro minulý měsíc)
    now = datetime.utcnow()
    previous_month = now - relativedelta(months=1)
    
    # Název, který byl vytvořen skriptem rotate_history.py (např. history_2025_09.csv)
    new_archive_file_name = f"history_{previous_month.strftime('%Y_%m')}.csv"
    current_history_file_name = "history.csv"
    
    file_list = []
    
    # 2. Načtení stávajícího JSON souboru
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            file_list = json.load(f)
        
        # OCHRANA: Pokud soubor existuje, ale není seznam
        if not isinstance(file_list, list):
            print("Varování: Načtený JSON není seznam. Inicializuji prázdný seznam.")
            file_list = []

        print(f"Soubor {INDEX_FILE} úspěšně načten.")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Varování: Soubor {INDEX_FILE} nenalezen/poškozen. Inicializuji prázdný seznam.")
        file_list = [] 
        
    # 3. Přidání/kontrola souborů
    
    # NOVÝ ARCHIVNÍ SOUBOR (history_RRRR_MM.csv)
    if new_archive_file_name not in file_list:
        # Přidáme na začátek seznamu, protože je nejnovější
        file_list.insert(0, new_archive_file_name) 
    
    # AKTIVNÍ history.csv - ZAJIŠTĚNÍ POŘADÍ
    if current_history_file_name in file_list:
        # Odstraníme ho z původního místa...
        file_list.remove(current_history_file_name)
    # ... a přidáme ho znovu na začátek, kde je nejvíce relevantní pro zobrazení
    file_list.insert(0, current_history_file_name)

    # 4. Uložení upraveného JSON souboru
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(file_list, f, indent=2) 
    print(f"Aktualizován {INDEX_FILE}. Přidán archiv: {new_archive_file_name}")

if __name__ == "__main__":
    update_index()
