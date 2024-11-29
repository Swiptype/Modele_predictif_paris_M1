# parse_stats.py

import os
from bs4 import BeautifulSoup
import pandas as pd

# Fonction pour extraire les statistiques détaillées d'un match donné
def get_detailed_match_stats(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    #On recupere la table particuliere qu'on cherche pour chaque page
    team_stats = soup.find_all('table')[1]
    if team_stats is None:
        return None

    winning_team_stat_rows = team_stats.find('tbody').find_all('tr')[0].find_all('td')

    FGA = int(winning_team_stat_rows[1].text)#Field Goals Attempted
    FTA = int(winning_team_stat_rows[2].text)#Free Throws Attempted
    ORB = int(winning_team_stat_rows[3].text)#Offensive Rebounds
    TOV = int(winning_team_stat_rows[4].text)#Turnovers

    return FGA, FTA, ORB, TOV

# Fonction pour parser les fichiers HTML en local et extraire les informations de match
def parse_local_html(file_path,save_dir):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    game_data = []

    games = soup.find_all('div', class_='game_summary expanded nohover')

    for game in games:
        #On verifie qu'on aa bien 2 équipes par match
        teams = game.find_all('tr')
        if len(teams) < 2:
            continue

        # Extraction des noms d'équipes et des scores
        loser = teams[0].find('td').text.strip()
        loser_score = int(teams[0].find_all('td')[1].text.strip())
        winner = teams[1].find('td').text.strip()
        winner_score = int(teams[1].find_all('td')[1].text.strip())

        # Télécharger et extraire les statistiques détaillées de chaque équipe 
        # On remplace les URL pour obtenir les statistiques

        try:
            winner_FGA, winner_FTA, winner_ORB, winner_TOV = get_detailed_match_stats(file_path)
            loser_FGA, loser_FTA, loser_ORB, loser_TOV = get_detailed_match_stats(file_path)
        except:
            # On créer des valeurs par défaut si jamais elles n'existent pas sur la page
            winner_FGA = loser_FGA = 80
            winner_FTA = loser_FTA = 20
            winner_ORB = loser_ORB = 10
            winner_TOV = loser_TOV = 12

        # Calcul des possessions pour chaque équipe
        # Calcul tiré de https://www.basketusa.com/news/46925/statistiques-et-basketball-la-notion-de-possession/
        winner_possessions = winner_FGA + 0.44 * winner_FTA - winner_ORB + winner_TOV
        loser_possessions = loser_FGA + 0.44 * loser_FTA - loser_ORB + loser_TOV

        # Ajout des informations détaillées au DataFrame final
        game_data.append({
            'Team': winner,
            'Opponent': loser,
            'Points_Scored': winner_score,
            'Points_Allowed': loser_score,
            'Possessions': winner_possessions,
            'Date': file_path.split('_')[-3] + "-" + file_path.split('_')[-2] + "-" + file_path.split('_')[-1].replace(".html", "")
        })

        
        game_data.append({
            'Team': loser,
            'Opponent': winner,
            'Points_Scored': loser_score,
            'Points_Allowed': winner_score,
            'Possessions': loser_possessions,
            'Date': file_path.split('_')[-3] + "-" + file_path.split('_')[-2] + "-" + file_path.split('_')[-1].replace(".html", "")
        })
        

    return game_data

# Fonction pour lire et extraire les données de toutes les pages locales
def extract_data_from_local_pages(save_dir):
    all_matches = pd.DataFrame()
    files = [os.path.join(save_dir, f) for f in os.listdir(save_dir) if f.endswith('.html')]

    for file in files:
        match_data = parse_local_html(file,save_dir)
        all_matches = pd.concat([all_matches, pd.DataFrame(match_data)], ignore_index=True)

    return all_matches