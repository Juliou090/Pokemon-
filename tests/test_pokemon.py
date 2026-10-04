"""Tests de Pokemon : PV privés, PVInvalideError, PokemonKOError, soins."""

import unittest

from donnees.pokemons import creer_dracaufeu
from exceptions import PokemonKOError
from exceptions import PVInvalideError
from modeles.statistiques import Statistiques


class TestPokemon(unittest.TestCase):
    """Vérifie l'encapsulation des PV et les exceptions."""

    def setUp(self):
        """Crée un Dracaufeu niveau 50 avec des IV fixes (153 PV)."""
        self.pokemon = creer_dracaufeu(50, Statistiques.identiques(31))

    def test_pv_negatifs_refuses(self):
        """Affecter des PV négatifs lève PVInvalideError."""
        with self.assertRaises(PVInvalideError):
            self.pokemon.pv = -1

    def test_pv_trop_grands_refuses(self):
        """Affecter plus que les PV max lève PVInvalideError."""
        with self.assertRaises(PVInvalideError):
            self.pokemon.pv = 154

    def test_pv_valides_acceptes(self):
        """Une valeur cohérente est acceptée."""
        self.pokemon.pv = 100

        self.assertEqual(self.pokemon.pv, 100)

    def test_degats_sans_descendre_sous_zero(self):
        """Trop de dégâts mettent le Pokémon K.O. avec 0 PV."""
        degats_reels = self.pokemon.subir_degats(1000)

        self.assertEqual(self.pokemon.pv, 0)
        self.assertEqual(degats_reels, 153)
        self.assertTrue(self.pokemon.est_ko)

    def test_pokemon_ko_ne_peut_pas_agir(self):
        """Un Pokémon K.O. lève PokemonKOError."""
        self.pokemon.subir_degats(1000)

        with self.assertRaises(PokemonKOError):
            self.pokemon.verifier_peut_agir()

    def test_soin_plafonne_au_maximum(self):
        """Un soin ne dépasse jamais les PV max."""
        self.pokemon.subir_degats(10)

        pv_rendus = self.pokemon.soigner(50)

        self.assertEqual(pv_rendus, 10)
        self.assertEqual(self.pokemon.pv, 153)

    def test_soigner_un_ko_est_refuse(self):
        """On ne soigne pas un K.O. avec un simple soin."""
        self.pokemon.subir_degats(1000)

        with self.assertRaises(PokemonKOError):
            self.pokemon.soigner(20)


if __name__ == "__main__":
    unittest.main()
