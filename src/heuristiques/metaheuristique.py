# Métaheuristique (recuit simulé) pour améliorer la solution anneau-étoile
# Utilise des voisinages simples : échange station/non-station et 2-opt

import random
import math
from src.calcul_distances import creer_matrice_distances
from src.p_median.affectation import affecter_points_aux_stations, calculer_cout_affectation
from src.tsp.plus_proche_voisin import construire_cycle_plus_proche_voisin, calculer_longueur_cycle
from src.tsp.two_opt import ameliorer_cycle_2opt


def recalculer_solution(points, stations, distances, alpha=0.5):
    """
    Recalcule une solution complète à partir d'une liste de stations.
    
    Utile pour la métaheuristique qui modifie les stations.
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        stations: Liste des identifiants des stations sélectionnées
        distances: Dictionnaire des distances
        alpha: Coefficient de pondération
        
    Returns:
        Dictionnaire de solution complète
    """
    # Construction du cycle
    cycle = construire_cycle_plus_proche_voisin(stations, distances)
    cycle = ameliorer_cycle_2opt(cycle, distances)
    
    # Affectation des points
    affectations = affecter_points_aux_stations(points, stations, distances)
    
    # Calcul des coûts
    longueur_cycle = calculer_longueur_cycle(cycle, distances)
    cout_affectation = calculer_cout_affectation(points, stations, distances)
    cout_total = alpha * longueur_cycle + (1 - alpha) * cout_affectation
    
    solution = {
        'stations': stations.copy(),
        'cycle': cycle,
        'affectations': affectations,
        'longueur_cycle': longueur_cycle,
        'cout_affectation': cout_affectation,
        'cout_total': cout_total
    }
    
    return solution


def generer_voisin_echange_station(points, stations_actuelles):
    """
    Génère un voisin en échangeant une station avec un point non station.
    
    Voisinage simple : on retire une station (sauf la station 1) et on
    la remplace par un point non station choisi aléatoirement.
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        stations_actuelles: Liste des identifiants des stations actuelles
        
    Returns:
        Nouvelle liste de stations (voisin)
    """
    # Création d'une copie
    nouvelles_stations = stations_actuelles.copy()
    
    # Extraction de tous les identifiants
    tous_ids = [point[0] for point in points]
    stations_set = set(stations_actuelles)
    
    # Liste des points non stations
    points_non_stations = [id_point for id_point in tous_ids if id_point not in stations_set]
    
    # Si on n'a pas de points non stations, on ne peut pas échanger
    if len(points_non_stations) == 0:
        return nouvelles_stations
    
    # Sélection aléatoire d'une station à retirer (sauf la station 1)
    stations_retirables = [s for s in nouvelles_stations if s != 1]
    if len(stations_retirables) == 0:
        # Si seule la station 1 reste, on ne peut pas échanger
        return nouvelles_stations
    
    station_a_retirer = random.choice(stations_retirables)
    
    # Sélection aléatoire d'un point non station à ajouter
    point_a_ajouter = random.choice(points_non_stations)
    
    # Échange
    nouvelles_stations.remove(station_a_retirer)
    nouvelles_stations.append(point_a_ajouter)
    
    return nouvelles_stations


def recuit_simule(points, solution_initiale, distances, alpha=0.5, 
                  temperature_initiale=1000.0, temperature_finale=0.1, 
                  facteur_refroidissement=0.95, iterations_par_temperature=10):
    """
    Améliore une solution avec le recuit simulé.
    
    Le recuit simulé est une métaheuristique qui permet d'échapper
    aux optima locaux en acceptant parfois des solutions pires.
    
    Paramètres :
    - temperature_initiale : Température de départ (contrôle l'acceptation)
    - temperature_finale : Température d'arrêt
    - facteur_refroidissement : Facteur de réduction de température (0 < facteur < 1)
    - iterations_par_temperature : Nombre d'itérations à chaque température
    
    Fonctionnement :
    1. On part d'une solution initiale
    2. À chaque itération, on génère un voisin
    3. Si le voisin est meilleur, on l'accepte
    4. Si le voisin est pire, on l'accepte avec probabilité exp(-delta/T)
    5. On réduit progressivement la température
    6. On s'arrête quand la température est trop basse
    
    Voisinages utilisés :
    - Échange station / non station : modifie la sélection des stations
    - 2-opt : améliore le cycle (appliqué à chaque recalcul)
    
    Limites :
    - Temps de calcul : dépend du nombre d'itérations
      Complexité approximative : O(iterations * (n + p²))
      où n = nombre de points, p = nombre de stations
    - Ne garantit pas l'optimalité
    - Sensible au réglage des paramètres
    - Peut être lent pour de grandes instances
    
    Avantages :
    - Peut échapper aux optima locaux
    - Améliore souvent significativement la solution initiale
    - Simple à implémenter
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        solution_initiale: Dictionnaire de solution initiale
        distances: Dictionnaire des distances
        alpha: Coefficient de pondération
        temperature_initiale: Température de départ
        temperature_finale: Température d'arrêt
        facteur_refroidissement: Facteur de réduction (0 < facteur < 1)
        iterations_par_temperature: Nombre d'itérations par température
        
    Returns:
        Meilleure solution trouvée
    """
    # Solution courante et meilleure solution
    solution_courante = solution_initiale.copy()
    solution_courante['stations'] = solution_initiale['stations'].copy()
    meilleure_solution = solution_courante.copy()
    meilleure_solution['stations'] = solution_initiale['stations'].copy()
    
    meilleur_cout = solution_initiale['cout_total']
    temperature = temperature_initiale
    
    # Compteurs pour le suivi
    nombre_acceptations = 0
    nombre_rejets = 0
    iteration = 0
    
    # Boucle principale du recuit simulé
    while temperature > temperature_finale:
        # Itérations à température constante
        for _ in range(iterations_par_temperature):
            iteration += 1
            
            # Génération d'un voisin (échange station / non station)
            nouvelles_stations = generer_voisin_echange_station(points, solution_courante['stations'])
            
            # Si le voisin est identique, on passe
            if nouvelles_stations == solution_courante['stations']:
                continue
            
            # Recalcul de la solution avec les nouvelles stations
            nouvelle_solution = recalculer_solution(points, nouvelles_stations, distances, alpha)
            
            # Calcul de la différence de coût
            delta = nouvelle_solution['cout_total'] - solution_courante['cout_total']
            
            # Décision d'acceptation
            accepter = False
            
            if delta < 0:
                # Solution meilleure : on accepte toujours
                accepter = True
                nombre_acceptations += 1
            else:
                # Solution pire : on accepte avec probabilité exp(-delta/T)
                probabilite = math.exp(-delta / temperature)
                if random.random() < probabilite:
                    accepter = True
                    nombre_acceptations += 1
                else:
                    nombre_rejets += 1
            
            # Mise à jour de la solution courante
            if accepter:
                solution_courante = nouvelle_solution.copy()
                solution_courante['stations'] = nouvelle_solution['stations'].copy()
                
                # Mise à jour de la meilleure solution
                if nouvelle_solution['cout_total'] < meilleur_cout:
                    meilleure_solution = nouvelle_solution.copy()
                    meilleure_solution['stations'] = nouvelle_solution['stations'].copy()
                    meilleur_cout = nouvelle_solution['cout_total']
        
        # Refroidissement
        temperature *= facteur_refroidissement
    
    return meilleure_solution
