# -*- coding: utf-8 -*-
try:
    try:
        from tkinter import *
        from tkinter.ttk import Combobox
        from tkinter.filedialog import *
        from tkinter.messagebox import *
    except:
        from Tkinter import *
        from ttk import Combobox
        from tkFileDialog import *
        from tkMessageBox import *
except:
    raise ImportError('Wrapper Tk non disponible')


# Méthodes en dehors des classes
def choisir_fichier(titre):
    """
    Affiche une fenêtre permettant de choisir un fichier existant
    :param titre: titre de la fenêtre à afficher
    :type titre: str
    :return: chemin absolu du fichier sélectionné
    :rtype: str
    """
    return askopenfilename(title=titre, filetypes=[('dat files', '*.dat'), ('all files', '.*')])


def rectangle(canvas, x1, y1, x2, y2, color="white", border_color="gray"):
    """
    Crée un rectangle, dont les coordonnées de 2 points opposés sont renseignés, dans le canvas donné
    :param canvas: widget de la fenêtre gauche où la grille est affichée
    :param x1: abscisse d'un des points
    :param y1: ordonnée d'un des points
    :param x2: abscisse de l'autre point
    :param y2: ordonnée de l'autre point
    :param color: couleur du rectangle
    :param border_color: couleur de la bordure du rectangle
    :type canvas: Widget
    :type x1: int
    :type y1: int
    :type x2: int
    :type y2: int
    :type color: str
    :type border_color: str
    """
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=border_color, tags="case")


def cercle(canvas, x, y, r, color="black"):
    """
    Crée un cercle, défini par les coordonnées de son centre et son rayon, dans le canvas donné
    :param canvas: widget de la fenêtre gauche où la grille est affichée
    :param x: abscisse du centre du cercle
    :param y: ordonnée du centre du cercle
    :param r: rayon du cercle
    :param color: couleur du cercle
    :type canvas: Widget
    :type x: int
    :type y: int
    :type r: int
    :type color: str
    """
    canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color)


def dessine_depart(canvas, x, y, rayon, direction, color="red"):
    """
    Dessine le robot dans sa position initiale, avec la flèche représentant son orientation de départ
    :param canvas: widget de la fenêtre gauche où la grille est affichée
    :param x: abscisse du centre du robot
    :param y: ordonnée du centre du robot
    :param rayon: rayon du cercle désignant le robot
    :param direction: direction du robot parmi ces valeurs ["nord", "sud", "est", "ouest"]
    :param color: couleur du robot
    :type canvas: Widget
    :type x: int
    :type y: int
    :type rayon: int
    :type direction: str
    :type color: str
    """
    cercle(canvas, x, y, rayon, color)
    canvas.create_line(x, y,
                       x + ((direction == "est") - (direction == "ouest")),
                       y + ((direction == "sud") - (direction == "nord")),
                       width=max(rayon // 4, 8), arrow=LAST, fill=color)
