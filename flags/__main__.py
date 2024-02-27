import os
import sys
import tkinter as tk
from tkinter import ttk
from get_images import (make_directory, get_flags_url,save_images)
from interfacels import App
from json_data import get_images_paths

#get_images initialization
cwd = os.getcwd()
dir_name = sys.argv[0] or 'flags'

flags_path = os.path.join(cwd,dir_name,'flags_images')
json_path = os.path.join(cwd,dir_name,'used.json')

make_directory(flags_path)
save_images(flags_path,get_flags_url())
images_path = get_images_paths(flags_path)

#App initialization
window = tk.Tk()
window.geometry('800x800')
window.title('Flags')

style = ttk.Style()
style.configure('Treeview',rowheight=35)

myapp = App(window,800,800,images_path,json_path)
myapp.mainloop()

