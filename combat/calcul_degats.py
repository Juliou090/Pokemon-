"""Calcul des dégâts d'une attaque (formule de la génération 3).

On a le droit ici : la formule officielle (Bulbapedia > Damage > Generation III), le STAB,
l'efficacité, le critique, la variation aléatoire 0,85-1, la brûlure.
On N'A PAS le droit : de modifier les PV (on RENVOIE un nombre, le Combat l'applique) ni de print.
"""

from modeles.attaque import Attaque
from modeles.pokemon import Pokemon


class ResultatDegats:
    """Compte rendu d'un calcul de dégâts (un objet, pas un tuple).

    Attributs prévus :
        # degats : int
        # efficacite : float     (0, 0.25, 0.5, 1, 2, 4)
        # critique : bool
    """

    def __init__(self, degats: int, efficacite: float, critique: bool) -> None:
        pass


class CalculateurDegats:
    """Calcule les dégâts.

    L'efficacité des types est demandée au type de l'attaque :
    attaque.type.efficacite_contre_pokemon(defenseur.types).
    """

    def __init__(self) -> None:
        pass

    def calculer(self, attaquant: Pokemon, defenseur: Pokemon, attaque: Attaque) -> ResultatDegats:
        """Applique la formule complète et renvoie un ResultatDegats."""
        raise NotImplementedError

    def _est_critique(self) -> bool:
        raise NotImplementedError

    def _stab(self, attaquant: Pokemon, attaque: Attaque) -> float:
        """1.5 si le type de l'attaque est un des types de l'attaquant, sinon 1."""
        raise NotImplementedError

    def _efficacite(self, attaque: Attaque, defenseur: Pokemon) -> float:
        """Produit des multiplicateurs sur chacun des types du défenseur."""
        raise NotImplementedError

    def _touche(self, attaque: Attaque) -> bool:
        """Test de précision (niveau 2 : esquive)."""
        raise NotImplementedError
