import tkinter as tk
from tkinter import messagebox,ttk
import customtkinter as ctk
import pandas as pd
import mysql.connector


class ListProduit:
    def __init__(self,screen):

        try:
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "boutique"
            )
            self.app = ctk.CTkToplevel(screen)
            self.app.title('Liste des produits')
            self.app.resizable(width=False,height=True)
            self.app.grab_set()
            self.cursor = self.conn.cursor()
            self.reqList = self.cursor.execute('SELECT nom_produit,prix_achat,prix_vente,date_registration,quantite FROM produit')
            self.result = self.cursor.fetchall()
            print(self.result)
            
            # creation du tableau
            self.tab = ttk.Treeview(self.app, columns=("col1","col2","col3","col4","col5"), show='headings')
            # definition des colonnes
            self.tab.heading("col1",text="nom produit")
            self.tab.heading("col2",text="prix achat")
            self.tab.heading("col3",text="prix vente")
            self.tab.heading("col4",text="date enregistrement")
            self.tab.heading("col5",text="quantité")

            # ajout des donné dans le tableau
            for i, row in enumerate(self.result):
                self.tab.insert("","end",values=row)

            self.tab.pack()
        except mysql.connector.Error:
            messagebox.showerror('Application Error', "erreur lors de la recuperation des donnée")
        except mysql.connector.errors.InterfaceError:
            messagebox.showerror("Application Error","Verifier que le serveur est connecter")
        finally:
            self.conn.close()
            self.app.mainloop()
