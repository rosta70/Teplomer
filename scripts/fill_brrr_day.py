import requests
import csv
from datetime import datetime, timedelta
import pytz
from pathlib import Path

DATA_FILE = Path("docs/data/history.csv")
tz = pytz.timezone("Europe/Prague")

SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f",
    "Doma": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data&ssid=Teplomer_UNI_318&kod=b2038caff21963d4f356aca3ea30387b"
}

def ensure_header():
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "source", "temp_c", "humidity_pct"])

def fill_yesterday():
    yesterday = (datetime.now(tz) - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now(tz).strftime("%Y-%m-%d")

    ensure_header()
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        for name, base_url in SENSORS.items():
            url = f"{base_url}&od={yesterday}&do={today}"
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            j = r.json()

            for rec in j:
                cas = rec.get("cas")
                if not cas:
                    continue

                # převod času (už vráceného jako string) na datetime → lokální
                dt = datetime.strptime(cas, "%Y-%m-%d %H:%M:%S")
                dt_local = tz.localize(dt)
                ts = dt_local.strftime("%Y-%m-%d %H:%M:%S")

                temp = rec.get("teplota")
                hum = rec.get("vlhkost")
                writer.writerow([ts, name, temp, hum])

if __name__ == "__main__":
    fill_yesterday()
