from tkinter import *
from tkinter import messagebox
from pathlib import Path
from tkinter.filedialog import askopenfilename

import ReseauNeuronal
import SaveNLoad
import Dessin
import os


class AppReseau(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Setup Menu
        MainMenu(self)

        # Window Setup
        self.title("Créateur de réseaux de neuronaux")
        self.geometry("720x480")
        self.minsize(720, 480)
        self.maxsize(720, 480)
        self.config(background='#33A4FF')

        # Setup Frame
        container = Frame(self, bg='#33A4FF')
        container.pack(expand=YES)

        self.frames = {}

        for F in (MenuPage, CreateNetworkF, LoadNetworkF):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MenuPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def confirm(self):
        msgCreate = messagebox.askquestion('Créateur de réseau',
                                           'Voulez-vous créer le réseau \"{}\" ?\nNb de neurones d\'entrée : {}\nNb de neurones de sortie : {}\n'.format(
                                               nomReseau.get(), nbEntre.get(), nbSortie.get()))
        print(msgCreate)
        print(nbEntre.get() + nbSortie.get())

        if msgCreate == 'yes':

            msgCreateConfirm = messagebox.showinfo('Créateur de réseau',
                                                   'Réseau créé !\nVous pouvez maintenant le charger')

            x = nbCN.get()
            n = x.split()

            tab_cc = n

            for i in range(0, len(tab_cc)):
                tab_cc[i] = int(tab_cc[i])

            print(tab_cc)

            # CREATION DU RESEAU
            leReseau = ReseauNeuronal.ReseauNeuronal(nbEntre.get(), tab_cc, nbSortie.get())

            # CREATION DE SA SAUVEGARDE
            laSauvegarde = SaveNLoad.SaveNLoad()
            laSauvegarde.save("sauvegardes/"+nomReseau.get(), leReseau)

            print("Réseau créé et sauvegardé")

            self.show_frame(MenuPage)
        else:
            print("no")

    def charger(self):

        filename = askopenfilename(initialdir="./", title="Sélectionner un fichier réseau")
        print(filename)

        full_path = filename
        os.path.split(full_path)

        print(os.path.split(full_path)[1])

        leLoad = SaveNLoad.SaveNLoad()
        Dessin.Dessin(leLoad.load("sauvegardes/"+os.path.split(full_path)[1]))


class MenuPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Créateur de réseau de neurones", font=("Courrier", 20), bg='white', fg='#33A4FF')
        label.pack(padx=10, pady=10)
        page_one = Button(self, text="Créer mon réseau", font=("Courrier", 20), bg='white', fg='#33A4FF',
                          command=lambda: controller.show_frame(CreateNetworkF))
        page_one.pack()
        page_two = Button(self, text="Charger un réseau", font=("Courrier", 20), bg='white', fg='#33A4FF',
                          command=lambda: controller.show_frame(LoadNetworkF))
        page_two.pack()


class CreateNetworkF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Nouveau réseau", font=("Courrier", 20), bg='white', fg='#33A4FF')
        label.pack(padx=10, pady=10)

        # NOM RESEAU
        L_nomReseau = Label(self, text="Nom du réseau", font=("Courrier", 10), bg='white', fg='#33A4FF')
        L_nomReseau.pack(padx=10, pady=10)
        global nomReseau
        nomReseau = StringVar()
        E_nomReseau = Entry(self, textvariable=nomReseau)
        E_nomReseau.pack()

        # NOMBRE DE NEURONES D'ENTREE
        L_nbEntre = Label(self, text="Nombre de neurones d'entrée", font=("Courrier", 10), bg='white', fg='#33A4FF')
        L_nbEntre.pack(padx=10, pady=10)
        global nbEntre
        nbEntre = IntVar()
        E_nbEntre = Entry(self, textvariable=nbEntre)
        E_nbEntre.pack()

        # NOMBRE DE COUCHES CACHEES ET NOMBRE DE NEURONES PAR COUCHES
        L_nbCNeurone = Label(self,
                             text="Nombre de neurone pour chaque couches\n Exemple : 3 couches, 1 neurone pour la première, 3 pour la deuxième et 2 pour la dernière == 1 3 2",
                             font=("Courrier", 10), bg='white', fg='#33A4FF')
        L_nbCNeurone.pack(padx=10, pady=10)
        global nbCN
        nbCN = StringVar()
        E_nbCNeurone = Entry(self, textvariable=nbCN)
        E_nbCNeurone.pack()

        # NOMBRE DE NEURONES DE SORTIE
        L_nbSortie = Label(self, text="Nombre de neurone en sortie", font=("Courrier", 10), bg='white', fg='#33A4FF')
        L_nbSortie.pack(padx=10, pady=10)
        global nbSortie
        nbSortie = IntVar()
        E_nbSortie = Entry(self, textvariable=nbSortie)
        E_nbSortie.pack()

        B_Return = Button(self, text="Retour", font=("Courrier", 20), bg='white', fg='#33A4FF',
                          command=lambda: controller.show_frame(MenuPage))
        B_Return.pack()

        BSubmit = Button(self, text="Valider", font=("Courrier", 20), bg='white', fg='#33A4FF',
                         command=lambda: controller.confirm())
        BSubmit.pack()


class LoadNetworkF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Charger un réseau", font=("Courrier", 20), bg='white', fg='#33A4FF')
        label.pack(padx=10, pady=10)

        B_Load = Button(self, text="Sélectionner un réseau", font=("Courrier", 20), bg='white', fg='#33A4FF',
                        command=lambda: controller.charger())
        B_Load.pack()

        B_Return = Button(self, text="Retour", font=("Courrier", 20), bg='white', fg='#33A4FF',
                          command=lambda: controller.show_frame(MenuPage))
        B_Return.pack()


class MainMenu:
    def __init__(self, master):
        # BARRE MENU
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quitter", command=master.quit)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        master.config(menu=menubar)


def main():
    app = AppReseau()
    app.mainloop()


if __name__ == '__main__':
    main()
