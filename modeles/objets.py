"""Les objets : soins, rappels, guérisons et objets tenus.

Choix : une classe Objet « de base » et quatre classes filles. Chaque fille
redéfinit verifier() (« est-ce que ça sert à quelque chose ? ») et utiliser()
(« je l'applique »). Le combat appelle objet.utiliser(cible) sans savoir si
c'est une potion ou un rappel. Pour avoir « Potion », « Super Potion »... je
n'ai pas fait une classe par potion : un Soin reçoit simplement ses PV.
S'il y a un @ que l'on ne connaît pas : tout est expliqué dans GUIDE_PYTHON.md.
"""

from exceptions import ActionInvalideError


class Objet:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

    def verifier(self, cible):
        """Lève ActionInvalideError si l'objet serait inutile sur cette cible.
        On l'appelle AVANT de consommer l'objet : un objet refusé n'est pas perdu."""

    def utiliser(self, cible):
        """Applique l'objet et renvoie la phrase à afficher."""
        return ""


class Soin(Objet):
    """Rend des PV (tous si pv_rendus vaut None)."""

    def __init__(self, nom, pv_rendus):
        if pv_rendus is None:
            description = "Rend tous les PV."
        else:
            description = "Rend " + str(pv_rendus) + " PV."

        super().__init__(nom, description)
        self.pv_rendus = pv_rendus

    def verifier(self, cible):
        if cible.est_ko():
            raise ActionInvalideError(cible.nom + " est K.O. : il faut un Rappel !")

        if cible.get_pv() == cible.pv_max:
            raise ActionInvalideError(cible.nom + " a déjà tous ses PV.")

    def utiliser(self, cible):
        self.verifier(cible)

        quantite = self.pv_rendus
        if quantite is None:
            quantite = cible.pv_max

        rendus = cible.soigner(quantite)

        return cible.nom + " récupère " + str(rendus) + " PV."


class Rappel(Objet):
    """Ranime un Pokémon K.O. avec un pourcentage de ses PV (50 ou 100)."""

    def __init__(self, nom, pourcentage):
        super().__init__(nom, "Ranime un K.O. (" + str(pourcentage) + " % des PV).")
        self.pourcentage = pourcentage

    def verifier(self, cible):
        if not cible.est_ko():
            raise ActionInvalideError(cible.nom + " n'est pas K.O. : aucun effet.")

    def utiliser(self, cible):
        self.verifier(cible)
        pv = cible.ranimer(self.pourcentage)

        return cible.nom + " est ranimé avec " + str(pv) + " PV !"


class Guerison(Objet):
    """Soigne un statut (identifiant_statut="poison"...) ou tous (None)."""

    def __init__(self, nom, identifiant_statut, description):
        super().__init__(nom, description)
        self.identifiant_statut = identifiant_statut

    def verifier(self, cible):
        if cible.est_ko():
            raise ActionInvalideError(cible.nom + " est K.O. : objet inutile.")

        if cible.statut is None:
            raise ActionInvalideError(cible.nom + " n'a aucun statut.")

        if self.identifiant_statut is None:
            return

        if cible.statut.identifiant != self.identifiant_statut:
            raise ActionInvalideError(self.nom + " ne soigne pas ce statut.")

    def utiliser(self, cible):
        self.verifier(cible)
        ancien_statut = cible.statut
        cible.statut = None

        return cible.nom + " n'est plus " + ancien_statut.nom + " !"


class ObjetTenu(Objet):
    """Objet donné à un Pokémon avant le combat. effet vaut "restes",
    "bandeau" ou "baie". Il agit tout seul, il ne s'utilise pas depuis le sac."""

    def __init__(self, effet):
        if effet == "restes":
            super().__init__("Restes", "Rend 1/16 des PV à chaque tour.")
        elif effet == "bandeau":
            super().__init__("Bandeau Choix", "Attaque +50 %.")
        else:
            super().__init__("Baie Sitrus", "Rend 30 PV sous la moitié des PV.")

        self.effet = effet

    def verifier(self, cible):
        raise ActionInvalideError(self.nom + " s'équipe avant le combat.")

    def pourcentage_stat(self, nom_stat):
        """Le Bandeau Choix augmente l'Attaque de 50 %."""
        if self.effet == "bandeau" and nom_stat == "attaque":
            return 150

        return 100

    def fin_de_tour(self, porteur):
        """Effet de fin de tour. Renvoie une phrase, ou "" s'il ne se passe rien."""
        if porteur.est_ko():
            return ""

        if self.effet == "restes" and porteur.get_pv() < porteur.pv_max:
            quantite = porteur.pv_max // 16

            if quantite < 1:
                quantite = 1

            porteur.soigner(quantite)
            return porteur.nom + " récupère un peu de PV grâce à ses Restes."

        # Baie Sitrus : génération 3, sous la moitié des PV, 30 PV puis elle disparaît.
        if self.effet == "baie" and porteur.get_pv() * 2 < porteur.pv_max:
            rendus = porteur.soigner(30)
            porteur.objet_tenu = None
            return porteur.nom + " mange sa Baie Sitrus et récupère " + str(rendus) + " PV !"

        return ""
