import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from json_data import load_json, save_json
import os

class App(tk.Frame):
    
    def __init__(self,master,heig,wid,images_path,json_path):
        super().__init__(master,height=heig,width=wid)
        self.pack()
        self.search = self.entry_frame()
        self.table = self.tree_frame()
        self.json_path = json_path
        self.images_path = images_path
        self.all_items = load_json(json_path,images_path)
        self.images = {}
        self.current_items = []
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
        search_ent_var.trace_add('write',self.search_function)

        used_button = tk.Button(entryFrame,text="Put as used", command=self.put_to_used)
        used_button.grid(row=0,column=2,padx=20)

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
        for name in self.all_items:
            if search in name and name not in self.current_items:
                self.table.insert('',0,values = (name,self.all_items[name]),image=self.images[name])
                self.current_items.append(name)
            elif search not in name and name in self.current_items:
                self.delete_for_name(name)
        self.sort_heading('flags',False)

        
    def sort_heading(self,col,reverse):
        data = [(self.table.set(child,'flags'),child) for child in self.table.get_children()]
        data.sort(reverse=reverse)
        
        for index, (val,child) in enumerate(data):
            self.table.move(child,'',index)

        self.table.heading(col,command=lambda:self.sort_heading(col,not reverse))

    def delete_for_name(self,name_flag):
        aux = {self.table.set(child,'flags'):child for child in self.table.get_children()}
        self.table.delete(aux[name_flag])
        self.current_items.remove(name_flag)

    def put_to_used(self):
        index = self.table.selection()[0]
        name = self.table.item(index)['values'][0]
        self.all_items[name] = True
        save_json(self.usedpath,self.all_items)
        self.delete_for_name(name)
        self.search_function()
        
    def put_all_items(self):
        for path in self.images_path:
            name = os.path.basename(path[:path.find('.')])
            with Image.open(path) as img_flag:
                self.images[name] = ImageTk.PhotoImage(img_flag.resize((50,25)))
            self.table.insert(parent="",index=tk.END,image=self.images[name],values=(name,self.all_items[name]))
            self.current_items.append(name)