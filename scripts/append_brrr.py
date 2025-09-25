import requests
import csv
from datetime import datetime
import pytz
from pathlib import Path

# Nastavení
DATA_FILE = Path("docs/data/history.csv")
tz = pytz.timezone("Europe/Prague")

SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f"
}

def ensure_header():
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "source", "temp_c", "humidity_pct"])

def append_data():
    ensure_header()
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        for name, url in SENSORS.items():
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            j = r.json()

            ts = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            temp = j.get("posledni_zaznam_teplota")
            hum = j.get("posledni_zaznam_vlhkost")

            writer.writerow([ts, name, temp, hum])

if __name__ == "__main__":
    append_data()
