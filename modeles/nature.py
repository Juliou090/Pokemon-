"""Classe Nature : une nature (Rigide, Timide...) qui augmente une stat de 10 %
et en diminue une autre de 10 %.

On a le droit ici : le nom, la stat augmentée, la stat diminuée et le
pourcentage appliqué à une stat.
On N'A PAS le droit : de calculer les stats complètes (c'est
Statistiques.calculer).
"""


class Nature:
    """Une nature.

    Attributs privés :
        _nom : nom de la nature
        _stat_augmentee : nom de la stat à +10 % (None si nature neutre)
        _stat_diminuee : nom de la stat à -10 % (None si nature neutre)

    Les noms de stats possibles : "attaque", "defense", "attaque_speciale",
    "defense_speciale", "vitesse" (jamais les PV, que les natures ne changent pas).
    """

    def __init__(self, nom, stat_augmentee, stat_diminuee):
        """Crée une nature."""
        self._nom = nom
        self._stat_augmentee = stat_augmentee
        self._stat_diminuee = stat_diminuee

    @property
    def nom(self):
        """Nom de la nature."""
        return self._nom

    def pourcentage(self, nom_stat):
        """Renvoie 110 si la stat est augmentée, 90 si elle est diminuée, 100 sinon."""
        if nom_stat == self._stat_augmentee:
            return 110

        if nom_stat == self._stat_diminuee:
            return 90

        return 100

    @staticmethod
    def neutre():
        """Renvoie une nature neutre (Sérieux) : aucune stat ne change."""
        return Nature("Sérieux", None, None)

    @staticmethod
    def toutes():
        """Renvoie les 25 natures (à écrire plus tard, pour le mode choisi)."""
        raise NotImplementedError

    def __str__(self):
        """Texte affiché quand on fait print(nature)."""
        return self._nom
