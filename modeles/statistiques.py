"""Les statistiques d'un Pokémon et sa nature (formules de la génération 3, Poképédia).

J'utilise la même classe Statistiques pour les stats de base, les IV, les EV et les stats
finales : c'est toujours un paquet de 6 nombres. Je calcule avec des nombres entiers (//) pour
retrouver exactement les valeurs du jeu, sans erreur d'arrondi.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""


class Statistiques:
    """Six valeurs. Je m'en sers pour les stats de base, les IV, les EV et les
    stats finales : c'est toujours le même paquet de 6 nombres."""

    # Les 5 stats qui peuvent monter ou baisser en combat (les PV sont à part).
    NOMS_DE_COMBAT = ["attaque", "defense", "attaque_speciale", "defense_speciale", "vitesse"]

    # Pour les messages : « L'Attaque Spéciale de X monte ! ».
    NOMS_FRANCAIS = {
        "attaque": "L'Attaque",
        "defense": "La Défense",
        "attaque_speciale": "L'Attaque Spéciale",
        "defense_speciale": "La Défense Spéciale",
        "vitesse": "La Vitesse",
    }

    def __init__(self, pv, attaque=None, defense=None, attaque_speciale=None,
                 defense_speciale=None, vitesse=None):
        """Statistiques(78, 84, 78, 109, 85, 100) : les six valeurs.
        Statistiques(31) : raccourci, les six valeurs sont égales à 31 (pratique
        pour des IV tous à 31 ou des EV tous à 0)."""
        if attaque is None:
            attaque = pv
            defense = pv
            attaque_speciale = pv
            defense_speciale = pv
            vitesse = pv

        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.attaque_speciale = attaque_speciale
        self.defense_speciale = defense_speciale
        self.vitesse = vitesse

    def valeur(self, nom_stat):
        """valeur("vitesse") donne self.vitesse (getattr = lire un attribut dont le
        nom est dans une variable)."""
        return getattr(self, nom_stat)

    def calculer(self, iv, ev, niveau, nature):
        """Calcule les stats FINALES d'un Pokémon. `self` = ses stats de base.

        PV      = ((2*B + IV + EV//4) * N // 100) + N + 10
        autres  = (((2*B + IV + EV//4) * N // 100) + 5) * nature
        Je travaille en entiers (// et pourcentage 90/100/110) pour retomber
        exactement sur les valeurs du jeu, sans erreur d'arrondi.
        """
        stats = Statistiques(0)
        stats.pv = (2 * self.pv + iv.pv + ev.pv // 4) * niveau // 100 + niveau + 10

        for nom in Statistiques.NOMS_DE_COMBAT:
            somme = 2 * self.valeur(nom) + iv.valeur(nom) + ev.valeur(nom) // 4
            valeur = somme * niveau // 100 + 5
            setattr(stats, nom, valeur * nature.pourcentage(nom) // 100)

        return stats


class Nature:
    """+10 % sur une stat, -10 % sur une autre (ou neutre : None, None)."""

    def __init__(self, nom, stat_plus, stat_moins):
        self.nom = nom
        self.stat_plus = stat_plus
        self.stat_moins = stat_moins

    def pourcentage(self, nom_stat):
        """110, 90 ou 100."""
        if nom_stat == self.stat_plus:
            return 110

        if nom_stat == self.stat_moins:
            return 90

        return 100
