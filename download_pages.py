# download_pages.py

import os
import random
import requests
import time
from datetime import timedelta

# Création d'un répertoire de sauvegarde des pages HTML
save_dir = "nba_season_pages"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Téléchargement des pages d'une saison NBA
def download_season_pages(start_date, end_date, save_dir):
    current_date = start_date
    while current_date <= end_date:
        file_name = f"boxscore_{current_date.year}_{current_date.month:02d}_{current_date.day:02d}.html"
        file_path = os.path.join(save_dir, file_name)

        if not os.path.isfile(file_path):
            url = f"https://www.basketball-reference.com/boxscores/?month={current_date.month}&day={current_date.day}&year={current_date.year}"
            headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'}

            for attempt in range(3):
                try:
                    response = requests.get(url, headers=headers, timeout=3)
                    if response.status_code == 200:
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(response.text)
                        print(f"Téléchargement réussi : {current_date.strftime('%Y-%m-%d')}")
                        break
                    else:
                        print(f"Échec : {current_date.strftime('%Y-%m-%d')} - Code: {response.status_code}")
                except Exception as e:
                    print(f"Erreur pour {current_date.strftime('%Y-%m-%d')}: {e}")
                time.sleep((2 ** attempt) + random.random())
        current_date += timedelta(days=1)
        time.sleep(1)
