"""Les 6 Pokémon du jeu : une fonction par Pokémon.

Chaque fonction creer_xxx() fabrique et renvoie un NOUVEL objet Pokemon, avec
ses types, ses stats de base et ses 4 attaques.

Stats de base vérifiées avec PokéAPI (champs stats et past_stats) pour la
génération 3. Une correction par rapport à la liste de départ : la Vitesse de
Raichu vaut 100 en génération 3 (elle n'est passée à 110 qu'en génération 6).

Paramètres communs à toutes les fonctions :
    niveau : niveau du Pokémon (50 par défaut)
    iv : objet Statistiques (None = IV tirés au hasard entre 0 et 31)
    nature : objet Nature (None = nature neutre)

On a le droit ici : décrire des Pokémon.
On N'A PAS le droit : de faire du combat ni d'afficher quoi que ce soit.
Pour ajouter un Pokémon : copier une fonction existante et l'adapter.
"""

from donnees.attaques import creer_ball_ombre
from donnees.attaques import creer_bombe_beurk
from donnees.attaques import creer_cage_eclair
from donnees.attaques import creer_casse_brique
from donnees.attaques import creer_cru_aile
from donnees.attaques import creer_eboulement
from donnees.attaques import creer_grincement
from donnees.attaques import creer_hypnose
from donnees.attaques import creer_lance_flammes
from donnees.attaques import creer_laser_glace
from donnees.attaques import creer_machouille
from donnees.attaques import creer_plenitude
from donnees.attaques import creer_poudre_dodo
from donnees.attaques import creer_poudre_toxik
from donnees.attaques import creer_psyko
from donnees.attaques import creer_seisme
from donnees.attaques import creer_surf
from donnees.attaques import creer_tonnerre
from donnees.attaques import creer_tranch_herbe
from donnees.attaques import creer_tranche
from donnees.attaques import creer_vive_attaque
from donnees.efficacite import creer_type_eau
from donnees.efficacite import creer_type_electrik
from donnees.efficacite import creer_type_feu
from donnees.efficacite import creer_type_plante
from donnees.efficacite import creer_type_poison
from donnees.efficacite import creer_type_psy
from donnees.efficacite import creer_type_roche
from donnees.efficacite import creer_type_sol
from donnees.efficacite import creer_type_tenebres
from donnees.efficacite import creer_type_vol
from modeles.pokemon import Pokemon
from modeles.statistiques import Statistiques


def creer_dracaufeu(niveau=50, iv=None, nature=None):
    """Crée un Dracaufeu."""
    types = []
    types.append(creer_type_feu())
    types.append(creer_type_vol())

    stats_base = Statistiques(
        pv=78,
        attaque=84,
        defense=78,
        attaque_speciale=109,
        defense_speciale=85,
        vitesse=100,
    )

    attaques = []
    attaques.append(creer_lance_flammes())
    attaques.append(creer_cru_aile())
    attaques.append(creer_tranche())
    attaques.append(creer_seisme())

    return Pokemon(
        "Dracaufeu",
        types,
        stats_base,
        niveau,
        attaques,
        nature=nature,
        iv=iv,
    )


def creer_florizarre(niveau=50, iv=None, nature=None):
    """Crée un Florizarre."""
    types = []
    types.append(creer_type_plante())
    types.append(creer_type_poison())

    stats_base = Statistiques(
        pv=80,
        attaque=82,
        defense=83,
        attaque_speciale=100,
        defense_speciale=100,
        vitesse=80,
    )

    attaques = []
    attaques.append(creer_tranch_herbe())
    attaques.append(creer_bombe_beurk())
    attaques.append(creer_poudre_dodo())
    attaques.append(creer_poudre_toxik())

    return Pokemon(
        "Florizarre",
        types,
        stats_base,
        niveau,
        attaques,
        nature=nature,
        iv=iv,
    )


def creer_raichu(niveau=50, iv=None, nature=None):
    """Crée un Raichu."""
    types = []
    types.append(creer_type_electrik())

    stats_base = Statistiques(
        pv=60,
        attaque=90,
        defense=55,
        attaque_speciale=90,
        defense_speciale=80,
        vitesse=100,
    )

    attaques = []
    attaques.append(creer_tonnerre())
    attaques.append(creer_cage_eclair())
    attaques.append(creer_vive_attaque())
    attaques.append(creer_casse_brique())

    return Pokemon(
        "Raichu",
        types,
        stats_base,
        niveau,
        attaques,
        nature=nature,
        iv=iv,
    )


def creer_laggron(niveau=50, iv=None, nature=None):
    """Crée un Laggron."""
    types = []
    types.append(creer_type_eau())
    types.append(creer_type_sol())

    stats_base = Statistiques(
        pv=100,
        attaque=110,
        defense=90,
        attaque_speciale=85,
        defense_speciale=90,
        vitesse=60,
    )

    attaques = []
    attaques.append(creer_surf())
    attaques.append(creer_seisme())
    attaques.append(creer_laser_glace())
    attaques.append(creer_eboulement())

    return Pokemon(
        "Laggron",
        types,
        stats_base,
        niveau,
        attaques,
        nature=nature,
        iv=iv,
    )


def creer_gardevoir(niveau=50, iv=None, nature=None):
    """Crée un Gardevoir."""
    types = []
    types.append(creer_type_psy())

    stats_base = Statistiques(
        pv=68,
        attaque=65,
        defense=65,
        attaque_speciale=125,
        defense_speciale=115,
        vitesse=80,
    )

    attaques = []
    attaques.append(creer_psyko())
    attaques.append(creer_ball_ombre())
    attaques.append(creer_hypnose())
    attaques.append(creer_plenitude())

    return Pokemon(
        "Gardevoir",
        types,
        stats_base,
        niveau,
        attaques,
        nature=nature,
        iv=iv,
    )


def creer_tyranocif(niveau=50, iv=None, nature=None):
    """Crée un Tyranocif."""
    types = []
    types.append(creer_type_roche())
    types.append(creer_type_tenebres())

    stats_base = Statistiques(
        pv=100,
        attaque=134,
        defense=110,
        attaque_speciale=95,
        defense_speciale=100,
        vitesse=61,
    )

    attaques = []
    attaques.append(creer_machouille())
    attaques.append(creer_eboulement())
    attaques.append(creer_grincement())
    attaques.append(creer_seisme())

    return Pokemon(
        "Tyranocif",
        types,
        stats_base,
        niveau,
        attaques,
        nature=nature,
        iv=iv,
    )


def creer_tous_les_pokemon(niveau=50):
    """Renvoie la liste des 6 Pokémon (une liste qui contient des objets Pokemon)."""
    liste_des_pokemon = []
    liste_des_pokemon.append(creer_dracaufeu(niveau))
    liste_des_pokemon.append(creer_florizarre(niveau))
    liste_des_pokemon.append(creer_raichu(niveau))
    liste_des_pokemon.append(creer_laggron(niveau))
    liste_des_pokemon.append(creer_gardevoir(niveau))
    liste_des_pokemon.append(creer_tyranocif(niveau))

    return liste_des_pokemon
