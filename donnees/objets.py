"""Catalogue des objets disponibles dans le jeu (FabriqueObjets).

On a le droit ici : créer des objets à partir de leur nom, lister ceux qui existent.
On N'A PAS le droit : de coder l'effet d'un objet (c'est objets/).
Pour une nouvelle potion : sous-classe dans objets/soins.py PUIS l'inscrire ici.
"""

from objets.objet import Objet


class FabriqueObjets:
    """Fabrique d'objets."""

    def creer(self, nom: str) -> Objet:
        """Instancie l'objet ; DonneesInvalidesError si inconnu."""
        raise NotImplementedError

    def noms_disponibles(self) -> list[str]:
        raise NotImplementedError

    def sac_predefini(self, numero: int):
        """Sac de départ du mode prédéfini."""
        raise NotImplementedError

    def sac_aleatoire(self):
        """Sac de départ tiré au hasard (mode aléatoire)."""
        raise NotImplementedError
