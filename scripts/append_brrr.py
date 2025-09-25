#!/usr/bin/env python3
import requests
import csv
import os
from datetime import datetime

# Cesty k souborům
DATA_DIR = "docs/data"
CSV_FILE = os.path.join(DATA_DIR, "history.csv")

# Čidla (API URL + alias)
SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f",
}

# Hlavička CSV
CSV_HEADER = ["timestamp_iso", "source", "temp_c", "humidity_pct"]

def fetch_sensor(name, url):
    """Stáhne data z brrr.cz API pro jedno čidlo"""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        ts = data.get("posledni_zaznam_cas")
        temp = data.get("posledni_zaznam_teplota")
        hum = data.get("posledni_zaznam_vlhkost")  # nemusí být vždy v odpovědi

        # Konverze
        ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        temp = float(temp) if temp is not None else ""
        hum = float(hum) if hum is not None else ""

        print(f"[OK] {name} {ts} → {temp} °C, {hum} %")
        return [ts.isoformat(sep=" "), name, temp, hum]

    except Exception as e:
        print(f"[ERR] {name}: {e}")
        return None

def ensure_header(path):
    """Pokud CSV neexistuje, vytvoří ho s hlavičkou"""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
        print(f"[INIT] Vytvořen nový soubor {path}")

def append_rows(path, rows):
    """Přidá řádky do CSV"""
    if not rows:
        print("[INFO] Žádná nová data k zápisu")
        return
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"[SAVE] Uloženo {len(rows)} řádků do {path}")

def main():
    ensure_header(CSV_FILE)
    rows = []
    for name, url in SENSORS.items():
        row = fetch_sensor(name, url)
        if row:
            rows.append(row)
    append_rows(CSV_FILE, rows)

if __name__ == "__main__":
    main()
