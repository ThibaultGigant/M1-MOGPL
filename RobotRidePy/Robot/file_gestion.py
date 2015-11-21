from Robot.classes import *
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

    ligne = fp.readline()
    while ligne:
        nb_lignes, nb_colonnes = map(int, ligne.split())  # Récupération du nombre de lignes et de colonnes
        lignes = []
        for i in range(nb_lignes):
            lignes.append(fp.readline().split())
        graphe = Graph(nb_lignes, nb_colonnes, lignes)
        robots.append(Robot(fp.readline().split(), graphe))
        ligne = fp.readline()
        if ligne == "0 0":
            break
        else:
            ligne = fp.readline()

    fp.close()
    fp = open(fichier_sortie, "w")
    for robot in robots:
        fp.write(robot.affiche_resultat() + "\n")

    fp.close()
