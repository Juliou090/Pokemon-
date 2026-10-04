"""Sprites en caractères colorés (NIVEAU 3) : blocs █ ▀ ▄ et couleurs ANSI.

On a le droit ici : transformer une image décrite en texte en lignes colorées.
On N'A PAS le droit : d'être indispensable : le jeu doit marcher sans.
"""


class Sprite:
    """Dessin d'un Pokémon en blocs.

    Attributs prévus :
        # _lignes : list[str]
    """

    def __init__(self, lignes: list[str]) -> None:
        pass

    def afficher(self) -> None:
        raise NotImplementedError
