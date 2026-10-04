"""Objets de rappel : ramènent un Pokémon K.O. au combat.

On a le droit ici : Rappel (50 % des PV) et RappelMax (100 %).
On N'A PAS le droit : de soigner un Pokémon qui n'est pas K.O.
"""

from objets.objet import Objet


class Rappel(Objet):
    """Ranime un K.O. avec 50 % de ses PV max.

    Attributs prévus :
        # _fraction : float
    """

    def __init__(self, nom: str = "Rappel", description: str = "", fraction: float = 0.5) -> None:
        pass

    def peut_etre_utilise_sur(self, cible) -> bool: raise NotImplementedError
    def utiliser(self, cible) -> str: raise NotImplementedError


class RappelMax(Rappel):
    """Ranime un K.O. avec 100 % de ses PV max."""
