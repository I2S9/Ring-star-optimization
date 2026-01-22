# Script pour générer automatiquement les figures
# Génère les visualisations des instances et des solutions

import os
import sys

# Ajout du répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lecture_tsp import lire_fichier_tsp
from src.visualisation import sauvegarder_instance, sauvegarder_solution_complete
from src.heuristiques.solution_initiale import construire_solution_initiale


def generer_figures_instance(chemin_fichier, dossier_sortie='results/figures'):
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


def generer_figures_solution(chemin_fichier, p, alpha=0.5, dossier_sortie='results/figures'):
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
    Génère toutes les figures pour les instances principales.
    """
    # Liste des instances à traiter
    instances = [
        'tsplib-master/tsplib-master/att48.tsp',
        'tsplib-master/tsplib-master/berlin52.tsp',
        'tsplib-master/tsplib-master/a280.tsp'
    ]
    
    # Paramètres de test
    valeurs_p = [5, 7, 10]
    valeurs_alpha = [0.3, 0.5, 0.7]
    
    print("Génération des figures d'instances...")
    for instance in instances:
        if os.path.exists(instance):
            generer_figures_instance(instance)
        else:
            print(f"Instance non trouvée : {instance}")
    
    print("\nGénération des figures de solutions...")
    for instance in instances:
        if os.path.exists(instance):
            # On génère quelques solutions représentatives
            generer_figures_solution(instance, p=5, alpha=0.5)
            if 'att48' in instance:
                # Pour att48, on génère plusieurs variantes
                generer_figures_solution(instance, p=7, alpha=0.5)
                generer_figures_solution(instance, p=5, alpha=0.3)
    
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
