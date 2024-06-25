from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, LSTM, Dropout, Activation # type: ignore


root = Tk()
root.title("PokoAI")
root.geometry("1200x800") 

file_path = None
df = None

def get_path_to_file():
    """Запись пути до выбранного файла"""
    global file_path
    file_path = askopenfilename(title = "Необходимо выбрать csv файл", 
                                filetypes = [("CSV files", "*.csv")])
    text_path.delete(0, END)
    if file_path:
        text_path.insert(0, file_path)
    else:
        text_path.insert(0, "LOGI.csv")
        file_path = "LOGI.csv"
        

def get_previev():
    """Функция отображения графа"""
    global df
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df = preproc(df)
    ax.plot(df[["Open", "Close", "Low", "High"]], 
            label = ["Open", "Close", "Low", "High"], 
            linewidth = 0.5)
    ax.legend()

    canvas.draw()
    canvas.get_tk_widget().pack(side = LEFT)
    get_all_col([column for column in 
                 df.drop(['Date', 'Adj Close'], axis = 1)])

def preproc(df):
    "Предподготовка датафрейма"
    df.info()
    if df.isnull().sum().any():
        df = df.dropna(how = "any")
        print("Удалил все строки с пропуски")
        return df
    else:
        return df
      
def get_all_col(df):
    """отображение кнопок с названиями столбцов """
    choise_entry.pack(anchor = N)
    btt_start_train.pack(anchor = N)
    btt_test.pack(anchor = N)
    new_plot.pack(anchor = N)
    for i in df:
        butt = ttk.Button(text = i, 
                          command = lambda x = i:choise_coll(x))
        butt.pack(anchor = N, pady = 5)
    

def choise_coll(comm):
    "Обновление текстового поля"
    choise_entry.delete(0, END)
    choise_entry.insert(0, comm)
    

def new_graph():
    "Обновление рисунка"
    canvas.get_tk_widget().pack_forget()
    ax.clear()
    print(df[choise_entry.get()])
    ch_col = df[choise_entry.get()]
    plt.title(choise_entry.get())
    ax.plot(ch_col)

    canvas.draw()
    canvas.get_tk_widget().pack(side = LEFT)


butt_choise_file = ttk.Button(root, text = "Выбрать файл", 
                              command=get_path_to_file)
butt_choise_file.pack(anchor = NW, padx = 10, pady = 10)

butt_start = ttk.Button(root, text = "Выбираю этот файл!",
                         command = get_previev)
butt_start.pack(anchor = NW, padx = 10)

from logg import new_win
butt_start = ttk.Button(root, text = "Авторизация",
                         command = new_win)
butt_start.pack(anchor = NE, padx = 10)

text_path = ttk.Entry(root, width = 75)
text_path.pack(anchor = NW, padx = 10, pady = 10)

choise_entry = ttk.Entry(root, width = 23)

fig = plt.figure(figsize=(8, 6), dpi = 100)
ax = fig.add_subplot()
canvas = FigureCanvasTkAgg(fig, master = root) #холст

new_plot = ttk.Button(root, 
                      text = "Отобразить новый график", 
                      width = 25, command = new_graph)



"""РАЗДЕЛ С ОБУЧЕНИЕМ"""
lb = 10 
val = 0.9

model = Sequential([
            LSTM(256, input_shape = (lb, 1), return_sequences = True),
            LSTM(10),
            Dense(1)
        ])
model.compile(optimizer = 'adam', loss = 'mse')


#import tracemalloc

#   Разделение данных на тестовые и тренеровочные
def start_train():
    #Разбиение на тестовые и тренеровочные данные

    x,y = xyarray(stab_data(choise_entry.get()))

    x_train, x_test = x[:int(x.shape[0] * val)], x[int(x.shape[0] * val):]
    y_train, y_test = y[:int(x.shape[0] * val)], y[int(x.shape[0] * val):]
    
    print(f"""x train -> {x_train.shape}  
          \ny train -> {y_train.shape}  
          \nx test  -> {x_test.shape} 
          \ny test  -> {y_test.shape}""")
    
    get_res(x_train, y_train, x_test, y_test)
    

def get_res(x_train, y_train, x_test, y_test):
    "Обучение модели на выбранных данных"
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))
    model.fit(x_train, y_train, epochs = 50, shuffle=False)
    model.save("saved_model")
    model.evaluate(x_test, y_test)
    result_predict = model.predict(x_test)
    canvas.get_tk_widget().pack_forget()
    ax.clear()
    plt.title(f"Обученная модель на {choise_entry.get()}")
    ax.plot(result_predict, label = 'x - Предсказанные данные')
    ax.plot(y_test, label = 'y - Истиные данные')
    ax.legend()
    canvas.draw()
    canvas.get_tk_widget().pack(side = LEFT)


def stab_data(name_col):
    "Нормализация данных"
    column = df[name_col].astype('float')
    #train = column[:int(len(column))] #не обязательно. ничего не делает, в случае чего, позже можно будет удалить
    scale_col = MinMaxScaler()
    scale_col.fit(column.values.reshape(-1, 1))
    column = scale_col.transform(column.values.reshape(-1, 1))
    return column

def xyarray(data):
    "Разбиение массива на x y "
    x, y = [], []
    for i in range(len(data) - lb - 1):
        x.append(data[i:(i + lb), 0])
        y.append(data[(i + lb), 0])
    return np.array(x), np.array(y)


def test():
    df_test = pd.read_csv("AAPL.csv", parse_dates=["Date"])
    df_test = preproc(df_test)
    canvas.get_tk_widget().pack_forget()
    ax.clear()
    new_model = tf.keras.models.load_model('saved_model')
    df_test = df_test[choise_entry.get()]
    scale_col = MinMaxScaler()
    x_for_test = df_test.astype('float')
    scale_col.fit(x_for_test.values.reshape(-1, 1))
    x_for_test = scale_col.transform(x_for_test.values.reshape(-1, 1))
    print(x_for_test)
    y_for_test = new_model.predict(x_for_test)
    print(len(y_for_test))
    ax.plot(y_for_test, label = 'Предсказанные данные')
    df_test_v = df_test.astype('float')
    scale_col.fit(df_test_v.values.reshape(-1, 1))
    df_test_v = scale_col.transform(df_test_v.values.reshape(-1, 1))
    print(df_test_v == y_for_test)
    print(df_test_v)

    plt.title(choise_entry.get())
    ax.plot(df_test_v, label = 'Данные за июнь 2024')
    ax.legend()
    canvas.draw()
    canvas.get_tk_widget().pack(side = LEFT)

btt_start_train = ttk.Button(root, text = "Начать обучение", width = 25,  command = start_train)
btt_test = ttk.Button(root, text = "Проверка", width = 25,  command = test)


root.mainloop()