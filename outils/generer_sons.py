"""Fabrique les bruitages du jeu (fichiers .wav) avec Python seul. À lancer une fois :

    python -m outils.generer_sons

Comme pour ui/audio.py, c'est une partie où je me suis beaucoup fait aider par Claude (
IA) : je lui ai décrit les sons que je voulais et il m'a donné les notes et les fonctions pour
les fabriquer. Ce qu'il faut comprendre : un son est une suite de nombres entre -1 et 1
(22050 par seconde). Une note est un sinus (ou un carré) dont la fréquence glisse d'une valeur
à une autre ; un souffle est une suite de nombres au hasard. Je superpose ou j'enchaîne ces
sons, puis je les écris dans un fichier .wav avec le module wave.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import math
import os
import random
import struct
import wave


class Synthe:
    def __init__(self):
        self.taux = 22050

    def ton(self, f_debut, f_fin, duree, volume=0.5, carre=False):
        """Un son qui glisse de f_debut à f_fin (en Hz) et qui s'éteint peu à peu."""
        nombre = int(duree * self.taux)
        son = []
        phase = 0.0

        for i in range(nombre):
            avancement = i / nombre
            phase = phase + 2 * math.pi * (f_debut + (f_fin - f_debut) * avancement) / self.taux
            valeur = math.sin(phase)

            if carre and valeur >= 0:
                valeur = 1.0
            elif carre:
                valeur = -1.0

            son.append(valeur * volume * (1 - avancement))

        return son

    def bruit(self, duree, volume=0.5):
        """Un souffle qui s'éteint peu à peu."""
        nombre = int(duree * self.taux)
        son = []

        for i in range(nombre):
            son.append(random.uniform(-1, 1) * volume * (1 - i / nombre))

        return son

    def superposer(self, sons):
        """Les sons joués en même temps (on additionne)."""
        taille = 0
        for son in sons:
            if len(son) > taille:
                taille = len(son)

        total = [0.0] * taille

        for son in sons:
            for i in range(len(son)):
                total[i] = total[i] + son[i]

        return total

    def enchainer(self, sons):
        """Les sons joués l'un après l'autre."""
        total = []

        for son in sons:
            total = total + son

        return total

    def ecrire(self, chemin, son):
        """Écrit un fichier .wav (mono, 16 bits)."""
        os.makedirs(os.path.dirname(chemin), exist_ok=True)

        with wave.open(chemin, "w") as fichier:
            fichier.setnchannels(1)
            fichier.setsampwidth(2)
            fichier.setframerate(self.taux)

            for valeur in son:
                if valeur > 1:
                    valeur = 1
                if valeur < -1:
                    valeur = -1

                fichier.writeframes(struct.pack("<h", int(valeur * 30000)))


def note(numero_midi):
    """Fréquence d'une note (69 = La à 440 Hz ; +12 = une octave plus haut)."""
    return 440 * 2 ** ((numero_midi - 69) / 12)


def main():
    s = Synthe()
    random.seed(1)
    coup = s.superposer([s.ton(160, 50, 0.18, 0.7), s.bruit(0.06, 0.5)])

    sons = {
        # Les bruits de combat
        "attaque": s.superposer([s.bruit(0.15, 0.3), s.ton(900, 300, 0.15, 0.3, True)]),
        "degats": coup,
        "super_efficace": s.superposer([coup, s.ton(1000, 1800, 0.25, 0.3, True)]),
        "peu_efficace": s.ton(110, 70, 0.18, 0.4),
        "critique": s.enchainer([coup, s.superposer([coup, s.ton(1500, 2200, 0.2, 0.3, True)])]),
        "rate": s.bruit(0.25, 0.2),
        "ko": s.ton(600, 60, 0.7, 0.5, True),
        "soin": s.enchainer([s.ton(note(72), note(72), 0.1, 0.4),
                             s.ton(note(76), note(76), 0.1, 0.4),
                             s.ton(note(79), note(79), 0.2, 0.4)]),
        "stat_haut": s.ton(400, 1000, 0.3, 0.4, True),
        "stat_bas": s.ton(800, 200, 0.3, 0.4, True),
        "statut": s.enchainer([s.ton(300, 450, 0.1, 0.4), s.ton(450, 300, 0.1, 0.4),
                               s.ton(300, 450, 0.1, 0.4)]),
        "changement": s.enchainer([s.ton(note(67), note(67), 0.08, 0.4),
                                   s.ton(note(72), note(72), 0.12, 0.4)]),
        "victoire": s.enchainer([s.ton(note(60), note(60), 0.15, 0.5, True),
                                 s.ton(note(64), note(64), 0.15, 0.5, True),
                                 s.ton(note(67), note(67), 0.15, 0.5, True),
                                 s.ton(note(72), note(72), 0.6, 0.5, True)]),
        # Les bruits des menus : deux petites notes carrées, comme dans les jeux Pokémon.
        "clic": s.enchainer([s.ton(note(88), note(88), 0.04, 0.25, True),
                             s.ton(note(93), note(93), 0.07, 0.25, True)]),
        "retour": s.enchainer([s.ton(note(86), note(86), 0.04, 0.25, True),
                               s.ton(note(79), note(79), 0.07, 0.25, True)]),
    }

    dossier = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "audio", "sons")

    for nom in sons:
        s.ecrire(os.path.join(dossier, nom + ".wav"), sons[nom])


if __name__ == "__main__":
    main()
