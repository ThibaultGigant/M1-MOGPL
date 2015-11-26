from random import randint, choice

directions = ["nord", "est", "sud", "ouest"]


def generation_lignes(nb_lignes, nb_colonnes, nb_obstacles):
    if nb_obstacles > nb_lignes * nb_colonnes:
        exit("Génération impossible, trop d'obstacles")
    lignes = [['0' for i in range(nb_colonnes)] for j in range(nb_lignes)]
    for i in range(nb_obstacles):
        x = randint(0, nb_lignes - 1)
        y = randint(0, nb_colonnes - 1)
        while lignes[x][y] == '1':
            x = randint(0, nb_lignes - 1)
            y = randint(0, nb_colonnes - 1)
        lignes[x][y] = '1'
    return lignes


def verif_choix(lignes, x, y):
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
    x_depart = randint(0, len(lignes))
    y_depart = randint(0, len(lignes[0]))
    while verif_choix(lignes, x_depart, y_depart):
        x_depart = randint(0, len(lignes))
        y_depart = randint(0, len(lignes[0]))
    x_arrivee = randint(0, len(lignes))
    y_arrivee = randint(0, len(lignes[0]))
    while verif_choix(lignes, x_arrivee, y_arrivee) or (x_depart == x_arrivee and y_depart == y_arrivee):
        x_arrivee = randint(0, len(lignes))
        y_arrivee = randint(0, len(lignes[0]))
    return [str(x_depart), str(y_depart), str(x_arrivee), str(y_arrivee), choice(directions)]


def choix_depart_arrivee_to_string(lignes):
    return " ".join(choix_depart_arrivee(lignes)) + "\n"


def generer_grille(nb_lignes, nb_colonnes, nb_obstacles):
    grille = [(nb_lignes, nb_colonnes)]
    grille += [generation_lignes(nb_lignes, nb_colonnes, nb_obstacles)]
    grille += [choix_depart_arrivee(grille[1])]


def creer_instances(fichier, nb_instances=1, nb_lignes=None, nb_colonnes=None, nb_obstacles=None):
    fp = open(fichier, "w")
    nbl = nb_lignes
    nbc = nb_colonnes
    nbo = nb_obstacles
    for i in range(nb_instances):
        if nb_lignes is None:
            nbl = randint(1, 5) * 10
        if nb_colonnes is None:
            nbc = randint(1, 5) * 10
        if nb_obstacles is None:
            nbo = randint(1, min(nbl, nbc) / 10) * 10
        lignes = generation_lignes(nbl, nbc, nbo)
        fp.write(str(nbl) + " " + str(nbc) + "\n")
        for ligne in lignes:
            fp.write(" ".join(ligne) + "\n")
        fp.write(choix_depart_arrivee_to_string(lignes))
        if i != nb_instances - 1:
            fp.write("\n")
    fp.write("0 0")
    fp.close()
