from Robot.classes import *
"""

"""


def lecture(fichier_entree, fichier_sortie):
    fp = open(fichier_entree, "r")
    fo = open(fichier_sortie, "w")

    ligne = fp.readline()
    while ligne:
        nb_lignes, nb_colonnes = ligne.split()
        nb_lignes = int(nb_lignes)
        nb_colonnes = int(nb_colonnes)
        lignes = []
        for i in range(nb_lignes):
            lignes.append(fp.readline().split())
        graphe = Graph(nb_lignes, nb_colonnes, lignes)
        robot = Robot(fp.readline().split(), graphe)
        fo.write(robot.affiche_resultat())
        ligne = fp.readline()
        if ligne == "0 0":
            break
        else:
            ligne = fp.readline()

    fp.close()
    fo.close()
