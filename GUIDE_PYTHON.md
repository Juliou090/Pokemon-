# Guide des syntaxes Python peu courantes

Ce fichier explique chaque syntaxe Python un peu avancée utilisée dans le projet, pour pouvoir
comprendre tout le code et le défendre à l'oral.

## Mode d'emploi

Chaque entrée suit le même modèle :

- **À quoi ça sert**, en une ou deux phrases simples ;
- **Exemple** très court et commenté ;
- **Où dans le projet** (fichier et classe).

Règle de mise à jour : à chaque fois qu'on utilise dans le code une syntaxe qui n'est pas encore
dans ce guide, on l'ajoute ici. Dans le doute sur le fait qu'elle soit « courante », on l'ajoute.

## Sommaire

1. [`__init__` et `self`](#1-__init__-et-self)
2. [Attribut privé (`_pv`)](#2-attribut-privé-_pv)
3. [`@property` (lecture)](#3-property-lecture)
4. [`@nom.setter` (écriture contrôlée)](#4-nomsetter-écriture-contrôlée)
5. [Exception personnalisée : `class MonErreur(Exception)`](#5-exception-personnalisée)
6. [`raise`](#6-raise)
7. [`try` / `except` et `assertRaises`](#7-try--except-et-assertraises)
8. [Héritage](#8-héritage)
9. [Classe abstraite : `ABC` et `@abstractmethod`](#9-classe-abstraite--abc-et-abstractmethod)
10. [`@staticmethod`](#10-staticmethod)
11. [Attribut de classe (`TAILLE = 3`)](#11-attribut-de-classe)
12. [`__str__`](#12-__str__)
13. [`__eq__` et `__hash__`](#13-__eq__-et-__hash__)
14. [`isinstance`](#14-isinstance)
15. [f-string](#15-f-string)
16. [Module `random`](#16-module-random)
17. [Division entière `//`](#17-division-entière-)
18. [Paramètre avec valeur par défaut et `is None`](#18-paramètre-avec-valeur-par-défaut-et-is-none)
19. [`import` et `from ... import ...`](#19-import-et-from--import-)
20. [`unittest` : `TestCase`, `setUp`, `assertEqual`...](#20-unittest)
21. [`if __name__ == "__main__":`](#21-if-__name__--__main__)
22. [Docstring](#22-docstring)

---

## 1. `__init__` et `self`

**À quoi ça sert** : `__init__` est la méthode appelée automatiquement quand on crée un objet. Elle
range les données de départ dans l'objet. `self` désigne « cet objet-ci » : c'est grâce à lui qu'on
accède à ses attributs.

```python
class Chien:
    def __init__(self, nom):
        self._nom = nom          # on range le nom DANS l'objet

rex = Chien("Rex")               # appelle Chien.__init__(rex, "Rex")
```

**Où** : toutes les classes, par exemple `Pokemon.__init__` dans `modeles/pokemon.py`.

## 2. Attribut privé (`_pv`)

**À quoi ça sert** : un nom qui commence par `_` signifie « n'y touche pas depuis l'extérieur ».
Pour le lire ou le modifier, on passe par une méthode ou une propriété qui vérifie que tout reste
cohérent. C'est l'**encapsulation** demandée par le prof.

```python
class Compte:
    def __init__(self):
        self._argent = 0         # privé : on ne fait pas compte._argent = -5 de l'extérieur
```

**Où** : `Pokemon._pv` (`modeles/pokemon.py`), `Attaque._pp` (`modeles/attaque.py`), etc.

## 3. `@property` (lecture)

**À quoi ça sert** : permet d'écrire `pokemon.nom` (sans parenthèses) alors que c'est en réalité une
petite fonction qui renvoie l'attribut privé. Comme il n'y a pas de « setter », on ne peut pas le
modifier de l'extérieur.

```python
class Chien:
    def __init__(self, nom):
        self._nom = nom

    @property
    def nom(self):
        return self._nom         # chien.nom renvoie le nom, sans parenthèses
```

**Où** : `Pokemon.nom`, `Attaque.puissance`, `TypePokemon.nom`...

## 4. `@nom.setter` (écriture contrôlée)

**À quoi ça sert** : s'exécute quand on écrit `objet.nom = valeur`. On y vérifie la valeur avant de
l'accepter. C'est ce qui protège les PV.

```python
@property
def pv(self):
    return self._pv

@pv.setter
def pv(self, nouvelle_valeur):
    if nouvelle_valeur < 0:
        raise PVInvalideError("PV négatifs")   # on refuse la valeur
    self._pv = nouvelle_valeur                 # sinon on l'accepte
```

**Où** : `Pokemon.pv` dans `modeles/pokemon.py`.

## 5. Exception personnalisée

**À quoi ça sert** : on crée notre propre type d'erreur, avec un nom clair, en héritant de
`Exception`.

```python
class PVInvalideError(Exception):
    """Levée si les PV sont incohérents."""
```

**Où** : `exceptions.py` (`PokemonKOError`, `ObjetIndisponibleError`, `PVInvalideError`...). Elles
héritent toutes de `SimulateurError`, qui hérite d'`Exception`.

## 6. `raise`

**À quoi ça sert** : déclenche une erreur volontairement. Le programme s'arrête à cet endroit, sauf
si quelqu'un rattrape l'erreur avec `try/except`.

```python
if age < 0:
    raise ValueError("L'âge ne peut pas être négatif")
```

**Où** : `Pokemon.pv` (setter), `Pokemon.verifier_peut_agir`, `Attaque.utiliser_pp`,
`Equipe.__init__`. On trouve aussi `raise NotImplementedError` dans les méthodes « à écrire plus
tard » : cela veut dire « pas encore codé ».

## 7. `try` / `except` et `assertRaises`

**À quoi ça sert** : `try/except` essaie un bout de code et réagit si une erreur survient, au lieu de
planter. Dans les tests, `assertRaises` vérifie qu'une erreur précise est bien levée.

```python
try:
    pokemon.pv = -5              # on essaie
except PVInvalideError:
    print("Valeur refusée")      # on réagit à l'erreur

# Dans un test :
with self.assertRaises(PVInvalideError):
    pokemon.pv = -5              # le test réussit SI cette erreur est levée
```

**Où** : `assertRaises` dans `tests/test_pokemon.py`, `tests/test_attaque.py`,
`tests/test_equipe_dresseur.py`.

## 8. Héritage

**À quoi ça sert** : une classe « fille » reprend tout ce que fait sa classe « mère » et peut y
ajouter ou y changer des choses. On l'écrit en mettant la mère entre parenthèses.

```python
class Animal:
    def parler(self):
        return "..."

class Chien(Animal):             # Chien hérite d'Animal
    def parler(self):            # il remplace la méthode de la mère
        return "Ouaf"
```

**Où** : `Poison`, `Paralysie`... héritent de `StatutMajeur` (`modeles/statuts.py`) ;
`EffetStatutMajeur` et `EffetModifStat` héritent de `EffetAttaque` (`modeles/effet.py`) ; les
exceptions héritent de `SimulateurError`.

## 9. Classe abstraite : `ABC` et `@abstractmethod`

**À quoi ça sert** : une classe abstraite est un « modèle » qu'on ne peut pas créer directement. Elle
impose à ses classes filles d'écrire certaines méthodes (celles marquées `@abstractmethod`).

```python
from abc import ABC, abstractmethod

class Forme(ABC):
    @abstractmethod
    def aire(self):
        """Chaque forme doit calculer son aire."""

class Carre(Forme):
    def aire(self):              # obligatoire, sinon on ne peut pas créer un Carre
        return 4
```

**Où** : `StatutMajeur` (`modeles/statuts.py`) et `EffetAttaque` (`modeles/effet.py`).

## 10. `@staticmethod`

**À quoi ça sert** : une méthode rangée dans une classe mais qui n'a pas besoin d'un objet (pas de
`self`). On l'appelle directement avec le nom de la classe.

```python
class Outils:
    @staticmethod
    def double(nombre):
        return nombre * 2

Outils.double(4)                 # renvoie 8, sans créer d'objet
```

**Où** : `Statistiques.calculer`, `Statistiques.zeros`, `Statistiques.aleatoires`,
`Statistiques.identiques` (`modeles/statistiques.py`) ; `Nature.neutre` (`modeles/nature.py`).

## 11. Attribut de classe

**À quoi ça sert** : une valeur partagée par tous les objets de la classe, écrite directement dans la
classe (au lieu de `__init__`). C'est ce qu'on utilise à la place d'une variable globale. On y accède
par `NomDeLaClasse.ATTRIBUT`.

```python
class Equipe:
    TAILLE = 3                   # attribut de classe

    def __init__(self, pokemons):
        if len(pokemons) != Equipe.TAILLE:
            ...
```

**Où** : `Equipe.TAILLE` (`modeles/equipe.py`), `Pokemon.NIVEAU_MAX` (`modeles/pokemon.py`),
`ModificateursStats.PALIER_MAX` (`modeles/modificateurs.py`).

## 12. `__str__`

**À quoi ça sert** : définit le texte qui s'affiche quand on fait `print(objet)` ou `str(objet)`.

```python
class Chien:
    def __str__(self):
        return "Un chien"
```

**Où** : `Pokemon.__str__`, `Attaque.__str__`, `TypePokemon.__str__`, `Nature.__str__`...

## 13. `__eq__` et `__hash__`

**À quoi ça sert** : `__eq__` définit quand deux objets sont considérés comme « égaux » (le `==`).
Dès qu'on redéfinit `__eq__`, il faut aussi définir `__hash__` pour que l'objet reste utilisable
dans un ensemble ou comme clé.

```python
def __eq__(self, autre):
    return self._nom == autre.nom        # même nom = même type

def __hash__(self):
    return hash(self._nom)
```

**Où** : `TypePokemon` (`modeles/type_pokemon.py`) : deux objets « Feu » créés séparément sont égaux.

## 14. `isinstance`

**À quoi ça sert** : teste si un objet est d'un certain type (d'une certaine classe).

```python
isinstance(5, int)               # True
isinstance("a", int)             # False
```

**Où** : `Pokemon.pv` (le setter vérifie que les PV sont un entier), `TypePokemon.__eq__`, et dans les
tests (`assertIsInstance`).

## 15. f-string

**À quoi ça sert** : fabriquer un texte en insérant des valeurs entre accolades. Elle commence par
`f` avant les guillemets.

```python
nom = "Dracaufeu"
niveau = 50
print(f"{nom} (niv. {niveau})")          # Dracaufeu (niv. 50)
```

**Où** : `Pokemon.__str__`, `Equipe.__init__`, `Statistiques.__str__`.

## 16. Module `random`

**À quoi ça sert** : tirer des nombres au hasard. `random.randint(0, 31)` donne un entier entre 0 et
31, bornes comprises.

```python
import random
iv = random.randint(0, 31)
```

**Où** : `Statistiques.aleatoires` (`modeles/statistiques.py`) pour tirer les IV.

## 17. Division entière `//`

**À quoi ça sert** : divise et garde seulement la partie entière (on « jette » les décimales). C'est
le « floor » des formules de Pokémon : `7 // 2` donne `3`.

```python
print(7 // 2)                    # 3
print(153 * 50 // 100)           # 76
```

**Où** : les formules de stats dans `Statistiques._calculer_pv` et `_calculer_autre_stat`. Les
natures utilisent un pourcentage entier (110, 100, 90) avec `//` plutôt que 1.1 pour éviter les
erreurs d'arrondi des décimaux.

## 18. Paramètre avec valeur par défaut et `is None`

**À quoi ça sert** : un paramètre peut avoir une valeur par défaut : si on ne le donne pas, c'est elle
qui est utilisée. On met souvent `None` (« rien ») et on crée la vraie valeur dans la fonction. `is None`
teste si on a reçu `None`. (On évite `liste=[]` dans la signature : cette liste serait partagée entre
tous les appels.)

```python
def creer(niveau=50, iv=None):
    if iv is None:
        iv = Statistiques.aleatoires()   # objet neuf à chaque appel
```

**Où** : `donnees/pokemons.py` (`creer_dracaufeu(niveau=50, iv=None, nature=None)`),
`Pokemon.__init__`, `Attaque.__init__` (`effets=None`).

## 19. `import` et `from ... import ...`

**À quoi ça sert** : utiliser du code écrit dans un autre fichier. `from donnees.attaques import
creer_surf` va chercher la fonction `creer_surf` dans le fichier `donnees/attaques.py`.

```python
import random                                    # tout le module
from modeles.pokemon import Pokemon              # une seule classe
```

**Où** : en haut de presque tous les fichiers. Les règles sur qui a le droit d'importer qui sont dans
`ARCHITECTURE.md`.

## 20. `unittest`

**À quoi ça sert** : écrire des tests automatiques. Une classe de test hérite de `unittest.TestCase`.
Chaque méthode dont le nom commence par `test_` est un test. `setUp` s'exécute avant chaque test pour
préparer les objets. `assertEqual(a, b)` vérifie que `a == b` ; `assertTrue`, `assertFalse`,
`assertIsInstance`, `assertRaises` vérifient d'autres choses.

```python
import unittest

class TestAddition(unittest.TestCase):
    def setUp(self):
        self.nombre = 2                      # préparé avant chaque test

    def test_double(self):
        self.assertEqual(self.nombre * 2, 4)
```

Lancer tous les tests : `python -m unittest discover -s tests -t .`

**Où** : tout le dossier `tests/`.

## 21. `if __name__ == "__main__":`

**À quoi ça sert** : ce bloc ne s'exécute que si on lance CE fichier directement (et pas quand un
autre fichier l'importe).

```python
if __name__ == "__main__":
    unittest.main()
```

**Où** : `main.py` et en bas de chaque fichier de `tests/`.

## 22. Docstring

**À quoi ça sert** : le texte entre triples guillemets juste sous `class` ou `def` : il décrit à quoi
sert la classe ou la méthode. Python le garde en mémoire (`help(Pokemon)` l'affiche).

```python
def soigner(self, quantite):
    """Rend des PV sans dépasser le maximum."""
```

**Où** : toutes les classes et méthodes publiques, et en tête de chaque fichier.
