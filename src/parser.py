# Fichier pour le parsing des instances TSPLIB
# Lit les fichiers au format TSPLIB et extrait les coordonnées des points

def lire_fichier_tsp(chemin_fichier):
    """
    Lit un fichier .tsp au format TSPLIB et extrait les points.
    
    Args:
        chemin_fichier: Chemin vers le fichier .tsp à lire
        
    Returns:
        liste de tuples (id, x, y) représentant les points
    """
    points = []
    
    # Ouverture du fichier en lecture
    with open(chemin_fichier, 'r') as fichier:
        # Indicateur pour savoir si on est dans la section des coordonnées
        dans_section_coord = False
        
        # Lecture ligne par ligne
        for ligne in fichier:
            # Suppression des espaces en début et fin de ligne
            ligne = ligne.strip()
            
            # Détection du début de la section des coordonnées
            if ligne == 'NODE_COORD_SECTION':
                dans_section_coord = True
                continue
            
            # Arrêt à la fin du fichier
            if ligne == 'EOF':
                break
            
            # Si on est dans la section des coordonnées, on lit les points
            if dans_section_coord:
                # Séparation de la ligne en éléments (id, x, y)
                elements = ligne.split()
                
                # Vérification qu'on a bien 3 éléments
                if len(elements) == 3:
                    id_point = int(elements[0])
                    x = float(elements[1])
                    y = float(elements[2])
                    
                    # Ajout du point à la liste
                    points.append((id_point, x, y))
    
    return points
