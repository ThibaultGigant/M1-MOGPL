from Generation.generation import generer_grille
from Robot.file_gestion import lancement_depuis_grille
import numpy as np


def temps_execution(nb_lignes, nb_obstacles):
    temps_creation = []
    temps_calcul = []
    for i in range(50):
        grille = generer_grille(nb_lignes, nb_lignes, nb_obstacles)
        tps1, tps2 = lancement_depuis_grille(grille)
        temps_creation += tps1
        temps_calcul += tps2
    return np.mean(temps_creation), np.mean(temps_calcul)


def affiche_stats_taille(min_taille, max_taille, pas, plt):
    temps_creation = []
    temps_calcul = []
    tab_nb_lignes = np.arange(min_taille, max_taille+1, pas, dtype=int)
    for i in tab_nb_lignes:
        tps1, tps2 = temps_execution(i, i)
        temps_creation.append(tps1)
        temps_calcul.append(tps2)
    temps_creation = np.array(temps_creation)
    temps_calcul = np.array(temps_calcul)
    plt.plot(tab_nb_lignes, temps_creation, 'g^--', label="Temps de création du graphe")
    plt.plot(tab_nb_lignes, temps_calcul, 'bs--', label="Temps de calcul du chemin")
    plt.plot(tab_nb_lignes, temps_creation + temps_calcul, 'ro-', label="Temps total")
    plt.legend(loc='best')


def affiche_stats_obstacles(nb_lignes, max_obstacles, pas, plt):
    temps_creation = []
    temps_calcul = []
    tab_nb_obstacles = np.arange(nb_lignes, max_obstacles+1, pas, dtype=int)
    for i in tab_nb_obstacles:
        tps1, tps2 = temps_execution(nb_lignes, i)
        temps_creation.append(tps1)
        temps_calcul.append(tps2)
    temps_creation = np.array(temps_creation)
    temps_calcul = np.array(temps_calcul)
    plt.plot(tab_nb_obstacles, temps_creation, 'g^--', label="Temps de création du graphe")
    plt.plot(tab_nb_obstacles, temps_calcul, 'bs--', label="Temps de calcul du chemin")
    plt.plot(tab_nb_obstacles, temps_creation + temps_calcul, 'ro-', label="Temps total")
    plt.legend(loc='best')
