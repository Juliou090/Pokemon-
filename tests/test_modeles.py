"""Tests des modèles : types, stats, Pokémon (PV privés), équipe, attaques, statuts.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import unittest

from donnees.catalogue import Catalogue
from exceptions import (
    ActionInvalideError,
    DonneesInvalidesError,
    PVInvalideError,
    PokemonKOError,
)
from modeles.attaque import EffetStatut
from modeles.dresseur import Equipe
from modeles.statistiques import Nature, Statistiques
from modeles.statuts import Brulure, Paralysie, Poison, Sommeil


def types(*noms):
    liste = []
    for nom in noms:
        liste.append(Catalogue.type(nom))
    return liste


class TestTypes(unittest.TestCase):
    def test_efficacite_simple(self):
        self.assertEqual(Catalogue.type("Eau").efficacite_contre(Catalogue.type("Feu")), 2.0)
        self.assertEqual(Catalogue.type("Feu").efficacite_contre(Catalogue.type("Eau")), 0.5)
        self.assertEqual(Catalogue.type("Normal").efficacite_contre(Catalogue.type("Spectre")), 0.0)

    def test_double_type(self):
        self.assertEqual(Catalogue.type("Roche").efficacite_contre_pokemon(types("Feu", "Vol")), 4.0)
        self.assertEqual(Catalogue.type("Sol").efficacite_contre_pokemon(types("Vol")), 0.0)
        self.assertEqual(Catalogue.type("Électrik").efficacite_contre_pokemon(types("Eau", "Sol")), 0.0)
        self.assertEqual(Catalogue.type("Plante").efficacite_contre_pokemon(types("Eau", "Sol")), 4.0)
        self.assertEqual(Catalogue.type("Psy").efficacite_contre_pokemon(types("Roche", "Ténèbres")), 0.0)

    def test_physique_ou_special(self):
        self.assertTrue(Catalogue.type("Feu").special)
        self.assertFalse(Catalogue.type("Sol").special)


class TestStats(unittest.TestCase):
    def test_dracaufeu_niveau_50(self):
        dracaufeu = Catalogue.pokemon(0, 50, Statistiques(31))

        self.assertEqual(dracaufeu.pv_max, 153)
        self.assertEqual(dracaufeu.stats.vitesse, 120)

    def test_nature(self):
        base = Statistiques(78, 84, 78, 109, 85, 100)
        rigide = Nature("Rigide", "attaque", "attaque_speciale")
        stats = base.calculer(Statistiques(31), Statistiques(0), 50, rigide)

        self.assertEqual(stats.attaque, 114)
        self.assertEqual(stats.attaque_speciale, 116)

    def test_tous_les_statuts_existent_dans_le_catalogue(self):
        identifiants = []

        for numero in range(Catalogue.nombre_de_pokemon()):
            for attaque in Catalogue.pokemon(numero).attaques:
                for effet in attaque.effets:
                    if isinstance(effet, EffetStatut):
                        identifiants.append(effet.identifiant_statut)

        for statut in ["poison", "brulure", "paralysie", "sommeil", "gel"]:
            self.assertIn(statut, identifiants)

    def test_25_natures_et_15_pokemon(self):
        self.assertEqual(len(Catalogue.natures()), 25)
        self.assertEqual(Catalogue.nombre_de_pokemon(), 15)

        for numero in range(Catalogue.nombre_de_pokemon()):
            self.assertEqual(len(Catalogue.pokemon(numero).attaques), 4)


class TestPokemon(unittest.TestCase):
    def setUp(self):
        self.pokemon = Catalogue.pokemon(0, 50, Statistiques(31))

    def test_pv_invalides(self):
        with self.assertRaises(PVInvalideError):
            self.pokemon.set_pv(-1)

        with self.assertRaises(PVInvalideError):
            self.pokemon.set_pv(999)

    def test_ko(self):
        self.assertEqual(self.pokemon.subir_degats(1000), 153)
        self.assertTrue(self.pokemon.est_ko())

        with self.assertRaises(PokemonKOError):
            self.pokemon.verifier_peut_agir()

        with self.assertRaises(PokemonKOError):
            self.pokemon.soigner(10)

    def test_soin_plafonne(self):
        self.pokemon.subir_degats(10)

        self.assertEqual(self.pokemon.soigner(50), 10)

    def test_niveau_invalide(self):
        with self.assertRaises(DonneesInvalidesError):
            Catalogue.pokemon(0, 101)

    def test_paliers(self):
        self.assertEqual(self.pokemon.modifier_palier("attaque", 4), 4)
        self.assertEqual(self.pokemon.modifier_palier("attaque", 4), 2)
        self.assertEqual(self.pokemon.modifier_palier("attaque", 1), 0)

        # Palier +6 : la stat est multipliée par 4.
        base = self.pokemon.stats.attaque
        self.assertEqual(self.pokemon.stat_effective("attaque"), base * 4)

    def test_pp(self):
        attaque = Catalogue.attaque("Séisme")

        for essai in range(10):
            attaque.utiliser_pp()

        with self.assertRaises(ActionInvalideError):
            attaque.utiliser_pp()


class TestEquipeEtStatuts(unittest.TestCase):
    def test_equipe_de_la_bonne_taille(self):
        with self.assertRaises(DonneesInvalidesError):
            Equipe([Catalogue.pokemon(0), Catalogue.pokemon(1)])

    def test_changement_refuse_vers_un_ko_ou_l_actif(self):
        equipe = Equipe([Catalogue.pokemon(0), Catalogue.pokemon(1), Catalogue.pokemon(2)])
        equipe.pokemons[1].subir_degats(1000)

        with self.assertRaises(PokemonKOError):
            equipe.changer_actif(1)

        with self.assertRaises(ActionInvalideError):
            equipe.changer_actif(0)

    def test_statuts(self):
        laggron = Catalogue.pokemon(3, 50, Statistiques(31))

        self.assertTrue(laggron.appliquer_statut(Paralysie()))
        self.assertFalse(laggron.appliquer_statut(Poison()))
        self.assertEqual(laggron.stat_effective("vitesse"), laggron.stats.vitesse // 4)

        # Un type Poison ne peut pas être empoisonné, un type Feu ne peut pas être brûlé.
        self.assertFalse(Catalogue.pokemon(1).appliquer_statut(Poison()))
        self.assertFalse(Catalogue.pokemon(0).appliquer_statut(Brulure()))

    def test_sommeil_dure_de_1_a_4_tours(self):
        for essai in range(30):
            pokemon = Catalogue.pokemon(3)
            pokemon.appliquer_statut(Sommeil())
            tours = 0

            while pokemon.statut is not None:
                if not pokemon.statut.peut_agir(pokemon):
                    tours = tours + 1

            self.assertTrue(1 <= tours <= 4)


if __name__ == "__main__":
    unittest.main()
