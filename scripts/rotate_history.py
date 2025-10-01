import os
import shutil
from datetime import datetime
# Nový import pro výpočet minulého měsíce
from dateutil.relativedelta import relativedelta 

DATA_DIR = "docs/data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.csv")

def rotate_history():
    if not os.path.exists(HISTORY_FILE):
        print("Soubor history.csv neexistuje.")
        return

    # Získání aktuálního data/času
    now = datetime.utcnow()
    
    # Od aktuálního data odečti jeden měsíc, abys získal minulý měsíc
    previous_month = now - relativedelta(months=1)
    
    # Název archivu podle ROKU a MĚSÍCE, který právě skončil
    archive_name = os.path.join(DATA_DIR, f"history_{previous_month.strftime('%Y_%m')}.csv")

    # Přesun do archivního souboru
    shutil.move(HISTORY_FILE, archive_name)
    print(f"Původní soubor přesunut do archivu: {archive_name}")

    # Založ nový prázdný history.csv s hlavičkou
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("timestamp,source,temp_c,humidity_pct\n")
    print(f"Založen nový prázdný soubor: {HISTORY_FILE}")


if __name__ == "__main__":
    rotate_history()
