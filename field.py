




class Tile:

  positionX = 0
  positionY = 0
  tileType = 0

  selected = False
  inspected = False

  dijk_value = 99999

  astar_value = 0


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

  
