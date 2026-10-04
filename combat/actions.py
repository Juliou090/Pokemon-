"""Les actions possibles pendant un tour (classe abstraite Action + 4 sous-classes).

On a le droit ici : décrire UNE décision d'un dresseur et savoir l'exécuter (polymorphisme).
On N'A PAS le droit : de demander quoi que ce soit au joueur (saisie) ni de print.
Pour une nouvelle action (ex. objet spécial) : nouvelle sous-classe ici.
"""

from abc import ABC, abstractmethod

from modeles.attaque import Attaque
from modeles.dresseur import Dresseur


class Action(ABC):
    """Action abstraite.

    Attributs prévus :
        # _acteur : Dresseur
    """

    def __init__(self, acteur: Dresseur) -> None:
        pass

    @property
    def acteur(self) -> Dresseur: raise NotImplementedError

    @property
    def priorite(self) -> int:
        """Priorité de l'action (changement/objet : +6 ; attaque : celle de l'attaque)."""
        raise NotImplementedError

    @abstractmethod
    def executer(self, adversaire: Dresseur, combat) -> list[str]:
        """Exécute l'action et renvoie la liste des messages à afficher."""


class ActionAttaque(Action):
    """Utiliser une attaque.

    Attributs prévus :
        # _attaque : Attaque
    """

    def __init__(self, acteur: Dresseur, attaque: Attaque) -> None:
        pass

    def executer(self, adversaire: Dresseur, combat) -> list[str]:
        raise NotImplementedError


class ActionChangement(Action):
    """Changer de Pokémon.

    Attributs prévus :
        # _indice : int
    """

    def __init__(self, acteur: Dresseur, indice: int) -> None:
        pass

    def executer(self, adversaire: Dresseur, combat) -> list[str]:
        raise NotImplementedError


class ActionObjet(Action):
    """Utiliser un objet du sac sur un Pokémon de son équipe.

    Attributs prévus :
        # _nom_objet : str
        # _indice_cible : int
    """

    def __init__(self, acteur: Dresseur, nom_objet: str, indice_cible: int) -> None:
        pass

    def executer(self, adversaire: Dresseur, combat) -> list[str]:
        raise NotImplementedError


class ActionAbandon(Action):
    """Déclarer forfait : le combat se termine, l'adversaire gagne."""

    def executer(self, adversaire: Dresseur, combat) -> list[str]:
        raise NotImplementedError
