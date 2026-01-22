# Fichier pour le calcul des distances
# Centralise le calcul des distances entre les points

import math


def distance_euclidienne(point1, point2):
    """
    Calcule la distance euclidienne entre deux points.
    
    La distance euclidienne est utilisée car elle est simple à calculer
    et adaptée aux problèmes de transport dans un plan. Cependant, c'est
    une approximation : dans la réalité, les trajets réels peuvent être
    plus longs (routes, obstacles, etc.). Pour un projet étudiant, cette
    approximation est suffisante.
    
    Args:
        point1: Tuple (id, x, y) du premier point
        point2: Tuple (id, x, y) du deuxième point
        
    Returns:
        Distance euclidienne entre les deux points
    """
    # Extraction des coordonnées
    x1 = point1[1]
    y1 = point1[2]
    x2 = point2[1]
    y2 = point2[2]
    
    # Calcul de la distance euclidienne : sqrt((x2-x1)² + (y2-y1)²)
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx * dx + dy * dy)
    
    return distance


def creer_matrice_distances(points):
    """
    Crée une matrice des distances entre tous les points.
    
    La matrice est stockée sous forme de dictionnaire pour faciliter
    l'accès : distances[(i, j)] donne la distance entre le point i et j.
    
    Args:
        points: Liste de tuples (id, x, y) représentant les points
        
    Returns:
        Dictionnaire où distances[(i, j)] = distance entre i et j
    """
    distances = {}
    nombre_points = len(points)
    
    # Calcul de la distance entre chaque paire de points
    for i in range(nombre_points):
        for j in range(nombre_points):
            point_i = points[i]
            point_j = points[j]
            
            # La distance d'un point à lui-même est 0
            if i == j:
                distances[(point_i[0], point_j[0])] = 0.0
            else:
                # Calcul de la distance euclidienne
                dist = distance_euclidienne(point_i, point_j)
                distances[(point_i[0], point_j[0])] = dist
    
    return distances


def obtenir_distance(distances, id_point1, id_point2):
    """
    Récupère la distance entre deux points à partir de la matrice.
    
    Args:
        distances: Dictionnaire des distances créé par creer_matrice_distances
        id_point1: Identifiant du premier point
        id_point2: Identifiant du deuxième point
        
    Returns:
        Distance entre les deux points
    """
    return distances[(id_point1, id_point2)]
