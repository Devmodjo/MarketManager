import tkinter as tk
import mysql.connector

class ListCLient:
    """programmer interface list_client"""
        
    def __init__(self,screen):
        def dimensions():
            largeur_ecran = self.app.winfo_screenwidth()
            hauteur_ecran = self.app.winfo_screenheight()
            x = (largeur_ecran - 800) // 2
            y = (hauteur_ecran - 500) // 2
            self.app.geometry("800x500+{}+{}".format(x, y))

        self.app = tk.Tk()
        dimensions()
        self.app.mainloop()
        pass