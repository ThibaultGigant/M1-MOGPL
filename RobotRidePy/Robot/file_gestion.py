from Robot.classes import *
import time
"""

"""


def lecture(fichier_entree, fichier_sortie):
    fp = open(fichier_entree, "r")
    fo = open(fichier_sortie, "w")

    ligne = fp.readline()
    while ligne:
        t1 = time.time()
        nb_lignes, nb_colonnes = map(int, ligne.split())  # Récupération du nombre de lignes et de colonnes
        lignes = []
        for i in range(nb_lignes):
            lignes.append(fp.readline().split())
        graphe = Graph(nb_lignes, nb_colonnes, lignes)
        t2 = time.time()
        print("Tremps pris pour la création du graphe : ", t2-t1)
        robot = Robot(fp.readline().split(), graphe)
        # print("Graphe de taille : ", nb_lignes, nb_colonnes)
        # print("Robot part de : ", robot.depart.x, robot.depart.y)
        # print("Robot arrive à : ", robot.arrivee[0], robot.arrivee[1])
        # graphe.affiche_graphe()
        fo.write(robot.affiche_resultat() + "\n")
        print("Temps de calcul: ", time.time()-t2, " secondes")
        print("Temps total : ", time.time()-t1)
        ligne = fp.readline()
        if ligne == "0 0":
            break
        else:
            ligne = fp.readline()

    fp.close()
    fo.close()
