#!/usr/bin/env python
import Formules
import Element


class Neurone(Element.Element):

    def __init__(self):
        Element.Element.__init__(self)
        self.valeur = 0
        self.formules = Formules.Formules()
        self.somme = 0

    def calcul_valeur(self, matrice, valeur_neurones):
        self.somme = 0
        for i in range(0, len(valeur_neurones)):
            self.somme += matrice[i]*valeur_neurones[i]
        # fonction à appliquer :
        self.set_valeur(self.formules.sigmoide(self.somme))


def main():
    n = Neurone()
    n.set_valeur(2)
    n.calcul_valeur([0.5, 0.5], [2, 2])
    print(n.get_valeur())


if __name__ == '__main__':
    main()
