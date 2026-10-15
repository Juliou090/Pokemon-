# Simulateur de combat Pokémon (génération 3)

Projet NSI Terminale : combat Pokémon au tour par tour entre deux dresseurs, dans la console, en
Python (programmation orientée objet).

## Lancer
```
python main.py
```
Python 3.10 ou plus (bibliothèque standard ; pygame seulement pour le son). Pour de belles couleurs, utiliser le terminal
de VS Code ou Windows Terminal.

## Son
Musique de fond et bruitages avec `pygame` (seulement `pygame.mixer`) : `pip install pygame`
(ou `pip install pygame-ce` avec Python 3.14). Sans pygame, le jeu marche en silence. Les musiques
sont dans `audio/` (leurs noms se règlent dans `ui/audio.py`), les bruitages dans `audio/sons/`.
`JEU_SANS_SON=1` coupe le son. La vitesse d'écriture du texte se règle dans `jeu.py`.

## Tests
```
python -m unittest discover -s tests -t .
```

## Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) : où se trouve chaque chose et pourquoi.
- [GUIDE_PYTHON.md](GUIDE_PYTHON.md) : les syntaxes Python utilisées, expliquées avec des exemples.
