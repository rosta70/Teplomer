import requests
import csv
from datetime import datetime

# URL a mapování senzorů
SENSORS = {
    "4065": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "2764": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f"
}

CSV_FILE = "docs/data/history.csv"

def fetch_and_append():
    rows = []
    for sensor_id, url in SENSORS.items():
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()

            # Vytáhneme hodnoty
            ts = data.get("cas")
            temp = data.get("teplota")
            hum = data.get("vlhkost")

            if ts and temp is not None:
                # použijeme číselné ID jako source
                rows.append([ts, sensor_id, temp, hum if hum is not None else ""])
        except Exception as e:
            print(f"Chyba u senzoru {sensor_id}: {e}")

    if not rows:
        print("Žádná nová data")
        return

    # Uložíme do CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
    print(f"Zapsáno {len(rows)} řádků do {CSV_FILE}")

if __name__ == "__main__":
    fetch_and_append()
