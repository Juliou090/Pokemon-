"""Une attaque, et ses effets (statut ou modification de stat).
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

import random

from exceptions import ActionInvalideError
from modeles.statistiques import Statistiques
from modeles.statuts import creer_statut


class EffetStatut:
    """L'attaque peut infliger un statut (ex. 10 % de brûlure)."""

    def __init__(self, identifiant_statut, chance):
        self.identifiant_statut = identifiant_statut
        self.chance = chance

    def appliquer(self, lanceur, cible):
        """Renvoie la phrase à afficher, ou "" s'il ne s'est rien passé."""
        if cible.est_ko():
            return ""

        if random.randint(1, 100) > self.chance:
            return ""

        statut = creer_statut(self.identifiant_statut)

        if cible.appliquer_statut(statut):
            return cible.nom + " est " + statut.nom + " !"

        return ""


class EffetStat:
    """L'attaque monte ou baisse une stat (palier de -6 à +6)."""

    def __init__(self, nom_stat, paliers, sur_soi, chance=100):
        self.nom_stat = nom_stat
        self.paliers = paliers
        self.sur_soi = sur_soi
        self.chance = chance

    def appliquer(self, lanceur, cible):
        """Renvoie la phrase à afficher, ou "" s'il ne s'est rien passé."""
        if self.sur_soi:
            vise = lanceur
        else:
            vise = cible

        if vise.est_ko() or random.randint(1, 100) > self.chance:
            return ""

        changement = vise.modifier_palier(self.nom_stat, self.paliers)
        debut = Statistiques.NOMS_FRANCAIS[self.nom_stat] + " de " + vise.nom

        if changement == 0:
            # Un effet « de chance » reste silencieux s'il ne change rien.
            if self.chance < 100:
                return ""

            if self.paliers > 0:
                return debut + " ne peut plus monter !"

            return debut + " ne peut plus baisser !"

        if changement > 0:
            verbe = "monte"
        else:
            verbe = "baisse"

        if abs(changement) == 2:
            verbe = verbe + " beaucoup"
        elif abs(changement) >= 3:
            verbe = verbe + " énormément"

        return debut + " " + verbe + " !"


class Attaque:
    def __init__(self, nom, type_attaque, puissance, precision, pp_max,
                 priorite=0, effets=None, critique_eleve=False, lutte=False):
        """puissance = 0 : attaque de statut. precision = 0 : ne rate jamais.
        lutte = True : ignore les types et blesse le lanceur (attaque Lutte)."""
        self.nom = nom
        self.type = type_attaque
        self.puissance = puissance
        self.precision = precision
        self.pp_max = pp_max
        self.pp = pp_max
        self.priorite = priorite
        self.critique_eleve = critique_eleve
        self.lutte = lutte

        # Je crée la liste ici : mettre « effets=[] » dans la signature
        # partagerait la même liste entre toutes les attaques.
        if effets is None:
            self.effets = []
        else:
            self.effets = effets

    def est_speciale(self):
        return self.type.special

    def est_de_statut(self):
        return self.puissance == 0

    def utiliser_pp(self):
        """Retire 1 PP, ou lève ActionInvalideError s'il n'y en a plus."""
        if self.pp <= 0:
            raise ActionInvalideError(self.nom + " n'a plus de PP.")

        self.pp = self.pp - 1
