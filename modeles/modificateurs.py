"""Classe ModificateursStats : les paliers temporaires de stats (-6 à +6).

On a le droit ici : stocker les paliers, les borner entre -6 et +6 et donner
le multiplicateur correspondant.
On N'A PAS le droit : de savoir qui a lancé la modification ni de faire un print.
Les paliers sont remis à zéro quand le Pokémon quitte le terrain.

Pour l'instant seuls la création, la lecture et la remise à zéro sont écrites.
"""


class ModificateursStats:
    """Un palier par stat de combat (les PV n'ont pas de palier).

    Attributs privés : un entier par stat, entre -6 et +6.
        _palier_attaque, _palier_defense, _palier_attaque_speciale,
        _palier_defense_speciale, _palier_vitesse
    """

    # Attributs de classe : valeurs communes à tous les objets (pas des globales).
    PALIER_MIN = -6
    PALIER_MAX = 6

    def __init__(self):
        """Crée des modificateurs tous à 0 (aucune modification)."""
        self._palier_attaque = 0
        self._palier_defense = 0
        self._palier_attaque_speciale = 0
        self._palier_defense_speciale = 0
        self._palier_vitesse = 0

    def palier(self, nom_stat):
        """Renvoie le palier actuel d'une stat (ex. "vitesse")."""
        if nom_stat == "attaque":
            return self._palier_attaque

        if nom_stat == "defense":
            return self._palier_defense

        if nom_stat == "attaque_speciale":
            return self._palier_attaque_speciale

        if nom_stat == "defense_speciale":
            return self._palier_defense_speciale

        if nom_stat == "vitesse":
            return self._palier_vitesse

        raise ValueError("Stat sans palier : " + str(nom_stat))

    def modifier(self, nom_stat, variation):
        """Ajoute variation au palier (borné), renvoie la variation réelle."""
        raise NotImplementedError

    def multiplicateur(self, nom_stat):
        """Renvoie le coefficient officiel du palier (à écrire plus tard)."""
        raise NotImplementedError

    def reinitialiser(self):
        """Remet tous les paliers à 0."""
        self._palier_attaque = 0
        self._palier_defense = 0
        self._palier_attaque_speciale = 0
        self._palier_defense_speciale = 0
        self._palier_vitesse = 0
