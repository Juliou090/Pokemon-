"""Classe Jeu : chef d'orchestre de toute la partie.

On a le droit ici : enchaîner les grandes phases (accueil, création des équipes,
combat, fin) en appelant les autres modules.
On N'A PAS le droit : de calculer des dégâts, d'afficher avec print (voir ui/),
ou de connaître les détails d'une attaque ou d'un objet.
"""

from modeles.dresseur import Dresseur
from ui.affichage import Affichage
from ui.saisie import Saisie


class Jeu:
    """Enchaîne : accueil -> création des équipes -> combat -> fin (-> rejouer).

    Attributs prévus :
        # _affichage : Affichage   (seul objet qui affiche)
        # _saisie : Saisie         (seul objet qui lit le clavier)
        # _dresseurs : list[Dresseur]  (les 2 joueurs, vide au départ)
    """

    def __init__(self) -> None:
        """Prépare l'affichage et la saisie ; ne lance rien."""
        pass

    def lancer(self) -> None:
        """Boucle principale : accueil, création, combat, proposition de rejouer."""
    
        raise NotImplementedError

    def _accueil(self) -> None:
        """Affiche le titre et les règles."""
        default_message = "Bienvenue dans le jeu Pokémon !"
        Affichage.afficher_message(default_message)

        raise NotImplementedError

    def _creer_equipes(self) -> list[Dresseur]:
        """Demande le mode de création (choisi/aléatoire/prédéfini) puis crée les 2 Dresseurs."""
        raise NotImplementedError

    def _jouer_combat(self, dresseurs: list[Dresseur]) -> Dresseur:
        """Crée un Combat, le déroule, et renvoie le Dresseur vainqueur."""
        raise NotImplementedError

    def _fin(self, vainqueur: Dresseur) -> None:
        """Annonce la victoire et soigne tous les Pokémon des deux équipes."""
        raise NotImplementedError
