from Robot.classes import *
import time
"""

"""


def lecture(fichier_entree, fichier_sortie):
    """
        S'occupe d'ouvrir les fichiers, récupérer les données des problèmes et les appliquer
        :param fichier_entree: fichier où récupérer les données
        :param fichier_sortie: fichier où écrire le résultat des calculs
        :type fichier_entree: str
        :type fichier_sortie: str
    """
    fp = open(fichier_entree, "r")

    robots = []
    temps_creation = []
    temps_calcul = []

    ligne = fp.readline()
    while ligne:
        nb_lignes, nb_colonnes = map(int, ligne.split())  # Récupération du nombre de lignes et de colonnes
        lignes = []
        for i in range(nb_lignes):
            lignes.append(fp.readline().split())
        t1 = time.time()
        graphe = Graph(nb_lignes, nb_colonnes, lignes)
        temps_creation.append(time.time()-t1)
        robots.append(Robot(fp.readline().split(), graphe))
        ligne = fp.readline()
        if ligne == "0 0":
            break
        else:
            ligne = fp.readline()

    fp.close()
    fp = open(fichier_sortie, "w")
    retour = []
    for robot in robots:
        t1 = time.time()
        res = robot.affiche_resultat()
        temps_calcul.append(time.time()-t1)
        fp.write(res + "\n")
        retour.append(res)

    fp.close()
    return retour, temps_creation, temps_calcul
