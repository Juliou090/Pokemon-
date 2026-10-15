"""Le combat tour par tour entre deux dresseurs.

Charlotte a écrit la première version de cette classe : j'ai gardé sa structure
(lancer, _jouer_tour, _demander_action, _fin_de_tour, _remplacer_ko,
est_termine, vainqueur). Je l'ai complétée pour qu'elle marche avec le reste
du jeu (voir le détail dans les commentaires « Charlotte » plus bas).

Un tour se passe en 4 temps :
    1. chaque joueur choisit son action ;
    2. les actions sont classées (priorité, puis vitesse) et exécutées ;
    3. effets de fin de tour (poison, brûlure, Restes...) ;
    4. les Pokémon K.O. sont remplacés.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import random

from combat.actions import ActionAbandon, ActionAttaque, ActionChangement, ActionObjet
from donnees.catalogue import Catalogue
from exceptions import ActionInvalideError, ObjetIndisponibleError, PokemonKOError


class ResultatDegats:
    """Ce que renvoie Combat.calculer_degats : dégâts, efficacité totale, critique ?"""

    def __init__(self, degats, efficacite, critique):
        self.degats = degats
        self.efficacite = efficacite
        self.critique = critique


class Combat:
    def __init__(self, dresseur1, dresseur2, affichage, menus):
        self.dresseur1 = dresseur1
        self.dresseur2 = dresseur2
        self.affichage = affichage
        self.menus = menus
        self.numero_tour = 0

    def lancer(self):
        """Joue jusqu'à la fin. Renvoie le vainqueur (None en cas d'égalité)."""
        self.affichage.messages([
            self.dresseur1.nom + " et " + self.dresseur2.nom + " s'affrontent !",
            self.dresseur1.nom + " envoie " + self.dresseur1.pokemon_actif().nom + " !",
            self.dresseur2.nom + " envoie " + self.dresseur2.pokemon_actif().nom + " !",
        ])

        while not self.est_termine():
            self._jouer_tour()

        return self.vainqueur()

    def est_termine(self):
        return self.dresseur1.a_perdu() or self.dresseur2.a_perdu()

    def vainqueur(self):
        """Le dresseur qui n'a pas perdu. None si les deux ont perdu en même temps
        (Charlotte levait une erreur dans ce cas ; c'est possible, par exemple
        avec deux Pokémon K.O. par le poison à la fin du même tour)."""
        if self.dresseur1.a_perdu() and self.dresseur2.a_perdu():
            return None

        if self.dresseur1.a_perdu():
            return self.dresseur2

        return self.dresseur1

    # ------------------------------------------------------------------
    # Calcul des dégâts (formule de la génération 3, Bulbapedia, page « Damage »)
    #
    #   dégâts = ((((2 x Niveau / 5 + 2) x Puissance x A / D) / 50) x Brûlure + 2)
    #            x Critique x Aléatoire(85 à 100 %) x STAB x Type1 x Type2
    #
    # Le prof m'a conseillé de mettre ce calcul dans Combat, avec self, plutôt que
    # dans une classe à part dont les fonctions n'auraient eu besoin d'aucun objet :
    # c'est bien le combat qui calcule les dégâts.
    # ------------------------------------------------------------------
    def touche(self, attaque):
        """Test de précision (précision 0 = ne rate jamais)."""
        if attaque.precision == 0:
            return True

        return random.randint(1, 100) <= attaque.precision

    def formule_de_base(self, niveau, puissance, valeur_attaque, valeur_defense,
                        brule_et_physique):
        """La partie « ((2N/5+2) x P x A/D / 50) x Brûlure + 2 » (séparée pour les tests)."""
        degats = (2 * niveau // 5 + 2) * puissance * valeur_attaque // valeur_defense // 50

        if brule_et_physique:
            degats = degats // 2

        return degats + 2

    def calculer_degats(self, attaquant, defenseur, attaque):
        """Renvoie un ResultatDegats. Toutes les divisions gardent la partie entière."""
        if attaque.critique_eleve:
            critique = random.randint(1, 8) == 1
        else:
            critique = random.randint(1, 16) == 1

        if attaque.est_speciale():
            stat_attaque = "attaque_speciale"
            stat_defense = "defense_speciale"
        else:
            stat_attaque = "attaque"
            stat_defense = "defense"

        # Un coup critique ignore les baisses de l'attaquant et les hausses du défenseur.
        valeur_attaque = attaquant.stat_effective(stat_attaque, ignorer_baisses=critique)
        valeur_defense = defenseur.stat_effective(stat_defense, ignorer_hausses=critique)

        brule_et_physique = False
        if attaquant.statut is not None and attaquant.statut.identifiant == "brulure":
            brule_et_physique = not attaque.est_speciale()

        degats = self.formule_de_base(attaquant.niveau, attaque.puissance,
                                      valeur_attaque, valeur_defense, brule_et_physique)

        if critique:
            degats = degats * 2

        degats = degats * random.randint(85, 100) // 100

        efficacite = 1.0

        # Lutte ignore les types : ni STAB, ni efficacité.
        if not attaque.lutte:
            if attaquant.a_le_type(attaque.type.nom):
                degats = degats * 15 // 10

            efficacite = attaque.type.efficacite_contre_pokemon(defenseur.types)

            # Un type après l'autre, comme dans le jeu (pour les arrondis).
            for type_defenseur in defenseur.types:
                multiplicateur = attaque.type.efficacite_contre(type_defenseur)

                if multiplicateur == 2.0:
                    degats = degats * 2
                elif multiplicateur == 0.5:
                    degats = degats // 2
                elif multiplicateur == 0.0:
                    degats = 0

        # Une attaque qui touche fait au moins 1 dégât, sauf immunité.
        if efficacite > 0 and degats < 1:
            degats = 1

        return ResultatDegats(degats, efficacite, critique)

    # ------------------------------------------------------------------
    def _adversaire_de(self, dresseur):
        if dresseur is self.dresseur1:
            return self.dresseur2

        return self.dresseur1

    # ------------------------------------------------------------------
    def _jouer_tour(self):
        self.numero_tour = self.numero_tour + 1

        action1 = self._demander_action(self.dresseur1)

        # J'efface l'écran pour que le joueur 2 ne voie pas le choix du joueur 1.
        self.affichage.effacer_ecran()
        action2 = self._demander_action(self.dresseur2)
        self.affichage.effacer_ecran()
        self.affichage.separateur_tour(self.numero_tour)

        # La musique baisse un peu pour laisser entendre les bruitages.
        self.affichage.musique_discrete()

        for action in self._ordonner(action1, action2):
            if self.est_termine():
                break

            adversaire = self._adversaire_de(action.acteur)
            self.affichage.messages(action.executer(adversaire, self))

        self.affichage.musique_normale()

        if not self.est_termine():
            self._fin_de_tour()

        if not self.est_termine():
            self._remplacer_ko()

    def _ordonner(self, action1, action2):
        """Priorité d'abord, puis vitesse du Pokémon, puis pile ou face."""
        if action1.priorite != action2.priorite:
            premiere_est_action1 = action1.priorite > action2.priorite
        elif action1.vitesse() != action2.vitesse():
            premiere_est_action1 = action1.vitesse() > action2.vitesse()
        else:
            premiere_est_action1 = random.randint(0, 1) == 0

        if premiere_est_action1:
            return [action1, action2]

        return [action2, action1]

    # ------------------------------------------------------------------
    def _demander_action(self, dresseur):
        """Redemande tant que le joueur n'a pas choisi une action valide.

        Charlotte : son _demander_action plantait (ValueError) sur un mauvais
        choix, et un Rappel sur un Pokémon vivant n'était pas géré. Ici chaque
        erreur est expliquée au joueur, qui peut choisir autre chose.
        """
        while True:
            self.affichage.separateur_tour(self.numero_tour)
            self.affichage.etat_combat(self.dresseur1, self.dresseur2)
            choix = self.menus.menu_principal(dresseur)
            action = None

            if choix == 1:
                action = self._choisir_attaque(dresseur)
            elif choix == 2:
                action = self._choisir_changement(dresseur)
            elif choix == 3:
                action = self._choisir_objet(dresseur)
            elif choix == 4:
                self.affichage.equipe_detaillee(dresseur)
                self.menus.attendre_entree()
            elif self.menus.confirmer(dresseur.nom + ", abandonner vraiment ?"):
                action = ActionAbandon(dresseur)

            # None = le joueur a fait « retour » : on lui redemande.
            if action is not None:
                return action

    def _choisir_attaque(self, dresseur):
        pokemon = dresseur.pokemon_actif()

        # Si toutes les attaques sont à 0 PP, il utilise Lutte.
        if not pokemon.a_encore_des_pp():
            self.affichage.messages([pokemon.nom + " n'a plus de PP !"])
            return ActionAttaque(dresseur, Catalogue.attaque_lutte())

        indice = self.menus.choisir_attaque(pokemon)

        if indice == -1:
            return None

        return ActionAttaque(dresseur, pokemon.attaques[indice])

    def _choisir_changement(self, dresseur):
        while True:
            indice = self.menus.choisir_pokemon(dresseur.equipe, "Quel Pokémon envoyer ?", True)

            if indice == -1:
                return None

            try:
                dresseur.equipe.verifier_changement(indice)
            except (ActionInvalideError, PokemonKOError) as erreur:
                self.affichage.erreur(str(erreur))
                continue

            return ActionChangement(dresseur, indice)

    def _choisir_objet(self, dresseur):
        while True:
            nom_objet = self.menus.choisir_objet(dresseur)

            if nom_objet == "":
                return None

            indice = self.menus.choisir_pokemon(
                dresseur.equipe, "Sur quel Pokémon utiliser " + nom_objet + " ?", True)

            if indice == -1:
                continue

            # Je vérifie tout de suite : si l'objet est inutile (Rappel sur un
            # Pokémon vivant...), le joueur le sait et l'objet n'est pas perdu.
            try:
                dresseur.verifier_objet(nom_objet, dresseur.equipe.pokemons[indice])
            except (ObjetIndisponibleError, ActionInvalideError) as erreur:
                self.affichage.erreur(str(erreur))
                continue

            return ActionObjet(dresseur, nom_objet, indice)

    # ------------------------------------------------------------------
    def _fin_de_tour(self):
        """Poison, brûlure et objets tenus agissent sur chaque Pokémon actif."""
        messages = []

        for dresseur in [self.dresseur1, self.dresseur2]:
            pokemon = dresseur.pokemon_actif()

            if pokemon.est_ko():
                continue

            if pokemon.statut is not None:
                degats = pokemon.statut.degats_fin_de_tour(pokemon)

                if degats > 0:
                    pokemon.subir_degats(degats)
                    messages.append(pokemon.statut.phrase_degats(pokemon) + " (-"
                                    + str(degats) + " PV)")

                    if pokemon.est_ko():
                        messages.append(pokemon.nom + " est K.O. !")

            if pokemon.objet_tenu is not None:
                phrase = pokemon.objet_tenu.fin_de_tour(pokemon)

                if phrase != "":
                    messages.append(phrase)

        self.affichage.messages(messages)

    def _remplacer_ko(self):
        """Chaque dresseur dont le Pokémon est K.O. en envoie un autre."""
        for dresseur in [self.dresseur1, self.dresseur2]:
            if dresseur.a_perdu() or not dresseur.pokemon_actif().est_ko():
                continue

            vivants = dresseur.equipe.vivants()

            # S'il ne reste qu'un Pokémon vivant, je n'ai pas besoin de demander.
            if len(vivants) == 1:
                indice = dresseur.equipe.pokemons.index(vivants[0])
            else:
                indice = self._demander_remplacant(dresseur)

            nouveau = dresseur.equipe.changer_actif(indice)
            self.affichage.messages([dresseur.nom + " envoie " + nouveau.nom + " !"])

    def _demander_remplacant(self, dresseur):
        while True:
            indice = self.menus.choisir_pokemon(
                dresseur.equipe, dresseur.nom + ", quel Pokémon envoyer ?", False)

            try:
                dresseur.equipe.verifier_changement(indice)
            except (ActionInvalideError, PokemonKOError) as erreur:
                self.affichage.erreur(str(erreur))
                continue

            return indice

