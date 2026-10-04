"""Classe Saisie : lecture du clavier avec vérification.

On a le droit ici : input() et la validation (redemander tant que la réponse est invalide).
On N'A PAS le droit : de print des messages de jeu (utiliser Affichage).
"""


class Saisie:
    """Entrées clavier."""

    def lire_entier(self, question: str, minimum: int, maximum: int) -> int:
        """Redemande jusqu'à avoir un entier entre minimum et maximum inclus."""
        raise NotImplementedError

    def lire_texte(self, question: str) -> str:
        raise NotImplementedError

    def lire_oui_non(self, question: str) -> bool:
        raise NotImplementedError
