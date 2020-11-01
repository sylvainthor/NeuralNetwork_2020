#!/usr/bin/env python
import tkinter as tk
from datetime import time
from time import sleep
from tkinter import filedialog
import os
import ReseauNeuronal
import SaveNLoad


class Dessin:

    def __init__(self, rn):
        """
        :param = rn : Réseau neuronal
        """
        self.infos = rn.get_infos()
        self.rn = rn
        self.detour = 0
        self.nbrcouche = len(self.infos[1])
        self.nentree = self.infos[0]
        self.nsortie = self.infos[2]
        self.texte = ""
        self.btnEntrainement = ""
        self.choixEntrainement = ""
        self.choix = 0
        self.btnLancerTest = ""
        self.choixTest = ""
        self.choixSortie = ""
        self.taille = 0
        self.root = tk.Tk()
        self.valCheck1 = tk.IntVar(self.root)

        if self.root.winfo_screenwidth() > 1600:
            self.widthInit = 1600
        else:
            self.widthInit = self.root.winfo_screenwidth()
        self.heightInit = self.root.winfo_screenheight() - 40
        dimension = str(self.widthInit) + "x" + str(self.heightInit)
        print("L, H, Dimensions : ", self.widthInit, self.heightInit, dimension)

        self.canvas = tk.Canvas(self.root, width=self.widthInit, height=self.heightInit, bg="#fefee0")
        self.root.geometry(dimension)
        self.canvas.pack()

        self.width = (self.widthInit / 6) * 5
        self.height = (self.heightInit / 5) * 4 - 40

        DivH = self.getNmax()

        if self.nbrcouche > 10:
            self.divisonX = round(self.width / (10 + 3))
        else:
            self.divisonX = round(self.width / (self.nbrcouche + 3))
        """on divise par le nombre de couche + 2 car on ajoute entree sortie """
        """et encore +1 pour avoir n + 1 partie"""

        self.orgaDessin(self.divisonX)
        self.PartieDroite()
        self.root.wm_title("Réseau neuronal")
        tk.mainloop()

    def getNmax(self):
        # liste = [self.nentree, max(self.infos[1]), self.nsortie]
        liste = self.infos[1][:]
        liste.append(self.nentree)
        liste.append(self.nsortie)

        if max(liste) > 10:
            return 10
        else:
            return max(liste)

    def orgaDessin(self, divisonX):
        sauvcouche = sauventree = sauvesortie = sauvenbr = 0

        self.taille = self.height / (self.getNmax() * 2)

        if self.nentree > 10:
            sauventree = self.nentree
            self.pointille(2, self.divisonX, 1, sauventree)
            self.nentree = 10
        if max(self.infos[1]) > 10:
            sauvcouche = max(self.infos[1])
            self.taillemax = 10

        if self.nbrcouche > 10:
            sauvenbr = self.nbrcouche
            detour = 1
            self.nbrcouche = 10

        if self.nsortie > 10:
            sauvesortie = self.nsortie
            self.pointille(3, self.divisonX, self.nbrcouche + 2, sauvesortie)
            self.nsortie = 10

        avancement = 0
        while avancement < len(self.infos[1]):
            if self.infos[1][avancement] > 10:
                self.pointille(1, self.divisonX, avancement + 2, self.infos[1][avancement])
            avancement = avancement + 1

        self.dessinerCercle(self.nentree, divisonX)
        self.dessinerLineEntree(divisonX)
        i = 0
        if len(self.infos[1]) > 10:
            tailleC = 10
        else:
            tailleC = len(self.infos[1])
        while i < tailleC:
            n = self.infos[1][i]
            i = i + 1
            self.dessinerCercle(n, divisonX * (i + 1))
        self.dessinerCercle(self.nsortie, divisonX * (self.nbrcouche + 2))

        self.canvas.create_line((self.widthInit / 6) * 5, 0, (self.widthInit / 6) * 5,
                                self.heightInit, width=1)
        self.canvas.create_line(0, (self.heightInit / 5) * 4 - 40, (self.widthInit / 6) * 5,
                                (self.heightInit / 5) * 4 - 40, width=1)
        self.canvas.create_rectangle(10, (self.heightInit / 5) * 4 - 25,
                                     ((self.widthInit / 6) * 5) - 10, self.heightInit - 10, fill="#708d23")
        if self.detour == 1:
            self.setText4(sauvenbr)

    def dessinerCercle(self, nombre, divisionX):
        if nombre > 10:
            nombre = 10
        divisionY = self.height / (nombre + 1)

        multi = 1
        x = 0
        x0 = x1 = divisionX
        taille2 = self.taille / 2

        while x < nombre:
            self.canvas.create_oval(x0 - self.taille, (multi * divisionY) - taille2, x1, (divisionY * multi) + taille2,
                                    fill="#476042")
            x = x + 1
            multi = multi + 1

    def dessinerLineEntree(self, divisionX):
        lesmatrices = self.rn.get_matrices()
        tmp = divisionX
        tab_CC = self.infos[1].copy()
        tab_CC.insert(0, self.infos[0])
        tab_CC.append(self.infos[2])
        isShort = False
        if len(tab_CC) > 10:
            tab_CC = tab_CC[:11]
            tab_CC.append(self.infos[2])
            isShort = True
        for a in range(1, len(tab_CC)):
            if a == len(tab_CC) - 1 and isShort:
                pass
            else:
                petiteMat = lesmatrices[a - 1].get_matrice()
                divisionX = tmp * a
                divisionX2 = tmp * (a + 1)

                nbrtour = tab_CC[a - 1] + 1
                nbrtour2 = tab_CC[a] + 1

                if nbrtour > 10:
                    nbrtour = 11
                if nbrtour2 > 10:
                    nbrtour2 = 11

                divisionY = self.height / nbrtour
                divisionY2 = self.height / nbrtour2
                for x in range(1, nbrtour):
                    for y in range(1, nbrtour2):
                        if petiteMat[y - 1][x - 1] < 0:
                            self.canvas.create_line(divisionX, divisionY * x, divisionX2 - (self.taille / 2),
                                                    divisionY2 * y,
                                                    width=1 + -2 * petiteMat[y - 1][x - 1], fill="#EF1414")
                        else:
                            self.canvas.create_line(divisionX, divisionY * x, divisionX2 - (self.taille / 2),
                                                    divisionY2 * y,
                                                    width=1 + 2 * petiteMat[y - 1][x - 1], fill="#1482EF")

    def pointille(self, choix, divi, place, sauvC):  # ajouter taille pour enelever les 25 50 ...
        hauteur = self.height / (10 + 1)
        tmp = divi

        if choix == 1:  # couche cachée
            divX = tmp * place
            divY = 9 * hauteur
            divY2 = 10 * hauteur
            self.canvas.create_line(divX - (self.taille / 2), divY + self.taille / 5, divX - (self.taille / 2), divY2,
                                    fill="#EF1414",
                                    width=5, dash=(4, 4))
            self.canvas.create_text(divX - self.taille, divY2 + self.taille, text=sauvC, fill="#EF1414")

        if choix == 2:  # entree
            divX = tmp * place
            divY = 9 * hauteur
            divY2 = 10 * hauteur
            self.canvas.create_line(divX - (self.taille / 2), divY + (self.taille / 3), divX - (self.taille / 2), divY2,
                                    fill="#EF1414",
                                    width=5, dash=(4, 4))
            self.canvas.create_text(divX - (self.taille / 2), divY2 + (self.taille), text=sauvC, fill="#EF1414")

        if choix == 3:  # sortie
            divX = tmp * place
            divY = 9 * hauteur
            divY2 = 10 * hauteur
            self.canvas.create_line(divX - (self.taille / 2), divY + (self.taille / 3), divX - (self.taille / 2), divY2,
                                    fill="#EF1414",
                                    width=5, dash=(4, 4))
            self.canvas.create_text(divX - (self.taille / 2), divY2 + self.taille, text=sauvC, fill="#EF1414")

    def terminal(self):
        self.canvas.create_rectangle(10, (self.heightInit / 5) * 4 - 25,
                                     ((self.widthInit / 6) * 5) - 10,
                                     self.heightInit - 10, fill="#708d23")
        self.canvas.create_text((self.widthInit / 6) * 2, self.height + self.height / 8, text=self.texte,
                                font=('comicsans', 14))

    def setText(self, choix):
        if choix == 1:
            self.texte = "Réseau entrainé"
        if choix == 2:
            self.texte = "Test effectué"
        else:
            self.texte = ""
        self.terminal()

    def setText2(self, text):
        self.texte = "Vous avez choisi :" + text
        self.terminal()

    def setText3(self, text):
        self.texte = "Erreur : " + text
        self.terminal()

    def setTextTerminal(self, texte):
        self.texte = texte
        self.terminal()

    def setText4(self, ncct):
        self.texte = "Nombre de couches cachées au total : " + str(ncct) + " (car > 10) "
        self.terminal()

    def PartieDroite(self):
        hauteur = self.height / 12
        # ligne option
        self.canvas.create_text(self.width + ((self.widthInit / 6) / 2), hauteur, text="Options",
                                font=('comicsans', 14))

        # bouton choix fichier entrainement
        self.btnEntrainement = tk.Button(self.root, text="Choisir un entrainement", command=self.GetFilesE)
        btnEntrainement_w = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 2,
                                                      window=self.btnEntrainement)

        # ligne option
        self.canvas.create_text(self.width + ((self.widthInit / 6) / 2), hauteur * 3, text="Lancer entrainement :",
                                font=('comicsans', 14))

        # checkbox choix
        """ Recuperer les valeurs des checkbox"""

        # check1 = tk.Checkbutton(self.root, text="Coup par coup", command=self.changerValCheck1)
        check1 = tk.Radiobutton(self.root, text="Coup par coup", variable=self.valCheck1, value=1, bg="#fefee0")
        c1_w = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 4, window=check1)

        # check2 = tk.Checkbutton(self.root, text="En un coup", command=self.changerValCheck2)
        check2 = tk.Radiobutton(self.root, text="En un coup", variable=self.valCheck1, value=2, bg="#fefee0")
        c2_w = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 5, window=check2)

        self.btnvalider = tk.Button(self.root, text="Valider", command=self.Choix)
        btn_valider = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 6,
                                                window=self.btnvalider)

        # bouton choix fichier test
        self.btnTest = tk.Button(self.root, text="Choisir fichier test", command=self.GetFilesT)
        btnTest_w = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 7, window=self.btnTest)

        # bouton choix fichier reception
        self.btnReception = tk.Button(self.root, text="Fichier reception", command=self.GetFilesR)
        btnReception_w = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 8,
                                                   window=self.btnReception)

        # Lancer test
        self.lancerTest = tk.Button(self.root, text="Lancer le test", command=self.LancerTest)
        lancerTest_w = self.canvas.create_window(self.width + ((self.widthInit / 6) / 2), hauteur * 9,
                                                 window=self.lancerTest)

    def GetFilesE(self):
        filename = filedialog.askopenfilename()
        self.choixEntrainement = filename
        self.setText2(self.choixEntrainement)
        self.btnEntrainement.config(state=tk.DISABLED)

    def GetDirE(self):
        dirname = filedialog.askdirectory()
        self.choixEntrainement = dirname

    def GetFilesT(self):
        filename = filedialog.askopenfilename()
        self.choixTest = filename
        self.setText2(self.choixTest)
        self.btnTest.config(state=tk.DISABLED)

    def GetFilesR(self):
        filename = filedialog.askopenfilename()
        self.choixSortie = filename
        self.setText2(self.choixSortie)
        self.btnReception.config(state=tk.DISABLED)

    def Choix(self):
        print(self.valCheck1)
        if self.valCheck1.get() == 1:
            print("coup par coup")
            self.setText2(" Coup par coup")
            self.choix = 1
        else:
            print("un coup")
            self.setText2(" En un coup")
            self.choix = 2
        self.btnvalider.config(state=tk.DISABLED)
        self.setTextTerminal("Test1")
        self.LancerEntrainement()

    def LancerEntrainement(self):
        self.setTextTerminal("Test2")
        if self.choix == 1:
            self.CoupParCoup()
        else:
            self.UnCoup()

    def CoupParCoup(self):
        print("coup par coup")
        poid = len(open(self.choixEntrainement, "r+").readlines())
        i = 0
        lenght = poid//100
        for i in range(0, (poid//lenght)-1):
            self.setTextTerminal("Progression : " + str(round((i*lenght) / poid * 100, 4)) + "%")
            self.canvas.update_idletasks()
            self.rn.entrainer_avec_fichier(self.choixEntrainement, i * lenght, (i+1)*lenght)
            self.refreshDessin()
        self.rn.entrainer_avec_fichier(self.choixEntrainement, (i + 1) * lenght)
        self.setTextTerminal("Entrainement fini !")

        self.btnvalider.config(state=tk.ACTIVE)
        self.btnEntrainement.config(state=tk.ACTIVE)

    def UnCoup(self):
        print("un coup")
        self.setTextTerminal("Entrainement se lance ...")
        self.rn.entrainer_avec_fichier(self.choixEntrainement)
        self.refreshDessin()
        self.setTextTerminal("Entrainement fini !")
        self.btnvalider.config(state=tk.ACTIVE)
        self.btnEntrainement.config(state=tk.ACTIVE)

    def refreshDessin(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#fefee0")
        self.orgaDessin(self.divisonX)

    def LancerTest(self):
        self.setTextTerminal("Mise à jour en cours ...")
        self.rn.mettre_a_jour_avec_enregistrement(self.choixTest, self.choixSortie)
        self.setTextTerminal("Mise à jour finie !")


def main():
    snl = SaveNLoad.SaveNLoad()
    rn = snl.load("sauvegardes/0.916")
    # rn = ReseauNeuronal.ReseauNeuronal(4, [2, 2], 1)
    dessin = Dessin(rn)


if __name__ == '__main__':
    main()
