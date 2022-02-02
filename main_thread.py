
import threading
from app import Window



#put threading class that handles all main logic

class mainThread(threading.Thread):

  RUNNING = False

  def run(self):
    
    mainThread.RUNNING = True

    while (mainThread.RUNNING):
      if (Window.RUN_TEST_ALG == 1):
        #print("DID IT")
        self.testAlgorithm()
        Window.RUN_TEST_ALG = 0

  def testAlgorithm(self):
    start = 
    Window.MAINWINDOW.set_output("Running test algorithm")
    
