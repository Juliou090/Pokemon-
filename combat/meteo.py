"""Météo (NIVEAU 2) : soleil, pluie, tempête de sable, grêle.

On a le droit ici : une classe abstraite Meteo et une sous-classe par météo (boost/malus de types, dégâts de fin de tour).
On N'A PAS le droit : de print. À ne coder qu'après le niveau 1.
"""

from abc import ABC, abstractmethod


class Meteo(ABC):
    """Météo abstraite.

    Attributs prévus :
        # _tours_restants : int
    """

    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom affichable."""

    def multiplicateur_degats(self, attaque) -> float:
        """Ex. Pluie : Eau x1.5, Feu x0.5."""
        raise NotImplementedError

    def fin_de_tour(self, pokemon) -> int:
        """Dégâts éventuels infligés à un Pokémon."""
        raise NotImplementedError


class Soleil(Meteo):
    """Feu x1.5, Eau x0.5."""


class Pluie(Meteo):
    """Eau x1.5, Feu x0.5."""
