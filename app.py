import math
import tkinter as tk

from numpy import resize



class Window(tk.Frame):

  canvas = 0

  upperFrame = None
  analyticFrame = None
  controlFrame = None

  lbl_time_var = None

  def __init__(self):
    super().__init__()

    self.initUI()



  def initUI(self):

    self.master.title("Pathfinding")


    #self.canvasFrame = tk.Frame(self)    
    self.upperFrame = tk.Frame(self)
    self.controlFrame = tk.Frame(self.upperFrame)
    self.analyticFrame = tk.Frame(self.upperFrame)

    
    #screenwidth = self.master.winfo_screenwidth()
    #creenheight = self.master.winfo_screenheight()

    self.canvas = tk.Canvas(self, bg="#778899")#, width= screenwidth, height= screenheight )






  #  self.canvasFrame.pack()#side = tk.LEFT)

    # testButton = tk.Button(self.controlFrame, text="Test", command=testButtonPress)
    # testButton.pack()#side=tk.LEFT)

    # testLabel = tk.Label(self.controlFrame, text="AAHHH")
    # testLabel.pack()#side=tk.RIGHT, padx=5, pady=5)

    lbl_analyze = tk.Label(self.analyticFrame, text="ANALYTICS")
    lbl_analyze.pack()#side=tk.RIGHT, padx=5, pady=5)

    lbl_time = tk.Label(self.analyticFrame, text="Time: ")
    lbl_time.pack()#side=tk.RIGHT, padx=5, pady=5)


    startButton = tk.Button(self.controlFrame, text="START", command=startProcess)
    startButton.pack()

    endButton = tk.Button(self.controlFrame, text="END", command=endProcess)
    endButton.pack()


    self.lbl_time_var = tk.Label(self.analyticFrame, text="-")
    self.lbl_time_var.pack()


    self.controlFrame.pack(side=tk.LEFT)
    self.analyticFrame.pack(side=tk.RIGHT, padx = 500)

    self.upperFrame.pack()


    self.canvas.pack()#side=tk.BOTTOM)

    #self.canvasFrame.pack()

    #self.canvas.pack(fill=tk.BOTH, expand=1)

    self.pack(fill=tk.BOTH, expand=1)
    #self._CANVAS = canvas

    # self.pack(fill=tk.BOTH, expand=1)

  def update_time(self, value):
    self.lbl_time_var["text"] = str(value)
    #self.lbl_time_var.pack()
    #self.analyticFrame.pack()
    #self.pack(fill=tk.BOTH, expand=1)


def shortenNumber(value):
  newValue = 10000 * value
  newValue = math.trunc(newValue)
  newValue = newValue * 0.00001
  return newValue

def testButtonPress():
  print("Test")


def startProcess():
  print("Starting process")


def endProcess():
  print("End process")

