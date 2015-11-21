from tkinter.filedialog import *
from tkinter.messagebox import *
from Robot.file_gestion import lecture
import os


apropos_message = """Ce programme est un projet réalisé par Thibault Gigant pour le projet de MOGPL en 2015
Le but de ce programme est de trouver le chemin le plus rapide d'un robot dans un entrepôt entre deux points"""
fenetre = None
entree = None
sortie = None


def apropos():
    showinfo("Robot Ride !", apropos_message)


def choisir_fichier(titre):
    return askopenfilename(title=titre, filetypes=[('dat files', '*.dat'), ('all files', '.*')])


def get_sortie(widget):
    global sortie
    if widget is not None:
        sortie = widget.get()
    else:
        sortie = choisir_fichier("Choisir un fichier de sortie")
    while os.path.isfile(sortie):
        if askyesno("Fichier existant", "Le fichier " + sortie + " existe déjà, la procédure effacera son contenu, voulez-vous vraiment choisir ce fichier ?"):
            break
        else:
            if widget:
                sortie = widget.get()
            else:
                sortie = choisir_fichier("Choisir un fichier de sortie")
    if entree and sortie:
        lecture(entree, sortie)
    else:
        showerror("Erreur Fichiers", "Les fichiers indiqués sont incorrects")


def lancer_base():
    global entree, sortie
    entree = choisir_fichier("Choisir un fichier en Entrée")
    value = StringVar()
    value.set("NomFichierSortie")
    text = Entry(fenetre, textvariable=value)
    text.pack(side=TOP)
    Button(fenetre, text="Choisir un fichier existant", command=lambda: get_sortie(None)).pack(side=LEFT)
    Button(fenetre, text="Valider", command=lambda: get_sortie(text)).pack(side=RIGHT)


#def creer_instances():


def ajoute_menu():
    menubar = Menu(fenetre)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Ouvrir", command=lancer_base)
    #menu1.add_command(label="Créer", command=lancer_base)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=fenetre.quit)
    menubar.add_cascade(label="Fichier", menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label="A propos", command=apropos)
    menubar.add_cascade(label="Aide", menu=menu2)

    fenetre.config(menu=menubar)


def affichage_fenetre():
    global fenetre
    fenetre = Tk()
    ajoute_menu()
    fenetre.mainloop()
