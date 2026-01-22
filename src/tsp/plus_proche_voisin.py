# Algorithme du plus proche voisin pour le TSP
# Construit un cycle hamiltonien en choisissant toujours le voisin le plus proche

from src.calcul_distances import obtenir_distance


def construire_cycle_plus_proche_voisin(stations, distances):
    """
    Construit un cycle TSP en utilisant l'algorithme du plus proche voisin.
    
    L'algorithme commence à la station 1 et, à chaque étape, choisit
    la station non visitée la plus proche. À la fin, on retourne à
    la station de départ pour fermer le cycle.
    
    Limites connues de cette heuristique :
    - Ne garantit pas l'optimalité (peut être très mauvais dans certains cas)
    - Peut créer des croisements dans le cycle
    - Sensible à l'ordre de départ (mais ici on commence toujours à 1)
    - Complexité : O(n²) où n est le nombre de stations
    
    Avantages :
    - Très rapide à calculer
    - Simple à implémenter et comprendre
    - Donne souvent de bons résultats pour des instances petites à moyennes
    
    Args:
        stations: Liste des identifiants des stations à visiter
        distances: Dictionnaire des distances créé par creer_matrice_distances
        
    Returns:
        Liste ordonnée des stations formant le cycle (commence et finit à la station 1)
    """
    # Vérification que la liste n'est pas vide
    if len(stations) == 0:
        return []
    
    # Vérification que la station 1 est dans la liste
    if 1 not in stations:
        # Si la station 1 n'est pas dans la liste, on commence par la première station
        station_depart = stations[0]
    else:
        station_depart = 1
    
    # Initialisation
    cycle = [station_depart]
    stations_visitees = set([station_depart])
    station_courante = station_depart
    
    # Construction du cycle
    # On continue tant qu'il reste des stations non visitées
    while len(stations_visitees) < len(stations):
        station_plus_proche = None
        distance_minimale = float('inf')
        
        # Recherche de la station non visitée la plus proche
        for station in stations:
            if station not in stations_visitees:
                distance = obtenir_distance(distances, station_courante, station)
                
                if distance < distance_minimale:
                    distance_minimale = distance
                    station_plus_proche = station
        
        # Si on a trouvé une station, on l'ajoute au cycle
        if station_plus_proche is not None:
            cycle.append(station_plus_proche)
            stations_visitees.add(station_plus_proche)
            station_courante = station_plus_proche
    
    # Fermeture du cycle : retour à la station de départ
    cycle.append(station_depart)
    
    return cycle


def calculer_longueur_cycle(cycle, distances):
    """
    Calcule la longueur totale d'un cycle TSP.
    
    Args:
        cycle: Liste ordonnée des stations formant le cycle
        distances: Dictionnaire des distances créé par creer_matrice_distances
        
    Returns:
        Longueur totale du cycle
    """
    if len(cycle) <= 1:
        return 0.0
    
    longueur_totale = 0.0
    
    # Somme des distances entre stations consécutives
    for i in range(len(cycle) - 1):
        station_actuelle = cycle[i]
        station_suivante = cycle[i + 1]
        distance = obtenir_distance(distances, station_actuelle, station_suivante)
        longueur_totale += distance
    
    return longueur_totale
