"""Les 4 modes de création d'équipe.

J'ai mis les 4 modes dans une seule classe, avec une méthode par mode. Chacun fabrique la
liste des Pokémon (avec _fabriquer), choisit le sac de départ, puis renvoie un Dresseur prêt
à combattre.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import random

from donnees.catalogue import Catalogue
from modeles.dresseur import Dresseur, Equipe
from modeles.statistiques import Statistiques


class CreationEquipe:
    NOMS_DES_MODES = ["Classique", "Aléatoire total", "Équipes toutes faites", "Personnalisé"]
    DESCRIPTIONS = [
        "niveau 50 · tu choisis tes Pokémon · IV et natures aléatoires · sac standard",
        "tout est tiré au hasard : Pokémon, niveaux (30 à 70), IV, natures, objets",
        "tu choisis une équipe prête · niveau 50 · IV maximaux · sac standard",
        "tu décides de ce qui est choisi ou aléatoire (niveau, IV, natures, sac...)",
    ]

    def __init__(self, menus):
        self.menus = menus

    def creer_dresseur(self, nom_joueur, mode):
        """mode = 0, 1, 2 ou 3 (position dans NOMS_DES_MODES). Renvoie un Dresseur."""
        if mode == 0:
            numeros = self._choisir_a_la_main()
            pokemons = self._fabriquer(numeros, 50, 50, False, True, False)
            return Dresseur(nom_joueur, Equipe(pokemons), Catalogue.sac("standard"))

        if mode == 1:
            numeros = self._tirer_au_hasard()
            pokemons = self._fabriquer(numeros, 30, 70, False, True, True)
            return Dresseur(nom_joueur, Equipe(pokemons), Catalogue.sac("aleatoire"))

        if mode == 2:
            return self._equipe_toute_faite(nom_joueur)

        return self._personnalise(nom_joueur)

    # --- Briques communes ----------------------------------------------------
    def _choisir_a_la_main(self):
        catalogue = []
        for numero in range(Catalogue.nombre_de_pokemon()):
            catalogue.append(Catalogue.pokemon(numero))

        choisis = []
        while len(choisis) < Equipe.TAILLE:
            choisis.append(self.menus.choisir_pokemon_du_catalogue(catalogue, choisis))

        return choisis

    def _tirer_au_hasard(self):
        choisis = []

        while len(choisis) < Equipe.TAILLE:
            numero = random.randint(0, Catalogue.nombre_de_pokemon() - 1)

            if numero not in choisis:
                choisis.append(numero)

        return choisis

    def _fabriquer(self, numeros, niveau_min, niveau_max, iv_maximaux,
                   natures_aleatoires, objets_tenus):
        """Construit les Pokémon avec les réglages demandés."""
        pokemons = []

        for numero in numeros:
            niveau = random.randint(niveau_min, niveau_max)

            iv = None
            if iv_maximaux:
                iv = Statistiques(31)

            nature = Catalogue.nature_neutre()
            if natures_aleatoires:
                nature = random.choice(Catalogue.natures())

            pokemon = Catalogue.pokemon(numero, niveau, iv, nature)

            if objets_tenus:
                pokemon.objet_tenu = Catalogue.objet_tenu_aleatoire()

            pokemons.append(pokemon)

        return pokemons

    # --- Mode « équipes toutes faites » ----------------------------------------
    def _equipe_toute_faite(self, nom_joueur):
        # Le texte de chaque équipe : son nom, puis les noms de ses Pokémon.
        options = []
        for indice in range(len(Catalogue.NOMS_DES_EQUIPES)):
            noms = ""
            for numero in Catalogue.numeros_de_l_equipe(indice):
                noms = noms + Catalogue.pokemon(numero).nom + ", "

            options.append(Catalogue.NOMS_DES_EQUIPES[indice] + " : " + noms.strip(", "))

        choix = self.menus.choisir_option("Choisis ton équipe", options)

        pokemons = self._fabriquer(Catalogue.numeros_de_l_equipe(choix), 50, 50,
                                   True, False, False)

        return Dresseur(nom_joueur, Equipe(pokemons), Catalogue.sac("standard"))

    # --- Mode personnalisé : chaque réglage est « choisi » ou « aléatoire » ------
    def _personnalise(self, nom_joueur):
        m = self.menus
        m.affichage.titre("Réglages de " + nom_joueur)

        a_la_main = m.choisir_option("Pokémon", ["Je choisis mes Pokémon", "Aléatoires"]) == 0

        niveau_min = 1
        niveau_max = 100
        if m.choisir_option("Niveau", ["Niveau fixe (je le choisis)",
                                       "Niveaux aléatoires (1 à 100)"]) == 0:
            niveau_min = m.lire_entier("Niveau des Pokémon (1 à 100) ?", 1, 100)
            niveau_max = niveau_min

        iv_maximaux = m.choisir_option("IV (talent naturel)",
                                       ["Maximums (31 partout)", "Aléatoires (0 à 31)"]) == 0
        natures = m.choisir_option("Natures", ["Neutre", "Aléatoires"]) == 1
        objets_tenus = m.choisir_option("Objets tenus", ["Aucun", "Aléatoires"]) == 1
        choix_sac = m.choisir_option("Sac d'objets", ["Standard", "Aléatoire", "Vide"])

        if a_la_main:
            numeros = self._choisir_a_la_main()
        else:
            numeros = self._tirer_au_hasard()

        pokemons = self._fabriquer(numeros, niveau_min, niveau_max, iv_maximaux,
                                   natures, objets_tenus)

        sac = Catalogue.sac("vide")
        if choix_sac == 0:
            sac = Catalogue.sac("standard")
        elif choix_sac == 1:
            sac = Catalogue.sac("aleatoire")

        return Dresseur(nom_joueur, Equipe(pokemons), sac)
