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
from Stats.stats import *
from matplotlib.figure import Figure

from .top_menu import TopMenu
from .left_frame import LeftFrame
from .right_frame import RightFrame


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
        """
        Provoque l'apparition du graphique du temps en fonction de la taille des graphes
        :param tailles: tableau des tailles de grilles
        :param tps_creation: tableau des temps de création de graphe
        :param tps_calcul: tableau des temps de calcul du chemin
        :param echelle_ord: échelle de l'axe des ordonnées à utiliser pour l'affichage
        :param echelle_abs: échelle de l'axe des abscisses à utiliser pour l'affichage
        :type tailles: np.array
        :type tps_creation: np.array
        :type tps_calcul: np.array
        :type echelle_ord: str
        :type echelle_abs: str
        """
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
        """
        Provoque l'apparition du graphique du temps en fonction du nombre d'obstacles
        :param taille: taille des grilles
        :param nb_obstacles: tableau du nombre d'obstacles
        :param tps_creation: tableau des temps de création des graphes
        :param tps_calcul: tableau des temps de calcul du chemin
        :param echelle_ord: échelle de l'axe des ordonnées à utiliser pour l'affichage
        :param echelle_abs: échelle de l'axe des abscisses à utiliser pour l'affichage
        :type taille: int
        :type nb_obstacles: np.array
        :type tps_creation: np.array
        :type tps_calcul: np.array
        :type echelle_ord: str
        :type echelle_abs: str
        """
        f = Figure()
        titre = "Temps d'exécution d'une grille de " + str(taille) + " de côté\nen fonction du nombre d'obstacles"
        plt = f.add_subplot(111, title=titre, ylabel="Temps", xlabel="Nombre d'obstacles",
                            yscale=echelle_ord, xscale=echelle_abs)
        affiche_stats(nb_obstacles, tps_creation, tps_calcul, plt)
        self.leftFrame.affiche_plot(f)

    def enregistrer_grille(self, numero_grille):
        """
        Provoque l'apparition d'un formulaire permettant d'enregistrer la grille passée en paramètre
        :param numero_grille: indice de la grille à enregistrer dans la liste des grilles
        :type numero_grille: int
        """
        self.rightFrame.enregistrer_grille(numero_grille)

    def ecrire_grille(self, numero_grille):
        """
        Provoque l'écriture de la grille dont le numéro est passé en paramètre
        :param numero_grille: indice de la grille à enregistrer dans la liste des grilles
        """
        ecriture_grilles([self.grilles[numero_grille]], self.sortie.get())
        self.rightFrame.clean()
        label = Label(self.rightFrame, text="Grille écrite dans le fichier")
        label.grid()


def affichage_fenetre():
    """
    Fonction d'accès à l'IHM. Il suffit d'appeler cette méthode pour afficher la fenêtre principale
    """
    fenetre = FenetrePrincipale(None)
    fenetre.title("Robot Ride !")
    fenetre.mainloop()
