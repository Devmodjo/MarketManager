import customtkinter as ct
import tkinter as tk
import time
from tkinter import messagebox,ttk
from PIL import Image, ImageTk
import mysql.connector

class NouveauProduit:
    def __init__(self,screen):

        def dimensions():
            largeur_ecran = self.app.winfo_screenwidth()
            hauteur_ecran = self.app.winfo_screenheight()
            x = (largeur_ecran - 350) // 2
            y = (hauteur_ecran - 520) // 2
            self.app.geometry("350x520+{}+{}".format(x,y))
            self.app.resizable(width=False,height=False)
        try:

            self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'boutique'
            )
            
            self.app = ct.CTkToplevel(screen)
            self.app.grab_set()
            self.cursor = self.conn.cursor()
            dimensions()
            self.app.title('nouveau produit')

            def enregister_produit():
                id_p = self.cursor.lastrowid
                Nom_Produit = self.entry_produit.get()
                Prix_Achat = self.entry_AprixProduit.get()
                Prix_vente = self.entry_VprixProduit.get()
                Quantite = self.entry_quantite.get()
                date_enregistrement = self.entry_registration.get()
                field_list = [id_p, Nom_Produit, Prix_Achat, Prix_vente, Quantite, date_enregistrement]

                if field_list[1] and field_list[2] and field_list[3] and field_list[4] and field_list[5] :
                    field_list[3] = float(field_list[3])
                    field_list[2] = float(field_list[2])

                    if field_list[3] > field_list[2] and field_list[3] >= 0 and field_list[2] >= 0:
                        field_list[4] = int(field_list[4])
                        
                        if field_list[4] > 0:
                            try:
                                self.cursor.execute("""
                                    INSERT INTO produit(id_produit, nom_produit, prix_achat, prix_vente, quantite, date_registration)
                                    VALUES(%s, %s, %s, %s, %s, %s)
                                """,(field_list[0], field_list[1], field_list[2], field_list[3], field_list[4], field_list[5])
                                )

                                self.conn.commit()
                                messagebox.showinfo('','{} Enregistre avec succès'.format(field_list[1]))
                                   
                            except Exception as e:
                                messagebox.showerror('','Une erreur est survenue : '.format(e))
                                print(e)
                                self.conn.rollback()
                            
                        else:
                            messagebox.showerror('','la quantite ne dois pas être null ou negative')
                    else:
                        messagebox.showerror('', "le prix de vente doit être supérieur au prix d'achat ou verifier que l'un des deux champs sont positifs")
                else:
                    messagebox.showerror('','Veuillez remplir tous les champs')

                
            self.lb_produit = ct.CTkLabel(self.app, text='Nom_Produit')
            self.lb_produit.grid(row=0, column=0, pady=20)
            self.entry_produit = ct.CTkEntry(self.app, width= 250)
            self.entry_produit.grid(row=0, column=1, pady=20)

            self.varPrixAchat = tk.DoubleVar()
            self.lb_AprixProduit = ct.CTkLabel(self.app, text='Prix_Achat')
            self.lb_AprixProduit.grid(row=1,column=0,pady=20)
            self.entry_AprixProduit = ct.CTkEntry(self.app, width=250,textvariable=self.varPrixAchat)
            self.entry_AprixProduit.grid(row=1,column=1,pady=20)

            self.varPrixVente = tk.DoubleVar()
            self.lb_VprixProduit = ct.CTkLabel(self.app, text='Prix_vente')
            self.lb_VprixProduit.grid(row=3,column=0,pady=20)
            self.entry_VprixProduit = ct.CTkEntry(self.app, width=250, textvariable=self.varPrixVente)
            self.entry_VprixProduit.grid(row=3, column=1, pady=20)

            self.varQuantite = tk.IntVar()
            self.lb_quantite = ct.CTkLabel(self.app, text='Quantité')
            self.lb_quantite.grid(row=4,column=0,pady=20)
            self.entry_quantite = ct.CTkEntry(self.app, width=250, textvariable=self.varQuantite)
            self.entry_quantite.grid(row=4, column=1, pady=20)

            self.lb_Registration = ct.CTkLabel(self.app, text="date_Achat")
            self.lb_Registration.grid(row=5,column=0,pady=20)
            self.entry_registration = ct.CTkEntry(self.app, width=250)
            self.entry_registration.grid(row=5,column=1,pady=20)
            
            self.btn_saveNewProduit = ct.CTkButton(self.app, text='enregister', width=250, command=enregister_produit)
            self.btn_saveNewProduit.grid(row=6, column=0, columnspan=3)

            self.app.mainloop()
            self.conn.close() 
        except mysql.connector.errors.InterfaceError:
            messagebox.showerror('','Veuillez demarrez le serveur')
        except Exception as e:
            messagebox.showerror('','une erreur est survenue : {}'.format(e))
            self.conn.rollback()