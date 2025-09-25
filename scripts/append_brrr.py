import requests
import csv
from datetime import datetime, timezone
import os

# URL pro API (UNI a Venek)
URLS = {
    "UNI": "https://brrr.cz/brrr.php?station=UNI&format=json",
    "Venek": "https://brrr.cz/brrr.php?station=Venek&format=json"
}

HISTORY_FILE = "docs/data/history.csv"

def fetch_data():
    results = []
    for source, url in URLS.items():
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            # vezmu poslední záznam
            if isinstance(data, list) and len(data) > 0:
                rec = data[-1]
                cas = rec.get("cas") or rec.get("time") or rec.get("timestamp")
                temp = rec.get("teplota") or rec.get("temp")
                hum = rec.get("vlhkost") or rec.get("humidity")

                # čas převedu na ISO bez Z
                if cas:
                    try:
                        dt = datetime.fromisoformat(cas.replace("Z", "+00:00"))
                        cas = dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        cas = str(cas)

                results.append((cas, source, temp, hum))
        except Exception as e:
            print(f"Chyba při čtení z {url}: {e}")
    return results

def append_history(rows):
    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # pokud soubor neexistuje, přidáme hlavičku
        if not file_exists or os.path.getsize(HISTORY_FILE) == 0:
            writer.writerow(["timestamp", "source", "temp_c", "humidity_pct"])

        # zapíšu všechny řádky bez kontroly duplicity
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    data = fetch_data()
    if data:
        append_history(data)
        print(f"Zapsáno {len(data)} záznamů do {HISTORY_FILE}")
    else:
        print("Žádná data k zápisu")
