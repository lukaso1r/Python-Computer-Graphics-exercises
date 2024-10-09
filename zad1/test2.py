import tkinter as tk
import json

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.shapes = []

        # Create buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        self.line_button = tk.Button(self.button_frame, text="Narysuj linię", command=self.draw_line)
        self.line_button.pack(side=tk.LEFT)
        self.rect_button = tk.Button(self.button_frame, text="Narysuj prostokąt", command=self.draw_rect)
        self.rect_button.pack(side=tk.LEFT)
        self.circle_button = tk.Button(self.button_frame, text="Narysuj okrąg", command=self.draw_circle)
        self.circle_button.pack(side=tk.LEFT)

        # Create input fields
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()
        self.x1_label = tk.Label(self.input_frame, text="X1:")
        self.x1_label.pack(side=tk.LEFT)
        self.x1_entry = tk.Entry(self.input_frame, width=5)
        self.x1_entry.pack(side=tk.LEFT)
        self.y1_label = tk.Label(self.input_frame, text="Y1:")
        self.y1_label.pack(side=tk.LEFT)
        self.y1_entry = tk.Entry(self.input_frame, width=5)
        self.y1_entry.pack(side=tk.LEFT)
        self.x2_label = tk.Label(self.input_frame, text="X2:")
        self.x2_label.pack(side=tk.LEFT)
        self.x2_entry = tk.Entry(self.input_frame, width=5)
        self.x2_entry.pack(side=tk.LEFT)
        self.y2_label = tk.Label(self.input_frame, text="Y2:")
        self.y2_label.pack(side=tk.LEFT)
        self.y2_entry = tk.Entry(self.input_frame, width=5)
        self.y2_entry.pack(side=tk.LEFT)
        self.color_label = tk.Label(self.input_frame, text="Kolor:")
        self.color_label.pack(side=tk.LEFT)
        self.color_entry = tk.Entry(self.input_frame, width=10)
        self.color_entry.pack(side=tk.LEFT)
        self.thickness_label = tk.Label(self.input_frame, text="Grubość:")
        self.thickness_label.pack(side=tk.LEFT)
        self.thickness_entry = tk.Entry(self.input_frame, width=5)
        self.thickness_entry.pack(side=tk.LEFT)

        # Create canvas bindings
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<Double-Button-1>", self.resize_shape)

        # Create menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save to JSON", command=self.save_to_json)
        self.file_menu.add_command(label="Load from JSON", command=self.load_from_json)

    def draw_line(self):
        self.draw_shape("line")

    def draw_rect(self):
        self.draw_shape("rect")

    def draw_circle(self):
        self.draw_shape("circle")

    def draw_shape(self, shape_type):
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())
        color = self.color_entry.get()
        thickness = int(self.thickness_entry.get())
        if shape_type == "line":
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=thickness)
        elif shape_type == "rect":
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, width=thickness)
        elif shape_type == "circle":
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=thickness)
        self.shapes.append({"type": shape_type, "coords": [x1, y1, x2, y2], "color": color, "thickness": thickness})

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def end_draw(self, event):
        self.end_x = event.x
        self .end_y = event.y
        self.draw_shape("line")

    def resize_shape(self, event):
        # TO DO: implement shape resizing
        pass

    def save_to_json(self):
        with open("shapes.json", "w") as f:
            json.dump(self.shapes, f)

    def load_from_json(self):
        with open("shapes.json", "r") as f:
            self.shapes = json.load(f)
        self.canvas.delete("all")
        for shape in self.shapes:
            if shape["type"] == "line":
                self.canvas.create_line(*shape["coords"], fill=shape["color"], width=shape["thickness"])
            elif shape["type"] == "rect":
                self.canvas.create_rectangle(*shape["coords"], fill=shape["color"], outline=shape["color"], width=shape["thickness"])
            elif shape["type"] == "circle":
                self.canvas.create_oval(*shape["coords"], fill=shape["color"], outline=shape["color"], width=shape["thickness"])

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()