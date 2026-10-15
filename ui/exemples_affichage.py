"""Ma boîte à outils d'affichage : couleurs, cadres, barres de PV, Poké Ball.

J'ai mis ici tout ce qui sert à faire un bel affichage dans la console. La classe
Affichage (affichage.py) en hérite : elle peut donc appeler directement
self.colorer(...), self.cadre(...), self.barre_de_vie(...), etc.
Pour voir tous les exemples à l'écran : python -m ui.exemples_affichage

Comment ça marche :
- un print écrit UNE ligne : pour un affichage sur plusieurs lignes, je fais
  plusieurs print (souvent dans une boucle for) ;
- une couleur est un code spécial, invisible, écrit avant le texte : le terminal
  le comprend comme « colore ce qui suit » ;
- les cadres, les barres et la Poké Ball sont fabriqués avec des caractères
  ordinaires (─ │ █ ░...) répétés avec l'opérateur * (ex. "─" * 10).
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
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

    Un objet OutilsAffichage retient la largeur de l'écran (self.largeur) :
    les cadres, les titres et la Poké Ball s'y adaptent tout seuls.
    """

    def __init__(self, largeur=72):
        self.largeur = largeur

    # ------------------------------------------------------------------
    # 1. Les couleurs
    # ------------------------------------------------------------------
    def colorer(self, texte, couleur):
        """Renvoie le texte coloré (le code de couleur avant, le RESET après).

        Sans le RESET, tout ce qui s'affiche ensuite resterait coloré.
        Exemple : print(self.colorer("Attention", Couleurs.ROUGE))
        """
        return couleur + texte + Couleurs.RESET

    # ------------------------------------------------------------------
    # 2. Aligner du texte coloré
    # ------------------------------------------------------------------
    def longueur_visible(self, texte):
        """Longueur du texte SANS compter les codes de couleur (invisibles).

        len() les compte, ce qui décalerait les cadres. Un code de couleur
        commence par \\033 et se termine par « m ».
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

    def completer(self, texte, largeur):
        """Ajoute des espaces à droite pour que le texte occupe `largeur` caractères."""
        manque = largeur - self.longueur_visible(texte)

        if manque <= 0:
            return texte

        return texte + " " * manque

    # ------------------------------------------------------------------
    # 3. Les cadres et les titres
    # ------------------------------------------------------------------
    def cadre(self, lignes, couleur=Couleurs.GRIS, titre=""):
        """Renvoie une LISTE de lignes qui forment un cadre autour des `lignes` données.

        Pour l'afficher :
            for ligne in self.cadre(["Dracaufeu", "PV 120/153"]):
                print(ligne)
        """
        resultat = []
        largeur_interieure = self.largeur - 4

        # Ligne du haut : coin, trait répété, (titre), coin.
        if titre == "":
            haut = "╭" + "─" * (self.largeur - 2) + "╮"
            resultat.append(self.colorer(haut, couleur))
        else:
            reste = self.largeur - self.longueur_visible(titre) - 5
            debut = self.colorer("╭─ ", couleur)
            fin = self.colorer(" " + "─" * reste + "╮", couleur)
            resultat.append(debut + titre + fin)

        # Une ligne par texte : barre | espace | texte complété | espace | barre.
        barre = self.colorer("│", couleur)
        for ligne in lignes:
            contenu = self.completer(ligne, largeur_interieure)
            resultat.append(barre + " " + contenu + " " + barre)

        bas = "╰" + "─" * (self.largeur - 2) + "╯"
        resultat.append(self.colorer(bas, couleur))

        return resultat

    def titre_centre(self, texte, couleur=Couleurs.CYAN):
        """Renvoie un titre centré entre des traits (ex. ══════  TOUR 1  ══════)."""
        ligne = "══════  " + texte + "  ══════"
        marge = " " * ((self.largeur - len(ligne)) // 2)

        return marge + self.colorer(ligne, couleur)

    # ------------------------------------------------------------------
    # 4. La barre de PV
    # ------------------------------------------------------------------
    def barre_de_vie(self, pv, pv_max, taille=20):
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

        partie_pleine = self.colorer("█" * cases_pleines, couleur)
        partie_vide = self.colorer("░" * (taille - cases_pleines), Couleurs.GRIS)

        return partie_pleine + partie_vide

    # ------------------------------------------------------------------
    # 5. La Poké Ball
    # ------------------------------------------------------------------
    def pokeball(self):
        """Renvoie une LISTE de lignes qui dessinent une Poké Ball.

        Principe : un cercle se dessine ligne par ligne. On mesure sa largeur
        au MILIEU de chaque ligne ; elle vient du théorème de Pythagore :
        racine(rayon² - y²).
        """
        resultat = []
        rayon = 6        # taille de la balle : plus grand = plus de lignes
        facteur = 2.4    # largeur : plus grand = plus large, plus petit = plus étroit

        for ligne in range(-rayon, rayon):
            y = ligne + 0.5
            demi_largeur = int(facteur * math.sqrt(rayon * rayon - y * y) + 0.5)
            marge = " " * ((self.largeur - 2 * demi_largeur) // 2)

            if ligne < -1:
                texte = self.colorer("█" * (2 * demi_largeur), Couleurs.ROUGE)
            elif ligne > 0:
                texte = self.colorer("█" * (2 * demi_largeur), Couleurs.BLANC)
            else:
                # Les 2 lignes du milieu : bande grise, bouton blanc au centre.
                cote = demi_largeur - 3
                bande_gauche = self.colorer("█" * cote, Couleurs.GRIS)
                bouton = self.colorer("█" * 6, Couleurs.BLANC)
                bande_droite = self.colorer("█" * cote, Couleurs.GRIS)
                texte = bande_gauche + bouton + bande_droite

            resultat.append(marge + texte)

        return resultat

    # ------------------------------------------------------------------
    # 6. Divers
    # ------------------------------------------------------------------
    def effacer_ecran(self):
        """Efface l'écran du terminal (pour cacher ce qui précède)."""
        print("\033[2J\033[3J\033[H", end="")

    def demonstration(self):
        """Affiche un exemple de chaque outil. Lancer : python -m ui.exemples_affichage"""
        print()
        print("1. Couleurs :")
        print("   " + self.colorer("texte rouge", Couleurs.ROUGE))
        print("   " + self.colorer("texte vert", Couleurs.VERT))
        print("   " + self.colorer("texte jaune", Couleurs.JAUNE))
        print("   " + self.colorer("texte bleu", Couleurs.BLEU))

        print()
        print("2. Un titre centré :")
        print(self.titre_centre("TOUR 1"))

        print()
        print("3. Un cadre avec une barre de PV :")
        lignes = [
            self.colorer("Dracaufeu", Couleurs.GRAS) + "  Niv.50  "
            + self.colorer("[Feu]", Couleurs.ORANGE) + " " + self.colorer("[Vol]", Couleurs.BLEU),
            "PV " + self.barre_de_vie(120, 153, 24) + " 120/153",
        ]
        for ligne in self.cadre(lignes, Couleurs.CYAN, "Sacha  ● ● ●"):
            print(ligne)

        print()
        print("4. Les barres de PV selon la vie restante :")
        for pv in [100, 60, 30, 10, 1, 0]:
            print("   " + self.barre_de_vie(pv, 100, 20) + " " + str(pv) + "/100")

        print()
        print("5. La Poké Ball :")
        for ligne in self.pokeball():
            print(ligne)


if __name__ == "__main__":
    OutilsAffichage().demonstration()
