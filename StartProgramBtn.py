import subprocess
import tkinter as tk

def run_main_script():
    subprocess.Popen(["python", r"C:\Users\JasonHong/Desktop/CODE/Python/Script/Tools/Video/Update/Main.py"])

root = tk.Tk()
root.title("Always On Top Button")
root.wm_attributes("-topmost", 1)

button = tk.Button(root, text="執行程式", command=run_main_script, width=10, height=5)
button.pack()


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# print(screen_width, screen_height)
button_width = 100
button_height = 30
button_x = 0 + button_width + 10
button_y = 0 + button_height + 10
# root.geometry(f"{button_width}x{button_height}+{button_x}+{button_y}")
root.geometry("300x100")

root.mainloop()
