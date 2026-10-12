"""Nos exceptions. Elles héritent toutes de SimulateurError, ce qui permet de les
attraper toutes d'un coup si besoin.
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""


class SimulateurError(Exception):
    """Mère de toutes nos erreurs."""


class PokemonKOError(SimulateurError):
    """On essaie de faire agir ou attaquer un Pokémon K.O."""


class ObjetIndisponibleError(SimulateurError):
    """Un dresseur veut utiliser un objet qu'il n'a pas (ou plus)."""


class PVInvalideError(SimulateurError):
    """On essaie de donner des PV incohérents (négatifs ou au-dessus du maximum)."""


class ActionInvalideError(SimulateurError):
    """Action impossible : pas de PP, objet inutile, changement vers le même Pokémon..."""


class DonneesInvalidesError(SimulateurError):
    """Données impossibles : équipe de mauvaise taille, niveau hors limites..."""
