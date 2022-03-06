import time
import sys


import RPi.GPIO as GPIO
from Motor import *

class GLOBALS:
  DIRECTION = 0 #How many rotations

  STARTING_POINT_X = 0
  STARTING_POINT_Y = 0

  CURRENT_X = 0
  CURRENT_Y = 0

  GOAL_X = 0
  GOAL_Y = 10

  X_OFFSET = 0
  Y_OFFSET = 0

  TRIG = 27
  ECHO = 22

  PWM=Motor() 

  TILES = []



#SENSOR ============================
def setupPins():
  #SETUP GPIO PINS
  GPIO.setmode(GPIO.BCM)

  TRIG = 27
  ECHO = 22

  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.output(TRIG,0)

  GPIO.setup(ECHO, GPIO.IN)

  #Allows time for setup
  time.sleep(0.1)

#Returns Distance in CM
def getDistance():
  #TRIGGER
  GPIO.output(GLOBALS.TRIG, 1)
  time.sleep(0.00001)
  GPIO.output(GLOBALS.TRIG, 0)

  while GPIO.input(GLOBALS.ECHO) == 0:
          pass
  start = time.time()

  while GPIO.input(GLOBALS.ECHO) == 1:
          pass
  stop = time.time()


  return ((stop - start) * 17000) #Centimeters, 170 for "meters"

def scanForWall():
  scanDis = getDistance()

  if(scanDis < 17):
    return 1
  else:
    return 0


#MOTORS ===================================
def forward(secs):
  GLOBALS.PWM.setMotorModel(1000,1000,1000,1000) 
  time.sleep(secs) #HOW LONG TO GO FORWARD
  GLOBALS.PWM.setMotorModel(0,0,0,0)

def rotate(secs):
  GLOBALS.PWM.setMotorModel(1500,1500,-1500,-1500) 
  time.sleep(secs)
  #ALWAYS MAKE SURE TO CLEAR AFTERWARDS
  GLOBALS.PWM.setMotorModel(0,0,0,0)

def rotateTimes(dir): #number of rotations
  rotate(dir * 0.45)

def extendField():
  if(len(GLOBALS.TILES) <= GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET + 1):
    extend_field_y_positive()
  if(GLOBALS.Y_OFFSET * -1 >  GLOBALS.CURRENT_Y - 1):
    extend_field_y_negative()

  print(len(GLOBALS.TILES[0]))
  if(len(GLOBALS.TILES[0]) <= GLOBALS.CURRENT_X + GLOBALS.X_OFFSET + 1): #add 1 for buffer / remove 1 cause buffer
    extend_field_x_positive()
  if(GLOBALS.X_OFFSET * -1 > GLOBALS.CURRENT_X - 1):
    extend_field_x_negative()

def scanSurrondings():

  #information = [0, 0, 0, 0, 0, 0, 0, 0] #1 value for each of the 8 directions

  rotateSecs = 0.5
  waitTime = 0.25

  tempTile = None

  extendField()

  rotate(rotateSecs)

  time.sleep(waitTime)

  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET - 1][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET + 1]
  #NORTH EAST
  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()



  rotate(rotateSecs)
  time.sleep(waitTime)
  #EAST
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET + 1]
  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  rotate(rotateSecs)
  time.sleep(waitTime)
  #SOUTH EAST
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET + 1][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET + 1]

  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  rotate(rotateSecs)
  time.sleep(waitTime)
  #SOUTH 
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET + 1][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET]

  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  rotate(rotateSecs)
  time.sleep(waitTime)
  #SOUTH WEST
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET + 1][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET - 1]

  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  rotate(rotateSecs)
  time.sleep(waitTime)
  #WEST 
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET - 1]

  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  rotate(rotateSecs)
  time.sleep(waitTime)
  #NORTH WEST 
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET - 1][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET - 1]

  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  rotate(rotateSecs)
  time.sleep(waitTime)
  #NORTH 
  tempTile = GLOBALS.TILES[GLOBALS.CURRENT_Y + GLOBALS.Y_OFFSET - 1][GLOBALS.CURRENT_X + GLOBALS.X_OFFSET]

  if (tempTile.tileType != 2 and tempTile.tileType != 3):
    tempTile.tileType = scanForWall()

  
#ALGORITHM =====================================


class Tile:

  positionX = 0
  positionY = 0
  tileType = 0

  #selected = False
  #inspected = False

  astar_G_value = 0#99999
  astar_H_value = 0#99999

  prevTile = None



  #Step for local A*
  #step = 0

            

  def set_type(self, t=0):
    self.tileType = t

  # def get_pos(self):
  #   return self.positionX, self.positionY


  def __str__(self):
    return str(self.tileType)

  def __init__(self, posX=0, posY=0, type=0):
    self.positionX = posX
    self.positionY = posY
    self.tileType = type

  def F_Value(self):
    return self.astar_G_value + self.astar_H_value


def create_field():

  yList = []
  xList = []
  xList.append(Tile(0,0,3))
  yList.append(xList)
  GLOBALS.TILES = yList


  xNeg = False
  yNeg = False

  #SET OFFSET BASED ON GOAL:
  if GLOBALS.GOAL_X < 0:
    #GLOBALS.X_OFFSET = 0#GLOBALS.GOAL_X
    xNeg = True

  if GLOBALS.GOAL_Y < 0:
    #GLOBALS.Y_OFFSET = 0#GLOBALS.GOAL_Y
    yNeg = True

  #if negative, extend reverse

  for x in range(abs(GLOBALS.GOAL_X)):
    
    if (xNeg):
      extend_field_x_negative()
    else:
      extend_field_x_positive()

  for y in range(abs(GLOBALS.GOAL_Y)):
    
    if (yNeg):
      extend_field_y_negative()
    else:
      extend_field_y_positive()
    

  GLOBALS.TILES[GLOBALS.GOAL_Y + GLOBALS.Y_OFFSET][GLOBALS.GOAL_X + GLOBALS.X_OFFSET].tileType = 2



def extend_field_x_positive():

  print("Extending X Pos")

  count = 0

  for tileList in GLOBALS.TILES:
    newTile = Tile(len(tileList) + GLOBALS.X_OFFSET, count + GLOBALS.Y_OFFSET,5)
    tileList.append(newTile)

  # for y in range(0, len(GLOBALS.TILES)):
  #   newTile = Tile(GLOBALS.TILES[y][len(GLOBALS.TILES[y])-1].positionX + 1, GLOBALS.TILES[y][len(GLOBALS.TILES[y])-1].positionY, 5)
  #   GLOBALS.TILES[y].append(newTile)

def extend_field_x_negative():

  print("Extending X Neg")

  count = 0

  for tileList in GLOBALS.TILES:
    newTile = Tile(GLOBALS.X_OFFSET - 1, count + GLOBALS.Y_OFFSET,5)
    tileList.insert(0, newTile)

  # for y in range(0, len(GLOBALS.TILES)):
  #   newTile = Tile(y[len(y)-1].positionX - 1, y[len(y)-1].positionY, 5)
  #   GLOBALS.TILES[y].insert(0, newTile)
  GLOBALS.X_OFFSET += 1

def extend_field_y_negative():

  print("Extending Y Neg")

  newList = []
  for x in range(len(GLOBALS.TILES[0])):
    newTile = Tile(GLOBALS.TILES[0][x].positionX - 1, GLOBALS.TILES[0][x].positionY, 5) 
    newList.append(newTile)
  GLOBALS.TILES.insert(0, newList)

  GLOBALS.Y_OFFSET += 1

def extend_field_y_positive():

  print("Extending Y Pos")

  newList = []
  for x in range(len(GLOBALS.TILES[0])):
    newTile = Tile(GLOBALS.TILES[len(GLOBALS.TILES)-1][x].positionX - 1, GLOBALS.TILES[len(GLOBALS.TILES)-1][x].positionY, 5) 
    newList.append(newTile)
  GLOBALS.TILES.append(newList)
   


def print_field():
  for tileList in GLOBALS.TILES:
    for tile in tileList:
      print(str(tile.tileType), end=" ")
    print()


def print_globals():
  print("CURRENT X: ", GLOBALS.CURRENT_X)
  print("CURRENT Y: ", GLOBALS.CURRENT_Y)
  print("OFFSET X: ", GLOBALS.X_OFFSET)
  print("OFFSET Y: ", GLOBALS.Y_OFFSET)


def main():

  print("RUNNING AUTONOMOUS")

  GLOBALS.GOAL_X = int(sys.argv[1])
  GLOBALS.GOAL_Y = int(sys.argv[2])

  #Wait for 5 seconds to disconnect
  #time.sleep(3)
  setupPins()

  
  create_field()

  print("Testing print:")
  print_field()
  print("Finished Test Print")

  scanSurrondings()

  print()
  print("After Updating:")
  print_field()


def destory():
  GPIO.cleanup()



if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()

