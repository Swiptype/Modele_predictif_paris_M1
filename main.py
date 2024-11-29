import pandas as pd
from datetime import datetime
from predict_model import *
from scrap import *
from download_pages import download_season_pages
from parse_stats import extract_data_from_local_pages
from betting_simulation import simulate_betting_with_data

# Fonction principale pour exécuter le script complet
def main(start_period, end_period):
    save_dir = "nba_season_pages"
    start_date = datetime(2022, 10, 18)
    end_date = datetime(2023, 4, 9)

    #Telechargement des pages web pour l'extraction des données
    #download_season_pages(start_date,end_date,save_dir)

    # Extraire les données des pages locales
    all_matches_df = extract_data_from_local_pages(save_dir)
    
    # Filtrer les matchs par date si une période est fournie
    if start_period and end_period:
        all_matches_df['Date'] = pd.to_datetime(all_matches_df['Date'])
        all_matches_df = all_matches_df[(all_matches_df['Date'] >= start_period) & (all_matches_df['Date'] <= end_period)]

    # Chargement et nettoyage des cotes de paris
    file_path = "nba_odds.html"
    odds_df = scrape_data_from_html(file_path, end_period)
    
    # Vérifier les premières lignes pour détecter des erreurs dans la colonne Date
    #print("Debug : \n")
    #print("Premieres lignes de Nba_Odds : \n", odds_df.head())
    #print("\n")

    # Supprimer la première ligne (si elle contient des erreurs comme 'Date' en valeur)
    if odds_df.iloc[0, 0] == 'Date':
        odds_df = odds_df.iloc[1:]

    # Convertir la colonne Date en format datetime
    try:
        odds_df['Date'] = pd.to_datetime(odds_df['Date'], format='%Y-%m-%d', errors='coerce')
    except Exception as e:
        print(f"Erreur lors de la conversion des dates: {e}")
        return

    # Supprimer les lignes où la conversion de la date a échoué
    odds_df = odds_df.dropna(subset=['Date'])

    # Filtrer par période
    odds_df = odds_df[(odds_df['Date'] >= start_period) & (odds_df['Date'] <= end_period)]

    # Initialiser les moyennes globales pour l'ensemble des matchs
    league_avg_OEff = all_matches_df['Points_Scored'].sum() / all_matches_df['Possessions'].sum() * 100
    league_avg_DEff = all_matches_df['Points_Allowed'].sum() / all_matches_df['Possessions'].sum() * 100

    # Calcul des efficacités et des efficacités ajustées cumulatives
    cumulative_stats = []

    for index, match in all_matches_df.iterrows():
        team = match['Team']
        opponent = match['Opponent']
        
        # Calcul des efficacités du match
        match['OEff'] = match['Points_Scored'] / (match['Possessions'] / 100)
        match['DEff'] = match['Points_Allowed'] / (match['Possessions'] / 100)
        
        # Efficacités ajustées
        if len(cumulative_stats) == 0:
            # Initialiser les efficacités ajustées au début de la saison
            match['OEffAdj'] = match['OEff']
            match['DEffAdj'] = match['DEff']
        else:
            prev_stats = cumulative_stats[-1]  # Derniers calculs
            match['OEffAdj'] = (match['OEff'] / prev_stats['DEffAdj']) * league_avg_OEff
            match['DEffAdj'] = (match['DEff'] / prev_stats['OEffAdj']) * league_avg_DEff

        cumulative_stats.append(match)

    # Convertir en DataFrame
    adjusted_stats_df = pd.DataFrame(cumulative_stats)

    # Sauvegarde des statistiques ajustées par date
    adjusted_stats_df[['Date', 'Team', 'OEffAdj', 'DEffAdj']].to_csv('dataset_OEff_DEff.txt', sep='\t', header=False, index=False)

    #print("Debug OEffAdj,DEffAdj :\n")
    #print("Efficacités offensives et defensives par équipes, après chaque match (les 10 dernieres):")
    #print(adjusted_stats_df[['Date', 'Team', 'OEffAdj', 'DEffAdj']].tail(10))
    #print("\n")

    # On execute la simulation
    results_df = simulate_betting_with_data(odds_df)

    print("Simulation de paris sportifs sur les données: \n")
    print("DataFrame des resultats:\n", results_df)
    print("\n")

    # Charger les données d'efficacité et les fusionner avec odds_df
    eff_data = pd.read_csv('dataset_OEff_DEff.txt', sep='\t', header=None, names=['Date', 'Team', 'OEffAdj', 'DEffAdj'])
    eff_data = eff_data.sort_values(by=['Date'])
    new_df = odds_df.merge(eff_data, how='left', on='Team')

    # Gérer les valeurs NaN
    new_df = new_df.dropna(subset=['OEffAdj', 'DEffAdj'])

    #print("Debug eff_data :\n")
    #print("eff_data :\n", eff_data)
    #print("\n")

    #print("Debug odds_df :\n")
    #print("odds_df :\n", odds_df)
    #print("\n")

    #print("Debug new_df :\n")
    #print("new_df :\n", new_df)
    #print("\n")

    # On utilise les mêmes arguments que pour l'entraînement du modèle
    X_odds = new_df[['OEffAdj', 'DEffAdj']]
    X_odds_selected = sfm.transform(X_odds)

    # On predit la possibilité de gagner pour chaque ligne dans odds_df
    new_df['Predicted_Prob'] = model.predict_proba(X_odds_selected)[:, 1]

    # On organise par equipe et on calcule la probabilité moyenne de gagner
    team_win_prob = new_df.groupby('Team')['Predicted_Prob'].mean().reset_index()

    # Exemple supplémentaire : on cherche les 10 équipes les plus susceptibles de gagner
    top_10_teams = team_win_prob.nlargest(10, 'Predicted_Prob')

    print("Exemple supplémentaire d'utilisation :\n")
    print("Top 10 des equipes les plus susceptibles de gagner la saison:")
    print(top_10_teams)

if __name__ == "__main__":
    # Définir une période pour le calcul des probabilités
    start_period = datetime(2022, 10, 18)
    end_period = datetime(2022, 11, 1)
    main(start_period, end_period)
