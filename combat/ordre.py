"""Détermine QUI agit en premier à chaque tour.

On a le droit ici : trier des actions selon la priorité puis la vitesse (égalité = tirage au sort).
On N'A PAS le droit : d'exécuter les actions.
"""

from combat.actions import Action


class OrdreDesActions:
    """Classeur d'actions."""

    def trier(self, actions: list[Action]) -> list[Action]:
        """Renvoie les actions dans l'ordre d'exécution (priorité décroissante, puis vitesse effective)."""
        raise NotImplementedError
