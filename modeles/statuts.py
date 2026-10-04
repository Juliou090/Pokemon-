"""Statuts majeurs : une classe abstraite StatutMajeur et une classe par statut.

Un Pokémon possède au plus UN statut majeur à la fois (poison, paralysie,
brûlure, sommeil ou gel).

On a le droit ici : décrire ce qu'un statut change (empêcher d'agir, dégâts en
fin de tour, modifier une stat). Chaque statut redéfinit les mêmes méthodes
(polymorphisme).
On N'A PAS le droit : de faire un print, ni de connaître le Combat.
Pour ajouter un statut : créer une nouvelle sous-classe ici.
Ce fichier est dans modeles/ (et non combat/) car un Pokémon POSSÈDE un statut.

Pour l'instant seul le nom de chaque statut est écrit : les effets en combat
seront codés plus tard.
"""

from abc import ABC, abstractmethod


class StatutMajeur(ABC):
    """Statut abstrait : on ne crée jamais un StatutMajeur directement."""

    @property
    @abstractmethod
    def nom(self):
        """Nom affichable du statut (ex. "empoisonné")."""

    def peut_agir(self, pokemon):
        """Dit si le Pokémon peut agir ce tour-ci (à écrire plus tard)."""
        raise NotImplementedError

    def degats_fin_de_tour(self, pokemon):
        """PV perdus en fin de tour (à écrire plus tard)."""
        raise NotImplementedError

    def multiplicateur_stat(self, nom_stat):
        """Modifie une stat, ex. paralysie : vitesse / 4 (à écrire plus tard)."""
        raise NotImplementedError

    def fin_de_tour(self, pokemon):
        """Mise à jour en fin de tour, ex. décompte du sommeil (plus tard)."""
        raise NotImplementedError

    def __str__(self):
        """Texte affiché quand on fait print(statut)."""
        return self.nom


class Poison(StatutMajeur):
    """Perd 1/8 des PV max à chaque fin de tour."""

    @property
    def nom(self):
        """Nom du statut."""
        return "empoisonné"


class Paralysie(StatutMajeur):
    """Vitesse divisée par 4 et 25 % de chances de ne pas pouvoir agir."""

    @property
    def nom(self):
        """Nom du statut."""
        return "paralysé"


class Brulure(StatutMajeur):
    """Perd 1/8 des PV max par tour ; dégâts physiques infligés divisés par 2."""

    @property
    def nom(self):
        """Nom du statut."""
        return "brûlé"


class Sommeil(StatutMajeur):
    """Ne peut pas agir pendant quelques tours."""

    @property
    def nom(self):
        """Nom du statut."""
        return "endormi"


class Gel(StatutMajeur):
    """Ne peut pas agir ; 20 % de chances de dégeler à chaque tour."""

    @property
    def nom(self):
        """Nom du statut."""
        return "gelé"
