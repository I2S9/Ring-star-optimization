# Comparaisons expérimentales des différentes méthodes
# Compare heuristiques, métaheuristiques et PLNE

import time
from src.lecture_tsp import lire_fichier_tsp
from src.calcul_distances import creer_matrice_distances
from src.heuristiques.solution_initiale import construire_solution_initiale
from src.heuristiques.metaheuristique import recuit_simule
from src.plne.formulation_compacte import resoudre_plne


def comparer_methodes(chemin_fichier, p, alpha=0.5, tester_plne=True):
    """
    Compare les différentes méthodes de résolution.
    
    Teste :
    - Heuristique initiale (grille + plus proche voisin + 2-opt)
    - Heuristique initiale (aléatoire + plus proche voisin + 2-opt)
    - Métaheuristique (recuit simulé)
    - PLNE (sur petites instances seulement)
    
    Args:
        chemin_fichier: Chemin vers le fichier .tsp
        p: Nombre de stations à sélectionner
        alpha: Coefficient de pondération
        tester_plne: Si True, teste aussi la PLNE (seulement pour petites instances)
        
    Returns:
        Dictionnaire contenant les résultats de toutes les méthodes
    """
    # Chargement de l'instance
    points = lire_fichier_tsp(chemin_fichier)
    distances = creer_matrice_distances(points)
    n = len(points)
    
    resultats = {
        'instance': chemin_fichier,
        'nombre_points': n,
        'nombre_stations': p,
        'alpha': alpha,
        'methodes': {}
    }
    
    print(f"\n=== Comparaison des méthodes ===")
    print(f"Instance : {chemin_fichier}")
    print(f"Nombre de points : {n}")
    print(f"Nombre de stations : {p}")
    print(f"Alpha : {alpha}\n")
    
    # 1. Heuristique initiale (grille)
    print("1. Heuristique initiale (grille)...")
    debut = time.time()
    solution_grille = construire_solution_initiale(
        points, p, methode_selection='grille', ameliorer_cycle=True, alpha=alpha
    )
    temps_grille = time.time() - debut
    resultats['methodes']['heuristique_grille'] = {
        'cout_total': solution_grille['cout_total'],
        'longueur_cycle': solution_grille['longueur_cycle'],
        'cout_affectation': solution_grille['cout_affectation'],
        'temps': temps_grille,
        'stations': solution_grille['stations']
    }
    print(f"   Coût total : {solution_grille['cout_total']:.2f}")
    print(f"   Temps : {temps_grille:.2f} secondes\n")
    
    # 2. Heuristique initiale (aléatoire)
    print("2. Heuristique initiale (aléatoire)...")
    debut = time.time()
    solution_aleatoire = construire_solution_initiale(
        points, p, methode_selection='aleatoire', ameliorer_cycle=True, alpha=alpha
    )
    temps_aleatoire = time.time() - debut
    resultats['methodes']['heuristique_aleatoire'] = {
        'cout_total': solution_aleatoire['cout_total'],
        'longueur_cycle': solution_aleatoire['longueur_cycle'],
        'cout_affectation': solution_aleatoire['cout_affectation'],
        'temps': temps_aleatoire,
        'stations': solution_aleatoire['stations']
    }
    print(f"   Coût total : {solution_aleatoire['cout_total']:.2f}")
    print(f"   Temps : {temps_aleatoire:.2f} secondes\n")
    
    # 3. Métaheuristique (recuit simulé)
    print("3. Métaheuristique (recuit simulé)...")
    debut = time.time()
    solution_recuit = recuit_simule(
        points, solution_grille, distances, alpha=alpha,
        temperature_initiale=1000.0,
        temperature_finale=0.1,
        facteur_refroidissement=0.95,
        iterations_par_temperature=10
    )
    temps_recuit = time.time() - debut
    resultats['methodes']['recuit_simule'] = {
        'cout_total': solution_recuit['cout_total'],
        'longueur_cycle': solution_recuit['longueur_cycle'],
        'cout_affectation': solution_recuit['cout_affectation'],
        'temps': temps_recuit,
        'stations': solution_recuit['stations']
    }
    print(f"   Coût total : {solution_recuit['cout_total']:.2f}")
    print(f"   Temps : {temps_recuit:.2f} secondes\n")
    
    # 4. PLNE (seulement pour petites instances)
    if tester_plne and n <= 15:
        print("4. PLNE (résolution exacte)...")
        debut = time.time()
        solution_plne = resoudre_plne(points, p, alpha=alpha, timeout=300)
        temps_plne = time.time() - debut
        
        if solution_plne is not None:
            resultats['methodes']['plne'] = {
                'cout_total': solution_plne['cout_total'],
                'longueur_cycle': solution_plne['longueur_cycle'],
                'cout_affectation': solution_plne['cout_affectation'],
                'temps': temps_plne,
                'stations': solution_plne['stations'],
                'statut': solution_plne.get('statut', 'Inconnu'),
                'borne_inf': solution_plne.get('borne_inf', None)
            }
            print(f"   Coût total : {solution_plne['cout_total']:.2f}")
            print(f"   Temps : {temps_plne:.2f} secondes")
            if 'borne_inf' in solution_plne and solution_plne['borne_inf'] is not None:
                print(f"   Borne inférieure : {solution_plne['borne_inf']:.2f}")
            print()
        else:
            resultats['methodes']['plne'] = {
                'cout_total': None,
                'temps': temps_plne,
                'statut': 'Non résolu'
            }
            print("   Non résolu dans le temps imparti\n")
    elif tester_plne:
        print("4. PLNE : Instance trop grande (n > 15), non testée\n")
        resultats['methodes']['plne'] = {
            'cout_total': None,
            'temps': None,
            'statut': 'Instance trop grande'
        }
    
    return resultats


def sauvegarder_resultats(resultats, chemin_fichier='resultats/resultats.txt'):
    """
    Sauvegarde les résultats dans un fichier texte.
    
    Format lisible pour le rapport avec tableaux comparatifs.
    
    Args:
        resultats: Dictionnaire de résultats créé par comparer_methodes
        chemin_fichier: Chemin où sauvegarder les résultats
    """
    with open(chemin_fichier, 'a', encoding='utf-8') as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"INSTANCE : {resultats['instance']}\n")
        f.write(f"Nombre de points : {resultats['nombre_points']}\n")
        f.write(f"Nombre de stations : {resultats['nombre_stations']}\n")
        f.write(f"Alpha : {resultats['alpha']}\n")
        f.write("="*80 + "\n\n")
        
        # Tableau comparatif
        f.write("TABLEAU COMPARATIF\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Méthode':<30} {'Coût total':<15} {'Temps (s)':<15} {'Longueur cycle':<15}\n")
        f.write("-"*80 + "\n")
        
        for nom_methode, donnees in resultats['methodes'].items():
            if donnees.get('cout_total') is not None:
                cout = f"{donnees['cout_total']:.2f}"
                temps = f"{donnees['temps']:.2f}"
                longueur = f"{donnees.get('longueur_cycle', 'N/A'):.2f}" if 'longueur_cycle' in donnees else "N/A"
                f.write(f"{nom_methode:<30} {cout:<15} {temps:<15} {longueur:<15}\n")
            else:
                f.write(f"{nom_methode:<30} {'N/A':<15} {donnees.get('temps', 'N/A'):<15} {'N/A':<15}\n")
        
        f.write("-"*80 + "\n\n")
        
        # Détails par méthode
        f.write("DÉTAILS PAR MÉTHODE\n")
        f.write("-"*80 + "\n")
        
        for nom_methode, donnees in resultats['methodes'].items():
            f.write(f"\n{nom_methode.upper()}\n")
            f.write(f"  Coût total : {donnees.get('cout_total', 'N/A')}\n")
            f.write(f"  Longueur du cycle : {donnees.get('longueur_cycle', 'N/A')}\n")
            f.write(f"  Coût d'affectation : {donnees.get('cout_affectation', 'N/A')}\n")
            f.write(f"  Temps de calcul : {donnees.get('temps', 'N/A')} secondes\n")
            if 'statut' in donnees:
                f.write(f"  Statut : {donnees['statut']}\n")
            if 'borne_inf' in donnees and donnees['borne_inf'] is not None:
                f.write(f"  Borne inférieure : {donnees['borne_inf']:.2f}\n")
            if 'stations' in donnees:
                f.write(f"  Stations : {donnees['stations']}\n")
        
        f.write("\n" + "="*80 + "\n\n")


def analyser_resultats(resultats):
    """
    Analyse les résultats et retourne des statistiques comparatives.
    
    Utile pour générer des tableaux dans le rapport.
    
    Args:
        resultats: Dictionnaire de résultats
        
    Returns:
        Dictionnaire d'analyse
    """
    analyse = {
        'meilleur_cout': float('inf'),
        'meilleure_methode': None,
        'plus_rapide': float('inf'),
        'methode_plus_rapide': None,
        'comparaisons': {}
    }
    
    # Recherche de la meilleure solution
    for nom_methode, donnees in resultats['methodes'].items():
        if donnees.get('cout_total') is not None:
            if donnees['cout_total'] < analyse['meilleur_cout']:
                analyse['meilleur_cout'] = donnees['cout_total']
                analyse['meilleure_methode'] = nom_methode
            
            if donnees.get('temps') is not None and donnees['temps'] < analyse['plus_rapide']:
                analyse['plus_rapide'] = donnees['temps']
                analyse['methode_plus_rapide'] = nom_methode
    
    # Calcul des écarts relatifs
    if analyse['meilleur_cout'] != float('inf'):
        for nom_methode, donnees in resultats['methodes'].items():
            if donnees.get('cout_total') is not None:
                ecart = ((donnees['cout_total'] - analyse['meilleur_cout']) / analyse['meilleur_cout']) * 100
                analyse['comparaisons'][nom_methode] = {
                    'ecart_pourcentage': ecart,
                    'ratio_temps': donnees.get('temps', 0) / analyse['plus_rapide'] if analyse['plus_rapide'] > 0 else 0
                }
    
    return analyse


def generer_tableau_comparatif(resultats_liste):
    """
    Génère un tableau comparatif pour plusieurs instances.
    
    Utile pour le rapport avec plusieurs tests.
    
    Args:
        resultats_liste: Liste de dictionnaires de résultats
        
    Returns:
        Chaîne de caractères formatée en tableau
    """
    tableau = "\nTABLEAU COMPARATIF MULTI-INSTANCES\n"
    tableau += "="*100 + "\n"
    
    # En-tête
    tableau += f"{'Instance':<20} {'Points':<10} {'Méthode':<25} {'Coût':<15} {'Temps (s)':<15}\n"
    tableau += "-"*100 + "\n"
    
    # Données
    for resultats in resultats_liste:
        instance = resultats['instance'].split('/')[-1]  # Nom du fichier seulement
        n = resultats['nombre_points']
        
        for nom_methode, donnees in resultats['methodes'].items():
            if donnees.get('cout_total') is not None:
                cout = f"{donnees['cout_total']:.2f}"
                temps = f"{donnees['temps']:.2f}"
                tableau += f"{instance:<20} {n:<10} {nom_methode:<25} {cout:<15} {temps:<15}\n"
    
    tableau += "="*100 + "\n"
    
    return tableau
