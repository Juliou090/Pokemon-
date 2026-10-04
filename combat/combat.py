"""Classe Combat : déroule le combat tour par tour entre deux Dresseurs.

On a le droit ici : la boucle de combat, la collecte des actions, leur exécution dans le bon ordre,
l'application des effets de fin de tour, le test de fin de combat.
On N'A PAS le droit : de print (on appelle l'objet Affichage reçu), de calculer les dégâts (calcul_degats.py),
ni de connaître le détail d'une attaque ou d'un objet précis.
"""

from combat.actions import Action
from modeles.dresseur import Dresseur


class Combat:
    """Un combat entre deux dresseurs.

    Attributs prévus :
        # _dresseur1, _dresseur2 : Dresseur
        # _affichage : Affichage   (reçu du Jeu)
        # _saisie : Saisie         (reçu du Jeu)
        # _numero_tour : int
        # _meteo : Meteo | None    (niveau 2)
    """

    def __init__(self, dresseur1: Dresseur, dresseur2: Dresseur, affichage, saisie) -> None:
        pass

    def lancer(self) -> Dresseur:
        """Boucle jusqu'à la fin ; renvoie le vainqueur."""
        raise NotImplementedError

    def _demander_action(self, dresseur: Dresseur) -> Action:
        """Utilise Menus/Saisie pour obtenir l'action choisie par ce dresseur."""
        raise NotImplementedError

    def _jouer_tour(self) -> None:
        """Collecte les 2 actions, les trie (ordre.py), les exécute, gère le fin de tour."""
        raise NotImplementedError

    def _fin_de_tour(self) -> None:
        """Dégâts de statut, objets tenus, météo..."""
        raise NotImplementedError

    def _remplacer_ko(self, dresseur: Dresseur) -> None:
        """Si le Pokémon actif est K.O., demande un remplaçant (ou fin de combat)."""
        raise NotImplementedError

    def est_termine(self) -> bool:
        raise NotImplementedError

    def vainqueur(self) -> Dresseur:
        raise NotImplementedError
