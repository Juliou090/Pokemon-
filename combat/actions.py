"""Les quatre actions possibles à chaque tour : attaquer, changer de Pokémon, utiliser un
objet, abandonner.

J'ai fait une classe Action « de base » et une classe fille par action, chacune avec sa
méthode executer() qui renvoie les phrases à afficher. Comme ça, le combat appelle toujours
action.executer() sans avoir besoin de savoir de quelle action il s'agit : c'est le
polymorphisme.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

from exceptions import ActionInvalideError, ObjetIndisponibleError, PokemonKOError


class Action:
    # Un changement ou un objet passe avant les attaques (priorité plus haute).
    priorite = 0

    def __init__(self, acteur):
        self.acteur = acteur

    def vitesse(self):
        """Vitesse du Pokémon actif : elle départage deux actions de même priorité."""
        return self.acteur.pokemon_actif().stat_effective("vitesse")

    def executer(self, adversaire, combat):
        """adversaire = le Dresseur d'en face ; combat = le Combat en cours (c'est lui
        qui sait calculer les dégâts). Renvoie la liste des phrases à afficher."""
        return []


class ActionAttaque(Action):
    def __init__(self, acteur, attaque):
        super().__init__(acteur)
        self.attaque = attaque
        self.priorite = attaque.priorite

    def executer(self, adversaire, combat):
        messages = []
        attaquant = self.acteur.pokemon_actif()
        defenseur = adversaire.pokemon_actif()

        # Un Pokémon mis K.O. plus tôt dans le tour n'attaque pas.
        try:
            attaquant.verifier_peut_agir()
        except PokemonKOError:
            return messages

        # Si la cible est déjà K.O. (ex. par son propre contrecoup), il n'y a rien à frapper.
        if defenseur.est_ko():
            return messages

        # Le statut peut empêcher d'agir (sommeil, paralysie, gel).
        statut = attaquant.statut
        if statut is not None:
            peut_agir = statut.peut_agir(attaquant)

            if statut.message != "":
                messages.append(statut.message)

            if not peut_agir:
                return messages

        try:
            self.attaque.utiliser_pp()
        except ActionInvalideError as erreur:
            return messages + [str(erreur)]

        messages.append("[" + self.acteur.nom + "] " + attaquant.nom
                        + " utilise " + self.attaque.nom + " !")

        if not combat.touche(self.attaque):
            messages.append("L'attaque de " + attaquant.nom + " rate !")
        elif self.attaque.est_de_statut():
            self._attaque_de_statut(attaquant, defenseur, messages)
        else:
            self._attaque_qui_blesse(attaquant, defenseur, messages, combat)

        return messages

    def _attaque_de_statut(self, attaquant, defenseur, messages):
        """Pas de dégâts : on applique les effets, et on dit si rien n'a marché."""
        un_effet_a_marche = False

        for effet in self.attaque.effets:
            phrase = effet.appliquer(attaquant, defenseur)

            if phrase != "":
                messages.append(phrase)
                un_effet_a_marche = True

        if not un_effet_a_marche:
            messages.append("Mais ça échoue !")

    def _attaque_qui_blesse(self, attaquant, defenseur, messages, combat):
        resultat = combat.calculer_degats(attaquant, defenseur, self.attaque)

        if resultat.efficacite == 0.0:
            messages.append("Ça n'affecte pas " + defenseur.nom + "...")
            return

        reels = defenseur.subir_degats(resultat.degats)

        if resultat.critique:
            messages.append("Coup critique !")

        if resultat.efficacite > 1.0:
            messages.append("C'est super efficace !")
        elif resultat.efficacite < 1.0:
            messages.append("Ce n'est pas très efficace...")

        messages.append(defenseur.nom + " perd " + str(reels) + " PV ("
                        + str(defenseur.get_pv()) + "/" + str(defenseur.pv_max) + ").")

        if defenseur.est_ko():
            messages.append(defenseur.nom + " est K.O. !")

        # Génération 3 : une attaque de type Feu dégèle le Pokémon touché.
        if (self.attaque.type.nom == "Feu" and defenseur.statut is not None
                and defenseur.statut.identifiant == "gel" and not defenseur.est_ko()):
            defenseur.statut = None
            messages.append(defenseur.nom + " dégèle !")

        # Effets secondaires (ex. 10 % de brûlure).
        for effet in self.attaque.effets:
            phrase = effet.appliquer(attaquant, defenseur)

            if phrase != "":
                messages.append(phrase)

        # Lutte : le lanceur perd 1/4 des dégâts qu'il inflige.
        if self.attaque.lutte and reels > 0:
            recul = max(1, reels // 4)
            attaquant.subir_degats(recul)
            messages.append(attaquant.nom + " est blessé par le contrecoup (-"
                            + str(recul) + " PV).")

            if attaquant.est_ko():
                messages.append(attaquant.nom + " est K.O. !")


class ActionChangement(Action):
    priorite = 6

    def __init__(self, acteur, indice):
        super().__init__(acteur)
        self.indice = indice

    def executer(self, adversaire, combat):
        ancien = self.acteur.pokemon_actif()

        try:
            nouveau = self.acteur.equipe.changer_actif(self.indice)
        except (ActionInvalideError, PokemonKOError) as erreur:
            return ["Changement impossible : " + str(erreur)]

        return [self.acteur.nom + " rappelle " + ancien.nom + " et envoie " + nouveau.nom + " !"]


class ActionObjet(Action):
    priorite = 6

    def __init__(self, acteur, nom_objet, indice_cible):
        super().__init__(acteur)
        self.nom_objet = nom_objet
        self.indice_cible = indice_cible

    def executer(self, adversaire, combat):
        cible = self.acteur.equipe.pokemons[self.indice_cible]

        try:
            phrase = self.acteur.utiliser_objet(self.nom_objet, cible)
        except (ObjetIndisponibleError, ActionInvalideError, PokemonKOError) as erreur:
            return [self.acteur.nom + " veut utiliser " + self.nom_objet
                    + ", mais : " + str(erreur)]

        annonce = self.acteur.nom + " utilise " + self.nom_objet + " sur " + cible.nom + "."

        return [annonce, phrase]


class ActionAbandon(Action):
    priorite = 10

    def executer(self, adversaire, combat):
        self.acteur.a_abandonne = True

        return [self.acteur.nom + " abandonne le combat !"]
