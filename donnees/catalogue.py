"""Toutes les données du jeu : types, attaques, Pokémon, natures, objets, équipes.
Si tu vois un @ que tu ne connais pas : tout est expliqué dans GUIDE_PYTHON.md.

Choix : pas de fichier JSON (consigne du prof) et pas de variable globale. Les
données sont de simples lignes « nom = Classe(...) » à l'intérieur de méthodes
de la classe Catalogue (ce sont des variables LOCALES, pas globales).

Pour ajouter un Pokémon : copier une ligne « xxx = Pokemon(...) » dans
_tous_les_pokemon() et l'ajouter à la liste renvoyée à la fin (dans l'ordre).
Pour ajouter une attaque : copier une ligne « xxx = Attaque(...) ».

Valeurs vérifiées pour la génération 3 sur PokéAPI (past_stats, past_values) et
Bulbapedia. Exemples : Raichu a 100 de Vitesse (110 depuis la génération 6) et
Lance-Flammes a 95 de puissance (90 aujourd'hui).
"""

import random

from modeles.attaque import Attaque, EffetStat, EffetStatut
from modeles.dresseur import Sac
from modeles.objets import Guerison, ObjetTenu, Rappel, Soin
from modeles.pokemon import Pokemon
from modeles.statistiques import Nature, Statistiques
from modeles.type_pokemon import TypePokemon


class Catalogue:
    NOMS_DES_EQUIPES = ["Trio de départ", "Tempête", "Muraille", "Poids lourds", "Mystères"]

    # ------------------------------------------------------------------
    # Les 14 types : (nom, spécial ?, super efficace contre, peu efficace, sans effet)
    # ------------------------------------------------------------------
    @staticmethod
    def types():
        normal = TypePokemon("Normal", False, [], ["Roche"], ["Spectre"])
        feu = TypePokemon("Feu", True, ["Plante", "Glace"], ["Feu", "Eau", "Roche"], [])
        eau = TypePokemon("Eau", True, ["Feu", "Sol", "Roche"], ["Eau", "Plante"], [])
        plante = TypePokemon("Plante", True, ["Eau", "Sol", "Roche"],
                             ["Feu", "Plante", "Poison", "Vol"], [])
        electrik = TypePokemon("Électrik", True, ["Eau", "Vol"], ["Électrik", "Plante"], ["Sol"])
        glace = TypePokemon("Glace", True, ["Plante", "Sol", "Vol"], ["Feu", "Eau", "Glace"], [])
        combat = TypePokemon("Combat", False, ["Normal", "Glace", "Roche", "Ténèbres"],
                             ["Poison", "Vol", "Psy"], ["Spectre"])
        poison = TypePokemon("Poison", False, ["Plante"], ["Poison", "Sol", "Roche", "Spectre"], [])
        sol = TypePokemon("Sol", False, ["Feu", "Électrik", "Poison", "Roche"], ["Plante"], ["Vol"])
        vol = TypePokemon("Vol", False, ["Plante", "Combat"], ["Électrik", "Roche"], [])
        psy = TypePokemon("Psy", True, ["Combat", "Poison"], ["Psy"], ["Ténèbres"])
        roche = TypePokemon("Roche", False, ["Feu", "Glace", "Vol"], ["Combat", "Sol"], [])
        tenebres = TypePokemon("Ténèbres", True, ["Psy", "Spectre"], ["Combat", "Ténèbres"], [])
        spectre = TypePokemon("Spectre", False, ["Psy", "Spectre"], ["Ténèbres"], ["Normal"])

        return [normal, feu, eau, plante, electrik, glace, combat, poison, sol, vol, psy,
                roche, tenebres, spectre]

    @staticmethod
    def type(nom):
        """Le type qui porte ce nom."""
        for type_pokemon in Catalogue.types():
            if type_pokemon.nom == nom:
                return type_pokemon

    # ------------------------------------------------------------------
    # Les Pokémon (et leurs attaques)
    # ------------------------------------------------------------------
    @staticmethod
    def _tous_les_pokemon(niveau, iv, nature):
        """Fabrique TOUS les Pokémon d'un coup (objets neufs à chaque appel).

        Attention : dans une même liste, plusieurs Pokémon peuvent partager le même
        objet Attaque (ex. « seisme »). C'est pour ça que Catalogue.pokemon() n'en
        renvoie qu'UN par appel : deux appels = deux jeux d'objets séparés.
        """
        # Les 14 types (chacun est récupéré par son nom).
        normal = Catalogue.type("Normal")
        feu = Catalogue.type("Feu")
        eau = Catalogue.type("Eau")
        plante = Catalogue.type("Plante")
        electrik = Catalogue.type("Électrik")
        glace = Catalogue.type("Glace")
        combat = Catalogue.type("Combat")
        poison = Catalogue.type("Poison")
        sol = Catalogue.type("Sol")
        vol = Catalogue.type("Vol")
        psy = Catalogue.type("Psy")
        roche = Catalogue.type("Roche")
        tenebres = Catalogue.type("Ténèbres")
        spectre = Catalogue.type("Spectre")

        # --- Attaques : Attaque(nom, type, puissance, précision, PP, ...) ---
        # puissance 0 = attaque de statut ; précision 0 = ne rate jamais.
        lance_flammes = Attaque("Lance-Flammes", feu, 95, 100, 15,
                                effets=[EffetStatut("brulure", 10)])
        poing_feu = Attaque("Poing Feu", feu, 75, 100, 15, effets=[EffetStatut("brulure", 10)])
        cru_aile = Attaque("Cru-Aile", vol, 60, 100, 35)
        aeropique = Attaque("Aéropique", vol, 60, 0, 20)
        tranche = Attaque("Tranche", normal, 70, 100, 20, critique_eleve=True)
        plaquage = Attaque("Plaquage", normal, 85, 100, 15, effets=[EffetStatut("paralysie", 30)])
        vive_attaque = Attaque("Vive-Attaque", normal, 40, 100, 30, priorite=1)
        vitesse_extreme = Attaque("Vitesse Extrême", normal, 80, 100, 5, priorite=2)
        grincement = Attaque("Grincement", normal, 0, 85, 40,
                             effets=[EffetStat("defense", -2, False)])
        mimi_queue = Attaque("Mimi-Queue", normal, 0, 100, 30,
                             effets=[EffetStat("defense", -1, False)])
        berceuse = Attaque("Berceuse", normal, 0, 55, 15, effets=[EffetStatut("sommeil", 100)])
        seisme = Attaque("Séisme", sol, 100, 100, 10)
        tranch_herbe = Attaque("Tranch'Herbe", plante, 55, 95, 25, critique_eleve=True)
        poudre_dodo = Attaque("Poudre Dodo", plante, 0, 75, 15,
                              effets=[EffetStatut("sommeil", 100)])
        bombe_beurk = Attaque("Bombe Beurk", poison, 90, 100, 10,
                              effets=[EffetStatut("poison", 30)])
        poudre_toxik = Attaque("Poudre Toxik", poison, 0, 75, 35,
                               effets=[EffetStatut("poison", 100)])
        tonnerre = Attaque("Tonnerre", electrik, 95, 100, 15,
                           effets=[EffetStatut("paralysie", 10)])
        cage_eclair = Attaque("Cage-Éclair", electrik, 0, 100, 20,
                              effets=[EffetStatut("paralysie", 100)])
        casse_brique = Attaque("Casse-Brique", combat, 75, 100, 15)
        coup_croix = Attaque("Coup Croix", combat, 100, 80, 5, critique_eleve=True)
        gonflette = Attaque("Gonflette", combat, 0, 0, 20,
                            effets=[EffetStat("attaque", 1, True), EffetStat("defense", 1, True)])
        surf = Attaque("Surf", eau, 95, 100, 15)
        laser_glace = Attaque("Laser Glace", glace, 95, 100, 10, effets=[EffetStatut("gel", 10)])
        poing_glace = Attaque("Poing Glace", glace, 75, 100, 15, effets=[EffetStatut("gel", 10)])
        eboulement = Attaque("Éboulement", roche, 75, 90, 10)
        psyko = Attaque("Psyko", psy, 90, 100, 10,
                        effets=[EffetStat("defense_speciale", -1, False, 10)])
        hypnose = Attaque("Hypnose", psy, 0, 60, 20, effets=[EffetStatut("sommeil", 100)])
        plenitude = Attaque("Plénitude", psy, 0, 0, 20,
                            effets=[EffetStat("attaque_speciale", 1, True),
                                    EffetStat("defense_speciale", 1, True)])
        amnesie = Attaque("Amnésie", psy, 0, 0, 20,
                          effets=[EffetStat("defense_speciale", 2, True)])
        ball_ombre = Attaque("Ball'Ombre", spectre, 80, 100, 15,
                             effets=[EffetStat("defense_speciale", -1, False, 20)])
        machouille = Attaque("Mâchouille", tenebres, 80, 100, 15,
                             effets=[EffetStat("defense", -1, False, 20)])
        feinte = Attaque("Feinte", tenebres, 60, 0, 20)

        # --- Pokémon : Pokemon(nom, types, stats de base, niveau, attaques, nature, iv) ---
        # Stats de base : Statistiques(PV, Attaque, Défense, Att. Spé., Déf. Spé., Vitesse).
        dracaufeu = Pokemon("Dracaufeu", [feu, vol], Statistiques(78, 84, 78, 109, 85, 100),
                            niveau, [lance_flammes, cru_aile, tranche, seisme], nature, iv)
        florizarre = Pokemon("Florizarre", [plante, poison],
                             Statistiques(80, 82, 83, 100, 100, 80), niveau,
                             [tranch_herbe, bombe_beurk, poudre_dodo, poudre_toxik], nature, iv)
        raichu = Pokemon("Raichu", [electrik], Statistiques(60, 90, 55, 90, 80, 100),
                         niveau, [tonnerre, cage_eclair, vive_attaque, casse_brique], nature, iv)
        laggron = Pokemon("Laggron", [eau, sol], Statistiques(100, 110, 90, 85, 90, 60),
                          niveau, [surf, seisme, laser_glace, eboulement], nature, iv)
        gardevoir = Pokemon("Gardevoir", [psy], Statistiques(68, 65, 65, 125, 115, 80),
                            niveau, [psyko, ball_ombre, hypnose, plenitude], nature, iv)
        tyranocif = Pokemon("Tyranocif", [roche, tenebres],
                            Statistiques(100, 134, 110, 95, 100, 61), niveau,
                            [machouille, eboulement, grincement, seisme], nature, iv)
        alakazam = Pokemon("Alakazam", [psy], Statistiques(55, 50, 45, 135, 85, 120),
                           niveau, [psyko, ball_ombre, plenitude, cage_eclair], nature, iv)
        ectoplasma = Pokemon("Ectoplasma", [spectre, poison],
                             Statistiques(60, 65, 60, 130, 75, 110), niveau,
                             [ball_ombre, bombe_beurk, hypnose, tonnerre], nature, iv)
        leviator = Pokemon("Léviator", [eau, vol], Statistiques(95, 125, 79, 60, 100, 81),
                           niveau, [surf, laser_glace, seisme, cage_eclair], nature, iv)
        arcanin = Pokemon("Arcanin", [feu], Statistiques(90, 110, 80, 100, 80, 95),
                          niveau, [lance_flammes, vitesse_extreme, plaquage, aeropique],
                          nature, iv)
        mackogneur = Pokemon("Mackogneur", [combat], Statistiques(90, 130, 80, 65, 85, 55),
                             niveau, [coup_croix, seisme, eboulement, gonflette], nature, iv)
        ronflex = Pokemon("Ronflex", [normal], Statistiques(160, 110, 65, 65, 110, 30),
                          niveau, [plaquage, seisme, amnesie, poing_glace], nature, iv)
        lokhlass = Pokemon("Lokhlass", [eau, glace], Statistiques(130, 85, 80, 85, 95, 60),
                           niveau, [surf, laser_glace, tonnerre, berceuse], nature, iv)
        grolem = Pokemon("Grolem", [roche, sol], Statistiques(80, 110, 130, 55, 65, 45),
                         niveau, [eboulement, seisme, poing_feu, plaquage], nature, iv)
        noctali = Pokemon("Noctali", [tenebres], Statistiques(95, 65, 110, 60, 130, 65),
                          niveau, [feinte, ball_ombre, grincement, mimi_queue], nature, iv)

        return [dracaufeu, florizarre, raichu, laggron, gardevoir, tyranocif, alakazam,
                ectoplasma, leviator, arcanin, mackogneur, ronflex, lokhlass, grolem, noctali]

    @staticmethod
    def nombre_de_pokemon():
        return len(Catalogue._tous_les_pokemon(50, None, None))

    @staticmethod
    def pokemon(numero, niveau=50, iv=None, nature=None):
        """Le Pokémon n°numero (0 = Dracaufeu, 1 = Florizarre...). Un objet NEUF à chaque appel."""
        return Catalogue._tous_les_pokemon(niveau, iv, nature)[numero]

    @staticmethod
    def attaque(nom):
        """Une attaque NEUVE à partir de son nom (cherchée parmi celles des Pokémon)."""
        for pokemon in Catalogue._tous_les_pokemon(50, None, None):
            for attaque in pokemon.attaques:
                if attaque.nom == nom:
                    return attaque

        return None

    @staticmethod
    def attaque_lutte():
        """Lutte : utilisée quand un Pokémon n'a plus aucun PP (50 de puissance, ignore
        les types, le lanceur perd 1/4 des dégâts qu'il inflige)."""
        return Attaque("Lutte", Catalogue.type("Normal"), 50, 0, 1, lutte=True)

    @staticmethod
    def numeros_de_l_equipe(indice):
        """Les numéros des Pokémon d'une équipe toute faite (voir NOMS_DES_EQUIPES)."""
        if indice == 0:
            return [1, 0, 3]

        if indice == 1:
            return [0, 2, 4]

        if indice == 2:
            return [3, 5, 1]

        if indice == 3:
            return [11, 10, 13]

        return [7, 14, 6]

    # ------------------------------------------------------------------
    # Natures, objets, sacs
    # ------------------------------------------------------------------
    @staticmethod
    def natures():
        """Les 25 natures (source : PokéAPI) : 5 neutres, puis +10 % / -10 %.
        Pour en ajouter une : Nature("Nom", stat_augmentée, stat_diminuée)."""
        att = "attaque"
        dfs = "defense"
        ats = "attaque_speciale"
        dfss = "defense_speciale"
        vit = "vitesse"

        return [
            Nature("Hardi", None, None), Nature("Docile", None, None),
            Nature("Pudique", None, None), Nature("Bizarre", None, None),
            Nature("Sérieux", None, None),
            Nature("Assuré", dfs, att), Nature("Modeste", ats, att),
            Nature("Calme", dfss, att), Nature("Timide", vit, att),
            Nature("Solo", att, dfs), Nature("Doux", ats, dfs),
            Nature("Gentil", dfss, dfs), Nature("Pressé", vit, dfs),
            Nature("Rigide", att, ats), Nature("Malin", dfs, ats),
            Nature("Prudent", dfss, ats), Nature("Jovial", vit, ats),
            Nature("Mauvais", att, dfss), Nature("Lâche", dfs, dfss),
            Nature("Foufou", ats, dfss), Nature("Naïf", vit, dfss),
            Nature("Brave", att, vit), Nature("Relax", dfs, vit),
            Nature("Discret", ats, vit), Nature("Malpoli", dfss, vit),
        ]

    @staticmethod
    def nature_neutre():
        return Nature("Sérieux", None, None)

    @staticmethod
    def objet_tenu_aleatoire():
        """Restes, Bandeau Choix, Baie Sitrus, ou rien (None)."""
        tirage = random.randint(0, 3)

        if tirage == 0:
            return ObjetTenu("restes")

        if tirage == 1:
            return ObjetTenu("bandeau")

        if tirage == 2:
            return ObjetTenu("baie")

        return None

    @staticmethod
    def sac(contenu):
        """Fabrique un sac. contenu : "standard", "aleatoire" ou "vide"."""
        objets = [Soin("Potion", 20), Soin("Super Potion", 50), Soin("Hyper Potion", 200),
                  Soin("Potion Max", None), Rappel("Rappel", 50), Rappel("Rappel Max", 100),
                  Guerison("Antidote", "poison", "Guérit le poison."),
                  Guerison("Anti-Para", "paralysie", "Guérit la paralysie."),
                  Guerison("Anti-Brûle", "brulure", "Guérit la brûlure."),
                  Guerison("Antigel", "gel", "Guérit le gel."),
                  Guerison("Réveil", "sommeil", "Réveille un Pokémon endormi."),
                  Guerison("Total Soin", None, "Guérit tous les statuts.")]
        quantites_standard = [3, 2, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0]

        sac = Sac()
        position = 0

        for objet in objets:
            if contenu == "standard":
                quantite = quantites_standard[position]
            elif contenu == "aleatoire":
                quantite = random.randint(0, 3)
            else:
                quantite = 0

            sac.ajouter(objet, quantite)
            position = position + 1

        return sac
