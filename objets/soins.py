"""Objets de soin des PV : Potion, SuperPotion, HyperPotion, PotionMax.

On a le droit ici : des objets qui rendent des PV à un Pokémon VIVANT.
On N'A PAS le droit : de ranimer un K.O. (voir rappel.py) ni de soigner un statut (guerison.py).
Pour ajouter une potion : créer une sous-classe de Soin avec ses PV, puis l'ajouter dans donnees/objets.py.
"""

from objets.objet import Objet


class Soin(Objet):
    """Soin générique : rend `_pv_rendus` PV (ou tous si None).

    Attributs prévus :
        # _pv_rendus : int | None
    """

    def __init__(self, nom: str, description: str, pv_rendus: int | None) -> None:
        pass

    def peut_etre_utilise_sur(self, cible) -> bool: raise NotImplementedError
    def utiliser(self, cible) -> str: raise NotImplementedError


class Potion(Soin):
    """Rend 20 PV."""


class SuperPotion(Soin):
    """Rend 50 PV."""


class HyperPotion(Soin):
    """Rend 200 PV."""


class PotionMax(Soin):
    """Rend tous les PV."""
