# -*- coding: utf-8 -*-
from Interface.ihm import affichage_fenetre
from Robot.file_gestion import lecture
import os


"""
Fichier d'entrée dans le programme : Il suffit de taper dans la console "python3 run.py" pour lancer le programme
"""


def lancer_algo_sur_repertoire(repertoire_entree, repertoire_sortie):
    """
    Lance l'algorithme sur tous les fichiers du répertoire "Instances"
    et stocke les résultats dans des fichiers du répertoire "Instances/Res"
    Lancez ce programme si vous voulez lancer sur une base de tests
    :param repertoire_entree: répertoire où récupérer tous les fichiers à faire tourner
    :param repertoire_sortie: répertoire où stocker tous les fichiers de sortie
    """
    base = [i for i in os.listdir(repertoire_entree) if i[-4:] == ".dat"]
    for i in base:
        lecture(repertoire_entree + i, repertoire_sortie + i[:-4] + ".out.dat")


if __name__ == "__main__":
    affichage_fenetre()
