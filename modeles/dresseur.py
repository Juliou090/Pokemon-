"""Classe Dresseur : un joueur, avec son équipe et son sac.

On a le droit ici : nom, équipe, sac, raccourcis (pokemon_actif, a_perdu).
On N'A PAS le droit : de demander une action au clavier (ui/ + combat/), ni de print.
"""

from modeles.equipe import Equipe
from modeles.pokemon import Pokemon
from modeles.sac import Sac


class Dresseur:
    """Un dresseur.

    Attributs prévus :
        # _nom : str
        # _equipe : Equipe
        # _sac : Sac
        # _a_abandonne : bool
    """

    def __init__(self, nom: str, equipe: Equipe, sac: Sac) -> None:
        """Prépare le dresseur avec son nom, son équipe et son sac."""
        self._nom = nom
        self._equipe = equipe
        self._sac = sac
    @property
    def nom(self) -> str: 
        return self._nom

    @property
    def equipe(self) -> Equipe: 
        raise NotImplementedError
    @property
    def sac(self) -> Sac: raise NotImplementedError
    @property
    def pokemon_actif(self) -> Pokemon: raise NotImplementedError

    def a_perdu(self) -> bool:
        """True si abandon ou équipe entièrement K.O."""
        raise NotImplementedError

    def abandonner(self) -> None:
        """Déclare forfait."""
        raise NotImplementedError

    def utiliser_objet(self, nom_objet: str, cible: Pokemon) -> str:
        """Retire l'objet du sac, l'utilise sur la cible, renvoie le message.
        Lève ObjetIndisponibleError si le dresseur ne l'a pas."""
        raise NotImplementedError
