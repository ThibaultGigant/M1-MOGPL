from Robot.classes import *
import time
"""

"""


def get_grilles(fichier_entree):
    """
        S'occupe d'ouvrir les fichiers, puis récupérer les grilles sans les résoudre
        :param fichier_entree: fichier où récupérer les données
        :type fichier_entree: str
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
    temps_calcul = []
    chemins = []
    for robot in robots:
        t1 = time.time()
        chemin = robot.affiche_resultat()
        temps_calcul.append(time.time()-t1)
        chemins.append(chemin)
    return chemins, temps_calcul


def ecriture(chemins, fichier_sortie):
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
    """
    grilles = get_grilles(fichier_entree)

    robots, temps_creation = creation_robots(grilles)
    chemins, temps_calcul = lancement_depuis_robots(robots)

    ecriture(chemins, fichier_sortie)

    # print("Moyenne de temps de création", sum(temps_creation)/len(temps_creation))
    # print("Moyenne de temps de calcul", sum(temps_calcul)/len(temps_calcul))
    return chemins, temps_creation, temps_calcul
