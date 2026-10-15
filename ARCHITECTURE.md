# Architecture du projet

Simulateur de combat Pokémon (génération 3), en console, à deux joueurs. Lancer : `python main.py`.
Tests : `python -m unittest discover -s tests -t .`

## Les fichiers

```
main.py                    crée un Jeu et le lance (rien d'autre)
jeu.py                     Jeu : écran titre -> création des 2 joueurs -> combat -> fin
exceptions.py              nos exceptions (PokemonKOError, ObjetIndisponibleError, PVInvalideError...)

modeles/                   les objets du monde Pokémon
  type_pokemon.py          TypePokemon : un type, ses forces et faiblesses
  statistiques.py          Statistiques (6 valeurs + formule de calcul) et Nature
  attaque.py               Attaque, EffetStatut, EffetStat
  statuts.py               StatutMajeur + Poison, Brulure, Paralysie, Sommeil, Gel
  pokemon.py               Pokemon (PV privés, stats en combat, paliers)
  objets.py                Objet + Soin, Rappel, Guerison, ObjetTenu
  dresseur.py              Equipe, Sac (LigneSac), Dresseur

donnees/
  catalogue.py             Catalogue : 14 types, 32 attaques, 15 Pokémon, 25 natures, sacs,
                           5 équipes toutes faites (une ligne « nom = Pokemon(...) » par Pokémon)

combat/
  actions.py               Action + ActionAttaque, ActionChangement, ActionObjet, ActionAbandon
  combat.py                Combat : la boucle tour par tour (écrit d'abord par Charlotte)
                           + le calcul des dégâts (méthodes avec self, génération 3)

modes/
  creation_equipe.py       CreationEquipe : les 4 modes de création d'équipe

ui/                        le seul dossier qui utilise print et input
  affichage.py             Affichage : tout ce qui s'affiche
  menus.py                 Menus : questions au joueur (avec vérification)
  exemples_affichage.py    OutilsAffichage : couleurs, cadres, barres de PV, Poké Ball
  audio.py                 Audio : musique de fond (avec transitions) et bruitages

audio/                     musiques (.mp3) et bruitages (audio/sons/*.wav)
outils/generer_sons.py     fabrique les bruitages (hors jeu)

tests/                     tests unittest
GUIDE_PYTHON.md            explication des syntaxes utilisées
```

## Qui dépend de qui

`main -> jeu -> {modes, combat, ui, donnees}` ; `combat -> modeles, donnees` ; `donnees -> modeles` ;
`ui -> modeles, donnees` ; `modeles` ne dépend de rien d'autre que de `exceptions`.
Aucun `print` ni `input` hors de `ui/`. Aucune variable globale : les valeurs communes sont des
attributs de classe.

## Choix principaux

- **Données en objets, pas de JSON** : `Catalogue.pokemon(0)` fabrique un vrai `Pokemon`. Chaque appel
  renvoie un objet neuf (deux Dracaufeu ne partagent pas leurs PP). Pour ajouter un Pokémon ou une
  attaque, on copie une ligne `xxx = Pokemon(...)` / `xxx = Attaque(...)` dans `catalogue.py`.
- **Orienté objet partout** : le calcul des dégâts est dans `Combat` (avec `self`), `Affichage`
  hérite de `OutilsAffichage`. Seule exception assumée : `Catalogue`, qui ne fait que fabriquer les
  données du jeu (le seul `@staticmethod`, expliqué dans `GUIDE_PYTHON.md`). Pas de `@property`
  ni de classe abstraite : des `get_` / `set_` pour les PV, et des classes mères normales.
- **Le son avec pygame.mixer** (seulement la partie son) : MP3, volume, fondus et bruitages en
  quelques lignes de Python. Sans pygame ou sans carte son, le jeu marche pareil, en silence.
- **Texte lettre par lettre** : `Affichage.ecrire`, vitesse réglable avec `delai_lettre`.
- **Les types connaissent leurs forces** : pas de tableau 14 x 14 ; `TypePokemon.efficacite_contre(...)`.
- **Encapsulation** : les PV sont privés (`_pv`) avec `get_pv` / `set_pv` qui vérifient la valeur.
- **Polymorphisme** : `Objet.utiliser`, `StatutMajeur.peut_agir`, `Action.executer` sont redéfinies
  par les classes filles ; le combat les appelle sans savoir de quelle fille il s'agit.
- **Exceptions** : un objet inutile ou épuisé, un changement impossible, des PV incohérents lèvent
  une exception, rattrapée dans `Combat` pour expliquer l'erreur au joueur sans perdre son tour.

## Check-list du prof

- [x] 14 types dont des doubles types, 15 Pokémon, 32 attaques (physiques, spéciales, de statut)
- [x] Dresseur : équipe de 3 Pokémon (`Equipe.TAILLE`) + sac d'objets
- [x] Combat tour par tour : attaque / changement / objet (+ abandon), ordre priorité puis vitesse
- [x] Dégâts avec efficacité des types (double type), STAB, critique, brûlure, variation aléatoire
- [x] Attaques de statut, stats temporaires (-6 à +6), 5 statuts majeurs
- [x] PV privés ; `PokemonKOError`, `ObjetIndisponibleError`, `PVInvalideError` levées
- [x] Aucune variable globale ; Pokémon / attaque / objet = objets
- [x] `main.py` sans logique ; `print` uniquement dans `ui/`
