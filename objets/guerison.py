"""Objets de guérison de statut : Antidote, Anti-Para, Total Soin...

On a le droit ici : des objets qui retirent un statut majeur précis (ou tous).
On N'A PAS le droit : de rendre des PV.
"""

from objets.objet import Objet


class Guerison(Objet):
    """Guérit un type de statut.

    Attributs prévus :
        # _statut_gueri : type[StatutMajeur] | None   (None = guérit tout)
    """

    def __init__(self, nom: str, description: str, statut_gueri=None) -> None:
        pass

    def peut_etre_utilise_sur(self, cible) -> bool: raise NotImplementedError
    def utiliser(self, cible) -> str: raise NotImplementedError


class Antidote(Guerison):
    """Guérit le poison."""


class AntiPara(Guerison):
    """Guérit la paralysie."""


class TotalSoin(Guerison):
    """Guérit n'importe quel statut."""
