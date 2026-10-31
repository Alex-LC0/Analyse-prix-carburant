# Mise en place de l'environnement de travail :
import pandas as pd
import requests
import json
from datetime import date

URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records"
all_results = []
offset = 0
limit = 100
today = date.today().isoformat()  # Date s'actualisant automatiquement chaque jour

params = {
    "offset": offset,
    "limit": limit,
    "select": "id,gazole_prix, gazole_maj, ville, code_departement",
    "order_by": "gazole_maj DESC, id ASC",
    "where": f"gazole_maj >= date'{today}' AND gazole_prix is not null",
}

while True:  # Boucle d'extraction des données de l'API des prix du pétrole
    params["offset"] = (
        offset  # Mise à jour de la valeur de l'offset à chaque tour de la boucle
    )
    response = requests.get(URL, params=params)  # Récupération des données de l'API
    response = response.json()  # Transformation de la réponse en Json lisible
    data = response["results"]  # Extraction des résultats du Json

    all_results.extend(
        data
    )  # Stockage des données extraites dans une liste précédemment créée
    print(len(all_results))  # Affichage afin de voir si le script tourne correctement

    if not data:  # Stop de la boucle seulement s'il n'y a plus de donnée à extraire
        break
    offset += (
        limit  # Augmentation du offset par la limite pour capter l'ensemble des données
    )

gazole = pd.DataFrame(all_results)  # Création d'un dataframe pandas
gazole["gazole_maj"] = (
    gazole["gazole_maj"].str.split("T").str[0]
)  # Normalisation de la date sans l'heure
prix_dep = gazole.groupby(
    ["code_departement", "gazole_maj"]
).gazole_prix.mean()  # Calcul des moyennnes des prix du gazole
prix_dep = pd.DataFrame(
    prix_dep
)  # Création d'un dataframe contenant les prix moyens par départements
prix_commune = (
    gazole.groupby(["code_departement", "ville", "gazole_maj"])
    .gazole_prix.mean()
    .reset_index()
)  # Création d'un regroupement des prix moyens par communes dans les départements
prix_commune = pd.DataFrame(
    prix_commune
)  # Création du dataframe contenant les prix du carburant par commune

date_today = gazole[
    "gazole_maj"
].unique()  # Récupération des données de la date du jour
date_today = pd.DataFrame(
    date_today, columns=["gazole_maj"]
)  # Création du dataframe de la date

prix_dep = prix_dep.reset_index()  # Reset des index pour créer un historique de données

try:  # Pour le premier lancement du script sur la machine
    historique = pd.read_csv("prix_carburant.csv")  # Ouverture de l'historique
    maj_data = pd.concat(
        [historique, prix_dep]
    )  # Fusion des anciennes et nouvelles données
    maj_data.to_csv("prix_carburant.csv", index=False)  # Création du fichier mis à jour
except FileNotFoundError as e:  # Cadre où le fichier historique n'existe pas encore
    prix_dep.to_csv("prix_carburant.csv", index=False)  # Création des données

try:
    historique_commune = pd.read_csv(
        "prix_carburant_commune.csv"
    )  # Ouverture de l'historique
    maj_data_commune = pd.concat(
        [historique_commune, prix_commune]
    )  # Fusion des anciennes et nouvelles données
    maj_data_commune.to_csv(
        "prix_carburant_commune.csv", index=False
    )  # Création du fichier mis à jour
except FileNotFoundError as e:  # Cadre où le fichier historique n'existe pas encore
    prix_commune.to_csv(
        "prix_carburant_commune.csv", index=False
    )  # Création des données

try:  # Création / Mise à jour de la table calendrier
    calendrier = pd.read_csv("calendrier.csv")  # Ouverture de l'historique des dates
    maj_calendrier = pd.concat(
        [calendrier, date_today]
    )  # Rajout de la date du jour dans l'historique
    maj_calendrier.to_csv("calendrier.csv")
except FileNotFoundError as e:
    date_today.to_csv("calendrier.csv")  # Création des données non existantes
