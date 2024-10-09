import tkinter as tk

class Task1:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.create_gui()

    def create_gui(self):
        self.root.title("Rysowanie prymitywów")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        btn_line = tk.Button(self.root, text="Rysuj Linię", command=self.draw_line)
        btn_line.pack(side=tk.LEFT)

        btn_rect = tk.Button(self.root, text="Rysuj Prostokąt", command=self.draw_rectangle)
        btn_rect.pack(side=tk.LEFT)

        btn_circle = tk.Button(self.root, text="Rysuj Okrąg", command=self.draw_circle)
        btn_circle.pack(side=tk.LEFT)

        btn_back = tk.Button(self.root, text="Powrót", command=self.back_to_menu)
        btn_back.pack(side=tk.RIGHT, pady=10)

        self.adjust_window_size()

    def back_to_menu(self):
        # Powracamy do menu głównego
        for widget in self.root.winfo_children():
            widget.destroy()
        from main import MainApp
        MainApp(self.root)

    def adjust_window_size(self):
        self.root.update_idletasks()
        new_width = self.root.winfo_reqwidth()
        new_height = self.root.winfo_reqheight()
        self.root.geometry(f"{new_width + 20}x{new_height + 20}")

    def draw_line(self):
        self.canvas.create_line(150, 50, 200, 200, fill="red", width=3)

    def draw_rectangle(self):
        self.canvas.create_rectangle(100, 100, 300, 200, outline="black", width=2)

    def draw_circle(self):
        self.canvas.create_oval(150, 150, 250, 250, outline="green", width=2)
