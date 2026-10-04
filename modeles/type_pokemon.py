"""Classe TypePokemon : un type (Feu, Eau, Plante...).

Un type connaît lui-même ses forces et ses faiblesses : c'est lui qui sait
répondre à la question « mon attaque est-elle efficace contre ce type ? ».

On a le droit ici : le nom du type, sa catégorie (physique ou spéciale en
génération 3) et les noms des types contre lesquels il est fort ou faible.
On N'A PAS le droit : de créer les 14 types (voir donnees/efficacite.py),
ni de calculer des dégâts.
"""


class TypePokemon:
    """Un type élémentaire.

    Attributs privés :
        _nom : nom du type (ex. "Feu")
        _est_special : True si les attaques de ce type sont spéciales
                       (règle de la génération 3)
        _super_efficace_contre : liste des NOMS de types qui subissent x2
        _peu_efficace_contre : liste des NOMS de types qui subissent x0,5
        _sans_effet_contre : liste des NOMS de types qui subissent x0
    """

    def __init__(self, nom, est_special, super_efficace_contre,
                 peu_efficace_contre, sans_effet_contre):
        """Crée un type à partir de son nom et de ses trois listes de noms."""
        self._nom = nom
        self._est_special = est_special
        self._super_efficace_contre = super_efficace_contre
        self._peu_efficace_contre = peu_efficace_contre
        self._sans_effet_contre = sans_effet_contre

    @property
    def nom(self):
        """Nom affichable du type."""
        return self._nom

    @property
    def est_special(self):
        """True si les attaques de ce type sont spéciales (génération 3)."""
        return self._est_special

    def efficacite_contre(self, type_defenseur):
        """Renvoie le multiplicateur de ce type contre UN type défenseur.

        Le résultat vaut 0.0, 0.5, 1.0 ou 2.0.
        """
        nom_defenseur = type_defenseur.nom

        # On teste l'immunité en premier : un x0 l'emporte sur tout le reste.
        if nom_defenseur in self._sans_effet_contre:
            return 0.0

        if nom_defenseur in self._super_efficace_contre:
            return 2.0

        if nom_defenseur in self._peu_efficace_contre:
            return 0.5

        # Tout ce qui n'est dans aucune liste est neutre.
        return 1.0

    def efficacite_contre_pokemon(self, types_du_defenseur):
        """Renvoie le multiplicateur contre un Pokémon à un ou deux types.

        On multiplie les efficacités obtenues contre chaque type du Pokémon.
        Exemple : Roche contre Feu/Vol donne 2.0 x 2.0 = 4.0.
        """
        multiplicateur_total = 1.0

        for type_defenseur in types_du_defenseur:
            multiplicateur_du_type = self.efficacite_contre(type_defenseur)
            multiplicateur_total = multiplicateur_total * multiplicateur_du_type

        return multiplicateur_total

    def __eq__(self, autre):
        """Deux types sont égaux s'ils ont le même nom."""
        if not isinstance(autre, TypePokemon):
            return False

        return self._nom == autre.nom

    def __hash__(self):
        """Nécessaire car on redéfinit __eq__ (un type peut alors servir de clé)."""
        return hash(self._nom)

    def __str__(self):
        """Texte affiché quand on fait print(type)."""
        return self._nom
