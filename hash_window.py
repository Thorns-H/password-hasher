from tkinter import *
import pathlib
import hashlib
import os

# Constants
WINDOW_SIZE = "450x350"
BACKGROUND_COLOR = "#161616"
FONT_COLOR = "#FFFFFF"
PATH = pathlib.Path(__file__).parent.resolve() # Path to this project folder.
DELETE = False
SYSTEM = ""

# We need a function to delete every Label when we make a new one to replace it. 
def clear(function):
    global DELETE

    function.destroy()
    DELETE = False

# We need a function to bind the keyboard.
def enter_bind(event):
    get_text()

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
        finished_hash = Label(root, text = 'Type Something!', bg = BACKGROUND_COLOR, fg = FONT_COLOR)
        finished_hash.pack()

        DELETE = True  # Everytime we make a label that's reusable we need to enable this with True.
    else:
        text = hashlib.md5(text.encode())
        text = text.hexdigest()
    
        # We consider this a success!
        finished_hash = Label(root, text = 'Hash Complete!', bg = BACKGROUND_COLOR, fg = FONT_COLOR)
        finished_hash.pack()

        if hashed.get() != '':
            hashed.delete(0, 'end')

        hashed.config(state = NORMAL)
        hashed.insert(0,'')
        hashed.insert(0,text)

        DELETE = True  

def main_window():
    global to_hash, root, hashed 

    # Window Configuration
    root = Tk()
    root.geometry(WINDOW_SIZE)
    root.configure(bg = BACKGROUND_COLOR)
    root.resizable(0,0)
    if os.name in ["nt"]: # This is just for windows users, linux doesn't support .ico images.
        root.iconbitmap(f'{PATH}/images/icon.ico')
    root.title('Hash Converter')

    # This is the top image configuration, if you want to change it make sure to make it .gif!
    title_image = PhotoImage(file=f'{PATH}/images/title.gif')
    title_image_label = Label(root, image = title_image , bg = BACKGROUND_COLOR)
    title_image_label.pack()

    # Typing Boxes.
    password_title = PhotoImage(file=f'{PATH}/images/password.gif')
    password_image_label = Label(root, image = password_title, bg = BACKGROUND_COLOR)
    password_image_label.pack()
    to_hash = Entry(root, font = ('Calibri',12), show = '*', justify = CENTER)
    to_hash.pack(pady = 2)
    to_hash.focus()
    hash_title = PhotoImage(file=f'{PATH}/images/hash.gif')
    hash_image_label = Label(root, image = hash_title, bg = BACKGROUND_COLOR)
    hash_image_label.pack()
    hashed = Entry(root, font = ('Calibri',12), width = 40)
    hashed.pack(pady = 2)
    hashed.config(state = DISABLED, justify = CENTER)

    root.bind('<Return>', enter_bind) # This is just a bind to the enter button.

    accept_button = Button(root, text = 'Hash it!' , font = ('Calibri',10), command = get_text)
    accept_button.pack(pady = 10)

    root.mainloop()