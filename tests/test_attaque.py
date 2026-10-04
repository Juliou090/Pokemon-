"""Tests de Attaque : PP et catégorie physique/spéciale selon le type."""

import unittest

from donnees.attaques import creer_lance_flammes
from donnees.attaques import creer_seisme
from exceptions import ActionInvalideError


class TestAttaque(unittest.TestCase):
    """Vérifie les PP et la catégorie."""

    def test_categorie_par_type(self):
        """Feu est spécial, Sol est physique (génération 3)."""
        self.assertTrue(creer_lance_flammes().est_speciale)
        self.assertFalse(creer_seisme().est_speciale)

    def test_utiliser_les_pp(self):
        """Chaque utilisation retire 1 PP, et restaurer_pp les remet au maximum."""
        seisme = creer_seisme()

        seisme.utiliser_pp()
        self.assertEqual(seisme.pp, 9)

        seisme.restaurer_pp()
        self.assertEqual(seisme.pp, 10)

    def test_plus_de_pp(self):
        """Sans PP, utiliser l'attaque lève ActionInvalideError."""
        seisme = creer_seisme()

        for essai in range(10):
            seisme.utiliser_pp()

        with self.assertRaises(ActionInvalideError):
            seisme.utiliser_pp()


if __name__ == "__main__":
    unittest.main()
