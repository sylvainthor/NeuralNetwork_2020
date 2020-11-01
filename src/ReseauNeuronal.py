#!/usr/bin/python

import CoucheNeuronale
import MatriceLiaisons
import Formules
import SaveNLoad
import operator
from random import randint


class ReseauNeuronal:
    """
    Classe représentant le Reseau Neuronale dans son entièreté
    """

    def __init__(self, nE, tab_cc, nS, hasBiais=True, biaisForce=1, degree_erreur=1.0):
        if type(nE) is not int or type(nS) is not int or type(tab_cc) is not list:
            raise TypeError('Bad type')
        for x in tab_cc:
            if type(x) is not int:
                raise TypeError('Bad type of list')
            if x < 1:
                raise ValueError('Couche de neurones ne peut pas etre négative')
        if nE < 1:
            raise ValueError('Nombre de neurones d\'entree doit etre superieur a 1')
        if nS < 1:
            raise ValueError('Nombre de neurones de sortie doit etre superieur a 1')
        if type(degree_erreur) is not int and type(degree_erreur) is not float:
            raise TypeError('degree_erreur mauvais type')
        if degree_erreur < 0:
            raise ValueError('degree_erreur ne peux pas être négatif')
        if type(hasBiais) is not bool:
            raise TypeError('hasBiais doit etre un boolean')

        self.degree_erreur = degree_erreur
        self.mesCouches = []
        self.mesMatrices = []
        self.hasBiais = hasBiais
        self.biaisForce = biaisForce
        self.formules = Formules.Formules()
        self.nNeuroneE = nE
        self.nNeuroneS = nS
        self.tab_CC = tab_cc
        self.mesCouches.append(CoucheNeuronale.CoucheNeuronale(nE, hasBiais, biaisForce))
        for i in range(0, len(tab_cc)-1):
            self.mesCouches.append(CoucheNeuronale.CoucheNeuronale(tab_cc[i], hasBiais, biaisForce))
        self.mesCouches.append(CoucheNeuronale.CoucheNeuronale(tab_cc[len(tab_cc)-1]))
        self.mesCouches.append(CoucheNeuronale.CoucheNeuronale(nS))
        for i in range(0, len(self.mesCouches) - 1):
            self.mesMatrices.append(MatriceLiaisons.MatriceLiaisons(self.mesCouches[i].get_nb_element(),
                                                                    self.mesCouches[i + 1].get_nb_neurones()))

    def entrainer(self, entrees, target):
        """
        Fonction qui permet aà l'utilisateur de donner des entrees
        et dire quel resultat doit etre obtenu, ces deux informations
        permettront à un algorithme de corriger les poids des matrices
        en fonction de leur participation à l'erreur ou la reussite
        afin de faire evoluer le reseaux
        @param entrees: tableau designant les entrees à inserer dans le reseaux
        @param target: tableau designant le resultat souhaitez
        """

        if type(entrees) is not list or type(target) is not list:
            raise TypeError('Entrees ou target de mauvais type')
        for x in entrees:
            if type(x) is not int and type(x) is not float:
                raise TypeError('valeurs d\'entrées du mauvais type')
        for x in target:
            if type(x) is not int and type(x) is not float:
                raise TypeError('valeurs des sorties du mauvais type')
        if len(entrees) != self.mesCouches[0].get_nb_neurones():
            raise ValueError('Tableau entrees mauvaise longueur')
        if len(target) != self.mesCouches[len(self.mesCouches) - 1].get_nb_neurones():
            raise ValueError('Tableau entrees mauvaise longueur')

        sortie = self.mettre_a_jour(entrees)
        # calcul de l'erreur
        erreur = []
        for i in range(0, len(target)):
            erreur.append(sortie[i] - target[i])

        # affichage du poids total de l'erreur
        """
        somme_erreur = 0
        for j in range(0, len(erreur)):
            somme_erreur = somme_erreur + erreur[j]
        print(somme_erreur)
        """

        for i in reversed(range(1, len(self.mesCouches))):
            neurone = self.mesCouches[i].get_neurones()
            neurone_suivants = self.mesCouches[i - 1].get_element()
            matrice = self.mesMatrices[i - 1].get_matrice()
            tab_dEdx = []
            for j in range(0, len(neurone)):
                dEdx = self.formules.sigmoide(neurone[j].get_somme()) * (
                        1 - self.formules.sigmoide(neurone[j].get_somme())) * erreur[j]
                for k in range(0, len(neurone_suivants)):
                    dEdW = neurone_suivants[k].get_valeur() * dEdx
                    matrice[j][k] = matrice[j][k] - self.degree_erreur * dEdW
                tab_dEdx.append(dEdx)
            erreur = []
            for k in range(0, len(neurone_suivants)):
                erreur.append(0)
                for m in range(0, len(neurone)):
                    erreur[k] = erreur[k] + tab_dEdx[m] * matrice[m][k]

    def mettre_a_jour(self, entrees):
        """
        Permet de tester le reseaux
        @param entrees: les entrees du reseau neuronal
        @return: le resultat obtenu
        """

        if type(entrees) is not list:
            raise TypeError('Bad type')
        for x in entrees:
            if type(x) is not int and type(x) is not float:
                raise TypeError('Bad type')
        if len(entrees) != self.mesCouches[0].get_nb_neurones():
            raise ValueError('Lenght of tab not correct')

        self.mesCouches[0].set_valeur(entrees)
        for i in range(1, len(self.mesCouches)):
            self.mesCouches[i].calculer_valeur_neurones(self.mesMatrices[i - 1],
                                                        self.mesCouches[i - 1].get_valeur())
        return self.mesCouches[len(self.mesCouches) - 1].get_valeur()

    def print_reseau(self):
        """
        Affichage simple du reseau neuronal
        """
        i = 0
        for couche in self.mesCouches:
            i += 1
            print("n:", couche.get_valeur())
            for j in couche.get_neurones():
                print(j.get_somme(), end=' ')
            print()
            if i != len(self.mesCouches):
                print("m:", self.mesMatrices[i - 1].get_matrice())

    def get_infos(self):
        return [self.nNeuroneE, self.tab_CC, self.nNeuroneS, self.hasBiais, self.biaisForce]

    def get_matrices(self):
        return self.mesMatrices

    def set_matrices(self, matrices):
        self.mesMatrices = matrices

    def entrainer_avec_fichier(self, fileName, start=-1, end=-1):
        """
        Cette fonction permet d'entrainer le reseau en lui donnant le nom d'un fichier d'entrainement
        un fichier d'entrainement est un fichier de type .csv qui contient une entrée par ligne
        la première ligne décrit le fichier
        le reste des lignes contient d'abord les valeurs de sortie voulues et ensuite les valeurs
        d'entrées toute séparés par des virgules.
        Start et end servent a entrainer le reseaux par morçeaux pour par exemple estimer le temps
        nécessaire en lançant une partie de l'entrainement seulement.
        Si Start est à -1 on commence du début et si End est à -1 on va jusqu'au bout
        @param fileName: le nom du fichier d'entrainement
        @param start: où commencer l'entrainement dans le fichier donné
        @param end: où finir l'entrainement
        """
        if type(fileName) is not str:
            raise TypeError('Bad Type')
        if fileName.split('.')[1] != "csv":
            raise ValueError('Fichier pas de type : filename.csv')
        if type(start) is not int:
            raise TypeError('Start pas int')
        if type(end) is not int:
            raise TypeError('End pas int')

        f = open(fileName, "r+")
        lines = f.readlines()
        lines.pop(0)
        if end == -1:
            end = len(lines)
        if start == -1:
            start = 0
        if end < 0 or end < start or end > len(lines):
            raise ValueError('Fin de fichier impossible')
        if start < 0:
            raise ValueError('Début de fichier impossible')
        for i in range(start, end):
            line = lines[i]
            values = line.split(',')
            entrees = []
            sorties = []
            for j in range(0, self.nNeuroneS):
                sorties.append(float(values[j]))
            for j in range(self.nNeuroneS, self.nNeuroneS + self.nNeuroneE):
                entrees.append(float(values[j]))
            self.entrainer(entrees, sorties)

    def mettre_a_jour_avec_enregistrement(self, testing_file, result_file, start=-1, end=-1):
        if type(testing_file) is not str:
            raise TypeError('Bad Type')
        if testing_file.split('.')[1] != "csv":
            raise ValueError('Fichier pas de type : filename.csv')
        if type(result_file) is not str:
            raise TypeError('Bad Type')
        if result_file.split('.')[1] != "csv":
            raise ValueError('Fichier pas de type : filename.csv')
        if type(start) is not int:
            raise TypeError('Start pas int')
        if type(end) is not int:
            raise TypeError('End pas int')

        file_test = open(testing_file, "r+")
        file_result = open(result_file, "w+")
        lines = file_test.readlines()
        lines.pop(0)
        if end == -1:
            end = len(lines)
        if start == -1:
            start = 0
        if end < 0 or end < start or end > len(lines):
            raise ValueError('Fin de fichier impossible')
        if start < 0:
            raise ValueError('Début de fichier impossible')

        for i in range(start, end):
            line = lines[i]
            values = line.split(',')
            entrees = []
            for j in range(0, self.nNeuroneE):
                entrees.append(float(values[j]))
            results = self.mettre_a_jour(entrees)
            results = [str(x) for x in results]
            resultats = ",".join(results)
            file_result.write(resultats + '\n')


def endespi(m):
    # m.entrainer_avec_fichier("fichier_entrainement/adapted_train.csv")
    f = open("fichier_entrainement/adapted_train.csv", "r+")
    the_lines = f.readlines()
    nombre_de_reussites = 0
    for i in range(0, 1000):
        print(i)
        line = the_lines[randint(1, len(the_lines) - 1)]
        line = line.split(',')
        nb = int(line[0])
        tmp = []
        for j in range(1, len(line)):
            tmp.append(float(line[j]) / 255)
        tmp = m.mettre_a_jour(tmp)
        max_value = max(tmp)
        max_index = tmp.index(max_value)
        if nb == max_index:
            nombre_de_reussites += 1
    print("nb de reussites = ", nombre_de_reussites / 1000)


def main():
    snl = SaveNLoad.SaveNLoad()
    m = snl.load("sauvegardes/0.916")
    print(m.get_infos())
    endespi(m)


if __name__ == '__main__':
    main()
