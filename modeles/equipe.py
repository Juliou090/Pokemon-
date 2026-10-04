"""Classe Equipe : les Pokémon d'un Dresseur et celui qui est au combat.

On a le droit ici : gérer la liste, le Pokémon actif et les changements.
On N'A PAS le droit : de choisir à la place du joueur ni d'afficher.

La taille d'une équipe est un attribut de CLASSE (Equipe.TAILLE) : pour passer
de 3 à 6 Pokémon, il suffit de changer ce seul nombre.
"""

from exceptions import EquipeInvalideError


class Equipe:
    """Équipe de Pokémon.

    Attribut de classe :
        TAILLE : nombre de Pokémon par équipe (3 pour l'instant)

    Attributs privés :
        _pokemons : liste d'objets Pokemon (len == TAILLE)
        _indice_actif : position dans la liste du Pokémon au combat
    """

    TAILLE = 3

    def __init__(self, pokemons):
        """Crée l'équipe. Lève EquipeInvalideError si la taille est mauvaise."""
        if len(pokemons) != Equipe.TAILLE:
            message = f"Une équipe doit avoir {Equipe.TAILLE} Pokémon."
            raise EquipeInvalideError(message)

        self._pokemons = pokemons

        # Le premier Pokémon de la liste commence le combat.
        self._indice_actif = 0

    @property
    def pokemons(self):
        """Liste des Pokémon de l'équipe."""
        return self._pokemons

    @property
    def actif(self):
        """Le Pokémon actuellement au combat."""
        return self._pokemons[self._indice_actif]

    @property
    def vivants(self):
        """Liste des Pokémon qui ne sont pas K.O."""
        liste_des_vivants = []

        for pokemon in self._pokemons:
            if not pokemon.est_ko:
                liste_des_vivants.append(pokemon)

        return liste_des_vivants

    def est_vaincue(self):
        """True si tous les Pokémon de l'équipe sont K.O."""
        nombre_de_vivants = len(self.vivants)

        return nombre_de_vivants == 0

    def changer_actif(self, indice):
        """Met le Pokémon n°indice au combat (à écrire plus tard)."""
        raise NotImplementedError

    def premier_vivant(self):
        """Envoie le premier Pokémon non K.O. (à écrire plus tard)."""
        raise NotImplementedError

    def soigner_tous(self):
        """Soigne complètement toute l'équipe (à écrire plus tard)."""
        raise NotImplementedError
