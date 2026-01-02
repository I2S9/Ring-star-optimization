# Heuristique aléatoire pour le problème p-médian
# Sélectionne p stations de manière aléatoire

import random


def selectionner_stations_aleatoire(points, p):
    """
    Sélectionne p stations de manière aléatoire.
    
    Cette méthode est très simple et rapide, mais elle ne garantit
    pas une bonne qualité de solution. Elle est utile comme point
    de départ pour d'autres méthodes ou pour comparer les performances.
    
    Avantages :
    - Très rapide (O(p))
    - Simple à implémenter
    
    Inconvénients :
    - Pas de garantie sur la qualité
    - Peut sélectionner des stations très proches
    - Ne prend pas en compte la répartition géographique
    
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
    
    # Extraction de tous les identifiants
    identifiants = [point[0] for point in points]
    
    # La station 1 est toujours incluse (contrainte du problème)
    stations_selectionnees = [1]
    
    # Si p = 1, on retourne juste la station 1
    if p == 1:
        return stations_selectionnees
    
    # Retrait de la station 1 de la liste des candidats
    identifiants_restants = [id_point for id_point in identifiants if id_point != 1]
    
    # Sélection aléatoire de (p-1) stations supplémentaires
    stations_supplementaires = random.sample(identifiants_restants, p - 1)
    
    # Ajout des stations supplémentaires
    stations_selectionnees.extend(stations_supplementaires)
    
    return stations_selectionnees
