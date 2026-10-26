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
)  # Création d'un dataframe contnenant les prix moyens par départements

prix_dep.to_csv(
    "prix_carburant.csv"
)  # Extraction du dataframe dans un fichier csv pour alimenter PowerBI
