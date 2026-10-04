"""Toutes les exceptions personnalisées du projet.

On a le droit ici : uniquement des classes d'exception (une ligne de docstring suffit).
On N'A PAS le droit : de mettre de la logique, ni d'importer un autre module du projet.
Toutes héritent de SimulateurError pour pouvoir toutes les attraper d'un coup.
"""


class SimulateurError(Exception):
    """Exception mère de toutes les erreurs du projet."""


class PokemonKOError(SimulateurError):
    """Levée si on essaie de faire agir ou attaquer un Pokémon déjà K.O. (imposée par le prof)."""


class ObjetIndisponibleError(SimulateurError):
    """Levée si un Dresseur utilise un objet qu'il n'a pas ou plus (imposée par le prof)."""


class PVInvalideError(SimulateurError):
    """Levée si on affecte des PV incohérents (négatifs, supérieurs au max...) (imposée par le prof)."""


class ActionInvalideError(SimulateurError):
    """Levée si une action est impossible (changer pour le Pokémon déjà actif, attaque sans PP...)."""


class EquipeInvalideError(SimulateurError):
    """Levée si une équipe n'a pas 3 Pokémon, ou en contient un invalide."""


class DonneesInvalidesError(SimulateurError):
    """Levée si un fichier JSON est introuvable, mal formé ou contient une valeur impossible."""


class SauvegardeError(SimulateurError):
    """Levée si une sauvegarde/un chargement échoue (niveau 3)."""
