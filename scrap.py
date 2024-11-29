# scrap.py

from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

# Recuperer les données pour les paris dans un fichier html
def scrape_data_from_html(file_path, end_period):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # On cherche la table qui encapsule toutes les données
    table = soup.find('table', class_='table bg-white table-hover table-bordered table-sm')
    
    # On verifie que la table existe
    if table is None:
        raise ValueError("Table non trouvée")

    # On cherche le tbody contenu à l'interieur de la table
    tbody = table.find('tbody')
    
    # On verifie que le tbody existe
    if tbody is None:
        raise ValueError("tbody non trouvé")

    # On recupere toutes les lignes du tbody
    rows = tbody.find_all('tr')
    
    # Extraction des données
    data = []
    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all('td')]
        if len(cols) == 13:  # On ajoute pile le bon nombre de lignes par rapport au nombre de colonnes
            try:
                row_date = datetime.strptime(cols[0], '%m%d').replace(year=end_period.year)
                if row_date > end_period:
                    break
                cols[0] = row_date
            except ValueError:
                continue

            data.append(cols)
    
    # Creation du DataFrame qui va accueillir nos données recueillies
    columns = ["Date", "Rot", "VH", "Team", "1st", "2nd", "3rd", "4th", "Final", "Open", "Close", "ML", "2H"]
    df = pd.DataFrame(data, columns=columns)
    return df