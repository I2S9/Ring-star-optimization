# Script pour générer automatiquement les figures
# Génère les visualisations des instances et des solutions

import os
import sys

# Ajout du répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lecture_tsp import lire_fichier_tsp
from src.visualisation import sauvegarder_instance, sauvegarder_solution_complete
from src.heuristiques.solution_initiale import construire_solution_initiale
from src.liste_instances import lister_instances_par_taille


def generer_figures_instance(chemin_fichier, dossier_sortie='resultats/figures'):
    """
    Génère la figure d'une instance TSPLIB.
    
    Args:
        chemin_fichier: Chemin vers le fichier .tsp
        dossier_sortie: Dossier où sauvegarder la figure
    """
    # Création du dossier si nécessaire
    os.makedirs(dossier_sortie, exist_ok=True)
    
    # Lecture de l'instance
    points = lire_fichier_tsp(chemin_fichier)
    
    # Nom du fichier sans extension
    nom_instance = os.path.basename(chemin_fichier).replace('.tsp', '')
    
    # Chemin de sortie
    chemin_figure = os.path.join(dossier_sortie, f'instance_{nom_instance}.png')
    
    # Génération de la figure
    sauvegarder_instance(points, chemin_figure, f"Instance {nom_instance}")
    
    print(f"Figure générée : {chemin_figure}")


def generer_figures_solution(chemin_fichier, p, alpha=0.5, dossier_sortie='resultats/figures'):
    """
    Génère les figures d'une solution pour une instance.
    
    Args:
        chemin_fichier: Chemin vers le fichier .tsp
        p: Nombre de stations
        alpha: Coefficient de pondération
        dossier_sortie: Dossier où sauvegarder les figures
    """
    # Création du dossier si nécessaire
    os.makedirs(dossier_sortie, exist_ok=True)
    
    # Lecture de l'instance
    points = lire_fichier_tsp(chemin_fichier)
    
    # Nom du fichier sans extension
    nom_instance = os.path.basename(chemin_fichier).replace('.tsp', '')
    
    # Construction de la solution
    solution = construire_solution_initiale(points, p, methode_selection='grille', 
                                          ameliorer_cycle=True, alpha=alpha)
    
    # Chemin de sortie
    chemin_figure = os.path.join(dossier_sortie, 
                                f'solution_{nom_instance}_p{p}_alpha{alpha}.png')
    
    # Génération de la figure
    sauvegarder_solution_complete(points, solution, chemin_figure, 
                                 f"Solution {nom_instance} (p={p}, α={alpha})")
    
    print(f"Figure générée : {chemin_figure}")


def generer_toutes_figures():
    """
    Génère toutes les figures pour les instances disponibles.
    Utilise toutes les instances TSPLIB disponibles dans donnees/tsplib/.
    """
    # Récupération de toutes les instances disponibles
    # On se limite aux petites et moyennes instances pour les figures
    # (les grandes instances peuvent être trop lourdes à visualiser)
    instances_petites = lister_instances_par_taille(taille_max=100)
    
    print(f"Génération des figures pour {len(instances_petites)} instances...")
    print("(Instances avec n <= 100 points)\n")
    
    print("Génération des figures d'instances...")
    for instance in instances_petites:
        if os.path.exists(instance):
            try:
                # Vérification que l'instance a des coordonnées avant de générer la figure
                from src.lecture_tsp import lire_fichier_tsp
                points = lire_fichier_tsp(instance)
                if len(points) > 0:
                    generer_figures_instance(instance)
                else:
                    nom_instance = os.path.basename(instance)
                    print(f"Instance {nom_instance} ignorée (pas de coordonnées, utilise une matrice de distances)")
            except Exception as e:
                print(f"Erreur pour {instance} : {e}")
        else:
            print(f"Instance non trouvée : {instance}")
    
    print("\nGénération des figures de solutions...")
    # Pour les solutions, on génère pour plusieurs instances représentatives
    # avec différentes tailles et différents paramètres
    instances_representatives = [
        'donnees/tsplib/burma14.tsp',      # Petite instance pour PLNE
        'donnees/tsplib/ulysses16.tsp',    # Petite instance
        'donnees/tsplib/att48.tsp',        # Instance moyenne (utilisée dans le rapport)
        'donnees/tsplib/berlin52.tsp',    # Instance moyenne (utilisée dans le rapport)
        'donnees/tsplib/eil51.tsp',        # Instance moyenne
        'donnees/tsplib/st70.tsp',         # Instance moyenne-grande
        'donnees/tsplib/a280.tsp'          # Grande instance (limite)
    ]
    
    for instance in instances_representatives:
        if os.path.exists(instance):
            try:
                # Génération avec différents paramètres pour comparaison
                generer_figures_solution(instance, p=5, alpha=0.5)
                # Pour les petites instances, on génère aussi avec p=3
                nom_instance = os.path.basename(instance).replace('.tsp', '')
                if 'burma14' in nom_instance or 'ulysses16' in nom_instance:
                    generer_figures_solution(instance, p=3, alpha=0.5)
            except Exception as e:
                print(f"Erreur pour {instance} : {e}")
    
    print("\nGénération terminée.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mode avec arguments
        if sys.argv[1] == "instance" and len(sys.argv) > 2:
            generer_figures_instance(sys.argv[2])
        elif sys.argv[1] == "solution" and len(sys.argv) > 3:
            p = int(sys.argv[3])
            alpha = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
            generer_figures_solution(sys.argv[2], p, alpha)
        else:
            print("Usage:")
            print("  python src/generer_figures.py")
            print("  python src/generer_figures.py instance <fichier.tsp>")
            print("  python src/generer_figures.py solution <fichier.tsp> <p> [alpha]")
    else:
        # Mode par défaut : génère toutes les figures
        generer_toutes_figures()
