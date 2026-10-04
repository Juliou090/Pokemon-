"""Les 14 types de la génération 3 et leur table d'efficacité.

La table d'efficacité est répartie dans les types eux-mêmes : chaque fonction
creer_type_xxx() fabrique un objet TypePokemon qui contient trois listes de
noms de types (ceux qu'il bat à x2, ceux qui lui résistent à x0,5 et ceux qui
l'annulent à x0). Tout ce qui n'est écrit nulle part vaut x1.

Il n'y a donc ni variable globale ni dictionnaire : on appelle une fonction,
on obtient un objet.

Vérifié avec l'historique des types de PokéAPI (past_damage_relations) : on ne
garde que les 14 types utilisés (pas d'Insecte, de Dragon ni d'Acier).

On a le droit ici : décrire les types et leur efficacité.
On N'A PAS le droit : de calculer des dégâts ni d'afficher quoi que ce soit.
Pour ajouter un type : écrire une nouvelle fonction, l'ajouter dans
creer_tous_les_types(), et ajouter son nom dans les listes des autres types.
"""

from modeles.type_pokemon import TypePokemon


def creer_type_normal():
    """Crée le type Normal (attaques physiques)."""
    return TypePokemon(
        "Normal",
        False,
        [],
        ["Roche"],
        ["Spectre"],
    )


def creer_type_feu():
    """Crée le type Feu (attaques spéciales)."""
    return TypePokemon(
        "Feu",
        True,
        ["Plante", "Glace"],
        ["Feu", "Eau", "Roche"],
        [],
    )


def creer_type_eau():
    """Crée le type Eau (attaques spéciales)."""
    return TypePokemon(
        "Eau",
        True,
        ["Feu", "Sol", "Roche"],
        ["Eau", "Plante"],
        [],
    )


def creer_type_plante():
    """Crée le type Plante (attaques spéciales)."""
    return TypePokemon(
        "Plante",
        True,
        ["Eau", "Sol", "Roche"],
        ["Feu", "Plante", "Poison", "Vol"],
        [],
    )


def creer_type_electrik():
    """Crée le type Électrik (attaques spéciales)."""
    return TypePokemon(
        "Électrik",
        True,
        ["Eau", "Vol"],
        ["Électrik", "Plante"],
        ["Sol"],
    )


def creer_type_glace():
    """Crée le type Glace (attaques spéciales)."""
    return TypePokemon(
        "Glace",
        True,
        ["Plante", "Sol", "Vol"],
        ["Feu", "Eau", "Glace"],
        [],
    )


def creer_type_combat():
    """Crée le type Combat (attaques physiques)."""
    return TypePokemon(
        "Combat",
        False,
        ["Normal", "Glace", "Roche", "Ténèbres"],
        ["Poison", "Vol", "Psy"],
        ["Spectre"],
    )


def creer_type_poison():
    """Crée le type Poison (attaques physiques)."""
    return TypePokemon(
        "Poison",
        False,
        ["Plante"],
        ["Poison", "Sol", "Roche", "Spectre"],
        [],
    )


def creer_type_sol():
    """Crée le type Sol (attaques physiques)."""
    return TypePokemon(
        "Sol",
        False,
        ["Feu", "Électrik", "Poison", "Roche"],
        ["Plante"],
        ["Vol"],
    )


def creer_type_vol():
    """Crée le type Vol (attaques physiques)."""
    return TypePokemon(
        "Vol",
        False,
        ["Plante", "Combat"],
        ["Électrik", "Roche"],
        [],
    )


def creer_type_psy():
    """Crée le type Psy (attaques spéciales)."""
    return TypePokemon(
        "Psy",
        True,
        ["Combat", "Poison"],
        ["Psy"],
        ["Ténèbres"],
    )


def creer_type_roche():
    """Crée le type Roche (attaques physiques)."""
    return TypePokemon(
        "Roche",
        False,
        ["Feu", "Glace", "Vol"],
        ["Combat", "Sol"],
        [],
    )


def creer_type_tenebres():
    """Crée le type Ténèbres (attaques spéciales)."""
    return TypePokemon(
        "Ténèbres",
        True,
        ["Psy", "Spectre"],
        ["Combat", "Ténèbres"],
        [],
    )


def creer_type_spectre():
    """Crée le type Spectre (attaques physiques)."""
    return TypePokemon(
        "Spectre",
        False,
        ["Psy", "Spectre"],
        ["Ténèbres"],
        ["Normal"],
    )


def creer_tous_les_types():
    """Renvoie la liste des 14 types (une liste qui contient des objets TypePokemon)."""
    liste_des_types = []
    liste_des_types.append(creer_type_normal())
    liste_des_types.append(creer_type_feu())
    liste_des_types.append(creer_type_eau())
    liste_des_types.append(creer_type_plante())
    liste_des_types.append(creer_type_electrik())
    liste_des_types.append(creer_type_glace())
    liste_des_types.append(creer_type_combat())
    liste_des_types.append(creer_type_poison())
    liste_des_types.append(creer_type_sol())
    liste_des_types.append(creer_type_vol())
    liste_des_types.append(creer_type_psy())
    liste_des_types.append(creer_type_roche())
    liste_des_types.append(creer_type_tenebres())
    liste_des_types.append(creer_type_spectre())

    return liste_des_types
