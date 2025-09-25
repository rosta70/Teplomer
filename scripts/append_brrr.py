import requests
import csv
import os
from datetime import datetime

# URL API pro jednotlivá čidla
URLS = {
    "UNI": "https://tmep.cz/vystup-json.php?id=4065&export_key=hgzwodurps",
    "Venek": "https://tmep.cz/vystup-json.php?id=2764&export_key=vyi603xoku"
}

HISTORY_FILE = "docs/data/history.csv"

def fetch_data():
    results = []
    for source, url in URLS.items():
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, list):
                data = data[-1]  # poslední záznam
            timestamp = data.get("cas") or data.get("time")
            temp = data.get("teplota") or data.get("temp")
            hum = data.get("vlhkost") or data.get("humidity")

            # Pokud čas není ve správném formátu, použij aktuální UTC
            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except Exception:
                dt = datetime.utcnow()

            results.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "source": source,
                "temp_c": temp,
                "humidity_pct": hum
            })
        except Exception as e:
            print(f"Chyba při načítání {source}: {e}")
    return results


def append_to_csv(rows):
    file_exists = os.path.isfile(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "source", "temp_c", "humidity_pct"])
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    new_rows = fetch_data()
    if new_rows:
        append_to_csv(new_rows)
        print(f"Přidány {len(new_rows)} záznamy do {HISTORY_FILE}")
    else:
        print("Žádná nová data")
