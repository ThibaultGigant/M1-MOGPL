import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
from Generation.generation import generer_grille
from Robot.file_gestion import lancement_depuis_grille
import numpy as np


def temps_execution_sur_nb_lignes(nb_lignes, nb_obstacles):
    temps_creation = []
    temps_calcul = []
    for i in range(50):
        grille = generer_grille(nb_lignes, nb_lignes, nb_obstacles)
        tps1, tps2 = lancement_depuis_grille(grille)
        temps_creation += tps1
        temps_calcul += tps2
    return np.mean(temps_creation), np.mean(temps_calcul)


def affiche_stats_noeuds():
    temps_creation = []
    temps_calcul = []
    tab_nb_lignes = np.linspace(10, 100, 10)  # crée un array de 10 à 100 avec 10,20,30,40,etc...
    for i in tab_nb_lignes:
        tps1, tps2 = temps_execution_sur_nb_lignes(int(i), int(i))
        temps_creation.append(tps1)
        temps_calcul.append(tps2)
    temps_creation = np.array(temps_creation)
    temps_calcul = np.array(temps_calcul)
    print(tab_nb_lignes)
    print(temps_creation)
    print(temps_calcul)
    plt.plot(tab_nb_lignes, temps_creation, 'r--',
             tab_nb_lignes, temps_calcul, 'bs',
             tab_nb_lignes, temps_creation + temps_calcul, 'g^')
    plt.show()


def affiche_stats_obstacles(nb_lignes, max_obstacles, nb_intervalles):
    temps_creation = []
    temps_calcul = []
    tab_nb_obstacles = np.linspace(nb_lignes, max_obstacles, nb_intervalles)  # crée un array de 10 à 100 avec 10,20,30,40,etc...
    for i in tab_nb_obstacles:
        tps1, tps2 = temps_execution_sur_nb_lignes(nb_lignes, int(i))
        temps_creation.append(tps1)
        temps_calcul.append(tps2)
    temps_creation = np.array(temps_creation)
    temps_calcul = np.array(temps_calcul)
    print(tab_nb_obstacles)
    print(temps_creation)
    print(temps_calcul)
    plt.plot(tab_nb_obstacles, temps_creation, 'r--',
             tab_nb_obstacles, temps_calcul, 'bs',
             tab_nb_obstacles, temps_creation + temps_calcul, 'g^')
    plt.show()


affiche_stats_obstacles(20, 100, 9)