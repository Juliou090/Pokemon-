"""Un Pokémon précis : niveau, PV, nature, IV, attaques, statut...

Encapsulation : les PV sont privés (_pv). On les lit avec get_pv() et on les
change avec set_pv(), qui vérifie que la valeur est cohérente. Les autres
informations (nom, types...) ne risquent rien : je les laisse publiques pour
ne pas écrire des dizaines de méthodes inutiles.
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

from exceptions import (
    ActionInvalideError,
    DonneesInvalidesError,
    PVInvalideError,
    PokemonKOError,
)
from modeles.statistiques import Nature, Statistiques


class Pokemon:
    def __init__(self, nom, types, stats_base, niveau, attaques,
                 nature=None, iv=None, objet_tenu=None):
        """nature=None : nature neutre. iv=None : IV tirés au hasard (0 à 31)."""
        if len(types) < 1 or len(types) > 2:
            raise DonneesInvalidesError("Un Pokémon a un ou deux types.")

        if niveau < 1 or niveau > 100:
            raise DonneesInvalidesError("Le niveau doit être entre 1 et 100.")

        if len(attaques) < 1 or len(attaques) > 4:
            raise DonneesInvalidesError("Un Pokémon a de 1 à 4 attaques.")

        self.nom = nom
        self.types = types
        self.stats_base = stats_base
        self.niveau = niveau
        self.attaques = attaques
        self.objet_tenu = objet_tenu
        self.statut = None

        if nature is None:
            nature = Nature("Sérieux", None, None)

        if iv is None:
            iv = Statistiques.aleatoires()

        self.nature = nature
        self.iv = iv
        self.stats = Statistiques.calculer(stats_base, iv, Statistiques.identiques(0),
                                           niveau, nature)
        self.pv_max = self.stats.pv

        # Les paliers de stats de combat (de -6 à +6), remis à 0 quand on sort.
        self.paliers = {}
        for nom_stat in Statistiques.NOMS_DE_COMBAT:
            self.paliers[nom_stat] = 0

        self._pv = self.pv_max

    # --- Les PV (privés) ---------------------------------------------------
    def get_pv(self):
        return self._pv

    def set_pv(self, valeur):
        """Refuse les PV négatifs ou au-dessus du maximum (PVInvalideError)."""
        if valeur < 0:
            raise PVInvalideError("Les PV ne peuvent pas être négatifs.")

        if valeur > self.pv_max:
            raise PVInvalideError("Les PV ne peuvent pas dépasser le maximum.")

        self._pv = valeur

    def est_ko(self):
        return self._pv == 0

    def a_encore_des_pp(self):
        """True si au moins une attaque a encore des PP."""
        for attaque in self.attaques:
            if attaque.pp > 0:
                return True

        return False

    def pourcentage_pv(self):
        return self._pv * 100 // self.pv_max

    def verifier_peut_agir(self):
        """Lève PokemonKOError si le Pokémon est K.O."""
        if self.est_ko():
            raise PokemonKOError(self.nom + " est K.O. et ne peut pas agir.")

    # --- Dégâts, soins ----------------------------------------------------
    def subir_degats(self, degats):
        """Retire des PV (jamais sous 0) et renvoie les dégâts réellement subis."""
        reels = degats

        if reels > self._pv:
            reels = self._pv

        self._pv = self._pv - reels

        return reels

    def soigner(self, quantite):
        """Rend des PV (jamais au-delà du max). Lève PokemonKOError si K.O."""
        self.verifier_peut_agir()

        rendus = quantite

        if rendus > self.pv_max - self._pv:
            rendus = self.pv_max - self._pv

        self._pv = self._pv + rendus

        return rendus

    def ranimer(self, pourcentage):
        """Remet un K.O. en vie avec un pourcentage de ses PV max."""
        if not self.est_ko():
            raise ActionInvalideError(self.nom + " n'est pas K.O.")

        self._pv = self.pv_max * pourcentage // 100

        if self._pv < 1:
            self._pv = 1

        return self._pv

    def soigner_completement(self):
        """Fin de combat : PV, PP, statut et paliers remis à neuf."""
        self._pv = self.pv_max
        self.statut = None

        for nom_stat in self.paliers:
            self.paliers[nom_stat] = 0

        for attaque in self.attaques:
            attaque.pp = attaque.pp_max

    # --- Statut, types, stats ---------------------------------------------
    def a_le_type(self, nom_type):
        for type_pokemon in self.types:
            if type_pokemon.nom == nom_type:
                return True

        return False

    def appliquer_statut(self, statut):
        """True si le statut a été donné (refusé : K.O., déjà un statut, immunité)."""
        if self.est_ko() or self.statut is not None or statut.immunise(self):
            return False

        self.statut = statut
        return True

    def modifier_palier(self, nom_stat, variation):
        """Change un palier (borné à -6/+6). Renvoie le changement réel."""
        ancien = self.paliers[nom_stat]
        nouveau = ancien + variation

        if nouveau > 6:
            nouveau = 6

        if nouveau < -6:
            nouveau = -6

        self.paliers[nom_stat] = nouveau

        return nouveau - ancien

    def stat_effective(self, nom_stat, ignorer_baisses=False, ignorer_hausses=False):
        """La stat utilisée en combat : stat finale x palier x statut x objet tenu.

        Sur un coup critique, la génération 3 ignore les baisses de l'attaquant
        et les hausses du défenseur : d'où les deux options.
        """
        valeur = self.stats.valeur(nom_stat)
        palier = self.paliers[nom_stat]

        if ignorer_baisses and palier < 0:
            palier = 0

        if ignorer_hausses and palier > 0:
            palier = 0

        if palier >= 0:
            valeur = valeur * (2 + palier) // 2
        else:
            valeur = valeur * 2 // (2 - palier)

        if self.statut is not None:
            valeur = valeur * self.statut.pourcentage_stat(nom_stat) // 100

        if self.objet_tenu is not None:
            valeur = valeur * self.objet_tenu.pourcentage_stat(nom_stat) // 100

        if valeur < 1:
            valeur = 1

        return valeur
