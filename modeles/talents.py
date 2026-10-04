"""Talents (NIVEAU 2) : capacités passives d'un Pokémon (Intimidation, Engrais...).

On a le droit ici : une classe abstraite Talent + une sous-classe par talent, qui réagissent
à des « moments » du combat (entrée au combat, dégâts reçus...).
On N'A PAS le droit : de print. À ne PAS coder avant que le niveau 1 soit terminé.
"""

from abc import ABC, abstractmethod


class Talent(ABC):
    """Talent abstrait."""

    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom affichable du talent."""

    def a_l_entree(self, proprietaire, adversaire) -> str:
        """Réaction quand le Pokémon entre au combat ; renvoie un message ou ""."""
        raise NotImplementedError

    def modifier_degats_recus(self, degats: int, attaque) -> int:
        """Réaction quand le propriétaire reçoit une attaque."""
        raise NotImplementedError
