# https://blog.csdn.net/aqqwvfbukn/article/details/121399647, https://blog.csdn.net/qq_59142194/article/details/123937365

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Treeview demo')
        self.geometry('620x200')

        self.tree = self.create_tree_widget()

    def create_tree_widget(self):
        columns = ('first_name', 'last_name', 'email')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('first_name', text='First Name')
        tree.heading('last_name', text='Last Name')
        tree.heading('email', text='Email')

        tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # generate sample data
        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

        # add data to the treeview
        i = 0
        for contact in contacts:
            tree.insert('', tk.END, values=contact,tag=i)
            i+=1

        tree.tag_bind('1hang', '<Button-1>', lambda even: print('奇数行'))
        tree.tag_bind('2hang', '<Button-1>', lambda even: print('偶数行'))

        return tree

    def item_selected(self, event):
        print(event.x,event.y)
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            # show a message
            showinfo(title='Information', message=','.join(record))


if __name__ == '__main__':
    app = App()
    app.mainloop()