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
from Robot.file_gestion import *
from Generation.generation import *

from .statics import *


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
        bouton_maj = Button(self, text="Mise à jour des grilles", command=self.update_widget_grilles)
        bouton_maj.grid(column=2, row=6, columnspan=2)
        self.update_widget_grilles()

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
        """
        Lance l'interface permettant de modifier la grille choisie dans la liste déroulante
        :param numero_grille: indice de la grille dans la liste
        :type numero_grille: int
        """
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
        btn_lancer_instance = Button(self, text="Lancer des statistiques sur\nun fichier créé préalablement",
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
        """
        Génère des grilles aléatoires avec les paramètres spécifiés en vue de créer une base de données statistiques
        puis les écrit dans un fichier
        :param min_taille: taille minimale des grilles
        :param max_taille: taille maximale des grilles
        :param pas: pas entre deux tailles de grille
        :param nb_instances: nombre d'instances créées pour chaque catégorie
        :param fichier: fichier de sortie où écrire le résultat
        :type min_taille: str
        :type max_taille: str
        :type pas: str
        :type nb_instances: str
        :type fichier: str
        """
        grilles = generer_base_statistiques_taille(int(min_taille), int(max_taille), int(pas), int(nb_instances))
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
        """
        Génère des grilles aléatoires avec les paramètres spécifiés en vue de créer une base de données statistiques
        puis les écrit dans un fichier
        :param taille: taille des grilles à générer
        :param min_obstacles: nombre minimal d'obstacles présents dans les grilles
        :param max_obstacles: nombre maximal d'obstacles présents dans les grilles
        :param pas: pas entre deux quantités d'obstacles par grille
        :param nb_instances: nombre d'instances créées pour chaque catégorie
        :param fichier: fichier de sortie où écrire le résultat
        :type taille: str
        :type min_obstacles: str
        :type max_obstacles: str
        :type pas: str
        :type nb_instances: str
        :type fichier: str
        """
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
        """
        Lance le programme menant à l'affichage d'une base de données récupérée dans un fichier,
        selon le type de statistiques voulu
        :param fichier: fichier où récupérer les données
        :param type: type de statistiques = en fonction de la taille des grilles ou du nombre d'obstacles
        :type fichier: str
        :type type: str
        """
        if type == "taille":
            self.parent.lancer_stats_base_donnees_taille(fichier)
        else:
            self.parent.lancer_stats_base_donnees_obstacles(fichier)

    def stats_demande_echelle_taille(self, tailles, tps_creation, tps_calcul):
        """
        Permet la modification de l'échelle du graphe situé en partie gauche
        sur un graphe dépendant de la taille
        :param tailles: tableau des tailles des grilles
        :param tps_creation: tableau recensant les temps de création des grilles
        :param tps_calcul: tableau recensant les temps de calcul des grilles
        :type tailles: np.array
        :type tps_creation: np.array
        :type tps_calcul: np.array
        """
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
        """
        Permet la modification de l'échelle du graphe situé en partie gauche
        sur un graphe dépendant du nombre d'obstacles
        :param taille: taille des grilles
        :param nb_obstacles: tableau représentant les nombres d'obstacles des graphes
        :param tps_creation: tableau représentant les temps de création des graphes selon les nombres d'obstacles
        :param tps_calcul: tableau représentant les temps de calcul des graphes selon les nombres d'obstacles
        :type taille: int
        :type nb_obstacles: np.array
        :type tps_creation: np.array
        :type tps_calcul: np.array
        """
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
        """
        Permet l'enregistrement d'une grille dont l'indice dans la liste des grilles est passé en paramètres
        :param numero_grille: indice de la grille dans la liste des grilles en self.parent.grilles
        :type numero_grille: int
        """
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
