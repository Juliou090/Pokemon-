"""Tests des objets, du sac, des dégâts et du combat complet (avec des menus « robots »).
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import contextlib
import io
import random
import unittest

from combat.actions import ActionAttaque
from combat.calcul_degats import CalculDegats
from combat.combat import Combat
from donnees.catalogue import Catalogue
from exceptions import ActionInvalideError, ObjetIndisponibleError
from modeles.dresseur import Dresseur, Equipe, Sac
from modeles.objets import ObjetTenu, Soin
from modeles.statistiques import Statistiques
from modeles.statuts import Poison
from ui.affichage import Affichage


def un_dresseur(nom, numeros):
    iv = Statistiques.identiques(31)
    pokemons = []
    for numero in numeros:
        pokemons.append(Catalogue.pokemon(numero, 50, iv))

    return Dresseur(nom, Equipe(pokemons), Catalogue.sac("standard"))


class TestObjets(unittest.TestCase):
    def setUp(self):
        self.dresseur = un_dresseur("Test", [0, 2, 4])
        self.dracaufeu = self.dresseur.equipe.pokemons[0]

    def test_potion(self):
        self.dracaufeu.subir_degats(50)
        self.dresseur.utiliser_objet("Potion", self.dracaufeu)

        self.assertEqual(self.dracaufeu.get_pv(), 153 - 50 + 20)
        self.assertEqual(self.dresseur.sac.trouver("Potion").nom, "Potion")

    def test_objet_refuse_n_est_pas_consomme(self):
        avant = self.dresseur.sac.lignes[0].quantite

        with self.assertRaises(ActionInvalideError):
            self.dresseur.utiliser_objet("Potion", self.dracaufeu)

        self.assertEqual(self.dresseur.sac.lignes[0].quantite, avant)

    def test_rappel_sur_un_pokemon_vivant_refuse(self):
        with self.assertRaises(ActionInvalideError):
            self.dresseur.verifier_objet("Rappel", self.dracaufeu)

    def test_rappel_ranime(self):
        self.dracaufeu.subir_degats(1000)
        self.dresseur.utiliser_objet("Rappel", self.dracaufeu)

        self.assertEqual(self.dracaufeu.get_pv(), 153 // 2)

    def test_antidote(self):
        self.dracaufeu.appliquer_statut(Poison())
        self.dresseur.utiliser_objet("Antidote", self.dracaufeu)

        self.assertIsNone(self.dracaufeu.statut)

    def test_objet_epuise(self):
        sac = Sac()
        sac.ajouter(Soin("Potion", 20), 1)
        sac.retirer("Potion")

        with self.assertRaises(ObjetIndisponibleError):
            sac.retirer("Potion")

    def test_objets_tenus(self):
        self.dracaufeu.objet_tenu = ObjetTenu("restes")
        self.dracaufeu.subir_degats(50)
        self.dracaufeu.objet_tenu.fin_de_tour(self.dracaufeu)
        self.assertEqual(self.dracaufeu.get_pv(), 153 - 50 + 153 // 16)

        self.dracaufeu.objet_tenu = ObjetTenu("baie")
        self.dracaufeu.subir_degats(100)
        self.dracaufeu.objet_tenu.fin_de_tour(self.dracaufeu)
        self.assertIsNone(self.dracaufeu.objet_tenu)


class TestDegats(unittest.TestCase):
    def test_formule_de_base(self):
        # ((2 x 50 / 5 + 2) x 100 x 100 / 100) / 50 + 2 = 46
        self.assertEqual(CalculDegats.formule_de_base(50, 100, 100, 100, False), 46)
        self.assertEqual(CalculDegats.formule_de_base(50, 100, 100, 100, True), 24)

    def test_immunite_et_super_efficace(self):
        iv = Statistiques.identiques(31)
        raichu = Catalogue.pokemon(2, 50, iv)
        laggron = Catalogue.pokemon(3, 50, iv)
        tyranocif = Catalogue.pokemon(5, 50, iv)
        dracaufeu = Catalogue.pokemon(0, 50, iv)

        sans_effet = CalculDegats.calculer(raichu, laggron, Catalogue.attaque("Tonnerre"))
        quadruple = CalculDegats.calculer(tyranocif, dracaufeu, Catalogue.attaque("Éboulement"))

        self.assertEqual(sans_effet.degats, 0)
        self.assertEqual(quadruple.efficacite, 4.0)
        self.assertGreater(quadruple.degats, 0)


class MenusRobot:
    """Faux menus : le robot attaque toujours (ou abandonne si on le lui dit)."""

    def __init__(self, abandonne=""):
        self.abandonne = abandonne

    def menu_principal(self, dresseur):
        if dresseur.nom == self.abandonne:
            return 5

        return 1

    def choisir_attaque(self, pokemon):
        for position in range(len(pokemon.attaques)):
            if pokemon.attaques[position].pp > 0:
                return position

        return 0

    def choisir_pokemon(self, equipe, question, retour_possible):
        for position in range(len(equipe.pokemons)):
            if not equipe.pokemons[position].est_ko() and position != equipe.indice_actif:
                return position

        return 0

    def choisir_objet(self, dresseur):
        return ""

    def confirmer(self, question):
        return True

    def attendre_entree(self):
        pass


class TestCombat(unittest.TestCase):
    def jouer(self, menus, graine=0):
        random.seed(graine)
        self.alice = un_dresseur("Alice", [0, 2, 4])
        self.bob = un_dresseur("Bob", [3, 5, 1])
        combat = Combat(self.alice, self.bob, Affichage(delai=0), menus)

        with contextlib.redirect_stdout(io.StringIO()):
            return combat.lancer()

    def test_le_combat_se_termine(self):
        for graine in range(20):
            vainqueur = self.jouer(MenusRobot(), graine)
            perdant = self.alice
            if vainqueur is self.alice:
                perdant = self.bob

            if vainqueur is not None:
                self.assertTrue(perdant.equipe.est_vaincue())
                self.assertGreaterEqual(len(vainqueur.equipe.vivants()), 1)

    def test_abandon(self):
        vainqueur = self.jouer(MenusRobot("Alice"))

        self.assertIs(vainqueur, self.bob)
        self.assertFalse(self.alice.equipe.est_vaincue())

    def test_pas_d_attaque_sur_une_cible_ko(self):
        alice = un_dresseur("Alice", [0, 2, 4])
        bob = un_dresseur("Bob", [3, 5, 1])
        bob.pokemon_actif().subir_degats(1000)

        action = ActionAttaque(alice, Catalogue.attaque("Surf"))

        self.assertEqual(action.executer(bob), [])

    def test_lutte_sans_pp(self):
        alice = un_dresseur("Alice", [0, 2, 4])
        bob = un_dresseur("Bob", [3, 5, 1])

        for attaque in alice.pokemon_actif().attaques:
            attaque.pp = 0

        random.seed(1)
        action = ActionAttaque(alice, Catalogue.attaque_lutte())
        messages = action.executer(bob)

        self.assertIn("Lutte", " ".join(messages))
        self.assertIn("contrecoup", " ".join(messages))


if __name__ == "__main__":
    unittest.main()
