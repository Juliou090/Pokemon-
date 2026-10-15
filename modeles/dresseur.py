"""Le dresseur et ce qu'il possède : une équipe de Pokémon (Equipe) et un sac d'objets (Sac).

J'ai mis ces classes dans le même fichier parce qu'elles vont toujours ensemble.
Equipe.TAILLE est un attribut de classe : pour passer à 6 Pokémon par équipe, je n'ai
que ce nombre à changer.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

from exceptions import (
    ActionInvalideError,
    DonneesInvalidesError,
    ObjetIndisponibleError,
    PokemonKOError,
)


class Equipe:
    # Attribut de CLASSE : pour passer à 6 Pokémon, on ne change que ce nombre.
    TAILLE = 3

    def __init__(self, pokemons):
        if len(pokemons) != Equipe.TAILLE:
            raise DonneesInvalidesError("Une équipe a " + str(Equipe.TAILLE) + " Pokémon.")

        self.pokemons = pokemons
        self.indice_actif = 0

    def actif(self):
        return self.pokemons[self.indice_actif]

    def vivants(self):
        liste = []

        for pokemon in self.pokemons:
            if not pokemon.est_ko():
                liste.append(pokemon)

        return liste

    def est_vaincue(self):
        return len(self.vivants()) == 0

    def verifier_changement(self, indice):
        """Lève une exception si on ne peut pas envoyer ce Pokémon."""
        pokemon = self.pokemons[indice]

        if pokemon.est_ko():
            raise PokemonKOError(pokemon.nom + " est K.O. : impossible de l'envoyer.")

        if indice == self.indice_actif:
            raise ActionInvalideError(pokemon.nom + " est déjà au combat !")

    def changer_actif(self, indice):
        """Envoie le Pokémon n°indice au combat. Il remet à zéro les paliers du sortant."""
        self.verifier_changement(indice)

        for nom_stat in self.actif().paliers:
            self.actif().paliers[nom_stat] = 0

        self.indice_actif = indice

        return self.actif()

    def soigner_tous(self):
        """Fin de combat : tous les Pokémon sont soignés."""
        for pokemon in self.pokemons:
            pokemon.soigner_completement()

        self.indice_actif = 0


class LigneSac:
    """Un objet et son nombre d'exemplaires."""

    def __init__(self, objet, quantite):
        self.objet = objet
        self.quantite = quantite


class Sac:
    def __init__(self):
        # Les objets épuisés restent dans le sac (x0) : on voit ce qu'on a utilisé,
        # et en choisir un lève ObjetIndisponibleError.
        self.lignes = []

    def ajouter(self, objet, quantite):
        self.lignes.append(LigneSac(objet, quantite))

    def trouver(self, nom_objet):
        """Renvoie l'objet SANS le retirer. Lève ObjetIndisponibleError s'il n'y en a plus."""
        for ligne in self.lignes:
            if ligne.objet.nom == nom_objet and ligne.quantite > 0:
                return ligne.objet

        raise ObjetIndisponibleError("Tu n'as plus de " + nom_objet + " !")

    def retirer(self, nom_objet):
        """Retire un exemplaire (lève ObjetIndisponibleError s'il n'y en a plus)."""
        self.trouver(nom_objet)

        for ligne in self.lignes:
            if ligne.objet.nom == nom_objet:
                ligne.quantite = ligne.quantite - 1


class Dresseur:
    def __init__(self, nom, equipe, sac):
        self.nom = nom
        self.equipe = equipe
        self.sac = sac
        self.a_abandonne = False

    def pokemon_actif(self):
        return self.equipe.actif()

    def a_perdu(self):
        return self.a_abandonne or self.equipe.est_vaincue()

    def verifier_objet(self, nom_objet, cible):
        """Vérifie sans consommer : ObjetIndisponibleError ou ActionInvalideError."""
        self.sac.trouver(nom_objet).verifier(cible)

    def utiliser_objet(self, nom_objet, cible):
        """Utilise un objet du sac sur un Pokémon de l'équipe. Renvoie la phrase.

        Je vérifie AVANT de retirer l'objet du sac : s'il est refusé, il n'est
        pas consommé.
        """
        objet = self.sac.trouver(nom_objet)
        objet.verifier(cible)
        self.sac.retirer(nom_objet)

        return objet.utiliser(cible)
