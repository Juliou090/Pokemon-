"""Les menus : ils posent une question au joueur et renvoient sa réponse. Un menu ne décide
de rien : c'est le combat (ou le jeu) qui décide de la suite.

J'ai aussi ajouté ici une protection : après une mauvaise réponse, je fais une pause et je
vide le clavier. Sans ça, laisser la touche Entrée appuyée enverrait des centaines de
réponses vides.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import time

from ui.exemples_affichage import Couleurs


class Menus:
    def __init__(self, affichage, pause_erreur=2.0):
        """pause_erreur : temps d'attente (en secondes) après une mauvaise réponse.
        Sans elle, laisser la touche Entrée appuyée enverrait des centaines de réponses
        vides et le message d'erreur s'afficherait en boucle."""
        self.affichage = affichage
        self.pause_erreur = pause_erreur

    # --- Lecture du clavier (avec vérification) -----------------------------
    def _vider_le_clavier(self):
        """Jette les touches déjà tapées mais pas encore lues (Entrée maintenue, etc.)."""
        try:
            import msvcrt
        except ImportError:
            return

        while msvcrt.kbhit():
            msvcrt.getch()

    def _demander(self, question):
        """Pose la question et renvoie la réponse. Je vide d'abord le clavier : une
        seule pression sur Entrée = une seule réponse."""
        self._vider_le_clavier()

        return input(question + " ").strip()

    def _refuser(self, message):
        """Réponse invalide : j'affiche l'erreur, puis j'attends un peu avant de
        reposer la question (et les touches pressées pendant ce temps sont jetées)."""
        self.affichage.erreur(message)
        time.sleep(self.pause_erreur)

    def lire_entier(self, question, minimum, maximum):
        """Redemande tant que la réponse n'est pas un nombre entre minimum et maximum."""
        while True:
            reponse = self._demander(question)

            try:
                nombre = int(reponse)
            except ValueError:
                self._refuser("Entre un nombre.")
                continue

            if nombre < minimum or nombre > maximum:
                self._refuser("Le nombre doit être entre " + str(minimum)
                              + " et " + str(maximum) + ".")
                continue

            # Petit bruit à chaque choix (un autre pour « retour », qui est le 0).
            if nombre == 0:
                self.affichage.bruitage("retour")
            else:
                self.affichage.bruitage("clic")

            return nombre

    def lire_texte(self, question):
        while True:
            reponse = self._demander(question)

            if reponse != "" and len(reponse) <= 16:
                self.affichage.bruitage("clic")
                return reponse

            self._refuser("Un nom de 1 à 16 caractères, s'il te plaît.")

    def confirmer(self, question):
        """True pour « o » / « oui »."""
        while True:
            reponse = self._demander(question + " (o/n)").lower()

            if reponse in ["o", "oui"]:
                self.affichage.bruitage("clic")
                return True

            if reponse in ["n", "non"]:
                self.affichage.bruitage("retour")
                return False

            self._refuser("Réponds par o (oui) ou n (non).")

    def attendre_entree(self):
        self._demander("Appuie sur Entrée pour continuer...")
        self.affichage.bruitage("clic")

    # --- Menus généraux ------------------------------------------------------
    def choisir_option(self, titre, options):
        """Affiche des options numérotées. Renvoie la position choisie (à partir de 0)."""
        self.affichage.titre(titre)
        self.affichage.liste(options)

        return self.lire_entier("Ton choix ?", 1, len(options)) - 1

    def choisir_pokemon_du_catalogue(self, pokemons, deja_pris):
        """Renvoie le numéro (à partir de 0) d'un Pokémon pas encore dans l'équipe."""
        self.affichage.catalogue(pokemons, deja_pris)

        while True:
            numero = self.lire_entier("Quel Pokémon ?", 1, len(pokemons)) - 1

            if numero not in deja_pris:
                return numero

            self.affichage.erreur("Ce Pokémon est déjà dans ton équipe.")

    # --- Menus du combat -----------------------------------------------------
    def menu_principal(self, dresseur):
        """Renvoie 1 (attaquer), 2 (changer), 3 (inventaire), 4 (équipe) ou 5 (abandonner)."""
        print()
        question = ("C'est à " + dresseur.nom + " de jouer ! Que fait "
                    + dresseur.pokemon_actif().nom + " ?")
        print("  " + self.affichage.colorer(question, Couleurs.GRAS))
        self.affichage.liste(["Attaquer", "Changer de Pokémon", "Inventaire (potions, rappels...)",
                              "Voir mon équipe", "Abandonner"])

        return self.lire_entier("Ton choix ?", 1, 5)

    def choisir_attaque(self, pokemon):
        """Renvoie la position de l'attaque choisie, ou -1 pour « retour »."""
        print()
        print("  Quelle attaque pour " + pokemon.nom + " ?")
        self.affichage.liste_attaques(pokemon)
        self.affichage.retour()

        while True:
            choix = self.lire_entier("Ton choix ?", 0, len(pokemon.attaques))

            if choix == 0:
                return -1

            if pokemon.attaques[choix - 1].pp > 0:
                return choix - 1

            self.affichage.erreur(pokemon.attaques[choix - 1].nom + " n'a plus de PP !")

    def choisir_pokemon(self, equipe, question, retour_possible):
        """Renvoie la position du Pokémon choisi, ou -1 pour « retour »."""
        print()
        print("  " + question)
        self.affichage.liste_pokemon(equipe)

        minimum = 1
        if retour_possible:
            self.affichage.retour()
            minimum = 0

        choix = self.lire_entier("Ton choix ?", minimum, len(equipe.pokemons))

        return choix - 1

    def choisir_objet(self, dresseur):
        """Renvoie le nom de l'objet choisi, ou "" pour « retour »."""
        print()
        print("  Inventaire de " + dresseur.nom + " :")
        self.affichage.liste_objets(dresseur)
        self.affichage.retour()

        choix = self.lire_entier("Quel objet ?", 0, len(dresseur.sac.lignes))

        if choix == 0:
            return ""

        return dresseur.sac.lignes[choix - 1].objet.nom
