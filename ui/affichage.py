"""Classe Affichage : tous les messages affichés dans la console.

On a le droit ici : print, mise en forme, couleurs, tout texte du jeu.
On N'A PAS le droit : de calculer des dégâts ou de décider quoi que ce soit.
Un nouveau message = une nouvelle méthode ici.
"""

from modeles.pokemon import Pokemon


class Affichage:
    """Sorties console."""

    def titre(self) -> None: raise NotImplementedError
    def message(self, texte: str) -> None:
        """Affiche une ligne simple."""
        raise NotImplementedError
    def messages(self, textes: list[str]) -> None: raise NotImplementedError
    def separateur_tour(self, numero: int) -> None: raise NotImplementedError

    def etat_pokemon(self, pokemon: Pokemon) -> None:
        """Nom, niveau, barre de PV, statut."""
        raise NotImplementedError

    def etat_combat(self, pokemon1: Pokemon, pokemon2: Pokemon) -> None:
        raise NotImplementedError

    def victoire(self, nom_vainqueur: str) -> None: raise NotImplementedError
    def erreur(self, texte: str) -> None: raise NotImplementedError
