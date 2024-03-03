import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from src.country import Country

class App(tk.Frame):
    
    def __init__(self,master,heig,wid,images_path,json_path):
        super().__init__(master,height=heig,width=wid)
        self.pack()
        self.search = self.entry_frame()
        self.table = self.tree_frame()
        self.countries = Country(json_path,images_path)
        # self.json_path = json_path
        # self.images_path = images_path
        # self.all_items = load_json(json_path,images_path)
        self.images = {}
        self.current_items = set()
        self.put_all_items()

    def entry_frame(self):
        search_ent_var = tk.StringVar()
        entryFrame = tk.Frame(self)
        self.update()
        entryFrame.place(x=10,y=10,width=self.winfo_width(),height=self.winfo_height())

        label = tk.Label(entryFrame, text= "Busca por nombre de la bandera")
        label.grid(row=0,column=0, padx=5,pady=5)
        
        search_ent = tk.Entry(entryFrame,textvariable=search_ent_var)
        search_ent.grid(row=0,column=1,padx=5)

        search_button = tk.Button(entryFrame,text="Search",command=self.search_function)
        search_button.grid(row=0,column=2,padx=20)
        
        used_button = tk.Button(entryFrame,text="Put as used", command=self.put_to_used)
        used_button.grid(row=0,column=3,padx=20)

        return search_ent_var

    def tree_frame(self):
        treeFrame = tk.Frame(self)
        treeFrame.place(x=10,y=50,width=800,height=700)

        columns_names = ('flags','used')
        table = ttk.Treeview(treeFrame,columns=columns_names)
        table.column('#0', width=200, minwidth=100, anchor='center')
        table.column('flags',width=400,minwidth=200)
        table.column('used',width=100,minwidth=100)

        table.heading('#0', text='Flag')
        table.heading('flags',text='Name')
        table.heading('used',text='Used')

        table.pack(fill=tk.BOTH,expand=True)

        return table
    
    def search_function(self,*args):
        search = self.search.get().capitalize()
        current = self.countries.search_function_levenshetein(search)

        to_delete = self.current_items.difference(current)
        to_add = current.difference(self.current_items)
        self.current_items = current

        aux = {self.table.set(child,'flags'):child for child in self.table.get_children()}
        indexes_to_delete = self.countries.delete_for_names(to_delete,aux)

        for idx in indexes_to_delete:
            self.table.delete(idx)
        for name in to_add:
            self.table.insert('',0,image=self.images[name],values=(name,self.countries.get_state(name)))
        self.sort_heading('flags',False)

        
    def sort_heading(self,col,reverse):
        data = [(self.table.set(child,'flags'),child) for child in self.table.get_children()]
        data.sort(reverse=reverse)
        
        for index, (val,child) in enumerate(data):
            self.table.move(child,'',index)

        self.table.heading(col,command=lambda:self.sort_heading(col,not reverse))

    def put_to_used(self):
        index = self.table.selection()[0]
        name = self.table.item(index)['values'][0]
        
        self.countries.put_to_used(name)
        self.table.delete(index)
        self.current_items.remove(name)
        self.search_function()
        
    def put_all_items(self):
        images_path = self.countries.get_images()
        for path in images_path:
            name = os.path.basename(path[:path.find('.')])
            with Image.open(path) as img_flag:
                self.images[name] = ImageTk.PhotoImage(img_flag.resize((50,25)))
            self.table.insert(parent="",index=tk.END,image=self.images[name],values=(name,self.countries.get_state(name)))
            self.current_items.add(name)