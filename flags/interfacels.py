import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from main import get_images_paths, load_json, save_json
import os

window = tk.Tk()
style = ttk.Style()
style.configure('Treeview',rowheight=35)

window.geometry('800x800')
window.title('Flags')

class App(tk.Frame):

    images = {}
    usedpath = os.path.join(os.getcwd(),'used.json')
    allitems = load_json(usedpath)
    currentItems = []
    data = []

    def __init__(self,master,heig,wid):
        super().__init__(master,height=heig,width=wid)
        self.pack()
        self.search = self.EntryFrame()
        self.table = self.TreeFrame()
        self.putAllItems()

    def EntryFrame(self):
        search_ent_var = tk.StringVar()
        entryFrame = tk.Frame(self)
        self.update()
        entryFrame.place(x=10,y=10,width=self.winfo_width(),height=self.winfo_height())

        label = tk.Label(entryFrame, text= "Busca por nombre de la bandera")
        label.grid(row=0,column=0, padx=5,pady=5)
        
        search_ent = tk.Entry(entryFrame,textvariable=search_ent_var)
        search_ent.grid(row=0,column=1,padx=5)
        search_ent_var.trace_add('write',self.searchFunction)

        used_button = tk.Button(entryFrame,text="Put as used", command=self.putToUsed)
        used_button.grid(row=0,column=2,padx=20)

        return search_ent_var

    def TreeFrame(self):
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
    
    def searchFunction(self,*args):
        search = myapp.search.get().capitalize()
        for name in self.allitems:
            if search in name and name not in self.currentItems:
                self.table.insert('',0,values = (name,self.allitems[name]),image=self.images[name])
                self.currentItems.append(name)
            elif search not in name and name in self.currentItems:
                self.deleteForName(name)
        self.sortHeading('flags',False)

        
    def sortHeading(self,col,reverse):
        data = [(self.table.set(child,'flags'),child) for child in self.table.get_children()]
        data.sort(reverse=reverse)
        
        for index, (val,child) in enumerate(data):
            self.table.move(child,'',index)

        self.table.heading(col,command=lambda:self.sortHeading(col,not reverse))

    def deleteForName(self,name_flag):
        aux = {self.table.set(child,'flags'):child for child in self.table.get_children()}
        self.table.delete(aux[name_flag])
        self.currentItems.remove(name_flag)

    def putToUsed(self):
        index = self.table.selection()[0]
        name = self.table.item(index)['values'][0]
        self.allitems[name] = True
        save_json(self.usedpath,self.allitems)
        self.deleteForName(name)
        self.searchFunction()

    def putAllItems(self):
        for path in get_images_paths():
            name = os.path.basename(path[:path.find('.')])
            with Image.open(path) as img_flag:
                self.images[name] = ImageTk.PhotoImage(img_flag.resize((50,25)))
            self.table.insert(parent="",index=tk.END,image=self.images[name],values=(name,self.allitems[name]))
            self.currentItems.append(name)

myapp = App(window,800,800) 

myapp.mainloop()