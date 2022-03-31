# import dependencies
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
import subprocess
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

# create a pop up welcoming user to IDE
open_ide = Tk()

# main function to create pop up
def mainWin():
    open_ide.destroy()
    win = Tk()
    win.title("Welcome")
    win.geometry("750x230")
    win_label = Label(win, text="Welcome To Python Surge \n \n In this IDE You can write and run python files \n \n Please Save Before You Run \n \n Enjoy!!", font=('Yanone', 18), fg="sky blue").pack(
        pady=20)


# set time to open after main window
open_ide.after(420, mainWin)

# start main file and commands
window = Tk()

window.title("Python Surge - IDE")

menu = Menu(window)
window.config(menu=menu)

editor = ScrolledText(window, font=("corbel 12 bold"), wrap=None)
editor.pack(fill=BOTH, expand=1)
editor.focus()
file_path = ""

# add syntax highlighting
Percolator(editor).insertfilter(ColorDelegator())
editor.pack()

# crate a command that allows you to open a file from device
def open_file(event=None):
    global code, file_path

    open_path = askopenfilename(filetypes=[("Python File", "*.py")])
    file_path = open_path
    with open(open_path, "r") as file:
        code = file.read()
        editor.delete(1.0, END)
        editor.insert(1.0, code)


# create a shortcut to open file
window.bind("<Control-o>", open_file)


# create a function that allows you to save a file to  your device
def save_file(event=None):
    global code, file_path
    if file_path == '':
        save_path = asksaveasfilename(defaultextension=".py", filetypes=[("Python File", "*.py")])
        file_path = save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code)


# create a shortcut to save file that was just edited
window.bind("<Control-s>", save_file)


# create a function to save file for the first time with a certain name with '.py' extension
def save_as(event=None):
    global code, file_path
    save_path = asksaveasfilename(defaultextension=".py", filetypes=[("Python File", "*.py")])
    file_path = save_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code)


window.bind("<Control-S>", save_as) 


# create a function that alows you to run file
def run(event=None):
    cmd = f"python {file_path}"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    output_window.delete(1.0, END)
    output_window.insert(1.0, output)
    output_window.insert(1.0, error)


# create shortcut to run
window.bind("<F5>", run)


# create a function that allows you to close the file/ IDE
def close(event=None):
    window.destroy()


window.bind("<Control-q>", close)


# create a command that allows you to cut, copy and paste text
def cut_text(event=None):
    editor.event_generate(("<<Cut>>"))


def copy_text(event=None):
    editor.event_generate(("<<Copy>>"))


def paste_text(event=None):
    editor.event_generate(("<<Paste>>"))


# create menus/navigation
file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
view_menu = Menu(menu, tearoff=0)
theme_menu = Menu(menu, tearoff=0)

# name each menu
menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label="View", menu=view_menu)
menu.add_cascade(label="Theme", menu=theme_menu)

# create shortcut and names for commands
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=close)

# create a shortcut and name to run the files, copy, paste and cut.
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=cut_text)
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=copy_text)
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=paste_text)
run_menu.add_command(label="Run", accelerator="F5", command=run)

# create a command that allows you to show or hide the status bar
show_status_bar = BooleanVar()
show_status_bar.set(True)


def hide_statusbar():
    global show_status_bar
    if show_status_bar:
        status_bars.pack_forget()
        show_status_bar = False
    else:
        status_bars.pack(side=BOTTOM)
        show_status_bar = True


view_menu.add_checkbutton(label="Status Bar", onvalue=True, offvalue=0, variable=show_status_bar, command=hide_statusbar)

# change text to what you want to show on status bar
status_bars = ttk.Label(window, text="\t\t Surge Productions \t\t\t\t\t characters: 0 words: 0 \t\t\t\t Please Save Before You Run Your File - No Spaces\t\t")
status_bars.pack(side="top")

text_change = False


# create a command that automatically changes word count and character count
def change_word(event=None):
    global text_change
    if editor.edit_modified():
        text_change = True
        word = len(editor.get(1.0, "end-1c").split())
        chararcter = len(editor.get(1.0, "end-1c").replace(" ", ""))
        status_bars.config(text=f"Surge Productions \t\t\t\t\t characters: {chararcter} words: {word} \t\t\t\t Please Save Before You Run Your File - No Spaces\t\t")
    editor.edit_modified(False)


editor.bind("<<Modified>>", change_word)


# create a light theme
def light():
    editor.config(fg="black", bg="white")
    output_window.config(fg="black", bg="white")

# create a command to change themes
theme_menu.add_command(label="light", command=light)

# create a terminal/output window
output_window = ScrolledText(window, font=("corbel 12 bold"), wrap=None, height=9)
output_window.pack(fill=BOTH, expand=1)
window.mainloop()
