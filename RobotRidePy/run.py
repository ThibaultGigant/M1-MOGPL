from Interface.ihm import affichage_fenetre
from Robot.file_gestion import lecture
import os


def lancer_algo_sur_repertoire():
    base = [i for i in os.listdir("Instances") if i[-4:] == ".dat"]
    for i in base:
        print(i)
        lecture("Instances/" + i, "Instances/Res/" + i[:-4] + ".out.dat")


def lancement_basique():
    lecture("Instances/x9y10o10.dat", "Instances/Résultats/x9y10o10out.dat")


if __name__ == "__main__":
    affichage_fenetre()
    # lancement_basique()
