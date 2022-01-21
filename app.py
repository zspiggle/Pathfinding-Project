import tkinter as tk



class Window(tk.Frame):

  canvas = 0

  def __init__(self):
    super().__init__()

    self.initUI()



  def initUI(self):

    self.master.title("Pathfinding")
    self.pack(fill=tk.BOTH, expand=1)

    self.canvas = tk.Canvas(self)
    # canvas.create_rectangle(30, 10, 120, 80,
    #     outline="#fb0", fill="#fb0")
    # canvas.create_rectangle(150, 10, 240, 80,
    #     outline="#f50", fill="#f50")
    # canvas.create_rectangle(270, 10, 370, 80,
    #     outline="#05f", fill="#05f")


    self.canvas.pack(fill=tk.BOTH, expand=1)

    #self._CANVAS = canvas

