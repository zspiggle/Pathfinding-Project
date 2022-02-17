from time import *


class Analyze():
  
  startTimeVal = 0   #time_ns()
  endTimeVal = 0
  difference = 0

  def startTime(self):
    self.startTimeVal = time()#time_ns()


  def endTime(self):
    self.endTimeVal = time()#time_ns()
    self.difference = self.endTimeVal - self.startTimeVal


  def getSecs(self):
    return self.difference 
  
  def reset(self):
    self.startTimeVal = 0
    self.endTimeVal = 0
    self.difference = 0



