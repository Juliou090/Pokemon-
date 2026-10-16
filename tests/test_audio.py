"""Tests du son : le bon bruitage pour chaque phrase, et les fichiers sont valides.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import os
import unittest
import wave

from ui.audio import Audio


class TestAudio(unittest.TestCase):
    def setUp(self):
        # actif=False : pas de son pendant les tests.
        self.audio = Audio(actif=False)

    def test_choix_du_bruitage(self):
        self.assertEqual(self.audio.nom_du_bruitage("C'est super efficace !"), "super_efficace")
        self.assertEqual(self.audio.nom_du_bruitage("Raichu perd 33 PV (10/84)."), "degats")
        self.assertEqual(self.audio.nom_du_bruitage("Raichu est K.O. !"), "ko")
        self.assertEqual(self.audio.nom_du_bruitage("[Ash] Dracaufeu utilise Surf !"), "attaque")
        self.assertEqual(self.audio.nom_du_bruitage("Bonjour"), "")

    def test_mode_muet_ne_plante_pas(self):
        self.audio.musique("menu")
        self.audio.bruitage("degats")
        self.audio.bruitage_pour("Raichu est K.O. !")
        self.audio.discrete()
        self.audio.normale()
        self.audio.fermer()
        self.assertEqual(self.audio.musique_en_cours, "")

    def test_les_fichiers_sonores_existent_et_sont_valides(self):
        noms = ["attaque", "degats", "super_efficace", "peu_efficace", "critique", "rate",
                "ko", "soin", "stat_haut", "stat_bas", "statut", "changement", "victoire",
                "clic", "retour"]

        for nom in noms:
            chemin = os.path.join(self.audio.dossier, "audio", "sons", nom + ".wav")
            self.assertTrue(os.path.exists(chemin), nom)

            with wave.open(chemin) as fichier:
                self.assertGreater(fichier.getnframes(), 0)

    def test_les_musiques_existent(self):
        for musique in self.audio.musiques:
            self.assertNotEqual(musique.chemin(self.audio.dossier), "", musique.nom)

    def test_volume_des_bruitages(self):
        self.assertEqual(self.audio._trouver_bruitage("clic").volume, 0.1)
        # Un bruitage qui n'est pas dans la liste est créé à volume 1, puis rangé.
        self.assertEqual(self.audio._trouver_bruitage("soin").volume, 1.0)
        self.assertIs(self.audio._trouver_bruitage("soin"), self.audio._trouver_bruitage("soin"))


if __name__ == "__main__":
    unittest.main()
