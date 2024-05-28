from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import nkot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = Tk()
root.title("PokoAI")
root.geometry("650x400") 

path_to_file = str

def get_path_to_file():
    try:
        path_to_file = askopenfilename(title = "Выберите csv файл!", filetypes=[("CSV files", "*.csv")])
        if path_to_file:
            choise_file = os.path.splitext(path_to_file)[1].lower()
        if choise_file == ".csv":
            text_path.insert(0, path_to_file)
            return path_to_file
    except:
        text_path.insert(0, os.getcwd() + "/LOGI.csv")
        return os.getcwd() + "/LOGI.csv"


butt_choise_file = ttk.Button(root, text = "Выбрать файл", command=get_path_to_file)
butt_choise_file.grid(row = 5, column = 1, padx = 10, pady = 10)

butt_start = ttk.Button(root, text = "Начать обучение")
butt_start.grid(row = 5, column = 2)


text_path = ttk.Entry(root)
text_path.place(x = 10, y = 45, width = 450)

#figure = plt.subplot()


root.mainloop()