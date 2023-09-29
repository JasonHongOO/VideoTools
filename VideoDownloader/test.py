import tkinter as tk
from tkinter import OptionMenu

def option_selected(*args):
    selected_option = option_var.get()
    selected_index = options.index(selected_option)
    print("Selected Index:", selected_index)

root = tk.Tk()

option_var = tk.StringVar()
option_var.set("Option 1")  # 设置默认选项
options = ["Option 1", "Option 2", "Option 3"]

option_menu = OptionMenu(root, option_var, *options)
option_menu.pack()

option_var.trace("w", option_selected)

root.mainloop()