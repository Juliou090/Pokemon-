"""Tests de Equipe (taille fixée par l'attribut de classe TAILLE)."""

import unittest

from donnees.pokemons import creer_dracaufeu
from donnees.pokemons import creer_gardevoir
from donnees.pokemons import creer_raichu
from exceptions import EquipeInvalideError
from modeles.equipe import Equipe


class TestEquipe(unittest.TestCase):
    """Vérifie la taille de l'équipe et la détection de la défaite."""

    def test_taille_par_defaut(self):
        """Une équipe doit avoir Equipe.TAILLE Pokémon (3 pour l'instant)."""
        self.assertEqual(Equipe.TAILLE, 3)

    def test_equipe_de_trois(self):
        """Une équipe de 3 Pokémon est acceptée, le premier est actif."""
        pokemons = [creer_dracaufeu(), creer_raichu(), creer_gardevoir()]

        equipe = Equipe(pokemons)

        self.assertEqual(equipe.actif.nom, "Dracaufeu")
        self.assertEqual(len(equipe.vivants), 3)

    def test_equipe_de_deux_refusee(self):
        """Une équipe de 2 Pokémon lève EquipeInvalideError."""
        pokemons = [creer_dracaufeu(), creer_raichu()]

        with self.assertRaises(EquipeInvalideError):
            Equipe(pokemons)

    def test_equipe_vaincue(self):
        """L'équipe est vaincue quand tous ses Pokémon sont K.O."""
        pokemons = [creer_dracaufeu(), creer_raichu(), creer_gardevoir()]
        equipe = Equipe(pokemons)

        for pokemon in pokemons:
            pokemon.subir_degats(1000)

        self.assertTrue(equipe.est_vaincue())

    def test_objet_indisponible(self):
        """À écrire quand le Sac et le Dresseur seront implémentés."""
        self.skipTest("à écrire")


if __name__ == "__main__":
    unittest.main()
