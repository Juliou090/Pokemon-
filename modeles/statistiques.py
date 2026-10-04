"""Classe Statistiques : un « paquet » de 6 valeurs nommées.

Les 6 valeurs sont : PV, Attaque, Défense, Attaque Spéciale, Défense Spéciale
et Vitesse. La même classe sert pour les stats de base, les IV, les EV et
les stats finales d'un Pokémon.

On a le droit ici : stocker les 6 valeurs et fournir la formule officielle de
calcul des stats (source : https://www.pokepedia.fr/Statistique).
On N'A PAS le droit : de connaître un Pokémon précis ni de faire du combat.
"""

import random


class Statistiques:
    """Six valeurs numériques.

    Attributs publics (ce sont de simples données, sans règle à contrôler) :
        pv, attaque, defense, attaque_speciale, defense_speciale, vitesse
    """

    def __init__(self, pv, attaque, defense, attaque_speciale,
                 defense_speciale, vitesse):
        """Crée un paquet de 6 statistiques."""
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.attaque_speciale = attaque_speciale
        self.defense_speciale = defense_speciale
        self.vitesse = vitesse

    def valeur(self, nom_stat):
        """Renvoie la valeur d'une stat à partir de son nom (ex. "vitesse")."""
        if nom_stat == "pv":
            return self.pv

        if nom_stat == "attaque":
            return self.attaque

        if nom_stat == "defense":
            return self.defense

        if nom_stat == "attaque_speciale":
            return self.attaque_speciale

        if nom_stat == "defense_speciale":
            return self.defense_speciale

        if nom_stat == "vitesse":
            return self.vitesse

        raise ValueError("Statistique inconnue : " + str(nom_stat))

    @staticmethod
    def zeros():
        """Renvoie des statistiques toutes à 0 (utile pour les EV par défaut)."""
        return Statistiques(0, 0, 0, 0, 0, 0)

    @staticmethod
    def aleatoires():
        """Renvoie des IV tirés au hasard : chaque valeur est entre 0 et 31."""
        pv = random.randint(0, 31)
        attaque = random.randint(0, 31)
        defense = random.randint(0, 31)
        attaque_speciale = random.randint(0, 31)
        defense_speciale = random.randint(0, 31)
        vitesse = random.randint(0, 31)

        return Statistiques(pv, attaque, defense, attaque_speciale,
                            defense_speciale, vitesse)

    @staticmethod
    def identiques(valeur):
        """Renvoie des statistiques où les 6 valeurs sont égales (ex. IV tous à 31)."""
        return Statistiques(valeur, valeur, valeur, valeur, valeur, valeur)

    @staticmethod
    def calculer(base, iv, ev, niveau, nature):
        """Calcule les stats finales d'un Pokémon (formule de la génération 3).

        base, iv, ev : des objets Statistiques.
        niveau : entier de 1 à 100.
        nature : un objet Nature.
        """
        pv_final = Statistiques._calculer_pv(base.pv, iv.pv, ev.pv, niveau)

        attaque_finale = Statistiques._calculer_autre_stat(
            base.attaque, iv.attaque, ev.attaque, niveau,
            nature.pourcentage("attaque"))

        defense_finale = Statistiques._calculer_autre_stat(
            base.defense, iv.defense, ev.defense, niveau,
            nature.pourcentage("defense"))

        attaque_speciale_finale = Statistiques._calculer_autre_stat(
            base.attaque_speciale, iv.attaque_speciale, ev.attaque_speciale,
            niveau, nature.pourcentage("attaque_speciale"))

        defense_speciale_finale = Statistiques._calculer_autre_stat(
            base.defense_speciale, iv.defense_speciale, ev.defense_speciale,
            niveau, nature.pourcentage("defense_speciale"))

        vitesse_finale = Statistiques._calculer_autre_stat(
            base.vitesse, iv.vitesse, ev.vitesse, niveau,
            nature.pourcentage("vitesse"))

        return Statistiques(pv_final, attaque_finale, defense_finale,
                            attaque_speciale_finale, defense_speciale_finale,
                            vitesse_finale)

    @staticmethod
    def _calculer_pv(base, iv, ev, niveau):
        """PV = ((2*B + IV + EV//4) * N // 100) + N + 10."""
        # EV // 4 : division entière (on garde la partie entière, comme le jeu).
        somme = 2 * base + iv + ev // 4
        pv = somme * niveau // 100 + niveau + 10

        return pv

    @staticmethod
    def _calculer_autre_stat(base, iv, ev, niveau, pourcentage_nature):
        """Autre stat = (((2*B + IV + EV//4) * N // 100) + 5) * nature.

        pourcentage_nature vaut 110, 100 ou 90. On travaille avec des entiers
        (et non 1.1 ou 0.9) pour éviter les erreurs d'arrondi des décimaux.
        """
        somme = 2 * base + iv + ev // 4
        valeur_sans_nature = somme * niveau // 100 + 5
        valeur_finale = valeur_sans_nature * pourcentage_nature // 100

        return valeur_finale

    def __str__(self):
        """Texte affiché quand on fait print(statistiques)."""
        return (f"PV {self.pv} / Att {self.attaque} / Déf {self.defense} / "
                f"AttSpé {self.attaque_speciale} / "
                f"DéfSpé {self.defense_speciale} / Vit {self.vitesse}")
