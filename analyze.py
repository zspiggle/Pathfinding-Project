from time import *


class Analyze():
  
  startTime = 0   #time_ns()
  endTime = 0
  difference = 0

  def startTime(self):
    self.startTime = time()#time_ns()


  def endTime(self):
    self.endTime = time()#time_ns()
    self.difference = self.endTime - self.startTime


  def getSecs(self):
    return (self.difference)# * 0.001)  
  
  def reset(self):
    self.startTime = 0
    self.endTime = 0
    self.difference = 0



