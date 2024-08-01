#coding:utf-8
import time
import customtkinter as ct
import mysql.connector
from tkinter import messagebox
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
# ///mes modules
from connect_app import *
from caisse import Caisse
from commande import Commande
from enregistrement import NouveauProduit
from NouvelUtilisateur import NouvelUser
from ListObjetMenu.ListUsers import *
from ListObjetMenu.ListProduit import *
from ListObjetMenu.ListClient import *
from ListObjetMenu.ListCommande import *
from ListObjetMenu.ImprimerFacture import *


class Boutique:
    def __init__(self):
        # self.boutique = Boutique()
        def dimensions():
            largeur_ecran = self.app.winfo_screenwidth()
            hauteur_ecran = self.app.winfo_screenheight()
            x = (largeur_ecran - 800) // 2
            y = (hauteur_ecran - 500) // 2
            self.app.geometry("800x500+{}+{}".format(x, y))
            
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="boutique"
            )
            self.cursor = self.conn.cursor()
            self.app = ct.CTk()
            # self.connApp = connect_app()
            # style = ttk.Style()
            # style.configure('TButton',bd=0,relief=tk.FLAT,highlightthickness=0)
            self.app.title('Market Management')
            dimensions()

            self.cursor.execute("CREATE DATABASE IF NOT EXISTS boutique")
            self.cursor.execute("USE boutique")
            # creation de la table commande
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS `commande`(
                            `id_commande` SMALLINT(8) NOT NULL AUTO_INCREMENT,
                            `nom_commande` VARCHAR(20) NOT NULL,
                            `date_commande` DATE NOT NULL,
                            PRIMARY KEY(`id_commande`)
                );
            """)
            # creation de la table produit
            self.cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS produit(
                            `id_produit` SMALLINT(8) NOT NULL AUTO_INCREMENT,
                            `nom_produit` VARCHAR(20) NOT NULL,
                            `prix_achat` INT(8) NOT NULL,
                            `prix_vente` INT(8) NOT NULL,
                            `quantite` SMALLINT(11) NOT NULL,
                            `date_registration` DATE NOT NULL,
                            PRIMARY KEY(`id_produit`)
                            -- FOREIGN KEY(id_produit) REFERENCES `commande`(`id_commande`)
                );
            """)
            # creation de la table client
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS client(
                            `id_client` SMALLINT(8) NOT NULL AUTO_INCREMENT,
                            `nom_client` VARCHAR(20) NOT NULL,
                            `tel_client` VARCHAR(10) NOT NULL,
                            PRIMARY KEY(`id_client`)

                );
            """)
  
            # def userActuel():
            #     print(f"actuellement connecté en tant que: {self.connApp.Connect.resultat}")
            #     pass

            # îcone bouton
            img_en = Image.open('img/mini enregistrement.png')
            imgentk = ImageTk.PhotoImage(img_en)

            img_us = Image.open('img/user_ico.png')
            imgustk = ImageTk.PhotoImage(img_us)

            img_cais = Image.open('img/min_caisse.png')
            imgcais = ImageTk.PhotoImage(img_cais)

            img_command = Image.open('img/commande.jpg')
            img_command= img_command.resize((50,50))
            imgcommand = ImageTk.PhotoImage(img_command,size=(50,50))


            # .....................effet ombrage sur un bouton
            # def on_enter(e):
            #     self.frame1.configure(background="white")
            # def on_leave(e):
            #     self.frame1.configure(background="white")

            # def on_enter2(e):
            #     self.frame2.configure(background="white")
            # def on_leave2(e):
            #     self.frame2.configure(background="white")

            # def on_enter3(e):
            #     self.frame3.configure(background="white")
            # def on_leave3(e):
            #     self.frame3.configure(relief='flat')
            # .................Affichage option_boutique
            self.frame1 = ct.CTkFrame(self.app)    #,padding=10
            # self.frame1.bind('<Enter>', on_enter)
            # self.frame1.bind('<Leave>', on_leave)
            self.frame1.grid(row=0, column=0, pady=10)
            self.labelImgUser = ct.CTkLabel(self.frame1, image=imgustk,text=None)
            self.labelImgUser.bind('<Button-1>', self.new_user)
            self.labelImgUser.pack()
            self.lbmsgu = ct.CTkLabel(self.frame1,text='utilisateur')
            self.lbmsgu.pack()

            self.frame2 = ct.CTkFrame(self.app)  #,padding=10
            # self.frame2.bind('<Enter>', on_enter2)
            # self.frame2.bind('<Leave>', on_leave2)
            self.frame2.grid(row=1, column=0, pady=10)
            self.labelEnregistrement = ct.CTkLabel(self.frame2, image=imgentk, text=None)
            self.labelEnregistrement.bind('<Button-1>', self.new_produit)
            self.labelEnregistrement.pack()
            self.lbmsg = ct.CTkLabel(self.frame2, text="enregistrement")
            self.lbmsg.pack()

            self.frame3 = ct.CTkFrame(self.app) #,padding=10
            # self.frame3.bind('<Enter>', on_enter3)
            # self.frame3.bind('<Leave>', on_leave3)
            self.frame3.grid(row=0, column=1, padx=20, pady=10)
            self.LabelCaisse = ct.CTkLabel(self.frame3, image=imgcais, text=None)
            self.LabelCaisse.bind('<Button-1>', self.LaCaisse)
            self.LabelCaisse.pack()
            self.lbmsgc = ct.CTkLabel(self.frame3, text="caisse")
            self.lbmsgc.pack()

            self.frame4 = ct.CTkFrame(self.app)
            self.frame4.grid(row=1, column=1, padx=20,pady=10) # afficher la date du jour
            self.Labelcommande = ct.CTkLabel(self.frame4, image=imgcommand, text=None)
            self.Labelcommande.bind('<Button-1>', self.GestCommandeClient)
            self.Labelcommande.pack()
            self.lbmsgcommd = ct.CTkLabel(self.frame4, text="Commande")
            self.lbmsgcommd.pack()
            date = time.strftime("%d/%m/%Y")
            hours = time.strftime("%H.%I.%S")
            
            lbdate = ct.CTkLabel(self.app, text=f" Date du jour : {date}")
            # lbdate.after(1, hours)
            lbdate.place(x=580,y=0)
            # ...................Affichage et creation option_menu
            self.barre_menu = tk.Menu(self.app,bg="black")

            self.fm = tk.Menu(self.barre_menu,tearoff=0)
            self.fm.add_command(label="Afficher liste des Produits",command=self.listProduit)
            self.fm.add_command(label="Commande en cours", command=None)
            self.fm.add_command(label="Utilisteur en ligne", command=None)
            self.barre_menu.add_cascade(label="Menu", menu=self.fm)
            self.barre_menu.add_cascade(label="DarkMode", command=self.Darkmode)
            self.barre_menu.add_cascade(label="LghtMode", command=self.Lightmode)
            # self.A_user = Gestion.connect_App.resultat[1]
            # self.lbA_user = ct.CTkLabel(self.app,text=f"Connecter : {self.A_user}")
            # self.lbA_user.place(x=0,y=0)

            # ...code
            self.app.configure(menu=self.barre_menu)
            self.app.mainloop()
            self.conn.close()

        except mysql.connector.errors.InterfaceError:
            messagebox.showerror("Application Error", "Veuillez demarrez le serveur")

        except Exception as e:
            messagebox.showerror("", "Une erreur est survenu : {}".format(e))
            print(e)
            self.conn.rollback()

    #  Fonctionnalité boutique
    def new_produit(self,event):
        NouveauProduit(self.app)

    def new_user(self,event):
        NouvelUser(self.app)

    def LaCaisse(self,event):
        Caisse(self.app)
        pass

    def GestCommandeClient(self,event):
        Commande(self.app)
        pass

    # Fonctionnalité du menu
    def listClient(self):
        ListCLient(self.app)
        pass

    def listProduit(self):
        ListProduit(self.app)
        

    def listCommande(self):
        ListCommande(self.app)
        pass
    def Darkmode(self):
        ct.set_appearance_mode("dark")
    def Lightmode(self):
        ct.set_appearance_mode("light")
