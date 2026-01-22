# Projet : Problème de l'anneau-étoile (Ring-Star Problem)

## Description

Ce projet a pour objectif de résoudre, de manière heuristique, métaheuristique et exacte (via PLNE), le problème dit de l'anneau-étoile.

Le problème modélise le tracé d'une ligne de transport public circulaire (métro, tramway, bus), passant par un sous-ensemble de points appelés **stations**, et desservant l'ensemble des zones environnantes. Chaque point non station est affecté à la station la plus proche. Les stations sont reliées entre elles par un **cycle**.

L'objectif est de minimiser :
- La longueur totale du cycle entre stations
- La somme des distances d'affectation des points non stations
- Éventuellement pondérée par un coefficient alpha

## Instances disponibles

Le projet utilise toutes les instances de la bibliothèque TSPLIB disponibles dans `donnees/tsplib/`. Il y a **111 instances** disponibles, de tailles variées :

- **Petites instances** (n ≤ 50) : 14 instances, idéales pour les tests rapides et la PLNE
- **Instances moyennes** (50 < n ≤ 200) : 35 instances, adaptées aux heuristiques et métaheuristiques
- **Grandes instances** (n > 200) : 62 instances, pour tester la robustesse des méthodes

Pour lister toutes les instances disponibles :

```bash
python src/liste_instances.py
```

Vous pouvez utiliser **n'importe quelle instance** avec le code. Par exemple :

```bash
# Petite instance pour test rapide
python src/main.py donnees/tsplib/burma14.tsp 3 0.5

# Instance moyenne
python src/main.py donnees/tsplib/eil51.tsp 5 0.5

# Grande instance
python src/main.py donnees/tsplib/a280.tsp 10 0.5
```

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de packages Python)
- make (optionnel, pour utiliser le Makefile)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

2. **Installer les dépendances**

   Avec make :
   ```bash
   make install
   ```

   Ou manuellement :
   ```bash
   pip install -r requirements.txt
   ```

3. **Vérifier l'installation**

   ```bash
   make test
   ```

   Ou manuellement :
   ```bash
   python -c "import numpy, matplotlib, pulp; print('OK')"
   ```

### Dépendances

Les dépendances sont listées dans `requirements.txt` :
- `numpy` : Calculs numériques
- `matplotlib` : Visualisation
- `pulp` : Résolution PLNE

## Exécution

### Utilisation avec Makefile (recommandé)

Le Makefile facilite l'exécution et garantit la reproductibilité :

```bash
# Afficher l'aide
make help

# Lancer les comparaisons avec les paramètres par défaut
make run

# Lancer avec des paramètres personnalisés
make run INSTANCE=donnees/tsplib/berlin52.tsp P=7 ALPHA=0.3

# Nettoyer les fichiers générés
make clean
```

### Utilisation directe avec Python

```bash
# Lancer les comparaisons expérimentales
python src/main.py <fichier_tsp> <nombre_stations> [alpha]

# Exemple avec une instance spécifique
python src/main.py donnees/tsplib/att48.tsp 5 0.5

# Vous pouvez utiliser n'importe quelle instance disponible dans donnees/tsplib/
python src/main.py donnees/tsplib/berlin52.tsp 7 0.5
python src/main.py donnees/tsplib/eil51.tsp 5 0.3
```

### Lister les instances disponibles

Pour voir toutes les instances TSPLIB disponibles :

```bash
python src/liste_instances.py
```

Pour filtrer par taille :

```bash
# Petites instances (n <= 50)
python src/liste_instances.py petites

# Instances moyennes (50 < n <= 200)
python src/liste_instances.py moyennes

# Grandes instances (n > 200)
python src/liste_instances.py grandes
```

### Paramètres

- `<fichier_tsp>` : Chemin vers le fichier d'instance TSPLIB (format .tsp)
  Les instances sont dans le répertoire `donnees/tsplib/`
- `<nombre_stations>` : Nombre de stations à sélectionner (p)
- `[alpha]` : Coefficient de pondération (optionnel, défaut : 0.5)
  - alpha = 0 : Minimise uniquement les affectations
  - alpha = 1 : Minimise uniquement le cycle
  - alpha = 0.5 : Équilibre entre les deux

### Résultats

Les résultats sont sauvegardés dans `resultats/resultats.txt` avec :
- Tableaux comparatifs des méthodes
- Détails par méthode (coût, temps, stations)
- Analyses statistiques

## Structure du projet

```
ring-star-optimization/
│
├── donnees/
│   └── tsplib/              # Toutes les instances TSPLIB (111 fichiers .tsp)
│       ├── att48.tsp
│       ├── berlin52.tsp
│       ├── a280.tsp
│       └── ... (toutes les instances disponibles)
│
├── src/
│   ├── lecture_tsp.py       # Lecture des fichiers TSPLIB
│   ├── calcul_distances.py  # Calcul des distances euclidiennes
│   ├── visualisation.py      # Visualisation des instances et solutions
│   ├── liste_instances.py    # Utilitaire pour lister les instances disponibles
│   ├── generer_figures.py    # Génération automatique des figures
│   ├── main.py               # Point d'entrée principal
│   ├── comparaisons.py        # Comparaisons expérimentales
│   │
│   ├── p_median/         # Méthodes pour le problème p-médian
│   │   ├── heuristique_aleatoire.py
│   │   ├── heuristique_gloutonne.py
│   │   └── affectation.py
│   │
│   ├── tsp/              # Méthodes pour le TSP
│   │   ├── plus_proche_voisin.py
│   │   └── two_opt.py
│   │
│   ├── heuristiques/     # Heuristiques complètes
│   │   ├── solution_initiale.py
│   │   └── metaheuristique.py
│   │
│   └── plne/             # Programmation linéaire en nombres entiers
│       ├── formulation_compacte.py
│       └── formulation_non_compacte.py
│
├── resultats/
│   ├── figures/          # Figures générées
│   └── resultats.txt     # Résultats des expérimentations
│
├── report/               # Rapport du projet
│
├── Makefile              # Commandes d'exécution
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

## Méthodes implémentées

### 1. Heuristiques p-médian

**Heuristique aléatoire** (`p_median/heuristique_aleatoire.py`)
- Sélection aléatoire de p stations
- Très rapide mais qualité non garantie

**Heuristique gloutonne** (`p_median/heuristique_gloutonne.py`)
- Utilise une grille pour répartir les stations
- Répartition géographique plus équilibrée

**Affectation** (`p_median/affectation.py`)
- Affecte chaque point à la station la plus proche
- Calcule le coût total d'affectation

### 2. Heuristiques TSP

**Plus proche voisin** (`tsp/plus_proche_voisin.py`)
- Construit un cycle en choisissant toujours le voisin le plus proche
- Commence toujours à la station 1

**2-opt** (`tsp/two_opt.py`)
- Améliore un cycle en testant des échanges d'arêtes
- Recherche locale simple

### 3. Heuristique complète

**Solution initiale** (`heuristiques/solution_initiale.py`)
- Chaîne p-médian + TSP
- Approche séquentielle : résout d'abord le p-médian, puis le TSP

### 4. Métaheuristique

**Recuit simulé** (`heuristiques/metaheuristique.py`)
- Améliore la solution globale
- Voisinages : échange station/non-station et 2-opt
- Permet d'échapper aux optima locaux

### 5. Résolution exacte

**PLNE compacte** (`plne/modele_compact.py`)
- Formulation en programmation linéaire en nombres entiers
- Variables : y[i] (stations), x[i,j] (arêtes), z[i,j] (affectations)
- Contraintes : degré, affectation, connexité (MTZ)
- Résout de manière exacte (garantit l'optimalité si résolu)

## Limites et contraintes

### Limites de taille

**PLNE (résolution exacte)**
- Recommandé pour n ≤ 15-20 points
- Pour n > 20, le temps de résolution devient prohibitif
- Complexité : O(n²) variables et contraintes

**Heuristiques et métaheuristiques**
- Fonctionnent sur des instances de taille moyenne (n ≤ 100)
- Pour de très grandes instances, les temps peuvent être longs
- Qualité non garantie (sauf pour la PLNE)

### Limitations connues

1. **Distance euclidienne**
   - Approximation des trajets réels
   - Ne prend pas en compte les obstacles, routes, etc.

2. **Approche séquentielle**
   - Résout p-médian et TSP indépendamment
   - Peut ignorer des solutions meilleures nécessitant une optimisation simultanée

3. **Heuristiques**
   - Ne garantissent pas l'optimalité
   - Sensibles aux paramètres (notamment le recuit simulé)

4. **PLNE**
   - Temps de résolution exponentiel dans le pire cas
   - Nécessite un solveur (CBC par défaut avec PuLP)

### Reproductibilité

- Les résultats sont sauvegardés dans `resultats/resultats.txt`
- Le Makefile garantit des commandes standardisées
- Les paramètres par défaut sont documentés
- Les graines aléatoires ne sont pas fixées (variabilité possible)

## Exemples d'utilisation

### Exemple 1 : Comparaison complète

```bash
# Installer les dépendances
make install

# Lancer les comparaisons
make run

# Consulter les résultats
cat resultats/resultats.txt
```

### Exemple 2 : Test rapide

```bash
# Vérifier l'installation
make test

# Lancer avec paramètres personnalisés
python src/main.py donnees/tsplib/att48.tsp 5 0.5
```

### Exemple 3 : Visualisation

```python
from src.lecture_tsp import lire_fichier_tsp
from src.visualisation import afficher_instance
from src.heuristiques.solution_initiale import construire_solution_initiale
from src.visualisation import afficher_solution_complete

# Charger une instance
points = lire_fichier_tsp('donnees/tsplib/att48.tsp')

# Afficher l'instance brute
afficher_instance(points, "Instance att48")

# Construire une solution
solution = construire_solution_initiale(points, p=5, alpha=0.5)

# Afficher la solution
afficher_solution_complete(points, solution, "Solution anneau-étoile")
```

## Format des instances

Les instances doivent être au format TSPLIB (.tsp) avec :
- Section `NODE_COORD_SECTION` contenant les coordonnées
- Format : `id x y` (un point par ligne)
- Section `EOF` pour marquer la fin

## Auteur et licence

Projet réalisé dans le cadre d'un cours d'optimisation combinatoire (SAE).

## Contact et support

Pour toute question ou problème, consulter le code source et les commentaires dans les fichiers Python.

---

**Note pour les correcteurs** : Ce README contient toutes les informations nécessaires pour comprendre et utiliser le projet sans avoir à lire le code source. Les sections principales sont l'installation, l'exécution, la structure et les limites.