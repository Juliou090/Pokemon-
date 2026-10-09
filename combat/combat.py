"""Classe Combat : déroule le combat tour par tour entre deux Dresseurs.

On a le droit ici : la boucle de combat, la collecte des actions, leur exécution dans le bon ordre,
l'application des effets de fin de tour, le test de fin de combat.
On N'A PAS le droit : de print (on appelle l'objet Affichage reçu), de calculer les dégâts (calcul_degats.py),
ni de connaître le détail d'une attaque ou d'un objet précis.
"""

from combat.actions import (
    Action,
    ActionAbandon,
    ActionAttaque,
    ActionChangement,
    ActionObjet,
)
from combat.ordre import OrdreDesActions
from modeles.dresseur import Dresseur
from ui.menus import Menus


class Combat:
    """Un combat entre deux dresseurs.

    Attributs prévus :
        # _dresseur1, _dresseur2 : Dresseur
        # _affichage : Affichage   (reçu du Jeu)
        # _saisie : Saisie         (reçu du Jeu)
        # _numero_tour : int
        # _meteo : Meteo | None    (niveau 2)
    """

    def __init__(self, dresseur1: Dresseur, dresseur2: Dresseur, affichage, saisie) -> None:
        self._dresseur1 = dresseur1
        self._dresseur2 = dresseur2
        self._affichage = affichage
        self._saisie = saisie
        self._numero_tour = 1
        self._meteo = None  # niveau 2, pas encore utilisée

    def lancer(self) -> Dresseur:
        """Boucle jusqu'à la fin ; renvoie le vainqueur."""
        while not self.est_termine():
            self._jouer_tour()

            # On applique les effets de fin de tour
            self._fin_de_tour()

            # On vérifie si un Pokémon est KO et qu'il faut le remplacer
            for dresseur in (self._dresseur1, self._dresseur2):
                if dresseur.pokemon_actif.est_ko:
                    self._remplacer_ko(dresseur)

            # Vérification de fin de combat
            if self.est_termine():
                break

        return self.vainqueur()

    def _demander_action(self, dresseur: Dresseur) -> Action:
        """Utilise Menus/Saisie pour obtenir l'action choisie par ce dresseur."""
        menus = Menus(self._saisie, self._affichage)
        choix = menus.menu_principal(dresseur).strip()

        if choix == "1":
            indice_attaque = menus.choisir_attaque(dresseur)
            attaque = dresseur.pokemon_actif.attaques[indice_attaque]
            return ActionAttaque(dresseur, attaque)

        if choix == "2":
            indice_pokemon = menus.choisir_pokemon(dresseur)
            return ActionChangement(dresseur, indice_pokemon)

        if choix == "3":
            nom_objet = menus.choisir_objet(dresseur)
            indice_cible = menus.choisir_pokemon(dresseur)
            return ActionObjet(dresseur, nom_objet, indice_cible)

        if choix == "4":
            return ActionAbandon(dresseur)

        raise ValueError(f"Choix d'action invalide : {choix!r}")

    def _jouer_tour(self) -> None:
        """Collecte les 2 actions, les trie (ordre.py), les exécute, gère le fin de tour."""
        action1 = self._demander_action(self._dresseur1)
        action2 = self._demander_action(self._dresseur2)

        actions = [action1, action2]
        actions_triees = OrdreDesActions().trier(actions)

        for action in actions_triees:
            if action.acteur is self._dresseur1:
                adversaire = self._dresseur2
            else:
                adversaire = self._dresseur1

            messages = action.executer(adversaire, self)
            if messages:
                self._affichage.messages(messages)

        self._numero_tour += 1

    def _fin_de_tour(self) -> None:
        """Dégâts de statut, objets tenus, météo..."""
        messages = []

        for dresseur in (self._dresseur1, self._dresseur2):
            pokemon = dresseur.pokemon_actif

            if pokemon is None or pokemon.est_ko:
                continue

            if pokemon.statut is not None:
                degats = pokemon.statut.degats_fin_de_tour(pokemon)
                if degats > 0:
                    pokemon.subir_degats(degats)
                    messages.append(
                        f"{pokemon.nom} perd {degats} PV à cause du statut {pokemon.statut.nom}."
                    )

                message_statut = pokemon.statut.fin_de_tour(pokemon)
                if message_statut:
                    messages.append(message_statut)

            if pokemon.objet_tenu is not None:
                message_objet = pokemon.objet_tenu.fin_de_tour(pokemon)
                if message_objet:
                    messages.append(message_objet)

            if self._meteo is not None:
                degats_meteo = self._meteo.fin_de_tour(pokemon)
                if degats_meteo > 0:
                    pokemon.subir_degats(degats_meteo)
                    messages.append(
                        f"{pokemon.nom} perd {degats_meteo} PV à cause de la météo {self._meteo.nom}."
                    )

        if messages:
            self._affichage.messages(messages)

    def _remplacer_ko(self, dresseur: Dresseur) -> None:
        """Si le Pokémon actif est K.O., demande un remplaçant (ou fin de combat)."""
        if not dresseur.pokemon_actif.est_ko:
            return

        if dresseur.equipe.est_vaincue():
            dresseur.abandonner()
            return

        menus = Menus(self._saisie, self._affichage)
        indice = menus.choisir_pokemon(dresseur)
        dresseur.equipe.changer_actif(indice)

    def est_termine(self) -> bool:
        """Le combat est terminé si un dresseur a perdu ou abandonné."""
        return (
            self._dresseur1.a_perdu()
            or self._dresseur2.a_perdu()
            or self._dresseur1.equipe.est_vaincue()
            or self._dresseur2.equipe.est_vaincue()
        )

    def vainqueur(self) -> Dresseur:
        """Renvoie le dresseur gagnant, ou lève une erreur si le combat n'est pas terminé."""
        dresseur1_a_perdu = self._dresseur1.a_perdu() or self._dresseur1.equipe.est_vaincue()
        dresseur2_a_perdu = self._dresseur2.a_perdu() or self._dresseur2.equipe.est_vaincue()

        if dresseur1_a_perdu and dresseur2_a_perdu:
            raise ValueError("Les deux dresseurs ont perdu : aucun vainqueur possible.")

        if dresseur1_a_perdu:
            return self._dresseur2

        if dresseur2_a_perdu:
            return self._dresseur1

        raise ValueError("Le combat n'est pas terminé : aucun vainqueur ne peut être déterminé.")
        

