import tkinter as tk

class Task4:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.entries = {}
        self.shape_var = tk.StringVar(value="Linia")  # Domyślnie ustawiamy "Linia"
        self.shapes = []  # Lista do przechowywania narysowanych kształtów
        self.selected_shape = None
        self.offset_x = 0
        self.offset_y = 0
        self.create_gui()

    def create_gui(self):
        self.root.title("Rysowanie i przesuwanie kształtów")

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

        # Ustawienie funkcji do przesuwania kształtów
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

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
            shape_id = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        elif shape == "Prostokąt":
            shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)
        elif shape == "Okrąg":
            shape_id = self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=width)

        # Dodajemy narysowany kształt do listy
        self.shapes.append(shape_id)

    def on_button_press(self, event):
        # Sprawdzenie, czy kliknięto na kształt
        self.selected_shape = self.canvas.find_closest(event.x, event.y)

        if self.selected_shape:
            # Ustalamy przesunięcie względem pozycji kursora
            coords = self.canvas.coords(self.selected_shape)
            self.offset_x = event.x - coords[0]
            self.offset_y = event.y - coords[1]

    def on_mouse_drag(self, event):
        if self.selected_shape:
            # Obliczenie nowej pozycji kształtu
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y

            # Sprawdzenie, czy nowa pozycja pozostaje w obrębie płótna
            coords = self.canvas.coords(self.selected_shape)

            # Warunki dla linii
            if self.shape_var.get() == "Linia":
                if (0 <= new_x <= self.canvas.winfo_width() and
                    0 <= new_y <= self.canvas.winfo_height() and
                    0 <= event.x - self.offset_x + (coords[2] - coords[0]) <= self.canvas.winfo_width() and
                    0 <= event.y - self.offset_y + (coords[3] - coords[1]) <= self.canvas.winfo_height()):
                    self.canvas.move(self.selected_shape, new_x - coords[0], new_y - coords[1])

            # Warunki dla prostokąta
            elif self.shape_var.get() == "Prostokąt":
                if (0 <= new_x <= self.canvas.winfo_width() and
                    0 <= new_y <= self.canvas.winfo_height() and
                    0 <= event.x - self.offset_x + (coords[2] - coords[0]) <= self.canvas.winfo_width() and
                    0 <= event.y - self.offset_y + (coords[3] - coords[1]) <= self.canvas.winfo_height()):
                    self.canvas.move(self.selected_shape, new_x - coords[0], new_y - coords[1])

            # Warunki dla okręgu
            elif self.shape_var.get() == "Okrąg":
                if (0 <= new_x <= self.canvas.winfo_width() and
                    0 <= new_y <= self.canvas.winfo_height() and
                    0 <= event.x - self.offset_x + (coords[2] - coords[0]) <= self.canvas.winfo_width() and
                    0 <= event.y - self.offset_y + (coords[3] - coords[1]) <= self.canvas.winfo_height()):
                    self.canvas.move(self.selected_shape, new_x - coords[0], new_y - coords[1])
