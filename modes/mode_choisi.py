"""Mode CHOISI : le joueur choisit ses Pokémon, niveaux, IV, natures, attaques et objets.

On a le droit ici : poser les questions via Saisie/Menus et construire les objets.
On N'A PAS le droit : de print ni de lire le clavier directement (passer par ui/).
"""

from modes.mode_selection import ModeSelection


class ModeChoisi(ModeSelection):
    """Création manuelle."""

    @property
    def nom(self) -> str: raise NotImplementedError
    def creer_dresseur(self, nom_joueur: str): raise NotImplementedError
