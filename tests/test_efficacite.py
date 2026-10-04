"""Tests de l'efficacité des types (donnees/efficacite.py)."""

import unittest

from donnees.efficacite import creer_tous_les_types
from donnees.efficacite import creer_type_combat
from donnees.efficacite import creer_type_eau
from donnees.efficacite import creer_type_electrik
from donnees.efficacite import creer_type_feu
from donnees.efficacite import creer_type_normal
from donnees.efficacite import creer_type_plante
from donnees.efficacite import creer_type_psy
from donnees.efficacite import creer_type_roche
from donnees.efficacite import creer_type_sol
from donnees.efficacite import creer_type_spectre
from donnees.efficacite import creer_type_tenebres
from donnees.efficacite import creer_type_vol


class TestEfficacite(unittest.TestCase):
    """Vérifie les multiplicateurs de types."""

    def test_il_y_a_quatorze_types(self):
        """Le jeu contient 14 types différents."""
        les_types = creer_tous_les_types()

        self.assertEqual(len(les_types), 14)

    def test_efficacite_simple(self):
        """Les quatre valeurs possibles : x2, x0,5, x0 et x1."""
        eau_contre_feu = creer_type_eau().efficacite_contre(creer_type_feu())
        feu_contre_eau = creer_type_feu().efficacite_contre(creer_type_eau())
        normal_contre_spectre = creer_type_normal().efficacite_contre(
            creer_type_spectre())
        feu_contre_sol = creer_type_feu().efficacite_contre(creer_type_sol())

        self.assertEqual(eau_contre_feu, 2.0)
        self.assertEqual(feu_contre_eau, 0.5)
        self.assertEqual(normal_contre_spectre, 0.0)
        self.assertEqual(feu_contre_sol, 1.0)

    def test_roche_contre_feu_vol(self):
        """Roche contre Feu/Vol : x2 puis x2, donc x4."""
        types_defenseur = [creer_type_feu(), creer_type_vol()]

        resultat = creer_type_roche().efficacite_contre_pokemon(types_defenseur)

        self.assertEqual(resultat, 4.0)

    def test_sol_contre_vol(self):
        """Sol contre Vol : aucun effet."""
        resultat = creer_type_sol().efficacite_contre_pokemon([creer_type_vol()])

        self.assertEqual(resultat, 0.0)

    def test_electrik_contre_eau_sol(self):
        """Électrik contre Eau/Sol : x2 puis x0, donc x0."""
        types_defenseur = [creer_type_eau(), creer_type_sol()]

        resultat = creer_type_electrik().efficacite_contre_pokemon(types_defenseur)

        self.assertEqual(resultat, 0.0)

    def test_plante_contre_eau_sol(self):
        """Plante contre Eau/Sol : x2 puis x2, donc x4."""
        types_defenseur = [creer_type_eau(), creer_type_sol()]

        resultat = creer_type_plante().efficacite_contre_pokemon(types_defenseur)

        self.assertEqual(resultat, 4.0)

    def test_psy_contre_roche_tenebres(self):
        """Psy contre Roche/Ténèbres : x1 puis x0, donc x0."""
        types_defenseur = [creer_type_roche(), creer_type_tenebres()]

        resultat = creer_type_psy().efficacite_contre_pokemon(types_defenseur)

        self.assertEqual(resultat, 0.0)

    def test_combat_contre_spectre(self):
        """Combat n'a aucun effet sur Spectre."""
        resultat = creer_type_combat().efficacite_contre(creer_type_spectre())

        self.assertEqual(resultat, 0.0)

    def test_categorie_physique_ou_speciale(self):
        """Génération 3 : la catégorie dépend du type de l'attaque."""
        self.assertTrue(creer_type_feu().est_special)
        self.assertTrue(creer_type_tenebres().est_special)
        self.assertFalse(creer_type_sol().est_special)
        self.assertFalse(creer_type_spectre().est_special)


if __name__ == "__main__":
    unittest.main()
