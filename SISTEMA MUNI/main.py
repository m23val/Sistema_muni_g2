from tkinter import Tk
from ui.menu_general import MenuGeneral

if __name__ == "__main__":
    root = Tk()
    #app = MainWindow(root)
    app = MenuGeneral(root)
    root.mainloop()
