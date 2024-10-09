import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
import json

class Shape:
    def __init__(self, canvas, shape_id, shape_type, coords, color, thickness):
        self.canvas = canvas
        self.id = shape_id
        self.type = shape_type
        self.coords = coords
        self.color = color
        self.thickness = thickness

    def to_dict(self):
        return {
            'type': self.type,
            'coords': self.coords,
            'color': self.color,
            'thickness': self.thickness
        }

    def update(self, coords=None, color=None, thickness=None):
        if coords:
            self.coords = coords
            self.canvas.coords(self.id, *coords)
        if color:
            self.color = color
            if self.type in ["rectangle", "circle"]:
                self.canvas.itemconfig(self.id, fill=color, outline=color)
            else:
                self.canvas.itemconfig(self.id, fill=color)  # Poprawka
        if thickness:
            self.thickness = thickness
            self.canvas.itemconfig(self.id, width=thickness)

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja do Rysowania")

        self.current_tool = None
        self.shapes = []
        self.current_shape = None
        self.start_x = None
        self.start_y = None
        self.pencil_mode = False
        self.selected_shape = None
        self.resizing = False

        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        # Górny panel z przyciskami rysowania
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_line = tk.Button(top_frame, text="Narysuj linię", command=self.select_line)
        self.btn_line.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_rect = tk.Button(top_frame, text="Narysuj prostokąt", command=self.select_rect)
        self.btn_rect.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_circle = tk.Button(top_frame, text="Narysuj okrąg", command=self.select_circle)
        self.btn_circle.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_pencil = tk.Button(top_frame, text="Ołówek", command=self.select_pencil)
        self.btn_pencil.pack(side=tk.LEFT, padx=2, pady=2)

        # **Nowy Przycisk: Wyczyść płótno**
        self.btn_clear = tk.Button(top_frame, text="Wyczyść płótno", command=self.clear_canvas, fg="red")
        self.btn_clear.pack(side=tk.LEFT, padx=10, pady=2)

        # Środkowe płótno
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Dolny panel z inputami
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Współrzędne
        tk.Label(bottom_frame, text="X1:").pack(side=tk.LEFT)
        self.entry_x1 = tk.Entry(bottom_frame, width=5)
        self.entry_x1.pack(side=tk.LEFT)

        tk.Label(bottom_frame, text="Y1:").pack(side=tk.LEFT)
        self.entry_y1 = tk.Entry(bottom_frame, width=5)
        self.entry_y1.pack(side=tk.LEFT)

        tk.Label(bottom_frame, text="X2:").pack(side=tk.LEFT)
        self.entry_x2 = tk.Entry(bottom_frame, width=5)
        self.entry_x2.pack(side=tk.LEFT)

        tk.Label(bottom_frame, text="Y2:").pack(side=tk.LEFT)
        self.entry_y2 = tk.Entry(bottom_frame, width=5)
        self.entry_y2.pack(side=tk.LEFT)

        # Kolor
        tk.Label(bottom_frame, text="Kolor:").pack(side=tk.LEFT, padx=(10,0))
        self.entry_color = tk.Entry(bottom_frame, width=10)
        self.entry_color.pack(side=tk.LEFT)
        self.btn_color = tk.Button(bottom_frame, text="Wybierz kolor", command=self.choose_color)
        self.btn_color.pack(side=tk.LEFT, padx=2)

        # Grubość
        tk.Label(bottom_frame, text="Grubość:").pack(side=tk.LEFT, padx=(10,0))
        self.entry_thickness = tk.Entry(bottom_frame, width=3)
        self.entry_thickness.pack(side=tk.LEFT)

        # Przyciski generowania kształtów z parametrów
        self.btn_generate_line = tk.Button(bottom_frame, text="Generuj linię", command=self.generate_line)
        self.btn_generate_line.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_generate_rect = tk.Button(bottom_frame, text="Generuj prostokąt", command=self.generate_rect)
        self.btn_generate_rect.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_generate_circle = tk.Button(bottom_frame, text="Generuj okrąg", command=self.generate_circle)
        self.btn_generate_circle.pack(side=tk.LEFT, padx=2, pady=2)

        # Przycisk Anuluj zmianę rozmiaru
        self.btn_cancel_resize = tk.Button(bottom_frame, text="Anuluj zmianę rozmiaru", command=self.cancel_resize)
        self.btn_cancel_resize.pack(side=tk.LEFT, padx=(20,2), pady=2)

        # Przycisk Zapisz i Odczytaj
        self.btn_save = tk.Button(bottom_frame, text="Zapisz do JSON", command=self.save_to_json)
        self.btn_save.pack(side=tk.RIGHT, padx=2, pady=2)

        self.btn_load = tk.Button(bottom_frame, text="Odczytaj z JSON", command=self.load_from_json)
        self.btn_load.pack(side=tk.RIGHT, padx=2, pady=2)

    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)

    def select_line(self):
        self.current_tool = "line"
        self.pencil_mode = False

    def select_rect(self):
        self.current_tool = "rectangle"
        self.pencil_mode = False

    def select_circle(self):
        self.current_tool = "circle"
        self.pencil_mode = False

    def select_pencil(self):
        self.current_tool = "pencil"
        self.pencil_mode = True

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.entry_color.delete(0, tk.END)
            self.entry_color.insert(0, color)

    def generate_line(self):
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
            color = self.entry_color.get() or "black"
            thickness = int(self.entry_thickness.get()) if self.entry_thickness.get() else 1
            line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=thickness)
            shape = Shape(self.canvas, line, "line", [x1, y1, x2, y2], color, thickness)
            self.shapes.append(shape)
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić prawidłowe wartości.")

    def generate_rect(self):
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
            color = self.entry_color.get() or "black"
            thickness = int(self.entry_thickness.get()) if self.entry_thickness.get() else 1
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=thickness)
            shape = Shape(self.canvas, rect, "rectangle", [x1, y1, x2, y2], color, thickness)
            self.shapes.append(shape)
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić prawidłowe wartości.")

    def generate_circle(self):
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            radius = int(self.entry_x2.get())  # W przypadku okręgu, x2 to promień
            color = self.entry_color.get() or "black"
            thickness = int(self.entry_thickness.get()) if self.entry_thickness.get() else 1
            x2 = x1 + radius
            y2 = y1 + radius
            circle = self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=thickness)
            shape = Shape(self.canvas, circle, "circle", [x1, y1, x2, y2], color, thickness)
            self.shapes.append(shape)
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić prawidłowe wartości.")

    def on_canvas_click(self, event):
        # Zaznaczanie kształtu
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            shape = self.get_shape_by_id(item[0])
            if shape:
                self.selected_shape = shape
                self.drag_data = {"x": event.x, "y": event.y}
        else:
            self.selected_shape = None

        if self.pencil_mode:
            self.current_shape = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=1)
            shape = Shape(self.canvas, self.current_shape, "pencil", [event.x, event.y, event.x, event.y], "black", 1)
            self.shapes.append(shape)

        elif self.current_tool in ["line", "rectangle", "circle"]:
            self.start_x = event.x
            self.start_y = event.y
            color = self.entry_color.get() or "black"
            thickness = int(self.entry_thickness.get()) if self.entry_thickness.get() else 1

            if self.current_tool == "line":
                self.current_shape = self.canvas.create_line(event.x, event.y, event.x, event.y, fill=color, width=thickness)
                shape = Shape(self.canvas, self.current_shape, "line", [self.start_x, self.start_y, self.start_x, self.start_y], color, thickness)

            elif self.current_tool == "rectangle":
                self.current_shape = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=color, width=thickness)
                shape = Shape(self.canvas, self.current_shape, "rectangle", [self.start_x, self.start_y, self.start_x, self.start_y], color, thickness)

            elif self.current_tool == "circle":
                self.current_shape = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=color, width=thickness)
                shape = Shape(self.canvas, self.current_shape, "circle", [self.start_x, self.start_y, self.start_x, self.start_y], color, thickness)

            # Dodaj nowo utworzony kształt do listy kształtów
            self.shapes.append(shape)

    def on_canvas_drag(self, event):
        if self.pencil_mode and self.current_shape:
            x1, y1, x2, y2 = self.canvas.coords(self.current_shape)
            self.canvas.coords(self.current_shape, x1, y1, event.x, event.y)
            shape = self.get_shape_by_id(self.current_shape)
            if shape:
                shape.coords = [x1, y1, event.x, y2]
        elif self.current_tool in ["line", "rectangle", "circle"] and self.current_shape:
            if self.current_tool == "line":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.current_tool == "rectangle":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.current_tool == "circle":
                radius = max(abs(event.x - self.start_x), abs(event.y - self.start_y))
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, self.start_x + radius, self.start_y + radius)
        elif self.selected_shape and not self.resizing:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.move_shape(self.selected_shape, dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_canvas_release(self, event):
        if self.pencil_mode and self.current_shape:
            self.current_shape = None
        elif self.current_tool in ["line", "rectangle", "circle"] and self.current_shape:
            color = self.entry_color.get() or "black"
            thickness = int(self.entry_thickness.get()) if self.entry_thickness.get() else 1
            shape = self.get_shape_by_id(self.current_shape)
            if shape:
                if shape.type in ["rectangle", "circle"]:
                    self.canvas.itemconfig(self.current_shape, outline=color, width=thickness)
                else:
                    self.canvas.itemconfig(self.current_shape, fill=color, width=thickness)
                shape.color = color
                shape.thickness = thickness
                # Aktualizuj współrzędne shape na podstawie aktualnych współrzędnych
                shape.coords = self.canvas.coords(self.current_shape)
            self.current_shape = None
            self.current_tool = None
        elif self.selected_shape:
            self.selected_shape = None

    def on_canvas_double_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            shape = self.get_shape_by_id(item[0])
            if shape:
                self.selected_shape = shape
                self.resizing = True
                self.highlight_shape(shape)
                # Prompt user for new parameters
                self.prompt_resize(shape)

    def prompt_resize(self, shape):
        if shape.type == "circle":
            new_radius = simpledialog.askinteger("Zmiana rozmiaru", "Podaj nowy promień:", parent=self.root, minvalue=1)
            if new_radius:
                x1, y1, _, _ = shape.coords
                x2 = x1 + new_radius
                y2 = y1 + new_radius
                shape.update(coords=[x1, y1, x2, y2])
        else:
            try:
                new_x1 = simpledialog.askinteger("Zmiana rozmiaru", "Podaj nowy X1:", parent=self.root)
                new_y1 = simpledialog.askinteger("Zmiana rozmiaru", "Podaj nowy Y1:", parent=self.root)
                new_x2 = simpledialog.askinteger("Zmiana rozmiaru", "Podaj nowy X2:", parent=self.root)
                new_y2 = simpledialog.askinteger("Zmiana rozmiaru", "Podaj nowy Y2:", parent=self.root)
                if None not in (new_x1, new_y1, new_x2, new_y2):
                    shape.update(coords=[new_x1, new_y1, new_x2, new_y2])
            except (ValueError, TypeError):
                messagebox.showerror("Błąd", "Nieprawidłowe wartości.")

        self.unhighlight_shape(shape)
        self.resizing = False
        self.selected_shape = None

    def cancel_resize(self):
        if self.resizing and self.selected_shape:
            self.unhighlight_shape(self.selected_shape)
            self.resizing = False
            self.selected_shape = None

    def highlight_shape(self, shape):
        self.canvas.itemconfig(shape.id, dash=(4, 2))

    def unhighlight_shape(self, shape):
        self.canvas.itemconfig(shape.id, dash=())

    def move_shape(self, shape, dx, dy):
        coords = shape.coords
        # Ensure the shape stays within canvas boundaries
        new_coords = [coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy]
        if new_coords[0] < 0:
            dx = -coords[0]
        if new_coords[1] < 0:
            dy = -coords[1]
        if new_coords[2] > self.canvas.winfo_width():
            dx = self.canvas.winfo_width() - coords[2]
        if new_coords[3] > self.canvas.winfo_height():
            dy = self.canvas.winfo_height() - coords[3]
        shape.update(coords=[coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy])

    def get_shape_by_id(self, shape_id):
        for shape in self.shapes:
            if shape.id == shape_id:
                return shape
        return None

    def save_to_json(self):
        if not self.shapes:
            messagebox.showinfo("Informacja", "Brak kształtów do zapisania.")
            return
        data = [shape.to_dict() for shape in self.shapes]
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Sukces", "Zapisano do pliku JSON.")
            except IOError as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku:\n{e}")

    def load_from_json(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.canvas.delete("all")
                self.shapes.clear()
                for item in data:
                    shape_type = item['type']
                    coords = item['coords']
                    color = item['color']
                    thickness = item['thickness']
                    if shape_type == "line":
                        shape_id = self.canvas.create_line(*coords, fill=color, width=thickness)
                    elif shape_type == "rectangle":
                        shape_id = self.canvas.create_rectangle(*coords, outline=color, width=thickness)
                    elif shape_type == "circle":
                        shape_id = self.canvas.create_oval(*coords, outline=color, width=thickness)
                    elif shape_type == "pencil":
                        shape_id = self.canvas.create_line(*coords, fill=color, width=thickness)
                    shape = Shape(self.canvas, shape_id, shape_type, coords, color, thickness)
                    self.shapes.append(shape)
                messagebox.showinfo("Sukces", "Wczytano z pliku JSON.")
            except (IOError, json.JSONDecodeError) as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać pliku:\n{e}")

    # **Nowa Metoda: clear_canvas**
    def clear_canvas(self):
        if not self.shapes:
            messagebox.showinfo("Informacja", "Płótno jest już puste.")
            return
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić płótno?")
        if confirm:
            self.canvas.delete("all")
            self.shapes.clear()
            messagebox.showinfo("Sukces", "Płótno zostało wyczyszczone.")

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
