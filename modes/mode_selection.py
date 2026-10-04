"""Classe abstraite ModeSelection : le contrat commun des 3 modes de création d'équipe.

On a le droit ici : déclarer la méthode que chaque mode doit définir.
On N'A PAS le droit : de coder un mode précis (un fichier par mode).
Pour un nouveau mode : une nouvelle sous-classe dans un nouveau fichier, puis l'ajouter au menu de Jeu.
"""

from abc import ABC, abstractmethod

from modeles.dresseur import Dresseur


class ModeSelection(ABC):
    """Mode de création d'équipe (polymorphisme : Jeu appelle creer_dresseur() sans savoir lequel).

    Attributs prévus :
        # (plus de chargeur : on appelle directement donnees.pokemons)
        # _saisie : Saisie
        # _affichage : Affichage
    """

    def __init__(self, saisie, affichage) -> None:
        pass

    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom du mode affiché dans le menu."""

    @abstractmethod
    def creer_dresseur(self, nom_joueur: str) -> Dresseur:
        """Construit un Dresseur complet : équipe de 3 + sac de départ."""
