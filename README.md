# Analyse-prix-carburant
Création d'un script de récupération et d'analyse des prix moyens du pétrole en France en fonction des départements à partir des données publiée par le Ministère de l'économie


## Sommaire

- [Contexte](#contexte)
- [Méthodologie](#méthodologie)
- [Stack technique](#stack-technique)
- [Structure du repo](#structure-du-repo)
- [Lancer le projet](#lancer-le-projet)
- [Limites et pistes futures](#limites-et-pistes-futures)
- [Auteur](#auteur)

## Contexte

Depuis le début de la guerre entre les États-Unis et l’Iran, les prix du carburant ont connu une hausse sans précédent. La France n’est pas épargnée par ces hausses, qui peuvent, en fonction des secteurs géographiques, avoir des conséquences très différentes.

Il est alors essentiel pour les consommateurs, les vendeurs et l’État de comprendre la répartition des prix du pétrole sur le territoire national. Ainsi, à l’aide des données publiques publiées par le ministère de l’économie, j’ai mis en place un script permettant, en quelques clics, de visualiser rapidement où les prix sont les plus forts, afin d'identifier les territoires les plus impactés par cette hausse.

L’objectif est donc de faciliter la compréhension de la répartition des prix du carburant sur le territoire français, à l'aide de données actuelles.

## Méthodologie

* Conception d’un script d’extraction des données quotidiennes des prix du carburant
* Nettoyage des données et stockage dans un fichier .csv
* Intégration des données dans un dashboard Power BI affichant les graphiques essentiels

## Stack technique

* Python
* pandas
* request
* Power BI

## Structure du repo

```bash
Prix-carburant/
├── main.py             # Script de récupération des prix du carburant
├── dashboard.pbix      # Dashboard d'affichage des données
├── requirements.txt    # Packages et bibliothèques Python nécessaires
└── README.md           # Documentation du projet
```

## Lancer le projet

### Prérequis

- Python 3.11
- Power BI Desktop

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-utilisateur>/Prix-carburant.git
cd Prix-carburant
```

### 2. Créer et activer un environnement virtuel (recommandé)

```bash
# Création
python -m venv venv

# Activation sous Windows
venv\Scripts\activate

# Activation sous macOS / Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Récupération et nettoyage des données

```bash
python main.py
```

Le script télécharge les prix du carburant publiés par le ministère de l'Économie, nettoie les données et génère les fichiers `prix_carburant.csv` , `prix_carburant_commune.csv`, `prix_carburant_sp95.csv`, `prix_carburant_commune_sp95.csv`, `calendrier.csv` à la racine du projet.

### 2. Ouverture du dashboard

1. Ouvrir `dashboard.pbix` avec Power BI Desktop.
2. Si le chemin de la source n'est pas reconnu, aller dans **Accueil > Transformer les données > Paramètres de la source de données > Modifier la source**, puis sélectionner `prix_carburant.csv`.
3. Cliquer sur **Actualiser** pour charger les données.

## Mise à jour quotidienne

Les données ne sont pas actualisées automatiquement. Pour obtenir les prix du jour :

1. Relancer `python main.py`.
2. Cliquer sur **Actualiser** dans Power BI.

## Limites et pistes futures

* Le fichier ne s’actualise pas automatiquement en arrière-plan, il est donc nécessaire de relancer le script chaque jour, ce qui est une piste d’amélioration
* Le croisement entre les données de revenus mensuelles moyens par départements et les données du carburants peuvent être une piste d'analyse plus fine de ces données (identification des territoires les plus impactés)
* Le croisement entre les données du prix du baril de pétrole ainsi que les données nationales peuvent être une autre piste d'analyse fine de ces données
* L'ajout d'un outil d'analyse des station en 'pénurie' pour juger si la baisse des prix est réelles ou dûe à la chute de l'effectif


## Auteur

Alexis LE CALVEZ
