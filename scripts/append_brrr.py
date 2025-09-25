#!/usr/bin/env python3
import requests, csv, os
from datetime import datetime

# URL zdroje dat z brrr.cz
SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f"
}

# Mapování jména → ID (aby sedělo s tmep.cz)
MAP = {
    "UNI": "4065",
    "Venek": "2764"
}

CSV_FILE = "docs/data/history.csv"

def fetch(sensor_name, url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    ts = datetime.strptime(data["posledni_zaznam_cas"], "%Y-%m-%d %H:%M:%S")
    temp = float(data["posledni_zaznam_teplota"])
    hum = float(data.get("posledni_zaznam_vlhkost", "nan")) if "posledni_zaznam_vlhkost" in data else None
    return ts, sensor_name, temp, hum

def append_row(ts, name, temp, hum):
    src = MAP.get(name, name)  # převod UNI→4065, Venek→2764
    new_row = [ts.isoformat()+"Z", src, temp, hum]

    # načti existující řádky
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))

    # zkontroluj duplicitní záznam
    if rows and new_row == rows[-1]:
        print(f"[SKIP] Duplicitní záznam {new_row}")
        return False

    # přidej řádek
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new_row)
    print(f"[OK] {name} {ts} → {temp} °C, {hum if hum is not None else '–'} % (uloženo jako {src})")
    return True

def main():
    added = 0
    for name, url in SENSORS.items():
        try:
            ts, n, temp, hum = fetch(name, url)
            if append_row(ts, n, temp, hum):
                added += 1
        except Exception as e:
            print(f"[ERR] {name}: {e}")
    print(f"[SAVE] Uloženo {added} řádků do {CSV_FILE}")

if __name__ == "__main__":
    main()
