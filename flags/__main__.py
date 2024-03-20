import os
import sys
import tkinter as tk
from tkinter import ttk
from src.get_images import (make_directory, get_flags_url,save_images)
from interfacels import App
from paths import (json_path,flags_path,images_path)

#get_images initialization
make_directory(flags_path)
save_images(flags_path,get_flags_url())

#App initialization
window = tk.Tk()
window.geometry('800x800')
window.title('Flags')

style = ttk.Style()
style.configure('Treeview',rowheight=35)

myapp = App(window,800,800,images_path,json_path)
myapp.mainloop()

