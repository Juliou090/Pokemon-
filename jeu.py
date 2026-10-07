"""Classe Jeu : chef d'orchestre de toute la partie.

On a le droit ici : enchaîner les grandes phases (accueil, création des équipes,
combat, fin) en appelant les autres modules.
On N'A PAS le droit : de calculer des dégâts, d'afficher avec print (voir ui/),
ou de connaître les détails d'une attaque ou d'un objet.
"""

from modeles.dresseur import Dresseur
from ui.affichage import Affichage
from ui.saisie import Saisie
from ui.exemples_affichage import *


class Jeu:
    """Enchaîne : accueil -> création des équipes -> combat -> fin (-> rejouer).

    Attributs prévus :
        # _affichage : Affichage   (seul objet qui affiche)
        # _saisie : Saisie         (seul objet qui lit le clavier)
        # _dresseurs : list[Dresseur]  (les 2 joueurs, vide au départ)
    """

    def __init__(self) -> None:
        """Prépare l'affichage et la saisie ; ne lance rien."""
        pass

    def lancer(self) -> None:
        """Boucle principale : accueil, création, combat, proposition de rejouer."""
        largeur = 72

        # 1. On efface l'écran pour partir d'une page propre.
        OutilsAffichage.effacer_ecran()
        print()

        # 2. La Poké Ball. pokeball() renvoie une LISTE de lignes : on fait un
        #    print par ligne avec une boucle for.
        for ligne in OutilsAffichage.pokeball(largeur):
            print(ligne)
        print()

        # 3. Le titre, centré et en jaune (titre_centre() renvoie UNE ligne).
        print(OutilsAffichage.titre_centre("SIMULATEUR DE COMBAT POKÉMON",
                                           largeur, Couleurs.JAUNE))

        # 4. Le sous-titre en gris. On calcule la marge à la main pour le centrer :
        #    on mesure le texte AVANT de le colorer (les codes de couleur
        #    sont invisibles mais compteraient dans len()).
        sous_titre = "Génération 3  ·  Rubis / Saphir"
        marge = " " * ((largeur - len(sous_titre)) // 2)
        print(marge + OutilsAffichage.colorer(sous_titre, Couleurs.GRIS))
        print()

        # 5. Un cadre de bienvenue : on prépare la liste des lignes, puis cadre()
        #    renvoie les lignes entourées d'un cadre à afficher une par une.
        lignes_du_cadre = []
        lignes_du_cadre.append("Un combat Pokémon au tour par tour, à deux joueurs.")
        lignes_du_cadre.append("")
        lignes_du_cadre.append(OutilsAffichage.colorer("Au programme :", Couleurs.GRAS))
        lignes_du_cadre.append("  • chacun choisit son mode de création d'équipe")
        lignes_du_cadre.append("  • attaquer, changer de Pokémon ou utiliser un objet")
        lignes_du_cadre.append("  • le dernier dresseur debout gagne !")
        lignes_du_cadre.append("")

        # Les types colorés, côte à côte, comme dans le combat.
        types_colores = OutilsAffichage.colorer("[Feu]", Couleurs.ORANGE) + " "
        types_colores = types_colores + OutilsAffichage.colorer("[Eau]", Couleurs.BLEU) + " "
        types_colores = types_colores + OutilsAffichage.colorer("[Plante]", Couleurs.VERT) + " "
        types_colores = types_colores + OutilsAffichage.colorer("[Électrik]", Couleurs.JAUNE) + " "
        types_colores = types_colores + OutilsAffichage.colorer("[Psy]", Couleurs.MAGENTA)
        lignes_du_cadre.append("Les types :  " + types_colores)

        # Un aperçu des barres de vie : pleine (vert), à moitié (jaune), presque vide (rouge).
        lignes_du_cadre.append("Les PV :     "
                               + OutilsAffichage.barre_de_vie(100, 100, 8) + " "
                               + OutilsAffichage.barre_de_vie(45, 100, 8) + " "
                               + OutilsAffichage.barre_de_vie(15, 100, 8))

        for ligne in OutilsAffichage.cadre(lignes_du_cadre, largeur, Couleurs.CYAN, "Bienvenue"):
            print(ligne)
        print()

        # 6. On appelle l'accueil (sans le modifier). ATTENTION aux parenthèses :
        #    self._accueil() lance la méthode, self._accueil la montre seulement.
        self._accueil()

    def _choix_mode(self) -> int:
        """Demande à l'utilisateur de choisir le mode de création des équipes."""
        choix = int(input("Choisissez le mode de création des équipes (1 : choisi, 2 : aléatoire, 3 : prédéfini) : "))
        if choix not in [1, 2, 3]:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")
            return self._choix_mode()
        if choix == 1:
            print("Vous avez choisi le mode 'choisi'.")
            input("Appuyez sur Entrée pour continuer...")

        elif choix == 2:
            print("Vous avez choisi le mode 'aléatoire'.")
            input("Appuyez sur Entrée pour continuer...")
        elif choix == 3:
            print("Vous avez choisi le mode 'prédéfini'.")
            input("Appuyez sur Entrée pour continuer...")
        return choix        

    def _accueil(self) -> None:
        """Affiche le titre et les règles."""
        
        print("Joueurs, veuillez choisir votre route :")
        input("Appuyez sur Entrée pour continuer...")
        print("Joueur 1, choisissez votre mode de création d'équipe :")
        choix1 = self._choix_mode()
        print("Joueur 2, choisissez votre mode de création d'équipe :")
        choix2 = self._choix_mode()
        self._creer_equipes(choix1)
        self._creer_equipes(choix2)
        Affichage.afficher_message(default_message)

        raise NotImplementedError

    def _creer_equipes(self, choix: int) -> list[Dresseur]:
        """Demande le mode de création (choisi/aléatoire/prédéfini) puis crée les 2 Dresseurs."""
        if choix == 1:
            # Mode choisi : demander à chaque joueur de choisir ses Pokémon
            dresseur1 = Saisie.saisir_dresseur(1)
            dresseur2 = Saisie.saisir_dresseur(2)
        elif choix == 2:
            # Mode aléatoire : créer des équipes aléatoires
            dresseur1 = Saisie.saisir_dresseur_aleatoire(1)
            dresseur2 = Saisie.saisir_dresseur_aleatoire(2)
        elif choix == 3:
            # Mode prédéfini : créer des équipes prédéfinies
            dresseur1 = Saisie.saisir_dresseur_predefini(1)
            dresseur2 = Saisie.saisir_dresseur_predefini(2)
        else:
            raise ValueError("Choix de mode invalide. Veuillez choisir 1, 2 ou 3.")
        raise NotImplementedError

    def _jouer_combat(self, dresseurs: list[Dresseur]) -> Dresseur:
        """Crée un Combat, le déroule, et renvoie le Dresseur vainqueur."""
        raise NotImplementedError

    def _fin(self, vainqueur: Dresseur) -> None:
        """Annonce la victoire et soigne tous les Pokémon des deux équipes."""
        raise NotImplementedError
