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
import matplotlib
matplotlib.use('TkAgg')


apropos_message = """Ce programme est un projet réalisé par Thibault Gigant pour le projet de MOGPL en 2015
Le but de ce programme est de trouver le chemin le plus rapide d'un robot entre deux points d'un dépôt"""


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

