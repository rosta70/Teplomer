#!/usr/bin/env python3
import requests, csv, os
from datetime import datetime, timezone

# URL čidel
SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f"
}

CSV_PATH = "docs/data/history.csv"
HEADER = ["timestamp_iso","source","temp_c","humidity_pct"]

# Načíst existující řádky (pokud CSV existuje)
rows = []
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

# Přidat hlavičku pokud chybí
if not rows or rows[0] != HEADER:
    rows.insert(0, HEADER)

# Zapsat nová data z API
new_rows = []
for source, url in SENSORS.items():
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()

        ts_str = data.get("posledni_zaznam_cas")
        temp_str = data.get("posledni_zaznam_teplota")
        hum_str  = data.get("posledni_zaznam_vlhkost")  # nemusí být vždy

        ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

        row = [
            ts.isoformat(),
            source,
            temp_str if temp_str not in (None,"") else "",
            hum_str if hum_str not in (None,"") else ""
        ]

        # přidat jen pokud ještě není v CSV
        if row not in rows:
            new_rows.append(row)
            print(f"✓ Nový záznam: {source} @ {ts.isoformat()} → {temp_str} °C"
                  + (f", {hum_str} %" if hum_str else ""))
        else:
            print(f"- Záznam už existuje: {source} @ {ts.isoformat()}")

    except Exception as e:
        print(f"⚠️ Chyba při načítání {source} z {url}: {e}")

if new_rows:
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(new_rows)
    print(f"=== Přidáno {len(new_rows)} nových záznamů ===")
else:
    print("=== Žádné nové záznamy k přidání ===")
