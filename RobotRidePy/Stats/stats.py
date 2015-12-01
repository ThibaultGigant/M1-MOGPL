# -*- coding: utf-8 -*-
from Generation.generation import generer_grille
from Robot.file_gestion import lancement_depuis_grille, get_grilles
import numpy as np


def temps_execution(nb_lignes, nb_obstacles):
    """
    Génère plusieurs instances de grilles carrées de côté nb_lignes, avec nb_obstacles
    puis calcule le temps moyen d'exécution (création du graphe et calcul du chemin séparément) de l'algorithme
    avant de le retourner
    :param nb_lignes: nombre de lignes et de colonnes des grilles à créer
    :param nb_obstacles: nombre d'obstacles dans les grilles à créer
    :type nb_lignes: int
    :type nb_obstacles: int
    :return: temps moyen de création des graphes et temps moyen de calcul du chemin le plus rapide
    """
    temps_creation = []
    temps_calcul = []
    for i in range(50):
        grille = generer_grille(nb_lignes, nb_lignes, nb_obstacles)  # génération des grilles
        tps1, tps2 = lancement_depuis_grille(grille)  # Récupération du temps d'exécution
        temps_creation += tps1
        temps_calcul += tps2
    return np.mean(temps_creation), np.mean(temps_calcul)


def affiche_stats_taille(min_taille, max_taille, pas, plt):
    """
    Modification de l'objet matplotlib (graphique) qui représentera les temps d'exécution
    en fonction de la taille de la grille de départ
    :param min_taille: taille minimale des grilles
    :param max_taille: taille maximale des grilles
    :param pas: pas de taille entre deux grilles
    :param plt: objet matplotlib (plot) qui sera affiché
    :type min_taille: int
    :type max_taille: int
    :type pas: int
    :type plt: subplot (matplotlib)
    """
    temps_creation = []
    temps_calcul = []
    # Création de l'axe des abscisses, avec les tailles espacées par le pas
    tab_nb_lignes = np.arange(min_taille, max_taille+1, pas, dtype=int)
    # Récupération des temps d'exécution sur des grilles aléatoires via l'appel à temps_execution
    for i in tab_nb_lignes:
        tps1, tps2 = temps_execution(i, i)
        temps_creation.append(tps1)
        temps_calcul.append(tps2)
    temps_creation = np.array(temps_creation)
    temps_calcul = np.array(temps_calcul)
    # Ajout des courbes les unes après les autres, ainsi que de la légende
    plt.plot(tab_nb_lignes, temps_creation, 'g^--', label="Temps de création du graphe")
    plt.plot(tab_nb_lignes, temps_calcul, 'bs--', label="Temps de calcul du chemin")
    plt.plot(tab_nb_lignes, temps_creation + temps_calcul, 'ro-', label="Temps total")
    plt.legend(loc='best')


def affiche_stats_obstacles(nb_lignes, max_obstacles, pas, plt):
    """
    Modification de l'objet matplotlib (graphique) qui représentera les temps d'exécution
    en fonction du nombre d'obstacles de la grille
    :param nb_lignes: nombre de lignes et de colonnes des grilles à générer et à étudier
    :param max_obstacles: nombre d'obstacles maximum dans les instances à générer
    :param pas: pas entre deux nombre d'obstacles dans les instances à générer
    :param plt: objet matplotlib (plot) qui sera affiché
    :type nb_lignes: int
    :type max_obstacles: int
    :type pas: int
    :type plt: subplot (matplotlib)
    :return:
    """
    temps_creation = []
    temps_calcul = []
    # Création de l'axe des abscisses, avec les tailles espacées par le pas
    tab_nb_obstacles = np.arange(nb_lignes, max_obstacles+1, pas, dtype=int)
    # Récupération des temps d'exécution sur des grilles aléatoires via l'appel à temps_execution
    for i in tab_nb_obstacles:
        tps1, tps2 = temps_execution(nb_lignes, i)
        temps_creation.append(tps1)
        temps_calcul.append(tps2)
    temps_creation = np.array(temps_creation)
    temps_calcul = np.array(temps_calcul)
    # Ajout des courbes les unes après les autres, ainsi que de la légende
    plt.plot(tab_nb_obstacles, temps_creation, 'g^--', label="Temps de création du graphe")
    plt.plot(tab_nb_obstacles, temps_calcul, 'bs--', label="Temps de calcul du chemin")
    plt.plot(tab_nb_obstacles, temps_creation + temps_calcul, 'ro-', label="Temps total")
    plt.legend(loc='best')


def recup_stats_fichier_taille(fichier):
    """
    Calcule les statistiques de temps d'exécution du fichier en fonction de la taille des grilles
    :param fichier: chemin du fichier où récupérer les instances
    :type fichier: str
    """
    grilles = get_grilles(fichier)
    # On crée un dictionnaire qui aura pour clé la taille de la grille et pour valeur une liste de 2 éléments :
    #   - une liste des temps de création du graphe des grilles de cette taille
    #   - une liste des temps de calcul du chemin le plus rapide pour les grilles de cette taille
    donnees = {}

    # Récupération des données des grilles
    for grille in grilles:
        taille = grille[0][0]
        if taille not in donnees.keys():
            donnees[taille] = [[], []]
        creat, calc = lancement_depuis_grille(grille)
        donnees[taille][0].append(creat)
        donnees[taille][1].append(calc)

    # calcul des moyennes et stockage dans des tableaux pour affichage
    tailles = []
    tps_creation = []
    tps_calcul = []
    for i, j in sorted(donnees.items(), key=lambda colonnes: colonnes[0]):
        tailles.append(i)
        tps_creation.append(np.mean(j[0]))
        tps_calcul.append(np.mean(j[1]))
    return np.array(tailles), np.array(tps_creation), np.array(tps_calcul)


def get_nb_obstacles(grille):
    """
    Compte le nombre d'obstacles dans les lignes de la grille
    :param grille: grille représentant le dépôt, dont l'élément d'indice 1 est la liste de listes de '0' et de '1'
    :type: list
    :return: nombre d'obstacles dans la grille
    :rtype: int
    """
    nb_obstacles = 0
    for ligne in grille[1]:
        nb_obstacles += ligne.count('1')
    return nb_obstacles


def recup_stats_fichier_obstacles(fichier):
    """
    Calcule les statistiques de temps d'exécution du fichier
    en fonction du nombre d'obstacles dans les grilles du fichier
    :param fichier: chemin du fichier où récupérer les instances
    :type fichier: str
    """
    grilles = get_grilles(fichier)
    taille = grilles[0][0][0]
    # On crée un dictionnaire qui aura pour clé le nombre d'obstacles de la grille
    # et pour valeur une liste de 2 éléments :
    #   - une liste des temps de création du graphe des grilles de cette taille
    #   - une liste des temps de calcul du chemin le plus rapide pour les grilles de cette taille
    donnees = {}

    # Récupération des données des grilles
    for grille in grilles:
        nb_obstacles = get_nb_obstacles(grille)
        if nb_obstacles not in donnees.keys():
            donnees[nb_obstacles] = [[], []]
        creat, calc = lancement_depuis_grille(grille)
        donnees[nb_obstacles][0].append(creat)
        donnees[nb_obstacles][1].append(calc)


    # calcul des moyennes et stockage dans des tableaux pour affichage
    nb_obstacles = []
    tps_creation = []
    tps_calcul = []
    for i, j in sorted(donnees.items(), key=lambda colonnes: colonnes[0]):
        nb_obstacles.append(i)
        tps_creation.append(np.mean(j[0]))
        tps_calcul.append(np.mean(j[1]))
    return taille, np.array(nb_obstacles), np.array(tps_creation), np.array(tps_calcul)


def affiche_stats_fichier(donnees, tps_creation, tps_calcul, plt):
    """
    Modification de l'objet matplotlib (graphique) <plt> affichant les temps d'exécution des instances de grilles
    en fonction des données passées en paramètre
    :param donnees: np.array des tailles des grilles
    :param tps_creation: np.array des temps de création correspondant aux tailles
    :param tps_calcul: np.array des temps de calcul du chemin correspondant aux tailles
    :param plt: objet matplotlib (plot) qui sera affiché
    :type donnees: np.array
    :type tps_creation: np.array
    :type tps_calcul: np.array
    :type plt: subplot (matplotlib)
    """

    # Ajout des courbes les unes après les autres, ainsi que de la légende
    plt.plot(donnees, tps_creation, 'g^--', label="Temps de création du graphe")
    plt.plot(donnees, tps_calcul, 'bs--', label="Temps de calcul du chemin")
    plt.plot(donnees, tps_creation + tps_calcul, 'ro-', label="Temps total")
    plt.legend(loc='best')