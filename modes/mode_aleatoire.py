"""Mode ALÉATOIRE : Pokémon, niveau, IV, nature, attaques et objets tirés au hasard.

On a le droit ici : random et les fonctions creer_xxx() de donnees/.
On N'A PAS le droit : de demander quoi que ce soit au joueur, hormis son nom.
"""

from modes.mode_selection import ModeSelection


class ModeAleatoire(ModeSelection):
    """Création au hasard (sac de départ aléatoire)."""

    @property
    def nom(self) -> str: raise NotImplementedError
    def creer_dresseur(self, nom_joueur: str): raise NotImplementedError
