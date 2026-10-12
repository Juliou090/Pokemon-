"""Tout ce que le jeu affiche à l'écran (le seul fichier, avec menus.py, qui
utilise print). Je m'appuie sur la boîte à outils de exemples_affichage.py
(couleurs, cadres, barres de PV) pour ne pas refaire deux fois le même travail.
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import os
import sys
import time

from donnees.catalogue import Catalogue
from ui.exemples_affichage import Couleurs, OutilsAffichage as Outils


class Affichage:
    COULEURS_DES_TYPES = {
        "Feu": Couleurs.ORANGE, "Eau": Couleurs.BLEU, "Plante": Couleurs.VERT,
        "Électrik": Couleurs.JAUNE, "Glace": Couleurs.CYAN, "Combat": Couleurs.ROUGE,
        "Poison": Couleurs.MAGENTA, "Sol": "\033[38;5;137m", "Vol": "\033[38;5;111m",
        "Psy": "\033[38;5;205m", "Roche": "\033[38;5;143m",
        "Ténèbres": "\033[38;5;103m", "Spectre": "\033[38;5;97m", "Normal": Couleurs.BLANC,
    }

    ABREVIATIONS = {"attaque": "Att", "defense": "Déf", "attaque_speciale": "AtS",
                    "defense_speciale": "DéS", "vitesse": "Vit"}

    def __init__(self, delai=0.6, largeur=72):
        """delai = pause (en secondes) après chaque message de combat."""
        self.delai = delai
        self.largeur = largeur

        # Réveille les couleurs de la console Windows et force l'UTF-8.
        os.system("")
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    # --- Petites pièces réutilisées partout ---------------------------------
    def col(self, texte, couleur):
        """Raccourci pour Outils.colorer."""
        return Outils.colorer(texte, couleur)

    def types(self, liste_de_types):
        """[Feu] [Vol], chaque type dans sa couleur."""
        texte = ""

        for type_pokemon in liste_de_types:
            couleur = Affichage.COULEURS_DES_TYPES[type_pokemon.nom]
            texte = texte + self.col("[" + type_pokemon.nom + "]", couleur) + " "

        return texte.strip()

    def statut(self, statut):
        if statut is None:
            return ""

        return self.col("[" + statut.abreviation + "]", Couleurs.JAUNE)

    def paliers(self, pokemon):
        """« Att +1  Vit -2 » : les stats modifiées pendant le combat."""
        texte = ""

        for nom_stat in pokemon.paliers:
            palier = pokemon.paliers[nom_stat]
            abreviation = Affichage.ABREVIATIONS[nom_stat]

            if palier > 0:
                texte = texte + self.col(abreviation + " +" + str(palier), Couleurs.VERT) + "  "
            elif palier < 0:
                texte = texte + self.col(abreviation + " " + str(palier), Couleurs.ROUGE) + "  "

        return texte.strip()

    def vie(self, pokemon, taille):
        """Barre de PV + « 120/153 », ou K.O."""
        if pokemon.est_ko():
            return self.col("K.O.", Couleurs.ROUGE + Couleurs.GRAS)

        chiffres = str(pokemon.get_pv()) + "/" + str(pokemon.pv_max)

        return Outils.barre_de_vie(pokemon.get_pv(), pokemon.pv_max, taille) + " " + chiffres

    def ligne_attaque(self, attaque):
        if attaque.est_de_statut():
            puissance = "statut"
        else:
            puissance = "Puiss. " + str(attaque.puissance)

        precision = str(attaque.precision)
        if attaque.precision == 0:
            precision = "—"

        return (Outils.completer(attaque.nom, 14)
                + Outils.completer(self.types([attaque.type]), 11)
                + Outils.completer(puissance, 13)
                + "Préc. " + Outils.completer(precision, 5)
                + "PP " + str(attaque.pp) + "/" + str(attaque.pp_max))

    def cadre(self, lignes, couleur, titre=""):
        for ligne in Outils.cadre(lignes, self.largeur, couleur, titre):
            print(ligne)

    # --- Messages -----------------------------------------------------------
    def effacer_ecran(self):
        Outils.effacer_ecran()

    def info(self, texte):
        print("  " + self.col(texte, Couleurs.GRIS))

    def erreur(self, texte):
        print("  " + self.col("✖ " + texte, Couleurs.ROUGE))

    def titre(self, texte):
        print()
        print(Outils.titre_centre(texte, self.largeur, Couleurs.CYAN))
        print()

    def separateur_tour(self, numero):
        print()
        print(Outils.titre_centre("TOUR " + str(numero), self.largeur, Couleurs.GRIS))

    def messages(self, textes):
        """Affiche les phrases du combat, en couleur, avec une courte pause."""
        for texte in textes:
            couleur = None

            if "K.O." in texte:
                couleur = Couleurs.ROUGE + Couleurs.GRAS
            elif "super efficace" in texte or "monte" in texte:
                couleur = Couleurs.VERT
            elif "pas très efficace" in texte or "Coup critique" in texte:
                couleur = Couleurs.JAUNE
            elif "baisse" in texte:
                couleur = Couleurs.ROUGE
            elif "rate" in texte or "échoue" in texte or "n'affecte pas" in texte:
                couleur = Couleurs.GRIS

            if couleur is not None:
                texte = self.col(texte, couleur)

            print("  " + texte)
            time.sleep(self.delai)

    # --- Écrans -------------------------------------------------------------
    def ecran_titre(self):
        """L'écran d'accueil : la Poké Ball, le titre et un cadre de bienvenue."""
        Outils.effacer_ecran()
        print()

        for ligne in Outils.pokeball(self.largeur):
            print(ligne)

        sous_titre = "Génération 3  ·  Rubis / Saphir"
        print()
        print(Outils.titre_centre("SIMULATEUR DE COMBAT POKÉMON", self.largeur, Couleurs.JAUNE))
        print(" " * ((self.largeur - len(sous_titre)) // 2) + self.col(sous_titre, Couleurs.GRIS))
        print()

        exemples_de_types = []
        for nom_type in ["Feu", "Eau", "Plante", "Électrik", "Psy"]:
            exemples_de_types.append(Catalogue.type(nom_type))

        barres = (Outils.barre_de_vie(100, 100, 8) + " " + Outils.barre_de_vie(45, 100, 8)
                  + " " + Outils.barre_de_vie(15, 100, 8))

        self.cadre([
            "Un combat Pokémon au tour par tour, à deux joueurs.",
            "",
            self.col("Au programme :", Couleurs.GRAS),
            "  • chacun choisit son mode de création d'équipe",
            "  • attaquer, changer de Pokémon ou utiliser un objet",
            "  • le dernier dresseur debout gagne !",
            "",
            "Les types :  " + self.types(exemples_de_types),
            "Les PV :     " + barres,
        ], Couleurs.CYAN, "Bienvenue")
        print()

    def etat_combat(self, dresseur1, dresseur2):
        """Les deux Pokémon actifs face à face."""
        print()
        self.panneau(dresseur1, Couleurs.CYAN)
        print(Outils.titre_centre("VS", self.largeur, Couleurs.GRIS))
        self.panneau(dresseur2, Couleurs.MAGENTA)

    def panneau(self, dresseur, couleur):
        pokemon = dresseur.pokemon_actif()

        # Un rond plein par Pokémon vivant, un rond vide par Pokémon K.O.
        boules = ""
        for membre in dresseur.equipe.pokemons:
            if membre.est_ko():
                boules = boules + self.col("○ ", Couleurs.ROUGE)
            else:
                boules = boules + self.col("● ", Couleurs.VERT)

        titre = self.col(dresseur.nom, couleur + Couleurs.GRAS) + "  " + boules.strip()
        nom = self.col(pokemon.nom, Couleurs.GRAS)
        lignes = [nom + "  Niv." + str(pokemon.niveau) + "  " + self.types(pokemon.types)
                  + " " + self.statut(pokemon.statut),
                  "PV " + self.vie(pokemon, 24)]

        if self.paliers(pokemon) != "":
            lignes.append(self.paliers(pokemon))

        if pokemon.objet_tenu is not None:
            lignes.append(self.col("Objet : " + pokemon.objet_tenu.nom, Couleurs.GRIS))

        self.cadre(lignes, couleur, titre)

    def equipe_detaillee(self, dresseur):
        """Toute l'équipe : PV, statut, attaques et PP."""
        lignes = []

        for pokemon in dresseur.equipe.pokemons:
            ligne = (self.col(pokemon.nom, Couleurs.GRAS) + "  Niv." + str(pokemon.niveau)
                     + "  " + self.types(pokemon.types) + " " + self.statut(pokemon.statut))

            if pokemon is dresseur.pokemon_actif():
                ligne = ligne + self.col("  (au combat)", Couleurs.JAUNE)

            lignes.append(ligne)
            lignes.append("   PV " + self.vie(pokemon, 20))

            for attaque in pokemon.attaques:
                lignes.append("   " + self.col(self.ligne_attaque(attaque), Couleurs.GRIS))

            lignes.append("")

        self.cadre(lignes, Couleurs.CYAN, "Équipe de " + dresseur.nom)

    def fiche_equipe(self, dresseur):
        """Récapitulatif d'une équipe juste après sa création."""
        lignes = []

        for pokemon in dresseur.equipe.pokemons:
            s = pokemon.stats
            lignes.append(self.col(pokemon.nom, Couleurs.GRAS) + "  Niv." + str(pokemon.niveau)
                          + "  " + self.types(pokemon.types) + "  Nature : " + pokemon.nature.nom)
            lignes.append("PV " + str(s.pv) + "  Att " + str(s.attaque) + "  Déf "
                          + str(s.defense) + "  AtS " + str(s.attaque_speciale) + "  DéS "
                          + str(s.defense_speciale) + "  Vit " + str(s.vitesse))

            if pokemon.objet_tenu is not None:
                lignes.append("Objet tenu : " + pokemon.objet_tenu.nom)

            lignes.append("")

        self.cadre(lignes, Couleurs.GRIS, "Équipe de " + dresseur.nom)

    def catalogue(self, pokemons, deja_pris):
        """Les Pokémon disponibles, avec leurs stats de base."""
        lignes = []
        numero = 0

        for pokemon in pokemons:
            b = pokemon.stats_base
            ligne = (self.col(str(numero + 1) + ".", Couleurs.JAUNE) + " "
                     + self.col(pokemon.nom, Couleurs.GRAS) + "  " + self.types(pokemon.types))

            if numero in deja_pris:
                ligne = ligne + self.col("  (déjà dans ton équipe)", Couleurs.GRIS)

            lignes.append(ligne)
            lignes.append(self.col("     PV " + str(b.pv) + "  Att " + str(b.attaque) + "  Déf "
                                   + str(b.defense) + "  AtS " + str(b.attaque_speciale)
                                   + "  DéS " + str(b.defense_speciale) + "  Vit "
                                   + str(b.vitesse), Couleurs.GRIS))
            numero = numero + 1

        self.cadre(lignes, Couleurs.CYAN, "Pokémon disponibles")

    # --- Listes numérotées pour les menus ----------------------------------
    def liste(self, options):
        numero = 1

        for option in options:
            print("  " + self.col(str(numero) + ".", Couleurs.JAUNE) + " " + option)
            numero = numero + 1

    def retour(self):
        print("  " + self.col("0.", Couleurs.JAUNE) + " " + self.col("Retour", Couleurs.GRIS))

    def liste_pokemon(self, equipe):
        options = []

        for pokemon in equipe.pokemons:
            texte = (Outils.completer(pokemon.nom, 11) + " Niv."
                     + Outils.completer(str(pokemon.niveau), 4) + self.vie(pokemon, 14))

            if pokemon is equipe.actif():
                texte = texte + self.col("  (au combat)", Couleurs.JAUNE)

            options.append(texte)

        self.liste(options)

    def liste_attaques(self, pokemon):
        options = []

        for attaque in pokemon.attaques:
            options.append(self.ligne_attaque(attaque))

        self.liste(options)

    def liste_objets(self, dresseur):
        options = []

        for ligne in dresseur.sac.lignes:
            texte = (Outils.completer(ligne.objet.nom, 13) + "x"
                     + Outils.completer(str(ligne.quantite), 3) + ligne.objet.description)

            if ligne.quantite == 0:
                texte = self.col(texte, Couleurs.GRIS)

            options.append(texte)

        self.liste(options)

    # --- Fin -----------------------------------------------------------------
    def victoire(self, vainqueur, perdant):
        if vainqueur is None:
            lignes = ["", self.col("ÉGALITÉ", Couleurs.JAUNE + Couleurs.GRAS),
                      "Les deux équipes sont K.O. en même temps !", ""]
        else:
            gagnant = self.col(vainqueur.nom, Couleurs.VERT + Couleurs.GRAS)
            lignes = ["", self.col("★  VICTOIRE  ★", Couleurs.JAUNE + Couleurs.GRAS), "",
                      gagnant + " remporte le combat contre " + perdant.nom + " !", ""]

        print()
        self.cadre(lignes, Couleurs.JAUNE)
