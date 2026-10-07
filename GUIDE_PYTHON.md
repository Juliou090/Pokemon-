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
3. [Les getters `get_...` et `@property` (lecture)](#3-les-getters-get_nom-et-property-lecture)
4. [Les setters `set_...` et `@nom.setter` (écriture contrôlée)](#4-les-setters-set_pv-et-nomsetter-écriture-contrôlée)
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
23. [Annotations de type (`: int`, `-> bool`, `-> None`)](#23-les-annotations-de-type--int---bool---none)
24. [`self` : sur quel objet travaille la méthode ?](#24-self--sur-quel-objet-travaille-la-méthode-)

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

## 3. Les getters (`get_nom()`) et `@property` (lecture)

**Le problème** : on a mis l'attribut en privé (`_nom`, avec un `_`) pour que personne ne le modifie
n'importe comment depuis l'extérieur. Mais alors, comment les autres fichiers peuvent-ils **lire** le nom ?
On leur fournit une méthode qui le renvoie : un **getter** (de l'anglais « get » = obtenir).

**Version classique avec `get_` (celle que ton prof préfère)** :

```python
class Chien:
    def __init__(self, nom):
        self._nom = nom            # attribut privé : on n'y touche pas de l'extérieur

    def get_nom(self):             # le getter : il RENVOIE le nom
        return self._nom

rex = Chien("Rex")
print(rex.get_nom())               # affiche Rex  (avec des parenthèses : c'est une méthode)
rex._nom = "Max"                   # possible techniquement, mais INTERDIT par convention (le _)
```

**À quoi ça sert, concrètement ?** Aujourd'hui `get_nom` renvoie juste `_nom`. Mais demain on pourrait
vouloir renvoyer le nom en majuscules, ou afficher « Rex (niv. 5) » : on change UNE seule méthode, et tous
les fichiers qui l'utilisent continuent de fonctionner sans rien changer. Si tout le monde lisait
`_nom` directement, il faudrait modifier tout le projet.

**La version raccourcie avec `@property`** (même résultat, écriture plus courte). Le `@` s'appelle un
**décorateur** : une étiquette collée juste au-dessus d'une fonction pour dire à Python « traite cette
fonction d'une manière spéciale ». `@property` dit : « cette méthode se lit comme un attribut, sans
parenthèses ».

```python
class Chien:
    def __init__(self, nom):
        self._nom = nom

    @property
    def nom(self):                 # même contenu que get_nom
        return self._nom

rex = Chien("Rex")
print(rex.nom)                     # affiche Rex : .nom et pas .nom()
rex.nom = "Max"                    # ERREUR : pas de setter, c'est en lecture seule
```

| Je veux... | Avec `get_` | Avec `@property` |
|---|---|---|
| lire le nom | `rex.get_nom()` | `rex.nom` |
| définir la méthode | `def get_nom(self):` | `@property` puis `def nom(self):` |
| risque | aucun | aucun, c'est équivalent |

**Conseil** : utilise les `get_` si ton prof les préfère. Les deux sont corrects : l'important est d'avoir
un attribut privé et un accès contrôlé.

**Où** : dans le code de départ, `Pokemon.nom`, `Attaque.puissance`, `TypePokemon.nom`... sont écrits
avec `@property` ; on peut les remplacer par `get_nom()`, `get_puissance()`...

## 4. Les setters (`set_pv()`) et `@nom.setter` (écriture contrôlée)

**Le problème** : on veut aussi pouvoir **modifier** une valeur privée (par exemple les PV), mais
seulement si la nouvelle valeur est cohérente. On passe par une méthode qui **vérifie avant d'écrire** :
un **setter** (de « set » = définir).

**Version classique avec `set_` (celle que ton prof préfère)** :

```python
class Pokemon:
    def __init__(self):
        self._pv = 100             # attribut privé

    def get_pv(self):              # lire
        return self._pv

    def set_pv(self, nouvelle_valeur):   # écrire, AVEC vérification
        if nouvelle_valeur < 0:
            raise PVInvalideError("PV négatifs")   # on refuse la valeur
        self._pv = nouvelle_valeur                 # sinon on l'accepte

p = Pokemon()
p.set_pv(50)                       # accepté
p.set_pv(-3)                       # lève PVInvalideError : la valeur est refusée
print(p.get_pv())                  # 50 : les PV n'ont pas été abîmés
```

Sans le setter, n'importe quel bout de code pourrait écrire `p._pv = -3` et le Pokémon aurait des PV
absurdes sans que personne s'en aperçoive. Le setter est le **gardien** de la valeur.

**La version raccourcie avec `@nom.setter`** (même résultat). Il faut DEUX morceaux qui portent le
**même nom** : le `@property` (lire) et le `@pv.setter` (écrire). On écrit ensuite `p.pv = 50` (un simple
`=`), et Python appelle automatiquement le setter.

```python
class Pokemon:
    def __init__(self):
        self._pv = 100

    @property
    def pv(self):                  # lire : print(p.pv)
        return self._pv

    @pv.setter
    def pv(self, nouvelle_valeur): # écrire : p.pv = 50
        if nouvelle_valeur < 0:
            raise PVInvalideError("PV négatifs")
        self._pv = nouvelle_valeur

p = Pokemon()
p.pv = 50                          # appelle le setter : accepté
p.pv = -3                          # le setter lève PVInvalideError
```

| Je veux... | Avec `get_` / `set_` | Avec `@property` / `@pv.setter` |
|---|---|---|
| lire les PV | `p.get_pv()` | `p.pv` |
| changer les PV | `p.set_pv(50)` | `p.pv = 50` |
| vérifier la valeur | dans `set_pv` | dans le `@pv.setter` |

**Où** : les PV de `Pokemon` dans `modeles/pokemon.py`.

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

**À quoi ça sert** : une classe abstraite est un **modèle** qu'on ne peut pas créer directement. Elle
impose à ses classes filles d'écrire certaines méthodes (celles marquées `@abstractmethod`). Si une
fille oublie une méthode, Python refuse de la créer et affiche une erreur : on est prévenu tout de suite.

```python
from abc import ABC, abstractmethod

class Forme(ABC):                       # ABC : « classe abstraite »
    @abstractmethod
    def aire(self):
        """Chaque forme doit calculer son aire."""

class Carre(Forme):
    def __init__(self, cote):
        self._cote = cote
    def aire(self):                     # obligatoire, sinon erreur
        return self._cote * self._cote

class Rond(Forme):
    pass                                # on a OUBLIÉ aire()

forme = Forme()                         # ERREUR : on ne crée pas une classe abstraite
rond = Rond()                           # ERREUR : Rond n'a pas défini aire()
carre = Carre(3)                        # OK
```

**Pourquoi c'est utile (polymorphisme)** : on est sûr que TOUTES les formes ont une méthode `aire()`.
Le reste du programme peut donc les traiter pareil, sans savoir de quelle forme il s'agit :

```python
for forme in [Carre(3), Cercle(2)]:
    print(forme.aire())                 # chacune calcule à SA façon
```

Dans le projet : le combat appelle `statut.peut_agir()` ou `objet.utiliser()` sans se demander s'il a
affaire à une paralysie ou à une potion.

**Où** : `StatutMajeur` (`modeles/statuts.py`), `EffetAttaque` (`modeles/effet.py`), `Objet`
(`objets/objet.py`), `Action` (`combat/actions.py`), `ModeSelection` (`modes/mode_selection.py`).

## 10. `@staticmethod`

**À quoi ça sert** : une méthode rangée dans une classe, mais qui n'a **besoin d'aucun objet** : elle
n'utilise aucun `self`. On l'appelle directement avec le nom de la classe, sans créer d'objet.

**Sans `@staticmethod`**, il faut d'abord créer un objet, même s'il ne sert à rien :

```python
class Outils:
    def double(self, nombre):           # self est là, mais jamais utilisé
        return nombre * 2

outils = Outils()                       # obligé de créer un objet...
print(outils.double(4))                 # ...pour pouvoir appeler la méthode : 8
```

**Avec `@staticmethod`**, plus de `self` et plus d'objet à créer :

```python
class Outils:
    @staticmethod
    def double(nombre):                 # pas de self
        return nombre * 2

print(Outils.double(4))                 # on appelle avec le nom de la classe : 8
```

**Pourquoi la ranger dans une classe plutôt que de faire une simple fonction ?** Pour le rangement : le
calcul des stats appartient logiquement à `Statistiques`, mais il n'a pas besoin d'un Pokémon précis,
juste de nombres. Même idée pour `Nature.neutre()` qui fabrique une nature sans avoir besoin d'une
nature existante.

**Règle simple** : si la méthode utilise `self._quelquechose` ou une autre méthode de l'objet, elle
garde `self` ; sinon, c'est un `@staticmethod`.

**Où** : `Statistiques.calculer`, `Statistiques.zeros`, `Statistiques.aleatoires`,
`Statistiques.identiques` (`modeles/statistiques.py`) ; `Nature.neutre` (`modeles/nature.py`) ;
tous les outils de `ui/exemples_affichage.py`.

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

## 23. Les annotations de type (`: int`, `-> bool`, `-> None`)

**À quoi ça sert** : ce sont des **notes pour le lecteur** (et pour l'éditeur de code), qui disent quel
genre de valeur on attend. **Python les ignore complètement** : si on les enlève, le programme
fonctionne exactement pareil.

- `nom: str` après un paramètre veut dire « ce paramètre est un texte ».
- `-> bool` après les parenthèses veut dire « cette fonction **renvoie** un booléen (True ou False) ».
- `-> None` veut dire « cette fonction **ne renvoie rien** » (elle fait une action, sans résultat).

```python
def est_ko(self) -> bool:          # renvoie True ou False
    return self._pv == 0

def afficher(self, texte: str) -> None:   # reçoit un texte, ne renvoie rien
    print(texte)
```

**Attention, deux confusions fréquentes** :
- Dans `def __init__(self) -> None:`, le `-> None` ne parle PAS de `self` : il dit seulement que
  `__init__` ne renvoie rien (c'est toujours le cas pour `__init__`). On n'« attend » pas que `self`
  soit `None`.
- La flèche ne change **rien** à l'exécution : si on écrit `-> bool` et que la fonction renvoie un
  texte, Python ne dit rien.

**Où** : dans les squelettes de départ des fichiers (non encore codés). Dans le code complet de la
branche de démonstration, on les a enlevées pour rester au plus simple.

## 24. `self` : sur quel objet travaille la méthode ?

**À quoi ça sert** : `self` est l'objet **sur lequel on a appelé la méthode**. C'est lui qui permet à la
méthode de retrouver ses données (`self._nom`) ou d'appeler ses autres méthodes (`self.autre()`).
`self` n'apparaît pas par magie : Python le fournit tout seul.

```python
class Chien:
    def __init__(self, nom):
        self._nom = nom                     # self = le chien qu'on est en train de créer

    def aboyer(self):
        print(self._nom + " : Ouaf !")      # self = le chien qui aboie

rex = Chien("Rex")
medor = Chien("Médor")
rex.aboyer()                                # Rex : Ouaf !     (ici self = rex)
medor.aboyer()                              # Médor : Ouaf !   (ici self = medor)

# Écrire rex.aboyer() revient EXACTEMENT à écrire Chien.aboyer(rex).
# Python met l'objet qui est devant le point à la place de self.
```

**Et pour une méthode comme `lancer()` du Jeu ?** Dans `main.py`, on écrit `Jeu().lancer()` :
1. `Jeu()` **crée un objet Jeu**. Son `__init__` range dedans un `_affichage`, une `_saisie`, des
   `_menus` ;
2. `.lancer()` est appelée **sur cet objet**. Dans `lancer`, `self` est donc ce Jeu-là, et
   `self._affichage` est l'affichage rangé dedans.

**Lire `self._affichage.accueil()`** de gauche à droite : `self` (le Jeu), son attribut `_affichage` (un
objet de la classe `Affichage`), et la méthode `accueil` de cet objet. Dans `accueil`, le `self` est
alors **l'objet Affichage** (il s'en sert pour retrouver, par exemple, la largeur des cadres).

**Appeler la méthode sur la classe ou sur un objet ?**

```python
Affichage.accueil()          # ERREUR : sur la classe, il manque l'objet (le self)
affichage = Affichage()      # on crée un objet
affichage.accueil()          # OK : self = cet objet
```

Sur la classe, ça ne marche que pour un `@staticmethod` (voir l'entrée 10), qui n'a justement pas de `self`.

**Règle simple** : une méthode a besoin de `self` quand elle utilise les données de l'objet
(`self._xxx`) ou ses autres méthodes (`self._creer_les_dresseurs()`). Sinon, c'est un `@staticmethod`.

**Où** : toutes les méthodes de toutes les classes.
