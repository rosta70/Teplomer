import requests
import csv
import os
from datetime import datetime
import pytz

# NOVÉ: Definuje URL pro získání POUZE posledního záznamu pro každé čidlo
SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f",
    # NOVÉ: Třetí čidlo "Doma"
    "Doma": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_318&kod=b2038caff21963d4f356aca3ea30387b" 
}

HISTORY_FILE = "docs/data/history.csv"
tz = pytz.timezone("Europe/Prague") # Používáme stejnou časovou zónu jako fill_brrr_day

def fetch_data():
    results = []
    for source, url in SENSORS.items():
        try:
            # NOVÉ: Používáme kratší timeout pro rychlý dotaz
            r = requests.get(url, timeout=5) 
            r.raise_for_status()
            data = r.json()

            # Data z brrr.cz jsou obvykle pole s jedním prvkem pro "jen_posledni"
            if isinstance(data, list) and data:
                rec = data[0] # Použij první (a jediný) záznam

                # Získání hodnot
                timestamp = rec.get("cas")
                temp = rec.get("teplota")
                hum = rec.get("vlhkost")

                # Převod času: lokalizujeme čas a formátujeme ho do UTC pro konzistentnost s webem
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                dt_local = tz.localize(dt)
                dt_utc = dt_local.astimezone(pytz.utc)

                results.append({
                    "timestamp": dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "source": source,
                    "temp_c": temp,
                    "humidity_pct": hum
                })
        except Exception as e:
            print(f"Chyba při načítání aktuálních dat pro {source}: {e}")
    return results


def append_to_csv(rows):
    file_exists = os.path.isfile(HISTORY_FILE)
    # POZOR: Změněny fieldnames na konzistentní s fill_brrr_day
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
