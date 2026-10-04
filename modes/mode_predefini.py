"""Mode PRÉDÉFINI : le joueur choisit une équipe toute faite parmi une liste.

On a le droit ici : lister les équipes de donnees/equipes.py et en créer une.
On N'A PAS le droit : d'écrire les équipes en dur ici (elles sont dans donnees/).
"""

from modes.mode_selection import ModeSelection


class ModePredefini(ModeSelection):
    """Équipe toute faite (sac de départ fixe)."""

    @property
    def nom(self) -> str: raise NotImplementedError
    def creer_dresseur(self, nom_joueur: str): raise NotImplementedError
