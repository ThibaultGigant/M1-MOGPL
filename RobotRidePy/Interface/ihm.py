from tkinter.ttk import Combobox
from tkinter.filedialog import *
from tkinter.messagebox import *
from Robot.file_gestion import *
from Generation.generation import *
import os


apropos_message = """Ce programme est un projet réalisé par Thibault Gigant pour le projet de MOGPL en 2015
Le but de ce programme est de trouver le chemin le plus rapide d'un robot dans un entrepôt entre deux points"""
leftframewidth = 600
leftframeheight = leftframewidth
couleur_obstacles = "#a28cff"


class TopMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.menu_fichier()
        self.menu_aide()
        self.parent.config(menu=self)

    def menu_fichier(self):
        menu1 = Menu(self, tearoff=0)
        menu1.add_command(label="Ouvrir", command=self.parent.lancer_fichier)
        menu1.add_command(label="Créer", command=self.parent.creer_grille)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.parent.quit)
        self.add_cascade(label="Fichier", menu=menu1)

    def menu_aide(self):
        menu2 = Menu(self, tearoff=0)
        menu2.add_command(label="A propos", command=apropos)
        self.add_cascade(label="Aide", menu=menu2)


class LeftFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None
        self.nb_colonnes = 0
        self.nb_lignes = 0
        self.pas_colonne = 0
        self.pas_ligne = 0
        self.rectangles = []
        self.depart = None
        self.arrivee = None
        self.initialize()

    def initialize(self):
        self.affiche_grille(self.parent.grilles[0])
        self.rescale()

    def clean(self):
        for i in self.winfo_children():
            i.destroy()

    def rescale(self):
        if self.canvas is not None and self.pas_colonne != 0 and self.pas_ligne != 0:
            self.canvas.scale(ALL, -1, -1, self.pas_colonne, self.pas_ligne)

    def afficher_resultat(self, resultat, tps_creat=[], tps_calc=[]):
        self.clean()
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

    def affiche_grille(self, grille):  # Ne pas oublier de faire un rescale après appel !!!
        self.nb_lignes, self.nb_colonnes = grille[0]
        lignes = grille[1]
        ligne = grille[2]
        self.clean()
        self.canvas = Canvas(self, width=leftframewidth, height=leftframeheight)
        # Récupération des données du problème
        self.pas_colonne = leftframewidth//(self.nb_colonnes + 2)
        self.pas_ligne = leftframeheight//(self.nb_lignes + 2)
        self.rectangles = [[None for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
        rayon = 1/2  # rayon des cercles du robot au départ et à l'arrivée
        # Dessin du quadrillage
        for i in range(0, self.nb_lignes):
            for j in range(0, self.nb_colonnes):
                if lignes[i][j] == '0':
                    self.rectangles[i][j] = rectangle(self.canvas, j, i, j+1, i+1)
                else:
                    self.rectangles[i][j] = rectangle(self.canvas,
                              j, i, j+1, i+1, color=couleur_obstacles)
        # Dessin du point de départ du robot avec sa flèche
        self.depart = dessine_depart(self.canvas, int(ligne[1]), int(ligne[0]), rayon, ligne[-1])
        # Dessin du point d'arrivée du robot
        self.arrivee = cercle(self.canvas, int(ligne[3]), int(ligne[2]), rayon)
        self.canvas.pack()

    def affiche_chemin(self, grille, chemin_list, chemin_str):
        # Affichage de la grille elle-même
        self.affiche_grille(grille)
        # Ajout du chemin par des lignes
        for i in range(1, len(chemin_list)):
            self.canvas.create_line(chemin_list[i-1][1], chemin_list[i-1][0],
                                    chemin_list[i][1], chemin_list[i][0], width=5)
        # on redessine le point de départ pour que ce soit plus "joli"
        ligne = grille[2]
        rayon = 1/2
        dessine_depart(self.canvas, int(ligne[1]), int(ligne[0]), rayon, ligne[-1])
        self.ecrire_chemin(chemin_str)
        self.rescale()

    def ecrire_chemin(self, chemin):
        self.canvas.create_text(0, self.nb_lignes+1/2, text=chemin, font=("Helvetica", 20), anchor=NW)

    def modifier_grille(self):
        for i in range(len(self.rectangles)):
            for j in range(len(self.rectangles[i])):
                self.canvas.tag_bind(self.rectangles[i][j], "<Button-1>", lambda _: self.toggle_obstacle(i, j))

    def toggle_obstacle(self, x, y):
        # self.parent.grilles[0][1] est l'ensemble des lignes de la grille
        # on accède à la valeur du rectangle avec [x][y]
        if self.parent.grilles[0][1][x][y] == '1':
            self.parent.grilles[0][1][x][y] = '0'
            self.canvas.itemconfig(self.rectangles[x][y], fill="white")
        else:
            self.parent.grilles[0][1][x][y] = '1'
            self.canvas.itemconfig(self.rectangles[x][y], fill=couleur_obstacles)


class RightFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.widget_grilles = None
        self.mode_creation = None
        self.nb_lignes = IntVar()  # Attention, ici ce sont les nombres de lignes, colonnes et obstacles à créer
        self.nb_colonnes = IntVar()  # et non le nombre présent au début sur la grille
        self.nb_obstacles = IntVar()

    def clean(self):
        for i in self.winfo_children():
            i.destroy()

    def choice_buttons(self):
        self.clean()
        open_button = Button(self, text="Récupérer un problème depuis un fichier",
                             command=self.parent.lancer_fichier)
        create_button = Button(self, text="Créer manuellement un problème",
                               command=self.creer_grille)
        open_button.grid()
        create_button.grid()

    def ouvrir_fichiers(self):
        self.clean()
        label = Label(self, text="Fichier d'entrée")
        entry = Entry(self, textvariable=self.parent.entree)
        bouton = Button(self, text="Changer le fichier d'entrée",
                        command=lambda: self.parent.entree.set(choisir_fichier("Choisir le fichier d'entrée")))
        label.grid(column=0, row=0, columnspan=4)
        entry.grid(column=0, row=1, columnspan=3)
        bouton.grid(column=3, row=1)

        # On demande enfin la sortie
        label = Label(self, text="Fichier de sortie")
        entry = Entry(self, textvariable=self.parent.sortie)
        bouton = Button(self, text="Choisir un fichier existant",
                        command=lambda: self.parent.sortie.set(choisir_fichier("Choisir le fichier de sortie")))
        label.grid(column=0, row=2, columnspan=4)
        entry.grid(column=0, row=3, columnspan=3)
        bouton.grid(column=3, row=3)

        # Lancement de l'algorithme pour toutes les grilles
        validate_all = Button(self, text="Lancer l'algorithme pour toutes les grilles du fichier d'entrée",
                              command=self.parent.lancer_algo)
        validate_all.grid(column=0, row=4, columnspan=4)

        # Lancement de l'algorithme pour une seule grille
        label = Label(self, text="Ou choisir une grille dans le fichier d'entrée")
        label.grid(column=0, row=5, columnspan=4)
        self.update_widget_grilles()
        bouton_maj = Button(self, text="Mise à jour des grilles", command=self.update_widget_grilles)
        bouton_maj.grid(column=2, row=6, columnspan=2)

    def update_widget_grilles(self):
        self.parent.update_grilles()
        if self.widget_grilles is not None:
            self.widget_grilles.destroy()
        varcombo = StringVar()
        combo = Combobox(self, textvariable=varcombo)
        combo_liste = []
        for i in range(1, len(self.parent.grilles)+1):
            combo_liste.append("Grille n°" + str(i))
        combo['values'] = tuple(combo_liste)
        combo['state'] = "readonly"
        combo.current(0)
        combo.grid(column=0, row=6, columnspan=2)
        bouton_affichage = Button(self, text="Visualiser la grille",
                                  command=lambda: self.parent.afficher_grille(combo_liste.index(combo.get())))
        bouton_lancement = Button(self, text="Lancer l'algorithme sur cette grille",
                                  command=lambda: self.parent.lancer_grille(combo_liste.index(combo.get())))
        bouton_affichage.grid(column=0, row=7, columnspan=2)
        bouton_lancement.grid(column=2, row=7, columnspan=2)

    def creer_grille(self):
        self.clean()
        label = Label(self, text="Choisissez la taille de la grille que vous voulez créer")
        spin_lignes = Spinbox(self, from_=1, to=100, textvariable=self.nb_lignes)
        spin_colonnes = Spinbox(self, from_=1, to=100, textvariable=self.nb_colonnes)
        spin_obstacles = Spinbox(self, from_=0, textvariable=self.nb_obstacles)
        label_lignes = Label(self, text="Nombre de lignes :")
        label_colonnes = Label(self, text="Nombre de colonnes :")
        label_obstacles = Label(self, text="Nombre d'obstacles :")
        label_placement = Label(self, text="Choix du placement des obstables, des points de départ et d'arrivée :")
        self.mode_creation = StringVar()
        radio_aleatoire = Radiobutton(self, text="Aléatoire", variable=self.mode_creation, value=1)
        radio_manuel = Radiobutton(self, text="Manuel", variable=self.mode_creation, value=2)
        bouton_valide = Button(self, text="Générer la grille", command=self.parent.generer_grille)

        label.grid(column=0, row=0, columnspan=4)
        label_lignes.grid(column=0, row=1, columnspan=2)
        spin_lignes.grid(column=2, row=1, columnspan=2)
        label_colonnes.grid(column=0, row=2, columnspan=2)
        spin_colonnes.grid(column=2, row=2, columnspan=2)
        label_obstacles.grid(column=0, row=3, columnspan=2)
        spin_obstacles.grid(column=2, row=3, columnspan=2)
        label_placement.grid(column=0, row=4, columnspan=4)
        radio_aleatoire.grid(column=0, row=5, columnspan=2)
        radio_manuel.grid(column=2, row=5, columnspan=2)
        bouton_valide.grid(column=1, row=6, columnspan=2)

    def grille_aleatoire(self):
        self.clean()
        bouton_modifier_grille = Button(self, text="Modifier la grille", command=self.parent.modifier_grille)
        bouton_lancement = Button(self,
                                  text="Lancer l'algorithme sur cette grille",
                                  command=lambda: self.parent.lancer_grille(0))

        bouton_modifier_grille.grid(column=0, row=0)
        bouton_lancement.grid(column=1, row=0)

    def modifier_grille(self):
        self.clean()
        orientation = StringVar()
        abscisse_depart = IntVar()
        ordonnee_depart = IntVar()
        abscisse_arrivee = IntVar()
        ordonnee_arrivee = IntVar()
        orientation.set(self.parent.grilles[0][2][4])
        abscisse_depart.set(int(self.parent.grilles[0][2][0]))
        ordonnee_depart.set(int(self.parent.grilles[0][2][1]))
        abscisse_arrivee.set(int(self.parent.grilles[0][2][2]))
        ordonnee_arrivee.set(int(self.parent.grilles[0][2][3]))
        label_depart = Label(self, text="Coordonnées de l'emplacement du Robot au départ :")
        label_orientation = Label(self, text="Orientation du Robot au départ :")
        spin_abscisse_depart = Spinbox(self, from_=0, to=self.parent.grilles[0][0][0], textvariable=abscisse_depart)
        spin_ordonnee_depart = Spinbox(self, from_=0, to=self.parent.grilles[0][0][1], textvariable=ordonnee_depart)
        combo_orientation = Combobox(self,
                                     values=("nord", "est", "sud", "ouest"),
                                     textvariable=orientation,
                                     state="readonly")
        label_arrivee = Label(self, text="Coordonnées de l'emplacement du Robot à l'arrivée :")
        spin_abscisse_arrivee = Spinbox(self, from_=0, to=self.parent.grilles[0][0][0], textvariable=abscisse_arrivee)
        spin_ordonnee_arrivee = Spinbox(self, from_=0, to=self.parent.grilles[0][0][1], textvariable=ordonnee_arrivee)
        bouton_maj = Button(self,
                            text="Mettre à jour",
                            command=lambda: self.maj_depart_arrivee(abscisse_depart.get(), ordonnee_depart.get(), abscisse_arrivee.get(), ordonnee_arrivee.get(), orientation.get()))
        bouton_lancement = Button(self, text="Lancer sur cette grille", command=lambda: self.parent.lancer_grille(0))
        label_depart.grid(column=0, row=0, columnspan=2)
        spin_abscisse_depart.grid(column=0, row=1)
        spin_ordonnee_depart.grid(column=1, row=1)
        label_orientation.grid(column=0, row=2, columnspan=2)
        combo_orientation.grid(column=0, row=3, columnspan=2)
        label_arrivee.grid(column=0, row=4, columnspan=2)
        spin_abscisse_arrivee.grid(column=0, row=5)
        spin_ordonnee_arrivee.grid(column=1, row=5)
        bouton_maj.grid(column=0, row=6)
        bouton_lancement.grid(column=1, row=6)

    def maj_depart_arrivee(self, abs_dep, ord_dep, abs_arr, ord_arr, orientation):
        self.parent.grilles[0][2][0] = abs_dep
        self.parent.grilles[0][2][1] = ord_dep
        self.parent.grilles[0][2][2] = abs_arr
        self.parent.grilles[0][2][3] = ord_arr
        self.parent.grilles[0][2][4] = orientation
        self.parent.afficher_grille(0)
        self.parent.modifier_grille()


class FenetrePrincipale(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.entree = StringVar()
        self.sortie = StringVar()
        self.entree.set("/Users/Tigig/Documents/Travail/M1/M1-MOGPL/RobotRidePy/Instances/x9y10o10.dat")
        self.sortie.set("/Users/Tigig/Documents/Travail/M1/M1-MOGPL/RobotRidePy/Instances/Résultats/x9y10o10out.dat")
        self.menu = None
        self.leftFrame = None
        self.rightFrame = None
        self.grilles = []
        self.initialize()

    def initialize(self):
        self.update_grilles()
        # self.grid()
        self.menu = TopMenu(self)
        self.rightFrame = RightFrame(self)
        self.leftFrame = LeftFrame(self)
        self.leftFrame.pack(side=LEFT, padx=10, pady=10)
        self.rightFrame.pack(side=RIGHT, padx=10, pady=10)
        self.menu_principal()

    def update_grilles(self):
        self.grilles = get_grilles(self.entree.get())

    def menu_principal(self):
        self.choice_buttons()

    def clear_fenetre(self):
        if self.leftFrame:
            for i in self.leftFrame.winfo_children():
                i.destroy()
        if self.rightFrame:
            for i in self.rightFrame.winfo_children():
                i.destroy()

    def choice_buttons(self):
        self.rightFrame.choice_buttons()

    def lancer_fichier(self):
        self.rightFrame.ouvrir_fichiers()

    def lancer_algo(self):
        if os.path.isfile(self.entree.get()):
            if os.path.isfile(self.sortie.get()):
                if not askyesno("Fichier existant", "Le fichier " + self.sortie.get() + " existe déjà, la procédure effacera son contenu, voulez-vous vraiment choisir ce fichier ?"):
                    return
            if self.sortie.get():
                resultat, tps_creat, tps_calc = lecture(self.entree.get(), self.sortie.get())
                self.leftFrame.afficher_resultat(resultat, tps_creat, tps_calc)
            else:
                showerror("Erreur Fichiers", "Le fichier de sortie est incorrect")
        else:
            showerror("Erreur Fichiers", "Le fichier d'entrée est introuvable")

    def afficher_grille(self, numero_grille):
        grille = self.grilles[numero_grille]
        self.leftFrame.affiche_grille(grille)
        self.leftFrame.rescale()

    def lancer_grille(self, numero_grille):
        grille = self.grilles[numero_grille]
        chemin_list, chemin_str = lancement_et_chemin(grille)
        self.leftFrame.affiche_chemin(grille, chemin_list, chemin_str)

    def creer_grille(self):
        self.rightFrame.creer_grille()

    def modifier_grille(self):
        # Pas besoin d'afficher, elle l'est déjà normalement...
        # self.leftFrame.affiche_grille()
        self.leftFrame.modifier_grille()
        self.rightFrame.modifier_grille()

    def generer_grille(self):
        if self.rightFrame.mode_creation is not None:
            if self.rightFrame.mode_creation.get() == '1':
                self.grilles = [generer_grille(self.rightFrame.nb_lignes.get(),
                                               self.rightFrame.nb_colonnes.get(),
                                               self.rightFrame.nb_obstacles.get())]
                self.leftFrame.affiche_grille(self.grilles[0])
                self.leftFrame.rescale()
                self.rightFrame.grille_aleatoire()
            if self.rightFrame.mode_creation.get() == '2':
                lignes = [['0' for i in range(self.rightFrame.nb_colonnes.get())] for j in range(self.rightFrame.nb_lignes.get())]
                ligne = ['0', '0', str(self.rightFrame.nb_lignes.get()), str(self.rightFrame.nb_colonnes.get()), "sud"]
                self.grilles = [[(self.rightFrame.nb_lignes.get(), self.rightFrame.nb_colonnes.get()), lignes, ligne]]
                self.afficher_grille(0)
                self.modifier_grille()


# Méthodes en dehors des classes, communes
def choisir_fichier(titre):
    return askopenfilename(title=titre, filetypes=[('dat files', '*.dat'), ('all files', '.*')])


def apropos():
    showinfo("Robot Ride !", apropos_message)


def rectangle(canvas, x1, y1, x2, y2, color="white", border_color="black"):  # FEFF8E
    return canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=border_color)


def cercle(canvas, x, y, r, color="black"):
    return canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color)


def dessine_depart(canvas, x, y, echelle, direction, color="red"):
    # triangle(canvas, x, y, echelle, direction, color)
    cerc = cercle(canvas, x, y, echelle, color)
    line = canvas.create_line(x, y,
                       x + ((direction == "est") - (direction == "ouest")),
                       y + ((direction == "sud") - (direction == "nord")),
                       width=max(echelle//4, 8), arrow=LAST, fill=color)
    return cerc, line


# Construit un triangle équilatéral dans la direction voulue
# la valeur "echelle" représente la dimension minimal leftframewidth//nb_colonnes ou leftframeheight//nb_lignes
def triangle(canvas, x, y, echelle, direction, color="black"):
    if direction == "sud":
        canvas.create_polygon(x-echelle, y-echelle, x+echelle, y-echelle, x, y+echelle, fill=color)
    if direction == "nord":
        canvas.create_polygon(x+echelle, y+echelle, x-echelle, y+echelle, x, y-echelle, fill=color)
    if direction == "est":
        canvas.create_polygon(x-echelle, y-echelle, x-echelle, y+echelle, x+echelle, y, fill=color)
    if direction == "ouest":
        canvas.create_polygon(x+echelle, y+echelle, x+echelle, y-echelle, x-echelle, y, fill=color)


def affichage_fenetre():
    fenetre = FenetrePrincipale(None)
    fenetre.title("Robot Ride !")
    fenetre.mainloop()
