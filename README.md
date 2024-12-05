Architecture du projet : 

|--nba_season_pages‎‎

|       |--boxscore_2022_10_18.html

|       |--boxscore_2022_10_19.html‎

|       |--......‎

|       |--boxscore_2023_04_09.html‎

|--betting_simulation.py

|--datdaset_OEff_DEff.txt

|--download_pages.py

|--main.py

|--nba_odds.html

|--parse_stats.py‎

|--predict_model.py

|--scrap.py

Fonctionnement : 

Pour executer le programme, il est seulement necessaire de faire 'python3 main.py' dans un terminal au niveau du fichier main.py

Le dossier 'nba_season_pages' contient les pages web avec les resultat des matchs de NBA de la saison 2022-2023.

Le programme s'execute sur la periode du 18 octobre 2022 au 1 novembre 2022.

Modifications : 

Pour changer la date d'éxecution du modèle, il suffit de changer les variables 'start_period' et 'end_period' à la fin du fichier 'main.py'.

Pour obtenir les matchs sur une autre saison, il faut modifier les variables 'start_date','end_date' et 'save_dir' (si vous voulez enregistrer les pages dans un autre dossier) au debut de la fonction main et décommenter la ligne "download_season_pages(start_date,end_date,save_dir)"

Il est possible de modifier quelque peu la simulation de paris; dans 'betting_simulation.py', il est possible de modifier la somme d'argent de base(initial_bankroll), le montant de la mise de base(base_bet_amount) et les cotes(decimal_odds)
