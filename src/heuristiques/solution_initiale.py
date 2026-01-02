# Construction d'une solution initiale pour le problème anneau-étoile
# Chaîne les méthodes p-médian et TSP pour produire une solution complète

from src.distances import creer_matrice_distances
from src.p_median.heuristique_aleatoire import selectionner_stations_aleatoire
from src.p_median.heuristique_gloutonne import selectionner_stations_grille
from src.p_median.affectation import affecter_points_aux_stations, calculer_cout_affectation
from src.tsp.plus_proche_voisin import construire_cycle_plus_proche_voisin, calculer_longueur_cycle
from src.tsp.two_opt import ameliorer_cycle_2opt


def construire_solution_initiale(points, p, methode_selection='grille', ameliorer_cycle=True, alpha=0.5):
    """
    Construit une solution complète pour le problème anneau-étoile.
    
    Cette fonction implémente une approche heuristique séquentielle :
    1. Sélection de p stations (problème p-médian)
    2. Construction d'un cycle entre ces stations (problème TSP)
    3. Amélioration du cycle avec 2-opt (optionnel)
    4. Affectation des points aux stations
    5. Calcul du coût total
    
    Justification de l'approche heuristique séquentielle :
    - Le problème anneau-étoile combine deux sous-problèmes NP-difficiles
    - Résoudre les deux simultanément serait très complexe
    - L'approche séquentielle est simple et donne de bons résultats
    - On résout d'abord le p-médian (sélection + affectation)
    - Puis on résout le TSP sur les stations sélectionnées
    - Cette décomposition permet d'utiliser des méthodes connues
    
    Avantages :
    - Simple à implémenter et comprendre
    - Rapide à calculer
    - Donne des solutions réalisables
    
    Inconvénients :
    - Ne garantit pas l'optimalité
    - Les deux sous-problèmes sont résolus indépendamment
    - Peut ignorer des solutions meilleures qui nécessitent
      de modifier à la fois les stations et le cycle
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        p: Nombre de stations à sélectionner
        methode_selection: 'aleatoire' ou 'grille' pour la sélection des stations
        ameliorer_cycle: Si True, applique 2-opt pour améliorer le cycle
        alpha: Coefficient de pondération (0 <= alpha <= 1)
               coût_total = alpha * longueur_cycle + (1-alpha) * cout_affectation
        
    Returns:
        Dictionnaire contenant :
        - 'stations': Liste des identifiants des stations sélectionnées
        - 'cycle': Liste ordonnée des stations dans le cycle
        - 'affectations': Dictionnaire affectations[id_point] = id_station
        - 'longueur_cycle': Longueur totale du cycle
        - 'cout_affectation': Coût total d'affectation
        - 'cout_total': Coût total pondéré de la solution
    """
    # Création de la matrice des distances
    distances = creer_matrice_distances(points)
    
    # Étape 1 : Sélection de p stations (p-médian)
    if methode_selection == 'aleatoire':
        stations = selectionner_stations_aleatoire(points, p)
    elif methode_selection == 'grille':
        stations = selectionner_stations_grille(points, p)
    else:
        # Par défaut, on utilise la grille
        stations = selectionner_stations_grille(points, p)
    
    # Étape 2 : Construction d'un cycle entre les stations (TSP)
    cycle = construire_cycle_plus_proche_voisin(stations, distances)
    
    # Étape 3 : Amélioration du cycle avec 2-opt (optionnel)
    if ameliorer_cycle:
        cycle = ameliorer_cycle_2opt(cycle, distances)
    
    # Étape 4 : Affectation des points aux stations
    affectations = affecter_points_aux_stations(points, stations, distances)
    
    # Étape 5 : Calcul des coûts
    longueur_cycle = calculer_longueur_cycle(cycle, distances)
    cout_affectation = calculer_cout_affectation(points, stations, distances)
    
    # Coût total pondéré
    cout_total = alpha * longueur_cycle + (1 - alpha) * cout_affectation
    
    # Construction de la solution complète
    solution = {
        'stations': stations,
        'cycle': cycle,
        'affectations': affectations,
        'longueur_cycle': longueur_cycle,
        'cout_affectation': cout_affectation,
        'cout_total': cout_total
    }
    
    return solution


def afficher_solution(solution):
    """
    Affiche les informations d'une solution.
    
    Args:
        solution: Dictionnaire de solution créé par construire_solution_initiale
    """
    print("=== Solution anneau-étoile ===")
    print(f"Nombre de stations : {len(solution['stations'])}")
    print(f"Stations sélectionnées : {solution['stations']}")
    print(f"Longueur du cycle : {solution['longueur_cycle']:.2f}")
    print(f"Coût d'affectation : {solution['cout_affectation']:.2f}")
    print(f"Coût total : {solution['cout_total']:.2f}")
    print(f"Cycle : {solution['cycle']}")
