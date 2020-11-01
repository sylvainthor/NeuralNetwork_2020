#!/usr/bin/env python
import Formules


class Element:

    def __init__(self):
        self.valeur = 0
        self.formules = Formules.Formules()
        self.somme = 0

    def get_valeur(self):
        return self.valeur

    def get_somme(self):
        return self.somme

    def set_valeur(self, valeur):
        self.valeur = valeur

    def calcul_valeur(self, matrice, valeur_neurones):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
