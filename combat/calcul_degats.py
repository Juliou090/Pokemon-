"""Calcul des dégâts, formule de la génération 3 (Bulbapedia, page « Damage ») :

    dégâts = ((((2 x Niveau / 5 + 2) x Puissance x A / D) / 50) x Brûlure + 2)
             x Critique x Aléatoire(85 à 100 %) x STAB x Type1 x Type2

A et D = Attaque et Défense (ou Att. Spé. et Déf. Spé. si l'attaque est
spéciale). Toutes les divisions gardent la partie entière (//).
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import random


class ResultatDegats:
    def __init__(self, degats, efficacite, critique):
        self.degats = degats
        self.efficacite = efficacite
        self.critique = critique


class CalculDegats:
    @staticmethod
    def touche(attaque):
        """Test de précision (précision 0 = ne rate jamais)."""
        if attaque.precision == 0:
            return True

        return random.randint(1, 100) <= attaque.precision

    @staticmethod
    def formule_de_base(niveau, puissance, valeur_attaque, valeur_defense, brule_et_physique):
        """La partie « ((2N/5+2) x P x A/D / 50) x Brûlure + 2 » (séparée pour les tests)."""
        degats = (2 * niveau // 5 + 2) * puissance * valeur_attaque // valeur_defense // 50

        if brule_et_physique:
            degats = degats // 2

        return degats + 2

    @staticmethod
    def calculer(attaquant, defenseur, attaque):
        """Renvoie un ResultatDegats (dégâts, efficacité totale, coup critique ?)."""
        if attaque.critique_eleve:
            critique = random.randint(1, 8) == 1
        else:
            critique = random.randint(1, 16) == 1

        if attaque.est_speciale():
            stat_attaque = "attaque_speciale"
            stat_defense = "defense_speciale"
        else:
            stat_attaque = "attaque"
            stat_defense = "defense"

        valeur_attaque = attaquant.stat_effective(stat_attaque, ignorer_baisses=critique)
        valeur_defense = defenseur.stat_effective(stat_defense, ignorer_hausses=critique)

        brule_et_physique = False
        if attaquant.statut is not None and attaquant.statut.identifiant == "brulure":
            brule_et_physique = not attaque.est_speciale()

        degats = CalculDegats.formule_de_base(attaquant.niveau, attaque.puissance,
                                              valeur_attaque, valeur_defense, brule_et_physique)

        if critique:
            degats = degats * 2

        degats = degats * random.randint(85, 100) // 100

        efficacite = 1.0

        # Lutte ignore les types : ni STAB, ni efficacité.
        if not attaque.lutte:
            if attaquant.a_le_type(attaque.type.nom):
                degats = degats * 15 // 10

            efficacite = attaque.type.efficacite_contre_pokemon(defenseur.types)

            # Un type après l'autre, comme dans le jeu (pour les arrondis).
            for type_defenseur in defenseur.types:
                multiplicateur = attaque.type.efficacite_contre(type_defenseur)

                if multiplicateur == 2.0:
                    degats = degats * 2
                elif multiplicateur == 0.5:
                    degats = degats // 2
                elif multiplicateur == 0.0:
                    degats = 0

        # Une attaque qui touche fait au moins 1 dégât, sauf immunité.
        if efficacite > 0 and degats < 1:
            degats = 1

        return ResultatDegats(degats, efficacite, critique)
