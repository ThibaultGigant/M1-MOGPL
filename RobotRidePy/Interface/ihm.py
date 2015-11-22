from tkinter.filedialog import *
from tkinter.messagebox import *
from Robot.file_gestion import lecture
import os

apropos_message = """Ce programme est un projet réalisé par Thibault Gigant pour le projet de MOGPL en 2015
Le but de ce programme est de trouver le chemin le plus rapide d'un robot dans un entrepôt entre deux points"""
fenetre = None
entree = ""
sortie = "NomFichierSortie"
opened_widgets = []


def clear_fenetre():
    global opened_widgets
    for i in opened_widgets:
        if i:
            i.destroy()


def apropos():
    showinfo("Robot Ride !", apropos_message)


def choisir_fichier(titre):
    return askopenfilename(title=titre, filetypes=[('dat files', '*.dat'), ('all files', '.*')])


def affichage_resultat(liste):
    clear_fenetre()
    for i in liste:
        label = Label(fenetre, text=i)
        label.pack(side=TOP)
        opened_widgets.append(label)
    bouton = Button(fenetre, text="Menu Principal", command=menu_principal)
    bouton.pack(side=BOTTOM)
    opened_widgets.append(bouton)


def get_sortie(widget):
    global sortie
    if widget is not None:
        sortie = widget.get()
    else:
        sortie = choisir_fichier("Choisir un fichier de sortie")
    while os.path.isfile(sortie):
        if askyesno("Fichier existant", "Le fichier " +
                    sortie +
                    " existe déjà, la procédure effacera son contenu, voulez-vous vraiment choisir ce fichier ?"):
            break
        else:
            if widget:
                sortie = widget.get()
            else:
                sortie = choisir_fichier("Choisir un fichier de sortie")
    if entree and sortie:
        retour = lecture(entree, sortie)
    else:
        showerror("Erreur Fichiers", "Les fichiers indiqués sont incorrects")
    affichage_resultat(retour)


def lancer_fichier():
    global entree, sortie, opened_widgets
    clear_fenetre()
    entree = choisir_fichier("Choisir un fichier en Entrée")
    open_button = Button(fenetre, text="Choisir un fichier existant", command=lambda: get_sortie(None))
    open_button.pack(side=TOP)
    label = Label(fenetre, text="OU")
    label.pack(side=TOP)
    value = StringVar()
    value.set(sortie)
    text = Entry(fenetre, textvariable=value)
    text.pack(side=LEFT)
    validate_button = Button(fenetre, text="Valider", command=lambda: get_sortie(text))
    validate_button.pack(side=RIGHT)
    opened_widgets.append(label)
    opened_widgets.append(text)
    opened_widgets.append(open_button)
    opened_widgets.append(validate_button)


# def creer_instances():


def ajoute_menu():
    menubar = Menu(fenetre)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Ouvrir", command=lancer_fichier)
    # menu1.add_command(label="Créer", command=lancer_base)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=fenetre.quit)
    menubar.add_cascade(label="Fichier", menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label="A propos", command=apropos)
    menubar.add_cascade(label="Aide", menu=menu2)

    fenetre.config(menu=menubar)


def choice_buttons():
    open_button = Button(fenetre, text="Récupérer un problème depuis un fichier", command=lancer_fichier)
    create_button = Button(fenetre, text="Créer manuellement un problème", command=lancer_fichier)
    opened_widgets.append(open_button)
    opened_widgets.append(create_button)
    open_button.pack()
    create_button.pack()


def menu_principal():
    clear_fenetre()
    choice_buttons()


def affichage_fenetre():
    global fenetre
    fenetre = Tk()
    fenetre.title("Robot Ride !")
    ajoute_menu()
    menu_principal()
    fenetre.mainloop()
