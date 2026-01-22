# Makefile pour le projet d'optimisation combinatoire
# Problème de l'anneau-étoile
#
# Ce Makefile facilite l'exécution du projet et garantit la reproductibilité
# des expérimentations. Toutes les commandes sont simples et claires.

# Variable pour Python (peut être python3 selon le système)
PYTHON = python

# Variable pour le fichier d'instance par défaut
INSTANCE = donnees/tsplib/att48.tsp

# Nombre de stations par défaut
P = 5

# Coefficient alpha par défaut
ALPHA = 0.5

# Règle par défaut : affiche l'aide
.DEFAULT_GOAL := help

# Règle help : affiche les commandes disponibles
.PHONY: help
help:
	@echo "Makefile pour le projet anneau-étoile"
	@echo ""
	@echo "Commandes disponibles :"
	@echo "  make install    - Installe les dépendances Python"
	@echo "  make run         - Lance une comparaison avec l'instance par défaut"
	@echo "  make figures     - Génère les figures des instances et solutions"
	@echo "  make clean       - Nettoie les fichiers générés"
	@echo "  make test        - Lance un test rapide"
	@echo ""
	@echo "Pour utiliser une autre instance :"
	@echo "  make run INSTANCE=donnees/tsplib/nom_instance.tsp P=5 ALPHA=0.5"
	@echo ""
	@echo "Pour lister toutes les instances disponibles :"
	@echo "  python src/liste_instances.py"
	@echo ""
	@echo "Variables (modifiables) :"
	@echo "  INSTANCE=$(INSTANCE)"
	@echo "  P=$(P)"
	@echo "  ALPHA=$(ALPHA)"

# Règle install : installe les dépendances Python
# Utilise pip pour installer les packages listés dans requirements.txt
.PHONY: install
install:
	@echo "Installation des dépendances..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Installation terminée."

# Règle run : lance le programme principal
# Exécute les comparaisons expérimentales avec les paramètres par défaut
# Les résultats sont sauvegardés dans resultats/resultats.txt
.PHONY: run
run:
	@echo "Lancement des comparaisons expérimentales..."
	@echo "Instance : $(INSTANCE)"
	@echo "Nombre de stations : $(P)"
	@echo "Alpha : $(ALPHA)"
	@echo ""
	@if [ ! -f $(INSTANCE) ]; then \
		echo "Erreur : le fichier $(INSTANCE) n'existe pas."; \
		echo "Veuillez utiliser un fichier .tsp depuis donnees/tsplib/"; \
		exit 1; \
	fi
	$(PYTHON) src/main.py $(INSTANCE) $(P) $(ALPHA)
	@echo ""
	@echo "Résultats sauvegardés dans resultats/resultats.txt"

# Règle test : lance un test rapide sur une petite instance
# Utile pour vérifier que tout fonctionne correctement
.PHONY: test
test:
	@echo "Test rapide..."
	@echo "Vérification de l'installation..."
	$(PYTHON) -c "import numpy, matplotlib, pulp; print('Dépendances OK')"
	@echo "Test terminé."

# Règle figures : génère automatiquement les figures
# Crée les visualisations des instances et des solutions
# Les figures sont sauvegardées dans resultats/figures/
.PHONY: figures
figures:
	@echo "Génération des figures..."
	$(PYTHON) src/generer_figures.py
	@echo "Figures générées dans resultats/figures/"

# Règle clean : nettoie les fichiers générés
# Supprime les résultats et les figures générées
# Ne supprime pas les données d'entrée ni le code source
.PHONY: clean
clean:
	@echo "Nettoyage des fichiers générés..."
	@if [ -f resultats/resultats.txt ]; then \
		rm resultats/resultats.txt; \
		echo "  - resultats/resultats.txt supprimé"; \
	fi
	@if [ -d resultats/figures ]; then \
		rm -f resultats/figures/*.png resultats/figures/*.jpg; \
		echo "  - Figures supprimées"; \
	fi
	@echo "Nettoyage terminé."

# Règle clean-all : nettoie tout (y compris les fichiers Python compilés)
.PHONY: clean-all
clean-all: clean
	@echo "Nettoyage complet..."
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Nettoyage complet terminé."
