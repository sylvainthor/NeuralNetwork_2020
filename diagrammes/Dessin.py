#!/usr/bin/env python
import builtins

import tkinter as tk


class Dessin:
    nbrcouche = nentree = ncouche = nsortie = 0

    def __init__(self, nbrcouche, nentree, ncouche, nsortie):
        """
        :param = nbrcouche : nombres de couches;
        :param = nentree : nombres n entrees;
        :param = ncouche : ombres n par couche;
        :param = nsortie : nbr n sortie;
        """
        root = tk.Tk()

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()-40
        dimension = str(width) + "x" + str(height)
        print("L, H, Dimensions : ", width, height, dimension)

        canvas = tk.Canvas(root, width=width, height=height)
        root.geometry(dimension)
        canvas.pack()

        DivH = getNmax(nentree, ncouche, nsortie)

        if nbrcouche > 10:
            divisonX = round(width / (10 + 3))
        else:
            divisonX = round(width / (nbrcouche + 3))
        """on divise par le nombre de couche + 2 car on ajoute entree sortie """
        """et encore +1 pour avoir n + 1 partie"""
        # print(divisonX)

        orgaDessin(canvas, nentree, divisonX, height, ncouche, nsortie, nbrcouche)

        root.wm_title("Réseau neuronal")
        tk.mainloop()


def getNmax(nentree, ncouche, nsortie):
    """
    :param :
    """
    liste = [nentree, ncouche, nsortie]

    return max(liste)


def orgaDessin(canvas, nentree, divisonX, height, ncouche, nsortie, nbrcouche):
    sauvcouche = sauventree = sauvesortie = sauvenbr = 0

    taille = height / (max(nentree, ncouche, nsortie) * 2)

    if nentree > 10:
        sauventree = nentree
        nentree = 10
    if ncouche > 10:
        sauvcouche = ncouche
        ncouche = 10
    if nsortie > 10:
        sauvesortie = nsortie
        nsortie = 10
    if nbrcouche > 10:
        sauvenbr = nbrcouche
        nbrcouche = 10

    if sauvcouche > 10:
        pointille(canvas, 1, nbrcouche, divisonX, height, sauvcouche, taille)
    if sauventree > 10:
        pointille(canvas, 2, nbrcouche, divisonX, height, sauventree, taille)
    if sauvesortie > 10:
        pointille(canvas, 3, nbrcouche, divisonX, height, sauvesortie, taille)
    if sauvenbr > 10:
        pointille(canvas, 4, nbrcouche, divisonX, height, sauvenbr, taille)

    dessinerCercle(canvas, nentree, divisonX, height, taille)
    dessinerLineEntree(canvas, nentree, ncouche, nbrcouche, nsortie, divisonX, height)
    i = 0
    while i < nbrcouche:
        i = i + 1
        print(i)
        dessinerCercle(canvas, ncouche, divisonX * (i + 1), height, taille)
    print("+")
    dessinerCercle(canvas, nsortie, divisonX * (nbrcouche + 2), height, taille)


def dessinerCercle(canvas, nentree, divisionX, height, taille):
    divisionY = height / (nentree + 1)
    multi = 1
    x = 0
    x0 = x1 = divisionX
    taille2 = taille/2
    while x < nentree:
        canvas.create_oval(x0 - taille, (multi * divisionY) - taille2, x1, (divisionY * multi) + taille2,
                           fill="#476042")
        x = x + 1
        multi = multi + 1


def dessinerLineEntree(canvas, nentree, ncouche, nbrcouche,nsortie, divisionX, height):
    tmp = divisionX
    for a in range(1, nbrcouche+2):
        divisionX = tmp * a
        divisionX2 = tmp * (a + 1)
        if a==1:
            nbrtour = nentree + 1
            nbrtour2 = ncouche + 1
            divisionY = height / (nentree + 1)
            divisionY2 = height / (ncouche + 1)
        else:
            if a == nbrcouche + 1:
                nbrtour = ncouche + 1
                nbrtour2 = nsortie +1
                divisionY = height / (ncouche + 1)
                divisionY2 = height / (nsortie + 1)
            else :
                nbrtour = ncouche + 1
                nbrtour2 = ncouche + 1
                divisionY = height / (ncouche + 1)
                divisionY2 = height / (ncouche + 1)

        for x in range(1, nbrtour):
            for y in range(1, nbrtour2):
                canvas.create_line(divisionX, divisionY*x, divisionX2-25, divisionY2*y, width=1)


def pointille(canvas, choix, nbrcouche, divisionX, height, ncouche, taille): # ajouter taille pour enelever les 25 50 ...
    hauteur = height/(10+1)
    tmp = divisionX
    if choix == 1:
        for x in range(1,nbrcouche+1):
            divX = tmp*(x+1)
            divY = 9*hauteur
            divY2 = 10*hauteur
            canvas.create_line(divX-(taille/2), divY+15, divX-(taille/2), divY2, fill="#EF1414", width=5, dash=(4, 4))
            canvas.create_text(divX-taille, divY2+40, text=ncouche, fill="#EF1414")

    if choix == 2:
            divX = tmp
            divY = 9*hauteur
            divY2 = 10*hauteur
            canvas.create_line(divX-(taille/2), divY+15, divX-(taille/2), divY2, fill="#EF1414", width=5, dash=(4, 4))
            canvas.create_text(divX-taille, divY2+40, text=ncouche, fill="#EF1414")

    if choix == 3:
            divX = tmp*(nbrcouche+2)
            divY = 9*hauteur
            divY2 = 10*hauteur
            canvas.create_line(divX-(taille/2), divY+15, divX-(taille/2), divY2, fill="#EF1414", width=5, dash=(4, 4))
            canvas.create_text(divX-taille, divY2+40, text=ncouche, fill="#EF1414")

    if choix == 4:
        for x in range(1, ncouche+1):
            divX2 = (tmp * 12)+taille
            divY = x*(hauteur+(taille/3))
            # canvas.create_line(divX-25, divY+15, divX2-25, divY+15, fill="#EF1414", width=5, dash=(4, 4))
            canvas.create_text(divX2, divY, text=ncouche, fill="#EF1414")


def main():
    dessin = Dessin(13, 3, 8, 5)


if __name__ == '__main__':
    main()
