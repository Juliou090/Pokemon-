"""Les menus : ils posent une question au joueur et renvoient sa réponse.
Un menu ne décide de rien : c'est le combat (ou le jeu) qui décide de la suite.
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

from ui.exemples_affichage import Couleurs


class Menus:
    def __init__(self, affichage):
        self.affichage = affichage

    # --- Lecture du clavier (avec vérification) -----------------------------
    def lire_entier(self, question, minimum, maximum):
        """Redemande tant que la réponse n'est pas un nombre entre minimum et maximum."""
        while True:
            reponse = input(question + " ").strip()

            try:
                nombre = int(reponse)
            except ValueError:
                self.affichage.erreur("Entre un nombre.")
                continue

            if nombre < minimum or nombre > maximum:
                self.affichage.erreur("Le nombre doit être entre " + str(minimum)
                                      + " et " + str(maximum) + ".")
                continue

            return nombre

    def lire_texte(self, question):
        while True:
            reponse = input(question + " ").strip()

            if reponse != "" and len(reponse) <= 16:
                return reponse

            self.affichage.erreur("Un nom de 1 à 16 caractères, s'il te plaît.")

    def confirmer(self, question):
        """True pour « o » / « oui »."""
        while True:
            reponse = input(question + " (o/n) ").strip().lower()

            if reponse in ["o", "oui"]:
                return True

            if reponse in ["n", "non"]:
                return False

    def attendre_entree(self):
        input("Appuie sur Entrée pour continuer... ")

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
        print("  " + self.affichage.col(question, Couleurs.GRAS))
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
