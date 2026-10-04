"""Équipes prédéfinies du mode PRÉDÉFINI.

On a le droit ici : décrire des équipes toutes faites (noms de Pokémon, niveaux, attaques)
sous forme d'objets de description (EquipePredefinie), puis les construire via les fonctions creer_xxx() de donnees/pokemons.py.
On N'A PAS le droit : de variable globale ; de mettre des Pokémon sous forme de dict/tuple.
"""

from modeles.equipe import Equipe


class EquipePredefinie:
    """Description d'une équipe toute faite.

    Attributs prévus :
        # nom : str   (ex. "Équipe Feu")
        # description : str
    """

    def __init__(self, nom: str, description: str) -> None:
        pass


class BibliothequeEquipes:
    """Liste des équipes prédéfinies et leur construction."""

    def __init__(self) -> None:
        pass

    def liste(self) -> list[EquipePredefinie]:
        raise NotImplementedError

    def construire(self, equipe_predefinie: EquipePredefinie) -> Equipe:
        raise NotImplementedError
