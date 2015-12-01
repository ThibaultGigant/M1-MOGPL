# -*- coding: utf-8 -*-
from Robot.classes import *
import time


def get_grilles(fichier_entree):
    """
    S'occupe d'ouvrir les fichiers, puis récupérer les grilles sans les résoudre
    :param fichier_entree: fichier où récupérer les données
    :type fichier_entree: str
    :return: Les grilles générées à partir des données du fichier d'entrée
    :rtype: list
    """
    grilles = []
    fp = open(fichier_entree, "r")
    ligne = fp.readline()
    while ligne:
        grille = []
        nb_lignes, nb_colonnes = map(int, ligne.split())  # Récupération du nombre de lignes et de colonnes
        grille.append((nb_lignes, nb_colonnes))
        lignes = []
        for i in range(nb_lignes):  # Récupération des lignes correspondant au dépôt
            lignes.append(fp.readline().split())
        grille.append(lignes)
        ligne = fp.readline().split()  # Récupération de la ligne correspondant au données liées au Robot
        grille.append(ligne)
        grilles.append(grille)
        # Vérification de la fin de problèmes
        ligne = fp.readline()
        if ligne == "0 0":
            break
        else:
            ligne = fp.readline()
    fp.close()
    return grilles


def creation_robots(grilles):
    """
    Crée tous les robots des grilles passées en paramètre
    :param grilles: liste de grilles récupérées d'un fichier
    :type grilles: list
    :return: liste des robots créés et la liste des temps pris pour la création des graphes correspondant à ces robots
    """
    temps_creation = []
    robots = []
    for grille in grilles:
        nb_lignes, nb_colonnes = grille[0]
        lignes = grille[1]
        donnees_robot = grille[2]
        t1 = time.time()
        graphe = Graph(nb_lignes, nb_colonnes, lignes)
        temps_creation.append(time.time()-t1)
        robots.append(Robot(donnees_robot, graphe))
    return robots, temps_creation


def lancement_depuis_robots(robots):
    """
    Calcule le chemin le plus rapide emprunté par chaque robot de la liste passée en paramètres
    :param robots: liste de robots
    :type robots: list
    :return: Liste des chemins les plus rapides correspondant à chaque robot de la liste
    """
    temps_calcul = []
    chemins = []
    for robot in robots:
        t1 = time.time()
        chemin = robot.affiche_resultat()
        temps_calcul.append(time.time()-t1)
        chemins.append(chemin)
    return chemins, temps_calcul


def lancement_depuis_grille(grille):
    """
    Génère le robot correspondant à la grille passée en paramètre, puis retourne le temps de création du graphe
    ainsi que le temps de calcul du chemin le plus rapide.
    Cette fonction sera surtout utilisée pour le calcul des statistiques
    :param grille: représente un dépôt avec ses données :
        - couple donnant le nombre de lignes et de colonnes
        - liste de listes de caractères 0 ou 1 représentant les lignes du dépôt
        - liste de caractères donnant les coordonées du robot au départ, à l'arrivée, et sa direction de départ
    :type grille: list
    :return: temps de création du graphe correspondant à la grille et temps de calcul du chemin le plus rapide
    """
    robots, temps_creation = creation_robots([grille])
    return temps_creation, lancement_depuis_robots(robots)[1]


def lancement_et_chemin(grille):
    """
    Génère le robot correspondant à la grille passée en paramètre,
    puis renvoie la liste des coordonnées des points empruntés par le robot dans son chemin le plus rapide
    :param grille: représente un dépôt avec ses données :
        - couple donnant le nombre de lignes et de colonnes
        - liste de listes de caractères 0 ou 1 représentant les lignes du dépôt
        - liste de caractères donnant les coordonées du robot au départ, à l'arrivée, et sa direction de départ
    :type grille: list
    :return: la liste des coordonnées des points empruntés par le robot dans son chemin le plus rapide
    :rtype: list
    """
    robots, temps_creation = creation_robots([grille])
    return robots[0].coordonnees_chemin()


def ecriture_chemins(chemins, fichier_sortie):
    """
    Ecrit le chemin passé en paramètre dans le fichier de sortie passé en paramètre
    :param chemins: liste de chaînes de caractères donnant les plus courts chemins d'un robot dans certaines grilles
    :param fichier_sortie: chemin absolu ou relatif du fichier de sortie où écrire les plus courts chemins
    :type chemins: list
    :type fichier_sortie: str
    """
    fp = open(fichier_sortie, "w")
    for chemin in chemins:
        fp.write(chemin + "\n")
    fp.close()


def lecture(fichier_entree, fichier_sortie):
    """
    S'occupe d'ouvrir les fichiers, récupérer les données des problèmes et les appliquer
    :param fichier_entree: fichier où récupérer les données
    :param fichier_sortie: fichier où écrire le résultat des calculs
    :type fichier_entree: str
    :type fichier_sortie: str
    :return: listes des chemins empruntés, des temps de création des graphes, et des temps de calcul
    """
    grilles = get_grilles(fichier_entree)

    robots, temps_creation = creation_robots(grilles)
    chemins, temps_calcul = lancement_depuis_robots(robots)

    ecriture_chemins(chemins, fichier_sortie)
    return chemins, temps_creation, temps_calcul


def ecriture_grilles(grilles, fichier_sortie):
    """
    Ecrit dans le fichier dont le chemin <fichier_sortie> est passé en paramètres les grilles contenues dans <grilles>
    :param grilles: liste de grilles à écrire dans le fichier
    :param fichier_sortie: chemin du fichier où écrire les grilles
    :type grilles: list
    :type fichier_sortie: str
    """
    fp = open(fichier_sortie, "w")
    # Ecriture de chaque grille
    for grille in grilles:
        # Ajout de la première ligne avec le nombre de lignes et colonnes
        fp.write(str(grille[0][0]) + " " + str(grille[0][1]) + "\n")
        for i in grille[1]:  # Ajout de chaque ligne du dépôt
            fp.write(" ".join(i) + "\n")
        fp.write(" ".join(grille[2]) + "\n")
        if grille != grilles[-1]:
            fp.write("\n")
        else:
            fp.write("0 0")
