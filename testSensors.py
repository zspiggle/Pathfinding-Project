import RPi.GPIO as GPIO
import time
from mpu6050 import mpu6050




TRIG = 23
ECHO = 24
mpu = mpu6050(0x68)


def setupPins():
  #SETUP GPIO PINS
  GPIO.setmode(GPIO.BCM)

  TRIG = 23
  ECHO = 24

  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.output(TRIG,0)

  GPIO.setup(ECHO, GPIO.IN)

  #Allows time for setup
  time.sleep(0.1)

#Returns Distance in CM
def getDistance():
  #TRIGGER
  GPIO.output(TRIG, 1)
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
    setupPins()

    print(getDistance())
    time.sleep(2)
    print(getDistance())
    time.sleep(2)

    while True:
      print("Temp : "+str(mpu.get_temp()))
      print()

      accel_data = mpu.get_accel_data()
      print("Acc X : "+str(accel_data['x']))
      print("Acc Y : "+str(accel_data['y']))
      print("Acc Z : "+str(accel_data['z']))
      print()

      gyro_data = mpu.get_gyro_data()
      print("Gyro X : "+str(gyro_data['x']))
      print("Gyro Y : "+str(gyro_data['y']))
      print("Gyro Z : "+str(gyro_data['z']))
      print()
      print("-------------------------------")
      time.sleep(1)
