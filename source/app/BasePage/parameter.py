import json
import tkinter as tk
import cv2

from data.data import select_image_user, get_user, set_user, get_all_users, update_user_id
from source.app.Sys import set_color, select_image, set_appwindow, center

from tkinter import filedialog as fd, messagebox


class ParametreWindow(tk.Tk):
    def __init__(self, window):
        tk.Tk.__init__(self)

        self.window = window
        self.geometry("348x420")
        self.config(bg=set_color("lightgreen"))
        self.wm_overrideredirect(True)
        self.iconbitmap(select_image('parametre.ico'))
        self.title_bar()
        self.title("GestMoney | Paramètre")

        self.profile_img = tk.PhotoImage(master=self, file=select_image_user(self.window.user_id)).subsample(9)

        self.widgets()
        self.profile = tk.Label(self, image=self.profile_img, background=set_color('lightgreen'), bd=0)
        self.profile.photo = self.profile_img
        self.profile.pack(ipady=10)

        # Affichage erreurs
        self.error_canvas = tk.Canvas(self)

        center(self)
        # Permet de voir l'icon dans notre barre des taches
        self.after(10, lambda: set_appwindow(self))

    def select_files(self):
        filetypes = (
            ('Type', '*.png'),
        )

        filenames = fd.askopenfilenames(
            title='GestMoney | Open files',
            initialdir='/',
            filetypes=filetypes)

        img = cv2.imread(filenames[0], cv2.IMREAD_UNCHANGED)

        width = img.shape[1]
        height = img.shape[0]

        if width and height == 500:
            self.profile_img = tk.PhotoImage(master=self, file=filenames).subsample(9)
            self.profile.photo = self.profile_img
            self.profile.configure(image=self.profile_img)

            image_show = tk.Label(self, text=r"/!\ Attention l'image s'actualisera \nau redémarrage de l'application !",
                                  background=set_color("lightgreen"),
                                  foreground="red", font=('Roboto', 8, 'bold'))
            image_show.place(x=25, y=138)

            with open(r'..\..\data\users.json', 'r+') as file:
                data = json.load(file)

                data[self.window.user_id]["image"] = filenames

            with open(r'..\..\data\users.json', 'w') as file:
                json.dump(data, file, indent=4)
        else:
            messagebox.showerror("GestMoney | Erreur", "S'il vous plait veuillez mettre une image de taille : 500x500")

    def widgets(self):
        global_canvas = tk.Canvas(self, height=self.winfo_height() - 48, width=self.winfo_width(),
                                  background=set_color("lightgreen"), highlightthickness=0)
        open_button = tk.Button(global_canvas, text="Modifier la photo", background=set_color("lightgreen"),
                                foreground=set_color("darkgreen"), bd=0, activebackground=set_color("lightgreen"),
                                activeforeground=set_color("darkgreen"), cursor='hand2', command=self.select_files)
        open_button.place(x=67, y=70)

        global_canvas.create_text(self.winfo_width() / 2, 125, text="Identifiant",
                                  fill=set_color("darkgreen"), font=('Roboto', 12))

        self.id_entry = tk.Entry(global_canvas, background=set_color("darkgreen"),
                                 bd=0, font=('Roboto', 12), fg='#FFFFFF')
        self.id_entry.insert(0, self.window.user_id)
        self.id_entry.configure(justify='center')
        self.id_entry.place(x=16, y=140, width=204, height=25)

        global_canvas.create_text(self.winfo_width() / 2, 185, text="Email",
                                  fill=set_color("darkgreen"), font=('Roboto', 12))

        self.email_entry = tk.Entry(global_canvas, background=set_color("darkgreen"),
                                    bd=0, font=('Roboto', 12), fg='#FFFFFF')
        self.email_entry.insert(0, self.window.user_email)
        self.email_entry.configure(justify='center')
        self.email_entry.place(x=16, y=200, width=204, height=25)

        global_canvas.create_text(self.winfo_width() / 2, 245, text="Mot de passe",
                                  fill=set_color("darkgreen"), font=('Roboto', 12))

        self.mdp_entry = tk.Entry(global_canvas, background=set_color("darkgreen"), bd=0,
                                  font=('Roboto', 12), fg='#FFFFFF', show='*')
        self.mdp_entry.configure(justify='center')
        self.mdp_entry.place(x=16, y=260, width=204, height=25)

        self.change_password = tk.Button(global_canvas, text="Changer le mot de passe",
                                         bg=set_color("lightgreen"), fg=set_color("darkgreen"),
                                         activebackground=set_color("lightgreen"),
                                         activeforeground=set_color("darkgreen"),
                                         font=('Roboto', 10, 'bold'), bd=0, cursor='hand2')
        self.change_password.place(x=35, y=285)

        valid_changes = tk.Button(global_canvas, text="Valider les changements", background=set_color("darkgreen"),
                                  activeforeground="#fff", activebackground=set_color("buttonactive"), bd=0,
                                  foreground="#fff", cursor='hand2', font=('Roboto', 11), command=self.valid_changes)
        valid_changes.place(x=self.winfo_width() / 2 - 92.5, y=325, width=185, height=40)

        # Copyright
        global_canvas.create_text(self.winfo_width() / 2, self.winfo_height() - 60, text="© 2022 GestMoney",
                                  fill=set_color("gray"), font=('Roboto', 10))

        global_canvas.place(x=0, y=48)

    def title_bar(self):
        title_bar = tk.Canvas(self, width=500, height=48, bg=set_color('darkgreen'), highlightthickness=0)
        title_bar.create_text(120, 25, text="GestMoney", font=('Roboto', 15, 'bold'), fill="white")
        title_bar.pack()

        imgs = tk.PhotoImage(master=self, file=select_image("parametre.png")).subsample(12)
        icon = tk.Label(self, image=imgs, background=set_color("darkgreen"), bd=0,
                        foreground=set_color("lightgreen"))
        icon.photo = imgs
        icon.place(x=5, y=2)

        quit_button = tk.Button(self, text="X", background=set_color("darkgreen"), cursor='hand2',
                                relief='groove', foreground=set_color("lightgreen"),
                                activebackground=set_color("darkgreen"), activeforeground=set_color("lightgreen"),
                                font=('Roboto', 15, 'bold'), command=self.destroy)
        quit_button.place(x=190, y=4, width=40, height=40)

        profile_img = tk.PhotoImage(master=self, file=select_image("profile-base.png")).subsample(14)
        profile_btn = tk.Button(self, image=profile_img, background=set_color('darkgreen'), cursor='hand2',
                                activebackground=set_color('darkgreen'), bd=0)
        profile_btn.photo = profile_img
        profile_btn.place(x=955, y=10)

        self.apply_drag([title_bar, icon])

    def show_error(self, text):
        self.error_canvas.destroy()
        self.error_canvas = tk.Canvas(self, height=20, width=self.winfo_width(), background=set_color("lightgreen"),
                                      highlightthickness=0)
        self.error_canvas.create_text(self.winfo_width() / 2, 0, text=text, font=('Roboto', 9), fill='red', anchor='n')

        self.error_canvas.place(x=0, y=145)

    def valid_changes(self):

        old_user = get_user(self.window.user_id)

        new_id = self.id_entry.get()
        new_email = self.email_entry.get()
        new_mdp = self.mdp_entry.get()
        mdp_confirm = self.confirm_mdp_entry.get()

        new_user = old_user.copy()
        new_user['id'] = new_id
        new_user['mdp'] = new_mdp
        new_user['email'] = new_email

        if '' in new_user.values():
            self.show_error('Veuillez remplir toutes les cases')

        elif not new_id.isalpha():
            self.show_error("L'identifiant ne doit contenir que des lettres")

        elif new_id in get_all_users() and new_id != old_user['id']:
            self.show_error('Cet identifiant est déjà utilisé')

        elif '@' not in new_email and '.' not in new_email:
            self.show_error('E-mail invalide')

        elif not 6 <= len(new_mdp) <= 20:
            self.show_error('Le mot de passe doit faire entre 6 et 20 aractères')

        else:
            set_user(new_id, old_user['id'], new_user)
            update_user_id(old_user['id'], new_id)
            self.window.user_id = new_id
            self.window.user_email = new_email
            self.destroy()

    def mouse_down(self, event):
        self.x, self.y = event.x, event.y

    def mouse_up(self, event):
        self.x, self.y = None, None

    def mouse_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x0 = self.winfo_x() + deltax
        y0 = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x0, y0))

    def apply_drag(self, elements):
        for element in elements:
            element.bind('<ButtonPress-1>', self.mouse_down)
            element.bind('<B1-Motion>', self.mouse_drag)
            element.bind('<ButtonRelease-1>', self.mouse_up)
