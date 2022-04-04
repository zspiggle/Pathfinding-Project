from mpu6050 import mpu6050
import time

mpu = mpu6050(0x68)

staringTime = time.time_ns()
angle = 0

while True:

    gyro_data = mpu.get_gyro_data()
    endTime = time.time_ns()
    
    angle += ((endTime - staringTime) * 0.000000001) * gyro_data['z']

    staringTime = endTime

    if angle > 360:
      angle = 0
    if angle < 0:
      angle = 360 - angle

    print("Gyro X : "+str(gyro_data['x']))
    print("Gyro Y : "+str(gyro_data['y']))
    print("Gyro Z : "+str(gyro_data['z']))
    print()
    print(angle)
    print()
    print("-------------------------------")

    time.sleep(0.01)