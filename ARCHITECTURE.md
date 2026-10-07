# ARCHITECTURE — où coder quoi

Document de référence pour les deux membres du binôme. **Si tu hésites sur où mettre du code, lis ce fichier avant de coder.**
Le détail exact de chaque classe est aussi dans les docstrings des fichiers `.py` (squelettes).

---

## 1. Arborescence

La racine du dépôt EST la racine du projet (on lance `python main.py` depuis ici).

```
main.py                    Crée un Jeu et le lance. RIEN d'autre.
jeu.py                     Classe Jeu : enchaîne accueil → équipes → combat → fin.
exceptions.py              Toutes nos exceptions (PokemonKOError, ObjetIndisponibleError, PVInvalideError...).

modeles/                   Les objets du « monde Pokémon ».
  type_pokemon.py          TypePokemon : un des 14 types ; connaît ses forces et faiblesses.
  statistiques.py          Statistiques : 6 valeurs (PV, Att, Déf, AttSpé, DéfSpé, Vit) + formule de calcul.
  nature.py                Nature : +10 % / -10 % sur deux stats.
  effet.py                 EffetAttaque (abstraite) + EffetStatutMajeur, EffetModifStat.
  statuts.py               StatutMajeur (abstraite) + Poison, Paralysie, Brulure, Sommeil, Gel.
  modificateurs.py         ModificateursStats : paliers -6 à +6.
  talents.py               Talent (abstraite) — niveau 2.
  attaque.py               Attaque : nom, type, puissance, précision, PP, priorité, effet.
  pokemon.py               Pokemon : un individu (niveau, PV privés, nature, IV, attaques, statut...).
  equipe.py                Equipe : 3 Pokémon + le Pokémon actif.
  sac.py                   Sac (+ LigneSac) : inventaire d'objets.
  dresseur.py              Dresseur : nom + équipe + sac.

objets/                    Les objets utilisables.
  objet.py                 Objet (classe abstraite).
  soins.py                 Soin → Potion, SuperPotion, HyperPotion, PotionMax.
  rappel.py                Rappel, RappelMax (ranime un K.O.).
  guerison.py              Guerison → Antidote, AntiPara, TotalSoin...
  tenu.py                  Tenu → Restes, BandeauChoix, LunettesChoix, BaieSitrus.

combat/                    Le déroulement du combat.
  combat.py                Combat : la boucle tour par tour.
  actions.py               Action (abstraite) → ActionAttaque, ActionChangement, ActionObjet, ActionAbandon.
  ordre.py                 OrdreDesActions : priorité puis vitesse.
  calcul_degats.py         CalculateurDegats + ResultatDegats : formule gen 3.
  meteo.py                 Meteo (abstraite) — niveau 2.

modes/                     Les 3 façons de créer une équipe.
  mode_selection.py        ModeSelection (abstraite).
  mode_choisi.py           ModeChoisi : le joueur choisit tout.
  mode_aleatoire.py        ModeAleatoire : tout au hasard.
  mode_predefini.py        ModePredefini : équipe toute faite.

donnees/                   Données et chargement.
  efficacite.py            Les 14 types (une fonction creer_type_xxx() par type) et leur efficacité.
  attaques.py              Les 21 attaques (une fonction creer_xxx() par attaque).
  pokemons.py              Les 6 Pokémon (une fonction creer_xxx() par Pokémon).
  objets.py                FabriqueObjets : crée les objets par leur nom, sacs de départ.
  equipes.py               BibliothequeEquipes : équipes prédéfinies.


ui/                        SEUL dossier avec print() et input().
  affichage.py             Affichage : tous les messages.
  menus.py                 Menus : menus numérotés.
  saisie.py                Saisie : lecture clavier validée.
  sprites.py               Sprite : dessins en blocs colorés — niveau 3.
  exemples_affichage.py    Boîte à outils copiable : couleurs, cadres, barres de PV, Poké Ball.

sauvegarde/
  sauvegarde.py            GestionnaireSauvegarde — niveau 3.

tests/                     Un fichier test_*.py par module important (unittest).
README.md  ARCHITECTURE.md  .gitignore
```

### Ce qui diffère de la proposition de départ (et pourquoi)

| Changement | Raison |
|---|---|
| `statuts.py` et `modificateurs.py` déplacés de `combat/` vers `modeles/` | Un Pokémon **possède** un statut et des paliers : ils font partie de son état. Sinon `modeles/` dépendrait de `combat/`, ce qui est interdit. `combat/` ne fait que les **utiliser**. |
| `talents.py` déplacé vers `modeles/` | Même raison (un Pokémon possède un talent). `meteo.py` reste dans `combat/` (la météo appartient au combat, pas au Pokémon). |
| Pas de JSON, pas de chargeur, pas de classe `Espece` | Consigne du prof : les Pokémon/attaques sont créés directement comme objets par des fonctions `creer_xxx()`. Les anciens fichiers `pokemon.json`, `attaques.json`, `chargeur.py` et `outils/` sont supprimés. |
| Ajout de `modeles/effet.py` | Les attaques de statut/à effet (niveau 2 : drain, recul...) s'ajoutent par héritage sans modifier `Attaque`. |
| `Sac` utilise `LigneSac` | Respecte l'interdiction des dictionnaires/tuples pour les objets. |

---

## 2. « Je veux ajouter… donc je vais dans… »

| Je veux ajouter… | Je vais dans… |
|---|---|
| Une nouvelle potion (ex. Potion Mega) | `objets/soins.py` (nouvelle sous-classe de `Soin`) puis l'inscrire dans `donnees/objets.py` |
| Un nouvel objet de rappel | `objets/rappel.py` + `donnees/objets.py` |
| Un nouvel objet qui guérit un statut | `objets/guerison.py` + `donnees/objets.py` |
| Un nouvel objet tenu | `objets/tenu.py` + `donnees/objets.py` |
| Une nouvelle attaque | `donnees/attaques.py` (copier une fonction `creer_xxx()`) |
| Un nouvel effet d'attaque (drain, recul...) | `modeles/effet.py` (sous-classe de `EffetAttaque`) |
| Un nouveau Pokémon | `donnees/pokemons.py` (copier une fonction `creer_xxx()` + l'ajouter à `creer_tous_les_pokemon`) |
| Un nouveau type | `donnees/efficacite.py` (nouvelle fonction + noms ajoutés dans les listes des autres types) |
| Un nouveau statut (ex. gelé amélioré, brûlure) | `modeles/statuts.py` (sous-classe de `StatutMajeur`) |
| Un nouveau talent (niveau 2) | `modeles/talents.py` |
| Une nouvelle météo (niveau 2) | `combat/meteo.py` |
| Une nouvelle nature | `modeles/nature.py` (méthode `toutes`) |
| Un nouveau message à l'écran | `ui/affichage.py` (nouvelle méthode) |
| Un nouveau menu | `ui/menus.py` |
| Une nouvelle question au clavier (ex. oui/non) | `ui/saisie.py` |
| Une couleur / un sprite | `ui/sprites.py` ou `ui/affichage.py` |
| Un nouveau mode de création d'équipe | nouveau fichier `modes/mode_xxx.py` (sous-classe de `ModeSelection`) + l'ajouter dans `jeu.py` |
| Une nouvelle équipe prédéfinie | `donnees/equipes.py` |
| Une nouvelle action en combat | `combat/actions.py` (sous-classe de `Action`) + `ui/menus.py` |
| Une modification de la formule de dégâts | `combat/calcul_degats.py` |
| Un changement de l'ordre de jeu | `combat/ordre.py` |
| Une nouvelle exception | `exceptions.py` (hérite de `SimulateurError`) |
| Un test | `tests/test_<module>.py` |
| La sauvegarde (niveau 3) | `sauvegarde/sauvegarde.py` |
| Un changement de la règle de fin de combat | `combat/combat.py` (`est_termine`) |
| Un nouveau calcul de stat | `modeles/statistiques.py` |

---

## 3. Le contrat (classes, attributs, méthodes publiques)

Notation : `_x` = attribut privé (on y accède par une propriété ou une méthode).

### exceptions.py
| Classe | Rôle |
|---|---|
| `SimulateurError` | Mère de toutes les erreurs du projet |
| `PokemonKOError` | Faire agir/attaquer un Pokémon K.O. |
| `ObjetIndisponibleError` | Utiliser un objet absent ou épuisé |
| `PVInvalideError` | PV < 0 ou > PV max |
| `ActionInvalideError` | Action impossible (pas de PP, même Pokémon...) |
| `EquipeInvalideError` | Équipe de taille ≠ `Equipe.TAILLE` |
| `DonneesInvalidesError` | Pokémon impossible (niveau, nombre de types ou d'attaques invalide) |
| `SauvegardeError` | Échec de sauvegarde/chargement |

### modeles/
| Classe | Attributs | Méthodes publiques |
|---|---|---|
| `TypePokemon(nom, est_special, super_efficace_contre, peu_efficace_contre, sans_effet_contre)` | 5 attributs privés (3 listes de NOMS de types) | `nom`, `est_special`, `efficacite_contre(type)`, `efficacite_contre_pokemon(liste_de_types)`, `__eq__`, `__hash__` |
| `Statistiques(pv, attaque, defense, attaque_speciale, defense_speciale, vitesse)` | 6 entiers | `valeur(nom_stat)`, statiques : `calculer(base, iv, ev, niveau, nature)` (stats finales gen 3), `zeros()`, `aleatoires()` (IV 0-31), `identiques(v)` |
| `Nature(nom, stat_augmentee, stat_diminuee)` | 3 attributs privés | `nom`, `pourcentage(nom_stat)` *(110, 100 ou 90)*, `neutre()` *(statique)*, `toutes()` *(à écrire)* |
| `EffetAttaque` *(abstraite)* | — | `appliquer(lanceur, cible) -> str` |
| `EffetStatutMajeur(statut, chance_pourcent)` | `_statut`, `_chance_pourcent` | `statut`, `chance_pourcent`, `appliquer` *(à écrire)* |
| `EffetModifStat(nom_stat, paliers, sur_soi, chance_pourcent)` | 4 attributs privés | lectures, `appliquer` *(à écrire)* |
| `StatutMajeur` *(abstraite)* | — | `nom`, `peut_agir(pokemon)`, `degats_fin_de_tour(pokemon)`, `multiplicateur_stat(nom_stat)`, `fin_de_tour(pokemon)` |
| `Poison`, `Paralysie`, `Brulure`, `Sommeil`, `Gel` | — | redéfinissent les méthodes ci-dessus |
| `ModificateursStats()` | 5 paliers privés (`_palier_attaque`...) | `palier(nom_stat)`, `reinitialiser()`, puis *(à écrire)* `modifier`, `multiplicateur` |
| `Talent` *(abstraite, niv. 2)* | — | `nom`, `a_l_entree(...)`, `modifier_degats_recus(...)` |
| `Attaque(nom, type_attaque, puissance, precision, pp_max, priorite, effets, critique_eleve)` | `_nom`, `_type`, `_puissance`, `_precision` *(0 = ne rate jamais)*, `_pp_max`, `_pp`, `_priorite`, `_effets` *(liste d'objets)*, `_critique_eleve` | propriétés, `est_speciale`, `est_de_statut`, `utiliser_pp()`, `restaurer_pp()` |
| `Pokemon(nom, types, stats_base, niveau, attaques, nature, iv, ev, objet_tenu)` | `_nom`, `_types`, `_stats_base`, `_niveau`, `_nature`, `_iv`, `_ev`, `_stats`, **`_pv` (privé)**, `_attaques`, `_statut`, `_modificateurs`, `_objet_tenu` | `nom`, `types`, `niveau`, `nature`, `stats`, `attaques`, `pv` *(propriété + setter → `PVInvalideError`)*, `pv_max`, `est_ko`, `verifier_peut_agir()` *(→ `PokemonKOError`)*, `subir_degats(n)`, `soigner(n)`, puis *(à écrire)* `stat_effective`, `ranimer`, `appliquer_statut`, `guerir_statut`, `soigner_completement`, `a_la_sortie_du_terrain` |
| `Equipe(pokemons)` — attribut de classe **`Equipe.TAILLE = 3`** | `_pokemons`, `_indice_actif` | `pokemons`, `actif`, `vivants`, `est_vaincue()`, puis *(à écrire)* `changer_actif(i)`, `premier_vivant()`, `soigner_tous()` |
| `LigneSac(objet, quantite)` | `objet`, `quantite` | — |
| `Sac()` | `_lignes` | `ajouter(objet, q)`, `retirer(nom)` *(→ `ObjetIndisponibleError`)*, `quantite(nom)`, `lignes()`, `est_vide()` |
| `Dresseur(nom, equipe, sac)` | `_nom`, `_equipe`, `_sac`, `_a_abandonne` | `nom`, `equipe`, `sac`, `pokemon_actif`, `a_perdu()`, `abandonner()`, `utiliser_objet(nom, cible)` |

### objets/
| Classe | Méthodes publiques |
|---|---|
| `Objet(nom, description)` *(abstraite)* | `nom`, `description`, `peut_etre_utilise_sur(cible)`, `utiliser(cible) -> str` |
| `Soin` → `Potion`, `SuperPotion`, `HyperPotion`, `PotionMax` | `utiliser` rend des PV (jamais sur un K.O.) |
| `Rappel` → `RappelMax` | `utiliser` ranime un K.O. |
| `Guerison` → `Antidote`, `AntiPara`, `TotalSoin` | `utiliser` retire un statut |
| `Tenu` → `Restes`, `BandeauChoix`, `LunettesChoix`, `BaieSitrus` | `multiplicateur_stat(nom)`, `multiplicateur_degats(attaque)`, `fin_de_tour(porteur)` |

### combat/
| Classe | Méthodes publiques |
|---|---|
| `Combat(dresseur1, dresseur2, affichage, saisie)` | `lancer() -> Dresseur`, `est_termine()`, `vainqueur()` |
| `Action(acteur)` *(abstraite)* | `acteur`, `priorite`, `executer(adversaire, combat) -> list[str]` |
| `ActionAttaque(acteur, attaque)`, `ActionChangement(acteur, indice)`, `ActionObjet(acteur, nom_objet, indice_cible)`, `ActionAbandon(acteur)` | `executer` |
| `OrdreDesActions` | `trier(actions) -> list[Action]` |
| `ResultatDegats(degats, efficacite, critique)` | attributs en lecture |
| `CalculateurDegats()` | `calculer(attaquant, defenseur, attaque) -> ResultatDegats` |
| `Meteo` *(abstraite, niv. 2)* | `nom`, `multiplicateur_degats(attaque)`, `fin_de_tour(pokemon)` |

### modes/
| Classe | Méthodes publiques |
|---|---|
| `ModeSelection(saisie, affichage)` *(abstraite)* | `nom`, `creer_dresseur(nom_joueur) -> Dresseur` |
| `ModeChoisi`, `ModeAleatoire`, `ModePredefini` | idem (polymorphisme) |

### donnees/
| Classe | Méthodes publiques |
|---|---|
| `creer_type_xxx()` (14 fonctions), `creer_tous_les_types()` | renvoient des `TypePokemon` |
| `creer_xxx()` dans `attaques.py` (21) et `pokemons.py` (6), `creer_tous_les_pokemon(niveau)` | renvoient des `Attaque` / `Pokemon` |
| `FabriqueObjets()` | `creer(nom)`, `noms_disponibles()`, `sac_predefini(n)`, `sac_aleatoire()` |
| `EquipePredefinie(nom, description)`, `BibliothequeEquipes()` | `liste()`, `construire(equipe_predefinie)` |

### ui/ et autres
| Classe | Méthodes publiques |
|---|---|
| `Affichage` | `titre()`, `message(t)`, `messages(l)`, `separateur_tour(n)`, `etat_pokemon(p)`, `etat_combat(p1, p2)`, `victoire(nom)`, `erreur(t)` |
| `Menus(saisie, affichage)` | `menu_principal(d)`, `choisir_attaque(d)`, `choisir_pokemon(d)`, `choisir_objet(d)`, `choisir_mode(modes)` |
| `Saisie` | `lire_entier(question, min, max)`, `lire_texte(q)`, `lire_oui_non(q)` |
| `Sprite(lignes)` *(niv. 3)* | `afficher()` |
| `GestionnaireSauvegarde(dossier)` *(niv. 3)* | `sauvegarder(dresseur, fichier)`, `charger(fichier)`, `lister()` |
| `Jeu` | `lancer()` |
| `RecuperateurPokeAPI` *(outil)* | `recuperer_pokemon`, `recuperer_attaque`, `tout_recuperer` |

---

## 4. Règles de dépendance (qui peut importer qui)

```
main  →  jeu  →  { modes, combat, ui, donnees, sauvegarde, modeles }
modes     →  modeles, objets, donnees        (reçoit ui/ en paramètre)
combat    →  modeles, objets                 (reçoit Affichage/Saisie en paramètre)
donnees   →  modeles, objets
ui        →  modeles                         (pour lire un Pokémon et l'afficher)
sauvegarde→  modeles, donnees
objets    →  (modeles seulement pour les annotations de type, dans `if TYPE_CHECKING:`)
modeles   →  exceptions, objets.objet (uniquement sac.py)   JAMAIS combat, ui, modes, donnees
exceptions→  rien
```

Autres règles :
- **Seul `ui/` utilise `print` et `input`.** Le reste renvoie des `str` ou appelle `Affichage`.
- **Aucune variable globale** (pas de variable au niveau du module, hors `import`, classes et fonctions). Les valeurs fixes vont dans un attribut de classe.
- **Aucune logique dans `main.py`.**
- Les Pokémon, attaques et types sont créés uniquement dans `donnees/` (fonctions `creer_xxx()`), jamais depuis un fichier JSON.
- Jamais d'import circulaire : si `A` importe `B`, alors `B` n'importe pas `A`.

### Table d'efficacité des types (à faire valider par le prof)
Solution retenue : **chaque `TypePokemon` contient trois listes de noms de types** (ceux qu'il bat à x2, ceux qui lui résistent à x0,5, ceux qui l'annulent à x0). Tout ce qui n'est dans aucune liste vaut x1. Le type répond à `efficacite_contre(autre_type)` et `efficacite_contre_pokemon(liste_de_types)` (produit des multiplicateurs). Aucun dictionnaire ni variable globale : une fonction `creer_type_xxx()` par type dans `donnees/efficacite.py`. Avantages à dire au prof : encapsulation (le type connaît ses propres règles), code simple, passer à 17 types = ajouter des fonctions. Table vérifiée avec l'historique des types de PokéAPI (14 types, génération 3).

---

## 5. Check-list des contraintes du prof (à vérifier à la fin)

- [ ] Au moins 5 types différents (14 dans le jeu), dont des doubles types
- [ ] Chaque Pokémon : nom, 1 ou 2 types, statistiques, liste d'attaques
- [ ] Dresseur : équipe de 3 Pokémon + sac d'objets
- [ ] Combat tour par tour : attaque / changement / objet (+ abandon)
- [ ] Dégâts tenant compte des types du défenseur (dont double type)
- [ ] Attaques de statut (sans dégâts) : statut ou stat temporaire
- [ ] Pokémon à 0 PV = K.O. et retiré du combat
- [ ] Fin du combat quand une équipe est entièrement K.O.
- [ ] Affichage lisible : qui agit, attaque/objet, effet, PV restants, K.O.
- [ ] Attributs privés (au moins `_pv`)
- [ ] `PokemonKOError`, `ObjetIndisponibleError`, `PVInvalideError` définies **et réellement levées**
- [ ] Aucune variable globale
- [ ] Pokémon / attaque / objet = objets (aucun dict, tuple ou liste pour les représenter)
- [ ] Aucune logique dans `main.py`
- [ ] Code découpé en plusieurs fichiers cohérents
- [ ] `print` uniquement dans `ui/`
- [ ] Tests `unittest` qui passent
- [ ] Formules vérifiées sur les sources (Poképédia, Bulbapedia), pas de mémoire

---

## 6. Glossaire POO

- **Classe** : le plan de construction (ex. `Pokemon`). **Objet** : une réalisation de ce plan (ex. ton Salamèche niveau 12).
- **Attribut** : une donnée stockée dans un objet (ex. `niveau`). **Méthode** : une action de l'objet (ex. `soigner()`).
- **Attribut privé** (`_pv`) : on n'y touche pas depuis l'extérieur ; on passe par une méthode/propriété qui vérifie que la valeur est cohérente. C'est l'**encapsulation**.
- **Héritage** : une classe « fille » reprend ce que fait sa « mère » (`Potion` hérite de `Soin`, qui hérite de `Objet`).
- **Classe abstraite** : une classe qu'on ne crée jamais directement ; elle impose des méthodes aux filles (`Objet.utiliser`).
- **Polymorphisme** : appeler la même méthode sur des objets différents, chacun réagit à sa façon (`action.executer()` marche pour une attaque comme pour un objet).
- **Composition** : un objet **contient** d'autres objets (un `Dresseur` a une `Equipe`, une `Equipe` a des `Pokemon`). Règle : « est un » → héritage, « a un » → composition.
- **Exception** : une erreur qu'on déclenche exprès (`raise PokemonKOError`) et qu'on rattrape (`try/except`) pour que le programme ne plante pas.

---

## 7. Travailler à deux avec Git

- Une branche par personne ou par tâche : `git switch -c prenom/ma-tache`.
- Un fichier = un propriétaire à un instant donné. **Ne modifie pas le fichier de l'autre sans prévenir.** Le contrat (section 3) permet de coder en parallèle : on respecte les signatures.
- Avant de commencer : `git pull`. Commits petits et fréquents : `git commit -m "feat(modeles): PV privés de Pokemon"`.
- Pousse souvent : `git push`. Fusionne sur `main` seulement du code qui **s'exécute** et dont les tests passent.
- En cas de conflit : ne panique pas, ouvre le fichier, garde les deux versions utiles, supprime les `<<<<<<<`/`>>>>>>>`, puis commit. Demande de l'aide si besoin.
- Lancer les tests : `python -m unittest discover -s tests -t .`
