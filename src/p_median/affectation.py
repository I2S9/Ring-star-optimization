# Affectation des points aux stations pour le problème p-médian
# Chaque point non station est affecté à la station la plus proche

from src.distances import creer_matrice_distances, obtenir_distance


def affecter_points_aux_stations(points, stations, distances):
    """
    Affecte chaque point non station à la station la plus proche.
    
    Cette fonction complète le problème p-médian en déterminant
    l'affectation optimale des points aux stations sélectionnées.
    Chaque point est affecté à exactement une station (la plus proche).
    
    Le lien avec le p-médian théorique :
    - Le problème p-médian consiste à sélectionner p stations
      et à affecter chaque point à sa station la plus proche
    - L'objectif est de minimiser la somme des distances
      d'affectation (coût total)
    - Cette fonction résout la partie affectation une fois
      les stations fixées
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        stations: Liste des identifiants des stations sélectionnées
        distances: Dictionnaire des distances créé par creer_matrice_distances
        
    Returns:
        Dictionnaire où affectations[id_point] = id_station
    """
    # Conversion en ensemble pour accès rapide
    stations_set = set(stations)
    
    # Dictionnaire des affectations
    affectations = {}
    
    # Pour chaque point
    for point in points:
        id_point = point[0]
        
        # Si le point est une station, il s'affecte à lui-même
        if id_point in stations_set:
            affectations[id_point] = id_point
        else:
            # Recherche de la station la plus proche
            station_plus_proche = None
            distance_minimale = float('inf')
            
            for id_station in stations:
                distance = obtenir_distance(distances, id_point, id_station)
                
                if distance < distance_minimale:
                    distance_minimale = distance
                    station_plus_proche = id_station
            
            # Affectation du point à la station la plus proche
            affectations[id_point] = station_plus_proche
    
    return affectations


def calculer_cout_affectation(points, stations, distances):
    """
    Calcule le coût total d'affectation pour une sélection de stations.
    
    Le coût est la somme des distances entre chaque point et sa station
    la plus proche. C'est l'objectif à minimiser dans le problème p-médian.
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        stations: Liste des identifiants des stations sélectionnées
        distances: Dictionnaire des distances créé par creer_matrice_distances
        
    Returns:
        Coût total d'affectation (somme des distances)
    """
    # Affectation des points aux stations
    affectations = affecter_points_aux_stations(points, stations, distances)
    
    # Calcul du coût total
    cout_total = 0.0
    
    for point in points:
        id_point = point[0]
        id_station = affectations[id_point]
        
        # Ajout de la distance d'affectation
        distance = obtenir_distance(distances, id_point, id_station)
        cout_total += distance
    
    return cout_total


def obtenir_affectations_et_cout(points, stations, distances):
    """
    Retourne à la fois les affectations et le coût total.
    
    Utile quand on a besoin des deux informations sans recalculer
    les affectations deux fois.
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        stations: Liste des identifiants des stations sélectionnées
        distances: Dictionnaire des distances créé par creer_matrice_distances
        
    Returns:
        Tuple (affectations, cout_total)
    """
    # Affectation des points aux stations
    affectations = affecter_points_aux_stations(points, stations, distances)
    
    # Calcul du coût total
    cout_total = 0.0
    
    for point in points:
        id_point = point[0]
        id_station = affectations[id_point]
        
        # Ajout de la distance d'affectation
        distance = obtenir_distance(distances, id_point, id_station)
        cout_total += distance
    
    return affectations, cout_total
