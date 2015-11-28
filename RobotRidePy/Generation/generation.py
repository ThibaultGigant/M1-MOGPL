from random import randint, choice

# Cette liste sert pour la génération du point de départ,
# on n'a qu'à choisir aléatoirement une direction dans cette liste
directions = ["nord", "est", "sud", "ouest"]


def generation_lignes(nb_lignes, nb_colonnes, nb_obstacles):
    """
    Génère aléatoirement les lignes d'une grille représentant un dépôt
    :param nb_lignes: nombre de lignes de la grille à générer
    :param nb_colonnes: nombre de colonnes de la grille à générer
    :param nb_obstacles: nombre d'obstacles dans la grille à générer
    :type nb_lignes: int
    :type nb_colonnes: int
    :type nb_obstacles: int
    :return: lignes du dépôt
    :rtype: list
    """
    if nb_obstacles > nb_lignes * nb_colonnes:
        exit("Génération impossible, trop d'obstacles")
    # Génération d'une grille avec uniquement des 0
    lignes = [['0' for i in range(nb_colonnes)] for j in range(nb_lignes)]
    # Ajout aléatoire d'obstacles en ajoutant un '1' à des positions aléatoires
    for i in range(nb_obstacles):
        x = randint(0, nb_lignes - 1)
        y = randint(0, nb_colonnes - 1)
        # On vérifie que le point n'est pas déjà un obstacles (sinon on ne rajoute pas le bon nombre d'obstacles)
        while lignes[x][y] == '1':
            x = randint(0, nb_lignes - 1)
            y = randint(0, nb_colonnes - 1)
        lignes[x][y] = '1'
    return lignes


def verif_choix(lignes, x, y):
    """
    Vérifie le choix fait pour un point de départ ou d'arrivée en vérifiant s'il n'y a pas des '1' autour
    :param lignes: lignes du dépôt avec les 1 représentant les obstacles et les 0
    :param x: coordonnée en abscisse du point
    :param y: coordonnée en abscisse du point
    :type lignes: list
    :type x: int
    :type y: int
    :return: True si la case ne peut pas être choisie, False sinon
    :rtype: bool
    """
    # Pour vérifier on vérifie que les cases (potentiellement au nombre de 4) autour du point voulu ne sont pas des '1'
    if x > 0 and y > 0:
        if lignes[x - 1][y - 1] == '1':
            return True
    if x > 0 and y < len(lignes[0]):
        if lignes[x - 1][y] == '1':
            return True
    if x < len(lignes) and y > 0:
        if lignes[x][y - 1] == '1':
            return True
    if x < len(lignes) and y < len(lignes[0]):
        if lignes[x][y] == '1':
            return True
    return False


def choix_depart_arrivee(lignes):
    """
    Choisit aléatoirement des points de départ et d'arrivée
    :param lignes: représente le dépôt
    :type lignes: list
    :return: liste des positions du robot au départ et à l'arrivée, ainsi que de son orientation au départ
    :rtype: list
    """
    # Choix du point de départ
    x_depart = randint(0, len(lignes))
    y_depart = randint(0, len(lignes[0]))
    while verif_choix(lignes, x_depart, y_depart):
        x_depart = randint(0, len(lignes))
        y_depart = randint(0, len(lignes[0]))
    # Choix du point d'arrivée
    x_arrivee = randint(0, len(lignes))
    y_arrivee = randint(0, len(lignes[0]))
    while verif_choix(lignes, x_arrivee, y_arrivee) or (x_depart == x_arrivee and y_depart == y_arrivee):
        x_arrivee = randint(0, len(lignes))
        y_arrivee = randint(0, len(lignes[0]))
    return [str(x_depart), str(y_depart), str(x_arrivee), str(y_arrivee), choice(directions)]


def choix_depart_arrivee_to_string(lignes):
    """
    Convertit en chaîne de caractères le choix fait pour les points de départ et d'arrivée en vue d'une écriture
    ultérieure dans un fichier
    :param lignes: représente le dépôt
    :type lignes: list
    :return: chaîne de caractère voulue
    """
    return " ".join(choix_depart_arrivee(lignes)) + "\n"


def generer_grille(nb_lignes, nb_colonnes, nb_obstacles):
    """
    Génère aléatoirement une grille entière pouvant par la suite être résolue ou écrite
    :param nb_lignes: nombre voulu de lignes du dépôt
    :param nb_colonnes: nombre voulu de colonnes du dépôt
    :param nb_obstacles: nombre voulu d'obstacles du dépôt
    :type nb_lignes: int
    :type nb_colonnes: int
    :type nb_obstacles: int
    :return: grille, représentant un dépôt, comprenant les données nécessaire à la résolution ou l'écriture de celle-ci
    """
    grille = [(nb_lignes, nb_colonnes)]
    grille += [generation_lignes(nb_lignes, nb_colonnes, nb_obstacles)]
    grille += [choix_depart_arrivee(grille[1])]
    return grille


def creer_instances(fichier, nb_instances=1, nb_lignes=None, nb_colonnes=None, nb_obstacles=None):
    """
    Génère aléatoirement des instances de grilles et les écrit dans un fichier
    (Cette fonction a surtout servi pour la génération des fichiers de test dans le répertoire Instances,
    et n'est plus vraiment utile pour une utilisation par l'interface utilisateur)
    :param fichier: fichier où écrire les instances créées
    :param nb_instances: nombre voulu d'instances à créer
    :param nb_lignes: nombre de lignes des instances
    :param nb_colonnes: nombre de colonnes des instances
    :param nb_obstacles: nombre d'obstacles des instances
    :type fichier: str
    :type nb_instances: int
    :type nb_lignes: int
    :type nb_colonnes: int
    :type nb_obstacles: int
    """
    fp = open(fichier, "w")
    nbl = nb_lignes
    nbc = nb_colonnes
    nbo = nb_obstacles
    for i in range(nb_instances):
        # Si nb_lignes, nb_colonnes ou nb_obstacles valent None, on les choisit aléatoirement
        if nb_lignes is None:
            nbl = randint(1, 5) * 10
        if nb_colonnes is None:
            nbc = randint(1, 5) * 10
        if nb_obstacles is None:
            nbo = randint(1, min(nbl, nbc) / 10) * 10
        # Génération et écriture des lignes du dépôt
        lignes = generation_lignes(nbl, nbc, nbo)
        fp.write(str(nbl) + " " + str(nbc) + "\n")
        for ligne in lignes:
            fp.write(" ".join(ligne) + "\n")
        fp.write(choix_depart_arrivee_to_string(lignes))
        if i != nb_instances - 1:
            fp.write("\n")
    fp.write("0 0")
    fp.close()
