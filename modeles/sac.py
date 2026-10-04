"""Classe Sac : l'inventaire d'objets d'un Dresseur.

On a le droit ici : ajouter, retirer, compter des objets.
On N'A PAS le droit : d'appliquer les effets d'un objet (c'est objets/) ni d'afficher.
Un objet est une instance d'une sous-classe de Objet ; le sac utilise des LigneSac (objets), pas de dict.
"""

from objets.objet import Objet


class LigneSac:
    """Une ligne du sac : un objet et sa quantité.

    Attributs prévus :
        # objet : Objet
        # quantite : int
    """

    def __init__(self, objet: Objet, quantite: int) -> None:
        pass


class Sac:
    """Inventaire.

    Attributs prévus :
        # _lignes : list[LigneSac]
    """

    def __init__(self) -> None:
        pass

    def ajouter(self, objet: Objet, quantite: int = 1) -> None:
        raise NotImplementedError

    def retirer(self, nom_objet: str) -> Objet:
        """Retire 1 exemplaire et le renvoie ; lève ObjetIndisponibleError si absent ou épuisé."""
        raise NotImplementedError

    def quantite(self, nom_objet: str) -> int:
        raise NotImplementedError

    def lignes(self) -> list[LigneSac]:
        """Lignes non vides (pour que ui/ affiche le sac)."""
        raise NotImplementedError

    def est_vide(self) -> bool:
        raise NotImplementedError
