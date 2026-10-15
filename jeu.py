"""Le chef d'orchestre : accueil -> création des deux équipes -> combat -> fin.

Jeu ne calcule rien lui-même : je lui fais seulement enchaîner les étapes et déléguer à
CreationEquipe (les équipes), Combat (la partie) et Affichage (l'écran). C'est aussi ici que
je règle la vitesse d'écriture du texte et que je lance la musique.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

from combat.combat import Combat
from modes.creation_equipe import CreationEquipe
from ui.affichage import Affichage
from ui.audio import Audio
from ui.menus import Menus


class Jeu:
    def __init__(self):
        self.audio = Audio()
        # delai_lettre : vitesse d'écriture du texte (0 = d'un coup, 0.05 = lent).
        self.affichage = Affichage(audio=self.audio, delai_lettre=0.02)
        self.menus = Menus(self.affichage)
        self.creation = CreationEquipe(self.menus)

    def lancer(self):
        """Écran titre, puis une partie, puis on propose de rejouer."""
        self.affichage.ecran_titre()
        self.audio.musique("menu")

        if self.audio.message != "":
            self.affichage.info(self.audio.message)

        try:
            rejouer = True

            while rejouer:
                joueur1 = self._creer_joueur(1)
                self.menus.attendre_entree()
                joueur2 = self._creer_joueur(2)
                self.menus.attendre_entree()

                self._jouer(joueur1, joueur2)

                rejouer = self.menus.confirmer("Faire une nouvelle partie ?")
        except KeyboardInterrupt:
            # Ctrl+C : on quitte proprement au lieu d'afficher une erreur.
            self.affichage.info("")

        self.audio.fermer()
        self.affichage.info("Merci d'avoir joué, à bientôt !")

    def _creer_joueur(self, numero):
        """Demande le nom et le mode de création d'équipe, puis construit le Dresseur."""
        self.affichage.titre("Joueur " + str(numero))
        nom = self.menus.lire_texte("Nom du joueur " + str(numero) + " ?")

        options = []
        for position in range(len(CreationEquipe.NOMS_DES_MODES)):
            options.append(CreationEquipe.NOMS_DES_MODES[position] + " — "
                           + CreationEquipe.DESCRIPTIONS[position])

        mode = self.menus.choisir_option(nom + ", choisis ton mode de jeu", options)

        dresseur = self.creation.creer_dresseur(nom, mode)
        self.affichage.fiche_equipe(dresseur)

        return dresseur

    def _jouer(self, dresseur1, dresseur2):
        """Lance le combat, annonce le résultat, puis soigne les Pokémon."""
        self.affichage.effacer_ecran()
        self.affichage.titre("Que le combat commence !")
        self.audio.musique("combat")

        vainqueur = Combat(dresseur1, dresseur2, self.affichage, self.menus).lancer()

        # Fanfare de victoire, puis retour à la musique du menu.
        self.audio.bruitage("victoire")
        self.audio.musique("menu")

        perdant = dresseur1
        if vainqueur is dresseur1:
            perdant = dresseur2

        self.affichage.victoire(vainqueur, perdant)

        # Fin de combat : on soigne tout le monde.
        dresseur1.equipe.soigner_tous()
        dresseur2.equipe.soigner_tous()
