"""Tests des fonctions de création des Pokémon et des attaques (donnees/)."""

import unittest

from donnees.attaques import creer_lance_flammes
from donnees.attaques import creer_plenitude
from donnees.attaques import creer_vive_attaque
from donnees.pokemons import creer_dracaufeu
from donnees.pokemons import creer_gardevoir
from donnees.pokemons import creer_raichu
from donnees.pokemons import creer_tous_les_pokemon
from modeles.attaque import Attaque
from modeles.pokemon import Pokemon
from modeles.statistiques import Statistiques


class TestDonnees(unittest.TestCase):
    """Vérifie que les données sont de vrais objets, avec les bonnes valeurs."""

    def test_six_pokemon_de_vrais_objets(self):
        """On obtient 6 objets Pokemon, chacun avec 4 objets Attaque."""
        tous_les_pokemon = creer_tous_les_pokemon()

        self.assertEqual(len(tous_les_pokemon), 6)

        for pokemon in tous_les_pokemon:
            self.assertIsInstance(pokemon, Pokemon)
            self.assertEqual(len(pokemon.attaques), 4)

            for attaque in pokemon.attaques:
                self.assertIsInstance(attaque, Attaque)

    def test_noms_et_types(self):
        """Les noms et les types des 6 Pokémon sont corrects."""
        noms_attendus = ["Dracaufeu", "Florizarre", "Raichu",
                         "Laggron", "Gardevoir", "Tyranocif"]
        types_attendus = [["Feu", "Vol"], ["Plante", "Poison"], ["Électrik"],
                          ["Eau", "Sol"], ["Psy"], ["Roche", "Ténèbres"]]
        tous_les_pokemon = creer_tous_les_pokemon()

        for position in range(6):
            pokemon = tous_les_pokemon[position]

            noms_types_obtenus = []
            for type_pokemon in pokemon.types:
                noms_types_obtenus.append(type_pokemon.nom)

            self.assertEqual(pokemon.nom, noms_attendus[position])
            self.assertEqual(noms_types_obtenus, types_attendus[position])

    def test_stats_dracaufeu(self):
        """Dracaufeu niveau 50, IV 31 : 153 PV et 120 de Vitesse."""
        dracaufeu = creer_dracaufeu(50, Statistiques.identiques(31))

        self.assertEqual(dracaufeu.pv_max, 153)
        self.assertEqual(dracaufeu.pv, 153)
        self.assertEqual(dracaufeu.stats.vitesse, 120)

    def test_vitesse_de_raichu_en_generation_3(self):
        """Raichu a 100 de Vitesse de base (110 seulement depuis la génération 6)."""
        raichu = creer_raichu(50, Statistiques.identiques(31))

        # (2 x 100 + 31) x 50 // 100 + 5 = 120
        self.assertEqual(raichu.stats.vitesse, 120)

    def test_gardevoir_est_de_type_psy_seul(self):
        """En génération 3, il n'y a pas de type Fée."""
        gardevoir = creer_gardevoir()

        self.assertEqual(len(gardevoir.types), 1)

    def test_valeurs_d_une_attaque(self):
        """Lance-Flammes : 95 de puissance en génération 3, spéciale."""
        lance_flammes = creer_lance_flammes()

        self.assertEqual(lance_flammes.puissance, 95)
        self.assertEqual(lance_flammes.precision, 100)
        self.assertEqual(lance_flammes.pp, 15)
        self.assertTrue(lance_flammes.est_speciale)
        self.assertFalse(lance_flammes.est_de_statut)

    def test_attaque_de_statut_et_priorite(self):
        """Plénitude n'inflige pas de dégâts ; Vive-Attaque a +1 de priorité."""
        plenitude = creer_plenitude()
        vive_attaque = creer_vive_attaque()

        self.assertTrue(plenitude.est_de_statut)
        self.assertEqual(len(plenitude.effets), 2)
        self.assertEqual(vive_attaque.priorite, 1)

    def test_chaque_pokemon_a_ses_propres_pp(self):
        """Utiliser une attaque d'un Pokémon ne change pas celle d'un autre."""
        premier = creer_dracaufeu()
        second = creer_dracaufeu()

        premier.attaques[0].utiliser_pp()

        self.assertEqual(premier.attaques[0].pp, 14)
        self.assertEqual(second.attaques[0].pp, 15)


if __name__ == "__main__":
    unittest.main()
