#!/usr/bin/env python

import ReseauNeuronal
import MatriceLiaisons


class SaveNLoad:
    """
    Classe permettant la sauvegarde de reseau neuronale dans un fichier
    ou l'obtention d'un reseaux neuronale précédemment sauvagarder dans un fichier
    """

    def __init__(self):
        pass

    def save(self, name_of_file, Neu_Net):
        if type(name_of_file) is not str or type(Neu_Net) is not ReseauNeuronal.ReseauNeuronal:
            raise TypeError('Bad type')

        f = open(name_of_file, "w+")
        f.write('Sauvegarde Reseau Neuronale' + '\n')

        # Recuperation des paramètres du Reseau et on les écrit
        infos = Neu_Net.get_infos()
        f.write(str(infos[0]) + '\n')
        for i in range(0, len(infos[1])):
            f.write(str(infos[1][i]) + ' ')
        f.write('\n')
        f.write(str(infos[2]) + '\n')
        f.write(str(infos[3]) + ' ' + str(infos[4]) + '\n')

        # Maintenant le principal les Matrices:
        f.write('Matrices : \n')

        matriceLi = Neu_Net.get_matrices()
        for i in range(0, len(matriceLi)):
            matrice = matriceLi[i].get_matrice()
            f.write(str(len(matrice)) + ' ')
            f.write(str(len(matrice[0])) + '\n')

            for j in range(0, len(matrice)):
                for k in range(0, len(matrice[0])):
                    f.write(str(matrice[j][k]) + ' ')
                f.write('\n')

    def load(self, name_of_file):
        print("Réseau chargé")
        f = open(name_of_file, "r+")
        the_lines = f.readlines()

        nI = int(the_lines[1])
        tab_CC = []
        tmp = the_lines[2].split(' ')
        for i in range(0, len(tmp) - 1):
            tab_CC.append(int(tmp[i]))
        nS = int(the_lines[3])
        tmp = the_lines[4].split(' ')
        hasBiais = bool(tmp[0])
        biaisForce = int(tmp[1])
        rn = ReseauNeuronal.ReseauNeuronal(nI, tab_CC, nS, hasBiais, biaisForce)

        les_matrices = []
        i = 6
        while i < len(the_lines):
            line = the_lines[i]
            x = int(line.split(' ')[0])
            y = int(line.split(' ')[1])
            object_matrice = MatriceLiaisons.MatriceLiaisons(x, y)
            matrice = []
            for j in range(0, x):
                matrice.append([])
                i += 1
                valeurs = the_lines[i].split(' ')
                for k in range(0, y):
                    matrice[j].append(float(valeurs[k]))
            object_matrice.set_matrice(matrice)
            les_matrices.append(object_matrice)
            i += 1
        rn.set_matrices(les_matrices)
        return rn


def main():
    rn = ReseauNeuronal.ReseauNeuronal(2, [4, 4, 4], 1)
    print(rn.mettre_a_jour([0, 1]))
    snl = SaveNLoad()
    snl.save("sauvegardes/saveTest", rn)
    print("sauvegarde faite")

    snl = SaveNLoad()
    rn1 = snl.load("sauvegardes/saveTest")
    print(rn1.mettre_a_jour([0, 1]))


if __name__ == '__main__':
    main()
