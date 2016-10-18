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
from Stats.stats import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from .statics import *


leftframewidth = 600
leftframeheight = leftframewidth
couleur_obstacles = "#a28cff"


class LeftFrame(Frame):
    """
    Classe pour la "frame" qui sera la partie gauche de l'insterface.
    Celle-ci accueillera les grilles et les plots des statistiques
    """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None
        self.nb_colonnes = 0
        self.nb_lignes = 0
        self.pas_colonne = 0
        self.pas_ligne = 0
        self.initialize()

    def initialize(self):
        self.affiche_grille(self.parent.grilles[0])
        self.rescale()

    def clean(self):
        """
        Vide le contenu de la frame en supprimant les objets contenus dans celle-ci,
        en vue de le remplacer par autre chose
        """
        for i in self.winfo_children():
            i.destroy()

    def rescale(self):
        """
        Change l'échelle prise par la fenêtre pour un affichage plus pratique,
        on n'a alors plus qu'à spécifier les coordonnées comme dans la grille et cette fonction repositionne tout
        pour que l'affichage fasse la taille de la fenêtre
        """
        if self.canvas is not None and self.pas_colonne != 0 and self.pas_ligne != 0:
            self.canvas.scale(ALL, -1, -1, self.pas_colonne, self.pas_ligne)

    def afficher_resultat(self, resultat, tps_creat=None, tps_calc=None):
        """
        Affiche pour chaque instance du fichier d'entrée:
        la chaîne de caractère représentant le chemin emprunté par le robot,
        ainsi que le temps de création du graphe et le temps de calcul de ce résultat
        :param resultat: liste des chaines de caractères résultats du calcul du chemin le plus rapide des instances
        :param tps_creat: temps de création du graphe pour chaque instance
        :param tps_calc: temps de calcul du chemin le plus rapide pour chaque instance (sans la création du graphe)
        :type resultat: list
        :type tps_creat: list
        :type tps_calc: list
        """
        self.clean()
        if tps_creat:
            label = Label(self,
                          text="La moyenne du temps de création de graphe sur ce fichier est : " +
                               str(np.mean(tps_creat)) + " secondes")
            label.pack()
        if tps_calc:
            label = Label(self,
                          text="La moyenne du temps de calcul du chemin le plus rapide sur ce fichier est : " +
                               str(np.mean(tps_calc)) + " secondes")
            label.pack()
        for i in range(len(resultat)):
            label = Label(self, text="Problème n°"+str(i))
            label.pack()
            label_res = Label(self, text=resultat[i])
            label_res.pack()
            if tps_creat:
                label_tps_creat = Label(self, text="La création du graphe a pris " + str(tps_creat[i]) + " secondes")
                label_tps_creat.pack()
            if tps_calc:
                label_tps_calc = Label(self, text="Le calcul de la solution a pris " + str(tps_calc[i]) + " secondes")
                label_tps_calc.pack()

    def affiche_grille(self, grille):  # Ne pas oublier de faire un rescale après appel à cette fonction !!!
        """
        Affiche la grille passée en paramètre dans la partie gauche de la fenêtre
        :param grille: grille représentant le dépôt constituée de 3 éléments :
            - un tuple pour le nombre de lignes et de colonnes
            - une liste représentant les lignes du dépôt avec les '0' et '1'
            - une liste pour les coordonnées du point de départ, d'arrivée, et l'orientation du robot au départ
        :type grille: list
        """
        self.clean()
        # Récupération des éléments de la grille
        self.nb_lignes, self.nb_colonnes = grille[0]
        lignes = grille[1]
        ligne = grille[2]
        self.canvas = Canvas(self, width=leftframewidth, height=leftframeheight)
        # Récupération des données du problème
        self.pas_colonne = leftframewidth//(self.nb_colonnes + 2)
        self.pas_ligne = leftframeheight//(self.nb_lignes + 2)
        rayon = 1/2  # rayon des cercles du robot au départ et à l'arrivée
        # Dessin du quadrillage
        for i in range(0, self.nb_lignes):
            for j in range(0, self.nb_colonnes):
                if lignes[i][j] == '0':
                    rectangle(self.canvas, j, i, j+1, i+1)
                else:
                    rectangle(self.canvas, j, i, j+1, i+1, color=couleur_obstacles)
        # Dessin du point de départ du robot avec sa flèche
        dessine_depart(self.canvas, int(ligne[1]), int(ligne[0]), rayon, ligne[-1])
        # Dessin du point d'arrivée du robot
        cercle(self.canvas, int(ligne[3]), int(ligne[2]), rayon)
        self.canvas.pack()

    def affiche_chemin(self, grille, chemin_list, chemin_str):
        """
        Affiche la grille et le chemin le plus rapide du robot entre son point de départ et d'arrivée
        :param grille: grille représentant le dépôt constituée de 3 éléments (cf affiche_grille)
        :param chemin_list: liste de coordonnées des points empruntés par le robot dans sont chemin
        :param chemin_str: chaine de caractères résultat du calcul du chemin le plus rapide dans cette grille
        :type grille: list
        :type chemin_list: list
        :type chemin_str: str
        """
        # Affichage de la grille elle-même
        self.affiche_grille(grille)
        # Ajout du chemin par des lignes
        for i in range(1, len(chemin_list)):
            self.canvas.create_line(chemin_list[i-1][1], chemin_list[i-1][0],
                                    chemin_list[i][1], chemin_list[i][0], width=3)
        # on redessine le point de départ pour que ce soit plus "joli"
        ligne = grille[2]
        rayon = 1/2
        dessine_depart(self.canvas, int(ligne[1]), int(ligne[0]), rayon, ligne[-1])
        self.canvas.create_text(0, self.nb_lignes+1/2, text=chemin_str, font=("Helvetica", 10), anchor=NW)
        self.rescale()

    def modifier_grille(self):
        """
        Ajoute un lien entre clic gauche et les rectangles de la grille
        pour pouvoir modifier leur statut (obstacle ou non)
        """
        self.canvas.tag_bind("case", "<Button-1>", self.toggle_obstacle)

    def toggle_obstacle(self, event):
        """
        Changement du status (obstacle ou non) d'un rectangle de la grille lorsqu'on clique dessus
        :param event: clic gauche sur un rectangle
        """
        # Récupération du rectangle sur lequel on a cliqué
        w = event.widget.find_closest(event.x, event.y)
        ligne = (w[0]-1)//self.nb_colonnes
        colonne = (w[0]-1) % self.nb_colonnes
        # Changement de la grille elle-même en changeant la case correspondante,
        # et changement de la couleur du rectangle
        if self.parent.grilles[0][1][ligne][colonne] == '1':
            self.parent.grilles[0][1][ligne][colonne] = '0'
            self.canvas.itemconfig(w, fill="white")
        else:
            self.parent.grilles[0][1][ligne][colonne] = '1'
            self.canvas.itemconfig(w, fill=couleur_obstacles)

    def affiche_patienter(self):
        """
        Demande à l'utilisateur de patienter pendant le calcul des statistiques qu'il a demandées
        """
        self.clean()
        label = Label(self, text="Patientez s'il vous plaît\nCalcul des statistiques en cours", font=("Helvetica", 50))
        label.grid()

    def affiche_plot(self, figure):
        """
        Affichage dans la fenêtre du plot correspondant aux statistiques demandées
        :param figure: élément figure matplotlib à afficher
        """
        self.clean()
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
