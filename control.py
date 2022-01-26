import tkinter as tk
from app import Window
from field import Tile

from array import *

tile_size = 35
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

def draw_tile(winndow, tile):
  xPos = tile.positionX * tile_size
  yPos = tile.positionY * tile_size
  winndow.canvas.create_rectangle(xPos, yPos, xPos+tile_size, yPos+tile_size, outline="#000", fill=tile.get_color())

def find_tile(posX, posY):
  for tile in tiles:
    if ((tile.positionX == posX) and (tile.positionY == posY)):
      return tile

def redraw(win):
  for tile in tiles:
    draw_tile(win, tile)

#Sets up tkinter
def main():
  root = tk.Tk()
  win = Window()


  for x in range(0, grid_size-1):
    for y in range(0, grid_size-1):
      newTile = Tile(x,y,1)
      #draw_tile(win, newTile)
      tiles.append(newTile)



  #print(tiles)

  for i in range(0, grid_size -1):
      t = find_tile(i,0)
      if t != None:
        t.set_type(1)
      print(t)
      t = find_tile(i,grid_size-1)
      if t != None:
        t.set_type(1)
      print(t)

  

  #root.geometry("400x100+300+300")

  redraw(win)

  win.canvas.pack(fill=tk.BOTH, expand=1) #Doesnt do anything
  win.pack(fill=tk.BOTH, expand=1)

  root.mainloop()




if __name__ == '__main__':
    main()