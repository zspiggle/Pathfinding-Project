import tkinter as tk

from numpy import resize



class Window(tk.Frame):

  canvas = 0

  canvasFrame = None
  analyticFrame = None
  controlFrame = None

  def __init__(self):
    super().__init__()

    self.initUI()



  def initUI(self):

    self.master.title("Pathfinding")


    self.canvasFrame = tk.Frame(self)    
    self.controlFrame = tk.Frame(self)
    
    #screenwidth = self.master.winfo_screenwidth()
    #creenheight = self.master.winfo_screenheight()

    self.canvas = tk.Canvas(self, bg="red")#, width= screenwidth, height= screenheight )






  #  self.canvasFrame.pack()#side = tk.LEFT)

    testButton = tk.Button(self.controlFrame, text="Test", command=testButtonPress)
    testButton.pack(side=tk.LEFT)

    testLabel = tk.Label(self.controlFrame, text="AAHHH")
    testLabel.pack(side=tk.RIGHT, padx=5, pady=5)


    self.controlFrame.pack()
    self.canvas.pack()

    # canvas.create_rectangle(30, 10, 120, 80,
    #     outline="#fb0", fill="#fb0")
    # canvas.create_rectangle(150, 10, 240, 80,
    #     outline="#f50", fill="#f50")
    # canvas.create_rectangle(270, 10, 370, 80,
    #     outline="#05f", fill="#05f")

    #self.canvas.pack(fill=tk.BOTH, expand=1)

    self.pack(fill=tk.BOTH, expand=1)
    #self._CANVAS = canvas

    # self.pack(fill=tk.BOTH, expand=1)

def testButtonPress():
  print("Test")