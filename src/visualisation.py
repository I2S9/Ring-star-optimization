# Fichier pour la visualisation des solutions
# Affiche les instances et les solutions du problème anneau-étoile

import matplotlib.pyplot as plt


def afficher_instance(points, titre="Instance TSPLIB"):
    """
    Affiche le nuage de points d'une instance TSPLIB.
    
    Cette fonction permet de visualiser les données brutes avant
    toute résolution. Les points sont affichés avec leurs numéros
    pour faciliter l'identification.
    
    Args:
        points: Liste de tuples (id, x, y) représentant les points
        titre: Titre à afficher sur le graphique
    """
    # Extraction des coordonnées x et y
    coordonnees_x = []
    coordonnees_y = []
    identifiants = []
    
    for point in points:
        identifiants.append(point[0])
        coordonnees_x.append(point[1])
        coordonnees_y.append(point[2])
    
    # Vérification qu'on a des points à afficher
    if len(points) == 0:
        print(f"Attention : aucun point trouvé")
        return
    
    # Création de la figure
    plt.figure(figsize=(10, 8))
    
    # Affichage des points (plus gros et plus visibles)
    plt.scatter(coordonnees_x, coordonnees_y, color='blue', s=100, zorder=3, edgecolors='darkblue', linewidths=1)
    
    # Affichage des numéros des points (seulement pour les petites instances)
    if len(points) <= 50:
        for i in range(len(points)):
            plt.annotate(
                str(identifiants[i]),
                (coordonnees_x[i], coordonnees_y[i]),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8,
                color='black',
                weight='bold'
            )
    
    # Configuration des axes pour qu'ils soient lisibles
    plt.xlabel('Coordonnée X', fontsize=12)
    plt.ylabel('Coordonnée Y', fontsize=12)
    plt.title(titre, fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Ajustement automatique des limites pour voir tous les points avec une marge
    if len(coordonnees_x) > 0:
        marge_x = (max(coordonnees_x) - min(coordonnees_x)) * 0.1
        marge_y = (max(coordonnees_y) - min(coordonnees_y)) * 0.1
        plt.xlim(min(coordonnees_x) - marge_x, max(coordonnees_x) + marge_x)
        plt.ylim(min(coordonnees_y) - marge_y, max(coordonnees_y) + marge_y)
    
    plt.tight_layout()
    
    # Affichage du graphique
    plt.show()


def sauvegarder_instance(points, chemin_fichier, titre="Instance TSPLIB"):
    """
    Sauvegarde l'affichage d'une instance dans un fichier.
    
    Utile pour générer les figures du rapport sans avoir à
    afficher les graphiques à l'écran.
    
    Args:
        points: Liste de tuples (id, x, y) représentant les points
        chemin_fichier: Chemin où sauvegarder l'image
        titre: Titre à afficher sur le graphique
    """
    # Extraction des coordonnées x et y
    coordonnees_x = []
    coordonnees_y = []
    identifiants = []
    
    for point in points:
        identifiants.append(point[0])
        coordonnees_x.append(point[1])
        coordonnees_y.append(point[2])
    
    # Création de la figure
    plt.figure(figsize=(10, 8))
    
    # Vérification qu'on a des points à afficher
    if len(points) == 0:
        print(f"Attention : aucun point trouvé pour {chemin_fichier}")
        plt.close()
        return
    
    # Affichage des points (plus gros et plus visibles)
    plt.scatter(coordonnees_x, coordonnees_y, color='blue', s=100, zorder=3, edgecolors='darkblue', linewidths=1)
    
    # Affichage des numéros des points (seulement pour les petites instances)
    if len(points) <= 50:
        for i in range(len(points)):
            plt.annotate(
                str(identifiants[i]),
                (coordonnees_x[i], coordonnees_y[i]),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8,
                color='black',
                weight='bold'
            )
    
    # Configuration des axes pour qu'ils soient lisibles
    plt.xlabel('Coordonnée X', fontsize=12)
    plt.ylabel('Coordonnée Y', fontsize=12)
    plt.title(titre, fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Ajustement automatique des limites pour voir tous les points avec une marge
    if len(coordonnees_x) > 0:
        marge_x = (max(coordonnees_x) - min(coordonnees_x)) * 0.1
        marge_y = (max(coordonnees_y) - min(coordonnees_y)) * 0.1
        plt.xlim(min(coordonnees_x) - marge_x, max(coordonnees_x) + marge_x)
        plt.ylim(min(coordonnees_y) - marge_y, max(coordonnees_y) + marge_y)
    
    plt.tight_layout()
    
    # Sauvegarde de la figure
    plt.savefig(chemin_fichier, dpi=150, bbox_inches='tight')
    plt.close()


def afficher_solution_complete(points, solution, titre="Solution anneau-étoile"):
    """
    Affiche une solution complète du problème anneau-étoile.
    
    La visualisation montre :
    - Les points non stations (en bleu)
    - Les stations (en rouge, plus gros)
    - Le cycle entre les stations (lignes noires épaisses)
    - Les affectations (lignes grises fines entre points et stations)
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        solution: Dictionnaire de solution créé par construire_solution_initiale
        titre: Titre à afficher sur le graphique
    """
    # Création d'un dictionnaire pour accéder rapidement aux coordonnées
    coordonnees_par_id = {}
    for point in points:
        coordonnees_par_id[point[0]] = (point[1], point[2])
    
    # Séparation des stations et des points non stations
    stations_set = set(solution['stations'])
    points_non_stations = []
    points_stations = []
    
    for point in points:
        if point[0] in stations_set:
            points_stations.append(point)
        else:
            points_non_stations.append(point)
    
    # Création de la figure
    plt.figure(figsize=(12, 10))
    
    # Affichage des points non stations (en bleu)
    if points_non_stations:
        x_non_stations = [p[1] for p in points_non_stations]
        y_non_stations = [p[2] for p in points_non_stations]
        plt.scatter(x_non_stations, y_non_stations, color='lightblue', s=30, zorder=2, label='Points non stations')
    
    # Affichage des stations (en rouge, plus gros)
    if points_stations:
        x_stations = [p[1] for p in points_stations]
        y_stations = [p[2] for p in points_stations]
        plt.scatter(x_stations, y_stations, color='red', s=150, zorder=4, marker='s', label='Stations')
    
    # Affichage des affectations (lignes grises fines)
    for id_point, id_station in solution['affectations'].items():
        if id_point != id_station:  # On n'affiche pas les auto-affectations
            x_point, y_point = coordonnees_par_id[id_point]
            x_station, y_station = coordonnees_par_id[id_station]
            plt.plot([x_point, x_station], [y_point, y_station], 
                    color='gray', linewidth=0.5, alpha=0.5, zorder=1)
    
    # Affichage du cycle (lignes noires épaisses)
    cycle = solution['cycle']
    if len(cycle) > 1:
        x_cycle = [coordonnees_par_id[s][0] for s in cycle]
        y_cycle = [coordonnees_par_id[s][1] for s in cycle]
        plt.plot(x_cycle, y_cycle, color='black', linewidth=2, zorder=3, label='Cycle')
    
    # Affichage des numéros des stations
    for point in points_stations:
        plt.annotate(
            str(point[0]),
            (point[1], point[2]),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=10,
            color='darkred',
            weight='bold'
        )
    
    # Configuration des axes
    plt.xlabel('Coordonnée X', fontsize=12)
    plt.ylabel('Coordonnée Y', fontsize=12)
    plt.title(f"{titre}\nCoût total: {solution['cout_total']:.2f}", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Affichage du graphique
    plt.show()


def sauvegarder_solution_complete(points, solution, chemin_fichier, titre="Solution anneau-étoile"):
    """
    Sauvegarde la visualisation d'une solution complète dans un fichier.
    
    Args:
        points: Liste de tuples (id, x, y) représentant tous les points
        solution: Dictionnaire de solution créé par construire_solution_initiale
        chemin_fichier: Chemin où sauvegarder l'image
        titre: Titre à afficher sur le graphique
    """
    # Création d'un dictionnaire pour accéder rapidement aux coordonnées
    coordonnees_par_id = {}
    for point in points:
        coordonnees_par_id[point[0]] = (point[1], point[2])
    
    # Séparation des stations et des points non stations
    stations_set = set(solution['stations'])
    points_non_stations = []
    points_stations = []
    
    for point in points:
        if point[0] in stations_set:
            points_stations.append(point)
        else:
            points_non_stations.append(point)
    
    # Création de la figure
    plt.figure(figsize=(12, 10))
    
    # Affichage des points non stations (en bleu)
    if points_non_stations:
        x_non_stations = [p[1] for p in points_non_stations]
        y_non_stations = [p[2] for p in points_non_stations]
        plt.scatter(x_non_stations, y_non_stations, color='lightblue', s=30, zorder=2, label='Points non stations')
    
    # Affichage des stations (en rouge, plus gros)
    if points_stations:
        x_stations = [p[1] for p in points_stations]
        y_stations = [p[2] for p in points_stations]
        plt.scatter(x_stations, y_stations, color='red', s=150, zorder=4, marker='s', label='Stations')
    
    # Affichage des affectations (lignes grises fines)
    for id_point, id_station in solution['affectations'].items():
        if id_point != id_station:  # On n'affiche pas les auto-affectations
            x_point, y_point = coordonnees_par_id[id_point]
            x_station, y_station = coordonnees_par_id[id_station]
            plt.plot([x_point, x_station], [y_point, y_station], 
                    color='gray', linewidth=0.5, alpha=0.5, zorder=1)
    
    # Affichage du cycle (lignes noires épaisses)
    cycle = solution['cycle']
    if len(cycle) > 1:
        x_cycle = [coordonnees_par_id[s][0] for s in cycle]
        y_cycle = [coordonnees_par_id[s][1] for s in cycle]
        plt.plot(x_cycle, y_cycle, color='black', linewidth=2, zorder=3, label='Cycle')
    
    # Affichage des numéros des stations
    for point in points_stations:
        plt.annotate(
            str(point[0]),
            (point[1], point[2]),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=10,
            color='darkred',
            weight='bold'
        )
    
    # Configuration des axes
    plt.xlabel('Coordonnée X', fontsize=12)
    plt.ylabel('Coordonnée Y', fontsize=12)
    plt.title(f"{titre}\nCoût total: {solution['cout_total']:.2f}", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Sauvegarde de la figure
    plt.savefig(chemin_fichier, dpi=150, bbox_inches='tight')
    plt.close()
