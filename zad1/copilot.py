import tkinter as tk
from tkinter import colorchooser, simpledialog
import json

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.shape = None
        self.start_x = None
        self.start_y = None
        self.current_item = None
        self.shapes = []
        
        self.create_buttons()
        self.create_inputs()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        
    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.line_button = tk.Button(button_frame, text="Narysuj linię", command=self.set_line)
        self.line_button.pack(side=tk.LEFT)
        
        self.rect_button = tk.Button(button_frame, text="Narysuj prostokąt", command=self.set_rect)
        self.rect_button.pack(side=tk.LEFT)
        
        self.circle_button = tk.Button(button_frame, text="Narysuj okrąg", command=self.set_circle)
        self.circle_button.pack(side=tk.LEFT)
        
        self.save_button = tk.Button(button_frame, text="Zapisz", command=self.save_shapes)
        self.save_button.pack(side=tk.LEFT)
        
        self.load_button = tk.Button(button_frame, text="Wczytaj", command=self.load_shapes)
        self.load_button.pack(side=tk.LEFT)
        
    def create_inputs(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.x1_entry = tk.Entry(input_frame)
        self.x1_entry.pack(side=tk.LEFT)
        self.x1_entry.insert(0, "x1")
        
        self.y1_entry = tk.Entry(input_frame)
        self.y1_entry.pack(side=tk.LEFT)
        self.y1_entry.insert(0, "y1")
        
        self.x2_entry = tk.Entry(input_frame)
        self.x2_entry.pack(side=tk.LEFT)
        self.x2_entry.insert(0, "x2")
        
        self.y2_entry = tk.Entry(input_frame)
        self.y2_entry.pack(side=tk.LEFT)
        self.y2_entry.insert(0, "y2")
        
        self.color_entry = tk.Entry(input_frame)
        self.color_entry.pack(side=tk.LEFT)
        self.color_entry.insert(0, "color")
        
        self.width_entry = tk.Entry(input_frame)
        self.width_entry.pack(side=tk.LEFT)
        self.width_entry.insert(0, "width")
        
        self.draw_line_button = tk.Button(input_frame, text="Rysuj linię", command=self.draw_line)
        self.draw_line_button.pack(side=tk.LEFT)
        
        self.draw_rect_button = tk.Button(input_frame, text="Rysuj prostokąt", command=self.draw_rect)
        self.draw_rect_button.pack(side=tk.LEFT)
        
        self.draw_circle_button = tk.Button(input_frame, text="Rysuj okrąg", command=self.draw_circle)
        self.draw_circle_button.pack(side=tk.LEFT)
        
    def set_line(self):
        self.shape = "line"
        
    def set_rect(self):
        self.shape = "rect"
        
    def set_circle(self):
        self.shape = "circle"
        
    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.shape == "line":
            self.current_item = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y)
        elif self.shape == "rect":
            self.current_item = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y)
        elif self.shape == "circle":
            self.current_item = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y)
        
    def on_drag(self, event):
        if self.current_item:
            if self.shape == "line":
                self.canvas.coords(self.current_item, self.start_x, self.start_y, event.x, event.y)
            elif self.shape == "rect":
                self.canvas.coords(self.current_item, self.start_x, self.start_y, event.x, event.y)
            elif self.shape == "circle":
                self.canvas.coords(self.current_item, self.start_x, self.start_y, event.x, event.y)
        
    def on_release(self, event):
        if self.current_item:
            self.shapes.append(self.current_item)
            self.current_item = None
        
    def on_double_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.current_item = item[0]
            self.canvas.itemconfig(self.current_item, outline="red")
            new_size = simpledialog.askstring("Zmiana rozmiaru", "Podaj nowe wymiary (x1, y1, x2, y2):")
            if new_size:
                coords = list(map(int, new_size.split(',')))
                self.canvas.coords(self.current_item, *coords)
            self.canvas.itemconfig(self.current_item, outline="black")
            self.current_item = None
        
    def draw_line(self):
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())
        color = self.color_entry.get()
        width = int(self.width_entry.get())
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        
    def draw_rect(self):
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())
        color = self.color_entry.get()
        width = int(self.width_entry.get())
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)
        
    def draw_circle(self):
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())
        color = self.color_entry.get()
        width = int(self.width_entry.get())
        self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=width)
        
    def save_shapes(self):
        shapes = []
        for shape in self.shapes:
            coords = self.canvas.coords(shape)
            shape_type = self.canvas.type(shape)
            color = self.canvas.itemcget(shape, "outline")
            width = self.canvas.itemcget(shape, "width")
            shapes.append({"type": shape_type, "coords": coords, "color": color, "width": width})
        with open("shapes.json", "w") as f:
            json.dump(shapes, f)
        
    def load_shapes(self):
        with open("shapes.json", "r") as f:
            shapes = json.load(f)
        for shape in shapes:
            if shape["type"] == "line":
                self.canvas.create_line(*shape["coords"], fill=shape["color"], width=shape["width"])
            elif shape["type"] == "rectangle":
                self.canvas.create_rectangle(*shape["coords"], outline=shape["color"], width=shape["width"])
            elif shape["type"] == "oval":
                self.canvas.create_oval(*shape["coords"], outline=shape["color"], width=shape["width"])

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()