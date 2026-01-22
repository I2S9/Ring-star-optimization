# Point d'entrée principal du programme
# Permet de lancer les comparaisons expérimentales

import sys
from src.comparaisons import comparer_methodes, sauvegarder_resultats, analyser_resultats


def main():
    """
    Point d'entrée principal pour les comparaisons expérimentales.
    
    Usage :
        python src/main.py <fichier_tsp> <p> [alpha]
    
    Exemple :
        python src/main.py tsplib-master/tsplib-master/att48.tsp 5 0.5
    """
    if len(sys.argv) < 3:
        print("Usage : python src/main.py <fichier_tsp> <p> [alpha]")
        print("Exemple : python src/main.py tsplib-master/tsplib-master/att48.tsp 5 0.5")
        sys.exit(1)
    
    chemin_fichier = sys.argv[1]
    p = int(sys.argv[2])
    alpha = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    
    # Comparaison des méthodes
    resultats = comparer_methodes(chemin_fichier, p, alpha=alpha, tester_plne=True)
    
    # Sauvegarde des résultats
    sauvegarder_resultats(resultats)
    
    # Analyse
    analyse = analyser_resultats(resultats)
    
    print("\n=== Analyse comparative ===")
    print(f"Meilleure méthode : {analyse['meilleure_methode']}")
    print(f"Meilleur coût : {analyse['meilleur_cout']:.2f}")
    print(f"Méthode la plus rapide : {analyse['methode_plus_rapide']}")
    print(f"Temps le plus rapide : {analyse['plus_rapide']:.2f} secondes")
    print("\nÉcarts relatifs :")
    for methode, comp in analyse['comparaisons'].items():
        print(f"  {methode} : {comp['ecart_pourcentage']:.2f}% d'écart, "
              f"{comp['ratio_temps']:.2f}x plus lent")
    
    print(f"\nRésultats sauvegardés dans results/resultats.txt")


if __name__ == "__main__":
    main()
