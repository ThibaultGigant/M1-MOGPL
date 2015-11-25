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
        self.pere = None  # Donne le père du noeud dans le chemin obtenu par le parcours en largeur

    def ajoute_adjacent(self, sommet):
        """
            Ajoute un sommet à la liste d'adjacence du sommet courant
            :param sommet: sommet à ajouter
            :type sommet: Node
        """
        self.adjacents.append(sommet)

    def calculer_chemin_str(self):
        """
            Calcule le chemin pour arriver au sommet de départ du robot depuis le sommet courant
            :return: Chaine de caractère représentant le temps de parcours et le chemin emprunté par le robot
            :rtype: str
        """
        temps = 0
        res = ""
        n = self
        if n.pere is None:
            return "-1"
        while n.pere != -1:
            if n.pere.x == n.x and n.pere.y == n.y:
                if ((n.orientation.value - n.pere.orientation.value) % 4) == 1:
                    res = " D" + res
                else:
                    res = " G" + res
            elif n.pere.x == n.x:
                res = " a" + str(abs(n.pere.y - n.y)) + res
            else:
                res = " a" + str(abs(n.pere.x - n.x)) + res
            temps += 1
            n = n.pere
        return str(temps) + res

    def calculer_chemin_liste(self):
        """
            Calcule le chemin pour arriver au sommet de départ du robot depuis le sommet courant
            :return: liste de couples de coordonnées des points sur le chemin emprunté par le robot
            :rtype: list
        """
        n = self
        res = []
        if n.pere is None:
            return res
        while n.pere != -1:
            res.append((n.x, n.y))
            n = n.pere
        res.append((n.x, n.y))  # On ajoute aussi le point de départ, qui a le père qui vaut -1
        return res


class Graph:
    """
        Classe décrivant le graphe associé à un problème
    """

    def __init__(self, nb_lignes, nb_colonnes, lignes):
        # "lignes" représente les lignes de 0 et 1 sous la forme d'une liste de listes
        # où chaque liste correspond à une ligne du fichier d'entrée
        self.sommets = {}  # Ensemble des sommets
        # les clés seront les tuples (x,y,orientation) et les valeurs le noeud correspondant
        self.remplir_graphe(nb_lignes, nb_colonnes, lignes)
        self.lignes = lignes

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
        if (x, y, orientation) in self.sommets.keys():
            return self.sommets[(x, y, orientation)]
        else:
            return None

    def remplir_graphe(self, nb_lignes, nb_colonnes, lignes):
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
        # self.ajoute_premiere_ligne(nb_colonnes, lignes)
        # for i in range(1, nb_lignes):
        #     self.ajoute_ligne_intermediaire(i, nb_colonnes, lignes)
        # self.ajoute_derniere_ligne(nb_lignes, nb_colonnes, lignes)
        self.ajoute_sommets(nb_lignes, nb_colonnes, lignes)
        self.ajoute_arcs(nb_lignes, nb_colonnes)

    def ajoute_sommets(self, nb_lignes, nb_colonnes, lignes):
        """
            Crée tous les sommets du graphe, puis fait le tri pour supprimer ceux inaccessibles par le robot
            :param nb_lignes: nombre de lignes du dépôt
            :param nb_colonnes: nombre de colonnes du dépôt
            :param lignes: liste de listes, chacune représentant une ligne du dépôt
            :type nb_lignes: int
            :type nb_colonnes: int
            :type lignes: list
        """
        # Ajout de tous les sommets
        for i in range(nb_lignes+1):
            for j in range(nb_colonnes+1):
                for k in Orientation:
                    self.sommets[(i, j, k)] = Node(i, j, k)
        # Suppression des sommets inaccessibles à cause des objets
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                if lignes[i][j] == '1':
                    for k in Orientation:
                        if self.get_sommet(i, j, k):
                            del self.sommets[(i, j, k)]
                        if self.get_sommet(i+1, j, k):
                            del self.sommets[(i+1, j, k)]
                        if self.get_sommet(i, j+1, k):
                            del self.sommets[(i, j+1, k)]
                        if self.get_sommet(i+1, j+1, k):
                            del self.sommets[(i+1, j+1, k)]

    def ajoute_premiere_ligne(self, nb_colonnes, lignes):
        """
            Crée les sommets de la première "ligne" du graphe
            :param nb_colonnes: nombre de colonnes du dépôt
            :param lignes: liste de listes, chacune représentant une ligne du dépôt
            :type nb_colonnes: int
            :type lignes: list
        """
        # ajout premier élément
        if lignes[0][0] == '0':
            for k in Orientation:
                self.sommets[(0, 0, k)] = Node(0, 0, k)
        # ajout éléments intermédiaires
        for i in range(1, nb_colonnes):
            if lignes[0][i] == '0' and (lignes[0][i - 1]) == '0':
                for k in Orientation:
                    self.sommets[(0, i, k)] = Node(0, i, k)
        # ajout du dernier élément
        if lignes[0][-1] == '0':
            for k in Orientation:
                self.sommets[(0, nb_colonnes, k)] = Node(0, nb_colonnes, k)

    def ajoute_ligne_intermediaire(self, numero_ligne, nb_colonnes, lignes):
        """
            Crée les sommet d'une "ligne" intermédiaire du graphe
            :param numero_ligne: indice de la ligne à remplir
            :param nb_colonnes: nombre de colonnes du dépôt
            :param lignes: liste de listes, chacune représentant une ligne du dépôt
            :type numero_ligne: int
            :type nb_colonnes: int
            :type lignes: list
        """
        # ajout premier élément
        if lignes[numero_ligne][0] == '0' and lignes[numero_ligne - 1][0] == '0':
            for k in Orientation:
                self.sommets[(numero_ligne, 0, k)] = Node(numero_ligne, 0, k)
        # ajout éléments intermédiaires
        for i in range(1, nb_colonnes):
            if lignes[numero_ligne - 1][i - 1] == '0' and lignes[numero_ligne][i - 1] == '0' and \
                            lignes[numero_ligne - 1][i] == '0' and lignes[numero_ligne][i] == '0':
                for k in Orientation:
                    self.sommets[(numero_ligne, i, k)] = Node(numero_ligne, i, k)
        # ajout du dernier élément
        if lignes[numero_ligne - 1][-1] == '0' and lignes[numero_ligne][-1] == '0':
            for k in Orientation:
                self.sommets[(numero_ligne, nb_colonnes, k)] = Node(numero_ligne, nb_colonnes, k)

    def ajoute_derniere_ligne(self, nb_lignes, nb_colonnes, lignes):
        """
            Crée les sommets de la dernière "ligne" du graphe
            :param nb_lignes: nombre de lignes du dépôt
            :param nb_colonnes: nombre de colonnes du dépôt
            :param lignes: liste de listes, chacune représentant une ligne du dépôt
            :type nb_lignes: int
            :type nb_colonnes: int
            :type lignes: list
        """
        # ajout premier élément
        if lignes[-1][0] == '0':
            for k in Orientation:
                self.sommets[(nb_lignes, 0, k)] = Node(nb_lignes, 0, k)
        # ajout des éléments intermédiaires
        for i in range(1, nb_colonnes):
            if lignes[-1][i - 1] == '0' and lignes[-1][i] == '0':
                for k in Orientation:
                    self.sommets[(nb_lignes, i, k)] = Node(nb_lignes, i, k)
        # ajout du dernier élément
        if lignes[-1][-1] == '0':
            for k in Orientation:
                self.sommets[(nb_lignes, nb_colonnes, k)] = Node(nb_lignes, nb_colonnes, k)

    def ajoute_arcs(self, nb_lignes, nb_colonnes):
        """
            Ajoute ses arcs à chaque sommet: pour cela on ajoute les noeuds accessibles
            en une seconde à la liste d'adjacence
            :param nb_lignes: nombre de lignes du dépôt
            :param nb_colonnes: nombre de colonnes du dépôt
            :type nb_lignes: int
            :type nb_colonnes: int
        """
        # On parcourt tous les noeuds du graphe pour ajouter leurs adjacents
        for noeud in self.sommets.values():
            # ajout des arcs symbolisant l'avancée du robot dans sa direction
            if noeud.orientation == Orientation.nord:
                for i in range(1, 4):
                    if noeud.x - i >= 0:
                        n = self.get_sommet(noeud.x - i, noeud.y, Orientation.nord)
                        if n:
                            noeud.ajoute_adjacent(n)
                        else:
                            break
                    else:
                        break
            elif noeud.orientation == Orientation.sud:
                for i in range(1, 4):
                    if noeud.x + i <= nb_lignes:
                        n = self.get_sommet(noeud.x + i, noeud.y, Orientation.sud)
                        if n:
                            noeud.ajoute_adjacent(n)
                        else:
                            break
                    else:
                        break
            elif noeud.orientation == Orientation.est:
                for i in range(1, 4):
                    if noeud.y + i <= nb_colonnes:
                        n = self.get_sommet(noeud.x, noeud.y + i, Orientation.est)
                        if n:
                            noeud.ajoute_adjacent(n)
                        else:
                            break
                    else:
                        break
            elif noeud.orientation == Orientation.ouest:
                for i in range(1, 4):
                    if noeud.y - i >= 0:
                        n = self.get_sommet(noeud.x, noeud.y - i, Orientation.ouest)
                        if n:
                            noeud.ajoute_adjacent(n)
                        else:
                            break
                    else:
                        break
            # ajout des arcs symbolisant les rotations du robot sur sa position actuelle
            n = self.get_sommet(noeud.x, noeud.y, Orientation((noeud.orientation.value + 1) % 4))
            if n:
                noeud.ajoute_adjacent(n)
            n = self.get_sommet(noeud.x, noeud.y, Orientation((noeud.orientation.value + 3) % 4))
            if n:
                noeud.ajoute_adjacent(n)

    def affiche_graphe(self):
        """
            Affiche dans la console une représentation du dépôt avec ses obstacles
        """
        sep = "—" * (len(self.lignes[0]) * 2 + 1)
        for ligne in self.lignes:
            print(sep)
            for j in ligne:
                if j == "0":
                    print("|O", end="")
                else:
                    print("|X", end="")
            print("|")
        print(sep)


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
        self.depart.pere = -1

        self.arrivee = (int(ligne[2]), int(ligne[3]))  # En revanche ici, l'orientation n'est pas précisée
        self.graphe = graphe

    def parcours_en_largeur(self):
        """
            Effectue un parcours en largueur depuis le point de départ du robot
            Le père de chaque sommet visité est mis à jour
        """
        ouverts = [self.depart]  # Représente les sommets ouverts
        done = False
        while ouverts and not done:
            noeud = ouverts.pop(0)
            for i in noeud.adjacents:
                if i.pere is None:
                    i.pere = noeud
                    ouverts.append(i)
                    if (i.x, i.y) == self.arrivee:
                        done = True
                        break

    def affiche_resultat(self):
        """
            Recherche le chemin le plus rapide entre le point de départ et d'arrivée du robot,
            puis calcule la chaine de caractère correspondant à ce chemin
            :return: chemin le plus rapide
            :rtype: str
        """
        self.parcours_en_largeur()
        for i in Orientation:
            n = self.graphe.get_sommet(self.arrivee[0], self.arrivee[1], i)
            if n.pere:
                break
        return n.calculer_chemin_str()

    def coordonnees_chemin(self):
        """
            Recherche le chemin le plus rapide entre le point de départ et d'arrivée du robot,
            puis trouve les coordonnées des points empruntés et les retourne
            :return: chemin le plus rapide
            :rtype: list
        """
        self.parcours_en_largeur()
        for i in Orientation:
            n = self.graphe.get_sommet(self.arrivee[0], self.arrivee[1], i)
            if n.pere:
                break
        return n.calculer_chemin_liste(), n.calculer_chemin_str()
