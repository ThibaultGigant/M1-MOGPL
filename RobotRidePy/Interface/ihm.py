# -*- coding: utf-8 -*-
try:
    try:
        from tkinter.ttk import Combobox
        from tkinter.filedialog import *
        from tkinter.messagebox import *
    except:
        from ttk import Combobox
        from tkFileDialog import *
        from tkMessageBox import *
except:
    raise ImportError('Wrapper Tk non disponible')
from Robot.file_gestion import *
from Generation.generation import *
from Stats.stats import *
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


apropos_message = """Ce programme est un projet réalisé par Thibault Gigant pour le projet de MOGPL en 2015
Le but de ce programme est de trouver le chemin le plus rapide entre deux points d'un robot dans un entrepôt"""
leftframewidth = 600
leftframeheight = leftframewidth
couleur_obstacles = "#a28cff"


class TopMenu(Menu):
    """
    Classe du menu dans le haut de la fenêtre (ou dans la "barre des menus" pour Mac)
    Chaque méthode crée un menu déroulant
    """
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
        menu1.add_command(label="Statistiques", command=self.parent.lancer_statistiques)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.parent.quit)
        self.add_cascade(label="Fichier", menu=menu1)

    def menu_aide(self):
        menu2 = Menu(self, tearoff=0)
        menu2.add_command(label="A propos", command=self.apropos)
        self.add_cascade(label="A propos", menu=menu2)

    @staticmethod
    def apropos():
        showinfo("Robot Ride !", apropos_message)


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
        print(w)
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


class RightFrame(Frame):
    """
    Classe pour la frame qui sera à droite, interaction principale avec l'utilisateur
    Demande à l'utilisateur ce qu'il veut effectuer ou les données nécessaire
    """
    def __init__(self, parent):
        Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.nb_lignes = IntVar()  # Attention, ici ce sont les nombres de lignes, colonnes et obstacles à créer
        self.nb_colonnes = IntVar()  # et non le nombre présent au début sur la grille
        self.nb_obstacles = IntVar()

    def clean(self):
        """
        Vide le contenu de la frame en supprimant les objets contenus dans celle-ci,
        en vue de le remplacer par autre chose
        """
        for i in self.winfo_children():
            i.destroy()

    def choice_buttons(self):
        """
        Affiche les boutons permettant de choisir l'action à réaliser au départ :
        ouvrir un fichier, créer une grille, ou faire des statistiques
        Ce sera le menu principal...
        """
        self.clean()
        open_button = Button(self, text="Récupérer un problème depuis un fichier",
                             command=self.parent.lancer_fichier)
        create_button = Button(self, text="Créer manuellement un problème",
                               command=self.creer_grille)
        stats_button = Button(self, text="Faire des statistiques",
                              command=self.lancer_statistiques)
        open_button.grid()
        create_button.grid()
        stats_button.grid()

    def ouvrir_fichiers(self):
        """
        Affiche la partie droite correspondant à l'ouverture d'un fichier
        et l'exécution des instances contenues dans celui-ci, voire même l'écriture du résultat dans un fichier
        """
        self.clean()
        # On demande le fichier d'entrée. Par défaut c'est le fichier correspondant à l'instance sur l'énoncé
        label = Label(self, text="Fichier d'entrée")
        entry = Entry(self, textvariable=self.parent.entree)
        bouton = Button(self, text="Changer le fichier d'entrée",
                        command=lambda: self.parent.entree.set(choisir_fichier("Choisir le fichier d'entrée")))
        label.grid(column=0, row=0, columnspan=4)
        entry.grid(column=0, row=1, columnspan=3)
        bouton.grid(column=3, row=1)

        # On demande la sortie
        label = Label(self, text="Fichier de sortie")
        entry = Entry(self, textvariable=self.parent.sortie)
        bouton = Button(self, text="Choisir un fichier existant",
                        command=lambda: self.parent.sortie.set(choisir_fichier("Choisir le fichier de sortie")))
        label.grid(column=0, row=2, columnspan=4)
        entry.grid(column=0, row=3, columnspan=3)
        bouton.grid(column=3, row=3)

        # Partie pour le lancement de l'algorithme sur toutes les grilles du fichier d'entrée
        validate_all = Button(self, text="Lancer l'algorithme\npour toutes les grilles\ndu fichier d'entrée",
                              command=self.parent.lancer_algo)
        validate_all.grid(column=0, row=4, columnspan=4)

        # Lancement de l'algorithme pour une seule grille sélectionnée du fichier d'entrée
        label = Label(self, text="Ou choisir une grille dans le fichier d'entrée")
        label.grid(column=0, row=5, columnspan=4)
        self.update_widget_grilles()
        bouton_maj = Button(self, text="Mise à jour des grilles", command=self.update_widget_grilles)
        bouton_maj.grid(column=2, row=6, columnspan=2)

    def update_widget_grilles(self):
        """
        Met à jour le menu déroulant listant les grilles contenues dans le fichier d'entrée
        """
        # Mise à jour des grilles correspondant au fichier d'entrée s'il a été changé
        self.parent.update_grilles()
        # Ajout de la liste des grilles
        varcombo = StringVar()
        combo = Combobox(self, textvariable=varcombo)
        combo_liste = []
        for i in range(1, len(self.parent.grilles)+1):
            combo_liste.append("Grille n°" + str(i))
        combo['values'] = tuple(combo_liste)
        combo['state'] = "readonly"
        combo.current(0)
        combo.grid(column=0, row=6, columnspan=2)

        # Ajout des boutons pour visualiser la grille choisie ou lancer l'exécution de l'algorithme sur celle-ci
        bouton_affichage = Button(self, text="Visualiser la grille",
                                  command=lambda: self.parent.afficher_grille(combo_liste.index(combo.get())))
        bouton_lancement = Button(self, text="Lancer l'algorithme sur cette grille",
                                  command=lambda: self.parent.lancer_grille(combo_liste.index(combo.get())))
        bouton_affichage.grid(column=0, row=7, columnspan=2)
        bouton_lancement.grid(column=2, row=7, columnspan=2)
        bouton_modification = Button(self, text="Modificer cette grille",
                                     command=lambda: self.modification_grille_ouverte(combo_liste.index(combo.get())))
        bouton_modification.grid(column=0, row=8, columnspan=4)

    def modification_grille_ouverte(self, numero_grille):
        self.parent.grilles[0] = self.parent.grilles[numero_grille]
        self.parent.modifier_grille()

    def creer_grille(self):
        """
        Demande les données nécessaire à la création aléatoire ou manuelle d'une grille
        """
        self.clean()
        # Création des éléments demandant ces données
        label = Label(self, text="Choisissez la taille de la grille que vous voulez créer")
        spin_lignes = Spinbox(self, from_=1, to=100, textvariable=self.nb_lignes)
        spin_colonnes = Spinbox(self, from_=1, to=100, textvariable=self.nb_colonnes)
        spin_obstacles = Spinbox(self, from_=0, to=3000, textvariable=self.nb_obstacles)
        label_lignes = Label(self, text="Nombre de lignes :")
        label_colonnes = Label(self, text="Nombre de colonnes :")
        label_obstacles = Label(self, text="Nombre d'obstacles :")
        label_placement = Label(self, text="Choix du placement des obstables, des points de départ et d'arrivée :")
        bouton_valide = Button(self, text="Générer la grille", command=self.parent.generer_grille)

        # Positionnement de ces éléments dans la "frame"
        label.grid(column=0, row=0, columnspan=4)
        label_lignes.grid(column=0, row=1, columnspan=2)
        spin_lignes.grid(column=2, row=1, columnspan=2)
        label_colonnes.grid(column=0, row=2, columnspan=2)
        spin_colonnes.grid(column=2, row=2, columnspan=2)
        label_obstacles.grid(column=0, row=3, columnspan=2)
        spin_obstacles.grid(column=2, row=3, columnspan=2)
        label_placement.grid(column=0, row=4, columnspan=4)
        bouton_valide.grid(column=1, row=5, columnspan=2)

    def modifier_grille(self):
        """
        Affiche dans la partie droite de la fenêtre les actions possibles sur une grille qu'on veut modifier
        """
        self.clean()

        # Définition des variables nécessaires
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

        # Création des éléments demandant les variables à l'utilisateur
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
        bouton_lancement = Button(self, text="Lancer sur cette grille", command=self.lancement_modifie)
        bouton_enregistrement = Button(self, text="Enregistrer cette grille dans un fichier",
                                       command= lambda: self.parent.enregistrer_grille(0))

        # Positionnement de ces éléments dans la "frame"
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
        bouton_enregistrement.grid(column=0, row=7, columnspan=2)

    def maj_depart_arrivee(self, abs_dep, ord_dep, abs_arr, ord_arr, orientation):
        """
        Met à jour la position du point de départ et d'arrivée de la grille
        Ces modifications sont effectuées directement dans la grille, puis celle-ci est réaffichée
        :param abs_dep: abscisse du point de départ
        :param ord_dep: ordonnée du point de départ
        :param abs_arr: abscisse du point d'arrivée
        :param ord_arr: ordonnée du point d'arrivée
        :param orientation: orientation du robot au départ
        """
        self.parent.grilles[0][2][0] = abs_dep
        self.parent.grilles[0][2][1] = ord_dep
        self.parent.grilles[0][2][2] = abs_arr
        self.parent.grilles[0][2][3] = ord_arr
        self.parent.grilles[0][2][4] = orientation
        self.parent.afficher_grille(0)
        self.parent.modifier_grille()

    def lancement_modifie(self):
        """
        Demande le lancement de l'algorithme sur la grille modifiée
        puis demande l'affichage de la fenêtre correspondant à une volonté de modifier la grille,
        pour ne pas perdre la position actuelle
        """
        self.parent.lancer_grille(0)
        self.parent.modifier_grille()

    def lancer_statistiques(self):
        """
        Entrée dans les requêtes de statistiques par l'utilisateur
        Demande la variable que veut étudier l'utilisateur : la taille de la grille ou le nombre d'obstacles
        """
        self.clean()
        label = Label(self, text="Quelles statistiques voulez-vous lancer ?")
        btn_taille = Button(self, text="En fonction de la taille de la grille\nsur des instances aléatoires",
                            command=self.stats_taille)
        btn_obstacles = Button(self, text="En fonction du nombre d'obstacles\nsur des instances aléatoires",
                               command=self.stats_obstacles)
        btn_creer_instances = Button(self, text="Créer un fichier qui servira\nde base de données de référence",
                                     command=self.stats_creer_instances)
        btn_lancer_instance = Button(self, text="Lancer un statistiques sur\nun fichier créé préalablement",
                                     command=self.stats_ouvrir_instances)
        label.grid(column=0, row=0)
        btn_taille.grid(column=0, row=1)
        btn_obstacles.grid(column=0, row=2)
        btn_creer_instances.grid(column=0, row=3)
        btn_lancer_instance.grid(column=0, row=4)

    def stats_taille(self):
        """
        Demande à l'utilisateur les données nécessaire au calcul des statistiques en fonction de la taille des grilles
        """
        self.clean()

        # Définition des variables nécessaires
        taille_min = IntVar()
        taille_min.set(10)
        taille_max = IntVar()
        taille_max.set(10)
        pas = IntVar()
        pas.set(10)
        echelle_ord = StringVar()
        echelle_ord.set("log")
        echelle_abs = StringVar()
        echelle_abs.set("log")

        # Création des éléments demandant les variables à l'utilisateur
        label = Label(self, text="Statistiques en fonction de la taille de la grille")
        label_min = Label(self, text="Taille minimale de la grille :")
        spin_taille_min = Spinbox(self, from_=10, to=100, increment=10, textvariable=taille_min)
        label_max = Label(self, text="Taille maximale de la grille :")
        spin_taille_max = Spinbox(self, from_=50, to=4000, increment=10, textvariable=taille_max)
        label_pas = Label(self, text="Pas d'incrément de taille de la grille :")
        spin_pas = Spinbox(self, from_=10, to=1000, increment=10, textvariable=pas)
        label_echelle = Label(self, text="Echelle de l'axe du temps :")
        radio_linear = Radiobutton(self, text="Linéaire", variable=echelle_ord, value="linear")
        radio_log = Radiobutton(self, text="Logarithmique", variable=echelle_ord, value="log")
        label_echelle_abs = Label(self, text="Echelle de l'axe des tailles :")
        radio_linear_abs = Radiobutton(self, text="Linéaire", variable=echelle_abs, value="linear")
        radio_log_abs = Radiobutton(self, text="Logarithmique", variable=echelle_abs, value="log")
        btn_lancement = Button(self, text="Lancer !",
                               command=lambda: self.parent.lancer_stats_taille(spin_taille_min.get(), spin_taille_max.get(), spin_pas.get(), echelle_ord.get(), echelle_abs.get()))

        # Positionnement de ces éléments
        label.grid(column=0, row=0, columnspan=3)
        label_min.grid(column=0, row=1)
        spin_taille_min.grid(column=1, row=1, columnspan=2)
        label_max.grid(column=0, row=2)
        spin_taille_max.grid(column=1, row=2, columnspan=2)
        label_pas.grid(column=0, row=3)
        spin_pas.grid(column=1, row=3, columnspan=2)
        label_echelle.grid(column=0, row=4)
        radio_linear.grid(column=1, row=4)
        radio_log.grid(column=2, row=4)
        label_echelle_abs.grid(column=0, row=5)
        radio_linear_abs.grid(column=1, row=5)
        radio_log_abs.grid(column=2, row=5)
        btn_lancement.grid(column=1, row=6)

    def stats_obstacles(self):
        """
        Demande à l'utilisateur les données nécessaire au calcul des statistiques en fonction du nombre d'obstacles
        """
        self.clean()

        # Définition des variables nécessaires
        taille_grille = IntVar()
        taille_grille.set(10)
        max_obstacles = IntVar()
        max_obstacles.set(10)
        pas = IntVar()
        pas.set(10)
        echelle_ord = StringVar()
        echelle_ord.set("log")
        echelle_abs = StringVar()
        echelle_abs.set("log")

        # Création des éléments demandant les variables à l'utilisateur
        label = Label(self, text="Statistiques en fonction du nombre d'obstacles")
        label_taille = Label(self, text="Taille de la grille :")
        spin_taille = Spinbox(self, from_=10, to=100, increment=10, textvariable=taille_grille)
        label_max = Label(self, text="Nombre maximum d'obstacles :")
        spin_max_obstacles = Spinbox(self, from_=50, to=150, increment=10, textvariable=max_obstacles)
        label_pas = Label(self, text="Pas d'incrément du nombre d'obstacles :")
        spin_pas = Spinbox(self, from_=10, to=140, increment=10, textvariable=pas)
        label_echelle = Label(self, text="Echelle de l'axe du temps :")
        radio_linear = Radiobutton(self, text="Linéaire", variable=echelle_ord, value="linear")
        radio_log = Radiobutton(self, text="Logarithmique", variable=echelle_ord, value="log")
        label_echelle_abs = Label(self, text="Echelle de l'axe du nombre d'obstacles :")
        radio_linear_abs = Radiobutton(self, text="Linéaire", variable=echelle_abs, value="linear")
        radio_log_abs = Radiobutton(self, text="Logarithmique", variable=echelle_abs, value="log")
        btn_lancement = Button(self, text="Lancer !",
                               command=lambda: self.parent.lancer_stats_obstacles(spin_taille.get(), spin_max_obstacles.get(), spin_pas.get(), echelle_ord.get(), echelle_abs.get()))

        # Positionnement de ces éléments
        label.grid(column=0, row=0, columnspan=3)
        label_taille.grid(column=0, row=1)
        spin_taille.grid(column=1, row=1, columnspan=2)
        label_max.grid(column=0, row=2)
        spin_max_obstacles.grid(column=1, row=2, columnspan=2)
        label_pas.grid(column=0, row=3)
        spin_pas.grid(column=1, row=3, columnspan=2)
        label_echelle.grid(column=0, row=4)
        radio_linear.grid(column=1, row=4)
        radio_log.grid(column=2, row=4)
        label_echelle_abs.grid(column=0, row=5)
        radio_linear_abs.grid(column=1, row=5)
        radio_log_abs.grid(column=2, row=5)
        btn_lancement.grid(column=1, row=6)

    def stats_creer_instances(self):
        """
        Demande à l'utilisateur quel type de base de données il veut créer :
        en fonction de la taille ou du nombre d'obstacles
        """
        self.clean()
        label = Label(self, text="Voulez-vous créer des instances pour des statistiques en fonction de :")
        btn_taille = Button(self, text="La taille", command=self.stats_creer_instances_taille)
        btn_obstacles = Button(self, text="Le nombre d'obstacles", command=self.stats_creer_instances_obstacles)

        label.grid(column=0, row=0, columnspan=2)
        btn_taille.grid(column=0, row=1)
        btn_obstacles.grid(column=1, row=1)

    def stats_creer_instances_taille(self):
        """
        Demande à l'utilisateur les informations nécessaires pour créer les instances demandées pour les statistiques
        en fonction de la taille de la grille
        """
        self.clean()
        # Définitions des variables nécessaires
        taille_min = IntVar()
        taille_max = IntVar()
        pas = IntVar()
        nb_instances = IntVar()
        taille_min.set(10)
        taille_max.set(50)
        pas.set(10)
        nb_instances.set(10)
        # Définition des widgets à afficher
        label_min = Label(self, text="Taille minimale des grilles :")
        label_max = Label(self, text="Taille maximale des grilles :")
        label_pas = Label(self, text="Pas entre deux tailles de grilles :")
        label_nb_instances = Label(self, text="Nombre d'instances par taille à générer :")
        spin_min = Spinbox(self, from_=10, to=200, textvariable=taille_min)
        spin_max = Spinbox(self, from_=20, to=500, textvariable=taille_max)
        spin_pas = Spinbox(self, from_=10, to=500, textvariable=pas)
        spin_nb_instances = Spinbox(self, from_=10, to=100, textvariable=nb_instances)
        label = Label(self, text="Dans quel fichier voulez-vous écrire ces instances ?")
        entry = Entry(self, textvariable=self.parent.sortie)
        bouton = Button(self, text="Choisir parmi les fichiers",
                        command=lambda: self.parent.sortie.set(choisir_fichier("Choisir le fichier où écrire")))
        btn_lancement = Button(self, text="Générer la base de données",
                               command=lambda: self.stats_generer_instances_taille(spin_min.get(), spin_max.get(), spin_pas.get(), spin_nb_instances.get(), self.parent.sortie.get()))
        # Placement des widgets à afficher
        label_min.grid(column=0, row=0, columnspan=2)
        spin_min.grid(column=2, row=0)
        label_max.grid(column=0, row=1, columnspan=2)
        spin_max.grid(column=2, row=1)
        label_pas.grid(column=0, row=2, columnspan=2)
        spin_pas.grid(column=2, row=2)
        label_nb_instances.grid(column=0, row=3, columnspan=2)
        spin_nb_instances.grid(column=2, row=3)
        label.grid(column=0, row=4, columnspan=3)
        entry.grid(column=0, row=5, columnspan=2)
        bouton.grid(column=2, row=5)
        btn_lancement.grid(column=0, row=6, columnspan=3)

    def stats_generer_instances_taille(self, min_taille, max_taille, pas, nb_instances, fichier):
        grilles = generer_base_statistiques_taille(int(min_taille), int(max_taille), int(pas), int(nb_instances))
        print(grilles)
        ecriture_grilles(grilles, fichier)
        self.clean()
        label = Label(self, text="Instances générées et écrites dans le fichier")
        label.grid()

    def stats_creer_instances_obstacles(self):
        """
        Demande à l'utilisateur les informations nécessaires pour créer les instances demandées pour les statistiques
        en fonction du nombre d'obstacles des grilles
        """
        self.clean()
        # Définitions des variables nécessaires
        taille = IntVar()
        min_obstacles = IntVar()
        max_obstacles = IntVar()
        pas = IntVar()
        nb_instances = IntVar()
        taille.set(20)
        min_obstacles.set(20)
        max_obstacles.set(240)
        pas.set(10)
        nb_instances.set(10)
        # Définition des widgets à afficher
        label_taille = Label(self, text="Taille des instances générées :")
        label_min = Label(self, text="Nombre minimal d'obstacles :")
        label_max = Label(self, text="Nombre maximal d'obstacles :")
        label_pas = Label(self, text="Pas entre deux nombres d'obstacles :")
        label_nb_instances = Label(self, text="Nombre d'instances par nombre d'obstacles à générer :")
        spin_taille = Spinbox(self, from_=10, to=500, textvariable=taille)
        spin_min = Spinbox(self, from_=10, to=200, textvariable=min_obstacles)
        spin_max = Spinbox(self, from_=20, to=500, textvariable=max_obstacles)
        spin_pas = Spinbox(self, from_=10, to=500, textvariable=pas)
        spin_nb_instances = Spinbox(self, from_=10, to=100, textvariable=nb_instances)
        label = Label(self, text="Dans quel fichier voulez-vous écrire ces instances ?")
        entry = Entry(self, textvariable=self.parent.sortie)
        bouton = Button(self, text="Choisir parmi les fichiers",
                        command=lambda: self.parent.sortie.set(choisir_fichier("Choisir le fichier où écrire")))
        btn_lancement = Button(self, text="Générer la base de données",
                               command=lambda: self.stats_generer_instances_obstacles(taille.get(), min_obstacles.get(), max_obstacles.get(), pas.get(), nb_instances.get(), self.parent.sortie.get()))
        # Placement des widgets à afficher
        label_taille.grid(column=0, row=0, columnspan=2)
        spin_taille.grid(column=2, row=0)
        label_min.grid(column=0, row=1, columnspan=2)
        spin_min.grid(column=2, row=1)
        label_max.grid(column=0, row=2, columnspan=2)
        spin_max.grid(column=2, row=2)
        label_pas.grid(column=0, row=3, columnspan=2)
        spin_pas.grid(column=2, row=3)
        label_nb_instances.grid(column=0, row=4, columnspan=2)
        spin_nb_instances.grid(column=2, row=4)
        label.grid(column=0, row=5, columnspan=3)
        entry.grid(column=0, row=6, columnspan=2)
        bouton.grid(column=2, row=6)
        btn_lancement.grid(column=0, row=7, columnspan=3)

    def stats_generer_instances_obstacles(self, taille, min_obstacles, max_obstacles, pas, nb_instances, fichier):
        grilles = generer_base_statistiques_obstacles(int(taille), int(min_obstacles), int(max_obstacles),
                                                      int(pas), int(nb_instances))
        ecriture_grilles(grilles, fichier)
        self.clean()
        label = Label(self, text="Instances générées et écrites dans le fichier")
        label.grid()

    def stats_ouvrir_instances(self):
        """
        Demande à l'utilisateur quelle base de données il veut ouvrir, et de quel type elle est
        :return:
        """
        self.clean()
        # Définition des variables
        type_stats = StringVar()
        type_stats.set("taille")
        # Définition des widgets à afficher
        label = Label(self, text="Quel fichier ouvrir ?")
        entry = Entry(self, textvariable=self.parent.entree)
        bouton = Button(self, text="Choisir parmi les fichiers",
                        command=lambda: self.parent.entree.set(choisir_fichier("Choisir le fichier à ouvrir")))
        label_type = Label(self, text="Quel est le type de statistiques à réaliser sur les instances de ce fichier ?")
        radio_taille = Radiobutton(self, text="En fonction de la taille", variable=type_stats, value="taille")
        radio_obstacles = Radiobutton(self, text="En fonction du nombre d'obstacles",
                                      variable=type_stats, value="obstacles")
        btn_lancement = Button(self, text="Lancer le calcul !",
                               command=lambda: self.stats_affiche_base_donnees(self.parent.entree.get(), type_stats.get()))
        # Placement des widgets
        label.grid(column=0, row=0, columnspan=4)
        entry.grid(column=0, row=1, columnspan=3)
        bouton.grid(column=3, row=1)
        label_type.grid(column=0, row=2, columnspan=4)
        radio_taille.grid(column=0, row=3, columnspan=2)
        radio_obstacles.grid(column=2, row=3, columnspan=2)
        btn_lancement.grid(column=0, row=4, columnspan=4)

    def stats_affiche_base_donnees(self, fichier, type):
        if type == "taille":
            self.parent.lancer_stats_base_donnees_taille(fichier)
        else:
            self.parent.lancer_stats_base_donnees_obstacles(fichier)

    def stats_demande_echelle_taille(self, tailles, tps_creation, tps_calcul):
        self.clean()
        echelle_ord = StringVar()
        echelle_abs = StringVar()
        echelle_ord.set("log")
        echelle_abs.set("log")
        label = Label(self, text="Changer l'échelle du graphique ?")
        label_ord = Label(self, text="Axe des ordonnées :")
        label_abs = Label(self, text="Axe des abscisses :")
        radio_ord_lin = Radiobutton(self, text="Linéaire", variable=echelle_ord, value="linear")
        radio_ord_log = Radiobutton(self, text="Logarithmique", variable=echelle_ord, value="log")
        radio_abs_lin = Radiobutton(self, text="Linéaire", variable=echelle_abs, value="linear")
        radio_abs_log = Radiobutton(self, text="Logarithmique", variable=echelle_abs, value="log")
        btn_valider = Button(self, text="Mettre à jour le graphique",
                             command=lambda: self.parent.afficher_stats_taille(tailles, tps_creation, tps_calcul, echelle_ord.get(), echelle_abs.get()))

        label.grid(column=0, row=0, columnspan=2)
        label_ord.grid(column=0, row=1, columnspan=2)
        radio_ord_lin.grid(column=0, row=2)
        radio_ord_log.grid(column=1, row=2)
        label_abs.grid(column=0, row=3, columnspan=2)
        radio_abs_lin.grid(column=0, row=4)
        radio_abs_log.grid(column=1, row=4)
        btn_valider.grid(column=0, row=5, columnspan=2)

    def stats_demande_echelle_obstacles(self, taille, nb_obstacles, tps_creation, tps_calcul):
        self.clean()
        echelle_ord = StringVar()
        echelle_abs = StringVar()
        echelle_ord.set("log")
        echelle_abs.set("log")
        label = Label(self, text="Changer l'échelle du graphique ?")
        label_ord = Label(self, text="Axe des ordonnées :")
        label_abs = Label(self, text="Axe des abscisses :")
        radio_ord_lin = Radiobutton(self, text="Linéaire", variable=echelle_ord, value="linear")
        radio_ord_log = Radiobutton(self, text="Logarithmique", variable=echelle_ord, value="log")
        radio_abs_lin = Radiobutton(self, text="Linéaire", variable=echelle_abs, value="linear")
        radio_abs_log = Radiobutton(self, text="Logarithmique", variable=echelle_abs, value="log")
        btn_valider = Button(self, text="Mettre à jour le graphique",
                             command=lambda: self.parent.afficher_stats_obstacles(taille, nb_obstacles, tps_creation, tps_calcul, echelle_ord.get(), echelle_abs.get()))

        label.grid(column=0, row=0, columnspan=2)
        label_ord.grid(column=0, row=1, columnspan=2)
        radio_ord_lin.grid(column=0, row=2)
        radio_ord_log.grid(column=1, row=2)
        label_abs.grid(column=0, row=3, columnspan=2)
        radio_abs_lin.grid(column=0, row=4)
        radio_abs_log.grid(column=1, row=4)
        btn_valider.grid(column=0, row=5, columnspan=2)

    def enregistrer_grille(self, numero_grille):
        self.clean()

        label = Label(self, text="Dans quel fichier voulez-vous enregistrer cette grille ?")
        entry = Entry(self, textvariable=self.parent.sortie)
        bouton = Button(self, text="Choisir parmi les fichiers",
                        command=lambda: self.parent.entree.set(choisir_fichier("Choisir le fichier où écrire la grille")))
        btn_lancement = Button(self, text="Lancer l'écriture",
                               command=lambda: self.parent.ecrire_grille(numero_grille))
        label.grid(column=0, row=0, columnspan=3)
        entry.grid(column=0, row=1, columnspan=2)
        bouton.grid(column=2, row=1)
        btn_lancement.grid(column=0, row=2, columnspan=3)



class BoutonMenuPrincipal(Frame):
    """
    Classe servant uniquement à afficher en permanence un bouton en bas à droite permettant de revenir au menu principal
    """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        bouton_menu = Button(self, text="Retour au menu principal", command=self.parent.menu_principal)
        bouton_menu.pack(side=BOTTOM)


class FenetrePrincipale(Tk):
    """
    Classe créant la fenêtre principal et gérant les requêtes des parties gauches et droites pour modifier les données
    """
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.entree = StringVar()
        self.sortie = StringVar()
        self.entree.set("Instances/x9y10o10.dat")
        self.sortie.set("Instances/Résultats/x9y10o10out.dat")
        self.grilles = []
        self.update_grilles()
        self.menu = TopMenu(self)
        self.rightFrame = RightFrame(self)
        self.leftFrame = LeftFrame(self)
        self.bouton_menu_principal = BoutonMenuPrincipal(self)
        self.leftFrame.pack(side=LEFT, padx=10, pady=10)
        self.rightFrame.pack(side=TOP, padx=10, pady=10)
        self.bouton_menu_principal.pack(side=BOTTOM, padx=10, pady=10)
        self.menu_principal()

    def update_grilles(self):
        """
        Met à jour les grilles courantes en fonction du fichier d'entrée
        Cette fonction est appelée après modification (ou création) de la variable correspondant au fichier d'entrée
        """
        self.grilles = get_grilles(self.entree.get())

    def menu_principal(self):
        """
        Affiche le menu principal demandant à l'utilisateur quelle est son intention
        """
        self.rightFrame.choice_buttons()

    def lancer_fichier(self):
        """
        Affiche la partie droite correspondant au lancement de l'algorithme depuis un fichier
        ou une grille contenue dans un fichier
        """
        self.rightFrame.ouvrir_fichiers()

    def lancer_algo(self):
        """
        Lance l'algorithme pour trouver le chemin le plus rapide dans toutes les grilles du fichier d'entrée
        Ecrit le résultat dans le fichier de sortie
        Ecrit le résultat dans la partie gauche de la fenêtre
        """
        # On vérifie que le fichier d'entrée existe bien
        if os.path.isfile(self.entree.get()):
            # Si le fichier de sortie existe, on demande à l'utilisateur s'il est sûr de vouloir l'écraser
            if os.path.isfile(self.sortie.get()):
                if not askyesno("Fichier existant", "Le fichier " + self.sortie.get() + " existe déjà, la procédure effacera son contenu, voulez-vous vraiment choisir ce fichier ?"):
                    return
            # Ecriture du résultat dans le fichier d'entrée s'il est spécifié
            if self.sortie.get() != '':
                resultat, tps_creat, tps_calc = lecture(self.entree.get(), self.sortie.get())
                self.leftFrame.afficher_resultat(resultat, tps_creat, tps_calc)
            else:
                showerror("Erreur Fichiers", "Le fichier de sortie est incorrect")
        else:
            showerror("Erreur Fichiers", "Le fichier d'entrée est introuvable")

    def afficher_grille(self, numero_grille):
        """
        Demande à la frame gauche d'afficher la grille demandée
        :param numero_grille: indice de la grille à afficher
        :type numero_grille: int
        """
        grille = self.grilles[numero_grille]
        self.leftFrame.affiche_grille(grille)
        self.leftFrame.rescale()

    def lancer_grille(self, numero_grille):
        """
        Lance l'algorithme trouvant le chemin le plus rapide dans la grille demandée
        et affiche ce chemin dans la frame gauche
        :param numero_grille: indice de la grille sur laquelle calculer le chemin le plus rapide à afficher
        :type numero_grille: int
        """
        grille = self.grilles[numero_grille]
        chemin_list, chemin_str = lancement_et_chemin(grille)
        self.leftFrame.affiche_chemin(grille, chemin_list, chemin_str)

    def creer_grille(self):
        """
        Demande à la frame droite d'afficher les possibilités liées à la création aléatoire ou manuelle d'une grille
        """
        self.rightFrame.creer_grille()

    def modifier_grille(self):
        """
        Demande aux frames gauche et droite d'afficher leurs états en liens avec la modification d'une grille
        """
        # Pas besoin d'afficher, elle l'est déjà normalement...
        # self.leftFrame.affiche_grille()
        self.leftFrame.modifier_grille()
        self.rightFrame.modifier_grille()

    def generer_grille(self):
        """
        Génère une grille avec les données récupérées par la frame droite et l'affiche
        """
        # Génération d'une grille aléatoire
        self.grilles = [generer_grille(self.rightFrame.nb_lignes.get(),
                                       self.rightFrame.nb_colonnes.get(),
                                       self.rightFrame.nb_obstacles.get())]
        self.leftFrame.affiche_grille(self.grilles[0])
        self.leftFrame.rescale()
        self.modifier_grille()

    def lancer_statistiques(self):
        """
        Demande à la frame droite d'afficher les possibilités qu'a l'utilisateur quant aux statistiques
        """
        self.rightFrame.lancer_statistiques()

    def lancer_stats_taille(self, min_taille, max_taille, pas, echelle_ord, echelle_abs):
        """
        Lance le calcul des statistiques du temps d'exécution en fonction de la taille de la grille
        :param min_taille: taille minimale de la grille
        :param max_taille: taille maximale de la grille
        :param pas: pas de taille entre chaque calcul de statistiques
        :param echelle_ord: échelle à utiliser (linéaire ou logarithmique) pour l'axe des ordonnées
        :param echelle_abs: échelle à utiliser (linéaire ou logarithmique) pour l'axe des abscisses
        :type min_taille: str
        :type max_taille: str
        :type pas: str
        :type echelle_ord: str
        :type echelle_abs: str
        """
        self.leftFrame.affiche_patienter()
        tailles, tps_creation, tps_calcul = recup_stats_taille(int(min_taille), int(max_taille), int(pas))
        self.afficher_stats_taille(tailles, tps_creation, tps_calcul, echelle_ord, echelle_abs)
        self.rightFrame.stats_demande_echelle_taille(tailles, tps_creation, tps_calcul)

    def lancer_stats_obstacles(self, taille_grille, max_obstacles, pas, echelle_ord, echelle_abs):
        """
        Lance le calcul des statistiques du temps d'exécution en fonction du nombre d'obstacles de la grille,
        la taille de la grille restant fixe
        :param taille_grille: taille des grilles à générer pour les calculs
        :param max_obstacles: nombre maximum d'obstacles
        :param pas: pas du nombre d'obstacles entre chaque calcul de statistiques
        :param echelle_ord: échelle à utiliser (linéaire ou logarithmique) pour l'axe des ordonnées
        :param echelle_abs: échelle à utiliser (linéaire ou logarithmique) pour l'axe des abscisses
        :type taille_grille: str
        :type max_obstacles: str
        :type pas: str
        :type echelle_ord: str
        :type echelle_abs: str
        """
        self.leftFrame.affiche_patienter()
        nb_obstacles, tps_creation, tps_calcul = recup_stats_obstacles(int(taille_grille),
                                                                               int(max_obstacles), int(pas))
        self.afficher_stats_obstacles(taille_grille, nb_obstacles, tps_creation, tps_calcul, echelle_ord, echelle_abs)
        self.rightFrame.stats_demande_echelle_obstacles(taille_grille, nb_obstacles, tps_creation, tps_calcul)

    def lancer_stats_base_donnees_taille(self, fichier):
        """
        Lance le calcul puis demande l'affichage des statistiques depuis un fichier base de données
        :param fichier: chemin du fichier base de données dont on veut les statistiques
        :type fichier: str
        """
        self.leftFrame.affiche_patienter()
        tailles, tps_creation, tps_calcul = recup_stats_fichier_taille(fichier)
        self.afficher_stats_taille(tailles, tps_creation, tps_calcul)
        self.rightFrame.stats_demande_echelle_taille(tailles, tps_creation, tps_calcul)

    def afficher_stats_taille(self, tailles, tps_creation, tps_calcul,
                              echelle_ord='linear', echelle_abs='linear'):
        f = Figure()
        titre = "Temps d'exécution en fonction de\nla taille d'un côté de la grille"
        plt = f.add_subplot(111, title=titre, ylabel="Temps", xlabel="Taille de la grille",
                            yscale=echelle_ord, xscale=echelle_abs)
        affiche_stats(tailles, tps_creation, tps_calcul, plt)
        self.leftFrame.affiche_plot(f)

    def lancer_stats_base_donnees_obstacles(self, fichier):
        """
        Lance le calcul puis demande l'affichage des statistiques depuis un fichier base de données
        :param fichier: chemin du fichier base de données dont on veut les statistiques
        :type fichier: str
        """
        self.leftFrame.affiche_patienter()
        taille, nb_obstacles, tps_creation, tps_calcul = recup_stats_fichier_obstacles(fichier)
        self.afficher_stats_obstacles(taille, nb_obstacles, tps_creation, tps_calcul)
        self.rightFrame.stats_demande_echelle_obstacles(taille, nb_obstacles, tps_creation, tps_calcul)

    def afficher_stats_obstacles(self, taille, nb_obstacles, tps_creation, tps_calcul,
                                 echelle_ord='linear', echelle_abs='linear'):
        f = Figure()
        titre = "Temps d'exécution d'une grille de " + str(taille) + " de côté\nen fonction du nombre d'obstacles"
        plt = f.add_subplot(111, title=titre, ylabel="Temps", xlabel="Nombre d'obstacles",
                            yscale=echelle_ord, xscale=echelle_abs)
        affiche_stats(nb_obstacles, tps_creation, tps_calcul, plt)
        self.leftFrame.affiche_plot(f)

    def enregistrer_grille(self, numero_grille):
        self.rightFrame.enregistrer_grille(numero_grille)

    def ecrire_grille(self, numero_grille):
        ecriture_grilles([self.grilles[numero_grille]], self.sortie.get())
        self.rightFrame.clean()
        label = Label(self.rightFrame, text="Grille écrite dans le fichier")
        label.grid()


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


def affichage_fenetre():
    """
    Fonction d'accès à l'IHM. Il suffit d'appeler cette méthode pour afficher la fenêtre principale
    """
    fenetre = FenetrePrincipale(None)
    fenetre.title("Robot Ride !")
    fenetre.mainloop()
