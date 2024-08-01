import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import mysql.connector


class Commande:
    def __init__(self,screen):
        try:
            self.con = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'boutique'
            )
            self.app = ctk.CTkToplevel(screen)
            self.app.title('Commande')
        except Exception as e:
            messagebox.showerror('Application Error', f'Erreur : {e}')
        finally:
            self.app.mainloop()
            self.con.close()