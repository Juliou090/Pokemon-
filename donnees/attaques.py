"""Les 21 attaques du jeu : une fonction par attaque.

Chaque fonction creer_xxx() fabrique et renvoie un NOUVEL objet Attaque, avec
tous ses PP. On en crée une neuve à chaque fois pour que deux Pokémon ne
partagent jamais les mêmes PP.

Valeurs vérifiées avec PokéAPI (champ past_values) pour la génération 3.
Rappel : en génération 3, une attaque est spéciale ou physique selon son TYPE.

On a le droit ici : décrire des attaques.
On N'A PAS le droit : de calculer des dégâts ni d'afficher quoi que ce soit.
Pour ajouter une attaque : copier une fonction existante et l'adapter.
"""

from donnees.efficacite import creer_type_combat
from donnees.efficacite import creer_type_eau
from donnees.efficacite import creer_type_electrik
from donnees.efficacite import creer_type_feu
from donnees.efficacite import creer_type_glace
from donnees.efficacite import creer_type_normal
from donnees.efficacite import creer_type_plante
from donnees.efficacite import creer_type_poison
from donnees.efficacite import creer_type_psy
from donnees.efficacite import creer_type_roche
from donnees.efficacite import creer_type_sol
from donnees.efficacite import creer_type_spectre
from donnees.efficacite import creer_type_tenebres
from donnees.efficacite import creer_type_vol
from modeles.attaque import Attaque
from modeles.effet import EffetModifStat
from modeles.effet import EffetStatutMajeur
from modeles.statuts import Brulure
from modeles.statuts import Gel
from modeles.statuts import Paralysie
from modeles.statuts import Poison
from modeles.statuts import Sommeil


def creer_lance_flammes():
    """Crée l'attaque Lance-Flammes : 10 % de brûlure."""
    effets = []
    effets.append(EffetStatutMajeur(Brulure(), 10))

    return Attaque(
        "Lance-Flammes",
        creer_type_feu(),
        95,
        100,
        15,
        effets=effets,
    )


def creer_cru_aile():
    """Crée l'attaque Cru-Aile."""
    return Attaque(
        "Cru-Aile",
        creer_type_vol(),
        60,
        100,
        35,
    )


def creer_tranche():
    """Crée l'attaque Tranche : taux de coup critique élevé."""
    return Attaque(
        "Tranche",
        creer_type_normal(),
        70,
        100,
        20,
        critique_eleve=True,
    )


def creer_seisme():
    """Crée l'attaque Séisme."""
    return Attaque(
        "Séisme",
        creer_type_sol(),
        100,
        100,
        10,
    )


def creer_tranch_herbe():
    """Crée l'attaque Tranch'Herbe : taux de coup critique élevé."""
    return Attaque(
        "Tranch'Herbe",
        creer_type_plante(),
        55,
        95,
        25,
        critique_eleve=True,
    )


def creer_bombe_beurk():
    """Crée l'attaque Bombe Beurk : 30 % de poison."""
    effets = []
    effets.append(EffetStatutMajeur(Poison(), 30))

    return Attaque(
        "Bombe Beurk",
        creer_type_poison(),
        90,
        100,
        10,
        effets=effets,
    )


def creer_poudre_dodo():
    """Crée l'attaque Poudre Dodo : endort."""
    effets = []
    effets.append(EffetStatutMajeur(Sommeil(), 100))

    return Attaque(
        "Poudre Dodo",
        creer_type_plante(),
        0,
        75,
        15,
        effets=effets,
    )


def creer_poudre_toxik():
    """Crée l'attaque Poudre Toxik : empoisonne."""
    effets = []
    effets.append(EffetStatutMajeur(Poison(), 100))

    return Attaque(
        "Poudre Toxik",
        creer_type_poison(),
        0,
        75,
        35,
        effets=effets,
    )


def creer_tonnerre():
    """Crée l'attaque Tonnerre : 10 % de paralysie."""
    effets = []
    effets.append(EffetStatutMajeur(Paralysie(), 10))

    return Attaque(
        "Tonnerre",
        creer_type_electrik(),
        95,
        100,
        15,
        effets=effets,
    )


def creer_cage_eclair():
    """Crée l'attaque Cage-Éclair : paralyse."""
    effets = []
    effets.append(EffetStatutMajeur(Paralysie(), 100))

    return Attaque(
        "Cage-Éclair",
        creer_type_electrik(),
        0,
        100,
        20,
        effets=effets,
    )


def creer_vive_attaque():
    """Crée l'attaque Vive-Attaque : priorité +1."""
    return Attaque(
        "Vive-Attaque",
        creer_type_normal(),
        40,
        100,
        30,
        priorite=1,
    )


def creer_casse_brique():
    """Crée l'attaque Casse-Brique."""
    return Attaque(
        "Casse-Brique",
        creer_type_combat(),
        75,
        100,
        15,
    )


def creer_surf():
    """Crée l'attaque Surf."""
    return Attaque(
        "Surf",
        creer_type_eau(),
        95,
        100,
        15,
    )


def creer_laser_glace():
    """Crée l'attaque Laser Glace : 10 % de gel."""
    effets = []
    effets.append(EffetStatutMajeur(Gel(), 10))

    return Attaque(
        "Laser Glace",
        creer_type_glace(),
        95,
        100,
        10,
        effets=effets,
    )


def creer_eboulement():
    """Crée l'attaque Éboulement."""
    return Attaque(
        "Éboulement",
        creer_type_roche(),
        75,
        90,
        10,
    )


def creer_psyko():
    """Crée l'attaque Psyko : 10 % de baisse de Déf. Spé. de la cible."""
    effets = []
    effets.append(EffetModifStat("defense_speciale", -1, False, 10))

    return Attaque(
        "Psyko",
        creer_type_psy(),
        90,
        100,
        10,
        effets=effets,
    )


def creer_ball_ombre():
    """Crée l'attaque Ball'Ombre : 20 % de baisse de Déf. Spé. de la cible."""
    effets = []
    effets.append(EffetModifStat("defense_speciale", -1, False, 20))

    return Attaque(
        "Ball'Ombre",
        creer_type_spectre(),
        80,
        100,
        15,
        effets=effets,
    )


def creer_hypnose():
    """Crée l'attaque Hypnose : endort."""
    effets = []
    effets.append(EffetStatutMajeur(Sommeil(), 100))

    return Attaque(
        "Hypnose",
        creer_type_psy(),
        0,
        60,
        20,
        effets=effets,
    )


def creer_plenitude():
    """Crée l'attaque Plénitude : +1 Att. Spé. et +1 Déf. Spé. du lanceur."""
    effets = []
    effets.append(EffetModifStat("attaque_speciale", 1, True, 100))
    effets.append(EffetModifStat("defense_speciale", 1, True, 100))

    return Attaque(
        "Plénitude",
        creer_type_psy(),
        0,
        0,
        20,
        effets=effets,
    )


def creer_machouille():
    """Crée l'attaque Mâchouille : 20 % de baisse de Défense de la cible."""
    effets = []
    effets.append(EffetModifStat("defense", -1, False, 20))

    return Attaque(
        "Mâchouille",
        creer_type_tenebres(),
        80,
        100,
        15,
        effets=effets,
    )


def creer_grincement():
    """Crée l'attaque Grincement : Défense de la cible -2."""
    effets = []
    effets.append(EffetModifStat("defense", -2, False, 100))

    return Attaque(
        "Grincement",
        creer_type_normal(),
        0,
        85,
        40,
        effets=effets,
    )
