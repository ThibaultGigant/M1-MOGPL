from Interface.ihm import affichage_fenetre
from Robot.file_gestion import lecture
import os


"""
Fichier d'entrée dans le programme : Il suffit de taper dans la console "python3 run.py" pour lancer le programme
"""


def lancer_algo_sur_repertoire():
    """
    Lance l'algorithme sur tous les fichiers du répertoire "Instances"
    et stocke les résultats dans des fichiers du répertoire "Instances/Res"
    Lancez ce programme si vous voulez lancer sur une base de tests
    """
    base = [i for i in os.listdir("Instances") if i[-4:] == ".dat"]
    for i in base:
        print(i)
        lecture("Instances/" + i, "Instances/Res/" + i[:-4] + ".out.dat")


if __name__ == "__main__":
    affichage_fenetre()
