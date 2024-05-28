from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import nkot

root = Tk()
root.title("PokoAI")
root.geometry("650x400") 

path_to_file = ''

def get_path_to_file():
    text_path.delete(0, END)
    try:
        path_to_file = askopenfilename(title = "Выберите csv файл!", filetypes=[("CSV files", "*.csv")])
        if path_to_file:
            choise_file = os.path.splitext(path_to_file)[1].lower()
        if choise_file == ".csv":
            text_path.insert(0, path_to_file)
            return path_to_file
    except:
        path_to_file = os.getcwd().replace("\\", "/") + "/LOGI.csv"
        text_path.insert(0, path_to_file)
        return path_to_file.replace("\\", "/")


butt_choise_file = ttk.Button(root, text = "Выбрать файл", command=get_path_to_file)
butt_choise_file.grid(row = 5, column = 1, padx = 10, pady = 10)

butt_start = ttk.Button(root, text = "Начать обучение")
butt_start.grid(row = 5, column = 2)


text_path = ttk.Entry(root)
text_path.place(x = 10, y = 45, width = 450)

#figure = plt.subplot()


root.mainloop()