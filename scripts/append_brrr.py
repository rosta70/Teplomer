import requests
import csv
from datetime import datetime
import os

HISTORY_FILE = "docs/data/history.csv"

# Číselná ID musí zůstat stejná kvůli grafu (4065 = UNI, 2764 = Venek)
SENSORS = {
    "4065": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "2764": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f"
}

def fetch_data():
    rows = []
    for sid, url in SENSORS.items():
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()

            ts = data.get("posledni_zaznam_cas")
            temp = data.get("posledni_zaznam_teplota")
            hum  = data.get("posledni_zaznam_vlhkost")

            if ts and temp is not None:
                # timestamp uložíme jako prostý string bez Z
                rows.append([ts, sid, temp, hum if hum is not None else ""])
        except Exception as e:
            print(f"[WARN] {sid}: {e}")
    return rows

def append_history(rows):
    newfile = not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # přidáme hlavičku jen pokud je soubor nový/prázdný
        if newfile:
            writer.writerow(["timestamp", "source", "temp_c", "humidity_pct"])
        writer.writerows(rows)

if __name__ == "__main__":
    rows = fetch_data()
    if rows:
        append_history(rows)
        print(f"Zapsáno {len(rows)} řádků do {HISTORY_FILE}")
    else:
        print("Žádná data k zápisu")
