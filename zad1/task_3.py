import tkinter as tk

class Task3:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.points = []
        self.create_gui()

    def create_gui(self):
        self.root.title("Rysowanie przy użyciu myszy")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.add_point)

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

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        if len(self.points) > 1:
            self.canvas.create_line(self.points[-2], self.points[-1], fill="blue", width=2)
