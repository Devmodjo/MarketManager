import tkinter as tk
import customtkinter as ct
from tkinter import ttk, messagebox
import mysql.connector

"""c'est un peu complique"""
class Caisse:
	def __init__(self,screen):
		try:
			self.conn = mysql.connector.connect(
				host = 'localhost',
				user = 'root',
				password = '',
				database = 'boutique'
			)
			self.app = ct.CTkToplevel(screen)
			self.app.title("Caisse")
			self.app.grab_set()
			self.dimensions()

			# Frame tableau modifiable sur les produits
			self.Fproduit = ct.CTkFrame(self.app, width=350,height=850)
			self.Fproduit.pack(side="left",padx=10)
			# Affichage des choix des produit
			self.FafficherChoix = ct.CTkFrame(self.app,width=self.app.winfo_screenwidth(), height=470)
			self.FafficherChoix.pack(side="top")
			# Operation sur money
			self.Foperation = ct.CTkFrame(self.app, width=self.app.winfo_screenwidth(), height=350)
			self.Foperation.pack(side="top",pady=10)
			

		except mysql.connector.errors.InterfaceError:
			messagebox.showerror('Application Error', 'Une erreur est survenue\nverifer si vous ête encore connecter au serveur')
		except Exception as e:
			messagebox.showerror('Application Error', f'Une Erreur est survenue : {e}')
		finally:
			self.app.mainloop()
			self.conn.close()

	def dimensions(self):
            largeur_ecran = self.app.winfo_screenwidth()
            hauteur_ecran = self.app.winfo_screenheight()
            x = (largeur_ecran - 1000) // 2
            y = (hauteur_ecran - 650) // 2
            self.app.geometry("1000x650+{}+{}".format(x, y))