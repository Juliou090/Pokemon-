"""Sauvegarde/chargement d'un Dresseur et de ses Pokémon dans un fichier JSON (NIVEAU 3).

On a le droit ici : sérialiser des objets en JSON et reconstruire des objets au chargement.
On N'A PAS le droit : d'être appelé avant que le niveau 1 soit terminé. Erreur => SauvegardeError.
"""

from modeles.dresseur import Dresseur


class GestionnaireSauvegarde:
    """Sauvegarde et chargement.

    Attributs prévus :
        # _dossier : str
    """

    def __init__(self, dossier: str = "sauvegardes") -> None:
        pass

    def sauvegarder(self, dresseur: Dresseur, nom_fichier: str) -> None:
        raise NotImplementedError

    def charger(self, nom_fichier: str) -> Dresseur:
        raise NotImplementedError

    def lister(self) -> list[str]:
        raise NotImplementedError
