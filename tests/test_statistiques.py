"""Tests de Statistiques et Nature (formules de stats de la génération 3)."""

import unittest

from modeles.nature import Nature
from modeles.statistiques import Statistiques


class TestStatistiques(unittest.TestCase):
    """Vérifie le calcul des stats sur l'exemple de Dracaufeu."""

    def setUp(self):
        """Prépare les stats de base de Dracaufeu et des IV tous à 31."""
        self.base_dracaufeu = Statistiques(78, 84, 78, 109, 85, 100)
        self.iv_maximaux = Statistiques.identiques(31)
        self.ev_nuls = Statistiques.zeros()

    def test_dracaufeu_niveau_50(self):
        """Niveau 50, IV 31, EV 0 : 153 PV et 120 de Vitesse."""
        stats = Statistiques.calculer(
            self.base_dracaufeu, self.iv_maximaux, self.ev_nuls, 50,
            Nature.neutre())

        self.assertEqual(stats.pv, 153)
        self.assertEqual(stats.vitesse, 120)

    def test_nature_qui_modifie_deux_stats(self):
        """Rigide : Attaque +10 %, Attaque Spéciale -10 %."""
        nature_rigide = Nature("Rigide", "attaque", "attaque_speciale")

        stats = Statistiques.calculer(
            self.base_dracaufeu, self.iv_maximaux, self.ev_nuls, 50,
            nature_rigide)

        # Sans nature : Attaque 104 et Attaque Spéciale 129.
        self.assertEqual(stats.attaque, 114)
        self.assertEqual(stats.attaque_speciale, 116)

    def test_les_pv_ne_dependent_pas_de_la_nature(self):
        """Une nature ne change jamais les PV."""
        nature_rigide = Nature("Rigide", "attaque", "attaque_speciale")

        stats = Statistiques.calculer(
            self.base_dracaufeu, self.iv_maximaux, self.ev_nuls, 50,
            nature_rigide)

        self.assertEqual(stats.pv, 153)

    def test_iv_aleatoires_entre_0_et_31(self):
        """Les IV tirés au hasard restent entre 0 et 31."""
        for essai in range(50):
            iv = Statistiques.aleatoires()

            self.assertGreaterEqual(iv.pv, 0)
            self.assertLessEqual(iv.pv, 31)
            self.assertGreaterEqual(iv.vitesse, 0)
            self.assertLessEqual(iv.vitesse, 31)


if __name__ == "__main__":
    unittest.main()
