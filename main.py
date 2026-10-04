"""Point d'entrée du programme.

On a le droit d'ici : créer un objet Jeu et appeler sa méthode lancer().
On N'A PAS le droit : d'écrire de la logique (pas de if/boucle/calcul métier).
"""

from jeu import Jeu


if __name__ == "__main__":
    Jeu().lancer()
