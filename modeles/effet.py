"""Effets d'une attaque : ce qu'une attaque fait EN PLUS ou À LA PLACE des dégâts.

Il y a une classe abstraite EffetAttaque et une sous-classe par sorte d'effet.

On a le droit ici : décrire un effet (quel statut, quelle stat, quelle chance)
et, plus tard, l'appliquer à des Pokémon en renvoyant un message (texte).
On N'A PAS le droit : de faire un print, ni de connaître le déroulement du
combat.
Niveau 2 : on ajoutera ici EffetDrain, EffetRecul, EffetDeuxTours sans toucher
au reste.

Pour l'instant seuls les constructeurs et les lectures sont écrits : la
méthode appliquer() sera codée avec la logique de combat.
"""

from abc import ABC, abstractmethod


class EffetAttaque(ABC):
    """Effet abstrait : toute sous-classe doit définir appliquer()."""

    @abstractmethod
    def appliquer(self, lanceur, cible):
        """Applique l'effet (lanceur et cible sont des Pokemon), renvoie un message."""


class EffetStatutMajeur(EffetAttaque):
    """Inflige un statut (poison, paralysie...) avec une certaine chance.

    Attributs privés :
        _statut : un objet StatutMajeur (ex. Brulure())
        _chance_pourcent : entier de 1 à 100 (100 = toujours)
    """

    def __init__(self, statut, chance_pourcent):
        """Crée l'effet à partir du statut et de sa chance en pourcentage."""
        self._statut = statut
        self._chance_pourcent = chance_pourcent

    @property
    def statut(self):
        """Le statut infligé."""
        return self._statut

    @property
    def chance_pourcent(self):
        """Chance de déclencher l'effet, en pourcentage."""
        return self._chance_pourcent

    def appliquer(self, lanceur, cible):
        """Applique le statut à la cible (à écrire plus tard)."""
        raise NotImplementedError


class EffetModifStat(EffetAttaque):
    """Monte ou baisse une stat temporaire (de -6 à +6) du lanceur ou de la cible.

    Attributs privés :
        _nom_stat : "attaque", "defense", "attaque_speciale",
                    "defense_speciale" ou "vitesse"
        _paliers : nombre de paliers (positif = monte, négatif = baisse)
        _sur_soi : True si l'effet vise le lanceur, False s'il vise la cible
        _chance_pourcent : entier de 1 à 100 (100 = toujours)
    """

    def __init__(self, nom_stat, paliers, sur_soi, chance_pourcent=100):
        """Crée l'effet de modification de stat."""
        self._nom_stat = nom_stat
        self._paliers = paliers
        self._sur_soi = sur_soi
        self._chance_pourcent = chance_pourcent

    @property
    def nom_stat(self):
        """Nom de la stat modifiée."""
        return self._nom_stat

    @property
    def paliers(self):
        """Nombre de paliers gagnés (positif) ou perdus (négatif)."""
        return self._paliers

    @property
    def sur_soi(self):
        """True si l'effet vise le lanceur."""
        return self._sur_soi

    @property
    def chance_pourcent(self):
        """Chance de déclencher l'effet, en pourcentage."""
        return self._chance_pourcent

    def appliquer(self, lanceur, cible):
        """Modifie la stat du lanceur ou de la cible (à écrire plus tard)."""
        raise NotImplementedError
