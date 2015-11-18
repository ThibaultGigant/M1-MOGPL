from enum import Enum

"""
Fichier regroupant les classes nécessaires à l'exécution du programme
"""

HelpMessage = "Le fichier d'entrée doit correspondre aux données de l'énoncé"


class Orientation(Enum):
    """
        Classe énumérant les orientations possibles
    """
    nord = 0
    est = 1
    sud = 2
    ouest = 3


class Node:
    """
        Classe décrivant les noeuds, c'est à dire les croisements avec orientation
    """

    def __init__(self, x, y, orientation):
        self.x = x  # représente la ligne sur laquelle se trouve le noeud
        self.y = y  # représente la colonne sur laquelle se trouve le noeud
        self.orientation = orientation
        self.adjacents = []  # Donne tous les sommets adjacents à ce sommet,
        # c'est à dire les sommets que le robot peut atteindre en 1 seconde à partir de celui-ci
        self.pere = -1  # Donne le père du noeud dans le chemin obtenu par le parcours en largeur

    def ajoute_adjacent(self, sommet):
        self.adjacents.append(sommet)

    def set_pere(self, pere):
        self.pere = pere


class Graph:
    """
        Classe décrivant le graphe associé à un problème
    """

    def __init__(self, nb_lignes, nb_colonnes, lignes):
        # Le buffer représente les lignes de 0 et 1 sous la forme d'une liste de listes
        # où chaque liste correspond à une ligne du fichier d'entrée
        self.sommets = {}  # Ensemble des sommets
        # les clés seront les tuples (x,y,orientation) et les valeurs le noeud correspondant
        self.remplir_sommets(nb_lignes, nb_colonnes, lignes)

    def remplir_sommets(self, nb_lignes, nb_colonnes, lignes):
        """
            Remplissage Complet du graphe lors de l'initialisation,
            on supprimera les arcs inutilisables par le robot plus tard

            :param nb_lignes: Nombre de lignes de 1m du dépôt
            :param nb_colonnes: Nombres de colonnes de 1m du dépôt
            :param lignes: liste de listes, chacune représentant une ligne du dépôt
            :type nb_lignes: int
            :type nb_colonnes: int
            :type lignes: list
        """

    def ajoute_premiere_ligne(self, nb_lignes, nb_colonnes, lignes):
        # ajout premier élément
        if lignes[0][0] == '0':
            for k in range(4):
                self.sommets[(0, 0, Orientation(k))] = Node(0, 0, Orientation(k))
        # ajout éléments intermédiaires
        for i in range(1, nb_colonnes):
            if lignes[0][i] == '0':
                if (lignes[0][i-1]) == '0':
                    self.sommets[(0, i, Orientation.ouest)] = Node(0,i,Orientation.ouest)
                    if i < nb_colonnes-1:
                        if lignes[0][i+1] == '0':
                            self.sommets[(0, i, Orientation.est)] = Node(0,i, Orientation.est)
                    else:
                        self.sommets[(0, i, Orientation.est)] = Node(0,i, Orientation.est)
                    if nb_lignes >= 2:
                        if lignes[1][i-1] == '0' and lignes[1][i] == '0':
                            self.sommets[(0, i, Orientation.sud)] = Node(0,i, Orientation.sud)
        # ajout du dernier élément
        if lignes[0][-1] == '0':
            if nb_colonnes >= 2:
                if lignes[0][-2] == '0':
                    self.sommets[(0, nb_colonnes+1, Orientation.ouest)] = Node(0, nb_colonnes+1, Orientation.ouest)
            else:
                self.sommets[(0, nb_colonnes+1, Orientation.ouest)] = Node(0, nb_colonnes+1, Orientation.ouest)
            if nb_lignes >= 2:
                if lignes[1][nb_colonnes] == '0':
                    self.sommets[(0, nb_colonnes+1, Orientation.sud)] = Node(0, nb_colonnes+1, Orientation.sud)
            else:
                self.sommets[(0, nb_colonnes+1, Orientation.sud)] = Node(0, nb_colonnes+1, Orientation.sud)


    def get_sommet(self, x, y, orientation):
        """
            Retourne le sommet demandé en fonction de ses coordonnées et son orientation
            :param x: coordonnée de la ligne voulue
            :param y: coordonnée de la colonne voulue
            :param orientation: Orientation du sommet voulu
            :type x: int
            :type y: int
            :type orientation: Orientation
            :return: Sommet correspondant aux données
            :rtype: Node
        """
        return self.sommets[(x, y, orientation)]


class Robot:
    """
        Classe définissant le Robot avec sa position, sa direction et toutes les données nécessaires à l'algorithme
        Il portera les fonctions nécessaires à l'algorithme de parcours en largeur
    """

    def __init__(self, ligne, graphe):
        # initialisation du noeud de départ dans lequel se trouve le robot
        if ligne[-1] == "nord":
            orientation = Orientation.nord
        elif ligne[-1] == "est":
            orientation = Orientation.est
        elif ligne[-1] == "sud":
            orientation = Orientation.sud
        elif ligne[-1] == "ouest":
            orientation = Orientation.ouest
        else:
            exit(HelpMessage)

        self.depart = graphe.get_sommet(int(ligne[0]), int(ligne[1]), orientation)

        self.arrivee = (int(ligne[2]), int(ligne[3]))  # En revanche ici, l'orientation n'est pas précisée
        self.graphe = graphe
        self.visites = [self.depart]
        self.depart.pere = None
