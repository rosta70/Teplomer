import requests
import csv
import os
from datetime import datetime
import pytz

# NOVÉ: Adresy používající ULOHA=nacti_data_jen_posledni, která vrací JSON slovník
SENSORS = {
    "UNI": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_2500&kod=49b5cf6b0607e62aa6d4cb10912cf107",
    "Venek": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_320&kod=fb2255b580a412aed10172ab7d973c7f",
    "Doma": "https://brrr.cz/brrr.php?runpagephp=afterlogin&uloha=nacti_data_jen_posledni&ssid=Teplomer_UNI_318&kod=b2038caff21963d4f356aca3ea30387b" 
}

HISTORY_FILE = "docs/data/history.csv"
tz = pytz.timezone("Europe/Prague") 

def fetch_data():
    results = []
    for source, url in SENSORS.items():
        try:
            r = requests.get(url, timeout=5) 
            r.raise_for_status()
            data = r.json() # data je JSON slovník, např. {"ssid": "...", "posledni_zaznam_cas": "..."}

            # Kontrola pro případ, že API vrátí pole (což by nemělo, ale pro jistotu)
            if isinstance(data, list) and data:
                data = data[0]

            # Důležité: Extrahujeme data přímo ze slovníku (ne z pole prvků)
            timestamp = data.get("posledni_zaznam_cas")
            temp = data.get("posledni_zaznam_teplota")
            hum = data.get("posledni_zaznam_vlhkost")

            if not timestamp:
                print(f"Varování: Chybí časový záznam pro {source}. Přeskočeno.")
                continue

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
        print("Žádná nová data k přidání.")
