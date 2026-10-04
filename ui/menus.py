"""Classe Menus : construit et affiche des menus numérotés, renvoie le choix.

On a le droit ici : afficher des listes d'options (attaques, Pokémon, sac, modes...) et récupérer le choix via Saisie.
On N'A PAS le droit : de décider de la suite du jeu.
"""

from modeles.dresseur import Dresseur


class Menus:
    """Menus interactifs.

    Attributs prévus :
        # _saisie : Saisie
        # _affichage : Affichage
    """

    def __init__(self, saisie, affichage) -> None:
        pass

    def menu_principal(self, dresseur: Dresseur) -> str:
        """Attaquer / Changer / Objet / Abandonner : renvoie le choix."""
        raise NotImplementedError

    def choisir_attaque(self, dresseur: Dresseur) -> int:
        raise NotImplementedError

    def choisir_pokemon(self, dresseur: Dresseur) -> int:
        raise NotImplementedError

    def choisir_objet(self, dresseur: Dresseur) -> str:
        raise NotImplementedError

    def choisir_mode(self, modes: list) -> int:
        raise NotImplementedError
