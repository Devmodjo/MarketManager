import customtkinter as ct
# import bcrypt
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import mysql.connector

class NouvelUser:
    def __init__(self,screen):

        # fonction pour centrer mon ecran
        def dimensions():
            largeur_ecran = self.wind.winfo_screenwidth()
            hauteur_ecran = self.wind.winfo_screenheight()
            x = (largeur_ecran - 300) // 2
            y = (hauteur_ecran - 350) // 2
            self.wind.geometry("300x350+{}+{}".format(x,y))
            self.wind.resizable(width=False,height=False)

        # fontion qui me permet de haché les mots de passes
        """def hash_password(password):
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password

        # fonction pour verifier un mot de passe
        def verify_password(input_password, hashed_password):
            return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)"""

        try:
            self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'boutique'
            )
            self.cursor = self.conn.cursor()
            self.wind = ct.CTkToplevel(screen)
            self.wind.title('Ajouter un utilisateur')
            self.wind.grab_set()
            dimensions()

            image = Image.open('img/user-icon-on-transparent-background-free-png.png')
            image.resize((10,10))
            image_tk = ImageTk.PhotoImage(image)
            label_img = ct.CTkLabel(self.wind,text=None,image=image_tk)
            label_img.pack(side='top',pady=20)
            lbmsg = ct.CTkLabel(self.wind, text='entrer les informations du nouvel utilisateur ici')
            lbmsg.pack(side='top')
            
            self.lf = ct.CTkFrame(self.wind)
            self.lf.pack(side='bottom')
            self.label_username = ct.CTkLabel(self.lf, text="Nom d'utilisateur:")
            self.label_password = ct.CTkLabel(self.lf, text="Mot de passe:")
            self.entry_username = ct.CTkEntry(self.lf, width=200)
            self.entry_password = ct.CTkEntry(self.lf, show="*",width=200)

            def nouvel_utilisateur(users, password):
                new_users = (users, password)
                try:
                    self.cursor.execute('INSERT INTO utilisateur (name_user, password_user) VALUES(%s,%s)',new_users)
                    messagebox.showinfo('','nouveaux compte enregisitrer avec succes')
                    self.conn.commit()
                except Exception as r:
                    messagebox.showerror('','une erreur est survenue : {}'.format(r))
                    self.conn.rollback()
            
            def process_add():
                users = self.entry_username.get()
                password = self.entry_password.get()

                if users and password:
                    nouvel_utilisateur(users , password)
                    #  messagebox.showinfo("", conect ok)
                    # dans le fichier interface de connection je vais  creer un nouvelle fenetre vas s'ouvrir(le logiciel en lui meme)
                    # tout en dessous c'est idem
                else:
                    messagebox.showerror('',"Veuillez entrez un nom d'utilisateur et un  mot de passe")

                self.entry_username.delete(0, ct.END)
                self.entry_password.delete(0, ct.END)


            self.label_username.grid(row=0, column=0, pady=5)
            self.label_password.grid(row=1, column=0, pady=5)
            self.entry_username.grid(row=0, column=1, pady=5)
            self.entry_password.grid(row=1, column=1, pady=5)

            self.button_login = ct.CTkButton(self.lf, text="Enregistrer", command=process_add)
            self.button_login.grid(row=2, column=0, columnspan=2, pady=10)
            self.wind.mainloop()
            self.conn.close()

        except Exception as e:
            messagebox.showerror('','une erreur est survenue : {}'.format(e))
            self.conn.rollback()
# if __name__ == '__main__':
#     NouvelUser()