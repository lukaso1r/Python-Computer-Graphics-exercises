import tkinter as tk
from task_1 import Task1
from task_2 import Task2
from task_3 import Task3
from task_4 import Task4
from task_5 import Task5
from task_6 import Task6

class MainApp:
    def __init__(self, root):
        self.root = root
        self.create_menu()

    def create_menu(self):
        self.root.title("Wybór zadania")
        self.root.geometry("800x500")

        # Usuwamy wszystkie istniejące widgety w głównym oknie
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Wybierz zadanie:", font=("Arial", 14))
        label.pack(pady=20)

        btn_task_1 = tk.Button(self.root, text="Rysowanie trzech prymitywów", command=lambda: self.run_task(Task1))
        btn_task_1.pack(pady=10)

        btn_task_2 = tk.Button(self.root, text="Podawanie parametrów rysowania", command=lambda: self.run_task(Task2))
        btn_task_2.pack(pady=10)

        btn_task_3 = tk.Button(self.root, text="Rysowanie przy użyciu myszy", command=lambda: self.run_task(Task3))
        btn_task_3.pack(pady=10)

        btn_task_4 = tk.Button(self.root, text="Przesuwanie przy użyciu myszy (uchwycenie np. za krawędź i przeciągnięcie)", command=lambda: self.run_task(Task4))
        btn_task_4.pack(pady=10)

        btn_task_5 = tk.Button(self.root, text="Przesuwanie przy użyciu myszy (uchwycenie np. za środek i przeciągnięcie)", command=lambda: self.run_task(Task5))
        btn_task_5.pack(pady=10)

        btn_task_6 = tk.Button(self.root, text="Zmiana  rozmiaru przy użyciu pola tekstowego (zaznaczenie obiektu i modyfikacja jego parametrów przy użyciu pola tekstowego).", command=lambda: self.run_task(Task6))
        btn_task_6.pack(pady=10)

        btn_quit = tk.Button(self.root, text="Zamknij", command=self.root.quit)
        btn_quit.pack(pady=20)

    def run_task(self, task_class):
        # Usuwamy wszystkie istniejące widgety przed uruchomieniem nowego zadania
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tworzymy instancję zadania i uruchamiamy jego GUI
        task_class(self.root)

        # Dostosowujemy rozmiar okna do zawartości
        self.root.update_idletasks()  # Aktualizujemy rozmiar widgetów
        self.root.geometry("")  # Ustalamy automatyczny rozmiar na podstawie zawartości

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
