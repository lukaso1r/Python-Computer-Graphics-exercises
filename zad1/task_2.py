import tkinter as tk

class Task2:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.entries = {}
        self.shape_var = tk.StringVar(value="Linia")  # Domyślnie ustawiamy "Linia"
        self.create_gui()

    def create_gui(self):
        self.root.title("Podawanie parametrów rysowania")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Wybór kształtu do rysowania
        shape_label = tk.Label(self.root, text="Wybierz kształt:")
        shape_label.pack()

        shapes_menu = tk.OptionMenu(self.root, self.shape_var, "Linia", "Prostokąt", "Okrąg")
        shapes_menu.pack()

        # Pola do wprowadzania współrzędnych
        for label_text in ["X1", "Y1", "X2", "Y2", "Kolor", "Szerokość"]:
            label = tk.Label(self.root, text=f"Współrzędna {label_text}:")
            label.pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.entries[label_text] = entry

        btn_draw = tk.Button(self.root, text="Rysuj", command=self.draw_shape)
        btn_draw.pack()

        btn_back = tk.Button(self.root, text="Powrót", command=self.back_to_menu)
        btn_back.pack()

        self.adjust_window_size()

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from main import MainApp
        MainApp(self.root)

    def adjust_window_size(self):
        self.root.update_idletasks()
        new_width = self.root.winfo_reqwidth()
        new_height = self.root.winfo_reqheight()
        self.root.geometry(f"{new_width + 20}x{new_height + 20}")

    def draw_shape(self):
        x1 = int(self.entries["X1"].get())
        y1 = int(self.entries["Y1"].get())
        x2 = int(self.entries["X2"].get())
        y2 = int(self.entries["Y2"].get())
        color = self.entries["Kolor"].get()
        width = int(self.entries["Szerokość"].get())

        shape = self.shape_var.get()

        if shape == "Linia":
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        elif shape == "Prostokąt":
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)
        elif shape == "Okrąg":
            self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=width)
