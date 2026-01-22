# Algorithme 2-opt pour améliorer un cycle TSP
# Recherche locale qui améliore un cycle en testant des échanges d'arêtes

from src.calcul_distances import obtenir_distance


def appliquer_2opt(cycle, i, j):
    """
    Applique un échange 2-opt au cycle.
    
    L'échange 2-opt consiste à :
    - Prendre deux arêtes (i, i+1) et (j, j+1) dans le cycle
    - Les remplacer par (i, j) et (i+1, j+1)
    - Cela inverse la section du cycle entre i+1 et j
    
    Args:
        cycle: Liste ordonnée des stations formant le cycle
        i: Indice de la première arête (0 <= i < j)
        j: Indice de la deuxième arête (i < j < len(cycle)-1)
        
    Returns:
        Nouveau cycle après l'échange 2-opt
    """
    # Création d'une copie du cycle
    nouveau_cycle = cycle.copy()
    
    # Inversion de la section entre i+1 et j
    # On inverse la sous-liste de i+1 à j (inclus)
    section_a_inverser = nouveau_cycle[i+1:j+1]
    section_a_inverser.reverse()
    nouveau_cycle[i+1:j+1] = section_a_inverser
    
    return nouveau_cycle


def calculer_gain_2opt(cycle, i, j, distances):
    """
    Calcule le gain (réduction de distance) d'un échange 2-opt.
    
    Le gain est positif si l'échange améliore le cycle (réduit la distance).
    Le gain est négatif si l'échange détériore le cycle.
    
    Args:
        cycle: Liste ordonnée des stations formant le cycle
        i: Indice de la première arête
        j: Indice de la deuxième arête
        distances: Dictionnaire des distances
        
    Returns:
        Gain de l'échange (positif = amélioration)
    """
    # Stations concernées par les arêtes actuelles
    station_i = cycle[i]
    station_i_suivante = cycle[i + 1]
    station_j = cycle[j]
    station_j_suivante = cycle[j + 1]
    
    # Distance actuelle des deux arêtes
    distance_actuelle = (
        obtenir_distance(distances, station_i, station_i_suivante) +
        obtenir_distance(distances, station_j, station_j_suivante)
    )
    
    # Distance après l'échange 2-opt
    distance_nouvelle = (
        obtenir_distance(distances, station_i, station_j) +
        obtenir_distance(distances, station_i_suivante, station_j_suivante)
    )
    
    # Le gain est la différence (positif = amélioration)
    gain = distance_actuelle - distance_nouvelle
    
    return gain


def ameliorer_cycle_2opt(cycle, distances):
    """
    Améliore un cycle TSP en utilisant l'algorithme 2-opt.
    
    L'algorithme 2-opt est une recherche locale qui teste tous les
    échanges possibles de deux arêtes et applique ceux qui améliorent
    le cycle. On répète jusqu'à ce qu'aucune amélioration ne soit possible.
    
    Le voisinage 2-opt :
    - Pour chaque paire d'arêtes (i, i+1) et (j, j+1) dans le cycle
    - On teste l'échange : remplacer par (i, j) et (i+1, j+1)
    - Cela inverse la section du cycle entre i+1 et j
    - Si le gain est positif (réduction de distance), on applique l'échange
    
    Avantages :
    - Simple à implémenter
    - Améliore souvent significativement un cycle initial
    - Peut être appliqué à n'importe quel cycle
    
    Limites :
    - Ne garantit pas l'optimalité (peut rester bloqué dans un optimum local)
    - Complexité : O(n²) par itération, plusieurs itérations possibles
    - Peut être lent pour de grandes instances
    
    Args:
        cycle: Liste ordonnée des stations formant le cycle (commence et finit par la même station)
        distances: Dictionnaire des distances créé par creer_matrice_distances
        
    Returns:
        Cycle amélioré (le coût diminue ou reste stable)
    """
    # Vérification que le cycle est valide
    if len(cycle) <= 3:
        # Un cycle avec 3 stations ou moins ne peut pas être amélioré par 2-opt
        return cycle
    
    # Copie du cycle pour ne pas modifier l'original
    cycle_ameliore = cycle.copy()
    amelioration_trouvee = True
    
    # On continue tant qu'on trouve des améliorations
    while amelioration_trouvee:
        amelioration_trouvee = False
        meilleur_gain = 0.0
        meilleur_i = -1
        meilleur_j = -1
        
        # Test de tous les échanges 2-opt possibles
        # On ignore la dernière station car c'est la même que la première (fermeture du cycle)
        nombre_stations = len(cycle_ameliore) - 1
        
        for i in range(nombre_stations - 1):
            for j in range(i + 2, nombre_stations):
                # Calcul du gain de l'échange
                gain = calculer_gain_2opt(cycle_ameliore, i, j, distances)
                
                # Si le gain est positif, on retient cet échange
                if gain > meilleur_gain:
                    meilleur_gain = gain
                    meilleur_i = i
                    meilleur_j = j
        
        # Si on a trouvé une amélioration, on l'applique
        if meilleur_gain > 0.0001:  # Petite tolérance pour les erreurs numériques
            cycle_ameliore = appliquer_2opt(cycle_ameliore, meilleur_i, meilleur_j)
            amelioration_trouvee = True
    
    return cycle_ameliore
