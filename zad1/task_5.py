import tkinter as tk

class Task5:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.entries = {}
        self.shape_var = tk.StringVar(value="Linia")
        self.shapes = []
        self.selected_shape = None
        self.is_resizing = False
        self.offset_x = 0
        self.offset_y = 0
        self.initial_coords = None
        self.create_gui()

    def create_gui(self):
        self.root.title("Rysowanie, przesuwanie i zmiana rozmiaru kształtów")

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

        # Przycisk czyszczący płótno
        btn_clear = tk.Button(self.root, text="Wyczyść płótno", command=self.clear_canvas)
        btn_clear.pack()

        btn_back = tk.Button(self.root, text="Powrót", command=self.back_to_menu)
        btn_back.pack()

        self.adjust_window_size()

        # Ustawienie funkcji do przesuwania i zmiany rozmiaru kształtów
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<Double-1>", self.on_double_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()

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

        self.shapes.append(shape_id)

    def on_button_press(self, event):
        # Sprawdzenie, czy kliknięto na kształt
        self.selected_shape = self.canvas.find_closest(event.x, event.y)

        if self.selected_shape:
            # Ustalamy przesunięcie względem pozycji kursora
            coords = self.canvas.coords(self.selected_shape)
            self.offset_x = event.x - coords[0]
            self.offset_y = event.y - coords[1]

            # Zachowujemy początkowe współrzędne dla okręgów
            if self.shape_var.get() == "Okrąg":
                self.initial_coords = coords[:]

    def on_mouse_drag(self, event):
        if self.selected_shape:
            if self.is_resizing:
                self.on_resize(event)  # Jeżeli zmieniamy rozmiar
            else:
                # Przesuwanie kształtu
                new_x = event.x - self.offset_x
                new_y = event.y - self.offset_y
                self.canvas.move(self.selected_shape, new_x - self.canvas.coords(self.selected_shape)[0],
                                 new_y - self.canvas.coords(self.selected_shape)[1])

    def on_double_click(self, event):
        # Sprawdzenie, czy kliknięto na kształt
        self.selected_shape = self.canvas.find_closest(event.x, event.y)

        if self.selected_shape:
            # Rozpoczęcie zmiany rozmiaru
            self.is_resizing = True
            self.show_resizing_message()

            # Ustawienie kursora na zmiany rozmiaru
            self.canvas.bind("<B1-Motion>", self.on_resize)

    def on_resize(self, event):
        if self.is_resizing and self.selected_shape:
            coords = self.canvas.coords(self.selected_shape)
            if self.shape_var.get() == "Linia":
                # Dostosowanie końców linii
                self.canvas.coords(self.selected_shape, coords[0], coords[1], event.x, event.y)
            elif self.shape_var.get() == "Prostokąt":
                self.canvas.coords(self.selected_shape, coords[0], coords[1], event.x, event.y)
            elif self.shape_var.get() == "Okrąg":
                # Oblicz nowy promień
                center_x = (coords[0] + coords[2]) / 2
                center_y = (coords[1] + coords[3]) / 2
                radius = max(abs(event.x - center_x), abs(event.y - center_y))  # Zachowanie proporcji
                new_x1 = center_x - radius
                new_y1 = center_y - radius
                new_x2 = center_x + radius
                new_y2 = center_y + radius
                self.canvas.coords(self.selected_shape, new_x1, new_y1, new_x2, new_y2)

    def show_resizing_message(self):
        self.message_label = tk.Label(self.root, text="Zmiana rozmiaru", bg="yellow")
        self.message_label.pack()

    def hide_resizing_message(self):
        if hasattr(self, 'message_label'):
            self.message_label.destroy()

    def on_button_release(self, event):
        if self.selected_shape:
            if self.is_resizing:
                self.hide_resizing_message()
                self.is_resizing = False  # Zakończenie procesu zmiany rozmiaru
            # Po zakończeniu zmiany rozmiaru, umożliwiamy przesuwanie
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        
        self.selected_shape = None  # Resetowanie wybranego kształtu


# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = Task5(root)
    root.mainloop()
