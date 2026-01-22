# Utilitaire pour lister et utiliser toutes les instances TSPLIB disponibles

import os
import glob


def lister_instances_tsplib(dossier='donnees/tsplib'):
    """
    Liste toutes les instances TSPLIB disponibles dans le dossier.
    
    Args:
        dossier: Chemin vers le dossier contenant les instances
        
    Returns:
        Liste des chemins complets vers les fichiers .tsp
    """
    if not os.path.exists(dossier):
        return []
    
    # Recherche de tous les fichiers .tsp
    pattern = os.path.join(dossier, '*.tsp')
    instances = glob.glob(pattern)
    
    # Tri par nom de fichier
    instances.sort()
    
    return instances


def obtenir_info_instance(chemin_fichier):
    """
    Obtient des informations sur une instance sans la charger complètement.
    
    Args:
        chemin_fichier: Chemin vers le fichier .tsp
        
    Returns:
        Dictionnaire avec les informations de l'instance
    """
    info = {
        'nom': os.path.basename(chemin_fichier),
        'chemin': chemin_fichier,
        'dimension': None,
        'type': None
    }
    
    try:
        with open(chemin_fichier, 'r') as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne.startswith('DIMENSION'):
                    info['dimension'] = int(ligne.split(':')[1].strip())
                elif ligne.startswith('TYPE'):
                    info['type'] = ligne.split(':')[1].strip()
                elif ligne == 'NODE_COORD_SECTION':
                    # On s'arrête ici pour ne pas lire tout le fichier
                    break
    except Exception as e:
        print(f"Erreur lors de la lecture de {chemin_fichier} : {e}")
    
    return info


def lister_instances_par_taille(dossier='donnees/tsplib', taille_min=None, taille_max=None):
    """
    Liste les instances filtrées par taille.
    
    Args:
        dossier: Chemin vers le dossier contenant les instances
        taille_min: Taille minimale (nombre de points)
        taille_max: Taille maximale (nombre de points)
        
    Returns:
        Liste des instances correspondant aux critères
    """
    toutes_instances = lister_instances_tsplib(dossier)
    instances_filtrees = []
    
    for instance in toutes_instances:
        info = obtenir_info_instance(instance)
        dimension = info['dimension']
        
        if dimension is None:
            continue
        
        # Filtrage par taille
        if taille_min is not None and dimension < taille_min:
            continue
        if taille_max is not None and dimension > taille_max:
            continue
        
        instances_filtrees.append(instance)
    
    return instances_filtrees


def afficher_instances_disponibles(dossier='donnees/tsplib'):
    """
    Affiche la liste de toutes les instances disponibles avec leurs informations.
    
    Args:
        dossier: Chemin vers le dossier contenant les instances
    """
    instances = lister_instances_tsplib(dossier)
    
    print(f"\n=== Instances TSPLIB disponibles ({len(instances)} fichiers) ===\n")
    
    # Groupement par taille pour faciliter la lecture
    petites = []  # n <= 50
    moyennes = []  # 50 < n <= 200
    grandes = []  # n > 200
    
    for instance in instances:
        info = obtenir_info_instance(instance)
        dimension = info['dimension']
        
        if dimension is None:
            continue
        
        if dimension <= 50:
            petites.append((info['nom'], dimension))
        elif dimension <= 200:
            moyennes.append((info['nom'], dimension))
        else:
            grandes.append((info['nom'], dimension))
    
    print(f"Petites instances (n <= 50) : {len(petites)}")
    for nom, dim in sorted(petites, key=lambda x: x[1]):
        print(f"  - {nom} ({dim} points)")
    
    print(f"\nInstances moyennes (50 < n <= 200) : {len(moyennes)}")
    for nom, dim in sorted(moyennes, key=lambda x: x[1]):
        print(f"  - {nom} ({dim} points)")
    
    print(f"\nGrandes instances (n > 200) : {len(grandes)}")
    for nom, dim in sorted(grandes, key=lambda x: x[1])[:10]:  # Afficher seulement les 10 premières
        print(f"  - {nom} ({dim} points)")
    if len(grandes) > 10:
        print(f"  ... et {len(grandes) - 10} autres")
    
    print(f"\nTotal : {len(petites) + len(moyennes) + len(grandes)} instances")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "petites":
            instances = lister_instances_par_taille(taille_max=50)
            print(f"\n{len(instances)} petites instances (n <= 50):")
            for inst in instances:
                print(f"  {inst}")
        elif sys.argv[1] == "moyennes":
            instances = lister_instances_par_taille(taille_min=51, taille_max=200)
            print(f"\n{len(instances)} instances moyennes (50 < n <= 200):")
            for inst in instances:
                print(f"  {inst}")
        elif sys.argv[1] == "grandes":
            instances = lister_instances_par_taille(taille_min=201)
            print(f"\n{len(instances)} grandes instances (n > 200):")
            for inst in instances:
                print(f"  {inst}")
    else:
        afficher_instances_disponibles()
