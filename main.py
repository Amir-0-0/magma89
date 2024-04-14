from magma import gost_zamena
import tkinter as tk
from tkinter import filedialog
import secrets
import string
from time import time


def generateRandomKey():
    'создание случайного клуча'
    simvols = string.ascii_letters + string.digits
    return ''.join(secrets.choice(simvols) for _ in range(32))




font = ('Comic Sans MS' , 13)
def browse_file():
    'Открывает диалог выбора файла и обновляет соответствующее поле'
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def clickGenerate():
    key = generateRandomKey()
    key_entry.delete(0, tk.END)
    key_entry.insert(0, key)

def encrypt_decrypt():
    file_path = file_path_entry.get()
    key = key_entry.get()

    try:
        start = time()
        gost_zamena(key, file_path)
        print(time()-start)
    except ValueError:
        result_label.config(text="Ошибка, попробуйте поменять ключ")



# Создание основного окна
app = tk.Tk()
app.title("Шифратор ГОСТ28147-89")

# Создание и настройка элементов интерфейса
file_path_label = tk.Label(app, font=font, text="Путь к файлу:")
file_path_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

file_path_entry = tk.Entry(app, font=font,width=40)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)

browse_button = tk.Button(app, font=font ,text="выбрать файл", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

generateKey_button = tk.Button(app, font=font ,text="создать случайный ключ", command=clickGenerate)
generateKey_button.grid(row=1, column=2, padx=10, pady=10)

key_label = tk.Label(app, font=font, text="Введите ключ(32 символа):")
key_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

key_entry = tk.Entry(app, font=font, width=40)
key_entry.grid(row=1, column=1, padx=10, pady=10)

encrypt_button = tk.Button(app, font=font, text="Шифровать/дешифровать", command=encrypt_decrypt)
encrypt_button.grid(row=3, column=1, pady=20)

result_label = tk.Label(app, font=font, text="")
result_label.grid(row=4, column=1, pady=10)

# Запуск главного цикла обработки событий
app.mainloop()
