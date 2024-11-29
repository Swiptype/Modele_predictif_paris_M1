# betting_simulation.py

import pandas as pd

# Simulations de paris sportifs
def simulate_betting_with_data(odds_df, initial_bankroll=1000, base_bet_amount=10):
    bankroll = initial_bankroll
    results = []

    for index, row in odds_df.iterrows():
        team = row["Team"]
        ml_odds = row["ML"]
        final_score = row["Final"]
        vh = row["VH"]

        if ml_odds == '' or final_score == '' or not ml_odds.replace('.', '', 1).replace('-', '', 1).isdigit():
            continue  # On passe s'il nous manque une valeur parmis ML ou Score Final

        ml_odds = float(ml_odds)
        final_score = int(final_score)

        # Convertir Moneyline en decimal
        if ml_odds > 0:
            decimal_odds = 1 + ml_odds / 100
        else:
            decimal_odds = 1 - 100 / ml_odds

        # On fait du pari dynamique en fonction des cotes
        # Si les cotes sont hautes, on reduit le montant du pari, sinon on l'augmente
        if decimal_odds >= 2.5:
            bet_amount = base_bet_amount * 0.5
        elif decimal_odds <= 1.5:
            bet_amount = base_bet_amount * 2
        else:
            bet_amount = base_bet_amount

        # Logique du pari : on part du principe que 'H' veut dire victoire en local et 'A' victoire ' à l'étranger '
        outcome = "win" if (vh == "H" and final_score > 100) or (vh == "A" and final_score < 100) else "lose"

        # Selon le resultat, on ajuste le bankroll (compte en banque)
        if outcome == "win":
            bankroll += bet_amount * (decimal_odds - 1)
        else:
            bankroll -= bet_amount

        results.append((team, ml_odds, decimal_odds, final_score, outcome, bankroll))

    # Creation d'un DataFrame pour les resultats
    results_df = pd.DataFrame(results, columns=["Team", "ML_Odds", "Decimal_Odds", "Final_Score", "Outcome", "Bankroll"])
    return results_df