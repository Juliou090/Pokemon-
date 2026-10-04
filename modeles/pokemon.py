"""Classe Pokemon : UN Pokémon précis (niveau, PV actuels, nature, IV, attaques...).

On a le droit ici : l'état d'un Pokémon et ce qu'il peut subir ou faire sur
lui-même (subir des dégâts, se soigner...).
On N'A PAS le droit : de décider de l'ordre des tours, de calculer les dégâts
d'une attaque (combat/), ni d'afficher (ui/).

Encapsulation : les PV sont PRIVÉS (_pv). On y accède par la propriété `pv`,
dont le « setter » vérifie que la valeur est cohérente.

Pour l'instant seuls la création, la lecture, les PV, les dégâts et les soins
sont écrits. Statuts, paliers de combat et objet tenu viendront plus tard.
"""

from exceptions import DonneesInvalidesError
from exceptions import PokemonKOError
from exceptions import PVInvalideError
from modeles.nature import Nature
from modeles.modificateurs import ModificateursStats
from modeles.statistiques import Statistiques


class Pokemon:
    """Un Pokémon.

    Attributs privés :
        _nom : nom de l'espèce (ex. "Dracaufeu")
        _types : liste de 1 ou 2 objets TypePokemon
        _stats_base : objet Statistiques (stats de base de l'espèce)
        _niveau : entier de 1 à 100
        _nature : objet Nature
        _iv : objet Statistiques (valeurs individuelles, de 0 à 31)
        _ev : objet Statistiques (points d'effort, 0 par défaut)
        _stats : objet Statistiques (stats finales calculées)
        _pv : PV actuels (PRIVÉ, entre 0 et _stats.pv)
        _attaques : liste de 1 à 4 objets Attaque
        _statut : objet StatutMajeur, ou None s'il n'y en a pas
        _modificateurs : objet ModificateursStats
        _objet_tenu : objet Tenu, ou None
    """

    # Attributs de classe (communs à tous les Pokémon, ce ne sont pas des globales).
    NIVEAU_MIN = 1
    NIVEAU_MAX = 100
    NOMBRE_ATTAQUES_MAX = 4

    def __init__(self, nom, types, stats_base, niveau, attaques,
                 nature=None, iv=None, ev=None, objet_tenu=None):
        """Crée un Pokémon et calcule ses stats finales.

        nature : si None, nature neutre.
        iv : si None, IV tirés au hasard entre 0 et 31.
        ev : si None, EV tous à 0.
        """
        self._verifier_les_donnees(types, niveau, attaques)

        self._nom = nom
        self._types = types
        self._stats_base = stats_base
        self._niveau = niveau
        self._attaques = attaques
        self._objet_tenu = objet_tenu
        self._statut = None
        self._modificateurs = ModificateursStats()

        # Valeurs par défaut : on les crée ici, pour avoir des objets neufs.
        if nature is None:
            self._nature = Nature.neutre()
        else:
            self._nature = nature

        if iv is None:
            self._iv = Statistiques.aleatoires()
        else:
            self._iv = iv

        if ev is None:
            self._ev = Statistiques.zeros()
        else:
            self._ev = ev

        self._stats = Statistiques.calculer(
            self._stats_base, self._iv, self._ev, self._niveau, self._nature)

        # Un Pokémon neuf démarre avec tous ses PV.
        self._pv = self._stats.pv

    def _verifier_les_donnees(self, types, niveau, attaques):
        """Lève DonneesInvalidesError si le Pokémon demandé est impossible."""
        if len(types) < 1 or len(types) > 2:
            raise DonneesInvalidesError("Un Pokémon a un ou deux types.")

        if niveau < Pokemon.NIVEAU_MIN or niveau > Pokemon.NIVEAU_MAX:
            raise DonneesInvalidesError("Le niveau doit être entre 1 et 100.")

        if len(attaques) < 1 or len(attaques) > Pokemon.NOMBRE_ATTAQUES_MAX:
            raise DonneesInvalidesError("Un Pokémon a de 1 à 4 attaques.")

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------
    @property
    def nom(self):
        """Nom de l'espèce."""
        return self._nom

    @property
    def types(self):
        """Liste des types du Pokémon (1 ou 2 objets TypePokemon)."""
        return self._types

    @property
    def niveau(self):
        """Niveau du Pokémon."""
        return self._niveau

    @property
    def nature(self):
        """Nature du Pokémon."""
        return self._nature

    @property
    def stats(self):
        """Stats finales (objet Statistiques)."""
        return self._stats

    @property
    def attaques(self):
        """Liste des attaques du Pokémon."""
        return self._attaques

    @property
    def statut(self):
        """Statut majeur actuel, ou None."""
        return self._statut

    @property
    def modificateurs(self):
        """Paliers temporaires de stats (objet ModificateursStats)."""
        return self._modificateurs

    @property
    def objet_tenu(self):
        """Objet tenu, ou None."""
        return self._objet_tenu

    @property
    def pv_max(self):
        """PV maximum."""
        return self._stats.pv

    @property
    def est_ko(self):
        """True si le Pokémon n'a plus de PV."""
        return self._pv == 0

    # ------------------------------------------------------------------
    # Les PV (encapsulation)
    # ------------------------------------------------------------------
    @property
    def pv(self):
        """PV actuels (lecture)."""
        return self._pv

    @pv.setter
    def pv(self, nouvelle_valeur):
        """Affecte les PV. Lève PVInvalideError si la valeur est incohérente."""
        if not isinstance(nouvelle_valeur, int):
            raise PVInvalideError("Les PV doivent être un nombre entier.")

        if nouvelle_valeur < 0:
            raise PVInvalideError("Les PV ne peuvent pas être négatifs.")

        if nouvelle_valeur > self.pv_max:
            raise PVInvalideError("Les PV ne peuvent pas dépasser le maximum.")

        self._pv = nouvelle_valeur

    # ------------------------------------------------------------------
    # Actions sur soi
    # ------------------------------------------------------------------
    def verifier_peut_agir(self):
        """Lève PokemonKOError si le Pokémon est K.O."""
        if self.est_ko:
            raise PokemonKOError(self._nom + " est K.O. et ne peut pas agir.")

    def subir_degats(self, degats):
        """Retire des PV (sans descendre sous 0) et renvoie les dégâts réels."""
        if degats < 0:
            raise PVInvalideError("Des dégâts ne peuvent pas être négatifs.")

        pv_avant = self._pv

        # Le Pokémon ne peut pas perdre plus de PV qu'il n'en a.
        if degats >= pv_avant:
            self._pv = 0
        else:
            self._pv = pv_avant - degats

        degats_reels = pv_avant - self._pv

        return degats_reels

    def soigner(self, quantite):
        """Rend des PV (sans dépasser le maximum) et renvoie les PV rendus.

        Lève PokemonKOError si le Pokémon est K.O. : seul un objet de rappel
        peut ranimer un Pokémon K.O.
        """
        self.verifier_peut_agir()

        if quantite < 0:
            raise PVInvalideError("Un soin ne peut pas être négatif.")

        pv_avant = self._pv
        pv_apres = pv_avant + quantite

        # On plafonne au maximum.
        if pv_apres > self.pv_max:
            pv_apres = self.pv_max

        self._pv = pv_apres
        pv_rendus = pv_apres - pv_avant

        return pv_rendus

    # ------------------------------------------------------------------
    # À écrire plus tard (logique de combat)
    # ------------------------------------------------------------------
    def stat_effective(self, nom_stat):
        """Stat finale x palier x statut x objet tenu (pour les dégâts)."""
        raise NotImplementedError

    def ranimer(self, fraction):
        """Remet un K.O. en vie avec une fraction de ses PV max (objet Rappel)."""
        raise NotImplementedError

    def appliquer_statut(self, statut):
        """Donne un statut si le Pokémon n'en a pas déjà."""
        raise NotImplementedError

    def guerir_statut(self):
        """Retire le statut majeur."""
        raise NotImplementedError

    def soigner_completement(self):
        """PV max, PP max, plus de statut, paliers à 0 (fin de combat)."""
        raise NotImplementedError

    def a_la_sortie_du_terrain(self):
        """Remet les paliers à 0 quand on change de Pokémon."""
        raise NotImplementedError

    def __str__(self):
        """Texte affiché quand on fait print(pokemon)."""
        return f"{self._nom} (niv. {self._niveau})"
