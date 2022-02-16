import tkinter as tk
from ctypes import windll


def set_appwindow(mainWindow):  # Pour afficher l'icon dans la barre des taches

    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    mainWindow.wm_withdraw()
    mainWindow.after(10, mainWindow.wm_deiconify)


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.COLOR = {
            'lightgreen': '#EAFCEC',
            'entrycolor': '#89DA92',
            'buttontext': '#45794A',
            'gray': '#666666'
        }

        # Config Window

        self.geometry("679x405")
        self.config(background=self.COLOR["lightgreen"])
        self.wm_overrideredirect(True)

        self.x, self.y = None, None

        self.bind('<ButtonPress-1>', self.mouse_down)
        self.bind('<B1-Motion>', self.mouse_drag)
        self.bind('<ButtonRelease-1>', self.mouse_up)

        # Design
        imgs = tk.PhotoImage(file=r'../ressource/img/icon.png').subsample(20)
        icons = tk.Label(self, image=imgs, background=self.COLOR["lightgreen"], bd=0,
                         foreground=self.COLOR["lightgreen"])
        icons.photo = imgs
        icons.place(x=10, y=10)

        title = tk.Label(self, text="GestMoney", background=self.COLOR["lightgreen"], foreground=self.COLOR["gray"],
                         font=('Roboto', 24, 'bold'))
        title.place(x=80, y=10)

        quit_button = tk.Button(self, text="X", bd=2, background=self.COLOR["lightgreen"],
                                foreground=self.COLOR["buttontext"], activebackground=self.COLOR["lightgreen"],
                                activeforeground=self.COLOR["buttontext"], font=('Roboto', 14, 'bold'),
                                command=self.destroy)
        quit_button.place(x=800, y=10)

        # Permet de voir l'icon dans notre barre des taches
        self.after(10, lambda: set_appwindow(self))

    # Fonction
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

    def update(self):
        self.mainloop()


if __name__ == "__main__":
    MainWindow().update()
