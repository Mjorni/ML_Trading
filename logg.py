from tkinter import *
from tkinter import ttk, messagebox
from tkinter.messagebox import showerror, showinfo
import json

log_state = False
glob_log = None

def new_win():
    logg_window = Tk()
    logg_window.geometry('600x400')
    logg_window.title("Экран авторизации")
    
    # Логгин
    logg_label = Label(logg_window, text = "Логин")
    logg_label.grid(column = 0, row = 0)
    logg_entry = Entry(logg_window, text = "Логин")
    logg_entry.grid(column = 0, row = 1)
    # Пароль
    pass_label = Label(logg_window, text = "Пароль")
    pass_label.grid(column = 0, row = 2)
    pass_entry = Entry(logg_window, text = "Пароль")
    pass_entry.grid(column = 0, row = 3)

    def login():
        login = logg_entry.get()
        password = pass_entry.get()

        with open("Log.json", "r") as f:
            data = json.load(f)
            if login in data.keys():
                if password == data[login]:
                    global log_state, glob_log
                    glob_log = login
                    log_state = True
                    showinfo(title = "Информация!", message = "Авторизация прошла успешно")
                else:
                    showerror(title = "Ошибка!", message = "Неверный пароль!")
            else:
                showerror(title = "Ошибка!", message = "Такого логина не существует!\nЗарегестрируйтесь!")

    def reg():
        login = logg_entry.get()
        password = pass_entry.get()
        try:
            with open('Log.json', 'r', encoding='utf-8') as f:
                logins = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logins = {}
        
        if login in logins.keys():
            showerror(title = "Ошибка!", message = "Данный логин занят")
        else:
            with open('Log.json', 'w', encoding='utf-8') as f:
                logins[login] = password
                json.dump(logins, f)
                showinfo(title = "Информация", message = "Регистрация прошла успешно")

    def save_notes():
        if log_state:
            print("+")
            text_on_notes = note_entry.get("1.0","end-1c")
            print(text_on_notes)
            with open('note.txt', 'r+') as f:
                f.write("".join(text_on_notes))
        else:
            print("-")

            
    # Кнопки
    logg_button = Button(logg_window, text = "Войти", command = login)
    logg_button.grid(column = 0, row = 4, sticky = W, pady = 5)
    logg_button = Button(logg_window, text = "Регистрация", command = reg)
    logg_button.grid(column = 0, row = 4, sticky = E, pady = 5)
    
    note_entry = Text(logg_window, width = 50, height = 15)
    note_entry.grid(column = 0, pady = 5, sticky = E, columnspan = 10)
    note_save_button = Button(logg_window, text = "Сохранить", command = save_notes)
    note_save_button.grid(column = 0)
    logg_button = Button(logg_window, text = "Закрыть окно регистрации", command = logg_window.destroy)
    logg_button.grid(column = 5, row = 6)
    logg_window.mainloop()

if __name__ == '__main__':
    new_win()