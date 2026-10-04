"""Objets tenus : donnés à un Pokémon avant le combat, ils boostent ses capacités.

On a le droit ici : des objets qui agissent via des « crochets » appelés par le combat
(modifier une stat, soigner en fin de tour...). Ils ne sont pas dans le sac pendant le combat.
On N'A PAS le droit : de modifier directement le combat. Pour un nouvel objet tenu : sous-classe de Tenu.
"""

from objets.objet import Objet


class Tenu(Objet):
    """Objet tenu abstrait (reste utilisable via utiliser() pour être donné au Pokémon)."""

    def multiplicateur_stat(self, nom_stat: str) -> float:
        """Coefficient appliqué à une stat (1.0 par défaut)."""
        raise NotImplementedError

    def multiplicateur_degats(self, attaque) -> float:
        """Coefficient appliqué aux dégâts de l'attaque (1.0 par défaut)."""
        raise NotImplementedError

    def fin_de_tour(self, porteur) -> str:
        """Effet en fin de tour (ex. Restes) ; renvoie un message ou ""."""
        raise NotImplementedError


class Restes(Tenu):
    """Rend 1/16 des PV max en fin de tour."""


class BandeauChoix(Tenu):
    """Attaque physique x1.5."""


class LunettesChoix(Tenu):
    """Attaque spéciale x1.5."""


class BaieSitrus(Tenu):
    """Rend 30 PV quand les PV passent sous la moitié (consommée)."""
