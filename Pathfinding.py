#IMPORTS
from asyncore import loop
import math
from pickle import GLOBAL
import tkinter as tk
from tkinter.tix import WINDOW
import threading
from time import *

from numpy import true_divide

#Custom imports
from layouts import *



#Contains global variables for all classes to use
class Globals:

  MAINWINDOW = None
  DEBUG = True

  ALGORITHM = "test"

  #Used by A*
  NEXT_INSPECT = None
  INCREMENT = 0.00001

  GRID_SIZE = 20
  SPACING = 0
  START_OFFSET = 20

  TILE_SIZE = 35

  ROOT = None

  TILES = []

  STARTTILE = None
  GOALTILE = None

  ALG_GOAL_TILE = None
  
  MAX_LEVEL = 5
  NEXT_LEVEL = 1

  stepPosition = 1

class Window(tk.Frame):

  canvas = None

  

  

  upperFrame = None
  analyticFrame = None
  controlFrame = None
  outputFrame = None
  timeFrame = None

  lbl_time_var = None
  lbl_op = None




  def __init__(self):
    super().__init__()

    self.initUI()

  def passTiles(self, tileRef):
    self.tiles = tileRef

#needs cleaned up
  def initUI(self):

    Globals.MAINWINDOW = self 

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






    # self.canvasFrame.pack()#side = tk.LEFT)

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

    astar2Button = tk.Button(self.controlFrame, text="A* +C", command=astar_withC_algorithm)
    astar2Button.pack(side = tk.RIGHT)

    astar3Button = tk.Button(self.controlFrame, text="A* +C Local Vision", command=astar_withC_LOCAL_algorithm)
    astar3Button.pack(side = tk.RIGHT)

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

  #Changes the time label value
  def update_time(self, value):
    self.lbl_time_var["text"] = str(value)

  #Changes the output label value
  def set_output(self, value):
    self.lbl_op["text"] = str(value)
    #self.lbl_op.pack()

  #Redraws all tiles on canvas with updated states
  def redraw(self):
    for tileList in Globals.TILES:
      for tile in tileList:
        self.draw_tile(tile)


  def draw_tile(self, tile):
    xPos = tile.positionX * Globals.TILE_SIZE
    yPos = tile.positionY * Globals.TILE_SIZE
    self.canvas.create_rectangle(xPos, yPos, xPos+Globals.TILE_SIZE, yPos+Globals.TILE_SIZE, outline="#000", fill=tile.get_color())

    #Displays value
    if (Globals.DEBUG == True):
      if Globals.ALGORITHM == "Dijk":
        self.canvas.create_text(xPos + math.floor(Globals.TILE_SIZE/2), yPos + math.floor(Globals.TILE_SIZE/2), text=str(round(tile.dijk_value, 3)))
      elif Globals.ALGORITHM == "A*+CL":
        self.canvas.create_text(xPos + math.floor(Globals.TILE_SIZE/2), yPos + math.floor(Globals.TILE_SIZE/2), text=str(round(tile.step, 2)))
      else:
        self.canvas.create_text(xPos + math.floor(Globals.TILE_SIZE/2), yPos + math.floor(Globals.TILE_SIZE/2), text=str(round(tile.F_Value(), 2)))
        #tile.astar_G_value))#round(tile.F_Value(), 2)))


  #Loads a map with new tile states
  def loadMap(self, newTileTypes):

    #Counter could be a for in range

    counter = 0

    self.canvas.delete("all")
    
    for lis in Globals.TILES:
      for t in lis:
        t.tileType = newTileTypes[counter]

        if (t.tileType == 2):
          self.goalTile = t
          Globals.GOALTILE = t

        elif (t.tileType == 3):
          self.startingTile = t
          Globals.STARTTILE = t


        self.draw_tile(t)

        counter += 1

    #self.redraw(self.tiles)

# =======================================================================================================
#BUTTON COMMANDS (CANT PUT THESE INTO A CLASS FOR SOME REASON)

#Runs test Algorithm
def testAlgorithm():
  newThread = mainThread()

  Globals.ALGORITHM = "test"
  newThread.start()


#Runs AStar
def astarAlgorithm():
  newThread = mainThread()

  Globals.ALGORITHM = "A*"

  newThread.start()

def astar_withC_algorithm():
  newThread = mainThread()

  Globals.ALGORITHM = "A*+C"

  newThread.start()

def astar_withC_LOCAL_algorithm():
  newThread = mainThread()

  Globals.ALGORITHM = "A*+CL"

  newThread.start()


#Runs Dijkstras, may not be needed anymore
def dijkstraAlgorithm():
  newThread = mainThread()

  Globals.ALGORITHM = algorithm = "Dijk"

  newThread.start()
  
#Resets tiles and redraws
def reset():
  #print("Resetting")

  for l in Globals.TILES:
    for t in l:
      t.dijk_value = 99999
      t.astar_G_value = 0#99999
      t.astar_H_value = 0#99999
      t.inspected = False
      t.selected = False
  Globals.ALG_GOAL_TILE = None
  Globals.MAINWINDOW.set_output("-")
  Globals.MAINWINDOW.update_time(0)
  Globals.MAINWINDOW.redraw()

  Globals.stepPosition = 1

#Changes layout to something new
def changeLayout():

  reset()

  if Globals.NEXT_LEVEL <Globals.MAX_LEVEL:
    Globals.NEXT_LEVEL += 1
  else:
    Globals.NEXT_LEVEL = 1

  newLayout = getLayout(Globals.NEXT_LEVEL)

  if newLayout != None:
    Globals.MAINWINDOW.loadMap(newLayout)
  else:
    print("Layout Not Found")
  
#Changes Debugs value (toggle)
def debug():
  if (Globals.DEBUG == True):
    Globals.DEBUG = False
  else:
    Globals.DEBUG = True



#========================================================================================================

#Thread Class
class mainThread(threading.Thread):

  analytics = None
  

  def run(self):
    self.analytics = Analyze()

    match Globals.ALGORITHM:
      case "test": self.testAlgorithm()
      case "A*": self.astarAlgorithm()
      case "Dijk": self.dijkstraAlgorithm()
      case "A*+C": self.astar_withC_Algorithm()
      case "A*+CL": self.localastar()

      case _: print("Algorithm Not Found")



  def testAlgorithm(self):
    print("RUNNING TEST ALGORITHM")

    self.analytics.startTime()
    # Window.MAINWINDOW.set_output("Running test algorithm")

    #print(tiles)
    startPosX, startPosY = Globals.STARTTILE.get_pos()

    foundGoal = False
    newposX = startPosX
    newposY = startPosY


    while (not foundGoal):
      newposX = newposX + 1

      #currentArray = tiles[newposY]
      currentTile = Globals.TILES[newposY][newposX]#currentArray[newposX]

      if currentTile.tileType != 1:
        currentTile.selected = True

        if(currentTile.tileType == 2):
          foundGoal = True
      else:
        break
    
    self.analytics.endTime()

    if foundGoal:
      Globals.MAINWINDOW.set_output("Test algorithm has found goal")
    else:
      Globals.MAINWINDOW.set_output("Test did not find goal")
    Globals.MAINWINDOW.redraw()
    Globals.MAINWINDOW.update_time(self.analytics.getSecs())


  def dijkstraAlgorithm(self):
    print("RUNNING DIJKSTRA's ALGORITHM")

    self.analytics.startTime()



    startPosX, startPosY = Globals.STARTTILE.get_pos()

    Globals.STARTTILE.dijk_value = -1

    foundGoal = False
    newposX = startPosX
    newposY = startPosY

    checkNeighborTiles = []
    upcomingTiles = []
    checkedTiles = []
    distanceFromStart = 1



    #Checking tile local functions
    def checkNeighbors(tileE):
      global foundGoal


      posX, posY = tileE.get_pos()

      if posY-1 >= 0:
        tileNorth = Globals.TILES[posY-1][posX]

        if ((tileNorth.inspected == False) and (tileNorth.tileType != 1)):
          foundGoal = checkTile(tileNorth)


      if posY+1 < Globals.GRID_SIZE:   
        tileSouth = Globals.TILES[posY+1][posX]

        if ((tileSouth.inspected == False) and (tileSouth.tileType != 1)):
          foundGoal = checkTile(tileSouth)

      if posX-1 >= 0:
        tileWest = Globals.TILES[posY][posX-1]

        if ((tileWest.inspected == False) and (tileWest.tileType != 1)):
          foundGoal = checkTile(tileWest)


      if posX+1 < Globals.GRID_SIZE: 
        tileEast = Globals.TILES[posY][posX+1]

        if ((tileEast.inspected == False) and (tileEast.tileType != 1)):
          foundGoal = checkTile(tileEast)


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
        Globals.ALG_GOAL_TILE = tileC

        return True
      else:
        return False


    checkNeighbors(Globals.TILES[newposY][newposX])

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
        tileNorth = Globals.TILES[posY-1][posX]
        neighbors.append(tileNorth)

      if posY+1 < Globals.GRID_SIZE:   
        tileSouth = Globals.TILES[posY+1][posX]
        neighbors.append(tileSouth)

      if posX-1 >= 0:
        tileWest = Globals.TILES[posY][posX-1]
        neighbors.append(tileWest)

      if posX+1 < Globals.GRID_SIZE: #LEVEL SIZE
        tileEast = Globals.TILES[posY][posX+1]
        neighbors.append(tileEast)

      if len(neighbors) > 0:
        smallestTile = neighbors[0]
        for tileX in neighbors:
          if tileX.dijk_value < smallestTile.dijk_value:
            smallestTile = tileX
        return smallestTile
      else:
        return None



    
    nextTile = Globals.ALG_GOAL_TILE
    #print(nextTile)

    if Globals.ALG_GOAL_TILE != None:
      for i in range(1, distanceFromStart):    
        nextTile = getSmallestNeighbor(nextTile)
        nextTile.selected = True



    #CLEANUP could be in own method
    self.analytics.endTime()
    if foundGoal:
      Globals.MAINWINDOW.set_output("Dijkstra has found goal")
    else:
      Globals.MAINWINDOW.set_output("Dijkstra did not find the goal")

    Globals.MAINWINDOW.redraw()

    #print(self.analytics.getSecs())
    Globals.MAINWINDOW.update_time(self.analytics.getSecs())
    





  def astarAlgorithm(self):
    print("RUNNING A* ALGORITHM")
    self.analytics.startTime()

    foundGoal = False

    distanceFromStart = 1

    openList = []
    closedList = []

    #start by adding current position to closedList
    closedList.append(Globals.STARTTILE)


    #def heuristic(a,b):
    #  return math.sqrt((b.positionX - a.positionX)**2 + (b.positionY - a.positionY)**2 ) 

    #Goal , Destination 
    def distanceFormula(tileOne, tileTwo):  
      return abs(tileTwo.positionY - tileOne.positionY) + abs(tileTwo.positionX - tileOne.positionX)
      #return math.sqrt((tileTwo.positionY - tileOne.positionY)**2 + (tileTwo.positionX - tileOne.positionX)**2)

    def setAValues(tileT):
      tileT.astar_G_value = (tileT.prevTile.astar_G_value + 1) 
      tileT.astar_H_value = (distanceFormula(tileT, Globals.GOALTILE)) * 10


    def legalTile(someTile):
      # if exists
          
      if (someTile != None):

        # if not wall
        if(someTile.tileType != 1):

          # check if in closed list or open list
          if not (someTile in closedList):
            return True

      return False

    def adjacentTasks(tileCenter):
      # if exists

      tileBelow = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX]
      if (legalTile(tileBelow)):
        #if in open list then update
        if (tileBelow in openList):
          if(tileBelow.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileBelow, Globals.GOALTILE))):
            setAValues(tileBelow)
        else:
          tileBelow.inspected = True
          tileBelow.prevTile = tileCenter
          setAValues(tileBelow)
          openList.append(tileBelow)



      # if exists
      tileAbove = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX]
      if (legalTile(tileAbove)):
        if (tileAbove in openList):
          if(tileAbove.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileAbove, Globals.GOALTILE))):
            setAValues(tileAbove)
        else:
          tileAbove.inspected = True
          tileAbove.prevTile = tileCenter
          setAValues(tileAbove)
          openList.append(tileAbove)
      
      tileRight = Globals.TILES[tileCenter.positionY][tileCenter.positionX + 1]  
      if (legalTile(tileRight)):
        #if in open list then update
        if (tileRight in openList):

          if(tileRight.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileRight, Globals.GOALTILE))):
            setAValues(tileRight)

        else:
          tileRight.inspected = True
          tileRight.prevTile = tileCenter
          setAValues(tileRight)
          openList.append(tileRight)
      
      tileLeft = Globals.TILES[tileCenter.positionY][tileCenter.positionX - 1]
      if (legalTile(tileLeft)):
        #if in open list then update
        if (tileLeft in openList):
          if(tileLeft.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileLeft, Globals.GOALTILE))):
            setAValues(tileLeft)
        else:
          tileLeft.inspected = True
          tileLeft.prevTile = tileCenter
          setAValues(tileLeft)
          openList.append(tileLeft)
      



    #Add starting tile
    adjacentTasks(Globals.STARTTILE)

    def getLowest(tileList):
      lowestTile = tileList[0]
      for tileX in tileList:
        if (tileX.F_Value() < lowestTile.F_Value()):
          lowestTile = tileX
      return lowestTile

    #WHILE NOT FOUNDGOAL
    while(not foundGoal and len(openList) > 0):
      lowestT = getLowest(openList)
      adjacentTasks(lowestT)
      openList.remove(lowestT)
      closedList.append(lowestT)

      if(Globals.GOALTILE in openList):
        foundGoal = True
      
      #Globals.MAINWINDOW.redraw()

    #get lowest F value on open list
    #remove from open list, add to closed list
    #for each square T in adjacent tiles:
    #   if in closed, ignore
    #   if in open, if F score is lower with new path, update
    #   if not in open, add it and compute score
    
    #backtrack from goal with lowest F value

      
    #GO back now
    def getSmallestAdjacent(tileN):
      posX, posY = tileN.get_pos()

      neighbors = []

      if posY-1 >= 0:
        tileNorth = Globals.TILES[posY-1][posX]
        if tileNorth in closedList:
          neighbors.append(tileNorth)

      if posY+1 < Globals.GRID_SIZE:   
        tileSouth = Globals.TILES[posY+1][posX]
        if tileSouth in closedList:
          neighbors.append(tileSouth)

      if posX-1 >= 0:
        tileWest = Globals.TILES[posY][posX-1]
        if tileWest in closedList:
          neighbors.append(tileWest)

      if posX+1 < Globals.GRID_SIZE: #LEVEL SIZE
        tileEast = Globals.TILES[posY][posX+1]
        if tileEast in closedList:
          neighbors.append(tileEast)

      if len(neighbors) > 0:
        smallestTile = neighbors[0]
        for tileX in neighbors:
          if tileX.astar_G_value < smallestTile.astar_G_value:
            smallestTile = tileX
        return smallestTile
      else:
        return None
      

    if foundGoal:
      currentTile = Globals.GOALTILE
      while (currentTile.tileType != 3):
        print(currentTile.astar_G_value)
        currentTile = getSmallestAdjacent(currentTile)
        currentTile.selected = True

    
    #CLEANUP could be in own method
    self.analytics.endTime()

    if foundGoal:
      Globals.MAINWINDOW.set_output("A* has found goal")
    else:
      Globals.MAINWINDOW.set_output("A* did not find the goal")

    Globals.MAINWINDOW.redraw()

    print(self.analytics.getSecs())
    Globals.MAINWINDOW.update_time(self.analytics.getSecs())
    

  def astar_withC_Algorithm(self):
    print("RUNNING A*+C ALGORITHM")
    self.analytics.startTime()

    foundGoal = False

    distanceFromStart = 1

    openList = []
    closedList = []

    #start by adding current position to closedList
    closedList.append(Globals.STARTTILE)


    #def heuristic(a,b):
    #  return math.sqrt((b.positionX - a.positionX)**2 + (b.positionY - a.positionY)**2 ) 

    #Goal , Destination 
    def distanceFormula(tileOne, tileTwo):  
      return abs(tileTwo.positionY - tileOne.positionY) + abs(tileTwo.positionX - tileOne.positionX)
      #return math.sqrt((tileTwo.positionY - tileOne.positionY)**2 + (tileTwo.positionX - tileOne.positionX)**2)

    def setAValues(tileT):
      tileT.astar_G_value = (tileT.prevTile.astar_G_value + 1) 
      tileT.astar_H_value = (distanceFormula(tileT, Globals.GOALTILE)) * 10

    def setCornerAValues(tileK):
      tileK.astar_G_value = (tileK.prevTile.astar_G_value + 1.4) 
      tileK.astar_H_value = (distanceFormula(tileK, Globals.GOALTILE)) * 10

    def legalTile(someTile):
      # if exists
          
      if (someTile != None):

        # if not wall
        if(someTile.tileType != 1):

          # check if in closed list or open list
          if not (someTile in closedList):
            return True

      return False

    def adjacentTasks(tileCenter):
      # if exists

      tileBelow = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX]
      if (legalTile(tileBelow)):
        #if in open list then update
        if (tileBelow in openList):
          if(tileBelow.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileBelow, Globals.GOALTILE))):
            setAValues(tileBelow)
        else:
          tileBelow.inspected = True
          tileBelow.prevTile = tileCenter
          setAValues(tileBelow)
          openList.append(tileBelow)



      # if exists
      tileAbove = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX]
      if (legalTile(tileAbove)):
        if (tileAbove in openList):
          if(tileAbove.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileAbove, Globals.GOALTILE))):
            setAValues(tileAbove)
        else:
          tileAbove.inspected = True
          tileAbove.prevTile = tileCenter
          setAValues(tileAbove)
          openList.append(tileAbove)
      
      tileRight = Globals.TILES[tileCenter.positionY][tileCenter.positionX + 1]  
      if (legalTile(tileRight)):
        #if in open list then update
        if (tileRight in openList):

          if(tileRight.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileRight, Globals.GOALTILE))):
            setAValues(tileRight)

        else:
          tileRight.inspected = True
          tileRight.prevTile = tileCenter
          setAValues(tileRight)
          openList.append(tileRight)
      
      tileLeft = Globals.TILES[tileCenter.positionY][tileCenter.positionX - 1]
      if (legalTile(tileLeft)):
        #if in open list then update
        if (tileLeft in openList):
          if(tileLeft.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileLeft, Globals.GOALTILE))):
            setAValues(tileLeft)
        else:
          tileLeft.inspected = True
          tileLeft.prevTile = tileCenter
          setAValues(tileLeft)
          openList.append(tileLeft)
      
      tileUpLeft = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX - 1]
      if (legalTile(tileUpLeft)):
        #if in open list then update
        if (tileUpLeft in openList):
          if(tileUpLeft.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileUpLeft, Globals.GOALTILE))):
            setCornerAValues(tileUpLeft)
        else:
          tileUpLeft.inspected = True
          tileUpLeft.prevTile = tileCenter
          setCornerAValues(tileUpLeft)
          openList.append(tileUpLeft)

      tileUpRight = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX + 1]
      if (legalTile(tileUpRight)):
        #if in open list then update
        if (tileUpRight in openList):
          if(tileUpRight.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileUpRight, Globals.GOALTILE))):
            setCornerAValues(tileUpLeft)
        else:
          tileUpRight.inspected = True
          tileUpRight.prevTile = tileCenter
          setCornerAValues(tileUpRight)
          openList.append(tileUpRight)

      tileDownLeft = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX - 1]
      if (legalTile(tileDownLeft)):
        #if in open list then update
        if (tileDownLeft in openList):
          if(tileDownLeft.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileDownLeft, Globals.GOALTILE))):
            setCornerAValues(tileDownLeft)
        else:
          tileDownLeft.inspected = True
          tileDownLeft.prevTile = tileCenter
          setCornerAValues(tileDownLeft)
          openList.append(tileDownLeft)

      tileDownRight = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX + 1]
      if (legalTile(tileDownRight)):
        #if in open list then update
        if (tileDownRight in openList):
          if(tileDownRight.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileDownRight, Globals.GOALTILE))):
            setCornerAValues(tileDownRight)
        else:
          tileDownRight.inspected = True
          tileDownRight.prevTile = tileCenter
          setCornerAValues(tileDownRight)
          openList.append(tileDownRight)



    #Add starting tile
    adjacentTasks(Globals.STARTTILE)

    def getLowest(tileList):
      lowestTile = tileList[0]
      for tileX in tileList:
        if (tileX.F_Value() < lowestTile.F_Value()):
          lowestTile = tileX
      return lowestTile

    #WHILE NOT FOUNDGOAL
    while(not foundGoal and len(openList) > 0):
      lowestT = getLowest(openList)
      adjacentTasks(lowestT)
      openList.remove(lowestT)
      closedList.append(lowestT)

      if(Globals.GOALTILE in openList):
        foundGoal = True
      
      #Globals.MAINWINDOW.redraw()

    #get lowest F value on open list
    #remove from open list, add to closed list
    #for each square T in adjacent tiles:
    #   if in closed, ignore
    #   if in open, if F score is lower with new path, update
    #   if not in open, add it and compute score
    
    #backtrack from goal with lowest F value

      
    #GO back now
    def getSmallestAdjacent(tileN):
      posX, posY = tileN.get_pos()

      neighbors = []

      if posY-1 >= 0:
        tileNorth = Globals.TILES[posY-1][posX]
        if tileNorth in closedList:
          neighbors.append(tileNorth)

      if posY+1 < Globals.GRID_SIZE:   
        tileSouth = Globals.TILES[posY+1][posX]
        if tileSouth in closedList:
          neighbors.append(tileSouth)

      if posX-1 >= 0:
        tileWest = Globals.TILES[posY][posX-1]
        if tileWest in closedList:
          neighbors.append(tileWest)

      if posX+1 < Globals.GRID_SIZE: #LEVEL SIZE
        tileEast = Globals.TILES[posY][posX+1]
        if tileEast in closedList:
          neighbors.append(tileEast)

      if ((posX+1 < Globals.GRID_SIZE) and (posY-1 < Globals.GRID_SIZE)):
        tileNorthEast = Globals.TILES[posY-1][posX+1]
        if tileNorthEast in closedList:
          neighbors.append(tileNorthEast)

      if ((posX-1 < Globals.GRID_SIZE) and (posY-1 < Globals.GRID_SIZE)):
        tileNorthWest = Globals.TILES[posY-1][posX-1]
        if tileNorthWest in closedList:
          neighbors.append(tileNorthWest)

      if ((posX+1 < Globals.GRID_SIZE) and (posY+1 < Globals.GRID_SIZE)):
        tileSouthEast = Globals.TILES[posY+1][posX+1]
        if tileSouthEast in closedList:
          neighbors.append(tileSouthEast)

      if ((posX-1 < Globals.GRID_SIZE) and (posY+1 < Globals.GRID_SIZE)):
        tileSouthWest = Globals.TILES[posY+1][posX-1]
        if tileSouthWest in closedList:
          neighbors.append(tileSouthWest)

      if len(neighbors) > 0:
        smallestTile = neighbors[0]
        for tileX in neighbors:
          if tileX.astar_G_value < smallestTile.astar_G_value:
            smallestTile = tileX
        return smallestTile
      else:
        return None
      

    if foundGoal:
      currentTile = Globals.GOALTILE
      while (currentTile.tileType != 3):
        print(currentTile.astar_G_value)
        currentTile = getSmallestAdjacent(currentTile)
        currentTile.selected = True

    
    #CLEANUP could be in own method
    self.analytics.endTime()

    if foundGoal:
      Globals.MAINWINDOW.set_output("A* has found goal")
    else:
      Globals.MAINWINDOW.set_output("A* did not find the goal")

    Globals.MAINWINDOW.redraw()

    print(self.analytics.getSecs())
    Globals.MAINWINDOW.update_time(self.analytics.getSecs())


  def localastar(self):
    print("RUNNING A* Local ALGORITHM")
    self.analytics.startTime()

    foundGoal = False

    distanceFromStart = 1

    Globals.stepPosition = 1

    openList = []
    closedList = []

    #start by adding current position to closedList
    closedList.append(Globals.STARTTILE)


    

    #def heuristic(a,b):
    #  return math.sqrt((b.positionX - a.positionX)**2 + (b.positionY - a.positionY)**2 ) 

    #Goal , Destination 
    def distanceFormula(tileOne, tileTwo):  
      return abs(tileTwo.positionY - tileOne.positionY) + abs(tileTwo.positionX - tileOne.positionX)
      #return math.sqrt((tileTwo.positionY - tileOne.positionY)**2 + (tileTwo.positionX - tileOne.positionX)**2)

    def setAValues(tileT):
      tileT.astar_G_value = (tileT.prevTile.astar_G_value + 1) 
      tileT.astar_H_value = (distanceFormula(tileT, Globals.GOALTILE)) * 10

    def setCornerAValues(tileK):
      tileK.astar_G_value = (tileK.prevTile.astar_G_value + 1.4) 
      tileK.astar_H_value = (distanceFormula(tileK, Globals.GOALTILE)) * 10

    def legalTile(someTile):
      # if exists
          
      if (someTile != None):

        # if not wall
        if(someTile.tileType != 1):

          # check if in closed list or open list
          if not (someTile in closedList):
            return True

      return False

    def adjacentTasks(tileCenter):
      tileCenter.step = Globals.stepPosition
      Globals.stepPosition += 1
      tileCenter.selected = True

      # if exists

      tileBelow = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX]
      if (legalTile(tileBelow)):
        #if in open list then update
        if (tileBelow in openList):
          if(tileBelow.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileBelow, Globals.GOALTILE))):
            setAValues(tileBelow)
        else:
          tileBelow.inspected = True
          tileBelow.prevTile = tileCenter
          setAValues(tileBelow)
          openList.append(tileBelow)



      # if exists
      tileAbove = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX]
      if (legalTile(tileAbove)):
        if (tileAbove in openList):
          if(tileAbove.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileAbove, Globals.GOALTILE))):
            setAValues(tileAbove)
        else:
          tileAbove.inspected = True
          tileAbove.prevTile = tileCenter
          setAValues(tileAbove)
          openList.append(tileAbove)
      
      tileRight = Globals.TILES[tileCenter.positionY][tileCenter.positionX + 1]  
      if (legalTile(tileRight)):
        #if in open list then update
        if (tileRight in openList):

          if(tileRight.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileRight, Globals.GOALTILE))):
            setAValues(tileRight)

        else:
          tileRight.inspected = True
          tileRight.prevTile = tileCenter
          setAValues(tileRight)
          openList.append(tileRight)
      
      tileLeft = Globals.TILES[tileCenter.positionY][tileCenter.positionX - 1]
      if (legalTile(tileLeft)):
        #if in open list then update
        if (tileLeft in openList):
          if(tileLeft.F_Value() > ((tileCenter.astar_G_value + 1) + distanceFormula(tileLeft, Globals.GOALTILE))):
            setAValues(tileLeft)
        else:
          tileLeft.inspected = True
          tileLeft.prevTile = tileCenter
          setAValues(tileLeft)
          openList.append(tileLeft)
      
      tileUpLeft = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX - 1]
      if (legalTile(tileUpLeft)):
        #if in open list then update
        if (tileUpLeft in openList):
          if(tileUpLeft.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileUpLeft, Globals.GOALTILE))):
            setCornerAValues(tileUpLeft)
        else:
          tileUpLeft.inspected = True
          tileUpLeft.prevTile = tileCenter
          setCornerAValues(tileUpLeft)
          openList.append(tileUpLeft)

      tileUpRight = Globals.TILES[tileCenter.positionY - 1][tileCenter.positionX + 1]
      if (legalTile(tileUpRight)):
        #if in open list then update
        if (tileUpRight in openList):
          if(tileUpRight.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileUpRight, Globals.GOALTILE))):
            setCornerAValues(tileUpLeft)
        else:
          tileUpRight.inspected = True
          tileUpRight.prevTile = tileCenter
          setCornerAValues(tileUpRight)
          openList.append(tileUpRight)

      tileDownLeft = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX - 1]
      if (legalTile(tileDownLeft)):
        #if in open list then update
        if (tileDownLeft in openList):
          if(tileDownLeft.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileDownLeft, Globals.GOALTILE))):
            setCornerAValues(tileDownLeft)
        else:
          tileDownLeft.inspected = True
          tileDownLeft.prevTile = tileCenter
          setCornerAValues(tileDownLeft)
          openList.append(tileDownLeft)

      tileDownRight = Globals.TILES[tileCenter.positionY + 1][tileCenter.positionX + 1]
      if (legalTile(tileDownRight)):
        #if in open list then update
        if (tileDownRight in openList):
          if(tileDownRight.F_Value() > ((tileCenter.astar_G_value + 1.4) + distanceFormula(tileDownRight, Globals.GOALTILE))):
            setCornerAValues(tileDownRight)
        else:
          tileDownRight.inspected = True
          tileDownRight.prevTile = tileCenter
          setCornerAValues(tileDownRight)
          openList.append(tileDownRight)



    #Add starting tile
    adjacentTasks(Globals.STARTTILE)

    def getLowest(tileList):
      lowestTile = tileList[0]
      for tileX in tileList:
        if (tileX.F_Value() < lowestTile.F_Value()):
          lowestTile = tileX
      return lowestTile

    #WHILE NOT FOUNDGOAL
    while(not foundGoal and len(openList) > 0):
      lowestT = getLowest(openList)
      adjacentTasks(lowestT)
      openList.remove(lowestT)
      closedList.append(lowestT)

      if(Globals.GOALTILE in openList):
        foundGoal = True
      
      #Globals.MAINWINDOW.redraw()

    #get lowest F value on open list
    #remove from open list, add to closed list
    #for each square T in adjacent tiles:
    #   if in closed, ignore
    #   if in open, if F score is lower with new path, update
    #   if not in open, add it and compute score
    
    #backtrack from goal with lowest F value

    """
    #GO back now
    # def getSmallestAdjacent(tileN):
    #   posX, posY = tileN.get_pos()

    #   neighbors = []

    #   if posY-1 >= 0:
    #     tileNorth = Globals.TILES[posY-1][posX]
    #     if tileNorth in closedList:
    #       neighbors.append(tileNorth)

    #   if posY+1 < Globals.GRID_SIZE:   
    #     tileSouth = Globals.TILES[posY+1][posX]
    #     if tileSouth in closedList:
    #       neighbors.append(tileSouth)

    #   if posX-1 >= 0:
    #     tileWest = Globals.TILES[posY][posX-1]
    #     if tileWest in closedList:
    #       neighbors.append(tileWest)

    #   if posX+1 < Globals.GRID_SIZE: #LEVEL SIZE
    #     tileEast = Globals.TILES[posY][posX+1]
    #     if tileEast in closedList:
    #       neighbors.append(tileEast)

    #   if ((posX+1 < Globals.GRID_SIZE) and (posY-1 < Globals.GRID_SIZE)):
    #     tileNorthEast = Globals.TILES[posY-1][posX+1]
    #     if tileNorthEast in closedList:
    #       neighbors.append(tileNorthEast)

    #   if ((posX-1 < Globals.GRID_SIZE) and (posY-1 < Globals.GRID_SIZE)):
    #     tileNorthWest = Globals.TILES[posY-1][posX-1]
    #     if tileNorthWest in closedList:
    #       neighbors.append(tileNorthWest)

    #   if ((posX+1 < Globals.GRID_SIZE) and (posY+1 < Globals.GRID_SIZE)):
    #     tileSouthEast = Globals.TILES[posY+1][posX+1]
    #     if tileSouthEast in closedList:
    #       neighbors.append(tileSouthEast)

    #   if ((posX-1 < Globals.GRID_SIZE) and (posY+1 < Globals.GRID_SIZE)):
    #     tileSouthWest = Globals.TILES[posY+1][posX-1]
    #     if tileSouthWest in closedList:
    #       neighbors.append(tileSouthWest)

    #   if len(neighbors) > 0:
    #     smallestTile = neighbors[0]
    #     for tileX in neighbors:
    #       if tileX.astar_G_value < smallestTile.astar_G_value:
    #         smallestTile = tileX
    #     return smallestTile
    #   else:
    #     return None
      

    # if foundGoal:
    #   currentTile = Globals.GOALTILE
    #   while (currentTile.tileType != 3):
    #     print(currentTile.astar_G_value)
    #     currentTile = getSmallestAdjacent(currentTile)
    #     currentTile.selected = True
    """
    
    #CLEANUP could be in own method
    self.analytics.endTime()

    if foundGoal:
      Globals.MAINWINDOW.set_output("A* Local has found goal")
    else:
      Globals.MAINWINDOW.set_output("A* Local did not find the goal")

    Globals.MAINWINDOW.redraw()

    print(self.analytics.getSecs())
    Globals.MAINWINDOW.update_time(self.analytics.getSecs())


#========================================================================================================



class Tile:

  positionX = 0
  positionY = 0
  tileType = 0

  selected = False
  inspected = False

  dijk_value = 99999

  astar_G_value = 0#99999
  astar_H_value = 0#99999

  prevTile = None



  #Step for local A*
  step = 0

  """
  Types:
  0-empty
  1-wall
  2-goal
  3-start
  """

  def get_color(self):
    match self.tileType:
      case 1:
        return "#345995"
      case 2:
        return "#399E5A"
      case 3:
        return "#26532B"

    if self.selected:
      return "#82204A"
    elif self.inspected:
      return "#F0E100"
    else:
      return "#A8E0FF"

            

  def set_type(self, t=0):
    self.tileType = t

  def get_pos(self):
    return self.positionX, self.positionY




  def __init__(self, posX=0, posY=0, type=0):
    self.positionX = posX
    self.positionY = posY

  def F_Value(self):
    return self.astar_G_value + self.astar_H_value

  

class Analyze():
  
  startTimeVal = 0   #time_ns()
  endTimeVal = 0
  difference = 0

  def startTime(self):
    self.startTimeVal = time_ns()#time()#time_ns()
    #print(self.startTimeVal)


  def endTime(self):
    self.endTimeVal = time_ns()#time()#time_ns()
    #print(self.endTimeVal)
    self.difference = self.endTimeVal - self.startTimeVal
    #print(self.difference)


  def getSecs(self):
    return self.difference 
  
  def reset(self):
    self.startTimeVal = 0
    self.endTimeVal = 0
    self.difference = 0



"""
Color Code:

light Green - Goal    Hex:#399E5A

Light Blue - Empty Tile Hex: #A8E0FF

Dark blue = Wall tile   Hex: #345995

Yellow - Inspected tile  Hex: #F0E100

Purple - Selected Tile    Hex: 82204A

Green - start   Hex: 26532B

"""



#Creates file of tiles
def create_field():
    for y in range(0, Globals.GRID_SIZE):

      appendedArray = []

      for x in range(0, Globals.GRID_SIZE):
        newTile = Tile(x,y,1)
        #draw_tile(win, newTile)
        appendedArray.append(newTile)
      
      Globals.TILES.append(appendedArray)


#Does nothing currently
def on_closing():
  #print("Closing")
  #mainThread.RUNNING = False
  Globals.ROOT.destroy()


#Sets up tkinter
def main():
  Globals.ROOT = tk.Tk()

  win = Window()


  # Fullscreen
  Globals.ROOT.attributes("-fullscreen", False)


  create_field()





  #redraw(win)
  win.redraw()

  win.canvas.pack(expand=1, fill=tk.BOTH) 
  win.pack()

  #win.passTiles(tiles)

  win.loadMap(getLayout(1))


  Globals.ROOT.protocol("WM_DELETE_WINDOW", on_closing)

  Globals.ROOT.mainloop()



if __name__ == '__main__':
    main()