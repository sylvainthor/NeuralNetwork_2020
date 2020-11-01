#!/usr/bin/env python
import random


class MatriceLiaisons:
    """
    Classe representant les matrices contenant les poids qui definissent le reseaux neuronale
    """
    def __init__(self, x, y):
        if type(x) is not int or type(y) is not int:
            raise TypeError('Bad type')

        self.matrice = []
        for i in range(0, y):
            self.matrice.append([])
            for j in range(0, x):
                self.matrice[i].append(random.uniform(-1.0, 1.0))

    def get_matrice(self):
        return self.matrice

    def set_matrice(self, matrice):
        if type(matrice) is not list:
            raise TypeError('Bad type')
        for x in matrice:
            if type(x) is not list:
                raise TypeError('Bad type')
        for ligne in matrice:
            for x in ligne:
                if type(x) is not int and type(x) is not float:
                    raise TypeError('Bad type')
        self.matrice = matrice


# test :
def main():
    m = MatriceLiaisons(2, 2)
    n = MatriceLiaisons(2, 2)
    print(str(m.get_matrice()))
    print(str(n.get_matrice()))


if __name__ == '__main__':
    main()
