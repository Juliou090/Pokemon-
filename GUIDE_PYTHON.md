# Guide : les `@` du projet

Les notions de classe, de `self`, de `get_` / `set_` et d'héritage sont déjà connues. Ce guide
explique **seulement** ce qu'il y a derrière le caractère `@` dans le code.

Il n'y a qu'**un seul** `@` dans tout le projet : `@staticmethod`.

---

## Que veut dire un `@` ?

Un `@quelquechose` écrit **juste au-dessus d'une fonction** s'appelle un **décorateur**. C'est une
étiquette collée sur la fonction pour dire à Python : « traite cette fonction d'une manière
particulière ». Ça ne change pas ce que la fonction fait à l'intérieur, seulement la façon dont on
l'utilise.

## `@staticmethod` : une méthode qui n'a pas besoin d'objet

### Le problème

Une méthode normale a `self` en premier paramètre. Pour l'appeler, il faut d'abord **créer un objet**,
parce que Python met cet objet à la place de `self`.

```python
class Outils:
    def double(self, nombre):        # self est là, mais on ne s'en sert jamais
        return nombre * 2

outils = Outils()                    # obligé de créer un objet...
print(outils.double(4))              # ...pour pouvoir appeler la méthode : 8
```

Créer un objet qui ne sert à rien juste pour appeler une fonction, c'est inutile.

### La solution

Avec `@staticmethod`, on dit à Python : « cette méthode n'a pas besoin d'objet ». On enlève `self`, et on
l'appelle directement avec **le nom de la classe** :

```python
class Outils:
    @staticmethod
    def double(nombre):              # plus de self
        return nombre * 2

print(Outils.double(4))              # 8, sans créer d'objet
```

### Comment savoir si une méthode doit avoir `self` ou être `@staticmethod` ?

| La méthode... | Elle a... |
|---|---|
| utilise les données de l'objet (`self.nom`, `self.pv`...) ou ses autres méthodes | `self` (méthode normale) |
| n'utilise que ses paramètres, rien de l'objet | `@staticmethod` (pas de `self`) |

### Où on le trouve dans le projet

Une seule classe l'utilise : `Catalogue` (`donnees/catalogue.py`). Elle sert seulement à fabriquer
d'un coup les données du jeu (Pokémon, attaques, natures...). On l'appelle avec le nom de la classe :

```python
dracaufeu = Catalogue.pokemon(0)       # un Pokémon neuf, sans créer d'objet Catalogue
natures = Catalogue.natures()
```

Partout ailleurs, les méthodes ont `self` : le calcul des dégâts est dans `Combat`, les outils
d'affichage sont dans `OutilsAffichage` (dont `Affichage` hérite), etc.

### Pourquoi la ranger dans une classe plutôt que d'écrire une simple fonction ?

Pour le rangement : la fabrication des Pokémon appartient logiquement au `Catalogue`. Quand on cherche
où sont les données, on regarde dans cette classe.

### Erreur classique

```python
Catalogue.pokemon(0)                 # OK : la méthode est un @staticmethod
Pokemon.get_pv()                     # ERREUR : get_pv a besoin d'un Pokémon (self), pas de @staticmethod
dracaufeu.get_pv()                   # OK : on l'appelle sur un objet
```

Si tu appelles une méthode normale avec le nom de la classe, Python répond qu'il manque l'argument
`self` : c'est le signe qu'il faut l'appeler sur un objet (ou que c'est un `@staticmethod` oublié).
