"""Exemples d'affichage : une boîte à outils pour faire un bel affichage console.

Ce fichier sert de DOCUMENTATION VIVANTE : chaque outil est expliqué, et on
peut le copier ou l'appeler tel quel dans le vrai affichage du jeu.

    from ui.exemples_affichage import OutilsAffichage, Couleurs

Pour voir tous les exemples à l'écran, lance simplement le fichier :

    python -m ui.exemples_affichage

On a le droit ici : print (c'est le dossier ui/), couleurs, cadres, barres.
On N'A PAS le droit : de calculer des dégâts ou de connaître les règles du jeu.

Comment ça marche, en résumé :
- Un « print » écrit UNE ligne. Pour un affichage sur plusieurs lignes, on
  fait plusieurs print (souvent dans une boucle for).
- Les couleurs sont des codes spéciaux (invisibles) écrits avant le texte : le
  terminal les comprend comme « colore ce qui suit ».
- Les cadres, les barres et la Poké Ball sont fabriqués avec des caractères
  ordinaires (─ │ █ ░...) répétés avec l'opérateur * (ex. "─" * 10).
"""

import math


class Couleurs:
    """Les codes de couleur (des attributs de CLASSE : pas de variable globale).

    Utilisation : Couleurs.ROUGE
    """

    RESET = "\033[0m"        # remet la couleur normale
    GRAS = "\033[1m"
    GRIS = "\033[90m"
    ROUGE = "\033[91m"
    VERT = "\033[92m"
    JAUNE = "\033[93m"
    BLEU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BLANC = "\033[97m"
    ORANGE = "\033[38;5;208m"


class OutilsAffichage:
    """Des outils pour construire de beaux affichages.

    Toutes les méthodes sont des @staticmethod : elles n'ont besoin d'aucun
    objet (pas de self). On les appelle directement avec le nom de la classe :
        OutilsAffichage.colorer("Bonjour", Couleurs.VERT)
    """

    # ------------------------------------------------------------------
    # 1. Les couleurs
    # ------------------------------------------------------------------
    @staticmethod
    def colorer(texte, couleur):
        """Renvoie le texte coloré (le code de couleur avant, le RESET après).

        Sans le RESET, tout ce qui s'affiche ensuite resterait coloré.

        Exemple :
            print(OutilsAffichage.colorer("Attention", Couleurs.ROUGE))
        """
        return couleur + texte + Couleurs.RESET

    # ------------------------------------------------------------------
    # 2. Aligner du texte coloré
    # ------------------------------------------------------------------
    @staticmethod
    def longueur_visible(texte):
        """Renvoie la longueur du texte SANS compter les codes de couleur.

        Pourquoi : les codes de couleur sont invisibles à l'écran, mais len() les
        compte. Pour aligner des cadres, il faut la longueur que l'on VOIT.

        Un code de couleur commence par le caractère \\033 et se termine par « m ».
        """
        longueur = 0
        dans_un_code = False

        for caractere in texte:
            if dans_un_code:
                if caractere == "m":
                    dans_un_code = False
            elif caractere == "\033":
                dans_un_code = True
            else:
                longueur = longueur + 1

        return longueur

    @staticmethod
    def completer(texte, largeur):
        """Ajoute des espaces à droite pour que le texte occupe `largeur` caractères."""
        manque = largeur - OutilsAffichage.longueur_visible(texte)

        if manque <= 0:
            return texte

        return texte + " " * manque

    # ------------------------------------------------------------------
    # 3. Les cadres
    # ------------------------------------------------------------------
    @staticmethod
    def cadre(lignes, largeur=50, couleur=Couleurs.GRIS, titre=""):
        """Renvoie une LISTE de lignes qui forment un cadre autour des `lignes` données.

        Pour l'afficher :
            for ligne in OutilsAffichage.cadre(["Dracaufeu", "PV 120/153"]):
                print(ligne)

        Les coins arrondis et les traits sont des caractères comme les autres.
        """
        resultat = []
        largeur_interieure = largeur - 4

        # Ligne du haut : coin, trait répété, (titre), coin.
        if titre == "":
            haut = "╭" + "─" * (largeur - 2) + "╮"
            resultat.append(OutilsAffichage.colorer(haut, couleur))
        else:
            reste = largeur - OutilsAffichage.longueur_visible(titre) - 5
            debut = OutilsAffichage.colorer("╭─ ", couleur)
            fin = OutilsAffichage.colorer(" " + "─" * reste + "╮", couleur)
            resultat.append(debut + titre + fin)

        # Une ligne par texte : barre | espace | texte complété | espace | barre.
        barre = OutilsAffichage.colorer("│", couleur)
        for ligne in lignes:
            contenu = OutilsAffichage.completer(ligne, largeur_interieure)
            resultat.append(barre + " " + contenu + " " + barre)

        # Ligne du bas.
        bas = "╰" + "─" * (largeur - 2) + "╯"
        resultat.append(OutilsAffichage.colorer(bas, couleur))

        return resultat

    @staticmethod
    def titre_centre(texte, largeur=50, couleur=Couleurs.CYAN):
        """Renvoie un titre centré entre des traits (ex. ══════  TOUR 1  ══════)."""
        ligne = "══════  " + texte + "  ══════"
        marge = " " * ((largeur - len(ligne)) // 2)

        return marge + OutilsAffichage.colorer(ligne, couleur)

    # ------------------------------------------------------------------
    # 4. La barre de PV
    # ------------------------------------------------------------------
    @staticmethod
    def barre_de_vie(pv, pv_max, taille=20):
        """Renvoie une barre de PV : des cases pleines (couleur) et des cases vides (gris).

        Exemple : pv=60, pv_max=100, taille=10  ->  ██████░░░░ (6 cases pleines).

        Couleur : verte au-dessus de 50 %, jaune au-dessus de 20 %, rouge sinon.
        """
        # Le // garde la partie entière : 60 * 10 // 100 = 6 cases.
        cases_pleines = pv * taille // pv_max

        # Un Pokémon vivant garde au moins une case pleine, pour qu'on le voie.
        if pv > 0 and cases_pleines == 0:
            cases_pleines = 1

        pourcentage = pv * 100 // pv_max

        if pourcentage > 50:
            couleur = Couleurs.VERT
        elif pourcentage > 20:
            couleur = Couleurs.JAUNE
        else:
            couleur = Couleurs.ROUGE

        partie_pleine = OutilsAffichage.colorer("█" * cases_pleines, couleur)
        partie_vide = OutilsAffichage.colorer("░" * (taille - cases_pleines),
                                              Couleurs.GRIS)

        return partie_pleine + partie_vide

    # ------------------------------------------------------------------
    # 5. La Poké Ball
    # ------------------------------------------------------------------
    @staticmethod
    def pokeball(largeur=50):
        """Renvoie une LISTE de lignes qui dessinent une Poké Ball.

        Principe : un cercle se dessine ligne par ligne. On mesure sa largeur
        au MILIEU de chaque ligne, ce qui évite les lignes vides en haut et en
        bas. La largeur vient du théorème de Pythagore : racine(rayon² - y²).
        """
        resultat = []
        rayon = 6        # taille de la balle : plus grand = plus de lignes
        facteur = 2.4    # largeur : plus grand = plus large, plus petit = plus étroit

        for ligne in range(-rayon, rayon):
            y = ligne + 0.5
            demi_largeur = int(facteur * math.sqrt(rayon * rayon - y * y) + 0.5)
            marge = " " * ((largeur - 2 * demi_largeur) // 2)

            if ligne < -1:
                texte = OutilsAffichage.colorer("█" * (2 * demi_largeur),
                                                Couleurs.ROUGE)
            elif ligne > 0:
                texte = OutilsAffichage.colorer("█" * (2 * demi_largeur),
                                                Couleurs.BLANC)
            else:
                # Les 2 lignes du milieu : bande grise, bouton blanc au centre.
                cote = demi_largeur - 3
                bande_gauche = OutilsAffichage.colorer("█" * cote, Couleurs.GRIS)
                bouton = OutilsAffichage.colorer("█" * 6, Couleurs.BLANC)
                bande_droite = OutilsAffichage.colorer("█" * cote, Couleurs.GRIS)
                texte = bande_gauche + bouton + bande_droite

            resultat.append(marge + texte)

        return resultat
    @staticmethod
    def _ligne_de_la_bande(ligne, demi_largeur):
        """Les 3 lignes du milieu : bande grise, avec le bouton blanc au centre."""
        largeur_bouton = 4

        if ligne != 0:
            largeur_bouton = 2

        cote = demi_largeur - largeur_bouton
        bande_gauche = OutilsAffichage.colorer("█" * cote, Couleurs.GRIS)
        bouton = OutilsAffichage.colorer("█" * (2 * largeur_bouton), Couleurs.BLANC)
        bande_droite = OutilsAffichage.colorer("█" * cote, Couleurs.GRIS)

        return bande_gauche + bouton + bande_droite

    # ------------------------------------------------------------------
    # 6. Divers
    # ------------------------------------------------------------------
    @staticmethod
    def effacer_ecran():
        """Efface l'écran du terminal (pour cacher ce qui précède)."""
        print("\033[2J\033[3J\033[H", end="")


def demonstration():
    """Affiche un exemple de chaque outil. Lancer : python -m ui.exemples_affichage"""
    print()
    print("1. Couleurs :")
    print("   " + OutilsAffichage.colorer("texte rouge", Couleurs.ROUGE))
    print("   " + OutilsAffichage.colorer("texte vert", Couleurs.VERT))
    print("   " + OutilsAffichage.colorer("texte jaune", Couleurs.JAUNE))
    print("   " + OutilsAffichage.colorer("texte bleu", Couleurs.BLEU))
    print("   " + OutilsAffichage.colorer("texte orange", Couleurs.ORANGE))
    print("   " + OutilsAffichage.colorer("texte gris", Couleurs.GRIS))

    print()
    print("2. Un titre centré :")
    print(OutilsAffichage.titre_centre("TOUR 1"))

    print()
    print("3. Un cadre avec une barre de PV et un statut :")
    lignes = [
        OutilsAffichage.colorer("Dracaufeu", Couleurs.GRAS) + "  Niv.50  "
        + OutilsAffichage.colorer("[Feu]", Couleurs.ORANGE) + " "
        + OutilsAffichage.colorer("[Vol]", Couleurs.BLEU) + "  "
        + OutilsAffichage.colorer("[PAR]", Couleurs.JAUNE),
        "PV " + OutilsAffichage.barre_de_vie(120, 153, 24) + " 120/153",
    ]
    for ligne in OutilsAffichage.cadre(lignes, 50, Couleurs.CYAN, "Sacha  ● ● ●"):
        print(ligne)

    print()
    print("4. Les barres de PV selon la vie restante :")
    for pv in [100, 60, 30, 10, 1, 0]:
        print("   " + OutilsAffichage.barre_de_vie(pv, 100, 20) + " " + str(pv) + "/100")

    print()
    print("5. La Poké Ball :")
    for ligne in OutilsAffichage.pokeball(50):
        print(ligne)
    print()


if __name__ == "__main__":
    demonstration()
