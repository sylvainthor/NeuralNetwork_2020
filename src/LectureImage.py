#!/usr/bin/env python
import builtins
import tkinter

from PIL import Image
from pathlib import Path
from tkinter import filedialog


class LectureImage:

    def __init__(self, nom):
        """
        :param nom: fournis par @gerDirectory, photo a placer dans une matrice
        """
        im = Image.open(nom)
        f = open('../Data/matrice.txt', 'a')
        phrase = ""
        (x, y) = im.size

        for i in range(x):
            for j in range(y):
                # print(i, j)
                couleur = im.getpixel((i, j))
                # srt() : convertit la couleur en string afin de le placer dans un string
                phrase = phrase + str(couleur / 255) + ", "
        phrase = phrase + "\n"
        f.write(phrase)


def getDirectory(chemin):
    """
    :param chemin: fournis par l'user, chemin de recherche d'image
    """
    # Path sert a chercher dans le chemin indiqué par l'utilisateur
    # rglob est une methode de globbing affin de ne prendre que les images

    for nom in Path(chemin).rglob("*.jpg"):
        print(nom)
        LectureImage(nom)


def main():
    # Ouvre un gestionnaire de dossier afin de selectionner un dossier d'images
    """
    :param: initialdir : chemin initial pour cherhcer des repertoires
    :param: title : Nom de la fenetre
    """
    dossier = filedialog.askdirectory(initialdir="/export/home/an18/chailloul/PT_2019/Data/", title="Choix du dossier")
    getDirectory(dossier)


if __name__ == '__main__':
    main()
