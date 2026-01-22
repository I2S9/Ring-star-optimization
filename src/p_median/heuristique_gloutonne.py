# Heuristique gloutonne pour le problème p-médian
# Utilise une grille pour répartir les stations de manière géographique

import math
from src.calcul_distances import distance_euclidienne


def selectionner_stations_grille(points, p):
    """
    Sélectionne p stations en utilisant une grille et les centres des rectangles.
    
    Cette méthode divise l'espace en une grille et sélectionne le point
    le plus proche du centre de chaque rectangle. C'est une approche
    géographique qui tente de répartir les stations de manière uniforme.
    
    Avantages :
    - Répartition géographique plus équilibrée que l'aléatoire
    - Rapide à calculer
    - Simple à comprendre
    
    Inconvénients :
    - Ne garantit pas l'optimalité
    - Peut ignorer des zones denses importantes
    - La grille peut ne pas correspondre à la distribution réelle des points
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        p: Nombre de stations à sélectionner
        
    Returns:
        Liste des identifiants des stations sélectionnées
    """
    # Vérification que p est valide
    if p <= 0:
        return []
    
    if p > len(points):
        # Si p est plus grand que le nombre de points, on prend tous les points
        return [point[0] for point in points]
    
    # La station 1 est toujours incluse (contrainte du problème)
    stations_selectionnees = [1]
    
    # Si p = 1, on retourne juste la station 1
    if p == 1:
        return stations_selectionnees
    
    # Calcul des bornes de l'espace (min et max en x et y)
    coordonnees_x = [point[1] for point in points]
    coordonnees_y = [point[2] for point in points]
    
    x_min = min(coordonnees_x)
    x_max = max(coordonnees_x)
    y_min = min(coordonnees_y)
    y_max = max(coordonnees_y)
    
    # Calcul de la taille de la grille
    # On veut approximativement p-1 rectangles (car la station 1 est déjà incluse)
    nombre_stations_restantes = p - 1
    
    # Calcul du nombre de lignes et colonnes pour la grille
    # On essaie de créer une grille à peu près carrée
    nombre_colonnes = math.ceil(math.sqrt(nombre_stations_restantes))
    nombre_lignes = math.ceil(nombre_stations_restantes / nombre_colonnes)
    
    # Calcul de la taille de chaque cellule
    largeur_cellule = (x_max - x_min) / nombre_colonnes
    hauteur_cellule = (y_max - y_min) / nombre_lignes
    
    # Création des centres des rectangles de la grille
    centres_grille = []
    for i in range(nombre_lignes):
        for j in range(nombre_colonnes):
            # Calcul du centre du rectangle (i, j)
            centre_x = x_min + (j + 0.5) * largeur_cellule
            centre_y = y_min + (i + 0.5) * hauteur_cellule
            centres_grille.append((centre_x, centre_y))
    
    # Limitation au nombre de stations restantes
    centres_grille = centres_grille[:nombre_stations_restantes]
    
    # Pour chaque centre de grille, trouver le point le plus proche
    identifiants_deja_selectionnes = set([1])
    
    for centre_x, centre_y in centres_grille:
        point_centre = (0, centre_x, centre_y)  # ID fictif pour le calcul
        
        meilleur_point = None
        meilleure_distance = float('inf')
        
        # Recherche du point le plus proche du centre
        for point in points:
            id_point = point[0]
            
            # On ignore les points déjà sélectionnés
            if id_point in identifiants_deja_selectionnes:
                continue
            
            # Calcul de la distance au centre
            distance = distance_euclidienne(point_centre, point)
            
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleur_point = id_point
        
        # Ajout du meilleur point trouvé
        if meilleur_point is not None:
            stations_selectionnees.append(meilleur_point)
            identifiants_deja_selectionnes.add(meilleur_point)
    
    return stations_selectionnees
