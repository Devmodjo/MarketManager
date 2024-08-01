import customtkinter as ct
from Boutique import Boutique
from PIL import Image, ImageTk
from tkinter import messagebox,ttk
from ttkthemes import ThemedStyle
import mysql.connector


class Connect:
    def __init__(self):
        def dimensions():
            largeur_ecran = self.ap.winfo_screenwidth()
            hauteur_ecran = self.ap.winfo_screenheight()
            x = (largeur_ecran - 300) // 2
            y = (hauteur_ecran - 350) // 2
            self.ap.resizable(width=False, height=False)
            self.ap.geometry("300x350+{}+{}".format(x,y))
        try:
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password ="",
                database = "boutique"
            )
            self.ap = ct.CTk()
            self.ap.title('Authentification')
            self.cursor = self.conn.cursor()
            # self.app.config(bg="#A8A8A8")
            dimensions()
            image = Image.open("img/cadenas-ferme.png")
            image.resize((10,10))
            image_tk = ImageTk.PhotoImage(image)
            label_img = ct.CTkLabel(self.ap,image=image_tk,text=None)
            label_img.pack()
            self.resultat = None
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS boutique")

            self.req = self.cursor.fetchone()
            print(self.resultat)
            self.cursor.execute("USE boutique")
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS utilisateur(
                                `id_user` SMALLINT(8) NOT NULL AUTO_INCREMENT,
                                `name_user` VARCHAR(20) NOT NULL,
                                `password_user` VARCHAR(20) NOT  NULL,
                                PRIMARY KEY(`id_user`)
                    );
                """)
            self.frame = ct.CTkFrame(self.ap)
            self.frame.pack(side='bottom')
                
            self.name = ct.CTkLabel(self.frame, text="Username")
            self.name.grid(row=0, column=0, pady=5)
            self.user_name = ct.CTkEntry(self.frame, width=200)
            self.user_name.grid(row=0,column=1, pady=5)

            self.password = ct.CTkLabel(self.frame,text="password")
            self.password.grid(row=1, column=0, pady=10)
            self.user_password = ct.CTkEntry(self.frame, width=200,show='*')
            self.user_password.grid(row=1, column=1, pady=10)
            self.btn = ct.CTkButton(self.frame,text="Se connecter",command=self.connection)
            self.btn.grid(row=2,column=0,columnspan=2)
            # self.l = tk.Label(text="Veuillez saisir vos identifiants", fg="red")
            # self.l.pack()
                
            self.ap.mainloop()
            self.conn.close()
        except mysql.connector.errors.InterfaceError:
            messagebox.showerror("Application Error","Veuillez demarrez le seveur")
        except Exception as e:
            messagebox.showerror("[ERREUR]","une erreur est survenue")
            print("Erreur : ", e)


    def connection(self):
        global resultat
        users = self.user_name.get()
        password = self.user_password.get()
     
        try:
            # global resultat
            self.cursor.execute("SELECT * FROM utilisateur WHERE name_user = %s AND password_user = %s",(users,password))
            resultat = self.cursor.fetchone()
            # print(resultat)
            self.resultat = resultat
            if resultat:
                # self.user_name.delete(0, tk.END)
                # self.user_password.delete(0, tk.END)
                messagebox.showinfo('Connect[OK]','connexion etablie avec succes')
                self.ap.destroy()
                Boutique()
                        
            else:
                messagebox.showerror('Connect[ERROR]','Identifiant non repertorier')
                self.user_name.delete(0, ct.END)
                self.user_password.delete(0, ct.END)
        except Exception as e:
            messagebox.showerror('Application Error','une erreur est survenue : {}'.format(e))

        

