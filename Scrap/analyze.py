from time import *


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



