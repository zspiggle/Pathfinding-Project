import RPi.GPIO as GPIO
import time


# FOR ROVER PI:
# TRIG = 23
# ECHO = 24
#
# FOR PROTO PI:
# TRIG = 27
# ECHO = 22

TRIG = 23
ECHO = 24



def setupPins():


  #SETUP GPIO PINS
  GPIO.setmode(GPIO.BCM)

  TRIG = 23
  ECHO = 24

  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.output(TRIG, 0)

  GPIO.setup(ECHO, GPIO.IN)

  #Allows time for setup
  time.sleep(0.1)

#Returns Distance in CM
def getDistance():
  #TRIGGER
  GPIO.output(TRIG, 1)
  #time.sleep(0.00001)
  time.sleep(0.00001)
  GPIO.output(TRIG, 0)

  while GPIO.input(ECHO) == 0:
    pass
  start = time.time()

  while GPIO.input(ECHO) == 1:
    pass
  stop = time.time()


  return ((stop - start) * 17000) #Centimeters, 170 for "meters"






if __name__ == "__main__":

  try:
    setupPins()

    print(getDistance())
    time.sleep(2)
    print(getDistance())

    GPIO.cleanup()

  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    GPIO.cleanup()



