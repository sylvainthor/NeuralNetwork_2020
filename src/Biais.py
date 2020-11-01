#!/usr/bin/env python
import Formules
import Element


class Biais(Element.Element):

    def __init__(self, force):
        Element.Element.__init__(self)
        self.valeur = force
        self.formules = Formules.Formules()

    def calcul_valeur(self, matrice, valeur_neurones):
        pass


def main():
    n = Biais(1)
    n.set_valeur(2)
    n.calcul_valeur([5, 5], [2, 2])
    print(n.get_valeur())


if __name__ == '__main__':
    main()
