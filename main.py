from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os

root = Tk()
root.title("PokoAI")
root.geometry("650x400") 

path_to_file = str

def get_path_to_file():
    path_to_file = askopenfilename(title = "Выберите csv файл!", filetypes=[("CSV files", "*.csv")])
    if path_to_file:
        choise_file = os.path.splitext(path_to_file)[1].lower()
    if choise_file == ".csv":
        return path_to_file
    else:
        text_path.insert("/Users/poko/Documents/PythonProject/ML_Trading/LOGI.csv")
        return "/Users/poko/Documents/PythonProject/ML_Trading/LOGI.csv"

button_start = ttk.Button(root, text = "Выбрать файл", command=get_path_to_file)
button_start.place(x = 10, y = 10)

text_path = ttk.Entry(root)
text_path.place(x = 10, y = 45, width = 450)


root.mainloop()