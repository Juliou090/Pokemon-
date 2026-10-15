"""Le son du jeu : la musique de fond et les bruitages.

Cette partie est celle où je me suis le plus fait aider : je l'ai demandée directement à
Claude (une IA), parce que je n'avais aucune idée de comment gérer les sons. J'avais déjà
touché un peu au son dans mon ancien projet, mais là je voulais en savoir plus, donc j'ai
expérimenté. J'ai décrit les sons que je voulais, et Claude m'a donné les notes à utiliser et
les fonctions pour les fabriquer et les jouer. Je l'ai testé et relu, mais c'est la partie la
plus technique du projet : si elle n'intéresse pas, elle peut être ignorée, le jeu marche
sans son.

Ce que ça fait : pygame.mixer lit les MP3 et les WAV, règle le volume et fait les fondus. Il
faut l'installer une fois (pip install pygame, ou pygame-ce avec Python 3.14). S'il n'est pas
installé, ou s'il n'y a pas de carte son, le jeu écrit un message au lancement et se joue
en silence.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import os
import time


class Audio:
    # Mes musiques : fichiers du dossier audio/ (.mp3 ou .wav), sans l'extension.
    FICHIERS_MUSIQUE = {"menu": "audio/Pokemon", "combat": "audio/P2"}

    # D'où viennent les musiques (pour les crédits, le programme ne s'en sert pas).
    LIENS_MUSIQUE = {"menu": "", "combat": ""}

    VOLUME_NORMAL = 0.01    # de 0 à 1
    VOLUME_DISCRET = 0.2    # pendant le déroulement d'un tour, pour entendre les bruitages

    def __init__(self, actif=True):
        """actif=False : jeu muet (tests). On peut aussi couper avec JEU_SANS_SON=1."""
        self.actif = False
        self.message = ""            # pourquoi il n'y a pas de son (affiché au lancement)
        self.musique_en_cours = ""
        self.dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bruitages = {}          # les sons déjà chargés, pour ne pas les relire

        if not actif or os.environ.get("JEU_SANS_SON") == "1":
            return

        try:
            os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
            import pygame
            pygame.mixer.init()
            self.pygame = pygame
            self.actif = True
        except ImportError:
            self.message = ("Pas de son : pour l'entendre, il faut installer pygame "
                            "(pip install pygame). Le jeu marche très bien sans.")
        except Exception:
            self.message = "Pas de son : aucune sortie audio détectée. Le jeu marche sans."

    # --- La musique -----------------------------------------------------------
    def _regler_volume(self, volume, duree):
        """Change le volume en douceur, en `duree` secondes."""
        depart = self.pygame.mixer.music.get_volume()

        for etape in range(1, 6):
            self.pygame.mixer.music.set_volume(depart + (volume - depart) * etape / 5)
            time.sleep(duree / 5)

    def musique(self, nom):
        """Passe à la musique "menu" ou "combat" : l'ancienne baisse, la nouvelle monte."""
        if not self.actif or nom == self.musique_en_cours:
            return

        base = os.path.join(self.dossier, Audio.FICHIERS_MUSIQUE[nom])

        for extension in [".mp3", ".wav"]:
            if os.path.exists(base + extension):
                if self.musique_en_cours != "":
                    self._regler_volume(0, 0.4)

                self.pygame.mixer.music.load(base + extension)
                self.pygame.mixer.music.set_volume(0)
                self.pygame.mixer.music.play(-1)       # -1 : en boucle
                self._regler_volume(Audio.VOLUME_NORMAL, 1.0)
                self.musique_en_cours = nom
                return

    def discrete(self):
        if self.musique_en_cours != "":
            self._regler_volume(Audio.VOLUME_DISCRET, 0.15)

    def normale(self):
        if self.musique_en_cours != "":
            self._regler_volume(Audio.VOLUME_NORMAL, 0.3)

    def fermer(self):
        """Arrête la musique (à la fin du jeu)."""
        if self.actif:
            self.pygame.mixer.quit()
            self.actif = False

    # --- Les bruitages --------------------------------------------------------
    def bruitage(self, nom):
        """Joue audio/sons/<nom>.wav (sans bloquer le jeu, par-dessus la musique)."""
        chemin = os.path.join(self.dossier, "audio", "sons", nom + ".wav")

        if not self.actif or not os.path.exists(chemin):
            return

        if nom not in self.bruitages:
            self.bruitages[nom] = self.pygame.mixer.Sound(chemin)

        self.bruitages[nom].play()

    def nom_du_bruitage(self, texte):
        """Le bruitage qui correspond à une phrase du combat ("" = aucun)."""
        if "Coup critique" in texte:
            return "critique"

        if "super efficace" in texte:
            return "super_efficace"

        if "pas très efficace" in texte:
            return "peu_efficace"

        if "K.O." in texte:
            return "ko"

        if "rate" in texte or "échoue" in texte or "n'affecte pas" in texte:
            return "rate"

        if " perd " in texte and "PV" in texte:
            return "degats"

        if "récupère" in texte or "ranimé" in texte:
            return "soin"

        if "monte" in texte:
            return "stat_haut"

        if "baisse" in texte:
            return "stat_bas"

        for mot in ["empoisonné", "paralysé", "brûlé", "endormi", "gelé"]:
            if " est " + mot in texte:
                return "statut"

        if " utilise " in texte and "[" in texte:
            return "attaque"

        if "envoie" in texte or "rappelle" in texte:
            return "changement"

        return ""

    def bruitage_pour(self, texte):
        """Joue le bruitage qui correspond à une phrase du combat."""
        nom = self.nom_du_bruitage(texte)

        if nom != "":
            self.bruitage(nom)
