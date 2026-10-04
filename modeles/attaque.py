"""Classe Attaque : une capacité utilisable par un Pokémon (Lance-Flammes...).

On a le droit ici : nom, type, puissance, précision, PP, priorité, effets.
On N'A PAS le droit : de calculer les dégâts (c'est combat/calcul_degats.py)
ni d'afficher quoi que ce soit.
Une attaque est TOUJOURS un objet Attaque, jamais un dictionnaire, un tuple
ou une liste.
"""

from exceptions import ActionInvalideError


class Attaque:
    """Une attaque.

    Attributs privés :
        _nom : nom de l'attaque
        _type : un objet TypePokemon
        _puissance : entier (0 pour une attaque de statut)
        _precision : entier de 1 à 100 (0 = ne rate jamais)
        _pp_max : nombre de PP au maximum
        _pp : nombre de PP restants
        _priorite : 0 normalement, +1 pour Vive-Attaque
        _effets : liste d'objets EffetAttaque (liste vide si aucun effet)
        _critique_eleve : True si le taux de coup critique est augmenté
    """

    def __init__(self, nom, type_attaque, puissance, precision, pp_max,
                 priorite=0, effets=None, critique_eleve=False):
        """Crée une attaque avec tous ses PP."""
        self._nom = nom
        self._type = type_attaque
        self._puissance = puissance
        self._precision = precision
        self._pp_max = pp_max
        self._pp = pp_max
        self._priorite = priorite
        self._critique_eleve = critique_eleve

        # On évite « effets=[] » dans la signature : cette liste serait alors
        # partagée entre toutes les attaques. On crée une liste neuve ici.
        if effets is None:
            self._effets = []
        else:
            self._effets = effets

    @property
    def nom(self):
        """Nom de l'attaque."""
        return self._nom

    @property
    def type(self):
        """Type de l'attaque (objet TypePokemon)."""
        return self._type

    @property
    def puissance(self):
        """Puissance (0 pour une attaque de statut)."""
        return self._puissance

    @property
    def precision(self):
        """Précision (0 = ne rate jamais)."""
        return self._precision

    @property
    def pp(self):
        """PP restants."""
        return self._pp

    @property
    def pp_max(self):
        """PP maximum."""
        return self._pp_max

    @property
    def priorite(self):
        """Priorité de l'attaque."""
        return self._priorite

    @property
    def effets(self):
        """Liste des effets de l'attaque (peut être vide)."""
        return self._effets

    @property
    def critique_eleve(self):
        """True si le taux de coup critique est augmenté."""
        return self._critique_eleve

    @property
    def est_speciale(self):
        """True si l'attaque est spéciale.

        En génération 3, cela dépend du TYPE de l'attaque, pas de l'attaque.
        """
        return self._type.est_special

    @property
    def est_de_statut(self):
        """True si l'attaque n'inflige pas de dégâts (puissance égale à 0)."""
        return self._puissance == 0

    def utiliser_pp(self):
        """Retire 1 PP. Lève ActionInvalideError s'il n'en reste plus."""
        if self._pp <= 0:
            raise ActionInvalideError(self._nom + " n'a plus de PP.")

        self._pp = self._pp - 1

    def restaurer_pp(self):
        """Remet les PP au maximum (fin de combat)."""
        self._pp = self._pp_max

    def __str__(self):
        """Texte affiché quand on fait print(attaque)."""
        return self._nom
