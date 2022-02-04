
import threading
from tracemalloc import start
from app import Window
from analyze import Analyze


#put threading class that handles all main logic

class mainThread(threading.Thread):

  RUNNING = False

  REDRAW = False

  analytics = Analyze()
  

  field = None 
  startingTile = None
  goalTile = None


  def passField(self, tiles):
    self.field = tiles



  def find_tile(self, posX, posY):

    findArray = self.field[posY] 
    tile = findArray[posX]
    return tile


  def run(self):
    
    mainThread.RUNNING = True

    while (mainThread.RUNNING):
      if (Window.RUN_TEST_ALG == 1):
        #print("DID IT")
        self.testAlgorithm()
        Window.RUN_TEST_ALG = 0

  def testAlgorithm(self):
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
      currentTile.inspected = True

      if(currentTile.tileType == 2):
        foundGoal = True
    

    Window.MAINWINDOW.set_output("Test algorithm has found goal")
    self.analytics.endTime()
    Window.MAINWINDOW.redraw(tiles)
    Window.MAINWINDOW.update_time(self.analytics.getSecs())
    