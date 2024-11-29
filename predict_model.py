# predict_model.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données du fichier dataset_OEff_DEff.txt
data = pd.read_csv('dataset_OEff_DEff.txt', sep='\t', header=None)
data.columns = ['Date','Team','OEffAdj', 'DEffAdj']

# Les features seront OEffAdj et DEffAdj
X = data[['OEffAdj', 'DEffAdj']]

# On considère comme cible les équipes avec une OEffAdj supérieure à la médiane
median_OEffAdj = data['OEffAdj'].median()
y = (data['OEffAdj'] > median_OEffAdj).astype(int)

# Séparation des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# On s'adapte au modele LassoCV
lasso_cv = LassoCV(cv=5)
lasso_cv.fit(X_train, y_train)

# Selection des features
sfm = SelectFromModel(lasso_cv, prefit=True)
X_train_selected = sfm.transform(X_train)
X_test_selected = sfm.transform(X_test)

# On entraine le modele avec les features
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_selected, y_train)

print("shape : ",X_train_selected.shape)

# Evaluation du modele
y_pred = model.predict(X_test_selected)
print(classification_report(y_test, y_pred))

# Analyse des features
selected_feature_indices = np.where(sfm.get_support())[0]
selected_features = X.columns[selected_feature_indices]
coefficients = lasso_cv.coef_
print("Selected Features:", selected_features)
print("Feature Coefficients:", coefficients)

# On recupere les features qu'on souhaite du dataset de base
X_selected_features = X_train.iloc[:, selected_feature_indices]

# Creation d'un dataframe pour une meilleure visualisation
selected_features_df = pd.DataFrame(X_selected_features, columns=selected_features)

# Ajout de la variable pour la coloration
selected_features_df['target'] = y_train.values


# Executer le code en paramètre suivant permet d'afficher un nuage de points sur les valeurs recuperées/calculées
# Il ets en commentaire car ce n'est pas obligatoire pour la comprehension ou necessaire au bon fonctionnement du code

"""
# Si seulement une caractéristique est sélectionnée
if len(selected_features) == 1:
    # Graphique en barre de la seule caractéristique sélectionnée par classe cible
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='target', y=selected_features[0], data=selected_features_df, palette='viridis')
    plt.xlabel('Classe cible')
    plt.ylabel(selected_features[0])
    plt.title(f'Boxplot de {selected_features[0]} par Classe cible')
    plt.show()
else:
    # Si deux caractéristiques ou plus ont été sélectionnées, afficher un nuage de points
    sns.scatterplot(x=selected_features[0], y=selected_features[1], hue='target', data=selected_features_df, palette='viridis')
    plt.xlabel(selected_features[0])
    plt.ylabel(selected_features[1])
    plt.title('Scatter Plot des Caractéristiques Sélectionnées - Dataset NBA')
    plt.show()

"""