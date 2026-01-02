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
    
    # Création de la figure
    plt.figure(figsize=(10, 8))
    
    # Affichage des points
    plt.scatter(coordonnees_x, coordonnees_y, color='blue', s=50, zorder=3)
    
    # Affichage des numéros des points
    for i in range(len(points)):
        plt.annotate(
            str(identifiants[i]),
            (coordonnees_x[i], coordonnees_y[i]),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8,
            color='black'
        )
    
    # Configuration des axes pour qu'ils soient lisibles
    plt.xlabel('Coordonnée X', fontsize=12)
    plt.ylabel('Coordonnée Y', fontsize=12)
    plt.title(titre, fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Ajustement automatique des limites pour voir tous les points
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
    
    # Affichage des points
    plt.scatter(coordonnees_x, coordonnees_y, color='blue', s=50, zorder=3)
    
    # Affichage des numéros des points
    for i in range(len(points)):
        plt.annotate(
            str(identifiants[i]),
            (coordonnees_x[i], coordonnees_y[i]),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8,
            color='black'
        )
    
    # Configuration des axes pour qu'ils soient lisibles
    plt.xlabel('Coordonnée X', fontsize=12)
    plt.ylabel('Coordonnée Y', fontsize=12)
    plt.title(titre, fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Ajustement automatique des limites pour voir tous les points
    plt.tight_layout()
    
    # Sauvegarde de la figure
    plt.savefig(chemin_fichier, dpi=150, bbox_inches='tight')
    plt.close()
