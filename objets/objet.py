"""Classe abstraite Objet : le « contrat » commun à tous les objets.

On a le droit ici : nom, description, et les deux méthodes que TOUT objet doit avoir.
On N'A PAS le droit : de coder un objet précis (une potion = sous-classe dans soins.py).
Polymorphisme : le combat appelle objet.utiliser(cible) sans savoir de quel objet il s'agit.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modeles.pokemon import Pokemon


class Objet(ABC):
    """Objet abstrait.

    Attributs prévus :
        # _nom : str
        # _description : str
    """

    def __init__(self, nom: str, description: str) -> None:
        pass

    @property
    def nom(self) -> str: raise NotImplementedError
    @property
    def description(self) -> str: raise NotImplementedError

    @abstractmethod
    def peut_etre_utilise_sur(self, cible: "Pokemon") -> bool:
        """True si l'objet aurait un effet sur cette cible (évite de gaspiller un objet)."""

    @abstractmethod
    def utiliser(self, cible: "Pokemon") -> str:
        """Applique l'effet sur la cible et renvoie un message décrivant le résultat."""
