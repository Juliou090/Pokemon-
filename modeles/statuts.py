"""Les 5 statuts majeurs (règles de la génération 3, Bulbapedia).

Choix : une classe « de base » StatutMajeur qui ne fait rien, et une classe par
statut qui redéfinit seulement ce qui change. Le combat appelle toujours les
mêmes méthodes (peut_agir, degats_fin_de_tour...) sans savoir de quel statut
il s'agit : c'est le polymorphisme.
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import random


class StatutMajeur:
    nom = ""
    identifiant = ""
    abreviation = ""

    def __init__(self):
        # peut_agir() y laisse une phrase à afficher (ex. « X est paralysé ! »).
        self.message = ""

    def immunise(self, pokemon):
        """True si ce Pokémon ne peut pas avoir ce statut."""
        return False

    def peut_agir(self, pokemon):
        self.message = ""
        return True

    def degats_fin_de_tour(self, pokemon):
        return 0

    def phrase_degats(self, pokemon):
        return ""

    def pourcentage_stat(self, nom_stat):
        """100 = la stat ne change pas."""
        return 100

    def un_huitieme(self, pokemon):
        """1/8 des PV max, au moins 1 (poison et brûlure)."""
        degats = pokemon.pv_max // 8

        if degats < 1:
            degats = 1

        return degats


class Poison(StatutMajeur):
    nom = "empoisonné"
    identifiant = "poison"
    abreviation = "PSN"

    def immunise(self, pokemon):
        return pokemon.a_le_type("Poison")

    def degats_fin_de_tour(self, pokemon):
        return self.un_huitieme(pokemon)

    def phrase_degats(self, pokemon):
        return pokemon.nom + " souffre du poison !"


class Brulure(StatutMajeur):
    nom = "brûlé"
    identifiant = "brulure"
    abreviation = "BRU"

    def immunise(self, pokemon):
        return pokemon.a_le_type("Feu")

    def degats_fin_de_tour(self, pokemon):
        return self.un_huitieme(pokemon)

    def phrase_degats(self, pokemon):
        return pokemon.nom + " souffre de sa brûlure !"


class Paralysie(StatutMajeur):
    nom = "paralysé"
    identifiant = "paralysie"
    abreviation = "PAR"

    def peut_agir(self, pokemon):
        """Une chance sur quatre d'être bloqué."""
        self.message = ""

        if random.randint(1, 4) == 1:
            self.message = pokemon.nom + " est paralysé ! Il ne peut pas attaquer !"
            return False

        return True

    def pourcentage_stat(self, nom_stat):
        """Vitesse divisée par 4."""
        if nom_stat == "vitesse":
            return 25

        return 100


class Sommeil(StatutMajeur):
    nom = "endormi"
    identifiant = "sommeil"
    abreviation = "SOM"

    def __init__(self):
        super().__init__()
        # En génération 3, le Pokémon est bloqué de 1 à 4 tours.
        self.tours_restants = random.randint(1, 4)

    def peut_agir(self, pokemon):
        self.message = ""

        if self.tours_restants > 0:
            self.tours_restants = self.tours_restants - 1
            self.message = pokemon.nom + " dort profondément."
            return False

        # Plus de tours à dormir : il se réveille et peut agir tout de suite.
        pokemon.statut = None
        self.message = pokemon.nom + " se réveille !"
        return True


class Gel(StatutMajeur):
    nom = "gelé"
    identifiant = "gel"
    abreviation = "GEL"

    def immunise(self, pokemon):
        return pokemon.a_le_type("Glace")

    def peut_agir(self, pokemon):
        """20 % de chances de dégeler à chaque tour."""
        self.message = ""

        if random.randint(1, 100) <= 20:
            pokemon.statut = None
            self.message = pokemon.nom + " dégèle !"
            return True

        self.message = pokemon.nom + " est gelé : il ne peut pas bouger !"
        return False


def creer_statut(identifiant):
    """Fabrique un statut NEUF à partir de son identifiant (chaque Pokémon touché
    doit avoir le sien, à cause du compteur du sommeil)."""
    if identifiant == "poison":
        return Poison()

    if identifiant == "brulure":
        return Brulure()

    if identifiant == "paralysie":
        return Paralysie()

    if identifiant == "sommeil":
        return Sommeil()

    return Gel()
