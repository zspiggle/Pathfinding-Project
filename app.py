import math
import tkinter as tk
from tkinter.tix import WINDOW
import threading
from analyze import Analyze



from numpy import resize

#from field import Tile

from layouts import *

#from main_thread import mainThread



class Globals:
  LEVEL_SIZE = 20

  #Used by A*
  NEXT_INSPECT = None
  INCREMENT = 0.00001

class Window(tk.Frame):

  MAINWINDOW = None
  DEBUG = True
  GOALTILE = None #Tired of pythons crap

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
  maxLevel = 4

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

    dijkstraButton = tk.Button(self.controlFrame, text="Dijkstra", command=dijkstraAlgorithm)
    dijkstraButton.pack(side = tk.RIGHT)

    resetButton = tk.Button(self.controlFrame, text="RESET", command=reset)
    resetButton.pack(side = tk.LEFT)

    debugButton = tk.Button(self.controlFrame, text="DEBUG", command=debug)
    debugButton.pack(side = tk.LEFT)

    # startButton = tk.Button(self.controlFrame, text="START", command=startProcess)
    # startButton.pack()

    # endButton = tk.Button(self.controlFrame, text="END", command=endProcess)
    # endButton.pack()

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
    if (Window.DEBUG == True):
      if Window.MAINWINDOW.algorithm == "Dijk":
        self.canvas.create_text(xPos + math.floor(self.tile_size/2), yPos + math.floor(self.tile_size/2), text=str(round(tile.dijk_value, 3)))
      else:
        self.canvas.create_text(xPos + math.floor(self.tile_size/2), yPos + math.floor(self.tile_size/2), text=str(round(tile.get_star_value(), 3)))



  def loadMap(self, newTileTypes):
    counter = 0

    self.canvas.delete("all")
    
    for lis in self.tiles:
      for t in lis:
        t.tileType = newTileTypes[counter]

        if (t.tileType == 2):
          self.goalTile = t
          t.selected = True
          t.inspected = True
        elif (t.tileType == 3):
          self.startingTile = t
          t.selected = True
          t.inspected = True

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


# def startProcess():
#   print("Starting process")


# def endProcess():
#   print("End process")


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

def dijkstraAlgorithm():
  newThread = mainThread()

  Window.MAINWINDOW.algorithm = algorithm = "Dijk"
  newThread.passField(Window.MAINWINDOW.tiles)

  newThread.start()
  

def reset():
  #print("Resetting")

  for l in Window.MAINWINDOW.tiles:
    for t in l:
      t.dijk_value = 99999
      t.astar_G_value = 99999
      t.astar_H_value = 99999
      t.inspected = False
      t.selected = False
  Window.MAINWINDOW.set_output("-")
  Window.MAINWINDOW.update_time(0)
  Window.MAINWINDOW.redraw(Window.MAINWINDOW.tiles)


def changeLayout():

  reset()

  if Window.MAINWINDOW.nextLevel < Window.MAINWINDOW.maxLevel: #THIS IS THE MAX NUMBER OF LEVELS IN LAYOUTS, DO NOT FORGET TO CHANGE THIS WHENEVER ADDING A LEVEL
    Window.MAINWINDOW.nextLevel += 1
  else:
    Window.MAINWINDOW.nextLevel = 1

  newLayout = getLayout(Window.MAINWINDOW.nextLevel)

  if newLayout != None:
    Window.MAINWINDOW.loadMap(newLayout)
  else:
    print("Layout Not Found")
  
def debug():
  if (Window.DEBUG == True):
    Window.DEBUG = False
  else:
    Window.DEBUG = True



#========================================================================================================


class mainThread(threading.Thread):

  #RUNNING = False

  #REDRAW = False

  algorithm = "test"

  analytics = None
  

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
    self.analytics = Analyze()

    self.algorithm = Window.MAINWINDOW.algorithm

    match self.algorithm:
      case "test": self.testAlgorithm()
      case "A*": self.astarAlgorithm()
      case "Dijk": self.dijkstraAlgorithm()

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
    print("RUNNING TEST ALGORITHM")

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

      if currentTile.tileType != 1:
        currentTile.selected = True

        if(currentTile.tileType == 2):
          foundGoal = True
      else:
        break
    
    self.analytics.endTime()

    if foundGoal:
      Window.MAINWINDOW.set_output("Test algorithm has found goal")
    else:
      Window.MAINWINDOW.set_output("Test did not find goal")
    Window.MAINWINDOW.redraw(tiles)
    Window.MAINWINDOW.update_time(self.analytics.getSecs())
    #print(self.analytics.getSecs())


    #Window.RUNNING = 0

  def dijkstraAlgorithm(self):
    print("RUNNING DIJKSTRA's ALGORITHM")

    self.analytics.startTime()

    tiles = self.field


    startPosX, startPosY = Window.MAINWINDOW.startingTile.get_pos()

    Window.MAINWINDOW.startingTile.dijk_value = -1

    foundGoal = False
    newposX = startPosX
    newposY = startPosY

    checkNeighborTiles = []
    upcomingTiles = []
    checkedTiles = []
    distanceFromStart = 1

    Window.GOALTILE = None

    #Checking tile local functions
    def checkNeighbors(tileE):
      global foundGoal
      global goalTile

      posX, posY = tileE.get_pos()

      if posY-1 >= 0:
        tileNorth = tiles[posY-1][posX]

        if ((tileNorth.inspected == False) and (tileNorth.tileType != 1)):
          foundGoal = checkTile(tileNorth)

          # if foundGoal:
          #   goalTile = tileNorth

      if posY+1 < Globals.LEVEL_SIZE:   #LEVEL SIZE
        tileSouth = tiles[posY+1][posX]

        if ((tileSouth.inspected == False) and (tileSouth.tileType != 1)):
          foundGoal = checkTile(tileSouth)

        # if foundGoal:
        #     goalTile = tileSouth

      if posX-1 >= 0:
        tileWest = tiles[posY][posX-1]

        if ((tileWest.inspected == False) and (tileWest.tileType != 1)):
          foundGoal = checkTile(tileWest)

          # if foundGoal:
          #   goalTile = tileWest

      if posX+1 < Globals.LEVEL_SIZE: #LEVEL SIZE
        tileEast = tiles[posY][posX+1]

        if ((tileEast.inspected == False) and (tileEast.tileType != 1)):
          foundGoal = checkTile(tileEast)

          # if foundGoal:
          #   goalTile = tileEast

      return foundGoal



    def checkTile(tileC):

      checkedTiles.append(tileC)
      upcomingTiles.append(tileC)

      tileC.inspected = True

      #print(tileC)

      tileC.dijk_value = distanceFromStart

      #print(tileC.dijk_value)

      if tileC.tileType == 2:

        print("FOUND GOAL")
        Window.GOALTILE = tileC
        #print(Window.GOALTILE)
        return True
      else:
        return False


    checkNeighbors(tiles[newposY][newposX])

    checkNeighborTiles.clear()
    checkNeighborTiles = upcomingTiles[:]
    upcomingTiles.clear()


    #MAIN LOOP
    while (foundGoal == False):

      distanceFromStart = distanceFromStart + 1

      if len(checkNeighborTiles) == 0: #No elements, prevents infinite loops
        break


      for tileT in checkNeighborTiles:
        #print(tileT)
        #print(len(checkNeighborTiles))
        foundGoal = checkNeighbors(tileT)


        #checkNeighborTiles.remove(tileT)
    
      checkNeighborTiles.clear()
      checkNeighborTiles = upcomingTiles[:]
      upcomingTiles.clear()
  
      if distanceFromStart > 100:
        break
        
      #print(distanceFromStart)

    def getSmallestNeighbor(tileN):
      posX, posY = tileN.get_pos()

      neighbors = []

      if posY-1 >= 0:
        tileNorth = tiles[posY-1][posX]
        neighbors.append(tileNorth)

      if posY+1 < Globals.LEVEL_SIZE:   #LEVEL SIZE
        tileSouth = tiles[posY+1][posX]
        neighbors.append(tileSouth)

      if posX-1 >= 0:
        tileWest = tiles[posY][posX-1]
        neighbors.append(tileWest)

      if posX+1 < Globals.LEVEL_SIZE: #LEVEL SIZE
        tileEast = tiles[posY][posX+1]
        neighbors.append(tileEast)

      if len(neighbors) > 0:
        smallestTile = neighbors[0]
        for tileX in neighbors:
          if tileX.dijk_value < smallestTile.dijk_value:
            smallestTile = tileX
        return smallestTile
      else:
        return None



    
    nextTile = Window.GOALTILE
    #print(nextTile)

    if Window.GOALTILE != None:
      for i in range(1, distanceFromStart):
        
        nextTile = getSmallestNeighbor(nextTile)
        nextTile.selected = True



    #CLEANUP could be in own method
    self.analytics.endTime()
    if foundGoal:
      Window.MAINWINDOW.set_output("Dijkstra has found goal")
    else:
      Window.MAINWINDOW.set_output("Dijkstra did not find the goal")

    Window.MAINWINDOW.redraw(tiles)

    print(self.analytics.getSecs())
    Window.MAINWINDOW.update_time(self.analytics.getSecs())
    





  def astarAlgorithm(self):
    print("RUNNING A* ALGORITHM")

    self.analytics.startTime()

    tiles = self.field


    startPosX, startPosY = Window.MAINWINDOW.startingTile.get_pos()

    Window.MAINWINDOW.startingTile.astar_G_value = -1
    Window.MAINWINDOW.startingTile.astar_H_value = -1

    foundGoal = False
    newposX = startPosX
    newposY = startPosY

    Globals.INCREMENT = 0.0

    checkNeighborTiles = []

    nextOptions = []
    optionsTiles = []

    distanceFromStart = 1

    #Window.GOALTILE = None



    #Checking tile local functions
    def checkNeighbors(tileE):
      global foundGoal


      posX, posY = tileE.get_pos()

      if posY-1 >= 0:
        tileNorth = tiles[posY-1][posX]

        if ((tileNorth.inspected == False) and (tileNorth.tileType != 1)):
          foundGoal = checkTile(tileNorth)

          # if foundGoal:
          #   goalTile = tileNorth

      if posY+1 < Globals.LEVEL_SIZE:   #LEVEL SIZE
        tileSouth = tiles[posY+1][posX]

        if ((tileSouth.inspected == False) and (tileSouth.tileType != 1)):
          foundGoal = checkTile(tileSouth)

        # if foundGoal:
        #     goalTile = tileSouth

      if posX-1 >= 0:
        tileWest = tiles[posY][posX-1]

        if ((tileWest.inspected == False) and (tileWest.tileType != 1)):
          foundGoal = checkTile(tileWest)

          # if foundGoal:
          #   goalTile = tileWest

      if posX+1 < Globals.LEVEL_SIZE: #LEVEL SIZE
        tileEast = tiles[posY][posX+1]

        if ((tileEast.inspected == False) and (tileEast.tileType != 1)):
          foundGoal = checkTile(tileEast)

          # if foundGoal:
          #   goalTile = tileEast

      return foundGoal



    def checkTile(tileC):
      #global goalTile

      #checkedTiles.append(tileC)
      nextOptions.append(tileC)

      tileC.inspected = True

      #print(tileC)

      

      #heuristic function:
      goalX, goalY = Window.MAINWINDOW.goalTile.get_pos() #gets raw position
      tilePosX, tilePosY = tileC.get_pos() #gets current tile pos

      #goalWeight = 2
      #startWeight = 0.5

      

      tileC.astar_H_value = math.floor(((goalX - tilePosX)**2 + (goalY - tilePosY)**2)**(1/2)) / 1.001# + Globals.INCREMENT #Distance Formula

      tileC.astar_G_value = math.floor( (((tilePosX - startPosX)**2)**(1/2)) +  (((tilePosY - startPosY)**2)**(1/2))) + (distanceFromStart / 1000)  #+ Globals.INCREMENT #Raw distance from start

      #Globals.INCREMENT += 0.00001

      #print(tileC.dijk_value)

      if tileC.tileType == 2:
        global goalTile

        print("FOUND GOAL")
        Window.GOALTILE = tileC
        #print(Window.GOALTILE)
        return True
      else:
        return False


    checkNeighbors(tiles[newposY][newposX])
    for tileQ in nextOptions:
      optionsTiles.append(tileQ)
    nextOptions.clear()


    #set next inspect
    if len(optionsTiles) > 0:
        Globals.NEXT_INSPECT = optionsTiles[0]
        for i in range(0, len(optionsTiles)):

          #print(optionsTiles[i].get_star_value())
          if optionsTiles[i].get_star_value() < Globals.NEXT_INSPECT.get_star_value():
            Globals.NEXT_INSPECT = optionsTiles[i]

          #print(optionsTiles[i].inspected)
          #print("STUCK 2")
          print(Globals.NEXT_INSPECT)
        print("last")
        print(Globals.NEXT_INSPECT)



    #MAIN LOOP
    while (foundGoal == False):

      foundGoal = checkNeighbors(Globals.NEXT_INSPECT)
      optionsTiles.remove(Globals.NEXT_INSPECT)
      print(len(nextOptions))
      
      if len(nextOptions) > 0:
        for tileQ in nextOptions:
          #if (tileQ.inspected == False):
          optionsTiles.append(tileQ)
            #Globals.NEXT_INSPECT  = None
          print(tileQ.get_pos())
          #print("STUCK 4")
        nextOptions.clear()

      print(len(optionsTiles))

      #print("NOT STUCK")

      #print("STUCK 1")

      if len(optionsTiles) > 0:
        Globals.NEXT_INSPECT = optionsTiles[0]
        for i in range(0, len(optionsTiles)):

          #print(optionsTiles[i].get_star_value())
          if optionsTiles[i].get_star_value() < Globals.NEXT_INSPECT.get_star_value():
            Globals.NEXT_INSPECT = optionsTiles[i]

          #print(optionsTiles[i].inspected)
          #print("STUCK 2")
          print(Globals.NEXT_INSPECT)
        print("last")
        print(Globals.NEXT_INSPECT)
        #print(nextInspect.get_star_value())

        

      else:
        print("Breaking")
        break

      

      print(Globals.NEXT_INSPECT)

      
      distanceFromStart += 1
      #if len(optionsTiles) > 5:
      #  break


    Window.MAINWINDOW.redraw(tiles)



    def getSmallestNeighbor(tileN):
      posX, posY = tileN.get_pos()

      neighbors = []

      if posY-1 >= 0:
        tileNorth = tiles[posY-1][posX]
        neighbors.append(tileNorth)

      if posY+1 < Globals.LEVEL_SIZE:   #LEVEL SIZE
        tileSouth = tiles[posY+1][posX]
        neighbors.append(tileSouth)

      if posX-1 >= 0:
        tileWest = tiles[posY][posX-1]
        neighbors.append(tileWest)

      if posX+1 < Globals.LEVEL_SIZE: #LEVEL SIZE
        tileEast = tiles[posY][posX+1]
        neighbors.append(tileEast)

      if len(neighbors) > 0:
        smallestTile = neighbors[0]
        for tileX in neighbors:
          if tileX.tileType == 3:
            return tileX

          if ((tileX.get_star_value() < smallestTile.get_star_value()) and (tileX.selected == False)):
            smallestTile = tileX
        #smallestTile.selected = True
        return smallestTile
      else:
        return None



    
    nextTile = Window.GOALTILE
    #print(nextTile)

    if foundGoal:
      #Starting values
      #sPosX, sPosY = Window.MAINWINDOW.startingTile.get_pos()
      #gPosX, gPosY = Window.GOALTILE.get_pos()
      #tilesNeeded = math.floor(((gPosX - sPosX)**2)**(1/2)) +  (((gPosY - sPosY)**2)**(1/2))

      reachedStart = False
      while (not reachedStart):
        print(nextTile.get_pos())
        nextTile = getSmallestNeighbor(nextTile)
        if(nextTile.tileType == 3):
          reachedStart = True
        nextTile.selected = True
        #Window.MAINWINDOW.redraw(tiles)
      #for i in range(1, int(tilesNeeded)):
        
        


    #CLEANUP could be in own method
    self.analytics.endTime()

    if foundGoal:
      Window.MAINWINDOW.set_output("A* has found goal")
    else:
      Window.MAINWINDOW.set_output("A* did not find the goal")

    Window.MAINWINDOW.redraw(tiles)

    print(self.analytics.getSecs())
    Window.MAINWINDOW.update_time(self.analytics.getSecs())
    
