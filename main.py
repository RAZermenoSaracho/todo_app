import tkinter as tk
from gui.app_window import ToDoApp

if __name__ == "__main__":
    root = tk.Tk()
    root.tk.call("tk", "scaling", 1.0)
    app = ToDoApp(root)
    root.mainloop()
