from tkinter import *
from ttkbootstrap import *
import pathlib
import hashlib
import os
from datetime import datetime
import json

# Constants
WINDOW_SIZE = "450x380"
BACKGROUND_COLOR = "#161616"
FONT_COLOR = "#FFFFFF"
PATH = pathlib.Path(__file__).parent.resolve() # Path to this project folder.
DELETE = False
SYSTEM = ""
data = {}
now = datetime.now()
current_hour = now.strftime("%H:%M:%S")

# We need a function to delete every Label when we make a new one to replace it. 
def clear(function):
    global DELETE

    function.destroy()
    DELETE = False

# We need a function to bind the keyboard.
def enter_bind(event):
    get_text()

# Function to put text in the disabled entry's.
def insert_text(entry, text):
    entry.config(state = NORMAL)
    entry.insert(0,'')
    entry.insert(0,text)

# This is where we need to put 
def get_text():
    global DELETE, finished_hash

    if DELETE == False:
        pass
    else:
        clear(finished_hash)

    text = to_hash.get()

    # We consider this an error, when the user doesn't type something and we don't have anything to hash!
    if text in [""]:
        finished_hash = ttk.Label(hasher, text = 'Type Something!', style='danger.TLabel', font=('Helvetica', 12, 'bold'))
        finished_hash.pack()

        DELETE = True  # Everytime we make a label that's reusable we need to enable this with True.
    else:
        text = hashlib.md5(text.encode())
        bytes_equivalent = text.digest()
        text = text.hexdigest()
    
        # We consider this a success!
        finished_hash = ttk.Label(hasher, text = 'Hash Complete!', style='success.TLabel', font=('Helvetica', 12, 'bold'))
        finished_hash.pack(pady = 10)

        if hashed_hexadecimal.get() and hashed_digest.get() != '':
            hashed_hexadecimal.delete(0, 'end')
            hashed_digest.delete(0, 'end')
        
        insert_text(hashed_hexadecimal, text)
        insert_text(hashed_digest, bytes_equivalent)

        now = datetime.now()
        current_hour = now.strftime("%H:%M:%S")

        data[current_hour] = text
        print(data)

        DELETE = True  

def export_data():
    global DELETE, finished_hash

    save=json.dumps(data,indent=4)
    file=open(f"{PATH}/exports/Work from {now}.json","w")

    file.write(save)
    file.close()

    if DELETE == False:
        pass
    else:
        clear(finished_hash)

    finished_hash = ttk.Label(hasher, text = 'JSON Exported!', style='success.TLabel', font=('Helvetica', 12, 'bold'))
    finished_hash.pack(pady = 10)

    DELETE = True

def main_window():
    global to_hash, root, to_hash, hashed_hexadecimal, hashed_digest , hasher

    # Window Style Configuration
    
    style = Style()
    style.theme_use('darkly')
    root = style.master

    # Initial Run

    data[now.strftime("%d/%b/%Y")] = f"logged at {current_hour}"

    # Window Configuration

    root.geometry(WINDOW_SIZE)
    root.resizable(0,0)
    if os.name in ["nt"]: # This is just for windows users, linux doesn't support .ico images.
        root.iconbitmap(f'{PATH}/images/icon.ico')
    root.title('Hash Converter')

    # Tabs Configuration

    tab_control = ttk.Notebook(root)
    hasher = ttk.Frame(tab_control)
    history = ttk.Frame(tab_control)
    tab_control.add(hasher, text = 'Hasher')
    tab_control.pack(expand=1, fill = 'both')
    
    # Hash Tab

    title_label = ttk.Label(hasher, text = "Password Hasher", font= ('Helvica',30,'bold'))
    title_label.pack(pady = 5)
    credits_label = ttk.Label(hasher, text = "Developed by ThornsH on Github", font= ('Helvica',8,'bold'))
    credits_label.pack(pady = 10)

    # Typing Boxes.

    password_label = ttk.Label(hasher, text = "Password :", font = ('Helvica',10,'bold'))
    password_label.pack()

    to_hash = Entry(hasher, font = ('Calibri',12), show = '*', justify = CENTER)
    to_hash.pack(pady = 2)
    to_hash.focus()

    hash_hex_label = ttk.Label(hasher, text = "Hexadecial Encode :", font = ('Helvica',10,'bold'))
    hash_hex_label.pack()

    hashed_hexadecimal = Entry(hasher, font = ('Calibri',12), width = 40)
    hashed_hexadecimal.pack(pady = 2)
    hashed_hexadecimal.config(state = DISABLED, justify = CENTER)

    hash_dig_label = ttk.Label(hasher, text = "Byte Equivalent :", font = ('Helvica',10,'bold'))
    hash_dig_label.pack()
    hashed_digest = Entry(hasher, font = ('Calibri',12), width = 40)
    hashed_digest.pack(pady = 2)
    hashed_digest.config(state = DISABLED, justify = CENTER)

    root.bind('<Return>', enter_bind) # This is just a bind to the enter button.

    accept_button = Button(hasher, text = 'Hash it!' , font = ('Helvica',10,'bold'), command = get_text)
    accept_button.place(x = 110, y = 290)
    save_button = Button(hasher, text = 'Export JSON!' , font = ('Helvica',10,'bold'), command = export_data)
    save_button.place(x = 200, y = 290)

    root.mainloop()