import math
import tkinter as tk
from tkinter.tix import WINDOW
import threading
from analyze import Analyze



from numpy import resize

#from field import Tile

from layouts import *

from main_thread import mainThread


class Window(tk.Frame):

  MAINWINDOW = None

  #RUNNING = 0
  #RUN_TEST_ALG = 0
  #RUN_A_STAR = 0

  canvas = 0

  tile_size = 35

  upperFrame = None
  analyticFrame = None
  controlFrame = None
  outputFrame = None
  timeFrame = None

  lbl_time_var = None
  lbl_op = None

  tiles = None

  startingTile = None
  goalTile = None

  nextLevel = 1
  maxLevel = 3

  algorithm = "test"

  def __init__(self):
    super().__init__()

    self.initUI()

  def passTiles(self, tileRef):
    self.tiles = tileRef

  def initUI(self):

    Window.MAINWINDOW = self 

    self.master.title("Pathfinding")


    #self.canvasFrame = tk.Frame(self)    
    self.upperFrame = tk.Frame(self)
    self.controlFrame = tk.Frame(self.upperFrame)
    self.analyticFrame = tk.Frame(self.upperFrame)
    self.timeFrame = tk.Frame(self.analyticFrame)
    self.outputFrame = tk.Frame(self.analyticFrame)
    
    
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

    lbl_time = tk.Label(self.timeFrame, text="Time: ")
    lbl_time.pack()#side=tk.RIGHT, padx=5, pady=5)

    lbl_op_message = tk.Label(self.outputFrame, text="Output: ")
    lbl_op_message.pack()#side = tk.RIGHT)#side=tk.RIGHT, padx=5, pady=5)

    self.lbl_op = tk.Label(self.outputFrame, text="-")
    self.lbl_op.pack()#side = tk.RIGHT)

    testButton = tk.Button(self.controlFrame, text="TEST", command=testAlgorithm)
    testButton.pack(side = tk.RIGHT)

    astarButton = tk.Button(self.controlFrame, text="A*", command=astarAlgorithm)
    astarButton.pack(side = tk.RIGHT)

    resetButton = tk.Button(self.controlFrame, text="RESET", command=reset)
    resetButton.pack(side = tk.LEFT)

    startButton = tk.Button(self.controlFrame, text="START", command=startProcess)
    startButton.pack()

    endButton = tk.Button(self.controlFrame, text="END", command=endProcess)
    endButton.pack()

    changeLevelButton = tk.Button(self.controlFrame, text="CHANGE LEVEL", command=changeLayout)
    changeLevelButton.pack()


    self.lbl_time_var = tk.Label(self.timeFrame, text="-")
    self.lbl_time_var.pack()


    self.controlFrame.pack(side=tk.LEFT)
    self.timeFrame.pack(side=tk.LEFT)
    self.outputFrame.pack(side=tk.RIGHT)
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

  def set_output(self, value):
    self.lbl_op["text"] = str(value)
    self.lbl_op.pack()

  def redraw(self, tiles):
    for tileList in tiles:
      for tile in tileList:
        self.draw_tile(tile)


  def draw_tile(self, tile):
    xPos = tile.positionX * self.tile_size
    yPos = tile.positionY * self.tile_size
    self.canvas.create_rectangle(xPos, yPos, xPos+self.tile_size, yPos+self.tile_size, outline="#000", fill=tile.get_color())



  def loadMap(self, newTileTypes):
    counter = 0

    self.canvas.delete("all")
    
    for lis in self.tiles:
      for t in lis:
        t.tileType = newTileTypes[counter]

        if (t.tileType == 2):
          self.goalTile = t
        elif (t.tileType == 3):
          self.startingTile = t

        self.draw_tile(t)
        counter += 1

    #self.redraw(self.tiles)

#---------------------------------

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


def testAlgorithm():
  newThread = mainThread()

  Window.MAINWINDOW.algorithm = algorithm = "test"
  newThread.passField(Window.MAINWINDOW.tiles)

  newThread.start()

  # if (Window.RUNNING == 0):
  #   Window.RUN_TEST_ALG = 1

def astarAlgorithm():
  newThread = mainThread()

  Window.MAINWINDOW.algorithm = algorithm = "A*"
  newThread.passField(Window.MAINWINDOW.tiles)

  newThread.start()
  
  # if (Window.RUNNING == 0):
  #   Window.RUN_A_STAR = 1
  #   Window.RUNNING = 1

def reset():
  #print("Resetting")

  for l in Window.MAINWINDOW.tiles:
    for t in l:
      t.inspected = False
      t.selected = False
  Window.MAINWINDOW.set_output("-")
  Window.MAINWINDOW.update_time(0)
  Window.MAINWINDOW.redraw(Window.MAINWINDOW.tiles)


def changeLayout():
  if Window.MAINWINDOW.nextLevel <= Window.MAINWINDOW.maxLevel: #THIS IS THE MAX NUMBER OF LEVELS IN LAYOUTS, DO NOT FORGET TO CHANGE THIS WHENEVER ADDING A LEVEL
    Window.MAINWINDOW.nextLevel += 1
  else:
    Window.MAINWINDOW.nextLevel = 1

  newLayout = getLayout(Window.MAINWINDOW.nextLevel)

  if newLayout != None:
    Window.MAINWINDOW.loadMap(newLayout)
  else:
    print("Layout Not Found")
  

#========================================================================================================

"""
class mainThread(threading.Thread):

  #RUNNING = False

  #REDRAW = False

  algorithm = "test"

  analytics = Analyze()
  

  field = None 
  #startingTile = None
  #goalTile = None


  def passField(self, tiles):
    self.field = tiles



  def find_tile(self, posX, posY):

    findArray = self.field[posY] 
    tile = findArray[posX]
    return tile


  def run(self):
    algorithm = Window.MAINWINDOW.algorithm

    match self.algorithm:
      case "test": self.testAlgorithm()
      case "A*": self.astarAlgorithm()

      case _: print("Algorithm Not Found")

    
    
    #mainThread.RUNNING = True

    # while (mainThread.RUNNING):
    #   if (Window.RUN_TEST_ALG == 1):
    #     #print("DID IT")
    #     self.testAlgorithm()
    #     Window.RUN_TEST_ALG = 0

    #   if (Window.RUN_A_STAR == 1):
    #     #print("DID IT")
    #     self.astarAlgorithm()
    #     Window.RUN_A_STAR = 0 


  def testAlgorithm(self):
    self.analytics.startTime()
    # Window.MAINWINDOW.set_output("Running test algorithm")

    tiles = self.field
    #print(tiles)
    startPosX, startPosY = Window.MAINWINDOW.startingTile.get_pos()

    foundGoal = False
    newposX = startPosX
    newposY = startPosY

    while (not foundGoal):
      newposX = newposX + 1

      #currentArray = tiles[newposY]
      currentTile = tiles[newposY][newposX]#currentArray[newposX]
      currentTile.selected = True

      if(currentTile.tileType == 2):
        foundGoal = True
    
    self.analytics.endTime()
    Window.MAINWINDOW.set_output("Test algorithm has found goal")

    Window.MAINWINDOW.redraw(tiles)
    Window.MAINWINDOW.update_time(self.analytics.getSecs())
    print(self.analytics.getSecs())


    #Window.RUNNING = 0

  def astarAlgorithm(self):

    self.analytics.startTime()
    # Window.MAINWINDOW.set_output("Running test algorithm")

    tiles = self.field
    #print(tiles)
    startPosX, startPosY = self.startingTile.get_pos()

    foundGoal = False
    newposX = startPosX
    newposY = startPosY

    while (not foundGoal):
      newposX = newposX + 1

      #currentArray = tiles[newposY]
      currentTile = tiles[newposY][newposX]#currentArray[newposX]
      currentTile.selected = True

      if(currentTile.tileType == 2):
        foundGoal = True
    
    self.analytics.endTime()
    Window.MAINWINDOW.set_output("A* has found goal")
    Window.MAINWINDOW.redraw(tiles)
    Window.MAINWINDOW.update_time(self.analytics.getSecs())
#    Window.RUNNING = 0 
    
"""