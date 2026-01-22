# Modèle PLNE compact pour le problème anneau-étoile
# Formulation exacte utilisant la programmation linéaire en nombres entiers

import pulp
from src.calcul_distances import creer_matrice_distances


def resoudre_plne(points, p, alpha=0.5, timeout=300):
    """
    Résout le problème anneau-étoile avec une formulation PLNE compacte.
    
    Variables :
    - y[i] : variable binaire, vaut 1 si le point i est une station
    - x[i,j] : variable binaire, vaut 1 si l'arête (i,j) est dans le cycle (i < j)
    - z[i,j] : variable binaire, vaut 1 si le point i est affecté à la station j
    
    Contraintes :
    1. Degré : chaque station a exactement 2 arêtes dans le cycle
    2. Affectation : chaque point est affecté à exactement une station
    3. Connexité : le cycle est connexe (contraintes de sous-tour élimination)
    4. Cardinalité : exactement p stations sont sélectionnées
    5. Station 1 : la station 1 est toujours sélectionnée
    
    Lien avec l'optimisation linéaire :
    - Le problème est modélisé comme un programme linéaire en nombres entiers
    - Le solveur utilise des techniques de branch-and-bound ou branch-and-cut
    - La relaxation linéaire donne une borne inférieure
    - L'exploration de l'arbre de recherche garantit l'optimalité (si résolu)
    
    Limites de taille d'instance :
    - Le nombre de variables est O(n²) où n = nombre de points
    - Le nombre de contraintes est O(n²)
    - Pour n > 20, le temps de résolution peut devenir très long
    - Pour n > 50, la résolution exacte devient souvent impraticable
    - Recommandé pour n <= 15-20 points
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        p: Nombre de stations à sélectionner
        alpha: Coefficient de pondération (0 <= alpha <= 1)
        timeout: Temps maximum de résolution en secondes
        
    Returns:
        Dictionnaire contenant la solution optimale ou None si non résolu
    """
    # Création de la matrice des distances
    distances = creer_matrice_distances(points)
    
    # Extraction des identifiants
    identifiants = [point[0] for point in points]
    n = len(identifiants)
    
    # Vérification de la taille
    if n > 20:
        print(f"Attention : instance de taille {n}, la résolution peut être longue")
    
    # Création du problème
    probleme = pulp.LpProblem("Anneau_Etoile", pulp.LpMinimize)
    
    # Variables de décision
    # y[i] : 1 si le point i est une station
    y = pulp.LpVariable.dicts("y", identifiants, cat='Binary')
    
    # x[i,j] : 1 si l'arête (i,j) est dans le cycle (i < j)
    x = {}
    for i in identifiants:
        for j in identifiants:
            if i < j:
                x[(i, j)] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')
    
    # z[i,j] : 1 si le point i est affecté à la station j
    z = {}
    for i in identifiants:
        for j in identifiants:
            z[(i, j)] = pulp.LpVariable(f"z_{i}_{j}", cat='Binary')
    
    # Fonction objectif
    # Minimiser : alpha * longueur_cycle + (1-alpha) * cout_affectation
    cout_cycle = pulp.lpSum([distances[(i, j)] * x[(i, j)] 
                            for i in identifiants for j in identifiants if i < j])
    cout_affectation = pulp.lpSum([distances[(i, j)] * z[(i, j)] 
                                  for i in identifiants for j in identifiants])
    
    probleme += alpha * cout_cycle + (1 - alpha) * cout_affectation
    
    # Contraintes
    
    # 1. Cardinalité : exactement p stations
    probleme += pulp.lpSum([y[i] for i in identifiants]) == p
    
    # 2. Station 1 toujours sélectionnée
    probleme += y[1] == 1
    
    # 3. Contraintes de degré : chaque station a exactement 2 arêtes
    for i in identifiants:
        # Somme des arêtes incidentes à i
        arêtes_incidentes = []
        for j in identifiants:
            if i < j:
                arêtes_incidentes.append(x[(i, j)])
            elif j < i:
                arêtes_incidentes.append(x[(j, i)])
        
        # Si i est une station, il a exactement 2 arêtes
        probleme += pulp.lpSum(arêtes_incidentes) == 2 * y[i]
    
    # 4. Contraintes d'affectation : chaque point est affecté à exactement une station
    for i in identifiants:
        probleme += pulp.lpSum([z[(i, j)] for j in identifiants]) == 1
    
    # 5. Contraintes logiques : un point ne peut être affecté qu'à une station
    for i in identifiants:
        for j in identifiants:
            probleme += z[(i, j)] <= y[j]
    
    # 6. Contraintes de sous-tour élimination (MTZ - Miller-Tucker-Zemlin)
    # Variables auxiliaires u[i] pour l'ordre de visite (seulement pour les stations)
    u = pulp.LpVariable.dicts("u", identifiants, lowBound=0, upBound=n, cat='Integer')
    
    # u[1] = 1 si la station 1 est sélectionnée
    probleme += u[1] == y[1]
    
    # Pour chaque arête (i,j) dans le cycle, u[j] >= u[i] + 1
    # Mais seulement si i et j sont des stations ET que l'arête est utilisée
    for i in identifiants:
        for j in identifiants:
            if i != j and i < j:
                # Si l'arête (i,j) est dans le cycle ET que i et j sont stations,
                # alors u[j] >= u[i] + 1
                # Utilisation de la big-M method
                M = n
                # Si x[(i,j)] = 1 et y[i] = 1 et y[j] = 1, alors u[j] >= u[i] + 1
                probleme += u[j] >= u[i] + 1 - M * (1 - x[(i, j)]) - M * (1 - y[i]) - M * (1 - y[j])
                
                # Si i n'est pas une station, u[i] = 0
                probleme += u[i] <= M * y[i]
                probleme += u[j] <= M * y[j]
    
    # Résolution
    try:
        # Utilisation du solveur par défaut (CBC si disponible)
        solveur = pulp.PULP_CBC_CMD(timeLimit=timeout, msg=1)
        probleme.solve(solveur)
        
        # Vérification du statut
        statut = pulp.LpStatus[probleme.status]
        
        if statut == 'Optimal':
            # Extraction de la solution
            stations = [i for i in identifiants if pulp.value(y[i]) > 0.5]
            
            # Extraction du cycle
            arêtes_cycle = [(i, j) for i in identifiants for j in identifiants 
                          if i < j and pulp.value(x[(i, j)]) > 0.5]
            
            # Construction du cycle ordonné
            cycle = construire_cycle_depuis_aretes(stations, arêtes_cycle)
            
            # Extraction des affectations
            affectations = {}
            for i in identifiants:
                for j in identifiants:
                    if pulp.value(z[(i, j)]) > 0.5:
                        affectations[i] = j
                        break
            
            # Calcul des coûts
            longueur_cycle = sum([distances[(i, j)] for i, j in arêtes_cycle])
            cout_affectation = sum([distances[(i, affectations[i])] for i in identifiants])
            cout_total = alpha * longueur_cycle + (1 - alpha) * cout_affectation
            
            solution = {
                'stations': stations,
                'cycle': cycle,
                'affectations': affectations,
                'longueur_cycle': longueur_cycle,
                'cout_affectation': cout_affectation,
                'cout_total': cout_total,
                'statut': statut,
                'borne_inf': probleme.objective.value()
            }
            
            return solution
        else:
            print(f"Statut de résolution : {statut}")
            return None
            
    except Exception as e:
        print(f"Erreur lors de la résolution : {e}")
        return None


def construire_cycle_depuis_aretes(stations, arêtes):
    """
    Construit un cycle ordonné à partir d'une liste d'arêtes.
    
    Args:
        stations: Liste des stations
        arêtes: Liste de tuples (i, j) représentant les arêtes du cycle
        
    Returns:
        Liste ordonnée des stations dans le cycle
    """
    if len(stations) == 0:
        return []
    
    if len(stations) == 1:
        return [stations[0], stations[0]]
    
    # Création d'un graphe avec les arêtes
    graphe = {s: [] for s in stations}
    for i, j in arêtes:
        if i in stations and j in stations:
            graphe[i].append(j)
            graphe[j].append(i)
    
    # Construction du cycle en partant de la station 1
    if 1 not in stations:
        station_depart = stations[0]
    else:
        station_depart = 1
    
    cycle = [station_depart]
    station_courante = station_depart
    station_precedente = None
    
    # Parcours du cycle
    while len(cycle) < len(stations):
        voisins = graphe[station_courante]
        # On choisit le voisin qui n'est pas le précédent
        for voisin in voisins:
            if voisin != station_precedente:
                cycle.append(voisin)
                station_precedente = station_courante
                station_courante = voisin
                break
    
    # Fermeture du cycle
    cycle.append(station_depart)
    
    return cycle
