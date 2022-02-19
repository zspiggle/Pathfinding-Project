import tkinter as tk

from app import Window
from field import Tile
#from analyze import *
#from main_thread import 

from array import *





grid_size = 20
spacing = 0
start_offset = 20


tiles = []

#Init array
#refactor as 2d array

"""
Colors:

light Green - Goal    Hex:#399E5A

Light Blue - Empty Tile Hex: #A8E0FF

Dark blue = Wall tile   Hex: #345995

Yellow - Inspected tile  Hex: #F0E100

Purple - Selected Tile    Hex: 82204A

Green - start   Hex: 26532B


"""

#def draw_tile(winndow, x=0, y=0):
  #winndow.canvas.create_rectangle(x, y, x+tile_size, y+tile_size, outline="#000", fill="#0AB2E5")



def find_tile(posX, posY):

  findArray = tiles[posY] 
  tile = findArray[posX]
  return tile


  # for tileList in tiles:
  #   for tile in tileList:
  #     if ((tile.positionX == posX) and (tile.positionY == posY)):
  #       return tile


def create_field():
    for y in range(0, grid_size):

      appendedArray = []

      for x in range(0, grid_size):
        newTile = Tile(x,y,1)
        #draw_tile(win, newTile)
        appendedArray.append(newTile)
      
      tiles.append(appendedArray)

def on_closing():
  #print("Closing")
  #mainThread.RUNNING = False
  root.destroy()


#Sets up tkinter
def main():
  #analytics = Analyze()
  #analytics.startTime()
  global root

  root = tk.Tk()

  #threadMain = mainThread()



  win = Window()


  # Fullscreen
  root.attributes("-fullscreen", False)

  #root.bind("<Escape>", )


  create_field()



  #Walls
  # for i in range(0, grid_size):
  #   t = find_tile(i,0)
  #   t.set_type(1)
  #   #print(t)
  #   t = find_tile(i,grid_size-1)
  #   t.set_type(1)
  #   #print(t)
  #   t = find_tile(0, i)
  #   t.set_type(1)

  #   t = find_tile(grid_size-1, i)
  #   t.set_type(1)
   

  
  # t = find_tile(9, 10)
  # t.set_type(3)
  # threadMain.startingTile = t
  # #startingTile = t

  # t = find_tile(15, 10)
  # t.set_type(2)
  # threadMain.goalTile = t
  

  #root.geometry("400x100+300+300")

  #redraw(win)
  win.redraw(tiles)

  win.canvas.pack(expand=1, fill=tk.BOTH) 
  win.pack()

  win.passTiles(tiles)

  win.loadMap(
    [
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]
  )

  #threadMain.passField(tiles)

  #threadMain.start()

  #analytics.endTime()
  #print(analytics.getSecs())

  
  #win.update_time(analytics.getSecs())

  root.protocol("WM_DELETE_WINDOW", on_closing)

  root.mainloop()

#def escape_key():
#  root.attributes("-fullscreen", False)


if __name__ == '__main__':
    main()


