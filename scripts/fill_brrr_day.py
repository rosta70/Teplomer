#!/usr/bin/env python3
import requests, csv, os
from datetime import datetime, timedelta

SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107&od={od}&do={do}",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f&od={od}&do={do}"
}

MAP = {
    "UNI": "4065",
    "Venek": "2764"
}

CSV_FILE = "docs/data/history.csv"

def fetch_day(sensor_name, url, day):
    od = day.strftime("%Y-%m-%d")
    do = day.strftime("%Y-%m-%d")
    r = requests.get(url.format(od=od, do=do), timeout=30)
    r.raise_for_status()
    data = r.json()
    out = []
    for rec in data:
        ts = datetime.strptime(rec["cas"], "%Y-%m-%d %H:%M:%S")
        temp = float(rec.get("teplota", "nan"))
        hum = float(rec.get("vlhkost", "nan")) if "vlhkost" in rec else None
        out.append((ts, sensor_name, temp, hum))
    return out

def load_existing():
    if not os.path.exists(CSV_FILE):
        return set()
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return set(tuple(row) for row in csv.reader(f))

def append_rows(rows):
    existing = load_existing()
    added = 0
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for ts, name, temp, hum in rows:
            src = MAP.get(name, name)
            new_row = [ts.isoformat()+"Z", src, temp, hum]
            if tuple(map(str, new_row)) not in existing:
                writer.writerow(new_row)
                added += 1
    return added

def main():
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    total = 0
    for name, url in SENSORS.items():
        try:
            rows = fetch_day(name, url, yesterday)
            added = append_rows(rows)
            print(f"[OK] {name} → {added} nových záznamů pro {yesterday}")
            total += added
        except Exception as e:
            print(f"[ERR] {name}: {e}")
    print(f"[DONE] Celkem přidáno {total} záznamů.")

if __name__ == "__main__":
    main()
