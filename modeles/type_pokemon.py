"""Un type de Pokémon (Feu, Eau...).

Choix : au lieu d'un grand tableau 14 x 14, chaque type connaît lui-même les
types qu'il bat, ceux qui lui résistent et ceux qui l'annulent. C'est plus
court, et le type répond tout seul à « suis-je efficace contre celui-là ? ».
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""


class TypePokemon:
    def __init__(self, nom, special, super_efficace, peu_efficace, sans_effet):
        """Les trois dernières listes contiennent des NOMS de types."""
        self.nom = nom
        # En génération 3, physique ou spécial dépend du type de l'attaque.
        self.special = special
        self.super_efficace = super_efficace
        self.peu_efficace = peu_efficace
        self.sans_effet = sans_effet

    def efficacite_contre(self, type_defenseur):
        """Renvoie 0, 0.5, 1 ou 2 face à UN type."""
        if type_defenseur.nom in self.sans_effet:
            return 0.0

        if type_defenseur.nom in self.super_efficace:
            return 2.0

        if type_defenseur.nom in self.peu_efficace:
            return 0.5

        return 1.0

    def efficacite_contre_pokemon(self, types_defenseur):
        """Multiplie l'efficacité sur chaque type du défenseur (Roche contre Feu/Vol = 4)."""
        total = 1.0

        for type_defenseur in types_defenseur:
            total = total * self.efficacite_contre(type_defenseur)

        return total
