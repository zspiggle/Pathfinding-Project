




class Tile:

  positionX = 0
  positionY = 0
  tileType = 0

  selected = False
  inspected = False

  """
  Types:
  0-empty
  1-wall
  2-goal
  3-start
  """

  def get_color(self):
    if self.tileType == 2 or self.tileType == 3:
      match self.tileType:
        case 2:
          return "#399E5A"
        case 3:
          return "#26532B"
    else:
      if self.selected:
        return "#82204A"
      elif self.inspected:
        return "#F0E100"
      else:
        match self.tileType:
          case 0:
            return "#A8E0FF"
          case 1:
            return "#345995"

  def set_type(self, t=0):
    self.tileType = t

  def get_pos(self):
    return self.positionX, self.positionY


  def __init__(self, posX=0, posY=0, type=0):
    self.positionX = posX
    self.positionY = posY

  
